#!/usr/bin/env python3
"""Strict structural reader for GIF87a/GIF89a evidence bytes.

The reader walks the logical screen descriptor, colour tables, extension
blocks, image descriptors and every data sub-block length, and requires the
trailer byte ``0x3B`` as the final byte of the file.  It does not decompress
LZW image data and never executes or renders the file.  Raw-evidence admission
in ``bootstrap_validate.py`` and the MAX PAIN source/media tooling share this
one implementation so that the admitted profile cannot drift between them.

The admitted profile is deliberately narrower than every GIF a browser will
display: unknown block introducers, unknown extension labels, unregistered
application extensions, GIF89a extensions inside a GIF87a file, more than one
Graphic Control Extension per graphic rendering block, frames outside the
logical screen, and any byte after the trailer are rejected.
"""

from __future__ import annotations

from dataclasses import dataclass
import struct
from typing import Any


GIF_SIGNATURES = (b"GIF87a", b"GIF89a")
TRAILER = 0x3B
EXTENSION_INTRODUCER = 0x21
IMAGE_SEPARATOR = 0x2C
PLAIN_TEXT_LABEL = 0x01
GRAPHIC_CONTROL_LABEL = 0xF9
COMMENT_LABEL = 0xFE
APPLICATION_LABEL = 0xFF
# Application extensions with a documented, non-executable payload.  Any other
# identifier fails closed until it is reviewed and added here deliberately.
ADMITTED_APPLICATION_IDENTIFIERS = frozenset({b"NETSCAPE2.0", b"ANIMEXTS1.0", b"XMP DataXMP"})
LOOPING_APPLICATION_IDENTIFIERS = frozenset({b"NETSCAPE2.0", b"ANIMEXTS1.0"})


class GifStructureError(ValueError):
    """Raised when bytes are not an admitted, structurally complete GIF."""


@dataclass(frozen=True)
class GifFrame:
    index: int
    offset: int
    left: int
    top: int
    width: int
    height: int
    interlaced: bool
    local_colour_table_entries: int
    lzw_minimum_code_size: int
    data_sub_block_bytes: int
    delay_centiseconds: int | None
    disposal_method: int | None
    transparent_index: int | None
    user_input: bool

    def to_dict(self) -> dict[str, Any]:
        return {
            "index": self.index,
            "byte_offset": self.offset,
            "left": self.left,
            "top": self.top,
            "width": self.width,
            "height": self.height,
            "interlaced": self.interlaced,
            "local_colour_table_entries": self.local_colour_table_entries,
            "lzw_minimum_code_size": self.lzw_minimum_code_size,
            "data_sub_block_bytes": self.data_sub_block_bytes,
            "delay_centiseconds": self.delay_centiseconds,
            "disposal_method": self.disposal_method,
            "transparent_index": self.transparent_index,
            "user_input": self.user_input,
        }


@dataclass(frozen=True)
class GifStructure:
    version: str
    width: int
    height: int
    global_colour_table_entries: int
    colour_resolution_bits: int
    background_index: int
    pixel_aspect_ratio_byte: int
    frames: tuple[GifFrame, ...]
    loop_count: int | None
    application_extensions: tuple[str, ...]
    comment_extension_count: int
    plain_text_extension_count: int
    trailer_offset: int
    byte_length: int

    @property
    def frame_count(self) -> int:
        return len(self.frames)

    @property
    def total_delay_centiseconds(self) -> int:
        return sum(frame.delay_centiseconds or 0 for frame in self.frames)

    def to_dict(self) -> dict[str, Any]:
        return {
            "version": self.version,
            "logical_screen": {
                "width": self.width,
                "height": self.height,
                "global_colour_table_entries": self.global_colour_table_entries,
                "colour_resolution_bits": self.colour_resolution_bits,
                "background_index": self.background_index,
                "pixel_aspect_ratio_byte": self.pixel_aspect_ratio_byte,
            },
            "frame_count": self.frame_count,
            "total_delay_centiseconds": self.total_delay_centiseconds,
            "loop_count": self.loop_count,
            "application_extensions": list(self.application_extensions),
            "comment_extension_count": self.comment_extension_count,
            "plain_text_extension_count": self.plain_text_extension_count,
            "trailer_offset": self.trailer_offset,
            "byte_length": self.byte_length,
            "frames": [frame.to_dict() for frame in self.frames],
        }


