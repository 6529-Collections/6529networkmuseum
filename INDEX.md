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
| `policies/donation-acceptance.md` | pending creation | Exact text of winning Wave proposal #1052812 |
| [`records/collections/approved-collections.json`](records/collections/approved-collections.json) | pending creation | Canonical donation preapproval list |

## Governance and programs

| File | Status | Contents |
|---|---|---|
| `records/governance/decisions.json` | pending creation | Six adopted and two non-adopted proposal observations |
| `records/programs/6529NM-AP-01/program.json` | pending creation | Keys and Gates rules and current stage |
| `records/programs/6529NM-AP-01/selected-works.json` | pending creation | Sixteen Wave winners, each explicitly pending acquisition/accession verification |
| `records/accessions/register.json` | pending creation | Canonical accession register; initially empty |

## Working standards and architecture

| File | Status | Contents |
|---|---|---|
| [`docs/record-model.md`](docs/record-model.md) | working standard | Record domains, identifiers, evidence classes, correction model |
| [`docs/accession-standard.md`](docs/accession-standard.md) | working standard | Accession statement, object record, curatorial statement, completion gates |
| [`docs/stream-interoperability.md`](docs/stream-interoperability.md) | working standard | Exact Stream envelope, identifiers, museum ontologies, convergence gate |
| [`docs/onchain-design.md`](docs/onchain-design.md) | working standard | General repository-to-chain migration target |
| [`docs/external-works-registry.md`](docs/external-works-registry.md) | WIP analysis | Recommended on-chain registry for donations minted outside Stream |
| [`docs/generative-trait-analysis.md`](docs/generative-trait-analysis.md) | working standard | Pinned NextGen-compatible trait prevalence analysis; not quality or curatorial significance |

## Dated WIP notebook

| File | Status | Contents |
|---|---|---|
| [`notes/wip/2026-08-01-stream-coverage-and-gaps.md`](notes/wip/2026-08-01-stream-coverage-and-gaps.md) | WIP analysis | What Stream covers, strengths, implementation caveat, Museum gaps |
| [`notes/wip/2026-08-01-external-works-registry.md`](notes/wip/2026-08-01-external-works-registry.md) | WIP analysis | Options and recommended boundary for externally minted works |
| [`notes/wip/2026-08-01-casey-accession-working-plan.md`](notes/wip/2026-08-01-casey-accession-working-plan.md) | WIP analysis | Multi-object numbering and proposed deliverables from the supplied accession draft |
| [`notes/wip/2026-08-01-nextgen-rarity-analysis.md`](notes/wip/2026-08-01-nextgen-rarity-analysis.md) | WIP analysis | Authoritative source pins, algorithm conclusions, implementation status, and unresolved questions |

## Generative analysis tooling

| File | Status | Contents |
|---|---|---|
| [`scripts/rarity/nextgen_compat.py`](scripts/rarity/nextgen_compat.py) | working standard | Deterministic input normalization, quality reporting, exact score/rank implementation, and hashes |
| [`scripts/rarity/analyze.py`](scripts/rarity/analyze.py) | working standard | CLI for snapshot analysis |
| [`tests/rarity/`](tests/rarity/) | test fixture | Exact compatibility fixture and coverage for missing/duplicate/tie/hash behavior |

## Integrity tooling

| File | Status | Contents |
|---|---|---|
| `schemas/` | pending creation | JSON Schemas and Stream-compatible profiles |
| `scripts/validate.py` | pending creation | Structural, semantic, secret, and status validation |
| `scripts/generate_manifest.py` | pending creation | Deterministic SHA-256 and JCS/Keccak release commitments |
| `release-artifacts/latest/record-manifest.json` | pending generation | Current governed-file manifest |

## Maintenance rule

Before ending a substantive design or research turn:

1. write new conclusions to a canonical document or dated WIP note;
2. record uncertainty and implementation status, not only conclusions;
3. update this index;
4. never promote WIP to adopted policy without a governance record;
5. run repository validation once the tooling exists.
