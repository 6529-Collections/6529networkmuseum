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
   commit `payloadMode` and `supersedesRecordHash` into the Museum hash, and
   enforce an existing, same-lane, older supersession target while retaining
   the schema-defined payload fields.
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
* The V1 inline caps and Stream-safe URI policy are pinned; storage budget,
  public-network resolution evidence, and content-addressed storage families
  still need an operations decision and preservation rehearsal.
* Registrar, curator, digital-conservation, privacy, and independent security
  reviews are required before governance can approve deployment.

## PR #2 general-review resolutions

The 6529bot general review on PR #2 identified seven valid specification gaps;
all are addressed in the companion contract specification:

1. `INLINE` is now explicitly restricted to nonempty RFC 8785/JCS UTF-8 JSON
   using Keccak-256. SHA-256, BLAKE3, multihash, IPFS-CID, and Arweave
   payloads remain content-addressed or `NONE` in V1; no algorithm-specific
   integrity check is implied for inline bytes outside that profile.
2. The normative record vector now pins every envelope/preimage field,
   including `signatureScheme = 0x00...00`, an empty `signatureHash`, its
   zero algorithm/canonicalization fields, both `HashRef` sub-hashes, and the
   exact payload mode.
3. The by-signature ABI now carries `signedRecordHash` and
   `signedPreviousRecordHash`. The implementation must recompute the record
   hash, compare both signed values to the supplied values, compare the
   predecessor to the lane head, and only then verify the EIP-712 signature.
4. Identical envelopes are global immutable duplicates: a second occurrence
   always reverts and never advances a lane. A correction must change a
   hashed envelope field and carry payload-level supersession evidence.
5. V1 pins `MAX_INLINE_PAYLOAD_BYTES = 16,384`,
   `MAX_BATCH_RECORDS = 64`, and `MAX_BATCH_INLINE_PAYLOAD_BYTES = 262,144`,
   with both per-record and aggregate limits applying to batches.
6. The Museum ABI now uses `InvalidMuseumHashRef`; the pinned Stream
   adapter's `InvalidHashRef` remains external and is explicitly not
   redeclared by the Museum registry.
7. The exact EIP-712 type string, signed-value bindings, and an independent
   Foundry `cast` transcript are now normative and reproducible.

The follow-up review also identified and resolved three implementation hazards:

1. `hashRefHash` always re-hashes the exact bytes in `HashRef.digest`, regardless
   of the algorithm. The transcript now computes that second hash explicitly;
   the corrected content-ref, record-hash, chain-hash, and EIP-712 values below
   were independently recomputed from it. The final EIP-712 digest uses the
   raw two-byte `0x1901` prefix, not ABI encoding of `bytes2`.
2. `recordMuseumRecordBySig` explicitly applies the §5.2 payload mode, inline
   profile, byte-cap, zero-payload, and digest checks to its payload argument.
3. A duplicate `recordHash` in an all-or-nothing batch reverts the entire batch;
   reorg retries must exclude every record already present on the surviving
   chain. Direct/batch envelope-field violations use
   `InvalidEnvelopeSignatureFields`, while `bySig` uses
   `InvalidRelayedSignatureFields`.

The independent implementation-readiness review added and resolved these
further requirements:

1. `revokeNonceBySig` has its own exact EIP-712 type string, domain, typehash,
   raw-prefix digest, state view, event, deadline, and `keccak256(signature)`
   commitment.
2. The pinned Stream commit's prose-only owner-record description is now an
   explicit provisional interface and vector with a closed convergence gate;
   the draft makes no executable compatibility claim.
3. Payload mode is an explicit ABI `uint8` and record-hash field. External
   asset registration and mirror-link selectors are role-gated, canonical,
   expected-subject-bound, and write-once.
4. ERC-1271 calls are non-reentrant and recheck lane-head/nonce state after
   the external callback. Supersession metadata is hash-bound and the target
   must exist in the same lane at an older revision.
5. URI schemes are restricted to `https`, `ipfs`, and `ar` with the public
   network safety gate; `MUSEUM_RELEASE_MANIFEST_V1` pins its JSON schema,
   source ordinal, entry hash, root formula, and worked root vector.

