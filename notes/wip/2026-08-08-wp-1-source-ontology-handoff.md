# WP-1 source ontology handoff

Date: 2026-08-08
Worker: `019fe093-6890-7d20-9685-e291642d23ef`
Branch: `codex/wp-1-source-ontology`
Initial base: `c01af9f08778c77b823283f81a989cd5f5e24a95`. The branch was rebased cleanly onto exact successor main `36ac78a1172327dab5ba55f7b8f96d6d45dc5d85` after PR #39 merged. This candidate is constructed and review-pending; fresh exact-head independent review is required after the receipt/media amendments.

## Decisions

- The common public record topology is Stream-shaped `PUBLIC_ENTITY`/`PUBLIC_RELATION`, with closed entity profiles and closed relation profiles. It is Museum-native until separately admitted by Stream; no deployment is implied.
- Curated Acquisition IDs are `6529NM-CA-2026-001` The System in Seven States, `...002` Keys and Gates, and `...003` Conflict at Its Edges. These are not accession, program, or proposal IDs.
- Curated Acquisition lifecycle labels are the seven closed labels in `docs/public-entity-ontology.md`. Mint, payment, title, custody, rights, technical, preservation, and display are independent typed facts.
- The Acquisitions area is defined primarily as coherent Curated Acquisition units. Acquisition Programs are separate pathway/mechanism records under the acquisition-program namespace; they link to produced acquisitions and outcomes but never create Collection membership.
- Casey remains accessioned; Keys and Gates remains selected/unminted under existing program `6529NM-AP-01`; Conflict at Its Edges now has a live `WINNER` status observation and is selected by the Museum Wave for acquisition review only. No Exhibition instance is created.
- The exact live readback observed at `2026-08-08T10:15:02.0167151Z` is serial `1276093`, signed `true` as reported by the API, `drop_type: WINNER`, rating/realtime `121603214`, and `29` raters. It is represented by `6529NM-WAVE-OBS-2026-08-08-001`; the earlier `PARTICIPATORY` proposal observation is retained in `prior_observation` and the public lifecycle histories.
- The separate `WAVE_PUBLICATION_OBSERVATION` retains all seven proposal parts, exact UTF-8 source paths and SHA-256 hashes, the five actual CloudFront Wave presentation URLs, credits, rights labels, and separate Arweave token/source locators. This is a signed-drop API readback (`is_signed:true`), not an independently verified cryptographic signature or license determination. The MED-0042 direct visual amendment is observed at `2026-08-08T14:25:44Z` and changes only current visible-facts accessibility text; historical part bytes and hashes remain unchanged.
- Magnum Photos 75 is a separate `PROJECT_OR_SERIES` entity (`6529NM-PRJ-0006`) and Magnum Photos is a separate `ORGANIZATION` entity (`6529NM-ORG-0002`). Evidence-bound organization→project and five project→Work relations describe the retained source context without conflating it with `6529NM-CA-2026-003`, the five independent Work identities, token manifestations, or Collection membership.
- Media is typed and rights/preservation-safe: retained preservation object, Museum derivative, Museum-authored public graphic, token-linked source media, and historical Wave proposal presentation are separate roles. A generic `image_url` is prohibited. The projection contains 31 media entities and 31 `ENTITY_HAS_MEDIA` joins (30 to Works and one historical proposal cover graphic bound to CA-003); every one of the 28 Works has at least one typed displayable media relation, with 7 Casey presentation records, 16 Keys and Gates derivatives, and 5 exact Magnum Wave presentation images. Magnum media is explicitly bound to CA-003 and the linked Work context, without download/zoom/fullscreen or license claims; the Moisés Saman child-subject media carries structural `identity_inference_prohibition` plus non-identifying alt text. The text-only cover is an independently authored Museum graphic with CC0-1.0 rights, no photograph derivation, and no selected-acquisition hero use.

## Generated release inventory

- 118 `PUBLIC_ENTITY` records: 1 Institution, 1 Collection, 21 relational Agent records, 21 public Artist records, 2 Organizations, 6 Project/Series records, 28 acquisition-independent Work records, 3 Curated Acquisitions, 2 Acquisition Programs, 1 Accession, 1 Research Publication, and 31 Media References. HugoFaz is one fixed Agent/Artist authority shared by two Works.
- 153 `PUBLIC_RELATION` records: 28 Artist→Work creator assertions, 28 Curated Acquisition→Work assertions, 16 Program→Work selection assertions, 7 Accession→Work and 7 Collection→Work assertions, 31 typed media joins (30 to Works and one CA-003 historical cover context), 5 Magnum Photos 75 project→Work context assertions, five Art Blocks publisher→Project assertions, one Magnum Photos originator→Project assertion, two Gift Acquisitions→Curated Acquisition production assertions, and the remaining closed project/program/publication/institution relations.
- One `WAVE_STATUS_OBSERVATION` record is included in the 272-record generated projection. Generated entity records are `entity_status: review_pending` in this candidate, never `archived`; a reviewed release will use `entity_status: published`. Generated files are staged completely before deterministic replacement to avoid bootstrap reads of half-materialized media inventories. Fixed candidate construction/created time is `2026-08-08T14:31:26Z`.

## Unresolved

