from __future__ import annotations

import contextlib
import io
import json
import math
import platform
from pathlib import Path
import tempfile
import unittest

from scripts.rarity.analyze import main
from scripts.rarity.nextgen_compat import (
    InputError,
    _dense_trait_ranks,
    analyze_snapshot,
    canonical_json,
)


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
        self.assertEqual(
            token_five["single_trait_rarity_score_trait_count_normalised"], 0.4
        )

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
        token_one = next(row for row in preserved["per_token"] if row["id"] == 1)
        self.assertAlmostEqual(token_one["statistical_score"], 0.140625)
        self.assertAlmostEqual(
            token_one["statistical_score_normalised"], 0.75 * 0.5
        )
        self.assertAlmostEqual(
            token_one["single_trait_rarity_score_trait_count_normalised"], 0.5
        )

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

    def test_opensea_metric_fields_are_prohibited_but_prose_is_allowed(self) -> None:
        allowed = json.loads(json.dumps(self.snapshot))
        allowed["source"]["note"] = "migrated off OpenSea in 2024"
        allowed["source"]["citation"] = "https://opensea.io/assets/example"
        analyze_snapshot(allowed)

        forbidden = json.loads(json.dumps(self.snapshot))
        forbidden["source"]["opensea_rarity_score"] = 1
        with self.assertRaisesRegex(InputError, "OpenSea"):
            analyze_snapshot(forbidden)

        sourced = json.loads(json.dumps(self.snapshot))
        sourced["source"]["provider"] = "OpenSea"
        sourced["source"]["rarity_score"] = 1
        with self.assertRaisesRegex(InputError, "OpenSea"):
            analyze_snapshot(sourced)

    def test_empty_trait_rank_group_is_defensive(self) -> None:
        rows: list[dict[str, object]] = []
        _dense_trait_ranks(rows, "rarity_score")
        self.assertEqual(rows, [])

    def test_cli_distinguishes_bad_data_from_bad_invocation(self) -> None:
        bad = json.loads(json.dumps(self.snapshot))
        bad["source"]["opensea_rarity_score"] = 1
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.json"
            path.write_text(json.dumps(bad), encoding="utf-8")
            with contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(main([str(path)]), 1)

        with contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit) as error:
                main([])
        self.assertEqual(error.exception.code, 2)

    def test_canonical_float_boundary_is_explicit(self) -> None:
        result = analyze_snapshot(self.snapshot)
        profile = result["determinism"]
        self.assertEqual(profile["implementation"], platform.python_implementation())
        self.assertEqual(profile["python_version"], platform.python_version())
        self.assertIn("same CPython implementation and version", profile["boundary"])
        self.assertEqual(
            canonical_json({"value": 0.1 + 0.2}),
            b'{"value":0.30000000000000004}',
        )
        self.assertEqual(canonical_json({"value": 1.0}), b'{"value":1.0}')

    def test_hashes_are_stable_for_repeated_runs(self) -> None:
        first = analyze_snapshot(self.snapshot)
        second = analyze_snapshot(self.snapshot)
        self.assertEqual(first, second)
        self.assertTrue(first["hashes"]["output_sha256"].startswith("sha256:"))


if __name__ == "__main__":
    unittest.main()
