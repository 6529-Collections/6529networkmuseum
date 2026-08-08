"""Validate the isolated Magnum proposal-media join without network access.

This check is deliberately local and fail-closed. It verifies the typed join
from each public Work to the exact historical public Wave URL and rejects any
runtime affordance that would turn proposal-context media into a download,
derivative, preservation object, or identifying child display.
"""

from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import sys
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parents[1]
JOIN_PATH = ROOT / "machine" / "wave-media-join.json"

EXPECTED = (
    ("6529NM-W-0024", "6529NM-MED-0003", "6529NM-PG-2026-001.OBJ-001", "127", "d498d837-3331-4650-a30e-27ca18d53521/magnum-75-127.jpg"),
    ("6529NM-W-0025", "6529NM-MED-0041", "6529NM-PG-2026-001.OBJ-002", "145", "3e2fbdea-cf3c-4949-b3d2-f081cb12de00/magnum-75-145.jpg"),
    ("6529NM-W-0026", "6529NM-MED-0042", "6529NM-PG-2026-001.OBJ-003", "97", "2146f5f7-9352-47e6-bf60-cba46e52c07f/magnum-75-97.jpg"),
    ("6529NM-W-0027", "6529NM-MED-0043", "6529NM-PG-2026-001.OBJ-004", "44", "5d6d9bf0-7ff3-4afd-ac69-c6b34079fbf9/magnum-75-44.jpg"),
    ("6529NM-W-0028", "6529NM-MED-0044", "6529NM-PG-2026-001.OBJ-005", "104", "4526b19e-76df-493b-86ac-105782c061ea/magnum-75-104.jpg"),
)

EXPECTED_CONTEXT = {
    "proposal_id": "6529NM-PG-2026-001",
    "curated_acquisition_id": "6529NM-CA-2026-003",
    "wave_id": "5f207393-5418-4a75-8738-e40edb44a94d",
    "drop_id": "002bfa4f-8416-48bf-b35e-38f354e9a9f0",
    "scope": "historical_public_wave_proposal_context_only",
    "outside_scope": "deny",
}

