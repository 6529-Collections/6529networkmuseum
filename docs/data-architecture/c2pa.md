# C2PA: signed claims about media

Status: working Museum application profile; the cited standard remains authoritative

## The question

**Who made this statement about this file, and do the file's bytes still match
it?**

C2PA is the technical system behind the “Content Credentials” label used by
some image and video tools. It attaches a signed record of selected actions,
sources, and other assertions to a particular media file.

A valid credential can show that a certificate-holder signed a claim and that
the claim's content binding matches the asset. It does not, by itself,
establish that the signer is the relevant party or that every assertion is
credible.

## In the Casey Reas accession

If the Museum creates a video documenting *Phototaxis #308*, a C2PA Manifest
could identify the Museum's capture process, source ingredient, date, and
transcoding action and bind the claim to the exact video bytes. A later web
derivative could cite the preservation master as an ingredient.

The credential would concern those video files. It would not turn the video
into the accessioned artwork or prove that every future execution of the live
system behaves identically.

## What C2PA contributes

A C2PA Manifest contains assertions, a claim that refers to those assertions, a
claim signature, and one or more bindings to the asset. A Manifest Store can
contain a history of Manifests. Common assertions describe actions,
ingredients, metadata, thumbnails, asset types, external references,
time-stamps, and repository receipts.

C2PA distinguishes:

- assertions in `created_assertions`, created by the claim generator and
  attributed to the signer under the trust model, from `gathered_assertions`,
  supplied by other workflow components and not attributed to the signer;
- hard bindings based on cryptographic hashes from soft bindings such as
  fingerprints or watermarks;
- a structurally valid claim from a credential trusted under a particular
  certificate and trust-list policy.

## Museum application profile

### Eligible assets

C2PA is applied to fixed Museum-created or Museum-received media when a clear
provenance claim adds value: preservation masters, exhibition copies,
documentation stills and videos, and derived access media. A live generator,
token, accession record, or abstract work is not converted into a C2PA asset
merely because related media exists.

### Claim scope

Museum assertions say exactly what the Museum did: captured, transcoded,
resized, annotated, packaged, or published. They cite the Museum object and
source record. They do not claim artist authorship, copyright ownership, token
authenticity, or completeness unless separately established and deliberately
asserted by the authorized party.

### Validation evidence

The Museum preserves the asset hash, Manifest identifier, `instanceID`,
signature and certificate summary, validation result, validator and version,
validation time, time-stamp result, trust-list source and digest, assertion
inventory, and any redaction declaration.

### Derivatives

Every material derivative receives its own asset identity and active Manifest.
The parent is retained as an ingredient, and the transformation is described as
an action. Earlier Manifests are never replaced by a new claim.

## What this standard leaves to the Museum

A successful C2PA validation authenticates a signed claim and content binding
within the configured trust model. It does not establish the truth or
completeness of every assertion, the signer's authority over the artwork,
Museum accession, legal title, copyright, or long-term reproducibility. C2PA
allows credentials to be removed from media; absence of a credential is not
evidence of manipulation.

## For machines and implementers

### Authority and version

- Authority: Coalition for Content Provenance and Authenticity, a Joint
  Development Foundation project.
- Profiled specification: **C2PA 2.4**, published April 2026 and current on the
  specification site in August 2026.
- Specification licence: CC BY 4.0.
- Trust and conformance state must be observed separately from the technical
  specification version.

### Core structures

```text
C2PA Manifest Store
  C2PA Manifest
    assertions
    claim (for example c2pa.claim.v2)
    claim signature (COSE_Sign1)
    content binding
```

Identifiers include a C2PA Manifest label/URN, an asset `instanceID`, assertion
labels, and ingredient references. None replaces the Museum object ID or
CAIP-19 asset ID.

### Hard and soft binding

A hard binding hashes all or defined portions of the asset. A soft binding uses
a fingerprint or watermark to support discovery after transformation. Museum
preservation masters require hard binding. A soft binding is recorded with its
algorithm, threshold, resolver, and limitations.

### Validation states

The implementation records structural, signature, content-binding,
certificate, revocation, time-stamp, assertion, ingredient, and trust results
individually. The Museum retains each validation result separately; a passing
summary is not the validation record. Trust-list-dependent outcomes include the
exact trust configuration and observation time.

### Security and key boundary

Private signing keys, issuance controls, and non-public identity material never
enter this repository. Public records may include certificate chains, public
identifiers, signatures, validation reports, and hashes. Key compromise or
revocation creates a new incident and preservation event; it does not authorize
rewriting the historical asset.

## The Casey Reas accession

Museum state: `conceptual_mapping`. No retained Casey media currently carries a Museum- or
artist-issued C2PA Manifest in the canonical package. The Museum must not imply
Content Credentials from ordinary SHA-256 hashes or signed Git commits.

## Official sources

- C2PA, [Specifications 2.4](https://spec.c2pa.org/specifications/specifications/2.4/).
- C2PA, [Technical Specification 2.4](https://spec.c2pa.org/specifications/specifications/2.4/specs/C2PA_Specification.html).
- C2PA, [Security Considerations](https://spec.c2pa.org/specifications/specifications/2.4/security/Security_Considerations.html).
- C2PA, [Conformance Program](https://c2pa.org/conformance/).
