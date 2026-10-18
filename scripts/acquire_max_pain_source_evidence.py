#!/usr/bin/env python3
"""Retain the public source package for MAX PAIN #4188/7394 (6529NM.2026.005.01).

The package records, with exact hashes and safe-fetch transport observations:

* the on-chain ``tokenURI`` and ``tokenIPFSHash`` read at one finalized block;
* the token metadata JSON fetched from an HTTPS IPFS gateway, with the IPFS
  path from the tokenURI root CID verified block by block (sha2-256 of every
  raw dag-pb block, go-unixfs HAMT shard indices, and the recomputed CIDv0 of
  the metadata bytes);
* the token's animated GIF, admitted out of band (it exceeds the safe-fetch
  response cap) from ``--gif-source-dir``.  Both downloaded copies -- the
  metadata ``image`` CDN URL and the ``image_hash`` CID through an IPFS
  gateway -- must be byte-identical, match the pinned SHA-256 and size, pass
  the strict GIF structure walk, recompute to the ``image_hash`` CIDv0 and
  match the CDN ETag as an MD5;
* public-safe projections of the Museum Wave drop, the Wave configuration, the
  drop's current votes and its vote log.  Raw Wave responses embed profile
  objects with wallet addresses, so only the projection is retained, with the
  raw response's SHA-256 and size (Magnum public-safe precedent);
* extracted visible-text transcripts of xcopy.art pages.  Raw HTML is not
  retained because it embeds ``<script`` elements, which the public evidence
  validator rejects; its SHA-256 and size are recorded;
* Nifty Gateway platform facts from a Wayback snapshot of the drop page, two
  short citations from the Wayback copy of the 2022 announcement, and two
  sentences of the live closure notice, when they are reachable within the
  safe-fetch limits; otherwise they are recorded as unretained sources.

X/Twitter is never fetched.  This tool does not decide title, rights,
authenticity, acceptance or accession.
"""

from __future__ import annotations

import argparse
from datetime import UTC, datetime
import hashlib
from html.parser import HTMLParser
from io import BytesIO
import json
from pathlib import Path
import re
import stat
import sys
from typing import Any

from PIL import Image

from gif_structure import GifStructureError, parse_gif
from ipfs_unixfs import IpfsBlockError, cidv0_for_file, hamt_index, read_dag_pb, verify_block
import max_pain_evidence_common as common
from max_pain_evidence_common import (
    ACCESSION_ID,
    CONTRACT,
    EvidenceError,
    IMAGE_CDN_URL,
    IMAGE_CID,
    IMAGE_SHA256,
    IMAGE_SIZE,
    METADATA_ROOT_CID,
    OBJECT_ID,
    PRIMARY_RPC_URL,
    PROPOSAL_DROP_ID,
    PROPOSAL_SERIAL,
    TOKEN_ID,
    TOKEN_NAME,
    TOKEN_URI,
    WAVE_ID,
)
from safe_fetch import FetchPolicyError


USER_AGENT = "6529-Network-Museum/xcopy-max-pain-4188-source-acquisition-v1"
RECORD_ID = f"{ACCESSION_ID}.SOURCE-EVIDENCE-01"
IPFS_GATEWAY = "https://gateway.pinata.cloud/ipfs"
METADATA_URL = f"{IPFS_GATEWAY}/{METADATA_ROOT_CID}/{TOKEN_ID}"
IMAGE_GATEWAY_URL = f"{IPFS_GATEWAY}/{IMAGE_CID}"
WAVE_API = "https://api.6529.io/api"
DROP_URL = f"{WAVE_API}/drops/{PROPOSAL_DROP_ID}"
WAVE_URL = f"{WAVE_API}/waves/{WAVE_ID}"
VOTES_URL = f"https://api.6529.io/api/v2/drops/{PROPOSAL_DROP_ID}/votes?page=1&page_size=50"
VOTE_LOG_URL = f"https://api.6529.io/api/v2/drops/{PROPOSAL_DROP_ID}/votes/logs?limit=100"
XCOPY_PAGES = (
    ("xcopy-art-works-max-pain", "https://xcopy.art/works/max-pain"),
    ("xcopy-art-works-max-pain-4188", "https://xcopy.art/works/max-pain/max-pain-41887394"),
    ("xcopy-art-series-max-pain-and-frens", "https://xcopy.art/series/max-pain-and-frens"),
    ("xcopy-art-series-damage-control", "https://xcopy.art/series/damage-control"),
    ("xcopy-art-creative-commons", "https://xcopy.art/creative-commons"),
    ("xcopy-art-privacy", "https://xcopy.art/privacy"),
)
XCOPY_EXPECTED_PHRASES = {
    "xcopy-art-works-max-pain": ("MAX PAIN AND FRENS", "1 of 4849", "Released March 24, 2022.", "No rights reserved."),
    "xcopy-art-works-max-pain-4188": (TOKEN_NAME, "1 of 7394", "No rights reserved."),
    "xcopy-art-series-max-pain-and-frens": ("Nifty Gateway smart contracts",),
    "xcopy-art-series-damage-control": ("Manifold smart contracts",),
    "xcopy-art-creative-commons": (),
    "xcopy-art-privacy": ("CC0 (Creative Commons Zero)", "do not imply affiliation, endorsement, or partnership"),
}
NG_DROP_WAYBACK_URL = (
    "https://web.archive.org/web/20250905032040id_/"
    "https://www.niftygateway.com/marketplace/collection/0xd1169e5349d1cb9941f3dcba135c8a4b9eacfdde/1/"
)
NG_MEDIUM_WAYBACK_URL = (
    "https://web.archive.org/web/20220518011554if_/"
    "https://medium.com/nifty-gateway/max-pain-and-frens-by-xcopy-959350e0fc70"
)
NG_MEDIUM_CITATIONS = (
    "MAX PAIN, 1 ETH, 10 Minute Open Edition",
    "It’s inspired by the chaos, adrenaline and risk in this space.",
)
NG_LIVE_URL = "https://niftygateway.com/collections/xcopy-oe"
NG_LIVE_CITATIONS = (
    "The Nifty Gateway platform officially closed on April 23, 2026.",
    "Our plan is to preserve NFT metadata and images on Nifty Gateway's servers in perpetuity.",
)
NG_STORE_DESCRIPTION_CITATIONS = (
    "It will be priced at ~ 1 ETH at the time of the drop.",
    "1 edition has been reserved by XCOPY + the Nifty Gateway team for a",
)
NG_CONTRACT_FIELDS = (
    "contractAddress",
    "contractId",
    "storeName",
    "storeURL",
    "template",
    "listingType",
    "publisherSlug",
    "project_category",
    "OpeningDateTimeInUTC",
    "ClosingDateTimeInUTC",
    "scheduled_start_date_time",
    "scheduled_end_date_time",
    "dropEndTime",
    "project_cover_photo_url",
    "isForPrimaryMarketSale",
)
NG_NIFTY_FIELDS = (
    "niftyType",
    "niftyTitle",
    "niftyDescription",
    "artist_name",
    "niftyContractAddress",
    "niftyCanonicalImageHash",
    "niftyImageURL",
    "niftyTotalNumOfEditions",
    "niftyTotalReserved",
    "niftyTotalBurnt",
    "niftyPriceInCents",
    "niftyEditionNumIncludedInTitle",
    "primary_sale_type",
    "projectType",
    "max_quantity_per_checkout",
    "scheduledStartDateTime",
    "scheduledEndDateTime",
    "baseChain",
    "has_sound",
    "isThreeDimensional",
)
PROJECTION_CANONICALIZATION = (
    "Hash the payload object only as UTF-8 JSON with recursively lexicographically sorted object keys, "
    "source-order arrays, compact separators, preserved Unicode, and no trailing newline."
)
WAVE_EXCLUSION_NOTE = (
    "Public-safe projection of an unauthenticated live 6529 API read. The retained record excludes "
    "author, voter, rater, reaction and profile objects, wallet addresses, handles, credentials and every "
    "field not listed in the payload; the raw response is recorded by SHA-256 and size only. WINNER and "
    "signed state record a Wave decision and publication observation only; they do not establish purchase "
    "or donor authority, the exact token, legal title, copyright, custody, acceptance, accession, "
    "Collection status, or display permission."
)
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
HTML_SKIP = {"script", "style", "noscript", "template", "svg", "head", "iframe", "object", "canvas"}
HTML_BLOCK = {
    "p", "div", "section", "article", "header", "footer", "main", "nav", "li", "ul", "ol", "h1", "h2",
    "h3", "h4", "h5", "h6", "br", "tr", "table", "blockquote", "figure", "figcaption", "pre", "dd",
    "dt", "dl", "hr", "aside", "title",
}
NEXT_FLIGHT_PUSH = re.compile(r'self\.__next_f\.push\(\[1,("(?:[^"\\]|\\.)*")\]\)')
GIF_HEADER_ALLOWLIST = (
    "content-type",
    "content-length",
    "etag",
    "last-modified",
    "x-amz-version-id",
    "date",
    "age",
    "x-cache",
    "cache-control",
    "x-ipfs-path",
    "x-ipfs-roots",
)
HEADER_VALUE = re.compile(r"^[\x20-\x7e]{1,200}$")
RFC3339_UTC = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z$")


