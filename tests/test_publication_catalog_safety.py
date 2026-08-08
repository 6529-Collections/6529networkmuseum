from __future__ import annotations

import contextlib
import io
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

import build_publication_catalog as publication_cli  # noqa: E402
from publication_catalog import (  # noqa: E402
    CATALOG_DIR,
    POINTER_PATH,
    build_pointer,
    render_json,
    sha256_prefixed,
    validate_catalog,
    validate_pointer,
)


class PublicationCatalogSafetyTests(unittest.TestCase):
    commit = "a" * 40

    def catalog(self, *, uri: str | None = None) -> dict:
        catalog_id = f"6529NM-PUBCAT-{self.commit}"
        return {
            "envelope": {
                "contentHash": {"digest": "0x" + "1" * 64},
                "uri": uri or f"https://6529networkmuseum.org/release/catalog/{catalog_id}.json",
            },
            "payload": {
                "catalog_id": catalog_id,
                "reviewed_source_head_commit": self.commit,
            },
        }

    def pointer(self, catalog: dict, *, catalog_path: str | None = None) -> dict:
        catalog_bytes = render_json(catalog)
        return {
            "$schema": "https://6529networkmuseum.org/schemas/publication-catalog-pointer-v1.json",
            "pointer_version": "1.0.0",
            "catalog_path": catalog_path or f"{CATALOG_DIR}/{catalog['payload']['catalog_id']}.json",
            "catalog_file_sha256": sha256_prefixed(catalog_bytes),
            "catalog_envelope_content_hash": catalog["envelope"]["contentHash"]["digest"],
            "source_commit": self.commit,
            "activation": {
                "actor_id": "release-activator:test",
                "activated_at": "2026-08-08T18:01:00Z",
                "mode": "activate",
                "prior_catalog_id": None,
            },
        }

    def copy_pointer_schema(self, root: Path) -> None:
        schema_path = root / "schemas/publication-catalog-pointer.schema.json"
        schema_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / "schemas/publication-catalog-pointer.schema.json", schema_path)

    def test_pointer_rejects_noncanonical_path_before_any_catalog_or_schema_read(self) -> None:
        catalog = self.catalog()
        unsafe_paths = (
            "/release-artifacts/catalog/6529NM-PUBCAT-" + self.commit + ".json",
            "release-artifacts/catalog/../latest/6529NM-PUBCAT-" + self.commit + ".json",
            "release-artifacts/catalog//6529NM-PUBCAT-" + self.commit + ".json",
            "release-artifacts/catalog/6529NM-PUBCAT-" + self.commit.upper() + ".json",
            "release-artifacts\\catalog\\6529NM-PUBCAT-" + self.commit + ".json",
        )
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for unsafe_path in unsafe_paths:
                pointer = self.pointer(catalog, catalog_path=unsafe_path)
                issues = validate_pointer(pointer, catalog, b"this is not JSON", root=root)
                self.assertEqual(len(issues), 1, issues)
                self.assertIn("not a canonical retained catalog path", issues[0])

    def test_pointer_schema_failure_stops_before_publication_tree_reads(self) -> None:
        catalog = self.catalog()
        pointer = self.pointer(catalog)
        pointer["activation"]["mode"] = "not-a-mode"
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.copy_pointer_schema(root)
            issues = validate_pointer(pointer, catalog, render_json(catalog), root=root)
        self.assertTrue(any("publication pointer" in issue for issue in issues), issues)
        self.assertFalse(any("does not exist in the supplied publication tree" in issue for issue in issues), issues)

    def test_pointer_proves_containment_before_reading_a_symlinked_catalog_path(self) -> None:
        catalog = self.catalog()
        pointer = self.pointer(catalog)
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "publication-root"
            outside = Path(temporary) / "outside"
            root.mkdir()
            outside.mkdir()
            self.copy_pointer_schema(root)
            catalog_dir = root / CATALOG_DIR
            catalog_dir.parent.mkdir(parents=True, exist_ok=True)
            try:
                os.symlink(str(outside), str(catalog_dir), target_is_directory=True)
            except (OSError, NotImplementedError) as exc:
                self.skipTest(f"directory symlinks unavailable: {exc}")
            issues = validate_pointer(pointer, catalog, render_json(catalog), root=root)
        self.assertTrue(any("outside the supplied publication root" in issue for issue in issues), issues)

    def test_pointer_accepts_a_contained_catalog_file(self) -> None:
        catalog = self.catalog()
        catalog_bytes = render_json(catalog)
        pointer = self.pointer(catalog)
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.copy_pointer_schema(root)
            catalog_path = root / Path(*pointer["catalog_path"].split("/"))
            catalog_path.parent.mkdir(parents=True, exist_ok=True)
            catalog_path.write_bytes(catalog_bytes)
            self.assertEqual(validate_pointer(pointer, catalog, catalog_bytes, root=root), [])

    def test_catalog_requires_exact_canonical_uri_for_its_catalog_id(self) -> None:
        catalog = self.catalog(uri="https://6529networkmuseum.org/release/catalog/current.json")
        issues = validate_catalog(catalog)
        self.assertTrue(
            any("exact canonical URI for its catalog ID" in issue for issue in issues),
            issues,
        )

    def test_rollback_cli_rejects_target_equal_to_current_prior_catalog(self) -> None:
        catalog = self.catalog()
        pointer = build_pointer(
            catalog,
            catalog_file_sha256=sha256_prefixed(render_json(catalog)),
            activation_actor="release-activator:test",
            activated_at="2026-08-08T18:01:00Z",
            mode="activate",
            prior_catalog_id=None,
        )
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            pointer_path = root / Path(*POINTER_PATH.split("/"))
            pointer_path.parent.mkdir(parents=True, exist_ok=True)
            pointer_path.write_bytes(render_json(pointer))
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                with mock.patch.object(publication_cli, "ROOT", root):
                    result = publication_cli.main(
                        [
                            "--write-release",
                            "--mode",
                            "rollback",
                            "--target-catalog-id",
                            catalog["payload"]["catalog_id"],
                            "--actor",
                            "release-activator:test",
                            "--activated-at",
                            "2026-08-08T18:02:00Z",
                        ]
                    )
        self.assertEqual(result, 1)
        self.assertIn("rollback target cannot equal the current prior catalog", output.getvalue())


if __name__ == "__main__":
    unittest.main()
