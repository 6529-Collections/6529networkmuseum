#!/usr/bin/env python3
"""Deterministic composition and semantic checks for proposed-gift records."""

from __future__ import annotations

import hashlib
import json
import re
import stat
import struct
from datetime import datetime
from pathlib import Path, PurePosixPath
from typing import Any


REGISTER_PATH = Path("records/proposed-gifts/register.json")
MAX_WAVE_PART_UTF16_CODE_UNITS = 25_000
MAX_WAVE_PART_UTF8_BYTES = 65_535
MAX_WAVE_STORM_UTF16_CODE_UNITS = 50_000
MAX_WAVE_STORM_MEDIA_FILES = 8
WAVE_COVER_DIMENSION = 1_600
MARKDOWN_LIST_OR_TABLE_LINE = re.compile(r"^(?:\s*(?:[-+*]|\d+[.)])\s+|\s*\|)")
PROPOSED_GIFT_CURRENT_VIEW_NAMES = {"proposal.json", "wave-storm.json"}
GOVERNED_SNAPSHOT_ROOTS = {"policies", "records", "docs", "governance", "schemas", "specs"}
SHA256_VALUE = re.compile(r"^sha256:[0-9a-f]{64}$")
SOURCE_COMMIT = re.compile(r"^[0-9a-f]{40}$")
IDENTITY_DISCRIMINATORS = (
    "$schema",
    "record_type",
    "schema_profile",
    "proposal_id",
    "register_id",
)
DOMAIN_IDENTIFIERS = ("proposal_id", "register_id")


def utf16_code_units(value: str) -> int:
    """Return the JavaScript string length used by the Wave clients and API."""
    return len(value.encode("utf-16-le")) // 2


def utf8_byte_length(value: str) -> int:
    """Return the UTF-8 transport size of an exact Wave part."""
    return len(value.encode("utf-8"))


def safe_relative_path(value: object) -> PurePosixPath | None:
    if (
        not isinstance(value, str)
        or not value
        or "\\" in value
        or ":" in value
        or any(ord(character) < 32 or 0xD800 <= ord(character) <= 0xDFFF for character in value)
    ):
        return None
    path = PurePosixPath(value)
    if path.is_absolute() or any(part in {"", ".", ".."} for part in path.parts):
        return None
    return path


def markdown_section(content: str, heading: str) -> str | None:
    marker = f"## {heading}"
    lines = content.splitlines()
    try:
        start = lines.index(marker) + 1
    except ValueError:
        return None
    end = next((index for index in range(start, len(lines)) if lines[index].startswith("## ")), len(lines))
    section = "\n".join(lines[start:end]).strip()
    return section or None


def markdown_has_ambiguous_soft_break(content: str) -> bool:
    """Return true when public Wave prose relies on an ambiguous soft break."""
    previous: str | None = None
    in_fence = False
    for line in content.splitlines():
        stripped = line.strip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
            previous = None
            continue
        if in_fence or not stripped:
            previous = None
            continue
        if previous is not None:
            previous_is_list_or_table = bool(MARKDOWN_LIST_OR_TABLE_LINE.match(previous))
            current_is_list_or_table = bool(MARKDOWN_LIST_OR_TABLE_LINE.match(line))
            if not (previous_is_list_or_table and current_is_list_or_table):
                return True
        previous = line
    return False


def png_profile(path: Path) -> tuple[int, int, int, int, bool]:
    """Read the PNG IHDR and report whether an embedded sRGB profile exists."""
    content = path.read_bytes()
    if len(content) < 33 or content[:8] != b"\x89PNG\r\n\x1a\n" or content[12:16] != b"IHDR":
        raise ValueError("not a PNG")
    width, height, bit_depth, color_type, compression, filtering, interlace = struct.unpack(
        ">IIBBBBB", content[16:29]
    )
    if compression != 0 or filtering != 0 or interlace not in {0, 1}:
        raise ValueError("unsupported PNG header")
    offset = 8
    chunks: set[bytes] = set()
    while offset + 12 <= len(content):
        length = struct.unpack(">I", content[offset : offset + 4])[0]
        end = offset + 12 + length
        if end > len(content):
            raise ValueError("truncated PNG chunk")
        chunks.add(content[offset + 4 : offset + 8])
        offset = end
        if b"IEND" in chunks:
            break
    if b"IEND" not in chunks:
        raise ValueError("missing PNG end marker")
    return width, height, bit_depth, color_type, bool({b"iCCP", b"sRGB"} & chunks)


def path_has_reparse_point(base: Path, relative: PurePosixPath) -> bool:
    current = base
    for part in relative.parts:
        current = current / part
        if not current.exists() and not current.is_symlink():
            continue
        metadata = current.lstat()
        attributes = getattr(metadata, "st_file_attributes", 0)
        if current.is_symlink() or attributes & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0):
            return True
    return False


