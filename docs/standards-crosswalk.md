# Museum accession and donation standards crosswalk

Status: working standard and implementation crosswalk; not an adopted governance policy.

Date of research baseline: 2026-08-01 UTC. External standards are cited for their published purpose and scope. The templates in [`../templates/`](../templates/) are a 6529 Network Museum application profile and must not be mistaken for a claim that any external standard is a complete collections-management system.

## Design objective

The Museum needs a durable packet for born-digital and tokenized art that can answer five different questions without collapsing them:

1. What object or objects are being considered or accessioned?
2. What authority and evidence support the acquisition and the legal title transfer?
3. What is the artwork's native technical constitution and current condition?
4. What may the Museum preserve, display, publish, reproduce, migrate, or make available?
5. Can another person reconstruct the record, verify its fixity, understand its limitations, and distinguish public facts from restricted registrar material?

The packet therefore uses an accession lot for the institutional act and an individual object record for every artwork/object. It adds a state-gate worksheet, object-level technical/condition and provenance schedules, a rights/donor-transfer record, a preservation dossier, a public inventory, a restricted-annex pointer, and constructor/reviewer attestations.

## Source register

| Source | Published scope used here | Operational consequence |
|---|---|---|
| [Spectrum 5.1, Collections Trust](https://collectionstrust.org.uk/spectrum/) and [Acquisition and accessioning](https://collectionstrust.org.uk/resource/acquisition-and-accessioning-the-spectrum-standard/) | Museum collections-management procedures, including object entry, acquisition/accessioning, inventory, cataloguing, technical/condition assessment, rights, preservation-related care, and audit | The packet must document policy fit, authority, title evidence, donor terms, unique numbering, provenance, rights, costs/obligations, and accountability across intake-to-accession. |
| [Object ID, ICOM](https://www.obs-traffic.museum/object-id) and [Object ID reference, Getty](https://www.getty.edu/publications/resources/virtuallibrary/0892365722.pdf) | Minimum documentation needed to identify cultural objects and support recovery/description | The object record begins with stable number, title/type, creator or maker, date, materials/technique, dimensions, distinguishing description, and identifying media/source references; token identity is an additional field, not a replacement. |
| [CIDOC CRM 7.1.3](https://cidoc-crm.org/get-last-official-release) | Formal ontology for integrating and mediating heterogeneous cultural-heritage documentation | Model acquisition, title/custody events, actors, times, rights, condition, creation, and information objects as linked events/entities rather than a flat ownership string. |
| [LIDO 1.1](https://lido-schema.org/schema/latest/lido.html) | XML delivery/exchange schema for describing cultural objects and works, including identification, events, rights, and resources | Keep human-readable display values and machine identifiers in the object record so a later LIDO export can carry title, object ID, creator, event, rights, resource, and credit information. LIDO is an interchange layer, not the Museum's acquisition ledger. |
| [PREMIS 3.0, Library of Congress](https://www.loc.gov/standards/premis/v3/index.html) | Preservation metadata model with Objects, Events, Rights, and Agents | Every preservation package records bit-level objects, environments, events/outcomes, agents, and rights; the preservation dossier must not be only a list of URLs. |
| [IIIF Presentation API 3.0](https://iiif.io/api/presentation/3.0/) | Linked description of collections/compound objects and views/resources for rich online presentation | Public inventory may expose a durable manifest with canvases/resources, attribution, rights, hashes, and accessible derivatives; a still or video remains a declared manifestation/documentation surrogate unless authorized otherwise. |
| [C2PA Technical Specification](https://c2pa.org/specifications/specifications/1.0/specs/C2PA_Specification.html) | Technical provenance and authenticity assertions for media | C2PA references are optional, content-addressed, and reported with validation status. C2PA does not by itself prove legal title, copyright, accession, or native token identity. |
| [BagIt, RFC 8493](https://datatracker.ietf.org/doc/html/rfc8493) | File layout conventions for reliable storage and transfer with payload/tag manifests | Preservation packages use `bagit.txt`, `data/`, payload manifests, tag manifests, and bag metadata; package completeness/fixity is tested separately from semantic validation. |
| [OCFL 1.1](https://ocfl.io/) | Application-independent, transparent, predictable, versioned digital-object storage | Store dossiers as versioned objects with parseable inventories, fixity, rebuildability, and superseding versions; do not overwrite a historical package in place. |
| [Smithsonian Institution Archives digital curation](https://siarchives.si.edu/what-we-do/digital-curation) and [born-digital preservation strategies](https://siarchives.si.edu/what-we-do/digital-curation/preservation-strategies-born-digital-materials) | Publicly described institutional practice for inventory, baseline risk assessment, fixity, backup, metadata, migration/emulation, lifecycle stewardship, and AIP/DIP access separation | Start preservation at accession/intake, document who did what and when, retain originals, produce access derivatives separately, and record format/environment risk and recovery plans. |
| [6529Stream interoperability profile](stream-interoperability.md) | Museum/Stream shared record envelope, title binding, work description, rights, PREMIS/LIDO/IIIF/BagIt/OCFL/C2PA semantics | Reuse the pinned field semantics and exact `HashRef`/`CollectionRecord` envelope where the shared concept exists; keep Museum governance, lot structure, state gates, privacy, evidence classes, and attestations in the Museum layer. |

The Spectrum web edition is licensed; this crosswalk paraphrases its requirements and links to the source rather than reproducing the procedure text.

## Field and workflow crosswalk

| Museum operating concern | Template anchor | Spectrum / Object ID | CIDOC CRM / LIDO | PREMIS / IIIF / C2PA / BagIt / OCFL | 6529Stream and Museum rule |
|---|---|---|---|---|---|
| Intake and offer | [`accession-state-gates.md`](../templates/accession-state-gates.md) | Spectrum Object entry; acquisition proposal and due diligence | Event/actor/time modelling; not a public LIDO accession claim | Intake package may be a BagIt submission; no preservation completion claim yet | An offer or unsolicited transfer is not an accession. Record the offer and disposition separately. |
| Authority, policy fit, and authorization | `accession-lot.md`, state gates | Spectrum acquisition/accessioning policy questions: mission, law, authority, provenance, rights, cost/obligation | Actors, types, times, decision event | PREMIS Agent references may identify the reviewing role | Governance/program evidence authorizes a pathway; it does not prove that a specific work was acquired or accessioned. |
| Accession lot and object numbering | `accession-lot.md`, `object-record.md` | Spectrum unique accession/object number and accession register | Linked group/object descriptions; an acquisition event can cover multiple objects | OCFL object/version IDs must remain distinct from Museum accession numbers | Museum identifiers are stable and do not encode artist, chain, wallet, or collection. One lot may contain many individually evidenced objects. |
| Minimum object identification | `object-record.md`, `public-inventory.md` | Object ID minimum identification record | LIDO `objectID`, title, object/work type, actor/event, measurements, subject, rights | IIIF descriptive metadata can expose the public view; hashes identify bytes, not the work alone | The token, contract, hash/seed, work, and documentation surrogates are related typed facts. |
| Artwork and token identity | `object-record.md` | Object ID's object description extended for digital media | CIDOC CRM information-object/event profile; LIDO object identifiers and events | C2PA/IIIF/BagIt references identify media or packages | Use CAIP-19-shaped citations for native assets. Never invent a token ID for an unminted selection. |
| Acquisition, title, and transfer | `rights-donor-transfer.md`, `provenance-chain-history.md` | Spectrum written title transfer, donor terms, and provenance checks | Proposed mapping: E8 Acquisition, E10 Transfer of Custody, E39 Actor, E52 Time-Span, E73 Information Object; validate property direction in implementation | PREMIS Rights/Agents can point to preservation rights, not replace a title instrument | `TITLE_BINDING` links one legal instrument to one specific transfer. Custody, title, token ownership, and accession remain separate. |
| Chain history and custody | `provenance-chain-history.md` | Spectrum provenance/inventory accountability | Acquisition/custody events and actors with times; protocol events are not automatically legal events | Fixity and retrieval events are preservation evidence, not chain custody | Record native chain events, legal-title events, Museum custody, and historical provenance in four lanes. |
| Technical constitution | `object-record.md`, `technical-condition-report.md` | Spectrum cataloguing and technical assessment | Digital information object, creation/event, environment/actor relationships | PREMIS environment and events; BagIt payload; OCFL version; C2PA/IIIF references when present | Capture script, dependency, runtime, mutability, parameters, randomness, network, sound, timing, and artist intent. |
| Condition and rendering | `technical-condition-report.md` | Spectrum condition checking and technical assessment | Condition assessment/state profile (typically E14/E3 patterns) | PREMIS render/validation events; IIIF/access capture; C2PA validation status | Separate byte integrity, retrieval, rendering, behavior, and documentation. `green/amber/red/not_assessed` is the Museum vocabulary. |
| Rights and restrictions | `rights-donor-transfer.md`, `public-inventory.md` | Spectrum rights management and reproduction; donor terms | LIDO rights/credit and actor relationships; CRM rights/actors | PREMIS Rights entity; IIIF rights/attribution; C2PA assertions may carry provenance, not legal permission | Record each use class as granted, not granted, conditional, unknown, or not applicable. CC0/default language never substitutes for verified scope. |
| Preservation package | `preservation-dossier.md` | Spectrum collections care, documentation planning, audit | Objects, events, agents, rights and environment relationships | PREMIS is the semantic preservation model; BagIt is package layout; OCFL is versioned storage | Preserve native metadata, code/media, dependencies, environment, captures, instructions, fixity, recovery lineage, and access derivatives. |
| Public access and checklist | `public-inventory.md` | Spectrum cataloguing, use of collections, rights/reproduction | LIDO delivery record and resource/rights fields | IIIF Presentation manifest; C2PA/BagIt/OCFL references where safe | The public record is a projection after rights/privacy/technical review. It never exposes restricted donor, appraisal, security, or private storage data. |
| Restricted registrar annex | `restricted-annex-reference.md` | Spectrum documentation planning and access controls; public museum practice supports restriction for legal, privacy, IP, and preservation reasons | Actor identities and sensitive events remain access-controlled in the application layer | Package/hash reference only; no private payload | Publish a non-sensitive custodian and hash, not the private annex. |
| Constructor and reviewer accountability | `attestations.md` | Spectrum audit/accountability | PREMIS Agents and Events; CRM actors/times | Stream signature/hash references and effective times; OCFL preserves versions | A second person reviews the record. Attestations state scope and limitations; they do not turn an unverified claim into a fact. |
| Corrections and versions | All templates | Spectrum audit/documentation continuity | New event/record linked to prior state | PREMIS event; OCFL superseding version; BagIt new package; Stream append-only record/supersession | Corrections append `supersedes`, preserve prior hashes, and never silently rewrite a historical assertion. |

## CIDOC CRM and LIDO profile notes

CIDOC CRM is a conceptual ontology, not a form-filling schema. The following is a proposed Museum mapping to test in a future export profile:

| Museum concept | Candidate CRM pattern | LIDO delivery shape | Constraint |
|---|---|---|---|
| Artwork/work identity | E73 Information Object or the applicable digital-art profile; local type identifies tokenized/born-digital work | `objectID`, title, object/work type, materials/technique, measurements, description | Do not represent the token as the entire artwork without an artist/project or curatorial basis. |
| Creation/minting | Creation or production event with creator/issuer and time | `event` with event type, actor, date, and related object/resource | Native mint event and artwork creation are distinct dates/events. |
| Donation/acquisition | E8 Acquisition with actors, time, object, method/type | Acquisition event and related actor/date/rights fields | Legal title and Museum acceptance must be object-specific even in a shared lot. |
| Custody receipt | E10 Transfer of Custody with surrendering/receiving actors and time | Event/resource reference where useful | Custody receipt is not title and not accession. |
| Condition assessment | E14 Condition Assessment and associated condition state/type | Descriptive/administrative note or event extension | Preserve protocol, environment, result, and limitations in the technical report; do not flatten into a single condition word. |
| Rights/credit | E30 Right with actor/holder and time/scope | Rights type, rights holder, credit line, resource rights | Each use class needs its own status/basis. |
| Provenance narrative | Attributed events, actors, times, and sources | Repeated events with display and indexing values | Historical and marketplace claims remain attributed evidence, not chain state. |

LIDO's purpose is to deliver and connect object descriptions for online services. It is therefore a downstream exchange view of the Museum object record, not a replacement for the lot, donor instrument, title-binding register, state-gate worksheet, or restricted annex.

## Digital-preservation interpretation

The standards have complementary boundaries:

- PREMIS supplies the preservation semantics: what object was acted on, what event occurred, which agent performed it, what environment/outcome applied, and what rights govern preservation.
- BagIt supplies a transport/storage layout and manifests. A valid bag does not prove that the content is authentic, the artwork is complete, or the runtime reproduces behavior.
- OCFL supplies a transparent/versioned storage layout. It does not decide which significant properties, rights, dependencies, or access derivatives the Museum must preserve.
- IIIF supplies a presentation description and linked resources. It is not a token registry, rights clearance, or conservation report.
- C2PA supplies signed/hash-linked provenance assertions for supported media. It is optional and its validation result must be reported; it is not a title instrument or accession authority.

The Museum's dossier therefore records the source/native capture, preservation masters, metadata, code/dependencies, execution environment, significant properties, reference manifestations, artist intent, fixity, events, rights, package/storage version, access derivatives, and recovery tests. It explicitly labels a retained copy or render as a surrogate unless the governing source authorizes another interpretation.

## State and scenario profile

Use the independent state sequence:

`offered` → `authorized` → `acquired` → `received_onchain` → `accessioned` → `catalogued` → `technically_verified` → `preservation_complete` → `display_ready`

For the completed Casey Reas donation, the packet is lot-first and object-specific: one accession act can cover multiple donated works, but every object has its own stable number, native identity, title binding, technical/condition evidence, rights, preservation status, public release, and review. This crosswalk intentionally does not copy or alter any Casey record.

For Keys and Gates while selections remain unminted, the program outcome is recorded as `selected_pending_mint`. A Wave selection can support an authorization/program-evidence field, but it cannot populate native chain identity, mint/acquisition transaction, title binding, custody receipt, accession, or preservation completion. A later amendment or object record may be created only after the specific asset and required evidence are verified.

## 6529Stream convergence and deliberate divergence

The Museum should reuse Stream's exact `HashRef` and `CollectionRecord` envelope and the pinned semantics for `STREAM_ACCESSION_V1`, `STREAM_WORK_DESCRIPTION_V1`, `STREAM_RIGHTS_V1`, PREMIS, LIDO, IIIF, BagIt, OCFL, C2PA, condition, dossier, and acquisition-packet concepts where the same concept exists. Before deployment, follow the convergence gate in [`stream-interoperability.md`](stream-interoperability.md): pin canonical profiles, compare schema/document hashes, round-trip exports, and reject drift.

The following are Museum-layer additions, not silent changes to Stream semantics:

- accession lots containing multiple subordinate object records;
- separate workflow states for authorization, acquisition, receipt, accession, cataloguing, technical verification, preservation, and display readiness;
- claim-level A–E evidence classes and observation times;
- donation diligence, donor terms, curatorial independence, and tax/valuation boundaries;
- public/restricted record separation and non-sensitive annex references;
- constructor, registrar, technical, curatorial, and independent-review attestations;
- an explicit pre-mint program-selection state for Keys and Gates.

## Completion gate

An object may be reported as accessioned only when the designated custody/control condition, object-specific title evidence and `TITLE_BINDING`, independent chain/identity verification, viewing/condition check, applicable technical and mutability assessment, explicit rights, preservation/display records, completed object and curatorial records, and second-person review are present. The public inventory may still be held or restricted after accession if rights, privacy, security, or preservation constraints require it.
