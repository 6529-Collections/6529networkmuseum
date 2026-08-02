"""Offline conformance model for inert deployment and initial activation V1.

This models the specification's state machine and commitment boundary.  It is
not contract bytecode, a deployment transaction, or deployment authorization.
"""

from __future__ import annotations

import copy
import re
from pathlib import Path

from Crypto.Hash import keccak

from abi_encoding_v1 import static_words


if not __debug__:
    raise SystemExit("optimized Python disables conformance checks")


ROOT = Path(__file__).resolve().parent
SPEC_PATH = ROOT / "contract-migration-v1.md"

INITIAL_AUTHORITY_ARTIFACT_DOMAIN_LITERAL = "6529networkmuseum.initial-authority-artifact.v1"
INITIAL_GOVERNANCE_EXECUTOR = "0x0000000000000000000000000000000000000652"
AUTHORITY_TARGET = "0x0000000000000000000000000000000000000042"
ZERO32 = bytes(32)

CONSTRUCTOR_FIELDS = {
    "initialGovernanceExecutor",
    "initialGovernanceExecutorEvidenceHash",
    "initialAuthorityArtifactCommitment",
    "releaseAttestorPolicyHash",
    "releaseAttestorSigner0",
    "releaseAttestorSigner1",
    "releaseAttestorSigner2",
    "streamCompatibilityCommit",
    "moduleSupersedes",
}

ADDRESS_BOUND_FORBIDDEN_CONSTRUCTOR_FIELDS = {
    "target",
    "releaseId",
    "conformanceDocumentHash",
    "signedDocumentHash",
    "releaseAttestationDigest",
    "releaseAttestorSignatures",
    "interfaceProbeHash",
    "capabilityCommitment",
}


class Rejected(Exception):
    """Closed-gate rejection in the state model."""


def k(value: bytes) -> bytes:
    digest = keccak.new(digest_bits=256)
    digest.update(value)
    return digest.digest()


def hx(value: str) -> bytes:
    return bytes.fromhex(value.removeprefix("0x"))


def bytes4_word(value: str) -> bytes:
    decoded = hx(value)
    if len(decoded) != 4:
        raise ValueError("bytes4")
    return decoded + bytes(28)


def initial_authority_artifact_commitment(release: dict[str, str]) -> str:
    words = (
        k(INITIAL_AUTHORITY_ARTIFACT_DOMAIN_LITERAL.encode("ascii")),
        hx(release["runtimePolicyHash"]),
        hx(release["sourceCommit"]),
        hx(release["sourceTreeHash"]),
        hx(release["artifactHash"]),
        bytes4_word(release["requiredInterfaceId"]),
        hx(release["expectedModuleVersion"]),
        hx(release["protocolVersion"]),
        hx(release["streamCompatibilityCommit"]),
        hx(release["previousReleaseId"]),
        hx(release["supersessionReasonHash"]),
    )
    return "0x" + k(static_words(*words)).hex()


def require_active(state: dict) -> None:
    if state["initializationState"] != 2:
        raise Rejected("NOT_ACTIVE")


def activate(
    state: dict,
    *,
    caller: str,
    release: dict[str, str],
    signatures_valid: bool = True,
    fail_after_staging: bool = False,
    exercise_reentrancy: bool = False,
) -> None:
    before = copy.deepcopy(state)
    try:
        if caller != state["initialGovernanceExecutor"]:
            raise Rejected("WRONG_EXECUTOR")
        if state["initializationState"] != 0:
            raise Rejected("ALREADY_INITIALIZED")
        if state["authority"] is not None or state["authorityRevision"] != 0:
            raise Rejected("DIRTY_INITIAL_STATE")
        state["initializationState"] = 1

        if exercise_reentrancy:
            try:
                require_active(state)
            except Rejected as error:
                if str(error) != "NOT_ACTIVE":
                    raise
            else:
                raise AssertionError("initializing state admitted a mutator")

        if initial_authority_artifact_commitment(release) != state["artifactCommitment"]:
            raise Rejected("ARTIFACT_COMMITMENT")
        if release["targetKind"] != "1" or release["target"] != AUTHORITY_TARGET:
            raise Rejected("AUTHORITY_TARGET")
        if not signatures_valid:
            raise Rejected("RELEASE_SIGNATURES")

        state["admittedReleaseId"] = release["releaseId"]
        state["authority"] = release["target"]
        state["authorityRevision"] = 1
        state["governanceExecutorCapabilityCommitment"] = release["capabilityCommitment"]
        if fail_after_staging:
            raise Rejected("INJECTED_POST_STAGE_FAILURE")
        state["initializationState"] = 2
    except Exception:
        state.clear()
        state.update(before)
        raise


