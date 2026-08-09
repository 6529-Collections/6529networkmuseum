"""Validate the isolated Magnum proposal-media join without network access.

The check is fail-closed. It verifies the exact Work, proposal alias, token
source, historical Wave-upload URL, source fixity observation, current Wave
observation, and route/display policy. It also runs adversarial mutations for
age-sensitive subject safeguards, source swaps, and standalone-route bypasses.
"""

from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from pathlib import Path
import re
import sys
from urllib.parse import urlsplit


REPOSITORY = Path(__file__).resolve().parents[2]
ROOT = REPOSITORY / "records" / "proposed-gifts" / "6529NM-PG-2026-001" / "public" / "scholarship"
JOIN_PATH = ROOT / "machine" / "wave-media-join.json"
PROJECTIONS_PATH = ROOT / "machine" / "work-projections.json"
INTEGRATION_PATH = ROOT / "machine" / "integration-map.json"
EVIDENCE_PATH = REPOSITORY / "records" / "proposed-gifts" / "6529NM-PG-2026-001" / "evidence" / "wave-publication-observation-public-safe-2026-08-09.json"
EVIDENCE_RELATIVE = "records/proposed-gifts/6529NM-PG-2026-001/evidence/wave-publication-observation-public-safe-2026-08-09.json"
CANONICAL_PUBLICATION_PATH = "records/proposed-gifts/6529NM-PG-2026-001/wave-publication-observation-2026-08-08.json"
CANONICAL_PUBLICATION_FILE = REPOSITORY / CANONICAL_PUBLICATION_PATH

