#!/usr/bin/env python3
"""Validate Museum records, their Stream envelope commitments, and relationships."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from ipaddress import ip_address
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import urlsplit

from Crypto.Hash import keccak
from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

from canonical import canonicalize
from safe_fetch import SAFE_FETCH_POLICY_JSON, FetchPolicyError, canonicalize_https_url

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
SCHEMAS_DIR = REPO_ROOT / "schemas"
VOCAB_PATH = SCHEMAS_DIR / "controlled-vocabularies.json"
VOCAB_SCHEMA_PATH = SCHEMAS_DIR / "controlled-vocabularies.schema.json"
ENVELOPE_PATH = SCHEMAS_DIR / "record-envelope.schema.json"
OFFCHAIN_ENVELOPE_SCHEMA = "https://6529networkmuseum.org/schemas/record-envelope-v1.json"


class DuplicateJsonKeyError(ValueError):
    """Raised when a JSON object repeats a key before validation or hashing."""

    def __init__(self, key: str) -> None:
        super().__init__(f"duplicate JSON object key: {key!r}")
        self.key = key


def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateJsonKeyError(key)
        result[key] = value
    return result

RECORD_REFERENCE_KEYS = {
    "references",
    "supersedes",
    "approval_decision_id",
    "program_id",
    "object_id",
    "object_ids",
    "accession_lot_id",
    "governing_references",
    "selected_outcome_ids",
    "amendment_ids",
}
ACCESSION_EVENT_ORDER = ("receipt", "acceptance", "acquisition", "title_passage", "custody_receipt", "accession")
SENSITIVE_KEY_PARTS = {
    "api_key",
    "apikey",
    "access_token",
    "auth_token",
    "credential",
    "donor_email",
    "donor_phone",
    "hardware_wallet",
    "internal_minutes",
    "mnemonic",
    "password",
    "private_key",
    "private_storage_location",
    "seed_phrase",
    "secret",
    "signer_secret",
    "tax_id",
}
SECRET_VALUE_PATTERNS = [
    re.compile(r"-----BEGIN [^-]+ PRIVATE KEY-----"),
    re.compile(r"^eyJ[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+$"),
    re.compile(r"\bBearer\s+[A-Za-z0-9._-]+", re.IGNORECASE),
    re.compile(r"\b(?:gho_|github_pat_|sk-|AKIA)[A-Za-z0-9_-]+"),
    re.compile(r"^(?:file://|\\\\|[A-Za-z]:\\|/Users/|/home/|/root/|C:/Users/)", re.IGNORECASE),
]
ENDPOINT_POLICY = dict(SAFE_FETCH_POLICY_JSON)
SUSPICIOUS_HOSTS = {"localhost", "localhost.localdomain", "metadata", "nip.io", "sslip.io", "xip.io", "localtest.me", "lvh.me"}
SUSPICIOUS_HOST_SUFFIXES = (".localhost", ".local", ".internal", ".lan", ".nip.io", ".sslip.io", ".xip.io", ".localtest.me", ".lvh.me")
NUMERIC_HOST = re.compile(r"^(?:0[xX][0-9a-fA-F]+|[0-9]+)(?:\.(?:0[xX][0-9a-fA-F]+|[0-9]+))*$")
CANONICAL_IPV4 = re.compile(r"^(?:0|[1-9][0-9]{0,2})(?:\.(?:0|[1-9][0-9]{0,2})){3}$")


def keccak256(data: bytes) -> bytes:
    digest = keccak.new(digest_bits=256)
    digest.update(data)
    return digest.digest()


def hex_bytes(data: bytes) -> str:
    return "0x" + data.hex()


def parse_time(value: str, label: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(f"{label} is not an ISO-8601 timestamp: {value}") from exc
    if parsed.tzinfo is None:
        raise ValueError(f"{label} must include a timezone: {value}")
    return parsed.astimezone(timezone.utc)


def unix_seconds(value: str, label: str) -> int:
    return int(parse_time(value, label).timestamp())


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle, object_pairs_hook=reject_duplicate_keys)


def load_schemas(root: Path = REPO_ROOT) -> tuple[dict[str, Any], dict[str, Any], dict[str, dict[str, Any]]]:
    schemas_dir = root / "schemas"
    vocabularies = load_json(schemas_dir / "controlled-vocabularies.json")
    envelope = load_json(schemas_dir / "record-envelope.schema.json")
    by_id: dict[str, dict[str, Any]] = {}
    for path in sorted(schemas_dir.glob("*.schema.json")):
        schema = load_json(path)
        schema_id = schema.get("$id")
        if schema_id:
            by_id[schema_id] = schema
    return vocabularies, envelope, by_id


def validator_for(schema: dict[str, Any], store: dict[str, dict[str, Any]]) -> Draft202012Validator:
    registry = Registry().with_resources((uri, Resource.from_contents(document)) for uri, document in store.items())
    return Draft202012Validator(schema, registry=registry, format_checker=FormatChecker())


def schema_leaf_errors(error: Any) -> Iterable[Any]:
    if error.context:
        for child in error.context:
            yield from schema_leaf_errors(child)
    else:
        yield error


def top_level_payload_keys(type_schema: dict[str, Any], store: dict[str, dict[str, Any]]) -> set[str]:
    common = store["https://6529networkmuseum.org/schemas/common-v1.json"]["$defs"]["commonPayload"]

    def properties_in(schema: dict[str, Any]) -> set[str]:
        keys = set(schema.get("properties", {}))
        for keyword in ("allOf", "anyOf", "oneOf"):
            for part in schema.get(keyword, []):
                if isinstance(part, dict):
                    keys.update(properties_in(part))
        return keys

    return set(common.get("properties", {})) | properties_in(type_schema)


def format_error(error: Any) -> str:
    path = "".join(f"[{part!r}]" if isinstance(part, int) else f".{part}" for part in error.absolute_path)
    return f"{path or '$'}: {error.message}"


def validate_vocabularies(vocabularies: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    if vocabularies.get("endpoint_policy") != ENDPOINT_POLICY:
        issues.append("vocabularies.endpoint_policy must require global-at-fetch resolution, IP pinning, redirect rechecks, and unknown-host rejection")
    record_types = vocabularies.get("record_types", [])
    schema_ids = vocabularies.get("schema_ids", {})
    schema_paths = vocabularies.get("schema_paths", {})
    if (
        not isinstance(record_types, list)
        or not all(isinstance(record_type, str) for record_type in record_types)
        or not isinstance(schema_ids, dict)
        or not isinstance(schema_paths, dict)
    ):
        return ["vocabularies: record_types must be an array and schema_ids/schema_paths must be objects"]
    if set(record_types) != set(schema_ids) or set(record_types) != set(schema_paths):
        issues.append("vocabularies: record_types, schema_ids, and schema_paths must cover exactly the same types")
    for name, value in schema_ids.items():
        if not isinstance(value, str) or not re.fullmatch(r"0x[0-9a-f]{64}", value):
            issues.append(f"vocabularies.schema_ids.{name}: must be a lowercase bytes32 hex value")
    transitions = vocabularies.get("workflow_transitions")
    workflow_states = vocabularies.get("workflow_states")
    if not isinstance(transitions, dict) or not isinstance(workflow_states, list) or not all(
        isinstance(state, str) for state in workflow_states
    ):
        return issues + ["vocabularies: workflow_states must be a string array and workflow_transitions must be an object"]
    if any(not isinstance(successors, list) or not all(isinstance(successor, str) for successor in successors) for successors in transitions.values()):
        issues.append("vocabularies.workflow_transitions: every state must map to a string array")
        return issues
    states = set(workflow_states)
    if set(transitions) != states:
        issues.append("vocabularies.workflow_transitions must define every workflow state")
    for state, successors in transitions.items():
        if any(successor not in states for successor in successors):
            issues.append(f"vocabularies.workflow_transitions.{state}: unknown successor")
    return issues


def validate_subject_id(record_type: str, subject_id: str, envelope_subject_id: str, prefix: str) -> str | None:
    material = f"{prefix}.{record_type.lower()}.v1:{subject_id}".encode("utf-8")
    expected = hex_bytes(keccak256(material))
    if envelope_subject_id.lower() != expected:
        return f"envelope.subjectId: expected domain-separated subject {expected}, got {envelope_subject_id}"
    return None


def inspect_sensitive(value: Any, path: str = "$") -> Iterable[str]:
    if isinstance(value, dict):
        for key, child in value.items():
            normalized = re.sub(r"[^a-z0-9]+", "_", key.lower()).strip("_")
            if any(part in normalized for part in SENSITIVE_KEY_PARTS):
                yield f"{path}.{key}: sensitive field is not allowed in public records"
            yield from inspect_sensitive(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from inspect_sensitive(child, f"{path}[{index}]")
    elif isinstance(value, str):
        if any(pattern.search(value) for pattern in SECRET_VALUE_PATTERNS):
            yield f"{path}: secret, credential, or private filesystem value is not allowed in public records"
        if is_private_network_url(value):
            yield f"{path}: local/private network URL is not allowed in public records"


def is_private_network_url(value: str) -> bool:
    try:
        parsed = urlsplit(value)
    except ValueError:
        return True
    if parsed.scheme.lower() not in {"http", "https"}:
        return False
    if parsed.scheme.lower() == "https":
        try:
            canonicalize_https_url(value)
        except FetchPolicyError:
            return True
        return False
    host = parsed.hostname
    if not host or parsed.username is not None or parsed.password is not None:
        return True
    if any(ord(char) > 127 for char in host) or any(char in host for char in ("%", "\\", "*")):
        return True
    host = host.rstrip(".").lower()
    if host in SUSPICIOUS_HOSTS or "." not in host or host.endswith(SUSPICIOUS_HOST_SUFFIXES):
        return True
    if NUMERIC_HOST.fullmatch(host):
        if not CANONICAL_IPV4.fullmatch(host):
            return True
        octets = [int(part) for part in host.split(".")]
        if any(octet > 255 for octet in octets):
            return True
    try:
        address = ip_address(host.split("%", 1)[0])
    except ValueError:
        return False
    return not address.is_global


def iter_reference_values(value: Any, key: str | None = None) -> Iterable[str]:
    if isinstance(value, dict):
        for child_key, child in value.items():
            if child_key in RECORD_REFERENCE_KEYS:
                yield from iter_reference_values(child, child_key)
            elif isinstance(child, (dict, list)):
                yield from iter_reference_values(child, child_key)
    elif isinstance(value, list):
        for child in value:
            yield from iter_reference_values(child, key)
    elif isinstance(value, str) and key in RECORD_REFERENCE_KEYS:
        yield value


def validate_state_machine(payload: dict[str, Any], vocabularies: dict[str, Any]) -> list[str]:
    if payload.get("record_type") != "WORK_DESCRIPTION":
        return []
    issues: list[str] = []
    history = payload.get("state_history", [])
    if not isinstance(history, list) or not all(isinstance(entry, dict) for entry in history):
        return ["state_history: must be an array of objects"]
    states = [entry.get("state") for entry in history]
    if not all(isinstance(state, str) for state in states):
        return ["state_history: every entry must have a string state"]
    transitions = vocabularies.get("workflow_transitions")
    if not isinstance(transitions, dict):
        return ["vocabularies.workflow_transitions: must be an object before workflow validation"]
    if states and states[0] != "offered":
        issues.append("state_history: the complete history must begin at offered")
    if len(states) != len(set(states)):
        issues.append("state_history: a workflow state may occur only once")
    for index, (current, following) in enumerate(zip(states, states[1:])):
        if following not in transitions.get(current, []):
            issues.append(f"state_history[{index}]: invalid transition {current} -> {following}")
    for index, entry in enumerate(history[1:], start=1):
        try:
            current_time = parse_time(entry["observed_at"], f"state_history[{index}].observed_at")
            previous_time = parse_time(history[index - 1]["observed_at"], f"state_history[{index - 1}].observed_at")
            if current_time < previous_time:
                issues.append(f"state_history[{index}]: observed_at moves backwards")
        except (KeyError, ValueError) as exc:
            issues.append(str(exc))
    if payload.get("current_state") != (states[-1] if states else None):
        issues.append("current_state: must equal the last state_history.state")
    state_set = set(states)
    chain = payload.get("chain_identity", {})
    title_binding = payload.get("title_binding", {})
    rights = payload.get("rights", {})
    condition = payload.get("condition", {})
    chain = chain if isinstance(chain, dict) else {}
    title_binding = title_binding if isinstance(title_binding, dict) else {}
    rights = rights if isinstance(rights, dict) else {}
    condition = condition if isinstance(condition, dict) else {}
    acquisition_transaction = chain.get("acquisition_transaction")
    transfer_transaction = title_binding.get("transfer_transaction")
    if isinstance(acquisition_transaction, str) and isinstance(transfer_transaction, str):
        if transfer_transaction.lower() != acquisition_transaction.lower():
            issues.append("title_binding.transfer_transaction must match chain_identity.acquisition_transaction")
    custody_account = chain.get("custody_account")
    title_binding_to = title_binding.get("to")
    if isinstance(custody_account, str) and isinstance(title_binding_to, str):
        custody_match = re.fullmatch(r"eip155:([0-9]+):(0x[0-9a-fA-F]{40})", custody_account)
        if custody_match:
            if isinstance(chain.get("chain_id"), int) and custody_match.group(1) != str(chain["chain_id"]):
                issues.append("chain_identity.custody_account chain must match chain_identity.chain_id")
            if title_binding_to.lower() != custody_match.group(2).lower():
                issues.append("title_binding.to must match chain_identity.custody_account")
    caip19 = chain.get("caip19")
    if isinstance(caip19, str):
        caip_match = re.fullmatch(r"eip155:([0-9]+)/((?:erc721|erc1155)):0x([0-9a-fA-F]{40})/([0-9]+)", caip19)
        if not caip_match:
            issues.append("chain_identity.caip19 must encode an eip155 ERC token identity")
        else:
            if isinstance(chain.get("chain_id"), int) and caip_match.group(1) != str(chain["chain_id"]):
                issues.append("chain_identity.caip19 chain must match chain_identity.chain_id")
            if isinstance(chain.get("contract"), str) and caip_match.group(3).lower() != chain["contract"].lower().removeprefix("0x"):
                issues.append("chain_identity.caip19 contract must match chain_identity.contract")
            if isinstance(chain.get("token_id"), str) and caip_match.group(4) != chain["token_id"]:
                issues.append("chain_identity.caip19 token must match chain_identity.token_id")
            expected_resource = {"ERC-721": "erc721", "ERC-1155": "erc1155"}.get(chain.get("token_standard"))
            if expected_resource and caip_match.group(2) != expected_resource:
                issues.append("chain_identity.caip19 resource type must match chain_identity.token_standard")
    if "received_onchain" in state_set and chain.get("custody_status") != "verified":
        issues.append("completion gate: received_onchain requires verified custody")
    if "accessioned" in state_set:
        if title_binding.get("status") != "executed":
            issues.append("completion gate: accessioned requires an executed TITLE_BINDING")
        if chain.get("custody_status") != "verified":
            issues.append("completion gate: accessioned requires verified custody")
        if any(grant.get("grant_status") in {None, "unspecified"} for grant in rights.values()):
            issues.append("completion gate: accessioned requires an explicit status for every rights use class")
        if any(value == "not_assessed" for value in condition.values() if isinstance(value, str)):
            issues.append("completion gate: accessioned requires condition assessment")
    if "preservation_complete" in state_set and payload.get("preservation", {}).get("status") != "complete":
        issues.append("completion gate: preservation_complete requires preservation.status=complete")
    if "display_ready" in state_set and payload.get("display", {}).get("status") not in {"ready", "ready_with_conditions"}:
        issues.append("completion gate: display_ready requires a ready display status")
    return issues


def validate_event_history(payload: dict[str, Any]) -> list[str]:
    record_type = payload.get("record_type")
    if record_type not in {"ACCESSION", "RIGHTS_STATEMENT", "CONDITION_REPORT"}:
        return []
    issues: list[str] = []
    events = payload.get("events")
    if not isinstance(events, list) or not all(isinstance(event, dict) for event in events):
        return [f"{record_type}.events: must be an array of event objects"]
    event_types = [event.get("event_type") for event in events]
    if record_type == "ACCESSION":
        if tuple(event_types) != ACCESSION_EVENT_ORDER:
            issues.append("ACCESSION.events must contain receipt, acceptance, acquisition, title_passage, custody_receipt, and accession exactly once in order")
    elif record_type == "RIGHTS_STATEMENT" and event_types and event_types[0] != "rights_assertion":
        issues.append("RIGHTS_STATEMENT.events must begin with rights_assertion")
    elif record_type == "CONDITION_REPORT" and event_types and event_types[0] != "condition_assessment":
        issues.append("CONDITION_REPORT.events must begin with condition_assessment")
    if record_type == "ACCESSION" and all(isinstance(event_type, str) for event_type in event_types) and len(event_types) != len(set(event_types)):
        issues.append("ACCESSION.events must not repeat an event_type")
    previous_time = None
    for index, event in enumerate(events):
        try:
            current_time = parse_time(event["occurred_at"], f"{record_type}.events[{index}].occurred_at")
        except (KeyError, ValueError) as exc:
            issues.append(str(exc))
            continue
        if previous_time is not None:
            invalid_order = current_time <= previous_time if record_type == "ACCESSION" else current_time < previous_time
            if invalid_order:
                issues.append(f"{record_type}.events[{index}]: occurred_at must be strictly increasing" if record_type == "ACCESSION" else f"{record_type}.events[{index}]: occurred_at moves backwards")
        previous_time = current_time
    if record_type == "ACCESSION" and len(events) == len(ACCESSION_EVENT_ORDER):
        acceptance = events[1]
        if acceptance.get("occurred_at") != payload.get("acceptance_date"):
            issues.append("ACCESSION acceptance_date must equal the acceptance event occurred_at")
        title_event = events[3]
        custody_event = events[4]
        instrument = title_event.get("instrument") if isinstance(title_event.get("instrument"), dict) else {}
        custody_path = custody_event.get("custody_path") if isinstance(custody_event.get("custody_path"), dict) else {}
        object_ids = payload.get("object_ids")
        bindings = payload.get("title_bindings")
        if isinstance(object_ids, list) and isinstance(bindings, list):
            binding_ids = [binding.get("object_id") for binding in bindings if isinstance(binding, dict)]
            if not all(isinstance(object_id, str) for object_id in object_ids + binding_ids):
                issues.append("ACCESSION title_bindings must identify every object_id")
            elif len(binding_ids) != len(set(binding_ids)) or set(binding_ids) != set(object_ids):
                issues.append("ACCESSION must contain exactly one title binding per object_id")
            if any(not isinstance(binding, dict) or binding.get("status") != "executed" for binding in bindings):
                issues.append("ACCESSION must require an executed title binding for every object_id")
            for binding in bindings:
                if isinstance(binding, dict) and instrument.get("sha256") and binding.get("instrument_sha256") != instrument.get("sha256"):
                    issues.append("ACCESSION title_passage instrument sha256 must match every title binding")
                if isinstance(binding, dict) and instrument.get("custodian_reference") and binding.get("custodian_reference") != instrument.get("custodian_reference"):
                    issues.append("ACCESSION title_passage custodian_reference must match every title binding")
        if instrument.get("kind") != "off_chain_instrument":
            issues.append("ACCESSION title_passage must identify an off_chain_instrument")
        if custody_path.get("kind") != "non_token_off_chain":
            issues.append("ACCESSION custody_receipt must identify a non_token_off_chain custody path")
        if instrument.get("reference") and custody_path.get("instrument_reference") != instrument.get("reference"):
            issues.append("ACCESSION custody_receipt instrument_reference must match title_passage instrument.reference")
        executed_bindings = [binding for binding in bindings if isinstance(binding, dict) and binding.get("status") == "executed"] if isinstance(bindings, list) else []
        path_object_id = custody_path.get("object_id")
        matching_bindings = [binding for binding in executed_bindings if binding.get("object_id") == path_object_id]
        if len(matching_bindings) != 1:
            issues.append("ACCESSION custody_path must identify exactly one executed title binding by object_id")
        else:
            binding = matching_bindings[0]
            for field in ("from", "to", "custodian_reference"):
                if custody_path.get(field) != binding.get(field):
                    issues.append(f"ACCESSION custody_path.{field} must match the executed title binding")
    return issues


def validate_semantics(record: dict[str, Any], vocabularies: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    envelope = record["envelope"]
    payload = record["payload"]
    record_type = payload.get("record_type")
    envelope_uri = envelope.get("uri")
    if isinstance(envelope_uri, str) and is_private_network_url(envelope_uri):
        issues.append("envelope.uri: local/private network URL is not allowed in public records")
    if not isinstance(record_type, str) or record_type not in vocabularies.get("schema_ids", {}):
        return [f"payload.record_type is unknown: {record_type!r}"]
    if envelope.get("recordType") != record_type:
        issues.append("envelope.recordType must equal payload.record_type")
    expected_schema = vocabularies["schema_ids"].get(record_type)
    if expected_schema and envelope.get("schemaId", "").lower() != expected_schema:
        issues.append(f"envelope.schemaId must equal the pinned schema ID for {record_type}")
    if expected_schema and payload.get("schema_id", "").lower() != expected_schema:
        issues.append(f"payload.schema_id must equal the pinned schema ID for {record_type}")
    subject_issue = validate_subject_id(record_type, payload.get("subject_id", ""), envelope.get("subjectId", ""), vocabularies["subject_domain_prefix"])
    if subject_issue:
        issues.append(subject_issue)
    content_hash = envelope.get("contentHash")
    if not isinstance(content_hash, dict):
        issues.append("envelope.contentHash must be an object")
        content_hash = {}
    try:
        expected_hash = hex_bytes(keccak256(canonicalize(payload)))
        actual_hash = content_hash.get("digest", "").lower()
        if content_hash.get("algorithm") != vocabularies["hash_algorithms"]["HASH_KECCAK256"]:
            issues.append("envelope.contentHash.algorithm must be HASH_KECCAK256 (1)")
        if actual_hash != expected_hash:
            issues.append(f"envelope.contentHash.digest does not match canonical payload; expected {expected_hash}")
    except (TypeError, ValueError) as exc:
        issues.append(f"payload canonicalization: {exc}")
    for hash_name in ("contentHash", "signatureHash"):
        hash_ref = envelope.get(hash_name, {})
        if not isinstance(hash_ref, dict):
            issues.append(f"envelope.{hash_name} must be an object")
            hash_ref = {}
        if hash_ref.get("canonicalizationId", "").lower() != vocabularies["canonicalization"]["id"]:
            issues.append(f"envelope.{hash_name}.canonicalizationId must be RFC8785_JCS")
        if len(hash_ref.get("digest", "")) != 66:
            issues.append(f"envelope.{hash_name}.digest must contain exactly 32 bytes")
    try:
        if unix_seconds(payload["effective_at"], "payload.effective_at") != envelope["effectiveAt"]:
            issues.append("envelope.effectiveAt must equal payload.effective_at in Unix seconds")
    except (KeyError, ValueError) as exc:
        issues.append(str(exc))
    constructor_data = payload.get("constructor", {})
    reviewer_data = payload.get("reviewer", {})
    source_data = payload.get("source", {})
    constructor = constructor_data.get("id") if isinstance(constructor_data, dict) else None
    reviewer = reviewer_data.get("id") if isinstance(reviewer_data, dict) else None
    if constructor == reviewer:
        issues.append("constructor/reviewer separation: constructor.id and reviewer.id must differ")
    try:
        if parse_time(reviewer_data["reviewed_at"], "reviewer.reviewed_at") < parse_time(payload["created_at"], "created_at"):
            issues.append("reviewer.reviewed_at must not precede created_at")
    except (KeyError, ValueError) as exc:
        issues.append(str(exc))
    issues.extend(inspect_sensitive(payload))
    if record_type == "GOVERNANCE_DECISION":
        source_status = source_data.get("status") if isinstance(source_data, dict) else None
        decision_status = payload.get("decision_status")
        if source_status == "WINNER" and decision_status != "adopted":
            issues.append("governance evidence: WINNER must be recorded as adopted")
        if source_status == "PARTICIPATORY" and decision_status == "adopted":
            issues.append("governance evidence: PARTICIPATORY cannot be recorded as adopted")
    issues.extend(validate_state_machine(payload, vocabularies))
    issues.extend(validate_event_history(payload))
    return issues


def validate_records(root: Path) -> list[str]:
    issues: list[str] = []
    schema_root = root if (root / "schemas").is_dir() else REPO_ROOT
    bootstrap_script = root / "scripts" / "bootstrap_validate.py"
    if bootstrap_script.is_file():
        bootstrap = subprocess.run(
            [sys.executable, str(bootstrap_script)],
            cwd=root,
            capture_output=True,
            text=True,
            check=False,
        )
        if bootstrap.returncode:
            detail = (bootstrap.stdout + bootstrap.stderr).strip()
            issues.append(f"bootstrap validation failed: {detail}")
    try:
        vocabularies, envelope_schema, schema_store = load_schemas(schema_root)
    except (OSError, json.JSONDecodeError, DuplicateJsonKeyError) as exc:
        return [f"schema and vocabulary load failed: {exc}"]
    issues.extend(validate_vocabularies(vocabularies))
    try:
        vocabulary_schema = load_json(schema_root / "schemas/controlled-vocabularies.schema.json")
        vocabulary_errors = sorted(
            (leaf for error in validator_for(vocabulary_schema, schema_store).iter_errors(vocabularies) for leaf in schema_leaf_errors(error)),
            key=lambda error: list(error.absolute_path),
        )
        issues.extend(f"schemas/controlled-vocabularies.json: {format_error(error)}" for error in vocabulary_errors)
    except OSError as exc:
        issues.append(f"schemas/controlled-vocabularies.schema.json: unavailable: {exc}")
    schemas_dir = schema_root / "schemas"
    for schema_path in [schemas_dir / "record-envelope.schema.json", *sorted(schemas_dir.glob("*.schema.json"))]:
        try:
            schema = load_json(schema_path)
            Draft202012Validator.check_schema(schema)
        except Exception as exc:  # schema compilation errors are repository errors
            issues.append(f"{schema_path.relative_to(root)}: invalid JSON Schema: {exc}")
    records_dir = root / "records"
    record_paths = sorted(records_dir.rglob("*.json")) if records_dir.exists() else []
    records: list[tuple[Path, dict[str, Any], dict[str, Any] | None]] = []
    record_ids: dict[str, Path] = {}
    for path in record_paths:
        relative = path.relative_to(root).as_posix()
        try:
            record = load_json(path)
        except (OSError, json.JSONDecodeError, DuplicateJsonKeyError) as exc:
            issues.append(f"{relative}: cannot parse JSON: {exc}")
            continue
        if not isinstance(record, dict):
            issues.append(f"{relative}: record must be an object")
            continue
        is_envelope = record.get("$schema") == OFFCHAIN_ENVELOPE_SCHEMA
        payload = record.get("payload") if is_envelope else None
        if is_envelope:
            envelope_errors = sorted(
                (leaf for error in validator_for(envelope_schema, schema_store).iter_errors(record) for leaf in schema_leaf_errors(error)),
                key=lambda error: list(error.absolute_path),
            )
            issues.extend(f"{relative}: envelope {format_error(error)}" for error in envelope_errors)
            if not isinstance(payload, dict):
                records.append((path, record, None))
                continue
        else:
            record_type = record.get("record_type")
            schema_path_name = vocabularies.get("schema_paths", {}).get(record_type)
            declared_schema = record.get("$schema")
            declared_path = (path.parent / declared_schema).resolve() if isinstance(declared_schema, str) else None
            if declared_path is None or not declared_path.is_relative_to(schemas_dir) or not declared_path.is_file():
                issues.append(f"{relative}: declared local schema is missing or escapes schemas/")
                records.append((path, record, None))
                continue
            if isinstance(schema_path_name, str) and declared_path != (schema_root / "schemas" / schema_path_name).resolve():
                issues.append(f"{relative}: $schema must route to schemas/{schema_path_name}")
            try:
                type_schema = load_json(declared_path)
                type_errors = sorted(
                    (leaf for error in validator_for(type_schema, schema_store).iter_errors(record) for leaf in schema_leaf_errors(error)),
                    key=lambda error: list(error.absolute_path),
                )
                issues.extend(f"{relative}: record {format_error(error)}" for error in type_errors)
            except (OSError, json.JSONDecodeError, DuplicateJsonKeyError) as exc:
                issues.append(f"{relative}: declared schema unavailable: {exc}")
            record_id = record.get("record_id")
            if isinstance(record_id, str):
                if record_id in record_ids:
                    issues.append(f"{relative}: duplicate record_id {record_id}; first seen at {record_ids[record_id].relative_to(root).as_posix()}")
                else:
                    record_ids[record_id] = path
            records.append((path, record, None))
            continue

        record_id = payload.get("record_id")
        if isinstance(record_id, str):
            if record_id in record_ids:
                issues.append(f"{relative}: duplicate record_id {record_id}; first seen at {record_ids[record_id].relative_to(root).as_posix()}")
            else:
                record_ids[record_id] = path
        record_type = payload.get("record_type")
        type_errors: list[Any] = []
        schema_path_name = vocabularies.get("schema_paths", {}).get(record_type)
        if not schema_path_name:
            issues.append(f"{relative}: unknown payload.record_type {record_type!r}")
            continue
        type_path = schema_root / "schemas" / schema_path_name
        try:
            type_schema = load_json(type_path)
            type_errors = sorted(
                (leaf for error in validator_for(type_schema, schema_store).iter_errors(payload) for leaf in schema_leaf_errors(error)),
                key=lambda error: list(error.absolute_path),
            )
            issues.extend(f"{relative}: payload {format_error(error)}" for error in type_errors)
            allowed_keys = top_level_payload_keys(type_schema, schema_store)
            for extra_key in sorted(set(payload) - allowed_keys):
                issues.append(f"{relative}: payload.{extra_key}: unknown field; schemas are closed at the top level")
        except OSError as exc:
            issues.append(f"{relative}: schema {schema_path_name} unavailable: {exc}")
        # Semantic checks deliberately run even when a schema error exists so a failed
        # record gets the complete diagnostic set in one deterministic CI run.
        if isinstance(record.get("envelope"), dict):
            issues.extend(f"{relative}: {message}" for message in validate_semantics(record, vocabularies))
        records.append((path, record, payload))
    for path, record, payload in records:
        if not isinstance(payload, dict):
            continue
        relative = path.relative_to(root).as_posix()
        for reference in iter_reference_values(payload):
            if reference not in record_ids:
                issues.append(f"{relative}: unresolved record reference {reference}")
        supersedes = payload.get("supersedes")
        if supersedes:
            if supersedes == payload.get("record_id"):
                issues.append(f"{relative}: supersedes must not point to itself")
            else:
                superseded_path = record_ids.get(supersedes)
                if superseded_path:
                    superseded = load_json(superseded_path)
                    if superseded.get("payload", {}).get("record_type") != payload.get("record_type"):
                        issues.append(f"{relative}: supersedes must point to the same record_type")
    return issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=REPO_ROOT, help="repository root (default: current script's repository)")
    args = parser.parse_args(argv)
    root = args.root.resolve()
    issues = validate_records(root)
    if issues:
        print("Museum validation failed:")
        print("\n".join(f"- {issue}" for issue in issues))
        return 1
    print("Museum validation passed: schemas, records, references, states, guardrails, and commitments are valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
