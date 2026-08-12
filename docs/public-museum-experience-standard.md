# 6529 Network Museum public experience and frontend rebuild standard

**Status:** replacement product specification and implementation standard

**Applies to:** the public 6529 Network Museum experience on `6529.io`, its GitHub-to-web publication adapter, and the public presentation records required to support it

**Current canonical route:** `https://6529.io/museum/network`

**Initial reference accession:** `6529NM.2026.001`, the seven-work Casey Reas gift

**Initial reference program:** `6529NM-AP-01`, Keys and Gates

## 1. Purpose

The present Museum frontend is a technically functioning registry browser. It is not an acceptable public museum experience. It proves that files can move from a governed GitHub release into web routes, but it does not give visitors a meaningful encounter with the art, the artists, or the Museum's curatorial work.

This document replaces that product model. It defines what must be designed, written, modeled, built, and verified before the 6529 Network Museum frontend can be described as a serious museum website.

The standard is intentionally art-first. Integrity, provenance, chain evidence, and reproducibility remain essential, but they support the encounter with the work. They must not displace it.

The experience hierarchy is:

1. **See or experience the artwork.**
2. **Understand the work and the artist.**
3. **Explore relationships across the collection.**
4. **Understand acquisition, provenance, rights, and technical constitution.**
5. **Inspect the underlying institutional and machine evidence.**

Any design that reverses this hierarchy is non-conforming.

## 2. What failed in the current release

The failure was not primarily styling. It was a product-definition failure.

The release was accepted against machine criteria: the manifest loaded, routes returned HTTP 200, seven Casey object records resolved, sixteen Keys and Gates outcomes resolved, status values were correct, and the source commitment was visible. Those are necessary infrastructure checks. They are not museum acceptance criteria.

The current implementation has the following material defects:

| Current behavior | Why it fails | Required replacement |
|---|---|---|
| The home page foregrounds record counts, source status, and generic section cards. | It opens as a control-plane dashboard, not a museum. | Open with a curatorially chosen artwork or exhibition-scale visual encounter, a concise mission, and immediate paths into art. |
| Collection cards and object pages contain no artwork imagery. | A visitor cannot see what the Museum holds or selected. | Every publicly presented artwork must have an approved visual or time-based representation, with a documented fallback when the live work is unavailable. |
| The object page foregrounds status badges, classification, scope, and raw JSON. | Internal record fields displace the work and interpretation. | Lead with the work; place catalog facts beside or below it; place evidence in a subordinate, legible record layer. |
| The Casey accession page shows donor, custody, transaction, limits, and object links but not the accession dossier. | The substantial human-readable scholarship already in the repository is invisible. | Publish the gift story, accession rationale, artist profile, collection essay, object entries, rights, technical review, and provenance as a coherent dossier. |
| `records/accessions/**/public/*.md` files are fetched but not normalized into routable documents. | The adapter has the content but discards its public meaning. | Add typed public-document indexing, routing, cross-linking, and page placement. |
| `MuseumObjectRecord` has no media model. | The frontend has no typed way to render a still, video, audio work, live generator, detail, caption, or credit. | Add a validated presentation projection backed by canonical media and IIIF records. |
| `MuseumMarkdown` replaces every Markdown image with “Media omitted from the record view.” | The renderer deliberately removes visual evidence and editorial imagery. | Render only approved, typed Museum media through secure components; never suppress approved media globally. |
| The source adapter allowlists only Markdown and JSON. | No image, video, audio, IIIF asset, or retained documentation byte can reach the frontend through the release. | Publish a content-addressed media inventory and media resolver contract in addition to the textual corpus. |
| The Casey records contain Art Blocks image and generator URLs, but the frontend does not promote or use them. | Available work-level presentation data remains buried in evidence. | Promote approved presentation resources into a canonical publication profile and render them. |
| No image or video bytes are tracked in the Museum repository. | The Museum depends on upstream availability and cannot present a retained documentation surrogate. | Retain rights-cleared Casey stills and required derivatives now; bind every byte to fixity, rights, credit, and source. |
| Approved donation categories appear as “Collections.” | Policy eligibility is confused with actual Museum holdings. | Move preapproved donation categories under “Collecting and donations.” Reserve “Collection” for accessioned objects. |
| Keys and Gates appears through status-heavy text cards. | A visual selection program is represented without its selected art. | Present the sixteen selections as an illustrated program while clearly stating that they are selected and unminted, not accessioned holdings. |
| Governance and methodology are top-level visitor concepts. | Institutional process overwhelms art and interpretation. | Keep mission, decisions, policy, methods, and source evidence in a clear but subordinate “About / How the Museum works” layer. |
| Raw JSON is the principal depth interaction. | Machine legibility is mistaken for human transparency. | Render provenance, rights, custody, condition, and source history as designed human-readable views; offer canonical JSON as an expert download. |
| Route and DOM checks were used as release sign-off. | A page can be technically live while visually empty and curatorially unusable. | Require captured visual QA, media playback, content-completeness checks, accessibility checks, and curatorial acceptance on real pages. |

The audited production implementation is represented by the Museum modules in `6529seize-frontend`, including `lib/museum/source.ts`, `lib/museum/normalize.ts`, `lib/museum/types.ts`, `components/museum/MuseumMarkdown.tsx`, and `app/museum/network/**`. The replacement must remove the failed assumptions, not merely restyle those components.

## 3. Product principles

### 3.1 Art before apparatus

The work is the primary content. On an artwork page, its visual, interactive, sonic, or time-based manifestation must dominate the initial viewport whenever rights and technology permit. Museum infrastructure must remain available without competing with the art.

### 3.2 Scholarship without intimidation

Every serious object deserves layered interpretation:

- a concise label for a first encounter;
- a substantive object text;
- an artist and practice profile;
- collection, project, or series context;
- acquisition and provenance history;
- technical and preservation context for those who want it;
- citations and source evidence.

Visitors should not need to understand accession vocabulary, smart-contract architecture, JSON, CAIP identifiers, or GitHub to learn from the Museum.

### 3.3 Chain-native, not chain-dominated

The Museum should do things conventional museum sites cannot: verify token identity, distinguish token title from copyright, expose custody and finality evidence, identify executable dependencies, publish content commitments, and let a visitor audit the record. These capabilities should be elegantly integrated as evidence, not used as the visual language of every page.

### 3.4 Live works are works, not thumbnails

A generative artwork is not adequately represented by a marketplace thumbnail. The site must support the live, token-specific behavior where safe and authorized, while also preserving and labeling a Museum-held reference still or video. A still must never be presented as if it were the complete live work.

### 3.5 Editorial judgment over automated filler

The homepage, collection pathways, related works, essays, captions, and display order require curatorial choices. They must not be populated by arbitrary record order, token price, marketplace popularity, OpenSea rarity, or generic generated prose.

### 3.6 Transparency through comprehension

Transparency means that a visitor can understand what the Museum knows, why it believes it, what remains uncertain, and where the evidence comes from. A JSON dump alone is not transparency.

### 3.7 A public institution, not a crypto dashboard

The visual system must avoid the default vocabulary of Web3 administration: metric tiles, badge clusters, terminal-like metadata, indiscriminate monospace, generic glowing cards, and governance-first navigation. Chain information should be precise and calm. The overall experience should feel like an institution built around art.

## 4. Audience and visitor outcomes

The site must serve at least five audiences without forcing them into one interface:

| Audience | Primary outcome |
|---|---|
| First-time visitor | Encounter compelling art immediately and understand what the 6529 Network Museum is. |
| Art-informed visitor | Read serious interpretation, learn about artists and projects, and follow meaningful relationships among works. |
| Artist, donor, or community participant | Understand how work entered or may enter the Museum, how it is credited, and how the Museum cares for it. |
| Researcher, registrar, conservator, or technologist | Inspect catalog, provenance, rights, technical, preservation, and source records with durable citations. |
| Chain auditor or developer | Verify token identity, transactions, custody observations, release commitments, and future on-chain record bindings. |

