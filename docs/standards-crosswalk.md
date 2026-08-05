# Museum accession and donation standards crosswalk

Status: documentation-only working crosswalk; not an adopted governance policy, governed schema, or current CI-validated record model. It describes the target application profile until matching schemas, cross-record invariants, state/publication gates, and constructor/reviewer commit/payload binding are merged.

Date of research baseline: 2026-08-01 UTC. External standards are cited for their published purpose and scope. The templates in [`../templates/`](../templates/) are a 6529 Network Museum application profile and must not be mistaken for a claim that any external standard is a complete collections-management system.

The controlling standards register is now [How the Museum knows and cares for
art](data-architecture.md) and its closed machine profile. This earlier
field-level crosswalk remains useful for template design. Where its provisional
language differs from the newer profile, the newer profile controls.

## Design objective

The Museum needs a durable packet for born-digital and tokenized art that can answer five different questions without collapsing them:

1. What object or objects are being considered or accessioned?
2. What authority and evidence support the acquisition and the legal title transfer?
3. What is the artwork's native technical constitution and current condition?
4. What may the Museum preserve, display, publish, reproduce, migrate, or make available?
5. Can another person reconstruct the record, verify its fixity, understand its limitations, and distinguish public facts from restricted registrar material?

The packet therefore uses an accession lot for the institutional act and an individual object record for every artwork/object. It adds a state-gate worksheet, object-level technical/condition and provenance schedules, a rights/donor-transfer record, a preservation dossier, a public inventory, a restricted-annex pointer, and constructor/reviewer attestations. Instantiated governed JSON uses the exact [`templates/record-control.md`](../templates/record-control.md) contract: the reviewer payload hash is computed over the top-level record after removing `record_control`.

## Source register