The exact-head review additionally required and resolved:

1. Global role IDs now authorize `setAuthority`, `setSuccessor`,
   `freezeWrites`, subject registration, mirror links, and convergence actions
   without an ambiguous family grant. Authority queuing, 48-hour timelock,
   successor-after-freeze, one-way freeze, role revocation, and transition
   events are normative.
2. `RecordSummary` and `MuseumRecordRecorded` now persist and emit relayer,
   nonce, deadline, outside-envelope signature scheme, signature commitment,
   class, and authority revision. Direct writes have explicit zero values.
   Revocation state/event fields distinguish `nonceRevision` from
   `authorityRevision`.
3. Asset profiles pin canonicalizer runtime/implementation hashes and version
   IDs, with immutable-runtime and EIP-1967 proxy checks on every registration.
4. The URI rule is now the versioned Museum-specific
   `MUSEUM_URI_SAFETY_PUBLIC_V1` predicate, with an exact HTTPS public-network
   assertion record and EIP-712 signature format plus explicit Stream-adapter
   convergence behavior.
5. The manifest fixture uses actual 40-hex Git SHA-1 values for the source and
   pinned Stream commits, right-aligned into `bytes32`; the root was
   independently recomputed.

### Reproducible hash transcript

This transcript was run in a clean PowerShell session with Foundry `cast`.
The commands use only the literals, ABI types, and values printed here; they
do not read repository state or rely on an implementation. The output is the
golden vector set for the draft.

