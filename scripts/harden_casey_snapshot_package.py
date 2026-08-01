#!/usr/bin/env python3
"""Harden an existing Casey acquisition run without network access.

The v2 acquisition preserved successful raw response bodies but did not retain
every request body or every batch attempt on disk. This command reconstructs
those canonical request bytes from the preserved configuration, token IDs, and
pinned block, explicitly labels the reconstruction, and fails closed whenever
the preserved bodies cannot support the reconstruction. It never performs
HTTP or JSON-RPC I/O.
"""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys
from typing import Any
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "evidence/casey-reas-collection-snapshots"
RUN_ID = "20260801T172252532Z"
TOKEN_ID_MULTIPLIER = 1_000_000
PR4_MERGE_COMMIT = "ff1c5825e3b61bfb2df0a639e057297beb946e4d"
RETRY_POLICY = {
    "max_retries": 2,
    "max_attempts": 3,
    "retry_delay_ms": 100,
    "retry_statuses": [408, 425, 429, "5xx", "network_error", "timeout"],
    "timestamp_mode": "not_recorded_in_v2; deterministic attempt ordinals retained",
}
EXPECTED = {
    "century": {
        "name": "CENTURY",
        "contract_address": "0xa7d8d9ef8d8ce8992df33d8b8cf4aebabd5bd270",
        "project_id": 100,
        "collection_id": 100,
        "project_info_method": "projectTokenInfo(uint256)",
    },
    "pre-process": {
        "name": "Pre-Process",
        "contract_address": "0x99a9b7c1116f9ceeb1652de04d5969cce509b069",
        "project_id": 383,
        "collection_id": 383,
        "project_info_method": "projectStateData(uint256)",
    },
    "phototaxis": {
        "name": "Phototaxis",
        "contract_address": "0xa7d8d9ef8d8ce8992df33d8b8cf4aebabd5bd270",
        "project_id": 164,
        "collection_id": 164,
        "project_info_method": "projectTokenInfo(uint256)",
    },
    "923-empty-rooms": {
        "name": "923 EMPTY ROOMS",
        "contract_address": "0x145789247973c5d612bf121e9e4eef84b63eb707",
        "project_id": 1,
        "collection_id": 1,
        "project_info_method": "projectStateData(uint256)",
    },
    "ex-nihilo-cosmos": {
        "name": "Ex Nihilo (Cosmos)",
        "contract_address": "0x0000000c687daed0fba60d1dba4e5f6149e8b894",
        "project_id": 0,
        "collection_id": 0,
        "project_info_method": "projectStateData(uint256)",
    },
}
RPC_URI = "https://ethereum.publicnode.com"
GRAPHQL_URI = "https://data.artblocks.io/v1/graphql"
TOKEN_URI_SELECTOR = "c87b56dd"
PROJECT_TOKEN_INFO_SELECTOR = "8c2c3622"
PROJECT_STATE_DATA_SELECTOR = "0ea5613f"


class HardeningError(RuntimeError):
    """Raised when existing observations cannot support a fail-closed ledger."""


