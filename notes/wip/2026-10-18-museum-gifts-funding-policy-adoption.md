# Museum gifts, acquisition programs, and funding assets policy adoption

Status: active governance and release ledger
Opened: 2026-10-18
Branch: `museum-funding-assets-policy`, from `origin/main` `3926d78f`

## Scope

This change records the Museum Wave's adoption of proposal serial `1282091`
as policy `6529NM-POL-004` and governance decision `6529NM-GOV-1282091`. It
lands before the MAX PAIN accession, which will cite this decision. It does not
accept, acquire, or accession any work, accept any funding, activate a
publication catalog, change the frontend, or post to the Wave.

## Live readback

An unauthenticated `GET https://api.6529.io/api/drops/6387c484-c602-4a2f-8d8b-456395cf077f`
through `scripts/safe_fetch.py` at `2026-10-18T08:28:48.748Z` returned:

| Field | Value |
|---|---|
| Wave | `5f207393-5418-4a75-8738-e40edb44a94d` (6529 Network Museum) |
| Serial | `1282091` |
| Title | Museum Gifts, Acquisition Programs, and Funding Assets Policy |
| `drop_type` | `WINNER` |
| `is_signed` | `true`, as reported by the API; the signature was not verified |
| `created_at` | `2026-08-08T09:43:48.737Z` |
| `winning_context.decision_time` | `2026-08-10T09:55:07.644Z` |
| `rating` and `realtime_rating` | `109,017,036` |
| `raters_count` | `21` |
| Parts | one text part |

The decision record takes its effective time from `decision_time`. The rating
is recorded as observed and is not the basis of the adoption finding; the live
`drop_type` is.

## Content-hash verification

The publication receipt recorded SHA-256
`ce4962072ddd0cbfacb7a071be51ae779c4cae40410851e6386e49ca405becb2`.

- **Input hashed:** the UTF-8 encoding of the string `parts[0].content`
  after JSON decoding of the API response. It is 16,289 bytes and 16,289
  UTF-16 code units, all ASCII, with no trailing newline. These exact bytes
  are retained as
  `parts/drop-6387c484-c602-4a2f-8d8b-456395cf077f-part-1.txt`, so the
  digest can be recomputed from the repository.
- **Result:** `ce4962072ddd0cbfacb7a071be51ae779c4cae40410851e6386e49ca405becb2`,
  equal to the receipt's publication and readback digests.
- **Source note:** the repository source file
  `2026-08-08-museum-gifts-acquisition-programs-and-funding-assets-policy.md`,
  with CRLF normalized to LF and surrounding whitespace trimmed, is identical
  to the API string.
- **Raw response:** the response body was 23,298 bytes with SHA-256
  `dca35591285cef958570c8a3618480ec22efabf890ef80a199afd93987ce1f47`. It is
  not retained (see below). This digest covers the whole JSON response,
  including profile fields that change over time, so it is a transport
  observation and not the proposal-content digest.

The policy file reproduces the content with one metadata block inserted after
the title line. `tests/test_museum_gifts_funding_policy.py` rebuilds the API
string from the policy file and checks the digest, the evidence package, and
the decision record.

## Earlier proposals replaced by Section 15

- **Serial `1281404`**, *Gift-Specific TDH Approval for Every Museum Gift*,
  drop `a991d0b2-4c57-4ae1-b3b1-0680a4772998`. The repository records its
  publication on 2026-08-07 as `PARTICIPATORY`, 14 raters and a rating of
  34,387,666 immediately before withdrawal, and deletion at
  `2026-08-08T09:02:02.862Z` on the owner's authorization. It was never
  observed as `WINNER`. The 2026-10-18 readback returned HTTP 404 with an
  `error` body stating that the drop was not found.
- **Serial `1282040`**, the first integrated draft, drop
  `401bdae4-1da7-41d0-aeef-73b1da78b39d`, was withdrawn with zero raters.
  The 2026-10-18 readback returned HTTP 404.

Neither proposal had an adopted effect. Section 15 of the adopted policy
replaces both in full.

## Evidence retention

The owner's privacy direction for these pull requests is that no voter wallet
addresses are committed. A drops-API response carries the author profile
and, for a rated drop, the `top_raters` profiles, each with a wallet address.
The package therefore follows the Magnum public-safe Wave receipt convention
(`records/proposed-gifts/6529NM-PG-2026-001/evidence/wave-publication-observation-public-safe-2026-08-09.json`)
for any response that contains profile objects:

- `projections/drop-6387c484-c602-4a2f-8d8b-456395cf077f.json` keeps an
  allowlisted payload (drop identity, Wave, status, `is_signed`, rating fields,
  creation and decision times, and per-part digests), its `payload_sha256`
  under the stated canonicalization, an exclusion note, and the SHA-256, size,
  and HTTP status of the response bytes that were not retained;
- `parts/drop-6387c484-c602-4a2f-8d8b-456395cf077f-part-1.txt` keeps the exact
  part text;
- `summary.json` keeps the transport observation for every request, including
  the raw byte length and SHA-256.

The two HTTP 404 bodies contain no profile objects and are retained
byte-for-byte under `raw/`. The acquisition script decides retention per
response and refuses to write a projection that contains a profile key or a
wallet-shaped value. The only `0x` addresses in the package are the USDC and
USDT token contracts named in the policy text.

`.gitattributes` marks `raw/**` and `parts/**` in this package as binary. The
generated projection, `summary.json`, and `manifest.json` remain LF text.

## Record design

- `records/governance/decisions.json` is unchanged. Bootstrap validation binds
  it to the 2026-08-01 proposal snapshot, row for row.
- `records/governance/6529NM-GOV-1282091.json` is a standalone
  `GOVERNANCE_DECISION` envelope record. It references the Donation Acceptance
  Policy decision and the four collection preapprovals named in Section 14.
- The record is review-pending, with no reviewer.

## Publication boundary

Every `policies/*.md` file belongs to the visitor publication inventory as an
`open_and_founding_required_paths` source, so the new policy adds one
inventory entry and its text enters the visitor bundle. The decision record
belongs to the release manifest only. The evidence package belongs to neither.
Visitors see the policy only after a reviewed catalog activates it.

## Open items

- `records/collections/approved-collections.json` still states that
  preapproval removes collection-specific pre-authorization. Under Sections 3
  and 14, preapproval is a collection-level eligibility finding and each art
  gift needs an exact-gift vote. The register needs an append-only amendment.
- `docs/proposed-gift-wave-standard.md` still describes the exact-gift rule
  for preapproved collections as a pending amendment.
- The public entity graph cites `6529NM-GOV-1052156` and
  `6529NM-GOV-1052812` as the gift pathway's authority. Adding
  `6529NM-GOV-1282091` is a separate graph change.
- The frontend has not been checked for rendering a fourth policy document.

## Candidate A checkpoint

The branch's second commit is publication candidate A. It is review-pending
and is not publishable. It differs from the governance commit only in review
state and in the regenerated bundle and release manifest:

- `python scripts/migrate_public_entities.py` regenerated the 370 public graph
  records (136 entities, 233 relations, and the 2026-08-08 Wave status
  observation) as review-pending.
- `python scripts/finalize_vera_accession.py --pending` returned the seven Vera
  direct records (six accession records and the `6529NM-PG-2026-002` Wave
  status observation) to review-pending.
- The Vera presentation manifest returned to `constructed`, with delivery
  status `prepared_for_contextual_museum_display_pending_review`. Its bytes
  equal the version in Vera candidate A
  `3eab50914a90c079fe0383624e760fc0a954e709`.
- In those 377 records only review fields, `entity_status`,
  `status_observation.status_label`, payload commitments, and envelope content
  hashes changed. The publication inventory is unchanged from the governance
  commit.
- Candidate A release manifest: SHA-256
  `sha256:74eea95ef31da7f314f1d1d9935b2e4d0775010dde8ceab0205c27918dcdd866`,
  Keccak `0x64a95512f8901579e36a6d443e534e6335dcf04cb75c2916115a003c7b30cc02`.

Bootstrap and full validators, deterministic replay, inventory, bundle,
manifest, media, rights, Casey, Vera, Magnum corpus, link, and Unicode checks,
and the complete test suite pass on this state.

## Reviewed B requirements

1. An independent reviewer, not the constructor, reviews the exact candidate A
   commit: the policy transcription against the retained part text, the
   projection and its privacy boundary, the decision record, the evidence
   package and script, the notes, and the unchanged content of the re-pended
   graph.
2. The review time must be later than every record's `created_at`; the latest
   is the decision record's `2026-10-18T08:30:00Z`. One reviewer panel and one
   review time cover all 377 records.