The default interface serves the first two audiences. The deeper record layers serve the remaining audiences without contaminating the first encounter.

## 5. Information architecture

### 5.1 Primary navigation

The primary Museum navigation should be the following five labels:

- **Collection**
- **Artists**
- **Acquisitions**
- **Research**
- **About**

The Museum home remains the institutional front door at `/museum/network`; it is not a sixth peer label. `AGENT`, `ACCESSION`, and `MEDIA_REFERENCE` records are relational-only and do not receive visitor navigation. Exhibition is reserved vocabulary only in this release: no Exhibition instance, placeholder, or page is published.

“Governance,” “Methodology,” “Accessions,” and “Approved Collections” must not be first-order visitor navigation labels.

### 5.2 Institutional navigation

The About area should contain:

- Mission and founding principles
- How the Museum collects
- Gifts and acquisitions
- Donation eligibility and preapproved collection scopes
- Decisions and governance history
- Collection care and digital preservation
- Data, standards, and open source
- Contact and feedback

This preserves radical transparency without making administrative structure the Museum's public face.

### 5.3 Meaning of “Collection”

“Collection” means accessioned Museum objects. It does not mean:

- collections whose tokens are eligible for donation;
- selected but unminted program outcomes;
- proposals;
- wallet holdings that have not been accessioned;
- evidence records or policies.

The site must preserve these distinctions in routing, labels, search results, and counts.

### 5.4 Required route model

The following canonical routes and identity rules are normative:

```text
/museum/network
/museum/network/collection
/museum/network/artists
/museum/network/artists/[artist-slug]
/museum/network/organizations/[organization-slug]
/museum/network/projects/[project-slug]
/museum/network/works/[workId]
/museum/network/acquisitions/[acquisition-slug]
/museum/network/acquisition-programs/[program-slug]
/museum/network/research/[research-slug]
/museum/network/about
/museum/network/about/collecting
/museum/network/about/decisions
/museum/network/about/standards
```

`[workId]` is the stored, acquisition-independent canonical Work ID `6529NM-W-####`; Casey accession IDs, Keys and Gates `OUT-*` outcome IDs, and Magnum proposal `OBJ-*` IDs are typed aliases and permanent redirects only. Acquisition Programs use stored visitor slugs such as `keys-and-gates`; `6529NM-AP-ENT-####` is the canonical entity ID and `6529NM-AP-01` is a source alias. Existing `/programs`, `/stories`, `/gifts`, `/collection/[object-id]`, and source-ID routes receive permanent redirects or compatible aliases. Stable source identifiers remain visible and citeable in provenance records without becoming visitor URLs.

## 6. Visual and editorial direction

### 6.1 The visual system

The Museum must be visibly and behaviorally native to `6529.io`. A visitor moving from Waves, the Meme Lab, or another established 6529 surface into the Museum must remain inside the same institution and product. The Museum needs an art-direction layer within that system, not a replacement design system and not a reuse of generic application cards.

The frontend repository is the source of truth for the 6529 visual language. Before designing Museum-specific components, implementation must inventory and reuse the actual production tokens and primitives for:

- font families, weights, type scale, line height, and text color;
- global navigation and sidebar structure;
- page containers, columns, grids, spacing, and breakpoints;
- background, foreground, border, divider, accent, and semantic colors in every supported theme;
- links, buttons, inputs, focus rings, selection states, and keyboard behavior;
- radii, borders, shadows, and image framing;
- loading, empty, stale, unavailable, and error states;
- animation durations, easing, reduced-motion behavior, and route transitions;
- desktop, tablet, and mobile navigation conventions.

Museum extensions may change composition, image scale, editorial pacing, and the relationship between artwork and text. They may introduce only the new primitives genuinely required for viewing art, such as a media stage, object caption, long-form reading measure, IIIF viewer, live-work controls, and provenance drawer. Those extensions must be expressed through existing 6529 tokens wherever possible and documented when a new token is unavoidable.

The following visual shortcuts are prohibited because they produce a detached, generic, or recognizably machine-generated interface:

- an imported standalone “museum” theme;
- oversized editorial serif type when it is not part of 6529's established type system;
- repeated rounded cards, pills, status badges, or boxed sections as the default composition;
- glassmorphism, arbitrary gradients, glow effects, soft shadows, and decorative blur without a site-native precedent;
- generic black-and-white “luxury institution” styling that erases 6529's identity;
- dashboard grids, metric tiles, process timelines, and schema diagrams on visitor-first routes;
- invented color, radius, spacing, icon, or motion systems that duplicate existing site tokens;
- placeholder image treatments or AI-generated decorative art used to simulate a collection.

This is not a request to make every Museum page look like an existing social feed. It is a requirement to build from the same visual grammar. Differentiation comes from the art, curation, scale, sequence, and controlled Museum-specific layouts.

Required characteristics:

- generous space around artworks;
- artwork-led color and composition rather than one inflexible dashboard skin;
- typography suitable for long-form reading and precise catalog labels;
- restrained institutional identity;
- deliberate transitions between looking, reading, and inspecting evidence;
- full-bleed and large-format media where appropriate;
- no default cropping of artworks;
- consistent captions, credit lines, and rights notices;
- desktop, tablet, and mobile compositions designed independently, not merely collapsed;
- dark and light presentation modes when required by a work or exhibition, with accessible contrast in both.

The site should feel quiet when the work needs quiet and dynamic when the work is dynamic. It should not impose one animated “Web3” aesthetic on every artist.

### 6.1.1 6529 visual-fidelity evidence

Visual-system conformity is a release artifact, not an aesthetic assertion. The implementation PR must contain a matrix identifying:

| Evidence | Required content |
|---|---|
| Existing 6529 source | Exact token, theme, layout, navigation, and shared-component files audited |
| Reused foundations | Existing primitives used by each Museum route and component |
| Museum extensions | Each new primitive or token, its purpose, and why no existing primitive suffices |
| Rejected patterns | Generic card, badge, gradient, serif, dashboard, or microsite patterns explicitly avoided or removed |
| Visual comparison | Side-by-side desktop and mobile captures of representative established 6529 pages and Museum pages |
| Computed verification | Representative computed font, color, spacing, radius, focus, and breakpoint values showing token use rather than visual approximation |

The comparison is not a demand for pixel identity between unrelated page types. It must demonstrate common authorship: stable global chrome, typography, interaction language, rhythm, color logic, responsive behavior, and accessibility treatment. A page that could plausibly be detached from `6529.io` and sold as a generic museum template fails this standard.

### 6.2 Type hierarchy

At minimum, the design system must distinguish:

- display title;
- artist name and life/practice line;
- object title and date;
- curatorial standfirst;
- body essay;
- catalog label;
- caption and credit line;
- provenance event;
- technical annotation;
- source citation;
- identifier and machine field.

Monospace is appropriate for hashes, addresses, token identifiers, and code—not for normal curatorial or institutional prose.

### 6.3 Editorial voice

The public voice should be direct, informed, and specific. Avoid:

- unexplained internal statuses such as `selected_unminted`;
- generalized claims of importance without evidence;
- repeated caveats before a visitor has encountered the work;
- process prose about who might review content later;
- generic statements that could describe any generative-art project;
- promotional price, floor, or rarity language.

Uncertainty should be stated where it matters, in natural language, close to the affected claim.

### 6.4 Curatorial writing is a primary Museum product

The frontend cannot become world-class by placing weak summaries beside good images. Artist profiles, collection overviews, project histories, and object entries must themselves meet publication standards.

The current Casey “artist and practice profile” is an accession research summary, not a sufficient Museum profile. It is organized as a sequence of sourced practice phases and evidence qualifications. It does not sustain an art-historical thesis, give enough intellectual biography, develop the artist's changing relation to drawing, instruction, photography, cinema, machine learning, software, networks, and institutions, or closely read enough works. The current collection essay is likewise too compressed and allows capture/preservation qualification to overtake interpretation. Both are useful research inputs; neither should be treated as the final public scholarship.

