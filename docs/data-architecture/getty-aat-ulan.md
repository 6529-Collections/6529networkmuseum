# Getty AAT and ULAN: shared names for art and artists

Status: working Museum application profile; the cited standard remains authoritative

## The question

**When two records use different words or names, do they mean the same thing?**

An artist may publish under several forms of a name. A material can have a
specialist term, a common term, historical terms, and translations. “Generative
art,” “software,” “computer programs,” and “algorithmic art” overlap without
being interchangeable. Search and scholarship suffer when every record invents
its own vocabulary.

The Getty Vocabularies give museums shared identifiers, terms, relationships,
sources, and scope notes. The Art & Architecture Thesaurus (AAT) covers concepts
such as work types, materials, techniques, styles, roles, and activities. The
Union List of Artist Names (ULAN) covers artists and other corporate bodies
connected with art.

## In the Casey Reas accession

The public label should read “Casey Reas” in the form appropriate to the artist
and publication. A machine record can also retain a reviewed ULAN URI if the
Museum confirms a unique match. AAT URIs can support stable indexing of work
types and techniques while the label continues to use natural language.

The URI is the durable reference. The displayed label records what the Museum
said at a particular time. If Getty later changes a preferred term or merges an
authority record, the Museum retains its earlier assertion and records the
mapping rather than silently rewriting history.

## What the Getty Vocabularies contribute

AAT concept records can include preferred and alternate terms, languages, scope
notes, broader and narrower concepts, associative relations, sources,
contributors, and revision history. Its polyhierarchy allows one concept to
appear under more than one broader context.

ULAN records can include preferred and variant names, pseudonyms, language,
person or corporate-body type, biography, nationality, roles, life dates,
relationships, sources, contributors, and revision history. One authority
record can therefore connect several name forms without treating them as
different people.

## Museum application profile

### Display and index values

Every controlled field keeps both:

```text
display value used by the Museum
authority URI
authority label observed at cataloguing
authority source and retrieval date
match status and evidence
```

The display value remains curatorial language. The authority value supports
search, exchange, and linked data.

### Authority matching

An exact name string is insufficient for a match. The cataloguer compares life
dates, roles, places, collaborators, biographies, published sources, and the
context of the work. Match status is one of `exact`, `probable`, `ambiguous`, or
`unmatched`. Only `exact` enters a production exchange record as an unqualified
identity link. Probable and ambiguous candidates remain attributed research.

### Attribution remains in the object record

ULAN can identify a person or group. It does not decide that the person made a
particular work. Qualifiers such as “attributed to,” “studio of,” “workshop of,”
or “formerly attributed to” belong to the Museum's work attribution and its
evidence.

### Digital-art terminology

Where AAT lacks the precision required for software, protocol, generative, or
networked art, the Museum records the nearest valid AAT concepts and maintains
a versioned Museum extension term. The local term has a definition, broader
concept, sources, and proposed Getty mapping. It is never presented as a Getty
term until Getty publishes it.

## What this standard leaves to the Museum

The Getty Vocabularies support naming and discovery. They do not authenticate a
work, establish authorship, grant rights, prove wallet identity, record an
accession, or replace evidence. Their ODC-By licence applies to the Getty data,
not to the artworks described with it.

## For machines and implementers

### Authority, release model, and licence

- Authority: Getty Vocabulary Program, Getty Research Institute.
- Release model: continuously maintained; online records are refreshed monthly.
- Data access: individual RDF/JSON/Turtle/N-Triples records, SPARQL,
  OpenRefine reconciliation, and periodic full Linked Open Data releases.
- Legacy XML and relational releases were archived after the 30 January 2026
  dataset; they are no longer the current delivery path.
- Licence: Open Data Commons Attribution 1.0 (ODC-By).

Official access and attribution instructions are in [Obtain the Getty
Vocabularies](https://www.getty.edu/research/tools/vocabularies/obtain/).

### Identifier forms

```text
AAT concept: http://vocab.getty.edu/aat/{subject_ID}
ULAN concept: http://vocab.getty.edu/ulan/{subject_ID}
ULAN agent:   http://vocab.getty.edu/ulan/{subject_ID}-agent
```

The Museum stores the URI, numeric subject ID, preferred label observed,
retrieval time, source release or response digest, match status, and match
evidence. Obsolete or merged IDs remain in correction lineage.

### Minimum authority assertion

```json
{
  "display_name": "Casey Reas",
  "authority": "ULAN",
  "uri": null,
  "match_status": "unmatched",
  "matched_at": null,
  "evidence_refs": []
}
```

`null` is preferable to a guessed URI. A later match appends a reviewed
authority assertion and supersedes the current view.

### Validation

Validation checks URI shape, authority type, match status, required evidence,
retrieval date, and retained label. Reconciliation output is a candidate list,
never an automatic exact match. Production builds use a pinned response or
dataset digest so a rolling service cannot change a historical release.

## The Casey Reas accession

Museum state: `conceptual_mapping`. The canonical object records contain the preferred artist
name and rich medium descriptions, but they do not yet carry a reviewed ULAN
identifier or AAT concept URIs. Authority reconciliation and controlled-term
selection remain publication work.

## Official sources

- Getty Research Institute, [Getty Vocabularies](https://www.getty.edu/research/tools/vocabularies/).
- Getty Research Institute, [AAT](https://www.getty.edu/research/tools/vocabularies/aat/).
- Getty Research Institute, [ULAN](https://www.getty.edu/research/tools/vocabularies/ulan/).
- Getty Research Institute, [editorial guidelines](https://www.getty.edu/research/tools/vocabularies/guidelines/).
- Getty Research Institute, [data access and licensing](https://www.getty.edu/research/tools/vocabularies/obtain/).
