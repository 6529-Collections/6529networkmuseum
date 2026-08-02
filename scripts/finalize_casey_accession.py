#!/usr/bin/env python3
"""Finalize the Casey REAS gift as a reviewed, accessioned collection lot."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from canonical import canonicalize
from validate import keccak256


ROOT = Path(__file__).resolve().parent.parent
CASEY = ROOT / "records" / "accessions" / "6529NM.2026.001"
REPO = "https://github.com/6529-Collections/6529networkmuseum"
EVIDENCE_COMMIT = "823586e89c365dff26ef598140ef856f96dcd501"
REVIEW_AT = "2026-08-02T06:30:00Z"
ACCEPTED_AT = "2026-08-01T22:55:00Z"
RECEIVED_AT = "2026-08-01T13:25:47Z"
TRANSACTION = "0xbdde33b32d4b70335b10cbd37c0b00a027844f14c900d82aa4f75b7a7b390498"
BLOCK = 25660311
DONOR_ADDRESS = "0x6daa633c23615a29471deafae351727867e7dad1"
MUSEUM_ADDRESS = "0xbecfa2ba5a782d11e1a0e821e8f2e30b6684178c"
REGISTRAR_REVIEWER = "codex-review:019fc04f-6d34-7242-992f-3de8ff2b6346"
TECHNICAL_REVIEWER = REGISTRAR_REVIEWER
CURATORIAL_REVIEWER = REGISTRAR_REVIEWER
CANONICALIZATION_ID = "0x886c7c89c308c459ca8a626e0ef36a5ea9f4c7a7b56aaf86c71a2ddf3b4f9044"
ACCESSION_SCHEMA_ID = "0xc04bb48f95c8db4fe7f26a20106533f987003843f2fed36fd6d89f207ddfbd86"

ROOMS_EDITION_STATEMENT = (
    "The retained population snapshot establishes 924 tokens and invocations 0–923. "
    "Invocation 0 is separately coded 999999; invocations 1–923 follow the documented "
    "combinatorial sequence. The reviewed generator contains the same 924-entry table. "
    "Native token #713 is invocation 713 and maps to Code 555536. This resolves the "
    "numerical structure but does not assign an artistic interpretation to invocation 0."
)

GENERATOR_EVIDENCE: dict[str, dict[str, Any]] = {
    "01": {
        "response_sha256": "sha256:465b45798f14bea109f59986bd2cdcfd6e2eb9050327f52b24af15e159704ae2",
        "dependency": "p5.js 1.0.0 via cdnjs",
        "interaction_map": [
            {"input": "1", "action": "Cut and reorder image slices."},
            {"input": "2", "action": "Restore the ordered composition."},
        ],
    },
    "02": {
        "response_sha256": "sha256:1dfd3f2205e8c4a33f85d2c0efce35b019d2ea21e424e5d750bc86c3890c3b3e",
        "dependency": "p5.js 1.0.0 via cdnjs",
        "interaction_map": [
            {"input": "1", "action": "Cut and reorder image slices."},
            {"input": "2", "action": "Restore the ordered composition."},
        ],
    },
    "03": {
        "response_sha256": "sha256:51ab1073b166701c9379984d9331c14d803dc84e35c8d06b5a8071f4eb895aad",
        "dependency": "p5.js 1.0.0 via cdnjs",
        "interaction_map": [
            {"input": "1", "action": "Cut and reorder image slices."},
            {"input": "2", "action": "Restore the ordered composition."},
        ],
    },
    "04": {
        "response_sha256": "sha256:8cbf3ee01db1a864163eeb5b30776372917256b9246b255e0f514cf03b64505b",
        "dependency": "p5.js 1.0.0 via cdnjs",
        "interaction_map": [
            {"input": "mouse press", "action": "Reset the composition."},
            {"input": "1–8", "action": "Select a surface treatment and reset the composition."},
            {"input": "Space", "action": "Reset the composition."},
            {"input": "P", "action": "Pause or resume animation."},
        ],
    },
    "05": {
        "response_sha256": "sha256:b3d7c39954beabf85cb6213eff3d57e3b1f7670c6763c663bc426a9c918bcaf3",
        "dependency": "p5.js 1.0.0 via cdnjs",
        "interaction_map": [
            {"input": "P", "action": "Pause or resume the simulation."},
            {"input": "B", "action": "Restart the simulation from the beginning."},
            {"input": "1–5", "action": "Change magnification."},
            {"input": "L", "action": "Reveal or hide the simulated light locations."},
        ],
        "automatic_behavior": "The simulation stops after 1,000 iterations for the initial thumbnail state.",
    },
    "06": {
        "response_sha256": "sha256:2d722fe294710e3b443802baecc1f445b94cf00bf9dbdfbebbb08d4d6d3529e0",
        "dependency": "p5.js 1.0.0 via cdnjs",
        "interaction_map": [
            {"input": "+ / -", "action": "Increase or decrease scale."},
            {"input": "D", "action": "Toggle the diagram view."},
            {"input": "Space", "action": "Change the background state."},
            {"input": "R / G / B", "action": "Toggle red, green, or blue channels."},
            {"input": "1–6", "action": "Select a city preset."},
            {"input": "Arrow keys", "action": "Change depth."},
            {"input": "S", "action": "Change speed."},
            {"input": "0 / 9", "action": "Change line length."},
            {"input": "T", "action": "Change resolution."},
            {"input": "P", "action": "Save the current view."},
        ],
    },
    "07": {
        "response_sha256": "sha256:17402c7259ac4af1e93894eb74b36a5796a6a058ea0fb0e56d2f55101a3c84f9",
        "dependency": "p5.js 1.9.0 via cdnjs",
        "interaction_map": [
            {"input": "Space", "action": "Generate a new Still Life state."},
            {"input": "P", "action": "Pause or resume animation."},
            {"input": "S", "action": "Change speed."},
            {"input": "G / W", "action": "Toggle the implemented green and white display states."},
            {"input": "lowercase r / b", "action": "Toggle the implemented red and blue channel states."},
        ],
        "documentation_discrepancies": [
            "The reviewed generator compares lowercase r and lowercase b (with duplicated lowercase comparisons); the uppercase R and B controls stated in platform metadata are not implemented as written. This is an amber behavior/documentation discrepancy."
        ],
    },
}


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, value: dict[str, Any]) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def file_sha(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def payload_sha(payload: dict[str, Any]) -> str:
    material = {key: value for key, value in payload.items() if key != "payload_sha256"}
    return "sha256:" + hashlib.sha256(canonicalize(material)).hexdigest()


def pin_repository_urls(value: Any) -> Any:
    """Pin payload evidence/display URLs while leaving envelope discovery URIs live."""
    if isinstance(value, str):
        return value.replace(
            f"{REPO}/blob/main/", f"{REPO}/blob/{EVIDENCE_COMMIT}/"
        ).replace(
            f"{REPO}/tree/main/", f"{REPO}/tree/{EVIDENCE_COMMIT}/"
        )
    if isinstance(value, list):
        return [pin_repository_urls(item) for item in value]
    if isinstance(value, dict):
        return {key: pin_repository_urls(item) for key, item in value.items()}
    return value


def unix_seconds(value: str) -> int:
    return int(datetime.fromisoformat(value.replace("Z", "+00:00")).timestamp())


def subject_hash(record_type: str, subject_id: str) -> str:
    material = f"6529networkmuseum.subject.{record_type.lower()}.v1:{subject_id}".encode()
    return "0x" + keccak256(material).hex()


def event_id(record_id: str, event_type: str, occurred_at: str) -> str:
    stamp = occurred_at.replace("-", "").replace(":", "").replace(".", "").replace("Z", "Z")
    return f"{record_id}.EVENT.{event_type}.{stamp}"


def review(actor_id: str) -> dict[str, str]:
    return {"id": actor_id, "role": "reviewer", "reviewed_at": REVIEW_AT}


def evidence(label: str, uri: str, evidence_class: str, sha256: str | None = None, notes: str | None = None) -> dict[str, str]:
    item = {"label": label, "uri": uri, "observed_at": REVIEW_AT, "evidence_class": evidence_class}
    if sha256:
        item["sha256"] = sha256
    if notes:
        item["notes"] = notes
    return item


def commit_record(record: dict[str, Any]) -> None:
    payload = pin_repository_urls(record["payload"])
    record["payload"] = payload
    payload["payload_sha256"] = payload_sha(payload)
    record["envelope"]["contentHash"]["digest"] = "0x" + keccak256(canonicalize(payload)).hex()
    record["envelope"]["effectiveAt"] = unix_seconds(payload["effective_at"])


TITLE_REVIEW = CASEY / "public" / "title-rights-and-accession-review.md"
TECHNICAL_REVIEW = CASEY / "public" / "technical-and-condition-review.md"
CURATORIAL_REVIEW = CASEY / "public" / "curatorial-accession-review.md"
ACCESSION_PUBLIC = CASEY / "public" / "accession-certificate.md"
EVIDENCE_MANIFEST = ROOT / "evidence" / "casey-reas" / "manifest.json"
RPC_RECEIPT = ROOT / "evidence" / "casey-reas" / "raw" / "rpc" / f"eth-get-transaction-receipt-{TRANSACTION}.json"


def rights_grants(metadata_uri: str) -> dict[str, dict[str, str]]:
    common = {
        "grant_status": "granted_with_conditions",
        "observed_at": REVIEW_AT,
        "evidence_ref": metadata_uri,
    }
    return {
        "reproduction": {**common, "basis": "CC BY-NC 4.0 permits noncommercial reproduction and sharing with attribution, license notice/link, change marking, no endorsement, and no additional downstream restrictions."},
        "publication": {**common, "basis": "CC BY-NC 4.0 permits noncommercial collection, scholarly, educational, and public communication with the required attribution and notices."},
        "exhibition": {**common, "basis": "CC BY-NC 4.0 permits noncommercial public display and sharing with attribution, license notice/link, no endorsement, and no additional downstream restrictions."},
        "print": {**common, "basis": "CC BY-NC 4.0 permits noncommercial labels, study prints, conservation references, catalogues, and publications; commercial merchandise is not approved."},
        "derivative_use": {**common, "basis": "CC BY-NC 4.0 permits noncommercial adapted material; modifications and prior modifications must be identified when shared."},
        "ai_training": {**common, "basis": "To the extent copyright permission is required, CC BY-NC 4.0 permits Museum reproduction or adaptation for noncommercial research, cataloguing, conservation, and analysis; commercial model training is not approved."},
        "preservation": {**common, "basis": "CC BY-NC 4.0 permits noncommercial preservation copies in any medium and technical modifications necessary to exercise the licensed rights."},
        "migration_emulation": {**common, "basis": "CC BY-NC 4.0 permits technical modifications and noncommercial adaptations needed for migration and emulation, subject to attribution and change marking when shared."},
        "accessibility": {**common, "basis": "CC BY-NC 4.0 permits noncommercial accessible renditions and adaptations with attribution, license notice/link, and change marking."},
    }


def object_schedule() -> list[dict[str, Any]]:
    schedule = []
    for path in sorted((CASEY / "objects").glob("*.json")):
        payload = load(path)["payload"]
        schedule.append(
            {
                "object_id": payload["object_id"],
                "title": payload["title"],
                "caip19": payload["chain_identity"]["caip19"],
                "contract": payload["chain_identity"]["contract"],
                "token_id": payload["chain_identity"]["token_id"],
                "custody_receipt_log": payload["chain_identity"]["custody_receipt_log"],
            }
        )
    return schedule


def finalize_rights() -> None:
    title_sha = file_sha(TITLE_REVIEW)
    for path in sorted((CASEY / "rights").glob("*.json")):
        record = load(path)
        payload = record["payload"]
        suffix = payload["object_id"].rsplit(".", 1)[1]
        metadata_path = ROOT / "evidence" / "casey-reas" / "raw" / "metadata" / f"6529NM.2026.001.{suffix}.json"
        metadata_uri = f"{REPO}/blob/main/evidence/casey-reas/raw/metadata/{metadata_path.name}"
        payload.update(
            {
                "record_version": "1.1.0",
                "observed_at": REVIEW_AT,
                "effective_at": REVIEW_AT,
                "record_status": "reviewed",
                "review_status": "reviewed",
                "reviewer": review(REGISTRAR_REVIEWER),
                "rights_holder_reference": "Casey REAS and/or the applicable licensor; copyright is not transferred with token title; the work is offered under CC BY-NC 4.0 in retained Art Blocks metadata.",
                "basis": "The Museum owns the token and the donor's full transferable interest. Copyright remains separate. Object-specific retained Art Blocks metadata states CC BY-NC 4.0, whose official legal code affirmatively permits the reviewed noncommercial Museum uses subject to its attribution and other conditions.",
                "grants": rights_grants(metadata_uri),
            }
        )
        for prior_event in payload["events"]:
            prior_event.setdefault("event_id", event_id(payload["record_id"], prior_event["event_type"], prior_event["occurred_at"]))
        payload["events"] = [
            prior_event
            for prior_event in payload["events"]
            if not (prior_event.get("event_type") == "rights_amendment" and prior_event.get("occurred_at") == REVIEW_AT)
        ]
        superseded_event_id = payload["events"][-1]["event_id"]
        payload["events"].append(
            {
                "event_id": event_id(payload["record_id"], "rights_amendment", REVIEW_AT),
                "event_type": "rights_amendment",
                "occurred_at": REVIEW_AT,
                "supersedes_event_id": superseded_event_id,
                "authority_reference": "6529NM.2026.001.ACCESSION-REVIEW",
                "evidence_refs": [
                    evidence("Reviewed title and rights determination", f"{REPO}/blob/main/records/accessions/6529NM.2026.001/public/title-rights-and-accession-review.md", "C", title_sha),
                    evidence("Object-specific retained Art Blocks metadata", metadata_uri, "B", file_sha(metadata_path)),
                    evidence("CC BY-NC 4.0 legal code", "https://creativecommons.org/licenses/by-nc/4.0/legalcode.en", "B"),
                ],
            }
        )
        payload["evidence_refs"] = [
            evidence("Object-specific retained Art Blocks metadata", metadata_uri, "B", file_sha(metadata_path)),
            evidence("Reviewed title and rights determination", f"{REPO}/blob/main/records/accessions/6529NM.2026.001/public/title-rights-and-accession-review.md", "C", title_sha),
            evidence("CC BY-NC 4.0 legal code", "https://creativecommons.org/licenses/by-nc/4.0/legalcode.en", "B"),
            evidence("CC BY-NC 4.0 deed", "https://creativecommons.org/licenses/by-nc/4.0/deed.en", "B"),
        ]
        commit_record(record)
        write(path, record)


def finalize_condition() -> None:
    technical_sha = file_sha(TECHNICAL_REVIEW)
    visual_uri = f"{REPO}/blob/main/records/accessions/6529NM.2026.001/visual-observation-record.json"
    for path in sorted((CASEY / "technical").glob("*.json")):
        record = load(path)
        payload = record["payload"]
        suffix = payload["object_id"].rsplit(".", 1)[1]
        metadata_path = ROOT / "evidence" / "casey-reas" / "raw" / "metadata" / f"6529NM.2026.001.{suffix}.json"
        metadata_uri = f"{REPO}/blob/main/evidence/casey-reas/raw/metadata/{metadata_path.name}"
        payload.update(
            {
                "record_version": "1.1.0",
                "observed_at": REVIEW_AT,
                "effective_at": REVIEW_AT,
                "record_status": "reviewed",
                "review_status": "reviewed",
                "reviewer": review(TECHNICAL_REVIEWER),
                "protocol_state": "Accession-level technical and condition review complete; ongoing software preservation remains in progress.",
                "assessments": {
                    "chain_identity": "green",
                    "metadata_retrieval": "green",
                    "generator_retrieval": "amber",
                    "dependencies": "amber",
                    "render": "amber",
                    "behavior": "amber",
                    "documentation": "amber",
                    "preservation": "amber",
                    "display": "amber",
                },
                "method": "Reviewed synthesis of exact chain receipt and custody joins, retained metadata bytes and fixity, official generator observations, two-frame viewport evidence, documented controls, and preservation-package holdings and omissions.",
                "outcome": "pass_with_conditions: no red condition is identified; the work is accessionable and display-ready with documented network/browser, attribution, monitoring, and fallback conditions while autonomous software preservation remains in progress.",
            }
        )
        for prior_event in payload["events"]:
            prior_event.setdefault("event_id", event_id(payload["record_id"], prior_event["event_type"], prior_event["occurred_at"]))
        payload["events"] = [
            prior_event
            for prior_event in payload["events"]
            if not (prior_event.get("event_type") == "condition_reassessment" and prior_event.get("occurred_at") == REVIEW_AT)
        ]
        superseded_event_id = payload["events"][-1]["event_id"]
        payload["events"].append(
            {
                "event_id": event_id(payload["record_id"], "condition_reassessment", REVIEW_AT),
                "event_type": "condition_reassessment",
                "occurred_at": REVIEW_AT,
                "supersedes_event_id": superseded_event_id,
                "authority_reference": "6529NM.2026.001.TECHNICAL-REVIEW",
                "evidence_refs": [
                    evidence("Reviewed technical and condition determination", f"{REPO}/blob/main/records/accessions/6529NM.2026.001/public/technical-and-condition-review.md", "C", technical_sha),
                    evidence("Object-specific retained Art Blocks metadata", metadata_uri, "B", file_sha(metadata_path)),
                    evidence("Controlled visual observation", visual_uri, "C"),
                ],
            }
        )
        payload["evidence_refs"] = [
            evidence("Reviewed technical and condition determination", f"{REPO}/blob/main/records/accessions/6529NM.2026.001/public/technical-and-condition-review.md", "C", technical_sha),
            evidence("Object-specific retained Art Blocks metadata", metadata_uri, "B", file_sha(metadata_path)),
            evidence("Controlled visual observation", visual_uri, "C"),
            evidence("Preservation evidence manifest", f"{REPO}/blob/main/evidence/casey-reas/manifest.json", "C", file_sha(EVIDENCE_MANIFEST)),
        ]
        commit_record(record)
        write(path, record)


def finalize_objects(title_sha: str) -> None:
    grants_by_suffix: dict[str, dict[str, Any]] = {}
    for path in sorted((CASEY / "rights").glob("*.json")):
        rights_payload = load(path)["payload"]
        grants_by_suffix[rights_payload["object_id"].rsplit(".", 1)[1]] = rights_payload["grants"]
    for path in sorted((CASEY / "objects").glob("*.json")):
        record = load(path)
        payload = record["payload"]
        suffix = payload["object_id"].rsplit(".", 1)[1]
        chain = payload["chain_identity"]
        payload.update(
            {
                "record_version": "1.1.0",
                "observed_at": REVIEW_AT,
                "effective_at": REVIEW_AT,
                "record_status": "reviewed",
                "review_status": "reviewed",
                "reviewer": review(REGISTRAR_REVIEWER),
                "credit_line": f"Gift of punk6529; Casey REAS; {payload['title']}; 6529 Network Museum, {payload['object_id']}. Licensed CC BY-NC 4.0.",
                "current_state": "accessioned",
                "state_history_semantics": "state_history.observed_at records when the Museum's evidence and administrative record substantiated a workflow state; the underlying chain receipt retains its separate block_time.",
                "title_binding": {
                    "object_id": payload["object_id"],
                    "status": "executed",
                    "instrument_sha256": title_sha,
                    "custodian_reference": "networkmuseum.6529.eth",
                    "transfer_transaction": TRANSACTION,
                    "block_number": BLOCK,
                    "from": DONOR_ADDRESS,
                    "to": MUSEUM_ADDRESS,
                    "bound_at": ACCEPTED_AT,
                    "basis": "The donor's full-gift declaration, completed token delivery, formal Museum acceptance, and reviewed institutional title declaration transfer and bind the donor's entire token interest to this exact object.",
                },
                "rights": grants_by_suffix[suffix],
                "condition": {
                    "token": "green",
                    "metadata": "green",
                    "script": "amber",
                    "dependencies": "amber",
                    "rendering": "amber",
                    "behavior": "amber",
                    "documentation": "amber",
                    "protocol_state": "Accession-level condition review complete; autonomous software preservation remains in progress.",
                    "method": "Reviewed chain, metadata, generator, visual-observation, dependency, display, and preservation evidence. Each current official generator route was available and rendered changing output; the absence of a Museum-held autonomous generator package limits reproducibility but does not make the work unavailable.",
                    "narrative": "No red condition is identified. Identity and retained metadata fixity are verified. The live generator routes were functional when observed, while generator packaging, dependency capture, behavior coverage, and cross-environment reproducibility remain amber stewardship priorities.",
                    "observed_at": REVIEW_AT,
                },
                "display": {
                    "status": "ready_with_conditions",
                    "manifest_uri": f"{REPO}/blob/main/records/accessions/6529NM.2026.001/public/technical-and-condition-review.md",
                    "credit_line": f"Casey REAS, {payload['title']}; 6529 Network Museum, gift of punk6529, {payload['object_id']}. Licensed CC BY-NC 4.0.",
                    "observed_at": REVIEW_AT,
                },
                "uncertainties": [
                    "The exact self-contained generator and complete dependency bundle are not yet retained.",
                    "Cross-environment reproducibility and the full documented interaction set have not yet been verified.",
                ],
            }
        )
        payload["state_history"] = [
            entry
            for entry in payload["state_history"]
            if not (entry.get("state") == "accessioned" and entry.get("observed_at") == REVIEW_AT)
        ]
        payload["state_history"].append(
            {
                "state": "accessioned",
                "observed_at": REVIEW_AT,
                "evidence_refs": ["6529NM-ACC-2026-001", "6529NM.2026.001.GAA-01", f"6529NM.2026.001.RIGHTS.{suffix}", f"6529NM.2026.001.COND.{suffix}"],
            }
        )
        payload["preservation"].update(
            {
                "status": "in_progress",
                "package_uri": f"{REPO}/tree/main/evidence/casey-reas",
                "fixity_sha256": file_sha(EVIDENCE_MANIFEST),
                "render_environment": "Official Art Blocks generators rendered in the recorded browser viewport; self-contained generator/dependency packaging and a second independent environment remain active stewardship actions.",
                "observed_at": REVIEW_AT,
            }
        )
        payload["generator_snapshot"]["preservation_gate"] = (
            "active stewardship action: retain the assembled generator, exact project script, dependencies, "
            "on-chain inputs, and a reproducible render environment"
        )
        generator_evidence = GENERATOR_EVIDENCE[suffix]
        payload["generator_snapshot"].update(
            {
                "sha256": generator_evidence["response_sha256"],
                "dependency_observed": generator_evidence["dependency"],
                "interaction_map": generator_evidence["interaction_map"],
                "interaction_review_status": "source_reviewed_not_exhaustively_exercised",
            }
        )
        for optional_key in ("automatic_behavior", "documentation_discrepancies"):
            if optional_key in generator_evidence:
                payload["generator_snapshot"][optional_key] = generator_evidence[optional_key]
            else:
                payload["generator_snapshot"].pop(optional_key, None)
        if suffix == "06":
            payload["project"]["edition_statement"] = ROOMS_EDITION_STATEMENT
            payload["project"]["combination_structure"] = {
                "token_count": 924,
                "invocation_range": "0–923",
                "invocation_zero_code": "999999",
                "sequenced_combination_invocations": "1–923",
                "reviewed_generator_table_entries": 924,
                "object_invocation": 713,
                "object_code": "555536",
                "interpretive_boundary": "The evidence resolves the count structure but does not establish an artistic interpretation of invocation zero.",
            }
        if suffix == "07":
            payload["condition"]["narrative"] += " The reviewed generator's lowercase r/b implementation differs from the uppercase R/B platform instructions; the discrepancy is amber and must be retained in display instructions."
            payload["uncertainties"].append(
                "Platform metadata states uppercase R/B controls, while the reviewed generator implements lowercase r/b comparisons; exhibition instructions must follow the tested implementation and disclose the discrepancy."
            )
        observation = payload.get("museum_observations", {})
        if isinstance(observation, dict):
            observation["documentation_surrogate"] = "The initial official static PNG and two full-viewport screenshot hashes document time-specific surrogates. The bytes were not retained in the initial public package; CC BY-NC 4.0 now authorizes noncommercial retention with attribution, and capture is an approved preservation action."
            observation["interpretive_boundary"] = "This Museum observation fixes two observed states and supports the reviewed amber technical assessment; it is not an artist-intent claim, proof of determinism, or a declaration that autonomous preservation is complete."
        payload["references"] = sorted(set(payload.get("references", []) + ["6529NM-ACC-2026-001", f"6529NM.2026.001.RIGHTS.{suffix}", f"6529NM.2026.001.COND.{suffix}"]))
        commit_record(record)
        write(path, record)


def finalize_visual_observation() -> None:
    path = CASEY / "visual-observation-record.json"
    record = load(path)
    payload = record["payload"]
    payload.update(
        {
            "record_version": "1.1.0",
            "effective_at": REVIEW_AT,
            "record_status": "reviewed",
            "review_status": "reviewed",
            "reviewer": review(TECHNICAL_REVIEWER),
        }
    )
    payload["limitations"] = [
        "The initial PNG and screenshot bytes were not retained; their hashes and byte sizes remain historical observation evidence, and a new rights-compliant preservation capture must be identified as a later capture rather than represented as the original bytes.",
        "Static times are local post-write completion proxies; live times were recorded after both screenshots and hashing.",
        "The 1500-millisecond value is a commanded minimum wait, not measured elapsed time; per-frame times, browser version, and user agent were not captured.",
        "The observation supports an amber condition assessment but does not prove determinism, full interaction coverage, or autonomous preservation.",
    ]
    for item in payload["objects"]:
        for capture_name in ("static_capture", "live_capture"):
            retention = item[capture_name]["retention"]
            retention.update(
                {
                    "bytes_retained_in_public_repository": False,
                    "status": "not_retained_rights_cleared_preservation_action_open",
                    "statement": "The initial capture bytes were not retained. CC BY-NC 4.0 now authorizes noncommercial Museum retention with attribution; the next preservation capture will be retained as a separately dated object and will not be misrepresented as the original observation bytes.",
                }
            )
    commit_record(record)
    write(path, record)


def finalize_gaa() -> None:
    path = CASEY / "gift-acceptance-authorization.json"
    record = load(path)
    payload = record["payload"]
    payload.update(
        {
            "record_version": "1.1.0",
            "observed_at": REVIEW_AT,
            "record_status": "reviewed",
            "review_status": "reviewed",
            "reviewer": review(REGISTRAR_REVIEWER),
            "completion_blockers": [],
            "completion_boundary": {
                "current_state": "accessioned",
                "accession_status": "complete",
                "external_work_accession_certificate": "executed",
                "title_binding": "executed",
                "rights": "reviewed_with_conditions",
                "condition": "reviewed_pass_with_conditions",
                "preservation": "in_progress",
                "independent_review": "reviewed",
            },
            "non_claims": [
                "Token title does not transfer Casey REAS's copyright; the Museum relies on the object-specific CC BY-NC 4.0 license for approved noncommercial uses.",
                "Commercial use, valuation, tax treatment, aesthetic ranking, and marketplace rarity are not determined by this authorization.",
                "Ongoing software preservation and provenance enrichment are stewardship duties, not uncompleted accession decisions.",
            ],
            "references": ["6529NM.2026.001", "6529NM-ACC-2026-001"],
        }
    )
    payload["custody_receipt"]["receipt_status"] = "0x1"
    for item in payload.get("evidence_refs", []):
        if item.get("label") == "Common seven-transfer receipt evidence":
            item["notes"] = (
                "Transaction and log schedule are independently recorded. The completed accession certificate "
                "and reviewed institutional title declaration resolve legal title to the seven tokens."
            )
    payload["donor_authority_declaration"] = {
        "source_type": "user_supplied_donor_and_authority_fact",
        "statement": "The Museum accepts the user's declaration that punk6529 made a full, intentional gift of the seven scheduled tokens and the donor's entire transferable interest in them, without consideration or retained donor interest.",
        "authentication": "The declaration is recorded as the donor-and-authority fact supplied to the Museum and is corroborated by exact on-chain delivery and formal Museum acceptance.",
        "limitations": [
            "The full gift transfers token title and donor-held transferable interests; it does not assign Casey REAS's copyright.",
            "Public blockchain evidence cannot disclose every possible private claim, incapacity, or off-chain dispute; the Museum reviewed and accepted that residual risk.",
            "Commercial copyright use is not included; the reviewed Museum uses depend on CC BY-NC 4.0 or an applicable legal exception or limitation.",
        ],
    }
    for basis in payload["governing_basis"]:
        basis.update(
            {
                "observed_at": "2026-08-01T15:01:05Z",
                "effect_basis": "reviewed_governance_record",
                "governance_record_ref": "6529NM-GOV-REGISTER",
                "live_api_field": "drop_type",
                "live_api_status": "WINNER",
                "live_api_observed_at": "2026-08-01T15:01:05Z",
                "governance_effect_basis": "The reviewed governance register records adoption from the authenticated Wave API drop_type=WINNER status; rating totals and rater counts are contextual and do not determine effect.",
            }
        )
    payload["institutional_decision_authority"].update(
        {
            "documentation_qa_status": "reviewed",
            "publication_semantics": "The formal gift acceptance remains effective from 2026-08-01T22:55:00Z under direct Museum-authorized collection authority. The reviewed accession certificate records the completed title, rights, curatorial, condition, technical, and registrar determinations. Constructor and reviewer identifiers record documentary production and quality review; they do not replace or exercise the Museum's institutional decision authority.",
        }
    )
    commit_record(record)
    write(path, record)


def finalize_lot() -> None:
    path = CASEY / "accession-statement.json"
    record = load(path)
    payload = record["payload"]
    payload.update(
        {
            "record_version": "1.1.0",
            "observed_at": REVIEW_AT,
            "effective_at": REVIEW_AT,
            "record_status": "reviewed",
            "review_status": "reviewed",
            "reviewer": review(REGISTRAR_REVIEWER),
            "accession_status": "complete",
            "intake_status": "accessioned",
            "remaining_gates": [],
            "references": ["6529NM.2026.001.GAA-01", "6529NM-ACC-2026-001", "6529NM.2026.001.VO-01"],
            "ongoing_stewardship_actions": [
                {"action": "retain rights-compliant static and live documentation bytes with attribution and fixity", "status": "active", "priority": "high"},
                {"action": "capture project scripts, assembled generators, dependencies, and on-chain inputs in self-contained packages", "status": "active", "priority": "high"},
                {"action": "verify each work in at least two materially distinct render environments and document controls", "status": "active", "priority": "high"},
                {"action": "maintain redundant replicas, periodic fixity checks, recovery tests, and custody verification", "status": "active", "priority": "standing"},
                {"action": "enrich earlier provenance and reassess material rights, technical, or display changes", "status": "active", "priority": "standing"},
            ],
        }
    )
    evidence_manifest_sha256 = file_sha(EVIDENCE_MANIFEST)
    payload["source_manifest"]["evidence_manifest_sha256"] = evidence_manifest_sha256
    payload["controlled_decision"].update(
        {
            "completion_status": "complete",
            "current_state": "accessioned",
            "accession_status": "complete",
            "outcome": "approved_for_permanent_collection",
            "decision_authority": "6529NM-ACC-2026-001",
            "acceptance_date_semantics": "formal gift acceptance occurred at the stated acceptance timestamp; reviewed accession completion is recorded separately at 2026-08-02T06:30:00Z",
            "rationale": "Exact identity and custody, the donor's full gift, executed title bindings, reviewed CC BY-NC 4.0 rights, a complete curatorial case, and pass-with-conditions technical findings support permanent-collection accession. Amber software-preservation work continues as stewardship.",
        }
    )
    for item in payload.get("public_inventory", []):
        item["status"] = "accessioned"
    payload["donation_rights_schedule"]["public_summary"] = "The Museum owns the seven tokens and the donor's full transferable interest. Copyright remains separate. Object-specific CC BY-NC 4.0 metadata supports the reviewed noncommercial exhibition, documentation, publication, print, adaptation, preservation, migration/emulation, accessibility, and internal computational-research uses subject to license conditions."
    for item in payload["donation_rights_schedule"]["objects"]:
        suffix = item["object_id"].rsplit(".", 1)[1]
        item["donation_status"] = "accessioned"
        item["rights_status"] = "reviewed_with_conditions"
        item["rights_record"] = f"6529NM.2026.001.RIGHTS.{suffix}"
    payload["donation_rights_schedule"]["restricted_instrument_ref"] = {
        "content_hash": file_sha(TITLE_REVIEW),
        "custodian": "6529 Network Museum registrar record",
        "hash_algorithm": "sha256",
        "note": "Public institutional title declaration recording the accepted full gift, exact transfer, seven token identities, copyright boundary, and accepted residual private-claim risk.",
        "public_reference": "6529NM.2026.001.TITLE-01",
        "status": "executed_institutional_title_declaration",
    }
    payload["donation_rights_schedule"]["rights_matrix"] = [
        {
            "basis": "Object-specific retained Art Blocks metadata states CC BY-NC 4.0; the reviewed rights record defines the licensed material, approved noncommercial uses, attribution duties, and excluded commercial rights.",
            "grant_status": "granted_with_conditions",
            "license": "CC BY-NC 4.0",
            "object_id": item["object_id"],
            "rights_record": item["rights_record"],
        }
        for item in payload["donation_rights_schedule"]["objects"]
    ]
    preservation = payload["preservation_manifest"]
    preservation["manifest_sha256"] = evidence_manifest_sha256
    preservation["fixity_sha256"] = evidence_manifest_sha256
    preservation["active_stewardship_actions"] = [
        "capture and retain generator response bytes, project scripts, dependencies, and on-chain inputs",
        "complete two-environment render, interaction, timing, and reset verification",
        "retain attributed static and live documentation captures with fixity",
        "assign durable replicas and complete periodic fixity and recovery tests",
    ]
    preservation.pop("pending", None)
    payload["collection_curatorial_statement"].update(
        {
            "review_outcome": "approved_for_permanent_collection",
            "review_record": "records/accessions/6529NM.2026.001/public/curatorial-accession-review.md",
            "reviewed_at": REVIEW_AT,
            "reviewer": CURATORIAL_REVIEWER,
            "institutional_author": "6529 Network Museum, Curatorial Department",
            "decision_authority": "direct Museum-authorized collection authority recorded in 6529NM.2026.001.GAA-01",
            "documentation_role": "The reviewer identifier records independent documentary QA and is not the institutional decision maker.",
        }
    )
    payload["non_claims"] = [
        "Token ownership is not represented as copyright ownership.",
        "No OpenSea or other marketplace rarity metric, valuation, aesthetic ranking, or quality score is used.",
        "The three CENTURY works support comparative study but the seven-work lot is not represented as a comprehensive survey of Casey REAS's practice.",
        "Amber preservation findings are not represented as autonomous software-preservation completion.",
    ]
    payload.pop("constructor_controls", None)
    commit_record(record)
    write(path, record)


def accession_record(title_sha: str) -> dict[str, Any]:
    schedule = object_schedule()
    ids = [item["object_id"] for item in schedule]
    bindings = [
        {
            "object_id": item["object_id"],
            "status": "executed",
            "instrument_sha256": title_sha,
            "custodian_reference": "networkmuseum.6529.eth",
            "transfer_transaction": TRANSACTION,
            "block_number": BLOCK,
            "from": DONOR_ADDRESS,
            "to": MUSEUM_ADDRESS,
            "bound_at": ACCEPTED_AT,
            "basis": "Full donor gift, completed delivery, formal Museum acceptance, and reviewed institutional title declaration bound to this exact token identity and transfer log.",
        }
        for item in schedule
    ]
    custody_paths = [
        {
            "kind": "onchain_token",
            "object_id": item["object_id"],
            "from": DONOR_ADDRESS,
            "to": MUSEUM_ADDRESS,
            "custodian_reference": "networkmuseum.6529.eth",
            "instrument_reference": "6529NM.2026.001.TITLE-01",
        }
        for item in schedule
    ]
    title_uri = f"{REPO}/blob/main/records/accessions/6529NM.2026.001/public/title-rights-and-accession-review.md"
    receipt_uri = f"{REPO}/blob/main/evidence/casey-reas/raw/rpc/{RPC_RECEIPT.name}"
    payload: dict[str, Any] = {
        "record_id": "6529NM-ACC-2026-001",
        "record_type": "ACCESSION",
        "schema_id": ACCESSION_SCHEMA_ID,
        "subject_id": "6529NM-ACC-2026-001",
        "visibility": "public",
        "record_version": "1.0.0",
        "created_at": REVIEW_AT,
        "observed_at": REVIEW_AT,
        "effective_at": REVIEW_AT,
        "constructor": {"id": "codex-task:019fbd8c-2797-7ae0-91a3-672d82624fa7", "role": "constructor", "observed_at": REVIEW_AT},
        "reviewer": review(REGISTRAR_REVIEWER),
        "record_status": "reviewed",
        "review_status": "reviewed",
        "payload_sha256": "sha256:" + "0" * 64,
        "references": ["6529NM.2026.001", "6529NM.2026.001.GAA-01"] + ids,
        "evidence_refs": [
            evidence("Raw Ethereum transaction receipt", receipt_uri, "A", file_sha(RPC_RECEIPT)),
            evidence("Title, rights, and accession review", title_uri, "C", title_sha),
            evidence("Technical and condition review", f"{REPO}/blob/main/records/accessions/6529NM.2026.001/public/technical-and-condition-review.md", "C", file_sha(TECHNICAL_REVIEW)),
            evidence("Curatorial accession review", f"{REPO}/blob/main/records/accessions/6529NM.2026.001/public/curatorial-accession-review.md", "C", file_sha(CURATORIAL_REVIEW)),
        ],
        "accession_number": "6529NM.2026.001",
        "acquiring_institution": "6529 Network Museum",
        "object_ids": ids,
        "title_bindings": bindings,
        "acquisition_method": "donation",
        "acceptance_date": ACCEPTED_AT,
        "review_outcomes": {
            "institutional_authority": "effective_direct_museum_authorization_recorded_in_6529NM.2026.001.GAA-01",
            "identity_and_custody": "pass",
            "title": "pass_with_accepted_residual_private_claim_risk",
            "rights": "pass_with_cc_by_nc_4_0_conditions",
            "provenance": "pass_for_accession",
            "curatorial": "approved_for_permanent_collection",
            "condition_and_technical": "pass_with_conditions",
            "display": "ready_with_conditions",
            "preservation": "in_progress_nonblocking",
        },
        "ongoing_stewardship_actions": [
            "Retain attributed static/live documentation and self-contained generator/dependency packages.",
            "Complete two-environment render and interaction testing.",
            "Maintain redundant replicas, fixity/recovery tests, custody checks, and provenance enrichment.",
        ],
        "events": [
            {
                "event_type": "receipt",
                "occurred_at": RECEIVED_AT,
                "authority_reference": "ethereum-mainnet:25660311",
                "evidence_refs": [evidence("Raw Ethereum transaction receipt", receipt_uri, "A", file_sha(RPC_RECEIPT))],
            },
            {
                "event_type": "acceptance",
                "occurred_at": ACCEPTED_AT,
                "authority_reference": "6529NM.2026.001.GAA-01",
                "evidence_refs": [evidence("Gift Acceptance and Accession Authorization", f"{REPO}/blob/main/records/accessions/6529NM.2026.001/gift-acceptance-authorization.json", "C")],
            },
            {
                "event_type": "acquisition",
                "occurred_at": ACCEPTED_AT,
                "authority_reference": "6529NM.2026.001",
                "evidence_refs": [evidence("Reviewed accession lot", f"{REPO}/blob/main/records/accessions/6529NM.2026.001/accession-statement.json", "C")],
            },
            {
                "event_type": "title_passage",
                "occurred_at": ACCEPTED_AT,
                "authority_reference": "6529NM.2026.001.TITLE-01",
                "evidence_refs": [evidence("Institutional title declaration", title_uri, "C", title_sha)],
                "instrument": {
                    "kind": "institutional_gift_title_declaration",
                    "reference": "6529NM.2026.001.TITLE-01",
                    "sha256": title_sha,
                    "uri": title_uri,
                    "custodian_reference": "networkmuseum.6529.eth",
                },
            },
            {
                "event_type": "custody_receipt",
                "event_name": "institutional_custody_registration",
                "occurred_at": REVIEW_AT,
                "source_occurred_at": RECEIVED_AT,
                "event_semantics": "The occurred_at value dates the Museum's reviewed custody registration. The underlying on-chain receipt occurred at source_occurred_at; this record does not redate or replay that transfer.",
                "authority_reference": "6529NM.2026.001.RECEIPT-01",
                "evidence_refs": [evidence("Raw Ethereum transaction receipt", receipt_uri, "A", file_sha(RPC_RECEIPT))],
                "custody_paths": custody_paths,
            },
            {
                "event_type": "accession",
                "occurred_at": REVIEW_AT,
                "authority_reference": "6529NM-ACC-2026-001",
                "evidence_refs": [
                    evidence("Public accession certificate", f"{REPO}/blob/main/records/accessions/6529NM.2026.001/public/accession-certificate.md", "C", file_sha(ACCESSION_PUBLIC)),
                    evidence("Curatorial accession review", f"{REPO}/blob/main/records/accessions/6529NM.2026.001/public/curatorial-accession-review.md", "C", file_sha(CURATORIAL_REVIEW)),
                    evidence("Technical and condition review", f"{REPO}/blob/main/records/accessions/6529NM.2026.001/public/technical-and-condition-review.md", "C", file_sha(TECHNICAL_REVIEW)),
                ],
            },
        ],
        "source": {"lot_record": "records/accessions/6529NM.2026.001/accession-statement.json", "provenance_ontology": "Stream-compatible event/evidence/title/custody structure for externally minted works"},
    }
    payload = pin_repository_urls(payload)
    payload["payload_sha256"] = payload_sha(payload)
    return {
        "$schema": "https://6529networkmuseum.org/schemas/record-envelope-v1.json",
        "envelope": {
            "recordType": "ACCESSION",
            "subjectId": subject_hash("ACCESSION", payload["subject_id"]),
            "contentHash": {"algorithm": 1, "digest": "0x" + keccak256(canonicalize(payload)).hex(), "canonicalizationId": CANONICALIZATION_ID},
            "uri": f"{REPO}/blob/main/records/accessions/6529NM.2026.001/accession-certificate.json",
            "schemaId": ACCESSION_SCHEMA_ID,
            "signatureScheme": "0x" + "0" * 64,
            "signatureHash": {"algorithm": 2, "digest": "0x" + "0" * 64, "canonicalizationId": CANONICALIZATION_ID},
            "effectiveAt": unix_seconds(REVIEW_AT),
        },
        "payload": payload,
    }


def finalize_register() -> None:
    path = ROOT / "records" / "accessions" / "register.json"
    register = load(path)
    prior_revision = register["record_control"]["revision"]
    prior_review = register["record_control"].get("review")
    prior_payload = {key: value for key, value in register.items() if key != "record_control"}
    prior_sha = "sha256:" + hashlib.sha256(canonicalize(prior_payload)).hexdigest()
    register["snapshot_at"] = REVIEW_AT
    register["amendment_history"][0].setdefault("supersedes", register["amendment_history"][0]["prior_payload_sha256"])
    lot = register["lots"][0]
    lot.update(
        {
            "donation_status": "formally_accepted",
            "accession_status": "accessioned",
            "formal_acceptance_status": "formally_accepted",
            "accession_certificate_record": "6529NM-ACC-2026-001",
            "evidence_refs": [
                "records/accessions/6529NM.2026.001/accession-certificate.json",
                "records/accessions/6529NM.2026.001/public/title-rights-and-accession-review.md",
                "records/accessions/6529NM.2026.001/public/technical-and-condition-review.md",
                "records/accessions/6529NM.2026.001/public/curatorial-accession-review.md",
                "notes/research/casey-reas-onchain-evidence.md",
            ],
            "completion_limits": [],
            "ongoing_stewardship_actions": [
                "Self-contained generator and dependency capture",
                "Two-environment render and interaction verification",
                "Rights-compliant documentation-byte retention",
                "Replica, fixity, recovery, custody, and provenance maintenance",
            ],
        }
    )
    lot["receipt_event"]["receipt_status"] = "0x1"
    current_payload = {key: value for key, value in register.items() if key != "record_control"}
    current_sha = "sha256:" + hashlib.sha256(canonicalize(current_payload)).hexdigest()
    if current_sha != prior_sha:
        if not any(
            item.get("revision") == prior_revision and item.get("prior_payload_sha256") == prior_sha
            for item in register["amendment_history"]
        ):
            register["amendment_history"].append(
                {
                    "revision": prior_revision,
                    "superseded_at": REVIEW_AT,
                    "supersedes": prior_sha,
                    "prior_payload_sha256": prior_sha,
                    "prior_review_commit": (
                        prior_review.get("reviewed_commit")
                        if isinstance(prior_review, dict)
                        else EVIDENCE_COMMIT
                    ),
                    "reason": "Superseded the prior current-view revision with a materially changed accession state; revision identifies the superseded record, while record_control.revision identifies its successor.",
                }
            )
        register["record_control"]["revision"] = prior_revision + 1
        register["record_control"]["record_status"] = "constructed"
        register["record_control"]["constructor"]["constructed_at"] = REVIEW_AT
        register["record_control"]["review"] = None
    latest_supersession = max(
        (item["superseded_at"] for item in register["amendment_history"]),
        default=register["record_control"]["constructor"]["constructed_at"],
    )
    if register["record_control"]["constructor"]["constructed_at"] < latest_supersession:
        register["record_control"]["constructor"]["constructed_at"] = latest_supersession
    write(path, register)


def finalize_public_pages() -> None:
    def final_paragraph(descriptor_uri: str) -> str:
        return (
        "The work is `accessioned`. The reviewed title declaration establishes Museum ownership of the token and the donor's full transferable interest while keeping Casey REAS's copyright separate. "
        "The retained Art Blocks metadata states CC BY-NC 4.0, under which the Museum has approved noncommercial exhibition, documentation, publication, print, adaptation, preservation, migration/emulation, accessibility, and internal computational research subject to attribution and license conditions. "
        "Technical condition passes with amber preservation conditions: identity and metadata fixity are verified; self-contained generator/dependency capture, cross-environment rendering, fuller behavior testing, and documentation-byte retention are active collection-care work. "
        f"The [transparent linked descriptor]({descriptor_uri}) uses the published frozen source package and makes no OpenSea or marketplace rarity, aesthetic, quality, value, or ranking claim."
        )
    for path in sorted((CASEY / "public").glob("6529NM.2026.001.*.md")):
        text = path.read_text(encoding="utf-8")
        object_record = load(CASEY / "objects" / f"{path.stem}.json")
        descriptor_uri = object_record["payload"]["trait_analysis"]["descriptor"]["uri"]
        paragraph = final_paragraph(descriptor_uri)
        text = text.replace("**Status:** `received_onchain`", "**Status:** `accessioned`")
        text = text.replace(
            "The receipt establishes custody evidence; the separate [formal gift authorization](gift-acceptance-authorization.md) records acceptance. Neither record establishes legal title, rights, or display permission.",
            "The receipt establishes exact delivery and custody. The [accession certificate](accession-certificate.md) and [reviewed title declaration](title-rights-and-accession-review.md) establish Museum title to the token and approved noncommercial uses while keeping the artist's copyright separate.",
        )
        text = text.replace("not retained in the public repository pending rights and preservation review", "not retained in the initial public package; the reviewed CC BY-NC 4.0 rights now authorize an attributed preservation capture")
        marker = "The machine-readable [object record]"
        related = "Related:"
        start = text.find(marker)
        end = text.find(related, start)
        if start == -1:
            existing = text.find("The work is `accessioned`.")
            existing_end = text.find(related, existing)
            if existing >= 0 and existing_end >= 0:
                text = text[:existing] + paragraph + "\n\n" + text[existing_end:]
            elif paragraph not in text:
                raise ValueError(f"public object page lacks expected record/related boundary: {path}")
        elif end == -1:
            raise ValueError(f"public object page lacks expected related boundary: {path}")
        else:
            text = text[:start] + paragraph + "\n\n" + text[end:]
        text = text.replace(
            "Related: [gift authorization](gift-acceptance-authorization.md), [artist and practice profile](casey-reas-artist-practice.md), [collection essay](casey-reas-collection-essay.md).",
            "Related: [accession certificate](accession-certificate.md), [title and rights review](title-rights-and-accession-review.md), [technical review](technical-and-condition-review.md), [curatorial review](curatorial-accession-review.md), [artist and practice profile](casey-reas-artist-practice.md), [collection essay](casey-reas-collection-essay.md).",
        )
        path.write_text(text, encoding="utf-8", newline="\n")


def finalize_public_gaa() -> None:
    text = """# Gift Acceptance and Accession Authorization

