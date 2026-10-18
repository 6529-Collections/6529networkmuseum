#!/usr/bin/env python3
"""Shared fixed identities and fail-closed helpers for MAX PAIN #4188 evidence.

The custody, source, technical and funding acquisition scripts for accession
lot ``6529NM.2026.005`` import these constants so that every package binds the
same object, transactions and Museum custody address.  Network access goes
only through ``scripts/safe_fetch.py`` with the HTTP/1.0 connection factory
used by the Vera and Magnum acquisitions.  Every endpoint is a keyless public
service; no API key, token or private environment file is read.

This module performs no accession, title, rights or valuation determination.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
import hashlib
import json
import os
from pathlib import Path
import ssl
import stat
import time
from typing import Any
from urllib.parse import urlsplit

from Crypto.Hash import keccak

from safe_fetch import FetchPolicyError, SafeHTTPSFetcher, _PinnedHTTPSConnection


ROOT = Path(__file__).resolve().parents[1]

ACCESSION_ID = "6529NM.2026.005"
OBJECT_ID = "6529NM.2026.005.01"
WORK_ENTITY_ID = "6529NM-W-0036"
ANIMATION_MEDIA_ENTITY_ID = "6529NM-MED-0060"
POSTER_MEDIA_ENTITY_ID = "6529NM-MED-0061"
WAVE_ID = "5f207393-5418-4a75-8738-e40edb44a94d"
PROPOSAL_DROP_ID = "87e1fc3a-deef-4d1d-bf36-b2a44507f17b"
PROPOSAL_SERIAL = 1_336_667

CHAIN_ID = 1
CONTRACT = "0xd1169e5349d1cb9941f3dcba135c8a4b9eacfdde"
TOKEN_ID = 171_000_104_188
CAIP19 = f"eip155:1/erc721:{CONTRACT}/{TOKEN_ID}"
TOKEN_NAME = "MAX PAIN #4188/7394"
TOKEN_URI = "ipfs://QmT9cJUe8NFwniMTjWHunf6YWgYRdACTyN7uAiZRuXP9ij/171000104188"
METADATA_ROOT_CID = "QmT9cJUe8NFwniMTjWHunf6YWgYRdACTyN7uAiZRuXP9ij"
IMAGE_CID = "QmTcTzTPgCyvF933oeFvB4GkPgaXtF6dKuQgvg32qqLYGF"
IMAGE_CDN_URL = (
    "https://media.niftygateway.com/image/upload/v1647441828/AA/XCOPY/OpenEdition/MAX_PAIN_1_bhtyc0.gif"
)
IMAGE_SHA256 = "3ba2c6c6a7b7da940b5780da8fe301e61366a0b5c738be16e537ee122630be2e"
IMAGE_SIZE = 4_541_937

# The Museum Safe.  This exact value is checked in full against ENS resolution
# of ``networkmuseum.6529.eth`` at the evidence block.  Look-alike addresses
# that share its leading and trailing characters were planted in the
# acquisition wallet's token history by address-poisoning spam; never copy the
# custody address from that history.
MUSEUM_ADDRESS = "0xbecfa2ba5a782d11e1a0e821e8f2e30b6684178c"
MUSEUM_CHECKSUM_ADDRESS = "0xbECfa2bA5a782D11E1a0e821E8F2e30b6684178c"
ADDRESS_POISONING_LOOKALIKE_PREFIXES = ("0xbecfa674", "0xbecf6883")
ENS_NAME = "networkmuseum.6529.eth"
ENS_NAMEHASH = "0xf90c6c0dca064bc19c04756dc088ceb60402ce8522ab4623f016d19abbb76394"
ENS_REGISTRY = "0x00000000000c2e074ec69a0dfb2997ba6c7d2e1e"

# The acquisition wallet acted as the executing agent of the Wave-authorized
# purchase.  It is not a contributor's payment wallet.
AGENT_ADDRESS = "0xe84576bd68882e037d8e4df484ad9a15e2b855bc"
SEAPORT_1_6 = "0x0000000000000068f116a894984e2db1123eb395"

PURCHASE_TX = "0xdf8b07004bfed397920355ac80991a9dd592c896ca77b1fadb5655f8c85aa4d6"
PURCHASE_BLOCK = 25_889_852
PURCHASE_TRANSFER_LOG_INDEX = 407
PURCHASE_VALUE_WEI = 458_999_999_900_000_000
MUSEUM_RECEIPT_TX = "0xe7511598bbdabd1d4ff1c5bb7e6d1f9157a413fbcf305f0392cc30c92252ea03"
MUSEUM_RECEIPT_BLOCK = 25_889_990
MUSEUM_RECEIPT_LOG_INDEX = 955
RESIDUAL_TX = "0x7d7b7733c696858dda93374395a978a4f7cb0cf4b631e2a81ab595f70d5debef"
RESIDUAL_BLOCK = 25_975_418
RESIDUAL_VALUE_WEI = 68_496_911_687_069_084
MINT_TX = "0x0b2da2a60e43772a73dc49383ca40da2d46ecf6ee9ba1669727aa03a78f3e6f8"
MINT_BLOCK = 14_451_983

ZERO_ADDRESS = "0x" + "0" * 40
TRANSFER_TOPIC = "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"

# Keyless public endpoints.  dRPC served archive-depth state for historical
# balances during research; BlastAPI and MEV Blocker are independent second
# providers and accept JSON-RPC batches.
PRIMARY_RPC_URL = "https://eth.drpc.org"
SECOND_RPC_URL = "https://eth-mainnet.public.blastapi.io"
BATCH_RPC_URL = "https://rpc.mevblocker.io"
RETRY_DELAYS_SECONDS = (2.0, 5.0, 10.0)


class EvidenceError(RuntimeError):
    """Raised when an exact, internally consistent package cannot be emitted."""


def http10_connection_factory(endpoint: Any, resolved: Any, policy: Any) -> Any:
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


def utc_now() -> str:
    return datetime.now(UTC).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def iso_from_unix(seconds: int) -> str:
    return datetime.fromtimestamp(seconds, UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def canonical_json(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def pretty_json(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, allow_nan=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def keccak256(payload: bytes) -> bytes:
    digest = keccak.new(digest_bits=256)
    digest.update(payload)
    return digest.digest()


def selector(signature: str) -> str:
    return keccak256(signature.encode("ascii"))[:4].hex()


def namehash(name: str) -> str:
    node = b"\x00" * 32
    for label in reversed(name.split(".")):
        node = keccak256(node + keccak256(label.encode("utf-8")))
    return "0x" + node.hex()


def checksum_address(address: str) -> str:
    lowered = address.lower().removeprefix("0x")
    digest = keccak256(lowered.encode("ascii")).hex()
    return "0x" + "".join(
        char.upper() if char.isalpha() and int(digest[index], 16) >= 8 else char
        for index, char in enumerate(lowered)
    )


def assert_fixed_identities() -> None:
    """Fail closed if a constant above was edited into an inconsistent state."""

    if checksum_address(MUSEUM_ADDRESS) != MUSEUM_CHECKSUM_ADDRESS:
        raise EvidenceError("Museum checksum address does not match its lowercase form")
    if MUSEUM_ADDRESS.startswith(ADDRESS_POISONING_LOOKALIKE_PREFIXES):
        raise EvidenceError("Museum address matches a known address-poisoning look-alike")
    if namehash(ENS_NAME) != ENS_NAMEHASH:
        raise EvidenceError("ENS namehash constant does not match networkmuseum.6529.eth")
    for value in (CONTRACT, MUSEUM_ADDRESS, AGENT_ADDRESS, SEAPORT_1_6, ENS_REGISTRY):
        if value != value.lower() or len(value) != 42:
            raise EvidenceError(f"fixed address is not canonical lowercase: {value}")


def require_museum_address(observed: str, label: str) -> None:
    """Compare all 40 hex characters; prefix/suffix similarity is never enough."""

    if observed.lower() != MUSEUM_ADDRESS:
        raise EvidenceError(f"{label}: {observed} is not the ENS-resolved Museum Safe")


def prepare_empty_output(output: Path) -> None:
    """Create or admit only an explicit empty, non-linked output directory."""

    if os.path.lexists(output):
        info = os.lstat(output)
        is_reparse = bool(
            getattr(info, "st_file_attributes", 0) & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
        )
        if stat.S_ISLNK(info.st_mode) or is_reparse:
            raise EvidenceError("output directory cannot be a symlink or reparse point")
        if not stat.S_ISDIR(info.st_mode):
            raise EvidenceError("output path is not a directory")
        if any(output.iterdir()):
            raise EvidenceError("output directory must be empty; evidence replacement is a separate governed operation")
    else:
        output.mkdir(parents=True, exist_ok=False)


def write_bytes(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_bytes(payload)
    temporary.replace(path)


def entry_for(output: Path, path: Path, media_type: str, **extra: Any) -> dict[str, Any]:
    """Return one evidence-manifest entry in the repository raw-byte profile."""

    payload = path.read_bytes()
    return {
        "path": path.relative_to(output).as_posix(),
        "sha256": sha256(payload),
        "size": len(payload),
        "media_type": media_type,
        "byte_mode": "raw",
        **extra,
    }


def _endpoint_is_keyless(url: str) -> bool:
    parts = urlsplit(url)
    return parts.scheme == "https" and not parts.query and not parts.username and parts.path in {"", "/", "/eth"}


def fetch(url: str, *, method: str = "GET", body: bytes | None = None, accept: str = "*/*", user_agent: str) -> tuple[Any, int]:
    """Fetch through the pinned safe-fetch policy with bounded transient retries.

    Only the final successful response is returned, with its attempt number.
    Responses that violate the fetch policy (oversized, compressed or chunked
    bodies, non-global addresses) are never retried.
    """

    headers = {"Accept": accept, "User-Agent": user_agent}
    if body is not None:
        headers["Content-Type"] = "application/json"
    last_error: Exception | None = None
    for attempt, delay in enumerate((0.0, *RETRY_DELAYS_SECONDS), start=1):
        if delay:
            time.sleep(delay)
        try:
            result = FETCHER.fetch(
                url,
                method=method,
                body=body,
                headers=headers,
                expires_at=datetime.now(UTC) + timedelta(seconds=60),
            )
        except FetchPolicyError as exc:
            message = str(exc)
            if not any(term in message for term in ("resolution failed", "read failed", "timed out", "timeout")):
                raise
            last_error = exc
            continue
        except OSError as exc:
            last_error = exc
            continue
        if result.observation.status in {429, 500, 502, 503, 504}:
            last_error = EvidenceError(f"HTTP {result.observation.status} from {url}")
            continue
        return result, attempt
    raise EvidenceError(f"{url}: transient failure after retries: {last_error}")


class RpcClient:
    """JSON-RPC over safe_fetch; callers retain the exact request/response bytes."""

    def __init__(self, user_agent: str, pause_seconds: float = 0.35) -> None:
        self.user_agent = user_agent
        self.pause_seconds = pause_seconds

    def call(self, endpoint: str, request_id: str, method: str, params: list[Any]) -> dict[str, Any]:
        if not _endpoint_is_keyless(endpoint):
            raise EvidenceError(f"RPC endpoint is not a keyless public URL: {endpoint}")
        request = {"jsonrpc": "2.0", "id": request_id, "method": method, "params": params}
        request_bytes = canonical_json(request)
        rounds = 0
        while True:
            time.sleep(self.pause_seconds)
            result, attempts = fetch(
                endpoint, method="POST", body=request_bytes, accept="application/json", user_agent=self.user_agent
            )
            if result.observation.status != 200:
                raise EvidenceError(f"{request_id}: HTTP {result.observation.status} from {endpoint}")
            try:
                response = json.loads(result.body.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                raise EvidenceError(f"{request_id}: response is not UTF-8 JSON") from exc
            if not isinstance(response, dict) or response.get("jsonrpc") != "2.0" or response.get("id") != request_id:
                raise EvidenceError(f"{request_id}: malformed JSON-RPC response")
            error = response.get("error")
            if isinstance(error, dict) and _transient_rpc_error(error) and rounds < len(RETRY_DELAYS_SECONDS):
                time.sleep(RETRY_DELAYS_SECONDS[rounds])
                rounds += 1
                continue
            transport = result.observation.to_dict()
            transport["endpoint"] = endpoint
            transport["attempts"] = attempts + rounds
            return {
                "request": request,
                "request_bytes": request_bytes,
                "response": response,
                "response_bytes": result.body,
                "transport": transport,
            }


def _transient_rpc_error(error: dict[str, Any]) -> bool:
    message = str(error.get("message", "")).lower()
    return error.get("code") in {-32005, 429} or any(
        term in message for term in ("rate limit", "temporarily unavailable", "timeout", "too many requests")
    )


def require_result(call: dict[str, Any], label: str) -> Any:
    response = call["response"]
    if "error" in response or "result" not in response:
        raise EvidenceError(f"{label}: JSON-RPC error {response.get('error')!r}")
    return response["result"]


def hex_int(value: Any, label: str) -> int:
    if not isinstance(value, str) or not value.startswith("0x"):
        raise EvidenceError(f"{label} is not a hex quantity")
    return int(value, 16)


def hex_bytes(value: Any, label: str) -> bytes:
    if not isinstance(value, str) or not value.startswith("0x") or len(value) % 2:
        raise EvidenceError(f"{label} is not even-length hex")
    try:
        return bytes.fromhex(value[2:])
    except ValueError as exc:
        raise EvidenceError(f"{label} is not valid hex") from exc


def abi_address(value: Any, label: str) -> str:
    raw = hex_bytes(value, label)
    if len(raw) != 32 or any(raw[:12]):
        raise EvidenceError(f"{label} is not one left-padded ABI address word")
    return "0x" + raw[12:].hex()


def abi_uint(value: Any, label: str) -> int:
    raw = hex_bytes(value, label)
    if len(raw) != 32:
        raise EvidenceError(f"{label} is not one ABI word")
    return int.from_bytes(raw, "big")


def abi_bool(value: Any, label: str) -> bool:
    number = abi_uint(value, label)
    if number not in (0, 1):
        raise EvidenceError(f"{label} is not a Solidity bool")
    return bool(number)


def abi_string(value: Any, label: str) -> str:
    raw = hex_bytes(value, label)
    if len(raw) < 64:
        raise EvidenceError(f"{label} string result is truncated")
    offset = int.from_bytes(raw[:32], "big")
    if offset % 32 or offset + 32 > len(raw):
        raise EvidenceError(f"{label} string offset is invalid")
    length = int.from_bytes(raw[offset : offset + 32], "big")
    if offset + 32 + length > len(raw):
        raise EvidenceError(f"{label} string exceeds the ABI result")
    return raw[offset + 32 : offset + 32 + length].decode("utf-8")


def word(value: int | str) -> str:
    if isinstance(value, int):
        return f"{value:064x}"
    return value.lower().removeprefix("0x").rjust(64, "0")


def calldata(signature: str, *values: int | str) -> str:
    return "0x" + selector(signature) + "".join(word(value) for value in values)


def address_topic(address: str) -> str:
    return "0x" + address.lower().removeprefix("0x").rjust(64, "0")


def transfer_logs(receipt: dict[str, Any], contract: str = CONTRACT) -> list[dict[str, Any]]:
    """Return ERC-721 Transfer logs (four topics) emitted by ``contract``."""

    logs = receipt.get("logs")
    if not isinstance(logs, list):
        raise EvidenceError("receipt has no log array")
    return [
        log
        for log in logs
        if isinstance(log, dict)
        and str(log.get("address", "")).lower() == contract
        and isinstance(log.get("topics"), list)
        and len(log["topics"]) == 4
        and str(log["topics"][0]).lower() == TRANSFER_TOPIC
    ]


def decoded_transfer(log: dict[str, Any]) -> dict[str, Any]:
    topics = log["topics"]
    return {
        "log_index": hex_int(log.get("logIndex"), "logIndex"),
        "from": "0x" + str(topics[1]).lower()[-40:],
        "to": "0x" + str(topics[2]).lower()[-40:],
        "token_id": int(str(topics[3]), 16),
    }


def wei_to_eth_string(value: int) -> str:
    whole, fraction = divmod(value, 10**18)
    text = f"{whole}.{fraction:018d}".rstrip("0")
    return text + "0" if text.endswith(".") else text
