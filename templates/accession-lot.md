# Accession lot record

Status: draft working template. This is the short institutional act plus an object schedule. It is not complete until the completion gate is met for every object claimed as accessioned.

## Record envelope

- Record type: `ACCESSION_LOT`
- Lot ID: `6529NM.<year>.<sequence>`
- Schema/profile version: `[...]`
- Record status: `[draft | proposed | approved | accessioned | amended | superseded]`
- Created at / effective at: `[...]`
- Supersedes / amendment: `[none | record ID]`
- Public record URI: `[...]`
- Restricted annex reference: `[...]`

## Institutional act

- Acquiring institution: `6529 Network Museum`
- Governing entity / custody reference: `[...]`
- Accession date: `[...]`
- Acceptance authority and decision evidence: `[...]`
- Acquisition method: `[donation | purchase | bequest | exchange | transfer | program acquisition | other]`
- Pathway: `[preapproved collection | ordinary donation review | network-funded program | Meme Card benefit-work program | individual/group-funded program | secondary acquisition | other]`
- Accession rationale (concise): `[...]`
- Explicit non-claims: `[...]`
- Donor credit line (public-safe): `[...]`
- Consideration or budget note (do not give tax, legal, accounting, or valuation advice): `[...]`

## Object schedule

| Object ID | Object name/title | Native subject citation | Object record | Object state | Public release |
|---|---|---|---|---|---|
| `6529NM.<year>.<sequence>.<item>` | `[...]` | `[...]` | `[...]` | `[...]` | `[publish/hold/restricted]` |

Every row must resolve to one object record. If an object has no native token yet, use the state gate template and write `not_yet_assigned`; do not invent a token ID or CAIP-19 citation.

## Dates and custody are separate

- Offer received: `[...]`
- Authorization date: `[...]`
- Acquisition/title date: `[...]`
- On-chain receipt date and finality observation: `[...]`
- Formal accession date: `[...]`
- Cataloguing date: `[...]`
- Technical verification date: `[...]`
- Preservation completion date: `[...]`
- Display-readiness date: `[...]`
- Museum custody address/reference: `[...]`
- Custody verification evidence and observer: `[...]`

## Authority and due diligence

| Check | Result | Evidence refs | Reviewer / date | Restricted detail reference |
|---|---|---|---|---|
| Mission, collection, and pathway fit | `[pass/fail/open]` | `[...]` | `[...]` | `[...]` |
| Authenticity and native identity | `[pass/fail/open]` | `[...]` | `[...]` | `[...]` |
| Donor/seller authority and title | `[pass/fail/open]` | `[...]` | `[...]` | `[...]` |
| Provenance, theft, dispute, sanctions, liens, encumbrances | `[pass/fail/open]` | `[...]` | `[...]` | `[...]` |
| Rights, consent, restrictions, credit | `[pass/fail/open]` | `[...]` | `[...]` | `[...]` |
| Technical receivability and sustainability | `[pass/fail/open]` | `[...]` | `[...]` | `[...]` |
| Costs, obligations, and curatorial independence | `[pass/fail/open]` | `[...]` | `[...]` | `[...]` |

## Title binding and transfer summary

The detailed record lives in [`rights-donor-transfer.md`](rights-donor-transfer.md). Summarize one object-specific binding per transferred token or other acquired object.

| Object ID | Instrument hash/URI | Non-sensitive custodian | Transfer transaction or receipt | From | To | Block/time | Binding result |
|---|---|---|---|---|---|---|---|
| `[...]` | `[...]` | `[...]` | `[...]` | `[...]` | `[...]` | `[...]` | `[verified/open/not_applicable]` |

## Public and restricted record split

- Public inventory: `[...]`
- Public checklist/catalogue: `[...]`
- Public rights/credit statement: `[...]`
- Restricted annex reference: `[...]`
- Restricted retention/access rule: `[...]`
- Public redactions and reason: `[...]`

## Preservation and publication summary

- Preservation dossier IDs: `[...]`
- BagIt package ID and manifest: `[...]`
- OCFL object/version: `[...]`
- IIIF manifest(s): `[...]`
- C2PA manifest reference/validation status: `[not_applicable | absent | present/unvalidated | present/validated]`
- Fixity verification date/result: `[...]`
- Render/behavior test date/result: `[...]`
- Public release decision: `[ready | pending rights | pending technical verification | restricted | not released]`

## Accession rationale and non-claims

Why this lot belongs in the collection: `[...]`

What this record does not claim (for example: selection is not accession; custody is not title; a documentation surrogate is not the token; a third-party rarity metric is not an intrinsic trait): `[...]`

## Attestations

Attach [`attestations.md`](attestations.md) and list the signed/hash-committed block here.

- Constructor/preparer attestation: `[...]`
- Registrar/title attestation: `[...]`
- Technical/condition attestation: `[...]`
- Curatorial attestation: `[...]`
- Independent reviewer attestation: `[...]`
- Approver/effective authority: `[...]`
