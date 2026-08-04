# Ex Nihilo (Cosmos): a solid translated into memory

## Curatorial proposition

*Ex Nihilo (Cosmos)* does not send a dodecahedron directly to the screen. It
passes ideal geometry through five materializations: golden-ratio coordinates,
colored vector edges, an additive raster image, a decaying memory of that
image, and channel-specific line geometry displaced in depth. The visible
Cosmos is the persistence of a form across translations that repeatedly put
its wholeness at risk.

For the Museum, the key distinction is between identity and continuation. The
token hash fixes the initial random stream and its first state. The spacebar
does not reseed from the token; it consumes the stream's current position and
begins another Still Life state within the same session. Token identity is
stable while manifestation remains a trajectory.

## The exact Museum work

| Field | Reviewed fact |
|---|---|
| Object | `6529NM.2026.001.07`, *Ex Nihilo (Cosmos)* #248 |
| Chain identity | `eip155:1/erc721:0x0000000c687daed0fba60d1dba4e5f6149e8b894/248` |
| Platform identity | Art Blocks Studio project 0, invocation 248 |
| Token hash | `0x09e7e497b272d55d199f92d3f0105d43d88f6f3b1f87e89f1ea64e4ea1ba01a8` |
| Published features | `RGB=false`; `CHUNK=3`; `# COSMOS=3`; `FFFFFF=true`; single channels false |
| Generator | `https://generator.artblocks.io/1/0x0000000c687daed0fba60d1dba4e5f6149e8b894/248` |
| Generator response SHA-256 | `sha256:17402c7259ac4af1e93894eb74b36a5796a6a058ea0fb0e56d2f55101a3c84f9` |
| Dependency observed | p5.js 1.9.0 via cdnjs |
| Rights boundary | Retained metadata states CC BY-NC 4.0; token title and copyright remain separate |
| Condition boundary | Display-ready with conditions; autonomous software preservation remains active stewardship |

See the [reviewed object
record](../../../../records/accessions/6529NM.2026.001/objects/6529NM.2026.001.07.json),
[rights statement](../../../../records/accessions/6529NM.2026.001/rights/6529NM.2026.001.RIGHTS.07.json),
[condition report](../../../../records/accessions/6529NM.2026.001/technical/6529NM.2026.001.07.json),
and [visual-observation
record](../../../../records/accessions/6529NM.2026.001/visual-observation-record.json).

## Evidence and source lock

