"""Run deterministic editorial and citation checks over the public Magnum corpus.

The check is local only. It includes dossiers and the source register because
both are intended for public research publication; machine records, review
scripts, and the construction README are excluded from visitor-copy tests.
"""

from __future__ import annotations

from pathlib import Path
import re
import sys


REPOSITORY = Path(__file__).resolve().parents[3]
ROOT = REPOSITORY / "records" / "proposed-gifts" / "6529NM-PG-2026-001" / "public" / "scholarship"
PUBLIC_DIRS = tuple(ROOT / name for name in ("entities", "artists", "works", "essays", "dossiers", "sources"))
SOURCE_REGISTER = ROOT / "sources" / "source-register.md"
FOOTNOTE_REF = re.compile(r"\[\^([^\]]+)\](?!:)")
FOOTNOTE_DEF = re.compile(r"^\[\^([^\]]+)\]:", re.MULTILINE)
SOURCE_ID = re.compile(r"\bS\d{2}\b")

FORBIDDEN_COPY = (
    "The The",
    "the the",
    "status-bound",
    "active Museum publication layer",
    "not a title instrument",
    "public page architecture",
    "decision boundary",
    "through the machine join",
    "frontend must",
    "The Museum should",
    "Public Work entity ID assigned by an earlier integration lane",
    "proposed five-work gift",
    "five proposed Works",
    "Why consider the gift",
)


def public_files() -> list[Path]:
    return sorted(path for directory in PUBLIC_DIRS for path in directory.rglob("*.md"))


def source_ids() -> set[str]:
    return set(SOURCE_ID.findall(SOURCE_REGISTER.read_text(encoding="utf-8")))


def check_footnotes(path: Path, text: str, errors: list[str]) -> None:
    definitions = set(FOOTNOTE_DEF.findall(text))
    references = set(FOOTNOTE_REF.findall(text))
    undefined = sorted(references - definitions)
    unused = sorted(definitions - references)
    if undefined:
        errors.append(f"{path.relative_to(ROOT)}: undefined footnotes {', '.join(undefined)}")
    if unused:
        errors.append(f"{path.relative_to(ROOT)}: orphaned footnotes {', '.join(unused)}")


def check_sources(path: Path, text: str, available: set[str], errors: list[str]) -> None:
    if path == SOURCE_REGISTER:
        return
    missing = sorted(set(SOURCE_ID.findall(text)) - available)
    if missing:
        errors.append(f"{path.relative_to(ROOT)}: source IDs absent from source register: {', '.join(missing)}")


def check_current_language(path: Path, text: str, errors: list[str]) -> None:
    for phrase in FORBIDDEN_COPY:
        if phrase in text:
            errors.append(f"{path.relative_to(ROOT)}: stale/process copy: {phrase}")


def check_work_artist_prose(path: Path, text: str, errors: list[str]) -> None:
    """Keep pixel/process language in plainly labelled technical records."""

    if path.parent.name not in {"works", "artists"}:
        return
    if re.search(r"\bthe\s+pixels\s+(?:show|reveal|prove|demonstrate)\b", text, flags=re.IGNORECASE):
        errors.append(f"{path.relative_to(ROOT)}: close-looking prose must describe the image or visible evidence, not pixels")


def check_required_sources(all_text: str, errors: list[str]) -> None:
    required = (
        "https://whc.unesco.org/en/list/23/",
        "https://whc.unesco.org/document/142423",
        "https://whc.unesco.org/en/news/1488",
        "https://store.magnumphotos.com/products/fine-print-tripoli-libya-2011",
        "https://gostbooks.com/products/we-dont-say-goodbye",
        "https://www.visapourlimage.com/files/a4c041c3/press_release_2017.pdf",
        "https://artwindsoressex.ca/collection/advanced-search/?artists=87344",
    )
    for url in required:
        if url not in all_text:
            errors.append(f"source register/public corpus is missing required locator: {url}")
    if "retained excerpt" not in all_text or "page-state" not in all_text:
        errors.append("unstable TIME/AFP access sources require retained-excerpt and page-state caveats")


def check_copy_citations() -> list[str]:
    errors: list[str] = []
    files = public_files()
    available = source_ids()
    texts: list[str] = []
    for path in files:
        text = path.read_text(encoding="utf-8")
        texts.append(text)
        check_footnotes(path, text, errors)
        check_sources(path, text, available, errors)
        check_current_language(path, text, errors)
        check_work_artist_prose(path, text, errors)

    all_text = "\n".join(texts)
    check_required_sources(all_text, errors)

    narrative = ROOT / "essays" / "acquisition-narrative.md"
    narrative_text = narrative.read_text(encoding="utf-8")
    if "## How the selected offer was formed" not in narrative_text:
        errors.append("acquisition narrative must use the selected-offer heading")
    if "The acquisition record would preserve" not in narrative_text:
        errors.append("acquisition narrative must use grammatical positive registrar language")

    work_text = "\n".join((ROOT / "works").joinpath(name).read_text(encoding="utf-8") for name in (
        "01-david-seymour-127.md", "02-larry-towell-145.md", "03-micha-bar-am-97.md",
        "04-moises-saman-44.md", "05-lorenzo-meloni-104.md",
    ))
    if re.search(r"tear\s+gas", work_text, flags=re.IGNORECASE):
        errors.append("public Work prose must not infer tear gas")
    if "The image shows a person" not in (ROOT / "works" / "03-micha-bar-am-97.md").read_text(encoding="utf-8"):
        errors.append("Bar-Am close-looking copy must use image/visible-evidence language")
    if "Moisés Saman" not in all_text or "Moises Saman" not in all_text:
        errors.append("Saman display accent and raw issuer spelling must both remain available")
    if "selected five-work gift" in all_text.lower() or "five proposed works" in all_text.lower():
        errors.append("current public prose must use selected offer language")
    return errors


def main() -> int:
    errors = check_copy_citations()
    if errors:
        print("WP-3 copy/citation check failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(f"WP-3 copy/citation check passed: {len(public_files())} public Markdown files; footnotes, source IDs, current-state language, and required locators verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
