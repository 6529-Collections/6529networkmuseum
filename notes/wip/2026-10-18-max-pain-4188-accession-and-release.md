# MAX PAIN #4188/7394 accession and release

Status: active accession and release ledger
Opened: 2026-10-18
Branch: `max-pain-4188-accession`, rebased onto `a6bfc1c6` (the reviewed funding-assets policy release: A `9dd1c3e9`, B `17bb167c`, catalog C `7f3a0af0`, and the `6529NM-GOV-1282091` review, on `origin/main` `3926d78f`)
Constructor: `claude-code-task:max-pain-4188-accession-2026-10-18`
Construction and acceptance time (T_C): `2026-10-18T12:15:00Z` (moved from `2026-10-18T09:30:00Z`; see "Construction time" below)

## Mandate

Accession XCOPY, *MAX PAIN* #4188/7394, bought for the Museum through a
community-funded purchase authorized by the Museum Wave, as lot
`6529NM.2026.005`. Combine the contributor's submission (PR #72), the purchase
record model, and the evidence and media work; construct every record, entity,
media manifest, and public text; and finish with a review-pending candidate A.
Nothing here pushes, opens a pull request, uploads to the CDN, or posts.

## Owner decisions applied

- Identifiers follow the plan's recommended column, leaving room for draft
  PR #71 (Salgado, `.004`): lot `6529NM.2026.005`, object `.005.01`,
  certificate `6529NM-ACC-2026-005`, authorization `.AQA-01`, rights
  `.RIGHTS.01`, condition `.COND.01`, display authority `.DISPLAY-01`,
  decision `6529NM-GOV-1336667`, proposal `6529NM-PA-2026-001`, Work
  `6529NM-W-0036`, Artist `6529NM-ART-0025`, Project `6529NM-PRJ-0009`, media
  `6529NM-MED-0060` (token-linked GIF) and `6529NM-MED-0061` (poster), Curated
  Acquisition `6529NM-CA-2026-006`, Accession entity `6529NM-ACC-ENT-0005`,
  Work lifecycle observation `6529NM-W-OBS-0046`, acquisition observation
  `6529NM-CA-OBS-0007`, relations `6529NM-REL-0280` to `0287`. Register
  revision 6 (main's revision 5 plus this lot); identity inventories 1.8.0 and
  1.6.0 (main plus this change).
- Model: `ACQUISITION_AUTHORIZATION` for the purchase,
  `institutional_purchase_title_declaration` as the title instrument, a
  standalone `6529NM-GOV-1336667`, and the proposal record under
  `records/proposed-acquisitions/`. No Wave status observation is needed.
- Formal acceptance: on 2026-10-18 the owner directed that this accession
  proceed. The authorization records that direction as the Museum's
  institutional decision (`user_authorized_institutional_decision`) at T_C,
  one instant for creation, observation, effect, and acceptance, later than
  every evidence observation and computation on the branch (the latest
  reading is the supplementary package's at `2026-10-18T11:29:06.917Z`; the
  last evidence file change is the display addendum's summary text at about
  `2026-10-18T12:12:54Z`). **Merging the pull request that carries these
  records is the owner's confirmation of that decision.**
- Credit line: "XCOPY, *MAX PAIN #4188/7394*, 2022. Ethereum token
  `eip155:1/erc721:0xd1169e5349d1cb9941f3dcba135c8a4b9eacfdde/171000104188`.
  Acquired through a community-funded purchase organized by Shelby and
  authorized by the 6529 Network Museum Wave, 2026. CC0 1.0." The records'
  public credit names the organizer; the 25 contributor names appear only in
  the essay's credits list.
- Addresses: no contributor or payer address anywhere. The acquisition
  wallet's address appears only where machine records require it (title
  binding, custody path, the authorization's executing agent and receipts,
  the provenance schedule, the register receipt). Earlier private holders,
  the seller included, appear by address only in raw RPC evidence and the lot's
  provenance schedule; prose names them by role. To honor this rule, the
  authorization now records the seller by role and the validator joins it to
  the provenance schedule (commit `0183523f`).
- Rights: CC0 1.0 from the artist's Legal & Privacy page and the 1 August 2022
  announcement; all nine grants `granted`, AI training included, each basis
  carrying the non-endorsement condition; the Museum asserts no copyright; the
  token metadata carries no license. `docs/rights/registry.json` is unchanged.
