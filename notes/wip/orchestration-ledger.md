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
