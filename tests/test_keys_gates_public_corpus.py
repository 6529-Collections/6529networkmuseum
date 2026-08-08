from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PROGRAM_ID = "6529NM-AP-01"
STATUS = "constructed_visual_description_reviewed"
EXPECTED_ALTS = {
    f"{PROGRAM_ID}-OUT-002": (
        "An elevated view shows blurred buses and traffic around a sharply defined "
        "performer seated in a small white tub or boat on the roadway."
    ),
    f"{PROGRAM_ID}-OUT-011": (
        "A nude figure reclines on an ornate gold chair, wearing bright sandals and "
        "holding a small dark booklet or document; its text is not legible at the "
        "public derivative scale."
    ),
    f"{PROGRAM_ID}-OUT-016": (
        "A small white house with a red roof stands on a hill beneath a starry sky, "
        "beyond a lit gate with a warning sign and a person-like silhouette."
    ),
}


def load_json(relative_path: str) -> dict[str, object]:
    return json.loads((REPO_ROOT / relative_path).read_text(encoding="utf-8"))


class KeysAndGatesPublicCorpusTests(unittest.TestCase):
    def test_reviewed_accessibility_projection_has_exact_corrections(self) -> None:
        accessibility = load_json(f"media/programs/{PROGRAM_ID}/accessibility.json")
        self.assertEqual(STATUS, accessibility["status"])
        items = accessibility["items"]
        self.assertIsInstance(items, list)
        self.assertEqual(16, len(items))
        by_id = {item["record_id"]: item["alt_text"] for item in items}
        self.assertEqual(16, len(by_id))
        for record_id, alt_text in EXPECTED_ALTS.items():
            self.assertEqual(alt_text, by_id[record_id])

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
            self.assertEqual(3, len(presentation["derivatives"]))

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
