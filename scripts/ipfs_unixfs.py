#!/usr/bin/env python3
"""Stdlib-only IPFS CIDv0 recomputation and dag-pb/UnixFS block reading.

``cidv0_for_file`` reproduces the CIDv0 that go-ipfs/kubo ``ipfs add``
assigns by default: fixed 262,144-byte chunks, a balanced DAG with at most 174
links per node, UnixFS ``File`` leaves wrapped in dag-pb (no raw leaves) and a
sha2-256 multihash rendered in base58btc.  A CIDv0 is the hash of the root
dag-pb block, not of the file bytes, so equality with a token's IPFS hash is a
content binding only when it is recomputed this way.

``read_dag_pb`` parses one dag-pb block and ``hamt_index`` returns the
HAMT shard index that go-unixfs uses for a directory entry name (murmur3
x64-128, first 64 bits, read big-endian), so a sharded-directory path can be
followed and checked block by block.  Nothing here performs network access.
"""

from __future__ import annotations

import hashlib
from typing import Any


CHUNK_SIZE = 262_144
MAX_LINKS = 174
BASE58_ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"


class IpfsBlockError(ValueError):
    """Raised when a block or CID is malformed or does not verify."""


def b58encode(data: bytes) -> str:
    number = int.from_bytes(data, "big")
    encoded = ""
    while number:
        number, remainder = divmod(number, 58)
        encoded = BASE58_ALPHABET[remainder] + encoded
    return "1" * (len(data) - len(data.lstrip(b"\x00"))) + encoded