def canonical_json(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def pretty_json(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode("utf-8")


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def digest_json(value: Any) -> str:
    return f"sha256:{sha256_bytes(canonical_json(value))}"


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_bytes(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(payload)


def write_json(path: Path, value: Any) -> None:
    write_bytes(path, pretty_json(value))


def raw_path(run_root: Path, ref: dict[str, Any]) -> Path:
    relative = ref.get("path")
    if not isinstance(relative, str) or not relative.startswith("raw/"):
        raise HardeningError(f"not a raw relative reference: {ref!r}")
    path = (run_root / relative).resolve()
    if run_root.resolve() not in path.parents or not path.is_file():
        raise HardeningError(f"missing raw response: {relative}")
    payload = path.read_bytes()
    expected = ref.get("sha256")
    actual = f"sha256:{sha256_bytes(payload)}"
    if actual != expected or len(payload) != ref.get("size"):
        raise HardeningError(f"raw reference hash/size mismatch: {relative}")
    return path


def raw_bytes(run_root: Path, ref: dict[str, Any]) -> bytes:
    return raw_path(run_root, ref).read_bytes()


def derived_ref(run_root: Path, category: str, payload: bytes) -> dict[str, Any]:
    sha = sha256_bytes(payload)
    relative = Path("derived") / category / f"sha256-{sha}.json"
    write_bytes(run_root / relative, payload)
    return {"path": relative.as_posix(), "sha256": f"sha256:{sha}", "size": len(payload), "byte_mode": "reconstructed_from_preserved_v2_invocation"}


def endpoint_authority(uri: str) -> str:
    parsed = urlparse(uri)
    if parsed.scheme != "https" or not parsed.netloc:
        raise HardeningError(f"non-HTTPS or malformed endpoint: {uri}")
    return parsed.netloc


def normalize_attempts(attempts: list[dict[str, Any]], *, mode: str) -> list[dict[str, Any]]:
    if not attempts:
        return [{"ordinal": 1, "status": 200, "ok": True, "basis": "preserved successful response", "mode": mode}]
    normalized = []
    for item in attempts:
        ordinal = item.get("attempt", item.get("ordinal"))
        if not isinstance(ordinal, int) or ordinal < 1:
            raise HardeningError(f"invalid attempt ordinal: {item!r}")
        normalized.append({"ordinal": ordinal, "status": item.get("status"), "ok": item.get("ok"), "error": item.get("error"), "mode": mode})
    return normalized


def request_record(
    *,
    request_id: str,
    family: str,
    endpoint: str,
    operation: str,
    http_method: str,
    payload: Any,
    request_ref: dict[str, Any],
    response_ref: dict[str, Any],
    attempts: list[dict[str, Any]],
    attempts_mode: str,
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    record = {
        "request_id": request_id,
        "family": family,
        "endpoint": endpoint,
        "endpoint_authority": endpoint_authority(endpoint),
        "http_method": http_method,
        "operation": operation,
        "request_payload": payload,
        "request_body": request_ref,
        "request_body_sha256": request_ref["sha256"],
        "request_bytes_mode": request_ref["byte_mode"],
        "response": {"raw_ref": response_ref, "response_sha256": response_ref["sha256"], "status_inferred": 200},
        "retry_policy": RETRY_POLICY,
        "attempts": normalize_attempts(attempts, mode=attempts_mode),
        "attempts_mode": attempts_mode,
        "attempt_timestamps": {"mode": RETRY_POLICY["timestamp_mode"], "timestamps": None},
        "discarded_partial_response": {
            "bytes_present": False,
            "basis": "v2 acquisition stored only the final response body; no retry partial body was preserved",
            "not_claimed": "network-level absence of an unpersisted partial body cannot be independently proven",
        },
    }
    if extra:
        record.update(extra)
    return record


def project_info_selector(method: str) -> str:
    if method == "projectTokenInfo(uint256)":
        return PROJECT_TOKEN_INFO_SELECTOR
    if method == "projectStateData(uint256)":
        return PROJECT_STATE_DATA_SELECTOR
    raise HardeningError(f"unsupported project info method: {method}")


def expected_ids(project_id: int, count: int) -> list[int]:
    return [project_id * TOKEN_ID_MULTIPLIER + invocation for invocation in range(count)]


def token_response_rows(run_root: Path, refs: list[dict[str, Any]]) -> dict[str, tuple[dict[str, Any], dict[str, Any]]]:
    rows: dict[str, tuple[dict[str, Any], dict[str, Any]]] = {}
    for ref in refs:
        payload = json.loads(raw_bytes(run_root, ref).decode("utf-8"))
        if not isinstance(payload, list):
            raise HardeningError(f"tokenURI response is not a JSON-RPC batch: {ref}")
        for row in payload:
            if not isinstance(row, dict) or not isinstance(row.get("id"), str):
                raise HardeningError(f"malformed tokenURI batch member: {ref}")
            if row["id"] in rows:
                raise HardeningError(f"duplicate tokenURI response member: {row['id']}")
            rows[row["id"]] = (row, ref)
    return rows


def build_request_provenance(output_dir: Path, run_root: Path, config: dict[str, Any], manifest: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    records: list[dict[str, Any]] = []
    request_body_refs: dict[str, dict[str, Any]] = {}
    block_tag = manifest["observation"]["block_tag"]

    def add_request(**kwargs: Any) -> None:
        record = request_record(**kwargs)
        records.append(record)
        request_body_refs[record["request_body"]["path"]] = record["request_body"]

    shared = manifest["rpc"]
    block_number_payload = {"jsonrpc": "2.0", "id": "block-number", "method": "eth_blockNumber", "params": []}
    block_number_body = derived_ref(run_root, "request-bytes", canonical_json(block_number_payload))
    add_request(request_id="block-number", family="rpc_shared", endpoint=RPC_URI, operation="eth_blockNumber", http_method="POST", payload=block_number_payload, request_ref=block_number_body, response_ref=shared["block_number_source"], attempts=shared.get("block_number_attempts", []), attempts_mode="contemporaneous_v2_manifest")
    block_payload = {"jsonrpc": "2.0", "id": "observed-block", "method": "eth_getBlockByNumber", "params": [block_tag, False]}
    block_body = derived_ref(run_root, "request-bytes", canonical_json(block_payload))
    add_request(request_id="observed-block", family="rpc_shared", endpoint=RPC_URI, operation="eth_getBlockByNumber", http_method="POST", payload=block_payload, request_ref=block_body, response_ref=shared["block_source"], attempts=shared.get("block_attempts", []), attempts_mode="contemporaneous_v2_manifest")

    for collection in config["collections"]:
        slug = collection["slug"]
        expected = EXPECTED[slug]
        snapshot_path = output_dir / next(row["snapshot_path"] for row in manifest["collections"] if row["slug"] == slug)
        snapshot = read_json(snapshot_path)
        source = snapshot["source"]
        project_id = int(collection["project_id"])
        selector = project_info_selector(collection["project_info_method"])
        project_payload = {
            "jsonrpc": "2.0",
            "id": f"project-info-{slug}",
            "method": "eth_call",
            "params": [{"to": collection["contract_address"], "data": "0x" + selector + project_id.to_bytes(32, "big").hex()}, block_tag],
        }
        project_body = derived_ref(run_root, "request-bytes", canonical_json(project_payload))
        add_request(request_id=f"project-info-{slug}", family="rpc_project_population", endpoint=RPC_URI, operation=collection["project_info_method"], http_method="POST", payload=project_payload, request_ref=project_body, response_ref=source["project_info_response"], attempts=source.get("project_info_attempts", []), attempts_mode="contemporaneous_v2_snapshot", extra={"collection": slug, "contract_address": expected["contract_address"], "project_id": project_id})

        project_graphql_payload = {"query": manifest["bulk_source"]["project_query"], "variables": {"id": collection["project_graphql_id"], "chain_id": 1}}
        project_graphql_body = derived_ref(run_root, "request-bytes", canonical_json(project_graphql_payload))
        add_request(request_id=f"project-metadata-{slug}", family="graphql_project_metadata", endpoint=GRAPHQL_URI, operation="CaseyProject", http_method="POST", payload=project_graphql_payload, request_ref=project_graphql_body, response_ref=source["project_graphql_response"], attempts=[], attempts_mode="reconstructed_success_only", extra={"collection": slug})

        collection_manifest = next(row for row in manifest["collections"] if row["slug"] == slug)
        page_refs = {page["raw_response"]["path"]: page for page in collection_manifest["bulk_pages"]}
        for page in collection_manifest["bulk_pages"]:
            payload = {"query": manifest["bulk_source"]["token_query"], "variables": page["variables"]}
            body = derived_ref(run_root, "request-bytes", canonical_json(payload))
            if body["sha256"] != page["request_sha256"]:
                raise HardeningError(f"bulk request hash reconstruction mismatch: {slug} offset {page['offset']}")
            add_request(request_id=f"tokens-metadata-{slug}-{page['offset']}", family="graphql_tokens_metadata", endpoint=GRAPHQL_URI, operation="CaseyTokens", http_method="POST", payload=payload, request_ref=body, response_ref=page["raw_response"], attempts=page.get("attempts", []), attempts_mode="contemporaneous_v2_manifest", extra={"collection": slug, "offset": page["offset"], "limit": page["limit"], "returned_count": page["returned_count"]})

        token_ids = snapshot["population"]["expected_token_ids"]
        unique_refs: dict[str, dict[str, Any]] = {row["token_uri_rpc_response"]["path"]: row["token_uri_rpc_response"] for row in snapshot["tokens"]}
        response_members = token_response_rows(run_root, list(unique_refs.values()))
        batch_size = int(manifest["rpc"]["batch_size"])
        for batch_number, start in enumerate(range(0, len(token_ids), batch_size)):
            batch_ids = token_ids[start : start + batch_size]
            expected_member_ids = {f"token-uri-{token_id}" for token_id in batch_ids}
            candidate_refs = {ref["path"]: ref for ref in unique_refs.values() if expected_member_ids.issubset({key for key, (_, response_ref) in response_members.items() if response_ref["path"] == ref["path"]})}
            if len(candidate_refs) != 1:
                raise HardeningError(f"cannot identify one preserved tokenURI batch response for {slug} batch {batch_number}")
            response_ref = next(iter(candidate_refs.values()))
            request_payload = [
                {"jsonrpc": "2.0", "id": f"token-uri-{token_id}", "method": "eth_call", "params": [{"to": collection["contract_address"], "data": "0x" + TOKEN_URI_SELECTOR + int(token_id).to_bytes(32, "big").hex()}, block_tag]}
                for token_id in batch_ids
            ]
            request_body = derived_ref(run_root, "request-bytes", canonical_json(request_payload))
            for token_id in batch_ids:
                member_id = f"token-uri-{token_id}"
                member, member_ref = response_members.get(member_id, ({}, None))
                if member_ref is None or member_ref["path"] != response_ref["path"] or not isinstance(member.get("result"), str):
                    raise HardeningError(f"missing successful tokenURI response member {member_id}")
                add_request(request_id=member_id, family="rpc_token_uri", endpoint=RPC_URI, operation="tokenURI(uint256)", http_method="POST", payload=request_payload[batch_ids.index(token_id)], request_ref=request_body, response_ref=response_ref, attempts=[], attempts_mode="reconstructed_success_only", extra={"collection": slug, "token_id": int(token_id), "batch_number": batch_number, "batch_offset": start, "batch_request_body_sha256": request_body["sha256"], "response_member_id": member_id, "response_member_digest": digest_json(member)})

    provenance = {
        "schema_version": "6529nm.casey-request-provenance.v1",
        "run_id": manifest["run_id"],
        "network_fetch_status": "offline_reconstruction_only",
        "reconstruction_notice": "Request bodies are cryptographically reconstructed from preserved v2 configuration, invocation IDs, variables, and pinned block tag; original request body bytes were not persisted by v2. Response bodies are contemporaneous content-addressed bytes.",
        "retry_policy": RETRY_POLICY,
        "request_counts": {"total_records": len(records), "token_uri": sum(1 for row in records if row["family"] == "rpc_token_uri"), "project_graphql": sum(1 for row in records if row["family"] == "graphql_project_metadata"), "bulk_graphql": sum(1 for row in records if row["family"] == "graphql_tokens_metadata"), "project_population_rpc": sum(1 for row in records if row["family"] == "rpc_project_population"), "shared_rpc": sum(1 for row in records if row["family"] == "rpc_shared")},
        "unique_request_bodies": sorted(request_body_refs.values(), key=lambda ref: ref["path"]),
        "requests": records,
    }
    provenance_ref = derived_ref(run_root, "provenance", pretty_json(provenance))
    return provenance, provenance_ref


def build_exclusions(run_root: Path, output_dir: Path, manifest: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for collection in manifest["collections"]:
        for check in collection["http_cross_checks"]:
            raw_ref = check.get("raw_response")
            if not isinstance(raw_ref, dict):
                raise HardeningError(f"cross-check has no preserved raw response: {collection['slug']} {check.get('token_id')}")
            metadata = json.loads(raw_bytes(run_root, raw_ref).decode("utf-8"))
            traits = metadata.get("traits")
            if not isinstance(traits, list) or not traits:
                raise HardeningError(f"cross-check has no traits array: {collection['slug']} {check.get('token_id')}")
            marker = traits[0]
            if not isinstance(marker, dict) or not isinstance(marker.get("value"), str) or not marker["value"].lower().startswith("all "):
                raise HardeningError(f"expected group marker is absent or not first: {collection['slug']} {check.get('token_id')}")
            rows.append({"collection": collection["slug"], "cross_check_order": len(rows), "token_id": int(check["token_id"]), "source_uri": check["source_uri"], "retrieval_uri": check["retrieval_uri"], "raw_response": raw_ref, "source_location": "traits[0]", "source_order": 0, "excluded_row": marker, "reason": "Art Blocks token endpoint group marker ('All <collection>') is not a token feature row", "token_identity": {"metadata_token_id": metadata.get("tokenID"), "contract_address": metadata.get("contract_address")}})
    reasons = Counter(row["reason"] for row in rows)
    summary = {"schema_version": "6529nm.casey-http-exclusions.v1", "run_id": manifest["run_id"], "observed_cross_check_count": sum(len(c["http_cross_checks"]) for c in manifest["collections"]), "excluded_row_count": len(rows), "by_reason": dict(reasons), "rows": rows, "fail_closed_rule": "exactly one excluded row per observed cross-check, always traits[0] with an All <collection> value; any other exclusion or missing cross-check fails verification"}
    return summary, derived_ref(run_root, "provenance", pretty_json(summary))


def harden(output_dir: Path) -> dict[str, Any]:
    output_dir = output_dir.resolve()
    run_root = output_dir / "runs" / RUN_ID
    config = read_json(output_dir / "collection-sources.json")
    latest = read_json(output_dir / "latest-run.json")
    manifest = read_json(output_dir / latest["manifest_path"])
    if manifest["run_id"] != RUN_ID or manifest.get("status") != "complete":
        raise HardeningError("expected the complete v2 run as the hardening input")
    if set(row["slug"] for row in config["collections"]) != set(EXPECTED):
        raise HardeningError("unexpected collection set")
    for collection in config["collections"]:
        expected = EXPECTED[collection["slug"]]
        for key in ("name", "contract_address", "project_id", "collection_id", "project_info_method"):
            if collection.get(key) != expected[key]:
                raise HardeningError(f"closed identity mismatch in config: {collection['slug']} {key}")
    for row in manifest["collections"]:
        snapshot_path = output_dir / row["snapshot_path"]
        snapshot = read_json(snapshot_path)
        materialization = snapshot.get("materialization")
        if isinstance(materialization, dict):
            materialization.pop("not_a_marketplace_metric", None)
        write_json(snapshot_path, snapshot)
        payload = snapshot_path.read_bytes()
        row["snapshot_file_sha256"] = f"sha256:{sha256_bytes(payload)}"
        row["snapshot_canonical_sha256"] = digest_json(snapshot)
    provenance, provenance_ref = build_request_provenance(output_dir, run_root, config, manifest)
    exclusions, exclusions_ref = build_exclusions(run_root, output_dir, manifest)
    manifest["schema_version"] = "6529nm.casey-collection-run-manifest.v3"
    manifest["request_provenance"] = provenance_ref
    manifest["exclusion_summary"] = exclusions_ref
    manifest["raw_observation_integrity"] = {"raw_directory": "raw", "raw_file_count": len([p for p in (run_root / "raw").rglob("*") if p.is_file()]), "raw_bytes_are_unchanged": True}
    manifest_path = run_root / "run-manifest.json"
    write_json(manifest_path, manifest)
    latest["manifest_sha256"] = f"sha256:{sha256_bytes(manifest_path.read_bytes())}"
    latest.pop("package_manifest", None)
    write_json(output_dir / "latest-run.json", latest)
    return {"run_id": RUN_ID, "status": "hardened", "token_uri_requests": provenance["request_counts"]["token_uri"], "project_graphql_requests": provenance["request_counts"]["project_graphql"], "bulk_graphql_requests": provenance["request_counts"]["bulk_graphql"], "excluded_rows": exclusions["excluded_row_count"], "raw_files": manifest["raw_observation_integrity"]["raw_file_count"]}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args(argv)
    try:
        print(json.dumps(harden(args.output_dir), ensure_ascii=False, indent=2))
    except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError, HardeningError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
