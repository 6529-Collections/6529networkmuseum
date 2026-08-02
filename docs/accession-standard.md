# 6529 Network Museum accession standard

Status: working standard for repository records; not yet an adopted governance policy.

The standard is museum-rigorous, chain-native, and reproducible by a third party decades later. It must answer:

1. What exactly did the Museum accession?
2. How did it obtain legal title and on-chain control?
3. Why does the work belong in the collection?
4. How can it be authenticated, rendered, displayed, and preserved?

## Standards base

- Spectrum 5.1 for acquisition/accessioning, inventory, custody, and audit;
- Getty CDWA and CDWA Lite/LIDO for art-historical description and exchange;
- ICOM Object ID for minimum identifying documentation;
- PREMIS v3 for preservation Objects, Events, Agents, and Rights;
- IIIF Presentation 3 for visual-resource manifests;
- BagIt and OCFL mapping for portable dossiers and versioned repository ingest;
- time-based/software-art conservation practice for behavior, dependencies, environment, and artist intent;
- 6529Stream for chain identity, record envelopes, title binding, rights, preservation, dossier, and acquisition-packet semantics.

## Three linked records

### 1. Accession statement

The short, permanent institutional act: the Museum accepted identified objects from an identified source, on a date, under an authority, with stated rights, conditions, and reasons. Corrections are dated amendments, never silent rewriting.

### 2. Individual object record

The living evidentiary record for one artwork: identity, chain facts, title/custody, technical constitution, condition, rendering, preservation, display, rights, provenance, and scholarship. Every object receives its own record even when acquired in a multi-object lot.

### 3. Collection-level curatorial statement

The revisable explanation of why a group belongs together. It does not substitute for individual object records or alter the legal accession act.

## Limited gift authorization before accession completion

A Museum may record a dated **Gift Acceptance and Accession Authorization**
when it formally accepts an identified gift through an adopted collection and
donation pathway. This is a limited administrative record, not a
`STREAM_ACCESSION_V1` certificate. It must bind the exact object schedule,
receipt, donor credit, consideration, governing decisions, and a public
statement of the authority evidence and its limitations. It must also state
permanent-collection intent without implying an unrestricted right to display,
publish, reproduce, preserve, or transfer the work.

Formal gift acceptance does not alone prove legal title, execute a
`TITLE_BINDING`, complete condition or preservation work, authorize display,
or move an object lifecycle state to `accessioned`. Until the executable
Stream-equivalent accession certificate is evidence-backed, the lot and its
objects remain `received_onchain` / `not_complete`; the record must name the
specific completion blockers and retain independent reviewer fields as pending.

## Accession statement minimum

- Museum and governing-entity reference;
- stable accession number and object schedule;
- receipt, acceptance, acquisition, title-passage, custody-receipt, and
  accession events as separate dated, authority-bound, evidence-backed events;
- acquisition method: donation, purchase, bequest, exchange, or transfer;
- governing approval and collecting-policy pathway;
- canonical chain identity for every token;
- source/donor reference, prior wallet, receiving wallet, consideration if any;
- `TITLE_BINDING` between the legal instrument and one specific on-chain transfer;
- title, authority, encumbrance, sanctions, contract, and provenance diligence;
- rights, conditions, restrictions, required credit line, and curatorial-independence review;
- concise accession rationale and explicit non-claims;
- preparer, technical verifier, curator, registrar, approver, dates, version, and amendments;
- final payload checksum and duplicate archival locations.

The executable `ACCESSION` record keeps these events distinct and requires an
off-chain title instrument plus an explicit custody path. A template or
Markdown completion statement cannot satisfy the accession gate.

Token ownership, legal title, copyright, display rights, and preservation rights are separate assertions.

## Individual object record minimum

### Museum and art-historical identity

- accession/object number, object name, classification, record status, curator, creator/reviewer, revision history;
- preferred artist name and authority identifiers;
- project, token title, series, date, mint/release dates, platform, edition/project size, medium;
- title, creator, creation date/range, medium/format, dimensions/duration, edition statement, and credit line compatible with `STREAM_WORK_DESCRIPTION_V1` and LIDO.

The medium describes the work, not merely its token. For example: “On-chain generative software; JavaScript; deterministic token-hash output; ERC-721 token on Ethereum.”

### Canonical chain identity

