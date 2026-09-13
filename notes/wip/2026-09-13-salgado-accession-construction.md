# Salgado accession construction — 13 September 2026

Status: construction in progress. Constructor: Codex, task
`01a087a1-5e64-7280-b5f8-82d0df4ec066`. No independent review, accession
admission or public release is claimed by this working note.

## Authority and working source

Punk6529 approved proceeding with the accession and scholarly publication work,
directly confirmed the gift is unrestricted, and instructed ordinary Museum
display without further donor rights questions. Preserve artist copyright and
source credits; do not manufacture a copyright assignment or public reuse
licence. The complete plan and donor-direction amendment are retained in the
original task checkout's September 13 accession scholarship plan. The same
task continuation was dispatched through the app with `thinking: ultra`.

This isolated branch is `codex/salgado-accession`, constructed from Museum main
`3926d78faacf67a62b8d9b48e15d26c43b52eae9`. Current main and GitHub identity
`punk6529` (108035228) were verified on September 13. The older dirty checkout
was preserved. Current main contains three accession lots and two proposed-gift
records; no Salgado/MAX PAIN reservation or fourth lot was found in its records
or current remote branch names. Reserve lot `6529NM.2026.004`, objects `.01`
through `.06`, and retrospective proposal record `6529NM-PG-2026-003` for
construction. These identifiers are not a completed accession decision.

The object order is 226, 1117, 2059, 2216, 2768, 4697, Ethereum contract
`0xf1f036cebb4b64f138e4f57754edbceb64fb80fc`. The group title *Amazônia:
Forest, Water, and Community* is Museum-formed.

## Evidence completed in this continuation

- All six retained metadata files and six JPEGs match the exact SHA-256 values
  in the August 24 proposal draft. All images fully decode with Pillow 12.3.0.
- Five JPEGs measure 3543 × 2362 pixels; token 2216 measures 3543 × 5315.
  All have RGB encoding, orientation 1 and the same 560-byte embedded ICC
  profile, SHA-256 `e5f6ffb83b6d3491301dd750975684cc5cc2a1951c994a14b08cfdaa0d75a041`.
- EXIF IFD dimensions differ from the actual JPEG dimensions. Use the decoded
  JPEG dimensions for this manifestation. The visible EXIF modification dates
  are in 2022 and must not replace photographic creation dates. Further nested
  EXIF characterization and source-to-web colour handling remain to complete.
- Full-frame inspection copies were created without cropping or tonal edits.
  The original of 226 was viewed; the other five were examined through
  1600-pixel full-frame inspection copies after the native image-view tool
  returned invalid-base64 transport errors. Every source file remains unchanged.
  Do not describe this as a completed native-pixel visual audit of all six.
- Successful transfer receipts, exact logs, ownerOf, zero token-specific
  getApproved and tokenURI were verified at finalized Ethereum block 25971024,
  hash `0x1fdc3989d9b07cd1bd2c48811da35e3ffcd676f30d02424ea57e759c8b85eed9`,
  block time `2026-09-13T20:51:35Z`. All six owners are Museum custody
  `0xbecfa2ba5a782d11e1a0e821e8f2e30b6684178c`; the ENS address matches at
  that same state. The pinned block hash was rechecked after technical reads.
- The finalized observation supersedes the earlier *current* finality-pending
  state while preserving that earlier observation. The actual gift transfer
  remains transaction
  `0xd1c9986c1e885a5c29b03eb15ef5194ae890678ebf6d0ab84d607af8affc3808`,
  block 25970845, time `2026-09-13T20:15:35Z`.
- The EIP-1967 implementation is
  `0x659d80ce8ac5cad5ab2fdd7137caf3d06d246289`; admin and beacon slots are
  zero. Zero admin does not establish absence of an upgrade path. Source-level
  authority and metadata-mutability review remains to complete. The optional
  totalSupply call reverted; no supply count is inferred from it.

Evidence is retained in the task artifact root under
`salgado-source-evidence` and `salgado-finalized-evidence-v2`. The latter summary
has raw-byte SHA-256
`8ea329d9ce50d4ac7c87ff086be6ab93ba9e61619f9f504e57e6d94846f0d423`.
The collector uses current Museum guarded HTTPS transport, retains request and
response bytes, and submits no transactions. Its first attempt stopped on the
optional totalSupply revert; that partial directory is retained separately and
is not the completed evidence package. No independently recoverable second
archive or restoration claim is made by these same-host working copies.

## Image observations to carry into the catalogue

