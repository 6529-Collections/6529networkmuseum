# Rights handbook and registry

Status: source corpus complete; review and release in progress
Started: 2026-08-05T17:01:32Z

## Purpose

The Museum needs one public place where a visitor can understand the rights
attached to a work without reading a legal file first. The same information
must remain precise enough for accession work, publication, preservation, and
future on-chain records.

The handbook will cover the common situations the collection is likely to
encounter: no stated public license; CC0 1.0; the six Creative Commons 4.0
licenses; the Public Domain Mark; the principal RightsStatements.org status
terms used by cultural institutions; and a clearly bounded custom-license
case. Exact official texts will be retained with source URLs and fixity. Each
entry will also explain, in ordinary language, what the Museum and a visitor
may usually do, which conditions apply, and which questions the rights label
does not answer.

## Record design

Copyright status, a public license or dedication, ownership of the token,
evidence for the determination, licensed components, and other rights such as
privacy, publicity, trademark, and moral rights remain separate facts. A token
transfer does not transfer copyright. Silence does not create a license.

The existing Stream-compatible `RIGHTS_STATEMENT` record remains unchanged.
A separate rights-expression registry will identify standard external terms,
their official URIs and retained texts, and their practical Museum reading.
An object map will connect an accessioned object to the applicable registry
entry without making the external vocabulary part of the Stream schema.

## Editorial rules

- Start with what a person may do.
- Name conditions directly: credit, noncommercial use, sharing on the same
  terms, or no sharing of adaptations.
- Say “the license does not grant this use” when that is the fact. Do not turn
  the absence of permission into a broader claim about all possible legal
  exceptions.
- Explain that “noncommercial” describes the use, not the tax status of the
  user.
- Explain that a no-derivatives license permits private modifications and
  necessary technical changes, while restricting public sharing of adapted
  material.
- Never describe ordinary museum practice as a license.
- Keep the official legal text unchanged and visibly distinct from the
  Museum's practical explanation.

## Initial object application

The seven Casey Reas objects in accession `6529NM.2026.001` will link to
CC BY-NC 4.0, matching their reviewed rights statements and retained Art
Blocks metadata. Keys and Gates remains selected but unminted. Its stated CC0
intention will be described at program level and will not be presented as an
effective object license before mint evidence exists.

## Release boundary

The repository change includes the source registry, retained official texts,
plain-language entries, object mappings, validation, tests, index updates, and
release-manifest regeneration. The frontend change will add a Rights section,
link object-level rights labels to the relevant entry, and retain official
source links. Staging and production qualification will follow both merges.

## Open questions

None block implementation. A future accession with a bespoke artist or
platform license will require its own exact text, source evidence, and
object-specific determination; it must not be forced into a nearby Creative
Commons category.

## Construction checkpoint

Completed at the source boundary on 2026-08-05. The release contains twenty-two
rights expressions, seven exact English Creative Commons legal-code snapshots,
seven Casey Reas object assignments, a conditional and explicitly ineffective
Keys and Gates CC0 program note, and public guides for artists and collectors.

Validation passed for the rights registry and mutations, retained legal-text
fixity, complete Museum JSON/schema validation, the reviewed Casey package,
program media, and the Casey diligence manifest. The full Python suite passed
138 tests with one intentional skip. The regenerated release manifest records
SHA-256 `sha256:b6b1d5ddf19c88335b752bc610a1d4020236a3eb4a86a13d52182a29aa22ffb1`
and Keccak-256
`0x11546194ab32ec2553562d48aa21788329da52afa86470812d4c327aa2d3d025`.
