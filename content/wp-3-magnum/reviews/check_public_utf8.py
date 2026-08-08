"""Fail-closed UTF-8 and mojibake check for the visitor-facing WP-3 corpus."""

from __future__ import annotations

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
PUBLIC_DIRS = (ROOT / "entities", ROOT / "artists", ROOT / "works", ROOT / "essays")
MOJIBAKE_RE = re.compile(r"[\u00c2\u00c3\u00e2\u00f0][\u0080-\u00bf]")
REPLACEMENT = "\ufffd"


def main() -> int:
    files = sorted(
        path
        for directory in PUBLIC_DIRS
        for path in directory.glob("*.md")
    )
    errors: list[str] = []
    for path in files:
        relative = path.relative_to(ROOT).as_posix()
        try:
            text = path.read_bytes().decode("utf-8")
        except UnicodeDecodeError as exc:
            errors.append(f"{relative}: invalid UTF-8 at byte {exc.start}")
            continue
        if REPLACEMENT in text:
            errors.append(f"{relative}: Unicode replacement character U+FFFD")
        match = MOJIBAKE_RE.search(text)
        if match:
            codepoints = " ".join(f"U+{ord(char):04X}" for char in match.group())
            errors.append(f"{relative}: suspicious mojibake {match.group()!r} ({codepoints})")

    if errors:
        print("Public corpus UTF-8 check failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"Public corpus UTF-8 check passed: {len(files)} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
