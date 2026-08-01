# Network Museum contract migration specification — V1 draft

Status: implementation-grade working specification; not adopted policy, not deployed, and not an implementation.

Pinned compatibility target: `6529-Collections/6529Stream` `origin/main` commit
`5021c8060950c3fef995271e674ed4b2007fee6d`, observed 2026-08-01 UTC.

This specification defines the first Museum registry that can carry governed
GitHub records to an append-only on-chain record chain. It covers external
tokens, Museum-native governance and accession records, and a bilateral path
for future Stream-native works. It does not mint, wrap, transfer, or deploy
anything.

The words MUST, MUST NOT, SHOULD, SHOULD NOT, and MAY are normative.

## 1. Decision summary

The Museum deploys a small token-agnostic `NetworkMuseumRegistryV1`.

* The original token remains the artwork identity. The registry records
  Museum assertions about that token; it never wraps or remints it.
* Every record uses the exact Stream `HashRef` and `CollectionRecord` field
  shapes. Museum chain metadata is stored beside the envelope, not inserted
  into it.
* Rich canonical payloads and archival dossiers are content-addressed. The
  registry stores the envelope, hash commitments, URI, lane head, and small
  payload bytes where configured. Events are an index, never the only copy.
* `effectiveAt` is the asserted effective time. `recordedAt`, revision, and
  predecessor describe the append operation. Latest is last accepted write,
  not the record with the greatest `effectiveAt`.
* Supersession is append-only. A correction is a new record whose payload
  identifies the superseded record and explains the change; no prior record is
  deleted or edited.
* Custody, legal title, copyright, and accession remain separate assertions.
  A registration, transfer, or `WINNER` label is never accession by itself.
* The pinned Stream commit supplies the collection-record ABI, but it does
  not pin an executable owner-record ABI or hash formula. V1 therefore does
  not claim that a Museum contract can write Stream owner records. A future
  Stream-native integration is provisional until the bilateral convergence
  gate in §2.1 passes. Until then, the Museum may carry a proposed work and
  its evidence, but it MUST NOT label that as a successful Stream owner-record
  write.

## 2. Compatibility facts pinned from Stream

At the pinned commit, `IStreamPreservationRecords` defines these exact
structures and must not be approximated:

```solidity
struct HashRef {
    uint16 algorithm;
    bytes digest;
    bytes32 canonicalizationId;
}

struct CollectionRecord {
    bytes32 recordType;
    bytes32 subjectId;
    HashRef contentHash;
    string uri;
    bytes32 schemaId;
    bytes32 signatureScheme;
    HashRef signatureHash;
    uint64 effectiveAt;
}
```

The pinned Stream implementation also establishes the following behavior
that a bilateral adapter MUST respect:

* `HASH_KECCAK256 = 1`, `HASH_SHA256 = 2`, `HASH_BLAKE3 = 3`,
  `HASH_MULTIHASH = 4`, `HASH_IPFS_CID = 5`, and `HASH_ARWEAVE_TX = 6`.
* Required `HashRef` values have a nonzero canonicalization ID. Keccak-256,
  SHA-256, and BLAKE3 use 32-byte digests. Multihash and IPFS CID digests
  are nonempty and at most 128 bytes. Arweave transaction digests are
  32 bytes. Unknown algorithms revert.
* A zero `signatureScheme` requires an entirely empty `signatureHash`.
  A nonzero scheme requires a valid required `signatureHash`.
* The URI is valid UTF-8 and at most 2,048 bytes.
* `effectiveAt` and `recordType`, `subjectId`, and `schemaId` are nonzero.
* Stream record storage is keyed by a domain-separated hash and latest is
  last-write-wins by record time, not maximum `effectiveAt`.
* The pinned Stream module does not verify the signature bytes in the
  envelope; its signature fields are commitments. The Museum registry adds
  optional EIP-712/ERC-1271 authorization for relayed writes without changing
  those envelope semantics.

The relevant pinned Stream ABI is:

```solidity
function recordCollectionRecord(uint256 collectionId, CollectionRecord calldata record)
    external returns (bytes32 recordHash);
function latestCollectionRecordHash(uint256 collectionId, bytes32 recordType, bytes32 subjectId)
    external view returns (bytes32);
function collectionRecordSummary(bytes32 recordHash)
    external view returns (CollectionRecordSummary memory);
function collectionRecord(bytes32 recordHash)
    external view returns (CollectionRecord memory);
function deriveCollectionRecordHash(uint256 collectionId, CollectionRecord calldata record)
    external view returns (bytes32);
```

Its write is additionally constrained by an existing Stream collection and
the Stream record-family registry. The Museum registry intentionally has no
`collectionId` requirement because an external ERC-721, ERC-1155, legacy EVM,
Bitcoin/Counterparty, or future namespace is not a Stream collection.

### 2.1 Provisional owner-record boundary

The pinned Stream source has prose describing owner records, but it does not
publish a callable owner-record selector, module ABI, or owner-record hash
preimage. No V1 requirement may therefore say that the Museum can call a
canonical Stream owner-record method. The following is a deliberately
provisional bilateral interface for design and test-vector purposes only; it
is not asserted to exist at `5021c8060950c3fef995271e674ed4b2007fee6d`:

```solidity
interface IProvisionalStreamOwnerRecordV0 {
    function ownerRecordHash(uint256 tokenId) external view returns (bytes32);
    function ownerRecordHashDomain() external pure returns (bytes32);
    function ownerRecordHashVectorId() external pure returns (bytes32);
}
```

External asset profiles use an admitted canonicalizer with the following
read-only contract surface. The registry MUST accept a candidate only when
the adapter returns the same canonical bytes supplied by the caller:

```solidity
interface IMuseumAssetCanonicalizerV1 {
    function canonicalize(bytes32 profileId, string calldata supplied)
        external view returns (string memory canonical);
    function versionId(bytes32 profileId) external view returns (bytes32);
    function implementationCodeHash(bytes32 profileId) external view returns (bytes32);
}
```

If adopted, the module's returned hash MUST be:

```solidity
keccak256(abi.encode(
    0x148c88658eea0b57062f88c63dba1f2aa0ffd33da6528e2a1ace1f145cf2b54a,
    block.chainid,
    ownerRecordModule,
    streamCore,
    collectionId,
    tokenId,
    streamSubjectId,
    keccak256(canonicalOwnerRecordPayload)
))
```

The exact bilateral reference carries `ownerRecordModule`, `streamCore`,
`collectionId`, `tokenId`, `streamSubjectId`, `ownerRecordHash`,
`ownerRecordHashDomain`, and `ownerRecordHashVectorId`. A mirror link MUST
not be described as a Stream owner-record write unless all of these values
are returned or independently verified by the converged adapter.

The convergence gate is closed until Stream publishes and pins the callable
ABI, module/version semantics, exact hash-domain literal and formula, payload
canonicalization, vector, and a round-trip test against a deployed Stream
module. The Museum deployment gate MUST record that evidence and the exact
Stream commit. Before that gate, Keys and Gates records remain Museum-side
proposals/evidence and a link, if admitted by governance, is only a
provisional cross-reference—not an owner-record mutation or title assertion.

## 3. Exact identifiers and profile rule

Identifiers are `keccak256` of the exact ASCII literal unless the value is a
numeric algorithm ID. Hex values are lowercase in this document.

### 3.1 Stream identifiers already pinned in the Museum profile

| Kind | ASCII literal | ID |
|---|---|---|
| Hash algorithm | `HASH_KECCAK256` | `1` |
| Hash algorithm | `HASH_SHA256` | `2` |
| JSON canonicalization | `RFC8785_JCS` | `0x886c7c89c308c459ca8a626e0ef36a5ea9f4c7a7b56aaf86c71a2ddf3b4f9044` |
| Record type | `ACCESSION` | `0x4dc3a5e33f97bcd06f2d025349086438272d94a398185aca416ae539e36521fb` |
| Schema | `STREAM_ACCESSION_V1` | `0xc04bb48f95c8db4fe7f26a20106533f987003843f2fed36fd6d89f207ddfbd86` |
| Record type | `WORK_DESCRIPTION` | `0x3b172fd545b59c0d525256a31f44b4304ca8e7e06892d1ba171dff45a7f1a9e6` |
| Schema | `STREAM_WORK_DESCRIPTION_V1` | `0x5bb3543c4c007f4396474b74ec81dd8bca13028b6d945020e4b48ff236b26a3c` |
| Record type | `RIGHTS_STATEMENT` | `0x45bc8cdeb4a6cf2cd35075c4e3176254f0ea24f8e938f632c52c83ef8d8434df` |
| Schema | `STREAM_RIGHTS_V1` | `0xdfdea1c86219c12e182b4023d399be35bd5602461ef1dc727784c18d7742b967` |
| Schema | `STREAM_PREMIS_V3_PROFILE` | `0x5df5267e55cdb4ee470cec99deebfeef16d1bb34992fa36b21a3b2e3d38ccc45` |
| Schema | `STREAM_LIDO_PROFILE_V1` | `0xbb318aaa815fbe5cb8cfa584f0102a18948118afe3ba1709cadc6ae36dba22f9` |

The pinned Museum interoperability document names
`STREAM_IIIF_P3_MIN_V1`, `STREAM_BAGIT_PROFILE_V1`,
`STREAM_CONDITION_REPORT_V1`, `STREAM_EXHIBITION_V1`,
`STREAM_ACQUISITION_PACKET_V1`, `STREAM_OBJECT_DOSSIER_V1`, and related
profiles, but the pinned Stream commit does not publish standalone canonical
schema documents and IDs for all of them. V1 MUST NOT guess an ID. A profile
is admissible only after its exact literal, schema bytes, RFC 8785 document
hash, and at least one worked vector are recorded in the deployment manifest.

### 3.2 Museum V1 constants

These constants are new Museum identifiers and do not redefine a Stream ID:

