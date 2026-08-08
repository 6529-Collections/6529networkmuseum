"""Keep release-manifest byte modes aligned with the publication catalog."""

from __future__ import annotations

import hashlib
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import generate_manifest  # noqa: E402
import publication_catalog  # noqa: E402


class ManifestBinaryModeTests(unittest.TestCase):
    FIXTURE = b"leading\r\n\x00binary\r\ntrailing\r\n"

    def test_binary_extensions_match_catalog_mode_size_and_sha(self) -> None:
        self.assertEqual(
            generate_manifest.BINARY_EXTENSIONS,
            publication_catalog.BINARY_EXTENSIONS,
        )

        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            for extension in sorted(publication_catalog.BINARY_EXTENSIONS):
                path = root / f"fixture{extension}"
                path.write_bytes(self.FIXTURE)

                catalog_bytes, catalog_mode = publication_catalog.normalized_bytes(
                    path.name,
                    self.FIXTURE,
                )
                manifest_entry = generate_manifest.file_entry(root, path)

                self.assertEqual(catalog_mode, "raw", extension)
                self.assertEqual(catalog_bytes, self.FIXTURE, extension)
                self.assertEqual(manifest_entry["byte_mode"], catalog_mode, extension)
                self.assertEqual(manifest_entry["size"], len(catalog_bytes), extension)
                self.assertEqual(
                    manifest_entry["sha256"],
                    "sha256:" + hashlib.sha256(catalog_bytes).hexdigest(),
                    extension,
                )

    def test_svg_remains_lf_normalized_text(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            path = root / "fixture.svg"
            path.write_bytes(self.FIXTURE)

            catalog_bytes, catalog_mode = publication_catalog.normalized_bytes(
                path.name,
                self.FIXTURE,
            )
            manifest_entry = generate_manifest.file_entry(root, path)

            self.assertEqual(catalog_mode, "lf-normalized")
            self.assertEqual(catalog_bytes, self.FIXTURE.replace(b"\r\n", b"\n").replace(b"\r", b"\n"))
            self.assertEqual(manifest_entry["byte_mode"], catalog_mode)
            self.assertEqual(manifest_entry["size"], len(catalog_bytes))
            self.assertEqual(
                manifest_entry["sha256"],
                "sha256:" + hashlib.sha256(catalog_bytes).hexdigest(),
            )


if __name__ == "__main__":
    unittest.main()
