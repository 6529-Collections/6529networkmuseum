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

from proposed_gifts import compose_voter_dossier, proposed_gift_issues  # noqa: E402


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

    def test_voter_dossier_is_exact_storm_projection(self) -> None:
        package = self.loaded[self.package_path]
        candidate_dir = self.proposal_path.parent
        expected = compose_voter_dossier(candidate_dir, package)
        dossier = candidate_dir / "public/voter-dossier.md"
        self.assertEqual(dossier.read_text(encoding="utf-8"), expected)

    def test_rejects_image_that_does_not_join_to_object(self) -> None:
        issues = self.issues_after(
            lambda loaded: loaded[self.package_path]["parts"][1]["media"][0].update(
                {"uri": "https://arweave.net/not-the-scheduled-image"}
            )
        )
        self.assertTrue(any("work image does not match" in issue for issue in issues))

    def test_rejects_missing_or_duplicate_work_part(self) -> None:
        def mutate(loaded) -> None:
            loaded[self.package_path]["parts"][2]["candidate_object_id"] = loaded[self.package_path]["parts"][1][
                "candidate_object_id"
            ]

        issues = self.issues_after(mutate)
        self.assertTrue(any("match the object schedule exactly and in order" in issue for issue in issues))

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
        self.assertTrue(any("match the object schedule exactly and in order" in issue for issue in issues))

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
                    "future\ngifts from Magnum Photos 75", "later\ngifts from Magnum Photos 75"
                ),
                encoding="utf-8",
            )
            loaded = {
                path.resolve(): json.loads(path.read_text(encoding="utf-8"))
                for path in (root / "records/proposed-gifts").rglob("*.json")
            }
            issues = proposed_gift_issues(root, loaded)
        self.assertTrue(any("opening and closing Resolution sections differ" in issue for issue in issues))

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
