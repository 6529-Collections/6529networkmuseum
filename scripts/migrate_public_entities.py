#!/usr/bin/env python3
"""Build the deterministic PUBLIC_ENTITY/PUBLIC_RELATION publication projection."""

from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import os
import re
import sys
import tempfile
from pathlib import Path
from typing import Any

from Crypto.Hash import keccak

from canonical import canonicalize

ROOT = Path(__file__).resolve().parent.parent
ENTITIES_DIR = ROOT / "records" / "entities"
RELATIONS_DIR = ROOT / "records" / "relations"
VOCAB_PATH = ROOT / "schemas" / "controlled-vocabularies.json"
IDENTITY_INVENTORY_PATH = ROOT / "schemas" / "public-entity-identity-inventory.json"
RELATION_IDENTITY_INVENTORY_PATH = ROOT / "schemas" / "public-relation-identity-inventory.json"
CONSTRUCTOR_ID = "codex-task:019fe8c0-306f-73c1-822c-f997dda66b2c"
GENERATED_AT = "2026-08-09T23:04:32Z"
CASEY_AT = "2026-08-02T06:30:00Z"
CASEY_MEDIA_AT = "2026-08-09T23:04:32Z"
KEYS_AT = "2026-08-01T15:03:35Z"
KEYS_PUBLICATION_AT = "2026-08-08T00:00:00Z"
MAGNUM_PUBLICATION_AT = "2026-08-09T00:00:00Z"
KEYS_MEDIA_WITHDRAWAL_AT = "2026-08-09T00:32:21Z"
PROPOSAL_AT = "2026-08-06T13:19:30.726Z"
MAGNUM_CHAIN_AT = "2026-08-05T17:46:53.817Z"
WINNER_AT = "2026-08-08T10:15:02.0167151Z"
DIRECT_VISUAL_AT = "2026-08-08T14:25:44Z"
WINNER_OBSERVATION_ID = "6529NM-WAVE-OBS-2026-08-08-001"
WINNER_SOURCE_PATH = "records/proposed-gifts/6529NM-PG-2026-001/wave-status-observation-2026-08-08.json"
WINNER_SOURCE_URL = "https://6529.io/waves/5f207393-5418-4a75-8738-e40edb44a94d?drop=002bfa4f-8416-48bf-b35e-38f354e9a9f0"
WAVE_PUBLICATION_OBSERVATION_ID = "6529NM-WAVE-PUB-OBS-2026-08-08-001"
WAVE_PUBLICATION_OBSERVATION_PATH = "records/proposed-gifts/6529NM-PG-2026-001/wave-publication-observation-2026-08-08.json"
MEDIA_DESCRIPTION_AMENDMENT_ID = "6529NM-MEDIA-DESC-AMD-2026-08-08-001"
MEDIA_DESCRIPTION_AMENDMENT_PATH = "records/proposed-gifts/6529NM-PG-2026-001/media-description-amendment-2026-08-08.json"
CASEY_MEDIA_AMENDMENT_ID = "6529NM-MEDIA-PRES-AMD-2026-08-09-001"
CASEY_MEDIA_AMENDMENT_PATH = "records/accessions/6529NM.2026.001/media-presentation-amendment-2026-08-09.json"
MAGNUM_SCHOLARSHIP_ROOT = "records/proposed-gifts/6529NM-PG-2026-001/public/scholarship"
MAGNUM_PUBLICATION_RECORD_PATH = f"{MAGNUM_SCHOLARSHIP_ROOT}/publication-record.md"
MAGNUM_WORK_PUBLICATION_PATHS = {
    "6529NM-PG-2026-001.OBJ-001": f"{MAGNUM_SCHOLARSHIP_ROOT}/works/01-david-seymour-127.md",
    "6529NM-PG-2026-001.OBJ-002": f"{MAGNUM_SCHOLARSHIP_ROOT}/works/02-larry-towell-145.md",
    "6529NM-PG-2026-001.OBJ-003": f"{MAGNUM_SCHOLARSHIP_ROOT}/works/03-micha-bar-am-97.md",
    "6529NM-PG-2026-001.OBJ-004": f"{MAGNUM_SCHOLARSHIP_ROOT}/works/04-moises-saman-44.md",
    "6529NM-PG-2026-001.OBJ-005": f"{MAGNUM_SCHOLARSHIP_ROOT}/works/05-lorenzo-meloni-104.md",
}
MAGNUM_PUBLICATION_COMPONENT_PATHS = (
    f"{MAGNUM_SCHOLARSHIP_ROOT}/artists/david-seymour.md",
    f"{MAGNUM_SCHOLARSHIP_ROOT}/artists/larry-towell.md",
    f"{MAGNUM_SCHOLARSHIP_ROOT}/artists/lorenzo-meloni.md",
    f"{MAGNUM_SCHOLARSHIP_ROOT}/artists/micha-bar-am.md",
    f"{MAGNUM_SCHOLARSHIP_ROOT}/artists/moises-saman.md",
    f"{MAGNUM_SCHOLARSHIP_ROOT}/dossiers/caption-evidence.md",
    f"{MAGNUM_SCHOLARSHIP_ROOT}/dossiers/chronologies.md",
    f"{MAGNUM_SCHOLARSHIP_ROOT}/dossiers/media-plan.md",
    f"{MAGNUM_SCHOLARSHIP_ROOT}/dossiers/rights-technical-provenance.md",
    f"{MAGNUM_SCHOLARSHIP_ROOT}/dossiers/source-and-rights-record.md",
    f"{MAGNUM_SCHOLARSHIP_ROOT}/entities/conflict-at-its-edges.md",
    f"{MAGNUM_SCHOLARSHIP_ROOT}/entities/magnum-photos-75.md",
    f"{MAGNUM_SCHOLARSHIP_ROOT}/entities/magnum-photos.md",
    f"{MAGNUM_SCHOLARSHIP_ROOT}/essays/acquisition-narrative.md",
    f"{MAGNUM_SCHOLARSHIP_ROOT}/essays/conflict-at-its-edges.md",
    f"{MAGNUM_SCHOLARSHIP_ROOT}/sources/source-register.md",
    *MAGNUM_WORK_PUBLICATION_PATHS.values(),
)
MAGNUM_PUBLIC_EVIDENCE_LOCATORS = {
    "6529NM-PG-2026-001": WINNER_SOURCE_URL,
    "records/proposed-gifts/6529NM-PG-2026-001/proposal.json": WINNER_SOURCE_URL,
    "records/proposed-gifts/6529NM-PG-2026-001/wave-storm.json": WINNER_SOURCE_URL,
    WINNER_OBSERVATION_ID: WINNER_SOURCE_URL,
    WINNER_SOURCE_PATH: WINNER_SOURCE_URL,
    WAVE_PUBLICATION_OBSERVATION_ID: WINNER_SOURCE_URL,
    WAVE_PUBLICATION_OBSERVATION_PATH: WINNER_SOURCE_URL,
    MEDIA_DESCRIPTION_AMENDMENT_ID: MAGNUM_WORK_PUBLICATION_PATHS["6529NM-PG-2026-001.OBJ-003"],
    MEDIA_DESCRIPTION_AMENDMENT_PATH: MAGNUM_WORK_PUBLICATION_PATHS["6529NM-PG-2026-001.OBJ-003"],
    **MAGNUM_WORK_PUBLICATION_PATHS,
}
JCS_ID = "0x886c7c89c308c459ca8a626e0ef36a5ea9f4c7a7b56aaf86c71a2ddf3b4f9044"
ZERO32 = "0x" + "0" * 64
GITHUB = "https://github.com/6529-Collections/6529networkmuseum/blob/main/"
LOGICAL_RECORD_BASE = "https://6529networkmuseum.org/"
PUBLIC_ENTITY_SCHEMA = "0xd8aef6592fe156c4c3c10e59de540f5cdf8b130eedca322e0e22b30764bee1a9"
PUBLIC_RELATION_SCHEMA = "0xaa76f1b93e01ae7a1cff2717b0c814df772fd26d3997a47847a1887cba6756de"
WAVE_STATUS_SCHEMA = "0xfe0b5244859ffb994766ff3aeace88f12961e07bb97941c647044327737c9be1"
TYPED_REFERENCE_REGISTRY_ID = "PUBLIC_TYPED_REFERENCE_REGISTRY_V1"
IDENTITY_BINDING_ENTITY_TYPES = (
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
IDENTITY_BINDING_AUXILIARY_TYPES = ("WORK_LIFECYCLE_OBSERVATION",)
IDENTITY_BINDING_TYPES = (*IDENTITY_BINDING_ENTITY_TYPES, *IDENTITY_BINDING_AUXILIARY_TYPES)


class DuplicateJsonKeyError(ValueError):
    """Raised when a source JSON object repeats a key."""


def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateJsonKeyError(f"duplicate JSON key: {key!r}")
        result[key] = value
    return result


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle, object_pairs_hook=reject_duplicate_keys)


def identity_binding_indexes(identity_inventory: dict[str, Any]) -> dict[str, dict[str, str]]:
    """Load governed source-key → canonical-ID bindings and fail closed.

    Source order is not an identity source. Every public identity is assigned in
    the versioned inventory, and missing categories plus duplicate keys or
    canonical IDs are rejected before generation begins.
    """

    raw_bindings = identity_inventory.get("identity_bindings")
    if not isinstance(raw_bindings, dict):
        raise ValueError("public identity inventory is missing identity_bindings")
    indexes: dict[str, dict[str, str]] = {}
    patterns = identity_inventory.get("entity_id_patterns", {})
    if not isinstance(patterns, dict) or set(patterns) != set(IDENTITY_BINDING_TYPES):
        raise ValueError("public identity patterns must exactly cover every governed identity binding type")
    if set(raw_bindings) != set(IDENTITY_BINDING_TYPES):
        raise ValueError("public identity bindings must exactly cover every governed identity binding type")
    retired_rows = identity_inventory.get("retired_identity_ids", [])
    if not isinstance(retired_rows, list):
        raise ValueError("public identity inventory retired_identity_ids must be a list")
    retired_ids: set[str] = set()
    for row in retired_rows:
        if not isinstance(row, dict) or not isinstance(row.get("entity_id"), str) or not isinstance(row.get("entity_type"), str):
            raise ValueError("invalid retired public identity tombstone")
        retired_id = row["entity_id"]
        if retired_id in retired_ids:
            raise ValueError(f"duplicate retired public identity {retired_id!r}")
        retired_ids.add(retired_id)
    for entity_type in IDENTITY_BINDING_TYPES:
        rows = raw_bindings.get(entity_type)
        if not isinstance(rows, list) or not rows:
            raise ValueError(f"public identity inventory has no {entity_type} identity bindings")
        by_source: dict[str, str] = {}
        seen_ids: set[str] = set()
        pattern = patterns.get(entity_type) if isinstance(patterns, dict) else None
        for row in rows:
            if not isinstance(row, dict) or not isinstance(row.get("source_key"), str) or not isinstance(row.get("entity_id"), str):
                raise ValueError(f"invalid {entity_type} identity binding")
            source_key = row["source_key"]
            entity_id = row["entity_id"]
            if source_key in by_source:
                raise ValueError(f"duplicate {entity_type} identity binding source_key {source_key!r}")
            if entity_id in seen_ids:
                raise ValueError(f"duplicate {entity_type} identity binding entity_id {entity_id!r}")
            if entity_id in retired_ids:
                raise ValueError(f"{entity_type} identity binding reuses retired entity_id {entity_id!r}")
            if isinstance(pattern, str) and not re.fullmatch(pattern, entity_id):
                raise ValueError(f"{entity_type} identity binding {entity_id!r} violates governed pattern")
            by_source[source_key] = entity_id
            seen_ids.add(entity_id)
        indexes[entity_type] = by_source
    return indexes


def resolve_identity_ids(identity_inventory: dict[str, Any], entity_type: str, source_keys: list[str]) -> list[str]:
    """Resolve source keys through the governed fixed identity inventory."""

    index = identity_binding_indexes(identity_inventory).get(entity_type)
    if index is None:
        raise ValueError(f"unsupported identity binding type {entity_type!r}")
    missing = [source_key for source_key in source_keys if source_key not in index]
    if missing:
        raise ValueError(f"missing {entity_type} identity bindings for {sorted(set(missing))}")
    return [index[source_key] for source_key in source_keys]


def semantic_relation_key(relation_type: str, source: str, target: str, qualifier: dict[str, Any]) -> str:
    """Return the governed relation identity independent of emission order.

    Qualifiers are assertion attributes, not identity for this closed graph;
    a later display-order, status, media-context, or role amendment therefore
    preserves the relation record ID.
    """

    return "|".join((relation_type, source, target))


def relation_binding_indexes(identity_inventory: dict[str, Any]) -> dict[str, str]:
    """Load active semantic relation keys and preserve retired identities."""

    rows = identity_inventory.get("relation_bindings")
    if not isinstance(rows, list) or not rows:
        raise ValueError("public relation identity inventory is missing relation_bindings")
    by_key: dict[str, str] = {}
    seen_ids: set[str] = set()
    for row in rows:
        if not isinstance(row, dict) or not isinstance(row.get("source_key"), str) or not isinstance(row.get("relation_id"), str):
            raise ValueError("invalid public relation identity binding")
        key = row["source_key"]
        relation_id = row["relation_id"]
        if key in by_key:
            raise ValueError(f"duplicate relation identity source_key {key!r}")
        if relation_id in seen_ids:
            raise ValueError(f"duplicate relation identity relation_id {relation_id!r}")
        if not re.fullmatch(r"6529NM-REL-[0-9]{4}", relation_id):
            raise ValueError(f"relation identity {relation_id!r} violates the governed ID pattern")
        by_key[key] = relation_id
        seen_ids.add(relation_id)
    retired_rows = identity_inventory.get("retired_relation_ids", [])
    if not isinstance(retired_rows, list):
        raise ValueError("public relation identity inventory retired_relation_ids must be a list")
    seen_retired_keys: set[str] = set()
    for row in retired_rows:
        if not isinstance(row, dict) or not isinstance(row.get("source_key"), str) or not isinstance(row.get("relation_id"), str):
            raise ValueError("invalid retired public relation identity tombstone")
        key = row["source_key"]
        relation_id = row["relation_id"]
        if key in by_key or key in seen_retired_keys:
            raise ValueError(f"retired public relation source_key {key!r} is duplicated or active")
        if relation_id in seen_ids:
            raise ValueError(f"retired public relation ID {relation_id!r} is reused by an active binding")
        if not re.fullmatch(r"6529NM-REL-[0-9]{4}", relation_id):
            raise ValueError(f"retired relation identity {relation_id!r} violates the governed ID pattern")
        seen_retired_keys.add(key)
        seen_ids.add(relation_id)
    return by_key


def keccak256(value: bytes) -> str:
    digest = keccak.new(digest_bits=256)
    digest.update(value)
    return "0x" + digest.hexdigest()


def sha256_bytes(value: bytes) -> str:
    return "sha256:" + hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def github_uri(repository_path: str) -> str:
    return GITHUB + repository_path.replace("\\", "/")


def logical_record_uri(repository_path: str) -> str:
    """Return the stable logical URI used by an off-chain record envelope.

    GitHub blob/main links remain evidence/source locators. They are mutable
    presentation links and are never the authoritative envelope locator.
    """

    return LOGICAL_RECORD_BASE + repository_path.replace("\\", "/")


def source_repository_path(source: str) -> str:
    if source.startswith(("records/", "evidence/", "schemas/", "docs/")):
        return source
    if re.fullmatch(r"6529NM\.2026\.001\.\d{2}", source):
        return f"records/accessions/6529NM.2026.001/objects/{source}.json"
    match = re.fullmatch(r"6529NM\.2026\.001\.RIGHTS\.\d{2}", source)
    if match:
        return f"records/accessions/6529NM.2026.001/rights/{source}.json"
    match = re.fullmatch(r"6529NM\.2026\.001\.COND\.(\d{2})", source)
    if match:
        return f"records/accessions/6529NM.2026.001/technical/6529NM.2026.001.{match.group(1)}.json"
    if source == "6529NM.2026.001":
        return "records/accessions/6529NM.2026.001/accession-statement.json"
    if source == "6529NM-ACC-2026-001":
        return "records/accessions/6529NM.2026.001/accession-certificate.json"
    if source == "6529NM.2026.001.VO-01":
        return "records/accessions/6529NM.2026.001/visual-observation-record.json"
    if source == "6529NM.2026.001.DILIGENCE-01":
        return "records/accessions/6529NM.2026.001/post-accession-diligence.json"
    if source == WINNER_OBSERVATION_ID:
        return WINNER_SOURCE_PATH
    if source == WAVE_PUBLICATION_OBSERVATION_ID:
        return WAVE_PUBLICATION_OBSERVATION_PATH
    if source == MEDIA_DESCRIPTION_AMENDMENT_ID:
        return MEDIA_DESCRIPTION_AMENDMENT_PATH
    if source == CASEY_MEDIA_AMENDMENT_ID:
        return CASEY_MEDIA_AMENDMENT_PATH
    if source.startswith("6529NM-GOV-"):
        return "records/governance/decisions.json"
    match = re.fullmatch(r"6529NM-AP-01-OUT-(\d{3})", source)
    if match:
        return f"records/programs/6529NM-AP-01/outcomes/OUT-{match.group(1)}.json"
    if source == "6529NM-AP-01":
        return "records/programs/6529NM-AP-01/program.json"
    if source.startswith("6529NM-PG-2026-001"):
        return "records/proposed-gifts/6529NM-PG-2026-001/proposal.json"
    if re.fullmatch(r"6529NM-(?:I|C|AGT|ART|ORG|W|PRJ|CA|AP-ENT|ACC-ENT|RP|MED|REL)-[A-Za-z0-9.-]+", source):
        if source.startswith("6529NM-REL-"):
            return f"records/relations/{source}.json"
        return f"records/entities/{source}.json"
    return source


