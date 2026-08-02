#!/usr/bin/env python3
"""Build canonical Casey visitor publications from accepted manuscripts."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "notes/wip/casey-curatorial-drafts"
PUBLIC = ROOT / "records/accessions/6529NM.2026.001/public"
OBJECT_DESCRIPTORS = {
    "6529NM.2026.001.01": "century",
    "6529NM.2026.001.02": "century",
    "6529NM.2026.001.03": "century",
    "6529NM.2026.001.04": "pre-process",
    "6529NM.2026.001.05": "phototaxis",
    "6529NM.2026.001.06": "923-empty-rooms",
    "6529NM.2026.001.07": "ex-nihilo-cosmos",
}


@dataclass(frozen=True)
class Publication:
    source: Path
    destination: Path
    strip_frontmatter: bool = False
    root_prefix: str | None = None


PUBLICATIONS = (
    Publication(
        SOURCE / "casey-reas-monograph.md",
        PUBLIC / "casey-reas-artist-practice.md",
        strip_frontmatter=True,
        root_prefix="../../../../",
    ),
    Publication(
        SOURCE / "the-system-in-seven-states.md",
        PUBLIC / "casey-reas-collection-essay.md",
        strip_frontmatter=True,
        root_prefix="../../../../",
    ),
    Publication(
        SOURCE / "gift-into-public-trust.md",
        PUBLIC / "gift-into-public-trust.md",
        strip_frontmatter=True,
        root_prefix="../../../../",
    ),
    Publication(
        SOURCE / "source-and-chronology-matrix.md",
        PUBLIC / "source-and-chronology-matrix.md",
        root_prefix="../../../../",
    ),
    *(
        Publication(
            SOURCE / filename,
            PUBLIC / "projects" / filename,
            root_prefix="../../../../../",
        )
        for filename in (
            "century.md",
            "process-and-pre-process.md",
            "microimage-and-phototaxis.md",
            "atomism-and-923-empty-rooms.md",
            "still-life-and-ex-nihilo.md",
        )
    ),
    *(
        Publication(
            SOURCE / "objects" / f"6529NM.2026.001.{index:02d}.md",
            PUBLIC / f"6529NM.2026.001.{index:02d}.md",
        )
        for index in range(1, 8)
    ),
)


def remove_frontmatter(text: str, source: Path) -> str:
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        return text
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            return "".join(lines[index + 1 :]).lstrip("\r\n")
    raise ValueError(f"unterminated frontmatter: {source.relative_to(ROOT)}")


def render(publication: Publication) -> str:
    text = publication.source.read_text(encoding="utf-8")
    if publication.strip_frontmatter:
        text = remove_frontmatter(text, publication.source)
    if publication.root_prefix is not None:
        text = text.replace("../../../", publication.root_prefix)
    if publication.source.parent.name == "objects":
        text = text.replace(
            "../source-and-chronology-matrix.md",
            "source-and-chronology-matrix.md",
        ).replace("../../../research/", "../../../../notes/research/")
        object_id = publication.source.stem
        descriptor = OBJECT_DESCRIPTORS[object_id]
        record_section = f"""## Museum record and research

- **Status:** `accessioned`. The work is `accessioned`. It forms part of the permanent collection.
- **Interpretive boundary:** This entry is Museum interpretation [E]. The official still documents one state; it is not a substitute for the executable software work.
- **Rights and condition:** See the [title and rights review](title-rights-and-accession-review.md). Technical condition passes with amber preservation conditions documented in the object-specific condition record.
- **Open research:** The [transparent linked descriptor](../../../../evidence/casey-reas-collection-snapshots/descriptors/{descriptor}.json) publishes the Museum's reproducible project-level feature analysis. It uses no OpenSea or marketplace rarity metric and makes no claim that feature frequency determines artistic quality.
- **Further context:** Read the [artist and practice profile](casey-reas-artist-practice.md), [collection essay](casey-reas-collection-essay.md), and [visual-observation record](../visual-observation-record.json).

"""
        marker = "## Notes and sources\n"
        if marker not in text:
            raise ValueError(f"object manuscript lacks notes section: {publication.source.relative_to(ROOT)}")
        text = text.replace(marker, record_section + marker, 1)
    return text.rstrip() + "\n"


def mismatches() -> list[Path]:
    return [
        publication.destination
        for publication in PUBLICATIONS
        if not publication.destination.is_file()
        or publication.destination.read_text(encoding="utf-8") != render(publication)
    ]


def write_publications() -> None:
    for publication in PUBLICATIONS:
        publication.destination.parent.mkdir(parents=True, exist_ok=True)
        publication.destination.write_text(render(publication), encoding="utf-8", newline="\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--write", action="store_true")
    args = parser.parse_args()

    if args.write:
        write_publications()

    stale = mismatches()
    if stale:
        names = ", ".join(str(path.relative_to(ROOT)) for path in stale)
        raise SystemExit(f"Casey publication promotion is stale: {names}")
    print(f"Casey publication promotion verified ({len(PUBLICATIONS)} files).")


if __name__ == "__main__":
    main()
