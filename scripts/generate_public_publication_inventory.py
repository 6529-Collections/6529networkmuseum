#!/usr/bin/env python3
"""Generate/check the closed visitor-publication inventory used by release C.

The repository manifest is the whole governed control-plane inventory.  This
file is deliberately narrower: it names only the visitor corpus and the
small set of control documents required to assemble it.  The visitor corpus
bundle is a separate artifact generated from this inventory and is never an
entry in it.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import stat
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from Crypto.Hash import keccak
from jsonschema import Draft202012Validator, FormatChecker

from canonical import canonicalize


ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "schemas" / "public-publication-inventory.json"
PUBLICATION_BUNDLE_PATH = "records/publication/visitor-corpus-bundle-v1.json"
PUBLICATION_INVENTORY_SCHEMA = "https://6529networkmuseum.org/schemas/public-publication-inventory-v1.json"
PUBLICATION_BUNDLE_SCHEMA = "https://6529networkmuseum.org/schemas/public-publication-bundle-v1.json"
JCS_ID = "0x886c7c89c308c459ca8a626e0ef36a5ea9f4c7a7b56aaf86c71a2ddf3b4f9044"
MAX_BUNDLE_BYTES = 8_000_000
TEXT_EXTENSIONS = {".json", ".md", ".txt", ".py", ".yml", ".yaml", ".svg", ".gitattributes", ".gitignore"}
MEDIA_EXTENSIONS = {".webp", ".png", ".jpg", ".jpeg", ".gif", ".avif", ".pdf", ".svg"}
PUBLIC_MEDIA_RIGHTS_STATUSES = {"cleared", "cleared_with_conditions"}
EXCLUDED_PUBLIC_MARKDOWN = {
    # Superseded accessibility and delivery records remain in the source
    # repository but are not visitor manuscripts. The current accessibility
    # JSON, publication boundary, and withdrawal amendment carry the active
    # public state without exposing obsolete derivative instructions.
    "records/programs/6529NM-AP-01/public/accessibility-amendment.md",
    "records/programs/6529NM-AP-01/public/accessibility-amendment-2026-08-08-002.md",
    "records/programs/6529NM-AP-01/public/accessibility-amendment-2026-08-08-003.md",
    "records/programs/6529NM-AP-01/public/accessibility-amendment-2026-08-08-004.md",
    "records/programs/6529NM-AP-01/public/accessibility-amendment-2026-08-08-006.md",
    "records/programs/6529NM-AP-01/public/publication-authority-amendment-2026-08-08-005.md",
}

# Proposed-gift ballots and their supporting Storm manuscripts are public
# historical evidence, not current Museum manuscripts. They remain in the
# governed repository and complete record manifest, while the visitor bundle
# admits only current scholarship below public/scholarship/. This general
# boundary prevents a future proposal from silently publishing voting copy,
# superseded descriptions, or restricted media links as collection scholarship.
PROPOSED_GIFT_DECISION_HISTORY = re.compile(
    r"^records/proposed-gifts/[^/]+/public/(?:"
    r"wave-storm/|status-amendments/|voter-dossier\.md$|wave-resolution\.md$)"
)

# These are the visitor-facing and frontend-contract manuscripts that do not
# live below records/**/public. The records/public tree is derived subject to
# the explicit historical-evidence boundaries above.
EXPLICIT_MANUSCRIPTS = (
    "CONTRIBUTING.md",
    "docs/curatorial-publication-standard.md",
    "docs/onchain-design.md",
    "docs/onchain-transition.md",
    "docs/open-museum.md",
    "docs/programs/keys-and-gates.md",
    "docs/public-entity-publication-contract.md",
    "docs/public-information-architecture.md",
    "docs/public-museum-experience-standard.md",
)

# These JSON controls are required by the frontend assembler.  They are
# assembly documents, not source manuscripts and not the inventory itself.
ASSEMBLY_CONTROL_PATHS = (
    "records/proposed-gifts/6529NM-PG-2026-001/public/scholarship/machine/media-source-continuity-amendment.json",
    "schemas/common.schema.json",
    "schemas/controlled-vocabularies.json",
    "schemas/controlled-vocabularies.schema.json",
    "schemas/public-entity-common.schema.json",
    "schemas/public-entity-identity-inventory.json",
    "schemas/public-entity-identity-inventory.schema.json",
    "schemas/public-entity.schema.json",
    "schemas/public-relation-identity-inventory.json",
    "schemas/public-relation-identity-inventory.schema.json",
    "schemas/public-relation.schema.json",
    "schemas/public-route-compatibility.json",
    "schemas/public-route-compatibility.schema.json",
    "schemas/public-publication-inventory.schema.json",
    "schemas/public-publication-bundle.schema.json",
    "schemas/publication-catalog-pointer.schema.json",
    "schemas/publication-catalog.schema.json",
    "schemas/record-envelope.schema.json",
    "schemas/wave-status-observation.schema.json",
)

# Accessibility descriptions and the active responsive manifest are safe
# visitor-facing controls. Delivery still fails closed: MEDIA_REFERENCE rights
# activate each Work, and the manifest may supply only that Work's exact sibling
# derivatives under the reviewed display authority.
MEDIA_SOURCE_MANIFEST_PATHS = (
    "media/programs/6529NM-AP-01/accessibility.json",
    "records/programs/6529NM-AP-01/public/presentation-manifest.json",
    "records/accessions/6529NM.2026.002/public/presentation-manifest.json",
)


class InventoryError(ValueError):
    """Raised when the closed visitor inventory is incomplete or unsafe."""


def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise InventoryError(f"duplicate JSON object key: {key!r}")
        result[key] = value
    return result


def strict_load(data: bytes | str) -> Any:
    return json.loads(data, object_pairs_hook=reject_duplicate_keys)


def schema_dependency_paths(root: Path, seed_paths: set[str]) -> set[str]:
    """Return the complete local schema dependency closure for seed paths."""

    schema_documents: dict[str, dict[str, Any]] = {}
    schema_id_paths: dict[str, str] = {}
    for path in sorted((root / "schemas").glob("*.schema.json")):
        relative = relative_path(root, path)
        document = strict_load(path.read_bytes())
        if not isinstance(document, dict):
            raise InventoryError(f"schema must be a JSON object: {relative}")
        schema_documents[relative] = document
        schema_id = document.get("$id")
        if isinstance(schema_id, str):
            base_id = schema_id.split("#", 1)[0]
            prior = schema_id_paths.get(base_id)
            if prior is not None and prior != relative:
                raise InventoryError(
                    f"duplicate local schema $id {base_id!r}: {prior}, {relative}"
                )
            schema_id_paths[base_id] = relative

    closure: set[str] = set()
    pending = sorted(
        path for path in seed_paths if path.startswith("schemas/") and path.endswith(".schema.json")
    )
    while pending:
        relative = pending.pop()
        if relative in closure:
            continue
        document = schema_documents.get(relative)
        if document is None:
            raise InventoryError(f"schema dependency does not exist: {relative}")
        closure.add(relative)
        nodes: list[Any] = [document]
        while nodes:
            node = nodes.pop()
            if isinstance(node, dict):
                reference = node.get("$ref")
                if isinstance(reference, str) and not reference.startswith("#"):
                    base_id = reference.split("#", 1)[0]
                    target = schema_id_paths.get(base_id)
                    if target is None:
                        raise InventoryError(
                            f"unresolved local schema dependency {reference!r} in {relative}"
                        )
                    if target not in closure:
                        pending.append(target)
                nodes.extend(node.values())
            elif isinstance(node, list):
                nodes.extend(node)
    return closure


def keccak256(data: bytes) -> bytes:
    digest = keccak.new(digest_bits=256)
    digest.update(data)
    return digest.digest()


def sha256_prefixed(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def relative_path(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def validate_path(path: str) -> None:
    if (
        not isinstance(path, str)
        or not path
        or path.startswith("/")
        or "\\" in path
        or "?" in path
        or "#" in path
        or any(part in {"", ".", ".."} for part in path.split("/"))
        or any(part.casefold() in {".git", "release-artifacts"} for part in path.split("/"))
        or any(char in path for char in "*?[]{}!")
    ):
        raise InventoryError(f"unsafe publication path: {path!r}")


def require_file(root: Path, relative: str) -> Path:
    validate_path(relative)
    candidate = root / Path(*relative.split("/"))
    current = root
    for part in Path(*relative.split("/" )).parts:
        current = current / part
        info = os.lstat(current)
        if stat.S_ISLNK(info.st_mode) or getattr(info, "st_file_attributes", 0) & 0x400:
            raise InventoryError(f"publication path may not cross a symlink/reparse point: {relative}")
    path = candidate.resolve()
    if not path.is_relative_to(root.resolve()) or not path.is_file():
        raise InventoryError(f"publication path is missing or not a regular file: {relative}")
    return path


def public_record_paths(root: Path) -> list[str]:
    paths = {
        relative_path(root, path)
        for path in (root / "records").rglob("*.md")
        if "/public/" in relative_path(root, path)
        and relative_path(root, path) not in EXCLUDED_PUBLIC_MARKDOWN
        and not PROPOSED_GIFT_DECISION_HISTORY.match(relative_path(root, path))
    }
    paths.update(EXPLICIT_MANUSCRIPTS)
    return sorted(paths)


def legacy_required_paths(root: Path) -> dict[str, set[str]]:
    """Closed source-owned sets required by the current visitor assembler."""

    casey_root = root / "records/accessions/6529NM.2026.001"
    casey = {relative_path(root, path) for path in casey_root.rglob("*.json")}
    institutional = {relative_path(root, path) for path in (root / "records/institutional-practice").rglob("*") if path.is_file()}
    data_architecture = {"docs/data-architecture.md"}
    data_architecture.update(relative_path(root, path) for path in (root / "docs/data-architecture").rglob("*") if path.is_file())
    rights = {relative_path(root, path) for path in (root / "docs/rights").rglob("*") if path.is_file()}
    open_and_founding = {relative_path(root, path) for path in (root / "policies").glob("*.md") if path.is_file()}
    open_and_founding.update({"docs/open-museum.md", "docs/casey-accession-control.md", "docs/institutional-source-inventory.json"})
    return {
        "legacy_casey_required_paths": casey,
        "institutional_practice_required_paths": institutional,
        "data_architecture_required_paths": data_architecture,
        "museum_rights_required_paths": rights,
        "open_and_founding_required_paths": open_and_founding,
    }


def _load_record(root: Path, relative: str) -> dict[str, Any]:
    value = strict_load(require_file(root, relative).read_bytes())
    if not isinstance(value, dict):
        raise InventoryError(f"JSON source is not an object: {relative}")
    return value


def _active_media_repository_paths(root: Path) -> set[str]:
    """Collect every local path referenced by active media projections."""

    paths: set[str] = set()
    entities = root / "records/entities"
    for path in sorted(entities.glob("*.json")):
        value = _load_record(root, relative_path(root, path))
        payload = value.get("payload")
        profile = payload.get("profile") if isinstance(payload, dict) else None
        if not isinstance(payload, dict) or not isinstance(profile, dict) or profile.get("profile_type") != "MEDIA_REFERENCE":
            continue
        if payload.get("entity_status") in {"archived", "superseded", "inactive"}:
            continue
        media = profile.get("media")
        if (
            not isinstance(media, dict)
            or media.get("visual") is not True
            or media.get("publication_boundary") not in {"public_derivative", "historical_wave_proposal_context", "public_graphic"}
            or not isinstance(media.get("rights"), dict)
            or media["rights"].get("status") not in PUBLIC_MEDIA_RIGHTS_STATUSES
        ):
            continue
        locator = media.get("source_locator") if isinstance(media, dict) else None
        repository_path = locator.get("repository_path") if isinstance(locator, dict) else None
        if isinstance(repository_path, str):
            require_file(root, repository_path)
            paths.add(repository_path)
    return paths


def _program_media_paths(root: Path) -> set[str]:
    """Collect all responsive derivatives admitted by the program manifest."""

    manifest_relative = "records/programs/6529NM-AP-01/media-manifest.json"
    manifest = _load_record(root, manifest_relative)
    paths: set[str] = set()
    for item in manifest.get("items", []):
        if not isinstance(item, dict):
            continue
        presentation = item.get("presentation")
        derivatives = presentation.get("derivatives", []) if isinstance(presentation, dict) else []
        for derivative in derivatives:
            if not isinstance(derivative, dict):
                continue
            repository_path = derivative.get("repository_path")
            if not isinstance(repository_path, str):
                continue
            require_file(root, repository_path)
            if Path(repository_path).suffix.casefold() not in MEDIA_EXTENSIONS:
                raise InventoryError(f"program media derivative is not a governed media extension: {repository_path}")
            paths.add(repository_path)
    media_root = root / "media/programs/6529NM-AP-01"
    actual = {
        relative_path(root, path)
        for path in media_root.rglob("*")
        if path.is_file() and path.suffix.casefold() in MEDIA_EXTENSIONS
    }
    if actual != paths:
        missing = sorted(paths - actual)
        extra = sorted(actual - paths)
        raise InventoryError(f"program media manifest is not an exact local asset inventory; missing={missing}, extra={extra}")
    return paths


def _accession_media_paths(root: Path) -> set[str]:
    """Collect the accession's exact reviewed responsive derivative inventory."""

    manifest_relative = "records/accessions/6529NM.2026.002/public/presentation-manifest.json"
    manifest = _load_record(root, manifest_relative)
    delivery = manifest.get("delivery")
    if (
        not isinstance(delivery, dict)
        or delivery.get("status") != "approved_for_contextual_museum_display"
        or delivery.get("authority_path")
        != "records/accessions/6529NM.2026.002/public/web-presentation-authority.md"
    ):
        return set()
    paths: set[str] = set()
    for item in manifest.get("items", []):
        if not isinstance(item, dict):
            continue
        presentation = item.get("presentation")
        derivatives = (
            presentation.get("derivatives", [])
            if isinstance(presentation, dict)
            else []
        )
        for derivative in derivatives:
            repository_path = (
                derivative.get("repository_path")
                if isinstance(derivative, dict)
                else None
            )
            if isinstance(repository_path, str):
                require_file(root, repository_path)
                paths.add(repository_path)
    media_root = root / "media/accessions/6529NM.2026.002"
    actual = {
        relative_path(root, path)
        for path in media_root.rglob("*.webp")
        if path.is_file()
    }
    if actual != paths:
        raise InventoryError("accession media manifest is not an exact local asset inventory")
    return paths