- Display (revised after the independent reviews of the first candidate A;
  option (a) was decided on 2026-10-18): poster first; no autoplay; play on
  request after a warning that also says zooming in or screen magnification
  enlarges the flashing area; a visible, keyboard-operable stop that returns
  to the poster; only the poster, with no play control, under reduced motion;
  only SHA-256-verified bytes (the IPFS-addressed or Museum-retained GIF,
  never the Nifty Gateway URL); at most `min(512px, 100%)`, so that 200
  percent zoom stays within 1,024 pixels; and never enlarged or full screen
  (`not_permitted`). The rules are machine-readable in the presentation
  manifest, required by schema v3, and enforced by
  `generate_max_pain_media.py --check`, which also checks that `DISPLAY-01`
  states the warning, the control name, and the size rule. The flash analysis
  of all eight loop steps is addendum 01 of
  `evidence/xcopy-max-pain-4188-display/`, cited by `DISPLAY-01` and `COND.01`.
- State history uses source event times: offered `2026-08-24T10:51:34.091Z`,
  authorized `2026-08-27T18:30:18.491Z`, acquired `2026-09-02T13:17:35Z`,
  received on chain `2026-09-02T13:45:23Z`, accessioned T_C.
- Residual: the 0.068496911687069084 ETH is not part of the acquisition. The
  Museum has received the funds but has not accepted them, and has asked the
  organizer how they should be held. See
  `notes/wip/2026-10-18-max-pain-residual-funding.md`.

## Fixed identity and decision facts

- Museum Wave `5f207393-5418-4a75-8738-e40edb44a94d`; proposal serial
  `1336667`, drop `87e1fc3a-deef-4d1d-bf36-b2a44507f17b`, posted
  2026-08-24T10:51:34.091Z. Readback at `2026-10-18T09:06:14.742Z`:
  `drop_type` `WINNER`, place 1, decision time `2026-08-27T18:30:18.491Z`,
  rating 97,358,417 TDH, 25 raters; `is_signed` true as reported by the API,
  signature not verified. Votes cast by the decision time totaled
  101,689,216 TDH; the threshold of 69,000,000 TDH was first crossed at
  2026-08-26T08:11:13Z. Proposal-content SHA-256
  `04b55a28c990f66a14d469fad9a01dcba9bcf1dc8f85c462bc09f1443844e170`.
- Exact object: `eip155:1/erc721:0xd1169e5349d1cb9941f3dcba135c8a4b9eacfdde/171000104188`,
  token name "MAX PAIN #4188/7394", minted 2022-03-24T23:39:21Z in transaction
  `0x0b2da2a60e43772a73dc49383ca40da2d46ecf6ee9ba1669727aa03a78f3e6f8`.
- Image: animated GIF, 4,000 × 4,000 pixels, eight frames of 50 ms, looping
  without end, 4,541,937 bytes, SHA-256
  `3ba2c6c6a7b7da940b5780da8fe301e61366a0b5c738be16e537ee122630be2e`,
  recomputed CIDv0 equal to the metadata `image_hash`
  `QmTcTzTPgCyvF933oeFvB4GkPgaXtF6dKuQgvg32qqLYGF`.

## Purchase and receipt

- Purchase: transaction
  `0xdf8b07004bfed397920355ac80991a9dd592c896ca77b1fadb5655f8c85aa4d6`, block
  25,889,852, 2026-09-02T13:17:35Z, Seaport 1.6, 0.4589999999 ETH from the
  organizer's acquisition wallet, Transfer log 407 from an earlier private
  holder to the wallet.
- Museum receipt: transaction
  `0xe7511598bbdabd1d4ff1c5bb7e6d1f9157a413fbcf305f0392cc30c92252ea03`, block
  25,889,990, 2026-09-02T13:45:23Z, Transfer log 955 from the wallet to
  `networkmuseum.6529.eth` (`0xbECfa2bA5a782D11E1a0e821E8F2e30b6684178c`).
  This is the object's `acquisition_transaction` and the title binding's
  transfer.
- Finalized custody: block 26,218,064, hash
  `0xfaa4f2991b8c1ff2aee75bf889a15b72913e6ee98e967b5c762ed4bb4d8051c7`;
  `ownerOf` equals the Safe on two providers, `getApproved` is zero, and the
  ENS name resolves to the Safe at the same block.