- blockchain, network, numeric chain ID, token standard;
- contract address, token ID, project/collection ID, token hash or seed where applicable;
- mint and acquisition transactions, blocks, timestamps, previous owner, custody wallet;
- last custody-verification date/block;
- CAIP-19-shaped citation and any typed record-state qualifier.

### Technical constitution

- script location/version/hash, language, dependencies and exact versions;
- generator/rendering mechanism and metadata snapshot;
- mutability and administrative controls;
- owner/artist/platform parameters;
- runtime, browser, hardware, network, audio, timing, state, and interaction requirements;
- randomness model and known rendering variance.

### Traits and description

Separate authoritative traits, derived analytical traits, and market rarity metrics. Record source, retrieval date, method, and mutability for each. Rarity is dated third-party analysis, never intrinsic identity.

Describe visual structure, palette, movement, density, space, temporal behavior, interaction, and the relationship between the live work and documentation surrogates in controlled, non-promotional language.

### Condition and integrity

Assess token, metadata, script, dependencies, rendering, behavior, and documentation separately:

- `green`: independently retrievable and verified;
- `amber`: functional but dependent on vulnerable infrastructure;
- `red`: a material component is unavailable or behavior cannot be reproduced;
- `not_assessed`: no claim has yet been made.

Condition reports must use `STREAM_CONDITION_REPORT_V1` where applicable and include reproducible protocol state, fixity coverage, render-verification method/outcome, recovery lineage, narrative, and optional hash-committed captures.

Visual documentation that does not meet the condition-report or preservation-package standard must use the local `VISUAL_OBSERVATION` profile. Record exact source URLs from retained metadata, byte fixity and size, viewport/canvas geometry, observation-completion timing semantics, commanded minimum waits, changed/unchanged outcome, and render-environment gaps. If capture bytes are not retained, say so and explain why. Never convert a post-save file timestamp into HTTP server timing, a post-hash completion time into a frame timestamp, or a minimum commanded wait into exact elapsed duration.

### Display and preservation

Record live/static/video manifestation status, aspect/orientation/resolution, hardware, light/sound/interaction, duration, restart/network behavior, fallback, credit, and interpretation. A still is a documentation surrogate unless the artist/project authorizes it as a manifestation.

The preservation package should retain metadata, project data, seed/hash, script or retrieval path, dependencies, generated output where appropriate, reference still/video, transfer evidence, interfaces, artist/project statements, display instructions, fixity, render environment/date, and risk assessment.

PREMIS object roles distinguish source capture, source/edit/print masters, display derivatives, token metadata, scripts, IIIF/C2PA manifests, archive packages, and accessibility material. Preservation does not claim a retained copy is itself the tokenized artwork.

### Provenance, rights, and curatorial record

Keep on-chain transfer history, legal-title history, and marketplace history separate. Record rights under `STREAM_RIGHTS_V1`, including basis and an explicit grant status for reproduction, publication, exhibition, print, derivative use, and AI training. Unknown rights are recorded as `unspecified`, not omitted.

The curatorial section carries significance, selection rationale, collection relationships, context, bibliography, exhibition/publication history, research notes, authorship, and dates.

## Evidence classes

Every factual claim carries evidence class A, B, C, D, or E as defined in `docs/record-model.md`, plus source, observation date, and where possible a content hash. Conflicting claims coexist with attribution until a reviewed correction supersedes one.

## Public and restricted layers

Public records include object identity, chain facts, acquisition method, agreed donor credit, public transaction evidence, provenance, curatorial context, technical description, approved imagery, and preservation/display summary.

Restricted registrar material includes private donor contacts, legal instruments, internal minutes, tax/appraisal material, security architecture, signer/hardware details, private storage locations, and sensitive risk analysis. Public payloads refer to restricted instruments by hash and non-sensitive custodian reference only.

## Completion gate

An accession is complete only when:

- the object is controlled by the designated Museum custody address;
- title documentation is executed and bound to the transfer;
- chain identity and transfer are independently verified;
- the work is viewed and condition-checked;
- metadata, code, dependencies, and mutability are assessed as applicable;
- preservation and display records exist;
- rights are explicitly documented;
- object and curatorial records are complete;
- a second person has reviewed the record.

The register reports `acquired`, `received_onchain`, `accessioned`, `catalogued`, `technically_verified`, `preservation_complete`, and `display_ready` independently.
