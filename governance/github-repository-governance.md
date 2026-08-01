# GitHub repository governance

Record ID: `6529NM-OPS-GH-001`
Status: active operating control
Observed/configured: 2026-08-01 UTC

## Policy

All changes to the default branch are made through pull requests and are subject to repository CI.

- Members of `@6529-Collections/6529seize-maintainers` are the Museum repository maintainers.
- A maintainer may authorize and merge a pull request after required CI succeeds.
- A pull request by anyone outside the maintainer team requires at least one approving review from a maintainer and successful CI before merge.
- A maintainer-authored pull request may be merged by a maintainer after successful CI; high-risk governed-record and release changes still use the constructor/reviewer separation defined in the record standards.
- Approval applies to the reviewed commit. Material changes after approval require review again.
- Administrators follow the same process except for a documented emergency intervention.

Repository-wide ownership is declared in `.github/CODEOWNERS`.

Every pull request opened by a trusted maintainer is enrolled in the repository-aware `6529bot` review profile at `.github/6529bot.yml`. Initial review fans out to general, security, external-media, Stream-contract, privacy/evidence, and advisory GLM-swarm review; subsequent commits receive follow-up review. Untrusted public contributors cannot consume model budget automatically; a maintainer triggers the same review before approval. The configuration contains budget ceilings and no secrets. GitHub Copilot review is requested independently through a repository ruleset on every draft and non-draft pull request.

## Configured access

The existing organization team `6529seize-maintainers` has `maintain` access to `6529-Collections/6529networkmuseum`. This permits team members to manage pull requests and merge eligible changes without granting repository administration.

Repository merge settings are configured for squash merge only, with merged branches deleted automatically. Merge commits and rebase merges are disabled. GitHub reported auto-merge as unavailable under the current configuration.

Team membership remains governed in GitHub. The repository does not duplicate the member roster as authority.

## Enforcement availability

Before public authorization, the repository was private and the `6529-Collections` organization was on GitHub Free. GitHub returned HTTP 403 for both branch protection and repository rulesets with the message that the repository must become public or the organization must upgrade. The repository owner subsequently authorized public visibility on the condition that the maintainer rule be activated. The repository is now public and the rules described below are active.

The following repository rulesets are active:

- `20188741` — `main maintainer review and merge policy`: pull request, one approval by the maintainer team for outside contributors, stale-review dismissal, latest-push approval, conversation resolution, squash merge, update-only, no deletion, and no non-fast-forward update. The maintainer team has `pull_request` bypass mode, so a maintainer can authorize and merge a maintainer PR without an unnecessary second maintainer while still using a PR.
- `20188742` — `Museum mandatory CI`: the `Museum validation` GitHub Actions check is required and current for every default-branch merge, with no bypass actor.
- `20188743` — `Museum Copilot review`: automatic review on every push, including draft pull requests, with no bypass actor.

The active settings implement:

1. require a pull request before merging;
2. require one approval;
3. require code-owner review for outside contributors;
4. dismiss stale approvals when new commits are pushed;
5. require approval of the latest reviewable push;
6. require all Museum validation and manifest checks;
7. require conversation resolution;
8. block force pushes and deletion;
9. do not permit a CI bypass, including by maintainers;
10. allow merge by squash only, unless preservation of a reviewed multi-commit history is specifically required.

The live rulesets must be reverified after material GitHub policy, team, visibility, or plan changes.