| Kind | ASCII literal | ID |
|---|---|---|
| Record hash domain | `6529networkmuseum.record.v1` | `0x0c86cc4258c69b4674aa86e715d4d167bd8288b78832a0a4c5a37943b31876c4` |
| Record-chain domain | `6529networkmuseum.record-chain.v1` | `0x4bc9065a5ebf49c9fff664fca90b1a40c0edac25bd076026f1b2685de7db666a` |
| External subject domain | `6529networkmuseum.subject.external-asset.v1` | `0x1dd722ea239e47e25bdadfcc0053bdc4e7ee75e7ca9dd0afe97076a6d9eb8a80` |
| CAIP-19 asset profile | `MUSEUM_ASSET_PROFILE_CAIP19_V1` | `0xac72cc7c2b027b8ee3d459de7829fd7b3b31cf575c28734e736ebd33b10f41cc` |
| Relayed authorization scheme (outside the envelope) | `MUSEUM_SIGNATURE_EIP712_RECORD_V1` | `0xd522d14409fadb7afb8c4cbf90ad662519010926e69625200b14f0ba12c90cba` |
| Relayed nonce-revocation scheme (outside the envelope) | `MUSEUM_SIGNATURE_EIP712_NONCE_REVOKE_V1` | `0xda7e20c41761de210a954ede904dd134c0d4dd6c8dc7e73c4072a8c717b956a5` |
| Global role | `MUSEUM_GLOBAL_ROLE_GOVERNANCE_EXECUTOR_V1` | `0x865cb1cc1a43094ea97b42f5b9e950e7952c1f106d37051e97d2a3fdb1584ce2` |
| Global role | `MUSEUM_GLOBAL_ROLE_REGISTRAR_V1` | `0xb1f5e657823d31bde6c263be60f0418d7361b8365b264c97798c0b790c1a5f8b` |
| Global role | `MUSEUM_GLOBAL_ROLE_MIGRATION_ADMIN_V1` | `0x2729f1662f9bb2682a0a433e8329cd1b73680e122f49b4b4987cef1106b97004` |
| Global role | `MUSEUM_GLOBAL_ROLE_AUTHORITY_ADMIN_V1` | `0x28ad41c29b6a0872dec6410316cebb3f72fc3c9e4f4ea88e8e87e81784c94426` |
| Museum URI safety profile | `MUSEUM_URI_SAFETY_PUBLIC_V1` | `0x5480eb62c7af1dd376bd8ddad6729a756d0f05ce8610d2a21e798440fc859189` |
| HTTPS assertion record type | `MUSEUM_HTTPS_PUBLIC_NETWORK_ASSERTION_V1` | `0x8041bfef6459ccf942bb6bfe17c778c4db60a9d0831f24f6154deba96e99391e` |
| HTTPS assertion signature scheme | `MUSEUM_SIGNATURE_EIP712_HTTPS_PUBLIC_V1` | `0x738aed5a63fd21dfdd96f878826e6652140072c65ee952653d5432bf6ded33d0` |
| HTTPS assertion subject domain | `6529networkmuseum.subject.https-public.v1` | `0xe08003722c1e7c0465bdd4353706df75808fa767fca549cc020bd0c0081e59f4` |
| Provisional Stream owner-record hash domain | `6529networkmuseum.stream-owner-record.v0` | `0x148c88658eea0b57062f88c63dba1f2aa0ffd33da6528e2a1ace1f145cf2b54a` |
| Provisional Stream owner-record vector | `STREAM_OWNER_RECORD_HASH_VECTOR_V0` | `0x8642db6f4603da6e1d6676bd54b8c64cc5c4f06521236402b75e1b84ab928e3c` |
| Payload schema | `MUSEUM_REGISTRY_RECORD_V1` | `0xc9f2c9b650ebb4955871484238be9d3dfd1bf9f0ec09a5365917d6294e5967c9` |
| Payload schema | `MUSEUM_EXTERNAL_ASSET_IDENTITY_V1` | `0x34e9649723069df3772c810e6e825f7589c211bac81acc9b908a60067f936aa6` |
| Payload schema | `MUSEUM_CUSTODY_OBSERVATION_V1` | `0xb0c467baa7db6862385e58253c1c4702d95b141a1ef66cd2b86234a597344014` |
| Payload schema | `MUSEUM_ACCESSION_LOT_V1` | `0x8bb4cfecf4d3736765bc80624dd0a876d2e1c17bf5a406066d5f2256fc739d44` |
| Payload schema | `MUSEUM_PROGRAM_OUTCOME_V1` | `0x7a25e6a6a5e91d55ef0ea9115ad5902929bcf0d3331b4bb2d22100f65fc78470` |
| Payload schema | `MUSEUM_RELEASE_MANIFEST_V1` | `0x7a41091035def3c5fa62722d73a7ea87f996fe9be34e9115317c5d128581d299` |
| Payload schema | `MUSEUM_RESEARCH_NOTE_V1` | `0xe3d3da75ee91ec6a7603f809eb413342e42874cabf3992d443409657745c3cf0` |
| Manifest entry domain | `6529networkmuseum.release-manifest.entry.v1` | `0xa524091b411df027ff64e4f8d590d93cf7e2e7658f6a5a8f623abfb4e01671ef` |
| Manifest root domain | `6529networkmuseum.release-manifest.root.v1` | `0xe615064b79fb81a121afe1ad24d886aa86536f320be540a31023f43bbe935b64` |

The subject formula is:

```solidity
bytes32 constant MUSEUM_SUBJECT_EXTERNAL_ASSET_V1 =
    0x1dd722ea239e47e25bdadfcc0053bdc4e7ee75e7ca9dd0afe97076a6d9eb8a80;

function externalAssetSubjectId(bytes32 assetProfileId, string memory canonicalAssetId)
    pure returns (bytes32)
{
    return keccak256(abi.encode(
        MUSEUM_SUBJECT_EXTERNAL_ASSET_V1,
        assetProfileId,
        keccak256(bytes(canonicalAssetId))
    ));
}
```

The registry stores the canonical string and its profile, not only the hash.
An unregistered or unprofiled string is not a usable Museum subject.

## 4. Identity, custody, title, and accession

### 4.1 CAIP identity

Asset identity uses CAIP-2, CAIP-10, and CAIP-19-shaped values:

* EVM ERC-721: `eip155:<decimal-chain-id>/erc721:<lowercase-20-byte-address>/<token-id>`.
* EVM ERC-1155: `eip155:<decimal-chain-id>/erc1155:<lowercase-20-byte-address>/<token-id>`.
* Custody account: `eip155:<decimal-chain-id>:<lowercase-20-byte-address>`.
* Bitcoin mainnet: `bip122:000000000019d6689c085ae165831e93`.

EIP-55 is retained only as a display form. Subject derivation uses the
lowercase canonical asset string. A non-EVM or legacy namespace needs an
admitted, versioned profile containing normalization, resolution, collision,
and worked-vector rules. Individual records MUST NOT invent an ad hoc string.

The Museum-native record IDs remain stable and chain-independent, for example
`6529NM.2026.001.1`. Chain, contract, wallet, creator, and collection data
are typed fields, never accession-number components.

### 4.2 Separate assertions

An `MUSEUM_CUSTODY_OBSERVATION_V1` payload records:

* CAIP-19 asset identity and the observed state qualifier (`@fin:`, `@snap:`,
  or `@chain:` plus a bytes32 state commitment where applicable);
* CAIP-10 custody account, observed block/height, transaction or proof URI,
  verification adapter/profile, and observation time;
* result `verified`, `pending`, `unverified`, `failed`, or `not_applicable`;
* evidence class and content-addressed evidence references.

For EVM ERC-721, a verifier checks `ownerOf(tokenId)`; for ERC-1155 it checks
the required balance; legacy and non-EVM assets use an admitted adapter or an
attributable independent attestation. The adapter reports evidence and never
declares legal title.

`STREAM_ACCESSION_V1` and Museum accession payloads keep these dates separate:

* acceptance date;
* legal title-passage date;
* on-chain custody receipt date;
* formal accession date;
* cataloguing, technical verification, preservation, and display dates.

The `TITLE_BINDING` is an instrument-to-one-transfer relation. It carries the
instrument hash/URI and non-sensitive custodian reference, transfer hash,
block/height, `from`, `to`, and the exact transfer to which title evidence
relates. Token control is not title. Title is not copyright. Copyright is not
display, reproduction, preservation, or migration permission.

No `ACCESSION` record may claim `accessioned` until the active Museum
completion profile verifies title evidence, custody evidence, rights,
technical receipt, and second-person review. A bare external-asset
registration is only identity registration.

## 5. Record model and storage

### 5.1 Record hash and lane

The Museum record hash is host-specific and deliberately separate from the
Stream hash:

```solidity
bytes32 recordHash = keccak256(abi.encode(
    MUSEUM_RECORD_HASH_DOMAIN,
    block.chainid,
    address(this),
    record.recordType,
    record.subjectId,
    hashRefHash(record.contentHash),
    keccak256(bytes(record.uri)),
    record.schemaId,
    record.signatureScheme,
    hashRefHash(record.signatureHash),
    record.effectiveAt,
    payloadMode,
    supersedesRecordHash
));

bytes32 hashRefHash(HashRef memory ref) {
    return keccak256(abi.encode(
        ref.algorithm, keccak256(ref.digest), ref.canonicalizationId
    ));
}
```

The implementation MUST use Solidity `abi.encode`, not packed encoding. The
inner `keccak256(ref.digest)` is always over the exact digest bytes stored in
the `HashRef`, regardless of `ref.algorithm`; it is not a conditional shortcut
for Keccak content. Thus a 32-byte SHA-256, BLAKE3, Arweave, or other fixed-size
digest is re-hashed as those 32 bytes before the outer ABI encoding. An
implementation MUST NOT substitute the source payload hash or skip this inner
hash merely because the digest came from content addressing. `payloadMode` is
a `uint8` encoded by `abi.encode` and is part of the Museum hash: `0 = NONE`,
`1 = INLINE`, and `2 = CONTENT_ADDRESSED`. The `supersedesRecordHash` slot is
zero for a non-correction. The Museum hash omits the predecessor so the same
immutable envelope has one identity even if an import is retried after a
reorg. A lane append separately computes:

```solidity
chainHash = keccak256(abi.encode(
    MUSEUM_RECORD_CHAIN_DOMAIN, previousChainHash, recordHash, revision
));
```

`recordHash` is a global immutable envelope identity, not a lane-entry ID. If
the same hash is already stored, every later write MUST revert with
`RecordAlreadyExists`, whether the requested predecessor is the same, a
different hash, or the current head of another lane. The registry MUST NOT
silently treat a duplicate as a new revision or move its latest pointer. A
migration client MAY treat a duplicate revert as an idempotent retry only
after reading the stored envelope, payload bytes, summary, and lane head and
confirming that they match the intended write; a duplicate in a different
lane is not a successful append.

A legitimate correction MUST therefore change at least one field committed by
`recordHash` (normally `contentHash`, `uri`, `schemaId`, `signatureScheme`,
`signatureHash`, `effectiveAt`, `payloadMode`, or the nonzero
`supersedesRecordHash`) and MUST carry payload-level
`supersedes`/reason/evidence. The supplied `supersedesRecordHash` MUST equal
the payload's schema-defined `supersedes` value; the contract enforces the
target's existence, lane, and age below, while the admitted schema validator
enforces that byte-level payload equality before submission. Repeating
byte-identical content under the same envelope is a reference to the existing
record, not a new revision. This explicitly resolves identical-envelope
recurrence: the first accepted hash wins, and corrections are new hashes.

Lanes are keyed by `(recordType, subjectId)`. Revision starts at 1. The first
record has predecessor and prior chain hash zero. A write MUST supply the
current lane head as `previousRecordHash`; a batch advances that head in array
order. A missing or incorrect predecessor reverts.

The record payload MUST contain the schema-defined correction fields when it
supersedes another record, including `supersedes`, `supersession_reason`,
`authority`, `effective_at`, and evidence references. The contract does not
parse arbitrary JSON; schema validation is a pre-write and deployment-gate
requirement. The contract still enforces the envelope, digest, URI, and
admitted-schema rules. When `supersedesRecordHash != bytes32(0)`, the target
MUST already exist, MUST have the same `recordType` and `subjectId`, and MUST
have a revision strictly less than the new revision. A target in another lane,
a missing target, or a target at or after the new revision MUST revert. A
nonzero target is immutable metadata in the record hash and `RecordSummary`,
so it cannot be detached or rewritten after signing.

### 5.2 State versus events

The registry stores enough state for a client with no event history to recover:

* every envelope by `recordHash`;
* a compact summary by `recordHash`;
* full inline payload bytes when `payloadMode == INLINE`;
* canonical asset strings and profile IDs;
* immutable Stream mirror links, including module/token/owner-record hash
  domain and vector fields;
* nonce-use and nonce-revocation state, including revocation deadline,
  signature commitment, actor, and revision;
* latest lane head and revision;
* admitted schema/profile/type documents and hashes;
* role/provider revisions, successor, and write-freeze state.

Events MUST expose the same commitments and are used for indexing and audit:
they are not the sole storage for records, payloads, or heads. Events MUST NOT
be used as an excuse to omit state-readable `payload`, `record`, or
`recordChainHead` views.

`payloadMode` is `NONE`, `INLINE`, or `CONTENT_ADDRESSED`. V1 pins these
limits and their interaction:

```solidity
uint256 constant MAX_INLINE_PAYLOAD_BYTES = 16_384;
uint256 constant MAX_BATCH_RECORDS = 64;
uint256 constant MAX_BATCH_INLINE_PAYLOAD_BYTES = 262_144;
```

