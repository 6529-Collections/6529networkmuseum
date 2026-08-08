# Keys and Gates — accessibility and public-size amendment

**Record ID:** `6529NM-AP-01-MEDIA-ACCESSIBILITY-2026-08-08-003`<br>
**Supersedes for current publication state:** [`6529NM-AP-01-MEDIA-ACCESSIBILITY-2026-08-08-001`](accessibility-amendment.md) and [`6529NM-AP-01-MEDIA-ACCESSIBILITY-2026-08-08-002`](accessibility-amendment-2026-08-08-002.md)<br>
**Record type:** derived publication amendment<br>
**Revision:** 1<br>
**Issued:** 8 August 2026<br>
**Constructor:** 6529 Network Museum, Curatorial Research<br>
**Scope:** current accessibility projection, per-work public derivative restrictions, and typed program-media output

This append-only follow-up corrects the current publication state without rewriting the historical amendments or immutable selected-outcome/source records. The constructor-only status was not independent review: the prior “reviewed” status cannot be treated as approval. The current root and typed status therefore return to `constructed_visual_description_pending_independent_review`; an independent visual reviewer must approve the final sixteen descriptions before that status changes.

## Superseded and current projections

| Projection | Superseded value | Current value |
|---|---|---|
| Accessibility root `status` | `constructed_visual_description_reviewed` | `constructed_visual_description_pending_independent_review` |
| Typed manifest `presentation.alt_text_status` for all 16 items | `constructed_visual_description_reviewed` | `constructed_visual_description_pending_independent_review` |
| OUT-008 `alt_text` | A vertical aerial view shows dense homes meeting an abrupt, unbroken edge of green forest. | A vertical aerial view shows dense residential roofs meeting an ordered palm plantation along a sharp boundary. |
| OUT-011 `public_widths` | `[640, 1280, 2400]` | `[640]` |
| OUT-011 public derivatives | 640, 1280, and 2400 presentation variants | 640 only; 1280 and 2400 withdrawn from this public release |

The accessibility projection, Work image alts, media-join text, and typed manifest now carry the same sixteen canonical descriptions. OUT-002 retains the central performer; OUT-011 identifies a booklet/document rather than a phone and states that its text is not legible at the approved size; OUT-013 preserves the separation between `NO / WHERE / TO` and the Esc key.

## Historical OUT-013 location note

The retained historical program prose says: “An ant is enclosed inside the key marked Esc.” The current reviewed 640 derivative shows the ant beside and below the Esc key. The current accessibility description follows the direct visual audit: “Black keyboard keys spell NO / WHERE / TO on a white surface, while the Esc key sits apart below beside a small ant.” The earlier sentence remains historical source text and is not silently rewritten; the derived publication projection records the correction boundary.

## OUT-011 presentation restriction and local fixity

The public release links and publishes only the 640px OUT-011 surrogate. The 1280px and 2400px derivatives are presentation surrogates, not source originals or preservation masters, and are not public/downloadable in this edition because their greater detail makes the booklet cover more legible. Their prior local fixity remains recorded for lineage:

| Width | Prior byte size | Prior SHA-256 |
|---:|---:|---|
| 1280 | 43,850 | `sha256:00f3ff73be1cfff57a5ddf3ae9890cd9a49e1de547c5883cd1ac405bcda6f985` |
| 2400 | 104,860 | `sha256:c704956b390385b6c8f2c9158455292618b8237aa3355ff6b0a2615b3f62c251` |

The source JPEG remains represented by its existing source hash in the typed manifest; source originals are not added to this repository.

## Integrity and lineage

| File | Superseded SHA-256 at head `287aa7f` | Current SHA-256 |
|---|---|---|
| `media/programs/6529NM-AP-01/accessibility.json` | `sha256:ea59d3e3053c996143b956617c16309cc34982f21107c31c523860484ba200d9` | `sha256:3a296516f19a2ef1028cfabd6004a1858d0f7eb07b5fd55d6265ae2ca9c90858` |
| `records/programs/6529NM-AP-01/media-manifest.json` | `sha256:b8be1be1046f0dd79ffbd55d970838f42b4330f3de5d5193117bc184ae228098` | `sha256:798df3807f67736083af2feaf441c0534c1afa3a37b3af0a8b71546186817f42` |

The selected-outcome IDs, `selected_unminted` statuses, source hashes, remaining derivative hashes, and per-outcome `rights_effective_status` values remain unchanged. This amendment is accessibility and presentation-control evidence; it is not a claim of legal identity, consent, authorship, acquisition, accession, minting, custody, or unrestricted reuse. The [rights and consent boundary](rights-and-consent.md) controls the image-specific publication questions.

## Revision history

- **1 · 8 August 2026:** Returned constructor-only accessibility status to pending independent review; corrected OUT-008; limited OUT-011 to the 640 surrogate; recorded the OUT-013 historical-location distinction; and synchronized public Work, media-join, accessibility, and typed-manifest projections.
