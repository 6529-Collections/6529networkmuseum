# Generative system analysis standard

## 1. Purpose

Generative art should be encountered before it is audited.

A museum account of generative art should explain more than what an output
looks like and more than which metadata traits it carries. It should make the
work intelligible as an authored system without pretending that code exhausts
its meaning.

This standard requires a dossier to connect four things:

1. the exact source, seed, parameters, runtime, and dependencies that constitute
   the studied system;
2. the transformations by which those inputs become behavior and appearance;
3. the structure of the edition or possible-output space;
4. an art-historical and object-led interpretation that remains answerable to
   close looking.

The resulting public scholarship is called **Inside the System**. Its
institutional research object is a **Generative System Dossier**. The public
name may change without changing this standard or the record boundary.

## 2. Scope and exclusions

The method applies to deterministic and stochastic generative editions,
interactive and time-based software works, rules-based static works, and
systems that incorporate external or learned models. Sections that do not
apply must be marked `not_applicable`, never silently omitted.

The dossier supplements rather than replaces:

- the accession statement and object record;
- title, custody, provenance, rights, and condition records;
- the preservation dossier and retained evidence manifests;
- artist/project statements and curatorial publications;
- the NextGen-compatible trait-prevalence method in
  [`docs/generative-trait-analysis.md`](generative-trait-analysis.md).

Trait prevalence describes a documented population. It does not establish
quality, value, desirability, importance, artist intent, or the causal role of
a parameter. The generative-system dossier must not become a rarity ranking.

## 3. The analytical object

Every dossier separates six layers that are often collapsed into “the
algorithm.”

| Layer | Question |
|---|---|
| **Identity** | What fixes this work or edition member as itself? |
| **Genotype** | What seed, invocation, parameters, assets, and authored rules define its starting conditions? |
| **Initial phenotype** | What first visible or audible state follows from those conditions in the reference environment? |
| **Performance** | What changes through time, feedback, simulation, randomness, or external input? |
| **Participation** | Which states can a viewer, operator, platform, or environment alter, and are those changes reversible? |
| **Encounter** | What is actually perceived in a particular display, duration, scale, and social setting? |

The layers are related but not interchangeable. A screenshot is evidence of
an encounter, not necessarily the work's complete state. A token hash may be
an identity input, not the sole artwork. A viewer-triggered continuation may
be authentic behavior without becoming a new canonical token state.

## 4. Claim and evidence discipline

### 4.1 Existing Museum evidence classes

Every material claim retains the Museum class from
[`docs/record-model.md`](record-model.md):

- `A` — direct chain evidence;
- `B` — authoritative issuer, artist, platform, or governance source;
- `C` — Museum technical verification or controlled observation;
- `D` — third-party historical or scholarly source;
- `E` — attributed curatorial interpretation.

### 4.2 Method qualifiers

The dossier adds a method qualifier. It refines rather than replaces the
evidence class.

| Qualifier | Permitted claim |
|---|---|
| `source_static` | A statement directly reconstructible from identified source bytes without executing them |
| `source_formal` | A mathematical result or proof derived from identified source or an authoritative specification |
| `execution_observed` | A result seen in a declared environment and protocol |
| `execution_instrumented` | A result emitted by declared Museum observation hooks without altering the artwork's governing logic |
| `population_empirical` | A result computed from a pinned, quality-checked population snapshot |
| `artist_statement` | A statement attributed to the artist or authorized project source |
| `museum_interpretation` | A contestable Museum reading, explicitly presented as interpretation |

Each material claim receives a stable claim ID, class, qualifier, source,
observation or publication date, and status. Use `verified`, `supported`,
`provisional`, or `unresolved`; do not manufacture numerical confidence.

### 4.3 Prohibited collapses

A dossier must not:

- infer artist intent from code;
- infer a canonical manifestation from the most convenient screenshot;
- treat dormant code as active behavior;
- treat a platform feature label as equivalent to an internal variable without
  proving the mapping;
