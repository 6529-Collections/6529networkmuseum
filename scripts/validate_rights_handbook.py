#!/usr/bin/env python3
"""Validate the public rights handbook, registry, sources, and object links."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = Path("docs/rights/registry.json")
SCHEMA_PATH = Path("schemas/rights-expression-registry.schema.json")
GUIDE_PATHS = (
    Path("records/institutional-practice/rights-and-licenses.md"),
    Path("records/institutional-practice/rights-for-artists.md"),
    Path("records/institutional-practice/rights-for-collectors.md"),
)
EXPECTED_CC = {
    "cc-by-4.0",
    "cc-by-sa-4.0",
    "cc-by-nd-4.0",
    "cc-by-nc-4.0",
    "cc-by-nc-sa-4.0",
    "cc-by-nc-nd-4.0",
}
EXPECTED_RIGHTS_STATEMENTS = {
    "rightsstatements-inc",
    "rightsstatements-inc-ow-eu",
    "rightsstatements-inc-edu",
    "rightsstatements-inc-nc",
    "rightsstatements-inc-ruu",
    "rightsstatements-noc-cr",
    "rightsstatements-noc-nc",
    "rightsstatements-noc-oklr",
    "rightsstatements-noc-us",
    "rightsstatements-cne",
    "rightsstatements-und",
    "rightsstatements-nkc",
}
EXPECTED_CASEY_OBJECTS = {
    f"6529NM.2026.001.{index:02d}" for index in range(1, 8)
}


class DuplicateJsonKeyError(ValueError):
    pass


def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateJsonKeyError(f"duplicate JSON key: {key!r}")
        result[key] = value
    return result


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle, object_pairs_hook=reject_duplicate_keys)


def format_schema_error(error: Any) -> str:
    location = "/".join(str(part) for part in error.absolute_path) or "$"
    return f"{location}: {error.message}"


def validate(root: Path = ROOT) -> list[str]:
    issues: list[str] = []
    registry_path = root / REGISTRY_PATH
    schema_path = root / SCHEMA_PATH
    try:
        registry = load_json(registry_path)
        schema = load_json(schema_path)
    except (OSError, json.JSONDecodeError, DuplicateJsonKeyError) as exc:
        return [f"rights registry or schema is unreadable: {exc}"]

    schema_errors = sorted(
        Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(registry),
        key=lambda error: list(error.absolute_path),
    )
    issues.extend(format_schema_error(error) for error in schema_errors)
    if schema_errors or not isinstance(registry, dict):
        return issues

    expressions = registry.get("expressions", [])
    if not isinstance(expressions, list) or not all(isinstance(item, dict) for item in expressions):
        return issues + ["expressions must be an array of objects"]
    ids = [item.get("id") for item in expressions]
    if len(ids) != len(set(ids)):
        issues.append("rights expression ids must be unique")
    by_id = {item.get("id"): item for item in expressions if isinstance(item.get("id"), str)}
    if {item_id for item_id, item in by_id.items() if item.get("group") == "creative_commons_license"} != EXPECTED_CC:
        issues.append("registry must contain exactly the six Creative Commons 4.0 licenses")
    if {item_id for item_id, item in by_id.items() if item.get("group") == "rights_statement"} != EXPECTED_RIGHTS_STATEMENTS:
        issues.append("registry must contain exactly the twelve RightsStatements.org 1.0 terms")
    for required_id in ("cc0-1.0", "public-domain-mark-1.0", "in-copyright-no-public-license", "custom-license"):
        if required_id not in by_id:
            issues.append(f"registry is missing required expression {required_id}")

    declared_legal_paths: set[str] = set()
    for expression_id, expression in by_id.items():
        legal_code = expression.get("legal_code")
        needs_legal_code = expression.get("group") == "creative_commons_license" or expression_id == "cc0-1.0"
        if needs_legal_code != isinstance(legal_code, dict):
            issues.append(f"{expression_id}: legal-code presence does not match instrument type")
            continue
        if not isinstance(legal_code, dict):
            continue
        relative = legal_code.get("path")
        expected_hash = legal_code.get("sha256")
        if not isinstance(relative, str) or not isinstance(expected_hash, str):
            continue
        if relative in declared_legal_paths:
            issues.append(f"{expression_id}: legal text path is reused: {relative}")
        declared_legal_paths.add(relative)
        path = (root / relative).resolve()
        legal_root = (root / "docs/rights/legal-texts").resolve()
        if not path.is_relative_to(legal_root) or not path.is_file():
            issues.append(f"{expression_id}: legal text is missing or escapes its directory: {relative}")
            continue
        actual_hash = "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()
        if actual_hash != expected_hash:
            issues.append(f"{expression_id}: legal text digest mismatch; expected {expected_hash}, got {actual_hash}")
        source_uri = legal_code.get("source_uri", "")
        pinned_commit = registry.get("sources", {}).get("creative_commons_data_commit", "")
        if f"/{pinned_commit}/" not in source_uri:
            issues.append(f"{expression_id}: legal source URI is not pinned to the declared Creative Commons commit")

    legal_dir = root / "docs/rights/legal-texts"
    actual_legal_paths = {
        path.relative_to(root).as_posix() for path in legal_dir.glob("*.txt")
    } if legal_dir.is_dir() else set()
    if actual_legal_paths != declared_legal_paths:
        issues.append(
            "legal text inventory differs from registry: "
            f"declared {sorted(declared_legal_paths)}, found {sorted(actual_legal_paths)}"
        )

    assignments = registry.get("object_assignments", [])
    assignment_ids = [item.get("object_id") for item in assignments if isinstance(item, dict)]
    if set(assignment_ids) != EXPECTED_CASEY_OBJECTS or len(assignment_ids) != len(EXPECTED_CASEY_OBJECTS):
        issues.append("object assignments must cover each Casey accession object exactly once")
    for assignment in assignments:
        if not isinstance(assignment, dict):
            continue
        object_id = assignment.get("object_id")
        expression_id = assignment.get("expression_id")
        rights_path_value = assignment.get("rights_record_path")
        if expression_id not in by_id:
            issues.append(f"{object_id}: unknown rights expression {expression_id!r}")
        if expression_id != "cc-by-nc-4.0":
            issues.append(f"{object_id}: Casey rights assignment must match reviewed CC BY-NC 4.0 record")
        if not isinstance(rights_path_value, str):
            continue
        rights_path = (root / rights_path_value).resolve()
        accessions_root = (root / "records" / "accessions").resolve()
        if not rights_path.is_relative_to(accessions_root) or not rights_path.is_file():
            issues.append(f"{object_id}: rights record is missing or escapes records/: {rights_path_value}")
            continue
        try:
            rights_record = load_json(rights_path)
        except (OSError, json.JSONDecodeError, DuplicateJsonKeyError) as exc:
            issues.append(f"{object_id}: rights record is unreadable: {exc}")
            continue
        payload = rights_record.get("payload", {}) if isinstance(rights_record, dict) else {}
        if payload.get("object_id") != object_id:
            issues.append(f"{object_id}: rights record object_id does not match assignment")
        rights_text = " ".join(
            str(payload.get(key, "")) for key in ("basis", "rights_holder_reference")
        )
        if "CC BY-NC 4.0" not in rights_text:
            issues.append(f"{object_id}: rights record does not state assigned CC BY-NC 4.0 basis")

    program_notes = registry.get("program_notes", [])
    if len(program_notes) != 1 or program_notes[0].get("program_id") != "6529NM-AP-01":
        issues.append("registry must retain one Keys and Gates program-level rights note")
    elif program_notes[0].get("effective_status") != "conditional_not_yet_effective":
        issues.append("Keys and Gates CC0 intention must remain conditional before mint")

    expected_titles = (
        "# Rights in digital art",
        "# Rights for artists",
        "# Rights for collectors",
    )
    for relative, expected_title in zip(GUIDE_PATHS, expected_titles, strict=True):
        path = root / relative
        if not path.is_file():
            issues.append(f"missing public guide: {relative.as_posix()}")
            continue
        text = path.read_text(encoding="utf-8")
        if not text.startswith(expected_title + "\n"):
            issues.append(f"{relative.as_posix()}: expected title {expected_title!r}")
    return issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args(argv)
    issues = validate(args.root.resolve())
    if issues:
        print("Rights handbook validation failed:")
        print("\n".join(f"- {issue}" for issue in issues))
        return 1
    print("Rights handbook validation passed: 22 expressions, 7 legal texts, 7 object links, and 3 public guides are consistent.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
