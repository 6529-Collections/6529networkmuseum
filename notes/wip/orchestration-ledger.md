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
reject missing or linked configured roots and files. Evidence, WIP notes, Git internals, and the
self-referential release-artifact directory retain explicit separate treatment.

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
