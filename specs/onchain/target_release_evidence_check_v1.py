"""Reproduce the non-deployment TargetRelease evidence vector offline.

The fixture is deliberately public and synthetic.  It exercises the complete
schema and the acyclic releaseId -> D0 -> D1 -> signatures/bundle derivation;
it neither names deployed code nor authorizes a release, admission, or write.
"""

from __future__ import annotations

import argparse
import base64
import copy
import hashlib
import json
from pathlib import Path

import jsonschema
import rfc8785

from abi_encoding_v1 import address_word, bytes32_arrays, static_words, uint_word
from release_attestor_policy_check_v1 import (
    load_and_validate_policy,
    policy_hash as release_attestor_policy_hash,
    signer_set_hash as release_attestor_signer_set_hash,
)
from target_release_signature_bundle_check_v1 import G, N, cidv1_raw_sha256, k, point_multiply, recover_address
from uri_safety_vectors_v1 import AR_TX, CID_V1, valid_uri


if not __debug__:
    raise SystemExit("optimized Python disables conformance checks")


ROOT = Path(__file__).resolve().parent
EVIDENCE_PATH = ROOT / "target-release-evidence-v1.fixture.json"
BUNDLE_PATH = ROOT / "target-release-signature-bundle-v1.fixture.json"
REFERENCE_PATH = ROOT / "target-release-signature-bundle-v1.reference.json"
EVIDENCE_SCHEMA_PATH = ROOT / "target-release-evidence-v1.schema.json"
BUNDLE_SCHEMA_PATH = ROOT / "target-release-signature-bundle-v1.schema.json"
CANONICALIZER_POLICY_PATH = ROOT / "canonicalizer-runtime-purity-v1.json"
TARGET_POLICY_PATH = ROOT / "target-runtime-nonupgradeability-v1.json"
DEPENDENCY_POLICY_PATH = ROOT / "dependency-runtime-nonproxy-v1.json"

ZERO_HASH = "0x" + "00" * 32
RELEASE_ID_DOMAIN = k(b"6529networkmuseum.target-release-id.v1")
DEPENDENCY_ROW_DOMAIN = k(b"6529networkmuseum.target-dependency-row.v1")
DEPENDENCY_SET_DOMAIN = k(b"6529networkmuseum.target-dependency-set.v1")
FIXTURE_SCALAR_LABELS = (
    b"MUSEUM_NON_DEPLOYMENT_TARGET_RELEASE_FIXTURE_SIGNER_A_V1",
    b"MUSEUM_NON_DEPLOYMENT_TARGET_RELEASE_FIXTURE_SIGNER_B_V1",
    b"MUSEUM_NON_DEPLOYMENT_TARGET_RELEASE_FIXTURE_SIGNER_C_V1",
)


def hx(value: str) -> bytes:
    return bytes.fromhex(value.removeprefix("0x"))


def h(value: bytes) -> str:
    return "0x" + k(value).hex()


def commit_word(value: str) -> bytes:
    """Encode an evidence SHA-1 as the right-aligned ABI bytes32 value."""
    raw = hx(value)
    if len(raw) != 20:
        raise ValueError("commit evidence must be exactly 20 bytes")
    return bytes(12) + raw


def tree_word(value: str) -> str:
    """Encode a 40-hex SHA-1 tree OID as the normative right-aligned bytes32."""
    if len(value) != 40 or any(character not in "0123456789abcdef" for character in value):
        raise ValueError("tree evidence must be exactly 40 lowercase hex characters")
    return "0x" + "00" * 12 + value


def address_for_scalar(scalar: int) -> str:
    point = point_multiply(scalar, G)
    assert point is not None
    return "0x" + k(point[0].to_bytes(32, "big") + point[1].to_bytes(32, "big"))[-20:].hex()


def fixture_scalar(label: bytes) -> int:
    scalar = int.from_bytes(k(label), "big") % N
    assert scalar != 0
    return scalar


