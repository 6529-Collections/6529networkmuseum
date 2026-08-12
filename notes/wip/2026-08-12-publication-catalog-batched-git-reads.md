# Publication/catalog batched Git-read process

Status: active future-process engineering work; not a Museum content,
accession, or frontend publication change.

## Mandate

Replace publication/catalog verification's per-file Git subprocess pattern for
future releases. Preserve exact-tree, byte-identical, fail-closed behavior and
cross-platform determinism. This work is independent of the active art-first
production release and must not hold that release.

## Finding and benchmark

The former `scripts/publication_catalog.py` path called `ls-tree` and
`cat-file blob` repeatedly while checking the manifest, inventory, bundle, A/B
review promotion, and catalog entries. On this Windows host, one small fixture
catalog build measured:

| implementation | wall time | Git subprocesses | `cat-file --batch` | `cat-file blob` |
|---|---:|---:|---:|---:|
| pre-change per-file reader | 25.640 s | 863 | 0 | repeated per file |
| batched reader | 0.938 s | 23 | 4 | 0 |

The baseline was measured before the implementation with the existing
`PublicationCatalogTests.test_catalog_binds_exact_git_objects_and_pointer`
fixture and a direct `build_catalog()` call; the optimized measurement used
the same fixture, commit, and call. The fixture is intentionally small; the
observed process-count reduction is the relevant Windows scaling signal behind
the previously reported approximately 41-minute large-release run.

## Implemented control

`GitTreeReader` now indexes one full commit tree with a NUL-delimited
`git ls-tree -r --full-tree` read. It validates the exact requested path,
ordinary-file mode, object type, and object ID. It then sorts and de-duplicates
the validated blob IDs and reads them through `git cat-file --batch` in
deterministic batches of at most 256 objects. The parser consumes the declared
byte length and required separator for every response. It rejects missing,
wrong-type, reordered, malformed, truncated, duplicated, and trailing data.

The reader is cached only by repository root and full commit ID during the
current process. Manifest/inventory/bundle/review checks share those exact
bytes. Text uses the existing LF-normalized domain; binary evidence remains
raw; JSON still receives the existing JCS/Keccak commitment. Activation pointer
and immutable catalog worktree checks still compare raw bytes directly against
the retained Git object. There is no per-file fallback.

The contract is documented in `docs/control-plane.md`. Tests cover direct
byte-identical comparison against Git, repeated cached reads, bounded batch
usage with no `cat-file blob` calls, missing paths, missing objects, malformed
headers, wrong object types, truncation, invalid sizes, and unexpected trailing
bytes.

## Current state and unresolved work

- Implementation and focused tests are complete locally.
- The release manifest was regenerated after the control-plane source,
  documentation, tests, INDEX, and this note settled; `generate_manifest.py
  --check` is green.
- Full local discovery is green on the cache-fix head: 331 tests, one skipped,
  in 458.866 seconds.
- Commit `0e63c74` is published as ready PR #57 on
  `codex/publication-catalog-batched-git-reads-v2`; the six required
  Ubuntu/Windows GitHub jobs are green, the addressed CodeRabbit thread is
  resolved/outdated, and the maintainer team was requested for review.
- CodeRabbit completed its review with one actionable memory-retention finding
  on the prior head:
  the reader cache is now bounded to two commit readers, exposes an explicit
  `clear_cached_git_tree_readers()` release helper, and the catalog CLI invokes
  it in `finally`; the new focused suite is 42 tests, OK. A fresh bot
  re-review was rate-limited after the fix; maintainer approval remains open.
- No Museum records, evidence, media, or frontend presentation files are in
  scope; any release-manifest change is a control-plane commitment only.
- The PR must not be merged until the exact final head is independently
  reviewed, all threads are resolved, and required CI is green.

### Final PR checkpoint — 2026-08-12

- Final head `31d6f3c2c246bf5786df6132a074a6c2b3f1cb08` passed all six required
  jobs in GitHub Actions run `31602796374`, including deterministic Windows.
- The CodeRabbit cache-retention finding was fixed in `0e63c74`; its thread is
  resolved and outdated. Fresh CodeRabbit re-review requests were externally
  rate-limited, so that bot result does not substitute for maintainer review.
- The `6529seize-maintainers` team remains requested, with no approval recorded
  yet. PR #57 therefore remains intentionally unmerged pending the required
  exact-head review gate.

## Reproduction commands

From the repository root:

```powershell
python -m unittest tests.test_stream_adapter_and_publication_catalog.PublicationCatalogTests.test_catalog_binds_exact_git_objects_and_pointer -q
python -m unittest tests.test_stream_adapter_and_publication_catalog.PublicationCatalogTests.test_batched_tree_reader_is_byte_identical_to_direct_git_objects -v
python -m unittest tests.test_stream_adapter_and_publication_catalog.PublicationCatalogTests.test_batched_reader_fails_closed_for_missing_and_malformed_objects -v
```
