"""Command-line entry point for transparent NextGen-compatible analysis."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

try:
    from .nextgen_compat import InputError, analyze_snapshot, load_snapshot
except ImportError:  # pragma: no cover - supports direct script execution
    from nextgen_compat import InputError, analyze_snapshot, load_snapshot


DATA_ERROR_EXIT = 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Analyze a dated JSON trait snapshot with the pinned 6529 NextGen "
            "trait-prevalence algorithm."
        )
    )
    parser.add_argument("snapshot", type=Path, help="input JSON snapshot")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="write the analysis JSON here instead of stdout",
    )
    parser.add_argument(
        "--duplicates",
        choices=("error", "preserve", "deduplicate"),
        default="error",
        help=(
            "duplicate handling: error by default; preserve mirrors raw-row "
            "source arithmetic; deduplicate is explicit preprocessing"
        ),
    )
    args = parser.parse_args(argv)

    try:
        result = analyze_snapshot(
            load_snapshot(args.snapshot), duplicate_policy=args.duplicates
        )
    except (OSError, UnicodeError, json.JSONDecodeError, InputError) as error:
        print(f"error: {error}", file=sys.stderr)
        return DATA_ERROR_EXIT

    encoded = json.dumps(
        result, ensure_ascii=False, indent=2, sort_keys=False
    ) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded, encoding="utf-8", newline="\n")
    else:
        sys.stdout.write(encoded)
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
