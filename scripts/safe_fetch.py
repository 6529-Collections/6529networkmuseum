#!/usr/bin/env python3
"""Fail-closed HTTPS fetching with DNS/address pinning and audit observations.

This module is the only approved runtime network-fetch implementation in the
repository. Callers must use :class:`SafeHTTPSFetcher`; the CI fetch guard
rejects direct HTTP client, URL opener, raw-socket, and command-line fetch code
elsewhere.
"""

from __future__ import annotations

import hashlib
import http.client
import re
import socket
import ssl
import time
from dataclasses import dataclass
from datetime import UTC, datetime
from ipaddress import IPv4Address, IPv6Address, ip_address
from types import MappingProxyType
from typing import Any, Callable, Iterable, Mapping, Sequence
from urllib.parse import urljoin, urlsplit, urlunsplit


def _deep_freeze(value: object) -> object:
    if isinstance(value, Mapping):
        return MappingProxyType({str(key): _deep_freeze(child) for key, child in value.items()})
    if isinstance(value, (list, tuple)):
        return tuple(_deep_freeze(child) for child in value)
    if isinstance(value, set):
        return frozenset(_deep_freeze(child) for child in value)
    return value


_POLICY_SOURCE: dict[str, object] = {
    "mode": "resolve_at_fetch",
    "scheme": "https",
    "require_all_a_aaaa_global": True,
    "pin_connected_ip": True,
    "recheck_every_redirect": True,
    "unknown_hostname": "reject",
    "allowed_methods": ["GET", "HEAD", "POST"],
    "allowed_ports": [443],
    "max_redirects": 5,
    "max_response_bytes": 1_048_576,
    "max_request_bytes": 1_048_576,
    "max_url_length": 8_192,
    "connect_timeout_seconds": 10,
    "read_timeout_seconds": 20,
    "resolver_profile": "system_getaddrinfo",
    "resolver_revision": "python-socket.getaddrinfo-v1",
    "address_selection": "lowest_numeric",
}

# This is an owned, recursively immutable policy. The JSON-shaped copy is
# exported separately for schema/config comparisons; runtime code uses only
# SAFE_FETCH_POLICY.
SAFE_FETCH_POLICY: Mapping[str, object] = _deep_freeze(_POLICY_SOURCE)  # type: ignore[assignment]
SAFE_FETCH_POLICY_JSON: dict[str, object] = {
    key: list(value) if isinstance(value, tuple) else value
    for key, value in _POLICY_SOURCE.items()
}

SUSPICIOUS_HOSTS = {
    "localhost",
    "localhost.localdomain",
    "metadata",
    "nip.io",
    "sslip.io",
    "xip.io",
    "localtest.me",
    "lvh.me",
}
SUSPICIOUS_HOST_SUFFIXES = (
    ".localhost",
    ".local",
    ".internal",
    ".lan",
    ".nip.io",
    ".sslip.io",
    ".xip.io",
    ".localtest.me",
    ".lvh.me",
)
NUMERIC_HOST = re.compile(r"^(?:0[xX][0-9a-fA-F]+|[0-9]+)(?:\.(?:0[xX][0-9a-fA-F]+|[0-9]+))*$")
CANONICAL_IPV4 = re.compile(r"^(?:0|[1-9][0-9]{0,2})(?:\.(?:0|[1-9][0-9]{0,2})){3}$")
HOST_LABEL = re.compile(r"^[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?$")
HEADER_NAME = re.compile(r"^[!#$%&'*+.^_`|~0-9A-Za-z-]+$")
DECIMAL_CONTENT_LENGTH = re.compile(r"^(?:0|[1-9][0-9]*)$")
NON_ASCII_DOTS = {"\u3002", "\uff0e", "\uff61"}
ALLOWED_REQUEST_HEADERS = {"accept", "content-type", "user-agent"}
RESPONSE_BINDING_HEADERS = {
    "content-length",
    "content-type",
    "content-encoding",
    "transfer-encoding",
    "location",
}
REDIRECT_STATUSES = {301, 302, 303, 307, 308}


class FetchPolicyError(ValueError):
    """Raised when a URL, resolution, connection, response, or deadline is unsafe."""


@dataclass(frozen=True)
class CanonicalURL:
    url: str
    hostname: str
    port: int
    target: str


