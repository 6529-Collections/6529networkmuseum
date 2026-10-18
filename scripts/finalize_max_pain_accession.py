#!/usr/bin/env python3
"""Seal the MAX PAIN #4188/7394 accession records into Stream-compatible envelopes.

Accession ``6529NM.2026.005`` is a community-funded purchase. This script only
seals: it never rewrites a record's facts. For every direct record under
``records/accessions/6529NM.2026.005`` (the presentation manifest excepted) it

* binds every repository evidence reference to the current bytes of the file it
  names: an evidence ``uri`` under the repository blob URL that carries a
  ``sha256``, a raw ``path``/``sha256``/``size`` artifact reference, the
  preservation-manifest and package fixity, and the token-metadata digest;
* binds the institutional purchase title declaration, whose content is derived
  from the acquisition authorization and the accession certificate, to every
  ``instrument_sha256`` and ``institutional_purchase_title_declaration``
  instrument;
* sets the review state (``--pending`` or ``--reviewed``; neither keeps the
  committed state), recomputes ``payload_sha256``, and rebuilds the envelope.

The standalone governance decision ``6529NM-GOV-1336667`` and the proposed
acquisition ``6529NM-PA-2026-001`` are sealed in the same pass for their
evidence bindings only. Their review state is never changed here: the
governance decision is reviewed in its own commit after the catalog, and the
proposal record carries its own record control.

``--check`` fails when any committed record differs from its sealed form.
"""

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
ACCESSION_ID = "6529NM.2026.005"
ACCESSION = ROOT / "records" / "accessions" / ACCESSION_ID
AUTHORIZATION_PATH = ACCESSION / "acquisition-authorization.json"
GOVERNANCE_PATH = ROOT / "records" / "governance" / "6529NM-GOV-1336667.json"
PROPOSAL_PATH = ROOT / "records" / "proposed-acquisitions" / "6529NM-PA-2026-001" / "proposal.json"
CERTIFICATE_PATH = ACCESSION / "accession-certificate.json"
REPO = "https://github.com/6529-Collections/6529networkmuseum"
BLOB_PREFIX = f"{REPO}/blob/main/"
TREE_PREFIX = f"{REPO}/tree/main/"
CANONICALIZATION_ID = "0x886c7c89c308c459ca8a626e0ef36a5ea9f4c7a7b56aaf86c71a2ddf3b4f9044"
ZERO_HASH = "0x" + "0" * 64
TITLE_KIND = "institutional_purchase_title_declaration"
TITLE_INTEREST = (
    "the executing agent's entire transferable interest in the exact ERC-721 token, acquired for the "
    "6529 Network Museum under the Wave authorization; contributors receive no individual or fractional "
    "ownership interest"
)
RECIPIENT = "6529 Network Museum"
SHA256_PATTERN = re.compile(r"^sha256:[0-9a-f]{64}$")


class SealError(ValueError):
    """Raised when a record cannot be bound to the repository evidence it names."""


def load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise SealError(f"{path}: JSON root must be an object")
    return value


def payload_of(path: Path) -> dict[str, Any]:
    source = load(path)
    payload = source.get("payload")
    if not isinstance(payload, dict):
        raise SealError(f"{path}: record has no payload object")
    return payload


def sha256_file(relative: str) -> tuple[str, int]:
    path = (ROOT / relative).resolve()
    if ROOT.resolve() not in path.parents or not path.is_file():
        raise SealError(f"bound evidence path is missing or outside the repository: {relative}")
    payload = path.read_bytes()
    return "sha256:" + hashlib.sha256(payload).hexdigest(), len(payload)


def repository_path(uri: str, prefix: str) -> str | None:
    if not uri.startswith(prefix):
        return None
    relative = uri.removeprefix(prefix)
    return relative or None


