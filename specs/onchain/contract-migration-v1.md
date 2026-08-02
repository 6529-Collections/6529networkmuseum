# Network Museum contract migration specification — V1 draft

Status: implementation-grade working specification; not adopted policy, not deployed, and not an implementation.

Pinned compatibility target: `6529-Collections/6529Stream` `origin/main` commit
`5021c8060950c3fef995271e674ed4b2007fee6d`, observed 2026-08-01 UTC.

The synchronized Museum repository source/release baseline for the worked
release manifest is `ff1c5825e3b61bfb2df0a639e057297beb946e4d` (`origin/main`
after the approved rarity-tooling merge). It is the source snapshot before
this PR, not the PR head and not a self-referential manifest input. Its
right-aligned
`bytes32` encoding and the resulting `0x8bb17fc4361cbfe29c586218e716d0c4789973b222ee7a403f9d22f6f483a280`
root are repeated in the one-record worked vector in §13.6; no other source
commit or worked-vector root is normative for this draft. That §13.6 root is
not the repository release-artifact root in
`release-artifacts/latest/record-manifest.json`: the latter is generated from
the complete governed inventory, including every `specs/onchain/` file, after
the final commit and is independently checked by the manifest tool.

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
* The pinned Stream commit supplies the collection-record implementation and
  publishes a draft owner-record struct, write/revocation ABI, EIP-712 domain,
  and typehashes in `docs/collection-metadata-contract.md`. It does not contain
  the corresponding `StreamOwnerRecords` source/deployment, a pinned owner
  `recordHash` preimage/read surface, or a deployed round-trip vector. V1
  therefore matches the published draft semantics but does not claim that a
  Museum contract can write Stream owner records. A Stream-native integration
  remains closed until the bilateral convergence gate in §2.1 passes.

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

### 2.1 Draft owner-record ABI and closed deployment boundary

The pinned Stream source publishes the generic preservation-record surface,
including the `CollectionRecord` field order at
`6529Stream@5021c8060950c3fef995271e674ed4b2007fee6d:smart-contracts/IStreamPreservationRecords.sol:18-28`,
the generic domain literal at
`6529Stream@5021c8060950c3fef995271e674ed4b2007fee6d:smart-contracts/StreamPreservationRecords.sol:22-29`,
and the generic `abi.encode` preimage at
`6529Stream@5021c8060950c3fef995271e674ed4b2007fee6d:smart-contracts/StreamPreservationRecords.sol:210-231`.
Separately, the pinned draft at
`docs/collection-metadata-contract.md:3062-3168` publishes this owner-record
shape and ABI:

```solidity
struct OwnerRecord {
    bytes32 recordType;
    bytes32 subjectId;
    bytes32 schemaId;
    HashRef contentHash;
    string uri;
    bytes payload;
    uint64 effectiveAt;
}

function recordOwnerRecord(uint256 tokenId, OwnerRecord calldata record) external;
function recordOwnerRecordFor(uint256 tokenId, OwnerRecord calldata record,
    address owner, uint256 nonce, uint64 deadline, bytes calldata signature) external;
function isOwnerRecordNonceUsed(address owner, uint256 nonce) external view returns (bool);
function revokeOwnerRecordNonce(uint256 nonce) external;
function revokeOwnerRecordNonceFor(address owner, uint256 nonce, uint64 deadline,
    bytes calldata signature) external;
```

The canonical write selectors are `0x198c95e3` and `0xf24bb020`; nonce/revoke
selectors are `0x18544c94`, `0x9d03970a`, and `0x50e9829a`. The draft pins
`STREAM_OWNER_RECORD_TYPEHASH =
0x9c8c4f8b7ec1e8731277f53e36271ebf92fc96425f0c082143042400814c6b05`
for the exact whitespace-free type string in §13.5, plus
`STREAM_OWNER_RECORD_REVOCATION_TYPEHASH =
0x11a07172744cbac614966ef944b190ff3c1b4a7076ab4483c69e48ba2b9ee49c`.
Its EIP-712 domain is name `6529StreamOwnerRecords`, version `1`, chain ID,
and the satellite address as verifying contract.

The owner-record `subjectId` is not caller-defined. The pinned Stream draft
requires token-scoped records to use
`STREAM_SUBJECT_TOKEN_V1 =
0x1e576f27850d12bc1ec9255ca277dbecfbc84fb3a9a34c474640dfca89811d7e`
and derive
`keccak256(abi.encode(STREAM_SUBJECT_TOKEN_V1, uint256(chainId),
address(streamCore), uint256(tokenId)))`. Every bilateral vector and future
adapter MUST recompute and reject a mismatching subject.

These are real published draft semantics, not an implemented module claim.
The pinned `smart-contracts/` tree has no corresponding `StreamOwnerRecords`
source, deployed address/runtime commitment, callable read surface, exact owner
`recordHash` preimage/domain, or deployed round-trip vector. The generic
`CollectionRecord` preimage is not an owner-record preimage. The Museum's
future convergence adapter is therefore a Museum interface, never represented
as Stream's current ABI:

```solidity
interface IMuseumStreamOwnerRecordConvergenceAdapterV1 {
    function streamCore() external view returns (address);
    function ownerRecordBinding(uint256 tokenId) external view returns (
        uint256 collectionId, bytes32 streamSubjectId, bytes32 ownerRecordHash);
    function ownerRecordHashDomain() external pure returns (bytes32);
    function ownerRecordHashVectorId() external pure returns (bytes32);
}

interface IStreamCoreCollectionView {
    function tokenCollectionIdentity(uint256 tokenId) external view returns (
        bool mappingExists, uint256 collectionId,
        uint256 collectionSerial, bool burned);
    function tokenLifecycle(uint256 tokenId) external view returns (uint8 lifecycle);
}
```

The Core reads are published at the pinned Stream commit and have canonical
selectors `0xa6b638c9` and `0x8c46d901`. Stream pins `UNKNOWN = 0`,
`PREPARED_INCOMPLETE = 1`, `MINTED = 2`, and `BURNED = 3`. The Museum registry
calls both reads directly on the admitted Core; it never accepts collection
identity or lifecycle solely from the convergence adapter.

External asset profiles use an admitted immutable, non-proxy canonicalizer
with the following read-only contract surface. The registry MUST accept a
candidate only when the canonicalizer returns the same canonical bytes
supplied by the caller:

```solidity
interface IMuseumAssetCanonicalizerV1 {
    function canonicalize(bytes32 profileId, string calldata supplied)
        external view returns (string memory canonical);
}
```

V1 deliberately has no proxy support and no self-reported implementation or
version hash. The canonicalizer's version ID is metadata bound to its admitted
runtime code hash; a target cannot change it by returning a different value.
V1 also pins one execution-limit profile:

```solidity
bytes32 constant MUSEUM_CANONICALIZER_EXECUTION_LIMITS_V1 =
    0xf66c08f21c02834b2dd294a0556fb5adb7c17b447338ee0ad5ecc1a2198509d3;
uint256 constant CANONICALIZER_CALL_GAS_LIMIT = 100_000;
uint256 constant MAX_CANONICALIZER_RETURN_DATA_BYTES = 4_096;
uint256 constant MAX_CANONICAL_ASSET_ID_BYTES = 2_048;
```

These values and their literal limit-profile ID are fields in
`canonicalizer-runtime-purity-v1.json`; changing any value requires a new
profile/version and new vectors, never reinterpretation of V1. The asset-profile
document MUST repeat the limit-profile ID and values and bind them through its
`documentHash`.

The registry's admission and registration checks are: (1) `canonicalizer` is
nonzero and has nonzero runtime code size; (2) `canonicalizerMode == 0`
(`IMMUTABLE_RUNTIME`); (3) `canonicalizerImplementationHash == bytes32(0)`;
(4) `extcodehash(canonicalizer) == canonicalizerCodeHash != bytes32(0)`;
(5) the runtime bytecode instruction scan below finds no forbidden mutable,
external-call, proxy, environment-dependent, or creation opcode; and (6) a
`staticcall` with exactly `CANONICALIZER_CALL_GAS_LIMIT` gas to
`canonicalize(profileId, supplied)` succeeds, returns no more than
`MAX_CANONICALIZER_RETURN_DATA_BYTES`, decodes as exactly one canonical ABI
`string`, and returns byte-for-byte `supplied`. The registry checks
`returndatasize` before copying or decoding the return and never allocates an
unbounded return buffer. `supplied` MUST be nonempty and at most
`MAX_CANONICAL_ASSET_ID_BYTES` UTF-8 bytes. Profile admission runs this exact
bounded call against the governance-supplied `conformanceInput`, verifies its
byte-for-byte fixed point, and stores `keccak256(bytes(conformanceInput))`;
registration repeats it against the proposed canonical asset ID. A zero code
hash, mode `1`/`EIP1967_PROXY`, a nonzero
implementation hash, a failed staticcall, or a code hash that changes between
admission and registration, gas exhaustion, excess return data, malformed ABI,
or output mismatch MUST revert. V1 therefore never reads an EIP-1967 slot and
never trusts a self-reported implementation hash.

The governed `AssetProfile` row is an allowlist entry for the exact tuple
`(profileId, canonicalizer, canonicalizerCodeHash,
canonicalizerConformanceInputHash)`. Its `documentHash` MUST
commit the reviewed canonicalizer source, deterministic compiler/toolchain
configuration, and the scanner report; `canonicalizerVersionId` identifies
that reviewed source/toolchain build. A caller-supplied hash is never an
allowlist grant. Governance MUST admit only an exact extcodehash produced by
that reviewed build, and the bytecode scan below is defense-in-depth rather
than a proof that arbitrary code is pure.

The scan pins the Cancun EVM revision (EIPs available through Cancun); a
future EVM revision MUST use a new canonicalizer profile/version, reviewed
opcode table, source/toolchain document hash, and exact extcodehash allowlist.
The scan operates on a defined executable runtime region. Read the complete
runtime bytes with `extcodecopy`; `canonicalizerCodeHash` remains the
`extcodehash` of those complete bytes, including any metadata. Exclude a
trailer only when the final two bytes encode a big-endian length `L`, the
preceding `L` bytes are exactly one definite-length CBOR map, and that map
contains a compiler marker key `solc` or `vyper` whose value is a byte string.
The executable region is `[0, codeSize-L-2)` in that case; otherwise the
region is the complete runtime and admission MUST fail if it is not a valid
instruction stream. An invalid, ambiguous, or nonstandard trailer is never
silently stripped. Bytes in a trailer satisfying the exact rule are metadata,
not executable opcodes, so a forbidden byte there cannot cause a metadata false
reject; bytes in any unrecognized trailer remain in the executable region and
make admission fail closed if decoding is ambiguous. No other suffix or
compiler marker is an accepted exclusion.

Within that region, the scanner is a deterministic syntactic EVM instruction
walk: begin at offset 0, decode one opcode, treat `PUSH0` (`0x5f`) as having
zero immediate bytes, skip exactly `opcode - 0x5f` immediate bytes for
`PUSH1`–`PUSH32`, and otherwise advance one byte. A byte inside a PUSH
immediate is never an opcode or a `JUMPDEST`. A `JUMPDEST` is a valid target
only at a decoded instruction boundary; a static jump to a non-boundary or an
invalid/truncated instruction stream rejects admission. Dynamic jump targets
are not used to waive any ban.

The scanner MUST reject `ADDRESS`, `ORIGIN`, `CALLER`, `CALLVALUE`, `CODESIZE`,
`CODECOPY`, `RETURNDATASIZE`, `RETURNDATACOPY`, and `PC`, as well as `SLOAD`,
`SSTORE`, `TLOAD`, `TSTORE`, `CALL`, `CALLCODE`, `DELEGATECALL`, `STATICCALL`,
`CREATE`, `CREATE2`, `SELFDESTRUCT`, `EXTCODESIZE`, `EXTCODECOPY`,
`EXTCODEHASH`, `BALANCE`, `BLOCKHASH`, `COINBASE`, `TIMESTAMP`, `NUMBER`,
`PREVRANDAO`, `GASLIMIT`, `CHAINID`, `SELFBALANCE`, `BASEFEE`, `BLOBHASH`
(`0x49`), `BLOBBASEFEE` (`0x4a`), `GAS` (`0x5a`), `GASPRICE`, and `LOG0`
through `LOG4`. `CALLDATALOAD`, `CALLDATASIZE`, and `CALLDATACOPY` remain
allowed because they read only the supplied profile/input bytes; the exact
allowlisted runtime and byte-for-byte return equality still govern their use.
Under the pinned Cancun opcode table, all reserved/unknown/invalid opcodes and
any EOF-form runtime are rejected closed. This rejects known proxy and
metamorphic forms and any runtime whose canonicalization result can depend on
storage, another contract, caller/address/value, code introspection, mutable
chain/blob state, returndata, program counter, gas, logging, or code creation.
The walk is deliberately not a reachability proof: it conservatively rejects
forbidden opcodes even in unreachable executable-region bytes and MUST NOT be
used to claim that an allowlisted hash is pure. It never skips decoded
executable bytes, and any PUSH-boundary, jump-target, opcode-table, trailer,
or EOF ambiguity rejects admission. The governed source/toolchain allowlist
and an independently reviewed control-flow/disassembly report are the primary
authority; the scan is defense-in-depth and cannot turn a non-allowlisted hash
into an admission. If that report cannot establish valid EVM boundaries and
JUMPDEST targets, the exact hash is rejected. The scan is performed at
admission and on every external-asset registration; an unscannable, changed,
proxy-like, or non-allowlisted runtime is not admitted.

The exact bilateral reference carries the Museum CAIP-19 external-asset
identity, `ownerRecordModule`, `streamCore`, `collectionId`, `collectionSerial`,
`tokenId`, `streamSubjectId`, `ownerRecordHash`,
`ownerRecordHashDomain`, and `ownerRecordHashVectorId`. The admitted adapter
returns the collection, Stream subject, and owner-record hash: its
`streamCore()` binds the deployment, and `ownerRecordBinding(tokenId)` returns
those three fields in one bounded read. The Museum registry independently
reads `tokenCollectionIdentity(tokenId)` from the admitted Core and requires a
present, unburned mapping with nonzero collection and serial whose collection
equals the adapter result. It independently recomputes the Stream subject from
`STREAM_SUBJECT_TOKEN_V1`, `block.chainid`, the admitted core, and `tokenId`,
and rejects any disagreement. It also reconstructs the exact lowercase
`eip155:<chainId>/erc721:<streamCore>/<tokenId>` CAIP-19 string, requires the
existing Museum `ExternalAsset` row to use `MUSEUM_ASSET_PROFILE_CAIP19_V1`
and that exact string/hash, recomputes its Museum external subject, and
requires the caller's Museum subject to equal it. V1 does not invent a record hash from the
published EIP-712 authorization typehash: the authorization digest and stored
owner `recordHash` are distinct commitments.

The convergence gate accepts the published draft ABI/typehash facts above but
remains closed until Stream publishes and pins the implementing source and
deployed module/version, exact owner `recordHash` domain/preimage and read
surface, payload/canonicalization enforcement, nonce/revocation behavior,
runtime hash, golden vector, and a state-readback round trip against that
deployment. The Museum gate MUST verify the draft selectors and EIP-712
typehash unchanged or explicitly adopt a later Stream revision, then record
the complete evidence and exact Stream commit. Before that gate, Keys and Gates
records remain Museum-side proposals/evidence; no mirror link may claim an
owner-record mutation or title assertion.

`admitStreamOwnerRecordInterface` is a dedicated append-only admission lane.
It increments its own interface `revision`, stores the evidence hash and
`authorityRevision`, and MUST emit `StreamOwnerRecordInterfaceAdmitted` with
the actual `MUSEUM_GLOBAL_ROLE_GOVERNANCE_EXECUTOR_V1` role ID. A role or
authority rotation never rewrites this admission history; a new interface
module or vector is a new revision and requires a new convergence gate.
`streamOwnerRecordInterfaceAtRevision(revision)` is the state reconstruction
view for every prior admission; the zero revision is absent and MUST revert.
Each revision binds one exact Stream Core address/runtime hash and one exact
adapter address/runtime hash. Admission rechecks both direct `extcodehash`
values and requires bounded exact-length adapter reads whose `streamCore()`,
hash domain, and vector ID equal the supplied values, plus source-backed
evidence for the Core's `tokenCollectionIdentity(uint256)` selector and return
shape. Every mirror write
repeats those runtime and readback checks, so a changed core, adapter, domain,
or vector cannot use an earlier admission.

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
| Draft owner-record EIP-712 typehash | `StreamOwnerRecord(address owner,uint256 tokenId,bytes32 subjectId,bytes32 recordType,bytes32 schemaId,uint16 algorithmId,bytes digest,bytes32 canonicalizationId,string uri,bytes payload,uint64 effectiveAt,uint256 nonce,uint64 deadline)` | `0x9c8c4f8b7ec1e8731277f53e36271ebf92fc96425f0c082143042400814c6b05` |
| Draft owner-record revocation typehash | `StreamOwnerRecordRevocation(address owner,uint256 nonce,uint64 deadline)` | `0x11a07172744cbac614966ef944b190ff3c1b4a7076ab4483c69e48ba2b9ee49c` |

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
| Batch commitment domain | `6529networkmuseum.batch-commitment.v1` | `0x6743de485825345432a60824968ffa9c8b3ef54adb2f4ad2d1cb219ec56e4400` |
| External subject domain | `6529networkmuseum.subject.external-asset.v1` | `0x1dd722ea239e47e25bdadfcc0053bdc4e7ee75e7ca9dd0afe97076a6d9eb8a80` |
| CAIP-19 asset profile | `MUSEUM_ASSET_PROFILE_CAIP19_V1` | `0xac72cc7c2b027b8ee3d459de7829fd7b3b31cf575c28734e736ebd33b10f41cc` |
| Relayed authorization scheme (outside the envelope) | `MUSEUM_SIGNATURE_EIP712_RECORD_V1` | `0xd522d14409fadb7afb8c4cbf90ad662519010926e69625200b14f0ba12c90cba` |
| Relayed nonce-revocation scheme (outside the envelope) | `MUSEUM_SIGNATURE_EIP712_NONCE_REVOKE_V1` | `0xda7e20c41761de210a954ede904dd134c0d4dd6c8dc7e73c4072a8c717b956a5` |
| Global role | `MUSEUM_GLOBAL_ROLE_GOVERNANCE_EXECUTOR_V1` | `0x865cb1cc1a43094ea97b42f5b9e950e7952c1f106d37051e97d2a3fdb1584ce2` |
| Global role | `MUSEUM_GLOBAL_ROLE_REGISTRAR_V1` | `0xb1f5e657823d31bde6c263be60f0418d7361b8365b264c97798c0b790c1a5f8b` |
| Global role | `MUSEUM_GLOBAL_ROLE_MIGRATION_ADMIN_V1` | `0x2729f1662f9bb2682a0a433e8329cd1b73680e122f49b4b4987cef1106b97004` |
| Global role | `MUSEUM_GLOBAL_ROLE_AUTHORITY_ADMIN_V1` | `0x28ad41c29b6a0872dec6410316cebb3f72fc3c9e4f4ea88e8e87e81784c94426` |
| Global role | `MUSEUM_GLOBAL_ROLE_HTTPS_ATTESTOR_V1` | `0x47df6320f751abd29d6ce09022685a520d0128d5f284c7573d3b6857127abc61` |
| Family kind enum (`uint8`) | `MUSEUM_FAMILY_KIND_STREAM_V1` | `1` |
| Family kind enum (`uint8`) | `MUSEUM_FAMILY_KIND_MUSEUM_V1` | `2` |
| Registry version | `MUSEUM_REGISTRY_VERSION_V1` | `0xa4377bcc11c8c6cbfc23ffd4952add9dc8738fbcf125cb088673edda975f1748` |
| Registry protocol version | `MUSEUM_PROTOCOL_VERSION_V1` | `0xea7ed1159fede00c63bf928f3b977361b7471b9bd72bb677289a42b8eec98713` |
| Stream compatibility commit | `MUSEUM_STREAM_COMPATIBILITY_COMMIT_V1` | `0x0000000000000000000000005021c8060950c3fef995271e674ed4b2007fee6d` |
| Empty-payload canonicalization | `MUSEUM_EMPTY_PAYLOAD_V1` | `0xa441d30896b70045ccf31ccc5b89cefd312a64c9c2102fa1c6898140d443ef4f` |
| HTTPS capacity-report profile | `MUSEUM_HTTPS_ASSERTION_CAPACITY_REPORT_V1` | `0x8254a96c886cc988ce26c264ffacd912591f898c2af6202c5aef644264741d2e` |
| Authority role domain | `MUSEUM_AUTHORITY_ROLE_DOMAIN_V1` | `0x5509945d050bff1c25739ca8055ca317188c749980e0e568fcca64f86ab3ceef` |
| Authority capability domain | `MUSEUM_AUTHORITY_CAPABILITY_DOMAIN` | `0x560a68b3805ede9cc4ce0392157e0f258fa8a17fe9b645807781464e1eb3ba7b` |
| Governance-executor binding domain | `6529networkmuseum.governance-executor-binding.v1` | `0xc36068b55c238ed7d9935be44bdbe89a03cee1aaacccd5c0b739c1b40f5e5b06` |
| Initial-authority artifact domain | `6529networkmuseum.initial-authority-artifact.v1` | `0x30f33e8eab225ed59c69940c862e794a4d87ebd05fb31cdbae4b1a8b93b39733` |
| Authority capability selector-set hash | `MUSEUM_AUTHORITY_SELECTOR_SET_HASH` | `0x4c2a05297ef36555d0bd199b80df1463d02702f6bd1bde9444960279d15957e5` |
| Transition target probe domain | `6529networkmuseum.target-probe.v1` | `0x122d724a712544b8c62e62a557b68492224acd31feabb1b39b05d778ab04336a` |
| Successor capability domain | `6529networkmuseum.successor-capability.v1` | `0x95cc8014d6585c06b5ef08da6faaa308466d830923f3aab6503afc261a5e4ad3` |
| Authority-provider interface | `IMuseumAuthorityProviderV1` | `0xea450898` |
| Successor interface | `IMuseumSuccessorV1` | `0x573d91cc` |
| Museum URI safety profile | `MUSEUM_URI_SAFETY_PUBLIC_V1` | `0x5480eb62c7af1dd376bd8ddad6729a756d0f05ce8610d2a21e798440fc859189` |
| Museum URI safety profile document hash | `MUSEUM_URI_SAFETY_PUBLIC_V1_DOCUMENT_V1` | `0x8dc321494e0703072c5f2f1e7967473836640551e4b5c64e8fe94116029cefbb` |
| HTTPS assertion record type | `MUSEUM_HTTPS_PUBLIC_NETWORK_ASSERTION_V1` | `0x8041bfef6459ccf942bb6bfe17c778c4db60a9d0831f24f6154deba96e99391e` |
| HTTPS assertion signature scheme | `MUSEUM_SIGNATURE_EIP712_HTTPS_PUBLIC_V1` | `0x738aed5a63fd21dfdd96f878826e6652140072c65ee952653d5432bf6ded33d0` |
| HTTPS assertion subject domain | `6529networkmuseum.subject.https-public.v1` | `0xe08003722c1e7c0465bdd4353706df75808fa767fca549cc020bd0c0081e59f4` |
| HTTPS assertion hash domain | `6529networkmuseum.https-assertion.v1` | `0x4fcfa708a5b354629d48cb2b96432841b5566b13b7c8f30468d34106b0f7904a` |
| HTTPS resolver profile | `MUSEUM_HTTPS_RESOLVER_PROFILE_DNS_V1` | `0x52be64fd2fb1c3795cf8dd6472100377858fd563f16de75584dcaf0f74b3e186` |
| Payload schema | `MUSEUM_REGISTRY_RECORD_V1` | `0xc9f2c9b650ebb4955871484238be9d3dfd1bf9f0ec09a5365917d6294e5967c9` |
| Payload schema | `MUSEUM_EXTERNAL_ASSET_IDENTITY_V1` | `0x34e9649723069df3772c810e6e825f7589c211bac81acc9b908a60067f936aa6` |
| Payload schema | `MUSEUM_CUSTODY_OBSERVATION_V1` | `0xb0c467baa7db6862385e58253c1c4702d95b141a1ef66cd2b86234a597344014` |
| Payload schema | `MUSEUM_ACCESSION_LOT_V1` | `0x8bb4cfecf4d3736765bc80624dd0a876d2e1c17bf5a406066d5f2256fc739d44` |
| Payload schema | `MUSEUM_PROGRAM_OUTCOME_V1` | `0x7a25e6a6a5e91d55ef0ea9115ad5902929bcf0d3331b4bb2d22100f65fc78470` |
| Payload schema | `MUSEUM_RELEASE_MANIFEST_V1` | `0x7a41091035def3c5fa62722d73a7ea87f996fe9be34e9115317c5d128581d299` |
| Payload schema | `MUSEUM_RESEARCH_NOTE_V1` | `0xe3d3da75ee91ec6a7603f809eb413342e42874cabf3992d443409657745c3cf0` |
| Manifest entry domain | `6529networkmuseum.release-manifest.entry.v1` | `0xa524091b411df027ff64e4f8d590d93cf7e2e7658f6a5a8f623abfb4e01671ef` |
| Manifest root domain | `6529networkmuseum.release-manifest.root.v1` | `0xe615064b79fb81a121afe1ad24d886aa86536f320be540a31023f43bbe935b64` |
| Target-release identity domain | `6529networkmuseum.target-release-id.v1` | `0xb46f066b6a2753ffb8634e3ab1934b6d08110f50ca4d56478f0c05b8ae5f6ff0` |
| Release-attestor signer-set domain | `6529networkmuseum.release-attestor-signer-set.v1` | `0x70780232933964b71995ee4297ea125c132dbe977dd96658f75b993dc82b8c78` |
| Target-release EIP-712 domain typehash | `EIP712Domain(string name,string version,uint256 chainId,address verifyingContract)` | `0x8b73c3c69bb8fe3d512ecc4cf759cc79239f7b179b0ffacaa9a75d522b39400f` |
| Target-release EIP-712 name hash | `6529NetworkMuseumTargetRelease` | `0xad57a2fb87ede840686d52adfaccaae3c8c993597c2d21faf621069c6907e07e` |
| Target-release EIP-712 version hash | `1` | `0xc89efdaa54c0f20c7adf612882df0950f5a951637e0307cdcb4c672f298b8bc6` |
| Target-release EIP-712 typehash | `MuseumTargetReleaseAttestation(bytes32 releaseId,bytes32 conformanceDocumentHash,bytes32 signedDocumentHash,bytes32 releaseAttestorPolicyHash,bytes32 releaseAttestorSignerSetHash)` | `0x56ebb221b517fc83550c540843ed9cc30095835ef9b097e4c7fb9a51b9854ed7` |
| Release-signature-set domain | `6529networkmuseum.release-signature-set.v1` | `0x4ab65e998eae4ebf35f9bc7579b02bcf9c44a1dae6b6eb14f65dfe6b2bc32a68` |
| Target-dependency row domain | `6529networkmuseum.target-dependency-row.v1` | `0x0b0481d6fc4f5287c63d8e94d48e3b7f67661cbb8773f25ee18b45f6531d33ca` |
| Target-dependency set domain | `6529networkmuseum.target-dependency-set.v1` | `0xeff667c3cf8eaa69b18ff3eea3d99d00f81293b6f031311cbe41b89a540a04a2` |
| Canonicalizer purity policy | `MUSEUM_CANONICALIZER_RUNTIME_PURITY_V1` | `0xa6bf8d47e01db9e1380475c7e9afe08bfa7bdc4ee378d3164d4058da2904e2e7` |
| Canonicalizer purity policy document hash | `canonicalizer-runtime-purity-v1.json` | `0x0c0a10c923084b4861fbf9c4e869302de19ef6b103c2698263915fc56ac3461f` |
| Target non-upgradeability policy | `MUSEUM_TARGET_RUNTIME_NONUPGRADEABILITY_V1` | `0x8148bd5ce1f57455106f3425ad39d8c0c80e527c51c51ad350f27028e8c6c367` |
| Target non-upgradeability policy document hash | `target-runtime-nonupgradeability-v1.json` | `0x95f9e52ebbfec6aa2d1ad41a516a6d9e7ce2f55cfed9de1fb906e6f6e9dae452` |
| Dependency non-proxy policy | `MUSEUM_DEPENDENCY_RUNTIME_NONPROXY_V1` | `0x91f6a97952f01ee36bc37c89abea588f77f59e170cfa6614d160d98762fdf452` |
| Dependency non-proxy policy document hash | `dependency-runtime-nonproxy-v1.json` | `0xf8efb731af735014514f4a5b8ad22a6e2007ba23b11b45a9c8845db3f144ee2c` |
| Target-release evidence schema | `MUSEUM_TARGET_RELEASE_EVIDENCE_V1` | `0xbb8a203a0f161e49f7f5fd9cdd4471c56e21263fa789bb50ec6198ff4b441f6c` |
| Target-release evidence schema document hash | `target-release-evidence-v1.schema.json` | `0xa54955d0077ad11a6b376b872aeeff758c36fe4c126f777ac3df64c01933a214` |
| Target-release signature bundle schema hash | `target-release-signature-bundle-v1.schema.json` | `0x12256931d7eebded2483454fdff90c2496ffca9cec980b1a07306b03082bef82` |
| Release-attestor policy schema document hash | `release-attestor-policy-v1.schema.json` | `0x7ce79b67b7882dfa70c5bee9e62b7ccba9a987a338ae3b0186862e03a21bbc06` |
| Batch benchmark schema | `MUSEUM_BATCH_GAS_BENCHMARK_V1` | `0xfd6cc699ac634ec33160703ce1c9a46a43fab11232511f2ef8ad220520d05d1c` |
| Batch benchmark corpus hash | `batch-gas-benchmark-v1.json` | `0xf69a816a38f9b0f1addd6f8270318d6c1aacf17cb55bfb2adcb7efbe5983b293` |
| Batch benchmark report schema hash | `batch-gas-benchmark-v1.schema.json` | `0x4384db06bd8e764511d5f0aca0a4ed656b1ff6ea5e412f313f6eb2407bec45e6` |
| URI vector bundle | `MUSEUM_URI_VECTOR_BUNDLE_V1` | `0xc5d4b5509668127362d486c057b5183a4cf2379d537401e0cf8b5e0cdedd9925` |
| Museum-native stable family | `MUSEUM_FAMILY_MUSEUM_NATIVE_V1` | `0x3b1abe4d004439222a742d0cad0e6c8e179135c6fbcf1853b509976d51b77cd0` |
| Authority target kind (`uint8`) | `MUSEUM_TARGET_KIND_AUTHORITY_V1` | `1` |
| Successor target kind (`uint8`) | `MUSEUM_TARGET_KIND_SUCCESSOR_V1` | `2` |

