# Casey Reas: the first implementation audit

Status: public implementation crosswalk; reviewed against canonical records

## What can the Museum already say, and what must it build next?

The seven works in the Casey Reas gift are the Museum's first full test of this
architecture. Each work is at once an artwork, a token on the Ethereum
blockchain, a running software system, a displayable image, a collection object,
and a subject of research. The records must connect those aspects without
treating one as a substitute for another.

The Museum has accepted and accessioned the gift. It retained the Art Blocks
metadata responses, verified the seven token identities and shared custody
transfer, recorded title and rights conclusions, completed technical and
curatorial reviews, and published the accession dossier. The live generators
rendered during the Museum's observations; a complete, self-contained copy of
each generator and its dependencies has not yet been preserved.

This crosswalk measures the canonical records against eleven standards. It
marks what is already evidenced and what still requires a generated export,
validation report, or preservation package.

## The seven collection objects

| Museum object | Work | External chain asset |
|---|---|---|
| `6529NM.2026.001.01` | *CENTURY #31* | `eip155:1/erc721:0xa7d8d9ef8d8ce8992df33d8b8cf4aebabd5bd270/100000031` |
| `6529NM.2026.001.02` | *CENTURY #724* | `eip155:1/erc721:0xa7d8d9ef8d8ce8992df33d8b8cf4aebabd5bd270/100000724` |
| `6529NM.2026.001.03` | *CENTURY #401* | `eip155:1/erc721:0xa7d8d9ef8d8ce8992df33d8b8cf4aebabd5bd270/100000401` |
| `6529NM.2026.001.04` | *Pre-Process #63* | `eip155:1/erc721:0x99a9b7c1116f9ceeb1652de04d5969cce509b069/383000063` |
| `6529NM.2026.001.05` | *Phototaxis #308* | `eip155:1/erc721:0xa7d8d9ef8d8ce8992df33d8b8cf4aebabd5bd270/164000308` |
| `6529NM.2026.001.06` | *923 EMPTY ROOMS #713* | `eip155:1/erc721:0x145789247973c5d612bf121e9e4eef84b63eb707/1000713` |
| `6529NM.2026.001.07` | *Ex Nihilo (Cosmos) #248* | `eip155:1/erc721:0x0000000c687daed0fba60d1dba4e5f6149e8b894/248` |

The seven tokens moved to the Museum in transaction
`0xbdde33b32d4b70335b10cbd37c0b00a027844f14c900d82aa4f75b7a7b390498`
at block `25,660,311`. The shared transaction does not merge the seven Museum
objects or their separate mint histories.

## Where the first accession stands

The table uses five implementation states:

| State | Meaning |
|---|---|
| `conceptual_mapping` | The Museum has adopted the role and designed the local mapping. |
| `source_fields_present` | Canonical records contain enough reviewed source data for a material projection. |
| `serialized` | A named, version-pinned standard serialization has been generated. |
| `validated` | The serialization has passed the standard and Museum profile validators. |
| `operational` | The process runs as part of normal Museum collections management. |

| Standard | Casey state | Evidence already present | Next controlled deliverable |
|---|---|---|---|
| Spectrum 5.1 | `operational` | object entry, gift acceptance, acquisition and accession, cataloguing, custody/location, condition and technical review, rights, audit, amendment and public-use controls | maintain the procedures and audit their execution for later accessions |
| CIDOC CRM 7.1.3 | `source_fields_present` | stable objects, actors, typed events, dates, sources, rights, condition assessments and corrections | Museum extension terms, RDF/JSON-LD projection and SHACL validation |
| LIDO 1.1 | `source_fields_present` | public titles, creators, project context, events, repository, credit, resources and record provenance | reconcile authorities and AAT terms; generate XML; validate XSD and Museum Schematron |
| PREMIS 3.0 | `source_fields_present` | Museum objects, event history, agents, metadata fixity, environments, outcomes and permissions sufficient for a PREMIS mapping | complete generator capture; PREMIS mapping; XML/RDF export and validation |
| PROV-O | `source_fields_present` | Museum source URIs, evidence classes, event history, agents, dates, derived records and correction lineage sufficient for a PROV-O mapping | release-bounded TriG Bundle, Museum SHACL shapes and PROV constraint report |
| Getty AAT and ULAN | `conceptual_mapping` | human-readable artist, medium, technique and work-type terms | reconcile Casey Reas to ULAN if available; assign reviewed AAT URIs and retain term labels/snapshots |
| IIIF Presentation API 3.0 | `conceptual_mapping` | approved still URLs, live generator routes, credits, rights, dimensions and object ordering | preserve authorized image bytes; publish one collection Manifest and seven object Manifests |
| C2PA Content Credentials 2.4 | `conceptual_mapping` | source, creation context and fixity records for current documentation | create authorized derivatives; sign Museum assertions; retain manifests and trust-validation reports |
| BagIt / RFC 8493 | `conceptual_mapping` | content-addressed evidence manifests and closed inventory checks | construct and independently validate one accession transfer bag and object-level preservation bags |
| OCFL 1.1 | `conceptual_mapping` | stable Museum IDs, append-only amendments, digest and version history | ingest each managed object into validated OCFL storage with external inventory commitments |
| CAIP-19 | `source_fields_present` | exact chain, token standard, normalized contract and decimal token ID for all seven works | publish a closed CAIP-19 Museum profile validator and retain state observations separately |

