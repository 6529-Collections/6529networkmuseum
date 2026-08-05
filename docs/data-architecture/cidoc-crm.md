# CIDOC CRM: a history made of events

Status: working Museum application profile; the cited standard remains authoritative

## The question

**What happened, to what, when, where, and through whose action?**

A conventional object record can make history look like a row of labels:
artist, owner, date, museum. Cultural objects are formed by relationships and
events. A work is created. A token is minted. A collector acquires it. A donor
makes a gift. Title passes. Custody moves. A museum accessions an object. A
conservator observes a dependency failure. A new record corrects an older one.

CIDOC CRM gives museums a shared way to describe histories as events and
relationships. It is the formal cultural-heritage model standardized as ISO
21127 and maintained by the CIDOC CRM Special Interest Group.

## In the Casey Reas accession

The Casey Reas gift contains at least three histories that a visitor might
mistake for one:

1. the artistic history of Reas's work and each project;
2. the protocol history of each ERC-721 token;
3. the Museum history of offer, receipt, gift acceptance, title passage,
   accession, cataloguing, observation, and preservation.

An event-based record can join these histories while preserving their
differences. The Ethereum transfer can be represented as an event with sender,
recipient, token, transaction, block, and time. The legal title declaration is
a different information object and a different institutional act. The Museum's
accession is another event. All three may refer to the same object schedule and
support one public chronology.

## What CIDOC CRM contributes

CIDOC CRM names the kinds of things a cultural-heritage record may need—objects,
events, people and organizations, places, periods, documents, rights,
conditions, and assessments—and defines the relationships among them.

Its event-centred design is especially useful when:

- the same object participates in several events;
- an event has multiple actors with different roles;
- dates are uncertain or bounded;
- custody and ownership change independently;
- a source supports one statement but not an entire narrative;
- a correction changes the Museum's knowledge without changing the past event.

## Museum application profile

The table below is the Museum's intended mapping. Before an RDF release, every
class, property direction, and cardinality will be checked against the pinned
official model.

| Museum concept | CIDOC CRM pattern |
|---|---|
| Accessioned digital artwork | A Museum extension aligned to `E28 Conceptual Object`, `E73 Information Object`, and, where warranted, `E90 Symbolic Object`; the profile must identify the work, token, files, and institutional collection object separately |
| Artistic work or conceptual content | `E28 Conceptual Object` / `E89 Propositional Object` pattern, qualified for software and generative systems |
| Museum record, metadata response, script, rights instrument | `E73 Information Object` with identifiers and carriers or digital representations distinguished as needed |
| Artist, donor, Museum, registrar | `E39 Actor`, normally `E21 Person` or `E74 Group`, with role expressed through the event or typed relation |
| Software program or runtime | `E73 Information Object`, `E29 Design or Procedure`, `E90 Symbolic Object`, or a documented Museum extension as applicable; software is never asserted as `E39 Actor` |
| Creation or authored production | `E65 Creation` and applicable production patterns |
| Token mint or protocol state transition | typed `E5 Event` / `E7 Activity` in the Museum extension, linked to chain evidence; never silently equated with creation of the artwork |
| Legal acquisition | A Museum digital-title activity aligned to `E8 Acquisition` without reusing `P24 transferred title of` outside its `E18 Physical Thing` range |
| Custody movement | A Museum digital-custody activity aligned to `E10 Transfer of Custody` without reusing `P30 transferred custody of` outside its `E18 Physical Thing` range |
| Title, licence, or other right | `E30 Right` linked to the applicable legal object, actors, and evidence |
| Condition observation | `E14 Condition Assessment`; `P35 has identified` links the assessment to `E3 Condition State`. `P34 concerned` is used only for an `E18 Physical Thing`; digital works use a Museum extension for the assessed entity |
| Time | `E52 Time-Span`, including bounded or uncertain dates |
| Place or chain context | `E53 Place` for applicable places; chain/network identity remains a Museum/CAIP extension rather than pretending a blockchain is a geographic place |
| Identifier assignment | `E15 Identifier Assignment` where the assignment event matters |
| Museum statement or attribution | `E13 Attribute Assignment`, with source and responsible actor |

