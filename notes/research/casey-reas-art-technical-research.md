# Casey REAS seven-work donation: art-historical and time-based-media technical research

Status: focused research note; not an accession statement, title record, condition report, or adopted curatorial policy
Research date: 2026-08-01 UTC
Proposed accession lot: `6529NM.2026.001`
Proposed objects: `6529NM.2026.001.1` through `.7`, following `notes/wip/2026-08-01-casey-accession-working-plan.md`

## Research conclusion

The seven proposed works form a coherent study of executable images: a token hash fixes a project-specific starting condition, code performs a rule system, and a viewer encounters a changing output rather than only a stored picture. The group is defensible as a Museum research lot because it follows a legible arc from historical abstraction and permutation in **CENTURY**, through the recovered origins of Reas's Process grammar in **Pre-Process**, into artificial-life behavior in **Phototaxis**, finite combinatorics and distributed exhibition in **923 EMPTY ROOMS**, and a return to geometric form, shader-based rendering, and continuous motion in **Ex Nihilo (Cosmos)**.

That thesis is a Museum interpretation, not an artist statement. The three CENTURY tokens should be treated as a comparative A/B/C palette study only; there is no evidence in the sources reviewed that Reas selected those three tokens as a Museum-specific triptych. The research supports identity and technical description, but it does not establish donor title, transfer history, rights beyond the platform metadata, Museum custody association, or accession. All seven remain provisional until the accession gates are completed.

## Evidence discipline and current status

This note separates claims into the repository's evidence classes:

- **A — chain/platform identity:** contract, token ID, token hash, project, invocation, mint timestamp, and an indexed owner observation. The owner result below is an Art Blocks API observation and still needs direct chain verification.
- **B — artist or authoritative issuer:** Reas's project pages and statements, Art Blocks project records and interviews, Bright Moments's project note, and Art Blocks technical documentation.
- **C — Museum technical analysis:** script retrieval, UTF-8 byte counts, SHA-256 digests of the retrieved `projects_metadata.script` values, static code inspection, generator-HTML inspection, and visual review of media-proxy stills. These are observations of the retrieved state, not claims that the Museum has yet reproduced the works.
- **E — Museum interpretation:** the seven-work thesis, collection relationships, and conservation priorities.

Art Blocks GraphQL reported the same current `owner_address` for all seven tokens at the research snapshot: `0xbecfa2ba5a782d11e1a0e821e8f2e30b6684178c`. This is a useful custody lead, not proof of legal title, donor authority, Museum control, or accession. The repository's rule remains controlling: a transfer to a Museum-associated address does not itself accession a work.

The Art Blocks token metadata also reports `CC BY-NC 4.0` for all seven projects. That license label must not be expanded into assumed permissions for exhibition, publication, high-resolution reproduction, preservation copying, migration, derivative use, or AI training. Those uses need an explicit rights schedule and donor/title instrument.

## Provisional object schedule

The CAIP-19-shaped citations below identify the native Ethereum ERC-721 objects. They are not Museum accession numbers and do not assert title.

The selected Pre-Process record has an aspect ratio of 1.78; the reviewed token metadata does not return a palette feature for that project, so no palette is inferred.

