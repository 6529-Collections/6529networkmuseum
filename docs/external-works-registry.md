# External works registry

Status: working architecture; no contract deployed
Working name: `NetworkMuseumRegistry`

## Why a separate contract is required

6529Stream is a primary-minting protocol. Its current `StreamPreservationRecords` implementation is constructed against one `StreamCore`, accepts a Stream `collectionId`, and rejects records for collections that do not exist in that Core.

Museum donations and secondary acquisitions usually remain tokens of their original contracts—and may live on non-EVM chains. The Museum therefore needs an on-chain registry for institutional records about externally minted works.

The registry must not wrap or remint the work. A wrapper would create a second token identity and introduce custody, bridge, marketplace, title, and interpretation risk. The original asset remains the object of record; the Museum contract records governed claims about it.

## Design objective

Create one token-agnostic, chain-agnostic, append-only registry that:

- identifies external assets without taking over their token contract;
- publishes Museum governance, program, accession, object, rights, and preservation commitments;
- uses Stream's exact `HashRef` and record envelope;
- reuses Stream museum schemas wherever concepts overlap;
- supports external ERC-721/1155, legacy EVM assets, Bitcoin/Counterparty assets, and future chain namespaces;
- never treats registration as proof of custody, title, rights, or accession by itself.

## Asset identity

Use CAIP-2 for chain IDs, CAIP-19 for asset types/IDs, and CAIP-10 for custody accounts wherever a registered namespace profile exists:

- Ethereum ERC-721 example: `eip155:1/erc721:0x06012c8cf97BEaD5deAe237070F9587f8E7A266d/771769`
- Ethereum custody account example: `eip155:1:0x...`
- Bitcoin mainnet chain example: `bip122:000000000019d6689c085ae165831e93`

