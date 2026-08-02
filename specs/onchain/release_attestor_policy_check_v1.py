"""Validate the governed release-attestor policy and signer-set commitment.

The checked policy is a public non-deployment fixture. A production deployment
must substitute a governance-approved policy artifact and immutably bind both
commitments in the registry constructor and release rows.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path

import jsonschema
import rfc8785
from Crypto.Hash import keccak

from abi_encoding_v1 import address_word, static_words, uint_word


if not __debug__:
    raise SystemExit("optimized Python disables conformance checks")


ROOT = Path(__file__).resolve().parent
POLICY_PATH = ROOT / "release-attestor-policy-v1.fixture.json"
POLICY_SCHEMA_PATH = ROOT / "release-attestor-policy-v1.schema.json"
EXPECTED_SCHEMA_HASH = "0x7ce79b67b7882dfa70c5bee9e62b7ccba9a987a338ae3b0186862e03a21bbc06"
EXPECTED_POLICY_HASH = "0xf57a8f644ffb7acc960d2aa9b86b8381eda086e6e8ce1300b17fecb30c4f35e8"
EXPECTED_SIGNER_SET_HASH = "0x4c22201c9dce9842bd7393223caa67d3383f802013b6d3fb6530f9086477046c"


def k(value: bytes) -> bytes:
    digest = keccak.new(digest_bits=256)
    digest.update(value)
    return digest.digest()


SIGNER_SET_DOMAIN = k(b"6529networkmuseum.release-attestor-signer-set.v1")


def hx(value: str) -> bytes:
    return bytes.fromhex(value.removeprefix("0x"))


def policy_hash(policy: dict) -> str:
    return "0x" + k(rfc8785.dumps(policy)).hex()


def signer_set_hash(policy: dict) -> str:
    words = [
        SIGNER_SET_DOMAIN,
        hx(policy_hash(policy)),
        uint_word(policy["threshold"]),
        uint_word(len(policy["addresses"])),
    ]
    words.extend(address_word(hx(address)) for address in policy["addresses"])
    return "0x" + k(static_words(*words)).hex()


def load_and_validate_policy() -> dict:
    schema = json.loads(POLICY_SCHEMA_PATH.read_text(encoding="utf-8"))
    policy = json.loads(POLICY_PATH.read_text(encoding="utf-8"))
    assert "0x" + k(rfc8785.dumps(schema)).hex() == EXPECTED_SCHEMA_HASH
    jsonschema.validate(policy, schema)
    addresses = policy["addresses"]
    assert addresses == sorted(addresses)
    assert len(addresses) == 3 and len(set(addresses)) == 3
    assert policy["threshold"] == 2
    assert policy["policyScope"] == "NON_DEPLOYMENT_CONFORMANCE_FIXTURE"
    assert policy["authoritySource"] == {
        "kind": "governance-approved-deployment-manifest",
        "policyHashBinding": "immutable-constructor",
        "signerSetHashBinding": "immutable-constructor",
        "rotationRule": "new-registry-deployment",
    }
    assert policy_hash(policy) == EXPECTED_POLICY_HASH
    assert signer_set_hash(policy) == EXPECTED_SIGNER_SET_HASH
    return policy


def main() -> int:
    policy = load_and_validate_policy()
    substituted = copy.deepcopy(policy)
    substituted["addresses"] = [
        "0x1000000000000000000000000000000000000001",
        "0x2000000000000000000000000000000000000002",
        "0x3000000000000000000000000000000000000003",
    ]
    assert policy_hash(substituted) != policy_hash(policy)
    assert signer_set_hash(substituted) != signer_set_hash(policy)
    print(f"releaseAttestorPolicyHash={policy_hash(policy)}")
    print(f"releaseAttestorSignerSetHash={signer_set_hash(policy)}")
    print("governedSignerSet=2/3 keySubstitution=REJECT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
