# Museum data architecture publication

Status: active construction and release ledger

## Mandate

Define the 6529 Network Museum's own collections, description, provenance,
preservation, presentation, packaging, authority, and chain-identity
architecture before treating 6529Stream as a dependency. Publish the result in
the canonical repository and as an intelligible section of the Museum website.

This is also a Museum education programme for artists and collectors. It must
teach the practical distinctions behind the data: a work and a token;
provenance and proof; a live work and its documentation; a checksum and
authenticity; custody and accession; a transfer package and a preservation
repository. The standards explain how the Museum works and help the public make
better records, gifts, acquisitions, presentation, and preservation decisions.

The public treatment has two readings. Its opening pages answer ordinary museum
questions in direct language and through the Casey Reas accession. The same
pages then provide the pinned authority, version, data structures, conformance
rules, machine serializations, validation boundary, and exact implementation
status required by registrars, conservators, engineers, and future contract
implementers.

## Fixed editorial decisions

- One standard cannot substitute for another. Spectrum governs procedure;
  CIDOC CRM and PROV-O express relations; LIDO delivers catalogue records;
  PREMIS records preservation; Getty vocabularies control names and terms;
  IIIF presents media; C2PA carries signed media assertions; BagIt transfers
  packages; OCFL versions repository content; CAIP-19 identifies chain assets.
- Every page begins with the human question the standard answers, why that
  question matters, and a concrete Museum example.
- Technical sections preserve the standard's own terminology and distinguish a
  conceptual mapping from a conformant serialization.
- The Casey package is described as it exists. Fields that can be mapped are
  not represented as completed LIDO, PREMIS, CRM, PROV-O, IIIF, C2PA, BagIt, or
  OCFL deliverables until those deliverables are generated and validated.
- Stream is outside the normative Museum profile in this release. A later
  convergence review will measure Stream against the Museum profile and record
  compatible fields, adapters, and unavoidable differences.

## Publication boundary

- `docs/data-architecture.md`: public introduction and integrated application
  profile.
- `docs/data-architecture/profile.json`: machine-readable version and standards
  register.
- `docs/data-architecture/*.md`: eleven public standards profiles.
- `docs/data-architecture/casey-reas-implementation.md`: honest implementation
  crosswalk for accession `6529NM.2026.001`.
- `docs/data-architecture/casey-reas-machine-schedule.json`: closed exact-field
  audit of all seven canonical object records.
- Updated crosswalk, accession, stewardship, Stream-interoperability, index,
  roadmap, and manifest.
- Website landing page and eleven standards routes, activated atomically from
  the exact canonical Museum commit.

## Release state

- 2026-08-05: four independent research lanes completed source, status,
  version, licensing, scope, and implementation checks for all eleven standards.
- Canonical introduction, eleven profiles, machine register/schema, Casey
  implementation audit, and semantic-authority corrections are constructed.
- Full local control plane before the independent correction pass: 139 tests
  passed with one platform skip; bootstrap, fetch guard, full validator,
  institutional inventory, program media, Casey diligence manifest, and Casey
  3,300-token snapshot verification passed.
- Independent review corrections incorporated: CIDOC digital-object
  domain/range and software-agent boundaries; P35 condition relation; TriG
  serialization; LIDO resource-set rights; PREMIS conformance criteria; PROV
  Bundle typing; populated IIIF shape and rights URI; C2PA assertion provenance;
  OCFL version-inventory rule; and a complete public-language edit.
- Post-correction focused profile tests, bootstrap, and whitespace validation:
  passed. The final Casey audit then added an exact seven-object machine
  schedule, a second closed schema, one-to-one semantic validation, release-
  manifest path binding, and primary-validator integration. Eight focused tests,
  the architecture validator, the full Museum/Casey validator, manifest check,
  and whitespace check pass.
- Current candidate manifest after reconciliation with the rights handbook: 345
  entries; SHA-256
  `sha256:258a2aa6a970cc84d036de511902cbc1d5fbb5141067cc146fe83ac879d20544`;
  Keccak-256
  `0x9ccca279ca25f1d0b65b2430168dd192a87dee77b682f63db25de44fc899ea26`.
- Final exact-tree full CI-equivalent rerun: passed in 461.1 seconds. The
  complete suite ran 141 tests with one expected Windows capability skip;
  bootstrap, fetch guard, program-media fixity, institutional-source inventory,
  full Museum/Casey validation, manifest verification, NextGen compatibility,
  Casey mutation controls, the 3,300-token snapshot verifier, the diligence
  manifest, and whitespace checks all passed.
- Museum repository PR #30: exact-head follow-up validation in progress.
- Frontend PR: pending.
- Staging and production qualification: pending.

### Review follow-up

PR #30 reconciled cleanly with the concurrent rights-handbook release. All
three hosted Museum jobs passed on the reconciled head. A head-bound 6529bot
follow-up review returned no findings and verified the schema, semantic
validator, manifest, and Casey one-to-one schedule controls. Its one
non-blocking coverage observation was adopted: the Casey audit and test now
require all eleven full canonical standard names rather than accepting a
first-word match.

## Deferred to the next compatibility phase

- Stream field-by-field conformance report and adapter work.
- Production CRM/RDF, PROV-O, LIDO XML, PREMIS XML/OWL, IIIF, C2PA, BagIt, and
  OCFL exports where the current implementation status is not yet complete.
- On-chain contract deployment. This publication defines semantics and
  admission evidence; it is not deployment evidence.