For a batch, each `INLINE` payload MUST be at most
`MAX_INLINE_PAYLOAD_BYTES`, and the sum of all inline payload byte lengths in
the batch MUST be at most `MAX_BATCH_INLINE_PAYLOAD_BYTES`. The per-record
limit still applies when the batch contains one record. `CONTENT_ADDRESSED`
and `NONE` contribute zero to the batch inline-byte total.

* `INLINE` retains byte-identical canonical payload bytes, subject to a
  hard cap of `MAX_INLINE_PAYLOAD_BYTES`. V1 permits `INLINE` only when
  `contentHash.algorithm == HASH_KECCAK256` and
  `contentHash.canonicalizationId == RFC8785_JCS`. The bytes MUST be
  nonempty canonical UTF-8 JSON for the admitted schema. V1 does not accept
  SHA-256, BLAKE3, multihash, IPFS-CID, or Arweave `INLINE` payloads; a future
  algorithm-complete inline carrier requires a new version and new vectors.
* `CONTENT_ADDRESSED` stores no payload bytes and requires a URI plus matching
  `contentHash`.
* `NONE` is allowed only for explicitly schema-approved commitment records
  whose schema says that no payload bytes are needed.

The mode is an explicit `uint8` argument to every write path and is committed
by `recordHash`; it is not inferred from whether the `bytes` argument happens
to be empty. `recordMuseumRecord` and the batch `RecordInput` still carry the
mode even though they carry no inline bytes. `INLINE` requires nonempty bytes,
`CONTENT_ADDRESSED` requires zero bytes, and `NONE` requires zero bytes. Any
mode/bytes/URI/schema mismatch MUST revert. This makes all three modes
unambiguous to an ABI decoder, a signature verifier, and a state-only reader.

Meaning-bearing migration records SHOULD be inline when they are small enough;
large dossiers, media, legal instruments, private annexes, BagIt/OCFL objects,
and manifests live in content-addressed storage. For V1 `INLINE`, the contract
MUST verify `keccak256(payload) == bytes32(record.contentHash.digest)` and MUST
reject any nonempty payload under another hash/canonicalization profile. A
`CONTENT_ADDRESSED` record MUST pass the envelope's algorithm-specific
`HashRef` validation, but its bytes are intentionally not supplied to the
contract. `NONE` MUST supply zero payload bytes and an empty URI.

### 5.3 Content addressing and privacy

Repository JSON is canonicalized with RFC 8785 JCS and committed with
`HashRef(1, keccak256(canonicalBytes), RFC8785_JCS)`. Repository and BagIt
manifests additionally retain LF-normalized SHA-256. V1 uses the distinct,
versioned `MUSEUM_URI_SAFETY_PUBLIC_V1` predicate; it is not claimed to be
the pinned Stream URI predicate. The Museum predicate MUST accept an empty
URI only for `NONE`, otherwise accept only `https://`, `ipfs://`, or `ar://`,
and require valid UTF-8 of at most 2,048 bytes with no control bytes, userinfo,
query, or fragment. `ipfs://` requires a nonempty CID authority/path and no
query or fragment. `ar://` requires exactly one nonempty base64url transaction
identifier and no query or fragment. `https://` requires a lower-case ASCII
DNS name or globally routable IP literal, no explicit port, no userinfo, and
no fragment; localhost names and loopback, link-local, private, multicast,
documentation, and other reserved address ranges are forbidden. The exact
canonical URI bytes remain in the envelope and are hashed as before.

The pinned Stream source documents only its shared UTF-8/2,048-byte URI
validation and does not supply this public-network predicate. A bilateral
adapter MUST pass the URI through both predicates and MUST NOT rewrite a URI;
if a future Stream predicate conflicts, the adapter defers the export and
opens a convergence gate. The Museum contract does not perform DNS resolution
or claim that an HTTPS host is public from syntax alone. For every nonempty
HTTPS URI, the migration adapter MUST provide the signed
`MUSEUM_HTTPS_PUBLIC_NETWORK_ASSERTION_V1` record below and reject an expired
or mismatched assertion before submission. An HTTPS gateway MAY be a
retrieval convenience, but it is never the integrity anchor.

The canonical HTTPS assertion payload is RFC 8785 JCS JSON with exactly these
fields and no signature bytes:

```json
{
  "schema": "MUSEUM_HTTPS_PUBLIC_NETWORK_ASSERTION_V1",
  "uriHash": "0x<64 lowercase hex>",
  "hostHash": "0x<64 lowercase hex>",
  "resolverProfileId": "0x<64 lowercase hex>",
  "resolvedAddressSetHash": "0x<64 lowercase hex>",
  "observedAt": 0,
  "expiresAt": 0
}
```

Its subject is
`keccak256(abi.encode(0xe08003722c1e7c0465bdd4353706df75808fa767fca549cc020bd0c0081e59f4, uriHash))`.
The assertion record MUST set `uriHash == keccak256(bytes(targetURI))` and
`hostHash == keccak256(bytes(lowercaseAsciiHost(targetURI)))`. The resolver
MUST canonicalize the resolved address set as strictly increasing, duplicate-
free 20-byte address values and set
`resolvedAddressSetHash == keccak256(abi.encode(sortedUniqueAddresses))`.
It MUST set `expiresAt > observedAt` and `expiresAt` no later than the resolver
profile's maximum TTL. The signer is an authority-admitted public-network
resolver or registrar. Its signature scheme is
`MUSEUM_SIGNATURE_EIP712_HTTPS_PUBLIC_V1`, and its exact signed type string is:

```text
MuseumHTTPSPublicNetworkAssertion(bytes32 uriHash,bytes32 hostHash,bytes32 resolverProfileId,bytes32 resolvedAddressSetHash,uint64 observedAt,uint64 expiresAt)
```

The domain is the registry EIP-712 domain from §6.2; the signature digest is
the raw `0x1901 || domainSeparator || structHash` preimage. The envelope's
`signatureHash` commits to the exact signature bytes, while the canonical
payload commits to the assertion fields. An adapter MUST verify the signer,
payload/URI equality, resolver profile, globally routable address set, and
validity window; the contract stores the resulting record and does not pretend
to be a DNS resolver.

The chain MUST NOT contain donor contact details, full legal instruments,
appraisals, private signer information, private storage locations, credentials,
or sensitive security analysis. Public payloads may carry a redacted
statement, hash of the restricted instrument, non-sensitive custodian
reference, rights summary, and review status. Restricted records are
identified by hash and custodian reference only.

URI substitution, redaction changes, or a change in the restricted instrument
creates a new payload and revision. No URI or payload is mutated in place.

## 6. Authority, roles, and signatures

### 6.1 Authorization classes

For shared Stream families, the Museum uses the same class values as the
pinned Stream family registry:

| Value | Stream class | Museum use |
|---:|---|---|
| 1 | `AUTHORIZATION_CLASS_ARTIST_SIGNER` | artist/estate assertion |
| 2 | `AUTHORIZATION_CLASS_OWNER_SIGNER` | owner-lane assertion |
| 3 | `AUTHORIZATION_CLASS_CURATOR_SIGNER` | curatorial/program authority |
| 4 | `AUTHORIZATION_CLASS_INSTITUTION_SIGNER` | Museum/Safe institution authority |
| 5 | `AUTHORIZATION_CLASS_INDEPENDENT_ATTESTOR` | independent preservation/condition evidence |
| 6 | `AUTHORIZATION_CLASS_PRESERVATION_ADMIN` | preservation administration |
| 7 | `AUTHORIZATION_CLASS_METADATA_ADMIN` | schema/metadata administration |
| 8 | `AUTHORIZATION_CLASS_GLOBAL_ADMIN` | deployment/root administration |

Museum-native families additionally use:

| Value | Museum-only class |
|---:|---|
| 9 | `AUTH_MUSEUM_GOVERNANCE_EXECUTOR` |
| 10 | `AUTH_MUSEUM_REGISTRAR` |
| 11 | `AUTH_MUSEUM_PROGRAM_AUTHORITY` |
| 12 | `AUTH_MUSEUM_MIGRATION_ADMIN` |

Values 9–12 MUST NOT be sent as Stream record-family classes. A shared
Stream-compatible record is written to Stream using one of values 1–8 and the
same authority meaning. The class is event/summary metadata, not a field in
the `CollectionRecord` envelope.

Record families are closed-world. Every admitted `recordType` has a family,
schema, permitted class mask, and revision. Role grants are family-scoped;
global administration MUST NOT silently become artist, owner, rights, or
independent-attestor authority.

The initial deployment MUST grant the Museum Safe or an explicitly governed
authority provider rather than hard-coding the current signer list. The
current `networkmuseum.6529.eth` reference and named 3-of-5 signers are
historical operating context, not contract constants.

### 6.1.1 Global roles and class-selection domain

Family grants are valid only for record writes and always key the tuple
`(familyId, authorizationClass, account)`. External subject registration,
Stream mirror links, owner-record convergence, authority transitions, and
freeze controls use the following global roles instead; they MUST NOT accept
an omitted or caller-chosen family ID as a substitute:

| Role ID | Scope |
|---|---|
| `MUSEUM_GLOBAL_ROLE_REGISTRAR_V1` | Register already-profiled external subjects and set an admitted Stream mirror link. |
| `MUSEUM_GLOBAL_ROLE_MIGRATION_ADMIN_V1` | The same subject/link selectors while its exact global-role grant is enabled; the grant's `GlobalRoleGrantUpdated` enable/revoke pair is the migration window. It does not grant governance, title, rights, or independent-attestor authority and does not bypass `freezeWrites`. |
| `MUSEUM_GLOBAL_ROLE_GOVERNANCE_EXECUTOR_V1` | Convergence admission, authority transition execution, successor transition, and irreversible write freeze. |
| `MUSEUM_GLOBAL_ROLE_AUTHORITY_ADMIN_V1` | Grant/revoke global roles and queue or cancel an authority transition. |

The global authorization domain is exactly the tuple
`(selector, globalRoleId, account, authorityRevision)`, where `selector` is
the four-byte Solidity selector in the role-control table and `account` is
the `msg.sender` being checked. A direct global-role call MUST check the exact
selector allowlist, the enabled role grant for `msg.sender`, and the active
`authorityRevision`; no global selector accepts a `familyId` or `classMask`.
V1 has no relayed global-role calls. A future
relayed global action requires a new signature scheme that signs this exact
domain and selector; a record-family EIP-712 signature MUST NOT be reused for
it. Record writes retain the separate family/class domain and include the
selected `authorizationClass` and `authorityRevision` in their audit state.

The constructor grants the initial authority account the governance-executor
and authority-admin roles at revision 1. Thereafter `setGlobalRoleGrant` is
authority-admin controlled, append-only by role revision, and emits the exact
role ID, account, enabled state, and authority revision. A role grant cannot
alter a record-family class mask or retroactively authorize a prior record.

### 6.1.2 Authority, successor, and freeze transitions

V1 pins `AUTHORITY_TIMELOCK_SECONDS = 172800` (48 hours). `setAuthority`
does not immediately change `authority`; it queues one nonzero pending address
and an `eta = block.timestamp + AUTHORITY_TIMELOCK_SECONDS`. A second queue
requires `cancelAuthority` first. `executeAuthority` is allowed only at or
after `eta`, changes the active authority exactly once for that transition,
increments `authorityRevision`, and emits `RegistryAuthorityUpdated`. The
execution atomically grants the new authority the governance-executor and
authority-admin roles and disables those two transition roles for the old
authority; ordinary registrar/migration roles are not implicitly transferred.
queue, cancellation, and execution events expose the address, ETA, and
authority revision. `cancelAuthority` is permitted before execution and
clears the queue without changing active authority.

`setSuccessor` is a one-way transition. It is authorized only by the global
governance-executor role, requires `writesFrozen == true`, requires a nonzero
successor with the successor interface/code evidence required by §12, and
reverts if a successor is already set. It changes no authority or record
state, and emits `SuccessorSet` with the current authority revision.

