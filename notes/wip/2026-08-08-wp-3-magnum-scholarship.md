# WP-3 Magnum scholarship and typed-publication handoff

## Scope

WP-3 built an isolated museum-grade scholarship corpus for the selected gift
`6529NM-PG-2026-001`, Curated Acquisition `6529NM-CA-2026-003`, and its five
Magnum Photos 75 photographs. The corpus is proposal scholarship and public Work
projection content. It is not an accession, object-record, title, custody,
acceptance, or permanent-Collection record.

## Durable conclusions

- The live proposal observation at `2026-08-08T09:06:07.985Z` remains drop
  `002bfa4f-8416-48bf-b35e-38f354e9a9f0`, serial `1276093`, `PARTICIPATORY`, rank
  1, realtime rating `122,969,240`, and 29 raters. The rating and rank are
  mutable observations; this observation is historical-only after the later
  signed-drop API readback.
- The canonical current signed-drop API readback at `2026-08-08T10:15:02.0167151Z`
  reports the same signed drop as `WINNER`, rank `1`, realtime rating
  `121,603,214`, and 29 raters. The current public status is **Selected by
  Museum Wave; acquisition review in progress**. Formal acceptance, donor
  authority, transfer, title, custody, rights clearance, technical and
  preservation completion, accession, and permanent-Collection membership
  remain separate later facts.
- The five public Work projections are bound to the WP-1 committed target IDs
  `6529NM-W-0024` through `6529NM-W-0028`. Their status line pairs the current
  selected-review state with **Outside the permanent Collection**. Proposal
  `OBJ-001` through `OBJ-005`, token IDs, CAIP-19 values, archive numbers,
  components, and manifestations remain typed aliases and references.
- The five works map to Wave parts 2–6 and to the exact historical public
  Wave-upload URLs in the retained presentation record. The Arweave URLs remain
  separate token-linked source-image references. Narrow reference/embed use in
  the selected acquisition's Wave context is documented with artist/Magnum
  credit, `All Rights Reserved`, and a Wave-source label. No authenticated
  publication receipt or snapshot is retained in this WP-3 branch; no copyright
  or broader reuse authority is inferred. No JPEG or responsive derivative is
  retained or generated; download, full-resolution delivery, derivative, IIIF,
  preservation, and Collection publication remain blocked. The machine join
  now enforces exact Wave-upload URLs, token-source separation, exact proposal
  context, no runtime fallback or URL rewriting, closed UI affordances,
  non-identifying child alt text, and the required Saman identity_inference
  block.
- The posted dossier’s 148 live-token observation at finalized block
  `25,690,178` and the separate research note’s 149 issued across two
  observable curations are preserved as different observation boundaries. The
  corpus does not reconcile them speculatively.
- Magnum is profiled as a 1947-founded photographer-member cooperative, with
  ICP’s *Magnum Manifesto* and photobook program added as an independent
  institutional source. Magnum Photos 75 is treated as a 2022 archive and
  blockchain publication project; the announced three-curation/225 description
  is kept separate from the unresolved question of third-release completion.
- The public page family is differentiated: acquisition gateway, institutional
  profile, project profile, group essay, artist/practice profiles, and
  artwork-led Work pages. Visitor pages use footnote/source-note citations;
  machine and dossier records retain evidence classes and integration controls.

## Corpus and machine handoff

The isolated root is `content/wp-3-magnum/`.

- Entity profiles: `entities/`.
- Five artist profiles: `artists/`.
- Five Work pages: `works/`.
- Acquisition gateway, group essay, and acquisition narrative: `entities/` and
  `essays/`.
- Caption/evidence, chronology, source/rights, rights/technical/provenance,
  and media records: `dossiers/`.
- Source register: `sources/source-register.md`.
- WP-1 input: `machine/integration-map.json`, `machine/work-projections.json`,
  `machine/object-schedule.json`, and `machine/wave-media-join.json`.
