#!/usr/bin/env python3
"""Deterministic Museum-off-chain to Stream v2 CollectionRecord adapter.

The Museum envelope remains an off-chain JSON serialization.  This module
only produces the exact typed Stream tuple/commitment inputs; it does not
claim that a record is admitted, authorized, or deployable on a Stream
collection.
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

from Crypto.Hash import keccak


STREAM_SOURCE_COMMIT = "f610e04979bf9a8f4f48b31131e7e0e8f78bac43"
STREAM_INTERFACE_PATH = "smart-contracts/interfaces/stream/IStreamPreservationRecords.sol"
STREAM_IMPLEMENTATION_PATH = "smart-contracts/domains/preservation/StreamPreservationRecords.sol"
STREAM_RECORD_HASH_DOMAIN = "6529stream.preservation-record.v2"
ZERO32 = "0x" + "0" * 64
STREAM_EMPTY_CANONICALIZATION = ZERO32
MUSEUM_JCS_ID = "0x886c7c89c308c459ca8a626e0ef36a5ea9f4c7a7b56aaf86c71a2ddf3b4f9044"
LOGICAL_RECORD_BASE = "https://6529networkmuseum.org/records/"
IMMUTABLE_RAW_BASE = "https://raw.githubusercontent.com/6529-Collections/6529networkmuseum/"
FULL_COMMIT = re.compile(r"^[0-9a-f]{40}$")
SHA256_DIGEST = re.compile(r"^sha256:[0-9a-f]{64}$")
KECCAK_DIGEST = re.compile(r"^0x[0-9a-f]{64}$")
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
MANIFEST_PATH = "release-artifacts/latest/record-manifest.json"
MAX_STREAM_URI_BYTES = 2048
MAX_STREAM_DIGEST_BYTES = 128
FIXED_32_BYTE_ALGORITHMS = frozenset({1, 2, 3, 6})
VARIABLE_DIGEST_ALGORITHMS = frozenset({4, 5})
BINARY_EXTENSIONS = frozenset({".webp", ".png", ".jpg", ".jpeg", ".gif", ".avif", ".pdf", ".woff", ".woff2", ".ttf"})

# Stream keeps recordType open/nonzero. These are Museum adapter pins, not a
# claim that Stream itself has admitted these preimages to its family registry.
MUSEUM_RECORD_TYPE_PREIMAGES = {
    "PUBLIC_ENTITY": "PUBLIC_ENTITY",
    "PUBLIC_RELATION": "PUBLIC_RELATION",
    "WAVE_STATUS_OBSERVATION": "WAVE_STATUS_OBSERVATION",
    "WAVE_PUBLICATION_OBSERVATION": "WAVE_PUBLICATION_OBSERVATION",
    "MEDIA_DESCRIPTION_AMENDMENT": "MEDIA_DESCRIPTION_AMENDMENT",
    "PUBLICATION_CATALOG": "PUBLICATION_CATALOG",
}


class StreamAdapterError(ValueError):
    """Raised when a Museum envelope cannot be mapped fail-closed."""


class StreamAdmissionError(StreamAdapterError):
    """Raised when registry/collection/writer admission is not established."""


def keccak256(data: bytes) -> bytes:
    digest = keccak.new(digest_bits=256)
    digest.update(data)
    return digest.digest()


def _hex_bytes(value: Any, field: str, *, allow_empty: bool = False) -> bytes:
    if not isinstance(value, str) or not value.startswith("0x"):
        raise StreamAdapterError(f"{field} must be a 0x-prefixed hex string")
    raw = value[2:]
    if not allow_empty and not raw:
        raise StreamAdapterError(f"{field} must not be empty")
    if len(raw) % 2 or any(char not in "0123456789abcdefABCDEF" for char in raw):
        raise StreamAdapterError(f"{field} is not byte-aligned hexadecimal")
    return bytes.fromhex(raw)


def _bytes32(value: Any, field: str, *, allow_zero: bool = True) -> str:
    raw = _hex_bytes(value, field)
    if len(raw) != 32:
        raise StreamAdapterError(f"{field} must contain exactly 32 bytes")
    if not allow_zero and raw == b"\x00" * 32:
        raise StreamAdapterError(f"{field} must be nonzero")
    return "0x" + raw.hex()


def _word_uint(value: int) -> bytes:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0 or value >= 2**256:
        raise StreamAdapterError(f"invalid ABI uint value {value!r}")
    return value.to_bytes(32, "big")


def _nonzero_uint64(value: Any, field: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0 or value >= 2**64:
        raise StreamAdapterError(f"{field} must be a nonzero uint64")
    return value


def _word_bytes32(value: str, field: str, *, allow_zero: bool = True) -> bytes:
    return _hex_bytes(_bytes32(value, field, allow_zero=allow_zero), field)


def museum_record_type_to_stream(record_type: str) -> str:
    preimage = MUSEUM_RECORD_TYPE_PREIMAGES.get(record_type)
    if preimage is None:
        raise StreamAdapterError(f"record type is not admitted to the Museum adapter pin: {record_type!r}")
    return "0x" + keccak256(preimage.encode("ascii")).hex()


def _hash_ref_hash(ref: dict[str, Any]) -> bytes:
    algorithm = ref.get("algorithm")
    if isinstance(algorithm, bool) or not isinstance(algorithm, int) or algorithm < 0 or algorithm > 65535:
        raise StreamAdapterError("HashRef.algorithm must be a uint16")
    digest = _hex_bytes(ref.get("digest"), "HashRef.digest", allow_empty=True)
    canonicalization_id = _word_bytes32(ref.get("canonicalizationId"), "HashRef.canonicalizationId")
    return keccak256(_word_uint(algorithm) + keccak256(digest) + canonicalization_id)


def _normalize_hash_ref(ref: Any, field: str, *, unsigned_signature: bool = False) -> dict[str, Any]:
    if not isinstance(ref, dict):
        raise StreamAdapterError(f"{field} must be an object")
    algorithm = ref.get("algorithm")
    digest = ref.get("digest")
    canonicalization_id = ref.get("canonicalizationId")
    if isinstance(algorithm, bool):
        raise StreamAdapterError(f"{field}.algorithm must be an integer, not a boolean")
    if unsigned_signature:
        # The Museum's legacy unsigned placeholder is algorithm 2 + zero32 +
        # JCS. Stream v2's unsigned HashRef is algorithm 0 + empty bytes + 0.
        if algorithm == 2 and digest == ZERO32 and canonicalization_id == MUSEUM_JCS_ID:
            return {"algorithm": 0, "digest": "0x", "canonicalizationId": ZERO32}
        if algorithm != 0 or digest != "0x" or canonicalization_id != ZERO32:
            raise StreamAdapterError("unsigned Stream signature must use algorithm 0, empty digest, and zero canonicalizationId")
        return {"algorithm": 0, "digest": "0x", "canonicalizationId": ZERO32}
    if not isinstance(algorithm, int) or isinstance(algorithm, bool) or algorithm < 1 or algorithm > 6:
        raise StreamAdapterError(f"{field}.algorithm must be a nonzero supported Stream hash algorithm")
    digest_bytes = _hex_bytes(digest, f"{field}.digest")
    if algorithm in FIXED_32_BYTE_ALGORITHMS and len(digest_bytes) != 32:
        raise StreamAdapterError(f"{field}.digest must contain 32 bytes for algorithm {algorithm}")
    if algorithm in VARIABLE_DIGEST_ALGORITHMS and not (1 <= len(digest_bytes) <= MAX_STREAM_DIGEST_BYTES):
        raise StreamAdapterError(
            f"{field}.digest must contain between 1 and {MAX_STREAM_DIGEST_BYTES} bytes for algorithm {algorithm}"
        )
    canonicalization = _bytes32(canonicalization_id, f"{field}.canonicalizationId", allow_zero=False)
    return {"algorithm": algorithm, "digest": "0x" + digest_bytes.hex(), "canonicalizationId": canonicalization}


def _safe_source_path(path: str) -> None:
    if (
        not isinstance(path, str)
        or not path
        or path.startswith("/")
        or path.startswith("./")
        or "\\" in path
        or any(part in {"", ".", ".."} for part in path.split("/"))
        or any(part.casefold() in {".git", "release-artifacts"} for part in path.split("/"))
        or any(char in path for char in "*?[]{}!#%")
        or any(ord(char) < 0x20 or ord(char) == 0x7F for char in path)
    ):
        raise StreamAdapterError(f"source path is not a safe governed literal: {path!r}")


def _strict_json_bytes(data: bytes, field: str) -> dict[str, Any]:
    def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        value: dict[str, Any] = {}
        for key, item in pairs:
            if key in value:
                raise StreamAdapterError(f"{field} contains duplicate JSON key {key!r}")
            value[key] = item
        return value

    try:
        parsed = json.loads(data.decode("utf-8"), object_pairs_hook=reject_duplicates)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise StreamAdapterError(f"{field} is not strict UTF-8 JSON: {exc}") from exc
    if not isinstance(parsed, dict):
        raise StreamAdapterError(f"{field} must contain a JSON object")
    return parsed


def _git_blob_bytes(root: Path, commit: str, path: str) -> bytes:
    try:
        resolved_result = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "--verify", f"{commit}^{{commit}}"],
            capture_output=True,
            text=True,
            check=False,
        )
        if resolved_result.returncode:
            raise StreamAdapterError("exact governed Git commit could not be resolved")
        resolved = resolved_result.stdout.strip()
        if resolved != commit:
            raise StreamAdapterError("source_commit does not resolve to the exact supplied commit")
        lookup = subprocess.run(
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
                path,
            ],
            capture_output=True,
            check=False,
        )
        if lookup.returncode:
            raise StreamAdapterError("exact governed Git source could not be resolved")
        rows = [row for row in lookup.stdout.split(b"\0") if row]
        if len(rows) != 1:
            raise StreamAdapterError(f"governed source path is absent at exact commit: {path}")
        metadata, separator, listed_path = rows[0].partition(b"\t")
        try:
            listed_path_text = listed_path.decode("utf-8")
            parts = metadata.decode("ascii").split()
        except UnicodeDecodeError as exc:
            raise StreamAdapterError(f"governed source path is not a canonical UTF-8 Git path: {path}") from exc
        if (
            separator != b"\t"
            or listed_path_text != path
            or len(parts) != 3
            or parts[1] != "blob"
            or parts[0] not in {"100644", "100755"}
        ):
            raise StreamAdapterError(f"governed source path is not one exact regular Git blob: {path}")
        blob = subprocess.run(
            ["git", "-C", str(root), "cat-file", "blob", f"{commit}:{path}"],
            capture_output=True,
            check=False,
        )
        if blob.returncode:
            raise StreamAdapterError(f"exact governed Git blob could not be read: {path}")
        return blob.stdout
    except OSError as exc:
        raise StreamAdapterError("exact governed Git source could not be resolved") from exc


def _manifest_bytes(path: str, raw: bytes) -> tuple[bytes, str]:
    if Path(path).suffix.casefold() in BINARY_EXTENSIONS:
        return raw, "raw"
    return raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n"), "lf-normalized"


def _manifest_entries(manifest: dict[str, Any]) -> dict[str, dict[str, Any]]:
    if manifest.get("manifest_type") != "6529NM_RECORD_MANIFEST" or not isinstance(manifest.get("manifest_version"), str) or not SEMVER.fullmatch(manifest["manifest_version"]):
        raise StreamAdapterError("exact B manifest has an invalid type or version")
    hash_algorithms = manifest.get("hash_algorithms")
    if (
        not isinstance(hash_algorithms, dict)
        or type(hash_algorithms.get("keccak256")) is not int
        or type(hash_algorithms.get("sha256")) is not int
        or hash_algorithms != {"keccak256": 1, "sha256": 2}
    ):
        raise StreamAdapterError("exact B manifest hash algorithm registry drifted")
    canonicalization = manifest.get("canonicalization")
    if not isinstance(canonicalization, dict) or canonicalization.get("id") != MUSEUM_JCS_ID:
        raise StreamAdapterError("exact B manifest canonicalization pin drifted")

    entries = manifest.get("entries")
    if not isinstance(entries, list) or not entries:
        raise StreamAdapterError("exact B manifest entries are unavailable")
    by_path: dict[str, dict[str, Any]] = {}
    for entry in entries:
        if not isinstance(entry, dict) or not isinstance(entry.get("path"), str):
            raise StreamAdapterError("exact B manifest contains an invalid entry")
        path = entry["path"]
        _safe_source_path(path)
        if path in by_path:
            raise StreamAdapterError(f"exact B manifest contains a duplicate path: {path}")
        size = entry.get("size")
        if isinstance(size, bool) or not isinstance(size, int) or size < 0:
            raise StreamAdapterError(f"exact B manifest entry has an invalid size: {path}")
        if not isinstance(entry.get("sha256"), str) or not SHA256_DIGEST.fullmatch(entry["sha256"]):
            raise StreamAdapterError(f"exact B manifest entry has an invalid SHA-256: {path}")
        if entry.get("byte_mode") not in {"raw", "lf-normalized"}:
            raise StreamAdapterError(f"exact B manifest entry has an invalid byte mode: {path}")
        by_path[path] = entry
    if list(by_path) != sorted(by_path):
        raise StreamAdapterError("exact B manifest paths must be sorted")

    body = dict(manifest)
    manifest_sha256 = body.pop("manifest_sha256", None)
    commitment = body.pop("manifest_commitment", None)
    if not isinstance(manifest_sha256, str) or not SHA256_DIGEST.fullmatch(manifest_sha256):
        raise StreamAdapterError("exact B manifest is missing a valid SHA-256 body commitment")
    if (
        not isinstance(commitment, dict)
        or type(commitment.get("algorithm")) is not int
        or commitment.get("algorithm") != 1
        or commitment.get("canonicalizationId") != MUSEUM_JCS_ID
        or not isinstance(commitment.get("digest"), str)
        or not KECCAK_DIGEST.fullmatch(commitment["digest"])
    ):
        raise StreamAdapterError("exact B manifest is missing a valid Keccak/JCS body commitment")
    try:
        canonical_body = canonical_json(body)
    except (TypeError, ValueError, OverflowError) as exc:
        raise StreamAdapterError("exact B manifest body is not canonicalizable") from exc
    expected_sha256 = "sha256:" + hashlib.sha256(canonical_body).hexdigest()
    expected_keccak = "0x" + keccak256(canonical_body).hex()
    if manifest_sha256 != expected_sha256 or commitment["digest"] != expected_keccak:
        raise StreamAdapterError("exact B manifest body commitments are inconsistent")
    return by_path


def _read_exact_source(
    payload: dict[str, Any] | None,
    *,
    source_root: Path | None,
    source_commit: str,
    source_path: str,
) -> dict[str, Any]:
    if source_root is None or payload is None or not isinstance(payload, dict):
        raise StreamAdapterError(
            "immutable Stream URI derivation requires source_root and source_payload proof"
        )
    root = source_root.resolve()
    manifest = _strict_json_bytes(
        _git_blob_bytes(root, source_commit, MANIFEST_PATH),
        "exact B manifest",
    )
    entries = _manifest_entries(manifest)
    manifest_entry = entries.get(source_path)
    if manifest_entry is None:
        raise StreamAdapterError("governed source path is not admitted by the exact B manifest")
    source_raw = _git_blob_bytes(root, source_commit, source_path)
    source_bytes, expected_byte_mode = _manifest_bytes(source_path, source_raw)
    if (
        manifest_entry["size"] != len(source_bytes)
        or manifest_entry["byte_mode"] != expected_byte_mode
        or manifest_entry["sha256"] != "sha256:" + hashlib.sha256(source_bytes).hexdigest()
    ):
        raise StreamAdapterError("exact B manifest entry does not describe the governed source bytes")
    source_record = _strict_json_bytes(source_bytes, "exact governed source record")
    if source_record.get("payload") != payload:
        raise StreamAdapterError("exact governed source payload does not match the adapter input")
    return source_record


def _verify_exact_source(
    envelope: dict[str, Any],
    payload: dict[str, Any] | None,
    *,
    source_root: Path | None,
    source_commit: str,
    source_path: str,
) -> None:
    source_record = _read_exact_source(
        payload,
        source_root=source_root,
        source_commit=source_commit,
        source_path=source_path,
    )
    if source_record.get("envelope") != envelope:
        raise StreamAdapterError("exact governed source envelope does not match the adapter input")


def _validate_stream_uri(uri: Any) -> str:
    if not isinstance(uri, str) or not uri:
        raise StreamAdapterError("CollectionRecord.uri must be a non-empty UTF-8 string")
    try:
        encoded = uri.encode("utf-8")
    except UnicodeEncodeError as exc:
        raise StreamAdapterError("CollectionRecord.uri must be valid UTF-8") from exc
    if len(encoded) > MAX_STREAM_URI_BYTES:
        raise StreamAdapterError(
            f"CollectionRecord.uri exceeds the Stream {MAX_STREAM_URI_BYTES}-byte limit"
        )
    if any(char.isspace() or ord(char) < 0x20 or ord(char) == 0x7F for char in uri):
        raise StreamAdapterError("CollectionRecord.uri must not contain whitespace or control characters")
    return uri


def _record_uri(
    envelope: dict[str, Any],
    *,
    source_commit: str | None,
    source_path: str | None,
    source_root: Path | None = None,
    source_payload: dict[str, Any] | None = None,
    allow_logical_uri: bool = False,
    allow_verified_immutable_raw_uri: bool = False,
) -> str:
    uri = envelope.get("uri")
    if source_commit is not None or source_path is not None:
        if not isinstance(source_commit, str) or not FULL_COMMIT.fullmatch(source_commit) or not isinstance(source_path, str):
            raise StreamAdapterError("immutable Stream URI derivation requires a full B commit and governed source path")
        _safe_source_path(source_path)
        _verify_exact_source(
            envelope,
            source_payload,
            source_root=source_root,
            source_commit=source_commit,
            source_path=source_path,
        )
        return _validate_stream_uri(IMMUTABLE_RAW_BASE + source_commit + "/" + source_path)
    if not allow_logical_uri:
        raise StreamAdapterError("immutable Stream URI derivation requires a full B commit and governed source path")
    uri = _validate_stream_uri(uri)
    lowered = uri.casefold()
    if "/blob/main/" in lowered or "/blob/head/" in lowered or "/raw/main/" in lowered or "/raw/head/" in lowered:
        raise StreamAdapterError("Stream adapter rejects moving branch/blob URIs; supply exact B commit/path or a stable logical URI")
    if uri.startswith("https://github.com/") and "/blob/" in uri:
        parts = uri.split("/blob/", 1)[1].split("/", 1)
        if len(parts) != 2 or not FULL_COMMIT.fullmatch(parts[0]):
            raise StreamAdapterError("GitHub source URI must bind a full immutable commit")
    parsed = urlsplit(uri)
    if parsed.scheme == "https" and parsed.netloc == "raw.githubusercontent.com":
        if not allow_verified_immutable_raw_uri:
            raise StreamAdapterError(
                "raw Museum source URIs require exact source-root, commit, path, and payload proof"
            )
        marker = "/6529-Collections/6529networkmuseum/"
        if not parsed.path.startswith(marker) or parsed.query or parsed.fragment:
            raise StreamAdapterError("raw Stream URI must bind the Museum repository")
        suffix = parsed.path[len(marker) :]
        commit, _, path = suffix.partition("/")
        if not FULL_COMMIT.fullmatch(commit) or not path:
            raise StreamAdapterError("raw Stream URI must bind a full immutable commit")
        _safe_source_path(path)
        return uri
    if (
        parsed.scheme == "https"
        and parsed.netloc == "6529networkmuseum.org"
        and parsed.path.startswith("/records/")
        and not parsed.query
        and not parsed.fragment
    ):
        logical_path = parsed.path[len("/records/") :]
        _safe_source_path(logical_path)
        return uri
    raise StreamAdapterError("logical Stream URI must use the Museum logical record host")


def _source_proof_supplied(
    *,
    source_envelope: dict[str, Any] | None,
    source_payload: dict[str, Any] | None,
    source_root: str | Path | None,
    source_commit: str | None,
    source_path: str | None,
) -> bool:
    values = (source_envelope, source_payload, source_root, source_commit, source_path)
    if not any(value is not None for value in values):
        return False
    if any(value is None for value in (source_payload, source_root, source_commit, source_path)):
        raise StreamAdapterError(
            "existing raw Stream URIs require source_payload, source_root, source_commit, and source_path proof"
        )
    if source_envelope is not None and not isinstance(source_envelope, dict):
        raise StreamAdapterError("source_envelope proof must be an object")
    if not isinstance(source_payload, dict):
        raise StreamAdapterError("source_payload proof must be an object")
    if not isinstance(source_root, (str, Path)) or not str(source_root):
        raise StreamAdapterError("source proof requires a non-empty repository root")
    if not isinstance(source_commit, str) or not FULL_COMMIT.fullmatch(source_commit):
        raise StreamAdapterError("source proof requires a full lowercase Git commit")
    if not isinstance(source_path, str):
        raise StreamAdapterError("source proof requires a governed source path")
    return True


def _verify_stream_record_source_proof(
    record: dict[str, Any],
    *,
    source_envelope: dict[str, Any] | None,
    source_payload: dict[str, Any],
    source_root: str | Path,
    source_commit: str,
    source_path: str,
) -> None:
    if source_envelope is None:
        source_record = _read_exact_source(
            source_payload,
            source_root=Path(source_root),
            source_commit=source_commit,
            source_path=source_path,
        )
        source_envelope = source_record.get("envelope")
        if not isinstance(source_envelope, dict):
            raise StreamAdapterError("exact governed source envelope is not an object")
    expected = museum_envelope_to_stream_record(
        source_envelope,
        source_commit=source_commit,
        source_path=source_path,
        source_payload=source_payload,
        source_root=source_root,
    )
    if expected != record:
        raise StreamAdapterError(
            "existing raw Stream URI does not match the exact Git/manifest/envelope/payload proof"
        )


def museum_envelope_to_stream_record(
    envelope: dict[str, Any],
    *,
    source_commit: str | None = None,
    source_path: str | None = None,
    source_payload: dict[str, Any] | None = None,
    source_root: str | Path | None = None,
    allow_logical_uri: bool = False,
) -> dict[str, Any]:
    """Map the Museum envelope fields to the exact v2 CollectionRecord tuple."""

    if not isinstance(envelope, dict):
        raise StreamAdapterError("Museum envelope must be an object")
    normalized_source_root: Path | None = None
    if source_root is not None:
        if not isinstance(source_root, (str, Path)) or not str(source_root):
            raise StreamAdapterError("source_root must be a non-empty repository root")
        normalized_source_root = Path(source_root)
    record_type = envelope.get("recordType")
    stream_record = {
        "recordType": museum_record_type_to_stream(record_type),
        "subjectId": _bytes32(envelope.get("subjectId"), "envelope.subjectId", allow_zero=False),
        "contentHash": _normalize_hash_ref(envelope.get("contentHash"), "envelope.contentHash"),
        "uri": _record_uri(
            envelope,
            source_commit=source_commit,
            source_path=source_path,
            source_root=normalized_source_root,
            source_payload=source_payload,
            allow_logical_uri=allow_logical_uri,
        ),
        "schemaId": _bytes32(envelope.get("schemaId"), "envelope.schemaId", allow_zero=False),
        "signatureScheme": _bytes32(envelope.get("signatureScheme"), "envelope.signatureScheme"),
        "signatureHash": None,
        "effectiveAt": envelope.get("effectiveAt"),
    }
    _nonzero_uint64(stream_record["effectiveAt"], "CollectionRecord.effectiveAt")
    if source_payload is not None:
        expected_payload_hash = "0x" + keccak256(canonical_json(source_payload)).hex()
        content_hash = stream_record["contentHash"]
        if content_hash["algorithm"] != 1 or content_hash["digest"] != expected_payload_hash:
            raise StreamAdapterError("immutable source payload does not match the Museum contentHash commitment")
    unsigned = stream_record["signatureScheme"] == ZERO32
    stream_record["signatureHash"] = _normalize_hash_ref(envelope.get("signatureHash"), "envelope.signatureHash", unsigned_signature=unsigned)
    return stream_record


def canonical_json(value: Any) -> bytes:
    """Encode a payload using the Museum's canonical JSON helper without importing the CLI."""

    from canonical import canonicalize

    return canonicalize(value)


