# Casey Reas accession research: art-historical and technical dossier

**Research status:** working research record; not an accession act, title opinion, custody assertion, or governance approval.

**Research date:** 2026-08-01 UTC.

**Scope:** CENTURY #31, #724, and #401; Pre-Process #63; Phototaxis #308; 923 EMPTY ROOMS #713; and Ex Nihilo (Cosmos) #248. The object numbers below are provisional Museum identifiers for the planned accession lot `6529NM.2026.001`; chain custody, legal title, donor instrument, transfer transaction, and final accession status remain separate records to be completed by the registrar.

## How to read this note

The dossier keeps four kinds of statement apart:

- **Documented fact [A/B]:** a chain/platform record, project publisher, artist site, artist-authored technical note, or commissioning institution records it.
- **Artist or project statement [B]:** the artist or presenting platform describes the work, its intent, or its expected behavior. This is authoritative evidence of the stated conception, not independent proof of every technical claim.
- **Technical observation/inference [C]:** the Museum observed a current live response, or inferred a consequence from an authoritative technical record. It is dated and must be re-tested at accession.
- **Museum interpretation [E]:** a provisional curatorial reading. It is not a statement of artist intent unless separately attributed.

The seven token numbers were supplied as the proposed donation contents and are mapped below to the project contracts and token IDs visible in Art Blocks’ project records and generator routes. This mapping does **not** prove that `networkmuseum.6529.eth` currently controls the objects or that a donation has occurred.

## Research conclusion

The seven proposed works form a coherent Museum research lot about executable images: a token-bound state is made performable by code, and the viewer encounters a changing output rather than only a stored picture. The group traces a defensible arc from modernist recombination in **CENTURY**, through the recovered Process grammar of **Pre-Process**, artificial-life behavior in **Phototaxis**, finite combinatorics and distributed exhibition in **923 EMPTY ROOMS**, and geometric/pixel simulation in **Ex Nihilo (Cosmos)**. This is a Museum interpretation, not an artist-authored sequence; the three CENTURY tokens are a comparative sample, not an asserted artist-defined triptych.

At the research snapshot, Art Blocks GraphQL reported the same `owner_address` for all seven tokens: `0xbecfa2ba5a782d11e1a0e821e8f2e30b6684178c`. That is an API observation and custody lead, not proof of legal title, donor authority, Museum control, or accession. Art Blocks token metadata reported `CC BY-NC 4.0`; that label does not by itself establish permissions for display, publication, preservation copying, migration, derivative use, or AI training. Those matters require separate title, rights, and accession records.

## Provisional object schedule and technical identity

For the Art Blocks V3 projects in this schedule, Art Blocks documents the token-ID relationship as `tokenId = (projectId × 1,000,000) + invocation`; its V3 Core Contract powers Studio, Curated, and Engine projects. Ex Nihilo (Cosmos) #248 is a V3.2.4 Studio deployment: the token API records `engine_type: studio`, `project_id: 0`, and `tokenID: 248`, which decodes as project 0, invocation 248 (`248 = (0 × 1,000,000) + 248`). Keep the raw API fields and decoded fields separate; this technical decoding does not establish title, custody, or accession. The generator endpoints below were requested on 2026-08-01 UTC. The response SHA-256 values are retrieval snapshots of the returned UTF-8 HTML bodies; they are not substitutes for the token’s on-chain script, token hash, metadata, or a legal title binding.

| Provisional object | Work / supplied number | Ethereum contract | Art Blocks project / token ID | Current generator dependency observed | Generator response SHA-256 |
|---|---|---|---|---|---|
| `6529NM.2026.001.01` | CENTURY #31 | `0xa7d8d9ef8d8ce8992df33d8b8cf4aebabd5bd270` | project 100 / `100000031` | p5.js 1.0.0 via cdnjs | `465b45798f14bea109f59986bd2cdcfd6e2eb9050327f52b24af15e159704ae2` |
| `6529NM.2026.001.02` | CENTURY #724 | `0xa7d8d9ef8d8ce8992df33d8b8cf4aebabd5bd270` | project 100 / `100000724` | p5.js 1.0.0 via cdnjs | `1dfd3f2205e8c4a33f85d2c0efce35b019d2ea21e424e5d750bc86c3890c3b3e` |
| `6529NM.2026.001.03` | CENTURY #401 | `0xa7d8d9ef8d8ce8992df33d8b8cf4aebabd5bd270` | project 100 / `100000401` | p5.js 1.0.0 via cdnjs | `51ab1073b166701c9379984d9331c14d803dc84e35c8d06b5a8071f4eb895aad` |
| `6529NM.2026.001.04` | Pre-Process #63 | `0x99a9b7c1116f9ceeb1652de04d5969cce509b069` | project 383 / `383000063` | p5.js 1.0.0 via cdnjs | `8cbf3ee01db1a864163eeb5b30776372917256b9246b255e0f514cf03b64505b` |
| `6529NM.2026.001.05` | Phototaxis #308 | `0xa7d8d9ef8d8ce8992df33d8b8cf4aebabd5bd270` | project 164 / `164000308` | p5.js 1.0.0 via cdnjs | `b3d7c39954beabf85cb6213eff3d57e3b1f7670c6763c663bc426a9c918bcaf3` |
| `6529NM.2026.001.06` | 923 EMPTY ROOMS #713 | `0x145789247973c5d612bf121e9e4eef84b63eb707` | project 1 / `1000713` | p5.js 1.0.0 via cdnjs | `2d722fe294710e3b443802baecc1f445b94cf00bf9dbdfbebbb08d4d6d3529e0` |
| `6529NM.2026.001.07` | Ex Nihilo (Cosmos) #248 | `0x0000000c687daed0fba60d1dba4e5f6149e8b894` | project 0 / token `248` / invocation `248` | p5.js 1.9.0 via cdnjs | `17402c7259ac4af1e93894eb74b36a5796a6a058ea0fb0e56d2f55101a3c84f9` |

