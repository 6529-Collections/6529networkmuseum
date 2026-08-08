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
CONSTRUCTOR_ID = "codex-task:019fe093-6890-7d20-9685-e291642d23ef"
REVIEWER_ID = "codex-review:pending-independent-review"
GENERATED_AT = "2026-08-08T00:00:00Z"
CASEY_AT = "2026-08-02T06:30:00Z"
KEYS_AT = "2026-08-01T15:03:35Z"
PROPOSAL_AT = "2026-08-06T13:19:30.726Z"
WINNER_AT = "2026-08-08T10:15:02.0167151Z"
WINNER_OBSERVATION_ID = "6529NM-WAVE-OBS-2026-08-08-001"
WINNER_SOURCE_PATH = "records/proposed-gifts/6529NM-PG-2026-001/wave-status-observation-2026-08-08.json"
WINNER_SOURCE_URL = "https://6529.io/waves/5f207393-5418-4a75-8738-e40edb44a94d?drop=002bfa4f-8416-48bf-b35e-38f354e9a9f0"
JCS_ID = "0x886c7c89c308c459ca8a626e0ef36a5ea9f4c7a7b56aaf86c71a2ddf3b4f9044"
ZERO32 = "0x" + "0" * 64
GITHUB = "https://github.com/6529-Collections/6529networkmuseum/blob/main/"
PUBLIC_ENTITY_SCHEMA = "0xd8aef6592fe156c4c3c10e59de540f5cdf8b130eedca322e0e22b30764bee1a9"
PUBLIC_RELATION_SCHEMA = "0xaa76f1b93e01ae7a1cff2717b0c814df772fd26d3997a47847a1887cba6756de"
WAVE_STATUS_SCHEMA = "0xfe0b5244859ffb994766ff3aeace88f12961e07bb97941c647044327737c9be1"


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


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


def evidence(label: str, source: str, observed_at: str, evidence_class: str = "C") -> dict[str, Any]:
    uri = source if source.startswith(("https://", "ipfs://", "ar://")) else github_uri(source_repository_path(source))
    return {"label": label, "uri": uri, "observed_at": observed_at, "evidence_class": evidence_class}


def names(value: str, source_kind: str, refs: list[str], observed_at: str | None = None) -> list[dict[str, Any]]:
    observed_at = observed_at or (CASEY_AT if any("6529NM.2026.001" in ref for ref in refs) else KEYS_AT)
    evidence_refs: list[dict[str, Any]] = []
    seen: set[str] = set()
    for ref in refs:
        item = evidence("Name source", ref, observed_at)
        key = json.dumps(item, sort_keys=True)
        if key not in seen:
            seen.add(key)
            evidence_refs.append(item)
    return [{"value": value, "variant_role": "preferred", "source_kind": source_kind, "evidence_refs": evidence_refs}]


def names_with_source_label(value: str, source_kind: str, refs: list[str], observed_at: str | None = None) -> list[dict[str, Any]]:
    observed_at = observed_at or PROPOSAL_AT
    variants = names(value, source_kind, refs, observed_at)
    variants.append({"value": value, "variant_role": "source_label", "source_kind": source_kind, "evidence_refs": [evidence("Raw issuer label", ref, observed_at) for ref in refs]})
    return variants


def fact(status: str, observed_at: str, refs: list[str], notes: str) -> dict[str, Any]:
    return {"status": status, "as_of": observed_at, "evidence_refs": [evidence("Source record", ref, observed_at) for ref in refs], "notes": notes}


