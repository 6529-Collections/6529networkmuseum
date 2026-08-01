"""Transparent compatibility implementation of 6529's NextGen analysis.

The implementation intentionally follows the arithmetic and ranking behavior in
6529seize-backend's ``src/nextgen/nextgen_tokens.ts``.  It does not fetch data,
query a marketplace, or infer missing metadata.  Callers provide a complete,
dated input snapshot and receive the normalized input, quality observations,
per-trait rows, per-token scores, and deterministic hashes.
"""

from __future__ import annotations

from collections import Counter
from copy import deepcopy
import hashlib
import json
import math
import platform
from pathlib import Path
from typing import Any, Iterable


ALGORITHM_ID = "6529-nextgen-trait-prevalence-v1"
BACKEND_COMMIT = "902557e9274f03b9851e97ef7ffac4b3c310b8a0"
NEXTGEN_COMMIT = "73c09d1c07e405ddb9ccdd462283ab98ea68f903"
MINT_TYPE_TRAIT = "Mint Type"
MINT_TYPE_TRAIT_PREFIX = MINT_TYPE_TRAIT.lower()

BACKEND_SOURCE_URL = (
    "https://github.com/6529-Collections/6529seize-backend/"
    f"blob/{BACKEND_COMMIT}/src/nextgen/nextgen_tokens.ts"
)
CONSTANTS_SOURCE_URL = (
    "https://github.com/6529-Collections/6529seize-backend/"
    f"blob/{BACKEND_COMMIT}/src/nextgen/nextgen_constants.ts"
)
NEXTGEN_SOURCE_URL = (
    "https://github.com/6529-Collections/nextgen/"
    f"tree/{NEXTGEN_COMMIT}/hardhat/smart-contracts"
)

TRAIT_SCORE_FIELDS = (
    "rarity_score",
    "rarity_score_normalised",
    "statistical_rarity",
    "statistical_rarity_normalised",
    "single_trait_rarity_score_normalised",
    "rarity_score_trait_count_normalised",
)

TOKEN_SCORE_FIELDS = (
    "rarity_score",
    "rarity_score_normalised",
    "rarity_score_trait_count",
    "rarity_score_trait_count_normalised",
    "statistical_score",
    "statistical_score_trait_count",
    "statistical_score_normalised",
    "statistical_score_trait_count_normalised",
    "single_trait_rarity_score",
    "single_trait_rarity_score_trait_count",
    "single_trait_rarity_score_normalised",
    "single_trait_rarity_score_trait_count_normalised",
)

TOKEN_RANK_DIRECTIONS = {
    "rarity_score": "descending",
    "rarity_score_normalised": "descending",
    "rarity_score_trait_count": "descending",
    "rarity_score_trait_count_normalised": "descending",
    "statistical_score": "ascending",
    "statistical_score_trait_count": "ascending",
    "statistical_score_normalised": "ascending",
    "statistical_score_trait_count_normalised": "ascending",
    "single_trait_rarity_score": "ascending",
    "single_trait_rarity_score_trait_count": "ascending",
    "single_trait_rarity_score_normalised": "ascending",
    "single_trait_rarity_score_trait_count_normalised": "ascending",
}


class InputError(ValueError):
    """Raised when a snapshot cannot be analyzed without an implicit repair."""


def determinism_profile() -> dict[str, str]:
    """Describe the runtime boundary for byte- and hash-stable output."""

    return {
        "implementation": platform.python_implementation(),
        "python_version": platform.python_version(),
        "json_encoder": (
            "stdlib json.dumps(ensure_ascii=False, allow_nan=False, "
            "sort_keys=True, separators=(',', ':'))"
        ),
        "float_encoding": (
            "CPython json.encoder shortest-round-trip float representation"
        ),
        "boundary": (
            "byte/hash reproducibility is guaranteed only for the same CPython "
            "implementation and version; review and regenerate fixtures after "
            "any implementation or version change"
        ),
    }


def canonical_json(value: Any) -> bytes:
    """Return the repository's compact, stable JSON form for hashing.

    This is deliberately smaller than RFC 8785 or a general JSON
    canonicalization implementation: snapshots are constrained to JSON
    values, UTF-8 text, finite IEEE-754 numbers, and sorted object keys.
    Array order is data and is therefore preserved. Float bytes are bounded
    by the CPython implementation/version reported by ``determinism_profile``.
    """

    return json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def sha256_json(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical_json(value)).hexdigest()