**Technical caution.** The current generator response exposes a p5.js CDN script, but that is a snapshot of the present generator route. The accession package must also capture the token hash, project script, dependency metadata, contract state, generator HTML, and a local render test. Art Blocks’ own documentation explains that the generator assembles the artist script, token hash, and dependencies; it does not make the Museum’s one-time retrieval hash a permanent claim about future gateway behavior.

### Token metadata snapshot [A/C]

The following values were queried from Art Blocks token/project metadata on 2026-08-01 UTC. The CAIP-19-shaped citations identify the native Ethereum ERC-721 objects; they are not Museum accession numbers or title claims.

| Work | Native object and token hash | Mint observation | Selected project features |
|---|---|---|---|
| CENTURY #31 | `eip155:1/erc721:0xa7d8d9ef8d8ce8992df33d8b8cf4aebabd5bd270/100000031`; `0x55f52fb6b8134eb95200dfe109941c2df4ef53618d08598ccf7bd20a955bbfa9` | 2021-06-25 19:00:08 UTC | Palette A; Line Count 17; Slice Count 16; Oculi true |
| CENTURY #724 | `eip155:1/erc721:0xa7d8d9ef8d8ce8992df33d8b8cf4aebabd5bd270/100000724`; `0x02a66fde5911ca99640218fb0b8143bf6d4b9da045626de7065f0a2c88453766` | 2021-06-25 19:04:52 UTC | Palette B; Line Count 11; Slice Count 7; Oculi true; Janky true |
| CENTURY #401 | `eip155:1/erc721:0xa7d8d9ef8d8ce8992df33d8b8cf4aebabd5bd270/100000401`; `0x8e536efbdddc966eb7cea6d719463fd1310cc9054e6e6850557a5fd69b49dd16` | 2021-06-25 19:02:56 UTC | Palette C; Line Count 15; Alpha true; Alpha Value 209 |
| Pre-Process #63 | `eip155:1/erc721:0x99a9b7c1116f9ceeb1652de04d5969cce509b069/383000063`; `0x0d800ffd4ec82f477918afd163ef9089a92f6b6bb5e81247671bbad6a27bcbd0` | 2022-11-30 18:25:23 UTC | Aspect ratio 1.78; Growth 4; Origin 1; Surface 8; no palette feature returned |
| Phototaxis #308 | `eip155:1/erc721:0xa7d8d9ef8d8ce8992df33d8b8cf4aebabd5bd270/164000308`; `0x0cfd2dddb2da0dcf086b6a7955e1d0201d0425566962d002be7669742bbec72c` | 2021-09-21 19:52:20 UTC | Size Base; Speed Lively; Lights 3; Sensors Nonlinear; Population Assemblage |
| 923 EMPTY ROOMS #713 | `eip155:1/erc721:0x145789247973c5d612bf121e9e4eef84b63eb707/1000713`; `0x293d12f425921929361c334bbe6402ff4eaf65b29d0b913df133e335f062896e` | 2023-08-18 16:57:59 UTC | City CDMX; Code 555536; six shapes; four Pyramids, one Cargo, one Moon; gray background |
| Ex Nihilo (Cosmos) #248 | `eip155:1/erc721:0x0000000c687daed0fba60d1dba4e5f6149e8b894/248`; `0x09e7e497b272d55d199f92d3f0105d43d88f6f3b1f87e89f1ea64e4ea1ba01a8` | 2026-03-11 16:41:35 UTC | `engine_type: studio`; project 0; RGB false; CHUNK 3; # COSMOS 3; FFFFFF true |

The token hashes and mint times are platform/API observations pending direct chain verification. The project script and generator response hashes elsewhere in this dossier are separate retrieval-fixity values, not contract bytecode or dependency-registry hashes.

### Project-script retrieval and static observations [C]

The Museum also retrieved the current `projects_metadata.script` values from Art Blocks GraphQL on 2026-08-01 UTC and computed SHA-256 over each returned UTF-8 string. These values describe the retrieved API state; they do not replace an on-chain script/dependency snapshot.

