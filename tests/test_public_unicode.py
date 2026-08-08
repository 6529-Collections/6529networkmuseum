import unittest

from scripts.check_public_unicode import scan_public


class PublicUnicodeTest(unittest.TestCase):
    def test_public_corpus_is_strict_utf8_without_known_mojibake(self) -> None:
        self.assertEqual(scan_public(), [])


if __name__ == "__main__":
    unittest.main()
