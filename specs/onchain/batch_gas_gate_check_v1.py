"""Check the V1 pre-write batch-gas eligibility envelope offline.

The calculation is a deterministic caller-reserve gate, not a measured or
claimed execution-gas bound. Deployment measurement remains a separately
governed report threshold in the corpus.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import rfc8785
from Crypto.Hash import keccak


if not __debug__:
    raise SystemExit("optimized Python disables conformance checks")


ROOT = Path(__file__).resolve().parent
CORPUS_PATH = ROOT / "batch-gas-benchmark-v1.json"
SPEC_PATH = ROOT / "contract-migration-v1.md"
EXPECTED_CORPUS_HASH = "f69a816a38f9b0f1addd6f8270318d6c1aacf17cb55bfb2adcb7efbe5983b293"


def k(value: bytes) -> bytes:
    digest = keccak.new(digest_bits=256)
    digest.update(value)
    return digest.digest()


def required_gas(count: int, inline_bytes: int) -> int:
    return 250_000 + 120_000 * count + 16 * inline_bytes


def main() -> int:
    corpus = json.loads(CORPUS_PATH.read_text(encoding="utf-8"))
    spec = SPEC_PATH.read_text(encoding="utf-8")
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
    spec_constants = {
        "MAX_BATCH_RECORDS": constants["maxBatchRecords"],
        "MAX_INLINE_PAYLOAD_BYTES": constants["maxInlinePayloadBytes"],
        "MAX_BATCH_INLINE_PAYLOAD_BYTES": constants["maxBatchInlinePayloadBytes"],
        "MAX_BATCH_GAS_UNITS": constants["maxBatchGasUnits"],
        "BATCH_CALLER_RESERVE_GAS": constants["callerReserveGas"],
        "MEASURED_BATCH_GAS_THRESHOLD": constants["measuredDeploymentGasUnits"],
    }
    for literal, value in spec_constants.items():
        rendered = f"{value:,}".replace(",", "_")
        assert f"uint256 constant {literal} = {rendered};" in spec, literal
    assert re.search(
        r"requiredGas\s*=\s*250000\s*\+\s*120000\s*\*\s*inputs\.length\s*\+\s*16\s*\*\s*inlineBytes",
        spec,
    ), "MUSEUM_BATCH_GAS_GATE_V1 formula drift"
    assert acceptance["measuredGasMustBeAtMost"] == constants["measuredDeploymentGasUnits"]
    assert acceptance["measuredGasPlusCallerReserveMustBeAtMost"] == 9_050_000
    assert acceptance["measuredGasPlusCallerReserveMustBeAtMost"] == (
        constants["measuredDeploymentGasUnits"] + constants["callerReserveGas"]
    )
    calculated = {case["id"]: required_gas(case["count"], case["inlineBytes"]) for case in corpus["corpus"]}
    worst_case = next(case for case in corpus["corpus"] if case["id"] == "https-supersession-max")
    assert worst_case["recordModes"] == ["INLINE", "CONTENT_ADDRESSED"]
    assert worst_case["inlineRecordCount"] == 16
    assert worst_case["nonInlineRecordCount"] == 48
    assert worst_case["nonInlineRecordMode"] == "CONTENT_ADDRESSED"
    assert worst_case["inlineRecordCount"] + worst_case["nonInlineRecordCount"] == worst_case["count"]
    assert worst_case["httpsRecordCount"] == worst_case["count"]
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
    print("specConstantsBound=true specFormulaBound=true")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
