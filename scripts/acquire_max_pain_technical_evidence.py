#!/usr/bin/env python3
"""Acquire exact-finalized-block technical evidence for MAX PAIN #4188/7394.

The package follows the Vera Molnar technical acquisition's collector pattern:
every retained JSON-RPC exchange is written as numbered request and response
bytes under ``raw/rpc/``, derived files are written under ``derived/``, and the
manifest commits to every file.  All state reads use the target finalized
block hash through EIP-1898 with ``requireCanonical``.

Observations:

* runtime bytecode (SHA-256 and keccak-256), EIP-1967 slots, ``name``,
  ``symbol``, ``creator``, ``tokenURI``, ``tokenIPFSHash``, ``tokenName``,
  ``_getFinalized(1)``, ``_mintCount(1)``, ``_typeCount``, ``_defaultOwner``,
  the token-id multipliers, interface support and the royalty surface;
* an ``ownerOf`` scan of all 7,394 minted ids through Multicall3
  ``aggregate3`` at the target block hash;
* the mint transaction of #4188 and every later transfer of the token, with
  receipts and blocks, decoded into roles, venues and payments;
* the complete set of burn ``Transfer`` logs from the first mint block to the
  target block, and each burn transaction's destination contract and method
  selector, compared with the ``ownerOf`` scan.

Responses that would publish third parties' wallet addresses in bulk (the
supply scan, the burn log scan and the burn transaction lookups) are not
retained; the package records their request and response SHA-256 commitments
and the derived counts.  A sample of burn receipts and the token's own
provenance receipts are retained, so prior holders' addresses appear only in
those raw receipts, never in derived prose.  This is an evidence acquisition
tool, not an accession, title, rights or valuation decision.
"""

from __future__ import annotations

import argparse
from collections import Counter
from datetime import UTC, datetime
import json
from pathlib import Path
import sys
import time
from typing import Any

from safe_fetch import FetchPolicyError

import max_pain_evidence_common as common
from max_pain_evidence_common import (
    ACCESSION_ID,
    AGENT_ADDRESS,
    BATCH_RPC_URL,
    CAIP19,
    CONTRACT,
    EvidenceError,
    IMAGE_CID,
    MINT_BLOCK,
    MINT_TX,
    MUSEUM_ADDRESS,
    MUSEUM_RECEIPT_BLOCK,
    MUSEUM_RECEIPT_TX,
    PRIMARY_RPC_URL,
    PURCHASE_BLOCK,
    PURCHASE_TX,
    TOKEN_ID,
    TOKEN_URI,
    TRANSFER_TOPIC,
    ZERO_ADDRESS,
)


USER_AGENT = "6529-Network-Museum/xcopy-max-pain-4188-technical-evidence-v1"
RECORD_ID = f"{ACCESSION_ID}.TECHNICAL-EVIDENCE-01"
MULTICALL3 = "0xca11bde05977b3631167028862be2a173976ca11"
FIRST_TOKEN_ID = 171_000_100_001
LAST_TOKEN_ID = 171_000_107_394
MINTED_COUNT = 7_394
FIRST_MINT_BLOCK = 14_451_975
SCAN_WINDOW_BLOCKS = 10_000
SUPPLY_BATCH = 500
TX_BATCH = 50
NONEXISTENT_REVERT = "ERC721: owner query for nonexistent token"
BURN_REDEEM_EXTENSION = "0xfc29813beeb3c7395c7a5f8dfc3352491d5ea0e2"
DAMAGE_CONTROL_CONTRACT = "0x3e34ff1790bf0a13efd7d77e75870cb525687338"
MAX_PAIN_FEE_HANDLER = "0x7aca5424c570c2ad530ee3d4dbfd731a9aebacff"
NIFTY_GATEWAY_MINTER_KEY = "0x1f670ec15f68f2011bc51f423a062565e13f5355"
OPENSEA_FEE_RECIPIENT = "0x0000a26b00c1f0df003000390027140000faa719"
WYVERN_EXCHANGE = "0x7f268357a8c2552623316e2562d90e642bb538e5"
TRANSFER_HELPER = "0x0000000000c2d145a2526bd8c716263bfebe1a72"
WETH = "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"
CONSECUTIVE_TRANSFER_TOPIC = "0xdeaa91b6123d068f5821d0fb0678463d1a8a6079fe8af5de3ce5e896dcf9133d"
ORDERS_MATCHED_TOPIC = "0xc4109843e0b7d514e4c093114b863f8e7d8d9a458c372cd51bfe526b588006c9"
ORDER_FULFILLED_TOPIC = "0x9d9af8e38d66c62e2c12f0225249fd9d721c54b83f48d9352c97c6cacdcb6f31"
METHOD_LABELS = {
    "0x4fba84ca": "mintNifty(uint256,uint256)",
    "0x42842e0e": "safeTransferFrom(address,address,uint256)",
    "0xab834bab": "atomicMatch_ (Wyvern 2.3)",
    "0x32389b71": "bulkTransfer (OpenSea TransferHelper)",
    "0x87201b41": "fulfillAvailableAdvancedOrders (Seaport)",
    "0x00000000": "fulfillBasicOrder_efficient_6GL6yc (Seaport)",
    "0xc9dad696": "burnRedeem(address,uint256,uint32,BurnToken[])",
    "0x42b54fee": "burnRedeem(address[],uint256[],uint32[],BurnToken[][])",
}
CONTRACT_LABELS = {
    CONTRACT: "MAX PAIN AND FRENS (NiftyBuilderInstance)",
    common.SEAPORT_1_6: "Seaport 1.6",
    WYVERN_EXCHANGE: "Wyvern Exchange 2.3 (OpenSea)",
    TRANSFER_HELPER: "OpenSea TransferHelper",
    BURN_REDEEM_EXTENSION: "Manifold ERC1155 burn-redeem extension",
    DAMAGE_CONTROL_CONTRACT: "DAMAGE CONTROL (Manifold ERC-1155 creator contract)",
    MAX_PAIN_FEE_HANDLER: "MaxPainFeeHandler",
}
PROVENANCE = (
    ("mint", MINT_TX, MINT_BLOCK),
    ("platform_withdrawal", "0x7df8b1b0da758522d551d23981abb98d85117be1f9c5c3e89161db264a96366d", 14_452_582),
    ("secondary_sale", "0xa941bb0dc42444e50052a7d886c208eb76df798a01595ce8573bf2785bef4935", 14_458_765),
    ("transfer_without_payment", "0x6a1793ad3a5fef87a88bac482a184149d31f3ef6463e5b0bf4e96579b2978bcb", 25_880_116),
    ("secondary_sale", "0x922415bb553845ae9df5289819ce2995988e0ccf5a6cd4c3460971194a98b915", 25_880_430),
    ("agent_purchase", PURCHASE_TX, PURCHASE_BLOCK),
    ("museum_receipt", MUSEUM_RECEIPT_TX, MUSEUM_RECEIPT_BLOCK),
)
VERIFIED_SOURCE_CITATIONS = (
    f"https://etherscan.io/address/{CONTRACT}#code",
    f"https://sourcify.dev/server/v2/contract/1/{CONTRACT}",
)