| Proposed object | Native identity and token hash | Project/date evidence | Runtime and selected token features |
|---|---|---|---|
| `6529NM.2026.001.1` — **CENTURY #31** | `eip155:1/erc721:0xa7d8d9ef8d8ce8992df33d8b8cf4aebabd5bd270/100000031`; hash `0x55f52fb6b8134eb95200dfe109941c2df4ef53618d08598ccf7bd20a955bbfa9` | Art Blocks Curated, project `100`; released 2021-06-25; minted 2021-06-25 19:00:08 UTC | `p5@1.0.0`; square; palette A; slice count 16; line count 17; Oculi true |
| `6529NM.2026.001.2` — **CENTURY #724** | `eip155:1/erc721:0xa7d8d9ef8d8ce8992df33d8b8cf4aebabd5bd270/100000724`; hash `0x02a66fde5911ca99640218fb0b8143bf6d4b9da045626de7065f0a2c88453766` | Art Blocks Curated, project `100`; released 2021-06-25; minted 2021-06-25 19:04:52 UTC | `p5@1.0.0`; square; palette B; slice count 7; line count 11; Oculi true |
| `6529NM.2026.001.3` — **CENTURY #401** | `eip155:1/erc721:0xa7d8d9ef8d8ce8992df33d8b8cf4aebabd5bd270/100000401`; hash `0x8e536efbdddc966eb7cea6d719463fd1310cc9054e6e6850557a5fd69b49dd16` | Art Blocks Curated, project `100`; released 2021-06-25; minted 2021-06-25 19:02:56 UTC | `p5@1.0.0`; square; palette C; slice count 10; line count 15; alpha 209 |
| `6529NM.2026.001.4` — **Pre-Process #63** | `eip155:1/erc721:0x99a9b7c1116f9ceeb1652de04d5969cce509b069/383000063`; hash `0x0d800ffd4ec82f477918afd163ef9089a92f6b6bb5e81247671bbad6a27bcbd0` | Art Blocks Curated, project `383`; released 2022-11-30; minted 2022-11-30 18:25:23 UTC | `p5@1.0.0`; aspect ratio 1.78; Growth 4, Origin 1, Surface 8 |
| `6529NM.2026.001.5` — **Phototaxis #308** | `eip155:1/erc721:0xa7d8d9ef8d8ce8992df33d8b8cf4aebabd5bd270/164000308`; hash `0x0cfd2dddb2da0dcf086b6a7955e1d0201d0425566962d002be7669742bbec72c` | Art Blocks Playground, project `164`; released 2021-09-21; minted 2021-09-21 19:52:20 UTC | `p5@1.0.0`; square; Size Base; Speed Lively; Lights 3; Façade Atomic A; Sensors Nonlinear; Population Assemblage; Magnification 0.66 |
| `6529NM.2026.001.6` — **923 EMPTY ROOMS #713** | `eip155:1/erc721:0x145789247973c5d612bf121e9e4eef84b63eb707/1000713`; hash `0x293d12f425921929361c334bbe6402ff4eaf65b29d0b913df133e335f062896e` | Art Blocks × Bright Moments, project `1`; project release 2023-08-19; token minted 2023-08-18 16:57:59 UTC; relationship retained as unresolved | `p5@1.0.0`; square; City CDMX; code 555536; six shapes; four Pyramids, one Cargo, one Moon; gray background; Primary Form Pyramid |
| `6529NM.2026.001.7` — **Ex Nihilo (Cosmos) #248** | `eip155:1/erc721:0x0000000c687daed0fba60d1dba4e5f6149e8b894/248`; hash `0x09e7e497b272d55d199f92d3f0105d43d88f6f3b1f87e89f1ea64e4ea1ba01a8` | Art Blocks Studio / Feral File, project `0`; released 2026-03-10; minted 2026-03-11 16:41:35 UTC | `p5@1.9.0`; square; RGB false; CHUNK 3; # COSMOS 3; FFFFFF true |

For the projects in this schedule whose metadata exposes the encoded form — CENTURY, Pre-Process, Phototaxis, and 923 EMPTY ROOMS — the platform's token-ID rule is `projectId × 1,000,000 + invocation`; this explains, for example, `1000713` as project 1, invocation 713. Do not apply that rule to a Studio or Engine deployment unless the contract/API exposes the same encoding. The Ex Nihilo token API identifies `engine_type: studio`, `project_id: "0"`, and `tokenID: "248"`; although `0 × 1,000,000 + 248` also equals 248 arithmetically, that coincidence does not establish that the Studio contract encoded the ID with the shared rule. Record #248 as the contract/API token ID and keep its project and engine metadata separate. The full token records, generator URLs, and static-image URLs are listed in the source register below.

## Project research

### CENTURY, including #31, #724, and #401

**Sourced fact and artist account (B).** Reas describes CENTURY as a response to twentieth-century painting and drawing, with references to concrete and non-objective art, color-field painting, minimalism, and Ellsworth Kelly's cut-and-reassembled images. In an Art Blocks interview, he said an earlier version began in 2015 and was pushed into its present direction in 2021. The project released on Art Blocks on 25 June 2021 as 1,000 unique works. Reas describes each output as tied to a unique transaction hash; the Art Blocks technical record exposes a token hash used as the deterministic seed. Those descriptions should be retained as attributed terminology rather than silently collapsed into one claim.

