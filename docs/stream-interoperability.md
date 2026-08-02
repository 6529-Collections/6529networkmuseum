# 6529Stream interoperability

## Pinned source

This profile is aligned to `6529-Collections/6529Stream` `origin/main` commit `5021c8060950c3fef995271e674ed4b2007fee6d`, observed 2026-08-01 UTC.

Normative Stream sources at that commit:

- `smart-contracts/IStreamPreservationRecords.sol`
- `smart-contracts/StreamPreservationRecords.sol`
- `docs/collection-metadata-contract.md`
- `docs/metadata-router-and-renderer.md`

Stream currently implements the generic preservation record envelope and specifies the museum profile semantics. Its design document also publishes a draft owner-record ABI and EIP-712 envelope, but the pinned source tree does not contain a `StreamOwnerRecords` implementation or a deployed owner-record module. At the pinned commit it does not yet publish standalone canonical JSON Schema files for `STREAM_ACCESSION_V1`, `STREAM_WORK_DESCRIPTION_V1`, `STREAM_RIGHTS_V1`, `STREAM_PREMIS_V3_PROFILE`, or `STREAM_LIDO_PROFILE_V1`. Museum schemas therefore pin the same fields and vocabularies now and must be replaced or proven byte-compatible when Stream publishes those canonical schema documents.

## Exact on-chain envelope

Museum records intended for a Stream-compatible chain use the exact Stream shapes:

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

The Museum must not create a semantically equivalent but field-incompatible envelope.

## Draft owner-record envelope

The pinned Stream design document publishes this design-level ABI:

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
function recordOwnerRecordFor(
    uint256 tokenId,
    OwnerRecord calldata record,
    address owner,
    uint256 nonce,
    uint64 deadline,
    bytes calldata signature
) external;
function isOwnerRecordNonceUsed(address owner, uint256 nonce) external view returns (bool);
function revokeOwnerRecordNonce(uint256 nonce) external;
function revokeOwnerRecordNonceFor(
    address owner,
    uint256 nonce,
    uint64 deadline,
    bytes calldata signature
) external;

function recordChainHash(uint256 scopeKey, bytes32 recordType)
    external view returns (bytes32 chainHash, uint64 recordCount);
function payloadPointerCount(uint256 scopeKey)
    external view returns (uint256);
function payloadPointerAt(uint256 scopeKey, uint256 index)
    external view returns (
        address pointer,
        bytes32 payloadFamily,
        bytes32 contentHash
    );

event OwnerRecordNonceRevoked(
    address indexed owner,
    uint256 indexed nonce,
    bool relayed,
    uint16 schemaVersion
);

event OwnerRecordRecorded(
    uint256 indexed tokenId,
    bytes32 indexed recordType,
    address indexed owner,
    OwnerRecord record,
    bytes32 recordHash,
    bytes32 recordChainHash,
    bool relayed,
    uint16 schemaVersion
);
```

The corresponding canonical selectors are `0x198c95e3`, `0xf24bb020`,
`0x18544c94`, `0x9d03970a`, and `0x50e9829a`, in declaration order. The
state-read selectors are `0x9d99a291`, `0x9a36f48e`, and `0x6c86be87`,
respectively. In the owner-record host, `scopeKey` is the token ID. Each
`(tokenId, recordType)` lane uses the exact `STREAM_RECORD_CHAIN_V1`
preimage: domain, chain ID, lane-host address, token ID, record type,
previous chain hash, record hash, and zero-based record index, ABI-encoded in
that order. `payloadPointerCount(tokenId)` and
`payloadPointerAt(tokenId,index)` must enumerate every state-backed owner
payload pointer, family, and committed content hash without relying on logs.
The write typehash is
`0x9c8c4f8b7ec1e8731277f53e36271ebf92fc96425f0c082143042400814c6b05`;
the nonce-revocation typehash is
`0x11a07172744cbac614966ef944b190ff3c1b4a7076ab4483c69e48ba2b9ee49c`.
The EIP-712 domain is name `6529StreamOwnerRecords`, version `1`, chain ID,
and the satellite address as verifying contract.

Owner-record `subjectId` is mandatory derived identity, not arbitrary input:

```solidity
bytes32 constant STREAM_SUBJECT_TOKEN_V1 =
    0x1e576f27850d12bc1ec9255ca277dbecfbc84fb3a9a34c474640dfca89811d7e;

