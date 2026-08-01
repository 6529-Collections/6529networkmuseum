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
| External media, metadata, RPC or HTTP evidence ingest | `media-external` | provenance capture, token metadata snapshots, preservation media, rarity source datasets |
| 6529Stream-compatible contracts or external-works registry specifications | `stream-contracts` | record registry, signature envelopes, hash commitments, Stream interoperability |
| GitHub Actions, CI, release manifests or deployment controls | `deploy-actions` | validation workflows, deterministic release production, permissions and action pins |
| Subsequent commits responding to review | `followup` | review-fix commits on any pull request |

Review kinds for WCAG, internationalization, backend APIs, databases, Safe writes, signer UX, release deployment, and responsiveness are not enabled because this repository currently has no corresponding product surface. If the repository gains one, the configuration and this matrix must be changed in a reviewed pull request before that specialist is relied upon.

## Pull request procedure

1. Keep the pull request in draft while construction or evidence gathering is incomplete.
2. Stabilize the head commit and run local validation.
3. Request the specialist kinds selected by the matrix. Multiple relevant kinds may be requested in one trusted maintainer comment, for example:

   ```text
   /6529bot review general security stream-contracts privacy-evidence glm-swarm
   ```

4. Request CodeRabbit review when the pull request is ready for external review. The repository ruleset also requests Copilot review.
5. Address all critical and important findings or record a concrete, evidence-backed disposition in the pull request.
6. After any review-fix commit, request `/6529bot followup` against the new head and rerun `Museum validation`.
7. For governed records, obtain a binding review from an identified reviewer who is not the constructor. Bot comments are advisory and cannot satisfy that role.
8. Merge only through the protected pull request path after required checks and review controls pass.

## Current pull request routing

The active build uses this routing:

| Workstream | Review kinds |
|---|---|
| Governance and policy evidence | `general`, `privacy-evidence`, `glm-swarm` |
| Casey Reas research and accession dossier | `general`, `media-external`, `privacy-evidence`, `glm-swarm`; add `security` when executable chain-evidence tooling changes |
| Keys and Gates evidence records | `general`, `media-external`, `privacy-evidence`, `glm-swarm` |
| NextGen-compatible rarity tooling and datasets | `general`, `security`, `media-external`, `privacy-evidence`, `glm-swarm` |
| Documentation control plane and CI | `general`, `security`, `deploy-actions`, `privacy-evidence`, `glm-swarm` |
| On-chain migration specification | `general`, `security`, `stream-contracts`, `privacy-evidence`, `glm-swarm` |
| Templates and standards crosswalk | `general`, `privacy-evidence`, `glm-swarm` |

The routing table is operational memory for the current build, not an accession or governance decision. New work must be classified by changed domain rather than by pull request title alone.