**Technical constitution (C, based on the retrieved project script).** The Art Blocks `projects_metadata.script` value for project 100 was 8,975 UTF-8 bytes at observation time; its Museum-computed SHA-256 over that returned string is `fd6e03daada52c152eb00093d33c0ec56c27b94e120b7b0cef8fb72876409eec`. The project is reported as `p5@1.0.0`. The script reads the first 16 hexadecimal characters of `tokenData.hash` into a custom xorshift-style random generator; chooses among palettes and line colors; creates a square `WEBGL` canvas sized to the smaller browser dimension; and animates moving quadrilateral bands and ellipses. It generates slices of the base image and can scramble or restore their order. The script binds `1` to a randomized slice order and `2` to the ordered sequence.

The three selected tokens make the project legible as a narrow comparative sample: #31 is palette A, #724 palette B, and #401 palette C. Their other feature values differ, so the trio is not only a palette comparison. The platform's feature labels are metadata, not a complete description of visual significance.

**Runtime and dependencies.** Art Blocks supplies the browser wrapper, `tokenData`, CSS/canvas environment, and p5 dependency. The retrieved artist script contains no project-specific image, audio, network, or file-loading call in the static scan; this supports a working assumption of no external asset dependency, but a registrar-grade record must still capture the contract's dependency registry and the exact generator HTML. `WEBGL` makes browser graphics support and headless-render behavior relevant.

**Display and preservation.** Reas's platform description says the work is best seen large, in motion, and as live code. The media-proxy PNG is a reference still, not the full artwork. Preserve a fresh-load recording, an interaction recording showing slice reordering and restoration, the token hash, the complete project script, p5 dependency bytes, generator HTML, reference PNG, and the screen dimensions and browser/WebGL details for each capture.

**Museum interpretation (E).** The CENTURY trio makes historical abstraction operational: the image is not simply assembled from a palette but repeatedly cut, ordered, and recomposed. Its curatorial value for this lot lies in showing how a modernist language of seriality and non-composition becomes a time-based software behavior. The interpretation should not claim that these three tokens constitute the artist's complete palette system or that their grouping was artist-authored for the Museum.

### Pre-Process #63

**Sourced fact and artist account (B).** Reas traces the idea to 2003 experiments with circles, connecting their centers, and placing circles in motion. An unresolved version appeared in the 2005 Process/Drawing exhibition; it was not then a finished sale work. He describes the 2022 Art Blocks release as a completion of that origin point and as a key to understanding his Process practice. The project contains 120 works because its stated system combines eight surfaces, three origins, and five growth patterns. Reas's Element 1 is a circle that moves in a straight line, stays within the surface, changes direction on contact, and moves away from overlap. The official work record describes the medium as silent black-and-white custom software on a computer, with variable horizontal or vertical dimensions.

**Technical constitution (C).** The retrieved project script was 11,256 UTF-8 bytes; SHA-256 `205c3bc9cd5a019cb94cb797755538446cddd564ca69ea4f55b6d57e97568369`; `p5@1.0.0`. The script reads the token hash and token ID, creates a full-window 2D canvas, sets a 30 fps frame rate, and implements a 100-element system with the behavior structure described by Reas. It includes mouse and keyboard handlers, multiple numbered rendering modes, and pause behavior. The selected token's platform features are retained as opaque metadata labels — Growth 4, Origin 1, Surface 8 — until the artist's feature mapping is captured; they should not be decoded from numeric labels by assumption.

**Runtime and dependencies.** The script scan found no external asset, audio, or network-loading call. The runtime is nevertheless browser-, p5-, canvas-, and timing-dependent. The 1.78 token aspect ratio is a useful documentation fact, not a fixed display dimension: the live script is responsive to the available window.

**Display and preservation.** Preserve the default live behavior at the stated 30 fps, a paused state, the documented numbered modes, and a mouse-interaction test. Record whether the output reaches a stable visual rhythm or remains in motion during a practical display interval. The black-and-white reference still should be stored as a surrogate alongside a behavioral recording, not as a replacement for the software work.

**Museum interpretation (E).** Pre-Process is the hinge of the lot. It makes the historical continuity between early software sketches, the Process series, and blockchain distribution visible without pretending that the 2022 token is identical to a 2003 sketch. The work is most useful here as an example of an executable score whose historical meaning includes both the rule grammar and the delayed completion of that grammar.

