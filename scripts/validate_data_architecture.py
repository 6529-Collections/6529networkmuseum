#!/usr/bin/env python3
"""Validate the Museum data architecture and Casey implementation schedule."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parent.parent
PROFILE_PATH = Path("docs/data-architecture/profile.json")
PROFILE_SCHEMA_PATH = Path("schemas/museum-data-architecture-profile.schema.json")
CASEY_SCHEDULE_PATH = Path("docs/data-architecture/casey-reas-machine-schedule.json")
CASEY_SCHEMA_PATH = Path("schemas/museum-data-architecture-case-study.schema.json")
CASEY_OBJECT_ROOT = Path("records/accessions/6529NM.2026.001/objects")
RELEASE_MANIFEST_PATH = Path("release-artifacts/latest/record-manifest.json")

STANDARD_SLUGS = (
    "spectrum",
    "cidoc-crm",
    "lido",
    "premis",
    "prov-o",
    "getty-aat-ulan",
    "iiif",
    "c2pa",
    "bagit",
    "ocfl",
    "caip-19",
)

EXPECTED_TITLES = {
    "spectrum": "# Spectrum 5.1:",
    "cidoc-crm": "# CIDOC CRM:",
    "lido": "# LIDO:",
    "premis": "# PREMIS:",
    "prov-o": "# PROV-O:",
    "getty-aat-ulan": "# Getty AAT and ULAN:",
    "iiif": "# IIIF:",
    "c2pa": "# C2PA:",
    "bagit": "# BagIt:",
    "ocfl": "# OCFL:",
    "caip-19": "# CAIP-19:",
}


class DuplicateJsonKeyError(ValueError):
    pass


def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateJsonKeyError(f"duplicate JSON object key: {key!r}")
        result[key] = value
    return result


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicate_keys)


def schema_issues(instance: Any, schema: Any, location: str) -> list[str]:
    issues: list[str] = []
    try:
        Draft202012Validator.check_schema(schema)
        validator = Draft202012Validator(schema, format_checker=FormatChecker())
        for error in sorted(validator.iter_errors(instance), key=lambda item: list(item.absolute_path)):
            path = "".join(f"[{part!r}]" if isinstance(part, int) else f".{part}" for part in error.absolute_path)
            issues.append(f"{location}{path}: {error.message}")
    except Exception as exc:
        issues.append(f"{location}: schema evaluation failure: {exc}")
    return issues


def validate(root: Path = ROOT) -> list[str]:
    issues: list[str] = []
    try:
        profile = load_json(root / PROFILE_PATH)
        profile_schema = load_json(root / PROFILE_SCHEMA_PATH)
        schedule = load_json(root / CASEY_SCHEDULE_PATH)
        schedule_schema = load_json(root / CASEY_SCHEMA_PATH)
    except Exception as exc:
        return [f"Museum data architecture JSON load failure: {exc}"]

    issues.extend(schema_issues(profile, profile_schema, PROFILE_PATH.as_posix()))
    issues.extend(schema_issues(schedule, schedule_schema, CASEY_SCHEDULE_PATH.as_posix()))
    if issues:
        return issues

    standards = profile["standards"]
    slugs = tuple(standard["slug"] for standard in standards)
    if slugs != STANDARD_SLUGS:
        issues.append(f"data architecture standard order/set mismatch: {slugs!r}")

    for standard in standards:
        slug = standard["slug"]
        expected_path = f"docs/data-architecture/{slug}.md"
        if standard["document_path"] != expected_path:
            issues.append(f"data architecture document path mismatch for {slug}: {standard['document_path']!r}")
            continue
        path = root / expected_path
        if not path.is_file():
            issues.append(f"missing data architecture standard document: {expected_path}")
            continue
        text = path.read_text(encoding="utf-8")
        if not text.startswith(EXPECTED_TITLES[slug]):
            issues.append(f"data architecture document title mismatch: {expected_path}")
        for heading in (
            "## The question",
            "## What this standard leaves to the Museum",
            "## For machines and implementers",
            "## The Casey Reas accession",
            "## Official sources",
        ):
            if heading not in text:
                issues.append(f"data architecture document missing {heading!r}: {expected_path}")
        if f"`{standard['casey_state']}`" not in text:
            issues.append(f"Casey implementation state missing from {expected_path}")

    object_paths = sorted((root / CASEY_OBJECT_ROOT).glob("6529NM.2026.001.*.json"))
    if len(object_paths) != 7:
        issues.append(f"Casey architecture schedule expected 7 canonical objects, found {len(object_paths)}")
    canonical: dict[str, dict[str, Any]] = {}
    for path in object_paths:
        try:
            payload = load_json(path)["payload"]
            canonical[payload["object_id"]] = payload
        except Exception as exc:
            issues.append(f"cannot load Casey object for architecture schedule: {path.relative_to(root)}: {exc}")

    rows = schedule["objects"]
    row_ids = [row["object_id"] for row in rows]
    if row_ids != sorted(canonical):
        issues.append(f"Casey architecture schedule object order/set mismatch: {row_ids!r}")

    for row in rows:
        payload = canonical.get(row["object_id"])
        if payload is None:
            continue
        chain = payload["chain_identity"]
        expected = {
            "object_id": payload["object_id"],
            "title": payload["title"],
            "caip19": chain["caip19"],
            "custody_receipt_log": chain["custody_receipt_log"],
            "metadata_sha256": chain["metadata_sha256"],
            "generator_observation_sha256": chain["generator_sha256"],
            "generator_bytes_retained": False,
            "accession_state": payload["current_state"],
            "preservation_state": payload["preservation"]["status"],
        }
        if row != expected:
            issues.append(f"Casey architecture schedule row mismatch for {row['object_id']}")
        if chain["custody_receipt_transaction"] != schedule["custody_transaction"]:
            issues.append(f"Casey architecture custody transaction mismatch for {row['object_id']}")
        if chain["custody_receipt_block"] != schedule["custody_block"]:
            issues.append(f"Casey architecture custody block mismatch for {row['object_id']}")

    evidence_path = root / schedule["evidence_manifest_path"]
    if not evidence_path.is_file():
        issues.append(f"Casey architecture evidence manifest is missing: {schedule['evidence_manifest_path']}")

    try:
        release_manifest = load_json(root / RELEASE_MANIFEST_PATH)
        release_paths = {entry["path"] for entry in release_manifest["entries"]}
    except Exception as exc:
        issues.append(f"cannot load release manifest for data architecture binding: {exc}")
        release_paths = set()

    required_release_paths = {
        PROFILE_PATH.as_posix(),
        PROFILE_SCHEMA_PATH.as_posix(),
        CASEY_SCHEDULE_PATH.as_posix(),
        CASEY_SCHEMA_PATH.as_posix(),
        "docs/data-architecture.md",
        "docs/data-architecture/casey-reas-implementation.md",
        "scripts/validate_data_architecture.py",
        "tests/test_data_architecture.py",
        *(f"docs/data-architecture/{slug}.md" for slug in STANDARD_SLUGS),
    }
    missing_release_paths = sorted(required_release_paths - release_paths)
    if missing_release_paths:
        issues.append(f"release manifest omits data architecture paths: {missing_release_paths!r}")

    if profile["case_study_data_path"] != CASEY_SCHEDULE_PATH.as_posix():
        issues.append("profile Casey machine schedule path mismatch")
    if profile["stream_convergence"]["normative_for_profile"] is not False:
        issues.append("Stream must remain non-normative for the Museum data architecture profile")

    return issues


def main() -> None:
    issues = validate()
    if issues:
        for issue in issues:
            print(f"error: {issue}", file=sys.stderr)
        raise SystemExit(1)
    print("Museum data architecture validation passed.")


if __name__ == "__main__":
    main()