## One work through the architecture

### *CENTURY #31*

The Museum object is `6529NM.2026.001.01`. Its external asset identifier is
`eip155:1/erc721:0xa7d8d9ef8d8ce8992df33d8b8cf4aebabd5bd270/100000031`.
The retained Art Blocks metadata response has SHA-256
`e193e1436718786aac6e96aac69d70b3ecbb224576626378137683bbf6916e74`.
The recorded generator route uses p5.js 1.0.0 and rendered changing output in
the controlled observation.

Those facts become several linked records:

- **Spectrum** records how the Museum received, accepted, accessioned, checked,
  catalogued, and continues to care for the object.
- **CIDOC CRM** links the work, token, artist, donor, transfer, title record,
  accession, condition observation, and publication as distinct entities and
  events.
- **LIDO** provides a reviewed public catalogue record suitable for exchange.
- **PREMIS** distinguishes the intellectual work, retained metadata file,
  observed environment, documentation surrogates, preservation Events, and the
  still-incomplete autonomous Representation.
- **PROV-O** connects the published account to the source records, the
  activities that produced them, and the agents associated with those
  activities.
- **Getty vocabularies** give stable identifiers to artist, work-type, medium,
  and technique terms.
- **IIIF** presents retained visual resources, sequence, annotation, rights, and
  links to the live work.
- **C2PA** can bind a signed Museum assertion to a Museum-created still or other
  derivative.
- **BagIt** verifies the completeness and fixity of a transferable evidence
  snapshot.
- **OCFL** preserves that snapshot and later versions without rewriting the
  earlier state.
- **CAIP-19** identifies the external token while the Museum ID continues to
  identify the institutional collection object.

## What is preserved today

All seven objects are accessioned. The Museum has verified their token
identities and retained metadata fixity; the official generator routes rendered
during observation. Preservation remains in progress because the Museum has not
yet retained complete, self-contained generator and dependency packages for
autonomous rendering, and it has not produced BagIt or OCFL preservation
objects. The machine preservation status for all seven works is `in_progress`.

The current record therefore treats:

- retained metadata responses as candidate PREMIS File records in the planned
  mapping;
- generator routes and observed digests as dated observations until the
  corresponding bytes and dependencies are retained;
- screenshots and videos as documentation surrogates;
- no current resource as a complete PREMIS Representation;
- no current directory as a validated BagIt bag or OCFL object; and
- the current JSON records as Museum records that can support future CIDOC CRM,
  LIDO, PREMIS, and PROV-O projections, not as validated exports of those
  standards.

The accession is complete as an institutional act; digital preservation work
continues.

## Exact machine schedule

The closed [Casey Reas machine schedule](casey-reas-machine-schedule.json)
binds each Museum object ID to its title, CAIP-19-shaped asset ID, custody log,
retained metadata digest, observed generator digest, accession state, and
preservation state. It also records the shared custody transaction and block and
states that generator response bytes were not retained. CI compares every field
to the seven canonical object records; presence somewhere in the document is
not sufficient.

## Machine checks for this crosswalk

The canonical profile is
[`profile.json`](profile.json). A release validator checks that:

1. exactly eleven standard entries are present;
2. every standard slug is unique and resolves to a public document;
3. every implementation state belongs to the closed state vocabulary;
4. this crosswalk exists and is release-manifest-declared;
5. the exact seven-row machine schedule agrees one-to-one with the canonical
   object records, including titles, CAIP-19 identities, custody transaction,
   block and log, metadata and generator-observation digests, accession state,
   preservation state, and generator-byte retention status;
6. `operational` is used only for the implemented Spectrum procedure layer;
7. no unbuilt serialization is presented as validated or operational;
8. the profile, machine schedule, both schemas, tests, introduction, standard
   pages, and crosswalk are present in the deterministic release manifest;
9. Stream is absent from the normative profile and is handled only as a later
   interoperability mapping.

## Canonical Museum evidence

- [Casey accession control](../casey-accession-control.md)
- [Accession certificate](../../records/accessions/6529NM.2026.001/accession-certificate.json)
- [Public technical and condition review](../../records/accessions/6529NM.2026.001/public/technical-and-condition-review.md)
- [Visual observation record](../../records/accessions/6529NM.2026.001/visual-observation-record.json)
- [Post-accession diligence](../../records/accessions/6529NM.2026.001/post-accession-diligence.json)
- [Evidence manifest](../../evidence/casey-reas/manifest.json)
- [Seven object records](../../records/accessions/6529NM.2026.001/objects/)
