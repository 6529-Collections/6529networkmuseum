"""Deterministic MUSEUM_URI_SAFETY_PUBLIC_V1 conformance harness.

This file is a release-controlled executable artifact. It performs no network
access and validates the exact positive/negative URI vectors used by V1.
"""

from __future__ import annotations

import base64
import hashlib
import ipaddress
import json
import re
import sys
from urllib.parse import urlsplit

import rfc8785
from Crypto.Hash import keccak


if not __debug__:
    raise SystemExit("optimized Python disables conformance checks")


PROFILE = (b'{"id":"MUSEUM_URI_SAFETY_PUBLIC_V1","version":1,"maxUtf8Bytes":2048,"schemes":["ar","https","ipfs"],"requireLowercaseScheme":true,"reject":{"controls":true,"userinfo":true,"query":true,"fragment":true,"httpsPort":true,"httpsTrailingDot":true,"httpsNumericAmbiguity":true,"httpsMappedIpv6":true},"httpsDns":{"asciiLowercase":true,"labelMaxBytes":63,"totalMaxBytes":253,"requireDot":true},"httpsIp":{"reservedIpv4Cidr":["0.0.0.0/8","10.0.0.0/8","100.64.0.0/10","127.0.0.0/8","169.254.0.0/16","192.0.0.0/24","192.0.2.0/24","192.88.99.0/24","192.168.0.0/16","198.18.0.0/15","198.51.100.0/24","203.0.113.0/24","224.0.0.0/4","240.0.0.0/4"],"reservedIpv6Cidr":["::/128","::1/128","::ffff:0:0/96","100::/64","2001:2::/48","2001:10::/28","2001:db8::/32","fc00::/7","fe80::/10","ff00::/8"],"rejectReservedCidr":true,"rejectIpv4MappedIpv6":true,"ipv4DottedDecimal":true,"ipv6Rfc5952":true,"rejectZoneId":true,"rejectEmbeddedIpv4":true},"ipfs":{"cidv0":"reject","cidv1":{"multibase":"base32lower","prefix":"b","version":1,"codecs":[85,112],"multihashCode":18,"digestBytes":32,"rejectOverlongVarint":true,"requireCanonicalReencode":true}},"ar":{"identifier":"base64url-unpadded","characters":"A-Z a-z 0-9 _ -","length":43,"decodedBytes":32,"requireCanonicalReencode":true},"path":{"asciiPchar":true,"percentTripletsUppercase":true,"rejectMalformedPercent":true,"rejectEncodedUnreserved":true}}')
PROFILE_HASH = "8dc321494e0703072c5f2f1e7967473836640551e4b5c64e8fe94116029cefbb"
CID_V1 = "bafybeiexd37whdwmbipbf7acxcrll2pg6lwcz6ks7atxc6z4niszkoragq"
AR_TX = "A" * 43
RESERVED_IPV4 = tuple(ipaddress.ip_network(value) for value in (
    "0.0.0.0/8", "10.0.0.0/8", "100.64.0.0/10", "127.0.0.0/8",
    "169.254.0.0/16", "192.0.0.0/24", "192.0.2.0/24", "192.88.99.0/24",
    "192.168.0.0/16", "198.18.0.0/15", "198.51.100.0/24", "203.0.113.0/24",
    "224.0.0.0/4", "240.0.0.0/4"
))
RESERVED_IPV6 = tuple(ipaddress.ip_network(value) for value in (
    "::/128", "::1/128", "::ffff:0:0/96", "100::/64", "2001:2::/48",
    "2001:10::/28", "2001:db8::/32", "fc00::/7", "fe80::/10", "ff00::/8"
))


def keccak256(value: bytes) -> bytes:
    digest = keccak.new(digest_bits=256)
    digest.update(value)
    return digest.digest()


def _varint(value: bytes, offset: int) -> tuple[int, int]:
    result = 0
    shift = 0
    while offset < len(value) and shift <= 28:
        byte = value[offset]
        offset += 1
        result |= (byte & 0x7F) << shift
        if byte < 0x80:
            if shift and byte == 0:
                raise ValueError("non-canonical overlong varint")
            return result, offset
        shift += 7
    raise ValueError("invalid varint")


def _valid_cid(authority: str) -> bool:
    if not re.fullmatch(r"b[a-z2-7]+", authority):
        return False
    try:
        raw = base64.b32decode(authority[1:].upper() + "=" * ((8 - len(authority[1:]) % 8) % 8))
        if base64.b32encode(raw).decode("ascii").lower().rstrip("=") != authority[1:]:
            return False
        version, offset = _varint(raw, 0)
        codec, offset = _varint(raw, offset)
        code, offset = _varint(raw, offset)
        length, offset = _varint(raw, offset)
        return version == 1 and codec in {0x55, 0x70} and code == 0x12 and length == 32 and len(raw) == offset + length
    except (ValueError, IndexError, base64.binascii.Error):
        return False