```powershell
$domain = '0x0c86cc4258c69b4674aa86e715d4d167bd8288b78832a0a4c5a37943b31876c4'
$chainDomain = '0x4bc9065a5ebf49c9fff664fca90b1a40c0edac25bd076026f1b2685de7db666a'
$subjectDomain = '0x1dd722ea239e47e25bdadfcc0053bdc4e7ee75e7ca9dd0afe97076a6d9eb8a80'
$assetProfile = '0xac72cc7c2b027b8ee3d459de7829fd7b3b31cf575c28734e736ebd33b10f41cc'
$canon = '0x886c7c89c308c459ca8a626e0ef36a5ea9f4c7a7b56aaf86c71a2ddf3b4f9044'
$type = '0x5a50f1234f1c89b5d9c2f5b2062279349feac41d8e01bf708ee9adc20a2d8ba0'
$subject = '0x1111111111111111111111111111111111111111111111111111111111111111'
$schema = '0xe3d3da75ee91ec6a7603f809eb413342e42874cabf3992d443409657745c3cf0'
$asset = 'eip155:1/erc721:0x06012c8cf97bead5deae2370709587f8e7a266d/771769'
$payload = '{"id":"6529NM.2026.001.1","status":"proposed"}'
$uri = 'ipfs://bafybeigdyrzt5example'
$assetHash = cast keccak $asset
$externalSubjectId = cast keccak (cast abi-encode 'f(bytes32,bytes32,bytes32)' $subjectDomain $assetProfile $assetHash)
$contentDigest = cast keccak $payload
$contentDigestHash = cast keccak $contentDigest
$uriHash = cast keccak $uri
# hashRefHash always places keccak256(ref.digest), not ref.digest, in slot 2.
# Here contentDigest is the stored 32-byte HashRef.digest, so it is re-hashed.
# The record vector uses the separately pinned $subject value above.
$contentRef = cast keccak (cast abi-encode 'f(uint16,bytes32,bytes32)' 1 $contentDigestHash $canon)
$emptyBytesHash = '0xc5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470'
$signatureRef = cast keccak (cast abi-encode 'f(uint16,bytes32,bytes32)' 0 $emptyBytesHash 0x0000000000000000000000000000000000000000000000000000000000000000)
$zero = '0x0000000000000000000000000000000000000000000000000000000000000000'
$recordHash = cast keccak (cast abi-encode 'f(bytes32,uint256,address,bytes32,bytes32,bytes32,bytes32,bytes32,bytes32,bytes32,uint64,uint8,bytes32)' $domain 1 0x0000000000000000000000000000000000000001 $type $subject $contentRef $uriHash $schema $zero $signatureRef 1722470400 1 $zero)
$chainHash = cast keccak (cast abi-encode 'f(bytes32,bytes32,bytes32,uint64)' $chainDomain 0x0000000000000000000000000000000000000000000000000000000000000000 $recordHash 1)
$domainTypeHash = cast keccak 'EIP712Domain(string name,string version,uint256 chainId,address verifyingContract)'
$nameHash = cast keccak '6529 Network Museum Registry'
$versionHash = cast keccak '1'
$domainSeparator = cast keccak (cast abi-encode 'f(bytes32,bytes32,bytes32,uint256,address)' $domainTypeHash $nameHash $versionHash 1 0x0000000000000000000000000000000000000001)
$writeTypeHash = cast keccak 'MuseumRecordWrite(bytes32 recordHash,bytes32 recordType,bytes32 subjectId,bytes32 previousRecordHash,uint256 nonce,uint64 deadline)'
$structHash = cast keccak (cast abi-encode 'f(bytes32,bytes32,bytes32,bytes32,bytes32,uint256,uint64)' $writeTypeHash $recordHash $type $subject 0x0000000000000000000000000000000000000000000000000000000000000000 7 1800000000)
$eipPreimage = '0x1901'+$domainSeparator.Substring(2)+$structHash.Substring(2)
$digest = cast keccak $eipPreimage
$nonceTypeHash = cast keccak 'MuseumNonceRevocation(address signer,uint256 nonce,uint64 deadline)'
$signer = '0x000000000000000000000000000000000000dead'
$nonceStructHash = cast keccak (cast abi-encode 'f(bytes32,address,uint256,uint64)' $nonceTypeHash $signer 7 1800000000)
$noncePreimage = '0x1901'+$domainSeparator.Substring(2)+$nonceStructHash.Substring(2)
$nonceDigest = cast keccak $noncePreimage
$manifestEntryDomain = cast keccak '6529networkmuseum.release-manifest.entry.v1'
$manifestRootDomain = cast keccak '6529networkmuseum.release-manifest.root.v1'
$pathHash = cast keccak 'specs/onchain/contract-migration-v1.md'
$payloadBytesHash = cast keccak $payload
$entryHash = cast keccak (cast abi-encode 'f(bytes32,uint64,bytes32,bytes32,uint8,bytes32)' $manifestEntryDomain 1 $pathHash $recordHash 1 $payloadBytesHash)
$sourceCommitHex = '6ab83b456f1ad8d1b7b88b79cc960954feb56432'
$streamCommitHex = '5021c8060950c3fef995271e674ed4b2007fee6d'
$sourceCommit = '0x'+('0'*24)+$sourceCommitHex
$streamCommit = '0x'+('0'*24)+$streamCommitHex
$generatorHash = cast keccak 'museum-migration/1.0.0'
$manifestRoot = cast keccak (cast abi-encode 'f(bytes32,bytes32,bytes32,bytes32,uint64,bytes32[])' $manifestRootDomain $sourceCommit $streamCommit $generatorHash 1 "[$entryHash]")
$ownerDomain = cast keccak '6529networkmuseum.stream-owner-record.v0'
$ownerVector = cast keccak 'STREAM_OWNER_RECORD_HASH_VECTOR_V0'
$ownerStreamCore = '0x0000000000000000000000000000000000001001'
$ownerModule = '0x0000000000000000000000000000000000002002'
$ownerSubject = '0x1111111111111111111111111111111111111111111111111111111111111111'
$ownerPayload = '{"record":"owner","tokenId":"771769"}'
$ownerPayloadHash = cast keccak $ownerPayload
$ownerRecordHash = cast keccak (cast abi-encode 'f(bytes32,uint256,address,address,uint256,uint256,bytes32,bytes32)' $ownerDomain 1 $ownerModule $ownerStreamCore 42 771769 $ownerSubject $ownerPayloadHash)
$assetHash
$externalSubjectId
$contentDigest
$contentDigestHash
$uriHash
$contentRef
$signatureRef
$recordHash
$chainHash
$domainTypeHash
$domainSeparator
$writeTypeHash
$structHash
$digest
$nonceTypeHash
$nonceStructHash
$nonceDigest
$manifestEntryDomain
$manifestRootDomain
$pathHash
$payloadBytesHash
$entryHash
$manifestRoot
$ownerDomain
$ownerVector
$ownerPayloadHash
$ownerRecordHash
```