- Stream admission and final shared schema IDs for the Museum-native public projections remain pending; no on-chain schema or contract change belongs in this branch.
- Full Magnum and Keys scholarship remains outside WP-1. The public projection may carry source-backed labels, work sets, and lifecycle facts without claiming a completed acquisition or writing a full artist dossier.
- Casey autonomous generator preservation remains an active stewardship action, not a completed preservation state.
- Media with mutable external sources remains explicitly mutable/unverified until retrieval and fixity evidence exists.
- The recovered independent review completion at `2026-08-08T12:34:35Z` (`019fe15a-2e89-77d3-af4c-a7d93842d2dc`) predates the receipt/media amendments and is not asserted as review metadata for this candidate. Fresh exact-head review must approve the completed candidate before a reviewed/published regeneration. No governance, acquisition, accession, mint, transfer, or deployment action is implied.
- Candidate constructor provenance is deterministic and separate from source observation times: `GENERATED_AT` is the fixed truthful UTC value `2026-08-08T14:31:26Z`; the MED-0042 direct visual observation remains `2026-08-08T14:25:44Z`, and the signed-drop status readback remains `2026-08-08T10:15:02.0167151Z`.
- The exact-head follow-up adds an inventory guard over generator-owned `records/entities` and `records/relations`: `--check` fails on unexpected or missing JSON paths, while write mode refuses only unexpected stale JSON and repairs missing/changed expected outputs. No recursive deletion is performed.

## Verification run to date

The candidate migration `python scripts/migrate_public_entities.py`, `python scripts/validate.py`, and the focused `python -m unittest tests.test_public_entity_layer -v` are the current qualification commands. The focused suite now covers exact counts, human slugs/routes, Work identity aliases, Magnum Photos 75 project relations, manifestation boundaries, all-Work media joins and 640px Keys and Gates derivatives, exact seven-part receipt/media mutation checks, review-pending status, tombstone reuse prevention, Collection=7, the Program/pathway boundary, chain-verified independent mint facts, WINNER history, durable program selection, stable identity/relation/media/observation reorder invariance, evidence-class and label invariance, schema/route/media adversaries, and evidence-path failure. Full repository controls remain to be rerun after this candidate update.

The complete repository suite passes: `python -m unittest discover -s tests -q` ran 200 tests with one platform skip after the successor-main rebase. The remaining control-plane checks pass for bootstrap (595 JSON files), proposed-gift dossiers, fetch guard, rights handbook/legal snapshots, institutional source inventory, program media, Casey diligence, public migration, the public validator, and `python scripts/generate_manifest.py --check`. The final release manifest is current with Keccak-256 `0x80ebacd53d08526e078e1d49ceeb86e9f80545fd4afa2394816b1fb36f8faab7` and SHA-256 `sha256:eaf55473b5cfbae60d504e7a9da095818a99802748708506ed5a4ac553a8210c`.

## Control boundary

This handoff records source design and implementation status only. It does not merge, deploy, mint, purchase, transfer, establish custody, grant rights, advance governance, or advance accession state.

## 2026-08-08 second-panel fail-closed correction

Exact candidate `71a94cb0e30000462337ffc38a9b56692f515838`
passed hosted run `31275658396`, but all four independent exact-head lanes
rejected its validators. The records themselves were confirmed safe and no
catalog activation existed. The follow-up correction closes the reported
admissible-state gaps:

- Collection, Project, Curated Acquisition, and Accession Work sets must equal
  their active relations in both directions. Permanent Collection membership
  requires one matching Collection relation. Typed Work targets resolve
  uniquely under a closed component/manifestation matrix.
- Restricted and unknown-rights media are structurally metadata-only:
  `visual:false`, null source and token locators, and no rendering or delivery
  affordances.
- Stream adaptation now pins literal lowercase `https://`, Museum Keccak/JCS
  content hashes, exact JSON manifest-entry commitments, preimage/record-type
  pairs, nonzero identities, closed hash-reference forms, URI bounds, and
  authorization classes 1-8.
- Candidate A and reviewed B visitor-bundle entries must equal their exact
  Git-tree source bytes. Activation and rollback verify the current active
  pointer and catalog against retained HEAD bytes before any write, while a
  repository with no retained pointer still supports its first activation.

Adversarial coverage was added for each boundary. The combined local matrix is
green: 261 tests with one expected Windows named-pipe skip, 621-file bootstrap
validation, full Museum/Casey semantic validation, deterministic migration,
inventory, bundle, and manifest checks, rights/legal checks, 48-derivative
media verification, institutional-source verification, Casey package and
diligence verification, Python compilation, and Windows-aware diff hygiene.

The corrected review-pending tree still has 118 entities and 164 relations. Its
closed visitor inventory has 420 entries; the atomic bundle has 419 documents
and 3,079,537 UTF-8 content bytes. Before this handoff update, the regenerated
whole-release manifest had 692 entries, SHA-256
`sha256:011ac757046b8aec9ce89b8d0f85a91b47806bd2dc75d785f7b0728a26e35078`,
and Keccak-256
`0x4b8ca73a385cafd87bd79dd3749bc40bf82d23617f205b442e80627d887503d3`.
Because this handoff is itself governed, the manifest is regenerated again
before commit and the committed exact commitments supersede these provisional
values. Fresh hosted CI and four fresh exact-head reviews remain mandatory.
