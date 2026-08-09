from __future__ import annotations

import json
import sys
import tempfile
import unittest
from contextlib import ExitStack
from pathlib import Path
from unittest.mock import patch

from PIL import Image, ImageCms

TESTS_DIR = Path(__file__).resolve().parent
REPO_ROOT = TESTS_DIR.parent
sys.path.append(str(REPO_ROOT / "scripts"))

import generate_program_media as media  # noqa: E402


class ProgramMediaTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="museum-program-media-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.outcome_root = self.root / "records" / "programs" / media.PROGRAM_ID / "outcomes"
        self.outcome_root.mkdir(parents=True)
        self.selected_path = self.outcome_root.parent / "selected-works.json"
        self.manifest_path = self.outcome_root.parent / "media-manifest.json"
        self.media_root = self.root / "media" / "programs" / media.PROGRAM_ID
        self.media_root.mkdir(parents=True)
        self.accessibility_path = self.media_root / "accessibility.json"
        self.source_root = self.root / "sources"
        self.source_root.mkdir()
        self.record_id = f"{media.PROGRAM_ID}-OUT-001"
        self.source_url = "https://d3lqz0a4bldqgf.cloudfront.net/drops/test/source.png"
        outcome = {
            "record_id": self.record_id,
            "media": [
                {
                    "url": self.source_url,
                    "mime_type": "image/png",
                }
            ],
            "rights_and_consent": {
                "rights_effective_status": "unverified until acquisition"
            },
        }
        (self.outcome_root / "OUT-001.json").write_text(
            json.dumps(outcome), encoding="utf-8"
        )
        self.selected_path.write_text(
            json.dumps({"works": [{"record_id": self.record_id}]}),
            encoding="utf-8",
        )
        self.accessibility_path.write_text(
            json.dumps(
                {
                    "program_id": media.PROGRAM_ID,
                    "status": media.ALT_TEXT_STATUS,
                    "items": [
                        {
                            "record_id": self.record_id,
                            "alt_text": "A geometric red and blue test image used to verify deterministic conversion.",
                            "public_widths": [640, 1280, 2400],
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )
        image = Image.new("RGB", (2400, 1200), "#2244aa")
        for x in range(0, 2400, 80):
            for y in range(0, 1200, 80):
                if (x // 80 + y // 80) % 2 == 0:
                    image.paste("#cc3322", (x, y, x + 80, y + 80))
        image.save(self.source_root / f"{self.record_id}.png", format="PNG")

    def patched_paths(self) -> ExitStack:
        stack = ExitStack()
        stack.enter_context(patch.object(media, "REPO_ROOT", self.root))
        stack.enter_context(patch.object(media, "OUTCOME_ROOT", self.outcome_root))
        stack.enter_context(patch.object(media, "SELECTED_WORKS_PATH", self.selected_path))
        stack.enter_context(patch.object(media, "ACCESSIBILITY_PATH", self.accessibility_path))
        stack.enter_context(patch.object(media, "MANIFEST_PATH", self.manifest_path))
        stack.enter_context(patch.object(media, "MEDIA_ROOT", self.media_root))
        stack.enter_context(patch.object(media, "EXPECTED_OUTCOME_COUNT", 1))
        return stack

    def generate(self) -> dict[str, object]:
        return media.generate_manifest(
            self.source_root,
            "2026-08-04T00:00:00Z",
            "2026-08-04T00:00:01Z",
            "codex-task:test-constructor",
            "test:reviewed-display-authority",
        )

    def test_generation_is_deterministic_and_closed(self) -> None:
        with self.patched_paths():
            first = self.generate()
            media.write_json(self.manifest_path, first)
            count, total_bytes = media.verify_manifest()
            paths = sorted(self.media_root.rglob("*.webp"))
            first_bytes = [path.read_bytes() for path in paths]
            second = self.generate()
            second_bytes = [path.read_bytes() for path in paths]

        self.assertEqual(first, second)
        self.assertEqual(first_bytes, second_bytes)
        self.assertEqual(3, count)
        self.assertGreater(total_bytes, 0)

    def test_srgb_profile_is_fixed_and_hash_bound(self) -> None:
        first_profile, first_bytes = media.fixed_srgb_profile()
        second_profile, second_bytes = media.fixed_srgb_profile()

        self.assertEqual(first_bytes, second_bytes)
        self.assertEqual(media.SRGB_ICC_SHA256, media.sha256_bytes(first_bytes))
        self.assertEqual(588, len(first_bytes))
        self.assertEqual(
            ImageCms.getProfileDescription(first_profile),
            ImageCms.getProfileDescription(second_profile),
        )

    def test_srgb_profile_hash_mismatch_keeps_specific_error(self) -> None:
        with patch.object(media, "SRGB_ICC_SHA256", "sha256:" + "0" * 64):
            with self.assertRaisesRegex(
                media.ProgramMediaError,
                r"^fixed sRGB ICC profile hash does not match$",
            ):
                media.fixed_srgb_profile()

    def test_fixity_check_rejects_changed_derivative(self) -> None:
        with self.patched_paths():
            manifest = self.generate()
            media.write_json(self.manifest_path, manifest)
            derivative = next(self.media_root.rglob("*.webp"))
            derivative.write_bytes(derivative.read_bytes() + b"changed")
            with self.assertRaisesRegex(media.ProgramMediaError, "fixity mismatch"):
                media.verify_manifest()

    def test_fixity_check_rejects_cross_variant_aspect_ratio_change(self) -> None:
        with self.patched_paths():
            manifest = self.generate()
            derivatives = manifest["items"][0]["presentation"]["derivatives"]
            self.assertEqual(
                [(640, 320), (1280, 640), (2400, 1200)],
                [(item["width"], item["height"]) for item in derivatives],
            )
            derivatives[0]["height"] = 511
            media.write_json(self.manifest_path, manifest)
            with self.assertRaisesRegex(media.ProgramMediaError, "aspect ratio differs"):
                media.verify_manifest()

    def test_withheld_manifest_has_no_derivatives_or_authority(self) -> None:
        accessibility = json.loads(self.accessibility_path.read_text(encoding="utf-8"))
        accessibility["items"][0]["public_widths"] = []
        self.accessibility_path.write_text(json.dumps(accessibility), encoding="utf-8")
        with self.patched_paths():
            manifest = media.generate_manifest(
                self.source_root,
                "2026-08-04T00:00:00Z",
                "2026-08-04T00:00:01Z",
                "codex-task:test-constructor",
            )
            media.write_json(self.manifest_path, manifest)
            count, total_bytes = media.verify_manifest()

        self.assertEqual(media.WITHHELD_DELIVERY_STATUS, manifest["delivery"]["status"])
        self.assertIsNone(manifest["delivery"]["authority_record_id"])
        self.assertEqual([], manifest["items"][0]["presentation"]["derivatives"])
        self.assertEqual((0, 0), (count, total_bytes))


if __name__ == "__main__":
    unittest.main()
