# Accession state and gate worksheet

Status: draft working template. Complete one worksheet per lot and retain object-level exceptions.

## Record identity

- Lot ID: `[6529NM.<year>.<sequence>]`
- Program or pathway: `[donation | preapproved donation | network-funded program | Meme Card benefit-work program | individual/group-funded program | purchase | other]`
- Object or outcome IDs covered: `[...]`
- Prepared by / date / version: `[...]`
- Governing source or authorization reference: `[...]`

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
- Selection evidence (Wave URL, serial, drop ID, live status, observation time): `[...]`
- Selection state: `selected_pending_mint`
- Mint status: `[not_minted | mint_pending_verification | minted_pending_purchase | minted_pending_transfer | verified]`
- Purchase/acquisition status: `[not_started | agreed | paid_pending_delivery | acquired | not_applicable]`
- Artist consent/rights status: `[pending | received | verified | failed | not_applicable]`
- Native object identity: `[not_yet_assigned]`
- CAIP-19 citation: `[not_applicable until chain identity is verified]`
- Title binding: `[not_applicable until legal instrument and specific transfer exist]`
- Custody receipt: `[not_received | pending | verified]`
- Accession status: `not_accessioned`
- Next authorized gate: `[...]`
- Non-claim: `The selection does not establish minting, purchase, transfer, title, custody, accession, or preservation completion.`

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
