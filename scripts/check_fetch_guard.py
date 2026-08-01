#!/usr/bin/env python3
"""Reject network fetch implementations outside scripts/safe_fetch.py."""

from __future__ import annotations

import argparse
import ast
import sys
from pathlib import Path


APPROVED_MODULE = Path("scripts/safe_fetch.py")
DISALLOWED_IMPORTS = {"requests", "httpx", "aiohttp"}
DISALLOWED_SOCKET_ATTRIBUTES = {
    "accept",
    "connect",
    "connect_ex",
    "create_connection",
    "create_server",
    "getaddrinfo",
    "socket",
}


def dotted_name(node: ast.AST) -> str | None:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        parent = dotted_name(node.value)
        return f"{parent}.{node.attr}" if parent else node.attr
    return None


def is_test_path(relative: Path) -> bool:
    return "tests" in relative.parts


def scan_file(path: Path, root: Path) -> list[str]:
    relative = path.relative_to(root)
    if relative == APPROVED_MODULE or is_test_path(relative):
        return []
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(relative))
    except (OSError, SyntaxError, UnicodeDecodeError) as exc:
        return [f"{relative}: cannot parse Python source: {exc}"]

    violations: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                module = alias.name
                if module.split(".", 1)[0] in DISALLOWED_IMPORTS:
                    violations.append(f"{relative}:{node.lineno}: disallowed HTTP client import {module}")
                if module == "socket":
                    violations.append(f"{relative}:{node.lineno}: raw socket import outside scripts/safe_fetch.py")
                if module == "urllib.request":
                    violations.append(f"{relative}:{node.lineno}: urllib.request import outside scripts/safe_fetch.py")
                if module == "http.client":
                    violations.append(f"{relative}:{node.lineno}: http.client import outside scripts/safe_fetch.py")
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            if module.split(".", 1)[0] in DISALLOWED_IMPORTS:
                violations.append(f"{relative}:{node.lineno}: disallowed HTTP client import {module}")
            if module in {"socket", "urllib.request", "http.client"}:
                violations.append(f"{relative}:{node.lineno}: unmediated network import {module}")
            if module == "urllib" and any(alias.name == "urlopen" for alias in node.names):
                violations.append(f"{relative}:{node.lineno}: urllib.urlopen is not allowed")
        elif isinstance(node, ast.Call):
            name = dotted_name(node.func) or ""
            if name in {"urlopen", "urllib.urlopen", "urllib.request.urlopen", "urllib.request.urlretrieve"}:
                violations.append(f"{relative}:{node.lineno}: unmediated URL opener {name}")
            if name.startswith("socket.") and name.split(".", 1)[1] in DISALLOWED_SOCKET_ATTRIBUTES:
                violations.append(f"{relative}:{node.lineno}: unmediated raw socket call {name}")
            if name in {"http.client.HTTPConnection", "http.client.HTTPSConnection"}:
                violations.append(f"{relative}:{node.lineno}: unmediated HTTP connection {name}")
            if name in {"requests.get", "requests.post", "requests.request", "httpx.get", "httpx.post", "aiohttp.ClientSession"}:
                violations.append(f"{relative}:{node.lineno}: unmediated HTTP client call {name}")
    return violations


def scan_tree(root: Path) -> list[str]:
    violations: list[str] = []
    for path in sorted(root.rglob("*.py")):
        if ".git" in path.parts or any(part in {"__pycache__", ".venv", "venv"} for part in path.parts):
            continue
        violations.extend(scan_file(path, root))
    return violations


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args(argv)
    violations = scan_tree(args.root.resolve())
    if violations:
        for violation in violations:
            print(f"ERROR: {violation}", file=sys.stderr)
        return 1
    print("Network fetch guard passed: only scripts/safe_fetch.py may use approved fetch primitives.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
