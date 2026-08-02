#!/usr/bin/env python3
"""Fail-closed foundation and evidence validator for the Museum register."""

from __future__ import annotations

import hashlib
import json
import re
import struct
import sys
import binascii
from datetime import UTC, datetime
from pathlib import Path, PurePosixPath

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

from promote_casey_publications import mismatches as casey_publication_mismatches


ROOT = Path(__file__).resolve().parents[1]
GOVERNED_DIRS = ("policies", "records", "docs", "governance", "schemas", "specs")
OFFCHAIN_ENVELOPE_SCHEMA = "https://6529networkmuseum.org/schemas/record-envelope-v1.json"
LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
LOCAL_PATH = re.compile(r"(?:[A-Za-z]:[\\/](?:Users|repos)[\\/]|\\\\[A-Za-z0-9][A-Za-z0-9_.-]*[\\/][A-Za-z0-9][A-Za-z0-9_.-]*[\\/]|/(?:home|Users|root)/)")
SECRET_PATTERNS = (
    re.compile(r"gh[opsu]_[A-Za-z0-9]{30,}"),
    re.compile(r"-----BEGIN (?:[A-Z0-9]+ )?PRIVATE KEY(?: BLOCK)?-----"),
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


def reject_duplicate_json_keys(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def check_keys_and_gates_duplicate_keys() -> None:
    program_root = ROOT / "records/programs/6529NM-AP-01"
    for path in sorted(program_root.rglob("*.json")):
        try:
            json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicate_json_keys)
        except ValueError as exc:
            fail(f"duplicate JSON key in {path.relative_to(ROOT)}: {exc}")


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


TEXT_MEDIA_PREFIXES = ("text/",)
TEXTUAL_MEDIA_TYPES = {"application/json", "application/ld+json", "application/xml", "application/yaml", "application/x-yaml"}
# V1 admits only PNG because it has a small, deterministic structural parser.
# Other image/PDF/container types remain text-or-fail-closed until a parser is
# deliberately added and covered by equivalent public-safety tests.
SAFE_BINARY_MEDIA_TYPES = {"image/png"}
UNMANIFESTED_TEXT_SUFFIXES = {
    ".csv", ".html", ".htm", ".json", ".log", ".md", ".ndjson", ".rst",
    ".txt", ".xml", ".yaml", ".yml",
}
EXECUTABLE_SUFFIXES = {
    ".apk", ".app", ".bat", ".bin", ".class", ".cmd", ".com", ".dll", ".dmg", ".elf",
    ".exe", ".jar", ".js", ".msi", ".ps1", ".scr", ".sh", ".so", ".vbs",
}
BINARY_EMBEDDED_SIGNATURES = (b"\x7fELF", b"PK\x03\x04", b"PK\x05\x06", b"PK\x07\x08")
BINARY_SECRET_MARKERS = (
    b"-----BEGIN DSA PRIVATE KEY-----",
    b"-----BEGIN PGP PRIVATE KEY BLOCK-----",
    b"-----BEGIN RSA PRIVATE KEY-----",
    b"-----BEGIN EC PRIVATE KEY-----",
    b"-----BEGIN OPENSSH PRIVATE KEY-----",
    b"-----BEGIN PRIVATE KEY-----",
)
BINARY_SECRET_PATTERNS = (
    re.compile(rb"gh[opsu]_[A-Za-z0-9]{30,}"),
    re.compile(rb"-----BEGIN (?:[A-Z0-9]+ )?PRIVATE KEY(?: BLOCK)?-----"),
    re.compile(rb"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(rb"\beyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\b"),
    re.compile(rb"(?i)(?:api[_ -]?key|client[_ -]?secret|private[_ -]?key|seed[_ -]?phrase|mnemonic|password)\s*[:=]\s*['\"]?[A-Za-z0-9_./+\-=]{8,}"),
)
BINARY_LOCAL_PATH = re.compile(rb"(?:[A-Za-z]:[\\/](?:Users|repos)[\\/]|\\\\[A-Za-z0-9][A-Za-z0-9_.-]*[\\/][A-Za-z0-9][A-Za-z0-9_.-]*[\\/]|/(?:home|Users|root)/)")
BINARY_EXECUTABLE_SIGNATURES = (b"MZ", b"\x7fELF", b"#!", b"PK\x03\x04", b"PK\x05\x06", b"PK\x07\x08", b"<script")
BINARY_TEXT_MARKERS = ("api", "client", "secret", "private", "seed", "mnemonic", "password", "token", "ghp_", "AKIA", "eyJ", "-----BEGIN", "C:\\", "/Users/", "/home/", "/root/")
UTF16_SCAN_LIMIT = 65_536
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
PNG_CHUNK_TYPE = re.compile(rb"^[A-Za-z]{4}$")


def is_manifest_approved_binary(entry: dict[str, object] | None) -> bool:
    if not isinstance(entry, dict) or entry.get("byte_mode") != "raw":
        return False
    media_type = entry.get("media_type")
    if not isinstance(media_type, str) or not media_type or media_type.startswith(TEXT_MEDIA_PREFIXES):
        return False
    return media_type in SAFE_BINARY_MEDIA_TYPES


def is_manifest_textual(entry: dict[str, object] | None) -> bool:
    if not isinstance(entry, dict):
        return False
    media_type = entry.get("media_type")
    if not isinstance(media_type, str):
        return False
    base_media_type = media_type.split(";", 1)[0].strip().lower()
    return base_media_type.startswith(TEXT_MEDIA_PREFIXES) or base_media_type in TEXTUAL_MEDIA_TYPES


def validate_unmanifested_evidence(path: Path, payload: bytes) -> None:
    """Reject binary-looking evidence before any permissive text decode."""
    if path.suffix.lower() not in UNMANIFESTED_TEXT_SUFFIXES:
        fail(f"unmanifested evidence has unsupported suffix: {path.relative_to(ROOT)}")
    if b"\x00" in payload or any(signature in payload for signature in BINARY_EMBEDDED_SIGNATURES):
        fail(f"unmanifested evidence has binary signature: {path.relative_to(ROOT)}")
    if payload.startswith(b"MZ") or re.search(rb"(?m)^MZ", payload):
        fail(f"unmanifested evidence has executable signature: {path.relative_to(ROOT)}")
    if payload.startswith(b"#!") or re.search(rb"(?m)^#!", payload):
        fail(f"unmanifested evidence has executable signature: {path.relative_to(ROOT)}")
    if b"<script" in payload.lower():
        fail(f"unmanifested evidence has executable content: {path.relative_to(ROOT)}")
    if BINARY_LOCAL_PATH.search(payload) or any(marker in payload for marker in BINARY_SECRET_MARKERS) or any(pattern.search(payload) for pattern in BINARY_SECRET_PATTERNS):
        fail(f"credential-shaped content in unmanifested public evidence: {path.relative_to(ROOT)}")


def validate_binary_evidence(path: Path, entry: dict[str, object]) -> None:
    media_type = entry.get("media_type")
    if not isinstance(media_type, str) or media_type not in SAFE_BINARY_MEDIA_TYPES:
        fail(f"raw evidence has unsupported media_type: {path.relative_to(ROOT)}")
    if path.suffix.lower() in EXECUTABLE_SUFFIXES:
        fail(f"raw evidence has executable suffix: {path.relative_to(ROOT)}")
    payload = path.read_bytes()
    if any(signature.lower() in payload.lower() for signature in BINARY_EXECUTABLE_SIGNATURES):
        fail(f"raw evidence has executable signature: {path.relative_to(ROOT)}")
    if BINARY_LOCAL_PATH.search(payload) or any(marker in payload for marker in BINARY_SECRET_MARKERS) or any(pattern.search(payload) for pattern in BINARY_SECRET_PATTERNS):
        fail(f"credential-shaped content in raw public evidence: {path.relative_to(ROOT)}")
    for encoding in ("utf-8-sig",):
        try:
            decoded = payload.decode(encoding)
        except UnicodeDecodeError:
            continue
        if LOCAL_PATH.search(decoded) or any(pattern.search(decoded) for pattern in SECRET_PATTERNS):
            fail(f"credential-shaped text in raw public evidence: {path.relative_to(ROOT)}")
    # UTF-16 evidence may be embedded at an arbitrary byte offset inside a
    # structurally valid container. Decode candidate spans for both endian
    # forms, with and without BOM, rather than trusting container alignment.
    folded_payload = payload.lower()
    for encoding in ("utf-16-le", "utf-16-be"):
        for marker in BINARY_TEXT_MARKERS:
            needle = marker.encode(encoding).lower()
            start = folded_payload.find(needle)
            while start >= 0:
                try:
                    decoded = payload[start : start + UTF16_SCAN_LIMIT].decode(encoding)
                except UnicodeDecodeError:
                    decoded = ""
                if LOCAL_PATH.search(decoded) or any(pattern.search(decoded) for pattern in SECRET_PATTERNS):
                    fail(f"credential-shaped UTF-16 text in raw public evidence: {path.relative_to(ROOT)}")
                start = folded_payload.find(needle, start + 2)
    if media_type != "image/png":
        fail(f"raw evidence media profile is not admitted: {path.relative_to(ROOT)}")
    if not payload.startswith(PNG_SIGNATURE):
        fail(f"raw evidence media signature does not match {media_type}: {path.relative_to(ROOT)}")
    cursor = len(PNG_SIGNATURE)
    saw_ihdr = False
    saw_iend = False
    while cursor < len(payload):
        if cursor + 12 > len(payload):
            fail(f"PNG has truncated chunk framing: {path.relative_to(ROOT)}")
        length = struct.unpack(">I", payload[cursor : cursor + 4])[0]
        chunk_type = payload[cursor + 4 : cursor + 8]
        if not PNG_CHUNK_TYPE.fullmatch(chunk_type):
            fail(f"PNG has invalid chunk type: {path.relative_to(ROOT)}")
        end = cursor + 12 + length
        if end > len(payload):
            fail(f"PNG has truncated chunk data: {path.relative_to(ROOT)}")
        chunk_data = payload[cursor + 8 : cursor + 8 + length]
        expected_crc = struct.unpack(">I", payload[cursor + 8 + length : end])[0]
        if binascii.crc32(chunk_type + chunk_data) & 0xFFFFFFFF != expected_crc:
            fail(f"PNG chunk CRC is invalid: {path.relative_to(ROOT)}")
        if not saw_ihdr:
            if chunk_type != b"IHDR" or length != 13:
                fail(f"PNG is missing a valid first IHDR: {path.relative_to(ROOT)}")
            width, height, bit_depth, color_type, compression, filter_method, interlace = struct.unpack(">IIBBBBB", chunk_data)
            if not width or not height or bit_depth not in {1, 2, 4, 8, 16} or color_type not in {0, 2, 3, 4, 6} or compression != 0 or filter_method != 0 or interlace not in {0, 1}:
                fail(f"PNG IHDR profile is not admitted: {path.relative_to(ROOT)}")
            saw_ihdr = True
        if chunk_type == b"IEND":
            if length != 0 or saw_iend or end != len(payload):
                fail(f"PNG has trailing or malformed data after IEND: {path.relative_to(ROOT)}")
            saw_iend = True
        elif saw_iend:
            fail(f"PNG has data after IEND: {path.relative_to(ROOT)}")
        cursor = end
    if not saw_ihdr or not saw_iend:
        fail(f"PNG has no complete IHDR/IEND structure: {path.relative_to(ROOT)}")


def check_public_record_safety(evidence_entries: dict[Path, dict[str, object]] | None = None) -> None:
    evidence_entries = evidence_entries or {}
    for directory in GOVERNED_DIRS:
        root = ROOT / directory
        if not root.exists():
            continue
        for path in sorted(p for p in root.rglob("*") if p.is_file()):
            try:
                text = path.read_bytes().decode("utf-8")
            except UnicodeDecodeError as exc:
                fail(f"undecodable governed file: {path.relative_to(ROOT)}: {exc}")
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
            entry = evidence_entries.get(path.resolve())
            if is_manifest_approved_binary(entry):
                validate_binary_evidence(path, entry)
                continue
            if isinstance(entry, dict) and not is_manifest_textual(entry):
                fail(f"undeclared or unsupported non-text evidence media: {path.relative_to(ROOT)}")
            payload = path.read_bytes()
            validate_unmanifested_evidence(path, payload)
            try:
                text = payload.decode("utf-8-sig")
            except UnicodeDecodeError as exc:
                fail(f"undecodable public evidence: {path.relative_to(ROOT)}: {exc}")
            for pattern in SECRET_PATTERNS:
                if pattern.search(text):
                    fail(f"credential-shaped content in public evidence: {path.relative_to(ROOT)}")


def schema_registry(loaded: dict[Path, object]) -> Registry:
    resources = []
    for path, schema in loaded.items():
        if "schemas" not in path.parts or not isinstance(schema, dict):
            continue
        schema_id = schema.get("$id")
        if isinstance(schema_id, str):
            Draft202012Validator.check_schema(schema)
            resources.append((schema_id, Resource.from_contents(schema)))
    return Registry().with_resources(resources)


def validate_declared_schema(instance: object, schema: object, location: str, registry: Registry) -> None:
    if not isinstance(schema, dict):
        fail(f"invalid schema node at {location}")
    try:
        validator = Draft202012Validator(schema, registry=registry, format_checker=FormatChecker())
        errors = sorted(
            (leaf for error in validator.iter_errors(instance) for leaf in schema_leaf_errors(error)),
            key=lambda error: list(error.absolute_path),
        )
    except Exception as exc:
        fail(f"schema evaluation failure at {location}: {exc}")
    if errors:
        details = "; ".join(f"{location}{''.join(f'[{part!r}]' if isinstance(part, int) else f'.{part}' for part in error.absolute_path)}: {error.message}" for error in errors[:8])
        fail(f"schema validation failure: {details}")


def schema_leaf_errors(error: object) -> list[object]:
    context = getattr(error, "context", ())
    if context:
        leaves: list[object] = []
        for child in context:
            leaves.extend(schema_leaf_errors(child))
        return leaves
    return [error]


def check_declared_schemas(loaded: dict[Path, object]) -> None:
    registry = schema_registry(loaded)
    for path in sorted((ROOT / "records").rglob("*.json")):
        instance = loaded[path]
        if not isinstance(instance, dict) or not isinstance(instance.get("$schema"), str):
            fail(f"governed JSON must declare a local schema: {path.relative_to(ROOT)}")
        if instance["$schema"] == OFFCHAIN_ENVELOPE_SCHEMA:
            schema_path = ROOT / "schemas/record-envelope.schema.json"
        else:
            schema_path = (path.parent / instance["$schema"]).resolve()
        if not schema_path.is_relative_to(ROOT) or not schema_path.is_file():
            fail(f"missing or escaping declared schema: {path.relative_to(ROOT)}")
        schema = loaded.get(schema_path)
        validate_declared_schema(instance, schema, str(path.relative_to(ROOT)), registry)


def canonical_payload_hash(record: dict[str, object]) -> str:
    payload = {key: value for key, value in record.items() if key != "record_control"}
    encoded = json.dumps(
        payload,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def check_record_controls(loaded: dict[Path, object]) -> None:
    for path in sorted((ROOT / "records").rglob("*.json")):
        record = loaded[path]
        if not isinstance(record, dict):
            fail(f"governed record must be an object: {path.relative_to(ROOT)}")
        if record.get("$schema") == OFFCHAIN_ENVELOPE_SCHEMA:
            continue
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
            required_review_fields = {
                "actor_id",
                "role",
                "reviewed_at",
                "reviewed_commit",
                "outcome",
                "payload_sha256",
            }
            if not required_review_fields.issubset(review):
                fail(f"reviewed record has incomplete reviewer identity: {path.relative_to(ROOT)}")
            if not isinstance(review.get("actor_id"), str) or not review["actor_id"].strip():
                fail(f"reviewed record has anonymous reviewer: {path.relative_to(ROOT)}")
            if not isinstance(review.get("reviewed_at"), str) or len(review["reviewed_at"]) < 20:
                fail(f"reviewed record has no review time: {path.relative_to(ROOT)}")
            if not isinstance(review.get("reviewed_commit"), str) or not re.fullmatch(
                r"[0-9a-f]{40}", review["reviewed_commit"]
            ):
                fail(f"reviewed record has no immutable commit: {path.relative_to(ROOT)}")
            if constructor.get("actor_id") == review.get("actor_id"):
                fail(f"constructor cannot review own record: {path.relative_to(ROOT)}")
            if review.get("outcome") != "approved":
                fail(f"reviewed record lacks approval: {path.relative_to(ROOT)}")
            if review.get("payload_sha256") != canonical_payload_hash(record):
                fail(f"review payload hash mismatch: {path.relative_to(ROOT)}")
        elif review is not None:
            fail(f"constructed record cannot contain review: {path.relative_to(ROOT)}")
        current_revision = control.get("revision")
        if not isinstance(current_revision, int) or current_revision < 1:
            fail(f"invalid current revision: {path.relative_to(ROOT)}")
        amendment_history = record.get("amendment_history")
        if current_revision > 1 and (
            not isinstance(amendment_history, list)
            or len(amendment_history) != current_revision - 1
        ):
            fail(f"revision requires a complete amendment history: {path.relative_to(ROOT)}")
        if current_revision == 1 and amendment_history not in (None, []):
            fail(f"revision one cannot have superseded revisions: {path.relative_to(ROOT)}")
        if isinstance(amendment_history, list) and amendment_history:
            if not all(isinstance(item, dict) for item in amendment_history):
                fail(f"invalid amendment-history entry: {path.relative_to(ROOT)}")
            prior_revisions = [item.get("revision") for item in amendment_history]
            if prior_revisions != list(range(1, current_revision)):
                fail(f"amendment revisions must be complete and ordered: {path.relative_to(ROOT)}")

            def parse_control_time(value: object, label: str) -> datetime:
                if not isinstance(value, str):
                    fail(f"invalid {label}: {path.relative_to(ROOT)}")
                try:
                    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
                except ValueError as exc:
                    fail(f"invalid {label}: {path.relative_to(ROOT)}: {exc}")
                if parsed.tzinfo is None or parsed.utcoffset() is None:
                    fail(f"timezone-less {label}: {path.relative_to(ROOT)}")
                return parsed.astimezone(UTC)

            constructed_at = parse_control_time(constructor.get("constructed_at"), "constructor timestamp")
            superseded_at = [
                parse_control_time(item.get("superseded_at"), f"revision {item.get('revision')} supersession timestamp")
                for item in amendment_history
            ]
            if superseded_at != sorted(superseded_at):
                fail(f"supersession timestamps must be ordered by revision: {path.relative_to(ROOT)}")
            if constructed_at < superseded_at[-1]:
                fail(f"current revision predates its latest supersession: {path.relative_to(ROOT)}")


MEDIA_TYPE = re.compile(r"^[A-Za-z0-9!#$&^_.+-]+/[A-Za-z0-9!#$&^_.+-]+(?:\s*;\s*[A-Za-z0-9!#$&^_.+-]+=[^;\s]+)*$")


def check_evidence_manifests(loaded: dict[Path, object]) -> dict[Path, dict[str, object]]:
    declared: dict[Path, dict[str, object]] = {}
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
            if (
                not isinstance(relative, str)
                or not relative
                or relative in seen
                or PurePosixPath(relative).is_absolute()
                or "\\" in relative
                or any(part in {"", ".", ".."} for part in PurePosixPath(relative).parts)
            ):
                fail(f"invalid or duplicate evidence path: {relative!r}")
            seen.add(relative)
            target = (manifest_path.parent / relative).resolve()
            if not target.is_relative_to(manifest_path.parent.resolve()) or not target.is_file():
                fail(f"missing or escaping evidence path: {relative}")
            byte_mode = entry.get("byte_mode", manifest.get("byte_mode"))
            if byte_mode not in {"utf-8", "utf-8-sig", "raw"}:
                fail(f"unsupported evidence byte_mode: {manifest_path.relative_to(ROOT)}:{relative}")
            media_type = entry.get("media_type")
            if not isinstance(media_type, str) or not MEDIA_TYPE.fullmatch(media_type):
                fail(f"evidence entry must declare a valid media_type: {manifest_path.relative_to(ROOT)}:{relative}")
            payload = target.read_bytes()
            observed_hash = hashlib.sha256(payload).hexdigest()
            if not re.fullmatch(r"[0-9a-f]{64}", str(entry.get("sha256", ""))) or observed_hash != entry.get("sha256"):
                fail(f"raw-byte evidence hash mismatch: {target.relative_to(ROOT)}")
            if not isinstance(entry.get("size"), int) or isinstance(entry.get("size"), bool) or len(payload) != entry.get("size"):
                fail(f"raw-byte evidence size mismatch: {target.relative_to(ROOT)}")
            if target in declared:
                fail(f"evidence path is declared by multiple manifests: {target.relative_to(ROOT)}")
            declared[target] = {**entry, "byte_mode": byte_mode, "media_type": media_type}
    return declared


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
    stale_publications = casey_publication_mismatches()
    if stale_publications:
        paths = ", ".join(str(path.relative_to(ROOT)) for path in stale_publications)
        fail(f"Casey publication promotion is stale: {paths}")
    loaded = load_json_files()
    check_local_markdown_links()
    evidence_entries = check_evidence_manifests(loaded)
    check_public_record_safety(evidence_entries)
    check_keys_and_gates_duplicate_keys()
    check_declared_schemas(loaded)
    check_record_controls(loaded)
    check_governance_references(loaded)
    print(f"Museum bootstrap validation passed ({len(loaded)} JSON files checked).")


if __name__ == "__main__":
    main()
