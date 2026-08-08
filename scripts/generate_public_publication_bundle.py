#!/usr/bin/env python3
"""Generate/check the deterministic UTF-8 visitor assembly bundle."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

from Crypto.Hash import keccak

from canonical import canonicalize
from generate_public_publication_inventory import (
    JCS_ID,
    MAX_BUNDLE_BYTES,
    OUTPUT as INVENTORY_PATH,
    PUBLICATION_BUNDLE_PATH,
    InventoryError,
    require_file,
    strict_load,
    validate_inventory,
)


ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / Path(*PUBLICATION_BUNDLE_PATH.split("/"))
TEXT_EXTENSIONS = {".json", ".md", ".txt", ".py", ".yml", ".yaml", ".svg", ".gitattributes", ".gitignore"}


def keccak256(data: bytes) -> bytes:
    digest = keccak.new(digest_bits=256)
    digest.update(data)
    return digest.digest()


def sha256_prefixed(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def normalized_text(path: str, data: bytes) -> bytes:
    suffix = Path(path).suffix.casefold()
    if suffix not in TEXT_EXTENSIONS and Path(path).name.casefold() not in {"codeowners"}:
        raise InventoryError(f"bundle contains unsupported non-text path: {path}")
    normalized = data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    try:
        normalized.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise InventoryError(f"bundle source is not UTF-8: {path}: {exc}") from exc
    return normalized


def entry(root: Path, relative: str) -> dict[str, Any]:
    data = normalized_text(relative, require_file(root, relative).read_bytes())
    jcs_keccak: str | None = None
    if relative.casefold().endswith(".json"):
        value = strict_load(data)
        jcs_keccak = "0x" + keccak256(canonicalize(value)).hex()
    return {
        "path": relative,
        "byte_mode": "lf-normalized",
        "content": data.decode("utf-8"),
        "file_size": len(data),
        "sha256": sha256_prefixed(data),
        "jcs_keccak256": jcs_keccak,
    }


def inventory_body_commitment(inventory: dict[str, Any]) -> tuple[str, str]:
    body = canonicalize(inventory)
    return sha256_prefixed(body), "0x" + keccak256(body).hex()


def generate(root: Path = ROOT) -> dict[str, Any]:
    inventory_path = root / "schemas/public-publication-inventory.json"
    inventory = strict_load(inventory_path.read_bytes())
    if not isinstance(inventory, dict):
        raise InventoryError("publication inventory must be an object")
    issues = validate_inventory(root, inventory)
    if issues:
        raise InventoryError("; ".join(issues))
    assembly_paths = inventory["assembler"]["required_paths"]
    entries = [entry(root, path) for path in assembly_paths]
    source_sha256, source_keccak = inventory_body_commitment(inventory)
    value = {
        "$schema": "../../schemas/public-publication-bundle.schema.json",
        "bundle_version": "1.0.0",
        "bundle_id": "6529NM_PUBLIC_VISITOR_CORPUS_BUNDLE_V1",
        "source_inventory_path": "schemas/public-publication-inventory.json",
        "source_inventory_body_sha256": source_sha256,
        "source_inventory_body_keccak256": source_keccak,
        "canonicalization_id": JCS_ID,
        "entries": entries,
        "entry_count": len(entries),
        "content_bytes": sum(item["file_size"] for item in entries),
    }
    encoded = (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")
    if len(encoded) > MAX_BUNDLE_BYTES:
        raise InventoryError(f"visitor corpus bundle exceeds {MAX_BUNDLE_BYTES} bytes: {len(encoded)}")
    return value


def write(root: Path = ROOT) -> None:
    value = generate(root)
    output = root / Path(*PUBLICATION_BUNDLE_PATH.split("/"))
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def check(root: Path = ROOT) -> int:
    output = root / Path(*PUBLICATION_BUNDLE_PATH.split("/"))
    try:
        actual = strict_load(output.read_bytes())
        if actual != generate(root):
            print("visitor corpus bundle is stale; regenerate with scripts/generate_public_publication_bundle.py")
            return 1
    except (OSError, json.JSONDecodeError, InventoryError) as exc:
        print(f"visitor corpus bundle check failed: {exc}")
        return 1
    print(f"visitor corpus bundle is current: {output}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args(argv)
    root = args.root.resolve()
    try:
        if args.check:
            return check(root)
        write(root)
    except (OSError, json.JSONDecodeError, InventoryError) as exc:
        print(f"visitor corpus bundle generation failed: {exc}")
        return 1
    print(f"wrote deterministic visitor corpus bundle: {root / Path(*PUBLICATION_BUNDLE_PATH.split('/'))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
