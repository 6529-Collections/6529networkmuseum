"""Check local Markdown links and governed repository paths without network access."""

from __future__ import annotations

from pathlib import Path
import re
import sys
from urllib.parse import unquote


REPOSITORY = Path(__file__).resolve().parents[3]
ROOT = REPOSITORY / "records" / "proposed-gifts" / "6529NM-PG-2026-001" / "public" / "scholarship"
MARKDOWN_LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
CODE_SPAN = re.compile(r"`([^`]+)`")
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


def inside_repository(path: Path) -> bool:
    try:
        path.relative_to(REPOSITORY)
    except ValueError:
        return False
    return True


def check_local_links(files: list[Path], errors: list[str]) -> int:
    checked = 0
    for source in files:
        text = source.read_text(encoding="utf-8")
        for match in MARKDOWN_LINK.finditer(text):
            target = unquote(match.group(1).split("#", 1)[0].strip())
            if not target or target.startswith(("http://", "https://", "mailto:", "//")):
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
    local_links = check_local_links(files, errors)
    source_register = ROOT / "sources" / "source-register.md"
    governed_files = [path for path in files if path != source_register]
    governed_paths = check_governed_paths(governed_files, errors)
    source_register_paths = check_governed_paths([source_register], errors)
    canonical_paths = check_canonical_paths(files, errors)
    if errors:
        print("Local reference check failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(
        "Local reference check passed: "
        f"{local_links} relative links; {governed_paths} governed paths; "
        f"{source_register_paths} source-register paths; {canonical_paths} canonical paths"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
