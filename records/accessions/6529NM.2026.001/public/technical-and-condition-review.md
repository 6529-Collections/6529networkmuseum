# Technical and condition review

**Accession lot:** `6529NM.2026.001`
**Review date:** 2026-08-02
**Scope:** seven Casey REAS Art Blocks works, `6529NM.2026.001.01` through `.07`
**Institutional author:** 6529 Network Museum, Collection Care and Technical Conservation
**Decision authority:** direct Museum-authorized collection authority recorded in `6529NM.2026.001.GAA-01`

## Outcome

The lot passes technical and condition review with conditions. All seven objects are suitable for accession and for noncommercial Museum display through the current official Art Blocks generator routes, provided the display identifies the live network and browser dependencies and carries the approved attribution. No red condition is present. Software preservation remains in progress and is managed as continuing stewardship, not as an unanswered accession review.

## Reviewed findings

| Domain | Rating | Finding |
| --- | --- | --- |
| Token and custody | Green | Contract, token ID, CAIP-19 identity, transfer transaction, block, log, destination, and current custody are verified and mutually joined. |
| Metadata | Green | Exact Art Blocks metadata response bytes are retained with SHA-256 fixity and object-specific source bindings. The live endpoint remains externally operated, but the accession evidence does not depend on its future availability. |
| Script/generator | Amber | All seven official generator URLs were available and produced changing renderable output. The complete assembled generator and project-script byte set has not yet been retained in a self-contained Museum preservation package. |
| Dependencies | Amber | The six `CENTURY`, `Pre-Process`, `Phototaxis`, and `923 EMPTY ROOMS` records identify p5.js 1.0.0 via cdnjs; the `Ex Nihilo (Cosmos)` record identifies p5.js 1.9.0 via cdnjs. A complete dependency lockfile and locally executable dependency bundle are not yet retained. |
| Rendering | Amber | Each official generator rendered successfully in the recorded viewport observation. Browser version, user agent, exact frame timestamps, and a second independent render environment were not fixed. |
| Behavior | Amber | Two successive frames differed for every object, establishing observed live change but not full interaction coverage, timing semantics, or determinism. Documented keyboard controls were not exhaustively exercised. |
| Documentation | Amber | Raw metadata, hashes, dimensions, byte counts, source URLs, object descriptions, and two-frame observations are retained. The previously observed image and screenshot bytes themselves are not in the public repository. Their noncommercial retention is now rights-cleared and is an active preservation action. |
| Preservation | Amber | The content-addressed evidence package, recovery lineage, chain evidence, and collection-wide descriptors are retained. Self-contained generator/dependency capture and two-environment reproducibility remain in progress. |
| Display | Ready with conditions | Current official generators may be used for noncommercial display with CC BY-NC 4.0 attribution, network/browser dependency disclosure, a tested fallback, and monitoring during exhibition. |

These ratings are deliberately asymmetric. Verified object identity and retained metadata fixity are green even though the works are not yet preserved as autonomous executable packages. The generator and render findings are amber, rather than red, because the object-specific official routes were available and produced changing output in the controlled observation. They are not green because that observation does not establish an independently executable Museum copy, complete dependencies, reproducibility across environments, or future-browser behavior. A later failure of the official route before local capture would trigger immediate reassessment and may justify a red rating.

## Object-specific findings

- **CENTURY #31, #724, and #401:** the retained metadata and token identity are complete. The observed route uses p5.js 1.0.0 via cdnjs, and the two-frame checks establish changing live output. For `#31`, the artist-documented `1` and `2` controls were not exercised. All three remain amber for behavior, generator capture, and reproducibility.
- **Pre-Process #63:** the p5.js 1.0.0 official generator rendered and changed across the two observed frames. Before preservation is marked complete, test orientation, restart, mouse and keyboard behavior, frame-rate and duration effects, and whether repeated execution returns to an equivalent initial state.
- **Phototaxis #308:** the p5.js 1.0.0 official generator rendered and changed. Artist-documented controls (`P`, `B`, `1`–`5`, `L`) and the described 1,000-frame stopping behavior were not exercised in the retained observation, so behavior remains amber.
- **923 EMPTY ROOMS #713:** the p5.js 1.0.0 official generator rendered and changed. The accession identity is project-encoded token `1000713`, whose invocation component is `713`; the project record must preserve the distinction between 923 unique room combinations and the 924-token release. Script, shader, controls, and state behavior must be captured before preservation completion. No condition defect is inferred from the identity convention.
- **Ex Nihilo (Cosmos) #248:** the p5.js 1.9.0 official generator rendered and changed. Documented controls (`R`, `G`, `B`, `W`, `S`, `P`, and spacebar) were not exhaustively exercised, and the resulting runtime-state transitions must be characterized. The work is displayable through the current official route with the same network and fallback conditions.

## Display specification

For each exhibition, the Museum must record the date, generator URI, browser and version, operating system, viewport and backing resolution, network requirement, interaction mode, and whether the work is shown live or through a labelled documentation surrogate. Test the exact installation before opening and after material browser, operating-system, generator, or dependency changes. Monitor network-backed live displays and maintain a rights-compliant fallback capture or recording. Do not present a still as the complete software work; label it as a documentation surrogate.

## Active preservation actions

The following actions are approved and required. They are not pending reviews:

1. Retain rights-compliant static and live documentation bytes with fixity and attribution.
2. Capture the exact project scripts, assembled generators, dependency assets, and on-chain inputs for each object.
3. Record a reproducible render environment and verify each object in at least two materially distinct browser/operating-system environments.
4. Exercise and document artist- or platform-described controls, timing behavior, and reset semantics.
5. Assign at least two durable replicas outside the live serving path and run periodic fixity and recovery tests.
6. Reassess after any material contract, metadata, generator, browser, dependency, custody, or display change.

Accession is complete at the reviewed amber condition. `Preservation complete`, `technically verified`, and `display ready` remain later workflow states only when their stricter evidence gates are met.