- replace authored probability with observed frequency, or the reverse;
- describe an analytical counterfactual as an authentic artwork state;
- infer completeness from successful execution in one browser;
- infer accession, title, copyright, or permission from custody or source
  availability.

## 5. Source lock and research boundary

Analysis starts with a source lock. It records the exact object(s), chain
citation where applicable, project and feature scripts, generator envelope,
dependencies, assets, metadata, authoritative statements, observation date,
retrieval method, byte length, hash, retention status, and rights restriction.

The lock distinguishes:

- **referenced** bytes: observed and hashed but not retained;
- **retained** bytes: present in a content-addressed evidence or preservation
  package;
- **reconstructed** material: Museum-authored pseudocode, traces, diagrams, or
  test harnesses;
- **remote dependencies**: required resources whose future availability or
  mutability remains outside Museum control.

No dossier may describe referenced-only source as preserved. Exact code may be
quoted, annotated, redistributed, or transformed only when the relevant rights
record permits it. Secrets, private custody information, and exploitable
infrastructure details stay outside the public dossier.

## 6. Identity, seed, and randomness reconstruction

The dossier traces identity from authoritative input to every random or
pseudorandom decision. It records, as applicable:

- token hash, invocation, edition index, transaction input, user input,
  external feed, or model state;
- parsing, truncation, byte order, signed/unsigned coercion, bitwise behavior,
  overflow, and language-specific number semantics;
- PRNG family, state width, initialization, warm-up, stream splitting,
  alternation, reseeding, and number-consumption order;
- mapping from raw draws to booleans, ranges, weighted choices, shuffles,
  distributions, or rejection loops;
- seeded and unseeded randomness, including runtime or dependency randomness;
- whether interaction resets the seed, continues the current stream, mutates
  state without consuming randomness, or introduces a new uncontrolled input.

A seed claim is incomplete unless an independent implementer can reproduce a
declared checkpoint. At least one test vector should bind input, normalized
seed state, early random values, derived parameters, and output-state digest
where rights and technical conditions permit.

## 7. Parameter provenance

Every visible or behaviorally significant parameter is classified by origin:

| Origin | Meaning |
|---|---|
| `identity_derived` | deterministically derived from the work's authoritative identity input |
| `invocation_derived` | determined by edition or invocation number |
| `runtime_evolving` | changes through the work's own state transition |
| `viewer_controlled` | changed through documented interaction |
| `environmental` | supplied by viewport, clock, GPU, browser, network, device, or external feed |
| `dependency_default` | inherited from a library, platform, shader, model, or runtime default |
| `museum_analytical` | introduced only in a Museum trace or counterfactual |

Record the exact domain, mapping, units, default, dependence, and downstream
effect. Published traits are cross-checked against internal variables but
remain separate facts until their mapping is demonstrated.

## 8. Algorithmic score

The dossier supplies a human-readable score that another technically capable
reader can follow without treating a source listing as the interpretation.
The score contains:

1. inputs and normalization;
2. initialization and random choices;
3. entities or data structures;
4. per-step state transition;
5. rendering or sonification stages;
6. interaction handlers;
7. termination, looping, reset, or persistence;
8. dormant, unreachable, or uncertain paths clearly marked as such.

Use compact pseudocode, equations, dependency graphs, or state machines where
they make causal relations clearer. Preserve language-specific edge cases when
they affect results. A simplified score must identify every simplification.

## 9. Time and state profile

For time-based work, define the state vector and transition boundary. Record:

- initialization time and reference frame;
- frame, tick, event, wall-clock, audio-clock, or network-clock dependence;
- fixed versus variable timestep;
- feedback buffers and prior-frame dependence;
- finite duration, convergence, stopping condition, or indefinite evolution;
- pause, reset, reload, resize, sleep/wake, and focus behavior;
- session persistence and whether a session can be resumed exactly;
- which moments are artist-designated, platform-selected, viewer-triggered,
  or Museum-selected for documentation.

