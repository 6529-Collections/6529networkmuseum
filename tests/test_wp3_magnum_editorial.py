"""Unit wrapper for the local WP-3 editorial/citation gate."""

from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "scripts" / "magnum" / "check_copy_citations.py"
SPEC = importlib.util.spec_from_file_location("wp3_copy_citations", CHECKER)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
MEDIA_CHECKER = ROOT / "scripts" / "magnum" / "check_media_policy.py"
MEDIA_SPEC = importlib.util.spec_from_file_location("wp3_media_policy", MEDIA_CHECKER)
assert MEDIA_SPEC and MEDIA_SPEC.loader
MEDIA_MODULE = importlib.util.module_from_spec(MEDIA_SPEC)
MEDIA_SPEC.loader.exec_module(MEDIA_MODULE)
REFERENCE_CHECKER = ROOT / "scripts" / "magnum" / "check_local_references.py"
REFERENCE_SPEC = importlib.util.spec_from_file_location("wp3_local_references", REFERENCE_CHECKER)
assert REFERENCE_SPEC and REFERENCE_SPEC.loader
REFERENCE_MODULE = importlib.util.module_from_spec(REFERENCE_SPEC)
REFERENCE_SPEC.loader.exec_module(REFERENCE_MODULE)
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))
import generate_public_publication_bundle as BUNDLE_MODULE  # noqa: E402
import generate_public_publication_inventory as INVENTORY_MODULE  # noqa: E402


class WP3EditorialChecks(unittest.TestCase):
    def test_public_copy_and_citations(self) -> None:
        self.assertEqual(MODULE.check_copy_citations(), [])

    def test_public_corpus_includes_scholarship_readme(self) -> None:
        files = MODULE.public_files()
        self.assertIn(MODULE.ROOT / "README.md", files)
        self.assertEqual(len(files), 23)

    def test_visitor_manuscripts_expose_no_restricted_photo_locator(self) -> None:
        join = json.loads(MEDIA_MODULE.JOIN_PATH.read_text(encoding="utf-8"))
        self.assertEqual(MEDIA_MODULE.validate_visitor_markdown_media_affordances(join), [])
        direct_url = join["works"][0]["token_source_image_url"]
        errors = MEDIA_MODULE.validate_visitor_markdown_media_affordances(
            join,
            [("probe.md", f"[Open photograph]({direct_url})")],
        )
        self.assertEqual(len(errors), 1)
        self.assertIn("restricted direct photograph locator", errors[0])

    def test_visitor_corpus_excludes_proposed_gift_decision_history(self) -> None:
        historical_root = ROOT / "records" / "proposed-gifts" / "6529NM-PG-2026-001" / "public"
        self.assertTrue((historical_root / "wave-storm" / "01-resolution.md").is_file())
        self.assertTrue((historical_root / "voter-dossier.md").is_file())
        self.assertTrue((historical_root / "wave-resolution.md").is_file())

        paths = INVENTORY_MODULE.public_record_paths(ROOT)
        magnum_prefix = "records/proposed-gifts/6529NM-PG-2026-001/public/"
        scholarship_paths = [path for path in paths if path.startswith(magnum_prefix + "scholarship/")]
        self.assertTrue(scholarship_paths)
        self.assertFalse(any(INVENTORY_MODULE.PROPOSED_GIFT_DECISION_HISTORY.match(path) for path in paths))

        bundle = BUNDLE_MODULE.generate(ROOT)
        bundle_paths = [entry["path"] for entry in bundle["entries"]]
        self.assertTrue(set(scholarship_paths).issubset(bundle_paths))
        self.assertFalse(any(INVENTORY_MODULE.PROPOSED_GIFT_DECISION_HISTORY.match(path) for path in bundle_paths))
        for complete_manifest_only_path in (
            "records/proposed-gifts/6529NM-PG-2026-001/wave-publication-observation-2026-08-08.json",
            "records/proposed-gifts/6529NM-PG-2026-001/media-description-amendment-2026-08-08.json",
        ):
            self.assertNotIn(complete_manifest_only_path, bundle_paths)

        public_graph_content = "\n".join(
            entry["content"]
            for entry in bundle["entries"]
            if entry["path"].startswith(("records/entities/", "records/relations/"))
            or entry["path"].endswith("wave-status-observation-2026-08-08.json")
        )
        for raw_decision_path in (
            "records/proposed-gifts/6529NM-PG-2026-001/proposal.json",
            "records/proposed-gifts/6529NM-PG-2026-001/wave-storm.json",
            "records/proposed-gifts/6529NM-PG-2026-001/public/wave-storm/",
            "records/proposed-gifts/6529NM-PG-2026-001/wave-publication-observation-2026-08-08.json",
            "records/proposed-gifts/6529NM-PG-2026-001/media-description-amendment-2026-08-08.json",
        ):
            self.assertNotIn(raw_decision_path, public_graph_content)

        join = json.loads(MEDIA_MODULE.JOIN_PATH.read_text(encoding="utf-8"))
        bundle_markdown = "\n".join(
            entry["content"] for entry in bundle["entries"] if entry["path"].endswith(".md")
        )
        for work in join["works"]:
            self.assertNotIn(work["token_source_image_url"], bundle_markdown)
        self.assertNotIn("A young girl stands", bundle_markdown)
        self.assertNotIn("child stands", bundle_markdown.casefold())

    def test_visitor_manuscripts_link_only_inside_atomic_publication(self) -> None:
        files = sorted(path for path in REFERENCE_MODULE.ROOT.rglob("*.md"))
        errors: list[str] = []
        declared_paths = REFERENCE_MODULE.publication_paths()
        REFERENCE_MODULE.check_visitor_boundary(files, declared_paths, errors)
        self.assertEqual(errors, [])

    def test_visitor_boundary_rejects_arweave_and_complete_manifest_markers(self) -> None:
        declared = {"records/proposed-gifts/6529NM-PG-2026-001/public/scholarship/probe.md"}
        label = "records/proposed-gifts/6529NM-PG-2026-001/public/scholarship/probe.md"
        probes = (
            "https://arweave.net/example",
            "records/proposed-gifts/6529NM-PG-2026-001/wave-publication-observation-2026-08-08.json",
            "../machine/object-schedule.json",
        )
        for probe_text in probes:
            with self.subTest(probe=probe_text):
                errors: list[str] = []
                REFERENCE_MODULE.check_visitor_document(label, probe_text, declared, errors)
                self.assertTrue(errors, f"expected visitor-boundary rejection for {label}: {probe_text}")

    def test_media_policy_reports_malformed_shapes_without_crashing(self) -> None:
        join = json.loads(MEDIA_MODULE.JOIN_PATH.read_text(encoding="utf-8"))
        malformed = copy.deepcopy(join)
        malformed["runtime_policy"]["age_sensitive_subject_rule"] = None
        malformed["works"][3]["subject_display_rule"] = None
        self.assertTrue(MEDIA_MODULE.validate_join(malformed))

        missing_rows = copy.deepcopy(join)
        missing_rows["works"] = []
        self.assertTrue(MEDIA_MODULE.validate_join(missing_rows))


if __name__ == "__main__":
    unittest.main()
