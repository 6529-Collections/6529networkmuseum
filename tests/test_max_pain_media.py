from __future__ import annotations

from contextlib import ExitStack
import copy
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

from jsonschema import Draft202012Validator, FormatChecker
from PIL import Image


TESTS_DIR = Path(__file__).resolve().parent
REPO_ROOT = TESTS_DIR.parent
sys.path.append(str(REPO_ROOT / "scripts"))

import generate_max_pain_media as media  # noqa: E402
import generate_program_media as transform  # noqa: E402
from gif_structure import parse_gif  # noqa: E402


SCHEMA = json.loads((REPO_ROOT / "schemas" / "accession-media-presentation-v3.schema.json").read_text(encoding="utf-8"))
COMMITTED_POSTERS = {
    640: "sha256:bfb1ae06ecc52f5c338b967b8eeefb0d7555361a56953bfe80bfe90fba32d0d3",
    1280: "sha256:b50c4375fd42103664cb4a7dd57a4d416a5ac87f0f6df3edcb520690b0f2b426",
    2400: "sha256:feee964c4e20584fb5c18583ae9e6d292356e6575239b316d0f23600c0719598",
}


def schema_errors(value: dict[str, object]) -> list[str]:
    validator = Draft202012Validator(SCHEMA, format_checker=FormatChecker())
    return [error.message for error in validator.iter_errors(value)]


class MaxPainMediaFixtureTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="museum-max-pain-media-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        evidence = self.root / "evidence" / "sources"
        self.source_path = evidence / "raw" / "token-image.gif"
        self.source_summary = evidence / "summary.json"
        self.source_manifest = evidence / "manifest.json"
        self.manifest_path = self.root / "records" / "accessions" / media.ACCESSION_ID / "public" / "presentation-manifest.json"
        self.media_root = self.root / "media" / "accessions" / media.ACCESSION_ID
        self.work_id = "6529NM-W-9999"
        self.media_id = "6529NM-MED-9998"
        self.animation_id = "6529NM-MED-9999"
        self.source_path.parent.mkdir(parents=True)
        frames = []
        for index in range(3):
            frame = Image.new("P", (2400, 2400), 0)
            frame.putpalette([0, 0, 0, 0, 153, 153, 255, 0, 153, 255, 0, 255] + [0] * (256 * 3 - 12))
            frame.paste(1, (300, 300, 2100, 2100))
            frame.paste(2 + index % 2, (900, 900 + 100 * index, 1500, 1500))
            frames.append(frame)
        frames[0].save(self.source_path, format="GIF", save_all=True, append_images=frames[1:], duration=50, loop=0, disposal=1)
        payload = self.source_path.read_bytes()
        structure = parse_gif(payload)
        self.source_sha = hashlib.sha256(payload).hexdigest()
        self.source_manifest.write_text(
            json.dumps(
                {
                    "entries": [
                        {
                            "source_id": media.SOURCE_ID,
                            "path": media.SOURCE_ENTRY_PATH,
                            "media_type": "image/gif",
                            "sha256": self.source_sha,
                            "size": len(payload),
                            "url": "https://media.example.test/MAX_PAIN.gif",
                            "ipfs_cid": media.IMAGE_CID,
                        }
                    ]
                }
            ),
            encoding="utf-8",
        )
        self.source_summary.write_text(
            json.dumps(
                {
                    "accession_id": media.ACCESSION_ID,
                    "media": {
                        "sha256": f"sha256:{self.source_sha}",
                        "size": len(payload),
                        "ipfs_cid_recomputation": {"match": True},
                        "animation": {"frame_count": 3, "frame_duration_ms": 50, "total_duration_ms": 150, "loop": "infinite"},
                        "structure": {"logical_screen": {"width": structure.width, "height": structure.height}},
                    },
                }
            ),
            encoding="utf-8",
        )
        for entity_id, text in (
            (self.media_id, "Still first frame of an animated work: a teal head on black with a pink band across it."),
            (self.animation_id, "Token-linked animated GIF of eight frames that loops without end."),
        ):
            path = self.root / "records" / "entities" / f"{entity_id}.json"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps({"payload": {"profile": {"media": {"accessibility_text": text}}}}), encoding="utf-8")
        authority = self.root / media.DISPLAY_AUTHORITY_PATH
        authority.parent.mkdir(parents=True, exist_ok=True)
        authority.write_text(f"---\nrecord_id: {media.DISPLAY_AUTHORITY_ID}\nstatus: active\n---\n", encoding="utf-8")

    def patched(self) -> ExitStack:
        stack = ExitStack()
        for name, value in (
            ("ROOT", self.root),
            ("SOURCE_PATH", self.source_path),
            ("SOURCE_SUMMARY", self.source_summary),
            ("SOURCE_MANIFEST", self.source_manifest),
            ("MANIFEST_PATH", self.manifest_path),
            ("MEDIA_ROOT", self.media_root),
            ("load_transform_module", lambda: transform),
        ):
            stack.enter_context(patch.object(media, name, value))
        return stack

    def generate(self) -> dict[str, object]:
        return media.generate(self.work_id, self.media_id, "2026-10-18T10:00:00Z", "codex-task:test-constructor", self.animation_id)

    def test_generation_is_deterministic_closed_and_schema_valid(self) -> None:
        with self.patched():
            first = self.generate()
            media.write_json(self.manifest_path, first)
            count, total = media.verify()
            paths = sorted(self.media_root.rglob("*.webp"))
            retained = [path.read_bytes() for path in paths]
            second = self.generate()
            second_retained = [path.read_bytes() for path in paths]
        self.assertEqual([], schema_errors(first))
        self.assertEqual(first, second)
        self.assertEqual(retained, second_retained)
        self.assertEqual(3, count)
        self.assertGreater(total, 0)
        self.assertEqual([640, 1280, 2400], sorted(int(path.stem) for path in paths))
        item = first["items"][0]
        self.assertEqual("first_frame_poster", item["source"]["frame_policy"])
        self.assertEqual({"frame_count": 3, "frame_duration_ms": 50, "total_duration_ms": 150, "loop": "infinite"}, item["source"]["animation"])
        constraints = item["animation_reference"]["display_constraints"]
        self.assertFalse(constraints["autoplay"])
        self.assertEqual("poster_only_when_prefers_reduced_motion", constraints["reduced_motion"])
        self.assertEqual(768, constraints["max_css_width_px"])
        self.assertEqual(f"ipfs://{media.IMAGE_CID}", item["animation_reference"]["uri"])
        for path in paths:
            with Image.open(path) as image:
                self.assertEqual(1, getattr(image, "n_frames", 1))

    def test_changed_derivative_fails_fixity(self) -> None:
        with self.patched():
            media.write_json(self.manifest_path, self.generate())
            derivative = next(self.media_root.rglob("*.webp"))
            derivative.write_bytes(derivative.read_bytes() + b"changed")
            with self.assertRaisesRegex(media.MaxPainMediaError, "derivative binding mismatch"):
                media.verify()

    def test_unexpected_media_file_breaks_closed_inventory(self) -> None:
        with self.patched():
            media.write_json(self.manifest_path, self.generate())
            stray = next(self.media_root.rglob("*.webp")).with_name("animated.webp")
            stray.write_bytes(b"RIFF")
            with self.assertRaisesRegex(media.MaxPainMediaError, "inventory is not closed"):
                media.verify()

    def test_changed_source_fails_generation(self) -> None:
        with self.patched():
            self.source_path.write_bytes(self.source_path.read_bytes() + b"changed")
            with self.assertRaisesRegex(media.MaxPainMediaError, "token image fixity mismatch"):
                self.generate()

    def test_animation_facts_must_match_the_gif(self) -> None:
        summary = json.loads(self.source_summary.read_text(encoding="utf-8"))
        summary["media"]["animation"]["frame_count"] = 8
        self.source_summary.write_text(json.dumps(summary), encoding="utf-8")
        with self.patched():
            with self.assertRaisesRegex(media.MaxPainMediaError, "animation facts differ"):
                self.generate()

    def test_generation_rejects_locale_formatted_timestamp(self) -> None:
        with self.patched():
            with self.assertRaisesRegex(media.MaxPainMediaError, "canonical RFC 3339 UTC"):
                media.generate(self.work_id, self.media_id, "10/18/2026 10:00:00", "codex-task:test-constructor", self.animation_id)

    def test_poster_and_animation_references_must_differ(self) -> None:
        with self.patched():
            with self.assertRaisesRegex(media.MaxPainMediaError, "must be distinct"):
                media.generate(self.work_id, self.media_id, "2026-10-18T10:00:00Z", "codex-task:test-constructor", self.media_id)

    def test_relaxed_display_constraints_fail_verification_and_schema(self) -> None:
        with self.patched():
            value = self.generate()
            relaxed = copy.deepcopy(value)
            relaxed["items"][0]["animation_reference"]["display_constraints"]["max_css_width_px"] = 2400
            media.write_json(self.manifest_path, relaxed)
            with self.assertRaisesRegex(media.MaxPainMediaError, "display constraints mismatch"):
                media.verify()
        autoplay = copy.deepcopy(value)
        autoplay["items"][0]["animation_reference"]["display_constraints"]["autoplay"] = True
        self.assertTrue(schema_errors(autoplay))
        missing = copy.deepcopy(value)
        del missing["items"][0]["animation_reference"]
        self.assertTrue(schema_errors(missing))
        no_policy = copy.deepcopy(value)
        del no_policy["items"][0]["source"]["frame_policy"]
        self.assertTrue(schema_errors(no_policy))

    def test_review_promotion_changes_only_review_and_delivery_state(self) -> None:
        with self.patched():
            candidate = self.generate()
            reviewed = media.promote_reviewed(
                candidate,
                reviewer_id="codex-reviewer:test-independent",
                reviewed_at="2026-10-18T12:00:00Z",
                reviewed_commit="a" * 40,
            )
        self.assertEqual("constructed", candidate["record_control"]["record_status"])
        self.assertIsNone(candidate["record_control"]["review"])
        self.assertEqual("reviewed", reviewed["record_control"]["record_status"])
        self.assertEqual("approved_for_contextual_museum_display", reviewed["delivery"]["status"])
        self.assertEqual([], schema_errors(reviewed))
        normalized = json.loads(json.dumps(reviewed))
        normalized["record_control"] = candidate["record_control"]
        normalized["delivery"]["status"] = candidate["delivery"]["status"]
        self.assertEqual(candidate, normalized)
        with self.assertRaisesRegex(media.MaxPainMediaError, "review-pending"):
            media.promote_reviewed(reviewed, reviewer_id="x", reviewed_at="2026-10-18T13:00:00Z", reviewed_commit="b" * 40)


