# Program media delivery

Status: active technical profile for public program presentation; not an
accession, rights, preservation, or mint record.

## Purpose

The Museum must let visitors encounter selected work without requiring a
browser to download a camera-original file for every card. It must retain a
clear provenance locator for the submitted high-resolution source without
turning that locator into a visitor download link or describing the source, or
any presentation copy, as an accessioned preservation master.

The first implementation applies to the sixteen selected works in Keys and
Gates (`6529NM-AP-01`). On 2026-08-04 UTC, the sixteen public submission files
totaled 233,601,493 bytes. Individual files ranged from 4.1 MB to 46.7 MB and
reached 10,080 by 5,670 pixels. The active release derives a 15,408,782-byte
closed set of responsive presentation copies from those sources under the
11 August 2026 image presentation authorization. It retains each submitted
source locator as provenance evidence without offering the source or a
high-resolution download to visitors.

## Three distinct media roles

1. **Submitted high-resolution source** — the exact submission URL used as a
   provenance locator, together with the SHA-256, byte size, MIME type, and
   oriented pixel dimensions observed during derivation. The `source.url` field
   is not a visitor-facing download affordance, and these bytes are not
   retained in this repository.
2. **Web presentation surrogate** — a deterministic, uncropped derivative for
   the public program interface. It is a technical delivery copy, not a new
   manifestation, a preservation master, or the tokenized artwork.
3. **Future preservation object** — any later Museum-retained master admitted
   through rights, fixity, preservation-event, and accession controls. No such
   object is created or implied by this profile.

The roles must not collapse into one `image_url` field. The public interface
uses only an approved presentation surrogate by default; the source locator
remains provenance data unless a later, explicit display/open-source authority
creates a separate approved affordance.

## Deterministic transform

Profile: `6529NM_WEB_PRESENTATION_WEBP_V2_Q82_M6_FIXED_ICC`.

- implementation: Pillow 12.3.0;
- output: lossy WebP, quality 82, encoder method 6;
- widths: 640, 1280, and 2400 pixels where the per-work public-size control permits;
- resize: Lanczos, proportional, no crop, no upscale;
- orientation: apply the source EXIF orientation before measuring or resizing;
- colour: convert embedded profiles to sRGB; treat untagged files as sRGB;
- metadata: remove source EXIF/XMP and retain only the output sRGB ICC profile;
- colour-profile determinism: embed the repository-pinned 588-byte sRGB ICC
  profile with SHA-256
  `4ed6f6f05df0d17516662c5fe06ac90e14e0c1936abd15a491b57998c56aef86`;
  do not create a fresh LittleCMS profile at generation time because its
  header contains a wall-clock creation timestamp;
- naming: include the complete source SHA-256 and transform profile in every
  repository and CDN path.

`scripts/generate_program_media.py` generates approved derivatives from a
local source directory and fails rather than replacing different bytes at an
existing content-addressed path. Its active-state check requires the exact
width allowlist, the display-authority record, the complete derivative entries,
and the corresponding local WebP files. The checker verifies byte fixity,
WebP structure, pixel geometry, ICC
presence, source/outcome agreement, rights-status agreement, accessibility
text, selected-work membership, and the exact authority-bound width inventory
without a network request.

## Delivery contract

Authority-approved presentation files use immutable CloudFront keys:

```text
museum/programs/{program_id}/{record_id}/{source_sha256}/{transform_profile}/{width}.webp
```

Each object is served as `image/webp` with:

```text
Cache-Control: public, max-age=31536000, immutable
Content-Disposition: inline
```

Publishing is additive and active for the authorized Keys and Gates
presentation set. A
publisher checks the target namespace before upload,
stores the declared SHA-256 as object metadata, requests an S3 SHA-256 checksum,
and must not overwrite an existing key whose bytes or metadata differ. The
frontend consumes only `presentation.derivatives[].url` values declared in the
governed media manifest; `source.url` is provenance-only and must not be
projected as a source or high-resolution link. The frontend does not expose an
open image-resizing proxy or accept visitor-supplied media URLs.

The repository release manifest covers `media/`. WebP files use raw-byte hashes;
Museum-authored text continues to use LF-normalized hashes. This byte-mode
distinction is explicit in each release-manifest entry.

## Public presentation

The current Keys and Gates publication presents all sixteen selected images.
The program grid uses `srcset` and `sizes` so the browser selects the smallest
declared derivative appropriate to the rendered image. Work pages use the same
responsive set without cropping and reserve the declared aspect ratio to
prevent layout shift. OUT-004 and OUT-011 are limited to their 640 pixel
surrogates. A submitted source URL or historical derivative does not authorize
visitor display outside the active manifest and display-authority record.

Every item has a concise visual description in
`media/programs/6529NM-AP-01/accessibility.json`. All sixteen descriptions were
independently checked against the 640-pixel presentation copies and approved
after four objective-language or visible-text corrections. The review,
per-work size restrictions, and current status are recorded in the
[append-only accessibility review](../records/programs/6529NM-AP-01/public/accessibility-review-2026-08-11.md);
the descriptions do not replace the artist statement or add a curatorial
interpretation.

Historically, OUT-004's 640px URL returned HTTP 200 with 45,202 bytes after the
2026-08-08 invalidation, while the exact 1280px and 2400px URLs returned HTTP
404. The readback and prior-byte lineage are recorded in [amendment 006](../records/programs/6529NM-AP-01/public/accessibility-amendment-2026-08-08-006.md).

Historically, OUT-011's 640px URL returned HTTP 200 with 15,306 bytes after the
2026-08-08 invalidation, while the exact 1280px and 2400px URLs returned HTTP
404. The readback and prior-byte lineage are recorded in [amendment 004](../records/programs/6529NM-AP-01/public/accessibility-amendment-2026-08-08-004.md).
Those observations remain part of the append-only technical history and do
not operate as current delivery instructions. The public document does not
expose delivery-origin identifiers.

## Rights and record boundary

The outcome record's `rights_effective_status` remains controlling. Derivation
and delivery do not activate a conditional CC0 declaration or grant downstream
reuse rights. The media manifest remains deliberately `constructed`; rights,
source, acquisition, accessibility, and presentation remain distinct records.

The current live evidence still supports `selected_unminted`: the sixteen works
won the Keys and Gates vote, but the Museum has no primary mint, purchase,
title, custody, or accession evidence for them. A 2026-07-26 direct program
update identified Stream contract work as the main blocker. Later forward-looking
chat did not supply mint evidence. The public interface may celebrate the vote
and explain that program minting is waiting for 6529Stream contract
finalization, but it must keep the later acquisition and accession gates
explicit.

## Updating the profile

Any source-byte change creates a new source-digest path. Any transform change
creates a new named transform profile. Neither may mutate an immutable key in
place. A change must regenerate the governed media manifest and release
manifest, pass the complete repository validation suite, receive independent
review, and then update the frontend projection.

## Open preservation work

- preserve the append-only accessibility amendments and retain the source,
  derivative, and rights boundaries as separate controls;
- determine whether and under what authority submitted source bytes may enter a
  Museum preservation package;
- add IIIF Presentation 3 resources only after the applicable rights and
  preservation roles are recorded;
- migrate the delivery origin to a private, versioned store with origin access
  control when the infrastructure change can be reviewed and rehearsed without
  changing public media identity.
