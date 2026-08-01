# 6529 Network Museum museum-standards crosswalk

Status: constructor research note; working implementation guidance, not adopted Museum policy

Prepared: 2026-08-01 UTC
Research scope: accessioning, acquisition, object entry, cataloguing, provenance, rights, condition, preservation, public access, and maker–checker controls for born-digital and tokenized art.

## 1. Purpose and reading rule

This note translates authoritative museum, cultural-heritage, digital-preservation, and content-provenance standards into an implementation crosswalk for the 6529 Network Museum. It is intentionally a bridge document: no single cited standard describes a tokenized artwork held by a multisignature wallet, and none replaces the Museum’s adopted governance, donation, or custody decisions.

The following distinction is mandatory:

- **Source requirement** means what the cited standard or institution publicly says.
- **Museum working control** means a proposed implementation requirement derived from that source and adapted to tokenized art.
- **Adopted policy** means a governance status that must be established elsewhere in the Museum record. This note does not create adoption merely by being committed to GitHub.

The Museum’s existing record model, accession standard, and 6529Stream interoperability profile are the local implementation context. Where this note proposes a stronger or more specific field than an external standard requires, that is deliberate and is labelled as a Museum working control.

## 2. Executive findings

### 2.1 Use a layered standards stack

The Museum should use the standards for different jobs rather than force one schema to carry every fact:

| Layer | Primary authority | Museum use |
|---|---|---|
| Ethical and institutional | ICOM Code of Ethics; ICOM Standards on Accessioning | Mission fit, public trust, lawful title, provenance, permanence, resources, conflicts, accountability, responsible disposal. |
| Collections procedures | Spectrum 5.1 | Acquisition proposal, object entry, accessioning, inventory, cataloguing, rights, condition, audit, and deaccession workflow. |
| Object identification | ICOM Object ID | Minimum identifying description and secure documentation for recovery, loss, or dispute. |
| Cultural-heritage semantics | CIDOC CRM | Event-centred graph of creation, minting, transfer, title, custody, accession, preservation, exhibition, and correction. |
| Exchange metadata | LIDO 1.1 | Public/export record for discovery, multilingual description, linked authorities, events, rights, and representations. |
| Digital preservation | PREMIS 3.0 | Objects, events, agents, rights, environments, fixity, validation, migration, and preservation outcomes. |
| Presentation and access | IIIF Presentation 3.0; IIIF Image 3.0 where applicable | Stable, machine-readable presentation of images, video, audio, 3D, and documentation surrogates. |
| Media provenance | C2PA 2.4 | Optional signed provenance for Museum-created captures, derivatives, and preservation/rendering surrogates; never a substitute for chain or title evidence. |
| Transfer package | BagIt 1.0 / RFC 8493 | Portable ingest and release package with payload, tags, and cryptographic manifests. |
| Storage and versioning | OCFL 1.1 | Rebuildable, content-addressed, versioned digital object storage and fixity. |
| Chain record envelope | 6529Stream profile | Hash references, canonical JSON, typed record envelopes, title binding, rights, condition, PREMIS, LIDO, IIIF, BagIt, and acquisition-packet references. |

### 2.2 The accession is an evidence-backed act, not a wallet observation

The Museum should preserve separate records for:

1. **Offer/intake** — an object has been proposed or has arrived for review.
2. **Acquisition** — the Museum has obtained it by donation, purchase, program, exchange, bequest, or another authorized mechanism.
3. **Custody** — a specified wallet, contract, custodian, or storage system controls or holds a specified asset.
4. **Accession** — the Museum has formally accepted the identified object into the permanent collection.
5. **Cataloguing** — a public or internal descriptive record has been prepared.
6. **Technical verification** — the token, metadata, code, media, rendering, and dependencies have been checked to the applicable level.
7. **Preservation complete** — the preservation package, fixity, environment, and recovery path pass the relevant gate.

This is consistent with ICOM’s statement that accessioning is the formal process of accepting and recording an item in the permanent collection, and with Spectrum’s separation of acquisition, object entry, and cataloguing. A transfer to `networkmuseum.6529.eth`, an unsolicited airdrop, a program `WINNER` label, or a marketplace listing is evidence for an event or lead—not by itself evidence of accession.

### 2.3 The public record should be rich, but not indiscriminate

The Museum should publish enough information to make an object identifiable, interpretable, reproducible, and auditable while keeping private donor contacts, legal instruments, security details, and sensitive risk material restricted. A public record can identify a restricted document by stable reference and content hash without disclosing its contents.

### 2.4 Maker–checker review is part of the record

Every accession package needs an identifiable constructor and an independent checker. The reviewer must see the source evidence, the proposed state transition, the rendered work or technical surrogate, and the exact payload or manifest being approved. A second person’s approval should be recorded as a signed or hash-linked review event, not merely implied by a GitHub merge.

## 3. Authority and version register

All web sources below were retrieved on 2026-08-01 UTC. Version status is recorded because several standards are living publications. At implementation time, the Museum should pin the exact document or schema hash used by CI and record any later repinning as an append-only standards amendment.

