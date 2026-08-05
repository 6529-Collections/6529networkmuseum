# Repository implementation roadmap

Record ID: `6529NM-OPS-001`
Status: active working plan
Last updated: 2026-08-01 UTC

This roadmap is the durable handoff for the build. A new constructor or reviewer should be able to resume work from this file and `INDEX.md` without relying on chat history.

## Fixed institutional facts

- The repository is the transitional public system of record before governed records are committed to decentralized storage and an on-chain registry.
- The first Casey Reas group has been donated. Its seven object records and accession dossier must therefore document an actual donation, while individual accession gates remain evidence-based.
- Keys and Gates has completed selection but the selected works have not been minted. The minting architecture remains a controlled decision between a dedicated 6529Stream instance and a subcollection on the main Stream deployment.
- A Keys and Gates `WINNER` is not evidence of minting, transfer, acquisition, accession, cataloguing, preservation completion, or display readiness.
- Externally minted works are never reminted or wrapped merely to enter the Museum record. Their existing token identity is cited by a registry record.
- OpenSea rarity metrics are prohibited as Museum evidence. If a generative collection requires trait analysis, the Museum publishes the input snapshot, exact NextGen-compatible algorithm, configuration, software version, output, and hash.

## Publication sequence

| Phase | Pull request scope | Completion gate |
|---|---|---|
| 1 | Mission, policies, governance decision ledger, and approved donation collections | Every policy effect traces to a Wave proposal or founding source; non-adopted proposals remain visibly non-adopted |
| 2 | Keys and Gates program and sixteen selected-work records | Every work remains `selected_unminted` unless later primary evidence proves otherwise; mint architecture decision is unresolved |
| 3 | Accession and donation operating standards, templates, schemas, constructor/reviewer controls, validation, and CI | Invalid status transitions, broken identifiers, role conflicts, and non-deterministic manifests fail CI |
| 4 | Casey Reas accession lot `6529NM.2026.001` | Donation, token identity, custody, provenance, rights, technical dependencies, condition, preservation, and interpretation are recorded with explicit evidence grades |
| 5 | Transparent generative trait analysis | NextGen compatibility is demonstrated by conformance fixtures; every result is reproducible and explicitly not an aesthetic judgment |
| 6 | On-chain migration specification | Implementable interface, canonical payload rules, authority model, correction semantics, privacy boundary, deployment gates, and Stream bilateral compatibility are complete |
| 7 | Independent review and release | Curatorial, registrar, technical, provenance, rights, security, and governance checks pass; releases are deterministically manifested |

## Constructor and reviewer rule

No governed record is complete solely because one person or agent authored it.

- A **constructor** assembles the record and its evidence packet.
- A **reviewer** independently checks scope, sources, state claims, internal consistency, and required gates.
- A constructor may not be the sole reviewer of the same record revision.
- Review is recorded against an immutable revision hash, not just a mutable filename.
- Factual corrections use an amendment or supersession record. They do not erase the earlier assertion from the evidence trail.

CI enforces structural separation. Governance determines who is authorized to fill each role; repository tooling does not grant institutional authority.

## Controlled unresolved decisions

| Decision | Current state | Required evidence/authority |
|---|---|---|
| Keys and Gates mint topology | `undecided` | Compare dedicated Stream instance with main-Stream subcollection; record governance/deployment authority |
| Keys and Gates token identifiers | `not_assigned` | Successful mint receipts and contract event verification |
| On-chain registry deployment | `not_deployed` | Reviewed specification, implementation, tests, audit, governance approval, and deployment record |
| Public versus restricted Casey donor instruments | `partition_required` | Publish safe summaries and cryptographic references only; keep private instruments outside this repository |

## Resume procedure

1. Read `INDEX.md`, this roadmap, and the most recent entry in `notes/wip/orchestration-ledger.md`.
2. Check the active branch and open pull requests before editing.
3. Reverify live claims with primary sources; record observation times.
4. Work on the earliest incomplete phase whose prerequisites are met.
5. Save research to `notes/research/` or `notes/wip/` before it can be lost to task compaction.
6. Update the index, run validation, obtain independent review, and publish through a pull request.

## 2026-08-01 — PR #2 remediation checkpoint

