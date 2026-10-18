# Proposed acquisitions

This directory holds source records for purchases proposed to the 6529 Network
Museum Wave. A proposed acquisition is not part of the collection. It receives
a candidate ID (`6529NM-PA-<year>-<NNN>`) and no accession number.

Gifts follow a different path. A proposed gift names an exact object offered by
a donor and lives under [`records/proposed-gifts/`](../proposed-gifts/README.md).
A proposed acquisition asks the Museum to buy, often from funds the proposal
itself describes, and the vote may leave the exact token, price, or treatment of
surplus funds to a later step.

Each candidate directory contains `proposal.json`, validated by
[`schemas/proposed-acquisition.schema.json`](../../schemas/proposed-acquisition.schema.json).
The record states:

- the proposer's role, without a name, and whether the Museum prepared the
  proposal;
- the acquisition method (`purchase`), the object scope, and whether the
  proposal names an exact token;
- the funding model, the fixed statement that contributors hold no ownership
  interest, and whether the proposal sets a price cap or says how excess
  contributions are handled;
- the Wave drop, serial, creation time, decision time, observed status, rating,
  and rater count, each with its observation time and evidence class;
- the SHA-256 of the proposal text and whether a transcription is retained.

A Wave `WINNER` status records that the Wave adopted the proposal. It does not
select a token, and it does not establish payment, title, custody, or
accession. Those facts belong to the purchase's
`ACQUISITION_AUTHORIZATION` record, its `ACCESSION` certificate, and the
object record, each with its own evidence. The working standard is in
[`docs/accession-standard.md`](../../docs/accession-standard.md#purchase-acquisition-authorization).

The validator requires each record to live at
`records/proposed-acquisitions/<proposal_id>/proposal.json`. The proposed-gift
tools (`scripts/proposed_gifts.py` and
`scripts/build_proposed_gift_dossiers.py`) read only `records/proposed-gifts/`
and do not process this directory. Wave resolution notes and status amendments
under a candidate's `public/` directory are historical evidence; like their
proposed-gift counterparts, they are excluded from the visitor publication
corpus.
