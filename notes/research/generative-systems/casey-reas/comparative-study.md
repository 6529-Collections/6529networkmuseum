# Casey Reas: five systems, seven works

## The argument

The gift is not a sampler of seven images. It is a compact account of how a
generative artist can relocate the image inside a system.

Across the five projects, the visible field assumes five different causal
roles. In *CENTURY*, it is a composition whose adjacency remains open to
revision. In *Pre-Process*, it is one surface through which a common population
behavior becomes legible. In *Phototaxis*, it is the accumulating history of
machines sensing hidden lights. In *923 EMPTY ROOMS*, it is an intermediate
color field converted into depth and rebuilt as a line-defined room. In *Ex
Nihilo (Cosmos)*, ideal geometry passes through colored edges, temporal memory,
channel displacement, and line projection without resolving into a stable
object.

The strongest collection-level claim is therefore not that all five works use
algorithms. It is that each asks **what kind of evidence an image can be**. An
image may be material for rearrangement, a selective skin over behavior, a
trace of prior motion, a displacement map, or the temporary persistence of a
form across translations.

## Exact scope of the gift

| Project | Museum objects | Project-level unit of difference | Principal evolving state | Viewer entry point |
|---|---|---|---|---|
| *CENTURY* | #31, #724, #401 | weighted composition and slice parameters from the token hash | oscillating quadrilaterals; continuing slice-state PRNG | cut/reorder and restore strip adjacency |
| *Pre-Process* | #63 | exhaustive `8 × 3 × 5` coordinate plus full-hash simulation seed | activation, growth, motion, and pairwise collision of 100 elements | rerender/reset the same rules through one of eight surfaces |
| *Phototaxis* | #308 | hash-derived environment, population, wiring, and display parameters | sensor-to-motor response and accumulated paths over 1,000 iterations | reveal lights, change magnification, reset, or pause |
| *923 EMPTY ROOMS* | #713 | one of 923 non-empty multisets of six colorforms plus city/presentation state | rotating forms, gradient, composite color field, and line-space projection | inspect diagram, channels, city preset, depth, speed, scale, or resolution |
| *Ex Nihilo (Cosmos)* | #248 | hash-derived dodecahedra, placement, color, chunking, and display state | rotation, additive edge image, retained temporal feedback, and line projection | continue seeded Still Life state; change channels, speed, or pause |

This table compresses rather than substitutes for the individual dossiers. In
particular, “viewer entry point” does not imply that every control changes the
same layer or creates a new canonical identity.

## I. Two technical histories of identity

The five projects do not share a single model of seeded chance.

*CENTURY*, *Phototaxis*, and *923 EMPTY ROOMS* initialize a bitwise xorshift
path from `tokenData.hash.slice(0, 16)`. Because the authoritative string is
`0x`-prefixed, that 16-character slice contains the prefix and fourteen hash
digits. Exact language coercions matter: JavaScript parses the resulting
number and later applies signed 32-bit bitwise operations. It is therefore not
valid to substitute a PRNG seeded from the first sixteen hash digits or bytes.

*Pre-Process* and *Ex Nihilo (Cosmos)* divide the full token hash into two
128-bit seed groups, initialize two `sfc32` streams, and alternate between
them. In both projects, a 500,000-iteration loop discards one value from each
stream per iteration: 500,000 values per stream and one million calls total.
This construction lets identity
enter through the whole hash and makes the order of random-number consumption
part of a reperformance specification.

The collection thus preserves two code-level histories of how a token identity
becomes a sequence of decisions. This is a technical difference with
interpretive force: “the hash” is never a self-explanatory cause. It becomes
meaningful only through an authored procedure of truncation, coercion, stream
construction, and consumption.

### Required comparative exhibit: seed provenance

The causal atlas should place all five seed paths side by side. For one Museum
token per project it should show:

`authoritative identity -> parsed words -> initialized state -> warm-up or
first draw -> first five derived decisions`

The exhibit should use exact test vectors and label source-static versus
instrumented values. It must not visualize a pseudorandom stream as if that
stream were itself the artwork.

## II. Enumeration and probability are different edition forms

The gift contains at least three fundamentally different ways to make an
edition.

### Exhaustive coordinate space

*Pre-Process* uses invocation arithmetic to traverse a Cartesian product of
eight surfaces, three origins, and five growth states. Because the factors are
used as explicit coordinates across 120 invocations, the project can be
tested for exact coverage and uniqueness. The project is not merely likely to
show every combination; its numbering system is intended to do so.

### Exhaustive multiset space