## Release quality contract

The package meets the accession, record-model, Stream-interoperability,
curatorial-publication, public-experience, and digital-art-stewardship
standards: separate authorization, title, custody, rights, condition,
preservation, display, and evidence records; CAIP-19 identity; claim-level
citations with evidence classes; reviewed alt text and a long description;
first-frame posters with fixity; a retained source GIF; append-only history;
and a public-safe boundary with no contributor or payer addresses.

## Evidence packages

| Package | Finalized block | Manifest SHA-256 |
|---|---|---|
| `evidence/xcopy-max-pain-4188-custody/` | 26,218,064 | `2cdaaf516ab62a12df4d035f76a415106720b5e089fa43918dba879bcd8f6939` |
| `evidence/xcopy-max-pain-4188-sources/` | 26,218,096 | `ff761f2f629ea6c71a85fffc4b63e431fb03531e1f2ec7d9b10f60d0368134c0` |
| `evidence/xcopy-max-pain-4188-technical/` | 26,218,159 | `d803c643defb441f274adb9d8532833493525fbad4949e54f98aeadbcb1187cf` |
| `evidence/xcopy-max-pain-4188-funding/` | 26,218,159 | `b60acf8412c30ade51a723187a131b6c721b2facb02799ccf72116f45e1d0767` |
| `evidence/xcopy-max-pain-4188-display/` | not applicable | `a96565fd2b3180e61400f3a4c5a1b7d0003e05c9a1e5f8ae4aa0424171b2cced` |
| `evidence/xcopy-max-pain-4188-supplement/` | 26,218,989 | `8a13dcffa87b4781b0a1e131356dd81cb97a1cbd331e4081f319444f0fcf1e5b` |
| `evidence/waves/museum-wave-governance-2026-10-18-max-pain-4188/` | not applicable | `e47bc89ceb6838ae318d85f694b08d852188a12b7e226f47a86fac16f4db1abc` |

