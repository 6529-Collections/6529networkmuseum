#!/usr/bin/env python3
"""Fail closed on the published Casey descriptor-package dossier binding."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable

from canonical import canonicalize
from build_casey_diligence_manifest import ManifestError, build as build_diligence_manifest

ROOT = Path(__file__).resolve().parent.parent
CASEY_ID = "6529NM.2026.001"
CASEY_DIR = Path("records/accessions") / CASEY_ID
GIFT_AUTHORIZATION_ID = f"{CASEY_ID}.GAA-01"
VISUAL_OBSERVATION_ID = f"{CASEY_ID}.VO-01"
PACKAGE_ROOT = Path("evidence/casey-reas-collection-snapshots")
PUBLISHED_SOURCE_COMMIT = "9700e842d0c991280b476cc67849d966221a742a"
PUBLISHED_RELEASE_COMMIT = "bf70ba3fd888d2d1b8add90fe56e913102f8aa68"
PUBLISHED_RELEASE_SHA256 = "sha256:d05f75c65c0af0172a0a2f2207693e4211d5c0f4f69fad8d4907ebd90e12470e"
PACKAGE_MANIFEST_SHA256 = "sha256:c08749355ea12c2948efdfdeb232675ab4bf693976a94c6ebb4ce24b0b5d08ab"
DESCRIPTOR_MANIFEST_SHA256 = "sha256:216bebd2f26e64488e7553a781ac278c18f54b1156ccd2bee7f9f1ff97012d63"
REPOSITORY = "https://github.com/6529-Collections/6529networkmuseum"
PUBLISHED_BLOB = f"{REPOSITORY}/blob/{PUBLISHED_RELEASE_COMMIT}"
STALE_BRANCH = "codex" + "/casey-reas-accession"
RECEIPT_TRANSACTION = "0xbdde33b32d4b70335b10cbd37c0b00a027844f14c900d82aa4f75b7a7b390498"
RECEIPT_BLOCK = 25660311
RECEIPT_BLOCK_HEX = "0x1878b97"
RECEIPT_BLOCK_HASH = "0x059428dfd0b8a09d639fd37452ae9f74bc56fbadef31e19a98dc28bb7130297f"
RECEIPT_BLOCK_TIME = "2026-08-01T13:25:47Z"
RECEIPT_BLOCK_TIMESTAMP_HEX = "0x6a6df3db"
RECEIPT_FROM = "0x6daa633c23615a29471deafae351727867e7dad1"
RECEIPT_TO = "0x0000000000c2d145a2526bd8c716263bfebe1a72"
MUSEUM_CUSTODY = "0xbecfa2ba5a782d11e1a0e821e8f2e30b6684178c"
TRANSFER_TOPIC = "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"
APPROVAL_TOPIC = "0x8c5be1e5ebec7d5bd14f71427d1e84f3dd0314c0f7b2291e5b200ac8c7c3b925"
RECEIPT_RELATIVE = Path("raw/rpc") / f"eth-get-transaction-receipt-{RECEIPT_TRANSACTION}.json"
ACQUISITION_RELATIVE = Path("raw/rpc/receipt-acquisition.json")
RECEIPT_SHA256 = "4a73a7b84bb11c5a857dd93d20f8ab6027ca5472d6e2f9878fece458ad35dd21"
ACQUISITION_SHA256 = "f143ba2d832b27ef9c3a11369fd5c183283e28e778b63e78a57d89d6e1e97f45"
RECEIPT_SIZE = 6781
ACQUISITION_SIZE = 1262
CASEY_RESEARCH_COMMIT = "951f5afb95c511adaf879d017c662046ff6365b5"
CASEY_ART_RESEARCH_SHA256 = "sha256:284f25c7405059f3de499c8720229f3b94c3ed6a93cf22a167c3bdd755f5affe"
CASEY_ONCHAIN_RESEARCH_SHA256 = "sha256:0b3daa8ebf3b008c341867724a05709a1439d534837f1869e15f1351533d1db9"
GENERATOR_OBSERVATIONS_RELATIVE = Path("generator-observations.json")
GENERATOR_OBSERVATIONS_SHA256 = "sha256:a2e6a2295ffdbee3332fdeec7cd9e044d4bc5313cd63f9d6e5b67e01c3ac79da"
PRESERVATION_ACTIONS = [
    "capture and retain generator response bytes, project scripts, dependencies, and on-chain inputs",
    "complete two-environment render, interaction, timing, and reset verification",
    "retain attributed static and live documentation captures with fixity",
    "assign durable replicas and complete periodic fixity and recovery tests",
]
DILIGENCE_ROOT = Path("evidence/casey-reas-diligence")
DILIGENCE_RECORD = CASEY_DIR / "post-accession-diligence.json"
DILIGENCE_PUBLIC = CASEY_DIR / "public/custody-title-and-compliance-diligence.md"
DILIGENCE_HEAD_RPC = "https://1rpc.io/eth"
DILIGENCE_CALL_RPC = "https://ethereum-rpc.publicnode.com/"
DILIGENCE_ENS_REGISTRY = "0x00000000000c2e074ec69a0dfb2997ba6c7d2e1e"
DILIGENCE_ENS_NAMEHASH = "f90c6c0dca064bc19c04756dc088ceb60402ce8522ab4623f016d19abbb76394"
DILIGENCE_SELECTORS = {
    "resolver": "0178b8bf",
    "addr": "3b3b57de",
    "ownerOf": "6352211e",
    "getApproved": "081812fc",
}
DILIGENCE_OBJECTS = (
    ("6529NM.2026.001.01", "0xa7d8d9ef8d8ce8992df33d8b8cf4aebabd5bd270", 100000031),
    ("6529NM.2026.001.02", "0xa7d8d9ef8d8ce8992df33d8b8cf4aebabd5bd270", 100000724),
    ("6529NM.2026.001.03", "0xa7d8d9ef8d8ce8992df33d8b8cf4aebabd5bd270", 100000401),
    ("6529NM.2026.001.04", "0x99a9b7c1116f9ceeb1652de04d5969cce509b069", 383000063),
    ("6529NM.2026.001.05", "0xa7d8d9ef8d8ce8992df33d8b8cf4aebabd5bd270", 164000308),
    ("6529NM.2026.001.06", "0x145789247973c5d612bf121e9e4eef84b63eb707", 1000713),
    ("6529NM.2026.001.07", "0x0000000c687daed0fba60d1dba4e5f6149e8b894", 248),
)

OBJECT_TO_DESCRIPTOR = {
    "6529NM.2026.001.01": "century",
    "6529NM.2026.001.02": "century",
    "6529NM.2026.001.03": "century",
    "6529NM.2026.001.04": "pre-process",
    "6529NM.2026.001.05": "phototaxis",
    "6529NM.2026.001.06": "923-empty-rooms",
    "6529NM.2026.001.07": "ex-nihilo-cosmos",
}
DESCRIPTOR_ORDER = ("century", "pre-process", "phototaxis", "923-empty-rooms", "ex-nihilo-cosmos")
NON_CLAIMS = [
    "No OpenSea or other marketplace metric is used.",
    "No aesthetic, quality, value, or ranking claim is made.",
]
PUBLIC_VISUAL_AUDIT_BOUNDARY = "rights-cleared derivative or a controlled restricted copy"
PUBLICATION_SEMANTICS = (
    "The published_source_commit is the reachable repository source anchor for this package; "
    "acquisition history remains package provenance, not an accession authority claim."
)
GOVERNING_BASIS = [
    {
        "basis_type": "wave_governance_decision",
        "decision_id": "6529NM-GOV-1052156",
        "wave_serial": 1052156,
        "drop_id": "2e88273f-013c-4fdd-bea3-7de5451098e8",
        "title": "Art Blocks donation preapproval",
        "observed_wave_status": "WINNER",
        "governance_effect": "adopted",
        "source_uri": "https://6529.io/waves/5f207393-5418-4a75-8738-e40edb44a94d?divider=1052156",
    },
    {
        "basis_type": "wave_governance_decision",
        "decision_id": "6529NM-GOV-1052812",
        "wave_serial": 1052812,
        "drop_id": "86e43beb-b55d-42f0-9eea-a3c115b08abc",
        "title": "Donation Acceptance Policy",
        "observed_wave_status": "WINNER",
        "governance_effect": "adopted",
        "source_uri": "https://6529.io/waves/5f207393-5418-4a75-8738-e40edb44a94d?divider=1052812",
    },
]
GOVERNING_REFERENCES = [basis["decision_id"] for basis in GOVERNING_BASIS]
OBSERVATION_MARKERS = {
    "6529NM.2026.001.01": "dark blue-charcoal circular field",
    "6529NM.2026.001.02": "large cream ground",
    "6529NM.2026.001.03": "Grayscale describes this captured surrogate only",
    "6529NM.2026.001.04": "rows of circular masses",
    "6529NM.2026.001.05": "blue-gray ovoid of paths",
    "6529NM.2026.001.06": "finely stippled perspectival field",
    "6529NM.2026.001.07": "black field with granular white lines",
}
OBJECT_SOURCE_BEHAVIOR_MARKERS = {
    "6529NM.2026.001.01": ("`1` key", "`2` key", "controls were not activated", "cannot establish the interaction state"),
    "6529NM.2026.001.02": (),
    "6529NM.2026.001.03": (),
    "6529NM.2026.001.04": (),
    "6529NM.2026.001.05": ("1,000-iteration initial thumbnail", "`P`", "`B`", "`1` through `5`", "`L`", "controls were not activated"),
    "6529NM.2026.001.06": (),
    "6529NM.2026.001.07": ("`R`", "`G`", "`B`", "`W`", "`S`", "`P`", "spacebar", "controls were not activated"),
}
STATIC_CAPTURE_DATA = {
    "6529NM.2026.001.01": ("2026-08-01T22:48:39.777Z", 429843, "2769e41b8ea77a39b53103e31e1eaa52c04031c400062d309f7bf547792ba5da"),
    "6529NM.2026.001.02": ("2026-08-01T22:48:41.026Z", 256912, "e13ec3c6506e8f5942859af6068e2c677724aed9f1855c6eec970a64f16bc556"),
    "6529NM.2026.001.03": ("2026-08-01T22:48:42.588Z", 370117, "416bedf30696ca410ed2dc84aa8f57c6e752c21671dc42b20c32d2ad2e234e06"),
    "6529NM.2026.001.04": ("2026-08-01T22:48:50.970Z", 2100837, "8b02640589888c3fd086a8208dab79dfb083c76e7fc9060848f1fe9f0e00acf2"),
    "6529NM.2026.001.05": ("2026-08-01T22:49:05.999Z", 3905978, "8f370bc60848959def351197cce7accd0b88474e997bae6e52459ef0d30c60dd"),
    "6529NM.2026.001.06": ("2026-08-01T22:49:09.075Z", 750358, "c4e1bf468e1c632e429aa743c8b72999c4bad0e1063c9cee7b02031908972e2c"),
    "6529NM.2026.001.07": ("2026-08-01T22:49:13.379Z", 1067736, "11724ce22525a6ec161af480cf8c60a3fb1519ea2c3d3e3f805827bde43398f8"),
}
LIVE_CAPTURE_DATA = {
    "6529NM.2026.001.01": ("2026-08-01T23:34:23.137Z", 720, 720, 1440, 1440, "0087ae3a7ca50354185cca6a3f059a519ceab4bb9b439838dd80d618cef09bc6", 57237, "bf3d9a6cf3a0951c536d35ac5f7cdd8ae25531525e0c8ec028c1ef12df89929d", 57188),
    "6529NM.2026.001.02": ("2026-08-01T23:34:27.653Z", 720, 720, 1440, 1440, "53630f32f5acde1a1f33f8d3d09c4c5db9f8c91a90a14fdabd79bae7c8ed56ab", 31108, "547716a08826f6aa70c0091f8fc17aef44e0c6d2bc44d8b51ca7d2626943ecff", 30918),
    "6529NM.2026.001.03": ("2026-08-01T23:34:32.225Z", 720, 720, 1440, 1440, "21086a07ce20552727669d32ed4de18a09f40eba99fbe1b228cc9d243cdee595", 40889, "75c393b3fa43cd888b8b045c72c0d1d89b4ce595198aee8c9af6f2f7e3b95ec8", 40986),
    "6529NM.2026.001.04": ("2026-08-01T23:34:36.244Z", 1280, 720, 1920, 1080, "c3f185dbcbdb9c872fa71f0e9a4ef9ac127ef344ae60634a93dbacc59fa51afe", 10585, "bdff46e49e6f266aa7ddff12b6f2db271e937134806da0324346a17dbcc81a84", 15333),
    "6529NM.2026.001.05": ("2026-08-01T23:34:40.079Z", 1280, 720, 2560, 1440, "2a06f425bc5fe835a01e37956bf75e18cd030a38bdf08550ef5886b293502ddf", 64886, "ce0f2b0007546f1bb6a2b62b36f81a8cd990294cb424ecf647f6e40d6ff15939", 92786),
    "6529NM.2026.001.06": ("2026-08-01T23:34:44.143Z", 1280, 720, 2560, 1440, "b85c1030b8057d29b808ce6bd5209eccd9ec679883d8437d5322f9c33fe8854b", 387720, "050db3c3cd61f894e25841abc435e56193609b542627817cf67956aca03d452b", 386006),
    "6529NM.2026.001.07": ("2026-08-01T23:34:48.596Z", 1280, 720, 2560, 1440, "97d2c726792d007f1a2dd4581f231fa6ad3be11066fb50775c9cbc2299a146d5", 210478, "7c083418582dcc184b36cd112ed2d14ca69c07d7fed69796c0508caf4f828478", 209731),
}


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_bytes(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def git_blob_uri(path: Path) -> str:
    data = path.read_bytes()
    oid = hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()
    return f"https://api.github.com/repos/6529-Collections/6529networkmuseum/git/blobs/{oid}"


def generator_observations(root: Path) -> tuple[str, dict[str, dict[str, Any]], list[str]]:
    """Load the independent observation transcript without importing constructor data."""
    issues: list[str] = []
    path = root / "evidence" / "casey-reas" / GENERATOR_OBSERVATIONS_RELATIVE
    try:
        transcript = read_json(path)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        return "", {}, [f"Casey generator observation transcript cannot be decoded: {exc}"]
    if sha256(path) != GENERATOR_OBSERVATIONS_SHA256:
        issues.append("Casey generator observation transcript does not match the independently reviewed bytes")
    if (
        transcript.get("schema_version") != "6529nm.generator-observation-transcript.v1"
        or transcript.get("evidence_kind") != "independently_reviewed_observation_transcript"
        or transcript.get("reviewed_commit") != "514cb18aee37b0d04c3eeb59703b411ea34f6bf9"
        or transcript.get("raw_response_bytes_retained") is not False
        or not isinstance(transcript.get("method"), str)
        or not isinstance(transcript.get("hash_semantics"), str)
        or not isinstance(transcript.get("preservation_boundary"), str)
    ):
        issues.append("Casey generator observation transcript has an invalid review or preservation boundary")
    reviewers = transcript.get("reviewers")
    if not isinstance(reviewers, list) or len(reviewers) < 2 or len(reviewers) != len(set(reviewers)):
        issues.append("Casey generator observation transcript must retain two distinct exact-head reviewers")
    objects = transcript.get("objects") if isinstance(transcript.get("objects"), list) else []
    expected_ids = list(OBJECT_TO_DESCRIPTOR)
    if [item.get("object_id") for item in objects if isinstance(item, dict)] != expected_ids:
        issues.append("Casey generator observation transcript must retain the exact seven-object schedule")
    observations: dict[str, dict[str, Any]] = {}
    for ordinal, item in enumerate(objects, 1):
        if not isinstance(item, dict):
            continue
        suffix = f"{ordinal:02d}"
        interactions = item.get("interaction_map")
        if (
            item.get("suffix") != suffix
            or item.get("object_id") != f"{CASEY_ID}.{suffix}"
            or not isinstance(item.get("title"), str)
            or not str(item.get("generator_uri", "")).startswith("https://generator.artblocks.io/")
            or not str(item.get("response_sha256", "")).startswith("sha256:")
            or len(str(item.get("response_sha256", ""))) != 71
            or not isinstance(item.get("dependency"), str)
            or not isinstance(interactions, list)
            or not interactions
            or any(not isinstance(control, dict) or not isinstance(control.get("input"), str) or not isinstance(control.get("action"), str) for control in interactions)
        ):
            issues.append(f"Casey generator observation is structurally invalid: {CASEY_ID}.{suffix}")
        observations[suffix] = item
    rooms_statement = transcript.get("rooms_edition_statement")
    if not isinstance(rooms_statement, str) or not rooms_statement:
        issues.append("Casey generator observation transcript must retain the 923 EMPTY ROOMS edition statement")
        rooms_statement = ""
    return rooms_statement, observations, issues


class HistoricalEvidenceError(RuntimeError):
    """The immutable published Casey evidence cannot be resolved locally."""


def git_bytes(history_root: Path, arguments: list[str], label: str) -> bytes:
    completed = subprocess.run(
        ["git", *arguments],
        cwd=history_root,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        detail = completed.stderr.decode("utf-8", errors="replace").strip()
        raise HistoricalEvidenceError(f"cannot resolve {label}: {detail or 'git command failed'}")
    return completed.stdout


def historical_bytes(history_root: Path, relative_path: str) -> bytes:
    return git_bytes(history_root, ["show", f"{PUBLISHED_RELEASE_COMMIT}:{relative_path}"], f"published Casey evidence {relative_path}")


def require_full_history(history_root: Path) -> None:
    shallow = git_bytes(history_root, ["rev-parse", "--is-shallow-repository"], "repository shallow-state").decode("ascii").strip()
    if shallow != "false":
        raise HistoricalEvidenceError("repository must have full history to verify the immutable Casey publication")
    git_bytes(history_root, ["cat-file", "-e", f"{PUBLISHED_RELEASE_COMMIT}^{{commit}}"], "published Casey release commit")
    git_bytes(history_root, ["cat-file", "-e", f"{PUBLISHED_SOURCE_COMMIT}^{{commit}}"], "published Casey source commit")
    source_ancestor = subprocess.run(
        [
            "git",
            "merge-base",
            "--is-ancestor",
            PUBLISHED_SOURCE_COMMIT,
            PUBLISHED_RELEASE_COMMIT,
        ],
        cwd=history_root,
        capture_output=True,
        check=False,
    )
    if source_ancestor.returncode != 0:
        raise HistoricalEvidenceError("published Casey source commit is not an ancestor of the published release commit")
    release_ancestor = subprocess.run(
        ["git", "merge-base", "--is-ancestor", PUBLISHED_RELEASE_COMMIT, "HEAD"],
        cwd=history_root,
        capture_output=True,
        check=False,
    )
    if release_ancestor.returncode != 0:
        raise HistoricalEvidenceError("published Casey release commit is not reachable from HEAD")


def read_json_bytes(data: bytes) -> dict[str, Any]:
    return json.loads(data.decode("utf-8"))


def payload_sha256(payload: dict[str, Any]) -> str:
    body = {key: value for key, value in payload.items() if key != "payload_sha256"}
    return "sha256:" + hashlib.sha256(canonicalize(body)).hexdigest()


def nested_strings(value: Any) -> Iterable[str]:
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for item in value.values():
            yield from nested_strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from nested_strings(item)


def source_package(history_root: Path) -> tuple[dict[str, Any], dict[str, dict[str, Any]], list[str]]:
    """Resolve the immutable Casey package only from its published release commit."""

    issues: list[str] = []
    try:
        require_full_history(history_root)
        latest = read_json_bytes(historical_bytes(history_root, f"{PACKAGE_ROOT.as_posix()}/latest-run.json"))
        package_manifest_bytes = historical_bytes(history_root, f"{PACKAGE_ROOT.as_posix()}/package-manifest.json")
        descriptor_manifest_bytes = historical_bytes(history_root, f"{PACKAGE_ROOT.as_posix()}/descriptor-manifest.json")
        release_manifest_bytes = historical_bytes(history_root, "release-artifacts/latest/record-manifest.json")
        package_manifest = read_json_bytes(package_manifest_bytes)
        descriptor_manifest = read_json_bytes(descriptor_manifest_bytes)
        release_manifest = read_json_bytes(release_manifest_bytes)
    except (HistoricalEvidenceError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        return {}, {}, [f"Casey immutable publication evidence cannot be verified: {exc}"]

    package_sha = sha256_bytes(package_manifest_bytes)
    descriptor_sha = sha256_bytes(descriptor_manifest_bytes)
    release_body = {
        key: value
        for key, value in release_manifest.items()
        if key not in {"manifest_commitment", "manifest_sha256"}
    }
    release_sha = "sha256:" + hashlib.sha256(canonicalize(release_body)).hexdigest()
    if latest.get("published_source_commit") != PUBLISHED_SOURCE_COMMIT:
        issues.append("Casey historical latest-run published_source_commit does not equal the reachable published source commit")
    if latest.get("package_manifest", {}).get("sha256") != PACKAGE_MANIFEST_SHA256 or package_sha != PACKAGE_MANIFEST_SHA256:
        issues.append("Casey historical package-manifest SHA-256 does not equal the published package hash")
    if descriptor_sha != DESCRIPTOR_MANIFEST_SHA256:
        issues.append("Casey historical descriptor-manifest SHA-256 does not equal the published descriptor hash")
    if release_manifest.get("manifest_sha256") != PUBLISHED_RELEASE_SHA256 or release_sha != PUBLISHED_RELEASE_SHA256:
        issues.append("Casey historical release manifest SHA-256 does not equal the published release hash")
    semantic = package_manifest.get("semantic_bindings", {}).get("descriptor_manifest", {})
    if semantic.get("sha256") != DESCRIPTOR_MANIFEST_SHA256:
        issues.append("Casey historical package manifest does not bind the descriptor manifest hash")

    try:
        run_id = latest["run_id"]
        run_manifest = read_json_bytes(
            historical_bytes(history_root, f"{PACKAGE_ROOT.as_posix()}/runs/{run_id}/run-manifest.json")
        )
    except (KeyError, HistoricalEvidenceError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        return {}, {}, issues + [f"Casey historical run manifest cannot be verified: {exc}"]
    populations = {
        entry.get("slug"): entry.get("population", {}).get("expected_token_count")
        for entry in run_manifest.get("collections", [])
        if isinstance(entry, dict)
    }
    descriptors: dict[str, dict[str, Any]] = {}
    for job in descriptor_manifest.get("jobs", []):
        if not isinstance(job, dict):
            continue
        slug = job.get("collection")
        output = job.get("output")
        if not isinstance(slug, str) or not isinstance(output, str):
            continue
        descriptor_path = (PACKAGE_ROOT / output).as_posix()
        try:
            descriptor_bytes = historical_bytes(history_root, descriptor_path)
            descriptor = read_json_bytes(descriptor_bytes)
        except (HistoricalEvidenceError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            issues.append(f"Casey historical descriptor cannot be verified for {slug}: {exc}")
            continue
        descriptor_sha256 = sha256_bytes(descriptor_bytes)
        if job.get("descriptor_sha256") != descriptor_sha256:
            issues.append(f"Casey historical descriptor file hash does not match its descriptor manifest for {slug}")
        if descriptor.get("result_sha256") != job.get("result_sha256"):
            issues.append(f"Casey historical descriptor result hash does not match its descriptor manifest for {slug}")
        descriptors[slug] = {
            "collection": slug,
            "path": descriptor_path,
            "uri": f"{PUBLISHED_BLOB}/{descriptor_path}",
            "descriptor_sha256": descriptor_sha256,
            "result_sha256": job.get("result_sha256"),
            "source_token_count": populations.get(slug),
            "trait_row_count": len(descriptor.get("result", {}).get("per_trait", [])),
        }
    if tuple(descriptors) != DESCRIPTOR_ORDER:
        issues.append("Casey descriptor manifest must contain exactly the five expected descriptors in publication order")

    inventory = package_manifest.get("inventory", {})
    source = {
        "published_source_commit": PUBLISHED_SOURCE_COMMIT,
        "publication_semantics": PUBLICATION_SEMANTICS,
        "publication_release": {
            "published_release_commit": PUBLISHED_RELEASE_COMMIT,
            "path": "release-artifacts/latest/record-manifest.json",
            "uri": f"{PUBLISHED_BLOB}/release-artifacts/latest/record-manifest.json",
            "sha256": PUBLISHED_RELEASE_SHA256,
            "scope": "Published Casey package boundary; this historical release commitment is not this dossier's regenerated release manifest.",
        },
        "path": PACKAGE_ROOT.as_posix(),
        "package_manifest": {
            "path": (PACKAGE_ROOT / "package-manifest.json").as_posix(),
            "uri": f"{PUBLISHED_BLOB}/{(PACKAGE_ROOT / 'package-manifest.json').as_posix()}",
            "sha256": PACKAGE_MANIFEST_SHA256,
        },
        "descriptor_manifest": {
            "path": (PACKAGE_ROOT / "descriptor-manifest.json").as_posix(),
            "uri": f"{PUBLISHED_BLOB}/{(PACKAGE_ROOT / 'descriptor-manifest.json').as_posix()}",
            "sha256": DESCRIPTOR_MANIFEST_SHA256,
        },
        "counts": {
            "bound_files": inventory.get("file_count"),
            "raw_files": inventory.get("raw_file_count"),
            "derived_files": inventory.get("derived_file_count"),
            "descriptor_results": inventory.get("descriptor_count"),
            "source_tokens": sum(value.get("source_token_count") or 0 for value in descriptors.values()),
            "trait_rows": sum(value.get("trait_row_count") or 0 for value in descriptors.values()),
        },
        "descriptors": [descriptors.get(slug) for slug in DESCRIPTOR_ORDER],
        "integrity_note": "Content hashes and exact blob/bf70ba3fd888d2d1b8add90fe56e913102f8aa68 URLs are immutable evidence anchors; tree/main and blob/main are reserved for intentionally mutable living-document links.",
    }
    if source["counts"] != {
        "bound_files": 175,
        "raw_files": 79,
        "derived_files": 64,
        "descriptor_results": 5,
        "source_tokens": 3300,
        "trait_rows": 35088,
    }:
        issues.append("Casey package counts do not match the published package manifests")
    return source, descriptors, issues


def evidence_reference(relative: Path, digest: str, size: int) -> dict[str, Any]:
    return {
        "path": f"evidence/casey-reas/{relative.as_posix()}",
        "sha256": f"sha256:{digest}",
        "size": size,
        "media_type": "application/json",
        "byte_mode": "raw",
    }


def validate_evidence_manifest(root: Path) -> list[str]:
    issues: list[str] = []
    evidence_root = root / "evidence" / "casey-reas"
    manifest = read_json(evidence_root / "manifest.json")
    entries = [entry for entry in manifest.get("entries", []) if isinstance(entry, dict)]
    metadata_paths = {f"raw/metadata/{CASEY_ID}.{suffix}.json" for suffix in ("01", "02", "03", "04", "05", "06", "07")}
    expected_paths = {
        "generator-capture-status.md",
        GENERATOR_OBSERVATIONS_RELATIVE.as_posix(),
        *metadata_paths,
        RECEIPT_RELATIVE.as_posix(),
        ACQUISITION_RELATIVE.as_posix(),
        "README.md",
    }
    entry_paths = [entry.get("path") for entry in entries]
    if len(entry_paths) != len(set(entry_paths)) or set(entry_paths) != expected_paths:
        issues.append("Casey raw-evidence manifest must bind exactly the twelve accession evidence files")
    for entry in entries:
        relative = entry.get("path")
        if not isinstance(relative, str):
            issues.append(f"Casey evidence manifest entry has no path: {entry!r}")
            continue
        path = evidence_root / relative
        valid = (
            path.is_file()
            and entry.get("sha256") == hashlib.sha256(path.read_bytes()).hexdigest()
            and entry.get("size") == path.stat().st_size
            and entry.get("byte_mode") == "raw"
            and isinstance(entry.get("media_type"), str)
        )
        if not valid:
            label = "raw public metadata manifest binding failed" if entry.get("path") in metadata_paths else "evidence manifest binding failed"
            issues.append(f"Casey {label}: {entry.get('path')}")
    source_heads = manifest.get("source_heads") if isinstance(manifest.get("source_heads"), dict) else {}
    source_hashes = manifest.get("source_hashes") if isinstance(manifest.get("source_hashes"), dict) else {}
    if source_heads.get("casey_research") != CASEY_RESEARCH_COMMIT:
        issues.append("Casey evidence manifest must pin the corrected research head")
    if (
        source_hashes.get("casey_art_technical_research_sha256") != CASEY_ART_RESEARCH_SHA256
        or source_hashes.get("casey_onchain_research_sha256") != CASEY_ONCHAIN_RESEARCH_SHA256
        or sha256(root / "notes" / "research" / "casey-reas-art-technical-research.md") != CASEY_ART_RESEARCH_SHA256
        or sha256(root / "notes" / "research" / "casey-reas-onchain-evidence.md") != CASEY_ONCHAIN_RESEARCH_SHA256
    ):
        issues.append("Casey evidence manifest must bind the corrected art-technical and on-chain research bytes")
    return issues


def validate_receipt_evidence(root: Path) -> tuple[list[dict[str, Any]], list[str]]:
    """Decode the retained RPC response and return the seven ERC-721 transfers."""
    issues: list[str] = []
    evidence_root = root / "evidence" / "casey-reas"
    response_path = evidence_root / RECEIPT_RELATIVE
    acquisition_path = evidence_root / ACQUISITION_RELATIVE
    try:
        response = read_json(response_path)
        acquisition = read_json(acquisition_path)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        return [], [f"Casey raw RPC receipt evidence cannot be decoded: {exc}"]

    expected_acquisition = {
        "schema_version": "6529nm.rpc-evidence-acquisition.v1",
        "observed_at": "2026-08-02T05:33:55Z",
        "request": {
            "transport_method": "POST",
            "endpoint": "https://ethereum.publicnode.com",
            "content_type": "application/json",
            "jsonrpc": "2.0",
            "id": 1,
            "rpc_method": "eth_getTransactionReceipt",
            "params": [RECEIPT_TRANSACTION],
        },
        "response": {
            "path": RECEIPT_RELATIVE.as_posix(),
            "media_type": "application/json",
            "byte_mode": "raw",
            "sha256": RECEIPT_SHA256,
            "size": RECEIPT_SIZE,
            "http_status": 200,
        },
        "acquisition": {
            "client": "Windows PowerShell Invoke-WebRequest",
            "response_body_mode": "OutFile raw response body",
            "tls_endpoint_observed": "ethereum.publicnode.com",
        },
        "limitations": [
            "This artifact preserves one provider response observed at the stated time; it is not a quorum of independent RPC providers.",
            "The response authenticates on-chain receipt fields through Ethereum block identity and receipt/log structure, not the off-chain identity of wallet controllers.",
        ],
    }
    if acquisition != expected_acquisition:
        issues.append("Casey raw RPC receipt acquisition metadata is invalid")

    result = response.get("result") if isinstance(response, dict) else None
    expected_receipt = {
        "blockHash": RECEIPT_BLOCK_HASH,
        "blockNumber": RECEIPT_BLOCK_HEX,
        "from": RECEIPT_FROM,
        "status": "0x1",
        "to": RECEIPT_TO,
        "transactionHash": RECEIPT_TRANSACTION,
    }
    if (
        not isinstance(result, dict)
        or response.get("jsonrpc") != "2.0"
        or response.get("id") != 1
        or any(result.get(key) != value for key, value in expected_receipt.items())
    ):
        issues.append("Casey raw RPC receipt header is invalid")
        return [], issues
    logs = result.get("logs")
    if not isinstance(logs, list) or len(logs) != 9 or not all(isinstance(log, dict) for log in logs):
        issues.append("Casey raw RPC receipt must retain all nine transaction logs")
        return [], issues

    transfers: list[dict[str, Any]] = []
    approval_count = 0
    malformed = False
    for log in logs:
        topics = log.get("topics")
        if (
            not isinstance(topics, list)
            or not topics
            or log.get("blockHash") != RECEIPT_BLOCK_HASH
            or log.get("blockNumber") != RECEIPT_BLOCK_HEX
            or log.get("blockTimestamp") != RECEIPT_BLOCK_TIMESTAMP_HEX
            or log.get("transactionHash") != RECEIPT_TRANSACTION
            or log.get("removed") is not False
            or log.get("data") != "0x"
        ):
            malformed = True
            continue
        if topics[0] == TRANSFER_TOPIC and len(topics) == 4:
            try:
                transfers.append(
                    {
                        "contract": str(log["address"]).lower(),
                        "from": "0x" + str(topics[1])[-40:].lower(),
                        "to": "0x" + str(topics[2])[-40:].lower(),
                        "token_id": str(int(str(topics[3]), 16)),
                        "log": int(str(log["logIndex"]), 16),
                    }
                )
            except (KeyError, TypeError, ValueError):
                malformed = True
        elif topics[0] == APPROVAL_TOPIC and len(topics) == 4:
            approval_count += 1
        else:
            malformed = True
    if malformed or len(transfers) != 7 or approval_count != 2:
        issues.append("Casey raw RPC receipt log structure is invalid")
    return sorted(transfers, key=lambda item: item["log"]), issues


def _rpc_request(method: str, request_id: str, params: list[Any]) -> bytes:
    return json.dumps(
        {"jsonrpc": "2.0", "id": request_id, "method": method, "params": params},
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def _calldata(selector: str, value: int | str) -> str:
    encoded = f"{value:064x}" if isinstance(value, int) else value.removeprefix("0x").lower().rjust(64, "0")
    return "0x" + selector + encoded


def _abi_address(value: Any) -> str | None:
    if not isinstance(value, str) or len(value) != 66 or not value.startswith("0x"):
        return None
    if any(character not in "0123456789abcdefABCDEF" for character in value[2:]):
        return None
    if value[2:26] != "0" * 24:
        return None
    return "0x" + value[-40:].lower()


def _validate_diligence_rpc_evidence(package_root: Path, custody: dict[str, Any]) -> list[str]:
    """Reconstruct every request and decode every retained custody response."""
    issues: list[str] = []
    package_root = package_root.resolve()
    block = custody.get("block") if isinstance(custody.get("block"), dict) else {}
    block_hash = block.get("hash")
    block_number = block.get("numeric_tag")
    state_selector = {"blockHash": block_hash, "requireCanonical": True}
    expected_ids = {
        "chain-id",
        "finalized-block",
        "finalized-block-after",
        "ens-resolver",
        "ens-address",
        *(f"owner:{object_id}" for object_id, _contract, _token_id in DILIGENCE_OBJECTS),
        *(f"approval:{object_id}" for object_id, _contract, _token_id in DILIGENCE_OBJECTS),
    }
    response_refs = custody.get("responses") if isinstance(custody.get("responses"), list) else []
    rows: dict[str, dict[str, Any]] = {}
    response_digests: dict[str, str] = {}
    response_sizes: dict[str, int] = {}
    try:
        if len(response_refs) != 19:
            raise ValueError("response reference count")
        for reference in response_refs:
            if not isinstance(reference, dict):
                raise ValueError("response reference shape")
            relative = Path(str(reference.get("path", "")))
            candidate = (package_root / relative).resolve()
            if package_root not in candidate.parents or relative.parts[:2] != ("raw", "rpc"):
                raise ValueError("response path escapes raw/rpc")
            payload = candidate.read_bytes()
            digest = hashlib.sha256(payload).hexdigest()
            if (
                reference.get("sha256") != f"sha256:{digest}"
                or reference.get("size") != len(payload)
                or candidate.name != f"sha256-{digest}.json"
                or reference.get("media_type") != "application/json"
                or reference.get("byte_mode") != "raw"
            ):
                raise ValueError("response reference fixity")
            row = json.loads(payload.decode("utf-8"))
            request_id = row.get("id") if isinstance(row, dict) else None
            if (
                not isinstance(request_id, str)
                or request_id in rows
                or row.get("jsonrpc") != "2.0"
                or "error" in row
            ):
                raise ValueError("response JSON-RPC envelope")
            rows[request_id] = row
            response_digests[request_id] = digest
            response_sizes[request_id] = len(payload)
        if set(rows) != expected_ids:
            raise ValueError("response identifier set")
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, TypeError, ValueError) as error:
        return [f"Casey diligence raw RPC responses are incomplete or malformed: {error}"]

    resolver_word = rows["ens-resolver"].get("result")
    resolver = _abi_address(resolver_word)
    if resolver is None:
        return ["Casey diligence raw RPC resolver response is not one ABI address word"]
    expected_requests: dict[str, tuple[str, list[Any]]] = {
        "chain-id": ("eth_chainId", []),
        "finalized-block": ("eth_getBlockByNumber", ["finalized", False]),
        "finalized-block-after": ("eth_getBlockByNumber", ["finalized", False]),
        "ens-resolver": (
            "eth_call",
            [{"to": DILIGENCE_ENS_REGISTRY, "data": _calldata(DILIGENCE_SELECTORS["resolver"], DILIGENCE_ENS_NAMEHASH)}, state_selector],
        ),
        "ens-address": (
            "eth_call",
            [{"to": resolver, "data": _calldata(DILIGENCE_SELECTORS["addr"], DILIGENCE_ENS_NAMEHASH)}, state_selector],
        ),
    }
    for object_id, contract, token_id in DILIGENCE_OBJECTS:
        expected_requests[f"owner:{object_id}"] = (
            "eth_call",
            [{"to": contract, "data": _calldata(DILIGENCE_SELECTORS["ownerOf"], token_id)}, state_selector],
        )
        expected_requests[f"approval:{object_id}"] = (
            "eth_call",
            [{"to": contract, "data": _calldata(DILIGENCE_SELECTORS["getApproved"], token_id)}, state_selector],
        )

    request_refs = custody.get("requests") if isinstance(custody.get("requests"), dict) else {}
    safe_observations = custody.get("safe_fetch_observations") if isinstance(custody.get("safe_fetch_observations"), dict) else {}
    request_key_for_id = {
        "chain-id": "chain_id",
        "finalized-block": "finalized_block",
        "finalized-block-after": "finalized_block_after",
        "ens-resolver": "ens_resolver",
        "ens-address": "ens_address",
        **{request_id: request_id for request_id in expected_ids if request_id.startswith(("owner:", "approval:"))},
    }
    if set(request_refs) != set(request_key_for_id.values()) or set(safe_observations) != set(request_key_for_id.values()):
        issues.append("Casey diligence request and safe-fetch observation sets must match all 19 RPC calls")
    for request_id, (method, params) in expected_requests.items():
        payload = _rpc_request(method, request_id, params)
        reference = request_refs.get(request_key_for_id[request_id], {})
        observation = safe_observations.get(request_key_for_id[request_id], {})
        expected_url = DILIGENCE_HEAD_RPC if request_id in {"chain-id", "finalized-block", "finalized-block-after"} else DILIGENCE_CALL_RPC
        if (
            reference != {
                "sha256": f"sha256:{hashlib.sha256(payload).hexdigest()}",
                "size": len(payload),
                "canonicalization": "sorted-key compact JSON",
            }
            or not isinstance(observation, dict)
            or observation.get("canonical_url") != expected_url
            or observation.get("status") != 200
            or observation.get("byte_sha256") != response_digests[request_id]
            or observation.get("byte_length") != response_sizes[request_id]
        ):
            issues.append(f"Casey diligence RPC request/transport binding is invalid: {request_id}")

    first_block = rows["finalized-block"].get("result")
    last_block = rows["finalized-block-after"].get("result")
    try:
        first_timestamp = int(first_block["timestamp"], 16) if isinstance(first_block, dict) else -1
        last_timestamp = int(last_block["timestamp"], 16) if isinstance(last_block, dict) else -2
        retained_number = int(block_number, 16)
        retained_timestamp = datetime.fromtimestamp(first_timestamp, UTC).isoformat(timespec="seconds").replace("+00:00", "Z")
    except (KeyError, OSError, OverflowError, TypeError, ValueError):
        issues.append("Casey diligence raw block timestamps and numeric tag must be valid hexadecimal values")
        first_timestamp = -1
        last_timestamp = -2
        retained_number = -1
        retained_timestamp = ""
    if (
        rows["chain-id"].get("result") != "0x1"
        or not isinstance(first_block, dict)
        or not isinstance(last_block, dict)
        or first_block.get("number") != block_number
        or last_block.get("number") != block_number
        or not isinstance(block_hash, str)
        or not isinstance(first_block.get("hash"), str)
        or not isinstance(last_block.get("hash"), str)
        or first_block["hash"].lower() != block_hash
        or last_block["hash"].lower() != block_hash
        or first_timestamp != last_timestamp
        or block.get("number") != retained_number
        or block.get("timestamp") != retained_timestamp
    ):
        issues.append("Casey diligence raw block responses must bind one stable finalized block")
    if _abi_address(rows["ens-address"].get("result")) != MUSEUM_CUSTODY:
        issues.append("Casey diligence raw ENS responses must resolve the Museum custody address")
    for object_id, contract, token_id in DILIGENCE_OBJECTS:
        owner = _abi_address(rows[f"owner:{object_id}"].get("result"))
        approval = _abi_address(rows[f"approval:{object_id}"].get("result"))
        summaries = custody.get("objects") if isinstance(custody.get("objects"), list) else []
        summary = next(
            (item for item in summaries if isinstance(item, dict) and item.get("object_id") == object_id),
            {},
        )
        if (
            owner != MUSEUM_CUSTODY
            or approval != "0x" + "0" * 40
            or summary.get("contract") != contract
            or summary.get("token_id") != str(token_id)
            or summary.get("caip19") != f"eip155:1/erc721:{contract}/{token_id}"
            or summary.get("owner") != owner
            or summary.get("token_level_approved_operator") != approval
        ):
            issues.append(f"Casey diligence raw owner/approval response does not match its exact object: {object_id}")
    method = custody.get("method") if isinstance(custody.get("method"), dict) else {}
    if (
        block.get("state_selector") != state_selector
        or method.get("rpc_endpoints") != {
            "chain_and_finalized_block": DILIGENCE_HEAD_RPC.rstrip("/"),
            "eip1898_block_hash_contract_reads": DILIGENCE_CALL_RPC.rstrip("/"),
        }
        or "EIP-1898" not in method.get("same_block_rule", "")
        or "requireCanonical true" not in method.get("same_block_rule", "")
    ):
        issues.append("Casey diligence custody method must bind every contract read to the exact finalized block hash")
    return issues


def validate_post_accession_diligence(root: Path) -> list[str]:
    """Validate the reviewed title, custody, control, and OFAC evidence enrichment."""
    issues: list[str] = []
    package_root = root / DILIGENCE_ROOT
    manifest_path = package_root / "manifest.json"
    custody_path = package_root / "custody-audit-2026-08-02.json"
    ofac_path = package_root / "ofac-address-screening-2026-08-02.json"
    record_path = root / DILIGENCE_RECORD
    public_path = root / DILIGENCE_PUBLIC
    try:
        actual_manifest = read_json(manifest_path)
        expected_manifest = build_diligence_manifest(package_root)
        custody = read_json(custody_path)
        ofac = read_json(ofac_path)
        record = read_json(record_path)
        public_text = public_path.read_text(encoding="utf-8")
    except (ManifestError, OSError, UnicodeDecodeError, json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
        return [f"Casey post-accession diligence package cannot be decoded: {error}"]

    if actual_manifest != expected_manifest:
        issues.append("Casey post-accession diligence evidence manifest must bind every package file exactly")
    issues.extend(_validate_diligence_rpc_evidence(package_root, custody))
    manifest_sha = sha256(manifest_path)
    custody_sha = sha256(custody_path)
    ofac_sha = sha256(ofac_path)
    control = record.get("record_control") if isinstance(record.get("record_control"), dict) else {}
    constructor = control.get("constructor") if isinstance(control.get("constructor"), dict) else {}
    review = control.get("review") if isinstance(control.get("review"), dict) else {}
    if (
        record.get("record_id") != f"{CASEY_ID}.DILIGENCE-01"
        or record.get("record_type") != "ACCESSION_DILIGENCE"
        or control.get("record_status") != "reviewed"
        or review.get("outcome") != "approved"
        or review.get("actor_id") == constructor.get("actor_id")
        or not review.get("actor_id")
    ):
        issues.append("Casey post-accession diligence record must have completed independent review")

    package = record.get("package") if isinstance(record.get("package"), dict) else {}
    if (
        package.get("manifest_sha256") != manifest_sha
        or package.get("file_count") != 22
        or package.get("raw_rpc_response_count") != 19
        or package.get("raw_ofac_api_bytes_retained") is not False
    ):
        issues.append("Casey diligence record must bind the complete evidence package and its API-capture boundary")

    result = custody.get("result") if isinstance(custody.get("result"), dict) else {}
    objects = custody.get("objects") if isinstance(custody.get("objects"), list) else []
    block = custody.get("block") if isinstance(custody.get("block"), dict) else {}
    expected_object_ids = list(OBJECT_TO_DESCRIPTOR)
    if (
        custody.get("audit_id") != f"{CASEY_ID}.CUSTODY-AUDIT-20260802"
        or [item.get("object_id") for item in objects if isinstance(item, dict)] != expected_object_ids
        or any(
            not isinstance(item, dict)
            or item.get("owner") != MUSEUM_CUSTODY
            or item.get("owner_matches_museum") is not True
            or item.get("token_level_approved_operator") != "0x" + "0" * 40
            or item.get("token_level_approval_is_zero") is not True
            for item in objects
        )
        or result != {
            "all_owner_of_results_match_museum": True,
            "all_token_level_approvals_are_zero": True,
            "ens_resolves_to_museum_at_same_block": True,
            "finalized_boundary_stable_before_and_after": True,
            "object_count": 7,
        }
        or block.get("number") != 25667060
        or block.get("hash") != "0x01dc7575349d0893386928c218b64a11b8d71e42015b1995bafa7d65e05084e3"
        or custody.get("custodian", {}).get("address") != MUSEUM_CUSTODY
        or custody.get("custodian", {}).get("ens") != "networkmuseum.6529.eth"
    ):
        issues.append("Casey custody audit must prove the seven owner, ENS, zero token-approval, and stable-finality observations")

    screened = ofac.get("screened_addresses") if isinstance(ofac.get("screened_addresses"), list) else []
    expected_screened = [
        ("0x6daa633c23615a29471deafae351727867e7dad1", "donor_and_transfer_source"),
        ("0xbecfa2ba5a782d11e1a0e821e8f2e30b6684178c", "museum_custody_address"),
        ("0xa7d8d9ef8d8ce8992df33d8b8cf4aebabd5bd270", "token_contract"),
        ("0x99a9b7c1116f9ceeb1652de04d5969cce509b069", "token_contract"),
        ("0x145789247973c5d612bf121e9e4eef84b63eb707", "token_contract"),
        ("0x0000000c687daed0fba60d1dba4e5f6149e8b894", "token_contract"),
        ("0x0000000000c2d145a2526bd8c716263bfebe1a72", "common_transfer_transaction_target"),
        ("0x457ee5f723c7606c12a7264b52e285906f91eea6", "project_artist_address_returned_by_contracts"),
    ]
    observed_screened = [
        (item.get("address"), item.get("role"))
        for item in screened
        if isinstance(item, dict)
    ]
    positive_control = ofac.get("positive_control") if isinstance(ofac.get("positive_control"), dict) else {}
    if (
        ofac.get("screening_id") != f"{CASEY_ID}.OFAC-20260802"
        or positive_control.get("control_passed") is not True
        or positive_control.get("address") != "0x67d40ee1a85bf4a4bb7ffae16de985e8427b6b45"
        or positive_control.get("result_count") != 1
        or positive_control.get("entity") != "CHATEX"
        or positive_control.get("program") != "CYBER2"
        or positive_control.get("list") != "SDN"
        or positive_control.get("detail_uri") != "https://sanctionssearch.ofac.treas.gov/Details.aspx?id=33854"
        or observed_screened != expected_screened
        or any(not isinstance(item, dict) or item.get("result") != "no_exact_match" for item in screened)
        or ofac.get("result") != {
            "screened_address_count": 8,
            "exact_match_count": 0,
            "positive_control_passed": True,
            "outcome": "no_exact_ofac_digital_currency_address_match_observed",
        }
        or "raw transfer-encoded API response bytes were not retained" not in " ".join(ofac.get("limitations", []))
    ):
        issues.append("Casey OFAC evidence must retain the positive control, eight exact no-match observations, and raw-byte limitation")

    title = record.get("title_and_authority") if isinstance(record.get("title_and_authority"), dict) else {}
    custody_binding = record.get("custody_verification") if isinstance(record.get("custody_verification"), dict) else {}
    sanctions_binding = record.get("sanctions_screening") if isinstance(record.get("sanctions_screening"), dict) else {}
    conclusion = record.get("conclusion") if isinstance(record.get("conclusion"), dict) else {}
    title_path = root / CASEY_DIR / "public/title-rights-and-accession-review.md"
    if (
        title.get("determination") != "confirmed"
        or title.get("instrument_id") != f"{CASEY_ID}.TITLE-01"
        or title.get("instrument_sha256") != sha256(title_path)
        or "does not create an uncompleted title gate" not in title.get("restricted_annex_interpretation", "")
        or custody_binding.get("audit_sha256") != custody_sha
        or sanctions_binding.get("screening_sha256") != ofac_sha
        or conclusion.get("outcome") != "completed_pass_with_documented_limits"
        or conclusion.get("accession_effect") != "confirmed_no_status_change"
        or conclusion.get("accession_status_after_review") != "accessioned"
        or conclusion.get("completion_blockers") != []
    ):
        issues.append("Casey diligence determination must confirm title, bind custody and OFAC evidence, and preserve accession status")

    public_markers = (
        "requires a title downgrade, custody hold, deaccession review, or new display restriction",
        "or create an uncompleted title gate",
        "every `ownerOf` call returned that Museum address",
        "every token-specific `getApproved` call returned the zero address",
        "no exact OFAC digital-currency-address match was observed",
        "does not identify the civil person behind a pseudonymous address",
        manifest_sha.removeprefix("sha256:"),
    )
    if any(marker.lower() not in public_text.lower() for marker in public_markers):
        issues.append("Casey public diligence review must state the final title, custody, sanctions, and evidence-boundary findings")
    return issues


def validate(root: Path = ROOT, history_root: Path | None = None) -> list[str]:
    """Validate the reviewed, accessioned Casey REAS collection package."""
    source, descriptors, issues = source_package(history_root or root)
    receipt_transfers, receipt_issues = validate_receipt_evidence(root)
    issues.extend(receipt_issues)
    issues.extend(validate_evidence_manifest(root))
    issues.extend(validate_post_accession_diligence(root))
    rooms_edition_statement, generator_evidence, generator_issues = generator_observations(root)
    issues.extend(generator_issues)

    descriptor_ledger = read_json(root / PACKAGE_ROOT / "pending-descriptors.json")
    descriptor_review = descriptor_ledger.get("review") if isinstance(descriptor_ledger.get("review"), dict) else {}
    descriptor_jobs = descriptor_ledger.get("jobs") if isinstance(descriptor_ledger.get("jobs"), list) else []
    if (
        descriptor_ledger.get("status") != "complete_reviewed"
        or descriptor_review.get("status") != "approved"
        or descriptor_review.get("reviewed_commit") != "514cb18aee37b0d04c3eeb59703b411ea34f6bf9"
        or not isinstance(descriptor_review.get("reviewer_ids"), list)
        or len(descriptor_review.get("reviewer_ids", [])) < 2
        or len(descriptor_jobs) != 5
        or any(
            not isinstance(job, dict)
            or job.get("status") != "complete_reviewed"
            or job.get("review") != {"status": "approved", "review_ref": "descriptor-package-review-2026-08-02"}
            for job in descriptor_jobs
        )
    ):
        issues.append("Casey descriptor review ledger must record the completed independent package review")

    records: dict[str, dict[str, Any]] = {}
    for path in sorted((root / CASEY_DIR).rglob("*.json")):
        record = read_json(path)
        payload = record.get("payload")
        if not isinstance(payload, dict):
            continue
        record_id = payload.get("record_id")
        if isinstance(record_id, str):
            records[record_id] = record
        if payload.get("payload_sha256") != payload_sha256(payload):
            issues.append(f"Casey payload commitment is invalid: {path.relative_to(root)}")
        reviewer = payload.get("reviewer")
        if payload.get("record_status") != "reviewed" or payload.get("review_status") != "reviewed" or not isinstance(reviewer, dict):
            issues.append(f"Casey accession record must be substantively reviewed: {path.relative_to(root)}")
        elif reviewer == payload.get("constructor") or reviewer.get("id") == payload.get("constructor", {}).get("id"):
            issues.append(f"Casey constructor/reviewer separation is invalid: {path.relative_to(root)}")
        signature_scheme = record.get("envelope", {}).get("signatureScheme")
        signature_digest = record.get("envelope", {}).get("signatureHash", {}).get("digest")
        if signature_scheme != "0x" + "0" * 64 or signature_digest != "0x" + "0" * 64:
            issues.append(f"Casey repository record must remain unsigned until on-chain execution: {path.relative_to(root)}")
        if any(STALE_BRANCH in text for text in nested_strings(record)):
            issues.append(f"Casey record has a mutable construction-branch URL: {path.relative_to(root)}")
        if any("9f38bd4ba5f779540eabf2dfce019cc1382561e2" in text for text in nested_strings(payload)):
            issues.append(f"Casey record retains the superseded research head: {path.relative_to(root)}")
        if any(
            marker in text
            for text in nested_strings(payload)
            for marker in (
                "https://github.com/6529-Collections/6529networkmuseum/blob/main/",
                "https://github.com/6529-Collections/6529networkmuseum/tree/main/",
            )
        ):
            issues.append(f"Casey payload evidence URL must be commit-pinned: {path.relative_to(root)}")

    lot_record = records.get(CASEY_ID)
    accession_record = records.get("6529NM-ACC-2026-001")
    authorization_record = records.get(GIFT_AUTHORIZATION_ID)
    visual_record = records.get(VISUAL_OBSERVATION_ID)
    if lot_record is None:
        return issues + ["Casey accession lot record is missing"]
    if accession_record is None:
        return issues + ["Casey accession certificate record is missing"]
    if authorization_record is None:
        return issues + ["Casey gift authorization record is missing"]
    if visual_record is None:
        return issues + ["Casey visual observation record is missing"]

    lot = lot_record["payload"]
    if (
        lot.get("accession_status") != "complete"
        or lot.get("intake_status") != "accessioned"
        or lot.get("formal_acceptance_status") != "formally_accepted"
        or lot.get("gift_acceptance_authorization_record") != GIFT_AUTHORIZATION_ID
        or lot.get("controlled_decision", {}).get("current_state") != "accessioned"
        or lot.get("controlled_decision", {}).get("completion_status") != "complete"
        or lot.get("controlled_decision", {}).get("accession_status") != "complete"
        or lot.get("controlled_decision", {}).get("outcome") != "approved_for_permanent_collection"
        or lot.get("remaining_gates") != []
    ):
        issues.append("Casey lot must record completed permanent-collection accession with no unresolved gate")
    actions = lot.get("ongoing_stewardship_actions")
    if not isinstance(actions, list) or len(actions) < 4 or any(not isinstance(item, dict) or item.get("status") != "active" for item in actions):
        issues.append("Casey lot must state concrete active preservation, testing, replica, custody, and provenance duties")
    if lot.get("references") != [GIFT_AUTHORIZATION_ID, "6529NM-ACC-2026-001", VISUAL_OBSERVATION_ID]:
        issues.append("Casey lot must link the gift authorization, accession certificate, and visual observation")
    if lot.get("governing_references") != GOVERNING_REFERENCES:
        issues.append("Casey lot governing references must identify the adopted Art Blocks and Donation Acceptance decisions")
    if lot.get("source_manifest", {}).get("casey_collection_snapshot_package") != source:
        issues.append("Casey lot source package binding does not match the published source package")
    evidence_manifest_sha256 = sha256(root / "evidence" / "casey-reas" / "manifest.json")
    if (
        lot.get("source_manifest", {}).get("evidence_manifest_sha256") != evidence_manifest_sha256
        or lot.get("preservation_manifest", {}).get("manifest_sha256") != evidence_manifest_sha256
        or lot.get("preservation_manifest", {}).get("fixity_sha256") != evidence_manifest_sha256
        or lot.get("preservation_manifest", {}).get("manifest_uri") != git_blob_uri(root / "evidence" / "casey-reas" / "manifest.json")
    ):
        issues.append("Casey lot must bind the current preservation evidence manifest")

    identity_list = lot.get("object_identities")
    identity_list = identity_list if isinstance(identity_list, list) and all(isinstance(item, dict) for item in identity_list) else []
    expected_object_ids = list(OBJECT_TO_DESCRIPTOR)
    identities = {item.get("object_id"): item for item in identity_list}
    identity_keys = [(str(item.get("contract", "")).lower(), item.get("token_id"), item.get("custody_receipt_log")) for item in identity_list]
    if (
        [item.get("object_id") for item in identity_list] != expected_object_ids
        or len(identities) != len(expected_object_ids)
        or len(identity_keys) != len(set(identity_keys))
        or any(item.get("caip19") != f"eip155:1/erc721:{str(item.get('contract', '')).lower()}/{item.get('token_id')}" for item in identity_list)
    ):
        issues.append("Casey accession identity schedule must retain seven exact unique chain identities")

    public_inventory = lot.get("public_inventory") if isinstance(lot.get("public_inventory"), list) else []
    if (
        [item.get("inventory_number") for item in public_inventory if isinstance(item, dict)] != expected_object_ids
        or any(item.get("status") != "accessioned" for item in public_inventory if isinstance(item, dict))
    ):
        issues.append("Casey public inventory must place all seven exact objects in accessioned state")

    rights_schedule = lot.get("donation_rights_schedule") if isinstance(lot.get("donation_rights_schedule"), dict) else {}
    rights_objects = rights_schedule.get("objects") if isinstance(rights_schedule.get("objects"), list) else []
    rights_matrix = rights_schedule.get("rights_matrix") if isinstance(rights_schedule.get("rights_matrix"), list) else []
    instrument = rights_schedule.get("restricted_instrument_ref") if isinstance(rights_schedule.get("restricted_instrument_ref"), dict) else {}
    if (
        [item.get("object_id") for item in rights_objects if isinstance(item, dict)] != expected_object_ids
        or any(item.get("donation_status") != "accessioned" or item.get("rights_status") != "reviewed_with_conditions" or not item.get("rights_record") for item in rights_objects if isinstance(item, dict))
        or [item.get("object_id") for item in rights_matrix if isinstance(item, dict)] != expected_object_ids
        or any(item.get("grant_status") != "granted_with_conditions" or item.get("license") != "CC BY-NC 4.0" or not item.get("rights_record") for item in rights_matrix if isinstance(item, dict))
        or instrument.get("status") != "executed_institutional_title_declaration"
        or instrument.get("content_hash") != sha256(root / CASEY_DIR / "public" / "title-rights-and-accession-review.md")
    ):
        issues.append("Casey lot-level donation, title, and rights schedule must state the completed accession and reviewed CC BY-NC 4.0 determinations")

    preservation_manifest = lot.get("preservation_manifest") if isinstance(lot.get("preservation_manifest"), dict) else {}
    preservation_actions = preservation_manifest.get("active_stewardship_actions")
    if "pending" in preservation_manifest or preservation_actions != PRESERVATION_ACTIONS:
        issues.append("Casey preservation manifest must state concrete active stewardship actions rather than an intake-stage pending list")

    expected_transfers = sorted(
        [
            {
                "contract": str(identity.get("contract", "")).lower(),
                "from": RECEIPT_FROM,
                "to": MUSEUM_CUSTODY,
                "token_id": identity.get("token_id"),
                "log": identity.get("custody_receipt_log"),
            }
            for identity in identity_list
        ],
        key=lambda item: item["log"] if isinstance(item["log"], int) else -1,
    )
    if receipt_transfers != expected_transfers:
        issues.append("Casey raw RPC receipt transfer schedule must match the seven accession identities")
    schedule = lot.get("provenance_schedule") if isinstance(lot.get("provenance_schedule"), dict) else {}
    common_receipt = schedule.get("common_receipt") if isinstance(schedule.get("common_receipt"), dict) else {}
    if (
        common_receipt.get("transaction_hash") != RECEIPT_TRANSACTION
        or common_receipt.get("block_hash") != RECEIPT_BLOCK_HASH
        or common_receipt.get("block_number") != RECEIPT_BLOCK
        or common_receipt.get("receipt_status") != "0x1"
        or common_receipt.get("transfer_count") != 7
        or common_receipt.get("museum_custody_address") != MUSEUM_CUSTODY
        or common_receipt.get("verification") != "direct_rpc_verified"
    ):
        issues.append("Casey provenance common receipt must remain joined to the retained direct RPC evidence")

    accession = accession_record["payload"]
    if (
        accession.get("accession_number") != CASEY_ID
        or accession.get("object_ids") != expected_object_ids
        or accession.get("acquisition_method") != "donation"
        or accession.get("acceptance_date") != "2026-08-01T22:55:00Z"
        or accession.get("review_outcomes", {}).get("curatorial") != "approved_for_permanent_collection"
        or accession.get("review_outcomes", {}).get("condition_and_technical") != "pass_with_conditions"
        or accession.get("review_outcomes", {}).get("preservation") != "in_progress_nonblocking"
    ):
        issues.append("Casey accession certificate must bind the exact lot, seven objects, and completed review outcomes")
    title_instrument_sha256 = sha256(root / CASEY_DIR / "public" / "title-rights-and-accession-review.md")
    bindings = accession.get("title_bindings") if isinstance(accession.get("title_bindings"), list) else []
    if (
        [item.get("object_id") for item in bindings if isinstance(item, dict)] != expected_object_ids
        or any(item.get("status") != "executed" or item.get("transfer_transaction") != RECEIPT_TRANSACTION or item.get("instrument_sha256") != title_instrument_sha256 for item in bindings if isinstance(item, dict))
    ):
        issues.append("Casey accession certificate must execute one exact title binding per object")
    events = accession.get("events") if isinstance(accession.get("events"), list) else []
    if [item.get("event_type") for item in events if isinstance(item, dict)] != ["receipt", "acceptance", "acquisition", "title_passage", "custody_receipt", "accession"]:
        issues.append("Casey accession certificate must preserve the Stream-compatible event order")
    elif events[3].get("instrument", {}).get("sha256") != title_instrument_sha256:
        issues.append("Casey accession title-passage event must bind the reviewed title instrument bytes")
    accession_lot_path = root / CASEY_DIR / "accession-statement.json"
    expected_lot_ref = {
        "label": "Reviewed accession lot",
        "uri": git_blob_uri(accession_lot_path),
        "observed_at": "2026-08-02T06:30:00Z",
        "evidence_class": "C",
        "sha256": sha256(accession_lot_path),
        "notes": "Immutable Git blob URI and raw-file SHA-256 identify the exact reviewed accession-lot bytes used by this certificate.",
    }
    acquisition_refs = events[2].get("evidence_refs", []) if len(events) == 6 and isinstance(events[2], dict) else []
    if acquisition_refs != [expected_lot_ref]:
        issues.append("Casey accession certificate must immutably bind the exact reviewed accession-lot bytes")
    custody_paths = events[4].get("custody_paths", []) if len(events) == 6 and isinstance(events[4], dict) else []
    if [item.get("object_id") for item in custody_paths if isinstance(item, dict)] != expected_object_ids or any(item.get("kind") != "onchain_token" for item in custody_paths if isinstance(item, dict)):
        issues.append("Casey accession certificate must bind one on-chain custody path per object")
    custody_event = events[4] if len(events) == 6 and isinstance(events[4], dict) else {}
    if (
        custody_event.get("event_name") != "institutional_custody_registration"
        or custody_event.get("occurred_at") != "2026-08-02T06:30:00Z"
        or custody_event.get("source_occurred_at") != RECEIPT_BLOCK_TIME
        or "does not redate or replay" not in custody_event.get("event_semantics", "")
        or events[0].get("occurred_at") != RECEIPT_BLOCK_TIME
        or any(events[index].get("occurred_at") != "2026-08-01T22:55:00Z" for index in (1, 2, 3))
        or events[5].get("occurred_at") != "2026-08-02T06:30:00Z"
    ):
        issues.append("Casey accession chronology must distinguish on-chain receipt, co-temporal acceptance/acquisition/title, and later custody registration")

    authorization = authorization_record["payload"]
    expected_boundary = {
        "current_state": "accessioned",
        "accession_status": "complete",
        "external_work_accession_certificate": "executed",
        "title_binding": "executed",
        "rights": "reviewed_with_conditions",
        "condition": "reviewed_pass_with_conditions",
        "preservation": "in_progress",
        "independent_review": "reviewed",
    }
    expected_authorized_assets = [
        {
            "object_id": identity.get("object_id"),
            "title": identity.get("title"),
            "caip19": identity.get("caip19"),
            "contract": identity.get("contract"),
            "token_id": identity.get("token_id"),
            "custody_receipt_log": identity.get("custody_receipt_log"),
        }
        for identity in identity_list
    ]
    expected_authorization_receipt = {
        "transaction_hash": RECEIPT_TRANSACTION,
        "block_number": RECEIPT_BLOCK,
        "block_time": RECEIPT_BLOCK_TIME,
        "from": RECEIPT_FROM,
        "to": MUSEUM_CUSTODY,
        "custody_ens": "networkmuseum.6529.eth",
        "transfer_count": len(expected_object_ids),
        "receipt_status": "0x1",
    }
    if (
        authorization.get("authorization_status") != "formally_accepted"
        or authorization.get("donor_public_credit") != "punk6529"
        or authorization.get("assets") != expected_authorized_assets
        or authorization.get("custody_receipt") != expected_authorization_receipt
        or authorization.get("completion_boundary") != expected_boundary
        or authorization.get("completion_blockers") != []
        or authorization.get("custody_receipt", {}).get("receipt_status") != "0x1"
        or authorization.get("references") != [CASEY_ID, "6529NM-ACC-2026-001"]
        or authorization.get("institutional_decision_authority", {}).get("documentation_qa_status") != "reviewed"
        or "direct Museum-authorized collection authority" not in authorization.get("institutional_decision_authority", {}).get("publication_semantics", "")
        or "do not replace or exercise" not in authorization.get("institutional_decision_authority", {}).get("publication_semantics", "")
        or "full" not in authorization.get("donor_authority_declaration", {}).get("statement", "").lower()
    ):
        issues.append("Casey gift authorization must record the full gift and its completed accession resolution")
    governing_basis = authorization.get("governing_basis")
    expected_basis_identity = [
        (
            basis["basis_type"],
            basis["decision_id"],
            basis["wave_serial"],
            basis["drop_id"],
            basis["source_uri"],
        )
        for basis in GOVERNING_BASIS
    ]
    actual_basis_identity = [
        (
            basis.get("basis_type"),
            basis.get("decision_id"),
            basis.get("wave_serial"),
            basis.get("drop_id"),
            basis.get("source_uri"),
        )
        for basis in governing_basis
        if isinstance(basis, dict)
    ] if isinstance(governing_basis, list) else []
    if actual_basis_identity != expected_basis_identity:
        issues.append("Casey governing basis must bind exactly decisions 1052156 and 1052812 once each")
    for basis in governing_basis if isinstance(governing_basis, list) else []:
        if not isinstance(basis, dict):
            issues.append("Casey governing basis must contain decision records")
            continue
        if (
            basis.get("observed_at") != "2026-08-01T15:01:05Z"
            or basis.get("effect_basis") != "reviewed_governance_record"
            or basis.get("governance_record_ref") != "6529NM-GOV-REGISTER"
            or basis.get("live_api_field") != "drop_type"
            or basis.get("live_api_status") != "WINNER"
            or basis.get("live_api_observed_at") != "2026-08-01T15:01:05Z"
            or "rating totals and rater counts" not in basis.get("governance_effect_basis", "")
        ):
            issues.append("Casey governing basis must state when and from which reviewed register its effect was observed")

    rights_classes = {"reproduction", "publication", "exhibition", "print", "derivative_use", "ai_training", "preservation", "migration_emulation", "accessibility"}
    condition_keys = {"token", "metadata", "script", "dependencies", "rendering", "behavior", "documentation"}
    for object_id, descriptor_slug in OBJECT_TO_DESCRIPTOR.items():
        object_record = records.get(object_id)
        rights_record = records.get(f"{CASEY_ID}.RIGHTS.{object_id.rsplit('.', 1)[1]}")
        condition_record = records.get(f"{CASEY_ID}.COND.{object_id.rsplit('.', 1)[1]}")
        if object_record is None or rights_record is None or condition_record is None:
            issues.append(f"Casey reviewed object/rights/condition record set is incomplete: {object_id}")
            continue
        payload = object_record["payload"]
        identity = identities.get(object_id, {})
        chain = payload.get("chain_identity", {})
        if payload.get("title") != identity.get("title") or chain.get("caip19") != identity.get("caip19") or chain.get("custody_receipt_transaction") != RECEIPT_TRANSACTION:
            issues.append(f"Casey object chain identity is invalid: {object_id}")
        state_history = payload.get("state_history")
        suffix = object_id.rsplit(".", 1)[1]
        expected_state_history = [
            {
                "state": state,
                "observed_at": "2026-08-01T22:55:00Z",
                "evidence_refs": [GIFT_AUTHORIZATION_ID],
            }
            for state in ("offered", "authorized", "acquired", "received_onchain")
        ] + [
            {
                "state": "accessioned",
                "observed_at": "2026-08-02T06:30:00Z",
                "evidence_refs": ["6529NM-ACC-2026-001", GIFT_AUTHORIZATION_ID, f"{CASEY_ID}.RIGHTS.{suffix}", f"{CASEY_ID}.COND.{suffix}"],
            }
        ]
        if payload.get("current_state") != "accessioned" or state_history != expected_state_history:
            issues.append(f"Casey object must end in accessioned state: {object_id}")
        title_binding = payload.get("title_binding", {})
        if title_binding.get("status") != "executed" or title_binding.get("transfer_transaction") != RECEIPT_TRANSACTION or title_binding.get("object_id") != object_id or title_binding.get("instrument_sha256") != title_instrument_sha256:
            issues.append(f"Casey object must retain an executed transaction-bound title declaration: {object_id}")
        grants = payload.get("rights", {})
        if set(grants) != rights_classes or any(item.get("grant_status") != "granted_with_conditions" or "CC BY-NC 4.0" not in item.get("basis", "") for item in grants.values()):
            issues.append(f"Casey object must state the complete conditional CC BY-NC 4.0 rights matrix: {object_id}")
        condition = payload.get("condition", {})
        if any(condition.get(key) in {None, "red", "not_assessed"} for key in condition_keys) or condition.get("token") != "green" or condition.get("metadata") != "green":
            issues.append(f"Casey object must state a complete non-red accession condition finding: {object_id}")
        if (
            payload.get("display", {}).get("status") != "ready_with_conditions"
            or payload.get("preservation", {}).get("status") != "in_progress"
            or payload.get("preservation", {}).get("package_uri") != git_blob_uri(root / "evidence" / "casey-reas" / "manifest.json")
        ):
            issues.append(f"Casey object must separate conditional display readiness from active preservation: {object_id}")
        expected_generator = generator_evidence.get(suffix, {})
        generator = payload.get("generator_snapshot") if isinstance(payload.get("generator_snapshot"), dict) else {}
        generator_transcript_path = root / "evidence" / "casey-reas" / GENERATOR_OBSERVATIONS_RELATIVE
        expected_generator_transcript = {
            "uri": git_blob_uri(generator_transcript_path),
            "sha256": GENERATOR_OBSERVATIONS_SHA256,
            "reviewed_commit": "514cb18aee37b0d04c3eeb59703b411ea34f6bf9",
            "raw_response_bytes_retained": False,
        }
        if (
            generator.get("sha256") != expected_generator.get("response_sha256")
            or generator.get("dependency_observed") != expected_generator.get("dependency")
            or generator.get("uri") != expected_generator.get("generator_uri")
            or generator.get("interaction_map") != expected_generator.get("interaction_map")
            or generator.get("interaction_review_status") != "source_reviewed_not_exhaustively_exercised"
            or generator.get("observation_transcript") != expected_generator_transcript
            or generator.get("automatic_behavior") != expected_generator.get("automatic_behavior")
            or generator.get("documentation_discrepancies") != expected_generator.get("documentation_discrepancies")
        ):
            issues.append(f"Casey generator response, dependency, and complete interaction map are invalid: {object_id}")
        expected_trait = {
            "status": "transparent_linked_descriptors_available",
            "method": "Museum published NextGen-compatible method over the frozen source package; linked descriptors are available and reproducible.",
            "marketplace_metrics": "not_used",
            "non_claims": NON_CLAIMS,
            "source_package": source,
            "descriptor": descriptors.get(descriptor_slug),
        }
        if payload.get("trait_analysis") != expected_trait:
            issues.append(f"Casey object descriptor mapping or no-marketplace claims are invalid: {object_id}")
        rights_payload = rights_record["payload"]
        rights_title_refs = [
            item
            for item in rights_payload.get("evidence_refs", [])
            if isinstance(item, dict) and item.get("label") == "Reviewed title and rights determination"
        ]
        if rights_payload.get("grants") != grants or "copyright is not transferred" not in rights_payload.get("rights_holder_reference", "").lower() or len(rights_title_refs) != 1 or rights_title_refs[0].get("sha256") != title_instrument_sha256:
            issues.append(f"Casey rights statement must match the object matrix and copyright boundary: {object_id}")
        condition_payload = condition_record["payload"]
        if condition_payload.get("outcome", "").split(":", 1)[0] != "pass_with_conditions" or any(value in {"red", "not_assessed"} for value in condition_payload.get("assessments", {}).values()):
            issues.append(f"Casey condition report must reach a complete pass-with-conditions outcome: {object_id}")
        condition_visual_refs = [
            item
            for item in condition_payload.get("evidence_refs", [])
            if isinstance(item, dict) and item.get("label") == "Controlled visual observation"
        ]
        visual_sha256 = sha256(root / CASEY_DIR / "visual-observation-record.json")
        if (
            len(condition_visual_refs) != 1
            or condition_visual_refs[0].get("sha256") != visual_sha256
            or condition_visual_refs[0].get("uri") != git_blob_uri(root / CASEY_DIR / "visual-observation-record.json")
        ):
            issues.append(f"Casey condition report must bind the controlled visual observation bytes: {object_id}")
        condition_generator_refs = [
            item
            for item in condition_payload.get("evidence_refs", [])
            if isinstance(item, dict) and item.get("label") == "Independent generator observation transcript"
        ]
        if (
            len(condition_generator_refs) != 1
            or condition_generator_refs[0].get("uri") != expected_generator_transcript["uri"]
            or condition_generator_refs[0].get("sha256") != GENERATOR_OBSERVATIONS_SHA256
        ):
            issues.append(f"Casey condition report must bind the independent generator observation transcript: {object_id}")

    visual = visual_record["payload"]
    observed_objects = visual.get("objects") if isinstance(visual.get("objects"), list) else []
    if [item.get("object_id") for item in observed_objects if isinstance(item, dict)] != expected_object_ids:
        issues.append("Casey visual observation must bind the exact seven-object schedule")
    for item in observed_objects:
        for capture_name in ("static_capture", "live_capture"):
            retention = item.get(capture_name, {}).get("retention", {})
            if (
                retention.get("bytes_retained_in_public_repository") is not False
                or retention.get("status") != "not_retained_rights_cleared_preservation_action_open"
                or "CC BY-NC 4.0" not in retention.get("statement", "")
            ):
                issues.append(f"Casey visual observation must record rights-cleared future capture without fabricating original bytes: {item.get('object_id')}")

    required_public = {
        "accession-certificate.md": ["approved and accessioned", "owns the seven tokens", "ready with conditions"],
        "title-rights-and-accession-review.md": ["entire ownership interest", "copyright", "CC BY-NC 4.0", "AI training"],
        "technical-and-condition-review.md": ["passes technical and condition review with conditions", "No red condition", "Active preservation actions"],
        "curatorial-accession-review.md": ["approved for the permanent collection", "Processing", "Object-level findings"],
        "gift-acceptance-authorization.md": ["full gift", "accession completed", "no accession blocker remains"],
    }
    for name, markers in required_public.items():
        text = (root / CASEY_DIR / "public" / name).read_text(encoding="utf-8")
        if any(marker.lower() not in text.lower() for marker in markers):
            issues.append(f"Casey finished public review is missing a required substantive conclusion: {name}")
    forbidden_final_phrases = (
        "registrar review remain pending",
        "independent review remains pending",
        "rights review pending",
        "completion certificate pending",
        "not_complete",
        "received_onchain` /",
    )
    for page in sorted((root / CASEY_DIR / "public").glob("*.md")):
        text = page.read_text(encoding="utf-8")
        if any(phrase.lower() in text.lower() for phrase in forbidden_final_phrases):
            issues.append(f"Casey public document retains an intake-stage placeholder: {page.name}")
    for object_id in expected_object_ids:
        page = (root / CASEY_DIR / "public" / f"{object_id}.md").read_text(encoding="utf-8")
        for marker in ("**Status:** `accessioned`", "The work is `accessioned`", "no OpenSea or marketplace rarity", "Museum interpretation [E]"):
            if marker.lower() not in page.lower():
                issues.append(f"Casey public object page lacks a finished state or interpretive boundary: {object_id}")
                break

    artist_profile = (root / CASEY_DIR / "public" / "casey-reas-artist-practice.md").read_text(encoding="utf-8")
    collection_essay = (root / CASEY_DIR / "public" / "casey-reas-collection-essay.md").read_text(encoding="utf-8")
    artist_boundary = (
        "the token exceeds the function of an external certificate while remaining one layer of the artwork",
        "a static platform image documents a token-specific state while the live work continues through execution",
    )
    if any(marker.lower() not in artist_profile.lower() for marker in artist_boundary):
        issues.append("Casey artist profile must retain the token/software interpretation boundary")
    collection_boundary = (
        "no single layer is the whole work",
        "a *CENTURY* still can be closely read as a composition and still remain a state of moving software",
    )
    if any(marker.lower() not in collection_essay.lower() for marker in collection_boundary):
        issues.append("Casey collection essay must retain the executable-image interpretation boundary")
    rooms = records.get("6529NM.2026.001.06", {}).get("payload", {})
    expected_rooms_structure = {
        "token_count": 924,
        "invocation_range": "0–923",
        "invocation_zero_code": "999999",
        "sequenced_combination_invocations": "1–923",
        "reviewed_generator_table_entries": 924,
        "object_invocation": 713,
        "object_code": "555536",
        "interpretive_boundary": "The evidence resolves the count structure but does not establish an artistic interpretation of invocation zero.",
    }
    if (
        rooms.get("project", {}).get("edition_statement") != rooms_edition_statement
        or rooms.get("project", {}).get("combination_structure") != expected_rooms_structure
    ):
        issues.append("Casey 923 EMPTY ROOMS record must retain the 923-combination / 924-token distinction")

    return issues


def main() -> None:
    issues = validate()
    if issues:
        for issue in issues:
            print(f"error: {issue}", file=sys.stderr)
        raise SystemExit(1)
    print("Casey dossier validation passed: published source binding, descriptors, claims, states, URLs, and raw evidence are valid.")


if __name__ == "__main__":
    main()
