#!/usr/bin/env python3
"""Retain public-safe Museum Wave API readbacks for governance decision records.

The script reads exact drops from the public, unauthenticated 6529 API through
``safe_fetch`` and writes an evidence package with a raw-byte manifest.

A response that contains profile objects (author, raters, mentioned users, or
any object with a handle or wallet address) is never written to disk. The
package keeps instead:

- ``projections/drop-<drop-id>.json``: a public-safe projection in the Magnum
  receipt convention. An allowlisted ``payload`` carries the drop identity,
  Wave, status, rating fields, decision time, and per-part digests. Its
  ``payload_sha256`` uses the stated canonicalization, and ``raw_response``
  records the SHA-256, size, and status of the bytes that were not retained;
- ``parts/drop-<drop-id>-part-<n>.txt``: the exact UTF-8 bytes of each part's
  ``content`` string, so the proposal-content digest can be recomputed from the
  repository.

A response without profile objects, such as a 404 error body, is retained
byte-for-byte as ``raw/drop-<drop-id>.json``.

``summary.json`` lists the fields a governance record relies on and the
transport observation for every request, including the raw response digest
and length.

A ``--decision`` drop must return HTTP 200 from the Museum Wave with exactly one
text part. Its content digest is SHA-256 over the UTF-8 bytes of that part's
``content`` string as returned by the API. An optional ``:<sha256>`` suffix
makes the run fail unless the live content has that digest.

A ``--withdrawn`` drop is a proposal that repository records describe as
deleted. Its readback is kept whatever the status, so a reviewer can see
whether the drop is still absent.

The package records point-in-time API observations. It does not infer adoption
from a rating, and it does not establish acceptance, acquisition, or accession.
"""

from __future__ import annotations

import argparse
from datetime import UTC, datetime, timedelta
from hashlib import sha256
import json
from pathlib import Path
import re
import ssl
import stat
import sys
import time
from typing import Any

from safe_fetch import FetchPolicyError, SafeHTTPSFetcher, _PinnedHTTPSConnection


ROOT = Path(__file__).resolve().parents[1]
API_BASE = "https://api.6529.io/api/drops/"
MUSEUM_WAVE_ID = "5f207393-5418-4a75-8738-e40edb44a94d"
USER_AGENT = "6529-Network-Museum/wave-governance-evidence-v1"
MANIFEST_TYPE = "6529NM_WAVE_GOVERNANCE_EVIDENCE"
SUMMARY_RECORD_TYPE = "WAVE_GOVERNANCE_API_OBSERVATION"
PROJECTION_TYPE = "WAVE_DROP_PUBLIC_SAFE_PROJECTION"
UUID = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$")
SHA256_HEX = re.compile(r"^[0-9a-f]{64}$")
PACKAGE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$")
ADDRESS = re.compile(r"^0x[0-9a-fA-F]{40}$")
# Keys that identify or describe a profile. Their presence anywhere in a
# response means the raw bytes are not retained.
PROFILE_MARKER_KEYS = {"handle", "primary_address", "pfp"}
PROFILE_CONTAINER_KEYS = {"author", "top_raters", "mentioned_users", "context_profile_context", "profile"}
CANONICALIZATION = (
    "Hash the payload object only as UTF-8 JSON with recursively lexicographically sorted object keys, "
    "source-order arrays, compact separators, preserved Unicode, and no trailing newline."
)
EXCLUSION_NOTE = (
    "Public-safe projection of a live drops-API read. The retained payload keeps only the allowlisted drop "
    "identity, Wave, status, rating, decision-time, and per-part digest and media fields. It excludes the "
    "author and rater profiles, mentioned users, reactions, boosts, viewer context, wallet addresses, and all "
    "other fields. The exact part text is retained separately under parts/. The raw response bytes are not "
    "retained; raw_response records their SHA-256 and size."
)


class GovernanceEvidenceError(RuntimeError):
    """Raised when a readback is incomplete or does not match its expectation."""


def http10_connection_factory(endpoint, resolved, policy):
    # HTTP/1.0 keeps the API from answering with Transfer-Encoding, which the
    # safe-fetch policy does not admit.
    connection = _PinnedHTTPSConnection(
        endpoint,
        resolved.selected_ip,
        float(policy["connect_timeout_seconds"]),
        float(policy["read_timeout_seconds"]),
        ssl.create_default_context(),
    )
    connection._http_vsn = 10
    connection._http_vsn_str = "HTTP/1.0"
    return connection