EVIDENCE_CLASSES = frozenset({"A", "B", "C", "D", "E"})


def source_record_evidence_class(source: str) -> str:
    """Resolve a stable source family to a record-model evidence class.

    This registry is keyed by normalized source identifiers and repository
    paths, never by human-readable labels. Context-sensitive projections
    (for example media rights versus source observation) pass an explicit
    class to :func:`evidence` instead.
    """

    source_text = source.casefold()
    repository_path = source_repository_path(source).casefold()
    if source == MEDIA_DESCRIPTION_AMENDMENT_ID:
        return "C"
    if source == WAVE_PUBLICATION_OBSERVATION_ID:
        return "B"
    if source_text.startswith(("eip155:", "ethereum:")) or "raw/rpc/" in source_text:
        return "A"
    if repository_path.startswith("third-party/") or repository_path.startswith("sources/third-party/"):
        return "D"
    if "/public/casey-reas-collection-essay.md" in repository_path or "/public/curatorial-" in repository_path:
        return "E"
    if repository_path.startswith("docs/") and any(token in repository_path for token in ("interpret", "essay", "curat")):
        return "E"
    if repository_path.startswith("evidence/"):
        return "C"
    if repository_path.startswith("media/") or "/public/media/" in repository_path or "/media/" in repository_path:
        return "C"
    if "/technical/" in repository_path or "condition" in repository_path or "visual-observation" in repository_path or "fixity" in repository_path or "diligence" in repository_path:
        return "C"
    if (
        repository_path.startswith(("records/governance/", "records/programs/", "records/proposed-gifts/", "records/accessions/"))
        or source_text.startswith("https://6529.io/")
        or re.fullmatch(r"6529NM-(?:GOV|AP|AP-01-OUT|PG|ACC|CA|WAVE|REL|MED|ORG|ART|AGT|PRJ|W)-[A-Za-z0-9.-]+", source)
        or re.fullmatch(r"6529NM\.2026\.001(?:\.(?:RIGHTS|DILIGENCE)\.\d{2}|\.\d{2})?", source)
    ):
        return "B"
    raise ValueError(f"unclassified evidence source family: source={source!r}")


def evidence(label: str, source: str, observed_at: str, evidence_class: str) -> dict[str, Any]:
    """Construct evidence with a mandatory, non-label-derived class."""

    if evidence_class not in EVIDENCE_CLASSES:
        raise ValueError(f"invalid evidence class {evidence_class!r} for {label!r}: {source!r}")
    uri = source if source.startswith(("https://", "ipfs://", "ar://")) else github_uri(source_repository_path(source))
    return {"label": label, "uri": uri, "observed_at": observed_at, "evidence_class": evidence_class}


def source_evidence(label: str, source: str, observed_at: str) -> dict[str, Any]:
    """Construct evidence through the governed stable source-family registry."""

    public_locator = MAGNUM_PUBLIC_EVIDENCE_LOCATORS.get(source, source)
    return evidence(label, public_locator, observed_at, source_record_evidence_class(source))


def names(value: str, source_kind: str, refs: list[str], observed_at: str | None = None) -> list[dict[str, Any]]:
    observed_at = observed_at or (CASEY_AT if any("6529NM.2026.001" in ref for ref in refs) else KEYS_AT)
    evidence_refs: list[dict[str, Any]] = []
    seen: set[str] = set()
    for ref in refs:
        item = source_evidence("Name source", ref, observed_at)
        key = json.dumps(item, sort_keys=True)
        if key not in seen:
            seen.add(key)
            evidence_refs.append(item)
    return [{"value": value, "variant_role": "preferred", "source_kind": source_kind, "evidence_refs": evidence_refs}]


def names_with_source_label(value: str, source_kind: str, refs: list[str], observed_at: str | None = None) -> list[dict[str, Any]]:
    observed_at = observed_at or PROPOSAL_AT
    variants = names(value, source_kind, refs, observed_at)
    variants.append({"value": value, "variant_role": "source_label", "source_kind": source_kind, "evidence_refs": [source_evidence("Raw issuer label", ref, observed_at) for ref in refs]})
    return variants


