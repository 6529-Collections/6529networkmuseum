#!/usr/bin/env python3
"""Build or verify proposed-gift voter dossiers from Wave Storm source parts."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from proposed_gifts import compose_voter_dossier


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail if a generated dossier is missing or stale")
    args = parser.parse_args()

    package_paths = sorted((ROOT / "records/proposed-gifts").glob("*/wave-storm.json"))
    stale: list[Path] = []
    for package_path in package_paths:
        package = json.loads(package_path.read_text(encoding="utf-8"))
        dossier = compose_voter_dossier(package_path.parent, package)
        target = package_path.parent / "public/voter-dossier.md"
        if target.exists() and target.read_text(encoding="utf-8") == dossier:
            continue
        if args.check:
            stale.append(target)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(dossier, encoding="utf-8", newline="\n")
            print(f"wrote {target.relative_to(ROOT)}")

    if stale:
        for path in stale:
            print(f"stale generated proposed-gift dossier: {path.relative_to(ROOT)}", file=sys.stderr)
        raise SystemExit(1)
    if args.check:
        print(f"Proposed-gift dossier check passed ({len(package_paths)} package(s)).")


if __name__ == "__main__":
    main()
