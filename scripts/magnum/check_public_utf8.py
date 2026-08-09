"""Fail-closed UTF-8 and classic-mojibake check for every public manuscript."""

from __future__ import annotations

from pathlib import Path
import sys


REPOSITORY = Path(__file__).resolve().parents[2]
ROOT = REPOSITORY / "records" / "proposed-gifts" / "6529NM-PG-2026-001" / "public" / "scholarship"
# These are the UTF-8 byte prefixes produced when classic Windows-1252
# mojibake markers (Â, Ã, â, ð) have themselves been saved as UTF-8. A marker
# is reported only when a complete cp1252 -> UTF-8 repair round-trip succeeds
# and removes at least one marker; valid Unicode such as ©, ×, —, or Å is not
# rejected by a decoded-text character class.
CLASSIC_MARKER_BYTES = (b"\xc3\x82", b"\xc3\x83", b"\xc3\xa2", b"\xc3\xb0")
CLASSIC_MARKERS = "ÂÃâð"
REPLACEMENT = "\ufffd"


def classic_mojibake_repair(text: str, raw: bytes) -> str | None:
    """Return a repaired candidate only for a conservative classic signature."""

    if not any(signature in raw for signature in CLASSIC_MARKER_BYTES):
        return None
    before = sum(text.count(marker) for marker in CLASSIC_MARKERS)
    if before == 0:
        return None
    try:
        repaired = text.encode("cp1252").decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError):
        return None
    after = sum(repaired.count(marker) for marker in CLASSIC_MARKERS)
    if repaired == text or after >= before or REPLACEMENT in repaired:
        return None
    return repaired


def main() -> int:
    files = sorted(ROOT.rglob("*.md"))
    if ROOT / "README.md" not in files:
        print("Public corpus UTF-8 check failed: scholarship README.md is missing", file=sys.stderr)
        return 1
    errors: list[str] = []
    for path in files:
        relative = path.relative_to(ROOT).as_posix()
        raw = path.read_bytes()
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError as exc:
            errors.append(f"{relative}: invalid UTF-8 at byte {exc.start}")
            continue
        if REPLACEMENT in text:
            errors.append(f"{relative}: Unicode replacement character U+FFFD")
        repaired = classic_mojibake_repair(text, raw)
        if repaired is not None:
            errors.append(f"{relative}: classic cp1252/UTF-8 mojibake signature detected")

    if errors:
        print("Public corpus UTF-8 check failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"Public corpus UTF-8 check passed: {len(files)} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
