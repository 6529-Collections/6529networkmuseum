"""Unit wrapper for the local WP-3 editorial/citation gate."""

from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path
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


class WP3EditorialChecks(unittest.TestCase):
    def test_public_copy_and_citations(self) -> None:
        self.assertEqual(MODULE.check_copy_citations(), [])

    def test_public_corpus_includes_scholarship_readme(self) -> None:
        files = MODULE.public_files()
        self.assertIn(MODULE.ROOT / "README.md", files)
        self.assertEqual(len(files), 22)

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
