"""Offline V1 manifest-vector and canonical ABI/authorization checker.

This checker is a conformance fixture for the design specification only.  It
does not contact a chain, publish a release, or authorize any deployment.
"""

from __future__ import annotations

import re
from pathlib import Path

from Crypto.Hash import keccak

from abi_encoding_v1 import address_word, bytes32_arrays, static_words, uint_word


ROOT = Path(__file__).resolve().parent
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
    ("successor()", "0x6ff968c3"),
    ("writesFrozen()", "0x290d086b"),
    ("pendingAuthority()", "0xfabb94bb"),
    ("successorTarget()", "0xae540c6b"),
    ("externalAssetSubjectId(bytes32,string)", "0x0b88b5e8"),
    ("registerExternalAsset(bytes32,string,bytes32)", "0x73c0a0b4"),
    ("externalAsset(bytes32)", "0xdb08b0b0"),
    ("admitAssetProfile(bytes32,bytes32,bytes32,string,address,uint8,bytes32,bytes32,bytes32)", "0xba597a03"),
    ("assetProfile(bytes32)", "0x2938cf75"),
    ("admitSchema(bytes32,bytes32,string,bool)", "0x541fd287"),
    ("schema(bytes32)", "0x072b9cf2"),
    ("admitRecordFamily(bytes32,uint8,uint16)", "0x63d20b1a"),
    ("recordFamily(bytes32)", "0x1ca9f8aa"),
    ("admitRecordType(bytes32,bytes32,bytes32,uint8)", "0x46a9f249"),
    ("recordTypePolicy(bytes32)", "0xcd2369a6"),
    ("setRecordFamilyGrant(bytes32,uint8,address,bool)", "0x40ee7ee3"),
    ("recordFamilyGrant(bytes32,uint8,address)", "0x1118ed2f"),
    ("admitTargetRelease(uint8,address,bytes32,bytes32,bytes32,bytes32,bytes32,bytes32,bytes32,bytes32,bytes4,bytes32,bytes32,bytes32,bytes32,bytes32)", "0x0742c529"),
    ("targetRelease(uint8,address,bytes32)", "0x85968ef0"),
    ("targetReleaseAtRevision(uint8,address,bytes32,uint64)", "0x288b2e93"),
    ("targetReleaseById(bytes32)", "0xb9bc97a1"),
    ("quarantineTargetRelease(uint8,address,bytes32,bytes32)", "0xda6d916f"),
    ("setAuthority((address,bytes32,bytes4,bytes32,bytes32,address,bytes32,bytes32))", "0x81a86ff4"),
    ("executeAuthority()", "0xc9dc7d0d"),
    ("cancelAuthority()", "0xf0edf065"),
    ("setGlobalRoleGrant(bytes32,address,bool)", "0xab6627c3"),
    ("globalRoleGrant(bytes32,address)", "0x59d2fe4a"),
    ("admitHttpsResolverProfile(bytes32,bytes32,address,uint64,uint64)", "0xaf2fb948"),
    ("resolverProfile(bytes32)", "0x3711d316"),
    ("recordHttpsAssertionBySig(string,bytes32,bytes32,uint64,bytes32,uint64,bytes32,uint64,uint64,address,uint256,uint64,address[],bytes)", "0x1e0c9fe6"),
    ("httpsAssertion(bytes32,bytes32,uint64,uint64)", "0x1120d46d"),
    ("currentHttpsAssertion(bytes32)", "0x080dab7b"),
    ("httpsAssertionByHash(bytes32)", "0x28208c17"),
    ("admitStreamOwnerRecordInterface(address,bytes32,bytes32,bytes32)", "0x75c75961"),
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
    ("setStreamMirrorLink(bytes32,address,address,uint256,uint256,bytes32,bytes32,bytes32,bytes32)", "0x49c44b5c"),
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
    ("ownerRecordHash(uint256)", "0x9ab2d595"),
    ("ownerRecordHashDomain()", "0xe79efeda"),
    ("ownerRecordHashVectorId()", "0xfda2f68a"),
)

GLOBAL_ROLE_IDS = (
    ("MUSEUM_GLOBAL_ROLE_GOVERNANCE_EXECUTOR_V1", "0x865cb1cc1a43094ea97b42f5b9e950e7952c1f106d37051e97d2a3fdb1584ce2"),
    ("MUSEUM_GLOBAL_ROLE_REGISTRAR_V1", "0xb1f5e657823d31bde6c263be60f0418d7361b8365b264c97798c0b790c1a5f8b"),
    ("MUSEUM_GLOBAL_ROLE_MIGRATION_ADMIN_V1", "0x2729f1662f9bb2682a0a433e8329cd1b73680e122f49b4b4987cef1106b97004"),
    ("MUSEUM_GLOBAL_ROLE_AUTHORITY_ADMIN_V1", "0x28ad41c29b6a0872dec6410316cebb3f72fc3c9e4f4ea88e8e87e81784c94426"),
    ("MUSEUM_GLOBAL_ROLE_HTTPS_ATTESTOR_V1", "0x47df6320f751abd29d6ce09022685a520d0128d5f284c7573d3b6857127abc61"),
)

AUTHORITY_SELECTOR_ALLOWLIST = (
    "0x05d53fba", "0x0742c529", "0x43dd6c37", "0x81a86ff4",
    "0xab6627c3", "0xc9dc7d0d", "0xda6d916f", "0xf0edf065",
)
EXPECTED_ALLOWLIST_HASH = "0xafee23b5447d9b050283c506b2af140cf332002f55e035ad1edfe6c5a4bb34b3"