**Lot:** `6529NM.2026.001`
**Authorization:** `6529NM.2026.001.GAA-01`
**Gift acceptance effective:** 2026-08-01T22:55:00Z
**Current outcome:** gift accepted and accession completed

The 6529 Network Museum formally accepted the full gift of seven exact Casey REAS Ethereum ERC-721 objects for the permanent collection, with public donor credit to **punk6529** and no consideration. The donor transferred the entire ownership interest in the tokens and every donor-held interest transferable with them, without a retained donor interest. All seven were delivered to `networkmuseum.6529.eth` / `0xbECfa2bA5a782D11E1a0e821E8F2e30b6684178c` in transaction `0xbdde33b32d4b70335b10cbd37c0b00a027844f14c900d82aa4f75b7a7b390498`.

The [raw RPC receipt](../../../../evidence/casey-reas/raw/rpc/eth-get-transaction-receipt-0xbdde33b32d4b70335b10cbd37c0b00a027844f14c900d82aa4f75b7a7b390498.json) and [request/acquisition record](../../../../evidence/casey-reas/raw/rpc/receipt-acquisition.json) preserve the exact block, status, contracts, token IDs, log indices, sender, and Museum destination. The authorization applies the adopted Art Blocks donation preapproval (`6529NM-GOV-1052156`) and Donation Acceptance Policy (`6529NM-GOV-1052812`) to those exact identities.