The stable Museum record-type IDs below are `keccak256` of the exact ASCII
literal shown (without the `_V1` schema suffix). Each type is permanently
paired with the listed payload schema; a deployment MUST NOT substitute a
deployment-local type ID for one of these records.

| Record-type literal | Record-type ID | Required payload schema | Required class |
|---|---|---|---|
| `MUSEUM_EXTERNAL_ASSET_IDENTITY` | `0xe1c1798f46d210552c5d3924b7059a57b07eedf054640a662eb47bac008b4a8e` | `MUSEUM_EXTERNAL_ASSET_IDENTITY_V1` | `AUTH_MUSEUM_REGISTRAR (10)` |
| `MUSEUM_CUSTODY_OBSERVATION` | `0x8351820e5600a2472b0dd68eb83a0480b8663df2efcab7d34321b1df5918316e` | `MUSEUM_CUSTODY_OBSERVATION_V1` | `AUTH_MUSEUM_PROGRAM_AUTHORITY (11)` |
| `MUSEUM_ACCESSION_LOT` | `0xc544e9b2b8226296197005f65dd84855588d18be5e1ce13082b8314004cb4661` | `MUSEUM_ACCESSION_LOT_V1` | `AUTH_MUSEUM_PROGRAM_AUTHORITY (11)` |
| `MUSEUM_PROGRAM_OUTCOME` | `0xe81870465556c524f1375c1a3cff4aa920e8f0c15b9858ae6bb55c6c3cb0ad5a` | `MUSEUM_PROGRAM_OUTCOME_V1` | `AUTH_MUSEUM_PROGRAM_AUTHORITY (11)` |
| `MUSEUM_RESEARCH_NOTE` | `0x5a50f1234f1c89b5d9c2f5b2062279349feac41d8e01bf708ee9adc20a2d8ba0` | `MUSEUM_RESEARCH_NOTE_V1` | `AUTH_MUSEUM_PROGRAM_AUTHORITY (11)` |
| `MUSEUM_RELEASE_MANIFEST` | `0x8889bb0d1446ec07b517aca915af9a4ad6d993ef8af5b999301ca8b15f789084` | `MUSEUM_RELEASE_MANIFEST_V1` | `AUTH_MUSEUM_MIGRATION_ADMIN (12)` |

The table is a closed-world admission rule, not documentation-only metadata.
The stable family for all six rows is
`MUSEUM_FAMILY_MUSEUM_NATIVE_V1`; its `familyKind` MUST be `2` and its
bitmap MUST include every listed class. Before storing or revising any row
whose `recordType` is one of these six IDs, `admitRecordType` MUST compare the
supplied `(familyId, schemaId, authorizationClass)` byte-for-byte with the row
above and MUST reject any other family, schema, or class with
`StableRecordTypePairMismatch`. A stable ID cannot be paired with a
deployment-local schema or family. The same check MUST run before a
record-type revision becomes active; non-stable record IDs remain subject to
the ordinary governed family/schema admission rules.

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
`6529NM.2026.999.01`. Chain, contract, wallet, creator, and collection data
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

The Museum preimage is intentionally not positionally ABI-tuple aligned with
Stream's pinned generic `CollectionRecord` preimage. `payloadMode` and
`supersedesRecordHash` are Museum-only fields, and the Museum host address is
not a positional substitute for Stream's `streamCore`/collection context.
Bilateral equality therefore applies only to named shared ontology/profile
fields and canonical payload bytes; it MUST NOT compare whole ABI tuples by
position or require the two record hashes to be equal.

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

V1's enforceable correction guarantee is envelope lineage only. A legitimate
correction MUST therefore change at least one field committed by
`recordHash` (normally `contentHash`, `uri`, `schemaId`, `signatureScheme`,
`signatureHash`, `effectiveAt`, `payloadMode`, or the nonzero
`supersedesRecordHash`) and SHOULD carry payload-level
`supersedes`/reason/evidence. The contract does not parse arbitrary JSON or
claim to validate those semantic fields. An admitted schema may require an
off-chain validator/attestation in its release-gated migration tooling, but
that is not a V1 on-chain guarantee unless a future version admits a pinned
validator interface, code hash, schema commitment, and proof bound to the
payload and `supersedesRecordHash`. V1 enforces only the target's existence,
same lane, and older revision below. Repeating
byte-identical content under the same envelope is a reference to the existing
record, not a new revision. This explicitly resolves identical-envelope
recurrence: the first accepted hash wins, and corrections are new hashes.

Lanes are keyed by `(recordType, subjectId)`. Revision starts at 1. The first
record has predecessor and prior chain hash zero. A write MUST supply the
current lane head as `previousRecordHash`; a batch advances that head in array
order. A missing or incorrect predecessor reverts.

The migration profile SHOULD contain schema-defined correction fields when it
supersedes another record, including `supersedes`, `supersession_reason`,
`authority`, `effective_at`, and evidence references. Those are release-gated
off-chain checks, not contract parsing. The contract still enforces the
envelope, digest, URI, and admitted-schema rules. When
`supersedesRecordHash != bytes32(0)`, the target
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
uint256 constant MAX_BATCH_GAS_UNITS = 13_000_000;
uint256 constant BATCH_CALLER_RESERVE_GAS = 50_000;
uint256 constant MEASURED_BATCH_GAS_THRESHOLD = 9_000_000;
uint256 constant MAX_HTTPS_ADDRESSES = 32;
```

For a batch, each `INLINE` payload MUST be at most
`MAX_INLINE_PAYLOAD_BYTES`, and the sum of all inline payload byte lengths in
the batch MUST be at most `MAX_BATCH_INLINE_PAYLOAD_BYTES`. The per-record
limit still applies when the batch contains one record. `CONTENT_ADDRESSED`
and `NONE` contribute zero to the batch inline-byte total.

The batch commitment is deterministic and is computed before the first state
write. For input index `i`, `payloadHash[i]` is `keccak256(payload[i])` for
`INLINE` and `bytes32(0)` for `NONE` or `CONTENT_ADDRESSED`; every
`recordHash[i]` is recomputed from the final envelope and every
`previousRecordHash[i]` is the supplied predecessor. The exact preimage is:

```solidity
batchCommitment = keccak256(abi.encode(
    MUSEUM_BATCH_COMMITMENT_DOMAIN,
    batchId,
    uint64(inputs.length),
    recordHashes,
    previousRecordHashes,
    payloadHashes,
    authorityRevision
));
```

`recordHashes`, `previousRecordHashes`, and `payloadHashes` are dynamic
`bytes32[]` values encoded by ordinary `abi.encode` in input order; no sorting
or packed encoding is permitted. The batch stores `batchId -> batchCommitment`
and `batchIdUsed(batchId) == true` atomically with the records. A reused batch
ID, duplicate record hash, stale predecessor, or any later record failure
reverts the entire call and emits no batch or record event. A reorg retry MUST
re-read `batchIdUsed`, each record hash, and each surviving lane head; it may
submit only the not-yet-present records under a fresh batch ID. A client may
treat an already-used ID as idempotent only after the stored commitment and
all record/lane state match exactly.

For a caller gas-budget gate, the contract computes
`requiredGas = 250000 + 120000 * inputs.length + 16 * inlineBytes` before any
write, rejects `requiredGas > MAX_BATCH_GAS_UNITS`, and rejects when
`gasleft() < requiredGas + BATCH_CALLER_RESERVE_GAS`. This formula is the versioned
`MUSEUM_BATCH_GAS_GATE_V1` best-effort caller gate; it is not a reproducible
upper bound on execution gas and MUST NOT be treated as one. URI parsing,
schema checks, HTTPS assertion checks, storage expansion, and event encoding
may cost more; an out-of-gas failure still reverts the whole call. Count,
inline-byte, and `MAX_BATCH_GAS_UNITS` budget caps remain independently
enforced. A deployment gate MUST retain a measured benchmark report for all
V1 batch paths, but the report is operational evidence rather than a protocol
gas proof.

The measured report is a JSON object with schema
`MUSEUM_BATCH_GAS_BENCHMARK_V1` and MUST validate against the release-controlled
corpus file `specs/onchain/batch-gas-benchmark-v1.json`. Its JCS corpus hash is
`0xf69a816a38f9b0f1addd6f8270318d6c1aacf17cb55bfb2adcb7efbe5983b293`.
The report MUST validate against
`specs/onchain/batch-gas-benchmark-v1.schema.json`, whose JCS hash is
`0x4384db06bd8e764511d5f0aca0a4ed656b1ff6ea5e412f313f6eb2407bec45e6`.
It MUST contain `schema`, `version`, `chainId`, `evmRevision`,
`registryCodeHash`, `deploymentAddress`, `deploymentBlock`, `rpcEndpointId`,
`forgeVersion`, `solcVersion`, optimizer/via-IR/EVM settings, the corpus hash,
one measured gas value for every corpus case, and two independent builder
signatures over the JCS report without its signatures member. The report's
chain ID MUST be 1 and its runtime code hash MUST equal the deployed registry.
The corpus pins Foundry `1.7.1` commit
`4072e48705af9d93e3c0f6e29e93b5e9a40caed8`, Solidity `0.8.19` commit
`7dd6d404`, optimizer enabled with 200 runs, `viaIR=false`, and Cancun. The
signed report additionally MUST bind the runner OS/architecture, immutable
runner-image digest, CPU model, RPC endpoint identifier, deployment block
hash, and registry runtime code hash; a missing or non-digest environment value
fails the gate. There are no placeholder toolchain values in the corpus.

The corpus is deliberately worst-case, not a representative average: 64
`NONE` records; 64 maximum-URI `CONTENT_ADDRESSED` records; 64 records with
16 maximum-size `INLINE` payloads consuming all 262,144 batch inline bytes;
and the same maximum inline load with HTTPS assertion pointers and envelope
supersession checks. Each case uses unique lanes, maximal schema/type/URI
field lengths, event emission, and the exact authority revision checks. The
worst `https-supersession-max` input calculates `12,124,304` required units and
`12,174,304` with the caller reserve, so it is admissible below the separate
`MAX_BATCH_GAS_UNITS` eligibility cap of 13,000,000. The deployment acceptance
threshold is independently measured execution gas at most 9,000,000 for every
case and measured gas plus the 50,000 caller reserve at most 9,050,000. Neither
threshold is inferred from, or converts, the caller formula into an execution
gas bound. Every case MUST complete atomically on a
fork at the pinned deployment block; any out-of-gas, revert, missing case,
placeholder toolchain value, or code-hash mismatch fails deployment. This is a
release/deployment gate and does not convert `MUSEUM_BATCH_GAS_GATE_V1` into an
execution upper-bound claim.

`python -B specs/onchain/batch_gas_gate_check_v1.py` MUST reproduce all corpus
formula results, including the worst-case caller-reserve calculation above. It
does not execute a contract and makes no measured-gas claim; the separately
signed benchmark report remains the deployment measurement gate.

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
  whose schema says that no payload bytes are needed. Its `contentHash` is the
  one exact empty-payload `HashRef` in §5.2.1; no caller-selected empty hash
  profile is permitted.

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
contract. `NONE` MUST supply zero payload bytes, an empty URI, and the exact
empty-payload `contentHash` below.

### 5.2.1 Exact `NONE` content-hash profile

Every V1 `NONE` record MUST use this exact `HashRef`:

```text
contentHash.algorithm = 1
contentHash.digest = 0xc5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470
contentHash.canonicalizationId = 0xa441d30896b70045ccf31ccc5b89cefd312a64c9c2102fa1c6898140d443ef4f
```

The digest is `keccak256(bytes(""))`; the canonicalization ID is
`keccak256(bytes("MUSEUM_EMPTY_PAYLOAD_V1"))`. Applying the ordinary V1
`hashRefHash` formula gives:

```solidity
keccak256(abi.encode(
    uint16(1),
    keccak256(hex"c5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470"),
    MUSEUM_EMPTY_PAYLOAD_V1
))
```

and MUST equal
`0x5d7e6369b77349763919edf197e8a1ba931bbfd63a9e40b5af00ca630a4346c7`.
The inner digest-byte hash is
`0x10ca3eff73ebec87d2394fc58560afeab86dac7a21f5e402ea0a55e5c8a6758f`.

This rule is intentionally different from the all-zero `signatureHash`
exception used when `signatureScheme == bytes32(0)`: an empty content payload
is still a typed content commitment, while an absent envelope signature is no
signature commitment. Direct, relayed, and batch write paths MUST recompute
and compare all three `contentHash` fields before authorization or any state
write. They MUST reject a zero/empty `HashRef`, a different algorithm,
`RFC8785_JCS`, a caller-selected canonicalization ID, the raw empty digest in
place of the required digest, or any other digest even when payload bytes and
URI are empty. Section 13.2.1 is the positive vector; §13.10 requires these
mutations as negative vectors.

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

`MUSEUM_URI_SAFETY_PUBLIC_V1` is independently implementable from the
following exact UTF-8 profile-document bytes (the code block contains one
line, with no trailing LF). Its Keccak-256 is
`0x8dc321494e0703072c5f2f1e7967473836640551e4b5c64e8fe94116029cefbb` and
an admission using this profile MUST use this document hash:

```text
{"id":"MUSEUM_URI_SAFETY_PUBLIC_V1","version":1,"maxUtf8Bytes":2048,"schemes":["ar","https","ipfs"],"requireLowercaseScheme":true,"reject":{"controls":true,"userinfo":true,"query":true,"fragment":true,"httpsPort":true,"httpsTrailingDot":true,"httpsNumericAmbiguity":true,"httpsMappedIpv6":true},"httpsDns":{"asciiLowercase":true,"labelMaxBytes":63,"totalMaxBytes":253,"requireDot":true},"httpsIp":{"reservedIpv4Cidr":["0.0.0.0/8","10.0.0.0/8","100.64.0.0/10","127.0.0.0/8","169.254.0.0/16","192.0.0.0/24","192.0.2.0/24","192.88.99.0/24","192.168.0.0/16","198.18.0.0/15","198.51.100.0/24","203.0.113.0/24","224.0.0.0/4","240.0.0.0/4"],"reservedIpv6Cidr":["::/128","::1/128","::ffff:0:0/96","100::/64","2001:2::/48","2001:10::/28","2001:db8::/32","fc00::/7","fe80::/10","ff00::/8"],"rejectReservedCidr":true,"rejectIpv4MappedIpv6":true,"ipv4DottedDecimal":true,"ipv6Rfc5952":true,"rejectZoneId":true,"rejectEmbeddedIpv4":true},"ipfs":{"cidv0":"reject","cidv1":{"multibase":"base32lower","prefix":"b","version":1,"codecs":[85,112],"multihashCode":18,"digestBytes":32,"rejectOverlongVarint":true,"requireCanonicalReencode":true}},"ar":{"identifier":"base64url-unpadded","characters":"A-Z a-z 0-9 _ -","length":43,"decodedBytes":32,"requireCanonicalReencode":true},"path":{"asciiPchar":true,"percentTripletsUppercase":true,"rejectMalformedPercent":true,"rejectEncodedUnreserved":true}}
```

The validator first rejects invalid UTF-8, more than 2,048 UTF-8 bytes,
U+0000--U+001F or U+007F controls, userinfo, query, and fragment. Scheme
matching is case-sensitive and only `https`, `ipfs`, and `ar` are admitted.
For HTTPS, the authority is either a dotted DNS name or a bracketed IPv6
literal, with no port. DNS is ASCII lowercase, has at least two labels, has
labels of 1--63 bytes containing only `a`--`z`, `0`--`9`, or interior `-`,
and has a total length of at most 253 bytes; an empty label, leading/trailing
hyphen, uppercase letter, trailing dot, or non-ASCII byte rejects. IPv4 is
exactly four decimal octets with no leading zero unless the octet is `0`, and
single-integer, hexadecimal, octal, short, and dotted forms with any other
numeric ambiguity reject. IPv6 uses lowercase RFC 5952 hexadecimal syntax,
allows `::` only once, disallows zone IDs and embedded dotted IPv4, and
rejects every CIDR in the profile document, including IPv4-mapped IPv6.
Listed IPv4/IPv6 ranges are checked as integer ranges, not by string prefix.
The path is empty or consists of ASCII RFC 3986 pchar and `/`; a literal `%`
is valid only as the start of exactly two hexadecimal digits, those triplets
are uppercase hexadecimal, and percent-encoding an unreserved byte rejects.
`ipfs` and `ar` use the same byte/control/query/fragment checks. CID varints
MUST use their shortest encoding; an overlong encoding is rejected before any
value is read. After decoding an accepted CIDv1 or Arweave identifier, the
validator MUST re-encode it in the required lowercase unpadded base32 or
base64url form and require byte-for-byte equality to the supplied authority;
unused encoding bits and every alternate textual spelling reject.

The complete V1 conformance vectors are executable, not merely illustrative.
The release-controlled harness at
`specs/onchain/uri_safety_vectors_v1.py` executes this table, validates the
1380-byte profile-document hash, and hashes the RFC 8785 vector bundle with
`MUSEUM_URI_VECTOR_BUNDLE_V1 =
0xc5d4b5509668127362d486c057b5183a4cf2379d537401e0cf8b5e0cdedd9925`.
The bundle contains 44 vectors and its exact Keccak-256 is
`0x252c699a34e0c162f4055c292f23f7360272e3ec4b37031f2d17966055641011`.
The command `python -B specs/onchain/uri_safety_vectors_v1.py` MUST pass before
deployment and whenever this profile is changed.

The complete V1 conformance vectors are:

| URI | Result | Reason |
|---|---|---|
| `https://example.com/art` | ACCEPT | lowercase DNS, valid labels |
| `https://a-b.example/x` | ACCEPT | interior hyphen and path |
| `https://8.8.8.8/x` | ACCEPT | canonical globally routable IPv4 |
| `https://[2001:4860:4860::8888]/x` | ACCEPT | canonical globally routable IPv6 |
| `https://example.com` | ACCEPT | empty path is allowed |
| `ipfs://bafybeiexd37whdwmbipbf7acxcrll2pg6lwcz6ks7atxc6z4niszkoragq/path` | ACCEPT | CIDv1 base32, dag-pb, sha2-256 CID |
| `ar://AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA` | ACCEPT | 43-character base64url transaction identifier |
| `https://example.com./x` | REJECT | DNS trailing dot |
| `https://a..example.com/x` | REJECT | empty DNS label |
| `https://-a.example.com/x` | REJECT | leading label hyphen |
| `https://A.example.com/x` | REJECT | uppercase DNS byte |
| `https://example.com:443/x` | REJECT | explicit port |
| `https://user@example.com/x` | REJECT | userinfo |
| `https://127.0.0.1/x` | REJECT | loopback IPv4 |
| `https://010.0.0.1/x` | REJECT | leading-zero numeric ambiguity |
| `https://2130706433/x` | REJECT | single-integer numeric ambiguity and no dot |
| `https://192.0.2.1/x` | REJECT | documentation IPv4 range |
| `https://[::ffff:8.8.8.8]/x` | REJECT | IPv4-mapped IPv6 |
| `https://[2001:db8::1]/x` | REJECT | documentation IPv6 range |
| `https://example.com/a%2fb` | REJECT | lowercase percent triplet |
| `https://example.com/a%2Fb` | ACCEPT | uppercase triplet for a reserved path byte |
| `https://example.com/a%41` | REJECT | encoded unreserved byte |
| `https://1.2.3/x` | REJECT | short numeric IPv4 form |
| `https://0x7f000001/x` | REJECT | hexadecimal numeric form |
| `https://[2001:4860:4860::8888%25eth0]/x` | REJECT | IPv6 zone identifier |
| `https://[2001:4860:4860:0:0:0:0:8888]/x` | REJECT | non-RFC-5952 IPv6 spelling |
| `hex("https://example.com/x\\x01")` | REJECT | exact control byte U+0001 |
| `https://example.com/x?y` | REJECT | query |
| `https://example.com/x#frag` | REJECT | fragment |
| `ipfs://bafybeigdyrzt5example/path` | REJECT | truncated CIDv1 multihash |
| `ar://AbCdEf012_-` | REJECT | transaction identifier is not exactly 32 decoded bytes |
| `https://example.com/a%` | REJECT | incomplete percent triplet |
| `https://example.com/a%G0` | REJECT | non-hex percent triplet |
| `https://100.64.0.1/x` | REJECT | shared CGNAT IPv4 range |
| `https://example.com:abc/x` | REJECT | nonnumeric port; parser failure is caught and rejected |
| `https://example.com/café` | REJECT | non-ASCII path character |
| `ipfs://bqeahaeraaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/path` | REJECT | overlong CIDv1 version varint |
| `ipfs://bafybeiexd37whdwmbipbf7acxcrll2pg6lwcz6ks7atxc6z4niszkoragq:443/path` | REJECT | explicit IPFS authority port |
| `ipfs://QmYwAPJzv5CZsnAzt8auVZRnGJH4p2v4WgDy5h1h7P42J9/path` | REJECT | CIDv0 is disallowed for new Museum writes |
| `ipfs://bafybeiexd37whdwmbipbf7acxcrll2pg6lwcz6ks7atxc6z4niszkoragr/path` | REJECT | CIDv1 unused base32 bits are noncanonical |
| `ar://AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAB` | REJECT | Arweave unused base64url bits are noncanonical |
| `HTTPS://example.com/x` | REJECT | uppercase scheme alias |
| `IPFS://bafybeiexd37whdwmbipbf7acxcrll2pg6lwcz6ks7atxc6z4niszkoragq/path` | REJECT | uppercase scheme alias |
| `AR://AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA` | REJECT | uppercase scheme alias |

The conformance table, executable harness, profile-document bytes, and document hash are one
versioned predicate. A future EVM revision or URI parser MUST use a new
profile ID/document hash and a new vector set; it MUST NOT reinterpret this
profile in place. The URI parser treats the profile ID and document hash as
immutable V1 constants and every HTTPS record path MUST execute that exact
predicate; a generic asset-profile admission MUST NOT be able to replace or
reinterpret it.

The non-HTTPS grammar is closed in V1. CIDv0 is rejected for all new Museum
writes: allowing a base58 CIDv0 and a CIDv1 representation of the same
multihash would fork canonical URI identity. An IPFS authority is only CIDv1:
lowercase multibase `b` followed by unpadded lowercase RFC 4648 base32,
decoding to the exact
minimally encoded varint sequence `version=1`, `codec in {0x55 (raw), 0x70 (dag-pb)}`,
`multihashCode=0x12`, `digestLength=32`, and exactly 32 digest bytes. Uppercase
base32, base32 padding, alternate multicodecs, alternate multihashes, CIDv0,
invalid varints, truncated values, noncanonical unused bits, percent escapes in
the authority, userinfo, ports, query, and fragment are rejected. The optional IPFS path uses the same pchar,
uppercase-percent-triplet, and encoded-unreserved rules as the HTTPS path.
An Arweave URI is exactly `ar://` followed by 43 unpadded base64url characters
(`A-Z`, `a-z`, `0-9`, `_`, `-`) decoding to exactly 32 bytes and re-encoding to
the identical 43-character unpadded form; it has no path, userinfo, port,
query, or fragment. No other IPFS or Arweave grammar is
implicitly accepted by V1.

