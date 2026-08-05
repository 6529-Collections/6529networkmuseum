# Generative Systems Analysis Standard: Casey Reas pilot

- **Status:** WIP analysis and design proposal; not adopted policy
- **Opened:** 2026-08-04
- **Pilot accession:** `6529NM.2026.001`
- **Pilot scope:** *CENTURY*, *Pre-Process*, *Phototaxis*, *923 EMPTY ROOMS*, and *Ex Nihilo (Cosmos)*
- **Larger scope:** a reusable Museum standard for the study, publication, exhibition, and preservation of generative art collections
- **Relationship to existing work:** complements the curatorial-publication standard, object and condition records, and NextGen-compatible trait-prevalence analysis; it does not replace or merge those layers

## 1. The ambition

The Museum should make the algorithm available as an artwork-level subject of
close reading. A visitor should be able to understand what the system does, a
scholar should be able to argue why those operations matter, and a conservator
should be able to reproduce the factual basis from pinned source and observed
behavior.

This requires more than a technical appendix and more than a trait table. The
standard should join three disciplines without collapsing them:

1. **algorithmic forensics** reconstructs source, seed, state, update rules,
   rendering, interaction, dependencies, and environmental variation;
2. **collection analysis** explains the authored possibility space, the
   released population, and the position of an exact Museum object without
   turning prevalence into quality or value;
3. **curatorial interpretation** asks what those operations do aesthetically,
   historically, materially, and politically.

The public result should let a person move from code to behavior to form and
back again. It must also preserve the remainder: an artwork is not exhausted
when its procedure can be explained.

## 2. The governing distinction

The existing NextGen-compatible method answers a narrow, useful question:
**how prevalent is a published metadata trait in the observed edition?** It is
descriptive technical evidence and never a measure of quality, importance, or
value.

The proposed standard answers a different question:
**how does this authored system transform an identity-bearing input into a
field of possible experiences, and what is at stake in those transformations?**

The two layers may meet in a publication, but neither may impersonate the
other. Trait prevalence begins with published labels. Algorithmic analysis
begins with the constitutive system. A label such as `Growth 4`, `Janky`, or
`# COSMOS: 3` is an observation to explain, not an interpretation.

## 3. Required model: from genotype to encounter

Every generative collection should be analyzed through six linked but distinct
states.

| State | Question | Examples |
|---|---|---|
| Identity | What exact work and algorithm version are being discussed? | contract, project, token, invocation, token hash, source hash, dependency |
| Genotype | What fixed inputs and authored probabilities define the work? | seed material, token index, feature assignment, palette and population rules |
| Initial phenotype | What state is produced at initialization or at the platform's designated reference moment? | base composition, first frame, 1,000-iteration thumbnail |
| Performance | How does the work change through time without viewer action? | motion, collision, accumulation, feedback, shader transformation |
| Participation | What state changes can a viewer cause, and which of them persist? | cut, reset, pause, channel toggle, new state, diagram view |
| Encounter | How do viewport, browser, GPU, screen, duration, and exhibition alter the manifestation? | aspect ratio, pixel density, frame rate, black level, projection scale |

This vocabulary prevents several common errors. A token hash is not the whole
algorithm. A platform thumbnail is not necessarily the initial state or the
complete work. A viewer-triggered state is not automatically a new canonical
token state. A screenshot is a documentation surrogate. A deterministic seed
does not by itself prove pixel-identical output across environments.

## 4. Evidence grammar

Every material claim should retain the repository's A-E evidence class and add
a non-normative method qualifier. The qualifiers do not redefine the existing
classes and should remain versioned inside this analysis profile.

| Qualifier | Meaning |
|---|---|
| `source_static` | derived by reading pinned constitutive source without executing it |
| `source_formal` | proved from code, combinatorics, or a mathematical model |
| `execution_observed` | observed in a named runtime and environment |
| `execution_instrumented` | emitted by a trace-enabled reproduction of the pinned program |
| `population_empirical` | measured across a pinned complete or declared edition snapshot |
| `artist_statement` | stated by the artist or authorized project source |
| `museum_interpretation` | a supported but revisable curatorial argument |

Code comments, metadata labels, artist statements, source behavior, and Museum
interpretation may disagree. The dossier should display the disagreement rather
than silently choose one. A claim such as "non-repeating" should say whether it
is artist-stated, mathematically established, or only not observed to repeat
inside a bounded run.

## 5. Required algorithm dossier

Each project dossier should contain the following.

