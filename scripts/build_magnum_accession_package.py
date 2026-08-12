#!/usr/bin/env python3
"""Build the completed Magnum Photos 75 accession package.

The custody summary is an input, never an accession authority. It binds the
five token identities and delivery receipts to the public accession record;
the institutional title basis remains the donor's full-gift declaration and
the Museum maintainer's completion instruction.
"""

from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import migrate_public_entities as migration  # noqa: E402


ACCESSION = "6529NM.2026.002"
CERTIFICATE_ID = "6529NM-ACC-2026-002"
GAA_ID = f"{ACCESSION}.GAA-01"
TITLE_ID = f"{ACCESSION}.TITLE-01"
MUSEUM = "0xbecfa2ba5a782d11e1a0e821e8f2e30b6684178c"
DONOR = "0x6daa633c23615a29471deafae351727867e7dad1"
CONTRACT = "0xe628b59d34f42b16c53f4d697f1ffd4d8d987b91"
PROPOSAL_ID = "6529NM-PG-2026-001"
ACQUISITION_ID = "6529NM-CA-2026-003"
WINNER_OBSERVATION_ID = migration.WINNER_OBSERVATION_ID
SUMMARY_RELATIVE = "evidence/magnum-75-custody/summary.json"
CONSTRUCTOR_ID = "codex-task:magnum-completed-accession-correction"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def write_text(relative: str, value: str) -> str:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    encoded = (value.rstrip() + "\n").encode("utf-8")
    path.write_bytes(encoded)
    return f"sha256:{sha256_bytes(encoded)}"


def write_json(relative: str, value: Any) -> None:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_enveloped(relative: str, payload: dict[str, Any]) -> None:
    envelope = migration.finalize(payload, relative, False, None)
    envelope["envelope"]["subjectId"] = migration.keccak256(
        (
            f"6529networkmuseum.subject.{payload['record_type'].lower()}.v1:"
            f"{payload['subject_id']}"
        ).encode("utf-8")
    )
    write_json(relative, envelope)


def source_head() -> str:
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
    ).strip()


def common_fields(
    template: dict[str, Any],
    record_id: str,
    record_type: str,
    subject_id: str,
    observed_at: str,
    references: list[str],
    evidence_refs: list[dict[str, Any]],
) -> dict[str, Any]:
    payload = deepcopy(template)
    payload.update(
        {
            "record_id": record_id,
            "record_type": record_type,
            "subject_id": subject_id,
            "visibility": "public",
            "record_version": "1.0.0",
            "created_at": observed_at,
            "observed_at": observed_at,
            "effective_at": observed_at,
            "constructor": {
                "id": CONSTRUCTOR_ID,
                "role": "constructor",
                "observed_at": observed_at,
            },
            "reviewer": None,
            "record_status": "review_pending",
            "review_status": "pending_independent_review",
            "payload_sha256": "sha256:" + "0" * 64,
            "references": sorted(set(references)),
            "evidence_refs": evidence_refs,
        }
    )
    return payload


def reset_review_state(payload: dict[str, Any], observed_at: str) -> None:
    """Mark a materially amended record as constructed and awaiting review."""
    payload["constructor"] = {
        "id": CONSTRUCTOR_ID,
        "role": "constructor",
        "observed_at": observed_at,
    }
    payload["created_at"] = observed_at
    payload["observed_at"] = observed_at
    payload["effective_at"] = observed_at
    payload["reviewer"] = None
    payload["record_status"] = "review_pending"
    payload["review_status"] = "pending_independent_review"
    payload["record_version"] = "1.0.0"


def github_uri(relative: str) -> str:
    return migration.github_uri(relative)


def amend_machine_record(
    relative: str,
    observed_at: str,
    update: Any,
) -> None:
    """Append one deterministic current-state amendment to a Magnum machine view."""
    path = ROOT / relative
    record = load_json(path)
    already_current = (
        record.get("record_control", {}).get("constructor", {}).get("actor_id")
        == CONSTRUCTOR_ID
    )
    if not already_current:
        prior_revision = int(record["record_control"]["revision"])
        prior_payload = {
            key: value
            for key, value in record.items()
            if key not in {"record_control", "amendment_history"}
        }
        prior_sha = "sha256:" + sha256_bytes(migration.canonicalize(prior_payload))
        record.setdefault("amendment_history", []).append(
            {
                "revision": prior_revision,
                "superseded_at": observed_at,
                "supersedes": prior_sha,
                "prior_payload_sha256": prior_sha,
            }
        )
        record["record_control"] = {
            "revision": prior_revision + 1,
            "record_status": "constructed",
            "constructor": {
                "actor_id": CONSTRUCTOR_ID,
                "role": "constructor",
                "constructed_at": observed_at,
            },
            "review": None,
        }
    update(record)
    write_json(relative, record)


def raw_evidence_ref(
    observation: dict[str, Any], needle: str, observed_at: str, label: str
) -> dict[str, Any]:
    raw = next(
        item
        for item in observation["raw_evidence"]
        if needle in str(item.get("path"))
    )
    evidence_path = (
        Path(SUMMARY_RELATIVE).parent / str(raw["path"])
    ).as_posix()
    ref = migration.evidence(label, evidence_path, observed_at, "A")
    ref["sha256"] = raw["sha256"]
    return ref