The pinned Stream source documents only its shared UTF-8/2,048-byte URI
validation and does not supply this public-network predicate. A bilateral
adapter MUST pass the URI through both predicates and MUST NOT rewrite a URI;
the Museum predicate is intentionally stricter. Therefore a URI that is
Stream-valid but Museum-invalid (for example, an HTTPS URI with a port or
userinfo) MUST be rejected for mirroring; it MUST NOT be rewritten or silently
downgraded. The adapter records this non-convergence and defers the export
until a governed Museum profile admits the URI. If a future Stream predicate
conflicts, the adapter opens the same convergence gate. The Museum contract
does not perform DNS resolution,
but it does enforce an on-chain assertion registry. Every Museum record write
whose parsed URI scheme is `https` MUST calculate `uriHash` from the exact
canonical URI bytes, load the current assertion pointer for that hash, and
require a matching admitted resolver profile, current profile revision,
nonexpired validity window, and globally routable address-set commitment.
No HTTPS record write may rely on a prose-only adapter precondition. An HTTPS
gateway MAY be a retrieval convenience, but it is never the integrity anchor.

The canonical HTTPS assertion payload is RFC 8785 JCS JSON with exactly these
fields and no signature bytes:

```json
{
  "schema": "MUSEUM_HTTPS_PUBLIC_NETWORK_ASSERTION_V1",
  "uriHash": "0x<64 lowercase hex>",
  "hostHash": "0x<64 lowercase hex>",
  "resolverProfileId": "0x<64 lowercase hex>",
  "resolverRevision": 0,
  "resolvedAddressSetHash": "0x<64 lowercase hex>",
  "assertionRevision": 0,
  "previousAssertionHash": "0x<64 lowercase hex>",
  "issuedAt": 0,
  "expiresAt": 0,
  "attestor": "0x<40 lowercase hex>",
  "nonce": 0,
  "deadline": 0
}
```

Its subject is
`keccak256(abi.encode(0xe08003722c1e7c0465bdd4353706df75808fa767fca549cc020bd0c0081e59f4, uriHash))`.
The assertion record MUST set `uriHash == keccak256(bytes(targetURI))` and
`hostHash == keccak256(bytes(lowercaseAsciiHost(targetURI)))`. The on-chain URI
parser extracts the lower-case ASCII host from the exact `https://` authority;
it rejects a port, userinfo, empty host, non-ASCII host, query, fragment,
control, or path syntax forbidden by `MUSEUM_URI_SAFETY_PUBLIC_V1`. The
resolver MUST submit `address[] sortedUniqueAddresses` in strictly increasing
numeric `uint160` order with no duplicates. The exact commitment is
`keccak256(abi.encode(sortedUniqueAddresses))`, where the ABI type is
`address[]`; the contract recomputes it from the submitted array. The
contract rejects zero, loopback, private, link-local, multicast, documentation,
unspecified, and otherwise reserved IPv4/IPv6 values using the exact predicate
in `MUSEUM_URI_SAFETY_PUBLIC_V1` before accepting the assertion.

V1 assertions are per-URI, not per-host. The primary assertion key is the
canonical `uriHash`, including the path; a host's address set MUST NOT be
reused as a wildcard for another URI. Every distinct canonical HTTPS URI,
including every distinct path, requires its own signed assertion and its own
current-pointer entry. The exact immutable version key is:

```solidity
bytes32 assertionKey = keccak256(abi.encode(
    uriHash, resolverProfileId, resolverRevision, assertionRevision
));
```

`assertionRevision` is the URI's monotone version and `previousAssertionHash`
links that version to the prior row. `hostHash`, `resolvedAddressSetHash`,
issued/deadline fields, attestor, nonce, and the predecessor are not alternate
lookup keys: they are included in the assertion hash and complete stored row.
A key collision with different complete fields MUST revert rather than
overwrite; an exact duplicate assertion hash also MUST revert without a second
event. The submitted `hostHash` is a redundant derived commitment, not a
host-wide lookup key: `recordHttpsAssertionBySig` MUST recompute it from the
submitted canonical URI and reject any mismatch, and every HTTPS record write
MUST parse the exact record URI, recompute both `uriHash` and `hostHash`, and
require equality with the current assertion's two fields. A record may reuse
the current unexpired assertion for the same exact URI; a different path,
address set, profile revision, or assertion revision requires a separately
signed row under the corresponding key and predecessor rules. Operations MUST
budget assertion admission, storage, expiry, and renewal per distinct URI;
shared host/address data does not reduce that cardinality. A large path set
SHOULD use `ipfs://`/`ar://` or content-addressed material when per-URI HTTPS
attestation is not operationally justified.

The resolver profile registry stores an admitted profile ID, document hash,
attestor, `minTtl`, `maxTtl`, profile `revision`, and admission
`authorityRevision`. The assertion MUST use the current profile revision,
`issuedAt <= block.timestamp <= expiresAt`,
`minTtl <= expiresAt - issuedAt <= maxTtl`, at most 32 resolved addresses,
and a signer equal to the profile's
attestor with the enabled `MUSEUM_GLOBAL_ROLE_HTTPS_ATTESTOR_V1` grant. The
signature scheme is
`MUSEUM_SIGNATURE_EIP712_HTTPS_PUBLIC_V1`, and its exact signed type string is:

```text
MuseumHTTPSPublicNetworkAssertion(bytes32 uriHash,bytes32 hostHash,bytes32 resolverProfileId,uint64 resolverRevision,bytes32 resolvedAddressSetHash,uint64 assertionRevision,bytes32 previousAssertionHash,uint64 issuedAt,uint64 expiresAt,address attestor,uint256 nonce,uint64 deadline)
```

The domain is the registry EIP-712 domain from §6.2; the signature digest is
the raw `0x1901 || domainSeparator || structHash` preimage. The envelope's
`signatureHash` commits to the exact signature bytes, while the canonical
payload commits to the assertion fields. The on-chain assertion hash is
`keccak256(abi.encode(0x4fcfa708a5b354629d48cb2b96432841b5566b13b7c8f30468d34106b0f7904a, uriHash, hostHash, resolverProfileId, resolverRevision, resolvedAddressSetHash, assertionRevision, previousAssertionHash, issuedAt, expiresAt, attestor, nonce, deadline))`.
`HttpsAssertion` stores that hash, the exact key tuple, predecessor, monotone
revision, `issuedAt`, `expiresAt`, attestor, signer-scoped nonce/deadline,
signature commitment, resolver revision, authority revision, and an immutable
copy of the validated `sortedUniqueAddresses`. The state read MUST return that
array so an auditor can recompute `resolvedAddressSetHash`, strict ordering,
uniqueness, and every public-routability predicate without event history.

The HTTPS signer uses the same signer-scoped nonce/revocation state as other
relayed authorizations, but the HTTPS EIP-712 type/domain separates its
authorization scheme. `deadline` is inclusive and must be no earlier than
`expiresAt`; `nonce` must be unused and not revoked. For a URI's first
assertion, `assertionRevision == 1` and `previousAssertionHash == bytes32(0)`.
Every later assertion requires `assertionRevision == currentRevision + 1` and
`previousAssertionHash == currentAssertionHash`, even when the prior assertion
has expired. This monotone predecessor rule prevents an older assertion from
being replayed over a renewal.

The contract accepts exact ECDSA recovery for an EOA attestor and
`isValidSignature(bytes32,bytes)` for an ERC-1271 attestor only when the call
succeeds and returns exactly the four-byte ERC-1271 magic value `0x1626ba7e`.
A revert, failed call, empty or malformed return, short or long return, or any
other value is invalid. It snapshots and
rechecks the URI pointer/revision/predecessor, profile and role revision,
address-set hash, signer nonce/revocation, freeze flag, authority revision,
and registry identity around an ERC-1271 callback in the §6.2 order. A failed
or changed dependency reverts the entire call. A duplicate assertion hash,
duplicate `(uriHash, resolverProfileId, resolverRevision, assertionRevision)`
key, nonce reuse, or predecessor mismatch reverts with no state transition and
no event; clients may treat that revert as idempotent only after exact
readback. The current assertion pointer updates only after all checks pass;
existing records retain their stored assertion hash/revision and are never
rebound. After a chain reorg, retry is permitted only after rereading nonce,
assertion, and pointer state; a surviving duplicate is not emitted again.

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

Record families are closed-world and governed in state. Each admitted family
has exactly one numeric `uint8 familyKind` (`0 = INVALID/RESERVED`,
`1 = MUSEUM_FAMILY_KIND_STREAM_V1`, `2 = MUSEUM_FAMILY_KIND_MUSEUM_V1`, and
`3..255` reserved/rejected), an `allowedClassBitmap`, a family revision, and
an authority revision. A Stream family MAY contain only pinned Stream
classes 1–8; a Museum family MAY contain only Museum classes 9–12. A family
admission or revision MUST reject any bit outside its kind's permitted set.
Every admitted `recordType` maps to exactly one family, schema, and
`authorizationClass`; it MUST NOT store a multi-bit class mask. That selected
class MUST be one bit in the family bitmap. Role grants are family-scoped;
global administration MUST NOT silently become artist, owner, rights, or
independent-attestor authority.

The deterministic authorization primitive is:

```solidity
requireRecordWriter(
    bytes32 familyId,
    uint8 authorizationClass,
    address signer
)
```

It MUST load the admitted family and record-type mapping, require the exact
family kind/class relationship, require the current family revision, and
require the enabled grant keyed by `(familyId, authorizationClass, signer)`.
On success it returns the exact `familyId`, record-type-policy revision,
family revision, and family-grant revision that were loaded; every write path
persists those four historical authorization facts in `RecordSummary` and
`MuseumRecordRecorded` before advancing the lane. A later family or grant
revision never rewrites an old summary.
Direct writes pass `msg.sender`; relayed writes pass the recovered EOA or
ERC-1271 signer. Both paths MUST call this same primitive and MUST NOT have a
separate relayed class-selection rule.

`admitRecordFamily(familyId, familyKind, allowedClassBitmap)` is authority-
controlled, append-only, and emits `RecordFamilyAdmitted`. `familyKind == 0`
or `familyKind >= 3` MUST revert with `InvalidFamilyKind`; the stored, event,
and typed value is this numeric `uint8`, never a bytes32 hash. The only valid
Stream bitmap is a subset of `0x01fe` (bits 1–8); the only valid Museum bitmap
is a subset of `0x1e00` (bits 9–12). `admitRecordType` stores one integer
`authorizationClass`; its selected bit is exactly `(uint16(1) <<
authorizationClass)`, so zero, out-of-range, and multi-bit selections are
rejected. It emits that class plus the family and authority revisions.
`setRecordFamilyGrant` and
`recordFamilyGrant` are keyed by the same exact family/class tuple and expose
both revisions; no class mask is accepted by a write selector.

The initial deployment MUST bind the Museum Safe or another explicitly
governed account as the direct governance executor and separately admit an
authority-provider TargetRelease, rather than hard-coding the current signer list. The
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
| `MUSEUM_GLOBAL_ROLE_GOVERNANCE_EXECUTOR_V1` | Closed binding to the current direct governance-executor account for convergence admission, authority/executor transition execution, successor transition, and irreversible write freeze. |
| `MUSEUM_GLOBAL_ROLE_AUTHORITY_ADMIN_V1` | Closed binding to that same direct governance-executor account for role grants, release admission/quarantine, and authority/executor queue or cancellation. |
| `MUSEUM_GLOBAL_ROLE_HTTPS_ATTESTOR_V1` | Submit signed HTTPS assertions only for the resolver profile whose attestor matches the signer; it grants no record-family or governance authority. |

The global authorization domain is exactly the tuple
`(selector, globalRoleId, account, authorityRevision, governanceExecutorRevision)`, where `selector` is
the four-byte Solidity selector in the role-control table and `account` is
the `msg.sender` being checked. For the governance-executor and authority-admin
role IDs, a direct global-role call MUST require
`msg.sender == governanceExecutor`, the exact selector allowlist, and the
active authority/executor revisions. Those two closed binding roles are not
ordinary grant rows and `setGlobalRoleGrant` MUST reject attempts to grant or
revoke them. Other global roles require an enabled grant for `msg.sender` and
the active revisions; no global selector accepts a `familyId` or `classMask`.
V1 has no relayed global-role calls. A future
relayed global action requires a new signature scheme that signs this exact
domain and selector; a record-family EIP-712 signature MUST NOT be reused for
it. Record writes retain the separate family/class domain and include the
selected `authorizationClass`, exact `familyId`, record-type-policy revision,
family revision, family-grant revision, and `authorityRevision` in their audit
state.

The constructor separately binds a nonzero initial governance executor at
executor revision 1 but leaves the registry inert at initialization state `0`.
The executor may be the external Museum Safe; it is an account that calls the
registry directly, not a TargetRelease, release dependency, or runtime-policy
target. The constructor does not inspect its code or signer list and does not
hardcode either. A one-shot `activateInitialAuthority` call establishes the
first authority only after the registry address exists and the address-bound
release attestations have been produced. `setGlobalRoleGrant` is thereafter
authority-admin controlled by the current executor, append-only by role
revision, and emits the exact role ID, account, enabled state, authority
revision, and executor revision. A role grant cannot alter a record-family
class bitmap or retroactively authorize a prior record.

### 6.1.2 Authority, successor, and freeze transitions

The only accepted authority target is a contract implementing this exact
probe interface in addition to ERC-165:

```solidity
interface IMuseumAuthorityProviderV1 {
    function isMuseumAuthorityProvider() external pure returns (bool);
    function registry() external view returns (address);
    function authorityRevision() external view returns (uint64);
    function capabilityHandshake(address registry, bytes32 roleDomain,
        bytes32 selectorSetHash, bytes32 challenge)
        external view returns (bytes32 capabilityCommitment, bool canAuthorize);
}
```

Its ERC-165 interface ID is pinned by the selector transcript; the ERC-165
interface itself is `0x01ffc9a7`. The only accepted successor target is a
contract implementing this exact interface:

```solidity
interface IMuseumSuccessorV1 {
    function isNetworkMuseumRegistry() external pure returns (bool);
    function registryVersion() external pure returns (bytes32);
    function protocolVersion() external pure returns (bytes32);
    function streamCompatibilityCommit() external view returns (bytes32);
    function moduleSupersedes() external view returns (address);
}
```

Its interface ID is pinned by the selector transcript. A transition target input
is exactly `(target, expectedCodeHash, requiredInterfaceId, interfaceProbeHash,
capabilityCommitment, predecessorRegistry, expectedModuleVersion,
evidenceHash)`. The queued/stored target additionally contains
`authorityRevision`, `proposer`, `queuedAt`, `queuedBlock`, and `eta`.

Target acceptance is also closed over a governed release registry. The current
and historical key is `(targetKind, target, codeHash)`; `releaseId` has its own
global non-reuse index and therefore cannot be recycled for the same code at a
different address. Its state row is:

```solidity
struct TargetDependency {
    address dependency;
    bytes32 codeHash;
    bytes32 runtimePolicyHash;
    bytes4 interfaceId;
    bytes32 purposeId;
}

struct TargetRelease {
    bool admitted;
    uint8 targetKind;                 // 1 authority, 2 successor
    address target;                   // exact admitted address
    bytes32 releaseId;
    bytes32 codeHash;
    bytes32 runtimePolicyHash;
    bytes32 releaseAttestorPolicyHash;    // governed JCS policy commitment
    bytes32 releaseAttestorSignerSetHash; // governed ABI signer-set commitment
    bytes32 externalDependencyHash;
    uint8 externalDependencyCount;
    bytes32 sourceCommit;             // right-aligned 40-hex Git SHA-1
    bytes32 sourceTreeHash;           // right-aligned 40-hex Git SHA-1 tree OID
    bytes32 artifactHash;             // exact runtime/build artifact hash
    bytes32 conformanceDocumentHash;  // independently reproduced probe report
    bytes32 signedDocumentHash;       // D1 evidence-document commitment
    bytes32 releaseAttestationDigest; // registry/chain-bound EIP-712 digest
    address releaseAttestor0;         // first recovered governed signer
    address releaseAttestor1;         // second recovered governed signer
    bytes32 releaseSignatureCommitment0;
    bytes32 releaseSignatureCommitment1;
    bytes32 releaseSignatureSetHash;
    bytes4 requiredInterfaceId;
    bytes32 expectedModuleVersion;    // zero for authority
    bytes32 protocolVersion;
    bytes32 streamCompatibilityCommit;
    uint64 revision;
    uint64 authorityRevision;
    uint8 status;                      // 1 active, 2 quarantined
    bytes32 previousReleaseId;         // zero for the first revision
    bytes32 supersessionReasonHash;    // zero for the first revision
}
```

`releaseAttestorPolicyHash` and the three strictly increasing release-attestor
addresses are immutable registry-wide constructor inputs. The constructor
derives `releaseAttestorSignerSetHash` from that policy hash, threshold `2`,
cardinality `3`, and those addresses; it does not trust a caller-supplied set
hash. The two commitments and each signer are publicly readable, and every
admitted release row MUST equal those immutables. A V1 signer-policy rotation
therefore requires a new registry deployment and the ordinary successor gate;
a release document cannot select its own trust root.

`admitTargetRelease` is authority-admin controlled and available only while
writes are not frozen. The release history is append-only, while the current
`(targetKind, target, codeHash)` pointer may advance to a new revision. It MUST reject
a zero target, zero release/code/artifact/conformance/signed-document/runtime-policy/dependency,
release-attestor-policy, or signer-set hash, either attestor commitment unequal
to the registry immutable, signer/signature arrays other than exact length two,
signers that are duplicated, unsorted, or outside the immutable three, a
noncanonical or incorrectly recovered signature, a nonzero authority module version,
or a kind/interface/version tuple outside the V1 rules. For kind `1`, the
interface MUST be `IMuseumAuthorityProviderV1`, module version MUST be zero,
and protocol/Stream commits MUST be zero. For kind `2`, the interface MUST be
`IMuseumSuccessorV1`, module version MUST be nonzero and different from
`MUSEUM_REGISTRY_VERSION_V1`, and protocol/Stream commits MUST equal the
current V1 constants. `sourceCommit` MUST be a right-aligned 20-byte Git
SHA-1: its high 12 bytes are zero and its low 20 bytes are nonzero. A first
`sourceTreeHash` uses the identical encoding for the 40-hex SHA-1 returned by
`git rev-parse <sourceCommit>^{tree}`: 12 zero high bytes followed by the exact
20 decoded tree-OID bytes. No hashing, ASCII encoding, or left alignment is
permitted. A first
admission has `revision == 1`, `status == 1`, `previousReleaseId == 0`, and
`supersessionReasonHash == 0`. A correction of an active or quarantined row
MUST use `revision == current.revision + 1`, a new release ID, and the exact
acyclic identity derivation. `releaseId` is derived before either evidence
projection, excludes `conformanceDocumentHash`, `signedDocumentHash`,
`releaseAttestationDigest`, signature bytes/commitments, and availability, and
is globally unique. The later EIP-712 attestation binds all of those evidence
values back to this identity without introducing a release-ID cycle:

`admitTargetRelease` takes the canonical `TargetDependency[]`,
`previousReleaseId`, and `supersessionReasonHash` explicitly, but never takes
a caller dependency hash or revision. It validates, hashes, and persists the
dependency rows before deriving the identity. The
contract derives revision `1` when no current row exists and otherwise derives
`current.revision + 1`; it requires zero predecessor and zero reason for the
first row, and for every later row requires
`previousReleaseId == current.releaseId` plus a nonzero reason. It recomputes
the complete identity tuple below and requires the supplied `releaseId` to
equal it before storing anything; a caller-supplied release ID is not trusted.

```solidity
releaseId = keccak256(abi.encode(
    MUSEUM_TARGET_RELEASE_ID_DOMAIN,
    targetKind,
    target,
    codeHash,
    runtimePolicyHash,
    releaseAttestorPolicyHash,
    releaseAttestorSignerSetHash,
    externalDependencyHash,
    sourceCommit,
    sourceTreeHash,
    artifactHash,
    requiredInterfaceId,
    expectedModuleVersion,
    protocolVersion,
    streamCompatibilityCommit,
    revision,
    previousReleaseId,
    supersessionReasonHash
));
```

The new row stores `previousReleaseId == current.releaseId` and the
`supersessionReasonHash` committed by its canonical evidence document. The
old row remains readable through `targetReleaseAtRevision`; it is never
overwritten. A duplicate release ID anywhere, a same-revision row, or a row
whose exact target differs from its evidence document reverts.

The row and `TargetReleaseAdmitted` event also store `signedDocumentHash`, the
recomputed EIP-712 `releaseAttestationDigest`, both recovered attestor
addresses, both exact signature commitments, and `releaseSignatureSetHash`.
Signature bytes remain available in transaction calldata and the retained
detached bundle; the state commitments make the accepted proof independently
reconstructable without paying permanent storage for 130 signature bytes.

The canonical evidence document MUST validate against the release-controlled
`specs/onchain/target-release-evidence-v1.schema.json`, whose JCS hash is
the exact value published in §13.9.1 and checked by the retained harness.
The document's `schema` is `MUSEUM_TARGET_RELEASE_EVIDENCE_V1`, its `version`
is `1`, and its `conformanceDocumentHash` is the Keccak-256 of the exact JCS
document preimage defined below. It MUST contain, with lowercase exact encodings, the target
kind/address/code hash, all TargetRelease fields, source repository and tree
hash, source commit, the versioned target non-upgradeability policy ID/hash,
declared external-dependency hash/list, two-build evidence, probe/vector
bundle hash, governed signer-policy identity/hash, signer-set hash, signer
threshold and commitments, two independent availability
observations, and supersession predecessor/reason fields. The fixed signer
policy is exactly 2-of-3 distinct release-attestor addresses, sorted by
numeric address. Its canonical policy artifact validates against
`release-attestor-policy-v1.schema.json` (JCS schema hash
`0x7ce79b67b7882dfa70c5bee9e62b7ccba9a987a338ae3b0186862e03a21bbc06`).
`releaseAttestorPolicyHash` is the Keccak-256 of the exact RFC 8785 JCS policy
bytes. `releaseAttestorSignerSetHash` is
`keccak256(abi.encode(MUSEUM_RELEASE_ATTESTOR_SIGNER_SET_DOMAIN,
releaseAttestorPolicyHash, uint256(2), uint256(3), signer0, signer1,
signer2))`, using three strictly increasing addresses. Both hashes MUST equal
the immutable registry commitments and the fields in the release row and
evidence document. The policy's authority source is a governance-approved
deployment manifest; the document under review is evidence for that prior
decision, never a self-authorizing signer list. The detached bundle contains exactly two entries: any two of
the three admitted addresses, strictly sorted by numeric address. Each entry
signs the exact registry-bound `releaseAttestationDigest` defined below, and the evidence document
records exactly those two signature commitments in bundle order. At least two availability observations
MUST use distinct content-addressed `ipfs://` or `ar://` URIs, match the `D0`
core hash, and be independently fetched and hash-checked. HTTPS evidence
MUST additionally carry a current Museum HTTPS assertion; the contract never
fetches a network URI.

The JSON schemas' `^(ipfs|ar)://[^?#]+$` pattern is only a structural first
pass. Schema validation alone is insufficient: ordinary JSON Schema does not
decode and re-encode CIDv1 or Arweave identifiers. The normative
`target_release_evidence_check_v1.py` and
`target_release_signature_bundle_check_v1.py` semantic checks MUST apply the
exact §5.3 V1 content-addressed URI predicate at every availability and bundle
reference call site after schema validation. CIDv0, malformed or noncanonical
CIDv1/Arweave encodings, userinfo, ports, IPFS paths, queries, fragments, and
uppercase schemes MUST reject even if the broad schema pattern accepts them.

The canonical document has no inline `signatures` member. Its hash projection
prevents self-reference and follows this mandatory acyclic order: first derive
`releaseId` from the identity tuple above; then define `core(E)` from the
schema-valid evidence object `E` by omitting `availability` and
`detachedSignatureBundle`, replacing every `signers.signatureCommitments` item
with `0x` followed by 64 zeroes, setting
`signers.releaseAttestationDigest` to zero, and then applying the substitutions below.
`D0` is `core(E)` with both `conformanceDocumentHash` and
`signers.signedDocumentHash` set to zero; `conformanceDocumentHash` is exactly
`keccak256(RFC8785_JCS(D0))`. `D1` is the same projection with the already
derived real `conformanceDocumentHash` restored and
`signers.signedDocumentHash` still zero; `signedDocumentHash` is exactly
`keccak256(RFC8785_JCS(D1))`. Only then is the registry- and chain-bound
EIP-712 release attestation derived. Its domain is name
`6529NetworkMuseumTargetRelease`, version `1`, `block.chainid`, and
`address(this)`. Its exact type string is
`MuseumTargetReleaseAttestation(bytes32 releaseId,bytes32 conformanceDocumentHash,bytes32 signedDocumentHash,bytes32 releaseAttestorPolicyHash,bytes32 releaseAttestorSignerSetHash)`:

```solidity
releaseAttestationStructHash = keccak256(abi.encode(
    MUSEUM_TARGET_RELEASE_ATTESTATION_TYPEHASH,
    releaseId,
    conformanceDocumentHash,
    signedDocumentHash,
    releaseAttestorPolicyHash,
    releaseAttestorSignerSetHash
));
releaseAttestationDigest = keccak256(abi.encodePacked(
    hex"1901", targetReleaseDomainSeparator, releaseAttestationStructHash
));
```

Only then are the two commitments, detached
bundle, and availability observations derived. Both projections replace the
two commitment slots with two zero hashes, preserving their fixed threshold
cardinality. The projection, rather than a self-referential
retrieval carrier, is the canonical release evidence; the EIP-712 digest binds
that evidence to one registry deployment. The detached signature bytes use
`EIP-712-MUSEUM-TARGET-RELEASE-V1` and sign
`releaseAttestationDigest` directly. The three admitted signer addresses are strictly
increasing as `uint160` and distinct; the two bundle signer addresses are a
strictly increasing subset of that set, and both detached signatures MUST
recover to their claimed addresses. The two signature commitments are
`keccak256` of the exact detached signature bytes. One entry or an entry from
outside the admitted three fails; a third entry fails the exact-threshold V1
schema. The registry receives the same two signer addresses and signature
bytes in `admitTargetRelease`, recomputes the EIP-712 digest from its own chain,
address, release ID, and evidence commitments, performs canonical ECDSA
recovery, and stores both signers and commitments. It also stores
`releaseSignatureSetHash = keccak256(abi.encode(
MUSEUM_RELEASE_SIGNATURE_SET_DOMAIN, releaseAttestationDigest, signer0,
keccak256(signature0), signer1, keccak256(signature1)))`. An executor cannot
substitute an unsigned report or signatures from another release, chain, or
registry.