A Museum-caliber artist profile or monograph must include:

- a clear and contestable curatorial thesis;
- intellectual and artistic biography, not only education and employment;
- art-historical genealogy, including affinities and differences rather than name-dropping predecessors;
- a chronological account of every material phase relevant to the artist's mature practice;
- specific close readings of representative works;
- the evolution of media, tools, production methods, and display conditions;
- the artist's role as teacher, author, tool-builder, organizer, or institution-builder where this changes the work's meaning;
- exhibition, collection, publication, and critical reception history;
- a serious account of recent work, not a career narrative that stops at the Museum's tokens;
- the Museum's own collection in the context of the larger practice;
- preservation and display implications as one critical dimension, not the controlling subject;
- endnotes or footnotes grounded primarily in artist, gallery, museum, publisher, archive, and project sources;
- a bibliography and a dated research boundary.

The writing must synthesize sources into an argument. It must not read as one paragraph per URL, one caveat per claim, or a compliance memo. Evidence-class distinctions belong in citations and the record layer; they should appear in the essay body only when they materially affect interpretation.

### 6.5 Required editorial depth

The following are minimum commissioning targets, not automatic word quotas:

| Publication type | Expected depth |
|---|---|
| Major artist monograph/profile | Approximately 12,000–20,000 words where the practice warrants it; thesis, chronology, genealogy, close readings, reception, current work, sources, and bibliography |
| Project or series essay | Approximately 3,000–6,000 words; genesis, formal system, technical constitution, exhibition/distribution history, close readings, and relation to the larger practice |
| Collection or accession essay | Approximately 5,000–8,000 words; why these works belong together, why they matter, what the group does and does not represent, and object-specific analysis |
| Artwork entry | Approximately 800–1,500 words for a significant born-digital work, plus a concise 100–200 word label |
| Acquisition/gift narrative | Approximately 1,500–3,500 words, distinct from the legal and registrar record |
| Technical or conservation feature | As long as required to explain behavior, dependencies, display, condition, and preservation without pretending to be the curatorial essay |

Length does not create quality. The acceptance question is whether the text offers a knowledgeable reader an argument and a first-time reader a way into the work. Unsupported grand claims, repetitive biography, generic computational-art language, and technical padding all fail regardless of word count.

For the initial Casey publication, a quickly generated 8,576-word survey is evidence of the minimum readily attainable scope, not the Museum's target. Every layer—the artist monograph, each represented project, the seven-work collection, the donation, and each individual object—must materially exceed that baseline in research depth, argument, close looking, sourcing, and editorial finish.

## 7. Page specifications

### 7.1 Museum home

The Museum home is a curated front door, not an index of database domains.

Required modules, in this order unless an exhibition-specific art direction justifies another sequence:

1. **Primary art encounter:** a large approved still, video, or lightweight live presentation from an accessioned work or current program. It includes title, artist, date, and one clear action to enter the work.
2. **Mission in one breath:** no more than approximately 60 words, with a link to the full institutional statement.
3. **Featured collection story:** initially the Casey Reas gift, showing the seven works as art and explaining why the gift matters.
4. **Current acquisition:** Keys and Gates is explicitly described as **Selected through an acquisition program; acquisition pending**, with the qualifier **Not yet minted; minting route under consideration.** Conflict at Its Edges is shown as **Selected by Museum Wave—accession processing in progress**. Its published scholarship, object records, diligence, and media presentation are accession work in progress; they do not imply completion of any title, custody, rights, technical, accession-certificate, or Collection gate that remains unrecorded.
5. **Explore the collection:** visually rich entry points by artist, project, medium, date, and curatorial theme.
6. **Research and essays:** Research Publications, artist profiles, technical conservation features, and acquisition stories.
7. **Institutional footer:** collecting, donations, decisions, standards, repository, release commitment, accessibility, and contact.

The home page must not lead with record totals, manifest health, policy cards, or governance decisions. A discreet source-health notice may appear only when the content is stale or incomplete.

### 7.2 Collection index

The collection index presents accessioned objects with media-first cards.

Each card must include:

- an approved image or poster frame;
- title;
- artist;
- date or date range;
- project or collection, when meaningful;
- media/format summary;
- accessible alt text;
- no price, marketplace rank, or rarity score.

Required discovery controls:

- search by artist, title, project, accession number, contract, or token ID;
- filter by artist, project/series, date, classification, media behavior, and public display availability;
- sort by curatorially featured, recently accessioned, artist, or date;
- a deliberate “Surprise me” or random-discovery path;
- list and visual-grid modes;
- URL-addressable filter state;
- clear result counts and empty states.

The default ordering must be curatorially chosen or clearly labeled, not repository order.

### 7.3 Artwork page

The artwork page is the center of the Museum.

Above the fold:

- the artwork's primary presentation occupying the majority of the available visual area;
- artist, title, date, and project/series;
- a concise media statement;
- fullscreen or focused viewing control;
- still/live/video choice when more than one manifestation is available;
- clear loading, unavailable, and reduced-motion states.

Immediately following:

- a 100–200 word Museum label written for this specific work;
- an artist-authored statement or project statement when available, clearly attributed;
- links to the artist and project pages;
- previous and next works within the current curatorial context.

Catalog layer:

- accession number;
- creator attribution;
- title and date;
- medium and technical constitution;
- dimensions or native aspect ratio where applicable;
- project, platform, and edition context;
- chain, contract, standard, and token identifier;
- acquisition method and date;
- donor credit line;
- rights and permitted-use summary;
- current display manifestation and preservation status, expressed in plain language.

Interpretive and evidentiary layers:

- detailed object entry;
- project or collection essay;
- provenance and title timeline;
- technical behavior and display notes;
- condition and preservation summary;
- rights and credit;
- citations;
- canonical JSON, IIIF manifest, and source package downloads.

Raw JSON must be a final expert option, never the principal content after the title.

### 7.4 Live generative artwork viewer

The viewer must distinguish three manifestations:

1. **Live token-specific presentation:** the approved executable generator or preserved runtime.
2. **Museum documentation:** a retained still or video captured under a documented environment and date.
3. **Fallback representation:** an approved upstream or cached poster used when the first two cannot load.

Required behavior:

- show an approved still first so that art appears at first paint;
- load executable content only after explicit visitor activation unless a reviewed work-specific exception permits otherwise;
- preserve the native aspect ratio and avoid decorative cropping;
- provide fullscreen viewing;
- provide “Live work” and “Documented still/video” controls with concise explanations;
- do not autoplay audio;
- honor `prefers-reduced-motion` and provide a static alternative;
- expose loading and failure states without substituting a blank rectangle;
- state whether the presentation is upstream, Museum-retained, emulated, or reconstructed;
- never imply determinism, completeness, or preservation status that the record does not establish.

Security requirements appear in section 12.

### 7.5 Artist page

Every represented artist needs a durable page. The initial Casey Reas page must include:

- portrait or approved contextual image if rights permit; otherwise a strong typographic opening, not a broken placeholder;
- concise biography and current practice summary;
- a substantive practice essay;
- a chronology of relevant artistic, pedagogical, software, publishing, and institutional work;
- all Museum-held works, shown visually;
- Museum-relevant projects and series;
- selected exhibitions, collections, publications, and sources limited to verified facts;
- related essays, interviews, programs, and technical features;
- name authority identifiers where available.

The existing `casey-reas-artist-practice.md` must be published as core page content, not left as a repository-only document.

### 7.6 Project or collection page

A project page explains the shared system behind a group of works without collapsing their differences.

Required content:

- project title, artist, date, platform, and project identifier;
- primary visual field showing the Museum's works from the project;
- project description and artist statement;
- Museum essay about the project's ideas, visual system, and behavior;
- technical account of generator, token inputs, dependencies, and output behavior;
- edition and project context;
- transparent trait-analysis methodology and results when the Museum publishes analysis;
- no marketplace rarity language or OpenSea metrics;
- citations and related works.

For the Casey gift, project pages must support CENTURY, 923 Empty Rooms, and Complexity, with the collection-level essay connecting them without erasing project-specific interpretation.

### 7.7 Gift and accession story

The visitor-facing label should be “Gift” or “Acquisition”; “Accession” remains the precise record term.

The Casey gift page must become a complete, illustrated dossier with:

- a strong visual opening using the seven works;
- “Gift of Punk 6529” or the exact approved donor credit;
- a concise explanation of why the Museum accepted the group;
- a substantial donation essay explaining the group's formation, the donor's relation to the works where documented, the artistic and historical significance of the gift, and what the donation establishes for the Museum at its founding moment;
- the seven works with images, titles, projects, and links;
- a narrative of the gift, receipt, formal acceptance, and accession;
- the full collection essay;
- the Casey Reas artist and practice profile;
- the curatorial accession review;
- the gift acceptance authorization and accession certificate in readable form;
- title, custody, compliance, rights, technical, condition, and preservation sections;
- a provenance timeline that separates token transfers, legal title, and Museum custody observations;
- transaction and chain evidence as inspectable detail;
- canonical documents and machine records as downloads;
- document status and dates without implying that Git history is the legal instrument.

The donation essay is not a warmed-over accession certificate. It must interpret the donor's selection, the relationships among the seven works, the transition from private collecting to public trust, and the gift's consequences for a decentralized museum, while grounding every donor-history and acquisition claim in evidence.

The following existing public files must be routed and placed intentionally:

| Existing file | Public placement |
|---|---|
| `public/gift-acceptance-authorization.md` | Gift page: Acceptance |
| `public/accession-certificate.md` | Gift page: Accession record |
| `public/casey-reas-artist-practice.md` | Artist page and linked gift section |
| `public/casey-reas-collection-essay.md` | Gift/project narrative |
| `public/curatorial-accession-review.md` | Why these works / curatorial rationale |
| `public/custody-title-and-compliance-diligence.md` | Provenance and diligence |
| `public/title-rights-and-accession-review.md` | Rights and title |
| `public/technical-and-condition-review.md` | Display, behavior, condition, and preservation |
| `public/6529NM.2026.001.01.md` through `.07.md` | Individual artwork pages |

### 7.8 Acquisitions and program records

Acquisitions pages are editorial experiences for coherent Curated Acquisition units, not record dumps. Acquisition Programs are separate pathway/mechanism records in the “How works enter the Museum” namespace: they are discoverable from the Acquisitions hub and link to the Curated Acquisitions or Work outcomes they produce, but they are not themselves acquisitions or Collection units. The public page is a projection of typed records; it never turns a source outcome or Program relation into an accession or Collection member. Only an active accession relation followed by the corresponding Collection relation can place a Work in the permanent Collection.

The Keys and Gates page must include:

- the program's curatorial premise;
- the selected works as a media-rich visual sequence;
- artist, title, and selection context for each work;
- the selection mechanism explained in plain language;
- a prominent, unambiguous visitor statement: **Selected through an acquisition program; acquisition pending**;
- an optional independent qualifier: **Not yet minted; minting route under consideration.**;
- no contract address, token ID, custody claim, accession number, or collection-holding claim before primary mint and subsequent evidence exist;
- future links to Stream or other primary-mint presentation only after deployment and mint evidence;
- an archive of the program source and decision history in the evidence layer.

Exhibition remains a reserved relation/type vocabulary, not a page or instance in this release. If a future exhibition is published, every displayed item's relationship to the Museum must be explicit and separately evidenced.

### 7.9 Research Publications and essays

The Museum should publish serious editorial material independently of the register:

- artist profiles;
- collection and project essays;
- close readings of individual works;
- acquisition and gift stories;
- conservation and software-preservation features;
- transparent generative trait studies;
- histories of decentralized and computational art;
- interviews and commissioned media when available.

Each story needs author, date, revision date, citations, related works, and a stable URL. Repository filenames must not be the public headline or navigation system.

### 7.10 About, collecting, and decisions

The About layer must render the full human-readable policies with a readable table of contents, not a wall of concatenated Markdown cards. It should explain:

- the Museum's mission;
- what is collected;
- what donation preapproval means and does not mean;
- how offers, gifts, accessions, display, and preservation differ;
- how decisions are made;
- how GitHub commitments and future on-chain records work;
- how to inspect the open repository.

Decision records should have human-readable titles, adopted effects, dates, sources, and affected Museum areas. Vote counts and Wave statuses must not be presented as self-executing governance when the record says otherwise.

## 8. Public content model

The current canonical record model is strong enough for evidence but incomplete for publication. The frontend must not scrape arbitrary nested JSON or infer page structure from filenames. The Museum repository must publish a validated, versioned public presentation projection.

### 8.1 Required publication entities

The projection must support:

- artwork;
- artist/agent;
- project or series;
- accession/gift;
- program;
- exhibition;
- story/essay;
- institutional page;
- decision;
- media resource;
- IIIF manifest;
- relationship among these entities.

### 8.2 Typed public documents

Every public Markdown document needs explicit metadata or a companion index declaring:

- stable document ID;
- document type;
- title and standfirst;
- author or institutional author;
- publication and revision dates;
- language;
- subjects and related entity IDs;
- display placement and order;
- citation list;
- publication status;
- canonical source path.

The Casey public dossier should have one accession-level publication index. The frontend must not guess that a file named `technical-and-condition-review.md` belongs after a rights review.

### 8.3 Public artwork projection

A generated artwork projection must include, at minimum:

```json
{
  "object_id": "6529NM.2026.001.01",
  "title": "...",
  "artist_ids": ["artist:casey-reas"],
  "date_display": "...",
  "classification": "...",
  "medium_display": "...",
  "project_id": "...",
  "accession_lot_id": "6529NM.2026.001",
  "credit_line": "...",
  "label_short": "...",
  "label_long_document_id": "...",
  "primary_media_id": "...",
  "iiif_manifest_id": "...",
  "rights_record_id": "...",
  "technical_record_id": "...",
  "chain_citation": "eip155:1/erc721:.../...",
  "related_object_ids": ["..."],
  "source_record_path": "..."
}
```

This is a web publication projection, not a replacement for the Stream-compatible canonical object envelope. It must be deterministically generated from canonical records and separately reviewed public editorial content.

### 8.4 Artist and project entities

The repository needs canonical public artist and project records so that pages do not derive identity from repeated strings. They must support names, preferred display, biography, chronology, authority identifiers, project relationships, sources, and linked documents. A project's technical and curatorial identities must remain distinct but cross-linked.

### 8.5 Future on-chain adapter

The frontend must consume a source-neutral publication interface. During the transitional phase, GitHub release artifacts supply it. Later, an Ethereum registry, content-addressed storage, or Stream records may supply canonical commitments and locations. The React page layer must not know whether a record came from GitHub or Ethereum.

The publication projection must preserve source record IDs, payload commitments, media commitments, and schema versions so that a source migration does not break public URLs or silently change meaning.

### 8.6 Open Museum and per-page source colophon

The public repository is an institutional feature, not backend trivia. During
the transitional phase, visitors must be able to understand that the Museum
record is publicly inspectable, cloneable, and group-editable through pull
requests. They must also understand the boundary: anyone may propose an
improvement, while review and deterministic validation protect the published
record.

The About page and source/research apparatus must publish the complete
three-layer account defined in `docs/open-museum.md` and
`docs/onchain-transition.md`:

1. the public repository is the current shared review and publication record;
2. the Fall 2026 goal is on-chain commitments and append-only lineage for every
   admitted Museum record, with large payloads on content-addressed storage;
   and
