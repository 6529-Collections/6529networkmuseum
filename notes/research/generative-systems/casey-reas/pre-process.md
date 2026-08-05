# Pre-Process: an exhaustive score performed through collision

## Curatorial thesis

**One-sentence thesis.** *Pre-Process* sets a finite, exhaustive score of 120
starting conditions against an open-ended performance in which collisions
turn a population of simple circles into different kinds of visible evidence.

REAS describes one hundred circular Elements governed by four behaviors:
straight movement, surface constraint, directional change on contact, and
movement away from overlap. He identifies eight surfaces, three origins, and
five growth configurations, and says the 120-work edition contains every
significant permutation.[^artist] The source does something unusually strong:
it assigns those three axes by invocation number through congruences modulo 8,
3, and 5. The edition's completeness can therefore be proved, not merely
inferred from labels.

The system is exhaustive in one sense and inexhaustible in another. Its
starting coordinate is one of exactly 120. Once running, however, one hundred
elements are progressively admitted into an order-dependent collision system,
and eight surfaces decide what aspects of that system remain visible or are
accumulated. The Museum interprets those surfaces as eight epistemic views:
not skins over an unchanged image, but different accounts of what counts as
evidence of behavior.

The Museum's #63 makes that argument with unusual clarity. `Origin 1` places
all elements at the center; `Growth 4` gives them one equal, large radius; and
`Surface 8` suppresses centers and direction markers while retaining pale
perimeters and a translucent black contact network on an uncleared light
field. The rows and dark axes in the official still are therefore not an
input "horizontal-line origin"—#63 does not have that origin. They are an
accumulated consequence of center-born bodies moving, contacting, and being
separated. That last sentence is Museum interpretation [E] supported by the
source and exact-object observation, not an artist-intent claim.

## Exact Museum scope

| Museum object | Exact work | Chain/object citation | Authoritative token inputs | Governed record |
|---|---|---|---|---|
| `6529NM.2026.001.04` | Casey REAS, *Pre-Process #63*, 2022 | `eip155:1/erc721:0x99a9b7c1116f9ceeb1652de04d5969cce509b069/383000063` | invocation `63`; hash `0x0d800ffd4ec82f477918afd163ef9089a92f6b6bb5e81247671bbad6a27bcbd0` | [`objects/6529NM.2026.001.04.json`](../../../../records/accessions/6529NM.2026.001/objects/6529NM.2026.001.04.json) |

The work is accessioned in lot `6529NM.2026.001`. The ERC-721 identifies the
work and its provenance; it is not by itself the running screen image. Token
title, copyright, license, custody, and software preservation remain distinct.

## Evidence and source lock

