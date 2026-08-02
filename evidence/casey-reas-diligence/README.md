# Casey REAS accession diligence evidence

This package retains post-accession verification for `6529NM.2026.001`. It supplements the original receipt and preservation packages; it does not replace or redate the gift, title passage, or accession decision.

The custody audit records Ethereum mainnet custody at one exact finalized block. One provider returned the same finalized block number and hash before and after the observation window. A second provider evaluated the ENS resolver, ENS address, seven `ownerOf(uint256)` calls, and seven `getApproved(uint256)` calls with an EIP-1898 selector containing that exact block hash and `requireCanonical: true`. Exact JSON-RPC responses, request digests, and fail-closed HTTPS observations are retained and semantically rejoined by validation. This is direct contract-state evidence, not proof against later transfers, operator-for-all approvals, key compromise, private claims, or legal encumbrances.

The OFAC record documents a point-in-time exact digital-currency-address screen in the official Sanctions List Service. A known listed address returned a positive control before the Museum accepted the eight no-match observations. OFAC states that its ID-number field can search digital-currency addresses and that those address searches use exact rather than fuzzy matching. The official search API used transfer-coded framing, which the repository transport deliberately rejects; the retained record therefore identifies its structured official-UI observation boundary and does not claim raw API-byte preservation.

The title conclusion remains the reviewed Museum determination already bound as `6529NM.2026.001.TITLE-01`: the donor made a full gift, delivered the seven exact tokens, retained no donor interest, and the Museum formally accepted and accessioned them. The optional restricted-annex stub in the lot is not an uncompleted title gate. No donor-signed deed or private annex is represented as existing, and none was required for the Museum's recorded acceptance mode. Copyright remains separate from token title.

Reproduce custody with:

```text
python scripts/acquire_casey_custody_audit.py --output-dir <new-empty-directory>
```

Build or check this package's complete fixity inventory with:

```text
python scripts/build_casey_diligence_manifest.py
```

The scripts do not perform transfers, signatures, approvals, or other on-chain writes.
