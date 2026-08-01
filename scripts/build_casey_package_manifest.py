#!/usr/bin/env python3
"""Build the deterministic root inventory for the Casey evidence package."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "evidence/casey-reas-collection-snapshots"
PR4_MERGE_COMMIT = "ff1c5825e3b61bfb2df0a639e057297beb946e4d"
PR4_TOOL_SHA256 = "e4060edf7354aa683458dfa0e620c598673a0c65202c8efadd768ae8dc03cc53"
PR4_TOOL_BLOB_OID = "755a1b1c948d900496f5e279594223c8c99ab3e8"
ACTOR_ID = "codex-task:019fbe33-c412-7550-a1ba-f6c68c3b5652"


class PackageManifestError(RuntimeError):
    """Raised when the root inventory cannot bind the complete package."""


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def record(repo_root: Path, relative: str, role: str) -> dict[str, Any]:
    path = (repo_root / relative).resolve()
    if not path.is_file() or repo_root.resolve() not in path.parents:
        raise PackageManifestError(f"missing package file: {relative}")
    payload = path.read_bytes()
    return {"path": relative.replace("\\", "/"), "role": role, "sha256": f"sha256:{sha256_bytes(payload)}", "size": len(payload)}


def ref_from_record(item: dict[str, Any]) -> dict[str, Any]:
    return {"path": item["path"], "sha256": item["sha256"], "size": item["size"]}


def collect_derived_paths(value: Any, found: set[str] | None = None) -> set[str]:
    if found is None:
        found = set()
    if isinstance(value, dict):
        if isinstance(value.get("path"), str) and value["path"].startswith("derived/"):
            found.add(value["path"])
        for child in value.values():
            collect_derived_paths(child, found)
    elif isinstance(value, list):
        for child in value:
            collect_derived_paths(child, found)
    return found


def build(output_dir: Path, source_snapshot_commit: str, acquisition_commit: str) -> dict[str, Any]:
    output_dir = output_dir.resolve()
    repo_root = ROOT.resolve()
    latest = read_json(output_dir / "latest-run.json")
    manifest = read_json(output_dir / latest["manifest_path"])
    run_id = manifest["run_id"]
    run_relative = Path("evidence/casey-reas-collection-snapshots") / "runs" / run_id
    run_root = output_dir / "runs" / run_id
    records: list[dict[str, Any]] = []

    def add(relative: str, role: str) -> None:
        records.append(record(repo_root, relative, role))

    add("evidence/casey-reas-collection-snapshots/collection-sources.json", "authoritative-acquisition-config")
    add("evidence/casey-reas-collection-snapshots/pending-descriptors.json", "review-ledger")
    add("evidence/casey-reas-collection-snapshots/descriptor-manifest.json", "descriptor-child-manifest")
    for fixture in sorted((output_dir / "fixtures").glob("*.json")):
        add(str(fixture.relative_to(repo_root)), "verification-fixture")
    for descriptor in sorted((output_dir / "descriptors").glob("*.json")):
        add(str(descriptor.relative_to(repo_root)), "descriptor")
    add(str(run_relative / "run-manifest.json"), "acquisition-child-manifest")
    for snapshot in sorted((run_root / "snapshots").rglob("*.json")):
        add(str(snapshot.relative_to(repo_root)), "metadata-snapshot")
    for raw in sorted((run_root / "raw").rglob("*")):
        if raw.is_file():
            add(str(raw.relative_to(repo_root)), "raw-observation")
    derived_paths = collect_derived_paths(manifest)
    for ref_name in ("request_provenance", "exclusion_summary"):
        ref = manifest.get(ref_name)
        if isinstance(ref, dict):
            derived_paths.add(ref["path"])
            derived_path = run_root / ref["path"]
            derived_paths.update(collect_derived_paths(read_json(derived_path)))
    for relative in sorted(derived_paths):
        add(str(run_relative / relative), "derived-provenance")
    for script in (
        "scripts/acquire_casey_collection_snapshots.py",
        "scripts/harden_casey_snapshot_package.py",
        "scripts/build_casey_package_manifest.py",
        "scripts/emit_casey_collection_descriptors.py",
        "scripts/verify_casey_snapshot_package.py",
        "scripts/bootstrap_validate.py",
        "scripts/rarity/analyze.py",
        "scripts/rarity/nextgen_compat.py",
        "tests/rarity/test_nextgen_compat.py",
        "tests/rarity/fixtures/nextgen-compatibility.json",
        "tests/rarity/fixtures/nextgen-compatibility.expected.json",
    ):
        add(script, "executable-or-test-source")
    add("evidence/casey-reas-collection-snapshots/README.md", "package-documentation")

    records.sort(key=lambda item: item["path"])
    if len({item["path"] for item in records}) != len(records):
        raise PackageManifestError("duplicate root inventory path")
    raw_records = [item for item in records if item["role"] == "raw-observation"]
    derived_records = [item for item in records if item["role"] == "derived-provenance"]
    descriptor_records = [item for item in records if item["role"] == "descriptor"]
    by_path = {item["path"]: item for item in records}

    def binding(relative: str) -> dict[str, Any]:
        relative = relative.replace("\\", "/")
        if relative not in by_path:
            raise PackageManifestError(f"semantic binding missing from root inventory: {relative}")
        return ref_from_record(by_path[relative])

    package = {
        "schema_version": "6529nm.casey-package-manifest.v1",
        "package_id": "6529NM.2026.001.casey-reas-full-collection",
        "run_id": run_id,
        "observation": manifest["observation"],
        "constructor": {"actor_id": ACTOR_ID, "role": "constructor"},
        "review": None,
        "dependency": {
            "acquisition_commit": acquisition_commit,
            "source_snapshot_commit": source_snapshot_commit,
            "rarity_tool_merge_commit": PR4_MERGE_COMMIT,
            "rarity_tool_sha256": PR4_TOOL_SHA256,
            "rarity_tool_git_blob_oid": PR4_TOOL_BLOB_OID,
        },
        "network_fetch_status": "offline_reconstruction_only_after_v2_acquisition",
        "pr7_safety_dependency": {"status": "deferred_until_pr7_merge", "network_fetch_migration_required": True, "no_pr7_migration_claim": True},
        "pointer_files_excluded_from_inventory": {"files": ["evidence/casey-reas-collection-snapshots/latest-run.json", "evidence/casey-reas-collection-snapshots/package-manifest.json"], "reason": "latest-run points to this manifest and therefore cannot be included without a self-referential cycle; package-manifest is bound externally by latest-run"},
        "inventory": {"file_count": len(records), "raw_file_count": len(raw_records), "derived_file_count": len(derived_records), "descriptor_count": len(descriptor_records), "files": records},
        "semantic_bindings": {
            "config": binding("evidence/casey-reas-collection-snapshots/collection-sources.json"),
            "acquisition_manifest": binding(str(run_relative / "run-manifest.json")),
            "descriptor_manifest": binding("evidence/casey-reas-collection-snapshots/descriptor-manifest.json"),
            "pending_review_ledger": binding("evidence/casey-reas-collection-snapshots/pending-descriptors.json"),
            "request_provenance": binding(str(run_relative / manifest["request_provenance"]["path"])),
            "exclusion_summary": binding(str(run_relative / manifest["exclusion_summary"]["path"])),
            "descriptors": [ref_from_record(item) for item in descriptor_records],
        },
        "source_order_policy": "server Hasura row order and feature insertion order are preserved; numeric token and deterministic trait order are separate fields",
        "raw_bytes_policy": "all raw v2 response bytes are content-addressed and included; derived request bodies are separately labeled reconstructed",
    }
    package_path = output_dir / "package-manifest.json"
    write_json(package_path, package)
    package_ref = {"path": "package-manifest.json", "sha256": f"sha256:{sha256_bytes(package_path.read_bytes())}", "size": package_path.stat().st_size}
    latest["package_manifest"] = package_ref
    latest_manifest_path = output_dir / latest["manifest_path"]
    latest["manifest_sha256"] = f"sha256:{sha256_bytes(latest_manifest_path.read_bytes())}"
    write_json(output_dir / "latest-run.json", latest)
    return {"status": "complete", "package_manifest": package_ref, "file_count": len(records), "raw_file_count": len(raw_records), "descriptor_count": len(descriptor_records)}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-snapshot-commit", required=True)
    parser.add_argument("--acquisition-commit", required=True)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args(argv)
    try:
        print(json.dumps(build(args.output_dir, args.source_snapshot_commit, args.acquisition_commit), ensure_ascii=False, indent=2))
    except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError, PackageManifestError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