The flash analysis was re-run from the retained GIF and masks on 2026-10-18;
`flash-analysis.json`, the three masks, and
`flash-windows-presentation-widths.json` reproduced byte for byte. Addendum
01 (`flash-analysis-all-steps.json` and `close-looking-census.json`) was
re-run from its retained method files on the retained GIF and also reproduced
byte for byte. The technical package's manifest changed only because its
derived burn attribution now names private burn callers by role (see "Review
fixes" below); no reading changed.

## Commits

Commits after `a6bfc1c6`, in order (hashes after the rebase):

1. `ea1e4b77` contributor submission (author sonoflasg, from `5d241715`).
2. `2bd9660f`, `b291a549`, `e0a9ec21`, `73e57546`, `1f2721dd`: purchase record
   model and publication table (from `c4e22ce9`, `53059563`, `baf20f9a`,
   `ff2306c7`, `7c644f2d`).
3. `01f57fca`, `f2716cb4`, `55f97bfb`, `94ebaf66`, `683459a4`, `4fdac396`,
   `e1724c32`: GIF evidence, evidence packages, and media v3 (from `118b831b`,
   `7c47c340`, `5fbf1c12`, `64ebf9a5`, `4916ac3b`, `8a13d5f0`, `ee4f358d`).
   Generated outputs that conflicted were regenerated; `.gitattributes` was
   resolved as the union of both blocks.
4. `16633403` Casey package root inventory rebound to the GIF-aware bootstrap
   validator (repository generator).
5. `0183523f` purchase seller recorded by role and joined to the provenance
   schedule.
6. `1087dc9c`, `17f0c2b4`, `8ebb7005`: construction commits for the
   governance decision and proposal record; the display evidence, accession
   records, manuscripts, register, and finalizer; and the graph code,
   inventories, publication unit, tests, CI, documentation, and notes.
7. The evidence-discipline commit (funding note and Museum note; see
   "Rebase and evidence discipline" below).
8. Review-fix commits after the first candidate A (see "Review fixes" below):
   the supplementary evidence, display addendum, and technical relabel; the
   display, schema, and catalog code; the purchase-lot validator; the
   manuscripts and records; and the promotion of the contributor's
   submission, which removes `notes/wip/max-pain-4188-staging/`.
9. Candidate A, the final commit (see below).

Construction commits carry hand-authored sources only. Every generated output
(the public entity graph, the re-pended Vera records and manifest, the MAX PAIN
presentation manifest, the publication inventory and bundle, and the release
manifest) is regenerated in candidate A, so the construction commits are not
individually valid; candidate A is.

## Candidate A, reviewed B, and catalog C

Candidate A is review-pending and not publishable. B requires an independent
reviewer, not the constructor, to review the exact candidate A commit: the
records, the evidence packages, the manuscripts (including the signed essay),
the graph, the posters, and the display constraints. The review time must be
later than every `created_at`; the latest is T_C, `2026-10-18T12:15:00Z`.

B is the single-parent child of A, produced only by:

```
python scripts/migrate_public_entities.py --reviewed --reviewer-id <id> --reviewed-at <ts> --reviewed-commit <A> --reviewed-manifest-sha256 <A sha256> --reviewed-manifest-keccak <A keccak>
python scripts/finalize_vera_accession.py --reviewed (same five arguments)
python scripts/finalize_max_pain_accession.py --reviewed (same five arguments)
python scripts/generate_vera_molnar_media.py --promote-reviewed --reviewer-id <id> --reviewed-at <ts> --reviewed-commit <A>
python scripts/generate_max_pain_media.py --promote-reviewed --reviewer-id <id> --reviewed-at <ts> --reviewed-commit <A>
python scripts/generate_public_publication_bundle.py
python scripts/generate_manifest.py
```

B may change only the graph records, the two accessions' direct records, the
two presentation manifests, the bundle, and the release manifest. In the MAX
PAIN presentation manifest, `--promote-reviewed` also records the flash
review's outcome: `max_css_width_status` becomes `confirmed_by_flash_review`
and the display `basis` takes the generator's pinned reviewed wording. The
publication-catalog check admits exactly that change from A to B. Notes, the
index, `6529NM-GOV-1336667`, and `6529NM-PA-2026-001` do not change in B;
`finalize_max_pain_accession.py` re-seals the decision and proposal records
without changing their review state.

C contains exactly `release-artifacts/catalog/6529NM-PUBCAT-<B>.json` and
`release-artifacts/latest/publication-catalog-pointer.json`:

```
python scripts/build_publication_catalog.py --write-release --commit <B> --created-at <ts> --actor <release actor> --activated-at <ts>
python scripts/build_publication_catalog.py --check --commit <B> --created-at <ts>
python scripts/build_publication_catalog.py --check-transition --previous-commit <main head before this PR> --current-commit <C>
```

The decision record's review and the ledger updates follow C in separate
commits.

## Regenerating candidate A after rebasing

The funding-assets policy PR's own B and C land first. This branch is then
rebased onto that main: replay every commit except candidate A (for example
`git rebase --onto <new main> <old base> <A>~1`), resolving conflicts in
generated files by regeneration and in `INDEX.md`, the roadmap, and the
orchestration ledger by keeping both sides. Then regenerate candidate A from
the repository root, in this order:

```
python scripts/build_casey_package_manifest.py --source-snapshot-commit 820f4bb6999fb9df3b094692913d70ebf6d9dc63 --acquisition-commit 48cd2fbf2914d295cdc4260dedb1345061f5e3b6
python scripts/migrate_public_entities.py
python scripts/finalize_vera_accession.py --pending
git show 3eab50914a90c079fe0383624e760fc0a954e709:records/accessions/6529NM.2026.003/public/presentation-manifest.json > records/accessions/6529NM.2026.003/public/presentation-manifest.json
python scripts/finalize_max_pain_accession.py --pending
python scripts/generate_max_pain_media.py --work-entity-id 6529NM-W-0036 --media-reference-entity-id 6529NM-MED-0061 --animation-media-reference-entity-id 6529NM-MED-0060 --generated-at 2026-10-18T12:15:00Z --actor-id claude-code-task:max-pain-4188-accession-2026-10-18
python scripts/generate_public_publication_inventory.py
python scripts/generate_public_publication_bundle.py
python scripts/generate_manifest.py
```

The first command matters only if `scripts/bootstrap_validate.py` changed
again; it is a no-op otherwise. Run the full validation set (bootstrap,
`validate.py`, `validate_full_with_casey.py`, replay with
`--check-existing-review-state`, inventory, bundle, manifest, media, both
finalizer checks, rights, Casey, corpus, link and Unicode checks, the
publication-catalog check, the complete unit suite with `STREAM_SOURCE_ROOT`,
and `git diff --check`), then commit A alone and record its manifest
commitments here and in the pull request.

## Open items

- Before publication: record the contributor's and the organizer's approval
  of the revised essay
  (`records/accessions/6529NM.2026.005/public/community-funded-acquisition.md`,
  the coordinator's v3 text), and its date, in the essay's publication
  details. The text differs from the version the organizer approved on
  26 September.
- The organizer's answer on the residual funds, then the owner's choice among
  the options in the residual note.
- Owner authorization for the CDN upload of the three posters, followed by an
  HTTP readback (status 200, size, SHA-256, `image/webp`, and
  `public, max-age=31536000, immutable`) recorded after C.
- Re-read on x.com every X post the manuscripts cite (they were read through
  public mirrors): the organizer's post of 7 September 2026, XCOPY's posts of
  1 August 2022 (the *Sunshine* post, its parent, and the CC0 post),
  15 December 2023, 11 February 2024, 21 March 2024, and 28 July 2024, and
  Nifty Gateway's post of 21 March 2022.
- The independent flash review of the 512-pixel limit, recorded in B as
  `confirmed_by_flash_review`.
- Writer notes still open: the variant-edition token counts on the
  ranked-auctions contract; confirmation of the Sotheby's lot wording; and the
  curatorial standard's section 13 apparatus (bibliography, revision history,
  immutable edition link) for the long texts. The Nifty Gateway closure notice
  (in the source package), the organizer's Wave messages, and the Tumblr
  listing (in the supplementary package) are now retained.
- Review of `6529NM-GOV-1336667` after C, and reconciliation with draft PR #71
  (Salgado) whichever merges second.

## Rebase and evidence discipline

The funding-assets policy release is final on branch
`museum-funding-assets-policy` at `a6bfc1c6`: its governance commit was
amended to `748b756b`, candidate A `9dd1c3e9` was approved at
`2026-10-18T09:39:49Z`, reviewed B `17bb167c` and catalog C `7f3a0af0`
activate `6529NM-PUBCAT-17bb167cc948666e527feb2ffb7287de980cbb42`, and
`a6bfc1c6` records the review of `6529NM-GOV-1282091`.

This branch was rebased with `git rebase --onto a6bfc1c6 68147b6c`, after the
first candidate A (`d8b86894`, which the three independent reviews were
reading) was dropped; that commit stays reachable at the local branch
`max-pain-4188-accession-candidate-a1`. Authorship was kept. Conflicts:

- the release manifest in eight replayed commits, and the visitor bundle in
  one, were resolved by regenerating with `generate_public_publication_bundle.py`
  and `generate_manifest.py` (never by hand);
- `INDEX.md`, `docs/implementation-roadmap.md`, and
  `notes/wip/orchestration-ledger.md` in the graph-and-ledgers commit were
  resolved by keeping the base's text first (its reviewed
  `6529NM-GOV-1282091` and adoption-ledger rows and its release-checkpoint
  entries) and appending this branch's new rows and entries.

