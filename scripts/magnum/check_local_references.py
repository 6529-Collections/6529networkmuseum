"""Check local Markdown links and governed repository paths without network access."""

from __future__ import annotations

import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote


REPOSITORY = Path(__file__).resolve().parents[2]
ROOT = REPOSITORY / "records" / "proposed-gifts" / "6529NM-PG-2026-001" / "public" / "scholarship"
PUBLICATION_INVENTORY = REPOSITORY / "schemas" / "public-publication-inventory.json"
MARKDOWN_LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
CODE_SPAN = re.compile(r"`([^`]+)`")
ABSOLUTE_URI = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")
CANONICAL_PATH = re.compile(r"(?<![A-Za-z0-9_./-])(records/proposed-gifts/6529NM-PG-2026-001/[A-Za-z0-9_./-]+)")
GOVERNED_PREFIXES = (
    "records/",
    "docs/",
    "schemas/",
    "INDEX.md",
    "release-artifacts/",
    "content/",
    "notes/wip/",
    "scripts/",
)
FORBIDDEN_VISITOR_URI = re.compile(
    r"(?:https://(?:[^/\s.]+\.)*arweave\.net/|ar://)", re.IGNORECASE
)
COMPLETE_MANIFEST_ONLY_MARKERS = (
    "records/proposed-gifts/6529NM-PG-2026-001/proposal.json",
    "records/proposed-gifts/6529NM-PG-2026-001/wave-storm.json",
    "records/proposed-gifts/6529NM-PG-2026-001/public/wave-storm/",
    "records/proposed-gifts/6529NM-PG-2026-001/wave-publication-observation-2026-08-08.json",
    "records/proposed-gifts/6529NM-PG-2026-001/evidence/wave-publication-observation-public-safe-2026-08-09.json",
    "records/proposed-gifts/6529NM-PG-2026-001/media-description-amendment-2026-08-08.json",
    "/machine/",
)


def inside_repository(path: Path) -> bool:
    try:
        path.relative_to(REPOSITORY)
    except ValueError:
        return False
    return True


def publication_paths() -> set[str]:
    inventory = json.loads(PUBLICATION_INVENTORY.read_text(encoding="utf-8"))
    entries = inventory.get("entries")
    if not isinstance(entries, list):
        raise ValueError("public publication inventory has no entries array")
    paths = {
        entry.get("path")
        for entry in entries
        if isinstance(entry, dict) and isinstance(entry.get("path"), str)
    }
    if not paths:
        raise ValueError("public publication inventory has no declared paths")
    return paths


def check_visitor_document(
    source_relative: str,
    text: str,
    declared_paths: set[str],
    errors: list[str],
) -> int:
    """Reject one visitor document's links and complete-manifest disclosures."""

    if FORBIDDEN_VISITOR_URI.search(text):
        errors.append(
            f"{source_relative}: visitor manuscript exposes a governed Arweave metadata locator"
        )
    normalized_text = text.replace("\\", "/")
    for marker in COMPLETE_MANIFEST_ONLY_MARKERS:
        if marker in normalized_text:
            errors.append(
                f"{source_relative}: visitor manuscript names complete-manifest-only material: {marker}"
            )
    checked = 0
    source = REPOSITORY / Path(*source_relative.split("/"))
    for match in MARKDOWN_LINK.finditer(text):
        target = unquote(match.group(1).split("#", 1)[0].strip())
        if not target or ABSOLUTE_URI.match(target) or target.startswith("//"):
            continue
        resolved = (source.parent / target).resolve()
        if not inside_repository(resolved):
            continue
        checked += 1
        target_relative = resolved.relative_to(REPOSITORY).as_posix()
        if target_relative not in declared_paths:
            errors.append(
                f"{source_relative}: visitor link target is outside the public publication inventory: {target_relative}"
            )
    return checked


def check_visitor_boundary(
    files: list[Path],
    declared_paths: set[str],
    errors: list[str],
) -> int:
    """Reject links or path disclosures that escape the atomic visitor corpus."""

    checked = 0
    for source in files:
        source_relative = source.relative_to(REPOSITORY).as_posix()
        if source_relative not in declared_paths:
            continue
        checked += check_visitor_document(
            source_relative,
            source.read_text(encoding="utf-8"),
            declared_paths,
            errors,
        )
    return checked


def check_local_links(files: list[Path], errors: list[str]) -> int:
    checked = 0
    for source in files:
        text = source.read_text(encoding="utf-8")
        for match in MARKDOWN_LINK.finditer(text):
            target = unquote(match.group(1).split("#", 1)[0].strip())
            if not target or ABSOLUTE_URI.match(target) or target.startswith("//"):
                continue
            checked += 1
            resolved = (source.parent / target).resolve()
            if not inside_repository(resolved):
                errors.append(f"{source.relative_to(REPOSITORY)}: link escapes repository: {target}")
            elif not resolved.exists():
                errors.append(f"{source.relative_to(REPOSITORY)}: missing local link: {target}")
    return checked


def check_governed_paths(files: list[Path], errors: list[str]) -> int:
    checked = 0
    for source in files:
        text = source.read_text(encoding="utf-8")
        for token in CODE_SPAN.findall(text):
            candidate = token.strip().rstrip(".,;:")
            if not candidate.startswith(GOVERNED_PREFIXES) or "://" in candidate:
                continue
            checked += 1
            resolved = (REPOSITORY / candidate).resolve()
            if not inside_repository(resolved) or not resolved.exists():
                errors.append(f"{source.relative_to(REPOSITORY)}: missing governed path: {candidate}")
    return checked


def check_canonical_paths(files: list[Path], errors: list[str]) -> int:
    """Resolve every explicit canonical Magnum path, including JSON values."""

    checked = 0
    for source in files:
        text = source.read_text(encoding="utf-8")
        for match in CANONICAL_PATH.finditer(text):
            candidate = match.group(1).rstrip(".,;:)")
            checked += 1
            resolved = (REPOSITORY / candidate).resolve()
            if not inside_repository(resolved) or not resolved.exists():
                errors.append(f"{source.relative_to(REPOSITORY)}: missing canonical path: {candidate}")
    return checked


def main() -> int:
    files = sorted(path for path in ROOT.rglob("*") if path.suffix in {".md", ".json"})
    errors: list[str] = []
    try:
        declared_paths = publication_paths()
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"Local reference check failed to read publication inventory: {exc}", file=sys.stderr)
        return 1
    local_links = check_local_links(files, errors)
    source_register = ROOT / "sources" / "source-register.md"
    governed_files = [path for path in files if path != source_register]
    governed_paths = check_governed_paths(governed_files, errors)
    source_register_paths = check_governed_paths([source_register], errors)
    canonical_paths = check_canonical_paths(files, errors)
    visitor_links = check_visitor_boundary(files, declared_paths, errors)
    if errors:
        print("Local reference check failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(
        "Local reference check passed: "
        f"{local_links} relative links; {governed_paths} governed paths; "
        f"{source_register_paths} source-register paths; {canonical_paths} canonical paths; "
        f"{visitor_links} visitor-boundary links"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
