#!/usr/bin/env python3
"""Verify the complete Casey REAS acquisition package without computing rarity."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "evidence/casey-reas-collection-snapshots"
EXPECTED_SLUGS = {
    "century",
    "pre-process",
    "phototaxis",
    "923-empty-rooms",
    "ex-nihilo-cosmos",
}
PR4_MERGE_COMMIT = "ff1c5825e3b61bfb2df0a639e057297beb946e4d"
PROHIBITED_KEY_FRAGMENTS = (
    "opensea",
    "marketplacerarity",
    "thirdpartyrarity",
    "rarityscore",
    "marketplacerank",
)


class VerificationError(RuntimeError):
    """Raised when the acquisition package is not internally consistent."""


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def within(root: Path, relative: str) -> Path:
    candidate = (root / relative).resolve()
    if candidate != root and root not in candidate.parents:
        raise VerificationError(f"path escapes package root: {relative}")
    return candidate


def assert_equal(actual: Any, expected: Any, label: str) -> None:
    if actual != expected:
        raise VerificationError(f"{label}: expected {expected!r}, got {actual!r}")


def verify_raw_references(package_root: Path, values: list[tuple[str, Any]]) -> int:
    checked = 0
    for label, value in values:
        refs: list[tuple[Path, dict[str, Any]]] = []
        if isinstance(value, dict):
            def collect(node: Any) -> None:
                nonlocal checked
                if isinstance(node, dict):
                    path_value = node.get("path")
                    if isinstance(path_value, str) and path_value.startswith("raw/"):
                        raw_path = within(package_root, path_value)
                        if not raw_path.is_file():
                            raise VerificationError(f"{label}: missing raw file {path_value}")
                        expected_hash = node.get("sha256")
                        expected_size = node.get("size")
                        if not isinstance(expected_hash, str) or not isinstance(expected_size, int):
                            raise VerificationError(f"{label}: incomplete raw-file reference {path_value}")
                        actual_hash = f"sha256:{sha256_bytes(raw_path.read_bytes())}"
                        assert_equal(actual_hash, expected_hash, f"{label}:{path_value}:sha256")
                        assert_equal(raw_path.stat().st_size, expected_size, f"{label}:{path_value}:size")
                        checked += 1
                    for child_key, child in node.items():
                        normalized = "".join(character.lower() for character in str(child_key) if character.isalnum())
                        if any(fragment in normalized for fragment in PROHIBITED_KEY_FRAGMENTS):
                            raise VerificationError(f"prohibited marketplace/third-party field present at {label}.{child_key}")
                        collect(child)
                elif isinstance(node, list):
                    for child in node:
                        collect(child)
            collect(value)
    return checked


def verify_ordering(snapshot: dict[str, Any], expected_ids: list[int], label: str) -> None:
    tokens = snapshot.get("tokens")
    traits = snapshot.get("traits")
    source_metadata = snapshot.get("source_metadata")
    source_trait_rows = snapshot.get("source_trait_rows")
    if not all(isinstance(item, list) for item in (tokens, traits, source_metadata, source_trait_rows)):
        raise VerificationError(f"{label}: token/trait arrays are missing")
    token_ids = [row.get("id") for row in tokens]
    assert_equal(len(token_ids), len(expected_ids), f"{label}: token count")
    assert_equal(sorted(token_ids), expected_ids, f"{label}: canonical token population")
    ordering = snapshot.get("ordering")
    if not isinstance(ordering, dict):
        raise VerificationError(f"{label}: ordering object missing")
    assert_equal(ordering.get("source_token_order"), token_ids, f"{label}: source token order")
    assert_equal(ordering.get("canonical_token_order"), expected_ids, f"{label}: canonical token order")
    source_indices = [row.get("source_row_index") for row in source_trait_rows]
    assert_equal(source_indices, list(range(len(source_indices))), f"{label}: source trait row indices")
    assert_equal(ordering.get("source_trait_row_order"), source_indices, f"{label}: source trait order")
    trait_index_by_id = {row.get("source_row_index"): row for row in traits}
    canonical_expected = [
        row["source_row_index"]
        for row in sorted(
            traits,
            key=lambda row: (
                row.get("token_id"),
                row.get("trait"),
                row.get("value"),
                row.get("source_feature_index"),
            ),
        )
    ]
    assert_equal(ordering.get("canonical_trait_order"), canonical_expected, f"{label}: canonical trait order")
    if set(trait_index_by_id) != set(source_indices):
        raise VerificationError(f"{label}: source trait and materialized trait indices diverge")


def verify_fixture() -> int:
    fixture = read_json(ROOT / "evidence/casey-reas-collection-snapshots/fixtures/features-materialization.json")
    if fixture.get("schema_version") != "6529nm.features-materialization-fixture.v1":
        raise VerificationError("materialization fixture schema mismatch")
    checked = 0
    for case in fixture.get("cases", []):
        features = case.get("features")
        expected = case.get("expected_scalar_text")
        if not isinstance(features, dict) or not isinstance(expected, dict):
            raise VerificationError(f"fixture case malformed: {case.get('name')}")
        actual: dict[str, str] = {}
        for key, value in features.items():
            if isinstance(value, str):
                actual[key] = value
            elif isinstance(value, bool):
                actual[key] = "true" if value else "false"
            elif isinstance(value, (int, float)):
                actual[key] = json.dumps(value, ensure_ascii=False, allow_nan=False, separators=(",", ":"))
            else:
                raise VerificationError(f"fixture case contains unsupported scalar: {case.get('name')}")
        assert_equal(actual, expected, f"fixture case {case.get('name')}")
        checked += 1
    return checked


def verify_tool_projection_fixture() -> None:
    fixture = read_json(ROOT / "evidence/casey-reas-collection-snapshots/fixtures/tool-input-projection.json")
    assert_equal(fixture.get("schema_version"), "6529nm.casey-tool-input-projection-fixture.v1", "tool projection fixture schema")
    assert_equal(fixture.get("source_snapshot_is_preserved"), True, "tool projection source preservation")
    assert_equal(fixture.get("removed_paths"), ["materialization.not_a_marketplace_metric"], "tool projection removed paths")


def verify_descriptor_outputs(output_dir: Path, manifest: dict[str, Any], collections: list[dict[str, Any]]) -> int:
    descriptor_manifest_path = output_dir / "descriptor-manifest.json"
    if not descriptor_manifest_path.is_file():
        raise VerificationError("descriptor-manifest.json is missing")
    descriptor_manifest = read_json(descriptor_manifest_path)
    assert_equal(descriptor_manifest.get("schema_version"), "6529nm.casey-collection-descriptor-manifest.v1", "descriptor manifest schema")
    assert_equal(descriptor_manifest.get("status"), "complete", "descriptor manifest status")
    assert_equal(descriptor_manifest.get("dependency", {}).get("pull_request"), 4, "descriptor PR dependency")
    assert_equal(descriptor_manifest.get("dependency", {}).get("merge_commit"), PR4_MERGE_COMMIT, "descriptor merge commit")
    assert_equal(descriptor_manifest.get("run_id"), manifest.get("run_id"), "descriptor run id")
    assert_equal(descriptor_manifest.get("review"), None, "descriptor manifest review")
    jobs = descriptor_manifest.get("jobs")
    if not isinstance(jobs, list) or {job.get("collection") for job in jobs} != EXPECTED_SLUGS:
        raise VerificationError("descriptor manifest does not contain exactly five jobs")
    collection_by_slug = {row["slug"]: row for row in collections}
    checked = 0
    for job in jobs:
        slug = job["collection"]
        descriptor_path = within(output_dir, job["output"])
        if not descriptor_path.is_file():
            raise VerificationError(f"{slug}: descriptor output is missing")
        assert_equal(f"sha256:{sha256_bytes(descriptor_path.read_bytes())}", job.get("descriptor_sha256"), f"{slug}: descriptor hash")
        descriptor = read_json(descriptor_path)
        assert_equal(descriptor.get("schema_version"), "6529nm.casey-collection-descriptor.v1", f"{slug}: descriptor schema")
        assert_equal(descriptor.get("status"), "complete", f"{slug}: descriptor status")
        assert_equal(descriptor.get("dependency", {}).get("merge_commit"), PR4_MERGE_COMMIT, f"{slug}: descriptor dependency")
        assert_equal(descriptor.get("review"), None, f"{slug}: descriptor review")
        assert_equal(descriptor.get("curatorial_significance"), None, f"{slug}: descriptor curatorial significance")
        assert_equal(descriptor.get("method", {}).get("quality_or_canonical_truth_claim"), False, f"{slug}: descriptor interpretation gate")
        assert_equal(descriptor.get("method", {}).get("duplicate_policy"), "error", f"{slug}: duplicate policy")
        collection = collection_by_slug[slug]
        descriptor_input = descriptor.get("input", {})
        assert_equal(descriptor_input.get("snapshot_sha256"), collection.get("snapshot_file_sha256"), f"{slug}: descriptor source snapshot hash")
        assert_equal(descriptor_input.get("compatibility_projection", {}).get("removed_paths"), ["materialization.not_a_marketplace_metric"], f"{slug}: descriptor projection")
        snapshot_path = output_dir / collection["snapshot_path"]
        snapshot = read_json(snapshot_path)
        for descriptor_key, snapshot_key in (("source_token_order", "source_token_order"), ("canonical_token_order", "canonical_token_order"), ("source_trait_order", "source_trait_row_order"), ("canonical_trait_order", "canonical_trait_order")):
            assert_equal(descriptor_input.get(descriptor_key), snapshot["ordering"][snapshot_key], f"{slug}: {descriptor_key}")
        result_bytes = (json.dumps(descriptor["result"], ensure_ascii=False, indent=2) + "\n").encode("utf-8")
        assert_equal(f"sha256:{sha256_bytes(result_bytes)}", descriptor.get("result_sha256"), f"{slug}: descriptor result hash")
        assert_equal(descriptor.get("result_sha256"), job.get("result_sha256"), f"{slug}: manifest result hash")
        if not isinstance(descriptor.get("result"), dict) or descriptor["result"].get("schema") != "6529nm.generative-trait-analysis-output/v1":
            raise VerificationError(f"{slug}: merged tool output schema missing")
        checked += 1
    return checked


def verify(output_dir: Path) -> dict[str, Any]:
    output_dir = output_dir.resolve()
    latest_path = output_dir / "latest-run.json"
    pending_path = output_dir / "pending-descriptors.json"
    if not latest_path.is_file() or not pending_path.is_file():
        raise VerificationError("latest-run.json or pending-descriptors.json is missing")
    latest = read_json(latest_path)
    manifest_path = within(output_dir, latest["manifest_path"])
    if not manifest_path.is_file():
        raise VerificationError("latest manifest is missing")
    assert_equal(f"sha256:{sha256_bytes(manifest_path.read_bytes())}", latest.get("manifest_sha256"), "latest manifest hash")
    manifest = read_json(manifest_path)
    assert_equal(latest.get("status"), "complete", "latest status")
    assert_equal(manifest.get("status"), "complete", "manifest status")
    collections = manifest.get("collections")
    if not isinstance(collections, list) or {row.get("slug") for row in collections} != EXPECTED_SLUGS:
        raise VerificationError("manifest does not contain exactly the five Casey collection slugs")
    config = read_json(output_dir / "collection-sources.json")
    config_by_slug = {row["slug"]: row for row in config["collections"]}
    total = 0
    raw_refs = 0
    snapshot_summaries = []
    for row in collections:
        slug = row["slug"]
        configured = config_by_slug[slug]
        expected = int(row["population"]["expected_token_count"])
        assert_equal(row["population"]["bulk_rows"], expected, f"{slug}: bulk count")
        assert_equal(row["population"]["token_uri_resolved"], expected, f"{slug}: tokenURI count")
        assert_equal(row["population"]["snapshot_tokens"], expected, f"{slug}: snapshot count")
        assert_equal(row["population"]["complete"], True, f"{slug}: completeness")
        assert_equal(row["contract_address"].lower(), configured["contract_address"].lower(), f"{slug}: contract")
        assert_equal(int(row["project_id"]), int(configured["project_id"]), f"{slug}: project")
        snapshot_path = within(output_dir, row["snapshot_path"])
        if not snapshot_path.is_file():
            raise VerificationError(f"{slug}: snapshot is missing")
        assert_equal(f"sha256:{sha256_bytes(snapshot_path.read_bytes())}", row.get("snapshot_file_sha256"), f"{slug}: snapshot hash")
        snapshot = read_json(snapshot_path)
        assert_equal(snapshot.get("schema"), "6529nm.generative-trait-analysis-input/v1", f"{slug}: input schema")
        assert_equal(snapshot.get("collection", {}).get("contract_address", "").lower(), configured["contract_address"].lower(), f"{slug}: snapshot contract")
        assert_equal(int(snapshot.get("collection", {}).get("project_id")), int(configured["project_id"]), f"{slug}: snapshot project")
        expected_ids = [int(configured["project_id"]) * 1_000_000 + invocation for invocation in range(expected)]
        assert_equal(snapshot.get("population", {}).get("expected_token_ids"), expected_ids, f"{slug}: expected token IDs")
        verify_ordering(snapshot, expected_ids, slug)
        raw_refs += verify_raw_references(output_dir / "runs" / manifest["run_id"], [(slug, snapshot)])
        raw_refs += verify_raw_references(output_dir / "runs" / manifest["run_id"], [(slug, row)])
        total += expected
        snapshot_summaries.append({"slug": slug, "tokens": expected, "traits": len(snapshot["traits"])})
    pending = read_json(pending_path)
    assert_equal(pending.get("status"), "complete_pending_review", "pending descriptor status")
    assert_equal(pending.get("dependency", {}).get("final_outputs_permitted"), True, "descriptor dependency gate")
    assert_equal(pending.get("review"), None, "pending review")
    assert_equal(pending.get("curatorial_significance"), None, "pending curatorial significance")
    fixture_cases = verify_fixture()
    verify_tool_projection_fixture()
    descriptor_count = verify_descriptor_outputs(output_dir, manifest, collections)
    return {"status": "verified", "run_id": manifest["run_id"], "collections": snapshot_summaries, "total_tokens": total, "raw_references_checked": raw_refs, "fixture_cases": fixture_cases, "descriptor_outputs": descriptor_count, "cross_check_warnings": len(manifest.get("cross_check_warnings", [])), "rarity_outputs_emitted": True}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args(argv)
    try:
        print(json.dumps(verify(args.output_dir), ensure_ascii=False, indent=2))
    except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError, VerificationError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