BASE_URL = "https://d3lqz0a4bldqgf.cloudfront.net/drops/author_7ee51a67-07b7-4c91-87ed-464c56446c43/"
CURRENT_OBSERVATION = {
    "record_type": "WAVE_STATUS_OBSERVATION",
    "observation_id": "6529NM-WAVE-OBS-2026-08-08-001",
    "observed_at": "2026-08-08T10:15:02.0167151Z",
    "payload_sha256": "sha256:beae463453c21a3e8e51e311f8d8b0d8e516b9a63b43dd6c2000d1d441d4a097",
}
CURRENT_PUBLICATION = {
    "record_type": "WAVE_PUBLICATION_OBSERVATION",
    "observation_id": "6529NM-WAVE-PUB-OBS-2026-08-08-001",
    "observed_at": "2026-08-08T10:15:02.0167151Z",
    "payload_sha256": "sha256:887d527756721cae1bf758a8205d1f5f7e0d1cebee2b3f27aafcab5271132995",
    "binding_status": "bound_canonical_wave_publication_observation",
    "receipt_path": CANONICAL_PUBLICATION_PATH,
    "receipt_sha256": "sha256:b1f57fa0010bdaf0f9f21854f88e446e7f20b4a1921ab6fd075d4836c5920e58",
}
PROJECTION_PUBLICATION = dict(CURRENT_PUBLICATION)
SUPPLEMENTAL_PUBLIC_SAFE = {
    "evidence_id": "6529NM-WAVE-PUB-OBS-2026-08-09-001",
    "observed_at": "2026-08-09T02:04:21.7672652Z",
    "payload_sha256": "sha256:93e968562297fe5acff792e027f302b938ba6fa1ac88284754c4ba684d1266a2",
    "path": EVIDENCE_RELATIVE,
    "file_sha256": "sha256:2d102b1e5ee4c448bad0631d3bb659949456d74a342f6203b3a1dd12d5f29d6a",
    "role": "later public-safe API evidence for unchanged signed WINNER and public media URL/MIME/status fields; not a replacement for the enveloped canonical observation",
}
EXPECTED_PUBLICATION_SOURCE = "punk6529bot drops get 002bfa4f-8416-48bf-b35e-38f354e9a9f0 --json"
EXPECTED_WAVE_MEDIA = {
    1: ("https://d3lqz0a4bldqgf.cloudfront.net/drops/author_7ee51a67-07b7-4c91-87ed-464c56446c43/f8006332-4f8a-4556-b0df-3c43eec16334/conflict-at-its-edges-cover.png", "image/png"),
    2: ("https://d3lqz0a4bldqgf.cloudfront.net/drops/author_7ee51a67-07b7-4c91-87ed-464c56446c43/d498d837-3331-4650-a30e-27ca18d53521/magnum-75-127.jpg", "image/jpeg"),
    3: ("https://d3lqz0a4bldqgf.cloudfront.net/drops/author_7ee51a67-07b7-4c91-87ed-464c56446c43/3e2fbdea-cf3c-4949-b3d2-f081cb12de00/magnum-75-145.jpg", "image/jpeg"),
    4: ("https://d3lqz0a4bldqgf.cloudfront.net/drops/author_7ee51a67-07b7-4c91-87ed-464c56446c43/2146f5f7-9352-47e6-bf60-cba46e52c07f/magnum-75-97.jpg", "image/jpeg"),
    5: ("https://d3lqz0a4bldqgf.cloudfront.net/drops/author_7ee51a67-07b7-4c91-87ed-464c56446c43/5d6d9bf0-7ff3-4afd-ac69-c6b34079fbf9/magnum-75-44.jpg", "image/jpeg"),
    6: ("https://d3lqz0a4bldqgf.cloudfront.net/drops/author_7ee51a67-07b7-4c91-87ed-464c56446c43/4526b19e-76df-493b-86ac-105782c061ea/magnum-75-104.jpg", "image/jpeg"),
}
EXPECTED = (
    {
        "work": "6529NM-W-0024", "media": "6529NM-MED-0003", "alias": "6529NM-PG-2026-001.OBJ-001", "token": "127",
        "wave_path": "d498d837-3331-4650-a30e-27ca18d53521/magnum-75-127.jpg",
        "source": "https://arweave.net/VE0zO2N1zVTsbEUHdUFazEgvuMbmVOi6OfaWfQOWkaM",
        "sha256": "sha256:65abf8b6a182bb641787a43b40d10f0b6471357e5c90777aacccf9eb73ea1453", "bytes": 2518674, "width": 3056, "height": 4600,
        "credit": "David Seymour, Negev, 1952. © David Seymour/Magnum Photos 2022. All Rights Reserved.",
    },
    {
        "work": "6529NM-W-0025", "media": "6529NM-MED-0041", "alias": "6529NM-PG-2026-001.OBJ-002", "token": "145",
        "wave_path": "3e2fbdea-cf3c-4949-b3d2-f081cb12de00/magnum-75-145.jpg",
        "source": "https://arweave.net/r0bUW6Mtxq897pgig0V01Ad43S_Ldwv3tARjwmjrqpE",
        "sha256": "sha256:e60f2d2c56b702981597606315c6c77e07dedf4dd9a95804ae2da720d0f5bcee", "bytes": 1813285, "width": 5369, "height": 3601,
    },
    {
        "work": "6529NM-W-0026", "media": "6529NM-MED-0042", "alias": "6529NM-PG-2026-001.OBJ-003", "token": "97",
        "wave_path": "2146f5f7-9352-47e6-bf60-cba46e52c07f/magnum-75-97.jpg",
        "source": "https://arweave.net/vRmOcFJRTK84ILXp2Tkjz5KoS4iXXbMqki7rxhTYlr4",
        "sha256": "sha256:a59d8624c8da11758c5f1c0b64484229e4ffb68167b8e5783cdbafa9628b74df", "bytes": 1666083, "width": 5000, "height": 3292,
    },
    {
        "work": "6529NM-W-0027", "media": "6529NM-MED-0043", "alias": "6529NM-PG-2026-001.OBJ-004", "token": "44",
        "wave_path": "5d6d9bf0-7ff3-4afd-ac69-c6b34079fbf9/magnum-75-44.jpg",
        "source": "https://arweave.net/zLifpzu3AQWqjg59nuy9jeRqHPA5o5-LpwwBqNRcD5o",
        "sha256": "sha256:cf1ec75dc4e3de3bcd85cffd9954c75395d9af2bff38374468440e403352b816", "bytes": 1540870, "width": 5616, "height": 3744,
    },
    {
        "work": "6529NM-W-0028", "media": "6529NM-MED-0044", "alias": "6529NM-PG-2026-001.OBJ-005", "token": "104",
        "wave_path": "4526b19e-76df-493b-86ac-105782c061ea/magnum-75-104.jpg",
        "source": "https://arweave.net/oz0t0DJj2BgFCux1WXskxisxvzV2KA0ukqaVbQ1Ckco",
        "sha256": "sha256:49c45762f344fcc058a1f1167b01e9c298b1f4cff5e200e9033577f9c1023ad2", "bytes": 16871807, "width": 5964, "height": 4768,
    },
)

