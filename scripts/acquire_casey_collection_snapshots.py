#!/usr/bin/env python3
"""Acquire complete Casey REAS collection snapshots from primary sources.

Completeness is established by the Art Blocks official paginated Hasura
``tokens_metadata`` response, ordered by the server's ``token_id: asc`` order.
The script materializes a separate numeric canonical order. It also resolves
every contract ``tokenURI(uint256)`` at one pinned Ethereum block and
retains raw JSON-RPC batch responses. HTTP retrieval of those URIs is sampled
cross-check evidence only; rate limiting cannot silently remove a token from
the bulk snapshot.
"""

from __future__ import annotations

import argparse
from datetime import UTC, datetime
import hashlib
import json
from pathlib import Path
import sys
import time
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / "evidence/casey-reas-collection-snapshots/collection-sources.json"
DEFAULT_OUTPUT = ROOT / "evidence/casey-reas-collection-snapshots"
GRAPHQL_URI = "https://data.artblocks.io/v1/graphql"
USER_AGENT = "6529-Network-Museum/casey-snapshot-acquisition-v2"
TOKEN_URI_SELECTOR = "c87b56dd"
PROJECT_TOKEN_INFO_SELECTOR = "8c2c3622"
PROJECT_STATE_DATA_SELECTOR = "0ea5613f"
TOKEN_ID_MULTIPLIER = 1_000_000

PROJECT_QUERY = """
query CaseyProject($id: String!, $chain_id: Int!) {
  projects_metadata(where: {id: {_eq: $id}, chain_id: {_eq: $chain_id}}) {
    id project_id chain_id contract_address name artist_name invocations
    max_invocations complete completed_at script_type_and_version aspect_ratio
    license website vertical_name
  }
}
""".strip()

TOKENS_QUERY = """
query CaseyTokens($project: String!, $limit: Int!, $offset: Int!) {
  tokens_metadata(
    where: {chain_id: {_eq: 1}, project_id: {_eq: $project}}
    order_by: {token_id: asc}
    limit: $limit
    offset: $offset
  ) {
    id token_id chain_id contract_address project_id invocation hash
    live_view_url media_url primary_asset_url features
  }
}
""".strip()


class AcquisitionError(RuntimeError):
    """Raised when a complete bulk snapshot cannot be emitted."""