`freezeWrites` is an immediate, one-way transition authorized only by the
global governance-executor role. It cancels any pending authority queue,
emitting `AuthorityChangeCancelled` for that pending address before
`WritesFrozen`,
blocks record, schema, profile, type, family-grant, global-role, convergence,
and authority-transition mutators, and leaves read selectors plus the single
post-freeze `setSuccessor` transition available. A second freeze reverts.
`WritesFrozen` records the active authority, successor, and authority
revision. No selector may bypass these guards through an alternate overload.
V1 is non-proxy and non-delegatecall; deployment behind an upgradeable proxy
or an implementation with an unguarded transition selector fails the
deployment gate.

### 6.2 Direct and relayed writes

Direct writes are authorized by `msg.sender` and the active family grant.
Relayed writes use EIP-712 and EIP-1271:

```solidity
EIP712Domain(
    name = "6529 Network Museum Registry",
    version = "1",
    chainId = block.chainid,
    verifyingContract = address(this)
)

MuseumRecordWrite(
    bytes32 recordHash,
    bytes32 recordType,
    bytes32 subjectId,
    bytes32 previousRecordHash,
    uint256 nonce,
    uint64 deadline
)

MuseumNonceRevocation(
    address signer,
    uint256 nonce,
    uint64 deadline
)
```

The exact EIP-712 type string is:

```text
MuseumRecordWrite(bytes32 recordHash,bytes32 recordType,bytes32 subjectId,bytes32 previousRecordHash,uint256 nonce,uint64 deadline)
```

The exact nonce-revocation type string is:

```text
MuseumNonceRevocation(address signer,uint256 nonce,uint64 deadline)
```

`MUSEUM_SIGNATURE_EIP712_RECORD_V1` names this relayed-authorization method;
it is an authorization-scheme ID outside the `CollectionRecord` envelope. It
MUST NOT be placed in `record.signatureScheme` for a V1 `bySig` write. The
digest is `keccak256(0x1901 || domainSeparator || structHash)`.

V1 pins the envelope/signature interaction to avoid a circular preimage:

* `recordMuseumRecord` and `recordMuseumRecordBatch` MAY carry a zero
  `signatureScheme` with the exact empty `signatureHash`, or a separately
  admitted nonzero envelope signature scheme with a valid required
  `signatureHash`; the contract treats a nonzero envelope scheme as a
  commitment and does not verify its external signature bytes.
* `recordMuseumRecordBySig` MUST use `record.signatureScheme == bytes32(0)`,
  `record.signatureHash.algorithm == 0`, empty `record.signatureHash.digest`,
  and `record.signatureHash.canonicalizationId == bytes32(0)`. The relayed
  EIP-712 signature is authorization metadata, not the envelope's
  `signatureHash`, so `recordHash` can be computed before signature creation.
* A zero envelope scheme with any nonempty or nonzero signature hash MUST
  revert. For direct and batch writes, either violation MUST revert with
  `InvalidEnvelopeSignatureFields`; for `bySig`, it MUST revert with
  `InvalidRelayedSignatureFields`. An unsupported nonzero envelope scheme MUST
  revert with the same path-specific error unless its schema/authority
  admission explicitly admits it.

The signer address is explicit in the ABI, is included in the record-write or
nonce-revocation EIP-712 struct, and is checked for the relevant authority.
EOA signatures use exact ECDSA recovery; contract signers use ERC-1271
`isValidSignature(bytes32,bytes)`.

Both ERC-1271 paths are `nonReentrant` and reserve the signer/nonce lane while
the external `isValidSignature` call is in flight. After the callback returns,
the registry MUST re-read the lane head and the signer nonce/revocation state;
any change from the pre-call values MUST revert with
`LaneHeadChangedDuringSignature` or `NonceStateChangedDuringSignature`.
The callback cannot call any registry mutator through the reentrancy guard.
Only after these checks does the registry consume the nonce and append the
record or persist the revocation.

Nonces are unordered and scoped to the signer. A used or revoked nonce cannot
be reused. Deadlines are inclusive: `block.timestamp <= deadline` is
required. The signer MAY revoke a nonce directly or through a valid
revocation signature. Authority rotation does not rewrite old records; the
record retains the class, signer, and role/provider revision observed at
write time.

The envelope's `signatureHash` is still only a commitment, as in Stream. In a
V1 relayed write, the relayed authorization signature MUST NOT be placed in
that field because doing so would make the `recordHash`/signature preimage
circular. It is checked for permission and is represented by the signer,
nonce, deadline, and authorization event metadata instead. Direct writes may
carry a separately admitted envelope signature commitment, but the contract
does not verify its external signature bytes.

`revokeNonceBySig` uses the same EIP-712 domain as record writes. Its digest is
`keccak256(0x1901 || domainSeparator || structHash)`, with
`structHash = keccak256(abi.encode(
keccak256("MuseumNonceRevocation(address signer,uint256 nonce,uint64 deadline)"),
signer, nonce, deadline))`. A valid revocation persists the signer, nonce,
inclusive deadline, and `keccak256(signature)` commitment in state and emits
them in `NonceRevocationRecorded` plus the relayer and authority revision. The persisted
deadline is an audit fact even after it has elapsed; it does not automatically
unrevoke or delete the nonce. A direct revocation persists zero deadline and
zero signature commitment. The revocation entry is immutable once written.

## 7. Proposed ABI

The implementation MUST expose the following public surface. Names and
parameter order are normative for V1; return structs may be ABI-generated
from these definitions.

```solidity
interface INetworkMuseumRegistryV1 {
    struct HashRef {
        uint16 algorithm;
        bytes digest;
        bytes32 canonicalizationId;
    }

    struct CollectionRecord {
        bytes32 recordType;
        bytes32 subjectId;
        HashRef contentHash;
        string uri;
        bytes32 schemaId;
        bytes32 signatureScheme;
        HashRef signatureHash;
        uint64 effectiveAt;
    }

    struct RecordInput {
        CollectionRecord record;
        bytes32 previousRecordHash;
        uint8 payloadMode;
        bytes32 supersedesRecordHash;
        bytes payload;
    }

    struct RecordSummary {
        bytes32 recordType;
        bytes32 subjectId;
        bytes32 recordHash;
        bytes32 previousRecordHash;
        bytes32 chainHash;
        uint64 revision;
        uint64 effectiveAt;
        uint64 recordedAt;
        uint64 recordedBlock;
        address recorder;
        address authorizedSigner;
        uint256 authorizationNonce;
        uint64 authorizationDeadline;
        bytes32 authorizationSignatureScheme;
        bytes32 authorizationSignatureCommitment;
        uint8 authorizationClass;
        uint8 payloadMode;
        bytes32 supersedesRecordHash;
        uint32 payloadLength;
        uint64 authorityRevision;
    }

    struct ExternalAsset {
        bytes32 subjectId;
        bytes32 assetProfileId;
        bytes32 canonicalAssetIdHash;
        string canonicalAssetId;
        uint64 registeredAt;
        address registrar;
    }

    struct AssetProfile {
        bool admitted;
        bytes32 schemaId;
        bytes32 documentHash;
        string uri;
        address canonicalizer;
        uint8 canonicalizerMode;
        bytes32 canonicalizerCodeHash;
        bytes32 canonicalizerImplementationHash;
        bytes32 canonicalizerVersionId;
        uint64 revision;
    }

    struct StreamMirrorLink {
        address streamCore;
        address ownerRecordModule;
        uint256 collectionId;
        uint256 tokenId;
        bytes32 streamSubjectId;
        bytes32 ownerRecordHash;
        bytes32 ownerRecordHashDomain;
        bytes32 ownerRecordHashVectorId;
        uint64 revision;
    }

    struct NonceRevocation {
        bool revoked;
        uint64 deadline;
        bytes32 signatureCommitment;
        address actor;
        uint64 nonceRevision;
        uint64 authorityRevision;
    }

    struct StreamOwnerRecordInterface {
        bool admitted;
        address interfaceModule;
        bytes32 ownerRecordHashDomain;
        bytes32 ownerRecordHashVectorId;
        bytes32 evidenceHash;
        uint64 revision;
    }

    struct GlobalRoleGrant {
        bool enabled;
        uint64 revision;
        uint64 authorityRevision;
    }

    function isNetworkMuseumRegistry() external pure returns (bool);
    function registryVersion() external pure returns (bytes32);
    function streamCompatibilityCommit() external pure returns (bytes32);
    function moduleSupersedes() external view returns (address);
    function authority() external view returns (address);
    function successor() external view returns (address);
    function writesFrozen() external view returns (bool);
    function pendingAuthority() external view returns (address newAuthority, uint64 eta,
        uint64 authorityRevision);

    function externalAssetSubjectId(bytes32 assetProfileId, string calldata canonicalAssetId)
        external pure returns (bytes32);
    function registerExternalAsset(bytes32 assetProfileId, string calldata canonicalAssetId,
        bytes32 expectedSubjectId)
        external returns (bytes32 subjectId);
    function externalAsset(bytes32 subjectId) external view returns (ExternalAsset memory);

    function admitAssetProfile(bytes32 profileId, bytes32 schemaId, bytes32 documentHash,
        string calldata uri, address canonicalizer, uint8 canonicalizerMode,
        bytes32 canonicalizerCodeHash, bytes32 canonicalizerImplementationHash,
        bytes32 canonicalizerVersionId)
        external;
    function assetProfile(bytes32 profileId)
        external view returns (AssetProfile memory);
    function admitSchema(bytes32 schemaId, bytes32 documentHash, string calldata uri,
        bool payloadRequired) external;
    function schema(bytes32 schemaId)
        external view returns (bool admitted, bytes32 documentHash, string memory uri,
            bool payloadRequired, uint64 revision);
    function admitRecordType(bytes32 recordType, bytes32 familyId, bytes32 schemaId, uint16 classMask)
        external;
    function recordTypePolicy(bytes32 recordType)
        external view returns (bytes32 familyId, bytes32 schemaId, uint16 classMask, bool admitted, uint64 revision);
    function setRecordFamilyGrant(bytes32 familyId, uint8 authorizationClass, address account, bool enabled)
        external;
    function recordFamilyGrant(bytes32 familyId, uint8 authorizationClass, address account)
        external view returns (bool enabled, uint64 revision);
    function setAuthority(address newAuthority) external;
    function executeAuthority() external;
    function cancelAuthority() external;
    function setGlobalRoleGrant(bytes32 globalRoleId, address account, bool enabled) external;
    function globalRoleGrant(bytes32 globalRoleId, address account)
        external view returns (GlobalRoleGrant memory);
    function admitStreamOwnerRecordInterface(address interfaceModule,
        bytes32 ownerRecordHashDomain, bytes32 ownerRecordHashVectorId, bytes32 evidenceHash)
        external;
    function streamOwnerRecordInterface()
        external view returns (StreamOwnerRecordInterface memory);

    function recordMuseumRecord(CollectionRecord calldata record, bytes32 previousRecordHash,
        uint8 payloadMode, bytes32 supersedesRecordHash)
        external returns (bytes32 recordHash);
    function recordMuseumRecordWithPayload(
        CollectionRecord calldata record,
        bytes32 previousRecordHash,
        uint8 payloadMode,
        bytes32 supersedesRecordHash,
        bytes calldata payload
    ) external returns (bytes32 recordHash);
    function recordMuseumRecordBySig(
        CollectionRecord calldata record,
        bytes32 previousRecordHash,
        bytes32 signedRecordHash,
        bytes32 signedPreviousRecordHash,
        address signer,
        uint256 nonce,
        uint64 deadline,
        bytes calldata signature,
        uint8 payloadMode,
        bytes32 supersedesRecordHash,
        bytes calldata payload
    ) external returns (bytes32 recordHash);
    function recordMuseumRecordBatch(RecordInput[] calldata inputs, bytes32 batchId)
        external returns (bytes32[] memory recordHashes);

    function deriveMuseumRecordHash(CollectionRecord calldata record, uint8 payloadMode,
        bytes32 supersedesRecordHash)
        external view returns (bytes32 recordHash);
    function latestRecordHash(bytes32 recordType, bytes32 subjectId)
        external view returns (bytes32);
    function recordChainHead(bytes32 recordType, bytes32 subjectId)
        external view returns (bytes32 head, uint64 revision, bytes32 chainHash);
    function recordSummary(bytes32 recordHash) external view returns (RecordSummary memory);
    function record(bytes32 recordHash) external view returns (CollectionRecord memory);
    function payload(bytes32 recordHash) external view returns (bytes memory);

    function setStreamMirrorLink(bytes32 subjectId, address streamCore, address ownerRecordModule,
        uint256 collectionId, uint256 tokenId, bytes32 streamSubjectId, bytes32 ownerRecordHash,
        bytes32 ownerRecordHashDomain, bytes32 ownerRecordHashVectorId) external;
    function streamMirrorLink(bytes32 subjectId)
        external view returns (StreamMirrorLink memory);

    function revokeNonce(uint256 nonce) external;
    function revokeNonces(uint256[] calldata nonces) external;
    function revokeNonceBySig(address signer, uint256 nonce, uint64 deadline, bytes calldata signature)
        external;
    function nonceRevocation(address signer, uint256 nonce)
        external view returns (NonceRevocation memory);
    function setSuccessor(address newSuccessor) external;
    function freezeWrites() external;
}
```

