from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PROGRAM_ID = "6529NM-AP-01"
STATUS = "constructed_visual_description_pending_independent_review"
EXPECTED_ALTS = {
    f"{PROGRAM_ID}-OUT-001": (
        "A lone figure stands before a tall blue patterned gate as sunlight casts long "
        "geometric shadows across a stone hall."
    ),
    f"{PROGRAM_ID}-OUT-002": (
        "An elevated view shows blurred buses and traffic around a sharply defined "
        "performer seated in a small white tub or boat on the roadway."
    ),
    f"{PROGRAM_ID}-OUT-003": (
        "A rider on a rearing white horse rises above a herd of brown horses on a wide "
        "plain beneath hazy mountains."
    ),
    f"{PROGRAM_ID}-OUT-004": "Two silhouetted figures walk toward daylight at the end of a rough stone passage.",
    f"{PROGRAM_ID}-OUT-005": (
        "A long weathered concrete barrier with faded graffiti divides a pale sky from a dark foreground."
    ),
    f"{PROGRAM_ID}-OUT-006": "A shirtless man opens a refrigerator covered in colorful magnets in a domestic kitchen.",
    f"{PROGRAM_ID}-OUT-007": (
        "A turquoise mountain lake is bordered by evergreen forest and a jagged, snow-dusted mountain range."
    ),
    f"{PROGRAM_ID}-OUT-008": (
        "A vertical aerial view shows dense residential roofs meeting an ordered palm plantation along a sharp boundary."
    ),
    f"{PROGRAM_ID}-OUT-009": (
        "Black-and-white industrial buildings sit beneath a cloudy sky, with the words NOW IS OUR TIME painted on a wall."
    ),
    f"{PROGRAM_ID}-OUT-010": "A bare torso emerges from folds of black fabric against a nearly black background.",
    f"{PROGRAM_ID}-OUT-011": (
        "A nude figure reclines on an ornate gold chair, wearing bright sandals and "
        "holding a small dark booklet or document; its text is not legible at the "
        "public derivative scale."
    ),
    f"{PROGRAM_ID}-OUT-012": "A person stands framed by successive arched doorways inside a heavily damaged building.",
    f"{PROGRAM_ID}-OUT-013": (
        "Black keyboard keys spell NO / WHERE / TO on a white surface, while the Esc "
        "key sits apart below beside a small ant."
    ),
    f"{PROGRAM_ID}-OUT-014": (
        "The camera looks upward through a dark, fluted circular structure toward a small opening of sky."
    ),
    f"{PROGRAM_ID}-OUT-015": (
        "Two people lean from the windows of a weathered teal train; one wears a bright orange head covering."
    ),
    f"{PROGRAM_ID}-OUT-016": (
        "A small white house with a red roof stands on a hill beneath a starry sky, "
        "beyond a lit gate with a warning sign and a person-like silhouette."
    ),
}
EXPECTED_WIDTHS = {
    record_id: [640] if record_id.endswith(("OUT-004", "OUT-011")) else [640, 1280, 2400]
    for record_id in EXPECTED_ALTS
}


def load_json(relative_path: str) -> dict[str, object]:
    return json.loads((REPO_ROOT / relative_path).read_text(encoding="utf-8"))


