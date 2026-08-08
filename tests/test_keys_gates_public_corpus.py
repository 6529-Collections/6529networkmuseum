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
    record_id: [640] if record_id.endswith("OUT-011") else [640, 1280, 2400]
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
                "Selected through the Keys and Gates acquisition program; acquisition pending.",
                text,
            )
            self.assertIn("**Mint:** **Mint pending.**", text)
            self.assertNotIn("selected_unminted", text)
            aliases[alias] = work
        self.assertEqual({f"OUT-{i:03d}" for i in range(1, 17)}, set(aliases))


if __name__ == "__main__":
    unittest.main()
