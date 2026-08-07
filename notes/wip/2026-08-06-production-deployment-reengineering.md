# Production deployment reengineering

Status: completed engineering and release ledger; ongoing measurement follow-up

This note preserves the cross-repository deployment work that affects the
Museum's release path. It is an engineering record, not Museum policy and not
evidence that a rollout completed.

## Objective

Replace timed drain checks and manually coordinated frontend/backend production
mutations with one backend-owned production authority. Preserve exact source,
artifact, selection, qualification, and terminal evidence while shortening
human idle time and making independent work parallel where mutation safety does
not require serialization.

## Architecture under review

- The backend persists one shared production lease for frontend and backend.
- The first trusted workflow job acquires and binds the lease to repository,
  service, target SHA, run ID, attempt, operator, and control epoch.
- Frontend artifact construction has no deployment or AWS authority. A separate
  verifier checks the exact archive and selection before the deployer receives
  cloud credentials.
- Reauthorization occurs immediately before AWS mutation and freezes the exact
  selection digest.
- Frontend retains authority through the exact automatic Production E2E run;
  backend retains authority through exact service-deployment completion.
- Terminal callbacks are evidence-bound and idempotent. Exact persisted terminal
  results can be replayed even when GitHub is temporarily unavailable.
- Automatic E2E dispatch is serialized per deploy, reuses one exact run, and
  reconciles an ambiguous dispatch response. The terminal listener accepts only
  the canonical lowest exact run ID and ignores duplicates.

## Review findings incorporated

Independent reviews found and closed these pre-release defects:

1. frontend and backend workflow titles initially disagreed with the API;
2. successful frontend deployment completion initially attempted a failure
   callback instead of retaining authority for E2E;
3. failure selection evidence could be inferred from artifact presence before
   reauthorization;
4. exact terminal retries still depended on a fresh GitHub read;
5. backend failure evidence was captured before a later failure-capable
   notification;
6. terminal callbacks had no bounded transport retry;
7. ambiguous reauthorization could commit server-side while leaving the
   listener unable to release the authority;
8. an automatic E2E retry could create competing terminal qualifiers.

## Pull requests and merged exact heads

