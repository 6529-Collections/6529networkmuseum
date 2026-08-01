"""RFC 8785-compatible canonical JSON for the Museum's constrained I-JSON profile."""

from __future__ import annotations

import json
import math
from typing import Any

import rfc8785

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
        return
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


def canonicalize(value: Any) -> bytes:
    _validate(value)
    return rfc8785.dumps(value)