EXPECTED_CONTEXT = {
    "proposal_id": "6529NM-PG-2026-001",
    "curated_acquisition_id": "6529NM-CA-2026-003",
    "wave_id": "5f207393-5418-4a75-8738-e40edb44a94d",
    "drop_id": "002bfa4f-8416-48bf-b35e-38f354e9a9f0",
    "scope": "historical_public_wave_proposal_context_only",
    "outside_scope": "deny",
}
ALLOWED_AFFORDANCES = {"alt_text", "copy_citation"}
BLOCKED_AFFORDANCES = {"download", "full_resolution", "zoom", "fullscreen", "iiif", "preservation_master"}
EXPECTED_ROUTE_POLICY = "deny_without_verified_work_ca_media_observation_relation"
EXPECTED_EVIDENCE_SCOPE = "Each Work array is the complete set of source-register IDs explicitly cited on that public Work page, including contextual cross-references and the shared historical Wave-publication source."
DENY_RUNTIME_FIELDS = {
    "url_rewrite": "deny", "runtime_fallback": "deny", "runtime_fetch": "deny",
    "repository_derivative": "deny",
    "responsive_variants": "deny", "download": "deny", "full_resolution_claim": "deny",
    "zoom": "deny", "fullscreen": "deny", "iiif_or_tiled_service": "deny", "preservation_claim": "deny",
}
SAMAN_FORBIDDEN_INFERENCES = {
    "name", "age", "identity", "consent", "unpublished location", "sensitive metadata",
    "sensitive visual context", "visual cause", "weapon attribution",
}
SAMAN_UNSAFE_TERMS = ("moises", "moisés", "saman", "tripoli", "libya", "name", "age", "identity", "air strike", "weapon")


BARAM_CURRENT_SAFE_ALT = "Black-and-white photograph of a person moving beside smoke and an airborne canister at the Western Wall, with a metal menorah barrier in the foreground."
BARAM_HISTORICAL_ALT = "Black-and-white photograph of a person running through tear gas at the Western Wall, with a canister in the air and a metal menorah barrier in the foreground."
BARAM_HISTORICAL_ALT_SHA256 = "sha256:ac2b178e1cb05f3f8c33aee655e763fc2d18261b2c1e6e67f72d77d16f4fc9a2"


def contains_term(text: str, term: str) -> bool:
    return re.search(r"(?<!\w)" + re.escape(term) + r"(?!\w)", text, flags=re.IGNORECASE) is not None


def canonical_payload(payload: dict) -> bytes:
    return json.dumps(payload, ensure_ascii=False, separators=(",", ":"), sort_keys=True).encode("utf-8")


def validate_visitor_markdown_media_affordances(
    join: dict,
    documents: list[tuple[str | Path, str]] | None = None,
) -> list[str]:
    """Reject image embeds and direct restricted-photo locators in visitor prose."""

    restricted_urls = {
        url
        for row in join.get("works", [])
        if isinstance(row, dict)
        for url in (row.get("token_source_image_url"), row.get("wave_media_url"))
        if isinstance(url, str) and url
    }
    if documents is None:
        documents = [
            (path.relative_to(ROOT), path.read_text(encoding="utf-8"))
            for path in sorted(ROOT.rglob("*.md"))
        ]

    errors: list[str] = []
    for label, text in documents:
        if re.search(r"!\[[^\]]*\]\(https?://", text):
            errors.append(f"{label}: visitor manuscript must not embed remote media")
        for url in sorted(restricted_urls):
            if url in text:
                errors.append(f"{label}: visitor manuscript exposes a restricted direct photograph locator")
    return errors


