# The Museum of Modern Art

- **Series:** A field of practice
- **Status:** public scholarship
- **Institutional author:** 6529 Network Museum
- **Version:** 1.0.0
- **Publication date:** 2026-08-04
- **Research cutoff:** 2026-08-04
- **Research apparatus:** [primary-source register](../source-register.md)

MoMA's public collection work makes the condition of a record visible. The
Museum states that its evolving collection contains almost 200,000 works and
that the website presents more than 83,000 artworks by more than 26,000 artists.
The same collection page calls the website a work in progress, identifies
incomplete records that have not necessarily received curatorial approval, and
provides a correction route. ([About the Collection](https://www.moma.org/collection/about/))

That combination is useful for a chain-native museum because identity,
availability, approval, and completeness remain separate properties. MoMA's
collection spans objects, events, installations, film, media, and performance;
its public records therefore have to connect artwork identity with duration,
display, technical process, and exhibition history. ([Media and Performance](https://www.moma.org/about/curatorial-departments/media-performance))

## A work record with technical identity

The collection record for Refik Anadol's *Unsupervised — Machine Hallucinations
— MoMA* identifies the work as 2021–2023, gives the medium as custom hardware
and software with color, sound, and a generative algorithm using artificial
intelligence, records variable dimensions, credit, object number 757.2022, and
places it in Media and Performance. It links the record to interpretive
articles and videos, states that the record is a work in progress, and provides
a feedback route. ([Refik Anadol, *Unsupervised — Machine Hallucinations — MoMA*](https://www.moma.org/collection/works/442077))

The page shows how a work record can state technical constitution before a
longer interpretation begins. For a live or generative work, the record should
also identify which captures are documentation and which are manifestations.
The 6529 Network Museum should preserve that distinction for token, project,
runtime, display, and conservation states.

## Exhibition history with published gaps

MoMA reports more than 3,500 exhibitions since 1929. Its exhibition-history
pages can include participating artists, installation views, annotated
checklists, press releases, catalogues, subsites, videos, and essays. The
Museum also says that the materials vary by page, that the archive is a living
resource, and that important film, performance, and MoMA PS1 histories remain
in future phases or outside the current online coverage. The underlying
1929–1989 exhibition data is available for research. ([About our exhibition history](https://www.moma.org/calendar/about/exhibition-history))

The operational lesson is to model exhibition history as a set of dated
relations, each with its own evidence and completeness state. An exhibition
record should link exact object identifiers, participating artists, documents,
installation views, and catalogue resources. A missing checklist should remain
missing; it should not be inferred from the exhibition title.

## Public data and its boundaries

MoMA publishes collection and artist metadata through its official GitHub
repository. The repository documents CC0 data, citation and attribution
expectations, incomplete records, rules for identifying modified derivative
datasets, and a correction route through the collection team. It also explains
that the data is generated from an internal database and is not maintained
through public pull requests. ([MoMA collection data](https://github.com/MuseumofModernArt/collection))

MoMA's API page describes a REST service for art, exhibition, artist, and image
data, but says that external access is currently limited to MoMA staff and
partners. The public open-data repository is therefore a different publication
layer, with metadata available for reuse and image rights handled separately.
([MoMA API](https://api.moma.org/))

The 6529 Network Museum should publish stable identifiers, authority and
approval states, completeness notes, correction routes, citation instructions,
and derivative-data disclosures. It should also state whether an API is public,
restricted, or versioned for partners. A public export should not imply that
every field is final or that every associated media file is reusable.

## Media conservation as shared practice

MoMA's Media and Performance department states that it collects, exhibits, and
preserves time-based art. Its remit includes securing equipment, updating
exhibition technology, and recreating presentations whose meaning depends on
duration. ([Media and Performance](https://www.moma.org/about/curatorial-departments/media-performance))

Through *Matters in Media Art*, MoMA, SFMOMA, Tate, and the New Art Trust
published guidance for acquiring, lending, installing, and caring for video,
film, audio, and computer-based installations. The project treats care as a
shared practice among artists, lenders, registrars, technicians, conservators,
and exhibition sites. ([Matters in Media Art](https://www.moma.org/research/conservation/matters-in-media-art))

MoMA's public conservation writing describes two complementary records. The
media-conservator account emphasizes artist consultation, equipment, duration,
installation guidance, and documentation. Its technical-history case records
the device model and serial number, settings, and migration sequence used to
create later copies, with structured process-history data intended to remain
searchable. ([What Does a Media Conservator Do?](https://www.moma.org/explore/inside_out/2015/03/24/what-does-a-media-conservator-do/); [Preserving the Technical History of Media Works](https://www.moma.org/explore/inside_out/2015/05/20/preserving-the-technical-history-of-media-works/))

For a chain-native work, the corresponding record should capture contract and
token identity, source and metadata versions, dependencies, runtime, browser or
renderer behavior, display conditions, artist-approved changes, migration
authority, and the evidence for each preserved state. Token ownership fixes one
provenance layer. Technical history belongs in the linked record set.

## Public scholarship and writing method

The sampled MoMA pages use distinct publication layers. The Anadol page is a
compact object record with a controlled technical description, credit, object
number, department, related interpretation, work-in-progress notice, and
feedback route. The conservation essays then explain a technical problem in
plain language, name the people and systems involved, and describe the
consequences for future display. This division lets the object page remain
readable while giving researchers a route into process history.

## What the Museum should adopt

The 6529 Network Museum should use the same separation:

- a concise object record for identity, status, credit, and rights;
- a curatorial entry for close looking and historical argument;
- a technical record for runtime, dependencies, captures, and interventions;
- provenance, condition, preservation, and correction records with their own
  sources and revision histories.

## Where the analogy ends

MoMA's collection scale, archives, departments, and conservation resources
exceed the Museum's present scale. Its open data is metadata, not a
complete public image repository; its API is not currently an open public
service; and its historical conservation essays describe particular workflows,
not a guarantee that every media work has the same documentation depth.

The 6529 Network Museum should adopt the record states, process-history model,
and correction discipline. It should not infer preservation completeness from a
public catalogue entry or treat a reusable dataset as proof of rights to every
associated image or software dependency.

## Sources

1. Museum of Modern Art, [“About the Collection”](https://www.moma.org/collection/about/).
2. Museum of Modern Art, [“Refik Anadol. *Unsupervised — Machine Hallucinations — MoMA*. 2021–2023”](https://www.moma.org/collection/works/442077).
3. Museum of Modern Art, [“About our exhibition history”](https://www.moma.org/calendar/about/exhibition-history).
4. Museum of Modern Art, [“Museum of Modern Art (MoMA) collection data”](https://github.com/MuseumofModernArt/collection).
5. Museum of Modern Art, [“MoMA API”](https://api.moma.org/).
6. Museum of Modern Art, [“Media and Performance”](https://www.moma.org/about/curatorial-departments/media-performance).
7. Museum of Modern Art, [“Matters in Media Art”](https://www.moma.org/research/conservation/matters-in-media-art).
8. Museum of Modern Art, [“What Does a Media Conservator Do?”](https://www.moma.org/explore/inside_out/2015/03/24/what-does-a-media-conservator-do/), 24 March 2015.
9. Museum of Modern Art, [“Preserving the Technical History of Media Works”](https://www.moma.org/explore/inside_out/2015/05/20/preserving-the-technical-history-of-media-works/), 20 May 2015.
10. Museum of Modern Art, [“MoMA.org Turns 20: Archiving Two Decades of Exhibition Sites”](https://www.moma.org/explore/inside_out/2015/05/25/moma-org-turns-20-archiving-two-decades-of-exhibition-sites/), 25 May 2015.

## Revision history

- `1.0.0` — 2026-08-04: revised after factual and editorial audit; added direct work, data, API, exhibition-history, and conservation sources.