| Project | Script bytes | Script SHA-256 | Runtime/behavior observed |
|---|---:|---|---|
| CENTURY | 8,975 | `fd6e03daada52c152eb00093d33c0ec56c27b94e120b7b0cef8fb72876409eec` | `p5@1.0.0`; square `WEBGL`; hash-seeded random generator; moving bands/ellipses; slice reorder keys `1`/`2` |
| Pre-Process | 11,256 | `205c3bc9cd5a019cb94cb797755538446cddd564ca69ea4f55b6d57e97568369` | `p5@1.0.0`; full-window 2D canvas; 30 fps; 100 elements; mouse/keyboard interaction and pause |
| Phototaxis | 7,308 | `57a994d9131fbdc79941579e3097d64291fb90bbfd1def3fc847f5df23bcc997` | `p5@1.0.0`; four machine classes; light field; accumulated line history; stops after 1,000 frames |
| 923 EMPTY ROOMS | 29,178 | `5298304d3583d02f62aaf6e35c1ffd682c52468d69a74073833b7e280032661f` | `p5@1.0.0`; square `WEBGL`; off-screen surface; custom shaders; fixed combination list; diagram/city/speed/scale controls |
| Ex Nihilo (Cosmos) | 20,434 | `a9f5e37a95115ac398856a4878ff03b2ac52af3dd41765518943f24bee8c18b7` | `p5@1.9.0`; responsive `WEBGL`; off-screen buffers; displacement texture; custom shaders; channel/pause/speed/new-state controls |

The static triage scan found no project-specific external image, audio, network, or file-loading calls in these retrieved scripts. That is not a security or semantic audit and does not eliminate browser, CDN, p5.js, shader, WebGL, timing, or contract-dependency preservation requirements. The media-proxy PNGs were reviewed as preliminary reference stills only, not as complete manifestations of the works.

## CENTURY (2021)

### Documented work identity and conception [A/B]

Art Blocks identifies CENTURY as a 1/1/1,000 generative project released 2021-06-25. The artist’s project record describes it as a response to twentieth-century painting and drawing, especially the cut-and-reassembled works Ellsworth Kelly made in the 1950s. The artist’s contemporary Art Blocks interview further identifies George Rickey as a reference for motion and chance, and describes the project’s compositional core as slicing and recomposing an image.

The artist’s current project taxonomy places CENTURY within a larger body of work concerned with modernist abstraction, seriality, modular form, optical effects, and the translation of those histories into software. That later taxonomy is useful context but is a retrospective artist-site synthesis; the 2021 Art Blocks interview is the nearer-in-time primary source for the release conception.

### Medium, algorithm, and output logic

- **Medium [B/C]:** browser-based custom generative software, with a live animated manifestation and an Art Blocks ERC-721 registration. The current Art Blocks generator route for each proposed token loads p5.js 1.0.0 and injects the token data before the artist script.
- **System [B]:** the system uses the token’s transaction hash to establish a distinct base picture. The artist describes controlled variation in line count, line thickness, slice count, palette, and related parameters; the work then applies movement and permits the base image to be cut and recombined in live viewing.
- **Edition [A/B]:** 1,000 unique artworks; release date 2021-06-25.
- **Token-specific project features [A/B]:** Art Blocks’ current token records expose project-generated feature fields. The three proposed tokens are recorded here descriptively, without marketplace rarity percentages or ranks:

  - **#31:** `Alpha=false`; `Janky=false`; `Oculi=true`; `Palette=A`; `Line Count=17`; `Slice Count=16`; `Slice Order=Chaos`; `Line Quantity=Less`; `Line Color Options=4`; `Oculus 1 Major Axis=1.68`; `Oculus 2 Major Axis=0.59`.
  - **#724:** `Alpha=false`; `Janky=true`; `Oculi=true`; `Palette=B`; `Line Count=11`; `Slice Count=7`; `Slice Order=Chaos`; `Line Quantity=Less`; `Line Color Options=4`; `Oculus 1 Major Axis=0.96`; `Oculus 2 Major Axis=0.42`.
  - **#401:** `Alpha=true`; `Janky=false`; `Oculi=true`; `Palette=C`; `Line Count=15`; `Alpha Value=209`; `Slice Count=10`; `Slice Order=Chaos`; `Line Quantity=Less`; `Line Color Options=2`; `Oculus 1 Major Axis=1.63`; `Oculus 2 Major Axis=0.55`.

The labels above are retained as project metadata, not converted into claims about artistic quality, scarcity, market value, or curatorial importance. Their semantics should be checked against the project script and the final Art Blocks metadata snapshot during accession.

### Runtime and display expectations [B/C]

The artist describes the work as intended to be experienced in motion rather than as a single still. The live view can be left running and the `1` key exposes the cut-and-recompose interaction described in the artist’s interview. The browser generator provides the practical screen manifestation; no authoritative installation specification for monitor size, projector calibration, orientation, or viewing duration was found in this pass.

**Accession preservation requirement:** retain the live generator HTML, token hash, project script, p5.js dependency reference, a static capture, a short interaction recording, and a display note distinguishing the still capture from the live work. Verify whether current behavior remains deterministic under repeated reloads and whether external CDN access is required by the returned HTML.

### Museum interpretation [E]

The three CENTURY outputs are best treated as a comparative sample from one generative system, not as a complete CENTURY survey or an artist-defined triptych. The palette and parameter differences provide a useful way to examine how one program distributes color, line density, slicing, opacity, and motion across individual tokens. The set also makes a direct institutional point: a museum can preserve both the token-specific state and the broader program that makes each state performable.

## Pre-Process (2022; originating in 2003)

### Documented work identity and conception [A/B]

The artist’s project record identifies Pre-Process as 2022 custom software, black and white, silent, computer-based, with variable dimensions and horizontal or vertical presentation. The artist traces its origin to 2003 experiments in which circles were drawn, connected, and set in motion through code. The artist links those experiments to the later Process series and describes the blockchain release as an archival completion of an unresolved origin point.