STABLE_RECORD_TYPE_ALLOWLIST = (
    ("MUSEUM_EXTERNAL_ASSET_IDENTITY", "0xe1c1798f46d210552c5d3924b7059a57b07eedf054640a662eb47bac008b4a8e", "MUSEUM_EXTERNAL_ASSET_IDENTITY_V1", "0x34e9649723069df3772c810e6e825f7589c211bac81acc9b908a60067f936aa6", 10),
    ("MUSEUM_CUSTODY_OBSERVATION", "0x8351820e5600a2472b0dd68eb83a0480b8663df2efcab7d34321b1df5918316e", "MUSEUM_CUSTODY_OBSERVATION_V1", "0xb0c467baa7db6862385e58253c1c4702d95b141a1ef66cd2b86234a597344014", 11),
    ("MUSEUM_ACCESSION_LOT", "0xc544e9b2b8226296197005f65dd84855588d18be5e1ce13082b8314004cb4661", "MUSEUM_ACCESSION_LOT_V1", "0x8bb4cfecf4d3736765bc80624dd0a876d2e1c17bf5a406066d5f2256fc739d44", 11),
    ("MUSEUM_PROGRAM_OUTCOME", "0xe81870465556c524f1375c1a3cff4aa920e8f0c15b9858ae6bb55c6c3cb0ad5a", "MUSEUM_PROGRAM_OUTCOME_V1", "0x7a25e6a6a5e91d55ef0ea9115ad5902929bcf0d3331b4bb2d22100f65fc78470", 11),
    ("MUSEUM_RESEARCH_NOTE", "0x5a50f1234f1c89b5d9c2f5b2062279349feac41d8e01bf708ee9adc20a2d8ba0", "MUSEUM_RESEARCH_NOTE_V1", "0xe3d3da75ee91ec6a7603f809eb413342e42874cabf3992d443409657745c3cf0", 11),
    ("MUSEUM_RELEASE_MANIFEST", "0x8889bb0d1446ec07b517aca915af9a4ad6d993ef8af5b999301ca8b15f789084", "MUSEUM_RELEASE_MANIFEST_V1", "0x7a41091035def3c5fa62722d73a7ea87f996fe9be34e9115317c5d128581d299", 12),
)


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


def check_selectors_and_allowlists() -> None:
    for signature, expected in (*ABI_SELECTORS, *INTERFACE_ONLY_SELECTORS):
        assert selector(signature) == expected, signature
    assert len({value for _, value in ABI_SELECTORS}) == len(ABI_SELECTORS)
    for literal, expected in GLOBAL_ROLE_IDS:
        assert "0x" + k(literal.encode("ascii")).hex() == expected, literal
    allowlist_words = [hx(value) + bytes(28) for value in AUTHORITY_SELECTOR_ALLOWLIST]
    assert tuple(sorted(AUTHORITY_SELECTOR_ALLOWLIST, key=lambda value: int(value, 16))) == AUTHORITY_SELECTOR_ALLOWLIST
    encoded = uint_word(32) + uint_word(len(allowlist_words)) + b"".join(allowlist_words)
    assert "0x" + k(encoded).hex() == EXPECTED_ALLOWLIST_HASH
    for record_type, expected_type, schema, expected_schema, authorization_class in STABLE_RECORD_TYPE_ALLOWLIST:
        assert "0x" + k(record_type.encode("ascii")).hex() == expected_type, record_type
        assert "0x" + k(schema.encode("ascii")).hex() == expected_schema, schema
        assert authorization_class in (10, 11, 12)


def check_published_transcript() -> None:
    spec = SPEC_PATH.read_text(encoding="utf-8")
    research = RESEARCH_PATH.read_text(encoding="utf-8")
    assert "ff1c5825e3b61bfb2df0a639e057297beb946e4d" in spec
    assert "0x8bb17fc4361cbfe29c586218e716d0c4789973b222ee7a403f9d22f6f483a280" in spec
    assert "### 13.6 Release-manifest vector" in spec
    block = re.search(r"\$selectorGolden = \[ordered\]@\{(.*?)\n\}", research, re.DOTALL)
    assert block is not None
    published = tuple(re.findall(r"'([^']+)' = '(0x[0-9a-f]{8})'", block.group(1)))
    assert published == ABI_SELECTORS
    for literal, expected in GLOBAL_ROLE_IDS:
        assert f"`{literal}` | `{expected}`" in spec
    for record_type, expected_type, schema, expected_schema, authorization_class in STABLE_RECORD_TYPE_ALLOWLIST:
        assert f"| `{record_type}` | `{expected_type}` | `{schema}` |" in spec
        assert expected_schema in spec
        assert f"({authorization_class})" in spec
    assert ",".join(AUTHORITY_SELECTOR_ALLOWLIST) in research
    assert "A state-only auditor MUST dereference `RecordSummary.httpsAssertionHash`" in spec


def main() -> int:
    root = check_manifest_vector()
    check_selectors_and_allowlists()
    check_published_transcript()
    print("sourceCommit=ff1c5825e3b61bfb2df0a639e057297beb946e4d")
    print(f"oneRecordManifestRoot=0x{root.hex()}")
    print(f"canonicalAbiSelectors={len(ABI_SELECTORS)}")
    print(f"authorizationSelectorAllowlist={len(AUTHORITY_SELECTOR_ALLOWLIST)}")
    print(f"stableRecordTypeAllowlist={len(STABLE_RECORD_TYPE_ALLOWLIST)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
