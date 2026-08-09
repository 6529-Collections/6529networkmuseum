import tempfile
import unittest
from pathlib import Path

from scripts.check_public_links import check_links


class PublicLinksTest(unittest.TestCase):
    def test_public_links_and_anchors_resolve(self) -> None:
        self.assertEqual(check_links(), [])

    def test_fenced_code_links_are_not_treated_as_document_links(self) -> None:
        with tempfile.TemporaryDirectory(
            dir=Path(__file__).resolve().parents[1] / "tests"
        ) as raw_root:
            root = Path(raw_root)
            (root / "example.md").write_text(
                "```markdown\n[example](missing-from-the-document.md)\n```\n",
                encoding="utf-8",
            )
            self.assertEqual(check_links(root), [])


if __name__ == "__main__":
    unittest.main()