def validate_publication_evidence(evidence: dict) -> list[str]:
    errors: list[str] = []
    if evidence.get("evidence_type") != "WAVE_PUBLICATION_PUBLIC_SAFE_EVIDENCE":
        errors.append("publication evidence must carry the public-safe evidence type")
    if evidence.get("observation_id") != SUPPLEMENTAL_PUBLIC_SAFE["evidence_id"]:
        errors.append("publication evidence must carry the current observation ID")
    if evidence.get("observed_at") != SUPPLEMENTAL_PUBLIC_SAFE["observed_at"]:
        errors.append("publication evidence time must match the bound observation")
    if evidence.get("source_command") != EXPECTED_PUBLICATION_SOURCE:
        errors.append("publication evidence must retain the exact safe source command")
    payload = evidence.get("payload")
    if not isinstance(payload, dict):
        return errors + ["publication evidence must contain a payload object"]
    expected_payload_keys = {"drop_id", "drop_serial_no", "drop_type", "is_signed", "observed_at", "parts", "wave_id", "wave_name"}
    if set(payload) != expected_payload_keys:
        errors.append("publication payload must contain only the public Wave identity/state/media fields")
    if payload.get("drop_id") != "002bfa4f-8416-48bf-b35e-38f354e9a9f0" or payload.get("drop_serial_no") != 1276093:
        errors.append("publication payload has the wrong drop identity or serial")
    if payload.get("wave_id") != "5f207393-5418-4a75-8738-e40edb44a94d" or payload.get("wave_name") != "6529 Network Museum":
        errors.append("publication payload has the wrong Wave identity")
    if payload.get("drop_type") != "WINNER" or payload.get("is_signed") is not True:
        errors.append("publication payload must preserve signed WINNER state")
    if payload.get("observed_at") != SUPPLEMENTAL_PUBLIC_SAFE["observed_at"]:
        errors.append("publication payload time must match the record observation time")
    parts = payload.get("parts")
    if not isinstance(parts, list) or [part.get("part_id") for part in parts if isinstance(part, dict)] != list(range(1, 8)):
        errors.append("publication payload must contain parts 1 through 7 in order")
        parts = parts if isinstance(parts, list) else []
    for part in parts:
        if not isinstance(part, dict) or set(part) != {"part_id", "media"}:
            errors.append("each publication part must contain only part_id and media")
            continue
        media = part.get("media")
        if not isinstance(media, list):
            errors.append(f"part {part.get('part_id')}: media must be an array")
            continue
        if part.get("part_id") == 7 and media:
            errors.append("part 7 must have no media binding")
        if part.get("part_id") in EXPECTED_WAVE_MEDIA:
            if len(media) != 1:
                errors.append(f"part {part.get('part_id')}: expected one public media binding")
            else:
                item = media[0]
                if set(item) != {"url", "mime_type", "media_status"}:
                    errors.append(f"part {part.get('part_id')}: media binding contains non-public fields")
                expected_url, expected_mime = EXPECTED_WAVE_MEDIA[part["part_id"]]
                if item.get("url") != expected_url or item.get("mime_type") != expected_mime or item.get("media_status") != "ready":
                    errors.append(f"part {part.get('part_id')}: public media binding drift")
    payload_text = json.dumps(payload, ensure_ascii=False, sort_keys=True)
    if any(term in payload_text.lower() for term in ("profile", "rater", "credential", "reaction")):
        errors.append("publication payload must exclude profile, rater, credential, and reaction data")
    expected_hash = "sha256:" + hashlib.sha256(canonical_payload(payload)).hexdigest()
    if evidence.get("payload_sha256") != expected_hash:
        errors.append("publication evidence payload hash does not match the declared canonicalization")
    note = evidence.get("exclusion_note", "").lower()
    if not all(term in note for term in ("donor authority", "legal title", "copyright", "custody", "accession", "display permission")):
        errors.append("publication evidence must carry the no-authority exclusion note")
    return errors


def validate_observations(join: dict) -> list[str]:
    errors: list[str] = []
    if join.get("current_status_observation") != CURRENT_OBSERVATION:
        errors.append("media join must carry the exact current WINNER observation ID, time, and payload hash")
    publication = join.get("current_publication_observation")
    if publication != CURRENT_PUBLICATION:
        errors.append("publication observation must carry the exact canonical enveloped receipt binding")
    if join.get("supplemental_public_safe_media_evidence") != SUPPLEMENTAL_PUBLIC_SAFE:
        errors.append("media join must preserve the exact later public-safe media evidence without replacing the canonical observation")
    binding = join.get("publication_observation_binding", {})
    expected_binding = {
        "record_type": "WAVE_PUBLICATION_OBSERVATION",
        "record_id": CURRENT_PUBLICATION["observation_id"],
        "payload_sha256": CURRENT_PUBLICATION["payload_sha256"],
        "receipt_path": CANONICAL_PUBLICATION_PATH,
        "receipt_sha256": CURRENT_PUBLICATION["receipt_sha256"],
        "required_after_rebase": False,
        "status": "bound_canonical_observation_and_graph",
        "source_record_currently_used": CANONICAL_PUBLICATION_PATH,
    }
    if binding != expected_binding:
        errors.append("media join must bind the exact public-safe receipt and canonical graph")
    return errors