3. the frontend is a replaceable display and interpretation layer, not the sole
   location of institutional memory.

The home page should carry a concise art-first version after the initial
collection encounter. It must not lead with GitHub, governance process, or
contract architecture.

Every Museum page family must end with a quiet source colophon. The colophon
must identify that the page comes from the public Museum record and provide:

- an immutable link to the exact reviewed source commit and validated source
  path;
- a contribution action targeting the canonical editable source path;
- a link to the governed contribution guide; and
- the short source commit as a machine-verifiable citation where useful.

Source and contribution paths must come from the validated publication model,
not arbitrary Markdown or route input. Exact-source and editable targets are
different links: an immutable commit can be inspected but is never presented
as directly editable. The contribution invitation must remain subordinate to
the art and scholarship and use the native 6529 visual grammar rather than a
generic process card.

## 9. Media and IIIF standard

### 9.1 Immediate Casey requirement

The Museum already has rights-reviewed authority under CC BY-NC 4.0 to make attributed noncommercial documentation and preservation copies of the seven Casey works, subject to the recorded conditions. The initial screenshot bytes were not retained. That gap must now be closed with a new, dated capture event; the new bytes must not be represented as the missing initial captures.

Before the Casey accession can be considered properly published, the repository and delivery system must contain for every one of the seven objects:

- a retained primary still or poster frame;
- a web delivery derivative;
- intrinsic dimensions and aspect ratio;
- media type, byte size, and SHA-256;
- capture date and environment;
- source URL and source-record reference;
- alt text, caption, credit line, and rights notice;
- relationship to the live generator;
- retention and preservation status;
- an IIIF Presentation 3 manifest.

Where behavior is essential, retain an approved short reference video or a documented pair/sequence of stills in addition to the primary still.

### 9.2 Media resource record

Each media resource must carry:

- stable media ID;
- related object ID;
- role: `primary_still`, `primary_live`, `poster`, `detail`, `reference_video`, `audio`, `transcript`, `long_description`, or `preservation_master`;
- native URI and delivery URI;
- MIME type;
- width, height, duration, and color information where applicable;
- raw-byte digest and byte size;
- source and derivation event;
- capture or creation time;
- alt text and optional long description;
- caption and required credit line;
- rights basis and use constraints;
- retained/upstream-only/derived state;
- relationship to the work, which must not falsely identify a documentation file as the tokenized work itself.

### 9.3 Storage and delivery

During the GitHub transitional phase:

- canonical presentation metadata, IIIF manifests, captions, rights, and small approved web derivatives may be tracked in the Museum repository;
- every binary must be raw-byte hashed and included in a dedicated media inventory;
- large preservation masters may live in content-addressed storage, but their identifiers, digests, byte sizes, and preservation events must remain in the repository;
- `media.6529.io` may resolve and transform delivery assets but is not the canonical identity of the underlying resource;
- upstream Art Blocks URLs remain source and fallback evidence, not the Museum's only copy where retention is authorized;
- Git LFS pointer files must never be mistaken for the retained media bytes;
- a missing upstream resource must not erase the Museum page or its retained surrogate.

### 9.4 IIIF Presentation 3

Every serious visual or time-based object should publish a IIIF Presentation 3 manifest under the Stream-aligned `STREAM_IIIF_P3_MIN_V1` profile. The manifest must include human-readable labels, required statements, rights, attribution, canvases with correct dimensions/duration, content-addressed painting resources, thumbnails, and links back to the Museum object and canonical record.

The site should provide a deep-zoom viewer when source resolution warrants it, without forcing a heavyweight viewer on ordinary images.

### 9.5 Media presentation rules

- Never crop an artwork by default to fit a card. Use letterboxing or an artist-approved crop derivative.
- Never upscale a small source and imply archival quality.
- Never show a thumbnail without title, artist, alt text, and credit available in context.
- Never call an upstream marketplace image the preservation master.
- Never silently swap a live work for a still.
- Never render arbitrary image URLs found in Markdown or untrusted metadata.
- Never expose tracking parameters, wallet requests, or third-party navigation through an embedded work.

## 10. GitHub publication adapter

### 10.1 Replace “fetch the repository” with a publication release

The current adapter loads the release manifest and then fetches every allowlisted Markdown and JSON document. A Museum with growing records and media needs a purpose-built release artifact.

Add a deterministic `publication-catalog` artifact containing:

- schema version;
- source Museum manifest commitment;
- generated-at and source-commit metadata;
- normalized entities and relationships;
- typed public-document index;
- media inventory references;
- IIIF manifest references;
- route slugs and aliases;
- search projection;
- content and media completeness flags;
- the artifact's own SHA-256 and Keccak commitment.

The frontend should fetch the catalog first, validate it, then fetch only the documents and media required for the requested route. It must cache by immutable commitment rather than treating every request to `main` as unrelated content.

At ingestion time, the adapter must resolve `main` once to a full Git commit SHA and fetch the release manifest, publication catalog, documents, and declared assets only from that immutable commit. It must never assemble a visitor response from files fetched across different moving-branch states. The accepted snapshot records repository, commit SHA, manifest SHA-256, manifest Keccak commitment, publication-catalog commitment, accepted paths, file digests, byte sizes, and build time.

All required publication entities and their declared source records must validate atomically before a new snapshot becomes active. A later delivery failure for one derivative may fall back to another approved presentation, but it must not create a mixed or partially verified canonical snapshot.

The Open Museum statement, on-chain transition statement, and contribution
guide are required publication documents. A snapshot that omits any of them,
cannot bind them to the active source commit, or cannot map a public page to its
declared source path must fail closed rather than rendering a hollow
participation invitation.

### 10.2 Fail-closed integrity, graceful public behavior

- Reject a catalog whose schema, digest, or source-manifest binding is invalid.
- Keep serving the last valid publication release when a new release is invalid or temporarily unavailable.
- Isolate a broken object or media asset rather than blanking the entire Museum.
- Display a concise stale-content notice only when material.
- Record diagnostics for operators without exposing internal error codes as visitor copy.
- Maintain at least one prior valid publication catalog for rollback.
- Validate canonical envelopes, payload commitments, schema IDs, record types, and statuses with pinned versioned schemas before normalization.
- Never publish permissively extracted fields from an envelope or payload that failed its canonical schema.

### 10.3 No filename inference

The adapter must not infer an entity's public meaning only from a repository path. Paths remain canonical evidence references; explicit typed indexes control publication. Unknown document and media types are rejected from public rendering until supported.

### 10.4 Secure Markdown

Markdown remains useful for reviewed long-form scholarship. The renderer must:

- support headings, paragraphs, lists, tables, footnotes, block quotations, figures, captions, and internal cross-links;
- sanitize HTML and disallow scripts, styles, event handlers, and unsafe URL schemes;
- render figures only through approved media IDs;
- rewrite repository document links to public Museum routes where a mapping exists;
- preserve a source link for citations;
- produce stable heading IDs and a table of contents for long documents;
- never replace all imagery with an omission notice.

## 11. Frontend component and data architecture

The rebuild should introduce explicit Museum primitives instead of extending generic cards indefinitely.

Required component families:

- `MuseumArtworkViewer`: chooses image, video, audio, live, IIIF, and fallback presentations;
- `MuseumImageViewer`: responsive image, zoom, fullscreen, caption, credit, and download/use information;
- `MuseumLiveWorkFrame`: activation, sandbox, loading, fullscreen, reduced-motion alternative, and failure fallback;
- `MuseumArtworkCard`: media-first, no default crop, complete identity;
- `MuseumObjectLabel`: title, artist, date, medium, accession, and credit line;
- `MuseumEssay`: long-form typography, footnotes, figures, and table of contents;
- `MuseumArtistHeader` and `MuseumProjectHeader`;
- `MuseumProvenanceTimeline`: separates transfer, title, custody observation, and accession events;
- `MuseumRightsSummary`: plain-language use and credit requirements;
- `MuseumTechnicalSummary`: behavior, dependencies, display, and preservation;
- `MuseumDossierNavigation`: coherent accession document order;
- `MuseumEvidenceDrawer`: canonical record, hashes, source links, and downloads;
- `MuseumSearch` and `MuseumFilterPanel`;
- `MuseumSourceNotice`: stale/partial source states only when necessary.