bytes32 subjectId = keccak256(abi.encode(
    STREAM_SUBJECT_TOKEN_V1,
    uint256(block.chainid),
    address(core),
    uint256(tokenId)
));
```

Museum bilateral vectors and any future adapter must recompute this value and
reject a declared subject that differs.

These are published draft semantics, not proof of an implemented interface.
The Museum contract specification matches them bilaterally while keeping the
deployment gate closed until Stream provides source, a deployment, an exact
stored-record hash preimage, read surfaces, and a successful write/read
round-trip. A synthetic EIP-712 vector cannot satisfy that gate.

The pinned draft does not yet define the exact `OwnerRecord -> recordHash`
preimage, a state read for the full immutable owner-record row, or an
implemented byte-recovery proof for every pointer row. Those are explicit
deployment blockers. The generic pointer and chain surfaces above are the
minimum published Stream requirements; they do not let the Museum invent the
missing hash preimage or claim archival convergence before Stream publishes
and implements it.

The Museum-side convergence adapter must expose this minimum read interface:

```solidity
function streamCore() external view returns (address);
function ownerRecordBinding(uint256 tokenId) external view returns (
    uint256 collectionId,
    bytes32 streamSubjectId,
    bytes32 ownerRecordHash
);
function ownerRecordHashDomain() external view returns (bytes32);
function ownerRecordHashVectorId() external view returns (bytes32);
```

The registry also uses the pinned Core read directly, independently of the
adapter:

```solidity
function tokenCollectionIdentity(uint256 tokenId) external view returns (
    bool mappingExists,
    uint256 collectionId,
    uint256 collectionSerial,
    bool burned
);
function tokenLifecycle(uint256 tokenId) external view returns (uint8 lifecycle);
```

Governance admits exact Stream Core and adapter addresses, both runtime code
hashes, the owner-record hash domain/vector, and convergence evidence. A
Museum mirror-link call supplies only the existing Museum subject, token ID,
and expected owner-record hash. The registry rechecks both runtimes, reads all
adapter values and Core token identity with bounded exact-length static calls,
requires their collection IDs to match, and independently requires the Core's
exact lifecycle value `MINTED (2)`. `PREPARED_INCOMPLETE (1)` is not an ERC-721
and can be aborted, so it is never mirror-linkable. It derives the Stream
subject itself. It separately reconstructs the exact lowercase
`eip155:<chainId>/erc721:<core>/<tokenId>` identity and requires the supplied
Museum subject to be the already registered CAIP-19 external-asset subject for
that exact string. The caller cannot swap the Museum subject or select a core,
module, collection, Stream subject, hash domain, or vector. The executable
synthetic readback and substitution vectors are in
`specs/onchain/stream_mirror_link_check_v1.py`; they do not open the deployment
gate.

## Shared identifiers

| Concept | Literal | Identifier |
|---|---|---|
| Keccak-256 algorithm | `HASH_KECCAK256` | `1` |
| SHA-256 algorithm | `HASH_SHA256` | `2` |
| JSON canonicalization | `RFC8785_JCS` | `0x886c7c89c308c459ca8a626e0ef36a5ea9f4c7a7b56aaf86c71a2ddf3b4f9044` |
| Owner record type | `ACCESSION` | `0x4dc3a5e33f97bcd06f2d025349086438272d94a398185aca416ae539e36521fb` |
| Token subject domain | `6529STREAM_SUBJECT_TOKEN_V1` | `0x1e576f27850d12bc1ec9255ca277dbecfbc84fb3a9a34c474640dfca89811d7e` |
| Accession schema | `STREAM_ACCESSION_V1` | `0xc04bb48f95c8db4fe7f26a20106533f987003843f2fed36fd6d89f207ddfbd86` |
| Record type | `WORK_DESCRIPTION` | `0x3b172fd545b59c0d525256a31f44b4304ca8e7e06892d1ba171dff45a7f1a9e6` |
| Work-description schema | `STREAM_WORK_DESCRIPTION_V1` | `0x5bb3543c4c007f4396474b74ec81dd8bca13028b6d945020e4b48ff236b26a3c` |
| Record type | `RIGHTS_STATEMENT` | `0x45bc8cdeb4a6cf2cd35075c4e3176254f0ea24f8e938f632c52c83ef8d8434df` |
| Rights schema | `STREAM_RIGHTS_V1` | `0xdfdea1c86219c12e182b4023d399be35bd5602461ef1dc727784c18d7742b967` |
| PREMIS profile | `STREAM_PREMIS_V3_PROFILE` | `0x5df5267e55cdb4ee470cec99deebfeef16d1bb34992fa36b21a3b2e3d38ccc45` |
| LIDO profile | `STREAM_LIDO_PROFILE_V1` | `0xbb318aaa815fbe5cb8cfa584f0102a18948118afe3ba1709cadc6ae36dba22f9` |

Identifiers are `keccak256` of the exact ASCII literal unless Stream assigns a numeric algorithm ID.

## Bilateral ontology profile

The Museum and Stream use the same concepts in both directions:

- **PREMIS v3:** digital preservation Objects, Events, Agents, and Rights. Museum preservation data must round-trip through `STREAM_PREMIS_V3_PROFILE`, including LoC preservation event and outcome vocabularies.
- **LIDO/CDWA-Lite:** the work-description/tombstone record must round-trip through `STREAM_LIDO_PROFILE_V1`. Creator authority references use ULAN, VIAF, or Wikidata; medium/technique uses Getty AAT where available.
- **IIIF Presentation 3:** serious visual works should expose an archival manifest under `STREAM_IIIF_P3_MIN_V1`, with content-addressed painting resources and explicit rights/attribution.
- **BagIt/OCFL:** object dossiers use `STREAM_BAGIT_PROFILE_V1`; SHA-256 and Keccak-256 manifests coexist, and superseding dossiers become new repository versions.
- **C2PA:** optional provenance references remain hash-committed records with explicit validation status.
- **CAIP-19-shaped citation:** `eip155:<chainId>/erc721:<lowercase-core>/<tokenId>`, optionally followed by `@fin:`, `@snap:`, or `@chain:` plus a bytes32 state commitment.

## Shared accession semantics

An accession uses `STREAM_ACCESSION_V1`: accession identifier, acquiring-institution reference, and a `TITLE_BINDING`. The binding separates a legal instrument from the on-chain transfer and records:

- instrument URI/hash and non-sensitive custodian reference;
- block number and transaction hash;
- `from` and `to` addresses;
- the specific transfer to which legal title evidence relates.

The acquisition packet remains distinct from the accession statement. It includes chain identity, record-chain heads, finality/content roots, attribution, rights completeness, fixity/preservation coverage, ownership history, title bindings, work description, condition records, recovery lineage, and platform-sustainability evidence where applicable.

### Limited Museum gift authorization

`GIFT_ACCEPTANCE_AUTHORIZATION` is a versioned Museum-local envelope profile
for a formally accepted gift whose Stream `ACCESSION` completion certificate is
not yet evidence-backed. It is intentionally not an alternate spelling of
`STREAM_ACCESSION_V1`: it cannot carry an executed title binding, a signed
authority claim, or an `accessioned` lifecycle assertion. It records the
effective acceptance decision and its limitations while independent
documentation QA remains pending.

## Shared provenance-entry format

Human-facing provenance histories use the Stream manifest shape:

```json
{
  "entry_id": "stable-entry-id",
  "entry_type": "curation",
  "occurred_at": "2026-07-09T12:00:00Z",
  "title": "Selected by TDH vote",
  "description": "Selection is not accession.",
  "evidence_refs": [
    {
      "label": "Wave result",
      "uri": "https://6529.io/...",
      "sha256": "not_available_local",
      "notes": "Live API status observed at the stated snapshot."
    }
  ]
}
```

Museum-specific event types may extend Stream's vocabulary only through a versioned profile with an explicit PREMIS mapping. Existing Stream terms and meanings are never redefined.

## Convergence gate

Before deploying a Museum contract or publishing a completed accession on Stream:

1. vendor or content-address the canonical Stream profile documents;
2. compare schema IDs and document hashes against the active Stream system manifest;
3. validate Museum → Stream → PREMIS/LIDO export round trips;
4. regenerate the acquisition packet and object dossier without operator-only data;
5. reject deployment if any shared field, vocabulary, hash, or subject derivation has drifted.
6. for owner records, pin the implemented module source and deployment, verify
   runtime code, confirm the stored-record hash preimage, the full immutable
   record read, `recordChainHash`, `payloadPointerCount`, and
   `payloadPointerAt`, and pass exact direct, relayed, nonce-revocation,
   state-only payload recovery, write/read round-trip, and Museum-side adapter
   readback/substitution vectors.
