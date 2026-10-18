#!/usr/bin/env python3
"""Generate or verify deterministic presentation media for accession 6529NM.2026.005.

The source is the token's animated GIF, retained as fixity evidence in
``evidence/xcopy-max-pain-4188-sources``.  Presentation follows schema v3
(``schemas/accession-media-presentation-v3.schema.json``):

* three still posters of the first displayed frame (640, 1280 and 2400 px)
  produced by the unchanged v2 WebP transform in ``generate_program_media.py``;
* a token-linked animation reference, bound to the IPFS ``image_hash`` CID and
  to the retained bytes, with display constraints: no autoplay, poster first,
  play only on explicit request after a flashing warning, poster only under
  ``prefers-reduced-motion``, and no larger than 768 CSS px or enlarged until a
  flash review says otherwise.

The command line matches ``generate_vera_molnar_media.py``.  Generation needs
the poster MEDIA_REFERENCE entity's reviewed ``accessibility_text`` and the
active ``DISPLAY-01`` front matter; ``--derivatives-only`` writes the three
posters from the evidence alone and prints their fixity.
"""

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
from gif_structure import GifStructureError, parse_gif


ROOT = Path(__file__).resolve().parents[1]
ACCESSION_ID = "6529NM.2026.005"
ACCESSION_ROOT = ROOT / "records" / "accessions" / ACCESSION_ID
MANIFEST_PATH = ACCESSION_ROOT / "public" / "presentation-manifest.json"
MEDIA_ROOT = ROOT / "media" / "accessions" / ACCESSION_ID
SOURCE_EVIDENCE = "evidence/xcopy-max-pain-4188-sources"
SOURCE_SUMMARY = ROOT / SOURCE_EVIDENCE / "summary.json"
SOURCE_MANIFEST = ROOT / SOURCE_EVIDENCE / "manifest.json"
SOURCE_ENTRY_PATH = "raw/token-image.gif"
SOURCE_PATH = ROOT / SOURCE_EVIDENCE / SOURCE_ENTRY_PATH
SOURCE_ID = "token-image"
IMAGE_CID = "QmTcTzTPgCyvF933oeFvB4GkPgaXtF6dKuQgvg32qqLYGF"
IPFS_GATEWAY_URL = f"https://gateway.pinata.cloud/ipfs/{IMAGE_CID}"
DEFAULT_ANIMATION_MEDIA_ID = "6529NM-MED-0060"
CDN_BASE = "https://d3lqz0a4bldqgf.cloudfront.net"
CDN_PREFIX = f"museum/accessions/{ACCESSION_ID}"
WIDTHS = (640, 1280, 2400)
TRANSFORM_PATH = "webp-v2-q82-m6-fixed-icc"
TRANSFORM_PROFILE = "6529NM_WEB_PRESENTATION_WEBP_V2_Q82_M6_FIXED_ICC"
SCHEMA_PATH = "../../../../schemas/accession-media-presentation-v3.schema.json"
SCHEMA_PROFILE = "6529NM_ACCESSION_MEDIA_PRESENTATION_V3"
CACHE_CONTROL = "public, max-age=31536000, immutable"
RFC3339_UTC = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z$")
DISPLAY_AUTHORITY_ID = f"{ACCESSION_ID}.DISPLAY-01"
DISPLAY_AUTHORITY_PATH = f"records/accessions/{ACCESSION_ID}/public/web-presentation-authority.md"
MAX_ANIMATION_CSS_WIDTH = 768
DISPLAY_CONSTRAINTS = {
    "autoplay": False,
    "initial_state": "poster",
    "activation": "explicit_visitor_request_after_warning",
    "reduced_motion": "poster_only_when_prefers_reduced_motion",
    "warning_required": True,
    "max_css_width_px": MAX_ANIMATION_CSS_WIDTH,
    "max_css_width_status": "provisional_pending_flash_review",
    "fullscreen_or_enlarged_animation": "not_permitted_pending_flash_review",
    "basis": (
        "Unreviewed Museum technical measurement of the composited frames (2026-10-18): eight frames at 50 ms "
        "loop without end, two colour states alternate 10 times per second, and black-and-white checkered streaks "
        "and mint outlines on black flash up to 10 times per second over about 5.5% of the image. The largest "
        "flashing share of a WCAG 2.3.1 ten-degree field is about 15% at 768 px, 24% at 1,536 px and 30% at "
        "2,048 px, so the animation is limited to 768 CSS px and is not enlarged or shown full screen until a "
        "flash review confirms or revises these limits."
    ),
}
RIGHTS_BOUNDARY = {
    "status": (
        "The artist's site states a CC0 (Creative Commons Zero) dedication for XCOPY artworks; the token metadata "
        "carries no licence field. The Museum asserts no copyright, and Museum display implies no affiliation with "
        "or endorsement by XCOPY."
    ),
    "source_originals": (
        "The token's animated GIF, bound on-chain by its IPFS CID, remains the source object. The Museum retains its "
        "exact bytes as preservation evidence and does not re-encode, crop or alter it."
    ),
    "technical_transformation": (
        "Still posters show the first displayed frame of eight, resized proportionally, normalized to sRGB and "
        "compressed as WebP; they document an animated work and are not the work. No crop, watermark, retouching or "
        "content alteration."
    ),
    "no_general_reuse": (
        "No permission is asserted beyond the artist's stated CC0 dedication; any reuse must not imply affiliation "
        "with or endorsement by XCOPY or the Museum."
    ),
}