References: [CAIP-2](https://standards.chainagnostic.org/CAIPs/caip-2), [CAIP-10](https://standards.chainagnostic.org/CAIPs/caip-10), [CAIP-19](https://standards.chainagnostic.org/CAIPs/caip-19).

CAIP-19 itself does not require canonical address casing. The Museum profile must therefore pin normalization per chain/asset namespace before subject derivation. For EVM subjects, use lowercase contract addresses in canonical work citations while retaining an EIP-55 display form separately.

For legacy or unprofiled asset classes, a versioned Museum namespace profile may be registered only with:

- a deterministic canonical string;
- a resolution procedure;
- collision and normalization rules;
- worked vectors;
- explicit chain and asset-standard references;
- governance approval.

Do not invent an ad hoc identifier in an individual accession record.

## Subject derivation

Illustrative derivation:

```solidity
bytes32 constant MUSEUM_SUBJECT_EXTERNAL_ASSET_V1 =
    keccak256("6529networkmuseum.subject.external-asset.v1");

function externalAssetSubjectId(string memory canonicalAssetId)
    pure
    returns (bytes32)
{
    return keccak256(
        abi.encode(
            MUSEUM_SUBJECT_EXTERNAL_ASSET_V1,
            keccak256(bytes(canonicalAssetId))
        )
    );
}
```

Other domain-separated subject types should cover institution, policy, governance decision, approved collection, accession program, program outcome, accession lot, and restricted-instrument commitment.

The original canonical asset ID remains stored in or recoverable from the payload. A hash alone is not a usable catalogue identifier.

## Record envelope

Use the Stream structure without renaming or reordering fields:

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

The contract may call this a Museum record in prose, but ABI compatibility should be preserved. Supersession, evidence references, and correction reasons belong in the schema-identified payload so the shared envelope does not fork.

Meaning-bearing records should support a payload-carrying write that verifies and retains small canonical bytes where economically reasonable. Larger dossiers live on content-addressed storage with on-chain hash/URI commitments.

## Required state and events

```solidity
function recordMuseumRecord(CollectionRecord calldata record)
    external
    returns (bytes32 recordHash);

function recordMuseumRecordWithPayload(
    CollectionRecord calldata record,
    bytes calldata payload
) external returns (bytes32 recordHash);

function record(bytes32 recordHash)
    external view
    returns (CollectionRecord memory);

function payload(bytes32 recordHash)
    external view
    returns (bytes memory);

function latestRecordHash(bytes32 recordType, bytes32 subjectId)
    external view
    returns (bytes32);

function recordChainHead(bytes32 recordType, bytes32 subjectId)
    external view
    returns (bytes32);
```

Every accepted write emits the full envelope, `recordHash`, previous/new chain head, recorder, authorization class, recorded time, and schema version. State reads—not event logs alone—must recover every committed payload/pointer and current chain head.

Duplicate record hashes revert. Latest means last accepted record, while `effectiveAt` remains the asserted effective time. Corrections are new records with payload-level supersession.

## Record families

Museum-native families:

- `MUSEUM_POLICY`
- `GOVERNANCE_DECISION`
- `APPROVED_COLLECTION`
- `ACCESSION_PROGRAM`
- `PROGRAM_OUTCOME`
- `ACCESSION_LOT`
- `EVIDENCE_ASSERTION`

Shared Stream families, unchanged:

- `ACCESSION` / `STREAM_ACCESSION_V1`
- `DEACCESSION` / `STREAM_DEACCESSION_V1`
- `WORK_DESCRIPTION` / `STREAM_WORK_DESCRIPTION_V1`
- `RIGHTS_STATEMENT` / `STREAM_RIGHTS_V1`
- `CONDITION_REPORT` / `STREAM_CONDITION_REPORT_V1`
- exhibition, loan, valuation, artist-intent, interview, IIIF, PREMIS, dossier, acquisition-packet, and BagIt profiles.

Museum-specific schemas may extend a shared payload through an explicit profile, but they must not redefine shared fields or vocabularies.

## Authority model

Authorization is record-family-specific:

| Family | Expected authority |
|---|---|
| Policy and governance decision | Museum governance executor |
| Approved collection and program | Governance executor or explicitly delegated program authority |
| Program outcome | Bound program decision mechanism |
| Accession lot | Museum registrar/custody authority under approved policy |
| Object accession | Museum registrar/custody authority, with custody verification result |
| Artist intent / artist statement | Artist, estate, or verified successor |
| Rights | Rights holder or instrument-backed institutional statement |
| Preservation/condition | Museum conservator or attributable independent attestor |
| Correction | Original authority or approved successor, with supersession |

Support direct and relayed EIP-712 writes, ERC-1271 contract-wallet signatures, unordered signer-scoped nonces, deadlines, nonce revocation, and authority rotation. Authorization class is permanent record metadata.

## Custody verification

Registration is never custody proof. Each accession payload carries a typed custody-verification result.

Recommended adapters:

- ERC-721: `ownerOf(tokenId)` equals the configured Museum custody account;
- ERC-1155: `balanceOf(custody, tokenId)` meets the accessioned quantity;
- CryptoPunks/legacy EVM: contract-specific read adapter approved by registry governance;
- cross-chain assets: chain-specific proof or attributable independent attestation with block/height, account, method, and evidence hash.

Adapters report evidence; they do not redefine legal title. Custody date, title-passage date, and accession date remain separate.

The contract should permit a record that says custody is pending or unverified, but an `accessioned` state transition must fail unless the active Museum accession schema's completion gate is satisfied.

## Schema and hash discipline

- Pin JSON schemas as immutable, hash-identified documents.
- Default off-chain JSON to RFC 8785 JCS and Keccak-256 (`algorithm = 1`).
- Retain SHA-256 alongside Keccak-256 in BagIt/repository manifests.
- Never reuse algorithm, canonicalization, schema, record-type, authority, or subject-profile identifiers.
- Accept a new identifier only through append-only registry governance.
- Reject malformed digest lengths, empty canonicalization IDs, oversized payloads, and unknown schemas.

## Relationship to Stream-native works

If the Museum later acquires a work minted by Stream:

1. the original Stream CAIP-19 citation remains the work identity;
2. the Museum writes the canonical accession/object payload through Stream's owner-record surface when available;
3. the Museum registry may record the institutional accession lot and a cross-reference to the Stream record hash;
4. both sides use the same canonical payload hash and schema ID;
5. neither registry creates a replacement token.

“Bilateral” means payloads and ontologies round-trip and hashes can match. Host-specific record hashes may legitimately differ because each contract has its own domain separator and chain context.

## Public/restricted boundary

The chain stores no private donor data, full non-public instrument, appraisal figure, key material, signer security detail, or sensitive storage location. It may store:

- a public redacted statement;
- a hash of the restricted instrument;
- execution/effective dates;
- rights/condition summary;
- a non-sensitive custodian reference;
- review/approval status.

## Non-goals

- Minting a Museum wrapper NFT.
- Replacing original ownership or marketplace state.
- Treating a record as proof of legal title without an instrument.
- Enforcing copyright or licence terms through token transfer restrictions.
- Publishing private registrar information.
- Hard-coding current Safe signers or a permanent governance mechanism.

## Deployment gates

Before deployment:

1. finalize subject derivations and cross-chain identifier profiles;
2. publish canonical schemas and worked vectors;
3. resolve exact bilateral schema hashes with Stream;
4. threat-model authority rotation, record spam, schema capture, URI substitution, replay, and false custody claims;
5. test EOA/Safe/ERC-1271 writes and revocations;
6. round-trip accession/object records through PREMIS and LIDO;
7. regenerate a BagIt/OCFL object dossier from chain state without operator-only data;
8. conduct registrar and digital-conservation practitioner review;
9. complete an independent security audit;
10. obtain explicit Museum governance approval for deployment and migration.
