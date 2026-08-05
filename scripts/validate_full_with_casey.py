#!/usr/bin/env python3
"""Run the generic Museum validator and the completed Casey accession controls."""

from __future__ import annotations

import sys
from pathlib import Path

from validate import validate_records
from validate_casey_dossier import validate as validate_casey_dossier
from validate_data_architecture import validate as validate_data_architecture


ROOT = Path(__file__).resolve().parent.parent


def main() -> None:
    issues = validate_records(ROOT)
    issues.extend(validate_casey_dossier(ROOT))
    issues.extend(validate_data_architecture(ROOT))
    if issues:
        for issue in issues:
            print(f"error: {issue}", file=sys.stderr)
        raise SystemExit(1)
    print("Museum full validation passed, including the reviewed Casey accession, evidence controls, and data architecture.")


if __name__ == "__main__":
    main()
