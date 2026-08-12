"""Check local Markdown links and governed repository paths without network access."""

from __future__ import annotations

from html import unescape as html_unescape
import json
from pathlib import Path
import posixpath
import re
import sys
from urllib.parse import unquote, urlsplit


REPOSITORY = Path(__file__).resolve().parents[2]
ROOT = REPOSITORY / "records" / "proposed-gifts" / "6529NM-PG-2026-001" / "public" / "scholarship"
PUBLICATION_INVENTORY = REPOSITORY / "schemas" / "public-publication-inventory.json"
MEDIA_JOIN = ROOT / "machine" / "wave-media-join.json"
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
WEB_LOCATOR = re.compile(
    r"(?=((?:https?:[\\/]*|[\\/]{2})[^\s<>'\"\)\]]+))", re.IGNORECASE
)
AR_URI = re.compile(r"(?<![A-Za-z0-9+.-])ar:", re.IGNORECASE)
MARKDOWN_ESCAPE = re.compile(r"\\([!\"#$%&'()*+,\-./:;<=>?@\[\]^_`{|}~])")
ASCII_CONTROL = re.compile(r"[\x00-\x1f\x7f]")
COMPLETE_MANIFEST_ONLY_MARKERS = (
    "records/proposed-gifts/6529NM-PG-2026-001/proposal.json",
    "records/proposed-gifts/6529NM-PG-2026-001/wave-storm.json",
    "records/proposed-gifts/6529NM-PG-2026-001/public/wave-storm/",
    "records/proposed-gifts/6529NM-PG-2026-001/wave-publication-observation-2026-08-08.json",
    "records/proposed-gifts/6529NM-PG-2026-001/evidence/wave-publication-observation-public-safe-2026-08-09.json",
    "records/proposed-gifts/6529NM-PG-2026-001/media-description-amendment-2026-08-08.json",
    "/machine/",
)
VISITOR_MACHINE_CONTROL_PATHS = frozenset(
    {
        "records/proposed-gifts/6529NM-PG-2026-001/public/scholarship/machine/"
        "media-source-continuity-amendment.json"
    }
)


def inside_repository(path: Path) -> bool:
    try:
        path.relative_to(REPOSITORY)
    except ValueError:
        return False
    return True


def fully_unquote(value: str) -> str:
    """Decode bounded nested percent-encoding without accepting an infinite rewrite."""

    decoded = value
    for _ in range(3):
        candidate = unquote(decoded)
        if candidate == decoded:
            break
        decoded = candidate
    return decoded


def canonical_web_locator(value: str) -> tuple[str, int | None, str] | None:
    """Return a scheme-insensitive, browser-equivalent HTTP(S) locator key."""

    candidate = html_unescape(value.strip().strip("<>")).rstrip(".,;!?")
    candidate = candidate.replace("\\", "/")
    if candidate.startswith("//"):
        candidate = "https:" + candidate
    candidate = re.sub(
        r"^(https?):/*", r"\1://", candidate, count=1, flags=re.IGNORECASE
    )
    try:
        parsed = urlsplit(candidate)
        if parsed.scheme.casefold() not in {"http", "https"}:
            return None
        host = fully_unquote(parsed.hostname or "").rstrip(".").casefold()
        if not host or any(
            ord(character) <= 32 or character in "/\\?#@" for character in host
        ):
            return None
        # IDNA maps browser-equivalent Unicode label separators such as U+3002,
        # U+FF0E, and U+FF61 to ASCII dots. Strip the DNS root marker only
        # after that mapping so every trailing-dot spelling canonicalizes to
        # the same host key.
        host = host.encode("idna").decode("ascii").rstrip(".")
        if not host:
            return None
        port = parsed.port
    except (UnicodeError, ValueError):
        return None
    if port in {80, 443}:
        port = None
    decoded_path = fully_unquote(parsed.path or "/")
    path = posixpath.normpath("/" + decoded_path.lstrip("/"))
    if decoded_path.endswith("/") and not path.endswith("/"):
        path += "/"
    return host, port, path


def decoded_text_variants(text: str) -> set[str]:
    """Return browser- and CommonMark-equivalent text representations."""

    decoded_text = fully_unquote(html_unescape(text))
    # Browsers discard ASCII tab/newline characters during URL parsing and
    # trim other C0 controls at URL boundaries. A fail-closed visitor gate
    # removes the complete control set (plus DEL) before comparison so a
    # restricted locator cannot acquire a distinct key through control bytes.
    browser_compacted_text = ASCII_CONTROL.sub("", decoded_text)
    markdown_unescaped_text = MARKDOWN_ESCAPE.sub(r"\1", browser_compacted_text)
    return {
        text,
        decoded_text,
        browser_compacted_text,
        markdown_unescaped_text,
    }