def _approved_responsive_program_media_paths(
    root: Path, active_paths: set[str]
) -> set[str]:
    """Expand an approved program image to its exact responsive derivative set.

    The active MEDIA_REFERENCE remains the rights gate. The program manifest
    may add only sibling derivatives of that same governed item, and only while
    its reviewed display authority is the active delivery status.
    """

    manifest_relative = "records/programs/6529NM-AP-01/media-manifest.json"
    manifest = _load_record(root, manifest_relative)
    delivery = manifest.get("delivery")
    if (
        not isinstance(delivery, dict)
        or delivery.get("status") != "approved_by_reviewed_display_authority"
        or not isinstance(delivery.get("authority_record_id"), str)
    ):
        return set()

    approved: set[str] = set()
    for item in manifest.get("items", []):
        if not isinstance(item, dict):
            continue
        presentation = item.get("presentation")
        derivatives = presentation.get("derivatives", []) if isinstance(presentation, dict) else []
        item_paths = {
            derivative.get("repository_path")
            for derivative in derivatives
            if isinstance(derivative, dict)
            and isinstance(derivative.get("repository_path"), str)
        }
        if item_paths & active_paths:
            approved.update(item_paths)
    return approved


def _entry(path: str, kind: str, role: str) -> dict[str, Any]:
    activation_mode = "atomic" if role == "assembly_document" else "deferred_on_demand"
    return {
        "path": path,
        "kind": kind,
        "delivery_role": role,
        "required_in_catalog": True,
        "activation_mode": activation_mode,
    }