### 5.1 Source and dependency lock

- exact collection, contract, project, token, and invocation identities;
- exact source-retrieval URI, observation time, response-byte hash, extracted
  script hash, dependency names and versions, and rights/retention status;
- distinction among on-chain source, generator assembly, feature script,
  platform wrapper, and external dependency;
- a reproducible path from retained bytes or on-chain chunks to executable
  source, with no claim of preservation completion when bytes are not retained.

### 5.2 Randomness and parameter provenance

- exact seed material and any truncation, parsing, numeric coercion, warm-up,
  stream alternation, or token-index contribution;
- PRNG family and state size;
- ordered random-call trace from seed to named parameter;
- authored probability table alongside the empirical edition distribution;
- explicit identification of traits assigned exhaustively, probabilistically,
  by token index, or by later session state.

The central public artifact should be a **parameter provenance graph**. It
should let a reader follow `token hash -> PRNG call -> parameter -> behavior ->
visible consequence` without implying that the graph explains the artwork
away.

### 5.3 Algorithmic score

- concise pseudocode in the order the system executes;
- state-variable glossary with units and valid ranges;
- equations for update rules, transforms, sensor functions, collision rules,
  shader mappings, and compositing;
- state-machine or pipeline diagram;
- a readable annotated-source companion where rights permit publication;
- an explicit list of dormant, unreachable, or interface-only code paths.

The score is analogous to, but not identical with, source code. It is a Museum
description of operative relations and must point back to exact source.

### 5.4 Temporal and interaction analysis

- initialization, frame/update order, stopping or convergence rule, and reset
  behavior;
- distinction among deterministic replay, deterministic session trajectory,
  environment-dependent variation, and unseeded state;
- every supported input, its changed variables, whether it consumes further
  PRNG state, and whether it changes identity, base state, or only the current
  manifestation;
- a bounded behavior trace at named checkpoints rather than a single still.

### 5.5 Collection topology

- authored possibility space and its mathematical structure;
- released population, missing or exceptional states, and edition coverage;
- source-implied probability versus observed population frequency;
- structural clusters, boundaries, and transitions based on actual operations;
- the Museum object's coordinate in that space;
- no market price, owner, popularity, or marketplace rarity input.

An exhaustive project should receive a proof of coverage. A stochastic project
should receive a probability model and empirical comparison. A continuous work
should receive a state-space description and bounded observation protocol,
not a false claim that all possible frames have been enumerated.

### 5.6 Causal atlas

The Museum should render controlled counterfactuals from an instrumented copy:

- one-parameter sweeps;
- ablations that remove a behavior, channel, light, collision term, or
  rendering pass;
- same seed across different parameter states;
- same parameter state across different seeds;
- intermediate buffers before and after compositing or shader translation;
- time-aligned comparisons at defined checkpoints.

These are analytical surrogates, never new artworks or authentic token states.
Every image must name the changed variable, fixed variables, source hash,
runtime, viewport, frame, and Museum authorship. The interface should include
a persistent **analysis view** label and a one-action return to the official
live manifestation.

### 5.7 Materiality, display, and conservation

- executable components and rendering pipeline;
- runtime, dependency, network, browser, GPU, precision, font, audio, and
  timing assumptions;
- cross-environment replay matrix and perceptual-difference protocol;
- artist/platform-designated reference state where one exists;
- display instructions derived from artist source versus Museum recommendation;
- preservation actions for source, dependency, environment, behavior traces,
  reference captures, and later migrations.

## 6. Public publication set

World-class analysis should not be buried in one long PDF or a registrar tab.
Each project should publish a coordinated set:

1. **Algorithm essay** — a sustained curatorial argument about the system's
   operative logic, history, materiality, and exact Museum work.
2. **Algorithm card** — one-screen account of inputs, state, time, interaction,
   rendering, and what the Museum object fixes.
3. **Executable score** — pseudocode, equations, variable glossary, and source
   references.
4. **Causal atlas** — labeled parameter sweeps, ablations, intermediate
   buffers, and same-seed comparisons.
5. **Collection map** — the authored possibility space and exact Museum-object
   position, with trait prevalence available as a secondary view.
6. **Behavior film** — time-based documentation with frame/time/environment
   identity and no suggestion that it is the artwork.
7. **Reproducibility bundle** — pinned inputs, trace output, tests, hashes,
   environment declaration, and instructions.
8. **Conservation note** — what must remain stable, what may vary, and which
   claims remain unverified.