`recordMuseumRecordBySig` MUST perform these checks before accepting the
signature:

1. Compute `derivedRecordHash = deriveMuseumRecordHash(
   record, payloadMode, supersedesRecordHash)`.
2. Require `derivedRecordHash == signedRecordHash`.
3. Require `signedPreviousRecordHash == previousRecordHash`.
4. Require `previousRecordHash` equals the current lane head (zero for the
   first revision).
5. Apply the same explicit `payloadMode`/`INLINE` profile, byte-cap,
   zero-payload, URI, and
   `PayloadDigestMismatch`/`InlinePayloadProfileMismatch` checks required by
   §5.2 for `recordMuseumRecordWithPayload` to the `payload` argument. A
   relayer MUST NOT be able to attach bytes that do not match the signed
   envelope.
6. Construct the EIP-712 struct using the exact `signedRecordHash`,
   `record.recordType`, `record.subjectId`, exact
   `signedPreviousRecordHash`, `nonce`, and `deadline` arguments.
   `payloadMode` and `supersedesRecordHash` are not duplicate EIP-712 fields;
   they are cryptographically covered by the recomputed `signedRecordHash`
   and therefore by the signed `recordHash` field.
7. Verify that digest for `signer`, re-read the lane head and signer nonce
   state, and revert if either changed during an ERC-1271 callback. Only then
   consume the signer-scoped nonce and append the record.

The contract MUST NOT derive a digest from one record/predecessor pair while
storing another. `SignedRecordHashMismatch` and
`SignedPreviousRecordHashMismatch` are distinct failure cases.

`recordMuseumRecordBatch` is all-or-nothing, has a hard maximum of
`MAX_BATCH_RECORDS` records, and advances each lane in input order. The sum of
`INLINE` payload bytes MUST obey `MAX_BATCH_INLINE_PAYLOAD_BYTES` and each
record MUST obey `MAX_INLINE_PAYLOAD_BYTES`. Each `RecordInput` supplies its
explicit `payloadMode` and `supersedesRecordHash`; neither is inferred from
the payload bytes. `batchId` is an audit label and
MUST be emitted; it is not part of any record hash. A retry after a reorg is
permitted once the caller re-reads state and resubmits only records not
present in the surviving chain. A record already present is handled by the
global duplicate semantics above, not by silently skipping it in a batch.
Since the batch is all-or-nothing, any already-present `recordHash` reverts the
whole batch; a reorg-retry batch MUST exclude every record hash already present
in the surviving chain.

### 7.0 Selector and role controls

The following selectors and caller classes are normative. A selector is
listed both as its Solidity signature and as its first four bytes so an
implementation cannot accidentally authorize an overload:

| Selector | Caller requirement | Additional anti-pollution rule |
|---|---|---|
| `0x73c0a0b4` `registerExternalAsset(bytes32,string,bytes32)` | Enabled `MUSEUM_GLOBAL_ROLE_REGISTRAR_V1` or `MUSEUM_GLOBAL_ROLE_MIGRATION_ADMIN_V1` grant for `msg.sender`; never an open/public or family-grant caller | `assetProfileId` MUST be admitted; the profile canonicalizer/runtime checks MUST pass; `expectedSubjectId` MUST equal the deterministic subject; an existing subject never overwrites or aliases another asset. |
| `0x49c44b5c` `setStreamMirrorLink(bytes32,address,address,uint256,uint256,bytes32,bytes32,bytes32,bytes32)` | Enabled global registrar or migration-admin grant, or enabled `MUSEUM_GLOBAL_ROLE_GOVERNANCE_EXECUTOR_V1` grant during the convergence-gate action | The Museum subject MUST already exist; the link is write-once; all Stream/module/token/hash-domain/vector fields are committed together; a duplicate or altered link reverts. |
| `0x75c75961` `admitStreamOwnerRecordInterface(address,bytes32,bytes32,bytes32)` | Active authority plus enabled global governance-executor grant | The evidence hash, exact owner-record domain/vector, interface module, and pinned Stream commit are recorded before any mirror link can be set. |
| `recordMuseumRecord(CollectionRecord,bytes32,uint8,bytes32)` and the payload/by-signature/batch write selectors | The active family grant for the record's admitted `(familyId, authorizationClass)`; `bySig` additionally requires a valid signer | Subject pollution is prevented by record-type policy: external-asset identity records require a previously registered subject, and every other subject namespace requires an admitted schema/profile. |
| `0xab6627c3` `setGlobalRoleGrant(bytes32,address,bool)` | Enabled `MUSEUM_GLOBAL_ROLE_AUTHORITY_ADMIN_V1` grant and active authority | The role ID is closed-world, the selector allowlist is fixed, and each change increments the role revision and records the authority revision. |
| `0x7a9e5e4b` `setAuthority(address)` | Enabled global authority-admin grant and active authority | Queues a 48-hour authority transition; it does not mutate active authority inline. |
| `0xc9dc7d0d` `executeAuthority()` / `0xf0edf065` `cancelAuthority()` | Enabled global governance-executor for execute; enabled global authority-admin for cancel | Execute requires the stored ETA; cancel clears only the pending transition. Both are blocked after freeze. |
| `0x10e5bff8` `setSuccessor(address)` | Enabled global governance-executor grant | Requires frozen writes, a nonzero successor, no prior successor, and successor code/interface evidence; one-way. |
| `0x05d53fba` `freezeWrites()` | Enabled global governance-executor grant | Immediate and one-way; cancels pending authority and blocks all mutators except post-freeze `setSuccessor`. |
| `admitAssetProfile`, `admitSchema`, `admitRecordType`, `setRecordFamilyGrant` | Active authority plus their explicitly admitted metadata/admin scope; never an unqualified family grant | Admission is append-only; a new document or policy revision gets a new revision and cannot silently broaden a prior grant. |

The canonical asset string is profile output, not caller interpretation. The
admitted profile MUST name a governance-approved canonicalizer, a
`canonicalizerMode` (`0 = IMMUTABLE_RUNTIME`, `1 = EIP1967_PROXY`), its exact
runtime `canonicalizerCodeHash`, its `canonicalizerVersionId`, and, for mode 1,
its exact `canonicalizerImplementationHash`. Registration MUST enforce
`extcodehash(canonicalizer) == canonicalizerCodeHash`, and the canonicalizer's
`versionId(profileId)` MUST equal the stored version ID. Mode 0 MUST have a
zero implementation hash and the adapter's `implementationCodeHash(profileId)`
MUST equal the runtime hash. Mode 1 MUST read the standard EIP-1967
implementation slot `bytes32(uint256(keccak256("eip1967.proxy.implementation")) - 1)`,
require the implementation's `extcodehash` and the
adapter-reported implementation hash to equal the stored implementation hash,
and reject any other proxy shape. `admitAssetProfile` MUST perform these same
code-hash, implementation-slot, and version checks before storing the profile;
these checks also occur on every registration;
changing runtime code, implementation code, or version is an
`AssetProfileAlreadyAdmitted` violation under the same profile ID and requires
a new profile ID and document. Registration calls the canonicalizer
in a read-only call and MUST require byte-for-byte equality between its
returned string and the supplied string. The string MUST be UTF-8 without leading/trailing whitespace or
controls, and the exact profile document hash MUST pin normalization, case,
decimal, Unicode, and collision rules. For
`MUSEUM_ASSET_PROFILE_CAIP19_V1`, the supplied string MUST use lowercase EVM
addresses, decimal chain IDs without leading zeroes, and canonical
nonnegative decimal token IDs. EIP-55 display strings, percent encoding,
Unicode lookalikes, alternate separators, aliases, and leading-zero token IDs
are rejected. `externalAssetSubjectId` hashes the exact admitted canonical
bytes. The caller supplies `expectedSubjectId` so a relayer or front-runner
cannot substitute a different result; only the authorized role can create the
first mapping. A same-subject/same-string retry reverts with
`ExternalAssetAlreadyRegistered`, while a same-subject/different profile or
string reverts with `SubjectIdCollision`.

`setStreamMirrorLink` is also not an untrusted assertion channel. It requires
an existing Museum subject, an admitted `streamOwnerRecordInterface`, a
converged/approved owner-record evidence vector, nonzero module/core
addresses, a nonzero token ID where the source namespace requires one, and a
nonzero owner-record hash/domain/vector ID. The supplied module, domain, and
vector MUST equal the admitted interface values, and the evidence hash for
the interface MUST be anchored to the pinned Stream compatibility commit.
The link is immutable and one-per-subject in V1; the contract MUST NOT
silently replace it after a source transfer or owner-record revision. A later
source revision is a new Museum evidence record, not a mutation of this link.

### 7.1 Required errors

The V1 implementation MUST define and use these custom errors (arguments are
normative):