def sign_document(scalar: int, document_hash: bytes) -> bytes:
    """Create a fixture-only signature with public scalars.

    This deliberately compact routine is non-RFC6979 and unaudited. It MUST
    never be reused with a real-secret scalar or outside this conformance
    fixture.
    """
    nonce = int.from_bytes(k(b"MUSEUM_TARGET_RELEASE_FIXTURE_NONCE_V1" + scalar.to_bytes(32, "big") + document_hash), "big") % N
    assert nonce != 0
    point = point_multiply(nonce, G)
    assert point is not None
    r = point[0] % N
    assert r != 0
    s = (pow(nonce, -1, N) * (int.from_bytes(document_hash, "big") + r * scalar)) % N
    assert s != 0
    recovery_id = point[1] & 1
    if s > N // 2:
        s = N - s
        recovery_id ^= 1
    return r.to_bytes(32, "big") + s.to_bytes(32, "big") + bytes([recovery_id])


def ar_uri(label: bytes) -> str:
    return "ar://" + base64.urlsafe_b64encode(k(label)).decode("ascii").rstrip("=")


def policy_hash(path: Path) -> str:
    return h(rfc8785.dumps(json.loads(path.read_text(encoding="utf-8"))))


def dependency_sort_key(dependency: dict[str, str]) -> tuple[int, bytes, bytes, bytes, bytes]:
    return (
        int(dependency["address"], 16),
        hx(dependency["codeHash"]),
        hx(dependency["runtimePolicyHash"]),
        hx(dependency["interfaceId"]),
        hx(dependency["purposeId"]),
    )


def dependency_row_hash(dependency: dict[str, str]) -> bytes:
    return k(static_words(
        DEPENDENCY_ROW_DOMAIN,
        address_word(hx(dependency["address"])),
        hx(dependency["codeHash"]),
        hx(dependency["runtimePolicyHash"]),
        hx(dependency["interfaceId"]) + bytes(28),
        hx(dependency["purposeId"]),
    ))


def dependency_hash(dependencies: list[dict[str, str]]) -> str:
    row_hashes = [dependency_row_hash(dependency) for dependency in dependencies]
    return h(bytes32_arrays([DEPENDENCY_SET_DOMAIN], [row_hashes], []))


def validate_dependencies(dependencies: list[dict[str, str]]) -> None:
    assert len(dependencies) <= 8
    keys = [dependency_sort_key(dependency) for dependency in dependencies]
    assert keys == sorted(keys) and len(set(keys)) == len(keys)
    for dependency in dependencies:
        assert dependency["address"] != "0x" + "00" * 20
        assert dependency["codeHash"] != ZERO_HASH
        assert dependency["runtimePolicyHash"] != ZERO_HASH
        assert dependency["interfaceId"] not in {"0x00000000", "0xffffffff"}
        assert dependency["purposeId"] == h(dependency["purpose"].encode("ascii"))


def validate_uri_semantics(evidence: dict, reference: dict) -> None:
    uri_rows = [reference["uri"]]
    uri_rows.extend(row["uri"] for row in reference["availability"])
    uri_rows.extend(row["uri"] for row in evidence["availability"])
    for uri in uri_rows:
        assert valid_uri(uri), uri


def release_id(evidence: dict) -> str:
    return h(static_words(
        RELEASE_ID_DOMAIN,
        uint_word(evidence["targetKind"]),
        address_word(hx(evidence["target"])),
        hx(evidence["codeHash"]),
        hx(evidence["runtimePolicyHash"]),
        hx(evidence["signers"]["policyHash"]),
        hx(evidence["signers"]["signerSetHash"]),
        hx(evidence["externalDependencyHash"]),
        commit_word("0x" + evidence["sourceCommit"]),
        hx(evidence["sourceTreeHash"]),
        hx(evidence["artifactHash"]),
        hx(evidence["requiredInterfaceId"]) + bytes(28),
        hx(evidence["expectedModuleVersion"]),
        hx(evidence["protocolVersion"]),
        hx(evidence["streamCompatibilityCommit"]),
        uint_word(evidence["revision"]),
        hx(evidence["previousReleaseId"]),
        hx(evidence["supersessionReasonHash"]),
    ))


def validate_release_lineage(evidence: dict, current: dict | None = None) -> None:
    if current is None:
        assert evidence["revision"] == 1
        assert evidence["previousReleaseId"] == ZERO_HASH
        assert evidence["supersessionReasonHash"] == ZERO_HASH
        return
    assert evidence["revision"] == current["revision"] + 1
    assert evidence["previousReleaseId"] == current["releaseId"]
    assert evidence["supersessionReasonHash"] != ZERO_HASH