Page components consume a normalized domain model. They must not traverse arbitrary `unknown` JSON at render time.

## 12. Security and privacy for live and remote media

Live generative work is untrusted executable content even when the artist and platform are trusted institutionally.

Required controls:

- explicit visitor activation before loading third-party executable content;
- a dedicated origin or tightly isolated route for embedded works;
- sandboxed iframe with the minimum required permissions;
- no wallet provider injection;
- no top navigation, popups, downloads, forms, pointer lock, clipboard, camera, microphone, geolocation, or payment permissions unless a work-specific security review explicitly requires one;
- strict frame-specific Content Security Policy and Permissions Policy;
- HTTPS-only transport;
- allowlisted generator origins and exact normalized URLs from approved media records;
- no arbitrary HTML from token metadata;
- referrer minimization;
- timeout and resource ceilings;
- visible fallback when the generator refuses framing or fails;
- security tests for sandbox escape, origin changes, redirects, and prohibited capability access;
- clear disclosure when activating a live work contacts a third-party host.

Museum media delivery URLs should be digest-addressed, not open `?url=` proxies. A server-side registry must bind every allowed upstream resource to an object, expected MIME family, byte ceiling, approved rights/display state, and cache identity. The resolver must reject private or reserved network targets, revalidate redirects and DNS at every hop, inspect magic bytes and dimensions, send `X-Content-Type-Options: nosniff`, and cache immutable derivatives by source digest.

The Museum should prefer a preserved or controlled-runtime presentation when technically and legally available. It must not rewrite artist code or claim fidelity without a documented preservation event and comparison.

Visitor analytics must be privacy-minimizing. Do not send token IDs, wallet addresses, search terms, or live-work interactions to third parties unnecessarily.

## 13. Accessibility

The entire Museum surface, including artwork viewers and alternate presentations, must meet WCAG 2.2 AA. Conformance applies to full pages and responsive variants, not only the surrounding text shell.

Required provisions:

- meaningful alt text written for each work and presentation, not the title repeated mechanically;
- long descriptions where visual complexity warrants them;
- captions and transcripts for time-based media;
- audio description or a meaningful media alternative when required;
- complete keyboard access and visible focus;
- no keyboard trap in fullscreen, zoom, filters, drawers, or live frames;
- controls with visible labels and accessible names;
- logical heading and landmark structure;
- correct reading order at all breakpoints;
- 200% text resize and 400% reflow without loss of content;
- target sizes and spacing meeting WCAG 2.2 expectations;
- contrast verified over real artwork-adjacent backgrounds;
- no information conveyed by color alone;
- reduced-motion behavior and pause/stop controls;
- no autoplay sound;
- programmatically identified language and language changes;
- accessible error, loading, and unavailable states;
- a static or textual alternative when live executable art cannot itself conform.

Accessibility description is part of the media record and collection scholarship, not a last-minute frontend patch.

## 14. Performance and resilience

The site must pass current Core Web Vitals at the 75th percentile on both mobile and desktop:

- Largest Contentful Paint at or below 2.5 seconds;
- Interaction to Next Paint at or below 200 milliseconds;
- Cumulative Layout Shift at or below 0.1.

Additional Museum requirements:

- a useful artwork still appears before any live generator initializes;
- responsive AVIF/WebP derivatives with a high-quality source fallback;
- explicit dimensions or aspect ratios to prevent layout shift;
- route-level data loading instead of fetching the entire corpus;
- immutable caching by content digest;
- CDN delivery without sacrificing canonical source identity;
- lazy loading below-the-fold media;
- constrained font families and subsets;
- no client-side hydration requirement for core labels, essays, captions, or catalog data;
- useful server-rendered output for search engines, archival crawlers, and no-JavaScript readers;
- graceful presentation on slow networks and when Art Blocks, GitHub, RPC, or media resolver endpoints are unavailable;
- monitoring that distinguishes source, catalog, media, and live-generator failures.

Performance budgets must include representative high-resolution art pages, not only text fixtures.

## 15. Search, discovery, and relationships

Search must index reviewed public display fields, not raw evidence indiscriminately. At minimum it should index title, artist, project, date, medium, accession number, chain identity, essay text, and controlled subjects.

Every object should expose meaningful relationships such as:

- more by this artist;
- more from this project;
- works acquired in the same gift;
- works sharing a technical or curatorial theme;
- related stories and conservation features;
- program or exhibition appearances.

Relationship labels must explain the connection. “Related” cannot mean only “the algorithm returned this.”

## 16. Rights, provenance, and chain evidence in the interface

### 16.1 Rights

The public page must separately state:

- token ownership/title;
- copyright holder or stated licensor;
- applicable license;
- Museum rights to reproduce, publish, exhibit, adapt, preserve, and create accessibility material;
- required attribution and credit line;
- material restrictions.

For the Casey works, the interface should explain CC BY-NC 4.0 in plain language and link to the official deed/legal code. It must not imply that owning the token transferred copyright.

### 16.2 Provenance

The provenance view must visibly separate:

- on-chain token transfers;
- legal-title events and donor declarations;
- Museum receipt and accession;
- custody observations;
- approvals or encumbrance checks;
- corrections and superseding evidence.

Each event should provide date, actor/role where public, object scope, evidence class, source, and uncertainty. A wallet balance or transfer is never labeled accession by implication.

### 16.3 Chain-native evidence

Chain details should use a compact human summary with optional expansion:

- network;
- token standard;
- contract and token ID;
- CAIP-19 citation;
- transaction;
- block number, time, and finality observation;
- custody address/ENS;
- source links and record commitment.

Hashes and addresses need copy controls and accessible names. Truncation must never make two identifiers indistinguishable, and the full value must remain available.

The expert evidence layer must also disclose the exact Museum publication source: repository, full Git commit SHA, release-manifest SHA-256 and Keccak commitment, publication-catalog commitment, record path and digest, asset digest, and snapshot build/retrieval time. “Canonical main” alone is not a reproducible citation.

## 17. Metadata, sharing, and open access

Every public artwork, artist, project, gift, program, exhibition, and story page needs:

- unique title and description;
- canonical URL;
- approved Open Graph and social image derived from Museum media, not a generic site card;
- artist, title, date, and credit in the social image metadata where appropriate;
- JSON-LD using suitable Schema.org types such as `VisualArtwork`, `Person`, `CollectionPage`, and `Article`, without forcing chain facts into semantically incorrect fields;
- IIIF manifest discovery for works;
- machine-readable rights and license links;
- citation guidance;
- stable identifiers;
- sitemap inclusion;
- indexability of public SSR content.

The site should expose open datasets and APIs as a research feature, but the open-data page must distinguish curatorially approved publication data from incomplete or machine-derived fields.

## 18. Mobile and interaction design

Mobile is a primary museum visit, not a reduced desktop page.

Requirements:

- artwork remains the first substantial content;
- captions and identity stay close to the media;
- sticky controls never obscure the work;
- fullscreen exits are obvious and reachable;
- swipe is optional and never the sole navigation method;
- filters use an accessible sheet with a persistent result summary;
- long provenance and technical sections collapse by meaningful topic, not arbitrary card height;
- hashes wrap or copy cleanly without horizontal page scrolling;
- live works receive an explicit device-compatibility message and fallback;
- all layouts are tested in portrait and landscape.

## 19. Casey Reas launch exemplar

The first complete implementation must make the Casey gift the quality benchmark. It is not sufficient to build generic templates with placeholder content.

### 19.1 Required visible experiences

