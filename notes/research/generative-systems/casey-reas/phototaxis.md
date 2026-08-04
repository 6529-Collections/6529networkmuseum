# Phototaxis: the image as a history of sensing

## The curatorial proposition

**One-sentence thesis.** The visible image is delayed evidence of behavior:
sensing becomes steering, steering becomes motion, motion becomes brightness,
and duration becomes graphic density.

Casey Reas describes *Phototaxis* as a simulated environment populated by four differently wired kinds of machines—Explorers, Aggressors, Lovers, and Cowards—whose lines chart their histories of movement. He connects the system to Valentino Braitenberg's *Vehicles* and to code developed for *Path*, *Tissue*, and *MicroImage* beginning in 2001. His 2021 technical note describes a migration from C++ through Processing/Java to p5.js/JavaScript and identifies the 1,000-iteration stop used for the platform thumbnail.

The source makes that history unusually exact. It does not render a body and then trail it. The body is withheld. At each frame, two virtual sensors sample distances to fixed lights; a wiring rule turns those measurements into speed and heading; speed modulates line brightness; and a segment joins the machine's prior coordinate to its new coordinate. The canvas is not cleared. The viewer sees an archive produced one local decision at a time.

The Museum's interpretive claim is therefore narrower and stronger than “simple rules make complexity.” *Phototaxis* makes an image whose marks are evidence but not explanation. A dense knot records repeated movement without exposing which sensor measurement or wiring relation caused any particular turn. The `L` control can reveal the lights, but even then the causal chain remains distributed across hundreds of machines and a thousand updates. The work converts a legible algorithm into a field that exceeds immediate reconstruction.

## Exact Museum work

| Field | Exact value | Authority |
|---|---|---|
| Museum object | `6529NM.2026.001.05` | canonical object record |
| Title | *Phototaxis #308* | canonical object record and retained metadata |
| Artist | Casey REAS | artist/platform metadata |
| Platform/project | Art Blocks Playground, project 164 | retained platform and chain evidence |
| Edition/invocation | 1,000 works; invocation 308 | canonical object record and frozen collection snapshot |
| Contract/token | `0xa7d8d9ef8d8ce8992df33d8b8cf4aebabd5bd270` / `164000308` | canonical object record |
| Token hash | `0x0cfd2dddb2da0dcf086b6a7955e1d0201d0425566962d002be7669742bbec72c` | canonical object record and retained metadata |
| Generator | `https://generator.artblocks.io/1/0xa7d8d9ef8d8ce8992df33d8b8cf4aebabd5bd270/164000308` | canonical object record |
| Dependency observed | p5.js 1.0.0 via cdnjs | reviewed generator transcript |
| License label | CC BY-NC 4.0, with conditions recorded separately | exact rights record; not a Museum grant |
| Accession state | `accessioned` | canonical object and accession records |
| Technical state | `pass_with_conditions`; autonomous software preservation remains in progress | exact technical/condition record |

The token title, copyright, license, executable manifestation, and documentation surrogates remain separate facts. The donor transferred the token interest; no copyright assignment is inferred.

## Evidence method and source lock

This dossier uses the standard qualifiers below.

- `artist_statement`: language or technical history stated by Reas.
- `source_static`: a fact read directly from the reviewed official script or generator wrapper.
- `source_formal`: a mathematical or logical consequence reconstructed from that source.
- `execution_observed`: a dated behavior observed in the official generator under a recorded but possibly incomplete environment.
- `execution_instrumented`: a value produced by a declared analytical runner or trace, distinct from ordinary presentation.
- `population_empirical`: a count computed from the Museum's frozen 1,000-token metadata snapshot.
- `museum_interpretation`: a contestable curatorial argument, not an intent claim.

### Source lock table