class Collector:
    """Numbered raw JSON-RPC retention, with hash-only commitments when needed."""

    def __init__(self, output: Path) -> None:
        self.output = output
        self.client = common.RpcClient(USER_AGENT)
        self.sequence = 0
        self.raw_entries: list[dict[str, Any]] = []
        self.commitments: dict[str, list[dict[str, Any]]] = {}

    def rpc(self, label: str, method: str, params: list[Any], *, endpoint: str = PRIMARY_RPC_URL, group: str | None = None, allow_error: bool = False) -> dict[str, Any]:
        call = self.client.call(endpoint, label, method, params)
        response = call["response"]
        if "error" in response and not allow_error:
            raise EvidenceError(f"{label}: {response['error']}")
        self._record(label, call["request_bytes"], call["response_bytes"], call["transport"], group)
        return response

    def batch(self, label: str, requests: list[tuple[str, list[Any]]], *, group: str, endpoint: str = BATCH_RPC_URL) -> list[Any]:
        """Send one JSON-RPC batch; batch responses are committed by hash only."""

        body = [{"jsonrpc": "2.0", "id": index, "method": method, "params": params} for index, (method, params) in enumerate(requests)]
        request_bytes = common.canonical_json(body)
        for attempt in range(len(common.RETRY_DELAYS_SECONDS) + 1):
            time.sleep(self.client.pause_seconds)
            result, attempts = common.fetch(endpoint, method="POST", body=request_bytes, accept="application/json", user_agent=USER_AGENT)
            if result.observation.status != 200:
                raise EvidenceError(f"{label}: HTTP {result.observation.status}")
            decoded = json.loads(result.body.decode("utf-8"))
            if not isinstance(decoded, list):
                raise EvidenceError(f"{label}: batch response is not a list")
            by_id = {row.get("id"): row for row in decoded if isinstance(row, dict)}
            transient = [row for row in by_id.values() if isinstance(row.get("error"), dict)]
            if len(by_id) == len(requests) and not transient:
                transport = result.observation.to_dict()
                transport["endpoint"] = endpoint
                transport["attempts"] = attempts + attempt
                self._record(label, request_bytes, result.body, transport, group)
                return [by_id[index]["result"] for index in range(len(requests))]
            if attempt < len(common.RETRY_DELAYS_SECONDS):
                time.sleep(common.RETRY_DELAYS_SECONDS[attempt])
        raise EvidenceError(f"{label}: batch response incomplete after retries")

    def _record(self, label: str, request_bytes: bytes, response_bytes: bytes, transport: dict[str, Any], group: str | None) -> None:
        self.sequence += 1
        if group is None:
            prefix = f"raw/rpc/{self.sequence:04d}-{label}"
            common.write_bytes(self.output / f"{prefix}-request.json", request_bytes)
            common.write_bytes(self.output / f"{prefix}-response.json", response_bytes)
            self.raw_entries.append(
                {
                    "sequence": self.sequence,
                    "label": label,
                    "request_path": f"{prefix}-request.json",
                    "request_sha256": f"sha256:{common.sha256(request_bytes)}",
                    "response_path": f"{prefix}-response.json",
                    "response_sha256": f"sha256:{common.sha256(response_bytes)}",
                    "response_size": len(response_bytes),
                    "transport": transport,
                }
            )
        else:
            self.commitments.setdefault(group, []).append(
                {
                    "sequence": self.sequence,
                    "label": label,
                    "endpoint": transport["endpoint"],
                    "observed_at": transport["observed_at"],
                    "request_sha256": f"sha256:{common.sha256(request_bytes)}",
                    "request_size": len(request_bytes),
                    "response_sha256": f"sha256:{common.sha256(response_bytes)}",
                    "response_size": len(response_bytes),
                }
            )


    def group_summary(self, group: str, *, include_entries: bool) -> dict[str, Any]:
        rows = self.commitments.get(group, [])
        summary: dict[str, Any] = {
            "group": group,
            "exchange_count": len(rows),
            "endpoints": sorted({row["endpoint"] for row in rows}),
            "first_observed_at": rows[0]["observed_at"] if rows else None,
            "last_observed_at": rows[-1]["observed_at"] if rows else None,
            "total_request_bytes": sum(row["request_size"] for row in rows),
            "total_response_bytes": sum(row["response_size"] for row in rows),
            "aggregate_sha256": f"sha256:{common.sha256(common.canonical_json([[row['label'], row['request_sha256'], row['response_sha256']] for row in rows]))}",
            "aggregate_canonicalization": "sorted-key compact JSON array of [label, request_sha256, response_sha256] in request order",
            "retained": False,
        }
        if include_entries:
            summary["exchanges"] = rows
        return summary


def result_of(response: dict[str, Any], label: str) -> Any:
    if "result" not in response:
        raise EvidenceError(f"{label}: missing result")
    return response["result"]


def block_identity(block: Any, label: str) -> dict[str, Any]:
    if not isinstance(block, dict):
        raise EvidenceError(f"{label}: no block object")
    return {
        "number": common.hex_int(block.get("number"), label),
        "hash": str(block.get("hash", "")).lower(),
        "timestamp": common.iso_from_unix(common.hex_int(block.get("timestamp"), label)),
    }


