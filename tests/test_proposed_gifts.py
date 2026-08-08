from __future__ import annotations

import copy
import hashlib
import json
import re
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
    _control_time,
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

    def copied_lineage_issues(self, mutate) -> list[str]:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            shutil.copytree(REPO_ROOT / "records/proposed-gifts", root / "records/proposed-gifts")
            loaded = {
                path.resolve(): json.loads(path.read_text(encoding="utf-8"))
                for path in (root / "records/proposed-gifts").rglob("*.json")
            }
            mutate(root, loaded)
            return proposed_gift_issues(root, loaded)

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
        self.assertEqual(
            proposal["resolution"]["later_required_events"],
            [
                "identity_verification",
                "donor_authority",
                "title_review",
                "rights_review",
                "technical_review",
                "transfer",
                "custody_receipt",
                "formal_acceptance",
                "preservation",
                "accession",
            ],
        )
        self.assertEqual(
            register["proposals"][0]["collection_status_effect"],
            "none_until_later_formal_acceptance_and_accession",
        )
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
        self.assertIn("schema status `selected` is a proposal-record layer", amendment)
        self.assertIn("future WP-1 Work-entity lifecycle", amendment)

        local_links = [
            target.split("#", 1)[0]
            for target in re.findall(r"\[[^]]+\]\(([^)]+)\)", amendment)
            if not target.startswith(("http://", "https://", "mailto:"))
        ]
        self.assertEqual(local_links, ["../wave-resolution.md"])
        self.assertTrue((amendment_path.parent / local_links[0]).resolve().is_file())

        resolution = (self.proposal_path.parent / "public/wave-resolution.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("status-amendments/2026-08-08-winner.md", resolution)
        self.assertIn("## Effect (historical publication rule)", resolution)
        self.assertIn("historical publication rule", resolution)

    def test_magnum_revision_two_binds_exact_revision_one_snapshots(self) -> None:
        expected = {
            self.proposal_path: (
                self.proposal_path.parent / "history/revision-1-proposal.json.snapshot",
                "sha256:b561564c19ff9e9ad74a4660a33df7dc113c20a6672560f81fbd97213e3966fd",
            ),
            self.package_path: (
                self.package_path.parent / "history/revision-1-wave-storm.json.snapshot",
                "sha256:2afab11df2fc258c76b79c547b86992ddc9b45d338de005a93682c736c514262",
            ),
            self.register_path: (
                self.register_path.parent / "6529NM-PG-2026-001/history/revision-1-register.json.snapshot",
                "sha256:2b030517bea9c39e4c0e495ea11041307681cecb95a3e2e62d3873588ecc42ff",
            ),
        }
        for current_path, (snapshot_path, expected_hash) in expected.items():
            current = self.loaded[current_path]
            self.assertEqual(current["record_control"]["revision"], 2)
            self.assertEqual(
                current["record_control"]["constructor"]["constructed_at"],
                "2026-08-08T10:15:02.0167151Z",
            )
            history = current["amendment_history"]
            self.assertEqual([entry["revision"] for entry in history], [1])
            entry = history[0]
            self.assertEqual(entry["supersedes"], expected_hash)
            self.assertEqual(entry["prior_payload_sha256"], expected_hash)
            self.assertEqual(
                entry["prior_source_commit"],
                "4821ea52e4cb8e0f0915824fbc2946ec0f6313b8",
            )
            self.assertEqual(
                entry["prior_snapshot_path"],
                snapshot_path.relative_to(REPO_ROOT).as_posix(),
            )
            raw = snapshot_path.read_bytes()
            normalized = raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
            self.assertEqual(
                "sha256:" + hashlib.sha256(normalized).hexdigest(),
                expected_hash,
            )
            snapshot = json.loads(normalized.decode("utf-8"))
            self.assertEqual(snapshot["record_control"]["revision"], 1)
            self.assertNotIn("amendment_history", snapshot)

    def test_revision_lineage_cannot_silently_drop_or_reorder_history(self) -> None:
        issues = self.issues_after(
            lambda loaded: loaded[self.proposal_path].pop("amendment_history")
        )
        self.assertTrue(
            any("count must equal current revision minus one" in issue for issue in issues),
            issues,
        )
        issues = self.issues_after(
            lambda loaded: loaded[self.proposal_path]["amendment_history"][0].__setitem__(
                "revision", 2
            )
        )
        self.assertTrue(any("unique, increasing" in issue for issue in issues), issues)
        issues = self.issues_after(
            lambda loaded: loaded[self.proposal_path]["amendment_history"][0].__setitem__(
                "supersedes", "sha256:" + "0" * 64
            )
        )
        self.assertTrue(any("supersedes and prior payload hash differ" in issue for issue in issues), issues)

    def test_revision_lineage_rejects_unsafe_and_missing_snapshot_paths(self) -> None:
        issues = self.issues_after(
            lambda loaded: loaded[self.proposal_path]["amendment_history"][0].__setitem__(
                "prior_snapshot_path", "../proposal.json"
            )
        )
        self.assertTrue(any("unsafe prior snapshot path" in issue for issue in issues), issues)
        issues = self.issues_after(
            lambda loaded: loaded[self.proposal_path]["amendment_history"][0].__setitem__(
                "prior_snapshot_path",
                "records/proposed-gifts/6529NM-PG-2026-001/history/missing.json.snapshot",
            )
        )
        self.assertTrue(any("prior snapshot is missing" in issue for issue in issues), issues)

    def test_revision_lineage_binds_stable_identity(self) -> None:
        def rewrite_snapshot(root: Path, loaded: dict[Path, object], current_relative: str, snapshot_name: str, mutate) -> None:
            snapshot_path = root / "records/proposed-gifts/6529NM-PG-2026-001/history" / snapshot_name
            snapshot = json.loads(snapshot_path.read_text(encoding="utf-8"))
            mutate(snapshot)
            snapshot_path.write_bytes((json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
            normalized = snapshot_path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
            digest = "sha256:" + hashlib.sha256(normalized).hexdigest()
            current_path = (root / "records/proposed-gifts" / current_relative).resolve()
            entry = loaded[current_path]["amendment_history"][0]
            entry["supersedes"] = digest
            entry["prior_payload_sha256"] = digest

        issues = self.copied_lineage_issues(
            lambda root, loaded: rewrite_snapshot(
                root,
                loaded,
                "6529NM-PG-2026-001/proposal.json",
                "revision-1-proposal.json.snapshot",
                lambda snapshot: snapshot.__setitem__("proposal_id", "6529NM-PG-2026-999"),
            )
        )
        self.assertTrue(any("identity binding mismatch for proposal_id" in issue for issue in issues), issues)

        issues = self.copied_lineage_issues(
            lambda root, loaded: rewrite_snapshot(
                root,
                loaded,
                "register.json",
                "revision-1-register.json.snapshot",
                lambda snapshot: snapshot.__setitem__("register_id", "6529NM-OTHER-REGISTER"),
            )
        )
        self.assertTrue(any("identity binding mismatch for register_id" in issue for issue in issues), issues)

        issues = self.issues_after(lambda loaded: loaded[self.proposal_path].pop("proposal_id"))
        self.assertTrue(any("at least one non-empty domain identifier" in issue for issue in issues), issues)

    def test_revision_lineage_requires_timezone_aware_constructor_timestamps(self) -> None:
        def rewrite_snapshot_constructor(root: Path, loaded: dict[Path, object], remove: bool) -> None:
            snapshot_path = root / "records/proposed-gifts/6529NM-PG-2026-001/history/revision-1-proposal.json.snapshot"
            snapshot = json.loads(snapshot_path.read_text(encoding="utf-8"))
            constructor = snapshot["record_control"]["constructor"]
            if remove:
                constructor.pop("constructed_at")
            else:
                constructor["constructed_at"] = "2026-08-05T17:34:39.310"
            snapshot_path.write_bytes((json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
            normalized = snapshot_path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
            digest = "sha256:" + hashlib.sha256(normalized).hexdigest()
            current_path = (root / "records/proposed-gifts/6529NM-PG-2026-001/proposal.json").resolve()
            entry = loaded[current_path]["amendment_history"][0]
            entry["supersedes"] = digest
            entry["prior_payload_sha256"] = digest

        for remove in (False, True):
            issues = self.copied_lineage_issues(
                lambda root, loaded, remove=remove: rewrite_snapshot_constructor(root, loaded, remove)
            )
            self.assertTrue(
                any("prior snapshot constructor timestamp is missing or not timezone-aware" in issue for issue in issues),
                issues,
            )

        issues = self.issues_after(
            lambda loaded: loaded[self.proposal_path]["record_control"]["constructor"].__setitem__(
                "constructed_at", "2026-08-08T10:15:02.016715"
            )
        )
        self.assertTrue(any("current constructor timestamp is missing or not timezone-aware" in issue for issue in issues), issues)

    def test_control_time_accepts_seven_digit_aware_fractional_timestamp(self) -> None:
        parsed = _control_time("2026-08-08T10:15:02.0167151Z")
        self.assertIsNotNone(parsed)
        assert parsed is not None
        self.assertIsNotNone(parsed.utcoffset())

    def test_revision_lineage_snapshot_path_is_schema_optional_but_semantically_required(self) -> None:
        schema = json.loads(
            (REPO_ROOT / "schemas/proposed-gift-register.schema.json").read_text(encoding="utf-8")
        )
        amendment_schema = schema["$defs"]["amendmentHistory"]
        self.assertIn("prior_snapshot_path", amendment_schema["properties"])
        self.assertNotIn("prior_snapshot_path", amendment_schema["required"])
        issues = self.issues_after(
            lambda loaded: loaded[self.proposal_path]["amendment_history"][0].pop(
                "prior_snapshot_path"
            )
        )
        self.assertTrue(any("unsafe prior snapshot path" in issue for issue in issues), issues)

    def test_revision_lineage_rejects_snapshot_hash_drift(self) -> None:
        def mutate(root: Path, loaded: dict[Path, object]) -> None:
            snapshot = root / "records/proposed-gifts/6529NM-PG-2026-001/history/revision-1-proposal.json.snapshot"
            snapshot.write_bytes(snapshot.read_bytes().replace(b"Conflict at Its Edges", b"Conflict at Its Edgex", 1))

        issues = self.copied_lineage_issues(mutate)
        self.assertTrue(any("LF hash does not match both recorded hashes" in issue for issue in issues), issues)

    def test_revision_lineage_rejects_gaps_and_duplicates(self) -> None:
        def gap(loaded) -> None:
            record = loaded[self.proposal_path]
            record["record_control"]["revision"] = 3
            record["amendment_history"].append(copy.deepcopy(record["amendment_history"][0]))
            record["amendment_history"][1]["revision"] = 3

        issues = self.issues_after(gap)
        self.assertTrue(any("unique, increasing" in issue for issue in issues), issues)

        def duplicate(loaded) -> None:
            record = loaded[self.proposal_path]
            record["record_control"]["revision"] = 3
            record["amendment_history"].append(copy.deepcopy(record["amendment_history"][0]))

        issues = self.issues_after(duplicate)
        self.assertTrue(any("unique, increasing" in issue for issue in issues), issues)

    def test_revision_lineage_rejects_mismatched_prior_snapshot_revision(self) -> None:
        def mutate(root: Path, loaded: dict[Path, object]) -> None:
            snapshot = root / "records/proposed-gifts/6529NM-PG-2026-001/history/revision-1-proposal.json.snapshot"
            changed = snapshot.read_bytes().replace(b'"revision": 1', b'"revision": 2', 1)
            snapshot.write_bytes(changed)
            digest = "sha256:" + hashlib.sha256(changed.replace(b"\r\n", b"\n").replace(b"\r", b"\n")).hexdigest()
            proposal_path = (root / "records/proposed-gifts/6529NM-PG-2026-001/proposal.json").resolve()
            entry = loaded[proposal_path]["amendment_history"][0]
            entry["supersedes"] = digest
            entry["prior_payload_sha256"] = digest

        issues = self.copied_lineage_issues(mutate)
        self.assertTrue(any("snapshot revision does not match" in issue for issue in issues), issues)

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
