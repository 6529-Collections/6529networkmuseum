# WP-3 Magnum Photos scholarship corpus

Status: WP-3 construction staging area with public Work projections ready for
WP-1 admission on rebase. This directory is not the final public canonical
namespace, is not an accession package, and does not change any shared schema or
controlled vocabulary. The admission contract is
`machine/integration-map.json`; the current closed release manifest does not
include this staging root.

## What this corpus is

This corpus deepens proposed gift `6529NM-PG-2026-001` into the intellectual
and evidentiary shape required for the Museum's current proposal publication
and for a later Museum publication if the proposal is selected and the
subsequent acquisition gates are completed. Its working Curated Acquisition
identity is `6529NM-CA-2026-003`, a stable content
identifier only. It is not an accession number and does not reserve one.

The corpus supplies a typed handoff for the WP-1 public ontology:

- **Organization:** Magnum Photos.
- **Project or Series:** Magnum Photos 75, an upstream 2022 archive and
  blockchain publication project.
- **Artists:** David Seymour, Larry Towell, Micha Bar-Am, Moises Saman, and
  Lorenzo Meloni.
- **Works:** five public Work projections for the exact token-linked
  photographs, with lifecycle `proposed_in_museum_wave` and collection
  membership `not_in_collection`. Acquisition-independent Work IDs are left
  null for WP-1 assignment; proposal object IDs remain typed aliases.
- **Curated Acquisition:** *Conflict at Its Edges*, the donor-formed,
  proposed five-work unit.
- **Research Publications:** the institutional and project profiles, artist
  profiles, object entries, essays, chronologies, and evidence dossiers in
  this staging directory; final governed publication paths are assigned during
  WP-1 admission.
- **Components and manifestations:** the ERC-721 tokens, token metadata,
  Arweave image pointers, and any future Museum derivative. The source image,
  token, legal title, copyright, display permission, and Museum custody remain
  separate facts.

## Live status boundary

The parent Museum Wave is the decision authority. A read-only authenticated
`punk6529bot drops get 002bfa4f-8416-48bf-b35e-38f354e9a9f0 --json` observation
on 2026-08-08 recorded:

- title: *Conflict at Its Edges*;
- serial: `1276093`;
- signed: `true`;
- live `drop_type`: `PARTICIPATORY`;
- Wave: `6529 Network Museum`,
  `5f207393-5418-4a75-8738-e40edb44a94d`;
- realtime rating: `122969240` and raters: `29` at that observation;
- observation time: `2026-08-08T09:06:07.985Z` UTC.

The rating is preserved only as a mutable observation. It is not interpreted as
adoption. The proposal remains proposed and the selection outcome is not
established by this corpus. The Work projections therefore use
`proposed_in_museum_wave`, `collection_membership: not_in_collection`, and
null accession/title-binding/custody fields. The proposal may appear in an
active Acquisitions hub as
**Proposed in the Museum Wave** while the drop is open; if it later closes
without selection, the stable page becomes archival and leaves that active
index.

The source package remains the proposal's historical decision record:
`records/proposed-gifts/6529NM-PG-2026-001/`. Its finalized Ethereum
observation at block `25690178` established a point-in-time owner and
token-level approval state for all five tokens. That is chain evidence for the
proposal, not donor-authority, legal-title, copyright, Museum-custody, or
accession evidence. The live Wave state must be re-read before any future
acceptance action.

## Corpus inventory

| Layer | File or directory | Purpose |
| --- | --- | --- |
| Entity profiles | `entities/` | Magnum Photos, Magnum Photos 75, and the proposed Curated Acquisition |
| Artist profiles | `artists/` | Five practice-led profiles with exact-work placement |
| Works | `works/` | Five public Work projections and substantial object essays |
| Essays | `essays/` | Group essay and acquisition narrative |
| Dossiers | `dossiers/` | Captions, evidence, chronologies, rights, technical, provenance, and media plan |
| Sources | `sources/` | Claim-addressable bibliography and source register |
| Machine drafts | `machine/` | Work projections, token/component schedule, media join, and WP-1 release admission contract |
| Review | `reviews/` | Editorial checks, unresolved questions, and release boundary |

The work entries are ordered chronologically for interpretation: Seymour
(1952), Towell (1986), Bar-Am (1989), Saman (2011), and Meloni (2016). The
token IDs are not the sequence of the photographs' histories. The metadata
`Sequence` values such as `44/225` are preserved as issuer metadata and are
not treated as proof that all 225 announced works were minted.

## Evidence method

Every substantial claim is written with one of the Museum's evidence classes:

- **A — direct chain or token observation:** contract, token ID, URI,
  finalized block, transfer, owner, approval, or retrieved bytes;
- **B — authoritative issuer, artist, estate, archive, institutional, or
  governance source:** Magnum, an artist archive, ICP, UNESCO, World Press
  Photo, a signed Wave record, or an equivalent primary authority;
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
2026-08-08. Their bytes were not added to this repository. The signed Wave
Storm proposal already published those exact upstream URLs as its five work
media items. The machine-readable join in
`machine/wave-media-join.json` permits a frontend to reference or embed those
historical proposal-display URLs in the proposal's Wave context only, with the
artist/Magnum credit, `All Rights Reserved`, and an explicit `Wave-source`
label. It does not promise download, full-resolution delivery, preservation,
or a new derivative.

No JPEG, AVIF, WebP, thumbnail, share card, IIIF manifest, tiled derivative,
or responsive `srcset` is generated here. The issuer metadata for every object
states `All Rights Reserved`; the historical Magnum terms do not establish a
general Museum copyright or Collection-publication grant. Arweave persistence
and a matching SHA-256 do not create permission. Future Collection pages,
download links, IIIF, and preservation masters remain blocked pending written,
component-specific rights evidence and a reviewed media manifest.

The rights/technical dossier defines a fail-closed media ladder. Derivatives
may be generated only after written rights evidence identifies the permitted
use, the source bytes are retained or re-retrievable under an approved
preservation plan, and a later reviewed manifest binds every derivative to the
source hash. A future page must show a rights-blocked state rather than
silently substituting an unlicensed image. The proposal's square cover is a
separate Museum-authored CC0 asset and is not reused as a photograph
derivative.

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

The staged public Work projections and proposal scholarship are ready for review.
For
accession-grade Collection publication, the Museum still needs a live selection result,
donor authority and legal-title instrument, a title binding to the exact
Museum transfer, custody receipt, independent chain verification, object-level
condition and preservation records, written reproduction/display permissions,
archive and caption correspondence, and second-person review. Corrections must
be append-only amendments with `supersedes`; unresolved questions remain
visible.

No merge or deployment is authorized by this corpus. The eventual frontend
should expose the proposed gift in its Wave context until those gates clear;
it must not add the five works to permanent Collection counts or imply that one
token represents an artist's oeuvre.