| Source | Fixity or date | Use and boundary |
|---|---|---|
| `records/accessions/6529NM.2026.001/objects/6529NM.2026.001.05.json` | reviewed canonical record, payload SHA-256 recorded within it | identity, status, token hash, generator URI, rights/condition links; not source-code preservation |
| `evidence/casey-reas/raw/metadata/6529NM.2026.001.05.json` | `sha256:b6c5bc8b64a2274f9941de3219e7284916f873a4f3092b7934d57e5c12a86573` | exact retained platform response with features and CC BY-NC 4.0 label |
| `evidence/casey-reas/generator-observations.json` | reviewed response `sha256:b3d7c39954beabf85cb6213eff3d57e3b1f7670c6763c663bc426a9c918bcaf3` | response fixity, dependency, controls, 1,000-iteration behavior; response bytes were not retained |
| Official generator, retrieved read-only 2026-08-04T17:50:25Z | 7,914 UTF-8 bytes; same `sha256:b3d7c39954beabf85cb6213eff3d57e3b1f7670c6763c663bc426a9c918bcaf3` | current-response match; no bytes or derived images added to the repository |
| Project script embedded in the reviewed response | 7,308 bytes; `sha256:57a994d9131fbdc79941579e3097d64291fb90bbfd1def3fc847f5df23bcc997` | static reconstruction of the algorithm; a retrieved script observation, not a complete autonomous package |
| Frozen collection snapshot `6529NM.2026.001.phototaxis.metadata.25661488` | observed 2026-08-01T17:22:52.532Z; `sha256:e3eee20294b8a15069c52e31b98ba79a517983f43d185e26cd5e75405a9b10c4` | complete feature population at block 25,661,488; metadata frequency, not aesthetic rank |
| `evidence/casey-reas-collection-snapshots/descriptors/phototaxis.json` | deterministic result `sha256:aa3c6259d0529b84cc42ddbf3dbc209d9d44a320440f80d69b5bd8d91b4a5044` | transparent collection descriptor; its market-style score fields are not used here |
| `records/accessions/6529NM.2026.001/visual-observation-record.json` | controlled observation dated 2026-08-01 | two changed viewport states and a static visual observation; no controls exercised, screenshot bytes not retained |
| Reas, “Notes on ‘Phototaxis’” | 20 September 2021 | artist-authored lineage, behavior, controls, 1,000-iteration reference, and Tissue/MicroImage context |
| Reas, *Phototaxis* project page | accessed during Museum research | artist-authored project description and four named behavioral types |

The official generator and exact artist URLs appear in the source registry at the end of this dossier. Independent publication review should bind every source-static claim to a lawfully retained or reproducibly acquired source object rather than rely on this prose alone.

## Identity and randomness provenance

### Seed formation

The reviewed source initializes one project-specific pseudorandom stream:

```text
seedNumber = parseInt(tokenData.hash.slice(0, 16), 16)
RND.seed = seedNumber
```

`source_static`: `slice(0, 16)` operates on the complete `0x`-prefixed string. For #308 it returns `0x0cfd2dddb2da0d`: fourteen hexadecimal digits after the prefix, not sixteen hash bytes. JavaScript parses that value as the exact Number `3656073155369485`. The first bitwise operation coerces it to signed 32-bit integer `-575481331`, unsigned hexadecimal `0xddb2da0d`.

The `RND` step is:

```text
s = s XOR (s << 13)
s = s XOR (s >> 17)     // signed right shift
s = s XOR (s << 5)
u = abs32(s) mod 1000 / 1000
```

The source expresses `abs32` as `s < 0 ? 1 + ~s : s`. The result lies on a 0.001 grid. This is a bitwise xorshift-derived stream, not a cryptographic random generator. The exact JavaScript signed-shift and 32-bit coercion semantics are constitutive to replay.

### What the stream controls

On a reset, the stream chooses, in order:

1. initial magnification;
2. coordinates for seven potential lights;
3. number of active lights;
4. population size;
5. sensor breadth;
6. heading perturbation magnitude;
7. linear versus nonlinear sensors;
8. maximum speed;
9. color facade;
10. for every machine: initial `x`, initial `y`, expanse, and heading.

The source creates coordinates for all seven potential lights before selecting the active count. Unused light coordinates still consume random values and therefore affect every later state. The machine species is not random: index `i` receives `i mod 4`, cycling evenly through the four source types.

`B` reconstructs `RND` from the same seed and reruns initialization. Keys `1` through `5` also reset first, then override magnification. Under the reviewed source and a compatible runtime, these are seed replays rather than continuations of the existing random stream.

## Exact parameter reconstruction for #308

A transient Node reconstruction of the reviewed JavaScript seed path was run on 2026-08-04. It retained no generator bytes or images. The following values are `source_formal` results; they should become `execution_instrumented` only after an independently reviewed trace runner reproduces them against pinned source bytes.

| Published feature | Internal value and branch | #308 RNG draw | Consequence |
|---|---|---:|---|
| Magnification `0.66` | `_zoom = 0.66` when `u > 0.9` | `0.988` | canvas transform uses 0.66 scale |
| Lights `3` | `_num_lights = 2 + int(u * 6)` | `0.183` | first three of seven generated lights are active |
| Population `Assemblage` | `_num_lines = 200` for `0.75 < u <= 0.85` | `0.848` | 200 machines, 50 of each source type |
| Size `Base` | `_breadth = 50` when `u <= 0.8` | `0.526` | sensors sit 50 world units from machine center |
| Alignment `Neutral` | `_nerves = 5` for `0.8 < u <= 0.9` | `0.894` | each light update adds seeded heading perturbation in `[-5, 5)` degrees |
| Sensors `Nonlinear` | `_linear_sensors = false` when `u <= 0.9` | `0.458` | normalized distance passes through the parabolic `hump` function |
| Speed `Lively` | `_max_speed = 12` when `u <= 0.5` | `0.086` | the highest of the three project speed constants |
| Facade `Atomic A` | facade draw selects color set `cs3` for `0.3 < u <= 0.4` | `0.342` | white ground; blue/gray/cyan/cool-gray type colors |

