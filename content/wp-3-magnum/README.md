# WP-3 Magnum Photos scholarship corpus

Status: WP-3 construction staging area with public Work projections ready for
WP-1 admission on rebase. This directory is not the final public canonical
namespace, is not an accession package, and does not change any shared schema or
controlled vocabulary. The admission contract is
`machine/integration-map.json`; the current closed release manifest does not
include this staging root ([integration map](machine/integration-map.json)).

## What this corpus is

This corpus deepens the selected proposed gift `6529NM-PG-2026-001` into the intellectual
and evidentiary shape required for the Museum's current acquisition publication
and for a later Museum publication after the subsequent acquisition gates are
completed ([S37](sources/source-register.md); [integration map](machine/integration-map.json)). Its working Curated Acquisition
identity is `6529NM-CA-2026-003`, a stable content
identifier only. It is not an accession number and does not reserve one
([integration map](machine/integration-map.json)).

The corpus supplies a typed handoff for the WP-1 public ontology:

- **Organization:** Magnum Photos.
- **Project or Series:** Magnum Photos 75, an upstream 2022 archive and
  blockchain publication project.
- **Artists:** David Seymour, Larry Towell, Micha Bar-Am, Moisés Saman, and
  Lorenzo Meloni.
- **Works:** five public Work projections for the exact token-linked
  photographs, bound to WP-1 target IDs `6529NM-W-0024` through
  `6529NM-W-0028`, with lifecycle
  `selected_by_museum_wave_acquisition_review_in_progress` and collection
  membership `not_in_collection`. Proposal object IDs remain typed aliases
  ([object schedule](machine/object-schedule.json); [integration map](machine/integration-map.json)).
- **Curated Acquisition:** *Conflict at Its Edges*, the donor-formed,
  selected five-work unit under acquisition review
  ([S37](sources/source-register.md); [integration map](machine/integration-map.json)).
- **Research Publications:** the institutional and project profiles, artist
  profiles, object entries, essays, chronologies, and evidence dossiers in
  this staging directory; final governed publication paths are assigned during
  WP-1 admission.
- **Components and manifestations:** the ERC-721 tokens, token metadata,
  Arweave image pointers, and any future Museum derivative. The source image,
  token, legal title, copyright, display permission, and Museum custody remain
  separate facts ([S37](sources/source-register.md); [integration map](machine/integration-map.json)).

## Live status boundary

The parent Museum Wave is the decision authority. The earlier read-only
signed-drop API readback from `punk6529bot drops get 002bfa4f-8416-48bf-b35e-38f354e9a9f0 --json`
observation on 2026-08-08 recorded:

- title: *Conflict at Its Edges*;
- serial: `1276093`;
- signed: `true`;
- live `drop_type`: `PARTICIPATORY`;
- Wave: `6529 Network Museum`,
  `5f207393-5418-4a75-8738-e40edb44a94d`;
- realtime rating: `122969240` and raters: `29` at that observation;
- observation time: `2026-08-08T09:06:07.985Z` UTC ([S37](sources/source-register.md);
  [object schedule](machine/object-schedule.json)).

The 09:06:07 observation is preserved as historical-only. The canonical current
signed-drop API readback at `2026-08-08T10:15:02.0167151Z` records the same signed
drop as `WINNER`, rating `121603214`, and `29` raters. Current public status is
**Selected by Museum Wave; acquisition review in progress** ([S37](sources/source-register.md);
[object schedule](machine/object-schedule.json)). Wave selection
established curatorial approval. Formal gift acceptance, donor authority,
transfer, title and custody, rights review, technical examination, preservation
planning, accession and Collection entry will follow. The five Work projections retain the typed
WP-1 lifecycle and `collection_membership: not_in_collection` fields
([object schedule](machine/object-schedule.json); [integration map](machine/integration-map.json)).

The source package remains the proposal's historical decision record:
`records/proposed-gifts/6529NM-PG-2026-001/`. Its finalized Ethereum
observation at block `25690178` established a point-in-time owner and
token-level approval state for all five tokens. That is chain evidence for the
proposal, not donor-authority, legal-title, copyright, Museum-custody, or
accession evidence ([S37](sources/source-register.md); [object schedule](machine/object-schedule.json)). The live Wave state must be re-read before any future
acceptance action or accession publication. The current signed-drop result and
its publication observation are time-bound evidence, not a substitute for that
revalidation.

