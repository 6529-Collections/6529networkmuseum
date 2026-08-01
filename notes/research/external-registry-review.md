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
3. Asset profiles admit only immutable, non-proxy canonicalizers. Admission
   and registration bind direct `extcodehash`, scan runtime opcodes for proxy,
   storage, external-call, creation, and environment dependence, require mode
   `0`/zero implementation hash, and never trust a self-reported implementation
   or version hash.
4. The URI rule is now the versioned Museum-specific
   `MUSEUM_URI_SAFETY_PUBLIC_V1` predicate, with an exact HTTPS public-network
   assertion record and EIP-712 signature format plus explicit Stream-adapter
   convergence behavior.
5. The manifest fixture uses actual 40-hex Git SHA-1 values for the source and
   pinned Stream commits, right-aligned into `bytes32`; the root was
   independently recomputed. The source is the intended Museum release
   baseline `origin/main` at `ff1c5825e3b61bfb2df0a639e057297beb946e4d`, not
   the PR head; the transcript asserts both that source pin and the resulting
   root so a self-referential manifest cannot be inferred.

6. The pinned Stream evidence was checked at commit
   `5021c8060950c3fef995271e674ed4b2007fee6d`: the generic
   `CollectionRecord` field order is published at
   `smart-contracts/IStreamPreservationRecords.sol:18-28`; the generic
   preservation domain literal is at
   `smart-contracts/StreamPreservationRecords.sol:22-29`; and its generic
   `abi.encode` preimage is at `smart-contracts/StreamPreservationRecords.sol:210-231`.
   The pinned source does not publish an owner-record selector, owner-module
   ABI, or owner-specific preimage. §13.5 is consequently a provisional Museum
   proposal only and is closed behind the §2.1 convergence gate; no inferred
   Stream owner behavior is normative.

7. Museum's `payloadMode` and `supersedesRecordHash` are Museum-only hash
   fields. The Museum and pinned Stream preimages are intentionally not
   positionally ABI-tuple aligned; bilateral equality is limited to named
   shared ontology/profile fields and canonical payload bytes.

8. The provisional owner-record vector prints `chainId = 1`; the independent
   transcript binds the same value through `$ownerChainId = 1` in the ABI
   preimage. It is still not a Stream compatibility vector.

9. Every function selector in the §7 ABI, including the complete
   `TransitionTargetInput`, `RecordInput[]`, `CollectionRecord`, and by-signature
   tuple forms, is covered by the executable golden selector transcript below.

The next exact-head review required and resolved:

1. Authority and successor transitions now queue/store complete target
   commitments: address, expected runtime code hash, ERC-165/interface ID,
   deterministic probe hash, predecessor linkage (`predecessorRegistry` must
   be this registry and the provider must report that same address), evidence hash, authority
   revision, proposer, and time. Execution repeats all checks; only pre-
   execution cancellation is a rollback, and emergency handling is freeze plus
   a validated successor. EOA/arbitrary targets are rejected.
2. Families now have governed STREAM/MUSEUM kind, allowed bitmap, revision,
   and authority revision; every record type selects exactly one class. Direct
   and relayed writes call the same writer primitive, and relayed EIP-712 binds
   class and family revision.
3. HTTPS is enforced on-chain through resolver profiles, bounded TTLs, signed
   assertions, sorted address-array commitments, current URI pointers, and
   record-side assertion hash/revision state. A golden HTTPS vector was added.
4. External assets, mirror links, and provisional owner-record interface
   admissions persist and emit their actual global role IDs and authority
   revisions; the new enforceability matrix maps each control to ABI/state,
   checks, and events.

5. The inline fixture was corrected to raw exact UTF-8 bytes (46 bytes), not a
   shell-parsed JSON value; the payload, record, chain, owner, manifest,
   HTTPS, and batch dependents were recomputed from those bytes by both
   Foundry `cast` and `Crypto.Hash.keccak`/`eth_abi`.
6. `familyKind` is the closed numeric `uint8` enum `1 = STREAM`, `2 = MUSEUM`,
   with zero and 3--255 reserved/rejected. Successors commit a strictly new
   module version, exact predecessor, and unchanged protocol/Stream commit;
   authority targets persist the capability handshake and full state view.
7. HTTPS assertions are per-URI, nonce/deadline/revision/predecessor-bound,
   EOA/ERC-1271 checked with callback dependency rechecks, and duplicate-safe;
   batches have an ordered dynamic-array commitment, persisted used/commitment
   state, count/bytes/gas caps, and all-or-nothing retry semantics.
8. V1 corrections enforce only envelope-level same-lane older-target lineage;
   semantic payload supersession remains release-gated unless a future pinned
   validator/proof interface is admitted. The Cancun canonicalizer policy now
   explicitly bans environment, code-introspection, returndata, state,
   external-call, creation, blob, gas, and logging opcodes, with exact
   extcodehash allowlisting primary and scanning defense-in-depth.