The canonical evidence object MUST also contain `detachedSignatureBundle`,
validated against `MUSEUM_TARGET_RELEASE_SIGNATURE_BUNDLE_V1` with schema hash
`0x12256931d7eebded2483454fdff90c2496ffca9cec980b1a07306b03082bef82`. It
commits an `ipfs://` or `ar://` URI, the exact Keccak content hash, media type
`application/json`, byte size in `1..65,536`, and two distinct fetch
observations whose content hashes equal that bundle hash. The bundle bytes are
RFC 8785 JCS of the schema-valid object with exactly two sorted entries;
each entry contains the exact 65-byte ECDSA signature bytes and its
`keccak256` commitment. The bundle's chain ID, registry address, `releaseId`,
`conformanceDocumentHash`, `signedDocumentHash`, attestor policy/set hashes,
and `releaseAttestationDigest` MUST equal the evidence and transaction fields,
and its entries MUST be a subset of the three
admitted signer addresses and match the two evidence commitments byte-for-byte.
The release gate fetches both
availability copies, checks the exact byte count and media type, parses the
bundle, recomputes the EIP-712 domain/struct digest, and recovers the signatures before an
authority-admin transaction is signed. A copied canonical evidence document
without this separately available bundle is incomplete and MUST NOT pass the
release gate.

JSON Schema `uniqueItems` distinguishes complete entry objects; it cannot
express cross-entry uniqueness of only the `signer` member. Schema-only
validation is therefore insufficient. The semantic checker is normative and
MUST additionally require exactly two numerically sorted unique bundle signers
drawn from the three sorted unique admitted addresses, two unique signature
commitments, exact evidence-commitment equality, and both valid recoveries;
its duplicate-signer negative deliberately remains schema-valid and then fails
the semantic gate.

The repository's deterministic detached-bundle fixture is
`specs/onchain/target-release-signature-bundle-v1.fixture.json`; it is checked
by `python -B specs/onchain/target_release_signature_bundle_check_v1.py` using
independent fixed-width secp256k1 public-key recovery. The fixture
has one normative documentation transcript, in §13.9.1. The checker parses
that marked block and compares every release/document/content hash, URI, byte
count, and observation hash directly with the fixture and reference; an
unmarked duplicate is non-normative. It MUST report `signatureRecovery=2/3`
before this vector is accepted. The separately committed
`specs/onchain/target-release-signature-bundle-v1.reference.json` is the
machine-readable availability record checked against the evidence schema.
These are conformance bytes and observations, not deployment attestations.

For avoidance of doubt, `availability` and the bundle descriptor are excluded
from `core(E)` precisely because their URIs, content hashes, and signature
bytes depend on `D0`/`D1`; they remain mandatory, independently verified
release-gate inputs. The `D0`/`D1` projection definition above supersedes any
interpretation that would hash a self-referential retrieval carrier.

Source validation is exact: `sourceCommit` is lower-case 40-hex SHA-1; the
release gate runs `git cat-file -e <sourceCommit>^{commit}`, obtains
the lower-case 40-hex output of `git rev-parse <sourceCommit>^{tree}`, decodes
its 20 bytes, right-aligns them in `bytes32` with 12 zero high bytes, compares
that exact value to `sourceTreeHash`, and hashes the required source paths from
that tree. A 20-byte value, ASCII hex bytes, left alignment, or a second hash
of the Git tree OID fails. The
source repository is exactly `6529-Collections/6529networkmuseum`; a detached
or shallow object, a missing commit/tree/path, a case or encoding mismatch, or
a source snapshot whose raw 20-byte commit does not right-align into the
on-chain `bytes32` value rejects the evidence. The two build entries require
distinct builders and toolchain identities, identical compiler-input and
runtime/artifact hashes, and runtime hashes equal to the target's direct
`extcodehash`. Availability uses the exact IPFS/Arweave grammar in §5.3; the
two URIs and fetch observations are distinct, each fetches the exact `D0` JCS
bytes, and each content hash equals `conformanceDocumentHash`. A missing, revoked,
expired, unreachable, mismatched, or superseded evidence bundle cannot be used
to admit a row.

The release gate MUST validate `git cat-file -e
<sourceCommit>^{commit}`, the exact source tree and compiler-input hashes,
two independent builds, equality of both artifact hashes and runtime
`extcodehash`, the required source paths, both threshold signatures, and
both availability observations before the authority-admin transaction is
signed. The on-chain primitive additionally checks the right-aligned SHA-1
encoding, `artifactHash == extcodehash(target)`, the fixed runtime policy,
all target probes, and the same governed 2-of-3 EIP-712 signatures supplied in
the detached bundle. The contract intentionally does not pretend to verify
GitHub, compiler, or content-addressed storage semantics from a `bytes32`;
those remain an explicit release-gate trust boundary. It does, however,
cryptographically enforce that two immutable governed attestors approved the
exact release ID, conformance-document hash, signed-document hash, policy/set
commitments, chain, and registry. A caller-supplied `expectedCodeHash`,
`evidenceHash`, unsigned `signedDocumentHash`, or unrelated signature cannot
create or bypass a release row.

The terminal `quarantineTargetRelease(targetKind, target, codeHash, reasonHash)` action
is authority-admin controlled, requires a nonzero reason hash, and changes the
current row to status `2`. Quarantine is terminal for that revision: no
authority or successor transition may reference it, and no second quarantine
event is emitted. A later admitted row must supersede it with the exact
predecessor/reason commitment above. This is the V1 revocation path; there is
no unquarantine or silent metadata edit. `TargetReleaseQuarantined` persists
the reason, prior release ID, revision, actor, and authority revision. The
current pointer, historical view, and events therefore make a mistaken row
recoverable by quarantine plus a new governed revision rather than permanently
poisoning the codehash key.

Quarantine is also a release-evidence revocation: the authority-admin release
gate records the affected evidence hash, reason hash, and revocation time in
its signed audit bundle, and the contract refuses that release ID at every
subsequent target admission, initial activation, queue, execution, and successor
check. A replacement must use a new release ID, a new conformance-document
hash, a new evidence bundle, and the exact `previousReleaseId` commitment; the
old code hash may be reused only after that new row is independently admitted.

The state view `targetRelease(targetKind, target, codeHash)` returns the current row;
`targetReleaseAtRevision(targetKind, target, codeHash, revision)` returns an immutable
historical row, and `targetReleaseById(releaseId)` is the globally unique
identity lookup. `targetReleaseDependencyCount(releaseId)` returns the stored
bounded row count and `targetReleaseDependency(releaseId,index)` returns the
exact immutable dependency row; an absent release or out-of-range index
reverts. A transition requires `status == 1`. A later EVM/toolchain revision
uses a new runtime-policy hash and a new release revision; it MUST not
reinterpret an existing row or dependency list.

The release row, source, artifact, conformance, interface, version,
compatibility, status, predecessor, and reason commitments are state and event
facts. `TargetRelease` is not an allowlist merely because an admin supplied a
hash.

Canonicalizer purity and target non-upgradeability are separate versioned
policies. `specs/onchain/canonicalizer-runtime-purity-v1.json` (hash
`0x0c0a10c923084b4861fbf9c4e869302de19ef6b103c2698263915fc56ac3461f`)
applies only to asset canonicalizers: it retains the strict state-free,
external-call-free, caller-free policy in §2.1. It MUST NOT be applied to an
authority provider or successor registry.

Every authority and successor target instead uses
`MUSEUM_TARGET_RUNTIME_NONUPGRADEABILITY_V1`, whose exact JCS document is
`specs/onchain/target-runtime-nonupgradeability-v1.json` and whose hash is
`0x95f9e52ebbfec6aa2d1ad41a516a6d9e7ce2f55cfed9de1fb906e6f6e9dae452`.
Its literal ID hash is separately `0x8148bd5ce1f57455106f3425ad39d8c0c80e527c51c51ad350f27028e8c6c367`;
`TargetRelease.runtimePolicyHash` and release evidence MUST use the governed
document hash, not that literal ID hash.
This policy permits `SLOAD`, `SSTORE`, `ADDRESS`, `CALLER`, and bounded
`STATICCALL` so a stateful successor and an authority provider can operate.
It still rejects `CALL`, `CALLCODE`, `DELEGATECALL`, `CREATE`,
`CREATE2`, and `SELFDESTRUCT`, all EOF/reserved/ambiguous instruction streams,
and declared EIP-1167, EIP-1967 implementation/beacon/admin-slot, beacon, and
diamond upgrade patterns. Thus a target has no proxy/delegatecall, creation,
self-destruct, metamorphic, or arbitrary-call upgrade path.

At admission, initial activation, queue, execution, and successor storage,
the registry MUST:

1. require nonzero code at the exact `TargetRelease.target`, size at most
   24,576 bytes, direct `extcodehash(target)` equal to `codeHash` and both
   independent build/runtime hashes, and the exact row runtime-policy hash;
2. apply the same exact Cancun decoder, PUSH-boundary rule, terminal
   definite-CBOR exclusion, reserved/EOF fail-closed behavior, and conservative
   decoded-instruction-boundary review used for canonicalizers;
3. reject every target-policy forbidden opcode and upgrade pattern, including
   unreachable executable bytes. This syntactic scan is not a reachability or
   semantic-purity proof; exact code hash, two distinct reproducible builds,
   source audit, and target-specific probes remain mandatory;
4. require the evidence's strictly sorted, unique, bounded
   `externalDependencies` list and persist every row by `releaseId`. Each row
   contains exact address, code hash, dependency runtime-policy hash, ERC-165
   interface ID, and nonzero `purposeId`; the evidence additionally carries the lower-case ASCII purpose
   label and proves `purposeId == keccak256(bytes(purpose))`. The on-chain
   order is strictly increasing lexicographically by the ABI values
   `(uint160(dependency), codeHash, runtimePolicyHash, bytes4(interfaceId),
   purposeId)`; duplicates cannot be hidden under a different purpose label.
   The on-chain
   commitment is not JCS. For every row compute
   `rowHash = keccak256(abi.encode(MUSEUM_TARGET_DEPENDENCY_ROW_DOMAIN,
   dependency, codeHash, runtimePolicyHash, interfaceId, purposeId))`, then compute
   `externalDependencyHash = keccak256(abi.encode(
   MUSEUM_TARGET_DEPENDENCY_SET_DOMAIN, rowHashes))` over the ordered
   `bytes32[]`. The contract recomputes this ABI commitment from calldata,
   stores the rows and count, and never accepts a caller hash in their place.
   The release document's D0/D1 JCS projections separately bind the complete
   human-readable list. Only declared static-call dependencies may support a
   target; the source audit and capability/probe commitments MUST account for
   each one; no undeclared external dependency may be relied on; and
5. at release admission and again before initial activation, authority
   use, authority queue/execution, and successor storage, load every persisted
   row, recompute all row/set hashes, require the exact stored purpose ID,
   require nonzero code with unchanged direct `extcodehash`, require the exact
   governed dependency-policy document hash declared by the row, run the
   complete `MUSEUM_DEPENDENCY_RUNTIME_NONPROXY_V1` scan, and bounded-call
   ERC-165 `supportsInterface(interfaceId) == true`. That dependency policy is
   independently JCS-hashed as
   `0xf8efb731af735014514f4a5b8ad22a6e2007ba23b11b45a9c8845db3f144ee2c`;
   it permits only purpose-bound immutable code and immutable storage reads,
   and rejects every external call, proxy, delegatecall, creation,
   self-destruct, mutable storage, and upgrade pattern. A zero/self dependency,
   duplicate/out-of-order row, changed code, malformed/reverting interface
   response, purpose-ID mismatch, set-hash mismatch, or more than eight rows
   reverts. The contract does not claim to prove the human purpose or off-chain
   source semantics; the release gate records that audit before an
   authority-admin transaction is signed.

The target probe calls are bounded to `TARGET_PROBE_GAS_LIMIT = 250_000` gas
per call and `TARGET_PROBE_RETURN_BYTES_LIMIT = 4_096` returned bytes. A call
that exceeds either bound, reverts, returns malformed length, or returns an
unexpected value fails the same admission primitive. These limits are part of
the runtime-policy document and the evidence schema; they are not supplied by
the target. The queue and execution phases re-run the bytecode copy, hash,
scanner, probe, and evidence-row status checks, so a same-code-hash proxy
cannot change an implementation behind an admitted target.

At queue and execution, the registry MUST set `releaseId` and
`conformanceDocumentHash` from the loaded row, then load the admitted row for the
target kind, exact `target`, and `expectedCodeHash`; require `status == 1`,
`row.target == target`, the input interface, version, runtime-policy/dependency
commitments, and `evidenceHash` to equal that row, and require the target's returned protocol
and Stream-compatibility values to equal the release row where those fields
apply. It MUST also reload and validate every dependency row and its ABI set
commitment, require `extcodehash(target) == expectedCodeHash`, and run the
complete target non-upgradeability scanner above. It then performs bounded
`staticcall`s to ERC-165 and every required probe method, checks exact return
lengths and values, and recomputes the context-bound probe and capability
commitments below. A failed call, malformed return, or changed code hash
reverts. The exact-codehash release row plus these independently recomputed
callability checks are the conformance gate; target-returned marker values or
target-supplied commitments are never accepted by themselves.

V1 pins `AUTHORITY_TIMELOCK_SECONDS = 172800` (48 hours). `setAuthority`
MUST reject an EOA, zero address, zero code hash, wrong interface ID, missing
ERC-165 support, failed probe, wrong predecessor, zero evidence hash, or a
nonzero `expectedModuleVersion`. It MUST require
an admitted `TargetRelease` under kind `MUSEUM_TARGET_KIND_AUTHORITY_V1` with
`target == target`, `codeHash == expectedCodeHash`, `requiredInterfaceId` equal to the input,
`expectedModuleVersion == bytes32(0)`, and `evidenceHash` equal to its
`conformanceDocumentHash`, `status == 1`; it MUST also require
`extcodehash(target) == expectedCodeHash`, `predecessorRegistry == address(this)`,
`isMuseumAuthorityProvider() == true`, `registry() == predecessorRegistry`,
and `authorityRevision() == authorityRevision + 1`. The exact interface probe
commitment is
`keccak256(abi.encode(MUSEUM_TARGET_PROBE_DOMAIN, releaseId, target,
expectedCodeHash, requiredInterfaceId, true, predecessorRegistry,
targetRevision, capabilityCommitment))`; the supplied `interfaceProbeHash`
MUST equal it. The target
MUST also pass the context-bound `capabilityHandshake` for
`MUSEUM_AUTHORITY_ROLE_DOMAIN_V1`, the exact closed-world
`MUSEUM_AUTHORITY_SELECTOR_SET_HASH`, and challenge
`keccak256(abi.encode(MUSEUM_AUTHORITY_CAPABILITY_DOMAIN, target,
predecessorRegistry, authorityRevision + 1, governanceExecutor,
governanceExecutorRevision))`. Its expected commitment MUST
equal
`keccak256(abi.encode(MUSEUM_AUTHORITY_CAPABILITY_DOMAIN, releaseId, target,
expectedCodeHash, predecessorRegistry, MUSEUM_AUTHORITY_ROLE_DOMAIN_V1,
MUSEUM_AUTHORITY_SELECTOR_SET_HASH, challenge, targetRevision,
governanceExecutor, governanceExecutorRevision))`,
`canAuthorize` MUST be true, and the supplied `capabilityCommitment` MUST
equal that value. The bounded staticcalls MUST return exactly the expected
booleans, addresses, revision, commitment, and `canAuthorize` value; a
malformed or reverting call fails the gate. This handshake covers the actual
required selector set and registry/role domain; it is not a marker-only probe
and grants no arbitrary call capability. The selector set is the strictly increasing numeric
`bytes4[]` `[0x3a1a0b96, 0x51b648fd, 0x51d8c5e0, 0x81a86ff4, 0x93936f62,
0x967059b8, 0xab6627c3, 0xaf2fb948, 0xc1713cf2, 0xc9dc7d0d,
0xda6d916f, 0xf0edf065]`, ABI-encoded as `address`-independent `bytes4[]`
and hashed to
`0x4c2a05297ef36555d0bd199b80df1463d02702f6bd1bde9444960279d15957e5`. It
binds authority, governance-executor, target-release admission/quarantine,
global-role, Stream owner-record-interface admission and mirror-link convergence,
HTTPS resolver-profile admission, execute, and cancel capabilities only. `freezeWrites` and
post-freeze `setSuccessor` are deliberately excluded because their emergency
authorization is the registry's direct executor binding, independent of a
mutable provider's `canAuthorize` state. It queues one complete target
and `eta = block.timestamp + AUTHORITY_TIMELOCK_SECONDS`; a second queue
requires `cancelAuthority` first.

`executeAuthority` is allowed only at or after `eta`. It MUST reload the
`TargetRelease` row and repeat every release, code-hash, ERC-165, interface,
probe, capability, evidence, predecessor, version, and target-revision check
against the stored target in the same transaction. A changed target reverts
with `AuthorityTargetChanged` and leaves the queue cancellable. On success it
changes active authority exactly once, increments `authorityRevision`, and
emits every stored target commitment. Before the write, the new provider's
capability is recomputed against the unchanged current executor
address/revision and the new authority revision. The transaction atomically
stores that same commitment and both active revisions in `AuthorityState`,
refreshes `GovernanceExecutorState.capabilityCommitment` and
`.authorityRevision`, and recomputes its `bindingCommitment` from the unchanged
executor/evidence/revision and new capability/authority revision. It emits
`GovernanceExecutorAuthorityRebound`; this refresh does not increment the
executor revision or change its original governance evidence. The governance
executor address does not move: neither the old nor new authority provider
receives a direct-call role, and ordinary registrar/migration roles are not
implicitly transferred.
`cancelAuthority` is permitted before
execution and clears the complete target without changing active authority.
The registry MUST persist the resulting `AuthorityState` and expose it through
`authorityState()` and `authorityRevision()`: authority address, direct
`extcodehash`, target-release ID and conformance-document hash, required
interface ID, interface-probe commitment,
context-bound capability commitment, evidence hash, predecessor/current
registry linkage, authority and governance-executor revisions, proposer,
proposed timestamp/block, and executed
timestamp/block. These are state facts, not event-only fields. Every use of
authority or a global role rechecks the active authority code hash, every
persisted dependency row/set commitment, and the capability handshake against
this state; a changed provider or dependency reverts. For every
provider-mediated call, `AuthorityState.governanceExecutorRevision` and
`GovernanceExecutorState.authorityRevision` MUST equal the active revisions,
both states MUST contain the same current capability commitment, and the
governance binding MUST recompute exactly. `freezeWrites` and post-freeze
`setSuccessor` use the independent emergency rule below instead.

The role-bearing executor has its own append-only binding and 48-hour
transition. `setGovernanceExecutor(newExecutor,evidenceHash,
capabilityCommitment)` is callable only by the current executor, rejects zero
or unchanged accounts and zero evidence/commitment, derives
`newRevision = governanceExecutorRevision + 1`, and permits only one pending
row. Queue, execute, and cancel all require `writesFrozen == false`; execution
of a stale or replayed pending row after freeze MUST revert even if storage is
malformed. The executor is deliberately not scanned or admitted as a TargetRelease:
it is the governance actor (for example, the Museum Safe), not code trusted as
a protocol release or a target dependency. The evidence hash identifies the
off-chain governance authorization for the account binding without asserting
its signer list or proxy status.

Before queueing, and again in `executeGovernanceExecutor`, the registry
revalidates the active authority TargetRelease, code hash, target runtime
policy, every persisted dependency row, and all bounded provider probes. It
calls the provider's existing `capabilityHandshake` with challenge
`keccak256(abi.encode(MUSEUM_AUTHORITY_CAPABILITY_DOMAIN, authority,
address(this), authorityRevision, newExecutor, newRevision))` and requires the
returned commitment to equal both the supplied/stored value and
`keccak256(abi.encode(MUSEUM_AUTHORITY_CAPABILITY_DOMAIN,
authorityReleaseId, authority, authorityCodeHash, address(this),
MUSEUM_AUTHORITY_ROLE_DOMAIN_V1, MUSEUM_AUTHORITY_SELECTOR_SET_HASH,
challenge, authorityRevision, newExecutor, newRevision))`, with
`canAuthorize == true`. Queue state stores every input, proposer, queue
timestamp/block, and `eta = block.timestamp + AUTHORITY_TIMELOCK_SECONDS`.
It also derives and stores
`bindingCommitment = keccak256(abi.encode(
MUSEUM_GOVERNANCE_EXECUTOR_BINDING_DOMAIN, newExecutor, evidenceHash,
capabilityCommitment, newRevision, authorityRevision))`; the binding domain is
the Keccak ID of the exact ASCII literal in §3.2. No caller supplies this
commitment.
Execution is callable only by the still-current executor at/after ETA. It
atomically advances the executor binding/revision, stores the new
executor-bound capability and revision in `AuthorityState`, records execution
timestamp/block, and invalidates the old executor's two derived roles without
modifying any grant row. After that write, `AuthorityState` and
`GovernanceExecutorState` MUST contain the same capability commitment and the
same authority/executor revision pair. `cancelGovernanceExecutor` is callable only by the current executor
and clears only the pending row. Every protected global call checks the current
executor address and both revisions and revalidates the active provider's
executor-bound capability; current-pointer replacement cannot reactivate an
old executor. The complete current and pending rows are exposed by
`governanceExecutorBinding()` and `pendingGovernanceExecutor()`.
Before initial activation, the current view exposes only the constructor-bound
executor/evidence at revision 1 with zero capability, binding, and authority
revision; that pre-initialization row authorizes only the one-shot activation
selector and cannot satisfy either closed global-role check.

`setSuccessor` is a one-way post-freeze transition whose input stores the same
complete target commitment. It is authorized only by the registry's direct
current governance-executor address/revision, requires `writesFrozen == true`,
and intentionally does not call the authority provider or require its
capability commitment or `canAuthorize`. It MUST reject an
EOA, zero code hash, wrong successor interface ID, missing ERC-165 support,
failed probe, an absent successor `TargetRelease`, or an input whose exact
target address, `requiredInterfaceId`, `expectedModuleVersion`, or `evidenceHash` differs from
that release row or whose `status != 1`. It MUST require
`predecessorRegistry == address(this)`, `moduleSupersedes() ==
predecessorRegistry` (and therefore exactly `address(this)`), and
`extcodehash(target) == expectedCodeHash`. It MUST reject
`expectedModuleVersion == bytes32(0)`,
`expectedModuleVersion == MUSEUM_REGISTRY_VERSION_V1`,
`registryVersion() != expectedModuleVersion`,
`protocolVersion() != MUSEUM_PROTOCOL_VERSION_V1`,
`streamCompatibilityCommit() != MUSEUM_STREAM_COMPATIBILITY_COMMIT_V1`, or a
zero evidence hash. The release row's `protocolVersion` and
`streamCompatibilityCommit` MUST equal the current V1 constants. Its
capability commitment is independently recomputed as
`keccak256(abi.encode(MUSEUM_SUCCESSOR_CAPABILITY_DOMAIN, releaseId, target,
expectedCodeHash, requiredInterfaceId, predecessorRegistry,
expectedModuleVersion, MUSEUM_PROTOCOL_VERSION_V1,
streamCompatibilityCommit, address(this),
conformanceDocumentHash))`; the supplied value MUST equal it. Its exact probe
commitment is
`keccak256(abi.encode(MUSEUM_TARGET_PROBE_DOMAIN, releaseId, target,
expectedCodeHash, requiredInterfaceId, true, predecessorRegistry,
expectedModuleVersion, MUSEUM_PROTOCOL_VERSION_V1, streamCompatibilityCommit,
address(this), capabilityCommitment))`; the supplied value MUST equal it.
Same-version targets and wrong-predecessor targets MUST fail; a new governed
module version with the same protocol/Stream compatibility and exact
predecessor MAY pass. Every successor staticcall and commitment is repeated
immediately before storing the target; no target-returned marker or
caller-supplied evidence can substitute for the release row.
The contract rechecks the target immediately before storing it; a change
reverts with `SuccessorTargetChanged`. The stored successor target and
`SuccessorSet` event include address, expected code hash, release ID,
conformance-document hash, interface ID/probe, capability, predecessor,
version, evidence hash, authority revision, proposer, and commit time.
`freezeWrites` is an immediate, one-way transition authorized only by the
registry's direct current governance-executor address/revision. It MUST NOT
call the authority provider, load provider `canAuthorize`, or require the
provider-bound capability commitment; this independence is the emergency
recovery invariant. It cancels any pending authority and
governance-executor queues, emitting their cancellation events before
`WritesFrozen`,
blocks record, schema, profile, type, family-grant, global-role, target-release,
convergence, and authority-transition mutators, and leaves read selectors plus the single
post-freeze `setSuccessor` transition available. A second freeze reverts.
`WritesFrozen` records the active authority, successor, and authority
revision. No selector may bypass these guards through an alternate overload.
V1 is non-proxy and non-delegatecall; deployment behind an upgradeable proxy
or an implementation with an unguarded transition selector fails the
deployment gate. There is no emergency authority rollback or timelocked
bypass: before execution, `cancelAuthority` is the only rollback; after
execution, governance must queue another fully probed target. An emergency
response is `freezeWrites` followed by the validated successor transition.

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
    uint8 authorizationClass,
    uint64 familyRevision,
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
MuseumRecordWrite(bytes32 recordHash,bytes32 recordType,bytes32 subjectId,bytes32 previousRecordHash,uint8 authorizationClass,uint64 familyRevision,uint256 nonce,uint64 deadline)
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
`isValidSignature(bytes32,bytes)`. Every ERC-1271 path accepts only a successful
call returning exactly `0x1626ba7e`; reverts, malformed/short/long return data,
empty data, and all other values are invalid.

Every V1 signature path that can call ERC-1271 (`recordMuseumRecordBySig`,
`revokeNonceBySig`, and `recordHttpsAssertionBySig` when its signer is a
contract) is protected by one full-call `nonReentrant` guard. The guard starts
at external-function entry and ends only after the final state write, so an
`isValidSignature` callback cannot call `setRecordFamilyGrant`,
`setGlobalRoleGrant`, a profile/family/type mutator, a record mutator, a nonce
mutator, or any authority/freeze/convergence mutator on this registry.