def _entries(root: Path) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    seen: set[str] = set()

    def add(value: dict[str, Any]) -> None:
        if value["path"] not in seen:
            entries.append(value)
            seen.add(value["path"])

    for path in sorted((root / "records/entities").glob("*.json")):
        add(_entry(relative_path(root, path), "public_entity_record", "assembly_document"))
    for path in sorted((root / "records/relations").glob("*.json")):
        add(_entry(relative_path(root, path), "public_relation_record", "assembly_document"))
    # The status observation is the closed public graph's current lifecycle
    # source. The full seven-part publication receipt and its accessibility
    # amendment remain complete-manifest evidence only: both retain historical
    # photographic locators that are not part of the visitor delivery surface.
    add(
        _entry(
            "records/proposed-gifts/6529NM-PG-2026-001/wave-status-observation-2026-08-08.json",
            "wave_observation",
            "assembly_document",
        )
    )
    for relative in public_record_paths(root):
        add(_entry(relative, "public_curatorial_manuscript", "assembly_document"))
    control_paths = set(ASSEMBLY_CONTROL_PATHS)
    vocabularies = strict_load((root / "schemas" / "controlled-vocabularies.json").read_bytes())
    schema_paths = vocabularies.get("schema_paths")
    if not isinstance(schema_paths, dict) or not schema_paths:
        raise InventoryError("controlled vocabularies must declare schema_paths")
    for record_type, filename in schema_paths.items():
        if not isinstance(record_type, str) or not isinstance(filename, str):
            raise InventoryError("controlled vocabulary schema_paths must map strings to strings")
        if Path(filename).name != filename or not filename.endswith(".schema.json"):
            raise InventoryError(f"unsafe controlled vocabulary schema path: {filename!r}")
        relative = f"schemas/{filename}"
        if not (root / relative).is_file():
            raise InventoryError(
                f"controlled vocabulary schema path does not exist: {relative}"
            )
        control_paths.add(relative)
    for required_paths in legacy_required_paths(root).values():
        control_paths.update(required_paths)
    control_paths.update(schema_dependency_paths(root, control_paths))
    for relative in sorted(control_paths):
        add(_entry(relative, "public_assembly_control_document", "assembly_document"))
    for relative in MEDIA_SOURCE_MANIFEST_PATHS:
        add(_entry(relative, "public_media_source_manifest", "assembly_document"))

    # The manifest is an exact responsive inventory, while each active
    # MEDIA_REFERENCE remains the rights gate for its Work. Once one governed
    # derivative is active, the reviewed display authority admits only that
    # item's declared sibling sizes; it cannot activate another Work.
    program_media_paths = _program_media_paths(root)
    all_media_paths = _active_media_repository_paths(root)
    responsive_paths = _approved_responsive_program_media_paths(root, all_media_paths)
    if not responsive_paths.issubset(program_media_paths):
        raise InventoryError("approved responsive media escaped the governed program manifest")
    all_media_paths.update(responsive_paths)
    all_media_paths.update(_accession_media_paths(root))
    for relative in sorted(all_media_paths):
        suffix = Path(relative).suffix.casefold()
        if suffix in MEDIA_EXTENSIONS:
            add(_entry(relative, "approved_public_media", "media_asset"))
        else:
            add(_entry(relative, "public_media_source_manifest", "assembly_document"))
    return sorted(entries, key=lambda item: item["path"])


