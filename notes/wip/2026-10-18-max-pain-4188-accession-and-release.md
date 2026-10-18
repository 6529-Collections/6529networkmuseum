# MAX PAIN #4188/7394 accession and release

Status: active accession and release ledger
Opened: 2026-10-18
Branch: `max-pain-4188-accession`, from `68147b6c` (the funding-assets policy record commit, on `origin/main` `3926d78f`)
Constructor: `claude-code-task:max-pain-4188-accession-2026-10-18`
Construction and acceptance time (T_C): `2026-10-18T09:30:00Z`

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
  every evidence observation (the latest is the governance readback at
  `2026-10-18T09:06:14.745Z`). **Merging the pull request that carries these
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
  the provenance schedule (commit `8be62000`).
- Rights: CC0 1.0 from the artist's Legal & Privacy page and the 1 August 2022
  announcement; all nine grants `granted`, AI training included, each basis
  carrying the non-endorsement condition; the Museum asserts no copyright; the
  token metadata carries no licence. `docs/rights/registry.json` is unchanged.
- Display: poster first, no autoplay, animation on request after a warning,
  poster only under reduced motion, animation at most 768 CSS pixels, no
  enlarged or full-screen animation until a flash review. The flash analysis
  is retained in `evidence/xcopy-max-pain-4188-display/` and cited by
  `DISPLAY-01` and `COND.01`.
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
| `evidence/xcopy-max-pain-4188-technical/` | 26,218,159 | `86da1fd74420031e3d8ef39ec360af7afb7333cb337538d097d62196f9605bd2` |
| `evidence/xcopy-max-pain-4188-funding/` | 26,218,159 | `b60acf8412c30ade51a723187a131b6c721b2facb02799ccf72116f45e1d0767` |
| `evidence/xcopy-max-pain-4188-display/` | not applicable | `a242565af5b81b8299ee73641a0907a0620e73f1a47e450e0de66659ed7ef2d0` |
| `evidence/waves/museum-wave-governance-2026-10-18-max-pain-4188/` | not applicable | `e47bc89ceb6838ae318d85f694b08d852188a12b7e226f47a86fac16f4db1abc` |

The flash analysis was re-run from the retained GIF and masks on 2026-10-18;
`flash-analysis.json`, the three masks, and
`flash-windows-presentation-widths.json` reproduced byte for byte.

## Commits

1. `777ac81c` contributor submission (author sonoflasg, from `5d241715`).
2. Purchase record model and publication table (from `c4e22ce9`, `53059563`,
   `baf20f9a`, `ff2306c7`, `7c644f2d`).
3. GIF evidence, evidence packages, and media v3 (from `118b831b`,
   `7c47c340`, `5fbf1c12`, `64ebf9a5`, `4916ac3b`, `8a13d5f0`, `ee4f358d`).
   Generated outputs that conflicted were regenerated; `.gitattributes` was
   resolved as the union of both blocks.
4. `87733619` Casey package root inventory rebound to the GIF-aware bootstrap
   validator (repository generator).
5. `8be62000` purchase seller recorded by role and joined to the provenance
   schedule.
6. Construction commits for the governance decision, proposal record, display
   evidence, accession records, manuscripts, register, graph code, inventories,
   tests, CI, documentation, and notes.
7. Candidate A, the final commit (see below).

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
later than every `created_at`; the latest is T_C, `2026-10-18T09:30:00Z`.

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
two presentation manifests, the bundle, and the release manifest. Notes, the
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
`git rebase --onto <new main> 68147b6c <A>~1`), resolving conflicts in
generated files by regeneration and in `INDEX.md`, the roadmap, and the
orchestration ledger by keeping both sides. Then regenerate candidate A from
the repository root, in this order:

```
python scripts/build_casey_package_manifest.py --source-snapshot-commit 820f4bb6999fb9df3b094692913d70ebf6d9dc63 --acquisition-commit 48cd2fbf2914d295cdc4260dedb1345061f5e3b6
python scripts/migrate_public_entities.py
python scripts/finalize_vera_accession.py --pending
git show 3eab50914a90c079fe0383624e760fc0a954e709:records/accessions/6529NM.2026.003/public/presentation-manifest.json > records/accessions/6529NM.2026.003/public/presentation-manifest.json
python scripts/finalize_max_pain_accession.py --pending
python scripts/generate_max_pain_media.py --work-entity-id 6529NM-W-0036 --media-reference-entity-id 6529NM-MED-0061 --animation-media-reference-entity-id 6529NM-MED-0060 --generated-at 2026-10-18T09:30:00Z --actor-id claude-code-task:max-pain-4188-accession-2026-10-18
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

- Contributor and organizer review of the revised essay
  (`records/accessions/6529NM.2026.005/public/community-funded-acquisition.md`),
  which differs from the text the organizer approved on 26 September.
- The organizer's answer on the residual funds, then the owner's choice among
  the options in the residual note.
- Owner authorization for the CDN upload of the three posters, followed by an
  HTTP readback (status 200, size, SHA-256, `image/webp`, and
  `public, max-age=31536000, immutable`) recorded after C.
- Re-read on x.com every X post the manuscripts cite (they were read through
  public mirrors): the organizer's post of 7 September 2026, XCOPY's posts of
  1 August 2022, 15 December 2023, 11 February 2024, 21 March 2024, and
  28 July 2024, and Nifty Gateway's post of 21 March 2022.
- An independent flash review of the 768-pixel limit and the prohibition on
  enlarged animation.
- Writer notes still open: captures of the Nifty Gateway closure notice, the
  Wave chat messages of 28 August and 14 September, and the Tumblr API
  response; the variant-edition token counts on the ranked-auctions contract;
  confirmation of the Sotheby's lot wording; and the curatorial standard's
  section 13 apparatus (bibliography, revision history, immutable edition
  link) for the long texts.
- Counts that rest on unretained readings: the 24 inbound payments and the
  Museum Safe's NFT history to block 26,217,714 come from the chain agent's
  indexer-assisted reading, not from a retained package; the funding package
  retains aggregates only.
- Review of `6529NM-GOV-1336667` after C, and reconciliation with draft PR #71
  (Salgado) whichever merges second.