def lifecycle_observation(observation_id: str, status: str, source_status: str, observed_at: str, refs: list[str], notes: str, evidence_refs: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    return {
        "observation_id": observation_id,
        "status": status,
        "source_status": source_status,
        "observed_at": observed_at,
        "source_record_ids": sorted(set(refs)),
        "evidence_refs": evidence_refs or [evidence("Lifecycle source", ref, observed_at) for ref in refs],
        "notes": notes,
    }


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


def finalize(payload: dict[str, Any], relative_path: str, reviewed: bool, reviewer_id: str | None) -> dict[str, Any]:
    if reviewed:
        reviewer = reviewer_id or REVIEWER_ID
        if reviewer.endswith("pending-independent-review"):
            raise ValueError("--reviewed requires --reviewer-id from an independent reviewer")
        payload["reviewer"] = {"id": reviewer, "role": "reviewer", "reviewed_at": GENERATED_AT}
        payload["record_status"] = "reviewed"
        payload["review_status"] = "reviewed"
    payload["payload_sha256"] = sha256_bytes(canonicalize(payload))
    effective_seconds = int(datetime.datetime.fromisoformat(payload["effective_at"].replace("Z", "+00:00")).timestamp())
    record_type = payload["record_type"]
    return {
        "$schema": "https://6529networkmuseum.org/schemas/record-envelope-v1.json",
        "envelope": {
            "recordType": record_type,
            "subjectId": keccak256(f"6529networkmuseum.subject.{record_type.lower()}.v1:{payload['record_id']}".encode("utf-8")),
            "contentHash": {"algorithm": 1, "digest": keccak256(canonicalize(payload)), "canonicalizationId": JCS_ID},
            "uri": github_uri(relative_path),
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
        "entity_status": "published" if reviewed else "archived",
        "status_observation": {"status_label": "published" if reviewed else "archived", "observed_at": effective_at, "evidence_refs": evidence_refs},
        "source_record_ids": sorted(set(refs)),
        "profile": profile,
    })
    if media_entity_ids is not None:
        payload["media_entity_ids"] = sorted(set(media_entity_ids))
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


def media_profile(role: str, locator_uri: str | None, repository_path: str | None, media_type: str, visual: bool, width: int | None, height: int | None, accessibility_text: str | None, accessibility_status: str, subject: str, credit: str, rights_status: str, source_status: str, source_refs: list[str], observed_at: str, fixity: dict[str, Any], affordances: list[str], *, derived_from: str | None = None, transform: str | None = None, signed_wave: dict[str, Any] | None = None, accessibility_subject_policy: str = "not_applicable") -> dict[str, Any]:
    publication_boundary = {
        "museum_retained_preservation_object": "preservation_record",
        "museum_generated_public_derivative": "public_derivative",
        "token_linked_source_media": "token_source",
        "signed_wave_proposal_presentation": "signed_wave_proposal_only",
    }[role]
    rights_evidence: list[dict[str, Any]] = []
    source_evidence: list[dict[str, Any]] = []
    seen_evidence: set[str] = set()
    for ref in source_refs:
        key = source_repository_path(ref)
        if key in seen_evidence:
            continue
        seen_evidence.add(key)
        rights_evidence.append(evidence("Rights boundary", ref, observed_at))
        source_evidence.append(evidence("Source observation", ref, observed_at))
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
            "subject_entity_id": subject,
            "credit": credit,
            "rights": {"status": rights_status, "statement_entity_id": None, "observed_at": observed_at, "evidence_refs": rights_evidence, "notes": "Rights state is projected from the cited source and is not inferred from media availability."},
            "source_observation": {"status": source_status, "observed_at": observed_at, "evidence_refs": source_evidence, "notes": "Source observation and mutable-host boundary remain separate from preservation status."},
            "fixity": fixity,
            "source_record_ids": sorted(set(source_refs)),
            "derived_from_media_entity_id": derived_from,
            "transform_profile": transform,
            "signed_wave": signed_wave,
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


def build_records(reviewed: bool = False, reviewer_id: str | None = None) -> dict[str, dict[str, Any]]:
    vocab = load_json(VOCAB_PATH)
    identity_inventory = load_json(IDENTITY_INVENTORY_PATH)
    slug_inventory = {
        row["entity_id"]: row for row in identity_inventory.get("public_slug_inventory", [])
    }
    records: dict[str, dict[str, Any]] = {}
    def add_entity(*args: Any, **kwargs: Any) -> str:
        relative, payload = entity(*args, reviewed=reviewed, **kwargs)
        records[relative] = finalize(payload, relative, reviewed, reviewer_id)
        return payload["entity_id"]
    def add_relation(*args: Any, **kwargs: Any) -> str:
        relative, payload = relation(*args, **kwargs)
        records[relative] = finalize(payload, relative, reviewed, reviewer_id)
        return payload["relation_id"]

    winner_payload = common("WAVE_STATUS_OBSERVATION", WINNER_OBSERVATION_ID, WINNER_AT, ["6529NM-PG-2026-001"], [
        evidence("Original PARTICIPATORY proposal observation", "records/proposed-gifts/6529NM-PG-2026-001/proposal.json", PROPOSAL_AT),
        evidence("Authenticated WINNER status observation", WINNER_SOURCE_URL, WINNER_AT),
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
        "observation_method": "authenticated_drop_readback",
        "selection_effect": "selected_by_museum_wave_acquisition_review_in_progress",
        "non_effects": ["acceptance_not_established", "transfer_not_established", "title_not_established", "custody_not_established", "rights_not_established", "technical_not_established", "preservation_not_established", "accession_not_established", "collection_membership_not_established"],
        "prior_observation": {
            "source_status": "PARTICIPATORY",
            "observed_at": PROPOSAL_AT,
            "source_record_id": "6529NM-PG-2026-001",
            "source_record_path": "records/proposed-gifts/6529NM-PG-2026-001/proposal.json",
            "source_url": "https://6529.io/waves/5f207393-5418-4a75-8738-e40edb44a94d?drop=002bfa4f-8416-48bf-b35e-38f354e9a9f0",
        },
        "source_record_ids": ["6529NM-PG-2026-001"],
    })
    records[WINNER_SOURCE_PATH] = finalize(winner_payload, WINNER_SOURCE_PATH, reviewed, reviewer_id)

    def typed_id(prefix: str, number: int) -> str:
        return f"6529NM-{prefix}-{number:04d}"

    institution = typed_id("I", 1)
    collection = typed_id("C", 1)
    casey_agent = typed_id("AGT", 1)
    casey_artist = typed_id("ART", 1)
    art_blocks = typed_id("ORG", 1)
    magnum_org = typed_id("ORG", 2)
    magnum_project = typed_id("PRJ", 6)
    gift_program = "6529NM-AP-ENT-0001"
    keys_program = "6529NM-AP-ENT-0002"
    project_names = ["CENTURY", "Pre-Process", "Phototaxis", "923 EMPTY ROOMS", "Ex Nihilo (Cosmos)"]
    projects = {name: typed_id("PRJ", 1 + index) for index, name in enumerate(project_names)}
    casey_work_ids = [typed_id("W", 1 + index) for index in range(7)]
    accession = "6529NM-ACC-ENT-0001"
    publication = typed_id("RP", 1)
    magnum_agents = [typed_id("AGT", 18 + index) for index in range(5)]
    magnum_works = [typed_id("W", 24 + index) for index in range(5)]
    media_retained = typed_id("MED", 1)
    media_token = typed_id("MED", 2)
    media_wave = typed_id("MED", 3)
    media_derivative = typed_id("MED", 4)
    casey_media_ids = [typed_id("MED", 10 + index) for index in range(7)]
    keys_media_ids = [typed_id("MED", 20 + index) for index in range(16)]
    magnum_media_ids = [media_wave, *[typed_id("MED", 41 + index) for index in range(4)]]

    object_paths = sorted((ROOT / "records/accessions/6529NM.2026.001/objects").glob("*.json"))
    casey_objects = [load_json(path)["payload"] for path in object_paths]
    accession_refs = ["6529NM.2026.001", "6529NM-ACC-2026-001"]
    institution_refs = ["6529NM-GOV-1052156", "6529NM-GOV-1052812"]
    add_entity(institution, "INSTITUTION", "6529 Network Museum", None, "/museum/network", CASEY_AT, {
        "profile_type": "INSTITUTION", "institution_kind": "network_museum", "mission": "A public, evidence-led museum for network-native art and its long-term care.",
        "authority": {"authority_status": "established", "authority_record_ids": institution_refs, "evidence_refs": [evidence("Adopted Museum policy", "6529NM-GOV-1052156", CASEY_AT)]},
        "name_variants": names("6529 Network Museum", "museum_record", institution_refs), "collection_entity_id": collection,
    }, institution_refs, [evidence("Museum governance source", "6529NM-GOV-1052156", CASEY_AT)], media_entity_ids=[media_derivative])
    add_entity(collection, "COLLECTION", "6529 Network Museum permanent Collection", None, "/museum/network/collection", CASEY_AT, {
        "profile_type": "COLLECTION", "collection_kind": "permanent_collection", "institution_entity_id": institution, "membership_rule": "accession_only", "admitted_work_entity_ids": casey_work_ids,
        "evidence_refs": [evidence("Casey accession register", "6529NM.2026.001", CASEY_AT)],
    }, [institution, *accession_refs], [evidence("Accession-only membership rule", "6529NM.2026.001", CASEY_AT)])
    add_entity(casey_agent, "AGENT", "Casey REAS", "casey-reas-agent", "/museum/network/agents/casey-reas-agent", CASEY_AT, {
        "profile_type": "AGENT", "agent_kind": "PERSON", "authority": {"authority_status": "established", "authority_record_ids": [], "evidence_refs": [evidence("Casey object records", object_paths[0].relative_to(ROOT).as_posix(), CASEY_AT)]},
        "name_variants": names("Casey REAS", "artist_statement", ["6529NM.2026.001.01"]), "role_contexts": ["artist", "creator", "donated-work subject"],
    }, ["6529NM.2026.001.01", "6529NM.2026.001.07"], [evidence("Casey artist practice record", "records/accessions/6529NM.2026.001/public/casey-reas-artist-practice.md", CASEY_AT)])
    add_entity(casey_artist, "ARTIST", "Casey Reas", "casey-reas", "/museum/network/artists/casey-reas", CASEY_AT, {
        "profile_type": "ARTIST", "authority": {"authority_status": "established", "authority_record_ids": [casey_agent], "evidence_refs": [evidence("Casey artist practice record", "records/accessions/6529NM.2026.001/public/casey-reas-artist-practice.md", CASEY_AT)]},
        "practice": {"summary": "A practice spanning software, generative systems, image, publication, and the cultural conditions of computation.", "areas": ["generative software", "digital image", "systems research"], "evidence_refs": [evidence("Casey artist practice record", "records/accessions/6529NM.2026.001/public/casey-reas-artist-practice.md", CASEY_AT)]},
        "name_variants": names("Casey Reas", "artist_statement", ["6529NM.2026.001.01"]),
    }, [casey_agent, "6529NM.2026.001.01", "6529NM.2026.001.07"], [evidence("Casey artist practice record", "records/accessions/6529NM.2026.001/public/casey-reas-artist-practice.md", CASEY_AT)])
    add_entity(art_blocks, "ORGANIZATION", "Art Blocks", "art-blocks", "/museum/network/organizations/art-blocks", CASEY_AT, {
        "profile_type": "ORGANIZATION", "organization_kind": "platform", "history_summary": "Art Blocks is the publishing platform identified by the Casey object records for the relevant generative projects.", "roles": ["publishing platform", "project context"],
        "authority": {"authority_status": "provisional", "authority_record_ids": [], "evidence_refs": [evidence("Casey object record", "6529NM.2026.001.01", CASEY_AT)]}, "name_variants": names("Art Blocks", "published_source", ["6529NM.2026.001.01"]),
    }, ["6529NM.2026.001.01"], [evidence("Casey object record", "6529NM.2026.001.01", CASEY_AT)])
    add_entity(magnum_org, "ORGANIZATION", "Magnum Photos", slug_inventory[magnum_org]["public_slug"], slug_inventory[magnum_org]["canonical_route"], PROPOSAL_AT, {
        "profile_type": "ORGANIZATION", "organization_kind": "collective", "history_summary": "Magnum Photos is the photographer cooperative and archive/publisher named by the retained Magnum Photos 75 proposal evidence. This limited public profile records its source-documented project role without asserting a Museum ownership or rights relationship.", "roles": ["photographic cooperative", "archive and publisher", "Magnum Photos 75 project originator/publisher"],
        "authority": {"authority_status": "provisional", "authority_record_ids": [], "evidence_refs": [evidence("Magnum Photos source profile", "records/proposed-gifts/6529NM-PG-2026-001/public/wave-storm/01-resolution.md", PROPOSAL_AT)]}, "name_variants": names("Magnum Photos", "published_source", ["records/proposed-gifts/6529NM-PG-2026-001/public/wave-storm/01-resolution.md"], PROPOSAL_AT),
    }, ["6529NM-PG-2026-001"], [evidence("Magnum Photos source profile", "records/proposed-gifts/6529NM-PG-2026-001/public/wave-storm/01-resolution.md", PROPOSAL_AT)])
    add_entity(gift_program, "ACQUISITION_PROGRAM", "Gift Acquisitions", slug_inventory[gift_program]["public_slug"], slug_inventory[gift_program]["canonical_route"], CASEY_AT, {
        "profile_type": "ACQUISITION_PROGRAM", "program_kind": "donation_pathway", "program_id": gift_program, "authority_record_ids": institution_refs, "rules_summary": "A standing donation pathway governed by adopted Museum donation and collection-scope decisions; each gift retains its own review and accession gates.", "program_status": "complete", "produced_acquisition_entity_ids": ["6529NM-CA-2026-001"], "selected_outcome_record_ids": [], "evidence_refs": [evidence("Adopted donation decision", "6529NM-GOV-1052812", CASEY_AT)],
    }, institution_refs, [evidence("Adopted donation decision", "6529NM-GOV-1052812", CASEY_AT)])
    keys_program_source = "6529NM-AP-01"
    program = load_json(ROOT / "records/programs/6529NM-AP-01/program.json")
    selected_index = load_json(ROOT / "records/programs/6529NM-AP-01/selected-works.json")
    outcomes = selected_index["works"]
    add_entity(keys_program, "ACQUISITION_PROGRAM", "Keys and Gates", slug_inventory[keys_program]["public_slug"], slug_inventory[keys_program]["canonical_route"], KEYS_AT, {
        "profile_type": "ACQUISITION_PROGRAM", "program_kind": "themed_program", "program_id": keys_program_source, "authority_record_ids": [keys_program_source], "rules_summary": "A 60-day photography program with TDH/WAVE selection, CC0 and consent terms, a planned 0.5 ETH purchase price per acquired work, quantity determined by Meme Card mints, and rank-order fallback.", "program_status": program["status"], "produced_acquisition_entity_ids": ["6529NM-CA-2026-002"], "selected_outcome_record_ids": [row["record_id"] for row in outcomes], "evidence_refs": [evidence("Keys and Gates program record", "records/programs/6529NM-AP-01/program.json", KEYS_AT)],
    }, [keys_program_source, *[row["record_id"] for row in outcomes]], [evidence("Keys and Gates program record", "records/programs/6529NM-AP-01/program.json", KEYS_AT)])

    for index, (project_name, project_id) in enumerate(projects.items()):
        project_work_ids = [casey_work_ids[i] for i, obj in enumerate(casey_objects) if obj.get("project", {}).get("name") == project_name]
        project_inventory = slug_inventory[project_id]
        add_entity(project_id, "PROJECT_OR_SERIES", project_name, project_inventory["public_slug"], project_inventory["canonical_route"], CASEY_AT, {
            "profile_type": "PROJECT_OR_SERIES", "project_type": "project", "project_relation_basis": "source_project_record", "scope_statement": f"The Casey object records identify {project_name} as a distinct project context; this projection does not assert ownership of all project outputs.", "agent_entity_ids": [casey_artist], "work_entity_ids": project_work_ids, "ownership_boundary": "Project context is distinct from Museum ownership; only separately accessioned Work entities enter the Collection.", "source_record_ids": project_work_ids and project_work_ids or ["6529NM.2026.001"], "evidence_refs": [evidence("Casey project source records", project_work_ids[0] if project_work_ids else "6529NM.2026.001", CASEY_AT)],
        }, [casey_artist, art_blocks, *project_work_ids], [evidence("Casey project source record", project_work_ids[0] if project_work_ids else "6529NM.2026.001", CASEY_AT)])

    for index, obj in enumerate(casey_objects):
        work_id = casey_work_ids[index]
        object_id = obj["record_id"]
        project_id = projects[obj["project"]["name"]]
        rights_id = next((ref for ref in obj.get("references", []) if ".RIGHTS." in ref), "6529NM.2026.001.RIGHTS.01")
        condition_id = next((ref for ref in obj.get("references", []) if ".COND." in ref), "6529NM.2026.001.COND.01")
        add_entity(work_id, "WORK", obj["title"], work_id, f"/museum/network/works/{work_id}", CASEY_AT, {
            "profile_type": "WORK", "creator_entity_ids": [casey_artist], "title": obj["title"], "creation_date": {"display": "not established in the accession projection", "status": "not_established", "earliest": None, "latest": None, "evidence_refs": [evidence("Casey object record", object_id, CASEY_AT)]}, "medium": obj["medium"], "work_lifecycle_status": "accessioned",
            "current_museum_relation": {"museum_entity_id": institution, "relation_status": "permanent_collection", "as_of": CASEY_AT, "evidence_refs": [evidence("Accession certificate", "6529NM-ACC-2026-001", CASEY_AT)]},
            "mint_fact": fact("verified", CASEY_AT, [object_id], "The existing Work Description carries the token identity; minting remains a separate fact from accession."),
            "collection_membership": {"status": "permanent_collection", "collection_entity_id": collection, "accession_entity_ids": [accession], "source_record_ids": ["6529NM.2026.001", "6529NM-ACC-2026-001"], "evidence_refs": [evidence("Accession certificate", "6529NM-ACC-2026-001", CASEY_AT)]},
            "project_or_series_entity_ids": [project_id], "acquisition_entity_ids": ["6529NM-CA-2026-001"], "program_entity_ids": [gift_program], "accession_entity_ids": [accession], "lifecycle_observations": [lifecycle_observation("6529NM-W-OBS-0001", "accessioned", "accessioned", CASEY_AT, ["6529NM-ACC-2026-001", object_id], "The Work is admitted through the completed Casey accession; mint, rights, custody, and preservation remain independently recorded facts.")],
            "component_references": [{"reference_type": "component", "record_id": object_id, "source_record_id": object_id, "evidence_refs": [evidence("Existing WORK_DESCRIPTION", object_id, CASEY_AT)]}], "manifestation_references": [{"reference_type": "manifestation", "record_id": "6529NM.2026.001.VO-01", "source_record_id": "6529NM.2026.001.VO-01", "evidence_refs": [evidence("Visual observation", "6529NM.2026.001.VO-01", CASEY_AT)]}], "identity_boundary": "The public Work identity is separate from the accession lot, token, component record, manifestation, title, custody, and future acquisition relations.", "evidence_refs": [evidence("Existing WORK_DESCRIPTION", object_id, CASEY_AT), evidence("Rights statement", rights_id, CASEY_AT), evidence("Condition report", condition_id, CASEY_AT)],
        }, [object_id, "6529NM.2026.001", "6529NM-ACC-2026-001", rights_id, condition_id, "6529NM.2026.001.VO-01", project_id, accession, "6529NM-CA-2026-001", gift_program], [evidence("Existing WORK_DESCRIPTION", object_id, CASEY_AT)], media_entity_ids=([media_retained, media_token, casey_media_ids[index]] if index == 0 else [casey_media_ids[index]]))

    add_entity(accession, "ACCESSION", "Casey Reas accession 6529NM.2026.001", None, None, CASEY_AT, {
        "profile_type": "ACCESSION", "accession_number": "6529NM.2026.001", "accession_status": "complete", "admitted_work_entity_ids": casey_work_ids, "source_accession_record_id": "6529NM-ACC-2026-001", "evidence_refs": [evidence("Accession certificate", "6529NM-ACC-2026-001", CASEY_AT)],
    }, ["6529NM.2026.001", "6529NM-ACC-2026-001", *casey_work_ids], [evidence("Accession certificate", "6529NM-ACC-2026-001", CASEY_AT)])
    add_entity(publication, "RESEARCH_PUBLICATION", "The System in Seven States", "the-system-in-seven-states", "/museum/network/research/the-system-in-seven-states", CASEY_AT, {
        "profile_type": "RESEARCH_PUBLICATION", "publication_kind": "collection_essay", "title": "The System in Seven States", "publication_date": "2026-08-02", "version": "1.5.0", "author_entity_ids": [institution], "subject_entity_ids": ["6529NM-CA-2026-001", *projects.values(), *casey_work_ids], "publication_document_uri": github_uri("records/accessions/6529NM.2026.001/public/casey-reas-collection-essay.md"), "evidence_refs": [evidence("Published collection essay", "records/accessions/6529NM.2026.001/public/casey-reas-collection-essay.md", CASEY_AT)],
    }, ["6529NM.2026.001", "6529NM-CA-2026-001", *projects.values(), *casey_work_ids], [evidence("Published collection essay", "records/accessions/6529NM.2026.001/public/casey-reas-collection-essay.md", CASEY_AT)])

    keys_agent_ids: list[str] = []
    keys_artist_ids_by_name: dict[str, str] = {}
    keys_artist_ids_by_index: list[str] = []
    for index, row in enumerate(outcomes):
        agent_id = typed_id("AGT", 2 + index)
        keys_agent_ids.append(agent_id)
        add_entity(agent_id, "AGENT", row["artist"], None, None, KEYS_AT, {
            "profile_type": "AGENT", "agent_kind": "PERSON", "authority": {"authority_status": "source_label_only", "authority_record_ids": [], "evidence_refs": [evidence("Keys and Gates outcome", row["record_id"], KEYS_AT)]}, "name_variants": names(row["artist"], "wave", [row["record_id"]]), "role_contexts": ["submitting artist label"],
        }, [row["record_id"], keys_program_source], [evidence("Keys and Gates outcome", row["record_id"], KEYS_AT)])
        artist_id = keys_artist_ids_by_name.setdefault(row["artist"], typed_id("ART", 2 + len(keys_artist_ids_by_name)))
        keys_artist_ids_by_index.append(artist_id)
    for artist_name, artist_id in keys_artist_ids_by_name.items():
        artist_outcomes = [row["record_id"] for row in outcomes if row["artist"] == artist_name]
        artist_slug = slug_inventory[artist_id]["public_slug"]
        add_entity(artist_id, "ARTIST", artist_name, artist_slug, slug_inventory[artist_id]["canonical_route"], KEYS_AT, {
            "profile_type": "ARTIST", "authority": {"authority_status": "source_label_only", "authority_record_ids": [keys_agent_ids[outcomes.index(next(row for row in outcomes if row["artist"] == artist_name))]], "evidence_refs": [evidence("Keys and Gates artist label", artist_outcomes[0], KEYS_AT)]}, "practice": {"summary": "A limited public artist profile derived from the artist label attached to a Keys and Gates program outcome; it does not assert a complete scholarly biography.", "areas": ["photography", "program submission"], "evidence_refs": [evidence("Keys and Gates artist label", ref, KEYS_AT) for ref in artist_outcomes]}, "name_variants": names(artist_name, "wave", artist_outcomes, KEYS_AT),
        }, [*artist_outcomes, keys_program_source, *[keys_agent_ids[index] for index, row in enumerate(outcomes) if row["artist"] == artist_name]], [evidence("Keys and Gates artist label", artist_outcomes[0], KEYS_AT)])
    keys_work_ids: list[str] = []
    for index, row in enumerate(outcomes):
        work_id = typed_id("W", 8 + index)
        keys_work_ids.append(work_id)
        outcome_id = row["record_id"]
        add_entity(work_id, "WORK", row["title"], work_id, f"/museum/network/works/{work_id}", KEYS_AT, {
            "profile_type": "WORK", "creator_entity_ids": [keys_artist_ids_by_index[index]], "title": row["title"], "creation_date": {"display": "not established", "status": "not_established", "earliest": None, "latest": None, "evidence_refs": [evidence("Keys and Gates outcome", outcome_id, KEYS_AT)]}, "medium": "photographic submission; final technical and identity state unverified", "work_lifecycle_status": "selected_through_acquisition_program", "current_museum_relation": {"museum_entity_id": institution, "relation_status": "selected_through_acquisition_program", "as_of": KEYS_AT, "evidence_refs": [evidence("Keys and Gates selected-works index", outcome_id, KEYS_AT)]}, "mint_fact": fact("pending", KEYS_AT, [outcome_id], "The source outcome is selected_unminted; minting is an independent pending fact and does not establish acquisition or Collection membership."), "collection_membership": {"status": "not_in_collection", "collection_entity_id": None, "accession_entity_ids": [], "source_record_ids": [outcome_id], "evidence_refs": [evidence("Selected outcome is not an accession", outcome_id, KEYS_AT)]}, "project_or_series_entity_ids": [], "acquisition_entity_ids": ["6529NM-CA-2026-002"], "program_entity_ids": [keys_program], "accession_entity_ids": [], "lifecycle_observations": [lifecycle_observation(f"6529NM-W-OBS-{8 + index:04d}", "selected_through_acquisition_program", "selected_unminted", KEYS_AT, [outcome_id, keys_program_source], "The program selection remains a historical source outcome; minting, acquisition, accession, and Collection membership are independent facts.")], "component_references": [{"reference_type": "component", "record_id": outcome_id, "source_record_id": outcome_id, "source_status": "selected_unminted", "evidence_refs": [evidence("Selected outcome source", outcome_id, KEYS_AT)]}], "manifestation_references": [], "identity_boundary": "This Work identity is independent of the acquisition, program outcome, mint, payment, title, custody, rights, technical review, preservation, display, and any later accession.", "evidence_refs": [evidence("Keys and Gates outcome", outcome_id, KEYS_AT)],
        }, [outcome_id, keys_program_source, keys_program, "6529NM-CA-2026-002", keys_agent_ids[index]], [evidence("Keys and Gates outcome", outcome_id, KEYS_AT)], media_entity_ids=[keys_media_ids[index]])

    proposal = load_json(ROOT / "records/proposed-gifts/6529NM-PG-2026-001/proposal.json")
    magnum_work_source_ids: list[str] = []
    magnum_artist_ids = [typed_id("ART", 17 + index) for index in range(5)]
    for index, obj in enumerate(proposal["objects"]):
        agent_id = magnum_agents[index]
        work_id = magnum_works[index]
        artist_id = magnum_artist_ids[index]
        candidate_id = obj["candidate_object_id"]
        magnum_work_source_ids.append(candidate_id)
        add_entity(agent_id, "AGENT", obj["artist"], None, None, PROPOSAL_AT, {
            "profile_type": "AGENT", "agent_kind": "PERSON", "authority": {"authority_status": "source_label_only", "authority_record_ids": [], "evidence_refs": [evidence("Proposed gift object label", "6529NM-PG-2026-001", PROPOSAL_AT)]}, "name_variants": names(obj["artist"], "proposal", ["6529NM-PG-2026-001"]), "role_contexts": ["proposed work creator label"],
        }, ["6529NM-PG-2026-001"], [evidence("Proposed gift object label", "6529NM-PG-2026-001", PROPOSAL_AT)])
        add_entity(artist_id, "ARTIST", obj["artist"], slug_inventory[artist_id]["public_slug"], slug_inventory[artist_id]["canonical_route"], PROPOSAL_AT, {
            "profile_type": "ARTIST", "authority": {"authority_status": "source_label_only", "authority_record_ids": [agent_id], "evidence_refs": [evidence("Proposed gift artist label", "6529NM-PG-2026-001", PROPOSAL_AT)]}, "practice": {"summary": "A limited public artist profile derived from the artist label attached to a proposed Museum Wave work; it does not assert a complete scholarly biography.", "areas": ["photography", "proposal work"], "evidence_refs": [evidence("Proposed gift artist label", "6529NM-PG-2026-001", PROPOSAL_AT)]}, "name_variants": names_with_source_label(obj["artist"], "proposal", ["6529NM-PG-2026-001"], PROPOSAL_AT),
        }, [agent_id, "6529NM-PG-2026-001", candidate_id], [evidence("Proposed gift artist label", "6529NM-PG-2026-001", PROPOSAL_AT)])
        add_entity(work_id, "WORK", obj["title"], work_id, f"/museum/network/works/{work_id}", WINNER_AT, {
            "profile_type": "WORK", "creator_entity_ids": [artist_id], "title": obj["title"], "creation_date": {"display": str(obj["date"]), "status": "established", "earliest": f"{obj['date']}-01-01", "latest": f"{obj['date']}-12-31", "evidence_refs": [evidence("Proposed gift object", "6529NM-PG-2026-001", PROPOSAL_AT)]}, "medium": "photograph", "work_lifecycle_status": "selected_by_museum_wave_acquisition_review_in_progress", "current_museum_relation": {"museum_entity_id": institution, "relation_status": "selected_by_museum_wave", "as_of": WINNER_AT, "evidence_refs": [evidence("Authenticated WINNER status observation", WINNER_SOURCE_PATH, WINNER_AT), evidence("Signed Museum Wave drop", WINNER_SOURCE_URL, WINNER_AT)]}, "mint_fact": fact("not_started", WINNER_AT, ["6529NM-PG-2026-001", WINNER_OBSERVATION_ID], "The WINNER source status establishes Museum Wave selection and acquisition review only; it does not establish mint, payment, title, custody, rights, technical review, preservation, accession, or Collection membership."), "collection_membership": {"status": "not_in_collection", "collection_entity_id": None, "accession_entity_ids": [], "source_record_ids": ["6529NM-PG-2026-001", WINNER_OBSERVATION_ID], "evidence_refs": [evidence("WINNER has no accession effect", WINNER_SOURCE_PATH, WINNER_AT)]}, "project_or_series_entity_ids": [magnum_project], "acquisition_entity_ids": ["6529NM-CA-2026-003"], "program_entity_ids": [], "accession_entity_ids": [], "lifecycle_observations": [lifecycle_observation(f"6529NM-W-OBS-{24 + index:04d}", "proposed_in_museum_wave", "PARTICIPATORY", PROPOSAL_AT, ["6529NM-PG-2026-001"], "The original published proposal observation is retained as history and is not rewritten.", [evidence("Original PARTICIPATORY proposal observation", "records/proposed-gifts/6529NM-PG-2026-001/proposal.json", PROPOSAL_AT)]), lifecycle_observation(f"6529NM-W-OBS-{29 + index:04d}", "selected_by_museum_wave_acquisition_review_in_progress", "WINNER", WINNER_AT, ["6529NM-PG-2026-001", WINNER_OBSERVATION_ID], "Authenticated live WINNER status changes the Museum relationship to selection under acquisition review only; the five Works remain outside the permanent Collection.", [evidence("Authenticated WINNER status observation", WINNER_SOURCE_PATH, WINNER_AT), evidence("Signed Museum Wave drop", WINNER_SOURCE_URL, WINNER_AT)])], "component_references": [], "manifestation_references": [{"reference_type": "manifestation", "record_id": f"{candidate_id}.TOKEN", "source_record_id": candidate_id, "source_status": "proposed", "caip19": f"eip155:1/erc721:{obj['contract']}/{obj['token_id']}", "evidence_refs": [evidence("Proposed ERC-721 manifestation reference", "6529NM-PG-2026-001", PROPOSAL_AT)]}], "identity_boundary": "Work identity is independent of the proposed acquisition, candidate object alias, chain identity, token manifestation, and any later accession.", "evidence_refs": [evidence("Authenticated WINNER status observation", WINNER_SOURCE_PATH, WINNER_AT), evidence("Original proposal object", "6529NM-PG-2026-001", PROPOSAL_AT)],
        }, ["6529NM-PG-2026-001", "6529NM-CA-2026-003", magnum_project, agent_id], [evidence("Proposed gift object", "6529NM-PG-2026-001", PROPOSAL_AT)], media_entity_ids=[magnum_media_ids[index]])

    add_entity(magnum_project, "PROJECT_OR_SERIES", "Magnum Photos 75", slug_inventory[magnum_project]["public_slug"], slug_inventory[magnum_project]["canonical_route"], PROPOSAL_AT, {
        "profile_type": "PROJECT_OR_SERIES", "project_type": "series", "project_relation_basis": "proposal_work_set", "scope_statement": "Retained proposal evidence names Magnum Photos 75 as a 2022 anniversary-year release context drawn from the Magnum archive. This Project projection links the five proposed Museum Works to that named context; it does not assert that the Museum owns, accepted, or catalogs the complete Magnum Photos 75 release.", "agent_entity_ids": [magnum_org, *magnum_artist_ids], "work_entity_ids": magnum_works, "ownership_boundary": "Magnum Photos 75 is a broader source project and tokenized release context, distinct from the Museum's Conflict at Its Edges Curated Acquisition and from each independent Work identity. Token manifestations and source media do not establish Museum title, custody, rights, or Collection membership.", "source_record_ids": ["6529NM-PG-2026-001", *magnum_work_source_ids], "evidence_refs": [evidence("Named Magnum Photos 75 project", "records/proposed-gifts/6529NM-PG-2026-001/public/wave-storm/01-resolution.md", PROPOSAL_AT), evidence("Five-work proposal set", "records/proposed-gifts/6529NM-PG-2026-001/proposal.json", PROPOSAL_AT)],
    }, [magnum_org, *magnum_artist_ids, *magnum_works, "6529NM-PG-2026-001"], [evidence("Named Magnum Photos 75 project", "records/proposed-gifts/6529NM-PG-2026-001/public/wave-storm/01-resolution.md", PROPOSAL_AT), evidence("Five-work proposal set", "records/proposed-gifts/6529NM-PG-2026-001/proposal.json", PROPOSAL_AT)])

    acquisition_facts_casey = {"mint": fact("verified", CASEY_AT, ["6529NM-ACC-2026-001"], "Existing accession records contain the token identity and receipt evidence."), "payment": fact("not_applicable", CASEY_AT, ["6529NM.2026.001"], "The completed gift is recorded as a donation."), "title": fact("verified", CASEY_AT, ["6529NM-ACC-2026-001"], "Title binding is recorded separately and is not copyright."), "custody": fact("verified", CASEY_AT, ["6529NM-ACC-2026-001"], "Custody receipt is recorded separately."), "rights": fact("verified_with_conditions", CASEY_AT, ["6529NM.2026.001.RIGHTS.01"], "Rights are recorded per object with attribution and noncommercial conditions."), "technical": fact("verified_with_conditions", CASEY_AT, ["6529NM.2026.001.COND.01"], "Technical and condition review passed with conditions."), "preservation": fact("in_progress", CASEY_AT, ["6529NM.2026.001.DILIGENCE-01"], "Autonomous generator preservation remains active stewardship."), "display": fact("verified_with_conditions", CASEY_AT, ["6529NM.2026.001.COND.01"], "Display is ready with conditions where the object record says so.")}
    acquisition_facts_keys = {key: fact(status, KEYS_AT, [keys_program_source], note) for key, status, note in [("mint", "not_established", "No primary mint evidence is recorded."), ("payment", "planned", "Program terms describe a planned purchase price only."), ("title", "not_established", "No title binding is recorded."), ("custody", "unverified", "Planned custody reference is not custody evidence."), ("rights", "unverified", "Conditional program terms are not an effective rights grant."), ("technical", "not_started", "No completed technical review is recorded."), ("preservation", "not_started", "No preservation completion is recorded."), ("display", "not_started", "No display authorization is recorded.")]}
    acquisition_facts_proposal = {key: fact(status, PROPOSAL_AT, ["6529NM-PG-2026-001"], note) for key, status, note in [("mint", "verified", "The proposal source records candidate chain history, not Museum acquisition."), ("payment", "not_established", "No Museum purchase is recorded."), ("title", "not_established", "No Museum title binding is recorded."), ("custody", "unverified", "Observed external owner is not Museum custody."), ("rights", "unverified", "All Rights Reserved is retained as source fact."), ("technical", "pending_review", "Proposal-level technical evidence is not an accession review."), ("preservation", "not_started", "The upstream files are not Museum preservation objects."), ("display", "not_started", "Proposal presentation is not display authorization.")]}
    add_entity("6529NM-CA-2026-001", "CURATED_ACQUISITION", "The System in Seven States", "the-system-in-seven-states", "/museum/network/acquisitions/the-system-in-seven-states", CASEY_AT, {"profile_type": "CURATED_ACQUISITION", "title": "The System in Seven States", "thesis": "A Museum curatorial grouping reads seven accessioned Casey Reas works through related computational systems without claiming an artist-defined canonical group.", "acquisition_method": "donation", "program_or_pathway": {"kind": "acquisition_program", "entity_ids": [gift_program], "source_record_ids": institution_refs}, "work_entity_ids": casey_work_ids, "source_work_record_ids": [obj["record_id"] for obj in casey_objects], "lifecycle": {"status": "accessioned_into_permanent_collection", "as_of": CASEY_AT, "evidence_refs": [evidence("Accession certificate", "6529NM-ACC-2026-001", CASEY_AT)]}, "lifecycle_observations": [lifecycle_observation("6529NM-CA-OBS-0001", "accessioned_into_permanent_collection", "accessioned", CASEY_AT, ["6529NM-ACC-2026-001"], "The completed Casey donation is accessioned into the permanent Collection.")], "collection_effect": "permanent_collection", "independent_acquisition_facts": acquisition_facts_casey, "public_credit": "Gift of punk6529", "evidence_refs": [evidence("Casey accession lot", "6529NM.2026.001", CASEY_AT)]}, [gift_program, accession, *casey_work_ids, *[obj["record_id"] for obj in casey_objects], "6529NM-ACC-2026-001"], [evidence("Casey accession lot", "6529NM.2026.001", CASEY_AT)])
    add_entity("6529NM-CA-2026-002", "CURATED_ACQUISITION", "Keys and Gates", "keys-and-gates", "/museum/network/acquisitions/keys-and-gates", KEYS_AT, {"profile_type": "CURATED_ACQUISITION", "title": "Keys and Gates", "thesis": "A provisional Museum program selection frames photographs around access, exclusion, permission, surveillance, custody, autonomy, and exit; selection is not completed acquisition.", "acquisition_method": "purchase", "program_or_pathway": {"kind": "acquisition_program", "entity_ids": [keys_program], "source_record_ids": [keys_program_source]}, "work_entity_ids": keys_work_ids, "source_work_record_ids": [row["record_id"] for row in outcomes], "lifecycle": {"status": "selected_through_acquisition_program_acquisition_pending", "as_of": KEYS_AT, "evidence_refs": [evidence("Keys and Gates selected-works index", keys_program_source, KEYS_AT)]}, "lifecycle_observations": [lifecycle_observation("6529NM-CA-OBS-0002", "selected_through_acquisition_program_acquisition_pending", "selected_unminted", KEYS_AT, [keys_program_source], "Keys and Gates remains selected through its acquisition program with acquisition pending.")], "collection_effect": "none", "independent_acquisition_facts": acquisition_facts_keys, "public_credit": "Selected through the Keys and Gates acquisition program; acquisition pending", "evidence_refs": [evidence("Keys and Gates program record", "records/programs/6529NM-AP-01/program.json", KEYS_AT)]}, [keys_program, keys_program_source, *keys_work_ids, *[row["record_id"] for row in outcomes]], [evidence("Keys and Gates program record", "records/programs/6529NM-AP-01/program.json", KEYS_AT)])
    add_entity("6529NM-CA-2026-003", "CURATED_ACQUISITION", "Conflict at Its Edges", "conflict-at-its-edges", "/museum/network/acquisitions/conflict-at-its-edges", WINNER_AT, {"profile_type": "CURATED_ACQUISITION", "title": "Conflict at Its Edges", "thesis": "A formal Museum Wave proposal presents five photographs as one proposed gift; the same public identity now records a live WINNER selection under acquisition review without implying acceptance, acquisition, custody, title, rights, preservation, accession, or Collection membership.", "acquisition_method": "donation", "program_or_pathway": {"kind": "museum_wave_proposal", "entity_ids": [], "source_record_ids": ["6529NM-PG-2026-001", WINNER_OBSERVATION_ID]}, "work_entity_ids": magnum_works, "source_work_record_ids": ["6529NM-PG-2026-001", *magnum_work_source_ids], "lifecycle": {"status": "selected_by_museum_wave_acquisition_review_in_progress", "as_of": WINNER_AT, "evidence_refs": [evidence("Authenticated WINNER status observation", WINNER_SOURCE_PATH, WINNER_AT), evidence("Signed Museum Wave drop", WINNER_SOURCE_URL, WINNER_AT)]}, "lifecycle_observations": [lifecycle_observation("6529NM-CA-OBS-0003", "proposed_in_museum_wave", "PARTICIPATORY", PROPOSAL_AT, ["6529NM-PG-2026-001"], "The original PARTICIPATORY proposal observation remains part of the append-only lifecycle history.", [evidence("Original PARTICIPATORY proposal observation", "records/proposed-gifts/6529NM-PG-2026-001/proposal.json", PROPOSAL_AT)]), lifecycle_observation("6529NM-CA-OBS-0004", "selected_by_museum_wave_acquisition_review_in_progress", "WINNER", WINNER_AT, ["6529NM-PG-2026-001", WINNER_OBSERVATION_ID], "Authenticated live WINNER status selects the proposed identity for Museum acquisition review only; it creates no accession or Collection membership.", [evidence("Authenticated WINNER status observation", WINNER_SOURCE_PATH, WINNER_AT), evidence("Signed Museum Wave drop", WINNER_SOURCE_URL, WINNER_AT)])], "collection_effect": "none", "independent_acquisition_facts": acquisition_facts_proposal, "public_credit": "Selected by the Museum Wave; acquisition review in progress", "evidence_refs": [evidence("Authenticated WINNER status observation", WINNER_SOURCE_PATH, WINNER_AT), evidence("Original proposed gift record", "6529NM-PG-2026-001", PROPOSAL_AT)]}, ["6529NM-PG-2026-001", WINNER_OBSERVATION_ID, *magnum_works, *magnum_work_source_ids], [evidence("Authenticated WINNER status observation", WINNER_SOURCE_PATH, WINNER_AT), evidence("Original proposed gift record", "6529NM-PG-2026-001", PROPOSAL_AT)])

    retained_path = ROOT / "evidence/casey-reas/manifest.json"
    derivative_path = ROOT / "records/proposed-gifts/6529NM-PG-2026-001/public/media/conflict-at-its-edges-cover.png"
    manifest = load_json(ROOT / "records/programs/6529NM-AP-01/media-manifest.json")
    wave_storm = load_json(ROOT / "records/proposed-gifts/6529NM-PG-2026-001/wave-storm.json")
    wave_media_by_candidate = {
        part.get("candidate_object_id"): part.get("media", [])[0]
        for part in wave_storm.get("parts", [])
        if part.get("candidate_object_id") and part.get("media")
    }
    add_entity(media_retained, "MEDIA_REFERENCE", "Casey retained preservation evidence manifest", None, None, CASEY_AT, media_profile("museum_retained_preservation_object", github_uri("evidence/casey-reas/manifest.json"), "evidence/casey-reas/manifest.json", "application/json", False, None, None, None, "not_applicable", casey_work_ids[0], "6529 Network Museum preservation evidence manifest", "cleared_with_conditions", "retrieved", ["6529NM.2026.001.01", "6529NM-ACC-2026-001"], CASEY_AT, {"status": "verified", "algorithm": "sha256", "digest": sha256_file(retained_path), "verified_at": GENERATED_AT, "basis": "Retrieved repository bytes hashed by the deterministic migration."}, ["view", "open_repository_path", "copy_citation"]), ["6529NM.2026.001.01", "6529NM-ACC-2026-001"] , [evidence("Retained evidence manifest", "evidence/casey-reas/manifest.json", CASEY_AT)])
    add_entity(media_token, "MEDIA_REFERENCE", "Casey token-linked metadata source", None, None, CASEY_AT, media_profile("token_linked_source_media", casey_objects[0]["chain_identity"]["metadata_uri"], None, "application/json", False, None, None, None, "not_applicable", casey_work_ids[0], "Casey Reas, token-linked metadata source", "cleared_with_conditions", "retrieved", ["6529NM.2026.001.01", "6529NM.2026.001.RIGHTS.01"], CASEY_AT, {"status": "verified", "algorithm": "sha256", "digest": casey_objects[0]["chain_identity"]["metadata_sha256"], "verified_at": CASEY_AT, "basis": "Existing object record metadata snapshot fixity."}, ["view", "open_token_source", "copy_citation"]), ["6529NM.2026.001.01", "6529NM.2026.001.RIGHTS.01"], [evidence("Token-linked metadata record", "6529NM.2026.001.01", CASEY_AT)])
    for index, obj in enumerate(casey_objects):
        object_id = obj["record_id"]
        add_entity(casey_media_ids[index], "MEDIA_REFERENCE", f"{obj['title']} live presentation source", None, None, CASEY_AT, media_profile(
            "token_linked_source_media",
            obj["chain_identity"]["generator_uri"],
            None,
            "text/html",
            False,
            None,
            None,
            None,
            "not_applicable",
            casey_work_ids[index],
            obj["credit_line"],
            "cleared_with_conditions",
            "mutable_external",
            [object_id, "6529NM.2026.001.VO-01"],
            CASEY_AT,
            {"status": "unverified_not_retrieved", "algorithm": None, "digest": None, "verified_at": None, "basis": "The live generator is an external mutable presentation source; the Museum retains observation evidence rather than the response bytes."},
            ["view", "open_token_source", "copy_citation"],
        ), [object_id, "6529NM.2026.001.VO-01"], [evidence("Casey live presentation source", object_id, CASEY_AT)])
    signed_obj = proposal["objects"][0]
    signed_wave_metadata = {"wave_id": "5f207393-5418-4a75-8738-e40edb44a94d", "drop_id": "002bfa4f-8416-48bf-b35e-38f354e9a9f0", "publication_record_id": "6529NM-PG-2026-001", "published_at": PROPOSAL_AT, "signature_status": "signed_and_published"}
    add_entity(media_wave, "MEDIA_REFERENCE", "Conflict at Its Edges signed-Wave presentation source", None, None, PROPOSAL_AT, media_profile("signed_wave_proposal_presentation", signed_obj["image"]["uri"], None, signed_obj["image"]["media_type"], True, signed_obj["image"]["width"], signed_obj["image"]["height"], wave_media_by_candidate[signed_obj["candidate_object_id"]]["alt_text"], "provided", magnum_works[0], signed_obj["rights"]["copyright_notice"], "restricted", "retrieved", ["6529NM-PG-2026-001"], PROPOSAL_AT, {"status": "verified", "algorithm": "sha256", "digest": signed_obj["image"]["sha256"], "verified_at": PROPOSAL_AT, "basis": "Proposal record retains the observed upstream image digest."}, ["view", "hero", "alt_text", "open_signed_wave_source", "copy_citation"], signed_wave=signed_wave_metadata, accessibility_subject_policy="non_identifying_sensitive_subject"), ["6529NM-PG-2026-001"], [evidence("Published signed-Wave presentation", "records/proposed-gifts/6529NM-PG-2026-001/wave-storm.json", PROPOSAL_AT)])
    for index, signed_obj in enumerate(proposal["objects"][1:], start=1):
        candidate_id = signed_obj["candidate_object_id"]
        wave_media = wave_media_by_candidate[candidate_id]
        add_entity(magnum_media_ids[index], "MEDIA_REFERENCE", f"{signed_obj['title']} signed-Wave presentation source", None, None, PROPOSAL_AT, media_profile(
            "signed_wave_proposal_presentation",
            signed_obj["image"]["uri"],
            None,
            signed_obj["image"]["media_type"],
            True,
            signed_obj["image"]["width"],
            signed_obj["image"]["height"],
            wave_media["alt_text"],
            "provided",
            magnum_works[index],
            wave_media["credit_line"],
            "restricted",
            "retrieved",
            ["6529NM-PG-2026-001", candidate_id],
            PROPOSAL_AT,
            {"status": "verified", "algorithm": "sha256", "digest": signed_obj["image"]["sha256"], "verified_at": PROPOSAL_AT, "basis": "Proposal record retains the observed upstream image digest."},
            ["view", "hero", "alt_text", "open_signed_wave_source", "copy_citation"],
            signed_wave=signed_wave_metadata,
            accessibility_subject_policy="non_identifying_child_subject" if index == 3 else "non_identifying_sensitive_subject",
        ), ["6529NM-PG-2026-001", candidate_id], [evidence("Published signed-Wave presentation", "records/proposed-gifts/6529NM-PG-2026-001/wave-storm.json", PROPOSAL_AT)])
    width = 1600
    add_entity(media_derivative, "MEDIA_REFERENCE", "Conflict at Its Edges Museum proposal cover derivative", None, None, PROPOSAL_AT, media_profile("museum_generated_public_derivative", github_uri("records/proposed-gifts/6529NM-PG-2026-001/public/media/conflict-at-its-edges-cover.png"), "records/proposed-gifts/6529NM-PG-2026-001/public/media/conflict-at-its-edges-cover.png", "image/png", True, width, width, "Dark square proposal cover for Conflict at Its Edges: Five Photographs of Evidence and Aftermath.", "provided", institution, "6529 Network Museum, Conflict at Its Edges proposal cover, 2026.", "cleared_with_conditions", "retrieved", ["6529NM-PG-2026-001"], PROPOSAL_AT, {"status": "verified", "algorithm": "sha256", "digest": sha256_file(derivative_path), "verified_at": GENERATED_AT, "basis": "Retrieved repository bytes hashed by the deterministic migration."}, ["view", "hero", "alt_text", "open_repository_path", "copy_citation"], derived_from=media_wave, transform="Museum proposal-cover PNG derived from the signed-Wave source package"), ["6529NM-PG-2026-001", media_wave], [evidence("Museum-generated proposal cover", "records/proposed-gifts/6529NM-PG-2026-001/public/media/conflict-at-its-edges-cover.png", PROPOSAL_AT)])

    for index, item in enumerate(manifest["items"]):
        outcome_id = item["record_id"]
        derivative = next(row for row in item["presentation"]["derivatives"] if row["width"] == 1280)
        outcome = outcomes[index]
        derivative_path_value = derivative["repository_path"]
        add_entity(keys_media_ids[index], "MEDIA_REFERENCE", f"{outcome['title']} Museum presentation derivative", None, None, KEYS_AT, media_profile(
            "museum_generated_public_derivative",
            derivative["url"],
            derivative_path_value,
            derivative["mime_type"],
            True,
            derivative["width"],
            derivative["height"],
            item["presentation"]["alt_text"],
            "provided",
            keys_work_ids[index],
            f"{outcome['artist']} — {outcome['title']}; Keys and Gates program presentation",
            "unknown",
            "retrieved",
            [outcome_id, keys_program_source],
            KEYS_AT,
            {"status": "verified", "algorithm": "sha256", "digest": derivative["sha256"], "verified_at": KEYS_AT, "basis": "The governed Keys and Gates media manifest records the retrieved derivative bytes and digest."},
            ["view", "thumbnail", "hero", "alt_text", "copy_citation"],
            transform=manifest["transform"]["profile"],
        ), [outcome_id, keys_program_source], [evidence("Keys and Gates presentation derivative", derivative_path_value, KEYS_AT)])

    add_relation("6529NM-REL-0001", "INSTITUTION_HOLDS_COLLECTION", institution, collection, {}, CASEY_AT, institution_refs, [evidence("Institution collection relation", "6529NM.2026.001", CASEY_AT)])
    for index, work_id in enumerate(casey_work_ids):
        add_relation(f"6529NM-REL-{2 + index:04d}", "ARTIST_CREATES_WORK", casey_artist, work_id, {"role": "creator"}, CASEY_AT, [casey_objects[index]["record_id"]], [evidence("Casey object creator", casey_objects[index]["record_id"], CASEY_AT)])
    relation_number = 9
    for index, work_id in enumerate(keys_work_ids):
        outcome_id = outcomes[index]["record_id"]
        add_relation(f"6529NM-REL-{relation_number:04d}", "ARTIST_CREATES_WORK", keys_artist_ids_by_index[index], work_id, {"role": "creator"}, KEYS_AT, [outcome_id], [evidence("Keys and Gates artist creator", outcome_id, KEYS_AT)])
        relation_number += 1
    for index, work_id in enumerate(magnum_works):
        add_relation(f"6529NM-REL-{relation_number:04d}", "ARTIST_CREATES_WORK", magnum_artist_ids[index], work_id, {"role": "creator"}, PROPOSAL_AT, [magnum_work_source_ids[index]], [evidence("Proposed artist creator", "6529NM-PG-2026-001", PROPOSAL_AT)])
        relation_number += 1
    for project_name, project_id in projects.items():
        for work_id in [casey_work_ids[i] for i, obj in enumerate(casey_objects) if obj.get("project", {}).get("name") == project_name]:
            object_id = next(obj["record_id"] for obj in casey_objects if projects[obj["project"]["name"]] == project_id and casey_work_ids[casey_objects.index(obj)] == work_id)
            add_relation(f"6529NM-REL-{relation_number:04d}", "PROJECT_CONTEXTUALIZES_WORK", project_id, work_id, {"scope": "source_project"}, CASEY_AT, [object_id], [evidence("Casey project context", object_id, CASEY_AT)])
            relation_number += 1
        add_relation(f"6529NM-REL-{relation_number:04d}", "ORGANIZATION_ORIGINATES_PROJECT", art_blocks, project_id, {"role": "platform"}, CASEY_AT, ["6529NM.2026.001.01"], [evidence("Art Blocks project context", "6529NM.2026.001.01", CASEY_AT)])
        relation_number += 1
    magnum_project_source_paths = [
        "records/proposed-gifts/6529NM-PG-2026-001/public/wave-storm/02-david-seymour-127.md",
        "records/proposed-gifts/6529NM-PG-2026-001/public/wave-storm/03-larry-towell-145.md",
        "records/proposed-gifts/6529NM-PG-2026-001/public/wave-storm/04-micha-bar-am-97.md",
        "records/proposed-gifts/6529NM-PG-2026-001/public/wave-storm/05-moises-saman-44.md",
        "records/proposed-gifts/6529NM-PG-2026-001/public/wave-storm/06-lorenzo-meloni-104.md",
    ]
    for index, work_id in enumerate(magnum_works):
        candidate_id = magnum_work_source_ids[index]
        source_path = magnum_project_source_paths[index]
        add_relation(f"6529NM-REL-{relation_number:04d}", "PROJECT_CONTEXTUALIZES_WORK", magnum_project, work_id, {"scope": "proposal_work_set"}, PROPOSAL_AT, [candidate_id, "6529NM-PG-2026-001"], [evidence("Magnum Photos 75 project context", source_path, PROPOSAL_AT)])
        relation_number += 1
    add_relation(f"6529NM-REL-{relation_number:04d}", "ORGANIZATION_ORIGINATES_PROJECT", magnum_org, magnum_project, {"role": "publisher"}, PROPOSAL_AT, ["6529NM-PG-2026-001"], [evidence("Magnum Photos 75 project origin", "records/proposed-gifts/6529NM-PG-2026-001/public/wave-storm/01-resolution.md", PROPOSAL_AT)])
    relation_number += 1
    add_relation(f"6529NM-REL-{relation_number:04d}", "ACQUISITION_PROGRAM_PRODUCES_ACQUISITION", gift_program, "6529NM-CA-2026-001", {}, CASEY_AT, institution_refs, [evidence("Gift pathway", "6529NM-GOV-1052812", CASEY_AT)]); relation_number += 1
    add_relation(f"6529NM-REL-{relation_number:04d}", "ACQUISITION_PROGRAM_PRODUCES_ACQUISITION", keys_program, "6529NM-CA-2026-002", {}, KEYS_AT, [keys_program_source], [evidence("Keys and Gates program", keys_program_source, KEYS_AT)]); relation_number += 1
    for index, work_id in enumerate(casey_work_ids):
        add_relation(f"6529NM-REL-{relation_number:04d}", "CURATED_ACQUISITION_BRINGS_TOGETHER_WORK", "6529NM-CA-2026-001", work_id, {"display_order": index + 1, "selection_status": "selected", "scope": "museum_curatorial_grouping"}, CASEY_AT, [casey_objects[index]["record_id"]], [evidence("Casey curated acquisition", casey_objects[index]["record_id"], CASEY_AT)]); relation_number += 1
    for index, work_id in enumerate(keys_work_ids):
        outcome_id = outcomes[index]["record_id"]
        add_relation(f"6529NM-REL-{relation_number:04d}", "CURATED_ACQUISITION_BRINGS_TOGETHER_WORK", "6529NM-CA-2026-002", work_id, {"display_order": index + 1, "selection_status": "selected_unminted", "scope": "source_project"}, KEYS_AT, [outcome_id], [evidence("Keys and Gates selected outcome", outcome_id, KEYS_AT)]); relation_number += 1
        add_relation(f"6529NM-REL-{relation_number:04d}", "PROGRAM_SELECTS_WORK", keys_program, work_id, {"display_order": index + 1, "selection_status": "selected_unminted", "mint_status": "pending"}, KEYS_AT, [outcome_id], [evidence("Keys and Gates selected outcome", outcome_id, KEYS_AT)]); relation_number += 1
    for index, work_id in enumerate(magnum_works):
        add_relation(f"6529NM-REL-{relation_number:04d}", "CURATED_ACQUISITION_BRINGS_TOGETHER_WORK", "6529NM-CA-2026-003", work_id, {"display_order": index + 1, "selection_status": "proposed", "scope": "proposal_work_set"}, PROPOSAL_AT, ["6529NM-PG-2026-001"], [evidence("Published proposal work set", "6529NM-PG-2026-001", PROPOSAL_AT)]); relation_number += 1
    for index, work_id in enumerate(casey_work_ids):
        object_id = casey_objects[index]["record_id"]
        add_relation(f"6529NM-REL-{relation_number:04d}", "ACCESSION_ADMITS_WORK", accession, work_id, {"accession_object_id": object_id}, CASEY_AT, ["6529NM-ACC-2026-001", object_id], [evidence("Accession certificate", "6529NM-ACC-2026-001", CASEY_AT)]); relation_number += 1
        add_relation(f"6529NM-REL-{relation_number:04d}", "COLLECTION_CONTAINS_WORK", collection, work_id, {"collection_membership_status": "permanent_collection"}, CASEY_AT, ["6529NM-ACC-2026-001", object_id], [evidence("Collection accession relation", "6529NM-ACC-2026-001", CASEY_AT)]); relation_number += 1
    for target in ["6529NM-CA-2026-001", *projects.values(), *casey_work_ids]:
        add_relation(f"6529NM-REL-{relation_number:04d}", "PUBLICATION_INTERPRETS_ENTITY", publication, target, {"role": "subject"}, CASEY_AT, ["6529NM.2026.001"], [evidence("The System in Seven States", "records/accessions/6529NM.2026.001/public/casey-reas-collection-essay.md", CASEY_AT)]); relation_number += 1
    add_relation(f"6529NM-REL-{relation_number:04d}", "INSTITUTION_PUBLISHES_PUBLICATION", institution, publication, {}, CASEY_AT, ["6529NM.2026.001"], [evidence("Published collection essay", "records/accessions/6529NM.2026.001/public/casey-reas-collection-essay.md", CASEY_AT)]); relation_number += 1
    for source, target, context, refs, observed in [(casey_work_ids[0], media_retained, "preservation", ["6529NM-ACC-2026-001"], CASEY_AT), (casey_work_ids[0], media_token, "source", ["6529NM.2026.001.01"], CASEY_AT), (magnum_works[0], media_wave, "source", ["6529NM-PG-2026-001"], PROPOSAL_AT), (institution, media_derivative, "hero", ["6529NM-PG-2026-001"], PROPOSAL_AT)]:
        add_relation(f"6529NM-REL-{relation_number:04d}", "ENTITY_HAS_MEDIA", source, target, {"media_context": context}, observed, refs, [evidence("Typed media relation", refs[0], observed)]); relation_number += 1
    for index, work_id in enumerate(casey_work_ids):
        object_id = casey_objects[index]["record_id"]
        add_relation(f"6529NM-REL-{relation_number:04d}", "ENTITY_HAS_MEDIA", work_id, casey_media_ids[index], {"media_context": "primary"}, CASEY_AT, [object_id], [evidence("Casey Work presentation media relation", object_id, CASEY_AT)]); relation_number += 1
    for index, work_id in enumerate(keys_work_ids):
        outcome_id = outcomes[index]["record_id"]
        add_relation(f"6529NM-REL-{relation_number:04d}", "ENTITY_HAS_MEDIA", work_id, keys_media_ids[index], {"media_context": "primary"}, KEYS_AT, [outcome_id], [evidence("Keys and Gates Work presentation media relation", outcome_id, KEYS_AT)]); relation_number += 1
    for index, work_id in enumerate(magnum_works[1:], start=1):
        candidate_id = proposal["objects"][index]["candidate_object_id"]
        add_relation(f"6529NM-REL-{relation_number:04d}", "ENTITY_HAS_MEDIA", work_id, magnum_media_ids[index], {"media_context": "source"}, PROPOSAL_AT, [candidate_id], [evidence("Magnum signed-Wave Work media relation", "records/proposed-gifts/6529NM-PG-2026-001/wave-storm.json", PROPOSAL_AT)]); relation_number += 1
    verify_evidence_paths(records)
    return records


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="verify generated bytes without writing")
    parser.add_argument("--reviewed", action="store_true", help="emit independently reviewed status")
    parser.add_argument("--reviewer-id", help="independent reviewer actor ID required with --reviewed")
    args = parser.parse_args(argv)
    records = build_records(args.reviewed, args.reviewer_id)
    mismatches: list[str] = []
    if args.check:
        for relative, record in sorted(records.items()):
            destination = ROOT / relative
            encoded = json.dumps(record, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
            if not destination.is_file() or destination.read_text(encoding="utf-8") != encoded:
                mismatches.append(relative)
    else:
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