Behavior should be documented at a duration appropriate to the system. A
single initial render is insufficient for a work whose principal structure is
temporal.

## 10. Collection topology

The dossier explains the project as a population, not only as one output.

For finite or enumerated projects, provide:

- the state space or coordinate product;
- the map from invocation or identity to coordinates;
- proof of coverage, uniqueness, exclusions, and exceptional states;
- an inverse map where practical;
- the exact location of Museum-held works.

For probabilistic projects, provide:

- authored distributions and dependencies;
- unreachable or constrained combinations;
- theoretical support distinct from empirical occurrence;
- a pinned empirical snapshot only when needed, with quality and exclusion
  reports under the NextGen-compatible method.

For open-ended or externally driven systems, define a bounded study frame and
state explicitly why the full output space cannot be enumerated.

The collection map is an interpretive and explanatory instrument. It must not
rank works by scarcity, price, desirability, or importance.

## 11. Render and media pipeline

Trace each transformation between internal state and encounter, including:

- coordinate systems, geometry, compositing, color spaces, blend modes, masks,
  shaders, buffers, filters, cameras, projection, audio synthesis, encoding,
  and display scaling;
- the role and order of every intermediate representation;
- GPU, browser, library, font, codec, network, model, and device dependencies;
- precision, implementation-defined behavior, nondeterminism, and fallbacks;
- accessibility transformations and whether they are part of the work or a
  Museum access layer.

Intermediate buffers are especially important when the final image is a
measurement, displacement, accumulation, feedback, or translation of another
image. The dossier should show which representation the viewer sees and which
representations remain causal but hidden.

## 12. Interaction semantics

Each control is described by input, precondition, state mutation, randomness
effect, reversibility, persistence, and visible consequence. Classify it as:

- `reveal` — exposes an existing cause or layer;
- `view` — changes scale, camera, framing, or channel without changing the
  underlying generative state;
- `render` — changes the rendering of the same behavioral state;
- `state` — advances or mutates the work's internal state;
- `identity` — selects or creates a different authoritative identity;
- `environment` — changes conditions external to the authored state.

Interface labels, keyboard case, touch parity, focus behavior, and undocumented
controls are tested rather than assumed. Participation is interpreted at the
level where it enters the system; interaction does not automatically make the
viewer a co-author.

## 13. Exact-object close reading

Every project dossier must return from the collection-wide system to the exact
Museum-held object. It should explain:

- the object's identity-derived coordinates and starting conditions;
- which visible events follow from those conditions;
- what develops only through time or interaction;
- what the object shares with and withholds from the broader project;
- why the exact object matters to the Museum's project-level argument.

This section must include close visual, spatial, temporal, or sonic analysis.
Parameter decoding alone is not close reading.

## 14. The causal atlas

The primary explanatory object is a **causal atlas**: a set of reproducible,
rights-cleared exhibits that lets a reader follow one cause through the
system. Each exhibit declares:

- source and environment lock;
- exact baseline identity and state;
- the single isolated intervention;
- all variables intentionally held constant;
- expected and observed consequence;
- trace or artifact digest;
- whether the result is an authentic work state, an observed performance, or
  a Museum-made analytical surrogate;
- reset and replay procedure;
- accessibility description and public-use rights.

Preferred exhibit families are seed provenance, parameter isolation, temporal
trace, hidden-cause reveal, intermediate-buffer pipeline, interaction state
machine, object comparison, and collection map. Counterfactuals should isolate
one cause whenever possible. A visually dramatic but causally ambiguous
demonstration fails the standard.

The atlas may include diagrams, traces, synchronized playback, equations,
instrumented overlays, or derived stills. None is silently presented as the
artwork.

## 15. Conservation and reperformance

The dossier identifies significant properties at three levels:

1. **identity properties** — authoritative seed, invocation, source, assets,
   parameters, and title/chain bindings;
2. **behavioral properties** — state transitions, timing relationships,
   interaction consequences, randomness consumption, and feedback;
