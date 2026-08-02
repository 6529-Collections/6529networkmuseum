# Repository index

Read this file first. It indexes both authoritative records and work in progress so design reasoning survives task compaction and agent handoff.

Status vocabulary:

- **source transcription** — faithful copy of an external governing source;
- **adopted** — approved through the recorded Museum governance process;
- **canonical register** — current machine-readable Museum register;
- **working standard** — active design, not yet governance-approved;
- **WIP analysis** — reasoning or proposal retained for review;
- **template** — no factual or completion claim.

## Institutional and policy records

| File | Status | Contents |
|---|---|---|
| [`policies/founding-and-operating-principles.md`](policies/founding-and-operating-principles.md) | source transcription | Mission, public-good posture, TDH governance, custody, permanent holding, pathways, documentation, CC0 default |
| [`policies/general-nft-collecting-scope.md`](policies/general-nft-collecting-scope.md) | adopted | Exact text of winning Wave proposal #1052604 |
| [`policies/donation-acceptance.md`](policies/donation-acceptance.md) | adopted | Exact text of winning Wave proposal #1052812 |
| [`records/collections/approved-collections.json`](records/collections/approved-collections.json) | canonical reviewed register | Four adopted donation preapprovals and two proposals with no adopted effect at snapshot |

## Governance and programs

| File | Status | Contents |
|---|---|---|
| [`records/governance/decisions.json`](records/governance/decisions.json) | canonical reviewed register | Six adopted decisions and two proposals with no adopted effect at snapshot, with source hashes |
| [`governance/github-repository-governance.md`](governance/github-repository-governance.md) | active operating control | Maintainer approval/merge policy, configured team access, and current GitHub Free enforcement limitation |
| [`governance/pull-request-review-policy.md`](governance/pull-request-review-policy.md) | active operating control | Baseline 6529bot reviews, specialist routing matrix, follow-up procedure, and constructor/reviewer boundary |
| [`.github/6529bot.yml`](.github/6529bot.yml) | active review policy | Four-kind automatic production baseline plus bounded, maintainer-requested specialists; Stream review uses the documented central head-bound fallback until catalog upgrade |
| [`.github/workflows/museum-validation.yml`](.github/workflows/museum-validation.yml) | active CI | Required `Museum validation` foundation/full checks plus Ubuntu/Windows deterministic matrix on every PR and main push |
| [`records/programs/6529NM-AP-01/program.json`](records/programs/6529NM-AP-01/program.json) | canonical constructed program record | Keys and Gates rules, source provenance, undecided mint topology, and registrar gates |
| [`records/programs/6529NM-AP-01/selected-works.json`](records/programs/6529NM-AP-01/selected-works.json) | canonical constructed outcome index | Sixteen Wave winners retained as `selected_unminted`, explicitly not acquisition/accession |
| [`records/accessions/register.json`](records/accessions/register.json) | canonical reviewed current-view register | Casey REAS seven-work gift accepted and accessioned; title, rights, curatorial, and technical decisions complete; software preservation remains active stewardship |

## Casey Reas accession dossier

