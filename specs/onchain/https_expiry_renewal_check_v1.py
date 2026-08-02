"""Executable V1 HTTPS expiry, renewal, and non-retroactivity fixture."""

from __future__ import annotations

from dataclasses import dataclass

from Crypto.Hash import keccak

from abi_encoding_v1 import address_word, static_words, uint_word


if not __debug__:
    raise SystemExit("optimized Python disables conformance checks")


def k(value: bytes) -> bytes:
    digest = keccak.new(digest_bits=256)
    digest.update(value)
    return digest.digest()


def hx(value: str) -> bytes:
    return bytes.fromhex(value.removeprefix("0x"))


DOMAIN = hx("0x4fcfa708a5b354629d48cb2b96432841b5566b13b7c8f30468d34106b0f7904a")
URI_HASH = k(b"https://example.com/archive/6529")
HOST_HASH = k(b"example.com")
PROFILE = hx("0x52be64fd2fb1c3795cf8dd6472100377858fd563f16de75584dcaf0f74b3e186")
ADDRESS_SET_HASH = hx("0x17971e83b91ac972b51bdefb4cab3445a46319fc90d6bc5894819de59fbf03a9")
ATTESTOR = hx("000000000000000000000000000000000000dead")
ZERO = bytes(32)


def assertion_hash(revision: int, previous: bytes, issued: int, expires: int, nonce: int, deadline: int) -> bytes:
    return k(static_words(
        DOMAIN, URI_HASH, HOST_HASH, PROFILE, uint_word(1), ADDRESS_SET_HASH,
        uint_word(revision), previous, uint_word(issued), uint_word(expires),
        address_word(ATTESTOR), uint_word(nonce), uint_word(deadline),
    ))


OLD = assertion_hash(1, ZERO, 1_750_000_000, 1_750_003_600, 9, 1_750_003_600)
RENEWED = assertion_hash(2, OLD, 1_750_003_601, 1_750_007_200, 10, 1_750_007_200)


@dataclass(frozen=True)
class Assertion:
    digest: bytes
    revision: int
    previous: bytes
    issued: int
    expires: int


class RegistryModel:
    """The V1 write/read rule exercised by this lifecycle vector."""

    def __init__(self, current: Assertion) -> None:
        self.current = current
        self.records: dict[str, bytes] = {}

    def write_https_record(self, record_id: str, now: int) -> None:
        if not self.current.issued <= now <= self.current.expires:
            raise PermissionError("current HTTPS assertion is expired")
        self.records[record_id] = self.current.digest

    def renew(self, successor: Assertion) -> None:
        if successor.revision != self.current.revision + 1 or successor.previous != self.current.digest:
            raise ValueError("renewal does not extend the current assertion")
        self.current = successor

    def read(self, record_id: str) -> bytes:
        return self.records[record_id]


def main() -> int:
    old = Assertion(OLD, 1, ZERO, 1_750_000_000, 1_750_003_600)
    renewed = Assertion(RENEWED, 2, OLD, 1_750_003_601, 1_750_007_200)
    registry = RegistryModel(old)

    registry.write_https_record("record-1", 1_750_003_600)
    try:
        registry.write_https_record("record-expired", 1_750_003_601)
    except PermissionError:
        pass
    else:
        raise AssertionError("expired current assertion admitted a new write")
    assert registry.read("record-1") == OLD  # expiry does not erase old state

    registry.renew(renewed)
    registry.write_https_record("record-2", 1_750_003_601)
    assert registry.read("record-2") == RENEWED
    assert registry.read("record-1") == OLD  # renewal is not retroactive
    assert old.issued <= 1_750_003_600 <= old.expires
    assert not old.issued <= 1_750_003_601 <= old.expires

    print(f"oldAssertionHash=0x{OLD.hex()}")
    print(f"renewedAssertionHash=0x{RENEWED.hex()}")
    print("expiredWrite=REJECT")
    print("renewedWrite=ACCEPT")
    print("historicalRecord=READABLE")
    print("oldValidityAfterRenewal=NOT_RETROACTIVE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
