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
reached 10,080 by 5,670 pixels. The existing grid loaded those source files
directly. The delivery profile replaces that default path with a 15,408,782-byte
closed set of responsive presentation derivatives while retaining each submitted
source locator for provenance and fixity. It does not offer a source or
high-resolution download link in the visitor interface.

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

`scripts/generate_program_media.py` generates the derivatives from a local
source directory and fails rather than replacing different bytes at an
existing content-addressed path. `--check` verifies the closed 44-file
inventory for this edition, including the OUT-004 and OUT-011 640-only
restrictions, byte
fixity, WebP structure, pixel geometry, ICC presence, source/outcome agreement,
rights-status agreement, accessibility text, and selected-work membership
without a network request.

## Delivery contract

The published files use new, immutable CloudFront keys:

```text
museum/programs/{program_id}/{record_id}/{source_sha256}/{transform_profile}/{width}.webp
```

Each object is served as `image/webp` with:

```text
Cache-Control: public, max-age=31536000, immutable
Content-Disposition: inline
```

Publishing is additive. A publisher checks the target namespace before upload,
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

The program grid uses `srcset` and `sizes` so the browser selects the smallest
declared derivative appropriate to the rendered card. Object pages use the same
responsive set without cropping, reserve the declared aspect ratio to prevent
layout shift, and prioritize only the primary above-the-fold image. The
submitted source is not exposed through the public presentation; the governed
derivatives are the only public media links. A per-work allowlist is authoritative
for the widths that may be projected, so a source URL or a historical derivative
does not authorize a larger public rendition.

Every item has a concise visual description in
`media/programs/6529NM-AP-01/accessibility.json`. These descriptions are
constructed and pending independent visual review. The current corrections,
per-work size restriction, and status transition are recorded in the append-only
public accessibility amendments; the descriptions do not replace the artist
statement or add a curatorial interpretation.

For OUT-004, the 640px URL returned HTTP 200 with 45,202 bytes after the
2026-08-08 invalidation, while the exact 1280px and 2400px URLs returned HTTP
404. The readback and prior-byte lineage are recorded in [amendment 006](../records/programs/6529NM-AP-01/public/accessibility-amendment-2026-08-08-006.md).

For OUT-011, the 640px URL returned HTTP 200 with 15,306 bytes after the
2026-08-08 invalidation, while the exact 1280px and 2400px URLs returned HTTP
404. The readback and prior-byte lineage are recorded in [amendment 004](../records/programs/6529NM-AP-01/public/accessibility-amendment-2026-08-08-004.md).
The public document does not expose delivery-origin identifiers.

## Rights and record boundary

The outcome record's `rights_effective_status` remains controlling. Derivation
and delivery do not activate a conditional CC0 declaration or grant downstream
reuse rights. The media manifest remains deliberately `constructed`; its
independent visual review is pending, while rights, source, and acquisition
controls remain separate gates.

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