class MaxPainMediaError(ValueError):
    """Raised when the presentation package is incomplete or stale."""


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise MaxPainMediaError(f"unable to read {path.relative_to(ROOT)}: {exc}") from exc
    if not isinstance(value, dict):
        raise MaxPainMediaError(f"JSON root is not an object: {path.relative_to(ROOT)}")
    return value


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def load_transform_module():
    path = ROOT / "scripts" / "generate_program_media.py"
    spec = importlib.util.spec_from_file_location("museum_program_media", path)
    if spec is None or spec.loader is None:
        raise MaxPainMediaError("unable to load the canonical transform implementation")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def source_record() -> dict[str, Any]:
    """Return the retained GIF's fixity, locations and animation facts."""

    manifest = load_json(SOURCE_MANIFEST)
    summary = load_json(SOURCE_SUMMARY)
    rows = [row for row in manifest.get("entries", []) if isinstance(row, dict) and row.get("source_id") == SOURCE_ID]
    media = summary.get("media")
    if len(rows) != 1 or not isinstance(media, dict):
        raise MaxPainMediaError("token image source is not unique in the source evidence")
    row = rows[0]
    animation = media.get("animation")
    structure = media.get("structure")
    if (
        summary.get("accession_id") != ACCESSION_ID
        or row.get("path") != SOURCE_ENTRY_PATH
        or row.get("media_type") != "image/gif"
        or row.get("ipfs_cid") != IMAGE_CID
        or media.get("sha256") != f"sha256:{row.get('sha256')}"
        or media.get("size") != row.get("size")
        or (media.get("ipfs_cid_recomputation") or {}).get("match") is not True
        or not isinstance(animation, dict)
        or not isinstance(structure, dict)
    ):
        raise MaxPainMediaError("source-evidence identity, fixity or CID binding mismatch")
    screen = structure.get("logical_screen") or {}
    return {
        "sha256": f"sha256:{row['sha256']}",
        "size": row["size"],
        "cdn_url": row.get("url"),
        "gateway_url": IPFS_GATEWAY_URL,
        "animation": {key: animation[key] for key in ("frame_count", "frame_duration_ms", "total_duration_ms", "loop")},
        "width": screen.get("width"),
        "height": screen.get("height"),
    }


def media_profile(media_id: str) -> dict[str, Any]:
    entity = load_json(ROOT / "records" / "entities" / f"{media_id}.json")
    payload = entity.get("payload")
    profile = payload.get("profile") if isinstance(payload, dict) else None
    media = profile.get("media") if isinstance(profile, dict) else None
    if not isinstance(media, dict):
        raise MaxPainMediaError(f"missing media profile: {media_id}")
    return media


def write_immutable(path: Path, payload: bytes) -> None:
    if path.exists():
        if path.read_bytes() != payload:
            raise MaxPainMediaError(f"refusing to overwrite different immutable bytes: {path.relative_to(ROOT)}")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(payload)


def verified_source_bytes(source: dict[str, Any], transform) -> bytes:
    payload = SOURCE_PATH.read_bytes()
    if transform.sha256_bytes(payload) != source["sha256"] or len(payload) != source["size"]:
        raise MaxPainMediaError("token image fixity mismatch")
    try:
        structure = parse_gif(payload)
    except GifStructureError as exc:
        raise MaxPainMediaError(f"token image is not an admitted GIF: {exc}") from exc
    delays = sorted({frame.delay_centiseconds for frame in structure.frames})
    observed = {
        "frame_count": structure.frame_count,
        "frame_duration_ms": 10 * delays[0] if len(delays) == 1 and delays[0] is not None else None,
        "total_duration_ms": 10 * structure.total_delay_centiseconds,
        "loop": "infinite" if structure.loop_count == 0 else structure.loop_count,
    }
    if observed != source["animation"] or (structure.width, structure.height) != (source["width"], source["height"]):
        raise MaxPainMediaError("token image animation facts differ from the source evidence")
    return payload


