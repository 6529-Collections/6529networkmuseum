# Rights handbook and registry

Status: live production publication
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

## Production closeout

The source publication merged through Museum PR
[#29](https://github.com/6529-Collections/6529networkmuseum/pull/29) as
`11c79489e0ae65d9a296577c44c881c3f79267d6`. The frontend publication merged
through PR
[#3627](https://github.com/6529-Collections/6529seize-frontend/pull/3627) as
`d448d4c282c034fa2a1d5d1d95ce90fc85561e54`.

Staging composition `21f58083e5c8974319701e25a0d62406c500bec3`
deployed in run
[`31043258638`](https://github.com/6529-Collections/6529seize-frontend/actions/runs/31043258638).
Its automatic selected-pack E2E run
[`31044289420`](https://github.com/6529-Collections/6529seize-frontend/actions/runs/31044289420)
passed. Production deployed exact frontend main in run
[`31045606678`](https://github.com/6529-Collections/6529seize-frontend/actions/runs/31045606678),
and automatic production E2E run
[`31046152675`](https://github.com/6529-Collections/6529seize-frontend/actions/runs/31046152675)
passed. The interval from frontend merge to completed production E2E was 50
minutes and 2 seconds; staging and production artifacts were built in parallel,
and the production deploy reused its completed exact-main artifact.

Independent live verification passed the six focused desktop/mobile journeys,
all twenty-two expression-detail routes, the artist and collector guides, the
Casey object-to-license path, exact legal-text disclosure, and source links.
The inspected 390-pixel pages had no horizontal overflow, and no page errors or
failed document responses were observed. Three consecutive production version
reads returned and announced exact frontend main with `stale: false`.

The Museum source advanced after PR #29 through the additive ontology and
preservation publication in PR #30. At production qualification, the live
adapter had refreshed without a frontend deployment and bound its source links
to canonical Museum main
`ad8ea4338659e0825dc5a79295e824eadec876e6`. That source release contains 345
governed files, SHA-256
`sha256:258a2aa6a970cc84d036de511902cbc1d5fbb5141067cc146fe83ac879d20544`,
and Keccak-256
`0x9ccca279ca25f1d0b65b2430168dd192a87dee77b682f63db25de44fc899ea26`.
PR #30 did not alter the rights corpus, and its post-merge Museum validation
run
[`31037002010`](https://github.com/6529-Collections/6529networkmuseum/actions/runs/31037002010)
passed.

## 2026-08-05 ordinary museum practice revision

The first public edition made the named license or rights statement carry too
much weight. Its six-use grid accurately described permission supplied by the
instrument, yet the public presentation made that narrow question look like
the complete answer. RightsStatements.org terms became rows of caution, and a
work with no public license appeared to require special permission before a
museum could show or care for it. That posture does not describe ordinary
museum work.

The revision keeps two separate readings. `use_matrix` continues to state what
the named instrument itself supplies. The new `museum_practice_matrix` records
how the Museum normally displays, documents, studies, publishes, preserves,
and, where appropriate, adapts a lawfully acquired work. Each of the twenty-two
entries now carries six action-specific notes. Five postures distinguish
ordinary practice, practice governed by recorded terms, purpose-limited use,
contextual museum judgment, and uses requiring separate permission or a legal
exception.

The reviewed practical baseline is:

- faithful display is ordinary collection use;
- a collection record may include a proportionate identification view and
  interpretation;
- criticism, cataloguing, scholarship, and education commonly support
  proportionate reproduction in print and online;
- controlled copying, dependency capture, migration, and emulation belong to
  collection care when the original and each intervention are retained;
- public remixes and new artistic adaptations are distinct from faithful
  technical conservation;
- merchandise, advertising, image licensing, endorsement, and
  substitute-quality commercial reproductions receive their own rights review.

For network-native work, the acquisition context includes the canonical media,
generator, contract, artist instructions, mint terms, and established mode of
viewing. Public on-chain availability proves technical publication and forms
part of the display record. Copyright ownership remains a separate fact.

Primary research for this revision includes the College Art Association Code
of Best Practices in Fair Use for the Visual Arts, United States Copyright Act
sections 107, 109(c), and 202, United Kingdom Intellectual Property Office
guidance on public exhibition, the United States Copyright Office and USPTO
NFT study, Creative Commons legal codes and NonCommercial guidance, and the
RightsStatements.org documentation and layer guidance. The registry retains
those sources as part of the governed publication.

The website design follows the same conceptual correction. The former colored
status chips and two-column dashboard are replaced by an unboxed editorial
register with six ruled rows. Each row presents the museum posture and its
object-specific practical explanation in ordinary typography. Version and
SPDX data become a quiet metadata line. The visitor note becomes part of the
page's editorial flow.

Construction is complete on source branch
`codex/museum-rights-practice-revision`. The full local source suite passed
151 tests with one intentional platform skip, together with bootstrap, fetch
guard, legal-text fixity, program media, institutional-source inventory, full
Museum and Casey validation, NextGen compatibility, Casey mutation controls,
snapshot-package verification, diligence-manifest verification, and the
deterministic release-manifest check. Frontend branch
`codex/museum-rights-practice-redesign` passed 158 Museum regression tests,
changed-file lint and typecheck, and React Doctor 100/100 before its exact
source build. Production release identifiers will be appended after source
merge, frontend merge, staging qualification, and production qualification.
