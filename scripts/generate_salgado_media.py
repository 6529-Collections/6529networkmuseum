#!/usr/bin/env python3
"""Package and check the approved Salgado WebPs in the accession media profile.

This is an offline publication projection of retained, reviewed derivatives.
It neither downloads private JPEGs nor claims a new image-generation event.
"""

from __future__ import annotations

import argparse
from copy import deepcopy
from datetime import datetime
import hashlib
import io
import json
from pathlib import Path
import re

from jsonschema import Draft202012Validator, FormatChecker
from PIL import Image

from canonical import canonicalize


ROOT = Path(__file__).resolve().parents[1]
LOT = "6529NM.2026.004"
ACTOR = "codex-task:01a087a1-5e64-7280-b5f8-82d0df4ec066"
BASE = f"records/accessions/{LOT}/public"
MANIFEST_PATH = f"{BASE}/presentation-manifest.json"
AUTHORITY_PATH = f"{BASE}/web-presentation-authority.md"
MEDIA_ROOT = f"media/accessions/{LOT}"
SOURCE_PATH = "evidence/salgado-amazonia-sources/manifest.json"
PREPARATION_PATH = "evidence/salgado-amazonia-preservation/display-preparation.json"
SOURCE_SHA = "03ecbf9fe61a8e066ee9730d1644550f164b908b1da65a20f36756cdcc6e9392"
PREPARATION_SHA = "29fc862a8764c7648fba1aff344e99f13020cdb734706bdfd72cd969148587ea"
ICC_SHA = "4ed6f6f05df0d17516662c5fe06ac90e14e0c1936abd15a491b57998c56aef86"
TOKENS = (226, 1117, 2059, 2216, 2768, 4697)
WIDTHS = (640, 1280, 2400)
TRANSFORM = "webp-v2-q82-m6-fixed-icc"
CDN = "https://d3lqz0a4bldqgf.cloudfront.net"
CACHE = "public, max-age=31536000, immutable"


class SalgadoMediaError(ValueError):
    """The publication differs from the retained approved media evidence."""


def digest(raw: bytes) -> str:
    return "sha256:" + hashlib.sha256(raw).hexdigest()


def load(path: Path) -> dict:
    value = json.loads(path.read_bytes())
    if not isinstance(value, dict):
        raise SalgadoMediaError(f"JSON source is not an object: {path.name}")
    return value


def source_rows(root: Path) -> list[tuple[dict, dict]]:
    for relative, expected in ((SOURCE_PATH, SOURCE_SHA), (PREPARATION_PATH, PREPARATION_SHA)):
        if digest((root / relative).read_bytes()) != "sha256:" + expected:
            raise SalgadoMediaError(f"Reviewed source evidence changed: {relative}")
    sources = load(root / SOURCE_PATH)["objects"]
    prepared = load(root / PREPARATION_PATH)["items"]
    if [item["token_id"] for item in sources] != list(TOKENS) or [item["token_id"] for item in prepared] != list(TOKENS):
        raise SalgadoMediaError("The six source/preparation identities do not match")
    rows = list(zip(sources, prepared))
    for index, (source, display) in enumerate(rows, 1):
        if source["object_id"] != f"{LOT}.{index:02d}" or source["object_id"] != display["object_id"] or source["image"]["sha256"] != display["source_sha256"]:
            raise SalgadoMediaError("Source image and derivative object binding differs")
        if [item["width"] for item in display["derivatives"]] != list(WIDTHS):
            raise SalgadoMediaError("The reviewed responsive set is incomplete")
    return rows