def generate(root: Path = ROOT) -> dict[str, Any]:
    entries = _entries(root)
    paths = [entry["path"] for entry in entries]
    if paths != sorted(set(paths)):
        raise InventoryError("publication inventory paths must be sorted and unique")
    assembly_paths = [entry["path"] for entry in entries if entry["delivery_role"] == "assembly_document"]
    media_paths = [entry["path"] for entry in entries if entry["delivery_role"] == "media_asset"]
    counts = dict(sorted(Counter(entry["kind"] for entry in entries).items()))
    value = {
        "$schema": PUBLICATION_INVENTORY_SCHEMA,
        "inventory_version": "1.0.0",
        "inventory_id": "6529NM_PUBLIC_VISITOR_CORPUS",
        "scope": "visitor_publication_corpus",
        "assembler": {
            "required_paths": assembly_paths,
            "activation_mode": "atomic",
            "bundle_path": PUBLICATION_BUNDLE_PATH,
        },
        "bundle": {
            "path": PUBLICATION_BUNDLE_PATH,
            "schema": PUBLICATION_BUNDLE_SCHEMA,
            "required_in_catalog": True,
            "activation_mode": "atomic",
            "max_serialized_bytes": MAX_BUNDLE_BYTES,
        },
        "entries": entries,
        "counts": counts,
        "required_source_sets": {
            name: sorted(paths)
            for name, paths in sorted(legacy_required_paths(root).items())
        },
    }
    body = canonicalize(value)
    value["integrity"] = {
        "canonicalization_id": JCS_ID,
        "body_sha256": sha256_prefixed(body),
        "body_keccak256": "0x" + keccak256(body).hex(),
    }
    return value