def validate_join(join: dict) -> list[str]:
    """Return all policy violations in a decoded join record."""

    errors = validate_observations(join)

    def fail(message: str) -> None:
        errors.append(message)

    if join.get("current_public_status") != "Selected by Museum Wave; acquisition review in progress":
        fail("media join must carry the canonical current selected-review status")
    if join.get("publication_boundary") != "historical_public_wave_url_only":
        fail("media join must be historical public URL evidence only")
    if join.get("source_evidence_boundary") != "historical_public_wave_url_with_publication_observation":
        fail("media join must declare the historical URL plus live publication-observation boundary")
    if join.get("source_record") != "records/proposed-gifts/6529NM-PG-2026-001/wave-storm.json":
        fail("wave-storm is retained only as the historical URL evidence source record")
    if join.get("authenticated_publication_receipt") != CANONICAL_PUBLICATION_PATH or join.get("authenticated_publication_receipt_sha256") != CURRENT_PUBLICATION["receipt_sha256"]:
        fail("the exact canonical publication observation path and hash must be retained")
    if join.get("prior_status_observation", {}).get("historical_only") is not True:
        fail("the prior PARTICIPATORY observation must remain historical-only")

    route = join.get("route_policy", {})
    if route.get("standalone_work_route") != "deny_without_verified_work_ca_media_observation_relation":
        fail("standalone Work routes must fail closed until the final graph relation is verified")
    if route.get("outside_scope") != "deny" or route.get("fail_closed") is not True:
        fail("route policy must fail closed outside the selected offer context")
    if route.get("historical_label_required") != "Wave-source historical proposal media":
        fail("historical Wave label must be required")

    runtime = join.get("runtime_policy", {})
    if runtime.get("source_url_policy") != "recorded_evidence_locator_no_runtime_fetch":
        fail("runtime source policy must retain locators without fetching them")
    for key, expected in DENY_RUNTIME_FIELDS.items():
        if runtime.get(key) != expected:
            fail(f"runtime policy {key!r} must be {expected!r}")
    age_rule = str(runtime.get("age_sensitive_subject_rule") or "").lower()
    if "apparently young" not in age_rule or "without assigning an age or child classification" not in age_rule:
        fail("runtime policy must prohibit inferred age and child classification for an apparently young subject")
    if "sha256:" + hashlib.sha256(BARAM_HISTORICAL_ALT.encode("utf-8")).hexdigest() != BARAM_HISTORICAL_ALT_SHA256:
        fail("Bar-Am historical alt hash fixture is internally inconsistent")

    rows = join.get("works")
    if not isinstance(rows, list) or len(rows) != len(EXPECTED):
        fail("media join must contain exactly five Work rows")
        rows = rows if isinstance(rows, list) else []

    for row, expected in zip(rows, EXPECTED):
        if not isinstance(row, dict):
            fail("every media row must be an object")
            continue
        label = row.get("proposal_object_alias", "<missing alias>")
        if row.get("work_entity_id") != expected["work"]:
            fail(f"{label}: wrong Work entity ID")
        if row.get("media_reference_entity_id") != expected["media"]:
            fail(f"{label}: wrong Media Reference entity ID")
        if row.get("proposal_object_alias") != expected["alias"] or row.get("proposal_object_id") != expected["alias"]:
            fail(f"{label}: proposal alias drift")
        if row.get("token_id") != expected["token"]:
            fail(f"{label}: token ID drift")
        if row.get("token_source_image_url") != expected["source"]:
            fail(f"{label}: token-linked source URL drift")
        source_fixity = row.get("source_image_fixity", {})
        for key in ("sha256", "bytes", "width", "height"):
            if source_fixity.get(key) != expected[key]:
                fail(f"{label}: source image {key} must remain the exact observed value")
        url = row.get("wave_media_url")
        parsed = urlsplit(url or "")
        if parsed.scheme != "https" or parsed.netloc != "d3lqz0a4bldqgf.cloudfront.net" or parsed.query or parsed.fragment:
            fail(f"{label}: media URL is not an exact allowlisted Wave-upload URL")
        if parsed.path != BASE_URL.replace("https://d3lqz0a4bldqgf.cloudfront.net", "") + expected["wave_path"]:
            fail(f"{label}: Wave-upload URL does not match the retained part/media path")
        if row.get("wave_media_url_type") != "historical_wave_drop_upload" or row.get("media_status") != "non_rendering_historical_source_locator":
            fail(f"{label}: Wave media must remain a non-rendering historical source locator")
        if row.get("rights_label") != "All Rights Reserved":
            fail(f"{label}: rights label must be All Rights Reserved")
        credit = row.get("credit_line", "")
        if "\u00a9" not in credit or "Magnum Photos" not in credit:
            fail(f"{label}: credit must include the supplied artist/Magnum copyright notice")
        if expected.get("credit") is not None and credit != expected["credit"]:
            fail(f"{label}: credit line must exactly preserve the canonical historical Wave credit")
        if set(row.get("allowed_ui_affordances", [])) != ALLOWED_AFFORDANCES or not BLOCKED_AFFORDANCES.issubset(set(row.get("blocked_ui_affordances", []))):
            fail(f"{label}: UI affordances are not the closed proposal set")
        if row.get("presentation_context") != EXPECTED_CONTEXT:
            fail(f"{label}: display and hero use must be bound to the exact proposal context")
        display = row.get("standalone_work_display", {})
        if display.get("requires_verified_graph_relation") is not True or display.get("historical_label_required") is not True or display.get("outside_scope") != "deny" or display.get("verification_status") != "canonical_graph_verified_display_authority_withheld":
            fail(f"{label}: standalone Work display must remain closed despite a verified graph because display authority is withheld")
        if row.get("load_policy") != "blocked_pending_reviewed_display_authority":
            fail(f"{label}: upstream source loading must remain blocked pending reviewed display authority")
        alt = row.get("alt_text", "")
        if not alt or any(contains_term(alt, term) for term in ("identity", "name", "age", "tear gas")):
            fail(f"{label}: alt text must remain a non-identifying visible-fact description")
        if row.get("work_entity_id") == "6529NM-W-0027":
            if row.get("accessibility_subject_policy") != "non_identifying_apparently_young_subject":
                fail("Saman media row must carry the exact age-sensitive accessibility policy")
            if row.get("age_classification") != "unverified_apparently_young_subject" or row.get("subject_age_documentation") != "not_available_in_reviewed_public_record":
                fail("Saman media row must state that age classification is unverified and undocumented")
            if "apparently young person" not in alt.lower() or contains_term(alt, "child"):
                fail("Saman alt text must preserve apparent youth without assigning a child classification")
            if any(contains_term(alt, term) for term in SAMAN_UNSAFE_TERMS):
                fail("Saman alt text must not expose identity, age, artist, location, or cause")
            rule = str(row.get("subject_display_rule") or "").lower()
            if "do not identify" not in rule or "assign an age or child classification" not in rule or "visible-fact level" not in rule:
                fail("Saman display rule must prohibit identity, age, and child-classification inference")
            identity = row.get("identity_inference")
            if not isinstance(identity, dict):
                fail("Saman media row must carry an identity_inference block")
            else:
                if identity.get("permitted") is not False or identity.get("display_policy") != "non_identifying_visible_facts_only" or identity.get("restricted_research_scope") is not True:
                    fail("Saman identity inference must be prohibited and restricted")
                if not SAMAN_FORBIDDEN_INFERENCES.issubset(set(identity.get("forbidden_inferences", []))):
                    fail("Saman identity_inference must forbid identity, age, consent, sensitive context, cause, and weapon inference")
        if row.get("work_entity_id") == "6529NM-W-0026":
            lowered_alt = alt.lower()
            if "smoke" not in lowered_alt or "canister" not in lowered_alt or "gas" in lowered_alt:
                fail("Bar-Am alt text must remain limited to visible smoke and canister")
            if alt != BARAM_CURRENT_SAFE_ALT:
                fail("Bar-Am current safe alt must remain the visible smoke/canister description")
            amendment = row.get("alt_text_amendment_binding", {})
            supersedes = amendment.get("supersedes", {})
            if (
                amendment.get("status") != "canonical_current_safe_description"
                or amendment.get("historical_seven_part_wording_preserved") is not True
                or supersedes.get("source_record") != "records/proposed-gifts/6529NM-PG-2026-001/wave-storm.json"
                or supersedes.get("record_revision") != 1
                or supersedes.get("part_number") != 4
                or supersedes.get("media_index") != 0
                or supersedes.get("assertion_path") != "media.alt_text"
                or supersedes.get("assertion_sha256") != BARAM_HISTORICAL_ALT_SHA256
            ):
                fail("Bar-Am safe alt must preserve the canonical current description and historical wording")
            historical = row.get("historical_publication_media", {})
            historical_text = historical.get("alt_text", "")
            recomputed_historical_hash = "sha256:" + hashlib.sha256(historical_text.encode("utf-8")).hexdigest()
            if (
                historical_text != BARAM_HISTORICAL_ALT
                or historical.get("source_record") != "records/proposed-gifts/6529NM-PG-2026-001/wave-storm.json"
                or historical.get("record_revision") != 1
                or historical.get("part_number") != 4
                or historical.get("media_index") != 0
                or historical.get("wording_status") != "retained_historical_seven_part_publication_wording"
                or historical.get("alt_text") != historical_text
                or historical.get("alt_text_sha256") != recomputed_historical_hash
            ):
                fail("Bar-Am historical seven-part wording and its exact source hash must be retained")
        if row.get("proposal_object_id") not in row.get("source_record_ids", []):
            fail(f"{label}: source records must retain the proposal object binding")
    return errors


