# Orchestration ledger

This append-oriented log preserves work state across task compaction and agent handoff. It is operational memory, not adopted policy.

## 2026-08-01 — autonomous build opened

### Mandate

Populate the GitHub repository through reviewable pull requests with the Museum mission and governance, adopted decisions, donation and accession policy, approved donation collections, Keys and Gates program/outcomes, the actual seven-work Casey Reas donation accession, transparent NextGen-compatible generative trait analysis, documentation-as-code controls, and the contract specification that will migrate repository records on-chain.

### User-confirmed status

- Keys and Gates works have not been minted.
- Minting may use a separate 6529Stream instance or a subcollection on the main Stream contract; this is TBD.
- The Casey Reas collection has been donated and requires accession documentation.
- The future contract specification must cover migration of the governed GitHub information on-chain.

### Non-negotiable controls

- Do not infer accession from custody or transfer.
- Do not infer acquisition or minting from selection.
- Do not use OpenSea rarity metrics.
- Separate constructor and reviewer roles.
- Preserve primary evidence, observation time, uncertainty, amendments, and deterministic hashes.
- Keep sensitive donor/legal/custody material outside the public repository; publish safe summaries and hashes only.

### Active phase

Phase 1: foundation, governance, decisions, donation policy, and approved-collection register.

### Research tracks launched

Independent parallel tracks cover museum standards, Casey on-chain provenance, Casey art/technical history, NextGen rarity, Keys and Gates evidence, repository/CI architecture, governance evidence, and the external registry. Results are to be written under `notes/research/` and then reviewed before promotion.

The user clarified that Luna work must run as parallel Codex tasks rather than subagents. Seven `gpt-5.6-luna`/`xhigh` worktree tasks were therefore launched:

- Casey token verification: `019fbdd6-6e75-7043-b510-0d6e426b8c2b`
- Casey art/technical research: `019fbdd6-6e75-7043-b510-0d8f523e4493`
- Keys and Gates records: `019fbdd6-8eb7-7663-8f51-2fd0e33e9f6c`
- NextGen rarity tooling: `019fbdd6-9ac1-7e81-b331-310ad99e7c90`
- Documentation control plane: `019fbdd6-ab7a-7470-9c87-5cff139d90a8`
- On-chain migration specification: `019fbdd6-bba5-7470-b827-726e5db08bdb`
- Governance evidence review: `019fbdd6-d7a2-7680-a454-0574d2df96c5`

Terra subagents are reserved for bounded independent review and disjoint sidecar work.

### GitHub control state

- `@6529-Collections/6529seize-maintainers` was granted `maintain` access.
- Repository-wide `CODEOWNERS` and a Museum review template were added.
- Squash-only merges and automatic deletion of merged branches were configured.
- GitHub Free did not expose branch protection/rulesets while this organization repository was private; the initial 403 limitation and intended rules were recorded before visibility changed.

The repository was subsequently made public with owner authorization. Rulesets `20188741`, `20188742`, and `20188743` now enforce maintainer review semantics, no-bypass Museum CI, and Copilot review respectively. The `6529bot` GitHub App installation `140321060` covers all organization repositories; the Museum review profile passed its repository-config and limited-initial readiness validators.

### Known evidence anchors

- Museum Wave: `5f207393-5418-4a75-8738-e40edb44a94d`
- Keys and Gates Wave: `4ff022b3-aa17-4a0a-ba78-58f64ff1d427`
- Museum custody reference: `networkmuseum.6529.eth`
- Casey accession lot: `6529NM.2026.001`
- 6529Stream implementation pin: `5021c8060950c3fef995271e674ed4b2007fee6d`

### Next actions

1. Publish Phase 1 pull request.
2. Reconstruct all sixteen Keys and Gates records as `selected_unminted`.
3. Verify Casey token identities and transfer evidence, then build the actual accession dossier without overstating incomplete gates.
4. Implement schemas, validation, deterministic manifests, and CI.
5. Produce an implementable on-chain migration contract specification and test vectors.

### Completed research sidecars available locally

- `notes/research/museum-standards-crosswalk.md`
- `notes/research/repository-ci-architecture.md`
- `notes/research/nextgen-rarity-method.md`
- `notes/research/casey-reas-art-technical-research.md`
- `notes/research/casey-reas-onchain-evidence.md`
- `notes/research/keys-and-gates-evidence.md`

These are research inputs, not governed records. They require integration review.
