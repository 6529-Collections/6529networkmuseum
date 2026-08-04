from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

from scripts.generate_institutional_source_inventory import build_inventory


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "records" / "institutional-practice"
INTRODUCTION = PACKAGE / "a-field-of-practice.md"
SOURCE_REGISTER = PACKAGE / "source-register.md"
STYLE_STANDARD = ROOT / "docs" / "curatorial-publication-standard.md"
STEWARDSHIP_STANDARD = ROOT / "docs" / "digital-art-stewardship-standard.md"
ADJACENT_STUDY = PACKAGE / "adjacent-chain-native-practice.md"
SOURCE_INVENTORY = ROOT / "docs" / "institutional-source-inventory.json"

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
    "acmi",
    "centro-multimedia",
    "dia",
    "hek-basel",
    "laboratorio-arte-alameda",
    "li-ma",
    "m-plus",
    "mca-chicago",
    "nam-june-paik-art-center",
    "ntt-icc",
    "transmediale",
    "v2",
    "walker-art-center",
)

MARKDOWN_LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
PUBLIC_LINK = re.compile(r"\[[^\]]+\]\((https?://[^)]+)\)")
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
    "acmi": ("Microgames", "Play It Again 2"),
    "centro-multimedia": ("Virtual Library", "Audiovisual Archive"),
    "dia": ("Spiral Jetty", "Aerial Documentation"),
    "hek-basel": ("minds of concern", "TraceNoizer"),
    "laboratorio-arte-alameda": ("Modos de", "Documentation Center"),
    "li-ma": ("ArtHost", "Artwork Documentation Tool"),
    "m-plus": ("M+ Collection", "Mediatheque"),
    "mca-chicago": ("Cinaedus Table", "I Was Raised on the Internet"),
    "nam-june-paik-art-center": ("Video Archive", "NJP Reader #13"),
    "ntt-icc": ("HIVE", "Restoring Media Art Works"),
    "transmediale": ("Unarchived", "Across and Beyond"),
    "v2": ("Capturing Unstable Media", "About the Archive"),
    "walker-art-center": ("Collecting Performance", "Interdisciplinary Initiative"),
}


class InstitutionalPracticePublicationTests(unittest.TestCase):
    def assert_https_external_links(self, text: str) -> None:
        external_links = [
            target for target in MARKDOWN_LINK.findall(text) if "://" in target
        ]
        self.assertTrue(
            all(target.startswith("https://") for target in external_links),
            f"non-HTTPS external links: {external_links}",
        )

    def test_profile_inventory_is_exact_and_complete(self) -> None:
        profile_directory = PACKAGE / "profiles"
        actual = tuple(sorted(path.stem for path in profile_directory.glob("*.md")))
        self.assertEqual(tuple(sorted(PROFILE_SLUGS)), actual)

    def test_introduction_routes_every_profile(self) -> None:
        text = INTRODUCTION.read_text(encoding="utf-8")
        for slug in PROFILE_SLUGS:
            self.assertIn(f"(profiles/{slug}.md)", text)
        self.assertIn("(source-register.md)", text)
        self.assertIn("../../docs/institutional-source-inventory.json", text)
        self.assertIn("(adjacent-chain-native-practice.md)", text)
        self.assertIn("../../docs/curatorial-publication-standard.md", text)
        self.assertIn("../../docs/digital-art-stewardship-standard.md", text)

    def test_profiles_carry_publication_control_and_analysis(self) -> None:
        required_metadata = (
            "- **Series:** A field of practice",
            "- **Status:** public scholarship",
            "- **Institutional author:** 6529 Network Museum",
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
                self.assertRegex(text, r"- \*\*Publication date:\*\* \d{4}-\d{2}-\d{2}")
                self.assertRegex(text, r"- \*\*Version:\*\* \d+\.\d+\.\d+")
                self.assert_https_external_links(text)
                self.assertGreaterEqual(len(PUBLIC_LINK.findall(text)), 3)
                body = text.split("## Sources", maxsplit=1)[0]
                self.assertGreaterEqual(
                    len(PUBLIC_LINK.findall(body)),
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
        self.assert_https_external_links(text)
        links = PUBLIC_LINK.findall(text)
        self.assertEqual(len(links), len(set(links)))
        self.assertEqual(114, len(links))
        self.assertTrue(
            all(link.startswith("https://") for link in links),
            "the public source register must not contain plaintext HTTP links",
        )
        self.assertNotIn("google.com/search", text)
        self.assertNotIn("bing.com/search", text)
        self.assertNotIn("https://cdn.rhizome.org/about/", text)
        self.assertIn("- **Access date for all web sources:** 2026-08-04", text)

    def test_source_inventory_is_deterministic_and_complete(self) -> None:
        committed = json.loads(SOURCE_INVENTORY.read_text(encoding="utf-8"))
        self.assertEqual(build_inventory(), committed)
        self.assertEqual(len(committed["sources"]), committed["source_count"])
        self.assertTrue(
            all(source["url"].startswith("https://") for source in committed["sources"])
        )
        self.assertTrue(all(source["cited_by"] for source in committed["sources"]))
        self.assertTrue(all(source["labels"] for source in committed["sources"]))

    def test_every_publication_source_is_reconciled_to_the_inventory(self) -> None:
        inventory_links = {
            source["url"]
            for source in json.loads(SOURCE_INVENTORY.read_text(encoding="utf-8"))[
                "sources"
            ]
        }
        publication_files = (INTRODUCTION, ADJACENT_STUDY, STEWARDSHIP_STANDARD) + tuple(
            PACKAGE / "profiles" / f"{slug}.md" for slug in PROFILE_SLUGS
        )
        for publication_file in publication_files:
            with self.subTest(publication=publication_file.name):
                text = publication_file.read_text(encoding="utf-8")
                self.assert_https_external_links(text)
                publication_links = set(PUBLIC_LINK.findall(text))
                self.assertFalse(
                    publication_links - inventory_links,
                    "uninventoried publication sources: "
                    f"{sorted(publication_links - inventory_links)}",
                )

    def test_style_standard_binds_comparative_study(self) -> None:
        text = STYLE_STANDARD.read_text(encoding="utf-8")
        self.assertIn("../records/institutional-practice/a-field-of-practice.md", text)
        self.assertIn("../records/institutional-practice/source-register.md", text)
        self.assertIn("### 12.7 Write technical scholarship from a case", text)
        self.assertIn("### 12.9 Edit for the audible sentence", text)
        self.assertIn("institutional-source-inventory.json", text)
        stewardship = STEWARDSHIP_STANDARD.read_text(encoding="utf-8")
        self.assertIn("## 2. Record architecture", stewardship)
        self.assertIn("## 9. Primary source basis", stewardship)


if __name__ == "__main__":
    unittest.main()
