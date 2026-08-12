# Keys and Gates publication integration — current state

**Record ID:** `6529NM-AP-01-PUBLICATION-INTEGRATION-2026-08-08`<br>
**Scope:** current illustrated accession-publication candidate for Curated Acquisition `6529NM-CA-2026-002`<br>
**Record role:** public integration state; not a schema, release manifest, catalog, acquisition, accession, or rights decision

The typed projection is now present as a governed, review-pending candidate. It
keeps the source aliases, public routes, and independent lifecycle facts
separate. No entity is `published`, and no typed projection claims minting,
purchase, title, custody, accession, Collection membership, or display
authorization.

**Visitor state:** Selected through the Keys and Gates acquisition program;
acquisition pending. **Mint qualifier:** Not yet minted; minting route under consideration.

## Governed typed state

| Projection | Typed identity | Public source | Current status |
|---|---|---|---|
| Program | `6529NM-AP-ENT-0002` (source alias `6529NM-AP-01`) | [program record](../program.json) | `review_pending` |
| Curated Acquisition (CA) | `6529NM-CA-2026-002` | [Curated Acquisition](curated-acquisition.md) | `review_pending` |
| Artist | `6529NM-ART-0002`–`6529NM-ART-0016` (15 entities) | [artist profile example](artists/gulyildiz.md) and sibling `artists/*.md` pages | `review_pending` |
| Work | `6529NM-W-0008`–`6529NM-W-0023` (16 entities) | [Work page example](works/take-the-key.md) and sibling `works/*.md` pages | `review_pending` |
| Media | `6529NM-MED-0020`–`6529NM-MED-0035` (16 entities) | [media joins](media-joins.md) and [program media manifest](../media-manifest.json) | `review_pending` |
| Research Publication (RP) | `6529NM-RP-0002` (new) | [Access, Control, and Exit](curatorial-essay.md) | `review_pending` |

The Program governs the CA; the CA retains the sixteen selected outcome
aliases; each Work retains its OUT alias, Artist creator, `not_in_collection`
state, and typed Media reference; and RP `6529NM-RP-0002` interprets the CA
and discusses its Works and Artists. The new RP identity is recorded here as
review-pending integration state; its exact catalog pointer is not yet
available.

## Current public boundary

The Work pages combine captions, close looking, sources, and typed Media
references. All sixteen Works have Museum-hosted WebP presentation media under
[the current display authority](media-display-authorization-amendment-2026-08-11.md).
Fourteen use 640, 1280, and 2400 pixel derivatives; OUT-004 and OUT-011 use the
640 pixel derivative only. The images appear in program, acquisition, artist,
and Work contexts without download, IIIF, preservation-master, mint, title,
custody, accession, or Collection claims. All sixteen accessibility
descriptions are `constructed_visual_description_reviewed` under the
[independent review record](accessibility-review-2026-08-11.md).

The special image cautions remain explicit: OUT-004 has unverified
depicted-figure ages and consent/privacy scope; OUT-010 has unresolved identity,
adult-status, self-portrait, and consent/publication-scope questions; and
OUT-011 has unresolved direct subject approval, document legibility, venue
permission, sensitive biography, and publication scope. Historical technical
derivation remains in the append-only source record.

## Relations and activation gate

The public relationship set remains:

    Program 6529NM-AP-ENT-0002
      -> produces -> Curated Acquisition 6529NM-CA-2026-002
    Curated Acquisition 6529NM-CA-2026-002
      -> brings together -> Work 6529NM-W-0008 ... 6529NM-W-0023
    Work
      -> created by -> Artist
      -> has media -> Media
    Research Publication 6529NM-RP-0002
      -> interprets -> Curated Acquisition 6529NM-CA-2026-002
      -> discusses -> Work and Artist

Public activation remains pending a fresh exact-commit independent review and a
catalog pointer/readback that binds RP `6529NM-RP-0002`, the governed typed
records, the illustrated candidate, and the atomic visitor release. Until both
gates are complete, this record must not be treated as a published catalog
entry or activation receipt.

The [institutional record](institutional-record.md), [media joins](media-joins.md),
[rights and consent record](rights-and-consent.md), and [curatorial essay](curatorial-essay.md)
remain the supporting public record. Source aliases `OUT-001` through
`OUT-016` and the public page routes remain unchanged.
