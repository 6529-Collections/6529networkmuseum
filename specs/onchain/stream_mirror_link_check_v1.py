"""Exercise the closed Stream owner-record mirror-link readback gate offline."""

from __future__ import annotations

import copy
import re
from pathlib import Path

from Crypto.Hash import keccak

from abi_encoding_v1 import address_word, static_words, uint_word


if not __debug__:
    raise SystemExit("optimized Python disables conformance checks")


SPEC_PATH = Path(__file__).resolve().parent / "contract-migration-v1.md"
CHAIN_ID = 1
STREAM_SUBJECT_TOKEN_V1 = bytes.fromhex(
    "1e576f27850d12bc1ec9255ca277dbecfbc84fb3a9a34c474640dfca89811d7e"
)
STREAM_CORE = "0x0000000000000000000000000000000000001001"
OWNER_RECORD_MODULE = "0x0000000000000000000000000000000000002002"
STREAM_CORE_CODE_HASH = "0x" + "11" * 32
OWNER_RECORD_MODULE_CODE_HASH = "0x" + "22" * 32
OWNER_RECORD_HASH_DOMAIN = "0x" + "33" * 32
OWNER_RECORD_HASH_VECTOR_ID = "0x" + "44" * 32
TOKEN_ID = 771769
COLLECTION_ID = 6529


def k(value: bytes) -> bytes:
    digest = keccak.new(digest_bits=256)
    digest.update(value)
    return digest.digest()


def subject_id(stream_core: str, token_id: int) -> str:
    return "0x" + k(static_words(
        STREAM_SUBJECT_TOKEN_V1,
        uint_word(CHAIN_ID),
        address_word(bytes.fromhex(stream_core.removeprefix("0x"))),
        uint_word(token_id),
    )).hex()


OWNER_RECORD_HASH = "0x" + k(b"MUSEUM_STREAM_OWNER_RECORD_READBACK_FIXTURE_V1").hex()


class MirrorRejection(ValueError):
    pass


def validate_link(admission: dict, readback: dict, expected_owner_record_hash: str) -> dict:
    if admission["streamCoreCodeHash"] != readback["streamCoreCodeHash"]:
        raise MirrorRejection("STREAM_CORE_RUNTIME")
    if admission["interfaceModuleCodeHash"] != readback["interfaceModuleCodeHash"]:
        raise MirrorRejection("INTERFACE_MODULE_RUNTIME")
    if admission["streamCore"] != readback["streamCore"]:
        raise MirrorRejection("STREAM_CORE_READBACK")
    if admission["ownerRecordHashDomain"] != readback["ownerRecordHashDomain"]:
        raise MirrorRejection("OWNER_RECORD_DOMAIN")
    if admission["ownerRecordHashVectorId"] != readback["ownerRecordHashVectorId"]:
        raise MirrorRejection("OWNER_RECORD_VECTOR")
    if readback["returnDataBytes"] != 96:
        raise MirrorRejection("RETURN_DATA_LENGTH")
    derived_subject = subject_id(admission["streamCore"], TOKEN_ID)
    if readback["streamSubjectId"] != derived_subject:
        raise MirrorRejection("STREAM_SUBJECT")
    if readback["collectionId"] == 0:
        raise MirrorRejection("COLLECTION_ID")
    if readback["ownerRecordHash"] == "0x" + "00" * 32:
        raise MirrorRejection("OWNER_RECORD_HASH_ZERO")
    if readback["ownerRecordHash"] != expected_owner_record_hash:
        raise MirrorRejection("EXPECTED_OWNER_RECORD_HASH")
    return {
        "streamCore": admission["streamCore"],
        "ownerRecordModule": admission["interfaceModule"],
        "collectionId": readback["collectionId"],
        "tokenId": TOKEN_ID,
        "streamSubjectId": derived_subject,
        "ownerRecordHash": readback["ownerRecordHash"],
        "ownerRecordHashDomain": admission["ownerRecordHashDomain"],
        "ownerRecordHashVectorId": admission["ownerRecordHashVectorId"],
    }