### Phototaxis #308

**Sourced fact and artist account (B).** Reas describes Phototaxis as a simulated environment populated by simple machines, following the artificial-life lineage of Valentino Braitenberg's *Vehicles*. The four machine types are named Explorers, Aggressors, Lovers, and Cowards; each line records the movement of one machine. The artist's MicroImage account places the code's lineage in work dating to 2001 and identifies Phototaxis as a 2021 development for Art Blocks. Art Blocks released 1,000 unique works on 21 September 2021.

**Technical constitution (C).** The retrieved project script was 7,308 UTF-8 bytes; SHA-256 `57a994d9131fbdc79941579e3097d64291fb90bbfd1def3fc847f5df23bcc997`; `p5@1.0.0`. The API returns the script as a minified one-line value. Static inspection found a token-hash seed, four machine classes, a configurable light field, line-history drawing, a responsive window-sized canvas, and a custom random generator. The draw loop stops after 1,000 iterations by calling `noLoop()`; the work can be restarted or changed through `P`, `B`, `1`–`5`, and `L`. No external asset, audio, or network-loading call was found in the scan.

For #308, the authoritative feature set is Size Base, Speed Lively, Lights 3, Façade Atomic A, Sensors Nonlinear, Alignment Neutral, Population Assemblage, and Magnification 0.66. These values are more useful for identification and comparison than rarity language.

**Display and preservation.** A conservation capture must record the initial state, the point at which the 1,000-frame run stops, and at least one reset using `B`; a single still cannot show the work's accumulation of traces or its finite run state. Preserve the controls as part of the interface, not as optional platform decoration. The four machine behaviors and the light positions should be described as algorithmic behavior, not as claims that the program models biology.

**Museum interpretation (E).** Phototaxis shifts the lot from systems that rearrange marks to systems whose marks are records of behavior. The line is no longer only a graphic element: it is the residue of a simulated agent's movement. That makes this work a strong bridge between Reas's earlier software/print practice and the time-based, interactive preservation demands of the proposed donation.

### 923 EMPTY ROOMS #713

**Sourced fact and project account (B).** Art Blocks and Bright Moments describe 923 EMPTY ROOMS as an evolution of *An Empty Room*, a 2023 LACMA commission for *Coded: Art Enters the Computer Age, 1952–1982*. The project contains six primary forms, each associated with one of six cities: Sun/Tokyo, Shard/Berlin, Cargo/London, Hive/New York, Pyramid/Mexico City, and Moon/Los Angeles. The generative system contains 923 unique rooms/combinations using those six forms. Art Blocks and Bright Moments separately identify the authoritative fixed project edition as 924 unique artworks/tokens, while Art Blocks gives the project-level release date as 19 August 2023. Bright Moments documents a six-day mint/reveal schedule from 14–19 August at 12:00 EDT, maps CDMX to 18 August, and states that the 923-combination mint order was predetermined. Token #713 is identified as City CDMX and its token metadata records a 2023-08-18 16:57:59 UTC mint. This supports placing the token mint within the documented six-day schedule, but it does not establish the semantic relationship between that token timestamp and the project-level release date; preserve both observations and mark that relationship unresolved rather than calling the mint pre-release.

For an accession record, claim “fixed edition: 924 unique artworks/tokens; generative system: 923 unique rooms/combinations; this object: native token #713.” Do not describe the accession object as one of 923 tokens, or call a 924th token an extra room, unless token-level evidence supports that narrower claim.

**Technical constitution (C).** The retrieved script was 29,178 UTF-8 bytes; SHA-256 `5298304d3583d02f62aaf6e35c1ffd682c52468d69a74073833b7e280032661f`; `p5@1.0.0`. It uses a token-hash seed, a fixed combination list, a square `WEBGL` canvas, an off-screen WebGL surface, and custom shader code for line rendering. It derives the initial combination from the invocation number when the token is in the 923-work range. The script includes city display presets, diagram mode, color toggles, speed and scale controls, and a save-canvas command. Static scan found no external asset, audio, or network-loading call.

