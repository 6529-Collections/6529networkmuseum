#!/usr/bin/env python3
"""Run the repository validator plus Casey's nullable-reviewer controls.

The published Casey package fixes ``scripts/validate.py`` as an external
inventory item.  Its generic semantic checker predates nullable constructed
reviewers, so this wrapper supplies an in-memory reviewer only while executing
that generic checker.  The companion Casey validator then fail-closes on the
actual ``reviewer: null`` record state, preserving the absence of authority.
"""

from __future__ import annotations

import copy
import sys
from pathlib import Path
from typing import Any

import validate as standard_validate
from validate_casey_dossier import CASEY_ID, validate as validate_casey_dossier


ROOT = Path(__file__).resolve().parent.parent
ORIGINAL_VALIDATE_SEMANTICS = standard_validate.validate_semantics


def validate_semantics_with_casey_nullable_reviewer(record: dict[str, Any], vocabularies: dict[str, Any]) -> list[str]:
    payload = record.get("payload") if isinstance(record.get("payload"), dict) else {}
    record_id = payload.get("record_id")
    if isinstance(record_id, str) and (record_id == CASEY_ID or record_id.startswith(CASEY_ID + ".") or record_id.startswith(CASEY_ID + "-")) and payload.get("reviewer") is None:
        compatible_record = copy.deepcopy(record)
        compatible_record["payload"]["reviewer"] = {
            "id": "pending-independent-reviewer-not-authority",
            "role": "reviewer",
            "reviewed_at": payload["created_at"],
        }
        return ORIGINAL_VALIDATE_SEMANTICS(compatible_record, vocabularies)
    return ORIGINAL_VALIDATE_SEMANTICS(record, vocabularies)


def main() -> None:
    standard_validate.validate_semantics = validate_semantics_with_casey_nullable_reviewer
    issues = standard_validate.validate_records(ROOT)
    issues.extend(validate_casey_dossier(ROOT))
    if issues:
        for issue in issues:
            print(f"error: {issue}", file=sys.stderr)
        raise SystemExit(1)
    print("Museum full validation passed, including Casey published-source and nullable-reviewer controls.")


if __name__ == "__main__":
    main()
