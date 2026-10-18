#!/usr/bin/env python3
"""Acquire aggregate funding evidence for the MAX PAIN #4188 purchase.

The acquisition agent's ETH balance and nonce are read at fixed historical
blocks around its three outgoing transactions (the Seaport purchase, the
transfer of the token to the Museum Safe and the residual ETH transfer), at
the finalized block, and the three receipts are retained.  From these class A
reads the package derives total inflows into the agent wallet by balance
arithmetic, without listing or retaining any individual incoming payment.

Contributor and payer wallet addresses are deliberately never requested,
derived or recorded.  The package records no acceptance, restriction,
designation or valuation of the residual ETH; it is observed fact only.
Historical balances require an archive-capable keyless endpoint.
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
    EvidenceError,
    MUSEUM_ADDRESS,
    MUSEUM_RECEIPT_BLOCK,
    MUSEUM_RECEIPT_TX,
    PRIMARY_RPC_URL,
    PURCHASE_BLOCK,
    PURCHASE_TX,
    PURCHASE_VALUE_WEI,
    RESIDUAL_BLOCK,
    RESIDUAL_TX,
    RESIDUAL_VALUE_WEI,
)


USER_AGENT = "6529-Network-Museum/xcopy-max-pain-4188-funding-aggregate-v1"
RECORD_ID = f"{ACCESSION_ID}.FUNDING-EVIDENCE-01"
OUTGOING = (
    ("agent_purchase", PURCHASE_TX, PURCHASE_BLOCK, PURCHASE_VALUE_WEI, 0),
    ("museum_receipt_transfer", MUSEUM_RECEIPT_TX, MUSEUM_RECEIPT_BLOCK, 0, 1),
    ("residual_transfer_to_museum_safe", RESIDUAL_TX, RESIDUAL_BLOCK, RESIDUAL_VALUE_WEI, 2),
)
CHECKPOINTS = (
    ("before_purchase", PURCHASE_BLOCK - 1),
    ("after_purchase", PURCHASE_BLOCK),
    ("after_museum_receipt", MUSEUM_RECEIPT_BLOCK),
    ("before_residual_transfer", RESIDUAL_BLOCK - 1),
    ("after_residual_transfer", RESIDUAL_BLOCK),
)


class Package:
    def __init__(self, output: Path) -> None:
        self.output = output
        self.client = common.RpcClient(USER_AGENT)
        self.sequence = 0
        self.entries: list[dict[str, Any]] = []
        self.calls: list[dict[str, Any]] = []

    def rpc(self, label: str, method: str, params: list[Any]) -> Any:
        call = self.client.call(PRIMARY_RPC_URL, label, method, params)
        self.sequence += 1
        prefix = f"raw/rpc/{self.sequence:04d}-{label}"
        for suffix, payload in (("request", call["request_bytes"]), ("response", call["response_bytes"])):
            relative = f"{prefix}-{suffix}.json"
            common.write_bytes(self.output / relative, payload)
            self.entries.append(common.entry_for(self.output, self.output / relative, "application/json"))
        self.calls.append(
            {
                "label": label,
                "method": method,
                "request_path": f"{prefix}-request.json",
                "response_path": f"{prefix}-response.json",
                "transport": call["transport"],
            }
        )
        return common.require_result(call, label)


def acquire(output: Path) -> dict[str, Any]:
    common.assert_fixed_identities()
    common.prepare_empty_output(output)
    package = Package(output)
    observed_at = common.utc_now()
    if package.rpc("chain-id", "eth_chainId", []) != "0x1":
        raise EvidenceError("RPC endpoint did not report Ethereum mainnet")
    finalized_block = package.rpc("finalized-block", "eth_getBlockByNumber", ["finalized", False])
    finalized = {
        "number": common.hex_int(finalized_block.get("number"), "finalized"),
        "hash": str(finalized_block.get("hash", "")).lower(),
        "timestamp": common.iso_from_unix(common.hex_int(finalized_block.get("timestamp"), "finalized")),
    }

    outgoing: list[dict[str, Any]] = []
    for label, tx_hash, block, value, nonce in OUTGOING:
        tx = package.rpc(f"{label}-transaction", "eth_getTransactionByHash", [tx_hash])
        receipt = package.rpc(f"{label}-receipt", "eth_getTransactionReceipt", [tx_hash])
        if (
            str(tx.get("from", "")).lower() != AGENT_ADDRESS
            or common.hex_int(tx.get("value"), "value") != value
            or common.hex_int(tx.get("nonce"), "nonce") != nonce
            or receipt.get("status") != "0x1"
            or common.hex_int(receipt.get("blockNumber"), "block") != block
        ):
            raise EvidenceError(f"{label} transaction does not match the fixed facts")
        fee = common.hex_int(receipt.get("gasUsed"), "gasUsed") * common.hex_int(receipt.get("effectiveGasPrice"), "gasPrice")
        outgoing.append(
            {
                "role": label,
                "transaction_hash": tx_hash,
                "block_number": block,
                "nonce": nonce,
                "value_wei": str(value),
                "value_eth": common.wei_to_eth_string(value),
                "gas_fee_wei": str(fee),
                "recipient_role": {"agent_purchase": "seaport_1_6", "museum_receipt_transfer": "token_contract", "residual_transfer_to_museum_safe": "museum_safe"}[label],
            }
        )
        if label == "residual_transfer_to_museum_safe" and str(tx.get("to", "")).lower() != MUSEUM_ADDRESS:
            raise EvidenceError("residual transfer recipient is not the Museum Safe")

    checkpoints: list[dict[str, Any]] = []
    for label, block in (*CHECKPOINTS, ("finalized", finalized["number"])):
        tag = hex(block)
        balance = common.hex_int(package.rpc(f"balance-{label}", "eth_getBalance", [AGENT_ADDRESS, tag]), "balance")
        nonce = common.hex_int(package.rpc(f"nonce-{label}", "eth_getTransactionCount", [AGENT_ADDRESS, tag]), "nonce")
        checkpoints.append({"checkpoint": label, "block_number": block, "balance_wei": str(balance), "balance_eth": common.wei_to_eth_string(balance), "nonce": nonce})
    expected_nonces = [0, 1, 2, 2, 3, 3]
    if [row["nonce"] for row in checkpoints] != expected_nonces:
        raise EvidenceError("agent nonces do not isolate the three outgoing transactions between checkpoints")

    by_label = {row["checkpoint"]: int(row["balance_wei"]) for row in checkpoints}
    out = {row["role"]: int(row["value_wei"]) + int(row["gas_fee_wei"]) for row in outgoing}
    intervals = [
        ("through_block_before_purchase", by_label["before_purchase"], 0),
        ("purchase_block", by_label["after_purchase"] - by_label["before_purchase"], out["agent_purchase"]),
        ("purchase_to_museum_receipt", by_label["after_museum_receipt"] - by_label["after_purchase"], out["museum_receipt_transfer"]),
        ("museum_receipt_to_block_before_residual", by_label["before_residual_transfer"] - by_label["after_museum_receipt"], 0),
        ("residual_block", by_label["after_residual_transfer"] - by_label["before_residual_transfer"], out["residual_transfer_to_museum_safe"]),
        ("after_residual_to_finalized", by_label["finalized"] - by_label["after_residual_transfer"], 0),
    ]
    inflows = []
    for label, delta, outflow in intervals:
        inflow = delta + outflow
        if inflow < 0:
            raise EvidenceError(f"negative derived inflow in {label}")
        inflows.append({"interval": label, "balance_change_wei": str(delta), "known_outflow_wei": str(outflow), "derived_inflow_wei": str(inflow), "derived_inflow_eth": common.wei_to_eth_string(inflow)})
    total_inflow = sum(int(row["derived_inflow_wei"]) for row in inflows)
    total_fees = sum(int(row["gas_fee_wei"]) for row in outgoing)

    summary = {
        "record_id": RECORD_ID,
        "record_type": "XCOPY_MAX_PAIN_4188_FUNDING_AGGREGATE_OBSERVATION",
        "observed_at": observed_at,
        "accession_id": ACCESSION_ID,
        "network": "Ethereum mainnet",
        "rpc_endpoint": PRIMARY_RPC_URL,
        "finalized_block": finalized,
        "acquisition_agent_address": AGENT_ADDRESS,
        "museum_address": MUSEUM_ADDRESS,
        "outgoing_transactions": outgoing,
        "balance_checkpoints": checkpoints,
        "derived_inflows": inflows,
        "totals": {
            "total_inflow_wei": str(total_inflow),
            "total_inflow_eth": common.wei_to_eth_string(total_inflow),
            "purchase_value_wei": str(PURCHASE_VALUE_WEI),
            "residual_transfer_wei": str(RESIDUAL_VALUE_WEI),
            "gas_fees_wei": str(total_fees),
            "remaining_balance_at_finalized_wei": str(by_label["finalized"]),
            "identity": "total_inflow = purchase value + residual transfer + gas fees + remaining balance",
            "identity_holds": total_inflow == PURCHASE_VALUE_WEI + RESIDUAL_VALUE_WEI + total_fees + by_label["finalized"],
        },
        "method": (
            "eth_getBalance and eth_getTransactionCount for the agent wallet at each checkpoint block (archive reads), with the "
            "three outgoing receipts. Nonces show that no other outgoing transaction occurred between checkpoints, so each "
            "interval's inflow is its balance change plus its known outflows (value plus gasUsed x effectiveGasPrice)."
        ),
        "privacy_boundary": (
            "Incoming payments are aggregated by balance arithmetic only. No incoming transaction, sender, contributor or payer "
            "address is requested, derived or retained."
        ),
        "limitations": [
            "These are chain observations of one wallet. They do not identify contributors, establish who paid what, or show whether any payment was a contribution.",
            "The residual ETH transfer to the Museum Safe is recorded as an observed transaction; it is not accepted, restricted or designated by this evidence.",
            "No valuation or tax characterization is made.",
        ],
        "raw_json_rpc": package.calls,
    }
    if not summary["totals"]["identity_holds"]:
        raise EvidenceError("aggregate funding identity does not hold")
    summary_bytes = common.pretty_json(summary)
    common.write_bytes(output / "summary.json", summary_bytes)
    manifest = {
        "manifest_type": "6529NM_XCOPY_MAX_PAIN_4188_FUNDING_AGGREGATE_EVIDENCE",
        "manifest_version": "1.0.0",
        "subject_id": ACCESSION_ID,
        "record_id": RECORD_ID,
        "observed_at": observed_at,
        "hash_algorithm": "sha256",
        "byte_mode": "raw",
        "entries": sorted([*package.entries, common.entry_for(output, output / "summary.json", "application/json")], key=lambda row: row["path"]),
    }
    manifest_bytes = common.pretty_json(manifest)
    common.write_bytes(output / "manifest.json", manifest_bytes)
    return {
        "status": "complete",
        "record_id": RECORD_ID,
        "finalized_block": finalized,
        "summary_sha256": f"sha256:{common.sha256(summary_bytes)}",
        "manifest_sha256": f"sha256:{common.sha256(manifest_bytes)}",
        "total_inflow_eth": summary["totals"]["total_inflow_eth"],
        "derived_inflows_eth": {row["interval"]: row["derived_inflow_eth"] for row in inflows},
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--output-dir", type=Path, default=common.ROOT / "evidence" / "xcopy-max-pain-4188-funding")
    args = parser.parse_args(argv)
    try:
        print(json.dumps(acquire(args.output_dir.absolute()), ensure_ascii=False, indent=2))
    except (EvidenceError, FetchPolicyError, OSError, ValueError) as exc:
        print(f"MAX PAIN funding evidence acquisition refused: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
