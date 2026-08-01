# Provenance and chain-history schedule

Status: draft working template. Keep the four lanes below distinct and attribute every claim.

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

For every acquired token, bind the legal instrument to the specific transfer it covers:

- Binding ID: `[...]`
- Instrument URI/hash: `[...]`
- Non-sensitive instrument custodian: `[...]`
- Transaction hash: `[...]`
- Block number/time: `[...]`
- `from`: `[...]`
- `to`: `[...]`
- Token/asset subject: `[...]`
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