def generate_derivatives(work_id: str, transform) -> tuple[dict[str, Any], list[dict[str, Any]], str]:
    """Write the three first-frame posters and return the source facts and derivative rows."""

    source = source_record()
    verified_source_bytes(source, transform)
    with Image.open(SOURCE_PATH) as raw:
        raw.load()
        if Image.MIME.get(raw.format or "") != "image/gif" or getattr(raw, "n_frames", 1) != source["animation"]["frame_count"]:
            raise MaxPainMediaError("token image is not the recorded animated GIF")
        if raw.tell() != 0:
            raise MaxPainMediaError("poster frame is not the first frame")
        orientation = raw.getexif().get(274, 1)
        source_icc = raw.info.get("icc_profile")
        if source_icc is not None and not isinstance(source_icc, bytes):
            raise MaxPainMediaError("token image contains a malformed ICC profile")
        normalized, colour_status, output_icc = transform.normalize_colour(ImageOps.exif_transpose(raw), source_icc)
    if normalized.size != (source["width"], source["height"]):
        raise MaxPainMediaError("token image geometry mismatch")
    if normalized.mode == "RGBA" and normalized.getchannel("A").getextrema() != (255, 255):
        raise MaxPainMediaError("first frame is not fully opaque")
    digest = source["sha256"].removeprefix("sha256:")
    derivatives: list[dict[str, Any]] = []
    for width in WIDTHS:
        payload, height = transform.webp_bytes(normalized, width, output_icc)
        relative = Path("media", "accessions", ACCESSION_ID, work_id, digest, TRANSFORM_PATH, f"{width}.webp")
        write_immutable(ROOT / relative, payload)
        key = "/".join((CDN_PREFIX, work_id, digest, TRANSFORM_PATH, f"{width}.webp"))
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
    source["exif_orientation_applied"] = orientation not in {None, 1}
    return source, derivatives, colour_status


def animation_reference(source: dict[str, Any], animation_media_id: str) -> dict[str, Any]:
    return {
        "role": "token_linked_source_animation",
        "media_reference_entity_id": animation_media_id,
        "binding": {
            "kind": "ipfs_cidv0",
            "cid": IMAGE_CID,
            "token_metadata_field": "image_hash",
            "verification": "recomputed_cidv0_match",
        },
        "uri": f"ipfs://{IMAGE_CID}",
        "access_urls": [IPFS_GATEWAY_URL, source["cdn_url"]],
        "mime_type": "image/gif",
        "sha256": source["sha256"],
        "byte_size": source["size"],
        "pixel_width": source["width"],
        "pixel_height": source["height"],
        "fixity_evidence": {
            "manifest_path": f"{SOURCE_EVIDENCE}/manifest.json",
            "entry_path": SOURCE_ENTRY_PATH,
            "retained_bytes": True,
        },
        "display_constraints": dict(DISPLAY_CONSTRAINTS),
    }


def generate_item(work_id: str, media_id: str, animation_media_id: str, transform) -> dict[str, Any]:
    alt_text = media_profile(media_id).get("accessibility_text")
    if not isinstance(alt_text, str) or len(alt_text.strip()) < 20:
        raise MaxPainMediaError(f"reviewed alt text missing: {media_id}")
    media_profile(animation_media_id)
    source, derivatives, colour_status = generate_derivatives(work_id, transform)
    return {
        "work_entity_id": work_id,
        "media_reference_entity_id": media_id,
        "source": {
            "role": "fixity_verified_token_source",
            "url": source["gateway_url"],
            "mime_type": "image/gif",
            "sha256": source["sha256"],
            "byte_size": source["size"],
            "pixel_width": source["width"],
            "pixel_height": source["height"],
            "exif_orientation_applied": source["exif_orientation_applied"],
            "colour_profile_status": colour_status,
            "frame_policy": "first_frame_poster",
            "animation": source["animation"],
        },
        "presentation": {
            "role": "web_presentation_surrogate",
            "alt_text": alt_text,
            "alt_text_status": "reviewed_accessibility_description",
            "public_widths": list(WIDTHS),
            "derivatives": derivatives,
        },
        "animation_reference": animation_reference(source, animation_media_id),
    }