## Corpus inventory

| Layer | File or directory | Purpose |
| --- | --- | --- |
| Entity profiles | `entities/` | Magnum Photos, Magnum Photos 75, and the selected Curated Acquisition |
| Artist profiles | `artists/` | Five practice-led profiles with exact-work placement |
| Works | `works/` | Five public Work projections and substantial object essays ([object schedule](machine/object-schedule.json)) |
| Essays | `essays/` | Group essay and acquisition narrative |
| Dossiers | `dossiers/` | Captions, evidence, chronologies, rights, technical, provenance, and media plan |
| Sources | `sources/` | Claim-addressable bibliography and source register |
| Machine drafts | `machine/` | Work projections, token/component schedule, media join, and WP-1 release admission contract |
| Review | `reviews/` | Recursive public UTF-8/no-mojibake scan, deterministic local-link/governed-path check, unresolved questions, and release boundary |

The work entries are ordered chronologically for interpretation: Seymour
(1952), Towell (1986), Bar-Am (1989), Saman (2011), and Meloni (2016). The
token IDs are not the sequence of the photographs' histories. The metadata
`Sequence` values such as `44/225` are preserved as issuer metadata and are
not treated as proof that all 225 announced works were minted
([S04](sources/source-register.md); [S10–S14](sources/source-register.md);
[machine object schedule](machine/object-schedule.json)).

## Evidence method

Every substantial claim is written with one of the Museum's evidence classes:

- **A — direct chain or token observation:** contract, token ID, URI,
  finalized block, transfer, owner, approval, or retrieved bytes;
- **B — authoritative issuer, artist, estate, archive, institutional, or
  governance source:** Magnum, an artist archive, ICP, UNESCO, World Press
  Photo, an authenticated Wave status record, or an equivalent primary authority;
- **C — Museum technical observation:** checksum, dimensions, byte count,
  visual inspection, link integrity, or local editorial check;
- **D — third-party historical source:** a reputable newspaper, book record,
  scholarly or contemporary report used with its authority and limitations
  named;
- **E — Museum interpretation:** close looking, significance, grouping, or
  a stated inference that does not replace a fact.

Source IDs such as `S01` and claim IDs such as `CL-127-04` are the citation
bridge. The source register records URL, title, source type, accessed date,
relevant claim, and limitation. A source URL is a locator, not a retained
preservation object. Historical captions are quoted as historical assertions;
they are not silently upgraded into Museum facts.

## Media and rights boundary

The five token-linked image URLs were retrieved for exact visual inspection on
2026-08-08. Their bytes were not added to this repository. The retained Wave
Storm package preserves URL strings and work-part history as historical public
presentation evidence ([S38](sources/source-register.md); [machine wave-media join](machine/wave-media-join.json)). The machine-readable join in
`machine/wave-media-join.json` is prepared to reference or embed those exact
URLs in the selected offer's proposal context only; after WP-1 admission, its
CloudFront binding must be verified by the public-safe
`WAVE_PUBLICATION_OBSERVATION` receipt and the final Work/Media/Acquisition
relation. The artist/Magnum credit, `All Rights Reserved`, and explicit
`Wave-source` label travel with the narrow reference ([S38](sources/source-register.md);
[machine wave-media join](machine/wave-media-join.json)). It does not promise
download, full-resolution delivery, preservation, or a new derivative
([S38](sources/source-register.md); [machine wave-media join](machine/wave-media-join.json)).

No JPEG, AVIF, WebP, thumbnail, share card, IIIF manifest, tiled derivative,
or responsive `srcset` is generated here. The issuer metadata for every object
states `All Rights Reserved` ([S10–S14](sources/source-register.md); [machine object schedule](machine/object-schedule.json)); the retained public URL evidence carries no
general Museum copyright or Collection-publication grant ([S38](sources/source-register.md);
[integration map](machine/integration-map.json)). Arweave persistence and a matching
SHA-256 do not create permission ([S09](sources/source-register.md); [integration map](machine/integration-map.json)).
Future Collection pages, download links, IIIF, and preservation masters remain
blocked pending written, component-specific rights evidence and a reviewed media
manifest ([S38](sources/source-register.md); [integration map](machine/integration-map.json)). The observed
16.9 MB Meloni source is user-initiated and non-eager; the corpus exposes its
dimensions and byte count and makes no claim that delivered bytes cannot be
saved ([S10–S14](sources/source-register.md); [S38](sources/source-register.md);
[machine wave-media join](machine/wave-media-join.json)).

