# Casey Reas publication program: durable work plan

- **Status:** active editorial integration plan; lead-editor lane manuscripts complete
- **Opened:** 2026-08-02
- **Accession:** `6529NM.2026.001`
- **Scope:** finished Museum publication writing for Casey Reas, the five represented project lines, the seven-work gift, and each accessioned object
- **Editorial target:** publication quality expected of a major contemporary-art museum; the supplied 8,576-word comparison manuscript is the minimum readily attainable scope, not the target

**Coordination update, 2026-08-02:** project essays and object entries are assigned to disjoint writing lanes. This lane owns the publication standard, this durable plan, the shared source/chronology matrix, the artist monograph, the seven-work collection essay, the gift narrative, and later editorial integration. It does not edit the five project essays or seven object entries.

## 1. Why this program exists

The existing Casey Reas artist/practice profile and collection essay are factually careful but materially below the Museum's publication standard. They were constructed as source-controlled accession research and then treated as finished public scholarship. Their paragraphs follow evidence clusters, technical qualifications, and defensive non-claims rather than a sustained argument about the art.

The problem is visible in the forms themselves. The current profile is approximately 1,600 words. It compresses twenty-five years of practice, biography, Processing, Feral File, five major bodies of work, museum history, and conservation into a source summary. The current collection essay is approximately 1,000 words and devotes a substantial share of that space to screenshot timing, byte retention, dependency status, and preservation caveats. The seven object pages repeat the same custody, rights, condition, and descriptor language around short observations. These documents are useful accession evidence. They are not sufficient curatorial publications.

The user supplied a public comparison manuscript, *Casey Reas: The System as Image*, produced from a one-line prompt in approximately six minutes. It contains 8,576 words in fifteen sections and succeeds where the Museum text failed: it advances a thesis, gives the practice a chronology, follows major bodies of work, and writes about artworks. Its weaknesses are equally important. It is lightly sourced, sometimes generic, uneven in critical pressure, and not closely tied to the exact seven works. The Museum publication must retain its confidence and breadth while exceeding it in original argument, primary-source depth, serious secondary scholarship, close looking, object specificity, and editorial finish.

## 2. Non-negotiable factual boundary

This program changes public interpretation, not collection identity or accession state. Every manuscript must preserve:

- the exact accession lot `6529NM.2026.001`;
- the exact seven object identifiers and native token identities;
- the accessioned status established by the reviewed control-plane records;
- the public credit line `Gift of punk6529`;
- the separation of token title, copyright, license, custody, display, and preservation facts;
- the reviewed CC BY-NC 4.0 conclusion and its conditions;
- the three CENTURY works as a Museum-formed comparative group, not an artist-designated triptych;
- the distinction between a static documentation surrogate and a live software manifestation;
- the 2021/2022 Phototaxis date discrepancy unless a source-backed amendment resolves it;
- the resolved 923/924 release structure without converting it into rarity or value language;
- the `pass_with_conditions` technical determination and ongoing software-preservation work;
- the prohibition on OpenSea and marketplace rarity metrics.

Interpretive writing may be confident. It may not invent artist intent, donor motive, historical influence, project chronology, or technical behavior. Facts will be established in notes; interpretation will be argued in prose.

## 3. Publication architecture and exact file plan

The current root-level public files remain as historical accession research summaries. New publication manuscripts will live under `records/accessions/6529NM.2026.001/public/curatorial/`. Each new file will carry version metadata and an explicit `supersedes_for_publication` field. Supersession applies only to the public narrative function named in the file; it does not supersede machine identity, title, rights, condition, custody, or accession records.

