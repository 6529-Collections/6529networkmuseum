# Record model

## Purpose

GitHub is the Museum's transitional publication and review layer. The repository must remain portable to content-addressed storage and to an append-only on-chain registry without changing the meaning of a record.

## Five record domains

1. **Institution and policy** — founding purpose, collection posture, custody principles, collecting scope, donation acceptance, and future amendments.
2. **Governance** — proposals, decisions, vote observations, source status, and the exact authority each decision grants.
3. **Programs and outcomes** — an approved accession program, its rules and budget, and separately identified selected works.
4. **Accessions and objects** — accession statements, individual object records, rights, title binding, technical/preservation evidence, and curatorial statements.
5. **Protocol migration** — schema IDs, record envelopes, deterministic hashes, append-only lineage, and the intended on-chain authorization model.

## Stable identifiers

- Policy: `6529NM-POL-<NNN>`
- Governance decision: `6529NM-GOV-<wave-serial>`
- Approved collection: `6529NM-COL-<slug>`
- Accession program: `6529NM-AP-<NN>`
- Program outcome: `6529NM-AP-<NN>-OUT-<NNN>`
- Accession lot: `6529NM.<year>.<sequence>`
- Object within an accession: `6529NM.<year>.<sequence>.<item>`
- Gift acceptance authorization: `6529NM.<year>.<sequence>.GAA-<NN>`
- Visual observation set: `6529NM.<year>.<sequence>.VO-<NN>`
- Associated documentation: append `-MD01`, `-IMG01`, `-VID01`, `-TECH01`, `-TX01`, or another registered suffix.

Accession numbers identify Museum records. Chain, artist, and collection information belongs in separate typed fields.

## Authority and source status

Every material assertion must state who made it, when it was observed, and what evidence supports it. Evidence uses the shared five-class profile:

| Class | Meaning | Examples |
|---|---|---|
| A | Directly chain-verifiable | contract, token ID, transaction, block, owner |
| B | Authoritative issuer, artist, or governance source | signed artist statement, adopted Wave proposal, project data |
| C | Museum-generated technical verification | render test, checksum, condition report |
| D | Third-party historical source | marketplace history, bibliography, rarity analysis |
| E | Curatorial interpretation | significance, visual analysis, collection relationship |

Evidence classes describe epistemic status, not importance. Marketplace-derived data must never be presented as if it were chain state.

## Visual observation records

`VISUAL_OBSERVATION` is a reusable, closed evidence-class-C record for static-response and live-render observations. It binds each Museum object to the retained raw-metadata source bytes, the image and generator URLs extracted from those bytes, capture fixity and byte size, viewport/canvas geometry, render-environment completeness, and explicit retention status. Cross-field validation requires source/capture URL agreement, ordered object scope, coherent screenshot-pair state, and projected object/CAIP identity uniqueness.

Timing fields must name what was actually measured. A downloaded file's local `LastWriteTimeUtc` is an observation-completion proxy, not a server `Date` or independently instrumented request timestamp. A command to wait between screenshots records a minimum wait, not exact elapsed time when screenshot and hashing overhead are unmeasured. Unknown frame times, browser versions, and user agents remain `null`; they are never reconstructed from a completion timestamp.

A digest can fix bytes that are not publicly retained, but it cannot make those bytes recoverable. Non-retention and its rights/preservation reason must be explicit. A visual observation is not a condition report, full generator capture, determinism proof, preservation completion, or display-readiness decision.

## Append-only corrections

Published facts are not deleted or overwritten without lineage. A correction is a new record or amendment that:

- identifies the superseded record;
- states what changed and why;
- preserves the prior record's hash;
- has its own authority, effective time, and evidence;
- leaves immutable source material intact.

Current-view indexes may point to the newest record, but they do not erase history.

## Release commitments

`release-artifacts/latest/record-manifest.json` inventories the closed governed
release boundary: records and policies, governance and review controls,
protocol specifications, templates, validation source and tests, plus named
root controls. The exact roots, files, and intentional exclusions are defined
in [`control-plane.md`](control-plane.md). JSON descriptors include a
Stream-shaped `HashRef` using Keccak-256 over constrained RFC 8785 canonical
JSON. Text files also receive LF-normalized SHA-256 digests for repository and
archival tooling.
