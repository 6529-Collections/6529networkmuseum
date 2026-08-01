from __future__ import annotations

import contextlib
import io
import json
import platform
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from scripts.rarity.analyze import main
from scripts.rarity.nextgen_compat import (
    InputError,
    _dense_trait_ranks,
    _left_to_right_sum,
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
        actual = analyze_snapshot(self.snapshot)
        expected = read_json(EXPECTED)
        expected["determinism"] = actual["determinism"]
        self.assertEqual(actual, expected)

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

    def test_marketplace_metric_fields_are_prohibited_but_provenance_is_allowed(
        self,
    ) -> None:
        allowed = json.loads(json.dumps(self.snapshot))
        allowed["source"]["note"] = "migrated off OpenSea in 2024"
        allowed["source"]["citation"] = "https://opensea.io/assets/example"
        allowed["source"]["opensea_trait_source_url"] = (
            "https://opensea.io/assets/example"
        )
        allowed["source"]["marketplace_url"] = "https://looksrare.org/collections/example"
        allowed["source"]["looksrare_citation_url"] = (
            "https://looksrare.org/collections/example"
        )
        allowed["source"]["provenance"] = (
            "The accession history mentions OpenSea and LooksRare as prior listings."
        )
        analyze_snapshot(allowed)

        for service in ("opensea", "looksrare"):
            forbidden = json.loads(json.dumps(self.snapshot))
            forbidden["source"][f"{service}_rarity_score"] = 1
            with self.assertRaisesRegex(InputError, "third-party"):
                analyze_snapshot(forbidden)

        provenance_citation = json.loads(json.dumps(self.snapshot))
        provenance_citation["source"]["rarity_provenance"] = (
            "https://museum.example/methodology"
        )
        provenance_citation["source"]["rarity_provenance_note"] = (
            "The methodology explains why OpenSea and LooksRare metrics are "
            "not imported."
        )
        analyze_snapshot(provenance_citation)

        provenance_with_metric = json.loads(json.dumps(self.snapshot))
        provenance_with_metric["source"]["rarity_provenance"] = {
            "url": "https://museum.example/methodology",
            "score": 1,
        }
        with self.assertRaisesRegex(InputError, "provenance/methodology"):
            analyze_snapshot(provenance_with_metric)

    def test_precomputed_metrics_are_rejected_at_any_depth_and_provider_claim(
        self,
    ) -> None:
        for semantic_key in (
            "provider",
            "marketplace",
            "service",
            "source",
            "origin",
            "issuer",
        ):
            invalid = json.loads(json.dumps(self.snapshot))
            invalid["source"][semantic_key] = "LooksRare"
            invalid["source"]["rarity_score"] = 1
            with self.subTest(semantic_key=semantic_key), self.assertRaisesRegex(
                InputError, "third-party"
            ):
                analyze_snapshot(invalid)

        for wrapper in (
            {"provider": {"url": "https://looksrare.org"}},
            {"provider": {"metadata": {"name": "LooksRare"}}},
            {"marketplace": {"url": "https://looksrare.org"}},
            {"service": {"metadata": {"name": "UnknownRarityService"}}},
            {"source": {"origin": {"issuer": "LooksRare"}}},
        ):
            nested = json.loads(json.dumps(self.snapshot))
            nested["source"]["evidence"] = {
                "wrapper": wrapper,
                "rarity_score": 1,
            }
            with self.subTest(wrapper=wrapper), self.assertRaisesRegex(
                InputError, "precomputed"
            ):
                analyze_snapshot(nested)

        internal_claim = json.loads(json.dumps(self.snapshot))
        internal_claim["source"]["provider"] = "6529 NextGen"
        internal_claim["source"]["wrapper"] = {"score": 1}
        with self.assertRaisesRegex(InputError, "precomputed"):
            analyze_snapshot(internal_claim)

        provenance_url = json.loads(json.dumps(self.snapshot))
        provenance_url["source"]["rarity_provenance"] = {
            "url": "https://looksrare.org/collection/example",
            "note": "prior marketplace citation only; no score or rank imported",
            "provider": {"url": "https://looksrare.org"},
        }
        analyze_snapshot(provenance_url)

    def test_left_fold_matches_javascript_reduce_not_python_sum(self) -> None:
        values = [1e16, 1.0, -1e16, 1.0]

        javascript_reduce = 0.0
        for value in values:
            javascript_reduce += value

        self.assertEqual(sum(values), 2.0)
        self.assertEqual(javascript_reduce, 1.0)
        self.assertEqual(_left_to_right_sum(values), javascript_reduce)

    def test_source_order_is_separate_from_canonical_presentation(self) -> None:
        reordered = json.loads(json.dumps(self.snapshot))
        reordered["tokens"] = [
            reordered["tokens"][2],
            reordered["tokens"][0],
            reordered["tokens"][3],
            reordered["tokens"][1],
        ]
        reordered["traits"] = list(reversed(reordered["traits"]))

        result = analyze_snapshot(reordered)
        self.assertEqual(
            [row["id"] for row in result["per_token"]], [3, 1, 4, 2]
        )
        self.assertEqual(
            [
                (row["token_id"], row["trait"], row["value"])
                for row in result["per_trait"]
            ],
            [
                (row["token_id"], row["trait"], row["value"])
                for row in reordered["traits"]
            ],
        )

        normalized = result["input"]["normalized_snapshot"]
        self.assertEqual([row["id"] for row in normalized["tokens"]], [1, 2, 3, 4])
        self.assertEqual(
            [
                (row["token_id"], row["trait"], row["value"])
                for row in normalized["traits"]
            ],
            sorted(
                (
                    row["token_id"],
                    row["trait"],
                    row["value"],
                )
                for row in reordered["traits"]
            ),
        )

    def test_snapshot_identity_and_provenance_are_required(self) -> None:
        missing_fields = (
            "snapshot_id",
            "observed_at",
            "collection",
            "source",
        )
        for field in missing_fields:
            invalid = json.loads(json.dumps(self.snapshot))
            invalid.pop(field)
            with self.subTest(field=field), self.assertRaises(InputError):
                analyze_snapshot(invalid)

        invalid_source = json.loads(json.dumps(self.snapshot))
        invalid_source["source"] = {}
        with self.assertRaisesRegex(InputError, "source provenance"):
            analyze_snapshot(invalid_source)

        mixed = json.loads(json.dumps(self.snapshot))
        mixed["traits"][0]["collection_id"] = 9002
        with self.assertRaisesRegex(InputError, "mixed collection_id"):
            analyze_snapshot(mixed)

    def test_mint_type_only_snapshot_matches_compatibility_scoring(self) -> None:
        mint_only = json.loads(json.dumps(self.snapshot))
        mint_only["tokens"] = [
            {"id": 1, "collection_id": 9001},
            {"id": 2, "collection_id": 9001},
        ]
        mint_only["traits"] = [
            {
                "token_id": 1,
                "collection_id": 9001,
                "trait": "Mint Type",
                "value": "Public",
            },
            {
                "token_id": 2,
                "collection_id": 9001,
                "trait": "Mint Type",
                "value": "Airdrop",
            },
        ]

        result = analyze_snapshot(mint_only)
        self.assertEqual(result["collection_summary"]["non_mint_type_trait_category_count"], 0)
        self.assertEqual(
            {row["rarity_score"] for row in result["per_trait"]}, {-1}
        )
        for token in result["per_token"]:
            self.assertEqual(token["rarity_score"], 0)
            self.assertEqual(token["rarity_score_trait_count"], 1.0)
            self.assertEqual(token["rarity_score_trait_count_normalised"], 500000.0)
            self.assertEqual(token["statistical_score"], 1)
            self.assertEqual(token["statistical_score_trait_count"], 1.0)
            self.assertEqual(token["statistical_score_normalised"], 1)
            self.assertEqual(token["statistical_score_trait_count_normalised"], 1.0)
            self.assertEqual(token["single_trait_rarity_score"], 0)
            self.assertEqual(token["single_trait_rarity_score_trait_count"], 0)
            self.assertEqual(token["single_trait_rarity_score_normalised"], 0)
            self.assertEqual(
                token["single_trait_rarity_score_trait_count_normalised"], 1.0
            )

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

    def test_cli_rejects_non_finite_json_and_output_failures_without_traceback(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for constant in ("NaN", "Infinity", "-Infinity"):
                path = root / f"{constant.replace('-', 'negative-')}.json"
                text = json.dumps(self.snapshot)[:-1]
                path.write_text(f'{text},"non_finite":{constant}}}', encoding="utf-8")
                stderr = io.StringIO()
                with contextlib.redirect_stderr(stderr):
                    self.assertEqual(main([str(path)]), 1)
                self.assertNotIn("Traceback", stderr.getvalue())

            output_directory = root / "output-directory"
            output_directory.mkdir()
            stderr = io.StringIO()
            with contextlib.redirect_stderr(stderr):
                self.assertEqual(
                    main([str(FIXTURE), "--output", str(output_directory)]), 1
                )
            self.assertNotIn("Traceback", stderr.getvalue())

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

    def test_runtime_profile_is_recorded_but_not_hashed(self) -> None:
        actual = analyze_snapshot(self.snapshot)
        alternate_profile = {
            "implementation": "alternate-runtime",
            "python_version": "0.0.0",
            "json_encoder": "alternate encoder",
            "float_encoding": "alternate float encoding",
            "boundary": "alternate boundary",
        }
        with patch(
            "scripts.rarity.nextgen_compat.determinism_profile",
            return_value=alternate_profile,
        ):
            alternate = analyze_snapshot(self.snapshot)
        self.assertNotEqual(actual["determinism"], alternate["determinism"])
        self.assertEqual(
            actual["hashes"]["output_sha256"],
            alternate["hashes"]["output_sha256"],
        )

    def test_hashes_are_stable_for_repeated_runs(self) -> None:
        first = analyze_snapshot(self.snapshot)
        second = analyze_snapshot(self.snapshot)
        self.assertEqual(first, second)
        self.assertTrue(first["hashes"]["output_sha256"].startswith("sha256:"))


if __name__ == "__main__":
    unittest.main()
