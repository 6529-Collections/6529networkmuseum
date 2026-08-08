# WP-1 publication integration handoff

This handoff keeps the Keys and Gates public corpus ready for admission to the canonical typed release. It is content and routing metadata only; it does not redefine a shared schema or claim that typed publication activation has happened.

## Admission state

| Subject | Current public route | Canonical typed ID |
|---|---|---|
| Acquisition Program | records/programs/6529NM-AP-01/program.json | 6529NM-AP-01 |
| Curated Acquisition | curated-acquisition.md | 6529NM-CA-2026-002 |
| Research Publication | curatorial-essay.md | WP-1 publication ID to be assigned |
| Artist entities | artists/*.md | WP-1 Artist IDs to be assigned |
| Work entities | works/*.md | WP-1 Work IDs to be assigned |
| Media references | media-joins.md and ../media-manifest.json | Existing program media-manifest item IDs |

The current branch is pending WP-1 admission. The public pages are complete as editorial routes and the written scholarship is complete as constructed text, but exact-commit independent review, accessibility, image display, sensitive-subject authorization, and image delivery remain pending. OUT-004, OUT-010, and OUT-011 images are not approved for delivery. The branch must still be rebased onto the WP-1 ontology/release work before it can claim a typed release activation.

## Identity rule

OUT-001 through OUT-016 are Acquisition Program selected-outcome/source IDs. They are retained as aliases and typed source relations. They are not canonical public Work entity IDs.

Artist handles are public names and source aliases. They are not canonical Artist entity IDs. WP-1 must assign independent, stable Work and Artist IDs while preserving the page routes and the source aliases below.

The title-slug routes below are stable presentation routes, not canonical Work or Artist IDs. The public URL must continue to identify the work or artist by its page route while the typed release binds that page to the independent WP-1 entity ID.

## Artist route admission

| Public name / handle | Route | Selected source aliases |
|---|---|---|
| Gül Yıldız / GulYildiz | artists/gulyildiz.md | OUT-001 |
| Hugo Faz / HugoFaz | artists/hugofaz.md | OUT-002, OUT-011 |
| Nasim Ghanizadeh / nasimghanizadeh | artists/nasimghanizadeh.md | OUT-003 |
| intrepid | artists/intrepid.md | OUT-004 |
| IKERTJE / ikertje | artists/ikertje.md | OUT-005 |
| Artem Humilevskiy / GIANT | artists/giant.md | OUT-006 |
| Priyanka Patel / priyanka | artists/priyanka.md | OUT-007 |
| Rakesh Pulapa / Rakesh | artists/rakesh.md | OUT-008 |
| Eric Pan / pandelic | artists/pandelic.md | OUT-009 |
| Minalisa | artists/minalisa.md | OUT-010 |
| Teyhu | artists/teyhu.md | OUT-012 |
| arsonic | artists/arsonic.md | OUT-013 |
| Zoku | artists/zoku.md | OUT-014 |
| Shams Pranto / shamspranto | artists/shamspranto.md | OUT-015 |
| Veerendra | artists/veerendra.md | OUT-016 |

## Work route admission

| Source alias | Public route | Artist route | Collection membership |
|---|---|---|---|
| OUT-001 | works/take-the-key.md | artists/gulyildiz.md | not_in_collection |
| OUT-002 | works/the-artist-in-teh-open-sea.md | artists/hugofaz.md | not_in_collection |
| OUT-003 | works/managed-freedom.md | artists/nasimghanizadeh.md | not_in_collection |
| OUT-004 | works/no-key-only-light.md | artists/intrepid.md | not_in_collection |
| OUT-005 | works/residual-barrier.md | artists/ikertje.md | not_in_collection |
| OUT-006 | works/the-hostile-gate.md | artists/giant.md | not_in_collection |
| OUT-007 | works/the-cost-of-open.md | artists/priyanka.md | not_in_collection |
| OUT-008 | works/dichotomy.md | artists/rakesh.md | not_in_collection |
| OUT-009 | works/now-is-our-time.md | artists/pandelic.md | not_in_collection |
| OUT-010 | works/checkpoint.md | artists/minalisa.md | not_in_collection |
| OUT-011 | works/sina-beizavi-in-brazil.md | artists/hugofaz.md | not_in_collection |
| OUT-012 | works/rusted.md | artists/teyhu.md | not_in_collection |
| OUT-013 | works/nowhere-to-esc.md | artists/arsonic.md | not_in_collection |
| OUT-014 | works/morning-glory.md | artists/zoku.md | not_in_collection |
| OUT-015 | works/fight-for-freedom.md | artists/shamspranto.md | not_in_collection |
| OUT-016 | works/no-access.md | artists/veerendra.md | not_in_collection |

## Typed relation handoff

After WP-1 supplies the canonical entity shape, admit the following relations without changing the editorial routes:

    Acquisition Program 6529NM-AP-01
      -> governs / produces -> Curated Acquisition 6529NM-CA-2026-002
    Curated Acquisition 6529NM-CA-2026-002
      -> has selected source outcome -> OUT-001 ... OUT-016
    Work [WP-1 Work ID]
      -> has source alias -> OUT-###
      -> created by -> Artist [WP-1 Artist ID]
      -> collection membership -> not_in_collection
      -> has presentation reference -> media-manifest item for OUT-###
    Research Publication [WP-1 Publication ID]
      -> interprets -> Curated Acquisition 6529NM-CA-2026-002
      -> discusses -> Work and Artist entities

The relation set must not create an accession, title binding, custody event, mint, token, purchase, or rights grant. The visitor status remains: **Selected through the Keys and Gates acquisition program; acquisition pending. Not yet minted; minting route under consideration.**

## Integration acceptance checks

1. Rebase this branch onto current source main, then onto the WP-1 ontology/release commit when available.
2. Assign independent canonical Work and Artist IDs while retaining every OUT alias, handle, public route, and source relation.
3. Admit the Program, Curated Acquisition, 15 Artist entities, 16 Work entities, Research Publication, media references, and typed relations to the canonical release/manifest.
4. Regenerate and check the repository release manifest after admission; preserve source-policy records and existing INDEX.md/orchestration updates.
5. Run the complete validator, public link/anchor inventory, media join checks, and UTF-8/no-mojibake check.