| File | Status | Contents |
|---|---|---|
| [`records/accessions/6529NM.2026.001/accession-statement.json`](records/accessions/6529NM.2026.001/accession-statement.json) | reviewed `ACCESSION_LOT` control-plane record | Completed permanent-collection accession with the exact seven-object identity/receipt schedule, curatorial determination, immutable evidence binding, reviewed rights, amber technical condition, and active preservation duties |
| [`records/accessions/6529NM.2026.001/gift-acceptance-authorization.json`](records/accessions/6529NM.2026.001/gift-acceptance-authorization.json) | reviewed `GIFT_ACCEPTANCE_AUTHORIZATION` | Executed full-gift acceptance under the adopted Art Blocks and donation-policy decisions, with authenticated Wave-status basis and completed title/accession resolution |
| [`records/accessions/6529NM.2026.001/visual-observation-record.json`](records/accessions/6529NM.2026.001/visual-observation-record.json) | reviewed `VISUAL_OBSERVATION` | Seven-object raw-metadata/source-URL binding, static-response and full-viewport screenshot fixity, canvas geometry, timing proxies, non-retention, and explicit observation limits |
| [`records/accessions/6529NM.2026.001/rights/6529NM.2026.001.RIGHTS.01.json`](records/accessions/6529NM.2026.001/rights/6529NM.2026.001.RIGHTS.01.json) | reviewed `RIGHTS_STATEMENT` | Per-object CC BY-NC 4.0 determination covering nine noncommercial Museum use classes with attribution, notice, change-marking, endorsement, and downstream-restriction conditions; sibling files cover all seven objects |
| [`records/accessions/6529NM.2026.001/technical/6529NM.2026.001.01.json`](records/accessions/6529NM.2026.001/technical/6529NM.2026.001.01.json) | reviewed `CONDITION_REPORT` | Per-object amber pass-with-conditions review with exact generator hash, dependency, interaction map, display conditions, and nonblocking preservation actions; sibling files cover all seven objects |
| [`evidence/casey-reas/manifest.json`](evidence/casey-reas/manifest.json) | content-addressed preservation evidence package | Seven retained raw metadata response byte streams, exact chain receipt, accession-level technical evidence, and an explicit boundary between completed review and unfinished autonomous generator preservation |
| [`docs/casey-accession-control.md`](docs/casey-accession-control.md) | active accession control note | Payload-hash basis, immutable Casey publication boundary, cross-file invariants, custody/title boundary, evidence grading, preservation gates, and reviewer boundary |
| [`records/accessions/6529NM.2026.001/objects/6529NM.2026.001.01.json`](records/accessions/6529NM.2026.001/objects/6529NM.2026.001.01.json) | reviewed object record | CENTURY #31 machine-readable object record; sibling files cover the other six objects |
| [`records/accessions/6529NM.2026.001/public/6529NM.2026.001.01.md`](records/accessions/6529NM.2026.001/public/6529NM.2026.001.01.md) | reviewed public page | Public object page for CENTURY #31; sibling pages cover the other six objects |
| [`records/accessions/6529NM.2026.001/public/casey-reas-artist-practice.md`](records/accessions/6529NM.2026.001/public/casey-reas-artist-practice.md) | reviewed public curatorial profile | Sourced artist biography, practice arc, pedagogy/tool-building/publishing context, and institutional exhibition/collection context |
| [`records/accessions/6529NM.2026.001/public/casey-reas-collection-essay.md`](records/accessions/6529NM.2026.001/public/casey-reas-collection-essay.md) | reviewed public curatorial essay | Collection-level reading of rule, behavior, room, and cosmos with static/live documentation boundary |
| [`records/accessions/6529NM.2026.001/public/gift-acceptance-authorization.md`](records/accessions/6529NM.2026.001/public/gift-acceptance-authorization.md) | public human-readable authorization | Full-gift acceptance, exact governing basis, completed accession resolution, and continuing nonblocking stewardship duties |
| [`records/accessions/6529NM.2026.001/accession-certificate.json`](records/accessions/6529NM.2026.001/accession-certificate.json) | reviewed `ACCESSION` certificate | Executed seven-object title bindings, real receipt chronology, institutional custody registration, completed review outcomes, and Stream-aligned event/evidence structure |
| [`records/accessions/6529NM.2026.001/post-accession-diligence.json`](records/accessions/6529NM.2026.001/post-accession-diligence.json) | revision 2 constructed; exact-commit review pending | Exact-block owner, ENS, and token-level approval verification; executed-title interpretation; point-in-time OFAC exact-address screening; residual-risk disposition; and immutable evidence bindings |
| [`records/accessions/6529NM.2026.001/public/custody-title-and-compliance-diligence.md`](records/accessions/6529NM.2026.001/public/custody-title-and-compliance-diligence.md) | revision 2 public-note construction; exact-commit review pending | Human-readable title, custody, encumbrance, sanctions-screening, limitations, and standing-action conclusions for the accessioned lot |
| [`evidence/casey-reas-diligence/manifest.json`](evidence/casey-reas-diligence/manifest.json) | content-addressed post-accession evidence package | Twenty-two-file package retaining nineteen exact JSON-RPC responses, the custody audit, the point-in-time official OFAC UI screening transcript, and package documentation |

## Working standards and architecture