| Publication | Planned path | Editorial function | Target depth |
|---|---|---|---:|
| Casey Reas monograph | `public/curatorial/casey-reas-monograph.md` | Career-scale thesis, biography, genealogy, chronology, close readings, reception, current practice, and Museum collection context | 16,000-22,000 words |
| CENTURY project essay | `public/curatorial/projects/century.md` | Modernist abstraction, Kelly/Rickey/Soto/Max Bill contexts, Networks and related bodies, Art Blocks edition, and three-token comparison | 3,500-5,500 words |
| Process / Pre-Process essay | `public/curatorial/projects/process-and-pre-process.md` | Software Structures, Process grammar, notation/execution, 2003 origin, 2005 partial presentation, 2022 completion, and #63 | 3,500-5,500 words |
| MicroImage / Phototaxis essay | `public/curatorial/projects/microimage-and-phototaxis.md` | Braitenberg, artificial life, machine behavior, trace, code migration, browser edition, and #308 | 3,500-5,000 words |
| Atomism / 923 EMPTY ROOMS essay | `public/curatorial/projects/atomism-and-923-empty-rooms.md` | Pixel/atom logic, Vasarely, LACMA, six-city distribution, combinatorics, spatial performance, and #713 | 4,000-6,000 words |
| Still Life / Ex Nihilo essay | `public/curatorial/projects/still-life-and-ex-nihilo.md` | Platonic solids, RGB/HSB, software painting, time, display, physical translations, 2016-2026 arc, and #248 | 4,000-6,000 words |
| Seven-work collection essay | `public/curatorial/the-system-in-seven-states.md` | Why these seven works belong together, what their sequence makes visible, what the group omits, and why three CENTURY states matter | 6,000-8,000 words |
| Gift and accession narrative | `public/curatorial/gift-and-accession-narrative.md` | Artistic, historical, donor, public-trust, and institutional significance of the completed gift | 2,000-3,500 words |
| Seven object entries | `public/curatorial/objects/6529NM.2026.001.01.md` through `.07.md` | Concise label, extended close reading, project relation, manifestation, collection role, and selected notes | 900-1,500 words each |
| Notes and bibliography | `public/curatorial/casey-reas-notes-and-bibliography.md` | Claim-level notes, chronology sources, bibliography, source-quality notes, and research boundary | As required |
| Reusable writing standard | `docs/curatorial-publication-standard.md` | Museum-wide commissioning, evidence, close-looking, editing, and acceptance standard | 3,000-5,000 words |

The completed package is expected to contain approximately 50,000-70,000 words. Word count is a planning instrument, not a quality proxy.

## 4. Governing curatorial thesis

The monograph will test and refine this proposition:

> Reas's central achievement is not the production of generative images but the construction of conditions in which images can continue to occur. Across instructions, code, screens, prints, installations, books, platforms, and tokenized editions, he has treated the artwork as a negotiated relation among score, execution, material support, perception, and time.

This thesis is stronger than the generic phrase "system as image" because it makes four claims that the writing must prove:

1. Reas does not merely visualize systems; he stages the interval between rule and event.
2. His physical and digital outputs are different analytical manifestations of one practice, not separate careers.
3. Processing, teaching, publishing, and Feral File matter because they extend the ethics and social form of his studio practice, not because biography needs an achievements section.
4. Blockchain works matter where they alter edition, instantiation, distribution, ownership, and public access; they do not begin the practice or make token permanence equivalent to artwork preservation.

Counter-pressure is required. The monograph must address moments when Reas's systems produce fatigue, illegibility, excessive visual density, or a friction between technical transparency and perceptual opacity. Nora N. Khan's 2016 review is useful precisely because it resists automatic praise of immersion. A Museum text should distinguish achievement from hagiography.

## 5. Research program by field

### 5.1 Formation and intellectual biography

Questions:

- How did drawing, drumming, design education, and the MIT Aesthetics and Computation Group shape Reas's sense of score, rhythm, tool, and visual behavior?
- What did John Maeda's environment make possible, and where did Reas diverge from information design toward autonomous art?
- How did teaching at Ivrea and UCLA affect the relation between explanation, notation, and public access in the work?
- How do book design, writing, and publishing function as artistic methods rather than ancillary documentation?

Primary sources: artist information and books archives; UCLA; MIT/ACG records; Processing histories; Reas/Fry's 2006 *AI & Society* article; Rhizome's 2009 Processing interview; artist lectures and interviews.