| Token | Direct observation | Editorial consequence |
|---|---|---|
| 226 | Narrow pale trunks and palm fronds fill the upper field; dark water reflects them over much of the lower field, interrupted by small ripples. The horizontal waterline sits above the image centre. | Develop the reversal between upright growth and reflected depth. Calling this only an immersive forest view misses much of the photograph. |
| 1117 | A near dark ridge rises diagonally from lower left toward upper right; a farther cliff has a long near-horizontal top. A lighter forested plain recedes toward haze on the left; clouds punctuate the upper right. | Explain overlapping planes, shadow and the interruption of apparent flatness. Retain the issuer's Imeri caption; do not rename the mountain from resemblance. |
| 2059 | Bright cumulus masses spread above a low, distant horizon; rain curtains connect sky and land. The foreground forest alternates between sunlight and broad shadow. A pale river segment appears left of centre. | Read weather through the relation between clouds, rainfall and ground shadows. This is distinct from the sustained river course in 2768. |
| 2216 | A young sitter turns slightly within a vertical frame and looks toward the camera. Pale bead strands cross the forehead and descend beside the face; dark painted bands surround the eyes and cross the lower face. The background is plain and dark. | Examine the portrait encounter and the different directions of ornament. Attribute Marubo/community information to the caption; do not invent the sitter's name or a symbolic translation of the designs. |
| 2768 | A broad pale river enters from the lower right, loops repeatedly through dense forest and narrows toward the upper left. No sky is visible. | Follow changes in width and the alternating bends without asserting upstream direction or an unsourced river name. |
| 4697 | A foreground figure on the right wears a broad feather headdress and holds a long dark carved object upright. Several people occupy the clearing farther left. Branches, fronds and feathers intersect across the upper frame. | Give the foreground figure and background group their separate spatial roles. Do not call the whole scene a procession or identify individuals without caption evidence. |

## Sources read and source-control issues

