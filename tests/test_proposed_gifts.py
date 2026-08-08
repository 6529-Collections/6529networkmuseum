from __future__ import annotations

import copy
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from proposed_gifts import (  # noqa: E402
    MAX_WAVE_PART_UTF16_CODE_UNITS,
    MAX_WAVE_PART_UTF8_BYTES,
    MAX_WAVE_STORM_MEDIA_FILES,
    MAX_WAVE_STORM_UTF16_CODE_UNITS,
    compose_voter_dossier,
    proposed_gift_issues,
    utf16_code_units,
    utf8_byte_length,
)


class ProposedGiftValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.register_path = (REPO_ROOT / "records/proposed-gifts/register.json").resolve()
        self.proposal_path = (
            REPO_ROOT / "records/proposed-gifts/6529NM-PG-2026-001/proposal.json"
        ).resolve()
        self.package_path = (
            REPO_ROOT / "records/proposed-gifts/6529NM-PG-2026-001/wave-storm.json"
        ).resolve()
        self.loaded = {
            self.register_path: json.loads(self.register_path.read_text(encoding="utf-8")),
            self.proposal_path: json.loads(self.proposal_path.read_text(encoding="utf-8")),
            self.package_path: json.loads(self.package_path.read_text(encoding="utf-8")),
        }

    def issues_after(self, mutate) -> list[str]:
        loaded = copy.deepcopy(self.loaded)
        mutate(loaded)
        return proposed_gift_issues(REPO_ROOT, loaded)

    def test_canonical_package_is_semantically_complete(self) -> None:
        self.assertEqual(proposed_gift_issues(REPO_ROOT, self.loaded), [])

    def test_magnum_winner_status_amendment_is_current_and_bounded(self) -> None:
        proposal = self.loaded[self.proposal_path]
        register = self.loaded[self.register_path]
        package = self.loaded[self.package_path]
        amendment_path = (
            self.proposal_path.parent
            / "public/status-amendments/2026-08-08-winner.md"
        )
        amendment = amendment_path.read_text(encoding="utf-8")
        drop = proposal["wave_authority"]["proposal_drop"]

        self.assertEqual(proposal["status"], "selected")
        self.assertEqual(proposal["status_as_of"], "2026-08-08T10:15:02.0167151Z")
        self.assertEqual(drop["status"], "WINNER")
        self.assertEqual(drop["status_observed_at"], "2026-08-08T10:15:02.0167151Z")
        self.assertEqual(package["status"], "selected")
        self.assertEqual(register["snapshot_at"], "2026-08-08T10:15:02.0167151Z")
        self.assertEqual(register["proposals"][0]["status"], "selected")
        self.assertEqual(register["proposals"][0]["wave_status"], "selected")
        self.assertIn(
            "Selected by Museum Wave; acquisition review in progress",
            amendment,
        )
        self.assertIn("selected_by_museum_wave_acquisition_review_in_progress", amendment)
        self.assertIn("PARTICIPATORY", amendment)
        self.assertIn("122,969,240", amendment)
        self.assertIn("WINNER", amendment)
        self.assertIn("121603214", amendment)
        for boundary in (
            "formal acceptance",
            "donor authority",
            "legal title",
            "Museum custody",
            "rights clearance",
            "preservation completion",
            "accession",
            "Collection membership",
        ):
            self.assertIn(boundary, amendment)

        resolution = (self.proposal_path.parent / "public/wave-resolution.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("status-amendments/2026-08-08-winner.md", resolution)

    def test_wave_selects_the_gift_before_later_accession_work(self) -> None:
        proposal = self.loaded[self.proposal_path]
        opening = (
            self.proposal_path.parent / "public/wave-storm/01-resolution.md"
        ).read_text(encoding="utf-8")
        self.assertEqual(proposal["resolution"]["threshold_cleared_effect"], "gift_selected")
        self.assertIn("the five-work gift is selected", opening)
        self.assertIn("and accession will follow", opening)
        self.assertNotIn("schedule for accession processing", opening)
        self.assertNotIn("scheduled ERC-721", opening)

    def test_donor_title_is_canonical_across_public_package(self) -> None:
        proposal = self.loaded[self.proposal_path]
        register = self.loaded[self.register_path]
        package = self.loaded[self.package_path]
        opening = (
            self.proposal_path.parent / "public/wave-storm/01-resolution.md"
        ).read_text(encoding="utf-8")
        self.assertEqual(proposal["title"], "Conflict at Its Edges")
        self.assertEqual(
            proposal["subtitle"],
            "Five Photographs of Evidence and Aftermath, 1952–2016",
        )
        self.assertEqual(register["proposals"][0]["title"], proposal["title"])
        self.assertEqual(package["drop_title"], proposal["title"])
        self.assertEqual(package["parts"][0]["title"], "Proposed gift: Conflict at Its Edges")
        self.assertEqual(package["parts"][-1]["title"], proposal["title"])
        self.assertIn(
            "Conflict at Its Edges: Five Photographs of Evidence and Aftermath, 1952–2016",
            opening,
        )

    def test_voter_dossier_is_exact_storm_projection(self) -> None:
        package = self.loaded[self.package_path]
        candidate_dir = self.proposal_path.parent
        expected = compose_voter_dossier(candidate_dir, package)
        dossier = candidate_dir / "public/voter-dossier.md"
        self.assertEqual(dossier.read_text(encoding="utf-8"), expected)

    def test_storm_fits_the_publication_envelope(self) -> None:
        package = self.loaded[self.package_path]
        candidate_dir = self.proposal_path.parent
        contents = [
            (candidate_dir / part["markdown_path"]).read_text(encoding="utf-8")
            for part in package["parts"]
        ]
        total_utf16_code_units = sum(utf16_code_units(content) for content in contents)
        total_utf8_bytes = sum(utf8_byte_length(content) for content in contents)
        total_media = sum(len(part["media"]) for part in package["parts"])
        cover = package["parts"][0]["media"][0]

        self.assertTrue(
            all(utf16_code_units(content) <= MAX_WAVE_PART_UTF16_CODE_UNITS for content in contents)
        )
        self.assertTrue(all(utf8_byte_length(content) <= MAX_WAVE_PART_UTF8_BYTES for content in contents))
        self.assertLessEqual(total_utf16_code_units, MAX_WAVE_STORM_UTF16_CODE_UNITS)
        self.assertEqual(total_media, 6)
        self.assertLessEqual(total_media, MAX_WAVE_STORM_MEDIA_FILES)
        self.assertEqual(
            package["publication_profile"]["totals"],
            {
                "utf16_code_units": total_utf16_code_units,
                "utf8_bytes": total_utf8_bytes,
                "media_count": total_media,
            },
        )
        self.assertEqual(cover["media_type"], "image/png")
        self.assertEqual((cover["width"], cover["height"]), (1600, 1600))
        self.assertEqual(cover["rights_label"], "CC0-1.0")

    def test_text_metric_boundaries_match_javascript_and_utf8(self) -> None:
        self.assertEqual(utf16_code_units("😀"), 2)
        self.assertEqual(utf8_byte_length("😀"), 4)
        self.assertEqual(utf16_code_units("a" * 25_000), MAX_WAVE_PART_UTF16_CODE_UNITS)
        self.assertEqual(utf8_byte_length("a" * 65_535), MAX_WAVE_PART_UTF8_BYTES)
        self.assertGreater(utf16_code_units("😀" * 12_501), MAX_WAVE_PART_UTF16_CODE_UNITS)
        self.assertGreater(utf8_byte_length("漢" * 21_846), MAX_WAVE_PART_UTF8_BYTES)

    def test_rejects_storm_over_total_character_limit(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            shutil.copytree(REPO_ROOT / "records/proposed-gifts", root / "records/proposed-gifts")
            candidate_dir = root / "records/proposed-gifts/6529NM-PG-2026-001"
            additions = {
                "public/wave-storm/01-resolution.md": "a" * 8_000,
                "public/wave-storm/07-case-and-decision.md": "b" * 8_000,
            }
            for relative, addition in additions.items():
                source = candidate_dir / relative
                source.write_text(
                    source.read_text(encoding="utf-8") + "\n\n" + addition + "\n",
                    encoding="utf-8",
                )
            loaded = {
                path.resolve(): json.loads(path.read_text(encoding="utf-8"))
                for path in (root / "records/proposed-gifts").rglob("*.json")
            }
            issues = proposed_gift_issues(root, loaded)
        self.assertTrue(any("exceeds 50000 total UTF-16 code units" in issue for issue in issues))

    def test_rejects_storm_part_over_utf16_limit(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            shutil.copytree(REPO_ROOT / "records/proposed-gifts", root / "records/proposed-gifts")
            candidate_dir = root / "records/proposed-gifts/6529NM-PG-2026-001"
            source = candidate_dir / "public/wave-storm/02-david-seymour-127.md"
            source.write_text("a" * 25_001, encoding="utf-8", newline="\n")
            loaded = {
                path.resolve(): json.loads(path.read_text(encoding="utf-8"))
                for path in (root / "records/proposed-gifts").rglob("*.json")
            }
            issues = proposed_gift_issues(root, loaded)
        self.assertTrue(any("part 2 exceeds 25000 UTF-16 code units" in issue for issue in issues))

    def test_rejects_storm_part_over_utf8_byte_limit(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            shutil.copytree(REPO_ROOT / "records/proposed-gifts", root / "records/proposed-gifts")
            candidate_dir = root / "records/proposed-gifts/6529NM-PG-2026-001"
            source = candidate_dir / "public/wave-storm/02-david-seymour-127.md"
            source.write_text("漢" * 21_846, encoding="utf-8", newline="\n")
            loaded = {
                path.resolve(): json.loads(path.read_text(encoding="utf-8"))
                for path in (root / "records/proposed-gifts").rglob("*.json")
            }
            issues = proposed_gift_issues(root, loaded)
        self.assertTrue(any("part 2 exceeds 65535 UTF-8 bytes" in issue for issue in issues))

    def test_rejects_publication_metric_drift(self) -> None:
        issues = self.issues_after(
            lambda loaded: loaded[self.package_path]["publication_profile"]["totals"].update(
                {"utf16_code_units": 1}
            )
        )
        self.assertTrue(any("publication totals do not match" in issue for issue in issues))

    def test_rejects_more_than_eight_storm_media_files(self) -> None:
        def mutate(loaded) -> None:
            cover = loaded[self.package_path]["parts"][0]["media"][0]
            loaded[self.package_path]["parts"][0]["media"].extend(
                [copy.deepcopy(cover) for _ in range(3)]
            )

        issues = self.issues_after(mutate)
        self.assertTrue(any("exceeds 8 total media files" in issue for issue in issues))

    def test_rejects_cover_fixity_drift(self) -> None:
        issues = self.issues_after(
            lambda loaded: loaded[self.package_path]["parts"][0]["media"][0].update(
                {"sha256": "0" * 64}
            )
        )
        self.assertTrue(any("cover image SHA-256 does not match" in issue for issue in issues))

    def test_rejects_image_that_does_not_join_to_object(self) -> None:
        issues = self.issues_after(
            lambda loaded: loaded[self.package_path]["parts"][1]["media"][0].update(
                {"uri": "https://arweave.net/not-the-gift-image"}
            )
        )
        self.assertTrue(any("work image does not match" in issue for issue in issues))

    def test_rejects_missing_or_duplicate_work_part(self) -> None:
        def mutate(loaded) -> None:
            loaded[self.package_path]["parts"][2]["candidate_object_id"] = loaded[self.package_path]["parts"][1][
                "candidate_object_id"
            ]

        issues = self.issues_after(mutate)
        self.assertTrue(any("match the gift's object list exactly and in order" in issue for issue in issues))

    def test_rejects_path_traversal(self) -> None:
        issues = self.issues_after(
            lambda loaded: loaded[self.package_path]["parts"][0].update(
                {"markdown_path": "../proposal.json"}
            )
        )
        self.assertTrue(any("invalid Storm markdown path" in issue for issue in issues))

    def test_rejects_partial_chain_observation(self) -> None:
        issues = self.issues_after(
            lambda loaded: loaded[self.proposal_path]["objects"][0]["chain_observation"].update(
                {"status": "pending_finalized_block_observation"}
            )
        )
        self.assertTrue(any("pending chain observation is partially populated" in issue for issue in issues))

    def test_rejects_register_status_drift(self) -> None:
        issues = self.issues_after(
            lambda loaded: loaded[self.register_path]["proposals"][0].update({"wave_status": "open"})
        )
        self.assertTrue(any("Wave status does not match" in issue for issue in issues))

    def test_rejects_discontinuous_provenance(self) -> None:
        issues = self.issues_after(
            lambda loaded: loaded[self.proposal_path]["objects"][0]["provenance"]["transfers"][1].update(
                {"from": "0x0000000000000000000000000000000000000001"}
            )
        )
        self.assertTrue(any("transfer chain is discontinuous" in issue for issue in issues))

    def test_rejects_reordered_work_parts_even_when_renumbered(self) -> None:
        def mutate(loaded) -> None:
            parts = loaded[self.package_path]["parts"]
            parts[1], parts[2] = parts[2], parts[1]
            for index, part in enumerate(parts, start=1):
                part["part_number"] = index

        issues = self.issues_after(mutate)
        self.assertTrue(any("match the gift's object list exactly and in order" in issue for issue in issues))

    def test_rejects_duplicate_storm_source_path(self) -> None:
        issues = self.issues_after(
            lambda loaded: loaded[self.package_path]["parts"][2].update(
                {"markdown_path": loaded[self.package_path]["parts"][1]["markdown_path"]}
            )
        )
        self.assertTrue(any("reuse a Markdown source path" in issue for issue in issues))

    def test_rejects_resolution_drift_between_first_and_last_part(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            shutil.copytree(REPO_ROOT / "records/proposed-gifts", root / "records/proposed-gifts")
            closing = root / "records/proposed-gifts/6529NM-PG-2026-001/public/wave-storm/07-case-and-decision.md"
            closing.write_text(
                closing.read_text(encoding="utf-8").replace(
                    "future gifts from Magnum Photos 75", "later gifts from Magnum Photos 75"
                ),
                encoding="utf-8",
            )
            loaded = {
                path.resolve(): json.loads(path.read_text(encoding="utf-8"))
                for path in (root / "records/proposed-gifts").rglob("*.json")
            }
            issues = proposed_gift_issues(root, loaded)
        self.assertTrue(any("opening and closing Resolution sections differ" in issue for issue in issues))

    def test_rejects_soft_wrapped_storm_prose(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            shutil.copytree(REPO_ROOT / "records/proposed-gifts", root / "records/proposed-gifts")
            source = root / "records/proposed-gifts/6529NM-PG-2026-001/public/wave-storm/02-david-seymour-127.md"
            source.write_text(
                source.read_text(encoding="utf-8").replace(
                    "born Dawid Szymin", "born\nDawid Szymin"
                ),
                encoding="utf-8",
            )
            loaded = {
                path.resolve(): json.loads(path.read_text(encoding="utf-8"))
                for path in (root / "records/proposed-gifts").rglob("*.json")
            }
            issues = proposed_gift_issues(root, loaded)
        self.assertTrue(any("ambiguous Markdown soft break" in issue for issue in issues))

    def test_rejects_media_credit_drift(self) -> None:
        issues = self.issues_after(
            lambda loaded: loaded[self.package_path]["parts"][1]["media"][0].update(
                {"credit_line": "Unattributed"}
            )
        )
        self.assertTrue(any("credit does not match" in issue for issue in issues))

    def test_rejects_noncanonical_document_topology(self) -> None:
        issues = self.issues_after(
            lambda loaded: loaded[self.proposal_path]["documents"].update(
                {"wave_resolution": "records/proposed-gifts/README.md"}
            )
        )
        self.assertTrue(any("wave_resolution does not use the canonical" in issue for issue in issues))


if __name__ == "__main__":
    unittest.main()