def build() -> None:
    proposal = load_json(
        ROOT / "records/proposed-gifts/6529NM-PG-2026-001/proposal.json"
    )
    summary_path = ROOT / SUMMARY_RELATIVE
    if not summary_path.is_file():
        raise RuntimeError(
            "run scripts/acquire_magnum_custody_evidence.py after finality reaches block 25741724"
        )
    summary = load_json(summary_path)
    observation = summary.get("observation", summary)
    finalized = observation.get("finalized_block")
    if not isinstance(finalized, dict) or int(finalized.get("number", 0)) < 25741724:
        raise RuntimeError(
            "custody summary is not bound to a finalized block at or after 25741724"
        )
    observed_at = str(observation["observed_at"])
    final_block = int(finalized["number"])
    final_hash = str(finalized["hash"])
    final_time = str(finalized["timestamp"])
    summary_sha = f"sha256:{sha256_bytes(summary_path.read_bytes())}"
    summary_ref = migration.evidence(
        "Finalized Magnum custody observation", SUMMARY_RELATIVE, observed_at, "A"
    )
    summary_ref["sha256"] = summary_sha

    proposal_objects = proposal["objects"]
    custody_objects = {
        item["candidate_object_id"]: item for item in observation["objects"]
    }
    if len(proposal_objects) != 5 or len(custody_objects) != 5:
        raise RuntimeError("Magnum accession requires exactly five objects")
    if any(
        item.get("owner", "").lower() != MUSEUM
        for item in custody_objects.values()
    ):
        raise RuntimeError(
            "not every Magnum token is owned by the Museum at the common finalized block"
        )

    casey_cert = load_json(
        ROOT / "records/accessions/6529NM.2026.001/accession-certificate.json"
    )["payload"]
    casey_object = load_json(
        ROOT / "records/accessions/6529NM.2026.001/objects/6529NM.2026.001.01.json"
    )["payload"]
    casey_rights = load_json(
        ROOT / "records/accessions/6529NM.2026.001/rights/6529NM.2026.001.RIGHTS.01.json"
    )["payload"]
    casey_condition = load_json(
        ROOT / "records/accessions/6529NM.2026.001/technical/6529NM.2026.001.01.json"
    )["payload"]
    casey_gaa = load_json(
        ROOT / "records/accessions/6529NM.2026.001/gift-acceptance-authorization.json"
    )["payload"]
    title_review_rel = (
        f"records/accessions/{ACCESSION}/public/title-rights-and-accession-review.md"
    )
    title_review_sha = write_text(
        title_review_rel,
        f"""# Title, rights, and accession review

**Accession lot:** {ACCESSION}  
**Gift:** Conflict at Its Edges, five photographs from Magnum Photos 75  
**Donor:** punk6529  
**Status:** accepted and accessioned into the permanent Collection

## Title basis

The donor offered the five scheduled tokens as a full gift. The Museum
maintainer instructed the Museum to record the gift as accepted and accessioned.
The five transfer receipts identify delivery from the donor address to
networkmuseum.6529.eth; the custody package records the receipts, their
Transfer logs, and the common finalized-block ownerOf observation.

The Museum's title record therefore covers the donor's transferable interest in
the five tokenized objects. This public record derives that determination from
the full-gift offer and the maintainer's instruction. It does not cite a
separate private instrument.

## Rights position

The source records identify the photographs as All Rights Reserved and credit
each artist and Magnum Photos. The gift transfers the tokenized objects and the
donor's transferable interest in them; it does not transfer copyright or
create a general reproduction licence. The Museum's public presentation is
limited to the credited accession context and remains subject to the source
rights position.

## Supporting records

- Gift acceptance and accession authorization
- Accession certificate
- Finalized custody evidence
- Source and rights record
""",
    )

    proposal_ref = migration.source_evidence(
        "Original proposed gift and full-gift offer", PROPOSAL_ID, observed_at
    )
    status_rel = (
        "records/proposed-gifts/6529NM-PG-2026-001/public/status-amendments/"
        "2026-08-12-accession-completed.md"
    )
    status_ref = migration.source_evidence(
        "Public accession status", status_rel, observed_at
    )
    title_uri = github_uri(title_review_rel)
    object_rows: list[dict[str, Any]] = []

    for index, proposal_object in enumerate(proposal_objects, start=1):
        candidate_id = proposal_object["candidate_object_id"]
        custody = custody_objects[candidate_id]
        object_id = f"{ACCESSION}.{index:02d}"
        rights_id = f"{ACCESSION}.RIGHTS.{index:02d}"
        condition_id = f"{ACCESSION}.COND.{index:02d}"
        candidate_ref = migration.source_evidence(
            "Proposed object record", candidate_id, observed_at
        )
        receipt_ref = raw_evidence_ref(
            observation,
            f"receipt-{custody['token_id']}",
            observed_at,
            f"Ethereum receipt for token {custody['token_id']}",
        )
        evidence_refs = [summary_ref, receipt_ref, proposal_ref, candidate_ref, status_ref]

        rights_grants: dict[str, dict[str, str]] = {}
        for grant in (
            "reproduction",
            "publication",
            "exhibition",
            "print",
            "derivative_use",
            "ai_training",
            "preservation",
            "migration_emulation",
            "accessibility",
        ):
            if grant in {"reproduction", "publication", "exhibition", "preservation", "migration_emulation", "accessibility"}:
                grant_status = "granted_with_conditions"
                basis = (
                    "The Museum interprets its acquisition of the tokenized object "
                    "as carrying the ordinary institutional right to display, "
                    "publish, and make the work accessible in a credited museum "
                    "context. This position does not transfer copyright or create "
                    "a commercial or general reproduction licence."
                )
            else:
                grant_status = "denied"
                basis = (
                    "The source record states All Rights Reserved. The accession "
                    "records no general grant for this use."
                )
            rights_grants[grant] = {
                "grant_status": grant_status,
                "observed_at": observed_at,
                "basis": basis,
                "evidence_ref": TITLE_ID if grant_status == "granted_with_conditions" else candidate_id,
            }

        title_binding = {
            "object_id": object_id,
            "status": "executed",
            "instrument_sha256": title_review_sha,
            "custodian_reference": "networkmuseum.6529.eth",
            "transfer_transaction": custody["tx_hash"],
            "block_number": custody["block_number"],
            "from": DONOR,
            "to": MUSEUM,
            "bound_at": observed_at,
            "basis": (
                "The donor's full-gift offer and the Museum maintainer's completion "
                "instruction, corroborated by the exact transfer receipt for this "
                "token, bind the donor's transferable token interest to this "
                "accession object."
            ),
        }

        rights_payload = common_fields(
            casey_rights,
            rights_id,
            "RIGHTS_STATEMENT",
            object_id,
            observed_at,
            [ACCESSION, CERTIFICATE_ID, object_id],
            evidence_refs,
        )
        rights_payload["subject_id"] = rights_id
        rights_payload["object_id"] = object_id
        rights_payload.update(
            {
                "schema_id": casey_rights["schema_id"],
                "rights_holder_reference": f"{proposal_object['artist']} / Magnum Photos",
                "basis": (
                    "The source metadata and public proposal identify the photograph "
                    "as All Rights Reserved. The Museum interprets acquisition as "
                    "including ordinary credited museum display, publication, and "
                    "accessibility uses; copyright ownership, commercial reproduction, "
                    "derivative use, licensing, and AI training remain separate."
                ),
                "grants": rights_grants,
                "events": [
                    {
                        "event_id": f"{rights_id}.EVENT.rights_assertion.{final_block}",
                        "event_type": "rights_assertion",
                        "occurred_at": observed_at,
                        "authority_reference": CERTIFICATE_ID,
                        "evidence_refs": [candidate_ref, status_ref],
                    }
                ],
                "source": {"source_record_ids": [PROPOSAL_ID, CERTIFICATE_ID]},
            }
        )
        write_enveloped(
            f"records/accessions/{ACCESSION}/rights/{rights_id}.json",
            rights_payload,
        )

        condition_payload = common_fields(
            casey_condition,
            condition_id,
            "CONDITION_REPORT",
            object_id,
            observed_at,
            [ACCESSION, CERTIFICATE_ID, object_id],
            evidence_refs,
        )
        condition_payload["subject_id"] = condition_id
        condition_payload["object_id"] = object_id
        condition_payload.update(
            {
                "schema_id": casey_condition["schema_id"],
                "protocol_state": (
                    "ERC-721 photographic object; no executable generator or "
                    "software dependency is asserted."
                ),
                "assessments": {
                    "token": "green",
                    "metadata": "green",
                    "script": "not_applicable",
                    "dependencies": "not_applicable",
                    "rendering": "green",
                    "behavior": "not_applicable",
                    "documentation": "amber",
                },
                "method": (
                    "Reviewed the source metadata, source image reference, transfer "
                    "receipt, Transfer log, and ownerOf result at the common "
                    "finalized block."
                ),
                "outcome": (
                    "Documented photographic token; source-image retention, "
                    "independent review, and continuing rights stewardship remain "
                    "active."
                ),
                "events": [
                    {
                        "event_id": f"{condition_id}.EVENT.condition_assessment.{final_block}",
                        "event_type": "condition_assessment",
                        "occurred_at": observed_at,
                        "authority_reference": CERTIFICATE_ID,
                        "evidence_refs": [summary_ref, candidate_ref],
                    }
                ],
                "source": {"source_record_ids": [PROPOSAL_ID, CERTIFICATE_ID]},
            }
        )
        write_enveloped(
            f"records/accessions/{ACCESSION}/technical/{object_id}.json",
            condition_payload,
        )

        image = proposal_object["image"]
        provenance = proposal_object.get("provenance", {}).get("transfers", [])
        mint = next((item for item in provenance if item.get("role") == "mint"), None)
        object_payload = deepcopy(casey_object)
        for key in ("project", "metadata_snapshot", "generator_snapshot", "trait_analysis"):
            object_payload.pop(key, None)
        object_payload.update(
            {
                "record_id": object_id,
                "record_type": "WORK_DESCRIPTION",
                "schema_id": casey_object["schema_id"],
                "subject_id": object_id,
                "object_id": object_id,
                "accession_lot_id": ACCESSION,
                "title": proposal_object["title"],
                "creator": proposal_object["artist"],
                "artist": {
                    "claim_type": "source_credit",
                    "evidence_class": "B",
                    "preferred_name": proposal_object["artist"],
                    "source_refs": [candidate_id],
                },
                "medium": "photograph (source image presented from the credited external source)",
                "credit_line": (
                    f"Gift of punk6529. {proposal_object['artist']}, "
                    f"{proposal_object['title']}, {proposal_object['date']}. "
                    f"{proposal_object['rights']['copyright_notice']}"
                ),
                "chain_identity": {
                    "caip19": custody["caip19"],
                    "chain_id": 1,
                    "contract": CONTRACT,
                    "token_id": str(custody["token_id"]),
                    "token_standard": "ERC-721",
                    "mint_transaction": (mint or {}).get("tx_hash", "0x" + "0" * 64),
                    "acquisition_transaction": custody["tx_hash"],
                    "custody_receipt_transaction": custody["tx_hash"],
                    "custody_receipt_block": custody["block_number"],
                    "custody_receipt_log": custody["log_index"],
                    "custody_account": f"eip155:1:{MUSEUM}",
                    "custody_status": "verified",
                    "custody_verified_at": observed_at,
                    "custody_block": final_block,
                },
                "title_binding": title_binding,
                "rights": rights_grants,
                "condition": {
                    "token": "green",
                    "metadata": "green",
                    "script": "not_applicable",
                    "dependencies": "not_applicable",
                    "rendering": "green",
                    "behavior": "not_applicable",
                    "documentation": "amber",
                    "protocol_state": (
                        "ERC-721 photographic object; no executable generator "
                        "or software dependency is asserted."
                    ),
                    "method": (
                        "Reviewed source metadata, image reference, chain receipt, "
                        "and common finalized-block ownership observation."
                    ),
                    "narrative": (
                        "The object is catalogued and displayable in the credited "
                        "accession context. Source-image retention and rights "
                        "stewardship remain active."
                    ),
                    "observed_at": observed_at,
                },
                "current_state": "accessioned",
                "state_history": [
                    {
                        "state": "offered",
                        "observed_at": migration.PROPOSAL_AT,
                        "evidence_refs": [PROPOSAL_ID],
                    },
                    {
                        "state": "authorized",
                        "observed_at": migration.WINNER_AT,
                        "evidence_refs": [WINNER_OBSERVATION_ID],
                    },
                    {
                        "state": "acquired",
                        "observed_at": observed_at,
                        "evidence_refs": [GAA_ID],
                    },
                    {
                        "state": "received_onchain",
                        "observed_at": observed_at,
                        "evidence_refs": [GAA_ID, WINNER_OBSERVATION_ID],
                    },
                    {
                        "state": "accessioned",
                        "observed_at": observed_at,
                        "evidence_refs": [CERTIFICATE_ID, rights_id, condition_id],
                    },
                ],
                "state_history_semantics": (
                    "The source proposal, token delivery, and Museum accession are "
                    "recorded as separate historical states. The common finalized "
                    "observation confirms current custody; it does not replace "
                    "the institutional accession decision."
                ),
                "preservation": {
                    "status": "in_progress",
                    "package_uri": image["uri"],
                    "fixity_sha256": image["sha256"],
                    "render_environment": (
                        "Museum source-image presentation; preservation master and "
                        "source-byte retention remain stewardship actions."
                    ),
                    "observed_at": observed_at,
                },
                "display": {
                    "status": "ready_with_conditions",
                    "manifest_uri": image["uri"],
                    "credit_line": (
                        f"{proposal_object['artist']}, {proposal_object['title']}. "
                        f"{proposal_object['rights']['copyright_notice']}"
                    ),
                    "observed_at": observed_at,
                },
                "museum_observations": {
                    "observed_at": observed_at,
                    "observation_record": f"{ACCESSION}.VO-01",
                    "documentation_surrogate": image["uri"],
                    "static_visual_observation": (
                        "The credited source image is available for accession-context display."
                    ),
                    "live_behavior_observation": "Not applicable to this photographic object.",
                    "interpretive_boundary": (
                        "The image is read through its caption, source history, and "
                        "visual evidence; unresolved scene-specific claims remain unresolved."
                    ),
                },
                "visual_observation_record": f"{ACCESSION}.VO-01",
                "evidence_grade": "A/B/C",
                "uncertainties": [
                    *proposal_object.get("source_notes", []),
                    "The Museum does not assert copyright ownership or a general reproduction licence.",
                    "The source image is not yet retained as a Museum preservation master.",
                ],
                "source": {"source_record_ids": [PROPOSAL_ID, WINNER_OBSERVATION_ID]},
                "source_refs": [PROPOSAL_ID, candidate_id, WINNER_OBSERVATION_ID, TITLE_ID],
                "references": [ACCESSION, CERTIFICATE_ID, rights_id, condition_id, candidate_id],
                "claims": {
                    "artist_statement": (
                        f"The source record identifies the photograph as a work by "
                        f"{proposal_object['artist']}."
                    ),
                    "documented_fact": (
                        f"The source record identifies the title, date, and place as "
                        f"{proposal_object['title']}, {proposal_object['date']}, "
                        f"{proposal_object['location']}."
                    ),
                    "evidence_class": "B",
                    "museum_interpretation": (
                        "The Museum presents this photograph within Conflict at Its "
                        "Edges, a five-work group concerned with documentary evidence "
                        "and its edges."
                    ),
                    "technical_observation": (
                        "The ERC-721 identity, transfer receipt, and finalized "
                        "ownerOf observation are recorded separately from interpretation."
                    ),
                },
            }
        )
        reset_review_state(object_payload, observed_at)
        object_payload["evidence_refs"] = evidence_refs
        write_enveloped(
            f"records/accessions/{ACCESSION}/objects/{object_id}.json",
            object_payload,
        )
        source_work_path = migration.MAGNUM_WORK_PUBLICATION_PATHS[candidate_id]
        write_text(
            f"records/accessions/{ACCESSION}/public/{object_id}.md",
            f"""# {proposal_object['artist']}: {proposal_object['title']}

**Accession:** {ACCESSION}  
**Artist:** {proposal_object['artist']}  
**Date:** {proposal_object['date']}  
**Medium:** Photograph  
**Credit:** {proposal_object['rights']['copyright_notice']}

The 6529 Network Museum presents this photograph in Conflict at Its Edges, a
five-work group from Magnum Photos 75. The image remains tied to its source
caption and archive context; the Museum does not extend unresolved details
beyond the evidence recorded in the proposal and source dossier.

## Token record

- CAIP-19: {custody['caip19']}
- Transfer: {custody['tx_hash']} at block {custody['block_number']}, log {custody['log_index']}
- Common finalized observation: block {final_block} ({final_hash})
- Owner at that observation: {custody['owner']}

The tokenized object is accessioned into the permanent Collection. Copyright and
reproduction permission remain separate; the source record states All Rights
Reserved.

[Read the source work record]({migration.github_uri(source_work_path)})
""",
        )
        object_rows.append(
            {
                "accession_object_id": object_id,
                "source_object_id": candidate_id,
                "title": proposal_object["title"],
                "artist": proposal_object["artist"],
                "caip19": custody["caip19"],
                "identity_status": "external_token_identity_observed",
                "token_id": custody["token_id"],
            }
        )

    certificate = common_fields(
        casey_cert,
        CERTIFICATE_ID,
        "ACCESSION",
        ACCESSION,
        observed_at,
        [ACCESSION, GAA_ID, PROPOSAL_ID, ACQUISITION_ID]
        + [row["accession_object_id"] for row in object_rows],
        [summary_ref, proposal_ref, status_ref],
    )
    title_bindings = []
    for row in object_rows:
        custody = custody_objects[row["source_object_id"]]
        title_bindings.append(
            {
                "object_id": row["accession_object_id"],
                "status": "executed",
                "instrument_sha256": title_review_sha,
                "custodian_reference": "networkmuseum.6529.eth",
                "transfer_transaction": custody["tx_hash"],
                "block_number": custody["block_number"],
                "from": DONOR,
                "to": MUSEUM,
                "bound_at": observed_at,
                "basis": (
                    "The donor's full-gift offer and the Museum maintainer's "
                    "completion instruction, corroborated by the exact transfer "
                    "receipt for this token, bind the donor's transferable token "
                    "interest to this accession object."
                ),
            }
        )
    earliest_receipt = min(
        custody_objects.values(), key=lambda item: item["transfer_block_timestamp"]
    )
    cert_events = [
        {
            "event_type": "receipt",
            "event_name": "five_token_delivery",
            "occurred_at": observed_at,
            "source_occurred_at": earliest_receipt["transfer_block_timestamp"],
            "event_semantics": (
                "Five successful ERC-721 Transfers delivered the scheduled tokens "
                "from the donor address to the Museum address."
            ),
            "authority_reference": f"{ACCESSION}.RECEIPT-01",
            "evidence_refs": [summary_ref],
        },
        {
            "event_type": "acceptance",
            "event_name": "formal_gift_acceptance",
            "occurred_at": observed_at,
            "authority_reference": GAA_ID,
            "evidence_refs": [proposal_ref, status_ref],
        },
        {
            "event_type": "acquisition",
            "event_name": "five_work_acquisition",
            "occurred_at": observed_at,
            "authority_reference": ACCESSION,
            "evidence_refs": [summary_ref, status_ref],
        },
        {
            "event_type": "title_passage",
            "event_name": "institutional_title_registration",
            "occurred_at": observed_at,
            "authority_reference": TITLE_ID,
            "evidence_refs": [proposal_ref, status_ref],
            "instrument": {
                "kind": "institutional_gift_title_declaration",
                "reference": TITLE_ID,
                "sha256": title_review_sha,
                "uri": title_uri,
                "custodian_reference": "networkmuseum.6529.eth",
            },
        },
        {
            "event_type": "custody_receipt",
            "event_name": "institutional_custody_registration",
            "occurred_at": observed_at,
            "source_occurred_at": final_time,
            "event_semantics": (
                "The Museum registers custody at the common finalized observation; "
                "the five source transfer times remain in the receipt events above."
            ),
            "authority_reference": f"{ACCESSION}.RECEIPT-01",
            "evidence_refs": [summary_ref],
            "custody_paths": [
                {
                    "kind": "onchain_token",
                    "object_id": row["accession_object_id"],
                    "from": DONOR,
                    "to": MUSEUM,
                    "custodian_reference": "networkmuseum.6529.eth",
                }
                for row in object_rows
            ],
        },
        {
            "event_type": "accession",
            "event_name": "permanent_collection_accession",
            "occurred_at": observed_at,
            "authority_reference": CERTIFICATE_ID,
            "evidence_refs": [status_ref, summary_ref],
        },
    ]
    certificate.update(
        {
            "schema_id": casey_cert["schema_id"],
            "accession_number": ACCESSION,
            "acquiring_institution": "6529 Network Museum",
            "object_ids": [row["accession_object_id"] for row in object_rows],
            "title_bindings": title_bindings,
            "acquisition_method": "donation",
            "acceptance_date": observed_at,
            "review_outcomes": {
                "institutional_authority": "formally_accepted_by_maintainer_instruction",
                "identity_and_custody": "pass_at_common_finalized_block",
                "title": "pass_based_on_full_gift_and_institutional_title_declaration",
                "rights": "pass_with_all_rights_reserved_conditions",
                "provenance": "pass_for_accession",
                "curatorial": "approved_for_permanent_collection",
                "condition_and_technical": "pass_with_documentation_conditions",
                "display": "ready_with_conditions",
                "preservation": "in_progress",
            },
            "ongoing_stewardship_actions": [
                "Retain source metadata and credited display bytes with fixity.",
                "Maintain rights-compliant display and attribution.",
                "Enrich provenance and preservation records as new evidence becomes available.",
            ],
            "events": cert_events,
            "source": {
                "proposal": PROPOSAL_ID,
                "acquisition_entity": ACQUISITION_ID,
                "gift_acceptance_authorization": GAA_ID,
                "custody_evidence": SUMMARY_RELATIVE,
                "title_basis": "Donor full-gift offer plus Museum maintainer completion instruction.",
            },
        }
    )
    write_enveloped(
        f"records/accessions/{ACCESSION}/accession-certificate.json", certificate
    )

    gaa = common_fields(
        casey_gaa,
        GAA_ID,
        "GIFT_ACCEPTANCE_AUTHORIZATION",
        ACCESSION,
        observed_at,
        [PROPOSAL_ID, ACQUISITION_ID, CERTIFICATE_ID],
        [proposal_ref, status_ref, summary_ref],
    )
    gaa.update(
        {
            "schema_id": casey_gaa["schema_id"],
            "authorization_id": GAA_ID,
            "authorization_kind": "gift_acceptance_and_accession_authorization",
            "authorization_status": "formally_accepted",
            "formal_acceptance_date": observed_at,
            "completion_blockers": [],
            "completion_boundary": {
                "current_state": "accessioned",
                "accession_status": "complete",
                "external_work_accession_certificate": "executed",
                "title_binding": "executed",
                "rights": "reviewed_with_conditions",
                "condition": "reviewed_pass_with_conditions",
                "preservation": "in_progress",
                "independent_review": "pending",
            },
            "consideration": {
                "status": "none",
                "statement": "No consideration is recorded for this intentional gift. This record makes no valuation, tax, accounting, or legal characterization claim.",
            },
            "assets": [
                {
                    "object_id": row["accession_object_id"],
                    "title": row["title"],
                    "caip19": row["caip19"],
                    "contract": CONTRACT,
                    "token_id": str(row["token_id"]),
                    "custody_receipt_log": custody_objects[row["source_object_id"]]["log_index"],
                }
                for row in object_rows
            ],
            "custody_receipt": {
                "transaction_hash": custody_objects[object_rows[0]["source_object_id"]]["tx_hash"],
                "block_number": custody_objects[object_rows[0]["source_object_id"]]["block_number"],
                "block_time": custody_objects[object_rows[0]["source_object_id"]]["transfer_block_timestamp"],
                "from": DONOR,
                "to": MUSEUM,
                "custody_ens": "networkmuseum.6529.eth",
                "transfer_count": 5,
                "receipt_status": "0x1",
            },
            "donor_authority_declaration": {
                "source_type": "user_supplied_donor_and_authority_fact",
                "statement": "The donor's full-gift offer covers the five scheduled tokens and the donor's entire transferable interest in them, without consideration or retained donor interest.",
                "authentication": "The Museum records that declaration as the title basis. Exact on-chain delivery corroborates transfer of the five tokenized objects; no separate private instrument is represented in this public record.",
                "limitations": [
                    "The gift transfers the tokenized objects and donor-held transferable interests; it does not assign the photographers' copyright.",
                    "Copyright and reproduction permission remain subject to the All Rights Reserved source position.",
                    "The Museum's credited institutional display position is distinct from copyright ownership and commercial licensing.",
                ],
            },
            "governing_basis": [
                {
                    "basis_type": "wave_governance_decision",
                    "decision_id": WINNER_OBSERVATION_ID,
                    "wave_serial": 1276093,
                    "drop_id": "002bfa4f-8416-48bf-b35e-38f354e9a9f0",
                    "title": "Conflict at Its Edges acquisition proposal",
                    "observed_wave_status": "WINNER",
                    "governance_effect": "adopted",
                    "observed_at": migration.WINNER_AT,
                    "effect_basis": "direct_wave_observation",
                    "governance_record_ref": WINNER_OBSERVATION_ID,
                    "live_api_field": "drop_type",
                    "live_api_status": "WINNER",
                    "live_api_observed_at": migration.WINNER_AT,
                    "governance_effect_basis": "The signed-drop API records the proposal as WINNER; that cleared the TDH threshold for this acquisition.",
                    "source_uri": migration.WINNER_SOURCE_URL,
                },
                {
                    "basis_type": "wave_governance_decision",
                    "decision_id": "6529NM-GOV-1052812",
                    "wave_serial": 1052812,
                    "drop_id": "86e43beb-b55d-42f0-9eea-a3c115b08abc",
                    "title": "Donation Acceptance Policy",
                    "observed_wave_status": "WINNER",
                    "governance_effect": "adopted",
                    "observed_at": "2026-08-01T15:01:05Z",
                    "effect_basis": "reviewed_governance_record",
                    "governance_record_ref": "6529NM-GOV-REGISTER",
                    "live_api_field": "drop_type",
                    "live_api_status": "WINNER",
                    "live_api_observed_at": "2026-08-01T15:01:05Z",
                    "governance_effect_basis": "The reviewed governance register records adoption from the authenticated Wave API WINNER status.",
                    "source_uri": github_uri("policies/donation-acceptance.md"),
                },
            ],
            "institutional_decision_authority": {
                "authority_basis": "user_authorized_institutional_decision",
                "decision_status": "formally_accepted",
                "documentation_qa_status": "pending_independent_review",
                "effective_at": observed_at,
                "publication_semantics": "The Museum records the completed gift and accession on the basis of the donor's full-gift offer and maintainer instruction; constructor and reviewer fields keep documentary production separate from institutional authority.",
            },
            "non_claims": [
                "The accession does not transfer copyright or create a general reproduction licence.",
                "All Rights Reserved source notices remain in force.",
                "No valuation, tax, or commercial-rights determination is made.",
            ],
            "observed_at": observed_at,
            "outcome": "formally_accepted_gift_and_accession_authorization",
            "permanent_collection_intent": "The Museum formally accepts this five-object gift for the permanent Collection under the adopted donation pathway and ordinary collection stewardship responsibilities.",
            "source": {"source_record_ids": [PROPOSAL_ID, WINNER_OBSERVATION_ID]},
        }
    )
    write_enveloped(
        f"records/accessions/{ACCESSION}/gift-acceptance-authorization.json", gaa
    )

    write_text(
        f"records/accessions/{ACCESSION}/public/maintainer-authoritative-completion.md",
        f"""# Conflict at Its Edges: accession completion

The 6529 Network Museum has accepted and accessioned the five-work gift from
punk6529 into the permanent Collection under {ACCESSION}.

The decision rests on the donor's full-gift offer and the Museum maintainer's
completion instruction. The five transfer receipts and the common finalized
Ethereum observation are recorded in the accession certificate and custody
evidence.

The title record covers the donor's transferable interest in the tokenized
objects. The source photographs remain credited to their artists and Magnum
Photos and are All Rights Reserved; copyright and reproduction permission
remain separate from Collection membership.
""",
    )
    write_text(
        f"records/accessions/{ACCESSION}/public/gift-acceptance-authorization.md",
        f"""# Gift acceptance and accession authorization

The 6529 Network Museum records the five Magnum Photos 75 photographs in
Conflict at Its Edges as a completed gift from punk6529 and admits them to the
permanent Collection under accession lot {ACCESSION}.

The title basis is the donor's full-gift offer together with the Museum
maintainer's completion instruction, corroborated by the five on-chain delivery
receipts. The public record does not cite a separate private instrument. The
photographs remain All Rights Reserved; the gift transfers the tokenized
objects and the donor's transferable interest, not copyright.

The accession certificate, title and rights review, technical record, and
finalized custody evidence provide the supporting record. Continuing rights,
preservation, and provenance work belongs to the Museum's ongoing stewardship
of the accession.
""",
    )
    write_text(
        f"records/accessions/{ACCESSION}/public/accession-certificate.md",
        f"""# Accession certificate: Conflict at Its Edges

Accession lot: {ACCESSION}  
Acquisition: Gift from punk6529  
Works: Five  
Current status: Accessioned into the permanent Collection

The 6529 Network Museum has completed the accession of five photographs from
Magnum Photos 75. Presented together as Conflict at Its Edges, they form a
coherent group about documentary evidence: the border, the aftermath, the
caption, and the uncertainty that remains beyond an image's frame.

The donor's full-gift offer and the Museum maintainer's completion instruction
form the institutional basis for acceptance. The five transfer receipts,
Transfer logs, and owner observations are preserved in the finalized custody
evidence and bound to this certificate.

The common custody observation is Ethereum block {final_block}, hash
{final_hash}, timestamp {final_time}. The individual receipt transactions,
blocks, log indexes, and token identities appear on each object page.

Copyright remains separate from the accession. The source records credit each
photographer and Magnum Photos and state All Rights Reserved. As with works
held by other museums, the Museum interprets ownership as permitting ordinary,
credited institutional display and publication in the accession context. This
position does not claim copyright, commercial reproduction, derivative,
licensing, or AI-training rights.

See the title and rights review, technical and condition review, and gift
authorization for the supporting record.
""",
    )
    write_text(
        f"records/accessions/{ACCESSION}/public/curatorial-accession-review.md",
        """# Curatorial accession review: Conflict at Its Edges

Conflict at Its Edges brings together five photographs from Magnum Photos 75:
David Seymour's patrol at the Negev border; Larry Towell's soldiers in a
church in Suchitoto; Micha Bar-Am's demonstration at the Western Wall; Moisés
Saman's damaged room in Tripoli; and Lorenzo Meloni's view of Palmyra after its
recapture. The group moves across decades and geographies, but its coherence is
not simply the presence of conflict. It is the way each image tests the distance
between an event and its representation.

The photographs attend to edges: territorial borders, a threshold between
military presence and religious space, the crowd and the wall, a room after an
air strike, and a site encountered after destruction. Their subjects are not
offered as interchangeable evidence or as a complete history of any conflict.
The group asks what a photograph can establish, what its caption supplies, and
what remains beyond the frame.

The Museum has accessioned the five works as one coherent curatorial group. The
individual object records preserve the source captions, artist credits,
technical observations, and unresolved claims. Together they form an accession
that can be studied as a set without collapsing the differences among the
photographers, assignments, places, and moments.
""",
    )
    write_text(
        f"records/accessions/{ACCESSION}/public/technical-and-condition-review.md",
        f"""# Technical and condition review

The five accession objects are ERC-721 tokens with photographic source images.
The Museum verified each transfer receipt and matching Transfer log, read
ownerOf at the common finalized Ethereum block {final_block}, and retained the
source metadata and image references from the proposal package.

The objects are ready for credited accession-context display. Their source
images are not yet asserted to be Museum preservation masters. Image-byte
retention, redundant replication, rights-compliant display, and further
provenance enrichment remain active stewardship actions. No executable artwork,
generator, or software dependency is asserted for these photographic objects.
""",
    )

    work_projection_path = (
        "records/proposed-gifts/6529NM-PG-2026-001/public/scholarship/"
        "machine/work-projections.json"
    )
    def update_work_projection(record: dict[str, Any]) -> None:
        record["status"] = "canonical_review_pending_accessioned_work_projection"
        record["current_public_status"] = "Accessioned into the permanent Collection"
        record["current_lifecycle"] = "accessioned_into_permanent_collection"
        record["work_lifecycle"] = "accessioned"
        record["collection_membership"] = "permanent_collection"
        record.pop("accession_record", None)
        record.pop("object_record", None)
        record["accession_record_id"] = CERTIFICATE_ID
        record["object_record_ids"] = [row["accession_object_id"] for row in object_rows]
    amend_machine_record(work_projection_path, observed_at, update_work_projection)

    object_schedule_path = (
        "records/proposed-gifts/6529NM-PG-2026-001/public/scholarship/"
        "machine/object-schedule.json"
    )
    def update_object_schedule(record: dict[str, Any]) -> None:
        record["status"] = "canonical_review_pending_accessioned_object_schedule"
        record["current_public_status"] = "Accessioned into the permanent Collection"
        record["current_lifecycle"] = "accessioned_into_permanent_collection"
        for index, work in enumerate(record["works"], start=1):
            work["collection_membership"] = True
            work["collection_membership_status"] = "permanent_collection"
            work["work_lifecycle"] = "accessioned"
            work["accession_record_id"] = CERTIFICATE_ID
            work["object_record_id"] = f"{ACCESSION}.{index:02d}"
    amend_machine_record(object_schedule_path, observed_at, update_object_schedule)

    wave_join_path = (
        "records/proposed-gifts/6529NM-PG-2026-001/public/scholarship/"
        "machine/wave-media-join.json"
    )
    def update_wave_join(record: dict[str, Any]) -> None:
        record["current_public_status"] = "Accessioned into the permanent Collection"
        record["lifecycle_status"] = "accessioned_into_permanent_collection"
    amend_machine_record(wave_join_path, observed_at, update_wave_join)

    integration_path = (
        "records/proposed-gifts/6529NM-PG-2026-001/public/scholarship/"
        "machine/integration-map.json"
    )
    def update_integration(record: dict[str, Any]) -> None:
        record["status"] = "canonical_review_pending_accessioned_publication_projection"
        works = record["entity_projections"]["works"]
        works["lifecycle"] = "accessioned"
        works["collection_membership"] = "permanent_collection"
        acquisition = record["entity_projections"]["curated_acquisition"]
        acquisition["state"] = "accessioned_into_permanent_collection"
        record["acquisition_boundary"] = {
            "accession_id": ACCESSION,
            "object_record_ids": [row["accession_object_id"] for row in object_rows],
            "title_binding": f"records/accessions/{ACCESSION}/public/title-rights-and-accession-review.md",
            "custody": SUMMARY_RELATIVE,
            "condition": f"records/accessions/{ACCESSION}/public/technical-and-condition-review.md",
            "preservation": "continuing_stewardship",
            "rights": f"records/accessions/{ACCESSION}/rights/{ACCESSION}.RIGHTS.01.json",
        }
    amend_machine_record(integration_path, observed_at, update_integration)

    register_path = ROOT / "records/accessions/register.json"
    register = load_json(register_path)
    existing_magnum_lot = next(
        (
            item
            for item in register["lots"]
            if item.get("accession_lot_id") == ACCESSION
        ),
        None,
    )
    existing_magnum_amendment = next(
        (
            item
            for item in register["amendment_history"]
            if item.get("revision") == 3
            and "Magnum Photos 75" in str(item.get("reason", ""))
        ),
        None,
    )
    if existing_magnum_lot is None:
        prior_revision = int(register["record_control"]["revision"])
        prior_review = register["record_control"].get("review")
        prior_payload = {
            key: value for key, value in register.items() if key != "record_control"
        }
        prior_sha = "sha256:" + sha256_bytes(migration.canonicalize(prior_payload))
        prior_review_commit = (
            prior_review["reviewed_commit"]
            if isinstance(prior_review, dict)
            else source_head()
        )
    else:
        if not isinstance(existing_magnum_amendment, dict):
            raise RuntimeError("existing Magnum accession has no revision-3 amendment")
        prior_revision = 3
        prior_sha = str(existing_magnum_amendment["prior_payload_sha256"])
        prior_review_commit = str(existing_magnum_amendment["prior_review_commit"])
        register["lots"] = [
            item
            for item in register["lots"]
            if item.get("accession_lot_id") != ACCESSION
        ]
        register["amendment_history"] = [
            item
            for item in register["amendment_history"]
            if item is not existing_magnum_amendment
        ]
    register["snapshot_at"] = observed_at
    final_receipt = max(
        custody_objects.values(), key=lambda item: int(item["block_number"])
    )
    register["lots"].append(
        {
            "accession_lot_id": ACCESSION,
            "preferred_title": "Conflict at Its Edges, five photographs from Magnum Photos 75",
            "object_count": 5,
            "donation_status": "formally_accepted",
            "accession_status": "accessioned",
            "formal_acceptance_status": "formally_accepted",
            "gift_acceptance_authorization_record": GAA_ID,
            "donor_public_credit": "Gift of punk6529",
            "custody": {
                "ens": "networkmuseum.6529.eth",
                "chain_id": "eip155:1",
                "address": "0xbECfa2bA5a782D11E1a0e821E8F2e30b6684178c",
                "observed_at": observed_at,
                "finalized_block": final_block,
                "finalized_block_hash": final_hash,
                "token_count": 5,
                "evidence_class": "A",
            },
            "receipt_event": {
                "transaction_hash": final_receipt["tx_hash"],
                "block_number": final_receipt["block_number"],
                "block_time": final_receipt["transfer_block_timestamp"],
                "from": "0x6DAA633C23615a29471dEaFae351727867E7dAD1",
                "to": "0xbECfa2bA5a782D11E1a0e821E8F2e30b6684178c",
                "transfer_count": 5,
                "receipt_status": "0x1",
                "evidence_class": "A",
                "transactions": [
                    {
                        "token_id": row["token_id"],
                        "transaction_hash": custody_objects[row["source_object_id"]]["tx_hash"],
                        "block_number": custody_objects[row["source_object_id"]]["block_number"],
                        "log_index": custody_objects[row["source_object_id"]]["log_index"],
                    }
                    for row in object_rows
                ],
            },
            "evidence_refs": [
                f"records/accessions/{ACCESSION}/accession-certificate.json",
                f"records/accessions/{ACCESSION}/public/title-rights-and-accession-review.md",
                f"records/accessions/{ACCESSION}/public/technical-and-condition-review.md",
                f"records/accessions/{ACCESSION}/public/curatorial-accession-review.md",
                SUMMARY_RELATIVE,
                status_rel,
            ],
            "completion_limits": [],
            "accession_certificate_record": CERTIFICATE_ID,
            "ongoing_stewardship_actions": [
                "Retain the source metadata and credited display bytes with fixity.",
                "Maintain rights-compliant display and attribution.",
                "Enrich provenance and preservation records as new evidence becomes available.",
            ],
        }
    )
    register["amendment_history"].append(
        {
            "revision": prior_revision,
            "superseded_at": observed_at,
            "supersedes": prior_sha,
            "prior_payload_sha256": prior_sha,
            "prior_review_commit": prior_review_commit,
            "reason": (
                "Appended the completed five-work Magnum Photos 75 gift accession "
                "after finalized transfer and custody evidence bound all five "
                "objects to the Museum address."
            ),
        }
    )
    register["record_control"] = {
        "revision": prior_revision + 1,
        "record_status": "constructed",
        "constructor": {
            "actor_id": CONSTRUCTOR_ID,
            "role": "constructor",
            "constructed_at": observed_at,
        },
        "review": None,
    }
    write_json("records/accessions/register.json", register)

    casey_statement = load_json(
        ROOT / "records/accessions/6529NM.2026.001/accession-statement.json"
    )["payload"]
    statement = common_fields(
        casey_statement,
        ACCESSION,
        "ACCESSION_LOT",
        ACCESSION,
        observed_at,
        [GAA_ID, CERTIFICATE_ID, PROPOSAL_ID, WINNER_OBSERVATION_ID],
        [proposal_ref, status_ref, summary_ref],
    )
    common_keys = {
        "record_id", "record_type", "schema_id", "subject_id", "visibility",
        "record_version", "created_at", "observed_at", "effective_at",
        "constructor", "reviewer", "record_status", "review_status",
        "payload_sha256", "references", "evidence_refs",
    }
    statement = {key: value for key, value in statement.items() if key in common_keys}
    statement.update(
        {
            "schema_id": casey_statement["schema_id"],
            "accession_number": ACCESSION,
            "acquisition_method": "donation",
            "acceptance_date": observed_at,
            "object_ids": [row["accession_object_id"] for row in object_rows],
            "governing_references": [
                WINNER_OBSERVATION_ID,
                "6529NM-GOV-1052812",
                GAA_ID,
            ],
            "intake_status": "accessioned",
            "formal_acceptance_status": "formally_accepted",
            "formal_acceptance_date": observed_at,
            "gift_acceptance_authorization_record": GAA_ID,
            "accession_status": "complete",
            "source": {"source_record_ids": [PROPOSAL_ID, WINNER_OBSERVATION_ID]},
            "remaining_gates": [],
            "non_claims": [
                "Accession does not assign copyright or create a commercial reproduction licence.",
                "The Museum's credited institutional display position is distinct from copyright ownership.",
            ],
            "evidence_grade": "A/B/C",
        }
    )
    write_enveloped(f"records/accessions/{ACCESSION}/accession-statement.json", statement)


if __name__ == "__main__":
    build()