- [TASCHEN, Amazônia](https://www.taschen.com/en/books/photography/42384/):
  current page now describes the **45th edition**, not necessarily the original
  2021 book's physical specification. Supports original project/book chronology,
  Lélia's editorial role and the publisher's framing. Do not transfer the current
  512-page/ISBN specification to the first edition.
- [MAXXI exhibition](https://www.maxxi.art/en/events/sebastiao-salgado/):
  October 1, 2021–August 21, 2022, curated by Lélia Wanick Salgado. The site's
  environmental figures are exhibition-era statements, not current ecological
  measurements. Do not claim a specific token image was exhibited without a match.
- [ICP artist text](https://www.icp.org/content/2022): Lisa Hostetler's account,
  credited to a 1999 publication, is reproduced on a 2022 award page. Preserve
  that authorship/date distinction. Its account of serial context is useful;
  its evaluative language is an attributed position.
- [Praemium Imperiale](https://www.praemiumimperiale.org/en/laureate/salgado/):
  award-era biography plus chronology updated with the May 23, 2025 death.
  Do not repeat historical present-tense claims as current. Degree wording
  differs from Chris Wiley's account; omit the disputed completion detail.
- [Emily Bierman's 2022 interview](https://www.sothebys.com/en/articles/photography-is-the-memory-of-our-society-a-conversation-with-sebastiao-salgado):
  artist account of expedition support, digital cameras, duplicate memory
  cards, portable studio backdrop and photographic selection. These are
  project-level methods; the exact six exposure circumstances require their own
  evidence. Separate François-Bernard Mâche's music for *Magnum Opus* from
  Jean-Michel Jarre's *Amazônia* exhibition sound.
- [Sotheby's digital catalogue](https://www.sothebys.com/en/digital-catalogues/sebastiao-salgado):
  the *Tree of Life* film auction and announced 5,000-photograph blind mint are
  distinct. The announcement is not by itself an observed minted supply.
- [Chris Wiley, 2025](https://www.newyorker.com/culture/photo-booth/sebastiao-salgados-view-of-humanity):
  read the complete accessible article. It defends formal beauty as potentially
  strengthening witness, with a retrospective artist interview. Use a concise
  attributed account; the source has a 100-word summarization limit.
- [Susan Sontag, Looking at War](https://www.newyorker.com/magazine/2002/12/09/looking-at-war):
  accessible opening sections read; full article still to read before presenting
  a complete account. The article predates *Amazônia*. It has a 100-word
  summarization limit. Do not claim it reviews these photographs.
- [Jonathan Jones, 2025](https://www.theguardian.com/artanddesign/2025/jan/17/let-amazonians-speak-for-themselves-trouble-in-paradise-for-sebastiao-salgados-amazonia):
  located, but body has not yet been examined. The source has a 25-word
  summarization limit. It is not yet an evidentiary basis for a detailed account.
- [UNIVAJA, Marubo](https://site2024.univaja.org/marubo/) and
  [Nossa União](https://univaja.org/nossa-uniao/): community organization sources
  place Maronal in the Curuçá region and supply Marubo self-description and
  political organizing history. Do not use general descriptions of ornaments to
  decode the sitter's individual designs without object-specific evidence.
- [Museu do Índio/PRODOCLIN, Yawanawa](https://prodoclin.museudoindio.gov.br/index.php/etnias/yawanawa/povo):
  historical text adapted from Camargo-Tavares (2013); useful for the distinct
  Nova Esperança/Mutum organizations and cultural festivals. It contains older
  population and office-holder claims and internally different demarcation years.
  Use only attributed historical points relevant to the photograph; do not make
  it a current census or legal-status report.

Next: source-level contract review and fresh media retrieval; precise visual
and caption records; complete the scholarly corpus and typed accession package;
build preservation and display derivatives; obtain genuine independent review;
integrate and verify the public edition under current release instructions.

## Construction update and correction — 13 September 2026

Supersedes the earlier current description of token 226 in this note: the
statement about water, a waterline and reflections was a constructor error.
The fixity-verified 1280-pixel colour-managed review image shows dense forest
vegetation, slender pale trunks, drooping fronds and dark gaps. No reflection
is established. The object entry is version 0.1.1; group, artist, project,
acquisition and river-comparison passages have been corrected. The original
assertion remains above as a superseded construction observation.

Fresh metadata retrieval matched all six retained proposal metadata hashes.
The ICC profile is Adobe RGB (1998); exact EXIF original-year fields agree
with catalogue years, while date-code suffixes are not calendar months.
Eighteen full-frame WebP copies were generated with the existing fixed-sRGB,
quality-82/method-6 transform. All decoded, retained the expected fixed ICC,
and had EXIF/XMP removed. All six 1280-pixel copies were visually inspected.
The illustrated local review copy was regenerated after the correction.

Twenty-five successful receipts and canonical block hashes verify the indexed
transfer sequences from mint to Museum. Indexer pagination was exhausted;
full-range independent log completeness is not asserted. The fresh Wave
readback completed at 2026-09-13T21:32:17.6672350Z and reports WINNER,
73600740 rating and 15 raters, API is_signed=true. The original August 25
PARTICIPATORY readback is retained as public extraction.

Contract source and pinned reads distinguish extension tokens 226/2216 from
base-path tokens 1117/2059/2768/4697. The proxy and implementation source/ABI
expose no public upgrade entry point in the examined source. Metadata remains
administratively or extension controlled; the extension endpoint did not
supply verified source/ABI. Zero EIP-1967 admin is not an immutability claim.

Twenty-one typed records now exist: six object records, six rights statements,
six condition reports, gift acceptance authorization, accession-processing
lot and Wave status observation. All are pending independent review; no
certificate, permanent Collection admission or production website release is
claimed. The Museum's schema/state/commitment validator and four Salgado
evidence-join tests pass. Existing dossier, network-fetch guard, rights,
institutional-source inventory, media and public-entity checks pass.

The scholarly corpus has the group essay, artist study, project study,
acquisition narrative, six labelled extended entries, source chronology,
title/display determination and technical/preservation instructions. The
retrospective proposal currently has its original resolution and typed status
readback; full proposal/register and public entity integration remain to finish.

The local 43 MB preservation archive was inventoried and its internal files
verified. Automatic approval review rejected the proposed creation of two
private Museum AWS buckets and upload: general preservation authorization was
not treated as explicit authorization for that source-image/metadata payload
and those destinations. The script did not run. No workaround was attempted.
The precise archive/destination plan is retained outside the public repository.
A concise asynchronous question requests that approval and authorization for
a separate Ultra reviewer. Pending answers are not approval.

Artifact directories in this task's permitted artifact root: salgado-review
(illustrated HTML and 18 WebP copies), salgado-preservation (archive, manifest
receipt and upload-approval plan), and the acquisition/verification scripts.
The complete evidence and source code needed for the next step remain there.


## 13 September 2026 — approved archive completion and Ultra review corrections

This update supersedes the earlier pending-approval status. The user explicitly
approved the exact source-image/metadata package, new regional archive
locations and restore tests, and authorized the separate Ultra agent review.
The prior automatic approval rejection was resolved by that explicit approval;
no bypass was attempted. Two private, encrypted, versioned regional archive
objects now exist. Each exact-version download matches source-package SHA-256
cc8f174cab25232ea8469862183e7f47ab3dc3239e30be5ed9998fb32728fecc.
Every one of the 341 files passed length/fixity verification; all eighteen WebP
copies rebuilt identically from each restored source set without a gateway.
The public restoration summary records custodial aliases. Exact bucket,
version and access receipts remain outside the public repository. Both
copies share one AWS account; no independent administrative custodian is claimed.

The [independent Ultra review](2026-09-13-salgado-independent-review.md)
checked the six images and 103 raw request/response fixity pairs, 35 exact
transfer logs across 25 receipts, source joins and eighteen derivatives.
The constructor corrected class-A labelling of off-chain characterization
to class C, tightened the Hostetler attribution, aligned the UNIVAJA source
version and added edition metadata/bibliographic apparatus. The first review
remains intact; a changed-file rereview is requested separately.

Scoped encumbrance/control diligence and an official OFAC exact-address UI
screen are documented. The positive control returned CHATEX/CYBER2/SDN;
ten accession-related address searches returned zero results, each with its
own observation time. This is not identity, exposure or general legal clearance.
No further donor rights information is required.

The 21 typed records remain pending binding Museum review, with no invented
human reviewer or certificate. Source preservation is complete for its captured
scope; capture of the final reviewed publication edition remains outstanding.
The local illustrated review copy now includes all sixteen scholarly and
registration sections, full-frame images, internal navigation and numbered
notes. The deterministic public inventory and visitor bundle are regenerated.
The first whole-suite run had 348 tests, one inventory-staleness error and one
platform skip; the missing regenerated inventory caused the error. Retesting
follows the fix. Current remote main remains 3926d78faacf67a62b8d9b48e15d26c43b52eae9;
GitHub identity punk6529 has admin/maintain authority. No merge or release
permission is inferred from account permissions alone.

## 13 September 2026 — binding intake approval and admission construction

The user-appointed independent Ultra AI review approved 70 exact intake files
at 22:28:02 UTC. All 70 Git blobs were verified against that receipt in commit
4939941ae69d5edf0eec86712186add1666ab410; the separate commit-binding receipt
preserves the original file receipt and reviewer statement unchanged.
This supersedes the earlier pending-binding-review status and human-only
interpretation. The appointed AI reviewer is identified honestly; protected
GitHub approval is separate.

Accession certificate 6529NM-ACC-2026-004 and the dated admission amendment
now bind the six exact objects to the gift, title declaration and transfers.
Receipt, acceptance, acquisition, title passage, custody registration and
accession are separate events. The register preserves revision five with its
source commit and exact snapshot: its missing prior review is not invented.
The title instrument remains bound to its immutable intake edition. The
unrestricted gift and ordinary Museum-use determination are unchanged.

The catalogue projection adds artist, project, acquisition, accession,
research, six work and six display-media entities. Forty governed relations
connect them. Collection and gift-program membership are amended under the
new review scope; earlier generated records retain their own review binding.
The eighteen reviewed WebPs are public presentation copies with EXIF/XMP
removed. Original JPEGs and private archive access receipts remain restricted.

The accession lifecycle gate now permits explicitly unspecified creative-
derivative and AI-training rights; it still rejects missing rights statuses
and unspecified ordinary Museum-use classes. This records the absence of
those optional licences without fabricating a grant or blocking admission.
Six evidence/media tests pass. The complete suite and final independent
admission/projection review follow. The source archives are verified; later
admission/publication edition capture remains a separate outstanding step.
No production site deployment or Wave announcement is claimed.

The historical proposal's original six-part publication is retained. A full
retrospective proposal-profile backfill is not invented: the current generic
storm validator assumes a different part structure. Its original resolution,
readback and adopted status remain directly cited for this accession.


### Independent admission review corrections — 13 September 2026

The appointed Ultra reviewer found the substantive catalogue, title/custody
joins, historical predecessors, media fixity and graph relations sound.
The constructor now requires the exact approved intake receipt, its source
identities and hashes, and all 70 original reviewed files through explicit
exceptions that remain active under Python optimization. The register schema
rejects mixed predecessor forms. Collection/program projections carry the
new accession sources in their source and evidence fields. Two mutation tests
cover the corrected gates. Eight accession tests and all 49 projection tests
pass. Static projection expectations now include 19 permanent works and 427
generated records. Six other local test failures were Windows Git checkout
path-length failures; rerun uses child-only core.longpaths configuration.
