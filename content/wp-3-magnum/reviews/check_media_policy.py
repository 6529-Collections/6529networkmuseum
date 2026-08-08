"""Validate the isolated Magnum proposal-media join without network access.

This check is deliberately local and fail-closed.  It verifies the typed join
from each public Work to the exact already-published Wave URL and rejects any
runtime affordance that would turn proposal-context media into a download,
derivative, preservation object, or identifying child display.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parents[1]
JOIN_PATH = ROOT / "machine" / "wave-media-join.json"

EXPECTED = (
    ("6529NM-W-0024", "6529NM-MED-0003", "6529NM-PG-2026-001.OBJ-001", "127"),
    ("6529NM-W-0025", "6529NM-MED-0041", "6529NM-PG-2026-001.OBJ-002", "145"),
    ("6529NM-W-0026", "6529NM-MED-0042", "6529NM-PG-2026-001.OBJ-003", "97"),
    ("6529NM-W-0027", "6529NM-MED-0043", "6529NM-PG-2026-001.OBJ-004", "44"),
    ("6529NM-W-0028", "6529NM-MED-0044", "6529NM-PG-2026-001.OBJ-005", "104"),
)

ALLOWED_AFFORDANCES = {
    "view",
    "hero",
    "alt_text",
    "open_signed_wave_source",
    "copy_citation",
}
BLOCKED_AFFORDANCES = {
    "download",
    "full_resolution",
    "zoom",
    "fullscreen",
    "iiif",
    "preservation_master",
}
DENY_RUNTIME_FIELDS = {
    "url_rewrite": "deny",
    "runtime_fallback": "deny",
    "repository_derivative": "deny",
    "responsive_variants": "deny",
    "download": "deny",
    "full_resolution_claim": "deny",
    "zoom": "deny",
    "fullscreen": "deny",
    "iiif_or_tiled_service": "deny",
    "preservation_claim": "deny",
}


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def main() -> int:
    errors: list[str] = []
    try:
        join = json.loads(JOIN_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Media-policy check failed to read {JOIN_PATH}: {exc}", file=sys.stderr)
        return 1

    if join.get("current_public_status") != "Selected by Museum Wave; acquisition review in progress":
        fail(errors, "media join must carry the canonical current selected-review status")
    if join.get("publication_boundary") != "signed_wave_proposal_only":
        fail(errors, "media join must be proposal-context-only")
    if join.get("prior_status_observation", {}).get("historical_only") is not True:
        fail(errors, "the prior PARTICIPATORY observation must remain historical-only")
    runtime = join.get("runtime_policy", {})
    if runtime.get("source_url_policy") != "exact_allowlisted_wave_media_url_only":
        fail(errors, "runtime source policy must allow exact URLs only")
    for key, expected in DENY_RUNTIME_FIELDS.items():
        if runtime.get(key) != expected:
            fail(errors, f"runtime policy {key!r} must be {expected!r}")

    rows = join.get("works")
    if not isinstance(rows, list) or len(rows) != len(EXPECTED):
        fail(errors, "media join must contain exactly five Work rows")
        rows = rows if isinstance(rows, list) else []

    for row, (work_id, media_id, object_alias, token_id) in zip(rows, EXPECTED):
        label = row.get("proposal_object_alias", "<missing alias>")
        if row.get("work_entity_id") != work_id:
            fail(errors, f"{label}: wrong Work entity ID")
        if row.get("media_reference_entity_id") != media_id:
            fail(errors, f"{label}: wrong Media Reference entity ID")
        if row.get("proposal_object_alias") != object_alias:
            fail(errors, f"{label}: proposal alias drift")
        if row.get("token_id") != token_id:
            fail(errors, f"{label}: token ID drift")
        if row.get("token_image_url") != row.get("wave_media_url"):
            fail(errors, f"{label}: token and Wave media URLs must be identical")
        url = row.get("wave_media_url")
        parsed = urlsplit(url or "")
        if parsed.scheme != "https" or parsed.netloc != "arweave.net" or parsed.query or parsed.fragment:
            fail(errors, f"{label}: media URL is not an exact allowlisted Arweave URL")
        if row.get("media_status") != "historical_wave_url_reference_only":
            fail(errors, f"{label}: media status must remain historical URL reference only")
        if row.get("rights_label") != "All Rights Reserved":
            fail(errors, f"{label}: rights label must be All Rights Reserved")
        credit = row.get("credit_line", "")
        if "©" not in credit or "Magnum Photos" not in credit:
            fail(errors, f"{label}: credit must include artist and Magnum copyright notice")
        if set(row.get("allowed_ui_affordances", [])) != ALLOWED_AFFORDANCES:
            fail(errors, f"{label}: allowed UI affordances are not the closed proposal set")
        if not BLOCKED_AFFORDANCES.issubset(set(row.get("blocked_ui_affordances", []))):
            fail(errors, f"{label}: blocked UI affordances are incomplete")
        alt = row.get("alt_text", "")
        if not alt or "identity" in alt.lower() or "name" in alt.lower():
            fail(errors, f"{label}: alt text must be a non-identifying visible-fact description")
        if row.get("work_entity_id") == "6529NM-W-0027":
            if row.get("child_subject") is not True:
                fail(errors, "Saman media row must be marked child-sensitive")
            if row.get("accessibility_subject_policy") != "non_identifying_child_subject":
                fail(errors, "Saman media row must use the child-safe accessibility policy")
            if any(term in alt.lower() for term in ("moisés", "moises", "saman", "tripoli", "libya")):
                fail(errors, "Saman child alt text must not identify artist or location")
            if "do not identify" not in row.get("child_display_rule", "").lower():
                fail(errors, "Saman child display rule must prohibit identification")
        if row.get("proposal_object_id") not in row.get("source_record_ids", []):
            fail(errors, f"{label}: source records must retain the proposal object binding")

    if errors:
        print("Media-policy check failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("Media-policy check passed: five exact Work/Media/Wave joins and fail-closed runtime rules")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