def _valid_path(path: str) -> bool:
    if any(ord(char) < 0x20 or ord(char) == 0x7F for char in path):
        return False
    allowed = "/:@!$&'()*+,;=-._~"
    index = 0
    while index < len(path):
        char = path[index]
        if char == "%":
            if index + 2 >= len(path) or not re.fullmatch(r"[0-9A-Fa-f]{2}", path[index + 1:index + 3]):
                return False
            triplet = path[index + 1:index + 3]
            if triplet != triplet.upper():
                return False
            if chr(int(triplet, 16)) in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~":
                return False
            index += 3
            continue
        if not (char.isascii() and (char.isalnum() or char in allowed)):
            return False
        index += 1
    return True


def _globally_routable(address: ipaddress._BaseAddress) -> bool:
    return not (
        any(address in network for network in (RESERVED_IPV4 if address.version == 4 else RESERVED_IPV6))
        or
        address.is_private
        or address.is_loopback
        or address.is_link_local
        or address.is_multicast
        or address.is_unspecified
        or address.is_reserved
        or address.is_link_local
        or (isinstance(address, ipaddress.IPv6Address) and (address.is_site_local or address.ipv4_mapped is not None))
    )


def valid_uri(uri: str) -> bool:
    try:
        raw = uri.encode("utf-8")
    except UnicodeError:
        return False
    if len(raw) > 2048 or any(byte < 0x20 or byte == 0x7F for byte in raw):
        return False
    if not uri.startswith(("https://", "ipfs://", "ar://")):
        return False
    try:
        parsed = urlsplit(uri)
        parsed_port = parsed.port
    except (UnicodeError, ValueError):
        return False
    if parsed.scheme not in {"https", "ipfs", "ar"} or parsed.username is not None or parsed.password is not None:
        return False
    if parsed.query or parsed.fragment or not _valid_path(parsed.path):
        return False
    if parsed.scheme == "ar":
        if parsed.path or re.fullmatch(r"[A-Za-z0-9_-]{43}", parsed.netloc or "") is None:
            return False
        try:
            decoded = base64.urlsafe_b64decode((parsed.netloc + "==").encode("ascii"))
        except (ValueError, base64.binascii.Error):
            return False
        return len(decoded) == 32 and base64.urlsafe_b64encode(decoded).decode("ascii").rstrip("=") == parsed.netloc
    if parsed.scheme == "ipfs":
        return parsed_port is None and bool(parsed.netloc) and _valid_cid(parsed.netloc) and _valid_path(parsed.path)
    if parsed_port is not None or not parsed.netloc:
        return False
    host = parsed.netloc[1:-1] if parsed.netloc.startswith("[") and parsed.netloc.endswith("]") else parsed.netloc
    if parsed.netloc.startswith("["):
        if "%" in host:
            return False
        try:
            address = ipaddress.IPv6Address(host)
        except ipaddress.AddressValueError:
            return False
        return host == host.lower() and str(address) == host and _globally_routable(address)
    if any(ord(char) > 127 for char in host) or host != host.lower() or host.endswith(".") or "." not in host:
        return False
    try:
        address = ipaddress.ip_address(host)
    except ValueError:
        address = None
    if address is not None:
        octets = host.split(".")
        return len(octets) == 4 and all(str(int(octet)) == octet for octet in octets) and _globally_routable(address)
    if not re.fullmatch(r"[a-z0-9-]+(?:\.[a-z0-9-]+)+", host):
        return False
    labels = host.split(".")
    if any(not label or len(label) > 63 or label[0] == "-" or label[-1] == "-" for label in labels):
        return False
    if sum(len(label) for label in labels) + len(labels) - 1 > 253:
        return False
    if all(label.isdigit() for label in labels):
        return False
    return True