*923 EMPTY ROOMS* enumerates every non-empty multiset of size one through six
drawn from six colorform types:

```text
sum(k = 1..6) C(6 + k - 1, k)
= C(12, 6) - 1
= 923
```

This is not the same topology as a Cartesian product. Repetition is allowed,
order is ignored, and size varies. Invocation 0 is separately coded and must
remain an exceptional unresolved state rather than being folded into the proof
or assigned an artistic meaning from code alone.

### Authored probability fields

*CENTURY*, *Phototaxis*, and *Ex Nihilo (Cosmos)* sample authored distributions
or ranges. Their edition structures require a dependency map and theoretical
support, not a false proof that every possible combination occurs. Empirical
population counts may supplement that map only through the Museum's pinned
NextGen-compatible snapshot method.

### Curatorial consequence

Long-form generative art is often discussed as if an edition were a bag of
random outputs. These five projects show three more exact possibilities: an
exhaustive coordinate argument, an exhaustive combinatorial argument, and a
probability field. An edition can be authored at the level of coverage as well
as at the level of individual appearance.

## III. Five positions for the image

### 1. The image as mutable adjacency — *CENTURY*

The initial composition is drawn into an off-screen buffer from oscillating
quadrilaterals and then sampled as vertical strips. The strip order, widths,
and optional gaps or overlaps decide which regions become neighbors. Pressing
`1` continues the work's random stream to cut and scramble the current image;
pressing `2` restores ordered composition. The image is simultaneously a
picture and material awaiting a later topology.

The three Museum tokens are essential here. #31, #724, and #401 permit a
controlled comparison across palettes, line/slice counts, alpha, Janky, and
Oculi states while holding the project logic constant. They prevent the
project essay from treating one output as the whole authored field.

### 2. The image as surface evidence — *Pre-Process*

One population of one hundred elements activates, grows, moves, and responds
to pairwise proximity. Eight surface treatments do not create eight different
behaviors; they disclose the same behavior through different graphic
consequences. The project's invocation arithmetic coordinates those surfaces
with origin and growth states.

The image here is a measurement surface. A different surface changes what the
same collision and movement system allows the viewer to know.

### 3. The image as accumulated path — *Phototaxis*

Machines sense two to seven lights through paired sensors, transform those
readings into motor values according to one of four wiring types, turn, move,
and leave paths. Since the background is not cleared during the principal run,
the final field contains the temporal history of responses, not only a final
position.

The `L` control is therefore epistemically important. Revealing the lights
adds hidden causes to an image that otherwise shows their effects. It turns a
seductive line field into an inspectable sensorimotor history without reducing
that history to a diagram.

### 4. The image as displacement instrument — *923 EMPTY ROOMS*

Six diagrammatic colorforms can be superimposed, rotated, and multiply blended
over a changing gradient. Their composite off-screen image is sampled by a
shader. Selected red, green, and blue intensities become depth, and a dense
lattice of short line segments makes that depth perceptible as space.

For #713, code `555536` instantiates four Pyramids, one Cargo, and one Moon.
The CDMX preset begins with the green channel visible against a dark
background. #713 retains the default symmetric depth mapping; the tranche's
special `-500..0` depth override applies only to boundary invocation 617. The
encountered room is thus not a direct rendering of six objects: it is a
channel-specific spatial reading of their composite image.

### 5. The image as temporal memory — *Ex Nihilo (Cosmos)*

One to three dodecahedra are constructed from golden-ratio coordinates, drawn
as colored additive edges, and mixed with retained prior state in a second
buffer. A related shader pipeline converts that temporally accumulated RGB
field into displaced line geometry.

This system shares an image-to-depth strategy with *923 EMPTY ROOMS* but adds a
different origin and temporal condition. The source image begins with ideal
solid geometry rather than a multiset of diagram forms, and the feedback
buffer makes prior frames an active material. Pause freezes rotation but not
the render loop: the static edge image continues entering the low-opacity
feedback buffer and can keep changing its density. Similar rendering machinery
therefore carries a different claim: not the counting of possible rooms, but
the persistence of recognizable form through representation and memory.

## IV. Participation enters at different causal depths

