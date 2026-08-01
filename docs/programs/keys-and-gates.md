# Keys and Gates — Accession Program 01

Status: program selection complete; acquisition, minting, custody, rights verification, and accession remain unresolved.

Program ID: `6529NM-AP-01`

Program Wave: [`4ff022b3-aa17-4a0a-ba78-58f64ff1d427`](https://6529.io/waves/4ff022b3-aa17-4a0a-ba78-58f64ff1d427)

Description drop: `71c798bc-629d-46f2-8610-507a91be4f57` / serial `972000`

## Registrar status

The live API returned 16 selected submissions as `WINNER`. This repository records each as `selected_unminted`: a program outcome, not an accession or object record. A `WINNER` label is selection evidence only. It does not establish a mint, purchase, title passage, legal rights grant, custody receipt, token identity, technical verification, or accession.

The canonical index is [`records/programs/6529NM-AP-01/selected-works.json`](../../records/programs/6529NM-AP-01/selected-works.json). Each outcome has an individual registrar-grade record under [`records/programs/6529NM-AP-01/outcomes/`](../../records/programs/6529NM-AP-01/outcomes/) with the verbatim artist submission, source media URL and MIME type, selection evidence, CC0/consent representation, source fixity, and unresolved acquisition fields.

## Fixed program rules

The public program note defines a 60-day open call for original 1/1 photographs about access, exclusion, permission, surveillance, custody, autonomy, and exit. An artist may submit up to three works. The submission package includes the photograph, title/year/location, a 75–150 word caption, a technical note, a CC0 declaration, and consent confirmation where people are depicted. Identifiable minors and submissions exposing sensitive personal data or vulnerable situations are excluded.

The program is CC0-only. Written consent is required for depicted people, and consent documentation must be available on request. The budget is based on Meme Card mints; the program note states a purchase price of `0.5 ETH` per acquired work and quantity determined by the number of Meme Cards minted. The planned custody reference is `networkmuseum.6529.eth`. If a selected work is unavailable or fails the terms at acquisition, the allocation rolls to the next eligible work by rank.

The live Wave configuration observed on 2026-08-01 used `TDH` with `WAVE` scope. The voting period ended at `2026-07-09T12:00:00Z`. The formal note and Wave do not authorize a conclusion that the selected works have been acquired.

## Mint topology decision state

The mint topology is deliberately unresolved between:

- a dedicated 6529Stream instance; and
- a subcollection on main 6529Stream.

Until that decision and the implementation are evidenced, every outcome leaves contract address, deployment transaction, chain/network, token standard, token ID, CAIP-19 citation, mint transaction, payment transaction, custody wallet, transfer transaction, title binding, accession number, and accession statement ID as `null` or explicitly unverified. The program’s custody reference is a planned/reference field, not proof of receipt.

## Rights and consent handling

The individual records preserve each artist’s CC0 declaration verbatim and distinguish it from an effective rights grant. The records also preserve the artist’s representation about consent without treating the representation as independently verified. Where a submission says written consent or model releases exist, the public record records that claim and leaves the restricted instrument unsupplied; where a submission does not state consent, the record says so and requires follow-up if people are depicted.

No artist statement that mentions permanent accession changes the Museum’s accession status. Accession requires a separate acceptance record, title binding, chain and custody evidence, rights review, technical and preservation records, and second-person review.

## Source fixity

The program and institutional notes were fetched on 2026-08-01 and hashed over the UTF-8 bytes of their HTTP response bodies:

| Source | SHA-256 |
|---|---|
| [`keysandgates_thememes.ar.io`](https://keysandgates_thememes.ar.io/) | `sha256:0dbb79439224de8c86359a164f4777c81a70c3bc2eb852127a2ec54ae467a441` |
| [`6529networkmuseum_thememes.ar.io`](https://6529networkmuseum_thememes.ar.io/) | `sha256:75889ed25b623fde356129e39ba5330d4c0c2b38de0f3a7d94355282ff28b8d4` |

The full evidence log, API observation timestamps, vote table, operational chat context, and unresolved questions are in [`notes/research/keys-and-gates-evidence.md`](../../notes/research/keys-and-gates-evidence.md).
