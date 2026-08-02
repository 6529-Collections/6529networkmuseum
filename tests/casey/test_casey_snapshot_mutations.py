"""Negative controls for Casey package bindings and semantic guards."""

from __future__ import annotations

import copy
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest import mock

import scripts.verify_casey_snapshot_package as verifier
from scripts.verify_casey_snapshot_package import (
    EXPECTED,
    PR4_MERGE_COMMIT,
    PR4_TOOL_BLOB_OID,
    PR4_TOOL_SHA256,
    PUBLISHED_SOURCE_COMMIT,
    VerificationError,
    reject_external_metrics,
    verify_exclusion_row,
    verify_file_record,
    verify_ordering,
    verify_stable_dependency,
    validate_config,
)


ROOT = Path(__file__).resolve().parents[2]


class CaseySnapshotMutationTests(unittest.TestCase):
    def _run_end_to_end_mutation(self, mutate: object, expected_error: str) -> None:
        with tempfile.TemporaryDirectory(prefix="casey-package-mutation-") as temp_dir:
            worktree = Path(temp_dir) / "repo"
            added = subprocess.run(
                ["git", "worktree", "add", "--detach", str(worktree), "HEAD"],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(added.returncode, 0, added.stderr)
            try:
                mutate(worktree)
                completed = subprocess.run(
                    [sys.executable, str(worktree / "scripts/verify_casey_snapshot_package.py")],
                    cwd=worktree,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertNotEqual(completed.returncode, 0, completed.stdout)
                self.assertIn(expected_error, completed.stderr)
            finally:
                removed = subprocess.run(
                    ["git", "worktree", "remove", "--force", str(worktree)],
                    cwd=ROOT,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertEqual(removed.returncode, 0, removed.stderr)

    @staticmethod
    def _write_json(path: Path, value: object) -> None:
        path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")

    @classmethod
    def _refresh_package_pointer(cls, worktree: Path, package: dict[str, object]) -> None:
        package_path = worktree / "evidence/casey-reas-collection-snapshots/package-manifest.json"
        cls._write_json(package_path, package)
        package_bytes = package_path.read_bytes()
        latest_path = worktree / "evidence/casey-reas-collection-snapshots/latest-run.json"
        latest = json.loads(latest_path.read_text(encoding="utf-8"))
        latest["package_manifest"] = {
            "path": "package-manifest.json",
            "sha256": "sha256:" + hashlib.sha256(package_bytes).hexdigest(),
            "size": len(package_bytes),
        }
        cls._write_json(latest_path, latest)

    @classmethod
    def _mutate_inventory_path(cls, worktree: Path) -> None:
        package_path = worktree / "evidence/casey-reas-collection-snapshots/package-manifest.json"
        package = json.loads(package_path.read_text(encoding="utf-8"))
        for item in package["inventory"]["files"]:
            if item["path"] == "evidence/casey-reas-collection-snapshots/README.md":
                replacement = worktree / "README.md"
                payload = replacement.read_bytes()
                item["path"] = "README.md"
                item["sha256"] = "sha256:" + hashlib.sha256(payload).hexdigest()
                item["size"] = len(payload)
                break
        else:
            raise AssertionError("package README inventory entry missing")
        cls._refresh_package_pointer(worktree, package)

    @classmethod
    def _mutate_descriptor_marketplace_reference(cls, worktree: Path) -> None:
        descriptor_relative = "evidence/casey-reas-collection-snapshots/descriptors/century.json"
        descriptor_path = worktree / descriptor_relative
        descriptor = json.loads(descriptor_path.read_text(encoding="utf-8"))
        descriptor["external_analysis"] = {
            "provider": "OpenSea",
            "url": "https://opensea.io/assets/1/0x0000000000000000000000000000000000000000/1",
            "rarity_score": 1,
        }
        cls._write_json(descriptor_path, descriptor)
        package_path = worktree / "evidence/casey-reas-collection-snapshots/package-manifest.json"
        package = json.loads(package_path.read_text(encoding="utf-8"))
        payload = descriptor_path.read_bytes()
        for item in package["inventory"]["files"]:
            if item["path"] == descriptor_relative:
                item["sha256"] = "sha256:" + hashlib.sha256(payload).hexdigest()
                item["size"] = len(payload)
                break
        else:
            raise AssertionError("century descriptor inventory entry missing")
        cls._refresh_package_pointer(worktree, package)

    @classmethod
    def _mutate_bound_raw_symlink(cls, worktree: Path) -> None:
        package_root = worktree / "evidence/casey-reas-collection-snapshots"
        package = json.loads((package_root / "package-manifest.json").read_text(encoding="utf-8"))
        raw_item = next(item for item in package["inventory"]["files"] if item.get("role") == "raw-observation")
        raw_path = worktree / raw_item["path"]
        target = package_root / "symlink-test-target.json"
        target.write_bytes(raw_path.read_bytes())
        raw_path.unlink()
        try:
            os.symlink(target, raw_path, target_is_directory=False)
        except OSError as error:
            raise unittest.SkipTest(f"filesystem does not permit test symlink creation: {error}") from error

    @classmethod
    def _mutate_published_source_commit(cls, worktree: Path) -> None:
        latest_path = worktree / "evidence/casey-reas-collection-snapshots/latest-run.json"
        latest = json.loads(latest_path.read_text(encoding="utf-8"))
        latest["published_source_commit"] = "0" * 40
        cls._write_json(latest_path, latest)

    @classmethod
    def _mutate_package_pointer_path(cls, worktree: Path) -> None:
        latest_path = worktree / "evidence/casey-reas-collection-snapshots/latest-run.json"
        latest = json.loads(latest_path.read_text(encoding="utf-8"))
        latest["package_manifest"]["path"] = "runs/package-manifest.json"
        cls._write_json(latest_path, latest)

    @classmethod
    def _mutate_package_pointer_size(cls, worktree: Path) -> None:
        latest_path = worktree / "evidence/casey-reas-collection-snapshots/latest-run.json"
        latest = json.loads(latest_path.read_text(encoding="utf-8"))
        latest["package_manifest"]["size"] += 1
        cls._write_json(latest_path, latest)

    def test_inventory_path_substitution_fails_end_to_end(self) -> None:
        self._run_end_to_end_mutation(self._mutate_inventory_path, "root inventory closed path/role allowlist")

    def test_descriptor_marketplace_provider_fails_end_to_end(self) -> None:
        self._run_end_to_end_mutation(self._mutate_descriptor_marketplace_reference, "forbidden external/provider field")

    def test_bound_raw_symlink_fails_end_to_end(self) -> None:
        self._run_end_to_end_mutation(self._mutate_bound_raw_symlink, "symlink or reparse point")

    def test_published_source_commit_mutation_fails_end_to_end(self) -> None:
        self._run_end_to_end_mutation(self._mutate_published_source_commit, "published source commit")

    def test_package_pointer_path_mutation_fails_closed(self) -> None:
        self._run_end_to_end_mutation(
            self._mutate_package_pointer_path,
            "root package manifest pointer path",
        )

    def test_package_pointer_size_mutation_fails_closed(self) -> None:
        self._run_end_to_end_mutation(
            self._mutate_package_pointer_size,
            "root package manifest pointer size",
        )

    def test_published_source_commit_is_reachable_from_main_package_release(self) -> None:
        latest = json.loads(
            (ROOT / "evidence/casey-reas-collection-snapshots/latest-run.json").read_text(encoding="utf-8")
        )
        self.assertEqual(latest["published_source_commit"], PUBLISHED_SOURCE_COMMIT)
        completed = subprocess.run(
            ["git", "merge-base", "--is-ancestor", PUBLISHED_SOURCE_COMMIT, "HEAD"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)

    def test_windows_reparse_attribute_fails_closed(self) -> None:
        root_info = SimpleNamespace(st_mode=stat.S_IFDIR, st_file_attributes=0)
        reparse_info = SimpleNamespace(st_mode=stat.S_IFREG, st_file_attributes=0x400)
        with mock.patch.object(verifier.os, "lstat", side_effect=(root_info, reparse_info)):
            with self.assertRaisesRegex(VerificationError, "symlink or reparse point"):
                verifier.within(Path("disposable-root"), "bound.json")

    def test_contract_mapping_mutation_fails_closed(self) -> None:
        config = json.loads((ROOT / "evidence/casey-reas-collection-snapshots/collection-sources.json").read_text(encoding="utf-8"))
        mutated = copy.deepcopy(config)
        mutated["collections"][0]["contract_address"] = "0x0000000000000000000000000000000000000001"
        with self.assertRaises(VerificationError):
            validate_config(mutated)

    def test_root_file_hash_mutation_fails_closed(self) -> None:
        path = ROOT / "scripts/verify_casey_snapshot_package.py"
        record = {"path": "scripts/verify_casey_snapshot_package.py", "sha256": "sha256:" + "0" * 64, "size": path.stat().st_size}
        with self.assertRaises(VerificationError):
            verify_file_record(ROOT, record)

    def test_mutable_head_dependency_fails_closed(self) -> None:
        dependency = {"rarity_tool_merge_commit": PR4_MERGE_COMMIT, "rarity_tool_sha256": PR4_TOOL_SHA256, "rarity_tool_git_blob_oid": PR4_TOOL_BLOB_OID, "source_snapshot_commit": "a" * 40, "acquisition_commit": "b" * 40, "current_head": "c" * 40}
        with self.assertRaises(VerificationError):
            verify_stable_dependency(dependency)

    def test_rarity_tool_hash_mutation_fails_closed(self) -> None:
        dependency = {"rarity_tool_merge_commit": PR4_MERGE_COMMIT, "rarity_tool_sha256": "sha256:" + "0" * 64, "rarity_tool_git_blob_oid": PR4_TOOL_BLOB_OID, "source_snapshot_commit": "a" * 40, "acquisition_commit": "b" * 40}
        with self.assertRaises(VerificationError):
            verify_stable_dependency(dependency)

    def test_rarity_runtime_patch_mutation_fails_closed(self) -> None:
        with mock.patch.object(verifier.platform, "python_version", return_value="3.12.13"):
            with self.assertRaises(VerificationError):
                verifier.verify_rarity_runtime()

    def test_forbidden_marketplace_metric_mutations_fail_closed(self) -> None:
        with self.assertRaises(VerificationError):
            reject_external_metrics({"OpenSea": {"score": 1}})
        with self.assertRaises(VerificationError):
            reject_external_metrics({"source": "https://opensea.io/assets/1/0x0/1"})

    def test_order_mutation_fails_closed(self) -> None:
        snapshot = {
            "tokens": [{"id": 0}],
            "source_metadata": [{}],
            "traits": [{"token_id": 0, "trait": "A", "value": "x", "source_row_index": 0, "source_feature_index": 0}],
            "source_trait_rows": [{"source_row_index": 0}],
            "ordering": {"source_token_order": [0], "canonical_token_order": [0], "source_trait_row_order": [0], "canonical_trait_order": [0]},
        }
        mutated = copy.deepcopy(snapshot)
        mutated["ordering"]["canonical_token_order"] = [1]
        with self.assertRaises(VerificationError):
            verify_ordering(mutated, [0], "mutated")

    def test_exclusion_marker_mutation_fails_closed(self) -> None:
        row = {"collection": "century", "cross_check_order": 0, "token_id": 100000000, "source_uri": "https://api.artblocks.io/token/100000000", "retrieval_uri": "https://api.artblocks.io/token/100000000", "raw_response": {"path": "raw/a.json", "sha256": "sha256:" + "0" * 64, "size": 1, "byte_mode": "raw"}, "source_location": "traits[0]", "source_order": 0, "excluded_row": {"trait_type": "CENTURY", "value": "All CENTURYs"}, "token_identity": {"metadata_token_id": "100000000", "contract_address": EXPECTED["century"]["contract_address"]}}
        check = {"source_uri": row["source_uri"], "retrieval_uri": row["retrieval_uri"], "raw_response": row["raw_response"]}
        raw = {"tokenID": "100000000", "traits": [{"trait_type": "CENTURY", "value": "All CENTURYs"}]}
        mutated = copy.deepcopy(row)
        mutated["excluded_row"]["value"] = "CENTURY"
        with self.assertRaises(VerificationError):
            verify_exclusion_row(mutated, check, raw, EXPECTED["century"]["contract_address"], {100000000 + i for i in range(EXPECTED["century"]["population"])}, 0)

    def test_population_mutation_fails_closed(self) -> None:
        config = json.loads((ROOT / "evidence/casey-reas-collection-snapshots/collection-sources.json").read_text(encoding="utf-8"))
        mutated = copy.deepcopy(config)
        mutated["collections"][0]["project_id"] = 101
        with self.assertRaises(VerificationError):
            validate_config(mutated)


if __name__ == "__main__":
    unittest.main()