Before the callback, the registry snapshots every authorization dependency
used by that path. A record write snapshots `writesFrozen`, registry address
and version, active authority revision/code hash/capability commitment, the
unique record-type mapping,
family kind/bitmap/revision, the exact family grant enabled/revision, lane
head/revision, and signer nonce/revocation state. A nonce revocation snapshots
`writesFrozen`, registry address/version, active authority revision/code hash/
capability commitment, and the
signer nonce/revocation state. An HTTPS assertion snapshots `writesFrozen`,
registry address/version, active authority revision, resolver profile and
revision, attestor, the exact HTTPS global-role grant/revision, active authority
code hash/capability commitment, URI/current
assertion pointer and revision/predecessor, submitted assertion revision,
nonce/deadline, signer nonce/revocation state, and address-set commitment. A
path MUST NOT
read an authorization dependency before the callback and assume it remains
valid merely because the callback returned successfully.

After the callback, the registry re-reads and revalidates those snapshots in
this deterministic order: (1) freeze flag, registry address/version, active
authority revision/code hash/capability commitment; (2) record type/family or
resolver-profile state;
(3) global-role or family-grant state; (4) URI/current assertion state where
applicable; (5) lane head; and (6) nonce/revocation state. Any mismatch MUST
revert with the applicable specific error or
`AuthorizationDependencyChanged(bytes32,bytes32,bytes32)`. The registry then
re-runs the same writer/profile authorization primitive immediately before
consuming the nonce or recording the assertion. All nonce consumption, record
or assertion state, and events occur after this final validation. A failed
callback, failed revalidation, or later check reverts the complete EVM call;
no Museum state or event from that call is committed.

EOA signature paths perform the same final authorization checks without an
external callback. Only after these checks does the registry consume the nonce
and append the record, persist the revocation, or record the HTTPS assertion.

Nonces are unordered and scoped to the signer. A used or revoked nonce cannot
be reused. Deadlines are inclusive: `block.timestamp <= deadline` is
required. The signer MAY revoke a nonce directly or through a valid
revocation signature. Authority rotation does not rewrite old records; the
record retains the exact `familyId`, record-type-policy revision, family
revision, family-grant revision, class, signer, and role/provider revision
observed at write time. The relayed ABI supplies
`authorizationClass` and `familyRevision` explicitly; the contract compares
both to the unique record-type mapping and current family state before calling
`requireRecordWriter`.

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
        bytes32 authorizationFamilyId;
        uint64 recordTypePolicyRevision;
        uint64 familyRevision;
        uint64 grantRevision;
        uint8 payloadMode;
        bytes32 supersedesRecordHash;
        uint32 payloadLength;
        bytes32 httpsAssertionHash;
        uint64 httpsResolverRevision;
        uint64 authorityRevision;
    }

    struct ExternalAsset {
        bytes32 subjectId;
        bytes32 assetProfileId;
        bytes32 canonicalAssetIdHash;
        string canonicalAssetId;
        uint64 registeredAt;
        address registrar;
        bytes32 authorizationRoleId;
        uint64 authorityRevision;
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
        bytes32 canonicalizerConformanceInputHash;
        uint64 revision;
    }

    struct StreamMirrorLink {
        address streamCore;
        address ownerRecordModule;
        uint256 collectionId;
        uint256 collectionSerial;
        uint256 tokenId;
        bytes32 streamSubjectId;
        bytes32 ownerRecordHash;
        bytes32 ownerRecordHashDomain;
        bytes32 ownerRecordHashVectorId;
        uint64 revision;
        bytes32 authorizationRoleId;
        uint64 authorityRevision;
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
        address streamCore;
        bytes32 streamCoreCodeHash;
        address interfaceModule;
        bytes32 interfaceModuleCodeHash;
        bytes32 ownerRecordHashDomain;
        bytes32 ownerRecordHashVectorId;
        bytes32 evidenceHash;
        uint64 revision;
        bytes32 authorizationRoleId;
        uint64 authorityRevision;
    }

    struct GlobalRoleGrant {
        bool enabled;
        uint64 revision;
        uint64 authorityRevision;
    }

    struct RecordFamily {
        bool admitted;
        uint8 familyKind;
        uint16 allowedClassBitmap;
        uint64 revision;
        uint64 authorityRevision;
    }

    struct TargetDependency {
        address dependency;
        bytes32 codeHash;
        bytes32 runtimePolicyHash;
        bytes4 interfaceId;
        bytes32 purposeId;
    }

    struct TargetRelease {
        bool admitted;
        uint8 targetKind;
        address target;
        bytes32 releaseId;
        bytes32 codeHash;
        bytes32 runtimePolicyHash;
        bytes32 releaseAttestorPolicyHash;
        bytes32 releaseAttestorSignerSetHash;
        bytes32 externalDependencyHash;
        uint8 externalDependencyCount;
        bytes32 sourceCommit;
        bytes32 sourceTreeHash;
        bytes32 artifactHash;
        bytes32 conformanceDocumentHash;
        bytes32 signedDocumentHash;
        bytes32 releaseAttestationDigest;
        address releaseAttestor0;
        address releaseAttestor1;
        bytes32 releaseSignatureCommitment0;
        bytes32 releaseSignatureCommitment1;
        bytes32 releaseSignatureSetHash;
        bytes4 requiredInterfaceId;
        bytes32 expectedModuleVersion;
        bytes32 protocolVersion;
        bytes32 streamCompatibilityCommit;
        uint64 revision;
        uint64 authorityRevision;
        uint8 status;
        bytes32 previousReleaseId;
        bytes32 supersessionReasonHash;
    }

    struct TargetReleaseInput {
        uint8 targetKind;
        address target;
        bytes32 releaseId;
        bytes32 codeHash;
        bytes32 runtimePolicyHash;
        bytes32 releaseAttestorPolicyHash;
        bytes32 releaseAttestorSignerSetHash;
        TargetDependency[] externalDependencies;
        bytes32 sourceCommit;
        bytes32 sourceTreeHash;
        bytes32 artifactHash;
        bytes32 conformanceDocumentHash;
        bytes32 signedDocumentHash;
        address[] releaseAttestors;
        bytes[] releaseAttestorSignatures;
        bytes4 requiredInterfaceId;
        bytes32 expectedModuleVersion;
        bytes32 protocolVersion;
        bytes32 streamCompatibilityCommit;
        bytes32 previousReleaseId;
        bytes32 supersessionReasonHash;
    }

    struct TransitionTargetInput {
        address target;
        bytes32 expectedCodeHash;
        bytes4 requiredInterfaceId;
        bytes32 interfaceProbeHash;
        bytes32 capabilityCommitment;
        address predecessorRegistry;
        bytes32 expectedModuleVersion;
        bytes32 evidenceHash;
    }

    struct TransitionTarget {
        address target;
        bytes32 expectedCodeHash;
        bytes32 releaseId;
        bytes32 conformanceDocumentHash;
        bytes4 requiredInterfaceId;
        bytes32 interfaceProbeHash;
        bytes32 capabilityCommitment;
        address predecessorRegistry;
        bytes32 expectedModuleVersion;
        bytes32 evidenceHash;
        uint64 authorityRevision;
        address proposer;
        uint64 queuedAt;
        uint64 queuedBlock;
        uint64 eta;
    }

    struct AuthorityState {
        address authority;
        bytes32 authorityCodeHash;
        bytes32 authorityReleaseId;
        bytes32 authorityConformanceDocumentHash;
        bytes4 requiredInterfaceId;
        bytes32 interfaceProbeHash;
        bytes32 capabilityCommitment;
        bytes32 evidenceHash;
        address predecessorRegistry;
        address currentRegistry;
        uint64 authorityRevision;
        uint64 governanceExecutorRevision;
        address proposer;
        uint64 proposedAt;
        uint64 proposedBlock;
        uint64 executedAt;
        uint64 executedBlock;
    }

    struct GovernanceExecutorState {
        address executor;
        bytes32 evidenceHash;
        bytes32 capabilityCommitment;
        bytes32 bindingCommitment;
        uint64 revision;
        uint64 authorityRevision;
        address proposer;
        uint64 queuedAt;
        uint64 queuedBlock;
        uint64 eta;
        uint64 executedAt;
        uint64 executedBlock;
    }

    struct ResolverProfile {
        bool admitted;
        bytes32 documentHash;
        address attestor;
        uint64 minTtl;
        uint64 maxTtl;
        uint64 revision;
        uint64 authorityRevision;
    }

    struct HttpsAssertion {
        bytes32 uriHash;
        bytes32 hostHash;
        bytes32 resolverProfileId;
        uint64 resolverRevision;
        bytes32 resolvedAddressSetHash;
        address[] sortedUniqueAddresses;
        uint64 assertionRevision;
        bytes32 previousAssertionHash;
        uint64 issuedAt;
        uint64 expiresAt;
        address attestor;
        uint256 nonce;
        uint64 deadline;
        bytes32 assertionHash;
        bytes32 signatureCommitment;
        uint64 authorityRevision;
    }

    function isNetworkMuseumRegistry() external pure returns (bool);
    function registryVersion() external pure returns (bytes32);
    function protocolVersion() external pure returns (bytes32);
    function streamCompatibilityCommit() external pure returns (bytes32);
    function moduleSupersedes() external view returns (address);
    function authority() external view returns (address);
    function authorityRevision() external view returns (uint64);
    function authorityState() external view returns (AuthorityState memory);
    function governanceExecutor() external view returns (address);
    function governanceExecutorRevision() external view returns (uint64);
    function governanceExecutorBinding() external view returns (GovernanceExecutorState memory);
    function pendingGovernanceExecutor() external view returns (GovernanceExecutorState memory);
    function initializationState() external view returns (uint8);
    function initialAuthorityArtifactCommitment() external view returns (bytes32);
    function releaseAttestorPolicyHash() external view returns (bytes32);
    function releaseAttestorSignerSetHash() external view returns (bytes32);
    function releaseAttestorSigner(uint256 index) external view returns (address);
    function successor() external view returns (address);
    function writesFrozen() external view returns (bool);
    function pendingAuthority() external view returns (TransitionTarget memory);
    function successorTarget() external view returns (TransitionTarget memory);

    function externalAssetSubjectId(bytes32 assetProfileId, string calldata canonicalAssetId)
        external pure returns (bytes32);
    function registerExternalAsset(bytes32 assetProfileId, string calldata canonicalAssetId,
        bytes32 expectedSubjectId)
        external returns (bytes32 subjectId);
    function externalAsset(bytes32 subjectId) external view returns (ExternalAsset memory);

    function admitAssetProfile(bytes32 profileId, bytes32 schemaId, bytes32 documentHash,
        string calldata uri, address canonicalizer, uint8 canonicalizerMode,
        bytes32 canonicalizerCodeHash, bytes32 canonicalizerImplementationHash,
        bytes32 canonicalizerVersionId, string calldata conformanceInput)
        external;
    function assetProfile(bytes32 profileId)
        external view returns (AssetProfile memory);
    function admitSchema(bytes32 schemaId, bytes32 documentHash, string calldata uri,
        bool payloadRequired) external;
    function schema(bytes32 schemaId)
        external view returns (bool admitted, bytes32 documentHash, string memory uri,
            bool payloadRequired, uint64 revision);
    function admitRecordFamily(bytes32 familyId, uint8 familyKind, uint16 allowedClassBitmap)
        external;
    function recordFamily(bytes32 familyId)
        external view returns (RecordFamily memory);
    function admitRecordType(bytes32 recordType, bytes32 familyId, bytes32 schemaId,
        uint8 authorizationClass)
        external;
    function recordTypePolicy(bytes32 recordType)
        external view returns (bytes32 familyId, bytes32 schemaId, uint8 authorizationClass,
            bool admitted, uint64 revision, uint64 authorityRevision);
    function admitTargetRelease(uint8 targetKind, address target, bytes32 releaseId, bytes32 codeHash,
        bytes32 runtimePolicyHash, bytes32 releaseAttestorPolicyHash,
        bytes32 releaseAttestorSignerSetHash,
        TargetDependency[] calldata externalDependencies, bytes32 sourceCommit,
        bytes32 sourceTreeHash, bytes32 artifactHash, bytes32 conformanceDocumentHash,
        bytes32 signedDocumentHash, address[] calldata releaseAttestors,
        bytes[] calldata releaseAttestorSignatures,
        bytes4 requiredInterfaceId, bytes32 expectedModuleVersion,
        bytes32 protocolVersion, bytes32 streamCompatibilityCommit,
        bytes32 previousReleaseId, bytes32 supersessionReasonHash) external;
    function targetRelease(uint8 targetKind, address target, bytes32 codeHash)
        external view returns (TargetRelease memory);
    function targetReleaseAtRevision(uint8 targetKind, address target, bytes32 codeHash, uint64 revision)
        external view returns (TargetRelease memory);
    function targetReleaseById(bytes32 releaseId) external view returns (TargetRelease memory);
    function targetReleaseDependencyCount(bytes32 releaseId) external view returns (uint256);
    function targetReleaseDependency(bytes32 releaseId, uint256 index)
        external view returns (TargetDependency memory);
    function quarantineTargetRelease(uint8 targetKind, address target, bytes32 codeHash, bytes32 reasonHash)
        external;
    function setRecordFamilyGrant(bytes32 familyId, uint8 authorizationClass, address account, bool enabled)
        external;
    function recordFamilyGrant(bytes32 familyId, uint8 authorizationClass, address account)
        external view returns (bool enabled, uint64 revision, uint64 authorityRevision);
    function activateInitialAuthority(TargetReleaseInput calldata release,
        TransitionTargetInput calldata target) external;
    function setAuthority(TransitionTargetInput calldata target) external;
    function executeAuthority() external;
    function cancelAuthority() external;
    function setGovernanceExecutor(address newExecutor, bytes32 evidenceHash,
        bytes32 capabilityCommitment) external;
    function executeGovernanceExecutor() external;
    function cancelGovernanceExecutor() external;
    function setGlobalRoleGrant(bytes32 globalRoleId, address account, bool enabled) external;
    function globalRoleGrant(bytes32 globalRoleId, address account)
        external view returns (GlobalRoleGrant memory);
    function admitHttpsResolverProfile(bytes32 profileId, bytes32 documentHash,
        address attestor, uint64 minTtl, uint64 maxTtl) external;
    function resolverProfile(bytes32 profileId)
        external view returns (ResolverProfile memory);
    function recordHttpsAssertionBySig(string calldata canonicalURI, bytes32 hostHash,
        bytes32 resolverProfileId, uint64 resolverRevision,
        bytes32 resolvedAddressSetHash, uint64 assertionRevision,
        bytes32 previousAssertionHash, uint64 issuedAt, uint64 expiresAt,
        address attestor, uint256 nonce, uint64 deadline,
        address[] calldata sortedUniqueAddresses, bytes calldata signature) external;
    function httpsAssertion(bytes32 uriHash, bytes32 resolverProfileId,
        uint64 resolverRevision, uint64 assertionRevision)
        external view returns (HttpsAssertion memory);
    function currentHttpsAssertion(bytes32 uriHash)
        external view returns (HttpsAssertion memory);
    function httpsAssertionByHash(bytes32 assertionHash)
        external view returns (HttpsAssertion memory);
    function admitStreamOwnerRecordInterface(address streamCore, bytes32 streamCoreCodeHash,
        address interfaceModule, bytes32 interfaceModuleCodeHash,
        bytes32 ownerRecordHashDomain, bytes32 ownerRecordHashVectorId, bytes32 evidenceHash)
        external;
    function streamOwnerRecordInterface()
        external view returns (StreamOwnerRecordInterface memory);
    function streamOwnerRecordInterfaceAtRevision(uint64 revision)
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
        uint8 authorizationClass,
        uint64 familyRevision,
        uint256 nonce,
        uint64 deadline,
        bytes calldata signature,
        uint8 payloadMode,
        bytes32 supersedesRecordHash,
        bytes calldata payload
    ) external returns (bytes32 recordHash);
    function recordMuseumRecordBatch(RecordInput[] calldata inputs, bytes32 batchId)
        external returns (bytes32[] memory recordHashes);
    function batchIdUsed(bytes32 batchId) external view returns (bool);
    function batchCommitment(bytes32 batchId) external view returns (bytes32);

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

    function setStreamMirrorLink(bytes32 subjectId, uint256 tokenId,
        bytes32 expectedOwnerRecordHash) external;
    function streamMirrorLink(bytes32 subjectId)
        external view returns (StreamMirrorLink memory);

    function revokeNonce(uint256 nonce) external;
    function revokeNonces(uint256[] calldata nonces) external;
    function revokeNonceBySig(address signer, uint256 nonce, uint64 deadline, bytes calldata signature)
        external;
    function nonceRevocation(address signer, uint256 nonce)
        external view returns (NonceRevocation memory);
    function setSuccessor(TransitionTargetInput calldata target) external;
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
5. Load the record type's unique `(familyId, authorizationClass)` mapping and
   current family revision. Require the supplied `authorizationClass` and
   `familyRevision` to equal those values, then call the same
   `requireRecordWriter(familyId, authorizationClass, signer)` primitive used
   by direct writes.
6. Apply the same explicit `payloadMode`/`INLINE` profile, byte-cap,
   zero-payload, URI, and
   `PayloadDigestMismatch`/`InlinePayloadProfileMismatch` checks required by
   §5.2 for `recordMuseumRecordWithPayload` to the `payload` argument. A
   relayer MUST NOT be able to attach bytes that do not match the signed
   envelope.
7. Construct the EIP-712 struct using the exact `signedRecordHash`,
   `record.recordType`, `record.subjectId`, exact
   `signedPreviousRecordHash`, `authorizationClass`, `familyRevision`, `nonce`,
   and `deadline` arguments.
   `payloadMode` and `supersedesRecordHash` are not duplicate EIP-712 fields;
   they are cryptographically covered by the recomputed `signedRecordHash`
   and therefore by the signed `recordHash` field.
8. Snapshot all authorization dependencies listed in §6.2, call the EOA or
   ERC-1271 verifier, and re-read every snapshot in the deterministic order
   specified there. Re-run `requireRecordWriter` after the callback and revert
   on any lane, nonce, family, grant, authority, freeze, or registry change.
   Only then consume the signer-scoped nonce and append the record.

The contract MUST NOT derive a digest from one record/predecessor pair while
storing another. `SignedRecordHashMismatch` and
`SignedPreviousRecordHashMismatch` are distinct failure cases.

Direct and batch writes MUST derive the same unique class and current family
revision from `recordType`, then call
`requireRecordWriter(familyId, authorizationClass, msg.sender)`. They MUST NOT
choose among a family bitmap at call time. A Stream-family record type can
therefore authorize only its one pinned Stream class, even when the family
bitmap admits several Stream classes for other record types.

`recordMuseumRecordBatch` is all-or-nothing, has a hard maximum of
`MAX_BATCH_RECORDS` records, and advances each lane in input order. The sum of
`INLINE` payload bytes MUST obey `MAX_BATCH_INLINE_PAYLOAD_BYTES` and each
record MUST obey `MAX_INLINE_PAYLOAD_BYTES`. Each `RecordInput` supplies its
explicit `payloadMode` and `supersedesRecordHash`; neither is inferred from
the payload bytes. At entry it snapshots the active `authorityRevision`,
computes the exact `batchCommitment` in §5.2, and persists
`batchId -> batchCommitment` only in the atomic success path. `batchId` is an
audit label and MUST be emitted; it is not part of any record hash. The
deterministic count/inline-byte/gas limits and duplicate-ID semantics in §5.2
apply. A retry after a reorg is
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
| `0xc1713cf2` `setStreamMirrorLink(bytes32,uint256,bytes32)` | Enabled global registrar or migration-admin grant, or the direct current governance-executor closed binding during the convergence-gate action; never a governance-executor grant row | The Museum subject MUST be the registered CAIP-19 identity for the exact chain/Core/token tuple; the link is write-once; Core and adapter independently agree on collection identity, while module/subject/hash/domain/vector values are runtime-checked and read back. |
| `0x51b648fd` `admitStreamOwnerRecordInterface(address,bytes32,address,bytes32,bytes32,bytes32,bytes32)` | Direct current governance executor plus active authority/provider capability | The evidence hash, exact Stream core and adapter addresses/runtime hashes, owner-record domain/vector, and pinned Stream commit are recorded before any mirror link can be set. |
| `0xaf2fb948` `admitHttpsResolverProfile(bytes32,bytes32,address,uint64,uint64)` | Direct current governance executor under the closed authority-admin binding plus active authority/provider capability | Profile ID is write-once; attestor, TTL bounds, profile revision, and authority revision are stored before any assertion. |
| `0x1e0c9fe6` `recordHttpsAssertionBySig(string,bytes32,bytes32,uint64,bytes32,uint64,bytes32,uint64,uint64,address,uint256,uint64,address[],bytes)` | Valid EIP-712 signature from the resolver profile's attestor with enabled HTTPS-attestor role | Canonical URI/host, current resolver revision, signer nonce/deadline, monotone assertion revision/predecessor, sorted bounded ABI address-set hash, routability, TTL, assertion hash, and signature commitment are recomputed on-chain. |
| `0x29f319b0` `recordMuseumRecord((bytes32,bytes32,(uint16,bytes,bytes32),string,bytes32,bytes32,(uint16,bytes,bytes32),uint64),bytes32,uint8,bytes32)` and the payload/by-signature/batch write selectors | `requireRecordWriter(familyId, authorizationClass, signer)` using the record type's unique class and current family revision; `bySig` additionally requires a valid signer and signed class/revision | Subject pollution is prevented by record-type policy: external-asset identity records require a previously registered subject, and every other subject namespace requires an admitted schema/profile. |
| `0x20f3cc85` `recordMuseumRecordBySig((bytes32,bytes32,(uint16,bytes,bytes32),string,bytes32,bytes32,(uint16,bytes,bytes32),uint64),bytes32,bytes32,bytes32,address,uint8,uint64,uint256,uint64,bytes,uint8,bytes32,bytes)` | Same family writer primitive as direct writes plus valid relayed signature | `authorizationClass` and `familyRevision` are signed and must equal the unique record-type mapping/current family state. |
| `0xab6627c3` `setGlobalRoleGrant(bytes32,address,bool)` | Direct current governance executor under the closed authority-admin binding and active authority | The role ID is closed-world; the two executor-derived role IDs reject mutation; each ordinary change increments the role revision and records both control revisions. |
| `0x5e798174` `activateInitialAuthority((uint8,address,bytes32,bytes32,bytes32,bytes32,bytes32,(address,bytes32,bytes32,bytes4,bytes32)[],bytes32,bytes32,bytes32,bytes32,bytes32,address[],bytes[],bytes4,bytes32,bytes32,bytes32,bytes32,bytes32),(address,bytes32,bytes4,bytes32,bytes32,address,bytes32,bytes32))` | Constructor-bound initial governance executor, only at initialization state `0`; no authority-provider call authorizes the caller | Sets state `1` before any external call, verifies the constructor-pinned address-independent artifact commitment and the complete registry/address-bound 2-of-3 release, admits that first release, establishes both authority/executor bindings atomically, sets state `2` last, and can never execute again. |
| `0x93936f62` `admitTargetRelease(uint8,address,bytes32,bytes32,bytes32,bytes32,bytes32,(address,bytes32,bytes32,bytes4,bytes32)[],bytes32,bytes32,bytes32,bytes32,bytes32,address[],bytes[],bytes4,bytes32,bytes32,bytes32,bytes32,bytes32)` | Direct current governance executor under the closed authority-admin binding and active authority before freeze | The release history is append-only; dependency rows are persisted and ABI-committed; the registry recomputes the release identity and chain/address-bound EIP-712 digest, then requires two sorted governed signers and valid signatures before storing the row. |
| `0x85968ef0` `targetRelease(uint8,address,bytes32)` / `0x288b2e93` `targetReleaseAtRevision(uint8,address,bytes32,uint64)` / `0xb9bc97a1` `targetReleaseById(bytes32)` / `0x1dcd55b2` `targetReleaseDependencyCount(bytes32)` / `0x1efe53c1` `targetReleaseDependency(bytes32,uint256)` / `0xda6d916f` `quarantineTargetRelease(uint8,address,bytes32,bytes32)` | Historical reads for any caller / quarantine by direct current governance executor under the closed authority-admin binding and active authority before freeze | The historical row and dependency rows are immutable; address A evidence cannot authorize identical code at address B; quarantine is terminal with a nonzero reason and a new governed revision is required. |
| `0x81a86ff4` `setAuthority((address,bytes32,bytes4,bytes32,bytes32,address,bytes32,bytes32))` (`TransitionTargetInput`) | Direct current governance executor under the closed authority-admin binding and active authority | Queues a 48-hour contract-only authority-provider transition with code hash, ERC-165/interface probe, executor-bound capability commitment, predecessor linkage, zero expected module version, evidence hash, authority revision, proposer, and time. |
| `0xc9dc7d0d` `executeAuthority()` / `0xf0edf065` `cancelAuthority()` | Direct current governance executor | Execute requires the stored ETA; cancel clears only the pending provider transition. Both are blocked after freeze. |
| `0x3a1a0b96` `setGovernanceExecutor(address,bytes32,bytes32)` / `0x967059b8` `executeGovernanceExecutor()` / `0x51d8c5e0` `cancelGovernanceExecutor()` | Direct current governance executor | Queue/cancel/execute the separate 48-hour account binding; every phase binds the exact new account/revision to the active provider capability. The account is not a TargetRelease or dependency. |
| `0x43dd6c37` `setSuccessor((address,bytes32,bytes4,bytes32,bytes32,address,bytes32,bytes32))` (`TransitionTargetInput`) | Direct current governance executor; no authority-provider authorization or capability call | Requires frozen writes, no prior successor, a strictly new expected module version, and immediate repeat validation of the complete successor target commitment; one-way. |
| `0x05d53fba` `freezeWrites()` | Direct current governance executor; no authority-provider authorization or capability call | Immediate and one-way; cancels pending authority and executor transitions and blocks all mutators except post-freeze `setSuccessor`. |
| `0x63d20b1a` `admitRecordFamily(bytes32,uint8,uint16)` / `0x46a9f249` `admitRecordType(bytes32,bytes32,bytes32,uint8)` | Active authority plus explicitly admitted metadata/admin scope | Family kind and bitmap are constrained; each type selects exactly one class. |
| `0xea2792ce` `admitAssetProfile(bytes32,bytes32,bytes32,string,address,uint8,bytes32,bytes32,bytes32,string)`, `admitSchema`, `setRecordFamilyGrant` | Active authority plus their explicitly admitted metadata/admin scope; never an unqualified family grant | Admission is append-only; the asset-profile path executes the bounded conformance input; a new document or policy revision gets a new revision and cannot silently broaden a prior grant. |

Every concrete selector in this table, including the canonical tuple forms for
`TransitionTargetInput` and `CollectionRecord`, MUST be golden-tested against
the exact ABI in §7. A display alias such as `setAuthority(TransitionTargetInput)`
MUST NOT be passed to a selector calculator. The reproducible selector
transcript in `notes/research/external-registry-review.md` is a conformance
fixture; changing any parameter order, tuple member, or type requires a new
selector review and a new ABI version.