def generate(
    work_id: str,
    media_id: str,
    generated_at: str,
    actor_id: str,
    animation_media_id: str = DEFAULT_ANIMATION_MEDIA_ID,
) -> dict[str, Any]:
    if not RFC3339_UTC.fullmatch(generated_at):
        raise MaxPainMediaError("generated-at must be a canonical RFC 3339 UTC timestamp")
    if media_id == animation_media_id:
        raise MaxPainMediaError("poster and animation media references must be distinct entities")
    transform = load_transform_module()
    return {
        "$schema": SCHEMA_PATH,
        "record_control": {
            "revision": 1,
            "record_status": "constructed",
            "constructor": {"actor_id": actor_id, "role": "constructor", "constructed_at": generated_at},
            "review": None,
        },
        "record_type": "ACCESSION_MEDIA_PRESENTATION",
        "schema_profile": SCHEMA_PROFILE,
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
            "metadata": "first displayed frame of the animated source only; source metadata stripped; output sRGB ICC profile retained",
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
        "rights_boundary": dict(RIGHTS_BOUNDARY),
        "items": [generate_item(work_id, media_id, animation_media_id, transform)],
    }


def promote_reviewed(value: dict[str, Any], *, reviewer_id: str, reviewed_at: str, reviewed_commit: str) -> dict[str, Any]:
    """Apply the sole permitted review promotion to a constructed manifest."""

    if not RFC3339_UTC.fullmatch(reviewed_at):
        raise MaxPainMediaError("reviewed-at must be a canonical RFC 3339 UTC timestamp")
    if not re.fullmatch(r"[0-9a-f]{40}", reviewed_commit):
        raise MaxPainMediaError("reviewed-commit must be 40 lowercase hexadecimal characters")
    control = value.get("record_control")
    delivery = value.get("delivery")
    if (
        not isinstance(control, dict)
        or control.get("record_status") != "constructed"
        or control.get("review") is not None
        or not isinstance(delivery, dict)
        or delivery.get("status") != "prepared_for_contextual_museum_display_pending_review"
    ):
        raise MaxPainMediaError("presentation manifest is not a review-pending candidate")
    constructed_at = str(control.get("constructor", {}).get("constructed_at", ""))
    if datetime.fromisoformat(reviewed_at.replace("Z", "+00:00")) <= datetime.fromisoformat(constructed_at.replace("Z", "+00:00")):
        raise MaxPainMediaError("reviewed-at must follow construction")
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
        value.get("$schema") != SCHEMA_PATH
        or value.get("record_type") != "ACCESSION_MEDIA_PRESENTATION"
        or value.get("schema_profile") != SCHEMA_PROFILE
        or value.get("accession_lot_id") != ACCESSION_ID
        or not RFC3339_UTC.fullmatch(str(value.get("generated_at", "")))
        or value.get("record_control", {}).get("constructor", {}).get("constructed_at") != value.get("generated_at")
        or value.get("delivery", {}).get("authority_record_id") != DISPLAY_AUTHORITY_ID
        or value.get("delivery", {}).get("authority_path") != DISPLAY_AUTHORITY_PATH
        or value.get("rights_boundary") != RIGHTS_BOUNDARY
    ):
        raise MaxPainMediaError("presentation manifest identity mismatch")
    authority_text = (ROOT / DISPLAY_AUTHORITY_PATH).read_text(encoding="utf-8")
    if f"record_id: {DISPLAY_AUTHORITY_ID}" not in authority_text or "status: active" not in authority_text:
        raise MaxPainMediaError("active display authority is missing")
    items = value.get("items")
    if not isinstance(items, list) or len(items) != 1 or not isinstance(items[0], dict):
        raise MaxPainMediaError("presentation manifest must contain exactly one item")
    item = items[0]
    work_id = str(item.get("work_entity_id", ""))
    media_id = str(item.get("media_reference_entity_id", ""))
    source = item.get("source")
    presentation = item.get("presentation")
    reference = item.get("animation_reference")
    expected = source_record()
    transform = load_transform_module()
    verified_source_bytes(expected, transform)
    if (
        not isinstance(source, dict)
        or source.get("url") != expected["gateway_url"]
        or source.get("sha256") != expected["sha256"]
        or source.get("byte_size") != expected["size"]
        or source.get("mime_type") != "image/gif"
        or source.get("pixel_width") != expected["width"]
        or source.get("pixel_height") != expected["height"]
        or source.get("frame_policy") != "first_frame_poster"
        or source.get("animation") != expected["animation"]
        or not isinstance(presentation, dict)
        or presentation.get("alt_text") != media_profile(media_id).get("accessibility_text")
    ):
        raise MaxPainMediaError("presentation manifest source binding mismatch")
    if not isinstance(reference, dict):
        raise MaxPainMediaError("animated source has no token-linked animation reference")
    animation_media_id = str(reference.get("media_reference_entity_id", ""))
    media_profile(animation_media_id)
    if animation_media_id == media_id or reference != animation_reference(expected, animation_media_id):
        raise MaxPainMediaError("animation reference binding or display constraints mismatch")
    derivatives = presentation.get("derivatives")
    if not isinstance(derivatives, list) or [row.get("width") for row in derivatives if isinstance(row, dict)] != list(WIDTHS):
        raise MaxPainMediaError("responsive derivative set is incomplete")
    expected_paths: set[str] = set()
    total = 0
    digest = expected["sha256"].removeprefix("sha256:")
    for derivative in derivatives:
        if not isinstance(derivative, dict):
            raise MaxPainMediaError("invalid derivative record")
        width = derivative.get("width")
        relative = Path("media", "accessions", ACCESSION_ID, work_id, digest, TRANSFORM_PATH, f"{width}.webp").as_posix()
        expected_url = f"{CDN_BASE}/{CDN_PREFIX}/{work_id}/{digest}/{TRANSFORM_PATH}/{width}.webp"
        height = transform.derivative_height(expected["width"], expected["height"], int(width))
        path = ROOT / Path(*relative.split("/"))
        if (
            derivative.get("repository_path") != relative
            or derivative.get("url") != expected_url
            or derivative.get("cache_control") != CACHE_CONTROL
            or derivative.get("height") != height
            or not path.is_file()
            or transform.sha256_file(path) != derivative.get("sha256")
            or path.stat().st_size != derivative.get("byte_size")
        ):
            raise MaxPainMediaError(f"derivative binding mismatch: {work_id}/{width}")
        with Image.open(path) as image:
            if image.format != "WEBP" or image.size != (width, height) or not image.info.get("icc_profile") or getattr(image, "n_frames", 1) != 1:
                raise MaxPainMediaError(f"derivative format mismatch: {relative}")
        expected_paths.add(relative)
        total += path.stat().st_size
    actual_paths = {path.relative_to(ROOT).as_posix() for path in MEDIA_ROOT.rglob("*") if path.is_file()}
    if actual_paths != expected_paths:
        raise MaxPainMediaError("accession derivative inventory is not closed")
    return len(expected_paths), total


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--derivatives-only", action="store_true", help="write the three posters from the evidence alone and print their fixity")
    parser.add_argument("--work-entity-id")
    parser.add_argument("--media-reference-entity-id")
    parser.add_argument("--animation-media-reference-entity-id", default=DEFAULT_ANIMATION_MEDIA_ID)
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
            print(f"MAX PAIN presentation manifest is current: {count} derivatives, {total} bytes")
            return 0
        if args.derivatives_only:
            if not args.work_entity_id or not re.fullmatch(r"6529NM-W-[0-9]{4}", args.work_entity_id):
                raise MaxPainMediaError("derivatives-only requires --work-entity-id 6529NM-W-NNNN")
            _, derivatives, _ = generate_derivatives(args.work_entity_id, load_transform_module())
            print(json.dumps(derivatives, indent=2))
            return 0
        if args.promote_reviewed:
            if not all((args.reviewer_id, args.reviewed_at, args.reviewed_commit)):
                raise MaxPainMediaError("review promotion requires reviewer-id, reviewed-at and reviewed-commit")
            write_json(
                MANIFEST_PATH,
                promote_reviewed(load_json(MANIFEST_PATH), reviewer_id=args.reviewer_id, reviewed_at=args.reviewed_at, reviewed_commit=args.reviewed_commit),
            )
            count, total = verify()
            print(f"promoted {MANIFEST_PATH.relative_to(ROOT)}: {count} derivatives, {total} bytes")
            return 0
        if not all((args.work_entity_id, args.media_reference_entity_id, args.generated_at, args.actor_id)):
            raise MaxPainMediaError("generation requires work/media IDs, generated-at and actor-id")
        write_json(
            MANIFEST_PATH,
            generate(args.work_entity_id, args.media_reference_entity_id, args.generated_at, args.actor_id, args.animation_media_reference_entity_id),
        )
        count, total = verify()
        print(f"wrote {MANIFEST_PATH.relative_to(ROOT)}: {count} derivatives, {total} bytes")
        return 0
    except (OSError, MaxPainMediaError, ValueError) as exc:
        print(f"MAX PAIN presentation media error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
