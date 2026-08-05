# IIIF: a shared plan for presenting digital objects

Status: working Museum application profile; the cited standard remains authoritative

## The question

**What should a viewer show, in what order, at what scale, and with which
credit and rights statement?**

A work may have one still, hundreds of pages, a sequence of views, several
minutes of sound, a video, annotations, or a live component. A URL to an image
does not explain how that resource belongs to the object. IIIF supplies a
shared presentation model that viewers at many institutions can understand.

In IIIF, a Manifest describes how an object should be presented. It contains one
or more Canvases; images, video, audio, text, and other content are attached to
those Canvases through annotations. A Canvas is the space or duration of a view,
not the image file itself.

## In the Casey Reas accession

A Manifest for *CENTURY #31* can present an approved fixed still with the
Museum credit line and media licence; link to the object, technical, and rights
records; and point separately to the live Art Blocks generator. The still is
identified as a dated documentation surrogate. The live generator remains a
related realization with its own dependency and preservation status.

A still records one viewing of a generative work; it must not be presented as
the complete work.

## What IIIF contributes

Presentation API 3.0 defines:

- `Collection`: a group of Manifests or Collections;
- `Manifest`: the presentation description of one object;
- `Canvas`: a spatial or temporal frame;
- `Range`: navigation or hierarchy within a Manifest;
- `AnnotationPage`: a page of annotations;
- `Annotation`: a relationship between content and a target;
- content resources: images, video, audio, text, or other web resources.

Its descriptive properties include labels, summaries, required attribution,
rights, provider, metadata, thumbnails, homepages, related records, rendering
options, and links to richer metadata. The Image API can provide standardized
regions and sizes for fixed images; it is a separate API.

## Museum application profile

### One Manifest, declared subject

Every Manifest states which Museum object it presents and links to the
canonical public record. The Manifest ID, object ID, accession number, CAIP-19
asset ID, content-resource IDs, and file hashes remain distinct.

### Resource role

Every content resource carries a Museum role:

```text
authorized_manifestation
documentation_surrogate
preservation_master
access_derivative
live_upstream_service
technical_model
```

Only resources approved for public access appear in the public Manifest.

### Rights and credit

A required credit statement tells the viewer what to display. The `rights`
field records an applicable Creative Commons or RightsStatements.org URI where
one accurately describes the resource. Work rights, record rights, and media
rights are evaluated separately. `provider` identifies the supplying
institution.

### Time and change

A new fixed media derivative receives a new resource URI and fixity. A material
change to presentation creates a new Manifest version through the Museum record
lineage. A mutable upstream live URL is labelled as such and paired with dated
observations rather than treated as byte-stable.

## What this standard leaves to the Museum

IIIF structures access. It provides no signature, content fixity, accession
authority, rights clearance, authenticity judgment, or preservation guarantee.
Its `metadata` values are intended for display and should not replace LIDO or a
semantic catalogue export.

## For machines and implementers

### Authority and version

- Authority: IIIF Consortium.
- Current stable Presentation API: **3.0.0**, released 3 June 2020.
- Current stable Image API: **3.0.0**.
- Presentation 4.0 is not the stable pin for this profile.
- Specification licence: CC BY.

### Minimal populated shape

```json
{
  "@context": "http://iiif.io/api/presentation/3/context.json",
  "id": "https://6529.io/iiif/objects/6529NM.2026.001.01/manifest",
  "type": "Manifest",
  "label": { "en": ["Casey Reas, CENTURY #31"] },
  "requiredStatement": {
    "label": { "en": ["Credit"] },
    "value": { "en": ["..."] }
  },
  "rights": "http://creativecommons.org/licenses/by-nc/4.0/",
  "items": [
    {
      "id": "https://6529.io/iiif/objects/6529NM.2026.001.01/canvas/1",
      "type": "Canvas",
      "height": 1200,
      "width": 1200,
      "items": [
        {
          "id": "https://6529.io/iiif/objects/6529NM.2026.001.01/page/1",
          "type": "AnnotationPage",
          "items": [
            {
              "id": "https://6529.io/iiif/objects/6529NM.2026.001.01/annotation/1",
              "type": "Annotation",
              "motivation": "painting",
              "body": {
                "id": "https://media.example/6529NM.2026.001.01.jpg",
                "type": "Image",
                "format": "image/jpeg",
                "height": 1200,
                "width": 1200
              },
              "target": "https://6529.io/iiif/objects/6529NM.2026.001.01/canvas/1"
            }
          ]
        }
      ]
    }
  ]
}
```

Production records add `provider`, `homepage`, `seeAlso` for the LIDO or Museum
record, and `rendering` where appropriate. The placeholder image URI above is
replaced by an approved, retained resource. A published Manifest always contains
at least one Canvas; a presented resource follows the Canvas → AnnotationPage →
Annotation structure.

### Transport and validation

The Manifest is UTF-8 JSON-LD served from a stable HTTPS URI with the specified
context and appropriate `application/ld+json` profile. Referenced resources are
dereferenceable, CORS-enabled where required, and use stable or explicitly
versioned URIs.

Validation includes the official Presentation validator, Museum JSON Schema or
shape checks for resource roles and source linkage, rights consistency, content
fixity for retained files, URL safety, accessibility metadata, and a browser
render test. Validator success confirms structure, not truth.

## The Casey Reas accession

Museum state: `conceptual_mapping`. The website presents upstream stills and live generators,
and the records preserve source URLs, credit, rights, and observation data. The
Museum has not published a IIIF Presentation 3.0 Manifest for any of the seven
objects. Existing `manifest_uri` labels in object data refer to Museum display
documentation and must not be described as IIIF manifests.

## Official sources

- IIIF Consortium, [current API specifications](https://iiif.io/api/).
- IIIF Consortium, [Presentation API 3.0](https://iiif.io/api/presentation/3.0/).
- IIIF Consortium, [Presentation API Cookbook](https://iiif.io/api/cookbook/).
- IIIF Consortium, [Presentation validator](https://presentation-validator.iiif.io/).
