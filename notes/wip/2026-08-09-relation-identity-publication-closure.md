# Relation identity publication closure

Status: candidate A4 under qualification; reviewed projection and replacement catalog activation pending

## Finding

Publication-catalog candidate `9635ffabb20198a252a1501ccfb57de92c87b401`
correctly bound canonical reviewed projection B3
`bf517353ef861e91f5137908daca514b81578b4d`, all 205 active relation records,
and the rest of the closed visitor corpus. Independent frontend-contract
review nevertheless rejected activation before merge. The catalog did not
include `schemas/public-relation-identity-inventory.json` or its governing
schema in its atomic assembly set.

The omitted inventory is part of the public relation contract. It binds every
active semantic relation key to its stable `6529NM-REL-*` identity and retains
six retired identity tombstones, `6529NM-REL-0159` through
`6529NM-REL-0164`. Current relation records alone cannot prove that an ID was
not reused, that a retired ID remains unavailable, or that a qualifier change
preserved semantic identity. Fetching this control outside the catalog would
weaken the closed-publication guarantee.

PR #46 was therefore closed without merge. No publication catalog or pointer
was activated on canonical `main`.

## Correction

The deterministic publication-inventory generator now treats the complete
frontend graph-validation contract as atomic assembly controls: the controlled
vocabularies, entity-identity inventory, relation-identity inventory, and route
compatibility map, together with each governing schema and the complete schema
dependency chain for entity, relation, lifecycle-observation, and envelope
records. The visitor publication inventory, visitor bundle, and release
manifest are regenerated from that closed set. Tests require the eighteen
graph and release controls plus every record schema declared by the controlled
vocabulary and their complete local `$ref` dependency closure in the inventory
and bundle, alongside the active bindings and retired tombstones.

Candidate A4's regenerated publication inventory contains 547 entries: 546
atomic assembly documents and one approved public media asset. Its 122 assembly
controls include the eighteen closed graph and release-validation files and all
seventeen record schemas declared by the controlled vocabulary; three of those
schemas are already among the eighteen controls. Recursive `$ref` closure adds
the transaction-provenance schema required by the accession-lot schema. The
visitor bundle contains all 546 assembly documents and remains below the
governed eight-megabyte ceiling.

Because the publication source commitments change, the correction follows the
same constructor/reviewer boundary as the prior identity fix:

1. candidate A4 contains the complete review-pending graph and corrected
   publication controls;
2. independent review produces direct child B4 by changing only governed
   review fields and deterministic generated commitments;
3. a new immutable publication catalog and pointer may bind only canonical
   B4;
4. the strict frontend may activate only that verified catalog, atomically.

The rejected catalog bytes remain on their unmerged branch as audit evidence;
they are not an active or canonical release.