The selected #713 is identified by Art Blocks as City CDMX, code 555536, six shapes, four Pyramids, one Cargo, and one Moon, with no Sun, Shard, or Hive; its primary form is Pyramid and its background is Gray. Those feature facts should be retained exactly. The source code maps the city/form system, but feature-number semantics should remain tied to the platform's metadata until a project-specific feature dictionary is archived.

**Display and preservation.** Preserve the default token state and interaction states for diagram mode, city presets, color toggles, speed, and scale. Because the work uses WebGL and an off-screen surface, record browser, viewport, device-pixel ratio, graphics backend, and whether the render used hardware acceleration or SwiftShader. The six-city exhibition history is part of the work's context and should be retained in the curatorial record, while a still remains only one view of a room within a larger finite system.

**Museum interpretation (E).** 923 EMPTY ROOMS enlarges the problem of the generative image from one token to a finite, collectively navigable space. Its room is both a visual container and an index into a combinatorial field; its city structure makes distribution and exhibition part of the work's history. #713 is especially useful for this lot because its feature set reaches the six-shape limit while remaining a specific, reproducible room rather than a representative claim about the whole edition.

### Ex Nihilo (Cosmos) #248

**Sourced fact and artist/project account (B).** Art Blocks and Reas's Atomism materials place Ex Nihilo (Cosmos) within the Still Life series, which translates the five Platonic solids into generative software. The project focuses on the dodecahedron/Cosmos position in the stated sequence; it was co-presented by Art Blocks and Feral File in March 2026 and released as 256 unique works on 10 March 2026. The project description states that the solid is not presented as a stable object: its pixel values are translated into lines and the resulting field is designed to run continuously without repeating. The interface includes controls for channels, speed, pause, and generating a new state.

**Technical constitution (C).** The retrieved script was 20,434 UTF-8 bytes; SHA-256 `a9f5e37a95115ac398856a4878ff03b2ac52af3dd41765518943f24bee8c18b7`; `p5@1.9.0`. It creates a responsive `WEBGL` canvas, two off-screen p5 graphics buffers, a displacement texture, and custom vertex/fragment shaders. Its deterministic random class is seeded from `tokenData.hash`; it then creates one to three Cosmos forms, evolves their rotation, and renders red/green/blue or white line passes. The selected token is tagged RGB false, CHUNK 3, # COSMOS 3, and FFFFFF true. Controls include space for a new generated state, `P` for pause, `S` for speed, `R/G/B/W` for channel display, and a window-resize handler.

The live generator HTML observed for #248 loaded p5.js 1.9.0 from the Art Blocks generator wrapper and injected the token hash before the script. The script scan found no project-specific external asset or audio loader, but the work depends materially on browser WebGL, p5 renderer internals, shader compilation, and texture transfer behavior. Those dependencies must be recorded as conservation facts, not hidden under the general label “on-chain.”

**Display and preservation.** Preserve a fresh load, a paused state, a speed change, channel toggles, and a space-triggered regeneration. Because regeneration advances the deterministic PRNG and creates a new runtime state, record the event sequence and not just the token hash. The on-chain script, p5 1.9.0 dependency, generator HTML, shader source, default PNG, and a WebGL capability report are all required parts of the preservation package. A headless PNG is particularly insufficient for this work.

**Museum interpretation (E).** Ex Nihilo closes the proposed sequence by returning to elemental geometry while making the computer's rendering stack visible: pixels become lines, lines become a field, and the field becomes a continuously changing encounter. The selected monochrome/Cosmos state is not treated as a symbol for the whole Still Life series; it is a precise point at which the group returns from social and biological simulation to mathematical form.

## Seven-work curatorial thesis for Museum use

**Working title: _The Executable Image: Rule, Behavior, Room, Cosmos_.**

This donation should be interpreted as a study in the changing status of the image when the artist's medium is a rule system executed over time. The three CENTURY works establish the first condition: historical abstraction is translated into a program that generates, cuts, orders, and reorders a visual field. Pre-Process then exposes the historical substrate of Reas's Process practice, where circles, behaviors, and relations remain more fundamental than any one output. Phototaxis makes behavior itself the visible material, turning simulated machine movement into accumulated line. 923 EMPTY ROOMS expands that logic into a finite atlas of rooms whose combinations, cities, mint order, and exhibition history are inseparable from the work's public form. Ex Nihilo (Cosmos) returns to geometric fundamentals but shifts the conservation problem into shader execution, GPU behavior, and an explicitly continuous field of transformations.

