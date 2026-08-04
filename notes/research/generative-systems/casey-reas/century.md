# CENTURY: adjacency as a mutable state

## Curatorial thesis

**One-sentence thesis.** *CENTURY* makes adjacency a mutable property of an
identity-bearing image: its moving composition persists while the program
changes which vertical fragments are neighbors.

Casey REAS identifies composing, slicing, and recomposing as the project's
core, developed in direct relation to Ellsworth Kelly's cut-and-reassembled
images; he also emphasizes motion and the variations available within each
mint.[^artist] The constitutive source makes that statement more exact without
exhausting it. The program first creates a moving composition in an off-screen
buffer. It then samples the buffer as vertical strips, places those strips in
an ordered or permuted sequence, and masks the square result into a circle.
The cut is therefore neither a static motif nor a post-production filter. It
is a state transition between an always-moving source image and its current
topology.

The three Museum works make a particularly strong comparison, although they
are a Museum-formed group rather than an artist-designated triptych. #31
concentrates sixteen cuts inside a blue-charcoal circular field; #724 spreads
seven broad slices across a cream field and activates the displaced `Janky`
path; #401 makes ten cuts and translucency operate in grayscale. Together they
show that the same operation can produce pressure, interval, or shallow planar
depth. That is a curatorial interpretation [E], not a value ranking.

## Exact Museum scope

| Museum object | Exact work | Chain/object citation | Token hash | Governed record |
|---|---|---|---|---|
| `6529NM.2026.001.01` | *CENTURY #31* | `eip155:1/erc721:0xa7d8d9ef8d8ce8992df33d8b8cf4aebabd5bd270/100000031` | `0x55f52fb6b8134eb95200dfe109941c2df4ef53618d08598ccf7bd20a955bbfa9` | [`objects/6529NM.2026.001.01.json`](../../../../records/accessions/6529NM.2026.001/objects/6529NM.2026.001.01.json) |
| `6529NM.2026.001.02` | *CENTURY #724* | `eip155:1/erc721:0xa7d8d9ef8d8ce8992df33d8b8cf4aebabd5bd270/100000724` | `0x02a66fde5911ca99640218fb0b8143bf6d4b9da045626de7065f0a2c88453766` | [`objects/6529NM.2026.001.02.json`](../../../../records/accessions/6529NM.2026.001/objects/6529NM.2026.001.02.json) |
| `6529NM.2026.001.03` | *CENTURY #401* | `eip155:1/erc721:0xa7d8d9ef8d8ce8992df33d8b8cf4aebabd5bd270/100000401` | `0x8e536efbdddc966eb7cea6d719463fd1310cc9054e6e6850557a5fd69b49dd16` | [`objects/6529NM.2026.001.03.json`](../../../../records/accessions/6529NM.2026.001/objects/6529NM.2026.001.03.json) |

All three are accessioned in lot `6529NM.2026.001`. Token title, copyright,
license, technical condition, and custody remain separate facts.

## Evidence and source lock

Evidence classes use the repository's A-E system. Method qualifiers are the
non-normative working qualifiers in the analysis standard.