### Reproducible custom-error and interface-ID checks

The following check parses only the normative error declarations above, strips
parameter names to obtain the canonical ABI signatures, recomputes every
custom-error selector with Foundry `cast`, and verifies that no selector is
ambiguous. It also recomputes the two published ERC-165 interface IDs by XORing
the exact function selectors. It is intentionally separate from the function
selector map so an error or interface change cannot be hidden by a display
alias.

```powershell
@'
import re, subprocess
from pathlib import Path

spec = Path('specs/onchain/contract-migration-v1.md').read_text(encoding='utf-8')
error_block = re.search(r'### 7\.1 Required errors.*?```solidity\n(.*?)```', spec, re.S).group(1)
signatures = []
for name, args in re.findall(r'error\s+(\w+)\((.*?)\);', error_block, re.S):
    types = [arg.strip().split()[0] for arg in args.replace('\n', ' ').split(',') if arg.strip()]
    signatures.append(f"{name}({','.join(types)})")
selectors = [subprocess.check_output(['cast', 'sig', sig], text=True).strip() for sig in signatures]
assert 'error InvalidHashRef(' not in error_block
assert len(selectors) == len(set(selectors))

interfaces = {
    'IMuseumAuthorityProviderV1': [
        'isMuseumAuthorityProvider()', 'registry()', 'authorityRevision()',
        'capabilityHandshake(address,bytes32,bytes32,bytes32)'],
    'IMuseumSuccessorV1': [
        'isNetworkMuseumRegistry()', 'registryVersion()', 'protocolVersion()',
        'streamCompatibilityCommit()', 'moduleSupersedes()']}
expected = {'IMuseumAuthorityProviderV1': '0xea450898', 'IMuseumSuccessorV1': '0x573d91cc'}
for name, sigs in interfaces.items():
    value = 0
    for sig in sigs:
        value ^= int(subprocess.check_output(['cast', 'sig', sig], text=True).strip(), 16)
    actual = f'0x{value:08x}'
    assert actual == expected[name], (name, actual, expected[name])
print(f'customErrorSelectors={len(selectors)} unique')
for name, value in expected.items(): print(name, value)
'@ | python -
```

### Reproducible ABI selector transcript

Run this from a clean PowerShell session with Foundry `cast`. The map is the
golden output for every function in the exact §7 ABI; a signature spelling or
tuple member/order change fails the check.