def validate_work_projections(projections: dict, join: dict, integration: dict) -> list[str]:
    errors: list[str] = []
    if projections.get("current_status_observation") != CURRENT_OBSERVATION:
        errors.append("work projections must carry the exact current WINNER observation ID, time, and payload hash")
    if projections.get("current_publication_observation") != PROJECTION_PUBLICATION:
        errors.append("work projections must carry the exact bound public-safe publication receipt")
    if projections.get("current_public_status") != "Selected by Museum Wave; acquisition review in progress":
        errors.append("work projections must use the selected-review public status")
    if projections.get("current_lifecycle") != "selected_by_museum_wave_acquisition_review_in_progress" or projections.get("collection_membership") != "not_in_collection":
        errors.append("work projections must preserve selected-review lifecycle and outside-Collection membership")
    if projections.get("evidence_sources_scope") != EXPECTED_EVIDENCE_SCOPE:
        errors.append("work projections must define evidence_sources as the complete cited source-register set")
    integration_media = integration.get("entity_projections", {}).get("media_references", {})
    if integration_media.get("standalone_work_route") != EXPECTED_ROUTE_POLICY:
        errors.append("integration map standalone Work route policy has drifted")
    join_by_work = {
        row.get("work_entity_id"): row
        for row in join.get("works", [])
        if isinstance(row, dict)
    }
    for row in projections.get("works", []):
        work_id = row.get("canonical_work_id")
        public_page = row.get("public_page")
        if not isinstance(public_page, str) or not (REPOSITORY / public_page).is_file():
            errors.append(f"{work_id}: public Work page is missing")
        else:
            try:
                public_page_text = (REPOSITORY / public_page).read_text(encoding="utf-8")
            except OSError as exc:
                errors.append(f"{work_id}: public Work page cannot be read: {exc}")
            else:
                cited = sorted(set(re.findall(r"\bS\d{2,}\b", public_page_text)))
                if row.get("evidence_sources") != cited:
                    errors.append(f"{work_id}: evidence_sources must exactly equal the source IDs cited on its public Work page")
        for manifestation in row.get("manifestations", []):
            if manifestation.get("type") == "historical_wave_presentation_media":
                if manifestation.get("wave_publication_observation_id") != CURRENT_PUBLICATION["observation_id"] or manifestation.get("wave_publication_observation_binding") != "bound_canonical_wave_publication_observation":
                    errors.append(f"{row.get('canonical_work_id')}: manifestation lacks current publication observation binding")
                if (
                    manifestation.get("standalone_route") != "deny"
                    or manifestation.get("display_scope") != "non_rendering_evidence_only"
                    or manifestation.get("load_policy") != "blocked_pending_reviewed_display_authority"
                ):
                    errors.append(f"{row.get('canonical_work_id')}: manifestation must remain non-rendering and fail closed")
                if row.get("canonical_work_id") == "6529NM-W-0026":
                    binding = manifestation.get("alt_text_amendment_binding", {})
                    supersedes = binding.get("supersedes", {})
                    if (
                        binding.get("status") != "canonical_current_safe_description"
                        or binding.get("historical_seven_part_wording_preserved") is not True
                        or supersedes.get("source_record") != "records/proposed-gifts/6529NM-PG-2026-001/wave-storm.json"
                        or supersedes.get("record_revision") != 1
                        or supersedes.get("part_number") != 4
                        or supersedes.get("media_index") != 0
                        or supersedes.get("assertion_path") != "media.alt_text"
                        or supersedes.get("assertion_sha256") != BARAM_HISTORICAL_ALT_SHA256
                    ):
                        errors.append("6529NM-W-0026: projected Bar-Am manifestation lacks the exact canonical safe-alt binding")
                if work_id == "6529NM-W-0027":
                    expected_identity = join_by_work.get(work_id, {}).get("identity_inference")
                    if manifestation.get("identity_inference") != expected_identity:
                        errors.append("6529NM-W-0027: projected and media-join identity safeguards must match exactly")
    return errors


