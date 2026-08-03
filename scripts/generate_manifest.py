#!/usr/bin/env python3
"""Generate or verify the deterministic public Museum release manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat
import sys
from pathlib import Path
from typing import Any

from Crypto.Hash import keccak

from canonical import canonicalize

REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT = REPO_ROOT / "release-artifacts" / "latest" / "record-manifest.json"
INVENTORY_ROOTS = (
    ".github",
    "policies",
    "records",
    "schemas",
    "docs",
    "governance",
    "specs",
    "templates",
    "scripts",
    "tests",
)
INVENTORY_FILES = (
    ".gitattributes",
    ".gitignore",
    "AGENTS.md",
    "CONTRIBUTING.md",
    "INDEX.md",
    "README.md",
    "RIGHTS.md",
    "requirements-dev.txt",
)
JCS_ID = "0x886c7c89c308c459ca8a626e0ef36a5ea9f4c7a7b56aaf86c71a2ddf3b4f9044"


class DuplicateJsonKeyError(ValueError):
    """Raised when a JSON object repeats a key before JCS hashing."""

    def __init__(self, key: str) -> None:
        super().__init__(f"duplicate JSON object key: {key!r}")
        self.key = key


class ManifestUnsafePathError(OSError):
    """Raised when governed inventory traversal encounters a link/reparse point."""


def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateJsonKeyError(key)
        result[key] = value
    return result


def keccak256(data: bytes) -> bytes:
    digest = keccak.new(digest_bits=256)
    digest.update(data)
    return digest.digest()


def prefixed(name: str, data: bytes) -> str:
    return f"{name}:" + data.hex()


def normalized_bytes(path: Path) -> bytes:
    raw = path.read_bytes()
    return raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def inventory_paths(root: Path) -> list[Path]:
    def assert_not_link(path: Path, file_stat: os.stat_result) -> None:
        if stat.S_ISLNK(file_stat.st_mode):
            raise ManifestUnsafePathError(f"symlink is not allowed in governed inventory: {path.relative_to(root)}")
        # Windows directory junctions and other reparse points can evade
        # POSIX-style S_ISLNK checks. Reject the FILE_ATTRIBUTE_REPARSE_POINT
        # bit for every path before deciding whether to recurse.
        if getattr(file_stat, "st_file_attributes", 0) & 0x400:
            raise ManifestUnsafePathError(f"reparse point is not allowed in governed inventory: {path.relative_to(root)}")

    paths: list[Path] = []
    for inventory_file in INVENTORY_FILES:
        path = root / inventory_file
        if not os.path.lexists(path):
            raise ManifestUnsafePathError(
                f"configured governed file is missing: {path.relative_to(root)}"
            )
        file_stat = path.lstat()
        assert_not_link(path, file_stat)
        if not stat.S_ISREG(file_stat.st_mode):
            raise ManifestUnsafePathError(
                f"configured governed file is not a regular file: {path.relative_to(root)}"
            )
        paths.append(path)

    for inventory_root in INVENTORY_ROOTS:
        directory = root / inventory_root
        if not os.path.lexists(directory):
            raise ManifestUnsafePathError(
                f"configured governed root is missing: {directory.relative_to(root)}"
            )
        directory_stat = directory.lstat()
        assert_not_link(directory, directory_stat)
        if not stat.S_ISDIR(directory_stat.st_mode):
            raise ManifestUnsafePathError(
                f"configured governed root is not a directory: {directory.relative_to(root)}"
            )
        pending = [directory]
        while pending:
            current = pending.pop()
            with os.scandir(current) as entries:
                for entry in entries:
                    path = Path(entry.path)
                    entry_stat = entry.stat(follow_symlinks=False)
                    assert_not_link(path, entry_stat)
                    if any(part in {"__pycache__", ".pytest_cache", ".mypy_cache"} for part in path.relative_to(root).parts):
                        continue
                    if stat.S_ISDIR(entry_stat.st_mode):
                        pending.append(path)
                    elif stat.S_ISREG(entry_stat.st_mode) and path.suffix.lower() not in {".pyc", ".pyo"}:
                        paths.append(path)
                    elif not stat.S_ISREG(entry_stat.st_mode):
                        raise ManifestUnsafePathError(
                            f"governed inventory entry is not a regular file or directory: "
                            f"{path.relative_to(root)}"
                        )
    return sorted(paths, key=lambda path: path.relative_to(root).as_posix())


def file_entry(root: Path, path: Path) -> dict[str, Any]:
    normalized = normalized_bytes(path)
    relative = path.relative_to(root).as_posix()
    entry: dict[str, Any] = {
        "path": relative,
        "size": len(normalized),
        "sha256": prefixed("sha256", hashlib.sha256(normalized).digest()),
    }
    if path.suffix.lower() == ".json":
        with path.open("r", encoding="utf-8") as handle:
            value = json.load(handle, object_pairs_hook=reject_duplicate_keys)
        entry["content_hash"] = {
            "algorithm": 1,
            "digest": "0x" + keccak256(canonicalize(value)).hex(),
            "canonicalizationId": JCS_ID,
        }
    return entry


def manifest_body(root: Path) -> dict[str, Any]:
    return {
        "manifest_type": "6529NM_RECORD_MANIFEST",
        "manifest_version": "1.0.0",
        "inventory_roots": list(INVENTORY_ROOTS),
        "inventory_files": list(INVENTORY_FILES),
        "hash_algorithms": {"keccak256": 1, "sha256": 2},
        "canonicalization": {"name": "RFC8785_JCS", "id": JCS_ID, "profile": "museum-i-json-v1"},
        "entries": [file_entry(root, path) for path in inventory_paths(root)],
    }


def make_manifest(root: Path) -> dict[str, Any]:
    body = manifest_body(root)
    canonical_body = canonicalize(body)
    body["manifest_commitment"] = {
        "algorithm": 1,
        "digest": "0x" + keccak256(canonical_body).hex(),
        "canonicalizationId": JCS_ID,
    }
    body["manifest_sha256"] = prefixed("sha256", hashlib.sha256(canonical_body).digest())
    return body


def write_pretty(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if the committed manifest is not current")
    parser.add_argument("--output", type=Path, default=OUTPUT, help="manifest path")
    parser.add_argument("--root", type=Path, default=REPO_ROOT, help="repository root")
    args = parser.parse_args(argv)
    root = args.root.resolve()
    output = args.output if args.output.is_absolute() else root / args.output
    try:
        expected = make_manifest(root)
    except (OSError, json.JSONDecodeError, DuplicateJsonKeyError) as exc:
        print(f"manifest generation failed: {exc}")
        return 1
    if args.check:
        if not output.exists():
            print(f"manifest missing: {output}")
            return 1
        try:
            with output.open("r", encoding="utf-8") as handle:
                actual = json.load(handle, object_pairs_hook=reject_duplicate_keys)
        except (OSError, json.JSONDecodeError, DuplicateJsonKeyError) as exc:
            print(f"manifest unreadable: {exc}")
            return 1
        if actual != expected:
            print(f"manifest is stale: regenerate with python scripts/generate_manifest.py ({output})")
            return 1
        print(f"manifest is current: {output}")
        return 0
    write_pretty(output, expected)
    print(f"wrote deterministic manifest: {output}")
    print(f"keccak256: {expected['manifest_commitment']['digest']}")
    print(f"sha256: {expected['manifest_sha256']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
