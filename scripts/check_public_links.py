"""Check local Markdown links and anchors in the Keys and Gates corpus."""

from __future__ import annotations

import re
import sys
import unicodedata
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
PUBLIC_ROOT = ROOT / "records" / "programs" / "6529NM-AP-01" / "public"
LINK_RE = re.compile(r"!?(?:\[[^\]]*\])\(([^)\s]+)\)")
HEADING_RE = re.compile(r"^#{1,6}\s+(.+?)\s*$")
ANCHOR_RE = re.compile(r"""<a\s+[^>]*id=['"]([^'"]+)['"]""", re.IGNORECASE)


def github_slug(heading: str) -> str:
    heading = re.sub(r"<[^>]+>", "", heading)
    heading = re.sub(r"[*_~]", "", heading)
    heading = unicodedata.normalize("NFC", heading).lower()
    heading = re.sub(r"[^\w\s-]", "", heading, flags=re.UNICODE)
    return re.sub(r"\s+", "-", heading).strip("-")


def anchors_for(path: Path) -> set[str]:
    text = path.read_text(encoding="utf-8")
    anchors = set(ANCHOR_RE.findall(text))
    for line in text.splitlines():
        match = HEADING_RE.match(line)
        if match:
            anchors.add(github_slug(match.group(1)))
    return anchors


def check_links(root: Path = PUBLIC_ROOT) -> list[str]:
    errors: list[str] = []
    checked = 0
    for source in sorted(root.rglob("*.md")):
        text = source.read_text(encoding="utf-8")
        for raw_target in LINK_RE.findall(text):
            target = unquote(raw_target.strip("<>"))
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc:
                continue
            checked += 1
            fragment = parsed.fragment
            relative = parsed.path
            destination = source.parent / relative if relative else source
            try:
                destination = destination.resolve().relative_to(ROOT).as_posix()
            except ValueError:
                errors.append(f"{source.relative_to(ROOT)} escapes repository: {target}")
                continue
            destination_path = ROOT / destination
            if not destination_path.exists():
                errors.append(
                    f"{source.relative_to(ROOT)} points to missing file: {target}"
                )
                continue
            if fragment and not destination_path.is_file():
                errors.append(
                    f"{source.relative_to(ROOT)} points to an anchor on a directory: {target}"
                )
                continue
            if fragment and fragment not in anchors_for(destination_path):
                errors.append(
                    f"{source.relative_to(ROOT)} points to missing anchor: {target}"
                )
    if not errors:
        print(f"local public link/anchor check passed ({checked} local targets)")
    return errors


def main() -> int:
    errors = check_links()
    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