def mutation_test_rejects(base: dict, mutate, label: str) -> str | None:
    candidate = deepcopy(base)
    mutate(candidate)
    if validate_join(candidate):
        return None
    return f"mutation test failed to reject {label}"


def validate_mutation_guards(join: dict) -> list[str]:
    mutations = (
        ("missing Saman identity_inference", lambda value: value["works"][3].pop("identity_inference", None)),
        ("permitted Saman identity inference", lambda value: value["works"][3]["identity_inference"].update(permitted=True)),
        ("Saman unsafe visual/context alt", lambda value: value["works"][3].update(alt_text="The identified nine-year-old child in Tripoli stands beside a house hit by an air strike.")),
        ("Saman display rule allowing inferred age", lambda value: value["works"][3].update(subject_display_rule="Identify the child and publish an estimated age.")),
        ("Saman swapped exact source URL", lambda value: value["works"][3].update(token_source_image_url=value["works"][0]["token_source_image_url"])),
        ("Saman swapped source fixity", lambda value: value["works"][3]["source_image_fixity"].update(sha256=value["works"][0]["source_image_fixity"]["sha256"])),
        ("inferred Bar-Am tear gas alt text", lambda value: value["works"][2].update(alt_text="Black-and-white photograph of a person moving through tear gas beside an airborne canister.")),
        ("mutated Bar-Am historical wording", lambda value: value["works"][2]["historical_publication_media"].update(alt_text="Black-and-white photograph of a person moving beside smoke.")),
        ("mutated Bar-Am historical wording hash", lambda value: value["works"][2]["historical_publication_media"].update(alt_text_sha256="sha256:0000000000000000000000000000000000000000000000000000000000000000")),
        ("missing Bar-Am historical publication record", lambda value: value["works"][2].pop("historical_publication_media", None)),
        ("missing Bar-Am amendment binding", lambda value: value["works"][2].pop("alt_text_amendment_binding", None)),
        ("mutated proposal presentation context", lambda value: value["works"][0]["presentation_context"].update(proposal_id="other")),
        ("presentation outside-scope permission", lambda value: value["works"][1]["presentation_context"].update(outside_scope="allow")),
        ("standalone route bypass", lambda value: value["works"][1]["standalone_work_display"].update(outside_scope="allow", verification_status="verified")),
        ("unsupported historical URL affordance", lambda value: value["works"][2]["allowed_ui_affordances"].append("open_signed_wave_source")),
        ("mutated current observation time", lambda value: value["current_status_observation"].update(observed_at="2026-08-08T09:06:07.985Z")),
    )
    return [error for label, mutate in mutations if (error := mutation_test_rejects(join, mutate, label))]