def contains_ar_uri(text: str) -> bool:
    return any(AR_URI.search(candidate) for candidate in decoded_text_variants(text))


def decoded_markdown_target(value: str) -> str:
    """Decode one Markdown target before URI or local-path classification."""

    target = value.split("#", 1)[0].strip()
    target = fully_unquote(html_unescape(target))
    return MARKDOWN_ESCAPE.sub(r"\1", target)


def web_locators(text: str) -> list[tuple[str, int | None, str]]:
    locators: set[tuple[str, int | None, str]] = set()
    for candidate_text in decoded_text_variants(text):
        for match in WEB_LOCATOR.finditer(candidate_text):
            locator = canonical_web_locator(match.group(1))
            if locator is not None:
                locators.add(locator)
    return sorted(locators)


def publication_paths() -> set[str]:
    inventory = json.loads(PUBLICATION_INVENTORY.read_text(encoding="utf-8"))
    if not isinstance(inventory, dict):
        raise ValueError("public publication inventory is not an object")
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


def restricted_media_locators() -> set[tuple[str, int | None, str]]:
    join = json.loads(MEDIA_JOIN.read_text(encoding="utf-8"))
    if not isinstance(join, dict):
        raise ValueError("Magnum media join is not an object")
    works = join.get("works")
    if not isinstance(works, list):
        raise ValueError("Magnum media join has no works array")
    urls = {
        url
        for row in works
        if isinstance(row, dict)
        for url in (row.get("token_source_image_url"), row.get("wave_media_url"))
        if isinstance(url, str) and url
    }
    locators = {
        locator
        for url in urls
        if (locator := canonical_web_locator(url)) is not None
    }
    if not locators:
        raise ValueError("Magnum media join has no restricted media locators")
    return locators


def check_visitor_document(
    source_relative: str,
    text: str,
    declared_paths: set[str],
    errors: list[str],
    restricted_locators: set[tuple[str, int | None, str]] | None = None,
) -> int:
    """Reject one visitor document's links and complete-manifest disclosures."""

    locators = web_locators(text)
    if restricted_locators is None:
        restricted_locators = restricted_media_locators()
    is_machine_control = source_relative in VISITOR_MACHINE_CONTROL_PATHS
    if not is_machine_control:
        if contains_ar_uri(text) or any(
            host == "arweave.net" or host.endswith(".arweave.net")
            for host, _, _ in locators
        ):
            errors.append(
                f"{source_relative}: visitor manuscript exposes a governed Arweave metadata locator"
            )
        if any(locator in restricted_locators for locator in locators):
            errors.append(
                f"{source_relative}: visitor manuscript exposes a restricted direct photograph locator"
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
        target = decoded_markdown_target(match.group(1))
        if ASCII_CONTROL.search(target):
            errors.append(
                f"{source_relative}: visitor link target contains an ASCII control character"
            )
            continue
        if not target or ABSOLUTE_URI.match(target) or target.startswith("//"):
            continue
        try:
            resolved = (source.parent / target).resolve()
        except (OSError, RuntimeError, ValueError):
            errors.append(f"{source_relative}: visitor link target is not a valid path")
            continue
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
    restricted_locators: set[tuple[str, int | None, str]] | None = None,
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
            restricted_locators,
        )
    return checked


def check_local_links(files: list[Path], errors: list[str]) -> int:
    checked = 0
    for source in files:
        text = source.read_text(encoding="utf-8")
        for match in MARKDOWN_LINK.finditer(text):
            target = decoded_markdown_target(match.group(1))
            if ASCII_CONTROL.search(target):
                errors.append(
                    f"{source.relative_to(REPOSITORY)}: link target contains an ASCII control character"
                )
                continue
            if not target or ABSOLUTE_URI.match(target) or target.startswith("//"):
                continue
            checked += 1
            try:
                resolved = (source.parent / target).resolve()
            except (OSError, RuntimeError, ValueError):
                errors.append(
                    f"{source.relative_to(REPOSITORY)}: invalid local link: {target!r}"
                )
                continue
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
        restricted_locators = restricted_media_locators()
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"Local reference check failed to read publication controls: {exc}", file=sys.stderr)
        return 1
    local_links = check_local_links(files, errors)
    source_register = ROOT / "sources" / "source-register.md"
    governed_files = [path for path in files if path != source_register]
    governed_paths = check_governed_paths(governed_files, errors)
    source_register_paths = check_governed_paths([source_register], errors)
    canonical_paths = check_canonical_paths(files, errors)
    visitor_links = check_visitor_boundary(
        files, declared_paths, errors, restricted_locators
    )
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