@dataclass(frozen=True)
class ResolvedEndpoint:
    hostname: str
    port: int
    addresses: tuple[str, ...]
    address_set_sha256: str
    selected_ip: str


@dataclass(frozen=True)
class FetchHop:
    canonical_url: str
    address_set: tuple[str, ...]
    address_set_sha256: str
    selected_ip: str
    peer_ip: str
    status: int
    media_type: str | None
    byte_length: int
    response_headers: tuple[tuple[str, str], ...]
    observed_at: str

    def to_dict(self) -> dict[str, object]:
        return {
            "canonical_url": self.canonical_url,
            "address_set": list(self.address_set),
            "address_set_sha256": self.address_set_sha256,
            "selected_ip": self.selected_ip,
            "peer_ip": self.peer_ip,
            "status": self.status,
            "media_type": self.media_type,
            "byte_length": self.byte_length,
            "response_headers": [[name, value] for name, value in self.response_headers],
            "observed_at": self.observed_at,
        }


@dataclass(frozen=True)
class FetchObservation:
    canonical_url: str
    resolver_profile: str
    resolver_revision: str
    address_set: tuple[str, ...]
    address_set_sha256: str
    selected_ip: str
    peer_ip: str
    redirect_chain: tuple[str, ...]
    observed_at: str
    status: int
    media_type: str | None
    byte_length: int
    byte_sha256: str
    response_headers: tuple[tuple[str, str], ...]
    hops: tuple[FetchHop, ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "canonical_url": self.canonical_url,
            "resolver_profile": self.resolver_profile,
            "resolver_revision": self.resolver_revision,
            "address_set": list(self.address_set),
            "address_set_sha256": self.address_set_sha256,
            "selected_ip": self.selected_ip,
            "peer_ip": self.peer_ip,
            "redirect_chain": list(self.redirect_chain),
            "observed_at": self.observed_at,
            "status": self.status,
            "media_type": self.media_type,
            "byte_length": self.byte_length,
            "byte_sha256": self.byte_sha256,
            "response_headers": [[name, value] for name, value in self.response_headers],
            "hops": [hop.to_dict() for hop in self.hops],
        }


@dataclass(frozen=True)
class SafeFetchResult:
    body: bytes
    observation: FetchObservation


Resolver = Callable[[str, int], Iterable[str | IPv4Address | IPv6Address]]
ConnectionFactory = Callable[[CanonicalURL, ResolvedEndpoint, Mapping[str, object]], Any]
Clock = Callable[[], datetime]


def _sort_addresses(addresses: Iterable[str]) -> tuple[str, ...]:
    return tuple(sorted(set(addresses), key=lambda value: (ip_address(value).version, int(ip_address(value)))))


def _format_host(hostname: str) -> str:
    return f"[{hostname}]" if ":" in hostname else hostname