The rights/technical dossier defines a fail-closed media ladder. Derivatives
may be generated only after written rights evidence identifies the permitted
use, the source bytes are retained or re-retrievable under an approved
preservation plan, and a later reviewed manifest binds every derivative to the
source hash. A future page must show a rights-blocked state rather than
silently substituting an unlicensed image. The proposal's square cover is a
separate Museum-authored CC0 asset and is not reused as a photograph
derivative ([S38](sources/source-register.md); [machine wave-media join](machine/wave-media-join.json);
[integration map](machine/integration-map.json)).

## Publication-path handoff

`content/wp-3-magnum/` is an acceptable construction staging area only. After
WP-1 merges its ontology and release contract, the manuscripts must be moved or
renamed into the governed entity/publication paths selected by WP-1. The
admitted release must bind final Organization, Project, Artist, Work, Curated
Acquisition, Research Publication, Media Reference, and relation IDs, rewrite
relative links, update `INDEX.md`, and regenerate the release manifest. A
visitor-facing `wp-3` path or label is not permitted in the final namespace.
Research memos remain in `notes/wip/wp-3-magnum-research/` as research handoff
material; the staging content root must not remain an orphan WIP-only public
tree after migration.

## Shared-schema integration boundary

WP-1 owns the shared schemas and controlled vocabularies. This corpus does not
add or edit them. The five Works are ready for public projection now; the
canonical, acquisition-independent Work IDs and release-manifest admission
must be assigned through WP-1 on rebase. The exact dependencies and admission
contract are listed in `machine/integration-map.json`; the important ones are:

- `docs/record-model.md` for evidence classes, stable identifiers, and
  append-only corrections;
- `docs/accession-standard.md` for the three linked records, title binding,
  rights, condition, preservation, and completion gates;
- `docs/stream-interoperability.md` for CAIP-19 identity, Stream envelopes,
  provenance shape, `STREAM_ACCESSION_V1`, `STREAM_WORK_DESCRIPTION_V1`,
  `STREAM_RIGHTS_V1`, PREMIS, LIDO, IIIF, and bilateral convergence gates;
- `docs/proposed-gift-wave-standard.md` and
  `docs/wave-storm-publication-standard.md` for the existing proposal and
  signed Storm package;
- `schemas/proposed-gift.schema.json` and
  `schemas/proposed-gift-wave-package.schema.json` for the existing candidate
  records;
- `schemas/object-record.schema.json`, `schemas/rights-statement.schema.json`,
  `schemas/condition-report.schema.json`,
  `schemas/visual-observation.schema.json`,
  `schemas/preservation-manifest.schema.json`, and
   `schemas/transaction-provenance.schema.json` for later accession/object-
   record stewardship, not as a precondition for the public Work projection;
- `schemas/record-envelope.schema.json` and the controlled vocabulary file
  for a later canonical payload, after WP-1 confirms the entity extension
  strategy.

The local machine drafts intentionally do not declare a canonical `$schema`,
invent record types, or manufacture Work IDs. They are a complete WP-1
integration input: the organization, project, artists, Works, Curated
Acquisition, publications, media references, and relations are listed for one
release group in the admission contract.

## What remains before accession-grade Collection publication

The staged public Work projections and selected-acquisition scholarship are ready for review.
For
accession-grade Collection publication, the Museum still needs a live selection result,
donor authority and legal-title instrument, a title binding to the exact
Museum transfer, custody receipt, independent chain verification, object-level
condition and preservation records, written reproduction/display permissions,
archive and caption correspondence, and second-person review. Corrections must
be append-only amendments with `supersedes`; unresolved questions remain
visible ([S37](sources/source-register.md); [integration map](machine/integration-map.json)).

No merge or deployment is authorized by this corpus. The eventual frontend can
present the selected acquisition in its Wave context while formal review
proceeds; Collection counts remain unchanged and one token does not represent
an artist's oeuvre ([S37](sources/source-register.md); [object schedule](machine/object-schedule.json);
[integration map](machine/integration-map.json)).