def _colour_table_entries(packed: int) -> int:
    return 2 ** ((packed & 0x07) + 1)


def _require(payload: bytes, cursor: int, length: int, label: str) -> None:
    if cursor < 0 or length < 0 or cursor + length > len(payload):
        raise GifStructureError(f"truncated {label} at byte {cursor}")


def _skip_sub_blocks(payload: bytes, cursor: int, label: str) -> tuple[int, int, bytes]:
    """Return (next cursor, data byte count, first sub-block) after a terminator."""

    total = 0
    first = b""
    while True:
        _require(payload, cursor, 1, f"{label} sub-block length")
        size = payload[cursor]
        cursor += 1
        if size == 0:
            return cursor, total, first
        _require(payload, cursor, size, f"{label} sub-block data")
        if not total:
            first = payload[cursor : cursor + size]
        total += size
        cursor += size


def parse_gif(payload: bytes) -> GifStructure:
    """Parse and validate the complete GIF block structure of ``payload``."""

    if not isinstance(payload, (bytes, bytearray)):
        raise GifStructureError("GIF payload must be bytes")
    payload = bytes(payload)
    _require(payload, 0, 13, "header and logical screen descriptor")
    signature = payload[:6]
    if signature not in GIF_SIGNATURES:
        raise GifStructureError("GIF signature is not GIF87a or GIF89a")
    version = signature.decode("ascii")
    width, height, packed, background_index, aspect = struct.unpack("<HHBBB", payload[6:13])
    if not width or not height:
        raise GifStructureError("GIF logical screen has a zero dimension")
    cursor = 13
    global_entries = 0
    if packed & 0x80:
        global_entries = _colour_table_entries(packed)
        _require(payload, cursor, 3 * global_entries, "global colour table")
        cursor += 3 * global_entries
        if background_index >= global_entries:
            raise GifStructureError("GIF background index is outside the global colour table")
    colour_resolution_bits = ((packed >> 4) & 0x07) + 1

    frames: list[GifFrame] = []
    application_extensions: list[str] = []
    comment_count = 0
    plain_text_count = 0
    loop_count: int | None = None
    pending_control: tuple[int, int, int | None, bool] | None = None

    while True:
        _require(payload, cursor, 1, "block introducer")
        introducer = payload[cursor]
        if introducer == TRAILER:
            if cursor + 1 != len(payload):
                raise GifStructureError(
                    f"GIF has {len(payload) - cursor - 1} trailing bytes after the trailer"
                )
            if pending_control is not None:
                raise GifStructureError("GIF Graphic Control Extension has no graphic rendering block")
            if not frames:
                raise GifStructureError("GIF contains no image")
            return GifStructure(
                version=version,
                width=width,
                height=height,
                global_colour_table_entries=global_entries,
                colour_resolution_bits=colour_resolution_bits,
                background_index=background_index,
                pixel_aspect_ratio_byte=aspect,
                frames=tuple(frames),
                loop_count=loop_count,
                application_extensions=tuple(application_extensions),
                comment_extension_count=comment_count,
                plain_text_extension_count=plain_text_count,
                trailer_offset=cursor,
                byte_length=len(payload),
            )
        if introducer == EXTENSION_INTRODUCER:
            if version == "GIF87a":
                raise GifStructureError("GIF87a file contains a GIF89a extension block")
            _require(payload, cursor, 2, "extension label")
            label = payload[cursor + 1]
            cursor += 2
            if label == GRAPHIC_CONTROL_LABEL:
                if pending_control is not None:
                    raise GifStructureError("GIF has consecutive Graphic Control Extensions")
                _require(payload, cursor, 6, "Graphic Control Extension")
                if payload[cursor] != 4:
                    raise GifStructureError("GIF Graphic Control Extension block size is not 4")
                control_packed, delay, transparent = struct.unpack("<BHB", payload[cursor + 1 : cursor + 5])
                if payload[cursor + 5] != 0:
                    raise GifStructureError("GIF Graphic Control Extension lacks its block terminator")
                if control_packed & 0xE0:
                    raise GifStructureError("GIF Graphic Control Extension reserved bits are set")
                disposal = (control_packed >> 2) & 0x07
                if disposal > 3:
                    raise GifStructureError("GIF disposal method is undefined")
                pending_control = (
                    delay,
                    disposal,
                    transparent if control_packed & 0x01 else None,
                    bool(control_packed & 0x02),
                )
                cursor += 6
            elif label == APPLICATION_LABEL:
                _require(payload, cursor, 12, "Application Extension header")
                if payload[cursor] != 11:
                    raise GifStructureError("GIF Application Extension block size is not 11")
                identifier = payload[cursor + 1 : cursor + 12]
                if identifier not in ADMITTED_APPLICATION_IDENTIFIERS:
                    raise GifStructureError(
                        f"GIF Application Extension is not admitted: {identifier!r}"
                    )
                cursor, _, first = _skip_sub_blocks(payload, cursor + 12, "Application Extension")
                if identifier in LOOPING_APPLICATION_IDENTIFIERS:
                    if loop_count is not None:
                        raise GifStructureError("GIF has more than one looping Application Extension")
                    if len(first) != 3 or first[0] != 1:
                        raise GifStructureError("GIF looping Application Extension is malformed")
                    loop_count = struct.unpack("<H", first[1:3])[0]
                application_extensions.append(identifier.decode("ascii"))
            elif label == COMMENT_LABEL:
                cursor, _, _ = _skip_sub_blocks(payload, cursor, "Comment Extension")
                comment_count += 1
            elif label == PLAIN_TEXT_LABEL:
                _require(payload, cursor, 13, "Plain Text Extension header")
                if payload[cursor] != 12:
                    raise GifStructureError("GIF Plain Text Extension block size is not 12")
                cursor, _, _ = _skip_sub_blocks(payload, cursor + 13, "Plain Text Extension")
                plain_text_count += 1
                pending_control = None
            else:
                raise GifStructureError(f"GIF extension label 0x{label:02x} is not admitted")
            continue
        if introducer == IMAGE_SEPARATOR:
            offset = cursor
            _require(payload, cursor, 10, "image descriptor")
            left, top, frame_width, frame_height, image_packed = struct.unpack(
                "<HHHHB", payload[cursor + 1 : cursor + 10]
            )
            cursor += 10
            if not frame_width or not frame_height:
                raise GifStructureError("GIF image has a zero dimension")
            if left + frame_width > width or top + frame_height > height:
                raise GifStructureError("GIF image lies outside the logical screen")
            if image_packed & 0x18:
                raise GifStructureError("GIF image descriptor reserved bits are set")
            local_entries = 0
            if image_packed & 0x80:
                local_entries = _colour_table_entries(image_packed)
                _require(payload, cursor, 3 * local_entries, "local colour table")
                cursor += 3 * local_entries
            table_entries = local_entries or global_entries
            if not table_entries:
                raise GifStructureError("GIF image has neither a local nor a global colour table")
            _require(payload, cursor, 1, "LZW minimum code size")
            code_size = payload[cursor]
            cursor += 1
            if code_size < 2 or code_size > 8:
                raise GifStructureError("GIF LZW minimum code size is outside 2..8")
            cursor, data_bytes, _ = _skip_sub_blocks(payload, cursor, "image data")
            if not data_bytes:
                raise GifStructureError("GIF image has no LZW data")
            delay, disposal, transparent, user_input = (
                pending_control if pending_control is not None else (None, None, None, False)
            )
            if transparent is not None and transparent >= table_entries:
                raise GifStructureError("GIF transparent index is outside the active colour table")
            frames.append(
                GifFrame(
                    index=len(frames),
                    offset=offset,
                    left=left,
                    top=top,
                    width=frame_width,
                    height=frame_height,
                    interlaced=bool(image_packed & 0x40),
                    local_colour_table_entries=local_entries,
                    lzw_minimum_code_size=code_size,
                    data_sub_block_bytes=data_bytes,
                    delay_centiseconds=delay,
                    disposal_method=disposal,
                    transparent_index=transparent,
                    user_input=user_input,
                )
            )
            pending_control = None
            continue
        raise GifStructureError(f"GIF block introducer 0x{introducer:02x} at byte {cursor} is not admitted")


__all__ = [
    "ADMITTED_APPLICATION_IDENTIFIERS",
    "GIF_SIGNATURES",
    "GifFrame",
    "GifStructure",
    "GifStructureError",
    "parse_gif",
]