The V1 on-chain migration specification remains a non-deployment working
standard. Its current remediation completes the full-width
`MUSEUM_BATCH_VECTOR_V1` ID and dependent commitment, strict executable URI
grammar vectors, an offline HTTPS expiry/renewal/history lifecycle check, and
a detached content-addressed TargetRelease signature-bundle fixture with
schema, retrieval reference, and public-key recovery validation. The branch
contains `origin/main` at `9700e842d0c991280b476cc67849d966221a742a` through
merge commit `4329953d66360037122691023b1d0d4da42e9ecd`.

Required next gates are the complete local validation/manifest suite, exact
head CI, independent protocol/security review, governance approval, a real
release-evidence retrieval rehearsal, and a separately reviewed implementation
and audit. No test URI, fixture signer, signature, TargetRelease, or vector
authorizes deployment, admission, custody, accession, or a network write.

## 2026-08-01 — PR #2 post-PR #15 integration checkpoint

PR #15 merged as `bf70ba3fd888d2d1b8add90fe56e913102f8aa68`, preserving the
Casey acquisition construction commit while adding the reachable public
`published_source_commit` `9700e842d0c991280b476cc67849d966221a742a` for
fresh-clone verification. PR #2 merges that new mainline before exact-head
review. Because its governed control-plane test is one of the Casey package's
closed external inventory inputs, the package manifest and its pointer are
regenerated without changing raw observations, snapshots, descriptor results,
or accession/curatorial status.

This integration does not alter the V1 boundary: the Museum wrapper/registry,
TargetRelease signature bundle, URI lifecycle, batch vectors, and Stream
bilateral ontology requirements remain design and conformance material only.
They are not a deployed contract, published TargetRelease, migration, Stream
owner-record write, accession assertion, or network-write authorization.

## 2026-08-01 — historical offline conformance-checker checkpoint (superseded)

The design now has an offline checker for the active one-record release vector
and canonical ABI/authorization transcript, and it explicitly binds state-only
HTTPS reconstruction to the stored assertion row rather than a mutable current
pointer. The checker is test-only and does not query a network, admit a target,
deploy a contract, migrate data, or create accession authority.

At this historical checkpoint the candidate remained draft and unpushed while
independent protocol review resolved two potential design contradictions:
whether the mandated
worst-case batch benchmark corpus is rejected by the pre-write gas formula,
and whether the shared immutable-target opcode policy forbids storage/calls a
usable authority provider or successor registry needs. Resolve those claims
from exact review evidence before final validation or publication. The
consolidated remediation below supersedes this status.

## 2026-08-01 - PR #2 consolidated protocol remediation

The confirmed batch contradiction is closed in the design: the explicit
eligibility formula accepts the 64-record/262,144-byte worst corpus at
base `requiredGas` `12,124,304`; adding the `50,000` caller reserve equals
`12,174,304`, under the `13,000,000` caller gate. The separate measured
deployment threshold remains `9,000,000`, or `9,050,000` with that reserve.
This is a testable eligibility envelope, not a measured-gas claim.

Canonicalizer purity is now a separate policy from target non-upgradeability.
The target policy permits state and declared bounded static dependencies for a
stateful successor or immutable authority provider, while a separately bound
direct governance-executor account (for example, the Museum Safe) remains
outside the TargetRelease/dependency runtime policy; the policy still rejects proxy,
delegatecall/callcode, creation, self-destruct, and recognized upgrade paths.
Target-release evidence binds the exact address, policy document hash,
dependency commitment, source/build evidence, and an acyclic globally unique
release ID. The complete synthetic fixture and its detached bundle are
schema-valid but expressly non-deployment material. V1 designates a successor;
record import is intentionally deferred to a required V2 interface revision.

Head `8a2e26a` was subsequently pushed and PR #2 marked ready for exact-head
review. Later exact-head review identified three final control improvements:
one canonical `NONE` content commitment, a measurable per-URI assertion
capacity gate, and executable binding of gas-corpus constants/formula to the
specification. A subsequent independent review also required provider-
independent emergency freeze/successor authorization, atomic authority/executor
cross-binding refresh in both rotation directions, a genuinely exact-threshold
2-of-3 release bundle, right-aligned SHA-1 tree-OID encoding, and removal of a
forbidden executor-grant reference. Those controls are part of the current
remediation and require fresh exact-head CI/reviewer disposition after
regeneration. Nothing in these
vectors, fixtures, policies, or tests is deployment, accession, custody, or
network-write evidence.

