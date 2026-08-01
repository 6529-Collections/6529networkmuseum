#!/usr/bin/env python3
"""Bind the Casey dossier to the merged descriptor package and refresh commitments."""

from __future__ import annotations

import copy
import hashlib
import json
import re
from pathlib import Path
from typing import Any

from canonical import canonicalize
from validate import keccak256
from validate_casey_dossier import PUBLISHED_SOURCE_COMMIT, source_package


ROOT = Path(__file__).resolve().parent.parent
CASEY_DIR = ROOT / "records" / "accessions" / "6529NM.2026.001"
REPOSITORY_URL = "https://github.com/6529-Collections/6529networkmuseum"
MAIN_TREE_URL = f"{REPOSITORY_URL}/tree/main"
MAIN_BLOB_URL = f"{REPOSITORY_URL}/blob/main"
STALE_BRANCH = "codex" + "/casey-reas-accession"
STALE_TREE_URL = f"{REPOSITORY_URL}/tree/{STALE_BRANCH}"
STALE_BLOB_URL = f"{REPOSITORY_URL}/blob/{STALE_BRANCH}"

OBJECT_TO_COLLECTION = {
    "6529NM.2026.001.01": "century",
    "6529NM.2026.001.02": "century",
    "6529NM.2026.001.03": "century",
    "6529NM.2026.001.04": "pre-process",
    "6529NM.2026.001.05": "phototaxis",
    "6529NM.2026.001.06": "923-empty-rooms",
    "6529NM.2026.001.07": "ex-nihilo-cosmos",
}

NON_CLAIMS = [
    "No OpenSea or other marketplace metric is used.",
    "No aesthetic, quality, value, or ranking claim is made.",
]


