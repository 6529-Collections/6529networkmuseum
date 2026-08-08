# WP-3 Magnum scholarship and typed-publication handoff

## Scope

WP-3 built an isolated museum-grade scholarship corpus for proposed gift
`6529NM-PG-2026-001`, Curated Acquisition `6529NM-CA-2026-003`, and its five
Magnum Photos 75 photographs. The corpus is proposal scholarship and public Work
projection content. It is not an accession, object-record, title, custody,
acceptance, or permanent-Collection record.

## Durable conclusions

- The live proposal observation at `2026-08-08T09:06:07.985Z` remains drop
  `002bfa4f-8416-48bf-b35e-38f354e9a9f0`, serial `1276093`, `PARTICIPATORY`, rank
  1, realtime rating `122,969,240`, and 29 raters. The rating and rank are
  mutable observations; this observation is historical-only after the later
  authenticated readback.
- The canonical current authenticated readback at `2026-08-08T10:15:02.0167151Z`
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
- The five works map to Wave parts 2–6 and to the exact already-published
  upstream JPEG URLs in the signed proposal. Narrow reference/embed use in the
  historical Wave presentation is documented with artist/Magnum credit, `All
  Rights Reserved`, and a Wave-source label. No JPEG or responsive derivative is
  retained or generated; download, full-resolution delivery, derivative, IIIF,
  preservation, and Collection publication remain blocked. The machine join
  now enforces exact allowlisted URLs, no runtime fallback or URL rewriting,
  closed UI affordances, and non-identifying child alt text.
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
- Public corpus check: `reviews/check_public_utf8.py`.

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
- Strict decoded-byte UTF-8/no-mojibake check passes for 21 public Markdown
  pages, including dossiers and the source register; README and `reviews/` are
  intentionally control-plane exclusions.
- Deterministic local Markdown/JSON reference check passes for 131 relative
  links and 19 governed repository paths, plus 5 source-register paths and 6
  explicit staging paths.
- Media-policy check passes for five exact Work/Media/Wave joins and fail-closed
  runtime rules.
- All source IDs referenced by the corpus, including S40 Digital Camera World,
  S41 AFP, S42 United Nations, S43 United States Department of State, and S44
  Micha Bar-Am Archive, resolve in the source register.
- Four machine JSON files parse successfully.

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
- Pre-rebase source base used for this correction pass:
  `4821ea52e4cb8e0f0915824fbc2946ec0f6313b8`.
- The local `origin/main` ref subsequently advanced to
  `36ac78a1172327dab5ba55f7b8f96d6d45dc5d85` (status amendment PR #39,
  parent `4821ea52`); this WP-3 branch remains unrebased and unpublished.
- Exact correction boundary in this pass: `INDEX.md`, `content/wp-3-magnum/**`,
  and this WIP note; no shared schemas, controlled vocabularies,
  status-amendment worktree, merge, deployment, or publication were touched.