## 2026-08-02 - Stream owner-record evidence correction

The pinned Stream design document publishes a draft owner-record ABI and
EIP-712 signature envelope; the pinned source tree does not contain the
corresponding implementation or deployment and does not establish the stored
record-hash/readback behavior. The Museum V1 design now reproduces the five
draft selectors, two typehashes, and a synthetic signing vector while keeping
the deployment-convergence gate closed. Source-backed implementation,
deployed-runtime verification, exact stored-hash semantics, read surfaces,
nonce tests, and direct/relayed write-read rehearsals remain prerequisites.

The owner-record conformance vector additionally derives its token subject from
the pinned `STREAM_SUBJECT_TOKEN_V1`, chain ID, synthetic Stream Core, and token
ID. A free-form subject is invalid even when the ABI and EIP-712 digest are
otherwise internally coherent.

Later exact-head review closed the Museum mirror side as well. Interface
admission now binds exact Stream Core and adapter addresses, both runtime code
hashes, and the owner-record hash domain/vector. Link creation accepts only a
Museum subject, token ID, and expected-hash guard; it reads back the adapter's
core, collection, derived subject, owner-record hash, domain, and vector and
independently reads the Core's token-collection identity under bounded
exact-length calls. It also requires the Museum subject to be the registered
CAIP-19 identity for the exact chain/Core/token tuple. A retained offline
checker rejects swapped Museum subjects and nonzero collection substitutions
as well as each other substituted value. This remains a conformance design until a source-backed Stream adapter
and deployment satisfy the convergence gate.

## 2026-08-02 - Final custody, title, compliance, and schema-closure pass

The completed Casey accession now has a separate post-accession diligence
record and content-addressed evidence package. It brackets nineteen retained
JSON-RPC responses inside one stable Ethereum finalized block, verifies ENS
and all seven `ownerOf` results against the Museum address, and records all
seven token-specific `getApproved` results as the zero address. A dated OFAC
Sanctions List Service exact-address screen includes a known listed positive
control and eight no-match observations, while expressly excluding identity,
fuzzy-name, 50 Percent Rule, transaction-exposure, and legal-opinion claims.
The title review confirms the executed public institutional title instrument
for the authorized full-gift mode and explains that the unused optional
restricted-annex stub is not an uncompleted title gate.

This pass also removes stale intake-stage Casey instructions from the migration
specification, indexes and supersedes the omitted historical control-plane WIP
note, and closes the live ACCESSION_LOT and WORK_DESCRIPTION nested schemas
against undeclared fields. Focused mutation tests make those controls fail
closed. The final release commitments and exact reviewed head are recorded only
after independent review, CI, and merge; values written earlier in this roadmap
remain historical checkpoints, not release authority.

## 2026-08-04 - Casey generative-system dossier construction

The Museum now has a working generative-system analysis standard and a reusable
documentation template. The method joins exact source/seed reconstruction,
algorithmic score, time and interaction semantics, collection topology,
exact-object close reading, causal counterfactuals, and conservation. It keeps
the existing NextGen-compatible population descriptor separate from rarity,
quality, value, and curatorial significance.

The standard has been applied in constructed research to all five Casey Reas
projects represented by the seven works in accession `6529NM.2026.001`:
*CENTURY*, *Pre-Process*, *Phototaxis*, *923 EMPTY ROOMS*, and *Ex Nihilo
(Cosmos)*. A comparative study treats the image respectively as mutable
adjacency, a surface over behavior, accumulated path history, a displacement
instrument, and temporal memory. Project dossiers contain source locks,
reconstructible algorithms, formal edition topology where available,
token-specific analysis, claim registers, causal-atlas specifications, and
display/preservation requirements.

The package is not a governed accession amendment or a public-release claim.
Required next gates are independent technical replay, independent curatorial
review, source/trace retention where rights permit, rights and accessibility
review for every analytical artifact, cross-environment behavior tests, and
explicit disposition of the published open questions. No current generator
response bytes or derived images were added by this research construction.