def fact(
    status: str,
    observed_at: str,
    refs: list[str],
    notes: str,
    *,
    evidence_class: str | None = None,
    evidence_label: str = "Source record",
    evidence_refs: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Construct an independent fact without deriving class from prose.

    Ordinary source-record facts use the stable source-family registry. A
    context-sensitive fact can provide an explicit class or fully constructed
    evidence refs; the evidence() boundary itself remains class-mandatory.
    """

    if evidence_refs is None:
        evidence_refs = [
            evidence(evidence_label, ref, observed_at, evidence_class)
            if evidence_class is not None
            else source_evidence(evidence_label, ref, observed_at)
            for ref in refs
        ]
    return {"status": status, "as_of": observed_at, "evidence_refs": evidence_refs, "notes": notes}


def lifecycle_observation(observation_id: str, status: str, source_status: str, observed_at: str, refs: list[str], notes: str, evidence_refs: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    return {
        "observation_id": observation_id,
        "status": status,
        "source_status": source_status,
        "observed_at": observed_at,
        "source_record_ids": sorted(set(refs)),
        "evidence_refs": evidence_refs or [source_evidence("Lifecycle source", ref, observed_at) for ref in refs],
        "notes": notes,
    }


def authoritative_typed_reference(
    reference_type: str,
    record_id: str,
    target_type: str,
    evidence_refs: list[dict[str, Any]],
    *,
    source_status: str | None = None,
) -> dict[str, Any]:
    """Build a typed reference to one exact source record.

    The target kind and target record type are intentionally carried in the
    projection. The validator resolves the ID against the repository source
    register and rejects a missing or type-mismatched record.
    """

    reference: dict[str, Any] = {
        "reference_type": reference_type,
        "record_id": record_id,
        "source_record_id": record_id,
        "target_kind": "authoritative_record",
        "target_type": target_type,
        "registry_id": None,
        "evidence_refs": evidence_refs,
    }
    if source_status is not None:
        reference["source_status"] = source_status
    return reference


def governed_typed_reference(
    identity_inventory: dict[str, Any],
    reference_type: str,
    target_id: str,
    source_record_id: str,
    evidence_refs: list[dict[str, Any]],
    *,
    source_status: str | None = None,
) -> dict[str, Any]:
    """Build a typed reference from an exact governed registry row."""

    rows = identity_inventory.get("typed_reference_registry")
    if not isinstance(rows, list):
        raise ValueError("public identity inventory is missing typed_reference_registry")
    matches = [
        row for row in rows
        if isinstance(row, dict)
        and row.get("registry_id") == TYPED_REFERENCE_REGISTRY_ID
        and row.get("reference_type") == reference_type
        and row.get("target_id") == target_id
    ]
    if len(matches) != 1:
        raise ValueError(f"typed reference registry must contain exactly one {reference_type} target {target_id!r}")
    target = matches[0]
    if target.get("authoritative_record_id") != source_record_id:
        raise ValueError(
            f"typed reference registry target {target_id!r} is bound to "
            f"{target.get('authoritative_record_id')!r}, not {source_record_id!r}"
        )
    reference: dict[str, Any] = {
        "reference_type": reference_type,
        "record_id": target_id,
        "source_record_id": source_record_id,
        "target_kind": "governed_typed_registry",
        "target_type": target["target_type"],
        "registry_id": TYPED_REFERENCE_REGISTRY_ID,
        "caip19": target.get("caip19"),
        "evidence_refs": evidence_refs,
    }
    if source_status is not None:
        reference["source_status"] = source_status
    return reference


def common(record_type: str, record_id: str, effective_at: str, refs: list[str], evidence_refs: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "record_id": record_id,
        "record_type": record_type,
        "schema_id": PUBLIC_ENTITY_SCHEMA if record_type == "PUBLIC_ENTITY" else PUBLIC_RELATION_SCHEMA if record_type == "PUBLIC_RELATION" else WAVE_STATUS_SCHEMA,
        "subject_id": record_id,
        "visibility": "public",
        "record_version": "1.0.0",
        "created_at": GENERATED_AT,
        "observed_at": effective_at,
        "effective_at": effective_at,
        "constructor": {"id": CONSTRUCTOR_ID, "role": "constructor", "observed_at": GENERATED_AT},
        "reviewer": None,
        "record_status": "review_pending",
        "review_status": "pending_independent_review",
        "payload_sha256": "sha256:" + "0" * 64,
        "references": sorted(set(refs)),
        "evidence_refs": evidence_refs,
    }


def finalize(
    payload: dict[str, Any],
    relative_path: str,
    reviewed: bool,
    reviewer_id: str | None,
    *,
    reviewed_at: str | None = None,
    reviewed_commit: str | None = None,
    reviewed_manifest_sha256: str | None = None,
    reviewed_manifest_keccak: str | None = None,
) -> dict[str, Any]:
    if reviewed:
        if not isinstance(reviewer_id, str) or not reviewer_id:
            raise ValueError("--reviewed requires --reviewer-id from an independent reviewer")
        if not isinstance(reviewed_at, str) or not reviewed_at:
            raise ValueError("--reviewed requires an explicit --reviewed-at")
        if not isinstance(reviewed_commit, str) or not re.fullmatch(r"[0-9a-f]{40}", reviewed_commit):
            raise ValueError("--reviewed requires a 40-character lowercase --reviewed-commit")
        if not isinstance(reviewed_manifest_sha256, str) or not re.fullmatch(r"sha256:[0-9a-f]{64}", reviewed_manifest_sha256):
            raise ValueError("--reviewed requires --reviewed-manifest-sha256 as sha256:<64 lowercase hex>")
        if not isinstance(reviewed_manifest_keccak, str) or not re.fullmatch(r"0x[0-9a-f]{64}", reviewed_manifest_keccak):
            raise ValueError("--reviewed requires --reviewed-manifest-keccak as 0x<64 lowercase hex>")
        created_at = datetime.datetime.fromisoformat(payload["created_at"].replace("Z", "+00:00"))
        review_time = datetime.datetime.fromisoformat(reviewed_at.replace("Z", "+00:00"))
        if review_time <= created_at:
            raise ValueError("--reviewed-at must be after construction time")
        payload["reviewer"] = {
            "id": reviewer_id,
            "role": "reviewer",
            "reviewed_at": reviewed_at,
            "reviewed_manifest_sha256": reviewed_manifest_sha256,
            "reviewed_manifest_keccak": reviewed_manifest_keccak,
            "reviewed_commit": reviewed_commit,
            "reviewer_ids": [reviewer_id],
            "outcome": "approved",
        }
        payload["record_status"] = "reviewed"
        payload["review_status"] = "reviewed"
    # Re-finalization is used for append-only construction amendments. Always
    # zero the prior commitment first so a second pass cannot hash the stale
    # digest into its own replacement.
    payload["payload_sha256"] = "sha256:" + "0" * 64
    payload["payload_sha256"] = sha256_bytes(canonicalize(payload))
    effective_seconds = int(datetime.datetime.fromisoformat(payload["effective_at"].replace("Z", "+00:00")).timestamp())
    record_type = payload["record_type"]
    return {
        "$schema": "https://6529networkmuseum.org/schemas/record-envelope-v1.json",
        "envelope": {
            "recordType": record_type,
            "subjectId": keccak256(f"6529networkmuseum.subject.{record_type.lower()}.v1:{payload['record_id']}".encode("utf-8")),
            "contentHash": {"algorithm": 1, "digest": keccak256(canonicalize(payload)), "canonicalizationId": JCS_ID},
            "uri": logical_record_uri(relative_path),
            "schemaId": payload["schema_id"],
            "signatureScheme": ZERO32,
            "signatureHash": {"algorithm": 2, "digest": ZERO32, "canonicalizationId": JCS_ID},
            "effectiveAt": effective_seconds,
        },
        "payload": payload,
    }


def entity(record_id: str, entity_type: str, label: str, slug: str | None, route: str | None, effective_at: str, profile: dict[str, Any], refs: list[str], evidence_refs: list[dict[str, Any]], *, media_entity_ids: list[str] | None = None, reviewed: bool = False) -> tuple[str, dict[str, Any]]:
    page_exposure = {
        "INSTITUTION": "canonical_page",
        "COLLECTION": "canonical_page",
        "ARTIST": "canonical_page",
        "ORGANIZATION": "canonical_page",
        "WORK": "canonical_page",
        "PROJECT_OR_SERIES": "canonical_page",
        "CURATED_ACQUISITION": "canonical_page",
        "ACQUISITION_PROGRAM": "canonical_page",
        "RESEARCH_PUBLICATION": "canonical_page",
        "EXHIBITION": "reserved_no_instance",
    }.get(entity_type, "relational_only")
    if page_exposure != "canonical_page":
        slug = None
        route = None
    payload = common("PUBLIC_ENTITY", record_id, effective_at, refs, evidence_refs)
    payload.update({
        "entity_id": record_id,
        "entity_type": entity_type,
        "preferred_label": label,
        "public_slug": slug,
        "canonical_route": route,
        "page_exposure": page_exposure,
        "entity_status": "published" if reviewed else "review_pending",
        "status_observation": {"status_label": "published" if reviewed else "review_pending", "observed_at": effective_at, "evidence_refs": evidence_refs},
        "source_record_ids": sorted(set(refs)),
        "profile": profile,
    })
    if media_entity_ids is not None:
        payload["media_entity_ids"] = list(dict.fromkeys(media_entity_ids))
    return f"records/entities/{record_id}.json", payload


def relation(record_id: str, relation_type: str, source: str, target: str, qualifier: dict[str, Any], effective_at: str, refs: list[str], evidence_refs: list[dict[str, Any]]) -> tuple[str, dict[str, Any]]:
    payload = common("PUBLIC_RELATION", record_id, effective_at, [source, target, *refs], evidence_refs)
    payload.update({
        "relation_id": record_id,
        "source_entity_id": source,
        "target_entity_id": target,
        "relation_type": relation_type,
        "assertion_status": "asserted",
        "qualifier": qualifier,
        "source_record_ids": sorted(set(refs)),
        "evidence_refs": evidence_refs,
    })
    return f"records/relations/{record_id}.json", payload


def media_profile(role: str, locator_uri: str | None, repository_path: str | None, media_type: str, visual: bool, width: int | None, height: int | None, accessibility_text: str | None, accessibility_status: str, subject: str, credit: str, rights_status: str, source_status: str, source_refs: list[str], observed_at: str, fixity: dict[str, Any], affordances: list[str], *, derived_from: str | None = None, transform: str | None = None, wave_proposal_context: dict[str, Any] | None = None, accessibility_subject_policy: str = "not_applicable", identity_inference_prohibition: dict[str, Any] | None = None, publication_context_entity_ids: list[str] | None = None, token_source_locator: dict[str, Any] | None = None, token_source_fixity: dict[str, Any] | None = None, rights_label: str | None = None, rights_evidence_refs: list[dict[str, Any]] | None = None, source_observation_evidence_refs: list[dict[str, Any]] | None = None, accessibility_evidence_refs: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    publication_boundary = {
        "museum_retained_preservation_object": "preservation_record",
        "museum_generated_public_derivative": "public_derivative",
        "museum_authored_public_graphic": "public_graphic",
        "token_linked_source_media": "token_source",
        "historical_wave_proposal_presentation": "historical_wave_proposal_context",
    }[role]
    rights_evidence: list[dict[str, Any]] = list(rights_evidence_refs or [])
    source_evidence_refs: list[dict[str, Any]] = list(source_observation_evidence_refs or [])
    accessibility_evidence: list[dict[str, Any]] = list(accessibility_evidence_refs or [])
    if rights_evidence_refs is None or source_observation_evidence_refs is None:
        seen_evidence: set[str] = set()
        for ref in source_refs:
            key = source_repository_path(ref)
            if key in seen_evidence:
                continue
            seen_evidence.add(key)
            if rights_evidence_refs is None:
                rights_evidence.append(evidence("Rights boundary", ref, observed_at, "B"))
            if source_observation_evidence_refs is None:
                source_evidence_refs.append(evidence("Source observation", ref, observed_at, "C"))
    if accessibility_evidence_refs is None:
        accessibility_evidence = [source_evidence("Accessibility source", ref, observed_at) for ref in source_refs]
    return {
        "profile_type": "MEDIA_REFERENCE",
        "media": {
            "media_role": role,
            "publication_boundary": publication_boundary,
            "source_locator": {"uri": locator_uri, "repository_path": repository_path},
            "media_type": media_type,
            "visual": visual,
            "width": width,
            "height": height,
            "accessibility_text": accessibility_text,
            "accessibility_status": accessibility_status,
            "accessibility_subject_policy": accessibility_subject_policy,
            "accessibility_publication_entity_id": None,
            "identity_inference_prohibition": identity_inference_prohibition,
            "subject_entity_id": subject,
            "credit": credit,
            "rights": {"status": rights_status, "statement_entity_id": None, "observed_at": observed_at, "evidence_refs": rights_evidence, "notes": (f"Source rights label: {rights_label}. " if rights_label else "") + "Rights state is projected from the cited source and is not inferred from media availability."},
            "source_observation": {"status": source_status, "observed_at": observed_at, "evidence_refs": source_evidence_refs, "notes": "Source observation and mutable-host boundary remain separate from preservation status."},
            "accessibility_evidence_refs": accessibility_evidence,
            "fixity": fixity,
            "token_source_locator": token_source_locator,
            "token_source_fixity": token_source_fixity,
            "source_record_ids": sorted(set(source_refs)),
            "derived_from_media_entity_id": derived_from,
            "transform_profile": transform,
            "wave_proposal_context": wave_proposal_context,
            "publication_context_entity_ids": sorted(set(publication_context_entity_ids or [])),
            "allowed_ui_affordances": affordances,
        },
    }


def verify_evidence_paths(records: dict[str, dict[str, Any]]) -> None:
    missing: set[str] = set()

    def visit(value: Any) -> None:
        if isinstance(value, dict):
            uri = value.get("uri")
            if isinstance(uri, str) and uri.startswith(GITHUB):
                relative = uri[len(GITHUB):]
                if not (ROOT / relative).is_file() and relative not in records:
                    missing.add(relative)
            for child in value.values():
                visit(child)
        elif isinstance(value, list):
            for child in value:
                visit(child)

    for record in records.values():
        visit(record.get("payload", {}))
    if missing:
        raise ValueError("public migration contains nonexistent evidence paths: " + ", ".join(sorted(missing)))


def build_records(
    reviewed: bool = False,
    reviewer_id: str | None = None,
    *,
    reviewed_at: str | None = None,
    reviewed_commit: str | None = None,
    reviewed_manifest_sha256: str | None = None,
    reviewed_manifest_keccak: str | None = None,
) -> dict[str, dict[str, Any]]:
    vocab = load_json(VOCAB_PATH)
    identity_inventory = load_json(IDENTITY_INVENTORY_PATH)
    identity_indexes = identity_binding_indexes(identity_inventory)
    relation_identity_inventory = load_json(RELATION_IDENTITY_INVENTORY_PATH)
    relation_indexes = relation_binding_indexes(relation_identity_inventory)
    used_relation_keys: set[str] = set()
    slug_inventory = {
        row["entity_id"]: row for row in identity_inventory.get("public_slug_inventory", [])
    }
    records: dict[str, dict[str, Any]] = {}
    def finish(payload: dict[str, Any], relative: str) -> dict[str, Any]:
        return finalize(
            payload,
            relative,
            reviewed,
            reviewer_id,
            reviewed_at=reviewed_at,
            reviewed_commit=reviewed_commit,
            reviewed_manifest_sha256=reviewed_manifest_sha256,
            reviewed_manifest_keccak=reviewed_manifest_keccak,
        )

    def add_entity(*args: Any, **kwargs: Any) -> str:
        relative, payload = entity(*args, reviewed=reviewed, **kwargs)
        if relative in records:
            raise ValueError(f"duplicate generated entity record {relative}")
        records[relative] = finish(payload, relative)
        return payload["entity_id"]
    def add_relation(_legacy_record_id: str, relation_type: str, source: str, target: str, qualifier: dict[str, Any], effective_at: str, refs: list[str], evidence_refs: list[dict[str, Any]]) -> str:
        relation_key = semantic_relation_key(relation_type, source, target, qualifier)
        record_id = relation_indexes.get(relation_key)
        if record_id is None:
            raise ValueError(f"missing governed relation identity binding for {relation_key!r}")
        if relation_key in used_relation_keys:
            raise ValueError(f"duplicate generated semantic relation {relation_key!r}")
        used_relation_keys.add(relation_key)
        relative, payload = relation(record_id, relation_type, source, target, qualifier, effective_at, refs, evidence_refs)
        if relative in records:
            raise ValueError(f"duplicate generated relation record {relative}")
        records[relative] = finish(payload, relative)
        return payload["relation_id"]

    winner_payload = common("WAVE_STATUS_OBSERVATION", WINNER_OBSERVATION_ID, WINNER_AT, ["6529NM-PG-2026-001"], [
        source_evidence("Original PARTICIPATORY proposal observation", "records/proposed-gifts/6529NM-PG-2026-001/proposal.json", PROPOSAL_AT),
        source_evidence("Signed-drop API WINNER status readback (is_signed=true)", WINNER_SOURCE_URL, WINNER_AT),
    ])
    winner_payload.update({
        "observation_id": WINNER_OBSERVATION_ID,
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
        "source_url": WINNER_SOURCE_URL,
        "observation_method": "signed_drop_api_readback",
        "selection_effect": "selected_by_museum_wave_acquisition_review_in_progress",
        "non_effects": ["acceptance_not_established", "transfer_not_established", "title_not_established", "custody_not_established", "rights_not_established", "technical_not_established", "preservation_not_established", "accession_not_established", "collection_membership_not_established"],
        "prior_observation": {
            "source_status": "PARTICIPATORY",
            "observed_at": PROPOSAL_AT,
            "source_record_id": "6529NM-PG-2026-001",
            "source_record_path": None,
            "source_repository_visibility": "complete_manifest_only",
            "source_url": "https://6529.io/waves/5f207393-5418-4a75-8738-e40edb44a94d?drop=002bfa4f-8416-48bf-b35e-38f354e9a9f0",
        },
        "source_record_ids": ["6529NM-PG-2026-001"],
    })
    records[WINNER_SOURCE_PATH] = finish(winner_payload, WINNER_SOURCE_PATH)

    def fixed_id(entity_type: str, source_key: str) -> str:
        try:
            return identity_indexes[entity_type][source_key]
        except KeyError as exc:
            raise ValueError(f"missing {entity_type} identity binding for {source_key!r}") from exc

    def fixed_observation_id(work_id: str, phase: str) -> str:
        return fixed_id("WORK_LIFECYCLE_OBSERVATION", f"{work_id}:{phase}")

    institution = fixed_id("INSTITUTION", "6529-network-museum")
    collection = fixed_id("COLLECTION", "permanent-collection")
    casey_agent = fixed_id("AGENT", "casey-reas")
    casey_artist = fixed_id("ARTIST", "casey-reas")
    art_blocks = fixed_id("ORGANIZATION", "art-blocks")
    magnum_org = fixed_id("ORGANIZATION", "magnum-photos")
    magnum_project = fixed_id("PROJECT_OR_SERIES", "magnum-photos-75")
    gift_program = fixed_id("ACQUISITION_PROGRAM", "gift-acquisitions")
    keys_program = fixed_id("ACQUISITION_PROGRAM", "keys-and-gates")
    project_names = ["CENTURY", "Pre-Process", "Phototaxis", "923 EMPTY ROOMS", "Ex Nihilo (Cosmos)"]
    projects = {name: fixed_id("PROJECT_OR_SERIES", f"casey-project:{name}") for name in project_names}
    accession = fixed_id("ACCESSION", "6529NM.2026.001")
    publication = fixed_id("RESEARCH_PUBLICATION", "the-system-in-seven-states")
    keys_publication = fixed_id("RESEARCH_PUBLICATION", "access-control-and-exit")
    magnum_publication = fixed_id("RESEARCH_PUBLICATION", "conflict-at-its-edges")
    media_retained = fixed_id("MEDIA_REFERENCE", "casey:retained-manifest")
    media_token = fixed_id("MEDIA_REFERENCE", "casey:token-metadata")
    media_derivative = fixed_id("MEDIA_REFERENCE", "museum:conflict-at-its-edges:cover")

    object_paths = sorted((ROOT / "records/accessions/6529NM.2026.001/objects").glob("*.json"))
    casey_objects = [load_json(path)["payload"] for path in object_paths]
    casey_objects_by_id = {obj["record_id"]: obj for obj in casey_objects}
    casey_object_ids = [obj["record_id"] for obj in casey_objects]
    casey_work_ids_by_object = {
        object_id: fixed_id("WORK", object_id)
        for object_id in casey_object_ids
    }
    casey_work_ids = [casey_work_ids_by_object[object_id] for object_id in casey_object_ids]
    casey_media_ids_by_object = {
        obj["record_id"]: fixed_id("MEDIA_REFERENCE", f"casey-live:{obj['record_id']}")
        for obj in casey_objects
    }
    casey_media_ids = [casey_media_ids_by_object[obj["record_id"]] for obj in casey_objects]
    casey_still_media_ids_by_object = {
        obj["record_id"]: fixed_id("MEDIA_REFERENCE", f"casey-still:{obj['record_id']}")
        for obj in casey_objects
    }
    casey_still_media_ids = [casey_still_media_ids_by_object[obj["record_id"]] for obj in casey_objects]
    accession_refs = ["6529NM.2026.001", "6529NM-ACC-2026-001"]
    institution_refs = ["6529NM-GOV-1052156", "6529NM-GOV-1052812"]
    add_entity(institution, "INSTITUTION", "6529 Network Museum", None, "/museum/network", CASEY_AT, {
        "profile_type": "INSTITUTION", "institution_kind": "network_museum", "mission": "A public, evidence-led museum for network-native art and its long-term care.",
        "authority": {"authority_status": "established", "authority_record_ids": institution_refs, "evidence_refs": [source_evidence("Adopted Museum policy", "6529NM-GOV-1052156", CASEY_AT)]},
        "name_variants": names("6529 Network Museum", "museum_record", institution_refs), "collection_entity_id": collection,
    }, institution_refs, [source_evidence("Museum governance source", "6529NM-GOV-1052156", CASEY_AT)])
    add_entity(collection, "COLLECTION", "6529 Network Museum permanent Collection", None, "/museum/network/collection", CASEY_AT, {
        "profile_type": "COLLECTION", "collection_kind": "permanent_collection", "institution_entity_id": institution, "membership_rule": "accession_only", "admitted_work_entity_ids": casey_work_ids,
        "evidence_refs": [source_evidence("Casey accession register", "6529NM.2026.001", CASEY_AT)],
    }, [institution, *accession_refs], [source_evidence("Accession-only membership rule", "6529NM.2026.001", CASEY_AT)])
    add_entity(casey_agent, "AGENT", "Casey REAS", "casey-reas-agent", "/museum/network/agents/casey-reas-agent", CASEY_AT, {
        "profile_type": "AGENT", "agent_kind": "PERSON", "authority": {"authority_status": "established", "authority_record_ids": [], "evidence_refs": [source_evidence("Casey object records", object_paths[0].relative_to(ROOT).as_posix(), CASEY_AT)]},
        "name_variants": names("Casey REAS", "artist_statement", ["6529NM.2026.001.01"]), "role_contexts": ["artist", "creator", "donated-work subject"],
    }, ["6529NM.2026.001.01", "6529NM.2026.001.07"], [source_evidence("Casey artist practice record", "records/accessions/6529NM.2026.001/public/casey-reas-artist-practice.md", CASEY_AT)])
    add_entity(casey_artist, "ARTIST", "Casey Reas", "casey-reas", "/museum/network/artists/casey-reas", CASEY_AT, {
        "profile_type": "ARTIST", "authority": {"authority_status": "established", "authority_record_ids": [casey_agent], "evidence_refs": [source_evidence("Casey artist practice record", "records/accessions/6529NM.2026.001/public/casey-reas-artist-practice.md", CASEY_AT)]},
        "practice": {"summary": "A practice spanning software, generative systems, image, publication, and the cultural conditions of computation.", "areas": ["generative software", "digital image", "systems research"], "evidence_refs": [source_evidence("Casey artist practice record", "records/accessions/6529NM.2026.001/public/casey-reas-artist-practice.md", CASEY_AT)]},
        "name_variants": names("Casey Reas", "artist_statement", ["6529NM.2026.001.01"]),
    }, [casey_agent, "6529NM.2026.001.01", "6529NM.2026.001.07"], [source_evidence("Casey artist practice record", "records/accessions/6529NM.2026.001/public/casey-reas-artist-practice.md", CASEY_AT)])
    add_entity(art_blocks, "ORGANIZATION", "Art Blocks", "art-blocks", "/museum/network/organizations/art-blocks", CASEY_AT, {
        "profile_type": "ORGANIZATION", "organization_kind": "platform", "history_summary": "Art Blocks is the publishing platform identified by the Casey object records for the relevant generative projects.", "roles": ["publishing platform", "project context"],
        "authority": {"authority_status": "provisional", "authority_record_ids": [], "evidence_refs": [source_evidence("Casey object record", "6529NM.2026.001.01", CASEY_AT)]}, "name_variants": names("Art Blocks", "published_source", ["6529NM.2026.001.01"]),
    }, ["6529NM.2026.001.01"], [source_evidence("Casey object record", "6529NM.2026.001.01", CASEY_AT)])
    magnum_org_profile_path = "records/proposed-gifts/6529NM-PG-2026-001/public/scholarship/entities/magnum-photos.md"
    magnum_org_original_evidence = source_evidence("Original Museum Wave publication context", WINNER_SOURCE_URL, PROPOSAL_AT)
    magnum_org_proposal_evidence = source_evidence("Original proposed-gift context", "records/proposed-gifts/6529NM-PG-2026-001/proposal.json", PROPOSAL_AT)
    magnum_org_research_evidence = source_evidence("Magnum Photos research profile", magnum_org_profile_path, MAGNUM_PUBLICATION_AT)
    add_entity(magnum_org, "ORGANIZATION", "Magnum Photos", slug_inventory[magnum_org]["public_slug"], slug_inventory[magnum_org]["canonical_route"], MAGNUM_PUBLICATION_AT, {
        "profile_type": "ORGANIZATION", "organization_kind": "collective", "history_summary": "Founded in 1947 as a photographer-owned cooperative, Magnum Photos joined individual authorship to a shared editorial, archival, and distribution structure. This profile follows that institutional history into Magnum Photos 75, the 2022 anniversary project from which the five Works under review were selected.", "roles": ["photographic cooperative", "archive and publisher", "Magnum Photos 75 project originator/publisher"],
        "authority": {"authority_status": "provisional", "authority_record_ids": [], "evidence_refs": [magnum_org_original_evidence, magnum_org_proposal_evidence, magnum_org_research_evidence]}, "name_variants": names("Magnum Photos", "published_source", [WINNER_SOURCE_URL, "6529NM-PG-2026-001", magnum_org_profile_path], MAGNUM_PUBLICATION_AT),
    }, ["6529NM-PG-2026-001"], [magnum_org_original_evidence, magnum_org_proposal_evidence, magnum_org_research_evidence])
    add_entity(gift_program, "ACQUISITION_PROGRAM", "Gift Acquisitions", slug_inventory[gift_program]["public_slug"], slug_inventory[gift_program]["canonical_route"], CASEY_AT, {
        "profile_type": "ACQUISITION_PROGRAM", "program_kind": "donation_pathway", "program_id": gift_program, "authority_record_ids": institution_refs, "rules_summary": "A standing donation pathway governed by adopted Museum donation and collection-scope decisions; each gift retains its own review and accession gates.", "program_status": "active", "produced_acquisition_entity_ids": ["6529NM-CA-2026-001", "6529NM-CA-2026-003"], "selected_outcome_record_ids": [], "evidence_refs": [source_evidence("Adopted donation decision", "6529NM-GOV-1052812", CASEY_AT)],
    }, institution_refs, [source_evidence("Adopted donation decision", "6529NM-GOV-1052812", CASEY_AT)])
    keys_program_source = "6529NM-AP-01"
    program = load_json(ROOT / "records/programs/6529NM-AP-01/program.json")
    selected_index = load_json(ROOT / "records/programs/6529NM-AP-01/selected-works.json")
    outcomes = selected_index["works"]
    outcomes_by_id = {row["record_id"]: row for row in outcomes}
    keys_media_ids_by_outcome = {
        row["record_id"]: fixed_id("MEDIA_REFERENCE", f"keys-presentation:{row['record_id']}")
        for row in outcomes
    }
    keys_media_ids = [keys_media_ids_by_outcome[row["record_id"]] for row in outcomes]
    add_entity(keys_program, "ACQUISITION_PROGRAM", "Keys and Gates", slug_inventory[keys_program]["public_slug"], slug_inventory[keys_program]["canonical_route"], KEYS_AT, {
        "profile_type": "ACQUISITION_PROGRAM", "program_kind": "themed_program", "program_id": keys_program_source, "authority_record_ids": [keys_program_source], "rules_summary": "A 60-day photography program with TDH/WAVE selection, CC0 and consent terms, a planned 0.5 ETH purchase price per acquired work, quantity determined by Meme Card mints, and rank-order fallback.", "program_status": program["status"], "produced_acquisition_entity_ids": ["6529NM-CA-2026-002"], "selected_outcome_record_ids": [row["record_id"] for row in outcomes], "evidence_refs": [source_evidence("Keys and Gates program record", "records/programs/6529NM-AP-01/program.json", KEYS_AT)],
    }, [keys_program_source, *[row["record_id"] for row in outcomes]], [source_evidence("Keys and Gates program record", "records/programs/6529NM-AP-01/program.json", KEYS_AT)])

    for index, (project_name, project_id) in enumerate(projects.items()):
        project_objects = [obj for obj in casey_objects if obj.get("project", {}).get("name") == project_name]
        project_object_ids = [obj["record_id"] for obj in project_objects]
        project_work_ids = [casey_work_ids_by_object[obj["record_id"]] for obj in project_objects]
        project_inventory = slug_inventory[project_id]
        add_entity(project_id, "PROJECT_OR_SERIES", project_name, project_inventory["public_slug"], project_inventory["canonical_route"], CASEY_AT, {
            "profile_type": "PROJECT_OR_SERIES", "project_type": "project", "project_relation_basis": "source_project_record", "scope_statement": f"The Casey object records identify {project_name} as a distinct project context; this projection does not assert ownership of all project outputs.", "agent_entity_ids": [casey_artist], "work_entity_ids": project_work_ids, "ownership_boundary": "Project context is distinct from Museum ownership; only separately accessioned Work entities enter the Collection.", "source_record_ids": project_object_ids or ["6529NM.2026.001"], "evidence_refs": [source_evidence("Casey project source records", project_object_ids[0] if project_object_ids else "6529NM.2026.001", CASEY_AT)],
        }, [casey_artist, art_blocks, *project_work_ids], [source_evidence("Casey project source record", project_object_ids[0] if project_object_ids else "6529NM.2026.001", CASEY_AT)])

    for index, obj in enumerate(casey_objects):
        object_id = obj["record_id"]
        work_id = casey_work_ids_by_object[object_id]
        project_id = projects[obj["project"]["name"]]
        rights_id = next((ref for ref in obj.get("references", []) if ".RIGHTS." in ref), "6529NM.2026.001.RIGHTS.01")
        condition_id = next((ref for ref in obj.get("references", []) if ".COND." in ref), "6529NM.2026.001.COND.01")
        add_entity(work_id, "WORK", obj["title"], work_id, f"/museum/network/works/{work_id}", CASEY_AT, {
            "profile_type": "WORK", "creator_entity_ids": [casey_artist], "title": obj["title"], "creation_date": {"display": "not established in the accession projection", "status": "not_established", "earliest": None, "latest": None, "evidence_refs": [source_evidence("Casey object record", object_id, CASEY_AT)]}, "medium": obj["medium"], "work_lifecycle_status": "accessioned",
            "current_museum_relation": {"museum_entity_id": institution, "relation_status": "permanent_collection", "as_of": CASEY_AT, "evidence_refs": [source_evidence("Accession certificate", "6529NM-ACC-2026-001", CASEY_AT)]},
            "mint_fact": fact("verified", CASEY_AT, [object_id], "The existing Work Description carries the token identity; minting remains a separate fact from accession."),
            "collection_membership": {"status": "permanent_collection", "collection_entity_id": collection, "accession_entity_ids": [accession], "source_record_ids": ["6529NM.2026.001", "6529NM-ACC-2026-001"], "evidence_refs": [source_evidence("Accession certificate", "6529NM-ACC-2026-001", CASEY_AT)]},
            "project_or_series_entity_ids": [project_id], "acquisition_entity_ids": ["6529NM-CA-2026-001"], "program_entity_ids": [gift_program], "accession_entity_ids": [accession], "lifecycle_observations": [lifecycle_observation(fixed_observation_id(work_id, "accessioned"), "accessioned", "accessioned", CASEY_AT, ["6529NM-ACC-2026-001", object_id], "The Work is admitted through the completed Casey accession; mint, rights, custody, and preservation remain independently recorded facts.")],
            "component_references": [authoritative_typed_reference("component", object_id, "WORK_DESCRIPTION", [source_evidence("Existing WORK_DESCRIPTION", object_id, CASEY_AT)])], "manifestation_references": [authoritative_typed_reference("manifestation", "6529NM.2026.001.VO-01", "VISUAL_OBSERVATION", [source_evidence("Visual observation", "6529NM.2026.001.VO-01", CASEY_AT)])], "identity_boundary": "The public Work identity is separate from the accession lot, token, component record, manifestation, title, custody, and future acquisition relations.", "evidence_refs": [source_evidence("Existing WORK_DESCRIPTION", object_id, CASEY_AT), evidence("Chain transfer receipt", "evidence/casey-reas/raw/rpc/eth-get-transaction-receipt-0xbdde33b32d4b70335b10cbd37c0b00a027844f14c900d82aa4f75b7a7b390498.json", CASEY_AT, "A"), source_evidence("Rights statement", rights_id, CASEY_AT), source_evidence("Condition report", condition_id, CASEY_AT)],
        }, [object_id, "6529NM.2026.001", "6529NM-ACC-2026-001", rights_id, condition_id, "6529NM.2026.001.VO-01", CASEY_MEDIA_AMENDMENT_ID, project_id, accession, "6529NM-CA-2026-001", gift_program], [source_evidence("Existing WORK_DESCRIPTION", object_id, CASEY_AT), source_evidence("Append-only Casey media presentation correction", CASEY_MEDIA_AMENDMENT_ID, CASEY_MEDIA_AT)], media_entity_ids=([casey_still_media_ids_by_object[object_id], casey_media_ids_by_object[object_id], media_retained, media_token] if index == 0 else [casey_still_media_ids_by_object[object_id], casey_media_ids_by_object[object_id]]))

    add_entity(accession, "ACCESSION", "Casey Reas accession 6529NM.2026.001", None, None, CASEY_AT, {
        "profile_type": "ACCESSION", "accession_number": "6529NM.2026.001", "accession_status": "complete", "admitted_work_entity_ids": casey_work_ids, "source_accession_record_id": "6529NM-ACC-2026-001", "evidence_refs": [source_evidence("Accession certificate", "6529NM-ACC-2026-001", CASEY_AT)],
    }, ["6529NM.2026.001", "6529NM-ACC-2026-001", *casey_work_ids], [source_evidence("Accession certificate", "6529NM-ACC-2026-001", CASEY_AT)])
    add_entity(publication, "RESEARCH_PUBLICATION", "The System in Seven States", "the-system-in-seven-states", "/museum/network/research/the-system-in-seven-states", CASEY_AT, {
        "profile_type": "RESEARCH_PUBLICATION", "publication_kind": "collection_essay", "title": "The System in Seven States", "publication_date": "2026-08-02", "version": "1.5.0", "author_entity_ids": [institution], "subject_entity_ids": ["6529NM-CA-2026-001", *projects.values(), *casey_work_ids], "publication_document_uri": github_uri("records/accessions/6529NM.2026.001/public/casey-reas-collection-essay.md"), "evidence_refs": [source_evidence("Published collection essay", "records/accessions/6529NM.2026.001/public/casey-reas-collection-essay.md", CASEY_AT)],
    }, ["6529NM.2026.001", "6529NM-CA-2026-001", *projects.values(), *casey_work_ids], [source_evidence("Published collection essay", "records/accessions/6529NM.2026.001/public/casey-reas-collection-essay.md", CASEY_AT)])

    keys_agent_ids_by_outcome: dict[str, str] = {}
    keys_artist_ids_by_outcome: dict[str, str] = {}
    grouped_keys_rows: dict[str, list[dict[str, Any]]] = {}
    for row in outcomes:
        artist_key = f"keys-and-gates:artist:{row['artist']}"
        agent_id = fixed_id("AGENT", artist_key)
        artist_id = fixed_id("ARTIST", artist_key)
        keys_agent_ids_by_outcome[row["record_id"]] = agent_id
        keys_artist_ids_by_outcome[row["record_id"]] = artist_id
        grouped_keys_rows.setdefault(artist_key, []).append(row)
    for artist_key, rows in sorted(grouped_keys_rows.items()):
        ordered_rows = sorted(rows, key=lambda row: row["record_id"])
        artist_name = ordered_rows[0]["artist"]
        if any(row["artist"] != artist_name for row in ordered_rows):
            raise ValueError(f"identity binding {artist_key!r} merges distinct artist labels")
        agent_id = fixed_id("AGENT", artist_key)
        artist_id = fixed_id("ARTIST", artist_key)
        artist_outcomes = [row["record_id"] for row in ordered_rows]
        add_entity(agent_id, "AGENT", artist_name, None, None, KEYS_AT, {
            "profile_type": "AGENT", "agent_kind": "PERSON", "authority": {"authority_status": "source_label_only", "authority_record_ids": [], "evidence_refs": [source_evidence("Keys and Gates outcome", artist_outcomes[0], KEYS_AT)]}, "name_variants": names(artist_name, "wave", artist_outcomes), "role_contexts": ["submitting artist label"],
        }, [*artist_outcomes, keys_program_source], [source_evidence("Keys and Gates outcome", outcome_id, KEYS_AT) for outcome_id in artist_outcomes])
        artist_slug = slug_inventory[artist_id]["public_slug"]
        add_entity(artist_id, "ARTIST", artist_name, artist_slug, slug_inventory[artist_id]["canonical_route"], KEYS_AT, {
            "profile_type": "ARTIST", "authority": {"authority_status": "source_label_only", "authority_record_ids": [agent_id], "evidence_refs": [source_evidence("Keys and Gates artist label", artist_outcomes[0], KEYS_AT)]}, "practice": {"summary": "A limited public artist profile derived from the artist label attached to a Keys and Gates program outcome; it does not assert a complete scholarly biography.", "areas": ["photography", "program submission"], "evidence_refs": [source_evidence("Keys and Gates artist label", ref, KEYS_AT) for ref in artist_outcomes]}, "name_variants": names(artist_name, "wave", artist_outcomes, KEYS_AT),
        }, [*artist_outcomes, keys_program_source, agent_id], [source_evidence("Keys and Gates artist label", artist_outcomes[0], KEYS_AT)])
    keys_work_ids: list[str] = []
    keys_work_ids_by_outcome: dict[str, str] = {}
    for index, row in enumerate(outcomes):
        work_id = fixed_id("WORK", row["record_id"])
        keys_work_ids.append(work_id)
        outcome_id = row["record_id"]
        keys_work_ids_by_outcome[outcome_id] = work_id
        add_entity(work_id, "WORK", row["title"], work_id, f"/museum/network/works/{work_id}", KEYS_AT, {
            "profile_type": "WORK", "creator_entity_ids": [keys_artist_ids_by_outcome[outcome_id]], "title": row["title"], "creation_date": {"display": "not established", "status": "not_established", "earliest": None, "latest": None, "evidence_refs": [source_evidence("Keys and Gates outcome", outcome_id, KEYS_AT)]}, "medium": "photographic submission; final technical and identity state unverified", "work_lifecycle_status": "selected_through_acquisition_program", "current_museum_relation": {"museum_entity_id": institution, "relation_status": "selected_through_acquisition_program", "as_of": KEYS_AT, "evidence_refs": [source_evidence("Keys and Gates selected-works index", outcome_id, KEYS_AT)]}, "mint_fact": fact("pending", KEYS_AT, [outcome_id], "The source outcome is selected_unminted; minting is an independent pending fact and does not establish acquisition or Collection membership."), "collection_membership": {"status": "not_in_collection", "collection_entity_id": None, "accession_entity_ids": [], "source_record_ids": [outcome_id], "evidence_refs": [source_evidence("Selected outcome is not an accession", outcome_id, KEYS_AT)]}, "project_or_series_entity_ids": [], "acquisition_entity_ids": ["6529NM-CA-2026-002"], "program_entity_ids": [keys_program], "accession_entity_ids": [], "lifecycle_observations": [lifecycle_observation(fixed_observation_id(work_id, "selected_unminted"), "selected_through_acquisition_program", "selected_unminted", KEYS_AT, [outcome_id, keys_program_source], "The program selection remains a historical source outcome; minting, acquisition, accession, and Collection membership are independent facts.")], "component_references": [authoritative_typed_reference("component", outcome_id, "PROGRAM_OUTCOME", [source_evidence("Selected outcome source", outcome_id, KEYS_AT)], source_status="selected_unminted")], "manifestation_references": [], "identity_boundary": "This Work identity is independent of the acquisition, program outcome, mint, payment, title, custody, rights, technical review, preservation, display, and any later accession.", "evidence_refs": [source_evidence("Keys and Gates outcome", outcome_id, KEYS_AT)],
        }, [outcome_id, keys_program_source, keys_program, "6529NM-CA-2026-002", keys_agent_ids_by_outcome[outcome_id]], [source_evidence("Keys and Gates outcome", outcome_id, KEYS_AT)], media_entity_ids=[keys_media_ids_by_outcome[outcome_id]])

    keys_artist_ids = sorted((fixed_id("ARTIST", artist_key) for artist_key in grouped_keys_rows), key=lambda entity_id: int(entity_id.rsplit("-", 1)[-1]))
    keys_essay_path = "records/programs/6529NM-AP-01/public/curatorial-essay.md"
    add_entity(keys_publication, "RESEARCH_PUBLICATION", "Access, Control, and Exit", slug_inventory[keys_publication]["public_slug"], slug_inventory[keys_publication]["canonical_route"], KEYS_PUBLICATION_AT, {
        "profile_type": "RESEARCH_PUBLICATION", "publication_kind": "catalogue_essay", "title": "Access, Control, and Exit", "publication_date": "2026-08-08", "version": "1.1", "author_entity_ids": [institution], "subject_entity_ids": ["6529NM-CA-2026-002", *keys_work_ids, *keys_artist_ids], "publication_document_uri": github_uri(keys_essay_path), "evidence_refs": [source_evidence("Keys and Gates Research Publication", keys_essay_path, KEYS_PUBLICATION_AT)],
    }, [keys_program_source, "6529NM-CA-2026-002", *keys_work_ids, *keys_artist_ids], [source_evidence("Keys and Gates Research Publication", keys_essay_path, KEYS_PUBLICATION_AT)])

    proposal = load_json(ROOT / "records/proposed-gifts/6529NM-PG-2026-001/proposal.json")
    magnum_work_source_ids = [obj["candidate_object_id"] for obj in proposal["objects"]]
    magnum_work_ids_by_candidate = {
        candidate_id: fixed_id("WORK", candidate_id)
        for candidate_id in magnum_work_source_ids
    }
    magnum_agent_ids_by_candidate = {
        candidate_id: fixed_id("AGENT", candidate_id)
        for candidate_id in magnum_work_source_ids
    }
    magnum_artist_ids_by_candidate = {
        candidate_id: fixed_id("ARTIST", candidate_id)
        for candidate_id in magnum_work_source_ids
    }
    magnum_artist_ids = [magnum_artist_ids_by_candidate[candidate_id] for candidate_id in magnum_work_source_ids]
    magnum_works = [magnum_work_ids_by_candidate[candidate_id] for candidate_id in magnum_work_source_ids]
    magnum_media_ids_by_candidate = {
        candidate_id: fixed_id("MEDIA_REFERENCE", f"magnum:{candidate_id}")
        for candidate_id in magnum_work_source_ids
    }
    magnum_media_ids = [magnum_media_ids_by_candidate[candidate_id] for candidate_id in magnum_work_source_ids]
    first_magnum_candidate = magnum_work_source_ids[0]
    media_wave = magnum_media_ids_by_candidate[first_magnum_candidate]
    magnum_artist_publications = {
        "6529NM-PG-2026-001.OBJ-001": {
            "path": "records/proposed-gifts/6529NM-PG-2026-001/public/scholarship/artists/david-seymour.md",
            "summary": "David Seymour's photographs often turn from the spectacle of war to its human aftermath, particularly children, displacement, and reconstruction. The selected 1952 Negev photograph belongs to this sustained attention to lives organized by borders and political upheaval.",
            "areas": ["documentary photography", "conflict and aftermath", "children and displacement"],
        },
        "6529NM-PG-2026-001.OBJ-002": {
            "path": "records/proposed-gifts/6529NM-PG-2026-001/public/scholarship/artists/larry-towell.md",
            "summary": "Larry Towell's long-form black-and-white practice is grounded in land, family, conflict, and the pressures political systems exert on private life. The selected 1986 El Salvador photograph places armed presence beside domestic and religious space.",
            "areas": ["documentary photography", "land and family", "conflict and private life"],
        },
        "6529NM-PG-2026-001.OBJ-003": {
            "path": "records/proposed-gifts/6529NM-PG-2026-001/public/scholarship/artists/micha-bar-am.md",
            "summary": "Micha Bar-Am's photography is rooted in the contested civic and military history of Israel, combining close access with a wary attention to ambiguity. The selected 1989 Jerusalem photograph records motion, smoke, ritual space, and public confrontation without resolving them into a single account.",
            "areas": ["documentary photography", "Israel and civic history", "conflict and ambiguity"],
        },
        "6529NM-PG-2026-001.OBJ-004": {
            "path": "records/proposed-gifts/6529NM-PG-2026-001/public/scholarship/artists/moises-saman.md",
            "summary": "Moisés Saman's work follows war and political upheaval through their unstable aftermaths, often attending to the distance between official narrative and lived experience. The selected 2011 Tripoli photograph centers an apparently young person before a wall marked by dark spots whose cause the image does not establish.",
            "areas": ["documentary photography", "war and political upheaval", "aftermath and uncertainty"],
        },
        "6529NM-PG-2026-001.OBJ-005": {
            "path": "records/proposed-gifts/6529NM-PG-2026-001/public/scholarship/artists/lorenzo-meloni.md",
            "summary": "Lorenzo Meloni examines the architecture, symbols, and historical afterlives of conflict, frequently allowing built space to carry the weight of absent bodies. The selected 2016 Palmyra photograph studies destruction as both material fact and contested image.",
            "areas": ["documentary photography", "architecture and conflict", "ruins and historical memory"],
        },
    }
    for obj in proposal["objects"]:
        candidate_id = obj["candidate_object_id"]
        agent_id = magnum_agent_ids_by_candidate[candidate_id]
        work_id = magnum_work_ids_by_candidate[candidate_id]
        artist_id = magnum_artist_ids_by_candidate[candidate_id]
        artist_publication = magnum_artist_publications[candidate_id]
        proposal_artist_evidence = source_evidence("Proposed gift artist label", "records/proposed-gifts/6529NM-PG-2026-001/proposal.json", PROPOSAL_AT)
        research_artist_evidence = source_evidence("Museum artist research profile", artist_publication["path"], MAGNUM_PUBLICATION_AT)
        add_entity(agent_id, "AGENT", obj["artist"], None, None, PROPOSAL_AT, {
            "profile_type": "AGENT", "agent_kind": "PERSON", "authority": {"authority_status": "source_label_only", "authority_record_ids": [], "evidence_refs": [source_evidence("Proposed gift object label", "6529NM-PG-2026-001", PROPOSAL_AT)]}, "name_variants": names(obj["artist"], "proposal", ["6529NM-PG-2026-001"]), "role_contexts": ["proposed work creator label"],
        }, ["6529NM-PG-2026-001"], [source_evidence("Proposed gift object label", "6529NM-PG-2026-001", PROPOSAL_AT)])
        add_entity(artist_id, "ARTIST", obj["artist"], slug_inventory[artist_id]["public_slug"], slug_inventory[artist_id]["canonical_route"], MAGNUM_PUBLICATION_AT, {
            "profile_type": "ARTIST", "authority": {"authority_status": "provisional", "authority_record_ids": [agent_id], "evidence_refs": [proposal_artist_evidence, research_artist_evidence]}, "practice": {"summary": artist_publication["summary"], "areas": artist_publication["areas"], "evidence_refs": [research_artist_evidence]}, "name_variants": names_with_source_label(obj["artist"], "proposal", ["6529NM-PG-2026-001"], PROPOSAL_AT),
        }, [agent_id, "6529NM-PG-2026-001", candidate_id], [proposal_artist_evidence, research_artist_evidence])
        add_entity(work_id, "WORK", obj["title"], work_id, f"/museum/network/works/{work_id}", WINNER_AT, {
            "profile_type": "WORK", "creator_entity_ids": [artist_id], "title": obj["title"], "creation_date": {"display": str(obj["date"]), "status": "established", "earliest": f"{obj['date']}-01-01", "latest": f"{obj['date']}-12-31", "evidence_refs": [source_evidence("Proposed gift object", "6529NM-PG-2026-001", PROPOSAL_AT)]}, "medium": "photograph", "work_lifecycle_status": "selected_by_museum_wave_acquisition_review_in_progress", "current_museum_relation": {"museum_entity_id": institution, "relation_status": "selected_by_museum_wave", "as_of": WINNER_AT, "evidence_refs": [source_evidence("Signed-drop API WINNER status readback (is_signed=true)", WINNER_SOURCE_PATH, WINNER_AT), source_evidence("Museum Wave drop page readback", WINNER_SOURCE_URL, WINNER_AT)]}, "mint_fact": fact("not_started", WINNER_AT, ["6529NM-PG-2026-001", WINNER_OBSERVATION_ID], "The WINNER source status establishes Museum Wave selection and acquisition review only; it does not establish mint, payment, title, custody, rights, technical review, preservation, accession, or Collection membership."), "collection_membership": {"status": "not_in_collection", "collection_entity_id": None, "accession_entity_ids": [], "source_record_ids": ["6529NM-PG-2026-001", WINNER_OBSERVATION_ID], "evidence_refs": [source_evidence("WINNER has no accession effect", WINNER_SOURCE_PATH, WINNER_AT)]}, "project_or_series_entity_ids": [magnum_project], "acquisition_entity_ids": ["6529NM-CA-2026-003"], "program_entity_ids": [gift_program], "accession_entity_ids": [], "lifecycle_observations": [lifecycle_observation(fixed_observation_id(work_id, "proposed_in_museum_wave"), "proposed_in_museum_wave", "PARTICIPATORY", PROPOSAL_AT, ["6529NM-PG-2026-001"], "The original published proposal observation is retained as history and is not rewritten.", [source_evidence("Original PARTICIPATORY proposal observation", "records/proposed-gifts/6529NM-PG-2026-001/proposal.json", PROPOSAL_AT)]), lifecycle_observation(fixed_observation_id(work_id, "selected_by_museum_wave_acquisition_review_in_progress"), "selected_by_museum_wave_acquisition_review_in_progress", "WINNER", WINNER_AT, ["6529NM-PG-2026-001", WINNER_OBSERVATION_ID], "Signed-drop API WINNER status readback changes the Museum relationship to selection under acquisition review only; the five Works remain outside the permanent Collection.", [source_evidence("Signed-drop API WINNER status readback (is_signed=true)", WINNER_SOURCE_PATH, WINNER_AT), source_evidence("Museum Wave drop page readback", WINNER_SOURCE_URL, WINNER_AT)])], "component_references": [], "manifestation_references": [governed_typed_reference(identity_inventory, "manifestation", f"{candidate_id}.TOKEN", candidate_id, [source_evidence("Proposed ERC-721 manifestation reference", "6529NM-PG-2026-001", PROPOSAL_AT)], source_status="proposed")], "identity_boundary": "Work identity is independent of the proposed acquisition, candidate object alias, chain identity, token manifestation, and any later accession.", "evidence_refs": [source_evidence("Signed-drop API WINNER status readback (is_signed=true)", WINNER_SOURCE_PATH, WINNER_AT), source_evidence("Original proposal object", "6529NM-PG-2026-001", PROPOSAL_AT)],
        }, ["6529NM-PG-2026-001", candidate_id, "6529NM-CA-2026-003", magnum_project, agent_id], [source_evidence("Proposed gift object", "6529NM-PG-2026-001", PROPOSAL_AT)], media_entity_ids=[magnum_media_ids_by_candidate[candidate_id]])

    add_entity(magnum_project, "PROJECT_OR_SERIES", "Magnum Photos 75", slug_inventory[magnum_project]["public_slug"], slug_inventory[magnum_project]["canonical_route"], PROPOSAL_AT, {
        "profile_type": "PROJECT_OR_SERIES", "project_type": "series", "project_relation_basis": "proposal_work_set", "scope_statement": "Magnum Photos 75 was a 2022 anniversary project that brought photographs from the Magnum archive into a tokenized publication context. This record concerns the five Works selected for Museum acquisition review and preserves the distinction among the Project, each Work, its token manifestation, and the Museum's Curated Acquisition.", "agent_entity_ids": [magnum_org], "work_entity_ids": magnum_works, "ownership_boundary": "Magnum Photos 75 is a broader source project and tokenized release context, distinct from the Museum's Conflict at Its Edges Curated Acquisition and from each independent Work identity. Token manifestations and source media do not establish Museum title, custody, rights, or Collection membership.", "source_record_ids": ["6529NM-PG-2026-001", *magnum_work_source_ids], "evidence_refs": [source_evidence("Magnum Photos 75 research profile", "records/proposed-gifts/6529NM-PG-2026-001/public/scholarship/entities/magnum-photos-75.md", MAGNUM_PUBLICATION_AT), source_evidence("Five-work proposal set", "records/proposed-gifts/6529NM-PG-2026-001/proposal.json", PROPOSAL_AT)],
    }, [magnum_org, *magnum_works, "6529NM-PG-2026-001"], [source_evidence("Magnum Photos 75 research profile", "records/proposed-gifts/6529NM-PG-2026-001/public/scholarship/entities/magnum-photos-75.md", MAGNUM_PUBLICATION_AT), source_evidence("Five-work proposal set", "records/proposed-gifts/6529NM-PG-2026-001/proposal.json", PROPOSAL_AT)])

    acquisition_facts_casey = {"mint": fact("verified", CASEY_AT, ["6529NM-ACC-2026-001"], "Existing accession records contain the token identity and receipt evidence."), "payment": fact("not_applicable", CASEY_AT, ["6529NM.2026.001"], "The completed gift is recorded as a donation."), "title": fact("verified", CASEY_AT, ["6529NM-ACC-2026-001"], "Title binding is recorded separately and is not copyright."), "custody": fact("verified", CASEY_AT, ["6529NM-ACC-2026-001"], "Custody receipt is recorded separately."), "rights": fact("verified_with_conditions", CASEY_AT, ["6529NM.2026.001.RIGHTS.01"], "Rights are recorded per object with attribution and noncommercial conditions."), "technical": fact("verified_with_conditions", CASEY_AT, ["6529NM.2026.001.COND.01"], "Technical and condition review passed with conditions."), "preservation": fact("in_progress", CASEY_AT, ["6529NM.2026.001.DILIGENCE-01"], "Autonomous generator preservation remains active stewardship."), "display": fact("verified_with_conditions", CASEY_AT, ["6529NM.2026.001.COND.01"], "Display is ready with conditions where the object record says so.")}
    acquisition_facts_keys = {key: fact(status, KEYS_AT, [keys_program_source], note) for key, status, note in [("mint", "not_established", "No primary mint evidence is recorded."), ("payment", "planned", "Program terms describe a planned purchase price only."), ("title", "not_established", "No title binding is recorded."), ("custody", "unverified", "Planned custody reference is not custody evidence."), ("rights", "unverified", "Conditional program terms are not an effective rights grant."), ("technical", "not_started", "No completed technical review is recorded."), ("preservation", "not_started", "No preservation completion is recorded."), ("display", "not_started", "No display authorization is recorded.")]}
    acquisition_facts_proposal = {key: fact(status, PROPOSAL_AT, ["6529NM-PG-2026-001"], note) for key, status, note in [("mint", "verified", "The proposal source records candidate chain history, not Museum acquisition."), ("payment", "not_established", "No Museum purchase is recorded."), ("title", "not_established", "No Museum title binding is recorded."), ("custody", "unverified", "Observed external owner is not Museum custody."), ("rights", "unverified", "All Rights Reserved is retained as source fact."), ("technical", "pending_review", "Proposal-level technical evidence is not an accession review."), ("preservation", "not_started", "The upstream files are not Museum preservation objects."), ("display", "not_started", "Proposal presentation is not display authorization.")]}
    add_entity("6529NM-CA-2026-001", "CURATED_ACQUISITION", "The System in Seven States", "the-system-in-seven-states", "/museum/network/acquisitions/the-system-in-seven-states", CASEY_AT, {"profile_type": "CURATED_ACQUISITION", "title": "The System in Seven States", "thesis": "A Museum curatorial grouping reads seven accessioned Casey Reas works through related computational systems without claiming an artist-defined canonical group.", "acquisition_method": "donation", "program_or_pathway": {"kind": "acquisition_program", "entity_ids": [gift_program], "source_record_ids": institution_refs}, "work_entity_ids": casey_work_ids, "source_work_record_ids": [obj["record_id"] for obj in casey_objects], "lifecycle": {"status": "accessioned_into_permanent_collection", "as_of": CASEY_AT, "evidence_refs": [source_evidence("Accession certificate", "6529NM-ACC-2026-001", CASEY_AT)]}, "lifecycle_observations": [lifecycle_observation("6529NM-CA-OBS-0001", "accessioned_into_permanent_collection", "accessioned", CASEY_AT, ["6529NM-ACC-2026-001"], "The completed Casey donation is accessioned into the permanent Collection.")], "collection_effect": "permanent_collection", "independent_acquisition_facts": acquisition_facts_casey, "public_credit": "Gift of punk6529", "evidence_refs": [source_evidence("Casey accession lot", "6529NM.2026.001", CASEY_AT), evidence("Curated acquisition thesis", "records/accessions/6529NM.2026.001/public/curatorial-accession-review.md", CASEY_AT, "E")]}, [gift_program, accession, *casey_work_ids, *[obj["record_id"] for obj in casey_objects], "6529NM-ACC-2026-001"], [source_evidence("Casey accession lot", "6529NM.2026.001", CASEY_AT), evidence("Curated acquisition thesis", "records/accessions/6529NM.2026.001/public/curatorial-accession-review.md", CASEY_AT, "E")])
    add_entity("6529NM-CA-2026-002", "CURATED_ACQUISITION", "Keys and Gates", "keys-and-gates", "/museum/network/acquisitions/keys-and-gates", KEYS_AT, {"profile_type": "CURATED_ACQUISITION", "title": "Keys and Gates", "thesis": "The program\u2019s selected group brings together photographs of access, exclusion, permission, surveillance, custody, autonomy, and exit; selection is complete, while acquisition and minting remain pending.", "acquisition_method": "purchase", "program_or_pathway": {"kind": "acquisition_program", "entity_ids": [keys_program], "source_record_ids": [keys_program_source]}, "work_entity_ids": keys_work_ids, "source_work_record_ids": [row["record_id"] for row in outcomes], "lifecycle": {"status": "selected_through_acquisition_program_acquisition_pending", "as_of": KEYS_AT, "evidence_refs": [source_evidence("Keys and Gates selected-works index", keys_program_source, KEYS_AT)]}, "lifecycle_observations": [lifecycle_observation("6529NM-CA-OBS-0002", "selected_through_acquisition_program_acquisition_pending", "selected_unminted", KEYS_AT, [keys_program_source], "Keys and Gates remains selected through its acquisition program with acquisition pending.")], "collection_effect": "none", "independent_acquisition_facts": acquisition_facts_keys, "public_credit": "Selected through the Keys and Gates acquisition program; acquisition pending", "evidence_refs": [source_evidence("Keys and Gates program record", "records/programs/6529NM-AP-01/program.json", KEYS_AT), evidence("Curated acquisition thesis", "records/programs/6529NM-AP-01/program.json", KEYS_AT, "E")]}, [keys_program, keys_program_source, *keys_work_ids, *[row["record_id"] for row in outcomes]], [source_evidence("Keys and Gates program record", "records/programs/6529NM-AP-01/program.json", KEYS_AT), evidence("Curated acquisition thesis", "records/programs/6529NM-AP-01/program.json", KEYS_AT, "E")])
    add_entity("6529NM-CA-2026-003", "CURATED_ACQUISITION", "Conflict at Its Edges", "conflict-at-its-edges", "/museum/network/acquisitions/conflict-at-its-edges", WINNER_AT, {"profile_type": "CURATED_ACQUISITION", "title": "Conflict at Its Edges", "thesis": "Five photographs made between 1952 and 2016 approach conflict through borders, religious and domestic space, smoke, ruins, and the uncertain aftermath of violence. Presented together by the selected proposal across two Magnum Photos 75 curations, they form a Museum acquisition under review whose coherence lies in how each image tests what documentary evidence can show and what remains unresolved.", "acquisition_method": "donation", "program_or_pathway": {"kind": "acquisition_program", "entity_ids": [gift_program], "source_record_ids": ["6529NM-PG-2026-001", WINNER_OBSERVATION_ID]}, "work_entity_ids": magnum_works, "source_work_record_ids": ["6529NM-PG-2026-001", *magnum_work_source_ids], "lifecycle": {"status": "selected_by_museum_wave_acquisition_review_in_progress", "as_of": WINNER_AT, "evidence_refs": [source_evidence("Signed-drop API WINNER status readback (is_signed=true)", WINNER_SOURCE_PATH, WINNER_AT), source_evidence("Museum Wave drop page readback", WINNER_SOURCE_URL, WINNER_AT)]}, "lifecycle_observations": [lifecycle_observation("6529NM-CA-OBS-0003", "proposed_in_museum_wave", "PARTICIPATORY", PROPOSAL_AT, ["6529NM-PG-2026-001"], "The original PARTICIPATORY proposal observation remains part of the append-only lifecycle history.", [source_evidence("Original PARTICIPATORY proposal observation", "records/proposed-gifts/6529NM-PG-2026-001/proposal.json", PROPOSAL_AT)]), lifecycle_observation("6529NM-CA-OBS-0004", "selected_by_museum_wave_acquisition_review_in_progress", "WINNER", WINNER_AT, ["6529NM-PG-2026-001", WINNER_OBSERVATION_ID], "Signed-drop API WINNER status readback selects the proposed identity for Museum acquisition review only; it creates no accession or Collection membership.", [source_evidence("Signed-drop API WINNER status readback (is_signed=true)", WINNER_SOURCE_PATH, WINNER_AT), source_evidence("Museum Wave drop page readback", WINNER_SOURCE_URL, WINNER_AT)])], "collection_effect": "none", "independent_acquisition_facts": acquisition_facts_proposal, "public_credit": "Selected by the Museum Wave; acquisition review in progress", "evidence_refs": [source_evidence("Signed-drop API WINNER status readback (is_signed=true)", WINNER_SOURCE_PATH, WINNER_AT), source_evidence("Original proposed gift record", "6529NM-PG-2026-001", PROPOSAL_AT), evidence("Curated acquisition thesis", "records/proposed-gifts/6529NM-PG-2026-001/public/scholarship/essays/conflict-at-its-edges.md", MAGNUM_PUBLICATION_AT, "E")]}, ["6529NM-PG-2026-001", WINNER_OBSERVATION_ID, *magnum_works, *magnum_work_source_ids], [source_evidence("Signed-drop API WINNER status readback (is_signed=true)", WINNER_SOURCE_PATH, WINNER_AT), source_evidence("Original proposed gift record", "records/proposed-gifts/6529NM-PG-2026-001/proposal.json", PROPOSAL_AT), evidence("Curated acquisition thesis", "records/proposed-gifts/6529NM-PG-2026-001/public/scholarship/essays/conflict-at-its-edges.md", MAGNUM_PUBLICATION_AT, "E")], media_entity_ids=[media_derivative])
    magnum_essay_path = f"{MAGNUM_SCHOLARSHIP_ROOT}/essays/conflict-at-its-edges.md"
    add_entity(magnum_publication, "RESEARCH_PUBLICATION", "Conflict at Its Edges", "conflict-at-its-edges", "/museum/network/research/conflict-at-its-edges", MAGNUM_PUBLICATION_AT, {
        "profile_type": "RESEARCH_PUBLICATION", "publication_kind": "research_dossier", "title": "Conflict at Its Edges", "publication_date": "2026-08-09", "version": "1.0.0", "author_entity_ids": [institution], "subject_entity_ids": ["6529NM-CA-2026-003", magnum_org, magnum_project, *magnum_artist_ids, *magnum_works], "publication_document_uri": github_uri(MAGNUM_PUBLICATION_RECORD_PATH), "publication_component_paths": list(MAGNUM_PUBLICATION_COMPONENT_PATHS), "evidence_refs": [source_evidence("Conflict at Its Edges publication record", MAGNUM_PUBLICATION_RECORD_PATH, MAGNUM_PUBLICATION_AT), source_evidence("Conflict at Its Edges catalogue essay", magnum_essay_path, MAGNUM_PUBLICATION_AT)],
    }, ["6529NM-PG-2026-001", "6529NM-CA-2026-003", magnum_org, magnum_project, *magnum_artist_ids, *magnum_works], [source_evidence("Conflict at Its Edges publication record", MAGNUM_PUBLICATION_RECORD_PATH, MAGNUM_PUBLICATION_AT), source_evidence("Conflict at Its Edges catalogue essay", magnum_essay_path, MAGNUM_PUBLICATION_AT)])

    retained_path = ROOT / "evidence/casey-reas/manifest.json"
    derivative_path = ROOT / "records/proposed-gifts/6529NM-PG-2026-001/public/media/conflict-at-its-edges-cover.png"
    manifest = load_json(ROOT / "records/programs/6529NM-AP-01/media-manifest.json")
    wave_storm = load_json(ROOT / "records/proposed-gifts/6529NM-PG-2026-001/wave-storm.json")
    wave_publication_record = load_json(ROOT / WAVE_PUBLICATION_OBSERVATION_PATH)
    wave_publication = wave_publication_record["payload"]
    media_description_record = load_json(ROOT / MEDIA_DESCRIPTION_AMENDMENT_PATH)
    media_description_amendment = media_description_record["payload"]
    casey_media_amendment_record = load_json(ROOT / CASEY_MEDIA_AMENDMENT_PATH)
    casey_media_amendment = casey_media_amendment_record["payload"]
    casey_media_corrections = {
        item["object_id"]: item for item in casey_media_amendment["presentation_corrections"]
    }
    wave_media_by_candidate = {
        part.get("candidate_object_id"): part.get("media", [])[0]
        for part in wave_storm.get("parts", [])
        if part.get("candidate_object_id") and part.get("media")
    }
    wave_publication_by_candidate = {
        part["candidate_object_id"]: part
        for part in wave_publication["parts"]
        if part.get("candidate_object_id")
    }
    add_entity(media_retained, "MEDIA_REFERENCE", "Casey retained preservation evidence manifest", None, None, CASEY_AT, media_profile("museum_retained_preservation_object", github_uri("evidence/casey-reas/manifest.json"), "evidence/casey-reas/manifest.json", "application/json", False, None, None, None, "not_applicable", casey_work_ids_by_object["6529NM.2026.001.01"], "6529 Network Museum preservation evidence manifest", "cleared_with_conditions", "retrieved", ["6529NM.2026.001.01", "6529NM-ACC-2026-001"], CASEY_AT, {"status": "verified", "algorithm": "sha256", "digest": sha256_file(retained_path), "verified_at": GENERATED_AT, "basis": "Retrieved repository bytes hashed by the deterministic migration."}, ["view", "open_repository_path", "copy_citation"]), ["6529NM.2026.001.01", "6529NM-ACC-2026-001"] , [source_evidence("Retained evidence manifest", "evidence/casey-reas/manifest.json", CASEY_AT)])
    casey_first_object = casey_objects_by_id["6529NM.2026.001.01"]
    add_entity(media_token, "MEDIA_REFERENCE", "Casey token-linked metadata source", None, None, CASEY_AT, media_profile("token_linked_source_media", casey_first_object["chain_identity"]["metadata_uri"], None, "application/json", False, None, None, None, "not_applicable", casey_work_ids_by_object["6529NM.2026.001.01"], "Casey Reas, token-linked metadata source", "cleared_with_conditions", "retrieved", ["6529NM.2026.001.01", "6529NM.2026.001.RIGHTS.01"], CASEY_AT, {"status": "verified", "algorithm": "sha256", "digest": casey_first_object["chain_identity"]["metadata_sha256"], "verified_at": CASEY_AT, "basis": "Existing object record metadata snapshot fixity."}, ["view", "open_token_source", "copy_citation"]), ["6529NM.2026.001.01", "6529NM.2026.001.RIGHTS.01"], [source_evidence("Token-linked metadata record", "6529NM.2026.001.01", CASEY_AT)])
    for index, obj in enumerate(casey_objects):
        object_id = obj["record_id"]
        correction = casey_media_corrections[object_id]
        rights_id = correction["rights_record_id"]
        common_source_refs = [object_id, rights_id, "6529NM.2026.001.VO-01", CASEY_MEDIA_AMENDMENT_ID]
        rights_evidence_refs = [
            source_evidence("Casey per-object rights statement", rights_id, CASEY_AT),
            evidence("CC BY-NC 4.0 license", correction["license_url"], CASEY_AT, "D"),
        ]
        accessibility_evidence_refs = [
            source_evidence("Casey visual observation", "6529NM.2026.001.VO-01", CASEY_AT),
            source_evidence("Append-only Casey media presentation correction", CASEY_MEDIA_AMENDMENT_ID, CASEY_MEDIA_AT),
        ]
        still = correction["still"]
        still_dimensions = still["dimensions"]
        add_entity(casey_still_media_ids_by_object[object_id], "MEDIA_REFERENCE", f"{obj['title']} official Art Blocks still", None, None, CASEY_MEDIA_AT, media_profile(
            "token_linked_source_media",
            still["source_url"],
            None,
            still["media_type"],
            True,
            still_dimensions["width"],
            still_dimensions["height"],
            correction["accessibility_text"],
            "provided",
            casey_work_ids_by_object[object_id],
            correction["credit"],
            "cleared_with_conditions",
            "mutable_external",
            common_source_refs,
            CASEY_MEDIA_AT,
            {
                "status": "verified",
                "algorithm": "sha256",
                "digest": still["response_sha256"],
                "verified_at": CASEY_MEDIA_AT,
                "basis": "Verified only for the exact observed Art Blocks media-proxy image response at the recorded observation. The external locator remains mutable; future bytes may differ, and the observed response bytes were not retained as a Museum preservation master.",
            },
            still["allowed_ui_affordances"],
            rights_label="CC BY-NC 4.0",
            rights_evidence_refs=rights_evidence_refs,
            source_observation_evidence_refs=[
                evidence("Exact observed Art Blocks media-proxy image response", still["source_url"], CASEY_MEDIA_AT, "C"),
                source_evidence("Casey visual observation", "6529NM.2026.001.VO-01", CASEY_AT),
                source_evidence("Append-only Casey media presentation correction", CASEY_MEDIA_AMENDMENT_ID, CASEY_MEDIA_AT),
            ],
            accessibility_evidence_refs=accessibility_evidence_refs,
        ), common_source_refs, [source_evidence("Append-only Casey media presentation correction", CASEY_MEDIA_AMENDMENT_ID, CASEY_MEDIA_AT), source_evidence("Casey per-object rights statement", rights_id, CASEY_AT)])

        live = correction["live"]
        live_dimensions = live["observed_canvas_dimensions"]
        add_entity(casey_media_ids_by_object[obj["record_id"]], "MEDIA_REFERENCE", f"{obj['title']} official Art Blocks live generator", None, None, CASEY_MEDIA_AT, media_profile(
            "token_linked_source_media",
            live["source_url"],
            None,
            live["media_type"],
            True,
            live_dimensions["width"],
            live_dimensions["height"],
            live["accessibility_text"],
            "provided",
            casey_work_ids_by_object[object_id],
            correction["credit"],
            "cleared_with_conditions",
            "mutable_external",
            common_source_refs,
            CASEY_MEDIA_AT,
            {"status": "unverified_not_retrieved", "algorithm": None, "digest": None, "verified_at": None, "basis": "The official Art Blocks live generator is mutable external HTML. No digest is asserted for the generator or future responses, and the Museum retains observation evidence rather than generator response bytes."},
            live["allowed_ui_affordances"],
            rights_label="CC BY-NC 4.0",
            rights_evidence_refs=rights_evidence_refs,
            source_observation_evidence_refs=[
                source_evidence("Casey live generator observation", "6529NM.2026.001.VO-01", CASEY_AT),
                source_evidence("Append-only Casey media presentation correction", CASEY_MEDIA_AMENDMENT_ID, CASEY_MEDIA_AT),
            ],
            accessibility_evidence_refs=accessibility_evidence_refs,
        ), common_source_refs, [source_evidence("Append-only Casey media presentation correction", CASEY_MEDIA_AMENDMENT_ID, CASEY_MEDIA_AT), source_evidence("Casey per-object rights statement", rights_id, CASEY_AT)])
    signed_obj = proposal["objects"][0]
    wave_proposal_context = {
        "wave_id": wave_publication["wave_id"],
        "drop_id": wave_publication["drop_id"],
        "publication_record_id": "6529NM-PG-2026-001",
        "observation_record_id": WAVE_PUBLICATION_OBSERVATION_ID,
        "api_endpoint": wave_publication["api_endpoint"],
        "published_at": wave_publication["drop_created_at"],
        "publication_status": "historical_public_proposal_context",
    }
    first_receipt = wave_publication_by_candidate[signed_obj["candidate_object_id"]]
    add_entity(media_wave, "MEDIA_REFERENCE", "Conflict at Its Edges historical Wave proposal presentation source", None, None, PROPOSAL_AT, media_profile(
        "historical_wave_proposal_presentation",
        None,
        None,
        first_receipt["mime_type"],
        False,
        signed_obj["image"]["width"],
        signed_obj["image"]["height"],
        wave_media_by_candidate[signed_obj["candidate_object_id"]]["alt_text"],
        "provided",
        magnum_work_ids_by_candidate[signed_obj["candidate_object_id"]],
        first_receipt["credit"],
        "restricted",
        "mutable_external",
        ["6529NM-PG-2026-001", WAVE_PUBLICATION_OBSERVATION_ID],
        PROPOSAL_AT,
        {"status": "unverified_not_retrieved", "algorithm": None, "digest": None, "verified_at": None, "basis": "The signed-drop API readback records the Wave upload locator; the upload bytes were not independently retrieved in this projection."},
        ["alt_text", "open_wave_proposal_context", "copy_citation"],
        wave_proposal_context=wave_proposal_context,
        accessibility_subject_policy="non_identifying_sensitive_subject",
        publication_context_entity_ids=["6529NM-CA-2026-003"],
        token_source_locator=None,
        token_source_fixity=None,
        rights_label=first_receipt["rights_label"],
    ), ["6529NM-PG-2026-001", WAVE_PUBLICATION_OBSERVATION_ID, "6529NM-CA-2026-003"], [source_evidence("Historical public Wave proposal presentation", WAVE_PUBLICATION_OBSERVATION_ID, WINNER_AT)])
    for signed_obj in proposal["objects"][1:]:
        candidate_id = signed_obj["candidate_object_id"]
        wave_media = wave_media_by_candidate[candidate_id]
        receipt = wave_publication_by_candidate[candidate_id]
        if candidate_id == "6529NM-PG-2026-001.OBJ-003":
            accessibility_text = media_description_amendment["current_accessibility_text"]
        elif candidate_id == "6529NM-PG-2026-001.OBJ-004":
            accessibility_text = "Black-and-white photograph of an apparently young person standing with head lowered before a white wall marked by many dark spots, beneath a caged lamp."
        else:
            accessibility_text = wave_media["alt_text"]
        media_source_refs = ["6529NM-PG-2026-001", WAVE_PUBLICATION_OBSERVATION_ID]
        if candidate_id == "6529NM-PG-2026-001.OBJ-003":
            media_source_refs.append(MEDIA_DESCRIPTION_AMENDMENT_ID)
        add_entity(magnum_media_ids_by_candidate[signed_obj["candidate_object_id"]], "MEDIA_REFERENCE", f"{signed_obj['title']} historical Wave proposal presentation source", None, None, PROPOSAL_AT, media_profile(
            "historical_wave_proposal_presentation",
            None,
            None,
            receipt["mime_type"],
            False,
            signed_obj["image"]["width"],
            signed_obj["image"]["height"],
            accessibility_text,
            "provided",
            magnum_work_ids_by_candidate[candidate_id],
            receipt["credit"],
            "restricted",
            "mutable_external",
            media_source_refs,
            PROPOSAL_AT,
            {"status": "unverified_not_retrieved", "algorithm": None, "digest": None, "verified_at": None, "basis": "The signed-drop API readback records the Wave upload locator; the upload bytes were not independently retrieved in this projection."},
            ["alt_text", "open_wave_proposal_context", "copy_citation"],
            wave_proposal_context=wave_proposal_context,
            accessibility_subject_policy="non_identifying_apparently_young_subject" if candidate_id == "6529NM-PG-2026-001.OBJ-004" else "non_identifying_sensitive_subject",
            identity_inference_prohibition={"status": "prohibited", "scope": "subject_identity_and_age_classification", "reason": "Do not infer or publish the subject's identity or age classification from this historical proposal image."} if candidate_id == "6529NM-PG-2026-001.OBJ-004" else None,
            publication_context_entity_ids=["6529NM-CA-2026-003"],
            token_source_locator=None,
            token_source_fixity=None,
            rights_label=receipt["rights_label"],
        ), [*media_source_refs, "6529NM-CA-2026-003"], [source_evidence("Historical public Wave proposal presentation", WAVE_PUBLICATION_OBSERVATION_ID, WINNER_AT)])
    width = 1600
    cover_accessibility_text = "Black, blue, and white square graphic with the printed words PROPOSED GIFT, CONFLICT AT ITS EDGES, Five Photographs of Evidence and Aftermath, 1952–2016, and 6529 NETWORK MUSEUM."
    add_entity(media_derivative, "MEDIA_REFERENCE", "Conflict at Its Edges historical proposal cover graphic", None, None, PROPOSAL_AT, media_profile("museum_authored_public_graphic", github_uri("records/proposed-gifts/6529NM-PG-2026-001/public/media/conflict-at-its-edges-cover.png"), "records/proposed-gifts/6529NM-PG-2026-001/public/media/conflict-at-its-edges-cover.png", "image/png", True, width, width, "Black, blue, and white square graphic with the printed words PROPOSED GIFT, CONFLICT AT ITS EDGES, Five Photographs of Evidence and Aftermath, 1952–2016, and 6529 NETWORK MUSEUM.", "provided", "6529NM-CA-2026-003", "6529 Network Museum, Conflict at Its Edges proposal cover, 2026.", "cleared", "retrieved", ["6529NM-PG-2026-001", WAVE_PUBLICATION_OBSERVATION_ID, "6529NM-CA-2026-003"], PROPOSAL_AT, {"status": "verified", "algorithm": "sha256", "digest": sha256_file(derivative_path), "verified_at": GENERATED_AT, "basis": "Retrieved Museum-authored repository bytes hashed by the deterministic migration."}, ["view", "thumbnail", "alt_text", "open_repository_path", "copy_citation"], transform="Museum-authored text-only historical proposal graphic; independently authored, not derived from a source photograph, and not a selected-acquisition hero.", rights_label="CC0-1.0", rights_evidence_refs=[evidence("Wave publication cover rights label", WAVE_PUBLICATION_OBSERVATION_ID, WINNER_AT, "B"), evidence("Museum-authored cover bytes and fixity", "records/proposed-gifts/6529NM-PG-2026-001/public/media/conflict-at-its-edges-cover.png", PROPOSAL_AT, "C")], source_observation_evidence_refs=[evidence("Museum-authored cover bytes and fixity", "records/proposed-gifts/6529NM-PG-2026-001/public/media/conflict-at-its-edges-cover.png", PROPOSAL_AT, "C")]), ["6529NM-PG-2026-001", WAVE_PUBLICATION_OBSERVATION_ID, "6529NM-CA-2026-003"], [source_evidence("Museum-authored proposal cover", "records/proposed-gifts/6529NM-PG-2026-001/public/media/conflict-at-its-edges-cover.png", PROPOSAL_AT)])

    keys_media_withdrawal = "records/programs/6529NM-AP-01/public/media-delivery-withdrawal-amendment-2026-08-09.md"
    for index, item in enumerate(manifest["items"]):
        outcome_id = item["record_id"]
        outcome = outcomes_by_id[outcome_id]
        add_entity(keys_media_ids_by_outcome[outcome_id], "MEDIA_REFERENCE", f"{outcome['title']} presentation record", None, None, KEYS_MEDIA_WITHDRAWAL_AT, media_profile(
            "museum_generated_public_derivative",
            None,
            None,
            "image/webp",
            False,
            None,
            None,
            item["presentation"]["alt_text"],
            "pending_review",
            keys_work_ids_by_outcome[outcome_id],
            f"{outcome['artist']} — {outcome['title']}; Keys and Gates presentation record",
            "unknown",
            "source_declared",
            [outcome_id, keys_program_source],
            KEYS_MEDIA_WITHDRAWAL_AT,
            {"status": "unverified_not_retrieved", "algorithm": None, "digest": None, "verified_at": None, "basis": "The active publication withholds every presentation derivative; prior fixity remains in the source history and withdrawal amendment."},
            ["alt_text", "copy_citation"],
            transform=manifest["transform"]["profile"],
            source_observation_evidence_refs=[source_evidence("Keys and Gates active media manifest", "records/programs/6529NM-AP-01/media-manifest.json", KEYS_MEDIA_WITHDRAWAL_AT), source_evidence("Keys and Gates media withdrawal", keys_media_withdrawal, KEYS_MEDIA_WITHDRAWAL_AT)],
            rights_evidence_refs=[source_evidence("Keys and Gates outcome rights statement", outcome_id, KEYS_AT), source_evidence("Keys and Gates media withdrawal", keys_media_withdrawal, KEYS_MEDIA_WITHDRAWAL_AT)],
            accessibility_evidence_refs=[source_evidence("Keys and Gates accessibility record", "media/programs/6529NM-AP-01/accessibility.json", KEYS_MEDIA_WITHDRAWAL_AT)],
        ), [outcome_id, keys_program_source], [source_evidence("Keys and Gates non-delivering presentation record", keys_media_withdrawal, KEYS_MEDIA_WITHDRAWAL_AT)])

    add_relation("6529NM-REL-0001", "INSTITUTION_HOLDS_COLLECTION", institution, collection, {}, CASEY_AT, institution_refs, [source_evidence("Institution collection relation", "6529NM.2026.001", CASEY_AT)])
    for index, work_id in enumerate(casey_work_ids):
        add_relation(f"6529NM-REL-{2 + index:04d}", "ARTIST_CREATES_WORK", casey_artist, work_id, {"role": "creator"}, CASEY_AT, [casey_objects[index]["record_id"]], [source_evidence("Casey object creator", casey_objects[index]["record_id"], CASEY_AT)])
    relation_number = 9
    for outcome_id, work_id in keys_work_ids_by_outcome.items():
        add_relation(f"6529NM-REL-{relation_number:04d}", "ARTIST_CREATES_WORK", keys_artist_ids_by_outcome[outcome_id], work_id, {"role": "creator"}, KEYS_AT, [outcome_id], [source_evidence("Keys and Gates artist creator", outcome_id, KEYS_AT)])
        relation_number += 1
    for candidate_id in magnum_work_source_ids:
        work_id = magnum_work_ids_by_candidate[candidate_id]
        add_relation(f"6529NM-REL-{relation_number:04d}", "ARTIST_CREATES_WORK", magnum_artist_ids_by_candidate[candidate_id], work_id, {"role": "creator"}, PROPOSAL_AT, [candidate_id], [source_evidence("Proposed artist creator", "6529NM-PG-2026-001", PROPOSAL_AT)])
        relation_number += 1
    for project_name, project_id in projects.items():
        project_objects = [obj for obj in casey_objects if obj.get("project", {}).get("name") == project_name]
        project_source_ids = [obj["record_id"] for obj in project_objects] or ["6529NM.2026.001"]
        add_relation(f"6529NM-REL-{relation_number:04d}", "AGENT_PLAYS_ROLE", casey_artist, project_id, {"role": "creator"}, CASEY_AT, project_source_ids, [source_evidence("Casey project agent source", project_source_ids[0], CASEY_AT)])
        relation_number += 1
    for project_name, project_id in projects.items():
        for obj in [item for item in casey_objects if item.get("project", {}).get("name") == project_name]:
            object_id = obj["record_id"]
            work_id = casey_work_ids_by_object[object_id]
            add_relation(f"6529NM-REL-{relation_number:04d}", "PROJECT_CONTEXTUALIZES_WORK", project_id, work_id, {"scope": "source_project"}, CASEY_AT, [object_id], [source_evidence("Casey project context", object_id, CASEY_AT)])
            relation_number += 1
        add_relation(f"6529NM-REL-{relation_number:04d}", "ORGANIZATION_PUBLISHES_PROJECT", art_blocks, project_id, {"role": "publisher"}, CASEY_AT, ["6529NM.2026.001.01"], [source_evidence("Art Blocks project publishing context", "6529NM.2026.001.01", CASEY_AT)])
        relation_number += 1
    magnum_project_source_paths_by_candidate = MAGNUM_WORK_PUBLICATION_PATHS
    for candidate_id in magnum_work_source_ids:
        work_id = magnum_work_ids_by_candidate[candidate_id]
        source_path = magnum_project_source_paths_by_candidate[candidate_id]
        add_relation(f"6529NM-REL-{relation_number:04d}", "PROJECT_CONTEXTUALIZES_WORK", magnum_project, work_id, {"scope": "proposal_work_set"}, PROPOSAL_AT, [candidate_id, "6529NM-PG-2026-001"], [source_evidence("Magnum Photos 75 project context", source_path, PROPOSAL_AT)])
        relation_number += 1
    add_relation(f"6529NM-REL-{relation_number:04d}", "ORGANIZATION_ORIGINATES_PROJECT", magnum_org, magnum_project, {"role": "originator"}, PROPOSAL_AT, ["6529NM-PG-2026-001"], [source_evidence("Magnum Photos 75 project origin", f"{MAGNUM_SCHOLARSHIP_ROOT}/entities/magnum-photos-75.md", MAGNUM_PUBLICATION_AT)])
    relation_number += 1
    add_relation(f"6529NM-REL-{relation_number:04d}", "ACQUISITION_PROGRAM_PRODUCES_ACQUISITION", gift_program, "6529NM-CA-2026-001", {}, CASEY_AT, institution_refs, [source_evidence("Gift pathway", "6529NM-GOV-1052812", CASEY_AT)])
    relation_number += 1
    add_relation(f"6529NM-REL-{relation_number:04d}", "ACQUISITION_PROGRAM_PRODUCES_ACQUISITION", gift_program, "6529NM-CA-2026-003", {}, WINNER_AT, ["6529NM-PG-2026-001", WINNER_OBSERVATION_ID], [source_evidence("Gift pathway for selected proposal", "6529NM-PG-2026-001", PROPOSAL_AT), source_evidence("Museum Wave selection observation", WINNER_SOURCE_PATH, WINNER_AT)])
    relation_number += 1
    add_relation(f"6529NM-REL-{relation_number:04d}", "ACQUISITION_PROGRAM_PRODUCES_ACQUISITION", keys_program, "6529NM-CA-2026-002", {}, KEYS_AT, [keys_program_source], [source_evidence("Keys and Gates program", keys_program_source, KEYS_AT)])
    relation_number += 1
    for index, work_id in enumerate(casey_work_ids):
        add_relation(f"6529NM-REL-{relation_number:04d}", "CURATED_ACQUISITION_BRINGS_TOGETHER_WORK", "6529NM-CA-2026-001", work_id, {"display_order": index + 1, "selection_status": "selected", "scope": "museum_curatorial_grouping"}, CASEY_AT, [casey_objects[index]["record_id"]], [source_evidence("Casey curated acquisition", casey_objects[index]["record_id"], CASEY_AT)])
        relation_number += 1
    for index, work_id in enumerate(keys_work_ids):
        outcome_id = outcomes[index]["record_id"]
        add_relation(f"6529NM-REL-{relation_number:04d}", "CURATED_ACQUISITION_BRINGS_TOGETHER_WORK", "6529NM-CA-2026-002", work_id, {"display_order": index + 1, "selection_status": "selected_unminted", "scope": "source_project"}, KEYS_AT, [outcome_id], [source_evidence("Keys and Gates selected outcome", outcome_id, KEYS_AT)])
        relation_number += 1
        add_relation(f"6529NM-REL-{relation_number:04d}", "PROGRAM_SELECTS_WORK", keys_program, work_id, {"display_order": index + 1, "selection_status": "selected_unminted", "mint_status": "pending"}, KEYS_AT, [outcome_id], [source_evidence("Keys and Gates selected outcome", outcome_id, KEYS_AT)])
        relation_number += 1
    for index, work_id in enumerate(magnum_works):
        add_relation(f"6529NM-REL-{relation_number:04d}", "CURATED_ACQUISITION_BRINGS_TOGETHER_WORK", "6529NM-CA-2026-003", work_id, {"display_order": index + 1, "selection_status": "selected", "scope": "proposal_work_set"}, WINNER_AT, ["6529NM-PG-2026-001", WINNER_OBSERVATION_ID], [source_evidence("Published proposal work set", "6529NM-PG-2026-001", PROPOSAL_AT), source_evidence("Museum Wave selection observation", WINNER_SOURCE_PATH, WINNER_AT)])
        relation_number += 1
    for index, work_id in enumerate(casey_work_ids):
        object_id = casey_objects[index]["record_id"]
        add_relation(f"6529NM-REL-{relation_number:04d}", "ACCESSION_ADMITS_WORK", accession, work_id, {"accession_object_id": object_id}, CASEY_AT, ["6529NM-ACC-2026-001", object_id], [source_evidence("Accession certificate", "6529NM-ACC-2026-001", CASEY_AT)])
        relation_number += 1
        add_relation(f"6529NM-REL-{relation_number:04d}", "COLLECTION_CONTAINS_WORK", collection, work_id, {"collection_membership_status": "permanent_collection"}, CASEY_AT, ["6529NM-ACC-2026-001", object_id], [source_evidence("Collection accession relation", "6529NM-ACC-2026-001", CASEY_AT)])
        relation_number += 1
    for target in ["6529NM-CA-2026-001", *projects.values(), *casey_work_ids]:
        add_relation(f"6529NM-REL-{relation_number:04d}", "PUBLICATION_INTERPRETS_ENTITY", publication, target, {"role": "subject"}, CASEY_AT, ["6529NM.2026.001"], [source_evidence("The System in Seven States", "records/accessions/6529NM.2026.001/public/casey-reas-collection-essay.md", CASEY_AT)])
        relation_number += 1
    add_relation(f"6529NM-REL-{relation_number:04d}", "INSTITUTION_PUBLISHES_PUBLICATION", institution, publication, {}, CASEY_AT, ["6529NM.2026.001"], [source_evidence("Published collection essay", "records/accessions/6529NM.2026.001/public/casey-reas-collection-essay.md", CASEY_AT)])
    relation_number += 1
    for target in ["6529NM-CA-2026-002", *keys_work_ids, *keys_artist_ids]:
        add_relation(f"6529NM-REL-{relation_number:04d}", "PUBLICATION_INTERPRETS_ENTITY", keys_publication, target, {"role": "subject"}, KEYS_PUBLICATION_AT, [keys_program_source, target], [source_evidence("Keys and Gates Research Publication", keys_essay_path, KEYS_PUBLICATION_AT)])
        relation_number += 1
    add_relation(f"6529NM-REL-{relation_number:04d}", "INSTITUTION_PUBLISHES_PUBLICATION", institution, keys_publication, {}, KEYS_PUBLICATION_AT, [keys_program_source, keys_publication], [source_evidence("Keys and Gates Research Publication", keys_essay_path, KEYS_PUBLICATION_AT)])
    relation_number += 1
    for target in ["6529NM-CA-2026-003", magnum_org, magnum_project, *magnum_artist_ids, *magnum_works]:
        add_relation(f"6529NM-REL-{relation_number:04d}", "PUBLICATION_INTERPRETS_ENTITY", magnum_publication, target, {"role": "subject"}, MAGNUM_PUBLICATION_AT, ["6529NM-PG-2026-001", target], [source_evidence("Conflict at Its Edges Research Publication", MAGNUM_PUBLICATION_RECORD_PATH, MAGNUM_PUBLICATION_AT)])
        relation_number += 1
    add_relation(f"6529NM-REL-{relation_number:04d}", "INSTITUTION_PUBLISHES_PUBLICATION", institution, magnum_publication, {}, MAGNUM_PUBLICATION_AT, ["6529NM-PG-2026-001", magnum_publication], [source_evidence("Conflict at Its Edges Research Publication", MAGNUM_PUBLICATION_RECORD_PATH, MAGNUM_PUBLICATION_AT)])
    relation_number += 1
    for source, target, context, refs, observed, publication_context in [(casey_work_ids_by_object[casey_object_ids[0]], media_retained, "preservation", ["6529NM-ACC-2026-001"], CASEY_AT, None), (casey_work_ids_by_object[casey_object_ids[0]], media_token, "source", ["6529NM.2026.001.01"], CASEY_AT, None), (magnum_work_ids_by_candidate[first_magnum_candidate], media_wave, "source", ["6529NM-PG-2026-001"], PROPOSAL_AT, "6529NM-CA-2026-003"), ("6529NM-CA-2026-003", media_derivative, "documentation", ["6529NM-PG-2026-001", "6529NM-CA-2026-003"], PROPOSAL_AT, "6529NM-CA-2026-003")]:
        qualifier = {"media_context": context}
        if publication_context is not None:
            qualifier["publication_context_entity_id"] = publication_context
        add_relation(f"6529NM-REL-{relation_number:04d}", "ENTITY_HAS_MEDIA", source, target, qualifier, observed, refs, [source_evidence("Typed media relation", refs[0], observed)])
        relation_number += 1
    for index, work_id in enumerate(casey_work_ids):
        object_id = casey_objects[index]["record_id"]
        rights_id = casey_media_corrections[object_id]["rights_record_id"]
        add_relation(f"6529NM-REL-{relation_number:04d}", "ENTITY_HAS_MEDIA", work_id, casey_media_ids_by_object[object_id], {"media_context": "primary", "display_order": 2}, CASEY_MEDIA_AT, [object_id, rights_id, "6529NM.2026.001.VO-01", CASEY_MEDIA_AMENDMENT_ID], [source_evidence("Append-only Casey live presentation relation correction", CASEY_MEDIA_AMENDMENT_ID, CASEY_MEDIA_AT)])
        relation_number += 1
    for index, work_id in enumerate(keys_work_ids):
        outcome_id = outcomes[index]["record_id"]
        add_relation(f"6529NM-REL-{relation_number:04d}", "ENTITY_HAS_MEDIA", work_id, keys_media_ids_by_outcome[outcome_id], {"media_context": "documentation"}, KEYS_AT, [outcome_id], [source_evidence("Keys and Gates Work presentation-record relation", outcome_id, KEYS_AT)])
        relation_number += 1
    for candidate_id in magnum_work_source_ids[1:]:
        work_id = magnum_work_ids_by_candidate[candidate_id]
        add_relation(f"6529NM-REL-{relation_number:04d}", "ENTITY_HAS_MEDIA", work_id, magnum_media_ids_by_candidate[candidate_id], {"media_context": "source", "publication_context_entity_id": "6529NM-CA-2026-003"}, PROPOSAL_AT, [candidate_id, "6529NM-CA-2026-003"], [source_evidence("Historical public Wave proposal media relation", "records/proposed-gifts/6529NM-PG-2026-001/wave-storm.json", PROPOSAL_AT)])
        relation_number += 1
    for index, work_id in enumerate(casey_work_ids):
        object_id = casey_objects[index]["record_id"]
        rights_id = casey_media_corrections[object_id]["rights_record_id"]
        add_relation(f"6529NM-REL-{relation_number:04d}", "ENTITY_HAS_MEDIA", work_id, casey_still_media_ids_by_object[object_id], {"media_context": "primary", "display_order": 1}, CASEY_MEDIA_AT, [object_id, rights_id, "6529NM.2026.001.VO-01", CASEY_MEDIA_AMENDMENT_ID], [source_evidence("Append-only Casey primary still relation", CASEY_MEDIA_AMENDMENT_ID, CASEY_MEDIA_AT)])
        relation_number += 1
    generated_entities = [record["payload"] for relative, record in records.items() if relative.startswith("records/entities/")]
    actual_entity_types = {payload["entity_type"] for payload in generated_entities}
    if actual_entity_types != set(IDENTITY_BINDING_ENTITY_TYPES):
        raise ValueError(
            "public entity type inventory mismatch: "
            f"missing={sorted(set(IDENTITY_BINDING_ENTITY_TYPES) - actual_entity_types)}, "
            f"undeclared={sorted(actual_entity_types - set(IDENTITY_BINDING_ENTITY_TYPES))}"
        )
    for binding_type in IDENTITY_BINDING_ENTITY_TYPES:
        actual_ids = {payload["entity_id"] for payload in generated_entities if payload.get("entity_type") == binding_type}
        expected_ids = set(identity_indexes[binding_type].values())
        if actual_ids != expected_ids:
            raise ValueError(f"{binding_type} identity inventory mismatch: missing={sorted(expected_ids - actual_ids)}, unused={sorted(actual_ids - expected_ids)}")
    actual_observation_ids = {
        observation["observation_id"]
        for payload in generated_entities
        if payload.get("entity_type") == "WORK"
        for observation in payload.get("profile", {}).get("lifecycle_observations", [])
        if isinstance(observation, dict) and isinstance(observation.get("observation_id"), str)
    }
    expected_observation_ids = set(identity_indexes["WORK_LIFECYCLE_OBSERVATION"].values())
    if actual_observation_ids != expected_observation_ids:
        raise ValueError(f"WORK_LIFECYCLE_OBSERVATION identity inventory mismatch: missing={sorted(expected_observation_ids - actual_observation_ids)}, unused={sorted(actual_observation_ids - expected_observation_ids)}")
    for obj in proposal["objects"]:
        media_relative = f"records/entities/{magnum_media_ids_by_candidate[obj['candidate_object_id']]}.json"
        media_record = records[media_relative]
        media_payload = media_record["payload"]
        media_payload["preferred_label"] = f"{obj['title']} historical Wave proposal presentation source"
        media = media_payload["profile"]["media"]
        media["source_observation"]["status"] = "mutable_external"
        wave_rights_evidence = [source_evidence("Signed-drop API rights-context readback", WAVE_PUBLICATION_OBSERVATION_ID, WINNER_AT)]
        wave_source_evidence = [source_evidence("Historical Wave presentation locator observation", WAVE_PUBLICATION_OBSERVATION_ID, WINNER_AT)]
        media["rights"]["evidence_refs"] = wave_rights_evidence
        media["source_observation"]["evidence_refs"] = wave_source_evidence
        if obj["candidate_object_id"] == "6529NM-PG-2026-001.OBJ-003":
            media["accessibility_evidence_refs"] = [
                source_evidence("Museum direct visual observation recorded in the media-description amendment", MEDIA_DESCRIPTION_AMENDMENT_ID, DIRECT_VISUAL_AT)
            ]
        else:
            media["accessibility_evidence_refs"] = [source_evidence("Historical Wave presentation accessibility source", WAVE_PUBLICATION_OBSERVATION_ID, WINNER_AT)]
        records[media_relative] = finish(media_payload, media_relative)

    # The proposal cover is an independently authored historical graphic. Its
    # CC0 basis is the Wave part-1 rights declaration plus retained repository
    # bytes; the acquisition is context, never license evidence.
    cover_relative = f"records/entities/{media_derivative}.json"
    cover_record = records[cover_relative]
    cover_media = cover_record["payload"]["profile"]["media"]
    cover_media["accessibility_text"] = cover_accessibility_text
    cover_media["rights"]["evidence_refs"] = [source_evidence("Wave part-1 rights declaration", WAVE_PUBLICATION_OBSERVATION_ID, WINNER_AT)]
    cover_media["source_observation"]["evidence_refs"] = [source_evidence("Retrieved Museum-authored cover bytes", "records/proposed-gifts/6529NM-PG-2026-001/public/media/conflict-at-its-edges-cover.png", GENERATED_AT)]
    cover_media["accessibility_evidence_refs"] = [source_evidence("Retrieved Museum-authored cover bytes for accessibility", "records/proposed-gifts/6529NM-PG-2026-001/public/media/conflict-at-its-edges-cover.png", GENERATED_AT)]
    cover_media["source_record_ids"] = ["6529NM-PG-2026-001", WAVE_PUBLICATION_OBSERVATION_ID]
    records[cover_relative] = finish(cover_record["payload"], cover_relative)

    # The retained proposal contains finalized Ethereum verification for all
    # five Magnum objects. Replace the provisional construction fact with the
    # explicit A-class chain observation before returning the envelope.
    for work_id in magnum_works:
        relative = f"records/entities/{work_id}.json"
        record = records[relative]
        record["payload"]["profile"]["mint_fact"] = fact(
            "verified",
            MAGNUM_CHAIN_AT,
            ["6529NM-PG-2026-001"],
            "Finalized Ethereum chain observation proves an existing external ERC-721 token manifestation only; it does not establish Museum acquisition, title, custody, rights, accession, or Collection membership.",
            evidence_refs=[evidence("Finalized Ethereum chain observation", WINNER_SOURCE_URL, MAGNUM_CHAIN_AT, "A")],
        )
        records[relative] = finish(record["payload"], relative)

    # Keep the acquisition-level mint fact aligned with the same independent
    # chain evidence while retaining all Museum acquisition gates separately.
    ca3_relative = "records/entities/6529NM-CA-2026-003.json"
    ca3_record = records[ca3_relative]
    ca3_record["payload"]["profile"]["independent_acquisition_facts"]["mint"] = fact(
        "verified",
        MAGNUM_CHAIN_AT,
        ["6529NM-PG-2026-001"],
        "Finalized Ethereum chain observation proves an existing external ERC-721 token manifestation only; it does not establish Museum acquisition, title, custody, rights, accession, or Collection membership.",
        evidence_refs=[evidence("Finalized Ethereum chain observation", WINNER_SOURCE_URL, MAGNUM_CHAIN_AT, "A")],
    )
    records[ca3_relative] = finish(ca3_record["payload"], ca3_relative)

    if used_relation_keys != set(relation_indexes):
        raise ValueError(f"relation identity inventory mismatch: missing={sorted(set(relation_indexes) - used_relation_keys)}, unused={sorted(used_relation_keys - set(relation_indexes))}")
    verify_evidence_paths(records)
    return records


def generated_directory_issues(
    records: dict[str, dict[str, Any]],
    entities_dir: Path = ENTITIES_DIR,
    relations_dir: Path = RELATIONS_DIR,
) -> tuple[list[str], list[str]]:
    """Classify exact-inventory mismatches for generator-owned JSON directories.

    The migration is intentionally append-only with respect to source records,
    but the generated projection itself must not retain retired entity or
    relation files. This helper compares the expected flat/generated paths to
    every JSON file below the two generator-owned directories. It never removes
    anything. The first result is unexpected stale JSON (write-fatal); the
    second is missing expected JSON (check-fatal but write-repairable).
    """

    def actual_paths(directory: Path, prefix: str) -> set[str]:
        if not directory.is_dir():
            return set()
        return {
            f"{prefix}/{path.relative_to(directory).as_posix()}"
            for path in directory.rglob("*.json")
            if path.is_file()
        }

    expected_entities = {relative for relative in records if relative.startswith("records/entities/")}
    expected_relations = {relative for relative in records if relative.startswith("records/relations/")}
    actual_entities = actual_paths(entities_dir, "records/entities")
    actual_relations = actual_paths(relations_dir, "records/relations")
    unexpected: list[str] = []
    missing: list[str] = []
    for relative in sorted(actual_entities - expected_entities):
        unexpected.append(f"unexpected generated JSON: {relative}")
    for relative in sorted(expected_entities - actual_entities):
        missing.append(f"missing generated JSON: {relative}")
    for relative in sorted(actual_relations - expected_relations):
        unexpected.append(f"unexpected generated JSON: {relative}")
    for relative in sorted(expected_relations - actual_relations):
        missing.append(f"missing generated JSON: {relative}")
    return unexpected, missing


def infer_existing_review_arguments(
    records: dict[str, dict[str, Any]],
    *,
    root: Path = ROOT,
) -> dict[str, Any]:
    """Derive one internally consistent generator mode from committed records.

    This is a deterministic replay aid, not an approval mechanism. Independent
    review authority remains enforced by the A-to-B catalog transition.
    """

    pending_paths: list[str] = []
    reviewed_bindings: list[tuple[str, str, str, str, str]] = []
    for relative in sorted(records):
        source = root / relative
        if not source.is_file():
            continue
        try:
            record = load_json(source)
        except (OSError, UnicodeError, json.JSONDecodeError, DuplicateJsonKeyError) as exc:
            raise ValueError(f"cannot read existing generated record {relative}: {exc}") from exc
        payload = record.get("payload") if isinstance(record, dict) else None
        if not isinstance(payload, dict):
            raise ValueError(f"existing generated record has no payload: {relative}")
        record_status = payload.get("record_status")
        review_status = payload.get("review_status")
        reviewer = payload.get("reviewer")
        if (
            record_status == "review_pending"
            and review_status in {"pending_independent_review", "review_pending"}
            and reviewer is None
        ):
            pending_paths.append(relative)
            continue
        if record_status != "reviewed" or review_status != "reviewed" or not isinstance(reviewer, dict):
            raise ValueError(f"existing generated record has an unsupported review state: {relative}")
        required = {
            "id",
            "role",
            "reviewed_at",
            "reviewed_commit",
            "reviewed_manifest_sha256",
            "reviewed_manifest_keccak",
            "reviewer_ids",
            "outcome",
        }
        if set(reviewer) != required or reviewer.get("role") != "reviewer" or reviewer.get("outcome") != "approved":
            raise ValueError(f"existing generated record has incomplete reviewer metadata: {relative}")
        reviewer_id = reviewer.get("id")
        reviewer_ids = reviewer.get("reviewer_ids")
        if reviewer_ids != [reviewer_id] or not isinstance(reviewer_id, str) or not reviewer_id:
            raise ValueError(f"existing generated record has an unsupported reviewer panel: {relative}")
        binding = (
            reviewer_id,
            reviewer.get("reviewed_at"),
            reviewer.get("reviewed_commit"),
            reviewer.get("reviewed_manifest_sha256"),
            reviewer.get("reviewed_manifest_keccak"),
        )
        if not all(isinstance(value, str) for value in binding):
            raise ValueError(f"existing generated record has non-string reviewer metadata: {relative}")
        if (
            not re.fullmatch(r"[0-9a-f]{40}", binding[2])
            or not re.fullmatch(r"sha256:[0-9a-f]{64}", binding[3])
            or not re.fullmatch(r"0x[0-9a-f]{64}", binding[4])
        ):
            raise ValueError(f"existing generated record has invalid reviewer commitments: {relative}")
        try:
            review_time = datetime.datetime.fromisoformat(binding[1].replace("Z", "+00:00"))
        except ValueError as exc:
            raise ValueError(f"existing generated record has an invalid review time: {relative}") from exc
        if review_time.tzinfo is None:
            raise ValueError(f"existing generated record has a review time without an offset: {relative}")
        created_at_value = payload.get("created_at")
        if not isinstance(created_at_value, str):
            raise ValueError(f"existing generated record has no construction time: {relative}")
        try:
            created_at = datetime.datetime.fromisoformat(created_at_value.replace("Z", "+00:00"))
        except ValueError as exc:
            raise ValueError(f"existing generated record has an invalid construction time: {relative}") from exc
        if created_at.tzinfo is None or review_time <= created_at:
            raise ValueError(f"existing generated record has a review time at or before construction: {relative}")
        reviewed_bindings.append(binding)

    if pending_paths and reviewed_bindings:
        raise ValueError("existing generated records mix pending and reviewed states")
    if not reviewed_bindings:
        return {"reviewed": False, "reviewer_id": None}
    if len(set(reviewed_bindings)) != 1:
        raise ValueError("existing reviewed records do not share one review binding")
    reviewer_id, reviewed_at, reviewed_commit, reviewed_manifest_sha256, reviewed_manifest_keccak = reviewed_bindings[0]
    return {
        "reviewed": True,
        "reviewer_id": reviewer_id,
        "reviewed_at": reviewed_at,
        "reviewed_commit": reviewed_commit,
        "reviewed_manifest_sha256": reviewed_manifest_sha256,
        "reviewed_manifest_keccak": reviewed_manifest_keccak,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="verify generated bytes without writing")
    parser.add_argument("--reviewed", action="store_true", help="emit independently reviewed status")
    parser.add_argument("--reviewer-id", help="independent reviewer actor ID required with --reviewed")
    parser.add_argument("--reviewed-at", help="review completion time, after construction, required with --reviewed")
    parser.add_argument("--reviewed-commit", help="exact candidate A commit reviewed, required with --reviewed")
    parser.add_argument("--reviewed-manifest-sha256", help="candidate A manifest SHA-256, required with --reviewed")
    parser.add_argument("--reviewed-manifest-keccak", help="candidate A manifest Keccak-256, required with --reviewed")
    parser.add_argument(
        "--check-existing-review-state",
        action="store_true",
        help="with --check, replay the one consistent pending or reviewed state already committed",
    )
    args = parser.parse_args(argv)
    explicit_review_arguments = any(
        value is not None
        for value in (
            args.reviewer_id,
            args.reviewed_at,
            args.reviewed_commit,
            args.reviewed_manifest_sha256,
            args.reviewed_manifest_keccak,
        )
    )
    if args.check_existing_review_state and (not args.check or args.reviewed or explicit_review_arguments):
        parser.error("--check-existing-review-state requires --check and cannot be combined with explicit review arguments")
    generation_arguments: dict[str, Any] = {
        "reviewed": args.reviewed,
        "reviewer_id": args.reviewer_id,
        "reviewed_at": args.reviewed_at,
        "reviewed_commit": args.reviewed_commit,
        "reviewed_manifest_sha256": args.reviewed_manifest_sha256,
        "reviewed_manifest_keccak": args.reviewed_manifest_keccak,
    }
    if args.check_existing_review_state:
        pending_records = build_records(False, None)
        try:
            generation_arguments = infer_existing_review_arguments(pending_records)
        except ValueError as exc:
            print(f"Public entity migration review-state replay refused: {exc}")
            return 1
    records = build_records(**generation_arguments)
    unexpected_inventory, missing_inventory = generated_directory_issues(records)
    inventory_issues = [*unexpected_inventory, *missing_inventory]
    # Missing expected outputs are repairable in write mode; stale unexpected
    # JSON is never removed or silently retained. --check remains strict on
    # both classes of inventory issue.
    mismatches: list[str] = list(inventory_issues if args.check else unexpected_inventory)
    if args.check:
        for relative, record in sorted(records.items()):
            destination = ROOT / relative
            encoded = json.dumps(record, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
            if not destination.is_file() or destination.read_text(encoding="utf-8") != encoded:
                mismatches.append(relative)
    else:
        if unexpected_inventory:
            print("Public entity migration refused: generated inventory mismatch:")
            print("\n".join(f"- {path}" for path in unexpected_inventory))
            print("Remove stale generated files explicitly, then rerun the migration.")
            return 1
        with tempfile.TemporaryDirectory(prefix=".public-entity-migration-", dir=ROOT) as staging_dir:
            staging_root = Path(staging_dir)
            for relative, record in sorted(records.items()):
                staged = staging_root / relative
                staged.parent.mkdir(parents=True, exist_ok=True)
                encoded = json.dumps(record, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
                staged.write_text(encoded, encoding="utf-8", newline="\n")
            for relative in sorted(records):
                destination = ROOT / relative
                destination.parent.mkdir(parents=True, exist_ok=True)
                os.replace(staging_root / relative, destination)
    if mismatches:
        print("Public entity migration is stale:")
        print("\n".join(f"- {path}" for path in mismatches))
        return 1
    print(f"Public entity migration {'verified' if args.check else 'generated'}: {len(records)} records")
    return 0


if __name__ == "__main__":
    sys.exit(main())
