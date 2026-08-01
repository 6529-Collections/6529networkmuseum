"""RFC 8785-compatible canonical JSON for the Museum's constrained I-JSON profile.

The public record profile permits JSON objects, arrays, strings, booleans, null,
and safe integers only. Rejecting floating point values keeps the release format
portable while remaining a valid RFC 8785/I-JSON subset.
"""

from __future__ import annotations

import json
import math
from typing import Any

MAX_SAFE_INTEGER = 9007199254740991


def _validate(value: Any, path: str = "$", *, key_context: bool = False) -> None:
    if value is None or isinstance(value, bool) or isinstance(value, str):
        if isinstance(value, str) and any(0xD800 <= ord(char) <= 0xDFFF for char in value):
            raise ValueError(f"surrogate code point is not valid I-JSON at {path}")
        return
    if isinstance(value, int) and not isinstance(value, bool):
        if abs(value) > MAX_SAFE_INTEGER:
            raise ValueError(f"integer outside I-JSON safe range at {path}")
        return
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError(f"non-finite number at {path}")
        raise TypeError(f"floating point values are not allowed in museum-i-json-v1 at {path}")
    if isinstance(value, list):
        for index, item in enumerate(value):
            _validate(item, f"{path}[{index}]")
        return
    if isinstance(value, dict):
        for key, item in value.items():
            if not isinstance(key, str):
                raise TypeError(f"object key is not a string at {path}")
            _validate(key, f"{path}.{key}", key_context=True)
            _validate(item, f"{path}.{key}")
        return
    raise TypeError(f"unsupported JSON value {type(value).__name__} at {path}")


def _string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), allow_nan=False)


def _encode(value: Any) -> str:
    if value is None:
        return "null"
    if value is True:
        return "true"
    if value is False:
        return "false"
    if isinstance(value, str):
        return _string(value)
    if isinstance(value, int) and not isinstance(value, bool):
        return str(value)
    if isinstance(value, list):
        return "[" + ",".join(_encode(item) for item in value) + "]"
    if isinstance(value, dict):
        # RFC 8785 sorts property names by their UTF-16 code-unit sequences.
        keys = sorted(value, key=lambda key: key.encode("utf-16-be"))
        return "{" + ",".join(_string(key) + ":" + _encode(value[key]) for key in keys) + "}"
    raise TypeError(f"unsupported JSON value {type(value).__name__}")


def canonicalize(value: Any) -> bytes:
    _validate(value)
    return _encode(value).encode("utf-8")