```solidity
error InvalidAssetProfile(bytes32 profileId);
error AssetProfileAlreadyAdmitted(bytes32 profileId);
error InvalidCanonicalAssetId(bytes32 profileId);
error InvalidCanonicalizer(bytes32 profileId, address canonicalizer);
error InvalidCanonicalizerCodeHash(bytes32 profileId, bytes32 expected, bytes32 actual);
error InvalidCanonicalizerImplementation(bytes32 profileId, bytes32 expected, bytes32 actual);
error CanonicalizerVersionMismatch(bytes32 profileId, bytes32 expected, bytes32 actual);
error SubjectIdMismatch(bytes32 expected, bytes32 derived);
error ExternalAssetAlreadyRegistered(bytes32 subjectId);
error SubjectIdCollision(bytes32 subjectId);
error SchemaNotAdmitted(bytes32 schemaId);
error SchemaAlreadyAdmitted(bytes32 schemaId);
error InvalidSchemaDocument(bytes32 schemaId, bytes32 suppliedHash);
error RecordTypeNotAdmitted(bytes32 recordType);
error RecordTypeAlreadyAdmitted(bytes32 recordType);
error InvalidClassMask(bytes32 familyId, uint16 supplied);
error InvalidMuseumRecord(bytes32 recordType, bytes32 subjectId, bytes32 schemaId);
error InvalidMuseumHashRef(uint16 algorithm, uint256 digestLength);
error URITooLarge(uint256 actual, uint256 maximum);
error InvalidUTF8URI();
error InvalidURI(bytes32 uriHash);
error InvalidPayloadMode(uint8 payloadMode);
error PayloadModeMismatch(uint8 payloadMode, uint256 payloadLength);
error PayloadRequired(bytes32 schemaId);
error PayloadTooLarge(uint256 actual, uint256 maximum);
error PayloadDigestMismatch(bytes32 expected, bytes32 actual);
error InlinePayloadProfileMismatch(uint16 algorithm, bytes32 canonicalizationId);
error InvalidEnvelopeSignatureFields(bytes32 signatureScheme, uint16 algorithm,
    uint256 digestLength, bytes32 canonicalizationId);
error InvalidRelayedSignatureFields(bytes32 signatureScheme, uint16 algorithm,
    uint256 digestLength, bytes32 canonicalizationId);
error RecordAlreadyExists(bytes32 recordHash);
error PreviousRecordMismatch(bytes32 expected, bytes32 actual);
error SignedRecordHashMismatch(bytes32 derived, bytes32 signed);
error SignedPreviousRecordHashMismatch(bytes32 supplied, bytes32 signed);
error SupersessionTargetMissing(bytes32 supersedesRecordHash);
error SupersessionLaneMismatch(bytes32 supersedesRecordHash, bytes32 recordType, bytes32 subjectId);
error SupersessionNotOlder(bytes32 supersedesRecordHash, uint64 targetRevision, uint64 newRevision);
error RecordFamilyUnauthorized(address actor, bytes32 recordType, bytes32 familyId, uint16 classMask);
error InvalidAuthority(address signer, uint8 authorizationClass);
error InvalidSignature(address signer);
error GlobalRoleUnauthorized(bytes32 globalRoleId, address caller, bytes4 selector);
error InvalidAuthorityTransition(address newAuthority);
error AuthorityChangePending(address pendingAuthority, uint64 eta);
error NoPendingAuthority();
error AuthorityChangeNotReady(uint64 eta, uint64 currentTime);
error WritesNotFrozen();
error WritesAlreadyFrozen();
error LaneHeadChangedDuringSignature(bytes32 expected, bytes32 actual);
error NonceStateChangedDuringSignature(address signer, uint256 nonce);
error SignatureExpired(uint64 deadline, uint64 currentTime);
error NonceUsed(address signer, uint256 nonce);
error NonceRevoked(address signer, uint256 nonce);
error BatchTooLarge(uint256 actual, uint256 maximum);
error BatchIdAlreadyUsed(bytes32 batchId);
error WritesFrozen();
error InvalidSuccessor(address successor);
error SuccessorAlreadySet(address successor);
error InvalidStreamMirrorLink(bytes32 subjectId, address streamCore, address ownerRecordModule,
    uint256 collectionId, uint256 tokenId);
error StreamMirrorLinkAlreadySet(bytes32 subjectId);
error OwnerRecordConvergenceRequired(bytes32 ownerRecordHashVectorId);
error InvalidRoleProvider(address provider);
error FunctionUnauthorized(address caller, bytes4 selector);
```

The Museum registry MUST NOT declare an `InvalidHashRef` error. The name
`InvalidMuseumHashRef` is intentionally distinct so its selector cannot be
confused with a pinned Stream adapter error. The Stream adapter MUST recognize
the pinned Stream errors:
`InvalidCoreContract`, `InvalidAdminContract`, `InvalidRecordFamilyRegistry`,
`FunctionAdminUnauthorized`, `MetadataMutationPaused`,
`CollectionDoesNotExist`, `InvalidCollectionRecord`, `InvalidHashRef`,
`PreservationURITooLarge`, and `CollectionRecordAlreadyExists`.

### 7.2 Required events

```solidity
event MuseumRecordRecorded(
    bytes32 indexed recordType,
    bytes32 indexed subjectId,
    bytes32 indexed recordHash,
    CollectionRecord record,
    bytes32 previousRecordHash,
    bytes32 chainHash,
    uint64 revision,
    address recorder,
    address authorizedSigner,
    uint256 authorizationNonce,
    uint64 authorizationDeadline,
    bytes32 authorizationSignatureScheme,
    bytes32 authorizationSignatureCommitment,
    uint8 authorizationClass,
    uint8 payloadMode,
    bytes32 supersedesRecordHash,
    uint32 payloadLength,
    uint64 authorityRevision
);
event MuseumRecordBatchRecorded(bytes32 indexed batchId, uint256 count, bytes32 batchCommitment);
event ExternalAssetRegistered(bytes32 indexed subjectId, bytes32 indexed assetProfileId,
    bytes32 canonicalAssetIdHash, string canonicalAssetId, address indexed registrar);
event AssetProfileAdmitted(bytes32 indexed profileId, bytes32 schemaId, bytes32 documentHash,
    string uri, address canonicalizer, uint8 canonicalizerMode, bytes32 canonicalizerCodeHash,
    bytes32 canonicalizerImplementationHash, bytes32 canonicalizerVersionId,
    uint64 revision, address authority);
event SchemaAdmitted(bytes32 indexed schemaId, bytes32 documentHash, string uri,
    uint64 revision, address authority);
event RecordTypeAdmitted(bytes32 indexed recordType, bytes32 indexed familyId, bytes32 indexed schemaId,
    uint16 classMask, uint64 revision, address authority);
event RecordFamilyGrantUpdated(bytes32 indexed familyId, uint8 indexed authorizationClass,
    address indexed account, bool enabled, uint64 revision, address authority);
event StreamMirrorLinkSet(bytes32 indexed subjectId, address indexed streamCore,
    address indexed ownerRecordModule, uint256 collectionId, uint256 tokenId,
    bytes32 streamSubjectId, bytes32 ownerRecordHash, bytes32 ownerRecordHashDomain,
    bytes32 ownerRecordHashVectorId, uint64 revision, address authority);
event NonceRevocationRecorded(address indexed signer, uint256 indexed nonce, uint64 deadline,
    bytes32 signatureCommitment, address actor, uint64 nonceRevision,
    uint64 authorityRevision);
event GlobalRoleGrantUpdated(bytes32 indexed globalRoleId, address indexed account,
    bool enabled, uint64 roleRevision, uint64 authorityRevision, address authority);
event AuthorityChangeQueued(address indexed pendingAuthority, uint64 eta,
    uint64 authorityRevision, address authority);
event AuthorityChangeCancelled(address indexed pendingAuthority, uint64 authorityRevision,
    address authority);
event RegistryAuthorityUpdated(address indexed oldAuthority, address indexed newAuthority,
    uint64 authorityRevision);
event SuccessorSet(address indexed successor, address authority, uint64 authorityRevision);
event WritesFrozen(address indexed authority, address indexed successor, uint64 authorityRevision);
```

The full envelope is emitted in `MuseumRecordRecorded`, but the state views
remain authoritative after event pruning or an RPC provider's log limits.

### 7.2.1 Normative state/audit reconstruction

The following table is normative. A state-only auditor MUST obtain the state
column; the event column is a redundant audit/index surface and MUST carry the
same value. A missing event never justifies omitting the state value.

| Audit fact | State source | Event source | Direct-write value | Relayed-write value |
|---|---|---|---|---|
| Envelope, predecessor, chain, revision, mode, supersession | `record(recordHash)` + `recordSummary(recordHash)` | `MuseumRecordRecorded` | Supplied envelope and explicit mode/supersession | Same signed/recomputed values |
| Recorder | `RecordSummary.recorder` | `MuseumRecordRecorded.recorder` | `msg.sender` | Relayer `msg.sender` |
| Authorized signer | `RecordSummary.authorizedSigner` | `MuseumRecordRecorded.authorizedSigner` | `address(0)` | Explicit `signer` |
| Authorization nonce | `RecordSummary.authorizationNonce` | `MuseumRecordRecorded.authorizationNonce` | `0` | Supplied signer-scoped nonce |
| Authorization deadline | `RecordSummary.authorizationDeadline` | `MuseumRecordRecorded.authorizationDeadline` | `0` | Supplied inclusive deadline |
| Authorization signature scheme | `RecordSummary.authorizationSignatureScheme` | `MuseumRecordRecorded.authorizationSignatureScheme` | `bytes32(0)` | `MUSEUM_SIGNATURE_EIP712_RECORD_V1` |
| Authorization signature commitment | `RecordSummary.authorizationSignatureCommitment` | `MuseumRecordRecorded.authorizationSignatureCommitment` | `bytes32(0)` | `keccak256(signature)`; signature bytes are never required for state reconstruction |
| Selected class and authority revision | `RecordSummary.authorizationClass`, `authorityRevision` | Same event fields | Direct caller's active family grant and current revision | Signer's active family grant and current revision |
| Inline payload | `payload(recordHash)` | `MuseumRecordRecorded.payloadMode/payloadLength` plus the state view | Exact bytes for `INLINE`, otherwise empty | Same signed envelope bytes |
| Nonce revocation | `nonceRevocation(signer,nonce)` | `NonceRevocationRecorded` | Deadline `0`, commitment `0`, actor `msg.sender`, `nonceRevision=1` | Supplied deadline, `keccak256(signature)`, relayer actor, `nonceRevision=1` |
| Revocation authority context | `NonceRevocation.authorityRevision` | `NonceRevocationRecorded.authorityRevision` | Current authority revision | Current authority revision |

`authorizationNonce` and `authorizationDeadline` are not part of
`recordHash`; the signed `recordHash` remains the envelope identity. They are
durable sidecar authorization facts and MUST be populated before the write
becomes visible. `authorizationSignatureScheme` is the outside-the-envelope
scheme ID; it MUST NOT be confused with `record.signatureScheme`. The
`nonceRevision` in a revocation is the revision of that signer/nonce lane,
while `authorityRevision` is the registry authority revision; neither may be
reused for the other.

## 8. Migration procedure

### 8.0 `MUSEUM_RELEASE_MANIFEST_V1`

The release manifest is a canonical JSON payload whose `root` is excluded
from the body hash and is recomputed from the ordered record entries. Its
schema is exactly this object shape (RFC 8785 JCS is applied after the
ordinary JSON object is constructed):

```json
{
  "schema": "MUSEUM_RELEASE_MANIFEST_V1",
  "sourceCommit": "<40 lowercase hexadecimal characters>",
  "streamCompatibilityCommit": "<40 lowercase hexadecimal characters>",
  "generator": "<nonempty ASCII generator/version>",
  "records": [
    {
      "sourceOrdinal": 1,
      "path": "<repository-relative POSIX path>",
      "recordHash": "0x<64 lowercase hexadecimal characters>",
      "payloadMode": "NONE|INLINE|CONTENT_ADDRESSED",
      "payloadBytesHash": "0x<64 lowercase hexadecimal characters>"
    }
  ],
  "root": "0x<64 lowercase hexadecimal characters>"
}
```

`sourceCommit` and `streamCompatibilityCommit` are Git SHA-1 values encoded
as `bytes32` by right-aligning the 20 decoded bytes and left-padding with
zeroes. `sourceOrdinal` is a positive `uint64`; records MUST be strictly
increasing by ordinal, and each path MUST be unique, POSIX-normalized, and
inside the governed-file set. `payloadBytesHash` is `keccak256` of the exact
inline bytes for `INLINE`, and `keccak256(bytes(""))` for `NONE` and
`CONTENT_ADDRESSED`; the latter's integrity anchor remains the record's
committed `HashRef` and URI. The JSON `payloadMode` strings map to the ABI
values `0`, `1`, and `2`.

For each record, define:

```solidity
bytes32 entryHash = keccak256(abi.encode(
    0xa524091b411df027ff64e4f8d590d93cf7e2e7658f6a5a8f623abfb4e01671ef,
    uint64(sourceOrdinal),
    keccak256(bytes(path)),
    recordHash,
    uint8(payloadMode),
    payloadBytesHash
));
```

Let `entryHashes` be the `bytes32[]` of entry hashes in strictly increasing
`sourceOrdinal` order. The manifest root is the `abi.encode` tuple with
argument types `(bytes32,bytes32,bytes32,bytes32,uint64,bytes32[])`:

