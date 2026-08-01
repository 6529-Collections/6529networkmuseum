#!/usr/bin/env python3
"""Small fail-closed validator used until the complete schema pipeline lands."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parents[1]
GOVERNED_DIRS = ("policies", "records", "docs", "governance", "schemas", "specs")
LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
LOCAL_PATH = re.compile(r"(?:[A-Za-z]:\\(?:Users|repos)\\|/home/|/Users/)")
SECRET_PATTERNS = (
    re.compile(r"gh[opsu]_[A-Za-z0-9]{30,}"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"\b(?:0x)?[0-9a-fA-F]{64}\b\s*(?:#.*)?$"),
)


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def load_json_files() -> dict[Path, object]:
    loaded: dict[Path, object] = {}
    for path in sorted(ROOT.rglob("*.json")):
        if ".git" in path.parts:
            continue
        try:
            # Immutable source snapshots may preserve an upstream UTF-8 BOM.
            # Governed JSON authored in this repository remains plain UTF-8.
            encoding = "utf-8-sig" if "evidence" in path.parts else "utf-8"
            loaded[path] = json.loads(path.read_text(encoding=encoding))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            fail(f"invalid JSON in {path.relative_to(ROOT)}: {exc}")
    return loaded


def check_local_markdown_links() -> None:
    for path in sorted(ROOT.rglob("*.md")):
        if ".git" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        for raw in LINK.findall(text):
            target = raw.strip().strip("<>").split("#", 1)[0]
            if not target or "://" in target or target.startswith(("mailto:", "#")):
                continue
            target = target.replace("%20", " ")
            if PurePosixPath(target).is_absolute():
                continue
            resolved = (path.parent / target).resolve()
            if not resolved.is_relative_to(ROOT) or not resolved.exists():
                fail(f"broken local link in {path.relative_to(ROOT)}: {raw}")


def check_public_record_safety() -> None:
    for directory in GOVERNED_DIRS:
        root = ROOT / directory
        if not root.exists():
            continue
        for path in sorted(p for p in root.rglob("*") if p.is_file()):
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            if LOCAL_PATH.search(text):
                fail(f"machine-local absolute path in governed record: {path.relative_to(ROOT)}")
            for pattern in SECRET_PATTERNS:
                if pattern.search(text):
                    fail(f"credential-shaped content in governed record: {path.relative_to(ROOT)}")


def check_governance_references(loaded: dict[Path, object]) -> None:
    decisions_path = ROOT / "records/governance/decisions.json"
    approvals_path = ROOT / "records/collections/approved-collections.json"
    if not decisions_path.exists() or not approvals_path.exists():
        return
    decisions = loaded[decisions_path]
    approvals = loaded[approvals_path]
    decision_rows = decisions.get("records", [])  # type: ignore[union-attr]
    ids = [row["decision_id"] for row in decision_rows]
    if len(ids) != len(set(ids)):
        fail("duplicate governance decision_id")
    adopted = {
        row["decision_id"]
        for row in decision_rows
        if row.get("governance_effect") == "adopted"
        and row.get("observed_wave_status") == "WINNER"
    }
    for row in approvals.get("collections", []):  # type: ignore[union-attr]
        if row.get("decision_id") not in adopted:
            fail(f"approved collection lacks adopted WINNER decision: {row.get('approval_id')}")


def main() -> None:
    loaded = load_json_files()
    check_local_markdown_links()
    check_public_record_safety()
    check_governance_references(loaded)
    print(f"Museum bootstrap validation passed ({len(loaded)} JSON files checked).")


if __name__ == "__main__":
    main()