Two evidence-discipline fixes followed, so that public notes cite only
committed evidence:

- the essay's funding note and the chronology's funding row now give the
  committed balance readings (0.4646 ETH before the purchase, 0.063 ETH after
  the transfer to the Museum, 0.5276 ETH in total;
  `evidence/xcopy-max-pain-4188-funding/`) and the organizer's 28 August call,
  replacing the unretained per-transfer counts;
- the essay's Museum note no longer states that the Museum's wallet held no
  XCOPY before this token. It reads "No XCOPY appears in the Museum's earlier
  accessions.", and its note cites only accession register lots
  `6529NM.2026.001` to `6529NM.2026.003`. The chronology's 7 September row and
  its note 16 drop the same unretained Safe-history reading.

The residual note no longer calls the 0.063 ETH "three shares".

## Review fixes after the first candidate A

Three independent reviews of the first candidate A (`d8b86894`) returned
changes required: registrar and technical, curatorial and editorial, and
accessibility and media. Their required items, and the advisories the
coordinator adopted, were applied on top of the rebased branch before
candidate A was regenerated.

- **Essay.** `community-funded-acquisition.md` is the coordinator's v3 text,
  verbatim except that each integration placeholder now cites committed
  evidence. Its publication-details placeholder is the first open item above,
  not visible text.
