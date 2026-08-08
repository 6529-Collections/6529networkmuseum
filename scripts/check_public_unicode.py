"""Reject known double-decoding markers in the Keys and Gates public corpus.

This check is intentionally narrower than an ASCII-only policy. Legitimate
Unicode names, titles, punctuation, and Bangla text are expected in the
corpus; only known replacement/double-decoding sequences are rejected.
"""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PUBLIC_ROOT = ROOT / "records" / "programs" / "6529NM-AP-01" / "public"
EXPECTED_TITLE = "মুক্তিযুদ্ধ - Fight for Freedom"
EXPECTED_TITLE_CODEPOINTS = (
    0x09AE,
    0x09C1,
    0x0995,
    0x09CD,
    0x09A4,
    0x09BF,
    0x09AF,
    0x09C1,
    0x09A6,
    0x09CD,
    0x09A7,
)

# These are observed UTF-8/Latin-1 or UTF-8/Windows-1252 double-decoding
# products from the previous artist-file pass. Do not reject Unicode merely
# because it is non-ASCII.
MOJIBAKE_MARKERS = (
    "\u00c3\u00a9",  # Ã©
    "\u00c3\u00bc",  # Ã¼
    "\u00c3\u00a3",  # Ã£
    "\u00c3\u00b6",  # Ã¶
    "\u00c3\u00b1",  # Ã±
    "\u00c3\u00b3",  # Ã³
    "\u00c3\u00a4",  # Ã¤
    "\u00c3\u00a7",  # Ã§
    "\u00c3\u00a1",  # Ã¡
    "\u00c3\u00ad",  # Ã­
    "\u00c3\u00ba",  # Ãº
    "\u00c2\u00a0",  # Â 
    "\u00c2\u00b7",  # Â·
    "\u00e2\u20ac",  # â€...
    "\u00e2\u0080",  # â...
    "\u00e2\u0081",  # â...
    "\u00e2\u0082",  # â...
    "\u00e2\u0083",  # â...
    "\u00e2\u0084",  # â...
    "\u00ce\u017e",  # Îž
    "\u00ef\u00bb\u00bf",  # ï»¿
    "\ufffd",  # replacement character
)


def scan_public(root: Path = PUBLIC_ROOT) -> list[str]:
    """Return validation errors for UTF-8 and known mojibake markers."""

    errors: list[str] = []
    markdown_files = sorted(root.rglob("*.md"))
    if not markdown_files:
        return [f"public corpus is empty: {root}"]

    decoded: dict[Path, str] = {}
    for path in markdown_files:
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError as exc:
            errors.append(f"{path.relative_to(ROOT)} is not strict UTF-8: {exc}")
            continue
        decoded[path] = text
        for marker in MOJIBAKE_MARKERS:
            if marker in text:
                offset = text.index(marker)
                errors.append(
                    f"{path.relative_to(ROOT)} contains {marker!r} at codepoint offset {offset}"
                )

    acquisition = root / "curated-acquisition.md"
    work = root / "works" / "fight-for-freedom.md"
    for path in (acquisition, work):
        text = decoded.get(path)
        if text is None:
            errors.append(f"missing Unicode test target: {path.relative_to(ROOT)}")
            continue
        if EXPECTED_TITLE not in text:
            errors.append(f"{path.relative_to(ROOT)} does not contain the exact UTF-8 title")

    if acquisition in decoded:
        text = decoded[acquisition]
        if "Selected through an acquisition program; acquisition pending" not in text:
            errors.append("acquisition page is missing the approved visitor state")
        if "Not in the permanent Collection; no accession recorded." not in text:
            errors.append("acquisition page is missing the approved Collection relationship")

    hugo = root / "artists" / "hugofaz.md"
    if hugo in decoded and "São Paulo" not in decoded[hugo]:
        errors.append("Hugo Faz profile does not contain the expected São Paulo codepoints")

    # Assert that the exact Bangla spelling is real Unicode, not a visually
    # similar ASCII or mojibake substitute.
    if work in decoded:
        title_index = decoded[work].find(EXPECTED_TITLE)
        if title_index >= 0:
            actual = tuple(
                ord(char) for char in EXPECTED_TITLE[: len(EXPECTED_TITLE_CODEPOINTS)]
            )
            if actual != EXPECTED_TITLE_CODEPOINTS:
                errors.append("Bangla title codepoint assertion failed")

    return errors


def main() -> int:
    errors = scan_public()
    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors))
        return 1
    print(f"UTF-8/no-mojibake check passed for {len(list(PUBLIC_ROOT.rglob('*.md')))} public Markdown files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