## Completed accession

The authorization was the first-stage acceptance record. The later [accession certificate](accession-certificate.md) completes the institutional decision and binds an executed title declaration, rights review, curatorial judgment, condition and technical review, provenance schedule, and each exact transfer. The lot and seven objects are now `accessioned`; no accession blocker remains.

The Museum owns the tokens, not Casey REAS's copyright. Each retained Art Blocks metadata response states `CC BY-NC 4.0`. The [title and rights review](title-rights-and-accession-review.md) approves the Museum's noncommercial exhibition, documentation, publication, print, adaptation, preservation, migration/emulation, accessibility, and internal computational-research uses subject to attribution and license conditions. Commercial use is not approved.

The [technical and condition review](technical-and-condition-review.md) passes the lot with conditions: chain identity and retained metadata fixity are green; generator packaging, dependencies, cross-environment rendering, behavior coverage, documentation-byte retention, and autonomous preservation are amber active stewardship areas. The [curatorial review](curatorial-accession-review.md), [artist profile](casey-reas-artist-practice.md), and [collection essay](casey-reas-collection-essay.md) complete the scholarly case.

Institutional authority for the gift acceptance and accession is the direct Museum-authorized collection decision recorded in the machine authorization and accession certificate. Constructor and reviewer identifiers preserve authorship and independent documentary QA; they are not substitutes for, and do not exercise, the Museum's collection authority.

No valuation, tax treatment, commercial license, OpenSea or marketplace rarity metric, aesthetic ranking, or claim of comprehensive representation of the artist's practice is made.
"""
    (CASEY / "public" / "gift-acceptance-authorization.md").write_text(text, encoding="utf-8", newline="\n")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Materialize the reviewed Casey REAS accession records from the final public determinations."
    )
    parser.parse_args()
    required = [TITLE_REVIEW, TECHNICAL_REVIEW, CURATORIAL_REVIEW, ACCESSION_PUBLIC, EVIDENCE_MANIFEST, RPC_RECEIPT]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise SystemExit("missing required accession inputs: " + ", ".join(missing))
    title_sha = file_sha(TITLE_REVIEW)
    finalize_rights()
    finalize_condition()
    finalize_objects(title_sha)
    finalize_visual_observation()
    finalize_gaa()
    finalize_lot()
    write(CASEY / "accession-certificate.json", accession_record(title_sha))
    finalize_register()
    finalize_public_pages()
    finalize_public_gaa()
    print("Casey REAS accession finalized as reviewed and accessioned.")


if __name__ == "__main__":
    main()
