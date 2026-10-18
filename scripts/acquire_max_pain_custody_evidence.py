#!/usr/bin/env python3
"""Acquire exact-finalized-block custody evidence for MAX PAIN #4188/7394.

The package binds accession object ``6529NM.2026.005.01`` to one finalized
Ethereum block.  It retains the exact JSON-RPC response bytes for:

* the chain id and the finalized block, read before and after the window;
* the Museum receipt transaction, its receipt and its block, with exactly one
  ERC-721 ``Transfer`` of token 171000104188 at log 955 from the acquisition
  agent to the Museum Safe;
* ``ownerOf`` and ``getApproved`` at the finalized block hash (EIP-1898,
  ``requireCanonical``), on two independent keyless providers;
* ENS ``resolver`` and ``addr`` for ``networkmuseum.6529.eth`` at that hash;
* the agent's Seaport purchase transaction and the later residual ETH transfer
  to the Museum Safe, each with its receipt and block, as history reads.

Prior private holders' addresses appear only inside the retained raw receipts;
the summary records roles, log indices and transaction facts.  This is an
evidence acquisition tool, not a title, rights, acceptance or accession
decision, and it does not accept the residual ETH.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any

from safe_fetch import FetchPolicyError

import max_pain_evidence_common as common
from max_pain_evidence_common import (
    ACCESSION_ID,
    AGENT_ADDRESS,
    CAIP19,
    CONTRACT,
    ENS_NAME,
    ENS_NAMEHASH,
    ENS_REGISTRY,
    EvidenceError,
    MUSEUM_ADDRESS,
    MUSEUM_CHECKSUM_ADDRESS,
    MUSEUM_RECEIPT_BLOCK,
    MUSEUM_RECEIPT_LOG_INDEX,
    MUSEUM_RECEIPT_TX,
    OBJECT_ID,
    PRIMARY_RPC_URL,
    PURCHASE_BLOCK,
    PURCHASE_TRANSFER_LOG_INDEX,
    PURCHASE_TX,
    PURCHASE_VALUE_WEI,
    RESIDUAL_BLOCK,
    RESIDUAL_TX,
    RESIDUAL_VALUE_WEI,
    SEAPORT_1_6,
    SECOND_RPC_URL,
    TOKEN_ID,
    ZERO_ADDRESS,
)


USER_AGENT = "6529-Network-Museum/xcopy-max-pain-4188-custody-audit-v1"
RECORD_ID = f"{ACCESSION_ID}.CUSTODY-EVIDENCE-01"
ORDER_FULFILLED_TOPIC = "0x9d9af8e38d66c62e2c12f0225249fd9d721c54b83f48d9352c97c6cacdcb6f31"
# keccak256("SafeReceived(address,uint256)"), emitted by the Museum Safe when it receives ETH.
SAFE_RECEIVED_TOPIC = "0x3d0ce9bfc3ed7d6862dbb28b2dea94561fe714a1b4d019aa8af39730d1ad7c3d"


class Package:
    def __init__(self, output: Path) -> None:
        self.output = output
        self.client = common.RpcClient(USER_AGENT)
        self.raw_entries: list[dict[str, Any]] = []

    def call(self, category: str, endpoint: str, request_id: str, method: str, params: list[Any]) -> Any:
        call = self.client.call(endpoint, request_id, method, params)
        digest = common.sha256(call["response_bytes"])
        relative = Path("raw") / category / f"sha256-{digest}.json"
        target = self.output / relative
        if target.exists() and target.read_bytes() != call["response_bytes"]:
            raise EvidenceError(f"content-addressed path collision: {relative.as_posix()}")
        common.write_bytes(target, call["response_bytes"])
        self.raw_entries.append(
            {
                "category": category,
                "path": relative.as_posix(),
                "sha256": f"sha256:{digest}",
                "size": len(call["response_bytes"]),
                "request_id": request_id,
                "request_sha256": f"sha256:{common.sha256(call['request_bytes'])}",
                "request_size": len(call["request_bytes"]),
                "request_canonicalization": "sorted-key compact JSON",
                "media_type": "application/json",
                "byte_mode": "raw",
                "transport": call["transport"],
            }
        )
        return common.require_result(call, request_id)


def block_identity(block: Any, label: str) -> dict[str, Any]:
    if not isinstance(block, dict):
        raise EvidenceError(f"{label} did not return a block object")
    number = common.hex_int(block.get("number"), f"{label} number")
    block_hash = str(block.get("hash", "")).lower()
    if len(block_hash) != 66:
        raise EvidenceError(f"{label} hash is malformed")
    timestamp = common.iso_from_unix(common.hex_int(block.get("timestamp"), f"{label} timestamp"))
    return {"number": number, "hash": block_hash, "timestamp": timestamp}


def verify_transaction(tx: Any, *, label: str, tx_hash: str, sender: str, recipient: str, value: int, nonce: int, block: int) -> dict[str, Any]:
    if not isinstance(tx, dict):
        raise EvidenceError(f"{label} transaction is missing")
    checks = {
        "hash": (str(tx.get("hash", "")).lower(), tx_hash),
        "from": (str(tx.get("from", "")).lower(), sender),
        "to": (str(tx.get("to", "")).lower(), recipient),
        "value": (common.hex_int(tx.get("value"), f"{label} value"), value),
        "nonce": (common.hex_int(tx.get("nonce"), f"{label} nonce"), nonce),
        "block": (common.hex_int(tx.get("blockNumber"), f"{label} block"), block),
    }
    for field, (observed, expected) in checks.items():
        if observed != expected:
            raise EvidenceError(f"{label} transaction {field} mismatch: expected {expected!r}, got {observed!r}")
    return {
        "transaction_hash": tx_hash,
        "from": sender,
        "to": recipient,
        "value_wei": str(value),
        "value_eth": common.wei_to_eth_string(value),
        "nonce": nonce,
        "input_selector": str(tx.get("input", "0x"))[:10],
        "block_hash_reported": str(tx.get("blockHash", "")).lower() or None,
    }


def verify_receipt(receipt: Any, *, label: str, tx_hash: str, block: int) -> dict[str, Any]:
    if not isinstance(receipt, dict):
        raise EvidenceError(f"{label} receipt is missing")
    if str(receipt.get("transactionHash", "")).lower() != tx_hash:
        raise EvidenceError(f"{label} receipt hash mismatch")
    if receipt.get("status") != "0x1":
        raise EvidenceError(f"{label} receipt status is not success")
    if common.hex_int(receipt.get("blockNumber"), f"{label} receipt block") != block:
        raise EvidenceError(f"{label} receipt block mismatch")
    return receipt


def acquire(output: Path) -> dict[str, Any]:
    common.assert_fixed_identities()
    common.prepare_empty_output(output)
    package = Package(output)
    observed_at = common.utc_now()

    if package.call("chain", PRIMARY_RPC_URL, "chain-id", "eth_chainId", []) != "0x1":
        raise EvidenceError("primary RPC endpoint did not report Ethereum mainnet")
    finalized = block_identity(
        package.call("finalized-block", PRIMARY_RPC_URL, "finalized-block", "eth_getBlockByNumber", ["finalized", False]),
        "finalized block",
    )
    if finalized["number"] <= RESIDUAL_BLOCK:
        raise EvidenceError("finalized block precedes the residual transfer")
    selector = {"blockHash": finalized["hash"], "requireCanonical": True}

    # Museum receipt: the custody transfer into the ENS-resolved Museum Safe.
    receipt_tx = verify_transaction(
        package.call("museum-receipt-transaction", PRIMARY_RPC_URL, "museum-receipt-transaction", "eth_getTransactionByHash", [MUSEUM_RECEIPT_TX]),
        label="museum receipt",
        tx_hash=MUSEUM_RECEIPT_TX,
        sender=AGENT_ADDRESS,
        recipient=CONTRACT,
        value=0,
        nonce=1,
        block=MUSEUM_RECEIPT_BLOCK,
    )
    receipt = verify_receipt(
        package.call("museum-receipt", PRIMARY_RPC_URL, "museum-receipt", "eth_getTransactionReceipt", [MUSEUM_RECEIPT_TX]),
        label="museum receipt",
        tx_hash=MUSEUM_RECEIPT_TX,
        block=MUSEUM_RECEIPT_BLOCK,
    )
    receipt_transfers = [common.decoded_transfer(log) for log in common.transfer_logs(receipt)]
    if len(receipt_transfers) != 1:
        raise EvidenceError(f"museum receipt contains {len(receipt_transfers)} token Transfer logs, expected 1")
    transfer = receipt_transfers[0]
    if transfer != {"log_index": MUSEUM_RECEIPT_LOG_INDEX, "from": AGENT_ADDRESS, "to": MUSEUM_ADDRESS, "token_id": TOKEN_ID}:
        raise EvidenceError(f"museum receipt Transfer log mismatch: {transfer}")
    common.require_museum_address(transfer["to"], "museum receipt Transfer recipient")
    receipt_block = block_identity(
        package.call("museum-receipt-block", PRIMARY_RPC_URL, "museum-receipt-block", "eth_getBlockByNumber", [hex(MUSEUM_RECEIPT_BLOCK), False]),
        "museum receipt block",
    )
    if receipt_block["number"] != MUSEUM_RECEIPT_BLOCK or receipt_block["hash"] != str(receipt.get("blockHash", "")).lower():
        raise EvidenceError("museum receipt block hash does not match the receipt")

    # Current custody at the exact finalized block hash.
    owner = common.abi_address(
        package.call("owner", PRIMARY_RPC_URL, "owner-of", "eth_call", [{"to": CONTRACT, "data": common.calldata("ownerOf(uint256)", TOKEN_ID)}, selector]),
        "ownerOf",
    )
    common.require_museum_address(owner, "ownerOf")
    approved = common.abi_address(
        package.call("approval", PRIMARY_RPC_URL, "get-approved", "eth_call", [{"to": CONTRACT, "data": common.calldata("getApproved(uint256)", TOKEN_ID)}, selector]),
        "getApproved",
    )
    resolver = common.abi_address(
        package.call("ens", PRIMARY_RPC_URL, "ens-resolver", "eth_call", [{"to": ENS_REGISTRY, "data": common.calldata("resolver(bytes32)", ENS_NAMEHASH)}, selector]),
        "ENS resolver",
    )
    if resolver == ZERO_ADDRESS:
        raise EvidenceError("ENS registry returned the zero resolver")
    ens_address = common.abi_address(
        package.call("ens", PRIMARY_RPC_URL, "ens-address", "eth_call", [{"to": resolver, "data": common.calldata("addr(bytes32)", ENS_NAMEHASH)}, selector]),
        "ENS addr",
    )
    common.require_museum_address(ens_address, f"{ENS_NAME} addr")

    # Independent second provider at the same block hash.
    if package.call("chain", SECOND_RPC_URL, "second-chain-id", "eth_chainId", []) != "0x1":
        raise EvidenceError("second RPC endpoint did not report Ethereum mainnet")
    second_block = block_identity(
        package.call("second-provider-block", SECOND_RPC_URL, "second-finalized-block-by-hash", "eth_getBlockByHash", [finalized["hash"], False]),
        "second provider finalized block",
    )
    if second_block != finalized:
        raise EvidenceError("second provider does not report the same finalized block")
    second_owner = common.abi_address(
        package.call("second-provider-owner", SECOND_RPC_URL, "second-owner-of", "eth_call", [{"to": CONTRACT, "data": common.calldata("ownerOf(uint256)", TOKEN_ID)}, selector]),
        "second provider ownerOf",
    )
    common.require_museum_address(second_owner, "second provider ownerOf")

    # History reads: the agent's purchase and the later residual transfer.
    purchase_tx = verify_transaction(
        package.call("purchase-transaction", PRIMARY_RPC_URL, "purchase-transaction", "eth_getTransactionByHash", [PURCHASE_TX]),
        label="purchase",
        tx_hash=PURCHASE_TX,
        sender=AGENT_ADDRESS,
        recipient=SEAPORT_1_6,
        value=PURCHASE_VALUE_WEI,
        nonce=0,
        block=PURCHASE_BLOCK,
    )
    purchase_receipt = verify_receipt(
        package.call("purchase-receipt", PRIMARY_RPC_URL, "purchase-receipt", "eth_getTransactionReceipt", [PURCHASE_TX]),
        label="purchase",
        tx_hash=PURCHASE_TX,
        block=PURCHASE_BLOCK,
    )
    purchase_transfers = [common.decoded_transfer(log) for log in common.transfer_logs(purchase_receipt)]
    if len(purchase_transfers) != 1:
        raise EvidenceError(f"purchase receipt contains {len(purchase_transfers)} token Transfer logs, expected 1")
    bought = purchase_transfers[0]
    if (
        bought["log_index"] != PURCHASE_TRANSFER_LOG_INDEX
        or bought["to"] != AGENT_ADDRESS
        or bought["token_id"] != TOKEN_ID
        or bought["from"] in {ZERO_ADDRESS, AGENT_ADDRESS, MUSEUM_ADDRESS}
    ):
        raise EvidenceError(f"purchase Transfer log mismatch at log {bought['log_index']}")
    fulfilled = [
        log
        for log in purchase_receipt.get("logs", [])
        if str(log.get("address", "")).lower() == SEAPORT_1_6
        and log.get("topics")
        and str(log["topics"][0]).lower() == ORDER_FULFILLED_TOPIC
    ]
    if len(fulfilled) != 1:
        raise EvidenceError("purchase receipt does not contain exactly one Seaport OrderFulfilled event")
    if "0x" + str(fulfilled[0]["topics"][1]).lower()[-40:] != bought["from"]:
        raise EvidenceError("Seaport order offerer is not the token sender")
    purchase_block = block_identity(
        package.call("purchase-block", PRIMARY_RPC_URL, "purchase-block", "eth_getBlockByNumber", [hex(PURCHASE_BLOCK), False]),
        "purchase block",
    )
    if purchase_block["hash"] != str(purchase_receipt.get("blockHash", "")).lower():
        raise EvidenceError("purchase block hash does not match the receipt")

    residual_tx = verify_transaction(
        package.call("residual-transaction", PRIMARY_RPC_URL, "residual-transaction", "eth_getTransactionByHash", [RESIDUAL_TX]),
        label="residual",
        tx_hash=RESIDUAL_TX,
        sender=AGENT_ADDRESS,
        recipient=MUSEUM_ADDRESS,
        value=RESIDUAL_VALUE_WEI,
        nonce=2,
        block=RESIDUAL_BLOCK,
    )
    residual_receipt = verify_receipt(
        package.call("residual-receipt", PRIMARY_RPC_URL, "residual-receipt", "eth_getTransactionReceipt", [RESIDUAL_TX]),
        label="residual",
        tx_hash=RESIDUAL_TX,
        block=RESIDUAL_BLOCK,
    )
    safe_received = residual_receipt.get("logs")
    if (
        not isinstance(safe_received, list)
        or len(safe_received) != 1
        or str(safe_received[0].get("address", "")).lower() != MUSEUM_ADDRESS
        or [str(topic).lower() for topic in safe_received[0].get("topics", [])]
        != [SAFE_RECEIVED_TOPIC, common.address_topic(AGENT_ADDRESS)]
        or common.abi_uint(safe_received[0].get("data"), "SafeReceived value") != RESIDUAL_VALUE_WEI
    ):
        raise EvidenceError("residual receipt does not contain exactly one matching Safe SafeReceived event")
    residual_block = block_identity(
        package.call("residual-block", PRIMARY_RPC_URL, "residual-block", "eth_getBlockByNumber", [hex(RESIDUAL_BLOCK), False]),
        "residual block",
    )
    if residual_block["hash"] != str(residual_receipt.get("blockHash", "")).lower():
        raise EvidenceError("residual block hash does not match the receipt")

    after = block_identity(
        package.call("finalized-block-after", PRIMARY_RPC_URL, "finalized-block-after", "eth_getBlockByNumber", ["finalized", False]),
        "closing finalized block",
    )
    if after != finalized:
        raise EvidenceError("finalized block changed during the custody observation window")

    summary = {
        "record_id": RECORD_ID,
        "record_type": "XCOPY_MAX_PAIN_4188_CUSTODY_OBSERVATION",
        "accession_id": ACCESSION_ID,
        "proposal_drop_id": common.PROPOSAL_DROP_ID,
        "observed_at": observed_at,
        "network": "Ethereum mainnet",
        "chain_id": 1,
        "contract": CONTRACT,
        "museum_address": MUSEUM_ADDRESS,
        "museum_checksum_address": MUSEUM_CHECKSUM_ADDRESS,
        "acquisition_agent_address": AGENT_ADDRESS,
        "custodian": {
            "ens": ENS_NAME,
            "ens_namehash": ENS_NAMEHASH,
            "ens_registry": ENS_REGISTRY,
            "resolver": resolver,
            "address": ens_address,
            "address_poisoning_guard": (
                "The Museum address is compared in all 40 hexadecimal characters with the ENS addr record "
                "read at the finalized block hash. Look-alike addresses beginning 0xbECfA674 and 0xBEcF6883, "
                "planted by spam contracts in the acquisition wallet's token history, are never accepted."
            ),
        },
        "finalized_block": finalized,
        "state_selector": selector,
        "rpc_endpoint": PRIMARY_RPC_URL,
        "second_rpc_endpoint": SECOND_RPC_URL,
        "objects": [
            {
                "object_id": OBJECT_ID,
                "caip19": CAIP19,
                "contract": CONTRACT,
                "token_id": TOKEN_ID,
                "tx_hash": MUSEUM_RECEIPT_TX,
                "block_number": MUSEUM_RECEIPT_BLOCK,
                "transfer_block_hash": receipt_block["hash"],
                "transfer_block_timestamp": receipt_block["timestamp"],
                "log_index": MUSEUM_RECEIPT_LOG_INDEX,
                "transfer_from": AGENT_ADDRESS,
                "transfer_to": MUSEUM_ADDRESS,
                "matching_transfer_log_count": 1,
                "receipt_token_transfer_count": 1,
                "receipt_status": "0x1",
                "owner": owner,
                "owner_matches_museum": True,
                "second_provider_owner": second_owner,
                "token_level_approved_operator": approved,
                "token_level_approval_is_zero": approved == ZERO_ADDRESS,
            }
        ],
        "museum_receipt_transaction": {
            **receipt_tx,
            "block_number": MUSEUM_RECEIPT_BLOCK,
            "block_hash": receipt_block["hash"],
            "block_time": receipt_block["timestamp"],
            "receipt_status": "0x1",
            "gas_used": common.hex_int(receipt.get("gasUsed"), "museum receipt gasUsed"),
            "effective_gas_price_wei": common.hex_int(receipt.get("effectiveGasPrice"), "museum receipt gas price"),
            "transfer_log": {"log_index": MUSEUM_RECEIPT_LOG_INDEX, "from_role": "acquisition_agent", "to_role": "museum_safe"},
        },
        "agent_purchase": {
            **purchase_tx,
            "venue": "Seaport 1.6 (OpenSea protocol)",
            "block_number": PURCHASE_BLOCK,
            "block_hash": purchase_block["hash"],
            "block_time": purchase_block["timestamp"],
            "receipt_status": "0x1",
            "gas_used": common.hex_int(purchase_receipt.get("gasUsed"), "purchase gasUsed"),
            "effective_gas_price_wei": common.hex_int(purchase_receipt.get("effectiveGasPrice"), "purchase gas price"),
            "transfer_log": {
                "log_index": PURCHASE_TRANSFER_LOG_INDEX,
                "from_role": "seller (Seaport order offerer); address retained only in the raw receipt",
                "to_role": "acquisition_agent",
                "token_id": TOKEN_ID,
            },
            "order_fulfilled_log_index": common.hex_int(fulfilled[0].get("logIndex"), "OrderFulfilled logIndex"),
            "semantics": (
                "The acquisition agent bought the token through Seaport 1.6 before delivering it to the Museum Safe. "
                "This is the agent's purchase transaction, not the Museum's custody receipt."
            ),
        },
        "residual_transfer": {
            **residual_tx,
            "block_number": RESIDUAL_BLOCK,
            "block_hash": residual_block["hash"],
            "block_time": residual_block["timestamp"],
            "receipt_status": "0x1",
            "log_count": 1,
            "safe_received_log": {
                "log_index": common.hex_int(safe_received[0].get("logIndex"), "SafeReceived logIndex"),
                "emitter": "museum_safe",
                "event": "SafeReceived(address,uint256)",
                "sender_role": "acquisition_agent",
                "value_wei": str(RESIDUAL_VALUE_WEI),
            },
            "gas_used": common.hex_int(residual_receipt.get("gasUsed"), "residual gasUsed"),
            "effective_gas_price_wei": common.hex_int(residual_receipt.get("effectiveGasPrice"), "residual gas price"),
            "status_boundary": (
                "Observed ETH transfer from the acquisition agent to the Museum Safe. It is not part of the "
                "accession and is not accepted, restricted or designated by this evidence."
            ),
        },
        "assertions": {
            "chain_id_is_ethereum_mainnet": True,
            "finalized_block_stable_before_and_after": True,
            "museum_receipt_successful_with_exactly_one_token_transfer": True,
            "museum_receipt_transfer_log_matches_agent_museum_token_and_log_index": True,
            "museum_receipt_block_hash_matches_receipt": True,
            "ownerOf_matches_ens_resolved_museum_safe": True,
            "second_provider_ownerOf_matches_at_same_block_hash": True,
            "token_level_approval_is_zero": approved == ZERO_ADDRESS,
            "ens_resolves_to_museum_at_same_block_hash": True,
            "purchase_receipt_successful_with_one_transfer_to_agent": True,
            "residual_receipt_successful_with_one_matching_safe_received_event": True,
        },
        "limitations": [
            "This package proves the observed on-chain receipt, purchase and residual transactions and the exact-finalized-block custody state only.",
            "It does not establish legal title, copyright, display or preservation rights, the Wave authorization, contributor arrangements or accession.",
            "A zero token-level approval is not proof that no operator-for-all approval, private claim, legal encumbrance, key compromise or later transfer exists.",
            "The residual ETH transfer is recorded as an observed transaction only; formal acceptance or restriction of those funds is outside this package.",
        ],
        "raw_evidence": sorted(package.raw_entries, key=lambda row: (row["path"], row["request_id"])),
    }
    summary_bytes = common.pretty_json(summary)
    common.write_bytes(output / "summary.json", summary_bytes)

    unique_entries: dict[str, dict[str, Any]] = {}
    for row in package.raw_entries:
        unique_entries.setdefault(
            row["path"],
            {key: (value.removeprefix("sha256:") if key == "sha256" else value) for key, value in row.items() if key in {"path", "sha256", "size", "media_type", "byte_mode"}},
        )
    entries = sorted(
        [*unique_entries.values(), common.entry_for(output, output / "summary.json", "application/json")],
        key=lambda row: row["path"],
    )
    manifest = {
        "manifest_type": "6529NM_XCOPY_MAX_PAIN_4188_CUSTODY_EVIDENCE",
        "manifest_version": "1.0.0",
        "subject_id": OBJECT_ID,
        "record_id": RECORD_ID,
        "observed_at": observed_at,
        "finalized_block": finalized,
        "hash_algorithm": "sha256",
        "byte_mode": "raw",
        "entries": entries,
    }
    manifest_bytes = common.pretty_json(manifest)
    common.write_bytes(output / "manifest.json", manifest_bytes)
    return {
        "status": "complete",
        "record_id": RECORD_ID,
        "finalized_block": finalized,
        "summary_sha256": f"sha256:{common.sha256(summary_bytes)}",
        "manifest_sha256": f"sha256:{common.sha256(manifest_bytes)}",
        "raw_response_count": len(package.raw_entries),
        "owner_matches_museum": True,
        "token_level_approval_is_zero": approved == ZERO_ADDRESS,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=common.ROOT / "evidence" / "xcopy-max-pain-4188-custody",
        help="new or empty destination; never a tracked package in place",
    )
    args = parser.parse_args(argv)
    try:
        print(json.dumps(acquire(args.output_dir.absolute()), ensure_ascii=False, indent=2))
    except (EvidenceError, FetchPolicyError, OSError, ValueError) as error:
        print(f"MAX PAIN custody evidence acquisition refused: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
