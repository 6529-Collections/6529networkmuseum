"""Small, dependency-free ABI encoders used by the V1 conformance vectors.

The functions intentionally support only the fixed-width values and bytes32
arrays exercised by the published fixtures. A production ABI implementation
must use a complete audited encoder instead.
"""

from __future__ import annotations


def uint_word(value: int) -> bytes:
    if not 0 <= value < 1 << 256:
        raise ValueError("uint value outside ABI word range")
    return value.to_bytes(32, "big")


def address_word(value: bytes) -> bytes:
    if len(value) != 20:
        raise ValueError("address must be exactly 20 bytes")
    return bytes(12) + value


def static_words(*values: bytes) -> bytes:
    if any(len(value) != 32 for value in values):
        raise ValueError("static ABI values must be exactly 32 bytes")
    return b"".join(values)


def bytes32_arrays(prefix: list[bytes], arrays: list[list[bytes]], suffix: list[bytes]) -> bytes:
    """Encode `prefix, bytes32[]..., suffix` using ordinary `abi.encode`."""
    if any(len(value) != 32 for value in [*prefix, *suffix]):
        raise ValueError("static ABI values must be exactly 32 bytes")
    if any(len(value) != 32 for array in arrays for value in array):
        raise ValueError("bytes32 arrays may contain only 32-byte values")

    head_words = len(prefix) + len(arrays) + len(suffix)
    offset = head_words * 32
    encoded_arrays: list[bytes] = []
    offsets: list[bytes] = []
    for array in arrays:
        encoded = uint_word(len(array)) + b"".join(array)
        offsets.append(uint_word(offset))
        encoded_arrays.append(encoded)
        offset += len(encoded)
    return static_words(*prefix, *offsets, *suffix) + b"".join(encoded_arrays)