- Public corpus check: `scripts/magnum/check_public_utf8.py`.

WP-1 must admit the Organization `6529NM-ORG-0002`, Project/Series
`6529NM-PRJ-0006`, five Artists `6529NM-ART-0017` through `0021`, five Works
`6529NM-W-0024` through `0028`, Curated Acquisition, Research Publications,
Media References, and declared relations as one release group; add the root and
reviewed projections to the release manifest; and bind the admitted group to
the reviewed commit and regenerated manifest. WP-1 owns shared schemas and
controlled vocabularies. No shared schema or vocabulary was changed here.

## Verification completed

- Five public Work pages have one status line, one concise Further research
  section, and one source/rights colophon. No visitor-facing WP-1 placeholder,
  raw lifecycle/collection row, evidence-class label, machine-join directive,
  frontend instruction, or repeated selection-status footer remains.
- Strict decoded-byte UTF-8/no-mojibake check passes for all 22 public Markdown
  manuscripts, including the scholarship README, dossiers, and source register.
- Deterministic local Markdown/JSON reference checking covers the complete
  canonical scholarship tree and its governed repository paths.
- Media-policy check passes for five exact Work/Media/Wave joins and fail-closed
  runtime rules.
- All source IDs referenced by the corpus, including S40 Digital Camera World,
  S41 AFP, S42 United Nations, S43 United States Department of State, and S44
  Micha Bar-Am Archive, resolve in the source register.
- Four machine JSON files parse successfully.

## Editorial audit disposition

- The Curated Acquisition entity is now a concise facts/thesis/status gateway;
  the acquisition narrative carries donor formation, mission fit, countercase,
  and consequences of later acceptance; the long group essay carries the only
  sustained comparative reading.