def now_iso() -> str:
    return datetime.now(UTC).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def canonical_json(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def digest(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def json_digest(value: Any) -> str:
    return "sha256:" + digest(canonical_json(value))


def write_bytes(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_bytes() == payload:
        return
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_bytes(payload)
    temporary.replace(path)


def write_json(path: Path, value: Any) -> None:
    write_bytes(path, (json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode("utf-8"))


def save_raw(run_root: Path, category: str, payload: bytes) -> dict[str, Any]:
    sha = digest(payload)
    relative = Path("raw") / category / f"sha256-{sha}.json"
    write_bytes(run_root / relative, payload)
    return {"path": relative.as_posix(), "sha256": f"sha256:{sha}", "size": len(payload), "byte_mode": "raw"}


def request_bytes(
    url: str,
    *,
    method: str,
    body: bytes | None,
    headers: dict[str, str],
    timeout: float,
    retries: int,
    sleep_ms: int,
) -> dict[str, Any]:
    attempts: list[dict[str, Any]] = []
    for attempt in range(1, retries + 2):
        if attempt > 1 and sleep_ms:
            time.sleep(sleep_ms / 1000)
        try:
            with urlopen(Request(url, data=body, headers=headers, method=method), timeout=timeout) as response:
                response_body = response.read()
                status = int(response.status)
                headers_out = {"content_type": response.headers.get("Content-Type", "")}
            attempts.append({"attempt": attempt, "status": status, "ok": status == 200})
            if status == 200:
                return {"ok": True, "body": response_body, "status": status, "headers": headers_out, "attempts": attempts}
            if status not in {408, 425, 429} and status < 500:
                break
        except HTTPError as error:
            status = int(error.code)
            attempts.append({"attempt": attempt, "status": status, "ok": False, "error": str(error)})
            if status not in {408, 425, 429} and status < 500:
                break
        except (OSError, URLError, TimeoutError) as error:
            attempts.append({"attempt": attempt, "status": None, "ok": False, "error": str(error)})
    return {"ok": False, "body": b"", "status": None, "headers": {}, "attempts": attempts}


def post_json(
    url: str,
    payload: Any,
    *,
    timeout: float,
    retries: int,
    sleep_ms: int,
) -> dict[str, Any]:
    body = canonical_json(payload)
    response = request_bytes(
        url,
        method="POST",
        body=body,
        headers={"Accept": "application/json", "Content-Type": "application/json", "User-Agent": USER_AGENT},
        timeout=timeout,
        retries=retries,
        sleep_ms=sleep_ms,
    )
    response["request_sha256"] = f"sha256:{digest(body)}"
    if response["ok"]:
        try:
            response["json"] = json.loads(response["body"].decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            response["ok"] = False
            response["semantic_error"] = str(error)
    return response


def abi_uint(data: bytes, index: int) -> int:
    start = index * 32
    if len(data) < start + 32:
        raise AcquisitionError("ABI response is shorter than expected")
    return int.from_bytes(data[start : start + 32], "big")


def project_info(
    rpc_uri: str,
    collection: dict[str, Any],
    block_tag: str,
    *,
    timeout: float,
    retries: int,
    sleep_ms: int,
) -> dict[str, Any]:
    method = collection["project_info_method"]
    if method == "projectTokenInfo(uint256)":
        selector, invocation_index, max_index, active_index = PROJECT_TOKEN_INFO_SELECTOR, 2, 3, 4
    elif method == "projectStateData(uint256)":
        selector, invocation_index, max_index, active_index = PROJECT_STATE_DATA_SELECTOR, 0, 1, 2
    else:
        raise AcquisitionError(f"unsupported project info method: {method}")
    payload = {
        "jsonrpc": "2.0",
        "id": f"project-info-{collection['slug']}",
        "method": "eth_call",
        "params": [{"to": collection["contract_address"], "data": "0x" + selector + int(collection["project_id"]).to_bytes(32, "big").hex()}, block_tag],
    }
    response = post_json(rpc_uri, payload, timeout=timeout, retries=retries, sleep_ms=sleep_ms)
    if not response["ok"] or not isinstance(response["json"].get("result"), str):
        raise AcquisitionError(f"{method} failed for {collection['slug']}")
    data = bytes.fromhex(response["json"]["result"][2:])
    return {
        "method": method,
        "selector": "0x" + selector,
        "invocations": abi_uint(data, invocation_index),
        "max_invocations": abi_uint(data, max_index),
        "active": bool(abi_uint(data, active_index)),
        "response": response,
    }


def decode_token_uri(result: str) -> str:
    if not isinstance(result, str) or not result.startswith("0x"):
        raise AcquisitionError("tokenURI returned no ABI bytes")
    data = bytes.fromhex(result[2:])
    offset = abi_uint(data, 0)
    length = abi_uint(data, offset // 32)
    end = offset + 32 + length
    if end > len(data):
        raise AcquisitionError("tokenURI ABI string is truncated")
    return data[offset + 32 : end].decode("utf-8")


def resolve_token_uris(
    run_root: Path,
    rpc_uri: str,
    collection: dict[str, Any],
    token_ids: list[int],
    block_tag: str,
    *,
    batch_size: int,
    timeout: float,
    retries: int,
    sleep_ms: int,
) -> tuple[dict[int, dict[str, Any]], list[dict[str, Any]]]:
    resolved: dict[int, dict[str, Any]] = {}
    errors: list[dict[str, Any]] = []
    for batch_number, start in enumerate(range(0, len(token_ids), batch_size)):
        batch_ids = token_ids[start : start + batch_size]
        payload = [
            {
                "jsonrpc": "2.0",
                "id": f"token-uri-{token_id}",
                "method": "eth_call",
                "params": [{"to": collection["contract_address"], "data": "0x" + TOKEN_URI_SELECTOR + token_id.to_bytes(32, "big").hex()}, block_tag],
            }
            for token_id in batch_ids
        ]
        response = post_json(rpc_uri, payload, timeout=timeout, retries=retries, sleep_ms=sleep_ms)
        raw = save_raw(run_root, f"{collection['slug']}/rpc", response.get("body", b"")) if response.get("body") else None
        parsed = response.get("json") if response["ok"] else None
        by_id = {row.get("id"): row for row in parsed} if isinstance(parsed, list) else {}
        for token_id in batch_ids:
            row = by_id.get(f"token-uri-{token_id}")
            entry = {"token_id": token_id, "batch_number": batch_number, "batch_offset": start, "raw_response": raw, "attempts": response.get("attempts", [])}
            if not isinstance(row, dict) or not isinstance(row.get("result"), str):
                error = {"collection": collection["slug"], "token_id": token_id, "error": "tokenURI missing from RPC batch response", "batch": entry}
                errors.append(error)
                continue
            try:
                entry["uri"] = decode_token_uri(row["result"])
                entry["rpc_id"] = row.get("id")
                resolved[token_id] = entry
            except AcquisitionError as error:
                errors.append({"collection": collection["slug"], "token_id": token_id, "error": str(error), "batch": entry})
    return resolved, errors


def scalar_text(value: Any) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return json.dumps(value, ensure_ascii=False, allow_nan=False, separators=(",", ":"))
    raise AcquisitionError("Hasura feature value is not a JSON scalar")


def validate_project(row: dict[str, Any], collection: dict[str, Any]) -> None:
    expected = {
        "id": collection["project_graphql_id"],
        "project_id": str(collection["project_id"]),
        "chain_id": 1,
        "contract_address": collection["contract_address"].lower(),
        "name": collection["name"],
        "artist_name": collection["artist"],
    }
    for key, value in expected.items():
        actual = row.get(key)
        if key == "contract_address" and isinstance(actual, str):
            actual = actual.lower()
        if actual != value:
            raise AcquisitionError(f"project identity mismatch for {collection['slug']}: {key}={actual!r}")


def validate_token(row: dict[str, Any], collection: dict[str, Any], token_id: int, invocation: int) -> None:
    if str(row.get("token_id")) != str(token_id) or row.get("invocation") != invocation:
        raise AcquisitionError(f"Hasura token identity/order mismatch for {collection['slug']}/{token_id}")
    if row.get("chain_id") != 1 or str(row.get("contract_address", "")).lower() != collection["contract_address"].lower():
        raise AcquisitionError(f"Hasura token contract/chain mismatch for {collection['slug']}/{token_id}")
    if row.get("project_id") != collection["project_graphql_id"]:
        raise AcquisitionError(f"Hasura token project mismatch for {collection['slug']}/{token_id}")
    if not isinstance(row.get("features"), dict):
        raise AcquisitionError(f"Hasura features is not an object for {collection['slug']}/{token_id}")


def metadata_traits_to_features(metadata: dict[str, Any]) -> dict[str, str]:
    raw_traits = metadata.get("traits")
    if not isinstance(raw_traits, list):
        raise AcquisitionError("cross-check metadata has no traits[]")
    result: dict[str, str] = {}
    for index, row in enumerate(raw_traits):
        if not isinstance(row, dict) or not isinstance(row.get("trait_type"), str) or not isinstance(row.get("value"), str):
            raise AcquisitionError(f"cross-check trait row {index} is malformed")
        value = row["value"]
        if index == 0 and value.lower().startswith("all "):
            continue
        if ": " in value:
            trait, value_text = value.split(": ", 1)
        else:
            trait, value_text = row["trait_type"], value
        if trait in result:
            raise AcquisitionError(f"cross-check has duplicate derived trait {trait!r}")
        result[trait] = value_text
    return result


def http_cross_check(
    run_root: Path,
    collection: dict[str, Any],
    row: dict[str, Any],
    uri_entry: dict[str, Any],
    *,
    timeout: float,
    retries: int,
    sleep_ms: int,
) -> dict[str, Any]:
    source_uri = uri_entry.get("uri", uri_entry.get("token_uri"))
    fallback_uri = f"https://token.artblocks.io/1/{collection['contract_address'].lower()}/{row['token_id']}"
    primary = request_bytes(source_uri, method="GET", body=None, headers={"Accept": "application/json", "User-Agent": USER_AGENT}, timeout=timeout, retries=retries, sleep_ms=sleep_ms)
    retrieval_uri = source_uri
    response = primary
    fallback = None
    if not primary["ok"] and fallback_uri != source_uri:
        fallback = request_bytes(fallback_uri, method="GET", body=None, headers={"Accept": "application/json", "User-Agent": USER_AGENT}, timeout=timeout, retries=retries, sleep_ms=sleep_ms)
        if fallback["ok"]:
            retrieval_uri, response = fallback_uri, fallback
    raw = save_raw(run_root, f"{collection['slug']}/http-cross-check", response.get("body", b"")) if response.get("body") else None
    result: dict[str, Any] = {
        "token_id": int(row["token_id"]),
        "source_uri": source_uri,
        "retrieval_uri": retrieval_uri,
        "fallback_from": source_uri if retrieval_uri != source_uri else None,
        "primary_attempts": primary.get("attempts", []),
        "fallback_attempts": fallback.get("attempts", []) if fallback else [],
        "raw_response": raw,
        "status": response.get("status"),
        "error": None,
        "identity_match": None,
        "features_match": None,
    }
    if not response["ok"] or raw is None:
        result["error"] = "cross-check HTTP retrieval failed; bulk Hasura row remains the completeness source"
        return result
    try:
        metadata = json.loads(response["body"].decode("utf-8"))
        result["identity_match"] = str(metadata.get("tokenID")) == str(row["token_id"]) and str(metadata.get("contract_address", "")).lower() == collection["contract_address"].lower()
        result["features_match"] = metadata_traits_to_features(metadata) == {str(k): scalar_text(v) for k, v in row["features"].items()}
    except (UnicodeDecodeError, json.JSONDecodeError, AcquisitionError) as error:
        result["error"] = str(error)
    return result


def run(args: argparse.Namespace) -> int:
    config = json.loads(args.config.resolve().read_text(encoding="utf-8"))
    collections = config.get("collections")
    if not isinstance(collections, list) or len(collections) != 5:
        raise AcquisitionError("configuration must contain exactly five collections")
    started = now_iso()
    run_id = started.replace("-", "").replace(":", "").replace(".", "")
    run_root = args.output_dir.resolve() / "runs" / run_id
    run_root.mkdir(parents=True, exist_ok=True)

    block_number_response = post_json(args.rpc_url, {"jsonrpc": "2.0", "id": "block-number", "method": "eth_blockNumber", "params": []}, timeout=args.timeout, retries=args.retries, sleep_ms=args.sleep_ms)
    block_number_raw = save_raw(run_root, "shared/rpc", block_number_response["body"])
    if not block_number_response["ok"]:
        raise AcquisitionError("eth_blockNumber failed")
    block_number = int(block_number_response["json"]["result"], 16)
    block_tag = hex(block_number)
    block_response = post_json(args.rpc_url, {"jsonrpc": "2.0", "id": "observed-block", "method": "eth_getBlockByNumber", "params": [block_tag, False]}, timeout=args.timeout, retries=args.retries, sleep_ms=args.sleep_ms)
    block_raw_response = save_raw(run_root, "shared/rpc", block_response["body"])
    if not block_response["ok"] or not isinstance(block_response["json"].get("result"), dict):
        raise AcquisitionError("eth_getBlockByNumber failed")
    block = block_response["json"]["result"]
    block_hash = block.get("hash")
    block_time = datetime.fromtimestamp(int(block["timestamp"], 16), tz=UTC).isoformat(timespec="seconds").replace("+00:00", "Z")

    manifest: dict[str, Any] = {
        "schema_version": "6529nm.casey-collection-run-manifest.v2",
        "run_id": run_id,
        "status": "incomplete",
        "constructor": {"actor_id": "codex-task:019fbe33-c412-7550-a1ba-f6c68c3b5652", "role": "constructor", "constructed_at": started},
        "review": None,
        "observation": {"chain": config["chain"], "rpc_uri": args.rpc_url, "block_number": block_number, "block_tag": block_tag, "block_hash": block_hash, "block_time": block_time, "run_started_at": started},
        "rpc": {"token_uri_method": "tokenURI(uint256)", "token_uri_selector": "0x" + TOKEN_URI_SELECTOR, "batch_size": args.rpc_batch_size, "block_number_source": block_number_raw, "block_number_attempts": block_number_response.get("attempts", []), "block_source": block_raw_response, "block_attempts": block_response.get("attempts", [])},
        "bulk_source": {"uri": GRAPHQL_URI, "project_query": PROJECT_QUERY, "project_query_sha256": json_digest(PROJECT_QUERY), "token_query": TOKENS_QUERY, "token_query_sha256": json_digest(TOKENS_QUERY), "order_by": "token_id asc", "page_size": args.page_size},
        "collections": [],
        "errors": [],
        "cross_check_warnings": [],
    }

    for collection in collections:
        slug = collection["slug"]
        errors: list[str] = []
        project_response = post_json(GRAPHQL_URI, {"query": PROJECT_QUERY, "variables": {"id": collection["project_graphql_id"], "chain_id": 1}}, timeout=args.timeout, retries=args.retries, sleep_ms=args.sleep_ms)
        project_raw = save_raw(run_root, f"{slug}/graphql", project_response.get("body", b"")) if project_response.get("body") else None
        try:
            rows = project_response["json"]["data"]["projects_metadata"]
            if not isinstance(rows, list) or len(rows) != 1:
                raise AcquisitionError("project query did not return exactly one row")
            project_row = rows[0]
            validate_project(project_row, collection)
        except (KeyError, TypeError, AcquisitionError) as error:
            errors.append(f"project query: {error}")
            project_row = None
        try:
            project_state = project_info(args.rpc_url, collection, block_tag, timeout=args.timeout, retries=args.retries, sleep_ms=args.sleep_ms)
            project_state_raw = save_raw(run_root, f"{slug}/rpc", project_state["response"]["body"])
        except AcquisitionError as error:
            errors.append(str(error))
            project_state = None
            project_state_raw = None
        if project_state is None:
            expected = 0
        else:
            expected = project_state["max_invocations"]
        if project_row is not None:
            if project_row.get("max_invocations") != expected or project_row.get("invocations") != expected or project_row.get("complete") is not True:
                errors.append(f"population/completion mismatch between on-chain and Art Blocks project response")

        expected_ids = [int(collection["project_id"]) * TOKEN_ID_MULTIPLIER + invocation for invocation in range(expected)]
        uri_map, uri_errors = resolve_token_uris(run_root, args.rpc_url, collection, expected_ids, block_tag, batch_size=args.rpc_batch_size, timeout=args.timeout, retries=args.retries, sleep_ms=args.sleep_ms)
        errors.extend(item["error"] for item in uri_errors)

        bulk_rows: list[dict[str, Any]] = []
        pages: list[dict[str, Any]] = []
        offset = 0
        while project_row is not None and offset < expected:
            payload = {"query": TOKENS_QUERY, "variables": {"project": collection["project_graphql_id"], "limit": args.page_size, "offset": offset}}
            page_response = post_json(GRAPHQL_URI, payload, timeout=args.timeout, retries=args.retries, sleep_ms=args.sleep_ms)
            page_raw = save_raw(run_root, f"{slug}/graphql", page_response.get("body", b"")) if page_response.get("body") else None
            try:
                page_rows = page_response["json"]["data"]["tokens_metadata"]
                if not isinstance(page_rows, list):
                    raise AcquisitionError("tokens_metadata is not an array")
            except (KeyError, TypeError, AcquisitionError) as error:
                errors.append(f"bulk page offset {offset}: {error}")
                break
            pages.append({"offset": offset, "limit": args.page_size, "variables": payload["variables"], "returned_count": len(page_rows), "raw_response": page_raw, "request_sha256": page_response.get("request_sha256"), "attempts": page_response.get("attempts", [])})
            bulk_rows.extend(page_rows)
            if not page_rows:
                break
            offset += len(page_rows)
            if len(page_rows) < args.page_size and offset < expected:
                errors.append(f"bulk page ended early at offset {offset}")
                break

        tokens: list[dict[str, Any]] = []
        source_metadata: list[dict[str, Any]] = []
        traits: list[dict[str, Any]] = []
        source_trait_rows: list[dict[str, Any]] = []
        for source_index, row in enumerate(bulk_rows):
            token_id = int(row.get("token_id")) if str(row.get("token_id", "")).isdigit() else None
            invocation = row.get("invocation")
            if token_id is None or not isinstance(invocation, int):
                errors.append(f"bulk row {source_index} has invalid token identity")
                continue
            try:
                validate_token(row, collection, token_id, invocation)
            except AcquisitionError as error:
                errors.append(str(error))
                continue
            uri_entry = uri_map.get(token_id)
            if uri_entry is None:
                errors.append(f"tokenURI missing for token {token_id}")
                continue
            feature_rows = []
            for feature_index, (feature, value) in enumerate(row["features"].items()):
                try:
                    text_value = scalar_text(value)
                except AcquisitionError as error:
                    errors.append(f"token {token_id} feature {feature!r}: {error}")
                    continue
                source_row_index = len(source_trait_rows)
                feature_rows.append({"feature_index": feature_index, "trait": str(feature), "raw_value": value, "value": text_value, "source_row_index": source_row_index})
                source_trait_rows.append({"source_row_index": source_row_index, "token_id": token_id, "collection_id": int(collection["collection_id"]), "feature_index": feature_index, "trait": str(feature), "raw_value": value, "value": text_value})
                traits.append({"token_id": token_id, "collection_id": int(collection["collection_id"]), "trait": str(feature), "value": text_value, "source_row_index": source_row_index, "source_feature_index": feature_index})
            source_metadata.append({"token_id": token_id, "invocation": invocation, "source_index": source_index, "hasura_id": row.get("id"), "hasura_project_id": row.get("project_id"), "token_hash": row.get("hash"), "features": row["features"], "live_view_url": row.get("live_view_url"), "media_url": row.get("media_url"), "primary_asset_url": row.get("primary_asset_url"), "token_uri": uri_entry["uri"], "token_uri_rpc_response": uri_entry["raw_response"]})
            tokens.append({"id": token_id, "collection_id": int(collection["collection_id"]), "invocation": invocation, "source_index": source_index, "token_uri": uri_entry["uri"], "token_uri_rpc_response": uri_entry["raw_response"], "rpc_id": uri_entry.get("rpc_id"), "token_hash": row.get("hash"), "live_view_url": row.get("live_view_url"), "media_url": row.get("media_url"), "primary_asset_url": row.get("primary_asset_url")})

        canonical_tokens = sorted(tokens, key=lambda item: item["id"])
        canonical_traits = sorted(traits, key=lambda item: (item["token_id"], item["trait"], item["value"], item["source_feature_index"]))
        snapshot = {
            "schema": "6529nm.generative-trait-analysis-input/v1",
            "snapshot_id": f"6529NM.2026.001.{slug}.metadata.{block_number}",
            "observed_at": started,
            "source": {"kind": "artblocks-hasura-token-metadata-snapshot", "chain": "eip155:1", "contract_address": collection["contract_address"], "project_id": int(collection["project_id"]), "project_info_method": collection["project_info_method"], "project_info_response": project_state_raw, "project_info_attempts": project_state["response"].get("attempts", []) if project_state else [], "block_number": block_number, "block_hash": block_hash, "block_time": block_time, "bulk_graphql_uri": GRAPHQL_URI, "project_graphql_query_sha256": json_digest(PROJECT_QUERY), "project_graphql_variables": {"id": collection["project_graphql_id"], "chain_id": 1}, "project_graphql_response": project_raw, "bulk_query_sha256": json_digest(TOKENS_QUERY), "bulk_order": "token_id asc", "bulk_pages": pages, "token_uri_method": "eth_call tokenURI(uint256) at the observed block; every URI string is retained", "http_cross_check_policy": args.cross_check, "generator_policy": "live_view_url and primary_asset_url are recorded as source fields; generator bytes are not claimed preserved by this metadata snapshot"},
            "collection": {"id": int(collection["collection_id"]), "name": collection["name"], "artist": collection["artist"], "contract_address": collection["contract_address"], "project_id": int(collection["project_id"]), "caip19_core": f"eip155:1/erc721:{collection['contract_address'].lower()}"},
            "population": {"onchain_invocations": project_state["invocations"] if project_state else None, "onchain_max_invocations": expected, "graphql_invocations": project_row.get("invocations") if project_row else None, "graphql_max_invocations": project_row.get("max_invocations") if project_row else None, "expected_token_ids": expected_ids, "enumeration": "project_id * 1000000 + invocation, invocation 0 through max_invocations - 1"},
            "tokens": tokens,
            "traits": traits,
            "source_metadata": source_metadata,
            "source_trait_rows": source_trait_rows,
            "ordering": {"source_token_order": [item["id"] for item in tokens], "source_trait_row_order": [item["source_row_index"] for item in source_trait_rows], "canonical_token_order": [item["id"] for item in canonical_tokens], "canonical_trait_order": [item["source_row_index"] for item in canonical_traits], "source_order_definition": "Hasura page order: pages by offset, tokens ordered by token_id asc, features object insertion order", "canonical_order_definition": "tokens by numeric id; traits by token_id, trait, value, source_feature_index"},
            "materialization": {"version": "6529nm.artblocks-hasura-features-to-analysis-rows.v1", "raw_field": "tokens_metadata.features", "scalar_rule": "strings unchanged; booleans become lowercase JSON text; numbers use compact JSON text", "not_a_marketplace_metric": True},
            "analysis_input_note": "The traits array is an explicit Museum materialization of the authoritative Art Blocks Hasura features object; it is a technical distribution descriptor input, not a platform or marketplace rarity taxonomy.",
        }
        snapshot_path = run_root / "snapshots" / slug / "snapshot.json"
        write_json(snapshot_path, snapshot)

        cross_ids = {int(value) for value in collection.get("cross_check_token_ids", [])}
        if args.cross_check == "sampled":
            cross_ids.update(expected_ids[:1] + expected_ids[-1:])
        elif args.cross_check == "all":
            cross_ids.update(expected_ids)
        row_by_id = {row["id"]: row for row in tokens}
        cross_checks = []
        for token_id in sorted(cross_ids):
            if token_id in row_by_id:
                cross_checks.append(http_cross_check(run_root, collection, {"token_id": token_id, "features": next(item["features"] for item in source_metadata if item["token_id"] == token_id)}, next(item for item in tokens if item["id"] == token_id), timeout=args.timeout, retries=args.retries, sleep_ms=args.sleep_ms))
        for check in cross_checks:
            if check["error"] or check["identity_match"] is not True or check["features_match"] is not True:
                manifest["cross_check_warnings"].append({"collection": slug, **check})

        complete = not errors and len(bulk_rows) == expected and len(tokens) == expected and len(uri_map) == expected and len({item["id"] for item in tokens}) == expected and sorted(item["id"] for item in tokens) == expected_ids and all(page["returned_count"] > 0 for page in pages)
        collection_manifest = {"slug": slug, "name": collection["name"], "contract_address": collection["contract_address"], "project_id": int(collection["project_id"]), "population": {"onchain_max_invocations": expected, "graphql_max_invocations": project_row.get("max_invocations") if project_row else None, "expected_token_count": expected, "bulk_rows": len(bulk_rows), "token_uri_resolved": len(uri_map), "snapshot_tokens": len(tokens), "complete": complete}, "bulk_pages": pages, "token_uri_errors": uri_errors, "http_cross_checks": cross_checks, "snapshot_path": snapshot_path.relative_to(args.output_dir.resolve()).as_posix(), "snapshot_file_sha256": f"sha256:{digest(snapshot_path.read_bytes())}", "snapshot_canonical_sha256": json_digest(snapshot), "errors": sorted(set(errors))}
        manifest["collections"].append(collection_manifest)
        manifest["errors"].extend({"collection": slug, "error": error} for error in sorted(set(errors)))

    manifest["status"] = "complete" if not manifest["errors"] and all(row["population"]["complete"] for row in manifest["collections"]) else "incomplete"
    manifest_path = run_root / "run-manifest.json"
    write_json(manifest_path, manifest)
    output_dir = args.output_dir.resolve()
    write_json(output_dir / "latest-run.json", {"schema_version": "6529nm.casey-collection-latest-run.v2", "run_id": run_id, "status": manifest["status"], "manifest_path": manifest_path.relative_to(output_dir).as_posix(), "manifest_sha256": f"sha256:{digest(manifest_path.read_bytes())}", "review": None})
    write_json(output_dir / "pending-descriptors.json", {"schema_version": "6529nm.casey-collection-descriptor-jobs.v2", "status": "pending_dependency_pr4", "dependency": {"pull_request": 4, "required_state": "independently_approved_and_merged", "current_state_at_construction": "open_without_independent_approval", "final_outputs_permitted": False}, "run_id": run_id, "snapshot_manifest": manifest_path.relative_to(output_dir).as_posix(), "constructor": manifest["constructor"], "review": None, "curatorial_significance": None, "jobs": [{"collection": row["slug"], "input": row["snapshot_path"], "output": f"descriptors/{row['slug']}.json", "status": "blocked_dependency_pr4", "result": None, "review": None} for row in manifest["collections"]]})
    print(json.dumps({"run_id": run_id, "status": manifest["status"], "manifest": str(manifest_path)}, indent=2))
    return 0 if manifest["status"] == "complete" else 1


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--rpc-url", default="https://ethereum.publicnode.com")
    parser.add_argument("--page-size", type=int, default=250)
    parser.add_argument("--rpc-batch-size", type=int, default=100)
    parser.add_argument("--cross-check", choices=("none", "sampled", "all"), default="sampled")
    parser.add_argument("--timeout", type=float, default=30.0)
    parser.add_argument("--retries", type=int, default=3)
    parser.add_argument("--sleep-ms", type=int, default=100)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    try:
        return run(parse_args(argv))
    except (AcquisitionError, OSError, UnicodeError, json.JSONDecodeError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
