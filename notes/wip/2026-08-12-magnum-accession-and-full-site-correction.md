# Magnum accession and full-site correction

## Authoritative institutional state

- *Conflict at Its Edges* is a completed gift from punk6529.
- The five Magnum Photos 75 tokenized works are formally accepted and
  accessioned as lot `6529NM.2026.002`.
- All five Works are members of the 6529 Network Museum permanent Collection.
- The original `PARTICIPATORY` proposal and signed `WINNER` observations remain
  append-only history. They are followed by formal acceptance, verified
  transfer and custody, and accession observations.
- Casey Reas accession `6529NM.2026.001` and Magnum accession
  `6529NM.2026.002` are the Museum's two completed accessions. Keys and Gates
  remains selected, unminted, in process, and outside the permanent Collection.

## Custody and display position

The custody package observes all five token manifestations at
`networkmuseum.6529.eth` at finalized Ethereum block `25,741,809`. Custody is
evidence for the transfer and object schedule; it is not treated as the source
of curatorial selection or accession authority.

The source photographs remain credited to their artists and Magnum Photos and
marked All Rights Reserved. The Museum interprets ownership as permitting the
ordinary credited institutional display, publication, and accessibility uses
by which another museum presents works in its collection. This position does
not claim copyright, commercial reproduction, derivative, licensing, print,
or AI-training rights.

## Canonical implementation state

The candidate package adds:

- accession statement, gift-acceptance authorization, title review, accession
  certificate, five object records, five rights statements, and five technical
  condition reports;
- exact finalized-block custody evidence and individual transfer receipts;
- an append-only completed-accession amendment to the earlier proposal status;
- one governed Accession entity, five accession relations, and five permanent
  Collection relations;
- updated public machine projections requiring the completed accession state;
- fail-closed tests that preserve the historical `WINNER` observation after a
  later accession observation is appended.

The pending candidate graph contains 128 public entities, 222 public
relations, and one Wave-status observation, 351 generated graph records in
total. Its permanent Collection contains exactly 12 Works: seven Casey Reas
Works and five Magnum Works. The 16 Keys and Gates Works remain outside it.

The corrected custody model records five distinct receipt transactions, each
with one token, one Transfer log, and `transfer_count: 1`; it no longer carries
the obsolete aggregate receipt. The rights model explicitly grants the
Museum's credited publication, exhibition, and accessibility uses while
denying general reproduction, print, derivative, AI-training, and
preservation-master use. Static-image migration/emulation is not applicable.
The current dossier and source register now label the 9 August donor-ownership
read as historical and identify the 12 August finalized Museum-custody record
as current.

`python scripts/bootstrap_validate.py`, `python scripts/validate.py`, and the
focused public-entity tests are green after the state correction. The full
repository suite, independent exact-head review, reviewed-B promotion,
catalogue activation, frontend qualification, staging, production, and the
every-route live audit remain required before release completion.

The complete local repository suite is green at 332 tests with one intentional
platform skip. Casey package verification, Magnum copy/citation, local-link,
media-policy, UTF-8, deterministic publication inventory/bundle, and manifest
checks are green. Exact review-candidate commitments are recorded after the
candidate is frozen so this governed ledger does not introduce a
self-referential manifest commitment.

## Frontend correction contract

Every public route must use the same taxonomy and state:

- **Collection**: accessioned Works only, currently Casey Reas and Magnum;
- **Acquisitions**: coherent curated units, currently two completed gifts and
  one selected/unminted acquisition in process;
- **Acquisition programs**: pathways that produce acquisitions, never a count
  or synonym for the acquisitions themselves;
- **Projects or series**: broader bodies of work that contextualize individual
  Works without implying Museum ownership of the whole project;
- **Artists and organizations**: people and institutions connected to Works,
  acquisitions, projects, or research, with explicit Collection counts;
- **Research**: interpretive scholarship presented as art scholarship, with
  imagery and useful thematic hierarchy rather than a record registry;
- **Exhibitions**: reserved for future time-bound presentations and not yet
  instantiated.

Collection, acquisitions, acquisition programs, artist/project directories,
Work pages, Research, redirects, count labels, media behavior, and rights copy
must agree with this model. Unresolved publication joins must fail visibly and
locally; they must not silently remove a completed acquisition from a listing.

## Release sequence

1. Freeze and commit review-pending candidate A.
2. Bind independent review to candidate A and its exact release commitments.
3. Create reviewed B as the review-only direct child of A.
4. Activate catalogue C only after B verifies.
5. Merge canonical PR after bots, threads, and required CI are green.
6. Rebase and qualify the frontend against the exact canonical Museum commit.
7. Merge the frontend PR after product, bot, and CI review.
8. Deploy and test staging, then production.
9. Audit every Museum route family for HTTP state, factual state, copy,
   responsive layout, imagery, console errors, and canonical navigation.