- The group argument is selection-specific and testable: one first-curation
  token (#44) and four second-curation tokens (#97, #104, #127, #145) form a
  donor-created relation across two Magnum Photos 75 registers.
- Every Work page leads with the exact historical Wave-upload image and a short
  label, then
  moves into object-specific looking, caption history, structured status/rights,
  and one Further research section. Saman's safeguarding determination remains
  in the object and rights apparatus; the group essay states one interpretive
  consequence and does not pursue public identification.
- Artist profiles now have distinct phase, book/exhibition, material, and
  reception structures, with concise Selected Work sections and no repeated
  object-caption or implementation language.
- Visitor-facing manuscripts contain no WP-1, rebase, deployment, schema,
  manifest, frontend, or machine-join narration. Those controls remain in the
  handoff, dossier, and machine records.

## Registrar media disposition

- The corpus retains historical public Wave-upload URL evidence and recorded
  credits/rights labels only. The exact signed API response is not retained as
  a public-safe receipt or snapshot in this branch; no signed-state, copyright,
  reproduction, or broader reuse authority is inferred.
- The five Work joins distinguish the exact Wave-upload presentation URL from
  the Arweave token-linked source-image URL. View and hero affordances are bound
  to proposal `6529NM-PG-2026-001`, Curated Acquisition `6529NM-CA-2026-003`,
  Wave `5f207393-5418-4a75-8738-e40edb44a94d`, and drop
  `002bfa4f-8416-48bf-b35e-38f354e9a9f0`; outside-context use fails closed.
- Saman's `identity_inference` block is required and mutation-tested. Public
  alt text remains non-identifying; name, age, identity, consent, unpublished
  location, and sensitive metadata are not inferred. Bar-Am alt text is likewise
  mutation-tested against tear-gas inference and stays with visible smoke and
  canister.

## Open correspondence and integration questions

Archive/rights correspondence remains open for exact assignment, contact sheets,
first publication, identifier crosswalks, rights instruments, and sensitive
subject documentation. For Saman, future inquiry should ask whether Magnum or
the photographer’s records contain safeguarding, consent, caption, or restricted
identity documentation; public publication does not make identification of the
child a research goal. Sensitive identity information remains restricted unless
a later review establishes a responsible public form. Analogous care applies to
unnamed people in the other works.

The proposal remains a typed public Work projection in the WP-1 migration
staging area until the governed release admits it. No accession/object-record
record is to be manufactured to fill the integration gap.

## Pre-rebase checkpoint

- WP-3 branch: `codex/wp-3-magnum-scholarship`.
- Clean baseline before this correction pass: `37ac11f80bd990055cf42c3b9e09632c7cc3fd90`.
- WP-1 target projection: `61ec035`; merge-base before migration:
  `c01af9f08778c77b823283f81a989cd5f5e24a95`.
- Actual WP-3 branch source base at this checkpoint:
  `ff26543908c5d1e1851e34b597b36ab13ff20849` (PR #36); PR #37
  `4821ea52e4cb8e0f0915824fbc2946ec0f6313b8` and status amendment PR #39
  `36ac78a1172327dab5ba55f7b8f96d6d45dc5d85` are later canonical main refs,
  not yet in this branch. The current branch/main merge-base is `ff265439`;
  this WP-3 branch remains unrebased and unpublished.
- Exact correction boundary in this pass: `INDEX.md`, `content/wp-3-magnum/**`,
  and this WIP note; no shared schemas, controlled vocabularies,
  status-amendment worktree, merge, deployment, or publication were touched.

## 2026-08-08 substantive rewrite checkpoint

- Rewrite parent checkpoint: `db5a39a9274f901c88b87f80aa68bc643aa65130`.
- This local branch remains `codex/wp-3-magnum-scholarship`, unrebased and
  unpublished. The rewrite separates the acquisition gateway, acquisition
  narrative, comparative essay, artist profiles, and art-first Work pages.
- The registrar correction distinguishes CloudFront Wave-upload presentation
  media from Arweave token-source media, keeps the receipt field unretained
  pending WP-1's public-safe receipt contract, and requires context-bound
  display plus Saman/Bar-Am mutation guards.
- The revised current-state wording is **Selected by Museum Wave; acquisition
  review in progress**. Formal gift acceptance, donor authority, title/custody,
  rights, technical, preservation, accession, and Collection steps remain later
  review events.

## 2026-08-08 final local rewrite and registrar-control checkpoint

- The five Work entries now expose observed source dimensions and byte counts:
  Seymour `3,056 × 4,600 / 2,518,674`, Towell `5,369 × 3,601 / 1,813,285`,
  Bar-Am `5,000 × 3,292 / 1,666,083`, Saman `5,616 × 3,744 / 1,540,870`,
  and Meloni `5,964 × 4,768 / 16,871,807`. These are upstream technical
  observations; no source bytes, responsive derivative, or preservation master
  is retained. The 16.9 MB Meloni source is user-initiated and non-eager.
- The current selected projections carry
  `6529NM-WAVE-OBS-2026-08-08-001` at
  `2026-08-08T10:15:02.0167151Z` with payload hash
  `sha256:beae463453c21a3e8e51e311f8d8b0d8e516b9a63b43dd6c2000d1d441d4a097`.
  They also carry the final WP-1 target publication observation ID
  `6529NM-WAVE-PUB-OBS-2026-08-08-001` and the same observation time, with
  receipt payload hash intentionally pending WP-1 merge and binding.
- `wave-media-join.json` treats `wave-storm.json` as historical public URL
  evidence only. The final public-safe `WAVE_PUBLICATION_OBSERVATION` receipt,
  per-part hashes, and Work/Media Reference/Curated Acquisition/proposal graph
  relation are required before a standalone Work route may display the exact
  historical Wave-upload URL. Outside that relation the route fails closed.
- The Arweave token-linked source URL, its fixity, dimensions, and byte count
  remain separate from the CloudFront Wave-upload presentation URL. Bar-Am's
  current smoke/canister alt is bound to a pending WP-1 append-only
  media-description amendment. The retained revision-1 Wave part 4 wording is
  preserved in the machine record with its exact LF/UTF-8 text hash
  `sha256:ac2b178e1cb05f3f8c33aee655e763fc2d18261b2c1e6e67f72d77d16f4fc9a2`;
  the public-safe smoke/canister wording remains a separate current value.
  Saman's identity prohibition, child rule, exact source URL/hash, and unsafe
  visual/context mutations are deterministic checks.
- Source corrections added direct UNESCO Palmyra list `23`, Rapid Assessment
  `142423`, and April 2016 mission `1488` locators; direct GOST and Visa records;
  the WARM practice record; the stable Art Windsor-Essex search locator; the
  Henri Cartier-Bresson Foundation Towell membership-date variant; and retained
  TIME/AFP excerpt and page-state caveats. The 2015 destruction chronology stays
  separate from the March/April 2016 access and demining chronology.
- New local gates are `scripts/magnum/check_copy_citations.py` and the
  `tests/test_wp3_magnum_editorial.py` wrapper. The media checker now validates
  current observation identity/time, exact source URL/hash/fixity, standalone
  route denial, Bar-Am amendment binding, Saman identity/age-classification restrictions,
  and adversarial mutations. No network-dependent CI behavior was added.

## 2026-08-09 independent scholarship review

- The five-Work argument is strongest when framed through borders, controlled
  access, caption authority, damaged sites, and documentary afterlives. It is
  weaker as a general account of war or aftermath. The preferred subtitle is
  **Five Photographs of Borders, Access, and Afterlives, 1952–2016**.
- The selected relation is donor-formed across two Magnum Photos 75 curations.
  The reviewed record contains no statement that Magnum Photos, Alejandro
  Cartagena, Azu Nwagbogu, or the photographers formed or endorsed this exact
  five-Work selection. Current prose states that evidentiary boundary rather
  than asserting a negative fact.
- Magnum Photos, the photographer-owned cooperative; Magnum Foundation, an
  independent nonprofit; and the Foundation NFT marketplace are distinct
  entities. Public copy and the source register must not collapse them.
- “One of one” describes the token edition represented by the contract record;
  it does not establish uniqueness of the underlying photograph, negative,
  print, or other manifestation. The contract is an EIP-1967 proxy with
  administrative URI controls, so metadata immutability must not be asserted
  without a historical implementation and admin audit.
- Seymour’s estate presents a visually matching frame under a King Solomon’s
  Mines description, but no public crosswalk binds `PAR116258.jpg` to
  `SED1952003W00003/23`. Towell’s preferred place form is Suchitoto; the issuer
  variant Suchitito remains part of the caption history. No reviewed source
  identifies the church, military unit, operation, assignment, or first
  publication.
- Bar-Am’s public description remains with visible smoke and an airborne
  canister. Police tear gas and the Women of the Wall dispute belong to
  separately attributed 1989 context. No reviewed source identifies the
  person or resolves the archive suffix difference between `/26C` and `/26`.
- Saman’s public description uses **apparently young person**. The official
  air-strike account remains attributed and explicitly unverified. The
  reviewed public record supplies no age, identity, consent documentation,
  precise house, weapon attribution, or later-life account. Public research
  must not turn identification into an objective.
- Meloni’s work is dated 1 April 2016. UNESCO’s destruction chronology and the
  later government-permitted, incompletely demined access chronology remain
  separate. TIME and AFP describe access conditions; they do not provide an
  archive crosswalk or prove every caption claim.
- Wave governance selected the proposal for acquisition review. It did not by
  itself complete gift acceptance, title, custody, rights, technical review,
  preservation, accession, or permanent-Collection membership.
- The serious countercase remains part of the acquisition scholarship:
  aestheticization of violence; unequal caption authority; represented
  communities absent from the selection process; managed access; safeguarding;
  and the danger that a donor-formed group flattens distinct histories. The
  response is object-specific scholarship, attributed claims, visible source
  boundaries, non-identifying publication, and the ability to withhold display
  where authority is incomplete.

## 2026-08-09 canonical dependency and publication evidence

- Keys & Gates WP-4 merged through PR #40 as canonical Museum main
  `b021b50c8c394d3f237707eded17fe6bb394b422`. Exact-head run `31288816982`
  and post-merge main run `31289263301` succeeded across Museum validation,
  deterministic Ubuntu/Windows, public-publication Ubuntu/Windows, and focused
  Stream/catalog checks. All sixteen K&G images remain withheld with zero
  public widths or derivatives and no display authority.
- A new public-safe Wave receipt is retained at
  `content/wp-3-magnum/evidence/6529nm-wave-publication-observation-2026-08-09-001.json`.
  Observation `6529NM-WAVE-PUB-OBS-2026-08-09-001` was made at
  `2026-08-09T02:04:21.7672652Z`; canonical payload SHA-256 is
  `sha256:93e968562297fe5acff792e027f302b938ba6fa1ac88284754c4ba684d1266a2`
  and receipt-file SHA-256 is
  `sha256:2d102b1e5ee4c448bad0631d3bb659949456d74a342f6203b3a1dd12d5f29d6a`.
  The projection contains only the public Wave/drop identity, signed WINNER
  state, seven part numbers, and public media URL/MIME/status bindings. Profile,
  rater, reaction, and credential data are excluded.
- The receipt proves the historical Wave publication and exact public media
  bindings. It supplies no copyright, display, derivative, preservation, title,
  custody, acceptance, accession, or Collection authority. Every runtime
  render, download, responsive derivative, zoom, fullscreen, IIIF, and
  preservation path remains denied.
- The five token identities were rechecked at finalized block `25,714,155`
  (`0x1885deb`), hash
  `0x9ec59a4b6029e30f52491f6ebfbf34c521a4338056fa1a0b9a5cff12bb9ac767`,
  timestamp `2026-08-09T01:33:11Z`. All five `ownerOf`, `tokenURI`, and
  `getApproved` reads matched the corpus; all five token approvals were zero.
  The deployed address uses an EIP-1967-style proxy and exposes
  administratively mutable token/base URI state. Arweave fixity therefore does
  not make the contract pointer immutable.

## 2026-08-09 canonical integration candidate

The scholarship corpus now lives under
`records/proposed-gifts/6529NM-PG-2026-001/public/scholarship/`, beside the
governed proposed-gift record it interprets. The deterministic editorial, link,
Unicode, and media-policy checks live under `scripts/magnum/` and are committed
by the complete release manifest. The public index, five artist profiles, five Work entries, Magnum Photos
and Magnum Photos 75 profiles, two acquisition essays, research dossiers, source
register, and machine projections are all release-manifest declared.

The public entity projection adds Research Publication `6529NM-RP-0003`, thirteen
`PUBLICATION_INTERPRETS_ENTITY` relations, and one
`INSTITUTION_PUBLISHES_PUBLICATION` relation. The complete generated projection
is 332 records: 120 entities, 211 relations, and one Wave status observation.
Permanent Collection membership remains exactly the seven Casey Reas Works.
Magnum remains `selected_by_museum_wave_acquisition_review_in_progress` and
`not_in_collection`.

The canonical signed Wave publication record remains
`6529NM-WAVE-PUB-OBS-2026-08-08-001`, payload
`sha256:887d527756721cae1bf758a8205d1f5f7e0d1cebee2b3f27aafcab5271132995`,
record SHA-256
`sha256:b1f57fa0010bdaf0f9f21854f88e446e7f20b4a1921ab6fd075d4836c5920e58`.
The later public-safe API observation at `2026-08-09T02:04:21.7672652Z`
confirms the continuing signed `WINNER` state and public
URL/MIME/media-state fields; it supplements rather than supersedes the
canonical enveloped observation.

All five photographic URLs are non-rendering evidence locators. No photograph,
thumbnail, derivative, responsive source set, download, zoom, fullscreen,
IIIF service, or preservation object is admitted. The Museum-authored CC0
proposal cover remains a separate media reference and may not impersonate a
source photograph.

The pre-schema candidate release contained 534 publication-inventory entries,
533 bundled visitor documents, and 775 complete-manifest entries. Candidate
manifest SHA-256 is
`sha256:617befc175f8f61897bd6150d85605a641210fdd2540cbfb4d579dae66a1bc80`;
Keccak is
`0xed2f45eb33c639ab579345012a02dced06dc830cc066cfc0807a6f2d30979df1`.
These commitments were superseded when the supplemental evidence and supporting
machine records received their required governed-record schemas. The exact
candidate release contains 534 publication-inventory entries, 533 bundled
visitor documents, and 777 complete-manifest entries. Its authoritative
SHA-256 is
`sha256:bbabfe4e198fe833782257496165374d80adacf37d163eb04388d317d563c4a9`;
its Keccak commitment is
`0x507e63112fb1573b866c28c89cf699f4cea51c23da702029850e10ae1aab4672`.
Independent review, deterministic reviewed-child promotion, and a release-only
catalog/pointer activation remain separate required commits.

## 2026-08-09 independent-review correction candidate

Four independent exact-head reviews rejected candidate `93f8742cb64121cabd8a2f68ccd128879ec49a6e` on evidence, rights/media, schema, and reproducibility grounds. The corrected candidate resolves each finding:

- The Saman record describes an **apparently young person** and expressly
  records that age classification is unverified. Public and machine records no
  longer assert that the subject is a child. Identity and age-classification
  inference remain prohibited. The Artist summary now states that the cause of
  the visible wall marks is not established by the image.
- No visitor Markdown contains or links directly to any of the five restricted
  CloudFront photographs or token-linked source-image URLs. Visitor pages link
  to the exact seven-part Wave proposal context. Exact source locators and
  fixity remain in governed machine and evidence records. A corpus-wide
  regression rejects future direct-locator or remote-image reintroduction.
- `schemas/magnum-scholarship-machine-record.schema.json` now closes every
  critical nested contract and all three five-Work row shapes. It fixes Work
  order and rejects empty projections, undeclared nested fields, malformed work
  rows, and route-policy drift. The public-safe Wave evidence schema fixes the
  seven ordered part identities, exactly one media item in parts 1–6, and no
  media in part 7.
- The four executable Magnum checks moved to `scripts/magnum/`, are committed by
  the release manifest, and are required unchanged across candidate A and
  reviewed child B by the publication-catalog verifier. All 22 public Markdown
  manuscripts, including the scholarship `README.md`, are covered by Unicode
  and editorial checks.

The corrected release contains 534 publication-inventory entries, 533 visitor
bundle entries, and 781 complete-manifest entries. The authoritative regenerated
commitments are carried by `release-artifacts/latest/record-manifest.json`;
they are not copied into this manifest-bound ledger because doing so would make
the ledger change the commitment it reports.
Focused editorial, media, schema-adversarial, projection, inventory, bundle,
manifest, and bootstrap checks pass. A fresh exact-head independent review is
required before merge and reviewed-child promotion.

## 2026-08-09 exact-evidence and append-only provenance correction

The subsequent bot review identified a final group of record-contract issues,
now corrected without changing the visitor scholarship or opening image
delivery. Each Work projection declares the complete set of source-register IDs
actually cited on its public page, and an executable check recomputes that set
from the manuscript. The integration map, media join, schema, and Saman Work
projection now share one exact fail-closed route token and one closed
identity-inference vocabulary. The Saman safeguards continue to describe an
apparently young person without assigning an age or child classification.

The Magnum Photos Organization and five Artist profiles now retain both layers
of evidence: the original 6 August proposal labels and the 9 August research
profiles that support the expanded institutional and practice accounts. Their
current profile observations are dated to the research publication; the earlier
proposal evidence remains explicitly present rather than being silently
replaced. The source transfer remains evidence of token-manifestation chain
provenance only. Donor authority, legal title, custody, rights, and accession
remain separate facts.

The generator's compound relation statements were split into ordinary Python
statements, and focused tests now reject route-token drift, the legacy identity
shape, incomplete Work-page source arrays, or loss of either provenance layer.
Regenerated release counts and commitments remain authoritative only in the
manifest artifacts produced after this correction.

## 2026-08-09 final publication-boundary and edition correction

Independent exact-head review rejected the candidate because the visitor
bundle admitted historical proposed-gift decision manuscripts alongside the
current scholarship. Those Storm, voter-dossier, resolution, and status files
remain public governed evidence and remain in the complete release manifest.
They are now excluded from the visitor publication inventory by a general
proposed-gift decision-history rule. The website corpus admits the current
`public/scholarship/` manuscripts instead. Tests prove that the historical
files remain preserved, that no decision-history manuscript enters the visitor
bundle, and that no restricted photograph locator or superseded Saman age
description reaches bundled Markdown.

The scholarly corpus now has a common publication record for Research
Publication `6529NM-RP-0003`, edition `1.0.0`, with institutional authorship,
publication and research-cutoff dates, suggested citation, research apparatus,
status, source route, exact-commit delivery method, and revision history. Each
of the 23 manuscripts links to that record and carries compact edition metadata.
The active catalog supplies the literal immutable GitHub source link from its
exact reviewed source commit, avoiding a circular self-commit reference inside
the manuscript.

The acquisition prose now attributes the public offer to punk6529 without
treating an offer as completed donor-authority evidence. The proposal-origin
title and relation, Museum interpretation, artist authorship, and later donor
authority review remain separate. Object records add explicit date precision;
the Larry Towell record separates the normalized Suchitoto place from the
issuer's `Suchitito` spelling. Historical Bar-Am alternative text is preserved
once and superseded through an exact record/revision/part/media/assertion/hash
binding. All five source-rights rows carry their exact All Rights Reserved
status, and the Seymour credit is normalized to the canonical Wave record.

Focused UTF-8, link, editorial, media, schema, entity, publication inventory,
and visitor-bundle gates pass. A new signed candidate, complete-manifest
regeneration, fresh exact-head independent review, hosted CI, reviewed-child
promotion, catalog activation, and frontend staging/production qualification
remain required.

## 2026-08-09 final ontology and record-integrity correction

Exact-record review found a duplicated logical path in every generated envelope,
proposal-time timestamps attached to later Wave-publication observations, and six
unsupported or duplicate Magnum Photos 75 role assertions. Logical envelope URIs
now resolve once from the repository root. Evidence that cites the retained Wave
publication observation carries that observation's `2026-08-08T10:15:02.0167151Z`
timestamp.

Magnum Photos remains the single evidenced originator of the Magnum Photos 75
Project. The five photographers are creators of their five independent Works;
five Project-to-Work relations place those Works in the source project context.
The duplicate generic organization role and five direct artist-to-project creator
roles are withdrawn. Their six public relation IDs remain in an append-only
retirement register and cannot be reused. The corrected projection contains 120
entities, 205 active relations, and one Wave status observation.

Focused entity, graph, schema, editorial, media, inventory, visitor-bundle, and
manifest checks pass. Complete-suite validation, a new signed exact candidate,
independent exact-head review, hosted CI, reviewed projection/catalog activation,
and frontend qualification remain open.

The complete pre-commit qualification subsequently passed: 306 unit tests with
one platform skip, the full Museum/Casey validator, the Casey snapshot verifier,
the 22-file diligence manifest check, bootstrap validation, the fetch guard, and
all Magnum publication checks. Exact-head review and hosted CI remain required.