def canonicalize_https_url(value: str) -> CanonicalURL:
    """Parse one canonical HTTPS URL and reject ambiguous/private host forms."""

    if not isinstance(value, str) or not value or len(value) > int(SAFE_FETCH_POLICY["max_url_length"]):
        raise FetchPolicyError("URL is empty or exceeds the policy length")
    if any(ord(char) < 0x20 or ord(char) == 0x7F for char in value):
        raise FetchPolicyError("URL contains control characters")
    try:
        parsed = urlsplit(value)
        port = parsed.port
    except ValueError as exc:
        raise FetchPolicyError("URL has invalid authority syntax") from exc
    if parsed.scheme.lower() != "https":
        raise FetchPolicyError("safe fetch requires HTTPS")
    if parsed.username is not None or parsed.password is not None:
        raise FetchPolicyError("URL userinfo is not allowed")
    if parsed.fragment:
        raise FetchPolicyError("URL fragments are not sent to HTTP servers")
    if port not in {None, 443}:
        raise FetchPolicyError("nonstandard HTTPS port is not allowed")
    raw_host = parsed.hostname
    if not raw_host:
        raise FetchPolicyError("URL has no hostname")
    if raw_host.endswith("."):
        raise FetchPolicyError("trailing-dot hostname is not admitted by the canonical policy")
    if any(dot in raw_host for dot in NON_ASCII_DOTS):
        raise FetchPolicyError("non-ASCII dot separator is not admitted")
    if any(char in raw_host for char in ("%", "\\", "*", "/")):
        raise FetchPolicyError("hostname has ambiguous or wildcard syntax")

    # IDNA normalization happens before all suspicious-name, suffix, numeric,
    # and IP checks. V1 then admits only ASCII canonical DNS labels, avoiding
    # Unicode confusables and resolver-dependent UTS-46 differences.
    try:
        hostname = raw_host.encode("idna").decode("ascii").casefold()
    except UnicodeError as exc:
        raise FetchPolicyError("hostname IDNA conversion failed") from exc
    if hostname in SUSPICIOUS_HOSTS or hostname.endswith(SUSPICIOUS_HOST_SUFFIXES):
        raise FetchPolicyError("wildcard, local, or metadata hostname is not allowed")
    if any(ord(char) > 127 for char in raw_host):
        raise FetchPolicyError("non-ASCII hostname is not admitted by the canonical policy")
    if not hostname or any(char in hostname for char in ("%", "\\", "*", "/")):
        raise FetchPolicyError("hostname has ambiguous or wildcard syntax")

    literal: IPv4Address | IPv6Address | None
    try:
        literal = ip_address(hostname)
    except ValueError:
        literal = None
    if literal is not None:
        if not literal.is_global:
            raise FetchPolicyError("literal IP is not globally routable")
        hostname = str(literal)
    else:
        if NUMERIC_HOST.fullmatch(hostname):
            if not CANONICAL_IPV4.fullmatch(hostname) or any(int(part) > 255 for part in hostname.split(".")):
                raise FetchPolicyError("noncanonical numeric IPv4 hostname")
        if "." not in hostname:
            raise FetchPolicyError("single-label hostname is not allowed")
        labels = hostname.split(".")
        if any(not HOST_LABEL.fullmatch(label) for label in labels):
            raise FetchPolicyError("hostname label is not canonical")

    path = parsed.path or "/"
    target = path + (f"?{parsed.query}" if parsed.query else "")
    canonical = urlunsplit(("https", _format_host(hostname), path, parsed.query, ""))
    return CanonicalURL(canonical, hostname, 443, target)


def system_resolver(hostname: str, port: int) -> tuple[str, ...]:
    """Resolve every TCP A/AAAA result without connecting or selecting in DNS."""

    infos = socket.getaddrinfo(hostname, port, family=socket.AF_UNSPEC, type=socket.SOCK_STREAM, proto=socket.IPPROTO_TCP)
    resolved: list[str] = []
    for family, _socktype, _proto, _canonname, sockaddr in infos:
        if family not in {socket.AF_INET, socket.AF_INET6}:
            continue
        resolved.append(_normalize_address(sockaddr[0]))
    return _sort_addresses(resolved)


def _normalize_address(value: str | IPv4Address | IPv6Address) -> str:
    if isinstance(value, (IPv4Address, IPv6Address)):
        address = value
    elif isinstance(value, str):
        try:
            address = ip_address(value)
        except ValueError as exc:
            raise FetchPolicyError("resolver returned a noncanonical IP address") from exc
    else:
        raise FetchPolicyError("resolver returned an unsupported address type")
    return str(address)


def resolve_and_pin(endpoint: CanonicalURL, resolver: Resolver = system_resolver) -> ResolvedEndpoint:
    try:
        raw_addresses = tuple(resolver(endpoint.hostname, endpoint.port))
    except (OSError, ValueError) as exc:
        raise FetchPolicyError("hostname resolution failed") from exc
    if not raw_addresses:
        raise FetchPolicyError("hostname resolution returned no A/AAAA answers")
    addresses = _sort_addresses(_normalize_address(value) for value in raw_addresses)
    if any(not ip_address(value).is_global for value in addresses):
        raise FetchPolicyError("hostname resolution returned a non-global address")
    address_set_sha256 = hashlib.sha256("\n".join(addresses).encode("ascii")).hexdigest()
    return ResolvedEndpoint(endpoint.hostname, endpoint.port, addresses, address_set_sha256, addresses[0])


