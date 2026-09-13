# Display and preservation

**Scope:** Six finished photographic JPEG manifestations and their token,
metadata, provenance, title and catalogue documentation.  
**Status:** Source retention, two regional replicas and offline restoration
verified; final catalogue edition and binding Museum review remain pending.

The source JPEGs remain unchanged. Each file has a recorded SHA-256 digest,
byte count, decoded dimensions, orientation and embedded colour profile. The
six metadata responses are retained separately, including the issuer's
captions and date codes. The package also retains the evidence for tokenURI,
finalized custody and transfer provenance.

The Museum's display position covers ordinary credited exhibition, catalogue,
educational presentation and faithful copies for care. Source-image retention
does not depend on another donor rights questionnaire. The artist's copyright
and the gift credit remain separately identified in the rights record.

## Presentation instructions

- Show the complete frame at its original aspect ratio. Five photographs are
  horizontal; token 2216 is vertical. Use contain/fit presentation and permit
  enlargement. A square card must not replace the complete work view.
- Convert the embedded Adobe RGB (1998) profile through the Museum's fixed
  sRGB profile using the established perceptual colour transform. Resize with
  Lanczos and encode WebP at quality 82, method 6. Record output hashes and
  dimensions. Do not add contrast, sharpening, colourization or invented detail.
- Strip EXIF and XMP from public copies; embed the fixed sRGB profile. This
  removes precise location fields from presentation copies while retaining
  original metadata in the private source package.
- Present artist, descriptive/source caption, photographic year, edition
  token number and “Gift of punk6529. Photograph © Sebastião Salgado.” Keep
  the Museum's descriptive titles distinguishable from issuer titles.
- Provide concise visual alternative text. Identify communities through the
  source captions; do not infer the names of photographed individuals.

## Recovery scope

Recovery means extracting and verifying the six source JPEGs and metadata
responses, then rebuilding the display copies without using the issuer's
gateway. It also requires the source manifest, technical profile, rights
determination and chain evidence. Camera originals and unheld physical prints
are outside this package's scope.

A working directory and a second directory on the same host do not satisfy
the independent-copy requirement. The archival record must identify two
recoverable storage objects, their version/fixity evidence and a restoration
test. Private locations and access details remain outside the public repository;
the public record identifies custodial aliases and the verified scope.

The package's ability to reproduce these six photographs is separate from
the long-term availability of Ethereum, the issuer's metadata services, or
the broader *Amazônia* edition. Preserve both the recorded URI and the exact
bytes so a changed endpoint can be investigated without losing the observed
manifestation.

## Verified source-package restoration

On 13 September 2026, two private, encrypted, versioned regional archive
objects were downloaded by their exact version identifiers. Each 43,150,603-byte
archive matched SHA-256
`cc8f174cab25232ea8469862183e7f47ab3dc3239e30be5ed9998fb32728fecc`.
All 341 internal files passed the manifest's length and checksum checks.

From each restored package, the six JPEGs decoded and all 18 display copies
were rebuilt without an issuer gateway. Every rebuilt copy matched the
previously prepared WebP bytes. The
[restoration record](../../../../evidence/salgado-amazonia-preservation/restoration-summary.json)
documents the method and results, using custodial aliases. Exact storage
locations and object-version receipts remain restricted.

The two regional copies share one AWS account and its administration. The
source-preservation scope is recoverable, while later catalogue amendments,
the binding review and the eventual publication edition require a subsequent
package edition. The archive does not purport to contain documents written
after its capture.