def resolve_candidate_file(candidate_dir: Path, value: object) -> Path | None:
    relative = safe_relative_path(value)
    if relative is None or path_has_reparse_point(candidate_dir, relative):
        return None
    try:
        target = (candidate_dir / Path(*relative.parts)).resolve()
    except (OSError, ValueError):
        return None
    if not target.is_relative_to(candidate_dir.resolve()) or not target.is_file():
        return None
    return target


def compose_voter_dossier(candidate_dir: Path, package: dict[str, Any]) -> str:
    """Compose the exact human-readable dossier from ordered Storm source parts."""
    sections: list[str] = []
    for part in package.get("parts", []):
        relative = safe_relative_path(part.get("markdown_path")) if isinstance(part, dict) else None
        if relative is None:
            raise ValueError("invalid Storm markdown path")
        if path_has_reparse_point(candidate_dir, relative):
            raise ValueError(f"Storm markdown path crosses a link or reparse point: {relative}")
        source = (candidate_dir / Path(*relative.parts)).resolve()
        if not source.is_relative_to(candidate_dir.resolve()) or not source.is_file():
            raise ValueError(f"missing or escaping Storm markdown path: {relative}")
        sections.append(source.read_text(encoding="utf-8").strip())
    if not sections:
        raise ValueError("Storm package has no parts")
    return "\n\n---\n\n".join(sections) + "\n"


def _control_time(value: object) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo is not None and parsed.utcoffset() is not None else None


def _normalized_sha256(path: Path) -> str:
    raw = path.read_bytes()
    normalized = raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return "sha256:" + hashlib.sha256(normalized).hexdigest()


def _proposed_gift_current_views(root: Path, loaded: dict[Path, object]) -> list[tuple[Path, dict[str, Any]]]:
    proposed_root = (root / "records/proposed-gifts").resolve()
    register_path = (root / REGISTER_PATH).resolve()
    views: list[tuple[Path, dict[str, Any]]] = []
    for path, record in loaded.items():
        if not isinstance(record, dict):
            continue
        resolved = path.resolve()
        if resolved == register_path:
            views.append((resolved, record))
            continue
        if not resolved.is_relative_to(proposed_root) or resolved.name not in PROPOSED_GIFT_CURRENT_VIEW_NAMES:
            continue
        if resolved.parent.parent == proposed_root:
            views.append((resolved, record))
    return sorted(views, key=lambda item: item[0].as_posix())


