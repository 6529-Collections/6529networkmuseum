#!/usr/bin/env python3
"""Generate or verify deterministic Keys and Gates web-presentation media."""

from __future__ import annotations

import argparse
import base64
import hashlib
import io
import json
import re
import sys
import warnings
from pathlib import Path
from typing import Any

from PIL import Image, ImageCms, ImageOps

REPO_ROOT = Path(__file__).resolve().parent.parent
PROGRAM_ID = "6529NM-AP-01"
OUTCOME_ROOT = REPO_ROOT / "records" / "programs" / PROGRAM_ID / "outcomes"
SELECTED_WORKS_PATH = REPO_ROOT / "records" / "programs" / PROGRAM_ID / "selected-works.json"
ACCESSIBILITY_PATH = REPO_ROOT / "media" / "programs" / PROGRAM_ID / "accessibility.json"
MANIFEST_PATH = REPO_ROOT / "records" / "programs" / PROGRAM_ID / "media-manifest.json"
MEDIA_ROOT = REPO_ROOT / "media" / "programs" / PROGRAM_ID
CDN_BASE_URL = "https://d3lqz0a4bldqgf.cloudfront.net"
CDN_KEY_PREFIX = f"museum/programs/{PROGRAM_ID}"
TRANSFORM_PROFILE = "6529NM_WEB_PRESENTATION_WEBP_V2_Q82_M6_FIXED_ICC"
TRANSFORM_PATH = "webp-v2-q82-m6-fixed-icc"
WIDTHS = (640, 1280, 2400)
QUALITY = 82
METHOD = 6
CACHE_CONTROL = "public, max-age=31536000, immutable"
EXPECTED_OUTCOME_COUNT = 16
ALT_TEXT_STATUS = "constructed_visual_description_pending_independent_review"
SHA256_PATTERN = re.compile(r"^sha256:[0-9a-f]{64}$")
RECORD_ID_PATTERN = re.compile(r"^6529NM-AP-01-OUT-[0-9]{3}$")
SRGB_ICC_SHA256 = "sha256:4ed6f6f05df0d17516662c5fe06ac90e14e0c1936abd15a491b57998c56aef86"
SRGB_ICC_BASE64 = (
    "AAACTGxjbXMEQAAAbW50clJHQiBYWVogB+oACAAEAAAAAAAAYWNzcE1TRlQAAAAAAAAAAAAAAAAA"
    "AAAAAAAAAAAAAAAAAPbWAAEAAAAA0y1sY21zAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
    "AAAAAAAAAAAAAAAAAAAAAAALZGVzYwAAAQgAAAA2Y3BydAAAAUAAAABMd3RwdAAAAYwAAAAUY2hh"
    "ZAAAAaAAAAAsclhZWgAAAcwAAAAUYlhZWgAAAeAAAAAUZ1hZWgAAAfQAAAAUclRSQwAAAggAAAAg"
    "Z1RSQwAAAggAAAAgYlRSQwAAAggAAAAgY2hybQAAAigAAAAkbWx1YwAAAAAAAAABAAAADGVuVVMA"
    "AAAaAAAAHABzAFIARwBCACAAYgB1AGkAbAB0AC0AaQBuAABtbHVjAAAAAAAAAAEAAAAMZW5VUwAA"
    "ADAAAAAcAE4AbwAgAGMAbwBwAHkAcgBpAGcAaAB0ACwAIAB1AHMAZQAgAGYAcgBlAGUAbAB5WFla"
    "IAAAAAAAAPbWAAEAAAAA0y1zZjMyAAAAAAABDEIAAAXe///zJQAAB5MAAP2Q///7of///aIAAAPc"
    "AADAblhZWiAAAAAAAABvoAAAOPUAAAOQWFlaIAAAAAAAACSfAAAPhAAAtsNYWVogAAAAAAAAYpcA"
    "ALeHAAAY2XBhcmEAAAAAAAMAAAACZmYAAPKnAAANWQAAE9AAAApbY2hybQAAAAAAAwAAAACj1wAA"
    "VHsAAEzNAACZmgAAJmYAAA9c"
)

Image.MAX_IMAGE_PIXELS = 100_000_000
warnings.simplefilter("error", Image.DecompressionBombWarning)


