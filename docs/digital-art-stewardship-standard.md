# 6529 Network Museum digital art stewardship standard

Status: working standard for Museum records; not an adopted governance policy.
Version: `v1.0.0`
Date: `2026-08-04`

This standard describes the evidence, documentation, preservation, and public
publication required for software, generative, time-based, interactive,
networked, and other digital or hybrid artworks. It is derived from the
demonstrated practices cited in [§9](#9-primary-source-basis).

This standard does not claim that the Museum has adopted the requirements, that
any implementation is complete, that any package is preserved, or that any
Stream contract or mirror is deployed. It does not itself authorize an
acquisition, create an accession, prove title, or advance a lifecycle state.

## 1. Scope and governing boundaries

### 1.1 What this standard governs

Use this standard when a work depends materially on one or more of the
following:

- source code, a natural-language instruction, or a generator;
- token, seed, hash, parameter, model, prompt, or other input state;
- exact software dependencies, runtimes, browsers, operating systems, or
  graphics/audio environments;
- network services, domains, APIs, CDNs, remote assets, or live data;
- duration, animation, sound, interaction, installation, or display conditions;
- emulation, migration, virtualization, reconstruction, or reinterpretation;
- a physical/digital relationship in which the digital layer affects identity,
  display, behavior, or preservation.

The standard applies to the work, its retained components, its documented
manifestations, its preservation events, and its public technical account. It
does not turn every related file, screenshot, source URL, or derivative into
the artwork.

### 1.2 Non-collapse rule

The following are separate facts and require separate evidence:

| Fact | Meaning | Does not mean |
|---|---|---|
| Chain identity | Contract, token, network, token ID, and CAIP-19-shaped reference | Legal title, artistic identity, generation state, or preservation completeness |
| Generation state | Seed, generation hash, parameters, prompt, model state, or other inputs that determine an output | Chain identity, legal title, or a permanent claim when mutable inputs change |
| Custody | Receipt or control of an asset at an observed chain state or approved physical/digital location | Accession or title |
| Legal title | Title instrument and its binding to the relevant transfer or receipt | Copyright, display rights, or preservation rights |
| Rights | Explicit grant or restriction for reproduction, publication, exhibition, print, derivative use, preservation, migration, or AI training | Title or custody |
| Accession | Reviewed institutional act accepting a specific object through a valid pathway | Transfer, donation offer, gift authorization, or technical verification |
| Preservation | Retained, identifiable, fixity-checked, recoverable evidence and documented preservation activity | Accession, title, custody, or display readiness |
| Display readiness | A documented work-specific manifestation can be presented under stated conditions | Preservation completeness or future availability |

No status in this standard may be used to infer another fact. In particular:

- a token transfer is not accession;
- custody is not title;
- title is not copyright or a right to preserve;
- a source package is not the tokenized artwork;
- a still or video is not the live work unless the artist or project authorizes
  that manifestation;
- a successful webpage load is not preservation completion;
- an artist statement is not a technical test;
- a hash proves the bytes that were hashed, not the recovery of bytes that were
  never retained.

### 1.3 Existing Museum and Stream records remain authoritative

This standard supplements, and does not replace, the [accession
standard](accession-standard.md), [record model](record-model.md), [Stream
interoperability contract](stream-interoperability.md), and [curatorial
publication standard](curatorial-publication-standard.md).

The existing accession model remains authoritative for accession statements,
individual object records, title binding, rights, chain identity, custody,
condition, preservation, display, and lifecycle states. The existing Stream
model remains authoritative for exact envelopes, `HashRef`, record types,
schema IDs, subject derivation, record-chain commitments, and bilateral
ontology profiles.

This document uses descriptive record parts such as `WORK_IDENTITY`,
`COMPONENT`, `ARTIST_DOCUMENTATION`, `MANIFESTATION`, `TECHNICAL_EVENT`,
`PRESERVATION_PACKAGE`, `REPRODUCIBILITY_TEST`, and `SERVICE_EXIT`. These are
working document terms, not new canonical Stream schema IDs. A future schema
or on-chain record must be assigned and reviewed through the repository's
normal control plane.

For Stream-compatible records:

- use the exact Stream envelope rather than a semantically equivalent local
  envelope;
- map preservation objects, events, agents, and rights through
  `STREAM_PREMIS_V3_PROFILE`;
- map work description through `STREAM_WORK_DESCRIPTION_V1` and
  `STREAM_LIDO_PROFILE_V1` where applicable;
- map rights through `STREAM_RIGHTS_V1`;
- use the Museum's bilateral BagIt/OCFL and IIIF profiles where applicable;
- keep optional C2PA references hash-committed and validation-status-bearing;
- use the existing CAIP-19-shaped citation for chain identity;
- do not claim Stream convergence, owner-record deployment, or on-chain
  preservation merely because a local dossier is complete.

## 2. Record architecture

Every applicable technical record must identify its subject, author or
responsible agent, observation or event date, evidence references, access tier,
revision, and supersession relationship. A record may be public, restricted,
or mixed; the access tier is part of the record, not an informal storage
decision.

### 2.1 `WORK_IDENTITY`

The identity record describes the work's constitution and significant
properties. It must distinguish the following layers:

- instruction or concept;
- source code and build inputs;
- generator, script, model, or runtime;
- dependencies and external services;
- token, seed, hash, parameter, prompt, or other state;
- generated output or edition state;
- live, installed, static, video, audio, or physical manifestation;
- documentation surrogate.

At minimum, record:

- stable Museum object ID and relations to accession and object records;
- title, creator authority, creation date or range, medium, edition, and
  project/series relation;
- technical constitution in plain language;
- significant visual, sonic, temporal, interactive, spatial, networked, or
  behavioral properties;
- deterministic or nondeterministic behavior and the relevant input state;
- mutability, administrative controls, and known platform dependencies;
- artist, estate, project, or commissioning authority for identity statements;
- evidence class, source, observation date, and unresolved questions.

The identity record must not duplicate or replace chain title, custody,
`TITLE_BINDING`, rights, or accession evidence. It may point to those records
by stable ID.

### 2.2 `COMPONENT`

Create one component entry for each material element needed to understand,
render, display, preserve, or recover the work. Appropriate roles include:

- source, source capture, edit master, print master, or display derivative;
- script, generator, lockfile, package manifest, library, runtime, or browser;
- font, texture, model, prompt, seed, input, metadata, or configuration;
- generated output, reference still, video, audio, interface, or accessibility
  material;
- hardware, display, speaker, controller, network service, domain, API, CDN, or
  remote asset;
- artist statement, installation instruction, rights document, IIIF manifest,
  C2PA manifest, or archive package.

Each component entry must record, as applicable:

- component ID and role;
- relation to the work, generator, manifestation, or package;
- file name/path or external locator;
- byte size, media type, version, retrieval date, and fixity;
- hash algorithm, digest, and canonicalization or byte mode;
- source or custodian and access tier;
- license, rights basis, restriction, and permitted preservation action;
- replacement, derivation, supersession, or unavailability relation;
- for dependencies, exact version, resolution source, lockfile or integrity
  data, transitive dependency information where available, runtime
  compatibility, offline availability, and failure behavior.

Credentials, private keys, bearer tokens, secret environment variables, and
private infrastructure details must never be stored in a public component
entry. A restricted record may identify their existence and custodian without
retaining or publishing the secret.

An external URL is a locator, not custody. If the bytes are not retained, say
so, state the preservation or rights reason, and do not report the component as
recoverable merely because its URL remains live.

### 2.3 `ARTIST_DOCUMENTATION`

Artist documentation may be a questionnaire, written response, interview,
studio note, installation instruction, annotated source review, or recorded
conversation. The record must identify:

- purpose and scope of the documentation;
- participant, interviewer, recorder, and institutional roles;
- date, method, medium, and version;
- questions, responses, annotations, transcript status, and attached media;
- consent, credit, access restrictions, and permitted uses;
- statements of preferred, acceptable, and unacceptable change;
- emulation, migration, reinterpretation, repair, and failure preferences;
- display, timing, interaction, network, and dependency requirements;
- later amendment, clarification, or supersession.

Artist documentation is attributed evidence. It is not silently converted into
Museum interpretation, legal title, or a technical verification result. Where
artist instructions conflict with retained files, observed behavior, rights
instruments, or chain facts, preserve the conflict with attribution and route
the resolution through a dated review or amendment.

### 2.4 `MANIFESTATION` and `ITERATION`

Record each materially different manifestation or installation separately.
The record must state whether it is:

- live or interactive;
- static, video, audio, or other documentation surrogate;
- physical or hybrid installation;
- emulated, migrated, virtualized, repaired, reconstructed, or reinterpreted;
- a public encounter, private test, loan installation, or research capture.

At minimum, record:

- manifestation ID, work ID, date, venue or context, and responsible agents;
- component versions and package IDs used;
- hardware, operating system, runtime, browser, display, audio, network,
  viewport, timing, and interaction conditions as applicable;
- seed, token, hash, prompt, input, or state used;
- installation instructions, settings, wiring, scale, orientation, duration,
  restart behavior, and fallback;
- artist or project-author presence, review, approval, or non-response;
- deviations from the identity record or prior manifestation;
- condition observations, captures, logs, and public/restricted evidence;
- status and supersession relation.

A planned manifestation is not evidence of a completed installation. A still
is a documentation surrogate unless the artist or project authorizes it as a
manifestation. A migrated or emulated manifestation must retain its relation
to the original source and state what changed.

### 2.5 `TECHNICAL_EVENT` and intervention provenance

Record every preservation or technical intervention as an event. Appropriate
event types include:

- capture, transfer, inventory, checksum, fixity verification, and replication;
- build, dependency freeze, environment capture, and recovery test;
- migration, emulation, virtualization, repair, reconstruction, or
  reinterpretation;
- installation, replay, display, loan, condition review, retirement, or service
  transition.

Each event must record:

- event ID and event type;
- date/time semantics and responsible agent;
- input objects, output objects, and derived or superseded relations;
- method, tool, version, environment, and protocol reference;
- rationale, authority, artist consultation, and approval status where
  applicable;
- result, deviations, reversibility, and unresolved conditions;
- evidence references, fixity, and access tier.

Technical provenance must be compatible with PREMIS Objects, Events, Agents,
and Rights and may use PROV-O-style entity/activity/agent relations. It must
not rewrite legal provenance, title history, custody history, or marketplace
history. Those remain separate typed records.

### 2.6 `PRESERVATION_PACKAGE`

The preservation dossier must distinguish package purpose:

- `SIP` — package prepared for transfer or repository ingest;
- `AIP` — managed preservation package retained by the Museum;
- `DIP` — public or operational dissemination package.

An applicable package must identify:

- package ID, version, type, work/object scope, and status;
- inventory of components and documentation;
- source, metadata, script, dependencies, runtime, inputs, outputs, and
  display evidence as applicable;
- artist documentation, installation instructions, rights records, and
  condition reports;
- fixity manifests, hash algorithms, canonicalization, and byte mode;
- transfer, storage, replica, recovery, and supersession events;
- responsible agents, access tiers, and restrictions;
- public derivative and accessibility material where rights permit;
- risk assessment, unresolved conditions, and next review date.

BagIt may package transfer and ingest. OCFL may provide versioned object
storage. They do not replace the Museum's object, event, agent, rights, or
curatorial records. SHA-256 and Keccak-256 may coexist; each digest must state
what bytes or canonical payload it covers. Museum-authored text normalized for
release tooling and raw-byte evidence snapshots are different fixity domains
and must not be silently interchanged.

For `complete` package status, the required preservation scope must be fully
inventoried, fixity-checked, and recoverable from at least two independently
recoverable copies, with a documented restore test. A second pointer to the
same storage object is not an independent replica. If rights, infrastructure,
or material evidence prevents that result, use `complete_with_conditions` or
`blocked` and state the condition.

Preservation of a package does not claim that the package is the tokenized
artwork. It preserves evidence and the means to understand, render, display,
or recover the work within the stated scope.

### 2.7 `REPRODUCIBILITY_TEST`

A reproducibility test must declare its scope. Possible scopes are:

- source retrieval and integrity;
- dependency resolution and build;
- deterministic output;
- visual, sonic, temporal, or interactive behavior;
- installation or display;
- recovery from a replica or archive package.

Record:

- protocol ID, version, repository commit, or exact procedure;
- test date, operator, reviewer, and declared outcome;
- hardware, operating system, browser, runtime, GPU, display, audio, network,
  viewport, timezone, and timing conditions as applicable;
- source and dependency versions, lockfile or integrity data, and package IDs;
- token, seed, hash, prompt, input, data snapshot, and configuration;
- expected behavior and observed behavior;
- replay count, independent environments, screenshots/video/logs, and fixity;
- variance, failure, blocked dependency, and next action.

Use `passed`, `passed_with_variance`, `failed`, `not_run`, or `blocked` for the
test outcome. Unknown frame times, browser versions, user agents, or elapsed
durations remain unknown. A commanded minimum wait is not an exact elapsed
duration; a local file timestamp is not an HTTP server timestamp.

Reproducibility is always bounded by the declared protocol. Passing one
render test does not prove future platform availability, artist intent, title,
rights, or preservation completeness.

### 2.8 `SERVICE_EXIT`

For any work dependent on a third-party host, domain, CDN, API, account,
commercial runtime, or remote data source, record:

- service, owner, domain, endpoint, account or custodian reference, and role;
- terms, license, access requirement, and known change or closure risk;
- capture or export format, date, scope, and fixity;
- static, self-hosted, emulated, or alternative runtime path;
- dependencies and instructions needed to operate the exit path;
- last successful test and responsible agent;
- planned, captured, validated, superseded, or blocked status;
- public and restricted evidence.

Service exit is not a promise that the work can always be restored. It is a
record of what the Museum captured, what it can operate, what it cannot
operate, and which conditions remain external.

## 3. Public and restricted views

### 3.1 Public view

The public record should expose, where rights permit:

- work identity and chain reference;
- technical constitution in understandable language;
- manifestation and iteration summaries;
- public preservation and condition status;
- intervention and technical-provenance summaries;
- fixity reference, package version, observation date, and limitations;
- artist documentation summary and authority attribution;
- rights summary, credit, approved imagery, and access conditions;
- source links, bibliography, correction history, and unresolved questions.

The public record must state when a component is not retained, a capture is
partial, a service is external, an artist response is unavailable, or a test
has not been run. It must not present a live interface, screenshot, or
platform page as stronger evidence than the retained record supports.

### 3.2 Restricted view

Restricted records may contain:

- source bytes and unpublished technical material;
- private legal instruments and donor or artist contact details;
- non-secret storage references, named custodians, access basis, and retention
  decisions;
- restricted interviews, personal data, appraisal material, or rights analysis;
- vulnerability findings whose handling and disclosure are separately
  authorized.

Credentials, private keys, signing material, tokens, recovery phrases, and
other secret values must never be retained in Museum records. When operational
access must be evidenced, record only a non-secret credential-store reference,
custodian, access basis, fingerprint where safe, retention decision, and
review date.

Public records may point to restricted material using a content hash and
non-sensitive custodian reference. Restricted status does not remove the
requirement to identify the evidence, responsible agent, date, access basis,
and retention decision.

Source-code custody does not require public source release. The Museum must,
however, record whether it has preservation access, whether it may modify or
execute the source, and which rights or restrictions govern those acts.

## 4. Status language

### 4.1 Component and condition status

Use the existing technical condition vocabulary:

- `not_assessed` — no claim has been made or the required test has not run;
- `green` — the declared component is retrievable, integrity-checked, and
  verified within the stated protocol;
- `amber` — functional or partially verified under stated conditions, but
  dependent on vulnerable infrastructure, incomplete evidence, or unresolved
  variance;
- `red` — a material component is unavailable, corrupt, or cannot be rendered,
  displayed, or behaviorally reproduced within the declared scope.

`green` is not permanent availability. It is a bounded observation.

### 4.2 Package status

Use the preservation dossier vocabulary:

- `not_started`;
- `in_progress`;
- `complete_with_conditions`;
- `complete`;
- `blocked`.

`complete` requires the declared package scope, component inventory, fixity,
replicas, recovery test, documentation, and access decision to be complete.
Material exceptions require `complete_with_conditions` or `blocked`.

### 4.3 Manifestation status

Use:

- `planned` — proposed, not observed;
- `observed` — occurred and has evidence;
- `superseded` — replaced by a later manifestation record;
- `cancelled` — planned but not completed, with reason;
- `blocked` — intended but prevented by a named dependency or authority issue.

The words “installed,” “replayed,” “migrated,” “emulated,” and “preserved” are
claims requiring a dated event and evidence. “Preservation complete” must not
mean “the webpage loads,” “a still exists,” “the token is in custody,” or “a
hash was recorded.”

### 4.4 Accession lifecycle

The accession lifecycle remains independent:

`acquired` → `received_onchain` → `accessioned` → `catalogued` →
`technically_verified` → `preservation_complete` → `display_ready`

The applicable states may be recorded independently. This stewardship
standard cannot move an object between them. In particular, a complete
technical dossier cannot establish title or accession, and an accession cannot
be described as preservation-complete while material preservation requirements
remain unresolved.

## 5. Technical publication requirements

Every public technical note should begin with the exact work and the
consequential preservation or display problem. It should state:

1. what the work did or required before intervention;
2. which component, dependency, behavior, or access path was at risk;
3. what evidence was examined;
4. which intervention or preservation decision was made;
5. who authorized and performed it;
6. what changed and what remained unchanged;
7. what remains unresolved;
8. how the public encounter is affected.

Separate artist statement, technical observation, institutional decision,
conservation interpretation, and curatorial interpretation. Do not use
generic claims about “digital art,” promotional superlatives, or a still as a
substitute for close description of behavior over time.

Each publication must include version, publication date, research cutoff,
authorship, direct primary-source citations, supporting technical-record links,
known limitations, and a correction or supersession path.

## 6. Review gates

Before a work is marked `technically_verified`, its reviewed record set must
contain:

- a completed or explicitly limited identity record;
- a component and dependency inventory;
- chain identity and title/custody/rights records kept separate;
- at least one declared reproducibility or condition protocol;
- documented unresolved conditions and access restrictions;
- a second-person review.

Before `preservation_complete`, its reviewed record set must contain:

- an applicable SIP/AIP/DIP package record;
- retained components within the declared preservation scope;
- fixity manifests with byte mode and canonicalization;
- at least two independently recoverable copies;
- a successful restore or recovery test;
- intervention and technical-provenance events;
- artist documentation or an explicit unavailable/declined record;
- service-exit assessment where external infrastructure is material;
- public and restricted views;
- a second-person review and dated next-review condition.

If a requirement for `technically_verified` is unmet, the accession lifecycle
must not advance to that state. If a requirement for `preservation_complete`
is unmet, the preservation package must remain `complete_with_conditions` or
`blocked`, and the lifecycle must not advance to `preservation_complete`.

Before `display_ready`, its reviewed record set must contain a documented
manifestation, display environment, rights basis, condition outcome,
restart/fallback plan, credit, and approved public encounter. Display readiness
remains separate from preservation completeness.

## 7. Corrections and supersession

Corrections are append-only. A correction or new technical finding must:

- identify the superseded record or assertion;
- state what changed and why;
- preserve the earlier record and its hash;
- identify authority, date, evidence, and access tier;
- update the current-view index without erasing history.

Conflicting dates, artist instructions, source versions, service states, and
reconstruction accounts must coexist with attribution until a reviewed
amendment resolves or narrows the conflict.

## 8. Implementation boundary

This standard is a documentation and evidence contract. It does not create
schemas, validators, contracts, storage replicas, Stream deployments, rights
instruments, or accession authority by itself.

When implementation begins, the Museum should first map these record parts to
closed JSON Schemas, controlled vocabularies, evidence-manifest rules,
cross-file references, and release-manifest inventory. Any new Stream-facing
schema must be proven byte-compatible with the published bilateral profile or
explicitly kept Museum-local until Stream publishes the canonical schema.

## 9. Primary source basis

The following official sources supplied the demonstrated practices behind this
standard. Dates are publication, record, or programme dates when displayed;
“date not shown” means the official page did not display one. All were accessed
2026-08-04.

- [Guggenheim, “The Conserving Computer-Based Art Initiative”](https://www.guggenheim.org/conservation/the-conserving-computer-based-art-initiative), date not shown; [“Conservation Department Iteration Report”](https://www.guggenheim.org/wp-content/uploads/2015/11/guggenheim-conservation-iteration-report-2012.pdf), 2012; [“Brandon: credits and restoration”](https://brandon.guggenheim.org/credits/), restoration project 2016–2017. These establish identity/iteration separation, source analysis, disk imaging, code annotation, version control, artist consultation, and treatment reporting.
- [Tate, “Intermedia Art Microsite”](https://archive.tate.org.uk/Record.aspx?id=TG+100%2F1%2F9&src=CalmView.Catalog), record 2008–2012 with archive capture November 2019–February 2020; [“Net Art Commissions”](https://archive.tate.org.uk/Record.aspx?id=TG+100%2F1&src=CalmView.Catalog), record 1999–2021; [“Reshaping the Collectible”](https://www.tate.org.uk/research/reshaping-the-collectible), programme 2018–2022. These establish recovery, capture scope, explicit loss, and changing net-art records.
- [Rhizome, “About ArtBase”](https://artbase.rhizome.org/wiki/About), date not shown; [“My Boyfriend Came Back From the War”](https://artbase.rhizome.org/wiki/Q3933), date not shown; [“The Making of Net Art Anthology”](https://old.rhizome.org/editorial/2019/jan/28/the-making-of-net-art-anthology-rhizome-and-google-arts-culture/), 2019; [Conifer “Twilight Webinar”](https://blog.conifer.rhizome.org/2026/05/06/twilight-webinar.html), 2026-05-06; [“Webinar Recap”](https://blog.conifer.rhizome.org/2026/05/22/webinar-recap.html), 2026-05-22. These establish variant records, preservation matrices, browser/archive conditions, and service-exit documentation.
- [LI-MA, “Documentation”](https://li-ma.nl/article/documentation), date not
  shown; [“What Are the Basics of Preserving Digital
  Art?”](https://li-ma.nl/article/preservation-introduction/), date not shown;
  [“Artwork Documentation
  Tool”](https://li-ma.nl/article/artwork-documentation-tool/), date not shown;
  [“Storing Digital and Analogue Art
  Safely”](https://li-ma.nl/article/storage/), date not shown. These establish
  artist-first documentation, versions and iterations, dependency inventories,
  storage monitoring, virtual servers, and LTO.
- [Smithsonian, “Time-based Media & Digital Art”](https://tbma.si.edu/), date not shown; [“Forms and Documentation”](https://tbma.si.edu/forms-and-documentation), date not shown; [“Iteration Report”](https://tbma.si.edu/resource/iteration-report), date not shown; [“Digital Preservation”](https://tbma.si.edu/resources/forms-documentation), date not shown; [“Handling Digital Assets in Time-Based Media Art”](https://siarchives.si.edu/blog/handling-digital-assets-time-based-media-art), 2014. These establish adaptable work-specific forms, installation-level reports, DAMS resources, and granular digital-preservation policy.
- [Matters in Media Art, “Matters in Media Art”](https://www.moma.org/research/conservation/matters-in-media-art), project milestones 2003, 2004, and 2007; [“Acquiring Media Art”](https://mattersinmediaart.org/acquiring-time-based-media-art.html), © 2015; [“Lending Media Art”](https://mattersinmediaart.org/lending-time-based-media.html), © 2015; [“Documenting Media Art”](https://mattersinmediaart.org/assessing-time-based-media-art.html), date not shown. These establish acquisition, loan, installation, artist-interview, condition, and documentation workflows.
- [Variable Media Network, “Variable Media Network”](https://www.variablemedia.net/e/welcome.html), date not shown; [“Variable Media Publication: Permanence Through Change”](https://www.variablemedia.net/e/preserving/html/var_pub_index.html), date not shown. These establish behavior, environment, interaction, significant-property, storage, emulation, migration, and reinterpretation vocabulary.
- [INCCA, “INCCA Guide to Good Practice Artists Interviews”](https://incca.org/incca-guide-good-practice-artists-interviews-2002), guide 2002, page posted 2008; [PDF](https://incca.org/sites/default/files/field_attachments/2002_incca_guide_to_good_practice_artists_interviews.pdf/2002_incca_guide_to_good_practice_artists_interviews.pdf); [“Artists Documentation Program”](https://incca.org/project-artists-documentation-program-adp), page posted 2012. These establish interview purpose, consent, outputs, annotations, access, and artist/conservator documentation.
- [ZKM, “Wipe Cycle”](https://zkm.de/de/werk/wipe-cycle), date not shown; [“Restoration of Electronic and Digital Art”](https://zkm.de/en/restoration-of-electronic-and-digital-art), date not shown. These establish technical constitution, reconstruction, equipment, software, and interdisciplinary restoration documentation.
- [MoMA, “Preserving the Technical History of Media Works”](https://www.moma.org/explore/inside_out/2015/05/20/preserving-the-technical-history-of-media-works/), 2015-05-20. This establishes structured process history for device models, serial numbers, settings, and migration.
- [Library of Congress, “PREMIS”](https://www.loc.gov/standards/premis/index.html) and [“PREMIS Data Dictionary for Preservation Metadata: Version 3.0”](https://www.loc.gov/standards/premis/v3/premis-3-0-final.pdf). These establish preservation Objects, Events, Agents, and Rights.
- [OCFL Specifications](https://ocfl.io/), specification series 1.1; the
  [OCFL release notes](https://ocfl.io/news/) identify 1.1.1 as the current
  patch at the research cutoff. Any implementation must pin the exact 1.1.x
  text it claims to follow. This establishes transparent, versioned,
  software-independent object storage.
- [RFC 8493, “The BagIt File Packaging Format”](https://www.rfc-editor.org/info/rfc8493/), 2018-10. This establishes package transfer and manifest fixity.
- [IIIF, “Presentation API 3.0”](https://iiif.io/api/presentation/3.0/), version 3.0.0. This establishes public presentation, manifest, temporal, and spatial structures.
- [W3C, “PROV-O: The PROV Ontology”](https://www.w3.org/TR/prov-o/), Recommendation 2013-04-30. This establishes entity, activity, agent, derivation, and association vocabulary.
- [C2PA, “Content Credentials: C2PA Technical Specification”](https://spec.c2pa.org/specifications/specifications/2.4/specs/C2PA_Specification.html), version 2.4. This establishes optional cryptographic provenance for media derivatives, not title, accession, or preservation proof.

## 10. Review status

This is `v1.0.0`, dated `2026-08-04`, and remains a working standard pending
repository review, schema mapping, validation implementation, and any future
governance adoption. Its existence must not be reported as completed
implementation or policy adoption.
