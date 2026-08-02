#!/usr/bin/env python3
"""Build or check the complete Casey accession-diligence evidence inventory."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PACKAGE = ROOT / "evidence" / "casey-reas-diligence"
MEDIA_TYPES = {".json": "application/json", ".md": "text/plain"}


class ManifestError(RuntimeError):
    """Raised when a complete deterministic manifest cannot be built."""


def entry(package: Path, path: Path) -> dict[str, Any]:
    relative = path.relative_to(package).as_posix()
    payload = path.read_bytes()
    media_type = MEDIA_TYPES.get(path.suffix.lower())
    if media_type is None:
        raise ManifestError(f"unsupported evidence media type: {relative}")
    return {
        "path": relative,
        # Evidence manifests use raw lowercase hex for per-entry digests; the
        # enclosing dossier uses the `sha256:` HashRef form for manifest-file
        # bindings. Keeping the two domains explicit matches bootstrap rules.
        "sha256": hashlib.sha256(payload).hexdigest(),
        "size": len(payload),
        "media_type": media_type,
        "byte_mode": "raw",
    }


def build(package: Path) -> dict[str, Any]:
    package = package.resolve()
    if not package.is_dir():
        raise ManifestError(f"package directory does not exist: {package}")
    files = sorted(
        (path for path in package.rglob("*") if path.is_file() and path.name != "manifest.json"),
        key=lambda path: path.relative_to(package).as_posix(),
    )
    if not files:
        raise ManifestError("diligence evidence package is empty")
    entries = [entry(package, path) for path in files]
    paths = [item["path"] for item in entries]
    required = {"README.md", "custody-audit-2026-08-02.json", "ofac-address-screening-2026-08-02.json"}
    if not required.issubset(paths):
        raise ManifestError("diligence evidence package is missing a required reviewed component")
    raw_rpc_count = sum(path.startswith("raw/rpc/") for path in paths)
    if raw_rpc_count != 19:
        raise ManifestError(f"expected 19 exact RPC response files, found {raw_rpc_count}")
    custody = json.loads((package / "custody-audit-2026-08-02.json").read_text(encoding="utf-8"))
    manifest = {
        "manifest_type": "6529NM_CASEY_ACCESSION_DILIGENCE_EVIDENCE",
        "manifest_version": "1.0.0",
        "subject_id": "6529NM.2026.001",
        "observed_at": custody["observed_at"],
        "hash_algorithm": "sha256",
        "byte_mode": "raw",
        "status": "complete",
        "inventory": {"file_count": len(entries), "raw_rpc_response_count": raw_rpc_count},
        "entries": entries,
    }
    return manifest


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--package", type=Path, default=DEFAULT_PACKAGE)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)
    try:
        package = args.package.resolve()
        expected = build(package)
        manifest_path = package / "manifest.json"
        if args.check:
            actual = json.loads(manifest_path.read_text(encoding="utf-8"))
            if actual != expected:
                raise ManifestError("committed diligence evidence manifest is stale")
            result = {"status": "current", "file_count": expected["inventory"]["file_count"]}
        else:
            manifest_path.write_text(json.dumps(expected, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
            result = {
                "status": "written",
                "file_count": expected["inventory"]["file_count"],
                "sha256": f"sha256:{hashlib.sha256(manifest_path.read_bytes()).hexdigest()}",
            }
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except (ManifestError, OSError, UnicodeDecodeError, json.JSONDecodeError, KeyError, TypeError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
