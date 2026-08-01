# 6529 NextGen rarity methodology: production archaeology

Status: research complete for the currently published production implementation.

Research date: 2026-08-01 UTC.

This note is the source-of-truth research record for reproducing the 6529 NextGen
rarity calculations in the Museum. It deliberately does not use OpenSea rarity,
OpenSea metadata, marketplace rankings, or any other third-party rarity service.

## Executive determination

The production method is implemented in `6529seize-backend`, in
`src/nextgen/nextgen_tokens.ts`. It is not implemented in the NextGen Solidity
repository, the NextGen generator, or the frontend. The frontend consumes and
displays backend-computed values.

The current production method is not one scalar called “rarity”. It produces:

- six trait-level measures;
- twelve token-level measures;
- trait ranks and token ranks for those measures;
- four user-facing combinations of the `Trait Normalization` toggle and the
  `Trait Count` toggle.

The two important interpretive conclusions for Museum use are:

1. These are distributional descriptors of metadata rows in a defined
   collection snapshot. They are not measures of artistic quality, historical
   importance, authorship, cultural significance, or curatorial judgment.
2. Exact reproduction requires a frozen source snapshot and the exact
   materialized trait rows. A later metadata refresh, duplicate attribute, or
   different database row order can change the persisted result even when the
   visible image appears unchanged.

## Source register

All source links below are pinned to immutable commit hashes. Line references
refer to those revisions.