User editorial review rejected the initial apparatus-first presentation as
unreadable for an art audience. The working standard, template, package index,
comparative study, and all five dossiers now lead with artistic proposition
and close-looking stakes. Record status, rights limitations, preservation
caveats, method vocabulary, and review controls remain intact but appear in a
research apparatus at the end. This art-first order is now a standard
requirement rather than a Casey-only copy edit.

## 2026-08-04 - Generative-system frontend experience direction

The recommended public architecture makes the project, not the acquisition,
the permanent owner of generative-system analysis. A project hub links to an
art-first **Inside the System** study; each collection object receives a compact
token-specific position and deep link; a gift page explains only why its
particular works entered together. Later acquisitions from the same project
therefore enrich one continuing study without rewriting an earlier gift.

The defining digital feature is a typed possibility-space visualizer that can
represent exhaustive lattices, finite combinatorial fields, explicitly sampled
edition fields, or dynamic state spaces. Museum-held works are an overlay on
that field, never the definition of it, and non-held outputs remain research
subjects rather than collection objects. The first recommended production
pilot is *Pre-Process* because its exact `8 × 3 × 5` topology provides a finite
and reviewable field; the three-work *CENTURY* comparison follows as the first
demonstration of a project study enriched by multiple Museum holdings.

The full route, page, responsive, accessibility, publication-model, and Casey
rollout recommendation is retained in
`notes/wip/2026-08-04-generative-system-frontend-experience.md`. This is
experience direction, not a frontend implementation or public-release claim.

## 2026-08-04 - Inside the System frontend implementation candidate

The complete five-project experience is now implemented for local review in
the isolated frontend worktree `C:\w\museum-inside-system-fe` on branch
`codex/museum-inside-system`, based on `origin/main` commit
`aa77ddf836c3c83cc680054e40247f7e4a78a18d`. Every relevant project page now
opens an art-first **Inside the System** study; object pages locate their exact
accession in that study; and the Casey gift and Stories pages expose the five
projects as a continuing research series.

The implementation provides four reusable visualizer types across the five
Casey projects: the exact 120-position *Pre-Process* lattice, finite
combinatorial structure for *923 EMPTY ROOMS* and *Ex Nihilo (Cosmos)*, an
explicitly observed edition field for *CENTURY*, and a causal dynamic-state
view for *Phototaxis*. Each view has a semantic table alternative, keyboard and
reduced-motion treatment, non-color Museum markers, exact-position selection,
and shareable object-to-study links. The typed study definition belongs to the
project, so a later accession can add a held position without rewriting the
earlier gift.

Changed-file formatting, strict typecheck, lint, 23 focused tests, React Doctor
100/100, desktop browser inspection, keyboard navigation, horizontal-overflow
inspection, and the Next.js production build pass. The branch is not committed,
pushed, merged, deployed, or adopted as a governed publication. Its study data
is a source-neutral frontend research bundle; later promotion into the remote
Museum publication should use optional atomic study groups rather than adding
unavailable study files to the adapter's current all-or-nothing required path
set. The existing exact-seven Casey publication overlay must also become
acquisition-extensible before a later accession is published through it.

## 2026-08-04 - Keys and Gates media delivery design

Live inspection of `/museum/network/programs/6529NM-AP-01` and frontend remote
`main` `11c91ab0576dd69ee3bc4dec671702dbc0d0bf69` established that the selected
work files are already on CloudFront, but the frontend bypasses optimization
and sends full camera originals into small cards. The sixteen sources total
233,601,493 bytes; the first nine observed card loads alone total 148,516,331
bytes. Current outcome records correctly identify only an observed upstream
URL, with no retained binary or SHA-256.

The recommended build separates upstream submission evidence, a rights-gated
Museum-retained master, and deterministic responsive/IIIF derivatives. It uses
a private versioned S3 origin behind CloudFront OAC, immutable digest-addressed
paths, pre-generated AVIF/WebP/JPEG variants and deep-zoom tiles, a separate
`MEDIA_RESOURCE` inventory, and an atomic publication-catalog projection.
High-resolution access belongs on the outcome detail page behind explicit user
activation, file-size/rights disclosure, and reviewed public-use authority; the
grid never requests a master. The full design, rollout, budgets, and unresolved
rights/CDN/IIIF choices are retained in
`notes/wip/2026-08-04-keys-and-gates-media-delivery.md`. No infrastructure,
media, record, or frontend change is claimed by this checkpoint.