Expected output, in order:

```text
0x0ff37eede3af67254c8d44c52b88bce8e1b191ace633f456212fd13d9cbdcca9
0xa6e5bb8be82a8267e4c7a5398a63d1b1cf8d3c612aa4529349882667e8a2ba78
0x5eb73c2a5337f2ba50340e7a39042e942894d09ec210e537334fbe068b710b73
0x23a91b3a3e46e505e103bc13198f617068273bf16ef976794ee14bde2640a2e5
0x8104a3a6d02c26de42514a3425567e1b75724dfda699658584c39e61153b713c
0x66de33e7d57cf2169917368e5d3e0e9e9841cd367f8de4ff95f3a15164456462
0x2653d71e6881daccbff9917e23f12df8e56f7a0f8688215ca7092a5368a7d470
0xc4c82486491323ce9af3d84d00b239e1148832fb059b8880483e4a838b320627
0xd4e3b242f775f431ac172cd764f032addceb847ceb646845c74b9fb6d6319f63
0x8b73c3c69bb8fe3d512ecc4cf759cc79239f7b179b0ffacaa9a75d522b39400f
0xfffa62454cc94111fc3da4487def1fc9f0e36727a701015f2a46ff4a1a7c7b70
0xa7df80542664ee83129e8d3ace9f44135f9a4514ad949246a14df795f16dbb3e
0x7d4ea0e0c6cc267d01b953edec4e87a7dc20e2cc8a0c882037830608b426c57b
0xee99a98f35e2cc855f10e1feeb3c21be639e75dd2c2c28effc811cf09cf8f4b8
0xe97842aa32d8e097ebbd7f3ac132b20c38ade8bb2862f2dcda25fb3b4fe51eef
0xadf1dd94e8baaec142f9dbd1eb48a0a874d50bf369dd06d1dfd0ab0e374eae13
0x87c87440dbee8e7d2313e0be413d6222bea14055b0f324da81e0e9ef8849e4cd
0xa524091b411df027ff64e4f8d590d93cf7e2e7658f6a5a8f623abfb4e01671ef
0xe615064b79fb81a121afe1ad24d886aa86536f320be540a31023f43bbe935b64
0x47f5e941106c25d308590891c8eb0bb3c721586361b9a9bf442b49782c132183
0x5eb73c2a5337f2ba50340e7a39042e942894d09ec210e537334fbe068b710b73
0x3aa074dec49b0294d9abb908dceea5a4d202418c4c3853fdf844bd645f62b7f7
0x685f7fa37801cc1c6264ff9bbf143d836926887ad890132e43a1943b7a91b41a
0x148c88658eea0b57062f88c63dba1f2aa0ffd33da6528e2a1ace1f145cf2b54a
0x8642db6f4603da6e1d6676bd54b8c64cc5c4f06521236402b75e1b84ab928e3c
0x1978e517eeb4e20fc20ca3b1110613584494206425197a9d447d7e11c6dab70d
0xee351e5f3e3edbbdf00670dc9116f99ef5ed8da4d070b6a3c734d81a099b0fd4
```

The EIP-712 preimages are constructed by literal hex concatenation. A
command using `cast abi-encode 'f(bytes2,bytes32,bytes32)'` inserts ABI padding
for `bytes2` and is intentionally not a valid conformance command.

The EIP-712 signature bytes are intentionally absent from the record-hash
preimage; V1 uses zero/empty envelope signature fields for `bySig` writes and
keeps the relay signature in authorization metadata, as specified above.

## Negative claims preserved

This review does not claim that any Casey work is accessioned, that any Keys
and Gates winner is minted or in Museum custody, that a wallet transfer proves
title, or that a vote total proves governance adoption. Those facts remain
subject to the repository's evidence and accession rules.
