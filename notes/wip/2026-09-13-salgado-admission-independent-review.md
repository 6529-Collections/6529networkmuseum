# Independent Salgado admission and projection review

Reviewer: `codex-reviewer:salgado-2026-09-13-independent`  
Canonical task: `/root/salgado_independent_review`  
Reviewer kind: independent AI agent, distinct from the constructor  
Review effort: Ultra, as expressly appointed by punk6529 for this accession  
Recorded: 2026-09-13T23:04:07.458083+00:00

This is a follow-on review of accession `6529NM.2026.004`. The original intake approval and its commit-binding receipt remain unchanged. The explicit appointment supports binding independent AI record review within this accession scope. No human identity, human signature, GitHub review, protected-PR approval, or production deployment approval is claimed.

## Initial finalization review

Reviewed source: `7c1c258696022689df36d35f232199980cf65a97`, compared with the independently approved intake at `4939941ae69d5edf0eec86712186add1666ab410`. The changed-file inventory contains 137 files. Its raw Git-blob SHA-256 inventory digest is `27fbb0175e0417f99a50e2fca6a7dc47d05e661e9d5b42f0e8d8a3064a627d35`. The digest is SHA-256 of UTF-8 concatenation of each sorted relative POSIX path, NUL, its lowercase raw SHA-256 hex, and LF. This inventory includes admission and catalogue records, public prose, media, graph and publication projections, their builders, validation/schema changes, evidence snapshots and implementation notes. Historical unchanged scholarship and primary source research retain their separate intake review.

The review examined the admission act and certificate; six object, rights and condition amendments; the register and exact predecessor snapshot; 17 new public entities and 40 relations; the Collection and Gift Acquisitions membership revisions; all 17 public texts; 18 display media files; visitor publication and identity inventories; the finalizer, projection/replay code, state-machine change, register schema and Salgado tests. It did not repeat live chain research or perform cloud, on-chain, external publication or repository approval actions.

Independent verification passed:

- All 20 historical record snapshots match the intake Git blobs, prior raw SHA-256, payload commitment and version.
- The retained revision-5 register is byte-identical to the intake register. Earlier lots and amendment-history entries are unchanged.
- The six title bindings retain the exact reviewed title-instrument hash; immutable title references resolve to the intake commit, including the rights-event references. Receipt, formal acceptance, title registration, administrative custody registration and accession remain separate dated facts.
- All 18 public WebP byte counts and SHA-256 values match the already reviewed restored display manifest. The six images were inspected during intake review; byte identity carries that visual review forward.
- The six works each have exactly one expected artist, project, curated-group, accession, Collection and media relation, with the correct object IDs, ordering and media identity. All 59 new or revised projection records remain openly pending independent review.
- All 17 Salgado public manuscripts appear in the visitor bundle with exact LF-normalized content. Caption and visual-description substance is unchanged from the corrected intake; the forest description for token 226 and the limits on identifying people/events in token 4697 remain intact.
- The rights-state change permits explicitly unspecified creative-derivative and AI-training rights while retaining the requirement for explicit ordinary Museum-use statuses. It does not convert token ownership into copyright.

## Findings at the initial review

Disposition: changes requested for two code gates and one source-anchor completeness correction. These are construction/projection issues; the existing intake approval remains valid.

1. **P2 — Require an exact approved intake receipt.** `scripts/finalize_salgado_accession.py` accepted the intake commit as a substring anywhere in receipt JSON. It did not require an approved outcome, the exact `reviewed_commit_sha`, reviewer identity, or source-receipt binding. Authority and fixity checks used `assert`, which is disabled by optimized Python. The actual receipt was approved and byte-bound; the concern is the reproducible construction gate. Require exact receipt fields and explicit exceptions, with mutation coverage.
2. **P2 — Make register predecessor forms exclusive.** `schemas/accession-register.schema.json` used `oneOf` with required fields only. A review-commit amendment carrying one of the source/snapshot fields still validated, despite the documented exclusive forms. An independent installed-jsonschema check reproduced both mixed partial forms passing. Explicitly exclude alternate fields in each branch and cover the mutations.
3. **P3 — Complete membership source anchors.** The revised Collection and Gift Acquisitions records appended the Salgado certificate to top-level references but retained old `source_record_ids` and profile evidence. Add the new source anchors and certificate evidence without removing earlier sources. Existing top-level evidence already supplied a trace, so the accession evidence itself is unaffected.

## Remaining controls

After correction, the exact amended commit must receive this reviewer's new disposition. Receipt-bound review sealing and final edition capture remain separate steps. The source archives were already verified; no later publication archive capture is presumed. The constructor's required full tests, deterministic replay, complete validator and manifest check must report their exact source/result. GitHub integration and protected-PR controls remain separate from this independent AI record review.

## Corrected commit disposition — 2026-09-13T23:12:43.441632+00:00

**Approved**, as the user-appointed independent AI record reviewer, for the exact admission and public projection scope at `c8165b5dff7e8a3a3a15601f057215c941d971fa`. The first review and its findings above remain historical evidence; all three findings are resolved. No material record finding remains. The appended registration-diligence statement also correctly distinguishes this binding AI appointment from separate GitHub approval.

The [machine-readable admission review receipt](2026-09-13-salgado-admission-review-receipt.json) contains all 140 changed-file raw Git-blob hashes and the precise approval scope. Its SHA-256 is `cc14cb269c9a0e13e5bc08f256f47c23faca6d088d61da5c018406608a414418`; its file-inventory SHA-256 is `e2dac8c2ce7761d2ccf9e493d12d3a19092c13ed5a42826afbd5341b26014cf1`. This binds bytes at the reviewed commit, not a line-ending-dependent working-tree copy. The original intake review receipts remain unchanged.

The exact approved manifest is `sha256:5f4cff5fde9882f0fe230e19cbb5753fddf2c1e1634bc5b9d8039e05e7409765`, Keccak-256 `0xaec772495b5c674745c7cd5cff362593adbc346b2cdfc120d7c3654246e6aeff`. Both commitments were independently recomputed from its committed canonical body. The eight Salgado tests passed independently; the constructor reports all 49 public projection tests passed. The entire final suite is not claimed passed here: isolated Windows Git-clone path-length reruns were still in progress.

F1 now requires exact approval/identity/commit fields, both source artifacts and the identical complete 70-file inventory with active fixity checks. F2 now rejects every mixed or partial predecessor form tested. F3 is present in both committed membership records, including source IDs and profile evidence. Caption, image, rights and provenance substance remains unchanged from the already reviewed package.

The record-review gate is satisfied for this exact source. Receipt-bound review sealing, verification of the resulting review-only delta, the outstanding release tests, final edition archival capture and separate GitHub integration controls remain. The receipt supplies an openly AI reviewer identity for the approved scope; it supplies no human signature, GitHub approval, protected-PR override, or approval of unrelated future changes.

### Validation update received after receipt issuance — 2026-09-13T23:13:09.188136+00:00

The constructor subsequently reported that commit `c8165b5dff7e8a3a3a15601f057215c941d971fa` passes bootstrap (1,291 JSON files), the full validator with Casey, deterministic replay of 427 records, all 17 Casey snapshot mutation tests using child-only Git longpaths, all 49 public entity tests and all eight Salgado tests. The six previously reported Windows clone-path failures are resolved in those targeted reruns. This is attributed constructor evidence; it supplements the receipt's accurately timed account without rewriting it. Final review sealing, final-edition archive/readback and separate GitHub integration controls remain.
