# Casey REAS collection metadata snapshots

Status: acquisition package and collection-level statistical descriptors were
constructed on 2026-08-01 UTC after the independent approval and merge of
Museum PR #4. Outputs remain pending independent review. This package does
not accept title, rights, accession, or curatorial-significance claims.

This package is the source-and-acquisition layer for the five Art Blocks
projects represented by accession lot `6529NM.2026.001`:

| Collection | Contract | Project | Population at the pinned observation |
|---|---|---:|---:|
| CENTURY | `0xa7d8d9ef8d8ce8992df33d8b8cf4aebabd5bd270` | 100 | 1,000 |
| Pre-Process | `0x99a9b7c1116f9ceeb1652de04d5969cce509b069` | 383 | 120 |
| Phototaxis | `0xa7d8d9ef8d8ce8992df33d8b8cf4aebabd5bd270` | 164 | 1,000 |
| 923 EMPTY ROOMS | `0x145789247973c5d612bf121e9e4eef84b63eb707` | 1 | 924 |
| Ex Nihilo (Cosmos) | `0x0000000c687daed0fba60d1dba4e5f6149e8b894` | 0 | 256 |

The population values above are planning references from the Art Blocks
project metadata and must be re-read and bound to the exact Ethereum block in
the generated run manifest. The 923 EMPTY ROOMS title is not used to infer a
token count; the authoritative project response reports 924 max invocations.

## Authoritative source boundary

The acquisition script uses only:

1. Ethereum mainnet JSON-RPC `eth_blockNumber`, `eth_getBlockByNumber`, and
   `eth_call` for the configured population view (`projectTokenInfo(uint256)`
   or `projectStateData(uint256)`) and `tokenURI(uint256)`. Every call is made
   at the one captured block and raw JSON-RPC batch responses are retained
   content-addressed.
2. Art Blocks' own paginated `tokens_metadata` Hasura GraphQL endpoint, ordered
   by the server's `token_id: asc` clause, as the complete trait-population
   source. The server row order is preserved separately from the numeric
   canonical token/trait order. Every page's exact query, variables, order,
   count, response status, retry attempts, and raw response bytes are retained.
   A token is complete when it is present in this bulk source and its contract
   URI is resolved; per-token HTTP is not the sole completeness gate.
3. The exact URI returned by each contract `tokenURI` call for sampled raw
   token-metadata cross-checks. If that endpoint is rate-limited, the documented
   chain-qualified Art Blocks token endpoint is recorded as a separate fallback
   with separate bytes and attempts. Neither URI is silently substituted for
   the other. Generator URLs are retained as metadata fields, but generator
   source bytes are not silently represented as preserved by this package.

Art Blocks documents the token ID encoding and token/generator APIs in its
primary developer documentation. No marketplace trait, rarity, ranking, sale,
price, or floor field is requested, imported, cited, or preserved.

## Package layout

- `collection-sources.json` - immutable acquisition configuration and exact
  contract/project identities.
- `run-manifest.json` - generated observation block/time, paginated bulk-query
  hashes, completeness counts, every tokenURI batch, all 3,327 request records
  (including reconstructed request bytes, endpoint authorities, response refs,
  retry policy, attempt ordinals, and discarded-partial caveats), HTTP
  cross-check attempts, errors, and raw-file hashes.
- `snapshots/<slug>/snapshot.json` - full rarity-tool input plus source and
  ordering provenance. It preserves token source order separately from the
  canonical numeric token-and-trait ordering used for deterministic analysis.
- `raw/<slug>/` - content-addressed raw GraphQL, JSON-RPC, and cross-check
  bodies.
- `derived/provenance/` and `derived/request-bytes/` - content-addressed
  request and exclusion records reconstructed offline from preserved v2
  invocation data. They are explicitly not presented as contemporaneous
  request-byte captures; raw response bodies remain contemporaneous evidence.
- `package-manifest.json` - root fail-closed inventory binding every raw file,
  child manifest, snapshot, descriptor, configuration, fixture, script, and
  merged tool blob identity. The verifier enforces a closed path/role allowlist
  and rejects package-external substitutions even when replacement hashes are
  internally consistent. `latest-run.json` is a pointer and is excluded from
  the inventory to avoid a self-reference cycle.
- `pending-descriptors.json` - dependency and review ledger for the emitted
  descriptors; it remains `complete_pending_review` with reviewer fields null.
  It is not a quality claim or marketplace result.

## Attribute materialization boundary

The official bulk response exposes a structured `features` object. The object
is preserved as received, including scalar types and key order. For a future
NextGen-compatible statistical descriptor, the acquisition script materializes
one analysis row per feature key and converts scalar values to explicit text
using a pinned rule. Sampled tokenURI metadata cross-checks additionally parse
the source `traits[]` delimiter representation, but they do not replace the
bulk snapshot. This is a documented Museum input materialization choice, not an
artist-authored trait taxonomy and not a marketplace rarity metric.

Any missing bulk page, URI resolution, token identity, malformed feature,
population mismatch, or non-empty completeness error keeps a snapshot
incomplete. Nothing is silently omitted. Cross-check HTTP failures remain
visible as warnings and are not conflated with the complete bulk source.

## Acquisition

From the repository root:

```powershell
python scripts/acquire_casey_collection_snapshots.py `
  --config evidence/casey-reas-collection-snapshots/collection-sources.json `
  --output-dir evidence/casey-reas-collection-snapshots
```

The command exits non-zero if any bulk page, tokenURI resolution, population
count, token identity, or materialized feature row fails. Re-running creates a
new observed run manifest and preserves already content-addressed bytes; it
does not claim that two observations are the same snapshot.

## Dependency-gated descriptor stage

`scripts/emit_casey_collection_descriptors.py` refuses to run unless the
checked-out history contains the caller-supplied merged PR #4 commit and the
merged `scripts/rarity/analyze.py` is present at the current HEAD. It invokes
that exact merged tool on all five snapshots, emits one collection-level
descriptor per project, retains the full result artifact, and records separate
source/canonical orderings. The input is byte-identical to the hash-bound
snapshot; no local compatibility projection is used. Descriptors record stable
`source_snapshot_commit` and `acquisition_commit` inputs plus the exact PR #4
merge commit, Git blob, and SHA-256. They contain no mutable `current_head`.
Outputs remain labeled as transparent statistical descriptors of a frozen
metadata snapshot, never as quality, value, importance, or canonical truth.

The verifier recursively rejects marketplace/provider references, marketplace
URLs, and imported or precomputed metric fields across every bound JSON
artifact, including descriptor metadata, generated-result inputs, methods,
provenance, fixtures, and raw observations. The generated internal statistical
fields in the descriptor result are retained and independently recomputed by
the exact merged tool.

The package currently remains independent of the PR #7 safety-control merge.
Executable network fetching is not migrated in this draft; after PR #7 merges,
the approved HTTPS primitive/static guard must be adopted before a future
acquisition run.

The frozen Casey descriptor package was generated under CPython 3.12.10. Its
GitHub validation workflow pins that exact version, and the package verifier
fails closed before recomputation if the active implementation or version
differs. This package-level guard makes the recorded descriptor bytes and
result hashes reproducible rather than silently accepting a patch-runtime
variant.
