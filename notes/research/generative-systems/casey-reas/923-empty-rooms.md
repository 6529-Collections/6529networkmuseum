# 923 EMPTY ROOMS: how color becomes space

## Curatorial proposition

The room in *923 EMPTY ROOMS* is not a modeled enclosure. It is the last term
in a translation: a six-digit code selects planar colorforms; the colorforms
move and multiply-blend with a changing gradient; the resulting RGB image is
sampled as three possible height fields; every sampled pixel is rebuilt as a
short line segment; a rotated orthographic view makes that line field available
as space.

The Museum's thesis is that the work makes completeness and instability
coexist. The edition exactly enumerates every non-empty multiset of up to six
items drawn from six colorforms, yet no enumeration determines what a viewer
will see as a room. Code can close the set while time, channels, display, and
perception keep each member open.

## The exact Museum work

| Field | Reviewed fact |
|---|---|
| Object | `6529NM.2026.001.06`, *923 EMPTY ROOMS* #713 |
| Chain identity | `eip155:1/erc721:0x145789247973c5d612bf121e9e4eef84b63eb707/1000713` |
| Native invocation | 713 |
| Token hash | `0x293d12f425921929361c334bbe6402ff4eaf65b29d0b913df133e335f062896e` |
| Published construction | `City=CDMX`; `Primary Form=Pyramid`; `Code=555536` |
| Decoded forms | four Pyramids, one Cargo, one Moon |
| Generator | `https://generator.artblocks.io/1/0x145789247973c5d612bf121e9e4eef84b63eb707/1000713` |
| Generator response SHA-256 | `sha256:2d722fe294710e3b443802baecc1f445b94cf00bf9dbdfbebbb08d4d6d3529e0` |
| Dependency observed | p5.js 1.0.0 via cdnjs |
| Rights boundary | Retained metadata states CC BY-NC 4.0; token title and copyright remain separate |
| Condition boundary | Display-ready with conditions; autonomous software preservation remains active stewardship |

Controlling references are the [reviewed object
record](../../../../records/accessions/6529NM.2026.001/objects/6529NM.2026.001.06.json),
[rights statement](../../../../records/accessions/6529NM.2026.001/rights/6529NM.2026.001.RIGHTS.06.json),
[condition report](../../../../records/accessions/6529NM.2026.001/technical/6529NM.2026.001.06.json),
and [visual-observation
record](../../../../records/accessions/6529NM.2026.001/visual-observation-record.json).

## Evidence and source lock

