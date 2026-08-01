#!/usr/bin/env python3
"""Fail-closed verification for the complete Casey REAS evidence package."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
import os
import platform
from pathlib import Path
from pathlib import PurePosixPath
import stat
import subprocess
import sys
import tempfile
from typing import Any
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "scripts"))
from acquire_casey_collection_snapshots import (  # noqa: E402
    PROJECT_QUERY,
    TOKENS_QUERY,
    scalar_text,
)

DEFAULT_OUTPUT = ROOT / "evidence/casey-reas-collection-snapshots"
EXPECTED_SLUGS = {"century", "pre-process", "phototaxis", "923-empty-rooms", "ex-nihilo-cosmos"}
EXPECTED = {
    "century": {"name": "CENTURY", "contract_address": "0xa7d8d9ef8d8ce8992df33d8b8cf4aebabd5bd270", "project_id": 100, "collection_id": 100, "project_info_method": "projectTokenInfo(uint256)", "population": 1000},
    "pre-process": {"name": "Pre-Process", "contract_address": "0x99a9b7c1116f9ceeb1652de04d5969cce509b069", "project_id": 383, "collection_id": 383, "project_info_method": "projectStateData(uint256)", "population": 120},
    "phototaxis": {"name": "Phototaxis", "contract_address": "0xa7d8d9ef8d8ce8992df33d8b8cf4aebabd5bd270", "project_id": 164, "collection_id": 164, "project_info_method": "projectTokenInfo(uint256)", "population": 1000},
    "923-empty-rooms": {"name": "923 EMPTY ROOMS", "contract_address": "0x145789247973c5d612bf121e9e4eef84b63eb707", "project_id": 1, "collection_id": 1, "project_info_method": "projectStateData(uint256)", "population": 924},
    "ex-nihilo-cosmos": {"name": "Ex Nihilo (Cosmos)", "contract_address": "0x0000000c687daed0fba60d1dba4e5f6149e8b894", "project_id": 0, "collection_id": 0, "project_info_method": "projectStateData(uint256)", "population": 256},
}
PR4_MERGE_COMMIT = "ff1c5825e3b61bfb2df0a639e057297beb946e4d"
PR4_TOOL_SHA256 = "e4060edf7354aa683458dfa0e620c598673a0c65202c8efadd768ae8dc03cc53"
PR4_TOOL_BLOB_OID = "755a1b1c948d900496f5e279594223c8c99ab3e8"
PR7_MERGE_COMMIT = "7193bfb9a0a6ead1871180b931aced755676b327"
PR7_SAFE_FETCH_BLOB_OID = "4b42a53b0e9d7a9bd409ae4c1ccbc8bf5a9462bc"
PR7_FETCH_GUARD_BLOB_OID = "72099b5b6484d1b292839562f94228567ed0a861"
EXPECTED_RARITY_RUNTIME = {
    "implementation": "CPython",
    "python_version": "3.12.10",
    "json_encoder": (
        "stdlib json.dumps(ensure_ascii=False, allow_nan=False, "
        "sort_keys=True, separators=(',', ':'))"
    ),
    "float_encoding": "CPython json.encoder shortest-round-trip float representation",
    "boundary": (
        "byte/hash reproducibility is guaranteed only for the same CPython "
        "implementation and version; review and regenerate fixtures after "
        "any implementation or version change"
    ),
}
PR4_RESULT_SERIALIZATION = (
    "UTF-8 bytes emitted by merged PR #4 scripts/rarity/analyze.py: "
    "stdlib json.dumps(ensure_ascii=False, indent=2, sort_keys=False) + '\\n'; "
    "the verifier compares these bytes directly, under the pinned CPython runtime"
)
RUN_ID = "20260801T172252532Z"
ACQUISITION_COMMIT = "48cd2fbf2914d295cdc4260dedb1345061f5e3b6"
PUBLISHED_SOURCE_COMMIT = "9700e842d0c991280b476cc67849d966221a742a"
TOKEN_URI_SELECTOR = "c87b56dd"
PROJECT_TOKEN_INFO_SELECTOR = "8c2c3622"
PROJECT_STATE_DATA_SELECTOR = "0ea5613f"
EXPECTED_RAW_FILES = 79
CROSS_CHECK_WARNINGS_SHA256 = "d94e65e6e6cdb30aaf01360a7bbcda9e8e24af894f917657e21e4a156db881c8"
FORBIDDEN_KEY_FRAGMENTS = ("opensea", "looksrare", "rarity", "score", "rank", "metric", "percentile", "prevalence", "frequency", "statistical")
FORBIDDEN_URL_FRAGMENTS = ("opensea.io", "looksrare.org", "rarible.com", "blur.io", "nftgo.io")
MARKETPLACE_PROVIDER_FRAGMENTS = ("opensea", "looksrare", "rarible", "blur", "nftgo")
EXTERNAL_REFERENCE_KEY_FRAGMENTS = (
    "precomputed",
    "imported",
    "provider",
    "externalrarity",
    "externalscore",
    "externalrank",
    "externalmetric",
    "marketplace",
)
PACKAGE_PREFIX = "evidence/casey-reas-collection-snapshots/"
PINNED_EXTERNAL_SEMANTIC_PATHS = {"scripts/rarity/analyze.py"}
EXPECTED_EXTERNAL_INVENTORY_ROLES = {
    "scripts/acquire_casey_collection_snapshots.py": "executable-or-test-source",
    "scripts/bootstrap_validate.py": "executable-or-test-source",
    "scripts/build_casey_package_manifest.py": "executable-or-test-source",
    "scripts/check_fetch_guard.py": "executable-or-test-source",
    "scripts/emit_casey_collection_descriptors.py": "executable-or-test-source",
    "scripts/harden_casey_snapshot_package.py": "executable-or-test-source",
    "scripts/rarity/analyze.py": "executable-or-test-source",
    "scripts/rarity/nextgen_compat.py": "executable-or-test-source",
    "scripts/safe_fetch.py": "executable-or-test-source",
    "scripts/verify_casey_snapshot_package.py": "executable-or-test-source",
    "tests/casey/test_casey_snapshot_mutations.py": "executable-or-test-source",
    "tests/test_control_plane.py": "executable-or-test-source",
    "tests/rarity/fixtures/nextgen-compatibility.expected.json": "executable-or-test-source",
    "tests/rarity/fixtures/nextgen-compatibility.json": "executable-or-test-source",
    "tests/rarity/test_nextgen_compat.py": "executable-or-test-source",
}


class VerificationError(RuntimeError):
    """Raised when any package binding or semantic invariant fails."""


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def canonical_json(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def digest_json(value: Any) -> str:
    return f"sha256:{sha256_bytes(canonical_json(value))}"


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def assert_equal(actual: Any, expected: Any, label: str) -> None:
    if actual != expected:
        raise VerificationError(f"{label}: expected {expected!r}, got {actual!r}")


def _is_reparse_point(info: os.stat_result) -> bool:
    """Return whether a directory entry is a Windows reparse point.

    ``Path.resolve`` and ``Path.is_file`` follow links.  On Windows, junctions
    and other reparse points are not all reported as POSIX symlinks, so the
    file-attribute bit is checked explicitly as well.
    """

    return bool(getattr(info, "st_file_attributes", 0) & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400))


def _checked_lstat(path: Path, label: str) -> os.stat_result:
    try:
        info = os.lstat(path)
    except OSError as error:
        raise VerificationError(f"bound path is missing or inaccessible: {label}: {path}") from error
    if stat.S_ISLNK(info.st_mode) or _is_reparse_point(info):
        raise VerificationError(f"bound path is a symlink or reparse point: {label}: {path}")
    return info


def _relative_parts(relative: str, label: str) -> tuple[str, ...]:
    if not isinstance(relative, str) or not relative or relative.startswith(("/", "\\")) or "\\" in relative:
        raise VerificationError(f"invalid bound relative path: {label}: {relative!r}")
    path = PurePosixPath(relative)
    if path.is_absolute() or any(part in {"", ".", ".."} for part in path.parts):
        raise VerificationError(f"bound path escapes root: {label}: {relative!r}")
    return path.parts


def within(root: Path, relative: str, *, require_file: bool = True, label: str = "bound path") -> Path:
    """Resolve a lexical relative path without following any component.

    The returned path is deliberately not resolved.  Every directory and the
    final file is lstat-checked, rejecting POSIX symlinks and Windows reparse
    points (including junctions) before any bytes are read.
    """

    root = Path(root)
    root_info = _checked_lstat(root, f"{label} root")
    if not stat.S_ISDIR(root_info.st_mode):
        raise VerificationError(f"bound path root is not a directory: {label}: {root}")
    candidate = root
    parts = _relative_parts(relative, label)
    final_info: os.stat_result | None = None
    for part in parts:
        candidate = candidate / part
        final_info = _checked_lstat(candidate, label)
        if candidate != root and not stat.S_ISDIR(final_info.st_mode) and part != parts[-1]:
            raise VerificationError(f"bound path component is not a directory: {label}: {candidate}")
    if final_info is None:
        raise VerificationError(f"bound path is empty: {label}")
    if require_file and not stat.S_ISREG(final_info.st_mode):
        raise VerificationError(f"bound path is not a regular file: {label}: {candidate}")
    if require_file is False and not stat.S_ISDIR(final_info.st_mode):
        raise VerificationError(f"bound path is not a directory: {label}: {candidate}")
    return candidate


def iter_regular_files_no_follow(root: Path, label: str) -> list[Path]:
    """Enumerate a bound tree while rejecting links/reparse points."""

    root = Path(root)
    root_info = _checked_lstat(root, f"{label} root")
    if not stat.S_ISDIR(root_info.st_mode):
        raise VerificationError(f"bound tree is not a directory: {label}: {root}")
    files: list[Path] = []
    pending = [root]
    while pending:
        current = pending.pop()
        try:
            entries = sorted(os.scandir(current), key=lambda entry: entry.name)
        except OSError as error:
            raise VerificationError(f"cannot enumerate bound tree: {label}: {current}") from error
        for entry in entries:
            path = Path(entry.path)
            info = _checked_lstat(path, label)
            if stat.S_ISDIR(info.st_mode):
                pending.append(path)
            elif stat.S_ISREG(info.st_mode):
                files.append(path)
            else:
                raise VerificationError(f"bound tree contains non-regular entry: {label}: {path}")
    return sorted(files, key=lambda path: path.as_posix())


def normalize_key(key: Any) -> str:
    return "".join(character.lower() for character in str(key) if character.isalnum())


def reject_current_head(value: Any, path: str = "value") -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            if str(key).lower() == "current_head":
                raise VerificationError(f"mutable current_head at {path}.{key}")
            reject_current_head(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            reject_current_head(child, f"{path}[{index}]")


def verify_commit_id(value: Any, label: str) -> str:
    if not isinstance(value, str) or len(value) != 40 or any(character not in "0123456789abcdefABCDEF" for character in value):
        raise VerificationError(f"{label} is not a full commit ID")
    return value.lower()


def verify_stable_dependency(dependency: dict[str, Any], label: str = "dependency") -> None:
    if not isinstance(dependency, dict):
        raise VerificationError(f"{label} is missing")
    reject_current_head(dependency, label)
    assert_equal(dependency.get("rarity_tool_merge_commit"), PR4_MERGE_COMMIT, f"{label} PR4 merge commit")
    assert_equal(dependency.get("rarity_tool_sha256"), PR4_TOOL_SHA256, f"{label} PR4 tool SHA")
    assert_equal(dependency.get("rarity_tool_git_blob_oid"), PR4_TOOL_BLOB_OID, f"{label} PR4 tool blob")
    verify_commit_id(dependency.get("source_snapshot_commit"), f"{label} source snapshot commit")
    verify_commit_id(dependency.get("acquisition_commit"), f"{label} acquisition commit")


def verify_pr7_dependency(value: Any, repo_root: Path) -> None:
    if not isinstance(value, dict):
        raise VerificationError("PR7 safety dependency is missing")
    reject_current_head(value, "PR7 safety dependency")
    assert_equal(value.get("status"), "merged_and_integrated", "PR7 safety dependency status")
    assert_equal(value.get("merge_commit"), PR7_MERGE_COMMIT, "PR7 merge commit")
    assert_equal(value.get("network_fetch_migration_required"), False, "PR7 network-fetch migration status")
    assert_equal(value.get("no_pr7_migration_claim"), False, "PR7 migration claim status")
    modules = (
        ("approved_fetch_module", "approved_fetch_module_sha256", "approved_fetch_module_pr7_blob_oid", PR7_SAFE_FETCH_BLOB_OID),
        ("fetch_guard_module", "fetch_guard_module_sha256", "fetch_guard_module_pr7_blob_oid", PR7_FETCH_GUARD_BLOB_OID),
    )
    for path_key, sha_key, blob_key, expected_blob in modules:
        relative = value.get(path_key)
        if not isinstance(relative, str) or relative not in {"scripts/safe_fetch.py", "scripts/check_fetch_guard.py"}:
            raise VerificationError(f"PR7 dependency path is not an approved control-plane module: {relative!r}")
        path = within(repo_root, relative, label=f"PR7 dependency module {relative}")
        assert_equal(value.get(sha_key), f"sha256:{sha256_bytes(path.read_bytes())}", f"PR7 current module hash {relative}")
        assert_equal(value.get(blob_key), expected_blob, f"PR7 merged blob pin {relative}")
        blob = subprocess.run(["git", "rev-parse", f"{PR7_MERGE_COMMIT}:{relative}"], cwd=repo_root, text=True, capture_output=True, check=False)
        if blob.returncode != 0 or blob.stdout.strip() != expected_blob:
            raise VerificationError(f"PR7 merge commit does not contain the pinned control-plane blob: {relative}")


def verify_pr4_tool_exact() -> Path:
    tool = within(ROOT, "scripts/rarity/analyze.py", label="merged PR #4 rarity tool")
    assert_equal(sha256_bytes(tool.read_bytes()), PR4_TOOL_SHA256, "current PR4 rarity tool SHA")
    blob = subprocess.run(["git", "rev-parse", f"{PR4_MERGE_COMMIT}:scripts/rarity/analyze.py"], cwd=ROOT, text=True, capture_output=True, check=False)
    if blob.returncode != 0 or blob.stdout.strip() != PR4_TOOL_BLOB_OID:
        raise VerificationError("PR4 merge commit does not contain the pinned rarity-tool blob")
    dirty = subprocess.run(["git", "status", "--porcelain", "--", "scripts/rarity"], cwd=ROOT, text=True, capture_output=True, check=False)
    if dirty.returncode != 0 or dirty.stdout.strip():
        raise VerificationError("rarity-tool path is dirty; local variants are not admissible")
    return tool


def verify_rarity_runtime() -> None:
    """Reject runtime drift before recomputing byte/hash-sensitive outputs."""

    actual = {
        "implementation": platform.python_implementation(),
        "python_version": platform.python_version(),
    }
    expected = {
        "implementation": EXPECTED_RARITY_RUNTIME["implementation"],
        "python_version": EXPECTED_RARITY_RUNTIME["python_version"],
    }
    assert_equal(actual, expected, "rarity runtime")


def verify_git_bytes(commit: str, relative: str, payload: bytes, label: str) -> None:
    completed = subprocess.run(["git", "cat-file", "blob", f"{commit}:{relative}"], cwd=ROOT, capture_output=True, check=False)
    if completed.returncode != 0:
        raise VerificationError(f"{label}: {commit} does not contain {relative}")
    assert_equal(completed.stdout, payload, f"{label} byte preservation {relative}")


def reject_external_metrics(value: Any, path: str = "value") -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            normalized = normalize_key(key)
            if any(fragment in normalized for fragment in FORBIDDEN_KEY_FRAGMENTS):
                raise VerificationError(f"forbidden external/precomputed metric key at {path}.{key}")
            reject_external_metrics(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            reject_external_metrics(child, f"{path}[{index}]")
    elif isinstance(value, str):
        lowered = value.lower()
        if any(fragment in lowered for fragment in FORBIDDEN_URL_FRAGMENTS):
            raise VerificationError(f"forbidden marketplace URL at {path}")


def reject_external_references(value: Any, path: str = "value") -> None:
    """Reject marketplace/provider and imported-metric references everywhere.

    Generated descriptor results intentionally contain the Museum's own
    statistical fields. This separate guard therefore rejects external
    provider/marketplace references and explicitly imported/precomputed field
    names, while ``reject_external_metrics`` remains the stricter input/raw
    policy for acquisition material.
    """

    if isinstance(value, dict):
        for key, child in value.items():
            normalized = normalize_key(key)
            if any(fragment in normalized for fragment in EXTERNAL_REFERENCE_KEY_FRAGMENTS):
                raise VerificationError(f"forbidden external/provider field at {path}.{key}")
            reject_external_references(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            reject_external_references(child, f"{path}[{index}]")
    elif isinstance(value, str):
        normalized = normalize_key(value)
        if any(fragment in normalized for fragment in MARKETPLACE_PROVIDER_FRAGMENTS) or any(fragment in value.lower() for fragment in FORBIDDEN_URL_FRAGMENTS):
            raise VerificationError(f"forbidden marketplace/provider reference at {path}")


def verify_file_record(repo_root: Path, item: dict[str, Any]) -> Path:
    relative = item.get("path")
    if not isinstance(relative, str) or relative.startswith("/"):
        raise VerificationError(f"invalid root inventory path: {item!r}")
    path = within(repo_root, relative, label=f"root inventory {relative}")
    payload = path.read_bytes()
    assert_equal(f"sha256:{sha256_bytes(payload)}", item.get("sha256"), f"root inventory hash {relative}")
    assert_equal(len(payload), item.get("size"), f"root inventory size {relative}")
    return path


def verify_raw_ref(run_root: Path, ref: dict[str, Any]) -> bytes:
    relative = ref.get("path")
    if not isinstance(relative, str) or not relative.startswith("raw/"):
        raise VerificationError(f"invalid raw ref: {ref!r}")
    assert_equal(ref.get("byte_mode"), "raw", f"raw byte mode {relative}")
    path = within(run_root, relative, label=f"raw response {relative}")
    payload = path.read_bytes()
    assert_equal(f"sha256:{sha256_bytes(payload)}", ref.get("sha256"), f"raw response hash {relative}")
    assert_equal(len(payload), ref.get("size"), f"raw response size {relative}")
    return payload


def verify_derived_ref(run_root: Path, ref: dict[str, Any]) -> bytes:
    relative = ref.get("path")
    if not isinstance(relative, str) or not relative.startswith("derived/"):
        raise VerificationError(f"invalid derived ref: {ref!r}")
    assert_equal(ref.get("byte_mode"), "reconstructed_from_preserved_v2_invocation", f"derived byte mode {relative}")
    path = within(run_root, relative, label=f"derived file {relative}")
    payload = path.read_bytes()
    assert_equal(f"sha256:{sha256_bytes(payload)}", ref.get("sha256"), f"derived hash {relative}")
    assert_equal(len(payload), ref.get("size"), f"derived size {relative}")
    return payload


def collect_raw_refs(value: Any, found: set[str] | None = None) -> set[str]:
    if found is None:
        found = set()
    if isinstance(value, dict):
        if isinstance(value.get("path"), str) and value["path"].startswith("raw/"):
            found.add(value["path"])
        for child in value.values():
            collect_raw_refs(child, found)
    elif isinstance(value, list):
        for child in value:
            collect_raw_refs(child, found)
    return found


def collect_derived_refs(value: Any, found: set[str] | None = None) -> set[str]:
    if found is None:
        found = set()
    if isinstance(value, dict):
        if isinstance(value.get("path"), str) and value["path"].startswith("derived/"):
            found.add(value["path"])
        for child in value.values():
            collect_derived_refs(child, found)
    elif isinstance(value, list):
        for child in value:
            collect_derived_refs(child, found)
    return found


def expected_static_inventory_roles() -> dict[str, str]:
    expected = {
        f"{PACKAGE_PREFIX}collection-sources.json": "authoritative-acquisition-config",
        f"{PACKAGE_PREFIX}pending-descriptors.json": "review-ledger",
        f"{PACKAGE_PREFIX}descriptor-manifest.json": "descriptor-child-manifest",
        f"{PACKAGE_PREFIX}fixtures/features-materialization.json": "verification-fixture",
        f"{PACKAGE_PREFIX}fixtures/tool-input-projection.json": "verification-fixture",
        f"{PACKAGE_PREFIX}runs/{RUN_ID}/run-manifest.json": "acquisition-child-manifest",
        f"{PACKAGE_PREFIX}README.md": "package-documentation",
    }
    for slug in sorted(EXPECTED_SLUGS):
        expected[f"{PACKAGE_PREFIX}descriptors/{slug}.json"] = "descriptor"
        expected[f"{PACKAGE_PREFIX}runs/{RUN_ID}/snapshots/{slug}/snapshot.json"] = "metadata-snapshot"
    expected.update(EXPECTED_EXTERNAL_INVENTORY_ROLES)
    return expected


def expected_inventory_roles(run_root: Path, manifest: dict[str, Any]) -> dict[str, str]:
    expected = expected_static_inventory_roles()
    repo_root = ROOT
    raw_root = within(run_root, "raw", require_file=False, label="raw observation tree")
    for raw in iter_regular_files_no_follow(raw_root, "raw observations"):
        expected[str(raw.relative_to(repo_root)).replace("\\", "/")] = "raw-observation"
    derived_paths = collect_derived_refs(manifest)
    for ref_name in ("request_provenance", "exclusion_summary"):
        ref = manifest.get(ref_name)
        if isinstance(ref, dict):
            derived_paths.add(ref["path"])
            derived_paths.update(collect_derived_refs(json.loads(verify_derived_ref(run_root, ref).decode("utf-8"))))
    for relative in sorted(derived_paths):
        expected[f"{PACKAGE_PREFIX}runs/{RUN_ID}/{relative}"] = "derived-provenance"
    return expected


def verify_inventory_scope(run_root: Path, manifest: dict[str, Any], inventory: list[dict[str, Any]]) -> None:
    expected = expected_inventory_roles(run_root, manifest)
    actual: dict[str, str] = {}
    for item in inventory:
        path = item.get("path")
        role = item.get("role")
        if not isinstance(path, str) or not isinstance(role, str):
            raise VerificationError(f"root inventory item is malformed: {item!r}")
        normalized = path.replace("\\", "/")
        if normalized != path or any(part in {"", ".", ".."} for part in PurePosixPath(path).parts):
            raise VerificationError(f"root inventory path is not canonical: {path}")
        actual[path] = role
    assert_equal(actual, expected, "root inventory closed path/role allowlist")


def verify_ordering(snapshot: dict[str, Any], expected_ids: list[int], label: str) -> None:
    tokens = snapshot.get("tokens")
    traits = snapshot.get("traits")
    source_metadata = snapshot.get("source_metadata")
    source_trait_rows = snapshot.get("source_trait_rows")
    if not all(isinstance(item, list) for item in (tokens, traits, source_metadata, source_trait_rows)):
        raise VerificationError(f"{label}: token/trait arrays are missing")
    token_ids = [row.get("id") for row in tokens]
    assert_equal(len(token_ids), len(expected_ids), f"{label}: token count")
    assert_equal(sorted(token_ids), expected_ids, f"{label}: canonical token population")
    ordering = snapshot.get("ordering")
    if not isinstance(ordering, dict):
        raise VerificationError(f"{label}: ordering object missing")
    assert_equal(ordering.get("source_token_order"), token_ids, f"{label}: source token order")
    assert_equal(ordering.get("canonical_token_order"), expected_ids, f"{label}: canonical token order")
    source_indices = [row.get("source_row_index") for row in source_trait_rows]
    assert_equal(source_indices, list(range(len(source_indices))), f"{label}: source trait row indices")
    assert_equal(ordering.get("source_trait_row_order"), source_indices, f"{label}: source trait order")
    canonical_expected = [row["source_row_index"] for row in sorted(traits, key=lambda row: (row.get("token_id"), row.get("trait"), row.get("value"), row.get("source_feature_index")))]
    assert_equal(ordering.get("canonical_trait_order"), canonical_expected, f"{label}: canonical trait order")
    if {row.get("source_row_index") for row in traits} != set(source_indices):
        raise VerificationError(f"{label}: source trait and materialized trait indices diverge")


def abi_uint(data: bytes, index: int) -> int:
    start = index * 32
    if len(data) < start + 32:
        raise VerificationError("ABI response is shorter than expected")
    return int.from_bytes(data[start : start + 32], "big")


def decode_token_uri(result: str) -> str:
    if not isinstance(result, str) or not result.startswith("0x"):
        raise VerificationError("tokenURI result is not ABI hex")
    data = bytes.fromhex(result[2:])
    offset = abi_uint(data, 0)
    length = abi_uint(data, offset // 32)
    end = offset + 32 + length
    if end > len(data):
        raise VerificationError("tokenURI ABI string is truncated")
    return data[offset + 32 : end].decode("utf-8")


def validate_config(config: dict[str, Any]) -> dict[str, dict[str, Any]]:
    assert_equal(config.get("schema_version"), "6529nm.casey-collection-sources.v1", "collection source schema")
    chain = config.get("chain")
    if not isinstance(chain, dict):
        raise VerificationError("closed chain identity is missing")
    assert_equal(chain.get("caip2"), "eip155:1", "collection chain")
    assert_equal(chain.get("chain_id"), 1, "collection chain ID")
    assert_equal(chain.get("token_id_encoding"), "(project_id * 1000000) + invocation_number", "token ID encoding")
    sources = config.get("authoritative_sources")
    if not isinstance(sources, dict):
        raise VerificationError("authoritative source map is missing")
    assert_equal(sources.get("project_graphql_uri"), "https://data.artblocks.io/v1/graphql", "authoritative GraphQL endpoint")
    collections = config.get("collections")
    if not isinstance(collections, list) or len(collections) != len(EXPECTED) or {row.get("slug") for row in collections} != EXPECTED_SLUGS:
        raise VerificationError("closed collection mapping does not contain exactly five expected projects")
    by_slug = {}
    for row in collections:
        slug = row["slug"]
        expected = EXPECTED[slug]
        for key in ("name", "contract_address", "project_id", "collection_id", "project_info_method"):
            actual = row.get(key)
            if key == "contract_address":
                actual = str(actual).lower()
                expected_value = expected[key].lower()
            else:
                expected_value = expected[key]
            assert_equal(actual, expected_value, f"closed config {slug}.{key}")
        assert_equal(row.get("artist"), "Casey REAS", f"closed config {slug}.artist")
        assert_equal(row.get("token_uri_method"), "tokenURI(uint256)", f"closed config {slug}.token_uri_method")
        assert_equal(row.get("project_graphql_id"), f"{expected['contract_address']}-{expected['project_id']}", f"closed config {slug}.project_graphql_id")
        by_slug[slug] = row
    return by_slug


def verify_block_and_population(output_dir: Path, run_root: Path, manifest: dict[str, Any], config_by_slug: dict[str, dict[str, Any]]) -> None:
    observation = manifest["observation"]
    assert_equal(observation.get("chain", {}).get("caip2"), "eip155:1", "observation chain")
    assert_equal(observation.get("chain", {}).get("chain_id"), 1, "observation chain ID")
    assert_equal(observation.get("chain", {}).get("token_id_encoding"), "(project_id * 1000000) + invocation_number", "observation token ID encoding")
    assert_equal(observation.get("block_number"), 25661488, "observation block number")
    assert_equal(observation.get("block_tag"), "0x1879030", "observation block tag")
    assert_equal(observation.get("block_hash"), "0x6802d1fd8a983eddc4c44588cdf3be88c8e5a3079d492b61ba7e97ca8c2fdd26", "observation block hash")
    assert_equal(manifest.get("bulk_source", {}).get("uri"), "https://data.artblocks.io/v1/graphql", "manifest GraphQL endpoint")
    assert_equal(manifest.get("bulk_source", {}).get("project_query"), PROJECT_QUERY, "manifest project GraphQL query")
    assert_equal(manifest.get("bulk_source", {}).get("token_query"), TOKENS_QUERY, "manifest token GraphQL query")
    assert_equal(manifest.get("bulk_source", {}).get("project_query_sha256"), digest_json(PROJECT_QUERY), "manifest project query hash")
    assert_equal(manifest.get("bulk_source", {}).get("token_query_sha256"), digest_json(TOKENS_QUERY), "manifest token query hash")
    assert_equal(manifest.get("bulk_source", {}).get("order_by"), "token_id asc", "manifest token order")
    assert_equal(manifest.get("bulk_source", {}).get("page_size"), 250, "manifest page size")
    assert_equal(manifest.get("rpc", {}).get("token_uri_selector"), "0x" + TOKEN_URI_SELECTOR, "tokenURI selector")
    block_number_response = json.loads(verify_raw_ref(run_root, manifest["rpc"]["block_number_source"]).decode("utf-8"))
    assert_equal(int(block_number_response["result"], 16), observation["block_number"], "pinned block number RPC")
    assert_equal(block_number_response.get("jsonrpc"), "2.0", "block number RPC version")
    block_response = json.loads(verify_raw_ref(run_root, manifest["rpc"]["block_source"]).decode("utf-8"))
    assert_equal(block_response.get("jsonrpc"), "2.0", "block header RPC version")
    block = block_response.get("result")
    if not isinstance(block, dict):
        raise VerificationError("pinned block header RPC has no result")
    assert_equal(block.get("number"), observation["block_tag"], "pinned block header number")
    assert_equal(block.get("hash"), observation["block_hash"], "pinned block header hash")
    for row in manifest["collections"]:
        slug = row["slug"]
        expected = config_by_slug[slug]
        closed = EXPECTED[slug]
        assert_equal(row.get("name"), closed["name"], f"{slug}: manifest name")
        assert_equal(str(row.get("contract_address")).lower(), closed["contract_address"].lower(), f"{slug}: manifest contract")
        assert_equal(row.get("project_id"), closed["project_id"], f"{slug}: manifest project")
        snapshot = read_json(within(output_dir, row["snapshot_path"], label=f"{slug}: metadata snapshot"))
        source = snapshot["source"]
        assert_equal(source.get("chain"), "eip155:1", f"{slug}: snapshot chain")
        assert_equal(str(source.get("contract_address")).lower(), closed["contract_address"].lower(), f"{slug}: snapshot contract")
        assert_equal(source.get("project_id"), closed["project_id"], f"{slug}: snapshot project")
        assert_equal(source.get("project_info_method"), closed["project_info_method"], f"{slug}: snapshot population method")
        assert_equal(source.get("bulk_graphql_uri"), "https://data.artblocks.io/v1/graphql", f"{slug}: snapshot GraphQL endpoint")
        assert_equal(source.get("project_graphql_variables"), {"id": expected["project_graphql_id"], "chain_id": 1}, f"{slug}: project GraphQL variables")
        info_response = json.loads(verify_raw_ref(run_root, source["project_info_response"]).decode("utf-8"))
        assert_equal(info_response.get("id"), f"project-info-{slug}", f"{slug}: population response ID")
        result = info_response.get("result")
        if not isinstance(result, str) or not result.startswith("0x"):
            raise VerificationError(f"{slug}: project population call has no result")
        data = bytes.fromhex(result[2:])
        if expected["project_info_method"] == "projectTokenInfo(uint256)":
            invocation_index, max_index = 2, 3
        else:
            invocation_index, max_index = 0, 1
        invocations = abi_uint(data, invocation_index)
        max_invocations = abi_uint(data, max_index)
        assert_equal(invocations, closed["population"], f"{slug}: decoded onchain invocations")
        assert_equal(max_invocations, closed["population"], f"{slug}: decoded onchain max invocations")
        assert_equal(snapshot["population"]["onchain_invocations"], invocations, f"{slug}: snapshot onchain invocations")
        assert_equal(snapshot["population"]["onchain_max_invocations"], max_invocations, f"{slug}: snapshot onchain max invocations")
        project_graphql = json.loads(verify_raw_ref(run_root, source["project_graphql_response"]).decode("utf-8"))
        project_rows = project_graphql.get("data", {}).get("projects_metadata")
        if not isinstance(project_rows, list) or len(project_rows) != 1:
            raise VerificationError(f"{slug}: project GraphQL row count")
        project = project_rows[0]
        assert_equal(project.get("id"), expected["project_graphql_id"], f"{slug}: project GraphQL ID")
        assert_equal(project.get("chain_id"), 1, f"{slug}: project GraphQL chain")
        assert_equal(str(project.get("project_id")), str(expected["project_id"]), f"{slug}: project GraphQL project")
        assert_equal(str(project.get("contract_address")).lower(), expected["contract_address"].lower(), f"{slug}: project GraphQL contract")
        assert_equal(project.get("max_invocations"), closed["population"], f"{slug}: project GraphQL max invocations")
        assert_equal(project.get("invocations"), closed["population"], f"{slug}: project GraphQL invocations")
        if project.get("complete") is not True:
            raise VerificationError(f"{slug}: project GraphQL completeness false")


def verify_materialization(output_dir: Path, run_root: Path, manifest: dict[str, Any], config_by_slug: dict[str, dict[str, Any]]) -> int:
    total_traits = 0
    for collection_manifest in manifest["collections"]:
        slug = collection_manifest["slug"]
        config = config_by_slug[slug]
        snapshot = read_json(within(output_dir, collection_manifest["snapshot_path"], label=f"{slug}: metadata snapshot"))
        bulk_rows: list[dict[str, Any]] = []
        expected_population = EXPECTED[slug]["population"]
        expected_page_count = (expected_population + 249) // 250
        assert_equal(len(collection_manifest["bulk_pages"]), expected_page_count, f"{slug}: bulk page count")
        for page_index, page in enumerate(collection_manifest["bulk_pages"]):
            expected_offset = page_index * 250
            expected_limit = 250
            expected_returned = min(250, expected_population - expected_offset)
            assert_equal(page.get("offset"), expected_offset, f"{slug}: bulk page offset")
            assert_equal(page.get("limit"), expected_limit, f"{slug}: bulk page limit")
            assert_equal(page.get("variables"), {"project": config["project_graphql_id"], "limit": expected_limit, "offset": expected_offset}, f"{slug}: bulk page variables")
            expected_payload = {"query": TOKENS_QUERY, "variables": page["variables"]}
            assert_equal(page.get("request_sha256"), digest_json(expected_payload), f"{slug}: bulk request hash")
            raw = json.loads(verify_raw_ref(run_root, page["raw_response"]).decode("utf-8"))
            rows = raw.get("data", {}).get("tokens_metadata")
            if not isinstance(rows, list) or len(rows) != page["returned_count"]:
                raise VerificationError(f"{slug}: raw bulk page count mismatch at {page['offset']}")
            assert_equal(page["returned_count"], expected_returned, f"{slug}: bulk page returned count")
            bulk_rows.extend(rows)
        expected = int(config["project_id"])
        expected_ids = [expected * 1_000_000 + invocation for invocation in range(EXPECTED[slug]["population"])]
        if sorted(int(row["token_id"]) for row in bulk_rows) != expected_ids:
            raise VerificationError(f"{slug}: raw Hasura token population mismatch")
        uri_by_id: dict[int, tuple[str, dict[str, Any], str]] = {}
        response_member_ids: set[str] = set()
        for token in snapshot["tokens"]:
            ref = token["token_uri_rpc_response"]
            response = json.loads(verify_raw_ref(run_root, ref).decode("utf-8"))
            if not isinstance(response, list):
                raise VerificationError(f"{slug}: tokenURI response is not a batch")
            members = {item.get("id"): item for item in response if isinstance(item, dict)}
            member = members.get(token.get("rpc_id"))
            if not isinstance(member, dict) or not isinstance(member.get("result"), str):
                raise VerificationError(f"{slug}: tokenURI raw member missing for {token.get('id')}")
            expected_member_id = f"token-uri-{int(token['id'])}"
            assert_equal(member.get("id"), expected_member_id, f"{slug}: tokenURI member ID")
            response_member_ids.add(expected_member_id)
            uri_by_id[int(token["id"])] = (decode_token_uri(member["result"]), ref, member["id"])
        assert_equal(response_member_ids, {f"token-uri-{token_id}" for token_id in expected_ids}, f"{slug}: tokenURI response member population")
        expected_tokens = []
        expected_metadata = []
        expected_traits = []
        expected_source_rows = []
        for source_index, row in enumerate(bulk_rows):
            token_id = int(row["token_id"])
            invocation = row["invocation"]
            assert_equal(token_id, expected * 1_000_000 + int(invocation), f"{slug}: token ID formula")
            assert_equal(int(invocation), token_id - expected * 1_000_000, f"{slug}: invocation formula")
            if row.get("chain_id") != 1 or str(row.get("contract_address", "")).lower() != config["contract_address"].lower() or row.get("project_id") != config["project_graphql_id"]:
                raise VerificationError(f"{slug}: raw Hasura identity mismatch at {token_id}")
            if not isinstance(row.get("features"), dict):
                raise VerificationError(f"{slug}: raw Hasura features is not an object at {token_id}")
            uri, uri_ref, rpc_id = uri_by_id.get(token_id, (None, None, None))
            if uri is None:
                raise VerificationError(f"{slug}: raw tokenURI missing at {token_id}")
            for feature_index, (feature, value) in enumerate(row["features"].items()):
                value_text = scalar_text(value)
                source_row_index = len(expected_source_rows)
                item = {"source_row_index": source_row_index, "token_id": token_id, "collection_id": int(config["collection_id"]), "feature_index": feature_index, "raw_value": value, "value": value_text, "trait": str(feature)}
                expected_source_rows.append(item)
                expected_traits.append({"token_id": token_id, "collection_id": int(config["collection_id"]), "trait": str(feature), "value": value_text, "source_row_index": source_row_index, "source_feature_index": feature_index})
            expected_metadata.append({"token_id": token_id, "invocation": invocation, "source_index": source_index, "hasura_id": row.get("id"), "hasura_project_id": row.get("project_id"), "token_hash": row.get("hash"), "features": row["features"], "live_view_url": row.get("live_view_url"), "media_url": row.get("media_url"), "primary_asset_url": row.get("primary_asset_url"), "token_uri": uri, "token_uri_rpc_response": uri_ref})
            expected_tokens.append({"id": token_id, "collection_id": int(config["collection_id"]), "invocation": invocation, "source_index": source_index, "token_uri": uri, "token_uri_rpc_response": uri_ref, "rpc_id": rpc_id, "token_hash": row.get("hash"), "live_view_url": row.get("live_view_url"), "media_url": row.get("media_url"), "primary_asset_url": row.get("primary_asset_url")})
        assert_equal(snapshot["source_metadata"], expected_metadata, f"{slug}: source metadata recomputation")
        assert_equal(snapshot["tokens"], expected_tokens, f"{slug}: token rows recomputation")
        assert_equal(snapshot["traits"], expected_traits, f"{slug}: materialized traits recomputation")
        assert_equal(snapshot["source_trait_rows"], expected_source_rows, f"{slug}: source trait rows recomputation")
        verify_ordering(snapshot, expected_ids, slug)
        total_traits += len(expected_traits)
    return total_traits


def verify_request_provenance(output_dir: Path, run_root: Path, manifest: dict[str, Any], config_by_slug: dict[str, dict[str, Any]]) -> dict[str, Any]:
    ref = manifest.get("request_provenance")
    if not isinstance(ref, dict):
        raise VerificationError("request provenance binding is missing")
    provenance = json.loads(verify_derived_ref(run_root, ref).decode("utf-8"))
    assert_equal(provenance.get("schema_version"), "6529nm.casey-request-provenance.v1", "request provenance schema")
    assert_equal(provenance.get("network_fetch_status"), "offline_reconstruction_only", "request provenance mode")
    retry_policy = provenance.get("retry_policy", {})
    assert_equal(retry_policy.get("max_attempts"), 3, "retry max attempts")
    assert_equal(retry_policy.get("max_retries"), 2, "retry max retries")
    assert_equal(retry_policy.get("retry_delay_ms"), 100, "retry delay")
    requests = provenance.get("requests")
    if not isinstance(requests, list):
        raise VerificationError("request provenance records are missing")
    counts = Counter(row.get("family") for row in requests)
    expected_bulk = sum(len(row["bulk_pages"]) for row in manifest["collections"])
    expected_counts = {"rpc_token_uri": 3300, "graphql_project_metadata": 5, "graphql_tokens_metadata": expected_bulk, "rpc_project_population": 5, "rpc_shared": 2}
    assert_equal(dict(counts), expected_counts, "request family counts")
    assert_equal(provenance.get("request_counts"), {"total_records": 3327, "token_uri": 3300, "project_graphql": 5, "bulk_graphql": expected_bulk, "project_population_rpc": 5, "shared_rpc": 2}, "request count summary")
    assert_equal(len(requests), 3327, "total request records")
    if len({row.get("request_id") for row in requests}) != len(requests):
        raise VerificationError("request IDs are not unique")

    observation = manifest["observation"]
    block_tag = observation["block_tag"]
    rpc_uri = observation["rpc_uri"]
    graphql_uri = manifest["bulk_source"]["uri"]
    expected_specs: dict[str, dict[str, Any]] = {}

    def add_spec(request_id: str, **spec: Any) -> None:
        if request_id in expected_specs:
            raise VerificationError(f"duplicate expected request ID: {request_id}")
        expected_specs[request_id] = spec

    add_spec("block-number", family="rpc_shared", endpoint=rpc_uri, operation="eth_blockNumber", payload={"jsonrpc": "2.0", "id": "block-number", "method": "eth_blockNumber", "params": []}, response_ref=manifest["rpc"]["block_number_source"])
    add_spec("observed-block", family="rpc_shared", endpoint=rpc_uri, operation="eth_getBlockByNumber", payload={"jsonrpc": "2.0", "id": "observed-block", "method": "eth_getBlockByNumber", "params": [block_tag, False]}, response_ref=manifest["rpc"]["block_source"])
    for collection in manifest["collections"]:
        slug = collection["slug"]
        config = config_by_slug[slug]
        snapshot = read_json(within(output_dir, collection["snapshot_path"], label=f"{slug}: metadata snapshot"))
        source = snapshot["source"]
        project_id = int(config["project_id"])
        selector = PROJECT_TOKEN_INFO_SELECTOR if config["project_info_method"] == "projectTokenInfo(uint256)" else PROJECT_STATE_DATA_SELECTOR
        project_payload = {"jsonrpc": "2.0", "id": f"project-info-{slug}", "method": "eth_call", "params": [{"to": config["contract_address"], "data": "0x" + selector + project_id.to_bytes(32, "big").hex()}, block_tag]}
        add_spec(f"project-info-{slug}", family="rpc_project_population", endpoint=rpc_uri, operation=config["project_info_method"], payload=project_payload, response_ref=source["project_info_response"], collection=slug)
        project_graphql_payload = {"query": PROJECT_QUERY, "variables": {"id": config["project_graphql_id"], "chain_id": 1}}
        add_spec(f"project-metadata-{slug}", family="graphql_project_metadata", endpoint=graphql_uri, operation="CaseyProject", payload=project_graphql_payload, response_ref=source["project_graphql_response"], collection=slug)
        expected_ids = [int(config["project_id"]) * 1_000_000 + invocation for invocation in range(EXPECTED[slug]["population"])]
        for page in collection["bulk_pages"]:
            payload = {"query": TOKENS_QUERY, "variables": page["variables"]}
            add_spec(f"tokens-metadata-{slug}-{page['offset']}", family="graphql_tokens_metadata", endpoint=graphql_uri, operation="CaseyTokens", payload=payload, response_ref=page["raw_response"], collection=slug, offset=page["offset"], limit=page["limit"])
        token_by_id = {int(token["id"]): token for token in snapshot["tokens"]}
        batch_size = int(manifest["rpc"].get("batch_size"))
        assert_equal(batch_size, 100, "tokenURI batch size")
        for batch_number, start in enumerate(range(0, len(expected_ids), batch_size)):
            batch_ids = expected_ids[start : start + batch_size]
            batch_refs = {token_by_id[token_id]["token_uri_rpc_response"]["path"] for token_id in batch_ids}
            if len(batch_refs) != 1:
                raise VerificationError(f"{slug}: tokenURI batch has multiple response references")
            batch_ref = token_by_id[batch_ids[0]]["token_uri_rpc_response"]
            batch_payload = [{"jsonrpc": "2.0", "id": f"token-uri-{token_id}", "method": "eth_call", "params": [{"to": config["contract_address"], "data": "0x" + TOKEN_URI_SELECTOR + token_id.to_bytes(32, "big").hex()}, block_tag]} for token_id in batch_ids]
            for token_id in batch_ids:
                add_spec(f"token-uri-{token_id}", family="rpc_token_uri", endpoint=rpc_uri, operation="tokenURI(uint256)", payload=batch_payload[batch_ids.index(token_id)], request_body_payload=batch_payload, response_ref=batch_ref, collection=slug, token_id=token_id, batch_number=batch_number, batch_offset=start)

    seen_body_keys = set()
    token_ids = []
    for request in requests:
        request_id = request.get("request_id")
        if request_id not in expected_specs:
            raise VerificationError(f"unexpected request ID: {request_id}")
        spec = expected_specs[request_id]
        for key in ("family", "endpoint", "operation"):
            assert_equal(request.get(key), spec[key], f"{request_id}: {key}")
        endpoint = urlsplit(str(request.get("endpoint")))
        assert_equal(endpoint.scheme, "https", f"{request_id}: HTTPS endpoint")
        assert_equal(request.get("endpoint_authority"), endpoint.netloc, f"{request_id}: endpoint authority")
        assert_equal(request.get("http_method"), "POST", f"{request_id}: HTTP method")
        assert_equal(request.get("request_payload"), spec["payload"], f"{request_id}: logical request payload")
        request_body_payload = spec.get("request_body_payload", spec["payload"])
        body_ref = request.get("request_body")
        body = verify_derived_ref(run_root, body_ref)
        assert_equal(body, canonical_json(request_body_payload), f"canonical request bytes {request_id}")
        assert_equal(request.get("request_body_sha256"), body_ref.get("sha256"), f"request body hash {request_id}")
        assert_equal(request.get("request_body_sha256"), digest_json(request_body_payload), f"{request_id}: body digest")
        seen_body_keys.add((body_ref.get("path"), body_ref.get("sha256"), body_ref.get("size")))
        response_ref = request.get("response", {}).get("raw_ref")
        assert_equal(response_ref, spec["response_ref"], f"{request_id}: response reference")
        raw = verify_raw_ref(run_root, response_ref)
        assert_equal(request.get("response", {}).get("response_sha256"), response_ref.get("sha256"), f"{request_id}: response hash")
        discarded = request.get("discarded_partial_response")
        if not isinstance(discarded, dict) or discarded.get("bytes_present") is not False or not isinstance(discarded.get("not_claimed"), str):
            raise VerificationError(f"partial response provenance is not fail-closed for {request_id}")
        attempts = request.get("attempts")
        if not isinstance(attempts, list) or not attempts or [row.get("ordinal") for row in attempts] != list(range(1, len(attempts) + 1)):
            raise VerificationError(f"attempt ordinals missing or unordered for {request_id}")
        if len(attempts) > retry_policy["max_attempts"]:
            raise VerificationError(f"too many attempts for {request_id}")
        for attempt in attempts:
            if not isinstance(attempt.get("status"), (int, str)) or not isinstance(attempt.get("ok"), bool):
                raise VerificationError(f"attempt outcome missing for {request_id}")
        if request.get("attempt_timestamps", {}).get("timestamps") is not None:
            raise VerificationError(f"unpreserved timestamps were invented for {request_id}")
        if request.get("attempts_mode") not in {"contemporaneous_v2_manifest", "contemporaneous_v2_snapshot", "reconstructed_success_only"}:
            raise VerificationError(f"unknown attempt mode for {request_id}")
        if spec["family"] in {"rpc_project_population", "graphql_project_metadata", "graphql_tokens_metadata"}:
            assert_equal(request.get("collection"), spec["collection"], f"{request_id}: collection")
        if spec["family"] == "graphql_tokens_metadata":
            assert_equal(request.get("offset"), spec["offset"], f"{request_id}: offset")
            assert_equal(request.get("limit"), spec["limit"], f"{request_id}: limit")
        elif spec["family"] == "rpc_token_uri":
            assert_equal(request.get("collection"), spec["collection"], f"{request_id}: collection")
            assert_equal(request.get("token_id"), spec["token_id"], f"{request_id}: token ID")
            assert_equal(request.get("response_member_id"), request_id, f"{request_id}: response member ID")
            assert_equal(request.get("batch_request_body_sha256"), body_ref.get("sha256"), f"{request_id}: batch body hash")
            members = {row.get("id"): row for row in json.loads(raw.decode("utf-8")) if isinstance(row, dict)}
            member = members.get(request_id)
            if not isinstance(member, dict) or not isinstance(member.get("result"), str):
                raise VerificationError(f"tokenURI response member missing for {request_id}")
            assert_equal(request.get("response_member_digest"), digest_json(member), f"{request_id}: response member digest")
            if decode_token_uri(member["result"]) == "":
                raise VerificationError(f"empty tokenURI response for {request_id}")
            token_ids.append(int(request["token_id"]))
        elif spec["family"] == "graphql_project_metadata":
            if not isinstance(json.loads(raw.decode("utf-8")).get("data", {}).get("projects_metadata"), list):
                raise VerificationError(f"project GraphQL response malformed for {request_id}")
    assert_equal(set(expected_specs), {row.get("request_id") for row in requests}, "closed request ID mapping")
    expected_all = []
    for slug, data in EXPECTED.items():
        expected_all.extend([data["project_id"] * 1_000_000 + invocation for invocation in range(data["population"])])
    assert_equal(sorted(token_ids), sorted(expected_all), "all tokenURI request IDs")
    assert_equal(len(token_ids), len(set(token_ids)), "unique tokenURI request IDs")
    unique_bodies = provenance.get("unique_request_bodies")
    if not isinstance(unique_bodies, list):
        raise VerificationError("unique reconstructed request body inventory is incomplete")
    for body_ref in unique_bodies:
        verify_derived_ref(run_root, body_ref)
    actual_unique = {(row.get("path"), row.get("sha256"), row.get("size")) for row in unique_bodies}
    assert_equal(actual_unique, seen_body_keys, "complete unique request body inventory")
    assert_equal(len(unique_bodies), 62, "unique reconstructed request body count")
    return {"records": len(requests), "token_uri": len(token_ids), "unique_request_bodies": len(unique_bodies)}


def verify_exclusion_row(row: dict[str, Any], check: dict[str, Any], raw: dict[str, Any], expected_contract: str, expected_population: set[int], row_index: int) -> None:
    key = (row.get("collection"), int(row.get("token_id")))
    if row.get("cross_check_order") != row_index or row.get("source_location") != "traits[0]" or row.get("source_order") != 0:
        raise VerificationError(f"invalid exclusion source location/order: {key}")
    assert_equal(row.get("source_uri"), check.get("source_uri"), f"exclusion source URI {key}")
    assert_equal(row.get("retrieval_uri"), check.get("retrieval_uri"), f"exclusion retrieval URI {key}")
    assert_equal(row.get("raw_response"), check.get("raw_response"), f"exclusion raw binding {key}")
    traits = raw.get("traits")
    if not isinstance(traits, list) or not traits or traits[0] != row.get("excluded_row") or not str(traits[0].get("value", "")).lower().startswith("all "):
        raise VerificationError(f"exclusion bytes do not match raw traits[0]: {key}")
    if str(raw.get("tokenID")) != str(row["token_id"]):
        raise VerificationError(f"exclusion token identity mismatch: {key}")
    if str(row.get("token_identity", {}).get("contract_address", "")).lower() != expected_contract.lower():
        raise VerificationError(f"exclusion contract identity mismatch: {key}")
    if int(row["token_id"]) not in expected_population:
        raise VerificationError(f"excluded token is outside closed population: {key}")


def verify_exclusions(run_root: Path, manifest: dict[str, Any], config_by_slug: dict[str, dict[str, Any]]) -> int:
    ref = manifest.get("exclusion_summary")
    if not isinstance(ref, dict):
        raise VerificationError("exclusion summary binding is missing")
    summary = json.loads(verify_derived_ref(run_root, ref).decode("utf-8"))
    assert_equal(summary.get("schema_version"), "6529nm.casey-http-exclusions.v1", "exclusion schema")
    checks = [check for collection in manifest["collections"] for check in collection["http_cross_checks"]]
    rows = summary.get("rows")
    assert_equal(summary.get("observed_cross_check_count"), len(checks), "observed cross-check count")
    assert_equal(summary.get("excluded_row_count"), len(checks), "excluded row count")
    if not isinstance(rows, list) or len(rows) != len(checks):
        raise VerificationError("exclusion rows are incomplete")
    seen = set()
    expected_keys = []
    for collection in manifest["collections"]:
        expected_keys.extend((collection["slug"], int(check["token_id"])) for check in collection["http_cross_checks"])
    assert_equal([(row.get("collection"), int(row.get("token_id"))) for row in rows], expected_keys, "exclusion source order")
    for row_index, row in enumerate(rows):
        key = (row.get("collection"), int(row.get("token_id")))
        check = next((item for collection in manifest["collections"] if collection["slug"] == row.get("collection") for item in collection["http_cross_checks"] if int(item["token_id"]) == int(row.get("token_id"))), None)
        if check is None or key in seen:
            raise VerificationError(f"invalid or duplicate exclusion row: {row}")
        seen.add(key)
        raw = json.loads(verify_raw_ref(run_root, row["raw_response"]).decode("utf-8"))
        expected = EXPECTED[row["collection"]]
        expected_population = {expected["project_id"] * 1_000_000 + invocation for invocation in range(expected["population"])}
        verify_exclusion_row(row, check, raw, config_by_slug[row["collection"]]["contract_address"], expected_population, row_index)
    if Counter(row.get("reason") for row in rows) != Counter(summary.get("by_reason", {})):
        raise VerificationError("exclusion reason summary mismatch")
    return len(rows)


def verify_descriptors(output_dir: Path, manifest: dict[str, Any], package: dict[str, Any], config_by_slug: dict[str, dict[str, Any]]) -> int:
    descriptor_manifest = read_json(within(output_dir, "descriptor-manifest.json", label="descriptor child manifest"))
    assert_equal(descriptor_manifest.get("schema_version"), "6529nm.casey-collection-descriptor-manifest.v2", "descriptor manifest schema")
    assert_equal(descriptor_manifest.get("review"), None, "descriptor manifest review")
    dependency = descriptor_manifest.get("dependency", {})
    verify_stable_dependency(dependency, "descriptor manifest dependency")
    package_dependency = package.get("dependency", {})
    verify_stable_dependency(package_dependency, "root dependency")
    for key in ("source_snapshot_commit", "acquisition_commit", "rarity_tool_merge_commit", "rarity_tool_sha256", "rarity_tool_git_blob_oid"):
        assert_equal(dependency.get(key), package_dependency.get(key), f"descriptor/root dependency {key}")
    jobs = descriptor_manifest.get("jobs")
    if not isinstance(jobs, list) or len(jobs) != len(EXPECTED) or {job.get("collection") for job in jobs} != EXPECTED_SLUGS:
        raise VerificationError("descriptor jobs are incomplete")
    by_slug = {row["slug"]: row for row in manifest["collections"]}
    verify_rarity_runtime()
    tool = verify_pr4_tool_exact()
    for job in jobs:
        slug = job["collection"]
        path = within(output_dir, job["output"], label=f"{slug}: descriptor")
        descriptor = read_json(path)
        reject_external_references(descriptor, f"descriptor.{slug}")
        reject_current_head(descriptor, f"descriptor.{slug}")
        assert_equal(descriptor.get("review"), None, f"{slug}: descriptor review")
        assert_equal(descriptor.get("curatorial_significance"), None, f"{slug}: curatorial significance")
        dep = descriptor.get("dependency", {})
        verify_stable_dependency(dep, f"{slug}: descriptor dependency")
        for key in ("source_snapshot_commit", "acquisition_commit", "rarity_tool_merge_commit", "rarity_tool_sha256", "rarity_tool_git_blob_oid"):
            assert_equal(dep.get(key), package_dependency.get(key), f"{slug}: dependency {key}")
        descriptor_input = descriptor.get("input", {})
        collection = by_slug[slug]
        snapshot_path = within(output_dir, collection["snapshot_path"], label=f"{slug}: descriptor snapshot input")
        assert_equal(descriptor.get("collection", {}).get("name"), config_by_slug[slug]["name"], f"{slug}: descriptor name")
        assert_equal(str(descriptor.get("collection", {}).get("contract_address")).lower(), config_by_slug[slug]["contract_address"].lower(), f"{slug}: descriptor contract")
        assert_equal(descriptor.get("collection", {}).get("project_id"), config_by_slug[slug]["project_id"], f"{slug}: descriptor project")
        assert_equal(descriptor_input.get("source_snapshot_commit"), package_dependency["source_snapshot_commit"], f"{slug}: source snapshot dependency")
        assert_equal(descriptor_input.get("acquisition_commit"), package_dependency["acquisition_commit"], f"{slug}: acquisition dependency")
        assert_equal(descriptor_input.get("snapshot_sha256"), collection["snapshot_file_sha256"], f"{slug}: snapshot hash")
        assert_equal(descriptor_input.get("tool_input_sha256"), f"sha256:{sha256_bytes(snapshot_path.read_bytes())}", f"{slug}: exact tool input hash")
        assert_equal(descriptor_input.get("compatibility_projection", {}).get("removed_paths"), [], f"{slug}: tool projection")
        assert_equal(descriptor_input.get("compatibility_projection", {}).get("mode"), "byte_identical_source_snapshot", f"{slug}: tool input mode")
        assert_equal(descriptor_input.get("request_provenance_sha256"), manifest["request_provenance"]["sha256"], f"{slug}: request provenance hash")
        assert_equal(descriptor_input.get("exclusion_summary_sha256"), manifest["exclusion_summary"]["sha256"], f"{slug}: exclusion hash")
        snapshot = read_json(snapshot_path)
        for key, source_key in (("source_token_order", "source_token_order"), ("canonical_token_order", "canonical_token_order"), ("source_trait_order", "source_trait_row_order"), ("canonical_trait_order", "canonical_trait_order")):
            assert_equal(descriptor_input.get(key), snapshot["ordering"][source_key], f"{slug}: {key}")
        result = descriptor.get("result")
        if not isinstance(result, dict) or result.get("schema") != "6529nm.generative-trait-analysis-output/v1":
            raise VerificationError(f"{slug}: result schema missing")
        reject_external_metrics(descriptor_input, f"descriptor.{slug}.input")
        reject_external_references(result, f"descriptor.{slug}.result")
        result_input = result.get("input")
        if isinstance(result_input, dict):
            reject_external_metrics(result_input, f"descriptor.{slug}.result.input")
        assert_equal(result.get("determinism"), EXPECTED_RARITY_RUNTIME, f"{slug}: recorded rarity runtime")
        result_bytes = (json.dumps(result, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
        assert_equal(f"sha256:{sha256_bytes(result_bytes)}", descriptor.get("result_sha256"), f"{slug}: result hash")
        with tempfile.TemporaryDirectory(prefix=f"casey-verify-{slug}-") as temp_dir:
            result_path = Path(temp_dir) / "result.json"
            completed = subprocess.run([sys.executable, str(tool), str(snapshot_path), "--duplicates", "error", "--output", str(result_path)], cwd=ROOT, text=True, capture_output=True, check=False)
            if completed.returncode != 0 or not result_path.is_file():
                raise VerificationError(f"{slug}: merged PR4 tool recomputation failed: {completed.stderr.strip()}")
            recomputed_bytes = result_path.read_bytes()
            assert_equal(f"sha256:{sha256_bytes(recomputed_bytes)}", descriptor.get("result_sha256"), f"{slug}: merged PR4 byte result hash")
            assert_equal(recomputed_bytes, result_bytes, f"{slug}: merged PR4 byte recomputation ({PR4_RESULT_SERIALIZATION})")
            assert_equal(read_json(result_path), result, f"{slug}: merged PR4 semantic result recomputation")
    return len(jobs)


def verify_fixture(output_dir: Path) -> int:
    fixture = read_json(within(output_dir, "fixtures/features-materialization.json", label="materialization fixture"))
    assert_equal(fixture.get("schema_version"), "6529nm.features-materialization-fixture.v1", "materialization fixture schema")
    count = 0
    for case in fixture.get("cases", []):
        actual = {key: scalar_text(value) for key, value in case["features"].items()}
        assert_equal(actual, case["expected_scalar_text"], f"materialization fixture {case.get('name')}")
        count += 1
    projection = read_json(within(output_dir, "fixtures/tool-input-projection.json", label="tool-input projection fixture"))
    assert_equal(projection.get("schema_version"), "6529nm.casey-tool-input-projection-fixture.v2", "tool input fixture schema")
    assert_equal(projection.get("mode"), "byte_identical_source_snapshot", "tool input fixture mode")
    assert_equal(projection.get("removed_paths"), [], "tool input fixture removals")
    return count


def verify_package(output_dir: Path) -> dict[str, Any]:
    repo_root = ROOT
    package_root = within(repo_root, PACKAGE_PREFIX.rstrip("/"), require_file=False, label="Casey package root")
    requested_output = Path(output_dir)
    if not requested_output.is_absolute():
        requested_output = repo_root / requested_output
    if requested_output != package_root:
        raise VerificationError(f"output directory is not the governed Casey package root: {output_dir}")
    output_dir = package_root
    latest_path = within(output_dir, "latest-run.json", label="latest-run pointer")
    latest = read_json(latest_path)
    reject_external_references(latest, "latest-run")
    manifest_path = within(output_dir, latest["manifest_path"])
    manifest = read_json(manifest_path)
    assert_equal(latest.get("status"), "complete", "latest status")
    assert_equal(manifest.get("run_id"), RUN_ID, "run id")
    assert_equal(manifest.get("status"), "complete", "manifest status")
    assert_equal(f"sha256:{sha256_bytes(manifest_path.read_bytes())}", latest.get("manifest_sha256"), "child manifest pointer hash")
    config = read_json(within(output_dir, "collection-sources.json", label="acquisition configuration"))
    config_by_slug = validate_config(config)
    reject_external_metrics(config, "collection-sources")
    package_path = within(output_dir, "package-manifest.json", label="root package manifest")
    package = read_json(package_path)
    reject_external_references(package, "root package")
    assert_equal(latest.get("package_manifest", {}).get("sha256"), f"sha256:{sha256_bytes(package_path.read_bytes())}", "root package manifest pointer hash")
    assert_equal(package.get("schema_version"), "6529nm.casey-package-manifest.v1", "root package manifest schema")
    assert_equal(package.get("review"), None, "root package review")
    reject_current_head(package, "root package")
    verify_stable_dependency(package.get("dependency", {}), "root package dependency")
    inventory_scope = package.get("inventory_scope")
    if not isinstance(inventory_scope, dict):
        raise VerificationError("root inventory scope is missing")
    assert_equal(inventory_scope.get("package_prefix"), PACKAGE_PREFIX, "root inventory package prefix")
    assert_equal(inventory_scope.get("external_inventory_roles"), EXPECTED_EXTERNAL_INVENTORY_ROLES, "root inventory external allowlist")
    assert_equal(inventory_scope.get("pinned_dependency_paths"), ["scripts/check_fetch_guard.py", "scripts/rarity/analyze.py", "scripts/safe_fetch.py"], "root inventory pinned dependency paths")
    assert_equal(package["dependency"].get("acquisition_commit"), ACQUISITION_COMMIT, "acquisition source commit")
    published_source_commit = latest.get("published_source_commit")
    assert_equal(published_source_commit, PUBLISHED_SOURCE_COMMIT, "published source commit")
    verify_commit_id(published_source_commit, "published source commit")
    assert_equal(package.get("network_fetch_status"), "offline_reconstruction_only_after_v2_acquisition", "root network-fetch status")
    verify_pr7_dependency(package.get("pr7_safety_dependency"), repo_root)
    inventory = package.get("inventory", {}).get("files")
    inventory_summary = package.get("inventory", {})
    if not isinstance(inventory, list) or len(inventory) != inventory_summary.get("file_count"):
        raise VerificationError("root inventory is incomplete")
    if len({item.get("path") for item in inventory}) != len(inventory):
        raise VerificationError("root inventory contains duplicate paths")
    inventory_paths = {item.get("path") for item in inventory}
    if "evidence/casey-reas-collection-snapshots/package-manifest.json" in inventory_paths or "evidence/casey-reas-collection-snapshots/latest-run.json" in inventory_paths:
        raise VerificationError("root inventory pointer exclusion is not fail-closed")
    run_root = within(output_dir, f"runs/{RUN_ID}", require_file=False, label="acquisition run root")
    verify_inventory_scope(run_root, manifest, inventory)
    for item in inventory:
        path = verify_file_record(repo_root, item)
        if path.suffix.lower() == ".json":
            artifact = read_json(path)
            reject_external_references(artifact, f"inventory.{item['path']}")
            if item.get("role") in {"raw-observation", "metadata-snapshot", "acquisition-child-manifest", "derived-provenance", "authoritative-acquisition-config"}:
                reject_external_metrics(artifact, f"inventory.{item['path']}")
    assert_equal(inventory_summary.get("raw_file_count"), sum(item.get("role") == "raw-observation" for item in inventory), "root raw inventory count")
    assert_equal(inventory_summary.get("derived_file_count"), sum(item.get("role") == "derived-provenance" for item in inventory), "root derived inventory count")
    assert_equal(inventory_summary.get("descriptor_count"), sum(item.get("role") == "descriptor" for item in inventory), "root descriptor inventory count")
    assert_equal(inventory_summary.get("raw_file_count"), EXPECTED_RAW_FILES, "root raw count")
    assert_equal(inventory_summary.get("descriptor_count"), len(EXPECTED), "root descriptor count")
    inventory_by_path = {item["path"]: item for item in inventory}
    bindings = package.get("semantic_bindings")
    if not isinstance(bindings, dict):
        raise VerificationError("root semantic bindings are missing")
    for binding_name, binding in bindings.items():
        binding_items = binding if binding_name == "descriptors" else [binding]
        if not isinstance(binding_items, list):
            raise VerificationError(f"root semantic binding is malformed: {binding_name}")
        for item in binding_items:
            if not isinstance(item, dict) or item.get("path") not in inventory_by_path:
                raise VerificationError(f"root semantic binding is not inventory-bound: {binding_name}")
            if not item["path"].startswith(PACKAGE_PREFIX) and item["path"] not in PINNED_EXTERNAL_SEMANTIC_PATHS:
                raise VerificationError(f"root semantic binding escapes package scope: {binding_name}")
            inventory_item = inventory_by_path[item["path"]]
            assert_equal(item.get("sha256"), inventory_item.get("sha256"), f"root semantic binding hash {binding_name}")
            assert_equal(item.get("size"), inventory_item.get("size"), f"root semantic binding size {binding_name}")
    expected_descriptor_paths = {item["path"] for item in inventory if item.get("role") == "descriptor"}
    assert_equal({item.get("path") for item in bindings.get("descriptors", [])}, expected_descriptor_paths, "root descriptor semantic bindings")
    expected_binding_paths = {
        "config": "evidence/casey-reas-collection-snapshots/collection-sources.json",
        "acquisition_manifest": str(Path("evidence/casey-reas-collection-snapshots") / "runs" / RUN_ID / "run-manifest.json").replace("\\", "/"),
        "descriptor_manifest": "evidence/casey-reas-collection-snapshots/descriptor-manifest.json",
        "pending_review_ledger": "evidence/casey-reas-collection-snapshots/pending-descriptors.json",
    }
    for binding_name, expected_path in expected_binding_paths.items():
        assert_equal(bindings[binding_name].get("path"), expected_path, f"root {binding_name} path")
    assert_equal(bindings["request_provenance"].get("path"), str(Path("evidence/casey-reas-collection-snapshots") / "runs" / RUN_ID / manifest["request_provenance"]["path"]).replace("\\", "/"), "root request provenance binding")
    assert_equal(bindings["exclusion_summary"].get("path"), str(Path("evidence/casey-reas-collection-snapshots") / "runs" / RUN_ID / manifest["exclusion_summary"]["path"]).replace("\\", "/"), "root exclusion binding")
    raw_root = within(run_root, "raw", require_file=False, label="raw observation tree")
    raw_files = iter_regular_files_no_follow(raw_root, "raw observations")
    raw_paths = {str(path.relative_to(repo_root)).replace("\\", "/") for path in raw_files}
    inventory_raw_paths = {item["path"] for item in inventory if item.get("role") == "raw-observation"}
    assert_equal(raw_paths, inventory_raw_paths, "root raw file inventory")
    assert_equal(len(raw_paths), EXPECTED_RAW_FILES, "raw file count")
    reject_external_metrics(manifest, "run-manifest")
    raw_refs = collect_raw_refs(manifest)
    for row in manifest["collections"]:
        snapshot = read_json(within(output_dir, row["snapshot_path"], label=f"{row['slug']}: metadata snapshot"))
        reject_external_metrics(snapshot, f"snapshot.{row['slug']}")
        raw_refs.update(collect_raw_refs(snapshot))
    raw_refs.update(collect_raw_refs(json.loads(verify_derived_ref(run_root, manifest["request_provenance"]).decode("utf-8"))))
    raw_refs.update(collect_raw_refs(json.loads(verify_derived_ref(run_root, manifest["exclusion_summary"]).decode("utf-8"))))
    assert_equal(raw_refs, {str(path.relative_to(run_root)).replace("\\", "/") for path in raw_files}, "all raw observations are referenced")
    for relative in sorted(raw_paths):
        verify_git_bytes(published_source_commit, relative, within(repo_root, relative, label=f"published raw source {relative}").read_bytes(), "published raw source")
    for row in manifest["collections"]:
        relative = str((Path("evidence/casey-reas-collection-snapshots") / row["snapshot_path"]).as_posix())
        verify_git_bytes(published_source_commit, relative, within(repo_root, relative, label=f"published snapshot {relative}").read_bytes(), "published snapshot")
    verify_git_bytes(published_source_commit, str((Path("evidence/casey-reas-collection-snapshots") / latest["manifest_path"]).as_posix()), manifest_path.read_bytes(), "published child manifest")
    for raw_path in raw_files:
        try:
            reject_external_metrics(json.loads(raw_path.read_text(encoding="utf-8")), f"raw.{raw_path.name}")
        except UnicodeDecodeError as error:
            raise VerificationError(f"raw observation is not UTF-8 JSON: {raw_path}") from error
    verify_block_and_population(output_dir, run_root, manifest, config_by_slug)
    total_traits = verify_materialization(output_dir, run_root, manifest, config_by_slug)
    request_summary = verify_request_provenance(output_dir, run_root, manifest, config_by_slug)
    exclusions = verify_exclusions(run_root, manifest, config_by_slug)
    descriptor_count = verify_descriptors(output_dir, manifest, package, config_by_slug)
    fixture_count = verify_fixture(output_dir)
    if len(manifest.get("cross_check_warnings", [])) != 8:
        raise VerificationError("cross-check warning count changed")
    assert_equal(sha256_bytes(canonical_json(manifest["cross_check_warnings"])), CROSS_CHECK_WARNINGS_SHA256, "cross-check warning bytes")
    return {"status": "verified", "run_id": RUN_ID, "total_tokens": 3300, "total_traits": total_traits, "raw_files": len(raw_paths), "request_records": request_summary["records"], "token_uri_requests": request_summary["token_uri"], "unique_request_bodies": request_summary["unique_request_bodies"], "excluded_http_group_rows": exclusions, "descriptor_outputs": descriptor_count, "fixture_cases": fixture_count, "cross_check_warnings": len(manifest["cross_check_warnings"]), "rarity_outputs_emitted": True}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args(argv)
    try:
        print(json.dumps(verify_package(args.output_dir), ensure_ascii=False, indent=2))
    except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError, VerificationError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