The group is therefore not best described as seven attractive generative images. It is seven instances of a sustained question: where does the artwork reside — in the instructions, in the performance of the instructions, in the token-bound state, in the viewer's interaction, or in the resulting image? Reas's own statements repeatedly keep those terms in tension. The Museum's role is to preserve the tension rather than flatten it into a PNG catalogue. A responsible collection record must retain the native token and hash, the executable script and dependencies, the visual output, the interface, the runtime conditions, and the artist's descriptions of intended behavior.

The thesis has limits. It does not claim that these works constitute a complete Reas retrospective, a complete account of the Process lineage, a representative sample of every CENTURY palette, or a direct artist-authored sequence for the Museum. It is a defensible institutional reading of the specified seven objects, pending title, rights, custody, and technical verification.

## Time-based-media preservation and accession work still required

Before any object moves beyond `received_onchain` or `proposed donation`, the registrar and time-based-media reviewer should obtain and bind:

1. Direct Ethereum verification of each contract, token ID, mint event, current owner, and proposed Museum custody address; preserve transaction hashes and block numbers.
2. Donor identity/authority, title warranties, transfer instrument, encumbrance/dispute checks, and a `TITLE_BINDING` that names the specific transfer to which legal title relates.
3. A rights schedule that separately addresses display, publication, reference stills, video capture, migration, derivative preservation copies, print, and AI training. The platform's CC BY-NC label is not enough to fill unknown fields.
4. A locked project-script and dependency snapshot obtained from the contract/dependency registry, not only from the current Art Blocks API. Preserve the GraphQL response as a dated research snapshot and record its digest separately from the contract data.
5. A reproducible render protocol for each token: generator HTML, browser version, p5 version, viewport, device-pixel ratio, WebGL renderer, OS, timing, interaction state, capture date, and fixity hashes.
6. Artist/studio confirmation of display intent, acceptable fallbacks, preferred screen/projection scale, restart behavior, whether keyboard/mouse interaction is required, and which runtime changes would be materially significant.
7. Independent condition and integrity reports. Until those tests are run, use `not_assessed`; do not infer “green” from a successful marketplace PNG.

Recommended documentation package: `-MD01` metadata snapshot, `-IMG01` reference still, `-VID01` default/behavioral recording, `-TECH01` technical dossier, `-TX01` chain/provenance schedule, plus a shared lot-level rights and preservation manifest. The static image is a documentation surrogate unless the artist or project documentation authorizes it as a manifestation.

## Reproducible research method

On 2026-08-01 UTC, the Museum research pass used:

- Artist/project pages on REAS.com and the artist's archived project database for historical framing, medium, dates, and artist statements.
- Art Blocks project pages, token API responses, `projects_metadata`, and `tokens_metadata` for project/token identity, hash, invocation, mint time, aspect ratio, feature metadata, script type/version, and live/static URLs.
- Art Blocks generator HTML for the actual browser wrapper and dependency injection; the #248 wrapper visibly loaded p5.js 1.9.0 and injected `tokenData` before the artist script.
- Bright Moments's project note for the six-city exhibition, six forms, combination count, and mint-order context.
- A static scan of retrieved scripts for `load`, `fetch`, `XMLHttpRequest`, audio, and project-specific external assets. This is a triage scan, not a security or semantic audit.
- Visual inspection of the seven current media-proxy PNGs. Those images were used for preliminary visual description only and were not added to the repository.

The script SHA-256 values above are computed over the UTF-8 bytes of the current Art Blocks GraphQL `projects_metadata.script` strings. They are research fixity values for that API observation, not substitutes for contract bytecode or dependency-registry hashes.

## Sources

All web sources below were accessed or queried on 2026-08-01 UTC. The source list favors artist, platform, program, and technical documentation; market pages were not used for market claims.

### Artist and project sources