### The active light field

The first three generated lights are active:

```text
L0 = ( 170,  344)
L1 = ( -94,  466)
L2 = (  -1, -306)
```

Coordinates are in the source's 1,000 × 1,000 world centered on the canvas, with positive `y` downward in p5.js screen coordinates. Two active lights therefore lie below center and one lies almost directly above it. Four additional coordinates are generated and advance the PRNG but remain inactive because `_num_lights` is three.

### Atomic A facade

The `cs3` facade sets a white background and assigns these source colors in species order:

| Source species | RGB before normalization | Display description |
|---|---:|---|
| `V2A` | `(61, 168, 201)` | blue-cyan |
| `V2B` | `(102, 102, 102)` | gray |
| `V3A` | `(68, 182, 198)` | cyan |
| `V3B` | `(118, 153, 153)` | cool gray |

Colors are divided by 255 after the source sets `colorMode(RGB, 1)`. #308 uses base stroke alpha `0.5`; the lower alphas reserved for very large lawful populations do not apply because `_nerves = 5`.

## Algorithmic score

The work can be stated as a score without pretending the score is the experience:

```text
INPUT
  token hash H; viewport width W and height Ht

RESET
  seed one signed-32-bit xorshift-derived stream from the leading hash substring
  choose zoom, seven potential lights, active-light count, population,
  sensor breadth, nerves, sensor response, maximum speed, and facade
  create N machines at seeded positions and headings
  assign source type i mod 4 and its facade color
  clear the canvas once to the facade background

FOR EACH FRAME t
  FOR EACH machine i
    freeze its sensor orientation at the heading at frame start
    FOR EACH active light j, in array order
      measure left and right sensor distances
      normalize distances by the world diagonal
      if nonlinear, transform both signals through a parabola
      update speed and heading according to source type
      add a seeded heading perturbation
    derive target brightness from the resulting speed
    ease current color toward target brightness
    enforce minimum movement speed
    advance position using final heading and speed

  FOR EACH machine i
    draw one alpha-composited segment from prior to current position
    store current position as prior position

  if requested, draw the active lights over the trace field
  after drawing frame 1,000, stop the loop
```

Three details matter. All machines update before any machine displays, so the trace at a frame is a synchronized population state. Sensor orientation is calculated once per machine per frame, even though heading changes sequentially while processing the lights. The background is not cleared during `draw()`, so the canvas is a cumulative state, not a view regenerated solely from the current positions.

## Sensor geometry and signal function

Let machine position be `p = (x, y)`, its frame-start heading be `theta`, sensor breadth be `b`, and active light `j` have position `ell_j`.

```text
leftSensor  = p + b (cos(theta + pi/5), sin(theta + pi/5))
rightSensor = p + b (cos(theta - pi/5), sin(theta - pi/5))

dL_j = ||ell_j - leftSensor||
dR_j = ||ell_j - rightSensor||

nL_j = dL_j / 1414.2136
nR_j = dR_j / 1414.2136
```

The constant `1414.2136` approximates the diagonal of the 1,000-unit square. For nonlinear tokens such as #308, the source then applies:

```text
hump(n) = 1 - [2(n - 0.5)]^2 = 4n(1 - n)
a_j = [hump(nL_j) + hump(nR_j)] / 2
```

For linear tokens, `a_j = (nL_j + nR_j) / 2` without the parabola. The source does not clamp `n` before or after `hump`. Within the nominal square and for sensor points near it, the function is zero at normalized distance 0 and 1 and maximal at 0.5. If a machine travels far enough that normalized distance exceeds 1, the parabola becomes negative. That extension is a code-derived behavior, not an artist-stated intention.

## The four Braitenberg-derived source types

The script defines species constants `V2A`, `V2B`, `V3A`, and `V3B`. Reas separately names the project's four behavioral kinds Explorers, Aggressors, Lovers, and Cowards. The reviewed minified project script does not encode a human-readable name-to-constant lookup. A conventional Braitenberg correspondence may be historically plausible, but this dossier does not turn that plausibility into a source fact. Until the feature script, unminified source, or artist/studio confirmation establishes the bijection, public technical exhibits should label the equations by source constant and present the four artist names as the project's stated vocabulary.

For one light update, let current speed be `v`, maximum speed `M`, machine-specific expanse `e`, and divisor `D = 2 + e / 25`. Let:

```text
qL_j = (dL_j / 8) (1 - nL_j)
qR_j = (dR_j / 8) (1 - nR_j)
epsilon_j = seeded draw in [-nerves, nerves)
```

Here `nL_j` and `nR_j` mean the post-`hump` values for a nonlinear token. The exact per-light recurrences are:

