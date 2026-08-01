# Technical and condition report

Status: draft working template. Complete per object, or explicitly identify a shared report and its object-specific exceptions.

## Examination envelope

- Report ID: `6529NM.<object-id>-TECH01`
- Record-control block: `[instantiate exactly from record-control.md]`
- Object ID / lot ID: `[...]`
- Examiner / independent reviewer: `[...]`
- Examination date/time (UTC): `[...]`
- Record version / supersedes: `[...]`
- Trigger: `[intake | accession | pre-display | post-incident | periodic review | migration | other]`
- Evidence class: `C` for Museum-generated technical observations

## State and scope

- Object state at examination: `[...]`
- Native token/contract inspected: `[yes/no/not_applicable]`
- Metadata endpoint(s) inspected: `[...]`
- Source bytes/code inspected: `[yes/no/partial/not_applicable]`
- Dependencies inspected: `[yes/no/partial/not_applicable]`
- Live rendering inspected: `[yes/no/partial/not_applicable]`
- Behavior/interaction inspected: `[yes/no/partial/not_applicable]`
- Scope limitations: `[...]`

## Integrity and fixity

| Component | Retrieval source | Hash algorithm/digest | Retrieved at | Fixity result | Notes |
|---|---|---|---|---|---|
| Token metadata | `[...]` | `[...]` | `[...]` | `[pass/fail/not_tested]` | `[...]` |
| Artwork/media bytes | `[...]` | `[...]` | `[...]` | `[pass/fail/not_tested]` | `[...]` |
| Script/code | `[...]` | `[...]` | `[...]` | `[pass/fail/not_tested]` | `[...]` |
| Dependency lockfile/list | `[...]` | `[...]` | `[...]` | `[pass/fail/not_tested]` | `[...]` |
| Reference capture | `[...]` | `[...]` | `[...]` | `[pass/fail/not_tested]` | `[...]` |
| IIIF/C2PA/BagIt/OCFL metadata | `[...]` | `[...]` | `[...]` | `[pass/fail/not_tested]` | `[...]` |

State what the hash proves and what it does not prove. A matching hash proves byte equality for the tested input; it does not by itself prove authorship, title, rights, or behavioral equivalence.

## Runtime and significant properties

- Operating system/version: `[...]`
- Browser/runtime/version: `[...]`
- Hardware/GPU/display/audio: `[...]`
- Network/RPC/oracle/data services: `[...]`
- Time zone/clock/timing inputs: `[...]`
- Fonts, codecs, libraries, and external dependencies: `[...]`
- Seed/hash/randomness and determinism: `[...]`
- Significant visual properties: `[...]`
- Significant temporal/behavioral properties: `[...]`
- Interaction/accessibility properties: `[...]`
- Known variance or non-determinism: `[...]`

## Rendering and behavior tests

| Test ID | Protocol state/inputs | Environment | Expected significant property | Observed outcome | Capture/hash | Result |
|---|---|---|---|---|---|---|
| `[...]` | `[...]` | `[...]` | `[...]` | `[...]` | `[...]` | `[pass/partial/fail/not_tested]` |

## Mutability and failure analysis

- Smart-contract administrative controls: `[...]`
- Metadata/media mutability: `[...]`
- Upgrade/proxy/dependency risk: `[...]`
- Domain/hosting/RPC/storage dependency: `[...]`
- Revocation, takedown, or license risk: `[...]`
- Failure modes and user-visible effect: `[...]`
- Recovery lineage or known prior changes: `[...]`
- Mitigation and next review: `[...]`

## Condition classification

- `green`: independently retrievable and verified for the assessed scope.
- `amber`: functional, but dependent on vulnerable infrastructure, incomplete evidence, or a documented variance.
- `red`: a material component is unavailable, corrupted, materially changed, or behavior cannot be reproduced for the assessed claim.
- `not_assessed`: no technical condition claim has been made.

| Component | Status | Basis/evidence | Impact on accession or display |
|---|---|---|---|
| Token/contract | `[green/amber/red/not_assessed]` | `[...]` | `[...]` |
| Metadata | `[green/amber/red/not_assessed]` | `[...]` | `[...]` |
| Media/bytes | `[green/amber/red/not_assessed]` | `[...]` | `[...]` |
| Script/dependencies | `[green/amber/red/not_assessed]` | `[...]` | `[...]` |
| Rendering/behavior | `[green/amber/red/not_assessed]` | `[...]` | `[...]` |
| Documentation/fixity | `[green/amber/red/not_assessed]` | `[...]` | `[...]` |

## Technical recommendation

- Technical gate: `[pass | pass_with_conditions | fail | deferred]`
- Display gate: `[ready | ready_with_conditions | not_ready | not_applicable]`
- Preservation actions required before completion: `[...]`
- Conditions, owner, due date: `[...]`

## Attestation

I attest that this report states the test protocol, evidence, limitations, and observed outcome without treating a documentation copy as the tokenized artwork.

- Constructor/examiner: `[...]`
- Date/version: `[...]`
- Independent technical reviewer: `[...]`
- Review date: `[...]`
- Signature/hash reference: `[...]`