- **Supplementary evidence.** `scripts/acquire_max_pain_supplementary_evidence.py`
  wrote `evidence/xcopy-max-pain-4188-supplement/` keylessly through
  `safe_fetch` (observed `2026-10-18T11:09:35.789Z`, target block 26,218,989):
  edition 3265's transfer to the strategy contract and its burn, with the
  seller of edition 4188 matched by role; the 21 mint transactions; the
  *DAMAGE CONTROL* contract's `owner()`, creation receipt (located through
  Blockscout, class D), ENS names, `uri(1..10)`, and metadata; the variant
  contract's `name()`; an address-free redemption table from a complete burn
  scan, every burn transaction's calldata, and the ten burn-redeem
  configurations (2,547 burns; 2,545 through the extension in 2,139
  transactions; 2,283 redemptions; 1,215 distinct accounts, as a count only;
  1,429 burns through block 19,482,931, the last block before XCOPY's post of
  21 March 2024), with the sorted burn transaction-hash list and its SHA-256;
  The Memes card 47 as a public-safe projection; the earliest Tumblr post; the
  creator-profile "Warning: flashing imagery" from the same Wayback bytes as
  the drop-page capture; and public-safe projections of the organizer's Wave
  messages of 28 August, 2 September, and 14 September 2026, with member
  mentions, three payment-status names, and the acquisition wallet address
  omitted from the transcripts and the exact part text committed by SHA-256.
  No organizer message of 9 September about the residual exists in the Wave;
  the residual note no longer claims one, or any participant's preference.
- **Technical package.** Derived burn attribution names the two
  self-addressed callers (EIP-7702-delegated accounts) by role; their
  addresses remain only in the two raw sample receipts.
- **Display.** Addendum 01 measures all eight loop steps under the committed
  definition and the stricter every-transition reading at 512 to 4,000 pixels
  with landscape and portrait fields; the largest share is 15.3 percent at
  512 pixels and 24.9 percent at 1,024 pixels (512 at 200 percent zoom). The
  cap, reduced-motion rule, stop control, verified-bytes rule, final
  `not_permitted` value, warning text, and "20 color changes a second (10 full
  cycles)" wording are applied across the generator, schema v3, the
  presentation manifest, `DISPLAY-01`, the object entry, `COND.01`, the alt
  text, the certificate, the statement, the authorization's blocker, the
  register, and the roadmap.
- **Registrar.** `docs/control-plane.md` describes the GIF raw-evidence
  profile. `validate.py` requires every purchase custody receipt to deliver to
  the lot's Museum custody address and every purchase register lot to agree
  with its authorization (identifiers, object count, certificate, credit,
  consideration, receipt, and custody), with tests.
- **Curatorial.** The object entry, artist and project essays, chronology, alt
  text, display authority, authorization and certificate texts, Wave
  resolution, current view, and roadmap carry the reviewers' corrections.
  The close-looking figures cite `close-looking-census.json`.
- **Contributor submission.** A dedicated commit promotes the contributor's
  submission into the accession and removes `notes/wip/max-pain-4188-staging/`.
  The submission's original text is preserved unchanged in the contributor's
  commit, `777ac81c` before the rebase and `ea1e4b77` on this branch.
- **Timing.** The supplementary readings, the display addendum, and the
  technical relabel were made after the first T_C, `2026-10-18T09:30:00Z`.
  T_C therefore moved (see "Construction time" below).

## Construction time

A formal acceptance must not cite evidence observed after it, so on
2026-10-18 the coordinator moved T_C from `2026-10-18T09:30:00Z` to a single
instant after every evidence observation and computation on the branch:
`2026-10-18T12:15:00Z`. The latest evidence events it follows are the
supplementary package's last read (`2026-10-18T11:29:06.917Z`), the display
addendum's computations (`11:17:40Z` and `11:20:37Z`), the technical relabel
(about `11:33Z`), and the correction of the addendum summary's text (about
`12:12:54Z`, committed `12:13:11Z`). T_C is the created, observed, effective,
acceptance, and accession time of the six direct records, the decision and
proposal records' construction time, the register snapshot and revision
time, the `accessioned` state, the graph records' time, the presentation
manifest's generation time, and the accession time stated in the
authorization text and the chronology.