The artist’s Art Blocks interview records that an early version was shown at the 2005 Process/Drawing exhibition but was not offered for sale because it was unfinished. The interview describes the 2022 edition of 120 as the complete set of significant permutations of the system.

### Medium, algorithm, and output logic

- **Medium [B/C]:** custom black-and-white, silent generative software; the current Art Blocks generator response for #63 loads p5.js 1.0.0 and returns a browser-viewable document.
- **Constituent system [B]:** each output uses 100 circle Elements. Each Element has a form and four behaviors: movement in a straight line; constraint to the display surface; a change of direction upon contact with another Element; and movement away from overlap. These rules describe a behavioral system rather than a precomposed image.
- **Finite edition logic [B]:** eight surfaces × three origins × five growth configurations = 120. The surfaces change how the Elements are rendered; the origins are center, horizontal line, or random positions; and the growth configurations vary the relative sizes of the Elements. The artist’s description makes the edition logic structural, not a market scarcity claim.
- **#63 project metadata [A/B]:** the Art Blocks token page records aspect ratio `1.78`, `Growth=4`, `Origin=1`, and `Surface=8`, but no palette feature in the reviewed metadata. These are descriptive output fields. Their human-readable meanings must be retained alongside the project’s own feature vocabulary rather than guessed from ordinal values; no palette is inferred.

### Runtime and display expectations [B/C]

The artist describes Pre-Process as moving toward, but never reaching, equilibrium, so a still image is only one state of a time-based software performance. The project record supports horizontal or vertical display and variable dimensions. The current generator response supplies the p5.js runtime; exact browser version, canvas scaling behavior, frame rate, and whether any non-CDN dependency is needed must be documented by the Museum’s reproducibility test.

**Accession preservation requirement:** save the generator response, token hash, project script, dependency snapshot, a representative still, a time-based screen recording, and a render test showing the same token across two clean browser environments. Record whether the Museum’s chosen display is a live manifestation or an authorized documentation surrogate.

### Museum interpretation [E]

Pre-Process is a particularly useful anchor for the accession because it connects the artist’s early rule-based software practice to a later blockchain edition without treating the token as the origin of the work. It also supplies a clear case study for the Museum’s distinction between code, performance, and image: the accession must preserve all three layers and must not reduce the work to the static thumbnail returned by a marketplace.

## Phototaxis (2021; code lineage from 2001)

### Documented work identity and conception [A/B]

Art Blocks identifies Phototaxis as a 1/1/1,000 project released 2021-09-21. The artist’s project page calls it a simulated environment containing simple machines. It names four machine types—Explorers, Aggressors, Lovers, and Cowards—and states that the core code grew out of the artist’s MicroImage work and earlier experiments.

In an artist-authored technical note dated 2021-09-18, Reas describes each line as a record of one software organism’s movement through the simulation. The note connects the work to Valentino Braitenberg’s *Vehicles* and to earlier Path and Tissue software. It records a code lineage from C++ to Processing/Java and then to p5.js/JavaScript for browser release.

### Medium, algorithm, and output logic

- **Medium [B/C]:** browser-based generative software drawing, with a current Art Blocks generator response that loads p5.js 1.0.0. The project is not adequately described as a still-image collection: its line fields are traces of simulated movement and its interface exposes ongoing computation.
- **System [B]:** simulated machines respond to environmental lights according to behavior classes. Coordinates accumulated during the simulation are joined into lines, so each visible path is both a graphic mark and a record of system behavior.
- **Edition [A/B]:** 1,000 unique Art Blocks outputs, released 2021-09-21. The artist describes the edition as a selected region of a much larger possibility space rather than a claim that the 1,000 outputs exhaust the system.
- **#308 project metadata [A/B]:** Art Blocks currently records `Size=Base`, `Speed=Lively`, `Lights=3`, `Façade=Atomic A`, `Sensors=Nonlinear`, `Alignment=Neutral`, `Population=Assemblage`, and `Magnification=0.66`. These are project feature assertions, not OpenSea rarity data and not Museum-authored evaluations.

### Runtime and display expectations [B/C]

The artist’s technical note gives unusually specific display behavior:

- the simulation stops after 1,000 iterations for the initial thumbnail state;
- `P` pauses and resumes the simulation;
- `B` restarts from the beginning;
- `1` through `5` change magnification;
- `L` reveals the locations of the simulated lights;
- the light locations are fixed per mint, with two to seven lights in the general project; #308’s current metadata says three.

These controls make a live screen presentation materially different from a static image. The accession record should preserve the initial capture, the live state, the interaction map, and a short recording of a restart-and-resume session. The current p5.js CDN reference must be rechecked against the final generator response and stored with its retrieval date and content hash.

### Museum interpretation [E]

Phototaxis brings an artificial-life lineage into the proposed group. Its visual marks are not merely abstract lines; they are the accumulated traces of agents reacting to an environment. In the accession, that distinction creates a productive counterpoint to CENTURY’s cut-and-recomposition logic and Pre-Process’s circle-and-behavior grammar: all three are rule-based systems, but they make different kinds of agency visible—reassembly, collision/avoidance, and environmental response.

## 923 EMPTY ROOMS (2023)

### Documented work identity and conception [A/B]