def build_manifest(generated_at: str, root: Path = ROOT) -> dict:
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z", generated_at):
        raise SalgadoMediaError("Construction time must be a UTC RFC 3339 timestamp")
    datetime.fromisoformat(generated_at.replace("Z", "+00:00"))
    items = []
    for index, (source, display) in enumerate(source_rows(root), 30):
        work = f"6529NM-W-{index:04d}"
        image = source["image"]
        source_sha = image["sha256"].removeprefix("sha256:")
        derivatives = []
        for prior in display["derivatives"]:
            relative = f"{MEDIA_ROOT}/{work}/{source_sha}/{TRANSFORM}/{prior['width']}.webp"
            derivatives.append({
                "width": prior["width"], "height": prior["height"],
                "mime_type": "image/webp", "sha256": prior["sha256"],
                "byte_size": prior["bytes"], "repository_path": relative,
                "url": f"{CDN}/museum/{relative.removeprefix('media/')}",
                "cache_control": CACHE,
            })
        items.append({
            "work_entity_id": work,
            "media_reference_entity_id": f"6529NM-MED-{index + 24:04d}",
            "source": {
                "role": "fixity_verified_token_source", "url": image["uri"],
                "mime_type": "image/jpeg", "sha256": image["sha256"],
                "byte_size": image["bytes"], "pixel_width": image["width"],
                "pixel_height": image["height"], "exif_orientation_applied": image["orientation"] != 1,
                "colour_profile_status": display["colour_profile_status"],
            },
            "presentation": {
                "role": "web_presentation_surrogate", "alt_text": display["accessibility_text"],
                "alt_text_status": "reviewed_accessibility_description",
                "public_widths": list(WIDTHS), "derivatives": derivatives,
            },
        })
    return {
        "$schema": "../../../../schemas/accession-media-presentation-v2.schema.json",
        "record_control": {
            "revision": 1, "record_status": "constructed",
            "constructor": {"actor_id": ACTOR, "role": "constructor", "constructed_at": generated_at},
            "review": None,
        },
        "record_type": "ACCESSION_MEDIA_PRESENTATION",
        "schema_profile": "6529NM_ACCESSION_MEDIA_PRESENTATION_V2",
        "accession_lot_id": LOT, "generated_at": generated_at,
        "transform": {
            "profile": "6529NM_WEB_PRESENTATION_WEBP_V2_Q82_M6_FIXED_ICC",
            "implementation": "Pillow 12.3.0", "format": "image/webp", "quality": 82, "method": 6,
            "widths": list(WIDTHS), "resize_filter": "Lanczos", "upscale": False,
            "orientation": "EXIF orientation respected; all six retained JPEGs have orientation 1",
            "colour_management": "embedded Adobe RGB (1998) profiles converted to fixed sRGB before resize",
            "icc_profile_sha256": "sha256:" + ICC_SHA,
            "metadata": "EXIF and XMP stripped; output fixed sRGB ICC retained",
        },
        "delivery": {
            "status": "prepared_for_contextual_museum_display_pending_review",
            "authority_record_id": f"{LOT}.DISPLAY-01", "authority_path": AUTHORITY_PATH,
            "cdn_base_url": CDN, "cache_control": CACHE,
            "key_profile": "museum/accessions/{accession_lot_id}/{work_entity_id}/{source_sha256}/{transform_profile}/{width}.webp",
            "overwrite_policy": "fail if an existing key does not contain the declared bytes",
        },
        "rights_boundary": {
            "status": "Credited ordinary Museum display under the recorded unrestricted-gift determination; photograph copyright retained",
            "source_originals": "The exact retained JPEGs remain source objects. The public payload contains only the reviewed WebPs; source originals and their embedded metadata remain in restricted preservation storage.",
            "technical_transformation": "Full-frame colour conversion, proportion-preserving Lanczos resize and WebP compression; no crop, retouching, watermark or alteration of depicted content.",
            "no_general_reuse": "Ordinary Museum use does not grant a general third-party reproduction, commercial-use, sublicensing or model-training licence.",
        },
        "items": items,
    }


def without_review(value: dict) -> dict:
    value = deepcopy(value)
    value["record_control"]["record_status"] = "constructed"
    value["record_control"]["review"] = None
    value["delivery"]["status"] = "prepared_for_contextual_museum_display_pending_review"
    return value