- merged backend authority API PR
  [#1908](https://github.com/6529-Collections/6529seize-backend/pull/1908):
  `8c9aae033b145d44811f1446ae5585b10a2fe78f`;
- merged backend workflow consumer PR
  [#1909](https://github.com/6529-Collections/6529seize-backend/pull/1909):
  `503007e116b6bf4dcfa1e70c1b84cc86696271b6`;
- merged frontend one-click controller PR
  [#3665](https://github.com/6529-Collections/6529seize-frontend/pull/3665):
  `8822d801ba0331ab74dae704ab9948c831c66f66`.

The production authority schema and API prerequisite are live. Production
`dbMigrationsLoop` run `31154178331` completed in 2 minutes 50 seconds, followed
by production API run `31154484782`. The public API health route returns 200;
unauthenticated requests to both authority acquisition routes return 401. The
new authority table is empty of active operations, and Release Bus remains
disabled. Workflow consumers remain unmerged pending their own exact-head
review and CI; the prerequisite no longer blocks them.

## Validation at this checkpoint

- authority API and route tests: 162/162;
- independent exact-head authority API re-review: no findings;
- backend workflow contract: 8/8, generated parity, actionlint, formatting;
- independent exact-head backend workflow re-review: no findings;
- frontend release-contract suites: 132/132;
- frontend authority callback retry contract: 14/14;
- frontend changed lint and 1,410-file changed typecheck: pass;
- backend and frontend OpenAPI sources: byte-identical;
- frontend workflow actionlint and deterministic generation: pass.

GitHub Actions entered an official major partial outage on 2026-08-06 and
returned to all-systems-operational status at 05:49 UTC on 2026-08-07. Outage
time is excluded from process timing. The held hotfix staging workflow resumed
at 05:50:25 UTC. Exact staging deployment and HTTP-version verification
completed at 05:59:36 UTC: 9 minutes 11 seconds. Automatic staging E2E and an
independent exact production-artifact build then started in parallel.

Recovered hosted CI exposed two additional exact-head defects. Backend PR
#1908 had not committed the generated OpenAPI authority models; the 13-file
deterministic generator output is now committed, with 162/162 focused tests and
TypeScript validation green locally. Frontend PR #3665's secret scanner allowed
generic whitespace to cross YAML newlines, causing a false positive on reusable
workflow secret declarations. Its assignment syntax now permits horizontal
whitespace only. CodeQL also found a path check/read race in the authority JSON
client; the client now opens one descriptor, verifies that descriptor, and
performs a byte-capped read through the same descriptor. The two focused suites
pass 88/88 with lint and changed typecheck green.

Subsequent exact-head validation closed the remaining integration findings.
Backend consumer PR #1909 is rebased on the live API merge and has no unresolved
review threads. Frontend controller PR #3665 passes 105 focused release tests,
the complete Jest/Playwright type ratchet, changed lint and changed typecheck.
Its one-click scripts are explicit Knip workflow entry points. Ten static-review
comments against generator-owned `HttpFile` imports were resolved with a
recorded generator-boundary disposition: the deterministic OpenAPI generator
erases those imports, so direct edits to generated output would be reverted and
would violate generated parity.

The first hosted full run on rebased backend PR #1909 passed 802 of 803 tests.
Its sole failure proved that the authority API merge advanced the protected
backend PR-policy bundle while the stacked consumer still pinned the preceding
digest. Exact head `49d0781e5e6e6d0296ec5bfa0c140241f73f79bc`
adds the explicit old-to-new trusted digest transition and updates the rollout
contract. It changes no lease or deployment behavior. Local lint, formatting
and diff checks pass; the policy reader intentionally rejects Windows because
Windows lacks the required `O_NOFOLLOW`, so the fresh hosted Linux full suite
is authoritative.

Exact frontend main `288653ac1ca1e6ce0ce62f5e11e784d090b3c693`
was composed for staging as `8718d8d415e2c6671fa6b5dc44e8a696235d8a83`.
Staging deploy run `31154124464` completed exact deployment and HTTP-version
proof in 8 minutes 45 seconds. Production artifact run `31153821324` completed
in parallel while automatic staging E2E run `31154708563` qualified the staged
runtime. The production mutation remains held until that automatic staging E2E
is terminal-success and the protected-main source is rechecked.

Automatic staging E2E run `31154708563` subsequently completed successfully.
Legacy production run `31155672123` was dispatched for the same exact main and
refused readiness with HTTP 409 on attempts 1 and 2 before the AWS job. Public
state reconstruction showed the production lane OFF/changeable, the production
lock unowned, no active production train, no nonterminal production operation,
and no competing frontend/backend production workflow. Because the legacy
fallback suppresses the conflict body, repeated retries would not produce new
evidence. That path is abandoned in favour of the reviewed transactional
consumer/controller rollout; production remains unchanged.

This incident also clarified the collaboration boundary. The legacy manual
guard requires `source_sha` to equal the moving `main` tip. The replacement
freezes one protected-main ancestor and binds the operation, lease, artifact,
selection, deployment and E2E to it; later main movement is permitted. The Dev
Team was told that the earlier merge hold applied only to the legacy fallback
and is no longer requested.

Final review produced substantive improvements rather than a bypass. Backend
PR #1909 removed an authority-state write that occurred before response
validation and corrected two invalid `actions/download-artifact` pins. Its
focused regression suite now proves response validation precedes the only state
write and binds the verified v7.0.0 action commit. The resulting protected
policy bytes advanced once more; exact head
`519ff71468966c8fb8adebfae79ee722b5cf930e` records the explicit
`18862aeb...` to `528692ae...` rollout. Final full Linux run `31158739110`
completed successfully in 13 minutes 38 seconds: 803/803 tests, generated
parity, lint and formatting, both builds, and immutable merge-tree evidence.
PR #1909 then merged as exact backend main
`503007e116b6bf4dcfa1e70c1b84cc86696271b6` at 07:57:04 UTC.

Frontend review found that rerun extraction roots were not explicitly cleaned.
Exact head `e2e31e84106a7bff2a51f759933ed96722ca842e` removed both roots
before extraction and added ordering assertions. A subsequent bundled
hardening pass removed the verifier's run-ID concurrency fallback, opened every
trusted artifact file through a descriptor bound to its directory entry,
rechecked the descriptor snapshot after reading, and documented the narrower
controller-minted operation-ID grammar. Exact head
`d48be644be91478113a15747b409c4d0e2606d9f` adds a Linux adversarial
replacement test and is the only frontend head now qualifying; the superseded
hosted run was cancelled to release runner capacity. Exact-head App PR CI run
`31159202747` completed successfully, including the protected Network Museum
browser pack, which itself ran for 24 minutes 25 seconds. All review threads
were resolved and the final 6529bot verdict was "No new findings." The Public
Review Snapshot Trust sentinel failed only because the PR intentionally changed
protected trust root `ops/scripts/testing-strategy.cjs`; the maintainer
disposition records that exact boundary without weakening the sentinel. Sonar's
quality gate passed; its remaining S5843 regex-complexity code smell is tracked
as focused follow-up debt rather than a release defect. PR #3665 merged as exact
frontend main `8822d801ba0331ab74dae704ab9948c831c66f66` at 08:20:10 UTC.

The exact merged frontend main was composed into `1a-staging` as signed merge
`67113a5d2fe4220abcb0cedd1ee806ec6a83632c`. Automatic staging deploy run
`31161291400` ran from 08:20:32 to 08:30:03 UTC and completed successfully:
7 minutes 49 seconds for the exact build/package job, 1 minute 23 seconds for
deployment and HTTP-version proof, and 9 minutes 31 seconds end to end including
workflow transitions. Dispatch run `31161951379` then selected exact main
`8822d801ba0331ab74dae704ab9948c831c66f66` and started automatic Staging E2E
run `31161969382`. That run completed successfully at 08:46:38 UTC: the browser
pack ran for 15 minutes 56 seconds and the workflow envelope for 16 minutes 19
seconds, including exact manifest-bound evidence validation.

At 08:47:13 UTC the production preflight proved that protected main remained
exactly `8822d801ba0331ab74dae704ab9948c831c66f66`, the exact automatic Staging
E2E was terminal-success, the production control was OFF/changeable under the
recorded owner-approved fallback, and no competing frontend or backend
production actor was active. The one-click production controller was dispatched
at 08:47:28 UTC as run `31163167029`, operation
`frontend-prod-31163167029`, bound to that exact SHA. Production remained on
`ee156caa5b2a9ed2efaee34659f098e916badcb9` at dispatch. The operation failed
closed during authority acquisition with HTTP 409
`WORKFLOW_IDENTITY_MISMATCH`, before artifact resolution, AWS credentials, or
mutation. Production therefore remained unchanged.

The live GitHub Actions payload identified the integration defect. For a
workflow that defines `run-name`, the Actions run API returns the evaluated
run-name in both `name` and `display_title`; it does not preserve the static
workflow title in `name`. The authority verifier required both the exact
workflow path and the impossible static-name comparison. All other live
identity fields matched, and `punk6529` was an active maintainer in the
`release-bus-operators` team. Backend hotfix PR
[#1910](https://github.com/6529-Collections/6529seize-backend/pull/1910), exact
head `4aa5da8a6147d34e2b40e33c06cbebfc3e2179ab`, removes only the four
redundant checks against the overloaded `name` field. Exact path, evaluated
operation-bound title, repository/head repository, protected branch/SHA,
event, status/conclusion/attempt and approved-operator checks remain. Fixtures
now model the live API shape. Local authority tests pass 36/36; focused lint,
format, full TypeScript and diff checks pass. Hosted review and CI are active.

The initial two-file head completed hosted backend/API build, Sonar, Snyk,
DCO, CodeRabbit and the 6529bot review lanes successfully. A pre-merge
self-deployment audit then found that the normal production reauthorization
and authority-evidence steps would still call or depend on the incompatible
live verifier. The follow-up keeps one narrow break-glass route: API/prod only,
exact protected-main SHA, allowlisted actor, explicit reason, no operation key,
and only HTTP 409 `WORKFLOW_IDENTITY_MISMATCH`. It runs the complete
lane/lock/train/GitHub-actor readiness guard at authorization and again
immediately before AWS credentials. The second execution is SHA-256-bound to
the first step's guard bytes, captures one copy before validation, and executes
under an empty environment, fixed system path and non-profile Bash. Normal
reauthorization and evidence remain mandatory outside this fallback; the
fallback writes its own exact-SHA, package-digest and guard-digest evidence
artifact with 30-day retention.

Final signed hotfix head
`feadf29a3ceaf3ef992bb03a7487726583809d61` also makes the workflow-name
contract explicit in tests. Frontend and backend authorization plus successful
and failed Production E2E qualification accept stale static `name` values only
when immutable workflow path and evaluated operation-bound title are exact.
Local evidence is 37/37 authority tests, 8/8 generated-workflow tests, three
emergency invariants, deterministic generation, focused format/lint, full root
TypeScript and diff validation. The non-secret repository variable
`EMERGENCY_API_BOOTSTRAP_ACTORS` was created as the minimal JSON allowlist
containing the existing default operator `prxt6529` and current admin operator
`punk6529`; all remaining emergency predicates are enforced in workflow code.
Fresh exact-head hosted CI and review are active. Production is unchanged.

A final dispatch audit found that the emergency branch did not inherit the
normal operation-key-only remote checks. Exact signed head
`d414d46a79c21a891925c67f131e1d83873cbc5f` extends those existing checks to
the emergency fallback: AWS `CodeSha256` for Lambda `seizeAPI` must match the
built ZIP, and `https://api.6529.io/health` must report `status=ok` plus the
exact merged backend SHA before emergency evidence is created. Focused
generated-workflow tests and the format/lint/type/diff gates pass. Exact-head
hosted run `31167106109` is authoritative; superseded CI was cancelled.

Run `31167106109` passed 804 of 805 tests. Its only failure was the deliberate
protected policy-bundle digest change caused by the reviewed workflow bytes:
expected `528692aee7457217f9956e950497a9abbd0b5eb317a7a899ce8fb04c0b73ff36`,
observed `3403deda84646791436614ab775fd32c5edf2b5e50935166c0b1f864085d5991`.
Signed head `049e7a74abfd4cf4a90b7fb4e922f6fa5b81f262` appends that exact old-to-new
transition to the GitHub App trust graph and advances the rollout-contract
constant. It changes no workflow or runtime behavior. Fresh hosted run
`31167781182` is authoritative.

Run `31167781182` then passed every shard except one stale broad-contract
assertion that still required the removed legacy error text. The affected
shard passed 861 of 862 tests. Signed head
`37ba7ea661c6324e48e9aa77f4179ae93db3609d` requires structured
`WORKFLOW_IDENTITY_MISMATCH` and explicitly rejects the legacy string. Because
that assertion file is policy-covered, a direct Linux computation produced
final digest `b8ef9667450785970266a71869d585b585a2f9ef99a8ca4382d310cf1fde7c6a`;
the trust graph now records exact transition `3403deda...` to `b8ef9667...`.
Direct Linux checks verified workflow blob `af4314e0...`, the final digest and
both rollout endpoints before push. Fresh hosted run `31169396368` was started.

Exact-head Sonar then failed its quality gate at 3.5-percent duplication on
new code against a 3-percent ceiling. The duplicate was the sanitized
environment block at both emergency-guard executions. The first execution is
before checkout or dependency code; the second is after untrusted build steps
and immediately before credentials. Signed head
`59c29d461412382777dc1f4677bb01039e6255fc` executes the first captured guard
under non-profile Bash and retains SHA binding, `env -i`, fixed system path and
single-copy execution for the second. Linux precomputation produced final
policy digest `071e4facda889950c1460d9eaf44fec0f6934655c327948b5fa01d3ec476231c`
and verified trust edge `b8ef9667...` to `071e4fac...`. Fresh hosted run
`31169902387` is authoritative. The Dev Team forecast was revised to
11:15–11:35 UTC because the valid Sonar round consumed the prior contingency.

Run `31169902387` was cancelled after Sonar identified the remaining duplicate
new-code block. The duplicated lines were not the two guard invocations: the
first refactor had already reduced both workflow files to zero duplicated new
lines. The remaining block was the three adjacent, explicit trust-rollout
entries in `release-bus-v2.github-app.ts`. Signed head
`d17d1c56ae1c9e651185143b76de3dfcf4d2ea5c` replaces those repetitions with
one typed rollout-chain helper. The accepted sequence remains exactly
`528692ae...` to `3403deda...` to `b8ef9667...` to `071e4fac...`; no trust edge
or expiry changed. Prettier, ESLint, full TypeScript, whitespace and 53
substantive focused assertions pass locally. The two additional policy-reader
assertions fail closed on Windows because that platform cannot supply
`O_NOFOLLOW`, as designed. An independent Linux/Docker policy-bundle build
reproduced digest `071e4facda889950c1460d9eaf44fec0f6934655c327948b5fa01d3ec476231c`.
Fresh exact-head hosted CI and 6529bot general, security, deploy-actions and
auth-api review lanes are authoritative. The Dev Team Wave received this exact
state at drop `1279526`; frontend main merges remain unblocked and only an
active production mutation is serialized.

Exact-head hosted run `31170651649` completed successfully in 15 minutes 39
seconds: 805/805 tests, deterministic generation, lint and formatting,
backend/API builds, and immutable merge-tree evidence. Sonar reported zero new
issues; Snyk, DCO and CodeRabbit were green; the exact-head 6529bot follow-up
reported no new findings and its full-stack review said "Good to merge." The
single inline review thread was resolved. PR #1910 merged under the recorded
controlled approval disposition as exact backend main
`6d4f09928f4cc8daee66c5c9e620db443e0c55bd` at 10:51:45 UTC.

Emergency API bootstrap run `31171791924` was dispatched after exact-main,
actor-allowlist and zero-active-production-actor readback. It failed closed in
15 seconds during its first authorization/readiness step, before checkout,
dependencies, credentials or AWS. The live server returned the expected 409
`WORKFLOW_IDENTITY_MISMATCH`, so the compatibility fallback activated. Its own
local guard then repeated the same impossible static-name assumption, requiring
`Deploy api to prod [manual]`. GitHub's live run payload instead contained the
evaluated, operation-bound run name in both `name` and `display_title`:
`Deploy api to prod [backend-prod-api-31171791924]`. Every other retained live
identity field matched. Production remained on healthy API SHA
`8c9aae033b145d44811f1446ae5585b10a2fe78f`.

Backend correction PR #1911, exact signed head
`9a9bbc3f321b6d68b51c026942cb48060de76533`, binds both guard fields to
`Deploy api to prod [backend-prod-api-${GITHUB_RUN_ID}]`. Exact run ID and
attempt, actor, workflow path, event, in-progress state, protected main
branch/SHA, controls, trains, lock state, workflow existence and active-run
checks remain. Generated-workflow regressions reject the stale static title.
Deterministic generation, the 8/8 authority integration suite, Prettier,
ESLint, full TypeScript and whitespace pass; live failed-run readback proves
the new title predicate; Linux/Docker rebuilt protected policy digest
`7ad7d9d8698d8adfe41ddca2d926d2a60af96e78e6b5ad10b00e13a583f4be4a`
and the trust graph records transition `071e4fac...` to `7ad7d9d8...`. Hosted
CI and bot review are authoritative before merge or retry.

Review of the initial #1911 head correctly identified a maintainability risk:
it independently shell-expanded a hardcoded `api` title. Signed follow-up head
`10fac20dadc48a1054c883979ae1401580ffffbc` passes the already validated
service and numeric run ID separately to `jq`, constructs the expected title
once inside `jq`, and requires `display_title == name`. It therefore has no
independent title argument and no hardcoded service segment. Emergency dispatch
remains separately restricted to service `api`. Live run `31171791924` proves
the resulting title character-for-character. Generated-workflow regressions,
the 8/8 authority integration suite, formatting, lint, full TypeScript and
whitespace pass. Linux/Docker rebuilt final protected policy digest
`4186f8f83b5c29af0ca3194a0dc2e18a72e2fa29b459acfc006725385254f551`;
the trust graph records exact transition `7ad7d9d8...` to `4186f8f8...`.
Superseded CI was cancelled and exact-head run `31172413335` is authoritative.

Run `31172413335` completed successfully in 15 minutes 20 seconds: 805/805
tests, deterministic generation, lint and formatting, backend/API builds and
immutable merge-tree evidence. Sonar reported zero new issues; Snyk, DCO and
the exact-head 6529bot review lanes were green, with no unresolved review
threads. PR #1911 merged under the recorded controlled approval disposition as
exact backend main `019f1e1f511bb926ab928fb02b9de4df9bceb093` at 11:18:28
UTC.

Emergency API bootstrap run `31173569521` then passed the corrected first
authority/readiness boundary, exact checkout and source verification, all
dependency installations and both builds. It failed closed in 7 seconds at the
second clean-environment guard, before AWS credentials, with
`INPUT_SERVICE: unbound variable`. The saved guard uses `INPUT_SERVICE` to bind
the evaluated GitHub run title, but the explicit `env -i` allowlist had omitted
that already validated non-secret value. No production mutation occurred; the
API remained on healthy SHA `8c9aae033b145d44811f1446ae5585b10a2fe78f`.

Backend correction PR #1912, exact signed head
`c2e32cd59525ac2d0581697484d37cbee96f11e2`, forwards only
`INPUT_SERVICE="$INPUT_SERVICE"` into the second guard. It changes no predicate,
secret, credential boundary or production authority. Both the critical-path
and production-authority suites now assert that the clean environment contains
the required input. Local evidence is 8/8 authority tests, the exact structural
regression, Prettier, ESLint, full TypeScript and whitespace. An independent
Linux/Docker exact-commit build reproduced protected policy digest
`2fdd612fba4a2490f06108dc2c5ed69574277de200e8b1a03fc104b0bb7a66c9`;
the trust graph records exact transition `4186f8f8...` to `2fdd612f...`.
Exact-head 6529bot reviews report Good to merge and no security, deployment,
auth/API, DB/Lambda or media findings. Hosted run `31174341951` is authoritative.

## Timing contract

The retained performance contract separates observed releases from a synthetic
critical-path model. The comparable observed baseline is 46.983 minutes. The
current serialized design forecasts 29/56/72 minutes best/median/conservative
p95. A future path with true production-artifact overlap forecasts 21/42/58
minutes. These are planning estimates, not an SLA; no 25-percent claim is valid
until artifact overlap is actually implemented and measured.

## Remaining release gates

1. merge backend correction PR #1912 under full review and deploy the API;
2. rerun the timed one-click production operation and its exact automatic
   Production E2E using retained evidence;
3. append actual timing and outage-excluded timing here and publish the same
   closeout to the Dev Team Wave as `punk6529bot`.

## Authority rollout and frontend recovery, 2026-08-07

Backend PR #1912 merged as exact main
`365f4fb9484948a82c951413b53cac8fd41a2b03`. Exact-head CI run
`31174341951` passed in 16 minutes 41 seconds with 805/805 tests and all
required review and analysis lanes green. Emergency API bootstrap run
`31175510742` then succeeded in 2 minutes 54 seconds. Three consecutive public
health reads bound the live API to the exact commit with healthy database and
Redis status. The retained deployment-evidence artifact has SHA-256
`c5f9f7b514bb93ab2636a71e9b542659167036ab5052e79798a9325441b4db0c`.

Frontend one-click retry `31175798509` acquired the new authority and launched
an operation-bound builder. Child run `31175824671` completed in 10 minutes 32
seconds and produced artifact `8993027703`, 119,397,503 bytes, with API digest
`sha256:c7c106f88f98b51ec61a0aa10e3d543001816891b06383c53c4704f4f13d5c41`.
The isolated verifier child `31176562035` failed in 18 seconds before artifact
download or production mutation because its immutable sparse checkout omitted
the verifier's local `cli-args.cjs` dependency. Production remained on healthy
frontend SHA `ee156caa5b2a9ed2efaee34659f098e916badcb9`.

Frontend verifier hotfix PR #3675 added the missing dependency and a recursive
source-derived local dependency-closure contract. It merged as exact main
`14c9314e7067f4c3fc7f457f08c0209fe4d8d6fc`. Exact-head App PR CI run
`31179257874` passed; its parallel jobs included quality/contracts in 3 minutes
25 seconds, production build in 6 minutes 44 seconds, Playwright smoke in 3
minutes 28 seconds, critical shell in 4 minutes 39 seconds, and the deliberately
selected Network Museum matrix in 27 minutes 19 seconds.

Fresh controller `31181441784` failed closed in four seconds with
`ENVIRONMENT_LOCK_HELD`; it did not build or deploy. The earlier verifier-failed
operation remained `BOUND` because completion listener job `31176607693` was
skipped. The listener repeated the GitHub name-shape compatibility error:
current run payloads expose the evaluated run title in both `name` and
`display_title`, while the event/job gate expected a static workflow name.

Frontend recovery PR #3677 therefore classifies terminal workflows by immutable
path and exact evaluated title after exact repository, head repository, main
branch, event, run ID and attempt checks. Manual recovery is main-only and
restricted to the two existing emergency actors in both the job gate and shell.
It accepts only a numeric terminal run ID, proves that a failed deployment had
exactly one successful authority acquisition, and derives the persisted
operation ID from that run. Zero acquisitions are ignored; ambiguous evidence
fails closed. The backend independently rereads the exact operation and terminal
run and permits only an idempotent release of the same persisted lock.

At exact signed head `94efe6b801141b75b32bd1bc1140ca2c5dc6bf8d`, local
completion/controller/failure tests are 23/23; full Jest and Playwright test
typechecking, changed lint, Prettier and whitespace pass. The job-level actor
check has a documented line-local Sonar false-positive suppression: Sonar rule
S8232 is intended for trigger contexts where an actor can differ from the
untrusted content author, whereas this check is the authenticated dispatcher of
a main-only `workflow_dispatch` and is only the first of three independent
identity checks. A source contract test preserves the exact gate and
suppression. Hosted exact-head CI remains authoritative before merge.

The Dev Team Wave received architecture and incident updates through drop
`1280071`. No team reply or unresolved design objection was visible at that
checkpoint. Five-minute monitoring remains active through the requested
observation window.

### Current remaining gates

1. complete #3677 exact-head hosted CI and review, then merge without bypassing
   an objective gate;
2. run the governed completion recovery for exact failed controller
   `31175798509` and retain proof that only its stale authority was released;
3. dispatch a fresh one-click controller from exact frontend main and require
   operation-bound build, isolated verification, deployment, exact live-version
   proof, automatic Production E2E and authority completion;
4. inspect and hash immutable selection, operation, qualification and E2E
   evidence, record actual end-to-end timing, and publish the final closeout in
   this repository and the Dev Team Wave.

## Terminal recovery hardening, 2026-08-07

Frontend recovery PR #3677 completed exact-head review at
`122155b2a59136d54b584dc574bcf73c118a26af` and merged as
`1c8f0982502019938ac8c79ca60e390af0ed6be4`. Hosted run `31183698203`
passed every selected lane; the long Museum matrix took 38 minutes 12 seconds,
while the production build, quality/contracts, Playwright smoke and critical
shell lanes completed independently in 6:37, 3:10, 3:33 and 4:25. The general
and security review bots reported no findings and there were no unresolved
threads.

The first manual recovery run, `31187092756`, then exposed a second name-shape
assumption in the immutable evidence helper. The outer workflow correctly used
the evaluated title, but the helper still required the static name
`Web Deploy - PROD`. No authority was released and no production mutation
occurred. Frontend PR #3678 changed the helper to require both GitHub `name`
and `display_title` to equal the exact evaluated production-deploy or automatic
E2E title. It replayed the exact failed run and produced evidence digest
`7c44ad1067c35666c919ca46c428ce31ab2ff3499aa97e5529ddb32b5d441ccd`.
The exact PR head `17b2ef7e79d92ee6067a357db4af10cf63620e6c` passed 25/25 local
tests and hosted run `31187467180` in 4 minutes 40 seconds, with no bot or
thread findings. It merged as exact frontend main
`51a1e3b533ae1ecd177e4464dfa8901dd82051d2`.

Recovery run `31187966416` proved the immutable terminal evidence, then the
backend returned HTTP 409 because operation `frontend-prod-31175798509` had
already reached terminal `EXPIRED` state with reason `LEASE_EXPIRED`. This was
a safe refusal to rewrite terminal history: the operation no longer owned the
lock, and the backend correctly did not report a new failure transition.

A fresh exact-main controller, `31188152187`, began at 14:33:06 UTC. Its
atomic acquisition succeeded at 14:33:15 UTC, independently proving that the
expired operation had released production authority. It is the final timed
qualification operation for this rollout; its complete builder, verifier,
deployment, live-version, automatic E2E, authority-completion and immutable
artifact evidence will be appended below.

That controller launched exact builder `31188183057`, which succeeded in 9
minutes 13 seconds. Artifact `8997939019` is 119,484,863 bytes and has GitHub
archive SHA-256
`2715fd2b95aadee7bb46fa348b29c2d759438b5a316db8f7d3b57ae6b39bf186`.
Isolated verifier `31188958948` failed in 27 seconds before extraction because
the verifier's closed archive contract admitted `target/package.zip` but not
the builder's 669 checksummed deployment assets under
`target/_next/static/`. No deploy job ran. Automatic completion listener
`31189033102` succeeded, submitted canonical terminal evidence and released
the operation without manual recovery, proving the repaired listener on a real
failure path.

The downstream audit found one additional mismatch before another controller
was dispatched: the deploy job reused the production-artifact member command
for the two-file selection archive. Frontend PR #3679, exact signed and
DCO-compliant head `28be844dedf238b3e5edeb34860daf8dc0b7281b`, separates
the contracts. Production artifacts may contain only required metadata,
`target/package.zip` and checksummed `target/_next/static/**`; selection
artifacts may contain exactly `SHA256SUMS` and `selection.json`. Traversal,
absolute and backslash paths, duplicate file/directory collisions, symlinks,
special files, missing or extra checksums and all digest/identity checks remain
fail closed.

The exact failed artifact was downloaded and replayed locally. All 673 outer
members passed the corrected pre-extraction contract, all 672 checksums and the
package passed, and deterministic selection generation produced digest
`8328aac43c0fc7f43468ad5b03fae5c77fc37d67a8c63aedaa5b6a0cc4f25c19`.
Focused validation is eight suites and 130 tests, with changed lint, changed
typecheck, full Jest and Playwright test typecheck, Prettier and whitespace
green. Hosted exact-head CI and review remain required before merge.

Before merging #3679, a downstream identity audit found four remaining static
workflow-name comparisons in the automatic qualification path. The operation-
bound workflows now use evaluated GitHub run titles, and GitHub returns that
evaluated value in both `name` and `display_title`. Live controller
`31188152187`, for example, has the exact bilateral identity
`Production deploy 51a1e3b533ae1ecd177e4464dfa8901dd82051d2
[frontend-prod-31188152187]`; the prior static `Web Deploy - PROD` comparison
would have rejected the genuine deploy after it completed.

PR #3679 follow-up `889cf79c0608ff9a83f49acb2d01da258f3aaaf1`
therefore binds automatic E2E discovery to exact title
`Production E2E automatic <deploy-run-id>` in both fields. Current deploy
resolution, previous-deploy discovery and the isolated evidence verifier bind
both fields to `Production deploy <head-sha> [frontend-prod-<run-id>]`, while
also requiring the immutable path, repository and head repository, protected
branch, numeric attempt, run/SHA identity and terminal status. Static names are
negative test cases. This is a stricter operation identity, not a compatibility
exception.

The exact follow-up passes eight one-click, recovery and verifier suites with
114 tests, changed lint, changed typecheck across 1,410 files, full Jest and
Playwright test typechecking, Prettier and `codex-diff-check`. The difference
from the earlier 130-test count reflects the exact eight-suite selection on the
current base rather than a product or contract regression. Hosted exact-head
review and CI restarted after the push; no production controller will run
until they pass and the reviewed head merges.

The pre-release live baseline at approximately 15:41 UTC remained healthy but
historically split: three uncached `https://6529.io/api/version` reads returned
served SHA `ee156caa5b2a9ed2efaee34659f098e916badcb9`, `stale:false` and no
accepted announced version, while three reads of the CloudFront announcement
returned older ready SHA `ebe465ed7bce1fb5e019384a75d205f35d503c57` from run
`31097806888`. The final acceptance check must therefore prove that both the
served runtime and fresh announcement converge on the new exact merged SHA;
the current healthy-but-split baseline is not final release evidence.

An independent adversarial pass also reviewed pagination and retry semantics.
Its findings do not block this release after inspection. Automatic E2E run
listings are bounded to 100 but constrained to runs created after the exact
deploy began, so exceeding the bound during a single release is operationally
implausible and fails closed. Artifact listings are scoped to one exact run,
which emits far fewer than 100 artifacts; they also fail closed if that
contract changes. Prior-deploy discovery can miss a success only after more
than 99 intervening completed deploy attempts, in which case it conservatively
runs all Museum packs. Duplicate bot-dispatched E2E runs are prevented by the
per-deploy dispatcher concurrency and exact-run reconciliation; human manual
runs do not match the required bot actor. Finally, a terminal automatic E2E
failure intentionally ends and releases that production operation; retry is a
new governed controller, not an in-place attempt that preserves deployment
authority. These are worthwhile future scale/documentation improvements, but
none can falsely qualify the pending exact release.

PR #3679 completed exact-head CI at
`889cf79c0608ff9a83f49acb2d01da258f3aaaf1`. App PR CI run
`31192449706` passed the quality/contracts, production build, smoke, critical
shell and protected Museum lanes; the Museum matrix completed in 24 minutes 42
seconds. CodeQL, Sonar, Snyk, DCO, secret scan, Debt Ratchet, public-review
trust and the 6529bot exact-head follow-up were green, and the PR had zero
review threads. The controlled maintainer merge produced exact frontend main
`fa6072da0de8ad476c93399b2bd122bfde797c7d` at 15:52:47 UTC.

The production lane was then read back quiescent. Fresh timed controller
`31194846549` was dispatched from that exact main at 15:53:15 UTC with exact
evaluated title
`Production deploy fa6072da0de8ad476c93399b2bd122bfde797c7d
[frontend-prod-31194846549]`. This is the only run eligible for final timing
and speedup claims. Its authority, builder, verifier, deploy, live-version,
automatic E2E, evidence and completion results remain to be appended.

Controller `31194846549` did not qualify and is excluded from timing claims.
Its builder `31194877787` succeeded in 9 minutes 5 seconds and uploaded exact
artifact `9000650448` with API digest
`sha256:e0864c71b6d82db840644e8dfc9e90e5b900c31bbffe97357246c35bc5368c28`.
Isolated verifier `31195650604` then passed input identity, builder/artifact
identity, archive membership, extraction, extracted membership, ancestry,
manifest, checksums, package bytes and the independent checksum replay. It
uploaded selection artifact `9000672392` and failed only in the final output
step: upload-artifact v4 emitted raw 64-hex digest
`2efbcea43af6156a84e79f2382eb8199778ad3532c212e58a223f46699802e1f`,
while the downstream API-digest contract correctly required the canonical
`sha256:<64hex>` form. No deployment job ran. Completion listener
`31195725657` submitted terminal failure evidence and released operation
`frontend-prod-31194846549`.

Narrow frontend PR #3682 is open at exact signed and DCO-compliant head
`95167eb6d20a7063bc692bcf8c2c5db48128227f`. It prefixes the one upload action
output with `sha256:` before publishing verifier outputs and pins that exact
expression in the workflow contract test. No archive, checksum, identity,
application or deployment rule changes. Four suites and 79 tests, changed
lint/typecheck, full Jest and Playwright test typecheck, Prettier and whitespace
pass locally. A fresh controller will start only after exact-head hosted review,
CI and merge.

PR #3682 completed exact-head hosted review and CI with all checks green and
zero review threads, then merged as frontend main
`47d3629c3bd0a60736b0836ea05af9de93be1d74` at 16:34:31 UTC. Before spending
another production build, manual verifier replay `31198251321` ran the corrected
main workflow against exact prior artifact `9000650448`; every identity,
archive, extraction, ancestry, checksum, package, selection-upload and digest-
publication step passed in 22 seconds. This provides real-artifact proof for
the boundary that failed in `31195650604`.

After a new quiescence readback, fresh timed controller `31198321516` was
dispatched at 16:35:41 UTC from exact main
`47d3629c3bd0a60736b0836ea05af9de93be1d74`. Its exact title is
`Production deploy 47d3629c3bd0a60736b0836ea05af9de93be1d74
[frontend-prod-31198321516]`. This supersedes the failed timing sample and is
the only current candidate for final speedup claims.

Controller `31198321516` did not qualify and is excluded from timing claims.
Builder `31198362313` succeeded in 8 minutes 16 seconds and uploaded artifact
`9002012819`, 119,470,951 bytes, with API digest
`sha256:eb42ad00ba91843785b1cbaaf24efd90eff0a5d62122a1a7485e0c871f5dce38`.
Verifier `31199024181` succeeded in 41 seconds and uploaded selection artifact
`9002033401`. The parent then rejected the selection attachment because the
unit fixture had invented `artifact.workflow_run.run_attempt`; GitHub's live
artifact API provides the attached run ID and head SHA but omits that field.
No deployment job ran. Completion listener `31199097332` submitted failure
evidence and released the exact operation.

Frontend PR #3683 made the selection attachment's attempt check conditional
on GitHub supplying that optional field. Exact attempt identity remains
mandatory through the authenticated verifier run, the attempt-suffixed
artifact name, and downloaded `selection.json`. A plainly named negative test
proves that a supplied mismatched attachment attempt still fails. The PR
completed exact-head review with the 6529bot follow-up reporting no findings,
all required CI green, and zero review threads, then merged as frontend main
`ba2506795b3eeeaf3857b0f701a6d400443097d4`.

Fresh controller `31200903180` began at 17:08:23 UTC from that exact main.
Authority acquisition passed. Builder `31200930098` succeeded in 9 minutes 23
seconds and uploaded artifact `9003035656`, 119,470,135 bytes, with API digest
`sha256:2f10dff30d29eaa069a9be286a10c427c5c6a32bf4b2b5a8cf2e14e1750924c9`.
Verifier `31201663334` passed every identity, archive, extraction, ancestry,
checksum, package, selection-upload and digest-publication step in 41 seconds,
creating selection artifact `9003060628`. The parent resolver passed, but the
deploy job then failed closed before AWS because its environment received
blank builder run ID and attempt. Resolver outputs `artifact-run-id` and
`artifact-run-attempt` referenced nonexistent child fields `artifact_run_id`
and `artifact_run_attempt`; the child contract emits `builder_run_id` and
`builder_run_attempt`. Completion listener `31201769571` released the failed
operation. Production remained unchanged.

Frontend PR #3685 corrects those two mappings and adds a generalized workflow
contract: every resolver output expression must refer to a field exported by
the child controller's authoritative `OUTPUT_FIELDS`. Four release suites and
95 tests, changed lint/typecheck, format and whitespace passed locally.
6529bot reported the exact head good to merge with no security findings, and
CodeRabbit produced no actionable comments. Exact-head hosted CI is in
progress. A new controller will be the only sample eligible for final timing.

PR #3685 completed exact-head hosted review and CI at
`a9a493791089f5ab3cf7db01862c73137e92e725`. All App PR CI lanes passed:
quality/contracts in 3 minutes 19 seconds, production build in 6 minutes 58
seconds, Playwright smoke in 4 minutes 40 seconds, critical shell in 5 minutes
10 seconds, and the protected Network Museum matrix in 25 minutes 49 seconds.
Installed Apps then passed in 2 seconds. CodeQL, Sonar, Snyk, DCO, secret scan,
Debt Ratchet, public-review trust, 6529bot and CodeRabbit were green, and the
exact head had zero review threads. The controlled maintainer merge produced
exact frontend main `6a6c5e1b51191d60f7424a7426c2a64832775b8a` at 17:49:28
UTC. The protected Museum duration is recorded separately from ordinary
non-Museum fast-path performance because this PR changed the production
controller and therefore entered the repository's high-risk tier.

Cross-repository production readback found no active frontend or backend
production, deploy, E2E, artifact, authority, migration or API actor. Fresh
controller `31204118712` was dispatched at 17:49:54 UTC from exact main
`6a6c5e1b51191d60f7424a7426c2a64832775b8a`, with evaluated title
`Production deploy 6a6c5e1b51191d60f7424a7426c2a64832775b8a
[frontend-prod-31204118712]`. Exact authority acquisition passed in five
seconds and launched operation-bound builder `31204144665` at 17:50:14 UTC.
This controller is the only current candidate for the final successful timing
sample; its builder, verifier, deploy, live convergence, automatic E2E,
evidence verification and authority completion remain to be appended.

Builder `31204144665` succeeded in 7 minutes 37 seconds and uploaded artifact
`9004232082`, 119,475,185 bytes, with API digest
`sha256:97312759f1b0cf6cbb9cc68460bcada0c9b7626156b657dac0f200bf0eda2b88`.
Isolated verifier `31204753177` then passed all exact-run, workflow, artifact,
archive-path, extraction-path, protected-main ancestry, manifest, checksum,
package and independent checksum-replay gates in 21 seconds. It created
selection artifact `9004252129`, API digest
`sha256:1b3dcebedc68c73333b78f5a4a080fdb88bddb55a2da39595e344133de1211fc`,
and selection digest
`310c2383a96e3b9882f041adca8701bdb5b810f0a3698d6d6acb69020291f446`.
The downloaded selection binds builder `31204144665/1`, verifier
`31204753177/1`, source/workflow/protected-main SHA
`6a6c5e1b51191d60f7424a7426c2a64832775b8a`, package SHA-256
`6716803b4485e63a52b206fd741064c186282258055f27f6f32b6b6d51d6ed1a`,
and exact operation `frontend-prod-31204118712`.

The controller's deployment job accepted those corrected run-ID/attempt
outputs, reverified the immutable selection and selected artifact, uploaded
operation evidence, reauthorized the production mutation, and completed S3
and Elastic Beanstalk deployment. Exact-version readiness, HTTP-version proof,
announced-version publication and durable evidence uploads passed. The deploy
job took 7 minutes 14 seconds; the complete controller ran from 17:49:54 to
18:05:59 UTC, 16 minutes 5 seconds by workflow timestamps (GitHub's displayed
job/run duration may round or exclude queue setup). Automatic Production E2E
run `31205398386`, evaluated title `Production E2E automatic 31204118712`,
started at 18:06:08 UTC on the same exact SHA. Its readonly packs, isolated
evidence verifier and completion listener remain to be appended before the
success timing clock closes.

Automatic E2E run `31205398386` did not qualify and is excluded from successful
timing claims. Its readonly job succeeded in 11 minutes 58 seconds: exact
automatic dispatch identity, immutable source, fail-closed full Museum
selection, all production-safe read-only packs, Playwright evidence and
authority evidence passed. The clean isolated runner also verified its own
immutable tooling, downloaded the untrusted evidence and immutable selection,
and validated the evidence successfully. The next step, `Write automatic
production qualification record`, failed because `gh api` rejected the
explicit `Accept: application/octet-stream` header when downloading the
controller operation ZIP: HTTP 415, `Must accept application/json`. No product
or evidence-validation test failed. Live production remained exact and healthy
at `6a6c5e1b51191d60f7424a7426c2a64832775b8a`; qualification remained closed.

Frontend PR #3686 is open at exact signed and DCO-compliant head
`0fcd11ac760c674e1043f9de1a2f5f93703bddee`. It changes the operation-artifact
download in Production E2E and both artifact-download helpers in authority
completion to GitHub's supported `Accept: application/vnd.github+json` media
type. All digest, size, exact-member, link, exclusive-write, identity and
authority checks remain unchanged. Contract tests require all three supported
headers and forbid the rejected header. A byte-preserving live probe downloaded
real operation artifact `9004273076` as an exact 574-byte PK ZIP with SHA-256
`b0bf862e86e3763b68fb93d954732574cba3ecdcc5fc6c2d70cf7d047859b940`,
matching GitHub's API digest. Ten release suites / 138 tests, changed lint,
changed typecheck, Prettier and whitespace pass locally. After exact-head CI and
review, the deployed release will be requalified before one clean controller is
used for the final uncontaminated timing sample.

The failed E2E exposed a second, independent automatic-completion gap. The
existing `workflow_run` completion listener ran when the deployment controller
became terminal, correctly found the newly dispatched E2E still pending, and
exited without mutation. GitHub did not emit another listener when the
dynamically named E2E later became terminal, so no event remained that could
close the authority operation. PR #3686 therefore now makes the deployment's
E2E dispatcher own the exact terminal handoff: it exports the unique E2E run
ID on every successful reuse or dispatch path, polls that exact run to a
terminal state while continually binding repository, workflow path, branch,
head SHA, deploy-run input, bot actor and evaluated title, then dispatches the
authority-completion workflow with the exact terminal run ID and requires one
exact completion run to appear. Authority completion independently re-reads
all terminal identity, canonical-run, isolated-verifier, operation, evidence,
selection, qualification-digest and backend-authority facts; the dispatcher
cannot declare completion itself.

The final PR #3686 head is
`0467ef08b576d3a5f9d5123bfd6718afaa2afdbf`. Bot-authored completion dispatch
is accepted only from protected `main` and only for an immutable
`production-e2e.yml` target. Human recovery remains restricted to the existing
release actors. The dispatcher job has a 120-minute ceiling around a bounded
100-minute terminal poll, leaving headroom over the E2E workflow's 90-minute
limit; completion-run discovery backdates its lower bound by five seconds for
runner/server clock skew. Contract tests pin the exact E2E run-ID output on
both success paths and every new trust gate. Local validation passes ten
release suites / 139 tests, changed lint and typecheck, formatting and
whitespace checks. The 6529bot exact-head follow-up reports no new findings,
explicitly accepting the real ZIP probe, timeout budget, skew buffer and
run-ID invariant. Exact-head hosted CI is in progress; no merge or production
mutation occurs before its required checks pass.

PR #3686 completed every exact-head gate and merged as frontend main
`4d870d0f7d579d5c950eae5321d7008e522b88c1`. Two manual authority-completion
recovery runs, `31209672795` and `31210103675`, then independently parsed and
verified the exact failed E2E and controller evidence but received five bounded
HTTP 503 responses each from the backend failure callback. CloudWatch confirmed
that every callback reached the production API. A credential-safe direct replay
returned `AUTHORITY_UNAVAILABLE`; no credential value was logged or persisted.

Live GitHub App diagnostics ruled out transport and installation failures. App
token creation returned HTTP 201, the exact deployment and E2E run reads both
returned HTTP 200 with the expected repository, path, title and terminal state,
and the deployment actor was an active organization administrator. The defect
was an internal parser contradiction: the shared workflow identity parser
rejected literal `github-actions[bot]`, while both Production Authority's
success and failure predicates require that exact actor for the automatic
Production E2E qualifier. The parser threw before those role-specific checks,
and the service correctly translated the unreadable qualifier to a fail-closed
503 response.

Backend PR #1913 initially made that bot actor parseable in the shared reader.
The auth/API review correctly observed that this broadened the parse boundary
for unrelated Release Bus operations. The final exact head
`ada537cbe0bf0a3425bd8d75394134fab31347c7` therefore restores the generic
reader's rejection and adds a separate Production E2E reader. That dedicated
reader accepts the bot only for the frontend repository and head repository,
`workflow_dispatch`, and `.github/workflows/production-e2e.yml`. Production
Authority invokes it only for a frontend qualifier; deployment, compose,
merge, manual-deployment, baseline-adoption and backend-completion paths retain
the generic reader. Adversarial tests prove that the generic reader rejects the
bot and the dedicated reader rejects the bot on a compose workflow. Local
validation passes 37/37 authority tests, 12/12 focused workflow-identity tests,
targeted ESLint, root TypeScript, Prettier and whitespace checks. Fresh hosted
CI and exact-head review are in progress.

Backend PR #1913 completed all hosted gates at exact head `ada537cb`: the
15-minute CI job passed the full 803-test backend suite, backend and API builds,
and exact merge-tree evidence; CodeRabbit, Sonar, Snyk, DCO and the 6529bot
follow-up were green, with zero review threads. It merged as backend main
`7103b31173c1b4e9d3d443c55ddf01d8510a0a98` at 19:45:02 UTC.

Emergency API bootstrap run `31212904987` was dispatched from that exact main
to deploy the compatibility correction. It failed closed in eight seconds,
before checkout, build or cloud credentials, because the stranded frontend
authority still owned the shared production lock (`ENVIRONMENT_LOCK_HELD`).
The bootstrap correctly does not bypass an active lease. The frontend lease is
bounded to 130 minutes and its authority to a 150-minute hard TTL; it was last
renewed during controller `31204118712` and should age out around 20:20 UTC.
The failed bootstrap did not renew it. The selected response is to preserve
serialization, wait for the bounded lease to expire, then retry the exact API
deployment; no direct production-database mutation or lock bypass is used.

The current production-authority API subsequently observed the old frontend
operation `frontend-prod-31204118712` after its bounded lease and marked it
`EXPIRED` with reason `LEASE_EXPIRED`. The shared production lock became free
through that ordinary control-plane transition; no database access or manual
lock mutation was used.

A second emergency API bootstrap, `31214794411`, then acquired and bound exact
backend operation `backend-prod-api-31214794411` to backend main
`7103b31173c1b4e9d3d443c55ddf01d8510a0a98`. It stopped 15 seconds after
dispatch, before checkout, build or cloud credentials. The cause was a strict
local response validator whose literal key array did not match lexical sort
order: `control_epoch` must precede `controller_identity`. The valid authority
response was therefore rejected after acquisition. Completion listener
`31214826356` exposed a separate identity mismatch: the listener expected the
static workflow label `Deploy a service`, while GitHub returned the evaluated
run title in both `name` and `display_title` for this workflow.

The exact failed operation was closed through the authenticated
`production-authority/fail` API using a deterministic state document bound to
run `31214794411/1`, service `api`, target SHA `7103b311...`, and null selection
digest. The callback independently verified the failed GitHub run and returned
status `FAILED`; the shared lock is null at row version 341. No cloud mutation
occurred. The local state document is 369 bytes with SHA-256
`fbaac1ad1e6ddf0fa95c3aa9640efe32513161633a1bd556768ccdb884e00b6e`.

Backend PR #1914 is open at signed, DCO-compliant head
`261cafa0fa66ed8593f2bb0a9ef379f4e059f181`. Its five-file patch corrects the
canonical response-key order in both the deploy-workflow generator and its
generated workflow, validates completed deploy identity against GitHub's
evaluated title while retaining exact repository/path/event/branch/SHA/title
bindings, and adds regression assertions for both live-discovered defects.
The focused production-authority workflow suite passes 8/8; targeted ESLint,
Prettier, deterministic generation and whitespace validation pass. The full
performance suite remains Linux-authoritative because unchanged cases require
`sha256sum`, POSIX Git paths and `O_NOFOLLOW`; hosted CI and review are in
progress. After merge, the release must still prove an exact backend API deploy
and automatic lock release, followed by one fresh frontend controller whose
deployment, automatic Production E2E, isolated verifier and authority
completion all succeed.

Review of PR #1914 challenged the intermediate run-name comparison. The real
GitHub API response for run `31214794411` reports the evaluated title in both
`name` and `display_title`, while its numeric `workflow_id` resolves through the
workflow endpoint to static name `Deploy a service`, exact deploy path and
active state. Exact head `7cd73a020298538e8c4974df40967e6135f2e226`
therefore removed the self-comparison and verifies both layers independently:
exact run identity and title grammar, then exact static workflow identity by
ID. The 6529bot exact-head follow-up reported no new findings.

Hosted run `31216141202` then passed 804/805 tests; the only failure was the
protected policy-bundle digest, which changed because the deploy generator,
generated workflow and performance contract are protected members. Exact head
`a2359e3f6d677d5ad3fea7f0f6f41645ae97c579` preserves the prior digest and
advances the trusted rollout chain to the Linux-computed current digest
`71ce7c1b557c45fe9096fda2b0e6ddb19d78f7c50f6b6ee12f8b56487547f296`.
Focused rollout trust tests, lint, formatting and whitespace checks pass; fresh
hosted run `31216912106` is in progress.

PR #1914 subsequently reached exact signed head
`64db036a6aeb2f689b648e7f8c27b2c99416f487`. The final review delta adds a
bounded retry for the static workflow-definition read and retains separate
GitHub Actions steps for temporary-file cleanup; CodeRabbit's cross-step shell
trap suggestion was rejected because traps cannot cross step/shell boundaries.
All review threads were answered and resolved. Exact-head hosted run
`31217950783` passed in 15m34s with 805/805 tests, backend and API builds,
generated-file verification, exact merge-tree evidence, CodeRabbit, Sonar,
Snyk and DCO green. PR #1914 merged as backend main
`99089bfe168684500cb78a302f44be592f13499c` at 21:11:52 UTC.

Emergency API bootstrap run `31219160800` then acquired and bound exact
operation `backend-prod-api-31219160800` to that main, but failed closed in 14
seconds at the response adapter, still before checkout, build or cloud
credentials. The corrected lexical key order was accepted. The next predicate
was semantically invalid jq: after piping into `.hard_expires_at`, the filter
attempted to read `.lease_expires_at` from the resulting number and raised
`Cannot index number with string "lease_expires_at"`. Both initial acquire and
reauthorization contained the same expression.

Completion listener `31219193219` correctly resolved the numeric run
`workflow_id` to the static `Deploy a service` workflow, proving the #1914
run-title/static-workflow separation in production. It could not close the
failed operation because no failure artifact existed. The deployment log
showed why: the exact authority-state file was written only after the jq
response validator, so the adapter failure left nothing for the successful
`upload-artifact` step to upload. The exact failed operation was then closed
through the ordinary authenticated `production-authority/fail` API with a
deterministic 369-byte state identity and evidence SHA-256
`5b4b8b3ff63a939ee346bb6b201d251c3dd4e40ce3745306cdda51de0c8c2b1e`.
The service returned `FAILED`, `reused:true`; the shared production lock is
null at row version 343. No database edit, lock bypass or cloud mutation
occurred.

Backend PR #1915 is open at exact signed+DCO head
`91cd5ee537b7fcf4113f0ef9663217ff7693cdf8`. It keeps the full response object
in scope for `.hard_expires_at > .lease_expires_at`, persists the exact
acquired-operation identity before response parsing, and gives the completion
listener twelve artifact-index observations over a bounded 55-second interval
before it treats evidence as absent. Regression coverage extracts both inline
jq filters from the generated production workflow and executes them against
valid, equal-expiry and wrong-type fixtures. The generated workflow remains
deterministic; the executable focused workflow suite passes 9/9, targeted
ESLint, Prettier and whitespace checks pass, and the exact Linux protected
policy digest was independently computed in a clean container as
`286fb53b44defe2958b8f0d97baa8d090f4992e521b3aa78d6b787da7890cb16`.
Hosted Linux CI and configured review bots are in progress. After merge, the
remaining release gates are an exact backend API deployment with automatic
authority closure and one fresh frontend controller with automatic Production
E2E, isolated verification and automatic authority completion.

PR #1915 completed its exact-head review at `91cd5ee537b7fcf4113f0ef9663217ff7693cdf8`.
Hosted run `31220090608` passed in 16m24s with 805/805 tests, backend and API
builds, deterministic generation and merge-tree evidence. The general review
reported Good to merge; auth/API, deploy/actions, security, DB/Lambda and
media/external lanes reported no findings; CodeRabbit completed with no inline
finding; Sonar, Snyk and DCO passed; and no review thread remained. PR #1915
merged as backend main `a14af4a197b5c3b8e4ffcf785bdb507f3e3b9cec` at
21:44:08 UTC.

Guarded API bootstrap `31221212093` then crossed every earlier control-plane
failure. It acquired exact authority, checked out immutable source, built the
API, reauthorized immediately before AWS credentials, deployed, and verified
the exact live version. `https://api.6529.io/health` reported commit
`a14af4a197b5c3b8e4ffcf785bdb507f3e3b9cec` with database and Redis healthy in
three consecutive reads before the frontend production operation began.

The run subsequently failed while constructing success evidence. The
generated jq filter contained `index\.zip` as jq source text; inside a jq
string, a literal dot requires `index\\.zip`. This was a post-deployment
evidence-generation defect, not a product deployment failure. The repaired
failure path uploaded artifact `backend-production-authority-failure-31221212093`
(artifact ID `9010470056`, ZIP SHA-256
`b07ece3e9a8cac9a173949aa4c41799112a86f47010ca5bd3b0e9b2421ce9969`).
Automatic completion run `31221338781` passed and released the shared
production lock at row version 346. No database edit or authority bypass was
used.

Backend PR #1916 is open at signed, DCO-compliant head
`aca59fffddca02711425ea0586c50191b85ef308`. Its runtime patch is the single
escaping correction in the deploy generator and generated workflow. It also
executes the exact generated deployment-selection jq filter against valid API
and named-service ZIP paths and rejects `indexXzip` and `index.zipx` lookalikes.
The executable production-authority suite passes 10/10, targeted lint,
formatting, deterministic generation and whitespace checks pass, and the
protected policy digest was independently recomputed in Linux as
`b563ed89a7edc5c70031503f74946ba5fa664ed1cecd401a456ed9190dafb0c4`.
Hosted CI and configured review are in progress.

Fresh frontend one-click controller `31221425555` was dispatched at
21:47:54 UTC from exact frontend main
`4d870d0f7d579d5c950eae5321d7008e522b88c1`, after three exact backend health
reads and a null production lock. Authority acquisition passed and child
artifact builder `31221446017` began compiling the immutable production bytes.
This is the release timing sample. The primary wall clock runs from controller
creation through terminal automatic Production E2E; authority-completion time
will be reported separately. The sample is successful only if deployment,
automatic E2E, isolated verification and automatic authority completion all
pass.

Builder `31221446017` completed successfully in 9m40s. GitHub artifact
`9010721865`, named
`production-frontend-4d870d0f7d579d5c950eae5321d7008e522b88c1-frontend-prod-31221425555`,
is 119,480,259 bytes with API digest
`sha256:cb4c38365d0ba3c29a8e6a254203e9a7de75d14e24575aed90b47b77d8545f86`.
Isolated verifier `31222072314` completed in 34 seconds after validating the
builder identity, protected-main ancestry, archive members, manifest,
checksums, package bytes and an independent checksum replay. Selection artifact
`9010737175` has API digest
`sha256:9fc8ff7b55fdf1145258e7c1309b586995016677685abc8134245baa5342b2d1`.
The downloaded 1,782-byte selection document has SHA-256
`70bec887a263fd7f0aee84ed4ab638a41de53b91ad2cd70fa21bfd03c0c30528`
and binds selection digest
`c09462d1854dc94b013c93c43d4b7adb32635e73059be34d165f2821adbf5216`,
manifest SHA-256 `fd9b64f30613611e53f3c09ab8949c81d7a569257fb0e70104deabfa4a74082a`,
checksums SHA-256 `c055cfd1fe11d1cecf67ca11b641ccece9c3a88917970169c5a5030abef6b993`,
and package SHA-256
`a76c1e491d2c17c70bebd02eeb282234f0aa9aae61a91a1a3f995ae0da0208b7`.

The controller reverified that exact selection and artifact, uploaded operation
evidence, reauthorized before AWS credentials, and completed S3 and Elastic
Beanstalk deployment. Exact readiness passed at 22:03:33 UTC; three consecutive
HTTP-version observations passed by 22:03:55 UTC. The controller completed in
16m13s. Its deployment-bus manifest has SHA-256
`3c0d5d86c552cd0ab7fb41eb84559ce663c29b4bbca5e87e432b6e4e26d4fa7d`,
and exact-version evidence has SHA-256
`081ef99e8be4e5aa7fc613be0b2f6f16a72014013f836b75988d141cc7a36376`.
Automatic Production E2E `31222473935` began at 22:04:16 UTC, dispatched by
listener `31222466996`. The simultaneous completion listener `31222466714`
correctly observed that E2E was not terminal and made no authority mutation.

Review of PR #1916 requested stronger parser-layer evidence. The runtime patch
was unchanged: two backslashes in the raw YAML survive Bash single quotes and
become one regex backslash after jq parses its string, so the regex engine sees
`\.` and matches a literal dot. Follow-up head
`a85d25a433a2c6b485fcb58b06a9fae41c2e9e01` extends the executable negative
set to an arbitrary missing-dot suffix, a literal-backslash path, a prefixed
path and an extra path segment. Generator regeneration remains byte-identical,
the focused suite passes 10/10, and the 6529bot exact-head follow-up reports no
new findings. Fresh hosted run `31222803633` supersedes cancelled earlier-head
run `31221940426`.

After the exact frontend deploy, thirteen representative Museum routes returned
HTTP 200: home, About, collection, Casey Reas artist, CENTURY project and
system, accession gift, first object, Stories, scholarship and writing, A Field
of Practice, Programs, and Rights. This direct status sweep supplements but
does not replace automatic browser qualification.

Automatic Production E2E `31222473935` completed successfully at 22:15:46 UTC.
Its readonly job passed in 10m59s and its clean isolated verifier passed in 22
seconds. The evidence records 16/16 packs passed on their first attempt, zero
product failures, zero infrastructure failures, three workers, and 165
Playwright assertions. The five fail-closed Museum packs contributed 92
assertions across About, data architecture, Inside the System, institutional
practice and Rights. Selection artifact `9010883734` has API digest
`sha256:3fe520a22d9da6e5129e90c6e4f509d2bb626330bd2fff95edce47ba39e8dc54`
and selection digest
`82067364f40cd96f2ca0ea013db1e43f277c34d438189e12c7c575a756b456d9`.
Evidence artifact `9011104056` has API digest
`sha256:f3c12a51691bf7dcc8fa0f3d278ac25bc8d282b837fe7d6614a38ee074fee268`;
its 10,401-byte canonical `evidence.json` has SHA-256
`02b842095a0de33661b124f5f44575b2a87b0c2ff0110ae062bef0066e011cdf`.
Qualification artifact `9011113075` has API digest
`sha256:2877627891037812198750a4303bfed60a28a388a696b5dce32c6a142fbc60bd`;
its qualification record has SHA-256
`cb9e561cff00a6914552552b7e3d2c0af34ed5712cad03cbe9057a1dd3a3b434`.

The dispatcher passed the exact terminal E2E run to automatic authority
completion `31223189513`. That workflow independently reread the deploy, E2E,
operation, selection, evidence and qualification identities, received a
`COMPLETED` response from the production-authority API, and released the shared
lane. The dispatcher itself completed successfully at 22:15:57 UTC. Three
subsequent public version reads matched both `version` and `announced_version`
to `4d870d0f7d579d5c950eae5321d7008e522b88c1` with `stale:false`.

The successful one-click clock began at 21:47:54 UTC. Terminal automatic E2E
arrived 1,672 seconds later: 27m52s. Authority closure arrived after 1,695
seconds: 28m15s. The primary E2E measure is 40.7 percent faster than the
46.983-minute comparable observation, 58.0 percent faster than the 66.3-minute
incident sequence, 33.7 percent faster than the 42-minute modeled parallel
median, and 50.2 percent faster than the 56-minute modeled serialized median.
This is one clean production observation, not a p95 or service-level claim.

Backend PR #1916 completed its exact-head review at
`a85d25a433a2c6b485fcb58b06a9fae41c2e9e01`. Hosted Linux run
`31222803633` passed in 16m02s: its four test passes reported 1,035, 807,
798 and 862 tests, and the backend build, API build, deterministic generation,
lint and format gates all passed. The exact merge-tree evidence artifact
`9011324701` binds merge tree
`c2e6d45131c554742e83e90407f9031c09bd666e`, the exact PR head and protected
policy digest
`b563ed89a7edc5c70031503f74946ba5fa664ed1cecd401a456ed9190dafb0c4`;
its ZIP SHA-256 is
`d136dc6ec1325f19b548ad55e55ffe5d47fa75ebce0b48dc645e5fae39e68219`.
DCO, Sonar and Snyk passed, CodeRabbit's status was green, 6529bot's exact-head
follow-up reported no new findings, and no review thread remained. Controlled
maintainer squash merge produced backend main
`092ea6218fbb29afbb311ecd2ee2ef31f3184d15` at 22:26:40 UTC; the audit
disposition is recorded on PR #1916.

The exact backend main was deployed by governed production run
`31223892606`, created at 22:27:43 UTC and completed successfully in 2m02s.
It acquired production authority, verified immutable source, built the API,
reauthorized the exact package immediately before cloud credentials, deployed,
and generated and uploaded the repaired success evidence. Artifact
`backend-production-authority-31223892606` is artifact ID `9011408949` with
GitHub ZIP digest
`sha256:955125452106c946d77d4cdd248fa04c4891c211332ae26613c944c5436eb3d0`.
Its sole 914-byte evidence document has SHA-256
`a8797d697c3b9ca799333a4f977cf1485dffd6c4508be557c7568d2c678cc10c`
and binds operation `backend-prod-api-31223892606`, exact target SHA
`092ea6218fbb29afbb311ecd2ee2ef31f3184d15`, exact package path
`src/api-serverless/dist/index.zip`, package SHA-256
`85a82fba1d69c2e0d88b84dc62f08e4cbebda422cb32f8d41a73d3b70777f018`,
package size 21,093,252 bytes, and selection digest
`559586baa6e321c615b2acb982a6e0e5e71b769becd0b3c4cb68005375c76a1d`.

Automatic completion listener `31224018833` then independently verified the
exact completed deploy run and downloaded artifact, replayed the evidence and
selection digests, received a `COMPLETED` response with a valid lock row
version from the production-authority API, and completed successfully in 13
seconds. Three subsequent public health reads reported status `ok`, database
and Redis healthy, and exact backend commit
`092ea6218fbb29afbb311ecd2ee2ef31f3184d15`. This closes the backend evidence
defect and proves automatic authority release without a database edit, manual
completion or control-plane bypass.

Dev Team Wave monitoring remained active on a five-minute cadence. Drop
`1281474` recorded the final architecture/status checkpoint before the backend
production proof; no new external team objection appeared before completion.

## Amendment: final release status

- amendment ID: `deployment-reengineering-closeout-2026-08-07`
- recorded at: `2026-08-07T22:30:05Z`
- supersedes: the status claims in the opening summary, **Architecture under
  review**, and every later gate section that describes the release as active,
  pending, blocked, provisional, or incomplete
- preserves: every run-time observation, failed-run account, decision,
  artifact identity, digest, timestamp, timing measurement, and historical
  checkpoint above

The superseded passages remain in place as a chronological engineering record.
Their status language describes the release at the time each passage was
written. The final release status is complete. Frontend production serves exact
SHA `4d870d0f7d579d5c950eae5321d7008e522b88c1`; controller `31221425555`,
automatic Production E2E `31222473935`, and automatic authority completion
`31223189513` all succeeded. Backend production serves exact SHA
`092ea6218fbb29afbb311ecd2ee2ef31f3184d15`; deploy `31223892606` generated
the valid success-evidence artifact and automatic completion `31224018833`
verified it and released authority. The production product and control-plane
gates described by this ledger are closed. Repeated clean releases remain
necessary before treating the single 28m15s observation as a percentile or
service-level measure.