class VisibleText(HTMLParser):
    """Collect visible text; executable and non-text containers are skipped."""

    def __init__(self, scope: str | None = None) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.skip_depth = 0
        self.scope = scope
        self.scope_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if self.scope and tag == self.scope:
            self.scope_depth += 1
        if tag in HTML_SKIP:
            self.skip_depth += 1
        if tag in HTML_BLOCK:
            self.parts.append("\n")

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in HTML_BLOCK:
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in HTML_SKIP and self.skip_depth:
            self.skip_depth -= 1
        if tag in HTML_BLOCK:
            self.parts.append("\n")
        if self.scope and tag == self.scope and self.scope_depth:
            self.scope_depth -= 1

    def handle_data(self, data: str) -> None:
        if not self.skip_depth and (not self.scope or self.scope_depth):
            self.parts.append(data)


def visible_text(html: str, scope: str | None = None) -> str:
    parser = VisibleText(scope)
    parser.feed(html)
    parser.close()
    lines = [re.sub(r"[ \t\r\f\v ​]+", " ", line).strip() for line in "".join(parser.parts).split("\n")]
    return "\n".join(line for line in lines if line) + "\n"


def redact_emails(text: str) -> tuple[str, int]:
    return EMAIL.subn("[email address omitted]", text)


def safe_transcript(text: str, label: str) -> str:
    if "<script" in text.lower() or "\x00" in text:
        raise EvidenceError(f"{label} transcript contains executable or binary content")
    return text


def flight_text(html: str) -> str:
    """Decode the Next.js app-router flight strings embedded in an HTML page."""

    return "".join(json.loads(literal) for literal in NEXT_FLIGHT_PUSH.findall(html))


def flight_object_with(text: str, key: str) -> dict[str, Any] | None:
    decoder = json.JSONDecoder()
    position = text.find(f'"{key}"')
    cursor = position
    while position >= 0 and cursor > 0:
        cursor = text.rfind("{", 0, cursor)
        if cursor < 0:
            return None
        try:
            value, end = decoder.raw_decode(text, cursor)
        except json.JSONDecodeError:
            continue
        if end > position and isinstance(value, dict) and key in value:
            return value
    return None


def citations(text: str, phrases: tuple[str, ...]) -> list[dict[str, Any]]:
    return [{"text": phrase, "found_verbatim": phrase in text} for phrase in phrases]


def projection_record(projection_id: str, url: str, observation: dict[str, Any], body: bytes, payload: dict[str, Any], reason: str) -> dict[str, Any]:
    return {
        "evidence_type": "WAVE_API_PUBLIC_SAFE_PROJECTION",
        "projection_id": projection_id,
        "observed_at": observation["observed_at"],
        "source_url": url,
        "source_request": "Unauthenticated HTTPS GET through scripts/safe_fetch.py (HTTP/1.0 connection factory).",
        "canonicalization": PROJECTION_CANONICALIZATION,
        "payload": payload,
        "payload_sha256": f"sha256:{common.sha256(common.canonical_json(payload))}",
        "raw_response": {
            "retained": False,
            "sha256": f"sha256:{common.sha256(body)}",
            "size": len(body),
            "media_type": observation.get("media_type"),
            "reason": reason,
        },
        "exclusion_note": WAVE_EXCLUSION_NOTE,
    }


