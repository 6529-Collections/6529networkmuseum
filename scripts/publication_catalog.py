#!/usr/bin/env python3
"""Build and validate the immutable A(candidate) -> B(reviewed) -> C(catalog) binding."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
import tempfile
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from Crypto.Hash import keccak
from jsonschema import Draft202012Validator, FormatChecker

from canonical import canonicalize


REPOSITORY = "6529-Collections/6529networkmuseum"
JCS_ID = "0x886c7c89c308c459ca8a626e0ef36a5ea9f4c7a7b56aaf86c71a2ddf3b4f9044"
MANIFEST_PATH = "release-artifacts/latest/record-manifest.json"
PUBLICATION_INVENTORY_PATH = "schemas/public-publication-inventory.json"
PUBLICATION_BUNDLE_PATH = "records/publication/visitor-corpus-bundle-v1.json"
CATALOG_DIR = "release-artifacts/catalog"
POINTER_PATH = "release-artifacts/latest/publication-catalog-pointer.json"
CATALOG_SCHEMA_PATH = "schemas/publication-catalog.schema.json"
POINTER_SCHEMA_PATH = "schemas/publication-catalog-pointer.schema.json"
BUNDLE_SCHEMA_PATH = "schemas/public-publication-bundle.schema.json"
FULL_COMMIT = re.compile(r"^[0-9a-f]{40}$")
SHA256 = re.compile(r"^sha256:[0-9a-f]{64}$")
KECCAK = re.compile(r"^0x[0-9a-f]{64}$")
CANONICAL_CATALOG_PATH = re.compile(
    rf"^{re.escape(CATALOG_DIR)}/6529NM-PUBCAT-[0-9a-f]{{40}}\.json$"
)
TEXT_EXTENSIONS = {".json", ".json.snapshot", ".md", ".py", ".txt", ".yml", ".yaml", ".svg", ".gitattributes", ".gitignore"}
BINARY_EXTENSIONS = {".webp", ".png", ".jpg", ".jpeg", ".gif", ".avif", ".pdf", ".woff", ".woff2", ".ttf"}
MEDIA_ASSET_EXTENSIONS = BINARY_EXTENSIONS | {".svg"}
MAX_BUNDLE_BYTES = 8_000_000


class CatalogError(ValueError):
    """Raised when a catalog, pointer, or source binding violates release rules."""


def strict_load(data: bytes | str) -> Any:
    def hook(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise CatalogError(f"duplicate JSON key: {key!r}")
            result[key] = value
        return result

    return json.loads(data, object_pairs_hook=hook)


def keccak256(data: bytes) -> bytes:
    digest = keccak.new(digest_bits=256)
    digest.update(data)
    return digest.digest()


def sha256_prefixed(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def validate_full_commit(commit: str) -> None:
    if not isinstance(commit, str) or not FULL_COMMIT.fullmatch(commit):
        raise CatalogError("catalog commits must be full lowercase Git object IDs")


def validate_accepted_path(path: str, *, allow_manifest: bool = False) -> None:
    if not isinstance(path, str) or not path or path.startswith("/") or path.startswith("./") or "\\" in path:
        raise CatalogError(f"unsafe publication path: {path!r}")
    if any(char in path for char in "*?[]{}!"):
        raise CatalogError(f"publication path must be a literal path, not a pathspec: {path!r}")
    parts = path.split("/")
    if any(part in {"", ".", ".."} for part in parts):
        raise CatalogError(f"publication path contains a non-canonical segment: {path!r}")
    lowered = [part.casefold() for part in parts]
    if any(part == ".git" or part == "release-artifacts" for part in lowered):
        if not (allow_manifest and path == MANIFEST_PATH):
            raise CatalogError(f"publication path crosses the catalog/self-reference boundary: {path!r}")
    if "?" in path or "#" in path:
        raise CatalogError(f"publication path must not contain query or fragment: {path!r}")


def validate_canonical_catalog_path(path: object) -> None:
    """Validate the only path form permitted for a moving catalog pointer.

    This is intentionally separate from ``validate_accepted_path``: catalog
    files live under the release-artifacts boundary, while visitor publication
    paths are forbidden from crossing that boundary. The anchored expression
    rejects absolute, backslash, traversal, empty-segment, case-variant, and
    otherwise non-canonical spellings without consulting the filesystem.
    """

    if not isinstance(path, str) or not CANONICAL_CATALOG_PATH.fullmatch(path):
        raise CatalogError(f"pointer catalog_path is not a canonical retained catalog path: {path!r}")


def _contained_path(root: Path, relative_path: str) -> Path:
    """Resolve a repository-relative path and prove it remains under ``root``."""

    validate_canonical_catalog_path(relative_path)
    resolved_root = root.resolve(strict=False)
    candidate = (resolved_root / Path(*relative_path.split("/"))).resolve(strict=False)
    try:
        candidate.relative_to(resolved_root)
    except ValueError as exc:
        raise CatalogError("pointer catalog_path resolves outside the supplied publication root") from exc
    return candidate


def _git_type(root: Path, objectish: str) -> str:
    result = subprocess.run(["git", "-C", str(root), "cat-file", "-t", objectish], capture_output=True, text=True, check=False)
    return result.stdout.strip() if result.returncode == 0 else ""


def require_commit_object(root: Path, commit: str) -> None:
    validate_full_commit(commit)
    if _git_type(root, commit) != "commit":
        raise CatalogError(f"source head is not a Git commit object: {commit}")


def _tree_entry(root: Path, commit: str, path: str, *, allow_manifest: bool = False) -> tuple[str, str]:
    require_commit_object(root, commit)
    validate_accepted_path(path, allow_manifest=allow_manifest)
    result = subprocess.run(
        ["git", "-C", str(root), "--literal-pathspecs", "ls-tree", "-r", "-z", "--full-tree", commit, "--", path],
        capture_output=True,
        check=False,
    )
    if result.returncode:
        raise CatalogError(f"Git tree lookup failed at {commit}:{path}")
    rows = [row for row in result.stdout.split(b"\0") if row]
    if len(rows) != 1:
        raise CatalogError(f"Git path is absent or ambiguous at {commit}:{path}")
    header, tab, raw_path = rows[0].partition(b"\t")
    if not tab or raw_path.decode("utf-8") != path:
        raise CatalogError(f"Git path lookup was not exact at {commit}:{path}")
    fields = header.decode("ascii").split()
    if len(fields) != 3 or fields[1] != "blob" or fields[0] not in {"100644", "100755"}:
        raise CatalogError(f"Git path is not an ordinary file blob at {commit}:{path}")
    return fields[0], fields[2]


def git_bytes(root: Path, commit: str, path: str, *, allow_manifest: bool = False) -> bytes:
    _tree_entry(root, commit, path, allow_manifest=allow_manifest)
    result = subprocess.run(["git", "-C", str(root), "cat-file", "blob", f"{commit}:{path}"], capture_output=True, check=False)
    if result.returncode:
        raise CatalogError(f"Git object is absent at {commit}:{path}")
    return result.stdout


def git_mode(root: Path, commit: str, path: str, *, allow_manifest: bool = False) -> str:
    return _tree_entry(root, commit, path, allow_manifest=allow_manifest)[0]


def immutable_blob_url(commit: str, path: str) -> str:
    validate_full_commit(commit)
    validate_accepted_path(path, allow_manifest=path == MANIFEST_PATH)
    return f"https://github.com/{REPOSITORY}/blob/{commit}/{path}"


def immutable_raw_url(commit: str, path: str) -> str:
    validate_full_commit(commit)
    validate_accepted_path(path, allow_manifest=path == MANIFEST_PATH)
    return f"https://raw.githubusercontent.com/{REPOSITORY}/{commit}/{path}"


def normalized_bytes(path: str, data: bytes) -> tuple[bytes, str]:
    lower = path.casefold()
    if lower.endswith(tuple(BINARY_EXTENSIONS)):
        return data, "raw"
    filename = lower.rsplit("/", 1)[-1]
    if filename != "codeowners" and not any(lower.endswith(extension) for extension in TEXT_EXTENSIONS):
        raise CatalogError(f"unsupported publication document extension: {path}")
    return data.replace(b"\r\n", b"\n").replace(b"\r", b"\n"), "lf-normalized"


def document_entry(root: Path, commit: str, path: str) -> dict[str, Any]:
    validate_accepted_path(path)
    git_mode(root, commit, path)
    raw = git_bytes(root, commit, path)
    data, byte_mode = normalized_bytes(path, raw)
    jcs_keccak: str | None = None
    if path.casefold().endswith(".json"):
        jcs_keccak = "0x" + keccak256(canonicalize(strict_load(data))).hex()
    return {
        "path": path,
        "file_size": len(data),
        "byte_mode": byte_mode,
        "sha256": sha256_prefixed(data),
        "jcs_keccak256": jcs_keccak,
        "immutable_source_url": immutable_blob_url(commit, path),
        "immutable_raw_url": immutable_raw_url(commit, path),
    }


def _schema_instance(value: Any, schema: dict[str, Any], label: str) -> None:
    try:
        Draft202012Validator.check_schema(schema)
        errors = sorted(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(value), key=lambda error: list(error.absolute_path))
    except Exception as exc:
        raise CatalogError(f"{label} schema evaluation failed: {exc}") from exc
    if errors:
        detail = "; ".join(f"{label}{list(error.absolute_path)}: {error.message}" for error in errors[:8])
        raise CatalogError(detail)


def _read_manifest(root: Path, commit: str) -> tuple[dict[str, Any], dict[str, dict[str, Any]], dict[str, Any]]:
    raw = git_bytes(root, commit, MANIFEST_PATH, allow_manifest=True)
    manifest = strict_load(raw)
    if not isinstance(manifest, dict):
        raise CatalogError("committed record manifest must be an object")
    if manifest.get("manifest_type") != "6529NM_RECORD_MANIFEST" or not re.fullmatch(r"\d+\.\d+\.\d+", str(manifest.get("manifest_version"))):
        raise CatalogError("committed whole-release manifest has an invalid type/version")
    if manifest.get("hash_algorithms") != {"keccak256": 1, "sha256": 2}:
        raise CatalogError("committed manifest hash algorithm registry drifted")
    canonicalization = manifest.get("canonicalization")
    if not isinstance(canonicalization, dict) or canonicalization.get("id") != JCS_ID:
        raise CatalogError("committed manifest canonicalization pin drifted")
    entries = manifest.get("entries")
    if not isinstance(entries, list) or not entries:
        raise CatalogError("committed manifest entries are unavailable")
    by_path: dict[str, dict[str, Any]] = {}
    for entry in entries:
        if not isinstance(entry, dict) or not isinstance(entry.get("path"), str):
            raise CatalogError("committed manifest contains an invalid entry")
        path = entry["path"]
        validate_accepted_path(path, allow_manifest=False)
        if path in by_path:
            raise CatalogError(f"committed manifest contains a duplicate path: {path}")
        if not isinstance(entry.get("size"), int) or entry["size"] < 0 or not SHA256.fullmatch(str(entry.get("sha256"))) or entry.get("byte_mode") not in {"raw", "lf-normalized"}:
            raise CatalogError(f"committed manifest entry has invalid size/hash/byte_mode: {path}")
        by_path[path] = entry
    if list(by_path) != sorted(by_path):
        raise CatalogError("committed manifest paths must be sorted")
    body = dict(manifest)
    body_sha256 = body.pop("manifest_sha256", None)
    commitment = body.pop("manifest_commitment", None)
    if not SHA256.fullmatch(str(body_sha256)) or not isinstance(commitment, dict):
        raise CatalogError("committed manifest is missing body commitments")
    canonical_body = canonicalize(body)
    expected_sha = sha256_prefixed(canonical_body)
    expected_keccak = "0x" + keccak256(canonical_body).hex()
    if body_sha256 != expected_sha or commitment.get("digest") != expected_keccak or commitment.get("canonicalizationId") != JCS_ID:
        raise CatalogError("committed manifest body commitments are inconsistent")
    binding = {
        "path": MANIFEST_PATH,
        "file_size": len(raw),
        "file_sha256": sha256_prefixed(raw),
        "body_sha256": body_sha256,
        "body_keccak256": commitment["digest"],
        "canonicalization_id": commitment["canonicalizationId"],
        "immutable_source_url": immutable_blob_url(commit, MANIFEST_PATH),
        "immutable_raw_url": immutable_raw_url(commit, MANIFEST_PATH),
    }
    # Verify every whole-release manifest entry against the exact B Git tree.
    for path, entry in by_path.items():
        actual = document_entry(root, commit, path)
        if entry["size"] != actual["file_size"] or entry["sha256"] != actual["sha256"] or entry["byte_mode"] != actual["byte_mode"]:
            raise CatalogError(f"committed manifest entry does not describe the exact B bytes: {path}")
        if path.casefold().endswith(".json"):
            expected_content = entry.get("content_hash")
            if not isinstance(expected_content, dict) or expected_content.get("digest") != actual["jcs_keccak256"] or expected_content.get("canonicalizationId") != JCS_ID:
                raise CatalogError(f"committed manifest JSON content commitment drifted: {path}")
    return manifest, by_path, binding


def publication_paths_from_manifest(root: Path, commit: str) -> list[str]:
    """Return the complete whole-release path set; it is not the visitor corpus."""

    return list(_read_manifest(root, commit)[1])


def _inventory_binding(root: Path, commit: str, inventory: dict[str, Any]) -> dict[str, Any]:
    raw = git_bytes(root, commit, PUBLICATION_INVENTORY_PATH)
    body = canonicalize(inventory)
    return {
        "path": PUBLICATION_INVENTORY_PATH,
        "file_size": len(raw),
        "file_sha256": sha256_prefixed(raw),
        "body_sha256": sha256_prefixed(body),
        "body_keccak256": "0x" + keccak256(body).hex(),
        "canonicalization_id": JCS_ID,
        "inventory_version": inventory["inventory_version"],
        "counts": inventory["counts"],
        "immutable_source_url": immutable_blob_url(commit, PUBLICATION_INVENTORY_PATH),
        "immutable_raw_url": immutable_raw_url(commit, PUBLICATION_INVENTORY_PATH),
    }


def _read_inventory(root: Path, commit: str, manifest_entries: dict[str, dict[str, Any]]) -> tuple[dict[str, Any], list[str], list[str], dict[str, Any]]:
    raw = git_bytes(root, commit, PUBLICATION_INVENTORY_PATH)
    inventory = strict_load(raw)
    schema = strict_load(git_bytes(root, commit, "schemas/public-publication-inventory.schema.json"))
    if not isinstance(inventory, dict) or not isinstance(schema, dict):
        raise CatalogError("B lacks a usable public publication inventory/schema")
    _schema_instance(inventory, schema, "public publication inventory")
    if inventory.get("scope") != "visitor_publication_corpus":
        raise CatalogError("B publication inventory has the wrong scope")
    integrity = inventory.get("integrity")
    if not isinstance(integrity, dict) or integrity.get("canonicalization_id") != JCS_ID:
        raise CatalogError("B publication inventory lacks the pinned body integrity object")
    inventory_body = dict(inventory)
    inventory_body.pop("integrity", None)
    canonical_inventory_body = canonicalize(inventory_body)
    if integrity.get("body_sha256") != sha256_prefixed(canonical_inventory_body) or integrity.get("body_keccak256") != "0x" + keccak256(canonical_inventory_body).hex():
        raise CatalogError("B publication inventory body commitments are inconsistent")
    entries = inventory.get("entries")
    if not isinstance(entries, list) or not entries:
        raise CatalogError("B publication inventory entries are missing")
    paths = [entry.get("path") for entry in entries if isinstance(entry, dict)]
    if len(paths) != len(entries) or paths != sorted(set(paths)):
        raise CatalogError("B publication inventory paths must be sorted and unique")
    assembly: list[str] = []
    media: list[str] = []
    count: dict[str, int] = {}
    for entry in entries:
        if not isinstance(entry, dict) or entry.get("required_in_catalog") is not True:
            raise CatalogError("every inventory entry must be required_in_catalog")
        path = entry["path"]
        validate_accepted_path(path)
        if path not in manifest_entries:
            raise CatalogError(f"public inventory path is absent from the whole B manifest: {path}")
        actual = document_entry(root, commit, path)
        manifest_entry = manifest_entries[path]
        if manifest_entry["size"] != actual["file_size"] or manifest_entry["sha256"] != actual["sha256"] or manifest_entry["byte_mode"] != actual["byte_mode"]:
            raise CatalogError(f"public inventory path does not match its whole-manifest entry: {path}")
        count[entry["kind"]] = count.get(entry["kind"], 0) + 1
        if entry["delivery_role"] == "assembly_document":
            assembly.append(path)
            if actual["byte_mode"] not in {"lf-normalized"}:
                raise CatalogError(f"assembly document must be text-normalized: {path}")
        elif entry["delivery_role"] == "media_asset":
            media.append(path)
            suffix = path.casefold()
            if not any(suffix.endswith(extension) for extension in MEDIA_ASSET_EXTENSIONS):
                raise CatalogError(f"media asset has unsupported extension: {path}")
        else:
            raise CatalogError(f"inventory entry has an invalid delivery role: {path}")
    if inventory.get("counts") != dict(sorted(count.items())):
        raise CatalogError("public publication inventory counts do not match its entries")
    assembler = inventory.get("assembler")
    if not isinstance(assembler, dict) or assembler.get("required_paths") != assembly:
        raise CatalogError("assembler.required_paths does not equal the role-filtered assembly set")
    bundle = inventory.get("bundle")
    if not isinstance(bundle, dict) or bundle.get("path") != PUBLICATION_BUNDLE_PATH or PUBLICATION_BUNDLE_PATH in paths:
        raise CatalogError("visitor bundle must be bound separately and never embedded in inventory entries")
    if PUBLICATION_BUNDLE_PATH not in manifest_entries:
        raise CatalogError("visitor bundle is absent from the whole B manifest")
    return inventory, assembly, media, _inventory_binding(root, commit, inventory)


def _bundle_binding(root: Path, commit: str, inventory: dict[str, Any], assembly_paths: list[str], inventory_binding: dict[str, Any]) -> dict[str, Any]:
    raw = git_bytes(root, commit, PUBLICATION_BUNDLE_PATH)
    schema = strict_load(git_bytes(root, commit, BUNDLE_SCHEMA_PATH))
    bundle = strict_load(raw)
    if not isinstance(schema, dict) or not isinstance(bundle, dict):
        raise CatalogError("B lacks a usable visitor bundle/schema")
    _schema_instance(bundle, schema, "visitor corpus bundle")
    entries = bundle.get("entries")
    paths = [entry.get("path") for entry in entries if isinstance(entry, dict)]
    if paths != assembly_paths or paths != sorted(set(paths)):
        raise CatalogError("visitor bundle paths must exactly equal the sorted assembly-document paths")
    inventory_body = canonicalize(inventory)
    inventory_sha = sha256_prefixed(inventory_body)
    inventory_keccak = "0x" + keccak256(inventory_body).hex()
    if bundle.get("source_inventory_body_sha256") != inventory_sha or bundle.get("source_inventory_body_keccak256") != inventory_keccak:
        raise CatalogError("visitor bundle is bound to a different inventory body")
    content_bytes = 0
    for entry in entries:
        content = entry.get("content")
        if not isinstance(content, str):
            raise CatalogError(f"visitor bundle content is not UTF-8 text: {entry.get('path')}")
        data = content.encode("utf-8")
        if len(data) != entry.get("file_size") or sha256_prefixed(data) != entry.get("sha256"):
            raise CatalogError(f"visitor bundle content digest/size mismatch: {entry.get('path')}")
        if entry["path"].casefold().endswith(".json") and entry.get("jcs_keccak256") != "0x" + keccak256(canonicalize(strict_load(data))).hex():
            raise CatalogError(f"visitor bundle JSON commitment mismatch: {entry['path']}")
        content_bytes += len(data)
    if bundle.get("entry_count") != len(entries) or bundle.get("content_bytes") != content_bytes:
        raise CatalogError("visitor bundle entry/content counts are inconsistent")
    if len(raw) > MAX_BUNDLE_BYTES:
        raise CatalogError("visitor bundle exceeds its byte ceiling")
    body = canonicalize(bundle)
    return {
        "path": PUBLICATION_BUNDLE_PATH,
        "file_size": len(raw),
        "file_sha256": sha256_prefixed(raw),
        "raw_file_size": len(raw),
        "raw_file_sha256": sha256_prefixed(raw),
        "body_sha256": sha256_prefixed(body),
        "body_keccak256": "0x" + keccak256(body).hex(),
        "canonicalization_id": JCS_ID,
        "source_inventory_body_sha256": inventory_sha,
        "source_inventory_body_keccak256": inventory_keccak,
        "immutable_source_url": immutable_blob_url(commit, PUBLICATION_BUNDLE_PATH),
        "immutable_raw_url": immutable_raw_url(commit, PUBLICATION_BUNDLE_PATH),
    }


def render_json(value: dict[str, Any]) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def _commit_parents(root: Path, commit: str) -> list[str]:
    require_commit_object(root, commit)
    result = subprocess.run(["git", "-C", str(root), "show", "-s", "--format=%P", commit], capture_output=True, text=True, check=True)
    return result.stdout.strip().split() if result.stdout.strip() else []


def _record_review_state(root: Path, commit: str, path: str) -> tuple[dict[str, Any], dict[str, Any] | None]:
    value = strict_load(git_bytes(root, commit, path))
    payload = value.get("payload") if isinstance(value, dict) else None
    return value, payload if isinstance(payload, dict) else None


def _is_public_graph_record_path(path: str) -> bool:
    return (
        path.startswith("records/entities/")
        or path.startswith("records/relations/")
        or path in {
            "records/proposed-gifts/6529NM-PG-2026-001/wave-status-observation-2026-08-08.json",
            "records/proposed-gifts/6529NM-PG-2026-001/wave-publication-observation-2026-08-08.json",
            "records/proposed-gifts/6529NM-PG-2026-001/media-description-amendment-2026-08-08.json",
        }
    ) and path.endswith(".json")


def _reviewable_record_paths(root: Path, commit: str) -> list[str]:
    """Return the exact generated public record set, never a prefix expansion."""

    manifest_paths = publication_paths_from_manifest(root, commit)
    return sorted(path for path in manifest_paths if _is_public_graph_record_path(path))


def _payload_without_review_fields(payload: dict[str, Any]) -> dict[str, Any]:
    value = json.loads(json.dumps(payload))
    for key in ("record_status", "review_status", "reviewer", "entity_status", "payload_sha256"):
        value.pop(key, None)
    status_observation = value.get("status_observation")
    if isinstance(status_observation, dict):
        # entity() projects the same promotion state into this typed status
        # observation.  Its evidence, timestamp, and shape remain immutable.
        status_observation.pop("status_label", None)
    return value


def _envelope_without_review_hash(envelope: dict[str, Any]) -> dict[str, Any]:
    value = json.loads(json.dumps(envelope))
    content_hash = value.get("contentHash")
    if isinstance(content_hash, dict):
        content_hash.pop("digest", None)
    return value


def _validate_record_commitments(record: dict[str, Any], path: str) -> None:
    payload = record.get("payload")
    envelope = record.get("envelope")
    if not isinstance(payload, dict) or not isinstance(envelope, dict):
        raise CatalogError(f"public record lacks an envelope/payload pair: {path}")
    content_hash = envelope.get("contentHash")
    if not isinstance(content_hash, dict) or content_hash.get("algorithm") != 1 or content_hash.get("canonicalizationId") != JCS_ID:
        raise CatalogError(f"public record has an invalid Museum contentHash reference: {path}")
    if content_hash.get("digest") != "0x" + keccak256(canonicalize(payload)).hex():
        raise CatalogError(f"public record envelope contentHash does not match its payload: {path}")
    payload_commitment = payload.get("payload_sha256")
    if not isinstance(payload_commitment, str) or not SHA256.fullmatch(payload_commitment):
        raise CatalogError(f"public record payload_sha256 is not a commitment string: {path}")
    without = dict(payload)
    without.pop("payload_sha256", None)
    expected_omitted = sha256_prefixed(canonicalize(without))
    with_zero = dict(payload)
    with_zero["payload_sha256"] = "sha256:" + "0" * 64
    expected_zero = sha256_prefixed(canonicalize(with_zero))
    if payload_commitment not in {expected_omitted, expected_zero}:
        raise CatalogError(f"public record payload_sha256 does not match its canonical payload: {path}")


def _verify_deterministic_promotion_artifacts(root: Path, commit: str, manifest_entries: dict[str, dict[str, Any]]) -> None:
    """Run the committed B generators in an isolated Git-tree checkout.

    A catalog must not bless an arbitrary inventory/bundle/manifest edit merely
    because its commitments are internally consistent.  The B tree is the
    source of truth for these generators; running the committed code in a
    temporary checkout proves the three generated artifacts are the exact
    deterministic outputs of B.
    """

    required = {
        "scripts/generate_manifest.py",
        "scripts/generate_public_publication_inventory.py",
        "scripts/generate_public_publication_bundle.py",
        "scripts/bootstrap_validate.py",
        "scripts/validate.py",
    }
    missing = sorted(required - set(manifest_entries))
    if missing:
        raise CatalogError(f"B whole-release manifest omits required deterministic generators: {missing}")
    with tempfile.TemporaryDirectory(prefix="museum-publication-b-") as temporary:
        checkout = Path(temporary)
        archive = checkout / "tree.zip"
        result = subprocess.run(
            ["git", "-C", str(root), "archive", "--format=zip", "--output", str(archive), commit],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode:
            raise CatalogError(f"could not materialize exact B Git tree: {result.stderr.strip()}")
        with zipfile.ZipFile(archive) as archive_file:
            archive_file.extractall(checkout / "tree")
        tree = checkout / "tree"
        for script in (
            "scripts/generate_manifest.py",
            "scripts/generate_public_publication_inventory.py",
            "scripts/generate_public_publication_bundle.py",
        ):
            result = subprocess.run(
                [sys.executable, str(tree / script), "--check"],
                cwd=tree,
                capture_output=True,
                text=True,
                check=False,
            )
            if result.returncode:
                detail = (result.stdout + result.stderr).strip()
                raise CatalogError(f"B deterministic generator check failed for {script}: {detail}")
        for script, arguments in (
            ("scripts/bootstrap_validate.py", []),
            ("scripts/validate.py", ["--root", str(tree)]),
        ):
            result = subprocess.run(
                [sys.executable, str(tree / script), *arguments],
                cwd=tree,
                capture_output=True,
                text=True,
                check=False,
            )
            if result.returncode:
                detail = (result.stdout + result.stderr).strip()
                raise CatalogError(f"B complete validator replay failed for {script}: {detail}")


def _parse_utc(value: Any, label: str) -> datetime:
    if not isinstance(value, str):
        raise CatalogError(f"{label} must be an ISO-8601 timestamp")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise CatalogError(f"{label} is not an ISO-8601 timestamp") from exc
    if parsed.tzinfo is None:
        raise CatalogError(f"{label} must include a UTC offset")
    return parsed.astimezone(timezone.utc)


def _review_binding(root: Path, commit: str, assembly_paths: list[str], media_paths: list[str]) -> dict[str, Any]:
    reviewer_panel: tuple[Any, ...] | None = None
    primary_reviewer_id: str | None = None
    reviewed_at: str | None = None
    candidate: str | None = None
    candidate_sha: str | None = None
    candidate_keccak: str | None = None
    checked_records = 0
    reviewed_paths = sorted(path for path in assembly_paths if _is_public_graph_record_path(path))
    if not reviewed_paths:
        raise CatalogError("catalog source context has no closed public record set")
    for path in reviewed_paths:
        _, payload = _record_review_state(root, commit, path)
        if payload is None or "record_status" not in payload:
            raise CatalogError(f"reviewed B public record lacks a payload/status: {path}")
        checked_records += 1
        if payload.get("record_status") != "reviewed" or payload.get("review_status") != "reviewed":
            raise CatalogError(f"reviewed B corpus contains an unreviewed record: {path}")
        reviewer = payload.get("reviewer")
        constructor = payload.get("constructor")
        if not isinstance(reviewer, dict) or not isinstance(constructor, dict):
            raise CatalogError(f"reviewed B record lacks constructor/reviewer: {path}")
        required = {"id", "role", "reviewed_at", "reviewed_commit", "reviewed_manifest_sha256", "reviewed_manifest_keccak", "reviewer_ids", "outcome"}
        if set(reviewer) != required or reviewer.get("role") != "reviewer" or reviewer.get("outcome") != "approved":
            raise CatalogError(f"reviewed B record has incomplete or self-reviewing metadata: {path}")
        if not SHA256.fullmatch(str(reviewer.get("reviewed_manifest_sha256"))) or not KECCAK.fullmatch(str(reviewer.get("reviewed_manifest_keccak"))):
            raise CatalogError(f"reviewed B record has invalid candidate manifest commitments: {path}")
        if (
            not isinstance(reviewer.get("reviewer_ids"), list)
            or not reviewer["reviewer_ids"]
            or any(not isinstance(item, str) or not item for item in reviewer["reviewer_ids"])
            or len(set(reviewer["reviewer_ids"])) != len(reviewer["reviewer_ids"])
            or reviewer.get("id") not in reviewer["reviewer_ids"]
            or constructor.get("id") in reviewer["reviewer_ids"]
        ):
            raise CatalogError(f"reviewed B record has an invalid reviewer panel: {path}")
        if not isinstance(reviewer.get("reviewed_at"), str):
            raise CatalogError(f"reviewed B record has no reviewed_at: {path}")
        reviewed_at = reviewed_at or reviewer["reviewed_at"]
        panel = tuple(reviewer["reviewer_ids"])
        reviewer_panel = reviewer_panel or panel
        primary_reviewer_id = primary_reviewer_id or reviewer.get("id")
        if reviewed_at != reviewer["reviewed_at"] or reviewer_panel != panel or primary_reviewer_id != reviewer.get("id"):
            raise CatalogError(f"reviewed B records do not share one reviewer panel/time: {path}")
        candidate = candidate or reviewer["reviewed_commit"]
        candidate_sha = candidate_sha or reviewer["reviewed_manifest_sha256"]
        candidate_keccak = candidate_keccak or reviewer["reviewed_manifest_keccak"]
        if (candidate, candidate_sha, candidate_keccak) != (reviewer["reviewed_commit"], reviewer["reviewed_manifest_sha256"], reviewer["reviewed_manifest_keccak"]):
            raise CatalogError(f"reviewed B records bind different candidate A values: {path}")
        if _parse_utc(reviewer["reviewed_at"], f"{path}.reviewer.reviewed_at") <= _parse_utc(payload.get("created_at"), f"{path}.created_at"):
            raise CatalogError(f"reviewed B reviewer time is not after construction: {path}")
    if checked_records == 0 or candidate is None or reviewed_at is None or reviewer_panel is None:
        raise CatalogError("catalog source context has no reviewed public records")
    require_commit_object(root, candidate)
    if candidate not in _commit_parents(root, commit):
        raise CatalogError("candidate A is not a direct parent of reviewed B")
    _, candidate_manifest_entries, candidate_manifest_binding = _read_manifest(root, candidate)
    candidate_inventory, candidate_assembly, candidate_media, candidate_inventory_binding = _read_inventory(
        root, candidate, candidate_manifest_entries
    )
    _bundle_binding(root, candidate, candidate_inventory, candidate_assembly, candidate_inventory_binding)
    _, reviewed_manifest_entries, _ = _read_manifest(root, commit)
    reviewed_inventory, reviewed_assembly, reviewed_media, _ = _read_inventory(
        root, commit, reviewed_manifest_entries
    )
    if candidate_inventory != reviewed_inventory:
        raise CatalogError("candidate A and reviewed B publication inventories differ")
    if candidate_assembly != assembly_paths or candidate_media != media_paths:
        raise CatalogError("candidate A publication inventory role sets differ from reviewed B")
    if reviewed_assembly != assembly_paths or reviewed_media != media_paths:
        raise CatalogError("reviewed B publication inventory role sets drifted from the catalog inputs")
    generator_paths = {
        "scripts/generate_manifest.py",
        "scripts/generate_public_publication_inventory.py",
        "scripts/generate_public_publication_bundle.py",
        "scripts/bootstrap_validate.py",
        "scripts/validate.py",
    }
    for generator_path in generator_paths:
        if generator_path not in candidate_manifest_entries or generator_path not in reviewed_manifest_entries:
            raise CatalogError(f"deterministic generator path is not present in both candidate A and reviewed B: {generator_path}")
        if candidate_manifest_entries[generator_path] != reviewed_manifest_entries[generator_path]:
            raise CatalogError(f"deterministic generator path changed across A to B: {generator_path}")
    if candidate_sha != candidate_manifest_binding["body_sha256"] or candidate_keccak != candidate_manifest_binding["body_keccak256"]:
        raise CatalogError("reviewed B reviewer metadata does not bind candidate A's actual manifest body commitments")
    candidate_paths = _reviewable_record_paths(root, candidate)
    if candidate_paths != reviewed_paths:
        raise CatalogError("candidate A and reviewed B public record sets differ")
    # A must still be the constructed/review-pending candidate, and B may only
    # apply the deterministic review promotion fields to those exact records.
    for path in candidate_paths:
        a_record, a_payload = _record_review_state(root, candidate, path)
        _validate_record_commitments(a_record, path)
        if not isinstance(a_payload, dict) or a_payload.get("record_status") != "review_pending" or a_payload.get("review_status") not in {"pending_independent_review", "review_pending"}:
            raise CatalogError(f"candidate A is not review-pending: {path}")
        b_record, b_payload = _record_review_state(root, commit, path)
        _validate_record_commitments(b_record, path)
        if not isinstance(a_payload, dict) or not isinstance(b_payload, dict):
            raise CatalogError(f"A/B public record payload is unavailable: {path}")
        if a_payload.get("reviewer") is not None:
            raise CatalogError(f"candidate A must not contain reviewer metadata: {path}")
        if a_payload.get("record_status") != "review_pending" or a_payload.get("review_status") not in {"pending_independent_review", "review_pending"}:
            raise CatalogError(f"candidate A has an invalid review state: {path}")
        if b_payload.get("record_status") != "reviewed" or b_payload.get("review_status") != "reviewed":
            raise CatalogError(f"reviewed B has an invalid review state: {path}")
        if "entity_status" in a_payload:
            if a_payload.get("entity_status") != "review_pending" or b_payload.get("entity_status") != "published":
                raise CatalogError(f"entity_status does not follow the exact review promotion: {path}")
        elif "entity_status" in b_payload:
            raise CatalogError(f"review promotion introduced entity_status on a non-entity record: {path}")
        a_status_observation = a_payload.get("status_observation")
        b_status_observation = b_payload.get("status_observation")
        if isinstance(a_status_observation, dict):
            if a_status_observation.get("status_label") != "review_pending" or not isinstance(b_status_observation, dict) or b_status_observation.get("status_label") != "published":
                raise CatalogError(f"status_observation does not follow the exact review promotion: {path}")
        elif "status_observation" in b_payload:
            raise CatalogError(f"review promotion introduced status_observation on a record that had none: {path}")
        if _payload_without_review_fields(a_payload) != _payload_without_review_fields(b_payload):
            raise CatalogError(f"reviewed B changed non-review payload fields: {path}")
        if _envelope_without_review_hash(a_record.get("envelope", {})) != _envelope_without_review_hash(b_record.get("envelope", {})):
            raise CatalogError(f"reviewed B changed non-review envelope fields: {path}")
    diff = subprocess.run(["git", "-C", str(root), "diff", "--name-only", candidate, commit, "--"], capture_output=True, text=True, check=True).stdout.splitlines()
    generated_paths = {PUBLICATION_INVENTORY_PATH, PUBLICATION_BUNDLE_PATH, MANIFEST_PATH}
    allowed_changed = set(reviewed_paths) | generated_paths
    changed = set(diff)
    # Every reviewed public record must be promoted.  The inventory/bundle/
    # manifest are deterministic consequences and are allowed to remain byte
    # identical when a source projection has no dependency on review metadata;
    # if present, each must be the exact replayed output checked below.
    if not set(reviewed_paths).issubset(changed) or not changed.issubset(allowed_changed):
        raise CatalogError(
            "reviewed B tree delta is not the exact deterministic promotion set: "
            f"unexpected={sorted(changed - allowed_changed)}, "
            f"missing_reviewed_records={sorted(set(reviewed_paths) - changed)}"
        )
    _verify_deterministic_promotion_artifacts(root, commit, _read_manifest(root, commit)[1])
    return {"candidate_commit": candidate, "reviewed_at": reviewed_at, "reviewer_ids": list(reviewer_panel), "manifest_sha256": candidate_sha, "manifest_keccak": candidate_keccak}


def build_catalog(root: Path, *, reviewed_source_head_commit: str, accepted_paths: list[str] | None, created_at: str) -> dict[str, Any]:
    """Construct C from exact Git objects at reviewed B; no catalog/pointer is read."""

    require_commit_object(root, reviewed_source_head_commit)
    _, manifest_entries, manifest_binding = _read_manifest(root, reviewed_source_head_commit)
    inventory, assembly_paths, media_paths, inventory_binding = _read_inventory(root, reviewed_source_head_commit, manifest_entries)
    all_paths = sorted(assembly_paths + media_paths)
    if accepted_paths is not None and accepted_paths != all_paths:
        raise CatalogError("accepted_documents input must equal the closed inventory union exactly")
    bundle_binding = _bundle_binding(root, reviewed_source_head_commit, inventory, assembly_paths, inventory_binding)
    review_binding = _review_binding(root, reviewed_source_head_commit, assembly_paths, media_paths)
    catalog_id = f"6529NM-PUBCAT-{reviewed_source_head_commit}"
    payload = {
        "catalog_id": catalog_id,
        "catalog_version": "1.0.0",
        "state": "immutable_binding",
        "created_at": created_at,
        "reviewed_source_head_commit": reviewed_source_head_commit,
        "candidate_parent_commit": review_binding["candidate_commit"],
        "manifest_binding": manifest_binding,
        "publication_inventory_binding": inventory_binding,
        "bundle_binding": bundle_binding,
        "assembly_documents": [document_entry(root, reviewed_source_head_commit, path) for path in assembly_paths],
        "media_assets": [document_entry(root, reviewed_source_head_commit, path) for path in media_paths],
        "activation_policy": "frontend_activates_only_verified_catalog",
    }
    payload_hash = "0x" + keccak256(canonicalize(payload)).hex()
    value = {
        "$schema": "https://6529networkmuseum.org/schemas/publication-catalog-v1.json",
        "envelope": {
            "recordType": "PUBLICATION_CATALOG",
            "contentHash": {"algorithm": 1, "digest": payload_hash, "canonicalizationId": JCS_ID},
            "uri": f"https://6529networkmuseum.org/release/catalog/{catalog_id}.json",
        },
        "payload": payload,
    }
    return value


def build_pointer(catalog: dict[str, Any], *, catalog_file_sha256: str, activation_actor: str, activated_at: str, mode: str, prior_catalog_id: str | None) -> dict[str, Any]:
    payload = catalog.get("payload") if isinstance(catalog, dict) else None
    if not isinstance(payload, dict):
        raise CatalogError("pointer source catalog must contain a payload")
    commit = payload.get("reviewed_source_head_commit")
    catalog_id = payload.get("catalog_id")
    validate_full_commit(commit)
    if catalog_id != f"6529NM-PUBCAT-{commit}" or not SHA256.fullmatch(catalog_file_sha256):
        raise CatalogError("pointer must bind the exact catalog B and file SHA-256")
    if mode not in {"activate", "rollback"} or not isinstance(activation_actor, str) or not activation_actor or not isinstance(activated_at, str):
        raise CatalogError("pointer activation inputs are invalid")
    if mode == "activate" and prior_catalog_id == catalog_id:
        raise CatalogError("activation cannot point to the same catalog as its prior catalog")
    if mode == "rollback" and prior_catalog_id == catalog_id:
        raise CatalogError("rollback target cannot equal the current prior catalog")
    return {
        "$schema": "https://6529networkmuseum.org/schemas/publication-catalog-pointer-v1.json",
        "pointer_version": "1.0.0",
        "catalog_path": f"{CATALOG_DIR}/{catalog_id}.json",
        "catalog_file_sha256": catalog_file_sha256,
        "catalog_envelope_content_hash": catalog["envelope"]["contentHash"]["digest"],
        "source_commit": commit,
        "activation": {"actor_id": activation_actor, "activated_at": activated_at, "mode": mode, "prior_catalog_id": prior_catalog_id},
    }


def validate_catalog(catalog: dict[str, Any], *, root: Path | None = None, expected_commit: str | None = None) -> list[str]:
    issues: list[str] = []
    if not isinstance(catalog, dict):
        return ["catalog must be an object"]
    schema_path = root / CATALOG_SCHEMA_PATH if root is not None else Path(__file__).resolve().parent.parent / CATALOG_SCHEMA_PATH
    try:
        _schema_instance(catalog, json.loads(schema_path.read_text(encoding="utf-8")), "publication catalog")
    except (OSError, json.JSONDecodeError, CatalogError) as exc:
        issues.append(str(exc))
    payload = catalog.get("payload")
    envelope = catalog.get("envelope")
    if not isinstance(payload, dict) or not isinstance(envelope, dict):
        return [*issues, "catalog must contain envelope and payload"]
    commit = payload.get("reviewed_source_head_commit")
    try:
        validate_full_commit(commit)
    except CatalogError as exc:
        issues.append(str(exc))
        return issues
    if expected_commit is not None and commit != expected_commit:
        issues.append("catalog uses a mixed source commit")
    catalog_id = payload.get("catalog_id")
    if isinstance(catalog_id, str):
        expected_uri = f"https://6529networkmuseum.org/release/catalog/{catalog_id}.json"
        if envelope.get("uri") != expected_uri:
            issues.append("catalog envelope URI is not the exact canonical URI for its catalog ID")
    if envelope.get("contentHash", {}).get("digest") != "0x" + keccak256(canonicalize(payload)).hex():
        issues.append("catalog envelope content hash does not match the catalog payload")
    assembly_documents = payload.get("assembly_documents", [])
    media_assets = payload.get("media_assets", [])
    assembly_paths = [doc.get("path") for doc in assembly_documents if isinstance(doc, dict)]
    media_paths = [doc.get("path") for doc in media_assets if isinstance(doc, dict)]
    if assembly_paths != sorted(set(assembly_paths)) or media_paths != sorted(set(media_paths)) or set(assembly_paths) & set(media_paths):
        issues.append("catalog assembly_documents/media_assets must each be sorted, unique, and disjoint")
    if root is None:
        issues.append("catalog source context is required for release approval")
        return issues
    try:
        require_commit_object(root, commit)
        # The release decision is about the exact B tree.  Re-evaluate the
        # catalog wire schema from B itself rather than trusting a mutable
        # checkout-side schema while inspecting another commit.
        exact_catalog_schema = strict_load(git_bytes(root, commit, CATALOG_SCHEMA_PATH))
        _schema_instance(catalog, exact_catalog_schema, "publication catalog at exact B")
        _, manifest_entries, manifest_binding = _read_manifest(root, commit)
        inventory, expected_assembly, expected_media, inventory_binding = _read_inventory(root, commit, manifest_entries)
        if assembly_paths != expected_assembly or media_paths != expected_media or set(assembly_paths + media_paths) != set(expected_assembly + expected_media):
            issues.append("catalog assembly/media documents do not equal the closed inventory role sets")
        if payload.get("manifest_binding") != manifest_binding:
            issues.append("catalog manifest binding drifted from exact B")
        if payload.get("publication_inventory_binding") != inventory_binding:
            issues.append("catalog public inventory binding drifted from exact B")
        expected_bundle = _bundle_binding(root, commit, inventory, expected_assembly, inventory_binding)
        if payload.get("bundle_binding") != expected_bundle:
            issues.append("catalog visitor bundle binding drifted from exact B")
        actual_assembly = [document_entry(root, commit, path) for path in expected_assembly]
        actual_media = [document_entry(root, commit, path) for path in expected_media]
        if actual_assembly != assembly_documents or actual_media != media_assets:
            issues.append("catalog document digests/URLs drifted from exact B Git objects")
        _review_binding(root, commit, expected_assembly, expected_media)
    except CatalogError as exc:
        issues.append(str(exc))
    return issues


def validate_pointer(pointer: dict[str, Any], catalog: dict[str, Any], catalog_file_bytes: bytes, *, root: Path | None = None) -> list[str]:
    issues: list[str] = []
    if not isinstance(pointer, dict):
        return ["pointer must be an object"]

    # Validate the path before parsing/schema-checking or touching any
    # repository path. A malformed pointer must not widen the read surface.
    try:
        validate_canonical_catalog_path(pointer.get("catalog_path"))
    except CatalogError as exc:
        return [str(exc)]

    try:
        parsed_catalog = strict_load(catalog_file_bytes)
        if parsed_catalog != catalog:
            issues.append("supplied catalog bytes do not parse exactly to the supplied catalog")
        schema_path = root / POINTER_SCHEMA_PATH if root is not None else Path(__file__).resolve().parent.parent / POINTER_SCHEMA_PATH
        _schema_instance(pointer, json.loads(schema_path.read_text(encoding="utf-8")), "publication pointer")
    except (CatalogError, OSError, json.JSONDecodeError) as exc:
        issues.append(str(exc))
        return issues

    payload = catalog.get("payload") if isinstance(catalog, dict) else None
    if not isinstance(payload, dict):
        return [*issues, "pointer catalog payload is absent"]
    commit = payload.get("reviewed_source_head_commit")
    if pointer.get("source_commit") != commit:
        issues.append("pointer source_commit does not equal catalog B")
    catalog_id = payload.get("catalog_id")
    expected_path = f"{CATALOG_DIR}/{catalog_id}.json"
    if pointer.get("catalog_path") != expected_path:
        issues.append("pointer catalog_path does not equal the catalog ID")
    if pointer.get("catalog_file_sha256") != sha256_prefixed(catalog_file_bytes):
        issues.append("pointer catalog file SHA-256 does not match supplied immutable catalog bytes")
    if pointer.get("catalog_envelope_content_hash") != catalog.get("envelope", {}).get("contentHash", {}).get("digest"):
        issues.append("pointer catalog envelope content hash does not match the catalog")
    activation = pointer.get("activation")
    if not isinstance(activation, dict):
        issues.append("pointer activation object is required")
    else:
        if activation.get("mode") not in {"activate", "rollback"}:
            issues.append("pointer activation mode is invalid")
        if activation.get("prior_catalog_id") == catalog_id:
            issues.append("activation prior_catalog_id cannot equal the active catalog")
        try:
            _parse_utc(activation.get("activated_at"), "pointer.activation.activated_at")
        except CatalogError as exc:
            issues.append(str(exc))
    if root is not None:
        try:
            catalog_path = _contained_path(root, pointer["catalog_path"])
            resolved_root = root.resolve(strict=False)
            pointer_path = (resolved_root / Path(*POINTER_PATH.split("/"))).resolve(strict=False)
            pointer_path.relative_to(resolved_root)
        except (CatalogError, OSError, ValueError) as exc:
            issues.append(str(exc))
            return issues
        if not catalog_path.is_file():
            issues.append("pointer catalog_path does not exist in the supplied publication tree")
        else:
            try:
                actual_bytes = catalog_path.read_bytes()
                if actual_bytes != catalog_file_bytes:
                    issues.append("pointer catalog file bytes differ from the supplied immutable catalog")
                if sha256_prefixed(actual_bytes) != pointer.get("catalog_file_sha256"):
                    issues.append("pointer catalog file fixity does not match the publication tree")
            except OSError as exc:
                issues.append(f"pointer catalog file is unreadable: {exc}")
        if pointer_path.is_file():
            try:
                if strict_load(pointer_path.read_bytes()) != pointer:
                    issues.append("committed activation pointer bytes differ from the supplied pointer")
            except (OSError, json.JSONDecodeError, CatalogError) as exc:
                issues.append(f"committed activation pointer is not a valid exact object: {exc}")
    return issues


def _catalog_payload(value: dict[str, Any] | None) -> dict[str, Any]:
    payload = value.get("payload") if isinstance(value, dict) else None
    if not isinstance(payload, dict):
        raise CatalogError("catalog must contain a payload")
    catalog_id = payload.get("catalog_id")
    commit = payload.get("reviewed_source_head_commit")
    validate_full_commit(commit)
    if catalog_id != f"6529NM-PUBCAT-{commit}":
        raise CatalogError("catalog_id must be the immutable publication catalog identity for its source commit")
    return payload


def _pointer_catalog_id(pointer: dict[str, Any] | None) -> str | None:
    if not isinstance(pointer, dict):
        return None
    path = pointer.get("catalog_path")
    if not isinstance(path, str) or not path.startswith(CATALOG_DIR + "/") or not path.endswith(".json"):
        return None
    return path.rsplit("/", 1)[-1][:-5]


def _catalog_file(root: Path, catalog_id: str) -> Path:
    if not re.fullmatch(r"6529NM-PUBCAT-[0-9a-f]{40}", catalog_id):
        raise CatalogError("invalid immutable catalog ID")
    return root / Path(*f"{CATALOG_DIR}/{catalog_id}.json".split("/"))


def _assert_catalog_file(root: Path, catalog_id: str, expected: dict[str, Any]) -> bytes:
    path = _catalog_file(root, catalog_id)
    if not path.is_file():
        raise CatalogError(f"retained immutable catalog file is missing: {path}")
    raw = path.read_bytes()
    if strict_load(raw) != expected:
        raise CatalogError(f"immutable catalog file was rewritten or does not match its retained object: {catalog_id}")
    return raw


def check_append_only_catalog(
    previous_catalog: dict[str, Any] | str | None,
    current_catalog: dict[str, Any],
    previous_pointer: dict[str, Any] | None = None,
    current_pointer: dict[str, Any] | None = None,
    *,
    root: Path | None = None,
    retained_catalog_ids: set[str] | None = None,
) -> list[str]:
    """Check an immutable catalog transition and its activation lineage.

    Catalog files are append-only.  The pointer may move, but an activation
    must advance from the previously active catalog and a rollback may target
    only a distinct retained catalog explicitly supplied by the history
    reader.  ``root`` enables exact file existence/fixity checks; the pure
    form still enforces IDs and pointer semantics for wire tests.
    """

    issues: list[str] = []
    try:
        current_payload = _catalog_payload(current_catalog)
        current_id = current_payload["catalog_id"]
    except CatalogError as exc:
        return [str(exc)]
    previous_id: str | None = None
    previous_object: dict[str, Any] | None = None
    if isinstance(previous_catalog, str):
        previous_id = previous_catalog
    elif isinstance(previous_catalog, dict):
        previous_object = previous_catalog
        try:
            previous_id = _catalog_payload(previous_catalog)["catalog_id"]
        except CatalogError as exc:
            issues.append(str(exc))
    if previous_id is not None and current_id == previous_id:
        issues.append("catalog IDs are immutable; rewrite requires a new catalog ID")
    if previous_id is not None and not re.fullmatch(r"6529NM-PUBCAT-[0-9a-f]{40}", previous_id):
        issues.append("previous catalog ID is not a valid immutable catalog identity")

    if current_pointer is not None:
        active_id = _pointer_catalog_id(current_pointer)
        if active_id != current_id:
            issues.append("current pointer does not target the current catalog ID")
        if current_pointer.get("source_commit") != current_payload.get("reviewed_source_head_commit"):
            issues.append("current pointer source_commit does not equal the current catalog source commit")
        activation = current_pointer.get("activation")
        if not isinstance(activation, dict):
            issues.append("current pointer has no activation object")
        else:
            mode = activation.get("mode")
            prior = activation.get("prior_catalog_id")
            previous_active = _pointer_catalog_id(previous_pointer)
            if mode == "activate":
                if previous_pointer is None:
                    if prior is not None:
                        issues.append("initial activation must have prior_catalog_id null")
                elif prior != previous_active:
                    issues.append("activation prior_catalog_id does not equal the previously active catalog")
                if prior == current_id:
                    issues.append("activation cannot point to the same catalog as its prior catalog")
            elif mode == "rollback":
                if previous_pointer is None or previous_active is None:
                    issues.append("rollback requires a previous active pointer")
                elif prior != previous_active:
                    issues.append("rollback prior_catalog_id does not equal the previously active catalog")
                if prior == current_id:
                    issues.append("rollback target must be distinct from the current active catalog")
                if retained_catalog_ids is None or current_id not in retained_catalog_ids:
                    issues.append("rollback target is not an explicitly retained historical catalog")
            else:
                issues.append("pointer mode must be activate or rollback")
    elif previous_pointer is not None:
        issues.append("a pointer transition requires the current pointer object")

    if root is not None:
        try:
            current_raw = _assert_catalog_file(root, current_id, current_catalog)
            if current_pointer is not None and current_pointer.get("catalog_file_sha256") != sha256_prefixed(current_raw):
                issues.append("current pointer catalog_file_sha256 does not match the retained catalog file")
            if previous_id is not None and previous_object is not None:
                _assert_catalog_file(root, previous_id, previous_object)
            if previous_pointer is not None:
                previous_active = _pointer_catalog_id(previous_pointer)
                if previous_active:
                    previous_path = _catalog_file(root, previous_active)
                    if not previous_path.is_file():
                        issues.append("previous active catalog file is missing from retained history")
        except (OSError, json.JSONDecodeError, CatalogError) as exc:
            issues.append(str(exc))
        pointer_path = root / Path(*POINTER_PATH.split("/"))
        if current_pointer is not None and pointer_path.is_file():
            try:
                if strict_load(pointer_path.read_bytes()) != current_pointer:
                    issues.append("current activation pointer was rewritten after validation")
            except (OSError, json.JSONDecodeError, CatalogError) as exc:
                issues.append(f"current activation pointer is invalid: {exc}")
    return issues


def _release_blob_bytes(root: Path, commit: str, path: str) -> bytes:
    """Read one exact catalog/pointer blob without widening publication paths."""

    validate_full_commit(commit)
    if path != POINTER_PATH and not re.fullmatch(
        rf"{re.escape(CATALOG_DIR)}/6529NM-PUBCAT-[0-9a-f]{{40}}\.json", path
    ):
        raise CatalogError(f"invalid release-artifact path: {path!r}")
    result = subprocess.run(
        [
            "git",
            "-C",
            str(root),
            "--literal-pathspecs",
            "ls-tree",
            "-z",
            "--full-tree",
            commit,
            "--",
            path,
        ],
        capture_output=True,
        check=False,
    )
    rows = [row for row in result.stdout.split(b"\0") if row]
    if result.returncode or len(rows) != 1:
        raise CatalogError(f"release artifact is absent or ambiguous at {commit}:{path}")
    header, separator, raw_path = rows[0].partition(b"\t")
    fields = header.decode("ascii").split()
    if (
        not separator
        or raw_path.decode("utf-8") != path
        or len(fields) != 3
        or fields[0] not in {"100644", "100755"}
        or fields[1] != "blob"
    ):
        raise CatalogError(f"release artifact is not an exact ordinary blob: {commit}:{path}")
    blob = subprocess.run(
        ["git", "-C", str(root), "cat-file", "blob", fields[2]],
        capture_output=True,
        check=False,
    )
    if blob.returncode:
        raise CatalogError(f"release artifact blob is unreadable at {commit}:{path}")
    return blob.stdout


def git_head_commit(root: Path) -> str:
    """Return the exact commit checked out by the repository's current Git tree."""

    result = subprocess.run(
        ["git", "-C", str(root), "rev-parse", "--verify", "HEAD^{commit}"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode:
        raise CatalogError("rollback requires a repository with a retained Git HEAD commit")
    commit = result.stdout.strip()
    require_commit_object(root, commit)
    return commit


def retained_release_json(root: Path, commit: str, path: str) -> tuple[dict[str, Any], bytes]:
    """Read one exact JSON release artifact from a retained Git tree."""

    raw = _release_blob_bytes(root, commit, path)
    value = strict_load(raw)
    if not isinstance(value, dict):
        raise CatalogError(f"retained release artifact is not a JSON object: {commit}:{path}")
    return value, raw


def retained_catalog_from_git_tree(root: Path, commit: str, catalog_id: str) -> tuple[dict[str, Any], bytes]:
    """Read and identity-check one exact immutable catalog blob from Git."""

    path = f"{CATALOG_DIR}/{catalog_id}.json"
    value, raw = retained_release_json(root, commit, path)
    payload = _catalog_payload(value)
    if payload["catalog_id"] != catalog_id:
        raise CatalogError(f"retained Git-tree catalog identity does not match its path: {catalog_id}")
    return value, raw


def _catalog_tree_blobs(root: Path, commit: str) -> dict[str, str]:
    """Return exact immutable catalog paths and blob IDs at one Git commit."""

    require_commit_object(root, commit)
    result = subprocess.run(
        [
            "git",
            "-C",
            str(root),
            "--literal-pathspecs",
            "ls-tree",
            "-r",
            "-z",
            "--full-tree",
            commit,
            "--",
            CATALOG_DIR,
        ],
        capture_output=True,
        check=False,
    )
    if result.returncode:
        raise CatalogError(f"catalog history lookup failed at {commit}")
    entries: dict[str, str] = {}
    for row in (row for row in result.stdout.split(b"\0") if row):
        header, separator, raw_path = row.partition(b"\t")
        fields = header.decode("ascii").split()
        path = raw_path.decode("utf-8") if separator else ""
        if (
            not separator
            or len(fields) != 3
            or fields[0] not in {"100644", "100755"}
            or fields[1] != "blob"
            or not re.fullmatch(
                rf"{re.escape(CATALOG_DIR)}/6529NM-PUBCAT-[0-9a-f]{{40}}\.json",
                path,
            )
            or path in entries
        ):
            raise CatalogError(f"catalog history contains an invalid tree entry: {path!r}")
        entries[path] = fields[2]
    return entries


def _optional_release_json(root: Path, commit: str, path: str) -> dict[str, Any] | None:
    try:
        value = strict_load(_release_blob_bytes(root, commit, path))
    except CatalogError as exc:
        if "absent or ambiguous" in str(exc):
            return None
        raise
    if not isinstance(value, dict):
        raise CatalogError(f"release artifact is not a JSON object: {commit}:{path}")
    return value


def _git_changed_paths(root: Path, previous_commit: str, current_commit: str) -> set[str]:
    result = subprocess.run(
        [
            "git",
            "-C",
            str(root),
            "diff",
            "--name-only",
            "--no-renames",
            "-z",
            previous_commit,
            current_commit,
            "--",
        ],
        capture_output=True,
        check=False,
    )
    if result.returncode:
        raise CatalogError(f"catalog transition changed-path lookup failed: {previous_commit} -> {current_commit}")
    return {path.decode("utf-8") for path in result.stdout.split(b"\0") if path}


def _first_parent_chain(root: Path, previous_commit: str, current_commit: str) -> list[str]:
    """Return the inclusive first-parent chain from ``previous`` to ``current``."""

    require_commit_object(root, previous_commit)
    require_commit_object(root, current_commit)
    if previous_commit == current_commit:
        raise CatalogError("catalog transition must compare distinct commits")
    chain = [current_commit]
    seen = {current_commit}
    cursor = current_commit
    while cursor != previous_commit:
        parents = _commit_parents(root, cursor)
        if not parents:
            raise CatalogError("catalog transition previous_commit is not a first-parent ancestor of current_commit")
        cursor = parents[0]
        if cursor in seen:
            raise CatalogError("catalog transition encountered a cycle in first-parent history")
        seen.add(cursor)
        chain.append(cursor)
    chain.reverse()
    return chain


def _is_catalog_release_path(path: str) -> bool:
    return path == POINTER_PATH or path.startswith(CATALOG_DIR + "/")


def _check_catalog_git_transition_adjacent(root: Path, previous_commit: str, current_commit: str) -> list[str]:
    """Verify one adjacent first-parent catalog activation or rollback."""

    issues: list[str] = []
    previous_blobs = _catalog_tree_blobs(root, previous_commit)
    current_blobs = _catalog_tree_blobs(root, current_commit)
    changed = _git_changed_paths(root, previous_commit, current_commit)
    if not any(_is_catalog_release_path(path) for path in changed):
        return []

    for path, blob_id in previous_blobs.items():
        if current_blobs.get(path) != blob_id:
            issues.append(f"immutable historical catalog was deleted or rewritten: {path}")
    additions = set(current_blobs) - set(previous_blobs)

    current_pointer = _optional_release_json(root, current_commit, POINTER_PATH)
    if current_pointer is None:
        return [*issues, "current catalog transition has no activation pointer"]
    current_id = _pointer_catalog_id(current_pointer)
    if current_id is None:
        return [*issues, "current activation pointer has an invalid catalog path"]
    current_path = f"{CATALOG_DIR}/{current_id}.json"
    try:
        current_catalog_bytes = _release_blob_bytes(root, current_commit, current_path)
    except CatalogError as exc:
        return [*issues, str(exc)]
    current_catalog = strict_load(current_catalog_bytes)
    if not isinstance(current_catalog, dict):
        return [*issues, "current pointer target is not a catalog object"]

    previous_pointer = _optional_release_json(root, previous_commit, POINTER_PATH)
    previous_active_id = _pointer_catalog_id(previous_pointer)
    previous_catalog: dict[str, Any] | None = None
    if previous_pointer is not None:
        if previous_active_id is None:
            issues.append("previous activation pointer has an invalid catalog path")
        else:
            previous_path = f"{CATALOG_DIR}/{previous_active_id}.json"
            try:
                previous_bytes = _release_blob_bytes(root, previous_commit, previous_path)
            except CatalogError as exc:
                issues.append(str(exc))
                previous_bytes = None
            if previous_bytes is not None:
                value = strict_load(previous_bytes)
                if not isinstance(value, dict):
                    issues.append("previous pointer target is not a catalog object")
                else:
                    previous_catalog = value
                    issues.extend(
                        validate_pointer(
                            previous_pointer,
                            previous_catalog,
                            previous_bytes,
                        )
                    )

    issues.extend(validate_catalog(current_catalog, root=root, expected_commit=current_pointer.get("source_commit")))
    issues.extend(validate_pointer(current_pointer, current_catalog, current_catalog_bytes))
    issues.extend(
        check_append_only_catalog(
            previous_catalog,
            current_catalog,
            previous_pointer,
            current_pointer,
            retained_catalog_ids={
                path.rsplit("/", 1)[-1].removesuffix(".json")
                for path in previous_blobs
            },
        )
    )

    activation = current_pointer.get("activation")
    mode = activation.get("mode") if isinstance(activation, dict) else None
    if mode == "activate":
        if additions != {current_path}:
            issues.append("catalog activation must add exactly its one new immutable catalog")
        if current_path in previous_blobs:
            issues.append("catalog activation target already existed in prior history")
    elif mode == "rollback":
        if additions:
            issues.append("catalog rollback must not add a catalog file")
        if current_path not in previous_blobs:
            issues.append("catalog rollback target was not retained in prior Git history")

    expected_changed = {POINTER_PATH} | additions
    if changed != expected_changed:
        issues.append(
            "catalog transition changed paths outside its exact release boundary: "
            f"unexpected={sorted(changed - expected_changed)}, "
            f"missing={sorted(expected_changed - changed)}"
        )
    return issues


def check_catalog_git_transition(root: Path, previous_commit: str, current_commit: str) -> list[str]:
    """Verify every adjacent first-parent catalog activation or rollback in Git.

    All prior catalog blobs must be retained byte-for-byte at every first-parent
    step. Checking only the endpoint trees would allow a delete/rewrite/restore
    sequence to disappear from the final diff.
    """

    try:
        chain = _first_parent_chain(root, previous_commit, current_commit)
        issues: list[str] = []
        for adjacent_previous, adjacent_current in zip(chain, chain[1:]):
            try:
                adjacent_issues = _check_catalog_git_transition_adjacent(
                    root, adjacent_previous, adjacent_current
                )
            except (CatalogError, json.JSONDecodeError, OSError, subprocess.CalledProcessError) as exc:
                adjacent_issues = [str(exc)]
            issues.extend(
                f"first-parent transition {adjacent_previous} -> {adjacent_current}: {issue}"
                for issue in adjacent_issues
            )
        return issues
    except (CatalogError, json.JSONDecodeError, OSError, subprocess.CalledProcessError) as exc:
        return [str(exc)]