def projection(evidence: dict, stage: str) -> dict:
    if stage not in {"D0", "D1"}:
        raise ValueError("unknown projection stage")
    value = copy.deepcopy(evidence)
    del value["availability"]
    del value["detachedSignatureBundle"]
    value["conformanceDocumentHash"] = ZERO_HASH if stage == "D0" else evidence["conformanceDocumentHash"]
    value["signers"]["signedDocumentHash"] = ZERO_HASH
    value["signers"]["signatureCommitments"] = [ZERO_HASH] * value["signers"]["threshold"]
    return value


def build_expected() -> tuple[dict, dict, dict]:
    target_policy_hash = policy_hash(TARGET_POLICY_PATH)
    dependency_policy_hash = policy_hash(DEPENDENCY_POLICY_PATH)
    attestor_policy = load_and_validate_policy()
    attestor_policy_hash = release_attestor_policy_hash(attestor_policy)
    attestor_signer_set_hash = release_attestor_signer_set_hash(attestor_policy)
    dependency_purpose = "immutable-erc165-policy-source"
    dependencies = [{
        "address": "0x000000000000000000000000000000000000d3e1",
        "codeHash": h(b"MUSEUM_NON_DEPLOYMENT_IMMUTABLE_ERC165_DEPENDENCY_V1"),
        "runtimePolicyHash": dependency_policy_hash,
        "interfaceId": "0x01ffc9a7",
        "purposeId": h(dependency_purpose.encode("ascii")),
        "purpose": dependency_purpose,
    }]
    code_hash = h(b"MUSEUM_NON_DEPLOYMENT_AUTHORITY_RUNTIME_V1")
    scalars = tuple(fixture_scalar(label) for label in FIXTURE_SCALAR_LABELS)
    signer_pairs = sorted((address_for_scalar(scalar), scalar) for scalar in scalars)
    assert [address for address, _ in signer_pairs] == attestor_policy["addresses"]
    evidence = {
        "schema": "MUSEUM_TARGET_RELEASE_EVIDENCE_V1",
        "version": 1,
        "evidenceScope": "NON_DEPLOYMENT_CONFORMANCE_FIXTURE",
        "targetKind": 1,
        "releaseId": ZERO_HASH,
        "target": "0x0000000000000000000000000000000000000042",
        "codeHash": code_hash,
        "runtimePolicyId": "MUSEUM_TARGET_RUNTIME_NONUPGRADEABILITY_V1",
        "runtimePolicyHash": target_policy_hash,
        "externalDependencyHash": dependency_hash(dependencies),
        "sourceCommit": "0123456789abcdef0123456789abcdef01234567",
        "sourceRepository": "6529-Collections/6529networkmuseum",
        "sourceTreeHash": tree_word(hashlib.sha1(b"MUSEUM_NON_DEPLOYMENT_TARGET_RELEASE_SOURCE_TREE_V1").hexdigest()),
        "artifactHash": code_hash,
        "requiredInterfaceId": "0xea450898",
        "expectedModuleVersion": ZERO_HASH,
        "protocolVersion": ZERO_HASH,
        "streamCompatibilityCommit": ZERO_HASH,
        "conformanceDocumentHash": ZERO_HASH,
        "revision": 1,
        "authorityRevision": 1,
        "status": 1,
        "builds": [
            {"builderId": "0x0000000000000000000000000000000000000101", "toolchainId": "synthetic-solc-0.8.19-builder-a", "compilerInputHash": h(b"MUSEUM_NON_DEPLOYMENT_COMPILER_INPUT_V1"), "artifactHash": code_hash, "runtimeCodeHash": code_hash},
            {"builderId": "0x0000000000000000000000000000000000000102", "toolchainId": "synthetic-solc-0.8.19-builder-b", "compilerInputHash": h(b"MUSEUM_NON_DEPLOYMENT_COMPILER_INPUT_V1"), "artifactHash": code_hash, "runtimeCodeHash": code_hash},
        ],
        "conformance": {"reportHash": h(b"MUSEUM_NON_DEPLOYMENT_TARGET_PROBE_REPORT_V1"), "vectorBundleHash": h(b"MUSEUM_NON_DEPLOYMENT_TARGET_PROBE_VECTORS_V1"), "runtimePolicyHash": target_policy_hash, "probeGasLimit": 250000, "returnDataBytesLimit": 4096},
        "externalDependencies": dependencies,
        "signers": {
            "policyId": attestor_policy["policyId"],
            "policyHash": attestor_policy_hash,
            "signerSetHash": attestor_signer_set_hash,
            "threshold": attestor_policy["threshold"],
            "signatureScheme": attestor_policy["signatureScheme"],
            "signedDocumentHash": ZERO_HASH,
            "addresses": attestor_policy["addresses"],
            "signatureCommitments": [ZERO_HASH, ZERO_HASH],
        },
        "detachedSignatureBundle": {},
        "availability": [],
        "previousReleaseId": ZERO_HASH,
        "supersessionReasonHash": ZERO_HASH,
    }
    evidence["releaseId"] = release_id(evidence)
    evidence["conformanceDocumentHash"] = h(rfc8785.dumps(projection(evidence, "D0")))
    evidence["signers"]["signedDocumentHash"] = h(rfc8785.dumps(projection(evidence, "D1")))
    digest = k(b"\x19Ethereum Signed Message:\n32" + hx(evidence["signers"]["signedDocumentHash"]))
    entries = []
    for address, scalar in signer_pairs[:evidence["signers"]["threshold"]]:
        signature = sign_document(scalar, digest)
        assert recover_address(digest, signature) == address
        entries.append({"signer": address, "signature": "0x" + signature.hex(), "signatureCommitment": h(signature)})
    evidence["signers"]["signatureCommitments"] = [entry["signatureCommitment"] for entry in entries]
    bundle = {"schema": "MUSEUM_TARGET_RELEASE_SIGNATURE_BUNDLE_V1", "version": 1, "releaseId": evidence["releaseId"], "signedDocumentHash": evidence["signers"]["signedDocumentHash"], "entries": entries}
    bundle_bytes = rfc8785.dumps(bundle)
    bundle_hash = h(bundle_bytes)
    bundle_uri = cidv1_raw_sha256(bundle_bytes)
    reference = {
        "schema": "MUSEUM_TARGET_RELEASE_SIGNATURE_BUNDLE_V1",
        "schemaHash": policy_hash(BUNDLE_SCHEMA_PATH),
        "version": 1,
        "uri": bundle_uri,
        "contentHash": bundle_hash,
        "mediaType": "application/json",
        "sizeBytes": len(bundle_bytes),
        "availability": [
            {"uri": bundle_uri, "contentHash": bundle_hash, "fetchObservationHash": h(b"MUSEUM_NON_DEPLOYMENT_BUNDLE_IPFS_OBSERVATION_V1" + bundle_bytes)},
            {"uri": ar_uri(b"MUSEUM_NON_DEPLOYMENT_BUNDLE_ARWEAVE_V1"), "contentHash": bundle_hash, "fetchObservationHash": h(b"MUSEUM_NON_DEPLOYMENT_BUNDLE_AR_OBSERVATION_V1" + bundle_bytes)},
        ],
    }
    d0_bytes = rfc8785.dumps(projection(evidence, "D0"))
    evidence["availability"] = [
        {"uri": cidv1_raw_sha256(d0_bytes), "contentHash": evidence["conformanceDocumentHash"], "fetchObservationHash": h(b"MUSEUM_NON_DEPLOYMENT_EVIDENCE_IPFS_OBSERVATION_V1" + d0_bytes)},
        {"uri": ar_uri(b"MUSEUM_NON_DEPLOYMENT_EVIDENCE_ARWEAVE_V1"), "contentHash": evidence["conformanceDocumentHash"], "fetchObservationHash": h(b"MUSEUM_NON_DEPLOYMENT_EVIDENCE_AR_OBSERVATION_V1" + d0_bytes)},
    ]
    evidence["detachedSignatureBundle"] = reference
    return evidence, bundle, reference


