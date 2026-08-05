# The project is the permanent home

## Recommendation

The Museum should publish each generative-system analysis as a living project
study, not as part of a gift, accession, or individual object record.

The public model is simple:

- the **project page** explains the system;
- the **object page** explains where this output sits within the system;
- the **gift or acquisition page** explains why these particular works entered
  the Museum together;
- **Stories and Research** helps visitors discover the studies but does not own
  them.

This is the only structure that remains coherent when the Museum later acquires
another work from the same project. The new work joins the existing project
study, receives its own object reading, and adds evidence to the project map.
The original gift remains an intact historical account of one acquisition.

## The visitor experience

The series should have a clear public name: **Inside the System**.

Every study begins with art and one strong proposition. A visitor should not
meet a schema, methodology note, technical glossary, or research-status warning
before understanding what kind of image the project makes.

The ideal route family is:

```text
/museum/network/projects/[project-slug]
/museum/network/projects/[project-slug]/system
/museum/network/collection/[object-id]
/museum/network/gifts/[accession-id]
/museum/network/stories
```

The project root is the durable hub. The `/system` child is the immersive study.
It should carry a visible **Inside the System** label and remain visibly inside
the project rather than feeling like a detached microsite.

### Project hub

`/museum/network/projects/[project-slug]` should answer three questions quickly:

1. What is this project?
2. What does its system make possible?
3. Which works from it does the Museum hold?

Recommended order:

1. a large artwork encounter or carefully chosen project sequence;
2. project title, artist, date, platform, and a 40- to 80-word thesis;
3. one primary action: **Enter the system**;
4. all Museum-held works from the project, generated from current collection
   relationships rather than a gift-specific list;
5. the existing project essay and artist statement;
6. related stories, acquisitions, and sources.

The project page should not embed the full research dossier. Its job is to make
the project legible and invite the deeper encounter.

### Inside the System

`/museum/network/projects/[project-slug]/system` should be an interactive essay,
not a long Markdown page with diagrams inserted between paragraphs.

Recommended chapter sequence:

1. **What kind of image is this?**  
   A project-specific proposition and a meaningful live or documented visual.
2. **Follow one cause.**  
   A short visual sequence showing how one authored decision becomes one
   perceptible consequence.
3. **See the field.**  
   The possibility-space visualizer: the project as a finite, sampled, or
   dynamic field, with Museum works clearly located inside it.
4. **Compare the Museum works.**  
   Synchronized or side-by-side comparison where the collection contains more
   than one work from the project.
5. **Read the score.**  
   An intelligible account of initialization, state transition, time,
   interaction, and render pipeline.
6. **Look again.**  
   Exact-output close readings that return the technical understanding to the
   art.
7. **Methods and evidence.**  
   Sources, claims, uncertainty, reproducibility, rights, conservation, and
   machine-readable downloads at the end.

This creates progressive depth without dividing the audience into “simple” and
“expert” modes. Everyone encounters the same argument; deeper layers are simply
available when wanted.

## The possibility-space visualizer

The visualizer is the distinctive digital-museum contribution. It should show
the relationship between a project’s authored field and a particular output,
not simulate a marketplace rarity dashboard.

Its public question is:

> What did the system make possible, and where does this work stand within it?

### Four honest map types

One generic scatterplot will not work across generative art. The publication
model should support four map types:

| Map type | Use when | Public form |
|---|---|---|
| Exhaustive lattice | Every combination is known | Complete grid or small multiples |
| Finite combinatorial field | The universe is known but not naturally rectangular | Grouped constellation, matrix, or topology |
| Sampled field | The edition is observed but the generative possibility space is larger or only partly reconstructed | Explicitly labeled edition sample with coverage statement |
| Dynamic state space | Time and interaction matter more than static features | Trace, timeline, or state-transition view |

The map must never imply completeness when the Museum has only sampled the
edition or observed a few runs. “All outputs,” “observed edition,” “reviewed
sample,” and “possible runtime states” are different claims and need different
labels.

### Museum-held works

Museum works should be overlaid as a relationship layer, not baked into the
definition of the project field. A marker should expose:

- title and token identity;
- Museum object ID when held;
- the structural coordinates that place it there;
- the evidence basis for those coordinates;
- a short statement of what the work contributes to understanding the project;
- a link to the object page.

When another work is accessioned, the project field does not change merely
because Museum ownership changed. A new Museum marker and object reading are
added. If the new work reveals a previously unrecognized behavior, the study is
revised as scholarship and the revision is recorded.

### No false axes

Axes must correspond to authored or reconstructed system variables, temporal
behavior, or clearly documented visual consequences. The interface must not
invent aesthetic scores, quality rankings, desirability measures, or proxy
rarity. Trait prevalence remains a separate, method-bound descriptor.