3. **experiential properties** — scale, duration, motion, responsiveness,
   color, sound, projection, and viewing conditions.

For each property, record test method, tolerance, evidence, known variance, and
failure consequence. Define an environment matrix spanning the reference
environment and justified alternatives. Include dependency loss, network
failure, resize, high-DPI, reduced motion, input-device parity, browser/GPU
variance, clock variance, and long-duration behavior where applicable.

The conservation note distinguishes bit preservation, functional
reperformance, emulation, migration, reinterpretation, and documentation-only
access. It states who may authorize a change, how the change is marked, and
what comparison would establish acceptable continuity. A working remote
generator is not a preservation package.

## 16. Instrumented analysis

Observation tooling is separate from the artwork. It loads pinned or
lawfully referenced source, inserts declared hooks at named boundaries, and
emits deterministic traces where determinism is claimed. It must not rewrite
the governing logic, consume the work's random stream, change frame order, or
mask environment errors.

Minimum tests are:

- source and dependency hash binding;
- seed and invocation replay;
- early PRNG checkpoint vectors;
- feature-to-internal-parameter mapping;
- state-transition and interaction replay;
- single-variable counterfactual isolation;
- trace determinism or an explicit nondeterminism report;
- population coverage for finite exhaustive projects;
- fail-closed behavior on source, asset, dependency, or environment drift.

Instrumentation code, configuration, trace schema, tool version, and known
observer effects are reviewed independently from the interpretive essay.

## 17. Publication architecture

The complete research package can produce seven public layers:

1. a short curatorial thesis;
2. an algorithm card;
3. the human-readable algorithmic score;
4. the causal atlas;
5. the collection map;
6. a behavior or state-transition film where time matters;
7. a reproducibility and conservation note.

Public presentation follows progressive disclosure: encounter first, thesis
second, explanatory system third, technical and evidentiary apparatus last.
The scholarship must remain usable by non-programmers without withholding the
precision required for independent reconstruction.

A reader-facing dossier must not open with record status, accession mechanics,
rights boilerplate, source-retention caveats, or method vocabulary. Its opening
sequence is:

1. title and one-sentence curatorial proposition;
2. close looking at the exact Museum work;
3. the project-level artistic argument;
4. an intelligible account of the system;
5. deeper technical, comparative, and causal material;
6. evidence, rights, conservation, status, and review apparatus at the end.

The controls remain complete; they simply do not demand the reader's attention
before the art has earned it.

All analytical media carry attribution, rights, change-marking, surrogate
status, alt text or transcript, source binding, and persistent citation. The
Museum publishes unresolved questions when they materially affect the reading.

## 18. System-family extensions

The common dossier remains stable across system families, but each family adds
specific controls.

| System family | Additional required analysis |
|---|---|
| Deterministic static output | exact render entry point, output dimensions, font/color/precision behavior, and proof that no later state is significant |
| Simulation or autonomous process | state vector, update order, timestep, boundary conditions, convergence/termination, observer duration, and long-run test |
| Interactive work | complete input state machine, device and accessibility parity, session persistence, reversible/irreversible changes, and operator/display protocol |
| Data-driven or networked work | endpoint and schema lock, observation timestamp, caching/fallback, authentication boundary, outage behavior, privacy, and a lawful replay dataset |
| Machine-learning system | exact model/weights or service version, architecture, preprocessing, conditioning, sampler, seed, inference parameters, safety filters, nondeterminism, training-data statement where authoritative, and model/data rights |
| On-chain autonomous system | chain/contract/block context, storage and event reads, oracle or registry dependencies, reorganization/finality assumptions, and deterministic offline replay where feasible |
| Physical or hybrid system | hardware identifiers, sensors/actuators, calibration, material tolerances, control software, latency, installation plan, and substitution authority |
| Collaborative or evolving system | contribution authority, moderation, version lineage, state ownership, deletion/withdrawal behavior, and the boundary between work state and documentation |

