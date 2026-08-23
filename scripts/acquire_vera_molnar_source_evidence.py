#!/usr/bin/env python3
"""Retain the public source package for *Themes and Variations* #210."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from hashlib import sha256
from io import BytesIO
import json
from pathlib import Path
import ssl
import stat
import sys
import time
from typing import Any

from PIL import Image

from safe_fetch import FetchPolicyError, SafeHTTPSFetcher, _PinnedHTTPSConnection


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "evidence" / "vera-molnar-210-sources"
CONTRACT = "0xe034bb2b1b9471e11cf1a0a9199a156fb227aa5d"
TOKEN_ID = 210
TOKEN_HASH = "0xd0a3be9aa1a3e101a12ec038ceb71a18846dbc62eac3e91fb425232e7820a318"
DROP_ID = "d09d3c3b-d354-4e39-9e1f-1e676e3cb62e"
WAVE_ID = "5f207393-5418-4a75-8738-e40edb44a94d"
USER_AGENT = "6529-Network-Museum/vera-molnar-210-source-acquisition-v1"
SOURCES = (
    (
        "token-metadata",
        f"https://token.artblocks.io/{CONTRACT}/{TOKEN_ID}",
        "application/json",
    ),
    (
        "official-preview",
        f"https://media-proxy.artblocks.io/1/{CONTRACT}/{TOKEN_ID}.png",
        "image/png",
    ),
    (
        "wave-drop",
        f"https://api.6529.io/api/drops/{DROP_ID}",
        "application/json",
    ),
    (
        "wave-cover",
        "https://d3lqz0a4bldqgf.cloudfront.net/drops/author_7ee51a67-07b7-4c91-87ed-464c56446c43/a4025328-fdeb-446f-a593-020988420a25/vera-molnar-themes-and-variations-210.png",
        "image/png",
    ),
)


def http10_connection_factory(endpoint, resolved, policy):
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


class SourceEvidenceError(RuntimeError):
    """Raised when the source package is incomplete or internally inconsistent."""


def prepare_output() -> None:
    if OUTPUT.exists():
        info = OUTPUT.lstat()
        if stat.S_ISLNK(info.st_mode) or info.st_file_attributes & 0x400:
            raise SourceEvidenceError("source evidence output cannot be a link")
        if any(OUTPUT.iterdir()):
            raise SourceEvidenceError("source evidence output must be empty")
    else:
        OUTPUT.mkdir(parents=True)


def canonical_json(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def write_bytes(path: Path, value: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(value)


def parse_json(name: str, payload: bytes) -> dict[str, Any]:
    try:
        value = json.loads(payload.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise SourceEvidenceError(f"{name} is not UTF-8 JSON") from exc
    if not isinstance(value, dict):
        raise SourceEvidenceError(f"{name} JSON root is not an object")
    return value


def main() -> int:
    try:
        prepare_output()
        fetcher = SafeHTTPSFetcher(connection_factory=http10_connection_factory)
        entries: list[dict[str, Any]] = []
        bodies: dict[str, bytes] = {}
        for name, url, expected_media_type in SOURCES:
            time.sleep(0.5)
            result = fetcher.fetch(
                url,
                headers={"Accept": "*/*", "User-Agent": USER_AGENT},
                expires_at=datetime.now(UTC) + timedelta(seconds=45),
            )
            if result.observation.status != 200:
                raise SourceEvidenceError(f"{name} returned HTTP {result.observation.status}")
            observed_type = result.observation.media_type or ""
            if observed_type != expected_media_type:
                raise SourceEvidenceError(
                    f"{name} returned {observed_type!r}, expected {expected_media_type!r}"
                )
            suffix = {
                "application/json": ".json",
                "image/png": ".png",
            }[expected_media_type]
            relative = Path("raw") / f"{name}{suffix}"
            write_bytes(OUTPUT / relative, result.body)
            bodies[name] = result.body
            entries.append(
                {
                    "source_id": name,
                    "url": url,
                    "path": relative.as_posix(),
                    "media_type": expected_media_type,
                    # Evidence manifests use the repository's raw lower-case
                    # 64-hex digest profile. Higher-level record assertions
                    # retain the explicit ``sha256:`` algorithm prefix.
                    "sha256": sha256(result.body).hexdigest(),
                    "size": len(result.body),
                    "byte_mode": "raw",
                    "transport": result.observation.to_dict(),
                }
            )

        metadata = parse_json("token-metadata", bodies["token-metadata"])
        drop = parse_json("wave-drop", bodies["wave-drop"])
        if str(metadata.get("contract_address", "")).lower() != CONTRACT:
            raise SourceEvidenceError("metadata contract mismatch")
        if str(metadata.get("tokenID")) != str(TOKEN_ID):
            raise SourceEvidenceError("metadata token mismatch")
        if str(metadata.get("token_hash", "")).lower() != TOKEN_HASH:
            raise SourceEvidenceError("metadata token hash mismatch")
        if metadata.get("name") != "Themes and Variations #210":
            raise SourceEvidenceError("metadata name mismatch")
        if metadata.get("artist") != "Vera Molnár, in collaboration with Martin Grasser":
            raise SourceEvidenceError("metadata artist credit mismatch")
        if metadata.get("license") != "CC BY-NC 4.0":
            raise SourceEvidenceError("metadata license mismatch")
        if metadata.get("is_static") is not False or metadata.get("engine_type") != "flex":
            raise SourceEvidenceError("metadata technical classification mismatch")
        if drop.get("id") != DROP_ID or drop.get("serial_no") != 1_296_797:
            raise SourceEvidenceError("Wave drop identity mismatch")
        if drop.get("drop_type") != "WINNER":
            raise SourceEvidenceError("Wave drop is not WINNER")
        if len(drop.get("parts", [])) != 4:
            raise SourceEvidenceError("Wave drop does not contain four parts")

        with Image.open(BytesIO(bodies["official-preview"])) as image:
            image.load()
            preview_geometry = {"width": image.width, "height": image.height, "mode": image.mode}
        with Image.open(BytesIO(bodies["wave-cover"])) as image:
            image.load()
            cover_geometry = {"width": image.width, "height": image.height, "mode": image.mode}
        if bodies["official-preview"] != bodies["wave-cover"]:
            raise SourceEvidenceError("Wave cover bytes differ from the official preview")
        summary = {
            "record_id": "6529NM.2026.003.SOURCE-EVIDENCE-01",
            "record_type": "DIGITAL_ART_SOURCE_OBSERVATION",
            "observed_at": datetime.now(UTC).isoformat(timespec="milliseconds").replace("+00:00", "Z"),
            "accession_id": "6529NM.2026.003",
            "object_id": "6529NM.2026.003.01",
            "wave": {"wave_id": WAVE_ID, "drop_id": DROP_ID, "serial_no": 1_296_797, "status": "WINNER"},
            "object": {
                "caip19": f"eip155:1/erc721:{CONTRACT}/{TOKEN_ID}",
                "token_hash": TOKEN_HASH,
                "name": metadata["name"],
                "artist_credit": metadata["artist"],
                "license": metadata["license"],
                "engine_type": metadata["engine_type"],
                "is_static": metadata["is_static"],
                "features": metadata.get("features"),
                "authenticity_signature": metadata.get("authenticity_signature"),
            },
            "media": {
                "official_preview": preview_geometry,
                "wave_cover": cover_geometry,
                "byte_identical": True,
                "sha256": f"sha256:{sha256(bodies['official-preview']).hexdigest()}",
            },
            "assertions": {
                "official_metadata_matches_exact_object": True,
                "live_generator_url_is_recorded_from_official_metadata": True,
                "wave_decision_is_winner": True,
                "wave_cover_matches_official_preview_bytes": True,
            },
            "entries": entries,
            "limitations": [
                "These are point-in-time public-source responses and do not establish legal title or copyright ownership.",
                "Active generator HTML is not retained in this public package. The exact on-chain scripts are captured separately in the technical evidence package; service-exit reconstruction remains preservation work.",
            ],
        }
        encoded = (json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")
        write_bytes(OUTPUT / "summary.json", encoded)
        manifest = {
            "manifest_type": "6529NM_VERA_MOLNAR_210_SOURCE_EVIDENCE",
            "manifest_version": "1.0.0",
            "subject_id": "6529NM.2026.003.01",
            "hash_algorithm": "sha256",
            "byte_mode": "raw",
            "entries": [
                *[{key: value for key, value in entry.items() if key != "transport"} for entry in entries],
                {
                    "source_id": "summary",
                    "path": "summary.json",
                    "media_type": "application/json",
                    "sha256": sha256(encoded).hexdigest(),
                    "size": len(encoded),
                    "byte_mode": "raw",
                },
            ],
        }
        manifest_bytes = (json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")
        write_bytes(OUTPUT / "manifest.json", manifest_bytes)
        print(
            json.dumps(
                {
                    "status": "complete",
                    "entry_count": len(manifest["entries"]),
                    "manifest_sha256": f"sha256:{sha256(manifest_bytes).hexdigest()}",
                    "preview_sha256": summary["media"]["sha256"],
                },
                indent=2,
            )
        )
        return 0
    except (FetchPolicyError, SourceEvidenceError, OSError, ValueError) as exc:
        print(f"Vera Molnár source evidence acquisition refused: {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