def validate_inventory(root: Path, value: dict[str, Any], *, require_bundle: bool = False) -> list[str]:
    issues: list[str] = []
    try:
        schema_path = root / "schemas/public-publication-inventory.schema.json"
        schema = strict_load(schema_path.read_bytes())
        Draft202012Validator.check_schema(schema)
        schema_errors = sorted(
            Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(value),
            key=lambda error: list(error.absolute_path),
        )
        issues.extend(f"inventory schema {list(error.absolute_path)}: {error.message}" for error in schema_errors[:20])
        if value.get("$schema") != PUBLICATION_INVENTORY_SCHEMA:
            issues.append("inventory schema identifier is incorrect")
        if value.get("scope") != "visitor_publication_corpus":
            issues.append("inventory scope is not visitor_publication_corpus")
        entries = value.get("entries")
        if not isinstance(entries, list) or not entries:
            return [*issues, "inventory entries are missing"]
        paths = [entry.get("path") if isinstance(entry, dict) else None for entry in entries]
        if paths != sorted(set(paths)):
            issues.append("inventory paths are not sorted and unique")
        counts = Counter()
        assembly: list[str] = []
        media: list[str] = []
        for entry in entries:
            if not isinstance(entry, dict):
                issues.append("inventory entry is not an object")
                continue
            path = entry.get("path")
            try:
                require_file(root, path)
            except (InventoryError, TypeError) as exc:
                issues.append(str(exc))
                continue
            if entry.get("required_in_catalog") is not True:
                issues.append(f"inventory entry is not required_in_catalog: {path}")
            role = entry.get("delivery_role")
            if role == "assembly_document":
                assembly.append(path)
                if Path(path).suffix.casefold() not in TEXT_EXTENSIONS and Path(path).name.casefold() not in {"codeowners"}:
                    issues.append(f"assembly document has unsupported extension: {path}")
                if entry.get("activation_mode") != "atomic":
                    issues.append(f"assembly document has non-atomic activation: {path}")
            elif role == "media_asset":
                media.append(path)
                if Path(path).suffix.casefold() not in MEDIA_EXTENSIONS:
                    issues.append(f"media asset has unsupported extension: {path}")
                if entry.get("activation_mode") != "deferred_on_demand":
                    issues.append(f"media asset is not deferred_on_demand: {path}")
            else:
                issues.append(f"inventory entry has invalid delivery role: {path}")
            counts[entry.get("kind")] += 1
        if value.get("counts") != dict(sorted(counts.items())):
            issues.append("inventory counts do not match entries")
        expected_source_sets = {
            name: sorted(paths)
            for name, paths in sorted(legacy_required_paths(root).items())
        }
        if value.get("required_source_sets") != expected_source_sets:
            issues.append("inventory required_source_sets do not equal the closed source-owned completeness sets")
        else:
            entry_paths = set(paths)
            for name, source_paths in expected_source_sets.items():
                missing = sorted(set(source_paths) - entry_paths)
                if missing:
                    issues.append(f"inventory source set {name} has missing entries: {missing}")
        assembler = value.get("assembler")
        if not isinstance(assembler, dict) or assembler.get("required_paths") != assembly or assembler.get("activation_mode") != "atomic":
            issues.append("assembler.required_paths must equal the complete assembly-document set")
        bundle = value.get("bundle")
        if not isinstance(bundle, dict) or bundle.get("path") != PUBLICATION_BUNDLE_PATH or bundle.get("required_in_catalog") is not True:
            issues.append("inventory bundle binding is invalid")
        if bundle and bundle.get("path") in paths:
            issues.append("bundle must not recursively appear as an inventory entry")
        integrity = value.get("integrity")
        if not isinstance(integrity, dict) or integrity.get("canonicalization_id") != JCS_ID:
            issues.append("inventory integrity canonicalization is invalid")
        else:
            body_value = dict(value)
            body_value.pop("integrity", None)
            body = canonicalize(body_value)
            if integrity.get("body_sha256") != sha256_prefixed(body) or integrity.get("body_keccak256") != "0x" + keccak256(body).hex():
                issues.append("inventory body commitments do not match the canonical inventory")
        if require_bundle:
            try:
                bundle_path = require_file(root, PUBLICATION_BUNDLE_PATH)
                if len(bundle_path.read_bytes()) > MAX_BUNDLE_BYTES:
                    issues.append("visitor corpus bundle exceeds its deterministic byte ceiling")
            except InventoryError as exc:
                issues.append(str(exc))
        expected = generate(root)
        if expected.get("entries") != entries or expected.get("counts") != value.get("counts"):
            issues.append("inventory is not the deterministic projection of active records/manifests")
        # A source-owned completeness check: all current public record manuscripts
        # and explicit frontend-facing manuscripts must be present.
        required_manuscripts = set(public_record_paths(root))
        required_manuscripts.update(EXPLICIT_MANUSCRIPTS)
        actual_manuscripts = {entry.get("path") for entry in entries if entry.get("kind") == "public_curatorial_manuscript"}
        if required_manuscripts != actual_manuscripts:
            issues.append("public manuscript set is incomplete or contains an ungoverned extra")
    except InventoryError as exc:
        issues.append(str(exc))
    return issues


