from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from generate_public_publication_inventory import (  # noqa: E402
    _active_media_repository_paths,
    _approved_responsive_program_media_paths,
    generate,
)


class PublicationInventoryRightsTests(unittest.TestCase):
    def _media_record(self, rights_status: str) -> dict:
        return {
            "payload": {
                "entity_status": "review_pending",
                "profile": {
                    "profile_type": "MEDIA_REFERENCE",
                    "media": {
                        "visual": True,
                        "publication_boundary": "public_derivative",
                        "rights": {"status": rights_status},
                        "source_locator": {"repository_path": "media/example.webp"},
                    },
                },
            }
        }

    def test_unknown_rights_local_media_is_not_admitted(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            entities = root / "records/entities"
            entities.mkdir(parents=True)
            asset = root / "media/example.webp"
            asset.parent.mkdir(parents=True)
            asset.write_bytes(b"example")
            record = entities / "MED.json"
            record.write_text(json.dumps(self._media_record("unknown")), encoding="utf-8")
            self.assertEqual(_active_media_repository_paths(root), set())

            record.write_text(json.dumps(self._media_record("cleared")), encoding="utf-8")
            self.assertEqual(_active_media_repository_paths(root), {"media/example.webp"})

    def test_reviewed_keys_and_gates_derivatives_are_visitor_assets(self) -> None:
        inventory = generate(ROOT)
        media_paths = {
            entry["path"]
            for entry in inventory["entries"]
            if entry["delivery_role"] == "media_asset"
        }
        keys_and_gates_paths = {
            path for path in media_paths if path.startswith("media/programs/6529NM-AP-01/")
        }
        self.assertEqual(len(keys_and_gates_paths), 44)
        self.assertIn(
            "records/programs/6529NM-AP-01/public/presentation-manifest.json",
            {entry["path"] for entry in inventory["entries"]},
        )
        self.assertIn(
            "records/proposed-gifts/6529NM-PG-2026-001/public/media/conflict-at-its-edges-cover.png",
            media_paths,
        )

    def test_responsive_expansion_requires_an_active_derivative(self) -> None:
        self.assertEqual(_approved_responsive_program_media_paths(ROOT, set()), set())


if __name__ == "__main__":
    unittest.main()
