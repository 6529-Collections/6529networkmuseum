# Accession state and gate worksheet

Status: documentation-only draft worksheet. It is not a governed record or executable state machine. Complete one worksheet per lot and retain object-level exceptions; current CI does not validate this Markdown form or its cross-record gates.

## Record identity

- Lot ID: `[6529NM.<year>.<sequence>]`
- Program or pathway: `[preapproved collection | ordinary donation review | network-funded program | Meme Card benefit-work program | individual/group-funded program | secondary acquisition | purchase | bequest | exchange | transfer | other]`
- Object or outcome IDs covered: `[...]`
- Record-control block: `[instantiate exactly from record-control.md]`
- Prepared by / date / version: `[...]`
- Governing source or authorization reference: `[...]`

Current status fields used by the canonical accession register:

- `donation_status`: `[offered | received | not_applicable]`
- `offer_status`: `[not_offered | offered | withdrawn | not_applicable]`
- `receipt_status`: `[not_received | received_offchain | received_onchain | not_applicable]`
- `acceptance_status`: `[not_started | pending | accepted | rejected | conditional | not_applicable]`
- `acquisition_status`: `[not_started | pending | completed | not_applicable]`
- `title_status`: `[not_started | pending | passed | disputed | not_applicable]`
- `custody_status`: `[not_received | received_offchain | received_onchain | verified | not_in_custody | not_applicable]`
- `accession_status`: `[not_started | documentation_in_progress | accessioned]`

## Separate institutional events and dates

Record each event independently. A received donation is not necessarily accepted; acceptance is not acquisition; acquisition is not passage of legal title; title passage is not custody receipt; custody receipt is not formal accession.

| Event | Status | Date/time | Authority or actor | Evidence/reference |
|---|---|---|---|---|
| Offer | `[not_offered/offered/withdrawn/not_applicable]` | `[...]` | `[...]` | `[...]` |
| Receipt | `[not_received/received_offchain/received_onchain/not_applicable]` | `[...]` | `[...]` | `[...]` |
| Institutional acceptance | `[not_started/pending/accepted/rejected/conditional/not_applicable]` | `[...]` | `[...]` | `[...]` |
| Acquisition | `[not_started/pending/completed/not_applicable]` | `[...]` | `[...]` | `[...]` |
| Legal title passage | `[not_started/pending/passed/disputed/not_applicable]` | `[...]` | `[...]` | `[...]` |
| Custody receipt | `[not_received/received_offchain/received_onchain/verified/not_in_custody/not_applicable]` | `[...]` | `[...]` | `[...]` |
| Formal accession | `[not_started/documentation_in_progress/accessioned]` | `[...]` | `[...]` | `[...]` |

## State register

Record the current state as an observed fact with evidence, not as an inferred workflow shortcut. A lot with mixed object states must show the object-level rows.

| State | Lot state | Object IDs | Observation date | Evidence refs | Gate result / open condition |
|---|---|---|---|---|---|
| `offered` | `[yes/no/not_applicable]` | `[...]` | `[...]` | `[...]` | `[offer and scope recorded]` |
| `authorized` | `[yes/no/not_applicable]` | `[...]` | `[...]` | `[...]` | `[policy/governance/program authority]` |
| `acquired` | `[yes/no/not_applicable]` | `[...]` | `[...]` | `[...]` | `[purchase/donation/transfer agreement]` |
| `received_onchain` | `[yes/no/not_applicable]` | `[...]` | `[...]` | `[...]` | `[specific transfer to Museum custody verified]` |
| `accessioned` | `[yes/no/not_applicable]` | `[...]` | `[...]` | `[...]` | `[formal institutional act and object schedule]` |
| `catalogued` | `[yes/no/not_applicable]` | `[...]` | `[...]` | `[...]` | `[object record and public/restricted split]` |
| `technically_verified` | `[yes/no/not_applicable]` | `[...]` | `[...]` | `[...]` | `[technical/condition report reviewed]` |
| `preservation_complete` | `[yes/no/not_applicable]` | `[...]` | `[...]` | `[...]` | `[fixity, package, storage, recovery evidence]` |
| `display_ready` | `[yes/no/not_applicable]` | `[...]` | `[...]` | `[...]` | `[manifest/derivative, rights, display test]` |

## Pre-mint program selection gate

Complete this section for a selected work without a verified token identity.

- Program ID: `[...]`
- Program authorization scope: `program-only; does not authorize any specific object`
- Selection evidence (Wave URL, serial, drop ID, live status, observation time): `[...]`
- Selection state: `selected_unminted`
- Object authorization: `not_granted_by_program_selection`
- Mint status: `[not_minted | mint_pending_verification | minted_pending_purchase | minted_pending_transfer | verified]`
- Purchase/acquisition status: `[not_started | agreed | paid_pending_delivery | acquired | not_applicable]`
- Artist consent/rights status: `[pending | received | verified | failed | not_applicable]`
- Native object identity: `[not_yet_assigned]`
- CAIP-19 citation: `[not_applicable until chain identity is verified]`
- Title binding: `[not_applicable until legal instrument and specific transfer exist]`
- Custody receipt: `[not_received | pending | verified]`
- Accession status: `not_accessioned`
- Off-chain instrument/receipt/title/custody event path (required for non-token or hybrid object): `[provenance-chain-history.md reference | not_applicable | pending]`
- Next authorized gate: `[...]`
- Non-claim: `Program authorization and selection do not establish object authorization, acquisition, minting, purchase, transfer, title, custody, accession, or preservation completion.`

Invariant `KNG-PROGRAM-OBJECT-BOUNDARY-01`: Keys and Gates program authorization and a Wave selection are program-level facts only. They never authorize a specific object's acquisition, mint, custody, title passage, or accession. Each selected object must pass its own availability, consent/rights, acquisition, identity, custody, and accession gates.

## Gate review

| Gate | Required evidence | Result | Reviewer / date | Open issue or amendment |
|---|---|---|---|---|
| Mission and pathway fit | Policy/program authority and rationale | `[pass/fail/open]` | `[...]` | `[...]` |
| Authenticity and identity | Contract/token/media/issuer evidence as applicable | `[pass/fail/open]` | `[...]` | `[...]` |
| Donor/seller authority and title | Executed instrument plus object-specific binding | `[pass/fail/open]` | `[...]` | `[...]` |
| Provenance and risk | Chain, legal, theft/dispute/sanctions/encumbrance review | `[pass/fail/open]` | `[...]` | `[...]` |
| Rights and restrictions | Rights matrix, consent, credit, curatorial independence | `[pass/fail/open]` | `[...]` | `[...]` |
| Technical receivability | Metadata, media, code, dependencies, mutability, contract | `[pass/fail/open]` | `[...]` | `[...]` |
| Custody | Museum custody address and transfer/finality verification | `[pass/fail/open]` | `[...]` | `[...]` |
| Condition and display | Technical/condition report and display test | `[pass/fail/open]` | `[...]` | `[...]` |
| Preservation | Dossier, fixity, copies, recovery plan/test | `[pass/fail/open]` | `[...]` | `[...]` |
| Independent review | Attestation from a second person | `[pass/fail/open]` | `[...]` | `[...]` |

## Amendments

| Amendment ID | Effective date | Supersedes | Change and reason | Evidence | Constructor / reviewer |
|---|---|---|---|---|---|
| `[6529NM.<year>.<sequence>-AMD01]` | `[...]` | `[...]` | `[...]` | `[...]` | `[...]` |