| Source type | Speed after light `j` | Heading change after light `j` |
|---|---|---|
| `V2A` | `(v + M(1 - a_j)) / D` | `+qL_j - qR_j + epsilon_j` |
| `V2B` | `(v + M(1 - a_j)) / D` | `+qR_j - qL_j + epsilon_j` |
| `V3A` | `(v + M a_j) / D` | `-qL_j + qR_j + epsilon_j` |
| `V3B` | `(v + M a_j) / D` | `-qR_j + qL_j + epsilon_j` |

These recurrences execute sequentially for every active light. With three lights, #308 updates speed three times and adds three deterministic perturbations for every machine in every frame. All three measurements use the frame-start sensor orientation and machine position; the final speed and heading move the machine only after the light loop ends.

The equations reveal two crossed pairings. `V2A` and `V3B` share a turn-sign formula while using opposite speed-response families. `V2B` and `V3A` share the other turn-sign formula. The four types are therefore not four unrelated behaviors: they are the Cartesian combination of two speed responses and two steering signs, plus the common expanse divisor and token-level perturbation.

## Motion, brightness, and trace

After the light loop, the source constructs target color from the machine's original facade color and current speed:

```text
brightnessFactor = map(M, 4, 12, 0.45, 0.15)
targetRGB = clamp(originalRGB * speed * brightnessFactor,
                  0, originalRGB)
currentRGB = currentRGB - (currentRGB - targetRGB) / 10
speed = max(speed, 0.4)
position = position + speed (cos(theta), sin(theta))
```

The map gives factors 0.45, 0.30, and 0.15 for maximum speeds 4, 8, and 12. Brightness is calculated before the minimum movement-speed floor, then eased over time. Reas's statement that color decreases in brightness when an organism moves slowly is thus visible in the code as an evolving, bounded mapping rather than a one-frame direct assignment.

Each display step draws a one-pixel, square-capped, alpha-composited segment from the new position to the preceding position. No background clear follows initialization. Crossings accumulate opacity and color, turning recurrence into density. The line's length records distance moved in one update; its curvature becomes legible across consecutive segments; its color records a smoothed relation to recent speed.

## State and time model

The work has multiple states that must not be collapsed.

### Fixed token state

- token hash and derived PRNG trajectory;
- potential and active light positions;
- number and source types of machines;
- breadth, nerves, sensor mode, maximum speed, and facade;
- seeded initial positions, headings, and expanses.

### Evolving simulation state

- per-machine position, previous position, heading, speed, and eased display color;
- the continuing PRNG state consumed by heading perturbations;
- the accumulated canvas pixels;
- iteration counter `bangTime`.

### Encounter state

- paused/running state;
- light overlay visible/hidden;
- magnification selection;
- elapsed continuation after the 1,000-frame reference stop.

### Environment state

- viewport width and height at setup;
- browser, JavaScript, p5.js, Canvas 2D, device-pixel-ratio, color-compositing, and frame-scheduling behavior;
- display hardware and capture pipeline.

The code does not set a frame rate. p5.js normally schedules draws through the browser, so 1,000 iterations is a logical duration, not a guaranteed number of wall-clock seconds. Each of the first 1,000 draws updates and renders the population, then increments `bangTime`. When the incremented value equals 1,000, the source sets pause and calls `noLoop()`. Pressing `P` after that stop resumes at frame 1,001; because the stop condition tests equality rather than `>=`, the continued run does not automatically halt again.

The 1,000-frame image is an artist- and platform-documented reference manifestation used for the thumbnail. It is not the only permissible state and is not yet verified as pixel-identical across environments.

## Interaction semantics

| Input | Source behavior | State category | Museum display note |
|---|---|---|---|
| `P` | toggle `loop()` / `noLoop()` and pause flag | encounter/time | make continuation beyond frame 1,000 explicit |
| `B` | reseed, reconstruct world and machines, clear ground, restart loop | token replay | call it a reset or “big bang,” not a new token state |
| `1` | reset, then set zoom `0.66` | replay plus display transform | for #308 this equals its seeded magnification |
| `2` | reset, then set zoom `1` | replay plus display transform | analytical/viewing scale, not trait mutation |
| `3` | reset, then set zoom `2` | replay plus display transform | same |
| `4` | reset, then set zoom `4` | replay plus display transform | same |
| `5` | reset, then set zoom `8` | replay plus display transform | same |
| `L` | toggle light overlay; if paused, request one `redraw()` | encounter/revelation | while paused, the requested redraw also executes one update frame under the reviewed code |

The last point is easy to miss. The light overlay is not an external static annotation. When `L` is pressed during a pause, `redraw()` runs the complete draw routine once: machines update, a new segment is deposited, the counter advances, and lights are displayed. A conservation test should confirm this behavior in the pinned runtime before publication.