def ms_to_iso(value: Any) -> str | None:
    if not isinstance(value, int) or isinstance(value, bool):
        return None
    return datetime.fromtimestamp(value / 1000, UTC).isoformat(timespec="milliseconds").replace("+00:00", "Z")


class SourcePackage:
    def __init__(self, output: Path) -> None:
        self.output = output
        self.client = common.RpcClient(USER_AGENT)
        self.entries: list[dict[str, Any]] = []
        self.rpc_sequence = 0
        self.rpc_records: list[dict[str, Any]] = []

    def add_file(self, relative: str, payload: bytes, media_type: str, source_id: str, url: str | None = None, **extra: Any) -> dict[str, Any]:
        target = self.output / relative
        if target.exists():
            raise EvidenceError(f"duplicate evidence path: {relative}")
        common.write_bytes(target, payload)
        entry = {
            "source_id": source_id,
            "path": relative,
            "media_type": media_type,
            "sha256": common.sha256(payload),
            "size": len(payload),
            "byte_mode": "raw",
            **({"url": url} if url else {}),
            **extra,
        }
        self.entries.append(entry)
        return entry

    def rpc(self, label: str, method: str, params: list[Any]) -> Any:
        self.rpc_sequence += 1
        call = self.client.call(PRIMARY_RPC_URL, label, method, params)
        prefix = f"raw/rpc/{self.rpc_sequence:04d}-{label}"
        self.add_file(f"{prefix}-request.json", call["request_bytes"], "application/json", f"rpc-{label}-request")
        self.add_file(f"{prefix}-response.json", call["response_bytes"], "application/json", f"rpc-{label}-response", PRIMARY_RPC_URL)
        self.rpc_records.append(
            {
                "label": label,
                "method": method,
                "request_path": f"{prefix}-request.json",
                "response_path": f"{prefix}-response.json",
                "transport": call["transport"],
            }
        )
        return common.require_result(call, label)

    def get(self, url: str, accept: str = "*/*") -> tuple[bytes, dict[str, Any]]:
        result, attempts = common.fetch(url, accept=accept, user_agent=USER_AGENT)
        observation = result.observation.to_dict()
        observation["attempts"] = attempts
        return result.body, observation


def parse_header_file(path: Path) -> dict[str, Any]:
    lines = path.read_text(encoding="ascii", errors="strict").splitlines()
    if not lines or not re.fullmatch(r"HTTP/\d(?:\.\d)? 200(?: OK)?", lines[0].strip()):
        raise EvidenceError(f"{path.name}: first line is not an HTTP 200 status line")
    selected: dict[str, str] = {}
    for line in lines[1:]:
        if not line.strip():
            continue
        name, separator, value = line.partition(":")
        name = name.strip().lower()
        value = value.strip()
        if not separator or name not in GIF_HEADER_ALLOWLIST:
            continue
        if not HEADER_VALUE.fullmatch(value):
            raise EvidenceError(f"{path.name}: header {name} has an unsafe value")
        if name in selected:
            raise EvidenceError(f"{path.name}: duplicate header {name}")
        selected[name] = value
    return {"status_line": lines[0].strip(), "headers": dict(sorted(selected.items()))}


def regular_file(directory: Path, relative: str) -> Path:
    path = directory / relative
    info = path.lstat()
    reparse = getattr(info, "st_file_attributes", 0) & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
    if not stat.S_ISREG(info.st_mode) or stat.S_ISLNK(info.st_mode) or reparse:
        raise EvidenceError(f"out-of-band source is not a regular file: {relative}")
    if not path.resolve().is_relative_to(directory.resolve()):
        raise EvidenceError(f"out-of-band source escapes its directory: {relative}")
    return path


