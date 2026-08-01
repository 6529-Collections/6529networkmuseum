# Pull request review policy

Status: active operating control

This policy applies the 6529 review bot to Museum work according to the risks in each pull request. It supplements, and never replaces, the required `Museum validation` check, GitHub rulesets, Code Owners, maintainer approval, and the constructor/reviewer separation required for governed records.

## Baseline review

Every pull request receives these initial 6529bot review kinds from the base-branch configuration:

- `general` for correctness, regressions, and meaningful verification;
- `security` for trust-boundary, injection, cryptographic, and workflow risks;
- `privacy-evidence` for public-record redaction, evidence handling, wallet and transaction facts, and accidental disclosure;
- `glm-swarm` as a bounded advisory second perspective.

The initial set is intentionally limited. Specialist reviewers are requested by a trusted maintainer only when the final diff falls within their domain.

## Specialist routing matrix

| Changed domain | Additional review kinds | Typical Museum work |
|---|---|---|
| Executable external-media, metadata, RPC or HTTP ingest | `media-external` | fetchers, safe-fetch boundaries, media parsers, snapshot importers; not evidence or accession prose alone |
| Normative contract surfaces intentionally equivalent to 6529Stream | `stream-contracts` | Solidity, ABI, EIP-712, contract invariants and executable contract test vectors; not high-level registry prose alone |
| GitHub Actions, CI, release manifests or deployment controls | `deploy-actions` | validation workflows, deterministic release production, permissions and action pins |
| Subsequent commits responding to review | `followup` | automatically enqueued on synchronize events; use a maintainer command only if the expected run was skipped or unavailable |

Review kinds for WCAG, internationalization, backend APIs, databases, Safe writes, signer UX, release deployment, and responsiveness are not enabled because this repository currently has no corresponding product surface. If the repository gains one, the configuration and this matrix must be changed in a reviewed pull request before that specialist is relied upon.

## Pull request procedure

1. Keep the pull request in draft while construction or evidence gathering is incomplete.
2. Stabilize the head commit and run local validation.
3. Request the specialist kinds selected by the matrix. The four automatic baseline jobs already cover general, security, privacy/evidence, and advisory review; do not repeat them in the specialist command. Keep each trusted maintainer request within the four-job delivery cap, for example:

   ```text
   /6529bot stream-contracts
   ```

4. Request CodeRabbit review when the pull request is ready for external review. The repository ruleset also requests Copilot review.
5. Address all critical and important findings or record a concrete, evidence-backed disposition in the pull request.
6. After any review-fix commit, rerun `Museum validation` and wait for the configured automatic `followup` review against the new head. Request `/6529bot followup` manually only when the expected automatic run was skipped or unavailable.
7. For governed records, obtain a binding review from an identified reviewer who is not the constructor. Bot comments are advisory and cannot satisfy that role.
8. Merge only through the protected pull request path after required checks and review controls pass.

## Current pull request routing

The active build uses this routing:

| Workstream | Additional specialist review kinds beyond the automatic baseline |
|---|---|
| Governance and policy evidence | none |
| Casey Reas research and accession dossier | `media-external` only if executable chain/media/metadata ingest changes |
| Keys and Gates evidence records | `media-external` only if executable ingest changes |
| NextGen-compatible rarity tooling and datasets | `media-external` when a fetcher, importer, parser, or external snapshot pipeline changes |
| Documentation control plane and CI | `deploy-actions` |
| On-chain migration specification | `stream-contracts` only for normative ABI, EIP-712, invariant, Solidity, or contract-vector changes intentionally equivalent to 6529Stream |
| Templates and standards crosswalk | none |

The routing table is operational memory for the current build, not an accession or governance decision. New work must be classified by changed domain rather than by pull request title alone.
