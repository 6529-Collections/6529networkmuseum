# Generative trait analysis

Status: working standard for transparent Museum analysis; not an adopted curatorial policy.

This document defines the Museum's reproducible compatibility implementation
of the internal 6529 NextGen trait-prevalence analysis. It is descriptive
technical evidence only. Trait rarity is not quality, artistic merit, market
value, desirability, or curatorial significance. A rare trait may occur in an
artistically unimportant work, and a common trait may occur in an important
work. Rarity must never substitute for artist, provenance, rights, condition,
technical, historical, or curatorial review.

Precomputed rarity/score/rank/metric fields are prohibited as Museum evidence
and rejected by this tooling, including fields claimed to come from OpenSea,
LooksRare, equivalent providers, or internal Museum/NextGen sources.
Provenance prose, citations, and URLs that mention a marketplace remain
admissible; they are evidence of provenance or source context, not rarity
inputs.

## Pinned sources

The implementation is based on the current authoritative 6529 backend source
observed 2026-08-01 UTC:

- [`nextgen_tokens.ts`](https://github.com/6529-Collections/6529seize-backend/blob/902557e9274f03b9851e97ef7ffac4b3c310b8a0/src/nextgen/nextgen_tokens.ts), commit `902557e9274f03b9851e97ef7ffac4b3c310b8a0`.
- [`nextgen_constants.ts`](https://github.com/6529-Collections/6529seize-backend/blob/902557e9274f03b9851e97ef7ffac4b3c310b8a0/src/nextgen/nextgen_constants.ts), which defines `MINT_TYPE_TRAIT = "Mint Type"`.
- [`NextGen`](https://github.com/6529-Collections/nextgen/tree/73c09d1c07e405ddb9ccdd462283ab98ea68f903/hardhat/smart-contracts), commit `73c09d1c07e405ddb9ccdd462283ab98ea68f903`, inspected as the contract source repository.

The Museum port is [`scripts/rarity/nextgen_compat.py`](../scripts/rarity/nextgen_compat.py).
The exact conformance input and complete expected output are
[`nextgen-compatibility.json`](../tests/rarity/fixtures/nextgen-compatibility.json)
and
[`nextgen-compatibility.expected.json`](../tests/rarity/fixtures/nextgen-compatibility.expected.json).

## Input snapshots

An input snapshot is a dated JSON object with:

- `snapshot_id`, `observed_at`, and `source` provenance;
- `collection` identity;
- `tokens`, the declared token universe as `{ "id", "collection_id" }` rows;
- `traits`, the raw metadata rows as `{ "token_id", "collection_id", "trait", "value" }`.

The snapshot is the evidence boundary. The tool does not fetch metadata,
render tokens, query a marketplace, or fill gaps from an external service.
Keep the raw snapshot with the generated analysis. A snapshot is not an
accession record and does not establish title, custody, authenticity, rights,
or curatorial importance.

Run the CLI with:

```powershell
python scripts/rarity/analyze.py path\to\snapshot.json --output analysis.json
```

The output exposes the raw snapshot, deterministically normalized snapshot,
quality observations, configuration, per-trait rows, per-token scores/ranks,
and hashes. It retains `Mint Type` rows in the audit/per-trait output while
excluding them from score aggregates, matching the backend.

The input guard rejects every structured precomputed rarity, score, rank, or
metric field at any depth, regardless of whether it claims to come from
OpenSea, LooksRare, the Museum, NextGen, or another provider. Provider claims
and wrapper URLs do not make an imported score trustworthy. Internal
NextGen-compatible scores are computed by this tool and appear only in its
output. Free-text notes, provenance descriptions, citation labels, and
citation URLs that mention marketplaces remain admissible. Exact provenance or
methodology citation objects such as `rarity_provenance` are admissible only
when they contain no structured precomputed metric fields; their text and URLs
are never treated as score inputs. Citation objects use a closed recursive
schema of URL/URI, source URI, method/methodology, version, observation time,
hash/digest, note/citation, source, and descriptive label fields. Only mapping
keys are inspected for metric semantics; raw artist trait names and values are
not scanned for words such as `Rarity` or `Score`.

## Normalization and data quality

Normalization produces a canonical presentation with token rows sorted by
token ID and trait rows sorted by token ID, trait, and value. It does not
invent rows or change case, whitespace, values, or trait names. Compatibility
calculations retain the effective source row order, including source token
order and raw/preserve-mode trait order; the sorted view is exposed separately
as `input.normalized_snapshot`. Values whose lowercase text starts with `none`
are recognized only for the source's `trait_count` adjustment; they remain in
the score products.

The tool reports:

- declared token count and observed token count;
- tokens with no trait rows;
- each observed trait's missing declared token IDs;
- duplicate token/trait rows and orphan rows;
- the selected duplicate policy.

Duplicate `(token_id, trait)` rows are rejected by default because the backend
trait entity uses that pair as its database key. `--duplicates preserve`
retains duplicates and reproduces raw-row counting, including their effect on
`value_count` and aggregates. `--duplicates deduplicate` is an explicit
preprocessing choice that keeps the lexicographically smallest value for each
pair; it is not exact compatibility. Missing rows are always preserved. The
tool never synthesizes a `None` value for a missing trait. Orphan rows are
rejected by default; explicit forensic modes retain them for per-trait audit
and raw prevalence counts, while declared-token aggregates still only process
the declared token universe.

## Exact score algorithm

Let `N` be the number of distinct `token_id` values in the effective trait
rows. This is the denominator used by the backend's per-trait calculations,
not necessarily the declared token count. For trait category `c` and value
`v`, let `n(c,v)` be the effective raw-row count and `V(c)` the number of
distinct values in that category. Let `C` be the number of observed trait
categories whose name does not start, case-insensitively, with `Mint Type`.

For non-`Mint Type` rows, the backend calculates:

```text
statistical_rarity                  = n(c,v) / N
single_trait_rarity_score_normalised = statistical_rarity * V(c)
statistical_rarity_normalised        = statistical_rarity ** (1 / V(c))
rarity_score                         = N / n(c,v)
rarity_score_normalised              = ((1 / n(c,v)) * 1,000,000) / (C * V(c))
rarity_score_trait_count_normalised  = ((1 / n(c,v)) * 1,000,000) / ((C + 1) * V(c))
```

For a `Mint Type` row, each of those six per-trait score fields is `-1`.
`trait_count` is `V(c)` and `value_count` is `n(c,v)` for every row, including
`Mint Type` rows. Per-trait ranks are assigned independently within each trait
category, in descending score order, with dense ranks: equal values share a
rank and the next distinct value receives the next integer (`1, 1, 2`).

For each declared token, exclude `Mint Type` rows from the following token
calculation. Let:

- `T` be the declared token count;
- `k(t)` be the number of distinct non-`None` trait categories on token `t`;
- `d(t)` be the number of declared tokens with the same `k(t)`;
- `A` be the observed non-`Mint Type` trait categories on declared tokens;
- `A_none` be the categories with at least one explicit `None`-prefixed value.

Every arithmetic sum above is evaluated as an explicit left-to-right fold,
matching JavaScript `reduce((total, value) => total + value, 0)`. Python's
built-in `sum()` is not used because its optimized CPython implementation can
produce a different last bit for adversarial input order. The pinned fixture
and regression test include an independent reference fold for this boundary.

The backend calculates:

```text
rarity_score                         = sum(per-trait rarity_score)
rarity_score_normalised              = sum(per-trait rarity_score_normalised)
rarity_score_trait_count             = T / d(t) + rarity_score
rarity_score_trait_count_normalised  =
  sum(per-trait rarity_score_trait_count_normalised)
  + ((1 / d(t)) * 1,000,000) / ((|A| + 1) * (|A_none| + 1))

statistical_score                    = product(per-trait statistical_rarity)
statistical_score_normalised         = product(per-trait statistical_rarity_normalised)
statistical_score_trait_count        = statistical_score * (d(t) / T)
statistical_score_trait_count_normalised =
  statistical_score_normalised * (d(t) / T) ** (1 / (|A_none| + 1))

single_trait_rarity_score            = min(per-trait statistical_rarity), or 0 if empty
single_trait_rarity_score_normalised =
  min(per-trait single_trait_rarity_score_normalised), or 0 if empty
single_trait_rarity_score_trait_count = min(single_trait_rarity_score, d(t) / T)
single_trait_rarity_score_trait_count_normalised = min(
  min(per-trait single_trait_rarity_score_normalised),
  (d(t) / T) * (|A_none| + 1)
)
```

If the snapshot has only `Mint Type` traits, the default
`production-compatibility` mode still emits each Mint Type row with `-1` and
scores each declared token using the backend's empty non-Mint list behavior.
In particular, the token score products are `1`, the additive rarity sums are
`0`, and the trait-count adjustment remains active. This is compatibility
behavior, not a claim that a Mint Type-only collection has useful descriptive
rarity.

The last `min` intentionally matches JavaScript `Math.min(...[])` behavior:
an empty per-trait list contributes positive infinity to that intermediate
expression, so the finite trait-count term wins. Empty or malformed source
denominators are rejected rather than hidden behind a fallback.

Token rarity ranks are descending. Statistical and single-trait ranks are
ascending because lower prevalence is the rarer result. Token ranks use the
backend's stable sort and competition ranks: ties share a rank and leave gaps
(`1, 1, 3`). Trait ranks use the separate dense-rank behavior above. No
secondary artist, token, wallet, market, or OpenSea tie-breaker is introduced.

## Deterministic hashes

The tool uses compact UTF-8 JSON with recursively sorted object keys and
preserved array order. It emits:

- `input_snapshot_sha256`: the canonical hash of the raw supplied snapshot;
- `normalized_snapshot_sha256`: the canonical hash after explicit
  normalization/duplicate handling;
- `output_sha256`: the canonical hash of the output payload while its `hashes`
  object is empty and its runtime-only `determinism` profile is omitted (the
  emitted hashes and environment description are not self-hashed data).

All are rendered as `sha256:<64 lowercase hex digits>`. Repeat runs over the
same snapshot and duplicate policy must produce identical JSON and hashes.
The output's `determinism` profile records the active Python implementation,
version, JSON encoder settings, and float boundary. JSON parsing rejects
`NaN`, `Infinity`, and `-Infinity`, and canonical encoding rejects any
non-finite value. This implementation's
output commitment deliberately excludes that runtime profile so the exact
fixture is not pinned to the maintainer's CPython patch version. The
byte/hash guarantee for the numeric payload is still intentionally limited to
the same CPython implementation and version: CPython's shortest-round-trip
float encoding is part of the commitment. A Python implementation/version
change requires review and fixture regeneration; this compact encoder is not a
claim of RFC 8785 cross-runtime compatibility.

## CLI exit semantics

Argument-parser misuse (missing required arguments, unknown flags, or invalid
choice values) exits with `2`, as required by `argparse`. A readable but
invalid snapshot, rejected duplicate/orphan policy, prohibited metric field,
non-finite JSON constant, input file/JSON error, or output-path failure exits
with `1` and a concise `error:` message without a traceback. A successful
analysis exits with `0`.

## Tests and review boundary

Run the focused suite with:

```powershell
python -m unittest discover -s tests/rarity -p 'test_*.py' -v
```

The fixture tests cover exact score values, explicit missing traits, `None`
handling, `Mint Type` exclusion, duplicate error/preserve/deduplicate modes,
per-trait dense ranks, token competition ranks, and repeatable hashes. They
also cover source-order versus canonical presentation, OpenSea/LooksRare and
generic third-party provenance versus metric fields, the defensive empty-rank
guard, preserve-mode products, the empty-token `Math.min(...[])` parity path,
Mint Type-only scoring, non-finite JSON and output failures, CLI exit codes,
the independent JavaScript-style left fold, and the CPython float boundary.

This analysis is an evidence aid only. It must remain separate from the
Museum accession register, object identity, rights, provenance, preservation,
and curatorial statements.

## Open questions

The current source does not publish a standalone serialized snapshot schema
or a formal versioned rarity specification. The Museum therefore pins the
backend commit and keeps conformance fixtures in-repository. If 6529 changes
the source formulas, excluded-trait rule, database key, or rank implementation,
publish a new algorithm ID and fixture rather than silently changing historic
outputs. See the dated research note
[`2026-08-01-nextgen-rarity-analysis.md`](../notes/wip/2026-08-01-nextgen-rarity-analysis.md)
for the retained implementation questions.
