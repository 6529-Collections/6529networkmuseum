"""Recompute the normative one-record MUSEUM_BATCH_VECTOR_V1 fixture."""

from __future__ import annotations

from Crypto.Hash import keccak

from abi_encoding_v1 import bytes32_arrays, uint_word


if not __debug__:
    raise SystemExit("optimized Python disables conformance checks")


def keccak256(value: bytes) -> bytes:
    digest = keccak.new(digest_bits=256)
    digest.update(value)
    return digest.digest()


def hx(value: str) -> bytes:
    return bytes.fromhex(value.removeprefix("0x"))


BATCH_ID_LITERAL = b"MUSEUM_BATCH_VECTOR_V1"
BATCH_DOMAIN = keccak256(b"6529networkmuseum.batch-commitment.v1")
BATCH_ID = keccak256(BATCH_ID_LITERAL)
RECORD_HASH = hx("0x217e7a966879dd7c379772be42f35fe353b45c113cec0ac76c21dd068bd506d1")
PREVIOUS_HASH = bytes(32)
PAYLOAD_HASH = hx("0x3f29b41d9d595ee7c116a4905fd8f4faf620b5757037db8a8988cd87b9c972a7")


def main() -> int:
    assert BATCH_ID.hex() == "a4713265f6f293e83885203722026053a888831af3f829e81b6aaed0d5d1d70b"
    commitment = keccak256(bytes32_arrays(
        [BATCH_DOMAIN, BATCH_ID, uint_word(1)],
        [[RECORD_HASH], [PREVIOUS_HASH], [PAYLOAD_HASH]],
        [uint_word(1)],
    ))
    assert commitment.hex() == "1c1c8c0c0c71816b08183589eaca344e6cd6b0ba1bc784c2d5a84337c377fc8d"
    print(f"batchId=0x{BATCH_ID.hex()}")
    print(f"batchCommitment=0x{commitment.hex()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