def _output_hash_payload(result: dict[str, Any]) -> dict[str, Any]:
    """Return the output payload with self-hashes and runtime metadata normalized."""

    payload = deepcopy(result)
    payload["hashes"] = {}
    payload.pop("determinism", None)
    return payload


def load_snapshot(path: str | Path) -> dict[str, Any]:
    """Load a UTF-8 JSON snapshot without changing its raw representation."""

    with Path(path).open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise InputError("snapshot root must be a JSON object")
    return value


def _require_int(value: Any, label: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise InputError(f"{label} must be an integer")
    return value


def _require_text(value: Any, label: str) -> str:
    if not isinstance(value, str):
        raise InputError(f"{label} must be a string")
    return value


def _is_mint_type(trait: str) -> bool:
    return trait.lower().startswith(MINT_TYPE_TRAIT_PREFIX)


def _is_none_value(value: str) -> bool:
    return value.lower().startswith("none")


OPEN_SEA_METRIC_TERMS = (
    "rarity",
    "rank",
    "score",
    "metric",
    "percentile",
    "frequency",
    "prevalence",
    "floor",
    "price",
    "sale",
    "volume",
)
RARITY_METRIC_TERMS = (
    "rarity",
    "rank",
    "score",
    "metric",
    "percentile",
    "frequency",
    "prevalence",
)
PROVIDER_KEYS = {"source", "provider", "marketplace", "origin", "issuer"}


def _normalized_key(key: Any) -> str:
    return "".join(character for character in str(key).lower() if character.isalnum())


def _is_metric_key(key: Any) -> bool:
    normalized = _normalized_key(key)
    return any(term in normalized for term in OPEN_SEA_METRIC_TERMS)


def _is_rarity_metric_key(key: Any) -> bool:
    normalized = _normalized_key(key)
    return any(term in normalized for term in RARITY_METRIC_TERMS)


def _is_opensea_metric_key(key: Any) -> bool:
    normalized = _normalized_key(key)
    return "opensea" in normalized and _is_metric_key(normalized)


def _contains_opensea_text(value: Any) -> bool:
    if isinstance(value, str):
        return "opensea" in value.lower()
    if isinstance(value, dict):
        return any(_contains_opensea_text(child) for child in value.values())
    if isinstance(value, list):
        return any(_contains_opensea_text(child) for child in value)
    return False


def _reject_opensea_metric_fields(value: Any, path: str = "snapshot") -> None:
    """Reject structured OpenSea metrics while allowing provenance text/citations."""

    if isinstance(value, dict):
        has_opensea_provider = any(
            _normalized_key(key) in PROVIDER_KEYS and _contains_opensea_text(child)
            for key, child in value.items()
        )
        has_metric_key = any(_is_rarity_metric_key(key) for key in value)
        if has_opensea_provider and has_metric_key:
            raise InputError(
                "OpenSea-sourced rarity metric fields are prohibited in Museum "
                f"snapshots: {path}"
            )
        for key, child in value.items():
            key_text = str(key)
            if _is_opensea_metric_key(key):
                raise InputError(
                    "OpenSea-sourced or computed rarity metric fields are "
                    f"prohibited in Museum rarity snapshots: {path}.{key_text}"
                )
            if _is_rarity_metric_key(key) and _contains_opensea_text(child):
                raise InputError(
                    "OpenSea-sourced or computed rarity metric fields are "
                    f"prohibited in Museum rarity snapshots: {path}.{key_text}"
                )
            _reject_opensea_metric_fields(child, f"{path}.{key_text}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            _reject_opensea_metric_fields(child, f"{path}[{index}]")


def _validate_snapshot_shape(snapshot: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    tokens_value = snapshot.get("tokens")
    traits_value = snapshot.get("traits")
    if not isinstance(tokens_value, list) or not tokens_value:
        raise InputError("snapshot.tokens must be a non-empty array")
    if not isinstance(traits_value, list) or not traits_value:
        raise InputError(
            "snapshot.traits must be a non-empty array; the source algorithm "
            "cannot divide by a zero observed-token count"
        )

    tokens: list[dict[str, Any]] = []
    for index, token in enumerate(tokens_value):
        if not isinstance(token, dict):
            raise InputError(f"tokens[{index}] must be an object")
        token_id = _require_int(token.get("id"), f"tokens[{index}].id")
        collection_id = _require_int(
            token.get("collection_id"), f"tokens[{index}].collection_id"
        )
        tokens.append({"id": token_id, "collection_id": collection_id})

    traits: list[dict[str, Any]] = []
    for index, row in enumerate(traits_value):
        if not isinstance(row, dict):
            raise InputError(f"traits[{index}] must be an object")
        token_id = _require_int(row.get("token_id"), f"traits[{index}].token_id")
        collection_id = _require_int(
            row.get("collection_id"), f"traits[{index}].collection_id"
        )
        trait = _require_text(row.get("trait"), f"traits[{index}].trait")
        value = _require_text(row.get("value"), f"traits[{index}].value")
        traits.append(
            {
                "token_id": token_id,
                "collection_id": collection_id,
                "trait": trait,
                "value": value,
            }
        )

    return tokens, traits


def _duplicate_groups(rows: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    groups: dict[tuple[int, str], list[str]] = {}
    for row in rows:
        key = (row["token_id"], row["trait"])
        groups.setdefault(key, []).append(row["value"])
    return [
        {
            "token_id": token_id,
            "trait": trait,
            "count": len(values),
            "values": sorted(values),
        }
        for (token_id, trait), values in sorted(groups.items())
        if len(values) > 1
    ]


def normalize_snapshot(
    snapshot: dict[str, Any], *, duplicate_policy: str = "error"
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Validate and deterministically order a raw snapshot.

    ``error`` is the safe default.  ``preserve`` reproduces the source's
    raw-row arithmetic (including duplicate rows) and is useful for forensic
    comparisons.  ``deduplicate`` is an explicit Museum preprocessing choice;
    it keeps the lexicographically smallest value for each ``(token_id,
    trait)`` key and must not be described as exact NextGen compatibility.
    """

    if duplicate_policy not in {"error", "preserve", "deduplicate"}:
        raise InputError(
            "duplicate_policy must be one of: error, preserve, deduplicate"
        )

    _reject_opensea_metric_fields(snapshot)
    tokens, raw_traits = _validate_snapshot_shape(snapshot)
    token_ids = [token["id"] for token in tokens]
    token_id_duplicates = sorted(
        token_id for token_id, count in Counter(token_ids).items() if count > 1
    )
    trait_duplicates = _duplicate_groups(raw_traits)
    declared_token_ids = set(token_ids)
    orphan_rows = [
        {
            "token_id": row["token_id"],
            "trait": row["trait"],
            "value": row["value"],
        }
        for row in raw_traits
        if row["token_id"] not in declared_token_ids
    ]

    if token_id_duplicates:
        raise InputError(f"duplicate token ids are not analyzable: {token_id_duplicates}")
    if orphan_rows and duplicate_policy == "error":
        raise InputError(
            "trait rows refer to undeclared tokens; add those tokens to the "
            "snapshot or choose --duplicates preserve for forensic analysis"
        )
    if trait_duplicates and duplicate_policy == "error":
        raise InputError(
            "duplicate (token_id, trait) rows found; choose --duplicates "
            "preserve or --duplicates deduplicate explicitly"
        )

    effective_traits = raw_traits
    deduplicated_rows: list[dict[str, Any]] = []
    if duplicate_policy == "deduplicate":
        by_key: dict[tuple[int, str], list[dict[str, Any]]] = {}
        for row in raw_traits:
            by_key.setdefault((row["token_id"], row["trait"]), []).append(row)
        effective_traits = []
        for (token_id, trait), rows in sorted(by_key.items()):
            kept_row = min(
                rows, key=lambda row: (row["value"], row["collection_id"])
            )
            effective_traits.append(kept_row)
            if len(rows) > 1:
                kept = False
                removed_values: list[str] = []
                for row in rows:
                    if row is kept_row and not kept:
                        kept = True
                    else:
                        removed_values.append(row["value"])
                deduplicated_rows.append(
                    {
                        "token_id": token_id,
                        "trait": trait,
                        "removed_values": sorted(removed_values),
                    }
                )

    normalized_tokens = sorted(tokens, key=lambda token: token["id"])
    normalized_traits = sorted(
        (
            {
                "token_id": row["token_id"],
                "collection_id": row["collection_id"],
                "trait": row["trait"],
                "value": row["value"],
            }
            for row in effective_traits
        ),
        key=lambda row: (row["token_id"], row["trait"], row["value"]),
    )

    rows_by_token = {token_id: 0 for token_id in token_ids}
    rows_by_trait: dict[str, set[int]] = {}
    for row in effective_traits:
        if row["token_id"] in rows_by_token:
            rows_by_token[row["token_id"]] += 1
        rows_by_trait.setdefault(row["trait"], set()).add(row["token_id"])

    quality = {
        "duplicate_policy": duplicate_policy,
        "duplicate_token_ids": token_id_duplicates,
        "duplicate_trait_rows": trait_duplicates,
        "deduplicated_rows": deduplicated_rows,
        "orphan_trait_rows": orphan_rows,
        "tokens_without_any_trait_rows": sorted(
            token_id for token_id, count in rows_by_token.items() if count == 0
        ),
        "missing_token_ids_by_observed_trait": [
            {
                "trait": trait,
                "missing_token_ids": sorted(declared_token_ids - token_ids_for_trait),
            }
            for trait, token_ids_for_trait in sorted(rows_by_trait.items())
        ],
        "raw_token_count": len(set(row["token_id"] for row in raw_traits)),
        "declared_token_count": len(normalized_tokens),
        "effective_trait_row_count": len(normalized_traits),
    }

    normalized = {
        "schema": "6529nm.generative-trait-analysis-input/v1",
        "collection": deepcopy(snapshot.get("collection")),
        "tokens": normalized_tokens,
        "traits": normalized_traits,
        "normalization": {
            "ordering": "tokens by token id; trait rows by token id, trait, value",
            "duplicate_policy": duplicate_policy,
            "missing_policy": "preserve absence; never synthesize a trait or None value",
            "mint_type_policy": (
                "retain Mint Type rows for audit and per-trait output; exclude "
                "them from score aggregates"
            ),
        },
    }
    return normalized, quality


def _competition_ranks(
    scores: list[dict[str, Any]], key: str, *, inverse: bool = False
) -> dict[int, int]:
    """Match NextGen's stable sort and competition rank behavior."""

    sorted_scores = sorted(
        scores,
        key=lambda score: score[key],
        reverse=not inverse,
    )
    ranks: dict[int, int] = {}
    current_rank = 1
    previous_score: float | None = None
    for index, score in enumerate(sorted_scores):
        value = score[key]
        if previous_score is not None and value == previous_score:
            ranks[score["id"]] = current_rank
        else:
            current_rank = index + 1
            ranks[score["id"]] = current_rank
            previous_score = value
    return ranks


def _dense_trait_ranks(rows: list[dict[str, Any]], key: str) -> None:
    """Match NextGen's per-category dense ranks (always descending)."""

    by_trait: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        by_trait.setdefault(row["trait"], []).append(row)
    for category_rows in by_trait.values():
        sorted_rows = sorted(category_rows, key=lambda row: row[key], reverse=True)
        if not sorted_rows:
            continue
        current_rank = 1
        previous_value = sorted_rows[0][key]
        for row in sorted_rows:
            if row[key] != previous_value:
                current_rank += 1
                previous_value = row[key]
            row[f"{key}_rank"] = current_rank


def _min_or_zero(values: list[float]) -> float:
    return min(values) if values else 0


def analyze_snapshot(
    snapshot: dict[str, Any], *, duplicate_policy: str = "error"
) -> dict[str, Any]:
    """Analyze a snapshot using the pinned NextGen backend algorithm."""

    normalized, quality = normalize_snapshot(
        snapshot, duplicate_policy=duplicate_policy
    )
    tokens = normalized["tokens"]
    traits = normalized["traits"]
    token_count = len(set(row["token_id"] for row in traits))
    if token_count == 0:
        raise InputError("the source algorithm has no observed token denominator")
    declared_token_count = len(tokens)

    trait_value_counts: dict[str, dict[str, int]] = {}
    for row in traits:
        values = trait_value_counts.setdefault(row["trait"], {})
        values[row["value"]] = values.get(row["value"], 0) + 1

    traits_count = len(
        {trait for trait in trait_value_counts if not _is_mint_type(trait)}
    )
    if traits_count == 0:
        raise InputError("no non-Mint Type trait categories are available")

    per_trait: list[dict[str, Any]] = []
    for row in traits:
        values = trait_value_counts[row["trait"]]
        trait_count = len(values)
        value_count = values[row["value"]]
        result = {
            "token_id": row["token_id"],
            "collection_id": row["collection_id"],
            "trait": row["trait"],
            "value": row["value"],
            "token_count": token_count,
            "trait_count": trait_count,
            "value_count": value_count,
        }
        if _is_mint_type(row["trait"]):
            for field in TRAIT_SCORE_FIELDS:
                result[field] = -1
        else:
            statistical_score = value_count / token_count
            result.update(
                {
                    "statistical_rarity": statistical_score,
                    "single_trait_rarity_score_normalised": (
                        statistical_score * trait_count
                    ),
                    "statistical_rarity_normalised": statistical_score
                    ** (1 / trait_count),
                    "rarity_score": token_count / value_count,
                    "rarity_score_normalised": (
                        ((1 / value_count) * 1_000_000)
                        / (traits_count * trait_count)
                    ),
                    "rarity_score_trait_count_normalised": (
                        ((1 / value_count) * 1_000_000)
                        / ((traits_count + 1) * trait_count)
                    ),
                }
            )
        per_trait.append(result)

    for field in TRAIT_SCORE_FIELDS:
        _dense_trait_ranks(per_trait, field)

    traits_by_token: dict[int, list[dict[str, Any]]] = {
        token["id"]: [] for token in tokens
    }
    for row in per_trait:
        if row["token_id"] in traits_by_token and not _is_mint_type(row["trait"]):
            traits_by_token[row["token_id"]].append(row)

    trait_categories: set[str] = set()
    trait_categories_with_none: set[str] = set()
    trait_count_per_token: dict[int, int] = {}
    for token in tokens:
        token_rows = traits_by_token[token["id"]]
        for row in token_rows:
            trait_categories.add(row["trait"])
            if _is_none_value(row["value"]):
                trait_categories_with_none.add(row["trait"])
        trait_count_per_token[token["id"]] = len(
            {
                row["trait"]
                for row in token_rows
                if not _is_none_value(row["value"])
            }
        )

    trait_count_frequencies = dict(Counter(trait_count_per_token.values()))

    per_token: list[dict[str, Any]] = []
    for token in tokens:
        token_rows = traits_by_token[token["id"]]
        rarity_score = sum(row["rarity_score"] for row in token_rows)
        rarity_score_normalised = sum(
            row["rarity_score_normalised"] for row in token_rows
        )
        rarity_score_trait_count_normalised = sum(
            row["rarity_score_trait_count_normalised"] for row in token_rows
        )
        statistical_score = math.prod(
            (row["statistical_rarity"] for row in token_rows), start=1
        )
        statistical_score_normalised = math.prod(
            (row["statistical_rarity_normalised"] for row in token_rows), start=1
        )
        single_trait_rarity = _min_or_zero(
            [row["statistical_rarity"] for row in token_rows]
        )
        single_trait_rarity_normalised = _min_or_zero(
            [row["single_trait_rarity_score_normalised"] for row in token_rows]
        )
        # Math.min(...[]) is +Infinity in JavaScript.  The following value is
        # finite because the second operand is finite for every declared token.
        min_single_trait_rarity_normalised = (
            min(
                [
                    row["single_trait_rarity_score_normalised"]
                    for row in token_rows
                ]
                or [math.inf]
            )
        )

        trait_count = trait_count_per_token[token["id"]]
        denominator = trait_count_frequencies[trait_count]
        rarity_score_trait_count = declared_token_count / denominator + rarity_score
        rarity_score_trait_count_normalised_adjustment = (
            ((1 / denominator) * 1_000_000)
            / ((len(trait_categories) + 1) * (len(trait_categories_with_none) + 1))
        )
        rarity_score_trait_count_normalised_adjusted = (
            rarity_score_trait_count_normalised
            + rarity_score_trait_count_normalised_adjustment
        )
        statistical_score_trait_count = statistical_score * (
            denominator / declared_token_count
        )
        statistical_score_trait_count_normalised = statistical_score_normalised * (
            denominator / declared_token_count
        ) ** (1 / (len(trait_categories_with_none) + 1))
        single_trait_rarity_trait_count = min(
            single_trait_rarity, denominator / declared_token_count
        )
        single_trait_rarity_trait_count_normalization = (
            denominator / declared_token_count
        ) * (len(trait_categories_with_none) + 1)
        single_trait_rarity_trait_count_normalised = min(
            min_single_trait_rarity_normalised,
            single_trait_rarity_trait_count_normalization,
        )

        per_token.append(
            {
                "id": token["id"],
                "collection_id": token["collection_id"],
                "trait_count": trait_count,
                "trait_count_denominator": denominator,
                "rarity_score": rarity_score,
                "rarity_score_normalised": rarity_score_normalised,
                "rarity_score_trait_count": rarity_score_trait_count,
                "rarity_score_trait_count_normalised": (
                    rarity_score_trait_count_normalised_adjusted
                ),
                "statistical_score": statistical_score,
                "statistical_score_trait_count": statistical_score_trait_count,
                "statistical_score_normalised": statistical_score_normalised,
                "statistical_score_trait_count_normalised": (
                    statistical_score_trait_count_normalised
                ),
                "single_trait_rarity_score": single_trait_rarity,
                "single_trait_rarity_score_trait_count": (
                    single_trait_rarity_trait_count
                ),
                "single_trait_rarity_score_normalised": (
                    single_trait_rarity_normalised
                ),
                "single_trait_rarity_score_trait_count_normalised": (
                    single_trait_rarity_trait_count_normalised
                ),
            }
        )

    for field in TOKEN_SCORE_FIELDS:
        ranks = _competition_ranks(
            per_token,
            field,
            inverse=TOKEN_RANK_DIRECTIONS[field] == "ascending",
        )
        for row in per_token:
            row[f"{field}_rank"] = ranks[row["id"]]

    normalized_snapshot_sha256 = sha256_json(normalized)
    raw_snapshot_sha256 = sha256_json(snapshot)
    result: dict[str, Any] = {
        "schema": "6529nm.generative-trait-analysis-output/v1",
        "algorithm": {
            "id": ALGORITHM_ID,
            "backend_commit": BACKEND_COMMIT,
            "backend_source": BACKEND_SOURCE_URL,
            "constants_source": CONSTANTS_SOURCE_URL,
            "nextgen_contract_commit": NEXTGEN_COMMIT,
            "nextgen_contract_source": NEXTGEN_SOURCE_URL,
            "mint_type_trait": MINT_TYPE_TRAIT,
        },
        "configuration": {
            "duplicate_policy": duplicate_policy,
            "token_count_for_trait_prevalence": "distinct token_id values in effective trait rows",
            "token_count_for_token_scores": "declared snapshot token rows",
            "missing_trait_policy": "absence is preserved; no synthetic None values",
            "none_value_policy": "values whose lowercase text starts with 'none' are excluded from trait_count but retained in score products",
            "trait_rank_tie_policy": "dense rank, descending, independently within each trait category",
            "token_rank_tie_policy": "competition rank, stable sort, direction depends on score family",
            "opensea_policy": (
                "reject structured OpenSea-sourced or computed metric fields; "
                "allow provenance prose, citations, and URLs that mention OpenSea"
            ),
        },
        "determinism": determinism_profile(),
        "input": {
            "snapshot": deepcopy(snapshot),
            "snapshot_sha256": raw_snapshot_sha256,
            "normalized_snapshot": normalized,
            "normalized_snapshot_sha256": normalized_snapshot_sha256,
            "data_quality": quality,
        },
        "collection_summary": {
            "declared_token_count": declared_token_count,
            "observed_token_count": token_count,
            "non_mint_type_trait_category_count": traits_count,
            "trait_category_count": len(trait_categories),
            "trait_category_with_none_count": len(trait_categories_with_none),
            "trait_count_frequencies": {
                str(key): value
                for key, value in sorted(trait_count_frequencies.items())
            },
        },
        "per_trait": per_trait,
        "per_token": per_token,
        "hashes": {},
    }
    result["hashes"] = {
        "input_snapshot_sha256": raw_snapshot_sha256,
        "normalized_snapshot_sha256": normalized_snapshot_sha256,
        "output_sha256": sha256_json(_output_hash_payload(result)),
    }
    return result