Art Blocks identifies 923 EMPTY ROOMS as a 2023 Art Blocks × Bright Moments project. Bright Moments presents it as an evolution of the LACMA-commissioned *An Empty Room*. The official Bright Moments record assigns six fundamental colorforms to six galleries/cities: Sun/Tokyo, Shard/Berlin, Cargo/London, Hive/New York, Pyramid/Mexico City, and Moon/Los Angeles.

The Bright Moments record describes a six-day release and in-person reveal across those cities. Art Blocks identifies the fixed project edition as 924 unique artworks and gives the project-level release date as 2023-08-19. Bright Moments separately lists edition size 924, 923 combinations, release dates 2023-08-14 through 2023-08-19 at 12:00 EDT, and CDMX on 2023-08-18. Token #713 is identified as City CDMX and its token metadata records a 2023-08-18 16:57:59 UTC mint. This supports placing the mint within the documented six-day schedule, but it does not establish the semantic relationship between the token timestamp and the project-level release date; preserve both observations and mark that relationship unresolved rather than calling the mint pre-release. LACMA’s official Art + Technology record places *An Empty Room* within the exhibition *Coded: Art Enters the Computer Age, 1952–1982* and describes the project as a software response to Victor Vasarely’s unrealized 1967–71 proposal for a grid-based machine capable of producing many permutations of colored forms. This is the authoritative institutional context for the relationship between *An Empty Room* and the later *923 EMPTY ROOMS* release; it does not make #713 an LACMA-commissioned work.

### Medium, algorithm, and output logic

- **Medium [B/C]:** browser-based generative software presented through an Ethereum token and a multi-city exhibition/reveal format. The current Art Blocks generator response for #713 loads p5.js 1.0.0.
- **System [B]:** six colorforms are combined using a combination-with-replacement approach. Bright Moments describes the full mint as the set of possible combinations, and says the release order begins with simpler combinations and proceeds through more complex ones. That is a project release rule, not a Museum or marketplace rarity metric.
- **Edition and discrepancy [A/B]:** The authoritative project size for accession metadata is 924 unique artworks/tokens, as reported by both Art Blocks and Bright Moments. The generative system is separately described as 923 unique rooms/combinations. The accession record may claim “fixed edition: 924 unique artworks/tokens; generative system: 923 unique rooms/combinations; this object: native token #713.” It should not call the object one of 923 tokens or call a 924th token an extra room unless token-level evidence supports that narrower claim. The invocation manifest still needs to be preserved and checked; no theory about a special starting/terminal output is adopted here.
- **#713 project metadata [A/B]:** Art Blocks currently records `Red=false`, `Blue=false`, `Green=true`, `City=CDMX`, `Code=555536`, `# Suns=0`, `# Hives=0`, `# Moons=1`, `# Cargos=1`, `# Shapes=6`, `# Shards=0`, `# Pyramids=4`, `Background=Gray`, and `Primary Form=Pyramid`. The code and counts should be preserved as source metadata; they should not be converted into a third-party rarity score.

### Runtime and display expectations [B/C]

The official project record supports a live browser manifestation and documents the six-city reveal as part of the work’s public presentation history. Bright Moments also says that viewing or attending the physical events was not required to acquire a token, which keeps the exhibition history distinct from title and ownership.

The Museum should preserve #713 as both a token-specific state and a member of a finite combinatorial system. The live generator response, the static render, a short live recording, the project explorer/mint-order documentation, and the six colorform definitions belong in the preservation package. A screen-based installation can reference the multi-city exhibition history, but it must not imply that the Museum is recreating the original six-city event.

### Museum interpretation [E]

923 EMPTY ROOMS is the accession’s clearest example of a finite generative system whose meaning includes distribution, sequencing, and collective completion. Its relationship to *An Empty Room* is best stated as a documented evolution and institutional dialogue, not as a simple edition or sequel. The project’s six-city structure also expands the accession’s curatorial frame from the individual screen to a networked exhibition logic.

## Ex Nihilo (Cosmos) (2026)

### Documented work identity and conception [A/B]

The artist’s NFT register identifies Ex Nihilo (Cosmos) as a 1/1/256 Ethereum work released 2026-03-10 through Art Blocks × Feral File. Art Blocks’ official project record calls it the latest work in the Still Life series and identifies the dodecahedron as its subject within the five Platonic solids. The same record maps the series’ solid/form associations and states that future works will address the remaining solids.

The project description links the title to the generation of images from code rather than physical materials. It describes the solid as being decomposed into pixels, with pixel values translated into lines whose positions and colors produce a continuing visual field. The artist’s official taxonomy and bitforms’ exhibition record place this work in a longer Still Life investigation of simulation, geometry, pixels, and the relationship between software and traditional pictorial forms.

### Medium, algorithm, and output logic

- **Medium [A/B/C]:** browser-based, color, silent, long-form generative software registered as an Ethereum token. The current Art Blocks generator response for #248 loads p5.js 1.9.0.
- **System [B]:** the dodecahedral source is not displayed as a stable three-dimensional object. The stated process transforms pixel information into line positions and colors, producing a field that moves between geometric structure and visual dissolution.
- **Edition [A/B]:** 256 unique artworks; Art Blocks and Feral File presented the work in March 2026 through a ranked auction/settlement format. The auction mechanism is provenance/release history, not evidence of artistic quality or a Museum selection criterion.
- **#248 project metadata [A/B]:** Art Blocks currently records `engine_type=studio`, `project_id=0`, `tokenID=248`, `RGB=false`, `CHUNK=3`, `0000FF=false`, `00FF00=false`, `FF0000=false`, `FFFFFF=true`, and `# COSMOS=3`. This is a V3.2.4 Studio deployment, so the documented V3 token-ID structure decodes the raw token ID as project 0, invocation 248 (`248 = (0 × 1,000,000) + 248`). Retain `engine_type`, `project_id`, `tokenID`, and decoded `invocation` as separate source fields; the technical decoding is not a custody, title, or accession claim.