| File | Status | Contents |
|---|---|---|
| [`docs/record-model.md`](docs/record-model.md) | working standard | Record domains, identifiers, evidence classes, correction model |
| [`docs/accession-standard.md`](docs/accession-standard.md) | working standard | Accession statement, object record, curatorial statement, completion gates |
| [`docs/stream-interoperability.md`](docs/stream-interoperability.md) | working standard | Exact Stream envelope, identifiers, museum ontologies, convergence gate |
| [`docs/onchain-design.md`](docs/onchain-design.md) | working standard | General repository-to-chain migration target |
| [`docs/external-works-registry.md`](docs/external-works-registry.md) | WIP analysis | Recommended on-chain registry for donations minted outside Stream |
| [`specs/onchain/contract-migration-v1.md`](specs/onchain/contract-migration-v1.md) | working standard | V1 immutable registry migration design, active-vector/ABI-selector conformance, Stream bilateral-convergence and release gates, and no-deployment status |
| [`specs/onchain/dependency-runtime-nonproxy-v1.json`](specs/onchain/dependency-runtime-nonproxy-v1.json) | governed policy | Exact no-proxy/no-external-call runtime policy for bounded TargetRelease dependency rows; distinct from the direct governance executor |
| [`specs/onchain/release-attestor-policy-v1.fixture.json`](specs/onchain/release-attestor-policy-v1.fixture.json) | non-deployment conformance fixture | Schema-checked synthetic 2-of-3 release-attestor policy whose JCS policy and ABI signer-set commitments demonstrate immutable governance binding; never production authority |
| [`specs/README.md`](specs/README.md) | working standard | Boundary and admission requirements for implementation-ready protocol specifications |
| [`docs/generative-trait-analysis.md`](docs/generative-trait-analysis.md) | working standard | Pinned NextGen-compatible trait prevalence analysis; not quality or curatorial significance |
| [`docs/implementation-roadmap.md`](docs/implementation-roadmap.md) | active working plan | Durable phased build, constructor/reviewer rules, unresolved decisions, and handoff procedure |
| [`docs/standards-crosswalk.md`](docs/standards-crosswalk.md) | working standard | Current operational field-level crosswalk used by the accession and donation templates |
| [`templates/`](templates/) | template | Blank born-digital/tokenized accession, donation, preservation, public/restricted, and review forms; no factual or completion claim |

## Dated WIP notebook

| File | Status | Contents |
|---|---|---|
| [`notes/wip/2026-08-01-stream-coverage-and-gaps.md`](notes/wip/2026-08-01-stream-coverage-and-gaps.md) | WIP analysis | What Stream covers, strengths, implementation caveat, Museum gaps |
| [`notes/wip/2026-08-01-external-works-registry.md`](notes/wip/2026-08-01-external-works-registry.md) | WIP analysis | Options and recommended boundary for externally minted works |
| [`notes/wip/2026-08-01-casey-accession-working-plan.md`](notes/wip/2026-08-01-casey-accession-working-plan.md) | superseded WIP analysis | Historical multi-object numbering and proposed deliverables from the supplied accession draft; the completed accession dossier and register supersede its intake-stage gates |
| [`notes/wip/2026-08-01-nextgen-rarity-analysis.md`](notes/wip/2026-08-01-nextgen-rarity-analysis.md) | WIP analysis | Authoritative source pins, algorithm conclusions, implementation status, and unresolved questions |
| [`notes/wip/2026-08-01-documentation-control-plane.md`](notes/wip/2026-08-01-documentation-control-plane.md) | historical implementation note | Construction rationale, fail-closed remediation history, and remaining Stream/cross-language boundaries for the active documentation-as-code controls; current operation is in [`docs/control-plane.md`](docs/control-plane.md) |
| [`notes/wip/orchestration-ledger.md`](notes/wip/orchestration-ledger.md) | operational WIP | Append-oriented mandate, fixed status facts, active phase, and next actions |

## Generative analysis tooling

| File | Status | Contents |
|---|---|---|
| [`scripts/rarity/nextgen_compat.py`](scripts/rarity/nextgen_compat.py) | working standard | Deterministic input normalization, quality reporting, exact score/rank implementation, and hashes |
| [`scripts/rarity/analyze.py`](scripts/rarity/analyze.py) | working standard | CLI for snapshot analysis |
| [`tests/rarity/`](tests/rarity/) | test fixture | Exact compatibility fixture and coverage for missing/duplicate/tie/hash behavior |

## Research inputs

| File | Status | Contents |
|---|---|---|
| [`notes/research/governance-decision-evidence.md`](notes/research/governance-decision-evidence.md) | research input | Independently verified Museum Wave governance evidence, source/interpretation boundary, and append-only decision format |
| [`notes/research/museum-standards-crosswalk.md`](notes/research/museum-standards-crosswalk.md) | research input | Foundation source register and public-practice research retained as background to the current operational crosswalk |
| [`notes/research/museum-standards-crosswalk-luna.md`](notes/research/museum-standards-crosswalk-luna.md) | research addendum | Template-alignment delta: exact record-control payload-hash semantics and current Casey/Keys and Gates states |
| [`notes/research/repository-ci-architecture.md`](notes/research/repository-ci-architecture.md) | research input | Proposed canonical-record, schema, status-gate, manifest, CI, and release architecture |
| [`notes/research/external-registry-review.md`](notes/research/external-registry-review.md) | research input | Stream boundary analysis and synchronized, non-deployment V1 registry/hash/URI/release-bundle vectors |
| [`notes/research/nextgen-rarity-method.md`](notes/research/nextgen-rarity-method.md) | research input | Exact production NextGen trait-measure archaeology and reproducibility requirements |
| [`notes/research/casey-reas-art-technical-research.md`](notes/research/casey-reas-art-technical-research.md) | research input | Primary-source art-historical, technical, display, and preservation research for seven donated works, with dated gift-status supersession note |
| [`notes/research/casey-reas-onchain-evidence.md`](notes/research/casey-reas-onchain-evidence.md) | research input | ENS resolution, seven token identities, common donation transaction, custody, metadata, and transfer evidence |
| [`notes/research/keys-and-gates-evidence.md`](notes/research/keys-and-gates-evidence.md) | research input | Full program rule, voting, artist statement, selected-work, CC0/consent, and unminted-status evidence inventory |