- one illustrated gift/acquisition page;
- one complete Casey Reas artist page;
- one collection-level essay presentation;
- project context for CENTURY, 923 Empty Rooms, and Complexity;
- seven artwork pages, each with a retained still and live-generator option where safe;
- a visual grid of all seven works;
- per-work short and long interpretation;
- accession, title, provenance, rights, technical, and preservation views;
- a correctly credited social card for each object and the gift;
- related-work navigation across the seven works;
- IIIF manifest and canonical record links for each object.

### 19.2 Casey-specific content rules

- Preserve the distinction between documented fact, artist/platform statement, Museum observation, and Museum interpretation.
- Do not flatten the moving works into static color/shape descriptions.
- Do not infer all possible generator states from one or two captures.
- Do not call trait prevalence rarity, quality, value, or significance.
- Do not use OpenSea traits or rankings.
- State the token-specific project and chain identity precisely.
- Apply the exact donor credit and CC BY-NC 4.0 attribution requirements.
- State the difference between the live generator, retained documentation, and preservation package.

### 19.3 Casey release acceptance

A person unfamiliar with the project must be able to reach the Museum home and, within two actions:

1. see a Casey work at meaningful size;
2. enter its live or documented presentation;
3. learn who Casey Reas is;
4. understand the three represented projects;
5. understand why these seven works entered the Museum;
6. find the donor credit and acquisition story;
7. inspect provenance, rights, and technical evidence if desired.

If any of those outcomes depends on visiting GitHub, the release is incomplete.

## 20. Keys and Gates launch requirements

Keys and Gates is the second quality benchmark and tests the Museum's ability to present work that is selected but not yet accessioned.

Required work:

- acquire or derive rights-cleared visual presentation resources for all sixteen selected outcomes;
- create typed artist, title, selection, and media projections;
- present the works in a designed sequence or exhibition, not a text-card matrix;
- publish the curatorial frame and selection history;
- label every work **Selected through an acquisition program; acquisition pending** in visitor language, with the qualifier **Not yet minted; minting route under consideration.**;
- suppress holdings, token, contract, custody, and accession fields until supported by primary evidence;
- update the presentation after minting through an append-only state change, not by rewriting the selection history;
- support either future Stream deployment option without changing visitor URLs.

## 21. Verification and release standard

A Museum frontend release cannot be approved from CI, route status, or DOM text alone.

### 21.1 Automated verification

Required checks include:

- publication-catalog schema and commitment validation;
- source-to-projection traceability for every displayed factual field;
- typed-document completeness and route resolution;
- media digest, MIME, size, dimension, rights, alt-text, caption, and credit validation;
- IIIF Presentation 3 conformance;
- no unapproved or unsafe media origins;
- no arbitrary executable embed URLs;
- unit tests for all normalizers and presentation adapters;
- object, artist, project, gift, program, essay, and policy route tests;
- keyboard and automated accessibility checks;
- CSP, iframe sandbox, and redirect tests;
- structured-data validation;
- broken-link and source-link checks;
- visual-regression tests at representative desktop and mobile viewports;
- image snapshot tests proving that actual artwork media, not only placeholders, rendered;
- Core Web Vitals and route payload budgets;
- stale, partial, unavailable, and invalid-source behavior;
- compatibility against the previous valid publication catalog.

### 21.2 Human verification

Every public release requires review of the real rendered pages, with retained screenshots or video evidence. The review must answer:

- Does the art appear, at the intended scale and without accidental cropping?
- Does live, video, zoom, fullscreen, and fallback behavior work?
- Are titles, artists, dates, media, captions, and credits correct?
- Does the interpretation say something specific and defensible?
- Can a first-time visitor understand the Museum without opening the evidence layer?
- Can a specialist reach the complete record without using repository search?
- Are selected, gifted, accessioned, held, display-ready, and preserved states represented accurately?
- Does the mobile experience remain an artwork experience?
- Does the page feel intentionally art-directed rather than generated from record fields?
- Is the page immediately recognizable as part of `6529.io`, with the real site typography, navigation, theme, spacing, interaction, and responsive conventions?
- Are Museum-specific visual extensions traceable to a real art-viewing need instead of a generic template convention?

The evidence package must include at least the Museum home, collection index, one artist page, one gift page, all media modes of a representative object page, a mobile viewport, a source-failure state, and the complete Casey object grid. It must also include side-by-side desktop and mobile captures of representative established 6529 routes and the corresponding Museum routes, with the visual-fidelity matrix required by section 6.1.1.

### 21.3 Absolute launch gates

The frontend must not be described as complete or world-class while any of these are true:

- accessioned artworks have no visible approved media;
- a live work has no meaningful fallback;
- public accession scholarship exists in GitHub but cannot be read on the site;
- the collection is confused with donation-eligibility policy;
- selected unminted works are presented as holdings;
- raw JSON is the main detailed experience;
- artwork credit or rights are missing;
- accessibility alternatives are missing;
- visual QA did not inspect actual rendered artwork;
- the Museum uses a detached theme or cannot be recognized as a native part of `6529.io`;
- the implementation approximates site styling instead of reusing the repository's actual tokens and shared primitives;
- generic cards, badges, gradients, dashboard composition, or invented editorial styling dominate visitor-first pages;
- the site can return HTTP 200 while silently omitting core dossier or media content.

## 22. Implementation sequence

This order minimizes throwaway frontend work because it fixes the publication product before polishing templates.

### Phase 0 — Correct the product boundary

- Adopt this standard as the replacement frontend brief.
- Freeze further expansion of the current dashboard/card pattern.
- Relabel current routes so policy eligibility is not confused with holdings.
- audit and document the exact production 6529 design tokens, global chrome, shared components, breakpoints, theme behavior, and representative page patterns;
- define a visual-fidelity matrix separating reused 6529 foundations from justified Museum extensions and rejected generic-template patterns;
- Define the visitor IA and visual direction through high-fidelity desktop and mobile designs using actual Casey art and text.

### Phase 1 — Publish the missing art and scholarship

- create the typed public-document index;
- create artist and project entities;
- create media resource records;
- retain and hash rights-cleared Casey media;
- publish seven IIIF manifests;
- generate the first publication catalog;
- add validation for every new artifact.

### Phase 2 — Build the artwork experience

- implement media viewers and the live-work sandbox;
- implement the artwork, artist, project, and gift pages;
- publish all Casey scholarship;
- implement responsive images, captions, credit, rights, and accessibility;
- add search projection and related-work navigation.

### Phase 3 — Replace the Museum home and collection discovery

- deploy the art-led home;
- deploy the actual collection index;
- move collecting policy, donation eligibility, decisions, and methods under About;
- add Research Publication and interpretive-essay surfaces;
- add structured metadata and social imagery.

### Phase 4 — Publish Keys and Gates as a program

- obtain and register media for the sixteen selected works;
- build the illustrated program experience;
- preserve selected/unminted boundaries;
- prepare append-only post-mint transitions.

### Phase 5 — Harden and extend

- complete visual, accessibility, security, performance, and preservation gates;
- add multilingual publication support;
- add richer IIIF viewing and downloadable research data;
- reserve the Exhibition route family and schema vocabulary; publish no Exhibition instance until a reviewed exhibition record exists;
- migrate the publication source from GitHub commitments to on-chain/content-addressed records when the contract is ready, without changing public URLs.

## 23. Definition of world-class for this Museum

The goal is not to imitate the surface styling of MoMA, the Met, Centre Pompidou, Tate, or the Whitney. It is to meet their public-service expectations—art at meaningful scale, authoritative cataloging, serious scholarship, strong artist and collection pathways, rights and credit, search, accessibility, and durable research access—while exceeding them in chain-native provenance, transparent record commitments, executable-art care, and reproducibility.

The finished Museum should make two impressions at once:

1. **This institution cares deeply about the art.**
2. **This institution can prove what it says.**

