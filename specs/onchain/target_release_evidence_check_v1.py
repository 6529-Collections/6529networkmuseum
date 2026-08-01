"""Reproduce the non-deployment TargetRelease evidence vector offline.

The fixture is deliberately public and synthetic.  It exercises the complete
schema and the acyclic releaseId -> D0 -> D1 -> signatures/bundle derivation;
it neither names deployed code nor authorizes a release, admission, or write.
"""

from __future__ import annotations

import argparse
import base64
import copy
import json
from pathlib import Path

import jsonschema
import rfc8785

from abi_encoding_v1 import address_word, static_words, uint_word
from target_release_signature_bundle_check_v1 import G, N, cidv1_raw_sha256, k, point_multiply, recover_address


ROOT = Path(__file__).resolve().parent
EVIDENCE_PATH = ROOT / "target-release-evidence-v1.fixture.json"
BUNDLE_PATH = ROOT / "target-release-signature-bundle-v1.fixture.json"
REFERENCE_PATH = ROOT / "target-release-signature-bundle-v1.reference.json"
EVIDENCE_SCHEMA_PATH = ROOT / "target-release-evidence-v1.schema.json"
BUNDLE_SCHEMA_PATH = ROOT / "target-release-signature-bundle-v1.schema.json"
CANONICALIZER_POLICY_PATH = ROOT / "canonicalizer-runtime-purity-v1.json"
TARGET_POLICY_PATH = ROOT / "target-runtime-nonupgradeability-v1.json"

ZERO_HASH = "0x" + "00" * 32
RELEASE_ID_DOMAIN = k(b"6529networkmuseum.target-release-id.v1")
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


def address_for_scalar(scalar: int) -> str:
    point = point_multiply(scalar, G)
    assert point is not None
    return "0x" + k(point[0].to_bytes(32, "big") + point[1].to_bytes(32, "big"))[-20:].hex()


def fixture_scalar(label: bytes) -> int:
    scalar = int.from_bytes(k(label), "big") % N
    assert scalar != 0
    return scalar


def sign_document(scalar: int, document_hash: bytes) -> bytes:
    """Create a public, deterministic ECDSA vector signature (not a secret)."""
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


def dependency_hash(dependencies: list[dict[str, str]]) -> str:
    return h(rfc8785.dumps(dependencies))


def release_id(evidence: dict) -> str:
    return h(static_words(
        RELEASE_ID_DOMAIN,
        uint_word(evidence["targetKind"]),
        address_word(hx(evidence["target"])),
        hx(evidence["codeHash"]),
        hx(evidence["runtimePolicyHash"]),
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
    value["signers"]["signatureCommitments"] = [ZERO_HASH, ZERO_HASH, ZERO_HASH]
    return value


def build_expected() -> tuple[dict, dict, dict]:
    target_policy_hash = policy_hash(TARGET_POLICY_PATH)
    dependencies = [{
        "address": "0x0000000000000000000000000000000000005afe",
        "codeHash": h(b"MUSEUM_NON_DEPLOYMENT_SAFE_ERC1271_RUNTIME_V1"),
        "interfaceId": "0x1626ba7e",
        "purpose": "erc1271-safe-validation",
    }]
    code_hash = h(b"MUSEUM_NON_DEPLOYMENT_AUTHORITY_RUNTIME_V1")
    scalars = tuple(fixture_scalar(label) for label in FIXTURE_SCALAR_LABELS)
    signer_pairs = sorted((address_for_scalar(scalar), scalar) for scalar in scalars)
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
        "sourceTreeHash": h(b"MUSEUM_NON_DEPLOYMENT_TARGET_RELEASE_SOURCE_TREE_V1"),
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
        "signers": {"threshold": 2, "signatureScheme": "EIP-191-KECCAK256-DOCUMENT_V1", "signedDocumentHash": ZERO_HASH, "addresses": [address for address, _ in signer_pairs], "signatureCommitments": [ZERO_HASH, ZERO_HASH, ZERO_HASH]},
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
    for address, scalar in signer_pairs:
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
    assert evidence["runtimePolicyHash"] == policy_hash(TARGET_POLICY_PATH)
    assert evidence["conformance"]["runtimePolicyHash"] == evidence["runtimePolicyHash"]
    assert evidence["externalDependencyHash"] == dependency_hash(evidence["externalDependencies"])
    assert evidence["releaseId"] == release_id(evidence)
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
    assert bundle["releaseId"] == evidence["releaseId"]
    assert bundle["signedDocumentHash"] == evidence["signers"]["signedDocumentHash"]
    assert [entry["signer"] for entry in bundle["entries"]] == addresses
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


def assert_rejected(mutated: dict, expected_reason: str) -> None:
    evidence, bundle, reference = build_expected()
    try:
        validate_semantics(mutated, bundle, reference)
    except (AssertionError, jsonschema.ValidationError):
        return
    raise AssertionError(expected_reason)


def negative_checks(evidence: dict) -> None:
    mutation = copy.deepcopy(evidence)
    mutation["target"] = "0x0000000000000000000000000000000000000043"
    assert_rejected(mutation, "target-address substitution accepted")
    mutation = copy.deepcopy(evidence)
    mutation["runtimePolicyHash"] = "0x" + "11" * 32
    assert_rejected(mutation, "runtime-policy substitution accepted")
    mutation = copy.deepcopy(evidence)
    mutation["codeHash"] = "0x" + "22" * 32
    assert_rejected(mutation, "code-hash substitution accepted")
    mutation = copy.deepcopy(evidence)
    mutation["signers"]["threshold"] = 1
    assert_rejected(mutation, "undersized signer threshold accepted")
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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit", action="store_true", help="print the deterministic fixture objects")
    arguments = parser.parse_args()
    expected_evidence, expected_bundle, expected_reference = build_expected()
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
    negative_checks(evidence)
    print(f"releaseId={evidence['releaseId']}")
    print(f"conformanceDocumentHash={evidence['conformanceDocumentHash']}")
    print(f"signedDocumentHash={evidence['signers']['signedDocumentHash']}")
    print(f"target={evidence['target']} runtimePolicyHash={evidence['runtimePolicyHash']}")
    print(f"detachedBundleHash={reference['contentHash']} signatureRecovery=3/3")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
