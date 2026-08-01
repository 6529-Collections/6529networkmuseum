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

## Append-only corrections

Published facts are not deleted or overwritten without lineage. A correction is a new record or amendment that:

- identifies the superseded record;
- states what changed and why;
- preserves the prior record's hash;
- has its own authority, effective time, and evidence;
- leaves immutable source material intact.

Current-view indexes may point to the newest record, but they do not erase history.

## Release commitments

`release-artifacts/latest/record-manifest.json` inventories governed files. JSON descriptors include a Stream-shaped `HashRef` using Keccak-256 over constrained RFC 8785 canonical JSON. Text files also receive LF-normalized SHA-256 digests for repository and archival tooling.