## Evidence snapshots

| File | Status | Contents |
|---|---|---|
| [`evidence/waves/museum-wave/README.md`](evidence/waves/museum-wave/README.md) | immutable evidence index | Complete authenticated 2026-08-01 Museum Wave snapshot, rendered history, source index, proposals, and SHA-256 digests |
| [`evidence/casey-reas-collection-snapshots/README.md`](evidence/casey-reas-collection-snapshots/README.md) | reviewed acquisition and descriptor evidence package | Full Art Blocks Hasura/tokenURI observations, reconstructed request provenance, 17 explicit cross-check exclusions, closed-scope/no-follow root manifest, direct PR #4 byte recomputation, and independently reviewed transparent descriptors for the five Casey REAS projects in lot `6529NM.2026.001` |

## Integrity tooling

| File | Status | Contents |
|---|---|---|
| [`schemas/`](schemas/) | active working standard | Bootstrap governance/collection/accession schemas plus controlled vocabularies and Stream-compatible profiles |
| [`scripts/bootstrap_validate.py`](scripts/bootstrap_validate.py) | active CI control | Source-derived governance, raw evidence manifest, record-control, local-link, and public-safety checks |
| [`scripts/safe_fetch.py`](scripts/safe_fetch.py) | active CI control | Pinned HTTPS fetch primitive with IDNA/endpoint filtering, IP pinning, strict framing/headers, bounded JSON POST/GET requests, redirect rechecks, streamed caps, and observations |
| [`scripts/check_fetch_guard.py`](scripts/check_fetch_guard.py) | active CI control | Alias/import-aware AST guard rejecting unmediated network, dynamic-import, and command-line fetch implementations across all Python, including tests |
| [`scripts/validate.py`](scripts/validate.py) | working standard | JSON Schema, semantic, secret, cross-reference, state, status, and commitment validation |
| [`scripts/generate_manifest.py`](scripts/generate_manifest.py) | working standard | Deterministic SHA-256 and JCS/Keccak release commitments over the closed governed release inventory |
| [`scripts/acquire_casey_custody_audit.py`](scripts/acquire_casey_custody_audit.py) | reproducible evidence acquisition | Bracketed finalized-state ENS, `ownerOf`, and token-level `getApproved` observations with exact JSON-RPC response retention and stable block-hash enforcement |
| [`scripts/build_casey_diligence_manifest.py`](scripts/build_casey_diligence_manifest.py) | active CI control | Complete-inventory raw-byte manifest builder and idempotence check for the Casey post-accession diligence evidence package |
| [`specs/onchain/`](specs/onchain/) | active design conformance | Offline-only contract-migration vectors for batch eligibility, URI canonical identity, HTTPS assertion lifecycle, address-bound TargetRelease evidence/signatures, and ABI/allowlist reconstruction; never deployment evidence |
| [`tests/`](tests/) | working standard | Valid record chain and negative control-plane fixtures |
| [`.github/workflows/museum-validation.yml`](.github/workflows/museum-validation.yml) | required CI | Required `Museum validation` check on pull requests and main pushes |
| [`docs/control-plane.md`](docs/control-plane.md) | working standard | Control-plane contract and local commands |
| [`release-artifacts/latest/record-manifest.json`](release-artifacts/latest/record-manifest.json) | canonical release commitment | Deterministic manifest for governed records and control-plane source |
| [`schemas/accession-program.schema.json`](schemas/accession-program.schema.json) | active local schema | Rigorous Keys and Gates program record contract |
| [`schemas/program-outcome-index.schema.json`](schemas/program-outcome-index.schema.json) | active local schema | Sixteen-row selected-work index contract |
| [`schemas/program-outcome.schema.json`](schemas/program-outcome.schema.json) | active local schema | Individual selected-work registrar outcome contract |

## Maintenance rule

Before ending a substantive design or research turn:

1. write new conclusions to a canonical document or dated WIP note;
2. record uncertainty and implementation status, not only conclusions;
3. update this index;
4. never promote WIP to adopted policy without a governance record;
5. run repository validation once the tooling exists.
