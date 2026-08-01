"""Negative controls for Casey package bindings and semantic guards."""

from __future__ import annotations

import copy
import json
from pathlib import Path
import unittest

from scripts.verify_casey_snapshot_package import (
    EXPECTED,
    PR4_MERGE_COMMIT,
    PR4_TOOL_BLOB_OID,
    PR4_TOOL_SHA256,
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