```solidity
bytes32 root = keccak256(abi.encode(
    0xe615064b79fb81a121afe1ad24d886aa86536f320be540a31023f43bbe935b64,
    sourceCommitBytes32,
    streamCompatibilityCommitBytes32,
    keccak256(bytes(generator)),
    uint64(records.length),
    entryHashes // encoded as bytes32[] in this exact order
));
```

The final JSON `root` MUST equal this value. The body hash is
`keccak256(RFC8785_JCS(bodyWithoutRoot))`; the body hash and root are both
stored in the manifest record or release evidence. No implementation may
sort entries by path or record hash, omit the source ordinal, or derive a
root from event order. This binds every migrated record to its source
ordinal, source path, explicit payload mode, exact inline bytes (when
present), record hash, generator, and both source commits.

### Phase 0 — freeze and pin

1. Select a repository commit and freeze the governed-file set.
2. Generate `record-manifest.json` with repository-relative POSIX paths,
   LF-normalized SHA-256, RFC 8785 JSON bytes, and Keccak `HashRef`s.
3. Record the source commit, Stream compatibility commit, generator version,
   schema-document hashes, and manifest root in one
   `MUSEUM_RELEASE_MANIFEST_V1` payload.
4. Do not include restricted files in the public manifest. A restricted
   commitment is a separate hash/reference with a non-sensitive custodian.

### Phase 1 — schema and authority admission

1. Admit the canonicalization profile, CAIP-19 profile, Museum schemas, exact
   shared Stream IDs, and their document hashes.
2. Admit record families and class masks. Shared Stream record types use the
   Stream family semantics; Museum-native types use Museum-only families.
3. Grant the Museum Safe/authority provider and migration operator only the
   required family classes. No migration operator gets artist, owner, rights,
   or independent-attestor authority by implication.
4. Record the authority contract/code hash and revision in the deployment
   manifest. Rotate providers through append-only events.

### Phase 2 — deploy V1

The constructor parameters are `authority`, the immutable Stream compatibility
commit (`bytes32`), `moduleSupersedes` (zero for the first deployment), and a
zero successor. Deployment MUST verify that the
authority/provider has the expected interface and that no successor is set.
The registry is not a proxy. A later implementation is a new immutable
contract with `streamCompatibilityCommit` and `moduleSupersedes` metadata.

### Phase 3 — register subjects and links

1. Register each external asset's exact canonical CAIP identity.
2. Record `MUSEUM_EXTERNAL_ASSET_IDENTITY_V1` only as identity evidence; do
   not mark custody, title, or accession in that record.
3. For a Stream-native work, set a `StreamMirrorLink` only after the §2.1
   convergence gate. It MUST contain the verified Stream Core address,
   owner-record module, collection ID, token ID, Stream subject ID, owner
   record hash, hash domain, and vector ID. A mirror link is a
   cross-reference, not a second artwork identity.

### Phase 4 — migrate records in lane order

For every lane, order records by source revision/effective date and use a
deterministic tie-breaker of `(source ordinal, recordHash)`. Migrate in this
order:

1. governance decisions and policy;
2. approved collections and accession programs;
3. program outcomes, preserving selection status separately from acquisition;
4. accession lots and individual object records;
5. work description, rights, condition, preservation, dossier, and export
   commitments;
6. custody observations and title bindings after their evidence is available.

The tool MUST compare the post-write state to the source manifest, verify
every `recordHash`, chain head, revision, inline payload, and schema document,
then wait for the target chain's declared finality before publishing the
migration checkpoint. It MUST retain the source transaction hash and target
block/transaction evidence off-chain; a contract cannot know its own current
transaction hash.

### Phase 5 — reconstruct and publish

An independent state-only client MUST regenerate the public index, accession
packet, object dossier, PREMIS/LIDO exports, and BagIt/OCFL manifests from
record state plus content-addressed bytes. Event replay is an additional
check, not the only path. The release is not complete until a third party can
reproduce the hashes without GitHub, the original operator, or a marketplace.

## 9. Casey donation records

The current Casey working plan proposes one accession lot and seven object
IDs, but it explicitly says that contract addresses, token IDs, title evidence,
transfer history, custody, rights, and review authority are not verified.
The migration MUST preserve that uncertainty.

| Proposed stable ID | Label from the working plan |
|---|---|
| `6529NM.2026.001.1` | `CENTURY #31` |
| `6529NM.2026.001.2` | `CENTURY #724` |
| `6529NM.2026.001.3` | `CENTURY #401` |
| `6529NM.2026.001.4` | `Pre-Process #63` |
| `6529NM.2026.001.5` | `Phototaxis #308` |
| `6529NM.2026.001.6` | `923 EMPTY ROOMS #713` |
| `6529NM.2026.001.7` | `Ex Nihilo (Cosmos) #248` |

Until verification is complete, the migration MAY carry the working plan as
one `MUSEUM_RESEARCH_NOTE_V1` record with explicit `status: "WIP"`, or as a
proposed lot/outcome record. It MUST NOT write any of these as an accessioned
object, title binding, verified custody observation, or completed donation.
It MUST NOT infer accession from a wallet transfer or a donor attribution.

When a valid donation later completes, append one `MUSEUM_ACCESSION_LOT_V1`
for `6529NM.2026.001` and one `STREAM_ACCESSION_V1` object record per token.
Each object gets its own CAIP-19 identity, title binding, custody observation,
rights record, technical/preservation evidence, and reviewer sign-off. The
collection-level curatorial argument does not substitute for those object
records.

## 10. Future Stream-native Keys and Gates

Keys and Gates `6529NM-AP-01` has 16 Wave `WINNER` outcomes in the current
Museum memory. `WINNER` means selection, not mint, purchase, transfer, title,
rights clearance, or accession. The contract migration MUST keep those states
separate.

For a future Stream-native Keys and Gates work:

1. Migrate the selected outcome with its stable
   `6529NM-AP-01-OUT-<NNN>` ID and source Wave/drop evidence.
2. After the actual mint and acquisition are independently verified, register
   the Stream subject. Do not replace the outcome ID.
3. Only after the §2.1 convergence gate has a pinned callable module, exact
   owner-record preimage, and deployed round-trip vector may an approved
   adapter write or link a Stream owner record. Until then, the Museum records
   the candidate and evidence without claiming a Stream owner-record write.
   After convergence, use `STREAM_WORK_DESCRIPTION_V1`,
   `STREAM_ACCESSION_V1`, `STREAM_RIGHTS_V1`, and only the exact profile IDs
   that passed that gate.
4. Write the Museum accession lot, program result, title/custody observations,
   and institutional approval in the Museum registry.
5. Cross-check byte-for-byte canonical payloads and `contentHash` values.
   Stream's `collectionId` and host-specific record hash remain in the link;
   neither system becomes the other's token or ownership authority.

No contract rule may assume that a Meme Card vote or funding formula creates
an accession. CC0, consent, availability, fallback ranking, and other Keys
and Gates conditions remain payload facts governed by the applicable program
record and live source status.

## 11. Chain reorgs and finality

The registry cannot make an EVM transaction reorg-safe. The migration client
MUST:

* treat a record as provisional until the target chain's declared finality
  threshold is reached;
* discard removed logs and re-read state after every detected reorg;
* never permanently cite an orphaned transaction or block in a custody/title
  observation;
* use the stateful lane head and record hash for retry decisions, not a local
  assumption that a prior batch survived;
* append a new observation/correction if a finalized source-chain state later
  differs, preserving the prior observation and its hash;
* use typed record-state qualifiers for custody, render, and metadata claims.

`recordedAt` is a block timestamp and is not finality. `recordedBlock` is an
observation aid. Finality evidence and source transaction hashes are captured
in the migration manifest or payload, not synthesized by the contract.

An L2 migration MUST additionally identify the L2 output/finality mechanism
and its content-addressed proof. Cross-chain custody claims MUST NOT be
finalized merely because an RPC endpoint returned a temporary owner value.

## 12. Upgrades and deprecation

V1 is append-only and non-proxy. A successor MUST:

* expose a new immutable module version and its predecessor address;
* preserve the exact V1 envelope and all V1 read selectors;
* retain the V1 hash domain and Stream compatibility commit for migrated data;
* import by record hash and verify envelope/payload/chain commitments;
* emit an import event with source registry, source record hash, source chain,
  and destination record hash;
* never rewrite or delete an old record;
* receive explicit governance approval before becoming the write target.

`setSuccessor` is one-way. `freezeWrites` is one-way for the old registry and
does not erase read access. A successor cannot silently change a shared schema,
canonicalization ID, subject derivation, authorization-class meaning, or
Stream adapter behavior. A change needs a new ID and a new convergence gate.

## 13. Test vectors and conformance

The following vectors are normative smoke tests. Test code MUST reproduce them
with Solidity ABI encoding, not packed encoding.

### 13.1 External subject

```text
assetProfileId = 0xac72cc7c2b027b8ee3d459de7829fd7b3b31cf575c28734e736ebd33b10f41cc
canonicalAssetId = eip155:1/erc721:0x06012c8cf97bead5deae2370709587f8e7a266d/771769
keccak256(bytes(canonicalAssetId)) = 0x0ff37eede3af67254c8d44c52b88bce8e1b191ace633f456212fd13d9cbdcca9
subjectId = 0xa6e5bb8be82a8267e4c7a5398a63d1b1cf8d3c612aa4529349882667e8a2ba78
```

Changing the address to EIP-55 case MUST be rejected by the CAIP-19
canonicalizer or produce a different non-admitted input; it MUST NOT silently
produce a second subject.

### 13.2 Canonical payload and Museum record hash

```text
recordTypeLiteral = MUSEUM_RESEARCH_NOTE
recordType = 0x5a50f1234f1c89b5d9c2f5b2062279349feac41d8e01bf708ee9adc20a2d8ba0
subjectId = 0x1111111111111111111111111111111111111111111111111111111111111111
canonicalPayload = {"id":"6529NM.2026.001.1","status":"proposed"}
payloadMode = INLINE
payloadMode uint8 = 1
supersedesRecordHash = 0x0000000000000000000000000000000000000000000000000000000000000000
recordHashDomain = 0x0c86cc4258c69b4674aa86e715d4d167bd8288b78832a0a4c5a37943b31876c4
contentHash.algorithm = 1
contentDigest = 0x5eb73c2a5337f2ba50340e7a39042e942894d09ec210e537334fbe068b710b73
keccak256(contentHash.digest) = 0x23a91b3a3e46e505e103bc13198f617068273bf16ef976794ee14bde2640a2e5
contentHash.canonicalizationId = 0x886c7c89c308c459ca8a626e0ef36a5ea9f4c7a7b56aaf86c71a2ddf3b4f9044
uri = ipfs://bafybeigdyrzt5example
uriHash = 0x8104a3a6d02c26de42514a3425567e1b75724dfda699658584c39e61153b713c
schemaId = 0xe3d3da75ee91ec6a7603f809eb413342e42874cabf3992d443409657745c3cf0
signatureScheme = 0x0000000000000000000000000000000000000000000000000000000000000000
signatureHash.algorithm = 0
signatureHash.digest = 0x
signatureHash.canonicalizationId = 0x0000000000000000000000000000000000000000000000000000000000000000
keccak256(signatureHash.digest) = 0xc5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470
hashRefHash(contentHash) = 0x66de33e7d57cf2169917368e5d3e0e9e9841cd367f8de4ff95f3a15164456462
hashRefHash(signatureHash) = 0x2653d71e6881daccbff9917e23f12df8e56f7a0f8688215ca7092a5368a7d470
chainId = 1
registry = 0x0000000000000000000000000000000000000001
effectiveAt = 1722470400
recordHash = 0xc4c82486491323ce9af3d84d00b239e1148832fb059b8880483e4a838b320627
```