def validate_semantics(evidence: dict, bundle: dict, reference: dict) -> None:
    evidence_schema = json.loads(EVIDENCE_SCHEMA_PATH.read_text(encoding="utf-8"))
    bundle_schema = json.loads(BUNDLE_SCHEMA_PATH.read_text(encoding="utf-8"))
    jsonschema.validate(evidence, evidence_schema)
    jsonschema.validate(bundle, bundle_schema)
    jsonschema.validate(reference, evidence_schema["properties"]["detachedSignatureBundle"])
    assert evidence["target"] != "0x" + "00" * 20
    attestor_policy = load_and_validate_policy()
    assert evidence["signers"]["policyId"] == attestor_policy["policyId"]
    assert evidence["signers"]["policyHash"] == release_attestor_policy_hash(attestor_policy)
    assert evidence["signers"]["signerSetHash"] == release_attestor_signer_set_hash(attestor_policy)
    assert evidence["signers"]["threshold"] == attestor_policy["threshold"]
    assert evidence["signers"]["signatureScheme"] == attestor_policy["signatureScheme"]
    assert evidence["signers"]["addresses"] == attestor_policy["addresses"]
    assert evidence["runtimePolicyHash"] == policy_hash(TARGET_POLICY_PATH)
    assert evidence["conformance"]["runtimePolicyHash"] == evidence["runtimePolicyHash"]
    validate_dependencies(evidence["externalDependencies"])
    assert all(dependency["runtimePolicyHash"] == policy_hash(DEPENDENCY_POLICY_PATH) for dependency in evidence["externalDependencies"])
    assert evidence["externalDependencyHash"] == dependency_hash(evidence["externalDependencies"])
    assert evidence["releaseId"] == release_id(evidence)
    assert hx(evidence["sourceTreeHash"])[:12] == bytes(12)
    assert hx(evidence["sourceTreeHash"])[12:] != bytes(20)
    assert len(evidence["builds"]) == 2
    assert len({row["builderId"] for row in evidence["builds"]}) == 2
    assert len({row["toolchainId"] for row in evidence["builds"]}) == 2
    assert {row["artifactHash"] for row in evidence["builds"]} == {evidence["artifactHash"], evidence["codeHash"]}
    assert {row["runtimeCodeHash"] for row in evidence["builds"]} == {evidence["codeHash"]}
    validate_release_lineage(evidence)
    assert evidence["conformanceDocumentHash"] == h(rfc8785.dumps(projection(evidence, "D0")))
    assert evidence["signers"]["signedDocumentHash"] == h(rfc8785.dumps(projection(evidence, "D1")))
    addresses = evidence["signers"]["addresses"]
    assert len(addresses) == 3 and addresses == sorted(addresses) and len(set(addresses)) == 3
    assert evidence["signers"]["threshold"] == 2
    assert len(evidence["signers"]["signatureCommitments"]) == evidence["signers"]["threshold"]
    assert bundle["releaseId"] == evidence["releaseId"]
    assert bundle["signedDocumentHash"] == evidence["signers"]["signedDocumentHash"]
    bundle_signers = [entry["signer"] for entry in bundle["entries"]]
    assert len(bundle_signers) == evidence["signers"]["threshold"]
    assert bundle_signers == sorted(bundle_signers) and len(set(bundle_signers)) == len(bundle_signers)
    assert set(bundle_signers).issubset(addresses)
    assert [entry["signatureCommitment"] for entry in bundle["entries"]] == evidence["signers"]["signatureCommitments"]
    digest = k(b"\x19Ethereum Signed Message:\n32" + hx(evidence["signers"]["signedDocumentHash"]))
    for entry in bundle["entries"]:
        signature = hx(entry["signature"])
        assert h(signature) == entry["signatureCommitment"]
        assert recover_address(digest, signature) == entry["signer"]
    canonical_bundle = rfc8785.dumps(bundle)
    assert reference == evidence["detachedSignatureBundle"]
    assert reference["contentHash"] == h(canonical_bundle)
    assert reference["sizeBytes"] == len(canonical_bundle)
    assert reference["uri"] == cidv1_raw_sha256(canonical_bundle)
    assert len({row["uri"] for row in reference["availability"]}) == 2
    assert all(row["contentHash"] == reference["contentHash"] for row in reference["availability"])
    assert len({row["uri"] for row in evidence["availability"]}) == 2
    assert all(row["contentHash"] == evidence["conformanceDocumentHash"] for row in evidence["availability"])
    validate_uri_semantics(evidence, reference)