The visitor-facing sequence should begin with the art, then reveal the system
progressively. Source code is not the required entry point.

## 7. Casey pilot: exact algorithmic opportunities

The seven-work gift is unusually strong as a pilot because its five projects
do not merely display five styles. They embody five different relationships
among identity, rule, chance, time, participation, and rendering.

### 7.1 CENTURY: composition becomes a mutable topology

**Source-backed system.** The platform-supplied `tokenData.hash` is reduced
through `parseInt(hash.slice(0, 16), 16)` and a bitwise xorshift generator.
Because the string is `0x`-prefixed, that slice contains fourteen hash digits
after the prefix, not sixteen hash digits or bytes. The seed
selects among four palettes with weighted thresholds, two or more available
line colors, a background, optional translucent ellipses, line quadrilaterals,
slice count and width, slice order, alpha, and a rare expanded line field. The
line quadrilaterals oscillate continuously. An off-screen composition is then
sampled as vertical strips and redrawn in ordered or scrambled sequence. The
`Janky` path offsets interior strips, creating overlaps or gaps. Key `1`
consumes the continuing PRNG stream to define and scramble a new set of cuts;
key `2` reorders the current strips without rebuilding the base composition.

**Museum thesis to test.** The cut is not an effect applied to a finished
picture. It is the work's state-transition mechanism. Identity persists while
adjacency changes; the image is defined as much by relations among parts as by
the parts themselves.

**Three-object opportunity.** The Museum can show the same causal pipeline
producing three materially different pressures:

- #31: Palette A, sixteen slices in a chaotic order without the `Janky`
  offset, and a dense oculus field;
- #724: Palette B, seven slices, `Janky` displacement, and an open cream field;
- #401: Palette C, ten slices, alpha enabled, and grayscale planar depth.

The decisive analytical artifact is a synchronized three-token atlas:
original off-screen buffer, slice boundary map, ordered state, scrambled state,
motion vector, and exact visible output. It would make the difference between
composition and recomposition inspectable without reducing the three works to
their metadata labels.

### 7.2 Pre-Process: an exhaustive score performed by collisions

**Source-backed system.** The edition's three principal axes are not randomly
assigned. For invocation `n`, the source increments it and computes surface as
`(n + 1) mod 8`, origin as `(n + 1) mod 3`, and growth as `(n + 1) mod 5`, with
zero residues renamed to the final category. Because 8, 3, and 5 are pairwise
coprime, the 120 invocations form one complete traversal of the Cartesian
product: every `8 x 3 x 5` combination occurs exactly once.

The token hash separately initializes two alternating `sfc32` streams from the
full 256-bit hash after a 500,000-iteration warm-up that calls each stream
once: 500,000 discarded values per stream and one million calls total. One
hundred circles receive
sizes, initial positions, and headings. They are introduced gradually, one
additional element every ten frames. Each active element advances along its
heading, is clamped inside a frame, eases toward its target position, and tests
later-index elements for overlap. A collision pushes both elements apart and
increments both headings. The eight surfaces do not change the underlying
behavioral rules; they change how centers, perimeters, heading marks, current
contacts, persistent contact histories, and backgrounds are made visible.

**Exact #63 fact.** Invocation 63 becomes ordinal 64 and therefore maps to
Surface 8, Origin 1, Growth 4: one of each exhaustive edition coordinate, not a
random bundle of traits. Origin 1 places all elements at the center; Growth 4
makes them uniformly large. Their progressive introduction begins from extreme
overlap and makes collision resolution the generator of the field.

**Museum thesis to test.** *Pre-Process* is simultaneously a behavioral system
and a theory of representation. The eight surfaces are eight epistemic views
of the same dynamics. Viewer keys `1`-`8` make that argument executable by
rerunning the same hash-derived initial state through alternative visible
surfaces.

The causal atlas should replay one seed across all eight surfaces, show the
population arriving over time, and separate physical state from rendered
evidence. The collection map should prove the 120-state traversal rather than
rank its coordinates.

### 7.3 Phototaxis: drawing as the delayed evidence of behavior

**Source-backed system.** The source creates a 1,000-by-1,000 simulated world,
two to seven fixed lights, and 50, 200, 400, or 800 machines divided across
four Braitenberg-derived wiring types. Each machine has left and right sensors
offset by plus or minus `PI/5`. Sensor-to-light distances are normalized by
the world diagonal and may pass through a parabolic `hump` response. The four
wiring rules alter speed and turning differently; a separate `nerves`
parameter may add seeded perturbation. Brightness is continuously derived from
speed. Each frame updates all machines and then draws a line from the previous
position to the new position without clearing the accumulated field. The
reference thumbnail stops at 1,000 iterations.