### 5.2 Genealogies

The writing will establish affinities and differences, not produce a list of names.

- **Instruction and score:** Sol LeWitt, John Cage, conceptual notation, delegated realization, and the difference between human interpretation and machine execution.
- **Systems and cybernetics:** Jack Burnham, systems aesthetics, artificial life, feedback, emergence, and Reas's insistence on perceptible local rules.
- **Early computer and plotter art:** Georg Nees, Frieder Nake, Vera Molnár, Manfred Mohr, and the distinction between offline plotted calculation and continuous real-time software.
- **Modernist and kinetic abstraction:** Ellsworth Kelly, Max Bill, Jesús Rafael Soto, George Rickey, Victor Vasarely, seriality, permutation, optical activation, and movement.
- **Experimental film and image systems:** Stan Brakhage, Ken Jacobs, montage, found footage, compression, and the movement from source image to machine-generated memory.
- **Software culture:** open source, Processing, p5.js, software studies, and the material/institutional conditions of executable art.

### 5.3 Practice chronology

The monograph will not jump directly from early Process to Art Blocks. It will give appropriate weight to:

1. Path, Tissue, and MicroImage, 2001-2004;
2. {Software} Structures and Process, 2004-2014;
3. Processing, teaching, and publication as continuous parallel practice;
4. Signal to Noise and Ultraconcentrated, from 2012;
5. Atomism, RGB/HSB, and Still Life, from 2012/2016;
6. Compressed Cinema and machine-learning work, 2018-2023;
7. a2p, Feral File, and networked exhibition, from 2019/2020;
8. CENTURY and Phototaxis, 2021;
9. Pre-Process, 2022;
10. An Empty Room and 923 EMPTY ROOMS, 2023;
11. There Is No Distance, Purely Platonic, In Silico, METACENTURY/METAJUDD, and other recent work through 2026;
12. Ex Nihilo (Cosmos), 2026.

### 5.4 Reception and institutional history

The text must distinguish an exhibition list from reception. It will use museum acquisitions and exhibitions to show how institutions have classified, displayed, and preserved the work; serious criticism to register disagreement and perceptual response; and publications to trace how Reas frames his own practice. Required institutional anchors include the Whitney, LACMA, Centre Pompidou, SFMOMA, V&A, Toledo Museum of Art, bitforms, DAM Projects, and Feral File.

## 6. Project-specific research and argument

### 6.1 CENTURY

Argument to test: CENTURY does not apply a modernist look to software. It extracts operations from twentieth-century abstraction—cutting, serial variation, optical vibration, recombination, kinetic change—and exposes how historical form behaves when it becomes executable and distributable.

Required distinctions:

- the wider CENTURY body begun in 2012 versus the 2021 Art Blocks project;
- reference versus imitation in relation to Kelly, Rickey, Soto, and Max Bill;
- circle/oculus, line, slice, palette, and movement as compositional operations;
- token-specific base state versus viewer-triggered recomposition;
- the three Museum works as contrasting states: density and interruption (#31), openness and suspension (#724), and tonal opacity/depth (#401).

### 6.2 Process and Pre-Process

Argument to test: Process relocates authorship from the placement of marks to the construction of relations, while Pre-Process makes the archaeology of that relocation visible. Its 2022 completion is not a retroactive origin myth but an artist-led return to an unresolved 2003 grammar.

Required distinctions:

- natural-language instruction, source code, execution, image, print, and installation;
- LeWitt's humanly interpreted instruction versus software's exact but materially contingent execution;
- Process as mature method versus Pre-Process as recovered precursor;
- the 8 × 3 × 5 edition structure as an exhaustive permutation of selected axes, not a rarity hierarchy;
- #63's panoramic, three-register field, circular masses, axial bands, and accumulated translucent collisions.

### 6.3 MicroImage and Phototaxis

Argument to test: Phototaxis is simultaneously an artwork, a code migration, and a twenty-year retrospective instrument. It turns behavior into trace and allows the Museum to see continuity at the level of a system while display, language, and circulation change.

Required distinctions:

- Braitenberg's thought experiments versus Reas's visual and temporal composition;
- simulated entity versus accumulated path;
- live behavior versus the canonical 1,000-iteration image;
- C++ / Processing-Java / p5.js migration as historical evidence;
- #308's cyan outer circulation, dark central knot, upper convergence, and escaping vertical paths.

### 6.4 Atomism and 923 EMPTY ROOMS

Argument to test: Reas converts Vasarely's unbuilt combinatorial environment into a distributed software exhibition, shifting the "room" from architectural enclosure to a relation among colorforms, code, cities, screens, and viewers.

Required distinctions:

- Atomism's pixel/unit logic;
- Vasarely's unrealized LACMA proposal, Reas's An Empty Room, and the later 923 project;
- six colorforms, six cities, combination-with-replacement logic, 923 enumerated rooms, and the 924-entry release structure;
- combinatorial position versus commercial rarity;
- #713's CDMX association and exact `555536` composition without hidden-symbolic inference;
- the static image's lime diagonal raster, charcoal architectural void, luminous right-hand seam, and unstable recession.

### 6.5 Still Life and Ex Nihilo

Argument to test: Reas's Still Life works stage an exact mathematical object inside unstable technical time. The Platonic solid supplies ideal definition; pixels, color channels, shaders, screens, and continuous execution make that ideal contingent and perceptually incomplete.

Required distinctions:

- RGB/HSB technical color models as visible structures;
- still-life genre, software painting, and the contradiction of a continuously changing "still";
- screen, projection, plotter drawing, print, and tokenized edition as related but non-equivalent manifestations;
- 2016 Still Life works, There Is No Distance, An Empty Room, Purely Platonic, and Ex Nihilo chronology;
- #248's black field, segmented white traces, unstable dodecahedral implication, layered depth, and refusal of a settled object.

## 7. Object close-looking protocol

Each object entry must be written from the exact official token still plus the recorded live observation and project behavior. The entry must move through five layers:

1. **First encounter:** what the eye meets before metadata.
2. **Formal organization:** palette, scale, density, figure/field, rhythm, direction, edge, depth, and the distribution of attention.
3. **Temporal behavior:** what changes, accumulates, recomposes, pauses, or continues, with no claim beyond observed or documented behavior.
4. **Project relation:** how the token makes the larger system legible without being reduced to its traits.
5. **Collection role:** why this exact object matters inside the seven-work group.

No entry may use a project feature label as a substitute for looking. No entry may praise an output because a trait is uncommon. No entry may describe a still as the complete artwork.

## 8. Gift and accession narrative questions

The gift narrative is not a legal instrument and will not repeat the accession certificate in prose. It must answer:

- What kind of artistic history became public through this gift?
- Why is a seven-work, five-project group more useful than a single trophy token?
- What does the three-work CENTURY comparison enable?
- How does the group connect 2001/2003 systems to 2026 work without pretending to be a retrospective?
- What is known about the donor's act, and what donor motives are not documented?
- What changes when privately held tokens enter a permanent public-trust collection?
- Why is this gift institutionally significant as the Museum's first completed accession package?
- What obligations—display, interpretation, rights compliance, preservation, and public access—does acceptance create?

The text may call the gift foundational because it is the Museum's first completed accession package and establishes a substantive collecting direction. It may not call it the artist's canonical group, the donor's definitive selection, or a complete survey.

## 9. Source hierarchy

### Tier 1: primary and official

- Casey Reas's current site and gray archive;
- artist books, lectures, technical notes, and project records;
- Whitney artport and *Programmed* materials;
- LACMA project records and interviews;
- UCLA and MIT/ACG records;
- Processing and Processing Foundation records;
- Reas/Fry's published Processing scholarship;
- Art Blocks artist interviews, project pages, official metadata, scripts, and generator records;
- Feral File institutional and exhibition records;
- bitforms and DAM Projects exhibition records;
- official museum collection and exhibition pages;
- the Museum's retained chain, metadata, technical, visual, rights, and accession evidence.

### Tier 2: serious scholarship and criticism

- Christiane Paul's writing on digital art, software art, and *Programmed*;
- Nora N. Khan's 2016 Still Life review and her introduction to *Making Pictures with Generative Adversarial Networks*;
- Meredith Hoy's "Painting as Programming";
- peer-reviewed writing on Processing, software art, generative systems, and Reas;
- exhibition catalogues and books on computational, systems, and conceptual art;
- primary historical texts by LeWitt, Burnham, Cage, Braitenberg, and relevant artists where the genealogy depends on them.

### Tier 3: contextual reporting

Reputable interviews and arts reporting may supply reception or context, but not sole support for identity, chronology, technical behavior, or artist intent.

Marketplace copy, auction promotion, unsourced collector commentary, rarity sites, and generic generated biographies are inadmissible as factual authority.

## 10. Notes and attribution method

The body text should read as an essay, not a deposition. Superscript-style numbered notes or Markdown endnote links will carry factual attribution. Interpretive claims will be signaled through syntax and argument, not repeated `[E]` labels. The label system remains in machine and research records where it is useful.

Each publication will include:

- a short standfirst;
- authoring/version/date metadata;
- a note explaining its relation to the accession control record;
- numbered notes or a shared notes map;
- selected bibliography;
- a research cutoff date;
- links to the technical, rights, provenance, and source record layers.

Quotations will be sparse and exact. The writing should paraphrase sources unless an artist's wording is itself historically or conceptually necessary.

## 11. Versioning and supersession

The first finished publication release is `version: 2.0.0` relative to the existing accession research summaries.

- `casey-reas-monograph.md` supersedes `public/casey-reas-artist-practice.md` **for visitor-facing artist interpretation only**.
- `the-system-in-seven-states.md` supersedes `public/casey-reas-collection-essay.md` **for visitor-facing collection interpretation only**.
- each new object entry supersedes the corresponding root-level object page **for extended curatorial interpretation only**.
- the gift narrative supplements, but does not supersede, `gift-acceptance-authorization.md`, `accession-certificate.md`, or the machine records.
- project essays are new publication objects and do not supersede control records.

The historical files remain in Git and in the release history. Once the new manuscripts are complete, the old pages will receive a short dated notice and link forward; their historical text will not be silently rewritten.

## 12. Editorial production sequence

### Phase A — evidence and image lock

- confirm exact seven-object identity table;
- retain the current public source list and add missing primary/critical sources;
- inspect the exact official still for each object;
- inspect live behavior where safe and necessary;
- build a fact/interpretation/source matrix and chronology.

**Exit test:** every factual claim planned for the prose has a source; every visual claim names the exact object and observation basis.

### Phase B — project essays

Write the five project essays first. They are the research engine for the monograph and object entries.

**Exit test:** each essay has a distinct argument, sustained close readings, historical context, project chronology, exact relation to the represented object(s), and notes.

### Phase C — object entries

Write all seven entries from the close-looking notes and finished project research.

**Exit test:** deleting the title and token metadata would not make the seven entries interchangeable.

### Phase D — seven-work and gift essays

Write the collection argument and institutional narrative only after the project/object work is stable.

**Exit test:** the group essay explains why these seven objects form a useful Museum argument; the gift essay explains why the transfer into public trust matters without inventing donor motive.

### Phase E — monograph

Synthesize the full practice at career scale, incorporating but not repeating the project essays.

**Exit test:** the monograph has a contestable thesis, complete chronology, serious genealogy, perceptual criticism, reception, and a conclusion that changes how the Museum's seven works are understood.

### Phase F — editorial and factual review

Run separate passes for:

1. argument and structure;
2. close-looking specificity;
3. chronology and names;
4. technical accuracy;
5. citation completeness;
6. prose rhythm, repetition, and generic language;
7. rights and public-record safety;
8. cross-file consistency.

**Exit test:** no paragraph exists mainly to announce process, governance, future review, or evidence caution; supporting caveats appear only where they change the interpretation.

### Phase G — publication integration

- add the new files to `INDEX.md`;
- add forward links from historical summaries;
- expose typed artist, project, story, and object-publication records for the frontend;
- generate the governed release manifest;
- run complete Museum validation;
- visually verify the rendered web pages when the frontend adapter is ready.

## 13. Acceptance rubric

Each finished publication must pass all of the following:

| Dimension | Pass condition |
|---|---|
| Argument | A reader can state the publication's specific claim in one or two sentences. |
| Art history | Genealogies explain transformation and difference, not resemblance alone. |
| Close looking | Formal observations are exact enough to distinguish this work from siblings. |
| Medium | Code, screen, print, installation, token, and documentation are treated as materially specific. |
| Chronology | The practice does not leap from Processing to NFTs or stop before current work. |
| Biography | Life and institution-building are included only where they illuminate artistic decisions. |
| Reception | The writing registers criticism, difficulty, and disagreement rather than becoming celebratory biography. |
| Evidence | Facts are sourced in notes; prose remains readable and confident. |
| Collection logic | The exact Museum objects are integral to the argument, not appended as examples. |
| Prose | No generic computational-art paragraph could be moved unchanged to another artist. |
| Public trust | The gift and accession are interpreted without overclaiming title, rights, motive, or institutional completion. |

## 14. Current close-looking record

On 2026-08-02 the lane retrieved the exact official Art Blocks static output for all seven tokens into a temporary, untracked research directory and inspected them at original resolution. These are later research observations, not the non-retained 2026-08-01 accession screenshots.

- **CENTURY #31:** a circular field dominated by slate, saturated blue, and cream; dense vertical splices interrupt diagonal cream and pale-salmon lines; large curved cream forms are partly buried by the slicing structure.
- **CENTURY #724:** a markedly open cream field; rust-red arcs and upper bands hang around broad negative space; sparse charcoal and salmon diagonals make the composition feel suspended rather than crowded.
- **CENTURY #401:** a grayscale field of gray planes, black vertical columns, white diagonals, and translucent circular/arc forms; slicing reads as both surface interruption and shallow architectural depth.
- **Pre-Process #63:** a panoramic black-and-white field in three horizontal registers; dark circular masses lock to axial bands while repeated translucent arcs record collision, passage, and accumulation.
- **Phototaxis #308:** pale-cyan and gray trajectories form an outer elliptical circulation around a dense central knot; a second convergence appears near the upper center while long paths escape beyond the field.
- **923 EMPTY ROOMS #713:** acid-green diagonal marks cover the field but break around charcoal voids that imply a cornered room; a luminous vertical seam at right and a bright lower ledge make the space recede and pulse simultaneously.
- **Ex Nihilo (Cosmos) #248:** segmented white traces cross a black ground in unstable polygonal and dodecahedral suggestions; interruptions and changes of scale create layered depth without allowing a stable solid to settle.

These notes are starting observations. The object entries must test them against live behavior, project instructions, and comparison within each edition.

## 15. Lead-editor lane status and next actions

Completed in this lane:

1. reusable Museum curatorial-publication standard;
2. shared source, chronology, object-identity, and factual-boundary matrix;
3. 12,000-plus-word artist monograph with standfirst, notes, and bibliography;
4. independent seven-work collection essay with exact object schedule, notes, and bibliography;
5. gift and accession narrative with exact delivery, acceptance, title, rights, condition, and public-trust boundaries;
6. internal footnote, encoding, object-identity, and unsupported-claim audit.

Next actions are editorial integration, not fresh first drafting:

1. receive the five project essays and seven object entries from their assigned lanes;
2. reconcile chronology, terminology, repeated passages, and source corrections against the shared matrix;
3. select publication cuts without reducing live works to static outputs;
4. move approved manuscripts from WIP to their final versioned public paths through a separate governed change;
5. update `INDEX.md` and the release manifest only in that integration change, then run complete validation and website QA.

This plan is the durable handoff. It must be updated when a factual boundary changes, another lane returns a material correction, or integration creates a new publication version.
