#!/usr/bin/env python3
"""Generate or verify deterministic Magnum accession web-presentation media."""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

from PIL import Image, ImageCms, ImageOps


ROOT = Path(__file__).resolve().parent.parent
ACCESSION_ID = "6529NM.2026.002"
ACCESSION_ROOT = ROOT / "records" / "accessions" / ACCESSION_ID
CONTINUITY_PATH = (
    ROOT
    / "records/proposed-gifts/6529NM-PG-2026-001/public/scholarship/machine/media-source-continuity-amendment.json"
)
MANIFEST_PATH = ACCESSION_ROOT / "public" / "presentation-manifest.json"
MEDIA_ROOT = ROOT / "media" / "accessions" / ACCESSION_ID
CDN_BASE = "https://d3lqz0a4bldqgf.cloudfront.net"
CDN_PREFIX = f"museum/accessions/{ACCESSION_ID}"
WIDTHS = (640, 1280, 2400)
TRANSFORM_PATH = "webp-v2-q82-m6-fixed-icc"
TRANSFORM_PROFILE = "6529NM_WEB_PRESENTATION_WEBP_V2_Q82_M6_FIXED_ICC"
CACHE_CONTROL = "public, max-age=31536000, immutable"
DISPLAY_AUTHORITY_ID = "6529NM.2026.002.DISPLAY-01"
DISPLAY_AUTHORITY_PATH = (
    "records/accessions/6529NM.2026.002/public/web-presentation-authority.md"
)


class AccessionMediaError(ValueError):
    """Raised when an accession presentation package is incomplete or stale."""


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise AccessionMediaError(f"unable to read {path.relative_to(ROOT)}: {exc}") from exc
    if not isinstance(value, dict):
        raise AccessionMediaError(f"JSON root is not an object: {path.relative_to(ROOT)}")
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
        raise AccessionMediaError("unable to load the canonical transform implementation")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def continuity_works() -> list[dict[str, Any]]:
    value = load_json(CONTINUITY_PATH)
    works = value.get("works")
    if not isinstance(works, list) or len(works) != 5 or not all(isinstance(row, dict) for row in works):
        raise AccessionMediaError("continuity record must contain five works")
    return works


def media_profile(media_id: str) -> dict[str, Any]:
    entity = load_json(ROOT / "records" / "entities" / f"{media_id}.json")
    payload = entity.get("payload")
    profile = payload.get("profile") if isinstance(payload, dict) else None
    media = profile.get("media") if isinstance(profile, dict) else None
    if not isinstance(media, dict):
        raise AccessionMediaError(f"missing media profile: {media_id}")
    return media


def source_path(source_dir: Path, work_id: str) -> Path:
    matches = sorted(path for path in source_dir.glob(f"{work_id}.*") if path.is_file())
    if len(matches) != 1:
        raise AccessionMediaError(f"expected one source named {work_id}.*, found {len(matches)}")
    return matches[0]


def write_immutable(path: Path, payload: bytes) -> None:
    if path.exists():
        if path.read_bytes() != payload:
            raise AccessionMediaError(
                f"refusing to overwrite different immutable bytes: {path.relative_to(ROOT)}"
            )
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(payload)


def normalize_accession_colour(image: Image.Image, source_icc: bytes | None, transform):
    """Normalize RGB and grayscale museum sources to the fixed sRGB profile."""

    output_profile, output_icc = transform.fixed_srgb_profile()
    if source_icc is None:
        return image.convert("RGB"), "untagged_assumed_srgb", output_icc
    try:
        import io

        input_profile = ImageCms.ImageCmsProfile(io.BytesIO(source_icc))
        output = ImageCms.profileToProfile(
            image,
            input_profile,
            output_profile,
            outputMode="RGB",
            renderingIntent=ImageCms.Intent.PERCEPTUAL,
        )
    except (OSError, ValueError, ImageCms.PyCMSError) as exc:
        raise AccessionMediaError(f"embedded ICC profile could not be converted: {exc}") from exc
    return output, "embedded_profile_converted_to_srgb", output_icc