The active update path contains no boundary clamp or wrap. Dormant `kill` and
`rebirth` methods exist but are not called by the reviewed source. A path may
therefore leave the nominal world, giving the escaping lines in #308 a direct
algorithmic basis without making them a fixed symbol.

**Exact #308 field.** Published features record three lights, nonlinear
sensors, neutral alignment, `Assemblage` population, `Lively` speed, `Atomic
A` facade, and 0.66 magnification. The algorithm dossier must trace each label
to the exact internal variable and source branch before using it publicly.

**Museum thesis to test.** The image is not a picture of the machines. It is an
archive made by their movement. The work converts sensing into steering,
steering into velocity, velocity into brightness, and duration into density.
The `L` control is therefore more than a convenience: it reveals the hidden
causes of a drawing that normally withholds them.

The causal atlas should pair paths with light locations, isolate each wiring
type, switch the nonlinear sensor function on and off, remove perturbation,
and compare frames 1, 10, 100, and 1,000. A line-by-line reading of the
equations should sit beside the artist's own account of the Path, Tissue, and
MicroImage lineage.

### 7.4 923 EMPTY ROOMS: a room reconstructed from a color field

**Source-backed system.** The source contains an explicit 924-entry lookup.
Invocations 1-923 enumerate the non-empty multisets of one through six items
chosen from six colorforms. The count is:

```text
sum(k = 1..6) C(6 + k - 1, k) = C(12, 6) - 1 = 923
```

Invocation 0 uses the exceptional code `999999`. The parser subtracts one
from each non-zero digit, producing indices outside the six implemented
colorform cases, so no colorform is drawn through that path. The changing
gradient and downstream line-field renderer remain active, so the source does
not establish a blank final display. This is a code-derived observation;
whether the exceptional state is intended as the literally empty room requires
artist or project confirmation.

For ordinary invocations, each code digit instantiates a Sun, Shard, Cargo,
Hive, Pyramid, or Moon form. The forms rotate slowly and are multiply blended
over a changing four-corner gradient in an off-screen WebGL surface. That
surface becomes a displacement texture. A custom shader samples every pixel,
uses selected red, green, and blue intensities as depth, and replaces the
pixel field with a dense array of short line segments viewed in rotated
orthographic space. City presets change channel visibility, background,
depth, and line length.

**Exact #713 fact.** Code `555536` means four Pyramids, one Cargo, and one Moon.
Invocation 713 falls inside the CDMX tranche, whose initial preset exposes only
the green channel against a dark background. The acid-green room is therefore
not a direct model of architecture. It is the green-channel depth projection
of six superimposed moving colorforms.

**Museum thesis to test.** The room exists in translation: code becomes
colorform, colorforms become a composite image, channel intensity becomes
depth, and depth becomes a field of lines that the viewer reads as space. The
algorithm counts the possible rooms exactly while leaving the experience of a
room unstable.

The essential public explainer is a reversible pipeline view:
`555536 -> six diagram forms -> multiply-blended color field -> RGB
displacement maps -> line lattice -> #713`. Channel toggles, the official
diagram view, and the exceptional invocation should be analyzed as part of the
project's theory of visibility, not offered as a rarity display.

### 7.5 Ex Nihilo (Cosmos): ideal geometry survives successive translations

**Source-backed system.** A dual-`sfc32` generator uses both 128-bit halves of
the token hash, alternates the streams, and runs 500,000 warm-up iterations
that call each stream once: 500,000 discarded values per stream and one
million calls total. Initialization chooses one to three dodecahedra,
their positions, rotations, diameters, line chunking, and RGB/white display
mode. Twelve five-vertex faces define each dodecahedron with the golden ratio.
Each face vertex receives a seeded color. The forms rotate and are drawn as
additively blended edges into a 420-by-420 buffer. A second buffer mixes the
new state into retained prior state with low opacity. As in *923 EMPTY ROOMS*,
a shader samples the resulting RGB field, converts channel intensity into
depth, and rebuilds it as offset line geometry in rotated orthographic space.

The spacebar continues the session's PRNG stream to generate a new Still Life
state; it does not reinitialize the token hash. The triggered state is
therefore a deterministic session continuation under the reviewed source, not
automatically a new canonical token image. The source's lowercase-only red and
blue key comparisons remain an interface/documentation discrepancy already
recorded in the accession dossier.