class KeysAndGatesPublicCorpusTests(unittest.TestCase):
    def test_accessibility_projection_is_pending_and_has_exact_all_16_text(self) -> None:
        accessibility = load_json(f"media/programs/{PROGRAM_ID}/accessibility.json")
        self.assertEqual(STATUS, accessibility["status"])
        items = accessibility["items"]
        self.assertIsInstance(items, list)
        self.assertEqual(16, len(items))
        by_id = {item["record_id"]: item["alt_text"] for item in items}
        self.assertEqual(16, len(by_id))
        self.assertEqual(EXPECTED_ALTS, by_id)
        self.assertIsNone(accessibility["record_control"]["review"])
        self.assertEqual("constructed", accessibility["record_control"]["record_status"])
        self.assertEqual(
            EXPECTED_WIDTHS,
            {item["record_id"]: item["public_widths"] for item in items},
        )

        amendment = (REPO_ROOT / "records/programs/6529NM-AP-01/public/accessibility-amendment.md").read_text(
            encoding="utf-8"
        )
        self.assertIn(
            "sha256:48337baf91adb7d50beb43c65275e33d1c04f22a8ced32416683c663ba42c96e",
            amendment,
        )
        self.assertIn(
            "sha256:7f18d61c2ff6ae547c1e80384334ddc8966fae803cbee67346da3c5e6f29d7f2",
            amendment,
        )

    def test_accessibility_text_projects_exactly_to_work_pages_and_media_joins(self) -> None:
        work_dir = REPO_ROOT / "records/programs/6529NM-AP-01/public/works"
        works_by_alias = {}
        alias_pattern = re.compile(r"\*\*Source alias:\*\* (OUT-\d{3})")
        image_pattern = re.compile(r"!\[([^\]]+)\]\([^\n]+\)")
        for work in work_dir.glob("*.md"):
            text = work.read_text(encoding="utf-8")
            alias_match = alias_pattern.search(text)
            image_match = image_pattern.search(text)
            self.assertIsNotNone(alias_match, work)
            self.assertIsNotNone(image_match, work)
            works_by_alias[alias_match.group(1)] = (work, image_match.group(1))
        self.assertEqual({f"OUT-{index:03d}" for index in range(1, 17)}, set(works_by_alias))

        media_text = (REPO_ROOT / "records/programs/6529NM-AP-01/public/media-joins.md").read_text(
            encoding="utf-8"
        )
        media_rows = {
            match.group(1): match.group(2).strip()
            for match in re.finditer(r"<a id=\"out-(\d{3})\"></a>OUT-\1 .*? \| ([^|]+) \| 640", media_text)
        }
        self.assertEqual({f"{index:03d}" for index in range(1, 17)}, set(media_rows))
        for record_id, alt_text in EXPECTED_ALTS.items():
            alias = record_id.rsplit("-", 1)[1]
            self.assertEqual(alt_text, works_by_alias[f"OUT-{alias}"][1])
            self.assertEqual(alt_text, media_rows[alias])

    def test_typed_manifest_matches_accessibility_and_is_one_to_one(self) -> None:
        accessibility = load_json(f"media/programs/{PROGRAM_ID}/accessibility.json")
        manifest = load_json(f"records/programs/{PROGRAM_ID}/media-manifest.json")
        accessibility_by_id = {
            item["record_id"]: item["alt_text"] for item in accessibility["items"]
        }
        manifest_items = manifest["items"]
        self.assertEqual(16, len(manifest_items))
        manifest_ids = [item["record_id"] for item in manifest_items]
        self.assertEqual(16, len(set(manifest_ids)))
        self.assertEqual(set(accessibility_by_id), set(manifest_ids))
        for item in manifest_items:
            presentation = item["presentation"]
            self.assertEqual(STATUS, presentation["alt_text_status"])
            self.assertEqual(accessibility_by_id[item["record_id"]], presentation["alt_text"])
            expected_widths = EXPECTED_WIDTHS[item["record_id"]]
            self.assertEqual(expected_widths, presentation["public_widths"])
            self.assertEqual(expected_widths, [entry["width"] for entry in presentation["derivatives"]])

        out_011 = next(item for item in manifest_items if item["record_id"].endswith("OUT-011"))
        self.assertEqual([640], out_011["presentation"]["public_widths"])
        self.assertEqual([640], [entry["width"] for entry in out_011["presentation"]["derivatives"]])
        self.assertNotIn("/1280.webp", json.dumps(out_011))
        self.assertNotIn("/2400.webp", json.dumps(out_011))

        out_004 = next(item for item in manifest_items if item["record_id"].endswith("OUT-004"))
        self.assertEqual([640], out_004["presentation"]["public_widths"])
        self.assertEqual([640], [entry["width"] for entry in out_004["presentation"]["derivatives"]])
        self.assertNotIn("/1280.webp", json.dumps(out_004))
        self.assertNotIn("/2400.webp", json.dumps(out_004))

    def test_wave_source_link_uses_canonical_program_uuid(self) -> None:
        program_note = (REPO_ROOT / "docs/programs/keys-and-gates.md").read_text(encoding="utf-8")
        self.assertIn(
            "https://6529.io/waves/4ff022b3-aa17-4a0a-ba78-58f64ff1d427?drop=dc75fe32-f3c2-49db-9069-d9975b5964f3",
            program_note,
        )
        self.assertNotIn("https://6529.io/waves/4ff0223b-", program_note)

    def test_current_accessibility_amendment_is_append_only_and_pending(self) -> None:
        amendment = (
            REPO_ROOT / "records/programs/6529NM-AP-01/public/accessibility-amendment-2026-08-08-003.md"
        ).read_text(encoding="utf-8")
        self.assertIn("6529NM-AP-01-MEDIA-ACCESSIBILITY-2026-08-08-003", amendment)
        self.assertIn("constructor-only status was not independent review", amendment)
        self.assertIn("OUT-008", amendment)
        self.assertIn("OUT-011", amendment)
        self.assertIn("constructed_visual_description_pending_independent_review", amendment)

    def test_out_011_withdrawal_has_exact_readback_and_stays_out_of_visitor_routes(self) -> None:
        amendment = (
            REPO_ROOT / "records/programs/6529NM-AP-01/public/accessibility-amendment-2026-08-08-004.md"
        ).read_text(encoding="utf-8")
        for required in (
            "6529NM-AP-01-MEDIA-ACCESSIBILITY-2026-08-08-004",
            "I8YFV5J3W4GCFQCZNXU39X6VYQ",
            "2026-08-08T12:49:27Z",
            "HTTP 200; 15,306 bytes",
            "HTTP 404",
            "sha256:00f3ff73be1cfff57a5ddf3ae9890cd9a49e1de547c5883cd1ac405bcda6f985",
            "sha256:c704956b390385b6c8f2c9158455292618b8237aa3355ff6b0a2615b3f62c251",
            "ECGWRHUV1NM3I",
            "6529bucket",
        ):
            self.assertIn(required, amendment)
        self.assertEqual(2, amendment.count("HTTP 404"))

        manifest = load_json(f"records/programs/{PROGRAM_ID}/media-manifest.json")
        out_011 = next(item for item in manifest["items"] if item["record_id"].endswith("OUT-011"))
        derivative = out_011["presentation"]["derivatives"]
        self.assertEqual(
            [
                {
                    "width": 640,
                    "sha256": "sha256:14eea8754ea08d39dd5fe39d93f2f69dbce8e18e9f550a10f7e76bc6ec3fc784",
                    "byte_size": 15306,
                }
            ],
            [
                {
                    "width": entry["width"],
                    "sha256": entry["sha256"],
                    "byte_size": entry["byte_size"],
                }
                for entry in derivative
            ],
        )

        visitor_paths = [
            REPO_ROOT / "records/programs/6529NM-AP-01/public/README.md",
            REPO_ROOT / "records/programs/6529NM-AP-01/public/curated-acquisition.md",
            REPO_ROOT / "records/programs/6529NM-AP-01/public/curatorial-essay.md",
            *sorted((REPO_ROOT / "records/programs/6529NM-AP-01/public/works").glob("*.md")),
            *sorted((REPO_ROOT / "records/programs/6529NM-AP-01/public/artists").glob("*.md")),
        ]
        visitor_text = "\n".join(path.read_text(encoding="utf-8") for path in visitor_paths)
        for internal_value in ("ECGWRHUV1NM3I", "6529bucket", "I8YFV5J3W4GCFQCZNXU39X6VYQ"):
            self.assertNotIn(internal_value, visitor_text)

        source_url = out_011["source"]["url"]
        self.assertNotIn(source_url, visitor_text)
        self.assertIn("source hash, fixed transform, width allowlist", amendment)

    def test_out_004_withdrawal_has_exact_readback_and_lineage(self) -> None:
        amendment = (
            REPO_ROOT / "records/programs/6529NM-AP-01/public/accessibility-amendment-2026-08-08-006.md"
        ).read_text(encoding="utf-8")
        for required in (
            "6529NM-AP-01-MEDIA-ACCESSIBILITY-2026-08-08-006",
            "IBOR4WFJPZAPTU36ZXYOFBWLGK",
            "2026-08-08T13:03:13Z",
            "HTTP 200; 45,202 bytes",
            "sha256:18bb9cadc9c91a36518da2d5650cfaa3a9c398bebb4a283275a1b538bce48ad1",
            "sha256:73c4e5dbf469c3c2757ac2368409974e6b6b2c7a508b0ec4db9425252666108c",
            "HTTP 404",
            "sha256:8e0915b020965a6090c868ba29397c03ee8322d84ebca32fe3714f0537d96987",
        ):
            self.assertIn(required, amendment)
        self.assertEqual(2, amendment.count("HTTP 404"))

        manifest = load_json(f"records/programs/{PROGRAM_ID}/media-manifest.json")
        out_004 = next(item for item in manifest["items"] if item["record_id"].endswith("OUT-004"))
        self.assertEqual([640], out_004["presentation"]["public_widths"])
        self.assertEqual(
            [{"width": 640, "sha256": "sha256:8e0915b020965a6090c868ba29397c03ee8322d84ebca32fe3714f0537d96987", "byte_size": 45202}],
            [
                {"width": entry["width"], "sha256": entry["sha256"], "byte_size": entry["byte_size"]}
                for entry in out_004["presentation"]["derivatives"]
            ],
        )

    def test_limited_editorial_display_authority_covers_all_16(self) -> None:
        amendment = (
            REPO_ROOT / "records/programs/6529NM-AP-01/public/publication-authority-amendment-2026-08-08-005.md"
        ).read_text(encoding="utf-8")
        self.assertIn("PROVISIONAL_EDITORIAL_DISPLAY_LIMITED", amendment)
        self.assertIn("No consent instrument", amendment)
        self.assertIn("private source", amendment)
        self.assertIn("does **not** activate CC0", amendment)
        self.assertEqual(16, amendment.count("| `PROVISIONAL_EDITORIAL_DISPLAY_LIMITED` |"))
        for alias in (f"OUT-{index:03d}" for index in range(1, 17)):
            self.assertIn(f"| {alias} |", amendment)

    def test_selected_outcomes_public_work_pages_and_media_are_one_to_one(self) -> None:
        selected = load_json(f"records/programs/{PROGRAM_ID}/selected-works.json")
        selected_ids = {item["record_id"] for item in selected["works"]}
        manifest = load_json(f"records/programs/{PROGRAM_ID}/media-manifest.json")
        manifest_ids = {item["record_id"] for item in manifest["items"]}
        self.assertEqual(16, len(selected_ids))
        self.assertEqual(selected_ids, manifest_ids)

        alias_pattern = re.compile(r"\*\*Source alias:\*\* (OUT-\d{3})")
        media_pattern = re.compile(r"/6529NM-AP-01-OUT-(\d{3})/")
        works = sorted((REPO_ROOT / "records/programs/6529NM-AP-01/public/works").glob("*.md"))
        self.assertEqual(16, len(works))
        aliases: dict[str, Path] = {}
        for work in works:
            text = work.read_text(encoding="utf-8")
            alias_match = alias_pattern.search(text)
            media_match = media_pattern.search(text)
            self.assertIsNotNone(alias_match, work)
            self.assertIsNotNone(media_match, work)
            alias = alias_match.group(1)
            self.assertNotIn(alias, aliases)
            self.assertEqual(alias, f"OUT-{media_match.group(1)}")
            self.assertIn(
                "**Status:** **Selected; not yet minted or accessioned; not in the permanent Collection.**",
                text,
            )
            self.assertNotIn("**Program state:**", text)
            self.assertNotIn("**Mint:**", text)
            self.assertNotIn("selected_unminted", text)
            aliases[alias] = work
        self.assertEqual({f"OUT-{i:03d}" for i in range(1, 17)}, set(aliases))

    def test_public_artist_and_work_navigation_is_bidirectional_and_direct(self) -> None:
        public_root = REPO_ROOT / "records/programs/6529NM-AP-01/public"
        acquisition = (public_root / "curated-acquisition.md").read_text(encoding="utf-8")
        essay_link = "(curatorial-essay.md)"
        self.assertIn(essay_link, acquisition)
        works = sorted((public_root / "works").glob("*.md"))
        artists = sorted((public_root / "artists").glob("*.md"))
        self.assertEqual(16, len(works))
        self.assertEqual(15, len(artists))
        for work in works:
            text = work.read_text(encoding="utf-8")
            self.assertIn("../curated-acquisition.md", text, work)
            self.assertIn("../curatorial-essay.md", text, work)
            artist_links = re.findall(r"\]\(\.\./artists/([^\)]+)\.md\)", text)
            self.assertTrue(artist_links, work)
            for artist_slug in set(artist_links):
                artist_path = public_root / "artists" / f"{artist_slug}.md"
                self.assertTrue(artist_path.exists(), artist_path)
                self.assertIn(f"../works/{work.name}", artist_path.read_text(encoding="utf-8"), artist_path)
        for artist in artists:
            text = artist.read_text(encoding="utf-8")
            self.assertIn("../curated-acquisition.md", text, artist)
            self.assertIn("../curatorial-essay.md", text, artist)
            self.assertRegex(text, r"\]\(\.\./works/[^\)]+\.md\)", artist)

    def test_visitor_copy_has_no_exhibition_or_formulaic_scaffolding_terms(self) -> None:
        public_root = REPO_ROOT / "records/programs/6529NM-AP-01/public"
        visitor_paths = [
            public_root / "curated-acquisition.md",
            public_root / "curatorial-essay.md",
            *sorted((public_root / "artists").glob("*.md")),
            *sorted((public_root / "works").glob("*.md")),
        ]
        visitor_text = "\n".join(path.read_text(encoding="utf-8") for path in visitor_paths).lower()
        for forbidden in ("exhibition", "neither", "rather than", "without", "schema", "manifest", "deployment"):
            self.assertNotIn(forbidden, visitor_text, forbidden)

    def test_work_pages_project_only_declared_presentation_urls(self) -> None:
        public_root = REPO_ROOT / "records/programs/6529NM-AP-01/public"
        manifest = load_json(f"records/programs/{PROGRAM_ID}/media-manifest.json")
        work_text = "\n".join(path.read_text(encoding="utf-8") for path in (public_root / "works").glob("*.md"))
        visitor_text = "\n".join(
            path.read_text(encoding="utf-8")
            for path in (
                public_root / "README.md",
                public_root / "curated-acquisition.md",
                public_root / "curatorial-essay.md",
                *(public_root / "artists").glob("*.md"),
            )
        )
        for item in manifest["items"]:
            presentation = item["presentation"]
            self.assertIn(presentation["derivatives"][0]["url"], work_text, item["record_id"])
            source_url = item["source"]["url"]
            self.assertNotIn(source_url, work_text, item["record_id"])
            self.assertNotIn(source_url, visitor_text, item["record_id"])


if __name__ == "__main__":
    unittest.main()