class MaxPainMediaRetainedEvidenceTests(unittest.TestCase):
    def test_retained_gif_reproduces_the_committed_posters(self) -> None:
        with tempfile.TemporaryDirectory(prefix="museum-max-pain-posters-") as temporary:
            root = Path(temporary)
            with patch.object(media, "ROOT", root), patch.object(media, "load_transform_module", lambda: transform):
                source, derivatives, colour = media.generate_derivatives("6529NM-W-0036", transform)
        self.assertEqual("untagged_assumed_srgb", colour)
        self.assertEqual({"frame_count": 8, "frame_duration_ms": 50, "total_duration_ms": 400, "loop": "infinite"}, source["animation"])
        self.assertEqual(COMMITTED_POSTERS, {row["width"]: row["sha256"] for row in derivatives})
        for row in derivatives:
            committed = REPO_ROOT / row["repository_path"]
            self.assertTrue(committed.is_file(), row["repository_path"])
            self.assertEqual(row["sha256"], transform.sha256_file(committed))

    def test_v3_admits_still_v2_style_items_without_animation_fields(self) -> None:
        vera = json.loads((REPO_ROOT / "records/accessions/6529NM.2026.003/public/presentation-manifest.json").read_text(encoding="utf-8"))
        vera["$schema"] = media.SCHEMA_PATH
        vera["schema_profile"] = media.SCHEMA_PROFILE
        self.assertEqual([], schema_errors(vera))
        vera["items"][0]["source"]["frame_policy"] = "first_frame_poster"
        self.assertTrue(schema_errors(vera))


if __name__ == "__main__":
    unittest.main()