class EvidenceRejection(ValueError):
    def __init__(self, code: str):
        super().__init__(code)
        self.code = code


def validate_mutation(mutated: dict, pristine: dict, bundle: dict, reference: dict) -> None:
    if mutated["target"] != pristine["target"]:
        raise EvidenceRejection("TARGET_ADDRESS")
    if mutated["runtimePolicyHash"] != policy_hash(TARGET_POLICY_PATH):
        raise EvidenceRejection("TARGET_RUNTIME_POLICY")
    if mutated["codeHash"] != pristine["codeHash"]:
        raise EvidenceRejection("TARGET_CODE_HASH")
    for dependency in mutated["externalDependencies"]:
        if dependency["purposeId"] != h(dependency["purpose"].encode("ascii")):
            raise EvidenceRejection("DEPENDENCY_PURPOSE")
        if dependency["runtimePolicyHash"] != policy_hash(DEPENDENCY_POLICY_PATH):
            raise EvidenceRejection("DEPENDENCY_RUNTIME_POLICY")
    if mutated["externalDependencyHash"] != dependency_hash(mutated["externalDependencies"]):
        raise EvidenceRejection("DEPENDENCY_SET_HASH")
    if not mutated["sourceTreeHash"].startswith("0x" + "00" * 12):
        raise EvidenceRejection("SOURCE_TREE_ENCODING")
    if mutated["signers"]["threshold"] != 2:
        raise EvidenceRejection("SIGNER_THRESHOLD")
    attestor_policy = load_and_validate_policy()
    if (
        mutated["signers"]["policyId"] != attestor_policy["policyId"]
        or mutated["signers"]["policyHash"] != release_attestor_policy_hash(attestor_policy)
        or mutated["signers"]["signerSetHash"] != release_attestor_signer_set_hash(attestor_policy)
        or mutated["signers"]["addresses"] != attestor_policy["addresses"]
    ):
        raise EvidenceRejection("RELEASE_ATTESTOR_POLICY")
    try:
        validate_semantics(mutated, bundle, reference)
    except (AssertionError, jsonschema.ValidationError) as error:
        raise EvidenceRejection("UNCLASSIFIED_SEMANTIC_FAILURE") from error