def stream_record_to_semantic_json(
    record: dict[str, Any],
    *,
    source_envelope: dict[str, Any] | None = None,
    source_payload: dict[str, Any] | None = None,
    source_root: str | Path | None = None,
    source_commit: str | None = None,
    source_path: str | None = None,
) -> dict[str, Any]:
    """Return the normalized JSON form used for deterministic round trips."""

    required = ("recordType", "subjectId", "contentHash", "uri", "schemaId", "signatureScheme", "signatureHash", "effectiveAt")
    if not isinstance(record, dict) or any(key not in record for key in required):
        raise StreamAdapterError("CollectionRecord must contain the exact eight v2 fields")
    record_type = next((name for name, preimage in MUSEUM_RECORD_TYPE_PREIMAGES.items() if "0x" + keccak256(preimage.encode("ascii")).hex() == record["recordType"]), None)
    if record_type is None:
        raise StreamAdapterError("CollectionRecord uses an unknown Museum recordType pin")
    source_proof = _source_proof_supplied(
        source_envelope=source_envelope,
        source_payload=source_payload,
        source_root=source_root,
        source_commit=source_commit,
        source_path=source_path,
    )
    if source_proof:
        _verify_stream_record_source_proof(
            record,
            source_envelope=source_envelope,
            source_payload=source_payload,
            source_root=source_root,
            source_commit=source_commit,
            source_path=source_path,
        )
    uri = {"uri": record.get("uri")}
    _record_uri(
        uri,
        source_commit=None,
        source_path=None,
        allow_logical_uri=True,
        allow_verified_immutable_raw_uri=source_proof,
    )
    effective_at = _nonzero_uint64(record.get("effectiveAt"), "CollectionRecord.effectiveAt")
    signature_scheme = _bytes32(record.get("signatureScheme"), "signatureScheme")
    normalized = {
        "recordType": museum_record_type_to_stream(record_type),
        "subjectId": _bytes32(record.get("subjectId"), "subjectId", allow_zero=False),
        "contentHash": _normalize_hash_ref(record.get("contentHash"), "contentHash"),
        "uri": record["uri"],
        "schemaId": _bytes32(record.get("schemaId"), "schemaId", allow_zero=False),
        "signatureScheme": signature_scheme,
        "signatureHash": _normalize_hash_ref(record.get("signatureHash"), "signatureHash", unsigned_signature=signature_scheme == ZERO32),
        "effectiveAt": effective_at,
    }
    if normalized != record:
        raise StreamAdapterError("CollectionRecord is not normalized or uses an unknown Museum recordType pin")
    return normalized