3. B is the single-parent child of A. It is produced only by:
   `migrate_public_entities.py --reviewed` and
   `finalize_vera_accession.py --reviewed`, each with `--reviewer-id`,
   `--reviewed-at`, `--reviewed-commit <A>`, `--reviewed-manifest-sha256`, and
   `--reviewed-manifest-keccak` set to the candidate A values above;
   `generate_vera_molnar_media.py --promote-reviewed` with the reviewer ID,
   time, and A commit; then `generate_public_publication_bundle.py` and
   `generate_manifest.py`.
4. B may change only those 377 records, the Vera presentation manifest, the
   bundle, the inventory, and the release manifest. Notes, the index, and
   `6529NM-GOV-1282091` cannot change in B.

## Catalog C requirements

- `python scripts/build_publication_catalog.py --write-release --commit <B>
  --created-at <time> --actor <release actor> --activated-at <time>`.
- C contains exactly `release-artifacts/catalog/6529NM-PUBCAT-<B>.json` and
  `release-artifacts/latest/publication-catalog-pointer.json`.
- Verify with `--check --commit <B> --created-at <time>` and
  `--check-transition --previous-commit 3926d78faacf67a62b8d9b48e15d26c43b52eae9
  --current-commit <C>`.
- Ledger updates and the decision record's reviewer binding follow C in a
  separate commit.

## Release record

- **Candidate A:** `9dd1c3e9ae7c0d8c77071b0b109a2cdc9bb7095f`, with
  manifest SHA-256
  `sha256:74eea95ef31da7f314f1d1d9935b2e4d0775010dde8ceab0205c27918dcdd866`
  and Keccak
  `0x64a95512f8901579e36a6d443e534e6335dcf04cb75c2916115a003c7b30cc02`.
- **Independent review:**
  - `claude-reviewer:museum-governance-2026-10-18-independent` approved
    candidate A at `2026-10-18T09:39:49Z`, bound to the commit and manifest
    commitments above.
  - An earlier review of a superseded candidate required three corrections.
    Two concerned the decision record's restatement of Sections 7 and 8; the
    third concerned the index description of the evidence. They were applied
    to the governance commit before the approved candidate was built.
- **Reviewed B:** `17bb167cc948666e527feb2ffb7287de980cbb42`, the single
  child of A. Its 380 changed files are the 377 records, the Vera
  presentation manifest, the bundle, and the release manifest. The inventory
  is unchanged. Release manifest SHA-256:
  `sha256:f83e6bdbde83b1c3e8963b3908b15e034b4df3f9fa7f90fef72b03caef8a1046`;
  Keccak:
  `0xa9df943dd3d48d6ba49c268ea62eefbb51baeb1934281349b718fd6635155b9e`.
- **Catalog C:** `7f3a0af033b9fa1f82800e44cf809c6999422523`.
  - It adds `release-artifacts/catalog/6529NM-PUBCAT-17bb167cc948666e527feb2ffb7287de980cbb42.json`
    and updates the pointer. Nothing else changes.
  - The prior catalog was
    `6529NM-PUBCAT-92966f2836ebf2af06edfe0fe2cff25041307c92`.
  - Created and activated at `2026-10-18T09:54:00.000Z`.
  - Catalog file SHA-256:
    `sha256:ef50f1231c0ede1400ba934e688a283327ec68953a8ee6fba34f62ca2186558e`.
    Envelope content hash:
    `0x16f7ba7483b3d75ec620b378900049303b11d4d2d6cc2e7305b9aec7359d1c31`.
  - The activation actor is
    `release-activator:claude-code-museum-funding-assets-policy-2026-10-18`.
    It follows the `release-activator:` convention of the 2026-08-09 to
    2026-08-12 activations. The activation was made on the instruction of the
    coordinating session acting for the owner.
- **Checks:**
  - `build_publication_catalog.py --check --commit <B> --created-at <time>`
    passes.
  - `--check-transition --previous-commit 3926d78faacf67a62b8d9b48e15d26c43b52eae9
    --current-commit <C>` passes.
  - The full validation set passes at A, B, and C.
- **After C:** the next commit applies the same review binding to
  `6529NM-GOV-1282091`, which the transition rules do not allow B to change,
  and records these hashes. It touches no catalog path, so the transition
  check treats it as a non-catalog step.
- **Not done:** push, pull request, frontend binding, CDN, and deployment.
  The catalog's immutable URLs name commit B. As in earlier squash-merged
  releases, B must stay reachable on GitHub after merge.