def eip1967_slot(name: str) -> str:
    value = (int.from_bytes(common.keccak256(name.encode("ascii")), "big") - 1) % (1 << 256)
    return "0x" + f"{value:064x}"


def aggregate3_calldata(token_ids: list[int]) -> str:
    owner_selector = common.selector("ownerOf(uint256)")
    count = len(token_ids)
    offsets = "".join(common.word(count * 32 + index * 192) for index in range(count))
    calls = "".join(
        common.word(CONTRACT) + common.word(1) + common.word(0x60) + common.word(36) + (owner_selector + common.word(token)).ljust(128, "0")
        for token in token_ids
    )
    return "0x" + common.selector("aggregate3((address,bool,bytes)[])") + common.word(0x20) + common.word(count) + offsets + calls


def decode_aggregate3(result: Any, expected: int) -> list[tuple[bool, bytes]]:
    raw = common.hex_bytes(result, "aggregate3 result")
    offset = int.from_bytes(raw[:32], "big")
    count = int.from_bytes(raw[offset : offset + 32], "big")
    if count != expected:
        raise EvidenceError("aggregate3 result count mismatch")
    base = offset + 32
    rows: list[tuple[bool, bytes]] = []
    for index in range(count):
        element = base + int.from_bytes(raw[base + index * 32 : base + index * 32 + 32], "big")
        success = int.from_bytes(raw[element : element + 32], "big")
        data_offset = element + int.from_bytes(raw[element + 32 : element + 64], "big")
        length = int.from_bytes(raw[data_offset : data_offset + 32], "big")
        rows.append((bool(success), raw[data_offset + 32 : data_offset + 32 + length]))
    return rows


def revert_reason(data: bytes) -> str | None:
    if len(data) < 68 or data[:4] != bytes.fromhex("08c379a0"):
        return None
    length = int.from_bytes(data[36:68], "big")
    return data[68 : 68 + length].decode("utf-8", errors="replace")


def abi_dynamic_items(data: bytes, offset: int, words: int) -> list[list[int]]:
    count = int.from_bytes(data[offset : offset + 32], "big")
    return [
        [int.from_bytes(data[offset + 32 + (index * words + position) * 32 : offset + 64 + (index * words + position) * 32], "big") for position in range(words)]
        for index in range(count)
    ]


def decode_order_fulfilled(log: dict[str, Any]) -> dict[str, Any]:
    data = common.hex_bytes(log.get("data"), "OrderFulfilled data")
    offer_offset = int.from_bytes(data[64:96], "big")
    consideration_offset = int.from_bytes(data[96:128], "big")
    offer = abi_dynamic_items(data, offer_offset, 4)
    consideration = abi_dynamic_items(data, consideration_offset, 5)
    return {
        "order_hash": "0x" + data[:32].hex(),
        "offerer": "0x" + str(log["topics"][1]).lower()[-40:],
        "recipient": "0x" + data[44:64].hex(),
        "offer": [{"item_type": row[0], "token": f"0x{row[1]:040x}", "identifier": row[2], "amount": row[3]} for row in offer],
        "consideration": [
            {"item_type": row[0], "token": f"0x{row[1]:040x}", "identifier": row[2], "amount": row[3], "recipient": f"0x{row[4]:040x}"}
            for row in consideration
        ],
    }


class Roles:
    def __init__(self, default_owner: str) -> None:
        self.fixed = {
            ZERO_ADDRESS: "zero_address",
            default_owner: "nifty_gateway_platform_custody",
            AGENT_ADDRESS: "acquisition_agent",
            MUSEUM_ADDRESS: "museum_safe",
            OPENSEA_FEE_RECIPIENT: "opensea_fee_recipient",
        }
        self.holders: dict[str, str] = {}

    def __call__(self, address: str) -> str:
        address = address.lower()
        if address in self.fixed:
            return self.fixed[address]
        if address not in self.holders:
            self.holders[address] = f"prior_holder_{chr(ord('a') + len(self.holders))}"
        return self.holders[address]


def currency(token: str) -> str:
    return {ZERO_ADDRESS: "ETH", WETH: "WETH"}.get(token, f"ERC-20 {token}")


def seaport_payment(orders: list[dict[str, Any]], seller: str, roles: Roles) -> dict[str, Any] | None:
    for order in orders:
        token_items = [item for item in order["offer"] + order["consideration"] if item["token"] == CONTRACT and item["identifier"] == TOKEN_ID]
        if not token_items:
            continue
        fungible_offer = [item for item in order["offer"] if item["item_type"] in (0, 1)]
        fungible_consideration = [item for item in order["consideration"] if item["item_type"] in (0, 1)]
        if fungible_offer:
            gross = sum(item["amount"] for item in fungible_offer)
            token = fungible_offer[0]["token"]
            order_kind = "buyer offer accepted by the token holder"
        else:
            gross = sum(item["amount"] for item in fungible_consideration)
            token = fungible_consideration[0]["token"] if fungible_consideration else ZERO_ADDRESS
            order_kind = "seller listing filled by the buyer"
        fees = [
            {"recipient_role": roles(item["recipient"]), "amount_wei": str(item["amount"]), "currency": currency(item["token"])}
            for item in fungible_consideration
            if item["recipient"].lower() != seller
        ]
        return {
            "order_kind": order_kind,
            "currency": currency(token),
            "gross_amount_wei": str(gross),
            "gross_amount": common.wei_to_eth_string(gross),
            "seller_proceeds_wei": str(gross - sum(int(fee["amount_wei"]) for fee in fees)),
            "fee_items": fees,
            "creator_royalty_item_present": False,
        }
    return None