class _PinnedHTTPSConnection(http.client.HTTPSConnection):
    """HTTPSConnection whose TCP destination is pinned while TLS uses the host."""

    def __init__(self, endpoint: CanonicalURL, selected_ip: str, connect_timeout: float, read_timeout: float, context: ssl.SSLContext) -> None:
        super().__init__(endpoint.hostname, endpoint.port, timeout=read_timeout, context=context)
        self._selected_ip = selected_ip
        self._connect_timeout = connect_timeout
        self._read_timeout = read_timeout
        self.peer_ip: str | None = None

    def connect(self) -> None:
        if self._tunnel_host:
            raise FetchPolicyError("HTTP proxy tunneling is not allowed")
        raw_socket = socket.create_connection((self._selected_ip, self.port), timeout=self._connect_timeout)
        try:
            self.sock = self._context.wrap_socket(raw_socket, server_hostname=self.host)
            self.sock.settimeout(self._read_timeout)
            peer = self.sock.getpeername()[0]
            self.peer_ip = _normalize_address(peer)
            if self.peer_ip != _normalize_address(self._selected_ip):
                raise FetchPolicyError("connected peer differs from pinned IP")
        except Exception:
            raw_socket.close()
            raise

    def request_with_headers(self, method: str, target: str, headers: Mapping[str, str], body: bytes | None = None) -> Any:
        self.putrequest(method, target, skip_host=True, skip_accept_encoding=True)
        host_header = next((value for name, value in headers.items() if name.lower() == "host"), _format_host(self.host))
        self.putheader("Host", host_header)
        for name, value in headers.items():
            if name.lower() != "host":
                self.putheader(name, value)
        self.endheaders(body)
        return self.getresponse()


def default_connection_factory(endpoint: CanonicalURL, resolved: ResolvedEndpoint, policy: Mapping[str, object]) -> _PinnedHTTPSConnection:
    context = ssl.create_default_context()
    return _PinnedHTTPSConnection(
        endpoint,
        resolved.selected_ip,
        float(policy["connect_timeout_seconds"]),
        float(policy["read_timeout_seconds"]),
        context,
    )


def _now(clock: Clock) -> datetime:
    value = clock()
    if value.tzinfo is None:
        raise FetchPolicyError("clock must return an aware UTC timestamp")
    return value.astimezone(UTC)


def _response_header_pairs(response: Any) -> tuple[tuple[str, str], ...]:
    headers = getattr(response, "headers", None)
    if headers is None:
        return ()
    try:
        raw_items = list(headers.items())
    except AttributeError:
        raw_items = list(headers)
    pairs: list[tuple[str, str]] = []
    for item in raw_items:
        if not isinstance(item, (tuple, list)) or len(item) != 2:
            raise FetchPolicyError("response headers are malformed")
        name, value = item
        name = str(name)
        values = value if isinstance(value, (list, tuple)) else (value,)
        for one_value in values:
            text_value = str(one_value)
            if not HEADER_NAME.fullmatch(name) or any(ord(char) < 0x20 or ord(char) == 0x7F for char in text_value):
                raise FetchPolicyError("response header contains invalid control syntax")
            pairs.append((name.lower(), text_value))
    return tuple(pairs)


def _header_values(pairs: Sequence[tuple[str, str]], name: str) -> tuple[str, ...]:
    return tuple(value for key, value in pairs if key == name.lower())


def _single_header(pairs: Sequence[tuple[str, str]], name: str) -> str | None:
    values = _header_values(pairs, name)
    if len(values) > 1:
        raise FetchPolicyError(f"duplicate response header: {name.lower()}")
    return values[0] if values else None


def _media_type(pairs: Sequence[tuple[str, str]]) -> str | None:
    value = _single_header(pairs, "content-type")
    return value.split(";", 1)[0].strip().lower() if value else None


def _validate_response_headers(pairs: Sequence[tuple[str, str]]) -> int | None:
    content_lengths = _header_values(pairs, "content-length")
    transfer_encodings = _header_values(pairs, "transfer-encoding")
    content_encodings = _header_values(pairs, "content-encoding")
    if len(content_lengths) > 1:
        raise FetchPolicyError("duplicate response Content-Length is not allowed")
    if transfer_encodings:
        # V1 deliberately does not admit chunked/transfer-coded responses.
        raise FetchPolicyError("Transfer-Encoding is not admitted by the safe-fetch policy")
    if content_encodings and any(value.casefold().strip() != "identity" for value in content_encodings):
        raise FetchPolicyError("compressed response bodies are not admitted")
    if content_lengths:
        value = content_lengths[0]
        if not DECIMAL_CONTENT_LENGTH.fullmatch(value):
            raise FetchPolicyError("response Content-Length is not a canonical nonnegative decimal")
        return int(value)
    return None


