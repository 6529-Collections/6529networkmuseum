# Orchestration ledger

This append-oriented log preserves work state across task compaction and agent handoff. It is operational memory, not adopted policy.

## 2026-08-01 — autonomous build opened

### Mandate

Populate the GitHub repository through reviewable pull requests with the Museum mission and governance, adopted decisions, donation and accession policy, approved donation collections, Keys and Gates program/outcomes, the actual seven-work Casey Reas donation accession, transparent NextGen-compatible generative trait analysis, documentation-as-code controls, and the contract specification that will migrate repository records on-chain.

### User-confirmed status

- Keys and Gates works have not been minted.
- Minting may use a separate 6529Stream instance or a subcollection on the main Stream contract; this is TBD.
- The Casey Reas collection has been donated and requires accession documentation.
- The future contract specification must cover migration of the governed GitHub information on-chain.

### Non-negotiable controls

- Do not infer accession from custody or transfer.
- Do not infer acquisition or minting from selection.
- Do not use OpenSea rarity metrics.
- Separate constructor and reviewer roles.
- Preserve primary evidence, observation time, uncertainty, amendments, and deterministic hashes.
- Keep sensitive donor/legal/custody material outside the public repository; publish safe summaries and hashes only.

### Active phase

Phase 1: foundation, governance, decisions, donation policy, and approved-collection register.

### Research tracks launched

Independent parallel tracks cover museum standards, Casey on-chain provenance, Casey art/technical history, NextGen rarity, Keys and Gates evidence, repository/CI architecture, governance evidence, and the external registry. Results are to be written under `notes/research/` and then reviewed before promotion.

The user clarified that Luna work must run as parallel Codex tasks rather than subagents. Seven `gpt-5.6-luna`/`xhigh` worktree tasks were therefore launched:

- Casey token verification: `019fbdd6-6e75-7043-b510-0d6e426b8c2b`
- Casey art/technical research: `019fbdd6-6e75-7043-b510-0d8f523e4493`
- Keys and Gates records: `019fbdd6-8eb7-7663-8f51-2fd0e33e9f6c`
- NextGen rarity tooling: `019fbdd6-9ac1-7e81-b331-310ad99e7c90`
- Documentation control plane: `019fbdd6-ab7a-7470-9c87-5cff139d90a8`
- On-chain migration specification: `019fbdd6-bba5-7470-b827-726e5db08bdb`
- Governance evidence review: `019fbdd6-d7a2-7680-a454-0574d2df96c5`

Terra subagents are reserved for bounded independent review and disjoint sidecar work.

### GitHub control state

- `@6529-Collections/6529seize-maintainers` was granted `maintain` access.
- Repository-wide `CODEOWNERS` and a Museum review template were added.
- Squash-only merges and automatic deletion of merged branches were configured.
- GitHub Free did not expose branch protection/rulesets while this organization repository was private; the initial 403 limitation and intended rules were recorded before visibility changed.

The repository was subsequently made public with owner authorization. Rulesets `20188741`, `20188742`, and `20188743` now enforce maintainer review semantics, no-bypass Museum CI, and Copilot review respectively. The `6529bot` GitHub App installation `140321060` covers all organization repositories; the Museum review profile passed its repository-config and limited-initial readiness validators.

Independent foundation review identified missing schemas, incomplete public-evidence admission scanning, unenforced constructor/reviewer separation, two overstated GitHub-rule claims, and an accession-conflating README heading. The working branch now contains bootstrap schemas, schema-subset validation, direct derivation of all governance facts/hashes from the authenticated proposal snapshot, raw-evidence secret admission checks, record controls, corrected GitHub wording, and a donation/accession-neutral heading. Source-derived validation also caught and corrected the Complaint Cards proposal author from `punk6529` to `blocknoob`.

The first reviewer correctly refused to bind approval because it shared the constructor task identity and found that an anonymous review object could pass. Schemas and CI now require reviewer `actor_id`, `reviewed_at`, role, approved outcome, and canonical payload SHA-256, with a hard constructor/reviewer identity inequality. Binding approval is delegated to a genuinely separate Codex task.

Separate Luna task `019fbdd6-8eb7-7663-8f51-2fd0e33e9f6c` independently approved all three payloads at 2026-08-01T15:42:12.081Z against commit `63eb40c39644559ab435b7fd8a2d75f9a6c30204`. Its payload hashes are now bound in each `record_control`; CI recomputes them and rejects self-review, anonymous review, missing immutable commit, non-approved outcome, or payload drift.

## 2026-08-01 — foundation merged and parallel build checkpoint

