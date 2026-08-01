# NextGen rarity analysis research note — 2026-08-01

Status: WIP research retained for review; the implementation is documented as
a working standard in [`docs/generative-trait-analysis.md`](../../docs/generative-trait-analysis.md).

## Findings

- `D:\repos\nextgen` is the 6529-Collections NextGen contract repository at
  local commit `73c09d1c07e405ddb9ccdd462283ab98ea68f903`.
- The exact internal prevalence and rarity calculations are in
  `D:\repos\6529seize-backend\src\nextgen\nextgen_tokens.ts`, matching
  authoritative backend commit `902557e9274f03b9851e97ef7ffac4b3c310b8a0`.
- `MINT_TYPE_TRAIT` is `Mint Type`; its rows remain auditable but receive `-1`
  per-trait scores and are omitted from token score aggregation.
- The implementation has different denominators: distinct token IDs observed
  in trait rows for per-trait prevalence, and declared token rows for token
  scores and trait-count adjustments.
- Missing trait rows are not synthesized. Raw duplicate rows are not silently
  corrected. Per-trait ranks are dense and descending; token ranks are stable
  competition ranks, with rarity descending and statistical/single-trait
  families ascending.
- OpenSea-sourced or computed rarity metric fields are outside the Museum
  analysis boundary; provenance prose, citations, and URLs mentioning OpenSea
  remain admissible and are not used as score inputs.
- Trait rarity is descriptive prevalence, not quality or curatorial
  significance.
- Hash determinism is explicitly bounded to the same CPython implementation
  and version because canonical JSON uses CPython's shortest-round-trip float
  encoding; fixture regeneration and review are required after a runtime
  change.

## Implementation status

- Reusable module and CLI: `scripts/rarity/`.
- Exact input/output conformance fixture: `tests/rarity/fixtures/`.
- Focused tests: `tests/rarity/test_nextgen_compat.py`.
- User-facing standard: `docs/generative-trait-analysis.md`.

## Unresolved questions

1. 6529 has not published a standalone versioned rarity schema or an explicit
   promise that backend `main` is a stable public algorithm contract. The
   Museum must pin commits and mint a new algorithm ID/fixture whenever source
   behavior changes.
2. Real production snapshots still need a source-specific capture protocol
   that records the exact API/database extraction, pagination, and retrieval
   time. This tooling intentionally does not invent that operational capture.
3. A future Museum policy may decide whether to accept `preserve` mode for
   forensic comparisons or require `deduplicate`/manual review before
   publication. The default remains rejection of duplicate `(token_id, trait)`
   rows.
4. The repository currently does not pin a Python runtime in a project-level
   manifest. Until it does, the fixture's recorded CPython version is the
   determinism boundary and must be checked by the focused tests.