## What appears on an object page

Immediately after the artwork viewer and concise Museum label, each generative
object page should contain a compact **In the system** module.

It should include:

- a miniature view of the relevant project field;
- the work’s highlighted position or path;
- two or three exact causal coordinates in plain language;
- one sentence explaining what is distinctive about this output without
  converting difference into rank;
- a deep link to the full study, focused on this object;
- links to other Museum-held works from the project.

The deep link should be stable and citeable, for example:

```text
/museum/network/projects/century/system#6529NM.2026.001.01
```

The object page remains the place for accession, provenance, rights, and
preservation detail. The project study should not duplicate those records.

## What appears on a gift page

The Casey gift page should gain a visual section titled **Five projects, seven
works**. It should show the five project propositions and link to each project
study. The comparative Casey essay belongs here because it interprets the
donor’s seven-work selection as a group.

The individual algorithm dossiers do not belong here. Otherwise later Museum
acquisitions from the same project would be forced into the history of a gift
through which they did not enter.

## Discovery across the Museum

Stories and Research should feature **Inside the System** as an editorial
series. This is the directory for browsing studies across artists and projects.
It can also host commissioned essays about generative methods, but the canonical
study URL remains under the project.

The Museum home can feature one current study below the primary collection
story. It should not gain a new top-level navigation item until the series is
large enough to justify one; the existing **Stories & Research** and project
paths are sufficient for launch.

The artist page should list system studies beside the relevant projects. The
collection index should not add badges to every card; the object page is the
cleaner entry into token-specific analysis.

## Casey launch treatments

The five Casey studies should share an interaction grammar without forcing the
same diagram onto unlike systems.

### CENTURY

- Open with the three Museum works as three manifestations of mutable
  adjacency.
- Let the visitor compare a shared structural layer across #31, #724, and #401.
- Show fixed token-derived conditions separately from continuing slice state.
- Use an observed-edition or reviewed-sample field unless exhaustive
  reconstruction is independently established.
- This is the strongest demonstration of how multiple Museum works make one
  project study richer.

### Pre-Process

- Make the exact `8 × 3 × 5 = 120` edition the first complete possibility-space
  visualizer.
- Use Surface, Origin, and Growth as the three authored coordinates.
- Highlight #63 and allow the visitor to hold two coordinates constant while
  moving through the third.
- This is the best first production pilot because the complete topology is
  finite, visually intelligible, and already reconstructed.

### Phototaxis

- Treat the field as a history of sensing rather than a set of static traits.
- Reveal light positions, sensor readings, vehicle response, and accumulated
  path in successive layers.
- Offer a static trace and keyboard-operable step sequence in addition to motion.
- Locate #308 through its fixed light/population conditions and its evolving
  encounter history.

### 923 EMPTY ROOMS

- Present the 923-room combinatorial topology as a complete field.
- Let the visitor follow one room from colorform selection through RGB
  displacement to line-built space.
- Highlight #713 and show that its room is one position in an exhaustive formal
  vocabulary, not a rarity tier.

### Ex Nihilo (Cosmos)

- Move from solid geometry to edges, temporal memory, channel displacement, and
  line field.
- Use a time view as well as an edition view because feedback is constitutive.
- Highlight #248 in the reviewed finite population while keeping unresolved
  feature-semantic mappings in the evidence layer.

## Responsive and accessible behavior

The current Museum is dark, restrained, art-led, and built inside the 6529
shell. The studies should extend that language rather than introduce a bright
data-visualization product or a detached microsite.

Desktop can use a quiet chapter rail and wide visual field. Mobile should turn
the same chapters into a linear story: art, proposition, one causal sequence,
the selected work, then the wider field. Dense plots should become grouped
small multiples or a searchable list instead of a pinched scatterplot.

Every visualizer requires:

- a keyboard and touch path that does not depend on dragging;
- a structured list or table alternative containing the same claims;
- visible focus and at least 44-pixel controls;
- shape and text labels in addition to color for Museum-held works;
- static and reduced-motion presentations;
- useful alt text and a concise textual finding;
- URL-addressable selected work and view state;
- clear loading, unavailable, partial-data, and recovery states;
- no horizontal page overflow at mobile widths.

## Publication and frontend model

The current frontend already has durable project, artwork, gift, and public
document entities. The minimum safe extension is:

1. add a project-linked public document kind such as
   `generative_system_study`;
2. add a typed project-analysis entity for structured chapters and visualizer
   configuration rather than parsing arbitrary Markdown conventions;
3. add a separately versioned possibility-space dataset whose rows describe
   project outputs or states without pretending those rows are Museum artworks;