def _encode_dynamic_bytes(value: bytes) -> bytes:
    padding = (32 - (len(value) % 32)) % 32
    return _word_uint(len(value)) + value + b"\x00" * padding


def _encode_hash_ref(ref: dict[str, Any]) -> bytes:
    algorithm = ref["algorithm"]
    digest = _hex_bytes(ref["digest"], "HashRef.digest", allow_empty=True)
    canonicalization = _word_bytes32(ref["canonicalizationId"], "HashRef.canonicalizationId")
    return _word_uint(algorithm) + _word_uint(96) + canonicalization + _encode_dynamic_bytes(digest)


def encode_collection_record_tuple_body(
    record: dict[str, Any],
    *,
    source_envelope: dict[str, Any] | None = None,
    source_payload: dict[str, Any] | None = None,
    source_root: str | Path | None = None,
    source_commit: str | None = None,
    source_path: str | None = None,
) -> bytes:
    """Encode the dynamic tuple body (without the outer single-argument offset)."""

    record = stream_record_to_semantic_json(
        record,
        source_envelope=source_envelope,
        source_payload=source_payload,
        source_root=source_root,
        source_commit=source_commit,
        source_path=source_path,
    )
    content_tail = _encode_hash_ref(record["contentHash"])
    signature_tail = _encode_hash_ref(record["signatureHash"])
    uri_tail = _encode_dynamic_bytes(record["uri"].encode("utf-8"))
    head_size = 32 * 8
    content_offset = head_size
    uri_offset = content_offset + len(content_tail)
    signature_offset = uri_offset + len(uri_tail)
    head = (
        _word_bytes32(record["recordType"], "recordType", allow_zero=False)
        + _word_bytes32(record["subjectId"], "subjectId", allow_zero=False)
        + _word_uint(content_offset)
        + _word_uint(uri_offset)
        + _word_bytes32(record["schemaId"], "schemaId", allow_zero=False)
        + _word_bytes32(record["signatureScheme"], "signatureScheme")
        + _word_uint(signature_offset)
        + _word_uint(record["effectiveAt"])
    )
    return head + content_tail + uri_tail + signature_tail


