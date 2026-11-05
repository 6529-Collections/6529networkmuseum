# Salgado normal accession pages

Status: narrow local integration and rendered review in progress, 5 November 2026.

The user requested one ordinary acquisition page and six work pages, using the
published Magnum accession as the model. The six works retain accession
6529NM.2026.004, the unrestricted gift credit to punk6529, and the verified
13 September 2026 accession/title/custody evidence. Ordinary Museum display
was already authorized. No accession research or donor-rights intake is reopened.

The isolated source branch starts from remote main
3926d78faacf67a62b8d9b48e15d26c43b52eae9. The frontend starts from remote main
633e4fd5b8f1a06d3cbb44d4b119effcafc691db. Both were fetched on 4 November;
applicable current guidance was compared with the original checkouts. Unrelated
local work remains intact.

Verified source B2 6a56c1e03368b95abfdcce9f9555b344ff48b3de supplies the
accession, evidence, six source records and eighteen approved display images.
Historical catalogue C2 is 9bb0176d6a5af3910b1f1df51e7645849865785e. Their
review remains evidence for those exact editions. New derived edits are pending
review and do not claim historical approval.

The six existing short image-specific labels are retained. Version 1.1.1,
5 November 2026 adds ordinary artist/project/acquisition links and links each
photograph from the concise acquisition narrative. Artist and project context
stay on their own pages. Administrative records remain in Records. No new
research entity, essay, archive, or shared Markdown-renderer experiment is added.
The eighteen derivatives and required retained evidence total about 14 MB;
the optional expanded 136 MB archive remains outside scope.

Earlier automatic approval-review denials for archive upload and GitHub
PR-ready/review-bot actions remain in force. No such action, merge or deployment
is part of this local review. The localhost:8768 standalone preview is not used.

Remaining at this checkpoint: finish precise source projections, validate the
source and frontend mapping, render the actual Museum pages, inspect all six
photographs and navigation, and record the resulting evidence here.

## Local review completed — 5 November 2026

Implemented one ordinary acquisition page and six work pages, with the normal
artist, project and permanent-collection entries. The six short labels and
verified accession facts are retained. The display mapping removes repeated
tombstone metadata and publication-control prose; complete source records and
correction lineage remain available.

The actual Museum frontend was captured at 1440×1000, 820×1000 and 390×844:
the seven requested pages plus artist, project and collection views, thirty
full-page captures. Every page returned HTTP200; all Salgado images loaded;
there were no page errors or horizontal overflow. These are development-build
local review captures, not a production-build visual release qualification.

The existing uncatalogued local fixture uses the exact historical B2 reviewed
graph with the candidate catalogue texts. This composite is disclosed in the
local fixture receipt. It does not promote the canonical source's 56 new or
amended pending projections. The 368 earlier reviewed graph records retain
their existing review. Production source pointers remain unchanged.

Passed source checks: bootstrap (1,289 JSON files), full Museum validator, 50 graph tests,
exact 18-image fixity/dimension checks, fetch guard, deterministic graph replay,
publication inventory/bundle and release-manifest checks. The broader existing
unit suite was stopped during unrelated Casey mutation fixtures after no
reported failure; that whole suite remains incomplete.

Frontend checks passed for the focused media/entity graph suites, scoped label
projection, changed-file lint/typechecking, exact-working-tree TypeScript,
help-index sync and documentation links. Existing browser contracts were
updated for the candidate's 19 collection works, 24 artists and 5 acquisitions;
they were not claimed to pass against the older live source edition.

A 5 November remote refresh confirmed Museum main remains 3926d78f. Frontend main
is 49dddaf24f7d9a51316b6da17499060778c6d0db; no Museum component/library or root
AGENTS delta was reported relative to the pinned frontend base 633e4fd5. The
isolated review branches preserve their recorded bases and unrelated work.

The exact eighteen approved WebPs total 9,787,776 bytes and are absent from the
existing CDN. Automatic approval review rejected their additive upload to that
public destination because it requires explicit approval naming the files and
destination. Zero files were uploaded. Review images were fulfilled locally in
the browser, including the ordinary Museum media-proxy requests. No expanded
archive, GitHub PR-ready/review-bot action, merge or deployment was attempted.

Remaining: obtain the specific eighteen-file CDN upload approval if requested,
then follow the ordinary source/publication integration process. No production
publication or final release qualification is asserted by these local captures.

Final handoff: source and frontend candidates remain uncommitted in their
isolated review branches. The final frontend checks passed: 11 display tests,
28 media tests, 28 graph tests, targeted lint and the recorded type checks.
The equivalent lint cleanup preserves the exact captured visible text.

## Display delivery activated — 5 November 2026

The user explicitly approved uploading the exact eighteen approved Salgado display WebPs to the existing public Museum CDN at d3lqz0a4bldqgf.cloudfront.net. This approval addressed the earlier automatic upload-review denial.

All eighteen files, totaling 9,787,776 bytes, were uploaded with conditional no-overwrite requests. Each passed S3 SHA-256 and delivery-header readback and a CDN HTTP 200 GET whose bytes matched the presentation manifest. The unchanged display-manifest SHA-256 is faf21bf83cf4d28efafce1d201df9057a64e1f1c22df8550e342567f10225b97. No cache invalidation was needed. A task-local receipt retains the per-file results and prior failed attempts.

The display files are live. The source and frontend candidates remain local and uncommitted; ordinary publication integration and release qualification remain pending. The current seven-page text was also requested for review in chat.

## Website release requested — 5 November 2026

The user approved this acquisition sentence: “The gift comprises four landscapes
and two photographs made in the Indigenous communities of Maronal and Nova
Esperança.” They requested removal of internal drafting notes and publication
through staging and production. The nine visitor manuscripts omit drafting
mastheads and publication-control tails. Each work has a short issuer-metadata
citation. No public correction history is asserted for these unpublished drafts.

Frontend e2ee8282afbecc578fd6666b784fdc304445d9a9 includes the narrow display
change and a normal merge of main c81953f0f986d7be6ac1d97280f8b0cb7bff448a.
The focused frontend suites pass (39 tests); source graph tests pass (51).
The optimized local build compiled, then encountered stale development-generated
route types. That task-owned cache was moved aside for a clean build retry.
Production-build visual qualification and PR/release checks remain pending.

Automatic approval review rejected a combined catalogue-preparation command
because it would reset review metadata on the existing Vera presentation
manifest and regenerate the full public graph. No such record mutation was
executed. A separate proposed metadata-only patch confirms that all non-review
payload/envelope fields would remain identical. It covers 368 earlier derived
records and the Vera review state; 56 Salgado projections are already pending.
The existing catalogue protocol requires one new exact-candidate review across
all 424 projections, plus its Vera review-only transition. Explicit approval of
that additional metadata renewal was requested. Neither live source activation
nor staging/production deployment has occurred. Prior denial is not bypassed.
