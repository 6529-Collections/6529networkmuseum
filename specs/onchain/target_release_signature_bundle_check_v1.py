"""Validate the detached TargetRelease signature-byte bundle V1 fixture.

This is a deterministic, offline conformance check.  Its identifiers model
content-addressed retrieval; they are test vectors, not deployment evidence.
"""

from __future__ import annotations

import base64
import hashlib
import json
from pathlib import Path

import jsonschema
import rfc8785
from Crypto.Hash import keccak


ROOT = Path(__file__).resolve().parent
BUNDLE_PATH = ROOT / "target-release-signature-bundle-v1.fixture.json"
REFERENCE_PATH = ROOT / "target-release-signature-bundle-v1.reference.json"
SCHEMA_PATH = ROOT / "target-release-signature-bundle-v1.schema.json"
EVIDENCE_SCHEMA_PATH = ROOT / "target-release-evidence-v1.schema.json"

EXPECTED_SCHEMA_HASH = "cc8807c693ea28ae50ba76544608529bb465ad11a1de5cfb1db5052916457439"
EXPECTED_RELEASE_ID = "caab6726358fae34ce8d4a969ce487e81c67b8003f76a8e57ab958be7cb6a63c"
EXPECTED_SIGNED_DOCUMENT_HASH = "a6e6398c9909bab2d2c4f2d9a26a2d357e3451f2a0ca8097691eba1cd41079c7"
EXPECTED_BUNDLE_HASH = "9201549e174049b0b389c44bcaaf86458cf2885ada61b2ad5a0f55196634b26f"
EXPECTED_IPFS_URI = "ipfs://bafkreifvfwpn5kbrw73c7jjydgwz5h7tacmv5n7zsesmbjho4crnfu3qtq"
EXPECTED_AR_URI = "ar://f69odaLOBxZAMm9ygWje576VMKP7-6nFsypCpNZYmCk"
EXPECTED_IPFS_OBSERVATION = "6c7cbb37a256f94a1a486a47bb158002258bac7c38dd417e70087b4e40b22324"
EXPECTED_AR_OBSERVATION = "997ed37a67abf99ed4b44942527a626e37ee3d696cbf0ad84dbea0ed7900dfc3"

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


def main() -> int:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    evidence_schema = json.loads(EVIDENCE_SCHEMA_PATH.read_text(encoding="utf-8"))
    bundle = json.loads(BUNDLE_PATH.read_text(encoding="utf-8"))
    reference = json.loads(REFERENCE_PATH.read_text(encoding="utf-8"))
    jsonschema.validate(bundle, schema)
    canonical = rfc8785.dumps(bundle)

    assert k(rfc8785.dumps(schema)).hex() == EXPECTED_SCHEMA_HASH
    assert bundle["releaseId"] == "0x" + EXPECTED_RELEASE_ID
    assert bundle["signedDocumentHash"] == "0x" + EXPECTED_SIGNED_DOCUMENT_HASH
    assert len(canonical) == 1131
    assert k(canonical).hex() == EXPECTED_BUNDLE_HASH
    assert cidv1_raw_sha256(canonical) == EXPECTED_IPFS_URI

    sign_digest = k(b"\x19Ethereum Signed Message:\n32" + bytes.fromhex(EXPECTED_SIGNED_DOCUMENT_HASH))
    entries = bundle["entries"]
    assert [entry["signer"] for entry in entries] == sorted(entry["signer"] for entry in entries)
    assert len({entry["signer"] for entry in entries}) == 3
    for entry in entries:
        signature = bytes.fromhex(entry["signature"][2:])
        assert k(signature).hex() == entry["signatureCommitment"][2:]
        assert recover_address(sign_digest, signature) == entry["signer"]

    jsonschema.validate(reference, evidence_schema["properties"]["detachedSignatureBundle"])
    assert reference["uri"] == EXPECTED_IPFS_URI
    assert reference["contentHash"] == "0x" + EXPECTED_BUNDLE_HASH
    assert reference["sizeBytes"] == len(canonical)
    assert reference["availability"] == [
        {"uri": EXPECTED_IPFS_URI, "contentHash": "0x" + EXPECTED_BUNDLE_HASH, "fetchObservationHash": "0x" + EXPECTED_IPFS_OBSERVATION},
        {"uri": EXPECTED_AR_URI, "contentHash": "0x" + EXPECTED_BUNDLE_HASH, "fetchObservationHash": "0x" + EXPECTED_AR_OBSERVATION},
    ]
    assert len({row["uri"] for row in reference["availability"]}) == 2
    assert all(row["contentHash"] == reference["contentHash"] for row in reference["availability"])

    print(f"bundleUri={reference['uri']}")
    print(f"bundleContentHash={reference['contentHash']}")
    print(f"bundleBytes={reference['sizeBytes']}")
    print(f"bundleSchemaHash=0x{EXPECTED_SCHEMA_HASH}")
    print(f"signatureDigest=0x{sign_digest.hex()}")
    print("signatureRecovery=3/3")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
