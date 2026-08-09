#!/usr/bin/env python3
"""Validate Museum records, their Stream envelope commitments, and relationships."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import unicodedata
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
MEDIA_DESCRIPTION_AMENDMENT_ID = "6529NM-MEDIA-DESC-AMD-2026-08-08-001"
TYPED_REFERENCE_REGISTRY_ID = "PUBLIC_TYPED_REFERENCE_REGISTRY_V1"
TYPED_REFERENCE_TARGET_TYPE_MATRIX = {
    ("component", "authoritative_record"): {"WORK_DESCRIPTION", "PROGRAM_OUTCOME"},
    ("manifestation", "authoritative_record"): {"VISUAL_OBSERVATION"},
    ("manifestation", "governed_typed_registry"): {"ERC721_TOKEN_MANIFESTATION"},
}
METADATA_ONLY_MEDIA_AFFORDANCES = {"alt_text", "open_wave_proposal_context", "copy_citation"}
MEDIA_RENDER_OR_DELIVERY_AFFORDANCES = {
    "view", "thumbnail", "hero", "play", "interact_sandboxed", "zoom", "fullscreen", "download",
    "open_token_source", "open_repository_path",
}


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
    "decision_id",
    "program_id",
    "object_id",
    "object_ids",
    "accession_lot_id",
    "governing_references",
    "selected_outcome_ids",
    "amendment_ids",
    "entity_id",
    "entity_ids",
    "relation_id",
    "observation_id",
    "amendment_id",
    "historical_source_observation_id",
    "subject_media_entity_id",
    "subject_work_entity_id",
    "source_entity_id",
    "target_entity_id",
    "source_record_ids",
    "source_work_record_ids",
    "authority_record_ids",
    "program_entity_ids",
    "acquisition_entity_ids",
    "accession_entity_ids",
    "collection_entity_id",
    "institution_entity_id",
    "admitted_work_entity_ids",
    "work_entity_ids",
    "creator_entity_ids",
    "agent_entity_ids",
    "author_entity_ids",
    "subject_entity_ids",
    "produced_acquisition_entity_ids",
    "selected_outcome_record_ids",
    "media_entity_ids",
    "publication_record_id",
    "source_accession_record_id",
    "derived_from_media_entity_id",
    "accession_object_id",
}
ACCESSION_EVENT_ORDER = ("receipt", "acceptance", "acquisition", "title_passage", "custody_receipt", "accession")
PUBLIC_ENTITY_TYPE = "PUBLIC_ENTITY"
PUBLIC_RELATION_TYPE = "PUBLIC_RELATION"
RELEASE_REVIEW_BOUND_RECORD_TYPES = {
    PUBLIC_ENTITY_TYPE,
    PUBLIC_RELATION_TYPE,
    "WAVE_STATUS_OBSERVATION",
    "WAVE_PUBLICATION_OBSERVATION",
    "MEDIA_DESCRIPTION_AMENDMENT",
}
PUBLIC_ENTITY_SCHEMA_ID = "0xd8aef6592fe156c4c3c10e59de540f5cdf8b130eedca322e0e22b30764bee1a9"
PUBLIC_RELATION_SCHEMA_ID = "0xaa76f1b93e01ae7a1cff2717b0c814df772fd26d3997a47847a1887cba6756de"
PUBLIC_IDENTITY_INVENTORY_FILENAME = "public-entity-identity-inventory.json"
PUBLIC_CANONICAL_PAGE_TYPES = {
    "INSTITUTION",
    "COLLECTION",
    "ARTIST",
    "ORGANIZATION",
    "WORK",
    "PROJECT_OR_SERIES",
    "CURATED_ACQUISITION",
    "ACQUISITION_PROGRAM",
    "RESEARCH_PUBLICATION",
}
PUBLIC_RELATIONAL_ONLY_TYPES = {"AGENT", "ACCESSION", "MEDIA_REFERENCE"}
PUBLIC_IDENTITY_BINDING_ENTITY_TYPES = (
    "INSTITUTION",
    "COLLECTION",
    "AGENT",
    "ARTIST",
    "ORGANIZATION",
    "WORK",
    "PROJECT_OR_SERIES",
    "CURATED_ACQUISITION",
    "ACQUISITION_PROGRAM",
    "ACCESSION",
    "RESEARCH_PUBLICATION",
    "MEDIA_REFERENCE",
)
PUBLIC_IDENTITY_BINDING_AUXILIARY_TYPES = ("WORK_LIFECYCLE_OBSERVATION",)
PUBLIC_IDENTITY_BINDING_TYPES = (
    *PUBLIC_IDENTITY_BINDING_ENTITY_TYPES,
    *PUBLIC_IDENTITY_BINDING_AUXILIARY_TYPES,
)


def load_public_identity_inventory(schema_root: Path) -> dict[str, Any]:
    inventory_path = schema_root / "schemas" / PUBLIC_IDENTITY_INVENTORY_FILENAME
    if not inventory_path.is_file():
        return {}
    return load_json(inventory_path)


def public_entity_id_pattern(entity_type: Any, identity_inventory: dict[str, Any] | None = None) -> str | None:
    patterns = identity_inventory.get("entity_id_patterns", {}) if isinstance(identity_inventory, dict) else {}
    pattern = patterns.get(entity_type)
    if isinstance(pattern, str):
        return pattern
    if entity_type == "CURATED_ACQUISITION":
        return r"^6529NM-CA-\d{4}-\d{3}$"
    if entity_type == "WORK":
        return r"^6529NM-W-\d{4}$"
    return None


def frozen_projection(value: Any) -> str:
    """Return a stable, hashable representation of JSON-derived untrusted data."""
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), default=str)


def _route_slug(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii").casefold()
    normalized = re.sub(r"[^a-z0-9]+", "-", normalized).strip("-")
    if not normalized:
        raise ValueError(f"cannot derive a governed route slug from {value!r}")
    return normalized


def _route_source_rows(root: Path, identity_inventory: dict[str, Any], expansion: dict[str, Any]) -> list[dict[str, Any]]:
    source_name = expansion.get("source_inventory")
    if source_name in {"work_aliases", "acquisition_aliases", "source_aliases", "route_aliases"}:
        rows = identity_inventory.get(source_name, [])
        return [row for row in rows if isinstance(row, dict)]
    if source_name == "approved_collections":
        value = load_json(root / "records/collections/approved-collections.json")
        return [
            {"alias": _route_slug(row["preferred_name"]), "canonical_route": "/museum/network/acquisition-programs/gift-acquisitions#" + _route_slug(row["preferred_name"]), "canonical_entity_id": None}
            for row in value.get("collections", [])
            if isinstance(row, dict) and isinstance(row.get("preferred_name"), str)
        ]
    if source_name == "institutional_practice":
        base = root / "records/institutional-practice"
        return [{"alias": path.relative_to(base).with_suffix("").as_posix(), "canonical_entity_id": None} for path in sorted(base.rglob("*")) if path.is_file()]
    if source_name == "data_architecture":
        rows = [{"alias": "overview", "canonical_entity_id": None}]
        base = root / "docs/data-architecture"
        rows.extend({"alias": path.relative_to(base).with_suffix("").as_posix(), "canonical_entity_id": None} for path in sorted(base.rglob("*")) if path.is_file())
        return rows
    if source_name == "rights":
        base = root / "docs/rights"
        return [{"alias": path.relative_to(base).with_suffix("").as_posix(), "canonical_entity_id": None} for path in sorted(base.rglob("*")) if path.is_file()]
    if source_name == "governance":
        value = load_json(root / "records/governance/decisions.json")
        return [{"alias": row.get("decision_id"), "canonical_entity_id": None} for row in value.get("records", []) if isinstance(row, dict) and isinstance(row.get("decision_id"), str)]
    return []


def _expected_route_expansion_keys(root: Path, identity_inventory: dict[str, Any], public_entities: dict[str, dict[str, Any]], route_inventory: dict[str, Any]) -> set[tuple[str, str, str | None]]:
    """Expand the closed compatibility contract without a catch-all redirect."""

    expected: set[tuple[str, str, str | None]] = set()
    for expansion in route_inventory.get("expansions", []):
        if not isinstance(expansion, dict):
            continue
        source_name = expansion.get("source_inventory")
        alias_kind = expansion.get("alias_kind")
        for row in _route_source_rows(root, identity_inventory, expansion):
            alias = row.get("alias")
            if not isinstance(alias, str):
                continue
            if source_name in {"work_aliases", "acquisition_aliases"} and alias_kind != "all" and row.get("alias_kind") != alias_kind:
                continue
            if source_name == "source_aliases" and alias_kind != "all" and row.get("alias_type") != alias_kind:
                continue
            target_id = row.get("canonical_entity_id") if expansion.get("canonical_route_from_entity") else None
            target = public_entities.get(target_id) if isinstance(target_id, str) else None
            if expansion.get("canonical_route_from_entity"):
                if target is None:
                    continue
                if expansion.get("only_permanent_collection") and target.get("profile", {}).get("collection_membership", {}).get("status") != "permanent_collection":
                    continue
                canonical = target.get("canonical_route")
            else:
                canonical = row.get("canonical_route")
                transform = expansion.get("path_transform")
                if transform == "institutional_practice_to_research":
                    canonical = "/museum/network/research/institutional-practice/" + alias
                elif transform == "data_architecture_to_research":
                    canonical = "/museum/network/research/data-architecture" if alias == "overview" else "/museum/network/research/data-architecture/" + alias
                elif transform == "rights_to_research":
                    canonical = "/museum/network/research/rights-and-licenses/" + alias
                elif transform == "governance_to_about":
                    canonical = "/museum/network/about/governance/" + alias
                elif transform == "approved_collection_to_gift_program":
                    canonical = "/museum/network/acquisition-programs/gift-acquisitions#" + alias
            if not isinstance(canonical, str):
                continue
            for template in expansion.get("legacy_templates", []):
                if not isinstance(template, str):
                    continue
                expected.add((template.replace("{alias}", alias), canonical, target_id))
    return expected


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
    public_relation_types = vocabularies.get("public_relation_types", [])
    relation_profiles = vocabularies.get("relation_profiles", {})
    if not isinstance(public_relation_types, list) or not isinstance(relation_profiles, dict):
        issues.append("vocabularies: public_relation_types and relation_profiles must be present")
    else:
        if set(public_relation_types) != set(relation_profiles):
            issues.append("vocabularies: public_relation_types and relation_profiles must cover exactly the same relation types")
        for relation_type, profile in relation_profiles.items():
            if not isinstance(profile, dict):
                issues.append(f"vocabularies.relation_profiles.{relation_type}: must be an object")
                continue
            allowed = profile.get("allowed_qualifier_fields", [])
            required = profile.get("required_qualifier_fields", [])
            if not isinstance(allowed, list) or not isinstance(required, list) or not set(required).issubset(set(allowed)):
                issues.append(f"vocabularies.relation_profiles.{relation_type}: required qualifiers must be an allowed subset")
            for bound in ("max_targets_per_source", "max_sources_per_target"):
                value = profile.get(bound)
                if value is not None and (not isinstance(value, int) or value < 1):
                    issues.append(f"vocabularies.relation_profiles.{relation_type}.{bound}: must be a positive integer or null")
    expected_public_schema_ids = {
        PUBLIC_ENTITY_TYPE: hex_bytes(keccak256(b"PUBLIC_ENTITY_V1")),
        PUBLIC_RELATION_TYPE: hex_bytes(keccak256(b"PUBLIC_RELATION_V1")),
    }
    for record_type, expected in expected_public_schema_ids.items():
        if vocabularies.get("schema_ids", {}).get(record_type) != expected:
            issues.append(f"vocabularies.schema_ids.{record_type}: must commit the exact {record_type}_V1 literal")
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
    prior_event_ids: set[str] = set()
    for index, event in enumerate(events):
        if record_type in {"RIGHTS_STATEMENT", "CONDITION_REPORT"}:
            current_event_id = event.get("event_id")
            if not isinstance(current_event_id, str) or not current_event_id:
                issues.append(f"{record_type}.events[{index}]: event_id is required")
            elif current_event_id in prior_event_ids:
                issues.append(f"{record_type}.events[{index}]: event_id must be unique")
            supersedes_event_id = event.get("supersedes_event_id")
            if supersedes_event_id is not None and (
                not isinstance(supersedes_event_id, str) or supersedes_event_id not in prior_event_ids
            ):
                issues.append(f"{record_type}.events[{index}]: supersedes_event_id must identify a unique earlier event")
            if isinstance(current_event_id, str) and current_event_id:
                prior_event_ids.add(current_event_id)
        try:
            current_time = parse_time(event["occurred_at"], f"{record_type}.events[{index}].occurred_at")
        except (KeyError, ValueError) as exc:
            issues.append(str(exc))
            continue
        if previous_time is not None:
            invalid_order = current_time < previous_time
            if invalid_order:
                issues.append(f"{record_type}.events[{index}]: occurred_at moves backwards")
        previous_time = current_time
    if record_type == "ACCESSION" and len(events) == len(ACCESSION_EVENT_ORDER):
        acceptance = events[1]
        if acceptance.get("occurred_at") != payload.get("acceptance_date"):
            issues.append("ACCESSION acceptance_date must equal the acceptance event occurred_at")
        title_event = events[3]
        custody_event = events[4]
        instrument = title_event.get("instrument") if isinstance(title_event.get("instrument"), dict) else {}
        custody_paths = custody_event.get("custody_paths")
        custody_paths = custody_paths if isinstance(custody_paths, list) and all(isinstance(path, dict) for path in custody_paths) else []
        object_ids = payload.get("object_ids")
        bindings = payload.get("title_bindings")
        if isinstance(object_ids, list) and isinstance(bindings, list):
            binding_ids = [binding.get("object_id") for binding in bindings if isinstance(binding, dict)]
            if not all(isinstance(object_id, str) for object_id in object_ids + binding_ids):
                issues.append("ACCESSION title_bindings must identify every object_id")
            elif (
                len(binding_ids) != len(set(map(frozen_projection, binding_ids)))
                or set(map(frozen_projection, binding_ids)) != set(map(frozen_projection, object_ids))
            ):
                issues.append("ACCESSION must contain exactly one title binding per object_id")
            if any(not isinstance(binding, dict) or binding.get("status") != "executed" for binding in bindings):
                issues.append("ACCESSION must require an executed title binding for every object_id")
            for binding in bindings:
                if isinstance(binding, dict) and instrument.get("sha256") and binding.get("instrument_sha256") != instrument.get("sha256"):
                    issues.append("ACCESSION title_passage instrument sha256 must match every title binding")
                if isinstance(binding, dict) and instrument.get("custodian_reference") and binding.get("custodian_reference") != instrument.get("custodian_reference"):
                    issues.append("ACCESSION title_passage custodian_reference must match every title binding")
        if instrument.get("kind") not in {"off_chain_instrument", "institutional_gift_title_declaration"}:
            issues.append("ACCESSION title_passage must identify a supported title instrument")
        executed_bindings = [binding for binding in bindings if isinstance(binding, dict) and binding.get("status") == "executed"] if isinstance(bindings, list) else []
        path_ids = [path.get("object_id") for path in custody_paths]
        object_ids = payload.get("object_ids") if isinstance(payload.get("object_ids"), list) else []
        if (
            not custody_paths
            or len(path_ids) != len(set(map(frozen_projection, path_ids)))
            or set(map(frozen_projection, path_ids)) != set(map(frozen_projection, object_ids))
        ):
            issues.append("ACCESSION custody_paths must identify exactly one path per object_id")
        for custody_path in custody_paths:
            matching_bindings = [binding for binding in executed_bindings if binding.get("object_id") == custody_path.get("object_id")]
            if len(matching_bindings) != 1:
                issues.append("ACCESSION custody_path must identify exactly one executed title binding by object_id")
                continue
            binding = matching_bindings[0]
            expected_kind = "onchain_token" if binding.get("transfer_transaction") else "non_token_off_chain"
            if custody_path.get("kind") != expected_kind:
                issues.append(f"ACCESSION custody_path.kind must be {expected_kind} for its title binding")
            if expected_kind == "non_token_off_chain" and instrument.get("reference") and custody_path.get("instrument_reference") != instrument.get("reference"):
                issues.append("ACCESSION off-chain custody_path.instrument_reference must match title_passage instrument.reference")
            for field in ("from", "to", "custodian_reference"):
                if custody_path.get(field) != binding.get(field):
                    issues.append(f"ACCESSION custody_path.{field} must match the executed title binding")
    return issues


def validate_gift_acceptance_authorization(payload: dict[str, Any]) -> list[str]:
    """Enforce cross-item GAA invariants that JSON Schema cannot project."""
    if payload.get("record_type") != "GIFT_ACCEPTANCE_AUTHORIZATION":
        return []
    issues: list[str] = []
    assets = payload.get("assets")
    receipt = payload.get("custody_receipt")
    if not isinstance(assets, list) or not all(isinstance(asset, dict) for asset in assets):
        return ["GIFT_ACCEPTANCE_AUTHORIZATION.assets must be an array of objects"]
    receipt = receipt if isinstance(receipt, dict) else {}
    projections: tuple[tuple[str, Any], ...] = (
        ("object_id", lambda asset: asset.get("object_id")),
        ("caip19", lambda asset: asset.get("caip19", "").lower() if isinstance(asset.get("caip19"), str) else None),
        (
            "contract+token_id",
            lambda asset: (
                asset.get("contract", "").lower() if isinstance(asset.get("contract"), str) else None,
                asset.get("token_id"),
            ),
        ),
        ("custody_receipt_log", lambda asset: asset.get("custody_receipt_log")),
    )
    for label, projection in projections:
        values = [projection(asset) for asset in assets]
        frozen = [json.dumps(value, sort_keys=True, separators=(",", ":"), default=str) for value in values]
        if len(frozen) != len(set(frozen)):
            issues.append(f"GIFT_ACCEPTANCE_AUTHORIZATION.assets contains duplicate {label}")
    if receipt.get("transfer_count") != len(assets):
        issues.append("GIFT_ACCEPTANCE_AUTHORIZATION.custody_receipt.transfer_count must equal assets.length")
    return issues


def validate_visual_observation(payload: dict[str, Any]) -> list[str]:
    """Enforce generic source/capture relationships for visual observations."""
    if payload.get("record_type") != "VISUAL_OBSERVATION":
        return []
    issues: list[str] = []
    objects = payload.get("objects")
    if not isinstance(objects, list) or not all(isinstance(item, dict) for item in objects):
        return ["VISUAL_OBSERVATION.objects must be an array of objects"]
    object_ids = [item.get("object_id") for item in objects]
    caip19s = [item.get("caip19", "").lower() if isinstance(item.get("caip19"), str) else None for item in objects]
    if len(object_ids) != len(set(map(frozen_projection, object_ids))):
        issues.append("VISUAL_OBSERVATION.objects contains duplicate object_id")
    if len(caip19s) != len(set(caip19s)):
        issues.append("VISUAL_OBSERVATION.objects contains duplicate caip19")
    capture_scope = payload.get("capture_scope")
    capture_scope = capture_scope if isinstance(capture_scope, dict) else {}
    if capture_scope.get("static_capture_order") != object_ids:
        issues.append("VISUAL_OBSERVATION.capture_scope.static_capture_order must equal objects order")
    for index, item in enumerate(objects):
        prefix = f"VISUAL_OBSERVATION.objects[{index}]"
        raw = item.get("raw_metadata_source")
        static = item.get("static_capture")
        live = item.get("live_capture")
        raw = raw if isinstance(raw, dict) else {}
        static = static if isinstance(static, dict) else {}
        live = live if isinstance(live, dict) else {}
        if static.get("source_url") != raw.get("image_url"):
            issues.append(f"{prefix}.static_capture.source_url must equal raw_metadata_source.image_url")
        if live.get("source_url") != raw.get("generator_url"):
            issues.append(f"{prefix}.live_capture.source_url must equal raw_metadata_source.generator_url")
        frames = live.get("frames")
        if not isinstance(frames, list) or len(frames) != 2 or not all(isinstance(frame, dict) for frame in frames):
            issues.append(f"{prefix}.live_capture.frames must contain exactly two frame objects")
        else:
            if [frame.get("frame_index") for frame in frames] != [1, 2]:
                issues.append(f"{prefix}.live_capture.frames must be ordered 1, 2")
            captured_times = [frame.get("captured_at") for frame in frames]
            if all(isinstance(value, str) for value in captured_times):
                try:
                    first = parse_time(captured_times[0], f"{prefix}.live_capture.frames[0].captured_at")
                    second = parse_time(captured_times[1], f"{prefix}.live_capture.frames[1].captured_at")
                    minimum_wait = live.get("minimum_wait_between_frames_ms")
                    if not isinstance(minimum_wait, int) or int((second - first).total_seconds() * 1000) < minimum_wait:
                        issues.append(f"{prefix}.live_capture frame timestamps must span at least minimum_wait_between_frames_ms")
                except ValueError as exc:
                    issues.append(str(exc))
            elif captured_times != [None, None]:
                issues.append(f"{prefix}.live_capture frame timestamps must be both known or both null")
            hashes_differ = frames[0].get("screenshot_sha256") != frames[1].get("screenshot_sha256")
            if live.get("changed") != hashes_differ:
                issues.append(f"{prefix}.live_capture.changed must equal screenshot hash inequality")
        for capture_name, capture in (("static_capture", static), ("live_capture", live)):
            retention = capture.get("retention")
            if not isinstance(retention, dict):
                continue
            retained = retention.get("bytes_retained_in_public_repository")
            status = retention.get("status")
            if retained is True and status != "retained":
                issues.append(f"{prefix}.{capture_name}.retention status must be retained when bytes are retained")
            if retained is False and status == "retained":
                issues.append(f"{prefix}.{capture_name}.retention status cannot be retained when bytes are absent")
    return issues


def validate_provenance_schedule(schedule: dict[str, Any]) -> list[str]:
    """Enforce generic receipt-to-object joins that JSON Schema cannot project."""
    issues: list[str] = []
    common = schedule.get("common_receipt")
    objects = schedule.get("objects")
    if not isinstance(common, dict) or not isinstance(objects, list) or not all(isinstance(item, dict) for item in objects):
        return ["transaction provenance common_receipt and objects must be present"]
    object_ids = [item.get("object_id") for item in objects]
    chain_objects = [item.get("chain_object", "").lower() if isinstance(item.get("chain_object"), str) else None for item in objects]
    if len(object_ids) != len(set(map(frozen_projection, object_ids))):
        issues.append("transaction provenance objects contains duplicate object_id")
    if len(chain_objects) != len(set(chain_objects)):
        issues.append("transaction provenance objects contains duplicate chain_object")
    if common.get("transfer_count") != len(objects):
        issues.append("transaction provenance common_receipt.transfer_count must equal objects.length")
    log_indices = common.get("log_indices")
    if not isinstance(log_indices, dict) or set(map(frozen_projection, log_indices)) != set(map(frozen_projection, object_ids)):
        issues.append("transaction provenance common_receipt.log_indices must identify every object exactly once")
        log_indices = {}
    receipt_logs: list[Any] = []
    for item in objects:
        object_id = item.get("object_id")
        events = item.get("events")
        events = events if isinstance(events, list) else []
        museum_receipts = [event for event in events if isinstance(event, dict) and event.get("kind") == "museum_receipt"]
        if len(museum_receipts) != 1:
            issues.append(f"transaction provenance {object_id} must contain exactly one museum_receipt event")
            continue
        event = museum_receipts[0]
        receipt_logs.append(event.get("log"))
        expected = {
            "block": common.get("block_number"),
            "block_hash": common.get("block_hash"),
            "direct_rpc_verified": True,
            "from": common.get("transaction_from"),
            "kind": "museum_receipt",
            "log": log_indices.get(object_id) if isinstance(object_id, str) else None,
            "receipt_status": common.get("receipt_status"),
            "time": common.get("block_time"),
            "to": common.get("museum_custody_address"),
            "tx": common.get("transaction_hash"),
            "verification": "direct_rpc_verified",
        }
        if event != expected:
            issues.append(f"transaction provenance {object_id} museum_receipt must equal common_receipt projection")
    if len(receipt_logs) != len(set(map(frozen_projection, receipt_logs))):
        issues.append("transaction provenance museum_receipt log indices must be unique")
    return issues


def has_key_recursive(value: Any, wanted: str) -> bool:
    if isinstance(value, dict):
        return wanted in value or any(has_key_recursive(child, wanted) for child in value.values())
    if isinstance(value, list):
        return any(has_key_recursive(child, wanted) for child in value)
    return False


def validate_public_fixity(fixity: Any, label: str) -> list[str]:
    issues: list[str] = []
    if not isinstance(fixity, dict):
        return [f"{label}: fixity must be an object"]
    status = fixity.get("status")
    algorithm = fixity.get("algorithm")
    digest = fixity.get("digest")
    if status == "verified":
        if algorithm == "sha256" and not (isinstance(digest, str) and re.fullmatch(r"sha256:[0-9a-f]{64}", digest)):
            issues.append(f"{label}: sha256 fixity requires a sha256:<64 lowercase hex> digest")
        if algorithm == "keccak256" and not (isinstance(digest, str) and re.fullmatch(r"0x[0-9a-f]{64}", digest)):
            issues.append(f"{label}: keccak256 fixity requires a 0x<64 lowercase hex> digest")
        if algorithm not in {"sha256", "keccak256"}:
            issues.append(f"{label}: verified fixity requires a supported algorithm")
    elif status == "unverified_not_retrieved":
        if algorithm is not None or digest is not None or fixity.get("verified_at") is not None:
            issues.append(f"{label}: unverified_not_retrieved fixity must not contain invented algorithm, digest, or verified_at")
    else:
        issues.append(f"{label}: unknown fixity status {status!r}")
    return issues


def validate_public_media(media: Any, label: str) -> list[str]:
    issues: list[str] = []
    if not isinstance(media, dict):
        return [f"{label}: media reference must be an object"]
    if has_key_recursive(media, "image_url"):
        issues.append(f"{label}: generic image_url is prohibited; use the closed media locator and role")
    locator = media.get("source_locator")
    has_source_locator = isinstance(locator, dict) and (locator.get("uri") is not None or locator.get("repository_path") is not None)
    rights = media.get("rights") if isinstance(media.get("rights"), dict) else {}
    rights_status = rights.get("status")
    affordances = media.get("allowed_ui_affordances", [])
    if rights_status in {"restricted", "unknown"}:
        if media.get("visual") is not False:
            issues.append(f"{label}: {rights_status} media must be metadata-only with visual false")
        if not isinstance(locator, dict) or locator.get("uri") is not None or locator.get("repository_path") is not None:
            issues.append(f"{label}: {rights_status} media must have a null source_locator (uri and repository_path)")
        if media.get("token_source_locator") is not None:
            issues.append(f"{label}: {rights_status} media must have a null token_source_locator")
        if isinstance(affordances, list) and not set(affordances).issubset(METADATA_ONLY_MEDIA_AFFORDANCES):
            issues.append(f"{label}: {rights_status} media may expose metadata-only affordances only")
    if not has_source_locator and rights_status not in {"restricted", "unknown"}:
        issues.append(f"{label}: source_locator must contain a URI or repository_path")
    visual = media.get("visual")
    if visual is True:
        if not isinstance(media.get("width"), int) or not isinstance(media.get("height"), int):
            issues.append(f"{label}: visual media requires positive width and height")
        if not (isinstance(media.get("accessibility_text"), str) and media.get("accessibility_text")):
            if media.get("accessibility_status") != "publication_join" or not isinstance(media.get("accessibility_publication_entity_id"), str):
                issues.append(f"{label}: visual media requires accessibility text or a typed publication join")
    source_observation = media.get("source_observation")
    source_status = source_observation.get("status") if isinstance(source_observation, dict) else None
    accessibility_evidence_refs = media.get("accessibility_evidence_refs")
    if not isinstance(accessibility_evidence_refs, list) or not accessibility_evidence_refs:
        issues.append(f"{label}: accessibility_evidence_refs must be a non-empty typed evidence list")
    else:
        for evidence_ref in accessibility_evidence_refs:
            if not isinstance(evidence_ref, dict) or evidence_ref.get("evidence_class") not in {"A", "B", "C", "D", "E"}:
                issues.append(f"{label}: accessibility evidence must carry an explicit evidence class")
    fixity = media.get("fixity")
    issues.extend(validate_public_fixity(fixity, f"{label}.fixity"))
    fixity_status = fixity.get("status") if isinstance(fixity, dict) else None
    if source_status == "retrieved" and fixity_status != "verified":
        issues.append(f"{label}: retrieved media requires verified fixity")
    if source_status in {"not_retrieved", "source_declared"} and fixity_status != "unverified_not_retrieved":
        issues.append(f"{label}: non-retrieved or source-declared media must use unverified_not_retrieved fixity")
    if source_status == "mutable_external" and fixity_status not in {"verified", "unverified_not_retrieved"}:
        issues.append(f"{label}: mutable external media may bind exact observed bytes or remain explicitly unverified")
    if source_status == "mutable_external" and fixity_status == "verified":
        basis = fixity.get("basis") if isinstance(fixity, dict) else None
        if not isinstance(basis, str) or "mutable" not in basis.casefold() or "not retained" not in basis.casefold():
            issues.append(f"{label}: mutable external verified fixity must state both locator mutability and that bytes are not retained")
    role = media.get("media_role")
    publication_boundary = media.get("publication_boundary")
    expected_boundary = {
        "museum_retained_preservation_object": "preservation_record",
        "museum_generated_public_derivative": "public_derivative",
        "museum_authored_public_graphic": "public_graphic",
        "token_linked_source_media": "token_source",
        "historical_wave_proposal_presentation": "historical_wave_proposal_context",
    }.get(role)
    if expected_boundary is None:
        issues.append(f"{label}: media_role must use the closed Museum media vocabulary")
    elif publication_boundary != expected_boundary:
        issues.append(f"{label}: publication_boundary must be {expected_boundary!r} for {role}")
    accessibility_subject_policy = media.get("accessibility_subject_policy")
    if accessibility_subject_policy == "non_identifying_apparently_young_subject":
        text = media.get("accessibility_text")
        if not isinstance(text, str) or not text:
            issues.append(f"{label}: an apparently young subject requires non-identifying accessibility text")
        elif re.search(r"\b(named|identified|known as|identified as)\b", text, flags=re.IGNORECASE):
            issues.append(f"{label}: accessibility text for an apparently young subject must not identify the subject")
        elif re.search(r"\b(child|children|minor|juvenile|adolescent|teen(?:ager)?|boy|girl|infant)\b", text, flags=re.IGNORECASE):
            issues.append(f"{label}: accessibility text for an apparently young subject must not assign an age classification")
        prohibition = media.get("identity_inference_prohibition")
        if not isinstance(prohibition, dict) or prohibition.get("status") != "prohibited" or prohibition.get("scope") != "subject_identity_and_age_classification" or not isinstance(prohibition.get("reason"), str) or not prohibition["reason"]:
            issues.append(f"{label}: an apparently young subject requires structural identity-and-age inference prohibition")
    elif media.get("identity_inference_prohibition") is not None:
        prohibition = media.get("identity_inference_prohibition")
        if not isinstance(prohibition, dict) or prohibition.get("status") != "prohibited" or prohibition.get("scope") not in {"subject_identity", "subject_identity_and_age_classification"}:
            issues.append(f"{label}: identity_inference_prohibition must be null or a closed prohibited identity-scope object")
    if role == "museum_retained_preservation_object" and (source_status != "retrieved" or fixity_status != "verified"):
        issues.append(f"{label}: retained preservation objects require retrieved bytes and verified fixity")
    if role == "museum_generated_public_derivative" and not isinstance(media.get("transform_profile"), str):
        issues.append(f"{label}: Museum-generated derivatives require a transform profile")
    if role == "museum_authored_public_graphic":
        if publication_boundary != "public_graphic":
            issues.append(f"{label}: Museum-authored public graphics require the public_graphic boundary")
        if media.get("derived_from_media_entity_id") is not None:
            issues.append(f"{label}: Museum-authored public graphics cannot claim derivation from another media object")
        if not isinstance(media.get("transform_profile"), str) or "independently authored" not in media.get("transform_profile", ""):
            issues.append(f"{label}: Museum-authored public graphics require an independent authorship transform statement")
        if "hero" in affordances:
            issues.append(f"{label}: historical Museum-authored public graphics cannot be published as an acquisition hero")
    if role == "museum_generated_public_derivative" and set(media.get("publication_context_entity_ids", [])) == {"6529NM-CA-2026-003"}:
        if media.get("derived_from_media_entity_id") is not None:
            issues.append(f"{label}: the historical CA-003 proposal graphic cannot claim derivation from a source photograph")
        if "hero" in affordances:
            issues.append(f"{label}: the historical CA-003 proposal graphic cannot be published as the selected-acquisition hero")
    subject_entity_id = media.get("subject_entity_id")
    if isinstance(subject_entity_id, str):
        for evidence_field in ("rights", "source_observation"):
            evidence_section = media.get(evidence_field)
            evidence_refs = evidence_section.get("evidence_refs", []) if isinstance(evidence_section, dict) else []
            for evidence_ref in evidence_refs if isinstance(evidence_refs, list) else []:
                uri = evidence_ref.get("uri") if isinstance(evidence_ref, dict) else None
                if isinstance(uri, str) and re.search(rf"(?<![A-Za-z0-9]){re.escape(subject_entity_id)}(?![A-Za-z0-9])", uri):
                    issues.append(f"{label}: {evidence_field} evidence cannot cite the subject MEDIA_REFERENCE entity itself")
        rights_refs = media.get("rights", {}).get("evidence_refs", []) if isinstance(media.get("rights"), dict) else []
        source_refs = media.get("source_observation", {}).get("evidence_refs", []) if isinstance(media.get("source_observation"), dict) else []
        def contains_amendment(refs: Any) -> bool:
            return any(
                isinstance(ref, dict)
                and isinstance(ref.get("uri"), str)
                and (MEDIA_DESCRIPTION_AMENDMENT_ID in ref["uri"] or "media-description-amendment-2026-08-08.json" in ref["uri"])
                for ref in refs if isinstance(refs, list)
            )
        if contains_amendment(rights_refs):
            issues.append(f"{label}: the class-C media description amendment cannot be rights evidence")
        if contains_amendment(source_refs) and subject_entity_id != "6529NM-MED-0042":
            issues.append(f"{label}: the media description amendment is restricted to the Bar-Am accessibility/source-description boundary")
        if subject_entity_id == "6529NM-MED-0042":
            if not contains_amendment(accessibility_evidence_refs):
                issues.append(f"{label}: Bar-Am media must bind the append-only description amendment as accessibility evidence")
            if contains_amendment(source_refs):
                issues.append(f"{label}: Bar-Am media description amendment belongs in accessibility evidence, not source_observation evidence")
    if role == "historical_wave_proposal_presentation":
        if publication_boundary != "historical_wave_proposal_context":
            issues.append(f"{label}: historical Wave media is proposal-context-only")
        if not isinstance(media.get("wave_proposal_context"), dict):
            issues.append(f"{label}: historical Wave media requires wave_proposal_context evidence")
        if "open_wave_proposal_context" not in affordances:
            issues.append(f"{label}: historical Wave media must expose only the exact proposal context through open_wave_proposal_context")
        if set(media.get("publication_context_entity_ids", [])) != {"6529NM-CA-2026-003"}:
            issues.append(f"{label}: historical Wave media must be explicitly bound to CA-003 publication context")
        if not set(affordances).issubset({"view", "thumbnail", "hero", "alt_text", "open_wave_proposal_context", "copy_citation"}):
            issues.append(f"{label}: historical Wave media affordances must remain within the proposal presentation allowlist")
        if any(item in affordances for item in {"download", "zoom", "fullscreen", "play"}):
            issues.append(f"{label}: historical Wave proposal media cannot expose download, zoom, fullscreen, or play by default")
        if any(item in affordances for item in {"open_token_source", "open_repository_path"}):
            issues.append(f"{label}: historical Wave media cannot expose token or repository source affordances")
    if rights_status in {"restricted", "unknown"} and any(item in affordances for item in MEDIA_RENDER_OR_DELIVERY_AFFORDANCES):
        issues.append(f"{label}: {rights_status} media cannot expose visual delivery, download, zoom, fullscreen, token, or repository source opening")
    if "download" in affordances and rights_status not in {"cleared", "cleared_with_conditions"}:
        issues.append(f"{label}: download requires cleared or cleared_with_conditions rights")
    if "interact_sandboxed" in affordances and (
        media.get("media_type") != "text/html"
        or visual is not True
        or rights_status not in {"cleared", "cleared_with_conditions"}
        or source_status != "mutable_external"
    ):
        issues.append(f"{label}: interact_sandboxed requires visual mutable-external text/html with cleared rights")
    if any(item in affordances for item in {"zoom", "fullscreen"}) and (visual is not True or rights_status not in {"cleared", "cleared_with_conditions"}):
        issues.append(f"{label}: zoom/fullscreen requires visual media with cleared rights")
    return issues


WAVE_PUBLICATION_EXPECTED_PARTS = {
    1: {
        "source_path": "records/proposed-gifts/6529NM-PG-2026-001/public/wave-storm/01-resolution.md",
        "content_sha256": "sha256:e735f85395398e97077dad532d14b69fef650f60b05dddd931bd26dfab490a3e",
        "media_url": "https://d3lqz0a4bldqgf.cloudfront.net/drops/author_7ee51a67-07b7-4c91-87ed-464c56446c43/f8006332-4f8a-4556-b0df-3c43eec16334/conflict-at-its-edges-cover.png",
        "mime_type": "image/png",
        "candidate_object_id": None,
        "token_source_uri": None,
    },
    2: {
        "source_path": "records/proposed-gifts/6529NM-PG-2026-001/public/wave-storm/02-david-seymour-127.md",
        "content_sha256": "sha256:c57190e0f57313153bd2f2817370e3ff259e12ca37b3a10b1e4bc7eca1b0513c",
        "media_url": "https://d3lqz0a4bldqgf.cloudfront.net/drops/author_7ee51a67-07b7-4c91-87ed-464c56446c43/d498d837-3331-4650-a30e-27ca18d53521/magnum-75-127.jpg",
        "mime_type": "image/jpeg",
        "candidate_object_id": "6529NM-PG-2026-001.OBJ-001",
        "token_source_uri": "https://arweave.net/VE0zO2N1zVTsbEUHdUFazEgvuMbmVOi6OfaWfQOWkaM",
    },
    3: {
        "source_path": "records/proposed-gifts/6529NM-PG-2026-001/public/wave-storm/03-larry-towell-145.md",
        "content_sha256": "sha256:e6440e460470e7a47bd9e2a184398bf0b95ab36db130b3cfc84716ed6aa66f31",
        "media_url": "https://d3lqz0a4bldqgf.cloudfront.net/drops/author_7ee51a67-07b7-4c91-87ed-464c56446c43/3e2fbdea-cf3c-4949-b3d2-f081cb12de00/magnum-75-145.jpg",
        "mime_type": "image/jpeg",
        "candidate_object_id": "6529NM-PG-2026-001.OBJ-002",
        "token_source_uri": "https://arweave.net/r0bUW6Mtxq897pgig0V01Ad43S_Ldwv3tARjwmjrqpE",
    },
    4: {
        "source_path": "records/proposed-gifts/6529NM-PG-2026-001/public/wave-storm/04-micha-bar-am-97.md",
        "content_sha256": "sha256:edb682412450b6fb22e1ac72853c2930944d3dcfa0fb22fc78ed4026cb8dc094",
        "media_url": "https://d3lqz0a4bldqgf.cloudfront.net/drops/author_7ee51a67-07b7-4c91-87ed-464c56446c43/2146f5f7-9352-47e6-bf60-cba46e52c07f/magnum-75-97.jpg",
        "mime_type": "image/jpeg",
        "candidate_object_id": "6529NM-PG-2026-001.OBJ-003",
        "token_source_uri": "https://arweave.net/vRmOcFJRTK84ILXp2Tkjz5KoS4iXXbMqki7rxhTYlr4",
    },
    5: {
        "source_path": "records/proposed-gifts/6529NM-PG-2026-001/public/wave-storm/05-moises-saman-44.md",
        "content_sha256": "sha256:0d47741f7399e86ff1abf184b6000c978b0b90051abc962863b3f572f4eef886",
        "media_url": "https://d3lqz0a4bldqgf.cloudfront.net/drops/author_7ee51a67-07b7-4c91-87ed-464c56446c43/5d6d9bf0-7ff3-4afd-ac69-c6b34079fbf9/magnum-75-44.jpg",
        "mime_type": "image/jpeg",
        "candidate_object_id": "6529NM-PG-2026-001.OBJ-004",
        "token_source_uri": "https://arweave.net/zLifpzu3AQWqjg59nuy9jeRqHPA5o5-LpwwBqNRcD5o",
    },
    6: {
        "source_path": "records/proposed-gifts/6529NM-PG-2026-001/public/wave-storm/06-lorenzo-meloni-104.md",
        "content_sha256": "sha256:1a069afa6164389e8482e2d72bd7a49f30d0df355e1a6f5f2c07983705bfa22f",
        "media_url": "https://d3lqz0a4bldqgf.cloudfront.net/drops/author_7ee51a67-07b7-4c91-87ed-464c56446c43/4526b19e-76df-493b-86ac-105782c061ea/magnum-75-104.jpg",
        "mime_type": "image/jpeg",
        "candidate_object_id": "6529NM-PG-2026-001.OBJ-005",
        "token_source_uri": "https://arweave.net/oz0t0DJj2BgFCux1WXskxisxvzV2KA0ukqaVbQ1Ckco",
    },
    7: {
        "source_path": "records/proposed-gifts/6529NM-PG-2026-001/public/wave-storm/07-case-and-decision.md",
        "content_sha256": "sha256:97672880e617004bd7094495b0bf759f5d16bb71f0316c5696c5e9d96e3b38d7",
        "media_url": None,
        "mime_type": None,
        "candidate_object_id": None,
        "token_source_uri": None,
    },
}


def validate_wave_publication_observation(payload: dict[str, Any], repository_root: Path = REPO_ROOT) -> list[str]:
    """Validate the frozen, public-safe readback against retained source bytes."""

    issues: list[str] = []
    expected_scalars = {
        "record_id": "6529NM-WAVE-PUB-OBS-2026-08-08-001",
        "observation_id": "6529NM-WAVE-PUB-OBS-2026-08-08-001",
        "proposal_id": "6529NM-PG-2026-001",
        "api_endpoint": "https://api.6529.io/api/drops/002bfa4f-8416-48bf-b35e-38f354e9a9f0",
        "is_signed": True,
        "wave_id": "5f207393-5418-4a75-8738-e40edb44a94d",
        "drop_id": "002bfa4f-8416-48bf-b35e-38f354e9a9f0",
        "serial_no": 1276093,
        "drop_type": "WINNER",
        "title": "Conflict at Its Edges",
        "drop_created_at": "2026-08-06T13:19:28.882Z",
        "parts_count": 7,
        "selection_context_entity_id": "6529NM-CA-2026-003",
        "source_package_path": "records/proposed-gifts/6529NM-PG-2026-001/wave-storm.json",
        "proposal_path": "records/proposed-gifts/6529NM-PG-2026-001/proposal.json",
    }
    for key, expected in expected_scalars.items():
        if payload.get(key) != expected:
            issues.append(f"WAVE_PUBLICATION_OBSERVATION.{key} does not match the retained signed-drop API readback")
    author = payload.get("author") if isinstance(payload.get("author"), dict) else {}
    expected_author = {
        "id": "7ee51a67-07b7-4c91-87ed-464c56446c43",
        "handle": "punk6529bot",
        "primary_address": "0xf58fe66af1a8c792cd64d8d706eddabadfcb2fd0",
    }
    if author != expected_author:
        issues.append("WAVE_PUBLICATION_OBSERVATION.author does not match the retained public-safe API author projection")
    parts = payload.get("parts") if isinstance(payload.get("parts"), list) else []
    if [part.get("part_id") for part in parts if isinstance(part, dict)] != list(WAVE_PUBLICATION_EXPECTED_PARTS):
        issues.append("WAVE_PUBLICATION_OBSERVATION.parts must contain exactly ordered parts 1 through 7")
    seen_candidates: set[str] = set()
    package_path = repository_root / "records/proposed-gifts/6529NM-PG-2026-001/wave-storm.json"
    proposal_path = repository_root / "records/proposed-gifts/6529NM-PG-2026-001/proposal.json"
    try:
        package = load_json(package_path)
        proposal = load_json(proposal_path)
    except (OSError, json.JSONDecodeError) as exc:
        return [f"WAVE_PUBLICATION_OBSERVATION source package is unreadable: {exc}"]
    package_by_part = {item.get("part_number"): item for item in package.get("parts", []) if isinstance(item, dict)}
    proposal_by_candidate = {item.get("candidate_object_id"): item for item in proposal.get("objects", []) if isinstance(item, dict)}
    for part in parts:
        if not isinstance(part, dict):
            issues.append("WAVE_PUBLICATION_OBSERVATION.parts entries must be objects")
            continue
        part_id = part.get("part_id")
        expected = WAVE_PUBLICATION_EXPECTED_PARTS.get(part_id)
        if expected is None:
            issues.append(f"WAVE_PUBLICATION_OBSERVATION has unsupported part_id {part_id!r}")
            continue
        for key, expected_value in expected.items():
            if part.get(key) != expected_value:
                issues.append(f"WAVE_PUBLICATION_OBSERVATION.part {part_id}.{key} does not match the immutable readback")
        source_path = part.get("source_path")
        source_file = repository_root / source_path if isinstance(source_path, str) else None
        if source_file is None or not source_file.is_file():
            issues.append(f"WAVE_PUBLICATION_OBSERVATION.part {part_id}: source_path does not resolve")
        else:
            raw = source_file.read_bytes()
            if b"\r" in raw:
                issues.append(f"WAVE_PUBLICATION_OBSERVATION.part {part_id}: retained source must use LF line endings")
            try:
                raw.decode("utf-8")
            except UnicodeDecodeError:
                issues.append(f"WAVE_PUBLICATION_OBSERVATION.part {part_id}: retained source is not UTF-8")
            actual = "sha256:" + hashlib.sha256(raw).hexdigest()
            if part.get("content_sha256") != actual:
                issues.append(f"WAVE_PUBLICATION_OBSERVATION.part {part_id}: content_sha256 does not match retained bytes")
            if part_id == 4 and b"tear gas" not in raw:
                issues.append("WAVE_PUBLICATION_OBSERVATION.part 4 must preserve the historical 'tear gas' text")
        package_part = package_by_part.get(part_id, {})
        package_media = package_part.get("media", []) if isinstance(package_part, dict) else []
        package_media = package_media[0] if package_media and isinstance(package_media[0], dict) else {}
        if part.get("candidate_object_id") != package_part.get("candidate_object_id"):
            issues.append(f"WAVE_PUBLICATION_OBSERVATION.part {part_id}: candidate binding disagrees with wave-storm package")
        if package_media and (part.get("credit") != package_media.get("credit_line") or part.get("rights_label") != package_media.get("rights_label")):
            issues.append(f"WAVE_PUBLICATION_OBSERVATION.part {part_id}: credit or rights label disagrees with wave-storm package")
        candidate = part.get("candidate_object_id")
        if isinstance(candidate, str):
            if candidate in seen_candidates:
                issues.append(f"WAVE_PUBLICATION_OBSERVATION: duplicate candidate binding {candidate}")
            seen_candidates.add(candidate)
            proposal_object = proposal_by_candidate.get(candidate, {})
            image = proposal_object.get("image", {}) if isinstance(proposal_object, dict) else {}
            if part.get("token_source_uri") != image.get("uri"):
                issues.append(f"WAVE_PUBLICATION_OBSERVATION.part {part_id}: token/source URI disagrees with proposal")
    if seen_candidates != {f"6529NM-PG-2026-001.OBJ-{index:03d}" for index in range(1, 6)}:
        issues.append("WAVE_PUBLICATION_OBSERVATION must bind exactly the five proposal candidates once")
    evidence_refs = payload.get("evidence_refs") if isinstance(payload.get("evidence_refs"), list) else []
    if not any(isinstance(ref, dict) and ref.get("evidence_class") == "B" and ref.get("label") == "Signed-drop API readback (is_signed=true)" for ref in evidence_refs):
        issues.append("WAVE_PUBLICATION_OBSERVATION must identify the API-reported signed state precisely as class B")
    return issues


def validate_media_description_amendment(payload: dict[str, Any], repository_root: Path = REPO_ROOT) -> list[str]:
    issues: list[str] = []
    expected_text = "Black-and-white photograph of a person running through smoke at the Western Wall, with a canister in the air and a metal menorah barrier in the foreground."
    expected_predecessor = "6529NM-WAVE-PUB-OBS-2026-08-08-001"
    expected_prior_payload_sha256 = "sha256:887d527756721cae1bf758a8205d1f5f7e0d1cebee2b3f27aafcab5271132995"
    expected_part_sha256 = "sha256:edb682412450b6fb22e1ac72853c2930944d3dcfa0fb22fc78ed4026cb8dc094"
    if payload.get("record_id") != "6529NM-MEDIA-DESC-AMD-2026-08-08-001" or payload.get("amendment_id") != payload.get("record_id"):
        issues.append("MEDIA_DESCRIPTION_AMENDMENT identity is not stable")
    if payload.get("supersedes") != expected_predecessor:
        issues.append("MEDIA_DESCRIPTION_AMENDMENT must supersede the exact Wave publication observation")
    if not isinstance(payload.get("supersession_reason"), str) or not payload.get("supersession_reason"):
        issues.append("MEDIA_DESCRIPTION_AMENDMENT must state an append-only supersession reason")
    if payload.get("prior_payload_sha256") != expected_prior_payload_sha256:
        issues.append("MEDIA_DESCRIPTION_AMENDMENT prior_payload_sha256 must bind the exact historical Wave observation payload")
    if payload.get("superseded_part_id") != 4 or payload.get("superseded_content_sha256") != expected_part_sha256:
        issues.append("MEDIA_DESCRIPTION_AMENDMENT must bind the exact historical Wave part-4 content hash")
    if payload.get("subject_media_entity_id") != "6529NM-MED-0042" or payload.get("subject_work_entity_id") != "6529NM-W-0026":
        issues.append("MEDIA_DESCRIPTION_AMENDMENT subject binding is incorrect")
    if payload.get("evidence_class") != "C" or payload.get("current_accessibility_text") != expected_text:
        issues.append("MEDIA_DESCRIPTION_AMENDMENT must project only the reviewed visible-facts description")
    if "tear gas" in str(payload.get("current_accessibility_text", "")).casefold():
        issues.append("MEDIA_DESCRIPTION_AMENDMENT current description must not identify the gas type")
    source_path = payload.get("source_path")
    source_file = repository_root / source_path if isinstance(source_path, str) else None
    if source_file is None or not source_file.is_file():
        issues.append("MEDIA_DESCRIPTION_AMENDMENT source_path does not resolve")
    expected = WAVE_PUBLICATION_EXPECTED_PARTS[4]
    if payload.get("source_media_uri") != expected["media_url"] or payload.get("historical_source_observation_id") != expected_predecessor or payload.get("historical_source_part_id") != 4:
        issues.append("MEDIA_DESCRIPTION_AMENDMENT must remain bound to Wave receipt part 4")
    receipt_path = repository_root / "records/proposed-gifts/6529NM-PG-2026-001/wave-publication-observation-2026-08-08.json"
    try:
        receipt = load_json(receipt_path)
        receipt_payload = receipt.get("payload", {}) if isinstance(receipt, dict) else {}
        if receipt_payload.get("record_id") != expected_predecessor or receipt_payload.get("record_type") != "WAVE_PUBLICATION_OBSERVATION":
            issues.append("MEDIA_DESCRIPTION_AMENDMENT predecessor must be the Wave publication observation record")
        if payload.get("prior_payload_sha256") != receipt_payload.get("payload_sha256"):
            issues.append("MEDIA_DESCRIPTION_AMENDMENT prior_payload_sha256 does not match the predecessor payload")
        receipt_parts = receipt_payload.get("parts", []) if isinstance(receipt_payload, dict) else []
        receipt_part = next((part for part in receipt_parts if isinstance(part, dict) and part.get("part_id") == 4), None)
        if not isinstance(receipt_part, dict) or receipt_part.get("content_sha256") != expected_part_sha256:
            issues.append("MEDIA_DESCRIPTION_AMENDMENT predecessor part 4 hash does not match the immutable receipt")
    except (OSError, json.JSONDecodeError, DuplicateJsonKeyError) as exc:
        issues.append(f"MEDIA_DESCRIPTION_AMENDMENT predecessor receipt is unreadable: {exc}")
    evidence_refs = payload.get("evidence_refs") if isinstance(payload.get("evidence_refs"), list) else []
    if not any(isinstance(ref, dict) and ref.get("evidence_class") == "C" and ref.get("uri") == expected["media_url"] for ref in evidence_refs):
        issues.append("MEDIA_DESCRIPTION_AMENDMENT direct visual evidence must cite the exact observed media URI")
    if any(isinstance(ref, dict) and ref.get("evidence_class") == "C" and isinstance(ref.get("uri"), str) and "/public/wave-storm/04-micha-bar-am-97.md" in ref.get("uri", "") for ref in evidence_refs):
        issues.append("MEDIA_DESCRIPTION_AMENDMENT direct visual evidence must not substitute the historical Markdown source path for the image")
    return issues


def validate_public_payload(payload: dict[str, Any], vocabularies: dict[str, Any], identity_inventory: dict[str, Any] | None = None) -> list[str]:
    issues: list[str] = []
    record_type = payload.get("record_type")
    record_status = payload.get("record_status")
    review_status = payload.get("review_status")
    reviewer = payload.get("reviewer")
    if record_status == "reviewed" or review_status == "reviewed":
        if record_status != "reviewed" or review_status != "reviewed" or not isinstance(reviewer, dict) or not reviewer.get("id"):
            issues.append("public record: reviewed publication requires record_status/review_status reviewed and a concrete reviewer")
        elif record_type in RELEASE_REVIEW_BOUND_RECORD_TYPES and (
            not re.fullmatch(r"[0-9a-f]{40}", str(reviewer.get("reviewed_commit", "")))
            or not re.fullmatch(r"sha256:[0-9a-f]{64}", str(reviewer.get("reviewed_manifest_sha256", "")))
            or not re.fullmatch(r"0x[0-9a-f]{64}", str(reviewer.get("reviewed_manifest_keccak", "")))
            or not isinstance(reviewer.get("reviewer_ids"), list)
            or reviewer.get("id") not in reviewer.get("reviewer_ids", [])
            or reviewer.get("outcome") != "approved"
        ):
            issues.append("public record: reviewed publication requires reviewer IDs, approved outcome, and the exact reviewed candidate commit")
    if record_status in {"constructed", "review_pending"} or review_status == "pending_independent_review":
        if payload.get("entity_status") == "published":
            issues.append("public record: entity_status published is prohibited while independent review is pending")
        if record_type == PUBLIC_ENTITY_TYPE and payload.get("entity_status") not in {None, "review_pending"}:
            issues.append("public entity: a review-pending record must use entity_status review_pending")
    if record_type == PUBLIC_ENTITY_TYPE and record_status == "reviewed" and payload.get("entity_status") != "published":
        issues.append("public entity: reviewed publication must use entity_status published")
    if payload.get("entity_status") == "published" and (record_status != "reviewed" or review_status != "reviewed" or not isinstance(reviewer, dict)):
        issues.append("public record: published entity must be independently reviewed")
    if record_type == PUBLIC_ENTITY_TYPE:
        if payload.get("entity_id") != payload.get("record_id"):
            issues.append("public entity: entity_id must equal record_id")
        entity_type = payload.get("entity_type")
        profile = payload.get("profile") if isinstance(payload.get("profile"), dict) else {}
        if profile.get("profile_type") != entity_type:
            issues.append("public entity: profile.profile_type must equal entity_type")
        if entity_type == "EXHIBITION":
            issues.append("public entity: Exhibition is reserved and cannot have a published instance")
        slug = payload.get("public_slug")
        route = payload.get("canonical_route")
        page_exposure = payload.get("page_exposure")
        route_prefixes = {
            "ARTIST": "/museum/network/artists/",
            "ORGANIZATION": "/museum/network/organizations/",
            "PROJECT_OR_SERIES": "/museum/network/projects/",
            "CURATED_ACQUISITION": "/museum/network/acquisitions/",
            "RESEARCH_PUBLICATION": "/museum/network/research/",
            "WORK": "/museum/network/works/",
            "ACQUISITION_PROGRAM": "/museum/network/acquisition-programs/",
        }
        if entity_type in PUBLIC_CANONICAL_PAGE_TYPES:
            if page_exposure != "canonical_page":
                issues.append(f"public entity: {entity_type} must declare canonical_page exposure")
            if entity_type == "INSTITUTION":
                if slug is not None or route != "/museum/network":
                    issues.append("public entity: Institution must use null public_slug and /museum/network")
            elif entity_type == "COLLECTION":
                if slug is not None or route != "/museum/network/collection":
                    issues.append("public entity: Collection must use null public_slug and /museum/network/collection")
            else:
                if not isinstance(slug, str) or not isinstance(route, str):
                    issues.append(f"public entity: {entity_type} canonical page requires stored public_slug and route")
                elif route != route_prefixes[entity_type] + slug:
                    issues.append(f"public entity: {entity_type} canonical_route must equal its route prefix plus stored public_slug")
        elif entity_type in PUBLIC_RELATIONAL_ONLY_TYPES:
            if page_exposure != "relational_only" or slug is not None or route is not None:
                issues.append(f"public entity: {entity_type} is relational_only and cannot publish a slug or visitor route")
        elif entity_type == "EXHIBITION":
            if page_exposure != "reserved_no_instance" or slug is not None or route is not None:
                issues.append("public entity: Exhibition is reserved_no_instance and cannot publish a route")
        else:
            issues.append(f"public entity: unsupported page exposure type {entity_type!r}")
        if entity_type == "CURATED_ACQUISITION":
            pattern = public_entity_id_pattern(entity_type, identity_inventory)
            if not (isinstance(payload.get("entity_id"), str) and isinstance(pattern, str) and re.fullmatch(pattern, payload["entity_id"])):
                issues.append("public entity: Curated Acquisition entity_id must use the stable 6529NM-CA-YYYY-NNN pattern")
            facts = profile.get("independent_acquisition_facts")
            if not isinstance(facts, dict) or set(facts) != {"mint", "payment", "title", "custody", "rights", "technical", "preservation", "display"}:
                issues.append("public entity: curated acquisition requires all eight typed independent acquisition facts")
            lifecycle = profile.get("lifecycle", {}).get("status") if isinstance(profile.get("lifecycle"), dict) else None
            collection_effect = profile.get("collection_effect")
            if lifecycle == "accessioned_into_permanent_collection" and collection_effect != "permanent_collection":
                issues.append("public entity: accessioned Curated Acquisition must have permanent_collection effect")
            if lifecycle in {"proposed_in_museum_wave", "selected_by_museum_wave_acquisition_review_in_progress", "selected_through_acquisition_program_acquisition_pending"} and collection_effect == "permanent_collection":
                issues.append("public entity: proposed/selected Curated Acquisition cannot have permanent_collection effect")
            observations = profile.get("lifecycle_observations")
            if isinstance(observations, list) and observations:
                latest = max(observations, key=lambda item: item.get("observed_at", ""))
                if latest.get("status") != lifecycle:
                    issues.append("public entity: Curated Acquisition lifecycle must equal its latest append-only observation")
                if lifecycle == "selected_by_museum_wave_acquisition_review_in_progress":
                    if latest.get("source_status") != "WINNER":
                        issues.append("public entity: Museum Wave-selected Curated Acquisition requires a WINNER source observation")
                    source_ids = latest.get("source_record_ids", [])
                    if not any(
                        isinstance(record_id, str) and re.fullmatch(r"6529NM-WAVE-OBS-\d{4}-\d{2}-\d{2}-\d{3}", record_id)
                        for record_id in source_ids
                    ):
                        issues.append("public entity: Museum Wave-selected Curated Acquisition requires a governed WINNER observation record ID")
        if entity_type == "WORK":
            pattern = public_entity_id_pattern(entity_type, identity_inventory)
            if not (isinstance(payload.get("entity_id"), str) and isinstance(pattern, str) and re.fullmatch(pattern, payload["entity_id"])):
                issues.append("public entity: Work entity_id must use the acquisition-independent 6529NM-W-NNNN pattern")
            work_status = profile.get("work_lifecycle_status")
            museum_relation = profile.get("current_museum_relation", {}).get("relation_status") if isinstance(profile.get("current_museum_relation"), dict) else None
            membership = profile.get("collection_membership", {}).get("status") if isinstance(profile.get("collection_membership"), dict) else None
            accession_ids = profile.get("accession_entity_ids", [])
            membership_accessions = profile.get("collection_membership", {}).get("accession_entity_ids", []) if isinstance(profile.get("collection_membership"), dict) else []
            mint_fact = profile.get("mint_fact") if isinstance(profile.get("mint_fact"), dict) else {}
            if mint_fact.get("status") not in set(vocabularies.get("public_work_mint_statuses", [])):
                issues.append("public entity: Work mint_fact must use the independent closed mint status vocabulary")
            if membership == "permanent_collection" and (museum_relation != "permanent_collection" or not accession_ids or not membership_accessions):
                issues.append("public entity: permanent Collection membership requires a permanent Museum relation and accession IDs")
            if museum_relation == "permanent_collection" and membership != "permanent_collection":
                issues.append("public entity: permanent Museum relation contradicts Collection membership")
            if work_status in {"proposed_in_museum_wave", "selected_by_museum_wave_acquisition_review_in_progress", "selected_through_acquisition_program", "not_established"} and membership == "permanent_collection":
                issues.append("public entity: proposed/selected/not-in-collection Work cannot be a permanent Collection member")
            if work_status == "accessioned" and membership != "permanent_collection":
                issues.append("public entity: accessioned Work requires permanent Collection membership")
            if work_status == "selected_by_museum_wave_acquisition_review_in_progress":
                if museum_relation != "selected_by_museum_wave":
                    issues.append("public entity: Museum Wave-selected Work requires the selected_by_museum_wave current relation")
                if membership != "not_in_collection":
                    issues.append("public entity: Museum Wave-selected Work must remain outside the permanent Collection")
                observations = profile.get("lifecycle_observations")
                latest = max(observations, key=lambda item: item.get("observed_at", "")) if isinstance(observations, list) and observations else {}
                if latest.get("status") != work_status or latest.get("source_status") != "WINNER":
                    issues.append("public entity: Museum Wave-selected Work requires a latest WINNER lifecycle observation")
                source_ids = latest.get("source_record_ids", [])
                if not any(
                    isinstance(record_id, str) and re.fullmatch(r"6529NM-WAVE-OBS-\d{4}-\d{2}-\d{2}-\d{3}", record_id)
                    for record_id in source_ids
                ):
                    issues.append("public entity: Museum Wave-selected Work requires a governed WINNER observation record ID")
        if entity_type == "MEDIA_REFERENCE" and isinstance(profile.get("media"), dict):
            issues.extend(validate_public_media(profile["media"], "public entity profile.media"))
        if "image_url" in payload or has_key_recursive(profile, "image_url"):
            issues.append("public entity: generic image_url is prohibited")
    elif record_type == PUBLIC_RELATION_TYPE:
        if payload.get("relation_id") != payload.get("record_id"):
            issues.append("public relation: relation_id must equal record_id")
        if payload.get("source_entity_id") == payload.get("target_entity_id"):
            issues.append("public relation: source and target must differ")
        if payload.get("relation_type") == "ENTITY_HAS_MEDIA" and "media_projection" in payload:
            issues.append("public relation: complete media identity belongs to the MEDIA_REFERENCE target, not a duplicated media_projection")
    return issues


def _typed_reference_record_index(repository_root: Path) -> dict[str, set[tuple[str, Path]]]:
    """Index authoritative record IDs and typed aliases for closed references."""

    index: dict[str, set[tuple[str, Path]]] = {}
    alias_keys = {
        "entity_id", "relation_id", "program_id", "proposal_id", "object_id",
        "accession_lot_id", "accession_number", "outcome_id", "publication_id", "accession_id",
        "observation_id", "amendment_id", "candidate_object_id",
    }

    def register(identifier: Any, record_type: Any, path: Path) -> None:
        if isinstance(identifier, str) and isinstance(record_type, str):
            index.setdefault(identifier, set()).add((record_type, path))

    def register_aliases(value: Any, record_type: Any, path: Path) -> None:
        if isinstance(value, dict):
            for key, child in value.items():
                if key in alias_keys:
                    register(child, record_type, path)
                register_aliases(child, record_type, path)
        elif isinstance(value, list):
            for child in value:
                register_aliases(child, record_type, path)

    records_dir = repository_root / "records"
    for path in (sorted(records_dir.rglob("*.json")) if records_dir.is_dir() else []):
        try:
            record = load_json(path)
        except (OSError, json.JSONDecodeError, DuplicateJsonKeyError):
            continue
        if not isinstance(record, dict):
            continue
        payload = record.get("payload") if record.get("$schema") == OFFCHAIN_ENVELOPE_SCHEMA else record
        if not isinstance(payload, dict):
            continue
        record_type = payload.get("record_type")
        register(payload.get("record_id"), record_type, path)
        register_aliases(payload, record_type, path)
    return index


def _typed_reference_registry_index(identity_inventory: dict[str, Any] | None) -> tuple[dict[tuple[str, str], dict[str, Any]], list[str]]:
    """Load the governed typed-target registry without accepting ambiguity."""

    issues: list[str] = []
    rows = identity_inventory.get("typed_reference_registry") if isinstance(identity_inventory, dict) else None
    if not isinstance(rows, list):
        return {}, ["public entity inventory: typed_reference_registry is missing"]
    index: dict[tuple[str, str], dict[str, Any]] = {}
    for row in rows:
        if not isinstance(row, dict):
            issues.append("public entity inventory: typed_reference_registry entries must be objects")
            continue
        key = (str(row.get("reference_type")), str(row.get("target_id")))
        if key in index:
            issues.append(f"public entity inventory: duplicate typed reference target {key[0]}:{key[1]}")
            continue
        if row.get("registry_id") != TYPED_REFERENCE_REGISTRY_ID:
            issues.append(f"public entity inventory: typed reference target {key[1]!r} has an unknown registry_id")
        allowed_target_types = TYPED_REFERENCE_TARGET_TYPE_MATRIX.get((str(row.get("reference_type")), "governed_typed_registry"), set())
        if row.get("target_type") not in allowed_target_types:
            issues.append(
                f"public entity inventory: typed reference target {key[1]!r} has target_type {row.get('target_type')!r} outside the closed target_type matrix"
            )
        index[key] = row
    return index, issues


def _validate_work_typed_references(
    payload: dict[str, Any],
    typed_record_index: dict[str, set[tuple[str, Path]]],
    typed_registry: dict[tuple[str, str], dict[str, Any]],
    display_path: str,
) -> tuple[list[str], set[tuple[str, str]]]:
    """Require every Work component/manifestation target to be closed and typed."""

    issues: list[str] = []
    used_registry_targets: set[tuple[str, str]] = set()
    profile = payload.get("profile") if isinstance(payload.get("profile"), dict) else {}
    declared_sources = set(payload.get("references", [])) if isinstance(payload.get("references"), list) else set()
    for field, expected_reference_type in (("component_references", "component"), ("manifestation_references", "manifestation")):
        references = profile.get(field, [])
        if not isinstance(references, list):
            continue
        for index, reference in enumerate(references):
            label = f"{display_path}.profile.{field}[{index}]"
            if not isinstance(reference, dict):
                issues.append(f"{label}: typed reference must be an object")
                continue
            reference_type = reference.get("reference_type")
            target_id = reference.get("record_id")
            source_record_id = reference.get("source_record_id")
            target_kind = reference.get("target_kind")
            target_type = reference.get("target_type")
            registry_id = reference.get("registry_id")
            if reference_type != expected_reference_type:
                issues.append(f"{label}: reference_type must be {expected_reference_type}")
            if not isinstance(target_id, str) or not target_id:
                issues.append(f"{label}: record_id must identify an explicit target")
                continue
            if not isinstance(source_record_id, str) or not source_record_id:
                issues.append(f"{label}: source_record_id must identify the target's source record")
            elif source_record_id not in declared_sources:
                issues.append(f"{label}: source_record_id {source_record_id!r} is not declared by the Work references")
            if not isinstance(target_type, str) or not target_type:
                issues.append(f"{label}: target_type is required")
            elif target_type not in TYPED_REFERENCE_TARGET_TYPE_MATRIX.get((expected_reference_type, target_kind), set()):
                issues.append(
                    f"{label}: target_type {target_type!r} is outside the closed target_type matrix for "
                    f"{expected_reference_type}/{target_kind}"
                )
            if target_kind == "authoritative_record":
                if registry_id is not None:
                    issues.append(f"{label}: authoritative_record target must not carry a registry_id")
                if target_id != source_record_id:
                    issues.append(f"{label}: authoritative_record target record_id must equal source_record_id")
                candidates = typed_record_index.get(target_id, set())
                if not candidates:
                    issues.append(f"{label}: authoritative target {target_id!r} does not resolve to a repository record")
                else:
                    matching_candidates = {
                        candidate for candidate in candidates
                        if isinstance(target_type, str) and candidate[0] == target_type
                    }
                    if not matching_candidates:
                        actual_types = sorted({record_type for record_type, _path in candidates})
                        issues.append(f"{label}: authoritative target {target_id!r} has target_type {target_type!r}, expected one of {actual_types}")
                    elif len(matching_candidates) != 1:
                        issues.append(f"{label}: authoritative target {target_id!r} must resolve to exactly one {target_type} repository record")
            elif target_kind == "governed_typed_registry":
                if registry_id != TYPED_REFERENCE_REGISTRY_ID:
                    issues.append(f"{label}: governed target must use registry_id {TYPED_REFERENCE_REGISTRY_ID}")
                key = (expected_reference_type, target_id)
                entry = typed_registry.get(key)
                if entry is None:
                    issues.append(f"{label}: governed typed target {target_id!r} is not in the closed registry")
                else:
                    used_registry_targets.add(key)
                    if entry.get("target_type") != target_type:
                        issues.append(f"{label}: governed target {target_id!r} has mismatched target_type")
                    if entry.get("authoritative_record_id") != source_record_id:
                        issues.append(f"{label}: governed target {target_id!r} has mismatched authoritative source record")
                    if reference.get("caip19") != entry.get("caip19"):
                        issues.append(f"{label}: governed target {target_id!r} has mismatched CAIP-19 manifestation identity")
                    authoritative_id = entry.get("authoritative_record_id")
                    authoritative_type = entry.get("authoritative_record_type")
                    authoritative_candidates = typed_record_index.get(authoritative_id, set()) if isinstance(authoritative_id, str) else set()
                    if not authoritative_candidates:
                        issues.append(f"{label}: governed target {target_id!r} has an unresolved authoritative source record")
                    else:
                        matching_authorities = {
                            candidate for candidate in authoritative_candidates
                            if isinstance(authoritative_type, str) and candidate[0] == authoritative_type
                        }
                        if len(matching_authorities) != 1:
                            issues.append(
                                f"{label}: governed target {target_id!r} must resolve to exactly one "
                                f"{authoritative_type} authoritative source record"
                            )
            else:
                issues.append(f"{label}: target_kind must be authoritative_record or governed_typed_registry")
    return issues, used_registry_targets


def validate_semantics(record: dict[str, Any], vocabularies: dict[str, Any], identity_inventory: dict[str, Any] | None = None, repository_root: Path = REPO_ROOT) -> list[str]:
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
    payload_commitment = payload.get("payload_sha256")
    if isinstance(payload_commitment, str):
        payload_without_commitment = dict(payload)
        payload_without_commitment.pop("payload_sha256", None)
        expected_omitted_commitment = "sha256:" + hashlib.sha256(canonicalize(payload_without_commitment)).hexdigest()
        payload_with_zero_commitment = dict(payload)
        payload_with_zero_commitment["payload_sha256"] = "sha256:" + "0" * 64
        expected_zero_commitment = "sha256:" + hashlib.sha256(canonicalize(payload_with_zero_commitment)).hexdigest()
        if payload_commitment not in {expected_omitted_commitment, expected_zero_commitment}:
            issues.append(
                "payload.payload_sha256 does not match the canonical payload under the omitted-field or zeroed-field commitment rule; "
                f"expected {expected_omitted_commitment} or {expected_zero_commitment}"
            )
    else:
        issues.append("payload.payload_sha256 must be a sha256 commitment string")
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
    if isinstance(reviewer_data, dict):
        try:
            if parse_time(reviewer_data["reviewed_at"], "reviewer.reviewed_at") < parse_time(payload["created_at"], "created_at"):
                issues.append("reviewer.reviewed_at must not precede created_at")
        except (KeyError, ValueError) as exc:
            issues.append(str(exc))
    issues.extend(inspect_sensitive(payload))
    issues.extend(validate_gift_acceptance_authorization(payload))
    issues.extend(validate_visual_observation(payload))
    provenance_schedule = payload.get("provenance_schedule") if record_type == "ACCESSION_LOT" else payload if record_type == "transaction_provenance_schedule" else None
    if isinstance(provenance_schedule, dict):
        issues.extend(validate_provenance_schedule(provenance_schedule))
    if record_type == "GOVERNANCE_DECISION":
        source_status = source_data.get("status") if isinstance(source_data, dict) else None
        decision_status = payload.get("decision_status")
        if source_status == "WINNER" and decision_status != "adopted":
            issues.append("governance evidence: WINNER must be recorded as adopted")
        if source_status == "PARTICIPATORY" and decision_status == "adopted":
            issues.append("governance evidence: PARTICIPATORY cannot be recorded as adopted")
    if record_type == "WAVE_STATUS_OBSERVATION":
        expected = {
            "observation_id": "6529NM-WAVE-OBS-2026-08-08-001",
            "proposal_id": "6529NM-PG-2026-001",
            "wave_id": "5f207393-5418-4a75-8738-e40edb44a94d",
            "drop_id": "002bfa4f-8416-48bf-b35e-38f354e9a9f0",
            "serial_no": 1276093,
            "signed": True,
            "drop_type": "WINNER",
            "source_status": "WINNER",
            "rating": 121603214,
            "realtime_rating": 121603214,
            "rater_count": 29,
            "selection_effect": "selected_by_museum_wave_acquisition_review_in_progress",
        }
        for key, value in expected.items():
            if payload.get(key) != value:
                issues.append(f"WAVE_STATUS_OBSERVATION.{key} must preserve the signed-drop API WINNER status readback")
        prior = payload.get("prior_observation") if isinstance(payload.get("prior_observation"), dict) else {}
        if prior.get("source_status") != "PARTICIPATORY" or prior.get("source_record_id") != "6529NM-PG-2026-001":
            issues.append("WAVE_STATUS_OBSERVATION must retain the earlier PARTICIPATORY proposal observation")
        if payload.get("observation_method") != "signed_drop_api_readback":
            issues.append("WAVE_STATUS_OBSERVATION must use the precise signed_drop_api_readback method")
    if record_type == "WAVE_PUBLICATION_OBSERVATION":
        issues.extend(validate_wave_publication_observation(payload, repository_root))
    if record_type == "MEDIA_DESCRIPTION_AMENDMENT":
        issues.extend(validate_media_description_amendment(payload, repository_root))
    issues.extend(validate_state_machine(payload, vocabularies))
    issues.extend(validate_event_history(payload))
    issues.extend(validate_public_payload(payload, vocabularies, identity_inventory))
    return issues


def validate_public_graph(
    records: list[tuple[Path, dict[str, Any], dict[str, Any] | None]],
    vocabularies: dict[str, Any],
    identity_inventory: dict[str, Any] | None = None,
    repository_root: Path = REPO_ROOT,
) -> list[str]:
    """Validate the closed public entity/relation graph after all records are loaded."""
    issues: list[str] = []
    entities: dict[str, tuple[Path, dict[str, Any]]] = {}
    relations: list[tuple[Path, dict[str, Any]]] = []
    wave_status_observations: dict[str, tuple[Path, dict[str, Any]]] = {}
    media_presentation_amendments: dict[str, tuple[Path, dict[str, Any]]] = {}
    for path, _record, payload in records:
        if not isinstance(payload, dict):
            continue
        if payload.get("record_type") == PUBLIC_ENTITY_TYPE:
            entity_id = payload.get("entity_id")
            if isinstance(entity_id, str):
                entities[entity_id] = (path, payload)
        elif payload.get("record_type") == PUBLIC_RELATION_TYPE:
            relations.append((path, payload))
        elif payload.get("record_type") == "WAVE_STATUS_OBSERVATION":
            observation_id = payload.get("observation_id")
            if isinstance(observation_id, str):
                wave_status_observations[observation_id] = (path, payload)
        elif payload.get("record_type") == "MEDIA_PRESENTATION_AMENDMENT":
            amendment_id = payload.get("amendment_id")
            if isinstance(amendment_id, str):
                media_presentation_amendments[amendment_id] = (path, payload)

    typed_record_index = _typed_reference_record_index(repository_root)
    typed_registry, typed_registry_issues = _typed_reference_registry_index(identity_inventory)
    issues.extend(typed_registry_issues)
    used_registry_targets: set[tuple[str, str]] = set()

    def display_path(path: Path) -> str:
        try:
            return path.relative_to(REPO_ROOT).as_posix()
        except ValueError:
            return path.as_posix()

    slug_paths: dict[tuple[str, str], Path] = {}
    route_paths: dict[str, Path] = {}
    route_prefixes = {
        "ARTIST": "/museum/network/artists/",
        "ORGANIZATION": "/museum/network/organizations/",
        "PROJECT_OR_SERIES": "/museum/network/projects/",
        "CURATED_ACQUISITION": "/museum/network/acquisitions/",
        "RESEARCH_PUBLICATION": "/museum/network/research/",
        "WORK": "/museum/network/works/",
        "ACQUISITION_PROGRAM": "/museum/network/acquisition-programs/",
    }
    for entity_id, (path, payload) in entities.items():
        entity_type = payload.get("entity_type")
        slug = payload.get("public_slug")
        route = payload.get("canonical_route")
        page_exposure = payload.get("page_exposure")
        relative = display_path(path)
        if entity_type in {"INSTITUTION", "COLLECTION"}:
            expected_route = "/museum/network" if entity_type == "INSTITUTION" else "/museum/network/collection"
            if page_exposure != "canonical_page" or slug is not None or route != expected_route:
                issues.append(f"{relative}: singleton {entity_type} must use canonical_page, null public_slug, and {expected_route}")
        elif entity_type in PUBLIC_RELATIONAL_ONLY_TYPES:
            if page_exposure != "relational_only" or slug is not None or route is not None:
                issues.append(f"{relative}: relational-only {entity_type} must use null public_slug and canonical_route")
        elif entity_type == "EXHIBITION":
            issues.append(f"{relative}: Exhibition is reserved; no published PUBLIC_ENTITY instance is allowed")
        elif entity_type in route_prefixes:
            expected_route = route_prefixes[entity_type] + slug if isinstance(slug, str) else None
            if page_exposure != "canonical_page" or not isinstance(slug, str) or route != expected_route:
                issues.append(f"{relative}: {entity_type} canonical_route must equal its route prefix plus stored public_slug")
        else:
            issues.append(f"{relative}: unsupported public entity type {entity_type!r}")
        if entity_type == "WORK":
            typed_issues, used_targets = _validate_work_typed_references(
                payload,
                typed_record_index,
                typed_registry,
                relative,
            )
            issues.extend(typed_issues)
            used_registry_targets.update(used_targets)
        profile = payload.get("profile") if isinstance(payload.get("profile"), dict) else {}
        if entity_type == "CURATED_ACQUISITION":
            lifecycle = profile.get("lifecycle", {}).get("status") if isinstance(profile.get("lifecycle"), dict) else None
            observations = profile.get("lifecycle_observations")
        elif entity_type == "WORK":
            lifecycle = profile.get("work_lifecycle_status")
            observations = profile.get("lifecycle_observations")
        else:
            lifecycle = None
            observations = None
        if lifecycle == "selected_by_museum_wave_acquisition_review_in_progress":
            latest = max(observations, key=lambda item: item.get("observed_at", "")) if isinstance(observations, list) and observations else {}
            winner_records = [
                wave_status_observations[record_id][1]
                for record_id in latest.get("source_record_ids", [])
                if isinstance(record_id, str) and record_id in wave_status_observations
            ]
            if not any(record.get("source_status") == "WINNER" and record.get("drop_type") == "WINNER" for record in winner_records):
                issues.append(f"{relative}: selected Museum Wave lifecycle must resolve to a governed WINNER observation record")
        if isinstance(slug, str):
            slug_key = (str(entity_type), slug)
            if slug_key in slug_paths and slug_paths[slug_key] != path:
                issues.append(f"{relative}: duplicate public_slug {slug} within {entity_type}; first seen at {display_path(slug_paths[slug_key])}")
            else:
                slug_paths[slug_key] = path
        if isinstance(route, str):
            if route in route_paths and route_paths[route] != path:
                issues.append(f"{relative}: duplicate canonical_route {route}; first seen at {display_path(route_paths[route])}")
            else:
                route_paths[route] = path

    relation_profiles = vocabularies.get("relation_profiles", {})
    active_relation_keys: dict[tuple[str, str, str], Path] = {}
    source_counts: dict[tuple[str, str], int] = {}
    target_counts: dict[tuple[str, str], int] = {}
    for path, relation in relations:
        relation_type = relation.get("relation_type")
        profile = relation_profiles.get(relation_type)
        relative = display_path(path)
        if not isinstance(profile, dict):
            issues.append(f"{relative}: unknown public relation type {relation_type!r}")
            continue
        source_id = relation.get("source_entity_id")
        target_id = relation.get("target_entity_id")
        source = entities.get(source_id) if isinstance(source_id, str) else None
        target = entities.get(target_id) if isinstance(target_id, str) else None
        if source is None:
            issues.append(f"{relative}: source_entity_id does not resolve to a PUBLIC_ENTITY")
            continue
        if target is None:
            issues.append(f"{relative}: target_entity_id does not resolve to a PUBLIC_ENTITY")
            continue
        source_type = source[1].get("entity_type")
        target_type = target[1].get("entity_type")
        if source_type not in profile.get("source_entity_types", []):
            issues.append(f"{relative}: relation {relation_type} has invalid source entity type {source_type}")
        if target_type not in profile.get("target_entity_types", []):
            issues.append(f"{relative}: relation {relation_type} has invalid target entity type {target_type}")
        qualifier = relation.get("qualifier") if isinstance(relation.get("qualifier"), dict) else {}
        allowed = set(profile.get("allowed_qualifier_fields", []))
        required = set(profile.get("required_qualifier_fields", []))
        unknown_qualifiers = set(qualifier) - allowed
        if unknown_qualifiers:
            issues.append(f"{relative}: relation {relation_type} has unsupported qualifiers {sorted(unknown_qualifiers)}")
        missing_qualifiers = {field for field in required if qualifier.get(field) is None}
        if missing_qualifiers:
            issues.append(f"{relative}: relation {relation_type} is missing required qualifiers {sorted(missing_qualifiers)}")
        allowed_values = profile.get("allowed_qualifier_values", {})
        if isinstance(allowed_values, dict):
            for field, allowed_values_for_field in allowed_values.items():
                if field in qualifier and isinstance(allowed_values_for_field, list) and qualifier[field] not in allowed_values_for_field:
                    issues.append(f"{relative}: relation {relation_type} qualifier {field}={qualifier[field]!r} is not allowed")
        if source_id == target_id:
            issues.append(f"{relative}: public relation cannot point to itself")
        reserved = bool(profile.get("reserved"))
        if reserved and relation.get("assertion_status") != "reserved":
            issues.append(f"{relative}: reserved relation {relation_type} must use assertion_status reserved")
        if not reserved and relation.get("assertion_status") == "reserved":
            issues.append(f"{relative}: non-reserved relation {relation_type} cannot use assertion_status reserved")
        active = relation.get("record_status") != "superseded" and relation.get("assertion_status") != "reserved"
        relation_key = (relation_type, source_id, target_id)
        if active:
            if relation_key in active_relation_keys:
                issues.append(f"{relative}: duplicate active relation {relation_type} for {source_id} -> {target_id}; first seen at {display_path(active_relation_keys[relation_key])}")
            else:
                active_relation_keys[relation_key] = path
            source_counts[(relation_type, source_id)] = source_counts.get((relation_type, source_id), 0) + 1
            target_counts[(relation_type, target_id)] = target_counts.get((relation_type, target_id), 0) + 1
        max_targets = profile.get("max_targets_per_source")
        max_sources = profile.get("max_sources_per_target")
        if max_targets is not None and source_counts.get((relation_type, source_id), 0) > max_targets:
            issues.append(f"{relative}: relation {relation_type} exceeds source cardinality {max_targets}")
        if max_sources is not None and target_counts.get((relation_type, target_id), 0) > max_sources:
            issues.append(f"{relative}: relation {relation_type} exceeds target cardinality {max_sources}")

        if relation_type == "ENTITY_HAS_MEDIA":
            target_profile = target[1].get("profile", {})
            media = target_profile.get("media") if isinstance(target_profile, dict) else None
            if target_type != "MEDIA_REFERENCE" or not isinstance(media, dict):
                issues.append(f"{relative}: ENTITY_HAS_MEDIA must target a MEDIA_REFERENCE with a complete media profile")
            else:
                if media.get("subject_entity_id") != source_id:
                    issues.append(f"{relative}: media subject_entity_id must equal relation source_entity_id")
                if target_id not in source[1].get("media_entity_ids", []):
                    issues.append(f"{relative}: source entity must list the target in media_entity_ids")
                context_ids = set(media.get("publication_context_entity_ids", []))
                if context_ids:
                    context_id = qualifier.get("publication_context_entity_id")
                    if context_id not in context_ids:
                        issues.append(f"{relative}: media publication context must be explicitly carried by the ENTITY_HAS_MEDIA relation")
                    if source_id != context_id:
                        source_profile = source[1].get("profile", {})
                        if source_type != "WORK" or context_id not in source_profile.get("acquisition_entity_ids", []):
                            issues.append(f"{relative}: media may only be reused in its declared acquisition/linked Work context")
                if media.get("media_role") == "historical_wave_proposal_presentation" and qualifier.get("publication_context_entity_id") != "6529NM-CA-2026-003":
                    issues.append(f"{relative}: historical Wave proposal media must be joined only in the CA-003 context")
        elif relation_type == "INSTITUTION_HOLDS_COLLECTION":
            if source[1].get("profile", {}).get("collection_entity_id") != target_id:
                issues.append(f"{relative}: institution profile collection_entity_id must match relation target")
        elif relation_type == "ARTIST_CREATES_WORK":
            if source_id not in target[1].get("profile", {}).get("creator_entity_ids", []):
                issues.append(f"{relative}: Work creator_entity_ids must include the Artist/Agent source")
        elif relation_type == "AGENT_PLAYS_ROLE":
            if target_type == "PROJECT_OR_SERIES":
                project_profile = target[1].get("profile", {})
                declared_agents = set(project_profile.get("agent_entity_ids", []))
                if source_id not in declared_agents:
                    issues.append(f"{relative}: Project agent relation source is missing from agent_entity_ids")
                role = qualifier.get("role")
                if not isinstance(role, str) or not role:
                    issues.append(f"{relative}: Project agent relation requires a non-empty role qualifier")
                project_sources = set(project_profile.get("source_record_ids", []))
                relation_sources = relation.get("source_record_ids")
                if not isinstance(relation_sources, list) or not project_sources.intersection(relation_sources):
                    issues.append(f"{relative}: Project agent relation must carry source_record_ids that back the Project assertion")
        elif relation_type == "PROJECT_CONTEXTUALIZES_WORK":
            if target_id not in source[1].get("profile", {}).get("work_entity_ids", []):
                issues.append(f"{relative}: Project/Series work_entity_ids must include the relation target")
        elif relation_type == "ACQUISITION_PROGRAM_PRODUCES_ACQUISITION":
            source_profile = source[1].get("profile", {})
            target_pathway = target[1].get("profile", {}).get("program_or_pathway", {})
            produced_ids = source_profile.get("produced_acquisition_entity_ids", [])
            if target_id not in produced_ids:
                issues.append(f"{relative}: Acquisition Program produced_acquisition_entity_ids must include the relation target")
            if source_id not in target_pathway.get("entity_ids", []):
                issues.append(f"{relative}: Curated Acquisition program_or_pathway must include the program source")
        elif relation_type == "CURATED_ACQUISITION_BRINGS_TOGETHER_WORK":
            if target_id not in source[1].get("profile", {}).get("work_entity_ids", []):
                issues.append(f"{relative}: Curated Acquisition work_entity_ids must include the relation target")
        elif relation_type == "PROGRAM_SELECTS_WORK":
            if qualifier.get("selection_status") != "selected_unminted":
                issues.append(f"{relative}: PROGRAM_SELECTS_WORK must preserve the source outcome status selected_unminted")
            if qualifier.get("mint_status") not in {"pending", "not_started", "verified", "not_applicable"}:
                issues.append(f"{relative}: PROGRAM_SELECTS_WORK must carry an independent mint_status qualifier")
            selected_outcomes = set(source[1].get("profile", {}).get("selected_outcome_record_ids", []))
            if not selected_outcomes.intersection(set(relation.get("source_record_ids", []))):
                issues.append(f"{relative}: PROGRAM_SELECTS_WORK source_record_ids must identify a durable program outcome")
        elif relation_type == "ACCESSION_ADMITS_WORK":
            accession_profile = source[1].get("profile", {})
            work_profile = target[1].get("profile", {})
            if accession_profile.get("accession_status") != "complete" or target_id not in accession_profile.get("admitted_work_entity_ids", []):
                issues.append(f"{relative}: accession relation must point from a complete accession that admits the Work")
            if work_profile.get("work_lifecycle_status") != "accessioned":
                issues.append(f"{relative}: accession relation requires an accessioned Work lifecycle")
        elif relation_type == "COLLECTION_CONTAINS_WORK":
            collection_profile = source[1].get("profile", {})
            membership = target[1].get("profile", {}).get("collection_membership", {})
            if collection_profile.get("membership_rule") != "accession_only" or membership.get("status") != "permanent_collection":
                issues.append(f"{relative}: Collection membership requires accession_only policy and permanent Work membership")
            if qualifier.get("collection_membership_status") != membership.get("status"):
                issues.append(f"{relative}: Collection relation membership qualifier must equal the Work collection membership status")
            if membership.get("collection_entity_id") != source_id:
                issues.append(f"{relative}: Work collection_entity_id must equal the Collection relation source")

    casey_amendment_entry = media_presentation_amendments.get("6529NM-MEDIA-PRES-AMD-2026-08-09-001")
    if entities and casey_amendment_entry is None:
        amendment_path = repository_root / "records/accessions/6529NM.2026.001/media-presentation-amendment-2026-08-09.json"
        try:
            amendment_record = load_json(amendment_path)
        except (OSError, ValueError, DuplicateJsonKeyError):
            amendment_record = None
        amendment_payload = amendment_record.get("payload") if isinstance(amendment_record, dict) else None
        if (
            isinstance(amendment_payload, dict)
            and amendment_payload.get("record_type") == "MEDIA_PRESENTATION_AMENDMENT"
            and amendment_payload.get("amendment_id") == "6529NM-MEDIA-PRES-AMD-2026-08-09-001"
        ):
            casey_amendment_entry = (amendment_path, amendment_payload)
    if entities and casey_amendment_entry is None:
        issues.append("Casey media presentation correction is missing from the candidate graph source set")
    elif casey_amendment_entry is not None:
        amendment_path, amendment = casey_amendment_entry
        amendment_label = display_path(amendment_path)
        corrections = amendment.get("presentation_corrections")
        if not isinstance(corrections, list) or len(corrections) != 7:
            issues.append(f"{amendment_label}: active Casey media correction must contain exactly seven rows")
            corrections = []
        expected_object_ids = {f"6529NM.2026.001.0{index}" for index in range(1, 8)}
        if {row.get("object_id") for row in corrections if isinstance(row, dict)} != expected_object_ids:
            issues.append(f"{amendment_label}: Casey media correction rows must exactly cover objects .01-.07")
        active_media_relations = {
            (relation.get("source_entity_id"), relation.get("target_entity_id")): relation
            for _relation_path, relation in relations
            if relation.get("relation_type") == "ENTITY_HAS_MEDIA"
            and relation.get("record_status") != "superseded"
            and relation.get("assertion_status") != "reserved"
        }
        for row in corrections:
            if not isinstance(row, dict):
                continue
            object_id = row.get("object_id")
            work_id = row.get("work_entity_id")
            still_id = row.get("still_media_entity_id")
            live_id = row.get("live_media_entity_id")
            rights_id = row.get("rights_record_id")
            license_url = row.get("license_url")
            work_entry = entities.get(work_id) if isinstance(work_id, str) else None
            still_entry = entities.get(still_id) if isinstance(still_id, str) else None
            live_entry = entities.get(live_id) if isinstance(live_id, str) else None
            if work_entry is None or still_entry is None or live_entry is None:
                issues.append(f"{amendment_label}: {object_id} correction does not resolve its Work, still, and live entities")
                continue
            expected_media = [still_id, live_id]
            if object_id == "6529NM.2026.001.01":
                expected_media.extend(["6529NM-MED-0001", "6529NM-MED-0002"])
            if work_entry[1].get("media_entity_ids") != expected_media:
                issues.append(f"{display_path(work_entry[0])}: Casey Work media order must be still, live, then retained nonvisual evidence where applicable")
            for media_id, media_entry, expected, order in (
                (still_id, still_entry, row.get("still"), 1),
                (live_id, live_entry, row.get("live"), 2),
            ):
                media = media_entry[1].get("profile", {}).get("media", {})
                relation = active_media_relations.get((work_id, media_id))
                if not isinstance(expected, dict) or not isinstance(media, dict):
                    issues.append(f"{display_path(media_entry[0])}: Casey governed media profile is missing")
                    continue
                expected_dimensions = expected.get("dimensions") if order == 1 else expected.get("observed_canvas_dimensions")
                if media.get("visual") is not True or media.get("media_type") != expected.get("media_type"):
                    issues.append(f"{display_path(media_entry[0])}: Casey still/live media must be visual with the governed MIME type")
                if not isinstance(expected_dimensions, dict) or media.get("width") != expected_dimensions.get("width") or media.get("height") != expected_dimensions.get("height"):
                    issues.append(f"{display_path(media_entry[0])}: Casey media geometry must match the governed still-response or live-canvas dimensions")
                locator = media.get("source_locator") if isinstance(media.get("source_locator"), dict) else {}
                observation = media.get("source_observation") if isinstance(media.get("source_observation"), dict) else {}
                if locator.get("uri") != expected.get("source_url") or observation.get("status") != "mutable_external":
                    issues.append(f"{display_path(media_entry[0])}: Casey media must retain the exact official mutable Art Blocks source")
                if media.get("accessibility_text") != (row.get("accessibility_text") if order == 1 else expected.get("accessibility_text")):
                    issues.append(f"{display_path(media_entry[0])}: Casey media accessibility text must preserve the governed visual description")
                if media.get("credit") != row.get("credit"):
                    issues.append(f"{display_path(media_entry[0])}: Casey media credit must match its exact per-object source credit")
                if media.get("allowed_ui_affordances") != expected.get("allowed_ui_affordances"):
                    issues.append(f"{display_path(media_entry[0])}: Casey media UI affordances must match the governed presentation row")
                rights = media.get("rights") if isinstance(media.get("rights"), dict) else {}
                rights_uris = {item.get("uri") for item in rights.get("evidence_refs", []) if isinstance(item, dict)}
                expected_rights_suffix = f"/records/accessions/6529NM.2026.001/rights/{rights_id}.json"
                if rights.get("status") != "cleared_with_conditions" or license_url not in rights_uris or not any(isinstance(uri, str) and uri.endswith(expected_rights_suffix) for uri in rights_uris):
                    issues.append(f"{display_path(media_entry[0])}: Casey media must cite its exact per-object rights record and CC BY-NC 4.0 license")
                if relation is None or relation.get("qualifier") != {"display_order": order, "media_context": "primary"}:
                    issues.append(f"{display_path(media_entry[0])}: Casey Work-to-media relation must carry primary context and governed display order {order}")
                fixity = media.get("fixity") if isinstance(media.get("fixity"), dict) else {}
                basis = str(fixity.get("basis", "")).casefold()
                if order == 1:
                    required_words = ("exact observed", "mutable", "future", "not retained", "preservation master")
                    if fixity.get("status") != "verified" or fixity.get("digest") != expected.get("response_sha256") or not all(word in basis for word in required_words):
                        issues.append(f"{display_path(media_entry[0])}: Casey still fixity must bind only the exact observed response and disclaim future mutable bytes and preservation-master retention")
                elif fixity.get("status") != "unverified_not_retrieved" or fixity.get("digest") is not None or "no digest" not in basis or "mutable" not in basis:
                    issues.append(f"{display_path(media_entry[0])}: Casey live generator must remain mutable with no asserted digest")
        for evidence_media_id in ("6529NM-MED-0001", "6529NM-MED-0002"):
            evidence_entry = entities.get(evidence_media_id)
            evidence_media = evidence_entry[1].get("profile", {}).get("media", {}) if evidence_entry else {}
            if evidence_media.get("visual") is not False or evidence_media.get("media_type") != "application/json":
                issues.append(f"{evidence_media_id}: Casey preservation manifest and token metadata must remain nonvisual JSON")
        unchanged_nonvisual_ids = {
            "6529NM-MED-0003", "6529NM-MED-0041", "6529NM-MED-0042", "6529NM-MED-0043", "6529NM-MED-0044",
            *{f"6529NM-MED-{index:04d}" for index in range(20, 36)},
        }
        for media_id in sorted(unchanged_nonvisual_ids):
            media_entry = entities.get(media_id)
            media = media_entry[1].get("profile", {}).get("media", {}) if media_entry else {}
            if media.get("visual") is not False or "6529NM-MEDIA-PRES-AMD-2026-08-09-001" in media.get("source_record_ids", []):
                issues.append(f"{media_id}: Magnum and Keys and Gates nonvisual presentation state must remain outside the Casey correction")

    def id_set(value: Any) -> set[str]:
        return {item for item in value if isinstance(item, str)} if isinstance(value, list) else set()

    def active_relation_targets(relation_type: str, source_id: str) -> set[str]:
        return {
            relation.get("target_entity_id")
            for _relation_path, relation in relations
            if relation.get("relation_type") == relation_type
            and relation.get("source_entity_id") == source_id
            and relation.get("record_status") != "superseded"
            and relation.get("assertion_status") != "reserved"
            and isinstance(relation.get("target_entity_id"), str)
        }

    def active_relation_sources(relation_type: str, target_id: str) -> set[str]:
        return {
            relation.get("source_entity_id")
            for _relation_path, relation in relations
            if relation.get("relation_type") == relation_type
            and relation.get("target_entity_id") == target_id
            and relation.get("record_status") != "superseded"
            and relation.get("assertion_status") != "reserved"
            and isinstance(relation.get("source_entity_id"), str)
        }

    for collection_id, (_path, collection) in entities.items():
        if collection.get("entity_type") != "COLLECTION":
            continue
        profile = collection.get("profile", {})
        declared_work_ids = id_set(profile.get("admitted_work_entity_ids"))
        related_work_ids = active_relation_targets("COLLECTION_CONTAINS_WORK", collection_id)
        if declared_work_ids != related_work_ids:
            issues.append(
                f"{display_path(_path)}: Collection admitted_work_entity_ids must equal active COLLECTION_CONTAINS_WORK targets; "
                f"missing={sorted(declared_work_ids - related_work_ids)}, unexpected={sorted(related_work_ids - declared_work_ids)}"
            )

    for project_id, (_path, project) in entities.items():
        if project.get("entity_type") != "PROJECT_OR_SERIES":
            continue
        profile = project.get("profile", {})
        declared_work_ids = id_set(profile.get("work_entity_ids"))
        related_work_ids = active_relation_targets("PROJECT_CONTEXTUALIZES_WORK", project_id)
        if declared_work_ids != related_work_ids:
            issues.append(
                f"{display_path(_path)}: Project work_entity_ids must equal active PROJECT_CONTEXTUALIZES_WORK targets; "
                f"missing={sorted(declared_work_ids - related_work_ids)}, unexpected={sorted(related_work_ids - declared_work_ids)}"
            )

    for acquisition_id, (_path, acquisition) in entities.items():
        if acquisition.get("entity_type") != "CURATED_ACQUISITION":
            continue
        profile = acquisition.get("profile", {})
        declared_work_ids = id_set(profile.get("work_entity_ids"))
        related_work_ids = active_relation_targets("CURATED_ACQUISITION_BRINGS_TOGETHER_WORK", acquisition_id)
        if declared_work_ids != related_work_ids:
            issues.append(
                f"{display_path(_path)}: Curated Acquisition work_entity_ids must equal active CURATED_ACQUISITION_BRINGS_TOGETHER_WORK targets; "
                f"missing={sorted(declared_work_ids - related_work_ids)}, unexpected={sorted(related_work_ids - declared_work_ids)}"
            )

    for accession_id, (_path, accession) in entities.items():
        if accession.get("entity_type") != "ACCESSION":
            continue
        profile = accession.get("profile", {})
        declared_work_ids = id_set(profile.get("admitted_work_entity_ids"))
        related_work_ids = active_relation_targets("ACCESSION_ADMITS_WORK", accession_id)
        if declared_work_ids != related_work_ids:
            issues.append(
                f"{display_path(_path)}: Accession admitted_work_entity_ids must equal active ACCESSION_ADMITS_WORK targets; "
                f"missing={sorted(declared_work_ids - related_work_ids)}, unexpected={sorted(related_work_ids - declared_work_ids)}"
            )

    for work_id, (_path, work) in entities.items():
        if work.get("entity_type") != "WORK":
            continue
        profile = work.get("profile", {})
        reverse_fields = (
            ("project_or_series_entity_ids", "PROJECT_CONTEXTUALIZES_WORK"),
            ("acquisition_entity_ids", "CURATED_ACQUISITION_BRINGS_TOGETHER_WORK"),
            ("accession_entity_ids", "ACCESSION_ADMITS_WORK"),
        )
        for field, relation_type in reverse_fields:
            declared_source_ids = id_set(profile.get(field))
            related_source_ids = active_relation_sources(relation_type, work_id)
            if declared_source_ids != related_source_ids:
                issues.append(
                    f"{display_path(_path)}: Work {field} must equal active {relation_type} sources; "
                    f"missing={sorted(declared_source_ids - related_source_ids)}, unexpected={sorted(related_source_ids - declared_source_ids)}"
                )
        membership = profile.get("collection_membership") if isinstance(profile.get("collection_membership"), dict) else {}
        declared_accession_ids = id_set(profile.get("accession_entity_ids"))
        membership_accession_ids = id_set(membership.get("accession_entity_ids"))
        if declared_accession_ids != membership_accession_ids:
            issues.append(f"{display_path(_path)}: Work accession_entity_ids must equal collection_membership.accession_entity_ids")
        collection_sources = active_relation_sources("COLLECTION_CONTAINS_WORK", work_id)
        membership_status = membership.get("status")
        if membership_status == "permanent_collection":
            collection_id = membership.get("collection_entity_id")
            if collection_sources != {collection_id}:
                issues.append(
                    f"{display_path(_path)}: permanent Collection membership must equal exactly one active COLLECTION_CONTAINS_WORK source; "
                    f"declared={collection_id!r}, related={sorted(collection_sources)}"
                )
        elif collection_sources:
            issues.append(
                f"{display_path(_path)}: active COLLECTION_CONTAINS_WORK sources require permanent Collection membership; "
                f"related={sorted(collection_sources)}"
            )

    for project_id, (_path, project) in entities.items():
        if project.get("entity_type") != "PROJECT_OR_SERIES":
            continue
        declared_agents = set(project.get("profile", {}).get("agent_entity_ids", []))
        related_agents = {
            relation.get("source_entity_id")
            for _relation_path, relation in relations
            if relation.get("relation_type") in {"AGENT_PLAYS_ROLE", "ORGANIZATION_ORIGINATES_PROJECT"}
            and relation.get("target_entity_id") == project_id
            and relation.get("record_status") != "superseded"
            and relation.get("assertion_status") != "reserved"
        }
        if declared_agents != related_agents:
            issues.append(
                f"{display_path(_path)}: Project agent_entity_ids must equal active AGENT_PLAYS_ROLE sources; "
                f"missing={sorted(declared_agents - related_agents)}, unexpected={sorted(related_agents - declared_agents)}"
            )

    # The identity registry is repository-global, while several control-plane
    # fixture validations intentionally contain no public Work graph. Enforce
    # closed registry use whenever a Work projection is actually present.
    if typed_registry and any(payload.get("entity_type") == "WORK" for _path, payload in entities.values()) and used_registry_targets != set(typed_registry):
        unused = sorted(set(typed_registry) - used_registry_targets)
        issues.append(f"public entity inventory: typed reference registry contains unreferenced targets {unused}")

    # Program projections and their durable production relations must agree in
    # both directions. A pathway can explain how an acquisition was produced;
    # it can never itself create Collection membership.
    for program_id, (_path, program) in entities.items():
        if program.get("entity_type") != "ACQUISITION_PROGRAM":
            continue
        profile = program.get("profile", {})
        produced = set(profile.get("produced_acquisition_entity_ids", []))
        related = {
            relation.get("target_entity_id")
            for _relation_path, relation in relations
            if relation.get("relation_type") == "ACQUISITION_PROGRAM_PRODUCES_ACQUISITION"
            and relation.get("source_entity_id") == program_id
            and relation.get("record_status") != "superseded"
        }
        if produced != related:
            issues.append(f"{display_path(_path)}: program produced_acquisition_entity_ids must equal active production relations; missing={sorted(produced - related)}, unexpected={sorted(related - produced)}")
    gift_program = entities.get("6529NM-AP-ENT-0001")
    if gift_program is not None:
        if gift_program[1].get("profile", {}).get("program_status") != "active":
            issues.append(f"{display_path(gift_program[0])}: Gift Acquisitions must remain an active donation pathway")
        produced = set(gift_program[1].get("profile", {}).get("produced_acquisition_entity_ids", []))
        if not {"6529NM-CA-2026-001", "6529NM-CA-2026-003"}.issubset(produced):
            issues.append(f"{display_path(gift_program[0])}: Gift Acquisitions must produce the Casey and Magnum Curated Acquisitions")

    # Foundation fixture roots may intentionally contain no PUBLIC_ENTITY layer.
    # Apply the governed public identity inventory only when that layer is present;
    # otherwise generic Stream/accession fixture validation must remain independent.
    if not entities:
        return issues
    identity_inventory = identity_inventory if isinstance(identity_inventory, dict) else load_public_identity_inventory(REPO_ROOT)
    required_acquisitions = identity_inventory.get("required_bootstrap_curated_acquisitions", []) if isinstance(identity_inventory, dict) else []
    required_acquisition_ids = {row.get("entity_id") for row in required_acquisitions if isinstance(row, dict)}
    present_acquisition_ids = {entity_id for entity_id, (_path, payload) in entities.items() if payload.get("entity_type") == "CURATED_ACQUISITION"}
    if entities and not required_acquisition_ids:
        issues.append("public entity inventory: governed bootstrap Curated Acquisition inventory is missing")
    elif entities and not required_acquisition_ids.issubset(present_acquisition_ids):
        missing = sorted(required_acquisition_ids - present_acquisition_ids)
        issues.append(f"public entity inventory: governed bootstrap Curated Acquisition IDs are missing {missing}")
    governed_slug_keys: set[tuple[str, str]] = set()
    governed_slug_routes: set[str] = set()
    for row in required_acquisitions:
        if not isinstance(row, dict):
            continue
        entity_id = row.get("entity_id")
        entity = entities.get(entity_id)
        slug = row.get("public_slug")
        route = f"/museum/network/acquisitions/{slug}" if isinstance(slug, str) else None
        if isinstance(slug, str):
            key = ("CURATED_ACQUISITION", slug)
            if key in governed_slug_keys:
                issues.append(f"public entity inventory: duplicate governed slug {slug!r} within CURATED_ACQUISITION")
            governed_slug_keys.add(key)
        if isinstance(route, str):
            if route in governed_slug_routes:
                issues.append(f"public entity inventory: duplicate governed route {route}")
            governed_slug_routes.add(route)
        if entity is not None and (
            entity[1].get("preferred_label") != row.get("preferred_label")
            or entity[1].get("public_slug") != slug
            or entity[1].get("canonical_route") != route
        ):
            issues.append(f"{display_path(entity[0])}: Curated Acquisition identity does not match governed inventory for {entity_id}")
    slug_rows = identity_inventory.get("public_slug_inventory", []) if isinstance(identity_inventory, dict) else []
    slug_inventory_keys = set(governed_slug_keys)
    slug_inventory_routes = set(governed_slug_routes)
    governed_slug_entity_ids = set(required_acquisition_ids)
    for row in slug_rows:
        if not isinstance(row, dict):
            issues.append("public entity inventory: public_slug_inventory entries must be objects")
            continue
        entity_id = row.get("entity_id")
        entity_type = row.get("entity_type")
        slug = row.get("public_slug")
        route = row.get("canonical_route")
        if isinstance(entity_id, str):
            governed_slug_entity_ids.add(entity_id)
        entity = entities.get(entity_id) if isinstance(entity_id, str) else None
        key = (str(entity_type), str(slug))
        if key in slug_inventory_keys:
            issues.append(f"public entity inventory: duplicate governed slug {slug!r} within {entity_type}")
        slug_inventory_keys.add(key)
        if isinstance(route, str) and route in slug_inventory_routes:
            issues.append(f"public entity inventory: duplicate governed route {route}")
        if isinstance(route, str):
            slug_inventory_routes.add(route)
        if entity is None:
            issues.append(f"public entity inventory: governed slug entity {entity_id!r} is not present in the candidate graph")
            continue
        actual = entity[1]
        if actual.get("entity_type") != entity_type or actual.get("preferred_label") != row.get("preferred_label") or actual.get("public_slug") != slug or actual.get("canonical_route") != route:
            issues.append(f"{display_path(entity[0])}: public slug inventory mismatch for {entity_id}")
        if entity_type == "ARTIST" and isinstance(slug, str) and slug.startswith(("keys-and-gates-artist-", "conflict-at-its-edges-artist-")):
            issues.append(f"{display_path(entity[0])}: Artist public_slug must be a stable name/handle, not a generated placeholder")
    actual_slug_entity_ids = {
        entity_id
        for entity_id, (_path, payload) in entities.items()
        if isinstance(payload.get("public_slug"), str) and payload.get("entity_type") != "WORK"
    }
    if actual_slug_entity_ids != governed_slug_entity_ids:
        issues.append(
            "public entity inventory: governed slug rows do not equal generated slug-bearing entities; "
            f"missing={sorted(governed_slug_entity_ids - actual_slug_entity_ids)}, "
            f"unexpected={sorted(actual_slug_entity_ids - governed_slug_entity_ids)}"
        )
    acquisition_aliases = identity_inventory.get("acquisition_aliases", []) if isinstance(identity_inventory, dict) else []
    alias_values: set[str] = set()
    for row in acquisition_aliases:
        if not isinstance(row, dict):
            continue
        alias = row.get("alias")
        canonical_id = row.get("canonical_entity_id")
        if isinstance(alias, str):
            if alias in alias_values:
                issues.append(f"public entity inventory: duplicate acquisition alias {alias}")
            alias_values.add(alias)
        if canonical_id not in entities:
            issues.append(f"public entity inventory: acquisition alias {alias!r} points to unpublished {canonical_id!r}")
        if isinstance(alias, str) and re.fullmatch(r"6529NM-AP-01-OUT-\d{3}", alias) and canonical_id in required_acquisition_ids:
            issues.append(f"public entity inventory: Work outcome alias {alias} must not identify a Curated Acquisition")
    source_aliases = identity_inventory.get("source_aliases", []) if isinstance(identity_inventory, dict) else []
    source_alias_keys: set[tuple[str, str]] = set()
    for row in source_aliases:
        if not isinstance(row, dict):
            issues.append("public entity inventory: source_aliases entries must be objects")
            continue
        alias = row.get("alias")
        alias_type = row.get("alias_type")
        canonical_id = row.get("canonical_entity_id")
        key = (str(alias), str(alias_type))
        if key in source_alias_keys:
            issues.append(f"public entity inventory: duplicate typed source alias {alias!r}/{alias_type!r}")
        source_alias_keys.add(key)
        entity = entities.get(canonical_id) if isinstance(canonical_id, str) else None
        if entity is None:
            issues.append(f"public entity inventory: typed source alias {alias!r}/{alias_type!r} points to unpublished {canonical_id!r}")
            continue
        entity_type = entity[1].get("entity_type")
        if alias_type == "source_program" and entity_type != "ACQUISITION_PROGRAM":
            issues.append(f"public entity inventory: source_program alias {alias!r} must resolve to an Acquisition Program")
        if alias_type == "source_acquisition_context" and entity_type != "CURATED_ACQUISITION":
            issues.append(f"public entity inventory: source_acquisition_context alias {alias!r} must resolve to a Curated Acquisition")
        if row.get("route_target") and entity_type not in PUBLIC_CANONICAL_PAGE_TYPES:
            issues.append(f"public entity inventory: route-target source alias {alias!r} must resolve to a canonical-page entity")
        if alias == "6529NM-AP-01" and alias_type == "source_acquisition_context" and canonical_id != "6529NM-CA-2026-002":
            issues.append("public entity inventory: 6529NM-AP-01 acquisition context must resolve to Keys and Gates CA-002")
        if alias == "6529NM-AP-01" and alias_type == "source_program" and canonical_id != "6529NM-AP-ENT-0002":
            issues.append("public entity inventory: 6529NM-AP-01 source program must resolve to AP-ENT-0002")
    route_aliases = identity_inventory.get("route_aliases", []) if isinstance(identity_inventory, dict) else []
    legacy_routes: set[str] = set()
    for row in route_aliases:
        if not isinstance(row, dict):
            continue
        legacy = row.get("legacy_route")
        canonical = row.get("canonical_route")
        canonical_id = row.get("canonical_entity_id")
        if isinstance(legacy, str):
            if legacy in legacy_routes:
                issues.append(f"public entity inventory: duplicate legacy route {legacy}")
            legacy_routes.add(legacy)
        entity = entities.get(canonical_id) if isinstance(canonical_id, str) else None
        if entity is None:
            issues.append(f"public entity inventory: route alias {legacy!r} points to unpublished {canonical_id!r}")
        elif entity[1].get("canonical_route") != canonical:
            issues.append(f"public entity inventory: route alias {legacy!r} does not target the entity's exact canonical route")
        if legacy == canonical:
            issues.append(f"public entity inventory: route alias {legacy!r} must differ from its canonical route")
    identity_bindings = identity_inventory.get("identity_bindings", {}) if isinstance(identity_inventory, dict) else {}
    retired_ids: set[str] = set()
    retired_rows = identity_inventory.get("retired_identity_ids", []) if isinstance(identity_inventory, dict) else []
    if not isinstance(retired_rows, list):
        issues.append("public entity inventory: retired_identity_ids must be a list")
        retired_rows = []
    for row in retired_rows:
        if not isinstance(row, dict):
            issues.append("public entity inventory: retired identity tombstones must be objects")
            continue
        retired_id = row.get("entity_id")
        retired_type = row.get("entity_type")
        if not isinstance(retired_id, str) or not isinstance(retired_type, str):
            issues.append("public entity inventory: retired identity tombstone requires entity_id and entity_type")
            continue
        if retired_id in retired_ids:
            issues.append(f"public entity inventory: duplicate retired identity {retired_id}")
        retired_ids.add(retired_id)
        pattern = public_entity_id_pattern(retired_type, identity_inventory)
        if isinstance(pattern, str) and not re.fullmatch(pattern, retired_id):
            issues.append(f"public entity inventory: retired identity {retired_id} violates the {retired_type} pattern")
        if retired_id in entities:
            issues.append(f"{display_path(entities[retired_id][0])}: retired identity {retired_id} must not be an active PUBLIC_ENTITY")
        superseded_by = row.get("superseded_by")
        if isinstance(superseded_by, str) and superseded_by not in entities:
            issues.append(f"public entity inventory: retired identity {retired_id} points to unpublished superseding identity {superseded_by}")
    if not isinstance(identity_bindings, dict):
        issues.append("public entity inventory: identity_bindings must be an object")
    else:
        binding_types = set(identity_bindings)
        expected_binding_types = set(PUBLIC_IDENTITY_BINDING_TYPES)
        if binding_types != expected_binding_types:
            issues.append(
                "public entity inventory: identity binding categories must be closed; "
                f"missing={sorted(expected_binding_types - binding_types)}, "
                f"unexpected={sorted(binding_types - expected_binding_types)}"
            )
        patterns = identity_inventory.get("entity_id_patterns", {})
        pattern_types = set(patterns) if isinstance(patterns, dict) else set()
        if pattern_types != expected_binding_types:
            issues.append(
                "public entity inventory: identity pattern categories must equal binding categories; "
                f"missing={sorted(expected_binding_types - pattern_types)}, "
                f"unexpected={sorted(pattern_types - expected_binding_types)}"
            )
        for binding_type in PUBLIC_IDENTITY_BINDING_ENTITY_TYPES:
            rows = identity_bindings.get(binding_type)
            if not isinstance(rows, list) or not rows:
                issues.append(f"public entity inventory: missing {binding_type} identity bindings")
                continue
            seen_sources: set[str] = set()
            seen_ids: set[str] = set()
            pattern = identity_inventory.get("entity_id_patterns", {}).get(binding_type)
            for row in rows:
                if not isinstance(row, dict):
                    issues.append(f"public entity inventory: {binding_type} identity binding must be an object")
                    continue
                source_key = row.get("source_key")
                entity_id = row.get("entity_id")
                if not isinstance(source_key, str) or not source_key:
                    issues.append(f"public entity inventory: {binding_type} identity binding has no source_key")
                elif source_key in seen_sources:
                    issues.append(f"public entity inventory: duplicate {binding_type} identity source_key {source_key!r}")
                else:
                    seen_sources.add(source_key)
                if not isinstance(entity_id, str) or not entity_id:
                    issues.append(f"public entity inventory: {binding_type} identity binding has no entity_id")
                    continue
                if entity_id in retired_ids:
                    issues.append(f"public entity inventory: active {binding_type} binding reuses retired identity {entity_id}")
                if entity_id in seen_ids:
                    issues.append(f"public entity inventory: duplicate {binding_type} identity entity_id {entity_id!r}")
                seen_ids.add(entity_id)
                if isinstance(pattern, str) and not re.fullmatch(pattern, entity_id):
                    issues.append(f"public entity inventory: {binding_type} identity binding {entity_id!r} violates its ID pattern")
                entity = entities.get(entity_id)
                if entity is None:
                    issues.append(f"public entity inventory: {binding_type} identity binding {entity_id!r} is not present in the candidate graph")
                elif entity[1].get("entity_type") != binding_type:
                    issues.append(f"{display_path(entity[0])}: identity binding type {binding_type} does not match entity type {entity[1].get('entity_type')}")
            actual_ids = {entity_id for entity_id, (_path, payload) in entities.items() if payload.get("entity_type") == binding_type}
            if actual_ids != seen_ids:
                issues.append(f"public entity inventory: {binding_type} identity bindings do not equal generated entities; missing={sorted(seen_ids - actual_ids)}, unexpected={sorted(actual_ids - seen_ids)}")
        observation_bindings = identity_bindings.get("WORK_LIFECYCLE_OBSERVATION")
        if not isinstance(observation_bindings, list) or not observation_bindings:
            issues.append("public entity inventory: missing WORK_LIFECYCLE_OBSERVATION identity bindings")
        else:
            seen_observation_sources: set[str] = set()
            seen_observation_ids: set[str] = set()
            pattern = identity_inventory.get("entity_id_patterns", {}).get("WORK_LIFECYCLE_OBSERVATION")
            for row in observation_bindings:
                if not isinstance(row, dict):
                    issues.append("public entity inventory: WORK_LIFECYCLE_OBSERVATION binding must be an object")
                    continue
                source_key = row.get("source_key")
                observation_id = row.get("entity_id")
                if not isinstance(source_key, str) or not source_key:
                    issues.append("public entity inventory: WORK_LIFECYCLE_OBSERVATION binding has no source_key")
                elif source_key in seen_observation_sources:
                    issues.append(f"public entity inventory: duplicate WORK_LIFECYCLE_OBSERVATION source_key {source_key!r}")
                else:
                    seen_observation_sources.add(source_key)
                if not isinstance(observation_id, str) or not observation_id:
                    issues.append("public entity inventory: WORK_LIFECYCLE_OBSERVATION binding has no entity_id")
                else:
                    if observation_id in seen_observation_ids:
                        issues.append(f"public entity inventory: duplicate WORK_LIFECYCLE_OBSERVATION entity_id {observation_id!r}")
                    seen_observation_ids.add(observation_id)
                    if isinstance(pattern, str) and not re.fullmatch(pattern, observation_id):
                        issues.append(f"public entity inventory: WORK_LIFECYCLE_OBSERVATION identity {observation_id!r} violates its ID pattern")
            actual_observation_ids = {
                observation.get("observation_id")
                for _entity_id, (_path, payload) in entities.items()
                if payload.get("entity_type") == "WORK"
                for observation in payload.get("profile", {}).get("lifecycle_observations", [])
                if isinstance(observation, dict) and isinstance(observation.get("observation_id"), str)
            }
            if actual_observation_ids != seen_observation_ids:
                issues.append(f"public entity inventory: WORK_LIFECYCLE_OBSERVATION bindings do not equal generated observations; missing={sorted(seen_observation_ids - actual_observation_ids)}, unexpected={sorted(actual_observation_ids - seen_observation_ids)}")
    for entity_id, (path, payload) in entities.items():
        pattern = public_entity_id_pattern(payload.get("entity_type"), identity_inventory)
        if isinstance(pattern, str) and not re.fullmatch(pattern, entity_id):
            issues.append(f"{display_path(path)}: {payload.get('entity_type')} entity_id {entity_id!r} violates governed identity pattern {pattern}")
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
    try:
        identity_inventory = load_public_identity_inventory(schema_root)
        inventory_schema = load_json(schema_root / "schemas/public-entity-identity-inventory.schema.json")
        inventory_errors = sorted(
            (leaf for error in validator_for(inventory_schema, schema_store).iter_errors(identity_inventory) for leaf in schema_leaf_errors(error)),
            key=lambda error: list(error.absolute_path),
        )
        issues.extend(f"schemas/{PUBLIC_IDENTITY_INVENTORY_FILENAME}: {format_error(error)}" for error in inventory_errors)
    except (OSError, json.JSONDecodeError, DuplicateJsonKeyError) as exc:
        identity_inventory = {}
        issues.append(f"schemas/{PUBLIC_IDENTITY_INVENTORY_FILENAME}: unavailable: {exc}")
    try:
        route_inventory = load_json(schema_root / "schemas/public-route-compatibility.json")
        route_schema = load_json(schema_root / "schemas/public-route-compatibility.schema.json")
        route_errors = sorted(
            (leaf for error in validator_for(route_schema, schema_store).iter_errors(route_inventory) for leaf in schema_leaf_errors(error)),
            key=lambda error: list(error.absolute_path),
        )
        issues.extend(f"schemas/public-route-compatibility.json: {format_error(error)}" for error in route_errors)
    except (OSError, json.JSONDecodeError, DuplicateJsonKeyError) as exc:
        route_inventory = {}
        issues.append(f"schemas/public-route-compatibility.json: unavailable: {exc}")
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
    record_aliases: dict[str, set[Path]] = {}

    def register_identifier(identifier: Any, path: Path) -> None:
        if not isinstance(identifier, str):
            return
        prior = record_ids.get(identifier)
        if prior is None:
            record_ids[identifier] = path
        elif prior != path:
            relative_path = path.relative_to(root).as_posix()
            issues.append(f"{relative_path}: duplicate record identifier {identifier}; first seen at {prior.relative_to(root).as_posix()}")

    def register_aliases(value: dict[str, Any], path: Path) -> None:
        alias_keys = {
            "entity_id", "relation_id", "program_id", "proposal_id", "object_id",
            "accession_lot_id", "accession_number", "outcome_id", "publication_id", "accession_id",
            "observation_id", "amendment_id", "candidate_object_id",
        }

        def visit_nested(item: Any) -> None:
            if isinstance(item, dict):
                for key, identifier in item.items():
                    if key in alias_keys and isinstance(identifier, str):
                        record_aliases.setdefault(identifier, set()).add(path)
                    visit_nested(identifier)
            elif isinstance(item, list):
                for child in item:
                    visit_nested(child)

        visit_nested(value)

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
            register_identifier(record.get("record_id"), path)
            register_aliases(record, path)
            if record.get("record_set_id") == "6529NM-GOV-REGISTER" and isinstance(record.get("records"), list):
                for row in record["records"]:
                    embedded_id = row.get("decision_id") if isinstance(row, dict) else None
                    if not isinstance(embedded_id, str):
                        continue
                    if embedded_id in record_ids:
                        issues.append(f"{relative}: duplicate embedded decision_id {embedded_id}; first seen at {record_ids[embedded_id].relative_to(root).as_posix()}")
                    else:
                        record_ids[embedded_id] = path
            records.append((path, record, None))
            continue

        register_identifier(payload.get("record_id"), path)
        register_aliases(payload, path)
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
            issues.extend(f"{relative}: {message}" for message in validate_semantics(record, vocabularies, identity_inventory, root))
        records.append((path, record, payload))
    aliases = {}
    has_public_entities = any(
        isinstance(payload, dict) and payload.get("record_type") == PUBLIC_ENTITY_TYPE
        for _path, _record, payload in records
    )
    if has_public_entities:
        for row in identity_inventory.get("work_aliases", []) if isinstance(identity_inventory, dict) else []:
            if isinstance(row, dict) and isinstance(row.get("alias"), str) and isinstance(row.get("canonical_entity_id"), str):
                aliases[row["alias"]] = row["canonical_entity_id"]
        for alias, canonical_id in aliases.items():
            canonical_path = record_ids.get(canonical_id)
            if canonical_path is None:
                issues.append(f"public identity inventory: canonical Work {canonical_id} is not present for alias {alias}")
                continue
            record_aliases.setdefault(alias, set()).add(canonical_path)
    for path, record, payload in records:
        if not isinstance(payload, dict):
            continue
        relative = path.relative_to(root).as_posix()
        for reference in iter_reference_values(payload):
            if reference not in record_ids and reference not in record_aliases:
                issues.append(f"{relative}: unresolved record reference {reference}")
        for field in ("references", "governing_references"):
            direct_references = payload.get(field, [])
            if isinstance(direct_references, list) and payload.get("record_id") in direct_references:
                issues.append(f"{relative}: {field} must not point to the record itself")
        supersedes = payload.get("supersedes")
        if supersedes:
            if supersedes == payload.get("record_id"):
                issues.append(f"{relative}: supersedes must not point to itself")
            else:
                superseded_path = record_ids.get(supersedes)
                if superseded_path:
                    superseded = load_json(superseded_path)
                    supersession_pair = (payload.get("record_type"), superseded.get("payload", {}).get("record_type"))
                    allowed_cross_type = supersession_pair == ("MEDIA_DESCRIPTION_AMENDMENT", "WAVE_PUBLICATION_OBSERVATION")
                    if superseded.get("payload", {}).get("record_type") != payload.get("record_type") and not allowed_cross_type:
                        issues.append(f"{relative}: supersedes must point to the same record_type")
    issues.extend(validate_public_graph(records, vocabularies, identity_inventory, root))
    public_entities = {
        payload.get("entity_id"): payload
        for _path, _record, payload in records
        if isinstance(payload, dict)
        and payload.get("record_type") == PUBLIC_ENTITY_TYPE
        and isinstance(payload.get("entity_id"), str)
    }
    if public_entities and isinstance(route_inventory, dict) and route_inventory:
        compatibility_keys: set[tuple[str, str, str | None]] = set()
        seen_legacy_routes: set[str] = set()
        for entry in route_inventory.get("entries", []):
            if not isinstance(entry, dict):
                continue
            legacy = entry.get("legacy_route")
            if legacy in seen_legacy_routes:
                issues.append(f"public route compatibility: duplicate legacy route {legacy}")
            seen_legacy_routes.add(legacy)
            compatibility_keys.add((legacy, entry.get("canonical_route"), entry.get("target_entity_id")))
            if entry.get("target_kind") == "entity":
                target_id = entry.get("target_entity_id")
                target = public_entities.get(target_id)
                if target is None:
                    issues.append(f"public route compatibility: {legacy!r} targets unpublished entity {target_id!r}")
                elif target.get("canonical_route") != entry.get("canonical_route"):
                    issues.append(f"public route compatibility: {legacy!r} does not equal the target entity's exact canonical route")
            if entry.get("legacy_route") == "/museum/network/programs/6529NM-AP-01" and entry.get("target_entity_id") != "6529NM-AP-ENT-0002":
                issues.append("public route compatibility: the Keys and Gates program route must never resolve to CA-002")
            if entry.get("canonical_route") == "/museum/network/acquisitions/keys-and-gates":
                issues.append("public route compatibility: a program route cannot target the Keys and Gates acquisition")
        if route_inventory.get("include_governed_route_aliases") is True:
            expected_expansion_keys = _expected_route_expansion_keys(
                root, identity_inventory, public_entities, route_inventory
            )
            for row in identity_inventory.get("route_aliases", []) if isinstance(identity_inventory, dict) else []:
                if not isinstance(row, dict):
                    continue
                key = (row.get("legacy_route"), row.get("canonical_route"), row.get("canonical_entity_id"))
                if key not in compatibility_keys and key not in expected_expansion_keys:
                    issues.append(f"public route compatibility: governed route alias is not covered by the closed compatibility contract: {row.get('legacy_route')}")
            explicit_keys = set(compatibility_keys)
            fixed_route_keys = {
                key for key in explicit_keys
                if key[0] in {
                    "/museum/network/collections",
                    "/museum/network/accessions",
                    "/museum/network/programs",
                    "/museum/network/methodology",
                    "/museum/network/stories",
                    "/museum/network/governance",
                }
            }
            expected_keys = fixed_route_keys | expected_expansion_keys
            # Every explicit entity/dynamic compatibility route must come from
            # a governed identity alias or one of the closed expansions; the
            # expansion itself is the complete runtime contract and need not
            # duplicate hundreds of concrete entries in this control file.
            unexpected_expansions = sorted(explicit_keys - expected_keys)
            if unexpected_expansions:
                issues.append(f"public route compatibility: ungoverned dynamic routes are present {unexpected_expansions[:8]}")
            compatibility_keys = expected_keys
            for expansion in route_inventory.get("expansions", []):
                if not isinstance(expansion, dict) or not expansion.get("canonical_route_from_entity"):
                    continue
                for row in _route_source_rows(root, identity_inventory, expansion):
                    if expansion.get("source_inventory") in {"work_aliases", "acquisition_aliases"} and expansion.get("alias_kind") != "all" and row.get("alias_kind") != expansion.get("alias_kind"):
                        continue
                    if expansion.get("source_inventory") == "source_aliases" and expansion.get("alias_kind") != "all" and row.get("alias_type") != expansion.get("alias_kind"):
                        continue
                    target_id = row.get("canonical_entity_id")
                    target = public_entities.get(target_id)
                    if target is None:
                        issues.append(f"public route compatibility: expansion target {target_id!r} is unpublished")
                    elif expansion.get("only_permanent_collection") and target.get("profile", {}).get("collection_membership", {}).get("status") != "permanent_collection":
                        issues.append(f"public route compatibility: collection alias expansion may only target permanent Collection Work {target_id}")
            if not any(route.startswith("/museum/network/collection/") for route, _canonical, _target in compatibility_keys):
                issues.append("public route compatibility: Casey Collection object expansion is missing")
            for route, _canonical, target in compatibility_keys:
                if route.startswith("/museum/network/collection/"):
                    target_payload = public_entities.get(target)
                    if target_payload is None or target_payload.get("entity_type") != "WORK" or target_payload.get("profile", {}).get("collection_membership", {}).get("status") != "permanent_collection":
                        issues.append(f"public route compatibility: /collection alias is not relation-gated to a permanent Collection Work: {route}")
            required_frontend_routes = {
                "/museum/network/collection",
                "/museum/network/artists",
                "/museum/network/organizations",
                "/museum/network/projects",
                "/museum/network/works",
                "/museum/network/acquisitions",
                "/museum/network/acquisition-programs",
                "/museum/network/research",
                "/museum/network/about",
            }
            if not required_frontend_routes.issubset(set(route_inventory.get("frontend_route_set", []))):
                issues.append("public route compatibility: frontend_route_set omits a canonical index route")
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