| Source/component | Exact reference | Fixity/version | Retention and evidentiary boundary |
|---|---|---|---|
| Official generator | [Art Blocks generator for token 383000063](https://generator.artblocks.io/1/0x99a9b7c1116f9ceeb1652de04d5969cce509b069/383000063) | reviewed response SHA-256 `8cbf3ee01db1a864163eeb5b30776372917256b9246b255e0f514cf03b64505b`; working decoded inline-script SHA-256 `1963439a07180ea603df530fa138f56e6d464c01b18608ae2430be4f7c028e9b` | Response hash independently reviewed [C]; response bytes not retained. Inline-script hash is a 2026-08-04 in-memory observation that includes token data and is not preservation evidence. |
| Runtime dependency | `https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.0.0/p5.min.js` | p5.js `1.0.0` declared by the reviewed response | Remote dependency; exact bytes are not bound by the current public package. |
| Generator transcript | [`evidence/casey-reas/generator-observations.json`](../../../../evidence/casey-reas/generator-observations.json) | reviewed commit `514cb18aee37b0d04c3eeb59703b411ea34f6bf9`; transcript SHA-256 `a2e6a2295ffdbee3332fdeec7cd9e044d4bc5313cd63f9d6e5b67e01c3ac79da` | Retained independent observation [C], explicitly not raw-source retention. |
| Exact platform metadata | [`raw/metadata/6529NM.2026.001.04.json`](../../../../evidence/casey-reas/raw/metadata/6529NM.2026.001.04.json) | SHA-256 `581bb33a3d97b9c411483523fb1272ea605064d9bcbc3dd7d42815a681bccbc5` | Retained exact response [B/C]; records Surface 8, Origin 1, Growth 4, aspect ratio, hash, URLs, and license label. |
| Complete edition snapshot | [`descriptors/pre-process.json`](../../../../evidence/casey-reas-collection-snapshots/descriptors/pre-process.json) | 120/120 tokens; descriptor SHA-256 `b88b1b57d5ef18a9b2edeb28687779a36a94dddeae1df9bb00c82f494aada3b3`; result SHA-256 `d91b94efdb923b18af0f15cad0c05aeb2c1ce343376019f0eb8cc29bf59b154f` | Retained, pinned population evidence. It confirms coordinate counts; its scoring fields are not used here. |
| Controlled visual observation | [`visual-observation-record.json`](../../../../records/accessions/6529NM.2026.001/visual-observation-record.json) | `6529NM.2026.001.VO-01`; completed 2026-08-01T23:34:36.244Z for #63 | Two non-retained screenshot hashes differed after a minimum 1,500 ms wait [C]. No reset, pause, or surface key was exercised. |
| Artist/project account | [Art Blocks interview, 28 November 2022](https://www.artblocks.io/articles/in-conversation-with-casey-reas-on-pre-process); [project page](https://www.artblocks.io/collection/pre-process-by-casey-reas) | official/primary sources | Artist statement [B], not source-code proof. |
| Museum interpretation | [`public/projects/process-and-pre-process.md`](../../../../records/accessions/6529NM.2026.001/public/projects/process-and-pre-process.md) and [`public/6529NM.2026.001.04.md`](../../../../records/accessions/6529NM.2026.001/public/6529NM.2026.001.04.md) | first-release publication, research cutoff 2026-08-02 | Reviewed Museum interpretation [E]. |
| Governed rights/condition | [`rights/...RIGHTS.04.json`](../../../../records/accessions/6529NM.2026.001/rights/6529NM.2026.001.RIGHTS.04.json); [`technical/...001.04.json`](../../../../records/accessions/6529NM.2026.001/technical/6529NM.2026.001.04.json) | reviewed 2026-08-02 | Rights and `pass_with_conditions` technical boundary; these records control over this dossier. |

The official generator wrapper currently combines token data, the project
program, and an external dependency reference. The feature script is not
separately preserved in this package. Exact source publication, annotation,
and redistribution require a dedicated rights determination.

## Identity has two independent coordinates

*Pre-Process* uses invocation number and token hash for different jobs.

- The **invocation** selects the finite edition coordinate—surface, origin,
  and growth—without randomness.
- The **full 256-bit token hash** initializes the positions and angles within
  that coordinate through two pseudorandom streams.
- The **runtime environment** supplies viewport width, height, device pixel
  density, achieved frame schedule, input history, and p5/browser rendering.

Conflating these layers would make #63 appear to have three randomly assigned
traits. It does not. Its three published axes follow from invocation 63; its
headings follow from the hash; its exact sizes and bounds follow from the
viewport.

## Formal edition proof: `8 x 3 x 5 = 120`

Let `n` be the zero-based invocation in `0..119`. The source increments the
mint number and converts zero residues to the final category. Equivalently:

```text
surface(n) = 1 + (n mod 8)
origin(n)  = 1 + (n mod 3)
growth(n)  = 1 + (n mod 5)
```

Suppose two invocations `n` and `m` have the same triple. Then `n-m` is
divisible by 8, 3, and 5. Those moduli are pairwise coprime, so `n-m` is
divisible by `lcm(8,3,5) = 120`. Because both invocations lie in a single
120-value interval, `n=m`. The map is injective. Its domain and codomain each
contain 120 elements, so it is also surjective: every surface-origin-growth
triple appears exactly once.

The Chinese Remainder Theorem gives a reconstructible inverse. For a triple
`(s,o,g)`:

```text
n = 105(s - 1) + 40(o - 1) + 96(g - 1)  (mod 120)
```

For #63, `(s,o,g)=(8,1,4)` gives
`105*7 + 40*0 + 96*3 = 1023`, and `1023 mod 120 = 63`. Thus the Museum work is
the unique edition coordinate Surface 8 / Origin 1 / Growth 4. This is a
`source_formal` proof, not a prevalence or rarity calculation.

The pinned complete metadata snapshot independently observes fifteen tokens
for every surface, forty for every origin, and twenty-four for every growth
state, exactly as the proof predicts.

## Full-hash pseudorandom reconstruction

### Stream construction

The operative `RND` class splits the 64 hexadecimal characters (32 bytes)
after `0x` into two 128-bit halves. Each half becomes four big-endian 32-bit
words for an `sfc32` stream. For #63:

```text
A0 = (0x0d800ffd, 0x4ec82f47, 0x7918afd1, 0x63ef9089)
B0 = (0xa92f6b6b, 0xb5e81247, 0x671bbad6, 0xa27bcbd0)
```

One `sfc32` advance is:

```text
t = (a + b + d) mod 2^32
d = d + 1 mod 2^32
a = b XOR (b >>> 9)
b = c + (c << 3) mod 2^32
c = rotateLeft32(c, 21)
c = c + t mod 2^32
u = unsigned(t) / 2^32
```

The constructor loop performs 500,000 calls to A and 500,000 calls to B—one
million calls in total. It then alternates A, B, A, B, beginning with A. The
first eight post-warm-up values reconstructed in memory are:

```text
.360362931620, .262264624471, .308908953099, .486332433531,
.958460750524, .377617158229, .136702994816, .265824409202
```

These are working `execution_instrumented` test vectors pending independent
reproduction from retained exact bytes. They matter because every reset creates
a new `RND` instance and repeats the warm-up. Given the same hash and viewport,
reset reconstructs the same element initialization. There is no unseeded
random call in the reviewed project source.

### Dormant hash path and consumed-but-unused values

The top-level source also computes a shorter `seed` with
`parseInt(tokenData.hash.slice(0,16),16)`, but that variable is not used by the
operative `RND` class. Every cell consumes two random angles. The first is
assigned to `moveangle`, which the constructor then overwrites with zero and
never uses; the second becomes the operative heading. An environment-scaled
`speed` value is also calculated per cell but is not used by the transition
rule. These are source-static observations. They must be retained in a faithful
call trace because the unused first angle still advances the alternating
streams.

## Parameter provenance

Let `E = sqrt(width^2 + height^2)` be the logical canvas diagonal and `i` the
cell index `0..99`.

| Parameter | Exact mapping | Origin | Consequence |
|---|---|---|---|
| Surface | `1 + invocation mod 8` | invocation-derived | selects one of eight render regimes; does not alter physics or RNG initialization |
| Origin | `1 + invocation mod 3` | invocation-derived | 1: all at center; 2: seeded x on horizontal center line; 3: seeded x and y within frame |
| Growth | `1 + invocation mod 5` | invocation-derived | chooses index-to-radius function |
| Largest radius | `.055E` for square viewport, otherwise `.06E` | environmental | size scale and collision threshold |
| Smallest radius | `.008E` | environmental | growth endpoints |
| Boundary frame | `E/40` | environmental | inset used when clamping target positions |
| Growth 1 | linear map of `i/100` from smallest to largest | invocation + index | increasing radii; final index approaches but does not equal largest |
| Growth 2 | linear map of `i/100` from largest to smallest | invocation + index | decreasing radii |
| Growth 3 | constant `4 * smallest` | invocation | uniformly small |
| Growth 4 | constant `.8 * largest` | invocation | uniformly large; #63 |
| Growth 5 | map `(i/100)^5` from smallest to `2 * largest` | invocation + index | nonlinear small-to-large |
| Initial position | origin mapping; random positions use the alternating full-hash streams | invocation + identity | starting density and collision geometry |
| Heading | second random angle per cell in `[0,2pi)` | identity-derived | one-unit target advance direction, then collision-driven spin |
| Active population | starts at one; increments after frames divisible by ten | runtime frame | gradually admits the 100 preconstructed cells |
| Collision spin | `.0125` radians for both cells per detected overlap | runtime evolving | changes future headings |
| Separation impulse | one logical unit along/opposite target-to-target bearing | runtime evolving | pushes target positions apart |
| Easing | actual position moves one tenth of target difference per active frame | runtime evolving | separates displayed position from collision target state |
| Pixel density | `displayDensity()` | environmental/dependency | backing-store resolution, not logical geometry |

### The eight surfaces

All surfaces execute the same element update. They differ in drawing and
framebuffer persistence.

| Surface | Per-frame clearing | Bodies/markers | Contact evidence | Temporal image memory |
|---:|---|---|---|---|
| 1 | black | gray outlines, white centers, angle markers | current white links | none |
| 2 | light | translucent filled bodies, dark centers/angles | current black links | none |
| 3 | black | numeric IDs only | links brighten on contact and fade | decaying pair-memory in `friendsAlpha`; repeated contact can continue increasing it |
| 4 | black | center points only | bright links with decay | decaying pair-memory in `friendsAlpha`; repeated contact can continue increasing it |
| 5 | mid-gray | black filled bodies and angle markers | current white links | none |
| 6 | only on reset; black thereafter | translucent outlines and centers | translucent current links | accumulated framebuffer |
| 7 | only on reset; light thereafter | translucent gray outlines and pale centers | translucent black links | accumulated framebuffer |
| 8 | only on reset; light thereafter | pale translucent outlines; no center or angle | translucent black links | accumulated framebuffer; #63 |

Surfaces 3 and 4 retain numerical contact memory and redraw it with decay.
Surfaces 6-8 do not clear the canvas inside `draw()`, so rendered marks remain
in the framebuffer. This distinction between system state and image memory is
central to the project and must survive reperformance.

## Algorithmic score

### Initialization and reset

```text
on setup:
    create viewport-sized 2D canvas
    set pixel density to display density and target frame rate to 30
    derive surface, origin, growth from invocation
    totalReset()

totalReset:
    r <- two full-hash sfc32 streams, warm and alternate
    activeCount <- 1
    E <- canvas diagonal
    compute largest/smallest radius, boundary frame, line thickness
    for i = 0..99:
        radius <- growthFunction(i)
        position <- originFunction(r, viewport)
        consume random angle r1                 // later overwritten
        heading <- random angle r2
        construct cell with target=position, actual=position
    configure drawing surface
    clear once to surface background
```

### Per-frame state transition

For every currently active cell `i`, in ascending index order:

```text
target_i <- target_i + (cos heading_i, sin heading_i)
target_i <- clamp target inside [radius_i + frame, dimension - radius_i - frame]
actual_i <- actual_i + (target_i - actual_i)/10

for each active j > i:
    deltaTarget <- target_j - target_i
    displayedDistance <- distance(actual_i, actual_j)
    if displayedDistance < radius_i + radius_j - 1:
        bearing <- atan2(deltaTarget.y, deltaTarget.x)
        target_j <- target_j + unit(bearing)
        target_i <- target_i + unit(bearing + pi)
        heading_i <- heading_i + .0125
        heading_j <- heading_j + .0125
        record pair (i,j) as a current friend of i
```

Pairs are tested once, by their lower-index cell. Mutations to a higher-index
cell's target and heading occur before that cell receives its own update later
in the same frame. The transition is therefore deliberately index-ordered,
not a simultaneous symmetric physics solve. Collision direction uses target
positions, while collision threshold uses eased display positions. Separation
impulses alter targets after that frame's easing and become visible through
later easing.

After all state updates, the source draws bodies, current/fading contact
networks, and centers/IDs according to the surface. Finally:

```text
if activeCount < 100 and global frameCount mod 10 == 0:
    activeCount <- activeCount + 1
```

The newly admitted cell first updates on the following draw call. At the
requested 30 frames/second and without interruption, the full population is
reached after roughly 990 draw calls, about 33 seconds. This is a nominal frame
calculation, not a guaranteed wall-clock observation.

### No convergence or terminal state

The reviewed source has no equilibrium detector, frame limit, or programmed
stop. It continues until the viewer pauses it or the environment stops
execution. This does not prove that a trajectory can never revisit a prior
mathematical or perceptual state; no non-repetition theorem is claimed.

## Time, persistence, and reset semantics

| State | Clock | Persistence | Reset/pause behavior |
|---|---|---|---|
| Token hash and invocation coordinate | none | stable | unchanged by all controls |
| Cell initialization | seeded reset | stable until reset, then exactly reconstructed for same viewport | mouse, Space, and surface keys rebuild it |
| Target/actual positions and headings | one update per active draw | evolves indefinitely | reset reconstructs; pause freezes draw loop |
| Active population | global draw-frame phase | grows from 1 to 100 | reset sets count to 1 but does **not** reset p5's global `frameCount` |
| Current pair contacts | current update | one frame | rebuilt every update |
| Surface 3/4 pair alpha | frame update | increments on contact, decays by 2 when drawn | reset reconstructs cells and clears canvas |
| Surface 6-8 framebuffer | draw operations | persists until reset/clear | reset clears once; pause retains pixels |
| Pixel density/backing store | setup environment | current page | not changed by project controls |

Because `frameCount` survives `totalReset()`, the delay before the first new
cell after a viewer reset depends on the reset's phase modulo ten. The seeded
cell array replays, but the population-admission schedule may start after
between one and ten subsequent draw calls. A rigorous same-state surface
comparison should therefore use isolated page loads with aligned frame counts
or an instrumented analytical clock, and must label any departure from
authentic session behavior.

The source initializes `freeze = true` while allowing the p5 draw loop to run.
On the first `P` press, it toggles `freeze` to false and calls `loop()`, which is
already active; the second press toggles it true and calls `noLoop()`. Later
presses alternate pause and resume. This source-static latch discrepancy with
the simple public instruction "P pauses or resumes" needs execution testing in
the exact dependency/browser package before publication.

## Interaction profile

| Input | State mutation | Randomness | Persistence/reversibility | Identity | Boundary |
|---|---|---|---|---|---|
| mouse press | `totalReset()` with current surface, origin, growth | recreates both streams and identical cell initialization for same viewport | resets dynamics and image memory; activation phase retains global `frameCount` | none | implemented source; no first-capture exercise |
| `Space` | same as mouse press | same | same | none | implemented source |
| `1`-`8` | set surface, then `totalReset()` | same initial RNG state | new render regime and clean run; token's recorded Surface 8 remains unchanged | none | implemented source; session view only |
| `P` or `p` | toggles `freeze`, calling `noLoop()` or `loop()` | none | current state and framebuffer persist while paused | none | latch caveat above |
| reload | recomputes invocation axes and resets page/global frame state | same hash streams | strongest replay of initial session for same environment | none | source-static |
| viewport changed then reload | changes diagonal-scaled size, frame inset, positions, and backing store | same random values mapped into new geometry | environment-dependent manifestation | none | no resize handler |

The code has no project-level touch handler, keyboard alternative for mouse
reset beyond Space, resize handler, or reduced-motion mode. Keyboard focus,
key-repeat, touch synthesis, and assistive-technology behavior remain untested.

## Exact-object close reading: `6529NM.2026.001.04`

### Fixed coordinates

The retained metadata records `Surface 8`, `Origin 1`, and `Growth 4`.
At the controlled observation's 1280 x 720 CSS-pixel canvas:

```text
E (diagonal)          = 1468.6047800548656
largest radius        = .06E = 88.11628680329193
#63 radius, Growth 4  = .8 * largest = 70.49302944263354
#63 diameter          = 140.98605888526708 logical pixels
boundary frame        = E/40 = 36.71511950137164
line thickness        = 1 logical pixel after minimum clamp
initial center        = (640, 360) for all 100 cells
```

The backing store was 1920 x 1080 because the generator requested display
density; logical behavior still used the 1280 x 720 p5 coordinate system.
These calculations are `source_formal` applications of the current source to
the recorded environment, not retained render evidence.

### From total overlap to accumulated relation

All one hundred cells are constructed at the same center with the same large
radius. Only the first is initially active. Every ten global draw frames,
another preconstructed center-born cell enters the update set. Each arrival
therefore meets an already moving field from a condition of strong overlap.
The collision loop pushes paired targets apart and increments both headings,
but actual positions lag behind targets through one-tenth easing. The visible
field is not a succession of clean elastic collisions. It is a temporally
thick negotiation among movement, boundary constraint, delayed position, and
index-ordered contact response.

Surface 8 chooses what the encounter remembers. It draws no center marker, no
direction marker, and no fill. Its body perimeters use translucent near-white
on a light background, while contact links use translucent black. Because the
background is not cleared per frame, repeated links darken and persist. The
controlled static observation—rows of circular masses, repeated axes, and
translucent sweeps and overlaps—can therefore be read as a history of contacts
rather than a direct census of current bodies.

This also corrects an easy visual misreading. The observed horizontal
registers might suggest that the elements began on the project's horizontal
origin. The exact coordinate says otherwise: `Origin 1` is the center, while
the horizontal-line origin is `Origin 2`. In #63, any register-like order is a
consequence of execution and accumulated rendering, not the recorded origin
axis. That distinction is precisely why algorithmic close reading matters.

### Relation to the edition

#63 is one of fifteen Surface 8 works, one of forty Origin 1 works, and one of
twenty-four Growth 4 works, but the combination occurs once because the whole
triple is exhaustive. Those counts identify the coordinate system. They do
not say that #63 is better, more important, more desirable, or "rarer" than
another token. Its Museum significance comes from what this exact coordinate
makes available for study: extreme initial overlap rendered as accumulating
contact evidence.

## Collection topology and non-ranking map

The authored topology is the finite product:

```text
Surface {1..8} x Origin {1..3} x Growth {1..5}
```

Invocation order is a single CRT traversal through that product. Adjacent
invocations advance all three residues together; numerical adjacency is not
visual similarity and should not be plotted as a one-dimensional rank. The
preferred Museum map is an 8 x 3 set of panels, each containing five growth
positions, or an interactive cube with equal visual weight for every cell.
It should expose the invocation inverse and locate #63 without prices,
ownership, popularity, marketplace scores, or ordinal badges.

| Axis | Artist-described categories | Formal coverage | Pinned observed coverage |
|---|---|---|---|
| Surface | eight ways the elements are rendered | each appears 15 times | 15 each |
| Origin | center, horizontal line, random positions | each appears 40 times | 40 each |
| Growth | small-to-large, large-to-small, all small, all large, nonlinear small-to-large | each appears 24 times | 24 each |
| Triple | every significant combination | exactly once by CRT | 120 distinct triples across 120 tokens |

The hash-defined headings and random origin coordinates make each token's
trajectory more specific than its triple. The product above is the authored
edition score, not a complete enumeration of all frames or encounters.

## Causal atlas manifest

All controlled variants are Museum analytical surrogates. They must not be
presented as authentic token states or new artworks. Every artifact must bind
the exact source and token inputs, surface/origin/growth coordinate, viewport,
pixel density, frame number, global-frame phase, active population, input
history, changed term, fixed terms, attribution, rights basis, and an always-
visible `ANALYSIS VIEW` label.

| Exhibit | Question | Baseline/intervention | Held constant | Expected result | Status |
|---|---|---|---|---|---|
| `PRE-ATLAS-01` | Is the 120-work score complete? | CRT traversal and inverse over every invocation | exact source mapping | proves one occurrence of every triple and locates #63 | proof complete; visualization pending |
| `PRE-ATLAS-02` | What does each surface reveal? | replay #63's same physical state through all eight render regimes at aligned frame checkpoints | hash, origin, growth, viewport, cell state | separates physical behavior from current links, fading pair memory, and framebuffer accumulation | specified; not rendered |
| `PRE-ATLAS-03` | How does the population arrive? | checkpoints at active counts 1, 2, 10, 25, 50, 100 | #63 coordinate and fresh-load frame phase | shows center-born arrivals turning overlap into structure | specified; not rendered |
| `PRE-ATLAS-04` | What does Origin 1 cause? | compare Origins 1, 2, 3 as labeled counterfactuals with same hash, surface, growth | all non-origin state | isolates center overlap from line/random initialization | specified; rights review required |
| `PRE-ATLAS-05` | What does Growth 4 cause? | compare all five growth functions with same hash, surface, origin | all non-growth state | isolates collision scale and index/radius ordering | specified; rights review required |
| `PRE-ATLAS-06` | Which term makes the field? | ablate spin, separation impulse, easing, boundary clamp, and progressive admission one at a time | #63 seed and render surface | assigns observed structures to update terms without claiming intent | specified; restricted prototype first |
| `PRE-ATLAS-07` | What is state and what is image memory? | show cell state, current contact graph, Surface 8 fresh frame, and accumulated framebuffer together | exact checkpoint | demonstrates that dark history can outlive a current contact | specified; not rendered |
| `PRE-ATLAS-08` | How does viewport materialize the score? | replay at square, 16:9, and tall viewports with aligned frame counts | token, source, inputs | shows diagonal-scaled radii/bounds and origin mapping | specified; not rendered |
| `PRE-ATLAS-09` | What does reset actually reset? | compare mouse/Space/surface reset and full reload at several global-frame phases | token and viewport | reveals identical RNG replay but different admission phase; tests pause latch | specified; execution test required |

The most important public exhibit is `PRE-ATLAS-02`: one synchronized physical
state rendered eight ways. It turns the project's abstract word "surface" into
a visible argument about representation.

## Display and conservation profile

### Significant properties

- **Identity:** exact contract/token, invocation 63, full token hash, project
  and generator relation.
- **Edition score:** CRT mapping of invocation to the exhaustive 8 x 3 x 5
  product.
- **Randomness:** two 128-bit `sfc32` states, 500,000-call warm-up per stream,
  A/B alternation beginning with A, and reset replay.
- **Behavior:** one hundred cells; one-unit target advance; inset clamping;
  one-tenth easing; ascending-index pair tests; target-space separation;
  `.0125` heading increments; progressive admission.
- **Representation:** eight surface regimes, including the distinction between
  per-frame clearing, decaying numerical memory, and persistent framebuffer.
- **Participation:** surface selection as reset/reperformance, mouse/Space
  reset, pause/resume behavior including the current latch semantics.
- **Encounter:** logical viewport, diagonal size model, display density, target
  versus achieved 30 fps, browser canvas compositing, screen contrast,
  duration, and input focus.

### Display recommendation

The artist describes software performance over extended timescales and viewer
participation in the project's changing presentation. The Museum should show
#63 live in its token-recorded Surface 8 by default, at its 1.78 horizontal
ratio, with a visible elapsed-frame/active-population disclosure available in
the research layer. A static still may document a state but must not stand in
for the executable work.

A supervised research mode may let visitors select Surfaces 1-8 and reset the
run, while clearly stating that those session views do not change #63's
recorded Surface 8 coordinate. Surface comparisons should not be described as
simultaneous authentic states unless independent instances are loaded and
their frame schedules are documented. Long viewing duration is material: an
installation that loops a short recording would replace progressive
admission, collision history, and framebuffer accumulation with a different
temporal object.

### Required preservation and reperformance tests

| Test | Reference expectation | Failure significance |
|---|---|---|
| Source/dependency package | reconstruct the reviewed response or a documented rights-cleared equivalent, exact project/feature scripts, and p5.js 1.0.0 offline | high: current autonomous preservation gap |
| PRNG conformance | reproduce stream seeds, 500,000 advances per stream, A/B alternation, and early vector in two implementations | high: changes all identity-derived headings/positions |
| CRT conformance | prove all 120 triples and inverse; verify #63 | high: changes edition ontology |
| Physics trace | retain state digests for selected cells/pairs before and after update, clamp, ease, collision, and draw at defined frames | high: detects ordering or numeric-semantics drift |
| Surface trace | replay one locked state through eight surfaces and retain state/image hashes separately | high: representation is a core work property |
| Reset/global-frame test | exercise mouse, Space, 1-8, reload at all modulo-ten phases | high for authentic population timing |
| Pause test | verify the initial `freeze` latch and later pause/resume across focus loss and sleep/wake | medium/high: interaction documentation may diverge from execution |
| Viewport/DPR matrix | 1:1, 16:9, 1.78, and tall logical canvases at representative DPRs | high: radius, boundary, positions, line weight, and raster memory vary |
| Browser/compositing matrix | Chromium, Firefox, Safari/WebKit and software rendering where possible | high if alpha accumulation or geometry changes; minor antialiasing variance needs tolerance review |
| Long-duration run | full admission plus hours/days with periodic state and framebuffer checkpoints | high: artist-stated extended performance remains untested in Museum custody |
| Network loss | execute from self-contained authorized package with no Art Blocks/CDN service | high: required for independent stewardship |

Migration must preserve JavaScript 32-bit `sfc32` arithmetic, warm-up and
alternation, ascending update order, the target/actual position split,
frame-count admission, and surface-specific image memory. Replacing the
framebuffer with a vector reconstruction or changing collision updates to a
simultaneous solver would materially alter the system even if a late still
looked similar.

Any shared migrated or annotated version must identify modifications under
the governed rights conditions. Pixel identity is not assumed across canvas
implementations; a perceptual tolerance can be adopted only after a reference
package and independent comparison exist.

## Claim register

| ID | Material claim | Class | Qualifier | Source/date | Status |
|---|---|---|---|---|---|
| `PRE-CL-01` | The Museum work is exact token 383000063, invocation 63, Surface 8 / Origin 1 / Growth 4. | A/B/C | `source_static` | governed object record and retained metadata | verified |
| `PRE-CL-02` | REAS describes 100 circular Elements, four behaviors, eight surfaces, three origins, five growth configurations, and every significant permutation. | B | `artist_statement` | Art Blocks interview, 2022-11-28 | supported |
| `PRE-CL-03` | The invocation mapping is a bijection over the 8 x 3 x 5 product. | C | `source_formal` | proof in this dossier against reviewed-hash source | verified mathematically; source retention pending |
| `PRE-CL-04` | The pinned snapshot observes 15 of each surface, 40 of each origin, and 24 of each growth state. | C | `population_empirical` | complete descriptor/result hashes above | verified as descriptive snapshot result |
| `PRE-CL-05` | The renderer uses two full-hash `sfc32` streams, warms each 500,000 calls, and alternates A then B. | C | `source_static` | official reviewed-hash response re-read 2026-08-04 | provisional pending retained source |
| `PRE-CL-06` | #63 initializes all 100 equal large cells at center for a fixed viewport. | C | `source_formal` | source mapping plus exact coordinate | supported; independent trace pending |
| `PRE-CL-07` | Surface 8 accumulates pale perimeters and black contact links without per-frame background clearing. | C | `source_static` | same | provisional pending independent execution |
| `PRE-CL-08` | The observed two viewport hashes differ after a minimum 1,500 ms wait. | C | `execution_observed` | visual-observation record, 2026-08-01 | verified within stated limits |
| `PRE-CL-09` | #63's dark registers are accumulated evidence of center-born collision relations rather than the horizontal origin input. | E | `museum_interpretation` | exact coordinate, source analysis, controlled still | supported, revisable |
| `PRE-CL-10` | Reset reconstructs seeded cell state but preserves global `frameCount`; the first P press may not pause the already running loop. | C | `source_static` | official reviewed-hash response re-read 2026-08-04 | provisional; exact-runtime exercise required |
| `PRE-CL-11` | The post-warm-up vector in this dossier reproduces the current source. | C | `execution_instrumented` | in-memory reconstruction, 2026-08-04 | provisional; durable independent harness required |

## Unresolved questions and competing explanations

| Question | Evidence needed | Consequence if wrong |
|---|---|---|
| Can the exact generator, feature script, and dependency bytes be retained and publicly redistributed? | source acquisition and rights review | determines reproducibility and annotated-source scope |
| Does an artist/platform reference capture use a fixed frame, active-population count, or elapsed duration? | rendering documentation and ideally studio confirmation | defines reference checkpoints and avoids treating any late still as canonical |
| Does the exact p5.js 1.0.0/browser combination exhibit the source-predicted first-press pause latch? | controlled keyboard execution with focus/input logging | may require correction or qualification of public controls |
| How should reset's global-frame phase be conserved? | exact-runtime traces at modulo-ten phases and studio consultation | determines whether phase is significant behavior or incidental implementation |
| Are numerical trajectories stable across JavaScript engines and long runs? | state-level, not only pixel-level, cross-engine replay | sets emulation and migration tolerances |
| Which surface histories are designated artwork manifestations versus analytical views for a token whose recorded surface differs? | artist/platform source and curatorial policy | governs public surface selector language |
| How long must a representative behavior film run? | full-admission capture plus long-duration observation | prevents a short clip from erasing the work's temporal scale |
| What touch, screen-reader, and reduced-motion interface preserves meaningful participation? | accessibility research and user testing | determines public parity without silently altering authentic state |

Publication gates remain open: exact source/dependency retention, independent
RNG and state-trace reproduction, technical review, curatorial review,
rights/accessibility review, cross-environment and long-duration execution,
artifact hashes, and release fixity. The dossier and formal proof are complete
as research; the proposed atlas has not been rendered.

## Publication package specification

- **Public thesis:** a finite exhaustive score becomes an open performance, and
  each surface defines what behavior can be seen or remembered.
- **Algorithm card:** invocation -> CRT coordinate; full hash -> dual sfc32
  state; viewport -> geometry; frames/collisions -> behavior; surface ->
  evidence.
- **Executable score:** the CRT inverse, dual-stream test vectors, ordered
  collision transition, and surface table above in an independent harness.
- **Causal atlas:** `PRE-ATLAS-01`-`09`, led by same-state/eight-surface replay.
- **Collection map:** equal-weight 8 x 3 x 5 topology with invocation inverse
  and #63 location, no ranking.
- **Behavior film:** fresh load through all 100 active cells, with frame,
  active count, global-frame phase, viewport, and source identity visible;
  include state/network/framebuffer split-screen in the research version.
- **Conservation note:** exact seed and topology tests, surface memory,
  reset/pause caveats, environment matrix, and current source-retention gap.
- **Accessibility:** equivalent reset/pause/surface controls, text explanation
  of current versus accumulated contacts, reduced-motion checkpoints, and
  narrated/transcribed behavior documentation.

[^artist]: Casey REAS, "In Conversation with Casey REAS on Pre-Process,"
    interview by Jordan Kantor, Art Blocks, 28 November 2022,
    https://www.artblocks.io/articles/in-conversation-with-casey-reas-on-pre-process.
    The interview is the primary source for the artist's chronology, Element
    specification, 8 x 3 x 5 account, and performance language. The formal
    traversal proof and source mechanics are Museum research, not quotations
    or claims of artist intent.

## Research status and boundaries

- **Working dossier ID:** `GSD-6529NM.2026.001-PREPROCESS`
- **Record family:** `GENERATIVE_SYSTEM_DOSSIER` (working; not governed)
- **Status:** constructed research dossier for independent technical, curatorial,
  rights, and accessibility review
- **Constructed:** 2026-08-04
- **Artist:** Casey REAS
- **Project:** *Pre-Process*, Art Blocks Curated project 383, 2022
- **Museum scope:** `6529NM.2026.001.04`
- **Working standard:** [`docs/generative-system-analysis.md`](../../../../docs/generative-system-analysis.md)

This dossier does not amend the governed accession, object, rights, condition,
or preservation records; constitute artist approval; authenticate an
unretained byte stream; or claim that source, dependency, and runtime
preservation is complete. It does not rank any token or treat an edition
coordinate as evidence of rarity, quality, value, or significance.

The reviewed generator transcript binds the official response to a SHA-256
observation and records p5.js 1.0.0 and the implemented controls. It also says
the response bytes were not retained. Read-only retrieval on 2026-08-04
reproduced the reviewed response hash. Source-static findings and in-memory
test vectors are therefore working research against the currently served
official generator, pending an independently reviewed, Museum-held source and
trace package.

Retained platform metadata reports CC BY-NC 4.0 for the work. The governed
rights record controls use of the artwork and required attribution, notice,
change marking, noncommercial scope, and downstream conditions. No inference
is made that the platform wrapper, p5.js dependency, or separately extractable
project source shares that license.
