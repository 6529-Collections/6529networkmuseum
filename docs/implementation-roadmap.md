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