def proposed_gift_revision_lineage_issues(root: Path, loaded: dict[Path, object]) -> list[str]:
    """Verify append-only lineage for every proposed-gift current-view record."""
    issues: list[str] = []
    root = root.resolve()
    for current_path, current in _proposed_gift_current_views(root, loaded):
        relative_current = current_path.relative_to(root).as_posix()
        control = current.get("record_control")
        if not isinstance(control, dict) or "revision" not in control:
            continue
        current_revision = control.get("revision")
        history = current.get("amendment_history")
        if not isinstance(current_revision, int) or current_revision < 1:
            issues.append(f"{relative_current}: current revision must be a positive integer")
            continue
        current_constructed_at = _control_time(
            control.get("constructor", {}).get("constructed_at")
            if isinstance(control.get("constructor"), dict)
            else None
        )
        if current_constructed_at is None:
            issues.append(f"{relative_current}: current constructor timestamp is missing or not timezone-aware")
        if current_revision == 1 and history in (None, []):
            continue
        current_domain_identifiers = [
            key
            for key in DOMAIN_IDENTIFIERS
            if key in current and isinstance(current.get(key), str) and bool(current.get(key))
        ]
        if not current_domain_identifiers:
            issues.append(
                f"{relative_current}: current view must contain at least one non-empty domain identifier (proposal_id or register_id)"
            )
        if not isinstance(history, list) or len(history) != current_revision - 1:
            issues.append(f"{relative_current}: amendment history count must equal current revision minus one")
            continue
        history_revisions = [item.get("revision") if isinstance(item, dict) else None for item in history]
        if history_revisions != list(range(1, current_revision)):
            issues.append(f"{relative_current}: amendment history revisions must be unique, increasing, and prior to the current revision")
        for index, entry in enumerate(history):
            if not isinstance(entry, dict):
                issues.append(f"{relative_current}: amendment-history entry {index + 1} is not an object")
                continue
            revision = entry.get("revision")
            snapshot_value = entry.get("prior_snapshot_path")
            snapshot_relative = safe_relative_path(snapshot_value)
            if snapshot_relative is None or not snapshot_relative.parts or snapshot_relative.parts[0] not in GOVERNED_SNAPSHOT_ROOTS:
                issues.append(f"{relative_current}: amendment-history entry {index + 1} has an unsafe prior snapshot path")
                continue
            if path_has_reparse_point(root, snapshot_relative):
                issues.append(f"{relative_current}: amendment-history entry {index + 1} snapshot path crosses a link or reparse point")
                continue
            snapshot_path = (root / Path(*snapshot_relative.parts)).resolve()
            if not snapshot_path.is_relative_to(root) or not snapshot_path.is_file():
                issues.append(f"{relative_current}: amendment-history entry {index + 1} prior snapshot is missing")
                continue
            if not isinstance(entry.get("prior_source_commit"), str) or not SOURCE_COMMIT.fullmatch(entry["prior_source_commit"]):
                issues.append(f"{relative_current}: amendment-history entry {index + 1} has no 40-hex prior source commit")
            if entry.get("supersedes") != entry.get("prior_payload_sha256"):
                issues.append(f"{relative_current}: amendment-history entry {index + 1} supersedes and prior payload hash differ")
            expected_hashes = (entry.get("supersedes"), entry.get("prior_payload_sha256"))
            actual_hash = _normalized_sha256(snapshot_path)
            if actual_hash not in expected_hashes or any(not isinstance(value, str) or not SHA256_VALUE.fullmatch(value) or value != actual_hash for value in expected_hashes):
                issues.append(f"{relative_current}: amendment-history entry {index + 1} prior snapshot LF hash does not match both recorded hashes")
            try:
                snapshot = json.loads(snapshot_path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n").decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError):
                issues.append(f"{relative_current}: amendment-history entry {index + 1} prior snapshot is not UTF-8 JSON")
                continue
            if not isinstance(snapshot, dict):
                issues.append(f"{relative_current}: amendment-history entry {index + 1} prior snapshot is not a JSON object")
                continue
            # A snapshot is the exact prior payload, not a relocated live
            # document. Its `$schema` value therefore remains an immutable
            # identity token from that payload and is not rebased to the
            # snapshot's storage directory.
            for identity_key in IDENTITY_DISCRIMINATORS:
                if identity_key in current and (
                    identity_key not in snapshot or snapshot[identity_key] != current[identity_key]
                ):
                    issues.append(
                        f"{relative_current}: amendment-history entry {index + 1} identity binding mismatch for {identity_key}"
                    )
            snapshot_control = snapshot.get("record_control")
            snapshot_revision = snapshot_control.get("revision") if isinstance(snapshot_control, dict) else None
            if snapshot_revision != revision:
                issues.append(f"{relative_current}: amendment-history entry {index + 1} snapshot revision does not match its history revision")
            snapshot_constructed_at = _control_time(snapshot_control.get("constructor", {}).get("constructed_at") if isinstance(snapshot_control, dict) and isinstance(snapshot_control.get("constructor"), dict) else None)
            superseded_at = _control_time(entry.get("superseded_at"))
            if superseded_at is None:
                issues.append(f"{relative_current}: amendment-history entry {index + 1} has no timezone-aware supersession time")
            if snapshot_constructed_at is None:
                issues.append(
                    f"{relative_current}: amendment-history entry {index + 1} prior snapshot constructor timestamp is missing or not timezone-aware"
                )
            elif superseded_at is not None and snapshot_constructed_at >= superseded_at:
                issues.append(f"{relative_current}: prior snapshot is not logically older than its supersession")
            if current_constructed_at is not None and superseded_at is not None and current_constructed_at < superseded_at:
                issues.append(f"{relative_current}: current constructor predates its amendment")
            snapshot_history = snapshot.get("amendment_history") if isinstance(snapshot, dict) else None
            if revision == 1 and snapshot_history not in (None, []):
                issues.append(f"{relative_current}: revision-one prior snapshot contains amendment history")
            elif isinstance(revision, int) and revision > 1:
                prior_revisions = [item.get("revision") if isinstance(item, dict) else None for item in snapshot_history] if isinstance(snapshot_history, list) else []
                if prior_revisions != list(range(1, revision)):
                    issues.append(f"{relative_current}: prior snapshot history is not logically older and complete")
    return issues


def proposed_gift_issues(root: Path, loaded: dict[Path, object]) -> list[str]:
    """Return semantic errors that JSON Schema cannot express across files."""
    issues: list[str] = []
    register_path = (root / REGISTER_PATH).resolve()
    if not register_path.exists():
        proposed_root = root / "records/proposed-gifts"
        if proposed_root.exists() and any(proposed_root.glob("*/proposal.json")):
            return ["proposed-gift records exist without the required register"]
        return issues
    register = loaded.get(register_path)
    if not isinstance(register, dict):
        return ["proposed-gift register is not a JSON object"]
    rows = register.get("proposals")
    if not isinstance(rows, list):
        return ["proposed-gift register has no proposal rows"]

    issues.extend(proposed_gift_revision_lineage_issues(root, loaded))

    proposal_ids = [row.get("proposal_id") for row in rows if isinstance(row, dict)]
    if len(proposal_ids) != len(set(proposal_ids)):
        issues.append("proposed-gift register contains duplicate proposal IDs")

    proposed_root = (root / "records/proposed-gifts").resolve()
    wave_status_by_record_status = {
        "draft": "not_submitted",
        "not_submitted": "not_submitted",
        "open": "open",
        "selected": "selected",
        "closed_without_selection": "closed_without_selection",
        "withdrawn": "withdrawn",
        "superseded": "withdrawn",
    }
    declared_record_paths: set[Path] = set()

    for row in rows:
        if not isinstance(row, dict):
            issues.append("proposed-gift register contains a non-object row")
            continue
        proposal_id = row.get("proposal_id", "<unknown>")
        relative_record = safe_relative_path(row.get("proposal_record"))
        if relative_record is None:
            issues.append(f"{proposal_id}: invalid proposal_record path")
            continue
        if path_has_reparse_point(proposed_root, relative_record):
            issues.append(f"{proposal_id}: proposal_record crosses a link or reparse point")
            continue
        record_path = (proposed_root / Path(*relative_record.parts)).resolve()
        if not record_path.is_relative_to(proposed_root) or not record_path.is_file():
            issues.append(f"{proposal_id}: missing or escaping proposal_record")
            continue
        declared_record_paths.add(record_path)
        proposal = loaded.get(record_path)
        if not isinstance(proposal, dict):
            issues.append(f"{proposal_id}: proposal_record is not a loaded JSON object")
            continue

        for field in ("proposal_id", "title", "status"):
            if row.get(field) != proposal.get(field):
                issues.append(f"{proposal_id}: register/proposal {field} mismatch")
        offer = proposal.get("offer")
        objects = proposal.get("objects")
        if not isinstance(offer, dict) or not isinstance(objects, list):
            issues.append(f"{proposal_id}: proposal lacks offer or object list")
            continue
        if row.get("object_count") != len(objects) or offer.get("object_count") != len(objects):
            issues.append(f"{proposal_id}: object count does not join across register, offer, and object list")
        if row.get("donor_public_credit") != offer.get("donor_public_credit"):
            issues.append(f"{proposal_id}: donor public credit mismatch")
        expected_wave_status = wave_status_by_record_status.get(proposal.get("status"))
        if row.get("wave_status") != expected_wave_status:
            issues.append(f"{proposal_id}: register Wave status does not match proposal status")

        object_ids: list[object] = []
        token_keys: list[tuple[object, object, object]] = []
        objects_by_id: dict[object, dict[str, Any]] = {}
        chain_states: list[str] = []
        contract_observation = proposal.get("contract_observation")
        contract_point = None
        if isinstance(contract_observation, dict):
            contract_point = (
                contract_observation.get("block_number"),
                contract_observation.get("block_hash"),
            )
        else:
            issues.append(f"{proposal_id}: missing contract observation")
        for obj in objects:
            if not isinstance(obj, dict):
                issues.append(f"{proposal_id}: object list contains a non-object entry")
                continue
            object_id = obj.get("candidate_object_id")
            object_ids.append(object_id)
            objects_by_id[object_id] = obj
            if not isinstance(object_id, str) or not object_id.startswith(f"{proposal_id}.OBJ-"):
                issues.append(f"{proposal_id}: candidate object ID uses a foreign proposal namespace")
            token_id = obj.get("token_id")
            if not isinstance(token_id, str) or (token_id != "0" and token_id.startswith("0")):
                issues.append(f"{proposal_id}: token ID is not canonically encoded for {object_id}")
            token_keys.append((obj.get("chain_id"), obj.get("contract"), obj.get("token_id")))
            expected_caip19 = f"{obj.get('chain_id')}/erc721:{obj.get('contract')}/{obj.get('token_id')}"
            if obj.get("caip19") != expected_caip19:
                issues.append(f"{proposal_id}: CAIP-19 mismatch for {object_id}")
            observation = obj.get("chain_observation")
            if not isinstance(observation, dict):
                issues.append(f"{proposal_id}: missing chain observation for {object_id}")
                continue
            state = observation.get("status")
            chain_states.append(str(state))
            point_fields = [
                observation.get("block_number"),
                observation.get("block_hash"),
                observation.get("owner"),
                observation.get("token_uri"),
                observation.get("approval"),
            ]
            if state == "pending_finalized_block_observation" and any(value is not None for value in point_fields):
                issues.append(f"{proposal_id}: pending chain observation is partially populated for {object_id}")
            if state == "verified_at_finalized_block":
                if any(value is None for value in point_fields):
                    issues.append(f"{proposal_id}: verified chain observation is incomplete for {object_id}")
                metadata = obj.get("metadata")
                if isinstance(metadata, dict) and observation.get("token_uri") != metadata.get("uri"):
                    issues.append(f"{proposal_id}: finalized tokenURI does not match fixed metadata for {object_id}")
                if contract_point != (observation.get("block_number"), observation.get("block_hash")):
                    issues.append(f"{proposal_id}: object and contract observations use different finalized blocks")

            provenance = obj.get("provenance")
            transfers = provenance.get("transfers") if isinstance(provenance, dict) else None
            if not isinstance(transfers, list) or len(transfers) != 3 or not all(
                isinstance(transfer, dict) for transfer in transfers
            ):
                issues.append(f"{proposal_id}: incomplete three-event provenance for {object_id}")
            else:
                expected_roles = ["mint", "foundation_market_escrow", "current_owner_transfer"]
                if [transfer.get("role") for transfer in transfers] != expected_roles:
                    issues.append(f"{proposal_id}: provenance roles are missing or out of order for {object_id}")
                tx_hashes = [transfer.get("tx_hash") for transfer in transfers]
                if len(tx_hashes) != len(set(tx_hashes)):
                    issues.append(f"{proposal_id}: provenance repeats a transaction hash for {object_id}")
                if transfers[0].get("from") != "0x0000000000000000000000000000000000000000":
                    issues.append(f"{proposal_id}: provenance does not begin with mint for {object_id}")
                if transfers[0].get("to") != transfers[1].get("from") or transfers[1].get("to") != transfers[2].get("from"):
                    issues.append(f"{proposal_id}: provenance transfer chain is discontinuous for {object_id}")
                if transfers[2].get("to") != observation.get("owner"):
                    issues.append(f"{proposal_id}: provenance does not terminate at observed owner for {object_id}")
                blocks = [transfer.get("block_number") for transfer in transfers]
                if not all(isinstance(block, int) for block in blocks) or blocks != sorted(blocks):
                    issues.append(f"{proposal_id}: provenance blocks are not ordered for {object_id}")
                elif isinstance(observation.get("block_number"), int) and blocks[-1] > observation["block_number"]:
                    issues.append(f"{proposal_id}: provenance postdates the finalized observation for {object_id}")

        if len(object_ids) != len(set(object_ids)):
            issues.append(f"{proposal_id}: duplicate candidate object ID")
        if len(token_keys) != len(set(token_keys)):
            issues.append(f"{proposal_id}: duplicate chain object in object list")
        if proposal.get("status") not in {"draft", "not_submitted"} and any(
            state != "verified_at_finalized_block" for state in chain_states
        ):
            issues.append(f"{proposal_id}: submitted or decided proposal lacks complete finalized-block observations")
        verified_points = {
            (obj["chain_observation"].get("block_number"), obj["chain_observation"].get("block_hash"))
            for obj in objects
            if isinstance(obj, dict)
            and isinstance(obj.get("chain_observation"), dict)
            and obj["chain_observation"].get("status") == "verified_at_finalized_block"
        }
        if len(verified_points) > 1:
            issues.append(f"{proposal_id}: objects were not observed at one finalized Ethereum block")

        wave_authority = proposal.get("wave_authority")
        if not isinstance(wave_authority, dict):
            issues.append(f"{proposal_id}: missing Wave authority")
            continue
        drop = wave_authority.get("proposal_drop")
        if isinstance(drop, dict):
            drop_id_missing = drop.get("drop_id") is None
            serial_missing = drop.get("serial_no") is None
            null_drop = drop_id_missing and serial_missing
            if drop_id_missing != serial_missing:
                issues.append(f"{proposal_id}: Wave drop ID and serial number must be present or null together")
            if proposal.get("status") in {"draft", "not_submitted"} and not null_drop:
                issues.append(f"{proposal_id}: unsubmitted proposal claims a Wave drop")
            if proposal.get("status") not in {"draft", "not_submitted"} and null_drop:
                issues.append(f"{proposal_id}: submitted or decided proposal lacks a Wave drop identity")
            expected_drop_status = {
                "draft": "not_submitted",
                "not_submitted": "not_submitted",
                "open": "PARTICIPATORY",
                "selected": "WINNER",
                "closed_without_selection": "PARTICIPATORY",
                "withdrawn": "WITHDRAWN",
                "superseded": "WITHDRAWN",
            }.get(proposal.get("status"))
            if drop.get("status") != expected_drop_status:
                issues.append(f"{proposal_id}: live Wave drop status does not match proposal state")

        documents = proposal.get("documents")
        if not isinstance(documents, dict):
            issues.append(f"{proposal_id}: missing document map")
            continue
        resolved_documents: dict[str, Path] = {}
        for label, value in documents.items():
            relative = safe_relative_path(value)
            if relative is None:
                issues.append(f"{proposal_id}: invalid {label} document path")
                continue
            if path_has_reparse_point(root, relative):
                issues.append(f"{proposal_id}: {label} document crosses a link or reparse point")
                continue
            try:
                target = (root / Path(*relative.parts)).resolve()
            except (OSError, ValueError):
                issues.append(f"{proposal_id}: unreadable {label} document path")
                continue
            if not target.is_relative_to(root.resolve()) or not target.is_file():
                issues.append(f"{proposal_id}: missing or escaping {label} document")
                continue
            resolved_documents[label] = target

        candidate_dir = record_path.parent.resolve()
        expected_documents = {
            "voter_dossier": candidate_dir / "public/voter-dossier.md",
            "wave_storm_package": candidate_dir / "wave-storm.json",
            "wave_resolution": candidate_dir / "public/wave-resolution.md",
        }
        for label, expected in expected_documents.items():
            if resolved_documents.get(label) != expected:
                issues.append(f"{proposal_id}: {label} does not use the canonical candidate path")

        package_path = resolved_documents.get("wave_storm_package")
        package = loaded.get(package_path) if package_path else None
        if not isinstance(package, dict):
            issues.append(f"{proposal_id}: Wave Storm package is not a loaded JSON object")
            continue
        if package.get("proposal_id") != proposal_id:
            issues.append(f"{proposal_id}: Wave Storm package proposal ID mismatch")
        if package.get("status") != proposal.get("status"):
            issues.append(f"{proposal_id}: Wave Storm package status does not match proposal status")
        if package.get("drop_title") != proposal.get("title"):
            issues.append(f"{proposal_id}: Wave Storm drop title does not match the proposed gift title")
        target_wave = package.get("target_wave")
        if not isinstance(target_wave, dict) or any(
            target_wave.get(field) != wave_authority.get(field)
            for field in ("wave_id", "wave_name", "wave_type", "credit_type", "credit_scope")
        ):
            issues.append(f"{proposal_id}: Wave Storm target does not match observed Wave authority")

        parts = package.get("parts")
        if not isinstance(parts, list) or not parts:
            issues.append(f"{proposal_id}: Wave Storm has no parts")
            continue
        if [part.get("part_number") for part in parts if isinstance(part, dict)] != list(range(1, len(parts) + 1)):
            issues.append(f"{proposal_id}: Wave Storm parts are not contiguous and ordered")
        if not isinstance(parts[0], dict) or parts[0].get("role") != "resolution":
            issues.append(f"{proposal_id}: Wave Storm must open with the resolution")
        if not isinstance(parts[-1], dict) or parts[-1].get("role") != "synthesis":
            issues.append(f"{proposal_id}: Wave Storm must close with the synthesis and repeated resolution")

        work_ids: list[object] = []
        source_paths: list[Path] = []
        resolution_sections: list[str] = []
        total_storm_utf16_code_units = 0
        total_storm_utf8_bytes = 0
        total_storm_media_files = 0
        computed_part_metrics: list[dict[str, int]] = []
        for part in parts:
            if not isinstance(part, dict):
                issues.append(f"{proposal_id}: Wave Storm contains a non-object part")
                continue
            role = part.get("role")
            part_utf16_code_units: int | None = None
            part_utf8_bytes: int | None = None
            relative = safe_relative_path(part.get("markdown_path"))
            if relative is None:
                issues.append(f"{proposal_id}: invalid Storm markdown path")
            else:
                if path_has_reparse_point(candidate_dir, relative):
                    issues.append(f"{proposal_id}: Storm markdown path crosses a link or reparse point")
                    continue
                try:
                    source = (candidate_dir / Path(*relative.parts)).resolve()
                except (OSError, ValueError):
                    issues.append(f"{proposal_id}: unreadable Storm markdown path")
                    source = candidate_dir / "__invalid__"
                if not source.is_relative_to(candidate_dir) or not source.is_file():
                    issues.append(f"{proposal_id}: missing or escaping Storm markdown source {relative}")
                else:
                    source_paths.append(source)
                    source_bytes = source.read_bytes()
                    try:
                        content = source_bytes.decode("utf-8")
                    except UnicodeDecodeError:
                        issues.append(f"{proposal_id}: Storm part {part.get('part_number')} is not valid UTF-8")
                        content = ""
                    if source_bytes.startswith(b"\xef\xbb\xbf"):
                        issues.append(f"{proposal_id}: Storm part {part.get('part_number')} contains a UTF-8 byte-order mark")
                    if b"\r" in source_bytes:
                        issues.append(f"{proposal_id}: Storm part {part.get('part_number')} does not use LF-only line endings")
                    if not source_bytes.endswith(b"\n"):
                        issues.append(f"{proposal_id}: Storm part {part.get('part_number')} lacks the required final LF")
                    part_utf16_code_units = utf16_code_units(content)
                    part_utf8_bytes = len(source_bytes)
                    total_storm_utf16_code_units += part_utf16_code_units
                    total_storm_utf8_bytes += part_utf8_bytes
                    if part_utf16_code_units > MAX_WAVE_PART_UTF16_CODE_UNITS:
                        issues.append(
                            f"{proposal_id}: Storm part {part.get('part_number')} exceeds "
                            f"{MAX_WAVE_PART_UTF16_CODE_UNITS} UTF-16 code units"
                        )
                    if part_utf8_bytes > MAX_WAVE_PART_UTF8_BYTES:
                        issues.append(
                            f"{proposal_id}: Storm part {part.get('part_number')} exceeds "
                            f"{MAX_WAVE_PART_UTF8_BYTES} UTF-8 bytes"
                        )
                    if markdown_has_ambiguous_soft_break(content):
                        issues.append(
                            f"{proposal_id}: Storm part {part.get('part_number')} contains an ambiguous Markdown soft break"
                        )
                    if role in {"resolution", "synthesis"}:
                        section = markdown_section(content, "Resolution")
                        if section is None:
                            issues.append(f"{proposal_id}: {role} part lacks an exact Resolution section")
                        else:
                            resolution_sections.append(section)
            media = part.get("media")
            if isinstance(media, list):
                total_storm_media_files += len(media)
                if part_utf16_code_units is not None and part_utf8_bytes is not None:
                    computed_part_metrics.append(
                        {
                            "part_number": part.get("part_number"),
                            "utf16_code_units": part_utf16_code_units,
                            "utf8_bytes": part_utf8_bytes,
                            "media_count": len(media),
                        }
                    )
            else:
                issues.append(f"{proposal_id}: Storm part {part.get('part_number')} media is not a list")
            if role == "work":
                object_id = part.get("candidate_object_id")
                work_ids.append(object_id)
                obj = objects_by_id.get(object_id)
                if not isinstance(obj, dict):
                    issues.append(f"{proposal_id}: Storm work part references an object outside the gift")
                elif not isinstance(media, list) or len(media) != 1 or not isinstance(media[0], dict):
                    issues.append(f"{proposal_id}: Storm work part must carry exactly one image")
                elif not isinstance(obj.get("image"), dict) or media[0].get("uri") != obj["image"].get("uri"):
                    issues.append(f"{proposal_id}: Storm work image does not match the fixed object image")
                else:
                    image = obj["image"]
                    rights = obj.get("rights")
                    if media[0].get("media_type") != image.get("media_type"):
                        issues.append(f"{proposal_id}: Storm work media type does not match the fixed object image")
                    if not isinstance(rights, dict) or media[0].get("rights_label") != rights.get("license"):
                        issues.append(f"{proposal_id}: Storm work rights label does not match the object record")
                    notice = rights.get("copyright_notice") if isinstance(rights, dict) else None
                    expected_credit = (
                        notice.removesuffix(" All Rights Reserved") + "."
                        if isinstance(notice, str)
                        else None
                    )
                    credit_line = media[0].get("credit_line")
                    if (
                        not isinstance(credit_line, str)
                        or not isinstance(expected_credit, str)
                        or not credit_line.endswith(expected_credit)
                        or obj.get("artist") not in credit_line
                    ):
                        issues.append(f"{proposal_id}: Storm work credit does not match the object rights record")
            elif role == "resolution":
                if part.get("candidate_object_id") is not None:
                    issues.append(f"{proposal_id}: resolution Storm part carries object identity")
                if not isinstance(media, list) or len(media) != 1 or not isinstance(media[0], dict):
                    issues.append(f"{proposal_id}: resolution Storm part must carry exactly one cover image")
                else:
                    cover = media[0]
                    cover_path = resolve_candidate_file(candidate_dir, cover.get("asset_path"))
                    source_asset_path = resolve_candidate_file(candidate_dir, cover.get("source_asset_path"))
                    if cover_path is None:
                        issues.append(f"{proposal_id}: cover image path is missing, unsafe, or escaping")
                    else:
                        cover_bytes = cover_path.read_bytes()
                        if cover.get("byte_length") != len(cover_bytes):
                            issues.append(f"{proposal_id}: cover image byte length does not match the retained asset")
                        if cover.get("sha256") != hashlib.sha256(cover_bytes).hexdigest():
                            issues.append(f"{proposal_id}: cover image SHA-256 does not match the retained asset")
                        try:
                            width, height, bit_depth, color_type, has_srgb_profile = png_profile(cover_path)
                        except ValueError as exc:
                            issues.append(f"{proposal_id}: invalid cover PNG: {exc}")
                        else:
                            if (width, height) != (WAVE_COVER_DIMENSION, WAVE_COVER_DIMENSION):
                                issues.append(f"{proposal_id}: cover PNG is not 1600 by 1600 pixels")
                            if (cover.get("width"), cover.get("height")) != (width, height):
                                issues.append(f"{proposal_id}: cover dimensions do not match the retained asset")
                            if bit_depth != 8 or color_type != 2:
                                issues.append(f"{proposal_id}: cover PNG must be opaque 8-bit truecolor")
                            if not has_srgb_profile:
                                issues.append(f"{proposal_id}: cover PNG lacks an embedded sRGB profile")
                    if source_asset_path is None:
                        issues.append(f"{proposal_id}: cover source path is missing, unsafe, or escaping")
                    else:
                        source_bytes = source_asset_path.read_bytes()
                        if cover.get("source_sha256") != hashlib.sha256(source_bytes).hexdigest():
                            issues.append(f"{proposal_id}: cover source SHA-256 does not match the retained asset")
            elif role == "synthesis":
                if part.get("candidate_object_id") is not None or media not in ([], None):
                    issues.append(f"{proposal_id}: synthesis Storm part carries object media or identity")
        expected_roles = ["resolution", *(["work"] * len(object_ids)), "synthesis"]
        actual_roles = [part.get("role") for part in parts if isinstance(part, dict)]
        if actual_roles != expected_roles:
            issues.append(f"{proposal_id}: Storm roles must be resolution, gift works, then synthesis")
        if work_ids != object_ids:
            issues.append(f"{proposal_id}: Storm work parts must match the gift's object list exactly and in order")
        if len(source_paths) != len(set(source_paths)):
            issues.append(f"{proposal_id}: Storm parts reuse a Markdown source path")
        if total_storm_utf16_code_units > MAX_WAVE_STORM_UTF16_CODE_UNITS:
            issues.append(
                f"{proposal_id}: Storm exceeds {MAX_WAVE_STORM_UTF16_CODE_UNITS} total UTF-16 code units"
            )
        if total_storm_media_files > MAX_WAVE_STORM_MEDIA_FILES:
            issues.append(
                f"{proposal_id}: Storm exceeds {MAX_WAVE_STORM_MEDIA_FILES} total media files"
            )
        publication_profile = package.get("publication_profile")
        if not isinstance(publication_profile, dict):
            issues.append(f"{proposal_id}: Storm lacks a publication profile")
        else:
            target_observation = publication_profile.get("target_observation")
            if not isinstance(target_observation, dict) or any(
                target_observation.get(field) != wave_authority.get(field)
                for field in ("winning_threshold", "winning_threshold_min_duration_ms")
            ):
                issues.append(f"{proposal_id}: Storm target observation does not match Wave authority")
            if publication_profile.get("part_metrics") != computed_part_metrics:
                issues.append(f"{proposal_id}: Storm publication part metrics do not match the exact source edition")
            expected_totals = {
                "utf16_code_units": total_storm_utf16_code_units,
                "utf8_bytes": total_storm_utf8_bytes,
                "media_count": total_storm_media_files,
            }
            if publication_profile.get("totals") != expected_totals:
                issues.append(f"{proposal_id}: Storm publication totals do not match the exact source edition")
        if len(resolution_sections) == 2 and resolution_sections[0] != resolution_sections[1]:
            issues.append(f"{proposal_id}: opening and closing Resolution sections differ")

        dossier_path = resolved_documents.get("voter_dossier")
        if dossier_path:
            try:
                expected_dossier = compose_voter_dossier(candidate_dir, package)
            except ValueError as exc:
                issues.append(f"{proposal_id}: cannot compose voter dossier: {exc}")
            else:
                if dossier_path.read_text(encoding="utf-8") != expected_dossier:
                    issues.append(f"{proposal_id}: generated voter dossier is stale")

    orphan_records = {
        path.resolve() for path in proposed_root.glob("*/proposal.json")
    } - declared_record_paths
    for orphan in sorted(orphan_records):
        issues.append(f"unregistered proposed-gift record: {orphan.relative_to(root.resolve())}")
    return issues