def rejected(admission: dict, readback: dict, expected: str, code: str) -> None:
    try:
        validate_link(admission, readback, expected)
    except MirrorRejection as error:
        assert str(error) == code, (str(error), code)
        return
    raise AssertionError(f"mirror mutation accepted: {code}")


def main() -> int:
    admission = {
        "streamCore": STREAM_CORE,
        "streamCoreCodeHash": STREAM_CORE_CODE_HASH,
        "interfaceModule": OWNER_RECORD_MODULE,
        "interfaceModuleCodeHash": OWNER_RECORD_MODULE_CODE_HASH,
        "ownerRecordHashDomain": OWNER_RECORD_HASH_DOMAIN,
        "ownerRecordHashVectorId": OWNER_RECORD_HASH_VECTOR_ID,
    }
    readback = {
        **admission,
        "collectionId": COLLECTION_ID,
        "streamSubjectId": subject_id(STREAM_CORE, TOKEN_ID),
        "ownerRecordHash": OWNER_RECORD_HASH,
        "returnDataBytes": 96,
    }
    link = validate_link(admission, readback, OWNER_RECORD_HASH)

    mutations = (
        ("streamCoreCodeHash", "0x" + "aa" * 32, "STREAM_CORE_RUNTIME"),
        ("interfaceModuleCodeHash", "0x" + "bb" * 32, "INTERFACE_MODULE_RUNTIME"),
        ("streamCore", "0x0000000000000000000000000000000000001002", "STREAM_CORE_READBACK"),
        ("ownerRecordHashDomain", "0x" + "cc" * 32, "OWNER_RECORD_DOMAIN"),
        ("ownerRecordHashVectorId", "0x" + "dd" * 32, "OWNER_RECORD_VECTOR"),
        ("returnDataBytes", 64, "RETURN_DATA_LENGTH"),
        ("streamSubjectId", "0x" + "ee" * 32, "STREAM_SUBJECT"),
        ("collectionId", 0, "COLLECTION_ID"),
        ("ownerRecordHash", "0x" + "00" * 32, "OWNER_RECORD_HASH_ZERO"),
    )
    for field, value, code in mutations:
        mutation = copy.deepcopy(readback)
        mutation[field] = value
        rejected(admission, mutation, OWNER_RECORD_HASH, code)
    rejected(admission, readback, "0x" + "ff" * 32, "EXPECTED_OWNER_RECORD_HASH")

    spec = SPEC_PATH.read_text(encoding="utf-8")
    match = re.search(
        r"<!-- STREAM_MIRROR_LINK_VECTOR_V1_BEGIN -->\s*```text\s*(.*?)\s*```\s*"
        r"<!-- STREAM_MIRROR_LINK_VECTOR_V1_END -->",
        spec,
        re.DOTALL,
    )
    assert match is not None
    values = dict(
        line.split(" = ", 1)
        for line in match.group(1).splitlines()
        if " = " in line
    )
    expected = {
        "streamCore": link["streamCore"],
        "ownerRecordModule": link["ownerRecordModule"],
        "collectionId": str(link["collectionId"]),
        "tokenId": str(link["tokenId"]),
        "streamSubjectId": link["streamSubjectId"],
        "ownerRecordHash": link["ownerRecordHash"],
        "ownerRecordHashDomain": link["ownerRecordHashDomain"],
        "ownerRecordHashVectorId": link["ownerRecordHashVectorId"],
        "substitutedCoreModuleCollectionSubjectHashDomainVector": "REJECT",
    }
    assert values == expected

    print(f"streamCore={link['streamCore']} ownerRecordModule={link['ownerRecordModule']}")
    print(f"collectionId={link['collectionId']} tokenId={link['tokenId']}")
    print(f"streamSubjectId={link['streamSubjectId']}")
    print(f"ownerRecordHash={link['ownerRecordHash']}")
    print("substitutedCoreModuleCollectionSubjectHashDomainVector=REJECT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
