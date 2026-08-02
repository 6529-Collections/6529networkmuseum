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

Correction to earlier in-progress wording: commit `8a2e26a` was pushed to PR
#2 and the PR was marked ready before this follow-up review began. Statements
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
subject, and owner-record hash with exact-length bounded calls. A new ninth
network-free checker rejects substitution of every readback field. The three
changed governed selectors produce closed selector-set hash
`0x4c2a05297ef36555d0bd199b80df1463d02702f6bd1bde9444960279d15957e5`
and therefore new executor binding commitment
`0x40a3c47c9686f82852e14e2b503ff9e02cdbed30d556db7347112bec4061e3f9`.

Focused conformance scripts pass locally. Full regeneration, repository-wide
validation, a new exact head, fresh CI, and fresh independent/bot review remain
required. Nothing in this entry authorizes deployment, a network write, or a
completed accession.
