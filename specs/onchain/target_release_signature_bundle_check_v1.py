"""Validate the detached TargetRelease signature-byte bundle V1 fixture.

This is a deterministic, offline conformance check.  Its identifiers model
content-addressed retrieval; they are test vectors, not deployment evidence.
"""

from __future__ import annotations

import base64
import hashlib
import json
import copy
import re
from pathlib import Path

import jsonschema
import rfc8785
from Crypto.Hash import keccak

from abi_encoding_v1 import address_word, static_words, uint_word
from release_attestor_policy_check_v1 import (
    load_and_validate_policy,
    policy_hash as release_attestor_policy_hash,
    signer_set_hash as release_attestor_signer_set_hash,
)


if not __debug__:
    raise SystemExit("optimized Python disables conformance checks")


ROOT = Path(__file__).resolve().parent
BUNDLE_PATH = ROOT / "target-release-signature-bundle-v1.fixture.json"
REFERENCE_PATH = ROOT / "target-release-signature-bundle-v1.reference.json"
SCHEMA_PATH = ROOT / "target-release-signature-bundle-v1.schema.json"
EVIDENCE_SCHEMA_PATH = ROOT / "target-release-evidence-v1.schema.json"
EVIDENCE_PATH = ROOT / "target-release-evidence-v1.fixture.json"
SPEC_PATH = ROOT / "contract-migration-v1.md"

EXPECTED_SCHEMA_HASH = "12256931d7eebded2483454fdff90c2496ffca9cec980b1a07306b03082bef82"
FIXTURE_CHAIN_ID = 1
FIXTURE_REGISTRY_ADDRESS = "0x0000000000000000000000000000000000006529"

# secp256k1 constants. They are used only to recover public keys from the
# public test signatures; no private key is retained by this repository.
P = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
G = (
    0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
    0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8,
)


def k(value: bytes) -> bytes:
    digest = keccak.new(digest_bits=256)
    digest.update(value)
    return digest.digest()


EIP712_DOMAIN_TYPEHASH = k(b"EIP712Domain(string name,string version,uint256 chainId,address verifyingContract)")
EIP712_NAME_HASH = k(b"6529NetworkMuseumTargetRelease")
EIP712_VERSION_HASH = k(b"1")
TARGET_RELEASE_ATTESTATION_TYPEHASH = k(
    b"MuseumTargetReleaseAttestation(bytes32 releaseId,bytes32 conformanceDocumentHash,bytes32 signedDocumentHash,bytes32 releaseAttestorPolicyHash,bytes32 releaseAttestorSignerSetHash)"
)
RELEASE_SIGNATURE_SET_DOMAIN = k(b"6529networkmuseum.release-signature-set.v1")


def release_attestation_digest(
    chain_id: int,
    registry_address: str,
    release_id: str,
    conformance_document_hash: str,
    signed_document_hash: str,
    release_attestor_policy_hash: str,
    release_attestor_signer_set_hash: str,
) -> bytes:
    domain_separator = k(static_words(
        EIP712_DOMAIN_TYPEHASH,
        EIP712_NAME_HASH,
        EIP712_VERSION_HASH,
        uint_word(chain_id),
        address_word(bytes.fromhex(registry_address.removeprefix("0x"))),
    ))
    struct_hash = k(static_words(
        TARGET_RELEASE_ATTESTATION_TYPEHASH,
        bytes.fromhex(release_id.removeprefix("0x")),
        bytes.fromhex(conformance_document_hash.removeprefix("0x")),
        bytes.fromhex(signed_document_hash.removeprefix("0x")),
        bytes.fromhex(release_attestor_policy_hash.removeprefix("0x")),
        bytes.fromhex(release_attestor_signer_set_hash.removeprefix("0x")),
    ))
    return k(b"\x19\x01" + domain_separator + struct_hash)


def release_signature_set_hash(digest: bytes, entries: list[dict[str, str]]) -> str:
    words = [RELEASE_SIGNATURE_SET_DOMAIN, digest]
    for entry in entries:
        words.extend((
            address_word(bytes.fromhex(entry["signer"].removeprefix("0x"))),
            bytes.fromhex(entry["signatureCommitment"].removeprefix("0x")),
        ))
    return "0x" + k(static_words(*words)).hex()


def point_add(left: tuple[int, int] | None, right: tuple[int, int] | None) -> tuple[int, int] | None:
    if left is None:
        return right
    if right is None:
        return left
    x1, y1 = left
    x2, y2 = right
    if x1 == x2 and (y1 + y2) % P == 0:
        return None
    slope = ((3 * x1 * x1) * pow(2 * y1, -1, P) if left == right else (y2 - y1) * pow(x2 - x1, -1, P)) % P
    x3 = (slope * slope - x1 - x2) % P
    return x3, (slope * (x1 - x3) - y1) % P


def point_multiply(scalar: int, point: tuple[int, int]) -> tuple[int, int] | None:
    result = None
    addend = point
    while scalar:
        if scalar & 1:
            result = point_add(result, addend)
        addend = point_add(addend, addend)
        scalar >>= 1
    return result


