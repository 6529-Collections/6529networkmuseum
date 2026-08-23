#!/usr/bin/env python3
"""Seal the Vera Molnár accession records into Stream-compatible envelopes."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime
from pathlib import Path
import re
from typing import Any

from canonical import canonicalize
from validate import keccak256


ROOT = Path(__file__).resolve().parents[1]
ACCESSION = ROOT / "records" / "accessions" / "6529NM.2026.003"
WAVE_STATUS = (
    ROOT
    / "records"
    / "proposed-gifts"
    / "6529NM-PG-2026-002"
    / "wave-status-observation.json"
)
REPO = "https://github.com/6529-Collections/6529networkmuseum"
CANONICALIZATION_ID = "0x886c7c89c308c459ca8a626e0ef36a5ea9f4c7a7b56aaf86c71a2ddf3b4f9044"
ZERO_HASH = "0x" + "0" * 64
BAD_MUSEUM_ADDRESS = "0xbecfa2b5a782d11e1a0e821e8f2e30b6684178c"
MUSEUM_ADDRESS = "0xbecfa2ba5a782d11e1a0e821e8f2e30b6684178c"
OLD_SOURCE_MANIFEST = "sha256:45953b19bcd9d51d476de6d73d2033030ac163b8568bf9ba5dd558cd78778688"
SOURCE_MANIFEST = "sha256:71fb6066e1113e22c8586e195bfb8d553dcc8c4d7dec5b33de3ae47d3ebcafe5"
TECHNICAL_MANIFEST = "sha256:da5fb28d5c55bc0ae480bf76582e0f47d1db246f4cdd691aa1b2ae162e1d4ccb"
TITLE_INSTRUMENT = {
    "accession_number": "6529NM.2026.003",
    "object_id": "6529NM.2026.003.01",
    "gift_authority": "6529NM.2026.003.GAA-01",
    "donor": "punk6529",
    "recipient": "6529 Network Museum",
    "caip19": "eip155:1/erc721:0xe034bb2b1b9471e11cf1a0a9199a156fb227aa5d/210",
    "interest": "the donor's transferable interest in the exact ERC-721 token",
}
TITLE_INSTRUMENT_SHA256 = "sha256:" + hashlib.sha256(canonicalize(TITLE_INSTRUMENT)).hexdigest()


def load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: JSON root must be an object")
    return value


def rewrite(value: Any) -> Any:
    if isinstance(value, str):
        if value.lower() == BAD_MUSEUM_ADDRESS:
            return MUSEUM_ADDRESS
        if value == OLD_SOURCE_MANIFEST:
            return SOURCE_MANIFEST
        if value == (
            "https://token.artblocks.io/1/"
            "0xe034bb2b1b9471e11cf1a0a9199a156fb227aa5d/210"
        ):
            return (
                "https://token.artblocks.io/"
                "0xe034bb2b1b9471e11cf1a0a9199a156fb227aa5d/210"
            )
        return value
    if isinstance(value, list):
        return [rewrite(item) for item in value if item != "6529NM.2026.003.VO-01"]
    if isinstance(value, dict):
        return {key: rewrite(item) for key, item in value.items()}
    return value


def payload_sha(payload: dict[str, Any]) -> str:
    material = {key: value for key, value in payload.items() if key != "payload_sha256"}
    return "sha256:" + hashlib.sha256(canonicalize(material)).hexdigest()


def subject_hash(record_type: str, subject_id: str) -> str:
    material = f"6529networkmuseum.subject.{record_type.lower()}.v1:{subject_id}".encode()
    return "0x" + keccak256(material).hex()


def unix_seconds(value: str) -> int:
    return int(datetime.fromisoformat(value.replace("Z", "+00:00")).timestamp())


def normalize_payload(
    payload: dict[str, Any],
    path: Path,
    review: dict[str, str] | None = None,
    *,
    pending: bool = False,
) -> dict[str, Any]:
    payload = rewrite(payload)
    payload["payload_sha256"] = "sha256:" + "0" * 64

    if pending:
        payload["reviewer"] = None
        payload["record_status"] = "review_pending"
        payload["review_status"] = "pending_independent_review"
    elif review is not None:
        created_at = datetime.fromisoformat(
            str(payload["created_at"]).replace("Z", "+00:00")
        )
        reviewed_at = datetime.fromisoformat(
            review["reviewed_at"].replace("Z", "+00:00")
        )
        if reviewed_at <= created_at:
            raise ValueError("--reviewed-at must be after every record's created_at")
        payload["reviewer"] = {
            "id": review["reviewer_id"],
            "role": "reviewer",
            "reviewed_at": review["reviewed_at"],
            "reviewed_manifest_sha256": review["reviewed_manifest_sha256"],
            "reviewed_manifest_keccak": review["reviewed_manifest_keccak"],
            "reviewed_commit": review["reviewed_commit"],
            "reviewer_ids": [review["reviewer_id"]],
            "outcome": "approved",
        }
        payload["record_status"] = "reviewed"
        payload["review_status"] = "reviewed"

    def bind_title(value: Any) -> None:
        if isinstance(value, dict):
            if "instrument_sha256" in value:
                value["instrument_sha256"] = TITLE_INSTRUMENT_SHA256
            if value.get("kind") == "institutional_gift_title_declaration":
                value["sha256"] = TITLE_INSTRUMENT_SHA256
            for item in value.values():
                bind_title(item)
        elif isinstance(value, list):
            for item in value:
                bind_title(item)

    bind_title(payload)

    if path == WAVE_STATUS:
        wave_url = (
            "https://6529.io/waves/5f207393-5418-4a75-8738-e40edb44a94d"
            "?drop=d09d3c3b-d354-4e39-9e1f-1e676e3cb62e"
        )
        payload["evidence_refs"] = [
            {
                "evidence_class": "B",
                "label": "Original PARTICIPATORY proposal observation",
                "observed_at": "2026-08-13T19:19:40.216Z",
                "uri": wave_url,
            },
            {
                "evidence_class": "B",
                "label": "Wave API WINNER status readback (is_signed=true)",
                "observed_at": "2026-08-23T09:40:25.465Z",
                "uri": wave_url,
            },
        ]
        payload.pop("signed", None)
        payload["api_reported_is_signed"] = True
        payload["observation_method"] = "wave_api_status_readback"
        payload["prior_observation"] = {
            "source_status": "PARTICIPATORY",
            "observed_at": "2026-08-13T19:19:40.216Z",
            "source_record_id": "6529NM-PG-2026-002",
            "source_record_path": None,
            "source_repository_visibility": "complete_manifest_only",
            "source_url": wave_url,
        }
        payload["non_effects"] = [
            "acceptance_not_established",
            "transfer_not_established",
            "title_not_established",
            "custody_not_established",
            "rights_not_established",
            "technical_not_established",
            "preservation_not_established",
            "accession_not_established",
            "collection_membership_not_established",
        ]

    if path.name == "6529NM.2026.003.01.json" and path.parent.name == "objects":
        chain = payload.get("chain_identity")
        if isinstance(chain, dict):
            chain["metadata_uri"] = (
                "https://token.artblocks.io/"
                "0xe034bb2b1b9471e11cf1a0a9199a156fb227aa5d/210"
            )
            chain.pop("generator_sha256", None)
        payload.pop("museum_observations", None)
        payload.pop("visual_observation_record", None)
        history = payload.get("state_history")
        if isinstance(history, list):
            for item in history:
                if isinstance(item, dict) and item.get("state") == "received_onchain":
                    item["observed_at"] = str(payload["effective_at"])
            state_order = {"offered": 0, "authorized": 1, "acquired": 2, "received_onchain": 3, "accessioned": 4}
            history.sort(
                key=lambda item: (
                    str(item.get("observed_at", "")),
                    state_order.get(str(item.get("state", "")), 99),
                )
            )
        condition = payload.get("condition")
        if isinstance(condition, dict):
            condition["method"] = (
                "Reviewed the exact token, finalized ownership, retained metadata and preview, "
                "and the on-chain project script package."
            )
            condition["narrative"] = (
                "Token identity, hash, finalized custody, and the locked on-chain project script "
                "are verified. Art Blocks metadata and generator endpoints remain service dependencies."
            )
        preservation = payload.get("preservation")
        if isinstance(preservation, dict):
            preservation["fixity_sha256"] = SOURCE_MANIFEST
            preservation["render_environment"] = (
                "The live Art Blocks generator remains the primary browser display. The Museum retains "
                "the official still and the exact on-chain script package."
            )
        payload["state_history_semantics"] = (
            "Lifecycle observed_at values record when the Museum verified and entered each "
            "institutional state. The on-chain receipt transaction occurred earlier, at "
            "2026-08-23T09:27:59Z, and is preserved separately in chain_identity and the "
            "custody evidence package."
        )

    if path.name == "accession-statement.json":
        preservation_manifest = payload.get("preservation_manifest")
        if isinstance(preservation_manifest, dict):
            preservation_manifest["active_stewardship_actions"] = [
                "retain dated runtime and service captures",
                "repeat rendering in a second environment and record the results",
            ]
        payload["remaining_gates"] = []

    if path.name == "6529NM.2026.003.01.json" and path.parent.name == "technical":
        events = payload.get("events")
        if isinstance(events, list) and events and isinstance(events[0], dict):
            events[0]["evidence_refs"] = [
                {
                    "evidence_class": "A",
                    "label": "Finalized custody summary",
                    "observed_at": str(payload["effective_at"]),
                    "sha256": "sha256:a4f3b10199b566c619c164e352be85072bb71197e2328834ab2d6f2efdd5987b",
                    "uri": f"{REPO}/blob/main/evidence/vera-molnar-210-custody/summary.json",
                },
                {
                    "evidence_class": "A",
                    "label": "Official source-evidence manifest",
                    "observed_at": str(payload["effective_at"]),
                    "sha256": SOURCE_MANIFEST,
                    "uri": f"{REPO}/blob/main/evidence/vera-molnar-210-sources/manifest.json",
                },
                {
                    "evidence_class": "A",
                    "label": "On-chain project technical manifest",
                    "observed_at": str(payload["effective_at"]),
                    "sha256": TECHNICAL_MANIFEST,
                    "uri": f"{REPO}/blob/main/evidence/vera-molnar-210-technical/manifest.json",
                },
            ]

    if path.name == "gift-acceptance-authorization.json":
        completion = payload.get("completion_boundary")
        if isinstance(completion, dict):
            completion.pop("responsive_media_presentation", None)
        payload["source"] = {
            "source_record_ids": [
                "6529NM-PG-2026-002",
                "6529NM-WAVE-OBS-2026-08-23-002",
            ]
        }
        blockers = payload.get("completion_blockers")
        if isinstance(blockers, list):
            payload["completion_blockers"] = [
                item for item in blockers if item != "responsive_media_presentation_v2_handoff"
            ]

    if path.name == "accession-certificate.json":
        actions = payload.get("ongoing_stewardship_actions")
        if isinstance(actions, list):
            payload["ongoing_stewardship_actions"] = [
                item for item in actions if item != "complete responsive media presentation handoff"
            ]

    payload["payload_sha256"] = payload_sha(payload)
    return payload


def seal(
    path: Path, review: dict[str, str] | None = None, *, pending: bool = False
) -> dict[str, Any]:
    source = load(path)
    payload_source = source.get("payload")
    if isinstance(payload_source, dict):
        payload = payload_source
    else:
        payload = {key: value for key, value in source.items() if key != "$schema"}
    payload = normalize_payload(payload, path, review, pending=pending)
    record_type = str(payload["record_type"])
    subject_id = str(payload["subject_id"])
    schema_id = str(payload["schema_id"])
    relative = path.relative_to(ROOT).as_posix()
    envelope = {
        "recordType": record_type,
        "subjectId": subject_hash(record_type, subject_id),
        "contentHash": {
            "algorithm": 1,
            "digest": "0x" + keccak256(canonicalize(payload)).hex(),
            "canonicalizationId": CANONICALIZATION_ID,
        },
        "uri": f"{REPO}/blob/main/{relative}",
        "schemaId": schema_id,
        "signatureScheme": ZERO_HASH,
        "signatureHash": {
            "algorithm": 2,
            "digest": ZERO_HASH,
            "canonicalizationId": CANONICALIZATION_ID,
        },
        "effectiveAt": unix_seconds(str(payload["effective_at"])),
    }
    return {
        "$schema": "https://6529networkmuseum.org/schemas/record-envelope-v1.json",
        "envelope": envelope,
        "payload": payload,
    }


def encoded(value: dict[str, Any]) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    state = parser.add_mutually_exclusive_group()
    state.add_argument("--pending", action="store_true")
    state.add_argument("--reviewed", action="store_true")
    parser.add_argument("--reviewer-id")
    parser.add_argument("--reviewed-at")
    parser.add_argument("--reviewed-commit")
    parser.add_argument("--reviewed-manifest-sha256")
    parser.add_argument("--reviewed-manifest-keccak")
    args = parser.parse_args()
    review_fields = {
        "reviewer_id": args.reviewer_id,
        "reviewed_at": args.reviewed_at,
        "reviewed_commit": args.reviewed_commit,
        "reviewed_manifest_sha256": args.reviewed_manifest_sha256,
        "reviewed_manifest_keccak": args.reviewed_manifest_keccak,
    }
    explicit_review_fields = any(value is not None for value in review_fields.values())
    if not args.reviewed and explicit_review_fields:
        parser.error("review binding arguments require --reviewed")
    review: dict[str, str] | None = None
    if args.reviewed:
        if not all(isinstance(value, str) and value for value in review_fields.values()):
            parser.error("--reviewed requires every review binding argument")
        review = {key: str(value) for key, value in review_fields.items()}
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._:-]{2,127}", review["reviewer_id"]):
            parser.error("--reviewer-id is not a valid Museum actor ID")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z", review["reviewed_at"]):
            parser.error("--reviewed-at must be a canonical RFC 3339 UTC timestamp")
        if not re.fullmatch(r"[0-9a-f]{40}", review["reviewed_commit"]):
            parser.error("--reviewed-commit must be 40 lowercase hexadecimal characters")
        if not re.fullmatch(r"sha256:[0-9a-f]{64}", review["reviewed_manifest_sha256"]):
            parser.error("--reviewed-manifest-sha256 must be sha256:<64 lowercase hex>")
        if not re.fullmatch(r"0x[0-9a-f]{64}", review["reviewed_manifest_keccak"]):
            parser.error("--reviewed-manifest-keccak must be 0x<64 lowercase hex>")
    paths = sorted(
        path
        for path in ACCESSION.rglob("*.json")
        if path.name != "presentation-manifest.json"
    )
    paths.append(WAVE_STATUS)
    stale: list[str] = []
    for path in paths:
        expected = encoded(seal(path, review, pending=args.pending))
        if args.check:
            if path.read_bytes() != expected:
                stale.append(path.relative_to(ROOT).as_posix())
        else:
            path.write_bytes(expected)
    if stale:
        raise SystemExit("stale Vera accession commitments: " + ", ".join(stale))
    print(f"Vera accession commitments are current: {len(paths)} records")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