def parse_decision(value: str) -> tuple[str, str | None]:
    drop_id, separator, expected = value.partition(":")
    if not UUID.fullmatch(drop_id):
        raise argparse.ArgumentTypeError(f"not a lowercase drop UUID: {drop_id!r}")
    if separator and not SHA256_HEX.fullmatch(expected):
        raise argparse.ArgumentTypeError(f"not a lowercase SHA-256 hex digest: {expected!r}")
    return drop_id, expected or None


def parse_withdrawn(value: str) -> str:
    if not UUID.fullmatch(value):
        raise argparse.ArgumentTypeError(f"not a lowercase drop UUID: {value!r}")
    return value


def prepare_output(output: Path) -> None:
    if output.exists():
        info = output.lstat()
        if stat.S_ISLNK(info.st_mode) or getattr(info, "st_file_attributes", 0) & 0x400:
            raise GovernanceEvidenceError("evidence output cannot be a link")
        if not output.is_dir() or any(output.iterdir()):
            raise GovernanceEvidenceError("evidence output must be an empty directory")
    else:
        output.mkdir(parents=True)


def write_bytes(path: Path, value: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_bytes(value)
    temporary.replace(path)


def encode_json(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def canonical_sha256(value: Any) -> str:
    body = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return f"sha256:{sha256(body).hexdigest()}"


def iso_from_api_time(value: Any) -> str | None:
    """Return an RFC 3339 UTC string for an API epoch-millisecond time."""

    if isinstance(value, bool) or not isinstance(value, int):
        return None
    moment = datetime.fromtimestamp(value / 1000, tz=UTC)
    return moment.isoformat(timespec="milliseconds").replace("+00:00", "Z")


def parse_object(name: str, body: bytes) -> dict[str, Any]:
    try:
        value = json.loads(body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise GovernanceEvidenceError(f"{name} is not UTF-8 JSON") from exc
    if not isinstance(value, dict):
        raise GovernanceEvidenceError(f"{name} JSON root is not an object")
    return value


def contains_profile_objects(value: Any) -> bool:
    """Return True when a response carries any profile object or wallet address."""

    if isinstance(value, dict):
        for key, child in value.items():
            if key in PROFILE_MARKER_KEYS:
                return True
            if key in PROFILE_CONTAINER_KEYS and child not in (None, [], {}):
                return True
            if contains_profile_objects(child):
                return True
        return False
    if isinstance(value, list):
        return any(contains_profile_objects(child) for child in value)
    return isinstance(value, str) and bool(ADDRESS.fullmatch(value))


def require_public_safe(value: Any, location: str = "payload") -> None:
    """Fail closed if a projection would retain a profile key or wallet address."""

    if isinstance(value, dict):
        for key, child in value.items():
            if key in PROFILE_MARKER_KEYS or key in PROFILE_CONTAINER_KEYS:
                raise GovernanceEvidenceError(f"{location}.{key}: profile field in public-safe projection")
            require_public_safe(child, f"{location}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            require_public_safe(child, f"{location}[{index}]")
    elif isinstance(value, str) and ADDRESS.fullmatch(value):
        raise GovernanceEvidenceError(f"{location}: wallet-shaped address in public-safe projection")


def part_content_path(drop_id: str, part_id: Any) -> str:
    if isinstance(part_id, bool) or not isinstance(part_id, int) or part_id < 1:
        raise GovernanceEvidenceError(f"{drop_id}: part_id must be a positive integer")
    return f"parts/drop-{drop_id}-part-{part_id}.txt"


def public_safe_projection(drop_id: str, drop: dict[str, Any]) -> tuple[dict[str, Any], dict[str, bytes]]:
    """Return the allowlisted projection payload and the exact part-content files."""

    if drop.get("id") != drop_id:
        raise GovernanceEvidenceError(f"{drop_id}: response id does not match the request")
    wave = drop.get("wave") if isinstance(drop.get("wave"), dict) else {}
    winning_context = drop.get("winning_context")
    parts = drop.get("parts")
    if not isinstance(parts, list):
        raise GovernanceEvidenceError(f"{drop_id}: response has no parts list")
    part_files: dict[str, bytes] = {}
    projected_parts: list[dict[str, Any]] = []
    for part in parts:
        if not isinstance(part, dict):
            raise GovernanceEvidenceError(f"{drop_id}: part is not an object")
        content = part.get("content")
        projected: dict[str, Any] = {
            "part_id": part.get("part_id"),
            "content_path": None,
            "content_sha256": None,
            "content_utf8_bytes": None,
            "content_utf16_code_units": None,
            "media": [
                {key: item.get(key) for key in ("url", "mime_type", "media_status")}
                for item in part.get("media") or []
                if isinstance(item, dict)
            ],
            "attachments_count": len(part.get("attachments") or []),
            "has_quoted_drop": part.get("quoted_drop") is not None,
        }
        if isinstance(content, str):
            content_bytes = content.encode("utf-8")
            path = part_content_path(drop_id, part.get("part_id"))
            if path in part_files:
                raise GovernanceEvidenceError(f"{drop_id}: duplicate part_id {part.get('part_id')}")
            part_files[path] = content_bytes
            projected.update(
                {
                    "content_path": path,
                    "content_sha256": f"sha256:{sha256(content_bytes).hexdigest()}",
                    "content_utf8_bytes": len(content_bytes),
                    "content_utf16_code_units": len(content.encode("utf-16-le")) // 2,
                }
            )
        projected_parts.append(projected)
    payload = {
        "drop_id": drop.get("id"),
        "serial_no": drop.get("serial_no"),
        "wave_id": wave.get("id"),
        "wave_name": wave.get("name"),
        "title": drop.get("title"),
        "drop_type": drop.get("drop_type"),
        "is_signed": drop.get("is_signed"),
        "rating": drop.get("rating"),
        "realtime_rating": drop.get("realtime_rating"),
        "raters_count": drop.get("raters_count"),
        "created_at": iso_from_api_time(drop.get("created_at")),
        "created_at_api_value": drop.get("created_at"),
        "winning_context": (
            {
                "place": winning_context.get("place"),
                "decision_time": iso_from_api_time(winning_context.get("decision_time")),
                "decision_time_api_value": winning_context.get("decision_time"),
            }
            if isinstance(winning_context, dict)
            else None
        ),
        "parts_count": drop.get("parts_count"),
        "parts": projected_parts,
    }
    require_public_safe(payload)
    return payload, part_files


def decision_summary(
    drop_id: str,
    expected_sha256: str | None,
    drop: dict[str, Any],
    payload: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if payload is None:
        payload, _ = public_safe_projection(drop_id, drop)
    if payload.get("wave_id") != MUSEUM_WAVE_ID:
        raise GovernanceEvidenceError(f"{drop_id}: drop is not in the Museum Wave")
    parts = payload["parts"]
    if len(parts) != 1 or not parts[0].get("content_sha256"):
        raise GovernanceEvidenceError(f"{drop_id}: decision drop must have exactly one text part")
    part = parts[0]
    if not part["content_utf8_bytes"]:
        raise GovernanceEvidenceError(f"{drop_id}: decision part has no text content")
    content_sha256 = part["content_sha256"].removeprefix("sha256:")
    if expected_sha256 is not None and content_sha256 != expected_sha256:
        raise GovernanceEvidenceError(
            f"{drop_id}: part content SHA-256 {content_sha256} differs from expected {expected_sha256}"
        )
    winning_context = payload.get("winning_context") or {}
    return {
        "drop_id": drop_id,
        "wave_id": payload["wave_id"],
        "serial_no": payload["serial_no"],
        "title": payload["title"],
        "drop_type": payload["drop_type"],
        "is_signed": payload["is_signed"],
        "rating": payload["rating"],
        "realtime_rating": payload["realtime_rating"],
        "raters_count": payload["raters_count"],
        "created_at": payload["created_at"],
        "decision_time": winning_context.get("decision_time"),
        "parts_count": payload["parts_count"],
        "part_content": {
            "part_id": part["part_id"],
            "path": part["content_path"],
            "digest_input": "UTF-8 bytes of parts[0].content exactly as returned by the API; retained at path",
            "sha256": part["content_sha256"],
            "expected_sha256": f"sha256:{expected_sha256}" if expected_sha256 else None,
            "utf8_bytes": part["content_utf8_bytes"],
            "utf16_code_units": part["content_utf16_code_units"],
        },
    }


def run(output: Path, package_id: str, decisions: list[tuple[str, str | None]], withdrawn: list[str]) -> dict[str, Any]:
    requested = [drop_id for drop_id, _ in decisions] + withdrawn
    if len(requested) != len(set(requested)):
        raise GovernanceEvidenceError("each drop may be requested only once")
    if not decisions:
        raise GovernanceEvidenceError("at least one --decision drop is required")
    prepare_output(output)
    fetcher = SafeHTTPSFetcher(connection_factory=http10_connection_factory)
    started_at = datetime.now(UTC).isoformat(timespec="milliseconds").replace("+00:00", "Z")
    files: dict[str, tuple[bytes, str, str, str]] = {}
    entries: list[dict[str, Any]] = []
    decision_rows: list[dict[str, Any]] = []
    withdrawn_rows: list[dict[str, Any]] = []
    expected_by_id = dict(decisions)
    for drop_id in requested:
        time.sleep(0.5)
        url = API_BASE + drop_id
        result = fetcher.fetch(
            url,
            headers={"Accept": "application/json", "User-Agent": USER_AGENT},
            expires_at=datetime.now(UTC) + timedelta(seconds=45),
        )
        status = result.observation.status
        media_type = result.observation.media_type or ""
        is_decision = drop_id in expected_by_id
        if is_decision and status != 200:
            raise GovernanceEvidenceError(f"{drop_id}: decision drop returned HTTP {status}")
        if media_type != "application/json":
            raise GovernanceEvidenceError(f"{drop_id}: response media type {media_type!r} is not application/json")
        body = parse_object(drop_id, result.body)
        raw_digest = sha256(result.body).hexdigest()
        entry: dict[str, Any] = {
            "source_id": f"drop-{drop_id}",
            "url": url,
            "http_status": status,
            "raw_sha256": raw_digest,
            "raw_size": len(result.body),
            "transport": result.observation.to_dict(),
        }
        payload: dict[str, Any] | None = None
        if contains_profile_objects(body):
            payload, part_files = public_safe_projection(drop_id, body)
            projection_path = f"projections/drop-{drop_id}.json"
            projection = {
                "evidence_type": PROJECTION_TYPE,
                "package_id": package_id,
                "source_url": url,
                "observed_at": result.observation.observed_at,
                "canonicalization": CANONICALIZATION,
                "payload": payload,
                "payload_sha256": canonical_sha256(payload),
                "raw_response": {
                    "retention": "not_retained",
                    "reason": "The response contains profile objects with wallet addresses.",
                    "http_status": status,
                    "media_type": media_type,
                    "sha256": f"sha256:{raw_digest}",
                    "size": len(result.body),
                },
                "exclusion_note": EXCLUSION_NOTE,
            }
            files[projection_path] = (encode_json(projection), "application/json", f"projection-{drop_id}", url)
            for path, content_bytes in part_files.items():
                files[path] = (content_bytes, "text/plain; charset=utf-8", path.removeprefix("parts/").removesuffix(".txt"), url)
            entry.update(
                {
                    "retention": "public_safe_projection",
                    "retained_paths": [projection_path, *part_files],
                }
            )
        else:
            raw_path = f"raw/drop-{drop_id}.json"
            files[raw_path] = (result.body, media_type, f"drop-{drop_id}", url)
            entry.update({"retention": "raw_response", "retained_paths": [raw_path]})
        entries.append(entry)
        if is_decision:
            row = decision_summary(drop_id, expected_by_id[drop_id], body, payload)
            row["evidence_path"] = entry["retained_paths"][0]
            row["observed_at"] = result.observation.observed_at
            row["raw_response"] = {"retained": False, "sha256": f"sha256:{raw_digest}", "size": len(result.body)}
            decision_rows.append(row)
        else:
            withdrawn_rows.append(
                {
                    "drop_id": drop_id,
                    "evidence_path": entry["retained_paths"][0],
                    "observed_at": result.observation.observed_at,
                    "http_status": status,
                    "present": status == 200,
                    "drop_type": payload.get("drop_type") if payload else None,
                    "response_keys": sorted(body) if payload is None else None,
                }
            )
    completed_at = datetime.now(UTC).isoformat(timespec="milliseconds").replace("+00:00", "Z")
    summary = {
        "record_id": package_id,
        "record_type": SUMMARY_RECORD_TYPE,
        "wave_id": MUSEUM_WAVE_ID,
        "started_at": started_at,
        "completed_at": completed_at,
        "method": (
            "Unauthenticated HTTPS GET of the public 6529 drops API through scripts/safe_fetch.py with an "
            "HTTP/1.0 connection. Responses with profile objects are kept as public-safe projections plus exact "
            "part text and the raw response digest; other responses are kept byte-for-byte."
        ),
        "decisions": decision_rows,
        "withdrawn_proposals": withdrawn_rows,
        "entries": entries,
        "limitations": [
            "These are point-in-time API readbacks. drop_type, rating, realtime_rating, and raters_count can change after observation.",
            "The API reports is_signed; this package does not verify the signature.",
            "A WINNER drop_type records the Wave's selection. It does not by itself accept, acquire, transfer, or accession any work or asset.",
            "Raw responses that contain profile objects are not retained. Their SHA-256 and length are recorded but cannot be recomputed from the repository; the projection and exact part text can.",
        ],
    }
    summary_bytes = encode_json(summary)
    files["summary.json"] = (summary_bytes, "application/json", "summary", "")
    for path, (data, _media_type, _source_id, _url) in files.items():
        write_bytes(output / path, data)
    manifest_entries = []
    for path, (data, file_media_type, source_id, source_url) in sorted(files.items()):
        manifest_entry = {
            "source_id": source_id,
            "path": path,
            "media_type": file_media_type,
            "sha256": sha256(data).hexdigest(),
            "size": len(data),
            "byte_mode": "raw",
        }
        if source_url:
            manifest_entry["url"] = source_url
        manifest_entries.append(manifest_entry)
    manifest = {
        "manifest_type": MANIFEST_TYPE,
        "manifest_version": "1.0.0",
        "package_id": package_id,
        "hash_algorithm": "sha256",
        "byte_mode": "raw",
        "entries": manifest_entries,
    }
    manifest_bytes = encode_json(manifest)
    write_bytes(output / "manifest.json", manifest_bytes)
    return {
        "status": "complete",
        "entry_count": len(manifest["entries"]),
        "manifest_sha256": f"sha256:{sha256(manifest_bytes).hexdigest()}",
        "decisions": [
            {key: row[key] for key in ("drop_id", "serial_no", "drop_type", "decision_time", "observed_at")}
            | {"part_sha256": row["part_content"]["sha256"], "raw_sha256": row["raw_response"]["sha256"]}
            for row in decision_rows
        ],
        "withdrawn_proposals": [
            {key: row[key] for key in ("drop_id", "http_status", "observed_at")} for row in withdrawn_rows
        ],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--output-dir", type=Path, required=True, help="new or empty evidence directory")
    parser.add_argument("--package-id", required=True, help="stable evidence package identifier")
    parser.add_argument(
        "--decision",
        action="append",
        type=parse_decision,
        default=[],
        metavar="DROP_ID[:SHA256]",
        help="Museum Wave decision drop; optional expected part-content SHA-256",
    )
    parser.add_argument(
        "--withdrawn",
        action="append",
        type=parse_withdrawn,
        default=[],
        metavar="DROP_ID",
        help="withdrawn proposal drop whose current readback is kept",
    )
    args = parser.parse_args(argv)
    if not PACKAGE_ID.fullmatch(args.package_id):
        parser.error("--package-id is not a valid Museum identifier")
    output = args.output_dir if args.output_dir.is_absolute() else Path.cwd() / args.output_dir
    try:
        result = run(output, args.package_id, args.decision, args.withdrawn)
    except (FetchPolicyError, GovernanceEvidenceError, OSError, ValueError) as exc:
        print(f"Wave governance evidence acquisition refused: {exc}")
        return 1
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