The viewer cannot move the lights in the reviewed *Phototaxis* source. Reas's earlier *Tissue* text describes audience-positioned stimuli in that earlier work; applying that interaction to the Art Blocks edition would confuse the lineage with the present implementation.

## Boundary behavior and dormant code

`source_static`: the active update path has no boundary clamp, wrap, bounce, cull, or automatic rebirth. A machine can leave the nominal `[-500, 500]` world. Its sensors and distance equations continue to run; its line continues to accumulate wherever the canvas transform makes it visible. This provides an algorithmic basis for paths that leave the central field, including the long departures observed in #308. It does not make any one departure an intentional symbol.

The class contains `kill()` and `rebirth()` methods and a conditional fade/death branch. In the reviewed project script, no active caller invokes `kill()`, every machine begins with `death = false`, and the path therefore remains dormant. The dormant branch also contains an unqualified `fade` reference that would require investigation if the death path were activated. Because it is not active in the reviewed execution path, this dossier records it as conservation-relevant dormant code, not as a defect in the encountered work.

The nonlinear sensor function is also unbounded after a machine leaves the nominal world. Normalized distances above one can produce negative `hump` values, which then feed speed and steering. A future instrumented trace should test whether this regime contributes to returning, accelerating, or further escaping paths in #308 rather than infer the outcome from a still.

## Render and display pipeline

```text
token hash
  -> signed-32-bit, 0.001-grid PRNG
  -> fixed world and machine initialization
  -> sensor distances to fixed lights
  -> optional nonlinear signal
  -> type-specific speed and steering
  -> seeded heading perturbation
  -> position update and speed-derived color
  -> alpha line segment on an uncleared Canvas 2D surface
  -> centered viewport transform and optional light overlay
  -> accumulated visible field
```

The canvas fills `window.innerWidth × window.innerHeight` at setup. The coordinate origin is translated to the viewport center. Scale is:

```text
max(viewportWidth, viewportHeight) / 1000 * zoom
```

Using the larger viewport dimension means framing changes with aspect ratio: a non-square viewport may crop more of one world axis. There is no reviewed window-resize handler. The seeded composition and the encountered crop must therefore be recorded separately. Pixel density, antialiasing, alpha compositing, and display color can alter appearance even when the simulation state is the same.

The active lights, when shown, are orange circles of diameter ten world units drawn after the machine paths. Their visibility is a source-provided causal disclosure layer, not a replacement for the path image.

## Close reading of *Phototaxis #308*

The Museum's published observation describes pale cyan and gray trajectories forming an outer elliptical circulation around a dense lower-central knot, a second convergence near the upper center, and long paths escaping beyond the field. That description is an observation of a documentation state, not a complete account of live behavior.

The reconstruction gives the close looking a causal question. In p5.js coordinates, #308 has two lower lights at `(170, 344)` and `(-94, 466)` and one upper light at `(-1, -306)`. It is plausible that repeated responses to the two lower stimuli contribute to the visually heavier lower knot while the single upper stimulus contributes to the smaller upper convergence. This is `museum_interpretation`, not yet a traced attribution: paths overlap, four wiring types respond differently, nonlinear distances are nonmonotonic, and seeded perturbation is applied three times per frame. The causal atlas should prove or refute the proposed relation by logging each segment's machine type and light-response terms.

#308's recorded tuple creates a particularly productive tension:

- **200 machines:** enough paths for collective density while retaining more open ground than the 400- and 800-machine configurations;
- **50 of each source type:** chromatic and behavioral differences begin from an exactly balanced population;
- **nonlinear sensors:** distance is folded through a parabola rather than treated as a direct gradient;
- **neutral alignment:** three `[-5, 5)` degree perturbations per frame make deviation part of every machine's active state;
- **lively speed:** the speed constant is 12, but the expanse divisor, repeated light updates, and minimum floor make actual motion stateful rather than uniformly fast;
- **0.66 magnification:** the view contracts the world, allowing more outward-traveling history to remain visible;
- **Atomic A:** two blue-cyan and two gray families give the balanced four-type population an atmospheric cool register.

The exact object therefore matters. A generic account of “agents attracted to lights” would miss the paired lower stimuli, upper stimulus, balanced types, nonlinear response, repeated perturbation, and expanded view that structure this particular field.

## Collection topology

The 1,000-work edition samples an authored branch structure rather than enumerating every parameter combination. The following counts are `population_empirical` results from the frozen complete snapshot. They describe feature prevalence only.