def recover_address(message_hash: bytes, signature: bytes) -> str:
    if len(message_hash) != 32 or len(signature) != 65:
        raise ValueError("invalid recovery input length")
    r = int.from_bytes(signature[:32], "big")
    s = int.from_bytes(signature[32:64], "big")
    recovery_id = signature[64]
    if not 0 < r < N or not 0 < s <= N // 2 or recovery_id not in (0, 1):
        raise ValueError("invalid canonical ECDSA signature")
    x = r
    y = pow((x * x * x + 7) % P, (P + 1) // 4, P)
    if y % 2 != recovery_id:
        y = P - y
    point_r = (x, y)
    if point_multiply(N, point_r) is not None:
        raise ValueError("recovery point is outside secp256k1 subgroup")
    z = int.from_bytes(message_hash, "big")
    inverse_r = pow(r, -1, N)
    public_key = point_add(point_multiply((s * inverse_r) % N, point_r), point_multiply((-z * inverse_r) % N, G))
    if public_key is None:
        raise ValueError("recovered point at infinity")
    return "0x" + k(public_key[0].to_bytes(32, "big") + public_key[1].to_bytes(32, "big"))[-20:].hex()


def cidv1_raw_sha256(payload: bytes) -> str:
    multihash = b"\x01\x55\x12\x20" + hashlib.sha256(payload).digest()
    return "ipfs://b" + base64.b32encode(multihash).decode("ascii").lower().rstrip("=")


def validate_entry_identity(entries: list[dict[str, str]]) -> None:
    if len(entries) != 2:
        raise ValueError("ENTRY_COUNT")
    signers = [entry["signer"] for entry in entries]
    if len(set(signers)) != 2:
        raise ValueError("DUPLICATE_SIGNER")
    if signers != sorted(signers):
        raise ValueError("SIGNER_ORDER")
    commitments = [entry["signatureCommitment"] for entry in entries]
    if len(set(commitments)) != 2:
        raise ValueError("DUPLICATE_SIGNATURE_COMMITMENT")


def validate_documentation(reference: dict, evidence: dict) -> None:
    spec = SPEC_PATH.read_text(encoding="utf-8")
    blocks = re.findall(
        r"<!-- TARGET_RELEASE_BUNDLE_VECTOR_V1_BEGIN -->(.*?)<!-- TARGET_RELEASE_BUNDLE_VECTOR_V1_END -->",
        spec,
        re.DOTALL,
    )
    assert len(blocks) == 1
    values = dict(re.findall(r"^([A-Za-z][A-Za-z0-9]+) = (\S+)$", blocks[0], re.MULTILINE))
    expected = {
        "releaseId": evidence["releaseId"],
        "releaseAttestorPolicyHash": evidence["signers"]["policyHash"],
        "releaseAttestorSignerSetHash": evidence["signers"]["signerSetHash"],
        "D0ConformanceDocumentHash": evidence["conformanceDocumentHash"],
        "D1SignedDocumentHash": evidence["signers"]["signedDocumentHash"],
        "releaseAttestationDigest": evidence["signers"]["releaseAttestationDigest"],
        "releaseSignatureSetHash": release_signature_set_hash(
            bytes.fromhex(evidence["signers"]["releaseAttestationDigest"][2:]),
            json.loads(BUNDLE_PATH.read_text(encoding="utf-8"))["entries"],
        ),
        "bundleUri": reference["uri"],
        "alternateBundleUri": reference["availability"][1]["uri"],
        "bundleContentHash": reference["contentHash"],
        "bundleBytes": str(reference["sizeBytes"]),
        "bundleSchemaHash": reference["schemaHash"],
        "ipfsFetchObservationHash": reference["availability"][0]["fetchObservationHash"],
        "arFetchObservationHash": reference["availability"][1]["fetchObservationHash"],
    }
    for label, expected_value in expected.items():
        assert values.get(label) == expected_value, label
    for stale in (
        "0x809e19f8e094804ffd9b7b8b4dd86d1597148d55f798b776e3e6f1dd0a02ba83",
        "ipfs://bafkreidtpcfaumxixdprbdlhqigzaicjua7u3zxuqwcg5grcmmnntxt6qu",
        "0xacf3819991e8be43bdeadd90707cc7a1ed01345f1faa682c63acc1ef7af56a65",
        "ipfs://bafkreihtaaya2ro2hb543773zxb5bgimfnioz5l6cf5srnz7v4xogl24lu",
    ):
        assert stale not in spec


def main() -> int:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    evidence_schema = json.loads(EVIDENCE_SCHEMA_PATH.read_text(encoding="utf-8"))
    evidence = json.loads(EVIDENCE_PATH.read_text(encoding="utf-8"))
    bundle = json.loads(BUNDLE_PATH.read_text(encoding="utf-8"))
    reference = json.loads(REFERENCE_PATH.read_text(encoding="utf-8"))
    jsonschema.validate(evidence, evidence_schema)
    jsonschema.validate(bundle, schema)
    canonical = rfc8785.dumps(bundle)
    attestor_policy = load_and_validate_policy()

    assert k(rfc8785.dumps(schema)).hex() == EXPECTED_SCHEMA_HASH
    assert bundle["releaseId"] == evidence["releaseId"]
    assert bundle["chainId"] == FIXTURE_CHAIN_ID
    assert bundle["registryAddress"] == FIXTURE_REGISTRY_ADDRESS
    assert bundle["conformanceDocumentHash"] == evidence["conformanceDocumentHash"]
    assert bundle["signedDocumentHash"] == evidence["signers"]["signedDocumentHash"]
    assert bundle["releaseAttestorPolicyHash"] == evidence["signers"]["policyHash"]
    assert bundle["releaseAttestorSignerSetHash"] == evidence["signers"]["signerSetHash"]
    assert evidence["signers"]["policyId"] == attestor_policy["policyId"]
    assert evidence["signers"]["policyHash"] == release_attestor_policy_hash(attestor_policy)
    assert evidence["signers"]["signerSetHash"] == release_attestor_signer_set_hash(attestor_policy)
    assert evidence["signers"]["threshold"] == attestor_policy["threshold"]
    assert evidence["signers"]["signatureScheme"] == attestor_policy["signatureScheme"]
    assert evidence["signers"]["addresses"] == attestor_policy["addresses"]
    assert cidv1_raw_sha256(canonical) == evidence["detachedSignatureBundle"]["uri"]

    sign_digest = release_attestation_digest(
        bundle["chainId"],
        bundle["registryAddress"],
        bundle["releaseId"],
        bundle["conformanceDocumentHash"],
        bundle["signedDocumentHash"],
        bundle["releaseAttestorPolicyHash"],
        bundle["releaseAttestorSignerSetHash"],
    )
    assert bundle["releaseAttestationDigest"] == "0x" + sign_digest.hex()
    assert evidence["signers"]["releaseAttestationDigest"] == bundle["releaseAttestationDigest"]
    entries = bundle["entries"]
    validate_entry_identity(entries)
    assert evidence["signers"]["threshold"] == 2
    assert set(entry["signer"] for entry in entries).issubset(evidence["signers"]["addresses"])
    assert [entry["signatureCommitment"] for entry in entries] == evidence["signers"]["signatureCommitments"]
    for entry in entries:
        signature = bytes.fromhex(entry["signature"][2:])
        assert k(signature).hex() == entry["signatureCommitment"][2:]
        assert recover_address(sign_digest, signature) == entry["signer"]

    jsonschema.validate(reference, evidence_schema["properties"]["detachedSignatureBundle"])
    assert reference == evidence["detachedSignatureBundle"]
    assert reference["uri"] == cidv1_raw_sha256(canonical)
    assert reference["contentHash"] == "0x" + k(canonical).hex()
    assert reference["sizeBytes"] == len(canonical)
    assert len({row["uri"] for row in reference["availability"]}) == 2
    assert all(row["contentHash"] == reference["contentHash"] for row in reference["availability"])
    validate_documentation(reference, evidence)

    duplicate_signer = copy.deepcopy(bundle)
    duplicate_signer["entries"][1]["signer"] = duplicate_signer["entries"][0]["signer"]
    jsonschema.validate(duplicate_signer, schema)
    try:
        validate_entry_identity(duplicate_signer["entries"])
    except ValueError as error:
        assert str(error) == "DUPLICATE_SIGNER"
    else:
        raise AssertionError("schema-only duplicate signer passed semantic validation")

    for wrong_count in (1, 3):
        mutation = copy.deepcopy(bundle)
        if wrong_count == 1:
            mutation["entries"].pop()
        else:
            extra = copy.deepcopy(mutation["entries"][-1])
            extra["signer"] = evidence["signers"]["addresses"][2]
            mutation["entries"].append(extra)
        try:
            jsonschema.validate(mutation, schema)
        except jsonschema.ValidationError:
            pass
        else:
            raise AssertionError(f"{wrong_count}-entry bundle passed exact 2-of-3 schema")

    unauthorized = copy.deepcopy(bundle)
    unauthorized["entries"][1]["signer"] = "0x8000000000000000000000000000000000000000"
    jsonschema.validate(unauthorized, schema)
    assert not set(entry["signer"] for entry in unauthorized["entries"]).issubset(evidence["signers"]["addresses"])

    print(f"bundleUri={reference['uri']}")
    print(f"bundleContentHash={reference['contentHash']}")
    print(f"bundleBytes={reference['sizeBytes']}")
    print(f"bundleSchemaHash=0x{EXPECTED_SCHEMA_HASH}")
    print(f"signatureDigest=0x{sign_digest.hex()}")
    print(f"releaseSignatureSetHash={release_signature_set_hash(sign_digest, entries)}")
    print("signatureRecovery=2/3")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