### Runtime and display expectations [B/C]

Art Blocks’ official record documents live controls: `R`, `G`, and `B` toggle channels; `W` changes the display to white; `S` adjusts speed; `P` pauses; and the spacebar generates a new Still Life state. The work is described as designed to run continuously and not repeat. Because the live state can be changed by the viewer, a static image must be catalogued as a capture or documentation surrogate rather than as the whole manifestation.

**Accession preservation requirement:** preserve the #248 generator response, token hash, project script, p5.js 1.9.0 dependency reference, static output, live recording, interaction instructions, and a note explaining which state is used for display. The Museum should test whether “new Still Life” is seeded solely by the token/program state or introduces another runtime state; this is a technical verification question, not an assumption.

### Museum interpretation [E]

Ex Nihilo (Cosmos) extends the accession’s concern with elemental systems from the flat colorforms of 923 EMPTY ROOMS into a dodecahedral/pixel/line system. Its relation to CENTURY and Pre-Process is not a claim of direct formal descent; it is a curatorial comparison of how different rule systems translate an abstract vocabulary into a time-based image. The work also gives the collection a contemporary endpoint without presenting the seven objects as a complete survey of Reas’s practice.

## Curatorial thesis: *The Executable Image: Rule, Behavior, Room, Cosmos*

The donation should be interpreted as a study in the changing status of the image when the medium is a rule system executed over time. The sequence moves from historical abstraction made operational in CENTURY, through Process grammar and artificial-life behavior, into a finite atlas of rooms whose combinations and exhibition history are part of the work, and finally to geometric form rendered as a continuously changing shader field. The Museum should preserve the tension among instructions, performance, token-bound state, viewer interaction, and resulting image rather than flattening the group into seven static catalogue pictures.

## Curatorial relationships among the seven objects

The following relationships are Museum interpretations grounded in the artist and platform records above:

1. **System as medium.** Each work makes a rule system part of its constitution. CENTURY cuts and recomposes; Pre-Process moves circles through behavioral constraints; Phototaxis records simulated machines responding to lights; 923 EMPTY ROOMS enumerates colorform combinations; and Ex Nihilo (Cosmos) translates geometric/pixel data into an ongoing line field.
2. **Time is not decoration.** CENTURY’s live recomposition, Pre-Process’s unresolved movement, Phototaxis’s accumulating trajectories, and Ex Nihilo’s continuous Still Life are time-based manifestations. 923 EMPTY ROOMS adds a different temporal structure: a finite work released over six days and staged across six cities. The accession should therefore document both static surrogates and live behavior.
3. **From inherited histories to computational form.** CENTURY explicitly addresses twentieth-century abstraction; Pre-Process carries a 2003 origin into a 2022 blockchain edition; Phototaxis carries a 2001 artificial-life/code lineage into browser generative art; 923 EMPTY ROOMS develops the LACMA/Vasarely dialogue through a distributed combinatorial release; Ex Nihilo (Cosmos) carries Platonic geometry and computer-graphics abstraction into a 2026 long-form work.
4. **Atoms, units, and fields.** The group can be read through its basic units: slices and lines; circles and behaviors; organisms, lights, and trajectories; six colorforms; and pixels/lines/dodecahedral structure. This is a comparative framework, not a claim that the artist uses one universal algorithm.
5. **A focused, not comprehensive, accession.** The seven objects represent five connected lines of inquiry—modernist recombination, Process grammar, artificial-life drawing, finite combinatorics, and geometric/pixel simulation. The three CENTURY tokens are a small comparative sample. They should not be described as a complete CENTURY set, a complete Reas retrospective, or an artist-defined canonical group.

## Provenance, title, and accession limits

The sources in this note establish project conception, platform metadata, current generator routes, and relevant exhibition context. They do **not** establish:

- current ownership or custody by `networkmuseum.6529.eth`;
- a donor’s legal title or authority to transfer;
- a completed donation agreement or copyright/display-rights grant;
- a specific Museum accession decision;
- the exact mint transaction, transfer transaction, block, or finality state;
- the immutable status of every dependency shown by the current generator route;
- the completeness of the project’s preservation package.

Those matters require separate evidence classes and registrar/technical records. In particular, no object should be promoted from proposed lot to accessioned object merely because an address appears to hold it, because a platform labels it as a project token, or because an output won a governance vote.

## Rarity and feature-handling policy for this research

This dossier does not use OpenSea rarity ranks, percentages, trait counts, or derived marketplace scores. OpenSea is not used as evidence for the technical or curatorial descriptions above.

The token-level feature fields transcribed here come from Art Blocks’ own project/token records and are preserved as descriptive metadata. They do not become Museum “rarity” claims. If the Museum later publishes an internal NextGen-style analysis for a generative accession, it must be a separately versioned, open, reproducible artifact containing:

- the exact input token/project manifest and retrieval timestamps;
- the source code and dependency lockfile;
- the feature vocabulary and mathematical definitions;
- the output table and deterministic checksums;
- a statement of what the analysis can and cannot measure;
- independent review showing that descriptive features have not been converted into unsupported judgments of artistic value.

## Required next research and accession tests

1. Fetch and hash the final token metadata, token hash, project script, dependency records, and generator HTML for all seven objects from authoritative/chain sources.
2. Independently verify contract address, token ID, mint transaction, current owner, transfer history, block/finality, and custody receipt for each object.
3. Resolve the 923-combination versus 924-token discrepancy from the project’s invocation manifest and record the result as an append-only amendment if the current interpretation changes.
4. Render each token in at least two clean environments, record browser/runtime versions, compare deterministic captures, and document any network/CDN dependency.
5. Request or verify artist/platform display instructions, especially for live duration, screen/projection orientation, color management, interaction, and whether a still or recording may serve as a public surrogate.
6. Complete rights, donor credit, title, provenance, sanctions, and encumbrance review separately from the art-historical description.
7. Have one art-historical reviewer and one technical/registrar reviewer sign the accession dossier before any object is marked `accessioned`, `technically_verified`, or `display_ready`.

## Source register

All URLs were retrieved or checked on **2026-08-01 UTC**. Source-quality notes use the Museum’s evidence vocabulary: **A** = directly chain/platform-verifiable or live technical response; **B** = artist, issuer, presenting platform, or commissioning-institution authority; **C** = Museum observation/inference; **E** = Museum interpretation.

### Artist-authored and artist-controlled sources

