# 6529Stream interoperability

## Relationship to the Museum data architecture

The Museum's normative semantic profile is [How the Museum knows and cares for
art](data-architecture.md) and its machine-readable
[`6529NM_DATA_ARCHITECTURE_V1`](data-architecture/profile.json) register. That
profile is defined independently of Stream and controls Museum meanings,
extension terms, implementation states, and conformance claims.

This document governs downstream compatibility with Stream's exact envelopes,
hash references, subject derivation, and deployed contract surfaces. After the
Museum profile is released, a separate field-by-field review will map Stream to
it in both directions. A Stream term that does not preserve the Museum meaning
requires an adapter or an explicit divergence; it does not silently redefine
the Museum record.

## Pinned source

The executable adapter profile is pinned to `6529-Collections/6529Stream`
commit `f610e04979bf9a8f4f48b31131e7e0e8f78bac43`, inspected 2026-08-08 UTC.
The pin is deliberate: later Stream changes require a new field-by-field review
and new independent ABI vectors before this profile can advance.

Normative Stream sources at that commit:

- `smart-contracts/interfaces/stream/IStreamPreservationRecords.sol`
- `smart-contracts/domains/preservation/StreamPreservationRecords.sol`
- `smart-contracts/domains/metadata/StreamMetadataRenderer.sol`

Stream implements the generic `CollectionRecord` preservation envelope and its
record-family/writer admission boundary. At the pinned commit it does not
publish standalone canonical JSON Schema files for `STREAM_ACCESSION_V1`,
`STREAM_WORK_DESCRIPTION_V1`, `STREAM_RIGHTS_V1`,
`STREAM_PREMIS_V3_PROFILE`, or `STREAM_LIDO_PROFILE_V1`. The Museum's PREMIS
and LIDO correspondences therefore remain proposed mappings. They are not
called exports or round trips until exact schemas, adapters, and fixtures exist.

## Exact on-chain envelope

The output of the Museum-to-Stream adapter uses the exact Stream shapes:

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

## Proposed ontology crosswalk

The Museum uses concepts that can support future Stream, PREMIS, and LIDO
exports. The following are design requirements rather than implemented
bilateral adapters:

- **PREMIS v3:** proposed mappings cover digital-preservation Objects, Events,
  Agents, and Rights, including Library of Congress preservation-event and
  outcome vocabularies. `STREAM_PREMIS_V3_PROFILE` is a reserved profile
  identifier until Stream publishes the profile and the Museum ships exact
  export/import fixtures.
- **LIDO/CDWA-Lite:** proposed mappings cover work descriptions, object
  identification, actors, events, and collection relationships. Creator
  authority references may use ULAN, VIAF, or Wikidata; medium and technique
  may use Getty AAT. `STREAM_LIDO_PROFILE_V1` is not called implemented until
  an exact schema and round-trip fixtures exist.
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
3. implement and validate Museum to Stream to PREMIS/LIDO export round trips;
4. regenerate the acquisition packet and object dossier without operator-only data;
5. reject deployment if any shared field, vocabulary, hash, or subject derivation has drifted.
6. for owner records, pin the implemented module source and deployment, verify
   runtime code, confirm the stored-record hash preimage, the full immutable
   record read, `recordChainHash`, `payloadPointerCount`, and
   `payloadPointerAt`, and pass exact direct, relayed, nonce-revocation,
   state-only payload recovery, write/read round-trip, and Museum-side adapter
   readback/substitution vectors.

## External rights vocabulary

The Museum's [`docs/rights/registry.json`](rights/registry.json) records
Creative Commons licenses and tools, RightsStatements.org terms, a no-public-
license case, and custom terms. These are external legal instruments or public
status labels. The Museum preserves their canonical URIs and meanings.

The registry does not change `STREAM_RIGHTS_V1`. The Stream-compatible
`RIGHTS_STATEMENT` remains the object-specific determination: who is understood
to hold the relevant right, the evidence for that conclusion, and the practical
grant status for Museum uses. A separate object assignment connects that
reviewed record to an external expression. This keeps three facts distinct:

- the external license or status term;
- the Museum's evidence that the term applies to a particular object;
- the use-by-use determination in the Stream-compatible rights record.

A future bilateral Stream field should carry the canonical external URI and
the component to which it applies. Until Stream publishes and pins that field,
the Museum registry remains an off-chain publication vocabulary and must not be
inserted into the shared envelope under an invented extension.

## Temporary generative-study display divergence

The first **Inside the System** release packages project study definitions and
compact edition indexes in the versioned frontend. This is a derived display
layer backed by pinned Museum evidence, not a Stream record envelope and not a
source of accession, title, custody, rights, or governance assertions.