## 2026-08-04 - Inside the System comparison instrument

The frontend review candidate now implements the scalable comparison contract
proposed for any generative project: a fixed Museum accession at left and, at
right, any minted output by invocation/token ID, random or trait-filtered
minted selection, or an explicitly labeled project-specific counterfactual or
session manifestation. All five Casey projects now use distinct SVG-native
visual grammars rather than one generic chart.

Compact indexes generated from the pinned complete project snapshots support
3,299 minted works across the five projects. Deterministic suggested
comparisons expose structural neighbors, complements, and uncommon published
trait combinations without marketplace rarity. This remains a local,
uncommitted review candidate. Before public release, the project-study content
and indexes must move into optional atomic governed publication groups.

## 2026-08-04 - Inside the System release-boundary amendment

This checkpoint supersedes only the public-release gate in the preceding
**Inside the System comparison instrument** checkpoint. Version 1 may ship the
study definitions and compact indexes as a versioned frontend display package.
The canonical research evidence remains the pinned snapshots, reviewed
descriptors, and project dossiers in this repository; the frontend package is
a derived interpretive access layer, not a new accession record or source of
record.

The release package contains 3,300 indexed edition records across the five
projects, including *923 EMPTY ROOMS* invocation 0. Official artwork leads each
study. Every synthetic view is persistently labeled **Museum model**. Minted
lookup and filtering use the pinned complete snapshots, and **less often seen**
uses the reviewed NextGen-compatible edition descriptor rather than marketplace
data or an in-browser rarity calculation.

Project-owned atomic publication groups remain the target for a future remote
record profile, especially before acquisitions extend beyond the present gift.
That promotion is no longer a blocker for this derived display release. This
amendment does not claim artist approval, governance adoption, completed
accession QA, or any change to the underlying Museum records.
## 2026-08-04 — Keys and Gates media delivery

The sixteen selected submission sources were re-read from their existing public
CloudFront objects and fixity-checked before conversion. They total 233,601,493
bytes. The constructed delivery manifest now binds each source URL, SHA-256,
byte size, MIME type, oriented dimensions, colour-profile treatment, recorded
rights status, visual description, and three deterministic uncropped WebP
presentation derivatives. Forty-eight derivatives total 16,093,924 bytes and
use new source-digest and transform-version paths with one-year immutable cache
headers. Submitted high-resolution sources remain separately available.

This closes the immediate browser-delivery gap without changing program state.
All sixteen works remain `selected_unminted`; no contract, token, purchase,
title, custody, accession, preservation master, or effective CC0 claim has been
added. Independent review of the constructed media manifest and accessibility
descriptions remains open. The frontend publication, pull-request review,
staging validation, and production validation are the next release gates.

## 2026-08-05 - Inside the System production release

The five Casey project studies and the reusable held-work comparison
instrument are live in production. Frontend PR
[`#3594`](https://github.com/6529-Collections/6529seize-frontend/pull/3594)
merged the experience; exact shell-diagnostic stabilization followed in PR
[`#3602`](https://github.com/6529-Collections/6529seize-frontend/pull/3602).
Production serves revision
`a36a5a437e68d03c886471caefe0bf01afc3827c`.

The release passed three independent adversarial reviews for natural editorial
voice, museum-design quality, and collector interest. Exact staging and
production gates passed the complete selected read-only suites: 14 staging
packs and 13 production packs, with 70 institutional-practice tests and 8
Inside the System desktop/mobile tests in each environment. Production deploy
and E2E evidence are retained in GitHub Actions runs
[`30978958753`](https://github.com/6529-Collections/6529seize-frontend/actions/runs/30978958753)
and
[`30979315540`](https://github.com/6529-Collections/6529seize-frontend/actions/runs/30979315540).

Future acquisitions from a represented project extend its held-position
overlay and receive their own object reading. They do not alter the historical
Casey gift. Optional atomic remote project-study records remain the next data-
interoperability improvement; they are not required for the live derived
display package.
