# Stream museum coverage and gaps

Status: WIP analysis
Date: 2026-08-01 UTC
Pinned Stream source: `6529-Collections/6529Stream` `origin/main` commit `5021c8060950c3fef995271e674ed4b2007fee6d`

## Conclusion

6529Stream is an unusually strong object-level provenance, preservation, and museum-interoperability design. It should be the shared substrate for object identity, title binding, rights, work description, technical constitution, preservation, condition, rendering, and dossier export. It is not a complete institutional collections-management system for the 6529 Network Museum.

The Museum should add a governance/accession application profile above Stream rather than fork Stream's shared semantics.

## Planned Stream coverage

- Generic append-only `HashRef` and `CollectionRecord` envelope.
- Algorithm-tagged hashes and explicit canonicalization/schema IDs.
- Schema registry, payload pointers, latest-record reads, record-chain heads, and supersession.
- `ACCESSION`, `DEACCESSION`, and legal-instrument-to-transfer `TITLE_BINDING`.
- `WORK_DESCRIPTION`, CDWA-Lite/LIDO fields, authority-file identifiers, and canonical citations.
- Explicit per-use-class rights under `STREAM_RIGHTS_V1`.
- PREMIS Objects, Events, Agents, and Rights with LoC vocabulary mapping.
- Fixity, replication, migration, preservation masters, archive receipts, and storage coverage.
- Artist intent, interviews, execution environments, reference renders, and significant properties.
- Condition, exhibition, loan, valuation, recovery-response, steward, and independent-attestor records.
- IIIF Presentation 3, C2PA references, BagIt packaging, and OCFL mapping.
- An acquisition packet and independently regenerable object dossier.
- EIP-712/1271 institutional signatures, signer-scoped nonces, and append-only authority attribution.

## Where Stream exceeds the supplied accession draft

- Entropy and generative-seed provenance.
- Distinction between byte integrity, rendering success, and behavioral equivalence.
- Post-finality recovery lineage and explicit artwork-byte-change status.
- Complete ownership history linked to accession/deaccession title bindings.
- Independent institutional preservation attestations without operator permission.
- State-readable reconstruction that does not depend only on old event logs.
- Storage-family/economic coverage, preservation drills, and recovery from family extinction.
- BagIt/OCFL repository ingest and specified registrar/time-based-media practitioner review.
- Museum-grade conservation floors before sale for designated collections.

## Museum-specific gaps

1. Founding policy, collecting scope, donation acceptance, approved-collection votes, and program governance.
2. A richer institutional accession statement than Stream's minimal accession schema.
3. Multi-object accession lots and subordinate object numbering.
4. Separate workflow states for authorization, acquisition, receipt, accession, cataloguing, technical verification, preservation, and display readiness.
5. Claim-level A-E evidence classes.
6. Public/restricted registrar boundaries for donors, instruments, appraisals, security, and internal records.
7. Donation diligence: disputes, theft, sanctions, liens, donor warranties, conditions, curatorial independence, and tax/valuation boundaries.
8. Collection-level curatorial statements independent of legal accession records.
9. Generalized identity for third-party ERC-721/1155 contracts, non-EVM chains, and non-token or hybrid objects.
10. Explicit Spectrum 5.1 and ICOM Object ID crosswalks.

## Implementation caveat

At the pinned Stream commit, `IStreamPreservationRecords` and `StreamPreservationRecords` implement the generic collection-level envelope. The broad owner-record, accession packet, object dossier, PREMIS/LIDO round-trip, BagIt, and institutional-ingest system is still primarily a specification. Standalone canonical JSON Schema documents for the named museum profiles are not yet present in the repository.

The design should therefore be described as strong and directionally compatible, not as a finished or deployed museum system.

## Recommended split

- **Museum layer:** governance, policy, approvals, programs, donation workflow, institutional accession, privacy, sign-off, and evidence classes.
- **Shared Stream layer:** object identity, title binding, work description, rights, preservation, condition, rendering, provenance, and dossier packaging.
- **Export layer:** PREMIS, LIDO, IIIF, BagIt/OCFL, public catalogue, and human-readable dossier.
- **Commitment layer:** schema IDs, canonical payload hashes, authority, effective time, supersession, and record-chain heads.
