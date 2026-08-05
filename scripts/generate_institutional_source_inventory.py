"""Generate the deterministic source inventory for institutional scholarship."""

from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "records" / "institutional-practice"
OUTPUT = ROOT / "docs" / "institutional-source-inventory.json"
RESEARCH_CUTOFF = "2026-08-04"
MARKDOWN_LINK = re.compile(r"\[([^\]]+)\]\((https://[^)]+)\)")
WHITESPACE = re.compile(r"\s+")


def publication_paths() -> tuple[Path, ...]:
    """Return the complete, ordered institutional-publication corpus."""
    paths = [
        PACKAGE / "a-field-of-practice.md",
        PACKAGE / "adjacent-chain-native-practice.md",
        PACKAGE / "rights-and-licenses.md",
        PACKAGE / "rights-for-artists.md",
        PACKAGE / "rights-for-collectors.md",
        ROOT / "docs" / "curatorial-publication-standard.md",
        ROOT / "docs" / "digital-art-stewardship-standard.md",
    ]
    paths.extend(sorted((PACKAGE / "profiles").glob("*.md")))
    return tuple(paths)


def build_inventory() -> dict[str, object]:
    """Project normalized citation labels and manuscript paths by source URL."""
    citations: dict[str, dict[str, set[str]]] = defaultdict(
        lambda: {"labels": set(), "cited_by": set()}
    )

    for path in publication_paths():
        relative_path = path.relative_to(ROOT).as_posix()
        text = path.read_text(encoding="utf-8")
        for match in MARKDOWN_LINK.finditer(text):
            label, url = match.groups()
            citations[url]["labels"].add(WHITESPACE.sub(" ", label).strip())
            citations[url]["cited_by"].add(relative_path)

    sources = [
        {
            "url": url,
            "labels": sorted(
                values["labels"], key=lambda label: (label.casefold(), label)
            ),
            "cited_by": sorted(values["cited_by"]),
        }
        for url, values in sorted(citations.items())
    ]

    return {
        "schema": "museum:institutional-source-inventory:v1",
        "research_cutoff": RESEARCH_CUTOFF,
        "source_count": len(sources),
        "sources": sources,
    }


def serialized_inventory() -> str:
    """Serialize the inventory with stable UTF-8 JSON formatting."""
    return json.dumps(build_inventory(), ensure_ascii=False, indent=2) + "\n"


def main() -> int:
    """Write the inventory or fail when the committed bytes are stale."""
    parser = argparse.ArgumentParser(
        description="Build the deterministic institutional-practice source inventory."
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true", help="write the inventory")
    mode.add_argument("--check", action="store_true", help="verify committed bytes")
    args = parser.parse_args()

    expected = serialized_inventory()
    if args.check:
        if not OUTPUT.exists() or OUTPUT.read_text(encoding="utf-8") != expected:
            raise SystemExit(
                "institutional source inventory is stale; run "
                "python scripts/generate_institutional_source_inventory.py --write"
            )
        print(f"Institutional source inventory: {build_inventory()['source_count']} sources")
        return 0

    OUTPUT.write_text(expected, encoding="utf-8", newline="\n")
    print(f"Wrote {OUTPUT.relative_to(ROOT)} with {build_inventory()['source_count']} sources")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
