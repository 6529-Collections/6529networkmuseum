from __future__ import annotations

import json
from pathlib import Path
import unittest

from scripts.rarity.nextgen_compat import InputError, analyze_snapshot


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "tests" / "rarity" / "fixtures" / "nextgen-compatibility.json"
EXPECTED = (
    ROOT / "tests" / "rarity" / "fixtures" / "nextgen-compatibility.expected.json"
)


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


class NextGenCompatibilityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.snapshot = read_json(FIXTURE)

    def test_full_output_matches_exact_compatibility_fixture(self) -> None:
        expected = read_json(EXPECTED)
        self.assertEqual(analyze_snapshot(self.snapshot), expected)

    def test_missing_rows_are_reported_and_not_synthesized(self) -> None:
        result = analyze_snapshot(self.snapshot)
        quality = result["input"]["data_quality"]
        self.assertEqual(quality["tokens_without_any_trait_rows"], [])
        self.assertEqual(
            quality["missing_token_ids_by_observed_trait"],
            [
                {"trait": "Accent", "missing_token_ids": [1]},
                {"trait": "Color", "missing_token_ids": []},
                {"trait": "Form", "missing_token_ids": []},
                {"trait": "Mint Type", "missing_token_ids": [2, 3, 4]},
            ],
        )
        token_one = next(row for row in result["per_token"] if row["id"] == 1)
        self.assertEqual(token_one["trait_count"], 2)

        sparse = json.loads(json.dumps(self.snapshot))
        sparse["tokens"].append({"id": 5, "collection_id": 9001})
        sparse_result = analyze_snapshot(sparse)
        self.assertEqual(
            sparse_result["input"]["data_quality"]["tokens_without_any_trait_rows"],
            [5],
        )
        self.assertEqual(sparse_result["collection_summary"]["observed_token_count"], 4)
        self.assertEqual(sparse_result["collection_summary"]["declared_token_count"], 5)
        token_five = next(row for row in sparse_result["per_token"] if row["id"] == 5)
        self.assertEqual(token_five["trait_count"], 0)
        self.assertEqual(token_five["rarity_score"], 0)

    def test_trait_and_token_ties_use_the_source_rank_rules(self) -> None:
        result = analyze_snapshot(self.snapshot)
        form_rows = [row for row in result["per_trait"] if row["trait"] == "Form"]
        self.assertEqual(
            {(row["value"], row["rarity_score_rank"]) for row in form_rows},
            {("Circle", 1), ("Square", 2)},
        )
        token_three = next(row for row in result["per_token"] if row["id"] == 3)
        token_four = next(row for row in result["per_token"] if row["id"] == 4)
        self.assertEqual(token_three["rarity_score_rank"], 3)
        self.assertEqual(token_four["rarity_score_rank"], 3)
        self.assertEqual(token_three["statistical_score_rank"], 3)
        self.assertEqual(token_four["statistical_score_rank"], 3)

    def test_duplicate_rows_require_an_explicit_policy(self) -> None:
        duplicate = json.loads(json.dumps(self.snapshot))
        duplicate["traits"].append(duplicate["traits"][0])
        with self.assertRaises(InputError):
            analyze_snapshot(duplicate)

        preserved = analyze_snapshot(duplicate, duplicate_policy="preserve")
        self.assertEqual(
            preserved["input"]["data_quality"]["duplicate_trait_rows"],
            [{"token_id": 1, "trait": "Color", "count": 2, "values": ["Red", "Red"]}],
        )
        red = next(
            row
            for row in preserved["per_trait"]
            if row["token_id"] == 1 and row["trait"] == "Color"
        )
        self.assertEqual(red["value_count"], 3)

        deduplicated = analyze_snapshot(duplicate, duplicate_policy="deduplicate")
        self.assertEqual(
            deduplicated["per_token"], analyze_snapshot(self.snapshot)["per_token"]
        )

    def test_orphan_rows_are_explicitly_rejected_or_preserved(self) -> None:
        orphan = json.loads(json.dumps(self.snapshot))
        orphan["traits"].append(
            {
                "token_id": 99,
                "collection_id": 9001,
                "trait": "Color",
                "value": "Purple",
            }
        )
        with self.assertRaises(InputError):
            analyze_snapshot(orphan)
        preserved = analyze_snapshot(orphan, duplicate_policy="preserve")
        self.assertEqual(
            preserved["input"]["data_quality"]["orphan_trait_rows"],
            [{"token_id": 99, "trait": "Color", "value": "Purple"}],
        )
        self.assertIn(99, [row["token_id"] for row in preserved["per_trait"]])
        self.assertEqual([row["id"] for row in preserved["per_token"]], [1, 2, 3, 4])

    def test_opensea_references_are_prohibited(self) -> None:
        forbidden = json.loads(json.dumps(self.snapshot))
        forbidden["source"]["opensea_metric"] = 1
        with self.assertRaisesRegex(InputError, "OpenSea"):
            analyze_snapshot(forbidden)

    def test_hashes_are_stable_for_repeated_runs(self) -> None:
        first = analyze_snapshot(self.snapshot)
        second = analyze_snapshot(self.snapshot)
        self.assertEqual(first, second)
        self.assertTrue(first["hashes"]["output_sha256"].startswith("sha256:"))


if __name__ == "__main__":
    unittest.main()