- [CENTURY project record](https://www.gray.reas.com/century_s/) — **B**. Artist-controlled project database entry; establishes the homage, Kelly reference, transaction-hash relationship, and 2021 release statement.
- [CENTURY project overview](https://reas.com/century) — **B**. Current artist-site synthesis of the broader CENTURY body of work; useful contextual source, with retrospective editorial framing.
- [Artist interview on CENTURY](https://www.artblocks.io/articles/in-conversation-with-casey-reas-on-century) — **B**. Artist-authored statements published by the presenting platform in 2021; strongest source here for motion, slicing, parameter variation, and display interaction.
- [Pre-Process project record](https://www.gray.reas.com/pre_process/) — **B**. Artist-controlled project entry; establishes medium, date, origin story, Element 1, and display orientation.
- [Process / Pre-Process overview](https://reas.com/process) — **B**. Current artist-site account of Process and Pre-Process; establishes the 8 × 3 × 5 permutation logic, with retrospective editorial framing.
- [Artist interview on Pre-Process](https://www.artblocks.io/articles/in-conversation-with-casey-reas-on-pre-process) — **B**. Artist interview published by Art Blocks in 2022; establishes the 100-Element system, permutation logic, and unfinished 2005 history.
- [Phototaxis project record](https://www.gray.reas.com/phototaxis/) — **B**. Artist-controlled project entry; establishes the machine types, artificial-life framing, and controls.
- [Artist technical note on Phototaxis](https://medium.com/@REAS/notes-on-phototaxis-db7aa7641ad8) — **B**. Artist-authored technical note dated 2021-09-18; strongest source for code lineage, iteration behavior, controls, and edition scope.
- [MicroImage project context](https://reas.com/microimage) — **B**. Current artist-site synthesis of the MicroImage/Phototaxis lineage; useful for long-term context, not treated as independent technical verification.
- [Atomism project overview](https://reas.com/atomism) — **B**. Current artist-site synthesis; establishes the relationship among Still Life, An Empty Room, 923 EMPTY ROOMS, and pixel/element recomposition, with retrospective editorial framing.
- [Artist NFT register](https://reas.com/nfts) — **B**. Artist-controlled list of project dates, edition structures, chains, and platforms; used for the 1/1/N descriptions and Ex Nihilo release record.

### Platform, presenter, and institutional sources

- [Art Blocks CENTURY collection](https://www.artblocks.io/collection/century-by-casey-reas) — **A/B**. Platform-authoritative project identity, edition size, and release date.
- [Art Blocks Pre-Process collection](https://www.artblocks.io/collection/pre-process-by-casey-reas) — **A/B**. Platform-authoritative project identity, edition size, and release date.
- [Art Blocks Phototaxis collection](https://www.artblocks.io/collection/phototaxis-by-casey-reas) — **A/B**. Platform-authoritative project identity, edition size, and release date.
- [Bright Moments 923 Empty Rooms archive](https://www.brightmoments.io/923emptyrooms) — **B**. Co-presenter’s official release and exhibition record; authoritative for colorforms, cities, schedule, combination logic, and the stated 923/924 figures.
- [Art Blocks 923 EMPTY ROOMS collection](https://www.artblocks.io/collection/923-empty-rooms-by-casey-reas) — **A/B**. Platform-authoritative project identity, edition size, release date, and current project metadata.
- [LACMA project record](https://www.lacma.org/zh/node/42726) — **B**. Commissioning institution’s official record for *METAVASARELY* and *An Empty Room*; establishes the Vasarely/LACMA context and separation between the two components.
- [LACMA Art + Technology interview with Reas](https://unframed.lacma.org/2023/02/13/introducing-metavasarely-and-empty-room-two-part-digital-work-casey-reas) — **B**. Institutional publication containing Reas’s interview responses; used for the artist’s account of simulating rather than fabricating Vasarely’s proposed machine and for the CENTURY/LACMA relationship.
- [Art Blocks Ex Nihilo (Cosmos) release record](https://www.artblocks.io/collection/ex-nihilo-cosmos-by-casey-reas/purchase) — **A/B**. Platform and co-presenter release record; establishes Still Life context, dodecahedron/COSMOS, 256-output release, continuous behavior, controls, and March 2026 presentation.
- [Feral File Casey Reas artist/exhibition page](https://feralfile.com/exhibitions/artist/casey-reas-nsa) — **B**. Presenting platform record for the Ex Nihilo exhibition and the artist’s related work; useful corroboration of the 2026 exhibition context.
- [bitforms Still Life exhibition record](https://www.bitforms.art/exhibition/casey-reas/) — **B**. Gallery exhibition and checklist record; used for Still Life medium, live display, series chronology, and the geometric/pixel context. It is not used as chain or ownership evidence.

### Technical platform sources and token records

- [Art Blocks protocol overview](https://docs.artblocks.io/protocol/overview/) — **A/B**. Official technical explanation of on-chain scripts, token hashes, deterministic generation, and generator architecture.
- [Art Blocks on-chain generator](https://docs.artblocks.io/protocol/on-chain-generator/) — **A/B**. Official generator assembly and dependency documentation; used for the runtime model and token-ID formula.
- [Art Blocks Core Contract V3](https://docs.artblocks.io/developer/core-contract/) — **A/B**. Official contract documentation for project scripts, token hashes, dependency variants, the V3 contract coverage of Studio, Curated, and Engine projects, and the encoded token-ID rule; used here for the #248 project/invocation decoding.
- [Art Blocks token and generator APIs](https://docs.artblocks.io/developer/token-and-generator-apis/) — **A/B**. Official URL patterns and API guidance for live views, static media, and authoritative token/project data.
- [Art Blocks GraphQL reference](https://docs.artblocks.io/developer/graphql/) — **A/B**. Official field reference for project scripts, script versions, token hashes, invocation, mint time, feature fields, and render URLs.
- [CENTURY #31 token record](https://www.artblocks.io/token/1/0xa7d8d9ef8d8ce8992df33d8b8cf4aebabd5bd270/100000031) — **A/B**. Art Blocks token page; used for project-generated feature assertions.
- [CENTURY #724 token record](https://www.artblocks.io/token/1/0xa7d8d9ef8d8ce8992df33d8b8cf4aebabd5bd270/100000724) — **A/B**. Art Blocks token page; used for project-generated feature assertions.
- [CENTURY #401 token record](https://www.artblocks.io/token/1/0xa7d8d9ef8d8ce8992df33d8b8cf4aebabd5bd270/100000401) — **A/B**. Art Blocks token page; used for project-generated feature assertions.
- [Pre-Process #63 token record](https://www.artblocks.io/token/1/0x99a9b7c1116f9ceeb1652de04d5969cce509b069/383000063) — **A/B**. Art Blocks token page; used for the `Growth`, `Origin`, and `Surface` feature assertions.
- [Phototaxis #308 token record](https://www.artblocks.io/token/1/0xa7d8d9ef8d8ce8992df33d8b8cf4aebabd5bd270/164000308) — **A/B**. Art Blocks token page; used for project-generated feature assertions.
- [923 EMPTY ROOMS #713 token record](https://www.artblocks.io/token/1/0x145789247973c5d612bf121e9e4eef84b63eb707/1000713) — **A/B**. Art Blocks token page; used for project-generated feature assertions and token ID mapping.
- [Ex Nihilo (Cosmos) #248 token record](https://www.artblocks.io/token/1/0x0000000c687daed0fba60d1dba4e5f6149e8b894/248) — **A/B**. Art Blocks token page; used for project-generated feature assertions and token ID mapping.
- [CENTURY #31 generator response](https://generator.artblocks.io/1/0xa7d8d9ef8d8ce8992df33d8b8cf4aebabd5bd270/100000031), [#724](https://generator.artblocks.io/1/0xa7d8d9ef8d8ce8992df33d8b8cf4aebabd5bd270/100000724), and [#401](https://generator.artblocks.io/1/0xa7d8d9ef8d8ce8992df33d8b8cf4aebabd5bd270/100000401) — **A/C**. Live Art Blocks generator responses observed 2026-08-01; used for current p5.js 1.0.0 dependency observations and retrieval hashes.
- [Pre-Process #63 generator response](https://generator.artblocks.io/1/0x99a9b7c1116f9ceeb1652de04d5969cce509b069/383000063), [Phototaxis #308](https://generator.artblocks.io/1/0xa7d8d9ef8d8ce8992df33d8b8cf4aebabd5bd270/164000308), and [923 EMPTY ROOMS #713](https://generator.artblocks.io/1/0x145789247973c5d612bf121e9e4eef84b63eb707/1000713) — **A/C**. Live generator responses observed 2026-08-01; used for current p5.js 1.0.0 dependency observations and retrieval hashes.
- [Ex Nihilo (Cosmos) #248 generator response](https://generator.artblocks.io/1/0x0000000c687daed0fba60d1dba4e5f6149e8b894/248) — **A/C**. Live generator response observed 2026-08-01; used for current p5.js 1.9.0 dependency observation and retrieval hash.
