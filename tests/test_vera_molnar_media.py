from __future__ import annotations

from contextlib import ExitStack
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

from jsonschema import Draft202012Validator
from PIL import Image


TESTS_DIR = Path(__file__).resolve().parent
REPO_ROOT = TESTS_DIR.parent
sys.path.append(str(REPO_ROOT / "scripts"))

import generate_program_media as transform  # noqa: E402
import generate_vera_molnar_media as media  # noqa: E402


class VeraMolnarMediaTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="museum-vera-media-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.source_path = self.root / "evidence" / "sources" / "official-preview.png"
        self.source_summary = self.root / "evidence" / "sources" / "summary.json"
        self.manifest_path = (
            self.root
            / "records"
            / "accessions"
            / media.ACCESSION_ID
            / "public"
            / "presentation-manifest.json"
        )
        self.media_root = self.root / "media" / "accessions" / media.ACCESSION_ID
        self.work_id = "6529NM-W-9999"
        self.media_id = "6529NM-MED-9999"
        self.source_path.parent.mkdir(parents=True)
        image = Image.new("RGBA", (2400, 2400), "#f3f0e9")
        image.paste("#00188d", (0, 1200, 1600, 2400))
        image.paste("#00188d", (1200, 0, 2400, 1200))
        image.save(self.source_path, format="PNG")
        digest = transform.sha256_file(self.source_path)
        self.source_summary.write_text(
            json.dumps(
                {
                    "accession_id": media.ACCESSION_ID,
                    "media": {
                        "official_preview": {
                            "height": 2400,
                            "mode": "RGBA",
                            "width": 2400,
                        }
                    },
                    "entries": [
                        {
                            "source_id": media.SOURCE_ID,
                            "url": "https://media-proxy.artblocks.io/1/test/210.png",
                            "sha256": digest,
                            "size": self.source_path.stat().st_size,
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )
        entity_path = self.root / "records" / "entities" / f"{self.media_id}.json"
        entity_path.parent.mkdir(parents=True)
        entity_path.write_text(
            json.dumps(
                {
                    "payload": {
                        "profile": {
                            "media": {
                                "accessibility_text": "A square blue and warm-white composition in which letterforms become blocks, lines and fields."
                            }
                        }
                    }
                }
            ),
            encoding="utf-8",
        )
        authority_path = self.root / media.DISPLAY_AUTHORITY_PATH
        authority_path.parent.mkdir(parents=True)
        authority_path.write_text(
            f"record_id: {media.DISPLAY_AUTHORITY_ID}\nstatus: active\n",
            encoding="utf-8",
        )

    def patched_paths(self) -> ExitStack:
        stack = ExitStack()
        stack.enter_context(patch.object(media, "ROOT", self.root))
        stack.enter_context(patch.object(media, "SOURCE_PATH", self.source_path))
        stack.enter_context(patch.object(media, "SOURCE_SUMMARY", self.source_summary))
        stack.enter_context(patch.object(media, "MANIFEST_PATH", self.manifest_path))
        stack.enter_context(patch.object(media, "MEDIA_ROOT", self.media_root))
        stack.enter_context(patch.object(media, "load_transform_module", lambda: transform))
        return stack

    def generate(self) -> dict[str, object]:
        return media.generate(
            self.work_id,
            self.media_id,
            "2026-08-23T10:00:00Z",
            "codex-task:test-constructor",
        )

    def test_generation_is_deterministic_closed_and_schema_valid(self) -> None:
        with self.patched_paths():
            first = self.generate()
            media.write_json(self.manifest_path, first)
            first_count, first_bytes = media.verify()
            paths = sorted(self.media_root.rglob("*.webp"))
            retained = [path.read_bytes() for path in paths]
            second = self.generate()
            second_retained = [path.read_bytes() for path in paths]

        schema = json.loads(
            (REPO_ROOT / "schemas" / "accession-media-presentation-v2.schema.json").read_text(
                encoding="utf-8"
            )
        )
        Draft202012Validator(schema).validate(first)
        self.assertEqual(first, second)
        self.assertEqual(retained, second_retained)
        self.assertEqual(3, first_count)
        self.assertGreater(first_bytes, 0)
        self.assertEqual([640, 1280, 2400], sorted(int(path.stem) for path in paths))
        self.assertIn("CC BY-NC 4.0", first["rights_boundary"]["status"])

    def test_changed_derivative_fails_fixity(self) -> None:
        with self.patched_paths():
            value = self.generate()
            media.write_json(self.manifest_path, value)
            derivative = next(self.media_root.rglob("*.webp"))
            derivative.write_bytes(derivative.read_bytes() + b"changed")
            with self.assertRaisesRegex(media.VeraMediaError, "derivative binding mismatch"):
                media.verify()

    def test_changed_source_fails_generation(self) -> None:
        with self.patched_paths():
            self.source_path.write_bytes(self.source_path.read_bytes() + b"changed")
            with self.assertRaisesRegex(media.VeraMediaError, "official preview fixity mismatch"):
                self.generate()

    def test_generation_rejects_locale_formatted_timestamp(self) -> None:
        with self.patched_paths():
            with self.assertRaisesRegex(media.VeraMediaError, "canonical RFC 3339 UTC"):
                media.generate(
                    self.work_id,
                    self.media_id,
                    "08/23/2026 10:00:00",
                    "codex-task:test-constructor",
                )


if __name__ == "__main__":
    unittest.main()
