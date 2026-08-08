import unittest

from scripts.check_public_links import check_links


class PublicLinksTest(unittest.TestCase):
    def test_public_links_and_anchors_resolve(self) -> None:
        self.assertEqual(check_links(), [])


if __name__ == "__main__":
    unittest.main()
