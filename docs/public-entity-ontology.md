# Public entity and relation ontology

Status: working Museum source standard for the public entity publication layer. This document defines a reviewed, Stream-shaped projection contract; it does not itself adopt governance, acquire an artwork, mint a token, establish custody, grant rights, or create an exhibition.

## Boundary and identity

`PUBLIC_ENTITY` and `PUBLIC_RELATION` use the existing `{envelope,payload}` CollectionRecord topology. Their Museum-native schema commitments are `keccak256("PUBLIC_ENTITY_V1")` and `keccak256("PUBLIC_RELATION_V1")`. A record's `record_id` is its stable Museum identifier; the envelope subject remains the domain-separated hash of the record type and identifier. Names, artists, collections, chains, and wallets never enter stable identifiers.

The public layer is a typed projection over authoritative source records. It does not replace accession, title, custody, rights, condition, preservation, governance, program, or Wave records. A relation can explain a connection; it cannot manufacture the event or status that the source record does not establish.

Reserved Curated Acquisition identifiers are:

| ID | Label | Source boundary |
|---|---|---|
| `6529NM-CA-2026-001` | The System in Seven States | Casey seven-work accession and publication records; separate from accession `6529NM.2026.001` |
| `6529NM-CA-2026-002` | Keys and Gates | Acquisition Program `6529NM-AP-ENT-0002` (source alias `6529NM-AP-01`); selected, unminted, and not accessioned |
| `6529NM-CA-2026-003` | Conflict at Its Edges | Proposed gift `6529NM-PG-2026-001` with append-only signed-Wave `WINNER` observation; selected by Museum Wave for acquisition review, with no Collection effect |

The same Curated Acquisition identity advances by append-only correction. Rejection closes it as `closed_without_selection`; it is not deleted or silently rewritten.

## Closed entity profiles

Every `PUBLIC_ENTITY` has one `entity_type` and one closed `profile`. The required profile fields are deliberately substantive:

| Entity type | Required source-contract facts |
|---|---|
| `INSTITUTION` | mission, public authority, collection relation, name evidence |
| `COLLECTION` | owning institution, accession-only membership rule, admitted works |
| `AGENT` | closed `agent_kind`, authority status, name variants with source evidence, role contexts |
| `ARTIST` | authority status, practice summary, name variants with source evidence |
| `ORGANIZATION` | history, roles, authority status, name variants with source evidence |
| `WORK` | creator entity set, title, creation date (including explicit not-established state), medium, lifecycle status, current Museum relation, collection membership, component/manifestation references |
| `PROJECT_OR_SERIES` | scope, agent set, work set, ownership boundary, source records |
| `CURATED_ACQUISITION` | thesis, method, lifecycle, program relation, work set or source work set, collection effect, independent acquisition facts |
| `ACQUISITION_PROGRAM` | authority records, rules, program status, selected outcome records, produced acquisitions |
| `ACCESSION` | accession number, accession status, admitted works, source accession record |
| `RESEARCH_PUBLICATION` | publication type/date/version, authors, subjects, document URI |
| `MEDIA_REFERENCE` | closed media role, locator, MIME/type, dimensions where visual, subject, credit, rights state, source observation, fixity state, and UI affordance policy |
| `EXHIBITION` | reserved vocabulary only; no instance is published by this work |

`AGENT` is not an untyped catch-all. It is allowed only with a closed subtype such as `PERSON`, `COLLECTIVE`, or `PUBLISHER`; `ARTIST` and `ORGANIZATION` remain explicit profiles when those roles are asserted. A name variant is an object with value, role, source kind, and evidence references, never an unqualified string list.

## Curated Acquisition lifecycle

The public lifecycle is intentionally independent from transaction and stewardship facts:

1. `proposed_in_museum_wave`
2. `selected_by_museum_wave_acquisition_review_in_progress`
3. `selected_through_acquisition_program_acquisition_pending`
4. `acquisition_complete_accession_review_in_progress`
5. `accessioned_into_permanent_collection`
6. `closed_without_selection`
7. `withdrawn`