When a work spans families, all relevant extensions apply. An external API or
model version that cannot be pinned is documented as a preservation risk, not
treated as an ordinary dependency. A replay dataset or model surrogate must be
identified as a Museum preservation or analytical layer unless authoritative
evidence establishes it as part of the artwork.

## 19. Dossier data model

The working record family is `GENERATIVE_SYSTEM_DOSSIER`. Until a schema and
interoperability profile pass independent review, dossiers remain research
documents and must not claim governed record status.

The future machine-readable payload should link rather than duplicate the
accession, object, rights, condition, visual-observation, preservation, and
trait records. Its minimum components are:

- `source_lock`
- `claims`
- `randomness_profile`
- `parameter_provenance`
- `algorithmic_score`
- `state_and_time_profile`
- `interaction_profile`
- `render_pipeline`
- `collection_topology`
- `object_readings`
- `causal_atlas_manifest`
- `execution_observations`
- `environment_matrix`
- `curatorial_argument`
- `conservation_requirements`
- `uncertainties`
- `review`

Any governed implementation must use the Museum record envelope, canonical
payload hash, append-only supersession, constructor/reviewer separation,
public/restricted boundary, and stable subject identifiers. A future Stream
mapping must be added to
[`docs/stream-interoperability.md`](stream-interoperability.md); this standard
does not invent or claim a deployed Stream schema.

## 20. Review and release gates

A dossier is ready for substantive review only when:

- every exact object, source, dependency, and authoritative statement is
  identified;
- seed handling and parameter provenance are reconstructible;
- fixed, temporal, interactive, and environmental state are separated;
- authored probabilities and empirical frequencies are separated;
- finite completeness claims include a proof;
- code, execution, statements, and interpretation use distinct qualifiers;
- each causal exhibit is reproducible and unmistakably labeled;
- exact Museum works receive close reading;
- conservation requirements test behavior as well as files;
- rights and public/restricted status are explicit;
- material uncertainty, dormant code, mismatches, and observer effects are
  reported;
- citations and local evidence links resolve;
- an independent technical reviewer can reconstruct the central claims;
- an independent curatorial reviewer finds that the interpretation remains
  contestable, object-led, and worth reading after the mechanism is known.

Publication requires both reviews, rights clearance for every public artifact,
accessibility review, and a fixity-checked release package. Constructor and
reviewer must be different people or agents under the Museum control model.

## 21. Definition of world-class

World-class analysis achieves four forms of fidelity at once:

- **computational fidelity:** exact inputs, coercions, random streams, state
  transitions, and dependencies are reconstructible;
- **collection fidelity:** the structure of the possible or issued population
  is demonstrated without turning difference into market rank;
- **experiential fidelity:** time, interaction, display, and hidden rendering
  stages are treated as part of what the work does;
- **interpretive fidelity:** the analysis makes an original, evidence-bounded
  argument about the art and returns repeatedly to the exact Museum object.

An analysis that succeeds technically but not interpretively is an engineering
report. One that succeeds interpretively but cannot distinguish source fact
from metaphor is an essay without sufficient control. The Museum standard
requires both, joined by reproducible evidence and explicit uncertainty.

## 22. Non-claims

This standard does not amend an accession, designate an official
manifestation, grant rights, preserve unretained source, authenticate remote
bytes, establish artist intent from code, rank artworks, or adopt a new Museum
policy. Applying it to an accession creates research and publication inputs;
promotion into the governed corpus requires the existing review and release
controls.

## 23. Working status and related files

This is a working Museum standard defining a reusable research,
interpretation, publication, and conservation method for generative art. It is
not an adopted governance policy, rights grant, accession record, or claim that
any current dossier has passed independent review.

The companion form is
[`templates/generative-system-dossier.md`](../templates/generative-system-dossier.md).
The dated design history and Casey Reas pilot reasoning remain in
[`notes/wip/2026-08-04-generative-systems-analysis-standard.md`](../notes/wip/2026-08-04-generative-systems-analysis-standard.md).