def generate_item(row: dict[str, Any], source_dir: Path, transform) -> dict[str, Any]:
    work_id = str(row.get("work_entity_id", ""))
    media_id = str(row.get("media_reference_entity_id", ""))
    source_url = str(row.get("display_token_source_uri", ""))
    expected_sha = str(row.get("sha256", ""))
    expected_size = row.get("bytes")
    expected_width = row.get("width")
    expected_height = row.get("height")
    media = media_profile(media_id)
    alt_text = media.get("accessibility_text")
    path = source_path(source_dir, work_id)
    if transform.sha256_file(path) != expected_sha or path.stat().st_size != expected_size:
        raise AccessionMediaError(f"source fixity mismatch: {work_id}")
    if not isinstance(alt_text, str) or len(alt_text.strip()) < 20:
        raise AccessionMediaError(f"reviewed alt text missing: {media_id}")

    with Image.open(path) as raw:
        raw.load()
        if Image.MIME.get(raw.format or "") != "image/jpeg":
            raise AccessionMediaError(f"source is not JPEG: {work_id}")
        orientation = raw.getexif().get(274, 1)
        source_icc = raw.info.get("icc_profile")
        if source_icc is not None and not isinstance(source_icc, bytes):
            raise AccessionMediaError(f"malformed ICC profile: {work_id}")
        normalized, colour_status, output_icc = normalize_accession_colour(
            ImageOps.exif_transpose(raw), source_icc, transform
        )
        if normalized.size != (expected_width, expected_height):
            raise AccessionMediaError(f"source geometry mismatch: {work_id}")
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
            "mime_type": "image/jpeg",
            "sha256": expected_sha,
            "byte_size": expected_size,
            "pixel_width": expected_width,
            "pixel_height": expected_height,
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


def generate(source_dir: Path, generated_at: str, actor_id: str) -> dict[str, Any]:
    if not source_dir.is_dir():
        raise AccessionMediaError(f"source directory does not exist: {source_dir}")
    transform = load_transform_module()
    return {
        "$schema": "../../../../schemas/accession-media-presentation.schema.json",
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
        "schema_profile": "6529NM_ACCESSION_MEDIA_PRESENTATION_V1",
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
            "colour_management": "embedded profiles converted to sRGB; untagged sources treated as sRGB; sRGB profile embedded in derivatives",
            "icc_profile_sha256": transform.SRGB_ICC_SHA256,
            "metadata": "source EXIF/XMP stripped; output sRGB ICC profile retained",
        },
        "delivery": {
            "status": "approved_for_contextual_museum_display",
            "authority_record_id": DISPLAY_AUTHORITY_ID,
            "authority_path": DISPLAY_AUTHORITY_PATH,
            "cdn_base_url": CDN_BASE,
            "cache_control": CACHE_CONTROL,
            "key_profile": "museum/accessions/{accession_lot_id}/{work_entity_id}/{source_sha256}/{transform_profile}/{width}.webp",
            "overwrite_policy": "fail if an existing key does not contain the declared bytes",
        },
        "rights_boundary": {
            "status": "All Rights Reserved; contextual Museum display only",
            "source_originals": "The exact Arweave source remains the recorded source object and is not replaced by these delivery surrogates.",
            "technical_transformation": "Proportion-preserving resize, sRGB normalization, and WebP compression for browser delivery; no crop, watermark, retouching, or content alteration.",
            "no_general_reuse": "The manifest grants no download, commercial, derivative, licensing, AI-training, or general reproduction right.",
        },
        "items": [
            generate_item(row, source_dir, transform) for row in continuity_works()
        ],
    }


