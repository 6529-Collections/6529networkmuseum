from __future__ import annotations

import contextlib
import io
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

import build_publication_catalog as publication_cli  # noqa: E402
import publication_catalog as catalog_module  # noqa: E402
from publication_catalog import (  # noqa: E402
    CATALOG_DIR,
    POINTER_PATH,
    build_catalog,
    build_pointer,
    check_catalog_git_transition,
    render_json,
    sha256_prefixed,
    validate_catalog,
    validate_pointer,
)


class PublicationCatalogSafetyTests(unittest.TestCase):
    commit = "a" * 40

    def catalog(self, *, commit: str | None = None, uri: str | None = None) -> dict:
        source_commit = commit or self.commit
        catalog_id = f"6529NM-PUBCAT-{source_commit}"
        return {
            "envelope": {
                "contentHash": {"digest": "0x" + "1" * 64},
                "uri": uri or f"https://6529networkmuseum.org/release/catalog/{catalog_id}.json",
            },
            "payload": {
                "catalog_id": catalog_id,
                "reviewed_source_head_commit": source_commit,
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
            "source_commit": catalog["payload"]["reviewed_source_head_commit"],
            "activation": {
                "actor_id": "release-activator:test",
                "activated_at": "2026-08-08T18:01:00Z",
                "mode": "activate",
                "prior_catalog_id": None,
            },
        }

    def init_git(self, root: Path) -> None:
        subprocess.run(["git", "init", "-q"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.invalid"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.name", "Publication Catalog Safety Test"], cwd=root, check=True)

    def commit_git(self, root: Path, message: str) -> str:
        subprocess.run(["git", "add", "-A"], cwd=root, check=True)
        subprocess.run(["git", "commit", "-qm", message], cwd=root, check=True)
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()

    def write_catalog(self, root: Path, catalog: dict) -> Path:
        path = root / Path(*f"{CATALOG_DIR}/{catalog['payload']['catalog_id']}.json".split("/"))
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(render_json(catalog))
        return path

    def write_pointer(self, root: Path, pointer: dict) -> Path:
        path = root / Path(*POINTER_PATH.split("/"))
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(render_json(pointer))
        return path

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
            catalog_path = self.write_catalog(root, catalog)
            pointer_path = root / Path(*POINTER_PATH.split("/"))
            self.write_pointer(root, pointer)
            self.init_git(root)
            self.commit_git(root, "retained active catalog")
            pointer_bytes = pointer_path.read_bytes()
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                with mock.patch.object(publication_cli, "ROOT", root), mock.patch.object(
                    publication_cli, "validate_catalog", return_value=[]
                ), mock.patch.object(publication_cli, "validate_pointer", return_value=[]):
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
            pointer_after = pointer_path.read_bytes()
            catalog_after = catalog_path.read_bytes()
        self.assertEqual(result, 1)
        self.assertIn("rollback target cannot equal the current prior catalog", output.getvalue())
        self.assertEqual(pointer_after, pointer_bytes)
        self.assertEqual(catalog_after, render_json(catalog))

    def test_rollback_rejects_a_worktree_only_catalog_before_pointer_write(self) -> None:
        active = self.catalog(commit="a" * 40)
        target = self.catalog(commit="b" * 40)
        active_pointer = build_pointer(
            active,
            catalog_file_sha256=sha256_prefixed(render_json(active)),
            activation_actor="release-activator:test",
            activated_at="2026-08-08T18:01:00Z",
            mode="activate",
            prior_catalog_id=None,
        )
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.write_catalog(root, active)
            pointer_path = self.write_pointer(root, active_pointer)
            self.init_git(root)
            self.commit_git(root, "retained active catalog")
            target_path = self.write_catalog(root, target)
            pointer_bytes = pointer_path.read_bytes()
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                with mock.patch.object(publication_cli, "ROOT", root), mock.patch.object(
                    publication_cli, "validate_catalog", return_value=[]
                ), mock.patch.object(publication_cli, "validate_pointer", return_value=[]):
                    result = publication_cli.main(
                        [
                            "--write-release",
                            "--mode",
                            "rollback",
                            "--target-catalog-id",
                            target["payload"]["catalog_id"],
                            "--actor",
                            "release-activator:test",
                            "--activated-at",
                            "2026-08-08T18:02:00Z",
                        ]
                    )
            self.assertEqual(result, 1)
            self.assertIn("absent or ambiguous", output.getvalue())
            self.assertEqual(pointer_path.read_bytes(), pointer_bytes)
            self.assertEqual(target_path.read_bytes(), render_json(target))

    def test_rollback_rejects_a_rewritten_worktree_catalog_even_when_git_retains_it(self) -> None:
        active = self.catalog(commit="a" * 40)
        target = self.catalog(commit="b" * 40)
        active_pointer = build_pointer(
            active,
            catalog_file_sha256=sha256_prefixed(render_json(active)),
            activation_actor="release-activator:test",
            activated_at="2026-08-08T18:01:00Z",
            mode="activate",
            prior_catalog_id=None,
        )
        target_bytes = render_json(target)
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.write_catalog(root, active)
            target_path = self.write_catalog(root, target)
            pointer_path = self.write_pointer(root, active_pointer)
            self.init_git(root)
            self.commit_git(root, "retained active and target catalogs")
            target_path.write_bytes(target_bytes + b"\n")
            pointer_bytes = pointer_path.read_bytes()
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                with mock.patch.object(publication_cli, "ROOT", root), mock.patch.object(
                    publication_cli, "validate_catalog", return_value=[]
                ), mock.patch.object(publication_cli, "validate_pointer", return_value=[]):
                    result = publication_cli.main(
                        [
                            "--write-release",
                            "--mode",
                            "rollback",
                            "--target-catalog-id",
                            target["payload"]["catalog_id"],
                            "--actor",
                            "release-activator:test",
                            "--activated-at",
                            "2026-08-08T18:02:00Z",
                        ]
                    )
            self.assertEqual(result, 1)
            self.assertIn("exact retained Git-tree catalog", output.getvalue())
            self.assertEqual(pointer_path.read_bytes(), pointer_bytes)

    def test_review_proof_parses_candidate_a_inventory_and_bundle(self) -> None:
        from tests.test_stream_adapter_and_publication_catalog import PublicationCatalogTests

        fixture = PublicationCatalogTests()
        temporary, root, candidate, reviewed = fixture.fixture_repo()
        try:
            with mock.patch.object(
                catalog_module, "_read_inventory", wraps=catalog_module._read_inventory
            ) as read_inventory, mock.patch.object(
                catalog_module, "_bundle_binding", wraps=catalog_module._bundle_binding
            ) as bundle_binding:
                build_catalog(
                    root,
                    reviewed_source_head_commit=reviewed,
                    accepted_paths=None,
                    created_at="2026-08-08T19:00:00Z",
                )
            self.assertIn(candidate, [call.args[1] for call in read_inventory.call_args_list])
            self.assertIn(candidate, [call.args[1] for call in bundle_binding.call_args_list])
            self.assertFalse((root / Path(*POINTER_PATH.split("/"))).exists())
        finally:
            temporary.cleanup()

    def test_transition_rejects_intermediate_delete_or_rewrite_restore(self) -> None:
        for mutation in ("delete", "rewrite"):
            with self.subTest(mutation=mutation):
                with tempfile.TemporaryDirectory() as temporary:
                    root = Path(temporary)
                    active = self.catalog(commit="a" * 40)
                    target = self.catalog(commit="b" * 40)
                    active_bytes = render_json(active)
                    active_path = self.write_catalog(root, active)
                    active_pointer = build_pointer(
                        active,
                        catalog_file_sha256=sha256_prefixed(active_bytes),
                        activation_actor="release-activator:test",
                        activated_at="2026-08-08T18:01:00Z",
                        mode="activate",
                        prior_catalog_id=None,
                    )
                    self.write_pointer(root, active_pointer)
                    self.init_git(root)
                    previous_commit = self.commit_git(root, "initial activation")
                    if mutation == "delete":
                        active_path.unlink()
                    else:
                        active_path.write_bytes(active_bytes + b"\n")
                    self.commit_git(root, f"intermediate {mutation}")
                    active_path.write_bytes(active_bytes)
                    self.commit_git(root, "restore historical catalog")
                    target_bytes = render_json(target)
                    self.write_catalog(root, target)
                    target_pointer = build_pointer(
                        target,
                        catalog_file_sha256=sha256_prefixed(target_bytes),
                        activation_actor="release-activator:test",
                        activated_at="2026-08-08T19:01:00Z",
                        mode="activate",
                        prior_catalog_id=active["payload"]["catalog_id"],
                    )
                    self.write_pointer(root, target_pointer)
                    current_commit = self.commit_git(root, "second activation")
                    with mock.patch.object(catalog_module, "validate_catalog", return_value=[]), mock.patch.object(
                        catalog_module, "validate_pointer", return_value=[]
                    ):
                        issues = check_catalog_git_transition(root, previous_commit, current_commit)
                    self.assertTrue(
                        any("immutable historical catalog was deleted or rewritten" in issue for issue in issues),
                        issues,
                    )


if __name__ == "__main__":
    unittest.main()