def expect_rejected(action, expected: str) -> None:
    try:
        action()
    except Rejected as error:
        assert str(error) == expected, (str(error), expected)
    else:
        raise AssertionError(f"expected {expected}")


def validate_documentation() -> None:
    spec = SPEC_PATH.read_text(encoding="utf-8")
    for literal in (
        INITIAL_AUTHORITY_ARTIFACT_DOMAIN_LITERAL,
        "initialization state `0` (`UNINITIALIZED`)",
        "state `1` (`INITIALIZING`)",
        "state `2` (`ACTIVE`)",
        "signature-free, target-address-free init code",
        "activateInitialAuthority(TargetReleaseInput,TransitionTargetInput)",
    ):
        assert literal in spec, literal
    assert re.search(r"every other mutator\s+reject states `0` and `1`", spec)


def main() -> int:
    assert not (CONSTRUCTOR_FIELDS & ADDRESS_BOUND_FORBIDDEN_CONSTRUCTOR_FIELDS)

    release = {
        "targetKind": "1",
        "target": AUTHORITY_TARGET,
        "releaseId": "0x" + "44" * 32,
        "runtimePolicyHash": "0x95f9e52ebbfec6aa2d1ad41a516a6d9e7ce2f55cfed9de1fb906e6f6e9dae452",
        "sourceCommit": "0x000000000000000000000000ff1c5825e3b61bfb2df0a639e057297beb946e4d",
        "sourceTreeHash": "0x0000000000000000000000001111111111111111111111111111111111111111",
        "artifactHash": "0x" + "22" * 32,
        "requiredInterfaceId": "0xea450898",
        "expectedModuleVersion": "0x" + "00" * 32,
        "protocolVersion": "0x" + "00" * 32,
        "streamCompatibilityCommit": "0x" + "00" * 32,
        "previousReleaseId": "0x" + "00" * 32,
        "supersessionReasonHash": "0x" + "00" * 32,
        "capabilityCommitment": "0x" + "55" * 32,
    }
    commitment = initial_authority_artifact_commitment(release)
    state = {
        "initializationState": 0,
        "initialGovernanceExecutor": INITIAL_GOVERNANCE_EXECUTOR,
        "artifactCommitment": commitment,
        "authority": None,
        "authorityRevision": 0,
        "admittedReleaseId": None,
        "governanceExecutorCapabilityCommitment": None,
    }
    pristine = copy.deepcopy(state)

    expect_rejected(lambda: require_active(state), "NOT_ACTIVE")
    expect_rejected(
        lambda: activate(state, caller="0x0000000000000000000000000000000000000001", release=release),
        "WRONG_EXECUTOR",
    )
    assert state == pristine

    changed = copy.deepcopy(release)
    changed["artifactHash"] = "0x" + "23" * 32
    expect_rejected(
        lambda: activate(state, caller=INITIAL_GOVERNANCE_EXECUTOR, release=changed),
        "ARTIFACT_COMMITMENT",
    )
    assert state == pristine

    expect_rejected(
        lambda: activate(
            state,
            caller=INITIAL_GOVERNANCE_EXECUTOR,
            release=release,
            signatures_valid=False,
        ),
        "RELEASE_SIGNATURES",
    )
    assert state == pristine

    expect_rejected(
        lambda: activate(
            state,
            caller=INITIAL_GOVERNANCE_EXECUTOR,
            release=release,
            fail_after_staging=True,
        ),
        "INJECTED_POST_STAGE_FAILURE",
    )
    assert state == pristine

    activate(
        state,
        caller=INITIAL_GOVERNANCE_EXECUTOR,
        release=release,
        exercise_reentrancy=True,
    )
    require_active(state)
    assert state["authority"] == AUTHORITY_TARGET
    assert state["authorityRevision"] == 1
    assert state["admittedReleaseId"] == release["releaseId"]
    assert state["governanceExecutorCapabilityCommitment"] == release["capabilityCommitment"]
    active = copy.deepcopy(state)
    expect_rejected(
        lambda: activate(state, caller=INITIAL_GOVERNANCE_EXECUTOR, release=release),
        "ALREADY_INITIALIZED",
    )
    assert state == active

    validate_documentation()
    print(f"initialAuthorityArtifactCommitment={commitment}")
    print("constructorAddressBoundFields=0 initialization=0->1->2 rollback=ATOMIC replay=REJECT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
