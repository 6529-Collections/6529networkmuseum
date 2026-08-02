# Casey REAS donation: custody, title, and compliance diligence

Record: `6529NM.2026.001.DILIGENCE-01`

Accession: `6529NM.2026.001`

Review outcome: completed; pass with documented limits

Collection status: accessioned; no status change

## Determination

The 6529 Network Museum confirms the Casey REAS accession. No fact identified in this review requires a title downgrade, custody hold, deaccession review, or new display restriction. The seven exact tokens remain registered to the Museum in the reviewed finalized-state observation; the Museum's public title instrument remains executed; and the official OFAC Sanctions List Service returned no exact digital-currency-address match for the eight addresses screened.

This is a post-accession diligence record. It supplements the original receipt, gift acceptance, title, rights, technical, curatorial, and accession records. It does not redate the gift, replay title passage, or imply that the accession had remained incomplete pending this review.

## Title and institutional authority

The governing title instrument is the public [Title, Rights, and Accession Review](title-rights-and-accession-review.md), identified as `6529NM.2026.001.TITLE-01` and fixed at SHA-256 `aab01e90b585b7722b2b0e2af6df0e04290406523369a540c94dece09ff700d5`.

The Museum's final determination is substantive and specific. Punk6529 made a full and intentional gift of the seven scheduled tokens and every donor-held interest transferable with them, without consideration or retained donor interest. The donor delivered those seven tokens in one successful Ethereum transaction. The Museum accepted the gift under its adopted Art Blocks preapproval and Donation Acceptance Policy, bound the transfer to each accessioned object, and completed accession. The declaration, completed delivery, formal acceptance, and public institutional title instrument are sufficient for the Museum's recorded gift mode.

No donor-signed deed or separate private title annex is represented as existing. The Museum did not require one for this acceptance mode. The `restricted_registrar_annex` in the accession lot is an unused optional private-record stub. Its `instrument_status: not_recorded` means that no separate restricted annex was recorded; it does not describe `TITLE-01`, contradict the executed public title bindings, or create an uncompleted title gate.

Token title and copyright remain separate. The gift transferred the tokens and the donor's transferable interests; it did not transfer Casey REAS's copyright. The Museum's reviewed exhibition, publication, documentation, preservation, adaptation, migration, accessibility, and research uses remain subject to each object's recorded CC BY-NC 4.0 conditions, legal exceptions or limitations, or later permission. Commercial copyright use is not approved.

Public chain evidence and the donor declaration cannot disprove every possible private claim, authority defect, incapacity, or off-chain dispute. The accession certificate expressly accepted that bounded residual risk. This review found no evidence that changes that determination.

## Finalized-state custody audit

The Museum ran the reproducible [custody audit](../../../../evidence/casey-reas-diligence/custody-audit-2026-08-02.json) through the repository's fail-closed HTTPS transport. It retained 19 exact JSON-RPC response files and their transport observations.

The observation was bracketed by Ethereum finalized block `25,666,454`, hash `0x03f4728f9ae5949d30d0b3217a4934f3a6bfa64145ac8b97a10ff809e0365cce`, timestamped `2026-08-02T09:58:47Z`. One provider returned that same finalized block number and hash before and after the contract-read window. During the window a second provider evaluated the ENS resolver, ENS address, seven ERC-721 `ownerOf(uint256)` calls, and seven token-specific `getApproved(uint256)` calls through its `finalized` tag.

The results are unambiguous:

- `networkmuseum.6529.eth` resolved to `0xbECfa2bA5a782D11E1a0e821E8F2e30b6684178c`;
- every `ownerOf` call returned that Museum address; and
- every token-specific `getApproved` call returned the zero address.

These facts prove the observed ERC-721 and ENS contract state in the bracketed finalized window. They do not prove future custody, key security, the absence of approval-for-all operators, or the absence of private legal claims. A zero token-specific approval is a useful control result, not a universal non-encumbrance certificate. Standing custody monitoring therefore remains part of ordinary stewardship.

## Exact-address sanctions screening

The Museum screened the donor/source address, the Museum custody address, the four token contracts, the common transfer transaction target, and the artist address returned by the project contracts in the official U.S. Treasury OFAC Sanctions List Service. OFAC explains that digital-currency addresses may be searched in the ID-number field and that this field uses exact rather than fuzzy matching. See [OFAC FAQ 594](https://ofac.treasury.gov/faqs/594).

The Museum set the minimum name score to 100, left other filters blank or at All, and separately ran a known listed ETH address as a positive control. The service returned one `CHATEX` result on the SDN list under `CYBER2`; the eight accession-related address searches each returned no exact result. The Museum accepted the eight no-match observations only after the positive control passed. The [screening record](../../../../evidence/casey-reas-diligence/ofac-address-screening-2026-08-02.json) retains the query method, address roles, individual timestamps, positive control, observed service version, exact official-UI result, and acquisition limitation.

This finding is deliberately narrow: no exact OFAC digital-currency-address match was observed at the recorded time. It does not identify the civil person behind a pseudonymous address; conduct fuzzy name or KYC screening; apply OFAC's 50 Percent Rule; trace transaction exposure; search non-OFAC lists; or provide legal advice. The official JSON endpoint used transfer-coded framing, which the repository transport correctly rejects. The evidence therefore records structured observations from the official UI and does not claim that raw API response bytes were retained.

## Encumbrance and control conclusion

The reviewed public facts form a coherent chain: the successful receipt transferred the seven exact assets from the donor address to the Museum; the subsequent finalized-state audit returned the Museum from every `ownerOf` call; ENS resolved to the same address; and every token-specific approval was zero. No contrary transfer, token-specific approval, custody mismatch, or exact OFAC address match was observed.

The review cannot establish the absence of every approval-for-all operator, private lien, unrecorded contract, claim, incapacity, dispute, or key compromise. Those are the limits of the available public evidence, not unanswered accession questions. The Museum accepts those limits and finds no observed basis to disturb the accession.

## Standing controls

The registrar should reverify custody before any transfer, loan, exhibition that depends on live token control, or material catalogue refresh. Sanctions and counterparty diligence should be repeated for future acquisitions or transfers and whenever a new material fact appears. Any title claim, sanctions match, unexpected approval, custody mismatch, or key-security concern should trigger immediate registrar review.

The complete evidence package is fixed by [manifest.json](../../../../evidence/casey-reas-diligence/manifest.json), SHA-256 `8770ca3f6a7591c4548a72c18f410bb2e51fa1862d1921d6cd800ffa355b6edd`. The custody acquisition and manifest builder are public, deterministic, and non-transactional. They do not transfer assets, grant approvals, or sign with a wallet.
