# WP-1 source ontology handoff

Date: 2026-08-08
Worker: `019fe093-6890-7d20-9685-e291642d23ef`
Branch: `codex/wp-1-source-ontology`
Initial base: `c01af9f08778c77b823283f81a989cd5f5e24a95`. The branch was rebased cleanly onto exact successor main `36ac78a1172327dab5ba55f7b8f96d6d45dc5d85` after PR #39 merged. The post-rebase projection and manifest were independently reviewed before publication.

## Decisions

- The common public record topology is Stream-shaped `PUBLIC_ENTITY`/`PUBLIC_RELATION`, with closed entity profiles and closed relation profiles. It is Museum-native until separately admitted by Stream; no deployment is implied.
- Curated Acquisition IDs are `6529NM-CA-2026-001` The System in Seven States, `...002` Keys and Gates, and `...003` Conflict at Its Edges. These are not accession, program, or proposal IDs.
- Curated Acquisition lifecycle labels are the seven closed labels in `docs/public-entity-ontology.md`. Mint, payment, title, custody, rights, technical, preservation, and display are independent typed facts.
- The Acquisitions area is defined primarily as coherent Curated Acquisition units. Acquisition Programs are separate pathway/mechanism records under the acquisition-program namespace; they link to produced acquisitions and outcomes but never create Collection membership.
- Casey remains accessioned; Keys and Gates remains selected/unminted under existing program `6529NM-AP-01`; Conflict at Its Edges now has a live `WINNER` status observation and is selected by the Museum Wave for acquisition review only. No Exhibition instance is created.
- The exact live readback observed at `2026-08-08T10:15:02.0167151Z` is serial `1276093`, signed `true`, `drop_type: WINNER`, rating/realtime `121603214`, and `29` raters. It is represented by `6529NM-WAVE-OBS-2026-08-08-001`; the earlier `PARTICIPATORY` proposal observation is retained in `prior_observation` and the public lifecycle histories.
- Magnum Photos 75 is a separate `PROJECT_OR_SERIES` entity (`6529NM-PRJ-0006`) and Magnum Photos is a separate `ORGANIZATION` entity (`6529NM-ORG-0002`). Evidence-bound organization→project and five project→Work relations describe the retained source context without conflating it with `6529NM-CA-2026-003`, the five independent Work identities, token manifestations, or Collection membership.
- Media is typed and rights/preservation-safe: retained preservation object, Museum derivative, token-linked source media, and signed-Wave proposal presentation are separate roles. A generic `image_url` is prohibited. The projection contains 31 media entities and 31 `ENTITY_HAS_MEDIA` joins (30 to Works and one grouped Institution cover); every one of the 28 Works has at least one typed displayable media relation, with 7 Casey presentation records, 16 Keys and Gates derivatives, and 5 exact Magnum signed-Wave images. Magnum media is proposal-context-only, without download/zoom/fullscreen; the Moisés Saman child-subject alt text is non-identifying by validation.

## Generated release inventory

- 119 `PUBLIC_ENTITY` records: 1 Institution, 1 Collection, 22 relational Agent records, 21 public Artist records, 2 Organizations, 6 Project/Series records, 28 acquisition-independent Work records, 3 Curated Acquisitions, 2 Acquisition Programs, 1 Accession, 1 Research Publication, and 31 Media References.
- 152 `PUBLIC_RELATION` records: 28 Artist→Work creator assertions, 28 Curated Acquisition→Work assertions, 16 Program→Work selection assertions, 7 Accession→Work and 7 Collection→Work assertions, 31 typed media joins (30 to Works and one grouped Institution cover), 5 Magnum Photos 75 project→Work context assertions, one Magnum Photos organization→project assertion, and the remaining closed project/program/publication/institution relations.
- One `WAVE_STATUS_OBSERVATION` record is included in the 272-record generated projection. Generated files are staged completely before deterministic replacement to avoid bootstrap reads of half-materialized media inventories.

## Unresolved

- Stream admission and final shared schema IDs for the Museum-native public projections remain pending; no on-chain schema or contract change belongs in this branch.
- Full Magnum and Keys scholarship remains outside WP-1. The public projection may carry source-backed labels, work sets, and lifecycle facts without claiming a completed acquisition or writing a full artist dossier.
- Casey autonomous generator preservation remains an active stewardship action, not a completed preservation state.
- Media with mutable external sources remains explicitly mutable/unverified until retrieval and fixity evidence exists.
- Final independent review is bound to `codex-review:019fe15a-2e89-77d3-af4c-a7d93842d2dc`; all generated records are reviewed/published-state projections. No governance, acquisition, accession, mint, transfer, or deployment action is implied.

## Verification run to date

`python scripts/migrate_public_entities.py --reviewed --reviewer-id codex-review:019fe15a-2e89-77d3-af4c-a7d93842d2dc`, `python scripts/bootstrap_validate.py`, `python scripts/validate.py`, and `python -m unittest tests.test_public_entity_layer -v` pass on the final reviewed projection. The focused suite has 12 tests covering exact counts, human slugs/routes, Work identity aliases, Magnum Photos 75 project relations, manifestation boundaries, all-Work media joins, Collection=7, the Program/pathway boundary, WINNER history, durable program selection, schema/route/media adversaries, and evidence-path failure.

The complete repository suite passes: `python -m unittest discover -s tests -q` ran 200 tests with one platform skip after the successor-main rebase. The remaining control-plane checks pass for bootstrap (595 JSON files), proposed-gift dossiers, fetch guard, rights handbook/legal snapshots, institutional source inventory, program media, Casey diligence, public migration, the public validator, and `python scripts/generate_manifest.py --check`. The final release manifest is current with Keccak-256 `0x80ebacd53d08526e078e1d49ceeb86e9f80545fd4afa2394816b1fb36f8faab7` and SHA-256 `sha256:eaf55473b5cfbae60d504e7a9da095818a99802748708506ed5a4ac553a8210c`.

## Control boundary

This handoff records source design and implementation status only. It does not merge, deploy, mint, purchase, transfer, establish custody, grant rights, advance governance, or advance accession state.
