#!/usr/bin/env python3
"""Acquire an exact-finalized-block custody audit for the Casey accession.

The acquisition uses the repository's fail-closed HTTPS transport, retains the
exact JSON-RPC response bytes, obtains one finalized Ethereum block, and then
evaluates ENS resolution, ``ownerOf`` and token-level ``getApproved`` against
that exact block hash through EIP-1898 on a second provider. It does not make
legal-title, sanctions, valuation, or off-chain-encumbrance conclusions.
"""

from __future__ import annotations

import argparse
from datetime import UTC, datetime, timedelta
import hashlib
import json
import os
from pathlib import Path
import stat
import sys
import time
from typing import Any

from safe_fetch import FetchPolicyError, SafeHTTPSFetcher


ROOT = Path(__file__).resolve().parents[1]
HEAD_RPC_URL = "https://1rpc.io/eth"
CALL_RPC_URL = "https://ethereum-rpc.publicnode.com"
USER_AGENT = "6529-Network-Museum/casey-custody-audit-v1"
MUSEUM_ADDRESS = "0xbecfa2ba5a782d11e1a0e821e8f2e30b6684178c"
ENS_NAME = "networkmuseum.6529.eth"
ENS_NAMEHASH = "f90c6c0dca064bc19c04756dc088ceb60402ce8522ab4623f016d19abbb76394"
ENS_REGISTRY = "0x00000000000c2e074ec69a0dfb2997ba6c7d2e1e"
ZERO_ADDRESS = "0x0000000000000000000000000000000000000000"
SELECTORS = {
    "resolver": "0178b8bf",
    "addr": "3b3b57de",
    "ownerOf": "6352211e",
    "getApproved": "081812fc",
}
OBJECTS = (
    ("6529NM.2026.001.01", "0xa7d8d9ef8d8ce8992df33d8b8cf4aebabd5bd270", 100000031),
    ("6529NM.2026.001.02", "0xa7d8d9ef8d8ce8992df33d8b8cf4aebabd5bd270", 100000724),
    ("6529NM.2026.001.03", "0xa7d8d9ef8d8ce8992df33d8b8cf4aebabd5bd270", 100000401),
    ("6529NM.2026.001.04", "0x99a9b7c1116f9ceeb1652de04d5969cce509b069", 383000063),
    ("6529NM.2026.001.05", "0xa7d8d9ef8d8ce8992df33d8b8cf4aebabd5bd270", 164000308),
    ("6529NM.2026.001.06", "0x145789247973c5d612bf121e9e4eef84b63eb707", 1000713),
    ("6529NM.2026.001.07", "0x0000000c687daed0fba60d1dba4e5f6149e8b894", 248),
)


class AuditError(RuntimeError):
    """Raised when an exact, internally consistent audit cannot be emitted."""


def prepare_empty_output(output: Path) -> None:
    """Create or admit only an explicit empty, non-linked output directory."""
    if os.path.lexists(output):
        info = os.lstat(output)
        is_reparse = bool(
            getattr(info, "st_file_attributes", 0)
            & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
        )
        if stat.S_ISLNK(info.st_mode) or is_reparse:
            raise AuditError("output directory cannot be a symlink or reparse point")
        if not stat.S_ISDIR(info.st_mode):
            raise AuditError("output path is not a directory")
        if any(output.iterdir()):
            raise AuditError("output directory must be empty; evidence replacement is a separate governed operation")
    else:
        output.mkdir(parents=True, exist_ok=False)