def admit_gif(package: SourcePackage, source_dir: Path, acquired_at: str) -> dict[str, Any]:
    cdn_path = regular_file(source_dir, "cdn/MAX_PAIN_1_bhtyc0.gif")
    ipfs_path = regular_file(source_dir, f"ipfs/{IMAGE_CID}.bin")
    cdn_bytes = cdn_path.read_bytes()
    ipfs_bytes = ipfs_path.read_bytes()
    if cdn_bytes != ipfs_bytes:
        raise EvidenceError("CDN and IPFS gateway copies of the token image differ")
    if common.sha256(cdn_bytes) != IMAGE_SHA256 or len(cdn_bytes) != IMAGE_SIZE:
        raise EvidenceError("token image does not match the pinned SHA-256 and size")
    try:
        structure = parse_gif(cdn_bytes)
    except GifStructureError as exc:
        raise EvidenceError(f"token image is not an admitted GIF: {exc}") from exc
    cid = cidv0_for_file(cdn_bytes)
    if cid["cid"] != IMAGE_CID:
        raise EvidenceError(f"recomputed CIDv0 {cid['cid']} does not equal the token image_hash")
    md5 = hashlib.md5(cdn_bytes).hexdigest()  # noqa: S324 - compared with an S3 ETag, not used for integrity
    cdn_headers = parse_header_file(regular_file(source_dir, "cdn/headers.txt"))
    ipfs_headers = parse_header_file(regular_file(source_dir, "ipfs/headers.txt"))
    etag = cdn_headers["headers"].get("etag", "").strip('"')
    if etag != md5:
        raise EvidenceError("CDN ETag is not the MD5 of the admitted bytes")
    if ipfs_headers["headers"].get("x-ipfs-roots") != IMAGE_CID:
        raise EvidenceError("IPFS gateway roots header does not name the image CID")
    for headers in (cdn_headers, ipfs_headers):
        if headers["headers"].get("content-length") != str(IMAGE_SIZE) or headers["headers"].get("content-type") != "image/gif":
            raise EvidenceError("out-of-band response headers do not match the admitted GIF")

    with Image.open(BytesIO(cdn_bytes)) as image:
        pillow = {
            "format": image.format,
            "width": image.width,
            "height": image.height,
            "frame_0_mode": image.mode,
            "n_frames": getattr(image, "n_frames", 1),
            "is_animated": bool(getattr(image, "is_animated", False)),
            "loop": image.info.get("loop"),
            "background": image.info.get("background"),
            "transparency": image.info.get("transparency"),
        }
        durations = []
        for index in range(pillow["n_frames"]):
            image.seek(index)
            durations.append(image.info.get("duration"))
        pillow["frame_durations_ms"] = durations
        pillow["version"] = Image.__version__
    if (
        pillow["n_frames"] != structure.frame_count
        or pillow["loop"] != structure.loop_count
        or durations != [10 * (frame.delay_centiseconds or 0) for frame in structure.frames]
        or (pillow["width"], pillow["height"]) != (structure.width, structure.height)
    ):
        raise EvidenceError("Pillow and the structural GIF reader disagree")

    entry = package.add_file(
        "raw/token-image.gif",
        cdn_bytes,
        "image/gif",
        "token-image",
        IMAGE_CDN_URL,
        alternate_urls=[IMAGE_GATEWAY_URL],
        ipfs_cid=IMAGE_CID,
    )
    frame_durations = sorted({frame.delay_centiseconds for frame in structure.frames})
    return {
        "source_id": "token-image",
        "path": entry["path"],
        "sha256": f"sha256:{IMAGE_SHA256}",
        "size": IMAGE_SIZE,
        "md5": md5,
        "sha3_256": hashlib.sha3_256(cdn_bytes).hexdigest(),
        "media_type": "image/gif",
        "admission": {
            "method": "out_of_band_download_admitted_by_hash",
            "reason": "The 4,541,937-byte image exceeds the 1 MiB safe-fetch response cap and Range requests are not admitted; both copies were downloaded separately and admitted here only after the checks below.",
            "precedent": "Magnum source-directory admission by SHA-256 and size",
            "acquired_at": acquired_at,
            "copies": [
                {
                    "role": "token_metadata_image_url",
                    "url": IMAGE_CDN_URL,
                    "response": cdn_headers,
                    "etag_equals_md5_of_bytes": True,
                    "mutable_location": True,
                },
                {
                    "role": "token_metadata_image_hash_via_ipfs_gateway",
                    "url": IMAGE_GATEWAY_URL,
                    "response": ipfs_headers,
                    "x_ipfs_roots_equals_image_hash": True,
                },
            ],
            "copies_byte_identical": True,
        },
        "ipfs_cid_recomputation": {**cid, "expected": IMAGE_CID, "match": True},
        "structure": {
            **{key: value for key, value in structure.to_dict().items() if key != "frames"},
            "frames": [frame.to_dict() for frame in structure.frames],
            "reader": "scripts/gif_structure.py strict block walk",
        },
        "pillow_cross_check": pillow,
        "animation": {
            "frame_count": structure.frame_count,
            "frame_duration_ms": 10 * frame_durations[0] if len(frame_durations) == 1 else None,
            "total_duration_ms": 10 * structure.total_delay_centiseconds,
            "loop": "infinite" if structure.loop_count == 0 else structure.loop_count,
        },
    }