**Exact #248 field.** Published features identify three Cosmos forms, a white
display state, and `CHUNK 3`. A full 256-token replay establishes the
branch-sensitive operational mapping: in white and RGB paths, published
`CHUNK 3` corresponds to runtime `metaCHUNK=4`; #248 therefore draws source
edges with `strokeWeight(4 / 1.2)`. The feature script is not retained, so the
reason for this semantic relabeling remains unresolved and no universal
arithmetic conversion should be inferred.

**Museum thesis to test.** The dodecahedron is not merely fragmented. It passes
through a chain of representations: ideal coordinates, colored vector edges,
temporal raster memory, channel displacement, and line-field projection. The
work's "Cosmos" is the persistence of a recognizable form across translations
that continually prevent it from becoming a settled object.

The causal atlas should expose all intermediate buffers, freeze temporal
feedback, isolate one dodecahedron, compare RGB with white reconstruction,
vary the chunk and line-depth parameters, and show exactly what the spacebar
changes.

## 8. The comparative Casey argument

The five dossiers should culminate in a cross-project study. Several relations
are already visible.

| Project | Identity/selection logic | Principal evolving state | Visible conversion | Viewer agency |
|---|---|---|---|---|
| CENTURY | hash-seeded weighted choices | oscillating quadrilaterals and continuing slice PRNG | composition -> off-screen buffer -> reordered strips | cut/reorder or restore order |
| Pre-Process | exhaustive token-index coordinate plus full-hash seed | growing population and pairwise collision response | element state -> one of eight surfaces | choose surface, reset, pause |
| Phototaxis | hash-seeded ecological parameters | sensor-driven machines and accumulating paths | sensing -> motion -> line history | reveal lights, reset, scale, pause |
| 923 EMPTY ROOMS | explicit combinatorial lookup plus seed | rotating colorforms and gradient | colorform composite -> RGB depth -> line room | diagram, channels, city preset, depth, speed, scale |
| Ex Nihilo (Cosmos) | full-hash seeded state | rotating dodecahedra and temporal feedback | ideal solid -> edge buffer -> RGB depth -> line field | new state, channels, speed, pause |

This supports at least four major essays:

1. **Two histories of chance.** *CENTURY*, *Phototaxis*, and *923 EMPTY ROOMS*
   use a 16-character `0x`-prefixed hash slice and bitwise xorshift path, while
   *Pre-Process* and *Ex Nihilo* use alternating full-hash `sfc32` streams after
   a large warm-up. The change
   is technical, but it also changes how identity enters the work.
2. **Enumeration versus probability.** *Pre-Process* and *923 EMPTY ROOMS*
   build edition completeness into their number structure; the other projects
   sample authored probability fields. Long-form generative art is not one
   model of variation.
3. **The image as evidence.** *Phototaxis* records movement; *Pre-Process*
   changes the surface through which behavior is known; *923* and *Ex Nihilo*
   translate intermediate images into depth; *CENTURY* exposes adjacency as a
   variable. Each project makes a different claim about what an output is
   evidence of.
4. **Participation without co-authorship.** Each interface lets a viewer enter
   the system at a different level: reorder an existing image, rerender the
   same dynamics, reveal hidden causes, manipulate a rendering pipeline, or
   continue a seeded state trajectory.

## 9. Implementation architecture

The standard should produce a versioned `GENERATIVE_SYSTEM_DOSSIER` whose
payload points to, rather than duplicates, the accession, rights, condition,
object, and NextGen descriptor records. Suggested linked components:

- `source_lock`
- `randomness_profile`
- `parameter_provenance`
- `algorithmic_score`
- `state_and_time_profile`
- `interaction_profile`
- `render_pipeline`
- `collection_topology`
- `causal_atlas_manifest`
- `execution_observations`
- `environment_matrix`
- `curatorial_argument`
- `uncertainties`
- `review`

The dossier should use the existing Museum envelope, stable object/project
subjects, canonical payload hash, append-only amendments, constructor/reviewer
separation, and public/restricted boundary. Any future Stream mapping requires
a versioned profile and explicit interoperability review; this WIP note does
not assign a Stream schema or record type.

