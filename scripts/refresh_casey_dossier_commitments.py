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


ROOT = Path(__file__).resolve().parent.parent
CASEY_DIR = ROOT / "records" / "accessions" / "6529NM.2026.001"
PACKAGE_ROOT = Path("evidence/casey-reas-collection-snapshots")
PUBLISHED_SOURCE_COMMIT = "9700e842d0c991280b476cc67849d966221a742a"
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
    package_dir = ROOT / PACKAGE_ROOT
    latest = read_json(package_dir / "latest-run.json")
    package_manifest = read_json(package_dir / "package-manifest.json")
    descriptor_manifest = read_json(package_dir / "descriptor-manifest.json")
    run_manifest = read_json(package_dir / "runs" / latest["run_id"] / "run-manifest.json")

    package_manifest_path = PACKAGE_ROOT / "package-manifest.json"
    descriptor_manifest_path = PACKAGE_ROOT / "descriptor-manifest.json"
    package_manifest_sha256 = sha256(ROOT / package_manifest_path)
    descriptor_manifest_sha256 = sha256(ROOT / descriptor_manifest_path)
    if latest.get("published_source_commit") != PUBLISHED_SOURCE_COMMIT:
        raise ValueError("latest-run published source commit does not match the published Casey source")
    if latest["package_manifest"]["sha256"] != package_manifest_sha256:
        raise ValueError("latest-run package manifest fixity does not match package-manifest.json")
    if package_manifest["semantic_bindings"]["descriptor_manifest"]["sha256"] != descriptor_manifest_sha256:
        raise ValueError("package manifest descriptor fixity does not match descriptor-manifest.json")

    population = {entry["slug"]: entry["population"]["expected_token_count"] for entry in run_manifest["collections"]}
    descriptors: dict[str, dict[str, Any]] = {}
    for job in descriptor_manifest["jobs"]:
        slug = job["collection"]
        descriptor_path = PACKAGE_ROOT / job["output"]
        descriptor = read_json(ROOT / descriptor_path)
        observed_descriptor_sha256 = sha256(ROOT / descriptor_path)
        if job["descriptor_sha256"] != observed_descriptor_sha256:
            raise ValueError(f"descriptor fixity does not match descriptor manifest: {slug}")
        if descriptor["result_sha256"] != job["result_sha256"]:
            raise ValueError(f"descriptor result fixity does not match descriptor manifest: {slug}")
        descriptors[slug] = {
            "collection": slug,
            "path": descriptor_path.as_posix(),
            "uri": f"{MAIN_BLOB_URL}/{descriptor_path.as_posix()}",
            "descriptor_sha256": observed_descriptor_sha256,
            "result_sha256": job["result_sha256"],
            "source_token_count": population[slug],
            "trait_row_count": len(descriptor["result"]["per_trait"]),
        }

    inventory = package_manifest["inventory"]
    source = {
        "published_source_commit": PUBLISHED_SOURCE_COMMIT,
        "publication_semantics": "The published_source_commit is the reachable repository source anchor for this package; acquisition history remains package provenance, not an accession authority claim.",
        "path": PACKAGE_ROOT.as_posix(),
        "package_manifest": {
            "path": package_manifest_path.as_posix(),
            "uri": f"{MAIN_BLOB_URL}/{package_manifest_path.as_posix()}",
            "sha256": package_manifest_sha256,
        },
        "descriptor_manifest": {
            "path": descriptor_manifest_path.as_posix(),
            "uri": f"{MAIN_BLOB_URL}/{descriptor_manifest_path.as_posix()}",
            "sha256": descriptor_manifest_sha256,
        },
        "counts": {
            "bound_files": inventory["file_count"],
            "raw_files": inventory["raw_file_count"],
            "derived_files": inventory["derived_file_count"],
            "descriptor_results": inventory["descriptor_count"],
            "source_tokens": sum(population.values()),
            "trait_rows": sum(item["trait_row_count"] for item in descriptors.values()),
        },
        "descriptors": [descriptors[slug] for slug in ("century", "pre-process", "phototaxis", "923-empty-rooms", "ex-nihilo-cosmos")],
        "integrity_note": "Content hashes are integrity anchors; tree/main and blob/main URLs are transitional publication locators, not future merge pins.",
    }
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
            "The dossier remains `received_onchain` / `not_complete`: formal accession acceptance, title, rights, condition, preservation, and registrar review are incomplete."
        )
        if old in text:
            updated = text.replace(old, new)
        elif new in text:
            updated = text
        elif "transparent linked descriptor" in text:
            updated = text.replace("merged source package", "published source package")
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
    if new in text:
        updated = text
    elif "Transparent linked descriptors are available from the merged Casey source package" in text:
        updated = text.replace("merged Casey source package", "published Casey source package")
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