| Source | Commit | Role in the method |
| --- | --- | --- |
| [6529seize-backend `nextgen_tokens.ts`](https://github.com/6529-Collections/6529seize-backend/blob/902557e9274f03b9851e97ef7ffac4b3c310b8a0/src/nextgen/nextgen_tokens.ts) | `902557e9274f03b9851e97ef7ffac4b3c310b8a0` | Production trait and token score computation, including ranks |
| [6529seize-backend trait-score tests](https://github.com/6529-Collections/6529seize-backend/blob/902557e9274f03b9851e97ef7ffac4b3c310b8a0/src/nextgen/nextgen-token-trait-scores.test.ts) | `902557e9274f03b9851e97ef7ffac4b3c310b8a0` | Verbatim pre-optimization reference pipeline and property tests |
| [6529seize-backend `INextGen.ts`](https://github.com/6529-Collections/6529seize-backend/blob/902557e9274f03b9851e97ef7ffac4b3c310b8a0/src/entities/INextGen.ts) | `902557e9274f03b9851e97ef7ffac4b3c310b8a0` | MySQL/TypeORM field names and numeric storage types |
| [6529seize-backend metadata ingestion](https://github.com/6529-Collections/6529seize-backend/blob/902557e9274f03b9851e97ef7ffac4b3c310b8a0/src/nextgen/nextgen_core_events.ts) | `902557e9274f03b9851e97ef7ffac4b3c310b8a0` | Converts `attributes[]` into persisted trait rows |
| [6529seize-backend API sorting](https://github.com/6529-Collections/6529seize-backend/blob/902557e9274f03b9851e97ef7ffac4b3c310b8a0/src/api-serverless/src/nextgen/nextgen.db-api.ts) | `902557e9274f03b9851e97ef7ffac4b3c310b8a0` | Selects rank columns and adds API tie-break ordering |
| [6529seize-frontend rarity display](https://github.com/6529-Collections/6529seize-frontend/blob/59119cb44621c17515e377e8c0faf7309318e591/components/nextGen/collections/nextgenToken/NextGenTokenProperties.tsx) | `59119cb44621c17515e377e8c0faf7309318e591` | Displays the backend fields and exposes the two toggles |
| [6529seize-frontend display test](https://github.com/6529-Collections/6529seize-frontend/blob/59119cb44621c17515e377e8c0faf7309318e591/__tests__/components/nextGen/NextGenTokenRarity.test.tsx) | `59119cb44621c17515e377e8c0faf7309318e591` | Tests display/toggle selection, not the formulas |
| [NextGen contracts](https://github.com/6529-Collections/nextgen/tree/73c09d1c07e405ddb9ccdd462283ab98ea68f903) | `73c09d1c07e405ddb9ccdd462283ab98ea68f903` | No rarity-score implementation found |
| [NextGen generator](https://github.com/6529-Collections/nextgen-generator/tree/cba39d65dfac192e4e82e06c237859b85e7fe268) | `cba39d65dfac192e4e82e06c237859b85e7fe268` | Generates/serves metadata and traits; no rarity-score implementation found |

The backend `main` ref was fetched from upstream on 2026-08-01 and resolved to
`902557e9274f03b9851e97ef7ffac4b3c310b8a0`. The optimization commit
`d34c98a23bb1cf8ade51f8a10e0534df3e666c99` states that it preserves the old
pipeline's content and order and adds a property test against the verbatim old
pipeline. The metric family was introduced by the historical “Reworked Rarity”
commit `912b6cd0f46ae461127332cd01cb081a39218f1b`.

The other local 6529 codebases inspected were `6529-core`, `6529mono`, and
multiple frontend worktrees. `6529-core` contains a duplicate frontend display
surface, not a second scoring implementation. No independent scoring algorithm
was found in `nextgen`, `nextgen-generator`, or the frontend codebases.

## Ingestion and collection scope

### Metadata-to-row materialization

The backend receives an NFT metadata `attributes` array and, for every element,
constructs one `NextGenTokenTrait` row with:

```text
token_id     = token id
collection_id = collection id
trait        = attribute.trait_type
value        = attribute.value
all score fields = -1
token_count  = 0
trait_count  = 0
```

This is visible in `nextgen_core_events.ts` lines 292-387 in the pinned source.
There is no trait-name trimming, Unicode normalization, case folding, value
normalization, sorting, or synthetic “None” insertion at this stage.

For on-demand generator metadata, `nextgen-generator` builds trait objects from
the generator's `traits` object by iterating its keys (lines 137-165 of
`src/pages/api/[network]/metadata/[token].ts` at commit
`cba39d65dfac192e4e82e06c237859b85e7fe268`). The returned values are runtime
data; the production backend's TypeScript type says strings, but there is no
general runtime validator in the trait materializer.

### Persisted key and duplicate behavior

`persistNextGenTraits` upserts on `['token_id', 'trait']` in
`nextgen.db.ts` lines 92-98. The entity declares `token_id` and `trait` as the
composite primary key in `INextGen.ts` lines 513-523.

Therefore, a production database cannot retain two distinct rows with the same
`(token_id, trait)` key. A source metadata array containing duplicate
`trait_type` values is not a valid one-to-one representation of the persisted
table. The exact winner of a same-batch duplicate upsert is database/statement
behavior, not an explicitly specified rarity rule and not covered by the
conformance tests. A reproducer must reject or explicitly quarantine duplicates
rather than silently choosing one.

### Collection snapshot

`refreshNextgenTokens` fetches all trait rows, filters them by
`collection_id`, and processes each collection (`nextgen_tokens.ts` lines 24-45).

For each collection:

- `tokenCount` is the number of distinct `token_id` values present in that
  collection's materialized trait rows (lines 50-60).
- `traitsCount` is the number of distinct trait names after excluding every
  trait whose lowercased name starts with `Mint Type` (lines 55-60).
- Trait name equality for counts is exact, case-sensitive JavaScript equality.
- Value equality for counts is exact, case-sensitive JavaScript equality.
- The `Mint Type` exclusion is a case-insensitive prefix test, not an exact
  equality test. `Mint Type`, `mint type`, and `Mint Type - Source` are all
  excluded from rarity scoring.

The token-level pass obtains the tokens for the collection and obtains their
trait rows by token id (`nextgen_tokens.ts` lines 137-200). This creates an
important reproducibility condition: a token with no trait rows is present in
the token-level pass but is absent from the trait-level `tokenCount` numerator.
The production implementation does not add a missing-trait row to repair that
difference.

## Trait-level calculation

For a collection snapshot, let:

- `N` = `tokenCount`, the distinct token id count in the trait rows;
- `C` = `traitsCount`, distinct non-`Mint Type` trait names;
- `v(t, x)` = number of materialized rows whose trait is `t` and value is `x`;
- `k(t)` = number of distinct values observed for trait `t`;
- `M` = `1,000,000`.

For every materialized trait row `(t, x)`, the backend writes:

| Production field | Exact formula | Directional meaning |
| --- | --- | --- |
| `token_count` | `N` | Snapshot context |
| `trait_count` | `k(t)` | Number of distinct observed values for this trait |
| `value_count` | `v(t, x)` | Number of rows with this exact trait/value pair |
| `statistical_rarity` | `v(t, x) / N` | Lower is less frequent |
| `single_trait_rarity_score_normalised` | `(v(t, x) / N) * k(t)` | Lower is less frequent after value-count scaling |
| `statistical_rarity_normalised` | `(v(t, x) / N) ** (1 / k(t))` | Lower is less frequent after geometric normalization |
| `rarity_score` | `N / v(t, x)` | Higher is less frequent |
| `rarity_score_normalised` | `((1 / v(t, x)) * M) / (C * k(t))` | Higher is less frequent |
| `rarity_score_trait_count_normalised` | `((1 / v(t, x)) * M) / ((C + 1) * k(t))` | Higher is less frequent with trait-count correction |

The formulas and assignments are `nextgen_tokens.ts` lines 76-113. There is no
rounding in this calculation.

### Mint Type rows

Rows whose trait name lowercases to a string beginning with `mint type` retain
their `token_count`, `trait_count`, and `value_count`, but all six score fields
are set to `-1` (lines 87-94). They are retained for metadata display and
counting, but they are excluded from collection trait count `C` and from the
token-level score pass.

### Trait ranks

`calulateTokenRanks` groups rows by exact trait name and calls
`calculateTokenRanksForCategory` for each category (lines 425-465). Every trait
rank field is assigned by sorting the category in descending numeric score,
regardless of whether a lower score is the rarer outcome. Thus:

- `rarity_score` and its normalized variants: high score gets rank 1;
- `statistical_rarity`, `statistical_rarity_normalised`, and
  `single_trait_rarity_score_normalised`: high score also gets rank 1 in the
  trait table, even though low score is the less frequent outcome.

Trait ranks are dense: equal values share the same rank and the next distinct
value increments the rank by one (`1, 1, 2`). The category order is first-seen
order, and the final persisted trait-row order is the result of the final
descending sort by `rarity_score_trait_count_normalised`, with stable equal-value
ordering inherited from the prior pass.

The six trait-level rank fields are:

```text
rarity_score_rank
rarity_score_normalised_rank
rarity_score_trait_count_normalised_rank
statistical_rarity_rank
statistical_rarity_normalised_rank
single_trait_rarity_score_normalised_rank
```

## Token-level calculation

The token pass excludes all rows whose trait name starts with `Mint Type`
(case-insensitive), but it does not exclude explicit `None` values from the
score reductions. `None` affects trait-count correction only.

For each token:

1. `filteredTokenTraits` is all non-`Mint Type` rows for that token.
2. Every trait category seen in those rows is added to `traitCategories`.
3. If a row's value lowercases to a string beginning with `none`, its trait
   category is also added to `traitCategoriesWithNone`.
4. `traitCount` is the number of distinct trait categories in the token after
   removing rows whose value starts with `none`.
5. `denominator` is the number of collection tokens whose `traitCount` equals
   this token's `traitCount`.

The category sets and `traitCount` logic are in `nextgen_tokens.ts` lines
181-206 of the pinned source. A missing attribute and an explicit value such as
`None`, `None Background`, or `none - not applicable` are not equivalent:

- a missing attribute creates no row, no category, and no explicit `None`;
- an explicit `None*` row participates in all score reductions but not in
  `traitCount`;
- a category is included in `traitCategoriesWithNone` if any token has an
  explicit `None*` row for it.

Let `r_i` be the trait-level fields for the rows on token `i`. The base token
measures are:

| Production field | Exact reduction |
| --- | --- |
| `rarity_score` | `sum(r_i.rarity_score)` |
| `rarity_score_normalised` | `sum(r_i.rarity_score_normalised)` |
| `rarity_score_trait_count_normalised` (before correction) | `sum(r_i.rarity_score_trait_count_normalised)` |
| `statistical_score` | `product(r_i.statistical_rarity)`, initialized to `1` |
| `statistical_score_normalised` | `product(r_i.statistical_rarity_normalised)`, initialized to `1` |
| `single_trait_rarity_score` | `min(r_i.statistical_rarity)`, or `0` if there are no rows |
| `single_trait_rarity_score_normalised` | `min(r_i.single_trait_rarity_score_normalised)`, or `0` if there are no rows |

The exact reducer is `nextgen_tokens.ts` lines 208-246.

The correction and trait-count variants are:

```text
rarity_score_trait_count
  = (number of fetched collection tokens / denominator) + rarity_score

rarity_score_trait_count_normalised
  = base rarity_score_trait_count_normalised
    + ((1 / denominator) * 1,000,000)
      / ((traitCategories.size + 1) * (traitCategoriesWithNone.size + 1))

statistical_score_trait_count
  = statistical_score * (denominator / number of fetched collection tokens)

statistical_score_trait_count_normalised
  = statistical_score_normalised
    * (denominator / number of fetched collection tokens)
      ** (1 / (traitCategoriesWithNone.size + 1))

single_trait_rarity_score_trait_count
  = min(single_trait_rarity_score,
        denominator / number of fetched collection tokens)

single_trait_rarity_score_trait_count_normalised
  = min(min(r_i.single_trait_rarity_score_normalised),
        (denominator / number of fetched collection tokens)
          * (traitCategoriesWithNone.size + 1))
```

The implementation is `nextgen_tokens.ts` lines 248-302. The spelling
`Normalised` and the local variable spelling `Adjustement` are part of the
production field/implementation history and should not be “cleaned up” in a
compatibility implementation.

The complete token-score entity has twelve doubles and twelve corresponding
rank fields in `INextGen.ts` lines 571-656:

```text
rarity_score
rarity_score_normalised
rarity_score_trait_count
rarity_score_trait_count_normalised
statistical_score
statistical_score_normalised
statistical_score_trait_count
statistical_score_trait_count_normalised
single_trait_rarity_score
single_trait_rarity_score_normalised
single_trait_rarity_score_trait_count
single_trait_rarity_score_trait_count_normalised
```

## Token ranks, direction, and tie behavior

`calculateRanks` is `nextgen_tokens.ts` lines 392-423.

- Default (`inverse = false`) sorts descending; high value receives rank 1.
- Inverse (`inverse = true`) sorts ascending; low value receives rank 1.
- Equal numeric values share a rank.
- Ranks are competition ranks, not dense ranks: for values `5, 5, 4`, ranks
  are `1, 1, 3`.
- There is no secondary key in the in-memory score sort. JavaScript's stable
  sort preserves the incoming order for equal values, but equal values receive
  the same rank.

The production direction is:

| Token rank family | Direction used by `calculateRanks` |
| --- | --- |
| `rarity_score*` | Descending, high score first |
| `statistical_score*` | Ascending, low score first |
| `single_trait_rarity_score*` | Ascending, low score first |

The backend persists all twelve rank fields in lines 305-390. The API selects
the rank column matching the two UI toggles, reverses the requested API sort
direction because lower rank is better, and adds `id asc` as its explicit
database tie-breaker (`nextgen.db-api.ts` lines 188-253). That API tie-breaker
is not part of the mathematical score or the in-memory rank algorithm, but it
is the correct stable order for a Museum result export that emulates API
presentation.

## Floating-point and serialization behavior

The backend computes with JavaScript `number` values in Node.js. Arithmetic,
division, exponentiation, `Math.min`, and comparisons therefore use IEEE-754
binary64 behavior. There is no explicit decimal rounding or epsilon comparison.
The entity stores score fields as MySQL/TypeORM `double` columns and ranks as
integer columns (`INextGen.ts` lines 525-569 and 585-655).

Implications for exact reproduction:

- preserve binary64 operations and operation order;
- do not round intermediate values;
- compare ties by exact numeric equality, not a tolerance;
- serialize full numeric precision in the result artifact;
- format for display only at the final presentation layer.

The frontend's `displayScore` helper deliberately formats for humans with three
decimal places or scientific notation (`NextGenTokenProperties.tsx` lines
21-35). That display formatting is not the production calculation and must not
be used as an input to a rerun.

The implementation has no explicit handling for `NaN`, `Infinity`, zero value
counts, non-string trait values, or malformed metadata. A Museum CLI should
fail closed on those inputs while documenting that this is an input-validation
boundary added by the Museum, not an internal NextGen scoring rule.

## Tests and confidence assessment

The authoritative backend test is
`src/nextgen/nextgen-token-trait-scores.test.ts` at commit
`902557e9274f03b9851e97ef7ffac4b3c310b8a0`.

The test's reference pipeline is deliberately the pre-optimization algorithm:

- it recomputes `tokenCount`, `traitsCount`, exact trait/value counts, and all
  trait metrics (lines 60-110);
- it reproduces the six trait-rank passes (lines 113-161);
- it generates arbitrary rows over Background, Palette, Mint Type, and Size,
  with values including `None Big` (lines 164-171);
- it runs 40 fast-check property cases and asserts persisted rows are deeply
  equal in both content and order to the optimized production pipeline (lines
  189-212);
- it asserts Mint Type rows retain counts but have `-1` rarity scores, while a
  normal trait is scored (lines 214-246).

This is strong evidence that the July 2026 performance refactor preserved the
historical production method. It is not a full mathematical specification:
there are no tests for duplicate `(token_id, trait)` inputs, absent attributes,
non-string values, malformed metadata, zero-row collections, explicit per-token
None variants, or cross-runtime floating-point serialization.

The frontend test at
`6529seize-frontend` commit `59119cb44621c17515e377e8c0faf7309318e591`
only confirms that the default toggle selects the normalized + trait-count
fields and that toggling `Trait Count` selects the normalized non-trait-count
fields. It does not independently verify formulas.

## Trait rarity versus Museum significance

The frontend itself warns users that rarity “does not necessarily correlate
with aesthetic quality or the value of generative art” (`NextGenTokenProperties.tsx`
lines 282-290). The Museum should make the separation explicit:

| Evidence layer | Question answered | Admissible use |
| --- | --- | --- |
| NextGen-compatible trait rarity | How distributed were the declared metadata values in this frozen snapshot? | Technical description, reproducible quantitative appendix, collection browsing |
| Generative-system evidence | How was the work generated, by which code, seed, hash, parameters, and runtime? | Provenance and conservation |
| Artist/issuer evidence | What did the artist or issuer intend, and how do they describe the system? | Authorship, intent, interpretation |
| Curatorial analysis | Why does this work matter in the artist's and the field's history? | Accession statement, catalogue essay, exhibition interpretation |
| Conservation/condition evidence | What can be displayed and preserved, under what conditions? | Stewardship and access |

Rarity must never be used as a proxy for aesthetic excellence, historical
importance, artist approval, accession priority, value, or insurance value. A
rare trait can be visually unimportant; a common trait can be central to an
artist's grammar. A Museum record should carry rarity as a technical analysis
with its method/version/snapshot hash, separate from curatorial significance.

## Proposed transparent reusable CLI

The reusable Museum tool should be a small, dependency-light CLI named
`museum-nextgen-rarity` (working name) with a versioned method identifier:

```text
method_id = 6529-nextgen-production-v1
source_algorithm_commit = 902557e9274f03b9851e97ef7ffac4b3c310b8a0
```

The implementation should use JavaScript/TypeScript or another runtime with
explicit binary64 semantics. It should keep the formulas in a directly
reviewable module and include the fixture below as a golden test. It must not
call OpenSea, infer traits from OpenSea, or import marketplace rarity values.

### CLI contract

Suggested commands:

```text
museum-nextgen-rarity compute \
  --input collection-snapshot.json \
  --method 6529-nextgen-production-v1 \
  --output rarity-result.json

museum-nextgen-rarity verify \
  --input collection-snapshot.json \
  --expected rarity-result.json

museum-nextgen-rarity explain \
  --result rarity-result.json \
  --token-id 2
```

Required input properties:

```text
schema_version
collection_id
collection_name (optional display context)
snapshot_observed_at
source_algorithm_commit
tokens[]
tokens[].token_id
tokens[].attributes[]
tokens[].attributes[].trait_type
tokens[].attributes[].value
```

The input reader should:

1. preserve the raw attribute strings and source order;
2. reject non-string `trait_type` and `value` in strict Museum mode;
3. reject duplicate `(token_id, trait_type)` keys rather than guessing which
   database upsert would win;
4. preserve missing attributes as missing and never synthesize `None`;
5. apply only the internal case-insensitive `Mint Type*` and `None*` prefix
   tests;
6. emit a source digest over the canonical raw input;
7. record the method commit, runtime version, and generated-at timestamp;
8. compute using full binary64 precision and no intermediate rounding.

For a byte-for-byte compatibility mode, the CLI may also accept a
`materialized_trait_rows[]` input that represents the already persisted
`NextGenTokenTrait` rows. This is the preferred mode for historical accession
work because it removes ambiguity from metadata refresh, duplicate upsert, and
database ordering behavior.

### Result format

The result should be a public, self-contained JSON artifact with a structure
like this:

```json
{
  "schema_version": "6529nm.nextgen-rarity-result.v1",
  "method_id": "6529-nextgen-production-v1",
  "source_algorithm_commit": "902557e9274f03b9851e97ef7ffac4b3c310b8a0",
  "source_snapshot": {
    "observed_at": "2026-08-01T00:00:00Z",
    "input_sha256": "sha256:<computed-over-canonical-input>",
    "collection_id": 1,
    "token_count_in_input": 4,
    "trait_row_count": 15,
    "traits_count": 3,
    "trait_categories": ["Background", "Palette", "Size"],
    "trait_categories_with_none": ["Size"]
  },
  "trait_rows": [],
  "token_scores": [],
  "warnings": [],
  "curatorial_significance": null
}
```

Each `trait_rows[]` entry should use the production field names, retain the raw
trait/value, and include all six scores, six ranks, `token_count`,
`trait_count`, and `value_count`. Each `token_scores[]` entry should use the
production twelve score field names and twelve rank field names. No displayed
rounded score should be stored in place of the full numeric value.

The result should also include a canonical sorted view by `token_id` for stable
Museum manifests. If an artifact claims to reproduce the internal persisted
row order, it must retain the raw source order and report that order separately;
canonical Museum ordering is a reproducibility convenience, not a new internal
rarity rule.

### Conformance modes

The tool should expose two clearly labeled modes:

- `production-compat`: reproduce the formulas and field semantics exactly on a
  validated, already materialized snapshot; fail if duplicate keys, non-string
  values, or missing required snapshot facts make exact reproduction uncertain.
- `museum-strict`: perform the same calculation but additionally emit explicit
  validation warnings for missing attributes, explicit `None*` values,
  metadata changes, absent generator/source hashes, and incomplete collection
  membership. It must not silently alter the production math.

Any future change to formulas, prefix rules, rank semantics, float behavior, or
input normalization must create a new method id, fixture, and result schema
version. It must never overwrite the meaning of `6529-nextgen-production-v1`.

## Proposed conformance fixture

This fixture intentionally covers:

- repeated and rare values;
- an explicit `None Small` value;
- a missing `Size` attribute;
- a `Mint Type` row that is counted but excluded from rarity;
- competition ties.

### Frozen input

```json
{
  "schema_version": "6529nm.nextgen-rarity-input.v1",
  "collection_id": 1,
  "snapshot_observed_at": "2026-08-01T00:00:00Z",
  "source_algorithm_commit": "902557e9274f03b9851e97ef7ffac4b3c310b8a0",
  "tokens": [
    {
      "token_id": 1,
      "attributes": [
        {"trait_type": "Background", "value": "Red"},
        {"trait_type": "Palette", "value": "Cool"},
        {"trait_type": "Mint Type", "value": "Public"},
        {"trait_type": "Size", "value": "Large"}
      ]
    },
    {
      "token_id": 2,
      "attributes": [
        {"trait_type": "Background", "value": "Red"},
        {"trait_type": "Palette", "value": "Warm"},
        {"trait_type": "Mint Type", "value": "Airdrop"},
        {"trait_type": "Size", "value": "None Small"}
      ]
    },
    {
      "token_id": 3,
      "attributes": [
        {"trait_type": "Background", "value": "Blue"},
        {"trait_type": "Palette", "value": "Cool"},
        {"trait_type": "Mint Type", "value": "Public"},
        {"trait_type": "Size", "value": "Large"}
      ]
    },
    {
      "token_id": 4,
      "attributes": [
        {"trait_type": "Background", "value": "Blue"},
        {"trait_type": "Palette", "value": "Warm"},
        {"trait_type": "Mint Type", "value": "Public"}
      ]
    }
  ]
}
```

The expected collection constants are:

```text
N = 4
C = 3
traitCategories = {Background, Palette, Size}
traitCategoriesWithNone = {Size}
trait counts by token id = {1: 3, 2: 2, 3: 3, 4: 2}
denominator for every token = 2
```

For a normal trait/value pair with `v=2` and `k=2`, the exact JavaScript
binary64 values are:

```text
statistical_rarity                         0.5
single_trait_rarity_score_normalised       1
statistical_rarity_normalised              0.7071067811865476
rarity_score                               2
rarity_score_normalised                    83333.33333333333
rarity_score_trait_count_normalised        62500
```

For `Size = None Small`, where `v=1` and `k=2`, they are:

```text
statistical_rarity                         0.25
single_trait_rarity_score_normalised       0.5
statistical_rarity_normalised              0.5
rarity_score                               4
rarity_score_normalised                    166666.66666666666
rarity_score_trait_count_normalised        125000
```

All `Mint Type` rows have `trait_count = 2`, `value_count` of `3` for Public
or `1` for Airdrop, and all six trait score fields equal to `-1`.

### Expected token scores

The following table uses production field names. Values are full-precision
JavaScript results; do not round them before comparison.

| token_id | `rarity_score` | `rarity_score_normalised` | `rarity_score_trait_count` | `rarity_score_trait_count_normalised` | `statistical_score` | `statistical_score_normalised` |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 6 | 250000 | 8 | 250000 | 0.125 | 0.35355339059327384 |
| 2 | 8 | 333333.3333333333 | 10 | 312500 | 0.0625 | 0.25000000000000006 |
| 3 | 6 | 250000 | 8 | 250000 | 0.125 | 0.35355339059327384 |
| 4 | 4 | 166666.66666666666 | 6 | 187500 | 0.25 | 0.5000000000000001 |

| token_id | `statistical_score_trait_count` | `statistical_score_trait_count_normalised` | `single_trait_rarity_score` | `single_trait_rarity_score_normalised` | `single_trait_rarity_score_trait_count` | `single_trait_rarity_score_trait_count_normalised` |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.0625 | 0.25000000000000006 | 0.5 | 1 | 0.5 | 1 |
| 2 | 0.03125 | 0.17677669529663692 | 0.25 | 0.5 | 0.25 | 0.5 |
| 3 | 0.0625 | 0.25000000000000006 | 0.5 | 1 | 0.5 | 1 |
| 4 | 0.125 | 0.35355339059327384 | 0.5 | 1 | 0.5 | 1 |

The expected token rank vector, in token id order `[1, 2, 3, 4]`, is:

| Rank field family | Expected ranks |
| --- | --- |
| `rarity_score_rank` | `[2, 1, 2, 4]` |
| `rarity_score_normalised_rank` | `[2, 1, 2, 4]` |
| `rarity_score_trait_count_rank` | `[2, 1, 2, 4]` |
| `rarity_score_trait_count_normalised_rank` | `[2, 1, 2, 4]` |
| `statistical_score_rank` | `[2, 1, 2, 4]` |
| `statistical_score_normalised_rank` | `[2, 1, 2, 4]` |
| `statistical_score_trait_count_rank` | `[2, 1, 2, 4]` |
| `statistical_score_trait_count_normalised_rank` | `[2, 1, 2, 4]` |
| `single_trait_rarity_score_rank` | `[2, 1, 2, 2]` |
| `single_trait_rarity_score_normalised_rank` | `[2, 1, 2, 2]` |
| `single_trait_rarity_score_trait_count_rank` | `[2, 1, 2, 2]` |
| `single_trait_rarity_score_trait_count_normalised_rank` | `[2, 1, 2, 2]` |

In this fixture, the final trait-row category order is the first-seen order
`Background`, `Palette`, `Mint Type`, `Size`. Within the category, the final
sort is descending `rarity_score_trait_count_normalised`, with stable order on
equal values. A conformance test should compare both the field values and this
order when it is testing production persisted-row compatibility.

## What cannot be reproduced without source metadata

The formulas alone are insufficient. A historical result cannot be claimed as
exact unless the accession record preserves:

- the collection id and authoritative token membership at observation time;
- each token's raw metadata response or a cryptographically committed copy;
- the exact `attributes[]` array, including trait/value spelling, case,
  Unicode, order, and explicit `None*` values;
- the separate on-chain token-data-derived `Mint Type` rows, when present;
- the metadata fetch and refresh timestamps;
- the materialized trait-row snapshot used for scoring;
- the algorithm commit and runtime version;
- the result artifact with full-precision doubles and source digest;
- whether the result was calculated before or after any metadata update;
- any duplicate trait_type rejection or database-upsert event.

Absent those facts, the Museum can produce a new transparent analysis, but it
must label it “recomputed from surviving metadata” rather than “the production
NextGen rarity result at mint/refresh time”.

The following are not valid substitutes for the missing source snapshot:

- OpenSea rarity or any marketplace rarity score;
- a current token page after metadata has changed;
- a rendered image alone;
- a manually reconstructed trait list with normalized labels;
- a rank copied from a third-party indexer;
- a claim that a collection is generative without a source/code/provenance
  record.

## Museum adoption recommendation

Adopt `6529-nextgen-production-v1` as a technical-analysis method only. For any
accessioned generative collection, publish alongside the accession record:

1. the raw metadata/source manifest;
2. the materialized attribute snapshot;
3. the algorithm commit and method id;
4. the open CLI source and golden fixture version;
5. the full result artifact and SHA-256 digest;
6. a short interpretation explaining that distributional rarity is not
   curatorial significance;
7. an independent constructor/reviewer record that confirms the snapshot,
   formula, source hashes, and absence of OpenSea data.

The Museum's curatorial catalogue should quote the result only as a bounded
technical observation, for example: “Within the accession's frozen metadata
snapshot, this value occurred in 1 of 4 materialized token rows under
`6529-nextgen-production-v1`.” It should not say that the work is important,
valuable, or aesthetically superior because it is rare.