4. relate Museum object IDs to dataset subjects only when the identity match is
   exact;
5. keep study revisions independent from acquisition events.

An indicative shape is:

```ts
interface MuseumGenerativeSystemStudy {
  id: string;
  projectId: string;
  documentId: string;
  mapKind:
    | "exhaustive_lattice"
    | "finite_combinatorial"
    | "sampled_field"
    | "dynamic_state";
  datasetId: string;
  coverageStatement: string;
  highlightedObjectIds: readonly string[];
  revisedAt: string;
}
```

The full project universe must not be represented as `MuseumArtwork[]`.
Non-held outputs are research subjects in the possibility-space dataset;
accessioned works remain the only collection objects.

## Recommended build sequence

1. Publish the art-first project study route and typed content model.
2. Add the compact **In the system** module to object pages and the five-project
   link section to the Casey gift.
3. Build *Pre-Process* as the first complete possibility-space visualizer.
4. Build the three-work *CENTURY* comparison as the first multi-holding study.
5. Add *923 EMPTY ROOMS*, then the more time-dependent *Phototaxis* and *Ex
   Nihilo (Cosmos)* experiences.
6. Launch the cross-project **Inside the System** directory in Stories and
   Research after at least two studies provide a credible public series.

## Study basis and open work

This recommendation was developed against the live Museum home at desktop and
390-pixel mobile widths, the current frontend project/object/gift/story routes,
the Museum public-experience standard, and the five constructed Casey system
dossiers. The live home already establishes the right art-first tone; the
project and object models already provide the correct semantic anchors.

Before a visualizer is published, the Museum still needs a reviewed output
snapshot or deterministic reconstruction, a declared coverage statement,
rights review for derived analytical media, accessibility review, and a stable
machine-readable dataset commitment. Those requirements belong in the final
chapter and source layer, not in the visitor’s opening encounter.

## Implementation checkpoint

The complete review candidate now exists in `C:\w\museum-inside-system-fe` on
branch `codex/museum-inside-system`, based on frontend `origin/main` commit
`aa77ddf836c3c83cc680054e40247f7e4a78a18d`. It implements the project route,
all five Casey study pages, four reusable possibility-space map types, exact
accession overlays and shareable selection, semantic table alternatives,
object-page position modules, the gift directory, and the Stories/Research
series entry.

The public reading order is thesis, map, algorithm, held works, finding, then
method and limitations. *Pre-Process* is exhaustive; the other studies use the
strongest evidence-honest form their current research supports and do not fake
precision with generic scatterplots. A later acquisition can extend the
project-owned `heldPositions` overlay without becoming part of the historical
gift.

Formatting, changed-file typecheck and lint, 23 focused tests, React Doctor
100/100, production build, desktop browser review, keyboard navigation, and
horizontal-overflow checks pass. The branch is not committed, pushed, merged,
deployed, or adopted. The remaining publication-engineering work is to promote
the bundled constructed studies into optional atomic remote-publication groups
and replace the frontend's exact-seven Casey overlay assumption before later
Casey acquisitions are published.

## Comparison instrument checkpoint

The visualizer has advanced from a map of Museum positions into a reusable
side-by-side project instrument. The Museum accession remains fixed at left.
The right side can now show any minted project output by invocation or token
ID, a deterministic random minted output, a random output matching a published
trait filter, or a project-specific counterfactual/session manifestation.

This interaction contract is reusable across generative projects while the
visual grammar remains specific to each system:

- *CENTURY* reconstructs the ellipse, band, slice, and adjacency logic as a
  pair of circular moving-image surrogates with palette, band, slice, Janky,
  and Alpha controls;
- *Pre-Process* joins the complete 120-position starting-condition lattice to
  paired collision chambers;
- *Phototaxis* compares accumulated behavioral traces and can reveal active
  lights, sensing, wiring, steering, motion, brightness, and trace layers;
- *923 EMPTY ROOMS* joins the complete 923-node form grammar to a line-built
  room manifestation;
- *Ex Nihilo (Cosmos)* joins a 256-state edition atlas to paired displaced
  geometric memory fields.

The frontend includes compact generated indexes for every minted work in the
five projects: 1,000 *CENTURY*, 120 *Pre-Process*, 1,000 *Phototaxis*, 923
*923 EMPTY ROOMS*, and 256 *Ex Nihilo (Cosmos)* records. Each index retains the
invocation, token ID, token hash, official still URL, published traits, pinned
snapshot identity, and observation time required for lookup and comparison.
It is derived from the complete governed evidence snapshots rather than a
marketplace API.

