"""Check the V1 pre-write batch-gas eligibility envelope offline.

The calculation is a deterministic caller-reserve gate, not a measured or
claimed execution-gas bound. Deployment measurement remains a separately
governed report threshold in the corpus.
"""

from __future__ import annotations

import json
from pathlib import Path

import rfc8785
from Crypto.Hash import keccak


ROOT = Path(__file__).resolve().parent
CORPUS_PATH = ROOT / "batch-gas-benchmark-v1.json"
EXPECTED_CORPUS_HASH = "458a9637f7acda5ea92f1a082c3211a716083d6198c050c587d65d67f58bfb50"


def k(value: bytes) -> bytes:
    digest = keccak.new(digest_bits=256)
    digest.update(value)
    return digest.digest()


def required_gas(count: int, inline_bytes: int) -> int:
    return 250_000 + 120_000 * count + 16 * inline_bytes


def main() -> int:
    corpus = json.loads(CORPUS_PATH.read_text(encoding="utf-8"))
    assert k(rfc8785.dumps(corpus)).hex() == EXPECTED_CORPUS_HASH
    constants = corpus["constants"]
    acceptance = corpus["acceptance"]
    assert constants == {
        "maxBatchRecords": 64,
        "maxInlinePayloadBytes": 16_384,
        "maxBatchInlinePayloadBytes": 262_144,
        "maxBatchGasUnits": 13_000_000,
        "callerReserveGas": 50_000,
        "measuredDeploymentGasUnits": 9_000_000,
    }
    assert acceptance["measuredGasMustBeAtMost"] == constants["measuredDeploymentGasUnits"]
    assert acceptance["measuredGasPlusCallerReserveMustBeAtMost"] == 9_050_000
    assert acceptance["measuredGasPlusCallerReserveMustBeAtMost"] == (
        constants["measuredDeploymentGasUnits"] + constants["callerReserveGas"]
    )
    calculated = {case["id"]: required_gas(case["count"], case["inlineBytes"]) for case in corpus["corpus"]}
    assert all(case["count"] <= constants["maxBatchRecords"] for case in corpus["corpus"])
    assert all(case["inlineBytes"] <= constants["maxBatchInlinePayloadBytes"] for case in corpus["corpus"])
    assert all(value <= constants["maxBatchGasUnits"] for value in calculated.values())
    worst = calculated["https-supersession-max"]
    assert worst == 12_124_304
    assert worst + constants["callerReserveGas"] == 12_174_304
    assert worst + constants["callerReserveGas"] <= constants["maxBatchGasUnits"]
    assert constants["measuredDeploymentGasUnits"] < worst
    print(f"worstCase=https-supersession-max requiredGas={worst}")
    print(f"callerReserveGas={constants['callerReserveGas']} eligibilityGas={worst + constants['callerReserveGas']}")
    print(f"maxBatchGasUnits={constants['maxBatchGasUnits']} measuredDeploymentGasUnits={constants['measuredDeploymentGasUnits']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