| Axis | Frozen edition counts | #308 position |
|---|---|---|
| Size | Base 815; Small 185 | Base |
| Speed | Lively 512; Steady 305; Slow 183 | Lively |
| Lights | 2: 165; 3: 159; 4: 163; 5: 166; 6: 170; 7: 177 | 3 |
| Facade | Toxic A 135; Toxic B 138; Atomic A 91; Atomic B 112; Atomic C 120; Frontier 305; Silt 99 | Atomic A |
| Sensors | Nonlinear 905; Linear 95 | Nonlinear |
| Alignment | Lawful 788; Neutral 110; Chaotic 102 | Neutral |
| Population | Cluster 738; Assemblage 109; Small is beautiful 101; Swarm 52 | Assemblage |
| Magnification | 1.0: 806; 0.66: 100; 2.0: 94 | 0.66 |

Static reconstruction across all 1,000 frozen token hashes maps the published names to source values as follows:

- Base/Small -> sensor breadth 50/35;
- Lively/Steady/Slow -> maximum speed 12/8/4;
- Lawful/Neutral/Chaotic -> perturbation magnitude 0/5/10;
- Cluster/Assemblage/Small is beautiful/Swarm -> 400/200/50/800 machines;
- Atomic A -> `cs3` facade;
- Nonlinear -> `_linear_sensors = false`;
- published magnification -> seeded `_zoom`.

These mappings are stronger than visual guesses because every label/value pairing was checked across the frozen population. They remain tied to the reviewed source and snapshot versions. No count should be presented as a hierarchy or measure of the object's merit.

## Causal atlas specification

Every atlas element below must be labeled **6529 Network Museum analytical surrogate**, bound to exact source and environment hashes, and marked as an adaptation where shared under CC BY-NC 4.0. None is a newly discovered canonical artwork state.

### Exhibit 1: Hidden causes / visible memory

Synchronize the ordinary #308 trace with a second view showing the three active lights and current machine positions. Allow a visitor to scrub frames 1, 10, 100, and 1,000 while keeping the official trace untouched in one panel. The key question is when the two knots become stable perceptual structures.

### Exhibit 2: One segment, fully accounted for

For a selected machine and frame, show:

```text
sensor coordinates
-> three pairs of raw distances
-> normalized or humped signals
-> three sequential speed/turn updates
-> three perturbation draws
-> final speed and heading
-> target and eased color
-> deposited line segment
```

The exhibit must retain machine index, source type, frame, light order, prior PRNG state, and numeric precision.

### Exhibit 3: Four source types under identical conditions

Clone one initial position, heading, expanse, lights, and perturbation stream into four Museum analytical runs differing only in `V2A`, `V2B`, `V3A`, or `V3B`. This isolates the two speed families and two steering signs. Do not attach the artist's four human-readable behavior names until the name-to-constant mapping is verified.

### Exhibit 4: Linear/nonlinear counterfactual

Replay #308 with only `_linear_sensors` changed. Pair raw distance, parabolic response, and resulting paths. Because `hump` is nonmonotonic and unbounded outside the nominal world, include response curves beyond normalized distance one rather than presenting it merely as “more sensitive.”

### Exhibit 5: Alignment counterfactual

Replay #308 with perturbation magnitudes 0, 5, and 10 while holding the random-draw sequence and every other parameter fixed. Report whether the source runner can fairly hold sequence consumption constant; changing a branch must not accidentally shift later random state.

### Exhibit 6: Light ablation and contribution

Run three one-light analyses and three leave-one-out analyses while retaining #308's initialization. Compare density maps and machine-type occupancy around the observed lower and upper knots. These are diagnostic experiments, not claims that the artwork has one-light states.

### Exhibit 7: Boundary study

Mark the nominal 1,000-unit square and record first-exit frame, maximum distance, normalized sensor values, and whether each machine re-enters by frame 1,000. Pair the results with zoom 0.66, 1, and 2 framing to separate simulation escape from viewport cropping.

### Exhibit 8: Drawing as accumulation

Provide synchronized views of current positions only, last-ten-frame segments, and the full accumulated canvas. This demonstrates that the image is neither a particle snapshot nor a neutral path map: alpha compositing and eased brightness materially construct its memory.

### Minimum trace schema

Each trace row should include source hash; dependency hash; browser/runner identity; token hash; frame; machine index; source type; prior and current position; frame-start and final heading; speed before/after each light; expanse; light index and coordinate; sensor coordinates; raw, normalized, and transformed distances; turn terms; perturbation draw; target/current color; line alpha; viewport; zoom; and accumulated-canvas checkpoint hash. Tests must fail closed if source or dependency bytes drift.

## Conservation, display, and reperformance

### Constitutive identity to preserve

- exact Ethereum object identity and token hash;
- exact project script and wrapper assembly path;
- exact p5.js 1.0.0 dependency bytes or authoritative dependency-registry reconstruction;
- JavaScript Number, signed shift, bitwise coercion, and Canvas 2D semantics;
- token-specific seed replay and initialization order, including unused potential lights;
- cumulative alpha line drawing and the 1,000-frame reference stop;
- source-provided controls and their state-transition behavior.

### Environment matrix to build