def read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def sha256(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def casey_payload_sha256(payload: dict[str, Any]) -> str:
    body = {key: value for key, value in payload.items() if key != "payload_sha256"}
    return "sha256:" + hashlib.sha256(canonicalize(body)).hexdigest()


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def descriptor_package() -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    source, descriptors, issues = source_package(ROOT)
    if issues:
        raise ValueError("; ".join(issues))
    return source, descriptors


def trait_analysis(source: dict[str, Any], descriptor: dict[str, Any] | None = None) -> dict[str, Any]:
    value: dict[str, Any] = {
        "status": "transparent_linked_descriptors_available",
        "method": "Museum published NextGen-compatible method over the frozen source package; linked descriptors are available and reproducible.",
        "marketplace_metrics": "not_used",
        "non_claims": NON_CLAIMS,
        "source_package": copy.deepcopy(source),
    }
    if descriptor is not None:
        value["descriptor"] = copy.deepcopy(descriptor)
    return value


def replace_stale_urls(value: Any) -> Any:
    if isinstance(value, str):
        return value.replace(STALE_TREE_URL, MAIN_TREE_URL).replace(STALE_BLOB_URL, MAIN_BLOB_URL)
    if isinstance(value, list):
        return [replace_stale_urls(item) for item in value]
    if isinstance(value, dict):
        return {key: replace_stale_urls(item) for key, item in value.items()}
    return value


def refresh_record(path: Path, source: dict[str, Any], descriptors: dict[str, dict[str, Any]]) -> None:
    record = replace_stale_urls(read_json(path))
    payload = record["payload"]
    record_id = payload["record_id"]
    if record_id == "6529NM.2026.001":
        payload["source"].pop("casey_collection_snapshot_package_commit", None)
        payload["source"]["casey_collection_snapshot_package_published_source_commit"] = PUBLISHED_SOURCE_COMMIT
        payload["source_manifest"].pop("casey_snapshot_source_head", None)
        payload["source_manifest"]["casey_collection_snapshot_package"] = copy.deepcopy(source)
        payload["constructor_controls"]["merge_authority"] = None
        payload["controlled_decision"]["decision_authority"] = None
        payload["formal_acceptance_status"] = "formally_accepted"
        payload["formal_acceptance_date"] = "2026-08-01T22:55:00Z"
        payload["acceptance_date"] = "2026-08-01T22:55:00Z"
        payload["gift_acceptance_authorization_record"] = "6529NM.2026.001.GAA-01"
        payload["intake_status"] = "received_onchain"
        payload["controlled_decision"]["acceptance_date_semantics"] = "formal gift/accession authorization timestamp; not a Stream-equivalent accession completion certificate or title passage"
        payload["controlled_decision"]["outcome"] = "formally_accepted_gift_and_accession_authorization"
        payload["controlled_decision"]["rationale"] = "The adopted Art Blocks preapproval and Donation Acceptance Policy, common receipt, and user-supplied donor/authority fact support formal acceptance of this gift. Title binding, rights, condition, preservation, technical verification, and independent review remain open."
        payload["donation_rights_schedule"]["public_summary"] = "The seven identified Casey REAS Art Blocks tokens are formally accepted as a gift under 6529NM.2026.001.GAA-01 and remain received_onchain. This is not a title, rights, condition, preservation, or Stream accession-completion conclusion."
        payload["non_claims"][0] = "Formal gift acceptance is limited to 6529NM.2026.001.GAA-01 and does not substitute for a Stream-equivalent accession completion certificate or title binding."
        payload["constructor_controls"]["completion_decision"]["reason"] = "Formal gift/accession authorization is complete; the Stream completion certificate, title, rights, condition, preservation, display, and independent review gates remain open."
        payload["constructor_controls"]["signature_semantics"] = "The zero Stream signatureScheme and signatureHash are constructed-record placeholders only; they do not constitute independent approval, an executed title instrument, completed Stream accession, rights grant, or signed authority."
        payload["trait_analysis"] = trait_analysis(source)
        payload["collection_curatorial_statement"]["trait_analysis"] = trait_analysis(source)
    elif record_id in OBJECT_TO_COLLECTION:
        payload["trait_analysis"] = trait_analysis(source, descriptors[OBJECT_TO_COLLECTION[record_id]])
    payload["payload_sha256"] = casey_payload_sha256(payload)
    record["envelope"]["contentHash"]["digest"] = "0x" + keccak256(canonicalize(payload)).hex()
    write_json(path, record)


def refresh_public_pages(descriptors: dict[str, dict[str, Any]]) -> None:
    for object_id, collection in OBJECT_TO_COLLECTION.items():
        page = CASEY_DIR / "public" / f"{object_id}.md"
        text = page.read_text(encoding="utf-8")
        old = "Trait analysis is a [typed pending deliverable](https://github.com/6529-Collections/6529networkmuseum/tree/ff1c5825e3b61bfb2df0a639e057297beb946e4d/scripts/rarity); no marketplace metrics are used."
        descriptor = descriptors[collection]
        new = (
            f"A [transparent linked descriptor]({descriptor['uri']}) is available from the published source package and reproducible from its published frozen snapshot and hashes. "
            "It makes no OpenSea or other marketplace-metric, aesthetic, quality, value, or ranking claim. "
            "The formal gift/accession authorization is complete; the dossier remains `received_onchain` / `not_complete`: completion certificate, title, rights, condition, preservation, and registrar review remain pending."
        )
        if old in text:
            updated = text.replace(old, new)
        elif new in text:
            updated = text
        elif "transparent linked descriptor" in text:
            updated, replacements = re.subn(
                r"A \[transparent linked descriptor\]\([^)]*\) is available.*?(?:registrar review are incomplete|registrar review remain pending)\.",
                new,
                text,
                flags=re.DOTALL,
            )
            if replacements != 1:
                raise ValueError(f"expected existing descriptor disclosure is malformed: {page}")
        else:
            raise ValueError(f"expected trait-analysis prose is missing: {page}")
        page.write_text(updated, encoding="utf-8", newline="\n")


def refresh_control_note() -> None:
    path = ROOT / "docs" / "casey-accession-control.md"
    text = path.read_text(encoding="utf-8")
    new = (
        "Transparent linked descriptors are available from the published Casey source package and are reproducible from its published frozen snapshots, method, configuration, and content hashes. "
        "They use no OpenSea or marketplace metrics and make no aesthetic, quality, value, or ranking claim. "
        "The dossier is intentionally left with `reviewer: null`; independent review and integration—not constructor self-review—control the next decision."
    )
    new += (
        "\n\nEvidence is intentionally two-level: the artwork-source bytes are anchored by "
        "`published_source_commit` `9700e842d0c991280b476cc67849d966221a742a`; the reviewed package/toolchain release is anchored by "
        "`bf70ba3fd888d2d1b8add90fe56e913102f8aa68`, package SHA-256 `c08749355ea12c2948efdfdeb232675ab4bf693976a94c6ebb4ce24b0b5d08ab`, "
        "and release SHA-256 `d05f75c65c0af0172a0a2f2207693e4211d5c0f4f69fad8d4907ebd90e12470e`. Exact commit URLs and content hashes "
        "identify this immutable evidence basis; later current-package revisions must not silently rewrite it."
    )
    if new in text:
        updated = text
    elif "Transparent linked descriptors are available" in text:
        updated, replacements = re.subn(
            r"Transparent linked descriptors are available.*?next decision\.",
            new,
            text,
            flags=re.DOTALL,
        )
        if replacements != 1:
            raise ValueError("expected existing descriptor control note is malformed")
    else:
        updated, replacements = re.subn(
            r"Trait analysis remains a typed .*?self-review—control the next decision\\.",
            new,
            text,
            flags=re.DOTALL,
        )
        if replacements != 1:
            raise ValueError("expected obsolete trait-analysis control note is missing")
    path.write_text(updated, encoding="utf-8", newline="\n")


def main() -> None:
    source, descriptors = descriptor_package()
    for path in sorted(CASEY_DIR.rglob("*.json")):
        refresh_record(path, source, descriptors)
    refresh_public_pages(descriptors)
    refresh_control_note()


if __name__ == "__main__":
    main()