For the first lane append, `revision = 1`, `previousRecordHash = 0x00...00`,
and `chainHash = 0xd4e3b242f775f431ac172cd764f032addceb847ceb646845c74b9fb6d6319f63`.

### 13.3 EIP-712 relayed write

With chain ID 1, verifying contract `0x0000000000000000000000000000000000000001`,
the record hash above, `signedRecordHash` equal to that record hash,
`signedPreviousRecordHash = 0x00...00`, `previousRecordHash = 0x00...00`,
nonce 7, and deadline 1,800,000,000:

```text
EIP712Domain type string = EIP712Domain(string name,string version,uint256 chainId,address verifyingContract)
EIP712 name = 6529 Network Museum Registry
EIP712 version = 1
MuseumRecordWrite type string = MuseumRecordWrite(bytes32 recordHash,bytes32 recordType,bytes32 subjectId,bytes32 previousRecordHash,uint256 nonce,uint64 deadline)
signedRecordHash = 0xc4c82486491323ce9af3d84d00b239e1148832fb059b8880483e4a838b320627
signedPreviousRecordHash = 0x0000000000000000000000000000000000000000000000000000000000000000
previousRecordHash = 0x0000000000000000000000000000000000000000000000000000000000000000
nonce = 7
deadline = 1800000000
record.signatureScheme = 0x0000000000000000000000000000000000000000000000000000000000000000
record.signatureHash = (algorithm=0,digest=0x,canonicalizationId=0x0000000000000000000000000000000000000000000000000000000000000000)
domainSeparator = 0xfffa62454cc94111fc3da4487def1fc9f0e36727a701015f2a46ff4a1a7c7b70
MuseumRecordWrite typeHash = 0xa7df80542664ee83129e8d3ace9f44135f9a4514ad949246a14df795f16dbb3e
structHash = 0x7d4ea0e0c6cc267d01b953edec4e87a7dc20e2cc8a0c882037830608b426c57b
preimage = 0x1901 || domainSeparator || structHash
preimage = 0x1901fffa62454cc94111fc3da4487def1fc9f0e36727a701015f2a46ff4a1a7c7b70d7d4ea0e0c6cc267d01b953edec4e87a7dc20e2cc8a0c882037830608b426c57b
digest = 0xee99a98f35e2cc855f10e1feeb3c21be639e75dd2c2c28effc811cf09cf8f4b8
```

The raw EIP-712 preimage is exactly 2 bytes followed by two 32-byte words;
it MUST NOT be ABI-encoded as `bytes2`, which would insert 30 zero bytes.

### 13.4 Nonce-revocation EIP-712 vector

The domain is the same as §13.3. For signer
`0x000000000000000000000000000000000000dead`, nonce `7`, and deadline
`1800000000`:

```text
EIP712Domain type string = EIP712Domain(string name,string version,uint256 chainId,address verifyingContract)
EIP712 name = 6529 Network Museum Registry
EIP712 version = 1
chainId = 1
verifyingContract = 0x0000000000000000000000000000000000000001
domainSeparator = 0xfffa62454cc94111fc3da4487def1fc9f0e36727a701015f2a46ff4a1a7c7b70
MuseumNonceRevocation type string = MuseumNonceRevocation(address signer,uint256 nonce,uint64 deadline)
MuseumNonceRevocation typeHash = 0xe97842aa32d8e097ebbd7f3ac132b20c38ade8bb2862f2dcda25fb3b4fe51eef
structHash = 0xadf1dd94e8baaec142f9dbd1eb48a0a874d50bf369dd06d1dfd0ab0e374eae13
preimage = 0x1901fffa62454cc94111fc3da4487def1fc9f0e36727a701015f2a46ff4a1a7c7b70adf1dd94e8baaec142f9dbd1eb48a0a874d50bf369dd06d1dfd0ab0e374eae13
digest = 0x87c87440dbee8e7d2313e0be413d6222bea14055b0f324da81e0e9ef8849e4cd
```

### 13.5 Provisional Stream owner-record vector

For the same envelope, a Stream write MUST derive its hash with the pinned
formula:

```solidity
keccak256(abi.encode(
    keccak256("6529stream.preservation-record.v2"),
    block.chainid,
    address(streamPreservationRecords),
    streamCore,
    collectionId,
    record.recordType,
    record.subjectId,
    hashRefHash(record.contentHash),
    keccak256(bytes(record.uri)),
    record.schemaId,
    record.signatureScheme,
    hashRefHash(record.signatureHash),
    record.effectiveAt
));
```

The Stream hash MUST NOT be compared to the Museum hash as an equality test.
The bilateral equality test is: exact envelope shape, exact content hash,
exact schema/type/subject IDs, canonical payload bytes, and successful
round-trip through the Stream and Museum export profiles.

The provisional owner-record vector is not evidence that the pinned Stream
commit implements this interface:

```text
streamCore = 0x0000000000000000000000000000000000001001
ownerRecordModule = 0x0000000000000000000000000000000000002002
collectionId = 42
tokenId = 771769
streamSubjectId = 0x1111111111111111111111111111111111111111111111111111111111111111
canonicalOwnerRecordPayload = {"record":"owner","tokenId":"771769"}
ownerRecordHashDomain = 0x148c88658eea0b57062f88c63dba1f2aa0ffd33da6528e2a1ace1f145cf2b54a
ownerRecordHashVectorId = 0x8642db6f4603da6e1d6676bd54b8c64cc5c4f06521236402b75e1b84ab928e3c
keccak256(canonicalOwnerRecordPayload) = 0x1978e517eeb4e20fc20ca3b1110613584494206425197a9d447d7e11c6dab70d
ownerRecordHash = 0xee351e5f3e3edbbdf00670dc9116f99ef5ed8da4d070b6a3c734d81a099b0fd4
```

### 13.6 Release-manifest vector

For one record with source ordinal `1`, path
`specs/onchain/contract-migration-v1.md`, record hash from §13.2, payload
mode `INLINE`, payload bytes from §13.2, source commit
`6ab83b456f1ad8d1b7b88b79cc960954feb56432`, Stream commit
`5021c8060950c3fef995271e674ed4b2007fee6d`, and generator
`museum-migration/1.0.0`. Their `bytes32` encodings are respectively
`0x0000000000000000000000006ab83b456f1ad8d1b7b88b79cc960954feb56432` and
`0x0000000000000000000000005021c8060950c3fef995271e674ed4b2007fee6d`.

```text
pathHash = 0x47f5e941106c25d308590891c8eb0bb3c721586361b9a9bf442b49782c132183
payloadBytesHash = 0x5eb73c2a5337f2ba50340e7a39042e942894d09ec210e537334fbe068b710b73
entryHash = 0x3aa074dec49b0294d9abb908dceea5a4d202418c4c3853fdf844bd645f62b7f7
root = 0x685f7fa37801cc1c6264ff9bbf143d836926887ad890132e43a1943b7a91b41a
```

### 13.7 Required negative tests

Conformance MUST cover malformed digest lengths, zero IDs, zero effective
time, invalid UTF-8/oversized or unsafe-scheme URI, unknown schema/type/profile,
wrong class, wrong predecessor, duplicate hash, payload-mode mismatch, payload
mismatch, empty payload for a meaning-bearing schema, missing/cross-lane/newer
supersession target, expired signature, invalid EOA signature, invalid
ERC-1271 result, ERC-1271 callback lane/nonce mutation, used/revoked nonce,
nonce-revocation digest mismatch, batch over cap, batch partial failure,
duplicate external subject, noncanonical asset alias, duplicate mirror link,
pre-convergence Stream link, reorg retry, URI substitution, and attempted
writes after freeze.

It MUST also prove that:

* an external token registration does not create a custody/title/accession
  state;
* a custody observation does not create legal title;
* a title binding does not change token owner;
* a `WINNER` program outcome does not create accession;
* a superseding record leaves the old hash and payload readable;
* state-only reconstruction works with all events unavailable;
* a Stream-native record can round-trip without changing its canonical payload;
* an unauthorized Museum-only class cannot write a Stream family;
* a successor import preserves the source hash and lane lineage.

## 14. Deployment gates

No contract deployment or migration transaction is authorized until all gates
below pass and Museum governance explicitly approves the deployment:

1. **Pinned source gate:** the Stream adapter is tested against commit
   `5021c8060950c3fef995271e674ed4b2007fee6d`; source and system-manifest
   hashes are recorded.
2. **Schema gate:** every shared profile used by a write has exact ID, canonical
   schema bytes, document hash, and worked vector. Unpublished pinned-commit
   profile IDs are resolved or excluded.
3. **Identity gate:** CAIP-19/CAIP-10 normalization and every supported legacy
   profile have collision tests and vectors.
4. **Envelope/hash gate:** ABI tuple order, `abi.encode`, hash algorithms,
   explicit payload mode and supersession binding, URI limits/public-network
   safety, signature emptiness rules, raw EIP-712 prefix, and Museum/Stream
   hash distinction pass golden tests.
5. **Authorization gate:** family masks, Safe/ERC-1271, EOA signatures,
   unordered nonces, nonce-revocation commitments/deadlines, reentrancy
   callback rechecks, global-role selector scope, authority timelock,
   successor-after-freeze, one-way freeze, provider rotation, and class
   isolation pass negative tests.
6. **Lineage gate:** duplicate rejection, predecessor/head accumulation,
   correction/supersession, successor import, batch atomicity, and state-only
   reconstruction pass.
7. **Privacy gate:** public/restricted separation is reviewed; no private
   donor, legal, appraisal, credential, signer-security, or storage-location
   data appears in payloads, events, or URIs.
8. **Custody/title gate:** ERC-721/1155/legacy/non-EVM adapters are reviewed;
   title binding is tested as a separate fact; no accession completes without
   the Museum completion profile.
9. **Migration rehearsal gate:** a frozen repository manifest migrates in a
   disposable environment; `MUSEUM_RELEASE_MANIFEST_V1` source ordinals,
   per-record entry hashes, root, and body hash are independently regenerated;
   reorg retry is rehearsed; and a third party regenerates the index, dossier,
   PREMIS/LIDO exports, and manifests.
10. **Canonicalizer/URI gate:** every asset profile's runtime hash,
    implementation hash when EIP-1967 proxyable, version ID, and collision
    behavior are checked before registration; every HTTPS URI has a valid,
    unexpired `MUSEUM_HTTPS_PUBLIC_NETWORK_ASSERTION_V1` record.
11. **Operational gate:** registrar, curator, digital-conservation, privacy,
    and records-management review is complete; incident and recovery runbooks
    are content-addressed.
12. **Security gate:** independent contract review/audit covers authority
    capture, replay, malformed external strings, griefing/spam, reentrancy in
    providers, URI/payload mismatch, upgrade/import, and chain reorg handling.
    The audit MUST also verify the write-once external-subject/mirror selectors
    and the closed Stream owner-record convergence gate.
13. **Governance gate:** deployment address, authority provider, write policy,
    migration scope, and non-goals are explicitly adopted; current signer
    names are not hard-coded.

## 15. Non-goals

V1 does not:

* mint, wrap, remint, bridge, transfer, burn, freeze, or escrow artwork;
* replace native ownership, title, provenance, marketplace, or custody state;
* enforce copyright, licenses, display terms, donor conditions, or curatorial
  interpretation through token transfer restrictions;
* treat a GitHub commit, Wave vote, `WINNER` label, airdrop, or wallet receipt
  as accession without the applicable evidence and authority;
* publish private donor, legal, appraisal, signer, infrastructure, or storage
  data;
* invent CAIP identifiers for unsupported chains;
* require every future Stream schema to be duplicated in the Museum registry;
* make event logs the sole data store;
* guarantee finality against a chain reorg;
* hard-code the current Safe signer set or a permanent governance mechanism;
* implement a contract, deploy an address, migrate live assets, accept a
  donation, or make a legal/tax/valuation determination.