def b58decode(text: str) -> bytes:
    number = 0
    for char in text:
        index = BASE58_ALPHABET.find(char)
        if index < 0:
            raise IpfsBlockError("CID is not base58btc")
        number = number * 58 + index
    body = number.to_bytes((number.bit_length() + 7) // 8, "big") if number else b""
    return b"\x00" * (len(text) - len(text.lstrip("1"))) + body


def _varint(value: int) -> bytes:
    out = bytearray()
    while True:
        byte = value & 0x7F
        value >>= 7
        if value:
            out.append(byte | 0x80)
        else:
            out.append(byte)
            return bytes(out)


def _read_varint(data: bytes, cursor: int) -> tuple[int, int]:
    shift = 0
    value = 0
    while True:
        if cursor >= len(data) or shift > 63:
            raise IpfsBlockError("truncated or oversized varint")
        byte = data[cursor]
        cursor += 1
        value |= (byte & 0x7F) << shift
        shift += 7
        if not byte & 0x80:
            return value, cursor


def _field_bytes(number: int, data: bytes) -> bytes:
    return _varint((number << 3) | 2) + _varint(len(data)) + data


def _field_varint(number: int, value: int) -> bytes:
    return _varint(number << 3) + _varint(value)


def _unixfs_file(data: bytes | None, filesize: int, blocksizes: list[int]) -> bytes:
    out = _field_varint(1, 2)
    if data is not None:
        out += _field_bytes(2, data)
    out += _field_varint(3, filesize)
    for size in blocksizes:
        out += _field_varint(4, size)
    return out


def _pb_node(links: list[bytes], data: bytes) -> bytes:
    return b"".join(_field_bytes(2, link) for link in links) + _field_bytes(1, data)


def _pb_link(multihash: bytes, tsize: int) -> bytes:
    return _field_bytes(1, multihash) + _field_bytes(2, b"") + _field_varint(3, tsize)


def sha256_multihash(block: bytes) -> bytes:
    return b"\x12\x20" + hashlib.sha256(block).digest()


def cidv0_of_block(block: bytes) -> str:
    return b58encode(sha256_multihash(block))


def multihash_of_cidv0(cid: str) -> bytes:
    raw = b58decode(cid)
    if len(raw) != 34 or raw[:2] != b"\x12\x20":
        raise IpfsBlockError(f"not a sha2-256 CIDv0: {cid}")
    return raw


def verify_block(cid: str, block: bytes) -> None:
    if sha256_multihash(block) != multihash_of_cidv0(cid):
        raise IpfsBlockError(f"block bytes do not hash to {cid}")


def cidv0_for_file(payload: bytes, chunk_size: int = CHUNK_SIZE, max_links: int = MAX_LINKS) -> dict[str, Any]:
    """Recompute the default ``ipfs add`` CIDv0 for ``payload``."""

    chunks = [payload[index : index + chunk_size] for index in range(0, len(payload), chunk_size)] or [b""]
    level: list[tuple[bytes, int, int]] = []
    for chunk in chunks:
        block = _pb_node([], _unixfs_file(chunk, len(chunk), []))
        level.append((sha256_multihash(block), len(block), len(chunk)))
    depth = 0
    while len(level) > 1:
        parents: list[tuple[bytes, int, int]] = []
        for index in range(0, len(level), max_links):
            group = level[index : index + max_links]
            data = _unixfs_file(None, sum(item[2] for item in group), [item[2] for item in group])
            block = _pb_node([_pb_link(item[0], item[1]) for item in group], data)
            parents.append((sha256_multihash(block), len(block) + sum(item[1] for item in group), sum(item[2] for item in group)))
        level = parents
        depth += 1
    root, cumulative, filesize = level[0]
    return {
        "cid": b58encode(root),
        "chunker": f"size-{chunk_size}",
        "max_links_per_node": max_links,
        "leaf_format": "dag-pb UnixFS File (no raw leaves)",
        "hash": "sha2-256",
        "cid_version": 0,
        "chunk_count": len(chunks),
        "dag_depth": depth,
        "filesize": filesize,
        "dag_cumulative_size": cumulative,
        "last_chunk_bytes": len(chunks[-1]),
    }


def _protobuf_fields(data: bytes) -> list[tuple[int, int | bytes]]:
    fields: list[tuple[int, int | bytes]] = []
    cursor = 0
    while cursor < len(data):
        key, cursor = _read_varint(data, cursor)
        number, wire_type = key >> 3, key & 0x07
        if wire_type == 0:
            value, cursor = _read_varint(data, cursor)
            fields.append((number, value))
        elif wire_type == 2:
            length, cursor = _read_varint(data, cursor)
            if cursor + length > len(data):
                raise IpfsBlockError("truncated protobuf field")
            fields.append((number, data[cursor : cursor + length]))
            cursor += length
        else:
            raise IpfsBlockError(f"unsupported protobuf wire type {wire_type}")
    return fields


def read_dag_pb(block: bytes) -> dict[str, Any]:
    """Return the links and UnixFS header of one dag-pb block."""

    links: list[dict[str, Any]] = []
    unixfs: dict[str, Any] | None = None
    for number, value in _protobuf_fields(block):
        if number == 2 and isinstance(value, bytes):
            link: dict[str, Any] = {"name": "", "cid": None, "tsize": None}
            for link_number, link_value in _protobuf_fields(value):
                if link_number == 1 and isinstance(link_value, bytes):
                    if len(link_value) != 34 or link_value[:2] != b"\x12\x20":
                        raise IpfsBlockError("link is not a sha2-256 CIDv0")
                    link["cid"] = b58encode(link_value)
                elif link_number == 2 and isinstance(link_value, bytes):
                    link["name"] = link_value.decode("utf-8")
                elif link_number == 3 and isinstance(link_value, int):
                    link["tsize"] = link_value
            links.append(link)
        elif number == 1 and isinstance(value, bytes):
            header: dict[str, Any] = {}
            for field_number, field_value in _protobuf_fields(value):
                if field_number == 1:
                    header["type"] = field_value
                elif field_number == 2 and isinstance(field_value, bytes):
                    header["data_bytes"] = len(field_value)
                elif field_number == 3:
                    header["filesize"] = field_value
                elif field_number == 5:
                    header["hash_type"] = field_value
                elif field_number == 6:
                    header["fanout"] = field_value
            unixfs = header
    return {"links": links, "unixfs": unixfs}


def _rotl64(value: int, shift: int) -> int:
    return ((value << shift) | (value >> (64 - shift))) & 0xFFFFFFFFFFFFFFFF


def _fmix64(value: int) -> int:
    value ^= value >> 33
    value = (value * 0xFF51AFD7ED558CCD) & 0xFFFFFFFFFFFFFFFF
    value ^= value >> 33
    value = (value * 0xC4CEB9FE1A85EC53) & 0xFFFFFFFFFFFFFFFF
    value ^= value >> 33
    return value


def murmur3_x64_128(data: bytes, seed: int = 0) -> tuple[int, int]:
    """Return (h1, h2) of MurmurHash3 x64-128."""

    mask = 0xFFFFFFFFFFFFFFFF
    c1, c2 = 0x87C37B91114253D5, 0x4CF5AD432745937F
    h1 = h2 = seed & mask
    blocks = len(data) // 16
    for index in range(blocks):
        k1 = int.from_bytes(data[index * 16 : index * 16 + 8], "little")
        k2 = int.from_bytes(data[index * 16 + 8 : index * 16 + 16], "little")
        k1 = (_rotl64((k1 * c1) & mask, 31) * c2) & mask
        h1 ^= k1
        h1 = (_rotl64(h1, 27) + h2) & mask
        h1 = (h1 * 5 + 0x52DCE729) & mask
        k2 = (_rotl64((k2 * c2) & mask, 33) * c1) & mask
        h2 ^= k2
        h2 = (_rotl64(h2, 31) + h1) & mask
        h2 = (h2 * 5 + 0x38495AB5) & mask
    tail = data[blocks * 16 :]
    k1 = k2 = 0
    if len(tail) > 8:
        k2 = int.from_bytes(tail[8:], "little")
        k2 = (_rotl64((k2 * c2) & mask, 33) * c1) & mask
        h2 ^= k2
    if tail:
        k1 = int.from_bytes(tail[:8], "little")
        k1 = (_rotl64((k1 * c1) & mask, 31) * c2) & mask
        h1 ^= k1
    h1 ^= len(data)
    h2 ^= len(data)
    h1 = (h1 + h2) & mask
    h2 = (h2 + h1) & mask
    h1 = _fmix64(h1)
    h2 = _fmix64(h2)
    h1 = (h1 + h2) & mask
    h2 = (h2 + h1) & mask
    return h1, h2


def hamt_index(name: str, depth: int, fanout: int = 256) -> str:
    """Return the go-unixfs HAMT shard prefix for ``name`` at ``depth``."""

    if fanout != 256:
        raise IpfsBlockError("only 256-way HAMT shards are supported")
    digest = murmur3_x64_128(name.encode("utf-8"))[0].to_bytes(8, "big")
    if depth >= len(digest):
        raise IpfsBlockError("HAMT depth exceeds the 64-bit hash")
    return f"{digest[depth]:02X}"


__all__ = [
    "IpfsBlockError",
    "b58decode",
    "b58encode",
    "cidv0_for_file",
    "cidv0_of_block",
    "hamt_index",
    "multihash_of_cidv0",
    "murmur3_x64_128",
    "read_dag_pb",
    "verify_block",
]
