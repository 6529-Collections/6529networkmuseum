# Open Museum public-record and on-chain transition plan

Date: 2026-08-03

Status: active implementation plan; public operating design, not evidence of a
deployed contract or an adopted governance amendment

## Foundational idea

The Museum record should outlive every interface used to see it.

The 6529 Network Museum is being built in three deliberately separate layers:

1. **Public record now.** During the transitional phase, the Museum repository
   is publicly readable, cloneable, and group-editable through pull requests.
   Anyone can inspect sources and revision history, propose better evidence,
   correct a factual error, deepen scholarship, improve accessibility, or
   strengthen technical and preservation documentation. The published record
   changes only after review and deterministic validation.
2. **Institutional memory on-chain.** Our Fall 2026 goal is for every admitted
   Museum record—from governance decisions and policies to accessions,
   provenance, rights, preservation events, and later corrections—to have an
   on-chain commitment and append-only lineage in a custom contract. Rich
   payloads may remain on content-addressed storage. This is a target, not a
   deployment claim.
3. **Replaceable display.** `6529.io` is a public exhibition and reading
   interface. It presents the art and interprets the record, but it is not the
   record's sole authority. A future frontend should be replaceable without
   losing Museum decisions, history, provenance, citations, or stable public
   identities.

The public expression should be warm and invitational. It must not make a
visitor learn GitHub or contract architecture before encountering the art.

## Visitor-facing language

Primary section:

> **The record outlives the interface**
>
> **An open museum, built in public.**
>
> The Museum's collection records, accession documents, research, policies,
> and curatorial texts are maintained in a public repository. Anyone can read
> the sources and revision history, or propose a correction, new evidence, or
> a stronger interpretation through a pull request. Review and automated
> validation protect the published record while keeping its construction open
> to the network.
>
> This repository is an intermediate home. Our Fall 2026 goal is for every
> admitted Museum record—from governance decisions and policies to accessions,
> provenance, rights, preservation events, and later corrections—to have an
> on-chain commitment and append-only lineage in a custom contract, with larger
> documents held on content-addressed storage. The website will remain what it
> should be: a beautiful, replaceable way to encounter the art, not the only
> place the Museum's memory exists.

Primary actions:

- `Explore the public record`
- `Propose an improvement`
- `How contributions work`

Per-page source language:

> **From the public Museum record**
>
> Read the exact source and revision behind this page, or propose an
> improvement to the Museum's shared record.

Actions:

- `View exact source`
- `Improve this record`

The source line may also expose the short exact source commit as a quiet
machine-verifiable citation. It should never dominate the artwork, title,
essay, or primary object facts.

## Page placement

| Page family | Full foundational section | Quiet exact-source strip |
|---|---:|---:|
| Museum home | concise editorial version below the first art-led collection encounter | repository/publication source |
| About | complete three-layer account | founding principles and this design record |
| Sources and chronology | complete research-oriented account | source matrix |
| Collection | no | collection essay and accession register |
| Artist | no | exact artist profile |
| Project | no | exact project essay |
| Gift/accession | no | gift narrative and accession statement |
| Object | no | public object entry and machine-readable object record |
| Other Museum stories | no | exact story source |

## Link contract

- Exact evidence links use
  `https://github.com/6529-Collections/6529networkmuseum/blob/<40-character-source-commit>/<repository-path>`.
- Contribution links use the canonical `main` edit surface for the exact
  human-authored source file. They must not pretend that an immutable commit is
  editable.
- The contribution guide uses the repository's canonical
  `CONTRIBUTING.md`; the interface may link to its exact-source version for
  reading and to the current `main` version for action.
- Repository paths come from the validated publication contract. The frontend
  must not construct a contribution target from arbitrary URL input.
- Every external link has a clear accessible name and safe external-link
  behavior. No source URL is accepted from unvalidated public Markdown.

## Contribution model

The repository should welcome:

- factual corrections with reliable evidence;
- stronger primary or scholarly sources;
- curatorial arguments and object-level visual analysis;
- provenance, rights, technical, condition, and preservation research;
- accessibility descriptions and careful editorial corrections;
- reproducible tooling and standards improvements.

The guide must explain the difference between proposing a change and changing
the published record. Pull requests preserve group editability; maintainer
review, evidence rules, append-only corrections, and CI preserve institutional
integrity. Restricted donor, legal, custody-security, and personal data never
belongs in the public repository.

## Frontend composition

The full section should use the established 6529 visual language: generous
editorial type, fine rules, monochrome hierarchy, and a simple three-part
sequence (`Public record` / `On-chain memory` / `Open display`). It must avoid
generic feature cards, ornamental gradients, fake dashboards, or process
diagrams that compete with the art.

The per-page source strip should read like a colophon: compact, typographic,
and placed after the substantive page content. It should be visible without
making GitHub the visitor's first encounter.

## Validation and release gates

- The Museum repository publishes `docs/open-museum.md`,
  `docs/onchain-transition.md`, and `CONTRIBUTING.md` inside the governed
  release manifest.
- The frontend activates all three documents atomically with its strict Museum
  publication.
- Tests prove every public page family maps to a validated repository path,
  exact-source links bind the active source commit, and contribution links
  cannot escape the canonical repository.
- Desktop and 390-pixel mobile rendered review covers the full section and at
  least one artist, project, gift, object, collection, and story source strip.
- Staging and production E2E verify content, exact source commit, contribution
  targets, accessibility, no overflow, and no browser errors.
- A final visual sweep confirms that the new institutional idea enriches the
  Museum without returning it to registry-first presentation.

## Open questions and explicit non-claims

- “Fall 2026” is the current delivery goal supplied by the Museum founder. It
  is not evidence of a deployed, audited, or governance-activated contract.
- Contract implementation, audit, deployment, authority activation, and the
  exact migration release remain separate future gates.
- “On-chain” means every admitted institutional record has an on-chain
  commitment and lineage; it does not require large essays, images, or
  preservation packages to be stored directly in contract bytecode or state.
- Group editability does not mean unreviewed direct mutation of the published
  record. It means the network can make concrete, attributable proposals using
  the same public source and review history.
