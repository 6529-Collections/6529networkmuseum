#!/usr/bin/env python3
"""Write or verify pinned English Creative Commons legal-code snapshots."""

from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

from safe_fetch import FetchPolicyError, SafeHTTPSFetcher

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT / "docs" / "rights" / "legal-texts"
CC_DATA_REVISION = "22fc2c31d0297a1feb8a257c0e6f84e95c9a38ae"
CC_DATA_ROOT = (
    "https://raw.githubusercontent.com/creativecommons/cc-legal-tools-data/"
    f"{CC_DATA_REVISION}/docs"
)

SOURCES = {
    "cc-by-4.0.txt": (
        f"{CC_DATA_ROOT}/licenses/by/4.0/legalcode.txt",
        "9ba9550ad48438d0836ddab3da480b3b69ffa0aac7b7878b5a0039e7ab429411",
    ),
    "cc-by-sa-4.0.txt": (
        f"{CC_DATA_ROOT}/licenses/by-sa/4.0/legalcode.txt",
        "28a9529c7d0bb4dc51f4bf5c116a3d16ef247a052f7591466768ddf563fd1cf5",
    ),
    "cc-by-nd-4.0.txt": (
        f"{CC_DATA_ROOT}/licenses/by-nd/4.0/legalcode.txt",
        "9cc97638cf0185884ac800144b6246c7772f94ff2cc70686afa9574aaea4fa2b",
    ),
    "cc-by-nc-4.0.txt": (
        f"{CC_DATA_ROOT}/licenses/by-nc/4.0/legalcode.txt",
        "41003d4a74749c0220e33dd415042164b5a1093ed401f36277234f772d22d3d0",
    ),
    "cc-by-nc-sa-4.0.txt": (
        f"{CC_DATA_ROOT}/licenses/by-nc-sa/4.0/legalcode.txt",
        "e66c269d4819aaab34b49ef5220c4ddab6756f21bb5180761a4eb8561f2b7bbd",
    ),
    "cc-by-nc-nd-4.0.txt": (
        f"{CC_DATA_ROOT}/licenses/by-nc-nd/4.0/legalcode.txt",
        "38762e3777f4ec00a6f769062a7c3f704fb78ce08303ecff88558da4c49cf9ea",
    ),
    "cc0-1.0.txt": (
        f"{CC_DATA_ROOT}/publicdomain/zero/1.0/legalcode.txt",
        "a2010f343487d3f7618affe54f789f5487602331c0a8d03f49e9a7c547cf0499",
    ),
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def check_local() -> list[str]:
    issues: list[str] = []
    expected_names = set(SOURCES)
    actual_names = {path.name for path in OUTPUT_DIR.glob("*.txt")} if OUTPUT_DIR.is_dir() else set()
    if actual_names != expected_names:
        issues.append(
            "legal-text inventory differs: "
            f"expected {sorted(expected_names)}, found {sorted(actual_names)}"
        )
    for name, (_url, expected_hash) in SOURCES.items():
        path = OUTPUT_DIR / name
        if not path.is_file():
            issues.append(f"missing legal text: {path.relative_to(ROOT).as_posix()}")
            continue
        actual_hash = sha256(path.read_bytes())
        if actual_hash != expected_hash:
            issues.append(f"{name}: expected sha256:{expected_hash}, got sha256:{actual_hash}")
    return issues


def fetch_and_write() -> None:
    fetcher = SafeHTTPSFetcher()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for name, (url, expected_hash) in SOURCES.items():
        result = fetcher.fetch(
            url,
            headers={
                "Accept": "text/plain",
                "User-Agent": "6529-Network-Museum-rights-source-sync/1.0",
            },
        )
        if result.observation.status != 200:
            raise FetchPolicyError(f"{url}: expected HTTP 200, got {result.observation.status}")
        if result.observation.media_type != "text/plain":
            raise FetchPolicyError(
                f"{url}: expected text/plain, got {result.observation.media_type}"
            )
        actual_hash = sha256(result.body)
        if actual_hash != expected_hash:
            raise FetchPolicyError(
                f"{url}: upstream bytes changed; expected sha256:{expected_hash}, "
                f"got sha256:{actual_hash}"
            )
        (OUTPUT_DIR / name).write_bytes(result.body)
        print(f"wrote {name} sha256:{actual_hash}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--write",
        action="store_true",
        help="fetch official sources through the repository safe-fetch transport and write snapshots",
    )
    args = parser.parse_args(argv)
    try:
        if args.write:
            fetch_and_write()
        issues = check_local()
    except (OSError, FetchPolicyError) as exc:
        print(f"rights legal-text sync failed: {exc}")
        return 1
    if issues:
        print("rights legal-text verification failed:")
        print("\n".join(f"- {issue}" for issue in issues))
        return 1
    print(f"Rights legal-text verification passed ({len(SOURCES)} pinned texts).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