def verify() -> tuple[int, int]:
    value = load_json(MANIFEST_PATH)
    delivery = value.get("delivery")
    transform_record = value.get("transform")
    if (
        value.get("record_type") != "ACCESSION_MEDIA_PRESENTATION"
        or value.get("schema_profile") != "6529NM_ACCESSION_MEDIA_PRESENTATION_V1"
        or value.get("accession_lot_id") != ACCESSION_ID
        or not isinstance(delivery, dict)
        or delivery.get("status") != "approved_for_contextual_museum_display"
        or delivery.get("authority_record_id") != DISPLAY_AUTHORITY_ID
        or delivery.get("authority_path") != DISPLAY_AUTHORITY_PATH
        or delivery.get("cdn_base_url") != CDN_BASE
        or delivery.get("cache_control") != CACHE_CONTROL
        or not isinstance(transform_record, dict)
        or transform_record.get("profile") != TRANSFORM_PROFILE
        or transform_record.get("widths") != list(WIDTHS)
    ):
        raise AccessionMediaError("manifest accession identifier mismatch")
    authority_text = (ROOT / DISPLAY_AUTHORITY_PATH).read_text(encoding="utf-8")
    if f"record_id: {DISPLAY_AUTHORITY_ID}" not in authority_text or "status: active" not in authority_text:
        raise AccessionMediaError("active display authority is missing")
    items = value.get("items")
    if not isinstance(items, list) or len(items) != 5:
        raise AccessionMediaError("manifest must contain five items")
    expected_paths: set[str] = set()
    total = 0
    transform = load_transform_module()
    continuity = {str(row.get("work_entity_id", "")): row for row in continuity_works()}
    seen_work_ids: set[str] = set()
    seen_media_ids: set[str] = set()
    for item in items:
        if not isinstance(item, dict):
            raise AccessionMediaError("manifest item is not an object")
        work_id = str(item.get("work_entity_id", ""))
        media_id = str(item.get("media_reference_entity_id", ""))
        if work_id in seen_work_ids or media_id in seen_media_ids:
            raise AccessionMediaError("manifest contains a duplicate work or media identifier")
        seen_work_ids.add(work_id)
        seen_media_ids.add(media_id)
        row = continuity.get(work_id)
        source = item.get("source")
        presentation = item.get("presentation")
        expected_alt_text = media_profile(media_id).get("accessibility_text")
        if (
            not isinstance(row, dict)
            or row.get("media_reference_entity_id") != media_id
            or not isinstance(source, dict)
            or source.get("url") != row.get("display_token_source_uri")
            or source.get("sha256") != row.get("sha256")
            or source.get("byte_size") != row.get("bytes")
            or source.get("pixel_width") != row.get("width")
            or source.get("pixel_height") != row.get("height")
            or not isinstance(presentation, dict)
            or presentation.get("alt_text") != expected_alt_text
        ):
            raise AccessionMediaError(f"manifest source binding mismatch: {work_id}")
        derivatives = presentation.get("derivatives") if isinstance(presentation, dict) else None
        if not isinstance(derivatives, list) or [d.get("width") for d in derivatives if isinstance(d, dict)] != list(WIDTHS):
            raise AccessionMediaError(f"responsive widths are incomplete: {work_id}")
        for derivative in derivatives:
            if not isinstance(derivative, dict):
                raise AccessionMediaError(f"invalid derivative: {work_id}")
            relative = str(derivative.get("repository_path", ""))
            width = derivative.get("width")
            height = derivative.get("height")
            source_digest = str(source.get("sha256", "")).removeprefix("sha256:")
            expected_relative = Path(
                "media",
                "accessions",
                ACCESSION_ID,
                work_id,
                source_digest,
                TRANSFORM_PATH,
                f"{width}.webp",
            ).as_posix()
            expected_url = f"{CDN_BASE}/{CDN_PREFIX}/{work_id}/{source_digest}/{TRANSFORM_PATH}/{width}.webp"
            expected_height = transform.derivative_height(
                int(source.get("pixel_width")),
                int(source.get("pixel_height")),
                int(width),
            )
            if (
                relative != expected_relative
                or derivative.get("url") != expected_url
                or derivative.get("cache_control") != CACHE_CONTROL
                or height != expected_height
            ):
                raise AccessionMediaError(f"derivative binding mismatch: {work_id}/{width}")
            path = ROOT / Path(*relative.split("/"))
            if not path.is_file():
                raise AccessionMediaError(f"missing derivative: {relative}")
            if transform.sha256_file(path) != derivative.get("sha256") or path.stat().st_size != derivative.get("byte_size"):
                raise AccessionMediaError(f"derivative fixity mismatch: {relative}")
            with Image.open(path) as image:
                image.verify()
            with Image.open(path) as image:
                if image.format != "WEBP" or image.size != (width, height) or not image.info.get("icc_profile"):
                    raise AccessionMediaError(f"derivative format mismatch: {relative}")
            expected_paths.add(relative)
            total += path.stat().st_size
    actual_paths = {
        path.relative_to(ROOT).as_posix()
        for path in MEDIA_ROOT.rglob("*")
        if path.is_file()
    }
    if actual_paths != expected_paths:
        raise AccessionMediaError("accession derivative inventory is not closed")
    return len(expected_paths), total


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--source-dir", type=Path)
    parser.add_argument("--generated-at")
    parser.add_argument("--actor-id")
    args = parser.parse_args(argv)
    try:
        if args.check:
            count, total = verify()
            print(f"accession media manifest is current: {count} derivatives, {total} bytes")
            return 0
        if args.source_dir is None or not args.generated_at or not args.actor_id:
            raise AccessionMediaError("generation requires --source-dir, --generated-at, and --actor-id")
        write_json(MANIFEST_PATH, generate(args.source_dir, args.generated_at, args.actor_id))
        count, total = verify()
        print(f"wrote {MANIFEST_PATH.relative_to(ROOT)}: {count} derivatives, {total} bytes")
        return 0
    except AccessionMediaError as exc:
        print(f"accession media error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
