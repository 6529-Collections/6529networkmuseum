from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "records" / "institutional-practice"
INTRODUCTION = PACKAGE / "a-field-of-practice.md"
SOURCE_REGISTER = PACKAGE / "source-register.md"
STYLE_STANDARD = ROOT / "docs" / "curatorial-publication-standard.md"

PROFILE_SLUGS = (
    "met",
    "getty",
    "moma",
    "whitney",
    "tate",
    "centre-pompidou",
    "sfmoma",
    "guggenheim",
    "zkm",
    "ars-electronica",
    "rhizome-new-museum",
    "serpentine-arts-technologies",
    "v-and-a",
    "lacma",
)

HTTPS_LINK = re.compile(r"\[[^\]]+\]\((https://[^)]+)\)")
FORBIDDEN_EDITORIAL_PHRASES = (
    "strongest examples",
    "best catalogues",
    "most instructive achievement",
    "most implementation-ready",
    "most valuable lesson",
    "the analogy is exact",
    "the right conceptual foundation",
    "borrow the prestige",
)

REQUIRED_CASES = {
    "met": ("Everything #4", "Salvator Mundi"),
    "getty": ("Museum Catalogues in the Digital Age", "Linked Art"),
    "moma": ("Unsupervised", "exhibition history"),
    "whitney": ("The World's First Collaborative Sentence", "Media Preservation Initiative"),
    "tate": ("Net Art Commissions", "Reshaping the Collectible"),
    "centre-pompidou": ("Sans titre", "Zapping Zone"),
    "sfmoma": ("Learning to Love You More", "Matters in Media Art"),
    "guggenheim": ("Brandon", "net.flag"),
    "zkm": ("Wipe Cycle", "Laboratory for Antiquated Video Systems"),
    "ars-electronica": ("Spaxels", "Ars Electronica Archive"),
    "rhizome-new-museum": ("My Boyfriend Came Back From the War", "Net Art Anthology"),
    "serpentine-arts-technologies": ("I DIDNT REALISE YOU THOUGHT LIKE THAT", "Future Art Ecosystems"),
    "v-and-a": ("Shaping Form", "collections online"),
    "lacma": ("METAVASARELY", "Examining the Life and Times of Media Art"),
}


class InstitutionalPracticePublicationTests(unittest.TestCase):
    def test_profile_inventory_is_exact_and_complete(self) -> None:
        profile_directory = PACKAGE / "profiles"
        actual = tuple(sorted(path.stem for path in profile_directory.glob("*.md")))
        self.assertEqual(tuple(sorted(PROFILE_SLUGS)), actual)

    def test_introduction_routes_every_profile(self) -> None:
        text = INTRODUCTION.read_text(encoding="utf-8")
        for slug in PROFILE_SLUGS:
            self.assertIn(f"(profiles/{slug}.md)", text)
        self.assertIn("(source-register.md)", text)
        self.assertIn("../../docs/curatorial-publication-standard.md", text)

    def test_profiles_carry_publication_control_and_analysis(self) -> None:
        required_metadata = (
            "- **Series:** A field of practice",
            "- **Status:** public scholarship",
            "- **Institutional author:** 6529 Network Museum",
            "- **Publication date:** 2026-08-04",
            "- **Research cutoff:** 2026-08-04",
            "- **Research apparatus:** [primary-source register](../source-register.md)",
        )
        required_sections = (
            "## What the Museum should adopt",
            "## Where the analogy ends",
            "## Sources",
            "## Revision history",
        )
        for slug in PROFILE_SLUGS:
            with self.subTest(profile=slug):
                text = (PACKAGE / "profiles" / f"{slug}.md").read_text(encoding="utf-8")
                for marker in (*required_metadata, *required_sections):
                    self.assertIn(marker, text)
                self.assertRegex(text, r"- \*\*Version:\*\* \d+\.\d+\.\d+")
                self.assertGreaterEqual(len(HTTPS_LINK.findall(text)), 3)
                body = text.split("## Sources", maxsplit=1)[0]
                self.assertGreaterEqual(
                    len(HTTPS_LINK.findall(body)),
                    2,
                    "factual analysis must carry claim-level links before the bibliography",
                )
                for case in REQUIRED_CASES[slug]:
                    self.assertIn(case, text)
                lowered = text.lower()
                for phrase in FORBIDDEN_EDITORIAL_PHRASES:
                    self.assertNotIn(phrase, lowered)

    def test_source_register_uses_primary_https_links(self) -> None:
        text = SOURCE_REGISTER.read_text(encoding="utf-8")
        links = HTTPS_LINK.findall(text)
        self.assertGreaterEqual(len(links), 50)
        self.assertNotIn("google.com/search", text)
        self.assertNotIn("bing.com/search", text)
        self.assertNotIn("https://cdn.rhizome.org/about/", text)
        self.assertIn("- **Access date for all web sources:** 2026-08-04", text)

    def test_every_profile_source_is_reconciled_to_the_register(self) -> None:
        register_links = set(HTTPS_LINK.findall(SOURCE_REGISTER.read_text(encoding="utf-8")))
        for slug in PROFILE_SLUGS:
            with self.subTest(profile=slug):
                text = (PACKAGE / "profiles" / f"{slug}.md").read_text(encoding="utf-8")
                profile_links = set(HTTPS_LINK.findall(text))
                self.assertFalse(
                    profile_links - register_links,
                    f"unregistered profile sources: {sorted(profile_links - register_links)}",
                )

    def test_style_standard_binds_comparative_study(self) -> None:
        text = STYLE_STANDARD.read_text(encoding="utf-8")
        self.assertIn("../records/institutional-practice/a-field-of-practice.md", text)
        self.assertIn("../records/institutional-practice/source-register.md", text)
        self.assertIn("### 12.7 Write technical scholarship from a case", text)
        self.assertIn("### 12.9 Edit for the audible sentence", text)


if __name__ == "__main__":
    unittest.main()
