#!/usr/bin/env python3
"""Acquire exact finalized custody evidence for *Themes and Variations* #210.

The transport, receipt/log verification, EIP-1898 block-hash reads and raw
byte retention are inherited from the reviewed Magnum single-chain evidence
acquisition.  This wrapper supplies the Vera Molnár object identity and emits
an accession-specific summary.  It proves the observed chain state only.
"""

from __future__ import annotations

from datetime import UTC, datetime
import json
from pathlib import Path
import sys

import acquire_magnum_custody_evidence as custody


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "evidence" / "vera-molnar-210-custody"
ACCESSION_ID = "6529NM.2026.003"
OBJECT_ID = "6529NM.2026.003.01"
PROPOSAL_OBJECT_ID = "6529NM-PG-2026-002.OBJ-001"
CONTRACT = "0xe034bb2b1b9471e11cf1a0a9199a156fb227aa5d"
TOKEN_ID = 210
TRANSFER_TRANSACTION = (
    "0x618603d9f21dc09a4a7b2d6b6b242cc337127e8052116d0ee28c6c25f012a5cd"
)
TRANSFER_BLOCK = 25_816_958
TRANSFER_LOG_INDEX = 315


def configure() -> None:
    custody.OUTPUT = OUTPUT
    custody.USER_AGENT = "6529-Network-Museum/vera-molnar-210-custody-audit-v1"
    custody.CONTRACT = CONTRACT
    custody.MAX_TRANSFER_BLOCK = TRANSFER_BLOCK
    custody.TOKENS = (
        {
            "object_id": OBJECT_ID,
            "candidate_object_id": PROPOSAL_OBJECT_ID,
            "token_id": TOKEN_ID,
            "tx_hash": TRANSFER_TRANSACTION,
            "block_number": TRANSFER_BLOCK,
            "log_index": TRANSFER_LOG_INDEX,
        },
    )


def main() -> int:
    configure()
    try:
        observation = custody.run()
    except (custody.EvidenceError, OSError, ValueError) as exc:
        print(f"Vera Molnár custody evidence acquisition refused: {exc}")
        return 1

    observation["record_id"] = f"{ACCESSION_ID}.CUSTODY-EVIDENCE-01"
    observation["record_type"] = "VERA_MOLNAR_210_CUSTODY_OBSERVATION"
    observation["accession_id"] = ACCESSION_ID
    observation["proposal_id"] = "6529NM-PG-2026-002"
    observation["observed_at"] = (
        datetime.now(UTC).isoformat(timespec="milliseconds").replace("+00:00", "Z")
    )
    observation["limitations"] = [
        "This package proves the retained transfer receipt, Transfer log and exact-finalized-block custody state.",
        "It does not merge token custody with copyright, display rights, preservation rights or accession authority.",
        "The donor's full-gift offer, the adopted Wave decision and the Museum acceptance record supply separate authority evidence.",
    ]

    encoded = (
        json.dumps(observation, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")
    custody.write_bytes(OUTPUT / "summary.json", encoded)
    print(
        "Vera Molnár custody evidence acquired at finalized block "
        f"{observation['finalized_block']['number']}: {OUTPUT}"
    )
    print(
        json.dumps(
            {
                "summary_sha256": f"sha256:{custody.sha256(encoded)}",
                "object_count": len(observation["objects"]),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