### Museum extensions

The base CRM does not supply native classes for a blockchain network, smart
contract, token ID, transaction log, deterministic seed, browser environment,
or wallet account. The Museum profile will introduce these as narrowly scoped
classes or typed information objects and events, aligned with CRMsci or other
compatible extensions where that improves the model. Every extension term will
have a stable URI, definition, domain, range, examples, and mapping back to the
base CRM.

### The digital legal-and-custody boundary

CIDOC CRM 7.1.3 places several familiar museum properties on physical things.
`P24 transferred title of`, `P30 transferred custody of`, `P34 concerned`,
`P50 has current keeper`, and `P52 has current owner` have `E18 Physical Thing`
as their applicable domain or range. An ERC-721 token, a software artwork, and a
Museum's institutional collection object are not made physical by assertion.

The Museum will therefore publish its digital-title, wallet-custody, and
digital-condition terms in a versioned extension namespace. Each term will
state its CRM alignment and the point at which it departs from the base
property's physical scope. A physical carrier may use the base properties when
the carrier itself is the subject. A token or digital work may not.

## What this standard leaves to the Museum

CIDOC CRM organizes meaning. It does not prescribe an acquisition procedure,
prove that an event occurred, replace a legal instrument, or determine which
facts may be public. RDF data is only as reliable as its sources and modelling.
The authoritative specification text, rather than a convenience RDF or OWL
encoding, controls interpretation.

## For machines and implementers

### Authority and release pin

- Authority: CIDOC CRM Special Interest Group under ICOM CIDOC.
- Official release pinned by this profile: **7.1.3**, February 2024, marked
  “Official (ISO Correspondence).”
- ISO correspondence: ISO 21127:2023.
- Release register: [Versions of the CIDOC CRM](https://cidoc-crm.org/versions-of-the-cidoc-crm).
- Namespace: `http://www.cidoc-crm.org/cidoc-crm/`.

Version 7.3.2, published in March 2026, is marked Draft in the official release
register and is not the production pin for this profile.

### Serialization

The Museum target graph is RDF 1.1 with stable HTTPS Museum identifiers and the
official 7.1.3 class/property semantics. Its canonical serialization is RDF
1.1 TriG. JSON-LD may provide an additional JSON-based serialization; it
remains a serialization of the graph rather than a new ontology. Each export
must include:

```text
profile identifier and version
CIDOC CRM release
Museum extension namespace and version
source Museum release commit and manifest commitment
generation software version
generation time
graph digest
validation report
```

### Validation

A production export must pass RDF syntax parsing, closed Museum-profile shape
validation, stable-URI checks, controlled-class/property checks, required source
and event identifiers, and golden round-trip tests. The round trip must recover
the Museum object, event type, actors and roles, time, evidence, and status
without converting custody into title or mint into creation.

### Minimal event shape

```turtle
<museum-event> a crm:E7_Activity ;
  crm:P14_carried_out_by <agent> ;
  crm:P4_has_time-span <time-span> ;
  crm:P2_has_type <museum-event-type> .

<source-record> a crm:E31_Document ;
  crm:P70_documents <museum-event> .
```

This fragment is illustrative. Production predicates for affected objects,
documents, rights, and custody must follow the reviewed profile and official
property directions.

## The Casey Reas accession

Museum state: `source_fields_present`. The canonical records contain identified objects,
actors, events, dates, rights, sources, condition assessments, and corrections
sufficient for a substantial graph. The Museum has not published or validated a
CIDOC CRM 7.1.3 RDF/JSON-LD export. No website or repository statement should
describe the current JSON records as CRM-conformant.

## Official sources

- CIDOC CRM SIG, [versions and official status](https://cidoc-crm.org/versions-of-the-cidoc-crm).
- CIDOC CRM SIG, [use and implementation guidance](https://cidoc-crm.org/use-learn).
- CIDOC CRM SIG, [scope](https://cidoc-crm.org/scope).
- International Organization for Standardization, [ISO 21127:2023](https://www.iso.org/standard/85100.html).
