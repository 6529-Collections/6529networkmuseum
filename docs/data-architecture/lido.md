# LIDO: a public catalogue record that can travel

Status: working Museum application profile; the cited standard remains authoritative

## The question

**How can another catalogue receive a coherent public record of the work?**

A visitor should be able to find an artwork by its artist, title, project,
date, type, technique, subject, collection, or accession number. A partner
archive should be able to receive the same description without scraping a web
page or reverse-engineering the Museum's internal database.

LIDO is a shared format for sending a museum's public object record to another
catalogue, portal, or archive. Its full name is Lightweight Information
Describing Objects. In its current form, it is an XML schema for cultural-object
metadata and online exchange.

## In the Casey Reas accession

A LIDO record for *Phototaxis #308* could carry:

- the Museum object and accession identifiers;
- the preferred title and Casey Reas as creator, with an authority URI;
- generative software as the work type and controlled terms for medium and
  technique;
- the project date, mint event, acquisition and accession events;
- the 6529 Network Museum as repository;
- the gift credit line and public rights statements;
- links to the chain asset, object page, live work, approved stills, and
  technical documentation;
- the source and version of the LIDO record itself.

The exchange record brings those facts together for discovery. The underlying
evidence, donor instrument, restricted registrar material, and preservation
package remain in their appropriate systems.

## What LIDO contributes

LIDO 1.1 separates descriptive metadata from administrative metadata. It groups
a public record into several areas:

- what the object is, including its classification and work type;
- titles, inscriptions, repository, measurements, materials, techniques,
  states, editions, and description;
- events with their actors, dates, places, methods, materials, and cultural
  context;
- subjects, related works, record identifiers, sources, rights, and record
  metadata; and
- images, audio, video, and other resources, with their own type, rights, and
  links.

The schema supports multilingual display text alongside identifiers and
controlled concepts. That distinction lets a catalogue remain readable while
also joining records across institutions.

## Museum application profile

### One public object per record

Each Museum LIDO record describes one accessioned object or a clearly declared
collection-level object. The `lidoRecID`, Museum object ID, chain asset ID, work
or project ID, and public page URI remain separate identifiers with explicit
types and sources.

### Event-centred description

Creation, mint, acquisition, title passage, custody receipt, accession,
exhibition, and modification are separate event sets. Each event states its
type, actors and roles, date or time-span, place or chain context, method, and
source to the extent available. For people, display text can summarize an
event; for catalogues and machines, the record preserves identifiers and event
structures.

### Work, token, and resource distinctions

The described object is never inferred from a thumbnail. The chain asset is an
identifier or related object. A still image, video, or live generator is a
resource representation with its own type, rights, credit, link, and format.
The record says whether that resource is an authorized manifestation,
documentation surrogate, access derivative, or upstream live service.

### Rights layers

LIDO provides separate rights structures for the object or work, the metadata
record, and each `resourceSet`. A `resourceSet` may carry `rightsResource`;
`resourceRepresentation` carries rendition links and measurements and has no
native rights child. The Museum uses separate resource sets when rendition-
specific rights must be expressed. A CC licence observed in token metadata
cannot silently license Museum-authored
catalogue text, and a Museum CC0 publication policy cannot license an artwork.

### Public projection

The LIDO export is produced only from reviewed public fields. Private donor
contacts, non-public legal instruments, security architecture, appraisal
material, and restricted storage locations never enter the public record.

## What this standard leaves to the Museum

LIDO delivers catalogue metadata. It is not the accession register, legal title
instrument, complete provenance graph, preservation event store, or exhibition
viewer. It can link to those records and carry selected public facts from them.

LIDO 1.1 does not define a generic, named condition element for every kind of
condition statement. The Museum will not invent one and call it standard LIDO.
A public digital-condition summary may be carried in a typed event, relation,
or note selected by the Museum profile, with the complete condition record
linked as a separate resource. The profile and its Schematron rules will make
that local choice explicit.

## For machines and implementers

### Authority and version

- Publisher: ICOM-CIDOC LIDO Working Group.
- Current version: **LIDO 1.1**, published 20 December 2021.
- Canonical schema documentation: [LIDO 1.1](https://lido-schema.org/schema/latest/lido.html).
- XSD: linked from the canonical schema documentation.
- Licence: CC BY 4.0.

### Required Museum record spine

The Museum profile will require at minimum:

```text
lidoRecID
category
objectWorkTypeWrap/objectWorkType
titleWrap/titleSet/appellationValue
repositoryWrap/repositorySet/workID
eventWrap/eventSet[creation or production]
recordWrap/recordID
recordWrap/recordSource
recordWrap/recordType
recordWrap/recordInfoSet/recordInfoLink
recordWrap/recordRights
rightsWorkWrap
resourceWrap/resourceSet (when a public resource is supplied)
```

Museum constraints add stable identifier types, language tags, controlled-term
URIs, explicit public-source provenance, chain-asset links, resource roles, and
the exact canonical Museum release used to generate the record.

### Serialization and validation

The normative exchange is XML validated against the pinned LIDO 1.1 XSD and
Museum Schematron rules. A JSON or JSON-LD convenience view may be published,
but its conformance claim names the Museum projection rather than calling it
LIDO XML.

Validation must cover:

- XSD validity;
- Museum-required cardinalities and identifier types;
- controlled vocabulary URI reachability at the pinned observation;
- public/restricted field exclusion;
- rights separation among work, record, and resource;
- preservation of repeated events and multilingual values;
- source commit, generation version, and deterministic output digest;
- round-trip recovery of the Museum object ID, title, creator, event types,
  repository, rights, credit line, and resource roles.

## The Casey Reas accession

Museum state: `source_fields_present`. The seven object records and public dossier contain
most of the facts needed for useful LIDO records. Creator authority URIs and
controlled AAT terms still require reconciliation, and no LIDO 1.1 XML or
Schematron validation report has been published.

## Official sources

- ICOM-CIDOC LIDO Working Group, [LIDO 1.1 schema documentation](https://lido-schema.org/schema/latest/lido.html).
- ICOM-CIDOC LIDO Working Group, [LIDO Primer](https://lido-schema.org/documents/primer/latest/lido-primer.html).
- ICOM-CIDOC LIDO Working Group, [LIDO Terminology](https://lido-schema.org/terminology/).