def assert_rejected(mutated: dict, pristine: dict, bundle: dict, reference: dict, expected_code: str) -> None:
    try:
        validate_mutation(mutated, pristine, bundle, reference)
    except EvidenceRejection as error:
        assert error.code == expected_code, (error.code, expected_code)
        return
    raise AssertionError(f"mutation accepted: {expected_code}")


def self_selected_rekey_attack(evidence: dict) -> tuple[dict, dict, dict]:
    """Build the formerly accepted all-new-keys attack as a coherent artifact."""
    attack = copy.deepcopy(evidence)
    attack_policy = copy.deepcopy(load_and_validate_policy())
    attack_scalars = tuple(
        fixture_scalar(label)
        for label in (
            b"MUSEUM_TARGET_RELEASE_ATTACKER_SIGNER_A_V1",
            b"MUSEUM_TARGET_RELEASE_ATTACKER_SIGNER_B_V1",
            b"MUSEUM_TARGET_RELEASE_ATTACKER_SIGNER_C_V1",
        )
    )
    signer_pairs = sorted((address_for_scalar(scalar), scalar) for scalar in attack_scalars)
    attack_policy["addresses"] = [address for address, _ in signer_pairs]
    attack["signers"]["addresses"] = attack_policy["addresses"]
    attack["signers"]["policyHash"] = release_attestor_policy_hash(attack_policy)
    attack["signers"]["signerSetHash"] = release_attestor_signer_set_hash(attack_policy)
    attack["signers"]["signatureCommitments"] = [ZERO_HASH, ZERO_HASH]
    attack["signers"]["signedDocumentHash"] = ZERO_HASH
    attack["conformanceDocumentHash"] = ZERO_HASH
    attack["availability"] = []
    attack["detachedSignatureBundle"] = {}
    attack["releaseId"] = release_id(attack)
    attack["conformanceDocumentHash"] = h(rfc8785.dumps(projection(attack, "D0")))
    attack["signers"]["signedDocumentHash"] = h(rfc8785.dumps(projection(attack, "D1")))
    digest = k(b"\x19Ethereum Signed Message:\n32" + hx(attack["signers"]["signedDocumentHash"]))
    entries = []
    for address, scalar in signer_pairs[:2]:
        signature = sign_document(scalar, digest)
        entries.append({"signer": address, "signature": "0x" + signature.hex(), "signatureCommitment": h(signature)})
    attack["signers"]["signatureCommitments"] = [entry["signatureCommitment"] for entry in entries]
    bundle = {
        "schema": "MUSEUM_TARGET_RELEASE_SIGNATURE_BUNDLE_V1",
        "version": 1,
        "releaseId": attack["releaseId"],
        "signedDocumentHash": attack["signers"]["signedDocumentHash"],
        "entries": entries,
    }
    bundle_bytes = rfc8785.dumps(bundle)
    bundle_hash = h(bundle_bytes)
    bundle_uri = cidv1_raw_sha256(bundle_bytes)
    reference = {
        "schema": "MUSEUM_TARGET_RELEASE_SIGNATURE_BUNDLE_V1",
        "schemaHash": policy_hash(BUNDLE_SCHEMA_PATH),
        "version": 1,
        "uri": bundle_uri,
        "contentHash": bundle_hash,
        "mediaType": "application/json",
        "sizeBytes": len(bundle_bytes),
        "availability": [
            {"uri": bundle_uri, "contentHash": bundle_hash, "fetchObservationHash": h(b"MUSEUM_ATTACK_BUNDLE_IPFS_V1" + bundle_bytes)},
            {"uri": ar_uri(b"MUSEUM_ATTACK_BUNDLE_AR_V1"), "contentHash": bundle_hash, "fetchObservationHash": h(b"MUSEUM_ATTACK_BUNDLE_AR_V1" + bundle_bytes)},
        ],
    }
    d0_bytes = rfc8785.dumps(projection(attack, "D0"))
    attack["availability"] = [
        {"uri": cidv1_raw_sha256(d0_bytes), "contentHash": attack["conformanceDocumentHash"], "fetchObservationHash": h(b"MUSEUM_ATTACK_EVIDENCE_IPFS_V1" + d0_bytes)},
        {"uri": ar_uri(b"MUSEUM_ATTACK_EVIDENCE_AR_V1"), "contentHash": attack["conformanceDocumentHash"], "fetchObservationHash": h(b"MUSEUM_ATTACK_EVIDENCE_AR_V1" + d0_bytes)},
    ]
    attack["detachedSignatureBundle"] = reference
    return attack, bundle, reference