ALLOWED_AFFORDANCES = {
    "view",
    "hero",
    "alt_text",
    "open_historical_public_wave_url",
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
SAMAN_FORBIDDEN_INFERENCES = {
    "name",
    "age",
    "identity",
    "consent",
    "unpublished location",
    "sensitive metadata",
}


def validate_join(join: dict) -> list[str]:
    """Return all policy violations in a decoded join record."""

    errors: list[str] = []

    def fail(message: str) -> None:
        errors.append(message)

    if join.get("current_public_status") != "Selected by Museum Wave; acquisition review in progress":
        fail("media join must carry the canonical current selected-review status")
    if join.get("publication_boundary") != "historical_public_wave_url_only":
        fail("media join must be historical public URL evidence only")
    if join.get("source_evidence_boundary") != "historical_public_wave_url_evidence_only":
        fail("media join must declare the historical public URL evidence boundary")
    if join.get("authenticated_publication_receipt") is not None:
        fail("no authenticated publication receipt is retained in this corpus")
    if join.get("authenticated_publication_receipt_sha256") is not None:
        fail("an authenticated receipt hash must remain null when no receipt is retained")
    if join.get("prior_status_observation", {}).get("historical_only") is not True:
        fail("the prior PARTICIPATORY observation must remain historical-only")

    runtime = join.get("runtime_policy", {})
    if runtime.get("source_url_policy") != "exact_allowlisted_wave_media_url_only":
        fail("runtime source policy must allow exact URLs only")
    for key, expected in DENY_RUNTIME_FIELDS.items():
        if runtime.get(key) != expected:
            fail(f"runtime policy {key!r} must be {expected!r}")

    rows = join.get("works")
    if not isinstance(rows, list) or len(rows) != len(EXPECTED):
        fail("media join must contain exactly five Work rows")
        rows = rows if isinstance(rows, list) else []

    for row, (work_id, media_id, object_alias, token_id, wave_path) in zip(rows, EXPECTED):
        if not isinstance(row, dict):
            fail("every media row must be an object")
            continue
        label = row.get("proposal_object_alias", "<missing alias>")
        if row.get("work_entity_id") != work_id:
            fail(f"{label}: wrong Work entity ID")
        if row.get("media_reference_entity_id") != media_id:
            fail(f"{label}: wrong Media Reference entity ID")
        if row.get("proposal_object_alias") != object_alias:
            fail(f"{label}: proposal alias drift")
        if row.get("token_id") != token_id:
            fail(f"{label}: token ID drift")
        token_source = row.get("token_source_image_url")
        if not isinstance(token_source, str) or not token_source.startswith("https://arweave.net/"):
            fail(f"{label}: token source image must remain an Arweave URL")
        url = row.get("wave_media_url")
        parsed = urlsplit(url or "")
        if parsed.scheme != "https" or parsed.netloc != "d3lqz0a4bldqgf.cloudfront.net" or parsed.query or parsed.fragment:
            fail(f"{label}: media URL is not an exact allowlisted Wave-upload URL")
        if parsed.path != f"/drops/author_7ee51a67-07b7-4c91-87ed-464c56446c43/{wave_path}":
            fail(f"{label}: Wave-upload URL does not match the retained part/media path")
        if row.get("wave_media_url_type") != "historical_wave_drop_upload":
            fail(f"{label}: Wave media must be typed as historical drop-upload media")
        if row.get("media_status") != "historical_wave_url_reference_only":
            fail(f"{label}: media status must remain historical URL reference only")
        if row.get("rights_label") != "All Rights Reserved":
            fail(f"{label}: rights label must be All Rights Reserved")
        credit = row.get("credit_line", "")
        if "\u00a9" not in credit or "Magnum Photos" not in credit:
            fail(f"{label}: credit must include artist and Magnum copyright notice")
        if set(row.get("allowed_ui_affordances", [])) != ALLOWED_AFFORDANCES:
            fail(f"{label}: allowed UI affordances are not the closed proposal set")
        if not BLOCKED_AFFORDANCES.issubset(set(row.get("blocked_ui_affordances", []))):
            fail(f"{label}: blocked UI affordances are incomplete")
        if row.get("presentation_context") != EXPECTED_CONTEXT:
            fail(f"{label}: display and hero use must be bound to the exact proposal context")
        alt = row.get("alt_text", "")
        if not alt or "identity" in alt.lower() or "name" in alt.lower():
            fail(f"{label}: alt text must be a non-identifying visible-fact description")
        if row.get("work_entity_id") == "6529NM-W-0027":
            if row.get("child_subject") is not True:
                fail("Saman media row must be marked child-sensitive")
            if row.get("accessibility_subject_policy") != "non_identifying_child_subject":
                fail("Saman media row must use the child-safe accessibility policy")
            if any(term in alt.lower() for term in ("moisés", "moises", "saman", "tripoli", "libya")):
                fail("Saman child alt text must not identify artist or location")
            if "do not identify" not in row.get("child_display_rule", "").lower():
                fail("Saman child display rule must prohibit identification")
            identity = row.get("identity_inference")
            if not isinstance(identity, dict):
                fail("Saman media row must carry an identity_inference block")
            else:
                if identity.get("permitted") is not False:
                    fail("Saman identity inference must be prohibited")
                if identity.get("display_policy") != "non_identifying_visible_facts_only":
                    fail("Saman identity inference must use the non-identifying display policy")
                if identity.get("restricted_research_scope") is not True:
                    fail("Saman identity research must remain restricted")
                forbidden = set(identity.get("forbidden_inferences", []))
                if not SAMAN_FORBIDDEN_INFERENCES.issubset(forbidden):
                    fail("Saman identity_inference must forbid identity, age, consent, and sensitive metadata inference")
        if row.get("work_entity_id") == "6529NM-W-0026":
            lowered_alt = alt.lower()
            if "smoke" not in lowered_alt or "canister" not in lowered_alt:
                fail("Bar-Am alt text must remain limited to visible smoke and canister")
            if "gas" in lowered_alt:
                fail("Bar-Am alt text must not infer tear gas")
        if row.get("proposal_object_id") not in row.get("source_record_ids", []):
            fail(f"{label}: source records must retain the proposal object binding")

    return errors


def mutation_test_rejects(base: dict, mutate, label: str) -> str | None:
    """Return an error if a deliberately unsafe mutation is accepted."""

    candidate = deepcopy(base)
    mutate(candidate)
    if validate_join(candidate):
        return None
    return f"mutation test failed to reject {label}"


def validate_mutation_guards(join: dict) -> list[str]:
    """Exercise fail-closed safeguards without network or fixture writes."""

    mutations = (
        ("missing Saman identity_inference", lambda value: value["works"][3].pop("identity_inference", None)),
        ("permitted Saman identity inference", lambda value: value["works"][3]["identity_inference"].update(permitted=True)),
        ("inferred Bar-Am tear gas alt text", lambda value: value["works"][2].update(alt_text="Black-and-white photograph of a person moving through tear gas beside an airborne canister.")),
        ("mutated proposal presentation context", lambda value: value["works"][0]["presentation_context"].update(proposal_id="other")),
        ("presentation outside-scope permission", lambda value: value["works"][1]["presentation_context"].update(outside_scope="allow")),
        ("unsupported historical URL affordance", lambda value: value["works"][2]["allowed_ui_affordances"].__setitem__(3, "open_signed_wave_source")),
    )
    return [error for label, mutate in mutations if (error := mutation_test_rejects(join, mutate, label))]


def main() -> int:
    try:
        join = json.loads(JOIN_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Media-policy check failed to read {JOIN_PATH}: {exc}", file=sys.stderr)
        return 1

    errors = validate_join(join)
    if not errors:
        errors.extend(validate_mutation_guards(join))

    if errors:
        print("Media-policy check failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("Media-policy check passed: five exact Work/Media/Wave joins, context binding, child safeguards, and mutation guards")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