| Layer | Identity and use | Method and limitation |
|---|---|---|
| Official generator response | URL above; 21,034 response bytes; SHA-256 `17402c…c84f9` | The 2026-08-04 read-only retrieval reproduced the independently reviewed digest in [`generator-observations.json`](../../../../evidence/casey-reas/generator-observations.json). Bytes were not retained. `[execution_observed]` |
| Inline project script | 20,434 UTF-8 bytes; working SHA-256 `a9f5e37a95115ac398856a4878ff03b2ac52af3dd41765518943f24bee8c18b7` | Extracted in memory from the matching response. Component hash is a working observation, not a governed preservation object. `[source_static]` |
| Exact metadata | [`evidence/casey-reas/raw/metadata/6529NM.2026.001.07.json`](../../../../evidence/casey-reas/raw/metadata/6529NM.2026.001.07.json); SHA-256 `60431b…6dc` | Retained response bytes containing token hash, project identity, published features, and license label. |
| Full population | [`snapshot.json`](../../../../evidence/casey-reas-collection-snapshots/runs/20260801T172252532Z/snapshots/ex-nihilo-cosmos/snapshot.json) and [`descriptor`](../../../../evidence/casey-reas-collection-snapshots/descriptors/ex-nihilo-cosmos.json) | Frozen 256-token metadata population. Used for feature/replay reconciliation, never aesthetic rank. `[population_empirical]` |
| Platform/artist account | [Art Blocks, “Ex Nihilo (Cosmos)”](https://www.artblocks.io/collection/ex-nihilo-cosmos-by-casey-reas/purchase) | Official account of Still Life lineage, dodecahedron/Cosmos, pixel-to-line translation, continuous behavior, and controls. `[artist_statement]` |
| Artist context | [REAS Studio, “Atomism”](https://reas.com/atomism) | Artist-controlled account of Still Life's pixel decomposition, RGB/HSB systems, and continuous unfolding. `[artist_statement]` |
| Museum scholarship | [Project essay](../../../../records/accessions/6529NM.2026.001/public/projects/still-life-and-ex-nihilo.md) and [technical research](../../casey-reas-art-technical-research.md) | Reviewed interpretation and source apparatus; not a substitute for generator evidence. |

The official page states that the work runs continuously and never repeats.
That is retained as an artist/platform statement. Neither this source review
nor the accession's brief two-frame observation proves non-repetition over an
unbounded run.

## Randomness provenance

### Full-hash construction

The source divides the 256-bit token hash into two 128-bit halves. Each half
initializes an `sfc32` generator using four 32-bit words. The warm-up loop runs
500,000 iterations and calls both streams once per iteration: 500,000 discarded
values from A plus 500,000 from B, one million discarded PRNG values total.
Subsequent `random_dec()` calls alternate A, B, A, B, beginning with A.
`[source_static]`

This count is conservation-significant. Describing the code loosely as “a
million-call warm-up for each stream” would advance each half twice as far and
produce a different work.

### Initial authored choices

`generateStillLife()` consumes the alternating stream in this order:

1. number of Cosmos forms: integer 1, 2, or 3 with equal authored probability;
2. provisional runtime `metaCHUNK` from `[1,1,1,4,4,7,7]`;
3. display branch `tr`:
   - `tr < 0.1`: one of red, green, or blue; replace `metaCHUNK` from
     `[1,1,7,7,10,10]`;
   - `0.1 ≤ tr < 0.7`: all RGB channels; replace `metaCHUNK` from
     `[1,1,1,4,4]`;
   - `tr ≥ 0.7`: white display; keep the provisional value;
4. for every Cosmos: position, x rotation, y rotation, and diameter.

The authored display probabilities are therefore 10% single-channel, 60% RGB,
and 30% white, before finite-edition sampling. Conditional `metaCHUNK`
probabilities are exactly the multiplicities in the arrays above. These are
source probabilities, not claims about artistic importance. `[source_formal]`

### Exact initial draws for #248

An independent in-memory replay of the source PRNG for #248 produced:

| Draw | Value | Consequence |
|---|---:|---|
| Cosmos-count draw | `0.9657193149905652` | 3 forms |
| provisional-chunk draw | `0.6229483252391219` | array index 4, runtime `metaCHUNK=4` |
| display-branch draw | `0.8496790907811373` | white branch |

These results reproduce the published `# COSMOS=3` and `FFFFFF=true` features.
They also expose the distinction between published `CHUNK=3` and the runtime
variable described below. `[execution_instrumented]`

## Resolving `CHUNK` and runtime `metaCHUNK`

The current render source never uses a variable named `CHUNK`. It uses
`metaCHUNK` as `strokeWeight(metaCHUNK / 1.2)` when drawing dodecahedral edges.
For #248 the replayed runtime value is 4, while retained platform metadata
reports `CHUNK=3`.

To test whether this was a token-specific mismatch, the Museum replayed the
initial three branches for all 256 retained token hashes and compared runtime
state with published features. The replay reproduced all 256 Cosmos counts and
all 256 channel modes. The complete cross-tab was:

| Runtime branch and `metaCHUNK` | Published `CHUNK` | Tokens |
|---|---:|---:|
| RGB, 1 | 1 | 97 |
| RGB, 4 | 3 | 62 |
| white, 1 | 1 | 45 |
| white, 4 | 3 | 17 |
| white, 7 | 5 | 19 |
| single channel, 1 | 1 | 5 |
| single channel, 7 | 7 | 9 |
| single channel, 10 | 10 | 2 |

This reconciles #248 operationally: its published semantic label `CHUNK=3`
corresponds consistently to runtime `metaCHUNK=4` in the white/RGB paths. It
also shows that no universal arithmetic conversion is valid: runtime 7 maps to
published 5 in the white path and published 7 in the single-channel path.

The feature script itself is not retained in the research package, so the
reason for this branch-sensitive label mapping remains unproven. It may be an
intentional semantic scale, a feature/render-version difference, or another
documented convention. The dossier must report the mapping, not guess its
meaning. `[source_static; execution_instrumented; population_empirical]`

### Frozen population, not probability

The 256-token source snapshot contains:

| Feature | Population counts |
|---|---|
| `# COSMOS` | 1: 87; 2: 91; 3: 78 |
| Display state | RGB: 159; white: 81; single red: 4; single green: 7; single blue: 5 |
| Published `CHUNK` | 1: 147; 3: 79; 5: 19; 7: 9; 10: 2 |

These are deterministic edition observations from the pinned snapshot. They
are separate from authored branch probabilities and have no ranking meaning.

## Algorithmic score

### Dodecahedral source geometry

The source defines the golden ratio `φ = 1.61803398875`, `b = 1/φ`, and
`c = 2 - φ`. Twelve ordered faces contain five vertices each. Every vertex is
assigned a hash-seeded RGB color once during initial setup. A `COSMOS` object
adds a position, two initial rotation angles, and a diameter; one to three
objects share the same face-color table. `[source_static]`

### Per-frame score

```text
INPUT tokenHash, viewport

(A, B)       ← sfc32(first hash half), sfc32(second hash half)
discard      ← 500,000 A values and 500,000 B values
R            ← alternating stream A, B, A, B, ...
state        ← generateStillLife(R)
faceColors   ← 60 seeded RGB triplets from R

FOR EACH FRAME:
    IF not paused:
        shapeSpeed   ← rotateCounter
        rotateCounter += metaSPEED

    clear current 420 × 420 edge buffer to black

    FOR EACH Cosmos object:
        rotate by (rx - shapeSpeed, ry + shapeSpeed)
        draw 12 five-vertex face boundaries with ADD blending
        use strokeWeight(metaCHUNK / 1.2)

    composite current edge buffer into persistent memory buffer
    with white tint alpha 51/255; do not clear memory each frame

    FOR EACH of 420 × 420 pixel sites and each displayed channel:
        channelIntensity ← sampled memory-buffer component
        z ← map(channelIntensity, 0..1, -30×depthScalar..+30×depthScalar)
        build a short 3D line rectangle at z

    render channel passes additively through orthographic projection,
    rotateY(0.33), rotateX(-0.33)
```

The 420 × 420 field supplies 176,400 possible line sites per channel pass.
Near-black source pixels are discarded by the fragment shader. In white mode,
the renderer still performs three channel-specific passes; it colors each pass
gray and offsets green and blue laterally. White is therefore a reconstruction
from all three channel geometries, not a single grayscale height map.
`[source_static]`

## Temporal memory and state

The current dodecahedral edge buffer is cleared every frame. The second buffer
is not. `tint(255, 51)` introduces the new edge image at approximately 20%
alpha, retaining prior marks as a decaying visual history. The shader samples
this memory buffer, not the current vector geometry. What reaches the line
field is therefore already temporal. `[source_static]`

| State layer | Contents | Change behavior |
|---|---|---|
| Identity | contract, token, token hash, Studio project/invocation | Fixed |
| Initial phenotype | Cosmos count, display branch, runtime chunk, form positions/rotations/diameters, face colors | Hash-derived at first setup |
| Frame state | `rotateCounter`, dodecahedral orientation, 420² memory-buffer pixels | Rotation advances per rendered frame when unpaused. Under pause, orientation freezes but the repeated static edge image continues to enter the memory buffer, which can still converge toward a denser state. |
| Session continuation | current positions/count/chunk/display after spacebar; retained face-color table | Spacebar clears memory and consumes the continuing PRNG; it does not reseed or regenerate face colors |
| Interaction state | pause, speed, channel flags, white flag | Viewer mutable |
| Environment | viewport/orientation, p5/WebGL build, browser, GPU/driver, cadence | Affects placement, scale, rasterization, memory evolution, and perception |

The spacebar nuance is exact: `generateStillLife()` clears the memory buffer
and chooses new count, chunk, display, positions, rotations, and diameters from
the current stream. `setVertexColors()` is called only during initial setup,
so later states retain the original face colors. A viewer-triggered state is a
deterministic session continuation if the entire prior call sequence is fixed;
it is not the token's initial reference state. `[source_static]`

## Interaction profile

| Input | Current implemented effect | Boundary |
|---|---|---|
| Space | Clears temporal memory and generates a new continuing-stream Still Life state | Does not reseed from token hash; not automatically a new canonical token image |
| `P` / `p` | Pauses/resumes rotation | The render loop and alpha-51 feedback continue; a paused orientation can therefore keep accumulating in the memory buffer |
| `S` / `s` | Adds 0.0002 to speed, wrapping above 0.001 to 0.00005 | Changes frame-step increment, not elapsed-time normalization |
| `G` / `g` | Toggles green channel | Implemented in both cases |
| `W` / `w` | Toggles white reconstruction | Implemented in both cases; may coexist with individual flags |
| lowercase `r` | Toggles red channel | Source duplicates lowercase comparison; uppercase `R` is not implemented as published |
| lowercase `b` | Toggles blue channel | Source duplicates lowercase comparison; uppercase `B` is not implemented as published |

The official project page publishes uppercase `R` and `B`. The reviewed source
implements lowercase only for those two controls. This remains an amber
interface/documentation discrepancy and belongs in every display instruction.

## Render pipeline

1. **Ideal coordinates:** twelve pentagonal faces encode a dodecahedron using
   golden-ratio relations. `[source_static]`
2. **Parameterized instances:** full-hash randomness selects one to three
   forms, placement, orientation, diameter, stroke chunk, and display state.
   `[source_static]`
3. **Colored edge raster:** seeded vertex colors interpolate along additively
   blended rotating face boundaries in a 420² off-screen buffer.
   `[source_static]`
4. **Temporal raster memory:** the current buffer enters an uncleared second
   buffer at tint alpha 51, accumulating decaying histories. `[source_static]`
5. **RGB displacement:** the vertex shader samples one channel at a time and
   maps intensity into depth. `[source_static]`
6. **Line-field reconstruction:** every source pixel becomes a possible short
   3D line; selected channel passes receive lateral offsets and RGB or gray
   display colors. `[source_static]`
7. **Orthographic encounter:** the rotated projection lets the viewer infer
   solid, field, dust, and depth from broken traces. `[museum_interpretation]`

### Relation to *923 EMPTY ROOMS*

The two projects share the image-to-depth and line-reconstruction principle,
including separate channel passes, a rotated orthographic view, and short
segments derived from sampled pixels. Their source images and temporal
ontologies differ. *Rooms* generates a multiply blended colorform/gradient
image selected by a finite invocation table; *Cosmos* generates additively
blended dodecahedral edges and then makes their prior frames part of the current
image. *Rooms* is exhaustive in its selection grammar. *Cosmos* is probabilistic
at initialization and open-ended in performance. The shared pipeline is best
understood as a reusable artistic operation whose meaning changes with its
input and time model.

## Exact-token close reading: #248

#248 begins with three dodecahedral instances, the white display branch, and
runtime `metaCHUNK=4`, corresponding to published `CHUNK=3`. The runtime stroke
weight in the source buffer is therefore `4 / 1.2`, before viewport and
downstream projection. The three forms receive separate positions, rotations,
and diameters but share the seeded face-color table. Their colored edge images
are accumulated before white-mode reconstruction turns the three channel
height fields into offset gray passes. `[source_static; execution_instrumented]`

This explains why the governed visual observation can describe granular white
lines and unstable polygonal or dodecahedral suggestions even though the
source begins with colored vector edges. The black intervals are produced at
several stages: the current edge drawing occupies only part of the raster; old
marks decay in memory; the shader discards near-black pixels; and line geometry
separates the remaining samples. The solid is not hidden intact behind the
image. It is proposed by a chain that also fragments it.
`[source_static; execution_observed; museum_interpretation]`

## Collection-wide argument

The project samples an authored probability field rather than enumerating a
Cartesian or combinatorial total. Its 256 tokens are a frozen realization of
that field. The important collection map therefore has two simultaneous views:

- the **score view**, showing authored display and chunk probabilities;
- the **edition view**, showing the exact 256 realized initial states without
  ranking them.

Each token then opens a second axis that metadata does not capture: continuous
frame state and viewer-triggered session continuations. A catalogue that stops
at `CHUNK`, `# COSMOS`, and channel flags describes initial conditions, not the
work's performed temporal object.

The dodecahedron supplies a rigorous perceptual test because a viewer brings a
strong expectation of regular solid form. The work neither simply depicts nor
randomly destroys it. It stages whether recognition can survive successive
technical translations. `[museum_interpretation]`

## Causal-atlas specification

All exhibits are Museum-made analytical surrogates. Every output must bind the
generator/script digest, token hash, environment, initial/session state,
frame/call count, and modification notice.

1. **Five-stage reveal.** Golden-ratio face diagram → one colored edge buffer →
   temporal memory buffer → isolated RGB depth maps → final line field.
2. **Memory laboratory.** Compare the official alpha-51 accumulation with a
   single-frame buffer, frozen memory, and controlled decay values. Only the
   official setting is a work state; alternatives are labeled counterfactual.
3. **One/three Cosmos comparison.** Hold face colors and rendering fixed while
   isolating the three #248 instances, then recombine them to show occlusion,
   additive mixing, and shared color structure.
4. **White anatomy.** Show that white mode is three gray channel passes with
   offsets rather than a luminance collapse. Pair each pass with its z field.
5. **`CHUNK` concordance.** Publish the complete branch-sensitive cross-tab,
   the #248 PRNG trace, runtime stroke weight, and feature-script evidence if it
   is later retained.
6. **Session genealogy.** Starting from a reload, log each PRNG call, spacebar
   event, newly selected state, retained face colors, and memory reset. This
   makes “new Still Life” precise without calling it a new token.
7. **Interface discrepancy.** Demonstrate published uppercase and implemented
   lowercase R/B behavior in a controlled environment, without turning the
   work into a defect display.

## Conservation, display, and reperformance

### Significant properties to preserve

- full token hash and exact two-half `sfc32` seeding;
- 500,000 discarded calls per substream and A/B alternation order;
- branch probabilities, runtime chunk arrays, and form initialization order;
- golden-ratio face coordinates and seeded face colors;
- additive edge drawing, alpha-51 temporal memory, and 420² sampling field;
- RGB-to-depth shader, black mask, channel offsets, gray white-mode passes, and
  rotated orthographic projection;
- continuing PRNG semantics and retained face colors after spacebar;
- lowercase R/B discrepancy, pause/speed behavior, and initial/viewer state
  distinction;
- p5.js 1.9.0 plus browser/GPU/WebGL environment.

### Display protocol

1. Begin with a fresh, logged load of #248; do not press space before the
   initial state is documented and given adequate duration.
2. Present the black field at sufficient black level and contrast to retain
   granular line separation.
3. Publish the actual lowercase R/B implementation beside the official
   uppercase instructions.
4. If visitors may use spacebar, explain that the action begins a continuing
   session state and preserve a reset path to the token's initial state.
5. Log viewport/orientation, browser, p5 build, OS, GPU/driver, pixel ratio,
   refresh/frame cadence, interaction sequence, and run duration.
6. Treat screenshots and behavior films as time-specific documentation, not
   substitutes for the executable work.

### Reperformance matrix

Run the pinned source across at least two browser engines and two GPU/driver
paths, with landscape and portrait viewports. Compare the deterministic
parameter trace first; then compare current edge buffers, temporal-buffer
checkpoints, channel z fields, geometry counts, frame cadence, and perceptual
results. Because feedback compounds small raster differences, later-frame pixel
identity should not be assumed. The conservation review must define acceptable
parameter, structural, temporal, and perceptual equivalence before declaring a
migration faithful.

CC BY-NC 4.0 permits the Museum's noncommercial preservation and adapted
technical work subject to its conditions. Public annotated source, derived
buffers, counterfactuals, and behavior films still require attribution,
license notice, change marking, no implied endorsement, and publication-form
rights review.

## Claim and evidence register

| Claim ID | Claim | Class | Method qualifier | Evidence | Status / boundary |
|---|---|---|---|---|---|
| `COS-CL-01` | #248 is Studio project 0, invocation 248, in a 256-work edition. | B+C | `population_empirical` | object record; frozen snapshot | verified |
| `COS-CL-02` | The generator uses two alternating full-hash `sfc32` streams. | C | `source_static` | current hash-identified project script | supported |
| `COS-CL-03` | Warm-up discards 500,000 values per stream, one million total. | C | `source_static` | loop bounds and two calls per iteration | supported |
| `COS-CL-04` | Initial display probabilities are 10% single, 60% RGB, and 30% white. | C | `source_formal` | `tr` branch thresholds | supported |
| `COS-CL-05` | #248 initially selects three forms, white, and runtime `metaCHUNK=4`. | C | `execution_instrumented` | exact PRNG replay | provisional; retain trace and review independently |
| `COS-CL-06` | Published `CHUNK=3` maps consistently to runtime 4 in white/RGB paths. | C | `execution_instrumented; population_empirical` | 256-token replay cross-tab | provisional operational result; feature-script rationale unresolved |
| `COS-CL-07` | Colored dodecahedral edges enter an uncleared alpha-51 memory buffer. | C | `source_static` | draw path | supported |
| `COS-CL-08` | White mode draws three offset gray channel-derived geometries. | C | `source_static` | shader uniforms and draw passes | supported |
| `COS-CL-09` | Spacebar continues the session PRNG and preserves initial face colors. | C | `source_static` | setup/generate call graph | supported |
| `COS-CL-10` | The reviewed source implements lowercase `r`/`b`, not the published uppercase R/B controls. | B+C | `artist_statement; source_static` | platform instructions and current key comparisons | supported as a documentation/source discrepancy |
| `COS-CL-11` | Official output changed across the accession's two observed frames. | C | `execution_observed` | visual-observation record | verified for that dated environment |
| `COS-CL-12` | The work never repeats. | B | `artist_statement` | Art Blocks and artist accounts | unresolved as an unbounded execution claim |
| `COS-CL-13` | Cosmos is recognizable form persisting through incompatible representations. | E | `museum_interpretation` | pipeline and close looking | supported curatorial proposition |

## Unresolved questions and required review

1. Retain and hash the exact feature script; determine whether `CHUNK` is an
   intentional public scale, a historical source version, or another mapping.
2. Retain lawful exact generator, project-script, p5 dependency, token input,
   and render-environment bytes in an autonomous preservation package.
3. Confirm with artist/studio which spacebar states are artist-designated
   manifestations and which initial state, if any, has reference priority.
4. Determine whether face colors are intentionally invariant across spacebar
   states and document that property in artist/studio language if available.
5. Test whether the zero-copy and CPU readback paths produce materially
   equivalent displacement textures across supported p5/WebGL environments.
6. Establish perceptual-equivalence tolerances for feedback accumulation,
   black masking, additive blending, channel offset, frame cadence, and
   portrait/landscape placement.
7. Rights-review all proposed intermediate buffers, annotated code,
   counterfactuals, and behavior media before public release.
8. Subject the PRNG trace, CHUNK concordance, shader reconstruction, and
   curatorial thesis to independent technical and curatorial review.

## Concise finding

*Ex Nihilo (Cosmos)* is not a dodecahedron decorated by a shader. The work is
the complete passage from ideal coordinate to unstable encounter. #248 makes
that passage especially legible: three colored solids become temporal raster
memory and then three offset white line fields, while `CHUNK=3` names a public
feature whose runtime operation is precisely—but differently—measurable. The
Museum's task is to preserve both the chain of transformations and the
uncertainties at its interfaces.

## Research status and boundaries

- **Status:** constructed research dossier; substantive technical, curatorial,
  rights, accessibility, and conservation review required before public promotion
- **Dossier version:** 0.1.0
- **Research cutoff:** 2026-08-04 UTC
- **Institutional author:** 6529 Network Museum
- **Accession:** `6529NM.2026.001`
- **Museum work:** `6529NM.2026.001.07`, *Ex Nihilo (Cosmos)* #248, 2026
- **System subject:** *Ex Nihilo (Cosmos)*, Art Blocks Studio | 92, fixed
  edition of 256
- **Working standard:** [`Generative system analysis standard`](../../../../docs/generative-system-analysis.md)

This is a research reconstruction of the currently served generator, not a
governed accession amendment, artist-approved technical account, new rights
grant, source-preservation completion claim, or declaration that one frame or
viewer-triggered state is the canonical artwork. It makes no rarity, quality,
price, desirability, or market-ranking claim. Reviewed accession records remain
controlling.

Method labels used in the research apparatus:

- `artist_statement` — artist or authorized-presenter statement;
- `source_static` — fact read from the hash-identified generator source;
- `source_formal` — mathematical or logical consequence of that source;
- `execution_observed` — dated observation of the official generator;
- `execution_instrumented` — working trace or replay made for this research;
- `population_empirical` — result from the frozen 256-token snapshot;
- `museum_interpretation` — contestable institutional reading.
