# External registry review — contract migration draft

Status: WIP research note supporting `specs/onchain/contract-migration-v1.md`.
Date: 2026-08-01 UTC.

## Evidence basis

This review used:

* the Museum repository's `README.md`, `INDEX.md`, `docs/record-model.md`,
  `docs/accession-standard.md`, `docs/stream-interoperability.md`,
  `docs/onchain-design.md`, and `docs/external-works-registry.md`;
* the Museum skill's current-state, accessions-and-controls, decision-ledger,
  linked-materials, and Wave-history guidance;
* the pinned local 6529Stream source at commit
  `5021c8060950c3fef995271e674ed4b2007fee6d`, especially
  `IStreamPreservationRecords.sol`, `StreamPreservationRecords.sol`,
  `IStreamRecordFamilyRegistry.sol`, and the collection-metadata contract
  specification.

The review is design evidence, not a deployed-contract or live-custody claim.

## Findings

### 1. External works need a Museum registry boundary

At the pinned Stream commit, `StreamPreservationRecords` is outside-Core but
still requires a `collectionId` that exists in `StreamCore`. Its record hash
also commits to `streamCore`, the preservation module address, and
`collectionId`. That surface cannot directly represent a donated CryptoPunk,
Rare Pepe, external Art Blocks work, legacy EVM token, or non-EVM object
without creating a false Stream collection relationship.

Wrapping/reminting is rejected because it creates a second token identity and
confuses custody, provenance, title, rights, bridge behavior, and conservation
claims. The original asset must remain the object of record.

### 2. Bilateral compatibility is payload-level, not host-hash equality

The Museum can use the exact Stream `HashRef` and `CollectionRecord` shapes and
the shared `ACCESSION`, `WORK_DESCRIPTION`, `RIGHTS_STATEMENT`, PREMIS, and
LIDO identifiers. The Museum record hash and Stream record hash nevertheless
must differ when their domain/host/collection context differs. Compatibility
means byte-identical canonical payloads, equal content hash/schema/type/subject
identifiers, and successful export/import round trips.

The pinned Stream contract stores envelope fields and signature commitments;
it does not verify the signature bytes. The draft therefore adds optional
EIP-712/ERC-1271 writer authorization in the Museum registry without changing
the shared envelope or claiming that a Stream record's signature fields are a
legal signature verifier.

### 3. The exact envelope has no revision field

Revision, predecessor, lane head, chain accumulator, recorder, authorization
class, and recorded time must live in Museum sidecar state/event metadata. The
payload schema must carry correction/supersession semantics. This preserves
the Stream field layout and still gives the Museum append-only correction
lineage and state-readable reconstruction.

### 4. Pinned Stream profile names are ahead of published schema artifacts

The pinned Museum interoperability document identifies profiles such as
`STREAM_IIIF_P3_MIN_V1`, `STREAM_BAGIT_PROFILE_V1`,
`STREAM_CONDITION_REPORT_V1`, `STREAM_ACQUISITION_PACKET_V1`, and
`STREAM_OBJECT_DOSSIER_V1`. The pinned Stream source describes a genesis schema
set, but it does not provide standalone canonical JSON Schema documents and
IDs for all named profiles in a form that this repository can safely copy.
The draft treats this as a convergence/deployment gate rather than guessing
identifiers.

### 5. Storage must survive log loss

The pinned Stream preservation module stores the complete record envelope in
state and emits it in `CollectionRecordRecorded`. The Museum registry should
follow that reconstructability model: envelope, summary, inline payload where
selected, lane head, subject identity, schema/profile admission, and authority
state must be readable without historical event logs. Events remain valuable
for indexing and audit but cannot be the only durable copy.

### 6. CAIP identity requires a registered profile

CAIP-19 does not itself prescribe a universal address-casing rule. The Museum
must pin lowercase EVM contract addresses in canonical citations, retain EIP-55
only as display data, and register versioned profiles for Counterparty/Bitcoin,
legacy EVM, and future namespaces before using them in subject derivation.
The original canonical string must remain retrievable; a hash-only subject is
not a catalog identifier.

### 7. Casey is a proposed multi-object donation, not a verified accession

The Casey working plan proposes `6529NM.2026.001` with seven object IDs, but
explicitly says no contract addresses, token IDs, title evidence, custody,
rights, or review authority are verified. The safe migration is a WIP research
record, not an `ACCESSION`, `TITLE_BINDING`, or completed custody record.
Future acceptance must append one object-level Stream accession record and
object evidence per token; the lot-level curatorial statement cannot replace
those records.

### 8. Keys and Gates selection must remain separate from accession

The current memory records 16 Wave `WINNER` outcomes and a formal program
with CC0, consent, availability, acquisition, and documentation requirements.
`WINNER` is selection evidence only. A future Stream-native Keys and Gates
token can use the Museum program/outcome IDs plus Stream owner records after
mint/acquisition verification, with a Museum cross-reference and no replacement
token identity.

## Resolved design decisions for the draft

1. Use a non-proxy, append-only `NetworkMuseumRegistryV1` with a successor
   pointer and one-way write freeze.
2. Preserve Stream's exact envelope and shared identifiers; define new Museum
   IDs only for Museum-native payloads and sidecar domains.
3. Use CAIP-profiled subject registration and store canonical asset strings;
   retain the existing Museum subject-domain literal
   `6529networkmuseum.subject.external-asset.v1` while including the admitted
   asset-profile ID in the V1 derivation to prevent cross-profile collisions.
4. Use EIP-712/EIP-1271 for optional relayed writes, unordered signer-scoped
   nonces, deadlines, and nonce revocation.
5. Require lane predecessor matching and a deterministic chain accumulator;
   keep supersession meaning in the payload.
6. Store full envelopes and selected payload bytes in state; use content-
   addressed URIs and hash commitments for larger/restricted material.
7. Batch migration atomically, with a bounded batch size and state-based reorg
   retry.
8. Keep custody, title, rights, and accession as independently evidenced facts.

## Unresolved before deployment

* Exact schema documents and IDs for every shared Stream profile actually used
  by the first migration must be reconciled with Stream's active system
  manifest, not only the pinned prose names.
* The Museum must choose its production authority/provider implementation and
  approve its family grants; the current Safe signer list must not be embedded
  as contract logic.
* Supported non-EVM/legacy asset profiles need maintainers, resolution rules,
  collision tests, and independent verification adapters.
* The inline payload limit, storage budget, URI policy, and content-addressed
  storage families need an operations decision and preservation rehearsal.
* Registrar, curator, digital-conservation, privacy, and independent security
  reviews are required before governance can approve deployment.

## Negative claims preserved

This review does not claim that any Casey work is accessioned, that any Keys
and Gates winner is minted or in Museum custody, that a wallet transfer proves
title, or that a vote total proves governance adoption. Those facts remain
subject to the repository's evidence and accession rules.
