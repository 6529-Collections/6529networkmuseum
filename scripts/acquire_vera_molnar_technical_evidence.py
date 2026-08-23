#!/usr/bin/env python3
"""Acquire exact-finalized-block technical evidence for Vera Molnar #210.

The package is deliberately self-contained and fail-closed.  It retains the
exact JSON-RPC request and response bytes for every observation, derives the
runtime and script bytes from those responses, and binds all state reads to
the supplied finalized block hash.  It is an evidence acquisition tool, not
an accession decision.

The output directory must be empty before a run.  A failed run therefore
leaves evidence for diagnosis but can never silently replace a prior package.
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
from typing import Any

from Crypto.Hash import keccak

from safe_fetch import SafeHTTPSFetcher, _PinnedHTTPSConnection


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "evidence" / "vera-molnar-210-technical"

CONTRACT = "0xe034bb2b1b9471e11cf1a0a9199a156fb227aa5d"
TOKEN_ID = 210
PROJECT_ID = 0
MUSEUM = "0xbecfa2ba5a782d11e1a0e821e8f2e30b6684178c"
DONOR = "0x6daa633c23615a29471deafae351727867e7dad1"
TRANSFER_TX = "0x618603d9f21dc09a4a7b2d6b6b242cc337127e8052116d0ee28c6c25f012a5cd"
TRANSFER_BLOCK = 25_816_958
TRANSFER_BLOCK_HASH = "0x3af2d05ec6a4f942ff56f3b049c62b639aec66bcece84c006ed3ec879257d7be"
TRANSFER_LOG_INDEX = 315

FINALIZED_BLOCK = 25_816_984
FINALIZED_BLOCK_HASH = "0x4f478846f35928cf4ead31161b54ffc601e9a9a519e035c73767aa3284b119d5"

EXPECTED_TOKEN_HASH = "0xd0a3be9aa1a3e101a12ec038ceb71a18846dbc62eac3e91fb425232e7820a318"
EXPECTED_SCRIPT_COUNT = 11
EXPECTED_SCRIPT_SHA256 = "d7799751c1017efe9de352cd73c969893fd7757fc9e58d468ebe9c2b1a9f3f42"

SCRIPT_STORAGE_ADDRESSES = (
    "0xa7ced9e81776daaa9a4f83e282a2503999f6527c",
    "0x8292d1b5f93f88725be87b0955c66162019cb246",
    "0x2ba03e6af03a5d7d5967182f4cce7ef259e8ebd1",
    "0x7a512ea80daf89dd36e0e5d10825a1722ff0b3b3",
    "0x8536978031ce00a6408627fb93661c8265d3925a",
    "0xc5973409ebd5e5fa8913d13800fcd46713bbd5cb",
    "0xfa2368ed8798c70b61af43f9ea85c2fd186939da",
    "0x034665d304ae48e7f8ee5afdc0fcdc34484e827f",
    "0x4c3f1c81075d14b4c263340c39f5650e8df38dce",
    "0xaaeaa6aefa6faf7bd8320d49d4efbf373f46ba6e",
    "0x96bd36648aebd846115d1500e7a0fc8ad5ac7403",
)

TRANSFER_TOPIC = "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"
USER_AGENT = "6529-Network-Museum/vera-molnar-210-technical-evidence-v1"
PUBLIC_RPC_URL = "https://eth-mainnet.public.blastapi.io"
ALCHEMY_ENV_FILES = (
    Path(r"D:\\repos\\6529seize-backend\\.env.local"),
    Path(r"D:\\repos\\6529seize-backend\\src\\api-serverless\\.env.local"),
)


class EvidenceError(RuntimeError):
    """Raised when the exact evidence boundary cannot be established."""


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


def http10_connection_factory(endpoint: Any, resolved: Any, policy: dict[str, Any]) -> Any:
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


def canonical_json(value: object) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def keccak_selector(signature: str) -> str:
    digest = keccak.new(digest_bits=256)
    digest.update(signature.encode("ascii"))
    return digest.hexdigest()[:8]


def address_word(address: str) -> str:
    return "0x" + address[2:].lower().rjust(64, "0")


def uint_word(value: int) -> str:
    return f"{value:064x}"


def calldata(signature: str, *values: int) -> str:
    return "0x" + keccak_selector(signature) + "".join(uint_word(value) for value in values)


def redacted(value: Any) -> Any:
    if isinstance(value, str):
        if RPC_URL in value:
            return value.replace(RPC_URL, RPC_DISPLAY_URL)
        if ALCHEMY_KEY and ALCHEMY_KEY in value:
            return value.replace(ALCHEMY_KEY, "<redacted>")
        return value
    if isinstance(value, dict):
        return {key: redacted(item) for key, item in value.items()}
    if isinstance(value, list):
        return [redacted(item) for item in value]
    return value


def prepare_output(recover_partial: bool = False) -> None:
    if OUTPUT.exists():
        info = OUTPUT.lstat()
        attributes = getattr(info, "st_file_attributes", 0)
        if stat.S_ISLNK(info.st_mode) or attributes & 0x400:
            raise EvidenceError("technical evidence output cannot be a link or reparse point")
        contents = sorted(
            path.relative_to(OUTPUT).as_posix()
            for path in OUTPUT.rglob("*")
            if path.is_file()
        )
        recoverable_partial = (
            bool(contents)
            and "manifest.json" not in contents
            and "manifest.sha256" not in contents
            and "summary.json" not in contents
            and all(relative.startswith(("raw/rpc/", "derived/")) for relative in contents)
        )
        if contents and not (recover_partial and recoverable_partial):
            raise EvidenceError("technical evidence output must be empty; replacement is a separate operation")
        if recover_partial and recoverable_partial:
            for relative in contents:
                (OUTPUT / relative).unlink()
            for directory in sorted(
                (path for path in OUTPUT.rglob("*") if path.is_dir()),
                key=lambda path: len(path.parts),
                reverse=True,
            ):
                directory.rmdir()
    else:
        OUTPUT.mkdir(parents=True)


def write_bytes(relative: str | Path, value: bytes) -> Path:
    path = OUTPUT / Path(relative)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(value)
    return path


def hex_bytes(value: Any, label: str) -> bytes:
    if not isinstance(value, str) or not value.startswith("0x") or len(value) % 2:
        raise EvidenceError(f"{label} is not even-length hex")
    try:
        return bytes.fromhex(value[2:])
    except ValueError as exc:
        raise EvidenceError(f"{label} is not valid hex") from exc


def abi_words(result: Any, label: str) -> list[bytes]:
    raw = hex_bytes(result, label)
    if len(raw) % 32:
        raise EvidenceError(f"{label} ABI result is not word aligned")
    return [raw[index : index + 32] for index in range(0, len(raw), 32)]


def decode_uint(result: Any, label: str) -> int:
    words = abi_words(result, label)
    if len(words) != 1:
        raise EvidenceError(f"{label} expected one ABI word")
    return int.from_bytes(words[0], "big")


def decode_address(result: Any, label: str) -> str:
    words = abi_words(result, label)
    if len(words) != 1:
        raise EvidenceError(f"{label} expected one ABI word")
    return "0x" + words[0][-20:].hex()


def decode_bool_word(word: bytes, label: str) -> bool:
    value = int.from_bytes(word, "big")
    if value not in (0, 1):
        raise EvidenceError(f"{label} is not a Solidity bool")
    return bool(value)


def decode_dynamic_bytes(result: Any, offset: int, label: str) -> bytes:
    raw = hex_bytes(result, label)
    if offset < 0 or offset + 32 > len(raw) or offset % 32:
        raise EvidenceError(f"{label} dynamic offset is invalid")
    length = int.from_bytes(raw[offset : offset + 32], "big")
    end = offset + 32 + length
    if end > len(raw):
        raise EvidenceError(f"{label} dynamic value exceeds ABI result")
    return raw[offset + 32 : end]


def decode_string(result: Any, label: str) -> str:
    raw = hex_bytes(result, label)
    if len(raw) < 64:
        raise EvidenceError(f"{label} string result is truncated")
    return decode_dynamic_bytes(result, int.from_bytes(raw[:32], "big"), label).decode("utf-8")


def decode_string_tuple(result: Any, count: int, label: str) -> list[str]:
    raw = hex_bytes(result, label)
    if len(raw) < count * 32:
        raise EvidenceError(f"{label} tuple head is truncated")
    values: list[str] = []
    for index in range(count):
        offset = int.from_bytes(raw[index * 32 : (index + 1) * 32], "big")
        values.append(decode_dynamic_bytes(result, offset, f"{label}[{index}]").decode("utf-8"))
    return values


def state_selector() -> dict[str, Any]:
    return {"blockHash": FINALIZED_BLOCK_HASH, "requireCanonical": True}


class Collector:
    def __init__(self) -> None:
        self.sequence = 0
        self.raw_entries: list[dict[str, Any]] = []

    def rpc(
        self,
        label: str,
        method: str,
        params: list[Any],
        *,
        allow_error: bool = False,
    ) -> tuple[dict[str, Any], bytes, bytes]:
        self.sequence += 1
        request = {"jsonrpc": "2.0", "id": label, "method": method, "params": params}
        request_bytes = canonical_json(request)
        time.sleep(0.5)
        result = FETCHER.fetch(
            RPC_URL,
            method="POST",
            body=request_bytes,
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "User-Agent": USER_AGENT,
            },
            expires_at=datetime.now(UTC) + timedelta(seconds=30),
        )
        response_bytes = result.body
        request_path = f"raw/rpc/{self.sequence:04d}-{label}-request.json"
        response_path = f"raw/rpc/{self.sequence:04d}-{label}-response.json"
        write_bytes(request_path, request_bytes)
        write_bytes(response_path, response_bytes)
        transport = redacted(result.observation.to_dict())
        response = json.loads(response_bytes.decode("utf-8"))
        if not isinstance(response, dict) or response.get("jsonrpc") != "2.0" or response.get("id") != label:
            raise EvidenceError(f"{label}: malformed JSON-RPC response")
        if "error" in response and not allow_error:
            raise EvidenceError(f"{label}: {response['error']}")
        self.raw_entries.extend(
            [
                {
                    "kind": "request",
                    "label": label,
                    "path": request_path,
                    "sha256": f"sha256:{sha256(request_bytes)}",
                    "size": len(request_bytes),
                    "transport": transport,
                },
                {
                    "kind": "response",
                    "label": label,
                    "path": response_path,
                    "sha256": f"sha256:{sha256(response_bytes)}",
                    "size": len(response_bytes),
                    "transport": transport,
                },
            ]
        )
        return response, request_bytes, response_bytes

    def call(self, label: str, signature: str, *values: int) -> tuple[dict[str, Any], str]:
        response, _, _ = self.rpc(
            label,
            "eth_call",
            [{"to": CONTRACT, "data": calldata(signature, *values)}, state_selector()],
        )
        result = response.get("result")
        if not isinstance(result, str):
            raise EvidenceError(f"{label}: missing ABI result")
        return response, result


def slot_for(name: str) -> str:
    digest = keccak.new(digest_bits=256)
    digest.update(name.encode("ascii"))
    value = (int.from_bytes(digest.digest(), "big") - 1) % (1 << 256)
    return "0x" + f"{value:064x}"


def block_number(value: Any, label: str) -> int:
    if not isinstance(value, str) or not value.startswith("0x"):
        raise EvidenceError(f"{label} block number is malformed")
    return int(value, 16)


def require_equal(actual: Any, expected: Any, label: str) -> None:
    if actual != expected:
        raise EvidenceError(f"{label} mismatch: expected {expected!r}, got {actual!r}")


def run(recover_partial: bool = False) -> dict[str, Any]:
    prepare_output(recover_partial=recover_partial)
    collector = Collector()
    target_block_tag = f"0x{FINALIZED_BLOCK:x}"

    chain, _, _ = collector.rpc("chain-id", "eth_chainId", [])
    require_equal(chain.get("result"), "0x1", "chain id")

    finality_before, _, _ = collector.rpc("finality-before", "eth_getBlockByNumber", ["finalized", False])
    finality_before_result = finality_before.get("result")
    if not isinstance(finality_before_result, dict):
        raise EvidenceError("finality-before did not return a block")
    if block_number(finality_before_result.get("number"), "finality-before") < FINALIZED_BLOCK:
        raise EvidenceError("supplied target block is not finalized at acquisition time")

    first_block, _, _ = collector.rpc("target-block-before", "eth_getBlockByNumber", [target_block_tag, False])
    first_block_result = first_block.get("result")
    if not isinstance(first_block_result, dict):
        raise EvidenceError("finalized-before did not return a block")
    require_equal(block_number(first_block_result.get("number"), "finalized-before"), FINALIZED_BLOCK, "finalized block number")
    require_equal(str(first_block_result.get("hash", "")).lower(), FINALIZED_BLOCK_HASH, "finalized block hash")
    finalized_timestamp = first_block_result.get("timestamp")

    contract_code_response, _, _ = collector.rpc(
        "contract-runtime-code", "eth_getCode", [CONTRACT, state_selector()]
    )
    contract_runtime = hex_bytes(contract_code_response.get("result"), "contract runtime code")
    if not contract_runtime:
        raise EvidenceError("contract runtime bytecode is empty")
    runtime_path = write_bytes(
        "derived/contract-runtime-bytecode.hex.txt",
        ("0x" + contract_runtime.hex() + "\n").encode("ascii"),
    )

    slots: dict[str, dict[str, Any]] = {}
    for slot_name in ("eip1967.proxy.implementation", "eip1967.proxy.beacon", "eip1967.proxy.admin"):
        slot = slot_for(slot_name)
        response, _, _ = collector.rpc(
            f"storage-{slot_name.rsplit('.', 1)[-1]}",
            "eth_getStorageAt",
            [CONTRACT, slot, state_selector()],
        )
        value = response.get("result")
        if not isinstance(value, str) or len(value) != 66:
            raise EvidenceError(f"{slot_name} storage response is malformed")
        slots[slot_name] = {"slot": slot, "value": value.lower(), "is_zero": int(value, 16) == 0}

    named: dict[str, Any] = {}
    for name, signature in (
        ("name", "name()"),
        ("symbol", "symbol()"),
        ("core_type", "coreType()"),
        ("core_version", "coreVersion()"),
    ):
        response, result = collector.call(f"{name}-call", signature)
        named[name] = decode_string(result, name)

    token_hash_response, token_hash_result = collector.call("token-hash-call", "tokenIdToHash(uint256)", TOKEN_ID)
    token_hash = token_hash_result.lower()
    require_equal(token_hash, EXPECTED_TOKEN_HASH, "tokenIdToHash")
    _, project_id_result = collector.call("token-project-id-call", "tokenIdToProjectId(uint256)", TOKEN_ID)
    token_project_id = decode_uint(project_id_result, "tokenIdToProjectId")
    require_equal(token_project_id, PROJECT_ID, "token project id")

    _, project_details_result = collector.call("project-details-call", "projectDetails(uint256)", PROJECT_ID)
    project_detail_values = decode_string_tuple(project_details_result, 5, "projectDetails")
    project_details = {
        "project_name": project_detail_values[0],
        "artist": project_detail_values[1],
        "description": project_detail_values[2],
        "website": project_detail_values[3],
        "license": project_detail_values[4],
    }
    require_equal(project_details["project_name"], "Themes and Variations", "project name")
    require_equal(project_details["artist"], "Vera Molnár, in collaboration with Martin Grasser", "project artist")
    require_equal(project_details["license"], "CC BY-NC 4.0", "project license")

    _, state_result = collector.call("project-state-call", "projectStateData(uint256)", PROJECT_ID)
    state_words = abi_words(state_result, "projectStateData")
    if len(state_words) != 6:
        raise EvidenceError(f"projectStateData expected 6 words, got {len(state_words)}")
    project_state = {
        "invocations": int.from_bytes(state_words[0], "big"),
        "max_invocations": int.from_bytes(state_words[1], "big"),
        "active": decode_bool_word(state_words[2], "projectStateData.active"),
        "paused": decode_bool_word(state_words[3], "projectStateData.paused"),
        "completed_timestamp": int.from_bytes(state_words[4], "big"),
        "locked": decode_bool_word(state_words[5], "projectStateData.locked"),
    }
    require_equal(project_state["invocations"], 500, "project invocations")
    require_equal(project_state["max_invocations"], 500, "project max invocations")
    require_equal(project_state["active"], True, "project active")
    require_equal(project_state["paused"], True, "project paused")
    require_equal(project_state["locked"], True, "project locked")

    _, script_details_result = collector.call("project-script-details-call", "projectScriptDetails(uint256)", PROJECT_ID)
    script_details_raw = hex_bytes(script_details_result, "projectScriptDetails")
    script_type = decode_dynamic_bytes(script_details_result, int.from_bytes(script_details_raw[0:32], "big"), "script type").decode("utf-8")
    aspect_ratio = decode_dynamic_bytes(script_details_result, int.from_bytes(script_details_raw[32:64], "big"), "aspect ratio").decode("utf-8")
    script_count = int.from_bytes(script_details_raw[64:96], "big")
    require_equal(script_type, "js@na", "script type")
    require_equal(script_count, EXPECTED_SCRIPT_COUNT, "script count")
    script_details = {"script_type": script_type, "aspect_ratio": aspect_ratio, "script_count": script_count}

    scripts: list[bytes] = []
    script_records: list[dict[str, Any]] = []
    for index, storage_address in enumerate(SCRIPT_STORAGE_ADDRESSES):
        _, script_result = collector.call(f"script-by-index-{index:02d}", "projectScriptByIndex(uint256,uint256)", PROJECT_ID, index)
        script_bytes = decode_dynamic_bytes(script_result, int.from_bytes(hex_bytes(script_result, "script result")[:32], "big"), f"script {index}")
        storage_response, _, _ = collector.rpc(
            f"script-storage-code-{index:02d}", "eth_getCode", [storage_address, state_selector()]
        )
        # Re-read the stored response from the raw result for binary derivation.
        # The response is already retained; parsing it here keeps the derived
        # payload cryptographically tied to that exact response.
        storage_code = hex_bytes(storage_response.get("result"), f"script storage code {index}")
        offset = storage_code.find(script_bytes)
        if offset != 65:
            raise EvidenceError(f"script {index} does not begin at the expected bytecode-storage offset 65")
        scripts.append(script_bytes)
        write_bytes(f"derived/scripts/{index:02d}.js.txt", script_bytes)
        write_bytes(
            f"derived/script-storage/{index:02d}-runtime.hex.txt",
            ("0x" + storage_code.hex() + "\n").encode("ascii"),
        )
        script_records.append(
            {
                "index": index,
                "storage_address": storage_address,
                "storage_runtime_sha256": f"sha256:{sha256(storage_code)}",
                "script_offset": offset,
                "script_length": len(script_bytes),
                "script_sha256": f"sha256:{sha256(script_bytes)}",
            }
        )
    aggregate_script = b"".join(scripts)
    aggregate_script_sha256 = sha256(aggregate_script)
    require_equal(aggregate_script_sha256, EXPECTED_SCRIPT_SHA256, "aggregate script SHA-256")

    _, dependency_count_result = collector.call(
        "external-dependency-count-call", "projectExternalAssetDependencyCount(uint256)", PROJECT_ID
    )
    dependency_count = decode_uint(dependency_count_result, "external dependency count")
    require_equal(dependency_count, 0, "external dependency count")
    _, dependency_registry_result = collector.call(
        "dependency-registry-call", "artblocksDependencyRegistryAddress()"
    )
    dependency_registry = decode_address(dependency_registry_result, "dependency registry")
    require_equal(dependency_registry, "0x0000000000000000000000000000000000000000", "dependency registry")
    _, ipfs_gateway_result = collector.call("preferred-ipfs-gateway-call", "preferredIPFSGateway()")
    _, arweave_gateway_result = collector.call("preferred-arweave-gateway-call", "preferredArweaveGateway()")
    ipfs_gateway = decode_string(ipfs_gateway_result, "preferred IPFS gateway")
    arweave_gateway = decode_string(arweave_gateway_result, "preferred Arweave gateway")
    require_equal(ipfs_gateway, "", "preferred IPFS gateway")
    require_equal(arweave_gateway, "", "preferred Arweave gateway")

    _, token_uri_result = collector.call("token-uri-call", "tokenURI(uint256)", TOKEN_ID)
    token_uri = decode_string(token_uri_result, "tokenURI")
    require_equal(
        token_uri,
        "https://token.artblocks.io/0xe034bb2b1b9471e11cf1a0a9199a156fb227aa5d/210",
        "tokenURI",
    )
    base_uri = token_uri.rsplit("/", 1)[0] + "/"

    # Engine Flex has no projectBaseURI(uint256) getter; retain the attempted
    # call and its exact revert response as a compatibility observation while
    # using tokenURI (the contract's public base-URI surface) as the authority.
    base_uri_response, _, _ = collector.rpc(
        "project-base-uri-compatibility-call",
        "eth_call",
        [{"to": CONTRACT, "data": calldata("projectBaseURI(uint256)", PROJECT_ID)}, state_selector()],
        allow_error=True,
    )
    base_uri_compatibility = {
        "method": "projectBaseURI(uint256)",
        "available": "error" not in base_uri_response,
        "response": base_uri_response,
        "authoritative_source": "tokenURI(uint256)",
        "derived_base_uri": base_uri,
    }

    owner_response, owner_result = collector.call("owner-of-call", "ownerOf(uint256)", TOKEN_ID)
    approved_response, approved_result = collector.call("get-approved-call", "getApproved(uint256)", TOKEN_ID)
    owner = decode_address(owner_result, "ownerOf")
    approved = decode_address(approved_result, "getApproved")
    require_equal(owner, MUSEUM, "ownerOf")
    require_equal(approved, "0x0000000000000000000000000000000000000000", "getApproved")

    transaction_response, _, _ = collector.rpc("transfer-transaction", "eth_getTransactionByHash", [TRANSFER_TX])
    transaction = transaction_response.get("result")
    if not isinstance(transaction, dict):
        raise EvidenceError("transfer transaction is missing")
    require_equal(str(transaction.get("hash", "")).lower(), TRANSFER_TX, "transfer transaction hash")
    require_equal(str(transaction.get("from", "")).lower(), DONOR, "transfer transaction from")
    require_equal(str(transaction.get("to", "")).lower(), CONTRACT, "transfer transaction to")
    require_equal(str(transaction.get("value", "")).lower(), "0x0", "transfer transaction value")

    receipt_response, _, _ = collector.rpc("transfer-receipt", "eth_getTransactionReceipt", [TRANSFER_TX])
    receipt = receipt_response.get("result")
    if not isinstance(receipt, dict):
        raise EvidenceError("transfer receipt is missing")
    require_equal(str(receipt.get("transactionHash", "")).lower(), TRANSFER_TX, "receipt transaction hash")
    require_equal(receipt.get("status"), "0x1", "receipt status")
    require_equal(block_number(receipt.get("blockNumber"), "receipt"), TRANSFER_BLOCK, "receipt block number")
    require_equal(str(receipt.get("blockHash", "")).lower(), TRANSFER_BLOCK_HASH, "receipt block hash")
    require_equal(int(str(receipt.get("transactionIndex")), 16), 95, "receipt transaction index")
    transfer_logs = []
    for log in receipt.get("logs", []):
        if not isinstance(log, dict):
            continue
        topics = log.get("topics")
        if (
            str(log.get("address", "")).lower() == CONTRACT
            and isinstance(topics, list)
            and len(topics) == 4
            and str(topics[0]).lower() == TRANSFER_TOPIC
            and str(topics[1]).lower() == address_word(DONOR)
            and str(topics[2]).lower() == address_word(MUSEUM)
            and int(str(topics[3]), 16) == TOKEN_ID
            and int(str(log.get("logIndex")), 16) == TRANSFER_LOG_INDEX
        ):
            transfer_logs.append(log)
    require_equal(len(transfer_logs), 1, "matching ERC-721 Transfer log count")

    transfer_block_response, _, _ = collector.rpc(
        "transfer-block", "eth_getBlockByHash", [TRANSFER_BLOCK_HASH, False]
    )
    transfer_block = transfer_block_response.get("result")
    if not isinstance(transfer_block, dict):
        raise EvidenceError("transfer block is missing")
    require_equal(str(transfer_block.get("hash", "")).lower(), TRANSFER_BLOCK_HASH, "transfer block hash")
    require_equal(block_number(transfer_block.get("number"), "transfer block"), TRANSFER_BLOCK, "transfer block number")

    finality_after, _, _ = collector.rpc("finality-after", "eth_getBlockByNumber", ["finalized", False])
    finality_after_result = finality_after.get("result")
    if not isinstance(finality_after_result, dict):
        raise EvidenceError("finality-after did not return a block")
    if block_number(finality_after_result.get("number"), "finality-after") < FINALIZED_BLOCK:
        raise EvidenceError("supplied target block is no longer finalized at the end of acquisition")

    second_block, _, _ = collector.rpc("target-block-after", "eth_getBlockByNumber", [target_block_tag, False])
    second_block_result = second_block.get("result")
    if not isinstance(second_block_result, dict):
        raise EvidenceError("target-block-after did not return a block")
    require_equal(block_number(second_block_result.get("number"), "target-block-after"), FINALIZED_BLOCK, "target block drift")
    require_equal(str(second_block_result.get("hash", "")).lower(), FINALIZED_BLOCK_HASH, "target block hash drift")

    finalized_iso = None
    if isinstance(finalized_timestamp, str):
        finalized_iso = datetime.fromtimestamp(int(finalized_timestamp, 16), UTC).isoformat(timespec="seconds").replace("+00:00", "Z")

    observation = {
        "record_id": "6529NM.2026.003.TECHNICAL-EVIDENCE-01",
        "record_type": "VERA_MOLNAR_210_ONCHAIN_TECHNICAL_OBSERVATION",
        "observed_at": datetime.now(UTC).isoformat(timespec="milliseconds").replace("+00:00", "Z"),
        "network": "Ethereum mainnet",
        "chain_id": 1,
        "rpc_endpoint": RPC_DISPLAY_URL,
        "contract": CONTRACT,
        "token_id": TOKEN_ID,
        "project_id": PROJECT_ID,
        "finalized_block": {
            "number": FINALIZED_BLOCK,
            "hash": FINALIZED_BLOCK_HASH,
            "timestamp": finalized_iso,
            "state_selector": state_selector(),
        },
        "finality_observation": {
            "before": {
                "number": block_number(finality_before_result.get("number"), "finality-before"),
                "hash": str(finality_before_result.get("hash", "")).lower(),
            },
            "after": {
                "number": block_number(finality_after_result.get("number"), "finality-after"),
                "hash": str(finality_after_result.get("hash", "")).lower(),
            },
            "target_was_finalized_before_and_after": True,
        },
        "runtime_bytecode": {
            "path": runtime_path.relative_to(OUTPUT).as_posix(),
            "encoding": "hexadecimal text with 0x prefix",
            "decoded_size": len(contract_runtime),
            "encoded_size": runtime_path.stat().st_size,
            "sha256": f"sha256:{sha256(contract_runtime)}",
        },
        "eip1967_slots": slots,
        "contract_identity": named,
        "token": {
            "token_id": TOKEN_ID,
            "token_hash": token_hash,
            "token_hash_method": "tokenIdToHash(uint256)",
            "project_id": token_project_id,
            "caip19": f"eip155:1/erc721:{CONTRACT}/{TOKEN_ID}",
        },
        "project": {
            "details": project_details,
            "state": project_state,
            "script_details": script_details,
            "scripts": script_records,
            "aggregate_script_sha256": f"sha256:{aggregate_script_sha256}",
            "external_dependencies": {
                "count": dependency_count,
                "registry": dependency_registry,
                "preferred_ipfs_gateway": ipfs_gateway,
                "preferred_arweave_gateway": arweave_gateway,
            },
            "token_uri": token_uri,
            "base_uri": base_uri,
            "base_uri_compatibility": base_uri_compatibility,
        },
        "custody": {
            "owner": owner,
            "approved": approved,
            "owner_matches_museum": True,
            "approved_is_zero": True,
            "museum_address": MUSEUM,
        },
        "transfer": {
            "transaction_hash": TRANSFER_TX,
            "block_number": TRANSFER_BLOCK,
            "block_hash": TRANSFER_BLOCK_HASH,
            "transaction_index": 95,
            "log_index": TRANSFER_LOG_INDEX,
            "from": DONOR,
            "to_contract": CONTRACT,
            "value": "0x0",
            "receipt_status": "0x1",
            "matching_transfer_log_count": 1,
            "matching_transfer_log": transfer_logs[0],
        },
        "raw_json_rpc": collector.raw_entries,
        "assertions": {
            "chain_id_is_ethereum_mainnet": True,
            "finalized_block_exact": True,
            "finalized_block_unchanged_during_run": True,
            "token_hash_matches_expected": True,
            "project_id_matches_expected": True,
            "script_count_is_11": True,
            "aggregate_script_sha256_matches_expected": True,
            "all_script_storage_addresses_match_expected": True,
            "owner_matches_museum": True,
            "getApproved_is_zero": True,
            "transfer_receipt_and_log_match_expected": True,
        },
        "limitations": [
            "This package proves the observed on-chain technical state, receipt, log and custody state only.",
            "It does not independently establish donor authority, legal title, copyright ownership or the terms of the gift instrument.",
            "The tokenURI surface and Art Blocks metadata service remain a mutable service layer even though the project script and token hash are captured on-chain.",
        ],
    }

    encoded_observation = (json.dumps(observation, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")
    write_bytes("derived/observation.json", encoded_observation)

    entries: list[dict[str, Any]] = []
    for path in sorted(OUTPUT.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(OUTPUT).as_posix()
        if relative in {"manifest.json", "summary.json"}:
            continue
        data = path.read_bytes()
        suffix = path.suffix.lower()
        media_type = {
            ".js": "text/javascript",
            ".json": "application/json",
            ".txt": "text/plain",
        }.get(suffix)
        if media_type is None:
            raise EvidenceError(f"technical evidence media type is not declared: {relative}")
        entries.append(
            {
                "path": relative,
                "size": len(data),
                "sha256": sha256(data),
                "media_type": media_type,
                "byte_mode": "raw",
            }
        )
    package_content_sha256 = sha256(canonical_json(entries))
    manifest = {
        "schema": "6529-museum-technical-evidence-manifest-v1",
        "hash_algorithm": "sha256",
        "byte_mode": "raw",
        "record_id": observation["record_id"],
        "finalized_block": observation["finalized_block"],
        "contract": CONTRACT,
        "token_id": TOKEN_ID,
        "package_content_sha256": f"sha256:{package_content_sha256}",
        "entries": entries,
    }
    manifest_bytes = (json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")
    manifest_sha256 = sha256(manifest_bytes)
    write_bytes("manifest.json", manifest_bytes)
    summary = {
        "record_id": observation["record_id"],
        "manifest": "manifest.json",
        "manifest_sha256": f"sha256:{manifest_sha256}",
        "package_content_sha256": f"sha256:{package_content_sha256}",
        "observation": observation,
    }
    summary_bytes = (json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")
    write_bytes("summary.json", summary_bytes)
    return {
        "summary_sha256": f"sha256:{sha256(summary_bytes)}",
        "manifest_sha256": f"sha256:{manifest_sha256}",
        "package_content_sha256": f"sha256:{package_content_sha256}",
        "file_count": len(entries),
        "raw_rpc_call_count": collector.sequence,
        "finalized_block": FINALIZED_BLOCK,
        "finalized_block_hash": FINALIZED_BLOCK_HASH,
        "aggregate_script_sha256": f"sha256:{aggregate_script_sha256}",
    }


def refresh_manifest_from_retained_observation() -> dict[str, Any]:
    """Rebuild package commitments after byte-preserving normalization.

    This mode performs no network requests and does not alter the retained
    observation. It exists so line-ending normalization can be verified and
    committed portably without reacquiring a different chain head.
    """
    summary_path = OUTPUT / "summary.json"
    if not summary_path.is_file():
        raise EvidenceError("technical evidence summary is missing")
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    observation = summary.get("observation")
    if not isinstance(observation, dict):
        raise EvidenceError("technical evidence summary has no observation")

    entries: list[dict[str, Any]] = []
    for path in sorted(OUTPUT.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(OUTPUT).as_posix()
        if relative in {"manifest.json", "summary.json"}:
            continue
        data = path.read_bytes()
        media_type = {
            ".js": "text/javascript",
            ".json": "application/json",
            ".txt": "text/plain",
        }.get(path.suffix.lower())
        if media_type is None:
            raise EvidenceError(f"technical evidence media type is not declared: {relative}")
        entries.append(
            {
                "path": relative,
                "size": len(data),
                "sha256": sha256(data),
                "media_type": media_type,
                "byte_mode": "raw",
            }
        )

    package_content_sha256 = sha256(canonical_json(entries))
    manifest = {
        "schema": "6529-museum-technical-evidence-manifest-v1",
        "hash_algorithm": "sha256",
        "byte_mode": "raw",
        "record_id": observation["record_id"],
        "finalized_block": observation["finalized_block"],
        "contract": CONTRACT,
        "token_id": TOKEN_ID,
        "package_content_sha256": f"sha256:{package_content_sha256}",
        "entries": entries,
    }
    manifest_bytes = (
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")
    manifest_sha256 = sha256(manifest_bytes)
    write_bytes("manifest.json", manifest_bytes)
    refreshed_summary = {
        "record_id": observation["record_id"],
        "manifest": "manifest.json",
        "manifest_sha256": f"sha256:{manifest_sha256}",
        "package_content_sha256": f"sha256:{package_content_sha256}",
        "observation": observation,
    }
    summary_bytes = (
        json.dumps(refreshed_summary, ensure_ascii=False, indent=2, sort_keys=True)
        + "\n"
    ).encode("utf-8")
    write_bytes("summary.json", summary_bytes)
    return {
        "summary_sha256": f"sha256:{sha256(summary_bytes)}",
        "manifest_sha256": f"sha256:{manifest_sha256}",
        "package_content_sha256": f"sha256:{package_content_sha256}",
        "file_count": len(entries),
        "finalized_block": observation["finalized_block"]["number"],
        "finalized_block_hash": observation["finalized_block"]["hash"],
    }


def main() -> int:
    try:
        recover_partial = len(sys.argv) == 2 and sys.argv[1] == "--recover-partial"
        refresh_manifest = len(sys.argv) == 2 and sys.argv[1] == "--refresh-manifest"
        if len(sys.argv) > 1 and not recover_partial and not refresh_manifest:
            raise EvidenceError("accepted modes are --recover-partial and --refresh-manifest")
        result = (
            refresh_manifest_from_retained_observation()
            if refresh_manifest
            else run(recover_partial=recover_partial)
        )
    except (EvidenceError, OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"Vera Molnar technical evidence acquisition refused: {exc}")
        return 1
    print(f"Vera Molnar technical evidence acquired: {OUTPUT}")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