Test pinned Chrome/Chromium, Firefox, and WebKit where supported, across at least Windows and Linux, with declared viewport, device pixel ratio, color profile, hardware acceleration, browser version, p5.js bytes, and frame scheduling. Compare simulation traces before comparing pixels. If state traces match but raster hashes differ, document the difference as rendering variance rather than algorithmic divergence.

The first validation oracle for #308 should assert the seed substring, signed 32-bit seed, seven generated light coordinates, active-light count, parameter tuple, first several machine initializations, and the first several frames of selected machines. Functional tests should cover deterministic reset, all five magnification keys, pause/resume, frame-1,000 stop, continuation beyond 1,000, light toggle while running, and the single-frame advance caused by light toggle while paused.

### Display recommendation under review

Use the executable manifestation as the primary presentation when a validated environment is available. Begin from a reset and allow the 1,000-frame reference state to form. Offer `P`, `B`, `1`-`5`, and `L` with plain-language labels and make clear that scale keys reset the simulation. If unattended operation continues beyond frame 1,000, disclose that this is a source-permitted continuation rather than the platform thumbnail state.

Record viewport, pixel density, display dimensions, elapsed iterations, and whether lights are shown for every exhibition. Do not call a static PNG the artwork or claim it preserves behavior. A still, frame ladder, trace, and behavior film are documentation surrogates with their own fixity and rights notices.

No authoritative artist installation specification for monitor model, physical scale, luminance, browser, or viewing duration is currently recorded in the accession dossier. Museum display parameters must be identified as institutional choices until artist/studio guidance says otherwise.

### Preservation package still required

The accession condition record correctly remains amber for script, dependencies, rendering, behavior, and documentation. The next package should retain exact generator/wrapper bytes where rights and policy permit; on-chain project and token inputs; exact dependency bytes; an offline assembly route; a trace runner; environment manifests; reference stills; a behavior film; interaction tests; and hashes. It should distinguish the official live work, platform reference manifestation, Museum reperformance, and Museum analytical adaptations.

## Claim and evidence register

| Claim ID | Claim | Class | Method qualifier | Evidence | Status / publication condition |
|---|---|---|---|---|---|
| `PHO-CL-01` | Reas connects the project to Braitenberg and the Path/Tissue/MicroImage lineage. | B | `artist_statement` | artist project page and 2021 technical note | verified as Reas's account |
| `PHO-CL-02` | The edition's initial thumbnail state stops after 1,000 iterations. | B+C | `artist_statement; source_static` | technical note; reviewed script equality stop | supported |
| `PHO-CL-03` | #308 has the published tuple Base/Lively/3/Atomic A/Nonlinear/Neutral/Assemblage/0.66. | B | `artist_statement` | retained platform metadata and canonical object record | verified as published metadata |
| `PHO-CL-04` | That tuple maps to breadth 50, speed 12, three active lights, `cs3`, nonlinear `hump`, nerves 5, 200 machines, and zoom 0.66. | C | `source_formal; population_empirical` | reviewed source; frozen snapshot | provisional pending independent trace review |
| `PHO-CL-05` | #308 contains exactly 50 machines of each source type. | C | `source_formal` | 200 machines and `species = index mod 4` | supported |
| `PHO-CL-06` | Three active lights are `(170,344)`, `(-94,466)`, and `(-1,-306)`. | C | `execution_instrumented` | exact seed replay against reviewed source | provisional pending independent trace review |
| `PHO-CL-07` | Each frame applies one perturbation per active light. | C | `source_static` | perturbation call lies inside the light loop | supported |
| `PHO-CL-08` | The active path has no boundary correction and can leave the nominal world. | C | `source_static; source_formal` | reviewed `idle()` and absence of active boundary calls | supported; do not infer intent |
| `PHO-CL-09` | `kill()` and `rebirth()` are dormant in the reviewed path. | C | `source_static` | current class and call-site review | supported for bound source only |
| `PHO-CL-10` | The lower and upper knots correspond to the two lower and one upper light configurations. | E | `museum_interpretation` | visual observation plus reconstructed coordinates | provisional; causal atlas must test |
| `PHO-CL-11` | The source response matched the reviewed byte length and hash on 2026-08-04. | C | `execution_observed` | read-only response length/hash comparison | verified for that retrieval; bytes not retained |
| `PHO-CL-12` | The work is pixel-identical across browsers or reloads. | C | `execution_observed` | no complete cross-environment execution study | unresolved; do not publish as fact |
| `PHO-CL-13` | Source constants map exactly to Explorer/Aggressor/Lover/Coward. | B+C | `artist_statement; source_static` | artist vocabulary and source constants exist, but reviewed source lacks lookup | unresolved; require primary confirmation |

## Unresolved questions and review gates

