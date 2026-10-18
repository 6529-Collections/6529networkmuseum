# MAX PAIN acquisition: residual funds received by the Museum

Status: open question; no acceptance recorded
Opened: 2026-10-18
Related accession: `6529NM.2026.005` (XCOPY, *MAX PAIN* #4188/7394)

## Status

The Museum has received the funds but has not accepted them, and has asked the organizer how they should be held.

This note records facts and options. It does not accept, restrict, designate, return, or spend the funds, and no Museum record treats them as part of accession `6529NM.2026.005`. Acquisition Authorization `6529NM.2026.005.AQA-01` and the accession statement both state that the transfer is outside the acquisition.

## The transfer

- Transaction `0x7d7b7733c696858dda93374395a978a4f7cb0cf4b631e2a81ab595f70d5debef`, block 25,975,418, 14 September 2026 at 11:32:23 UTC, receipt status `0x1`.
- From the organizer's acquisition wallet (nonce 2) to the Museum Safe, `networkmuseum.6529.eth` (`0xbECfa2bA5a782D11E1a0e821E8F2e30b6684178c`).
- Value 68,496,911,687,069,084 wei, that is 0.068496911687069084 ETH (`eip155:1/slip44:60`). The Safe emitted one `SafeReceived` event for that value.
- Evidence: `evidence/xcopy-max-pain-4188-custody/summary.json` (`residual_transfer`, raw receipt, transaction, and block responses) and `evidence/xcopy-max-pain-4188-funding/summary.json`.
- The organizer's message in the Museum Wave on 14 September 2026 says the funds were sent "for any future XCOPY purchases". On 2 September the organizer had offered contributors three options for the surplus (hold it for a future XCOPY purchase, send it to XCOPY as a royalty, or another use); one participant preferred paying XCOPY and one preferred holding it, and on 9 September the organizer said the surplus would go to the Museum wallet for future XCOPY purchases. These are the organizer's class B statements, observed by the Museum in the Wave chat; no capture is retained.

## Reconciliation of the acquisition wallet

The funding package reads the wallet's ETH balance and nonce at each checkpoint (archive reads at finalized block 26,218,159). The nonces show that no other outgoing transaction occurred, so each interval's inflow is its balance change plus its known outflows.

| Interval | Inflow (ETH) | Outflow (ETH) |
|---|---|---|
| Through block 25,889,851, before the purchase | 0.4646 | 0 |
| Purchase, block 25,889,852 | 0 | 0.4589999999 value plus 0.000038617152717696 gas |
| Purchase to Museum receipt | 0 | 0.00002791026021322 gas |
| Museum receipt to block 25,975,417 | 0.063 | 0 |
| Residual transfer, block 25,975,418 | 0 | 0.068496911687069084 value plus 0.000008204245573351 gas |
| After the residual to block 26,218,159 | 0 | 0 |

Total inflow 0.5276 ETH = purchase 0.4589999999 + residual 0.068496911687069084 + gas 0.000074731658504267 + remaining balance 0.000028356754426649. The identity holds exactly.

The call in the Museum Wave asked each of 25 voters for 0.021 ETH, 0.525 ETH in all. Inflows exceeded that by 0.0026 ETH, and 0.063 ETH arrived after the transfer to the Museum. The residual is therefore the surplus of the shares over the purchase price and gas plus the overpayments; it is not simply "the leftover of 25 equal shares". The package records aggregates only. No contributor or payer address is requested, derived, or retained, and the Museum publishes no per-person payment mapping.

## Policy analysis

The adopted Museum Gifts, Acquisition Programs, and Funding Assets Policy (`6529NM-POL-004`, decision `6529NM-GOV-1282091`) governs the funds.

- **Section 2 and section 10.** Transfer to a Museum wallet is not formal acceptance, and an unsolicited transfer is not an accepted gift or a funding commitment. The receipt alone changes nothing.
- **Section 5.** The MAX PAIN Wave decision authorized one purchase funded by equal shares of the final cost. It does not say how excess contributions are handled, so it does not "expressly permit" a continuing XCOPY fund.
- **Section 7.** Funds "restricted to an artist" require TDH approval before formal acceptance unless an authorized acquisition program expressly covers them. A binding "future XCOPY purchases" designation is such a restriction. A proposal would have to state the exact restriction, the amount, its duration, the consequence of non-use, any return terms, donor recognition, and whether acceptance would compromise curatorial independence.
- **Section 6.** ETH (`eip155:1/slip44:60`) is on settlement-asset schedule `6529NM-ASA-1`. An unrestricted gift of it may be accepted administratively after the section 6 checks: donor authority and control, legal and source-of-funds review, confirmation that no restriction or side agreement exists, recording of receipt and acceptance, and the Museum's unrestricted right to hold, spend, or convert. A donor's nonbinding hope is not a restriction, and before acceptance the Museum should state in writing that the gift is unrestricted and that no promised use follows from the donor's preference.
- **Section 12.** Before any formal acceptance the Museum records donor authority, asset identity, the gift's class (restricted or unrestricted), restrictions and the absence of side agreements, donor credit, and the governing authority. The surplus came from many contributors' payments; who holds donor authority over it (the organizer, the contributors, or both) is itself open.
- **Section 13.** No administrator, signer, or registrar may bypass these approvals.

## Owner options

1. **Restricted fund.** Put a restricted-funding proposal to the Museum Wave under section 7, stating the restriction to future XCOPY purchases, the amount, its duration, what happens if it is not used, return terms, and credit. Accept only after a `WINNER` decision.
2. **Unrestricted gift.** Obtain written confirmation from the organizer, and where needed from the contributors, that the XCOPY preference is a nonbinding hope; state in writing that the gift is unrestricted; then accept it administratively under section 6 and record the acceptance.
3. **Return.** Return the funds to the acquisition wallet or as the organizer directs, recording the return transaction.

Until the organizer answers and the owner chooses, the funds stay outside every accession and acquisition record. The open question is listed in the MAX PAIN release ledger.