def main() -> int:
    try:
        join = json.loads(JOIN_PATH.read_text(encoding="utf-8"))
        projections = json.loads(PROJECTIONS_PATH.read_text(encoding="utf-8"))
        integration = json.loads(INTEGRATION_PATH.read_text(encoding="utf-8"))
        evidence = json.loads(EVIDENCE_PATH.read_text(encoding="utf-8"))
        evidence_bytes = EVIDENCE_PATH.read_bytes()
        canonical_publication_bytes = CANONICAL_PUBLICATION_FILE.read_bytes()
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Media-policy check failed to read machine/evidence records: {exc}", file=sys.stderr)
        return 1

    errors = validate_publication_evidence(evidence)
    evidence_file_hash = "sha256:" + hashlib.sha256(evidence_bytes).hexdigest()
    canonical_file_hash = "sha256:" + hashlib.sha256(canonical_publication_bytes).hexdigest()
    if evidence_file_hash != SUPPLEMENTAL_PUBLIC_SAFE["file_sha256"]:
        errors.append("supplemental public-safe media evidence file hash drift")
    if canonical_file_hash != CURRENT_PUBLICATION["receipt_sha256"]:
        errors.append("canonical Wave publication observation file hash drift")
    errors.extend(validate_join(join))
    errors.extend(validate_work_projections(projections, join, integration))
    errors.extend(validate_visitor_markdown_media_affordances(join))
    works = join.get("works")
    if not isinstance(works, list) or len(works) < 4 or not isinstance(works[3], dict):
        errors.append("Saman accessibility check requires the fourth exact Work row")
    else:
        saman_alt = str(works[3].get("alt_text") or "").lower()
        if "impact mark" in saman_alt or "bullet" in saman_alt or "air strike" in saman_alt:
            errors.append("Saman accessibility text must not infer the cause of visible wall marks")
    if not errors:
        errors.extend(validate_mutation_guards(join))
    if errors:
        print("Media-policy check failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("Media-policy check passed: exact five Work/Media joins, current observations, route gates, source fixity, age-sensitive safeguards, visitor locator suppression, and mutation guards")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