An instrumented runner should be separate from the official source and should
never rewrite the artwork. It should load pinned bytes, inject observation
hooks at declared boundaries, and emit deterministic JSON traces. Tests should
prove source hash binding, seed replay, parameter mapping, counterfactual
isolation, trace determinism where claimed, full population coverage, and
fail-closed behavior when source or dependency bytes drift.

## 10. Acceptance rubric

An analysis is publication-ready only if all answers are yes.

- Can a reader state the transformation from input to visible event?
- Is every fixed, temporal, interactive, and environmental state separated?
- Is seed handling reconstructed exactly, including truncation and coercion?
- Are authored probabilities separated from observed edition frequencies?
- Is an exhaustive collection accompanied by a proof of coverage?
- Can each public counterfactual be reproduced from a pinned source and trace?
- Are analytical surrogates unmistakably labeled as Museum-made?
- Does the interpretation advance a contestable claim rather than celebrate
  complexity in the abstract?
- Does close looking remain necessary after the algorithm is explained?
- Are live work, official reference state, and documentation distinguished?
- Are code facts, execution observations, artist statements, and Museum
  interpretations attributed separately?
- Are dormant code, bugs, mismatches, and uncertainty reported without turning
  the essay into a defect list?
- Does the exact Museum object matter to the analysis?
- Are rarity, quality, price, desirability, and curatorial significance kept
  separate?
- Can an independent reviewer reconstruct the core factual claims?

## 11. Recommended pilot sequence

1. **Source lock and rights review.** Retain or lawfully reference exact
   generator, project-script, feature-script, and dependency bytes for the five
   projects. Resolve publication rights for annotated code and derived
   screenshots.
2. **Trace prototype.** Build the provenance tracer first for *Pre-Process* and
   *923 EMPTY ROOMS*, because their exhaustive structures provide unusually
   strong correctness oracles.
3. **Behavior prototype.** Add *Phototaxis* for temporal equations, trace
   accumulation, and hidden-cause visualization.
4. **Rendering-pipeline prototype.** Add *923* and *Ex Nihilo* intermediate
   buffers and shader-stage views.
5. **Comparative object prototype.** Build the three-*CENTURY* synchronized
   causal atlas.
6. **Schema and review.** Only after the five pilots are intelligible should
   the Museum stabilize a reusable schema and validation profile.
7. **Public integration.** Add art-first progressive disclosure to the Museum
   site: artwork, thesis, algorithm card, causal atlas, collection map,
   reproducibility and conservation layers.

## 12. Current evidence checkpoint

On 2026-08-04 UTC, the seven official Art Blocks generator responses were
retrieved read-only for analysis. Their byte lengths and SHA-256 digests
matched the independently reviewed values in
`evidence/casey-reas/generator-observations.json` for all seven objects. No
response bytes were added to the repository in this turn. The retained
transcript remains the governed source for the exact hashes and the explicit
preservation boundary.

The current official source observations support the algorithmic conclusions
above, but they do not complete a source-preservation package, feature-script
reconstruction, cross-environment execution study, or independent substantive
review of this proposal.

## 13. Open questions

- What working name should the public program use: **Algorithm Dossier**,
  **Generative System Study**, or another term that is rigorous but not
  forbidding?
- Should the standard cover only generative editions, or all executable and
  rules-based artworks, including deterministic one-offs and interactive
  systems?
- Which counterfactuals can be published under the current rights record, and
  which should remain non-public conservation research?
- Can the project and feature scripts be retained as exact bytes, or must some
  dossiers publish hashes and commentary without redistributing source?
- What constitutes perceptual equivalence across browsers and GPUs for each
  project?
- Which states are artist-designated manifestations, platform reference
  states, viewer-triggered states, or Museum analytical states?
- Does *923 EMPTY ROOMS* invocation 0 intentionally constitute the literally
  empty room, or is that only a code-level effect of the exceptional entry?
- Why does the published *Ex Nihilo* `CHUNK` feature use a branch-sensitive
  semantic mapping from runtime `metaCHUNK`? The operational mapping is
  reconstructed across all 256 tokens, but the feature-script rationale is
  unretained and unresolved.
- Should a collection map display metadata prevalence at all, or keep it in a
  separate research view to prevent market-style reading?
- Which scholars, software conservators, creative coders, and artist/studio
  representatives should review the standard before it becomes canonical?

## 14. Non-claims

This note does not amend the Casey accession, assign new rights, claim source
preservation completion, publish a new rarity method, authenticate an
unretained byte stream, establish artist intent from code alone, or adopt a
Museum policy. It proposes a research and publication standard for review.