```powershell
$selectorGolden = [ordered]@{
  'isNetworkMuseumRegistry()' = '0xedc7801f'
  'registryVersion()' = '0x0f9be51c'
  'protocolVersion()' = '0x2ae9c600'
  'streamCompatibilityCommit()' = '0xc8e1a0da'
  'moduleSupersedes()' = '0x57699215'
  'authority()' = '0xbf7e214f'
  'authorityRevision()' = '0x48de7dbc'
  'authorityState()' = '0xa865a4c7'
  'successor()' = '0x6ff968c3'
  'writesFrozen()' = '0x290d086b'
  'pendingAuthority()' = '0xfabb94bb'
  'successorTarget()' = '0xae540c6b'
  'externalAssetSubjectId(bytes32,string)' = '0x0b88b5e8'
  'registerExternalAsset(bytes32,string,bytes32)' = '0x73c0a0b4'
  'externalAsset(bytes32)' = '0xdb08b0b0'
  'admitAssetProfile(bytes32,bytes32,bytes32,string,address,uint8,bytes32,bytes32,bytes32)' = '0xba597a03'
  'assetProfile(bytes32)' = '0x2938cf75'
  'admitSchema(bytes32,bytes32,string,bool)' = '0x541fd287'
  'schema(bytes32)' = '0x072b9cf2'
  'admitRecordFamily(bytes32,uint8,uint16)' = '0x63d20b1a'
  'recordFamily(bytes32)' = '0x1ca9f8aa'
  'admitRecordType(bytes32,bytes32,bytes32,uint8)' = '0x46a9f249'
  'recordTypePolicy(bytes32)' = '0xcd2369a6'
  'setRecordFamilyGrant(bytes32,uint8,address,bool)' = '0x40ee7ee3'
  'recordFamilyGrant(bytes32,uint8,address)' = '0x1118ed2f'
  'setAuthority((address,bytes32,bytes4,bytes32,bytes32,address,bytes32,bytes32))' = '0x81a86ff4'
  'executeAuthority()' = '0xc9dc7d0d'
  'cancelAuthority()' = '0xf0edf065'
  'setGlobalRoleGrant(bytes32,address,bool)' = '0xab6627c3'
  'globalRoleGrant(bytes32,address)' = '0x59d2fe4a'
  'admitHttpsResolverProfile(bytes32,bytes32,address,uint64,uint64)' = '0xaf2fb948'
  'resolverProfile(bytes32)' = '0x3711d316'
  'recordHttpsAssertionBySig(string,bytes32,bytes32,uint64,bytes32,uint64,bytes32,uint64,uint64,address,uint256,uint64,address[],bytes)' = '0x1e0c9fe6'
  'httpsAssertion(bytes32,bytes32,uint64,uint64)' = '0x1120d46d'
  'currentHttpsAssertion(bytes32)' = '0x080dab7b'
  'httpsAssertionByHash(bytes32)' = '0x28208c17'
  'admitStreamOwnerRecordInterface(address,bytes32,bytes32,bytes32)' = '0x75c75961'
  'streamOwnerRecordInterface()' = '0xfbab3335'
  'streamOwnerRecordInterfaceAtRevision(uint64)' = '0x7940fbb2'
  'recordMuseumRecord((bytes32,bytes32,(uint16,bytes,bytes32),string,bytes32,bytes32,(uint16,bytes,bytes32),uint64),bytes32,uint8,bytes32)' = '0x29f319b0'
  'recordMuseumRecordWithPayload((bytes32,bytes32,(uint16,bytes,bytes32),string,bytes32,bytes32,(uint16,bytes,bytes32),uint64),bytes32,uint8,bytes32,bytes)' = '0x82447563'
  'recordMuseumRecordBySig((bytes32,bytes32,(uint16,bytes,bytes32),string,bytes32,bytes32,(uint16,bytes,bytes32),uint64),bytes32,bytes32,bytes32,address,uint8,uint64,uint256,uint64,bytes,uint8,bytes32,bytes)' = '0x20f3cc85'
  'recordMuseumRecordBatch(((bytes32,bytes32,(uint16,bytes,bytes32),string,bytes32,bytes32,(uint16,bytes,bytes32),uint64),bytes32,uint8,bytes32,bytes)[],bytes32)' = '0xb12754c9'
  'batchIdUsed(bytes32)' = '0xd4b4d9f4'
  'batchCommitment(bytes32)' = '0x70ad2bd4'
  'deriveMuseumRecordHash((bytes32,bytes32,(uint16,bytes,bytes32),string,bytes32,bytes32,(uint16,bytes,bytes32),uint64),uint8,bytes32)' = '0x4bc9025c'
  'latestRecordHash(bytes32,bytes32)' = '0xaec646e8'
  'recordChainHead(bytes32,bytes32)' = '0xb9f4933e'
  'recordSummary(bytes32)' = '0x45fafe2f'
  'record(bytes32)' = '0xb5c645bd'
  'payload(bytes32)' = '0x9f165a87'
  'setStreamMirrorLink(bytes32,address,address,uint256,uint256,bytes32,bytes32,bytes32,bytes32)' = '0x49c44b5c'
  'streamMirrorLink(bytes32)' = '0xfc584dc4'
  'revokeNonce(uint256)' = '0x05c1ee20'
  'revokeNonces(uint256[])' = '0xac7410a1'
  'revokeNonceBySig(address,uint256,uint64,bytes)' = '0xc75a6797'
  'nonceRevocation(address,uint256)' = '0x51b366d4'
  'setSuccessor((address,bytes32,bytes4,bytes32,bytes32,address,bytes32,bytes32))' = '0x43dd6c37'
  'freezeWrites()' = '0x05d53fba'
}
foreach($signature in $selectorGolden.Keys) {
  $actual = cast sig $signature
  if($actual -ne $selectorGolden[$signature]) {
    throw "selector mismatch for $signature`: $actual != $($selectorGolden[$signature])"
  }
  "$actual  $signature"
}
```

### Reproducible hash transcript

This transcript was run in a clean PowerShell session with Foundry `cast`.
The commands use only the literals, ABI types, and values printed here; they
do not read repository state or rely on an implementation. The output is the
golden vector set for the draft.

```powershell
git cat-file -e 'ff1c5825e3b61bfb2df0a639e057297beb946e4d^{commit}'
if ($LASTEXITCODE -ne 0) { throw 'Museum release/source baseline is absent' }