def title_instrument() -> dict[str, Any]:
    """Return the purchase title declaration derived from the sealed source records."""

    authorization = payload_of(AUTHORIZATION_PATH)
    certificate = payload_of(CERTIFICATE_PATH)
    assets = authorization.get("assets")
    receipts = authorization.get("custody_receipts")
    if not isinstance(assets, list) or len(assets) != 1 or not isinstance(receipts, list) or len(receipts) != 1:
        raise SealError("the purchase title declaration covers exactly one asset and one Museum receipt")
    asset = assets[0]
    receipt = receipts[0]
    payment = authorization["consideration"]["payment_transaction"]
    decisions = sorted(
        item["decision_id"]
        for item in authorization.get("governing_basis", [])
        if isinstance(item, dict) and item.get("basis_type") == "wave_governance_decision"
    )
    policies = sorted(
        item["record_id"]
        for item in authorization.get("governing_basis", [])
        if isinstance(item, dict) and item.get("basis_type") == "policy_record"
    )
    return {
        "accession_number": certificate["accession_number"],
        "object_id": asset["object_id"],
        "acquisition_authority": authorization["authorization_id"],
        "governing_decisions": decisions,
        "governing_policies": policies,
        "executing_agent": authorization["executing_agent"]["address"],
        "purchase_transaction": payment["transaction_hash"],
        "transfer_transaction": receipt["transaction_hash"],
        "recipient": RECIPIENT,
        "custodian_reference": receipt["custody_ens"],
        "caip19": asset["caip19"],
        "interest": TITLE_INTEREST,
    }


def title_instrument_sha256() -> str:
    return "sha256:" + hashlib.sha256(canonicalize(title_instrument())).hexdigest()


def payload_sha(payload: dict[str, Any]) -> str:
    material = {key: value for key, value in payload.items() if key != "payload_sha256"}
    return "sha256:" + hashlib.sha256(canonicalize(material)).hexdigest()


def subject_hash(record_type: str, subject_id: str) -> str:
    material = f"6529networkmuseum.subject.{record_type.lower()}.v1:{subject_id}".encode()
    return "0x" + keccak256(material).hex()


def unix_seconds(value: str) -> int:
    return int(datetime.fromisoformat(value.replace("Z", "+00:00")).timestamp())


def bind_evidence(value: Any, title_sha: str) -> None:
    """Bind every repository evidence reference and title instrument in place."""

    if isinstance(value, dict):
        uri = value.get("uri")
        if isinstance(uri, str) and "sha256" in value:
            relative = repository_path(uri, BLOB_PREFIX)
            if relative is not None:
                value["sha256"] = sha256_file(relative)[0]
        if value.get("byte_mode") == "raw" and isinstance(value.get("path"), str) and "sha256" in value and "size" in value:
            value["sha256"], value["size"] = sha256_file(value["path"])
        if "instrument_sha256" in value:
            value["instrument_sha256"] = title_sha
        if value.get("kind") == TITLE_KIND:
            value["sha256"] = title_sha
        manifest_uri = value.get("manifest_uri")
        if isinstance(manifest_uri, str) and "manifest_sha256" in value:
            relative = repository_path(manifest_uri, BLOB_PREFIX)
            if relative is None:
                raise SealError(f"preservation manifest is not a repository path: {manifest_uri}")
            digest = sha256_file(relative)[0]
            value["manifest_sha256"] = digest
            if "fixity_sha256" in value:
                value["fixity_sha256"] = digest
        package_uri = value.get("package_uri")
        if isinstance(package_uri, str) and "fixity_sha256" in value:
            relative = repository_path(package_uri, TREE_PREFIX)
            if relative is None:
                raise SealError(f"preservation package is not a repository tree: {package_uri}")
            value["fixity_sha256"] = sha256_file(f"{relative}/manifest.json")[0]
        metadata_path = value.get("metadata_raw_path")
        if isinstance(metadata_path, str) and "metadata_sha256" in value:
            value["metadata_sha256"] = sha256_file(metadata_path)[0]
        for item in value.values():
            bind_evidence(item, title_sha)
    elif isinstance(value, list):
        for item in value:
            bind_evidence(item, title_sha)


def bind_chain_metadata(payload: dict[str, Any]) -> None:
    """Bind the object's token-metadata digest to the retained metadata response."""

    chain = payload.get("chain_identity")
    preservation = payload.get("preservation")
    if not isinstance(chain, dict) or "metadata_sha256" not in chain or not isinstance(preservation, dict):
        return
    package = repository_path(str(preservation.get("package_uri", "")), TREE_PREFIX)
    if package is None:
        raise SealError("object preservation package is not a repository tree")
    manifest = load(ROOT / package / "manifest.json")
    rows = [
        row for row in manifest.get("entries", [])
        if isinstance(row, dict) and row.get("url") == chain.get("metadata_uri")
    ]
    if len(rows) != 1:
        raise SealError("object metadata_uri must match exactly one retained source entry")
    chain["metadata_sha256"] = sha256_file(f"{package}/{rows[0]['path']}")[0]