The layer records mint, payment, title, custody, rights, technical, preservation, and display as typed independent facts with their own evidence and observation times. None is inferred from a lifecycle label, wallet custody, a transfer, a `WINNER` label, or a selected outcome. The Keys and Gates projection therefore retains `selected_through_acquisition_program_acquisition_pending`, selected outcome references, and null/unverified downstream facts. The Magnum projection retains the earlier `PARTICIPATORY` proposal observation and appends the authenticated `WINNER` observation as `selected_by_museum_wave_acquisition_review_in_progress`; all five Works remain outside Collection. The Casey projection records the completed accession boundary without claiming that software preservation is complete.

## Relations and direction

Relations are closed, directed assertions. The validator checks endpoint existence and type, allowed cardinality, required/allowed qualifiers, duplicate active assertions, self-links, and lifecycle-sensitive restrictions.

The initial relation vocabulary includes:

`INSTITUTION_HOLDS_COLLECTION`, `ARTIST_CREATES_WORK`, `AGENT_PLAYS_ROLE`, `PROJECT_CONTEXTUALIZES_WORK`, `ORGANIZATION_ORIGINATES_PROJECT`, `ACQUISITION_PROGRAM_PRODUCES_ACQUISITION`, `CURATED_ACQUISITION_BRINGS_TOGETHER_WORK`, `PROGRAM_SELECTS_WORK`, `ACCESSION_ADMITS_WORK`, `COLLECTION_CONTAINS_WORK`, `WORK_CONSTITUTED_BY_COMPONENT`, `WORK_HAS_MANIFESTATION`, `PUBLICATION_INTERPRETS_ENTITY`, `INSTITUTION_PUBLISHES_PUBLICATION`, and `ENTITY_HAS_MEDIA`.

The reserved `EXHIBITION_PRESENTS_WORK` relation is not instantiated. It may validate only when an actual reviewed Exhibition entity exists. A rights-use class, display-ready state, image manifest, or prose mention is not an exhibition.

Relation qualifiers are closed per relation profile. Examples include ordered acquisition membership, selection status, role, accession object ID, collection membership status, and media context. A broad `qualifier` object may not introduce arbitrary graph predicates.

## Component, manifestation, and media boundaries

Work identity, component, manifestation, token-linked source media, documentation, and preservation objects remain distinct. A `component_references` or `manifestation_references` field points to an existing authoritative record or a typed public media/reference entity; it does not turn a screenshot, derivative, or metadata response into the artwork or a token.

Media is never represented by a generic `image_url`. Each `MEDIA_REFERENCE` target of an `ENTITY_HAS_MEDIA` assertion carries:

- one role: `museum_retained_preservation_object`, `museum_generated_public_derivative`, `token_linked_source_media`, or `signed_wave_proposal_presentation`;
- a source URI and/or repository path, MIME type, and visual dimensions when applicable;
- the Work or other public entity subject and a credit line;
- a rights statement/status independent of title and custody;
- source observation/status and evidence references;
- a fixity object only when the bytes were actually retrieved and hashed, otherwise an explicit closed `unverified_not_retrieved` status;
- an allow-list of UI affordances. Unknown/restricted media cannot gain download, zoom, or fullscreen through a default.

Mutable external media is represented with `source_status: mutable_external`, an observed-at timestamp, and no fabricated permanence. Signed-Wave proposal media retains its Wave/drop/publication evidence, `publication_boundary: signed_wave_proposal_only`, and only the closed presentation affordances including the non-licensing `open_signed_wave_source` locator. It cannot imply selection or acquisition and cannot gain download, zoom, fullscreen, token-source, or repository-source access. Accessibility metadata can require `non_identifying_child_subject`; that policy is executable and forbids identifying language in the alt text. Museum-generated derivatives retain their transform/source relationship and are not preservation masters. A retained preservation object is not the tokenized work.

## Interoperability

The public records map to Stream's `CollectionRecord` envelope without claiming that the Museum-native payload is already an admitted Stream on-chain schema. `ARTIST_CREATES_WORK` maps to LIDO creation actor semantics; `INSTITUTION_HOLDS_COLLECTION`, acquisition/accession relations, and `ENTITY_HAS_MEDIA` map through the Museum's LIDO view. Media fixity, derivation, source, and preservation roles map to PREMIS Object/Event/Rights semantics. The source records remain authoritative for event detail, and any adapter must preserve bilateral identity, evidence, rights, and custody boundaries.