$domain = '0x0c86cc4258c69b4674aa86e715d4d167bd8288b78832a0a4c5a37943b31876c4'
$chainDomain = '0x4bc9065a5ebf49c9fff664fca90b1a40c0edac25bd076026f1b2685de7db666a'
$subjectDomain = '0x1dd722ea239e47e25bdadfcc0053bdc4e7ee75e7ca9dd0afe97076a6d9eb8a80'
$assetProfile = '0xac72cc7c2b027b8ee3d459de7829fd7b3b31cf575c28734e736ebd33b10f41cc'
$canon = '0x886c7c89c308c459ca8a626e0ef36a5ea9f4c7a7b56aaf86c71a2ddf3b4f9044'
$type = '0x5a50f1234f1c89b5d9c2f5b2062279349feac41d8e01bf708ee9adc20a2d8ba0'
$subject = '0x1111111111111111111111111111111111111111111111111111111111111111'
$schema = '0xe3d3da75ee91ec6a7603f809eb413342e42874cabf3992d443409657745c3cf0'
$asset = 'eip155:1/erc721:0x06012c8cf97bead5deae2370709587f8e7a266d/771769'
$payloadUtf8Hex = '0x7b226964223a22363532394e4d2e323032362e3030312e31222c22737461747573223a2270726f706f736564227d'
$payloadUtf8Length = 46
$uri = 'ipfs://bafybeigdyrzt5example'
$assetHash = cast keccak $asset
$externalSubjectId = cast keccak (cast abi-encode 'f(bytes32,bytes32,bytes32)' $subjectDomain $assetProfile $assetHash)
$contentDigest = cast keccak $payloadUtf8Hex
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
$writeTypeHash = cast keccak 'MuseumRecordWrite(bytes32 recordHash,bytes32 recordType,bytes32 subjectId,bytes32 previousRecordHash,uint8 authorizationClass,uint64 familyRevision,uint256 nonce,uint64 deadline)'
$structHash = cast keccak (cast abi-encode 'f(bytes32,bytes32,bytes32,bytes32,bytes32,uint8,uint64,uint256,uint64)' $writeTypeHash $recordHash $type $subject 0x0000000000000000000000000000000000000000000000000000000000000000 12 1 7 1800000000)
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
$payloadBytesHash = cast keccak $payloadUtf8Hex
$entryHash = cast keccak (cast abi-encode 'f(bytes32,uint64,bytes32,bytes32,uint8,bytes32)' $manifestEntryDomain 1 $pathHash $recordHash 1 $payloadBytesHash)
$sourceCommitHex = 'ff1c5825e3b61bfb2df0a639e057297beb946e4d'
# This is the synchronized Museum release/source baseline (origin/main), not
# the PR head. The PR head must never be substituted into this fixture.
$expectedSourceCommitHex = 'ff1c5825e3b61bfb2df0a639e057297beb946e4d'
if ($sourceCommitHex -ne $expectedSourceCommitHex) { throw "unexpected source baseline: $sourceCommitHex" }
$streamCommitHex = '5021c8060950c3fef995271e674ed4b2007fee6d'
$sourceCommit = '0x'+('0'*24)+$sourceCommitHex
$streamCommit = '0x'+('0'*24)+$streamCommitHex
$generatorHash = cast keccak 'museum-migration/1.0.0'
$manifestRoot = cast keccak (cast abi-encode 'f(bytes32,bytes32,bytes32,bytes32,uint64,bytes32[])' $manifestRootDomain $sourceCommit $streamCommit $generatorHash 1 "[$entryHash]")
$expectedManifestRoot = '0x9743e8c811e3bc2760c438012d1ad61a265b385f903e02d823aa5664be5bcd7d'
if ($manifestRoot -ne $expectedManifestRoot) { throw "manifest root mismatch: $manifestRoot" }
$ownerDomain = cast keccak '6529networkmuseum.stream-owner-record.v0'
$ownerVector = cast keccak 'STREAM_OWNER_RECORD_HASH_VECTOR_V0'
$ownerChainId = 1
$ownerStreamCore = '0x0000000000000000000000000000000000001001'
$ownerModule = '0x0000000000000000000000000000000000002002'
$ownerSubject = '0x1111111111111111111111111111111111111111111111111111111111111111'
$ownerPayloadUtf8Hex = '0x7b227265636f7264223a226f776e6572222c22746f6b656e4964223a22373731373639227d'
$ownerPayloadUtf8Length = 37
$ownerPayloadHash = cast keccak $ownerPayloadUtf8Hex
$ownerRecordHash = cast keccak (cast abi-encode 'f(bytes32,uint256,address,address,uint256,uint256,bytes32,bytes32)' $ownerDomain $ownerChainId $ownerModule $ownerStreamCore 42 771769 $ownerSubject $ownerPayloadHash)
  "payloadUtf8Hex=$payloadUtf8Hex"
  "payloadUtf8Length=$payloadUtf8Length"
  "ownerPayloadUtf8Hex=$ownerPayloadUtf8Hex"
  "ownerPayloadUtf8Length=$ownerPayloadUtf8Length"
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
payloadUtf8Hex=0x7b226964223a22363532394e4d2e323032362e3030312e31222c22737461747573223a2270726f706f736564227d
payloadUtf8Length=46
ownerPayloadUtf8Hex=0x7b227265636f7264223a226f776e6572222c22746f6b656e4964223a22373731373639227d
ownerPayloadUtf8Length=37
0x0ff37eede3af67254c8d44c52b88bce8e1b191ace633f456212fd13d9cbdcca9
0xa6e5bb8be82a8267e4c7a5398a63d1b1cf8d3c612aa4529349882667e8a2ba78
0x3f29b41d9d595ee7c116a4905fd8f4faf620b5757037db8a8988cd87b9c972a7
0x648907ed3d936c0f74f8e05755c2ca9b06447e792208a269350464151c68fe36
0x8104a3a6d02c26de42514a3425567e1b75724dfda699658584c39e61153b713c
0x2a7a69c6080aa4baf28ec37f556a929a605eab80f755f25a5d8416c1fabaa0a5
0x2653d71e6881daccbff9917e23f12df8e56f7a0f8688215ca7092a5368a7d470
0x96b210df56d85918cd186e5f9a1eff34918626f25b424c2e883e72c7c54cb2d9
0x7e68037dddf1c53e8b0ac5256d02893fd85d9ffee59207f1e1eca6881588bf7c
0x8b73c3c69bb8fe3d512ecc4cf759cc79239f7b179b0ffacaa9a75d522b39400f
0xfffa62454cc94111fc3da4487def1fc9f0e36727a701015f2a46ff4a1a7c7b70
0x9db358603fafa20478b7907082a0cba6193d6d183e21cb617b78c5f3b35ddbba
0x60c2187bc87f2fe0a6f4f22d4ce61d050ae3ce7a4ce82a5607a772f356bc5cf4
0xb97f2572a6bd9f4b0075771cd3d0fb2de1c0ffa41345ac05ae4f30e6879a91ae
0xe97842aa32d8e097ebbd7f3ac132b20c38ade8bb2862f2dcda25fb3b4fe51eef
0xadf1dd94e8baaec142f9dbd1eb48a0a874d50bf369dd06d1dfd0ab0e374eae13
0x87c87440dbee8e7d2313e0be413d6222bea14055b0f324da81e0e9ef8849e4cd
0xa524091b411df027ff64e4f8d590d93cf7e2e7658f6a5a8f623abfb4e01671ef
0xe615064b79fb81a121afe1ad24d886aa86536f320be540a31023f43bbe935b64
0x47f5e941106c25d308590891c8eb0bb3c721586361b9a9bf442b49782c132183
0x3f29b41d9d595ee7c116a4905fd8f4faf620b5757037db8a8988cd87b9c972a7
0xb4e92c4245949474f8dacf09e36c2ae4a5a82ae6bd2ccc46654ce311630f8919
0x9743e8c811e3bc2760c438012d1ad61a265b385f903e02d823aa5664be5bcd7d
0x148c88658eea0b57062f88c63dba1f2aa0ffd33da6528e2a1ace1f145cf2b54a
0x8642db6f4603da6e1d6676bd54b8c64cc5c4f06521236402b75e1b84ab928e3c
0x869b5e7167f9281b7c232510e776e95500162af0fe1c031f5f7d065bf7014ee7
0xc9b32f342b0bbb44603958986a0bec0933b5a930b351002d2cf8eca9bdd3236c
```

The EIP-712 preimages are constructed by literal hex concatenation. A
command using `cast abi-encode 'f(bytes2,bytes32,bytes32)'` inserts ABI padding
for `bytes2` and is intentionally not a valid conformance command.

The EIP-712 signature bytes are intentionally absent from the record-hash
preimage; V1 uses zero/empty envelope signature fields for `bySig` writes and
keeps the relay signature in authorization metadata, as specified above.

### Independent Python Keccak/ABI check

The following second implementation uses `Crypto.Hash.keccak` and
`eth_abi.encode`; it consumes the printed payload hex as bytes and asserts the
dependent record, chain, EIP-712, owner, manifest, and batch values. It is
independent of Foundry `cast` and fails if JSON parsing or shell quoting changes
any input byte.

```powershell
@'
from Crypto.Hash import keccak
from eth_abi import encode

