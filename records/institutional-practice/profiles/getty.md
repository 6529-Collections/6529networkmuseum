# Getty

- **Series:** A field of practice
- **Status:** public scholarship
- **Institutional author:** 6529 Network Museum
- **Version:** 1.0.0
- **Publication date:** 2026-08-04
- **Research cutoff:** 2026-08-04
- **Research apparatus:** [primary-source register](../source-register.md)

Getty’s public documentation is useful as a model of connected collection and
research infrastructure. The Museum Collection API describes more than
250,000 object records, including deaccessioned objects, and exposes objects,
people, groups, places, exhibitions, documents, images, and activities through
Linked Art JSON-LD, IIIF, REST, ActivityStreams, and SPARQL. The same
documentation warns that the data can be incomplete or contain errors, is
still being updated, and does not carry a guarantee of curatorial approval.
[Getty Museum Collection API Documentation](https://data.getty.edu/museum/collection/docs/)

That qualification is part of the institutional profile. Getty’s systems make
semantics, relations, identifiers, and change visible, while their own
documentation tells users where the data remains provisional. The [Getty
Vocabularies](https://www.getty.edu/research/tools/vocabularies/index.html)
extend this approach beyond object records: they describe structured resources
with sources, contributors, historical information, variant names, complex
relationships, multilingual terms, and disputed or ambiguous art-historical
information.

## Demonstrated practices

### 1. Provenance has explicit notation

Getty’s [Research on Museum Collection
Provenance](https://www.getty.edu/museum/provenance/) page explains how its
public provenance format handles date ranges, “by” dates, open-ended
intervals, unknown owners, private collections, dealers, transactions, sales,
locations, and source notes. It gives distinct meanings to forms such as
`1955–1970`, `1955–`, `–1955`, and `by 1955–`; it also explains that a private
collection may identify an anonymous owner or withhold a known identity.

The lesson for a chain-native Museum is exact semantic typing. “Unknown,”
“private,” “disputed,” and “not yet researched” should not share one empty
field. A provenance interval, owner identity, transaction, and source note
should be separate assertions with their own uncertainty and revision status.

### 2. An object record joins history, scholarship, and identifiers

The Getty page for Vittore Carpaccio’s *Hunting on the Lagoon* (recto) and
*Letter Rack* (verso) provides Provenance, Bibliography, and Exhibitions as
distinct research paths. Its provenance sequence names owners and date ranges,
retains source notes, and records uncertainty such as “possibly.” The page
also exposes an API URL, TMS and DOR identifiers, a SPARQL route, a permalink,
and a “Last updated: June 2, 2026” notice for the primary JSON-LD document.
[Hunting on the Lagoon (recto); Letter Rack
(verso)](https://www.getty.edu/art/collection/object/103REK)

The record therefore documents two histories: the artwork’s reported passage
through owners and the catalogue’s own addressability and update state. For
the 6529 Network Museum, a token transfer should remain one event in a larger
provenance graph. It cannot, by itself, prove legal title, donor authority,
artist attribution, consent, or the condition of the work.

### 3. APIs expose a graph and a change vocabulary

The Museum Collection API documentation lists entity types for objects, places,
documents, groups, people, exhibitions, and activities. It describes Linked
Art JSON-LD and RDF graph queries through SPARQL, IIIF image and presentation
services, and ActivityStreams for tracking record changes. These choices make
relations and updates queryable alongside page prose.
[Getty Museum Collection API Documentation](https://data.getty.edu/museum/collection/docs/)

The 6529 Network Museum can apply this at a smaller scale by publishing typed
relations among works, wallets, artists, contracts, transactions, exhibitions,
documents, images, and conservation events. The on-chain layer should hold
authorized assertions and durable lineage; public exports should expose the
larger research graph without pretending that every assertion has the same
status.

### 4. Vocabularies carry provenance and disagreement

The Getty Vocabularies page describes its resources as more than lists of
preferred labels. Entries can connect to published sources and contributors,
other resources, historical and current information, variant names,
multilingual terms, and debated or ambiguous art-historical information. The
vocabularies are published as Linked Open Data and are intended for cataloguers,
researchers, and data providers. [Getty
Vocabularies](https://www.getty.edu/research/tools/vocabularies/index.html)

For the Museum, a term such as “interactive,” “generative,” or “software-based”
should have an identifier, definition, source, contributor, revision history,
and alternatives where relevant. A vocabulary is an evidentiary layer, not a
permanent tag embedded without explanation in an accession record.

### 5. Digital catalogues are planned as publications

The Getty Foundation’s 2017 [*Museum Catalogues in the Digital
Age*](https://www.getty.edu/publications/osci-report/) is the final report of
the Online Scholarly Catalogue Initiative. It treats the online catalogue as a
web publication with notes, media, rights, citations, multiple reading paths,
and revision. Its structure includes projects at a glance, lessons learned,
approaches, costs, remaining challenges, evaluation, functional requirements,
rights documentation, a user study, and a glossary.

The report’s public-writing value lies in its operational detail. It makes
catalogue design answerable to audiences, existing systems, rights, labour,
maintenance, and preservation. A Museum publication from GitHub or
content-addressed records should therefore have a citable edition, accessible
web reading, open formats where rights permit, stable links, and an explicit
plan for revisions and preservation.

## Close reading of public scholarship

The Carpaccio object page uses a restrained, notation-led voice. “Provenance,”
“Bibliography,” and “Exhibitions” are separate invitations to research rather
than headings inside one undifferentiated narrative. The provenance sequence
uses dates, owners, source notes, and qualified language; identifiers and an
update date tell the reader how to address the record itself. The editorial
style teaches the reader how to read the evidence by making its units visible.
[Hunting on the Lagoon (recto); Letter Rack
(verso)](https://www.getty.edu/art/collection/object/103REK)

The OSCI report uses a different but complementary voice. It is a long-form
institutional research document organized around implementation questions:
what participating institutions built, what systems and rights they needed,
how users read the results, what the work cost, and what remains difficult.
Its headings, downloadable requirements, rights form, user study, and glossary
make the report usable as a design record with testable requirements.
The page’s preservation discussion is especially relevant: a stable PDF does
not preserve interactive audio or video, and a changing online catalogue needs
planned capture and continuing maintenance. [*Museum Catalogues in the Digital
Age*](https://www.getty.edu/publications/osci-report/)

## What the Museum should adopt

- Give provenance dates, owner identities, transactions, source notes, and
  uncertainty different fields and identifiers.
- Publish an object graph with typed relations and stable cross-system IDs;
  include a machine-readable change record and a human-readable update notice.
- Treat wallet custody, token transfer, legal title, donor authority, artist
  attribution, consent, and condition as separate claims with separate
  evidence.
- Build small, versioned vocabularies whose definitions, sources, contributors,
  alternatives, and revisions are public.
- Design essays and catalogues as maintainable publications: specify citation,
  rights, accessibility, export, versioning, and preservation before release.

## Where the analogy ends

The Getty API documentation identifies the data as work in progress and warns
of incompleteness, errors, and ongoing change. The Museum should snapshot and
identify any external Getty-derived data it uses; an API response is not a
substitute for checking the underlying record or preserving the retrieval
state. Getty’s vocabulary and publication systems also reflect long-running
institutional labour. A small Museum should adopt the semantics it can govern,
not copy the full graph or vocabulary surface.

The OSCI report also sets a boundary around digital publication. A web page can
remain available while its interactive media, dependencies, or previous
versions become inaccessible. The Museum needs explicit capture, media
preservation, rights, and migration procedures. Getty’s open-data terms do not
automatically determine the rights in an artwork, an artist’s software, a
third-party text, or a hosted image.

## Sources

1. Getty, [“Getty API Documentation”](https://data.getty.edu/). Publication date: not shown. Accessed: 2026-08-04. Supports: the API entry point and the institution’s linked-data documentation.
2. Getty, [“Getty Museum Collection API Documentation”](https://data.getty.edu/museum/collection/docs/). Publication date: not shown; page states last updated 21 March 2022. Accessed: 2026-08-04. Supports: the reported record scale; entity types; Linked Art JSON-LD, IIIF, REST, ActivityStreams, and SPARQL; and the incompleteness and work-in-progress cautions.
3. Getty, [“Getty Provenance Index API Documentation”](https://data.getty.edu/provenance/docs/). Publication date: not shown. Accessed: 2026-08-04. Retained source for the Provenance Index API documentation and provenance-data research path.
4. Getty Museum, [“Research on Museum Collection Provenance”](https://www.getty.edu/museum/provenance/). Publication date: not shown. Accessed: 2026-08-04. Supports: provenance notation, date semantics, ownership and transaction language, source notes, and the reasons gaps remain.
5. Getty Museum, [“Hunting on the Lagoon (recto); Letter Rack (verso)”](https://www.getty.edu/art/collection/object/103REK). Publication date: not shown; page states last updated June 2, 2026. Accessed: 2026-08-04. Supports: the object’s provenance, bibliography and exhibition paths; qualified ownership history; identifiers; API and SPARQL links; and update notice.
6. Getty Research Institute, [“Getty Vocabularies”](https://www.getty.edu/research/tools/vocabularies/index.html). Publication date: not shown. Accessed: 2026-08-04. Supports: vocabulary structure, sources, contributors, relationships, variants, multilingual terms, historical information, disputed terminology, and Linked Open Data.
7. Getty Foundation, [“Museum Catalogues in the Digital Age”](https://www.getty.edu/publications/osci-report/), 2017. Accessed: 2026-08-04. Supports: the OSCI catalogue model, implementation apparatus, publication requirements, and preservation and maintenance cautions.
8. Getty Publications, [“Getty Research Journal”](https://www.getty.edu/publications/getty-research-journal/). Publication date: not shown. Accessed: 2026-08-04. Retained source for Getty’s research-publication context.

## Revision history

- `1.0.0` — 2026-08-04: initial profile.