def canonical_json(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def write_bytes(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_bytes(payload)
    temporary.replace(path)


def write_json(path: Path, value: Any) -> None:
    write_bytes(path, (json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode("utf-8"))


def post_rpc(fetcher: SafeHTTPSFetcher, url: str, payload: Any) -> tuple[bytes, Any, dict[str, Any]]:
    request = canonical_json(payload)
    result = fetcher.fetch(
        url,
        method="POST",
        body=request,
        headers={"Accept": "application/json", "Content-Type": "application/json", "User-Agent": USER_AGENT},
        expires_at=datetime.now(UTC) + timedelta(seconds=30),
    )
    if result.observation.status != 200:
        raise AuditError(f"JSON-RPC HTTP status from {url} is {result.observation.status}")
    try:
        decoded = json.loads(result.body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise AuditError("JSON-RPC response is not valid UTF-8 JSON") from error
    return request, decoded, {"body": result.body, "observation": result.observation.to_dict()}


def by_id(response: Any) -> dict[str, dict[str, Any]]:
    rows = response if isinstance(response, list) else [response]
    if not all(isinstance(row, dict) and isinstance(row.get("id"), str) for row in rows):
        raise AuditError("JSON-RPC response does not preserve string request identifiers")
    result = {row["id"]: row for row in rows}
    if len(result) != len(rows):
        raise AuditError("JSON-RPC response contains duplicate identifiers")
    for request_id, row in result.items():
        if row.get("jsonrpc") != "2.0" or "error" in row or not isinstance(row.get("result"), (str, dict)):
            raise AuditError(f"JSON-RPC call failed: {request_id}")
    return result


def abi_word_address(value: str) -> str:
    if not isinstance(value, str) or not value.startswith("0x") or len(value) != 66:
        raise AuditError("ABI address result is not one 32-byte word")
    if any(character not in "0123456789abcdefABCDEF" for character in value[2:]):
        raise AuditError("ABI address result is not hexadecimal")
    return "0x" + value[-40:].lower()


def calldata(selector: str, value: int | str) -> str:
    encoded = f"{value:064x}" if isinstance(value, int) else value.removeprefix("0x").lower().rjust(64, "0")
    if len(encoded) != 64:
        raise AuditError("ABI argument is not one word")
    return "0x" + selector + encoded


def raw_ref(output: Path, category: str, payload: bytes) -> dict[str, Any]:
    digest = sha256(payload)
    relative = Path("raw") / category / f"sha256-{digest}.json"
    write_bytes(output / relative, payload)
    return {
        "path": relative.as_posix(),
        "sha256": f"sha256:{digest}",
        "size": len(payload),
        "media_type": "application/json",
        "byte_mode": "raw",
    }


def request_ref(payload: bytes) -> dict[str, Any]:
    return {"sha256": f"sha256:{sha256(payload)}", "size": len(payload), "canonicalization": "sorted-key compact JSON"}


def call_rpc(
    fetcher: SafeHTTPSFetcher,
    output: Path,
    request_id: str,
    method: str,
    params: list[Any],
    endpoint: str,
) -> tuple[bytes, dict[str, Any], dict[str, Any], dict[str, Any]]:
    # Public endpoints enforce per-IP limits.  A fixed interval keeps the
    # evidence acquisition reproducible without treating rate-limit pages as
    # RPC responses.
    time.sleep(1.0)
    try:
        request, decoded, fetched = post_rpc(
            fetcher,
            endpoint,
            {"jsonrpc": "2.0", "id": request_id, "method": method, "params": params},
        )
    except AuditError as error:
        raise AuditError(f"{request_id}: {error}") from error
    try:
        row = by_id(decoded).get(request_id)
    except AuditError as error:
        raise AuditError(f"{request_id}: {error}") from error
    if row is None:
        raise AuditError(f"JSON-RPC response omitted request identifier: {request_id}")
    return request, row, raw_ref(output, "rpc", fetched["body"]), fetched["observation"]


def acquire(output: Path) -> dict[str, Any]:
    prepare_empty_output(output)
    fetcher = SafeHTTPSFetcher()
    observed_at = datetime.now(UTC).isoformat(timespec="milliseconds").replace("+00:00", "Z")

    raw_entries: list[dict[str, Any]] = []
    request_refs: dict[str, Any] = {}
    observations: dict[str, Any] = {}

    chain_request, chain_row, chain_raw, chain_observation = call_rpc(
        fetcher, output, "chain-id", "eth_chainId", [], HEAD_RPC_URL
    )
    raw_entries.append(chain_raw)
    request_refs["chain_id"] = request_ref(chain_request)
    observations["chain_id"] = chain_observation
    if chain_row["result"] != "0x1":
        raise AuditError("RPC endpoint did not report Ethereum mainnet")

    block_request, block_row, block_raw, block_observation = call_rpc(
        fetcher, output, "finalized-block", "eth_getBlockByNumber", ["finalized", False], HEAD_RPC_URL
    )
    raw_entries.append(block_raw)
    request_refs["finalized_block"] = request_ref(block_request)
    observations["finalized_block"] = block_observation
    block = block_row["result"]
    if not isinstance(block, dict):
        raise AuditError("finalized block response has no block object")
    block_tag = block.get("number")
    block_hash = block.get("hash")
    block_timestamp = block.get("timestamp")
    if not all(isinstance(value, str) and value.startswith("0x") for value in (block_tag, block_hash, block_timestamp)):
        raise AuditError("finalized block identity is incomplete")
    block_number = int(block_tag, 16)
    block_time = datetime.fromtimestamp(int(block_timestamp, 16), UTC).isoformat(timespec="seconds").replace("+00:00", "Z")
    # Bind every state read to the exact finalized block hash through EIP-1898.
    # A moving ``finalized`` tag would prove only a window, not that all calls
    # were evaluated at the retained block/hash.
    state_selector = {"blockHash": block_hash, "requireCanonical": True}

    resolver_request, resolver_row, resolver_raw, resolver_observation = call_rpc(
        fetcher,
        output,
        "ens-resolver",
        "eth_call",
        [{"to": ENS_REGISTRY, "data": calldata(SELECTORS["resolver"], ENS_NAMEHASH)}, state_selector],
        CALL_RPC_URL,
    )
    raw_entries.append(resolver_raw)
    request_refs["ens_resolver"] = request_ref(resolver_request)
    observations["ens_resolver"] = resolver_observation
    resolver_address = abi_word_address(resolver_row["result"])
    if resolver_address == ZERO_ADDRESS:
        raise AuditError("ENS Registry returned the zero resolver")

    ens_request, ens_row, ens_raw, ens_observation = call_rpc(
        fetcher,
        output,
        "ens-address",
        "eth_call",
        [{"to": resolver_address, "data": calldata(SELECTORS["addr"], ENS_NAMEHASH)}, state_selector],
        CALL_RPC_URL,
    )
    raw_entries.append(ens_raw)
    request_refs["ens_address"] = request_ref(ens_request)
    observations["ens_address"] = ens_observation
    ens_address = abi_word_address(ens_row["result"])
    if ens_address != MUSEUM_ADDRESS:
        raise AuditError(f"{ENS_NAME} resolved to {ens_address}, not the configured Museum address")

    objects: list[dict[str, Any]] = []
    for object_id, contract, token_id in OBJECTS:
        owner_request, owner_row, owner_raw, owner_observation = call_rpc(
            fetcher,
            output,
            f"owner:{object_id}",
            "eth_call",
            [{"to": contract, "data": calldata(SELECTORS["ownerOf"], token_id)}, state_selector],
            CALL_RPC_URL,
        )
        approval_request, approval_row, approval_raw, approval_observation = call_rpc(
            fetcher,
            output,
            f"approval:{object_id}",
            "eth_call",
            [{"to": contract, "data": calldata(SELECTORS["getApproved"], token_id)}, state_selector],
            CALL_RPC_URL,
        )
        raw_entries.extend([owner_raw, approval_raw])
        request_refs[f"owner:{object_id}"] = request_ref(owner_request)
        request_refs[f"approval:{object_id}"] = request_ref(approval_request)
        observations[f"owner:{object_id}"] = owner_observation
        observations[f"approval:{object_id}"] = approval_observation
        owner = abi_word_address(owner_row["result"])
        approved = abi_word_address(approval_row["result"])
        if owner != MUSEUM_ADDRESS:
            raise AuditError(f"{object_id} ownerOf returned {owner}")
        objects.append(
            {
                "object_id": object_id,
                "contract": contract,
                "token_id": str(token_id),
                "caip19": f"eip155:1/erc721:{contract}/{token_id}",
                "owner": owner,
                "owner_matches_museum": True,
                "token_level_approved_operator": approved,
                "token_level_approval_is_zero": approved == ZERO_ADDRESS,
            }
        )

    after_request, after_row, after_raw, after_observation = call_rpc(
        fetcher, output, "finalized-block-after", "eth_getBlockByNumber", ["finalized", False], HEAD_RPC_URL
    )
    raw_entries.append(after_raw)
    request_refs["finalized_block_after"] = request_ref(after_request)
    observations["finalized_block_after"] = after_observation
    after_block = after_row["result"]
    if not isinstance(after_block, dict):
        raise AuditError("closing finalized block response has no block object")
    if after_block.get("number") != block_tag or after_block.get("hash") != block_hash:
        raise AuditError("finalized block changed during the custody observation window")
    summary = {
        "schema_version": "6529nm.casey-custody-audit.v1",
        "audit_id": "6529NM.2026.001.CUSTODY-AUDIT-20260802",
        "subject_id": "6529NM.2026.001",
        "observed_at": observed_at,
        "chain": {"chain_id": 1, "caip2": "eip155:1", "finality_tag": "finalized"},
        "block": {"number": block_number, "numeric_tag": block_tag, "state_selector": state_selector, "hash": block_hash.lower(), "timestamp": block_time},
        "custodian": {"ens": ENS_NAME, "ens_namehash": "0x" + ENS_NAMEHASH, "resolver": resolver_address, "address": ens_address},
        "objects": objects,
        "result": {
            "all_owner_of_results_match_museum": True,
            "all_token_level_approvals_are_zero": all(item["token_level_approval_is_zero"] for item in objects),
            "ens_resolves_to_museum_at_same_block": True,
            "finalized_boundary_stable_before_and_after": True,
            "object_count": len(objects),
        },
        "method": {
            "rpc_endpoints": {"chain_and_finalized_block": HEAD_RPC_URL, "eip1898_block_hash_contract_reads": CALL_RPC_URL},
            "transport": "scripts/safe_fetch.py",
            "selectors": {name: "0x" + value for name, value in SELECTORS.items()},
            "same_block_rule": "One provider returned the retained finalized block number and hash before and after the observation window; every ENS resolver, ENS address, ownerOf, and getApproved call on the second provider used an EIP-1898 selector containing that exact blockHash with requireCanonical true.",
            "evidence_boundary": "This proves the queried contract state at the retained finalized block. A zero token-level approval is not proof that no operator-for-all approval, private claim, legal encumbrance, key compromise, or later transfer exists.",
        },
        "requests": request_refs,
        "responses": sorted(raw_entries, key=lambda item: item["path"]),
        "safe_fetch_observations": observations,
    }
    summary_path = output / "custody-audit-2026-08-02.json"
    write_json(summary_path, summary)
    summary_ref = {
        "path": summary_path.relative_to(output).as_posix(),
        "sha256": f"sha256:{sha256(summary_path.read_bytes())}",
        "size": summary_path.stat().st_size,
        "media_type": "application/json",
        "byte_mode": "raw",
    }
    manifest = {
        "manifest_type": "6529NM_CASEY_ACCESSION_DILIGENCE_EVIDENCE",
        "manifest_version": "1.0.0",
        "subject_id": "6529NM.2026.001",
        "observed_at": observed_at,
        "hash_algorithm": "sha256",
        "byte_mode": "raw",
        "entries": sorted([*raw_entries, summary_ref], key=lambda item: item["path"]),
    }
    write_json(output / "manifest.json", manifest)
    return {
        "status": "complete",
        "audit": summary_ref,
        "manifest_sha256": f"sha256:{sha256((output / 'manifest.json').read_bytes())}",
        "block_number": block_number,
        "block_hash": block_hash.lower(),
        "all_owner_of_results_match_museum": True,
        "all_token_level_approvals_are_zero": summary["result"]["all_token_level_approvals_are_zero"],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True, help="new or empty destination; never a tracked package in place")
    args = parser.parse_args(argv)
    try:
        print(json.dumps(acquire(args.output_dir.absolute()), ensure_ascii=False, indent=2))
    except (AuditError, FetchPolicyError, OSError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