class ProgramMediaError(ValueError):
    """Raised when media input, output, or manifest state is invalid."""


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ProgramMediaError(f"unable to read JSON {path.relative_to(REPO_ROOT)}: {exc}") from exc
    if not isinstance(value, dict):
        raise ProgramMediaError(f"JSON root is not an object: {path.relative_to(REPO_ROOT)}")
    return value


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def sha256_bytes(payload: bytes) -> str:
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
    return "sha256:" + digest.hexdigest()


def require_string(value: object, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise ProgramMediaError(f"{label} must be a non-empty string")
    return value


def load_outcomes() -> list[dict[str, Any]]:
    outcomes = [load_json(path) for path in sorted(OUTCOME_ROOT.glob("OUT-*.json"))]
    if len(outcomes) != EXPECTED_OUTCOME_COUNT:
        raise ProgramMediaError(
            f"expected {EXPECTED_OUTCOME_COUNT} outcomes, found {len(outcomes)}"
        )
    record_ids = [require_string(outcome.get("record_id"), "outcome record_id") for outcome in outcomes]
    if len(set(record_ids)) != EXPECTED_OUTCOME_COUNT or any(
        RECORD_ID_PATTERN.fullmatch(record_id) is None for record_id in record_ids
    ):
        raise ProgramMediaError("outcome record IDs are missing, duplicated, or malformed")
    return outcomes


def load_accessibility() -> tuple[dict[str, str], dict[str, list[int]]]:
    accessibility = load_json(ACCESSIBILITY_PATH)
    if accessibility.get("program_id") != PROGRAM_ID:
        raise ProgramMediaError("accessibility program_id does not match")
    if accessibility.get("status") != ALT_TEXT_STATUS:
        raise ProgramMediaError("accessibility review status is not the expected constructed status")
    items = accessibility.get("items")
    if not isinstance(items, list) or len(items) != EXPECTED_OUTCOME_COUNT:
        raise ProgramMediaError("accessibility inventory must contain exactly 16 items")
    result: dict[str, str] = {}
    public_widths: dict[str, list[int]] = {}
    for item in items:
        if not isinstance(item, dict):
            raise ProgramMediaError("accessibility item is not an object")
        record_id = require_string(item.get("record_id"), "accessibility record_id")
        alt_text = require_string(item.get("alt_text"), f"{record_id} alt_text").strip()
        if record_id in result or len(alt_text) < 20:
            raise ProgramMediaError(f"invalid or duplicated accessibility entry: {record_id}")
        result[record_id] = alt_text
        widths = item.get("public_widths", list(WIDTHS))
        if (
            not isinstance(widths, list)
            or not widths
            or len(widths) > len(WIDTHS)
            or widths != sorted(set(widths))
            or any(width not in WIDTHS for width in widths)
        ):
            raise ProgramMediaError(f"invalid public widths for {record_id}")
        public_widths[record_id] = widths
    return result, public_widths


def outcome_media(outcome: dict[str, Any]) -> dict[str, Any]:
    media = outcome.get("media")
    if not isinstance(media, list) or len(media) != 1 or not isinstance(media[0], dict):
        raise ProgramMediaError(f"{outcome.get('record_id')} must declare exactly one media source")
    return media[0]


def outcome_rights_status(outcome: dict[str, Any]) -> str:
    rights = outcome.get("rights_and_consent")
    if not isinstance(rights, dict):
        raise ProgramMediaError(f"{outcome.get('record_id')} has no rights_and_consent object")
    return require_string(
        rights.get("rights_effective_status"),
        f"{outcome.get('record_id')} rights_effective_status",
    )


def source_path_for(source_dir: Path, record_id: str, source_url: str) -> Path:
    source_suffix = Path(source_url.split("?", 1)[0]).suffix.casefold()
    candidates = [
        path
        for path in source_dir.glob(f"{record_id}.*")
        if path.is_file() and path.suffix.casefold() == source_suffix
    ]
    if len(candidates) != 1:
        raise ProgramMediaError(
            f"expected one local source for {record_id} with suffix {source_suffix}, found {len(candidates)}"
        )
    return candidates[0]


def has_alpha(image: Image.Image) -> bool:
    return image.mode in {"RGBA", "LA"} or (
        image.mode == "P" and "transparency" in image.info
    )


def fixed_srgb_profile() -> tuple[ImageCms.ImageCmsProfile, bytes]:
    try:
        profile_bytes = base64.b64decode(SRGB_ICC_BASE64, validate=True)
        profile = ImageCms.ImageCmsProfile(io.BytesIO(profile_bytes))
    except (OSError, ValueError) as exc:
        raise ProgramMediaError(f"fixed sRGB ICC profile is invalid: {exc}") from exc
    if sha256_bytes(profile_bytes) != SRGB_ICC_SHA256:
        raise ProgramMediaError("fixed sRGB ICC profile hash does not match")
    return profile, profile_bytes


def normalize_colour(image: Image.Image, source_icc: bytes | None) -> tuple[Image.Image, str, bytes]:
    output_profile, output_icc = fixed_srgb_profile()
    alpha = image.convert("RGBA").getchannel("A") if has_alpha(image) else None
    rgb = image.convert("RGB")
    status = "untagged_assumed_srgb"
    if source_icc:
        try:
            input_profile = ImageCms.ImageCmsProfile(io.BytesIO(source_icc))
            rgb = ImageCms.profileToProfile(
                rgb,
                input_profile,
                output_profile,
                outputMode="RGB",
                renderingIntent=ImageCms.Intent.PERCEPTUAL,
            )
        except (OSError, ValueError) as exc:
            raise ProgramMediaError(f"embedded ICC profile could not be converted: {exc}") from exc
        status = "embedded_profile_converted_to_srgb"
    if alpha is not None:
        rgb.putalpha(alpha)
    return rgb, status, output_icc


def webp_bytes(image: Image.Image, width: int, output_icc: bytes) -> tuple[bytes, int]:
    if image.width < width:
        raise ProgramMediaError(
            f"source width {image.width} is smaller than required derivative width {width}"
        )
    height = max(1, round(image.height * width / image.width))
    resized = image.resize(
        (width, height),
        resample=Image.Resampling.LANCZOS,
        reducing_gap=3.0,
    )
    output = io.BytesIO()
    resized.save(
        output,
        format="WEBP",
        quality=QUALITY,
        method=METHOD,
        exact=True,
        icc_profile=output_icc,
    )
    return output.getvalue(), height


def write_immutable_asset(path: Path, payload: bytes) -> None:
    if path.exists():
        if path.read_bytes() != payload:
            raise ProgramMediaError(
                f"refusing to overwrite immutable derivative with different bytes: {path.relative_to(REPO_ROOT)}"
            )
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(payload)


def generate_item(
    outcome: dict[str, Any],
    alt_text: str,
    public_widths: list[int],
    source_dir: Path,
) -> dict[str, Any]:
    record_id = require_string(outcome.get("record_id"), "record_id")
    source = outcome_media(outcome)
    source_url = require_string(source.get("url"), f"{record_id} media URL")
    source_mime = require_string(source.get("mime_type"), f"{record_id} media MIME type")
    source_path = source_path_for(source_dir, record_id, source_url)
    source_sha256 = sha256_file(source_path)
    source_size = source_path.stat().st_size
    digest = source_sha256.removeprefix("sha256:")

    with Image.open(source_path) as raw_image:
        raw_image.load()
        detected_mime = Image.MIME.get(raw_image.format or "")
        if detected_mime != source_mime:
            raise ProgramMediaError(
                f"{record_id} source MIME mismatch: record={source_mime}, detected={detected_mime}"
            )
        orientation = raw_image.getexif().get(274, 1)
        source_icc = raw_image.info.get("icc_profile")
        if source_icc is not None and not isinstance(source_icc, bytes):
            raise ProgramMediaError(f"{record_id} has a malformed ICC profile")
        oriented = ImageOps.exif_transpose(raw_image)
        normalized, colour_status, output_icc = normalize_colour(oriented, source_icc)
        source_width, source_height = normalized.size
        derivatives: list[dict[str, Any]] = []
        for width in public_widths:
            payload, height = webp_bytes(normalized, width, output_icc)
            relative_path = Path(
                "media",
                "programs",
                PROGRAM_ID,
                record_id,
                digest,
                TRANSFORM_PATH,
                f"{width}.webp",
            )
            write_immutable_asset(REPO_ROOT / relative_path, payload)
            cdn_key = "/".join(
                (
                    CDN_KEY_PREFIX,
                    record_id,
                    digest,
                    TRANSFORM_PATH,
                    f"{width}.webp",
                )
            )
            derivatives.append(
                {
                    "width": width,
                    "height": height,
                    "mime_type": "image/webp",
                    "sha256": sha256_bytes(payload),
                    "byte_size": len(payload),
                    "repository_path": relative_path.as_posix(),
                    "url": f"{CDN_BASE_URL}/{cdn_key}",
                    "cache_control": CACHE_CONTROL,
                }
            )

    return {
        "record_id": record_id,
        "source": {
            "role": "submitted_high_resolution_source",
            "url": source_url,
            "mime_type": source_mime,
            "sha256": source_sha256,
            "byte_size": source_size,
            "pixel_width": source_width,
            "pixel_height": source_height,
            "exif_orientation_applied": orientation not in {None, 1},
            "colour_profile_status": colour_status,
            "retention_status": "source bytes fixity-checked during derivation but not retained in this repository",
            "rights_effective_status": outcome_rights_status(outcome),
        },
        "presentation": {
            "role": "web_presentation_surrogate",
            "alt_text": alt_text,
            "alt_text_status": ALT_TEXT_STATUS,
            "public_widths": public_widths,
            "derivatives": derivatives,
        },
    }


def generate_manifest(
    source_dir: Path,
    source_observed_at: str,
    constructed_at: str,
    constructor_actor: str,
) -> dict[str, Any]:
    if not source_dir.is_dir():
        raise ProgramMediaError(f"source directory does not exist: {source_dir}")
    outcomes = load_outcomes()
    alt_texts, public_widths = load_accessibility()
    outcome_ids = {require_string(outcome.get("record_id"), "record_id") for outcome in outcomes}
    if set(alt_texts) != outcome_ids:
        raise ProgramMediaError("accessibility and outcome record ID sets differ")
    items = [
        generate_item(
            outcome,
            alt_texts[require_string(outcome.get("record_id"), "record_id")],
            public_widths[require_string(outcome.get("record_id"), "record_id")],
            source_dir,
        )
        for outcome in outcomes
    ]
    return {
        "$schema": "../../../schemas/program-media-manifest.schema.json",
        "record_control": {
            "revision": 1,
            "record_status": "constructed",
            "constructor": {
                "actor_id": constructor_actor,
                "role": "constructor",
                "constructed_at": constructed_at,
            },
            "review": None,
        },
        "record_type": "PROGRAM_MEDIA_MANIFEST",
        "schema_profile": "6529NM_PROGRAM_MEDIA_MANIFEST_V1",
        "program_id": PROGRAM_ID,
        "generated_at": constructed_at,
        "source_observed_at": source_observed_at,
        "transform": {
            "profile": TRANSFORM_PROFILE,
            "implementation": f"Pillow {Image.__version__}",
            "format": "image/webp",
            "quality": QUALITY,
            "method": METHOD,
            "widths": list(WIDTHS),
            "resize_filter": "Lanczos",
            "upscale": False,
            "orientation": "EXIF transpose before resize",
            "colour_management": "embedded profiles converted to sRGB; untagged sources treated as sRGB; sRGB profile embedded in derivatives",
            "icc_profile_sha256": SRGB_ICC_SHA256,
            "metadata": "source EXIF/XMP stripped; output sRGB ICC profile retained",
        },
        "delivery": {
            "cdn_base_url": CDN_BASE_URL,
            "cache_control": CACHE_CONTROL,
            "key_profile": "museum/programs/{program_id}/{record_id}/{source_sha256}/{transform_profile}/{width}.webp",
            "overwrite_policy": "fail if an existing key does not contain the declared bytes",
        },
        "rights_boundary": {
            "purpose": "Technical presentation surrogates for the existing public Keys and Gates program display",
            "status": "Each outcome's recorded rights-effective status remains controlling; this manifest does not activate CC0 or grant reuse rights",
            "non_claims": [
                "A presentation surrogate is not a preservation master or the tokenized artwork.",
                "Media delivery does not prove mint, purchase, title, custody, or accession.",
                "The submitted high-resolution source remains distinct from the generated web derivatives.",
            ],
        },
        "items": items,
    }


def expected_selected_ids() -> set[str]:
    selected = load_json(SELECTED_WORKS_PATH)
    works = selected.get("works")
    if not isinstance(works, list):
        raise ProgramMediaError("selected works register has no works array")
    result = {
        require_string(work.get("record_id"), "selected work record_id")
        for work in works
        if isinstance(work, dict)
    }
    if len(result) != EXPECTED_OUTCOME_COUNT:
        raise ProgramMediaError("selected works register does not contain 16 unique IDs")
    return result


def verify_webp(path: Path, width: int, height: int) -> None:
    try:
        with Image.open(path) as image:
            image.verify()
        with Image.open(path) as image:
            if image.format != "WEBP" or image.size != (width, height):
                raise ProgramMediaError(
                    f"derivative geometry or format mismatch: {path.relative_to(REPO_ROOT)}"
                )
            if not image.info.get("icc_profile"):
                raise ProgramMediaError(
                    f"derivative is missing its sRGB profile: {path.relative_to(REPO_ROOT)}"
                )
    except OSError as exc:
        raise ProgramMediaError(f"unreadable derivative {path.relative_to(REPO_ROOT)}: {exc}") from exc


def verify_manifest() -> tuple[int, int]:
    manifest = load_json(MANIFEST_PATH)
    outcomes = {require_string(item.get("record_id"), "record_id"): item for item in load_outcomes()}
    alt_texts, public_widths = load_accessibility()
    items = manifest.get("items")
    if not isinstance(items, list) or len(items) != EXPECTED_OUTCOME_COUNT:
        raise ProgramMediaError("media manifest must contain exactly 16 items")
    if manifest.get("program_id") != PROGRAM_ID:
        raise ProgramMediaError("media manifest program_id does not match")
    transform = manifest.get("transform")
    if not isinstance(transform, dict) or transform.get("profile") != TRANSFORM_PROFILE:
        raise ProgramMediaError("media manifest transform profile does not match the implementation")
    if transform.get("implementation") != f"Pillow {Image.__version__}":
        raise ProgramMediaError("media manifest Pillow version does not match the pinned runtime")
    if transform.get("icc_profile_sha256") != SRGB_ICC_SHA256:
        raise ProgramMediaError("media manifest sRGB ICC profile hash does not match")
    manifest_ids = {
        require_string(item.get("record_id"), "media manifest record_id")
        for item in items
        if isinstance(item, dict)
    }
    if manifest_ids != set(outcomes) or manifest_ids != set(alt_texts) or manifest_ids != expected_selected_ids():
        raise ProgramMediaError("media, accessibility, outcome, and selected-work ID sets differ")

    declared_paths: set[str] = set()
    total_bytes = 0
    for item in items:
        if not isinstance(item, dict):
            raise ProgramMediaError("media manifest item is not an object")
        record_id = require_string(item.get("record_id"), "record_id")
        outcome = outcomes[record_id]
        source = item.get("source")
        presentation = item.get("presentation")
        if not isinstance(source, dict) or not isinstance(presentation, dict):
            raise ProgramMediaError(f"{record_id} source or presentation object is missing")
        recorded_source = outcome_media(outcome)
        if source.get("url") != recorded_source.get("url") or source.get("mime_type") != recorded_source.get("mime_type"):
            raise ProgramMediaError(f"{record_id} source identity differs from the outcome record")
        if source.get("rights_effective_status") != outcome_rights_status(outcome):
            raise ProgramMediaError(f"{record_id} rights status differs from the outcome record")
        source_sha256 = require_string(source.get("sha256"), f"{record_id} source sha256")
        if SHA256_PATTERN.fullmatch(source_sha256) is None:
            raise ProgramMediaError(f"{record_id} source sha256 is malformed")
        source_width = source.get("pixel_width")
        source_height = source.get("pixel_height")
        if (
            not isinstance(source_width, int)
            or not isinstance(source_height, int)
            or source_width <= 0
            or source_height <= 0
        ):
            raise ProgramMediaError(f"{record_id} source dimensions are invalid")
        if presentation.get("alt_text") != alt_texts[record_id]:
            raise ProgramMediaError(f"{record_id} alt text differs from the accessibility source")
        expected_widths = public_widths[record_id]
        if presentation.get("public_widths") != expected_widths:
            raise ProgramMediaError(f"{record_id} public widths differ from the accessibility source")
        derivatives = presentation.get("derivatives")
        if not isinstance(derivatives, list) or [entry.get("width") for entry in derivatives if isinstance(entry, dict)] != expected_widths:
            raise ProgramMediaError(f"{record_id} derivative widths are incomplete or unordered")
        digest = source_sha256.removeprefix("sha256:")
        for derivative in derivatives:
            if not isinstance(derivative, dict):
                raise ProgramMediaError(f"{record_id} derivative is not an object")
            width = derivative.get("width")
            height = derivative.get("height")
            repository_path = require_string(
                derivative.get("repository_path"), f"{record_id} repository_path"
            )
            if not isinstance(width, int) or not isinstance(height, int):
                raise ProgramMediaError(f"{record_id} derivative dimensions are invalid")
            expected_height = max(1, round(source_height * width / source_width))
            if height != expected_height:
                raise ProgramMediaError(
                    f"{record_id} derivative aspect ratio differs from its source at width {width}"
                )
            expected_path = Path(
                "media", "programs", PROGRAM_ID, record_id, digest, TRANSFORM_PATH, f"{width}.webp"
            ).as_posix()
            expected_url = f"{CDN_BASE_URL}/{CDN_KEY_PREFIX}/{record_id}/{digest}/{TRANSFORM_PATH}/{width}.webp"
            if repository_path != expected_path or derivative.get("url") != expected_url:
                raise ProgramMediaError(f"{record_id} derivative path or URL is not content addressed")
            if repository_path in declared_paths:
                raise ProgramMediaError(f"duplicate derivative path: {repository_path}")
            declared_paths.add(repository_path)
            path = REPO_ROOT / Path(repository_path)
            if not path.is_file():
                raise ProgramMediaError(f"declared derivative is missing: {repository_path}")
            payload_size = path.stat().st_size
            if payload_size != derivative.get("byte_size") or sha256_file(path) != derivative.get("sha256"):
                raise ProgramMediaError(f"derivative fixity mismatch: {repository_path}")
            verify_webp(path, width, height)
            total_bytes += payload_size

    actual_paths = {
        path.relative_to(REPO_ROOT).as_posix()
        for path in MEDIA_ROOT.rglob("*.webp")
        if path.is_file()
    }
    if actual_paths != declared_paths:
        missing = sorted(declared_paths - actual_paths)
        extra = sorted(actual_paths - declared_paths)
        raise ProgramMediaError(f"derivative inventory is not closed; missing={missing}, extra={extra}")
    return len(declared_paths), total_bytes


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="verify the committed manifest and derivatives")
    parser.add_argument("--source-dir", type=Path, help="directory containing record-ID-named source images")
    parser.add_argument("--source-observed-at", help="UTC observation time for the downloaded source bytes")
    parser.add_argument("--constructed-at", help="UTC construction time for the generated manifest")
    parser.add_argument("--constructor-actor", help="public constructor identifier")
    args = parser.parse_args(argv)
    try:
        if args.check:
            count, total_bytes = verify_manifest()
            print(f"program media manifest is current: {count} derivatives, {total_bytes} bytes")
            return 0
        if args.source_dir is None or not args.source_observed_at or not args.constructed_at or not args.constructor_actor:
            parser.error(
                "generation requires --source-dir, --source-observed-at, --constructed-at, and --constructor-actor"
            )
        manifest = generate_manifest(
            args.source_dir.resolve(),
            args.source_observed_at,
            args.constructed_at,
            args.constructor_actor,
        )
        write_json(MANIFEST_PATH, manifest)
        count, total_bytes = verify_manifest()
        print(f"wrote {MANIFEST_PATH.relative_to(REPO_ROOT)}: {count} derivatives, {total_bytes} bytes")
        return 0
    except ProgramMediaError as exc:
        print(f"program media generation failed: {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