1. Which source constant—`V2A`, `V2B`, `V3A`, `V3B`—maps to each artist name? Obtain the feature script, unminified source, or artist/studio confirmation before joining names to equations.
2. Can exact generator wrapper, project script, on-chain assembly inputs, and p5.js 1.0.0 bytes be retained in a rights-compliant autonomous package?
3. Does a pinned full-browser trace reproduce the transient #308 initialization values and first-frame states exactly?
4. How much raster variation occurs across browser engines, GPU/CPU compositing paths, device-pixel ratios, and color profiles when state traces match?
5. Do machines leaving the nominal world contribute materially to #308's observed long departures, and how often do they re-enter before frame 1,000?
6. Does toggling `L` while paused advance exactly one frame in all supported p5.js 1.0.0 environments?
7. Which manifestations does Reas or the studio recognize as preferred for museum display: forming trace, 1,000-frame stop, continued run, light-revealed state, or a sequence among them?
8. What physical scale, brightness, duration, and visitor-control policy are appropriate, given the absence of an accessioned installation specification?
9. Should the 2021/2022 date discrepancy be resolved through artist/studio clarification or retained as a documented difference between edition history and current register?
10. Which causal-atlas counterfactuals may be publicly distributed under CC BY-NC 4.0, and which should remain controlled conservation research?

Publication requires independent source review, trace reproduction, curatorial review, conservation review, rights review for analytical adaptations, and explicit promotion through the repository's governed workflow. Until then, this file is the durable research record of a reconstructible argument, not the final public interpretation.

## Source registry

### Canonical and retained local sources

- `records/accessions/6529NM.2026.001/objects/6529NM.2026.001.05.json`
- `records/accessions/6529NM.2026.001/technical/6529NM.2026.001.05.json`
- `records/accessions/6529NM.2026.001/rights/6529NM.2026.001.RIGHTS.05.json`
- `records/accessions/6529NM.2026.001/visual-observation-record.json`
- `records/accessions/6529NM.2026.001/public/6529NM.2026.001.05.md`
- `records/accessions/6529NM.2026.001/public/projects/microimage-and-phototaxis.md`
- `records/accessions/6529NM.2026.001/public/source-and-chronology-matrix.md`
- `notes/research/casey-reas-art-technical-research.md`
- `evidence/casey-reas/raw/metadata/6529NM.2026.001.05.json`
- `evidence/casey-reas/generator-observations.json`
- `evidence/casey-reas-collection-snapshots/runs/20260801T172252532Z/snapshots/phototaxis/snapshot.json`
- `evidence/casey-reas-collection-snapshots/descriptors/phototaxis.json`
- `notes/wip/2026-08-04-generative-systems-analysis-standard.md`
- `docs/generative-system-analysis.md`

### Exact official and artist URLs

- Official live generator: `https://generator.artblocks.io/1/0xa7d8d9ef8d8ce8992df33d8b8cf4aebabd5bd270/164000308`
- Art Blocks token page: `https://artblocks.io/token/1/0xa7d8d9ef8d8ce8992df33d8b8cf4aebabd5bd270/164000308`
- Art Blocks token API recorded by the accession: `https://api.artblocks.io/token/164000308`
- Casey Reas project record: `https://www.gray.reas.com/phototaxis/`
- Casey Reas, “Notes on ‘Phototaxis’”: `https://medium.com/@REAS/notes-on-phototaxis-db7aa7641ad8`
- Casey Reas, *MicroImage*: `https://reas.com/microimage`
- Casey Reas NFT register carrying the unresolved 2022 listing: `https://reas.com/nfts`

## Research status and boundaries

- **Working record type:** `GENERATIVE_SYSTEM_DOSSIER`
- **Dossier status:** research draft for independent technical, curatorial,
  conservation, rights, and accessibility review
- **Project:** Casey Reas, *Phototaxis*, Art Blocks Playground project 164,
  edition of 1,000
- **Museum object:** `6529NM.2026.001.05`, *Phototaxis #308*
- **Native object:** `eip155:1/erc721:0xa7d8d9ef8d8ce8992df33d8b8cf4aebabd5bd270/164000308`
- **Research date:** 2026-08-04 UTC
- **Working standard:** [`Generative system analysis standard`](../../../../docs/generative-system-analysis.md)

This is a research dossier, not a governed object record or an amendment to
the accession. It does not assign new rights, prove artist intent from code,
declare autonomous preservation complete, establish a canonical pixel state,
or make claims about price, value, quality, desirability, or feature rarity.

The code analysis concerns the official generator response bound by the source
lock. A code path is not automatically an artist statement. A formally derived
behavior is not automatically an observed browser event. A Museum-made
counterfactual is an analytical surrogate, not a state of the artwork.

The artist and Art Blocks sources date the edition and its release to 2021;
the current artist NFT register lists *Phototaxis* as 2022. The Museum records
the discrepancy and uses 2021 for this Art Blocks edition without silently
resolving the later register entry.
