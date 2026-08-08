import hashlib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


PUBLICATIONS = (
    {
        "serial": 1281404,
        "source": "notes/wip/2026-08-07-all-gifts-wave-vote-resolution.md",
        "receipt": "notes/wip/2026-08-07-all-gifts-wave-vote-publication.md",
        "utf16": 9_583,
        "utf8": 9_583,
        "sha256": "9883e18bd88331a3f98ad15a6279aaa0cc782aa366537bf13b8ad9e0b39ada76",
    },
    {
        "serial": 1282040,
        "source": "notes/wip/2026-08-08-integrated-gifts-and-acquisition-funding-policy.md",
        "receipt": "notes/wip/2026-08-08-integrated-gifts-and-acquisition-funding-publication.md",
        "utf16": 14_752,
        "utf8": 14_752,
        "sha256": "60eaebbbaebab62cbdc10beab31e8e9a8a2a20cf488d5a29dff174f272b1f57d",
    },
    {
        "serial": 1282091,
        "source": "notes/wip/2026-08-08-museum-gifts-acquisition-programs-and-funding-assets-policy.md",
        "receipt": "notes/wip/2026-08-08-museum-gifts-acquisition-programs-and-funding-assets-publication.md",
        "utf16": 16_289,
        "utf8": 16_289,
        "sha256": "ce4962072ddd0cbfacb7a071be51ae779c4cae40410851e6386e49ca405becb2",
    },
)


def published_content(path: Path) -> str:
    return path.read_text(encoding="utf-8").replace("\r\n", "\n").strip()


def utf16_code_units(text: str) -> int:
    return len(text.encode("utf-16-le")) // 2


class GovernancePublicationIntegrityTests(unittest.TestCase):
    def test_published_sources_match_their_receipts(self) -> None:
        for publication in PUBLICATIONS:
            with self.subTest(serial=publication["serial"]):
                content = published_content(ROOT / publication["source"])
                content_bytes = content.encode("utf-8")
                receipt = (ROOT / publication["receipt"]).read_text(encoding="utf-8")

                self.assertTrue(content.isascii())
                self.assertEqual(utf16_code_units(content), publication["utf16"])
                self.assertEqual(len(content_bytes), publication["utf8"])
                self.assertEqual(hashlib.sha256(content_bytes).hexdigest(), publication["sha256"])
                self.assertIn(f"UTF-16 code units: `{publication['utf16']:,}`", receipt)
                self.assertIn(f"UTF-8 bytes: `{publication['utf8']:,}`", receipt)
                self.assertIn(publication["sha256"], receipt)


if __name__ == "__main__":
    unittest.main()