The current site demonstrates mostly the second, and only to specialists. The rebuild is complete when the first is unmistakable and the second remains available without dominating it.

## 24. Benchmark and standards references

These references establish useful public-experience and interoperability benchmarks. They are not visual templates.

- [MoMA: The Collection](https://www.moma.org/collection/) — art-led collection entry, artwork/artist search, on-view and recent-acquisition paths.
- [MoMA: About the Collection](https://www.moma.org/collection/about/) — explicit public research access and distinction between published and not-yet-curatorially-approved data.
- [The Metropolitan Museum of Art: The Met Collection](https://www.metmuseum.org/art/collection) — broad collection search and object-centered research access.
- [Whitney Museum: Collection](https://whitney.org/collection/works) — visual collection discovery, media-aware filtering, artist pathways, digital-art presentation, and reduced-motion respect.
- [Whitney Museum: Artists](https://whitney.org/artists) — artist-centered discovery connected to works and exhibitions.
- [Centre Pompidou: Pompidou+](https://www.centrepompidou.fr/en/pompidou) — high-resolution collection resources, video, audio, educational material, and virtual exhibitions.
- [IIIF Presentation API 3.0](https://iiif.io/api/presentation/3.0/) — interoperable human presentation of images, video, audio, and compound born-digital objects.
- [W3C Web Content Accessibility Guidelines 2.2](https://www.w3.org/TR/WCAG22/) — required accessibility baseline.
- [Schema.org VisualArtwork](https://schema.org/VisualArtwork) — public structured-data vocabulary for artworks.
- [Core Web Vitals](https://web.dev/articles/vitals) — field-performance thresholds for loading, interaction, and visual stability.

## 25. Current frontend remediation map

This map turns the product standard into an initial code boundary for `6529seize-frontend`. It describes replacement responsibility, not a requirement to preserve the present component structure.

| Current source | Current limitation | Required change |
|---|---|---|
| `styles/fonts.css`, `styles/globals.css`, and `tailwind.config.ts` | These define the site's real Montserrat-led typography, black ground, white/iron hierarchy, primary-blue accent, focus states, layout variables, breakpoint extension, and motion vocabulary; a Museum-only theme would bypass them. | Treat these files as visual source of truth. Reuse their tokens and scoped utilities; document and narrowly justify every Museum-specific extension instead of approximating the site with local values. |
| `components/layout/WebLayout.tsx` and `components/layout/sidebar/**` | The existing shell establishes the 1324px desktop boundary, collapsible/off-canvas sidebar, global rhythm, navigation behavior, and focus conventions. | Keep the Museum inside this shell and validate it at expanded, collapsed, narrow, and mobile states. Museum layouts may become media-wide inside the content region but must not replace or visually contradict global chrome. |
| `hooks/useSidebarSections.ts` and `components/navigation/BottomNavigation.tsx` | Desktop and mobile route discovery use established site-native section, active-state, icon, and dock conventions. | Integrate Museum navigation through these real systems, including active-path, localization, touch, keyboard, and mobile behavior; do not add a detached Museum navigation framework. |
| Existing art surfaces under `components/the-memes/**`, `components/memelab/**`, and `components/nextGen/collections/**` | They contain useful 6529-native image, collection, slideshow, provenance, and zoom conventions, but also product-specific commerce and metric patterns. | Audit and reuse sound low-level patterns while removing mint, market, rarity, leaderboard, and metric semantics from Museum presentation. Record reused and rejected patterns in the visual-fidelity matrix. |
| `lib/museum/types.ts` | Canonical source URLs embed moving branch `main`; `MuseumObjectRecord` has no media, rights summary, project, essay, artist entity, provenance timeline, or IIIF fields. | Introduce immutable snapshot identity and a versioned publication-domain model with discriminated presentation types. |
| `lib/museum/source.ts` | `PUBLIC_PREFIXES` and `SUPPORTED_EXTENSIONS` admit only Markdown/JSON records; raw URLs are built against moving `main`; document failures yield a partial corpus. | Resolve one full commit SHA, verify one atomic publication catalog, fetch by immutable SHA/digest, support declared media/IIIF resources, and retain the last complete snapshot. |
| `lib/museum/normalize.ts` | Permissive field extraction produces a thin view; only `policies/` and `docs/` Markdown become text documents; accession public Markdown is ignored as publication content. | Replace path inference with schema-validated typed entity/document indexes and deterministic source-to-publication projections. |
| `components/museum/MuseumMarkdown.tsx` | All Markdown images are replaced with “Media omitted from the record view”; raw JSON disclosure is the main depth component. | Add sanitized essay/figure rendering through approved media IDs and move JSON to an expert evidence/download component. |
| `components/museum/MuseumRecordCard.tsx` | One generic text card represents policies, decisions, programs, accessions, and art. | Replace with domain-specific media-first artwork, artist, project, story, program, and institutional components. |
| `components/museum/MuseumShell.tsx` | Navigation foregrounds institutional record domains; source banner describes moving canonical main. | Implement visitor IA, move institutional material under About, and cite exact immutable snapshot evidence in the expert layer. |
| `app/museum/network/page.tsx` | The home is dominated by section cards, counts, and release evidence. | Replace with curated artwork hero, mission, Casey gift, Keys and Gates program, collection discovery, and stories. |
| `app/museum/network/accessions/[accessionId]/page.tsx` | The page renders register summary, limits, object links, and JSON but none of the human-readable dossier. | Build an illustrated gift/acquisition narrative and route every declared dossier document. |
| `app/museum/network/objects/[objectId]/page.tsx` | Legacy implementation path has no artwork viewer and only thin object fields, statement text, JSON, and source link. | Replace with `/museum/network/works/[workId]`, using the canonical `6529NM-W-####` Work ID and the complete artwork-page specification, including still/live presentation, interpretation, catalog, rights, provenance, preservation, IIIF, and evidence. |
| `app/museum/network/collections/**` | “Collections” means preapproved donation scopes rather than holdings. | Move these records to About / Collecting and reserve the Collection routes for accessioned objects. |
| `app/museum/network/programs/**` | Legacy program paths render Keys and Gates selections as text cards without art. | Move the visitor contract to `/museum/network/acquisition-programs/keys-and-gates`; add approved media and a designed acquisition-program presentation while preserving the source `selected_unminted` status. |
| `components/common/SandboxedExternalIframe.tsx` | Existing sandboxing is a useful starting pattern but its current origin contract does not cover Museum generators. | Build a dedicated `MuseumLiveWorkFrame` with exact work-level allowlisting and stricter capabilities. |
| `components/nft-image/renderers/NFTHTMLRenderer.tsx` | Existing generic HTML NFT rendering is not an adequate security boundary for Museum live works. | Do not reuse it for Museum presentation; use the dedicated sandbox and CSP. |
| `components/drops/view/item/content/media/**` | Generic social/drop media dispatch trusts broad URL/MIME inputs, uses generic alt text, and may autoplay video in view. | Reuse only low-level visual ideas; Museum media must be record-bound, rights-aware, digest-addressed, specifically described, and non-autoplaying. |
| `config/securityHeaders.ts` | Global media/frame policies are broader than a Museum live-work route should allow. | Add route- or origin-specific Museum CSP and Permissions Policy. |
| `next-sitemap.config.ts` and metadata helpers | Dynamic Museum objects, artists, projects, gifts, and stories are not comprehensively emitted as canonical sitemap/structured-data entities. | Generate sitemap paths, canonical metadata, social cards, and JSON-LD from the verified publication catalog. |
| Frontend tests | Tests prove normalization and route behavior but not that artwork and complete scholarship are actually visible. | Add the source, media, IIIF, security, accessibility, visual, performance, and human-rendered evidence gates in section 21. |

The frontend must not compensate for missing publication data with brittle scraping. Required artist, project, essay, media, rights, alt-text, and IIIF data belongs in the Museum repository's governed publication projection first.