| Project | Control class | What remains fixed | What changes | Interpretive risk to avoid |
|---|---|---|---|---|
| *CENTURY* | `state` plus `view` | token-derived composition system | strip partition/order using continuing randomness; ordered restoration | calling every cut a new token identity |
| *Pre-Process* | `render` and `state` reset | identity parameters and behavior rules | surface selection and restarted performance | claiming eight different behavioral systems |
| *Phototaxis* | `reveal`, `view`, reset, pause | token-defined ecology | visibility, magnification, performance state | treating revealed lights as normally visible output |
| *923 EMPTY ROOMS* | `reveal`, `render`, `view`, environment-like presets | invocation code and six selected forms | diagram, channels, projection, timing, spatial presentation | collapsing an analytical view into the work's sole canonical view |
| *Ex Nihilo (Cosmos)* | `state`, `render`, partial pause | token-seeded session and authored generator | continued PRNG state, new Still Life arrangement, channels, rotation speed; pause freezes rotation while feedback continues | treating a spacebar continuation as a newly minted work or pause as a frozen raster state |

The viewer is not positioned identically in these systems. One rearranges
adjacency, another chooses a surface, another reveals causes, another operates
a chain of representations, and another continues a seeded trajectory.
“Interactive” is therefore too blunt as the final category. The dossier must
locate participation inside the causal structure.

The source also shows why a museum must test controls as state transitions,
not copy interface labels. *CENTURY* key `2` orders the current partition
without rebuilding the composition. A *Pre-Process* reset reconstructs its
seeded population but does not reset p5's global `frameCount`, so activation
phase can differ; its initial pause latch needs execution confirmation.
*Phototaxis* `L` can advance one complete frame when invoked during pause.
*923 EMPTY ROOMS* `P` saves the canvas rather than pausing. *Ex Nihilo* pause
freezes rotation while its feedback buffer continues to accumulate. These are
not incidental interface trivia: each determines what state a conservator or
visitor actually produces.

## V. The seven-work gift as a deliberately useful study group

The gift is asymmetrical in a productive way: three *CENTURY* works and one
work from each of four other projects. The three-work group supports
within-project controlled comparison. The four single works support
cross-project comparison across behavior, enumeration, hidden causes, image
translation, and viewer agency.

This structure suggests a Museum presentation in five movements:

1. **Composition can be cut:** synchronize the three *CENTURY* works, then
   reorder each without losing its baseline.
2. **One behavior has many skins:** expose *Pre-Process* state beneath its
   eight surfaces and place #63 in the exact 120-state grid.
3. **A line remembers a sensor:** run *Phototaxis* #308 with lights hidden,
   reveal them, and replay the identical trace.
4. **A color becomes a room:** unfold #713 from `555536` through colorforms,
   composite image, channel displacement, and line lattice.
5. **A solid survives translation:** follow #248 from dodecahedral coordinates
   through edges, feedback, channels, and line field.

The visitor should encounter each live work before seeing the analytical
surrogate. Explanation follows attention; it does not replace it.

## VI. Master causal-atlas program

The five dossiers together require a coherent atlas rather than unrelated
demos.

| Atlas family | CENTURY | Pre-Process | Phototaxis | 923 EMPTY ROOMS | Ex Nihilo |
|---|---|---|---|---|---|
| Seed provenance | 16-character `0x`-prefixed slice, then xorshift and weighted choices | full-hash dual `sfc32`; invocation coordinates | 16-character `0x`-prefixed slice, then xorshift and ecology parameters | 16-character `0x`-prefixed slice plus explicit code table | full-hash dual `sfc32`; session continuation |
| Topology | authored probability/dependency map | exact `8 × 3 × 5` grid | authored parameter support | exact non-empty multiset lattice | authored parameter support |
| Hidden state | moving quadrilaterals beneath strips | common element state beneath surfaces | lights, sensors, motor values | diagrams and RGB maps beneath room | ideal coordinates, edge and feedback buffers |
| Time | oscillation and continuing cut state | staged activation and collision history | 1,000-step trace | rotating forms and changing gradient | rotation and temporal feedback |
| Interaction | cut vs ordered adjacency | surface/reset/pause | reveal/reset/scale/pause | channel/preset/depth/diagram controls | Still Life continuation/channels/speed/pause |
| Exact gift | three synchronized comparison | #63 coordinate and behavior | #308 ecology | #713 `555536` pipeline | #248 three-form white state and unresolved chunk label |

Every exhibit should have a baseline, one isolated intervention, held-constant
variables, replay procedure, source/environment lock, trace digest, surrogate
label, rights status, and accessible text description. The atlas should permit
movement both forward from cause to image and backward from a visible event to
its causes.

## VII. Conservation across the collection

The common preservation problem is not only whether a script file survives.
It is whether the relation among identity, state transition, rendering, and
encounter can be re-performed and tested.

### Shared significant properties

- authoritative token identity, invocation, source, assets, and dependency
  binding;