The convergence target is an optional atomic project-study profile that can be
extended when later acquisitions from the same project arrive. Until that
profile exists, the frontend package must retain exact source snapshot and
reviewed descriptor identities, label synthetic views **Museum model**, and
must not be promoted or interpreted as a canonical Stream record.

## PUBLIC_ENTITY/PUBLIC_RELATION bilateral profile

WP-1 uses `PUBLIC_ENTITY` and `PUBLIC_RELATION` as a Museum-native publication
layer designed for deterministic conversion to Stream. The Museum's off-chain
record remains `{envelope,payload}`. It is not ABI-identical to
`CollectionRecord`: the readable Museum `recordType` is converted to a pinned
`bytes32` value; JSON hex values are decoded into the corresponding Solidity
types; and the Museum's legacy unsigned placeholder is normalized to Stream's
zero-scheme, empty-hash convention. `schemaId`, `subjectId`, `contentHash`, and
`effectiveAt` retain their meanings through the conversion. The public schema
commitments are the Keccak-256 commitments to `PUBLIC_ENTITY_V1` and
`PUBLIC_RELATION_V1`.
`WAVE_STATUS_OBSERVATION` uses the same envelope for an append-only source
observation and preserves its prior observation rather than rewriting it.

`scripts/stream_adapter.py` tests one precise direction: Museum envelope plus
exact reviewed-source proof to normalized Stream `CollectionRecord`, then
Stream struct to its normalized semantic JSON representation. It also checks
the exact `abi.encode(record)` layout and Stream v2 record-hash preimage against
an independently computed fixed record-hash golden constant. It does not claim
a lossless conversion from an arbitrary Stream record back to the original
Museum payload or evidence package.

An immutable raw-source URI is an admission proof, not merely a string. The
adapter requires the exact full lowercase Git commit, an exact regular Git
blob, the source envelope and payload, and the exact source root/path. Before
that URI may enter semantic normalization, ABI encoding, or record-hash
derivation, the commit's `release-artifacts/latest/record-manifest.json` must
have internally consistent SHA-256 and Keccak/JCS body commitments, and its
source entry must match the exact repository-relative path, normalized byte
size, declared byte mode, and SHA-256. The source blob must then parse as one
strict JSON object whose envelope and payload equal the supplied proof, and
the payload must match the envelope content commitment. ABI/hash helpers
require this proof again when handed an existing raw URI; a raw URI cannot be
admitted by shape validation alone.

Source paths are literal POSIX paths only. URL query/fragment delimiters
(`?`, `#`) and percent-encoded equivalents are rejected, as are pathspec,
traversal, separator, and control-character ambiguities. Stable Museum logical
record URIs remain an explicit off-chain mode and do not establish Stream
admission. Every Python value entering a Stream integer ABI slot is an actual
integer, never a Boolean; the JSON Schema states the same closed-type rule.

The proposed crosswalk is typed:

| Museum projection | Tested Stream boundary and proposed PREMIS/LIDO correspondence |
|---|---|
| `PUBLIC_ENTITY` identity and closed profile | Stream `CollectionRecord` envelope; LIDO object/actor identity views; no claim that the Museum profile is already an on-chain Stream schema |
| `PUBLIC_RELATION` endpoint and qualifier | LIDO event/actor/object or object/object relationship view; relation direction, cardinality, and evidence remain Museum constraints |
| Work component/manifestation references | PREMIS Object/Representation identity and LIDO digital-object/physical-digital boundary; a token, derivative, or metadata response is not silently promoted to the Work |
| `MEDIA_REFERENCE` | PREMIS Object, Event, Rights, and fixity boundary; role, source observation, retrieval/fixity, rights, accessibility, and affordances remain separate facts |
| Artist/Organization/Agent profiles | LIDO actor/name/role mapping; typed Artist and Organization identities are not collapsed into a generic Agent |
| Accession and Collection relations | PREMIS event/rights/custody evidence plus LIDO collection/object relations; membership requires an actual accession relation |

Any future PREMIS or LIDO exporter must preserve the Museum ID, source alias,
evidence URI/path, source observation time, rights status, and independent
lifecycle facts in both directions. A historical Wave proposal presentation image maps to a public
presentation object with a restricted affordance allowlist and the
non-licensing `open_wave_proposal_context` locator. The signed-drop API
publication observation preserves the exact retained part/source hashes and
actual CloudFront presentation URLs, while the Arweave URI remains a separate
token-linked/source locator. API-reported `is_signed:true` is not an independent
signature or license determination; the media cannot become a downloadable
preservation master, a title/custody assertion, or an accession through
serialization.
Unknown profiles, relations, media roles, affordances, algorithms, and
algorithm/digest pairs fail closed. Future Stream admission requires a
field-by-field schema comparison, deterministic JCS/Keccak commitment check,
implemented PREMIS/LIDO round trip, and readback of the exact source/evidence
boundaries.
