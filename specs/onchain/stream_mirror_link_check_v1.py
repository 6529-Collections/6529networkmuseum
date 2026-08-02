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
MUSEUM_EXTERNAL_SUBJECT_DOMAIN = bytes.fromhex(
    "1dd722ea239e47e25bdadfcc0053bdc4e7ee75e7ca9dd0afe97076a6d9eb8a80"
)
MUSEUM_ASSET_PROFILE_CAIP19_V1 = bytes.fromhex(
    "ac72cc7c2b027b8ee3d459de7829fd7b3b31cf575c28734e736ebd33b10f41cc"
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


def stream_subject_id(stream_core: str, token_id: int) -> str:
    return "0x" + k(static_words(
        STREAM_SUBJECT_TOKEN_V1,
        uint_word(CHAIN_ID),
        address_word(bytes.fromhex(stream_core.removeprefix("0x"))),
        uint_word(token_id),
    )).hex()


def canonical_stream_asset_id(stream_core: str, token_id: int) -> str:
    return f"eip155:{CHAIN_ID}/erc721:{stream_core.lower()}/{token_id}"


def museum_subject_id(canonical_asset_id: str) -> str:
    return "0x" + k(static_words(
        MUSEUM_EXTERNAL_SUBJECT_DOMAIN,
        MUSEUM_ASSET_PROFILE_CAIP19_V1,
        k(canonical_asset_id.encode("ascii")),
    )).hex()


OWNER_RECORD_HASH = "0x" + k(b"MUSEUM_STREAM_OWNER_RECORD_READBACK_FIXTURE_V1").hex()


class MirrorRejection(ValueError):
    pass


def validate_link(
    admission: dict,
    external_asset: dict,
    museum_subject: str,
    readback: dict,
    expected_owner_record_hash: str,
    token_id: int = TOKEN_ID,
) -> dict:
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
    if readback["coreReturnDataBytes"] != 128:
        raise MirrorRejection("CORE_RETURN_DATA_LENGTH")
    if not readback["coreMappingExists"] or readback["coreCollectionId"] == 0:
        raise MirrorRejection("TOKEN_COLLECTION_IDENTITY")
    if readback["coreCollectionSerial"] == 0:
        raise MirrorRejection("TOKEN_COLLECTION_SERIAL")
    if readback["coreBurned"]:
        raise MirrorRejection("TOKEN_BURNED")
    if readback["returnDataBytes"] != 96:
        raise MirrorRejection("RETURN_DATA_LENGTH")
    if readback["collectionId"] != readback["coreCollectionId"]:
        raise MirrorRejection("COLLECTION_ID")

    canonical_asset_id = canonical_stream_asset_id(admission["streamCore"], token_id)
    canonical_asset_hash = "0x" + k(canonical_asset_id.encode("ascii")).hex()
    derived_museum_subject = museum_subject_id(canonical_asset_id)
    if (
        external_asset["assetProfileId"] != "0x" + MUSEUM_ASSET_PROFILE_CAIP19_V1.hex()
        or external_asset["canonicalAssetId"] != canonical_asset_id
        or external_asset["canonicalAssetIdHash"] != canonical_asset_hash
        or external_asset["subjectId"] != derived_museum_subject
    ):
        raise MirrorRejection("MUSEUM_ASSET_IDENTITY")
    if museum_subject != derived_museum_subject:
        raise MirrorRejection("MUSEUM_SUBJECT")

    derived_subject = stream_subject_id(admission["streamCore"], token_id)
    if readback["streamSubjectId"] != derived_subject:
        raise MirrorRejection("STREAM_SUBJECT")
    if readback["ownerRecordHash"] == "0x" + "00" * 32:
        raise MirrorRejection("OWNER_RECORD_HASH_ZERO")
    if readback["ownerRecordHash"] != expected_owner_record_hash:
        raise MirrorRejection("EXPECTED_OWNER_RECORD_HASH")
    return {
        "streamCore": admission["streamCore"],
        "ownerRecordModule": admission["interfaceModule"],
        "collectionId": readback["collectionId"],
        "collectionSerial": readback["coreCollectionSerial"],
        "coreMappingExists": readback["coreMappingExists"],
        "coreBurned": readback["coreBurned"],
        "tokenId": token_id,
        "canonicalAssetId": canonical_asset_id,
        "canonicalAssetIdHash": canonical_asset_hash,
        "museumSubjectId": derived_museum_subject,
        "streamSubjectId": derived_subject,
        "ownerRecordHash": readback["ownerRecordHash"],
        "ownerRecordHashDomain": admission["ownerRecordHashDomain"],
        "ownerRecordHashVectorId": admission["ownerRecordHashVectorId"],
    }


def rejected(
    admission: dict,
    external_asset: dict,
    museum_subject: str,
    readback: dict,
    expected: str,
    code: str,
    token_id: int = TOKEN_ID,
) -> None:
    try:
        validate_link(
            admission, external_asset, museum_subject, readback, expected, token_id
        )
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
    canonical_asset_id = canonical_stream_asset_id(STREAM_CORE, TOKEN_ID)
    museum_subject = museum_subject_id(canonical_asset_id)
    external_asset = {
        "subjectId": museum_subject,
        "assetProfileId": "0x" + MUSEUM_ASSET_PROFILE_CAIP19_V1.hex(),
        "canonicalAssetId": canonical_asset_id,
        "canonicalAssetIdHash": "0x" + k(canonical_asset_id.encode("ascii")).hex(),
    }
    readback = {
        **admission,
        "collectionId": COLLECTION_ID,
        "streamSubjectId": stream_subject_id(STREAM_CORE, TOKEN_ID),
        "ownerRecordHash": OWNER_RECORD_HASH,
        "returnDataBytes": 96,
        "coreMappingExists": True,
        "coreCollectionId": COLLECTION_ID,
        "coreCollectionSerial": 713,
        "coreBurned": False,
        "coreReturnDataBytes": 128,
    }
    link = validate_link(
        admission, external_asset, museum_subject, readback, OWNER_RECORD_HASH
    )

    mutations = (
        ("streamCoreCodeHash", "0x" + "aa" * 32, "STREAM_CORE_RUNTIME"),
        ("interfaceModuleCodeHash", "0x" + "bb" * 32, "INTERFACE_MODULE_RUNTIME"),
        ("streamCore", "0x0000000000000000000000000000000000001002", "STREAM_CORE_READBACK"),
        ("ownerRecordHashDomain", "0x" + "cc" * 32, "OWNER_RECORD_DOMAIN"),
        ("ownerRecordHashVectorId", "0x" + "dd" * 32, "OWNER_RECORD_VECTOR"),
        ("coreReturnDataBytes", 96, "CORE_RETURN_DATA_LENGTH"),
        ("coreMappingExists", False, "TOKEN_COLLECTION_IDENTITY"),
        ("coreCollectionId", 0, "TOKEN_COLLECTION_IDENTITY"),
        ("coreCollectionId", COLLECTION_ID + 1, "COLLECTION_ID"),
        ("coreCollectionSerial", 0, "TOKEN_COLLECTION_SERIAL"),
        ("coreBurned", True, "TOKEN_BURNED"),
        ("returnDataBytes", 64, "RETURN_DATA_LENGTH"),
        ("streamSubjectId", "0x" + "ee" * 32, "STREAM_SUBJECT"),
        ("collectionId", COLLECTION_ID + 1, "COLLECTION_ID"),
        ("ownerRecordHash", "0x" + "00" * 32, "OWNER_RECORD_HASH_ZERO"),
    )
    for field, value, code in mutations:
        mutation = copy.deepcopy(readback)
        mutation[field] = value
        rejected(
            admission, external_asset, museum_subject, mutation,
            OWNER_RECORD_HASH, code,
        )
    for field, value in (
        ("assetProfileId", "0x" + "aa" * 32),
        ("canonicalAssetId", canonical_asset_id + "0"),
        ("canonicalAssetIdHash", "0x" + "bb" * 32),
        ("subjectId", "0x" + "cc" * 32),
    ):
        mutation = copy.deepcopy(external_asset)
        mutation[field] = value
        rejected(
            admission, mutation, museum_subject, readback,
            OWNER_RECORD_HASH, "MUSEUM_ASSET_IDENTITY",
        )
    rejected(
        admission, external_asset, "0x" + "dd" * 32, readback,
        OWNER_RECORD_HASH, "MUSEUM_SUBJECT",
    )
    rejected(
        admission, external_asset, museum_subject, readback,
        OWNER_RECORD_HASH, "MUSEUM_ASSET_IDENTITY", TOKEN_ID + 1,
    )
    rejected(
        admission, external_asset, museum_subject, readback,
        "0x" + "ff" * 32, "EXPECTED_OWNER_RECORD_HASH",
    )

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
        "collectionSerial": str(link["collectionSerial"]),
        "coreMappingExists": str(link["coreMappingExists"]).lower(),
        "coreBurned": str(link["coreBurned"]).lower(),
        "tokenId": str(link["tokenId"]),
        "tokenCollectionIdentitySelector": "0x" + k(b"tokenCollectionIdentity(uint256)")[:4].hex(),
        "canonicalAssetId": link["canonicalAssetId"],
        "canonicalAssetIdHash": link["canonicalAssetIdHash"],
        "museumSubjectId": link["museumSubjectId"],
        "streamSubjectId": link["streamSubjectId"],
        "ownerRecordHash": link["ownerRecordHash"],
        "ownerRecordHashDomain": link["ownerRecordHashDomain"],
        "ownerRecordHashVectorId": link["ownerRecordHashVectorId"],
        "swappedMuseumSubject": "REJECT",
        "substitutedNonzeroAdapterCollectionId": "REJECT",
        "substitutedMuseumAssetCoreModuleCollectionSubjectHashDomainVector": "REJECT",
    }
    assert values == expected

    print(f"streamCore={link['streamCore']} ownerRecordModule={link['ownerRecordModule']}")
    print(
        f"collectionId={link['collectionId']} collectionSerial={link['collectionSerial']} "
        f"tokenId={link['tokenId']}"
    )
    print(f"museumSubjectId={link['museumSubjectId']}")
    print(f"streamSubjectId={link['streamSubjectId']}")
    print(f"ownerRecordHash={link['ownerRecordHash']}")
    print("substitutedMuseumAssetCoreModuleCollectionSubjectHashDomainVector=REJECT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