def write(root: Path = ROOT) -> None:
    value = generate(root)
    issues = validate_inventory(root, value)
    if issues:
        raise InventoryError("; ".join(issues))
    output = root / "schemas/public-publication-inventory.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def check(root: Path = ROOT) -> int:
    output = root / "schemas/public-publication-inventory.json"
    if not output.is_file():
        print(f"publication inventory missing: {output}")
        return 1
    try:
        actual = strict_load(output.read_bytes())
        if not isinstance(actual, dict):
            raise InventoryError("publication inventory must be an object")
        issues = validate_inventory(root, actual, require_bundle=True)
    except (OSError, json.JSONDecodeError, InventoryError) as exc:
        print(f"publication inventory check failed: {exc}")
        return 1
    if issues:
        print("publication inventory check failed:")
        print("\n".join(f"- {issue}" for issue in issues))
        return 1
    if actual != generate(root):
        print("publication inventory is stale; regenerate with scripts/generate_public_publication_inventory.py")
        return 1
    print(f"publication inventory is current: {output}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args(argv)
    root = args.root.resolve()
    try:
        if args.check:
            return check(root)
        write(root)
    except (OSError, json.JSONDecodeError, InventoryError) as exc:
        print(f"publication inventory generation failed: {exc}")
        return 1
    print(f"wrote deterministic publication inventory: {root / 'schemas/public-publication-inventory.json'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
