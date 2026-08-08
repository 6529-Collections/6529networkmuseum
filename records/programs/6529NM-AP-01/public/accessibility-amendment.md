# Keys and Gates — accessibility amendment

**Record ID:** `6529NM-AP-01-MEDIA-ACCESSIBILITY-2026-08-08-001`<br>
**Record type:** derived publication amendment<br>
**Revision:** 1<br>
**Issued:** 8 August 2026<br>
**Constructor:** 6529 Network Museum, Curatorial Research<br>
**Scope:** public accessibility projection and typed program-media presentation output

This append-only record documents the completed visual audit of the sixteen selected-work presentation derivatives. It supersedes the earlier accessibility projection and the corresponding typed manifest wording without rewriting the immutable selected-outcome source records or changing any derivative bytes.

## Superseded and revised projections

| Projection | Superseded value | Revised value |
|---|---|---|
| Accessibility root `status` | `constructed_visual_description_pending_independent_review` | `constructed_visual_description_reviewed` |
| Typed manifest `presentation.alt_text_status` for all 16 items | `constructed_visual_description_pending_independent_review` | `constructed_visual_description_reviewed` |
| `6529NM-AP-01-OUT-002` | An elevated night view of buses and blurred vehicles moving through a lit transit station bordered by trees. | An elevated view shows blurred buses and traffic around a sharply defined performer seated in a small white tub or boat on the roadway. |
| `6529NM-AP-01-OUT-011` | A man wearing sunglasses reclines nude on an ornate gold chair in a dark room while holding a phone. | A nude figure reclines on an ornate gold chair, wearing bright sandals and holding a small dark booklet or document; its text is not legible at the public derivative scale. |
| `6529NM-AP-01-OUT-016` | A small white house with a red roof stands on a green hill at night above an illuminated gate under a starry sky. | A small white house with a red roof stands on a hill beneath a starry sky, beyond a lit gate with a warning sign and a person-like silhouette. |

The other thirteen descriptions were retained after comparison with the public presentation derivatives. The audit confirms exactly sixteen accessibility items, exactly sixteen typed manifest items, three deterministic derivatives per item, and a one-to-one join among selected source outcomes, accessibility records, media-manifest items, and public Work routes. The public derivative for OUT-011 does not make personal document identifiers legible at the standard 640px presentation size; no identifier is transcribed here.

## Integrity and boundary

| File | Superseded SHA-256 | Revised SHA-256 |
|---|---|---|
| `media/programs/6529NM-AP-01/accessibility.json` | `sha256:62bcf67437a29f2745654c6de24480fb7cee22eeffd29a970407633c08919abb` | `sha256:48337baf91adb7d50beb43c65275e33d1c04f22a8ced32416683c663ba42c96e` |
| `records/programs/6529NM-AP-01/media-manifest.json` | `sha256:1b57932e3395ac3c4b0eab05930068f5af3096ac06a5989c0797efbc3fe988a6` | `sha256:7f18d61c2ff6ae547c1e80384334ddc8966fae803cbee67346da3c5e6f29d7f2` |

The source outcome JSON files, source hashes, derivative paths, derivative hashes, `selected_unminted` statuses, and per-outcome `rights_effective_status` values are unchanged. The revised descriptions are visual accessibility text, not claims of legal identity, consent, authorship, acquisition, accession, minting, custody, or unrestricted reuse. Rights and sensitive-person treatment remain governed by the [rights and consent boundary](rights-and-consent.md) and the work-specific source notes.

## Revision history

- **1 · 8 August 2026:** Completed the sixteen-image visual audit; corrected OUT-002, OUT-011, and OUT-016; promoted the accessibility status from pending review to reviewed; and synchronized the typed manifest.
