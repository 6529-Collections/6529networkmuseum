#!/usr/bin/env python3
"""Acquire one exact-finalized-block custody package for Magnum 75.

This is an evidence acquisition tool, not an accession decision.  It binds
the five externally minted ERC-721 tokens to one finalized Ethereum block,
retains the exact JSON-RPC request/response bytes, verifies each expected
transfer receipt and ``Transfer`` log, and reads ``ownerOf`` and
``getApproved`` at the same EIP-1898 block hash.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
import hashlib
import json
import os
from pathlib import Path
import re
import ssl
import stat
import sys
import time

from safe_fetch import SafeHTTPSFetcher, _PinnedHTTPSConnection


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "evidence" / "magnum-75-custody"
PUBLIC_RPC_URL = "https://eth-mainnet.public.blastapi.io"
ALCHEMY_ENV_FILES = (
    Path(r"D:\\repos\\6529seize-backend\\.env.local"),
    Path(r"D:\\repos\\6529seize-backend\\src\\api-serverless\\.env.local"),
)


def load_alchemy_key() -> str | None:
    value = os.environ.get("ALCHEMY_API_KEY", "").strip()
    if value:
        return value
    for path in ALCHEMY_ENV_FILES:
        if not path.is_file():
            continue
        for line in path.read_text(encoding="utf-8").splitlines():
            match = re.match(r"^\s*ALCHEMY_API_KEY\s*=\s*(.+?)\s*$", line)
            if match:
                candidate = match.group(1).strip().strip('"').strip("'")
                if candidate:
                    return candidate
    return None


ALCHEMY_KEY = load_alchemy_key()
RPC_URL = (
    f"https://eth-mainnet.g.alchemy.com/v2/{ALCHEMY_KEY}"
    if ALCHEMY_KEY
    else PUBLIC_RPC_URL
)
RPC_DISPLAY_URL = (
    "https://eth-mainnet.g.alchemy.com/v2/<redacted>"
    if ALCHEMY_KEY
    else PUBLIC_RPC_URL
)
USER_AGENT = "6529-Network-Museum/magnum-75-custody-audit-v1"


def http10_connection_factory(endpoint, resolved, policy):
    connection = _PinnedHTTPSConnection(
        endpoint,
        resolved.selected_ip,
        float(policy["connect_timeout_seconds"]),
        float(policy["read_timeout_seconds"]),
        ssl.create_default_context(),
    )
    connection._http_vsn = 10
    connection._http_vsn_str = "HTTP/1.0"
    return connection


FETCHER = SafeHTTPSFetcher(connection_factory=http10_connection_factory)
MUSEUM = "0xbecfa2ba5a782d11e1a0e821e8f2e30b6684178c"
DONOR = "0x6daa633c23615a29471deafae351727867e7dad1"
CONTRACT = "0xe628b59d34f42b16c53f4d697f1ffd4d8d987b91"
TRANSFER_TOPIC = "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"
MAX_TRANSFER_BLOCK = 25741724
OWNER_OF_SELECTOR = "6352211e"
GET_APPROVED_SELECTOR = "081812fc"
TOKENS = (
    {
        "object_id": "6529NM.2026.002.01",
        "candidate_object_id": "6529NM-PG-2026-001.OBJ-001",
        "token_id": 127,
        "tx_hash": "0xa7c3ac876453a9b5af10b53402a284e6f14d66a29df197e4b148c3c23970836c",
        "block_number": 25741708,
        "log_index": 696,
    },
    {
        "object_id": "6529NM.2026.002.02",
        "candidate_object_id": "6529NM-PG-2026-001.OBJ-002",
        "token_id": 145,
        "tx_hash": "0xe4af0f51779cf14b18297aa922876029640734c102395c02f0d054c55e630b8d",
        "block_number": 25741724,
        "log_index": 229,
    },
    {
        "object_id": "6529NM.2026.002.03",
        "candidate_object_id": "6529NM-PG-2026-001.OBJ-003",
        "token_id": 97,
        "tx_hash": "0x0ff08ed5fb29cc8e83dd50191e1156615ad23d584e05c9d1803af39151ecb33d",
        "block_number": 25741718,
        "log_index": 430,
    },
    {
        "object_id": "6529NM.2026.002.04",
        "candidate_object_id": "6529NM-PG-2026-001.OBJ-004",
        "token_id": 44,
        "tx_hash": "0x9fbef477914c51b2d4e3ae13f791d36499a5ac0516e7ce13a0b40531bc833e74",
        "block_number": 25741721,
        "log_index": 207,
    },
    {
        "object_id": "6529NM.2026.002.05",
        "candidate_object_id": "6529NM-PG-2026-001.OBJ-005",
        "token_id": 104,
        "tx_hash": "0x443e02349d0b5538fd33acb392edbb6ce63a6479917b3be0d71cd5069cdaaa07",
        "block_number": 25741705,
        "log_index": 385,
    },
)


class EvidenceError(RuntimeError):
    """Raised when the exact evidence boundary cannot be established."""


def canonical_json(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def prepare_output() -> None:
    if OUTPUT.exists():
        info = OUTPUT.lstat()
        if stat.S_ISLNK(info.st_mode) or info.st_file_attributes & 0x400:
            raise EvidenceError("evidence output cannot be a link or reparse point")
        if any(OUTPUT.iterdir()):
            raise EvidenceError("evidence output must be empty; replacement is a separate governed operation")
    else:
        OUTPUT.mkdir(parents=True)


def write_bytes(path: Path, value: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(value)


def rpc(method: str, params: list[object]) -> tuple[bytes, dict[str, object]]:
    request = {"jsonrpc": "2.0", "id": method, "method": method, "params": params}
    body = canonical_json(request)
    # Public Ethereum endpoints enforce per-IP limits and may vary response
    # framing under burst traffic. Keep one guarded transport and pace calls so
    # the evidence run remains admitted by the repository's fail-closed policy.
    time.sleep(1.0)
    result = FETCHER.fetch(
        RPC_URL,
        method="POST",
        body=body,
        headers={"Accept": "application/json", "Content-Type": "application/json", "User-Agent": USER_AGENT},
        expires_at=datetime.now(UTC) + timedelta(seconds=30),
    )
    if result.observation.status != 200:
        raise EvidenceError(f"{method}: HTTP {result.observation.status}")
    try:
        response = json.loads(result.body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise EvidenceError(f"{method}: response is not JSON") from exc
    if not isinstance(response, dict) or response.get("jsonrpc") != "2.0" or response.get("id") != method:
        raise EvidenceError(f"{method}: malformed JSON-RPC response")
    if "error" in response:
        raise EvidenceError(f"{method}: {response['error']}")
    transport = result.observation.to_dict()
    if isinstance(transport, dict):
        transport["url"] = RPC_DISPLAY_URL
    return body, {"response": response, "transport": transport, "response_bytes": result.body}


def abi_word(value: object) -> str:
    if not isinstance(value, str) or not value.startswith("0x") or len(value) != 66:
        raise EvidenceError("ABI result is not one 32-byte word")
    return "0x" + value[-40:].lower()


def calldata(selector: str, value: int) -> str:
    return "0x" + selector + f"{value:064x}"


def raw_ref(category: str, request: bytes, response: bytes, transport: dict[str, object]) -> dict[str, object]:
    digest = sha256(response)
    relative = Path("raw") / category / f"sha256-{digest}.json"
    write_bytes(OUTPUT / relative, response)
    return {
        "path": relative.as_posix(),
        "sha256": f"sha256:{digest}",
        "size": len(response),
        "request_sha256": f"sha256:{sha256(request)}",
        "request_size": len(request),
        "byte_mode": "raw",
        "media_type": "application/json",
        "transport": transport,
    }


def run() -> dict[str, object]:
    prepare_output()
    evidence: list[dict[str, object]] = []

    chain_request, chain = rpc("eth_chainId", [])
    chain_result = chain["response"].get("result")
    if chain_result != "0x1":
        raise EvidenceError(f"RPC is not Ethereum mainnet: {chain_result!r}")
    evidence.append(raw_ref("chain", chain_request, chain["response_bytes"], chain["transport"]))

    block_request, block_call = rpc("eth_getBlockByNumber", ["finalized", False])
    block = block_call["response"].get("result")
    if not isinstance(block, dict):
        raise EvidenceError("finalized tag did not return a block")
    block_number_hex = block.get("number")
    block_hash = block.get("hash")
    block_timestamp_hex = block.get("timestamp")
    if not all(isinstance(value, str) for value in (block_number_hex, block_hash, block_timestamp_hex)):
        raise EvidenceError("finalized block identity is incomplete")
    block_number = int(block_number_hex, 16)
    if block_number < MAX_TRANSFER_BLOCK:
        raise EvidenceError(f"finalized block {block_number} is before transfer block {MAX_TRANSFER_BLOCK}")
    block_time = datetime.fromtimestamp(int(block_timestamp_hex, 16), UTC).isoformat(timespec="seconds").replace("+00:00", "Z")
    state_selector = {"blockHash": block_hash, "requireCanonical": True}
    evidence.append(raw_ref("finalized-block", block_request, block_call["response_bytes"], block_call["transport"]))

    objects: list[dict[str, object]] = []
    for item in TOKENS:
        receipt_request, receipt_call = rpc("eth_getTransactionReceipt", [item["tx_hash"]])
        receipt = receipt_call["response"].get("result")
        if not isinstance(receipt, dict):
            raise EvidenceError(f"receipt missing for {item['object_id']}")
        if receipt.get("transactionHash", "").lower() != item["tx_hash"].lower():
            raise EvidenceError(f"receipt hash mismatch for {item['object_id']}")
        if int(str(receipt.get("blockNumber")), 16) != item["block_number"] or receipt.get("status") != "0x1":
            raise EvidenceError(f"receipt status/block mismatch for {item['object_id']}")
        matching_logs = []
        for log in receipt.get("logs", []):
            if not isinstance(log, dict):
                continue
            topics = log.get("topics", [])
            if (
                str(log.get("address", "")).lower() == CONTRACT
                and isinstance(topics, list)
                and len(topics) == 4
                and str(topics[0]).lower() == TRANSFER_TOPIC
                and str(topics[1]).lower() == "0x" + DONOR[2:].rjust(64, "0")
                and str(topics[2]).lower() == "0x" + MUSEUM[2:].rjust(64, "0")
                and int(str(topics[3]), 16) == item["token_id"]
                and int(str(log.get("logIndex")), 16) == item["log_index"]
            ):
                matching_logs.append(log)
        if len(matching_logs) != 1:
            raise EvidenceError(f"expected one matching Transfer log for {item['object_id']}, found {len(matching_logs)}")
        evidence.append(raw_ref(f"receipt-{item['token_id']}", receipt_request, receipt_call["response_bytes"], receipt_call["transport"]))

        transfer_block_request, transfer_block_call = rpc(
            "eth_getBlockByNumber", [f"0x{item['block_number']:x}", False]
        )
        transfer_block = transfer_block_call["response"].get("result")
        if not isinstance(transfer_block, dict):
            raise EvidenceError(f"transfer block missing for {item['object_id']}")
        transfer_block_hash = transfer_block.get("hash")
        receipt_block_hash = receipt.get("blockHash")
        transfer_timestamp_hex = transfer_block.get("timestamp")
        if (
            not isinstance(transfer_block_hash, str)
            or not isinstance(receipt_block_hash, str)
            or transfer_block_hash.lower() != receipt_block_hash.lower()
            or not isinstance(transfer_timestamp_hex, str)
        ):
            raise EvidenceError(f"transfer block identity mismatch for {item['object_id']}")
        transfer_block_time = datetime.fromtimestamp(
            int(transfer_timestamp_hex, 16), UTC
        ).isoformat(timespec="seconds").replace("+00:00", "Z")
        evidence.append(
            raw_ref(
                f"transfer-block-{item['token_id']}",
                transfer_block_request,
                transfer_block_call["response_bytes"],
                transfer_block_call["transport"],
            )
        )

        owner_request, owner_call = rpc("eth_call", [{"to": CONTRACT, "data": calldata(OWNER_OF_SELECTOR, item["token_id"])}, state_selector])
        owner = abi_word(owner_call["response"].get("result"))
        if owner != MUSEUM:
            raise EvidenceError(f"ownerOf mismatch for {item['object_id']}: {owner}")
        evidence.append(raw_ref(f"owner-{item['token_id']}", owner_request, owner_call["response_bytes"], owner_call["transport"]))

        approval_request, approval_call = rpc("eth_call", [{"to": CONTRACT, "data": calldata(GET_APPROVED_SELECTOR, item["token_id"])}, state_selector])
        approved = abi_word(approval_call["response"].get("result"))
        evidence.append(raw_ref(f"approval-{item['token_id']}", approval_request, approval_call["response_bytes"], approval_call["transport"]))
        objects.append({
            **item,
            "contract": CONTRACT,
            "caip19": f"eip155:1/erc721:{CONTRACT}/{item['token_id']}",
            "owner": owner,
            "owner_matches_museum": True,
            "token_level_approved_operator": approved,
            "token_level_approval_is_zero": approved == "0x" + "0" * 40,
            "matching_transfer_log_count": 1,
            "transfer_block_hash": transfer_block_hash,
            "transfer_block_timestamp": transfer_block_time,
        })

    after_request, after_call = rpc("eth_getBlockByNumber", ["finalized", False])
    after = after_call["response"].get("result")
    if not isinstance(after, dict) or after.get("number") != block_number_hex or after.get("hash") != block_hash:
        raise EvidenceError("finalized block changed during acquisition")
    evidence.append(raw_ref("finalized-block-after", after_request, after_call["response_bytes"], after_call["transport"]))

    return {
        "record_id": "6529NM.2026.002.CUSTODY-EVIDENCE-01",
        "record_type": "MAGNUM_75_CUSTODY_OBSERVATION",
        "observed_at": datetime.now(UTC).isoformat(timespec="milliseconds").replace("+00:00", "Z"),
        "network": "Ethereum mainnet",
        "rpc_endpoint": RPC_DISPLAY_URL,
        "museum_address": MUSEUM,
        "donor_address": DONOR,
        "contract": CONTRACT,
        "finalized_block": {"number": block_number, "hash": block_hash, "timestamp": block_time},
        "state_selector": {"blockHash": block_hash, "requireCanonical": True},
        "objects": objects,
        "assertions": {
            "all_expected_transfer_receipts_successful": True,
            "all_transfer_logs_match_donor_museum_contract_token_and_log_index": True,
            "all_ownerOf_reads_match_museum": True,
            "all_reads_share_one_finalized_block_hash": True,
            "token_level_approvals_are_zero": all(item["token_level_approval_is_zero"] for item in objects),
        },
        "raw_evidence": evidence,
        "limitations": [
            "This package proves the observed on-chain transfer and custody state only.",
            "It does not itself prove the donor's legal authority, copyright transfer, or the terms of the gift instrument.",
            "The exact transfer receipts are bound to the Museum accession package; the finalized block is the common state observation.",
        ],
    }


def main() -> int:
    try:
        observation = run()
    except (EvidenceError, OSError, ValueError) as exc:
        print(f"Magnum custody evidence acquisition refused: {exc}")
        return 1
    encoded = (json.dumps(observation, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")
    summary = {
        "path": "summary.json",
        "sha256": f"sha256:{sha256(encoded)}",
        "size": len(encoded),
        "byte_mode": "raw",
        "observation": observation,
    }
    write_bytes(OUTPUT / "summary.json", encoded)
    print(f"Magnum custody evidence acquired at finalized block {observation['finalized_block']['number']}: {OUTPUT}")
    print(json.dumps({"summary_sha256": summary["sha256"], "object_count": len(observation["objects"])}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