def negative_checks(evidence: dict, bundle: dict, reference: dict) -> None:
    mutation = copy.deepcopy(evidence)
    mutation["target"] = "0x0000000000000000000000000000000000000043"
    assert_rejected(mutation, evidence, bundle, reference, "TARGET_ADDRESS")
    mutation = copy.deepcopy(evidence)
    mutation["runtimePolicyHash"] = "0x" + "11" * 32
    assert_rejected(mutation, evidence, bundle, reference, "TARGET_RUNTIME_POLICY")
    mutation = copy.deepcopy(evidence)
    mutation["codeHash"] = "0x" + "22" * 32
    assert_rejected(mutation, evidence, bundle, reference, "TARGET_CODE_HASH")
    mutation = copy.deepcopy(evidence)
    mutation["externalDependencies"][0]["purposeId"] = "0x" + "33" * 32
    assert_rejected(mutation, evidence, bundle, reference, "DEPENDENCY_PURPOSE")
    mutation = copy.deepcopy(evidence)
    mutation["externalDependencies"][0]["runtimePolicyHash"] = "0x" + "55" * 32
    assert_rejected(mutation, evidence, bundle, reference, "DEPENDENCY_RUNTIME_POLICY")
    mutation = copy.deepcopy(evidence)
    mutation["externalDependencyHash"] = "0x" + "44" * 32
    assert_rejected(mutation, evidence, bundle, reference, "DEPENDENCY_SET_HASH")
    mutation = copy.deepcopy(evidence)
    mutation["signers"]["threshold"] = 1
    assert_rejected(mutation, evidence, bundle, reference, "SIGNER_THRESHOLD")
    mutation = copy.deepcopy(evidence)
    mutation["signers"]["addresses"] = [
        "0x1000000000000000000000000000000000000001",
        "0x2000000000000000000000000000000000000002",
        "0x3000000000000000000000000000000000000003",
    ]
    assert_rejected(mutation, evidence, bundle, reference, "RELEASE_ATTESTOR_POLICY")
    mutation = copy.deepcopy(evidence)
    mutation["signers"]["policyHash"] = "0x" + "66" * 32
    assert_rejected(mutation, evidence, bundle, reference, "RELEASE_ATTESTOR_POLICY")
    mutation = copy.deepcopy(evidence)
    mutation["signers"]["signerSetHash"] = "0x" + "77" * 32
    assert_rejected(mutation, evidence, bundle, reference, "RELEASE_ATTESTOR_POLICY")
    attack, attack_bundle, attack_reference = self_selected_rekey_attack(evidence)
    assert attack["releaseId"] != evidence["releaseId"]
    assert_rejected(attack, evidence, attack_bundle, attack_reference, "RELEASE_ATTESTOR_POLICY")
    mutation = copy.deepcopy(evidence)
    tree_oid = mutation["sourceTreeHash"][26:]
    mutation["sourceTreeHash"] = "0x" + tree_oid + "00" * 12
    assert_rejected(mutation, evidence, bundle, reference, "SOURCE_TREE_ENCODING")
    correction = copy.deepcopy(evidence)
    correction["revision"] = 2
    correction["previousReleaseId"] = evidence["releaseId"]
    correction["supersessionReasonHash"] = h(b"MUSEUM_NON_DEPLOYMENT_CORRECTION_REASON_V1")
    correction["releaseId"] = release_id(correction)
    assert correction["releaseId"] != evidence["releaseId"]
    validate_release_lineage(correction, evidence)
    bad_correction = copy.deepcopy(correction)
    bad_correction["previousReleaseId"] = ZERO_HASH
    try:
        validate_release_lineage(bad_correction, evidence)
    except AssertionError:
        pass
    else:
        raise AssertionError("incorrect correction predecessor accepted")
    bad_correction = copy.deepcopy(correction)
    bad_correction["supersessionReasonHash"] = ZERO_HASH
    try:
        validate_release_lineage(bad_correction, evidence)
    except AssertionError:
        pass
    else:
        raise AssertionError("reasonless correction accepted")

    invalid_uris = {
        "malformed CIDv1": "ipfs://bafybad",
        "noncanonical CIDv1": f"ipfs://{CID_V1[:-1]}r",
        "malformed Arweave": "ar://short",
        "noncanonical Arweave": f"ar://{AR_TX[:-1]}B",
        "content-addressed port": f"ipfs://{CID_V1}:443",
        "content-addressed userinfo": f"ipfs://user@{CID_V1}",
        "Arweave path": f"ar://{AR_TX}/path",
        "uppercase HTTPS scheme": "HTTPS://example.com/x",
        "uppercase IPFS scheme": f"IPFS://{CID_V1}/path",
        "uppercase Arweave scheme": f"AR://{AR_TX}",
    }
    for label, uri in invalid_uris.items():
        if valid_uri(uri):
            raise AssertionError(f"{label} accepted: {uri}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit", action="store_true", help="print the deterministic fixture objects")
    parser.add_argument("--write", action="store_true", help="rewrite the three deterministic fixture files")
    arguments = parser.parse_args()
    expected_evidence, expected_bundle, expected_reference = build_expected()
    if arguments.write:
        for path, value in (
            (EVIDENCE_PATH, expected_evidence),
            (BUNDLE_PATH, expected_bundle),
            (REFERENCE_PATH, expected_reference),
        ):
            path.write_text(json.dumps(value, separators=(",", ":"), sort_keys=True) + "\n", encoding="utf-8", newline="\n")
        print("wrote deterministic TargetRelease fixtures")
        return 0
    if arguments.emit:
        for name, value in (("evidence", expected_evidence), ("bundle", expected_bundle), ("reference", expected_reference)):
            print(f"---{name}---")
            print(json.dumps(value, separators=(",", ":"), sort_keys=True))
        return 0
    evidence = json.loads(EVIDENCE_PATH.read_text(encoding="utf-8"))
    bundle = json.loads(BUNDLE_PATH.read_text(encoding="utf-8"))
    reference = json.loads(REFERENCE_PATH.read_text(encoding="utf-8"))
    assert evidence == expected_evidence
    assert bundle == expected_bundle
    assert reference == expected_reference
    validate_semantics(evidence, bundle, reference)
    negative_checks(evidence, bundle, reference)
    print(f"releaseId={evidence['releaseId']}")
    print(f"conformanceDocumentHash={evidence['conformanceDocumentHash']}")
    print(f"signedDocumentHash={evidence['signers']['signedDocumentHash']}")
    print(f"target={evidence['target']} runtimePolicyHash={evidence['runtimePolicyHash']}")
    print(f"externalDependencyHash={evidence['externalDependencyHash']} dependencies={len(evidence['externalDependencies'])}")
    print(f"releaseAttestorPolicyHash={evidence['signers']['policyHash']}")
    print(f"releaseAttestorSignerSetHash={evidence['signers']['signerSetHash']}")
    print(f"detachedBundleHash={reference['contentHash']} signatureRecovery=2/3")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