| ID | Authority and version/status | What it contributes | Direct source |
|---|---|---|---|
| S1 | Collections Trust, Spectrum 5.1 | UK collections-management standard; 21 procedures, including object entry, acquisition/accessioning, inventory, cataloguing, condition, rights, deaccessioning, and audit. | [Spectrum 5.1](https://collectionstrust.org.uk/spectrum/) and [all procedures](https://collectionstrust.org.uk/spectrum/procedures/) |
| S2 | Collections Trust, acquisition and accessioning procedure | Written acquisition case, due diligence, title, object identification, source, date, conditions, credit line, restrictions, and retained evidence. | [Acquisition and accessioning—suggested procedure](https://collectionstrust.org.uk/resource/acquisition-and-accessioning-suggested-procedure/) |
| S3 | Collections Trust, rights management | Record rights, permissions, licences, rightsholders, due diligence, expiry, and catalogue references. | [Rights management—the Spectrum standard](https://collectionstrust.org.uk/resource/rights-management-the-spectrum-standard/) |
| S4 | Collections Trust, condition and technical assessment | Document make-up and condition, assessment method/date/checker, recommendations, and change audit trail. | [Condition checking and technical assessment](https://collectionstrust.org.uk/spectrum/procedures/condition-checking-spectrum-5-0/) and [suggested procedure](https://collectionstrust.org.uk/resource/condition-checking-and-technical-assessment-suggested-procedure/) |
| S5 | Collections Trust, deaccessioning and disposal | Written case, ownership proof, risk/cost review, governing approval, register update, ethics, and retained audit documentation. | [Deaccessioning and disposal](https://collectionstrust.org.uk/resource/deaccessioning-and-disposal-the-spectrum-standard/) |
| S6 | ICOM Code of Ethics for Museums | Minimum professional standards covering acquisition, law, due diligence, provenance, security, returns/restitution, and disposal. | [ICOM Code of Ethics](https://icom.museum/en/resources/standards-guidelines/code-of-ethics/) |
| S7 | ICOM ETHCOM Standards on Accessioning | Public trust, rightful ownership, provenance, permanence, documentation, accessibility, resources, published policy, conflicts, named roles, multiple perspectives, and retained decision records. | [Standards on Accessioning PDF](https://icom.museum/wp-content/uploads/2022/02/Accessioning-Standards_EN.pdf) and [ICOM standards index](https://icom.museum/en/resources/standards-guidelines/) |
| S8 | ICOM Object ID | Nine minimum categories: type, materials/techniques, measurements, inscriptions/markings, distinguishing features, title, subject, date/period, maker; photographs, description, and secure storage. | [Object ID](https://icom.museum/en/resources/standards-guidelines/objectid/) |
| S9 | CIDOC CRM 7.1.3 official ISO correspondence | Formal ontology for integration, mediation, and interchange of heterogeneous cultural-heritage information. Later 7.3.x releases were drafts at retrieval; do not use a draft as an unannounced production namespace. | [CIDOC CRM versions](https://cidoc-crm.org/versions-of-the-cidoc-crm) |
| S10 | LIDO 1.1 schema and 2025 primer | Exchange/harvesting schema for object descriptions, events, authorities, multilingual labels, administrative rights, and resource representations; supports Spectrum and CIDOC CRM concepts. | [LIDO schema](https://lido-schema.org/schema/latest/lido.html) and [LIDO Primer](https://lido-schema.org/documents/primer/latest/lido-primer.html) |
| S11 | PREMIS 3.0 | Preservation metadata data model with Objects, Events, Rights, and Agents, plus schemas, controlled vocabularies, and implementation guidance. | [PREMIS 3.0](https://www.loc.gov/standards/premis/v3/index.html) and [PREMIS home](https://www.loc.gov/standards/premis/) |
| S12 | IIIF Presentation 3.0 / Image 3.0 | Interoperable viewing and presentation resources; identifiers, types, manifests/canvases, labels, representations, rights, and HTTP-discoverable resources. | [IIIF API index](https://iiif.io/api/) and [Presentation API 3.0](https://iiif.io/api/presentation/3.0/) |
| S13 | C2PA 2.4 | Cryptographically verifiable assertions, claims, signatures, manifests, content bindings, provenance, validation, and signer identity for digital assets. | [C2PA 2.4 index](https://spec.c2pa.org/specifications/specifications/2.4/index.html) and [C2PA Technical Specification 2.4](https://spec.c2pa.org/specifications/specifications/2.4/specs/C2PA_Specification.html) |
| S14 | BagIt 1.0 / RFC 8493 | Hierarchical payload/tag package, manifests, checksums, direct file access, and transfer/integrity semantics. The RFC is informational, not an IETF Standards Track document. | [RFC 8493](https://datatracker.ietf.org/doc/html/rfc8493) |
| S15 | OCFL 1.1 | Application-independent storage with completeness, parsability, robustness, versioning, storage diversity, inventories, manifests, and fixity. | [OCFL overview](https://ocfl.io/) and [OCFL 1.1 specification](https://ocfl.io/1.1/spec/) |
| S16 | The Metropolitan Museum of Art, public collection and policy | Public object fields, object numbers, credit lines, rights split, open-access data/images, public feedback, policy-level acquisition and provenance controls. | [Met policies](https://www.metmuseum.org/about-the-met/policies), [image and data resources](https://www.metmuseum.org/policies/image-resources), [public object record](https://www.metmuseum.org/art/collection/search/436535), [public collection API record](https://collectionapi.metmuseum.org/public/collection/v1/objects/436535) |
| S17 | The Museum of Modern Art, public policy and collection record | Mission fit, care resources, clear title, donor restrictions, committee approval, curator rationale, condition/provenance review, permanent records, object number, credit line, public provenance research, and feedback. | [MoMA Collections Management Policy](https://www.moma.org/docs/about/Collections-Management-Policy-2020-04-20.pdf), [public object/provenance record](https://www.moma.org/collection/works/79347?page=1&sov_referrer=provenance) |
| S18 | Centre Pompidou, public collection and reproduction practice | Public collection record with artist, title, date, domain, technique, dimensions, acquisition, inventory number, subject terms, rights/credit, image reference, bibliography; separate reproduction request workflow. | [public collection object](https://www.centrepompidou.fr/en/ressources/oeuvre/c8E4L9r), [visual-arts collection](https://www.centrepompidou.fr/en/collection/visual-arts), [loan and reproduction requests](https://www.centrepompidou.fr/en/offer-to-professionals/loan-and-reproduction-requests) |

## 4. Standards crosswalk

The `Required / conditional` column is a Museum implementation decision, not a claim that every source uses the same word. `Required` means every completed accession record must contain the field or an explicit `not_applicable`, `unknown`, or `restricted` state. `Conditional` means the field becomes required when the object, rights, pathway, or preservation risk makes it relevant.

| Source | Source requirement or capability | Museum working implementation | Required / conditional | Minimum evidence / visibility |
|---|---|---|---|---|
| S1–S2 Spectrum acquisition/accessioning | Make a written case, perform due diligence, record object identity, method, source, date, title/conditions, rationale, credit line, restrictions, and retain supporting documents. | `acquisition-proposal`, `acquisition-method`, `source-agent`, `acquisition-date`, `object-schedule`, `title-instrument-ref`, `conditions`, `credit-line`, `restriction-set`, `rationale`, and `evidence-refs`. | Required for every acquisition; donor/vendor contact details conditional and restricted. | A/B/C; public summary plus restricted instrument hash/reference. |
| S1 Object entry | Record what entered custody, assign a unique number, identify objects and parts, and preserve initial information. | Create an `entry` record before accession. Assign a Museum object ID even if the token is unaccessioned; do not use wallet address or token ID as the accession number. | Required on receipt or intake; separate temporary intake ID from permanent accession ID. | A/C; object identity and intake date public, personal data restricted. |
| S1 Cataloguing | Maintain an ongoing, multi-perspective record that retrieves known information and cross-references supporting files. | Separate factual cataloguing from curatorial interpretation; add `record-version`, `source-date`, `authority-refs`, `related-works`, `bibliography`, and `amendment-lineage`. | Required for catalogue-ready state; extended scholarship conditional. | A/B/C/D/E according to claim; public factual record and interpretive attribution. |
| S3 Rights management | Record rights held by the institution and others, permissions, licences, rightsholder contacts, due diligence, and expiry. | Store token ownership, legal title, copyright, moral rights, display, reproduction, publication, preservation, migration, derivative, AI-training, and commercial permissions as separate assertions. | Rights basis/status required; each individual grant is conditional on relevance and known evidence. | B/A where on-chain; public rights summary; instruments/contact data restricted. |
| S4 Condition/technical assessment | Record condition/make-up, event reference, date, checker, method, reason, notes, results, and recommendations; escalate to specialist where needed. | Assess token, contract, metadata, media, script, dependencies, renderer, output, and documentation separately. Use `green`, `amber`, `red`, `not_assessed`, with narrative and test evidence. | A technical intake check required; deeper reports conditional on medium, risk, or display state. | C plus A/B sources; public status summary, detailed exploit/security notes restricted if sensitive. |
| S5 Deaccessioning/disposal | Written case, ownership proof, risk/cost review, governing approval, register update, ethics, retained documentation. | Add append-only `deaccession-proposal`, `deaccession-decision`, `disposition-event`, and successor/retained-record links. Disposal is not a destructive Git rewrite or silent token transfer. | Conditional only when proposed; controls must exist before first accession. | A/B/C; public decision and current status, restricted legal/operational detail as needed. |
| S6–S7 ICOM ethics/accessioning | Collections are held in public trust; consider mission, significance, provenance, rightful title, law, resources, permanence, accessibility, restrictions, conflicts, and multiple perspectives; publish/update policy and preserve decision records. | Require mission-fit, collection-fit, significance, title/provenance, sanctions/legal, rights, care cost, sustainability, access, conflict, and curatorial-independence findings. Identify constructor, checker, recommending curator, registrar, approver, and any external specialist. | All accession proposals; fields may be `unknown` only with a documented remediation owner and state. | A–E with provenance; decision summary public, conflicts/legal instruments restricted. |
| S8 Object ID | Nine categories and secure documentation help identify/recover cultural objects. | Adapt to digital/tokenized art: object type, medium/technical technique, dimensions/duration, inscriptions/metadata markings, distinguishing hash/seed/traits, title, subject, creation/release dates, and maker/artist authority. Add chain identity as a Museum extension. | Required for every catalogued object; photographic/visual representation conditional on the work and rights. | A/B/C; public object identifier and approved representation, restricted security copies when necessary. |
| S9 CIDOC CRM | Use an event-centred conceptual model to integrate and interchange cultural-heritage information. | Model creation, minting, metadata publication, transfer, title passage, receipt, accession, condition check, preservation event, exhibition, interpretation, correction, and deaccession as distinct events linked to agents, times, places, objects, records, and sources. | Event timeline required for accession; optional CRM/RDF export becomes required at exchange/on-chain readiness. | A/B/C/D/E per event; public event summary and source links, restricted personal/legal details. |
| S10 LIDO | Deliver object metadata for discovery/aggregation, with descriptive and administrative metadata, events, authorities, multilingual support, and resource links; distinguish object, page, surrogate, and LIDO record IDs. | Publish a Museum LIDO profile that preserves `museum-object-id`, `chain-subject`, `record-id`, `record-source`, title, type, creator, dates, technique/medium, measurements, events, subjects, rights, resource representations, and source/revision data. | Required for public catalogue/export; richer fields conditional on available scholarship. | A/B/C/E; public export excludes restricted donor/legal/security fields. |
| S11 PREMIS | Preservation record has Objects, Events, Rights, Agents and semantic units for long-term usability. | Treat token, contract metadata, script, dependency set, renderer/environment, generated output, documentation surrogate, IIIF manifest, C2PA manifest, BagIt package, and OCFL object as distinct preservation objects where appropriate. Record ingest, validation, fixity, render, migration, recovery, and access events. | Required for preservation-complete; environment and migration events conditional on medium and future action. | A/C for technical events; public preservation summary and hashes, sensitive infrastructure restricted. |
| S12 IIIF | Presentation resources require stable IDs/types and interoperable manifests/canvases/resources; Image API provides standard image requests. | Create IIIF Presentation 3.0 manifests for public visual manifestations or documentation surrogates. Use stable HTTP IDs, explicit label, attribution/rights, dimensions, media type, and links to the chain subject and Museum object. A still is a surrogate unless the artist or project defines it as the work’s manifestation. | Conditional for visual/audio/video/3D/public display; required for a public presentation-ready visual object when technically feasible. | C/B; public manifest and approved resources, restricted high-resolution masters where rights/security require. |
| S13 C2PA | Assertions are signed into claims/manifests, cryptographically bound to assets, and validated through signer identity, signature, timestamp, and content binding. It provides trust signals; it does not make a value judgment. | Preserve source C2PA manifests when present. For Museum-created captures or derivatives, optionally issue a Museum-signed manifest that says exactly what the Museum did; never assert artist origin, mint authenticity, or legal title merely because a Museum key signed a derivative. | Conditional; required only where a creator/issuer supplies it or the Museum generates a signed derivative/preservation capture. | B/C; manifest and validation result public where safe, signer infrastructure and private keys never. |
| S14 BagIt | Package payload plus tag files; support manifests and checksums; direct file access; valid bags verify listed content. | Every accession or preservation packet has a reproducible BagIt package with `bagit.txt`, SHA-256 manifest, optional stronger manifest, `bag-info`, provenance/title/rights/condition/preservation records, and pointers to external chain evidence. | Required for preservation-complete and release artifacts; optional at early intake. | A/C; package and manifest public if rights allow; restricted annex separate. |
| S15 OCFL | Store objects in a transparent, predictable, versioned layout with inventory, manifest, fixity, and reconstructable history. | Use one OCFL object per Museum accession dossier or defined preservation object; append versions for corrections/migrations; never replace historical content without preserving the prior inventory and digest. | Required when the Museum operates a durable storage layer; GitHub alone is not a substitute for OCFL. | C; public OCFL metadata/manifests and content where licensed; infrastructure locations may be restricted. |
| S16–S18 public institutional practice | The Met, MoMA, and Centre Pompidou expose stable object numbers/inventory numbers, creator/title/date, medium/technique, dimensions, acquisition/credit, rights, images or image references, subjects/classification, provenance or bibliography, and public feedback/reproduction paths. | Use a public object page that is concise but complete enough for independent identification and research. Include stable Museum ID, chain subject, creator authority, title, date, medium, manifestation, acquisition method and credit, provenance summary, rights, technical/preservation status, curatorial statement, source/update date, and feedback/correction path. | Required for public catalogue; individual fields may be unknown with explicit status. | A/B/C/E; public rights status and source links; restricted agreements/contact details. |

## 5. Core record field profile

This is the proposed Museum field profile. It is designed to fit the existing Stream-shaped record envelope while leaving the human-facing record readable. Each field should be represented as an assertion with value, status, evidence, source, observation time, and attribution; a bare string without that context is insufficient for a permanent record.

### 5.1 Assertion wrapper

Every material fact should be representable as:

```json
{
  "value": "example",
  "assertion_status": "verified",
  "evidence_class": "A",
  "source_refs": ["source-id"],
  "observed_at": "2026-08-01T00:00:00Z",
  "asserted_by": "agent-or-institution-id",
  "source_hash": "sha256:..."
}
```

Allowed `assertion_status` values should include at least `verified`, `reported`, `inferred`, `disputed`, `unknown`, `not_applicable`, `restricted`, and `superseded`. `inferred` is never silently promoted to `verified`.

### 5.2 Required and conditional field matrix

| Domain | Required for every completed accession | Conditional or extended fields | Evidence floor | Public / restricted treatment |
|---|---|---|---|---|
| Museum identity | `museum_object_id`, `accession_lot_id`, `object_status`, `record_version`, `record_created_at`, `record_updated_at`, `record_source`, `amendment_lineage` | Part/component IDs, group/lot relationships, temporary intake ID | C for assignment; A/B/C for status | Public object ID and status; internal workflow notes may be restricted. |
| Chain identity | `chain_namespace`, `network_id`, `contract_address`, `token_standard`, `token_id` or equivalent subject, canonical subject citation, chain identity evidence refs | Token hash/seed, project/collection ID, metadata URI history, proxy/upgrade admin, contract source verification, bridge/wrapped-asset lineage | A | Public when safe; security-sensitive admin analysis can be restricted but the fact of a limitation must remain visible. |
| Acquisition | `acquisition_method`, `acquisition_date`, `source_agent_ref`, `acceptance_authority_ref`, `acquisition_rationale`, `title_binding_ref`, `conditions_status` | Purchase price, appraisal, tax data, donor contact, promised gift, escrow, funding allocation, program budget | B plus A for transfer | Public method/date/rationale/credit; instrument, price, contacts, and tax material restricted. |
| Custody | `custody_status`, `receiving_custodian_ref`, `receipt_transaction_ref` or off-chain receipt, `last_verified_at`, custody assertion status | SAFE configuration, signer details, key ceremony, hardware, recovery locations, chain finality parameters | A/C | Public receiving address/reference and verification date; signer/security details restricted. |
| Title and provenance | `title_status`, `provenance_summary`, transfer/event timeline, source quality, unresolved gaps, claim/dispute status | Prior-owner identity, marketplace records, legal opinions, export/import records, stolen-art databases, confidential correspondence | A/B/D | Public history and gap statement; private identities and legal correspondence restricted. |
| Art identity | `title`, `creator`, creator authority ref or `authority_unavailable`, `creation_date_or_range`, `object_type`, `medium_or_technical_technique`, `distinguishing_description`, `credit_line` | Alternate titles, language variants, edition statement, series, subject, place, inscriptions, bibliography, exhibition/publication history | B/C/E depending on field | Public catalogue; sensitive content warnings and unpublished research can be restricted. |
| Object ID minimum | Object type, medium/technique, dimensions/duration, distinguishing features, title, subject, date/period, maker, approved identifying representation | Inscriptions/markings become metadata/contract/seed/artist signature equivalents; additional photographs or forensic captures | B/C | Public where rights permit; security copies may be restricted. |
| Technical constitution | `technical_medium`, token standard, rendering mechanism, metadata/script/dependency references, mutability status, renderer/test method, output capture status | Language/runtime versions, browser/OS/GPU, audio/network/timing, source code, exact dependency lockfile, random seed model, variable state, external APIs | A/B/C | Public technical summary and hashes; exploit paths, private infra, and source assets only if rights/safety allow. |
| Rights | Rights holder(s) or unknown status, token/title/IP separation, display/publication/reproduction/preservation status, credit, instrument/source ref, expiry/review date | Derivative, migration, commercial, AI-training, merchandising, accessibility, sublicensing, moral-rights or privacy restrictions | B; A for chain rights; C for Museum-generated rights | Public rights summary and license links; donor agreement and personal data restricted. |
| Condition/integrity | Assessment date, assessor, method, object/metadata/media/renderer coverage, status for each component, narrative, evidence refs | Full technical report, security review, vulnerability detail, recovery test, failed renders, conservation recommendation | C plus A/B | Public status and remediation summary; detailed security or personal material restricted. |
| Preservation | Preservation-object list, fixity algorithm/digests, BagIt/OCFL/IIIF refs where applicable, environment reference, ingest/validation events, recovery state | Migration plan, multiple replicas, storage provider, bit-level logs, emulation/container recipe, format risk | C | Public manifests/hashes and broad recovery statement; exact locations and security architecture restricted. |
| Display/access | Manifest or access URI, manifestation type, display instructions, accessibility notes, credit/attribution, content warning if needed | Hardware, installation geometry, live-network requirement, interaction, audio, timing, fallback, artist-approved surrogate rules | B/C | Public access route and display summary; operational credentials or private endpoints restricted. |
| Curatorial interpretation | Selection rationale, significance, collection relationship, scope/non-claims, author, date, review status | Comparative scholarship, bibliography, interviews, interpretive alternatives, community/artist review | E with source refs | Public after curatorial review; drafts and sensitive research may remain restricted. |
| Governance/review | Pathway, approval decision, decision source, constructor, checker, registrar, curator, technical reviewer, approval timestamps, payload hash | External specialist, conflict disclosure, abstention, dissent, amendment, remediation owner | B/C | Public decision and responsible roles; personal contact/security details restricted. |

### 5.3 Unknown is a valid state, omission is not

If a field cannot yet be established, the record should state `unknown` or `not_assessed`, identify the reason, list the next research action, assign an owner, and keep the object out of any state whose completion gate depends on that fact. This is particularly important for title, rights, provenance, mutability, code availability, and reproducible rendering.

## 6. Evidence classes and claim discipline

The Museum’s existing five-class model is a useful local control. It is not a replacement for the cited standards; it is the provenance layer that makes the standards auditable in a decentralized system.

| Class | Meaning | Examples for tokenized art | What it can establish |
|---|---|---|---|
| A | Directly chain-verifiable evidence | Contract bytecode, token ID, mint/transfer transaction, block, event log, current owner, URI response observed at a stated time | Chain subject identity, observed custody, transfer chronology, contract state at an observation point. It does not by itself establish copyright or legal title. |
| B | Authoritative issuer, artist, donor, or governance evidence | Signed artist statement, issuer documentation, adopted Wave decision, executed title instrument, donor consent, project source repository | Authorship, intended medium, rights grant, acquisition authority, governance approval, artist intent. Verify authenticity and scope. |
| C | Museum-generated technical verification | Independent render, metadata capture, fixity check, C2PA validation, BagIt validation, OCFL validation, condition report | What the Museum observed or reproduced, by what method, on what environment, and with what result. It does not prove an external claim simply because the test passed. |
| D | Third-party historical or analytical evidence | Public catalogue, bibliography, archive, marketplace history, external provenance research, transparent generative analysis | Context and corroboration. It is not chain state, legal title, or intrinsic artwork identity. |
| E | Curatorial interpretation | Significance, selection rationale, relation to movements/works, interpretive thesis, public-facing essay | Meaning and institutional interpretation, attributed to its author and review date. It is not a factual substitute for A–D. |

### 6.1 Required source metadata

Every source reference should include:

- stable source ID;
- direct URL or content-addressed URI;
- source title and publisher/issuer;
- observed/retrieved date and time in UTC;
- source type and evidence class;
- content hash when a copy is retained or when the source is material to a decision;
- relevant block/transaction/serial/drop ID for on-chain or governance evidence;
- extraction note identifying the exact fact supported;
- access or restriction status;
- supersedes/superseded-by when a correction is published.

### 6.2 Prohibited evidence shortcuts

- Do not use OpenSea rarity rankings as an authenticity, significance, or accession criterion. They are mutable third-party market displays and are not a Museum standard.
- Do not treat a marketplace’s “owner” field as legal title or current chain custody without independent chain verification.
- Do not treat a generated image, screenshot, thumbnail, or video as the tokenized work unless the artist/project record establishes that manifestation.
- Do not treat a C2PA signature as proof of chain provenance, title, authorship, or artistic value; it proves only the claims and bindings that validate under its trust model.
- Do not treat an artist or donor statement as chain state; retain it as B evidence and compare it with A evidence.
- Do not treat a vote result, program selection, or preapproved collection as accession of a specific object.

## 7. Public and restricted data boundary

### 7.1 Public by default after accession

- Museum object and accession identifiers;
- object title, creator, project/series, date, medium/technical technique, type, dimensions/duration;
- canonical chain subject, contract, token ID, network, and public transaction references;
- acquisition method, acquisition/acceptance dates, public credit line, and public donor attribution or approved anonymity label;
- provenance summary, gaps, disputes, and source references;
- rights status, licenses, attribution, and reproduction conditions;
- technical/preservation summary, fixity digests, manifests, condition state, and last verification date;
- approved images, video, audio, 3D or other manifestations and their IIIF/C2PA records where available;
- curatorial statement, significance, collection relationships, bibliography, exhibition/publication history;
- review state, correction history, and public feedback/correction route.

### 7.2 Restricted unless there is a reviewed reason to publish

- donor personal contact data, identity documents, private wallet attribution, and private communications;
- signed legal instrument contents, tax/appraisal material, legal advice, and private consent details;
- SAFE signer roster, signing policy internals, key ceremony, hardware, recovery, private endpoints, and operational security;
- exact private storage locations, credentials, unredacted logs, vulnerability details, and abuse-sensitive technical data;
- non-public artist files or source code where the artist has not granted access;
- sensitive personal data depicted in a work or provenance file;
- internal reviewer comments that contain personal or security information.

Restricted data must not be silently dropped. The public assertion should state `restricted`, include a stable non-sensitive reference and a content hash where permissible, and state the reason and review authority.

## 8. Constructor–reviewer control model

### 8.1 Roles

The role names below are proposed implementation roles. One person may hold more than one role only when the record explicitly discloses the combination and a genuinely independent checker remains available.

| Role | Responsibility | Cannot be the sole approver for |
|---|---|---|
| Intake registrar | Opens intake, assigns temporary ID, captures receipt, quarantines unsolicited material, starts evidence ledger. | Accession, title acceptance, or public completion. |
| Constructor | Builds the proposed record, normalizes sources, prepares manifests, writes factual and curatorial drafts, and signs the payload hash. | Independent review of their own work. |
| Curatorial constructor | Researches significance, collection relationship, and interpretive thesis; attributes claims and alternatives. | Sole chain/title/rights verification. |
| Technical constructor | Captures metadata/code/dependencies, performs render and fixity tests, builds preservation package. | Sole rights/title/acquisition approval. |
| Rights/registrar checker | Checks title instrument, donor authority, conditions, rights scope, provenance, restrictions, and acquisition pathway. | Approving an unresolved conflict in which they are personally interested. |
| Technical checker | Repeats or independently validates chain, URI, fixity, rendering, preservation, and C2PA/BagIt/OCFL results. | Treating a failed or partial test as complete. |
| Curatorial checker | Challenges selection rationale, historical claims, language, collection fit, and non-claims. | Changing factual chain/title evidence without registrar sign-off. |
| Registrar / accession authority | Confirms all gates, assigns permanent accession number, and records the institutional act. | Bypassing a missing required review or restricted instrument. |
| Publication constructor | Produces public object page, LIDO, IIIF, manifests, and release bundle from approved records. | Altering approved facts or rights without amendment. |
| Release checker | Verifies public/restricted split, schema/CI output, hashes, links, and no secrets/private data. | Publishing a package with failed checks. |

### 8.2 Maker–checker minimum evidence

Each completed accession must record:

```text
constructor: person/agent ID, role, timestamp, payload hash
independent_checker: person/agent ID, role, timestamp, checked payload hash
registrar_decision: person/agent ID, authority, decision timestamp, accession state
curatorial_review: person/agent ID, scope, timestamp, interpretation hash
technical_review: person/agent ID, protocol/environment, result, evidence refs
rights_review: person/agent ID, rights scope, instrument/source refs, result
```

The checker must not merely check formatting. The review must include substantive verification of the fields assigned to that role. A GitHub approval can be one record of review, but it is not enough unless its identity, scope, commit/payload hash, and change set are retained in the Museum record.

### 8.3 Review gates

| Gate | Required artifacts | Pass condition |
|---|---|---|
| G0 Intake | Temporary ID, receipt event, object lead, quarantine status, initial source list | Receipt is recorded; no accession claim is made. |
| G1 Eligibility | Mission/collection fit, pathway, approval source, conflict check, resource/risk screen | Correct accession pathway is identified and authorized. |
| G2 Identity | Object ID minimum, CAIP-19-shaped chain subject, contract/token checks, metadata snapshot | The exact work/token is uniquely identified; unresolved ambiguity is visible. |
| G3 Title/provenance | Donor/seller authority, transfer, title instrument, provenance timeline, dispute/sanctions review | Legal title and chain custody assertions are separately supported or explicitly unresolved. |
| G4 Rights/conditions | Rights matrix, donor conditions, credit line, reproduction/display/preservation permissions, restriction decision | No material rights or condition gap is hidden; unacceptable conditions are rejected or escalated. |
| G5 Technical | Independent render/inspection, metadata/code/dependency and mutability report, fixity, security notes | The work’s constitution and present condition are documented with reproducible tests. |
| G6 Preservation/access | BagIt/OCFL/IIIF/C2PA artifacts as applicable, recovery test or plan, public/restricted split | Required preservation objects and public manifestations are valid and linked. |
| G7 Curatorial | Collection-level and object-level statements, references, author/checker, non-claims | Interpretation is attributed, sourced, reviewed, and not presented as chain fact. |
| G8 Accession | Accession statement, object schedule, review events, payload hash, accession register update | Registrar records the formal accession act; status becomes `accessioned`. |
| G9 Publication | Public record, LIDO/IIIF exports, release manifest, secret/restricted scan, link check | Public package is reproducible, safe, rights-aware, and references the approved payload. |

### 8.4 Exceptions

An exception may shorten timing but may not erase evidence. It must state:

- the gate or field being excepted;
- why it cannot be completed now;
- who authorized the exception and under what authority;
- the risk and public disclosure decision;
- remediation owner and due date;
- the state to which the object is limited until remediation;
- the amendment that will close or supersede the exception.

No exception may convert `unknown`, `disputed`, or `not_assessed` into `verified` by assertion alone.

## 9. Tokenized and generative-art extensions

### 9.1 Model the artwork and token as related, not identical

The Museum record should represent at least these entities:

| Entity | Meaning | Example evidence |
|---|---|---|
| Artwork/work | The artist’s work or project as a cultural object. | Artist/project statement, catalogue, contract semantics. |
| Tokenized instance | A specific on-chain token or equivalent object. | Contract, token ID, mint event, token metadata. |
| Manifestation | A render, live generative view, still, video, audio, 3D scene, or installation. | IIIF resource, capture, renderer/environment, artist instructions. |
| Preservation object | A file, package, script, dependency, metadata snapshot, or environment record retained for future use. | PREMIS object, BagIt payload, OCFL inventory. |
| Event | Creation, mint, metadata update, transfer, title passage, receipt, accession, render, preservation, display, correction. | A/B/C/D/E event record. |
| Agent | Artist, issuer, donor, buyer/seller, Museum role, signer, platform, software, or external institution. | Authority record and attribution. |
| Record | Accession, work description, rights, condition, PREMIS, LIDO, IIIF, C2PA, acquisition packet, or curatorial statement. | Stream-compatible record envelope. |

The chain subject is a typed identity; it is not a substitute for the Museum accession number. Legal title is not a synonym for current token custody. Copyright is not a synonym for either.

### 9.2 Generative work requirements

For a generative or algorithmic object, the constructor should capture:

- project and token identity, including token hash/seed when the project exposes it;
- generator/script location, version, and digest;
- language/runtime and dependency versions or lockfile;
- renderer and environment used for each Museum capture;
- metadata and source URI snapshots, with dates and digests;
- mutability: immutable, issuer-updatable, owner-configurable, externally dependent, or unknown;
- randomness model and deterministic/reproducibility claim;
- output dimensions, colour profile, timing, animation, audio, interaction, network, and device requirements;
- known differences between the live work, artist-approved display, and Museum documentation surrogate;
- technical/condition status for every material component;
- artist/project instructions and rights for capture, display, preservation, migration, and derivative documentation;
- transparent analytical metrics, if used, with method version, source data, script digest, results, and limitations.

### 9.3 Rarity and trait analysis

The Museum must not use OpenSea rarity metrics as an accession, significance, or curatorial ranking input. For any generative collection where analytical distribution is useful, the Museum should instead:

1. identify the authoritative trait/feature source (project metadata, script output, or a Museum-derived measurement);
2. publish the exact analysis script and dependency lockfile;
3. pin the input snapshot and hash it;
4. describe every normalization, exclusion, and missing-value rule;
5. distinguish issuer-authored traits from Museum-derived traits;
6. calculate results deterministically with a reproducible command;
7. publish raw result tables or a content-addressed equivalent where rights allow;
8. report algorithm version, run timestamp, runtime, and output digest;
9. label the result as dated analysis, not intrinsic value or authenticity;
10. have a second reviewer rerun the script from the pinned inputs and compare the digest.

The intended design is an open, transparent, internally consistent analytical layer that can be calculated for any accessioned generative collection. It must be independent from marketplace ranking systems and must not be backfilled into historical accession decisions without an amendment.

## 10. Stream bilateral interoperability profile

The Museum should preserve 6529Stream’s exact envelope whenever the concept is shared:

```solidity
struct HashRef {
    uint16 algorithm;
    bytes digest;
    bytes32 canonicalizationId;
}

struct CollectionRecord {
    bytes32 recordType;
    bytes32 subjectId;
    HashRef contentHash;
    string uri;
    bytes32 schemaId;
    bytes32 signatureScheme;
    HashRef signatureHash;
    uint64 effectiveAt;
}
```

Implementation requirements:

- use the pinned Stream hash and canonicalization identifiers in `docs/stream-interoperability.md`;
- use RFC 8785-compatible canonical JSON for payloads where the profile requires it;
- preserve Keccak-256 commitments for on-chain record identity and SHA-256 for file/package fixity;
- use `ACCESSION`, `WORK_DESCRIPTION`, `RIGHTS_STATEMENT`, PREMIS, LIDO, IIIF, BagIt, and acquisition-packet profile identifiers without redefining their meanings;
- add Museum-specific fields through a versioned profile and explicit mapping, not by silently overloading Stream fields;
- preserve a `TITLE_BINDING` that links the legal title instrument to the exact on-chain transfer, while keeping the acquisition packet distinct from the accession statement;
- use the same provenance-entry shape for human-facing events, with `entry_id`, `entry_type`, `occurred_at`, `title`, `description`, and `evidence_refs`;
- record any Stream schema/profile drift by comparing pinned IDs, source document hashes, round-trip output, and release manifest before publication or contract deployment.

### 10.1 Proposed external-work mapping

For works minted outside Stream, the Museum’s future external-works registry should register the external chain subject and Museum accession linkage; it should not wrap, remint, or imply that the Museum is the original issuer. Stream-native records can still describe the Museum accession, work, rights, condition, preservation, and acquisition packet, with the external token represented as the subject or related subject.

## 11. Public institutional practice: what is evidenced and what is not

The Met, MoMA, and Centre Pompidou pages are not standards and should not be copied as if they were universal law. They are useful public comparators because they show what mature institutions expose to researchers and how public policy relates to collection records.

### 11.1 The Met

The Met’s public object page and collection API expose a stable accession number, artist authority links, title, date, medium, dimensions, credit line, classification, rights/public-domain state, image resources, metadata date, repository, and object URL. Its image/data policy explicitly separates public-domain images from restricted images while making basic collection data available under CC0; it also states that catalogue completeness varies and that data is updated regularly.

Implementation lesson: publish a stable object record and data export, separate metadata openness from image rights, expose a clear rights state, and never imply that a sparse public record means the research is complete.

### 11.2 MoMA

MoMA’s public Collections Management Policy requires mission relevance, capacity to care, firm legal title, review of restrictions, committee approval before accession, curator rationale, condition/provenance checks, and complete records. The policy distinguishes approval from accession numbering and requires permanent acquisition records. Its public object records expose medium, dimensions, credit, object number, copyright, provenance, installation history, licensing routes, and a feedback/correction path; the provenance pages explicitly say research is ongoing.

Implementation lesson: require a documented approval rationale, title and care review, a distinct accession number, exact credit line, ongoing provenance label, public correction channel, and a permanent evidence trail.

### 11.3 Centre Pompidou

The public object record examined here exposes artist authority, title, date, collection domain, technique, dimensions, acquisition method/date, inventory number, subjects, rights/credit, photo credit, image reference, detailed description, and bibliography. Its professional page separates collection records from reproduction requests and requires an inventory number and work list for rights handling.

Implementation lesson: retain an inventory/accession identity, acquisition details, technique/medium, authority links, subject vocabulary, image/representation credits, bibliography, and a separate rights/reproduction workflow.

### 11.4 Boundary of the comparator evidence

These public pages evidence published practice and policy language, not each institution’s confidential registrar workflow, staff permission model, storage architecture, or legal advice. The Museum should cite them as examples of public accountability and record richness, never as evidence that a private procedure has been inferred.

## 12. Implementation checklist for the repository

The documentation and CI system should eventually enforce the following:

### 12.1 Schema and semantic validation

- validate JSON Schema and profile IDs;
- require stable Museum IDs and typed chain subjects;
- require assertion status, evidence class, source refs, observation time, and attribution for material claims;
- reject accession status if title binding, custody, rights, technical, curatorial, or checker gates are missing;
- prohibit wallet-derived accession numbers and implicit `WINNER`/transfer-to-accession promotion;
- reject unbounded external URLs in final records unless the source has retrieval metadata or a declared live-source policy;
- require `unknown`, `not_assessed`, or `restricted` rather than missing values for required concepts;
- verify public/restricted field policy and prevent restricted payloads from entering public exports.

### 12.2 Integrity and reproducibility

- produce deterministic SHA-256 and Stream-compatible Keccak/JCS manifests;
- verify BagIt manifests and OCFL inventories where present;
- rerun generative analysis from pinned inputs and compare outputs;
- record renderer/environment for every technical capture;
- validate IIIF JSON-LD and resource IDs for public visual objects;
- validate C2PA manifests when supplied or generated, while recording validation result and signer trust scope;
- preserve append-only amendments and superseded hashes;
- run link, secret, privacy, and rights scans before publication.

### 12.3 Review automation

- require constructor and independent checker metadata in accession records;
- require separate technical, rights/registrar, and curatorial checks for completed accessions;
- require a release checker for public/restricted split and public URLs;
- make CI report failures by Museum object ID, record type, gate, and source reference;
- publish a machine-readable validation report alongside the release manifest;
- fail closed for accidental private key, JWT, credential, donor-contact, or SAFE-internal material.

### 12.4 Version pinning

The standards register must record:

- source URL;
- exact version or revision;
- retrieval date;
- local source digest where retained;
- schema/profile namespace;
- mapping version;
- conformance test status;
- owner for repinning;
- change note and effective date.

When a standard changes, the Museum should not silently rewrite existing records. It should publish an amendment or a new profile version, rerun conformance tests, and state whether the change affects interpretation, serialization, or only validation tooling.

## 13. Immediate constructor priorities

1. Freeze the source register and exact Stream identifiers used by the Museum profile.
2. Add schemas for the assertion wrapper, accession statement, object record, rights matrix, condition/technical report, PREMIS event, LIDO export, IIIF manifest, BagIt metadata, review event, and public/restricted projection.
3. Create fixtures for one external generative token, one externally minted photographic work, and one multi-object donation lot.
4. Build the constructor/checker workflow and require the second-person review record before `accessioned`.
5. Build the no-OpenSea generative-analysis contract: pinned input, open script, deterministic results, output digest, limitations, and rerun check.
6. Add a standards-drift job that checks pinned source/profile versions and opens a review issue when a source changes.
7. Use the Casey Reas collection as the first high-rigor accession test, but do not state that any token is accessioned until title, custody, rights, technical, preservation, and independent review gates pass.

## 14. Sources and retrieval notes

The source register in section 3 is the citation index for this note. The most important implementation sources are repeated here for auditability:

- [Spectrum 5.1](https://collectionstrust.org.uk/spectrum/) — retrieved 2026-08-01 UTC.
- [Spectrum acquisition and accessioning](https://collectionstrust.org.uk/resource/acquisition-and-accessioning-suggested-procedure/) — retrieved 2026-08-01 UTC.
- [Spectrum rights management](https://collectionstrust.org.uk/resource/rights-management-the-spectrum-standard/) — retrieved 2026-08-01 UTC.
- [Spectrum condition and technical assessment](https://collectionstrust.org.uk/resource/condition-checking-and-technical-assessment-suggested-procedure/) — retrieved 2026-08-01 UTC.
- [Spectrum deaccessioning and disposal](https://collectionstrust.org.uk/resource/deaccessioning-and-disposal-the-spectrum-standard/) — retrieved 2026-08-01 UTC.
- [ICOM Code of Ethics](https://icom.museum/en/resources/standards-guidelines/code-of-ethics/) — retrieved 2026-08-01 UTC.
- [ICOM Standards on Accessioning](https://icom.museum/wp-content/uploads/2022/02/Accessioning-Standards_EN.pdf) — retrieved 2026-08-01 UTC.
- [ICOM Object ID](https://icom.museum/en/resources/standards-guidelines/objectid/) — retrieved 2026-08-01 UTC.
- [CIDOC CRM versions and status](https://cidoc-crm.org/versions-of-the-cidoc-crm) — retrieved 2026-08-01 UTC.
- [LIDO schema 1.1](https://lido-schema.org/schema/latest/lido.html) and [LIDO Primer](https://lido-schema.org/documents/primer/latest/lido-primer.html) — retrieved 2026-08-01 UTC.
- [PREMIS 3.0](https://www.loc.gov/standards/premis/v3/index.html) — retrieved 2026-08-01 UTC.
- [IIIF API specifications](https://iiif.io/api/) and [Presentation API 3.0](https://iiif.io/api/presentation/3.0/) — retrieved 2026-08-01 UTC.
- [C2PA Specifications 2.4](https://spec.c2pa.org/specifications/specifications/2.4/index.html) and [technical specification](https://spec.c2pa.org/specifications/specifications/2.4/specs/C2PA_Specification.html) — retrieved 2026-08-01 UTC.
- [BagIt RFC 8493](https://datatracker.ietf.org/doc/html/rfc8493) — retrieved 2026-08-01 UTC.
- [OCFL 1.1](https://ocfl.io/1.1/spec/) — retrieved 2026-08-01 UTC.
- [The Met image and data policy](https://www.metmuseum.org/policies/image-resources), [public object record](https://www.metmuseum.org/art/collection/search/436535), and [collection API](https://collectionapi.metmuseum.org/public/collection/v1/objects/436535) — retrieved 2026-08-01 UTC.
- [MoMA Collections Management Policy](https://www.moma.org/docs/about/Collections-Management-Policy-2020-04-20.pdf) and [public provenance record](https://www.moma.org/collection/works/79347?page=1&sov_referrer=provenance) — retrieved 2026-08-01 UTC.
- [Centre Pompidou public collection object](https://www.centrepompidou.fr/en/ressources/oeuvre/c8E4L9r) and [reproduction workflow](https://www.centrepompidou.fr/en/offer-to-professionals/loan-and-reproduction-requests) — retrieved 2026-08-01 UTC.

## 15. Open questions retained for later design

- Which exact CIDOC CRM release will the Museum pin for production export when 7.3.x becomes official, and what is the versioned mapping for token, manifestation, and accession events?
- Will the Museum publish LIDO 1.1 XML only, or also a JSON-LD projection with a formally registered profile?
- Which OCFL storage implementation and independent replicas will be used for the first durable preservation repository?
- What signing identity and trust policy, if any, should be used for Museum-generated C2PA manifests?
- Which digital condition vocabulary and render-environment profile should become the Museum’s controlled vocabulary?
- What are the minimum public-resolution and accessibility requirements for generative, video, audio, interactive, and live-network work?
- How should the future external-works registry expose a stable relation between an externally minted token, the Museum accession, and Stream-compatible records without implying original issuance?
- What governance action will adopt the working fields and gate thresholds as formal Museum policy?