- exact seed parsing, PRNG state, warm-up, and consumption order;
- parameter maps and exceptional invocation handling;
- frame/state transition, feedback, termination, and reset behavior;
- intermediate-buffer order, shader semantics, projection, and blend modes;
- interaction consequences, including key-case discrepancies;
- meaningful scale, duration, color/channel behavior, and input parity.

### Project-specific conservation pressure

- *CENTURY*: preserve continued random state after load; otherwise identical
  initial images can cut differently.
- *Pre-Process*: preserve activation timing, pairwise update order, collision
  consequences, and all eight render surfaces.
- *Phototaxis*: preserve sensor equations, update order, non-cleared trace,
  stopping condition, and actual boundary behavior rather than a presumed one.
- *923 EMPTY ROOMS*: preserve the 924-entry table, exceptional invocation,
  colorform-to-buffer pipeline, shader, and city/control semantics.
- *Ex Nihilo*: preserve golden-ratio geometry, dual-stream initialization and
  500,000-call-per-stream warm-up, feedback buffers, session-continuing state
  generation, shader, and actual key comparisons.

The reviewed remote generators remain evidence, not autonomous preservation.
Exact generator, project-script, dependency, and reproducible-environment
capture is still active stewardship under the accession records.

## VIII. Claims requiring review

| Claim ID | Comparative claim | Class / qualifier | Current status | Principal review need |
|---|---|---|---|---|
| `CASEY-COMP-001` | The five projects position the image as mutable adjacency, surface evidence, path history, displacement instrument, or temporal memory. | `E / museum_interpretation` | supported | independent curatorial challenge and alternative reading |
| `CASEY-COMP-002` | Three projects use a 16-character `0x`-prefixed hash slice and xorshift path; two use alternating full-hash `sfc32` streams after warm-up. | `C / source_static` | provisional | independent exact-source reconstruction and test vectors |
| `CASEY-COMP-003` | *Pre-Process* exhausts `8 × 3 × 5`; *923 EMPTY ROOMS* exhausts the 923 non-empty multisets of up to six of six types. | `C / source_formal` | provisional | independent code-to-index proof, including exceptions |
| `CASEY-COMP-004` | *923 EMPTY ROOMS* and *Ex Nihilo* share an image-to-RGB-depth-to-line-field strategy but differ in source geometry and temporal feedback. | `C+E / source_static+museum_interpretation` | provisional | stage-level source comparison and instrumented buffer traces |
| `CASEY-COMP-005` | Viewer controls enter the five systems at materially different causal depths. | `C+E / source_static+museum_interpretation` | supported | interaction replay and curatorial review |
| `CASEY-COMP-006` | The seven-work structure is especially useful because three *CENTURY* works support within-project comparison while four singletons support cross-project comparison. | `E / museum_interpretation` | supported | curatorial review; no claim of donor intent |

## IX. Material unresolved questions

- Does the independently retained or lawfully referenceable source package
  permit exact replay when the live generator, CDN, or browser environment
  changes?
- What is an acceptable perceptual and behavioral tolerance for each project
  across browsers, GPUs, displays, and frame schedules?
- Which project states are artist-designated manifestations, platform
  reference states, viewer-triggered performances, or Museum analytical
  states?
- Is *923 EMPTY ROOMS* invocation 0 intended as a literally empty room? Its
  exceptional table entry dispatches no implemented colorform, but the
  gradient and line-field pipeline remain active, so the source does not
  establish a blank final display.
- Why does *Ex Nihilo*'s branch-sensitive published `CHUNK` label map runtime
  `metaCHUNK=4` to `CHUNK=3` for #248? The full-edition replay establishes the
  operational mapping, but the feature-script rationale remains unretained and
  unresolved.
- Which annotated code, buffer captures, traces, screenshots, and
  counterfactuals can be published under the current rights determination?
- Can the viewer-facing collection map explain structure without importing a
  rarity or market hierarchy?
- Which external software conservator, creative-code scholar, and artist or
  studio representative should review the package before public promotion?

## X. Release boundary

The comparative account and five dossiers are research candidates. Before
public promotion they require independent technical reconstruction,
independent curatorial review, rights/accessibility review of every analytical
artifact, source and trace fixity, and an explicit disposition for each
material unresolved question. Uncertainty may be published; it may not be
silently converted into fact.

This is constructed comparative research for the seven works in accession
`6529NM.2026.001`, not an accession amendment, assignment of artist intent,
designation of an official manifestation, rights clearance for derived media,
or claim of preservation completion.