def normalize_payload(
    payload: dict[str, Any],
    review: dict[str, str] | None = None,
    *,
    pending: bool = False,
) -> dict[str, Any]:
    payload = json.loads(json.dumps(payload))
    payload["payload_sha256"] = "sha256:" + "0" * 64
    if pending:
        payload["reviewer"] = None
        payload["record_status"] = "review_pending"
        payload["review_status"] = "pending_independent_review"
    elif review is not None:
        created_at = datetime.fromisoformat(str(payload["created_at"]).replace("Z", "+00:00"))
        reviewed_at = datetime.fromisoformat(review["reviewed_at"].replace("Z", "+00:00"))
        if reviewed_at <= created_at:
            raise SealError("--reviewed-at must be after every record's created_at")
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
    bind_evidence(payload, title_instrument_sha256())
    bind_chain_metadata(payload)
    payload["payload_sha256"] = payload_sha(payload)
    return payload


def seal(path: Path, review: dict[str, str] | None = None, *, pending: bool = False) -> dict[str, Any]:
    payload = normalize_payload(payload_of(path), review, pending=pending)
    record_type = str(payload["record_type"])
    relative = path.resolve().relative_to(ROOT.resolve()).as_posix()
    envelope = {
        "recordType": record_type,
        "subjectId": subject_hash(record_type, str(payload["subject_id"])),
        "contentHash": {
            "algorithm": 1,
            "digest": "0x" + keccak256(canonicalize(payload)).hex(),
            "canonicalizationId": CANONICALIZATION_ID,
        },
        "uri": f"{BLOB_PREFIX}{relative}",
        "schemaId": str(payload["schema_id"]),
        "signatureScheme": ZERO_HASH,
        "signatureHash": {"algorithm": 2, "digest": ZERO_HASH, "canonicalizationId": CANONICALIZATION_ID},
        "effectiveAt": unix_seconds(str(payload["effective_at"])),
    }
    return {
        "$schema": "https://6529networkmuseum.org/schemas/record-envelope-v1.json",
        "envelope": envelope,
        "payload": payload,
    }


def encoded(value: dict[str, Any], *, sort_keys: bool = True) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=sort_keys) + "\n").encode("utf-8")


def seal_proposal(path: Path) -> dict[str, Any]:
    """Bind the proposed-acquisition record's evidence references; its record control is unchanged."""

    value = json.loads(json.dumps(load(path)))
    bind_evidence(value, title_instrument_sha256())
    return value


def record_paths() -> list[Path]:
    return sorted(path for path in ACCESSION.rglob("*.json") if path.name != "presentation-manifest.json")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true")
    state = parser.add_mutually_exclusive_group()
    state.add_argument("--pending", action="store_true")
    state.add_argument("--reviewed", action="store_true")
    parser.add_argument("--reviewer-id")
    parser.add_argument("--reviewed-at")
    parser.add_argument("--reviewed-commit")
    parser.add_argument("--reviewed-manifest-sha256")
    parser.add_argument("--reviewed-manifest-keccak")
    args = parser.parse_args(argv)
    review_fields = {
        "reviewer_id": args.reviewer_id,
        "reviewed_at": args.reviewed_at,
        "reviewed_commit": args.reviewed_commit,
        "reviewed_manifest_sha256": args.reviewed_manifest_sha256,
        "reviewed_manifest_keccak": args.reviewed_manifest_keccak,
    }
    if not args.reviewed and any(value is not None for value in review_fields.values()):
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
    paths = record_paths()
    try:
        sealed = {path: encoded(seal(path, review, pending=args.pending)) for path in paths}
        sealed[GOVERNANCE_PATH] = encoded(seal(GOVERNANCE_PATH))
        sealed[PROPOSAL_PATH] = encoded(seal_proposal(PROPOSAL_PATH), sort_keys=False)
    except (KeyError, OSError, SealError, TypeError, ValueError) as exc:
        raise SystemExit(f"MAX PAIN accession sealing failed: {exc}") from exc
    stale: list[str] = []
    for path, expected in sealed.items():
        if args.check:
            if path.read_bytes() != expected:
                stale.append(path.relative_to(ROOT).as_posix())
        else:
            path.write_bytes(expected)
    if stale:
        raise SystemExit("stale MAX PAIN accession commitments: " + ", ".join(stale))
    print(f"MAX PAIN accession commitments are current: {len(sealed)} records")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