Suggested comparisons are deterministic and project-relative: closest shared
published traits, strongest contrast in published traits, and the largest sum
of low-prevalence published trait values. The last label is **structurally
uncommon**, not "rare," and the interface explicitly rejects marketplace
rarity scores and desirability rankings.

Counterfactual language is also project-relative. For sampled fields such as
*CENTURY* and *Phototaxis*, the control surface can describe an unminted
analytical state. Where the authored starting composition was exhaustively
minted, as in *Pre-Process* and *923 EMPTY ROOMS*, the controls are labeled as
a new session or presentation manifestation and do not imply that an unminted
composition exists.

The implementation remains a local review candidate in
`C:\w\museum-inside-system-fe`. It is uncommitted, unpushed, unmerged,
undeployed, and not artist-approved or Museum-adopted. The principal remaining
publication gate is to move the pinned project indexes and study definitions
behind the Museum's governed optional atomic project-study envelope rather than
treating the frontend bundle as the durable source of record.

## Release-boundary amendment

This section supersedes the release-gate paragraph immediately above. The
version 1 frontend may publish the study definitions and 3,300-record compact
index as a versioned derived display package. Canonical evidence remains in the
Museum repository's pinned snapshots, reviewed descriptors, and Casey project
dossiers. The display package neither changes accession records nor claims
artist approval or governance adoption.

The release conditions are: official artwork before analytical diagrams;
persistent **Museum model** labels on generated views; complete snapshot-backed
minted lookup; reviewed NextGen-compatible analysis for **less often seen**;
and no marketplace rarity, desirability, or value claims. Optional atomic
project-study records remain the future interoperability target, not a blocker
for this display-layer release.

## Production release — 2026-08-05

**Inside the System** is live as a project-owned Museum instrument for all five
Casey Reas projects in accession `6529NM.2026.001`:

- [CENTURY](https://6529.io/museum/network/projects/century/system)
- [Pre-Process](https://6529.io/museum/network/projects/pre-process/system)
- [Phototaxis](https://6529.io/museum/network/projects/phototaxis/system)
- [923 EMPTY ROOMS](https://6529.io/museum/network/projects/923-empty-rooms/system)
- [Ex Nihilo (Cosmos)](https://6529.io/museum/network/projects/ex-nihilo-cosmos/system)

Frontend PR
[`#3594`](https://github.com/6529-Collections/6529seize-frontend/pull/3594)
introduced the five studies and merged as
`5b03302719b306b29582d43f6910fd1a843de1f7`. Follow-up PR
[`#3602`](https://github.com/6529-Collections/6529seize-frontend/pull/3602)
made the deployed Museum checks tolerate two exact, known shell-level fetch
diagnostics without weakening route, content, media, layout, response, or
unexpected-console assertions. Production revision
`a36a5a437e68d03c886471caefe0bf01afc3827c` contains both changes.

The released comparison contract fixes a Museum-held work at left. At right, a
visitor can retrieve any minted work by invocation or token ID, filter the
complete edition snapshot, request deterministic structural neighbors,
complements, or less-often-seen examples, or explore a clearly labeled
project-specific Museum model. The five projects keep distinct visual and
algorithmic grammars rather than collapsing into one generic chart. The
display package indexes all 3,300 minted outputs represented by the governed
snapshots, including invocation 0 in *923 EMPTY ROOMS*.

Three independent adversarial reviews tested the release for editorial voice
and LLM smell, museum-design quality, and collector interest. All three
returned **SHIP** after iteration. The frontend PR's required quality,
security, accessibility, internationalization, and Museum checks also passed.

Release evidence is exact and environment-bound:

- staging deployment
  [`30977518490`](https://github.com/6529-Collections/6529seize-frontend/actions/runs/30977518490)
  and staging E2E
  [`30978079115`](https://github.com/6529-Collections/6529seize-frontend/actions/runs/30978079115):
  all 14 read-only packs passed, including 70 institutional-practice and 8
  Inside the System desktop/mobile tests;
- production artifact
  [`30977459534`](https://github.com/6529-Collections/6529seize-frontend/actions/runs/30977459534),
  production deployment
  [`30978958753`](https://github.com/6529-Collections/6529seize-frontend/actions/runs/30978958753),
  and production E2E
  [`30979315540`](https://github.com/6529-Collections/6529seize-frontend/actions/runs/30979315540):
  all 13 read-only packs passed, including 70 institutional-practice and 8
  Inside the System desktop/mobile tests. The deployed `/api/version` matched
  the exact production revision.

The permanent content model remains the one recommended above: scholarship is
owned by the project; an object is located within that continuing study; a
gift records why a particular group entered together. A later accession from
one of these projects therefore adds a held-work position and object reading
without being rewritten into the Casey gift or changing the project field.
