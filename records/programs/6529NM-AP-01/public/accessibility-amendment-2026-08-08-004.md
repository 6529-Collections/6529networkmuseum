# Keys and Gates — OUT-011 media-enforcement amendment

**Record ID:** `6529NM-AP-01-MEDIA-ACCESSIBILITY-2026-08-08-004`<br>
**Supersedes for this enforcement assertion:** [amendment 003](accessibility-amendment-2026-08-08-003.md)<br>
**Record type:** derived publication amendment<br>
**Revision:** 1<br>
**Issued:** 8 August 2026<br>
**Constructor:** 6529 Network Museum, Curatorial Research<br>
**Scope:** exact OUT-011 public-key withdrawal, invalidation, and post-change readback

This append-only amendment supplements the current accessibility and
per-work-size projection in amendment 003. It supersedes only the earlier
qualified statement that the OUT-011 1280px and 2400px keys were withheld from
the edition pending delivery verification. The accessibility text, pending
independent-review status, source hash, 640px derivative, and rights status
remain unchanged.

## Enforced public projection

OUT-011 is published at 640px only. The exact 1280px and 2400px presentation
keys were removed from the delivery origin, and the distribution cache was
invalidated. The 640px key was retained. No other program media key is covered
by this mutation.

| Width | Public URL | Post-invalidation readback | Current treatment |
|---:|---|---|---|
| 640 | `https://d3lqz0a4bldqgf.cloudfront.net/museum/programs/6529NM-AP-01/6529NM-AP-01-OUT-011/4d7c6e452638a6dd091253bf1cc2c5b14e141920dd72a28dab5085bb7b4526fc/webp-v2-q82-m6-fixed-icc/640.webp` | HTTP 200; 15,306 bytes | Retained public derivative |
| 1280 | `https://d3lqz0a4bldqgf.cloudfront.net/museum/programs/6529NM-AP-01/6529NM-AP-01-OUT-011/4d7c6e452638a6dd091253bf1cc2c5b14e141920dd72a28dab5085bb7b4526fc/webp-v2-q82-m6-fixed-icc/1280.webp` | HTTP 404 | Withdrawn; prior local bytes retained only for lineage |
| 2400 | `https://d3lqz0a4bldqgf.cloudfront.net/museum/programs/6529NM-AP-01/6529NM-AP-01-OUT-011/4d7c6e452638a6dd091253bf1cc2c5b14e141920dd72a28dab5085bb7b4526fc/webp-v2-q82-m6-fixed-icc/2400.webp` | HTTP 404 | Withdrawn; prior local bytes retained only for lineage |

The invalidation completed at `2026-08-08T12:49:27Z` under invalidation ID
`I8YFV5J3W4GCFQCZNXU39X6VYQ`. The readback was performed with browser-like
GET requests after completion. The exact delivery distribution and origin
binding were read-bound for this operation:

| Institutional source field | Exact value |
|---|---|
| CloudFront distribution | `ECGWRHUV1NM3I` |
| Origin bucket | `6529bucket` |

These infrastructure identifiers are source-layer evidence and are
deliberately omitted from visitor Work, Artist, Acquisition, and essay pages.

## Withdrawn-byte lineage

The larger files were presentation surrogates, not source originals or
preservation masters. Their prior local fixity remains recorded so the
withdrawal is reproducible as an append-only change:

| Width | Prior byte size | Prior SHA-256 |
|---:|---:|---|
| 1280 | 43,850 | `sha256:00f3ff73be1cfff57a5ddf3ae9890cd9a49e1de547c5883cd1ac405bcda6f985` |
| 2400 | 104,860 | `sha256:c704956b390385b6c8f2c9158455292618b8237aa3355ff6b0a2615b3f62c251` |

The retained OUT-011 source hash is
`sha256:4d7c6e452638a6dd091253bf1cc2c5b14e141920dd72a28dab5085bb7b4526fc`.
The 640px derivative remains generated under
`6529NM_WEB_PRESENTATION_WEBP_V2_Q82_M6_FIXED_ICC`; its current manifest
fixity is `sha256:14eea8754ea08d39dd5fe39d93f2f69dbce8e18e9f550a10f7e76bc6ec3fc784`
and 15,306 bytes. The source hash, fixed transform, width allowlist, and
content-addressed path continue to provide the reproducible derivation rule;
the source original is not retained in this repository.

The typed media manifest for this edition is the committed file
`records/programs/6529NM-AP-01/media-manifest.json`. Its
`record_control.constructor.constructed_at` and `generated_at` fields currently
both read `2026-08-08T13:17:24Z`; the focused corpus test binds those fields to
this amendment and checks the OUT-011 source and derivative projections against
the hashes above.

## Rights and record boundary

This amendment records technical availability, not rights clearance. The
OUT-011 `rights_effective_status` remains the source outcome's controlling
value. The 640px presentation surrogate does not establish consent, venue
permission, unrestricted reuse, minting, purchase, title, custody, or
accession. The source URL in the typed media manifest remains a provenance
locator, not an automatic public high-resolution or source-download
affordance.

## Revision history

- **1 · 8 August 2026:** Recorded exact deletion of the 1280px and 2400px
  keys, completed cache invalidation, post-change 640/1280/2400 readback, prior
  byte fixity, and the visitor/institutional boundary.
