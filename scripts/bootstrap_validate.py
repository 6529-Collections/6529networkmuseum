#!/usr/bin/env python3
"""Small fail-closed validator used until the complete schema pipeline lands."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from datetime import UTC, datetime
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parents[1]
GOVERNED_DIRS = ("policies", "records", "docs", "governance", "schemas", "specs")
LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
LOCAL_PATH = re.compile(r"(?:[A-Za-z]:\\(?:Users|repos)\\|/home/|/Users/)")
SECRET_PATTERNS = (
    re.compile(r"gh[opsu]_[A-Za-z0-9]{30,}"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"\beyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\b"),
    re.compile(
        r"(?i)(?:api[_ -]?key|client[_ -]?secret|private[_ -]?key|seed[_ -]?phrase|mnemonic|password)"
        r"\s*[:=]\s*['\"]?[A-Za-z0-9_./+\-=]{8,}"
    ),
)


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def load_json_files() -> dict[Path, object]:
    loaded: dict[Path, object] = {}
    for path in sorted(ROOT.rglob("*.json")):
        if ".git" in path.parts:
            continue
        try:
            # Immutable source snapshots may preserve an upstream UTF-8 BOM.
            # Governed JSON authored in this repository remains plain UTF-8.
            encoding = "utf-8-sig" if "evidence" in path.parts else "utf-8"
            loaded[path] = json.loads(path.read_text(encoding=encoding))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            fail(f"invalid JSON in {path.relative_to(ROOT)}: {exc}")
    return loaded


def check_local_markdown_links() -> None:
    for path in sorted(ROOT.rglob("*.md")):
        if ".git" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        for raw in LINK.findall(text):
            target = raw.strip().strip("<>").split("#", 1)[0]
            if not target or "://" in target or target.startswith(("mailto:", "#")):
                continue
            target = target.replace("%20", " ")
            if PurePosixPath(target).is_absolute():
                continue
            resolved = (path.parent / target).resolve()
            if not resolved.is_relative_to(ROOT) or not resolved.exists():
                fail(f"broken local link in {path.relative_to(ROOT)}: {raw}")


def check_public_record_safety() -> None:
    for directory in GOVERNED_DIRS:
        root = ROOT / directory
        if not root.exists():
            continue
        for path in sorted(p for p in root.rglob("*") if p.is_file()):
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            if LOCAL_PATH.search(text):
                fail(f"machine-local absolute path in governed record: {path.relative_to(ROOT)}")
            for pattern in SECRET_PATTERNS:
                if pattern.search(text):
                    fail(f"credential-shaped content in governed record: {path.relative_to(ROOT)}")

    # Evidence is public source material and may legitimately contain local-path
    # prose or hashes, but it must never admit credential-shaped material.
    evidence_root = ROOT / "evidence"
    if evidence_root.exists():
        for path in sorted(p for p in evidence_root.rglob("*") if p.is_file()):
            try:
                text = path.read_text(encoding="utf-8-sig")
            except UnicodeDecodeError:
                continue
            for pattern in SECRET_PATTERNS:
                if pattern.search(text):
                    fail(f"credential-shaped content in public evidence: {path.relative_to(ROOT)}")


def type_matches(value: object, expected: str) -> bool:
    return {
        "object": isinstance(value, dict),
        "array": isinstance(value, list),
        "string": isinstance(value, str),
        "integer": isinstance(value, int) and not isinstance(value, bool),
        "number": isinstance(value, (int, float)) and not isinstance(value, bool),
        "boolean": isinstance(value, bool),
        "null": value is None,
    }.get(expected, False)


def validate_schema_subset(instance: object, schema: object, location: str) -> None:
    """Validate the deliberately small JSON Schema subset used by bootstrap schemas."""
    if not isinstance(schema, dict):
        fail(f"invalid schema node at {location}")
    expected = schema.get("type")
    if isinstance(expected, str) and not type_matches(instance, expected):
        fail(f"schema type failure at {location}: expected {expected}")
    if isinstance(expected, list) and not any(type_matches(instance, item) for item in expected):
        fail(f"schema type failure at {location}: expected one of {expected}")
    if "const" in schema and instance != schema["const"]:
        fail(f"schema const failure at {location}")
    if "enum" in schema and instance not in schema["enum"]:
        fail(f"schema enum failure at {location}: {instance!r}")
    if isinstance(instance, str):
        if len(instance) < schema.get("minLength", 0):
            fail(f"schema minLength failure at {location}")
        pattern = schema.get("pattern")
        if isinstance(pattern, str) and re.search(pattern, instance) is None:
            fail(f"schema pattern failure at {location}: {instance!r}")
    if isinstance(instance, int) and not isinstance(instance, bool):
        if "minimum" in schema and instance < schema["minimum"]:
            fail(f"schema minimum failure at {location}")
    if isinstance(instance, list):
        if len(instance) < schema.get("minItems", 0):
            fail(f"schema minItems failure at {location}")
        item_schema = schema.get("items")
        if item_schema is not None:
            for index, item in enumerate(instance):
                validate_schema_subset(item, item_schema, f"{location}[{index}]")
    if isinstance(instance, dict):
        required = schema.get("required", [])
        for key in required:
            if key not in instance:
                fail(f"schema required-field failure at {location}.{key}")
        properties = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            extras = set(instance) - set(properties)
            if extras:
                fail(f"schema additional-properties failure at {location}: {sorted(extras)}")
        for key, child_schema in properties.items():
            if key in instance:
                validate_schema_subset(instance[key], child_schema, f"{location}.{key}")


def check_declared_schemas(loaded: dict[Path, object]) -> None:
    for path in sorted((ROOT / "records").rglob("*.json")):
        instance = loaded[path]
        if not isinstance(instance, dict) or not isinstance(instance.get("$schema"), str):
            fail(f"governed JSON must declare a local schema: {path.relative_to(ROOT)}")
        schema_path = (path.parent / instance["$schema"]).resolve()
        if not schema_path.is_relative_to(ROOT) or not schema_path.is_file():
            fail(f"missing or escaping declared schema: {path.relative_to(ROOT)}")
        schema = loaded.get(schema_path)
        validate_schema_subset(instance, schema, str(path.relative_to(ROOT)))


def canonical_payload_hash(record: dict[str, object]) -> str:
    payload = {key: value for key, value in record.items() if key != "record_control"}
    encoded = json.dumps(
        payload,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def check_record_controls(loaded: dict[Path, object]) -> None:
    for path in sorted((ROOT / "records").rglob("*.json")):
        record = loaded[path]
        if not isinstance(record, dict):
            fail(f"governed record must be an object: {path.relative_to(ROOT)}")
        control = record.get("record_control")
        if not isinstance(control, dict):
            fail(f"missing record_control: {path.relative_to(ROOT)}")
        constructor = control.get("constructor")
        review = control.get("review")
        if not isinstance(constructor, dict) or constructor.get("role") != "constructor":
            fail(f"invalid constructor control: {path.relative_to(ROOT)}")
        if control.get("record_status") == "reviewed":
            if not isinstance(review, dict) or review.get("role") != "reviewer":
                fail(f"reviewed record lacks reviewer: {path.relative_to(ROOT)}")
            if constructor.get("actor_id") == review.get("actor_id"):
                fail(f"constructor cannot review own record: {path.relative_to(ROOT)}")
            if review.get("outcome") != "approved":
                fail(f"reviewed record lacks approval: {path.relative_to(ROOT)}")
            if review.get("payload_sha256") != canonical_payload_hash(record):
                fail(f"review payload hash mismatch: {path.relative_to(ROOT)}")
        elif review is not None:
            fail(f"constructed record cannot contain review: {path.relative_to(ROOT)}")


def check_evidence_manifests(loaded: dict[Path, object]) -> None:
    for manifest_path in sorted((ROOT / "evidence").rglob("manifest.json")):
        manifest = loaded.get(manifest_path)
        if not isinstance(manifest, dict):
            fail(f"evidence manifest must be an object: {manifest_path.relative_to(ROOT)}")
        if manifest.get("hash_algorithm") != "sha256" or manifest.get("byte_mode") != "raw":
            fail(f"unsupported evidence digest mode: {manifest_path.relative_to(ROOT)}")
        entries = manifest.get("entries")
        if not isinstance(entries, list) or not entries:
            fail(f"evidence manifest has no entries: {manifest_path.relative_to(ROOT)}")
        seen: set[str] = set()
        for entry in entries:
            if not isinstance(entry, dict):
                fail(f"invalid evidence entry: {manifest_path.relative_to(ROOT)}")
            relative = entry.get("path")
            if not isinstance(relative, str) or relative in seen:
                fail(f"invalid or duplicate evidence path: {relative!r}")
            seen.add(relative)
            target = (manifest_path.parent / relative).resolve()
            if not target.is_relative_to(manifest_path.parent.resolve()) or not target.is_file():
                fail(f"missing or escaping evidence path: {relative}")
            payload = target.read_bytes()
            observed_hash = hashlib.sha256(payload).hexdigest()
            if observed_hash != entry.get("sha256"):
                fail(f"raw-byte evidence hash mismatch: {target.relative_to(ROOT)}")
            if len(payload) != entry.get("size"):
                fail(f"raw-byte evidence size mismatch: {target.relative_to(ROOT)}")


def check_governance_references(loaded: dict[Path, object]) -> None:
    decisions_path = ROOT / "records/governance/decisions.json"
    approvals_path = ROOT / "records/collections/approved-collections.json"
    if not decisions_path.exists() or not approvals_path.exists():
        return
    decisions = loaded[decisions_path]
    approvals = loaded[approvals_path]
    if not isinstance(decisions, dict) or not isinstance(approvals, dict):
        fail("governance registers must be objects")
    decision_rows = decisions.get("records", [])  # type: ignore[union-attr]
    ids = [row["decision_id"] for row in decision_rows]
    if len(ids) != len(set(ids)):
        fail("duplicate governance decision_id")
    adopted = {
        row["decision_id"]
        for row in decision_rows
        if row.get("governance_effect") == "adopted"
        and row.get("observed_wave_status") == "WINNER"
    }
    for row in approvals.get("collections", []):  # type: ignore[union-attr]
        if row.get("decision_id") not in adopted:
            fail(f"approved collection lacks adopted WINNER decision: {row.get('approval_id')}")

    source_ref = decisions.get("source_snapshot")
    if not isinstance(source_ref, dict) or not isinstance(source_ref.get("path"), str):
        fail("governance register lacks source snapshot")
    source_path = (ROOT / source_ref["path"]).resolve()
    if not source_path.is_relative_to(ROOT) or source_path not in loaded:
        fail("governance source snapshot is missing")
    source = loaded[source_path]
    if not isinstance(source, dict) or not isinstance(source.get("proposals"), list):
        fail("governance source snapshot has invalid proposal set")
    if decisions.get("snapshot_at") != source.get("snapshot_at"):
        fail("governance snapshot time differs from source")
    observed_source_hash = hashlib.sha256(source_path.read_bytes()).hexdigest()
    if observed_source_hash != source_ref.get("sha256"):
        fail("governance source snapshot raw-byte hash differs")

    proposals_by_id = {row.get("id"): row for row in source["proposals"] if isinstance(row, dict)}
    if len(proposals_by_id) != len(decision_rows):
        fail("governance decision count differs from proposal evidence")
    for row in decision_rows:
        source_row = proposals_by_id.get(row.get("drop_id"))
        if not isinstance(source_row, dict):
            fail(f"governance decision lacks source proposal: {row.get('decision_id')}")
        parts = source_row.get("parts")
        if not isinstance(parts, list) or len(parts) != 1 or not isinstance(parts[0], dict):
            fail(f"proposal source parts are not exactly reproducible: {row.get('decision_id')}")
        content = parts[0].get("content")
        if not isinstance(content, str):
            fail(f"proposal source content missing: {row.get('decision_id')}")
        created = datetime.fromtimestamp(source_row["created_at"] / 1000, tz=UTC)
        created_iso = created.isoformat(timespec="milliseconds").replace("+00:00", "Z")
        expected = {
            "serial_no": source_row.get("serial_no"),
            "observed_wave_status": source_row.get("drop_type"),
            "created_at": created_iso,
            "rating": source_row.get("rating"),
            "raters_count": source_row.get("raters_count"),
            "author_handle": (source_row.get("author") or {}).get("handle"),
            "proposal_content_hash": "sha256:" + hashlib.sha256(content.encode("utf-8")).hexdigest(),
        }
        for field, value in expected.items():
            if row.get(field) != value:
                fail(f"governance source mismatch for {row.get('decision_id')}.{field}")
        adopted_effect = row.get("governance_effect") == "adopted"
        if adopted_effect != (source_row.get("drop_type") == "WINNER"):
            fail(f"governance effect/status mismatch: {row.get('decision_id')}")

    non_adopted = {
        row["decision_id"]
        for row in decision_rows
        if row.get("governance_effect") == "no_adopted_effect_at_snapshot"
        and row.get("observed_wave_status") == "PARTICIPATORY"
    }
    for row in approvals.get("not_approved_at_snapshot", []):
        if row.get("decision_id") not in non_adopted:
            fail(f"non-approved collection status lacks participatory source: {row.get('decision_id')}")


def main() -> None:
    loaded = load_json_files()
    check_local_markdown_links()
    check_public_record_safety()
    check_evidence_manifests(loaded)
    check_declared_schemas(loaded)
    check_record_controls(loaded)
    check_governance_references(loaded)
    print(f"Museum bootstrap validation passed ({len(loaded)} JSON files checked).")


if __name__ == "__main__":
    main()