| Source/component | Exact reference | Fixity or version | Retention and evidentiary boundary |
|---|---|---|---|
| Official generator, #31 | [Art Blocks generator](https://generator.artblocks.io/1/0xa7d8d9ef8d8ce8992df33d8b8cf4aebabd5bd270/100000031) | response SHA-256 `465b45798f14bea109f59986bd2cdcfd6e2eb9050327f52b24af15e159704ae2`; working decoded inline-script SHA-256 `675f4e3c2c898cd73f60574e6099e7e22f25e91811685d4f1f372ff7aa473030` | Response hash independently reviewed [C]; bytes not retained. Inline-script hash is a 2026-08-04 in-memory working observation, includes token data, and is not a preservation commitment. |
| Official generator, #724 | [Art Blocks generator](https://generator.artblocks.io/1/0xa7d8d9ef8d8ce8992df33d8b8cf4aebabd5bd270/100000724) | response SHA-256 `1dfd3f2205e8c4a33f85d2c0efce35b019d2ea21e424e5d750bc86c3890c3b3e`; working decoded inline-script SHA-256 `acc09cb3421a51ad3ade9e6f2f7f4b0b2823a5875ee8b4abc49675e5f097c740` | Same boundary. |
| Official generator, #401 | [Art Blocks generator](https://generator.artblocks.io/1/0xa7d8d9ef8d8ce8992df33d8b8cf4aebabd5bd270/100000401) | response SHA-256 `51ab1073b166701c9379984d9331c14d803dc84e35c8d06b5a8071f4eb895aad`; working decoded inline-script SHA-256 `9d54b3125899e39f39b19f65caa410ab05c9b0b0c6f81e617eb828142a8d7647` | Same boundary. |
| Runtime dependency | `https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.0.0/p5.min.js` | p5.js `1.0.0` as declared in all three reviewed generator responses | Remote dependency; exact dependency bytes are not bound by the current public preservation package. |
| Generator transcript | [`evidence/casey-reas/generator-observations.json`](../../../../evidence/casey-reas/generator-observations.json) | reviewed commit `514cb18aee37b0d04c3eeb59703b411ea34f6bf9`; transcript SHA-256 `a2e6a2295ffdbee3332fdeec7cd9e044d4bc5313cd63f9d6e5b67e01c3ac79da` | Retained, independently reviewed observation transcript [C]; explicitly not raw source retention. |
| Exact metadata | [`raw/metadata/6529NM.2026.001.01.json`](../../../../evidence/casey-reas/raw/metadata/6529NM.2026.001.01.json), [`.02.json`](../../../../evidence/casey-reas/raw/metadata/6529NM.2026.001.02.json), [`.03.json`](../../../../evidence/casey-reas/raw/metadata/6529NM.2026.001.03.json) | SHA-256 `e193e143...`, `3516518a...`, `7feffd29...` in the object and visual-observation records | Retained exact platform responses [B/C]. |
| Complete edition snapshot | [`descriptors/century.json`](../../../../evidence/casey-reas-collection-snapshots/descriptors/century.json) | 1,000/1,000 tokens; descriptor SHA-256 `cb64ad56ba979efabbee441708a4c130977aed409fe697607acfb2c8a5841bc9`; result SHA-256 `22964c531e1a41a2945931b81f72d8ab5fad41807f3a408539161d6fca0c1275` | Retained, pinned population evidence. Counts are descriptive and non-ranking. |
| Controlled visual observation | [`visual-observation-record.json`](../../../../records/accessions/6529NM.2026.001/visual-observation-record.json) | `6529NM.2026.001.VO-01`, observations completed 2026-08-01 | Two non-retained screenshot hashes per work show frame change after a minimum 1,500 ms wait [C]; no control was exercised. |
| Artist/project account | [Art Blocks interview, 21 June 2021](https://www.artblocks.io/articles/in-conversation-with-casey-reas-on-century); [project page](https://www.artblocks.io/collection/century-by-casey-reas) | Official/primary web sources | Artist statement [B], not source-code proof. |
| Museum interpretation | [`public/projects/century.md`](../../../../records/accessions/6529NM.2026.001/public/projects/century.md) and the three public object entries | first-release publication, research cutoff 2026-08-02 | Reviewed Museum interpretation [E]. |

The current generator wrapper embeds `tokenData`, the project program, and an
external p5.js reference in one HTML response. The project/feature scripts are
not separately retained in the governed evidence package. In particular, the
published metadata's feature vocabulary is evidence about platform labels; it
must not be presumed to be a literal inventory of runtime state where it
diverges from the constitutive renderer.

## Identity and randomness profile

### Hash projection

The full token hash establishes the platform identity input. The renderer does
not use all 256 bits. It evaluates:

```text
seedNumber = parseInt(tokenHash.slice(0, 16), 16)
```

Because the string includes `0x`, `slice(0, 16)` contains fourteen hexadecimal
digits. JavaScript parses that 56-bit prefix into a binary64 `Number`; the
first bitwise operation then coerces it to a signed 32-bit integer. The
operative random state is therefore a lossy projection of the full hash. This
is a source-static statement, not a claim that token identity itself is only
32 bits or that outputs are unique.

The generator then advances a signed xorshift32 state:

```text
s = s XOR (s << 13)
s = s XOR (s >> 17)       // arithmetic right shift
s = s XOR (s << 5)
u = (two_complement_abs(s) mod 1000) / 1000
```

Consequently `u` lies on a thousandth-resolution lattice from `0.000` through
`0.999`. Thresholds in the source should be reported literally, not rounded
as if `u` were an ideal continuous uniform variable.

### Reconstructible test vectors

| Work | Effective signed int32 state before first advance | First ten `u` values |
|---|---:|---|
| #31 | `-1229450416` | `.217, .462, .712, .448, .674, .315, .092, .945, .826, .935` |
| #724 | `-564588086` | `.674, .580, .606, .032, .121, .997, .475, .370, .098, .184` |
| #401 | `-69346152` | `.975, .062, .346, .545, .144, .859, .483, .907, .712, .893` |

These vectors were reconstructed in memory from the currently served source
on 2026-08-04. They are `execution_instrumented` working checkpoints pending a
retained independent test harness. They explain the opening branch decisions:
#31 selects Palette A, four line-color options, oculi, opaque ellipses, fewer
lines, no `Janky`, and a blue background; #724 selects Palette B, four
line-color options, oculi, fewer lines, `Janky`, and a cream background; #401
selects Palette C, two line-color options, oculi, alpha `209.184` before the
published integer label, fewer lines, no `Janky`, and the palette's fixed
black background.

### Random-call provenance

The initialization stream is branch-dependent:

```text
token hash
  -> 56-bit textual prefix -> binary64 parse -> signed int32 xorshift state
  -> palette
  -> number of enabled line colors
  -> oculi on/off
  -> alpha eligibility [and, conditionally, alpha value]
  -> expanded-line flag
  -> Janky flag
  -> background [except Palette C, which fixes black]
  -> two ellipse parameter blocks [when oculi are enabled]
  -> line-band count
  -> ten random draws per line band
  -> repeated slice width and offset pairs
  -> ordered/scrambled branch
  -> one removal index per slice when scrambled
```

Every call matters because later calls shift when an earlier conditional
branch consumes or skips a value. Calls that produce ignored strip offsets for
non-`Janky` works still advance the stream. Key `1` continues from the current
stream state; it does not reconstruct the original seed. Reloading the page
does.

## Parameter provenance

Let `d = min(window.innerWidth, window.innerHeight)` and let `u` denote the
next xorshift lattice value.

| Parameter | Exact source mapping | Type and downstream effect | Published relation |
|---|---|---|---|
| Palette | D if `u > .99`; C if `.95 < u <= .99`; B if `.63 < u <= .95`; otherwise A | Identity-derived; selects composition and line color arrays | `Palette A-D` |
| Available line colors | `floor(2 + (L - 1)u)`, where `L` is palette line-array length | Identity-derived; only the leading portion of the array may be sampled by bands | `Line Color Options` |
| Oculi | enabled iff `u > .1` | Identity-derived; creates two rotated ellipses behind the line bands | `Oculi` |
| Ellipse alpha | if `u > .5` and palette is A or C, consume another value and set `204 + 36u`; otherwise `255` | Identity-derived; changes overlap and planar depth | `Alpha`, `Alpha Value` |
| Expanded line field | enabled iff `u > .95`; if enabled, add 32 bands | Identity-derived | `Line Quantity More/Less` |
| `Janky` | enabled iff `u > .7` | Identity-derived; offsets interior destination strips only while order is scrambled | `Janky` |
| Background | Palette C fixes black; other palettes choose `floor(u * colors.length)` | Identity-derived | not independently interpreted |
| Oculus 1 | diameter `[.5d, 1.75d)`, y in an upper/lower `.4d` band, angle `+.57595867`, x `[0,d)`; color excludes background | Identity-derived | major axis rounded in metadata |
| Oculus 2 | diameter `[.33d, 1.0d)`, same y logic, angle `-.57595867`, x `[0,d)`; any palette color | Identity-derived | major axis rounded in metadata |
| Band count | `8 + floor((1-u)^3 * 12)`, plus 32 when expanded | Identity-derived; 8-20 or 40-52 filled quadrilateral bands, cubic-biased toward lower counts | `Line Count` |
| Band motion | amplitude `[d/100,d/25)`; phase `[0,2pi)`; speed call is fixed at `.01` radians/frame | Identity-derived initialization plus runtime frame | visible subtle motion |
| Slice width | ordinarily `.02d + u^3(.25d)`; terminal slice consumes the remainder when another minimum slice would not fit | Identity/session-derived; cubic-biased toward narrow strips | `Slice Count` is a platform label, not accepted uncritically as runtime count |
| Slice order | scrambled when `u > .02`, ordered otherwise | Identity-derived at load; viewer-controlled later | `Chaos/Cosmos` |
| Strip offset | integer conversion of `[-d/100,d/100)` for each source strip | Identity/session-derived; visible only for interior destination positions when both `Janky` and scrambled | part of `Janky` behavior |

The palette bands above are exact program conditions. If the thousand lattice
values were equally represented, their band sizes would be 631 (A), 320 (B),
40 (C), and 9 (D). That is a description of the threshold lattice, not a
prediction that 1,000 token seeds distribute perfectly across it.

## Algorithmic score

### Initialization

```text
d <- min(viewport width, viewport height)
create square WEBGL canvas d x d
create 2D off-screen buffer gg of the same logical size
r <- xorshift32(projected token-hash prefix)

choose palette, enabled line colors, oculi, alpha, expanded lines,
Janky state, and background from r
if oculi: construct two static rotated ellipses
construct N line bands with endpoint, thickness, color, phase, amplitude
define vertical source slices with cubic-biased widths and per-slice offsets
choose initial ordered or without-replacement permuted slice sequence
```

### Per-frame transition

For band `i`, with phase `theta_i`, amplitude `a_i`, left baseline `y1_i`, and
right baseline `y2_i`:

```text
m_i(t) = cos(theta_i(t)) * a_i
theta_i(t + 1) = theta_i(t) + 0.01
left endpoints  <- y1_i + m_i(t)
right endpoints <- y2_i - m_i(t)/2
```

The nominal oscillator period is `2pi/.01`, about 628.3 draw calls. The source
does not use elapsed wall time or set a frame rate; seconds per cycle therefore
depend on the achieved display rate.

```text
clear gg
draw static oculi into gg
advance and draw all moving filled bands into gg

x <- 0
for each destination position i:
    source strip j <- currentOrder[i]
    destination x' <- x
    if i is interior and Janky and scrambled:
        x' <- x + sourceStrip[j].offset
    texture-map gg[j.x : j.x + j.width] at destination x'
    x <- x + j.width

draw four white corner shapes as a circular aperture mask
```

The off-screen buffer is cleared each frame. *CENTURY* therefore has motion
but no framebuffer trail accumulation in this renderer. The texture stage
changes adjacency without changing the underlying moving band and ellipse
objects.

### State machine and interaction

```text
LOAD
  -> initialize base composition, current cuts, and initial order
  -> PERFORM: update base composition and render through current cuts

PERFORM -- key 1 --> consume continuing PRNG
                    define new cut widths and offsets
                    permute them
                    return to PERFORM

PERFORM -- key 2 --> order the current cuts by their source positions
                    return to PERFORM

RELOAD -> reconstruct token-derived initialization from the original seed
```

Key `2` does not reset the random stream, phases, or cuts, and it does not
recover a prior session's initial permutation. It orders the *current*
partition. This source-static distinction refines, rather than contradicts,
the platform's public phrase "put the slices in the original order."

## Time and state profile

| State component | Initial source | Transition | Persistence and reset |
|---|---|---|---|
| Token identity/full hash | platform `tokenData` | none | stable across manifestations |
| Project PRNG state | lossy hash-prefix projection | advances during initialization and each key-`1` recut | not reset by keys; reset by reload |
| Ellipse geometry/color | initialization PRNG | static | survives both keys; reset on reload |
| Band geometry/color | initialization PRNG | static except vertical oscillation | phases continue through both keys |
| Band phase | initialization PRNG | `+.01` per draw call | never reset by documented keys |
| Slice boundary set | initialization PRNG | rebuilt by key `1` | key `2` preserves current boundaries |
| Slice order | initialization or session PRNG | key `1` permutes; key `2` orders | current-session state |
| `Janky` capability | initialization PRNG | none | fixed for token initialization |
| Visible raster | current base frame, current cuts, WebGL texture sampling | replaced each draw | no source-program framebuffer memory |
| Viewport `d` and pixel density | browser environment | fixed at setup; no resize handler | reload at a new viewport reconstructs geometry at a new scale |

The generator's performance is deterministic in frame space given the exact
source, dependency, token data, viewport, JavaScript semantics, and input
sequence. Pixel identity across browsers/GPUs is not established. Wall-clock
identity is not expected because motion advances per draw call.

## Interaction profile

| Input | Mutation | PRNG effect | Reversible? | Identity effect | Evidence boundary |
|---|---|---|---|---|---|
| `1` | replaces current slice boundary set and creates a new permutation | consumes two calls per new strip, a branch call, and one selection call per strip | key `2` orders the new cuts but does not recover the old partition; reload recovers initialization | none | artist/platform statement [B] plus source-static reconstruction [C] |
| `2` | sets current slice order to ascending source indices | none | a later `1` makes another partition/permutation | none | same |
| reload | reconstructs all token-derived parameters from the original page input | resets to projected seed | yes, subject to same environment | none | source-static |
| viewport change followed by reload | changes `d` and all dimension-scaled geometry | same random sequence mapped to new dimensions | environment-dependent | none | source-static; cross-environment execution not yet tested |

No touch equivalent, focus behavior, resize handler, or reduced-motion mode is
implemented in the reviewed project source. Their absence is a source-level
interface observation, not evidence about artist intent.

## Collection topology: stochastic field, observed edition

The project is a fixed edition of 1,000. It samples a branch-dependent,
hash-projected probability field; it does not enumerate a Cartesian product.
The complete pinned metadata snapshot observes all 1,000 declared tokens and
all twelve published trait categories.

| Published field | Source condition | Observed count in pinned 1,000-token snapshot |
|---|---|---:|
| Palette A / B / C / D | threshold bands above | 646 / 307 / 39 / 8 |
| Oculi true / false | `u > .1` | 903 / 97 |
| Janky true / false | `u > .7` | 311 / 689 |
| Alpha true / false | conditional on palette A/C and `u > .5` | 339 / 661 |
| More / Less lines | `u > .95` adds 32 | 43 / 957 |
| Chaos / Cosmos | `u > .02` selects scrambled order | 975 / 25 |

These are `population_empirical` counts, not aesthetic evidence. One notable
research question is the label/runtime boundary: the snapshot associates all
25 `Cosmos` records with published `Slice Count 0`, while the constitutive
renderer always constructs a non-empty strip array before choosing ordered or
scrambled display. Until the feature script is independently preserved and
reviewed, `Slice Count 0` should be treated as a platform feature label rather
than proof that no runtime slices exist.

The Museum trio occupies a sharply useful but incomplete cross-section. It
contains Palettes A, B, and C; three slice counts; one alpha state; one `Janky`
state; and three chaotic initial orders. It contains no Palette D, no
oculi-absent work, no expanded-line work, and no initially ordered `Cosmos`
work. A collection map should display this coverage and its absences without
turning them into scarcity or rank.

## Exact-object comparison and close reading

### Token-derived coordinates

| Work | Palette | Bands | Oculi | Alpha | Janky | Slices | Initial zero-based source-strip order |
|---|---|---:|---|---|---|---:|---|
| #31 | A | 17 | true; axes `1.68`, `.59` | false | false | 16 | `0,13,8,4,5,3,1,11,6,9,14,15,7,10,2,12` |
| #724 | B | 11 | true; axes `.96`, `.42` | false | true | 7 | `2,0,5,4,3,1,6` |
| #401 | C | 15 | true; axes `1.63`, `.55` | true; published `209` | false | 10 | `6,1,9,2,5,3,0,8,4,7` |

Feature values come from retained exact metadata [B/C]. The order vectors are
2026-08-04 in-memory `execution_instrumented` traces at logical `d = 720`; the
ordering itself is dimension-independent for this source path, but the vectors
remain provisional until a retained independent harness reproduces them.

### `6529NM.2026.001.01` / *CENTURY #31*

The controlled still observation records a dark blue-charcoal circular field
with cream semicircles, diagonal fragments, and conspicuous vertical
divisions. The source trace explains why the circle can feel both forceful and
jointed. A blue Palette A background and two large oculi establish a centered
mass; seventeen oscillating bands cross it; sixteen relatively numerous cuts
redistribute the field without `Janky` displacement. The seams therefore
register predominantly as changes of adjacency inside a continuous circular
aperture, not as lateral gaps. The Museum interpretation is that #31 makes
coherence appear pressurized: the eye reconstructs a circle while the strip
order denies that the circle was ever a single indivisible surface.

### `6529NM.2026.001.02` / *CENTURY #724*

The controlled still records an open rust-and-cream field with broad dark
partitions. Its seven slices are the fewest of the Museum trio and include
several very broad source bands. Palette B supplies the cream background and
rust/dark ellipse field; eleven moving bands leave more open interval than in
#31. `Janky` then moves the interior destination strips by their source-strip
offsets whenever the order is scrambled. At the observed 720-pixel logical
dimension, the source generated offsets between -6 and +4 pixels for the seven
source strips, although the first and last destination positions suppress
their offsets. The Museum interpretation is that #724 makes the cut spatial:
open ground lets small gaps, overlaps, and displaced edges become events in
their own right.

### `6529NM.2026.001.03` / *CENTURY #401*

The controlled still records a grayscale field with black bands, gray planes,
and intersecting white lines. Palette C fixes a black outer background and
restricts the active line palette to its first two colors for this token. The
oculi share gray color, while alpha `209.184` in the renderer (published as
`209`) lets their overlap remain partially legible. Ten reordered strips cut
through fifteen bands. The Museum interpretation is that #401 converts
adjacency into uncertain depth: opaque black/white bands and translucent gray
ellipses can be read as supports, obstructions, or planes, yet that shallow
architecture is only the perceptual consequence of a reordered flat buffer.

### What the trio proves and what it does not

The comparison demonstrates that one source pipeline supports three distinct
relations among density, interval, opacity, and partition. It does not prove
that palette or slice count alone caused the total aesthetic difference. Each
token changes many dependent variables and its random-call path. Causal
attribution requires the controlled counterfactual exhibits below.

## Causal atlas manifest

All proposed images and traces are Museum analytical surrogates, not authentic
token states or new artworks. Each eventual artifact must state source hash,
token input, changed variable, fixed variables, logical viewport, pixel
density, browser/GPU, frame number, input history, attribution, license basis,
and a persistent `ANALYSIS VIEW` label.

| Exhibit | Question | Baseline and intervention | Held constant | Expected result | Status |
|---|---|---|---|---|---|
| `CEN-ATLAS-01` | Where does each visible pixel originate? | For each Museum token, expose base buffer, slice boundaries, zero-based order, destination positions, and circular mask | exact token, frame, environment | makes source-to-destination provenance inspectable | specified; not rendered |
| `CEN-ATLAS-02` | What changes when order changes but cuts do not? | show current scrambled order beside key-`2` order at the same frozen base frame | token, cut widths, band phases, viewport | isolates adjacency from composition and motion | specified; not rendered |
| `CEN-ATLAS-03` | What does key `1` preserve? | checkpoint immediately before/after one recut, then after key `2` | base band/ellipse state and frame | reveals new partition/permutation while base composition continues | specified; not rendered |
| `CEN-ATLAS-04` | How does session history matter? | run two and ten key-`1` recuts, then reload | token and environment | demonstrates continuing PRNG state versus seed reset | specified; not rendered |
| `CEN-ATLAS-05` | What does `Janky` do in #724? | render current #724 state with offsets active and analytically zeroed | all other state and texture sampling | isolates gaps/overlaps from permutation | specified; rights review required |
| `CEN-ATLAS-06` | What does alpha do in #401? | render alpha `209.184` beside analytical alpha `255` | all geometry, order, color, frame | isolates translucency's contribution to planar ambiguity | specified; rights review required |
| `CEN-ATLAS-07` | What differs across the Museum trio? | synchronize at phase checkpoints `0`, `pi/2`, `pi`, `3pi/2` in the 628.3-frame oscillator | each token's authentic initialization and a common logical viewport | compares motion amplitude and partition without false wall-clock synchrony | specified; not rendered |
| `CEN-ATLAS-08` | Do source thresholds predict the released population? | threshold-lattice diagram beside pinned empirical counts | published snapshot and exact threshold definitions | separates authored mapping from observed population | data specified; visualization pending |

The preferred public sequence is artwork first, thesis second, then a
synchronized three-token provenance view. An atlas must always offer a
one-action return to the official live work.

## Display and conservation profile

### Significant properties

- **Identity:** full contract/token citation, full token hash, project identity,
  and exact generator assembly relation.
- **Genotype:** hash-prefix parsing, binary64-to-int32 coercion, xorshift32
  transitions, branch-dependent call order, palette arrays, thresholds, and
  token-derived initialization.
- **Performance:** static oculi behind continuously oscillating filled bands;
  `.01` radians per draw call; an off-screen buffer cleared every frame.
- **Participation:** key `1` creates and permutes a new partition using the
  continuing stream; key `2` orders the current partition; neither changes
  token identity.
- **Rendering:** p5.js 1.0.0, square logical canvas `d`, WEBGL texture mapping,
  color/alpha semantics, strip sampling, `Janky` destination offsets, and the
  final circular aperture.
- **Encounter:** achieved frame rate, CSS viewport, device pixel ratio,
  browser/GPU texture sampling, screen black/white levels, viewing duration,
  input focus, and the relation among three displays.

### Display recommendation

Artist/platform sources say the works are landscapes that look best large,
live, and in motion. A Museum three-screen installation should use equal
logical dimensions and aligned sightlines, document brightness and color
calibration, and allow each token to run independently. A forced synchronized
loop would be an analytical mode, not a neutral presentation. Separate an
unattended performance from a clearly signaled interactive session so visitors
can tell whether they are watching token-derived duration or a recut state.

### Required preservation and reperformance tests

| Test | Reference expectation | Failure significance |
|---|---|---|
| Source/dependency package | reconstruct all three reviewed response hashes or a documented, rights-cleared equivalent package including p5.js 1.0.0 | high: current preservation gap remains amber |
| PRNG conformance | reproduce effective int32 states and first-ten vectors above in at least two independent implementations | high: changes all downstream parameters |
| Initialization conformance | reproduce published features and initial order vectors; record exact branch/call trace | high: genotype/phenotype divergence |
| Frame conformance | compare buffer and final output at defined draw calls over one nominal oscillator cycle | high for motion/order; minor pixel differences require measured tolerance |
| Input conformance | verify repeated `1`, `2`, reload, key repeat, focus loss, and non-US keyboard behavior | high for participation |
| Viewport/DPR matrix | square logical sizes at representative DPRs and wide/tall outer viewports | medium/high: geometry scales with `d`, while texture rasterization may vary |
| Browser/GPU matrix | current Chromium, Firefox, Safari/WebKit and software rendering where feasible | high if strip topology or color/alpha changes; bounded antialiasing variance may be acceptable after review |
| Long run/sleep-wake | multiple oscillator cycles, tab backgrounding, display sleep, and resume | medium/high: frame-based rather than elapsed-time motion must be documented |
| Network loss | execute from an authorized self-contained package with no CDN or generator availability | high: required for autonomous stewardship |

Migration or emulation must preserve token inputs, PRNG and JavaScript bitwise
semantics, frame-step motion, ordering state, and viewer controls. Any
technical modification shared under the recorded CC BY-NC 4.0 basis must be
attributed and change-marked. An emulator that changes raster antialiasing may
still be acceptable only after a documented perceptual comparison; it may not
silently claim pixel identity.

## Claim register

| ID | Material claim | Class | Qualifier | Source/date | Status |
|---|---|---|---|---|---|
| `CEN-CL-01` | The Museum scope is the three exact accessioned tokens listed above. | A/C | `source_static` | governed object records, reviewed 2026-08-02 | verified |
| `CEN-CL-02` | REAS identifies composition, slicing, recomposition, motion, and within-mint variation as central. | B | `artist_statement` | Art Blocks interview/project page | supported |
| `CEN-CL-03` | The renderer projects a fourteen-hex-digit hash prefix through JavaScript number parsing into xorshift32 state. | C | `source_static` | reviewed-hash official generator responses, re-read 2026-08-04 | provisional pending retained source |
| `CEN-CL-04` | Key `1` continues the PRNG to replace and permute cuts; key `2` orders current cuts without reseeding. | C | `source_static` | same | provisional pending independent execution |
| `CEN-CL-05` | The off-screen buffer is cleared per frame; motion is not a trail-accumulation process in this renderer. | C | `source_static` | same | provisional pending independent execution |
| `CEN-CL-06` | The pinned edition contains the empirical counts in the topology table. | C | `population_empirical` | complete descriptor/result hashes above | verified as descriptive snapshot result |
| `CEN-CL-07` | Two viewport hashes differed for each Museum token after a minimum 1,500 ms wait. | C | `execution_observed` | visual-observation record, 2026-08-01 | verified within stated limits |
| `CEN-CL-08` | #31, #724, and #401 make adjacency perceptible respectively as pressure, interval, and shallow depth. | E | `museum_interpretation` | Museum project/object essays and this dossier | supported, revisable |
| `CEN-CL-09` | The order and PRNG vectors in this dossier reproduce the currently served source. | C | `execution_instrumented` | in-memory reconstruction, 2026-08-04 | provisional; durable harness required |

## Unresolved questions and review gates

| Question | Evidence needed | Consequence |
|---|---|---|
| Can the exact wrapper, project script, feature script, and p5.js bytes be retained and redistributed? | rights review plus rights-cleared source acquisition | determines reproducibility-bundle contents and annotated-source publication |
| Why does published `Slice Count 0` coincide with `Cosmos` when the renderer constructs strips? | exact feature-script preservation and reconstruction | prevents a feature label from being mistaken for runtime ontology |
| Which static/live moment is artist- or platform-designated as the reference output? | platform rendering documentation and, ideally, artist/studio confirmation | affects conservation checkpoints and labels |
| Are the early vectors and order arrays independently reproduced from exact retained bytes? | second implementation and signed trace artifacts | required before publication as verified test vectors |
| What pixel/perceptual variance is acceptable across p5/browser/GPU migrations? | reference package, multi-environment render matrix, reviewed difference protocol | defines reperformance tolerance |
| Should `Janky`, alpha, and ordered counterfactuals be published? | rights, curatorial, and artist/studio consultation | determines public versus restricted atlas scope |
| What input parity is appropriate for touch, assistive technology, and reduced motion? | accessibility design and user testing | determines whether public participation is equivalent and intelligible |

Publication gates remain open: independent source reconstruction, technical
review, curatorial review, code/media rights review, accessible exhibit design,
cross-environment execution, persistent trace/artifact hashes, and release
fixity. Until those gates close, this is a complete research dossier and atlas
specification, not a governed or artist-approved publication.

## Publication package specification

- **Public thesis:** identity persists while adjacency changes.
- **Algorithm card:** full hash -> lossy seed projection -> moving buffer ->
  current strips -> circular aperture, with keys `1` and `2` distinguished.
- **Executable score:** the initialization, frame equation, and state machine
  above, independently implemented and hash-bound.
- **Causal atlas:** `CEN-ATLAS-01`-`08`, led by the synchronized three-token
  provenance view.
- **Collection map:** exact threshold bands, complete empirical counts, Museum
  trio coverage, and explicit absences; no rank or price.
- **Behavior film:** each token from load through one motion cycle, then one
  recut and an ordered-current state, with frame/input/environment identity.
- **Conservation note:** source/dependency gap, significant properties,
  conformance vectors, and perceptual-variance policy.
- **Accessibility:** text description of source/destination strips, keyboard
  alternatives, reduced-motion analytical stills, and narration/transcript for
  any behavior film.

[^artist]: Casey REAS, "In Conversation with Casey REAS on CENTURY," interview
    by Jeff Davis, Art Blocks, 21 June 2021,
    https://www.artblocks.io/articles/in-conversation-with-casey-reas-on-century;
    and "CENTURY by Casey REAS," Art Blocks,
    https://www.artblocks.io/collection/century-by-casey-reas. The interview and
    project page are used for artist/project statements, not as proof of the
    source reconstruction.

## Research status and boundaries

- **Working dossier ID:** `GSD-6529NM.2026.001-CENTURY`
- **Record family:** `GENERATIVE_SYSTEM_DOSSIER` (working; not governed)
- **Status:** constructed research dossier for independent technical, curatorial,
  rights, and accessibility review
- **Constructed:** 2026-08-04
- **Artist:** Casey REAS
- **Project:** *CENTURY*, Art Blocks Curated project 100, 2021
- **Museum scope:** `6529NM.2026.001.01`-`.03`
- **Working standard:** [`docs/generative-system-analysis.md`](../../../../docs/generative-system-analysis.md)

This dossier applies the Museum's working generative-system method to three
accessioned works. It does not amend their governed object, rights, condition,
or preservation records; constitute artist approval; authenticate an
unretained byte stream; establish autonomous software preservation; or make a
claim about rarity, price, desirability, or quality from feature prevalence.

The independently reviewed generator transcript records exact response-body
hashes, dependency declarations, and controls, but says that the response
bytes were not retained. Read-only retrieval on 2026-08-04 reproduced those
three hashes. The source analysis is therefore reconstructible against the
currently served official responses, but it is not yet reproducible from a
Museum-held source package. The current inline-script observations and
in-memory traces are working research, not independently reviewed evidence.

Retained Art Blocks metadata reports CC BY-NC 4.0 for the works. The governed
rights records control Museum uses. That license observation is not silently
extended into a representation that Art Blocks' wrapper, p5.js, or separately
extractable source code has the same license.