VECTORS = [
    {"id": "https-dns", "uri": "https://example.com/art", "accept": True},
    {"id": "https-hyphen", "uri": "https://a-b.example/x", "accept": True},
    {"id": "https-ipv4", "uri": "https://8.8.8.8/x", "accept": True},
    {"id": "https-ipv6", "uri": "https://[2001:4860:4860::8888]/x", "accept": True},
    {"id": "https-empty-path", "uri": "https://example.com", "accept": True},
    {"id": "ipfs-cidv1", "uri": f"ipfs://{CID_V1}/path", "accept": True},
    {"id": "ar-tx", "uri": f"ar://{AR_TX}", "accept": True},
    {"id": "https-trailing-dot", "uri": "https://example.com./x", "accept": False},
    {"id": "https-empty-label", "uri": "https://a..example.com/x", "accept": False},
    {"id": "https-leading-hyphen", "uri": "https://-a.example.com/x", "accept": False},
    {"id": "https-uppercase", "uri": "https://A.example.com/x", "accept": False},
    {"id": "https-port", "uri": "https://example.com:443/x", "accept": False},
    {"id": "https-userinfo", "uri": "https://user@example.com/x", "accept": False},
    {"id": "https-loopback", "uri": "https://127.0.0.1/x", "accept": False},
    {"id": "https-leading-zero", "uri": "https://010.0.0.1/x", "accept": False},
    {"id": "https-single-integer", "uri": "https://2130706433/x", "accept": False},
    {"id": "https-documentation-v4", "uri": "https://192.0.2.1/x", "accept": False},
    {"id": "https-mapped-v6", "uri": "https://[::ffff:8.8.8.8]/x", "accept": False},
    {"id": "https-documentation-v6", "uri": "https://[2001:db8::1]/x", "accept": False},
    {"id": "https-lower-percent", "uri": "https://example.com/a%2fb", "accept": False},
    {"id": "https-uppercase-percent", "uri": "https://example.com/a%2Fb", "accept": True},
    {"id": "https-encoded-unreserved", "uri": "https://example.com/a%41", "accept": False},
    {"id": "https-short-v4", "uri": "https://1.2.3/x", "accept": False},
    {"id": "https-hex-v4", "uri": "https://0x7f000001/x", "accept": False},
    {"id": "https-zone-id", "uri": "https://[2001:4860:4860::8888%25eth0]/x", "accept": False},
    {"id": "https-non-rfc5952", "uri": "https://[2001:4860:4860:0:0:0:0:8888]/x", "accept": False},
    {"id": "https-query", "uri": "https://example.com/x?y", "accept": False},
    {"id": "https-fragment", "uri": "https://example.com/x#frag", "accept": False},
    {"id": "ipfs-invalid-cid", "uri": "ipfs://bafybeigdyrzt5example/path", "accept": False},
    {"id": "ar-short", "uri": "ar://AbCdEf012_-", "accept": False},
    {"id": "https-control", "uri": "https://example.com/x\x01", "accept": False},
    {"id": "https-bare-percent", "uri": "https://example.com/a%", "accept": False},
    {"id": "https-invalid-percent-hex", "uri": "https://example.com/a%G0", "accept": False},
    {"id": "https-cgnat", "uri": "https://100.64.0.1/x", "accept": False},
    {"id": "https-nonnumeric-port", "uri": "https://example.com:abc/x", "accept": False},
    {"id": "https-nonascii-path", "uri": "https://example.com/café", "accept": False},
    {"id": "ipfs-overlong-varint", "uri": "ipfs://bqeahaeraaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/path", "accept": False},
    {"id": "ipfs-port", "uri": f"ipfs://{CID_V1}:443/path", "accept": False},
    {"id": "ipfs-cidv0-rejected", "uri": "ipfs://QmYwAPJzv5CZsnAzt8auVZRnGJH4p2v4WgDy5h1h7P42J9/path", "accept": False},
    {"id": "ipfs-cidv1-noncanonical-unused-bits", "uri": f"ipfs://{CID_V1[:-1]}r/path", "accept": False},
    {"id": "ar-noncanonical-unused-bits", "uri": f"ar://{AR_TX[:-1]}B", "accept": False},
    {"id": "https-uppercase-scheme", "uri": "HTTPS://example.com/x", "accept": False},
    {"id": "ipfs-uppercase-scheme", "uri": f"IPFS://{CID_V1}/path", "accept": False},
    {"id": "ar-uppercase-scheme", "uri": f"AR://{AR_TX}", "accept": False},
]


def main() -> int:
    assert len(PROFILE) == 1380
    assert keccak256(PROFILE).hex() == PROFILE_HASH
    for vector in VECTORS:
        actual = valid_uri(vector["uri"])
        assert actual == vector["accept"], (vector["id"], actual, vector)
    bundle = rfc8785.dumps(VECTORS)
    bundle_hash = keccak256(bundle).hex()
    expected_bundle_hash = "252c699a34e0c162f4055c292f23f7360272e3ec4b37031f2d17966055641011"
    assert bundle_hash == expected_bundle_hash, bundle_hash
    print(f"profileBytes={len(PROFILE)} profileHash=0x{PROFILE_HASH}")
    print(f"vectorCount={len(VECTORS)} vectorBundleHash=0x{bundle_hash}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