def encode_collection_record_abi(
    record: dict[str, Any],
    *,
    source_envelope: dict[str, Any] | None = None,
    source_payload: dict[str, Any] | None = None,
    source_root: str | Path | None = None,
    source_commit: str | None = None,
    source_path: str | None = None,
) -> bytes:
    """Encode ``abi.encode(record)`` for one dynamic CollectionRecord argument."""

    return _word_uint(32) + encode_collection_record_tuple_body(
        record,
        source_envelope=source_envelope,
        source_payload=source_payload,
        source_root=source_root,
        source_commit=source_commit,
        source_path=source_path,
    )


def derive_collection_record_hash(
    record: dict[str, Any],
    *,
    chain_id: int,
    contract_address: str,
    stream_core: str,
    collection_id: int,
    source_envelope: dict[str, Any] | None = None,
    source_payload: dict[str, Any] | None = None,
    source_root: str | Path | None = None,
    source_commit: str | None = None,
    source_path: str | None = None,
) -> str:
    """Derive the exact v2 Solidity record hash preimage."""

    record = stream_record_to_semantic_json(
        record,
        source_envelope=source_envelope,
        source_payload=source_payload,
        source_root=source_root,
        source_commit=source_commit,
        source_path=source_path,
    )
    address = _hex_bytes(contract_address, "address")
    core = _hex_bytes(stream_core, "streamCore")
    if len(address) != 20 or len(core) != 20:
        raise StreamAdapterError("contract_address and stream_core must be 20-byte addresses")
    words = (
        keccak256(STREAM_RECORD_HASH_DOMAIN.encode("ascii"))
        + _word_uint(chain_id)
        + b"\x00" * 12 + address
        + b"\x00" * 12 + core
        + _word_uint(collection_id)
        + _word_bytes32(record["recordType"], "recordType", allow_zero=False)
        + _word_bytes32(record["subjectId"], "subjectId", allow_zero=False)
        + _hash_ref_hash(record["contentHash"])
        + keccak256(record["uri"].encode("utf-8"))
        + _word_bytes32(record["schemaId"], "schemaId", allow_zero=False)
        + _word_bytes32(record["signatureScheme"], "signatureScheme")
        + _hash_ref_hash(record["signatureHash"])
        + _word_uint(record["effectiveAt"])
    )
    return "0x" + keccak256(words).hex()


def require_stream_admission(*, known_collection: bool, family_admitted: bool, writer_authorized: bool, authorization_class: int | None = None) -> int:
    """Model the v2 registry/collection/writer gate without claiming deployment."""

    if not known_collection:
        raise StreamAdmissionError("Stream v2 requires a known Core collection")
    if not family_admitted:
        raise StreamAdmissionError("Stream v2 requires record-family registry admission")
    if not writer_authorized:
        raise StreamAdmissionError("Stream v2 requires record-writer authorization")
    if isinstance(authorization_class, bool) or not isinstance(authorization_class, int) or authorization_class <= 0 or authorization_class > 255:
        raise StreamAdmissionError("Stream v2 admission must return a nonzero authorizationClass")
    return authorization_class


def reject_legacy_unsigned_placeholder(record: dict[str, Any]) -> None:
    if record.get("signatureScheme") == ZERO32 and record.get("signatureHash") != {"algorithm": 0, "digest": "0x", "canonicalizationId": ZERO32}:
        raise StreamAdapterError("legacy Museum unsigned signature placeholder must not pass through unchanged")