def _bound_response_headers(pairs: Sequence[tuple[str, str]]) -> tuple[tuple[str, str], ...]:
    return tuple((name, value) for name, value in pairs if name in RESPONSE_BINDING_HEADERS)


class SafeHTTPSFetcher:
    """Fetch bounded HTTPS responses through one resolve-pin-connect path."""

    def __init__(
        self,
        resolver: Resolver = system_resolver,
        connection_factory: ConnectionFactory = default_connection_factory,
        clock: Clock | None = None,
        policy: Mapping[str, object] = SAFE_FETCH_POLICY,
    ) -> None:
        if _deep_freeze(dict(policy)) != SAFE_FETCH_POLICY:
            raise FetchPolicyError("safe fetch policy is not the pinned repository policy")
        self.resolver = resolver
        self.connection_factory = connection_factory
        self.clock = clock or (lambda: datetime.now(UTC))
        # Never retain caller-owned policy data and never expose mutable state.
        self.policy = SAFE_FETCH_POLICY

    def _check_expiry(self, expires_at: datetime | None) -> None:
        if expires_at is None:
            return
        if expires_at.tzinfo is None:
            raise FetchPolicyError("expiry must be timezone-aware")
        if _now(self.clock) >= expires_at.astimezone(UTC):
            raise FetchPolicyError("fetch request expired")

    def _validate_headers(self, headers: Mapping[str, str] | None) -> dict[str, str]:
        result: dict[str, str] = {}
        seen: set[str] = set()
        for name, value in (headers or {}).items():
            if not isinstance(name, str) or not isinstance(value, str) or not HEADER_NAME.fullmatch(name):
                raise FetchPolicyError("invalid request header name")
            if name.lower() not in ALLOWED_REQUEST_HEADERS:
                raise FetchPolicyError(f"request header is not allowed: {name.lower()}")
            if name.lower() in seen:
                raise FetchPolicyError(f"duplicate request header: {name.lower()}")
            if any(ord(char) < 0x20 or ord(char) == 0x7F for char in value):
                raise FetchPolicyError("request header contains control characters")
            result[name] = value
            seen.add(name.lower())
        return result

    def _validate_body(self, method: str, headers: Mapping[str, str], body: bytes | None) -> bytes | None:
        if body is not None and not isinstance(body, bytes):
            raise FetchPolicyError("request body must be bytes")
        if body is not None and len(body) > int(self.policy["max_request_bytes"]):
            raise FetchPolicyError("request body exceeds policy")
        content_types = [value for name, value in headers.items() if name.lower() == "content-type"]
        if method == "POST":
            if body is None:
                raise FetchPolicyError("POST requests require a body")
            if len(content_types) != 1 or content_types[0].split(";", 1)[0].strip().casefold() != "application/json":
                raise FetchPolicyError("POST requests require an application/json Content-Type")
        elif body is not None:
            raise FetchPolicyError("request bodies are only allowed for POST")
        elif content_types:
            raise FetchPolicyError("Content-Type is only allowed for POST")
        return body

    @staticmethod
    def _read_limited(response: Any, limit: int, deadline: float) -> bytes:
        read = getattr(response, "read", None)
        if not callable(read):
            raise FetchPolicyError("response has no readable body")
        chunks: list[bytes] = []
        total = 0
        while True:
            if time.monotonic() > deadline:
                raise FetchPolicyError("response read timeout exceeded")
            try:
                chunk = read(min(65_536, limit - total + 1))
            except (OSError, TimeoutError) as exc:
                raise FetchPolicyError("response read failed or timed out") from exc
            if not isinstance(chunk, bytes):
                raise FetchPolicyError("response body is not bytes")
            if not chunk:
                break
            total += len(chunk)
            if total > limit:
                raise FetchPolicyError("response body exceeds policy")
            chunks.append(chunk)
        return b"".join(chunks)

    def fetch(
        self,
        url: str,
        *,
        method: str = "GET",
        body: bytes | None = None,
        headers: Mapping[str, str] | None = None,
        expires_at: datetime | None = None,
    ) -> SafeFetchResult:
        if not isinstance(method, str):
            raise FetchPolicyError("HTTP method must be a string")
        method = method.upper()
        allowed_methods = self.policy["allowed_methods"]
        if not isinstance(allowed_methods, Sequence) or method not in allowed_methods:
            raise FetchPolicyError("HTTP method is not allowed")
        request_headers = self._validate_headers(headers)
        request_body = self._validate_body(method, request_headers, body)
        endpoint = canonicalize_https_url(url)
        initial_url = endpoint.url
        redirect_chain = [initial_url]
        hops: list[FetchHop] = []

        for _redirect_index in range(int(self.policy["max_redirects"]) + 1):
            self._check_expiry(expires_at)
            resolved = resolve_and_pin(endpoint, self.resolver)
            connection = self.connection_factory(endpoint, resolved, self.policy)
            response: Any | None = None
            try:
                connection_headers = {**request_headers, "Host": _format_host(endpoint.hostname)}
                if request_body is not None:
                    # The caller cannot supply framing headers; the primitive
                    # emits one exact Content-Length for the bounded body.
                    connection_headers["Content-Length"] = str(len(request_body))
                if hasattr(connection, "request_with_headers"):
                    response = connection.request_with_headers(method, endpoint.target, connection_headers, request_body)
                else:
                    if request_body is None:
                        response = connection.request(method, endpoint.target, connection_headers)
                    else:
                        response = connection.request(method, endpoint.target, connection_headers, request_body)
                peer_ip = _normalize_address(getattr(connection, "peer_ip", ""))
                if peer_ip != resolved.selected_ip or peer_ip not in resolved.addresses:
                    raise FetchPolicyError("connected peer differs from vetted selected IP")
                status = int(response.status)
                response_pairs = _response_header_pairs(response)
                declared_size = _validate_response_headers(response_pairs)
                media_type = _media_type(response_pairs)
                observed_at = _now(self.clock).isoformat(timespec="milliseconds").replace("+00:00", "Z")
                body = self._read_limited(
                    response,
                    int(self.policy["max_response_bytes"]),
                    time.monotonic() + float(self.policy["read_timeout_seconds"]),
                )
                if method == "HEAD" and body:
                    raise FetchPolicyError("HEAD response unexpectedly contained a body")
                if declared_size is not None and declared_size != len(body):
                    raise FetchPolicyError("response Content-Length does not match actual bytes")
                bound_headers = _bound_response_headers(response_pairs)
                hops.append(
                    FetchHop(
                        endpoint.url,
                        resolved.addresses,
                        resolved.address_set_sha256,
                        resolved.selected_ip,
                        peer_ip,
                        status,
                        media_type,
                        len(body),
                        bound_headers,
                        observed_at,
                    )
                )
                if status in REDIRECT_STATUSES:
                    location = _single_header(response_pairs, "location")
                    if not location:
                        raise FetchPolicyError("redirect response has no Location")
                    if len(location) > int(self.policy["max_url_length"]):
                        raise FetchPolicyError("redirect Location exceeds policy length")
                    if len(redirect_chain) > int(self.policy["max_redirects"]):
                        raise FetchPolicyError("redirect limit exceeded")
                    endpoint = canonicalize_https_url(urljoin(endpoint.url, location))
                    redirect_chain.append(endpoint.url)
                    continue

                self._check_expiry(expires_at)
                observation = FetchObservation(
                    endpoint.url,
                    str(self.policy["resolver_profile"]),
                    str(self.policy["resolver_revision"]),
                    resolved.addresses,
                    resolved.address_set_sha256,
                    resolved.selected_ip,
                    peer_ip,
                    tuple(redirect_chain),
                    observed_at,
                    status,
                    media_type,
                    len(body),
                    hashlib.sha256(body).hexdigest(),
                    bound_headers,
                    tuple(hops),
                )
                return SafeFetchResult(body, observation)
            finally:
                close = getattr(connection, "close", None)
                if callable(close):
                    close()
        raise FetchPolicyError("redirect limit exceeded")


__all__ = [
    "CanonicalURL",
    "FetchObservation",
    "FetchPolicyError",
    "ResolvedEndpoint",
    "SAFE_FETCH_POLICY",
    "SAFE_FETCH_POLICY_JSON",
    "SafeFetchResult",
    "SafeHTTPSFetcher",
    "canonicalize_https_url",
    "default_connection_factory",
    "resolve_and_pin",
    "system_resolver",
]