def k(value):
    h = keccak.new(digest_bits=256); h.update(value); return h.digest()
def hx(value): return bytes.fromhex(value[2:])
def abi(types, values): return encode(types, values)
z = bytes(32)
domain = hx('0x0c86cc4258c69b4674aa86e715d4d167bd8288b78832a0a4c5a37943b31876c4')
chain_domain = hx('0x4bc9065a5ebf49c9fff664fca90b1a40c0edac25bd076026f1b2685de7db666a')
subject_domain = hx('0x1dd722ea239e47e25bdadfcc0053bdc4e7ee75e7ca9dd0afe97076a6d9eb8a80')
asset_profile = hx('0xac72cc7c2b027b8ee3d459de7829fd7b3b31cf575c28734e736ebd33b10f41cc')
canon = hx('0x886c7c89c308c459ca8a626e0ef36a5ea9f4c7a7b56aaf86c71a2ddf3b4f9044')
record_type = hx('0x5a50f1234f1c89b5d9c2f5b2062279349feac41d8e01bf708ee9adc20a2d8ba0')
subject = bytes.fromhex('11' * 32)
schema = hx('0xe3d3da75ee91ec6a7603f809eb413342e42874cabf3992d443409657745c3cf0')
payload = bytes.fromhex('7b226964223a22363532394e4d2e323032362e3030312e31222c22737461747573223a2270726f706f736564227d')
assert len(payload) == 46
asset_hash = k(b'eip155:1/erc721:0x06012c8cf97bead5deae2370709587f8e7a266d/771769')
content_digest = k(payload)
content_ref = k(abi(['uint16','bytes32','bytes32'], [1, k(content_digest), canon]))
signature_ref = k(abi(['uint16','bytes32','bytes32'], [0, k(b''), z]))
uri_hash = k(b'ipfs://bafybeigdyrzt5example')
record_hash = k(abi(['bytes32','uint256','address','bytes32','bytes32','bytes32','bytes32','bytes32','bytes32','bytes32','uint64','uint8','bytes32'], [domain, 1, bytes.fromhex('00'*19+'01'), record_type, subject, content_ref, uri_hash, schema, z, signature_ref, 1722470400, 1, z]))
chain_hash = k(abi(['bytes32','bytes32','bytes32','uint64'], [chain_domain, z, record_hash, 1]))
domain_separator = k(abi(['bytes32','bytes32','bytes32','uint256','address'], [k(b'EIP712Domain(string name,string version,uint256 chainId,address verifyingContract)'), k(b'6529 Network Museum Registry'), k(b'1'), 1, bytes.fromhex('00'*19+'01')]))
write_type = k(b'MuseumRecordWrite(bytes32 recordHash,bytes32 recordType,bytes32 subjectId,bytes32 previousRecordHash,uint8 authorizationClass,uint64 familyRevision,uint256 nonce,uint64 deadline)')
struct_hash = k(abi(['bytes32','bytes32','bytes32','bytes32','bytes32','uint8','uint64','uint256','uint64'], [write_type, record_hash, record_type, subject, z, 12, 1, 7, 1800000000]))
digest = k(b'\x19\x01' + domain_separator + struct_hash)
nonce_type = k(b'MuseumNonceRevocation(address signer,uint256 nonce,uint64 deadline)')
nonce_struct = k(abi(['bytes32','address','uint256','uint64'], [nonce_type, bytes.fromhex('00'*18+'dead'), 7, 1800000000]))
nonce_digest = k(b'\x19\x01' + domain_separator + nonce_struct)
entry_domain = k(b'6529networkmuseum.release-manifest.entry.v1')
root_domain = k(b'6529networkmuseum.release-manifest.root.v1')
entry = k(abi(['bytes32','uint64','bytes32','bytes32','uint8','bytes32'], [entry_domain, 1, k(b'specs/onchain/contract-migration-v1.md'), record_hash, 1, content_digest]))
root = k(abi(['bytes32','bytes32','bytes32','bytes32','uint64','bytes32[]'], [root_domain, bytes.fromhex('00'*12+'ff1c5825e3b61bfb2df0a639e057297beb946e4d'), bytes.fromhex('00'*12+'5021c8060950c3fef995271e674ed4b2007fee6d'), k(b'museum-migration/1.0.0'), 1, [entry]]))
owner_payload = bytes.fromhex('7b227265636f7264223a226f776e6572222c22746f6b656e4964223a22373731373639227d')
assert len(owner_payload) == 37
owner_hash = k(abi(['bytes32','uint256','address','address','uint256','uint256','bytes32','bytes32'], [k(b'6529networkmuseum.stream-owner-record.v0'), 1, bytes.fromhex('00'*18+'2002'), bytes.fromhex('00'*18+'1001'), 42, 771769, subject, k(owner_payload)]))
batch = k(abi(['bytes32','bytes32','uint64','bytes32[]','bytes32[]','bytes32[]','uint64'], [k(b'6529networkmuseum.batch-commitment.v1'), k(b'MUSEUM_BATCH_VECTOR_V1'), 1, [record_hash], [z], [content_digest], 1]))
uri2=k(b'https://example.com/archive/6529'); host2=k(b'example.com'); profile2=hx('0x52be64fd2fb1c3795cf8dd6472100377858fd563f16de75584dcaf0f74b3e186'); a1=bytes.fromhex('0000000000000000000000000000000001010101'); a2=bytes.fromhex('0000000000000000000000000000000008080808')
address_set=abi(['address[]'],[[a1,a2]]); address_set_hash=k(address_set); https_domain=hx('0x4fcfa708a5b354629d48cb2b96432841b5566b13b7c8f30468d34106b0f7904a'); previous=z
https_hash=k(abi(['bytes32','bytes32','bytes32','bytes32','uint64','bytes32','uint64','bytes32','uint64','uint64','address','uint256','uint64'],[https_domain,uri2,host2,profile2,1,address_set_hash,1,previous,1750000000,1750003600,bytes.fromhex('00'*18+'dead'),9,1750003600]))
https_key=k(abi(['bytes32','bytes32','uint64','uint64'],[uri2,profile2,1,1]))
https_type=k(b'MuseumHTTPSPublicNetworkAssertion(bytes32 uriHash,bytes32 hostHash,bytes32 resolverProfileId,uint64 resolverRevision,bytes32 resolvedAddressSetHash,uint64 assertionRevision,bytes32 previousAssertionHash,uint64 issuedAt,uint64 expiresAt,address attestor,uint256 nonce,uint64 deadline)')
https_struct=k(abi(['bytes32','bytes32','bytes32','bytes32','uint64','bytes32','uint64','bytes32','uint64','uint64','address','uint256','uint64'],[https_type,uri2,host2,profile2,1,address_set_hash,1,previous,1750000000,1750003600,bytes.fromhex('00'*18+'dead'),9,1750003600]))
https_digest=k(b'\x19\x01'+domain_separator+https_struct)
expected = {'content':'3f29b41d9d595ee7c116a4905fd8f4faf620b5757037db8a8988cd87b9c972a7', 'record':'96b210df56d85918cd186e5f9a1eff34918626f25b424c2e883e72c7c54cb2d9', 'chain':'7e68037dddf1c53e8b0ac5256d02893fd85d9ffee59207f1e1eca6881588bf7c', 'write_type':'9db358603fafa20478b7907082a0cba6193d6d183e21cb617b78c5f3b35ddbba', 'write_struct':'60c2187bc87f2fe0a6f4f22d4ce61d050ae3ce7a4ce82a5607a772f356bc5cf4', 'write_digest':'b97f2572a6bd9f4b0075771cd3d0fb2de1c0ffa41345ac05ae4f30e6879a91ae', 'nonce_type':'e97842aa32d8e097ebbd7f3ac132b20c38ade8bb2862f2dcda25fb3b4fe51eef', 'nonce_struct':'adf1dd94e8baaec142f9dbd1eb48a0a874d50bf369dd06d1dfd0ab0e374eae13', 'nonce_digest':'87c87440dbee8e7d2313e0be413d6222bea14055b0f324da81e0e9ef8849e4cd', 'https_hash':'fd50c11dda2772e18067aab5b420f82784cec302f5327e459c894f437507b92a', 'https_key':'73b47b012ffa32766331b8ae4c360579931aea1202421bef120b851f83f177fa', 'https_type':'3bf3a1c189f1a79ba1cb192e6bb3295aa74108a14e15a1a9d48d450c22fdb02b', 'https_struct':'13c54d9975522fc40701f92c4642fb3fbfd64ced140ff9ecfdc21a3e98ad2be7', 'https_digest':'baf085c9cb66508ee83f1793c2e10319a15b005ab234bae3c23e0feac9477ecc', 'owner':'869b5e7167f9281b7c232510e776e95500162af0fe1c031f5f7d065bf7014ee7', 'owner_record':'c9b32f342b0bbb44603958986a0bec0933b5a930b351002d2cf8eca9bdd3236c', 'manifest':'9743e8c811e3bc2760c438012d1ad61a265b385f903e02d823aa5664be5bcd7d', 'batch':'ad748c99c6edc245f77ae5a46660e3c0706696e9f9c4117308a7dd773a312314'}
actual = {'content':content_digest.hex(), 'record':record_hash.hex(), 'chain':chain_hash.hex(), 'write_type':write_type.hex(), 'write_struct':struct_hash.hex(), 'write_digest':digest.hex(), 'nonce_type':nonce_type.hex(), 'nonce_struct':nonce_struct.hex(), 'nonce_digest':nonce_digest.hex(), 'https_hash':https_hash.hex(), 'https_key':https_key.hex(), 'https_type':https_type.hex(), 'https_struct':https_struct.hex(), 'https_digest':https_digest.hex(), 'owner':k(owner_payload).hex(), 'owner_record':owner_hash.hex(), 'manifest':root.hex(), 'batch':batch.hex()}
assert actual == expected, (actual, expected)
for name, value in actual.items(): print(name, '0x' + value)
'@ | python -
```

### HTTPS assertion vector transcript

The HTTPS vector was independently recomputed with the following PowerShell
commands. The address-set hash uses the ABI type `address[]`, not packed
encoding or JSON bytes:

```powershell
$uri = 'https://example.com/archive/6529'
$hostName = 'example.com'
$profile = '0x52be64fd2fb1c3795cf8dd6472100377858fd563f16de75584dcaf0f74b3e186'
$attestor = '0x000000000000000000000000000000000000dead'
$a1 = '0x0000000000000000000000000000000001010101'
$a2 = '0x0000000000000000000000000000000008080808'
$uriHash = cast keccak $uri
$hostHash = cast keccak $hostName
$addressSetEncoding = cast abi-encode 'f(address[])' "[$a1,$a2]"
$addressSetHash = cast keccak $addressSetEncoding
$assertionDomain = '0x4fcfa708a5b354629d48cb2b96432841b5566b13b7c8f30468d34106b0f7904a'
$assertionRevision = 1
$previousAssertionHash = '0x0000000000000000000000000000000000000000000000000000000000000000'
$nonce = 9
$deadline = 1750003600
$assertionHash = cast keccak (cast abi-encode 'f(bytes32,bytes32,bytes32,bytes32,uint64,bytes32,uint64,bytes32,uint64,uint64,address,uint256,uint64)' $assertionDomain $uriHash $hostHash $profile 1 $addressSetHash $assertionRevision $previousAssertionHash 1750000000 1750003600 $attestor $nonce $deadline)
$assertionKey = cast keccak (cast abi-encode 'f(bytes32,bytes32,uint64,uint64)' $uriHash $profile 1 $assertionRevision)
$subjectDomain = '0xe08003722c1e7c0465bdd4353706df75808fa767fca549cc020bd0c0081e59f4'
$assertionSubject = cast keccak (cast abi-encode 'f(bytes32,bytes32)' $subjectDomain $uriHash)
$domainSeparator = '0xfffa62454cc94111fc3da4487def1fc9f0e36727a701015f2a46ff4a1a7c7b70'
$typeHash = cast keccak 'MuseumHTTPSPublicNetworkAssertion(bytes32 uriHash,bytes32 hostHash,bytes32 resolverProfileId,uint64 resolverRevision,bytes32 resolvedAddressSetHash,uint64 assertionRevision,bytes32 previousAssertionHash,uint64 issuedAt,uint64 expiresAt,address attestor,uint256 nonce,uint64 deadline)'
$structHash = cast keccak (cast abi-encode 'f(bytes32,bytes32,bytes32,bytes32,uint64,bytes32,uint64,bytes32,uint64,uint64,address,uint256,uint64)' $typeHash $uriHash $hostHash $profile 1 $addressSetHash $assertionRevision $previousAssertionHash 1750000000 1750003600 $attestor $nonce $deadline)
$digest = cast keccak ('0x1901'+$domainSeparator.Substring(2)+$structHash.Substring(2))
$uriHash
$hostHash
$addressSetEncoding
$addressSetHash
$assertionHash
$assertionKey
$assertionSubject
$typeHash
$structHash
$digest
```

Expected output:

```text
0x000c84d539237dee07b2286ba2f354c5f808a9e49e2001c1e7ed9279e11cb704
0x02438d3405cadd648e08dbff51bdbeb415913e642189100dc4a012064c870883
0x0000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000000200000000000000000000000000000000000000000000000000000000010101010000000000000000000000000000000000000000000000000000000008080808
0x17971e83b91ac972b51bdefb4cab3445a46319fc90d6bc5894819de59fbf03a9
0xfd50c11dda2772e18067aab5b420f82784cec302f5327e459c894f437507b92a
0x73b47b012ffa32766331b8ae4c360579931aea1202421bef120b851f83f177fa
0x6528698388e83a3af89e9af7095da74d003172bf2979ea74d7e27f9fc22a745c
0x3bf3a1c189f1a79ba1cb192e6bb3295aa74108a14e15a1a9d48d450c22fdb02b
0x13c54d9975522fc40701f92c4642fb3fbfd64ced140ff9ecfdc21a3e98ad2be7
0xbaf085c9cb66508ee83f1793c2e10319a15b005ab234bae3c23e0feac9477ecc
```

### Batch commitment transcript

```powershell
$batchDomain = cast keccak '6529networkmuseum.batch-commitment.v1'
$batchId = cast keccak 'MUSEUM_BATCH_VECTOR_V1'
$recordHash = '0x96b210df56d85918cd186e5f9a1eff34918626f25b424c2e883e72c7c54cb2d9'
$zero = '0x0000000000000000000000000000000000000000000000000000000000000000'
$payloadHash = '0x3f29b41d9d595ee7c116a4905fd8f4faf620b5757037db8a8988cd87b9c972a7'
$batchCommitment = cast keccak (cast abi-encode 'f(bytes32,bytes32,uint64,bytes32[],bytes32[],bytes32[],uint64)' $batchDomain $batchId 1 "[$recordHash]" "[$zero]" "[$payloadHash]" 1)
$batchDomain
$batchId
$batchCommitment
```

Expected output:

```text
0x6743de485825345432a60824968ffa9c8b3ef54adb2f4ad2d1cb219ec56e4400
0xa4713265f6f293e83885203722026053a888831af3f829e81b6aaed0d5d1d70b
0xad748c99c6edc245f77ae5a46660e3c0706696e9f9c4117308a7dd773a312314
```

## Negative claims preserved

This review does not claim that any Casey work is accessioned, that any Keys
and Gates winner is minted or in Museum custody, that a wallet transfer proves
title, or that a vote total proves governance adoption. Those facts remain
subject to the repository's evidence and accession rules.
