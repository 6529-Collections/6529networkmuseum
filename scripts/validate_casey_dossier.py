#!/usr/bin/env python3
"""Fail closed on the published Casey descriptor-package dossier binding."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Iterable

from canonical import canonicalize

ROOT = Path(__file__).resolve().parent.parent
CASEY_ID = "6529NM.2026.001"
CASEY_DIR = Path("records/accessions") / CASEY_ID
PACKAGE_ROOT = Path("evidence/casey-reas-collection-snapshots")
PUBLISHED_SOURCE_COMMIT = "9700e842d0c991280b476cc67849d966221a742a"
PUBLISHED_RELEASE_COMMIT = "bf70ba3fd888d2d1b8add90fe56e913102f8aa68"
PUBLISHED_RELEASE_SHA256 = "sha256:d05f75c65c0af0172a0a2f2207693e4211d5c0f4f69fad8d4907ebd90e12470e"
PACKAGE_MANIFEST_SHA256 = "sha256:c08749355ea12c2948efdfdeb232675ab4bf693976a94c6ebb4ce24b0b5d08ab"
DESCRIPTOR_MANIFEST_SHA256 = "sha256:216bebd2f26e64488e7553a781ac278c18f54b1156ccd2bee7f9f1ff97012d63"
REPOSITORY = "https://github.com/6529-Collections/6529networkmuseum"
PUBLISHED_BLOB = f"{REPOSITORY}/blob/{PUBLISHED_RELEASE_COMMIT}"
STALE_BRANCH = "codex" + "/casey-reas-accession"

OBJECT_TO_DESCRIPTOR = {
    "6529NM.2026.001.01": "century",
    "6529NM.2026.001.02": "century",
    "6529NM.2026.001.03": "century",
    "6529NM.2026.001.04": "pre-process",
    "6529NM.2026.001.05": "phototaxis",
    "6529NM.2026.001.06": "923-empty-rooms",
    "6529NM.2026.001.07": "ex-nihilo-cosmos",
}
DESCRIPTOR_ORDER = ("century", "pre-process", "phototaxis", "923-empty-rooms", "ex-nihilo-cosmos")
NON_CLAIMS = [
    "No OpenSea or other marketplace metric is used.",
    "No aesthetic, quality, value, or ranking claim is made.",
]
PUBLIC_NON_CLAIM = "no OpenSea or other marketplace-metric, aesthetic, quality, value, or ranking claim"
PUBLIC_STATE = "received_onchain` / `not_complete"
PUBLIC_DESCRIPTOR = "transparent linked descriptor"
PUBLICATION_SEMANTICS = (
    "The published_source_commit is the reachable repository source anchor for this package; "
    "acquisition history remains package provenance, not an accession authority claim."
)


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_bytes(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


class HistoricalEvidenceError(RuntimeError):
    """The immutable published Casey evidence cannot be resolved locally."""


def git_bytes(history_root: Path, arguments: list[str], label: str) -> bytes:
    completed = subprocess.run(
        ["git", *arguments],
        cwd=history_root,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        detail = completed.stderr.decode("utf-8", errors="replace").strip()
        raise HistoricalEvidenceError(f"cannot resolve {label}: {detail or 'git command failed'}")
    return completed.stdout


def historical_bytes(history_root: Path, relative_path: str) -> bytes:
    return git_bytes(history_root, ["show", f"{PUBLISHED_RELEASE_COMMIT}:{relative_path}"], f"published Casey evidence {relative_path}")


def require_full_history(history_root: Path) -> None:
    shallow = git_bytes(history_root, ["rev-parse", "--is-shallow-repository"], "repository shallow-state").decode("ascii").strip()
    if shallow != "false":
        raise HistoricalEvidenceError("repository must have full history to verify the immutable Casey publication")
    git_bytes(history_root, ["cat-file", "-e", f"{PUBLISHED_RELEASE_COMMIT}^{{commit}}"], "published Casey release commit")
    git_bytes(history_root, ["cat-file", "-e", f"{PUBLISHED_SOURCE_COMMIT}^{{commit}}"], "published Casey source commit")
    source_ancestor = subprocess.run(
        [
            "git",
            "merge-base",
            "--is-ancestor",
            PUBLISHED_SOURCE_COMMIT,
            PUBLISHED_RELEASE_COMMIT,
        ],
        cwd=history_root,
        capture_output=True,
        check=False,
    )
    if source_ancestor.returncode != 0:
        raise HistoricalEvidenceError("published Casey source commit is not an ancestor of the published release commit")
    release_ancestor = subprocess.run(
        ["git", "merge-base", "--is-ancestor", PUBLISHED_RELEASE_COMMIT, "HEAD"],
        cwd=history_root,
        capture_output=True,
        check=False,
    )
    if release_ancestor.returncode != 0:
        raise HistoricalEvidenceError("published Casey release commit is not reachable from HEAD")


def read_json_bytes(data: bytes) -> dict[str, Any]:
    return json.loads(data.decode("utf-8"))


def payload_sha256(payload: dict[str, Any]) -> str:
    body = {key: value for key, value in payload.items() if key != "payload_sha256"}
    return "sha256:" + hashlib.sha256(canonicalize(body)).hexdigest()


def nested_strings(value: Any) -> Iterable[str]:
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for item in value.values():
            yield from nested_strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from nested_strings(item)


def source_package(history_root: Path) -> tuple[dict[str, Any], dict[str, dict[str, Any]], list[str]]:
    """Resolve the immutable Casey package only from its published release commit."""

    issues: list[str] = []
    try:
        require_full_history(history_root)
        latest = read_json_bytes(historical_bytes(history_root, f"{PACKAGE_ROOT.as_posix()}/latest-run.json"))
        package_manifest_bytes = historical_bytes(history_root, f"{PACKAGE_ROOT.as_posix()}/package-manifest.json")
        descriptor_manifest_bytes = historical_bytes(history_root, f"{PACKAGE_ROOT.as_posix()}/descriptor-manifest.json")
        release_manifest_bytes = historical_bytes(history_root, "release-artifacts/latest/record-manifest.json")
        package_manifest = read_json_bytes(package_manifest_bytes)
        descriptor_manifest = read_json_bytes(descriptor_manifest_bytes)
        release_manifest = read_json_bytes(release_manifest_bytes)
    except (HistoricalEvidenceError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        return {}, {}, [f"Casey immutable publication evidence cannot be verified: {exc}"]

    package_sha = sha256_bytes(package_manifest_bytes)
    descriptor_sha = sha256_bytes(descriptor_manifest_bytes)
    release_body = {
        key: value
        for key, value in release_manifest.items()
        if key not in {"manifest_commitment", "manifest_sha256"}
    }
    release_sha = "sha256:" + hashlib.sha256(canonicalize(release_body)).hexdigest()
    if latest.get("published_source_commit") != PUBLISHED_SOURCE_COMMIT:
        issues.append("Casey historical latest-run published_source_commit does not equal the reachable published source commit")
    if latest.get("package_manifest", {}).get("sha256") != PACKAGE_MANIFEST_SHA256 or package_sha != PACKAGE_MANIFEST_SHA256:
        issues.append("Casey historical package-manifest SHA-256 does not equal the published package hash")
    if descriptor_sha != DESCRIPTOR_MANIFEST_SHA256:
        issues.append("Casey historical descriptor-manifest SHA-256 does not equal the published descriptor hash")
    if release_manifest.get("manifest_sha256") != PUBLISHED_RELEASE_SHA256 or release_sha != PUBLISHED_RELEASE_SHA256:
        issues.append("Casey historical release manifest SHA-256 does not equal the published release hash")
    semantic = package_manifest.get("semantic_bindings", {}).get("descriptor_manifest", {})
    if semantic.get("sha256") != DESCRIPTOR_MANIFEST_SHA256:
        issues.append("Casey historical package manifest does not bind the descriptor manifest hash")

    try:
        run_id = latest["run_id"]
        run_manifest = read_json_bytes(
            historical_bytes(history_root, f"{PACKAGE_ROOT.as_posix()}/runs/{run_id}/run-manifest.json")
        )
    except (KeyError, HistoricalEvidenceError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        return {}, {}, issues + [f"Casey historical run manifest cannot be verified: {exc}"]
    populations = {
        entry.get("slug"): entry.get("population", {}).get("expected_token_count")
        for entry in run_manifest.get("collections", [])
        if isinstance(entry, dict)
    }
    descriptors: dict[str, dict[str, Any]] = {}
    for job in descriptor_manifest.get("jobs", []):
        if not isinstance(job, dict):
            continue
        slug = job.get("collection")
        output = job.get("output")
        if not isinstance(slug, str) or not isinstance(output, str):
            continue
        descriptor_path = (PACKAGE_ROOT / output).as_posix()
        try:
            descriptor_bytes = historical_bytes(history_root, descriptor_path)
            descriptor = read_json_bytes(descriptor_bytes)
        except (HistoricalEvidenceError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            issues.append(f"Casey historical descriptor cannot be verified for {slug}: {exc}")
            continue
        descriptor_sha256 = sha256_bytes(descriptor_bytes)
        if job.get("descriptor_sha256") != descriptor_sha256:
            issues.append(f"Casey historical descriptor file hash does not match its descriptor manifest for {slug}")
        if descriptor.get("result_sha256") != job.get("result_sha256"):
            issues.append(f"Casey historical descriptor result hash does not match its descriptor manifest for {slug}")
        descriptors[slug] = {
            "collection": slug,
            "path": descriptor_path,
            "uri": f"{PUBLISHED_BLOB}/{descriptor_path}",
            "descriptor_sha256": descriptor_sha256,
            "result_sha256": job.get("result_sha256"),
            "source_token_count": populations.get(slug),
            "trait_row_count": len(descriptor.get("result", {}).get("per_trait", [])),
        }
    if tuple(descriptors) != DESCRIPTOR_ORDER:
        issues.append("Casey descriptor manifest must contain exactly the five expected descriptors in publication order")

    inventory = package_manifest.get("inventory", {})
    source = {
        "published_source_commit": PUBLISHED_SOURCE_COMMIT,
        "publication_semantics": PUBLICATION_SEMANTICS,
        "publication_release": {
            "published_release_commit": PUBLISHED_RELEASE_COMMIT,
            "path": "release-artifacts/latest/record-manifest.json",
            "uri": f"{PUBLISHED_BLOB}/release-artifacts/latest/record-manifest.json",
            "sha256": PUBLISHED_RELEASE_SHA256,
            "scope": "Published Casey package boundary; this historical release commitment is not this dossier's regenerated release manifest.",
        },
        "path": PACKAGE_ROOT.as_posix(),
        "package_manifest": {
            "path": (PACKAGE_ROOT / "package-manifest.json").as_posix(),
            "uri": f"{PUBLISHED_BLOB}/{(PACKAGE_ROOT / 'package-manifest.json').as_posix()}",
            "sha256": PACKAGE_MANIFEST_SHA256,
        },
        "descriptor_manifest": {
            "path": (PACKAGE_ROOT / "descriptor-manifest.json").as_posix(),
            "uri": f"{PUBLISHED_BLOB}/{(PACKAGE_ROOT / 'descriptor-manifest.json').as_posix()}",
            "sha256": DESCRIPTOR_MANIFEST_SHA256,
        },
        "counts": {
            "bound_files": inventory.get("file_count"),
            "raw_files": inventory.get("raw_file_count"),
            "derived_files": inventory.get("derived_file_count"),
            "descriptor_results": inventory.get("descriptor_count"),
            "source_tokens": sum(value.get("source_token_count") or 0 for value in descriptors.values()),
            "trait_rows": sum(value.get("trait_row_count") or 0 for value in descriptors.values()),
        },
        "descriptors": [descriptors.get(slug) for slug in DESCRIPTOR_ORDER],
        "integrity_note": "Content hashes and exact blob/bf70ba3fd888d2d1b8add90fe56e913102f8aa68 URLs are immutable evidence anchors; tree/main and blob/main are reserved for intentionally mutable living-document links.",
    }
    if source["counts"] != {
        "bound_files": 175,
        "raw_files": 79,
        "derived_files": 64,
        "descriptor_results": 5,
        "source_tokens": 3300,
        "trait_rows": 35088,
    }:
        issues.append("Casey package counts do not match the published package manifests")
    return source, descriptors, issues


def validate_raw_metadata(root: Path) -> list[str]:
    issues: list[str] = []
    evidence_root = root / "evidence" / "casey-reas"
    manifest = read_json(evidence_root / "manifest.json")
    raw_entries = [entry for entry in manifest.get("entries", []) if isinstance(entry, dict) and str(entry.get("path", "")).startswith("raw/metadata/")]
    expected_paths = {f"raw/metadata/{CASEY_ID}.{suffix}.json" for suffix in ("01", "02", "03", "04", "05", "06", "07")}
    if {entry.get("path") for entry in raw_entries} != expected_paths:
        issues.append("Casey raw-evidence manifest must bind exactly the seven public metadata files")
    for entry in raw_entries:
        path = evidence_root / str(entry["path"])
        if not path.is_file() or entry.get("sha256") != hashlib.sha256(path.read_bytes()).hexdigest() or entry.get("size") != path.stat().st_size:
            issues.append(f"Casey raw public metadata manifest binding failed: {entry.get('path')}")
    return issues


def validate(root: Path = ROOT, history_root: Path | None = None) -> list[str]:
    source, descriptors, issues = source_package(history_root or root)
    records: dict[str, dict[str, Any]] = {}
    for path in sorted((root / CASEY_DIR).rglob("*.json")):
        record = read_json(path)
        payload = record.get("payload", {})
        record_id = payload.get("record_id")
        if isinstance(record_id, str):
            records[record_id] = record
        if payload.get("payload_sha256") != payload_sha256(payload):
            issues.append(f"Casey payload commitment is invalid: {path.relative_to(root)}")
        if payload.get("record_status") != "constructed" or payload.get("review_status") != "pending_independent_review" or payload.get("reviewer") is not None:
            issues.append(f"Casey record must remain constructed, unsigned, and independently unreviewed: {path.relative_to(root)}")
        signature_scheme = record.get("envelope", {}).get("signatureScheme")
        signature_digest = record.get("envelope", {}).get("signatureHash", {}).get("digest")
        if signature_scheme != "0x" + "0" * 64 or signature_digest != "0x" + "0" * 64:
            issues.append(f"Casey record must retain unsigned Stream placeholders: {path.relative_to(root)}")
        if any(STALE_BRANCH in text for text in nested_strings(record)):
            issues.append(f"Casey record has a mutable construction-branch URL: {path.relative_to(root)}")

    lot_record = records.get(CASEY_ID)
    if lot_record is None:
        return issues + ["Casey accession lot record is missing"]
    lot = lot_record["payload"]
    source_manifest = lot.get("source_manifest", {})
    if source_manifest.get("casey_snapshot_source_head") is not None:
        issues.append("Casey dossier must not retain the obsolete snapshot-source head")
    if source_manifest.get("casey_collection_snapshot_package") != source:
        issues.append("Casey lot source package binding does not match the published source package")
    if lot.get("source", {}).get("casey_collection_snapshot_package_published_source_commit") != PUBLISHED_SOURCE_COMMIT:
        issues.append("Casey lot source must name the published source commit")
    if lot.get("accession_status") != "not_complete" or lot.get("formal_acceptance_status") != "not_formally_accepted":
        issues.append("Casey lot must remain not_complete without formal acceptance")
    if lot.get("controlled_decision", {}).get("current_state") != "received_onchain":
        issues.append("Casey lot must remain received_onchain")
    if lot.get("review_status") != "pending_independent_review" or lot.get("reviewer") is not None:
        issues.append("Casey lot must retain incomplete independent registrar review without authority")
    if lot.get("constructor_controls", {}).get("reviewer") is not None or lot.get("constructor_controls", {}).get("merge_authority") is not None or lot.get("controlled_decision", {}).get("decision_authority") is not None:
        issues.append("Casey lot reviewer and decision-authority fields must remain null without evidence")

    expected_trait = {
        "status": "transparent_linked_descriptors_available",
        "method": "Museum published NextGen-compatible method over the frozen source package; linked descriptors are available and reproducible.",
        "marketplace_metrics": "not_used",
        "non_claims": NON_CLAIMS,
        "source_package": source,
    }
    if lot.get("trait_analysis") != expected_trait:
        issues.append("Casey lot trait analysis must provide transparent linked descriptors without prohibited claims")
    if lot.get("collection_curatorial_statement", {}).get("trait_analysis") != expected_trait:
        issues.append("Casey curatorial statement must provide transparent linked descriptors without prohibited claims")

    for object_id, descriptor_slug in OBJECT_TO_DESCRIPTOR.items():
        record = records.get(object_id)
        if record is None:
            issues.append(f"Casey object record is missing: {object_id}")
            continue
        payload = record["payload"]
        expected_object_trait = {**expected_trait, "descriptor": descriptors.get(descriptor_slug)}
        if payload.get("trait_analysis") != expected_object_trait:
            issues.append(f"Casey object descriptor mapping or claims are invalid: {object_id}")
        if payload.get("current_state") != "received_onchain":
            issues.append(f"Casey object must remain received_onchain: {object_id}")
        if payload.get("review_status") != "pending_independent_review" or payload.get("reviewer") is not None:
            issues.append(f"Casey object review must remain incomplete without authority: {object_id}")
        if "accessioned" in [entry.get("state") for entry in payload.get("state_history", []) if isinstance(entry, dict)]:
            issues.append(f"Casey object may not claim accessioned: {object_id}")

    for object_id, descriptor_slug in OBJECT_TO_DESCRIPTOR.items():
        page = root / CASEY_DIR / "public" / f"{object_id}.md"
        text = page.read_text(encoding="utf-8")
        descriptor_path = descriptors.get(descriptor_slug, {}).get("path")
        expected_url = f"{PUBLISHED_BLOB}/{descriptor_path}"
        if expected_url not in text or PUBLIC_DESCRIPTOR not in text or PUBLIC_STATE not in text or PUBLIC_NON_CLAIM not in text:
            issues.append(f"Casey public page lacks required transparent descriptor/state/non-claim disclosure: {page.name}")
        if "pending linked deliverable" in text or STALE_BRANCH in text:
            issues.append(f"Casey public page retains obsolete pending or mutable-branch language: {page.name}")

    issues.extend(validate_raw_metadata(root))
    return issues


def main() -> None:
    issues = validate()
    if issues:
        for issue in issues:
            print(f"error: {issue}", file=sys.stderr)
        raise SystemExit(1)
    print("Casey dossier validation passed: published source binding, descriptors, claims, states, URLs, and raw evidence are valid.")


if __name__ == "__main__":
    main()