def verify_manifest(value: dict, root: Path = ROOT, *, check_files: bool = True) -> tuple[int, int]:
    schema = load(root / "schemas/accession-media-presentation-v2.schema.json")
    errors = list(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(value))
    if errors:
        raise SalgadoMediaError("Presentation schema: " + errors[0].message)
    expected = build_manifest(value["generated_at"], root)
    if without_review(value) != expected:
        raise SalgadoMediaError("Presentation differs from the exact reviewed source/derivative projection")
    control = value["record_control"]
    review = control["review"]
    if control["record_status"] == "constructed":
        if review is not None or value["delivery"]["status"] != "prepared_for_contextual_museum_display_pending_review":
            raise SalgadoMediaError("Construction and display review states disagree")
    else:
        if not isinstance(review, dict) or review["actor_id"] == ACTOR or value["delivery"]["status"] != "approved_for_contextual_museum_display":
            raise SalgadoMediaError("Reviewed presentation has no separate reviewer/display approval")
        if datetime.fromisoformat(review["reviewed_at"].replace("Z", "+00:00")) <= datetime.fromisoformat(value["generated_at"].replace("Z", "+00:00")):
            raise SalgadoMediaError("Review must follow construction")
        material = {key: item for key, item in value.items() if key != "record_control"}
        if review["payload_sha256"] != digest(canonicalize(material)):
            raise SalgadoMediaError("Reviewed presentation payload hash differs")
    authority = (root / AUTHORITY_PATH).read_text(encoding="utf-8").splitlines()
    if authority[:5] != ["---", f"record_id: {LOT}.DISPLAY-01", "status: active", f"accession_number: {LOT}", "---"]:
        raise SalgadoMediaError("Active accession display authority is missing")
    paths = set()
    total = 0
    for item in value["items"]:
        for derivative in item["presentation"]["derivatives"]:
            relative = derivative["repository_path"]
            paths.add(relative)
            total += derivative["byte_size"]
            if not check_files:
                continue
            raw = (root / relative).read_bytes()
            if digest(raw) != derivative["sha256"] or len(raw) != derivative["byte_size"]:
                raise SalgadoMediaError(f"Derivative bytes differ: {relative}")
            with Image.open(io.BytesIO(raw)) as image:
                image.load()
                if image.format != "WEBP" or image.size != (derivative["width"], derivative["height"]):
                    raise SalgadoMediaError(f"Derivative format or geometry differs: {relative}")
                if "exif" in image.info or "xmp" in image.info or digest(image.info.get("icc_profile", b"")) != "sha256:" + ICC_SHA:
                    raise SalgadoMediaError(f"Derivative metadata or colour profile differs: {relative}")
    if check_files:
        actual = {path.relative_to(root).as_posix() for path in (root / MEDIA_ROOT).rglob("*") if path.is_file()}
        if paths != actual:
            raise SalgadoMediaError("The accession media directory is not the exact 18-file manifest inventory")
    return len(paths), total


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--generated-at")
    args = parser.parse_args()
    try:
        if args.check:
            count, size = verify_manifest(load(ROOT / MANIFEST_PATH))
            print(f"Salgado presentation verified: {count} derivatives, {size} bytes")
            return 0
        if not args.generated_at:
            raise SalgadoMediaError("--generated-at is required to construct the publication manifest")
        value = build_manifest(args.generated_at)
        verify_manifest(value, check_files=False)
        output = ROOT / MANIFEST_PATH
        if output.exists():
            raise SalgadoMediaError("A presentation manifest already exists; use --check instead")
        output.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
        print(f"Constructed {MANIFEST_PATH}; verify the retained derivative paths before publication")
        return 0
    except (OSError, ValueError, KeyError) as exc:
        print(f"Salgado media check failed: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