The canonical asset string is profile output, not caller interpretation. The
admitted profile MUST name a governance-approved canonicalizer with
`canonicalizerMode == 0`, an exact nonzero runtime `canonicalizerCodeHash`, a
nonzero `canonicalizerVersionId`, and a zero
`canonicalizerImplementationHash`. `admitAssetProfile` additionally requires a
nonempty governance-reviewed `conformanceInput` no longer than
`MAX_CANONICAL_ASSET_ID_BYTES`, executes the exact bounded fixed-point check,
and persists its hash. `admitAssetProfile` and every external
asset registration MUST perform the exact immutable-runtime code-size,
`extcodehash`, forbidden-opcode scan, and static canonicalizer-call checks in
§2.1. A code hash that changes, a proxy opcode, or a mutable/environmental
opcode is a hard failure; there is no EIP-1967 mode in V1. The version ID is
bound to the admitted code hash in the profile document and is never obtained
from the target contract. Registration calls the canonicalizer in a read-only
call with exactly `CANONICALIZER_CALL_GAS_LIMIT`, checks `returndatasize` before
copying, rejects more than `MAX_CANONICALIZER_RETURN_DATA_BYTES`, and MUST
require byte-for-byte equality between its canonical ABI-string result and the
supplied string. The string MUST be nonempty, at most
`MAX_CANONICAL_ASSET_ID_BYTES`, and UTF-8 without leading/trailing whitespace or
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
string reverts with `SubjectIdCollision`. The state and event MUST persist the
actual enabled global role ID used by `msg.sender` and the active
`authorityRevision`; a later role rotation never rewrites this registration.

`setStreamMirrorLink` is also not an untrusted assertion channel. It requires
an existing Museum external-asset subject and an admitted
`streamOwnerRecordInterface` whose
convergence evidence is anchored to the pinned Stream compatibility commit.
The caller supplies only that Museum subject, the Stream token ID, and an
`expectedOwnerRecordHash` substitution guard. The contract loads the admitted
core/module/domain/vector, rechecks both direct runtime hashes, and performs
bounded exact-length staticcalls to `streamCore()`,
`ownerRecordHashDomain()`, `ownerRecordHashVectorId()`, and
`ownerRecordBinding(tokenId)` on the adapter and
`tokenCollectionIdentity(tokenId)` plus `tokenLifecycle(tokenId)` directly on
the Core. It requires the
adapter's core/domain/vector to equal the admitted row; the Core call to return
exactly 128 bytes, `mappingExists == true`, `burned == false`, and nonzero
collection ID and collection serial; the lifecycle call to return exactly 32
bytes whose canonical `uint8` value is `MINTED (2)`; and the adapter's 96-byte binding return
to contain that exact Core-read collection ID. It derives
`keccak256(abi.encode(STREAM_SUBJECT_TOKEN_V1, uint256(block.chainid),
streamCore, uint256(tokenId)))`, and requires the adapter-returned subject to
equal that derivation.

The registry also reconstructs the exact ASCII external-asset identity
`eip155:<block.chainid>/erc721:<40-lowercase-hex-streamCore>/<tokenId>` using
canonical decimal integers without leading zeroes. It requires the stored
`ExternalAsset` row for `subjectId` to use
`MUSEUM_ASSET_PROFILE_CAIP19_V1`, contain that exact string and its
`keccak256(bytes(...))`, and have
`subjectId == externalAssetSubjectId(MUSEUM_ASSET_PROFILE_CAIP19_V1,
canonicalAssetId)`. This is an equality check against the already registered
identity, not a second registration or caller-provided alias. The owner-record
hash must be nonzero and equal the caller's expected value. The registry stores
only these independently checked/read-back values; no Museum subject, Stream
core, module, collection, Stream subject, hash domain, or vector is
caller-selected.

The link is immutable and one-per-subject in V1; the contract MUST NOT
silently replace it after a source transfer or owner-record revision. A later
source revision is a new Museum evidence record, not a mutation of this link.
The state and event MUST persist the actual enabled global role ID used by
`msg.sender` and the active `authorityRevision`. Negative conformance vectors
MUST reject substituted core/module code, collection, derived subject,
owner-record hash, domain, vector, expected hash, swapped Museum subject or
CAIP-19 identity, absent/burned Core token identity, zero collection serial,
truncated adapter/Core return data, and a changed readback between admission
and link creation.

`admitHttpsResolverProfile` is authority-controlled and append-only. It MUST
reject a zero attestor, zero or inverted TTL bounds, and a profile ID already
admitted; each admission increments `revision` and records the active
`authorityRevision`. `recordHttpsAssertionBySig` is the only V1 assertion
writer. It recomputes the canonical URI/host hashes, sorted address-set hash,
EIP-712 digest, assertion hash, and signature commitment; requires the
profile's exact current revision and attestor role; and stores the complete
`HttpsAssertion` under the exact `assertionKey` above. It also updates
`currentHttpsAssertion[uriHash]` only when the assertion is valid now and has
the required next revision and predecessor. This is a per-URI registry: the
canonical URI path is part of `uriHash`, so each distinct path needs a distinct
signed assertion even when the host and resolved address set are unchanged.
`hostHash` is recomputed from the exact canonical URI and is checked as a
redundant field, never used as a host-wide wildcard. The canonical assertion
payload and EIP-712 type string are exactly the 12-field form shown above; an
older 8-field form is not a V1 encoding and MUST be rejected.

Every record path calls `requireCurrentHttpsAssertion` after URI validation.
For a non-HTTPS URI it stores zero assertion hash/revision. For HTTPS it
recomputes `uriHash` and `hostHash` from the exact record URI, requires the
current pointer keyed by that `uriHash`, `block.timestamp >= issuedAt`,
`block.timestamp <= expiresAt`, admitted profile, equal profile revision,
equal URI/host hashes, and valid address-set commitment; it then stores and
emits the assertion hash and resolver revision in `RecordSummary` and
`MuseumRecordRecorded`. Expiry or profile revision change does not mutate old
records and forces a new assertion association on the next write.

A state-only auditor MUST dereference `RecordSummary.httpsAssertionHash` with
`httpsAssertionByHash`, verify that the returned stored `HttpsAssertion` has
the same `assertionHash`, and verify its stored `resolverProfileId` and
`resolverRevision` (the latter equals `RecordSummary.httpsResolverRevision`);
the auditor MUST also recompute `keccak256(abi.encode(sortedUniqueAddresses))`
from the returned immutable array and rerun its ordering, uniqueness, and
routability checks against the stored `resolvedAddressSetHash`;
replacing `currentHttpsAssertion[uriHash]`, including across profiles, cannot
change an old record's assertion context.

### 7.1 Required errors

The V1 implementation MUST define and use these custom errors (arguments are
normative):

```solidity
error InvalidAssetProfile(bytes32 profileId);
error AssetProfileAlreadyAdmitted(bytes32 profileId);
error InvalidCanonicalAssetId(bytes32 profileId);
error InvalidCanonicalizer(bytes32 profileId, address canonicalizer);
error InvalidCanonicalizerCodeHash(bytes32 profileId, bytes32 expected, bytes32 actual);
error CanonicalizerRuntimeMutable(bytes32 codeHash, uint8 opcode, uint256 offset);
error CanonicalizerRuntimeInvalid(bytes32 codeHash);
error CanonicalAssetIdTooLarge(uint256 supplied, uint256 maximum);
error CanonicalizerCallFailed(bytes32 profileId);
error CanonicalizerReturnDataTooLarge(uint256 supplied, uint256 maximum);
error CanonicalizerReturnDataMalformed(bytes32 profileId);
error SubjectIdMismatch(bytes32 expected, bytes32 derived);
error ExternalAssetAlreadyRegistered(bytes32 subjectId);
error SubjectIdCollision(bytes32 subjectId);
error SchemaNotAdmitted(bytes32 schemaId);
error SchemaAlreadyAdmitted(bytes32 schemaId);
error InvalidSchemaDocument(bytes32 schemaId, bytes32 suppliedHash);
error FamilyNotAdmitted(bytes32 familyId);
error FamilyAlreadyAdmitted(bytes32 familyId);
error InvalidFamilyKind(uint8 familyKind);
error InvalidFamilyClassBitmap(bytes32 familyId, uint16 supplied);
error StreamClassNotPinned(uint8 authorizationClass);
error RecordTypeNotAdmitted(bytes32 recordType);
error RecordTypeAlreadyAdmitted(bytes32 recordType);
error RecordTypeClassMismatch(bytes32 recordType, uint8 authorizationClass);
error StableRecordTypePairMismatch(bytes32 recordType, bytes32 familyId, bytes32 schemaId,
    uint8 authorizationClass);
error FamilyRevisionMismatch(bytes32 familyId, uint64 expected, uint64 actual);
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
error RecordFamilyUnauthorized(address actor, bytes32 recordType, bytes32 familyId,
    uint8 authorizationClass, uint64 familyRevision);
error InvalidAuthority(address signer, uint8 authorizationClass);
error InvalidSignature(address signer);
error GlobalRoleUnauthorized(bytes32 globalRoleId, address caller, bytes4 selector);
error InvalidAuthorityTransition(address newAuthority);
error InvalidAuthorityCapability(bytes32 expected, bytes32 actual);
error AuthorityChangePending(address pendingAuthority, uint64 eta);
error NoPendingAuthority();
error AuthorityChangeNotReady(uint64 eta, uint64 currentTime);
error InvalidGovernanceExecutor(address executor);
error GovernanceExecutorChangePending(address pendingExecutor, uint64 eta);
error NoPendingGovernanceExecutor();
error GovernanceExecutorChangeNotReady(uint64 eta, uint64 currentTime);
error GovernanceExecutorChanged(address expected, address actual);
error InvalidTransitionTarget(address target, bytes32 expectedCodeHash);
error TargetReleaseNotAdmitted(uint8 targetKind, address target, bytes32 codeHash);
error TargetReleaseAlreadyAdmitted(uint8 targetKind, address target, bytes32 codeHash);
error TargetReleaseMismatch(uint8 targetKind, address target, bytes32 codeHash);
error ReleaseAttestorPolicyMismatch(bytes32 expectedPolicyHash, bytes32 actualPolicyHash,
    bytes32 expectedSignerSetHash, bytes32 actualSignerSetHash);
error InvalidTargetDependency(bytes32 releaseId, uint256 index);
error TargetDependencyChanged(bytes32 releaseId, uint256 index, address dependency);
error TargetConformanceMismatch(bytes32 expected, bytes32 actual);
error InvalidInterfaceProbe(bytes32 expected, bytes32 actual);
error InvalidSuccessorVersion(bytes32 expected, bytes32 actual);
error SuccessorVersionNotNew(bytes32 version);
error InvalidPredecessorRegistry(address expected, address actual);
error AuthorityTargetChanged(bytes32 expected, bytes32 actual);
error SuccessorTargetChanged(bytes32 expected, bytes32 actual);
error WritesNotFrozen();
error WritesAlreadyFrozen();
error LaneHeadChangedDuringSignature(bytes32 expected, bytes32 actual);
error NonceStateChangedDuringSignature(address signer, uint256 nonce);
error AuthorizationDependencyChanged(bytes32 dependencyId, bytes32 expected, bytes32 actual);
error SignatureExpired(uint64 deadline, uint64 currentTime);
error NonceUsed(address signer, uint256 nonce);
error NonceRevoked(address signer, uint256 nonce);
error BatchTooLarge(uint256 actual, uint256 maximum);
error BatchGasBudgetExceeded(uint256 required, uint256 available);
error BatchIdAlreadyUsed(bytes32 batchId);
error WritesFrozen();
error InvalidSuccessor(address successor);
error SuccessorAlreadySet(address successor);
error InvalidStreamMirrorLink(bytes32 subjectId, address streamCore, address ownerRecordModule,
    uint256 collectionId, uint256 collectionSerial, uint256 tokenId);
error StreamMirrorRuntimeMismatch(address target, bytes32 expected, bytes32 actual);
error StreamMirrorReadbackMismatch(uint256 tokenId, bytes32 field, bytes32 expected, bytes32 actual);
error StreamMirrorReturnDataInvalid(address module, bytes4 selector, uint256 actualLength);
error StreamTokenNotMinted(uint256 tokenId, uint8 lifecycle);
error StreamMirrorLinkAlreadySet(bytes32 subjectId);
error OwnerRecordConvergenceRequired(bytes32 ownerRecordHashVectorId);
error InvalidRoleProvider(address provider);
error ResolverProfileNotAdmitted(bytes32 profileId);
error ResolverProfileAlreadyAdmitted(bytes32 profileId);
error InvalidResolverProfile(bytes32 profileId);
error InvalidHttpsAssertion(bytes32 uriHash);
error HttpsAssertionRequired(bytes32 uriHash);
error HttpsAssertionExpired(bytes32 assertionHash, uint64 expiresAt, uint64 currentTime);
error HttpsAssertionMismatch(bytes32 uriHash, bytes32 assertionHash);
error HttpsAssertionAlreadyExists(bytes32 assertionHash);
error HttpsAssertionRevisionMismatch(uint64 expected, uint64 actual);
error HttpsAssertionPredecessorMismatch(bytes32 expected, bytes32 actual);
error ResolverRevisionMismatch(bytes32 expected, bytes32 actual);
error InvalidAddressSet(uint256 index);
error FunctionUnauthorized(address caller, bytes4 selector);
error InvalidReleaseAttestorSet(bytes32 expectedSignerSetHash);
error InvalidReleaseAttestation(bytes32 releaseId, bytes32 releaseAttestationDigest);
error InvalidReleaseAttestorSignature(uint256 index, address expected, address recovered);
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
    bytes32 authorizationFamilyId,
    uint64 recordTypePolicyRevision,
    uint64 familyRevision,
    uint64 grantRevision,
    uint8 payloadMode,
    bytes32 supersedesRecordHash,
    uint32 payloadLength,
    bytes32 httpsAssertionHash,
    uint64 httpsResolverRevision,
    uint64 authorityRevision
);
event MuseumRecordBatchRecorded(bytes32 indexed batchId, uint256 count,
    bytes32 batchCommitment, uint64 authorityRevision);
event ExternalAssetRegistered(bytes32 indexed subjectId, bytes32 indexed assetProfileId,
    bytes32 canonicalAssetIdHash, string canonicalAssetId, address indexed registrar,
    bytes32 authorizationRoleId, uint64 authorityRevision);
event AssetProfileAdmitted(bytes32 indexed profileId, bytes32 schemaId, bytes32 documentHash,
    string uri, address canonicalizer, uint8 canonicalizerMode, bytes32 canonicalizerCodeHash,
    bytes32 canonicalizerImplementationHash, bytes32 canonicalizerVersionId,
    bytes32 canonicalizerConformanceInputHash, uint64 revision, address authority);
event SchemaAdmitted(bytes32 indexed schemaId, bytes32 documentHash, string uri,
    uint64 revision, address authority);
event RecordTypeAdmitted(bytes32 indexed recordType, bytes32 indexed familyId, bytes32 indexed schemaId,
    uint8 authorizationClass, uint64 revision, uint64 authorityRevision, address authority);
event RecordFamilyAdmitted(bytes32 indexed familyId, uint8 familyKind,
    uint16 allowedClassBitmap, uint64 revision, uint64 authorityRevision, address authority);
event RecordFamilyGrantUpdated(bytes32 indexed familyId, uint8 indexed authorizationClass,
    address indexed account, bool enabled, uint64 revision, uint64 authorityRevision,
    address authority);
event StreamMirrorLinkSet(bytes32 indexed subjectId, address indexed streamCore,
    address indexed ownerRecordModule, uint256 collectionId, uint256 collectionSerial,
    uint256 tokenId,
    bytes32 streamSubjectId, bytes32 ownerRecordHash, bytes32 ownerRecordHashDomain,
    bytes32 ownerRecordHashVectorId, uint64 revision, bytes32 authorizationRoleId,
    uint64 authorityRevision, address authority);
event StreamOwnerRecordInterfaceAdmitted(address indexed streamCore, bytes32 streamCoreCodeHash,
    address indexed interfaceModule, bytes32 interfaceModuleCodeHash,
    bytes32 ownerRecordHashDomain, bytes32 ownerRecordHashVectorId, bytes32 evidenceHash,
    uint64 revision, bytes32 authorizationRoleId, uint64 authorityRevision, address authority);
event ResolverProfileAdmitted(bytes32 indexed profileId, bytes32 documentHash,
    address indexed attestor, uint64 minTtl, uint64 maxTtl, uint64 revision,
    uint64 authorityRevision, address authority);
event HttpsAssertionRecorded(bytes32 indexed uriHash, bytes32 indexed resolverProfileId,
    uint64 resolverRevision, uint64 assertionRevision, bytes32 previousAssertionHash,
    bytes32 indexed resolvedAddressSetHash, bytes32 hostHash, uint64 issuedAt,
    uint64 expiresAt, address attestor, uint256 nonce, uint64 deadline,
    address[] sortedUniqueAddresses, bytes32 assertionHash,
    bytes32 signatureCommitment, uint64 authorityRevision);
event NonceRevocationRecorded(address indexed signer, uint256 indexed nonce, uint64 deadline,
    bytes32 signatureCommitment, address actor, uint64 nonceRevision,
    uint64 authorityRevision);
event GlobalRoleGrantUpdated(bytes32 indexed globalRoleId, address indexed account,
    bool enabled, uint64 roleRevision, uint64 authorityRevision,
    uint64 governanceExecutorRevision, address authority, address governanceExecutor);
event TargetReleaseAdmitted(uint8 indexed targetKind, address indexed target, bytes32 indexed codeHash,
    bytes32 releaseId, bytes32 runtimePolicyHash, bytes32 releaseAttestorPolicyHash,
    bytes32 releaseAttestorSignerSetHash, bytes32 externalDependencyHash,
    uint8 externalDependencyCount, bytes32 sourceCommit, bytes32 sourceTreeHash, bytes32 artifactHash,
    bytes32 conformanceDocumentHash, bytes32 signedDocumentHash,
    bytes32 releaseAttestationDigest, address releaseAttestor0, address releaseAttestor1,
    bytes32 releaseSignatureCommitment0, bytes32 releaseSignatureCommitment1,
    bytes32 releaseSignatureSetHash, bytes4 requiredInterfaceId,
    bytes32 expectedModuleVersion, bytes32 protocolVersion,
    bytes32 streamCompatibilityCommit, uint64 revision,
    uint64 authorityRevision, uint8 status, bytes32 previousReleaseId,
    bytes32 supersessionReasonHash, address authority);
event TargetReleaseDependencyStored(bytes32 indexed releaseId, uint256 indexed index,
    address indexed dependency, bytes32 codeHash, bytes32 runtimePolicyHash,
    bytes4 interfaceId, bytes32 purposeId);
event TargetReleaseQuarantined(uint8 indexed targetKind, address indexed target, bytes32 indexed codeHash,
    bytes32 releaseId, uint64 revision, bytes32 reasonHash,
    uint64 authorityRevision, address actor, address authority);
event InitialAuthorityActivated(address indexed authority, bytes32 indexed releaseId,
    address indexed governanceExecutor, bytes32 initialAuthorityArtifactCommitment,
    bytes32 expectedCodeHash, bytes32 conformanceDocumentHash, bytes4 requiredInterfaceId,
    bytes32 interfaceProbeHash, bytes32 capabilityCommitment, bytes32 evidenceHash,
    uint64 authorityRevision, uint64 governanceExecutorRevision,
    uint64 activatedAt, uint64 activatedBlock);
event AuthorityChangeQueued(address indexed pendingAuthority, bytes32 expectedCodeHash,
    bytes32 releaseId, bytes32 conformanceDocumentHash, bytes4 requiredInterfaceId,
    bytes32 interfaceProbeHash, bytes32 capabilityCommitment,
    address predecessorRegistry, bytes32 expectedModuleVersion, bytes32 evidenceHash,
    uint64 eta, uint64 authorityRevision, address proposer, uint64 queuedAt,
    uint64 queuedBlock, address authority);
event AuthorityChangeCancelled(address indexed pendingAuthority, bytes32 expectedCodeHash,
    bytes32 releaseId, bytes32 conformanceDocumentHash, bytes4 requiredInterfaceId,
    bytes32 interfaceProbeHash, bytes32 capabilityCommitment,
    address predecessorRegistry, bytes32 expectedModuleVersion, bytes32 evidenceHash,
    uint64 authorityRevision, address proposer, uint64 queuedAt, uint64 queuedBlock,
    address authority);
event RegistryAuthorityUpdated(address indexed oldAuthority, address indexed newAuthority,
    bytes32 expectedCodeHash, bytes32 releaseId, bytes32 conformanceDocumentHash,
    bytes4 requiredInterfaceId, bytes32 interfaceProbeHash,
    bytes32 capabilityCommitment, address predecessorRegistry,
    bytes32 expectedModuleVersion, bytes32 evidenceHash, uint64 authorityRevision,
    address proposer, uint64 queuedAt, uint64 queuedBlock, uint64 executedAt,
    uint64 executedBlock, address authority);
event GovernanceExecutorChangeQueued(address indexed oldExecutor, address indexed pendingExecutor,
    bytes32 evidenceHash, bytes32 capabilityCommitment, bytes32 bindingCommitment,
    uint64 executorRevision,
    uint64 authorityRevision, uint64 eta, address proposer, uint64 queuedAt,
    uint64 queuedBlock, address authority);
event GovernanceExecutorChangeCancelled(address indexed currentExecutor,
    address indexed pendingExecutor, bytes32 evidenceHash, bytes32 capabilityCommitment,
    bytes32 bindingCommitment, uint64 executorRevision, uint64 authorityRevision, address proposer,
    uint64 queuedAt, uint64 queuedBlock, address authority);
event GovernanceExecutorUpdated(address indexed oldExecutor, address indexed newExecutor,
    bytes32 evidenceHash, bytes32 capabilityCommitment, bytes32 bindingCommitment,
    uint64 executorRevision,
    uint64 authorityRevision, address proposer, uint64 queuedAt, uint64 queuedBlock,
    uint64 executedAt, uint64 executedBlock, address authority);
event GovernanceExecutorAuthorityRebound(address indexed executor,
    address indexed oldAuthority, address indexed newAuthority, bytes32 evidenceHash,
    bytes32 capabilityCommitment, bytes32 bindingCommitment, uint64 executorRevision,
    uint64 authorityRevision, uint64 reboundAt, uint64 reboundBlock);
event SuccessorSet(address indexed successor, bytes32 expectedCodeHash,
    bytes32 releaseId, bytes32 conformanceDocumentHash, bytes4 requiredInterfaceId,
    bytes32 interfaceProbeHash, bytes32 capabilityCommitment,
    address predecessorRegistry, bytes32 expectedModuleVersion, bytes32 evidenceHash,
    uint64 authorityRevision, address proposer, uint64 committedAt, address authority);
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
| Exact authorization mapping and revisions | `RecordSummary.authorizationClass`, `authorizationFamilyId`, `recordTypePolicyRevision`, `familyRevision`, `grantRevision`, `authorityRevision` | Same event fields | Direct caller's unique record-type mapping plus exact current family/grant/authority revisions | Signer's signed class/family revision plus the exact mapping, grant, and authority revisions loaded at execution |
| Inline payload | `payload(recordHash)` | `MuseumRecordRecorded.payloadMode/payloadLength` plus the state view | Exact bytes for `INLINE`, otherwise empty | Same signed envelope bytes |
| HTTPS assertion context | `RecordSummary.httpsAssertionHash`, `httpsResolverRevision` | Same event fields | Current exact per-URI assertion hash/revision for HTTPS; `bytes32(0), 0` otherwise | Same signed/recomputed per-URI values |
| HTTPS assertion nonce/revision lineage | `httpsAssertionByHash`/`currentHttpsAssertion` | `HttpsAssertionRecorded` carries nonce, deadline, monotone revision, predecessor, and signature commitment | N/A | Signed assertion row; duplicate/replay/reorg rules are state-readback based |
| Batch atomicity/commitment | `batchIdUsed(batchId)`, `batchCommitment(batchId)` | `MuseumRecordBatchRecorded` with commitment and authority revision | Exact ordered `MUSEUM_BATCH_COMMITMENT_DOMAIN` preimage; stored before visibility; duplicate ID/record or stale lane reverts all writes | N/A |
| Batch gas budget | Batch entry gate and `MAX_BATCH_GAS_UNITS` | `MuseumRecordBatchRecorded` on success; no event on revert | `MUSEUM_BATCH_GAS_GATE_V1` best-effort gate; benchmark retained separately; all writes atomic on out-of-gas | N/A |
| Target release reconstruction | `targetRelease`, historical/by-ID views, and dependency count/row views | `TargetReleaseAdmitted`, `TargetReleaseDependencyStored`, `TargetReleaseQuarantined` | Authority-admin admission binds address, dependency rows/ABI commitment, acyclic release ID, status, and predecessor/reason | N/A |
| Active authority reconstruction | `authorityRevision()`, `authorityState()`, `pendingAuthority()` | `AuthorityChangeQueued`, `RegistryAuthorityUpdated`, `GovernanceExecutorAuthorityRebound` with all commitments | Queue/execution/use recheck target release, dependencies, code, interface, capability, predecessor, version, authority linkage, and the current executor revision | N/A |
| Governance executor reconstruction | `governanceExecutor()`, revision/current/pending binding views | `GovernanceExecutorChangeQueued`, `GovernanceExecutorChangeCancelled`, `GovernanceExecutorUpdated`, `GovernanceExecutorAuthorityRebound` | Direct current executor, evidence/capability commitments, equal cross-bound authority/executor revisions, queue/ETA/execution/rebind provenance | N/A |
| External asset authorization | `ExternalAsset.authorizationRoleId`, `authorityRevision` | `ExternalAssetRegistered.authorizationRoleId/authorityRevision` | Actual enabled global role and authority revision | N/A |
| Stream mirror authorization | `StreamMirrorLink.authorizationRoleId`, `authorityRevision` | `StreamMirrorLinkSet.authorizationRoleId/authorityRevision` | Actual enabled global role and authority revision | N/A |
| Owner-record interface admission | `StreamOwnerRecordInterface.revision`, `authorizationRoleId`, `authorityRevision` | `StreamOwnerRecordInterfaceAdmitted` | Governance-executor role and authority revision | N/A |
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

### 7.3 Enforceability matrix

This matrix is normative for the new control surfaces. A requirement is not
implementation-grade unless its ABI input/state, deterministic check, and
redundant audit event are all identified here.

| MUST requirement | ABI/state surface | Deterministic check | Audit event/state output |
|---|---|---|---|
| Canonicalizer is immutable, bounded, and non-proxy | `admitAssetProfile`, `AssetProfile` | governed exact `(profileId, address, extcodehash, conformance-input hash)` allowlist; reviewed source/toolchain evidence; code size, defined executable-region scan, forbidden-opcode scan, mode `0`, zero implementation hash, exact gas/return/input limits, and static canonicalize equality at admission and registration | `AssetProfileAdmitted`, `ExternalAssetRegistered` |
| Canonicalizer opcode policy is revision-pinned | `AssetProfile.documentHash`, `canonicalizerVersionId` | Cancun opcode table, exact executable region/CBOR treatment, PUSH/JUMPDEST boundary rules, reserved/unknown fail-closed, future revision requires new profile/version/allowlist | `AssetProfileAdmitted` and deployment manifest |
| Initial authority activation is acyclic and one-shot | `initializationState`, `initialAuthorityArtifactCommitment`, `activateInitialAuthority` | signature/target-address-free constructor; address-independent artifact precommitment; post-deployment registry-bound 2-of-3 release; states `0 -> 1 -> 2`; all other mutators blocked before `2`; full rollback on failure; exact constructor/executor/release/target bindings | `TargetReleaseAdmitted`, dependency events, `InitialAuthorityActivated`, complete authority/executor state |
| Authority target is accepted only after proof | Target-release row/dependency views, `quarantineTargetRelease`, `setAuthority(TransitionTargetInput)`, `pendingAuthority`, `authorityState()` | canonical evidence schema/JCS hash, 2-of-3 signatures, two availability observations, source SHA-1/tree validation, two-build equality, fixed non-proxy runtime scanner, persisted dependency row/ABI-set recomputation plus code/interface checks, bounded target probes, context-bound `IMuseumAuthorityProviderV1` capability handshake, predecessor/linkage/version/status/evidence checks | `TargetReleaseAdmitted`, `TargetReleaseQuarantined`, `AuthorityChangeQueued`, `AuthorityChangeCancelled`, `RegistryAuthorityUpdated` |
| Authority execution is safe against target mutation | `executeAuthority` | ETA; repeat every stored target and dependency code/interface/purpose-ID/commitment check plus linkage/probe; atomically refresh both authority/executor cross-bound capability rows | `RegistryAuthorityUpdated`, `GovernanceExecutorAuthorityRebound`; pending state remains on failed execution |
| Governance executor is separate and replaceable | executor address/revision/current/pending views; `setGovernanceExecutor`, `executeGovernanceExecutor`, `cancelGovernanceExecutor` | direct current caller; closed derived roles; 48-hour ETA; provider capability recomputed over exact new executor/revision and atomically copied to `AuthorityState`; Safe is neither TargetRelease nor dependency | executor transition events and complete current/pending/authority cross-bound state |
| Emergency freeze is provider-independent | `freezeWrites`, executor address/revision, `writesFrozen` | direct current executor and registry-held revision only; authority-provider call/capability/`canAuthorize` is forbidden on this path | queue-cancellation events and `WritesFrozen` |
| Successor is validated after freeze | `setSuccessor(TransitionTargetInput)`, `successorTarget`, `targetRelease` | direct current executor without provider authorization; freeze state, no prior successor, pre-admitted governed exact-codehash release row, canonical evidence gate, fixed non-proxy runtime scanner, bounded `IMuseumSuccessorV1` calls, full capability/probe/predecessor binding, `moduleSupersedes()==address(this)`, expected new module version, current protocol/Stream compatibility | `SuccessorSet` |
| Family kind and class bitmap are governed | `admitRecordFamily`, `recordFamily` | closed-world kind; Stream subset `0x01fe`; Museum subset `0x1e00`; append-only revision | `RecordFamilyAdmitted` |
| Record type has one class | `admitRecordType`, `recordTypePolicy` | nonzero one-bit class selected and present in family bitmap; stable six IDs additionally require the exact closed-world family/schema/class row; no write-time selection | `RecordTypeAdmitted` or revert with `StableRecordTypePairMismatch` |
| Direct and relayed writers are identical | record selectors, `recordFamilyGrant`, by-signature fields | both call `requireRecordWriter`; full-call nonReentrant guard; every snapshotted dependency revalidated after ERC-1271 callback; by-signature class and family revision equal current mapping and are signed | `MuseumRecordRecorded`, `RecordFamilyGrantUpdated`, `RecordSummary`; no state/event on revert |
| HTTPS profile and TTL are governed | `admitHttpsResolverProfile`, `resolverProfile`, immutable `MUSEUM_URI_SAFETY_PUBLIC_V1` constants | nonzero attestor, bounded TTL, append-only resolver-profile revision and authority revision; URI parser executes the pinned safety-document hash and vectors | `ResolverProfileAdmitted` and `HttpsAssertionRecorded` |
| HTTPS assertion is valid on-chain | `recordHttpsAssertionBySig`, `httpsAssertion`, `currentHttpsAssertion`, `httpsAssertionByHash` | per-URI key; canonical URI/host parse; hostHash recomputed; EOA/ERC-1271 signer; signer nonce/deadline; monotone revision/predecessor; profile revision/attestor role; sorted/deduped bounded address ABI hash; routability; TTL/window; assertion hash | `HttpsAssertionRecorded` |
| Every HTTPS record has current evidence | record write selectors, `RecordSummary` | recompute exact record `uriHash` and `hostHash`; load current per-URI pointer; require matching profile/revision/hash and live window; store assertion hash/revision | `MuseumRecordRecorded` and state-only summary |
| External/mirror authorization is reconstructable | `ExternalAsset`, `StreamMirrorLink` | exact enabled global role and active authority revision captured at write | `ExternalAssetRegistered`, `StreamMirrorLinkSet` |
| Owner-record admission history is reconstructable | `StreamOwnerRecordInterface` | append-only interface revision, pinned evidence and governance-executor role | `StreamOwnerRecordInterfaceAdmitted` |

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
2. Admit governed record families with exact kind and allowed-class bitmaps;
   map each record type to exactly one class. Shared Stream record types use
   pinned Stream classes; Museum-native types use Museum-only families.
3. Govern the Museum Safe as the constructor-bound direct
   governance-executor account, pin the address-independent initial-authority
   artifact commitment and release-attestor policy, and prepare the
   post-deployment activation package. The Safe is not a TargetRelease or
   provider dependency. No migration operator gets artist, owner, rights,
   governance, or independent-attestor authority by implication.
4. After inert deployment, deploy and verify the provider, collect the
   registry-bound 2-of-3 release attestations, execute the one-shot activation,
   then grant any migration operator only its required family classes. Record
   the authority contract/code hash, interface/probe commitment,
   context-bound capability commitment, role-domain/selector-set hash, active
   `authorityRevision`, and full `authorityState()` in the deployment manifest.
   Rotate providers through append-only events and re-run the capability
   handshake at every transition/use.

### Phase 2 — deploy V1

The constructor parameters include the exact separate nonzero inputs
`address initialGovernanceExecutor`,
`bytes32 initialGovernanceExecutorEvidenceHash`, and
`bytes32 initialAuthorityArtifactCommitment`; nonzero
`bytes32 releaseAttestorPolicyHash` plus three strictly increasing
`address releaseAttestorSigner0..2` inputs from the separately
governance-approved deployment policy; the immutable Stream compatibility
commit (`bytes32`); and `moduleSupersedes` (zero for the first deployment).
The constructor derives and stores the signer-set commitment, binds the
executor at revision 1 with capability/binding commitments temporarily zero,
sets initialization state `0` (`UNINITIALIZED`), and stores zero authority and
successor state. It performs no external call and receives no target address,
release ID, conformance/signed-document hash, interface probe, capability
commitment, EIP-712 digest, signature, or signature commitment.

The constructor-pinned artifact commitment is exactly
`keccak256(abi.encode(MUSEUM_INITIAL_AUTHORITY_ARTIFACT_DOMAIN,
runtimePolicyHash, sourceCommit, sourceTreeHash, artifactHash,
requiredInterfaceId, bytes32(0), bytes32(0), bytes32(0), bytes32(0),
bytes32(0)))`, where the five trailing zero values are respectively the
authority release's `expectedModuleVersion`, `protocolVersion`,
`streamCompatibilityCommit`, `previousReleaseId`, and
`supersessionReasonHash`. It deliberately excludes the target/registry
addresses, release ID, dependency-address set, evidence-document hashes,
attestation digest/signatures, probe, and capability commitment. The committed
runtime artifact therefore MUST be address-independent; an authority runtime
that embeds the registry address in immutable bytecode is not eligible for
initial activation. This preimage is completely reproducible before computing
the registry init-code hash and cannot introduce a CREATE2 fixed-point
dependency.

After deployment, the initial executor submits one
`activateInitialAuthority(TargetReleaseInput,TransitionTargetInput)` call. The
release attestations are produced only after the actual chain ID, registry
address, and authority-provider address are known. On entry the function MUST
require `msg.sender == initialGovernanceExecutor`, executor revision 1,
initialization state `0`, zero authority/authority revision/successor, and
unchanged constructor immutables. It sets state `1` (`INITIALIZING`) before any
external call. Reentrancy and every other mutator reject states `0` and `1`;
a reverting activation atomically restores state `0`, while a successful call
sets state `2` (`ACTIVE`) only after every release, dependency, target,
authority, and executor write and event is complete. No function can reset the
state or invoke activation from state `2`.

`activateInitialAuthority`, ordinary `admitTargetRelease`, `setAuthority`, and
`setSuccessor` MUST call the same internal, non-reentrant
`_admitAndValidateTargetReleaseV1` primitive with a transition-context enum; no
path may copy only part of its checks or call a setter as a weaker substitute.
The activation primitive's machine-checkable checklist is exactly:

1. recompute the constructor-pinned artifact commitment from the supplied
   release and require equality; validate authority kind, nonzero/revision-1
   first-row fields, right-aligned source SHA-1, evidence-schema and
   release-attestor-policy schema hashes, the exact policy JCS and signer-set
   ABI commitments against the constructor immutables, the registry/chain-bound
   2-of-3 EIP-712 signatures from that governed set, two availability
   observations, and the target runtime-policy hash;
2. require `artifactHash == extcodehash(target) ==` both independent build
   runtime hashes, code size within 24,576 bytes, and the complete
   `MUSEUM_TARGET_RUNTIME_NONUPGRADEABILITY_V1` scanner result and the exact
   declared dependency rows: validate their order/count/purpose IDs and exact
   dependency runtime-policy hashes, direct code hashes, complete no-proxy
   dependency-policy scans, and ERC-165 interfaces; recompute the ABI row/set
   commitment and stage the rows by release ID;
3. require the exact required ERC-165 interface and exact return lengths for
   every probe, with `TARGET_PROBE_GAS_LIMIT` and
   `TARGET_PROBE_RETURN_BYTES_LIMIT` enforced per call;
4. require the target's booleans, registry address, target revision,
   protocol/Stream commitments, predecessor linkage, expected module version,
   and `canAuthorize` to equal the initial-row formulas;
5. recompute `interfaceProbeHash`, the authority and initial-executor
   `capabilityCommitment` values, and
   `MUSEUM_AUTHORITY_SELECTOR_SET_HASH` from the same validated fields, the now
   known registry address, and the exact initial executor address/revision;
   require equality with the supplied transition target and derive the
   executor binding commitment on-chain;
6. require `status == 1`, `predecessorRegistry == address(this)`, the provider's
   `authorityRevision() == 1`, executor revision 1, and no successor; then
   atomically store the full release/dependency rows, `AuthorityState`, and
   completed `GovernanceExecutorState`, emit the release and initial-authority
   events, and set initialization state `2` last. The executor obtains the two
   closed direct-call roles from that binding; the provider receives no role
   grant.

Any checklist failure leaves an inert, retryable deployment with no admitted
release or authority state; governance may retry only a complete valid package
or abandon that address. No ordinary mutator, freeze, or successor path is
available before state `2`. The deployed bytecode MUST expose the same checklist
through the ordinary admission primitive (an implementation may share an
internal library but may not duplicate or weaken it), and MUST NOT accept an
arbitrary caller hash or evidence value. A CREATE2 deployment MUST compute and
govern the address from signature-free, target-address-free init code, deploy
the inert registry, deploy/verify the address-bound provider if necessary, and
only then collect the registry-bound attestations and activate. No successor
target may be set at deployment. The registry is not a proxy. A later
implementation is a new immutable contract with `streamCompatibilityCommit`
and `moduleSupersedes` metadata.

Checklist items 1 and 2 have two explicit inputs: the signed release-evidence
bundle is validated by the release gate before the transaction, and the
contract-facing primitive validates the fixed schema/policy hashes, immutable
release-attestor policy/signer-set commitments, row fields,
direct runtime hash, and all deterministic bytecode/probe invariants before it
stores the row. The contract does not claim to fetch GitHub, IPFS, Arweave, or
compiler output. A deployment controller MUST refuse to construct the
transaction unless the external evidence result is present, signed by the
fixed governance-approved 2-of-3 policy, and bound to the exact `releaseId` and
`conformanceDocumentHash`; the primitive then refuses any row whose committed
evidence hash, signer-policy/signer-set hash, or policy/schema hash is not the
registry's immutable V1 value. This is the
complete trust boundary, rather than an unreviewable imported rule.

### Phase 3 — register subjects and links

1. Register each external asset's exact canonical CAIP identity.
2. Record `MUSEUM_EXTERNAL_ASSET_IDENTITY_V1` only as identity evidence; do
   not mark custody, title, or accession in that record.
3. For a Stream-native work, set a `StreamMirrorLink` only after the §2.1
   convergence gate. It MUST contain the verified Stream Core address,
   owner-record module, collection ID, token ID, Stream subject ID, owner
   record hash, hash domain, and vector ID. A mirror link is a
   cross-reference, not a second artwork identity.
4. Before migrating any HTTPS-bearing record, enumerate distinct canonical
   HTTPS URIs (including paths) and budget one signed assertion, current-pointer
   entry, storage slot, and renewal stream per URI. Assertions are not
   host-wide; sharing a DNS host or address set does not reduce this count.
   Produce a signed `MUSEUM_HTTPS_ASSERTION_CAPACITY_REPORT_V1` that binds the
   exact URI count, resolver TTL, renewal lead time, peak initial-issue and
   renewal transactions per hour, storage and measured gas, retry allowance,
   operator/service throughput, and the source-manifest root. In a disposable
   rehearsal, issue every required assertion and renew a representative
   maximum-size cohort before its lead-time deadline while injecting the stated
   retry rate. The report MUST show positive throughput and gas headroom after
   retries; a zero/negative margin, omitted URI, missed deadline, or unbound
   manifest fails migration.

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

For every HTTPS record, the tool MUST verify the per-URI assertion's exact
`uriHash` and recomputed `hostHash` before submission; a Stream-valid but
Museum-invalid URI is rejected rather than rewritten. The tool MUST compare
the post-write state to the source manifest, verify
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

## 9. Casey REAS completed donation and accession records

The Casey Reas seven-work group donated by punk 6529 is a completed donation
and has been received on-chain under the Art Blocks preapproval. The canonical
accession register and on-chain evidence record the exact seven CAIP-19-shaped
native identities, receipt transaction, and custody observations. A migration
MUST preserve those completed donation and receipt facts; it MUST cite their
recorded evidence rather than infer either fact merely from a wallet transfer
or donor attribution.

The receipt alone is not an accession-complete claim, but the canonical record
chain now is. `6529NM.2026.001.GAA-01` formally accepts the full gift;
`6529NM.2026.001.TITLE-01` and the seven executed title bindings document token
title; seven rights statements determine the CC BY-NC 4.0 use boundary; seven
condition reports record pass-with-conditions technical outcomes; an
independently reviewed accession certificate records the completed Museum
accession. Post-accession record `6529NM.2026.001.DILIGENCE-01` separately
binds finalized-state custody, token-specific approval, title interpretation,
and point-in-time exact-address compliance evidence. Migration MUST preserve
each record, its evidence boundary, effective time, status, and append-only
relationship. It MUST NOT infer the completed institutional decision from the
receipt alone or downcast the completed accession to intake-stage research.

| Stable Museum ID | Accessioned work |
|---|---|
| `6529NM.2026.001.01` | `CENTURY #31` |
| `6529NM.2026.001.02` | `CENTURY #724` |
| `6529NM.2026.001.03` | `CENTURY #401` |
| `6529NM.2026.001.04` | `Pre-Process #63` |
| `6529NM.2026.001.05` | `Phototaxis #308` |
| `6529NM.2026.001.06` | `923 EMPTY ROOMS #713` |
| `6529NM.2026.001.07` | `Ex Nihilo (Cosmos) #248` |

