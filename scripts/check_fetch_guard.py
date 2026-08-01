#!/usr/bin/env python3
"""Reject unmediated network and command-line fetches in every Python file."""

from __future__ import annotations

import argparse
import ast
import re
import sys
from pathlib import Path


APPROVED_MODULE = Path("scripts/safe_fetch.py")
NETWORK_IMPORT_ROOTS = {"requests", "httpx", "aiohttp"}
NETWORK_IMPORTS = {"socket", "urllib.request", "http.client"}
SOCKET_ATTRIBUTES = {
    "accept",
    "connect",
    "connect_ex",
    "create_connection",
    "create_server",
    "fromfd",
    "getaddrinfo",
    "gethostbyname",
    "gethostbyname_ex",
    "getnameinfo",
    "socket",
}
SUBPROCESS_CALLS = {"run", "call", "check_call", "check_output", "Popen"}
COMMAND_FETCH_WORDS = re.compile(
    r"(?i)(?:^|[^a-z0-9])(?:curl|wget|powershell|pwsh|invoke-webrequest|invoke-restmethod|bitsadmin|certutil)(?:[^a-z0-9]|$)"
)


def dotted_name(node: ast.AST) -> str | None:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        parent = dotted_name(node.value)
        return f"{parent}.{node.attr}" if parent else node.attr
    return None


def resolve_alias(name: str | None, aliases: dict[str, str]) -> str:
    if not name:
        return ""
    root, separator, rest = name.partition(".")
    mapped = aliases.get(root, root)
    return mapped + (separator + rest if separator else "")


def _network_import(module: str) -> bool:
    return module in NETWORK_IMPORTS or module.split(".", 1)[0] in NETWORK_IMPORT_ROOTS


def _string_literals(node: ast.AST) -> list[str]:
    return [child.value for child in ast.walk(node) if isinstance(child, ast.Constant) and isinstance(child.value, str)]


def _safe_static_subprocess_call(node: ast.Call) -> bool:
    if not node.args:
        return False
    command = node.args[0]
    if not isinstance(command, (ast.List, ast.Tuple)):
        return False
    literals = _string_literals(command)
    if any(COMMAND_FETCH_WORDS.search(value) for value in literals):
        return False
    # A list/tuple with a statically visible interpreter or ordinary command
    # is inspectable. Dynamic command objects are fail-closed above.
    return bool(literals or any(dotted_name(child) == "sys.executable" for child in ast.walk(command)))


def scan_file(path: Path, root: Path) -> list[str]:
    relative = path.relative_to(root)
    if relative == APPROVED_MODULE:
        return []
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(relative))
    except (OSError, SyntaxError, UnicodeDecodeError) as exc:
        return [f"{relative}: cannot parse Python source: {exc}"]

    aliases: dict[str, str] = {}
    violations: list[str] = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for imported in node.names:
                local = imported.asname or imported.name.split(".", 1)[0]
                aliases[local] = imported.name
                if _network_import(imported.name):
                    violations.append(f"{relative}:{node.lineno}: unmediated network import {imported.name}")
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            for imported in node.names:
                if imported.name == "*":
                    if _network_import(module):
                        violations.append(f"{relative}:{node.lineno}: wildcard network import {module}")
                    continue
                local = imported.asname or imported.name
                qualified = f"{module}.{imported.name}" if module else imported.name
                aliases[local] = qualified
                if _network_import(module) or _network_import(qualified):
                    violations.append(f"{relative}:{node.lineno}: unmediated network import {qualified}")

    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        qualified = resolve_alias(dotted_name(node.func), aliases)
        root = qualified.split(".", 1)[0]
        if qualified in {"importlib.import_module", "builtins.__import__", "__import__"}:
            literals = _string_literals(node)
            if not literals or any(_network_import(value) for value in literals) or qualified in {"builtins.__import__", "__import__"}:
                violations.append(f"{relative}:{node.lineno}: dynamic module loading is not allowed: {qualified}")
        elif root in NETWORK_IMPORT_ROOTS:
            violations.append(f"{relative}:{node.lineno}: unmediated HTTP client call {qualified}")
        elif qualified in {"urllib.urlopen", "urllib.request.urlopen", "urllib.request.urlretrieve"} or qualified.endswith(".urlopen"):
            violations.append(f"{relative}:{node.lineno}: unmediated URL opener {qualified}")
        elif qualified in {"http.client.HTTPConnection", "http.client.HTTPSConnection"}:
            violations.append(f"{relative}:{node.lineno}: unmediated HTTP connection {qualified}")
        elif root == "socket" and qualified.rsplit(".", 1)[-1] in SOCKET_ATTRIBUTES:
            violations.append(f"{relative}:{node.lineno}: unmediated raw socket call {qualified}")
        elif qualified in {"os.system", "os.popen", "os.spawnl", "os.spawnle", "os.spawnlp", "os.spawnlpe", "os.spawnv", "os.spawnve", "os.spawnvp", "os.spawnvpe"}:
            violations.append(f"{relative}:{node.lineno}: shell/process invocation is not allowed: {qualified}")
        elif root == "subprocess" and qualified.rsplit(".", 1)[-1] in SUBPROCESS_CALLS:
            if not _safe_static_subprocess_call(node):
                violations.append(f"{relative}:{node.lineno}: dynamic or network subprocess command is not allowed: {qualified}")
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
