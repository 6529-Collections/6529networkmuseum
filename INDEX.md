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
| [`.github/6529bot.yml`](.github/6529bot.yml) | active review policy | Multi-lane Museum-relevant review profile and bounded spend/admission policy for every PR |
| [`.github/workflows/museum-validation.yml`](.github/workflows/museum-validation.yml) | active CI | Required `Museum validation` foundation/full checks plus Ubuntu/Windows deterministic matrix on every PR and main push |
| `records/programs/6529NM-AP-01/program.json` | pending creation | Keys and Gates rules and current stage |
| `records/programs/6529NM-AP-01/selected-works.json` | pending creation | Sixteen Wave winners, each explicitly pending acquisition/accession verification |
| [`records/accessions/register.json`](records/accessions/register.json) | canonical reviewed register | Casey Reas donation received; seven-work accession documentation in progress |

## Working standards and architecture

| File | Status | Contents |
|---|---|---|
| [`docs/record-model.md`](docs/record-model.md) | working standard | Record domains, identifiers, evidence classes, correction model |
| [`docs/accession-standard.md`](docs/accession-standard.md) | working standard | Accession statement, object record, curatorial statement, completion gates |
| [`docs/stream-interoperability.md`](docs/stream-interoperability.md) | working standard | Exact Stream envelope, identifiers, museum ontologies, convergence gate |
| [`docs/onchain-design.md`](docs/onchain-design.md) | working standard | General repository-to-chain migration target |
| [`docs/external-works-registry.md`](docs/external-works-registry.md) | WIP analysis | Recommended on-chain registry for donations minted outside Stream |
| [`docs/implementation-roadmap.md`](docs/implementation-roadmap.md) | active working plan | Durable phased build, constructor/reviewer rules, unresolved decisions, and handoff procedure |
| [`docs/standards-crosswalk.md`](docs/standards-crosswalk.md) | working standard | Current operational field-level crosswalk used by the accession and donation templates |
| [`templates/`](templates/) | template | Blank born-digital/tokenized accession, donation, preservation, public/restricted, and review forms; no factual or completion claim |

## Dated WIP notebook

| File | Status | Contents |
|---|---|---|
| [`notes/wip/2026-08-01-stream-coverage-and-gaps.md`](notes/wip/2026-08-01-stream-coverage-and-gaps.md) | WIP analysis | What Stream covers, strengths, implementation caveat, Museum gaps |
| [`notes/wip/2026-08-01-external-works-registry.md`](notes/wip/2026-08-01-external-works-registry.md) | WIP analysis | Options and recommended boundary for externally minted works |
| [`notes/wip/2026-08-01-casey-accession-working-plan.md`](notes/wip/2026-08-01-casey-accession-working-plan.md) | WIP analysis | Multi-object numbering and proposed deliverables from the supplied accession draft |
| [`notes/wip/orchestration-ledger.md`](notes/wip/orchestration-ledger.md) | operational WIP | Append-oriented mandate, fixed status facts, active phase, and next actions |

## Research inputs

| File | Status | Contents |
|---|---|---|
| [`notes/research/governance-decision-evidence.md`](notes/research/governance-decision-evidence.md) | research input | Independently verified Museum Wave governance evidence, source/interpretation boundary, and append-only decision format |
| [`notes/research/museum-standards-crosswalk.md`](notes/research/museum-standards-crosswalk.md) | research input | Foundation source register and public-practice research retained as background to the current operational crosswalk |
| [`notes/research/museum-standards-crosswalk-luna.md`](notes/research/museum-standards-crosswalk-luna.md) | research addendum | Template-alignment delta: exact record-control payload-hash semantics and current Casey/Keys and Gates states |
| [`notes/research/repository-ci-architecture.md`](notes/research/repository-ci-architecture.md) | research input | Proposed canonical-record, schema, status-gate, manifest, CI, and release architecture |
| [`notes/research/nextgen-rarity-method.md`](notes/research/nextgen-rarity-method.md) | research input | Exact production NextGen trait-measure archaeology and reproducibility requirements |
| [`notes/research/casey-reas-art-technical-research.md`](notes/research/casey-reas-art-technical-research.md) | research input | Primary-source art-historical, technical, display, and preservation research for seven donated works |
| [`notes/research/casey-reas-onchain-evidence.md`](notes/research/casey-reas-onchain-evidence.md) | research input | ENS resolution, seven token identities, common donation transaction, custody, metadata, and transfer evidence |
| [`notes/research/keys-and-gates-evidence.md`](notes/research/keys-and-gates-evidence.md) | research input | Full program rule, voting, artist statement, selected-work, CC0/consent, and unminted-status evidence inventory |

## Evidence snapshots

| File | Status | Contents |
|---|---|---|
| [`evidence/waves/museum-wave/README.md`](evidence/waves/museum-wave/README.md) | immutable evidence index | Complete authenticated 2026-08-01 Museum Wave snapshot, rendered history, source index, proposals, and SHA-256 digests |

## Integrity tooling

| File | Status | Contents |
|---|---|---|
| [`schemas/`](schemas/) | active working standard | Bootstrap governance/collection/accession schemas plus controlled vocabularies and Stream-compatible profiles |
| [`scripts/bootstrap_validate.py`](scripts/bootstrap_validate.py) | active CI control | Source-derived governance, raw evidence manifest, record-control, local-link, and public-safety checks |
| [`scripts/validate.py`](scripts/validate.py) | working standard | JSON Schema, semantic, secret, cross-reference, state, status, and commitment validation |
| [`scripts/generate_manifest.py`](scripts/generate_manifest.py) | working standard | Deterministic SHA-256 and JCS/Keccak release commitments |
| [`tests/`](tests/) | working standard | Valid record chain and negative control-plane fixtures |
| [`.github/workflows/museum-validation.yml`](.github/workflows/museum-validation.yml) | required CI | Required `Museum validation` check on pull requests and main pushes |
| [`docs/control-plane.md`](docs/control-plane.md) | working standard | Control-plane contract and local commands |
| [`release-artifacts/latest/record-manifest.json`](release-artifacts/latest/record-manifest.json) | canonical register commitment | Current governed-file manifest |

## Maintenance rule

Before ending a substantive design or research turn:

1. write new conclusions to a canonical document or dated WIP note;
2. record uncertainty and implementation status, not only conclusions;
3. update this index;
4. never promote WIP to adopted policy without a governance record;
5. run repository validation once the tooling exists.