def acquire(output: Path, target_block: int | None) -> dict[str, Any]:
    common.assert_fixed_identities()
    common.prepare_empty_output(output)
    collector = Collector(output)
    observed_at = common.utc_now()

    if result_of(collector.rpc("chain-id", "eth_chainId", []), "chain id") != "0x1":
        raise EvidenceError("RPC endpoint did not report Ethereum mainnet")
    finality_before = block_identity(result_of(collector.rpc("finality-before", "eth_getBlockByNumber", ["finalized", False]), "finality"), "finality-before")
    target_number = target_block if target_block is not None else finality_before["number"]
    if target_number > finality_before["number"]:
        raise EvidenceError("supplied target block is not finalized at acquisition time")
    target = block_identity(
        result_of(collector.rpc("target-block-before", "eth_getBlockByNumber", [hex(target_number), False]), "target"), "target block"
    )
    selector = {"blockHash": target["hash"], "requireCanonical": True}

    def call(label: str, signature: str, *values: int | str, to: str = CONTRACT, allow_error: bool = False) -> dict[str, Any]:
        return collector.rpc(label, "eth_call", [{"to": to, "data": common.calldata(signature, *values)}, selector], allow_error=allow_error)

    code = common.hex_bytes(result_of(collector.rpc("contract-runtime-code", "eth_getCode", [CONTRACT, selector]), "code"), "runtime code")
    if not code:
        raise EvidenceError("contract runtime bytecode is empty")
    common.write_bytes(output / "derived/contract-runtime-bytecode.hex.txt", ("0x" + code.hex() + "\n").encode("ascii"))
    slots = {}
    for name in ("eip1967.proxy.implementation", "eip1967.proxy.beacon", "eip1967.proxy.admin"):
        slot = eip1967_slot(name)
        value = result_of(collector.rpc(f"storage-{name.rsplit('.', 1)[-1]}", "eth_getStorageAt", [CONTRACT, slot, selector]), name)
        slots[name] = {"slot": slot, "value": str(value).lower(), "is_zero": int(value, 16) == 0}

    identity = {
        "name": common.abi_string(result_of(call("name-call", "name()"), "name"), "name"),
        "symbol": common.abi_string(result_of(call("symbol-call", "symbol()"), "symbol"), "symbol"),
        "creator": common.abi_string(result_of(call("creator-call", "creator()"), "creator"), "creator"),
        "type_count": common.abi_uint(result_of(call("type-count-call", "_typeCount()"), "typeCount"), "typeCount"),
        "mint_count_type_1": common.abi_uint(result_of(call("mint-count-call", "_mintCount(uint256)", 1), "mintCount"), "mintCount"),
        "finalized_type_1": common.abi_bool(result_of(call("get-finalized-call", "_getFinalized(uint256)", 1), "finalized"), "finalized"),
        "default_owner": common.abi_address(result_of(call("default-owner-call", "_defaultOwner()"), "defaultOwner"), "defaultOwner"),
        "top_level_multiplier": common.abi_uint(result_of(call("top-level-multiplier-call", "topLevelMultiplier()"), "top"), "top"),
        "mid_level_multiplier": common.abi_uint(result_of(call("mid-level-multiplier-call", "midLevelMultiplier()"), "mid"), "mid"),
        "supports_erc721": common.abi_bool(result_of(call("supports-erc721-call", "supportsInterface(bytes4)", "80ac58cd".ljust(64, "0")), "erc721"), "erc721"),
        "supports_erc2981": common.abi_bool(result_of(call("supports-erc2981-call", "supportsInterface(bytes4)", "2a55205a".ljust(64, "0")), "erc2981"), "erc2981"),
    }
    token_uri = common.abi_string(result_of(call("token-uri-call", "tokenURI(uint256)", TOKEN_ID), "tokenURI"), "tokenURI")
    token_ipfs_hash = common.abi_string(result_of(call("token-ipfs-hash-call", "tokenIPFSHash(uint256)", TOKEN_ID), "ipfs"), "ipfs")
    token_name = common.abi_string(result_of(call("token-name-call", "tokenName(uint256)", TOKEN_ID), "tokenName"), "tokenName")
    royalty = call("royalty-info-call", "royaltyInfo(uint256,uint256)", TOKEN_ID, 10**18, allow_error=True)
    royalty_receiver = common.abi_address(result_of(call("royalty-receiver-call", "getRoyaltyReceiverByTokenId(uint256)", TOKEN_ID), "royalty"), "royalty receiver")
    owner = common.abi_address(result_of(call("owner-of-call", "ownerOf(uint256)", TOKEN_ID), "ownerOf"), "ownerOf")
    approved = common.abi_address(result_of(call("get-approved-call", "getApproved(uint256)", TOKEN_ID), "getApproved"), "getApproved")
    common.require_museum_address(owner, "ownerOf")
    expected_id = identity["top_level_multiplier"] + identity["mid_level_multiplier"] + 4188
    checks = {
        "name": (identity["name"], "MAX PAIN AND FRENS OPEN EDITION BY XCOPY"),
        "creator": (identity["creator"], "XCOPY"),
        "tokenURI": (token_uri, TOKEN_URI),
        "tokenIPFSHash": (token_ipfs_hash, IMAGE_CID),
        "mint count": (identity["mint_count_type_1"], MINTED_COUNT),
        "type count": (identity["type_count"], 1),
        "token id encoding": (expected_id, TOKEN_ID),
        "first id encoding": (identity["top_level_multiplier"] + identity["mid_level_multiplier"] + 1, FIRST_TOKEN_ID),
        "approval": (approved, ZERO_ADDRESS),
        "supports ERC-721": (identity["supports_erc721"], True),
    }
    for label, (observed, expected) in checks.items():
        if observed != expected:
            raise EvidenceError(f"{label} mismatch: expected {expected!r}, got {observed!r}")
    default_owner = identity["default_owner"]
    default_owner_balance = common.abi_uint(result_of(call("default-owner-balance-call", "balanceOf(address)", default_owner), "balance"), "balance")
    multicall_code = common.hex_bytes(result_of(collector.rpc("multicall3-runtime-code", "eth_getCode", [MULTICALL3, selector]), "multicall"), "multicall")

    # Supply: ownerOf for every minted id at the target block hash.
    owners: dict[int, str] = {}
    nonexistent: list[int] = []
    batches: list[dict[str, Any]] = []
    token_ids = list(range(FIRST_TOKEN_ID, LAST_TOKEN_ID + 1))
    for start in range(0, len(token_ids), SUPPLY_BATCH):
        chunk = token_ids[start : start + SUPPLY_BATCH]
        label = f"supply-scan-{chunk[0]}-{chunk[-1]}"
        response = collector.rpc(label, "eth_call", [{"to": MULTICALL3, "data": aggregate3_calldata(chunk)}, selector], group="supply-scan")
        result = result_of(response, label)
        for token, (success, data) in zip(chunk, decode_aggregate3(result, len(chunk))):
            if success:
                if len(data) != 32 or any(data[:12]):
                    raise EvidenceError(f"ownerOf({token}) returned a malformed address")
                owners[token] = "0x" + data[12:].hex()
            elif revert_reason(data) == NONEXISTENT_REVERT:
                nonexistent.append(token)
            else:
                raise EvidenceError(f"ownerOf({token}) failed with an unexpected revert")
        batches.append({"first_token_id": chunk[0], "last_token_id": chunk[-1], "call_count": len(chunk), "result_sha256": f"sha256:{common.sha256(result.encode('ascii'))}"})
    owner_counts = Counter(owners.values())
    if owners.get(TOKEN_ID) != MUSEUM_ADDRESS:
        raise EvidenceError("supply scan disagrees with the direct ownerOf read")
    supply = {
        "method": f"Multicall3 aggregate3 at {MULTICALL3} with allowFailure true; ownerOf(uint256) for every id {FIRST_TOKEN_ID}..{LAST_TOKEN_ID}, {SUPPLY_BATCH} per call, at the target block hash",
        "multicall3_runtime_sha256": f"sha256:{common.sha256(multicall_code)}",
        "minted_count_onchain": identity["mint_count_type_1"],
        "scanned_id_count": len(token_ids),
        "existing_count": len(owners),
        "nonexistent_count": len(nonexistent),
        "nonexistent_revert_reason": NONEXISTENT_REVERT,
        "nonexistent_token_ids": nonexistent,
        "distinct_owner_count": len(owner_counts),
        "held_by_museum_safe": owner_counts.get(MUSEUM_ADDRESS, 0),
        "held_by_nifty_gateway_platform_custody": owner_counts.get(default_owner, 0),
        "nifty_gateway_platform_custody_balance_of": default_owner_balance,
        "owner_map_sha256": f"sha256:{common.sha256(common.canonical_json({str(key): value for key, value in sorted(owners.items())}))}",
        "owner_map_canonicalization": "sorted-key compact JSON object mapping decimal token id to lowercase owner address",
        "batches": batches,
        "raw_retention": "The aggregate3 requests and responses (about 0.4 MB each) are committed by SHA-256 in raw_commitments.supply_scan and are not retained; they are reproducible at the recorded block hash on an archive node.",
    }
    if supply["held_by_nifty_gateway_platform_custody"] != default_owner_balance:
        raise EvidenceError("platform custody count differs from balanceOf")

    # Provenance of #4188: every transfer of the token, decoded into roles.
    roles = Roles(default_owner)
    provenance: list[dict[str, Any]] = []
    for index, (kind, tx_hash, block_number) in enumerate(PROVENANCE):
        tx = result_of(collector.rpc(f"provenance-{index:02d}-transaction", "eth_getTransactionByHash", [tx_hash]), "tx")
        receipt = result_of(collector.rpc(f"provenance-{index:02d}-receipt", "eth_getTransactionReceipt", [tx_hash]), "receipt")
        block = block_identity(result_of(collector.rpc(f"provenance-{index:02d}-block", "eth_getBlockByNumber", [hex(block_number), False]), "block"), "block")
        receipt_path = collector.raw_entries[-2]["response_path"]
        if not isinstance(tx, dict) or not isinstance(receipt, dict) or receipt.get("status") != "0x1":
            raise EvidenceError(f"provenance transaction {tx_hash} is missing or failed")
        if common.hex_int(receipt.get("blockNumber"), "block") != block_number or str(receipt.get("blockHash", "")).lower() != block["hash"]:
            raise EvidenceError(f"provenance transaction {tx_hash} block mismatch")
        selector_hex = str(tx.get("input", "0x"))[:10]
        event: dict[str, Any] = {
            "sequence": index,
            "kind": kind,
            "transaction_hash": tx_hash,
            "block_number": block_number,
            "block_hash": block["hash"],
            "time": block["timestamp"],
            "transaction_to_contract": CONTRACT_LABELS.get(str(tx.get("to", "")).lower(), "unlabelled contract"),
            "method_selector": selector_hex,
            "method": METHOD_LABELS.get(selector_hex, "unlabelled selector"),
            "transaction_value_wei": str(common.hex_int(tx.get("value"), "value")),
            "receipt_status": "0x1",
            "receipt_path": receipt_path,
            "verification": "direct_rpc_verified",
        }
        if kind == "mint":
            consecutive = [
                log
                for log in receipt.get("logs", [])
                if str(log.get("address", "")).lower() == CONTRACT and str(log["topics"][0]).lower() == CONSECUTIVE_TRANSFER_TOPIC
            ]
            if len(consecutive) != 1:
                raise EvidenceError("mint receipt does not hold exactly one ConsecutiveTransfer event")
            log = consecutive[0]
            first = int(log["topics"][1], 16)
            last = common.abi_uint(log["data"], "toTokenId")
            to = "0x" + str(log["topics"][3]).lower()[-40:]
            if not first <= TOKEN_ID <= last or int(log["topics"][2], 16) != 0 or to != default_owner:
                raise EvidenceError("mint ConsecutiveTransfer does not cover #4188 into platform custody")
            if str(tx.get("from", "")).lower() != NIFTY_GATEWAY_MINTER_KEY:
                raise EvidenceError("mint transaction sender is not the recorded Nifty Gateway minting key")
            event.update(
                {
                    "token_event": "ConsecutiveTransfer(uint256,uint256,address,address) (EIP-2309)",
                    "log_index": common.hex_int(log.get("logIndex"), "logIndex"),
                    "token_range": [first, last],
                    "from_role": "zero_address",
                    "to_role": roles(to),
                    "sender_role": "nifty_gateway_minting_key",
                    "payment": None,
                    "payment_note": "Primary sale settled off-chain by Nifty Gateway; no on-chain payment in the mint.",
                }
            )
        else:
            matches = [common.decoded_transfer(log) for log in common.transfer_logs(receipt) if int(str(log["topics"][3]), 16) == TOKEN_ID]
            if len(matches) != 1:
                raise EvidenceError(f"{tx_hash} does not hold exactly one Transfer of #4188")
            transfer = matches[0]
            event.update(
                {
                    "token_event": "Transfer(address,address,uint256)",
                    "log_index": transfer["log_index"],
                    "from_role": roles(transfer["from"]),
                    "to_role": roles(transfer["to"]),
                    "address_refs": {
                        "from": {"path": receipt_path, "log_index": transfer["log_index"], "topic_index": 1},
                        "to": {"path": receipt_path, "log_index": transfer["log_index"], "topic_index": 2},
                    },
                    "erc721_token_transfers_in_transaction": len(common.transfer_logs(receipt)),
                }
            )
            payment: dict[str, Any] | None = None
            if selector_hex == "0xab834bab":
                matched = [log for log in receipt.get("logs", []) if str(log["topics"][0]).lower() == ORDERS_MATCHED_TOPIC and str(log.get("address", "")).lower() == WYVERN_EXCHANGE]
                if len(matched) != 1:
                    raise EvidenceError("Wyvern sale lacks exactly one OrdersMatched event")
                price = int.from_bytes(common.hex_bytes(matched[0]["data"], "OrdersMatched")[64:96], "big")
                payment = {
                    "order_kind": "Wyvern atomic match",
                    "currency": "ETH",
                    "gross_amount_wei": str(price),
                    "gross_amount": common.wei_to_eth_string(price),
                    "fee_split_note": "The marketplace fee split was paid by internal transfers that receipts do not show; it is not asserted here.",
                }
                if str(price) != event["transaction_value_wei"]:
                    raise EvidenceError("Wyvern matched price differs from the transaction value")
            elif str(tx.get("to", "")).lower() == common.SEAPORT_1_6:
                orders = [decode_order_fulfilled(log) for log in receipt.get("logs", []) if str(log["topics"][0]).lower() == ORDER_FULFILLED_TOPIC]
                payment = seaport_payment(orders, transfer["from"], roles)
                if payment is None:
                    raise EvidenceError(f"{tx_hash}: no Seaport order moves #4188")
            event["payment"] = payment
            event["venue"] = {
                "0xab834bab": "OpenSea (Wyvern 2.3)",
                "0x32389b71": "OpenSea TransferHelper (no payment)",
                "0x87201b41": "OpenSea (Seaport 1.6)",
                "0x00000000": "OpenSea (Seaport 1.6)",
                "0x42842e0e": "direct contract transfer",
            }.get(selector_hex, "unlabelled")
        provenance.append(event)
    chain_ok = all(provenance[index]["to_role"] == provenance[index + 1]["from_role"] for index in range(len(provenance) - 1))
    if not chain_ok or provenance[-1]["to_role"] != "museum_safe":
        raise EvidenceError("provenance chain is not continuous into the Museum Safe")

    # Burns: complete Transfer(to = 0) log scan, then each transaction's target.
    burn_logs: list[dict[str, Any]] = []
    nonempty_windows: list[dict[str, Any]] = []
    for start in range(FIRST_MINT_BLOCK, target_number + 1, SCAN_WINDOW_BLOCKS):
        end = min(start + SCAN_WINDOW_BLOCKS - 1, target_number)
        response = collector.rpc(
            f"burn-log-scan-{start}-{end}",
            "eth_getLogs",
            [{"address": CONTRACT, "topics": [TRANSFER_TOPIC, None, common.address_topic(ZERO_ADDRESS)], "fromBlock": hex(start), "toBlock": hex(end)}],
            endpoint=BATCH_RPC_URL,
            group="burn-log-scan",
        )
        window_logs = result_of(response, "getLogs")
        if window_logs:
            nonempty_windows.append(
                {
                    "from_block": start,
                    "to_block": end,
                    "burn_log_count": len(window_logs),
                    "response_sha256": collector.commitments["burn-log-scan"][-1]["response_sha256"],
                }
            )
        for log in window_logs:
            if str(log.get("address", "")).lower() != CONTRACT or len(log.get("topics", [])) != 4:
                raise EvidenceError("burn log scan returned an unexpected log")
            burn_logs.append(
                {
                    "token_id": int(log["topics"][3], 16),
                    "transaction_hash": str(log["transactionHash"]).lower(),
                    "block_number": common.hex_int(log["blockNumber"], "log block"),
                }
            )
    burned_ids = sorted(row["token_id"] for row in burn_logs)
    if len(burned_ids) != len(set(burned_ids)):
        raise EvidenceError("a token id was burned twice")
    transactions = sorted({row["transaction_hash"] for row in burn_logs})
    tx_facts: dict[str, dict[str, Any]] = {}
    for start in range(0, len(transactions), TX_BATCH):
        chunk = transactions[start : start + TX_BATCH]
        results = collector.batch(f"burn-transactions-{start:05d}", [("eth_getTransactionByHash", [tx]) for tx in chunk], group="burn-transactions")
        for tx_hash, tx in zip(chunk, results):
            if not isinstance(tx, dict) or str(tx.get("hash", "")).lower() != tx_hash:
                raise EvidenceError(f"burn transaction lookup failed: {tx_hash}")
            tx_facts[tx_hash] = {
                "to": str(tx.get("to", "")).lower(),
                "selector": str(tx.get("input", "0x"))[:10],
                "time": common.iso_from_unix(common.hex_int(tx["blockTimestamp"], "blockTimestamp")) if tx.get("blockTimestamp") else None,
            }
    mechanism = Counter()
    mechanism_txs: dict[tuple[str, str], set[str]] = {}
    months = Counter()
    for row in burn_logs:
        facts = tx_facts[row["transaction_hash"]]
        key = (facts["to"], facts["selector"])
        mechanism[key] += 1
        mechanism_txs.setdefault(key, set()).add(row["transaction_hash"])
        if facts["time"]:
            months[facts["time"][:7]] += 1
    via_extension = sum(count for (to, _), count in mechanism.items() if to == BURN_REDEEM_EXTENSION)
    other_txs = sorted(tx for (to, _), txs in mechanism_txs.items() if to != BURN_REDEEM_EXTENSION for tx in txs)
    samples: list[str] = []
    for selector_hex in ("0xc9dad696", "0x42b54fee"):
        candidates = sorted(
            (row["block_number"], row["transaction_hash"])
            for row in burn_logs
            if tx_facts[row["transaction_hash"]]["to"] == BURN_REDEEM_EXTENSION and tx_facts[row["transaction_hash"]]["selector"] == selector_hex
        )
        if candidates:
            samples.append(candidates[0][1])
    samples.extend(other_txs)
    sample_records = []
    for index, tx_hash in enumerate(samples):
        receipt = result_of(collector.rpc(f"burn-sample-{index:02d}-receipt", "eth_getTransactionReceipt", [tx_hash]), "receipt")
        emitters = sorted({str(log.get("address", "")).lower() for log in receipt.get("logs", [])})
        sample_records.append(
            {
                "transaction_hash": tx_hash,
                "receipt_path": collector.raw_entries[-1]["response_path"],
                "transaction_to": CONTRACT_LABELS.get(tx_facts[tx_hash]["to"], "unlabelled contract"),
                "method_selector": tx_facts[tx_hash]["selector"],
                "method": METHOD_LABELS.get(tx_facts[tx_hash]["selector"], "unlabelled selector"),
                "log_emitters": [{"address": address, "label": CONTRACT_LABELS.get(address, "unlabelled contract")} for address in emitters],
                "max_pain_fee_handler_emitted_logs": MAX_PAIN_FEE_HANDLER in emitters,
            }
        )
    burns = {
        "method": (
            f"eth_getLogs on {BATCH_RPC_URL} for Transfer(address,address,uint256) logs of the contract with to = 0x0, "
            f"in {SCAN_WINDOW_BLOCKS}-block windows from block {FIRST_MINT_BLOCK} (first mint) to the target block; then "
            "eth_getTransactionByHash for every burn transaction (JSON-RPC batches)."
        ),
        "scan_window_count": len(range(FIRST_MINT_BLOCK, target_number + 1, SCAN_WINDOW_BLOCKS)),
        "windows_with_burns": nonempty_windows,
        "burn_log_count": len(burn_logs),
        "burn_transaction_count": len(transactions),
        "burned_token_ids_equal_ownerOf_nonexistent_ids": burned_ids == sorted(nonexistent),
        "by_transaction_target": [
            {
                "transaction_to": to,
                "label": CONTRACT_LABELS.get(to, "unlabelled contract"),
                "method_selector": selector_hex,
                "method": METHOD_LABELS.get(selector_hex, "unlabelled selector"),
                "burns": count,
                "transactions": len(mechanism_txs[(to, selector_hex)]),
            }
            for (to, selector_hex), count in sorted(mechanism.items(), key=lambda item: (-item[1], item[0]))
        ],
        "burns_via_manifold_burn_redeem_extension": via_extension,
        "burns_in_other_transactions": len(burn_logs) - via_extension,
        "burns_by_month": dict(sorted(months.items())),
        "first_burn_block": min((row["block_number"] for row in burn_logs), default=None),
        "last_burn_block": max((row["block_number"] for row in burn_logs), default=None),
        "sample_receipts": sample_records,
        "evidence_class": "A (derived from retained commitments; per-transaction raw responses are not retained because they carry burners' wallet addresses)",
        "interpretation_boundary": (
            "Counts attribute burns by the transaction's destination contract and method. Which DAMAGE CONTROL redemption "
            "each burn served, and the program terms, are not decoded here and remain research findings."
        ),
    }
    if not burns["burned_token_ids_equal_ownerOf_nonexistent_ids"]:
        raise EvidenceError("burn log scan and ownerOf scan disagree")

    finality_after = block_identity(result_of(collector.rpc("finality-after", "eth_getBlockByNumber", ["finalized", False]), "finality"), "finality-after")
    if finality_after["number"] < target_number:
        raise EvidenceError("target block is no longer finalized")
    target_after = block_identity(result_of(collector.rpc("target-block-after", "eth_getBlockByNumber", [hex(target_number), False]), "target"), "target block after")
    if target_after != target:
        raise EvidenceError("target block identity changed during acquisition")

    observation = {
        "record_id": RECORD_ID,
        "record_type": "XCOPY_MAX_PAIN_4188_ONCHAIN_TECHNICAL_OBSERVATION",
        "observed_at": observed_at,
        "accession_id": ACCESSION_ID,
        "object_id": common.OBJECT_ID,
        "network": "Ethereum mainnet",
        "chain_id": 1,
        "rpc_endpoint": PRIMARY_RPC_URL,
        "batch_rpc_endpoint": BATCH_RPC_URL,
        "contract": CONTRACT,
        "token_id": TOKEN_ID,
        "caip19": CAIP19,
        "finalized_block": {**target, "state_selector": selector},
        "finality_observation": {"before": finality_before, "after": finality_after, "target_was_finalized_before_and_after": True},
        "runtime_bytecode": {
            "path": "derived/contract-runtime-bytecode.hex.txt",
            "encoding": "hexadecimal text with 0x prefix",
            "decoded_size": len(code),
            "sha256": f"sha256:{common.sha256(code)}",
            "keccak256": "0x" + common.keccak256(code).hex(),
        },
        "eip1967_slots": slots,
        "contract_identity": identity,
        "token": {
            "token_id": TOKEN_ID,
            "token_uri": token_uri,
            "token_ipfs_hash": token_ipfs_hash,
            "token_name_override": token_name,
            "token_id_encoding": "topLevelMultiplier + niftyType * midLevelMultiplier + tokenNumber = 171000000000 + 1 * 100000 + 4188",
            "owner": owner,
            "approved": approved,
            "royalty_info": {"reverted": "error" in royalty, "revert": royalty.get("error"), "royalty_receiver_by_token": royalty_receiver},
        },
        "verified_source": {
            "status": "cited_not_retained",
            "contract_name": "NiftyBuilderInstance",
            "citations": list(VERIFIED_SOURCE_CITATIONS),
            "evidence_class": "D (block-explorer and verifier attestation); the runtime bytecode above is class A",
            "precedent": "Vera Molnar technical research cites the verified contract source by URL",
        },
        "metadata_mutability": {
            "token_uri": "tokenURI is _baseURI + decimal token id. The verified source lets Nifty Gateway registry-authorized senders replace _baseURI (setBaseURI), so the tokenURI location is administratively mutable.",
            "token_ipfs_hash": "tokenIPFSHash is stored per nifty type and the verified source sets it once (setNiftyIPFSHash requires an empty value); it is set to the image CID at this block.",
            "token_name": "setNiftyName can change the nifty type name; tokenName for #4188 returns the observed value above.",
            "further_minting": f"_getFinalized(1) is {identity['finalized_type_1']} at this block, so registry-authorized senders could mint more type-1 tokens; _mintCount(1) is {identity['mint_count_type_1']}.",
            "basis": "Function behaviour from the cited verified source (class D); state values from the retained calls (class A).",
        },
        "supply": supply,
        "provenance": {
            "events": provenance,
            "continuous_from_mint_to_museum_safe": True,
            "private_address_boundary": "Prior holders are labelled by role. Their addresses appear only in the retained raw receipts (see address_refs), for use in a provenance schedule; they are not repeated in derived text.",
            "known_role_addresses": {"nifty_gateway_platform_custody": default_owner, "acquisition_agent": AGENT_ADDRESS, "museum_safe": MUSEUM_ADDRESS, "opensea_fee_recipient": OPENSEA_FEE_RECIPIENT},
        },
        "burns": burns,
        "raw_json_rpc": collector.raw_entries,
        "raw_commitments": {
            "supply_scan": collector.group_summary("supply-scan", include_entries=True),
            "burn_log_scan": collector.group_summary("burn-log-scan", include_entries=False),
            "burn_transactions": collector.group_summary("burn-transactions", include_entries=True),
            "boundary": "These exchanges are committed by SHA-256 only: the supply-scan responses are large, and the burn log and burn transaction responses carry burners' wallet addresses. Every request is reproducible from this script at the recorded block range or hash.",
        },
        "assertions": {
            "chain_id_is_ethereum_mainnet": True,
            "target_block_finalized_and_unchanged": True,
            "token_uri_and_ipfs_hash_match": True,
            "minted_count_is_7394": True,
            "owner_matches_museum": True,
            "getApproved_is_zero": True,
            "provenance_chain_continuous": True,
            "burn_logs_equal_nonexistent_ids": True,
        },
        "limitations": [
            "This package proves the observed on-chain technical state, supply, provenance transfers and burns only.",
            "It does not establish legal title, copyright, the meaning of edition counts on third-party sites, or the terms of any sale or redemption program.",
            "Marketplace and venue labels identify the contracts called; off-chain order books and fee agreements are not observed.",
        ],
    }
    observation_bytes = common.pretty_json(observation)
    common.write_bytes(output / "derived/observation.json", observation_bytes)

    entries: list[dict[str, Any]] = []
    for path in sorted(output.rglob("*")):
        if not path.is_file() or path.name in {"manifest.json", "summary.json"}:
            continue
        media_type = {".json": "application/json", ".txt": "text/plain"}.get(path.suffix.lower())
        if media_type is None:
            raise EvidenceError(f"technical evidence media type is not declared: {path}")
        entries.append(common.entry_for(output, path, media_type))
    package_content_sha256 = common.sha256(common.canonical_json(entries))
    manifest = {
        "schema": "6529-museum-technical-evidence-manifest-v1",
        "manifest_type": "6529NM_XCOPY_MAX_PAIN_4188_TECHNICAL_EVIDENCE",
        "hash_algorithm": "sha256",
        "byte_mode": "raw",
        "record_id": RECORD_ID,
        "subject_id": common.OBJECT_ID,
        "finalized_block": observation["finalized_block"],
        "contract": CONTRACT,
        "token_id": TOKEN_ID,
        "package_content_sha256": f"sha256:{package_content_sha256}",
        "entries": entries,
    }
    manifest_bytes = common.pretty_json(manifest)
    common.write_bytes(output / "manifest.json", manifest_bytes)
    summary = {
        "record_id": RECORD_ID,
        "manifest": "manifest.json",
        "manifest_sha256": f"sha256:{common.sha256(manifest_bytes)}",
        "package_content_sha256": f"sha256:{package_content_sha256}",
        "observation": observation,
    }
    summary_bytes = common.pretty_json(summary)
    common.write_bytes(output / "summary.json", summary_bytes)
    return {
        "status": "complete",
        "record_id": RECORD_ID,
        "finalized_block": target,
        "summary_sha256": f"sha256:{common.sha256(summary_bytes)}",
        "manifest_sha256": f"sha256:{common.sha256(manifest_bytes)}",
        "package_content_sha256": f"sha256:{package_content_sha256}",
        "file_count": len(entries),
        "retained_rpc_exchanges": len(collector.raw_entries),
        "committed_unretained_exchanges": sum(len(rows) for rows in collector.commitments.values()),
        "existing": len(owners),
        "nonexistent": len(nonexistent),
        "burns_via_extension": via_extension,
        "burns_other": len(burn_logs) - via_extension,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--output-dir", type=Path, default=common.ROOT / "evidence" / "xcopy-max-pain-4188-technical")
    parser.add_argument("--block", type=int, help="finalized target block number; defaults to the current finalized block")
    args = parser.parse_args(argv)
    started = datetime.now(UTC)
    try:
        result = acquire(args.output_dir.absolute(), args.block)
    except (EvidenceError, FetchPolicyError, OSError, ValueError, KeyError) as exc:
        print(f"MAX PAIN technical evidence acquisition refused: {exc}", file=sys.stderr)
        return 1
    result["elapsed_seconds"] = round((datetime.now(UTC) - started).total_seconds(), 1)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
