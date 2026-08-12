# WP-1 schema and vocabulary dependencies

This WP-4 corpus is isolated content plus one narrowly scoped program-media control correction. It does not redefine WP-1 schemas, controlled vocabularies, record envelopes, or shared ontology files.

## Required integration dependencies

The content layer expects downstream integration to use the existing WP-1-owned definitions for:

- stable identifiers `6529NM-AP-01` and `6529NM-AP-01-OUT-###`;
- lifecycle state `selected_unminted` and the program status `selection_complete_acquisition_and_accession_unverified`;
- `ACCESSION_PROGRAM`, `PROGRAM_OUTCOME_INDEX`, and `PROGRAM_OUTCOME` schemas;
- the distinction among a Work, a documentation/presentation surrogate, a chain asset, a manifestation, an event/activity, an agent, a right/permission, evidence, a record, and a package;
- evidence grades, source-status semantics, observation times, fixity, and negative evidence;
- append-only corrections with `supersedes` rather than silent historical rewrites;
- Stream-compatible record envelopes, subject derivation, schema identifiers, hash algorithms, and CAIP-19-shaped on-chain citations;
- rights vocabulary and object-specific rights-effective status;
- program media-manifest joins and the source/presentation-surrogate/preservation-object boundary;
- the existing `schemas/program-media-manifest.schema.json` control, whose accessibility status vocabulary records the independently reviewed state `constructed_visual_description_reviewed`; and
- public/restricted record separation and public-safety scanning.

## Suggested future content relations

When WP-1 integrates the corpus, the projection can be related as:

```text
Curated Acquisition 6529NM-CA-2026-002
  produced by / governed through -> Acquisition Program 6529NM-AP-01
  has selected outcome -> 6529NM-AP-01-OUT-001 ... OUT-016
  has public scholarship -> this Markdown corpus
  has technical presentation -> existing PROGRAM_MEDIA_MANIFEST
```

The relation is descriptive only. It must not be serialized as an accession, Collection membership, custody event, title binding, mint, purchase, or rights grant until the relevant control-plane evidence exists.

## Deliberate non-changes

WP-4 does not:

- create a new schema profile or controlled term for “Curated Acquisition”;
- change the canonical selected-work title, status, source hash, or evidence files;
- normalize legal names from unverified public leads into authoritative identity records;
- convert the presentation derivatives into preservation masters or tokenized works;
- assert that the planned custody reference `networkmuseum.6529.eth` has received any asset;
- decide the future mint topology between a dedicated 6529Stream instance and a main-Stream subcollection.

The program-media status correction is not a WP-1 ontology change. It is an implementation dependency for the typed media manifest, accessibility JSON, generator, and tests; WP-1 integration should preserve the derived amendment and its one-to-one media joins.
