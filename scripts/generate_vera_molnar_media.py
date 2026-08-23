#!/usr/bin/env python3
"""Generate or verify deterministic presentation media for accession 6529NM.2026.003."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from datetime import datetime
from pathlib import Path
import re
import sys
from typing import Any

from PIL import Image, ImageOps

from canonical import canonicalize


ROOT = Path(__file__).resolve().parents[1]
ACCESSION_ID = "6529NM.2026.003"
ACCESSION_ROOT = ROOT / "records" / "accessions" / ACCESSION_ID
MANIFEST_PATH = ACCESSION_ROOT / "public" / "presentation-manifest.json"
MEDIA_ROOT = ROOT / "media" / "accessions" / ACCESSION_ID
SOURCE_SUMMARY = ROOT / "evidence" / "vera-molnar-210-sources" / "summary.json"
SOURCE_PATH = (
    ROOT
    / "evidence"
    / "vera-molnar-210-sources"
    / "raw"
    / "official-preview.png"
)
SOURCE_ID = "official-preview"
CDN_BASE = "https://d3lqz0a4bldqgf.cloudfront.net"
CDN_PREFIX = f"museum/accessions/{ACCESSION_ID}"
WIDTHS = (640, 1280, 2400)
TRANSFORM_PATH = "webp-v2-q82-m6-fixed-icc"
TRANSFORM_PROFILE = "6529NM_WEB_PRESENTATION_WEBP_V2_Q82_M6_FIXED_ICC"
CACHE_CONTROL = "public, max-age=31536000, immutable"
RFC3339_UTC = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z$")
DISPLAY_AUTHORITY_ID = "6529NM.2026.003.DISPLAY-01"
DISPLAY_AUTHORITY_PATH = (
    "records/accessions/6529NM.2026.003/public/web-presentation-authority.md"
)


class VeraMediaError(ValueError):
    """Raised when the presentation package is incomplete or stale."""


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise VeraMediaError(f"unable to read {path.relative_to(ROOT)}: {exc}") from exc
    if not isinstance(value, dict):
        raise VeraMediaError(f"JSON root is not an object: {path.relative_to(ROOT)}")
    return value


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def load_transform_module():
    path = ROOT / "scripts" / "generate_program_media.py"
    spec = importlib.util.spec_from_file_location("museum_program_media", path)
    if spec is None or spec.loader is None:
        raise VeraMediaError("unable to load the canonical transform implementation")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def source_record() -> dict[str, Any]:
    summary = load_json(SOURCE_SUMMARY)
    entries = summary.get("entries")
    if (
        summary.get("accession_id") != ACCESSION_ID
        or not isinstance(entries, list)
        or summary.get("media", {}).get("official_preview")
        != {"height": 2400, "mode": "RGBA", "width": 2400}
    ):
        raise VeraMediaError("source-evidence identity or geometry mismatch")
    matches = [
        row
        for row in entries
        if isinstance(row, dict) and row.get("source_id") == SOURCE_ID
    ]
    if len(matches) != 1:
        raise VeraMediaError("official preview source is not unique")
    return matches[0]


def normalized_sha256(value: Any) -> str:
    digest = str(value)
    return digest if digest.startswith("sha256:") else f"sha256:{digest}"


def media_profile(media_id: str) -> dict[str, Any]:
    entity = load_json(ROOT / "records" / "entities" / f"{media_id}.json")
    payload = entity.get("payload")
    profile = payload.get("profile") if isinstance(payload, dict) else None
    media = profile.get("media") if isinstance(profile, dict) else None
    if not isinstance(media, dict):
        raise VeraMediaError(f"missing media profile: {media_id}")
    return media


def write_immutable(path: Path, payload: bytes) -> None:
    if path.exists():
        if path.read_bytes() != payload:
            raise VeraMediaError(
                f"refusing to overwrite different immutable bytes: {path.relative_to(ROOT)}"
            )
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(payload)


def generate_item(work_id: str, media_id: str, transform) -> dict[str, Any]:
    source = source_record()
    expected_sha = normalized_sha256(source.get("sha256", ""))
    expected_size = source.get("size")
    source_url = str(source.get("url", ""))
    alt_text = media_profile(media_id).get("accessibility_text")
    if transform.sha256_file(SOURCE_PATH) != expected_sha or SOURCE_PATH.stat().st_size != expected_size:
        raise VeraMediaError("official preview fixity mismatch")
    if not isinstance(alt_text, str) or len(alt_text.strip()) < 20:
        raise VeraMediaError(f"reviewed alt text missing: {media_id}")

    with Image.open(SOURCE_PATH) as raw:
        raw.load()
        if Image.MIME.get(raw.format or "") != "image/png":
            raise VeraMediaError("official preview is not PNG")
        orientation = raw.getexif().get(274, 1)
        source_icc = raw.info.get("icc_profile")
        if source_icc is not None and not isinstance(source_icc, bytes):
            raise VeraMediaError("official preview contains a malformed ICC profile")
        normalized, colour_status, output_icc = transform.normalize_colour(
            ImageOps.exif_transpose(raw), source_icc
        )
        if normalized.size != (2400, 2400):
            raise VeraMediaError("official preview geometry mismatch")
        digest = expected_sha.removeprefix("sha256:")
        derivatives: list[dict[str, Any]] = []
        for width in WIDTHS:
            payload, height = transform.webp_bytes(normalized, width, output_icc)
            relative = Path(
                "media",
                "accessions",
                ACCESSION_ID,
                work_id,
                digest,
                TRANSFORM_PATH,
                f"{width}.webp",
            )
            write_immutable(ROOT / relative, payload)
            key = "/".join(
                (CDN_PREFIX, work_id, digest, TRANSFORM_PATH, f"{width}.webp")
            )
            derivatives.append(
                {
                    "width": width,
                    "height": height,
                    "mime_type": "image/webp",
                    "sha256": transform.sha256_bytes(payload),
                    "byte_size": len(payload),
                    "repository_path": relative.as_posix(),
                    "url": f"{CDN_BASE}/{key}",
                    "cache_control": CACHE_CONTROL,
                }
            )

    return {
        "work_entity_id": work_id,
        "media_reference_entity_id": media_id,
        "source": {
            "role": "fixity_verified_token_source",
            "url": source_url,
            "mime_type": "image/png",
            "sha256": expected_sha,
            "byte_size": expected_size,
            "pixel_width": 2400,
            "pixel_height": 2400,
            "exif_orientation_applied": orientation not in {None, 1},
            "colour_profile_status": colour_status,
        },
        "presentation": {
            "role": "web_presentation_surrogate",
            "alt_text": alt_text,
            "alt_text_status": "reviewed_accessibility_description",
            "public_widths": list(WIDTHS),
            "derivatives": derivatives,
        },
    }


def generate(
    work_id: str, media_id: str, generated_at: str, actor_id: str
) -> dict[str, Any]:
    if not RFC3339_UTC.fullmatch(generated_at):
        raise VeraMediaError("generated-at must be a canonical RFC 3339 UTC timestamp")
    transform = load_transform_module()
    return {
        "$schema": "../../../../schemas/accession-media-presentation-v2.schema.json",
        "record_control": {
            "revision": 1,
            "record_status": "constructed",
            "constructor": {
                "actor_id": actor_id,
                "role": "constructor",
                "constructed_at": generated_at,
            },
            "review": None,
        },
        "record_type": "ACCESSION_MEDIA_PRESENTATION",
        "schema_profile": "6529NM_ACCESSION_MEDIA_PRESENTATION_V2",
        "accession_lot_id": ACCESSION_ID,
        "generated_at": generated_at,
        "transform": {
            "profile": TRANSFORM_PROFILE,
            "implementation": f"Pillow {Image.__version__}",
            "format": "image/webp",
            "quality": 82,
            "method": 6,
            "widths": list(WIDTHS),
            "resize_filter": "Lanczos",
            "upscale": False,
            "orientation": "EXIF transpose before resize",
            "colour_management": "embedded profiles converted to sRGB; untagged sources treated as sRGB; alpha retained",
            "icc_profile_sha256": transform.SRGB_ICC_SHA256,
            "metadata": "source metadata stripped; output sRGB ICC profile retained",
        },
        "delivery": {
            "status": "prepared_for_contextual_museum_display_pending_review",
            "authority_record_id": DISPLAY_AUTHORITY_ID,
            "authority_path": DISPLAY_AUTHORITY_PATH,
            "cdn_base_url": CDN_BASE,
            "cache_control": CACHE_CONTROL,
            "key_profile": "museum/accessions/{accession_lot_id}/{work_entity_id}/{source_sha256}/{transform_profile}/{width}.webp",
            "overwrite_policy": "fail if an existing key does not contain the declared bytes",
        },
        "rights_boundary": {
            "status": "CC BY-NC 4.0; Museum display and noncommercial reuse subject to attribution and the license",
            "source_originals": "The exact Art Blocks preview remains the recorded source object and is not replaced by these delivery surrogates.",
            "technical_transformation": "Proportion-preserving resize, sRGB normalization and WebP compression for browser delivery; no crop, watermark, retouching or content alteration.",
            "no_general_reuse": "No permission is asserted beyond CC BY-NC 4.0; reuse must preserve attribution, remain noncommercial and comply with the license.",
        },
        "items": [generate_item(work_id, media_id, transform)],
    }


def promote_reviewed(
    value: dict[str, Any], *, reviewer_id: str, reviewed_at: str, reviewed_commit: str
) -> dict[str, Any]:
    """Apply the sole permitted review promotion to a constructed manifest."""

    if not RFC3339_UTC.fullmatch(reviewed_at):
        raise VeraMediaError("reviewed-at must be a canonical RFC 3339 UTC timestamp")
    if not re.fullmatch(r"[0-9a-f]{40}", reviewed_commit):
        raise VeraMediaError("reviewed-commit must be 40 lowercase hexadecimal characters")
    control = value.get("record_control")
    delivery = value.get("delivery")
    if (
        not isinstance(control, dict)
        or control.get("record_status") != "constructed"
        or control.get("review") is not None
        or not isinstance(delivery, dict)
        or delivery.get("status")
        != "prepared_for_contextual_museum_display_pending_review"
    ):
        raise VeraMediaError("presentation manifest is not a review-pending candidate")
    constructed_at = str(control.get("constructor", {}).get("constructed_at", ""))
    if datetime.fromisoformat(reviewed_at.replace("Z", "+00:00")) <= datetime.fromisoformat(
        constructed_at.replace("Z", "+00:00")
    ):
        raise VeraMediaError("reviewed-at must follow construction")
    promoted = json.loads(json.dumps(value))
    promoted["delivery"]["status"] = "approved_for_contextual_museum_display"
    material = {key: item for key, item in promoted.items() if key != "record_control"}
    promoted["record_control"]["record_status"] = "reviewed"
    promoted["record_control"]["review"] = {
        "actor_id": reviewer_id,
        "role": "reviewer",
        "reviewed_at": reviewed_at,
        "reviewed_commit": reviewed_commit,
        "outcome": "approved",
        "payload_sha256": "sha256:" + hashlib.sha256(canonicalize(material)).hexdigest(),
    }
    return promoted


def verify() -> tuple[int, int]:
    value = load_json(MANIFEST_PATH)
    if (
        value.get("$schema")
        != "../../../../schemas/accession-media-presentation-v2.schema.json"
        or value.get("record_type") != "ACCESSION_MEDIA_PRESENTATION"
        or value.get("schema_profile") != "6529NM_ACCESSION_MEDIA_PRESENTATION_V2"
        or value.get("accession_lot_id") != ACCESSION_ID
        or not RFC3339_UTC.fullmatch(str(value.get("generated_at", "")))
        or value.get("record_control", {}).get("constructor", {}).get("constructed_at")
        != value.get("generated_at")
        or value.get("delivery", {}).get("authority_record_id")
        != DISPLAY_AUTHORITY_ID
        or value.get("delivery", {}).get("authority_path")
        != DISPLAY_AUTHORITY_PATH
    ):
        raise VeraMediaError("presentation manifest identity mismatch")
    authority_text = (ROOT / DISPLAY_AUTHORITY_PATH).read_text(encoding="utf-8")
    if (
        f"record_id: {DISPLAY_AUTHORITY_ID}" not in authority_text
        or "status: active" not in authority_text
    ):
        raise VeraMediaError("active display authority is missing")
    items = value.get("items")
    if not isinstance(items, list) or len(items) != 1 or not isinstance(items[0], dict):
        raise VeraMediaError("presentation manifest must contain exactly one item")
    item = items[0]
    work_id = str(item.get("work_entity_id", ""))
    media_id = str(item.get("media_reference_entity_id", ""))
    source = item.get("source")
    presentation = item.get("presentation")
    expected = source_record()
    if (
        not isinstance(source, dict)
        or source.get("url") != expected.get("url")
        or source.get("sha256") != normalized_sha256(expected.get("sha256"))
        or source.get("byte_size") != expected.get("size")
        or source.get("mime_type") != "image/png"
        or source.get("pixel_width") != 2400
        or source.get("pixel_height") != 2400
        or not isinstance(presentation, dict)
        or presentation.get("alt_text")
        != media_profile(media_id).get("accessibility_text")
    ):
        raise VeraMediaError("presentation manifest source binding mismatch")
    derivatives = presentation.get("derivatives")
    if (
        not isinstance(derivatives, list)
        or [row.get("width") for row in derivatives if isinstance(row, dict)]
        != list(WIDTHS)
    ):
        raise VeraMediaError("responsive derivative set is incomplete")
    expected_paths: set[str] = set()
    total = 0
    transform = load_transform_module()
    digest = str(source.get("sha256", "")).removeprefix("sha256:")
    for derivative in derivatives:
        if not isinstance(derivative, dict):
            raise VeraMediaError("invalid derivative record")
        width = derivative.get("width")
        relative = Path(
            "media",
            "accessions",
            ACCESSION_ID,
            work_id,
            digest,
            TRANSFORM_PATH,
            f"{width}.webp",
        ).as_posix()
        expected_url = f"{CDN_BASE}/{CDN_PREFIX}/{work_id}/{digest}/{TRANSFORM_PATH}/{width}.webp"
        path = ROOT / Path(*relative.split("/"))
        if (
            derivative.get("repository_path") != relative
            or derivative.get("url") != expected_url
            or derivative.get("cache_control") != CACHE_CONTROL
            or derivative.get("height") != int(width)
            or not path.is_file()
            or transform.sha256_file(path) != derivative.get("sha256")
            or path.stat().st_size != derivative.get("byte_size")
        ):
            raise VeraMediaError(f"derivative binding mismatch: {work_id}/{width}")
        with Image.open(path) as image:
            if (
                image.format != "WEBP"
                or image.size != (width, width)
                or not image.info.get("icc_profile")
            ):
                raise VeraMediaError(f"derivative format mismatch: {relative}")
        expected_paths.add(relative)
        total += path.stat().st_size
    actual_paths = {
        path.relative_to(ROOT).as_posix()
        for path in MEDIA_ROOT.rglob("*")
        if path.is_file()
    }
    if actual_paths != expected_paths:
        raise VeraMediaError("accession derivative inventory is not closed")
    return len(expected_paths), total


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--work-entity-id")
    parser.add_argument("--media-reference-entity-id")
    parser.add_argument("--generated-at")
    parser.add_argument("--actor-id")
    parser.add_argument("--promote-reviewed", action="store_true")
    parser.add_argument("--reviewer-id")
    parser.add_argument("--reviewed-at")
    parser.add_argument("--reviewed-commit")
    args = parser.parse_args(argv)
    try:
        if args.check:
            count, total = verify()
            print(f"Vera presentation manifest is current: {count} derivatives, {total} bytes")
            return 0
        if args.promote_reviewed:
            if not all((args.reviewer_id, args.reviewed_at, args.reviewed_commit)):
                raise VeraMediaError(
                    "review promotion requires reviewer-id, reviewed-at and reviewed-commit"
                )
            write_json(
                MANIFEST_PATH,
                promote_reviewed(
                    load_json(MANIFEST_PATH),
                    reviewer_id=args.reviewer_id,
                    reviewed_at=args.reviewed_at,
                    reviewed_commit=args.reviewed_commit,
                ),
            )
            count, total = verify()
            print(f"promoted {MANIFEST_PATH.relative_to(ROOT)}: {count} derivatives, {total} bytes")
            return 0
        if not all(
            (
                args.work_entity_id,
                args.media_reference_entity_id,
                args.generated_at,
                args.actor_id,
            )
        ):
            raise VeraMediaError(
                "generation requires work/media IDs, generated-at and actor-id"
            )
        write_json(
            MANIFEST_PATH,
            generate(
                args.work_entity_id,
                args.media_reference_entity_id,
                args.generated_at,
                args.actor_id,
            ),
        )
        count, total = verify()
        print(f"wrote {MANIFEST_PATH.relative_to(ROOT)}: {count} derivatives, {total} bytes")
        return 0
    except (OSError, VeraMediaError, ValueError) as exc:
        print(f"Vera presentation media error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