| Layer | Identity and use | Method and limitation |
|---|---|---|
| Official generator response | URL above; response body 29,782 bytes; SHA-256 `2d722f…529e0` | The 2026-08-04 read-only retrieval reproduced the independently reviewed digest in [`generator-observations.json`](../../../../evidence/casey-reas/generator-observations.json). Bytes were not retained. `[execution_observed]` |
| Inline project script | 29,178 UTF-8 bytes; working SHA-256 `5298304d3583d02f62aaf6e35c1ffd682c52468d69a74073833b7e280032661f` | Extracted in memory from the matching response. This working component hash is not a governed preservation object. `[source_static]` |
| Exact object metadata | [`evidence/casey-reas/raw/metadata/6529NM.2026.001.06.json`](../../../../evidence/casey-reas/raw/metadata/6529NM.2026.001.06.json); SHA-256 `a63ba2…9fcd` | Retained mutable-endpoint response bytes, including token hash, title, features, and CC BY-NC 4.0 label. |
| Full population | [`snapshot.json`](../../../../evidence/casey-reas-collection-snapshots/runs/20260801T172252532Z/snapshots/923-empty-rooms/snapshot.json) and [`descriptor`](../../../../evidence/casey-reas-collection-snapshots/descriptors/923-empty-rooms.json) | Frozen, reviewed 924-token input and transparent NextGen-compatible descriptor. Used for coverage and object position, never for aesthetic rank. `[population_empirical]` |
| Project account | [Bright Moments, “923 Empty Rooms”](https://www.brightmoments.io/923emptyrooms) | Official co-presenter account of six colorforms, six cities, the combination-with-replacement logic, edition size, and display forms. `[artist_statement]` |
| Platform project page | [Art Blocks, “923 EMPTY ROOMS”](https://www.artblocks.io/collection/923-empty-rooms-by-casey-reas) | Official project identity, fixed edition, release date, interaction/animation status, combination counts, and project description. `[artist_statement]` |
| Artist context | [REAS Studio, “Atomism”](https://reas.com/atomism) | Artist-controlled retrospective account of image decomposition and recomposition, Still Life, *An Empty Room*, and *923 EMPTY ROOMS*. `[artist_statement]` |
| Museum scholarship | [Project essay](../../../../records/accessions/6529NM.2026.001/public/projects/atomism-and-923-empty-rooms.md) and [technical research](../../casey-reas-art-technical-research.md) | Reviewed interpretation and source apparatus; not a substitute for generator evidence. |

The source lock establishes a reproducible research target by URL and digest.
It does not satisfy the accession's open duty to retain an autonomous assembled
generator, dependency, input, and render environment.

## Identity, selection, and randomness

### Token-to-room identity

For canonical edition tokens, the visible room selection is not sampled from
the token hash:

```text
projectNumber = floor(tokenId / 1,000,000)
mintNumber    = tokenId mod 1,000,000
index         = mintNumber, when mintNumber < 924
code          = allCombinations[index]
```

Thus token `1000713` selects table index 713 and code `555536` directly. The
source contains a fallback that uses p5's `random(0, 924)` when `mintNumber >=
924`; that branch is outside the released invocation range and is not part of
the 924-token topology described here. `[source_static]`

### Hash-seeded motion

The hash does govern motion details. The source parses
`tokenData.hash.slice(0, 16)` as a JavaScript number and passes it to an `RND`
object. Because the string is `0x`-prefixed, the 16-character slice contains
the prefix and fourteen hash digits. Each `rd()` call applies a three-step
bitwise xorshift and reduces
the absolute signed result modulo 1,000:

```text
s ^= s << 13
s ^= s >> 17
s ^= s << 5
u  = abs_signed(s) mod 1000 / 1000
```

JavaScript's number parsing and subsequent 32-bit bitwise coercion are part of
the algorithm and must be reproduced rather than replaced with an ideal
64-bit integer implementation. Each instantiated colorform consumes this
stream for a moon angle, two motion magnitudes in `[0.0005, 0.002)`, and two
sign decisions. There is no per-frame random draw in the active update loop;
after initialization, frame counters and these fixed velocities drive the
motion. `[source_static]`

This creates an important division of labor: invocation fixes *which* room;
the token hash fixes fine-grained behavior within it.

## Collection topology: proof of the 923 rooms

There are six colorform types. A room contains from one through six forms,
with repetition allowed and order ignored. The number of multisets of size
`k` from six types is

```text
C(6 + k - 1, k) = C(k + 5, k).
```

Therefore

```text
Σ(k=1..6) C(k + 5, k)
= 6 + 21 + 56 + 126 + 252 + 462
= C(12, 6) - 1
= 923.
```

The identity is not enough by itself: a 923-entry list could still contain a
duplicate and omit another multiset. The 2026-08-04 in-memory verification
parsed the current generator table, removed zero padding, sorted the digits of
each ordinary code into canonical multiset form, and compared the result with
an independently generated combinations-with-replacement set. It found:

| Check | Result |
|---|---:|
| Total table entries | 924 |
| Exceptional entry at index 0 | `999999` |
| Ordinary entries, indices 1–923 | 923 |
| Unique canonical multisets | 923 |
| Missing multisets | 0 |
| Extraneous multisets | 0 |
| Duplicate multisets | 0 |
| Counts by size | 6, 21, 56, 126, 252, 462 |
| Entry at index 713 | `555536` |

This is an exact coverage proof plus a table-content verification, not a
probability or rarity analysis. `[source_formal; execution_instrumented]`

### Invocation 0

Index 0 contains `999999`. The parser subtracts one from each non-zero digit,
creating six type indices equal to 8. The active display dispatch implements
only indices 0 through 5, so none of these six objects draws a colorform. The
changing gradient ground and the downstream line-field renderer remain active,
however; the source does **not** justify calling the final display blank.
Whether this exceptional state is artist-designated as the literally empty
room remains unresolved. `[source_static]`

## Algorithmic score

### Colorform vocabulary

The code digit is converted to a zero-based dispatch index:

| Digit | Internal index | Published form | City | Source primitive |
|---:|---:|---|---|---|
| 1 | 0 | Sun | Tokyo | ellipse |
| 2 | 1 | Shard | Berlin | asymmetric four-vertex polygon |
| 3 | 2 | Cargo | London | square |
| 4 | 3 | Hive | New York | six-vertex polygon |
| 5 | 4 | Pyramid | Mexico City | triangle |
| 6 | 5 | Moon | Los Angeles | chord-closed arc |

The form names and city relations are presenter statements; the primitive
dispatch is a source fact. The geometric primitive should not be treated as a
complete definition of the named colorform.

### Per-frame score

```text
INPUT tokenId, tokenHash, viewport

index       ← tokenId mod 1,000,000
code        ← lookup[index]
combination ← [digit - 1 for each non-zero digit in code]
forms       ← initialize one moving VShape for every combination entry
cityPreset  ← tranche(index)

FOR EACH FRAME:
    IF running:
        gradientPhase += 0.0005
        citySpin      += 1

    s  ← (sin(gradientPhase) + 1) / 2
    G  ← four-corner gradient made by interpolating four pastel colors at s

    FOR EACH form:
        motionX += velocityX × speedScalar
        motionY += velocityY × speedScalar
        scale   += 0.05 × (targetScale - scale)
        F       ← draw form with its authored rotations and city color
        G       ← MULTIPLY(G, F)

    FOR EACH pixel (x, y) in the 200 × 200 initial off-screen field:
        FOR EACH enabled channel c in {R,G,B}:
            z ← map(pixel[c], 0..1, -depthNegative..depthPositive)
            construct short 3D segment at (x, y, -z)

    project all segments through scale(1.45), orthographic camera,
    rotateY(0.33), rotateX(-0.33)
```

At the initial resolution, the geometry supplies 40,000 potential line sites
per enabled channel. Each site is expanded to a two-triangle screen-space
line rectangle. Channel passes are slightly offset in x, so enabling several
channels does not merely recolor a single geometry. `[source_static]`

## State and time

| State layer | Contents | Reset/change behavior |
|---|---|---|
| Identity | contract, token ID, invocation, token hash, table code | Fixed for the Museum object |
| Initial phenotype | combination, initial city preset, seeded velocities/angles, initial resolution | Rebuilt on page load; `T` rebuilds at a different resolution while continuing the same `RND` object |
| Frame state | gradient phase, `CDMXSpin`, form rotations and translations, eased scale | Advances by frame, not elapsed wall-clock time; pause-speed state stops the two counters and zeroes movement through `speedScalar` |
| Interaction state | enabled RGB channels, background, city preset, depth, speed, scale, line length, resolution, diagram flag | Viewer mutable; not token identity |
| Environment | viewport, p5/WebGL implementation, GPU/driver, browser timing, pixel readback | May change composition scale, numerical raster result, and cadence |

The work has no terminal frame in the active source. Its continuity is
frame-driven and therefore should be documented by frame count or trace state,
not only by clock time.

## Interaction profile

| Input | Active effect | Analytical meaning |
|---|---|---|
| `+` / `-` | Increments/decrements every form's target scale; actual scale eases toward it | Separates form size from combination identity |
| `D` | Shows/hides the off-screen color-field diagram | Reveals the image that the line field translates |
| Space | Decreases background brightness by 26, wrapping to 255 | Alters ground presentation, not the code or colorforms |
| `R`, `G`, `B` | Toggles channel-specific displacement passes | Makes RGB decomposition directly inspectable |
| `1`–`6` | Applies Tokyo, Berlin, London, New York, CDMX, or Los Angeles render preset | Lets a viewer move a room across presenter-authored display conditions |
| Up/down | Adds/subtracts 26 from both depth bounds | Changes relief amplitude/offset |
| `S` | Cycles speed multipliers `0.25, 0.5, 1, 2, 0` | Includes a source-level still state |
| `0` / `9` | Increases/decreases line-length scalar | Changes the depth-directed extent of every segment |
| `T` | Cycles 150, 200, and 300 source resolutions and rebuilds | Changes sampling density, not simply CSS size |
| `P` | Saves the current canvas | Documentation action; it does not pause |

The Museum should record whether a displayed state is the token's initial
state, a viewer-triggered state, or a deliberately staged analytical state.

## Render pipeline

1. **Lookup:** invocation selects one six-digit entry. `[source_static]`
2. **Parsing:** non-zero digits become form indices 0–5. `[source_static]`
3. **Colorform field:** all selected forms occupy the same off-screen system,
   move slowly in two axes, and are multiply blended over a changing gradient.
   `[source_static]`
4. **Readback:** the p5/WebGL surface is read into pixels and copied into a
   power-of-two WebGL texture with nearest-neighbor sampling. `[source_static]`
5. **RGB-to-depth conversion:** a vertex shader takes the dot product of a
   sampled RGB value with a one-hot channel vector and maps the result into the
   configured negative/positive depth range. `[source_static]`
6. **Line reconstruction:** each pixel coordinate becomes a short 3D segment;
   each enabled channel is a separate pass with a small lateral offset.
   `[source_static]`
7. **Spatial presentation:** the dense line field is viewed through a rotated
   orthographic transform. `[source_static]`
8. **Perceptual completion:** a viewer reads planes, corners, apertures, and
   interiors from that field. This final conversion belongs to encounter, not
   to the source code. `[museum_interpretation]`

### Relation to *Ex Nihilo (Cosmos)*

Both projects use an image as a displacement texture and reconstruct channel
intensities as offset line geometry. They are not the same system. *Rooms*
begins with a finite invocation-indexed colorform multiset, a changing gradient,
and multiply blended planar forms; it exposes city presets, diagram, depth,
resolution, and scale. *Cosmos* begins with full-hash-seeded dodecahedral
edges, additive color, and a temporal feedback buffer; it exposes channel/
white state, speed, pause, and continuing-state regeneration. Shared pipeline
does not imply shared ontology: one translates a combinatorial room, the other
translates ideal geometry and its memory.

## Exact-token close reading: #713

### Causal decoding

`555536` parses to `[4,4,4,4,2,5]`: four Pyramids, one Cargo, and one Moon.
Each receives its own hash-seeded motion parameters, but all are composited
into the same off-screen field. Invocation 713 lies in the source's CDMX
tranche, indices 617–770. Its initial preset is therefore:

| Parameter | #713 initial value |
|---|---|
| Enabled channels | green only |
| Canvas background | 51/255 dark gray |
| Line-length scalar | 0.7 |
| Source resolution | 200 × 200 |
| Depth range | default `-255..+255` mapping; only boundary invocation 617 receives the preset's special `-500..0` range |
| Transform | orthographic; scale 1.45; y rotation 0.33; x rotation -0.33 radians |

That boundary-invocation qualification matters: “CDMX preset” does not imply
that every token in the tranche receives the special depth override. For #713,
the acid-green room is the green-channel depth projection of the six-form
composite under the default symmetric depth bounds. `[source_static]`

The reviewed visual observation describes a bright green and dark, finely
stippled perspectival field whose converging planes appear room-like. The
algorithm explains why green dominates and why the field has relief; it does
not exhaust the visual work. Four Pyramids do not appear as four countable
triangles in the final image because multiply blending, overlap, motion,
sampling, projection, and the viewer's spatial inference intervene between
code and encounter. `[execution_observed; museum_interpretation]`

## Collection-wide argument

*923 EMPTY ROOMS* is exhaustive at exactly one level: the multiset grammar.
The table contains every allowed non-empty selection of up to six forms once.
It is not exhaustive at the levels of animation state, channel display,
depth, form scale, resolution, background, viewport, or human perception.
The collection therefore supplies an unusually exact distinction between a
closed genotype space and an open manifestation space.

The six city tranches organize initial rendering and historical presentation.
They do not authorize reading a channel, color, or primitive as the essence of
Tokyo, Berlin, London, New York, Mexico City, or Los Angeles. The institutional
claim should remain structural: distribution determines conditions of access
and comparison, while the source lets a viewer re-stage presets inside a
single token. `[artist_statement; museum_interpretation]`

## Causal-atlas specification

Every exhibit below is a Museum-made analytical surrogate and must carry the
exact source digest, token input, environment, trace identifier, and change
notice.

1. **The complete-set proof.** An interactive multiset lattice for sizes one
   through six, paired with a machine check that every table row maps to one
   and only one lattice node. Index 0 sits outside the 923-node field.
2. **`555536` reversible pipeline.** Code → six labeled form instances →
   multiply-blended color field → isolated R/G/B textures → z maps → line
   lattice → official #713 state. Every stage can be traversed in both
   directions without presenting an intermediate buffer as the artwork.
3. **Channel anatomy.** Lock form state and camera; compare red, green, blue,
   RGB, and the six presets. This isolates channel selection from motion.
4. **Time anatomy.** Record frames 0, 1, 10, 100, and 1,000 with gradient phase,
   per-form rotation/translation, and `CDMXSpin` values. Pair the animation with
   the source diagram rather than a single screenshot.
5. **Resolution and relief.** Hold state fixed while comparing 150, 200, and
   300 samples and controlled depth/line-length changes. State plainly that
   these are counterfactual analytical runs.
6. **Invocation-zero inquiry.** Show parser state, absent colorform dispatch,
   surviving gradient, and downstream line field. Label artist intent
   unresolved; do not title it “the empty room” without confirmation.

## Conservation, display, and reperformance

### Significant properties to preserve

- exact contract/token/hash/invocation-to-code binding;
- the 924-entry table and exact 923-multiset coverage;
- 16-character `0x`-prefixed hash slicing plus JavaScript bitwise xorshift
  semantics;
- the six form dispatches, movement rules, gradient, and multiply blending;
- RGB channel-to-depth shader equations and per-pixel line geometry;
- initial tranche/preset behavior and the complete interaction map;
- p5.js 1.0.0 dependency, shader behavior, viewport transform, and resolution
  choices;
- the distinction among live work, initial state, viewer state, saved canvas,
  and Museum analytical surrogate.

### Display protocol

1. Begin from a documented reload of token #713 and allow enough duration for
   the field's motion to become legible.
2. Preserve the initial CDMX/green state before inviting interaction.
3. Provide the actual controls; identify `P` as save, not pause.
4. Use a display with adequate black/green separation and avoid environmental
   scaling that crops the canvas.
5. Log browser, p5 build, GPU/driver, operating system, viewport, pixel ratio,
   frame cadence, and any interaction sequence.
6. If the official endpoint is unavailable, distinguish a recorded surrogate
   from an emulated or migrated execution.

### Reperformance and environment matrix

The next conservation experiment should run the pinned source in at least two
browser engines and two GPU/driver paths, at the three internal resolutions
and representative portrait/landscape viewports. Compare parameter traces,
off-screen pixel hashes where stable, channel textures, geometry counts, and
perceptual output. Pixel identity across WebGL environments is not assumed;
the review must define which numerical and perceptual differences are
acceptable before making an equivalence claim.

The reviewed rights statement permits noncommercial preservation and adapted
technical copies subject to CC BY-NC 4.0 conditions. Any public annotated code,
counterfactual image, or behavior film still needs attribution, license notice,
change marking, no implied endorsement, and a rights review of the particular
publication form.

## Claim and evidence register

| Claim ID | Claim | Class | Method qualifier | Evidence | Status / boundary |
|---|---|---|---|---|---|
| `ROOM-CL-01` | The released project contains 924 tokens, invocations 0–923. | B+C | `population_empirical` | frozen snapshot; object record | verified |
| `ROOM-CL-02` | Indices 1–923 exactly enumerate every non-empty multiset of up to six of six forms. | C | `source_formal; execution_instrumented` | current table plus independent generator/check | provisional until trace retention and independent review |
| `ROOM-CL-03` | Index 713 maps to `555536`. | C | `source_static; population_empirical` | generator table; metadata | supported |
| `ROOM-CL-04` | `555536` decodes to four Pyramids, one Cargo, and one Moon. | B+C | `source_static; artist_statement` | parser and dispatch; presenter vocabulary | supported |
| `ROOM-CL-05` | #713 begins in green-only CDMX rendering. | C | `source_static` | tranche and preset branches | supported |
| `ROOM-CL-06` | #713 retains the default symmetric depth bounds. | C | `source_static` | `theDetails()` and `cdmxParams()` boundary test | supported; corrects an easy overgeneralization |
| `ROOM-CL-07` | Form motion is hash-seeded; room selection is invocation-indexed. | C | `source_static` | selection and `RND` paths | supported |
| `ROOM-CL-08` | The source image is multiply blended and converted channel-by-channel to line depth. | C | `source_static` | p5 draw path and vertex shader | supported |
| `ROOM-CL-09` | The official endpoint rendered changing output in the accession observation. | C | `execution_observed` | visual observation and generator transcript | verified for that dated environment only |
| `ROOM-CL-10` | Invocation 0 dispatches no implemented colorform, while its gradient and line renderer remain active. | C | `source_static` | parser, display dispatch, and render path | supported |
| `ROOM-CL-11` | Invocation 0 is artist-intended as the literally empty room. | B | `artist_statement` | no primary confirmation located | unresolved; do not claim |
| `ROOM-CL-12` | The room is produced in translation rather than represented directly. | E | `museum_interpretation` | pipeline plus close looking | supported curatorial proposition, not artist-intent fact |

## Unresolved questions and required review

1. Obtain artist/studio or presenter confirmation of invocation 0's intended
   status and naming.
2. Retain lawful exact generator, project-script, p5 dependency, token input,
   and render-environment bytes in a preservation package.
3. Determine why the special depth overrides apply only to boundary
   invocations 155, 463, and 617 and whether this is a significant authored
   behavior, implementation residue, or documentation issue.
4. Verify whether `T` is intended as a visitor-facing resolution control and
   document its continuation of the existing random stream.
5. Establish cross-browser/GPU tolerances for pixel readback, shader depth,
   additive channel alignment, and frame cadence.
6. Rights-review the proposed reversible buffers, annotated code, screenshots,
   and behavior film before public release.
7. Subject the topology proof, source trace, causal atlas, and interpretation
   to independent technical and curatorial review.

## Concise finding

*923 EMPTY ROOMS* is not merely a collection with a combinatorial theme. It is
an exact finite grammar connected to an open temporal renderer. #713 matters
because its code can be decoded completely while its green line-built room
cannot be reduced to that decoding. A world-class Museum account must preserve
both achievements: proof that the system closes, and close looking at the
experience that refuses to close with it.

## Research status and boundaries

- **Status:** constructed research dossier; substantive technical, curatorial,
  rights, accessibility, and conservation review required before public promotion
- **Dossier version:** 0.1.0
- **Research cutoff:** 2026-08-04 UTC
- **Institutional author:** 6529 Network Museum
- **Accession:** `6529NM.2026.001`
- **Museum work:** `6529NM.2026.001.06`, *923 EMPTY ROOMS* #713, 2023
- **System subject:** *923 EMPTY ROOMS*, Art Blocks x Bright Moments, fixed
  edition of 924
- **Working standard:** [`Generative system analysis standard`](../../../../docs/generative-system-analysis.md)

This dossier reconstructs the currently served generator and gives the exact
Museum token a causal, collection-wide, and conservation-oriented reading. It
does not amend the accession, authenticate artist intent from source code,
declare software preservation complete, privilege an analytical rendering as
the artwork, or make rarity, quality, price, or desirability claims. The
reviewed object, rights, condition, and visual-observation records remain
controlling.

Method labels used in the research apparatus:

- `artist_statement` — artist or authorized-presenter statement;
- `source_static` — fact read from the hash-identified generator source;
- `source_formal` — mathematical or logical consequence of that source;
- `execution_observed` — dated observation of the official generator;
- `execution_instrumented` — working trace or replay made for this research;
- `population_empirical` — result from the frozen 924-token snapshot;
- `museum_interpretation` — contestable institutional reading.
