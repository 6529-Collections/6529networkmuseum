# Provenance and chain-history schedule

Status: documentation-only draft template. It is not a governed record or current CI-validated schema. Keep the four principal lanes below distinct, use Lane 2A when applicable, and attribute every claim.

## Record envelope

- Schedule ID: `6529NM.<object-id>-PROV01`
- Record-control block: `[instantiate exactly from record-control.md]`
- Object ID / lot ID: `[...]`
- Prepared / reviewed by: `[...]`
- Observation cutoff (UTC): `[...]`
- Supersedes: `[none | record ID]`

## Lane 1 — Native chain and protocol history (evidence class A where directly verified)

| Sequence | Event type | Chain/network | Contract/asset | Token ID | From | To | Tx/block/time | Evidence URI/hash | Notes |
|---|---|---|---|---|---|---|---|---|---|
| `01` | `[mint | transfer | burn | metadata update | admin event | other]` | `[...]` | `[...]` | `[...]` | `[...]` | `[...]` | `[...]` | `[...]` | `[...]` |

Do not infer legal title or Museum accession from a transfer. Record observed custody and protocol events only.

## Lane 2A — Off-chain instrument, receipt, title, and custody path

Required for `non_token_digital_object` and `hybrid` objects when an off-chain instrument, delivery, title passage, or custody event exists or is expected. It is a distinct event path from the native chain lane; use `not_applicable` only when the object and its legal/acquisition pathway genuinely have no corresponding event.

| Sequence | Event type | Object/manifestation | Instrument or receipt ref/hash | From/actor | To/actor | Event date/time | Title/authority result | Custody result | Evidence/ref/reviewer |
|---|---|---|---|---|---|---|---|---|---|
| `01` | `[instrument_executed/object_received/title_passage/custody_receipt/custody_verification/other]` | `[...]` | `[...]` | `[...]` | `[...]` | `[...]` | `[verified/pending/disputed/not_applicable]` | `[verified/pending/not_in_custody/not_applicable]` | `[...]` |

Keep the executed instrument, object receipt, legal title passage, and custody receipt as separate rows when they occur at different times or have different evidence. For public records, use only a hash and non-sensitive custodian reference; retain private instruments in the restricted annex.

## Lane 2 — Legal title and acquisition history

| Sequence | Event/date | Acquirer/transferor | Method | Instrument ref/hash | Object(s) covered | Title status | Evidence class/source | Review note |
|---|---|---|---|---|---|---|---|---|
| `01` | `[...]` | `[...]` | `[donation | purchase | bequest | exchange | other]` | `[...]` | `[...]` | `[verified/pending/disputed/unknown]` | `[...]` | `[...]` |

## Lane 3 — Museum custody and control

| Sequence | Receipt/control event | Address or custody ref | Asset/object | Verification method | Finality/block/time | Observer | Result |
|---|---|---|---|---|---|---|---|
| `01` | `[...]` | `[...]` | `[...]` | `[...]` | `[...]` | `[...]` | `[verified/pending/not_in_custody]` |

## Lane 4 — Historical/curatorial provenance

Use the Stream-compatible entry shape. Historical or marketplace evidence is not chain state.

| Entry ID | Entry type | Occurred at | Title | Description | Evidence refs | Evidence class | Attribution/conflict |
|---|---|---|---|---|---|---|---|
| `[...]` | `[creation | curation | exhibition | publication | sale | custody | other]` | `[...]` | `[...]` | `[...]` | `[...]` | `[B-E]` | `[...]` |

## Title binding

For every acquired token, bind the legal instrument to the specific transfer it covers. For a non-token or hybrid object, bind the instrument to the distinct off-chain receipt/title/custody path above rather than inventing a token transaction:

- Binding ID: `[...]`
- Instrument URI/hash: `[...]`
- Non-sensitive instrument custodian: `[...]`
- Transaction hash or off-chain receipt reference: `[...]`
- Block number/time (token only; otherwise `not_applicable`): `[...]`
- `from` (on-chain only; otherwise `not_applicable`): `[...]`
- `to` (on-chain only; otherwise `not_applicable`): `[...]`
- Token/asset or off-chain object subject: `[...]`
- Object ID: `[...]`
- Binding result and reviewer: `[verified/open/disputed]`

## Diligence and unresolved claims

- Theft/loss/illicit-trade search: `[...]`
- Dispute/claim/lien/encumbrance search: `[...]`
- Sanctions/legal review: `[...]`
- Provenance gaps: `[...]`
- Conflicting claims preserved as: `[...]`
- Follow-up/amendment owner and date: `[...]`

## Attestation

- Constructor: `[...]`
- Registrar/title reviewer: `[...]`
- Independent reviewer: `[...]`
- Effective date/version/signature hash: `[...]`
