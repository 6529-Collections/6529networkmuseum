#!/usr/bin/env python3
"""Fail closed on the published Casey descriptor-package dossier binding."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Iterable

from canonical import canonicalize
from finalize_casey_accession import GENERATOR_EVIDENCE, ROOMS_EDITION_STATEMENT

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
PUBLIC_NON_CLAIM = "no OpenSea or other marketplace-metric, aesthetic, quality, value, or ranking claim"
PUBLIC_STATE = "received_onchain` / `not_complete"
PUBLIC_DESCRIPTOR = "transparent linked descriptor"
PUBLIC_ACCEPTANCE = "The Gift Acceptance and Accession Authorization was issued and formally accepts the gift; it does not complete accession."
PUBLIC_COMPLETION_BOUNDARY = "Title, rights, condition, preservation, and registrar review remain pending."
PUBLIC_VISUAL_AUDIT_BOUNDARY = "rights-cleared derivative or a controlled restricted copy"
OBJECT_MEDIUM = (
    "On-chain generative software associated with an ERC-721 token on Ethereum; Art Blocks records a token hash. "
    "Determinism of live behavior has not yet been independently verified."
)
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
        *metadata_paths,
        RECEIPT_RELATIVE.as_posix(),
        ACQUISITION_RELATIVE.as_posix(),
        "README.md",
    }
    entry_paths = [entry.get("path") for entry in entries]
    if len(entry_paths) != len(set(entry_paths)) or set(entry_paths) != expected_paths:
        issues.append("Casey raw-evidence manifest must bind exactly the eleven accession evidence files")
    for entry in entries:
        path = evidence_root / str(entry["path"])
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


def validate_intake_stage_legacy(root: Path = ROOT, history_root: Path | None = None) -> list[str]:
    source, descriptors, issues = source_package(history_root or root)
    receipt_transfers, receipt_issues = validate_receipt_evidence(root)
    issues.extend(receipt_issues)
    issues.extend(validate_evidence_manifest(root))
    records: dict[str, dict[str, Any]] = {}
    for path in sorted((root / CASEY_DIR).rglob("*.json")):
        record = read_json(path)
        payload = record.get("payload", {})
        record_id = payload.get("record_id")
        if isinstance(record_id, str):
            records[record_id] = record
        if payload.get("payload_sha256") != payload_sha256(payload):
            issues.append(f"Casey payload commitment is invalid: {path.relative_to(root)}")
        if payload.get("record_status") != "constructed" or payload.get("review_status") != "pending_independent_review" or payload.get("reviewer") is not None:
            issues.append(f"Casey record must retain constructed documentation QA, unsigned placeholders, and pending independent review: {path.relative_to(root)}")
        signature_scheme = record.get("envelope", {}).get("signatureScheme")
        signature_digest = record.get("envelope", {}).get("signatureHash", {}).get("digest")
        if signature_scheme != "0x" + "0" * 64 or signature_digest != "0x" + "0" * 64:
            issues.append(f"Casey record must retain unsigned Stream placeholders: {path.relative_to(root)}")
        if any(STALE_BRANCH in text for text in nested_strings(record)):
            issues.append(f"Casey record has a mutable construction-branch URL: {path.relative_to(root)}")

    lot_record = records.get(CASEY_ID)
    if lot_record is None:
        return issues + ["Casey accession lot record is missing"]
    lot = lot_record["payload"]
    source_manifest = lot.get("source_manifest", {})
    if source_manifest.get("casey_snapshot_source_head") is not None:
        issues.append("Casey dossier must not retain the obsolete snapshot-source head")
    if source_manifest.get("casey_collection_snapshot_package") != source:
        issues.append("Casey lot source package binding does not match the published source package")
    if lot.get("source", {}).get("casey_collection_snapshot_package_published_source_commit") != PUBLISHED_SOURCE_COMMIT:
        issues.append("Casey lot source must name the published source commit")
    if (
        lot.get("accession_status") != "not_complete"
        or lot.get("formal_acceptance_status") != "formally_accepted"
        or lot.get("gift_acceptance_authorization_record") != GIFT_AUTHORIZATION_ID
        or lot.get("formal_acceptance_date") != "2026-08-01T22:55:00Z"
    ):
        issues.append("Casey lot must retain formal gift acceptance while remaining not_complete")
    if lot.get("controlled_decision", {}).get("current_state") != "received_onchain":
        issues.append("Casey lot must remain received_onchain")
    if lot.get("controlled_decision", {}).get("outcome") != "formally_accepted_gift_and_accession_authorization":
        issues.append("Casey lot must name the limited formal gift/accession authorization outcome")
    if lot.get("review_status") != "pending_independent_review" or lot.get("reviewer") is not None:
        issues.append("Casey lot must retain incomplete independent registrar review without authority")
    if lot.get("constructor_controls", {}).get("reviewer") is not None or lot.get("constructor_controls", {}).get("merge_authority") is not None or lot.get("controlled_decision", {}).get("decision_authority") is not None:
        issues.append("Casey lot reviewer and decision-authority fields must remain null without evidence")
    if lot.get("governing_references") != GOVERNING_REFERENCES:
        issues.append("Casey lot governing references must identify the adopted Art Blocks and Donation Acceptance decisions")
    if lot.get("references") != [GIFT_AUTHORIZATION_ID, VISUAL_OBSERVATION_ID]:
        issues.append("Casey lot generic reference graph must link the gift authorization and visual observation record")
    evidence_manifest_sha256 = sha256(root / "evidence" / "casey-reas" / "manifest.json")
    if (
        lot.get("source_manifest", {}).get("evidence_manifest_sha256") != evidence_manifest_sha256
        or lot.get("preservation_manifest", {}).get("manifest_sha256") != evidence_manifest_sha256
        or lot.get("preservation_manifest", {}).get("fixity_sha256") != evidence_manifest_sha256
    ):
        issues.append("Casey accession lot does not bind the current preservation evidence manifest")

    identity_list = lot.get("object_identities")
    identity_list = identity_list if isinstance(identity_list, list) and all(isinstance(item, dict) for item in identity_list) else []
    expected_object_ids = list(OBJECT_TO_DESCRIPTOR)
    identities = {item.get("object_id"): item for item in identity_list}
    identity_keys = [
        (str(item.get("contract", "")).lower(), item.get("token_id"), item.get("custody_receipt_log"))
        for item in identity_list
    ]
    if (
        [item.get("object_id") for item in identity_list] != expected_object_ids
        or len(identities) != len(expected_object_ids)
        or len(identity_keys) != len(set(identity_keys))
        or any(
            item.get("caip19") != f"eip155:1/erc721:{str(item.get('contract', '')).lower()}/{item.get('token_id')}"
            for item in identity_list
        )
    ):
        issues.append("Casey accession identity schedule must contain seven unique, internally consistent chain identities")

    expected_receipt_evidence = {
        "acquisition": evidence_reference(ACQUISITION_RELATIVE, ACQUISITION_SHA256, ACQUISITION_SIZE),
        "response": evidence_reference(RECEIPT_RELATIVE, RECEIPT_SHA256, RECEIPT_SIZE),
    }
    schedule = lot.get("provenance_schedule")
    schedule = schedule if isinstance(schedule, dict) else {}
    common_receipt = schedule.get("common_receipt")
    common_receipt = common_receipt if isinstance(common_receipt, dict) else {}
    receipt_summary = lot.get("receipt_summary")
    receipt_summary = receipt_summary if isinstance(receipt_summary, dict) else {}
    expected_log_indices = {
        object_id: identities.get(object_id, {}).get("custody_receipt_log")
        for object_id in expected_object_ids
    }
    expected_common_receipt = {
        "block_hash": RECEIPT_BLOCK_HASH,
        "block_number": RECEIPT_BLOCK,
        "block_time": RECEIPT_BLOCK_TIME,
        "evidence": expected_receipt_evidence,
        "evidence_grade": "A",
        "log_indices": expected_log_indices,
        "museum_custody_address": MUSEUM_CUSTODY,
        "purpose": "on-chain receipt into the ENS-resolved Museum custody address; legal title and rights are separate fields",
        "receipt_status": "0x1",
        "transaction_from": RECEIPT_FROM,
        "transaction_hash": RECEIPT_TRANSACTION,
        "transaction_to": RECEIPT_TO,
        "transfer_count": 7,
        "verification": "direct_rpc_verified",
    }
    if common_receipt != expected_common_receipt:
        issues.append("Casey common receipt does not match the retained raw RPC receipt and accession identities")
    if {key: value for key, value in receipt_summary.items() if key != "ens_semantics"} != expected_common_receipt:
        issues.append("Casey receipt summary must equal the provenance common-receipt projection")
    expected_rpc_refs = {
        f"evidence/casey-reas/{RECEIPT_RELATIVE.as_posix()}",
        f"evidence/casey-reas/{ACQUISITION_RELATIVE.as_posix()}",
    }
    if not expected_rpc_refs.issubset(set(schedule.get("evidence_refs", []))):
        issues.append("Casey provenance evidence_refs must bind the retained raw RPC response and acquisition metadata")

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
        issues.append("Casey raw RPC receipt transfer schedule does not match the seven accession identities")

    provenance_objects = schedule.get("objects")
    provenance_objects = provenance_objects if isinstance(provenance_objects, list) else []
    if [item.get("object_id") for item in provenance_objects if isinstance(item, dict)] != expected_object_ids:
        issues.append("Casey provenance object schedule must identify the exact seven objects in accession order")
    for item in provenance_objects:
        if not isinstance(item, dict):
            continue
        object_id = item.get("object_id")
        identity = identities.get(object_id, {})
        expected_event = {
            "block": RECEIPT_BLOCK,
            "block_hash": RECEIPT_BLOCK_HASH,
            "direct_rpc_verified": True,
            "from": RECEIPT_FROM,
            "kind": "museum_receipt",
            "log": identity.get("custody_receipt_log"),
            "receipt_status": "0x1",
            "time": RECEIPT_BLOCK_TIME,
            "to": MUSEUM_CUSTODY,
            "tx": RECEIPT_TRANSACTION,
            "verification": "direct_rpc_verified",
        }
        events = item.get("events") if isinstance(item.get("events"), list) else []
        museum_events = [event for event in events if isinstance(event, dict) and event.get("kind") == "museum_receipt"]
        if item.get("chain_object") != identity.get("caip19") or museum_events != [expected_event]:
            issues.append(f"Casey provenance schedule chain identity/receipt binding is invalid: {object_id}")

    expected_inventory = [
        {
            "artist": "Casey REAS",
            "caip19": identities.get(object_id, {}).get("caip19"),
            "inventory_number": object_id,
            "public_page": f"public/{object_id}.md",
            "status": "received_onchain",
            "title": identities.get(object_id, {}).get("title"),
        }
        for object_id in expected_object_ids
    ]
    if lot.get("public_inventory") != expected_inventory:
        issues.append("Casey public inventory must project the exact seven accession identities")

    authorization_record = records.get(GIFT_AUTHORIZATION_ID)
    if authorization_record is None:
        issues.append("Casey formal gift acceptance authorization record is missing")
    else:
        authorization = authorization_record["payload"]
        expected_assets = [
            {
                "object_id": identity["object_id"],
                "title": identity["title"],
                "caip19": identity["caip19"],
                "contract": identity["contract"],
                "token_id": identity["token_id"],
                "custody_receipt_log": identity["custody_receipt_log"],
            }
            for identity in lot.get("object_identities", [])
        ]
        expected_receipt = {
            "transaction_hash": "0xbdde33b32d4b70335b10cbd37c0b00a027844f14c900d82aa4f75b7a7b390498",
            "block_number": 25660311,
            "block_time": "2026-08-01T13:25:47Z",
            "from": "0x6daa633c23615a29471deafae351727867e7dad1",
            "to": "0xbecfa2ba5a782d11e1a0e821e8f2e30b6684178c",
            "custody_ens": "networkmuseum.6529.eth",
            "transfer_count": 7,
            "receipt_status": "success",
        }
        expected_boundary = {
            "current_state": "received_onchain",
            "accession_status": "not_complete",
            "stream_accession_completion_certificate": "pending",
            "title_binding": "pending",
            "rights": "pending",
            "condition": "pending",
            "preservation": "pending",
            "independent_review": "pending",
        }
        if (
            authorization.get("authorization_status") != "formally_accepted"
            or authorization.get("outcome") != "formally_accepted_gift_and_accession_authorization"
            or authorization.get("formal_acceptance_date") != "2026-08-01T22:55:00Z"
            or authorization.get("donor_public_credit") != "punk6529"
            or authorization.get("governing_basis") != GOVERNING_BASIS
            or authorization.get("assets") != expected_assets
            or authorization.get("custody_receipt") != expected_receipt
            or authorization.get("completion_boundary") != expected_boundary
        ):
            issues.append("Casey formal gift acceptance authorization does not bind the adopted basis, seven assets, receipt, and pending completion boundary")
        declaration = authorization.get("donor_authority_declaration", {})
        if declaration.get("source_type") != "user_supplied_donor_and_authority_fact" or "No cryptographic signature" not in declaration.get("authentication", ""):
            issues.append("Casey donor/authority declaration must identify its user-supplied authentication limitation")
        decision_authority = authorization.get("institutional_decision_authority", {})
        if (
            decision_authority.get("decision_status") != "formally_accepted"
            or decision_authority.get("authority_basis") != "user_authorized_institutional_decision"
            or decision_authority.get("effective_at") != "2026-08-01T22:55:00Z"
            or decision_authority.get("documentation_qa_status") != "pending_independent_review"
            or "does not create" not in decision_authority.get("publication_semantics", "")
        ):
            issues.append("Casey gift authorization must separate effective institutional acceptance from pending documentation QA")
        if authorization.get("reviewer") is not None or "signed deed" not in " ".join(authorization.get("non_claims", [])):
            issues.append("Casey gift authorization may not masquerade as a signed deed or reviewed title authority")
        if authorization.get("references") != [CASEY_ID]:
            issues.append("Casey gift authorization generic reference graph must link its accession lot")

    visual_record = records.get(VISUAL_OBSERVATION_ID)
    if visual_record is None:
        issues.append("Casey controlled visual observation record is missing")
    else:
        visual = visual_record["payload"]
        if (
            visual.get("accession_lot_id") != CASEY_ID
            or visual.get("observation_kind") != "static_and_live_visual_observation"
            or visual.get("observed_at") != "2026-08-01T23:34:48.596Z"
            or visual.get("capture_scope", {}).get("static_capture_order") != expected_object_ids
            or visual.get("references") != [CASEY_ID, *expected_object_ids]
        ):
            issues.append("Casey visual observation record must bind the exact lot and seven objects in capture order")
        limitation_text = " ".join(visual.get("limitations", [])).lower()
        for required in (
            "not retained in the public repository pending rights and preservation review",
            "lastwritetimeutc",
            "observation-completion proxy",
            "not a server date header",
            "commanded 1500-millisecond minimum wait",
            "not an exact elapsed-time measurement",
            "not constitute a condition report",
            "not a full generator capture",
            "determinism proof",
            "does not establish preservation completion",
            "rights-cleared derivative or a controlled restricted copy",
            "browser version and user-agent were not captured",
        ):
            if required not in limitation_text:
                issues.append(f"Casey visual observation record lacks required timing/retention limitation: {required}")
        observed_objects = visual.get("objects", [])
        if not isinstance(observed_objects, list) or [item.get("object_id") for item in observed_objects if isinstance(item, dict)] != expected_object_ids:
            issues.append("Casey visual observation record object schedule is not exact")
            observed_objects = []
        evidence_manifest = read_json(root / "evidence" / "casey-reas" / "manifest.json")
        manifest_entries = {
            entry.get("path"): entry
            for entry in evidence_manifest.get("entries", [])
            if isinstance(entry, dict)
        }
        for item in observed_objects:
            object_id = item.get("object_id")
            if object_id not in STATIC_CAPTURE_DATA or object_id not in LIVE_CAPTURE_DATA:
                issues.append(f"Casey visual observation has an unexpected object: {object_id}")
                continue
            suffix = str(object_id).rsplit(".", 1)[-1]
            raw_relative = f"raw/metadata/{CASEY_ID}.{suffix}.json"
            raw_path = root / "evidence" / "casey-reas" / raw_relative
            raw_metadata = read_json(raw_path)
            manifest_entry = manifest_entries.get(raw_relative, {})
            expected_raw = {
                "path": f"evidence/casey-reas/{raw_relative}",
                "sha256": f"sha256:{manifest_entry.get('sha256')}",
                "byte_size": manifest_entry.get("size"),
                "image_field": "image",
                "image_url": raw_metadata.get("image"),
                "generator_field": "generator_url",
                "generator_url": raw_metadata.get("generator_url"),
            }
            static_time, static_size, static_sha = STATIC_CAPTURE_DATA[object_id]
            static = item.get("static_capture", {})
            live = item.get("live_capture", {})
            completed_at, canvas_width, canvas_height, backing_width, backing_height, first_sha, first_size, second_sha, second_size = LIVE_CAPTURE_DATA[object_id]
            expected_frames = [
                {"frame_index": 1, "captured_at": None, "screenshot_scope": "full_viewport", "screenshot_sha256": f"sha256:{first_sha}", "byte_size": first_size},
                {"frame_index": 2, "captured_at": None, "screenshot_scope": "full_viewport", "screenshot_sha256": f"sha256:{second_sha}", "byte_size": second_size},
            ]
            if item.get("caip19") != identities.get(object_id, {}).get("caip19") or item.get("raw_metadata_source") != expected_raw:
                issues.append(f"Casey visual observation raw metadata URL/hash binding is invalid: {object_id}")
            if (
                static.get("local_response_file_written_at") != static_time
                or static.get("timing_semantics") != "local_file_last_write_utc_observation_completion_proxy"
                or static.get("source_url") != raw_metadata.get("image")
                or static.get("response_sha256") != f"sha256:{static_sha}"
                or static.get("byte_size") != static_size
                or static.get("capture_method") != "exact_http_response_bytes"
                or static.get("media_type") != "image/png"
            ):
                issues.append(f"Casey visual observation static response binding is invalid: {object_id}")
            if (
                live.get("observation_completed_at") != completed_at
                or live.get("source_url") != raw_metadata.get("generator_url")
                or live.get("viewport_css_pixels") != {"width": 1280, "height": 720}
                or live.get("canvas_css_pixels") != {"width": canvas_width, "height": canvas_height}
                or live.get("canvas_backing_store_pixels") != {"width": backing_width, "height": backing_height}
                or live.get("minimum_wait_between_frames_ms") != 1500
                or live.get("changed") is not True
                or live.get("frames") != expected_frames
                or live.get("render_environment") != {"browser_version": None, "user_agent": None, "completeness": "partial", "missing_fields": ["browser_version", "user_agent"]}
            ):
                issues.append(f"Casey visual observation live screenshot binding is invalid: {object_id}")
            for capture in (static, live):
                retention = capture.get("retention", {})
                if (
                    retention.get("bytes_retained_in_public_repository") is not False
                    or retention.get("status") != "not_retained_pending_rights_and_preservation_review"
                    or "not retained in the public repository pending rights and preservation review" not in retention.get("statement", "")
                ):
                    issues.append(f"Casey visual observation must retain the public-byte non-retention boundary: {object_id}")

    expected_trait = {
        "status": "transparent_linked_descriptors_available",
        "method": "Museum published NextGen-compatible method over the frozen source package; linked descriptors are available and reproducible.",
        "marketplace_metrics": "not_used",
        "non_claims": NON_CLAIMS,
        "source_package": source,
    }
    if lot.get("trait_analysis") != expected_trait:
        issues.append("Casey lot trait analysis must provide transparent linked descriptors without prohibited claims")
    if lot.get("collection_curatorial_statement", {}).get("trait_analysis") != expected_trait:
        issues.append("Casey curatorial statement must provide transparent linked descriptors without prohibited claims")

    for object_id, descriptor_slug in OBJECT_TO_DESCRIPTOR.items():
        record = records.get(object_id)
        if record is None:
            issues.append(f"Casey object record is missing: {object_id}")
            continue
        payload = record["payload"]
        identity = identities.get(object_id, {})
        chain_identity = payload.get("chain_identity")
        chain_identity = chain_identity if isinstance(chain_identity, dict) else {}
        expected_chain_projection = {
            "caip19": identity.get("caip19"),
            "chain_id": 1,
            "contract": identity.get("contract"),
            "custody_account": f"eip155:1:{MUSEUM_CUSTODY}",
            "custody_block": RECEIPT_BLOCK,
            "custody_receipt_block": RECEIPT_BLOCK,
            "custody_receipt_log": identity.get("custody_receipt_log"),
            "custody_receipt_transaction": RECEIPT_TRANSACTION,
            "custody_status": "verified",
            "token_id": identity.get("token_id"),
            "token_standard": "ERC-721",
        }
        if (
            payload.get("object_id") != object_id
            or payload.get("title") != identity.get("title")
            or any(chain_identity.get(key) != value for key, value in expected_chain_projection.items())
        ):
            issues.append(f"Casey object chain identity/provenance binding is invalid: {object_id}")
        if payload.get("preservation", {}).get("fixity_sha256") != evidence_manifest_sha256:
            issues.append(f"Casey object preservation evidence-manifest binding is invalid: {object_id}")
        expected_object_trait = {**expected_trait, "descriptor": descriptors.get(descriptor_slug)}
        if payload.get("trait_analysis") != expected_object_trait:
            issues.append(f"Casey object descriptor mapping or claims are invalid: {object_id}")
        if payload.get("medium") != OBJECT_MEDIUM:
            issues.append(f"Casey object medium must retain the unverified live-determinism boundary: {object_id}")
        if payload.get("current_state") != "received_onchain":
            issues.append(f"Casey object must remain received_onchain: {object_id}")
        if payload.get("review_status") != "pending_independent_review" or payload.get("reviewer") is not None:
            issues.append(f"Casey object review must remain incomplete without authority: {object_id}")
        if "accessioned" in [entry.get("state") for entry in payload.get("state_history", []) if isinstance(entry, dict)]:
            issues.append(f"Casey object may not claim accessioned: {object_id}")
        observation = payload.get("museum_observations", {})
        if (
            payload.get("visual_observation_record") != VISUAL_OBSERVATION_ID
            or payload.get("references") != [VISUAL_OBSERVATION_ID]
            or observation.get("observation_record") != VISUAL_OBSERVATION_ID
            or observation.get("observed_at") != LIVE_CAPTURE_DATA[object_id][0]
            or OBSERVATION_MARKERS[object_id] not in observation.get("static_visual_observation", "")
            or "commanded minimum wait of 1500 milliseconds" not in observation.get("live_behavior_observation", "")
            or "Exact per-frame timestamps" not in observation.get("live_behavior_observation", "")
            or "documentation surrogate" not in observation.get("documentation_surrogate", "")
            or PUBLIC_VISUAL_AUDIT_BOUNDARY not in observation.get("documentation_surrogate", "")
            or any(marker not in observation.get("live_behavior_observation", "") for marker in OBJECT_SOURCE_BEHAVIOR_MARKERS[object_id])
        ):
            issues.append(f"Casey object must retain dated, bounded visual and live-behavior observation: {object_id}")
    phototaxis = records.get("6529NM.2026.001.05", {}).get("payload", {})
    if "2022" not in phototaxis.get("project", {}).get("date_conflict", "") or "2021" not in phototaxis.get("project", {}).get("date_conflict", ""):
        issues.append("Casey Phototaxis record must retain the 2021 release / 2022 artist-register date conflict")
    rooms = records.get("6529NM.2026.001.06", {}).get("payload", {})
    if rooms.get("project", {}).get("edition_statement") != "Edition size reported as 924; generative system described as 923 unique rooms/combinations; this object: native token #713. Reviewed sources do not explain the relationship between the two counts.":
        issues.append("Casey 923 EMPTY ROOMS record must retain the 923-combination / 924-token distinction")

    for object_id, descriptor_slug in OBJECT_TO_DESCRIPTOR.items():
        page = root / CASEY_DIR / "public" / f"{object_id}.md"
        text = page.read_text(encoding="utf-8")
        descriptor_path = descriptors.get(descriptor_slug, {}).get("path")
        expected_url = f"{PUBLISHED_BLOB}/{descriptor_path}"
        if expected_url not in text or PUBLIC_DESCRIPTOR not in text or PUBLIC_STATE not in text or PUBLIC_NON_CLAIM not in text or PUBLIC_ACCEPTANCE not in text or PUBLIC_COMPLETION_BOUNDARY not in text or PUBLIC_VISUAL_AUDIT_BOUNDARY not in text:
            issues.append(f"Casey public page lacks required transparent descriptor/state/non-claim disclosure: {page.name}")
        if "pending linked deliverable" in text or STALE_BRANCH in text:
            issues.append(f"Casey public page retains obsolete pending or mutable-branch language: {page.name}")
        static_time = STATIC_CAPTURE_DATA[object_id][0]
        completed_at = LIVE_CAPTURE_DATA[object_id][0]
        for required in (
            "../visual-observation-record.json",
            static_time,
            completed_at,
            "commanded minimum wait of 1500 milliseconds",
            "not retained in the public repository pending rights and preservation review",
            "Museum interpretation [E]",
            *OBJECT_SOURCE_BEHAVIOR_MARKERS[object_id],
        ):
            if required not in text:
                issues.append(f"Casey public page lacks exact observation/interpretation disclosure {required!r}: {page.name}")
                break
    authorization_page = root / CASEY_DIR / "public" / "gift-acceptance-authorization.md"
    if not authorization_page.is_file():
        issues.append("Casey public gift acceptance authorization is missing")
    else:
        authorization_text = authorization_page.read_text(encoding="utf-8")
        for required in ("Gift Acceptance and Accession Authorization", "formally accepted", "not a signed deed", "completion certificate pending"):
            if required not in authorization_text:
                issues.append("Casey public gift acceptance authorization lacks its required limited-status disclosure")
                break

    artist_profile = (root / CASEY_DIR / "public" / "casey-reas-artist-practice.md").read_text(encoding="utf-8")
    if "**Museum interpretation [E]:** The token does not replace the software artwork" not in artist_profile:
        issues.append("Casey artist profile must label token/software continuity as Museum interpretation [E]")
    collection_essay = (root / CASEY_DIR / "public" / "casey-reas-collection-essay.md").read_text(encoding="utf-8")
    if "**Museum interpretation [E]:** The collection proposes an encounter with an executable image" not in collection_essay:
        issues.append("Casey collection essay must label executable-image ontology as Museum interpretation [E]")

    return issues


def validate(root: Path = ROOT, history_root: Path | None = None) -> list[str]:
    """Validate the reviewed, accessioned Casey REAS collection package."""
    source, descriptors, issues = source_package(history_root or root)
    receipt_transfers, receipt_issues = validate_receipt_evidence(root)
    issues.extend(receipt_issues)
    issues.extend(validate_evidence_manifest(root))

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
        if reviewer == payload.get("constructor") or reviewer.get("id") == payload.get("constructor", {}).get("id"):
            issues.append(f"Casey constructor/reviewer separation is invalid: {path.relative_to(root)}")
        signature_scheme = record.get("envelope", {}).get("signatureScheme")
        signature_digest = record.get("envelope", {}).get("signatureHash", {}).get("digest")
        if signature_scheme != "0x" + "0" * 64 or signature_digest != "0x" + "0" * 64:
            issues.append(f"Casey repository record must remain unsigned until on-chain execution: {path.relative_to(root)}")
        if any(STALE_BRANCH in text for text in nested_strings(record)):
            issues.append(f"Casey record has a mutable construction-branch URL: {path.relative_to(root)}")

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
    if not isinstance(actions, list) or len(actions) < 4 or any(item.get("status") != "active" for item in actions if isinstance(item, dict)):
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
    ):
        issues.append("Casey lot must bind the current preservation evidence manifest")

    identity_list = lot.get("object_identities")
    identity_list = identity_list if isinstance(identity_list, list) and all(isinstance(item, dict) for item in identity_list) else []
    expected_object_ids = list(OBJECT_TO_DESCRIPTOR)
    identities = {item.get("object_id"): item for item in identity_list}
    identity_keys = [(str(item.get("contract", "")).lower(), item.get("token_id"), item.get("custody_receipt_log")) for item in identity_list]
    if (
        [item.get("object_id") for item in identity_list] != expected_object_ids
        or len(identities) != 7
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
        or not instrument.get("content_hash")
    ):
        issues.append("Casey lot-level donation, title, and rights schedule must state the completed accession and reviewed CC BY-NC 4.0 determinations")

    preservation_manifest = lot.get("preservation_manifest") if isinstance(lot.get("preservation_manifest"), dict) else {}
    preservation_actions = preservation_manifest.get("active_stewardship_actions")
    if "pending" in preservation_manifest or not isinstance(preservation_actions, list) or len(preservation_actions) < 4:
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
    bindings = accession.get("title_bindings") if isinstance(accession.get("title_bindings"), list) else []
    if (
        [item.get("object_id") for item in bindings if isinstance(item, dict)] != expected_object_ids
        or any(item.get("status") != "executed" or item.get("transfer_transaction") != RECEIPT_TRANSACTION or not item.get("instrument_sha256") for item in bindings if isinstance(item, dict))
    ):
        issues.append("Casey accession certificate must execute one exact title binding per object")
    events = accession.get("events") if isinstance(accession.get("events"), list) else []
    if [item.get("event_type") for item in events if isinstance(item, dict)] != ["receipt", "acceptance", "acquisition", "title_passage", "custody_receipt", "accession"]:
        issues.append("Casey accession certificate must preserve the Stream-compatible event order")
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
    if (
        authorization.get("authorization_status") != "formally_accepted"
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
    for basis in authorization.get("governing_basis", []):
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
        if payload.get("current_state") != "accessioned" or payload.get("state_history", [])[-1].get("state") != "accessioned":
            issues.append(f"Casey object must end in accessioned state: {object_id}")
        title_binding = payload.get("title_binding", {})
        if title_binding.get("status") != "executed" or title_binding.get("transfer_transaction") != RECEIPT_TRANSACTION or title_binding.get("object_id") != object_id:
            issues.append(f"Casey object must retain an executed transaction-bound title declaration: {object_id}")
        grants = payload.get("rights", {})
        if set(grants) != rights_classes or any(item.get("grant_status") != "granted_with_conditions" or "CC BY-NC 4.0" not in item.get("basis", "") for item in grants.values()):
            issues.append(f"Casey object must state the complete conditional CC BY-NC 4.0 rights matrix: {object_id}")
        condition = payload.get("condition", {})
        if any(condition.get(key) in {None, "red", "not_assessed"} for key in condition_keys) or condition.get("token") != "green" or condition.get("metadata") != "green":
            issues.append(f"Casey object must state a complete non-red accession condition finding: {object_id}")
        if payload.get("display", {}).get("status") != "ready_with_conditions" or payload.get("preservation", {}).get("status") != "in_progress":
            issues.append(f"Casey object must separate conditional display readiness from active preservation: {object_id}")
        suffix = object_id.rsplit(".", 1)[1]
        expected_generator = GENERATOR_EVIDENCE[suffix]
        generator = payload.get("generator_snapshot") if isinstance(payload.get("generator_snapshot"), dict) else {}
        if (
            generator.get("sha256") != expected_generator["response_sha256"]
            or generator.get("dependency_observed") != expected_generator["dependency"]
            or generator.get("interaction_map") != expected_generator["interaction_map"]
            or generator.get("interaction_review_status") != "source_reviewed_not_exhaustively_exercised"
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
        if rights_payload.get("grants") != grants or "copyright is not transferred" not in rights_payload.get("rights_holder_reference", "").lower():
            issues.append(f"Casey rights statement must match the object matrix and copyright boundary: {object_id}")
        condition_payload = condition_record["payload"]
        if condition_payload.get("outcome", "").split(":", 1)[0] != "pass_with_conditions" or any(value in {"red", "not_assessed"} for value in condition_payload.get("assessments", {}).values()):
            issues.append(f"Casey condition report must reach a complete pass-with-conditions outcome: {object_id}")

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
    if "**Museum interpretation [E]:** The token does not replace the software artwork" not in artist_profile:
        issues.append("Casey artist profile must retain the token/software interpretation boundary")
    if "**Museum interpretation [E]:** The collection proposes an encounter with an executable image" not in collection_essay:
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
        rooms.get("project", {}).get("edition_statement") != ROOMS_EDITION_STATEMENT
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