The migration MUST carry the reviewed Museum accession, title, rights,
condition, object, curatorial, technical, and diligence records under their
admitted Museum profiles; it MUST NOT substitute `MUSEUM_RESEARCH_NOTE_V1` for
those completed decisions. It MUST also preserve the stricter states that have
not been claimed: autonomous software preservation remains active stewardship,
and the objects are not represented as `preservation_complete` or
`display_ready`. The existing completed Museum `ACCESSION` certificate uses the
bilaterally matched `STREAM_ACCESSION_V1` payload profile. What remains
prohibited until the convergence gate in section 2.1 is a Stream owner-record
write or `StreamMirrorLink`: those actions require the source-backed Stream
implementation, deployed module, exact owner-record hash preimage and read
surface, runtime hash, golden vector, and state-readback round trip. That
host-side integration gate does not reopen or downgrade the Museum's completed
accession.

The lot `6529NM.2026.001` and its seven accessioned object records retain their
native CAIP-19 identities. Migration MUST preserve the existing evidence-backed
title, rights, condition, curatorial, technical, review, certificate, and
post-accession diligence records without collapsing them into one assertion.
Later preservation or display milestones are appended only when their own
evidence supports those stricter states; where the Stream convergence gate
permits it, a later Stream owner-record mirror link is likewise additive. The
collection-level curatorial argument does not substitute for object-level
records, and a future Stream link does not become the Museum's title or
accession authority.

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

* expose a new immutable module/implementation version through
  `registryVersion()` and its predecessor address through `moduleSupersedes()`;
* expose the unchanged compatible `MUSEUM_PROTOCOL_VERSION_V1` through
  `protocolVersion()`; the module version MUST be new and strictly different
  from `MUSEUM_REGISTRY_VERSION_V1`;
* preserve the exact V1 envelope and all V1 read selectors;
* retain the V1 hash domain and Stream compatibility commit if a future governed
  import interface is introduced; and
* never rewrite or delete an old record.
* receive explicit governance approval before becoming the write target.

`setSuccessor` is one-way. `freezeWrites` is one-way for the old registry and
does not erase read access. A successor cannot silently change a shared schema,
canonicalization ID, subject derivation, authorization-class meaning, or
Stream adapter behavior. A change needs a new ID and a new convergence gate.

V1 designates a successor but defines no import selector, import event, or
source-record/lane commitment. It therefore makes no V1 claim that a successor
imports, preserves, or verifies source hash/lane lineage. Any transfer of V1
records into a successor is scoped to a required V2 interface revision, which
MUST define an import ABI, source-registry/record/chain commitment, destination
record commitment, import event, replay protection, and executable vectors
before it can be deployed or relied on.

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

This is a synthetic, non-Casey conformance vector only. Its Casey-like local
identifier and `"proposed"` payload are not a statement about the Casey Reas
donation, its receipt, or accession status.

```text
recordTypeLiteral = MUSEUM_RESEARCH_NOTE
recordType = 0x5a50f1234f1c89b5d9c2f5b2062279349feac41d8e01bf708ee9adc20a2d8ba0
subjectId = 0x1111111111111111111111111111111111111111111111111111111111111111
canonicalPayload = {"id":"6529NM.2026.001.1","status":"proposed"}
canonicalPayloadUtf8Hex = 0x7b226964223a22363532394e4d2e323032362e3030312e31222c22737461747573223a2270726f706f736564227d
canonicalPayloadUtf8Bytes = 46
payloadMode = INLINE
payloadMode uint8 = 1
supersedesRecordHash = 0x0000000000000000000000000000000000000000000000000000000000000000
recordHashDomain = 0x0c86cc4258c69b4674aa86e715d4d167bd8288b78832a0a4c5a37943b31876c4
contentHash.algorithm = 1
contentDigest = 0x3f29b41d9d595ee7c116a4905fd8f4faf620b5757037db8a8988cd87b9c972a7
keccak256(contentHash.digest) = 0x648907ed3d936c0f74f8e05755c2ca9b06447e792208a269350464151c68fe36
contentHash.canonicalizationId = 0x886c7c89c308c459ca8a626e0ef36a5ea9f4c7a7b56aaf86c71a2ddf3b4f9044
uri = ipfs://bafybeiexd37whdwmbipbf7acxcrll2pg6lwcz6ks7atxc6z4niszkoragq
uriHash = 0x8ad820c94c531631741265f884f264fc8f3052c9f34c6590cdc7c59f7ebedffe
schemaId = 0xe3d3da75ee91ec6a7603f809eb413342e42874cabf3992d443409657745c3cf0
signatureScheme = 0x0000000000000000000000000000000000000000000000000000000000000000
signatureHash.algorithm = 0
signatureHash.digest = 0x
signatureHash.canonicalizationId = 0x0000000000000000000000000000000000000000000000000000000000000000
keccak256(signatureHash.digest) = 0xc5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470
hashRefHash(contentHash) = 0x2a7a69c6080aa4baf28ec37f556a929a605eab80f755f25a5d8416c1fabaa0a5
hashRefHash(signatureHash) = 0x2653d71e6881daccbff9917e23f12df8e56f7a0f8688215ca7092a5368a7d470
chainId = 1
registry = 0x0000000000000000000000000000000000000001
effectiveAt = 1722470400
recordHash = 0x217e7a966879dd7c379772be42f35fe353b45c113cec0ac76c21dd068bd506d1
```

For the first lane append, `revision = 1`, `previousRecordHash = 0x00...00`,
and `chainHash = 0xd4b722a75d08db3e38afd4cfa1a887ec72915640cd08af54596401e7fa62ac49`.

### 13.2.1 Exact `NONE` content-hash vector

This vector is the only valid V1 `contentHash` for `payloadMode = NONE`:

```text
emptyPayloadCanonicalizationLiteral = MUSEUM_EMPTY_PAYLOAD_V1
emptyPayloadCanonicalizationId = 0xa441d30896b70045ccf31ccc5b89cefd312a64c9c2102fa1c6898140d443ef4f
contentHash.algorithm = 1
contentHash.digest = 0xc5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470
keccak256(contentHash.digest) = 0x10ca3eff73ebec87d2394fc58560afeab86dac7a21f5e402ea0a55e5c8a6758f
contentHash.canonicalizationId = 0xa441d30896b70045ccf31ccc5b89cefd312a64c9c2102fa1c6898140d443ef4f
hashRefHash(contentHash) = 0x5d7e6369b77349763919edf197e8a1ba931bbfd63a9e40b5af00ca630a4346c7
payloadMode = NONE
payloadMode uint8 = 0
payload = 0x
uri =
```

`specs/onchain/manifest_abi_selector_check_v1.py` independently recomputes
every value and binds this transcript. Its negative mutations prove that a
zero `HashRef`, raw empty digest bytes, `RFC8785_JCS`, SHA-256, and a nonempty
digest or URI all reject on each direct, relayed, and batch write path.

### 13.3 EIP-712 relayed write

With chain ID 1, verifying contract `0x0000000000000000000000000000000000000001`,
the record hash above, `signedRecordHash` equal to that record hash,
`signedPreviousRecordHash = 0x00...00`, `previousRecordHash = 0x00...00`,
authorization class 12, family revision 1, nonce 7, and deadline 1,800,000,000:

```text
EIP712Domain type string = EIP712Domain(string name,string version,uint256 chainId,address verifyingContract)
EIP712 name = 6529 Network Museum Registry
EIP712 version = 1
MuseumRecordWrite type string = MuseumRecordWrite(bytes32 recordHash,bytes32 recordType,bytes32 subjectId,bytes32 previousRecordHash,uint8 authorizationClass,uint64 familyRevision,uint256 nonce,uint64 deadline)
signedRecordHash = 0x217e7a966879dd7c379772be42f35fe353b45c113cec0ac76c21dd068bd506d1
signedPreviousRecordHash = 0x0000000000000000000000000000000000000000000000000000000000000000
previousRecordHash = 0x0000000000000000000000000000000000000000000000000000000000000000
nonce = 7
deadline = 1800000000
authorizationClass = 12
familyRevision = 1
record.signatureScheme = 0x0000000000000000000000000000000000000000000000000000000000000000
record.signatureHash = (algorithm=0,digest=0x,canonicalizationId=0x0000000000000000000000000000000000000000000000000000000000000000)
domainSeparator = 0xfffa62454cc94111fc3da4487def1fc9f0e36727a701015f2a46ff4a1a7c7b70
MuseumRecordWrite typeHash = 0x9db358603fafa20478b7907082a0cba6193d6d183e21cb617b78c5f3b35ddbba
structHash = 0x146b17442eacd5df800066c61aac564531f3e69f18b61ea7d23580b6a9f286fa
preimage = 0x1901 || domainSeparator || structHash
preimage = 0x1901fffa62454cc94111fc3da4487def1fc9f0e36727a701015f2a46ff4a1a7c7b70d146b17442eacd5df800066c61aac564531f3e69f18b61ea7d23580b6a9f286fa
digest = 0x797c9ee306e88434acb70222d8510ee98bc5e502e3e3be94efeb94423d44dfca
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

### 13.5 Pinned Stream draft owner-record EIP-712 vector (not deployed)

The pinned Stream design document publishes an `OwnerRecord` ABI, five
function selectors, the owner-write and nonce-revocation EIP-712 type strings
and typehashes, and the domain name/version. This is real draft protocol
evidence and the Museum matches it exactly. The pinned source tree does not,
however, contain a `StreamOwnerRecords` implementation, a deployed module
address, an exact stored `recordHash` preimage, or a source-backed read
round-trip. The §2.1 convergence gate therefore remains closed: this vector
tests the published draft signature envelope only and MUST NOT be represented
as a successful Stream write or deployed compatibility result.

The canonical draft ABI selectors are:

```text
recordOwnerRecord selector = 0x198c95e3
recordOwnerRecordFor selector = 0xf24bb020
isOwnerRecordNonceUsed selector = 0x18544c94
revokeOwnerRecordNonce selector = 0x9d03970a
revokeOwnerRecordNonceFor selector = 0x50e9829a
```

The following deterministic vector uses chain ID `1`, the explicitly synthetic
Stream Core address `0x0000000000000000000000000000000000001001`, and the
explicitly synthetic satellite address
`0x0000000000000000000000000000000000002002`. Those addresses are test
inputs, not Stream deployment claims. Dynamic EIP-712 fields are represented
by `keccak256(fieldBytes)` in the struct preimage.

```text
owner = 0x000000000000000000000000000000000000dead
tokenId = 771769
STREAM_SUBJECT_TOKEN_V1 = 0x1e576f27850d12bc1ec9255ca277dbecfbc84fb3a9a34c474640dfca89811d7e
streamCore = 0x0000000000000000000000000000000000001001
subjectId = 0x7839d73dfe2384e7818fa90691f4ffa27260eb4af0cfe50f8d1615f8bf6db5b4
recordType = 0x4dc3a5e33f97bcd06f2d025349086438272d94a398185aca416ae539e36521fb
schemaId = 0xc04bb48f95c8db4fe7f26a20106533f987003843f2fed36fd6d89f207ddfbd86
algorithmId = 1
contentHash.digest = 0x869b5e7167f9281b7c232510e776e95500162af0fe1c031f5f7d065bf7014ee7
canonicalizationId = 0x886c7c89c308c459ca8a626e0ef36a5ea9f4c7a7b56aaf86c71a2ddf3b4f9044
uri = ipfs://bafybeiexd37whdwmbipbf7acxcrll2pg6lwcz6ks7atxc6z4niszkoragq
payload = {"record":"owner","tokenId":"771769"}
effectiveAt = 1722470400
nonce = 7
deadline = 1800000000
verifyingContract = 0x0000000000000000000000000000000000002002
EIP712 name = 6529StreamOwnerRecords
EIP712 version = 1
STREAM_OWNER_RECORD_TYPEHASH = 0x9c8c4f8b7ec1e8731277f53e36271ebf92fc96425f0c082143042400814c6b05
STREAM_OWNER_RECORD_REVOCATION_TYPEHASH = 0x11a07172744cbac614966ef944b190ff3c1b4a7076ab4483c69e48ba2b9ee49c
domainSeparator = 0x0529e5a05df15f9cb773e9a719e83050647d6252d8658a700154434484f653f5
structHash = 0xfb71d60a68e0894166ae306df4fd11238530ee87e5714aa5d8c3e990fb6506f6
digest = 0x1fe370911b6eda46ee6153458ffeac7bdc2c0c7fd7e9fb0af6d7385e66df2605
```

The checker derives `subjectId` exactly as
`keccak256(abi.encode(STREAM_SUBJECT_TOKEN_V1, uint256(chainId),
address(streamCore), uint256(tokenId)))`; it is not a free-form fixture value.

Museum-only `payloadMode` and `supersedesRecordHash` remain in the Museum
record hash. They are not fields of this Stream draft signature envelope, so
whole-tuple positional equality is invalid. A future adapter MUST publish a
named-field crosswalk plus source-backed stored-hash and readback vectors.

### 13.5.1 Stream mirror-link readback vector

This synthetic, non-deployment vector exercises the closed mirror-link gate.
The registry admits exact core and adapter addresses plus both runtime hashes,
then reads the adapter's core/domain/vector/binding and the Core's independent
token-collection identity. It derives both the Stream subject and the Museum
CAIP-19 external-asset subject from the admitted core and token ID. The
executable checker rejects a swapped Museum subject or canonical asset,
nonzero adapter collection substitution, and substitutions of the core,
adapter, Stream subject, owner-record hash, hash domain, vector, return-data
length, prepared/unknown/burned lifecycle, or caller expected hash before any
link can be stored.

<!-- STREAM_MIRROR_LINK_VECTOR_V1_BEGIN -->
```text
streamCore = 0x0000000000000000000000000000000000001001
ownerRecordModule = 0x0000000000000000000000000000000000002002
collectionId = 6529
collectionSerial = 713
coreMappingExists = true
coreBurned = false
coreLifecycle = 2
tokenId = 771769
tokenCollectionIdentitySelector = 0xa6b638c9
tokenLifecycleSelector = 0x8c46d901
canonicalAssetId = eip155:1/erc721:0x0000000000000000000000000000000000001001/771769
canonicalAssetIdHash = 0x90b7a82bdf2c1cb3873489133de2fa3acf8e8d8d6322970ce9d24c2d1be0610f
museumSubjectId = 0xfdcb969005c2ac59498f282a4a95b19c7a186392e8f5224db12e249fd72a541d
streamSubjectId = 0x7839d73dfe2384e7818fa90691f4ffa27260eb4af0cfe50f8d1615f8bf6db5b4
ownerRecordHash = 0xfa797ba9f4ce165b23b56b09a245ca0776764c4043725b15b75397783abbc0b0
ownerRecordHashDomain = 0x3333333333333333333333333333333333333333333333333333333333333333
ownerRecordHashVectorId = 0x4444444444444444444444444444444444444444444444444444444444444444
swappedMuseumSubject = REJECT
substitutedNonzeroAdapterCollectionId = REJECT
preparedIncompleteLifecycle = REJECT
substitutedMuseumAssetCoreModuleCollectionSubjectHashDomainVector = REJECT
```
<!-- STREAM_MIRROR_LINK_VECTOR_V1_END -->

`python -B specs/onchain/stream_mirror_link_check_v1.py` independently
recomputes this block and all listed rejection paths without contacting a
network. The addresses and values are fixtures, not deployed Stream claims.

### 13.6 Release-manifest vector

For one record with source ordinal `1`, path
`specs/onchain/contract-migration-v1.md`, record hash from §13.2, payload
mode `INLINE`, payload bytes from §13.2, source commit
`ff1c5825e3b61bfb2df0a639e057297beb946e4d`, Stream commit
`5021c8060950c3fef995271e674ed4b2007fee6d`, and generator
`museum-migration/1.0.0`. Their `bytes32` encodings are respectively
`0x000000000000000000000000ff1c5825e3b61bfb2df0a639e057297beb946e4d` and
`0x0000000000000000000000005021c8060950c3fef995271e674ed4b2007fee6d`.

```text
pathHash = 0x47f5e941106c25d308590891c8eb0bb3c721586361b9a9bf442b49782c132183
payloadBytesHash = 0x3f29b41d9d595ee7c116a4905fd8f4faf620b5757037db8a8988cd87b9c972a7
entryHash = 0xfa531a4233206547049d1b83c4b4e3e4d9763effb47227b2fd761ea1846ddfc8
root = 0x8bb17fc4361cbfe29c586218e716d0c4789973b222ee7a403f9d22f6f483a280
```

The offline command `python -B
specs/onchain/manifest_abi_selector_check_v1.py` MUST independently recompute
this active source commit, every published general hash golden in §13.1--§13.9
(including HTTPS lifecycle and batch values), the record/entry/root vector,
every canonical §7 ABI selector, and the closed role/selector/stable-record
authorization allowlists. The §13.9.1 evidence/bundle transcript is separately
recomputed and documentation-bound by the two TargetRelease checkers.
It is a design conformance check only; it does not contact a network, publish
a release, admit a target, or authorize deployment.

### 13.7 HTTPS assertion vector

This vector uses the exact on-chain assertion record and address-array ABI;
the address array is sorted by numeric `uint160` value:

```text
targetURI = https://example.com/archive/6529
host = example.com
uriHash = 0x000c84d539237dee07b2286ba2f354c5f808a9e49e2001c1e7ed9279e11cb704
hostHash = 0x02438d3405cadd648e08dbff51bdbeb415913e642189100dc4a012064c870883
resolverProfileId = 0x52be64fd2fb1c3795cf8dd6472100377858fd563f16de75584dcaf0f74b3e186
resolverRevision = 1
sortedUniqueAddresses = [0x0000000000000000000000000000000001010101, 0x0000000000000000000000000000000008080808]
abi.encode(address[]) = 0x0000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000000200000000000000000000000000000000000000000000000000000000010101010000000000000000000000000000000000000000000000000000000008080808
resolvedAddressSetHash = 0x17971e83b91ac972b51bdefb4cab3445a46319fc90d6bc5894819de59fbf03a9
assertionRevision = 1
previousAssertionHash = 0x0000000000000000000000000000000000000000000000000000000000000000
issuedAt = 1750000000
expiresAt = 1750003600
attestor = 0x000000000000000000000000000000000000dead
nonce = 9
deadline = 1750003600
assertionHash = 0xfd50c11dda2772e18067aab5b420f82784cec302f5327e459c894f437507b92a
assertionKey = 0x73b47b012ffa32766331b8ae4c360579931aea1202421bef120b851f83f177fa
assertionSubject = 0x6528698388e83a3af89e9af7095da74d003172bf2979ea74d7e27f9fc22a745c
EIP712 typeHash = 0x3bf3a1c189f1a79ba1cb192e6bb3295aa74108a14e15a1a9d48d450c22fdb02b
structHash = 0x13c54d9975522fc40701f92c4642fb3fbfd64ced140ff9ecfdc21a3e98ad2be7
digest = 0xbaf085c9cb66508ee83f1793c2e10319a15b005ab234bae3c23e0feac9477ecc
```

The signature type string is the exact string in §5.3; the digest is the raw
`0x1901 || domainSeparator || structHash` concatenation. Reversing the two
addresses, hashing packed bytes, or hashing a JSON representation instead of
`abi.encode(address[])` is non-conformant.

The expiry/renewal state transition is executable in
`specs/onchain/https_expiry_renewal_check_v1.py` and MUST pass with:

```text
oldAssertionHash=0xfd50c11dda2772e18067aab5b420f82784cec302f5327e459c894f437507b92a
renewedAssertionHash=0x757cefc2594290ff8a4fd62b99be6bf050165023c854b50061797dc9cc9f2eb5
expiredWrite=REJECT
renewedWrite=ACCEPT
historicalRecord=READABLE
oldValidityAfterRenewal=NOT_RETROACTIVE
```

At timestamp `1,750,003,601`, the revision-1 pointer is expired and a new
HTTPS-bearing write MUST reject until the signed revision-2 pointer is stored.
The revision-2 pointer starts at that timestamp, names the revision-1 hash as
its predecessor, and permits the new write. A record already stored with the
revision-1 assertion remains readable with its original assertion hash and
revision after expiry and renewal; renewal changes neither historical record
validity nor its audit fields.

### 13.8 Batch commitment vector

This one-record vector exercises the dynamic-array ABI encoding and the
byte-exact inline payload hash. It is not a permission to omit the count,
predecessor, payload hash, or authority revision from a production batch:

```text
batchCommitmentDomain = 0x6743de485825345432a60824968ffa9c8b3ef54adb2f4ad2d1cb219ec56e4400
batchIdLiteral = MUSEUM_BATCH_VECTOR_V1
batchId = 0xa4713265f6f293e83885203722026053a888831af3f829e81b6aaed0d5d1d70b
authorityRevision = 1
recordHashes = [0x217e7a966879dd7c379772be42f35fe353b45c113cec0ac76c21dd068bd506d1]
previousRecordHashes = [0x0000000000000000000000000000000000000000000000000000000000000000]
payloadHashes = [0x3f29b41d9d595ee7c116a4905fd8f4faf620b5757037db8a8988cd87b9c972a7]
batchCommitment = 0x1c1c8c0c0c71816b08183589eaca344e6cd6b0ba1bc784c2d5a84337c377fc8d
```

The exact one-record fixture is executable: `python -B
specs/onchain/batch_vector_check_v1.py` MUST print the batch ID above and
`0x1c1c8c0c0c71816b08183589eaca344e6cd6b0ba1bc784c2d5a84337c377fc8d`.
The batch ID is the direct 32-byte Keccak result of the literal; no extra
leading zero nibble is permitted.

### 13.9 Successor capability/probe vector

This deterministic successor-probe fixture isolates the complete probe
preimages. Its `probeReleaseId` is an input to those preimages only; it is not
an admitted `TargetRelease.releaseId`, not a deployable address, and not a code
hash:

```text
target = 0x0000000000000000000000000000000000000042
predecessorRegistry = 0x000000000000000000000000000000000000cafe
probeReleaseId = 0x5681ad0ab20e496843b5795ad4c7b9e7a3f460f069b4891ea07a9a34ee64d95a
expectedCodeHash = 0xd5a00f7341bd82056e931b07a2d8f28c4e11346df2d42d2c36566e108d31df2a
conformanceDocumentHash = 0x6e4410d14b8d771e9e6250b6e8aa1124051d3b30887bd53cd4658b88921b7fa9
expectedModuleVersion = 0x8578d451c146e5c9542b0a271b29ec0826085f5f1b5991d77245cfdcae3d7465
capabilityCommitment = 0x9eb7de0ee6411bd638968f0c3eea4ddefe9982952982164a9c8d9cf81bbc19c9
interfaceProbeHash = 0x8640ff49f37e78608f06f222a9a753e83c4e9687cb0d25f620368a8b7bc9dcc1
```

The fixture uses `requiredInterfaceId = 0x573d91cc`,
`protocolVersion = MUSEUM_PROTOCOL_VERSION_V1`,
`streamCompatibilityCommit = bytes32(0x5021c8060950c3fef995271e674ed4b2007fee6d)`,
and `moduleSupersedes = predecessorRegistry`. The capability preimage is
the exact `MUSEUM_SUCCESSOR_CAPABILITY_DOMAIN` tuple in §6.1.2; the probe
preimage is the exact `MUSEUM_TARGET_PROBE_DOMAIN` tuple and includes the
capability commitment. Ordinary `abi.encode` is required; packed encoding is
not a valid implementation.

### 13.9.1 Complete TargetRelease evidence and detached-bundle vector

`specs/onchain/target-release-evidence-v1.fixture.json` is a complete,
schema-valid `NON_DEPLOYMENT_CONFORMANCE_FIXTURE`, not a published release or
deployment attestation. It uses the exact synthetic authority target below and
the only permitted target policy. Its signer addresses come exclusively from
the separately schema-valid `release-attestor-policy-v1.fixture.json`; the
fixture policy's JCS hash and ABI signer-set hash model the two immutable
constructor commitments and do not approve production keys. `python -B
specs/onchain/target_release_evidence_check_v1.py` derives the acyclic order
`releaseId -> D0 -> conformanceDocumentHash -> D1 -> signedDocumentHash ->
two public test signatures from three admitted addresses -> detached
bundle/reference/availability`, checks
the exact target address, two builds, dependency list, runtime and governed
attestor policy hashes, predecessor and reason, and rejects target-address,
policy, code-hash, signer-threshold, signer-set, and self-selected-key
mutations. It uses only public deterministic test scalars and contacts no
network.

<!-- TARGET_RELEASE_BUNDLE_VECTOR_V1_BEGIN -->
```text
targetKind = 1
target = 0x0000000000000000000000000000000000000042
runtimePolicyHash = 0x95f9e52ebbfec6aa2d1ad41a516a6d9e7ce2f55cfed9de1fb906e6f6e9dae452
dependencyAddress = 0x000000000000000000000000000000000000d3e1
dependencyRuntimePolicyHash = 0xf8efb731af735014514f4a5b8ad22a6e2007ba23b11b45a9c8845db3f144ee2c
externalDependencyHash = 0x9b07c036f5d4638634e2b73bd0fa079ea1b1e78ede7e9475a952a2513e3329de
releaseAttestorPolicyHash = 0xf57a8f644ffb7acc960d2aa9b86b8381eda086e6e8ce1300b17fecb30c4f35e8
releaseAttestorSignerSetHash = 0x4c22201c9dce9842bd7393223caa67d3383f802013b6d3fb6530f9086477046c
releaseId = 0xdeb8472c3dfa2af9d997baf62026478c0cf5b4b8439ac94cdda47a48ac4b48e0
EIP712 domain type = EIP712Domain(string name,string version,uint256 chainId,address verifyingContract)
EIP712 name = 6529NetworkMuseumTargetRelease
EIP712 version = 1
EIP712 attestation type = MuseumTargetReleaseAttestation(bytes32 releaseId,bytes32 conformanceDocumentHash,bytes32 signedDocumentHash,bytes32 releaseAttestorPolicyHash,bytes32 releaseAttestorSignerSetHash)
release signature set domain = 6529networkmuseum.release-signature-set.v1
D0ConformanceDocumentHash = 0x8b05f34d37ea7478df221e0e7478df668bf0df5cf3758f096677520003059a6f
D1SignedDocumentHash = 0x0242d2cb6bbedce063eccbf4ade87df5f255de26e661884ac0c93f44b8d754cc
releaseAttestationDigest = 0x682aae357582c8d22cd11f69c58abc9d62ef5847e5b1cd916564768a733a688d
releaseSignatureSetHash = 0x3a76ae6b31e8ef8ffcab6c11f7e4f57ad8ca2a806ebb1cae85fcd766db3b818b
bundleUri = ipfs://bafkreicmpobzufsvdnkivssjjljhehh7ic22pnw52p2xnjkn2tda3rcou4
alternateBundleUri = ar://JE9OKl_-dxGWxR_BGEqrC8SmAnuvxwQL3ZuSa2dhNkQ
bundleContentHash = 0x26f70f9a77520b8210eae127c167edeed42f37e25a34abfbd213b02f6d6c6e09
bundleBytes = 1300
bundleSchemaHash = 0x12256931d7eebded2483454fdff90c2496ffca9cec980b1a07306b03082bef82
ipfsFetchObservationHash = 0xcb5df062f8b9758acacc207213b12f55edbbd24fe2e7641d04de50a85899fb93
arFetchObservationHash = 0x2014ca677eefa21c6565f15377313b8f294a0d5a206296dfe5d08cadf088b947
signatureRecovery = 2/3
```
<!-- TARGET_RELEASE_BUNDLE_VECTOR_V1_END -->

The coherent detached bundle is
`specs/onchain/target-release-signature-bundle-v1.fixture.json`; its descriptor
and two retrieval observations are
`specs/onchain/target-release-signature-bundle-v1.reference.json` and are
byte-for-byte the evidence object's `detachedSignatureBundle`. `python -B
specs/onchain/target_release_signature_bundle_check_v1.py` independently
schema-validates that linkage, content hash/CID/size, an exact two-of-three
sorted unique signer subset, and 2/3 EIP-712 recovery. These synthetic
IPFS/Arweave identifiers only exercise
the required retrieval shape. They MUST NOT be used as admission evidence,
deployment evidence, custody evidence, or authorization for a network write.

### 13.9.2 Governance-executor binding and freeze vector

This offline, synthetic vector proves the direct executor/provider split and
the freeze invariant. The authority provider remains the immutable target at
`0x0000000000000000000000000000000000000042`; the proposed executor account
is `0x0000000000000000000000000000000000006529`, which is neither a
TargetRelease nor a dependency. Ordinary `abi.encode` and the formulas in
§6.1.2 produce:

```text
authorityReleaseId = 0x442b8c759b677e48ed822ecf57344181e081deeb894664d60f0e076d22ef00e8
authorityCodeHash = 0x17e02f491227b715d8167c6ee64b87a3c70d51345ab5cb63c23b003fccd44fa1
evidenceHash = 0xb87be17166140c2103b87cadde72103d5673422df7e2a8fb0b0745e1e865f6fb
challenge = 0x369583a21a48e0cb37b85e373ffcce219434789d2d4c536ae16a1a683c43729f
capabilityCommitment = 0x970b6d8b04de91cb88b8b6fa3cf9f5af6faa46e452f27309a247ef7c5052e487
bindingCommitment = 0x40a3c47c9686f82852e14e2b503ff9e02cdbed30d556db7347112bec4061e3f9
crossBoundAfterExecutorRotation = true
reboundAuthorityReleaseId = 0xc7a2f5889fb4663ad2269ab003b5c32fe16ec960aeaf09f7255b4fe9adf998de
reboundAuthorityCodeHash = 0x86d7cb2cdbcff163f6f0ee294587f8cec673905c2e4d077024a09f3529455f90
reboundChallenge = 0xa858dee6314a072796ced21f2446e1324b27d61c97b2e437a0d639e8828bc15f
reboundCapabilityCommitment = 0x3c884a3210b5f6d3a8ff58804c326c58b2d67d3088d8a692e9e62f0838c552b4
reboundBindingCommitment = 0xdbb9a475785baab44b9a2c20fbdcb9a1626bdb853081135cae8afd58d7cbe73c
crossBoundAfterAuthorityRotation = true
providerDeniedFreeze = ACCEPT
providerDeniedSuccessor = ACCEPT
freezeClearsPendingExecutor = true
postFreezeExecuteGovernanceExecutor = REJECT WritesFrozen
```

`python -B specs/onchain/manifest_abi_selector_check_v1.py` independently
recomputes every hash, queues the revision-2 synthetic binding, models both
directions of atomic authority/executor cross-binding refresh, proves that a
provider returning `canAuthorize == false` cannot block the direct executor's
freeze or pre-admitted successor path, models `freezeWrites` atomically clearing
the pending row, and asserts that a stale/replayed
`executeGovernanceExecutor` cannot replace the frozen revision-2 executor after
freeze. This is executable design conformance, not a deployed-state claim.

### 13.9.3 Canonicalizer execution-limit vector

The executable checker binds the V1 fixed-point call to these exact limits and
tests each rejection independently:

```text
limitsId = 0xf66c08f21c02834b2dd294a0556fb5adb7c17b447338ee0ad5ecc1a2198509d3
callGasLimit = 100000
maxReturnDataBytes = 4096
maxCanonicalAssetIdBytes = 2048
boundaryFixedPoint = ACCEPT
overGas = REJECT
overReturnData = REJECT
oversizedInput = REJECT
malformedAbi = REJECT
outputMismatch = REJECT
```

Admission and registration run the same bounded-call primitive. The model
also rejects empty input and a failed/reverting call. These vectors prove the
design predicate, not gas behavior of an undeployed implementation.

### 13.10 Required negative tests

Conformance MUST cover malformed digest lengths, zero IDs, zero effective
time, invalid UTF-8/oversized or unsafe-scheme URI, unknown schema/type/profile,
wrong class, wrong predecessor, duplicate hash, payload-mode mismatch, payload
mismatch, empty payload for a meaning-bearing schema, every noncanonical
`NONE` content-hash mutation in §13.2.1 on direct/relayed/batch paths,
missing/cross-lane/newer
supersession target, expired signature, invalid EOA signature, invalid
ERC-1271 result, ERC-1271 callback lane/nonce mutation, used/revoked nonce,
nonce-revocation digest mismatch, batch over cap, batch partial failure,
duplicate external subject, noncanonical asset alias, duplicate mirror link,
pre-convergence Stream link, mutable/proxy canonicalizer opcode, canonicalizer
gas exhaustion, excess return data, oversized/empty input, malformed ABI, or
fixed-point mismatch, changed
authority/successor code hash or probe, EOA transition target, family kind or
ambiguous class, stale family revision, invalid HTTPS address-set ordering,
HTTPS address-count over 32, HTTPS nonce reuse/revocation/deadline, duplicate
assertion hash/key, assertion predecessor/revision mismatch, stale authority
capability, same-version successor, wrong-predecessor successor, and
new-version successor with a mismatched protocol or Stream compatibility,
expired/mismatched HTTPS assertion, resolver-profile revision mismatch, URI
substitution, reorg retry, attempted writes after freeze, stale cross-bound
authority/executor revisions or capabilities after either rotation, and any
provider attempt to veto the direct-executor `freezeWrites` or pre-admitted
post-freeze `setSuccessor` path.

Target-release evidence conformance additionally MUST reject a target-address
substitution (including equal code at a second address), runtime-policy or
external-dependency-hash substitution, code/build-hash substitution, duplicate
or circular release ID, malformed D0/D1 projection, a signer count other than
exactly two, duplicated or out-of-order signers, a signer outside the admitted
three, a detached bundle/reference
mismatch, a non-right-aligned SHA-1 tree OID, and any CIDv0 or noncanonical
CIDv1/Arweave textual alias. The modeled on-chain primitive MUST additionally
reject changed release/conformance/signed-document/policy/signer-set fields,
missing or altered signature bytes, and replay under a different chain ID or
registry address. Dependency conformance additionally rejects a
changed address/code/interface/purpose/policy, mutable or proxy runtime,
external-call or external-account-read opcode (`BALANCE`, `EXTCODESIZE`,
`EXTCODECOPY`, `EXTCODEHASH`), malformed ERC-165 response,
duplicate/out-of-order row,
or set-commitment mismatch. URI conformance rejects uppercase HTTPS/IPFS/AR
scheme aliases before parser normalization. Executor conformance proves that
freeze atomically cancels a queued executor transition and a post-freeze
`executeGovernanceExecutor` call rejects without changing the binding. It also
proves both directions of cross-binding refresh and accepts direct-executor
freeze/successor recovery when the active provider returns
`canAuthorize == false`.

Stream mirror conformance MUST reject a changed core or adapter runtime,
adapter core/domain/vector readback mismatch, non-exact adapter or Core
return-data length, absent/burned Core mapping, zero collection serial,
zero or nonzero-substituted adapter collection ID relative to the direct Core
read, a Stream subject not derived from the admitted core/chain/token tuple, a
Museum subject or stored CAIP-19 identity not derived from that same tuple,
zero or substituted owner-record hash, and a mismatch with the caller's
expected-hash guard. The registry MUST persist no partial link state on any
rejection.

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
* V1 successor designation exposes no import path; any V2 import path must pass
  its separately defined source-hash and lane-lineage vectors.

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
   safety, current HTTPS assertion association, signature emptiness rules, raw
   EIP-712 prefix, and Museum/Stream hash distinction pass golden tests.
5. **Authorization gate:** governed family kinds/bitmaps and unique classes,
   Safe/ERC-1271, EOA signatures,
   unordered nonces, nonce-revocation commitments/deadlines, reentrancy
   callback rechecks, global-role selector scope, authority timelock,
   successor-after-freeze, one-way freeze, provider rotation, and class
   isolation pass negative tests.
6. **Lineage gate:** duplicate rejection, predecessor/head accumulation,
   correction/supersession, successor designation without an import path, batch atomicity, and state-only
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
10. **Canonicalizer/URI gate:** every asset profile passes the immutable
    non-proxy runtime opcode scan and direct `extcodehash` check with mode 0;
    resolver profiles, bounded TTLs, sorted address-set checks, signed
    assertions, and current write-time HTTPS associations pass golden tests.
    A signed `MUSEUM_HTTPS_ASSERTION_CAPACITY_REPORT_V1` binds the frozen
    manifest's exact canonical-URI count and demonstrates, in a disposable
    full-issue plus maximum-cohort renewal rehearsal, positive measured
    throughput/gas headroom after the declared retry allowance and before the
    renewal lead deadline. Missing URIs, missed deadlines, or nonpositive
    headroom fail this gate.
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
14. **Initialization/CREATE2 gate:** constructor init code contains no target or
    registry-address-bound release ID, evidence hash, probe, capability,
    digest, or signature; the artifact commitment is independently reproduced;
    the governed CREATE2 address is computed from those inert inputs; all
    non-activation mutators reject states `0` and `1`; a reentrant or failing
    activation leaves state `0` and no partial release/dependency/authority
    storage; and one successful, exact-head, registry-bound activation advances
    `0 -> 1 -> 2`, emits complete audit events, and rejects every replay.

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
