# Public identity inventory completion

Status: completed in canonical reviewed projection B3

## Why this increment exists

The strict frontend publication assembler evaluated canonical reviewed source
`311ae4281893f404472b8f7ba94454a57a2cd572` and correctly refused activation.
Four generated public entities were not declared by the governed identity
inventory:

- `6529NM-I-0001` (6529 Network Museum);
- `6529NM-C-0001` (permanent Collection);
- `6529NM-ACC-ENT-0001` (Casey Reas accession);
- `6529NM-RP-0001` (*The System in Seven States* Research Publication).

The Research Publication also had a generated public slug and canonical route
that were absent from `public_slug_inventory`. This was a source-contract gap,
not a frontend defect. Catalog activation from reviewed candidate B2 was
stopped before any release pointer or catalog bytes were written.

## Correction design

`schemas/public-entity-identity-inventory.json` version 1.4.0 now binds every
generated public identity category, including the institution, Collection,
organizations, Curated Acquisitions, Acquisition Programs, accession, and
Research Publications. The generator resolves formerly hard-coded singleton
identities through those bindings and proves exact equality between every
generated public entity and every governed entity binding. The schema requires
the complete closed set of identity categories. Missing, additional, duplicate,
retired, or pattern-invalid bindings fail before generation.

`6529NM-RP-0001` is also declared in `public_slug_inventory` at
`/museum/network/research/the-system-in-seven-states`.

Tests cover exact whole-graph inventory equality, the four formerly missing
identities, the Casey Research Publication route, category closure, missing
binding refusal, and source-order independence.

## Release boundary

This correction changes the reviewed graph contract. It therefore creates a
new pending candidate A3 rather than silently editing reviewed B2. The complete
326-record graph, visitor bundle, publication inventory, and release manifest
are regenerated in pending state. Independent review must produce B3 as an
exact direct child of canonical A3. Publication catalog activation C may bind
only to canonical B3.

The exact A3 manifest commitments are computed only after this ledger and every
other governed byte are final. They are recorded in the immutable candidate
commit and release review, avoiding a self-referential manifest claim inside a
file covered by that manifest.

## Completion

Candidate A3 merged as `de6539004fccee7d850d1e9cae7545ccbdf375bf`.
Its direct reviewed child B3 merged as
`bf517353ef861e91f5137908daca514b81578b4d`. The first publication-catalog
activation attempt was subsequently stopped before merge when independent
frontend-contract review found that the relation-identity inventory was not
yet included in the closed visitor publication. That separate correction is
tracked in `2026-08-09-relation-identity-publication-closure.md`.