- [REAS.com project archive](https://gray.reas.com/) — artist-maintained archive context and project index.
- [CENTURY — REAS.com](https://www.gray.reas.com/century_s/) — artist statement and 2021 release date.
- [Pre-Process — REAS.com](https://www.gray.reas.com/pre_process/) — artist statement, medium, 2003 origin, Element 1 behavior grammar.
- [Phototaxis — REAS.com](https://www.gray.reas.com/phototaxis/) — simulated-machine description, MicroImage lineage, controls.
- [MicroImage — REAS.com](https://reas.com/microimage) — 2001–2005 lineage and 2021 p5.js/Art Blocks development context.
- [Process — REAS.com](https://reas.com/process) — Process lineage and relationship between rules, software, and outputs.
- [Atomism — REAS.com](https://reas.com/atomism) — Still Life and 923 EMPTY ROOMS context.
- [Still Life (RGB A) — REAS.com](https://gray.reas.com/still_life_la/) — earlier Still Life medium/display context.
- [In Conversation with Casey REAS on CENTURY — Art Blocks](https://www.artblocks.io/articles/in-conversation-with-casey-reas-on-century) — artist interview on 2015/2021 development, Kelly reference, motion, and transaction-hash language.
- [In Conversation with Casey REAS on Pre-Process — Art Blocks](https://www.artblocks.io/articles/in-conversation-with-casey-reas-on-pre-process) — artist interview on the 2003/2005 history, 120 permutations, and Element behavior system.

### Project and token sources

- [CENTURY — Art Blocks](https://www.artblocks.io/collection/century-by-casey-reas)
- [Pre-Process — Art Blocks](https://www.artblocks.io/collection/pre-process-by-casey-reas)
- [Phototaxis — Art Blocks](https://www.artblocks.io/collection/phototaxis-by-casey-reas)
- [923 EMPTY ROOMS — Art Blocks](https://www.artblocks.io/collection/923-empty-rooms-by-casey-reas) — fixed edition 924 unique artworks; 923 unique rooms/combinations; project release date 2023-08-19.
- [Ex Nihilo (Cosmos) — Art Blocks](https://www.artblocks.io/collection/ex-nihilo-cosmos-by-casey-reas)
- [923 Empty Rooms — Bright Moments](https://www.brightmoments.io/923emptyrooms) — edition size 924; 923 combinations; six-day mint/reveal schedule and predetermined combination order.
- [CENTURY #31 token API](https://token.artblocks.io/1/0xa7d8d9ef8d8ce8992df33d8b8cf4aebabd5bd270/100000031) · [#724](https://token.artblocks.io/1/0xa7d8d9ef8d8ce8992df33d8b8cf4aebabd5bd270/100000724) · [#401](https://token.artblocks.io/1/0xa7d8d9ef8d8ce8992df33d8b8cf4aebabd5bd270/100000401)
- [Pre-Process #63 token API](https://token.artblocks.io/1/0x99a9b7c1116f9ceeb1652de04d5969cce509b069/383000063)
- [Phototaxis #308 token API](https://token.artblocks.io/1/0xa7d8d9ef8d8ce8992df33d8b8cf4aebabd5bd270/164000308)
- [923 EMPTY ROOMS #713 token API](https://token.artblocks.io/1/0x145789247973c5d612bf121e9e4eef84b63eb707/1000713)
- [Ex Nihilo (Cosmos) #248 token API](https://token.artblocks.io/1/0x0000000c687daed0fba60d1dba4e5f6149e8b894/248) — `engine_type: studio`, `project_id: 0`, `tokenID: 248`.

### Technical sources

- [Art Blocks Token & Generator APIs](https://docs.artblocks.io/developer/token-and-generator-apis/) — token metadata, live generator, media proxy, and GraphQL endpoints.
- [Art Blocks GraphQL Reference](https://docs.artblocks.io/developer/graphql/) — project and token fields, including scripts, script versions, hashes, features, mint times, and render URLs.
- [Art Blocks On-Chain Generator](https://docs.artblocks.io/protocol/on-chain-generator/) — generator assembly, `tokenData`, p5 versions, dependency handling, and browser/runtime model.
- [NFT Metadata Storage at Art Blocks](https://docs.artblocks.io/protocol/on-chain-storage/) — on-chain scripts, dependencies, generator, and browser relationships.
- [Art Blocks Core Contract V3](https://docs.artblocks.io/developer/core-contract/) — project scripts, token hashes, dependency registry, and token-ID structure.
- [Art Blocks production GraphQL endpoint](https://data.artblocks.io/v1/graphql) — queried `projects_metadata` and `tokens_metadata`; query results were not copied into the repository as raw API dumps.
