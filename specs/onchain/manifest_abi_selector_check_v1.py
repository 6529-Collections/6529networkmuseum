"""Offline V1 manifest-vector and canonical ABI/authorization checker.

This checker is a conformance fixture for the design specification only.  It
does not contact a chain, publish a release, or authorize any deployment.
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

from Crypto.Hash import keccak

from abi_encoding_v1 import address_word, bytes32_arrays, static_words, uint_word


if not __debug__:
    raise SystemExit("optimized Python disables conformance checks")


ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parents[1]
SPEC_PATH = ROOT / "contract-migration-v1.md"
RESEARCH_PATH = ROOT.parents[1] / "notes" / "research" / "external-registry-review.md"


def k(value: bytes) -> bytes:
    digest = keccak.new(digest_bits=256)
    digest.update(value)
    return digest.digest()


def hx(value: str) -> bytes:
    return bytes.fromhex(value.removeprefix("0x"))


def selector(signature: str) -> str:
    return "0x" + k(signature.encode("ascii"))[:4].hex()


def hash_ref(algorithm: int, digest: bytes, canonicalization_id: bytes) -> bytes:
    return k(static_words(uint_word(algorithm), k(digest), canonicalization_id))


# This is the complete published golden selector transcript for the exact §7
# IMuseumRegistryV1 ABI.  Tuple forms are canonical Solidity ABI forms, not
# display aliases using struct names.
ABI_SELECTORS = (
    ("isNetworkMuseumRegistry()", "0xedc7801f"),
    ("registryVersion()", "0x0f9be51c"),
    ("protocolVersion()", "0x2ae9c600"),
    ("streamCompatibilityCommit()", "0xc8e1a0da"),
    ("moduleSupersedes()", "0x57699215"),
    ("authority()", "0xbf7e214f"),
    ("authorityRevision()", "0x48de7dbc"),
    ("authorityState()", "0xa865a4c7"),
    ("governanceExecutor()", "0x8fc98386"),
    ("governanceExecutorRevision()", "0x533620f9"),
    ("governanceExecutorBinding()", "0x5bcde725"),
    ("pendingGovernanceExecutor()", "0x737aa558"),
    ("releaseAttestorPolicyHash()", "0x274ac640"),
    ("releaseAttestorSignerSetHash()", "0xd66c61c0"),
    ("releaseAttestorSigner(uint256)", "0xbb295d02"),
    ("successor()", "0x6ff968c3"),
    ("writesFrozen()", "0x290d086b"),
    ("pendingAuthority()", "0xfabb94bb"),
    ("successorTarget()", "0xae540c6b"),
    ("externalAssetSubjectId(bytes32,string)", "0x0b88b5e8"),
    ("registerExternalAsset(bytes32,string,bytes32)", "0x73c0a0b4"),
    ("externalAsset(bytes32)", "0xdb08b0b0"),
    ("admitAssetProfile(bytes32,bytes32,bytes32,string,address,uint8,bytes32,bytes32,bytes32,string)", "0xea2792ce"),
    ("assetProfile(bytes32)", "0x2938cf75"),
    ("admitSchema(bytes32,bytes32,string,bool)", "0x541fd287"),
    ("schema(bytes32)", "0x072b9cf2"),
    ("admitRecordFamily(bytes32,uint8,uint16)", "0x63d20b1a"),
    ("recordFamily(bytes32)", "0x1ca9f8aa"),
    ("admitRecordType(bytes32,bytes32,bytes32,uint8)", "0x46a9f249"),
    ("recordTypePolicy(bytes32)", "0xcd2369a6"),
    ("setRecordFamilyGrant(bytes32,uint8,address,bool)", "0x40ee7ee3"),
    ("recordFamilyGrant(bytes32,uint8,address)", "0x1118ed2f"),
    ("admitTargetRelease(uint8,address,bytes32,bytes32,bytes32,bytes32,bytes32,(address,bytes32,bytes32,bytes4,bytes32)[],bytes32,bytes32,bytes32,bytes32,bytes32,address[],bytes[],bytes4,bytes32,bytes32,bytes32,bytes32,bytes32)", "0x93936f62"),
    ("targetRelease(uint8,address,bytes32)", "0x85968ef0"),
    ("targetReleaseAtRevision(uint8,address,bytes32,uint64)", "0x288b2e93"),
    ("targetReleaseById(bytes32)", "0xb9bc97a1"),
    ("targetReleaseDependencyCount(bytes32)", "0x1dcd55b2"),
    ("targetReleaseDependency(bytes32,uint256)", "0x1efe53c1"),
    ("quarantineTargetRelease(uint8,address,bytes32,bytes32)", "0xda6d916f"),
    ("setAuthority((address,bytes32,bytes4,bytes32,bytes32,address,bytes32,bytes32))", "0x81a86ff4"),
    ("executeAuthority()", "0xc9dc7d0d"),
    ("cancelAuthority()", "0xf0edf065"),
    ("setGovernanceExecutor(address,bytes32,bytes32)", "0x3a1a0b96"),
    ("executeGovernanceExecutor()", "0x967059b8"),
    ("cancelGovernanceExecutor()", "0x51d8c5e0"),
    ("setGlobalRoleGrant(bytes32,address,bool)", "0xab6627c3"),
    ("globalRoleGrant(bytes32,address)", "0x59d2fe4a"),
    ("admitHttpsResolverProfile(bytes32,bytes32,address,uint64,uint64)", "0xaf2fb948"),
    ("resolverProfile(bytes32)", "0x3711d316"),
    ("recordHttpsAssertionBySig(string,bytes32,bytes32,uint64,bytes32,uint64,bytes32,uint64,uint64,address,uint256,uint64,address[],bytes)", "0x1e0c9fe6"),
    ("httpsAssertion(bytes32,bytes32,uint64,uint64)", "0x1120d46d"),
    ("currentHttpsAssertion(bytes32)", "0x080dab7b"),
    ("httpsAssertionByHash(bytes32)", "0x28208c17"),
    ("admitStreamOwnerRecordInterface(address,bytes32,address,bytes32,bytes32,bytes32,bytes32)", "0x51b648fd"),
    ("streamOwnerRecordInterface()", "0xfbab3335"),
    ("streamOwnerRecordInterfaceAtRevision(uint64)", "0x7940fbb2"),
    ("recordMuseumRecord((bytes32,bytes32,(uint16,bytes,bytes32),string,bytes32,bytes32,(uint16,bytes,bytes32),uint64),bytes32,uint8,bytes32)", "0x29f319b0"),
    ("recordMuseumRecordWithPayload((bytes32,bytes32,(uint16,bytes,bytes32),string,bytes32,bytes32,(uint16,bytes,bytes32),uint64),bytes32,uint8,bytes32,bytes)", "0x82447563"),
    ("recordMuseumRecordBySig((bytes32,bytes32,(uint16,bytes,bytes32),string,bytes32,bytes32,(uint16,bytes,bytes32),uint64),bytes32,bytes32,bytes32,address,uint8,uint64,uint256,uint64,bytes,uint8,bytes32,bytes)", "0x20f3cc85"),
    ("recordMuseumRecordBatch(((bytes32,bytes32,(uint16,bytes,bytes32),string,bytes32,bytes32,(uint16,bytes,bytes32),uint64),bytes32,uint8,bytes32,bytes)[],bytes32)", "0xb12754c9"),
    ("batchIdUsed(bytes32)", "0xd4b4d9f4"),
    ("batchCommitment(bytes32)", "0x70ad2bd4"),
    ("deriveMuseumRecordHash((bytes32,bytes32,(uint16,bytes,bytes32),string,bytes32,bytes32,(uint16,bytes,bytes32),uint64),uint8,bytes32)", "0x4bc9025c"),
    ("latestRecordHash(bytes32,bytes32)", "0xaec646e8"),
    ("recordChainHead(bytes32,bytes32)", "0xb9f4933e"),
    ("recordSummary(bytes32)", "0x45fafe2f"),
    ("record(bytes32)", "0xb5c645bd"),
    ("payload(bytes32)", "0x9f165a87"),
    ("setStreamMirrorLink(bytes32,uint256,bytes32)", "0xc1713cf2"),
    ("streamMirrorLink(bytes32)", "0xfc584dc4"),
    ("revokeNonce(uint256)", "0x05c1ee20"),
    ("revokeNonces(uint256[])", "0xac7410a1"),
    ("revokeNonceBySig(address,uint256,uint64,bytes)", "0xc75a6797"),
    ("nonceRevocation(address,uint256)", "0x51b366d4"),
    ("setSuccessor((address,bytes32,bytes4,bytes32,bytes32,address,bytes32,bytes32))", "0x43dd6c37"),
    ("freezeWrites()", "0x05d53fba"),
)

INTERFACE_ONLY_SELECTORS = (
    ("supportsInterface(bytes4)", "0x01ffc9a7"),
    ("isMuseumAuthorityProvider()", "0x28a26c9f"),
    ("registry()", "0x7b103999"),
    ("capabilityHandshake(address,bytes32,bytes32,bytes32)", "0xf1292022"),
    ("streamCore()", "0x5f59b4d2"),
    ("ownerRecordBinding(uint256)", "0x814e950a"),
    ("ownerRecordHashDomain()", "0xe79efeda"),
    ("ownerRecordHashVectorId()", "0xfda2f68a"),
    ("tokenCollectionIdentity(uint256)", "0xa6b638c9"),
    ("tokenLifecycle(uint256)", "0x8c46d901"),
)

# Stream publishes these owner-record selectors as a design-level ABI at the
# pinned commit. They are not part of IMuseumRegistryV1 and their presence here
# does not assert that a source-backed or deployed StreamOwnerRecords module
# exists.
STREAM_DRAFT_OWNER_SELECTORS = (
    ("recordOwnerRecord(uint256,(bytes32,bytes32,bytes32,(uint16,bytes,bytes32),string,bytes,uint64))", "0x198c95e3"),
    ("recordOwnerRecordFor(uint256,(bytes32,bytes32,bytes32,(uint16,bytes,bytes32),string,bytes,uint64),address,uint256,uint64,bytes)", "0xf24bb020"),
    ("isOwnerRecordNonceUsed(address,uint256)", "0x18544c94"),
    ("revokeOwnerRecordNonce(uint256)", "0x9d03970a"),
    ("revokeOwnerRecordNonceFor(address,uint256,uint64,bytes)", "0x50e9829a"),
    ("recordChainHash(uint256,bytes32)", "0x9d99a291"),
    ("payloadPointerCount(uint256)", "0x9a36f48e"),
    ("payloadPointerAt(uint256,uint256)", "0x6c86be87"),
)

GLOBAL_ROLE_IDS = (
    ("MUSEUM_GLOBAL_ROLE_GOVERNANCE_EXECUTOR_V1", "0x865cb1cc1a43094ea97b42f5b9e950e7952c1f106d37051e97d2a3fdb1584ce2"),
    ("MUSEUM_GLOBAL_ROLE_REGISTRAR_V1", "0xb1f5e657823d31bde6c263be60f0418d7361b8365b264c97798c0b790c1a5f8b"),
    ("MUSEUM_GLOBAL_ROLE_MIGRATION_ADMIN_V1", "0x2729f1662f9bb2682a0a433e8329cd1b73680e122f49b4b4987cef1106b97004"),
    ("MUSEUM_GLOBAL_ROLE_AUTHORITY_ADMIN_V1", "0x28ad41c29b6a0872dec6410316cebb3f72fc3c9e4f4ea88e8e87e81784c94426"),
    ("MUSEUM_GLOBAL_ROLE_HTTPS_ATTESTOR_V1", "0x47df6320f751abd29d6ce09022685a520d0128d5f284c7573d3b6857127abc61"),
)

AUTHORITY_SELECTOR_ALLOWLIST = (
    "0x3a1a0b96", "0x51b648fd", "0x51d8c5e0", "0x81a86ff4", "0x93936f62",
    "0x967059b8", "0xab6627c3", "0xaf2fb948", "0xc1713cf2",
    "0xc9dc7d0d", "0xda6d916f", "0xf0edf065",
)
EXPECTED_ALLOWLIST_HASH = "0x4c2a05297ef36555d0bd199b80df1463d02702f6bd1bde9444960279d15957e5"
EMPTY_PAYLOAD_LITERAL = b"MUSEUM_EMPTY_PAYLOAD_V1"
EMPTY_PAYLOAD_CANONICALIZATION_ID = "0xa441d30896b70045ccf31ccc5b89cefd312a64c9c2102fa1c6898140d443ef4f"
EMPTY_PAYLOAD_DIGEST = "0xc5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470"
EMPTY_PAYLOAD_DIGEST_HASH = "0x10ca3eff73ebec87d2394fc58560afeab86dac7a21f5e402ea0a55e5c8a6758f"
EMPTY_PAYLOAD_HASH_REF_HASH = "0x5d7e6369b77349763919edf197e8a1ba931bbfd63a9e40b5af00ca630a4346c7"
CANONICALIZER_LIMITS_ID = "0xf66c08f21c02834b2dd294a0556fb5adb7c17b447338ee0ad5ecc1a2198509d3"
CANONICALIZER_CALL_GAS_LIMIT = 100_000
MAX_CANONICALIZER_RETURN_DATA_BYTES = 4_096
MAX_CANONICAL_ASSET_ID_BYTES = 2_048

STABLE_RECORD_TYPE_ALLOWLIST = (
    ("MUSEUM_EXTERNAL_ASSET_IDENTITY", "0xe1c1798f46d210552c5d3924b7059a57b07eedf054640a662eb47bac008b4a8e", "MUSEUM_EXTERNAL_ASSET_IDENTITY_V1", "0x34e9649723069df3772c810e6e825f7589c211bac81acc9b908a60067f936aa6", "AUTH_MUSEUM_REGISTRAR", 10),
    ("MUSEUM_CUSTODY_OBSERVATION", "0x8351820e5600a2472b0dd68eb83a0480b8663df2efcab7d34321b1df5918316e", "MUSEUM_CUSTODY_OBSERVATION_V1", "0xb0c467baa7db6862385e58253c1c4702d95b141a1ef66cd2b86234a597344014", "AUTH_MUSEUM_PROGRAM_AUTHORITY", 11),
    ("MUSEUM_ACCESSION_LOT", "0xc544e9b2b8226296197005f65dd84855588d18be5e1ce13082b8314004cb4661", "MUSEUM_ACCESSION_LOT_V1", "0x8bb4cfecf4d3736765bc80624dd0a876d2e1c17bf5a406066d5f2256fc739d44", "AUTH_MUSEUM_PROGRAM_AUTHORITY", 11),
    ("MUSEUM_PROGRAM_OUTCOME", "0xe81870465556c524f1375c1a3cff4aa920e8f0c15b9858ae6bb55c6c3cb0ad5a", "MUSEUM_PROGRAM_OUTCOME_V1", "0x7a25e6a6a5e91d55ef0ea9115ad5902929bcf0d3331b4bb2d22100f65fc78470", "AUTH_MUSEUM_PROGRAM_AUTHORITY", 11),
    ("MUSEUM_RESEARCH_NOTE", "0x5a50f1234f1c89b5d9c2f5b2062279349feac41d8e01bf708ee9adc20a2d8ba0", "MUSEUM_RESEARCH_NOTE_V1", "0xe3d3da75ee91ec6a7603f809eb413342e42874cabf3992d443409657745c3cf0", "AUTH_MUSEUM_PROGRAM_AUTHORITY", 11),
    ("MUSEUM_RELEASE_MANIFEST", "0x8889bb0d1446ec07b517aca915af9a4ad6d993ef8af5b999301ca8b15f789084", "MUSEUM_RELEASE_MANIFEST_V1", "0x7a41091035def3c5fa62722d73a7ea87f996fe9be34e9115317c5d128581d299", "AUTH_MUSEUM_MIGRATION_ADMIN", 12),
)


def check_none_content_hash_vector() -> dict[str, str]:
    canonicalization_id = k(EMPTY_PAYLOAD_LITERAL)
    digest = k(b"")
    assert "0x" + canonicalization_id.hex() == EMPTY_PAYLOAD_CANONICALIZATION_ID
    assert "0x" + digest.hex() == EMPTY_PAYLOAD_DIGEST
    assert "0x" + k(digest).hex() == EMPTY_PAYLOAD_DIGEST_HASH
    assert "0x" + hash_ref(1, digest, canonicalization_id).hex() == EMPTY_PAYLOAD_HASH_REF_HASH

    def valid_none(
        path: str, *, mode: int = 0, payload: bytes = b"", uri: bytes = b"",
        algorithm: int = 1, content_digest: bytes = digest,
        canonicalization: bytes = canonicalization_id,
    ) -> bool:
        assert path in {"direct", "relayed", "batch"}
        return (
            mode == 0 and payload == b"" and uri == b"" and algorithm == 1
            and content_digest == digest and canonicalization == canonicalization_id
        )

    mutations = (
        {"algorithm": 0, "content_digest": b"", "canonicalization": bytes(32)},
        {"content_digest": b""},
        {"canonicalization": hx("0x886c7c89c308c459ca8a626e0ef36a5ea9f4c7a7b56aaf86c71a2ddf3b4f9044")},
        {"algorithm": 2},
        {"content_digest": k(b"not empty")},
        {"uri": b"ipfs://bafkreiaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"},
    )
    for path in ("direct", "relayed", "batch"):
        assert valid_none(path)
        assert all(not valid_none(path, **mutation) for mutation in mutations)

    return {
        "emptyPayloadCanonicalizationId": EMPTY_PAYLOAD_CANONICALIZATION_ID,
        "contentHash.digest": EMPTY_PAYLOAD_DIGEST,
        "keccak256(contentHash.digest)": EMPTY_PAYLOAD_DIGEST_HASH,
        "contentHash.canonicalizationId": EMPTY_PAYLOAD_CANONICALIZATION_ID,
        "hashRefHash(contentHash)": EMPTY_PAYLOAD_HASH_REF_HASH,
    }


def canonicalizer_call_accepts(
    supplied: bytes,
    *,
    call_succeeded: bool = True,
    gas_used: int = CANONICALIZER_CALL_GAS_LIMIT,
    return_data_size: int | None = None,
    abi_well_formed: bool = True,
    returned: bytes | None = None,
) -> bool:
    returned = supplied if returned is None else returned
    if return_data_size is None:
        return_data_size = 64 + ((len(returned) + 31) // 32) * 32
    return (
        0 < len(supplied) <= MAX_CANONICAL_ASSET_ID_BYTES
        and call_succeeded
        and 0 <= gas_used <= CANONICALIZER_CALL_GAS_LIMIT
        and 0 <= return_data_size <= MAX_CANONICALIZER_RETURN_DATA_BYTES
        and abi_well_formed
        and returned == supplied
    )


def check_canonicalizer_execution_limits() -> dict[str, str]:
    assert "0x" + k(b"MUSEUM_CANONICALIZER_EXECUTION_LIMITS_V1").hex() == CANONICALIZER_LIMITS_ID
    boundary = b"a" * MAX_CANONICAL_ASSET_ID_BYTES
    assert canonicalizer_call_accepts(boundary)
    assert not canonicalizer_call_accepts(b"")
    assert not canonicalizer_call_accepts(boundary + b"a")
    assert not canonicalizer_call_accepts(b"asset", call_succeeded=False)
    assert not canonicalizer_call_accepts(b"asset", gas_used=CANONICALIZER_CALL_GAS_LIMIT + 1)
    assert not canonicalizer_call_accepts(
        b"asset", return_data_size=MAX_CANONICALIZER_RETURN_DATA_BYTES + 1
    )
    assert not canonicalizer_call_accepts(b"asset", abi_well_formed=False)
    assert not canonicalizer_call_accepts(b"asset", returned=b"different")
    return {
        "limitsId": CANONICALIZER_LIMITS_ID,
        "callGasLimit": str(CANONICALIZER_CALL_GAS_LIMIT),
        "maxReturnDataBytes": str(MAX_CANONICALIZER_RETURN_DATA_BYTES),
        "maxCanonicalAssetIdBytes": str(MAX_CANONICAL_ASSET_ID_BYTES),
        "boundaryFixedPoint": "ACCEPT",
        "overGas": "REJECT",
        "overReturnData": "REJECT",
        "oversizedInput": "REJECT",
        "malformedAbi": "REJECT",
        "outputMismatch": "REJECT",
    }


def check_manifest_vector() -> bytes:
    zero = bytes(32)
    payload = b'{"id":"6529NM.2026.001.1","status":"proposed"}'
    payload_hash = k(payload)
    content_ref = hash_ref(1, payload_hash, hx("0x886c7c89c308c459ca8a626e0ef36a5ea9f4c7a7b56aaf86c71a2ddf3b4f9044"))
    signature_ref = hash_ref(0, b"", zero)
    record_hash = k(static_words(
        hx("0x0c86cc4258c69b4674aa86e715d4d167bd8288b78832a0a4c5a37943b31876c4"),
        uint_word(1), address_word(hx("0x0000000000000000000000000000000000000001")),
        hx("0x5a50f1234f1c89b5d9c2f5b2062279349feac41d8e01bf708ee9adc20a2d8ba0"),
        hx("0x1111111111111111111111111111111111111111111111111111111111111111"),
        content_ref, k(b"ipfs://bafybeiexd37whdwmbipbf7acxcrll2pg6lwcz6ks7atxc6z4niszkoragq"),
        hx("0xe3d3da75ee91ec6a7603f809eb413342e42874cabf3992d443409657745c3cf0"),
        zero, signature_ref, uint_word(1_722_470_400), uint_word(1), zero,
    ))
    assert record_hash.hex() == "217e7a966879dd7c379772be42f35fe353b45c113cec0ac76c21dd068bd506d1"
    entry_hash = k(static_words(
        k(b"6529networkmuseum.release-manifest.entry.v1"), uint_word(1),
        k(b"specs/onchain/contract-migration-v1.md"), record_hash, uint_word(1), payload_hash,
    ))
    assert entry_hash.hex() == "fa531a4233206547049d1b83c4b4e3e4d9763effb47227b2fd761ea1846ddfc8"
    source_commit = hx("0x000000000000000000000000ff1c5825e3b61bfb2df0a639e057297beb946e4d")
    root = k(bytes32_arrays(
        [k(b"6529networkmuseum.release-manifest.root.v1"), source_commit,
         hx("0x0000000000000000000000005021c8060950c3fef995271e674ed4b2007fee6d"),
         k(b"museum-migration/1.0.0"), uint_word(1)],
        [[entry_hash]], [],
    ))
    assert root.hex() == "8bb17fc4361cbfe29c586218e716d0c4789973b222ee7a403f9d22f6f483a280"
    return root


def check_general_vectors() -> dict[str, dict[str, str]]:
    zero = bytes(32)
    registry = hx("0x0000000000000000000000000000000000000001")
    record_type = hx("0x5a50f1234f1c89b5d9c2f5b2062279349feac41d8e01bf708ee9adc20a2d8ba0")
    subject = hx("0x1111111111111111111111111111111111111111111111111111111111111111")
    schema = hx("0xe3d3da75ee91ec6a7603f809eb413342e42874cabf3992d443409657745c3cf0")
    payload = b'{"id":"6529NM.2026.001.1","status":"proposed"}'
    payload_hash = k(payload)
    uri_hash = k(b"ipfs://bafybeiexd37whdwmbipbf7acxcrll2pg6lwcz6ks7atxc6z4niszkoragq")
    canonicalization = hx("0x886c7c89c308c459ca8a626e0ef36a5ea9f4c7a7b56aaf86c71a2ddf3b4f9044")
    content_ref = hash_ref(1, payload_hash, canonicalization)
    signature_ref = hash_ref(0, b"", zero)
    record_hash = k(static_words(
        hx("0x0c86cc4258c69b4674aa86e715d4d167bd8288b78832a0a4c5a37943b31876c4"),
        uint_word(1), address_word(registry), record_type, subject, content_ref,
        uri_hash, schema, zero, signature_ref, uint_word(1_722_470_400),
        uint_word(1), zero,
    ))
    chain_hash = k(static_words(
        hx("0x4bc9065a5ebf49c9fff664fca90b1a40c0edac25bd076026f1b2685de7db666a"),
        zero, record_hash, uint_word(1),
    ))
    asset = b"eip155:1/erc721:0x06012c8cf97bead5deae2370709587f8e7a266d/771769"
    asset_profile = hx("0xac72cc7c2b027b8ee3d459de7829fd7b3b31cf575c28734e736ebd33b10f41cc")
    external_subject = k(static_words(
        hx("0x1dd722ea239e47e25bdadfcc0053bdc4e7ee75e7ca9dd0afe97076a6d9eb8a80"),
        asset_profile, k(asset),
    ))

    domain_type = k(b"EIP712Domain(string name,string version,uint256 chainId,address verifyingContract)")
    domain_separator = k(static_words(
        domain_type, k(b"6529 Network Museum Registry"), k(b"1"),
        uint_word(1), address_word(registry),
    ))
    record_write_type = k(b"MuseumRecordWrite(bytes32 recordHash,bytes32 recordType,bytes32 subjectId,bytes32 previousRecordHash,uint8 authorizationClass,uint64 familyRevision,uint256 nonce,uint64 deadline)")
    record_write_struct = k(static_words(
        record_write_type, record_hash, record_type, subject, zero,
        uint_word(12), uint_word(1), uint_word(7), uint_word(1_800_000_000),
    ))
    record_write_digest = k(b"\x19\x01" + domain_separator + record_write_struct)
    revoke_type = k(b"MuseumNonceRevocation(address signer,uint256 nonce,uint64 deadline)")
    revoke_struct = k(static_words(
        revoke_type, address_word(hx("0x000000000000000000000000000000000000dead")),
        uint_word(7), uint_word(1_800_000_000),
    ))
    revoke_digest = k(b"\x19\x01" + domain_separator + revoke_struct)

    owner_payload = b'{"record":"owner","tokenId":"771769"}'
    owner_content_digest = k(owner_payload)
    owner_uri = b"ipfs://bafybeiexd37whdwmbipbf7acxcrll2pg6lwcz6ks7atxc6z4niszkoragq"
    owner = hx("0x000000000000000000000000000000000000dead")
    owner_module = hx("0x0000000000000000000000000000000000002002")
    owner_stream_core = hx("0x0000000000000000000000000000000000001001")
    owner_subject_domain = hx("0x1e576f27850d12bc1ec9255ca277dbecfbc84fb3a9a34c474640dfca89811d7e")
    owner_subject = k(static_words(
        owner_subject_domain, uint_word(1), address_word(owner_stream_core),
        uint_word(771_769),
    ))
    owner_type_string = b"StreamOwnerRecord(address owner,uint256 tokenId,bytes32 subjectId,bytes32 recordType,bytes32 schemaId,uint16 algorithmId,bytes digest,bytes32 canonicalizationId,string uri,bytes payload,uint64 effectiveAt,uint256 nonce,uint64 deadline)"
    owner_type_hash = k(owner_type_string)
    owner_revocation_type_hash = k(b"StreamOwnerRecordRevocation(address owner,uint256 nonce,uint64 deadline)")
    owner_domain_separator = k(static_words(
        domain_type, k(b"6529StreamOwnerRecords"), k(b"1"), uint_word(1),
        address_word(owner_module),
    ))
    owner_struct_hash = k(static_words(
        owner_type_hash, address_word(owner), uint_word(771_769), owner_subject,
        hx("0x4dc3a5e33f97bcd06f2d025349086438272d94a398185aca416ae539e36521fb"),
        hx("0xc04bb48f95c8db4fe7f26a20106533f987003843f2fed36fd6d89f207ddfbd86"),
        uint_word(1), k(owner_content_digest), canonicalization, k(owner_uri),
        k(owner_payload), uint_word(1_722_470_400), uint_word(7),
        uint_word(1_800_000_000),
    ))
    owner_digest = k(b"\x19\x01" + owner_domain_separator + owner_struct_hash)

    uri = b"https://example.com/archive/6529"
    uri_hash_https = k(uri)
    host_hash = k(b"example.com")
    profile = hx("0x52be64fd2fb1c3795cf8dd6472100377858fd563f16de75584dcaf0f74b3e186")
    addresses = (
        hx("0x0000000000000000000000000000000001010101"),
        hx("0x0000000000000000000000000000000008080808"),
    )
    address_array_abi = uint_word(32) + uint_word(2) + b"".join(address_word(value) for value in addresses)
    address_set_hash = k(address_array_abi)
    attestor = hx("0x000000000000000000000000000000000000dead")
    assertion_hash = k(static_words(
        hx("0x4fcfa708a5b354629d48cb2b96432841b5566b13b7c8f30468d34106b0f7904a"),
        uri_hash_https, host_hash, profile, uint_word(1), address_set_hash,
        uint_word(1), zero, uint_word(1_750_000_000), uint_word(1_750_003_600),
        address_word(attestor), uint_word(9), uint_word(1_750_003_600),
    ))
    assertion_key = k(static_words(uri_hash_https, profile, uint_word(1), uint_word(1)))
    assertion_subject = k(static_words(
        hx("0xe08003722c1e7c0465bdd4353706df75808fa767fca549cc020bd0c0081e59f4"),
        uri_hash_https,
    ))
    assertion_type = k(b"MuseumHTTPSPublicNetworkAssertion(bytes32 uriHash,bytes32 hostHash,bytes32 resolverProfileId,uint64 resolverRevision,bytes32 resolvedAddressSetHash,uint64 assertionRevision,bytes32 previousAssertionHash,uint64 issuedAt,uint64 expiresAt,address attestor,uint256 nonce,uint64 deadline)")
    assertion_struct = k(static_words(
        assertion_type, uri_hash_https, host_hash, profile, uint_word(1),
        address_set_hash, uint_word(1), zero, uint_word(1_750_000_000),
        uint_word(1_750_003_600), address_word(attestor), uint_word(9),
        uint_word(1_750_003_600),
    ))
    assertion_digest = k(b"\x19\x01" + domain_separator + assertion_struct)
    renewed_assertion_hash = k(static_words(
        hx("0x4fcfa708a5b354629d48cb2b96432841b5566b13b7c8f30468d34106b0f7904a"),
        uri_hash_https, host_hash, profile, uint_word(1), address_set_hash,
        uint_word(2), assertion_hash, uint_word(1_750_003_601),
        uint_word(1_750_007_200), address_word(attestor), uint_word(10),
        uint_word(1_750_007_200),
    ))

    batch_id = k(b"MUSEUM_BATCH_VECTOR_V1")
    batch_commitment = k(bytes32_arrays(
        [hx("0x6743de485825345432a60824968ffa9c8b3ef54adb2f4ad2d1cb219ec56e4400"), batch_id, uint_word(1)],
        [[record_hash], [zero], [payload_hash]], [uint_word(1)],
    ))

    successor_domain = k(b"6529networkmuseum.successor-capability.v1")
    probe_domain = k(b"6529networkmuseum.target-probe.v1")
    release = k(b"MUSEUM_SUCCESSOR_RELEASE_VECTOR_V1")
    target = hx("0x0000000000000000000000000000000000000042")
    predecessor = hx("0x000000000000000000000000000000000000cafe")
    code_hash = k(b"MUSEUM_SUCCESSOR_CODEHASH_VECTOR_V1")
    conformance = k(b"MUSEUM_SUCCESSOR_CONFORMANCE_VECTOR_V1")
    module_version = k(b"MUSEUM_REGISTRY_VERSION_V2_VECTOR")
    protocol = hx("0xea7ed1159fede00c63bf928f3b977361b7471b9bd72bb677289a42b8eec98713")
    stream = hx("0x0000000000000000000000005021c8060950c3fef995271e674ed4b2007fee6d")
    interface_word = hx("0x573d91cc") + bytes(28)
    capability = k(static_words(
        successor_domain, release, address_word(target), code_hash, interface_word,
        address_word(predecessor), module_version, protocol, stream,
        address_word(predecessor), conformance,
    ))
    probe = k(static_words(
        probe_domain, release, address_word(target), code_hash, interface_word,
        uint_word(1), address_word(predecessor), module_version, protocol,
        stream, address_word(predecessor), capability,
    ))

    vectors = {
        "13.1": {
            "keccak256(bytes(canonicalAssetId))": "0x" + k(asset).hex(),
            "subjectId": "0x" + external_subject.hex(),
        },
        "13.2": {
            "contentDigest": "0x" + payload_hash.hex(),
            "keccak256(contentHash.digest)": "0x" + k(payload_hash).hex(),
            "uriHash": "0x" + uri_hash.hex(),
            "hashRefHash(contentHash)": "0x" + content_ref.hex(),
            "hashRefHash(signatureHash)": "0x" + signature_ref.hex(),
            "recordHash": "0x" + record_hash.hex(),
            "chainHash": "0x" + chain_hash.hex(),
        },
        "13.2.1": check_none_content_hash_vector(),
        "13.3": {
            "domainSeparator": "0x" + domain_separator.hex(),
            "MuseumRecordWrite typeHash": "0x" + record_write_type.hex(),
            "structHash": "0x" + record_write_struct.hex(),
            "digest": "0x" + record_write_digest.hex(),
        },
        "13.4": {
            "domainSeparator": "0x" + domain_separator.hex(),
            "MuseumNonceRevocation typeHash": "0x" + revoke_type.hex(),
            "structHash": "0x" + revoke_struct.hex(),
            "digest": "0x" + revoke_digest.hex(),
        },
        "13.5": {
            "recordOwnerRecord selector": selector("recordOwnerRecord(uint256,(bytes32,bytes32,bytes32,(uint16,bytes,bytes32),string,bytes,uint64))"),
            "recordOwnerRecordFor selector": selector("recordOwnerRecordFor(uint256,(bytes32,bytes32,bytes32,(uint16,bytes,bytes32),string,bytes,uint64),address,uint256,uint64,bytes)"),
            "isOwnerRecordNonceUsed selector": selector("isOwnerRecordNonceUsed(address,uint256)"),
            "revokeOwnerRecordNonce selector": selector("revokeOwnerRecordNonce(uint256)"),
            "revokeOwnerRecordNonceFor selector": selector("revokeOwnerRecordNonceFor(address,uint256,uint64,bytes)"),
            "STREAM_OWNER_RECORD_TYPEHASH": "0x" + owner_type_hash.hex(),
            "STREAM_OWNER_RECORD_REVOCATION_TYPEHASH": "0x" + owner_revocation_type_hash.hex(),
            "STREAM_SUBJECT_TOKEN_V1": "0x" + owner_subject_domain.hex(),
            "streamCore": "0x" + owner_stream_core.hex(),
            "subjectId": "0x" + owner_subject.hex(),
            "domainSeparator": "0x" + owner_domain_separator.hex(),
            "structHash": "0x" + owner_struct_hash.hex(),
            "digest": "0x" + owner_digest.hex(),
        },
        "13.7": {
            "uriHash": "0x" + uri_hash_https.hex(),
            "hostHash": "0x" + host_hash.hex(),
            "resolvedAddressSetHash": "0x" + address_set_hash.hex(),
            "assertionHash": "0x" + assertion_hash.hex(),
            "assertionKey": "0x" + assertion_key.hex(),
            "assertionSubject": "0x" + assertion_subject.hex(),
            "EIP712 typeHash": "0x" + assertion_type.hex(),
            "structHash": "0x" + assertion_struct.hex(),
            "digest": "0x" + assertion_digest.hex(),
            "oldAssertionHash": "0x" + assertion_hash.hex(),
            "renewedAssertionHash": "0x" + renewed_assertion_hash.hex(),
        },
        "13.8": {
            "batchId": "0x" + batch_id.hex(),
            "batchCommitment": "0x" + batch_commitment.hex(),
        },
        "13.9": {
            "probeReleaseId": "0x" + release.hex(),
            "expectedCodeHash": "0x" + code_hash.hex(),
            "conformanceDocumentHash": "0x" + conformance.hex(),
            "expectedModuleVersion": "0x" + module_version.hex(),
            "capabilityCommitment": "0x" + capability.hex(),
            "interfaceProbeHash": "0x" + probe.hex(),
        },
        "13.9.3": check_canonicalizer_execution_limits(),
    }
    expected_values = {
        "subjectId": "0xa6e5bb8be82a8267e4c7a5398a63d1b1cf8d3c612aa4529349882667e8a2ba78",
        "recordHash": "0x217e7a966879dd7c379772be42f35fe353b45c113cec0ac76c21dd068bd506d1",
        "chainHash": "0xd4b722a75d08db3e38afd4cfa1a887ec72915640cd08af54596401e7fa62ac49",
        "recordDigest": "0x797c9ee306e88434acb70222d8510ee98bc5e502e3e3be94efeb94423d44dfca",
        "revokeDigest": "0x87c87440dbee8e7d2313e0be413d6222bea14055b0f324da81e0e9ef8849e4cd",
        "ownerRecordDigest": "0x1fe370911b6eda46ee6153458ffeac7bdc2c0c7fd7e9fb0af6d7385e66df2605",
        "assertionHash": "0xfd50c11dda2772e18067aab5b420f82784cec302f5327e459c894f437507b92a",
        "renewedAssertionHash": "0x757cefc2594290ff8a4fd62b99be6bf050165023c854b50061797dc9cc9f2eb5",
        "batchCommitment": "0x1c1c8c0c0c71816b08183589eaca344e6cd6b0ba1bc784c2d5a84337c377fc8d",
        "successorProbe": "0x8640ff49f37e78608f06f222a9a753e83c4e9687cb0d25f620368a8b7bc9dcc1",
    }
    assert vectors["13.1"]["subjectId"] == expected_values["subjectId"]
    assert vectors["13.2"]["recordHash"] == expected_values["recordHash"]
    assert vectors["13.2"]["chainHash"] == expected_values["chainHash"]
    assert vectors["13.3"]["digest"] == expected_values["recordDigest"]
    assert vectors["13.4"]["digest"] == expected_values["revokeDigest"]
    assert vectors["13.5"]["digest"] == expected_values["ownerRecordDigest"]
    assert vectors["13.7"]["assertionHash"] == expected_values["assertionHash"]
    assert vectors["13.7"]["renewedAssertionHash"] == expected_values["renewedAssertionHash"]
    assert vectors["13.8"]["batchCommitment"] == expected_values["batchCommitment"]
    assert vectors["13.9"]["interfaceProbeHash"] == expected_values["successorProbe"]
    return vectors


def check_governance_executor_vector() -> dict[str, str]:
    capability_domain = hx("0x560a68b3805ede9cc4ce0392157e0f258fa8a17fe9b645807781464e1eb3ba7b")
    role_domain = hx("0x5509945d050bff1c25739ca8055ca317188c749980e0e568fcca64f86ab3ceef")
    selector_set_hash = hx(EXPECTED_ALLOWLIST_HASH)
    binding_domain = k(b"6529networkmuseum.governance-executor-binding.v1")
    authority = hx("0x0000000000000000000000000000000000000042")
    registry = hx("0x000000000000000000000000000000000000cafe")
    current_executor = "0x0000000000000000000000000000000000000001"
    new_executor = hx("0x0000000000000000000000000000000000006529")
    release_id = k(b"MUSEUM_EXECUTOR_VECTOR_AUTHORITY_RELEASE_V1")
    code_hash = k(b"MUSEUM_EXECUTOR_VECTOR_AUTHORITY_CODE_V1")
    evidence_hash = k(b"MUSEUM_EXECUTOR_VECTOR_GOVERNANCE_EVIDENCE_V1")
    challenge = k(static_words(
        capability_domain, address_word(authority), address_word(registry),
        uint_word(1), address_word(new_executor), uint_word(2),
    ))
    capability = k(static_words(
        capability_domain, release_id, address_word(authority), code_hash,
        address_word(registry), role_domain, selector_set_hash, challenge,
        uint_word(1), address_word(new_executor), uint_word(2),
    ))
    binding = k(static_words(
        binding_domain, address_word(new_executor), evidence_hash, capability,
        uint_word(2), uint_word(1),
    ))
    rebound_authority = hx("0x0000000000000000000000000000000000000043")
    rebound_release_id = k(b"MUSEUM_EXECUTOR_VECTOR_REBOUND_AUTHORITY_RELEASE_V1")
    rebound_code_hash = k(b"MUSEUM_EXECUTOR_VECTOR_REBOUND_AUTHORITY_CODE_V1")
    rebound_challenge = k(static_words(
        capability_domain, address_word(rebound_authority), address_word(registry),
        uint_word(2), address_word(new_executor), uint_word(2),
    ))
    rebound_capability = k(static_words(
        capability_domain, rebound_release_id, address_word(rebound_authority),
        rebound_code_hash, address_word(registry), role_domain, selector_set_hash,
        rebound_challenge, uint_word(2), address_word(new_executor), uint_word(2),
    ))
    rebound_binding = k(static_words(
        binding_domain, address_word(new_executor), evidence_hash, rebound_capability,
        uint_word(2), uint_word(2),
    ))
    expected = {
        "authorityReleaseId": "0x442b8c759b677e48ed822ecf57344181e081deeb894664d60f0e076d22ef00e8",
        "authorityCodeHash": "0x17e02f491227b715d8167c6ee64b87a3c70d51345ab5cb63c23b003fccd44fa1",
        "evidenceHash": "0xb87be17166140c2103b87cadde72103d5673422df7e2a8fb0b0745e1e865f6fb",
        "challenge": "0x369583a21a48e0cb37b85e373ffcce219434789d2d4c536ae16a1a683c43729f",
        "capabilityCommitment": "0x970b6d8b04de91cb88b8b6fa3cf9f5af6faa46e452f27309a247ef7c5052e487",
        "bindingCommitment": "0x40a3c47c9686f82852e14e2b503ff9e02cdbed30d556db7347112bec4061e3f9",
        "reboundAuthorityReleaseId": "0xc7a2f5889fb4663ad2269ab003b5c32fe16ec960aeaf09f7255b4fe9adf998de",
        "reboundAuthorityCodeHash": "0x86d7cb2cdbcff163f6f0ee294587f8cec673905c2e4d077024a09f3529455f90",
        "reboundChallenge": "0xa858dee6314a072796ced21f2446e1324b27d61c97b2e437a0d639e8828bc15f",
        "reboundCapabilityCommitment": "0x3c884a3210b5f6d3a8ff58804c326c58b2d67d3088d8a692e9e62f0838c552b4",
        "reboundBindingCommitment": "0xdbb9a475785baab44b9a2c20fbdcb9a1626bdb853081135cae8afd58d7cbe73c",
        "crossBoundAfterExecutorRotation": "true",
        "crossBoundAfterAuthorityRotation": "true",
        "providerDeniedFreeze": "ACCEPT",
        "providerDeniedSuccessor": "ACCEPT",
    }
    actual = {
        "authorityReleaseId": "0x" + release_id.hex(),
        "authorityCodeHash": "0x" + code_hash.hex(),
        "evidenceHash": "0x" + evidence_hash.hex(),
        "challenge": "0x" + challenge.hex(),
        "capabilityCommitment": "0x" + capability.hex(),
        "bindingCommitment": "0x" + binding.hex(),
        "reboundAuthorityReleaseId": "0x" + rebound_release_id.hex(),
        "reboundAuthorityCodeHash": "0x" + rebound_code_hash.hex(),
        "reboundChallenge": "0x" + rebound_challenge.hex(),
        "reboundCapabilityCommitment": "0x" + rebound_capability.hex(),
        "reboundBindingCommitment": "0x" + rebound_binding.hex(),
        "crossBoundAfterExecutorRotation": "true",
        "crossBoundAfterAuthorityRotation": "true",
        "providerDeniedFreeze": "ACCEPT",
        "providerDeniedSuccessor": "ACCEPT",
    }
    assert actual == expected

    state = {
        "writesFrozen": False, "executor": current_executor, "executorRevision": 1,
        "authorityRevision": 1, "authorityCapability": None,
        "governanceCapability": None, "pending": None,
    }
    state["pending"] = {"executor": "0x" + new_executor.hex(), "revision": 2, **actual}
    assert state["pending"] is not None
    state["executor"] = "0x" + new_executor.hex()
    state["executorRevision"] = 2
    state["authorityCapability"] = actual["capabilityCommitment"]
    state["governanceCapability"] = actual["capabilityCommitment"]
    assert state["authorityCapability"] == state["governanceCapability"]
    state["authorityRevision"] = 2
    state["authorityCapability"] = actual["reboundCapabilityCommitment"]
    state["governanceCapability"] = actual["reboundCapabilityCommitment"]
    assert state["authorityCapability"] == state["governanceCapability"]
    provider_can_authorize = False
    emergency_authorized = state["executor"] == "0x" + new_executor.hex() and state["executorRevision"] == 2
    assert emergency_authorized and not provider_can_authorize
    state["writesFrozen"] = True
    state["pending"] = None
    assert state["pending"] is None
    assert emergency_authorized and state["writesFrozen"] and not provider_can_authorize
    try:
        if state["writesFrozen"]:
            raise ValueError("WritesFrozen")
        state["executor"] = current_executor
    except ValueError as error:
        assert str(error) == "WritesFrozen"
    else:
        raise AssertionError("post-freeze governance-executor rotation accepted")
    assert state["executor"] == "0x" + new_executor.hex()
    return actual


def check_source_commit_reachability() -> None:
    source_commit = "ff1c5825e3b61bfb2df0a639e057297beb946e4d"
    origin = subprocess.run(
        ["git", "config", "--get", "remote.origin.url"], cwd=REPO_ROOT,
        check=True, capture_output=True, text=True,
    ).stdout.strip().replace("\\", "/")
    assert re.fullmatch(
        r"(?:https://github\.com/|ssh://git@github\.com/|git@github\.com:)"
        r"6529-Collections/6529networkmuseum(?:\.git)?",
        origin,
        re.IGNORECASE,
    ), origin
    subprocess.run(["git", "cat-file", "-e", f"{source_commit}^{{commit}}"], cwd=REPO_ROOT, check=True)
    subprocess.run(
        ["git", "merge-base", "--is-ancestor", source_commit, "refs/remotes/origin/main"],
        cwd=REPO_ROOT, check=True,
    )


def check_selectors_and_allowlists() -> None:
    for signature, expected in (*ABI_SELECTORS, *INTERFACE_ONLY_SELECTORS, *STREAM_DRAFT_OWNER_SELECTORS):
        assert selector(signature) == expected, signature
    assert len({value for _, value in ABI_SELECTORS}) == len(ABI_SELECTORS)
    for literal, expected in GLOBAL_ROLE_IDS:
        assert "0x" + k(literal.encode("ascii")).hex() == expected, literal
    allowlist_words = [hx(value) + bytes(28) for value in AUTHORITY_SELECTOR_ALLOWLIST]
    assert tuple(sorted(AUTHORITY_SELECTOR_ALLOWLIST, key=lambda value: int(value, 16))) == AUTHORITY_SELECTOR_ALLOWLIST
    declared_selectors = {value for _, value in ABI_SELECTORS}
    assert set(AUTHORITY_SELECTOR_ALLOWLIST).issubset(declared_selectors), sorted(
        set(AUTHORITY_SELECTOR_ALLOWLIST) - declared_selectors
    )
    encoded = uint_word(32) + uint_word(len(allowlist_words)) + b"".join(allowlist_words)
    assert "0x" + k(encoded).hex() == EXPECTED_ALLOWLIST_HASH
    for record_type, expected_type, schema, expected_schema, _, authorization_class in STABLE_RECORD_TYPE_ALLOWLIST:
        assert "0x" + k(record_type.encode("ascii")).hex() == expected_type, record_type
        assert "0x" + k(schema.encode("ascii")).hex() == expected_schema, schema
        assert authorization_class in (10, 11, 12)


def check_published_transcript(executor_vector: dict[str, str], vectors: dict[str, dict[str, str]]) -> None:
    spec = SPEC_PATH.read_text(encoding="utf-8")
    research = RESEARCH_PATH.read_text(encoding="utf-8")
    assert "ff1c5825e3b61bfb2df0a639e057297beb946e4d" in spec
    assert "0x8bb17fc4361cbfe29c586218e716d0c4789973b222ee7a403f9d22f6f483a280" in spec
    assert "### 13.6 Release-manifest vector" in spec
    profile_rows = (
        (
            "Empty-payload canonicalization", "MUSEUM_EMPTY_PAYLOAD_V1",
            EMPTY_PAYLOAD_CANONICALIZATION_ID,
        ),
        (
            "HTTPS capacity-report profile", "MUSEUM_HTTPS_ASSERTION_CAPACITY_REPORT_V1",
            "0x8254a96c886cc988ce26c264ffacd912591f898c2af6202c5aef644264741d2e",
        ),
    )
    for kind, literal, expected in profile_rows:
        assert "0x" + k(literal.encode("ascii")).hex() == expected, literal
        assert spec.count(f"| {kind} | `{literal}` | `{expected}` |") == 1, literal
    headings = list(re.finditer(r"^### (13\.[0-9]+(?:\.[0-9]+)?)\b", spec, re.MULTILINE))
    section_text: dict[str, str] = {}
    for index, match in enumerate(headings):
        end = headings[index + 1].start() if index + 1 < len(headings) else len(spec)
        section_text[match.group(1)] = spec[match.start():end]
    for section, rows in vectors.items():
        assert section in section_text, section
        for label, value in rows.items():
            spaced = f"{label} = {value}"
            compact = f"{label}={value}"
            assert spaced in section_text[section] or compact in section_text[section], (section, label)
    manifest_section = section_text["13.6"]
    for line in (
        "pathHash = 0x47f5e941106c25d308590891c8eb0bb3c721586361b9a9bf442b49782c132183",
        "payloadBytesHash = 0x3f29b41d9d595ee7c116a4905fd8f4faf620b5757037db8a8988cd87b9c972a7",
        "entryHash = 0xfa531a4233206547049d1b83c4b4e3e4d9763effb47227b2fd761ea1846ddfc8",
        "root = 0x8bb17fc4361cbfe29c586218e716d0c4789973b222ee7a403f9d22f6f483a280",
    ):
        assert line in manifest_section, line
    block = re.search(r"\$selectorGolden = \[ordered\]@\{(.*?)\n\}", research, re.DOTALL)
    assert block is not None
    published = tuple(re.findall(r"'([^']+)' = '(0x[0-9a-f]{8})'", block.group(1)))
    assert published == ABI_SELECTORS
    for literal, expected in GLOBAL_ROLE_IDS:
        assert f"`{literal}` | `{expected}`" in spec
    for record_type, expected_type, schema, expected_schema, authorization_name, authorization_class in STABLE_RECORD_TYPE_ALLOWLIST:
        expected_row = f"| `{record_type}` | `{expected_type}` | `{schema}` | `{authorization_name} ({authorization_class})` |"
        assert spec.count(expected_row) == 1, expected_row
        expected_schema_row = f"| Payload schema | `{schema}` | `{expected_schema}` |"
        assert spec.count(expected_schema_row) == 1, expected_schema_row
    assert ",".join(AUTHORITY_SELECTOR_ALLOWLIST) in research
    assert "$trustedRef = 'refs/remotes/origin/main'" in research
    assert "git merge-base --is-ancestor $sourceCommit $trustedRef" in research
    assert "equality to its current tip is neither" in research
    assert "A state-only auditor MUST dereference `RecordSummary.httpsAssertionHash`" in spec
    assert "returns exactly the four-byte ERC-1271 magic value `0x1626ba7e`" in spec
    assert "address[] sortedUniqueAddresses;" in spec
    assert "uint64 recordTypePolicyRevision;" in spec
    assert "uint64 grantRevision;" in spec
    for label, value in executor_vector.items():
        assert spec.count(f"{label} = {value}") == 1, label
    assert "freezeClearsPendingExecutor = true" in spec
    assert "postFreezeExecuteGovernanceExecutor = REJECT WritesFrozen" in spec


def main() -> int:
    root = check_manifest_vector()
    executor_vector = check_governance_executor_vector()
    vectors = check_general_vectors()
    check_source_commit_reachability()
    check_selectors_and_allowlists()
    check_published_transcript(executor_vector, vectors)
    print("sourceCommit=ff1c5825e3b61bfb2df0a639e057297beb946e4d")
    print(f"oneRecordManifestRoot=0x{root.hex()}")
    print(f"canonicalAbiSelectors={len(ABI_SELECTORS)}")
    print(f"streamDraftOwnerSelectors={len(STREAM_DRAFT_OWNER_SELECTORS)}")
    print(f"authorizationSelectorAllowlist={len(AUTHORITY_SELECTOR_ALLOWLIST)}")
    print(f"stableRecordTypeAllowlist={len(STABLE_RECORD_TYPE_ALLOWLIST)}")
    print(f"governanceExecutorBindingCommitment={executor_vector['bindingCommitment']} freezeReplay=REJECT")
    print(f"publishedVectorSections={','.join(vectors)}")
    print(f"noneContentHash={EMPTY_PAYLOAD_HASH_REF_HASH} directRelayedBatchMutations=REJECT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
