"""Fail-closed admission of GIF bytes as manifested raw public evidence."""

from __future__ import annotations

import hashlib
import io
import json
import struct
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import bootstrap_validate  # noqa: E402
import gif_structure  # noqa: E402


def sub_blocks(data: bytes) -> bytes:
    chunks = [data[index : index + 255] for index in range(0, len(data), 255)]
    return b"".join(bytes([len(chunk)]) + chunk for chunk in chunks) + b"\x00"


def graphic_control(delay: int = 5, transparent: int | None = 1, disposal: int = 1) -> bytes:
    packed = (disposal << 2) | (1 if transparent is not None else 0)
    return b"\x21\xf9\x04" + struct.pack("<BHB", packed, delay, transparent or 0) + b"\x00"


def image_block(left: int = 0, top: int = 0, width: int = 4, height: int = 4, code_size: int = 2) -> bytes:
    descriptor = b"\x2c" + struct.pack("<HHHHB", left, top, width, height, 0)
    return descriptor + bytes([code_size]) + sub_blocks(b"\x8c\x2d\x99\x87\x2a\x1c\xdc\x33\xa0\x02\x75\xec\x95\xfa\xa8\xde")


def make_gif(
    *,
    version: bytes = b"GIF89a",
    width: int = 4,
    height: int = 4,
    blocks: bytes | None = None,
    trailer: bytes = b"\x3b",
) -> bytes:
    screen = struct.pack("<HHBBB", width, height, 0x80 | 0x10, 0, 0)
    colour_table = b"\x00\x00\x00\xff\xff\xff"
    if blocks is None:
        blocks = (
            b"\x21\xff\x0bNETSCAPE2.0\x03\x01\x00\x00\x00"
            + graphic_control()
            + image_block()
            + graphic_control()
            + image_block(1, 1, 2, 2)
        )
    return version + screen + colour_table + blocks + trailer


def comment(text: bytes) -> bytes:
    return b"\x21\xfe" + sub_blocks(text)


class GifStructureParserTests(unittest.TestCase):
    def test_minimal_animation_is_parsed_with_timing_and_loop(self) -> None:
        parsed = gif_structure.parse_gif(make_gif())
        self.assertEqual("GIF89a", parsed.version)
        self.assertEqual(2, parsed.frame_count)
        self.assertEqual(10, parsed.total_delay_centiseconds)
        self.assertEqual(0, parsed.loop_count)
        self.assertEqual(("NETSCAPE2.0",), parsed.application_extensions)
        self.assertEqual(len(make_gif()) - 1, parsed.trailer_offset)

    def test_pillow_animation_matches_pillow_frame_timing_and_loop(self) -> None:
        frames = [Image.new("P", (32, 24), index) for index in range(3)]
        for frame in frames:
            frame.putpalette([0, 0, 0, 255, 0, 153, 0, 153, 153] + [0] * (256 * 3 - 9))
        buffer = io.BytesIO()
        frames[0].save(buffer, format="GIF", save_all=True, append_images=frames[1:], duration=50, loop=0, disposal=1)
        payload = buffer.getvalue()
        parsed = gif_structure.parse_gif(payload)
        with Image.open(io.BytesIO(payload)) as image:
            self.assertEqual(image.n_frames, parsed.frame_count)
            self.assertEqual(image.info.get("loop"), parsed.loop_count)
        self.assertEqual([5] * 3, [frame.delay_centiseconds for frame in parsed.frames])

    def test_structural_mutations_are_rejected(self) -> None:
        valid = make_gif()
        cases = {
            "unknown signature": b"GIF88a" + valid[6:],
            "zero logical screen": make_gif(width=0),
            "missing trailer": valid[:-1],
            "truncated sub-block": valid[: valid.index(b"\x2c") + 14],
            "trailing executable after trailer": valid + b"MZ",
            "trailing ELF after trailer": valid + b"\x7fELF",
            "trailing archive after trailer": valid + b"PK\x03\x04",
            "trailing script after trailer": valid + b"<script>alert(1)</script>",
            "trailing second trailer": valid + b"\x3b",
            "unknown block introducer": make_gif(blocks=b"\x00" + image_block()),
            "unknown extension label": make_gif(blocks=b"\x21\x99" + sub_blocks(b"x") + image_block()),
            "unadmitted application extension": make_gif(
                blocks=b"\x21\xff\x0bEVILAPPS1.0" + sub_blocks(b"payload") + image_block()
            ),
            "malformed looping extension": make_gif(
                blocks=b"\x21\xff\x0bNETSCAPE2.0\x02\x01\x00\x00" + image_block()
            ),
            "graphic control block size": make_gif(
                blocks=b"\x21\xf9\x05\x05\x05\x00\x01\x00\x00" + image_block()
            ),
            "consecutive graphic controls": make_gif(blocks=graphic_control() + graphic_control() + image_block()),
            "dangling graphic control": make_gif(blocks=image_block() + graphic_control()),
            "undefined disposal": make_gif(blocks=graphic_control(disposal=5) + image_block()),
            "transparent index outside table": make_gif(blocks=graphic_control(transparent=9) + image_block()),
            "image outside logical screen": make_gif(blocks=image_block(2, 2, 4, 4)),
            "zero image dimension": make_gif(blocks=image_block(width=0)),
            "LZW code size": make_gif(blocks=image_block(code_size=12)),
            "empty image data": make_gif(
                blocks=b"\x2c" + struct.pack("<HHHHB", 0, 0, 4, 4, 0) + b"\x02\x00"
            ),
            "no image": make_gif(blocks=b""),
            "GIF87a extension": make_gif(version=b"GIF87a"),
        }
        for label, payload in cases.items():
            with self.subTest(label=label):
                with self.assertRaises(gif_structure.GifStructureError):
                    gif_structure.parse_gif(payload)


class GifRawEvidenceAdmissionTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory(prefix="museum-gif-evidence-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.evidence = self.root / "evidence" / "package"
        self.evidence.mkdir(parents=True)
        self.manifest = self.evidence / "manifest.json"

    def write(self, payload: bytes, *, name: str = "raw/source.gif", media_type: str = "image/gif") -> None:
        for existing in sorted(self.evidence.rglob("*"), reverse=True):
            if existing.is_file():
                existing.unlink()
        target = self.evidence / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(payload)
        self.manifest.write_text(
            json.dumps(
                {
                    "hash_algorithm": "sha256",
                    "byte_mode": "raw",
                    "entries": [
                        {
                            "path": name,
                            "byte_mode": "raw",
                            "media_type": media_type,
                            "size": len(payload),
                            "sha256": hashlib.sha256(payload).hexdigest(),
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )

    def admit(self) -> None:
        with patch.object(bootstrap_validate, "ROOT", self.root):
            entries = bootstrap_validate.check_evidence_manifests(
                {self.manifest: json.loads(self.manifest.read_text(encoding="utf-8"))}
            )
            bootstrap_validate.check_public_record_safety(entries)

    def assert_rejected(self) -> None:
        with self.assertRaises(SystemExit):
            self.admit()

    def test_manifest_declared_gif_is_admitted(self) -> None:
        self.assertIn("image/gif", bootstrap_validate.SAFE_BINARY_MEDIA_TYPES)
        self.write(make_gif())
        self.admit()

    def test_structural_and_polyglot_mutations_fail_closed(self) -> None:
        valid = make_gif()
        for payload in (
            valid[:-1],
            valid + b"MZ",
            valid + b"#!/bin/sh\necho unsafe",
            valid + b"PK\x03\x04",
            valid + b"<script>alert(1)</script>",
            b"GIF89b" + valid[6:],
            make_gif(blocks=b"\x21\xff\x0bEVILAPPS1.0" + sub_blocks(b"payload") + image_block()),
        ):
            with self.subTest(payload=payload[-12:]):
                self.write(payload)
                self.assert_rejected()

    def test_media_type_and_signature_must_agree(self) -> None:
        png = b"\x89PNG\r\n\x1a\n" + b"\x00" * 16
        self.write(png)
        self.assert_rejected()
        self.write(make_gif(), name="raw/source.png", media_type="image/png")
        self.assert_rejected()

    def test_executable_suffix_is_rejected(self) -> None:
        self.write(make_gif(), name="raw/source.exe")
        self.assert_rejected()

    def test_credential_shapes_inside_extensions_are_rejected(self) -> None:
        shapes = (
            b"api_key=synthetic-secret-value",
            b"ghp_" + b"a" * 36,
            b"AKIA" + b"A" * 16,
            b"private_key=0x" + b"b" * 64,
            b"-----BEGIN PRIVATE KEY-----",
            b"-----BEGIN OPENSSH PRIVATE KEY-----",
            b"eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxIn0.signature",
            b"C:\\Users\\Administrator\\private.psd",
            "api_key=synthetic-secret-value".encode("utf-16-le"),
            "C:\\Users\\Administrator\\private.psd".encode("utf-16-be"),
        )
        for shape in shapes:
            with self.subTest(shape=shape[:12]):
                payload = make_gif(blocks=comment(shape) + graphic_control() + image_block())
                gif_structure.parse_gif(payload)
                self.write(payload)
                self.assert_rejected()
        xmp = b"\x21\xff\x0bXMP DataXMP" + sub_blocks("PASSWORD=SyntheticSecretValue".encode("utf-16-be")) + image_block()
        gif_structure.parse_gif(make_gif(blocks=xmp))
        self.write(make_gif(blocks=xmp))
        self.assert_rejected()


if __name__ == "__main__":
    unittest.main()