| Source | Published scope used here | Operational consequence |
|---|---|---|
| [Spectrum 5.1, Collections Trust](https://collectionstrust.org.uk/spectrum/) and [Acquisition and accessioning](https://collectionstrust.org.uk/resource/acquisition-and-accessioning-the-spectrum-standard/) | Museum collections-management procedures, including object entry, acquisition/accessioning, inventory, cataloguing, technical/condition assessment, rights, preservation-related care, and audit | The packet must document policy fit, authority, title evidence, donor terms, unique numbering, provenance, rights, costs/obligations, and accountability across intake-to-accession. |
| [Object ID, ICOM](https://www.obs-traffic.museum/object-id) and [Object ID reference, Getty](https://www.getty.edu/publications/resources/virtuallibrary/0892365722.pdf) | Minimum documentation needed to identify cultural objects and support recovery/description | The object record begins with stable number, title/type, creator or maker, date, materials/technique, dimensions, distinguishing description, and identifying media/source references; token identity is an additional field, not a replacement. |
| [CIDOC CRM 7.1.3](https://cidoc-crm.org/get-last-official-release) | Formal ontology for integrating and mediating heterogeneous cultural-heritage documentation | Model acquisition, title/custody events, actors, times, rights, condition, creation, and information objects as linked events/entities rather than a flat ownership string. |
| [LIDO 1.1](https://lido-schema.org/schema/latest/lido.html) | XML delivery/exchange schema for describing cultural objects and works, including identification, events, rights, and resources | Keep human-readable display values and machine identifiers in the object record so a later LIDO export can carry title, object ID, creator, event, rights, resource, and credit information. LIDO is an interchange layer, not the Museum's acquisition ledger. |
| [PREMIS 3.0, Library of Congress](https://www.loc.gov/standards/premis/v3/index.html) | Preservation metadata model with Objects, Events, Rights, and Agents | Every preservation package records bit-level objects, environments, events/outcomes, agents, and rights; the preservation dossier must not be only a list of URLs. |
| [PROV-O, W3C Recommendation](https://www.w3.org/TR/prov-o/) | General ontology for provenance relations among Entities, Activities, and Agents | Give every material Museum assertion a traceable source and producing activity; use qualified relations for roles and times; assess trust separately from graph validity. |
| [Getty AAT and ULAN](https://www.getty.edu/research/tools/vocabularies/) | Continuously maintained controlled vocabularies for art, architecture, artists, and cultural actors | Retain stable concept/subject identifiers, preferred and historical labels, source edition or retrieval date, and Museum extension terms where no reviewed Getty match exists. |
| [IIIF Presentation API 3.0](https://iiif.io/api/presentation/3.0/) | Linked description of collections/compound objects and views/resources for rich online presentation | Public inventory may expose a durable manifest with canvases/resources, attribution, rights, hashes, and accessible derivatives; a still or video remains a declared manifestation/documentation surrogate unless authorized otherwise. |
| [C2PA Technical Specification 2.4](https://spec.c2pa.org/specifications/specifications/2.4/specs/C2PA_Specification.html) | Technical provenance and authenticity assertions for media | C2PA 2.4 references are optional, content-addressed, and reported with `specVersion`, manifest/claim identifiers, and validation status. C2PA does not by itself prove legal title, copyright, accession, or native token identity. |
| [BagIt, RFC 8493](https://datatracker.ietf.org/doc/html/rfc8493) | File layout conventions for reliable storage and transfer with payload/tag manifests | A valid bag requires `bagit.txt`, a `data/` directory, and at least one payload manifest. `bag-info.txt` and tag manifests are optional; package completeness/fixity is tested separately from semantic validation. |
| [OCFL 1.1](https://ocfl.io/) | Application-independent, transparent, predictable, versioned digital-object storage | Store dossiers as versioned objects with parseable inventories, fixity, rebuildability, and superseding versions; do not overwrite a historical package in place. |
| [CAIP-19](https://standards.chainagnostic.org/CAIPs/caip-19) | Chain-agnostic asset-type and asset-ID syntax, currently in Review | Use the Museum's pinned lowercase-contract and canonical-decimal ERC-721 profile; keep block hash, observation time, custody, title, and accession state outside the asset identifier. |
| [Smithsonian Institution Archives digital curation](https://siarchives.si.edu/what-we-do/digital-curation) and [born-digital preservation strategies](https://siarchives.si.edu/what-we-do/digital-curation/preservation-strategies-born-digital-materials) | Publicly described institutional practice for inventory, baseline risk assessment, fixity, backup, metadata, migration/emulation, lifecycle stewardship, and AIP/DIP access separation | Start preservation at accession/intake, document who did what and when, retain originals, produce access derivatives separately, and record format/environment risk and recovery plans. |
| [6529Stream interoperability profile](stream-interoperability.md) | Downstream record envelope, hash references, subject derivation, and contract compatibility | Use the exact `HashRef`/`CollectionRecord` envelope when exporting to Stream-compatible infrastructure. Museum semantics and implementation states come from the Museum data architecture; a later bilateral mapping records adapters and divergences. |

The Spectrum web edition is licensed; this crosswalk paraphrases its requirements and links to the source rather than reproducing the procedure text.

## Field and workflow crosswalk

| Museum operating concern | Template anchor | Spectrum / Object ID | CIDOC CRM / LIDO | PREMIS / IIIF / C2PA 2.4 / BagIt / OCFL | 6529Stream and Museum rule |
|---|---|---|---|---|---|
| Intake and offer | [`accession-state-gates.md`](../templates/accession-state-gates.md) | Spectrum Object entry; acquisition proposal and due diligence | Event/actor/time modelling; not a public LIDO accession claim | Intake package may be a BagIt submission; no preservation completion claim yet | An offer or unsolicited transfer is not an accession. Record the offer and disposition separately. |
| Acceptance, acquisition, title, custody, and accession events | `accession-lot.md`, `accession-state-gates.md`, `rights-donor-transfer.md` | Spectrum acquisition/accessioning policy questions and written acceptance/title evidence | Distinct actors, events, and time-spans; acceptance is not acquisition, title passage, custody, or accession | PREMIS Agents/Events/Rights can carry preservation-side references but do not replace the institutional decision or legal instrument | Record offer/receipt, acceptance status/date/authority/evidence, acquisition date, title-passage date, custody-receipt date, and formal accession date separately. |
| Authority, policy fit, and authorization | `accession-lot.md`, state gates | Spectrum acquisition/accessioning policy questions: mission, law, authority, provenance, rights, cost/obligation | Actors, types, times, decision event | PREMIS Agent references may identify the reviewing role | Governance/program evidence authorizes a pathway; it does not prove that a specific work was acquired or accessioned. |
| Accession lot and object numbering | `accession-lot.md`, `object-record.md` | Spectrum unique accession/object number and accession register | Linked group/object descriptions; an acquisition event can cover multiple objects | OCFL object/version IDs must remain distinct from Museum accession numbers | Museum identifiers are stable and do not encode artist, chain, wallet, or collection. One lot may contain many individually evidenced objects. |
| Minimum object identification | `object-record.md`, `public-inventory.md` | Object ID minimum identification record | LIDO `objectID`, title, object/work type, actor/event, measurements, subject, rights | IIIF descriptive metadata can expose the public view; hashes identify bytes, not the work alone | The token, contract, hash/seed, work, and documentation surrogates are related typed facts. |
| Artwork and token identity | `object-record.md` | Object ID's object description extended for digital media | CIDOC CRM information-object/event profile; LIDO object identifiers and events | C2PA 2.4/IIIF/BagIt references identify media or packages | Use CAIP-19-shaped citations for native assets. Never invent a token ID for an unminted selection. |
| Acquisition, title, and transfer | `rights-donor-transfer.md`, `provenance-chain-history.md` | Spectrum written title transfer, donor terms, and provenance checks | Museum digital-title and digital-custody activities align to E8/E10 while using extension properties: CRM's P24 and P30 ranges are E18 Physical Thing and cannot be applied directly to a token | PREMIS Rights/Agents can point to preservation permissions, not replace a title instrument | `TITLE_BINDING` links one legal instrument to one specific transfer. Custody, title, token ownership, and accession remain separate. |
| Non-token and hybrid event path | `provenance-chain-history.md`, `rights-donor-transfer.md` | Off-chain instrument, object receipt, title, and custody documentation | Distinct off-chain events/actors/time-spans; do not fabricate chain identity | PREMIS/OCFL/IIIF/C2PA 2.4 references may document the object or package, not a nonexistent token event | Require the separate instrument/receipt/title/custody path for non-token and hybrid objects; `not_applicable` must be justified. |
| Chain history and custody | `provenance-chain-history.md` | Spectrum provenance/inventory accountability | Acquisition/custody events and actors with times; protocol events are not automatically legal events | Fixity and retrieval events are preservation evidence, not chain custody | Record native chain events, legal-title events, Museum custody, and historical provenance in four lanes. |
| Technical constitution | `object-record.md`, `technical-condition-report.md` | Spectrum cataloguing and technical assessment | Digital information object, creation/event, environment/actor relationships | PREMIS environment and events; BagIt payload; OCFL version; C2PA 2.4/IIIF references when present | Capture script, dependency, runtime, mutability, parameters, randomness, network, sound, timing, and artist intent. |
| Condition and rendering | `technical-condition-report.md` | Spectrum condition checking and technical assessment | Museum digital-condition activity aligned to E14/E3; CRM P34 concerns E18 Physical Thing, so the digital subject uses an explicit extension property | PREMIS render/validation events; IIIF/access capture; C2PA 2.4 validation status | Separate byte integrity, retrieval, rendering, behavior, and documentation. `green/amber/red/not_assessed` is the Museum vocabulary. |
| Rights and restrictions | `rights-donor-transfer.md`, `public-inventory.md` | Spectrum rights management and reproduction; donor terms | LIDO rights/credit and actor relationships; CRM rights/actors | PREMIS Rights entity; IIIF rights/attribution; C2PA 2.4 assertions may carry provenance, not legal permission | Record each use class as granted, not granted, conditional, unknown, or not applicable. CC0/default language never substitutes for verified scope. |
| Preservation package and structured exports | `preservation-dossier.md`, `object-record.md` | Spectrum collections care, documentation planning, audit | Objects, events, agents, rights and environment relationships | Record structured PREMIS Object/Event/Rights/Agent IDs; IIIF manifest/resource IDs; C2PA 2.4 manifest/claim IDs; OCFL object/version/inventory identifiers and exports. Mark each mapping `pending` until produced. | Preserve native metadata, code/media, dependencies, environment, captures, instructions, fixity, recovery lineage, and access derivatives. |
| Public access and checklist | `public-inventory.md` | Spectrum cataloguing, use of collections, rights/reproduction | LIDO delivery record and resource/rights fields | IIIF Presentation manifest; C2PA 2.4/BagIt/OCFL references where safe | The public record is a projection after rights/privacy/technical review. It never exposes restricted donor, appraisal, security, or private storage data. |
| Restricted registrar annex | `restricted-annex-reference.md` | Spectrum documentation planning and access controls; public museum practice supports restriction for legal, privacy, IP, and preservation reasons | Actor identities and sensitive events remain access-controlled in the application layer | Package/hash reference only; no private payload | Publish a non-sensitive custodian and hash, not the private annex. |
| Constructor and reviewer accountability | `attestations.md`, `record-control.md` | Spectrum audit/accountability | PREMIS Agents and Events; CRM actors/times | The target `record_control` requires constructor/reviewer roles, distinct actor IDs, immutable reviewed commit, approved outcome, and payload SHA-256; current CI validates existing governed JSON, not these blank forms | A second person reviews the record. `payload_sha256` hashes the entire top-level JSON payload after removing `record_control`; prose attestations do not replace this binding. |
| Corrections and versions | All templates | Spectrum audit/documentation continuity | New event/record linked to prior state | PREMIS event; OCFL superseding version; BagIt new package; Stream append-only record/supersession | Corrections append `supersedes`, preserve prior hashes, and never silently rewrite a historical assertion. |

## CIDOC CRM and LIDO profile notes

CIDOC CRM is a conceptual ontology, not a form-filling schema. The following is a proposed Museum mapping to test in a future export profile:

| Museum concept | Candidate CRM pattern | LIDO delivery shape | Constraint |
|---|---|---|---|
| Artwork/work identity | E73 Information Object or the applicable digital-art profile; local type identifies tokenized/born-digital work | `objectID`, title, object/work type, materials/technique, measurements, description | Do not represent the token as the entire artwork without an artist/project or curatorial basis. |
| Creation/minting | Creation or production event with creator/issuer and time | `event` with event type, actor, date, and related object/resource | Native mint event and artwork creation are distinct dates/events. |
| Donation/acquisition | Museum digital-title activity aligned to E8, with actors, time, object, method/type; no direct P24 use for a token | Acceptance and acquisition events with related actor/date/rights fields | Legal title and Museum acceptance must be object-specific even in a shared lot; acceptance and acquisition remain separate events. |
| Custody receipt | Museum digital-custody activity aligned to E10, with actors and time; no direct P30 use for a token | Event/resource reference where useful | Custody receipt is not title and not accession. |
| Condition assessment | Museum digital-condition activity aligned to E14/E3; no direct P34 use for a digital subject | Profile-declared descriptive note, event, or relation because LIDO 1.1 has no generic named condition element | Preserve protocol, environment, result, and limitations in the technical report; do not flatten into a single condition word. |
| Rights/credit | E30 Right with actor/holder and time/scope | Rights type, rights holder, credit line, resource rights | Each use class needs its own status/basis. |
| Provenance narrative | Attributed events, actors, times, and sources | Repeated events with display and indexing values | Historical and marketplace claims remain attributed evidence, not chain state. |

LIDO's purpose is to deliver and connect object descriptions for online services. It is therefore a downstream exchange view of the Museum object record, not a replacement for the lot, donor instrument, title-binding register, state-gate worksheet, or restricted annex.

## Digital-preservation interpretation

The standards have complementary boundaries:

- PREMIS supplies the preservation semantics: what object was acted on, what event occurred, which agent performed it, what environment/outcome applied, and what rights govern preservation.
- BagIt supplies a transport/storage layout and manifests. A valid bag requires `bagit.txt`, `data/`, and at least one payload manifest; `bag-info.txt` and tag manifests are optional. A valid bag does not prove that the content is authentic, the artwork is complete, or the runtime reproduces behavior.
- OCFL supplies a transparent/versioned storage layout. It does not decide which significant properties, rights, dependencies, or access derivatives the Museum must preserve.
- IIIF supplies a presentation description and linked resources. It is not a token registry, rights clearance, or conservation report.
- C2PA 2.4 supplies signed/hash-linked provenance assertions for supported media. It is optional and its `specVersion`, manifest/claim identifiers, and validation result must be reported; it is not a title instrument or accession authority.

The Museum's dossier therefore records the source/native capture, preservation masters, metadata, code/dependencies, execution environment, significant properties, reference manifestations, artist intent, fixity, events, rights, package/storage version, access derivatives, and recovery tests. It explicitly labels a retained copy or render as a surrogate unless the governing source authorizes another interpretation.

## State and scenario profile

Use the independent state sequence:

`offered` → `authorized` → `acquired` → `received_onchain` → `accessioned` → `catalogued` → `technically_verified` → `preservation_complete` → `display_ready`

For the completed Casey REAS donation, the packet is lot-first and object-specific. The canonical lot and all seven objects are `accessioned`: the full gift, exact identities and custody, title bindings, rights determination, curatorial decision, condition review, and accession certificate are complete. Each object retains its own stable number, native identity, title binding, technical/condition evidence, rights, preservation status, public release, and review. The separate `technically_verified`, `preservation_complete`, and `display_ready` states remain unclaimed because their stricter evidence gates have not been met; active software-preservation work does not reopen the accession decision.

For Keys and Gates while selections remain unminted, the program outcome is recorded as `selected_unminted`. A Wave selection can support a program authorization/evidence field, but it is never object authorization and cannot populate native chain identity, mint/acquisition transaction, title binding, custody receipt, accession, or preservation completion. Invariant `KNG-PROGRAM-OBJECT-BOUNDARY-01`: program authorization and selection never authorize a specific object's acquisition, mint, custody, title passage, or accession. A later amendment or object record may be created only after the specific asset and required evidence are verified.

## 6529Stream convergence and deliberate divergence

The Museum first defines its own meanings through
`6529NM_DATA_ARCHITECTURE_V1`. Stream's exact `HashRef` and
`CollectionRecord` envelope remains the downstream contract boundary where
Stream-compatible infrastructure is used. Before deployment, the convergence
gate in [`stream-interoperability.md`](stream-interoperability.md) must pin both
profiles, compare fields and document hashes, round-trip exports, record every
adapter or divergence, and reject semantic drift.

The following are Museum-layer additions, not silent changes to Stream semantics:

- accession lots containing multiple subordinate object records;
- separate workflow states for authorization, acquisition, receipt, accession, cataloguing, technical verification, preservation, and display readiness;
- claim-level A–E evidence classes and observation times;
- donation diligence, donor terms, curatorial independence, and tax/valuation boundaries;
- public/restricted record separation and non-sensitive annex references;
- constructor, registrar, technical, curatorial, and independent-review attestations;
- an explicit pre-mint program-selection state for Keys and Gates.

## Implementation boundary

This crosswalk and the linked Markdown forms are documentation-only/non-governed target artifacts. PR #7's executable control plane currently validates the existing governed JSON records and their record-control blocks; it does not validate these blank forms, cross-record invariants, state/publication gates, or their future schema/export mappings. Do not describe a field as enforced until the matching schema, invariant, gate, and commit/payload binding is merged and exercised by CI.

## Completion gate

An object may be reported as accessioned only when the designated custody/control condition, object-specific title evidence and `TITLE_BINDING`, independent chain/identity verification, viewing/condition check, applicable technical and mutability assessment, explicit rights, preservation/display records, completed object and curatorial records, and second-person review are present. The public inventory may still be held or restricted after accession if rights, privacy, security, or preservation constraints require it.