def acquire_metadata(package: SourcePackage) -> dict[str, Any]:
    body, observation = package.get(METADATA_URL, "application/json")
    if observation["status"] != 200:
        raise EvidenceError(f"metadata gateway returned HTTP {observation['status']}")
    try:
        metadata = json.loads(body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise EvidenceError("token metadata is not UTF-8 JSON") from exc
    if not isinstance(metadata, dict):
        raise EvidenceError("token metadata JSON root is not an object")
    expected = {"name": TOKEN_NAME, "description": "MAX PAIN by XCOPY", "image": IMAGE_CDN_URL, "image_hash": IMAGE_CID}
    for key, value in expected.items():
        if metadata.get(key) != value:
            raise EvidenceError(f"token metadata {key} mismatch")
    package.add_file("raw/token-metadata.json", body, "application/json", "token-metadata", METADATA_URL, transport=observation)

    # Follow tokenURI's root CID through the sharded directory to the file.
    blocks: list[dict[str, Any]] = []
    cid = METADATA_ROOT_CID
    entry_name = str(TOKEN_ID)
    file_cid = cidv0_for_file(body)["cid"]
    for depth in range(8):
        block, block_observation = package.get(f"{IPFS_GATEWAY}/{cid}?format=raw", "application/vnd.ipld.raw")
        if block_observation["status"] != 200:
            raise EvidenceError(f"raw block {cid} returned HTTP {block_observation['status']}")
        verify_block(cid, block)
        node = read_dag_pb(block)
        header = node["unixfs"] or {}
        if header.get("type") != 5 or header.get("fanout") != 256 or header.get("hash_type") != 0x22:
            raise EvidenceError(f"block {cid} is not a 256-way murmur3 HAMT shard")
        prefix = hamt_index(entry_name, depth)
        leaf = [link for link in node["links"] if link["name"] == prefix + entry_name]
        shard = [link for link in node["links"] if link["name"] == prefix]
        record = {
            "cid": cid,
            "byte_length": len(block),
            "sha256": f"sha256:{common.sha256(block)}",
            "sha256_multihash_matches_cid": True,
            "unixfs_type": "HAMTShard",
            "fanout": 256,
            "link_count": len(node["links"]),
            "hamt_prefix": prefix,
            "transport": block_observation,
        }
        if len(leaf) == 1 and not shard:
            record["followed_link"] = {"name": leaf[0]["name"], "cid": leaf[0]["cid"], "kind": "entry"}
            blocks.append(record)
            if leaf[0]["cid"] != file_cid:
                raise EvidenceError("directory entry CID does not equal the recomputed metadata CIDv0")
            break
        if len(shard) != 1 or leaf:
            raise EvidenceError(f"HAMT block {cid} has no unique path for {entry_name}")
        record["followed_link"] = {"name": shard[0]["name"], "cid": shard[0]["cid"], "kind": "shard"}
        blocks.append(record)
        cid = shard[0]["cid"]
    else:
        raise EvidenceError("HAMT path exceeds the supported depth")
    return {
        "source_id": "token-metadata",
        "url": METADATA_URL,
        "token_uri": TOKEN_URI,
        "sha256": f"sha256:{common.sha256(body)}",
        "size": len(body),
        "fields": {key: metadata[key] for key in sorted(metadata)},
        "absent_fields": [key for key in ("license", "animation_url", "attributes", "properties") if key not in metadata],
        "file_cidv0": file_cid,
        "ipfs_path_verification": {
            "root_cid": METADATA_ROOT_CID,
            "entry_name": entry_name,
            "method": (
                "Each raw dag-pb block was fetched with ?format=raw, hashed with sha2-256 against its CID, parsed, "
                "and the go-unixfs HAMT shard prefix for the entry name (murmur3-x64-64, 256-way) was followed to "
                "the entry link, whose CID equals the CIDv0 recomputed from the metadata bytes."
            ),
            "blocks": blocks,
            "verified": True,
        },
    }


def wave_projections(package: SourcePackage) -> dict[str, Any]:
    raw: dict[str, tuple[bytes, dict[str, Any], Any]] = {}
    for name, url in (("drop", DROP_URL), ("wave", WAVE_URL), ("votes", VOTES_URL), ("vote_log", VOTE_LOG_URL)):
        body, observation = package.get(url, "application/json")
        if observation["status"] != 200:
            raise EvidenceError(f"Wave API {name} returned HTTP {observation['status']}")
        raw[name] = (body, observation, json.loads(body.decode("utf-8")))
    drop = raw["drop"][2]
    wave = raw["wave"][2]
    votes = raw["votes"][2]
    vote_log = raw["vote_log"][2]
    if drop.get("id") != PROPOSAL_DROP_ID or drop.get("serial_no") != PROPOSAL_SERIAL or drop.get("drop_type") != "WINNER":
        raise EvidenceError("Wave drop identity or WINNER status mismatch")
    if (drop.get("wave") or {}).get("id") != WAVE_ID or wave.get("id") != WAVE_ID:
        raise EvidenceError("Wave identity mismatch")
    parts = drop.get("parts")
    if not isinstance(parts, list) or not parts:
        raise EvidenceError("Wave drop has no parts")
    for part in parts:
        content = part.get("content") or ""
        if "@" in content or re.search(r"0x[0-9a-fA-F]{40}", content):
            raise EvidenceError("proposal text contains a mention or address; projection needs review")
    if not isinstance(votes, dict) or votes.get("next") is not False or not isinstance(votes.get("data"), list):
        raise EvidenceError("vote list is not a single complete page")
    if not isinstance(vote_log, list) or len(vote_log) >= 100:
        raise EvidenceError("vote log is not complete within one page")

    winning = drop.get("winning_context") or {}
    decision_ms = winning.get("decision_time")
    drop_payload = {
        "drop_id": drop["id"],
        "serial_no": drop["serial_no"],
        "drop_type": drop["drop_type"],
        "is_signed": drop.get("is_signed"),
        "title": drop.get("title"),
        "created_at_ms": drop.get("created_at"),
        "created_at": ms_to_iso(drop.get("created_at")),
        "updated_at_ms": drop.get("updated_at"),
        "author_role": "community member who posted the proposal; profile, handle and address excluded",
        "parts_count": drop.get("parts_count"),
        "parts": [
            {
                "part_id": part.get("part_id"),
                "content": part.get("content"),
                "content_sha256": "sha256:" + hashlib.sha256((part.get("content") or "").encode("utf-8")).hexdigest(),
                "media_count": len(part.get("media") or []),
                "attachment_count": len(part.get("attachments") or []),
                "quoted_drop": part.get("quoted_drop"),
            }
            for part in parts
        ],
        "mentioned_user_count": len(drop.get("mentioned_users") or []),
        "referenced_nft_count": len(drop.get("referenced_nfts") or []),
        "rating": drop.get("rating"),
        "realtime_rating": drop.get("realtime_rating"),
        "raters_count": drop.get("raters_count"),
        "winning_context": {
            "place": winning.get("place"),
            "decision_time_ms": decision_ms,
            "decision_time": ms_to_iso(decision_ms),
            "sale_time": winning.get("sale_time"),
            "sale_price": winning.get("sale_price"),
            "sale_price_currency": winning.get("sale_price_currency"),
            "awards": winning.get("awards"),
        },
        "wave": {
            "id": drop["wave"].get("id"),
            "name": drop["wave"].get("name"),
            "voting_credit_type": drop["wave"].get("voting_credit_type"),
            "voting_credit_scope": drop["wave"].get("voting_credit_scope"),
            "voting_period_start_ms": drop["wave"].get("voting_period_start"),
            "voting_period_end_ms": drop["wave"].get("voting_period_end"),
            "voting_group_id": drop["wave"].get("voting_group_id"),
            "participation_group_id": drop["wave"].get("participation_group_id"),
        },
    }

    decision = wave.get("wave") or {}
    voting = wave.get("voting") or {}
    participation = wave.get("participation") or {}
    voting_group = ((voting.get("scope") or {}).get("group") or {})
    participation_group = ((participation.get("scope") or {}).get("group") or {})
    wave_payload = {
        "wave_id": wave["id"],
        "name": wave.get("name"),
        "serial_no": wave.get("serial_no"),
        "created_at_ms": wave.get("created_at"),
        "voting": {
            "credit_type": voting.get("credit_type"),
            "credit_scope": voting.get("credit_scope"),
            "credit_category": voting.get("credit_category"),
            "signature_required": voting.get("signature_required"),
            "period": voting.get("period"),
            "forbid_negative_votes": voting.get("forbid_negative_votes"),
            "group": {"id": voting_group.get("id"), "name": voting_group.get("name"), "is_hidden": voting_group.get("is_hidden")},
        },
        "participation": {
            "signature_required": participation.get("signature_required"),
            "period": participation.get("period"),
            "terms": participation.get("terms"),
            "group": {"id": participation_group.get("id"), "name": participation_group.get("name"), "is_hidden": participation_group.get("is_hidden")},
        },
        "decision_configuration": {
            key: decision.get(key)
            for key in (
                "type",
                "winning_threshold",
                "winning_threshold_min_duration_ms",
                "max_winners",
                "max_votes_per_identity_to_drop",
                "time_lock_ms",
                "decisions_strategy",
                "total_no_of_decisions",
                "no_of_decisions_done",
            )
        },
        "pauses": wave.get("pauses"),
    }

    # Voter identities are used transiently to join the current votes with the
    # log; only anonymous counts, totals and timings are emitted.
    current = {row["voter"]["id"]: int(row["vote"]) for row in votes["data"]}
    entries = sorted(vote_log, key=lambda row: (row["created_at"], row["id"]))
    latest: dict[str, int] = {}
    running: list[dict[str, Any]] = []
    threshold = decision.get("winning_threshold")
    first_crossing = None
    dipped_after_crossing = False
    for row in entries:
        latest[row["voter"]["id"]] = int(row["new_vote"])
        total = sum(latest.values())
        running.append(
            {
                "created_at_ms": row["created_at"],
                "created_at": ms_to_iso(row["created_at"]),
                "old_vote": row["old_vote"],
                "new_vote": row["new_vote"],
                "cast_total_after": total,
            }
        )
        if isinstance(threshold, int) and total >= threshold and first_crossing is None:
            first_crossing = row["created_at"]
        if first_crossing is not None and isinstance(threshold, int) and total < threshold and row["created_at"] <= (decision_ms or 0):
            dipped_after_crossing = True
    at_decision = {}
    for row in entries:
        if isinstance(decision_ms, int) and row["created_at"] <= decision_ms:
            at_decision[row["voter"]["id"]] = int(row["new_vote"])
    capped = [voter for voter, value in current.items() if voter in latest and value < latest[voter]]
    votes_payload = {
        "page": votes.get("page"),
        "next": votes.get("next"),
        "count": votes.get("count"),
        "vote_entry_count": len(votes["data"]),
        "distinct_voter_count": len(current),
        "sum_of_current_votes": sum(current.values()),
        "all_current_votes_positive": all(value > 0 for value in current.values()),
        "drop_rating_at_observation": drop.get("rating"),
        "sum_minus_drop_rating": sum(current.values()) - (drop.get("rating") or 0),
        "current_votes_below_last_logged_vote_count": len(capped),
        "current_votes_below_last_logged_vote_total_reduction": sum(latest[voter] - current[voter] for voter in capped),
        "all_current_voters_appear_in_vote_log": set(current) <= set(latest),
    }
    log_payload = {
        "entry_count": len(entries),
        "complete_within_limit": True,
        "distinct_voter_count": len(latest),
        "entries": running,
        "winning_threshold": threshold,
        "first_threshold_crossing_at": ms_to_iso(first_crossing),
        "fell_below_threshold_before_decision": dipped_after_crossing,
        "decision_time": ms_to_iso(decision_ms),
        "cast_total_at_decision_time": sum(at_decision.values()),
        "distinct_voters_at_decision_time": len(at_decision),
    }
    reason = "The raw response embeds profile objects with handles and primary wallet addresses; only this projection is retained."
    outputs = {}
    for name, payload in (("drop", drop_payload), ("wave", wave_payload), ("votes", votes_payload), ("vote_log", log_payload)):
        body, observation, _ = raw[name]
        url = {"drop": DROP_URL, "wave": WAVE_URL, "votes": VOTES_URL, "vote_log": VOTE_LOG_URL}[name]
        record = projection_record(f"{RECORD_ID}.WAVE-{name.upper().replace('_', '-')}", url, observation, body, payload, reason)
        encoded = common.pretty_json(record)
        text = encoded.decode("utf-8").lower()
        if re.search(r'"(?:primary_address|handle|pfp|voter|profile|profiles|author|top_raters|reactions)"\s*:', text) or re.search(r"0x[0-9a-f]{40}", text):
            raise EvidenceError(f"{name} projection is not public-safe")
        slug = name.replace("_", "-")
        package.add_file(
            f"raw/wave/{slug}-public-safe.json",
            encoded,
            "application/json",
            f"wave-{slug}-public-safe-projection",
            url,
            raw_response_sha256=record["raw_response"]["sha256"].removeprefix("sha256:"),
            raw_response_size=len(body),
        )
        outputs[name] = {
            "path": f"raw/wave/{slug}-public-safe.json",
            "url": url,
            "payload_sha256": record["payload_sha256"],
            "raw_response": record["raw_response"],
            "transport": observation,
        }
    outputs["observations"] = {
        "drop_type": drop["drop_type"],
        "is_signed": drop.get("is_signed"),
        "serial_no": drop["serial_no"],
        "created_at": drop_payload["created_at"],
        "decision_time": drop_payload["winning_context"]["decision_time"],
        "rating": drop.get("rating"),
        "raters_count": drop.get("raters_count"),
        "winning_threshold": threshold,
        "first_threshold_crossing_at": log_payload["first_threshold_crossing_at"],
        "cast_total_at_decision_time": log_payload["cast_total_at_decision_time"],
        "distinct_voters": votes_payload["distinct_voter_count"],
        "proposal_content_sha256": drop_payload["parts"][0]["content_sha256"],
    }
    return outputs


def xcopy_transcripts(package: SourcePackage) -> list[dict[str, Any]]:
    records = []
    for source_id, url in XCOPY_PAGES:
        body, observation = package.get(url, "text/html")
        if observation["status"] != 200 or observation["media_type"] != "text/html":
            raise EvidenceError(f"{url} returned {observation['status']} {observation['media_type']}")
        text, redactions = redact_emails(visible_text(body.decode("utf-8")))
        text = safe_transcript(text, source_id)
        entry = package.add_file(f"raw/xcopy-art/{source_id}.txt", text.encode("utf-8"), "text/plain", source_id, url)
        records.append(
            {
                "source_id": source_id,
                "url": url,
                "final_url": observation["redirect_chain"][-1],
                "transcript": {
                    "path": entry["path"],
                    "sha256": f"sha256:{entry['sha256']}",
                    "size": entry["size"],
                    "method": "visible text via Python html.parser; script, style, noscript, template, svg, head, iframe, object and canvas content omitted; whitespace collapsed per line; e-mail addresses replaced",
                    "email_redactions": redactions,
                },
                "raw_response": {
                    "retained": False,
                    "sha256": f"sha256:{observation['byte_sha256']}",
                    "size": observation["byte_length"],
                    "media_type": observation["media_type"],
                    "reason": "Raw HTML embeds executable script elements, which the public evidence validator rejects; the extracted visible text is retained.",
                },
                "expected_phrases": citations(text, XCOPY_EXPECTED_PHRASES[source_id]),
                "evidence_class": "B",
                "transport": observation,
            }
        )
    return records


def nifty_gateway_sources(package: SourcePackage) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    retained: list[dict[str, Any]] = []
    unretained: list[dict[str, Any]] = []

    def attempt(source_id: str, url: str, build) -> None:
        try:
            body, observation = package.get(url, "text/html")
            if observation["status"] != 200:
                raise EvidenceError(f"HTTP {observation['status']}")
            payload = build(body.decode("utf-8", errors="strict"))
        except (EvidenceError, FetchPolicyError, OSError, UnicodeDecodeError, ValueError, KeyError) as exc:
            unretained.append({"source_id": source_id, "url": url, "retained": False, "observation": f"not retained: {exc}"})
            return
        record = {
            "source_id": source_id,
            "url": url,
            "served_url": observation["redirect_chain"][-1],
            "raw_response": {
                "retained": False,
                "sha256": f"sha256:{observation['byte_sha256']}",
                "size": observation["byte_length"],
                "media_type": observation["media_type"],
                "reason": "Raw HTML embeds executable script elements and third-party page text; only the listed facts and short citations are retained.",
            },
            "payload": payload,
            "transport": observation,
        }
        encoded = common.pretty_json(record)
        safe_transcript(encoded.decode("utf-8"), source_id)
        entry = package.add_file(f"raw/nifty-gateway/{source_id}.json", encoded, "application/json", source_id, url)
        retained.append({"source_id": source_id, "url": url, "path": entry["path"], "sha256": f"sha256:{entry['sha256']}", "evidence_class": payload["evidence_class"]})

    def drop_page(html: str) -> dict[str, Any]:
        flight = flight_text(html)
        contract = flight_object_with(flight, "storeName")
        nifty = flight_object_with(flight, "niftyTotalNumOfEditions")
        if not contract or not nifty:
            raise EvidenceError("drop data objects are not present in the snapshot")
        if str(contract.get("contractAddress", "")).lower() != CONTRACT or nifty.get("niftyCanonicalImageHash") != IMAGE_CID:
            raise EvidenceError("snapshot drop data does not describe this contract and image")
        store_description, _ = redact_emails(str(contract.get("storeDescription", "")))
        return {
            "evidence_class": "B",
            "snapshot": {"archive": "Internet Archive Wayback Machine", "requested_timestamp": "20250905032040", "mode": "id_ (original bytes); the served capture is the record's served_url"},
            "platform_contract_fields": {key: contract.get(key) for key in NG_CONTRACT_FIELDS},
            "platform_nifty_fields": {key: nifty.get(key) for key in NG_NIFTY_FIELDS},
            "store_description_citations": citations(store_description, NG_STORE_DESCRIPTION_CITATIONS),
            "visible_text_sha256": f"sha256:{common.sha256(visible_text(html).encode('utf-8'))}",
            "extraction": "Next.js flight strings decoded from self.__next_f.push literals; listed fields copied verbatim; user, owner and engagement fields excluded.",
        }

    def medium(html: str) -> dict[str, Any]:
        text = visible_text(html, "article")
        found = citations(text, NG_MEDIUM_CITATIONS)
        if not all(item["found_verbatim"] for item in found):
            raise EvidenceError("expected citations are not present in the archived article")
        return {
            "evidence_class": "B",
            "publication": "Nifty Gateway publication on Medium, 23 March 2022 (announcement with an XCOPY Q&A)",
            "snapshot": {"archive": "Internet Archive Wayback Machine", "requested_timestamp": "20220518011554", "mode": "if_ (archived page without toolbar); the served capture is the record's served_url"},
            "citations": found,
            "article_text_sha256": f"sha256:{common.sha256(text.encode('utf-8'))}",
            "retention_boundary": "Only the two short citations are retained; the article text is a third-party work and is not reproduced.",
        }

    def live(html: str) -> dict[str, Any]:
        text = visible_text(html)
        found = citations(text, NG_LIVE_CITATIONS)
        if not all(item["found_verbatim"] for item in found):
            raise EvidenceError("closure notice text not found")
        return {
            "evidence_class": "B",
            "page_role": "token metadata external_url, observed live",
            "citations": found,
            "visible_text_sha256": f"sha256:{common.sha256(text.encode('utf-8'))}",
        }

    attempt("nifty-gateway-drop-page-wayback-20250905", NG_DROP_WAYBACK_URL, drop_page)
    attempt("nifty-gateway-medium-announcement-wayback-20220518", NG_MEDIUM_WAYBACK_URL, medium)
    attempt("nifty-gateway-live-collection-page", NG_LIVE_URL, live)
    return retained, unretained


def acquire(output: Path, gif_source_dir: Path, gif_acquired_at: str) -> dict[str, Any]:
    if not RFC3339_UTC.fullmatch(gif_acquired_at):
        raise EvidenceError("--gif-acquired-at must be an RFC 3339 UTC timestamp")
    if not gif_source_dir.is_dir():
        raise EvidenceError("--gif-source-dir is not a directory")
    common.assert_fixed_identities()
    common.prepare_empty_output(output)
    package = SourcePackage(output)
    observed_at = common.utc_now()

    if package.rpc("chain-id", "eth_chainId", []) != "0x1":
        raise EvidenceError("RPC endpoint did not report Ethereum mainnet")
    block = package.rpc("finalized-block", "eth_getBlockByNumber", ["finalized", False])
    if not isinstance(block, dict):
        raise EvidenceError("finalized block is missing")
    finalized = {
        "number": common.hex_int(block.get("number"), "finalized number"),
        "hash": str(block.get("hash", "")).lower(),
        "timestamp": common.iso_from_unix(common.hex_int(block.get("timestamp"), "finalized timestamp")),
    }
    selector = {"blockHash": finalized["hash"], "requireCanonical": True}
    token_uri = common.abi_string(
        package.rpc("token-uri", "eth_call", [{"to": CONTRACT, "data": common.calldata("tokenURI(uint256)", TOKEN_ID)}, selector]),
        "tokenURI",
    )
    image_hash = common.abi_string(
        package.rpc("token-ipfs-hash", "eth_call", [{"to": CONTRACT, "data": common.calldata("tokenIPFSHash(uint256)", TOKEN_ID)}, selector]),
        "tokenIPFSHash",
    )
    if token_uri != TOKEN_URI:
        raise EvidenceError(f"tokenURI mismatch: {token_uri}")
    if image_hash != IMAGE_CID:
        raise EvidenceError(f"tokenIPFSHash mismatch: {image_hash}")

    metadata = acquire_metadata(package)
    image = admit_gif(package, gif_source_dir, gif_acquired_at)
    wave = wave_projections(package)
    xcopy = xcopy_transcripts(package)
    nifty_retained, nifty_unretained = nifty_gateway_sources(package)

    summary = {
        "record_id": RECORD_ID,
        "record_type": "DIGITAL_ART_SOURCE_OBSERVATION",
        "observed_at": observed_at,
        "accession_id": ACCESSION_ID,
        "object_id": OBJECT_ID,
        "object": {
            "caip19": common.CAIP19,
            "contract": CONTRACT,
            "token_id": TOKEN_ID,
            "token_name": TOKEN_NAME,
        },
        "onchain": {
            "rpc_endpoint": PRIMARY_RPC_URL,
            "finalized_block": finalized,
            "state_selector": selector,
            "token_uri": token_uri,
            "token_ipfs_hash": image_hash,
            "token_ipfs_hash_equals_metadata_image_hash": True,
            "calls": package.rpc_records,
        },
        "metadata": metadata,
        "media": image,
        "wave": {
            "wave_id": WAVE_ID,
            "drop_id": PROPOSAL_DROP_ID,
            "serial_no": PROPOSAL_SERIAL,
            **wave,
        },
        "artist_site": xcopy,
        "platform_sources": nifty_retained,
        "unretained_sources": [
            *nifty_unretained,
            {
                "source_id": "x-twitter-posts",
                "url": "https://x.com/",
                "retained": False,
                "observation": "Not fetched: X/Twitter content is outside this package's fetch policy; posts are cited by URL in research notes only.",
            },
        ],
        "assertions": {
            "token_uri_matches_expected_ipfs_path": True,
            "metadata_reached_from_token_uri_root_by_verified_ipfs_path": True,
            "metadata_image_hash_equals_onchain_token_ipfs_hash": True,
            "image_copies_byte_identical": True,
            "image_cidv0_recomputes_to_image_hash": True,
            "image_structure_admitted": True,
            "wave_drop_is_signed_winner": drop_is_signed_winner(wave),
        },
        "limitations": [
            "These are point-in-time public-source observations. They do not establish legal title, copyright ownership, display rights or accession.",
            "The metadata image URL is a mutable CDN location; the IPFS image_hash CID, set once on-chain through tokenIPFSHash, is the content binding.",
            "The retained GIF is preservation evidence of the token's image bytes; presentation derivatives are generated separately under media/.",
            "Wave projections omit voter and author identities; per-person contribution or wallet facts are not recorded here.",
            "xcopy.art and Nifty Gateway statements are issuer or platform sources (class B) and are recorded as observed, not as Museum determinations.",
        ],
    }
    summary_bytes = common.pretty_json(summary)
    safe_transcript(summary_bytes.decode("utf-8"), "summary")
    common.write_bytes(output / "summary.json", summary_bytes)
    manifest = {
        "manifest_type": "6529NM_XCOPY_MAX_PAIN_4188_SOURCE_EVIDENCE",
        "manifest_version": "1.0.0",
        "subject_id": OBJECT_ID,
        "record_id": RECORD_ID,
        "observed_at": observed_at,
        "hash_algorithm": "sha256",
        "byte_mode": "raw",
        "entries": [
            *[{key: value for key, value in entry.items() if key != "transport"} for entry in package.entries],
            {
                "source_id": "summary",
                "path": "summary.json",
                "media_type": "application/json",
                "sha256": common.sha256(summary_bytes),
                "size": len(summary_bytes),
                "byte_mode": "raw",
            },
        ],
    }
    manifest_bytes = common.pretty_json(manifest)
    common.write_bytes(output / "manifest.json", manifest_bytes)
    return {
        "status": "complete",
        "record_id": RECORD_ID,
        "finalized_block": finalized,
        "entry_count": len(manifest["entries"]),
        "summary_sha256": f"sha256:{common.sha256(summary_bytes)}",
        "manifest_sha256": f"sha256:{common.sha256(manifest_bytes)}",
        "image_sha256": f"sha256:{IMAGE_SHA256}",
        "unretained_sources": [item["source_id"] for item in summary["unretained_sources"]],
    }


def drop_is_signed_winner(wave: dict[str, Any]) -> bool:
    observations = wave.get("observations", {})
    return observations.get("drop_type") == "WINNER" and observations.get("is_signed") is True


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--output-dir", type=Path, default=common.ROOT / "evidence" / "xcopy-max-pain-4188-sources")
    parser.add_argument(
        "--gif-source-dir",
        type=Path,
        required=True,
        help="directory holding cdn/MAX_PAIN_1_bhtyc0.gif, cdn/headers.txt, ipfs/<image CID>.bin and ipfs/headers.txt",
    )
    parser.add_argument("--gif-acquired-at", required=True, help="RFC 3339 UTC time the out-of-band copies were downloaded")
    args = parser.parse_args(argv)
    try:
        result = acquire(args.output_dir.absolute(), args.gif_source_dir.absolute(), args.gif_acquired_at)
    except (EvidenceError, FetchPolicyError, GifStructureError, IpfsBlockError, OSError, ValueError) as exc:
        print(f"MAX PAIN source evidence acquisition refused: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
