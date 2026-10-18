#!/usr/bin/env python3
"""Acquire the supplementary MAX PAIN #4188/7394 readings that the public texts cite.

The custody, source, technical and funding packages retain the facts the
accession records rely on.  The public scholarship also cites readings that
those packages did not retain.  This script retains them, keyless and
public-safe, in ``evidence/xcopy-max-pain-4188-supplement``:

* edition 3265: the 29 August 2026 transfer to the TokenWorks strategy
  contract and the 1 September 2026 burn (transactions, receipts and blocks);
* the 21 ``mintNifty`` transactions (one ``eth_getLogs`` read of the EIP-2309
  ``ConsecutiveTransfer`` events) and the first and last mint blocks;
* the *DAMAGE CONTROL* contract's ``owner()``, its creation receipt (located
  through Blockscout, class D, then read by RPC), the ENS names of both
  accounts, its ``uri(1..10)`` and the ten token-metadata documents, and the
  variant contract's ``name()``;
* a public-safe *DAMAGE CONTROL* redemption table, derived from a complete
  burn-log scan, every burn transaction's calldata and the ten burn-redeem
  configurations: per work the burn requirement, ETH cost, window, MAX PAIN
  burned and redemptions, with first and last burn blocks and times; counts of
  burns, transactions, redemptions and distinct burner accounts; and the burns
  through the block of XCOPY's 21 March 2024 post.  Burner and payer
  addresses are never written: scan and transaction responses are committed by
  SHA-256 only, and the sorted burn transaction-hash list is retained with its
  own digest;
* The Memes card 47 (*EXIT STRATEGY*) record from the 6529 API, the earliest
  post of XCOPY's Tumblr (keyless v1 API), and the Nifty Gateway creator
  profile sentence "Warning: flashing imagery" from the same Wayback bytes as
  the source package's drop-page capture;
* public-safe projections of the organizer's Museum Wave messages of
  28 August, 2 September and 14 September 2026.  Member mentions, the names in
  a per-person payment-status sentence and the acquisition wallet address are
  omitted from the transcripts; the exact part text is committed by SHA-256.

All reads use ``safe_fetch`` against keyless public endpoints.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import max_pain_evidence_common as common
from max_pain_evidence_common import (
    BATCH_RPC_URL,
    CONTRACT,
    PRIMARY_RPC_URL,
    TRANSFER_TOPIC,
    ZERO_ADDRESS,
    EvidenceError,
)


USER_AGENT = "6529-Network-Museum/xcopy-max-pain-4188-supplementary-evidence-v1"
RECORD_ID = f"{common.ACCESSION_ID}.SUPPLEMENTARY-EVIDENCE-01"
DEFAULT_OUTPUT = common.ROOT / "evidence" / "xcopy-max-pain-4188-supplement"

FIRST_MINT_BLOCK = 14_451_975
LAST_MINT_BLOCK = 14_451_998
FIRST_TOKEN_ID = 171_000_100_001
LAST_TOKEN_ID = 171_000_107_394
SCAN_WINDOW_BLOCKS = 10_000
TX_BATCH = 50
CONSECUTIVE_TRANSFER_TOPIC = "0xdeaa91b6123d068f5821d0fb0678463d1a8a6079fe8af5de3ce5e896dcf9133d"
BURN_REDEEM_EXTENSION = "0xfc29813beeb3c7395c7a5f8dfc3352491d5ea0e2"
DAMAGE_CONTROL = "0x3e34ff1790bf0a13efd7d77e75870cb525687338"
VARIANT_CONTRACT = "0x18a62e93ff3ab180e0c7abd4812595bf2be3405f"
TOKENWORKS_STRATEGY = "0xdfc3af477979912ec90b138d3e5552d5304c5663"
MAX_PAIN_FEE_HANDLER = "0x7aca5424c570c2ad530ee3d4dbfd731a9aebacff"
EDITION_3265_TRANSFER_TX = "0xfd84dfc72eb17f80c15948c7fccccac53147203477021eccbfab0fd22bf76001"
EDITION_3265_BURN_TX = "0x4f99a83d0001ba00013d99f5076ccae55d1cd1d1337749aaed6c7eda1a19bda9"
EDITION_3265_TOKEN_ID = 171_000_103_265
SELLER_PURCHASE_TX = "0x922415bb553845ae9df5289819ce2995988e0ccf5a6cd4c3460971194a98b915"
SINGLE_BURN_REDEEM = "0xc9dad696"
BATCH_BURN_REDEEM = "0x42b54fee"
# XCOPY's post of 21 March 2024 (status 1770784105791107412) was published at
# 12:06:45 UTC; the reading counts burns through the last block at or before it.
POST_2024_03_21_UNIX = 1_711_022_805
DAMAGE_CONTROL_TOKEN_IDS = tuple(range(1, 11))
BLOCKSCOUT_ADDRESS_URL = f"https://eth.blockscout.com/api/v2/addresses/{DAMAGE_CONTROL}"
MEMES_CONTRACT = "0x33FD426905F149f8376e227d0C9D3340AaD17aF1"
MEMES_CARD_URL = f"https://api.6529.io/api/nfts?contract={MEMES_CONTRACT}&id=47"
TUMBLR_TOTAL_POSTS_HINT = 2973
TUMBLR_URL_TEMPLATE = "https://xcopy.tumblr.com/api/read/json?num=1&start={start}"
WAYBACK_DROP_URL = (
    "https://web.archive.org/web/20250905031141id_/https://www.niftygateway.com/marketplace/collection/"
    "0xd1169e5349d1cb9941f3dcba135c8a4b9eacfdde/1/"
)
WAYBACK_DROP_SHA256 = "b6ac99c09d183a0cc04c67448873e15ec8f6f4bcce744e42906129ad0c6c7ad8"
FLASHING_CITATION = "Warning: flashing imagery"
DROPS_API = "https://api.6529.io/api/drops/"
ORGANIZER_HANDLE = "Shelby"
WAVE_MESSAGES = (
    ("f8fb553e-a31d-4378-b7fe-88814d7349d3", "funding_call_2026_08_28"),
    ("241c669f-fc4d-4e9c-8ac6-547c13f61284", "purchase_and_leftover_options_2026_09_02"),
    ("5798bc3c-f7d4-4c32-8fcf-45bb2919f4ce", "residual_transfer_2026_09_14"),
)
MENTION = re.compile(r"@\[[^\]\n]+\]")
MENTION_RUN = re.compile(r"@\[[^\]\n]+\](?:[ \t]+@\[[^\]\n]+\])+")
ADDRESS = re.compile(r"0x[0-9a-fA-F]{40}")
OUTSTANDING_NAMES = re.compile(r"(three outstanding contributions from )([^.\n]+)(\.)")


class Collector:
    """Numbered raw retention for public reads; SHA-256 commitments for address-bearing reads."""

    def __init__(self, output: Path) -> None:
        self.output = output
        self.client = common.RpcClient(USER_AGENT)
        self.sequence = 0
        self.raw: list[dict[str, Any]] = []
        self.commitments: dict[str, list[dict[str, Any]]] = {}

    def _next(self) -> int:
        self.sequence += 1
        return self.sequence

    def rpc(self, label: str, method: str, params: list[Any], *, endpoint: str = PRIMARY_RPC_URL, group: str | None = None) -> Any:
        call = self.client.call(endpoint, label, method, params)
        response = call["response"]
        if "error" in response or "result" not in response:
            raise EvidenceError(f"{label}: {response.get('error')!r}")
        self._record(label, call["request_bytes"], call["response_bytes"], call["transport"], group)
        return response["result"]

    def batch(self, label: str, requests: list[tuple[str, list[Any]]], *, group: str) -> list[Any]:
        body = [{"jsonrpc": "2.0", "id": index, "method": method, "params": params} for index, (method, params) in enumerate(requests)]
        request_bytes = common.canonical_json(body)
        for attempt in range(len(common.RETRY_DELAYS_SECONDS) + 1):
            time.sleep(self.client.pause_seconds)
            result, attempts = common.fetch(BATCH_RPC_URL, method="POST", body=request_bytes, accept="application/json", user_agent=USER_AGENT)
            if result.observation.status != 200:
                raise EvidenceError(f"{label}: HTTP {result.observation.status}")
            decoded = json.loads(result.body.decode("utf-8"))
            by_id = {row.get("id"): row for row in decoded if isinstance(row, dict)} if isinstance(decoded, list) else {}
            if len(by_id) == len(requests) and not any(isinstance(row.get("error"), dict) for row in by_id.values()):
                transport = result.observation.to_dict()
                transport["endpoint"] = BATCH_RPC_URL
                transport["attempts"] = attempts + attempt
                self._record(label, request_bytes, result.body, transport, group)
                return [by_id[index]["result"] for index in range(len(requests))]
            if attempt < len(common.RETRY_DELAYS_SECONDS):
                time.sleep(common.RETRY_DELAYS_SECONDS[attempt])
        raise EvidenceError(f"{label}: batch response incomplete after retries")

    def http(self, label: str, url: str, *, accept: str, retain_as: str | None, group: str | None = None) -> tuple[bytes, dict[str, Any]]:
        result, attempts = common.fetch(url, accept=accept, user_agent=USER_AGENT)
        if result.observation.status != 200:
            raise EvidenceError(f"{label}: HTTP {result.observation.status} from {url}")
        transport = result.observation.to_dict()
        transport["attempts"] = attempts
        sequence = self._next()
        row = {
            "sequence": sequence,
            "label": label,
            "url": url,
            "response_sha256": f"sha256:{common.sha256(result.body)}",
            "response_size": len(result.body),
            "transport": transport,
        }
        if retain_as is not None:
            path = f"raw/http/{sequence:04d}-{label}{retain_as}"
            common.write_bytes(self.output / path, result.body)
            row["response_path"] = path
            self.raw.append(row)
        else:
            row["retained"] = False
            self.commitments.setdefault(group or "unretained-http", []).append(row)
        return result.body, row

    def _record(self, label: str, request_bytes: bytes, response_bytes: bytes, transport: dict[str, Any], group: str | None) -> None:
        sequence = self._next()
        if group is None:
            prefix = f"raw/rpc/{sequence:04d}-{label}"
            common.write_bytes(self.output / f"{prefix}-request.json", request_bytes)
            common.write_bytes(self.output / f"{prefix}-response.json", response_bytes)
            self.raw.append(
                {
                    "sequence": sequence,
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
                    "sequence": sequence,
                    "label": label,
                    "endpoint": transport.get("endpoint"),
                    "observed_at": transport.get("observed_at"),
                    "request_sha256": f"sha256:{common.sha256(request_bytes)}",
                    "response_sha256": f"sha256:{common.sha256(response_bytes)}",
                    "response_size": len(response_bytes),
                }
            )

    def group_summary(self, group: str) -> dict[str, Any]:
        rows = self.commitments.get(group, [])
        return {
            "group": group,
            "exchange_count": len(rows),
            "first_observed_at": rows[0].get("observed_at") if rows else None,
            "last_observed_at": rows[-1].get("observed_at") if rows else None,
            "total_response_bytes": sum(row["response_size"] for row in rows),
            "aggregate_sha256": f"sha256:{common.sha256(common.canonical_json([[row['label'], row.get('request_sha256'), row['response_sha256']] for row in rows]))}",
            "aggregate_canonicalization": "sorted-key compact JSON array of [label, request_sha256, response_sha256] in request order",
            "retained": False,
        }


# ---------------------------------------------------------------- ABI decoding


def _word(data: bytes, offset: int) -> int:
    if offset + 32 > len(data):
        raise EvidenceError("ABI word out of range")
    return int.from_bytes(data[offset : offset + 32], "big")


def _burn_tokens(data: bytes, base: int) -> list[dict[str, Any]]:
    """Decode BurnToken[] (uint48 groupIndex, uint48 itemIndex, address, uint256 id, bytes32[] proof) at ``base``."""

    count = _word(data, base)
    tokens = []
    for index in range(count):
        start = base + 32 + _word(data, base + 32 + 32 * index)
        tokens.append(
            {
                "group_index": _word(data, start),
                "item_index": _word(data, start + 32),
                "contract": "0x" + data[start + 64 + 12 : start + 96].hex(),
                "token_id": _word(data, start + 96),
            }
        )
    return tokens


def decode_burn_redeem(input_hex: str) -> list[dict[str, Any]]:
    """Return one call row per redeemed instance in a burn-redeem transaction."""

    raw = common.hex_bytes(input_hex, "burn-redeem input")
    selector, data = raw[:4].hex(), raw[4:]
    if "0x" + selector == SINGLE_BURN_REDEEM:
        return [
            {
                "creator_contract": "0x" + data[12:32].hex(),
                "instance_id": _word(data, 32),
                "redeem_count": _word(data, 64),
                "burn_tokens": _burn_tokens(data, _word(data, 96)),
            }
        ]
    if "0x" + selector == BATCH_BURN_REDEEM:
        heads = [_word(data, 32 * index) for index in range(4)]
        count = _word(data, heads[0])
        if not all(_word(data, head) == count for head in heads):
            raise EvidenceError("batch burn-redeem arrays differ in length")
        rows = []
        for index in range(count):
            token_base = heads[3] + 32 + _word(data, heads[3] + 32 + 32 * index)
            rows.append(
                {
                    "creator_contract": "0x" + data[heads[0] + 32 + 32 * index + 12 : heads[0] + 64 + 32 * index].hex(),
                    "instance_id": _word(data, heads[1] + 32 + 32 * index),
                    "redeem_count": _word(data, heads[2] + 32 + 32 * index),
                    "burn_tokens": _burn_tokens(data, token_base),
                }
            )
        return rows
    raise EvidenceError(f"unrecognized burn-redeem selector 0x{selector}")


def decode_burn_redeem_config(result_hex: str) -> dict[str, Any]:
    """Decode the Manifold getBurnRedeem(address,uint256) BurnRedeem struct."""

    data = common.hex_bytes(result_hex, "getBurnRedeem")
    base = _word(data, 0)
    field = lambda index: _word(data, base + 32 * index)  # noqa: E731
    location_offset = base + field(9)
    location_length = _word(data, location_offset)
    location = data[location_offset + 32 : location_offset + 32 + location_length].decode("utf-8")
    groups_offset = base + field(10)
    group_count = _word(data, groups_offset)
    groups = []
    for group_index in range(group_count):
        group_base = groups_offset + 32 + _word(data, groups_offset + 32 + 32 * group_index)
        required = _word(data, group_base)
        items_offset = group_base + _word(data, group_base + 32)
        item_count = _word(data, items_offset)
        items = []
        for item_index in range(item_count):
            item = items_offset + 32 + 32 * 8 * item_index
            items.append(
                {
                    "validation_type": ["invalid", "contract", "range", "merkle_tree", "any"][_word(data, item)],
                    "contract": "0x" + data[item + 32 + 12 : item + 64].hex(),
                    "token_spec": ["invalid", "erc721", "erc1155"][_word(data, item + 64)],
                    "burn_spec": ["none", "manifold", "openzeppelin"][_word(data, item + 96)] if _word(data, item + 96) < 3 else _word(data, item + 96),
                    "amount": _word(data, item + 128),
                    "min_token_id": _word(data, item + 160),
                    "max_token_id": _word(data, item + 192),
                }
            )
        groups.append({"required_count": required, "items": items})
    unix = lambda value: common.iso_from_unix(value) if value else None  # noqa: E731
    return {
        "storage_protocol": ["invalid", "none", "arweave", "ipfs"][field(1)],
        "redeemed_count": field(2),
        "redeem_amount": field(3),
        "total_supply": field(4),
        "contract_version": field(5),
        "start_date": unix(field(6)),
        "end_date": unix(field(7)),
        "cost_wei": str(field(8)),
        "location": location,
        "burn_set": groups,
    }


# ---------------------------------------------------------------- projections


def wave_projection(raw: bytes, drop_id: str, purpose: str, output: Path) -> dict[str, Any]:
    drop = json.loads(raw.decode("utf-8"))
    if drop.get("id") != drop_id or drop.get("wave", {}).get("id") != common.WAVE_ID:
        raise EvidenceError(f"{drop_id}: not a drop of the Museum Wave")
    author = drop.get("author", {}).get("handle")
    if author != ORGANIZER_HANDLE:
        raise EvidenceError(f"{drop_id}: author is not the organizer")
    parts = []
    bindings: dict[str, Any] = {}
    for part in drop.get("parts", []):
        content = part.get("content") or ""
        redactions: list[dict[str, Any]] = []
        transcript = content
        mentions = MENTION.findall(transcript)
        if mentions:
            transcript = MENTION_RUN.sub(lambda match: f"[{len(MENTION.findall(match.group(0)))} mentions omitted]", transcript)
            transcript = MENTION.sub("[mention omitted]", transcript)
            redactions.append({"kind": "member_mentions", "count": len(mentions), "reason": "Member handles appear only in the essay's credits list."})
        outstanding = OUTSTANDING_NAMES.search(transcript)
        if outstanding:
            names = [name.strip() for name in re.split(r",|\band\b", outstanding.group(2)) if name.strip()]
            transcript = OUTSTANDING_NAMES.sub(lambda match: f"{match.group(1)}[{len(names)} contributor names omitted]{match.group(3)}", transcript)
            redactions.append({"kind": "per_contributor_payment_status", "count": len(names), "reason": "Per-person payment facts are not published."})
        addresses = sorted({value.lower() for value in ADDRESS.findall(transcript)})
        for address in addresses:
            if address != common.AGENT_ADDRESS:
                raise EvidenceError(f"{drop_id}: unexpected address in message content")
            bindings["names_the_acquisition_wallet"] = True
            bindings["acquisition_wallet_reference"] = "the acquisition_agent role address of evidence/xcopy-max-pain-4188-custody (all 40 hex characters compared)"
        if addresses:
            transcript = ADDRESS.sub("[acquisition wallet address omitted]", transcript)
            redactions.append({"kind": "acquisition_wallet_address", "count": len(addresses), "reason": "The acquisition wallet address appears only in machine records that require it."})
        if "@[" in transcript:
            raise EvidenceError(f"{drop_id}: a member mention survived redaction")
        transcript_bytes = transcript.encode("utf-8")
        path = f"wave/{purpose}-part-{part.get('part_id')}.txt"
        common.write_bytes(output / path, transcript_bytes)
        parts.append(
            {
                "part_id": part.get("part_id"),
                "content_sha256": f"sha256:{common.sha256(content.encode('utf-8'))}",
                "content_utf8_bytes": len(content.encode("utf-8")),
                "transcript_path": path,
                "transcript_sha256": f"sha256:{common.sha256(transcript_bytes)}",
                "redactions": redactions,
            }
        )
    return {
        "purpose": purpose,
        "drop_id": drop_id,
        "serial_no": drop.get("serial_no"),
        "wave_id": common.WAVE_ID,
        "drop_type": drop.get("drop_type"),
        "author_handle": author,
        "created_at": common.iso_from_unix(int(drop["created_at"]) // 1000).replace("Z", f".{int(drop['created_at']) % 1000:03d}Z"),
        "created_at_api_value": drop.get("created_at"),
        "is_signed": drop.get("is_signed"),
        "parts": parts,
        "machine_bindings": bindings,
        "source_url": f"{DROPS_API}{drop_id}",
    }


def memes_projection(raw: bytes) -> dict[str, Any]:
    rows = json.loads(raw.decode("utf-8")).get("data", [])
    if len(rows) != 1 or rows[0].get("id") != 47:
        raise EvidenceError("6529 API did not return exactly card 47")
    card = rows[0]
    metadata = card.get("metadata") or {}
    return {
        "contract": card.get("contract"),
        "id": card.get("id"),
        "name": card.get("name"),
        "collection": card.get("collection"),
        "artist": card.get("artist"),
        "token_type": card.get("token_type"),
        "supply": card.get("supply"),
        "mint_date": card.get("mint_date"),
        "uri": card.get("uri"),
        "image": card.get("image"),
        "metadata_image": metadata.get("image"),
        "metadata_image_details": metadata.get("image_details"),
        "excluded_fields": "market, holder, offer and floor fields (including account addresses) are excluded",
    }


def acquire(output: Path) -> dict[str, Any]:
    common.assert_fixed_identities()
    common.prepare_empty_output(output)
    collector = Collector(output)
    observed_at = common.utc_now()
    if collector.rpc("chain-id", "eth_chainId", []) != "0x1":
        raise EvidenceError("RPC endpoint did not report Ethereum mainnet")
    finalized = collector.rpc("finalized-block", "eth_getBlockByNumber", ["finalized", False])
    target = {"number": common.hex_int(finalized["number"], "number"), "hash": finalized["hash"].lower(), "timestamp": common.iso_from_unix(common.hex_int(finalized["timestamp"], "ts"))}
    selector = {"blockHash": target["hash"], "requireCanonical": True}

    def call(label: str, to: str, signature: str, *values: int | str) -> str:
        return collector.rpc(label, "eth_call", [{"to": to, "data": common.calldata(signature, *values)}, selector])

    def block(label: str, number: int) -> dict[str, Any]:
        header = collector.rpc(label, "eth_getBlockByNumber", [hex(number), False])
        return {"number": number, "hash": header["hash"].lower(), "timestamp": common.iso_from_unix(common.hex_int(header["timestamp"], "ts"))}

    # Edition 3265 and the seller of edition 4188.
    def roles_for(seller: str) -> dict[str, str]:
        return {
            TOKENWORKS_STRATEGY: "tokenworks_strategy_contract",
            MAX_PAIN_FEE_HANDLER: "max_pain_fee_handler",
            ZERO_ADDRESS: "burn_zero_address",
            seller: "seller_of_edition_4188",
            common.AGENT_ADDRESS: "acquisition_wallet",
        }

    purchase_receipt = collector.rpc("purchase-receipt", "eth_getTransactionReceipt", [common.PURCHASE_TX])
    purchase_moves = [common.decoded_transfer(log) for log in common.transfer_logs(purchase_receipt) if int(log["topics"][3], 16) == common.TOKEN_ID]
    if len(purchase_moves) != 1 or purchase_moves[0]["log_index"] != common.PURCHASE_TRANSFER_LOG_INDEX or purchase_moves[0]["to"] != common.AGENT_ADDRESS:
        raise EvidenceError("purchase receipt does not carry edition 4188 to the acquisition wallet at the recorded log")
    seller = purchase_moves[0]["from"]
    roles = roles_for(seller)

    def role(address: str) -> str:
        return roles.get(address, "unlabelled_account")

    def edition_step(label: str, tx_hash: str, token_id: int) -> dict[str, Any]:
        tx = collector.rpc(f"{label}-transaction", "eth_getTransactionByHash", [tx_hash])
        receipt = collector.rpc(f"{label}-receipt", "eth_getTransactionReceipt", [tx_hash])
        header = block(f"{label}-block", common.hex_int(receipt["blockNumber"], "block"))
        if receipt.get("status") != "0x1" or receipt["blockHash"].lower() != header["hash"]:
            raise EvidenceError(f"{label}: receipt failed or block hash differs")
        moves = [common.decoded_transfer(log) for log in common.transfer_logs(receipt) if int(log["topics"][3], 16) == token_id]
        sender, recipient = str(tx["from"]).lower(), str(tx.get("to") or "").lower()
        return {
            "step": label,
            "token_id": token_id,
            "transaction_hash": tx_hash,
            "block_number": header["number"],
            "block_hash": header["hash"],
            "time": header["timestamp"],
            "transfers": [{"log_index": move["log_index"], "from_role": role(move["from"]), "to_role": role(move["to"])} for move in moves],
            "transaction_sender_role": role(sender),
            "transaction_target_role": "sender_own_account_self_addressed" if recipient == sender else role(recipient),
            "method_selector": str(tx.get("input", "0x"))[:10],
            "log_emitter_roles": sorted({role(str(log.get("address", "")).lower()) if str(log.get("address", "")).lower() != CONTRACT else "max_pain_contract" for log in receipt["logs"]}),
        }

    seller_acquisition = edition_step("seller-acquires-edition-4188", SELLER_PURCHASE_TX, common.TOKEN_ID)
    edition_3265 = [
        edition_step("edition-3265-to-strategy", EDITION_3265_TRANSFER_TX, EDITION_3265_TOKEN_ID),
        edition_step("edition-3265-burn", EDITION_3265_BURN_TX, EDITION_3265_TOKEN_ID),
    ]
    if [move["to_role"] for move in seller_acquisition["transfers"]] != ["seller_of_edition_4188"]:
        raise EvidenceError("the seller did not acquire edition 4188 in the recorded transaction")
    if [(move["from_role"], move["to_role"]) for move in edition_3265[0]["transfers"]] != [("seller_of_edition_4188", "tokenworks_strategy_contract")]:
        raise EvidenceError("edition 3265 did not pass from the seller of edition 4188 to the strategy contract")
    if [(move["from_role"], move["to_role"]) for move in edition_3265[1]["transfers"]] != [
        ("tokenworks_strategy_contract", "max_pain_fee_handler"),
        ("max_pain_fee_handler", "burn_zero_address"),
    ]:
        raise EvidenceError("edition 3265 was not bought from the strategy contract and burned by the fee handler")
    edition_3265_record = {
        "seller_of_edition_4188": {
            "identified_by": f"from of the edition 4188 Transfer, log {common.PURCHASE_TRANSFER_LOG_INDEX}, in purchase transaction {common.PURCHASE_TX}",
            "address_boundary": "The seller's address is retained only in the raw receipts; derived fields name it by role.",
        },
        "seller_acquires_edition_4188": seller_acquisition,
        "edition_3265": edition_3265,
        "same_wallet": True,
    }

    # Mint transactions.
    mint_logs = collector.rpc(
        "mint-consecutive-transfer-logs",
        "eth_getLogs",
        [{"address": CONTRACT, "topics": [CONSECUTIVE_TRANSFER_TOPIC], "fromBlock": hex(FIRST_MINT_BLOCK), "toBlock": hex(LAST_MINT_BLOCK)}],
    )
    mints = sorted(
        (
            {
                "transaction_hash": log["transactionHash"].lower(),
                "block_number": common.hex_int(log["blockNumber"], "block"),
                "log_index": common.hex_int(log["logIndex"], "log"),
                "from_token_id": int(log["topics"][1], 16),
                "to_token_id": int(log["data"], 16),
                "to_role": "nifty_gateway_platform_custody",
            }
            for log in mint_logs
        ),
        key=lambda row: (row["block_number"], row["log_index"]),
    )
    covered = sum(row["to_token_id"] - row["from_token_id"] + 1 for row in mints)
    if len(mints) != 21 or len({row["transaction_hash"] for row in mints}) != 21 or covered != LAST_TOKEN_ID - FIRST_TOKEN_ID + 1:
        raise EvidenceError("mint logs are not 21 transactions covering the 7,394 token ids")
    mint_first = block("mint-first-block", mints[0]["block_number"])
    mint_last = block("mint-last-block", mints[-1]["block_number"])

    # Contract identity reads.
    dc_owner = common.abi_address(call("damage-control-owner", DAMAGE_CONTROL, "owner()"), "owner")
    blockscout_raw, blockscout_row = collector.http("blockscout-damage-control-address", BLOCKSCOUT_ADDRESS_URL, accept="application/json", retain_as=None, group="class-d-locators")
    blockscout = json.loads(blockscout_raw.decode("utf-8"))
    creation_tx = str(blockscout.get("creation_transaction_hash") or blockscout.get("creation_tx_hash")).lower()
    creation_receipt = collector.rpc("damage-control-creation-receipt", "eth_getTransactionReceipt", [creation_tx])
    if str(creation_receipt.get("contractAddress", "")).lower() != DAMAGE_CONTROL or creation_receipt.get("status") != "0x1":
        raise EvidenceError("Blockscout creation transaction does not create the DAMAGE CONTROL contract")
    deployer = str(creation_receipt["from"]).lower()

    def reverse_name(label: str, address: str) -> str | None:
        node = common.namehash(address.removeprefix("0x") + ".addr.reverse")
        resolver = common.abi_address(call(f"{label}-reverse-resolver", common.ENS_REGISTRY, "resolver(bytes32)", node), "resolver")
        if resolver == ZERO_ADDRESS:
            return None
        return common.abi_string(call(f"{label}-reverse-name", resolver, "name(bytes32)", node), "name")

    owner_name = reverse_name("damage-control-owner", dc_owner)
    deployer_name = reverse_name("damage-control-deployer", deployer)
    xcopy_node = common.namehash("xcopy.eth")
    xcopy_resolver = common.abi_address(call("xcopy-eth-resolver", common.ENS_REGISTRY, "resolver(bytes32)", xcopy_node), "resolver")
    xcopy_addr = common.abi_address(call("xcopy-eth-addr", xcopy_resolver, "addr(bytes32)", xcopy_node), "addr")
    variant_name = common.abi_string(call("variant-contract-name", VARIANT_CONTRACT, "name()"), "name")
    uris = {token_id: common.abi_string(call(f"damage-control-uri-{token_id:02d}", DAMAGE_CONTROL, "uri(uint256)", token_id), "uri") for token_id in DAMAGE_CONTROL_TOKEN_IDS}
    metadata = {}
    for token_id, uri in uris.items():
        body, row = collector.http(f"damage-control-metadata-{token_id:02d}", uri, accept="application/json", retain_as=".json")
        document = json.loads(body.decode("utf-8"))
        details = document.get("image_details") or {}
        metadata[token_id] = {
            "uri": uri,
            "name": document.get("name"),
            "created_by": document.get("created_by"),
            "image_format": details.get("format"),
            "image_width": details.get("width"),
            "image_height": details.get("height"),
            "path": row["response_path"],
        }

    # Burn scan and calldata.
    burn_logs: list[dict[str, Any]] = []
    for start in range(FIRST_MINT_BLOCK, target["number"] + 1, SCAN_WINDOW_BLOCKS):
        end = min(start + SCAN_WINDOW_BLOCKS - 1, target["number"])
        for log in collector.rpc(
            f"burn-log-scan-{start}-{end}",
            "eth_getLogs",
            [{"address": CONTRACT, "topics": [TRANSFER_TOPIC, None, common.address_topic(ZERO_ADDRESS)], "fromBlock": hex(start), "toBlock": hex(end)}],
            endpoint=BATCH_RPC_URL,
            group="burn-log-scan",
        ):
            burn_logs.append({"token_id": int(log["topics"][3], 16), "transaction_hash": log["transactionHash"].lower(), "block_number": common.hex_int(log["blockNumber"], "block")})
    burn_hashes = sorted({row["transaction_hash"] for row in burn_logs})
    txs: dict[str, dict[str, Any]] = {}
    for start in range(0, len(burn_hashes), TX_BATCH):
        chunk = burn_hashes[start : start + TX_BATCH]
        for tx_hash, tx in zip(chunk, collector.batch(f"burn-transactions-{start:05d}", [("eth_getTransactionByHash", [tx]) for tx in chunk], group="burn-transactions")):
            if str(tx.get("hash", "")).lower() != tx_hash:
                raise EvidenceError(f"burn transaction lookup failed: {tx_hash}")
            txs[tx_hash] = tx
    burns_per_tx = Counter(row["transaction_hash"] for row in burn_logs)
    extension_hashes = [tx for tx in burn_hashes if str(txs[tx].get("to", "")).lower() == BURN_REDEEM_EXTENSION]
    instances: dict[int, dict[str, Any]] = {}
    burners: set[str] = set()
    for tx_hash in extension_hashes:
        tx = txs[tx_hash]
        burners.add(str(tx["from"]).lower())
        calls = decode_burn_redeem(tx["input"])
        decoded_burns = 0
        for row in calls:
            if row["creator_contract"] != DAMAGE_CONTROL:
                raise EvidenceError("burn-redeem call targets another creator contract")
            entry = instances.setdefault(row["instance_id"], {"redemptions": 0, "max_pain_burned": 0, "transactions": set(), "blocks": []})
            entry["redemptions"] += row["redeem_count"]
            burned = sum(1 for token in row["burn_tokens"] if token["contract"] == CONTRACT)
            entry["max_pain_burned"] += burned
            decoded_burns += burned
            entry["transactions"].add(tx_hash)
            entry["blocks"].append(common.hex_int(tx["blockNumber"], "block"))
        if decoded_burns != burns_per_tx[tx_hash]:
            raise EvidenceError(f"{tx_hash}: decoded MAX PAIN burns differ from Transfer logs")
    configs = {
        instance_id: decode_burn_redeem_config(call(f"burn-redeem-config-{instance_id}", BURN_REDEEM_EXTENSION, "getBurnRedeem(address,uint256)", DAMAGE_CONTROL, instance_id))
        for instance_id in sorted(instances)
    }
    by_location = {uri.rsplit("/", 1)[-1]: token_id for token_id, uri in uris.items()}
    works = []
    for instance_id, entry in instances.items():
        config = configs[instance_id]
        token_id = by_location.get(config["location"])
        if token_id is None:
            raise EvidenceError(f"instance {instance_id} location does not match a DAMAGE CONTROL uri")
        first_block, last_block = min(entry["blocks"]), max(entry["blocks"])
        first = block(f"damage-control-{token_id:02d}-first-burn-block", first_block)
        last = block(f"damage-control-{token_id:02d}-last-burn-block", last_block) if last_block != first_block else first
        works.append(
            {
                "damage_control_token_id": token_id,
                "title": metadata[token_id]["name"],
                "burn_redeem_instance_id": instance_id,
                "burn_requirement": [
                    {"required_count": group["required_count"], "items": [{"contract_role": "max_pain" if item["contract"] == CONTRACT else ("damage_control" if item["contract"] == DAMAGE_CONTROL else "other"), "token_spec": item["token_spec"], "amount": item["amount"], "min_token_id": item["min_token_id"], "max_token_id": item["max_token_id"]} for item in group["items"]]}
                    for group in config["burn_set"]
                ],
                "cost_wei": config["cost_wei"],
                "cost_eth": common.wei_to_eth_string(int(config["cost_wei"])),
                "window_start": config["start_date"],
                "window_end": config["end_date"],
                "redemptions_by_burn": entry["redemptions"],
                "contract_redeemed_count": config["redeemed_count"],
                "max_pain_burned": entry["max_pain_burned"],
                "transactions": len(entry["transactions"]),
                "first_burn": {"block": first["number"], "time": first["timestamp"]},
                "last_burn": {"block": last["number"], "time": last["timestamp"]},
            }
        )
    works.sort(key=lambda row: row["damage_control_token_id"])

    # Burns through the block of XCOPY's 21 March 2024 post.
    low, high = FIRST_MINT_BLOCK, target["number"]
    while low < high:
        middle = (low + high + 1) // 2
        header = collector.rpc(f"boundary-search-{middle}", "eth_getBlockByNumber", [hex(middle), False], group="boundary-search")
        if common.hex_int(header["timestamp"], "ts") <= POST_2024_03_21_UNIX:
            low = middle
        else:
            high = middle - 1
    boundary = block("post-2024-03-21-boundary-block", low)
    boundary_next = block("post-2024-03-21-next-block", low + 1)
    burns_through_boundary = sum(1 for row in burn_logs if row["block_number"] <= low)

    first_burn_block = min(row["block_number"] for row in burn_logs)
    last_redemption_block = max(max(entry["blocks"]) for entry in instances.values())
    first_burn = block("first-burn-block", first_burn_block)
    last_redemption = block("last-redemption-burn-block", last_redemption_block)
    hash_list = ("\n".join(burn_hashes) + "\n").encode("ascii")
    common.write_bytes(output / "derived/burn-transaction-hashes.txt", hash_list)
    redemptions = {
        "record_id": f"{RECORD_ID}.DAMAGE-CONTROL-REDEMPTIONS",
        "method": (
            f"Complete eth_getLogs scan on {BATCH_RPC_URL} of MAX PAIN Transfer logs to the zero address, {SCAN_WINDOW_BLOCKS}-block "
            f"windows from block {FIRST_MINT_BLOCK} to {target['number']}; eth_getTransactionByHash for every burn transaction; "
            "burnRedeem calldata decoded per call (instance, redemption count, burn tokens) and checked against each transaction's "
            "Transfer logs; getBurnRedeem(address,uint256) read for each instance at the target block; instances matched to tokens by "
            "their Arweave location and uri(n)."
        ),
        "scan_block_range": [FIRST_MINT_BLOCK, target["number"]],
        "burn_transaction_hash_list": {
            "path": "derived/burn-transaction-hashes.txt",
            "sha256": f"sha256:{common.sha256(hash_list)}",
            "count": len(burn_hashes),
            "canonicalization": "lowercase 0x transaction hashes sorted ascending, one per line, LF-terminated",
        },
        "works": works,
        "totals": {
            "burn_logs": len(burn_logs),
            "burn_transactions": len(burn_hashes),
            "burns_through_burn_redeem_extension": sum(burns_per_tx[tx] for tx in extension_hashes),
            "burn_redeem_transactions": len(extension_hashes),
            "single_call_transactions": sum(1 for tx in extension_hashes if txs[tx]["input"].startswith(SINGLE_BURN_REDEEM)),
            "batch_call_transactions": sum(1 for tx in extension_hashes if txs[tx]["input"].startswith(BATCH_BURN_REDEEM)),
            "redemptions_by_burn": sum(row["redemptions_by_burn"] for row in works),
            "distinct_burn_redeem_accounts": len(burners),
            "burns_in_other_transactions": len(burn_logs) - sum(burns_per_tx[tx] for tx in extension_hashes),
            "first_burn": {"block": first_burn["number"], "time": first_burn["timestamp"]},
            "last_redemption_burn": {"block": last_redemption["number"], "time": last_redemption["timestamp"]},
            "burns_through_2024_03_21_post_block": {
                "boundary_block": boundary["number"],
                "boundary_block_time": boundary["timestamp"],
                "next_block_time": boundary_next["timestamp"],
                "post_time": common.iso_from_unix(POST_2024_03_21_UNIX),
                "burns": burns_through_boundary,
                "existing_after": (LAST_TOKEN_ID - FIRST_TOKEN_ID + 1) - burns_through_boundary,
            },
        },
        "privacy_boundary": "Counts only. No burner, payer or caller address is retained; scan and transaction responses are committed by SHA-256.",
        "interpretation_boundary": "contract_redeemed_count is the burn-redeem extension's counter and includes redemptions that were not paid by burning (for example airdrops); redemptions_by_burn counts only burn-redeem calls.",
    }
    common.write_bytes(output / "derived/damage-control-redemptions.json", common.pretty_json(redemptions))
    mint_record = {
        "transactions": mints,
        "first_block": mint_first,
        "last_block": mint_last,
        "token_ids_covered": covered,
        "transaction_count": len(mints),
    }
    common.write_bytes(output / "derived/mint-transactions.json", common.pretty_json(mint_record))

    # Public web readings.
    memes_raw, memes_row = collector.http("memes-card-47", MEMES_CARD_URL, accept="application/json", retain_as=None, group="public-safe-projections")
    memes = memes_projection(memes_raw)
    memes["raw_response"] = {"sha256": memes_row["response_sha256"], "size": memes_row["response_size"], "retained": False, "reason": "The response carries holder and offer account addresses."}
    common.write_bytes(output / "projections/memes-card-47.json", common.pretty_json(memes))
    tumblr_raw, tumblr_row = collector.http(
        "tumblr-earliest-post", TUMBLR_URL_TEMPLATE.format(start=TUMBLR_TOTAL_POSTS_HINT - 1), accept="*/*", retain_as=".txt"
    )
    tumblr_text = tumblr_raw.decode("utf-8")
    tumblr = json.loads(tumblr_text[tumblr_text.index("{") : tumblr_text.rindex("}") + 1])
    earliest = tumblr["posts"][0]
    if int(tumblr["posts-total"]) != TUMBLR_TOTAL_POSTS_HINT or "<script" in tumblr_text.lower():
        raise EvidenceError("Tumblr post total changed or the response embeds a script")
    wayback_raw, wayback_row = collector.http("nifty-gateway-drop-page-wayback", WAYBACK_DROP_URL, accept="text/html", retain_as=None, group="citation-sources")
    if common.sha256(wayback_raw) != WAYBACK_DROP_SHA256:
        raise EvidenceError("Wayback capture bytes differ from the source package's recorded capture")
    position = wayback_raw.find(FLASHING_CITATION.encode("utf-8"))
    if position < 0:
        raise EvidenceError("creator-profile flashing warning not found in the capture")
    prefix = wayback_raw[max(0, position - 200) : position]
    context_bytes = prefix[prefix.rfind(b'"') + 1 :] + FLASHING_CITATION.encode("utf-8")
    context_text = context_bytes.decode("utf-8").replace("\\\\n", "\n").replace("\\n", "\n")
    context_text = " / ".join(line.strip() for line in context_text.split("\n") if line.strip())
    citation = {
        "source_url": WAYBACK_DROP_URL,
        "raw_sha256": f"sha256:{WAYBACK_DROP_SHA256}",
        "raw_size": len(wayback_raw),
        "raw_retained": False,
        "raw_reason": "Raw HTML embeds executable script elements; the citation is retained with its byte offset.",
        "citations": [
            {
                "field": "creator profile bio (Next.js flight data, artist name XCOPY)",
                "text": FLASHING_CITATION,
                "byte_offset": position,
                "context_text": context_text,
                "context_canonicalization": "bytes from the opening quotation mark of the string that holds the citation, with escaped newlines read as line breaks and lines joined by ' / '",
            }
        ],
    }
    common.write_bytes(output / "citations/nifty-gateway-creator-profile.json", common.pretty_json(citation))
    wave_messages = []
    for drop_id, purpose in WAVE_MESSAGES:
        raw, row = collector.http(f"wave-message-{purpose}", f"{DROPS_API}{drop_id}", accept="application/json", retain_as=None, group="public-safe-projections")
        projection = wave_projection(raw, drop_id, purpose, output)
        projection["raw_response"] = {"sha256": row["response_sha256"], "size": row["response_size"], "retained": False, "reason": "The response contains profile objects with wallet addresses."}
        common.write_bytes(output / f"wave/{purpose}.json", common.pretty_json(projection))
        wave_messages.append({key: projection[key] for key in ("purpose", "drop_id", "serial_no", "created_at", "author_handle")} | {"path": f"wave/{purpose}.json"})

    summary = {
        "record_id": RECORD_ID,
        "record_type": "XCOPY_MAX_PAIN_4188_SUPPLEMENTARY_READINGS",
        "accession_id": common.ACCESSION_ID,
        "object_id": common.OBJECT_ID,
        "observed_at": observed_at,
        "target_block": target,
        "rpc_endpoint": PRIMARY_RPC_URL,
        "batch_rpc_endpoint": BATCH_RPC_URL,
        "edition_3265": edition_3265_record,
        "mint_transactions": {"path": "derived/mint-transactions.json", "count": len(mints), "first_block": mint_first, "last_block": mint_last},
        "contract_identity": {
            "damage_control": {
                "contract": DAMAGE_CONTROL,
                "owner_ens_reverse_name": owner_name,
                "deployer_ens_reverse_name": deployer_name,
                "owner_equals_deployer": dc_owner == deployer,
                "owner_equals_xcopy_eth_forward_resolution": dc_owner == xcopy_addr,
                "creation_transaction": creation_tx,
                "creation_located_by": {"source": "Blockscout address API (class D)", "url": BLOCKSCOUT_ADDRESS_URL, "response_sha256": blockscout_row["response_sha256"], "verified_by": "eth_getTransactionReceipt contractAddress (class A)"},
                "uri": {str(token_id): uri for token_id, uri in uris.items()},
                "metadata": {str(token_id): row for token_id, row in metadata.items()},
            },
            "variant_contract": {"contract": VARIANT_CONTRACT, "name": variant_name},
            "address_boundary": "The owner and deployer account addresses are retained only in the raw RPC responses; derived fields give their ENS names.",
        },
        "damage_control_redemptions": {"path": "derived/damage-control-redemptions.json", "totals": redemptions["totals"]},
        "memes_card_47": {"path": "projections/memes-card-47.json", "image_format": (memes.get("metadata_image_details") or {}).get("format")},
        "tumblr_earliest_post": {
            "path": next(row["response_path"] for row in collector.raw if row["label"] == "tumblr-earliest-post"),
            "posts_total": int(tumblr["posts-total"]),
            "post_id": earliest.get("id"),
            "url": earliest.get("url"),
            "type": earliest.get("type"),
            "date_gmt": earliest.get("date-gmt"),
            "tags": earliest.get("tags"),
            "boundary": "The keyless v1 API lists posts that exist now; deleted earlier posts would not appear.",
        },
        "nifty_gateway_creator_profile": {"path": "citations/nifty-gateway-creator-profile.json", "text": FLASHING_CITATION},
        "wave_messages": wave_messages,
        "wave_messages_not_found": [
            {"described_as": "organizer message of 9 September 2026 on the residual", "search": f"all {ORGANIZER_HANDLE} drops in the Museum Wave", "result": "no such message; the organizer's 9 September drop concerns the essay"}
        ],
        "raw_rpc": collector.raw,
        "commitments": {group: collector.group_summary(group) for group in sorted(collector.commitments)},
        "limitations": [
            "These are point-in-time public readings. They do not establish title, rights, the meaning of a redemption program, or any person's identity.",
            "Blockscout (class D) only locates the DAMAGE CONTROL creation transaction; the receipt read by RPC verifies it.",
            "The Wave transcripts omit contributor mentions, per-person payment status and the acquisition wallet address; the exact part text is committed by SHA-256.",
        ],
    }
    common.write_bytes(output / "summary.json", common.pretty_json(summary))
    entries = []
    for path in sorted(p for p in output.rglob("*") if p.is_file() and p.name != "manifest.json"):
        relative = path.relative_to(output).as_posix()
        media_type = "application/json" if path.suffix == ".json" else "text/plain; charset=utf-8"
        entries.append(common.entry_for(output, path, media_type, source_id=relative.replace("/", "-").rsplit(".", 1)[0]))
    manifest = {
        "byte_mode": "raw",
        "entries": entries,
        "hash_algorithm": "sha256",
        "manifest_type": "6529NM_XCOPY_MAX_PAIN_4188_SUPPLEMENTARY_EVIDENCE",
        "manifest_version": "1.0.0",
        "observed_at": observed_at,
        "record_id": RECORD_ID,
        "subject_id": common.OBJECT_ID,
    }
    common.write_bytes(output / "manifest.json", common.pretty_json(manifest))
    return {"status": "complete", "entries": len(entries), "manifest_sha256": f"sha256:{common.sha256((output / 'manifest.json').read_bytes())}", "totals": redemptions["totals"]}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args(argv)
    try:
        result = acquire(args.output_dir.resolve())
    except (EvidenceError, OSError, ValueError, KeyError) as exc:
        print(f"MAX PAIN supplementary evidence acquisition refused: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