PR [#5](https://github.com/6529-Collections/6529networkmuseum/pull/5) merged at 2026-08-01T15:44:14Z as `82e9069f5e8666b84ed14fdc4d04ee64b39b6bc1`. It established the public repository, active GitHub rulesets, no-bypass `Museum validation`, full Museum Wave evidence snapshot, adopted donation policy, independently reviewed governance/approved-collection/Casey-receipt registers, source-derived validation, and durable review controls.

### Active pull requests

| PR | Constructor scope | Review state at checkpoint |
|---|---|---|
| [#1](https://github.com/6529-Collections/6529networkmuseum/pull/1) | Complete governance evidence note and append-only decision format | Bot review found only terminology/versioning consistency fixes; constructor updating from main |
| [#2](https://github.com/6529-Collections/6529networkmuseum/pull/2) | Implementation-grade on-chain migration contract specification | Bot review found hash/signature/inline-payload/vector ambiguities; constructor resolving before merge |
| [#3](https://github.com/6529-Collections/6529networkmuseum/pull/3) | Casey Reas art-historical and technical research | Bot review passed with three factual-consistency clarifications requested |
| [#4](https://github.com/6529-Collections/6529networkmuseum/pull/4) | Transparent NextGen-compatible trait analysis tooling | Bot review requires narrower OpenSea-metric rejection, defensive guards, deterministic boundaries, and additional tests |
| [#6](https://github.com/6529-Collections/6529networkmuseum/pull/6) | Keys and Gates program plus sixteen selected-unminted records | Updating from main; program schemas and constructor controls required by new CI |
| [#7](https://github.com/6529-Collections/6529networkmuseum/pull/7) | Full documentation-as-code control plane, manifests, schemas, tests, and CI | Updating from main while preserving required check name and foundation controls |
| [#8](https://github.com/6529-Collections/6529networkmuseum/pull/8) | Born-digital accession/donation templates and standards crosswalk | Updating from main and aligning with executable review controls |

### Next construction tracks

- The chain-verification Luna task is pivoting to the complete Casey accession dossier under `records/accessions/6529NM.2026.001/`; it must not duplicate the evidence note already on main.
- After rarity PR #4 is reviewed and merged, freeze complete project metadata snapshots and publish NextGen-compatible trait results for every generative collection represented in the Casey accession. Trait prevalence remains separate from curatorial significance.
- Keys and Gates stays `selected_unminted`. No accession or custody work begins until the Stream topology decision and actual mint evidence exist.
- Contract specification PR #2 remains non-deployed design. Implementation, audit, governance approval, and deployment are separate later gates.

### Integration order

1. Governance evidence note and standards/templates, if their rebased diffs remain independent.
2. Documentation control plane.
3. Keys and Gates records against the final schemas.
4. Reviewed rarity tooling.
5. Casey accession dossier, then full-collection trait snapshots/results.
6. Contract migration specification after all integrity and signature findings are closed.
7. Cross-disciplinary release audit and deterministic manifest.

### Known evidence anchors

- Museum Wave: `5f207393-5418-4a75-8738-e40edb44a94d`
- Keys and Gates Wave: `4ff022b3-aa17-4a0a-ba78-58f64ff1d427`
- Museum custody reference: `networkmuseum.6529.eth`
- Casey accession lot: `6529NM.2026.001`
- 6529Stream implementation pin: `5021c8060950c3fef995271e674ed4b2007fee6d`

### Next actions

1. Publish Phase 1 pull request.
2. Reconstruct all sixteen Keys and Gates records as `selected_unminted`.
3. Verify Casey token identities and transfer evidence, then build the actual accession dossier without overstating incomplete gates.
4. Implement schemas, validation, deterministic manifests, and CI.
5. Produce an implementable on-chain migration contract specification and test vectors.

### Completed research sidecars available locally

- `notes/research/museum-standards-crosswalk.md`
- `notes/research/repository-ci-architecture.md`
- `notes/research/nextgen-rarity-method.md`
- `notes/research/casey-reas-art-technical-research.md`
- `notes/research/casey-reas-onchain-evidence.md`
- `notes/research/keys-and-gates-evidence.md`

These are research inputs, not governed records. They require integration review.

## 2026-08-01 - review-bot routing checkpoint

The `6529reviewbot` source repository was audited before changing Museum review routing. Its specialist kinds are intentionally opt-in rather than part of `review all`, and `followup` is designed for commits made after initial review.

The Museum automatic baseline applies exactly `general`, `security`, `privacy-evidence`, and advisory `glm-swarm` to every pull request. `media-external` and `deploy-actions` are maintainer-requested specialists; Stream-equivalent contract review is manually dispatched through the central head-bound review job while the deployed catalog lacks `stream-contracts`. The active PR-by-PR matrix is preserved in `governance/pull-request-review-policy.md`.

Independent review rejected the first routing draft because it documented five-kind commands that the four-job delivery cap would deny, duplicated automatic synchronize-event follow-up, and assigned external-media and Stream-contract specialists to prose outside their prompt boundaries. The corrected procedure keeps the conservative four-job cap, does not repeat the automatic baseline in specialist commands, and limits each command to four or fewer specialist jobs. `media-external` is now limited to executable external ingest, and `stream-contracts` to normative contract surfaces intentionally equivalent to 6529Stream.

## 2026-08-01 - exact-head review checkpoint

Main is `9f38bd4ba5f779540eabf2dfce019cc1382561e2` at this checkpoint.

### Merged work

- PR #1 merged as `7fa982abaadbd253cb813d71e67accf089759ff2`, adding the complete governance evidence note and append-only decision format.
- PR #9 merged as `72622a670854cc489330d930136bae7318044e41`, adding the risk-based review-bot policy after an independent reviewer rejected and then approved its corrected routing.
- PR #3 merged as `9f38bd4ba5f779540eabf2dfce019cc1382561e2`, adding the Casey REAS art/technical research. Independent review caught and corrected a false Studio exception: Art Blocks V3 token-ID decoding also applies to the Ex Nihilo V3.2.4 Studio token.

### Casey accession dossier

Draft PR #10 constructs lot `6529NM.2026.001` at initial head `880203dca23d3a56ec57468a2ac12069b1776aff`. It contains the formal statement, collection interpretation, seven object records/pages, seven technical/condition reports, provenance/transaction and rights schedules, preservation manifest, public inventory, restricted-annex stub, schemas, and record controls.

Its controlled state remains `received_onchain` with accession completion `not_complete`. The user-confirmed donation and seven-token receipt are recorded; title binding, donor-authority/adverse-provenance diligence, rights bases, render/condition verification, preservation ingest/recovery, display permissions, and independent review remain explicit gates. No deed, license grant, title conclusion, or rarity result is invented.

### Independent review findings in remediation

- PR #7 control plane: enforce accession cross-field identity, reject private-network envelope URIs and duplicate JSON keys, reject self-supersession, close nested schemas, and add executable ACCESSION/RIGHTS/CONDITION event-path fixtures. Receipt, acceptance, acquisition, title passage, custody receipt, and accession must be distinct events, including off-chain/non-token paths.
- PR #8 templates: add a distinct donation-acceptance event and dates, an off-chain transfer/custody path, accurate BagIt required/optional files, a C2PA 2.4 pin, structured PREMIS/IIIF/C2PA/OCFL mappings, and an explicit no-object-authorization consequence for Keys and Gates selection. Markdown remains documentation-only until executable schemas and gates exist.
- PR #6 Keys and Gates: correct OUT-015's statement-declared consent, keep per-work price null while purchase is unverified, and preserve the three previously reviewed foundation registers byte-for-byte. All 16 identities, ranks, votes, media references, statement hashes, CC0 declarations, and `selected_unminted` boundaries otherwise matched evidence.
- PR #4 rarity: match JavaScript left-fold arithmetic exactly, preserve production row order, require one collection plus observation/source provenance, support declared zero-non-Mint-trait tokens, handle NaN/Infinity and output failures without tracebacks, and reject every third-party rarity-service metric while allowing provenance citations.
- PR #2 contract specification: independent cryptographic/protocol review is in progress; no deployment or implementation claim is permitted.

Each remediation is assigned back to its constructor. The original reviewer task will re-review the exact corrected head; constructors do not bind their own approval. Mandatory `Museum validation` remains no-bypass even when other review services are rate-limited or budget-delayed.

## 2026-08-01 - standards and Keys and Gates merge checkpoint

Main is `a821eeadd3193f010dd5d27184ec3cf7dc90500f` at this checkpoint.

### Newly merged work

- PR [#8](https://github.com/6529-Collections/6529networkmuseum/pull/8) merged as `956ca06ba9c4563c844422c400ccb0bd37c94357`. It adds the born-digital/tokenized accession and donation templates plus the operational standards crosswalk. These files remain documentation-only templates until enforced by the executable control plane; they do not authorize an object, prove title, or complete accession.
- PR [#6](https://github.com/6529-Collections/6529networkmuseum/pull/6) merged as `a821eeadd3193f010dd5d27184ec3cf7dc90500f`. It adds the Keys and Gates program record, outcome index, and sixteen independently reviewed outcome records. Every outcome remains `selected_unminted`; no mint, purchase, custody, acquisition, or accession is claimed. The Stream instance-versus-main-subcollection topology remains undecided.

The independent Keys and Gates reviewer was task `019fbe15-7872-7312-a455-697a8835683c`. It approved the eighteen payloads at commit `0e82d12306048c7356cd27587e7d5c84e2bbde80`; the final exact-head binding check passed at `6cd1b0da88f4aa23cd06a18db08bf8b74d77628b`, with payloads unchanged and review metadata correctly bound.

### Current dependency order

1. PR #7 must close the remaining fail-closed validation findings and merge the executable control plane.
2. Draft PR #10 must then migrate the Casey lot into that merged control plane, resolve schema/index integration, add canonical payload hashes and accurate source authority, preserve raw Art Blocks Studio fields, and receive exact-head independent review.
3. PR #4 must match the production NextGen left-fold arithmetic and source-order behavior, enforce collection/source identity, support zero-trait tokens, reject all third-party rarity metrics, and pass exact-head re-review.
4. After PR #4 merges, a separate Luna worktree task (queued as `client-new-thread:1548c2fb-8ba0-465d-82b5-789185a34834`) will freeze complete authoritative metadata observations and publish transparent descriptor results for CENTURY, Pre-Process, Phototaxis, 923 EMPTY ROOMS, and Ex Nihilo (Cosmos).
5. PR #2 must close all cryptographic, authorization, payload-mode, Stream-convergence, URI-safety, reentrancy, supersession, and release-manifest findings before its specification can merge. It remains a design, not a deployed contract.

### Casey accession review boundary

Independent review confirms the seven token identities, CAIP-19 values, common receipt, log indices, custody, and `received_onchain` / `not_complete` state. It blocks accession-safe treatment until cross-file invariants fail closed, canonical payload hashes and source-head evidence are bound, PR #7 integration is complete, historical transaction verification grades are corrected, and the preservation evidence package captures raw metadata/generator bytes. Formal donation acceptance, title passage, rights grants, condition assessment, and preservation completion remain unclaimed gates.

## 2026-08-01 - deployed review-catalog compatibility checkpoint

Production evidence identifies App Runner image `eefe911e-202606222152` as
rejecting `stream-contracts` in the repository catalog. The repository config
now omits that kind so the automatic `general`/`security`/`privacy-evidence`/
`glm-swarm` baseline and synchronize follow-up can resume after merge. This is
a temporary compatibility pin, machine-checked by the catalog fixture; it is
not a permanent specialist decision. Stream-equivalent contract diffs still
require the central `review-job.yml` at a head-bound SHA with supported inputs
until App Runner is upgraded. No production deployment or restart is part of
PR #7.

## 2026-08-01 - exact-head remediation in progress

The independent review of PR #7 head `0a8f6b766c26ae3bde0febd03d95a8e59b3c8b5f`
found three conservative public-control gaps: declared non-text raw evidence
could fall back to text scanning, uppercase UTF-16 credential labels were not
found, and `getattr` could mediate sensitive process/import calls around the
AST guard. The remediation adds fail-closed media routing, bounded folded
UTF-16 scanning, alias-aware sensitive-root dynamic-attribute rejection, and
focused negative tests. No governed records are changed; exact-head review and
head-bound bot reruns follow the cross-platform validation.

## 2026-08-01 - protocol-spec release boundary

The merged control plane validates `specs/` as governed public content, but its
deterministic release manifest initially omitted that root because no protocol
specification existed when the control plane was constructed. The first narrow
remediation exposed a wider boundary omission: governance controls, templates,
GitHub CI/review policy, and named root controls also affected releases without
being committed by the release manifest.

Before the on-chain migration specification can merge, the release inventory is
therefore closed over `.github/`, policies, records, schemas, docs, governance,
specs, templates, scripts, tests, and six named root control files. A formal
`specs/README.md` defines the admission boundary. Tests pin the exact roots and
files, prove that real and future specification files are inventoried, and
reject missing or linked configured roots and files. Evidence, WIP notes, Git
internals, and the self-referential release-artifact directory retain explicit
separate treatment.

## 2026-08-01 - Casey accession exact-head synchronization

PR #10 was rebased once onto current `origin/main` at `ab4ec5e1193382133aa09677fbfb32dbbe51725f`, preserving the merged Casey research and this ledger checkpoint. The dossier now ends at `4b75ece88b354c534137e2f6306965f541a38faa`. Local bootstrap validation, whitespace checks, and the refreshed mandatory Museum validation pass. The PR remains draft and unmerged; no constructor self-review or accession-completion claim is made.

## 2026-08-01 - Casey accession synchronization after PR #8

`origin/main` advanced to `956ca06ba9c4563c844422c400ccb0bd37c94357` after the independently approved templates/crosswalk PR #8. PR #10 was rebased once onto that exact main. The Casey dossier records and schemas are byte-for-byte unchanged from the pre-sync head `ae42e16f5e93a169c30ce0b111fe992fddd59652`, and the approved main templates/crosswalk remain unchanged. The synchronized dossier head is `8435faf858ec4dc807487a618e75baa3f1d0f229`; local bootstrap and whitespace checks pass, and mandatory Museum validation run `30708569720` / job `91391853135` passed. PR #10 remains open, draft, and unmerged for independent integration review; no merge or accession-completion claim is made.

## 2026-08-01 - Hold Casey remediation for PR #7 integration

`origin/main` advanced to `a821eeadd3193f010dd5d27184ec3cf7dc90500f` after independently approved PR #6 merged the Keys and Gates selected-unminted records. PR #7 remains open and is the controlling dependency for the Casey fail-closed control-plane integration, so no rebase or dossier/schema remediation was applied in this checkpoint. PR #10 remains draft at `353858d46c2d2530381bc7664efd77e3abd21bba`; its accession payload is untouched. When synchronization resumes, preserve every `records/programs/6529NM-AP-01/**` payload byte-for-byte against the `a821eea` main-tree baseline while resolving only the required integration conflicts and review findings.

## 2026-08-01 - Casey dossier migrated to merged control plane

`origin/main` was synchronized once at the user-specified PR #7 merge `7193bfb9a0a6ead1871180b931aced755676b327`. The Casey lot is now represented by one enforced `ACCESSION_LOT`, seven `WORK_DESCRIPTION` object records, seven `RIGHTS_STATEMENT` records, and seven `CONDITION_REPORT` records, with public pages and a content-addressed preservation evidence manifest. The seven-token receipt remains custody evidence and the lot remains `received_onchain`/`not_complete`; intake processing is not formal acceptance, title, rights, condition, curatorial, preservation, or display approval. Historical events are classified per-event, `.07` retains raw Studio fields, and every Casey payload has a self-excluding canonical SHA-256 commitment. Reviewer fields remain null for independent review. Bootstrap, fetch guard, and the full 57-test suite pass at this working checkpoint; final manifest/CI and draft-PR head binding remain to be completed.

## 2026-08-01 - post-migration release-inventory synchronization

Main subsequently advanced to `13578fe13a9638e497e96b26b5ce8c4a863543ab` through PR #14, which closes the governed release inventory over `.github/`, policies, records, schemas, docs, governance, specs, templates, scripts, tests, and named root controls. PR #10 was rebased onto that current main so the release manifest and mandatory validation use the merged tooling; Casey payloads and evidence boundaries remain substantive work in this draft. The draft remains open, unmerged, and independent-reviewer metadata remains null.

## 2026-08-01 - Casey final merged-main validation checkpoint

The closed manifest was regenerated at the PR #14 boundary with 146 governed entries and commitments `keccak256:0x2eeacfa36a8f8ddd32df4ddd4e22859848487dfb76133775354dce005754415a` / `sha256:603e6fae89122f6a023483a0f6c3197551287b2897ea05908e3ea6deff9509ba`. Bootstrap, fetch guard, full validator, manifest idempotence, whitespace checks, and the complete 60-test merged-main suite pass (one platform skip). Targeted mutations of a token ID, receipt transfer count, and `received_onchain` state were each rejected after canonical commitments were refreshed. Casey remains `received_onchain`/`not_complete`; reviewer metadata remains null pending the same independent reviewer’s exact-head re-review.

## 2026-08-01 - Casey exact-head review remediation

The same independent reviewer requested changes at `cb1e822b2221cdbcd614dc4b20478ae066223874`. The remediation replaces the dangling provenance evidence path with all seven canonical rights records, removes the nested provenance `$schema` marker, and routes the nested schedule through the accession schema's authoritative transaction-provenance `$defs` reference. Validation now resolves Casey evidence path/record targets and rejects dangling references or malformed nested events. The raw upstream metadata bytes remain unchanged and the public boundary explicitly documents verbatim royalty-routing wallet fields, authenticity signatures, and historical counterparty wallets as source-fidelity/provenance data only, without donor-identity, title, rights, or payment inference.

The evidence manifest was refreshed in declared raw-byte mode; all nine entry hashes/sizes validate, and the seven raw metadata streams remain byte-identical. Its current file SHA-256 is `sha256:98848849d43b808cf231a289f2dada7e760bedbdb486a77648711ab8995160bd`, bound into the lot source/preservation fields and all seven object preservation records. Zero Stream signatures and reviewer-null constructed records are explicitly unsigned placeholders; validator mutations for signed-authority, formal-acceptance, completed-accession, and premature-review interpretations fail closed. The regenerated closed release manifest is `keccak256:0xd97f5d597a5a4dbb94b7453e1a9d74b4835d68e341ba6660bb2accc7c27f42a3` / `sha256:593bb1107c7507748c13df05974c0a6cf333d55a08979e7dcefbc56fa7381c00`. Bootstrap, fetch guard, full validator, manifest idempotence, whitespace checks, and the complete 62-test suite pass (one platform skip). The draft remains `received_onchain`/`not_complete`, open, and pending independent re-review.

## 2026-08-01 - nested preservation manifest hash remediation

The independent exact-head review found one remaining stale field: `preservation_manifest.manifest_sha256` still carried the pre-disclosure `sha256:4091651e...` while the raw evidence manifest and other fixity bindings carried `sha256:98848849d43b808cf231a289f2dada7e760bedbdb486a77648711ab8995160bd`. The nested field is now bound to the actual manifest bytes; `scripts/validate.py` cross-checks it alongside the lot/source and seven object fixity references, and a hash-refreshed targeted mutation rejects divergence. Raw metadata remains unchanged. Bootstrap, fetch guard, full validator, manifest generation/idempotence, whitespace checks, and the complete 63-test suite pass (one platform skip). New release commitments are `keccak256:0x2ff70eadf76e8c82d44f76a780fd22f82c309ee4ee242c1d5b8213af8972e8b0` / `sha256:ccd16b1d03ceebf4cc659a1d5a1421eeb2c4a4002aecdceb5e02c73b2a9a65f5`; the draft remains `received_onchain`/`not_complete` pending re-review.
## 2026-08-01 - Casey full-collection acquisition checkpoint

The follow-on acquisition branch is `codex/casey-reas-collection-snapshots`,
based exactly on synchronized `origin/main`
`6ab83b456f1ad8d1b7b88b79cc960954feb56432`. It adds source configuration,
reviewable acquisition and verification tooling, a materialization fixture, and
one complete v2 run for all five Casey REAS projects represented in accession
lot `6529NM.2026.001`. Governed `records/` payloads were not changed.

The authoritative route is deliberately bulk-first: one observed Ethereum
mainnet block binds the configured on-chain project population view and every
`tokenURI(uint256)` string by batched `eth_call`; the official Art Blocks
Hasura `tokens_metadata` endpoint supplies the complete paginated feature
population with raw page bytes, query/variables, server order, counts, request
hashes, and retry attempts. The current complete run is
`20260801T172252532Z`: CENTURY 1,000, Pre-Process 120, Phototaxis 1,000,
923 EMPTY ROOMS 924, and Ex Nihilo (Cosmos) 256, totaling 3,300 tokens. The
server row order is retained separately from numeric canonical token/trait
ordering. Sampled official token endpoint checks are cross-check evidence only;
their eight feature omissions/differences are visible warnings and do not
replace or reduce the bulk population.

`scripts/verify_casey_snapshot_package.py` passes the run, raw-reference
hashes, population/identity/order checks, prohibited-field checks, and the
scalar materialization fixtures. At this checkpoint PR #4 is independently
merged as `ff1c5825e3b61bfb2df0a639e057297beb946e4d`; descriptor emission is
now permitted only after rebasing this branch to that exact mainline and
running the merged `scripts/rarity/analyze.py`. Collection descriptor outputs
remain transparent statistical descriptors, not quality judgments, value
signals, or canonical truth; constructor/reviewer separation remains explicit
with `review: null` until a separate reviewer is assigned.

## 2026-08-01 - Casey descriptor emission checkpoint

After PR #4 independently merged into `origin/main` at
`ff1c5825e3b61bfb2df0a639e057297beb946e4d`, the branch was rebased so that
the merged `scripts/rarity/analyze.py` is an ancestor and its rarity-tool path
is clean. That exact entry point ran with duplicate policy `error` against all
five complete v2 snapshots. The resulting full collection artifacts are in
`evidence/casey-reas-collection-snapshots/descriptors/`, with descriptor
manifest `descriptor-manifest.json` and result hashes bound to the run.

PR #4's closed-field safety guard rejects any input key containing `metric`,
including the acquisition package's negative `not_a_marketplace_metric`
control annotation. The source snapshots were not changed. Each descriptor
records a hash of an explicit derived tool-input projection and the single
removed path; all source rows, feature values, raw observations, source order,
canonical order, block provenance, and cross-check warnings remain in the
frozen acquisition package. The outputs are transparent statistical
descriptors only, not quality, value, marketplace, or canonical-truth claims.
The descriptor manifest and every descriptor retain `review: null` pending
independent review.

## 2026-08-01 - PR #13 reviewer-remediation construction checkpoint

Reviewer changes requested at exact head
`0181ec4c7eed184dd4bbac963ef30392dca37f34` were remediated on
`codex/casey-reas-collection-snapshots`. The stable source-snapshot commit is
`820f4bb6999fb9df3b094692913d70ebf6d9dc63`; the raw acquisition source commit
is `8585aedb9f176806624a7b069cdd10a6f1995824`. The current package contains
the exact independently merged PR #4 tool at merge commit
`ff1c5825e3b61bfb2df0a639e057297beb946e4d`, Git blob
`755a1b1c948d900496f5e279594223c8c99ab3e8`, and SHA-256
`e4060edf7354aa683458dfa0e620c598673a0c65202c8efadd768ae8dc03cc53`.

The complete run remains `20260801T172252532Z`: 3,300 tokenURI requests,
3,327 total request records, 62 unique reconstructed request bodies, 35,088
materialized traits, 79 raw files, 17 explicitly recorded HTTP group-marker
exclusions, and eight unchanged cross-check warnings. The verifier compares
all raw bytes to the acquisition commit, all snapshots and the child manifest
to the stable source commit, recomputes rows from raw Hasura/JSON-RPC bytes,
recomputes all five descriptor results with the exact tool, and checks the
root inventory and mutation controls. The root package manifest has 171 bound
files (79 raw, 64 derived provenance/request files, five snapshots, and five
descriptors); no tracked file exceeds GitHub's per-file limit.

Generated descriptors remain transparent statistical descriptors only. Review,
curatorial significance, title, rights, accession acceptance, and accession
completion remain null/unclaimed. PR #7's approved safe-HTTPS migration is a
deferred dependency; this draft does not claim that migration or readiness for
merge.

## 2026-08-01 - PR #13 CI runtime-determinism remediation checkpoint

Fresh CI run `30713015267` checked the full-history PR merge ref
`d65bf813a195fba40fb262e54f0f9491974012d0` and failed only during merged PR #4
descriptor recomputation. Native reproduction at that exact merge ref showed
the source verifier itself was sound: descriptors were generated under CPython
`3.12.10`, while `python-version: "3.12"` resolved in Actions to `3.12.13`.
The differing float serialization caused the expected result comparison to
fail at `century: merged PR4 result recomputation`; no source, raw observation,
or descriptor payload was changed.

The workflow now pins CPython `3.12.10` exactly (while retaining full history),
and the verifier rejects any other CPython implementation/version before
recomputing byte/hash-sensitive descriptors. It also checks each recorded
descriptor determinism profile against that pinned runtime, with a dedicated
negative mutation test. Review remains null; PR #7 remains deferred; the PR
remains draft.

## 2026-08-01 - PR #13 exact-head fail-open remediation checkpoint

Independent exact-head review at `d58926fcf9ba5c8fe7ad5d09455db9e202042fd8`
reproduced two fail-open mutations. The root verifier accepted a package README
inventory substitution with internally updated hashes, and it accepted an
OpenSea URL added to a descriptor when descriptor inventory and pointer hashes
were updated. Neither mutation changed the preserved acquisition bytes or
descriptor result payloads in the governed package.

The verifier now derives and checks a closed path/role allowlist for all 172
root inventory entries: package files, the exact five snapshots/descriptors,
the pinned run raw/derived paths, and an explicit fixed list of shared source
files. Semantic bindings must stay inside the package prefix except the
hard-coded PR #4 tool path. A recursive external-reference guard now scans
every bound JSON artifact, including descriptors, results, inputs, methods,
provenance, fixtures, and raw observations. It rejects marketplace/provider
variants, URLs, and imported/precomputed metric field names while allowing the
Museum's generated internal statistical result fields. Two disposable exact
worktree end-to-end mutations cover the README substitution and descriptor
OpenSea/provider injection.

Raw/source bytes, populations, runtime pin, descriptor results, review nulls,
and PR #7 deferral remain unchanged. PR #13 stays draft and must not be
merged or synchronized to PR #7 until this remediation receives independent
exact-head review.

## 2026-08-01 - PR #13 PR7 control-plane integration checkpoint

The two fail-closed findings above were completed before the one permitted
mainline synchronization. The branch was then rebased exactly once onto merged
PR #7 / `origin/main` `7193bfb9a0a6ead1871180b931aced755676b327`. The package no
longer records a deferred PR #7 status: its root dependency binds that merge
commit, the merged control-plane blob pins, and current hashes for
`scripts/safe_fetch.py` and `scripts/check_fetch_guard.py`; those modules and
the control-plane test are now in the closed root inventory.

Every executable network-retrieval path is mediated by `safe_fetch.py`. Because
the authoritative acquisition protocols are JSON-RPC and Hasura POST, the
approved primitive now admits only bounded `application/json` POST bodies in
addition to GET/HEAD, with the same HTTPS-only resolve/pin/redirect/framing/
deadline controls. `check_fetch_guard.py` passes. No acquisition run was
performed: the preserved v2 raw bytes, source commits, populations, 3,300
tokenURI requests, 35,088 traits, 17 explicit exclusions, eight warnings, and
five descriptor payloads remain byte-for-byte unchanged.

The regenerated package has 175 inventory files (79 raw observations and five
descriptors), with package manifest SHA-256
`sha256:9d9b863e728d554454817057bc4e536ff4b367056e4aa6798887eb9ed84fbc89`.
The release manifest is current at SHA-256
`sha256:e2e8cbbcc0149238307f5706a8225f232079265c17e36d11fc33aea2c4307f4b`.
Review metadata remains null, no title/rights/accession acceptance is claimed,
and PR #13 remains a draft pending exact-head independent review.

## 2026-08-01 - PR #14 exact-main synchronization checkpoint

After the complete merged-main suite passed (68 tests, including 17 rarity,
11 Casey mutation, and merged control-plane tests), PR #13 fetched and verified
`origin/main` exactly at `13578fe13a9638e497e96b26b5ce8c4a863543ab` and rebased
the Casey work exactly once. The only conflicts were derived release-manifest
hunks and the append-only ledger; PR #14's closed release inventory and both
Casey ledger entries were preserved. An exact Git comparison reports no changes
under the preserved 79-file raw observation tree.

The package was regenerated without acquisition or descriptor reruns: 175 root
inventory files, 79 raw observations, five descriptors, 3,300 tokenURI
requests, 35,088 traits, 17 exclusions, and eight warnings remain bound. The
rebased package manifest is
`sha256:11e5a963a508fc15c5bfe683986a43aa25b0c85a06a0a98a7b66a621be1df8f6`;
the closed release manifest is
`sha256:518a80d7dfb20b25070c9fee94552824b250cd672e4f7de1fc63f30ea39480f2`.
The exact rebase result before final manifest/ledger commit is `fda242b`; the
working branch remains draft with reviewer, title/rights, and accession
acceptance metadata unbound.

## 2026-08-01 - PR #13 acquisition-pin reachability remediation

Exact-head CI at `8b02fece50b7f93b0c0ca4b6e4db25dff39b6c20` showed that the
historical acquisition pin `8585aedb9f176806624a7b069cdd10a6f1995824` was not
reachable from the rebased remote history, although the local object-rich
worktree could still read it. The acquisition commit pin is therefore updated
to the reachable rebased acquisition commit
`48cd2fbf2914d295cdc4260dedb1345061f5e3b6`, which contains the same preserved
79 raw observation files byte-for-byte. The historical source-snapshot pin
`820f4bb6999fb9df3b094692913d70ebf6d9dc63` remains unchanged and is retained as
a reachable parent without a tree change.

The five descriptors, descriptor manifest, pending review ledger, root package
manifest, and release manifest were regenerated only for this dependency-pin
change. The package now reports SHA-256
`sha256:8b438b09c09eedc8ec53c3d8e4e063f6ebba9f32ff75afe672d6a1cea725cae6`;
the deterministic release-manifest commitment reports
`sha256:6bd97c002283999ae739f705a11e1b2d8fc2cca93e7fa03a2510764bfd706892`.
All populations, source/canonical orderings, raw bytes, exclusion rows,
descriptor results, runtime pin, and null reviewer fields remain unchanged.

## 2026-08-01 - PR #13 symlink and direct-PR4-byte remediation checkpoint

Independent review at `3391d74619a0955fb479ea1ffae706aa8ea37d19` identified a
fail-open bound-raw symlink substitution and an unconfirmed Phototaxis
serialization hash alternative. The pinned PR #4 tool was rerun from the
preserved Phototaxis snapshot under CPython `3.12.10` in isolated constructor
and reviewer trees, including `PYTHONHASHSEED` values `0`, `1`, `2`, `42`,
`123`, and `random`; every raw output was
`sha256:aa3c6259d0529b84cc42ddbf3dbc209d9d44a320440f80d69b5bd8d91b4a5044`,
matching the recorded descriptor. The reported
`sha256:492687b80070621cc10f7dd32855e11ccffefad69c875b039b9eed9efcfa58c8`
was not reproducible by the pinned tool or common JSON reserializations and is
therefore not substituted for governed bytes.

The verifier now lstat-checks every bound package/inventory/raw/derived/
snapshot/descriptor path component, rejects POSIX symlinks and Windows
reparse points/junctions before reads or enumeration, and constrains the
governed package root lexically. The mutation suite includes an end-to-end
same-byte bound-raw symlink case and a Windows reparse-attribute negative
control. Descriptor verification now compares direct merged-PR4 output bytes
and SHA-256 for all five results, in addition to semantic equality, under the
pinned UTF-8/indent/newline serialization boundary.

No acquisition or descriptor rerun was performed. The preserved package still
contains 79 raw files, 3,300 tokenURI requests, 35,088 traits, 3,327 request
records, 62 unique request bodies, 17 explicit exclusions, eight warnings, and
five descriptor outputs; source and canonical orderings remain separate. The
working package manifest is
`sha256:fdaddda0989c34a7b9c1cef4c79faee3eba5d1382d68ed06b4f519ba5a1fc70f`;
the release manifest was regenerated after this append-only checkpoint. Its
current commitment is intentionally reported by the validation handoff rather
than embedded here, avoiding a self-referential ledger/manifest hash.
Review and curatorial metadata remain null; no title/rights/accession
acceptance is claimed. PR #13 remains draft pending the same independent
exact-head review.

## 2026-08-01 - PR #10 Casey dossier package integration checkpoint

PR #10 merged the exact draft head `ec6493ee48ffa155c8c923a669c8ff7a1ad4dba8`
with `origin/main` `9700e842d0c991280b476cc67849d966221a742a` in the isolated
PR worktree. The Casey lot now binds the merged source package at
`evidence/casey-reas-collection-snapshots`, package-manifest SHA-256
`fdaddda0989c34a7b9c1cef4c79faee3eba5d1382d68ed06b4f519ba5a1fc70f`, and
the complete descriptor manifest. Each object maps to its required descriptor:
CENTURY `.01`/`.02`/`.03`, Pre-Process `.04`, Phototaxis `.05`, 923 EMPTY
ROOMS `.06`, and Ex Nihilo (Cosmos) `.07`.

The public and machine records now call the descriptors transparent, linked,
available, and reproducible, anchored by package and descriptor hashes. They
make no OpenSea/marketplace, aesthetic, quality, value, or ranking claim. URLs
are transitional `tree/main` or `blob/main` publication locators only; no
future merge pin is asserted. The seven raw public metadata files remain
byte-identical and keep their raw-byte evidence-manifest binding.

This integration does not change the accession decision: the lot and every
object remain `received_onchain` / `not_complete`; formal acceptance, title,
rights, condition, preservation, and independent registrar/curatorial review
remain incomplete. The draft remains open and must receive independent
exact-head review after validation.
## 2026-08-01 — PR #2 deterministic remediation checkpoint

The PR #2 branch merged `origin/main` at
`9700e842d0c991280b476cc67849d966221a742a` through
`4329953d66360037122691023b1d0d4da42e9ecd`. The V1 specification now pins the
full `keccak256("MUSEUM_BATCH_VECTOR_V1")` value
`0xa4713265f6f293e83885203722026053a888831af3f829e81b6aaed0d5d1d70b`
and batch commitment
`0x1c1c8c0c0c71816b08183589eaca344e6cd6b0ba1bc784c2d5a84337c377fc8d`.
The one-record manifest vector remains
`0x8bb17fc4361cbfe29c586218e716d0c4789973b222ee7a403f9d22f6f483a280`.

The URI harness rejects malformed percent escapes, CGNAT/private/reserved
literals, overlong CIDv1 varints, non-ASCII path characters, and malformed or
explicit ports without throwing. The HTTPS lifecycle harness proves expiry
blocks new writes, renewal restores eligibility, and pre-expiry records remain
readable with their historical assertion. The detached signature-bundle
fixture has a content-addressed IPFS URI, alternate Arweave-form retrieval
reference, schema, then-current 3/3 offline recovery check (superseded by the
exact-threshold 2-of-3 remediation below), and an explicit statement that
it is not published release or deployment evidence. Full validation, a fresh
release manifest, exact-head CI, and independent review remain required before
any merge; implementation and deployment remain separate authorization gates.

## 2026-08-01 - Post-merge fresh-clone publication-pin correction

Supersedes: `2026-08-01 - PR #13 acquisition-pin reachability remediation` in
this ledger.

Post-merge `main` workflow run `30718106015` failed only in the Casey package
verifier. PR-head and long-lived local worktrees could resolve construction
commit `48cd2fbf2914d295cdc4260dedb1345061f5e3b6`, but GitHub's squash merge did
not retain that construction history in the ancestry fetched by a fresh
`main` checkout. The prior entry's claim that the acquisition pin would remain
reachable after squash publication is therefore corrected here; it was
reachable from the PR branch, not from the resulting public main history.

The immutable construction provenance remains unchanged in the package:
`acquisition_commit` is `48cd2fbf2914d295cdc4260dedb1345061f5e3b6` and
`source_snapshot_commit` is `820f4bb6999fb9df3b094692913d70ebf6d9dc63`.
The excluded `latest-run.json` pointer now additionally records
`published_source_commit` as merged main commit
`9700e842d0c991280b476cc67849d966221a742a`. Fresh clones verify the 79 raw
observations, five snapshots, and child run manifest against that reachable
publication commit. A fail-closed mutation test and an ancestry test cover the
new boundary.

No raw observation, snapshot, descriptor, descriptor-result, request,
exclusion, warning, or collection-population byte changed. The regenerated
package-manifest SHA-256 is
`sha256:c08749355ea12c2948efdfdeb232675ab4bf693976a94c6ebb4ce24b0b5d08ab`;
its change is limited to the updated README, verifier, and mutation-test
inventory entries. The excluded `latest-run.json` pointer itself also changed
to add `published_source_commit` and the regenerated package-manifest pointer.
The governed release-manifest SHA-256 is
`sha256:d05f75c65c0af0172a0a2f2207693e4211d5c0f4f69fad8d4907ebd90e12470e`.

After final package and governed-manifest regeneration, the constructor ran
`python scripts/bootstrap_validate.py`, `python scripts/check_fetch_guard.py`,
`python scripts/validate.py`, `python scripts/generate_manifest.py --check`,
`python scripts/verify_casey_snapshot_package.py`, the complete discovered
unittest suite, and `codex-diff-check`. All passed; 75 tests ran with the one
expected Windows named-pipe skip, and the package verifier reproduced 3,300
tokens, 35,088 traits, 79 raw files, and five descriptor outputs.

## 2026-08-01 - PR #10 immutable Casey publication-boundary correction

This append-only checkpoint supersedes the mutable-locator assertion in the
earlier PR #10 package-integration checkpoint. The accession evidence is
two-level: artwork-source bytes are bound to reachable
`published_source_commit` `9700e842d0c991280b476cc67849d966221a742a`; the
reviewed Casey package/toolchain publication is bound to immutable release
commit `bf70ba3fd888d2d1b8add90fe56e913102f8aa68`, package-manifest SHA-256
`sha256:c08749355ea12c2948efdfdeb232675ab4bf693976a94c6ebb4ce24b0b5d08ab`,
and release-manifest SHA-256
`sha256:d05f75c65c0af0172a0a2f2207693e4211d5c0f4f69fad8d4907ebd90e12470e`.
Construction commit OIDs remain provenance labels only.

The accession records use exact `blob/bf70ba3fd888d2d1b8add90fe56e913102f8aa68`
links for release-bound package, descriptor-manifest, and descriptor evidence;
`main` links are reserved for deliberately mutable living documentation. The
dossier refresher and fail-closed validator retrieve and hash the published
bytes with fixed-argument Git history calls, require complete reachable
history, and do not rebind this dossier if a future current package changes.
Tests reject wrong release commits or hashes and mutable `blob/main` links in
release-bound fields. The seven raw public metadata bytes remain separately
bound and unchanged. Formal state remains `received_onchain` / `not_complete`,
with reviewer and authority fields null; no acceptance, title, rights,
condition, preservation, or registrar decision is asserted.

## 2026-08-01 - Casey formal gift authorization and curatorial integration

This checkpoint adds a limited, effective Gift Acceptance and Accession
Authorization for lot `6529NM.2026.001`. It records the user-authorized
institutional decision to formally accept the seven verified gifts under the
adopted Art Blocks preapproval (`6529NM-GOV-1052156`, Wave `#1052156`, drop
`2e88273f-013c-4fdd-bea3-7de5451098e8`) and Donation Acceptance Policy
(`6529NM-GOV-1052812`, Wave `#1052812`, drop
`86e43beb-b55d-42f0-9eea-a3c115b08abc`). The authorization is formally
accepted and effective; its constructed record status and pending independent
review describe documentation QA only, not a provisional institutional
decision. The public donor/authority declaration is expressly user-supplied
and is neither a cryptographic signature nor an executed deed.

The generic Gift Acceptance and Accession Authorization schema is reusable:
it requires one or more assets and closed evidence structures but does not
hard-code this donor, custody name, transfer count, or seven-asset schedule.
Casey-specific semantic checks bind those facts, the shared receipt, exact
CAIP-19 assets, governing records, and the pending completion boundary.

The lot therefore remains `received_onchain` / `not_complete`. The pending
gates are the Stream-equivalent completion certificate and title binding,
rights, condition, preservation, registrar review, and independent exact-head
review. No title, copyright assignment, unrestricted display or publication
right, legal opinion, preservation completion, technical completion, signed
authority, or `accessioned` lifecycle transition is asserted.

The public dossier now includes a sourced Casey Reas artist/practice profile,
a collection essay, and dated object-specific static/live observations on all
seven object pages. These distinguish documented fact, artist or platform
statement, time-specific static documentation surrogate, live generator
observation, and Museum interpretation. The seven raw public metadata files
remain byte-identical to the pre-change Casey branch and retain their manifest
binding. The immutable source/publication evidence remains bound to source
commit `9700e842d0c991280b476cc67849d966221a742a`, publication commit
`bf70ba3fd888d2d1b8add90fe56e913102f8aa68`, package SHA-256
`sha256:c08749355ea12c2948efdfdeb232675ab4bf693976a94c6ebb4ce24b0b5d08ab`,
and release SHA-256
`sha256:d05f75c65c0af0172a0a2f2207693e4211d5c0f4f69fad8d4907ebd90e12470e`.

Before local commit, regenerate the governed manifest and run fetch guard,
complete validation, package verification, and the diff check. The full
discovered unittest suite has already passed: 80 tests, one expected Windows
named-pipe skip.
## 2026-08-01 - PR #2 post-PR #15 Casey-pin integration checkpoint

PR #15 is merged on `origin/main` as
`bf70ba3fd888d2d1b8add90fe56e913102f8aa68`. Its reachable publication
boundary stays `published_source_commit`
`9700e842d0c991280b476cc67849d966221a742a`; the historical Casey construction
provenance remains immutable. PR #2 merges that exact mainline before its
independent exact-head review.

PR #2 changes the governed `tests/test_control_plane.py`, which is deliberately
one of the Casey package's closed external inventory inputs. The reproducible
package builder therefore regenerates only the package inventory and
`latest-run.json` pointer to bind that new test byte. It does not change the
79 raw observations, five snapshots, five descriptor outputs, 3,300-token
population, 35,088 traits, source/canonical ordering, exclusions, warnings,
review-null state, or accession/rights/curatorial status.

The V1 contract specification remains a non-deployment design. Its
TargetRelease signature fixture, URI lifecycle harness, vectors, Stream
bilateral compatibility gate, and immutable wrapper/registry requirements do
not constitute a deployed contract, released TargetRelease, Stream
owner-record mutation, accession, or authorization for a network write. The
next gates remain final local validation, exact-head CI and independent
protocol review, governance approval, a release-evidence rehearsal, and a
separately reviewed implementation and audit.

## 2026-08-01 - PR #2 current Casey toolchain-manifest revision

The immutable historical PR #15 publication remains main commit
`bf70ba3fd888d2d1b8add90fe56e913102f8aa68` with package-manifest SHA-256
`sha256:c08749355ea12c2948efdfdeb232675ab4bf693976a94c6ebb4ce24b0b5d08ab`.
It is not rewritten by this branch. Its reachable
`published_source_commit` remains
`9700e842d0c991280b476cc67849d966221a742a`.

PR #2's governed `tests/test_control_plane.py` evolves the current verification
toolchain. The Casey package therefore has a new current toolchain-manifest
revision, SHA-256
`sha256:fd2da3c8227e8077a22a651507d5537c01915e61d58c9e71488dcb1203929d72`,
with a regenerated `latest-run.json` pointer. This revision binds the evolved
toolchain input; it is not an art-data, accession-authority, or historical
release rewrite.

The integration proof is a closed evidence-path diff against
`bf70ba3fd888d2d1b8add90fe56e913102f8aa68`: only
`package-manifest.json` and the excluded `latest-run.json` pointer may differ
under `evidence/casey-reas-collection-snapshots/`. Thus every raw observation,
snapshot, descriptor and result, reconstructed request, exclusion, warning,
population, and child run-manifest byte remains unchanged. The Casey verifier
also checks the preserved raw bytes, snapshots, and child manifest against the
reachable publication commit and recomputes all five descriptor outputs.

## 2026-08-01 - PR #2 offline vector/ABI checker toolchain amendment

The immutable historical PR #15 publication remains
`bf70ba3fd888d2d1b8add90fe56e913102f8aa68` with Casey package-manifest
SHA-256 `sha256:c08749355ea12c2948efdfdeb232675ab4bf693976a94c6ebb4ce24b0b5d08ab`.
Its `published_source_commit`
`9700e842d0c991280b476cc67849d966221a742a` remains unchanged. This amendment
does not rewrite that publication.

PR #2 adds an offline active-manifest/ABI-selector checker and wires it into
the governed control-plane test. The resulting current Casey toolchain-manifest
revision is `sha256:76fe8e967ca9e4da87497b063c3873effa5b85a1d838a222a4bb9560e5f81842`.
It supersedes only this branch's current toolchain pointer, not any historical
art-data release or accession authority. The closed Casey evidence-path diff
continues to allow only `package-manifest.json` and excluded `latest-run.json`
to differ from `bf70ba3...`; raw observations, snapshots, descriptors/results,
requests, exclusions, warnings, populations, and child run manifest remain
byte-identical.

The new checker is offline and independently recomputes the active §13.6
`ff1c5825...` / `0x8bb17fc4...` vector plus the canonical ABI and authorization
allowlists. The state-only HTTPS audit rule is clarified without adding any
network, target-admission, deployment, accession, or migration behavior.
Independent protocol review is still evaluating potential batch-gas and
immutable-target-policy contradictions; this candidate must remain unpushed
and draft pending its exact evidence and disposition.

## 2026-08-01 - PR #2 consolidated protocol-remediation toolchain amendment

The immutable PR #15 Casey publication remains main commit
`bf70ba3fd888d2d1b8add90fe56e913102f8aa68` with package-manifest SHA-256
`sha256:c08749355ea12c2948efdfdeb232675ab4bf693976a94c6ebb4ce24b0b5d08ab`.
Its reachable `published_source_commit` remains
`9700e842d0c991280b476cc67849d966221a742a`. It is historical release
evidence and is not rewritten.

The current PR #2 toolchain-manifest revision is
`sha256:443c412cde107af915c1719e4d2bd2c767ae8fdf9e597cd6e2b8210a7fe654bb`.
It is a governed test/toolchain evolution that binds the expanded offline
control-plane checks; it is not a new art-data release, accession authority,
or deployment claim. The only Casey evidence-tree differences from the
historical PR #15 baseline are `package-manifest.json` and the excluded
`latest-run.json` pointer. Every raw observation, snapshot, descriptor,
descriptor result, reconstructed request, exclusion, warning, population, and
child run-manifest byte remains unchanged; the verifier reproduces 3,300
tokens, 35,088 traits, 79 raw files, and five descriptor outputs from the
reachable publication boundary.

The local, unpushed protocol remediation now makes the batch caller gate
internally satisfiable without calling it a measured gas bound; separates
strict canonicalizer purity from stateful-target non-upgradeability; binds
TargetRelease evidence and identity to the exact target address; derives
release identity before D0/D1 projections; admits exact predecessor/reason
commitments; rejects URI textual aliases; and scopes successor import to a
future V2 interface. The complete TargetRelease fixture is explicitly
non-deployment conformance evidence. Casey remains a completed, received
donation with accession documentation in progress, not an accession-complete
claim. This candidate remains local and draft pending the final validation
pass and reviewer direction; it must not be pushed yet.

## 2026-08-01 - PR #2 executor/dependency remediation toolchain amendment

Correction to earlier in-progress wording: commit `8a2e26a` was pushed to PR `#2`
and the PR was marked ready before this follow-up review began. Statements
above that described the earlier candidate as unpushed/draft remain historical
status at their observation times. The remediation after `8a2e26a` is local
and unpushed, and this task does not mark the PR ready, merge it, or push it.

The immutable PR #15 publication remains main commit
`bf70ba3fd888d2d1b8add90fe56e913102f8aa68` with package-manifest SHA-256
`sha256:c08749355ea12c2948efdfdeb232675ab4bf693976a94c6ebb4ce24b0b5d08ab`
and reachable `published_source_commit`
`9700e842d0c991280b476cc67849d966221a742a`. It is not rewritten.

The complete current-pointer lineage is explicit:

Supersedes (toolchain pointer only):
`sha256:c08749355ea12c2948efdfdeb232675ab4bf693976a94c6ebb4ce24b0b5d08ab`
-> `sha256:fd2da3c8227e8077a22a651507d5537c01915e61d58c9e71488dcb1203929d72`.

Supersedes (toolchain pointer only):
`sha256:fd2da3c8227e8077a22a651507d5537c01915e61d58c9e71488dcb1203929d72`
-> `sha256:76fe8e967ca9e4da87497b063c3873effa5b85a1d838a222a4bb9560e5f81842`.

Supersedes (toolchain pointer only):
`sha256:76fe8e967ca9e4da87497b063c3873effa5b85a1d838a222a4bb9560e5f81842`
-> `sha256:443c412cde107af915c1719e4d2bd2c767ae8fdf9e597cd6e2b8210a7fe654bb`.

Supersedes (toolchain pointer only):
`sha256:443c412cde107af915c1719e4d2bd2c767ae8fdf9e597cd6e2b8210a7fe654bb`
-> `sha256:2b41d542c71d7c2517611efbbd2ad363686a24e223f955fb9f685da3f75718a1`.

The new 65,519-byte package manifest is a governed test/toolchain revision for
the executor/dependency, URI, TargetRelease, Casey-pointer, and optimized-mode
checks. The only Casey evidence-tree differences from the immutable PR #15
baseline remain `package-manifest.json` and the excluded `latest-run.json`
pointer. Every raw observation, snapshot, descriptor, descriptor result,
reconstructed request, exclusion, warning, population, and child run-manifest
byte remains unchanged. This is not a new art-data release, accession
authority, TargetRelease admission, deployment, or network-write claim.

## 2026-08-02 - PR #2 Casey pointer-verifier test amendment

Supersedes (toolchain pointer only):
`sha256:2b41d542c71d7c2517611efbbd2ad363686a24e223f955fb9f685da3f75718a1`
-> `sha256:fc8d7c19f1831edfc274fa35a4c98ebe6aa4774156c03b6ec9981c40bd8010ba`.

This final 65,519-byte toolchain-manifest revision factors the
`latest-run.json` package pointer check into a directly mutation-tested
verifier function. It requires the exact `package-manifest.json` path, measured
byte size, and measured SHA-256. The immutable PR #15 publication, reachable
`published_source_commit`, and all art/source/snapshot/descriptor/result/
request/exclusion/warning/population/child-run-manifest bytes remain unchanged.
The revision is local and unpushed and is not an art-data release, accession
authority, TargetRelease admission, deployment, or network-write claim.

## 2026-08-02 - PR #2 exact-threshold and emergency-independence remediation

Independent exact-head protocol review found five genuine design
contradictions after head `2f6517c`: the mutable authority provider could veto
the claimed emergency path; authority/executor rotations could leave their
cross-bound capability rows stale; the stated 2-of-3 release policy required
three valid signatures; the SHA-1 repository tree OID lacked a reproducible
`bytes32` encoding; and the selector table referred to a forbidden
governance-executor grant.

The local remediation excludes `freezeWrites` and post-freeze `setSuccessor`
from the provider selector set. Their authorization now uses only the
registry-held direct executor address/revision, while successor evidence still
must have been admitted before freeze. The provider-mediated selector-set hash
is `0xe4b26f95f96aa2744535537bbd3c6769693127a9315162ca1d63bffe2fa6a5ff`.
Both rotation directions atomically refresh `AuthorityState` and
`GovernanceExecutorState`; authority rotation emits the new
`GovernanceExecutorAuthorityRebound` audit event.

Release evidence now admits three sorted addresses but carries exactly two
sorted signature entries from that set, both of which must recover. The bundle
schema hash is
`0xff21eb38d2c75ee54155020e7ed88fb1b952963cd8c889b6bb771b9366fb29a3`;
the evidence-schema hash is
`0x57027a81db3fea11b211564ba7381273f6171df37d3621ceb6ab3959e27f996f`.
The regenerated non-deployment vector has release ID
`0x7d3cf4d1cc5a540e950b98c52138a6a75d9e747edf365602af12729adda1a522`
and 837-byte bundle hash
`0x76db1ca68ab4561ad0e6b193d85e853494ea3984010ace8de8369a685efb74c1`.
Git commit and tree SHA-1 values now share one exact encoding: decode the
40 lowercase hex characters and right-align those 20 bytes in `bytes32` with
12 zero high bytes. The Stream-mirror selector table now names the direct
executor closed binding and expressly forbids an executor grant row.

The same local pass pins the sole `NONE` content commitment, adds a measurable
per-URI assertion-capacity deployment gate, and binds the batch-gas checker to
the specification constants/formula. All seven focused harnesses and their
optimized-Python rejection controls pass. Full regeneration, full validation,
fresh exact-head review, CI, and bot disposition remain required. Nothing in
this entry is a deployment, TargetRelease admission, network write, donation
acceptance, or accession-completion act.

## 2026-08-02 - Stream draft owner-record evidence correction

Independent review identified an overstatement in the earlier Stream premise.
At pinned commit `5021c8060950c3fef995271e674ed4b2007fee6d`, Stream's design
document does publish the `OwnerRecord` shape, five owner-record function
signatures, the owner-write and nonce-revocation EIP-712 typehashes, and the
`6529StreamOwnerRecords` domain. The source tree still does not include a
`StreamOwnerRecords` implementation or deployment, and the design document
does not pin an exact stored `recordHash` preimage and read surface.

The local specification now matches the real draft ABI and EIP-712 envelope
bilaterally. Its executable checker recomputes all five selectors, both
typehashes, and a synthetic domain/struct/signing vector. The synthetic module
address is explicitly not a deployment claim. The convergence gate remains
closed pending source, deployed runtime, stored-hash semantics, read ABI,
nonce behavior, and a successful direct/relayed write-read rehearsal. Full
regeneration, validation, exact-head review, CI, and bot disposition remain
required.

The complete local gate subsequently passed on this remediation: bootstrap
validated 226 JSON files; the network-fetch guard passed; all 79 tests passed
with the one expected Windows named-pipe skip; schema, reference, state,
guardrail, and commitment validation passed; the deterministic release
manifest check passed; the Casey evidence package reproduced 3,300 tokens,
35,088 traits, 79 raw files, 3,327 request records, and five descriptor
outputs; and `codex-diff-check` reported no whitespace defects. These local
results do not substitute for fresh exact-head CI or independent review.

## 2026-08-02 - Stream token-subject derivation remediation

Independent Stream review of pushed head `1f2dc03` confirmed the corrected
draft-versus-deployment boundary but found that the synthetic owner-record
EIP-712 vector still supplied a free-form subject. The pinned Stream draft
requires every token-scoped owner record to derive `subjectId` as
`keccak256(abi.encode(STREAM_SUBJECT_TOKEN_V1, chainId, streamCore, tokenId))`.

The local remediation now pins
`STREAM_SUBJECT_TOKEN_V1 =
0x1e576f27850d12bc1ec9255ca277dbecfbc84fb3a9a34c474640dfca89811d7e`,
uses explicitly synthetic Core `0x0000000000000000000000000000000000001001`,
and derives subject
`0x7839d73dfe2384e7818fa90691f4ffa27260eb4af0cfe50f8d1615f8bf6db5b4`
for chain ID `1` and token `771769`. The recomputed owner struct hash is
`0xfb71d60a68e0894166ae306df4fd11238530ee87e5714aa5d8c3e990fb6506f6`
and signing digest is
`0x1fe370911b6eda46ee6153458ffeac7bdc2c0c7fd7e9fb0af6d7385e66df2605`.
The checker, specification, Stream profile, and two independent transcripts
bind the same derivation. The synthetic addresses remain non-deployment test
inputs. Regeneration, full validation, a new pushed head, and fresh exact-head
review are required.

## 2026-08-02 - closed authority selectors and governed release attestors

An exact-head adversarial review found two additional protocol contradictions
after CI was green. First, `admitStreamOwnerRecordInterface` and
`admitHttpsResolverProfile` normatively required active provider capability but
were absent from the closed selector commitment. Second, the release evidence
proved 2-of-3 only over addresses declared by the evidence itself; substituting
three attacker-controlled keys and recomputing signatures remained valid under
the old checker and retained the same release ID.

The remediation makes both trust boundaries explicit. The closed authority set
now includes the two required admission selectors and the new attestor-bound
`admitTargetRelease` selector. The independent release-attestor policy artifact
has a schema, exact 2-of-3 signer list, governance-approved deployment-manifest
authority source, and new-registry-only rotation rule. Its JCS policy hash and
ABI signer-set hash are immutable constructor commitments, public registry
getters, TargetRelease row fields, and inputs to `releaseId`. Evidence and
bundle checkers must equal the external policy, not merely a self-declared
address array; key/policy/set substitutions are negative tests. The checked
file is explicitly a public non-deployment fixture. A real deployment must
replace it with a governance-approved production policy and bind the resulting
commitments in both constructor and release manifest.

## 2026-08-02 - runtime attestation and Stream readback closure

Exact-head independent review of `cf6ff24` found two substantive remaining
gaps, so that head was not merged. First, the 2-of-3 release review existed in
the evidence package but was not unavoidable inside `admitTargetRelease`.
Second, a mirror-link caller could still supply a Stream subject and
owner-record hash without a mandatory adapter readback tying both to the
admitted Stream deployment.

The local remediation makes release approval a registry-enforced EIP-712 gate.
The domain binds chain ID and registry address; the exact struct binds release
ID, D0 conformance hash, D1 signed-document hash, and the immutable policy and
signer-set commitments. Admission accepts exactly two sorted governed signer
addresses and their 65-byte canonical signatures, recovers both on-chain, and
stores the digest, signer addresses, signature commitments, and signature-set
commitment. The deterministic vector now has release ID
`0x118d59bded209701cb211f4515fff0935c96fa4d2aa50d42e0a749d45c0eca85`,
attestation digest
`0xac389ba1bd808d6bb58087be65d31fcbe9ce9593d503a1a267f1aa0d80be5bc3`,
and signature-set hash
`0x8a1d8004d16e0b3de6f7d242a3cfad1e40740d517003d9ab827697e7452db555`.
Its 1,300-byte detached bundle hash is
`0xbc553ca1ffb482755bea510253a73b941dd81b5c313dce82267f6915ca75f70b`.
The executable runtime model rejects missing, duplicate, out-of-order, or
unauthorized signers; altered signatures; changed release/document/policy
fields; and cross-chain or cross-registry replay.

Stream interface admission now binds exact Core and adapter addresses plus
both runtime hashes, domain, vector, and evidence. Mirror-link creation accepts
only the Museum subject, token ID, and expected-hash guard; it rechecks both
runtimes and reads the adapter's Core, domain, vector, collection, derived
subject, and owner-record hash with exact-length bounded calls. It independently
reads Core token-collection identity and requires the Museum subject to be the
registered CAIP-19 identity for the exact chain/Core/token. A new ninth
network-free checker rejects swapped Museum subjects, nonzero adapter collection
substitution, and substitution of every other readback field. The three
changed governed selectors produce closed selector-set hash
`0x4c2a05297ef36555d0bd199b80df1463d02702f6bd1bde9444960279d15957e5`
and therefore new executor binding commitment
`0x40a3c47c9686f82852e14e2b503ff9e02cdbed30d556db7347112bec4061e3f9`.

Focused conformance scripts pass locally. Full regeneration, repository-wide
validation, a new exact head, fresh CI, and fresh independent/bot review remain
required. Nothing in this entry authorizes deployment, a network write, or a
completed accession.

## 2026-08-02 - Museum-subject and Core-collection mirror binding

Exact-head reviews of `eff5811` agreed that release-attestation enforcement
was closed but found two remaining Stream mirror gaps. A valid Stream token
could be linked to the wrong already registered Museum subject, and the model
treated any nonzero adapter collection ID as valid instead of comparing it to
an independent source. That head was not merged.

The local remediation now reconstructs the exact lowercase
`eip155:<chainId>/erc721:<streamCore>/<tokenId>` string, checks its hash and
`MUSEUM_ASSET_PROFILE_CAIP19_V1` row, recomputes the Museum external subject,
and requires equality with the caller's `subjectId`. It also calls the pinned
Stream Core `tokenCollectionIdentity(uint256)` selector `0xa6b638c9` directly,
requires an existing unburned mapping with nonzero collection and serial, and
requires the adapter's independently returned collection ID to equal the Core
result. The retained vector now rejects a wrong existing Museum subject, a
changed token/canonical asset, nonzero adapter/Core collection disagreement,
absent/burned tokens, zero serials, and truncated Core or adapter return data.

Focused harnesses and the full 79-test/validator/Casey-verifier regression pass
are green locally. A regenerated exact commit, push, CI, and fresh independent
reviews are still required; no superseded-head approval counts.

## 2026-08-02 - exact-head control-plane review remediation

CodeRabbit's review of the PR `#2` candidate exposed nine live controls that
were not waived: complete Stream owner-record event/chain/pointer surfaces;
exact canonical Git origin matching; one-read Casey package binding;
canonicalizer gas/input/return bounds; immutable HTTPS address-list evidence;
exact ERC-1271 magic-value handling; historical record-type/family/grant
authorization revisions; and a truly closed dependency external-capability
set. The remediation is in progress and no earlier approval counts.

The dependency policy now rejects `BALANCE`, `EXTCODESIZE`, `EXTCODECOPY`, and
`EXTCODEHASH`; its JCS hash is
`0xf8efb731af735014514f4a5b8ad22a6e2007ba23b11b45a9c8845db3f144ee2c`.
The regenerated non-deployment TargetRelease vector supersedes the earlier
synthetic values with release ID
`0xdeb8472c3dfa2af9d997baf62026478c0cf5b4b8439ac94cdda47a48ac4b48e0`,
attestation digest
`0x682aae357582c8d22cd11f69c58abc9d62ef5847e5b1cd916564768a733a688d`,
and bundle hash
`0x26f70f9a77520b8210eae127c167edeed42f37e25a34abfbd213b02f6d6c6e09`.
The canonicalizer policy now pins 100,000 gas, 4,096 returned bytes, and a
2,048-byte canonical asset ID. Exact-head validation, commit, push, CI, bots,
and independent reviews remain required.

The two independent `d44c559` protocol reviews then converged on one further
P1: Stream's `tokenCollectionIdentity` exists during
`PREPARED_INCOMPLETE`, before an ERC-721 exists, and that prepared identity can
be aborted. The local gate now also calls Core `tokenLifecycle(uint256)`
(`0x8c46d901`), requires its exact 32-byte ABI result to be `MINTED (2)`, and
rejects unknown, prepared, burned, and malformed lifecycle results. The
complete local candidate passes bootstrap over 228 JSON files, fetch guard,
all nine conformance harnesses and optimized-Python rejection, 79 tests with
one expected Windows named-pipe skip, full validation, deterministic manifest,
Casey replay (3,300 tokens, 35,088 traits, 79 raw files, 3,327 requests, five
descriptors), and `codex-diff-check`. A committed exact head and fresh review
remain required.

## 2026-08-02 - evidence-hash amendment and inert activation design

Append-only amendment: the evidence-schema hash
`0x57027a81db3fea11b211564ba7381273f6171df37d3621ceb6ab3959e27f996f`
appearing in an earlier working checkpoint is stale and MUST NOT be used. It is
superseded by the canonical governed hash
`0xff380ff5d024aa7bf60a067141efa6302e679a448054b3109bd05ac8ea5623ce`.
This amendment changes no checked manifest or fixture; it only makes the WIP
history's supersession explicit.

Exact-head review of `5afcbe7` found that constructor verification of
registry-address-bound EIP-712 signatures is circular when those signature
bytes are themselves part of CREATE2 init code. That head was not merged. The
specification now requires a target-address/signature-free inert constructor,
an address-independent initial-authority artifact commitment, and a one-shot
post-deployment `activateInitialAuthority` transaction. Initialization states
`0`, `1`, and `2` are explicit; all other mutators reject states `0` and `1`;
activation sets state `1` before any external call and state `2` last; and any
failure rolls all release, dependency, authority, and executor writes back to
state `0`. The fully registry/chain-bound 2-of-3 release signatures are made
only after the actual deployment address exists. Fresh regeneration,
validation, exact-head review, CI, and merge remain required.

## 2026-08-02 - PR #10 post-protocol-foundation sync checkpoint

The Casey accession branch merged the independently reviewed protocol
foundation from `origin/main` at
`67d8528511917bd6b06a2c9c4bfe4a0b7445034d`. The append-only PR #10 and PR #2
WIP histories were both preserved; generated Casey package and repository
release manifests are being regenerated from the merged source bytes rather
than selecting either stale side of the merge.

The formal Gift Acceptance and Accession Authorization remains bound to the
seven exact CAIP-19 identities, their shared receipt transaction and log
indices, adopted Art Blocks donation preapproval, adopted Donation Acceptance
Policy, donor credit `punk6529`, no consideration, and permanent-collection
intent. The accession lot and all seven objects remain `received_onchain` /
`not_complete`: this sync does not create a title instrument, copyright or
display-right grant, legal conclusion, condition conclusion, preservation
completion, registrar sign-off, independent review, or
`STREAM_ACCESSION_V1` completion event.

The artist/practice profile, five-project collection essay, and seven distinct
object pages remain the current curatorial construction. Their claim-level
source boundaries, immutable-versus-mutable technical distinctions,
923-combinations/924-artworks distinction, 2021/2022 Phototaxis source
conflict, transparent non-market descriptors, and no-rarity/no-value posture
remain unchanged. Full package regeneration, validation, commit, push, exact
CI, specialist review, and independent exact-head approval remain required.

## 2026-08-02 - 923 EMPTY ROOMS edition-language correction

Independent exact-head curatorial review of `7893dd9` found that the machine
object record's phrase “Public edition: 924 unique artworks/tokens” exceeded
the source boundary already enforced in the research dossier and public
scholarship. Art Blocks and Bright Moments report an edition size of 924 and,
separately, describe 923 unique rooms or combinations; the reviewed sources do
not explain the relationship between those figures. The object record now
preserves those two source statements separately, identifies the accessioned
work only as native token `#713`, and adopts no reconciliation theory. The
exact checker has been updated to require that source-limited formulation.

The object payload SHA-256, envelope Keccak content commitment, and governed
release manifest were regenerated after the correction. Targeted Casey
validation, commitment refresh check, full Museum/Casey validation, all eight
Casey dossier-control tests, deterministic-manifest check, and whitespace
check pass locally. The correction requires a new committed head and complete
fresh exact-head CI and independent review; no approval of `7893dd9` carries
forward.

## 2026-08-02 - Casey generic-schema and raw-receipt evidence remediation

Advisory GLM review of `ff8fd6b` found two valid documentation-control issues:
the Casey control note repeated its immutable-evidence paragraph, and the
nominally generic public-inventory schema required exactly seven entries. The
duplicate paragraph is removed. Public-inventory and transaction-provenance
schemas now accept arbitrary non-empty Museum lots while generic semantic
checks enforce object uniqueness, transfer-count equality, exact receipt-log
projection, and one museum-receipt event per object. Behavioral tests exercise
a valid one-object schedule and reject count and log mismatches.

Independent Einstein review of the same head demonstrated that a Casey object
record's contract, token ID, and CAIP-19 could be changed coherently and
recommitted without being compared to the accession lot. It also found that
the `direct_rpc_verified` receipt assertion retained conclusions but not the
raw provider response bytes and acquisition metadata. Both findings are
accepted. The dossier now retains and content-addresses the exact
`eth_getTransactionReceipt` response for transaction
`0xbdde33b32d4b70335b10cbd37c0b00a027844f14c900d82aa4f75b7a7b390498`
and a separate request/acquisition artifact identifying the provider,
transport, method, parameter, client, HTTP result, byte hash, and limitation
that this is one-provider evidence rather than an RPC quorum.

The Casey validator decodes all nine receipt logs, requires seven ERC-721
`Transfer` logs and two `Approval` logs, and joins every transfer's contract,
token ID, source, destination, and log index to the accession identity
schedule. It then joins that schedule bilaterally to the formal gift
authorization, provenance schedule, seven work records, visual-observation
record, and public inventory. The raw receipt and acquisition artifacts are
also bound in the provenance record, preservation manifest, lot, and seven
object fixity fields. Mutation tests now prove rejection of a coherently
rewritten object identity, an altered raw transfer token, and altered RPC
request metadata. The original source limitation remains explicit: the raw
receipt proves Ethereum event/custody facts, not donor identity, legal title,
rights, tax treatment, or accession completion.

This remediation invalidates all earlier PR #10 exact-head approvals. Package
and repository manifests, CI, specialist bots, and independent reviewers must
all run again on the next committed head before merge.

## 2026-08-02 - Casey accession substantive finalization checkpoint

The Casey lot is no longer represented as an intake dossier awaiting a future
reviewer. The current candidate makes and records the Museum's decisions:
title to the seven tokens and the donor's full transferable interest is
accepted; Casey REAS's copyright remains separate; the object-specific Art
Blocks metadata supports the complete conditional CC BY-NC 4.0 Museum-use
matrix; the seven objects and lot are accessioned; and the curatorial,
registrar, condition, technical, display, and preservation findings are stated
in final public and machine-readable records.

The technical conclusion is `pass_with_conditions`. Exact token/custody
identity and retained metadata fixity are green. The official generator routes
were available and all seven produced changing output, so generator, render,
dependency, behavior, documentation, and preservation findings are amber
rather than red. They are not green because the Museum has not yet retained
self-contained generator/dependency packages, complete interaction evidence,
or two-environment reproducibility. Those are concrete active collection-care
actions; `technically_verified`, `preservation_complete`, and unconditional
`display_ready` remain later stricter states without reopening accession.

The package now includes an accession certificate, title/rights determination,
technical/condition review, curatorial decision, lot-level rights schedule,
seven reviewed rights statements, seven reviewed condition reports, executed
object-level title bindings, exact on-chain custody paths, a research-note
resolution addendum, and a deterministic finalization script. The finalizer is
idempotent and `--help` is non-mutating. Generic validators now fail closed on
multi-object custody joins, malformed duplicate projections, malformed visual
frames, and retention contradictions. Casey-specific controls reject any
reversion to intake status, unspecified rights, placeholder title material,
or a pending preservation list.

Local verification at this checkpoint is green: full Museum/Casey validation,
bootstrap validation over 276 JSON files, fetch guard, deterministic manifest,
whitespace check, Python compilation, and 59 unit tests with one expected
Windows named-pipe skip. After final record generation, the deterministic
release manifest commits to Keccak-256
`0x6480dbc430cf80f2f499fd1898892d1597918913ea3b2f0027a57e7340cb28f9`
and SHA-256
`5bf026405e3c6de8755ad1331151c56d0f18e3ff9417f6d7087f0593db2df37a`.
Independent technical review, immutable exact-head URLs,
PR bots, CI, and maintainer review must target the new committed head; earlier
approvals do not carry forward.

## 2026-08-02 - Exact technical facts and chronology correction checkpoint

Exact-head registrar review of commit `05eb786b4ed1ac5f8093cff8f038d5f2923b010d`
rejected two residual contradictions: invented millisecond offsets in the
accession event chronology and canonical discovery pages that still described
the superseded intake state. Both are corrected in the next candidate.

The accession certificate now retains the Ethereum receipt at
`2026-08-01T13:25:47Z`; acceptance, acquisition, and title passage share the
actual `2026-08-01T22:55:00Z` institutional timestamp; and the later reviewed
custody registration is dated `2026-08-02T06:30:00Z` while binding the earlier
source occurrence explicitly. The generic validator permits co-temporal events
but still rejects time moving backwards. No administrative timestamp is
presented as the time of the on-chain transfer.

The technical record now binds each exact generator-response SHA-256,
dependency version, and complete source-reviewed interaction map. For 923 EMPTY
ROOMS, the retained population and reviewed generator establish 924 invocations
numbered 0–923, separate invocation-zero code `999999`, the documented 1–923
combination sequence, and #713 code `555536`; no artistic meaning is assigned to
invocation zero. For Ex Nihilo (Cosmos), the record preserves the generator's
lowercase `r`/`b` implementation and duplicated lowercase comparisons against
the platform's uppercase `R`/`B` instructions as an amber behavior/documentation
discrepancy. Mutation tests reject changes to hashes, dependency versions,
controls, automatic behavior, count structure, and discrepancy disclosure.

The top-level README, repository index, standards crosswalk, and collection
essay now state the completed accession and distinguish it from still-active
software preservation. The governance basis separately binds the authenticated
Wave API `drop_type=WINNER` observation to the reviewed governance register and
states that rating totals do not determine effect.

Local verification after these corrections: Casey dossier validation, bootstrap
validation over 276 JSON files, full control-plane validation, 48 generic tests,
and 11 Casey tests pass; the only skip is the expected Windows named-pipe test.
The finalizer is idempotent.
The corrected deterministic release manifest commits to Keccak-256
`0xd9a06e653d2124c93e2ab14f3d8699c7fed2589ed8fa2d8e60592eabb722c37b`
and SHA-256
`771414c47e784d2a93a1d484481ad19a0dec8e2448661a63486fad56412f7383`.

A separate durable Codex task, `019fc14e-8e9a-73a3-8213-2f4eddc077bf`, is
building the Museum section in the 6529 Evolve monorepo from fresh remote main.
Its scope is a GitHub-release-backed public Museum interface with immutable
manifest verification and a source adapter designed to switch to Ethereum
records later, followed by PR bots, maintainer merge, and post-merge validation.

## 2026-08-02 - Immutable and append-only release-hardening checkpoint

The candidate now pins every GitHub evidence URI inside committed Casey record
payloads to exact source commit `823586e89c365dff26ef598140ef856f96dcd501`;
only envelope discovery URIs remain live. The final validator rejects mutable
`blob/main` and `tree/main` payload evidence links. Rights amendments,
condition reassessments, and object state transitions are append-only,
deterministically identified, and linked to the assertions they supersede.
The completed accession cannot be rewritten by the legacy intake commitment
refresher; that tool now refuses the operation and directs maintainers to the
reviewed finalizer and full validator.

The accession register finalizer is revision-generic and idempotent. It creates
a successor only for a material payload change, preserves prior amendment
history, records the real `2026-08-02T06:30:00Z` revision-three construction
time, and leaves an existing review intact when the payload is unchanged. A
generic control rejects current revisions constructed before their latest
supersession and rejects incomplete or unordered revision histories.

The Casey authority validator now requires exactly the adopted Art Blocks
preapproval `1052156` and Donation Acceptance Policy `1052812`, once each,
including their decision, drop, serial, and source identities. Mutation tests
prove that substitution with another valid Wave winner, omission, and
duplication all fail closed. Additional malformed-input tests cover missing
evidence paths, null reviewers, empty object histories, mutable evidence URLs,
and unhashable accession/provenance identities without validator crashes.

The public collection essay, canonical repository index, and dated research
record now distinguish the historical intake state from the completed
accession. The rebuilt 175-file Casey package commits at
`sha256:e76f18901101efda51361bda30ce22b57a87b9d60e1c21bd4ed2c66c1b41a22d`.
The final hardening pass additionally binds the reviewed title instrument bytes
across the lot, certificate, title-passage event, seven object records, and
seven rights records; binds every condition report to the controlled visual
observation bytes; rejects malformed stewardship-action entries; makes public
page finalization assert the completed state; and removes the obsolete
intake-stage validator and its dormant test corpus. The deterministic Museum
release therefore commits at Keccak-256
`0x072e076dad777042af9bae7569ce3035cd0abeb892d6623949333e6e1deb4eea`
and SHA-256
`217b2597f2a687c8c00b9fcde6fda99402f838e277f327597b0eab3251d00fdd`.
The CI-equivalent discovery suite passes 96 tests with one expected Windows
named-pipe skip; full Museum/Casey validation, package verification, fetch
safety, compilation, deterministic-manifest checking, and whitespace checking
also pass. Independent reviewers Turing (`019fc04f-6d34-7242-992f-3de8ff2b6346`)
and Einstein (`019fc04f-7397-7a30-86b0-65fe1944f27d`) approved exact committed
head `514cb18aee37b0d04c3eeb59703b411ea34f6bf9`; both recomputed the title and
visual-observation byte joins and found no release blocker. The register review
records Turing's documentary-QA approval at `2026-08-02T08:39:53Z`, bound to
payload SHA-256
`0bd254e59ae0dfb60018914c8df55ab7aa76317ac9dfc520737430f5f731409f`.
Adding that review envelope does not change the reviewed register payload; it
does produce the final repository release commitments: Keccak-256
`0x5c9471e01cb0b4b0a84424388df3be3e0214d839ee48db87cfc05f0a3f61d2b2`
and SHA-256
`e459c8e3bf4f19263b50cd27c8481078de85dee1a719715491fdd58d0dd5e12b`.

## 2026-08-02 - Final factual-integrity remediation checkpoint

Luna's exact-head variance review identified seven remaining documentary
integrity defects after the earlier approvals: custody had been mislabeled as
an offer; one certificate link did not bind the current accession-lot bytes;
the descriptor ledger still said review was pending; INDEX statuses
contradicted reviewed records; preservation actions admitted null entries;
generator findings came from finalizer constants rather than an independent
evidence object; and records retained a research head superseded by the
923/924 correction.

The next candidate resolves all seven in substance. Object lifecycle histories
now begin offered only when the donor declaration substantiates the offer, at
`2026-08-01T22:55:00Z`; the earlier Ethereum receipt remains a separately dated
custody fact. The acquisition certificate binds the exact accession-statement
bytes by immutable Git blob URI and SHA-256. The descriptor ledger is
`complete_reviewed`, records two exact-head reviewers and five per-output
approvals, and is enforced by the dossier validator. INDEX labels now match the
reviewed records. The accession-lot schema closes and types the preservation
manifest, and Casey validation requires the exact four substantive stewardship
actions, so null or placeholder substitution fails closed.

Generator findings now originate in the separately retained,
manifest-bound `evidence/casey-reas/generator-observations.json` transcript.
The finalizer and validator load it independently; the validator also pins its
reviewed SHA-256 and requires every object and condition report to bind that
exact transcript. The transcript expressly preserves the absence of raw
generator bytes and therefore does not overstate autonomous preservation.
Corrected art-technical and on-chain research bytes are hash-bound at commit
`951f5afb95c511adaf879d017c662046ff6365b5`; superseded head
`9f38bd4ba5f779540eabf2dfce019cc1382561e2` is rejected in canonical payloads.

Focused negative controls now cover false offered chronology, an unhashable
accession-lot citation, null preservation actions, mutated generator evidence,
and a cleared descriptor review. Sixty-five focused tests pass with one
expected Windows named-pipe skip; the 175-file Casey package verifies with
SHA-256
`2b2e7ce8897688fa8fde9137cf8f0c361e420d0799b6fbb9b6bfb5fa4d7c6299`.
The candidate deterministic release before the final Git-blob URI hardening
committed at Keccak-256
`0xe5325c93e7bc12910909af1399551c95e3d2829a6b7ee5b0bfc03795694cd3cf`
and SHA-256
`36e069cbb1e9c20b000922605f8093907c9a8db560006b3c179fb43c13174471`.
These values are retained as an intermediate checkpoint, not the release
authority. The current commitments are always the values in
`release-artifacts/latest/record-manifest.json` and must be approved against the
resulting exact head.

## 2026-08-02 - Post-accession diligence and final completeness remediation

The final audit rejected three forms of apparent completion: a Casey section in
the on-chain migration specification still described intake-stage gates; the
live ACCESSION_LOT and WORK_DESCRIPTION schemas admitted undeclared nested
fields; and one historical control-plane WIP note was omitted from the index
and still said the canonical register did not exist. The current branch
corrects those source-of-truth defects rather than treating them as future
review work.

Casey record `6529NM.2026.001.DILIGENCE-01` now documents the Museum's final
post-accession title, custody, token-approval, encumbrance, and point-in-time
exact-address sanctions review. Its twenty-two-file evidence package retains
nineteen exact JSON-RPC responses and brackets the contract-read window at
Ethereum finalized block `25,666,454`, hash
`0x03f4728f9ae5949d30d0b3217a4934f3a6bfa64145ac8b97a10ff809e0365cce`.
All seven owners and the ENS resolution match the Museum address; all seven
token-specific approvals are zero. The official OFAC UI screen passed a known
listed-address positive control and returned no exact match for eight
lot-related addresses. The record preserves the limits: no identity or fuzzy
name verification, 50 Percent Rule analysis, transaction tracing, legal
opinion, operator-for-all review, or claim about future state.

The existing public title declaration is treated as the executed institutional
title instrument for the user-authorized full gift, completed delivery, formal
acceptance, and accession. No donor-signed deed or private annex is invented.
The unused optional restricted-annex stub records only that no separate private
annex exists; it does not reopen title. The original gift and accession dates,
records, and hashes remain unchanged. Exact final commitments are intentionally
deferred until independent review, complete local validation, governed PR
checks, and merge.

Independent substantive reviewer Peirce
(`019fc237-73ed-7b33-85a2-cd65cbd207a8`) approved exact constructed commit
`ffd2cf34b66571a9617dc273037e3cf7bc8670c0` at
`2026-08-02T11:35:27Z`. The reviewer recomputed the twenty-two-file
manifest at
`sha256:8770ca3f6a7591c4548a72c18f410bb2e51fa1862d1921d6cd800ffa355b6edd`,
verified all nineteen raw RPC response digests and the exact custody/approval/
ENS/finality results, confirmed the eight OFAC no-match observations and
positive control, and found the title, annex, copyright, and residual-risk
statements consistent with the accepted full-gift record. No substantive
correction was required. A separate schema reviewer exhaustively rejected
unknown-field probes throughout the live accession-lot, object, provenance,
and diligence structures; its preapproval hold was limited to the then-pending
review envelope and two now-corrected test-message assertions.

## 2026-08-02 exact-block evidence correction

PR #16 merged as `b161938bceb80b3c14309e9b0ef6606eff51e63a` at
`2026-08-02T12:07:44Z`. When completed reviewer tasks were closed after merge,
an earlier adversarial report surfaced a real contradiction inside the raw
custody-audit JSON: contract calls had used a second provider's moving
`finalized` tag, while two raw fields described the reads as block-pinned and
same-block. The public Museum note and governed diligence record had already
limited the conclusion to a bracketed finalized window, but the raw evidence
overclaimed its method. Website production briefly refreshed to the 199-entry
`b161938...` manifest; final sign-off was immediately withheld.

Construction moved to `codex/casey-exact-block-evidence`. A fresh read-only
acquisition now anchors finalized block `25,667,060`, hash
`0x01dc7575349d0893386928c218b64a11b8d71e42015b1995bafa7d65e05084e3`,
timestamp `2026-08-02T12:00:23Z`. The head provider returned that same
finalized number and hash before and after the observation window. Every ENS,
`ownerOf`, and `getApproved` read on the call provider used an EIP-1898 block
selector containing the exact hash with `requireCanonical: true`. The new
custody-audit SHA-256 is
`sha256:ed6483d632cbe8c5c72cd395395d698f4e2100e5fb90b242ef39c4efca31b76e`;
all seven owners and ENS still match Museum custody and all seven token-level
approvals remain zero.

The correction also adds independent reconstruction of all nineteen canonical
request digests, exact raw-response IDs and bytes, safe-fetch byte bindings,
EIP-1898 selectors, block responses, ABI address words, CAIP-19 identities,
owners, approvals, and summaries. OFAC validation now pins all eight exact
address/role pairs plus the complete CHATEX/CYBER2/SDN positive control and
detail ID 33854. Diligence manifest traversal now rejects symlinks, Windows
reparse points, and non-regular entries. The replacement twenty-two-file
manifest is
`sha256:5ff2fc3f7d312c889fc05c0fe8f1a79a18880ed84da4cd43b4b7b64c0b204510`.
Revision 2 is intentionally `constructed` pending a new exact-commit
independent review; no PR #16 approval is reused for the changed evidence.

Independent chain/evidence reviewer Poincare
(`019fc278-cbf1-75c1-b630-41483c6ae4df`) and independent control-plane
reviewer Planck (`019fc278-ccbc-73b0-9bbc-9f333296cb6b`) both approved exact
constructed commit `b89604ef1967579241fa72152cf65d92ef3e6151` at
`2026-08-02T12:54:40.157Z` and `2026-08-02T12:52:54.647Z`, respectively.
The primary review envelope binds payload
`sha256:c8ad08661746f5c9f8a0522e2313ea9c6592ea15164520b4f47d0fea497f1513`.
After the approved construction, the review envelope and pending-to-reviewed
labels changed, followed by PR-review hardening of ABI padding validation,
nested-manifest inventory, amendment-history schema enforcement, unsafe-path
and CLI tests, runtime declaration, validator error clarity, and exact-block
index wording. No acquired evidence, RPC method or selector, raw response,
object result, OFAC observation, or museum conclusion changed.

## 2026-08-02 - Public Museum experience and curatorial reset

The production Museum frontend was re-audited against the actual visitor
experience rather than release transport alone. It is a functioning registry
browser, not an acceptable museum: it resolves records but presents no artwork
media, omits the public Casey accession dossier, foregrounds counts/status/JSON,
confuses donation-preapproved scopes with Museum holdings, and presents Keys
and Gates as text despite being a visual selection program. The source adapter
follows moving `main`, fetches Markdown and JSON only, does not normalize
`records/accessions/**/public/*.md` into public routes, has no typed object-media
model, and deliberately omits Markdown images.

`docs/public-museum-experience-standard.md` is the replacement product and
implementation standard. It makes the artwork encounter primary; defines
visitor and institutional information architecture; specifies object, artist,
project, gift, program, exhibition, story, policy, search, media, IIIF, live
generator, rights, provenance, accessibility, performance, security, SEO, and
release behavior; and uses the Casey gift and Keys and Gates as required launch
exemplars. The release boundary is now 200 entries with Keccak-256
`0x101e83c65f913ea6faf1db4c184845fa8bad878497edcaf58096de6f14fa77a5`
and SHA-256
`sha256:aadb082ea555a3b29a5f39dc54a189f3876f91c6ec8089f084cee71168c606a0`.
These are local candidate values, not merged release authority.

The curatorial audit also rejected the existing Casey artist/practice profile
and collection essay as final public scholarship. They are careful accession
research summaries whose structure is controlled by source qualifications and
technical caveats rather than sustained art-historical argument. A user-supplied
five-minute comparison produced an 8,576-word, fifteen-section monograph; that
result is now treated as a floor, not a target. The persistent third lane is
recorded in `notes/wip/2026-08-02-curatorial-writing-redo.md` and owns a finished
Casey monograph, separate project essays, a major seven-work collection essay,
a full donation narrative, seven object entries, and a separate conservation
layer. Evidence must support that writing without becoming its subject.

All 119 repository tests pass with one expected Windows named-pipe skip. The
301-file bootstrap, complete Museum validator, network fetch guard, twenty-two-
file Casey diligence package check, and deterministic 200-entry manifest check
also pass. No frontend code, Casey media bytes, IIIF manifests, or replacement
curatorial texts have yet been merged or deployed; this checkpoint defines and
validates the required redo rather than claiming its implementation.

### 6529-native visual-system correction

The user identified a further release failure: the Museum page does not look
native to `6529.io` and instead uses generic generated-product styling. The
replacement standard now makes visual-system fidelity an absolute launch gate.
The Museum must build from the frontend's actual Montserrat typography, black
ground, white/iron hierarchy, primary-blue accent, global layout/sidebar,
desktop/mobile navigation, spacing, focus, breakpoint, and motion conventions.
Museum differentiation must come from artwork scale, sequence, editorial
pacing, and narrowly justified viewing primitives, not a detached “museum”
theme, oversized serif, rounded-card system, badges, gradients, glass effects,
or dashboard composition.

The exact frontend audit boundary now includes `styles/fonts.css`,
`styles/globals.css`, `tailwind.config.ts`,
`components/layout/WebLayout.tsx`, `components/layout/sidebar/**`,
`hooks/useSidebarSections.ts`, `components/navigation/BottomNavigation.tsx`,
and the existing art surfaces under `components/the-memes/**`,
`components/memelab/**`, and `components/nextGen/collections/**`. The
frontend worker must publish a visual-fidelity matrix, list reused foundations
and justified extensions, and return side-by-side desktop/mobile captures plus
computed-style evidence before product acceptance. The prior 200-entry
candidate manifest commitments above are obsolete because the governed
frontend standard changed after they were generated; new candidate commitments
must be generated only after the current documentation and curatorial edits
stabilize.

### Timeboxed production rescue directive

The user set a hard three-to-four-hour maximum for replacing the embarrassing
production Museum experience while AFK. The authorized release sequence is:
implement the smallest complete non-embarrassing art-first and 6529-native
release in `6529-Collections/6529seize-frontend`; raise and iterate its PR
with all configured bots and required CI; merge under the existing rules;
deploy the exact merge to staging; retain desktop/mobile E2E evidence; promote
the exact verified release to production; repeat the E2E suite in production;
then begin a second improvement sweep against the full public-experience and
curatorial standards.

The rescue release may publish verified existing interpretation while longer
replacement scholarship completes, but it may not fabricate text, media,
rights, status, or technical behavior. Its minimum visitor outcome is actual
Casey art at meaningful scale, an art-led home and holdings collection,
readable Casey gift/accession and seven object routes, native 6529 visual
grammar, corrected mobile overflow, governance/JSON demoted to supporting
evidence, and honest live/fallback labeling. Keys and Gates remains selected
and unminted and must never be presented as a holding. The frontend lane has
been authorized to complete PR, controlled merge, staging deployment, staging
E2E, production deployment, and production E2E without waiting for routine
approval. Finished long-form scholarship and deeper visual refinement continue
immediately after the rescue release as sweep two.

### 21:29 UTC verification and editorial state

- The first complete long-form Casey package now exists in WIP: a 12,557-word
  artist monograph, five project essays, a 4,055-word seven-work collection
  essay, a 2,557-word gift/accession narrative, seven object entries, and a
  4,990-word source-and-chronology control matrix.
- These files remain withheld from the canonical public release while the
  constructor/reviewer correction cycle runs. The first project-essay
  cross-review returned substantive revisions rather than a ceremonial pass;
  all findings are recorded in
  `notes/wip/casey-curatorial-drafts/editorial-review.md` and returned to the
  original authors.
- `python scripts/bootstrap_validate.py` passed at 21:29 UTC with 301 JSON
  files checked while the manuscript package was present.
- The production-rescue frontend is frozen to a coherent art-first slice. Its
  remaining local gates are runtime activation of the strict atomic Casey
  publication adapter, type/test completion, and retained desktop/mobile
  visual evidence before PR review.

### 22:30 UTC public-scholarship promotion checkpoint

The complete Casey publication package has passed independent editorial review
after substantive revision: the artist monograph, seven-work collection essay,
gift narrative, five project essays, seven object entries, and the source and
chronology matrix are all accepted for first release. The accepted manuscripts
are promoted deterministically into the accession's canonical `public/` tree by
`scripts/promote_casey_publications.py`; `scripts/bootstrap_validate.py` now
fails closed if a canonical publication diverges from its accepted manuscript.
This turns the editorial package into reproducible publication source rather
than leaving it as untracked prose or a hand-copied website artifact.

The generated public tree contains sixteen upgraded publications. Local
promotion and bootstrap validation pass with all 301 JSON records checked.
`INDEX.md` and `README.md` now expose the human-readable gift narrative,
project essays, object entries, artist and collection writing, and supporting
research apparatus directly rather than forcing a visitor to discover them
through control-plane records. The release manifest and full package/test
matrix remain to be regenerated and run only after this source boundary is
final; this checkpoint does not claim a merge or deployment.

The finalized local candidate now passes deterministic promotion, bootstrap,
full Museum/Casey semantic validation, the 175-file immutable Casey package
replay, the focused public-page binding regression, manifest idempotence, and
whitespace validation. The complete 119-test run reached one obsolete literal-
sentence assertion after all substantive validators passed; the generated
publication was corrected to preserve that existing assertion, and its focused
regression then passed. Hosted CI will rerun the entire matrix from the exact PR
head. Candidate release commitments are
`sha256:f115c92ec0c02a3d0ffb57b0688503a8ed979cef98749cd736ea04c23314ef0e`
and
`keccak256:0x0143e12b323e7171dc2f4d6233e4cab6e7ec0d3b8542077dca179d814342c523`;
the Casey package SHA-256 is
`4251581350afdee29e67c93e0da9b561d8da56f0382526b9306e7104d9e166be`.
These remain candidate values until governed merge to canonical `main`.

### 2026-08-03 production Museum frontend release checkpoint

The art-first rescue and its second publication sweep are now merged and live
in `6529-Collections/6529seize-frontend`. [Rescue PR #3550](https://github.com/6529-Collections/6529seize-frontend/pull/3550)
merged as `bd0983475802c8a742a1f52416fe480285ab1960`. [Second-sweep PR #3551](https://github.com/6529-Collections/6529seize-frontend/pull/3551)
merged as production main `5acf2f5f85531a0970cd6ba1fd8988f762923865`;
its final reviewed head was `b42e30880aee2792f2b133635d42ed368a3cd997`.

The second sweep publishes the canonical gift narrative, five project essays,
and the visitor-facing *Casey Reas: Sources and chronology* research record as
part of one strict atomic Museum publication. It also makes the gift open with
the first three governed artwork stills, retains exact-commit source links,
keeps live media sandboxed with a timed recovery to the still image, and fixes
the production read-only RPC/session-storage test harness. A final review fix
makes source-matrix section projection ignore heading-like text inside Markdown
fences and fail closed when its exact public boundaries are not unique.

Staging composition `156e2d0c3134d96d78a14b110f5006b57873268d`
embedded the exact production candidate. [Staging deploy run 30779714023](https://github.com/6529-Collections/6529seize-frontend/actions/runs/30779714023)
passed exact HTTP-version verification; automatic manifest-bound [staging E2E
run 30780357100](https://github.com/6529-Collections/6529seize-frontend/actions/runs/30780357100)
passed; and the retained Museum staging sweep passed 14/14 desktop/mobile
routes, all 390-pixel overflow checks, governed media, source links, dossier
disclosure, and live-recovery behavior.

[Production deploy run 30780811939](https://github.com/6529-Collections/6529seize-frontend/actions/runs/30780811939)
completed successfully for exact main
`5acf2f5f85531a0970cd6ba1fd8988f762923865` and produced release
`fe-production-20260803T030417Z-5acf2f5f8553`. Production `/api/version`
matched that SHA three consecutive times with `stale:false`. Exact detached-main
live validation passed all 11 declared production packs (73 tests), core smoke
14/14, WCAG/i18n 6/6, and the retained Museum sweep 14/14 including
desktop/mobile routes, 390-pixel no-overflow, governed art, immutable source
link, dossier, and live recovery. The validation bundles uploaded with the
release are identified as `production-pack-evidence-5acf2f5f`,
`production-companion-evidence-5acf2f5f`, and `production-5acf2f5f`; the
approved S3 copies were read back with SHA-256 metadata.

The current `PRODUCTION: OFF` serialized manual-fallback path has no sanctioned
automatic Production E2E trigger: the manifest-bound workflow is Release-Bus-
only and rejects invented train inputs. The exact detached-main packs above are
the truthful production E2E substitute for this release. The exact
`test:e2e:surface-matrix` command also passed with 26 tests green, 22 intentional
project skips, and zero failures. This disposition is release-specific and does
not create a fallback precedent for later Museum releases.

Final sign-off passed after the deployment manifest's mandatory 30-minute
release-captain checkpoint from 03:26:15 through 03:56:18 UTC. The final sixteen
minutes included thirty-three consecutive polling observations from 03:40:17
through 03:56:18 UTC; every observation retained the exact served and announced
frontend SHA, returned no stale response, and kept the Museum route healthy.
Final atomic readback found
frontend main and live production at `5acf2f5f85531a0970cd6ba1fd8988f762923865`,
canonical Museum main at `04856bc3d137cc2a74a8cf15f068e02d3d026038`,
all seven representative Museum routes at HTTP 200, zero active release actors,
and both Release Bus lanes deliberately `OFF` and changeable under the recorded
fallback controls. The completed manifest validates with no holds or warnings;
its redacted evidence, release report, and watch record were written to the
approved S3 release prefix and read back with SHA-256 metadata.

### 2026-08-03 Open Museum public-record implementation directive

The founder directed the Museum to make a foundational operating idea visible
on the public site: the GitHub repository is not only inspectable but publicly
cloneable and group-editable through pull requests. Anyone should be able to
read the source and revision history and propose a correction, stronger
evidence, deeper scholarship, improved accessibility, or technical and
preservation work. Review and deterministic validation protect the published
record without closing its construction to the network.

This repository phase is explicitly intermediate. Our Fall 2026 goal is for
every admitted Museum record—from governance decisions and policies to
accessions, provenance, rights, preservation events, and later corrections—to
have an on-chain commitment and append-only lineage in a custom contract, with
large documents and media on content-addressed storage. The website remains a
replaceable display and interpretation layer rather than the sole location of
institutional memory. The target is not evidence that a contract is
implemented, audited, deployed, activated, or migrated.

The implementation contract is retained in
`notes/wip/2026-08-03-open-museum-public-record.md`. The Museum repository lane
will publish a governed human-readable statement and contribution guide. The
frontend lane will add the complete idea to About and Sources, a concise
version to the home experience, and a quiet exact-source/contribution colophon
to every Museum page family. Exact-source links bind the active immutable
source commit; contribution actions target only validated canonical repository
paths. The repository lane is gated by PR review, merge, manifest, bootstrap,
fetch-guard, unit-test, and full-validator checks. The frontend lane is gated
by PR review, merge, rendered review, staging E2E, production deployment,
production E2E, and the final rendered-product polish sweep. Both lanes bind to
the same reviewed source state; frontend qualification does not imply contract
deployment or migration.

### 2026-08-03 Museum publication copy-desk checkpoint

The public Museum corpus has completed a sentence-level copy edit across the
Open Museum statement, on-chain transition, contributor guide, curatorial
publication standard, Casey Reas artist and collection essays, gift narrative,
five project essays, seven object entries, curatorial review, and public gift
authorization. The edit removes repeated synthetic antithesis, process
narration, and software-product language while preserving evidence, citations,
rights, provenance, accession status, technical condition, and deployment
boundaries. Adopted policy transcriptions remain verbatim.

The retained Casey manuscripts and sixteen promoted public publications are
reproducible and pass the publication promotion check. Local validation passes
119 unit tests with one intentional Windows skip, the fetch guard, 301-record
bootstrap validation, Casey snapshot verification, diligence manifest check,
full Museum validation, and deterministic manifest verification. The candidate
release remains 213 entries with SHA-256
`sha256:0534cdbe0ffac082c9a37ae3fcf95eb9eea46aa36511bb48978afb22f5cbc246`
and Keccak-256
`0x39fc02bbf1f66fd60adea9ca54b0ee8e079cade31dc69e1e796544ab34dd8cce`.
These values remain candidates until the governed source pull request merges.

The frontend copy edit is implemented in a separate focused branch. About now
leads with mission, governed manuscripts carry their own argument, source and
revision information is treated as a quiet colophon, and the Methods page
presents adopted policies, standards, research methods, on-chain designs, and
technical specifications as a curated source index. Complete technical sources
remain public without being reproduced as visitor-facing essays. Frontend
focused tests, changed lint and typecheck, diff checks, and React Doctor 100/100
pass before source activation and release qualification.

### 2026-08-03 Museum publication exact-head review follow-up

The source copy edit is complete. Exact-head review added five precision
corrections before release: the on-chain transition now defines the
`6529NM_RECORD_MANIFEST` inventory, canonicalization, hashing, ordering, and
contract-export invariant; machine-record copy corrections require an
append-only amendment carrying `supersedes`; chain-native and off-chain receipt
paths are distinguished; the *{Software} Structures* chronology cites Reas for
the 2001 invitation and the Whitney for the 2004 public launch; and generative
trait analysis is bound to the Museum's published NextGen-compatible method,
source snapshot, configuration, and deterministic result set. Four leading
token numbers were recast as normal paragraph prose without changing their
identifiers. Governed release remains pending the refreshed manifest,
exact-head validation, and review readback.

The corrected source tree then passed manuscript promotion parity, bootstrap
validation across 301 JSON files, 119 unit tests with one intentional Windows
named-pipe skip, the network fetch guard, Casey snapshot verification, the
22-file diligence inventory, full Museum validation, deterministic manifest
verification, and the Windows-safe diff check. The refreshed 213-entry
candidate manifest has SHA-256
`sha256:02c0c65f48017156094221aed490915c853dbbcac12b713b43d8aebece2da0fa`
and Keccak-256
`0x9c276bcbfcc142e6933aa3c3f337425398b3e2c1fde059351f6221debad7a4e3`.
These commitments remain candidates until the reviewed source pull request
merges.

### 2026-08-04 institutional-practice source package

The Museum has completed the research and editorial draft for *A field of
practice*, a comparative study of fourteen institutions and institutional
systems: the Met, Getty, MoMA, the Whitney, Tate, Centre Pompidou, SFMOMA, the
Guggenheim, ZKM, Ars Electronica, Rhizome/New Museum, Serpentine Arts
Technologies, the V&A, and LACMA. The package contains an introductory essay,
fourteen profiles, a primary-source register, and a revised Museum scholarship
and editorial standard.

An adversarial factual and prose audit materially changed the first draft.
Every profile now carries primary-source links beside factual claims, examines
a named work or project and a longer research or conservation source, separates
institutional self-description from demonstrated practice, and ends with
specific Museum requirements and limits. The audit corrected MoMA's
exhibition-history completeness claim, Rhizome's May–June 2026 Conifer service
transition, and a Centre Pompidou URL that resolved to a different artwork. It
also removed comparative rankings, prestige language, repetitive antithesis,
and generic technology rhetoric.

The source register records displayed titles, dates shown, source types, access
date, and evidentiary use. Its current 114 unique links pass the local hard-link
audit with no HTTP 404 or server-error response. The package test enforces exact
profile inventory, common publication control, named cases, claim-level links,
profile-to-register source reconciliation, direct HTTPS sources, and selected
editorial prohibitions. Full repository validation, manifest generation,
governed source review, and frontend publication remain pending.

### 2026-08-04 institutional-practice PR #22 review correction

The governed source review correctly found that the comparative essay's link
to Centre Pompidou's *Icône* object record was absent from the source register.
The record was reverified as Vera Molnar, *Icône*, 1964, and registered with
the exact catalogue functions for which the essay cites it. Source
reconciliation now covers the comparative essay and all fourteen profiles;
the register invariant is exactly 114 unique primary-source URLs. Profile
publication dates now validate as ISO dates so later additions do not inherit
the first release date. Rhizome's historical editorial path and archive root
were separately rechecked at HTTP 200. Serpentine's `1.1.0` version remains
correct because its revision history records a substantive hostile-audit
revision after the initial draft.

### 2026-08-04 institutional-practice PR #22 second review correction

The second exact-head review separated four dates and states that had been
compressed in the draft: Tate's Intermedia Art microsite dates (2008–2012),
its Conifer capture dates (November 2019–February 2020), Conifer's completed
May 2026 subscription closure, and its planned June platform replacement. The
current Conifer landing-page notice remains separately cited. A Met grammar
defect was corrected. The publication validator now extracts HTTP as well as
HTTPS Markdown links and rejects any registered public source that is not
HTTPS.

The review request for self-declared immutable edition URLs was not adopted.
The canonical frontend already constructs each exact-commit GitHub source URL
from the verified publication identity. Writing a future merge SHA into its
own manuscript would be circular and would immediately stale on correction.
Pre-publication changes are recorded in this append-only ledger and manuscript
revision histories; they do not fabricate `supersedes` relationships to
versions that were never publicly released.

Status amendment: this paragraph supersedes the pending-validation statement
in the initial 2026-08-04 institutional-practice entry above. The corrected
tree passed the six institutional-publication tests, bootstrap
validation across 301 JSON files, full Museum validation, the network fetch
guard, Casey dossier validation, and the current twenty-two-file Casey
diligence inventory. Deterministic regeneration produced a 230-entry candidate
manifest with SHA-256
`sha256:7ae561a27b5c3494d3bc81035af506ba5c49501ebb5c73a5535a3a2898c1b416`
and Keccak-256
`0xe71d1d744b2bccf1e2c724ab907a5bcc8e53bbf9befdc8f93b21ff89e76dd93c`.
The values remain candidates until governed PR #22 merges.

### 2026-08-04 expanded institutional-practice study

Production was verified before work began: runtime
`88a4f19885f9ff70a1632bda7255b8091263ee86`, `stale:false`, with the overview,
profile, and source routes returning HTTP 200. Six Luna-max research lanes then
covered digital-native institutions, the global digital field, contemporary
museum scholarship, digital conservation, chain-native adjacent practice, and
editorial/web structure. The orchestrator retained source, selection, prose,
test, and release responsibility.

The source draft now contains twenty-seven profiles, an expanded *A field
of practice* overview, a classified adjacent-chain-native-practice essay, an
expanded curatorial publication standard, and a detailed digital-art
stewardship standard. The deterministic institutional source inventory binds
236 unique HTTPS sources to their citation labels and manuscript paths. It is
generated by `scripts/generate_institutional_source_inventory.py` and checked
in CI.

Selection is evidence-based and confers no ranking. HEK, LI-MA, V2_,
transmediale, ACMI, M+, Nam June Paik Art Center, NTT ICC, Centro Multimedia,
Laboratorio Arte Alameda, Dia, Walker Art Center, and MCA Chicago join the
original fourteen profiles. Platforms, marketplaces, festivals, archives, communities,
private collections, and self-described museums remain separately classified;
no mint, sale, vote, exhibition, wallet transfer, or platform publication is
treated as accession, title, rights, or preservation.

Focused tests, source-inventory idempotence, bootstrap validation across 302
JSON files, the complete 126-test suite, full Museum validation, Casey package
verification, and diligence-inventory verification pass. All 236 cited URLs
were observed. HEAD returned 198 HTTP 200 responses; GET rechecks distinguished
five HEAD-only 404s from two stale citations, which were replaced with current
official Bright Moments and MCA Chicago pages. Bot controls and transport
failures at known official domains are recorded as access conditions rather
than treated as evidence of disappearance.

Deterministic regeneration produced a 247-entry candidate manifest with
SHA-256
`sha256:15056aa38c28ef5662063fd9193d211a59dd03797d543fed57a0b82c497c03d5`
and Keccak-256
`0x48e475c5ff45f183f69b1aa28b3b7d6b1fb50269757d51902b4ade68252eca7c`.
The values remain candidates until governed PR review and merge. The website
remains a subsequent atomic publication and release phase.

### 2026-08-04 living-study and public-corpus editorial checkpoint

The same living institutional-practice study now comprises twenty-seven
profiles, the comparative overview, the adjacent-practice study, the public
scholarship and editorial standard, and the source register. No “second
edition” identity is asserted. Review corrections increased the deterministic
inventory to 237 cited HTTPS sources and kept claim-level source notes in the
public manuscripts.

The editorial standard was applied across the Open Museum statements, Casey
Reas artist and collection scholarship, five project essays, seven object
entries, the gift and curatorial accession narratives, Keys and Gates, and the
institutional-practice corpus. Adopted and historical policy transcriptions
remain unchanged. The Casey retained drafts and promoted public pages are again
byte-reproducible through `scripts/promote_casey_publications.py`; its finished
status and interpretation markers were restated in direct Museum prose without
weakening the validation boundary.

Local qualification passes the 126-test repository suite with one intentional
Windows named-pipe skip, deterministic Casey publication promotion, bootstrap
and full Museum validation, fetch guard, snapshot/package verification,
diligence-manifest verification, and institutional-source reconciliation. The
current 247-entry candidate manifest has SHA-256
`sha256:754acbdc27c5b13beb20cf460c95b0a595d9cdeab6f5ee8ad40395db4319c796`
and Keccak-256
`0xe583d775ff1feb724db2187451d290b167f9155b0f2074983d1f7c5ed72e1204`.
These commitments remain candidates until the governed source PR merges.

### 2026-08-04 final public copy desk

Two independent editorial reviews audited the exact integrated source tree.
Accepted corrections removed residual formulaic contrasts and internal workflow
language, attributed the *Ex Nihilo (Cosmos)* non-repetition claim, restored
`noncommercial` to the computational-research rights statement, separated
chain identity and transfer history from legal title, copyright, and accession,
and corrected the `technically_verified`, `preservation_complete`, and
`display_ready` gate language. The study remains one living publication.

The Casey retained drafts regenerate all sixteen promoted public manuscripts
byte-for-byte. The complete 126-test suite passes with one intentional Windows
named-pipe skip; full Museum validation, publication promotion, the 237-source
inventory, and manifest checks pass. The resulting 247-entry candidate manifest
has SHA-256
`sha256:40065c69a864377d92ed48106c48c2abfd72e2ffd3d1b02f9097a4e08a87393f`
and Keccak-256
`0x63a97f876a08a18fa8062df8e60798bde45598962a483318d9289a71eb9e011c`.
These commitments remain candidates until the governed source PR merges.

The review-bot follow-up added the institutional source-inventory command to
the contributor path, removed consent-sensitive biographical detail from the
Keys and Gates public essay, disambiguated token-number paragraph openings for
Markdown, attributed a live-software capability to artist documentation, added
two omitted profile revision notes, and reconciled the 236-URL availability
pass with the later 237-source inventory. Forty-one focused tests and full
Museum, promotion, source-inventory, and manifest checks pass on the follow-up.
## 2026-08-04 generative-systems analysis checkpoint

The user set a world-class algorithm-analysis ambition for the five Casey Reas
projects in accession `6529NM.2026.001` and directed that the result establish
a reusable standard for any generative-art collection. The durable proposal is
indexed at
`notes/wip/2026-08-04-generative-systems-analysis-standard.md`. It separates
the existing NextGen-compatible trait-prevalence layer from a new generative-
system dossier covering identity, genotype, initial phenotype, performance,
participation, encounter, exact source/seed reconstruction, algorithmic score,
collection topology, causal counterfactuals, conservation, publication, and
reproducibility.

The Casey pilot identifies project-specific analytical cores: *CENTURY* as an
off-screen composition made topologically mutable through continuing slice
state; *Pre-Process* as an exact `8 x 3 x 5` traversal whose 120 combinations
occur once each and whose 100 circles expose one behavior through eight
surfaces; *Phototaxis* as a Braitenberg-derived sensor-motion system whose
accumulated path drawing records speed and permits escape beyond the nominal
world; *923 EMPTY ROOMS* as a 923-state combination-with-replacement system
whose colorform field is converted through RGB displacement into a line-built
room; and *Ex Nihilo (Cosmos)* as dodecahedral geometry translated through
colored edges, temporal raster memory, channel displacement, and projected
line fields.

Read-only retrieval on 2026-08-04 confirmed that all seven official generator
response lengths and SHA-256 digests still match the independently reviewed
values in `evidence/casey-reas/generator-observations.json`. No generator bytes
were retained or added in this checkpoint. Source preservation, feature-script
reconstruction, rights clearance for annotated code and counterfactual images,
instrumented trace tooling, cross-environment tests, and independent review
remain open. The proposal is WIP analysis, not adopted policy and not an
accession amendment.

### Five-project dossier construction

The user approved applying the method to every Casey project in the gift. The
proposal is now implemented as the working standard
`docs/generative-system-analysis.md`, the reusable template
`templates/generative-system-dossier.md`, and a constructed research package
at `notes/research/generative-systems/casey-reas/`. The package contains five
project dossiers covering all seven works, a comparative study, and a package
index. It is explicitly pending independent technical, curatorial, rights,
accessibility, and conservation review and has not been promoted into the
reviewed accession publications.

The construction/reconciliation pass materially corrected the initial WIP
analysis. The xorshift projects parse a 16-character slice of an `0x`-prefixed
hash, hence fourteen hash digits before JavaScript bitwise coercion.
*Pre-Process* and *Ex Nihilo* each discard 500,000 values from each of two
`sfc32` streams, one million calls total, rather than one million per stream.
*923 EMPTY ROOMS* invocation 0 dispatches no implemented colorform but retains
the gradient and line-field render path; #713 retains default symmetric depth
while the CDMX special depth applies only to invocation 617. The 256-token *Ex
Nihilo* replay establishes that #248's published `CHUNK=3` maps operationally
to runtime `metaCHUNK=4`, while the unretained feature script leaves the reason
for that semantic mapping unresolved.

Further source-level findings now carried as reviewable claims include the
*Pre-Process* Chinese-remainder inverse and reset/pause-latch caveats;
*Phototaxis* #308's exact three-light field, balanced four-type population,
unbounded active movement, dormant death/rebirth paths, and single-frame
advance when lights are toggled during pause; and *Ex Nihilo*'s partial pause,
which freezes rotation while temporal feedback continues to accumulate.

`python scripts/bootstrap_validate.py` passes with 301 JSON files,
`python scripts/validate.py` passes the full schema/semantic/commitment suite,
the 22-file Casey diligence manifest check passes, and `codex-diff-check`
passes for the complete construction. The public release-manifest check was
run and correctly reports stale because the working standard, template, and
root index change governed release inventory. The manifest was not regenerated
against this unreviewed research construction and the concurrently dirty
homepage WIP; release generation belongs after substantive review and an exact
release-scope freeze.

### Art-first editorial correction

The user rejected the constructed dossiers' initial apparatus-first reading
order: an art connoisseur should not have to cross record status, rights
limitations, preservation caveats, or method vocabulary before reaching the
work. The correction is applied across the Casey package. All five project
dossiers now open with their curatorial proposition; the comparative study and
package index open with the seven-work argument; and research status and
control boundaries appear at the end.

The working standard and reusable template now make this a general rule for
future collections: encounter, thesis, close looking, artistic argument, and
intelligible system first; evidence, rights, conservation, governance status,
and review apparatus last. The change preserves controls while refusing to
make bureaucracy the reader's entrance to the art.

## 2026-08-04 generative-system frontend study

The user clarified two enduring product requirements. First, the Museum should
analyze a generative project as it accessions work while allowing later
acquisitions from the same project to join that analysis. Second, the public
experience should eventually visualize the project as a whole and show where a
particular token falls within it.

The resulting WIP recommendation is indexed at
`notes/wip/2026-08-04-generative-system-frontend-experience.md`. It assigns the
permanent study to the project, token-specific interpretation to object pages,
and acquisition-group interpretation to gift pages. The public label is
**Inside the System**, with a project child route for the immersive study and a
compact **In the system** module on each relevant object page.

The proposed visualizer supports four evidence-honest forms: exhaustive
lattice, finite combinatorial field, sampled field, and dynamic state space.
Museum holdings appear as exact-identity overlays, so a later accession adds a
new marker and close reading without changing the historical gift or treating
non-held project outputs as collection objects. *Pre-Process* is the preferred
first complete-field pilot; *CENTURY* is the preferred first multi-holding
comparison. The recommendation was checked against the live Museum home at
desktop and 390-pixel mobile widths and the current frontend project, object,
gift, story, shell, and publication-domain source. No frontend files were
changed in this study.

## 2026-08-04 Inside the System implementation checkpoint

The five Casey project studies are implemented for local review in
`C:\w\museum-inside-system-fe` on branch `codex/museum-inside-system`, based on
remote-main commit `aa77ddf836c3c83cc680054e40247f7e4a78a18d`. The build adds
the canonical project child route, art-first study pages, reusable typed study
definitions, a narrow interactive possibility-space island, object-page
position modules, a five-project gift directory, and the Stories/Research
entry point.

All four evidence-honest visualization modes are live. *Pre-Process* exposes
its complete 120-position `8 × 3 × 5` lattice; *923 EMPTY ROOMS* and *Ex Nihilo
(Cosmos)* expose finite combinatorial structure; *CENTURY* exposes an observed
edition field and compares all three Museum works; and *Phototaxis* exposes a
causal dynamic-state sequence with its exact held-token light positions. A
semantic table accompanies every map, and exact accession selection is
shareable through a validated `work` query and object deep link.

Verification passes: formatting, changed-file typecheck and lint, 23 focused
tests, React Doctor 100/100, production build, desktop visual inspection,
keyboard grid movement, and zero-horizontal-overflow inspection. The branch is
uncommitted, unpushed, unmerged, undeployed, and not a public-release claim.
The constructed study definitions remain frontend-bundled until the governed
publication adapter supports optional atomic study groups. A separate future
fix must remove the frontend's exact-seven Casey overlay assumption before a
later acquisition can enter the live publication safely.

## 2026-08-04 Inside the System comparison instrument checkpoint

The frontend review candidate in `C:\w\museum-inside-system-fe` now keeps the
Museum accession fixed at left and lets visitors place any minted project work,
a trait-filtered/random minted work, or a project-specific analytical
counterfactual/session manifestation at right. Piece-specific SVG renderers are
implemented for all five Casey projects, backed by compact indexes for all
3,299 minted project works in the pinned complete snapshots.

Suggested structural neighbor, complement, and uncommon examples are derived
deterministically from published project traits and explicitly reject
marketplace rarity. Exhaustively minted starting grammars use session or
presentation language rather than implying nonexistent tokens. The branch is
still uncommitted, unpushed, unmerged, undeployed, and not an adopted Museum
publication; governed optional project-study envelopes remain the release gate.

## 2026-08-04 Inside the System release-boundary amendment

This checkpoint supersedes only the final release-gate sentence in the
preceding comparison-instrument checkpoint. Version 1 may ship a versioned
frontend display package derived from the repository's pinned snapshots,
reviewed descriptors, and project dossiers. It includes 3,300 edition records,
with *923 EMPTY ROOMS* invocation 0 retained explicitly. The package is an
interpretive access layer, not an accession or governance record.

Release conditions are official art first, persistent **Museum model** labels,
snapshot-backed minted lookup, reviewed NextGen-compatible **less often seen**
selection, and no marketplace or value ranking. Optional atomic remote
project-study records remain future work and are not a blocker for this
display-layer release. No deployment is asserted by this checkpoint.

### 2026-08-04 Keys and Gates responsive media delivery

The active source and frontend branches were created from the latest remote
`main` revisions in clean worktrees; unrelated dirty checkouts were preserved.
The live Keys and Gates Wave was re-read through authenticated 6529 tooling.
The latest direct program update still identifies Stream contract work as the
main blocker, while later chat is forward-looking and supplies no primary mint,
purchase, title, custody, or accession evidence. The sixteen outcomes therefore
remain `selected_unminted`.

All sixteen public submission objects were downloaded from their existing CDN
origin into an untracked local staging area and fixity-checked. They total
233,601,493 bytes and range from 4.1 MB to 46.7 MB. The new deterministic
`6529NM_WEB_PRESENTATION_WEBP_V1_Q82_M6` pipeline applies EXIF orientation,
converts embedded profiles to sRGB, strips source metadata except for the output
sRGB profile, preserves the complete uncropped frame, and emits 640, 1280, and
2400 pixel WebP variants without upscaling. The forty-eight governed
derivatives total 16,103,634 bytes.

The constructed media manifest keeps submitted source, web presentation
surrogate, and any future preservation object distinct. It joins source fixity,
recorded rights status, constructed visual descriptions, derivative fixity,
repository paths, and immutable CDN paths to all sixteen outcome IDs. It does
not activate CC0, establish a preservation master, or alter mint/acquisition/
accession state. The source originals are not committed; their existing public
URLs remain the explicit high-resolution route.

The CDN publication uses a new content-addressed namespace and additive writes
with `image/webp`, inline disposition, one-year immutable caching, stored
SHA-256 metadata, and S3 SHA-256 checksums. Existing source objects are not
overwritten. Repository validation, release-manifest regeneration, frontend
integration, bot review, merge, staging E2E, and production E2E remain the
active gates.

### 2026-08-04 Keys and Gates media determinism amendment

Museum PR #26's first Linux CI run exposed that a newly created LittleCMS sRGB
profile contains a wall-clock creation timestamp. Two otherwise identical
WebP conversions could therefore differ when they crossed a one-second
boundary. The v1 derivative record above remains the historical construction
checkpoint; it is superseded for publication by
`6529NM_WEB_PRESENTATION_WEBP_V2_Q82_M6_FIXED_ICC`.

The v2 generator embeds one repository-pinned 588-byte sRGB profile with
SHA-256
`4ed6f6f05df0d17516662c5fe06ac90e14e0c1936abd15a491b57998c56aef86`
instead of generating a profile at runtime. The new forty-eight derivatives
total 16,093,924 bytes, occupy a separate immutable transform namespace, and
were regenerated twice in separate processes with identical bytes. All v2 CDN
objects were then fetched and checked against the manifest for SHA-256, byte
size, WebP MIME type, and immutable cache headers. The uploaded v1 objects were
not overwritten and are not referenced by the amended manifest.

### 2026-08-04 Keys and Gates media review hardening

Automated PR review identified that ICC-profile hash failures were being
re-wrapped by the generic invalid-profile handler. The hash comparison now
runs outside that handler and a regression test preserves the specific
integrity error. Review also reported a possible aspect-ratio mismatch for the
OUT-009 640-pixel derivative. Direct Pillow inspection confirmed the committed
variants are 640x426, 1280x851, and 2400x1596 and are the uncropped products of
the recorded 6016x4000 source. The validator now independently derives every
declared height from its recorded oriented source dimensions, and a mutation
test rejects a cross-variant ratio change before fixity or geometry checks.

## 2026-08-05 Inside the System production closeout

Canonical generative-system standards, the Casey comparative study, and all
five project dossiers merged through Museum PR
[`#27`](https://github.com/6529-Collections/6529networkmuseum/pull/27) at
`2304497e343197fa0324d3f110255fedbb1e6fa8`. Frontend PR
[`#3594`](https://github.com/6529-Collections/6529seize-frontend/pull/3594)
merged the production experience at
`5b03302719b306b29582d43f6910fd1a843de1f7`; stabilization PR
[`#3602`](https://github.com/6529-Collections/6529seize-frontend/pull/3602)
produced the final production revision
`a36a5a437e68d03c886471caefe0bf01afc3827c`.

The public route family is live for *CENTURY*, *Pre-Process*, *Phototaxis*,
*923 EMPTY ROOMS*, and *Ex Nihilo (Cosmos)*. It provides official art first,
the Museum holding against any minted output, full-edition lookup and filters,
deterministic neighbor/complement/less-often-seen suggestions, and explicitly
labeled project-specific Museum models. All 3,300 minted records in the pinned
snapshots are represented.

Editorial/no-LLM-smell, museum-design, and collector-fun adversarial reviews
all returned **SHIP**. Required frontend CI, security, accessibility,
internationalization, and Museum gates passed. Staging deployment
[`30977518490`](https://github.com/6529-Collections/6529seize-frontend/actions/runs/30977518490)
and E2E
[`30978079115`](https://github.com/6529-Collections/6529seize-frontend/actions/runs/30978079115)
passed all 14 packs, including Museum 70/70 and Inside the System 8/8.
Production artifact
[`30977459534`](https://github.com/6529-Collections/6529seize-frontend/actions/runs/30977459534),
deployment
[`30978958753`](https://github.com/6529-Collections/6529seize-frontend/actions/runs/30978958753),
and E2E
[`30979315540`](https://github.com/6529-Collections/6529seize-frontend/actions/runs/30979315540)
passed all 13 packs, again including Museum 70/70 and Inside the System 8/8.
Direct production verification also passed the focused 8-test desktop/mobile
suite, and `/api/version` matched the exact revision.

The continuing ownership rule is now implemented: project scholarship persists
across acquisitions; object pages locate individual holdings; gift pages retain
their historical acquisition scope. A future work from one of these projects
adds an object reading and held-position overlay without being made part of
the Casey gift.

## 2026-08-05 Museum data architecture construction checkpoint

The Museum-native profile now treats Stream as a later interoperability target
instead of the source of Museum semantics. `6529NM_DATA_ARCHITECTURE_V1`
registers eleven complementary standards: Spectrum 5.1, CIDOC CRM 7.1.3, LIDO
1.1, PREMIS 3.0, PROV-O, Getty AAT/ULAN, IIIF Presentation 3.0, C2PA 2.4,
BagIt/RFC 8493, OCFL 1.1 with its 1.1.1 patch context, and CAIP-19 with its
Review/Draft caveat.

The public publication contains one integrated introduction, eleven standard
profiles, and a Casey Reas implementation audit. Every standard page opens with
the question it answers and a collection example before presenting authority,
version, classes or structures, Museum extensions, serialization, validation,
scope, and implementation state. The closed JSON profile and JSON Schema require
exactly eleven unique documents and preserve the five-state distinction among
conceptual mapping, source fields, serialization, validation, and operation.

Four primary-source research lanes and four independent review lanes were used.
The review pass corrected CIDOC physical-domain and software-agent mistakes,
LIDO resource-rights granularity, PREMIS conformance wording, PROV Bundle
typing, IIIF minimum structure and rights URI, C2PA assertion provenance, OCFL
inventory optionality, and recurring standards-engineering prose.

The final Casey audit found no literal data mismatch and strengthened the
control plane. A closed machine schedule now binds every object to title,
CAIP-19 identity, custody log, retained metadata digest, observed generator
digest, accession state, preservation state, and the explicit non-retention of
generator response bytes. The full Museum validator invokes the data-
architecture validator, which also binds exact standard-document paths and the
complete architecture publication to the deterministic release manifest.

Before the correction pass, the complete local control plane passed 139 tests
with one Windows capability skip, plus bootstrap, fetch guard, full validation,
institutional inventory, program media, Casey diligence, and the 3,300-token
snapshot verifier. After correction, eight focused tests, the dedicated data-
architecture validator, the full Museum/Casey validator, manifest check, and
whitespace check passed. The final exact-tree CI-equivalent run then passed in
461.1 seconds: 141 tests with one expected Windows capability skip, bootstrap,
fetch guard, program-media and institutional-source inventory checks, full
Museum/Casey validation, deterministic manifest verification, NextGen
compatibility, all Casey mutation controls, the 3,300-token snapshot verifier,
the diligence manifest, and whitespace validation. Pull request, bot review,
merge, website adapter, staging, and production remain active gates.

PR #30 was reconciled with Museum main after the rights-handbook merge. The
combined semantic validators and deterministic manifest passed. Hosted Museum
validation and the Ubuntu/Windows deterministic jobs all passed on exact head
`490adda4dd48fdc0e7d23b066b5c98c8ba91cf00`. Because the synchronized webhook
did not enqueue its configured follow-up, central head-bound review job
`31035730573` ran the documented 6529bot fallback and returned no findings. Its
one non-blocking coverage observation was adopted by requiring the Casey audit
to contain all eleven complete profile names.

## 2026-08-05 rights education and expression registry

The source corpus for the Museum's public rights learning room is complete.
It joins a closed twenty-two-entry registry to three public manuscripts, seven
exact English Creative Commons legal-code snapshots, and the reviewed rights
records for all seven Casey Reas accessioned objects. The public-domain and
collector guidance states directly that possession of a token or artwork
usually does not transfer copyright, and that copyright expiration places a
large part of art history in the public domain for study, publication, and new
work.

The registry preserves the distinction among a public license, CC0
dedication, Public Domain Mark, RightsStatements.org status term, absence of a
public license, and bespoke terms. Keys and Gates retains its announced CC0
intention as `conditional_not_yet_effective` because the selected works remain
unminted. The Stream-compatible object rights records are unchanged; the new
registry supplies a linked external vocabulary without silently extending the
Stream schema.

Source validation passed the complete Museum and Casey controls, 138 Python
tests with one intentional skip, program-media and diligence-manifest checks,
and deterministic release-manifest regeneration. The current source release
commitments are SHA-256
`sha256:b6b1d5ddf19c88335b752bc610a1d4020236a3eb4a86a13d52182a29aa22ffb1`
and Keccak-256
`0x11546194ab32ec2553562d48aa21788329da52afa86470812d4c327aa2d3d025`.
Frontend integration, staged qualification, and production qualification are
the remaining release gates.

## 2026-08-05 rights education production closeout

The remaining gates are complete. Museum PR #29 merged the rights corpus as
`11c79489e0ae65d9a296577c44c881c3f79267d6`; frontend PR #3627 merged the
public experience as `d448d4c282c034fa2a1d5d1d95ce90fc85561e54`.

Staging deploy run `31043258638` and automatic staging E2E run `31044289420`
passed. Production deploy run `31045606678` and automatic production E2E run
`31046152675` passed on exact frontend main. Independent staging and production
checks passed the six focused rights journeys; the final production sweep also
passed all twenty-two expression routes, both audience guides, the Casey
object-to-rights path, exact legal-text access, desktop and 390-pixel rendering,
and version/source identity checks.

Canonical Museum main subsequently advanced through additive PR #30 to
`ad8ea4338659e0825dc5a79295e824eadec876e6`. Its 345-entry manifest commits to
SHA-256 `sha256:258a2aa6a970cc84d036de511902cbc1d5fbb5141067cc146fe83ac879d20544`
and Keccak-256
`0x9ccca279ca25f1d0b65b2430168dd192a87dee77b682f63db25de44fc899ea26`.
At production qualification, the live frontend had refreshed to that exact
source commit; PR #30 did not change the rights corpus. This append-only
closeout changes the repository release commitment again without changing the
public rights corpus. The rights publication is live and no product or release
gate remains open.

## 2026-08-05 rights practice and editorial redesign

The public detail page was reopened after product review. The six-use display
looked like a generic software dashboard, and the no-public-license entry made
ordinary museum display appear exceptional. Four independent research lanes
reviewed museum display and fair-use practice, Creative Commons and public
domain terms, all twelve RightsStatements.org expressions, and the frontend's
visual language.

The source branch now carries registry version 1.1.0 with a second,
action-specific Museum-practice matrix for all twenty-two expressions. The
original instrument-permission matrix remains intact. Public manuscripts now
state directly that lawful acquisition supports faithful display, collection
documentation, scholarship, and care, while copyright ownership remains with
the artist unless transferred. Tests prevent a no-license or uncertain-status
entry from becoming a blanket display, documentation, or preservation ban.

The frontend branch replaces status chips, colored state coding, rounded
dashboard cells, metadata pills, and the boxed visitor note with a ruled
editorial register and quiet metadata. The public component reads the new
Museum-practice matrix and keeps the exact license text and instrument record
available below it. A no-em-dash control applies to the revised public rights
copy.

Local source validation is complete: 151 tests passed with one intentional
platform skip, together with every deterministic validation and package gate
used by hosted Museum CI. The frontend passed 158 Museum regression tests,
changed-file lint and typecheck, and React Doctor 100/100 before its exact
source build. Required remaining gates are final manifest regeneration, both
pull-request review cycles, exact-source frontend build and visual review,
staging deployment and E2E, production deployment and E2E, and a release note
to the Dev Team Chat subwave using the `punk6529bot` identity.
