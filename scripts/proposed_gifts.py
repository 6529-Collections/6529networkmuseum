#!/usr/bin/env python3
"""Deterministic composition and semantic checks for proposed-gift records."""

from __future__ import annotations

import stat
from pathlib import Path, PurePosixPath
from typing import Any


REGISTER_PATH = Path("records/proposed-gifts/register.json")
MAX_WAVE_PART_CHARACTERS = 25_000


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

    proposal_ids = [row.get("proposal_id") for row in rows if isinstance(row, dict)]
    if len(proposal_ids) != len(set(proposal_ids)):
        issues.append("proposed-gift register contains duplicate proposal IDs")

    proposed_root = (root / "records/proposed-gifts").resolve()
    wave_status_by_record_status = {
        "draft": "not_submitted",
        "not_submitted": "not_submitted",
        "open": "open",
        "selected_for_accession_processing": "selected",
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
            issues.append(f"{proposal_id}: proposal lacks offer or object schedule")
            continue
        if row.get("object_count") != len(objects) or offer.get("object_count") != len(objects):
            issues.append(f"{proposal_id}: object count does not join across register, offer, and schedule")
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
                issues.append(f"{proposal_id}: object schedule contains a non-object entry")
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
            issues.append(f"{proposal_id}: duplicate chain object in schedule")
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
                "selected_for_accession_processing": "WINNER",
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
        for part in parts:
            if not isinstance(part, dict):
                issues.append(f"{proposal_id}: Wave Storm contains a non-object part")
                continue
            role = part.get("role")
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
                    content = source.read_text(encoding="utf-8")
                    if len(content) > MAX_WAVE_PART_CHARACTERS:
                        issues.append(f"{proposal_id}: Storm part {part.get('part_number')} exceeds {MAX_WAVE_PART_CHARACTERS} characters")
                    if role in {"resolution", "synthesis"}:
                        section = markdown_section(content, "Resolution")
                        if section is None:
                            issues.append(f"{proposal_id}: {role} part lacks an exact Resolution section")
                        else:
                            resolution_sections.append(section)
            media = part.get("media")
            if role == "work":
                object_id = part.get("candidate_object_id")
                work_ids.append(object_id)
                obj = objects_by_id.get(object_id)
                if not isinstance(obj, dict):
                    issues.append(f"{proposal_id}: Storm work part references an unscheduled object")
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
            elif part.get("candidate_object_id") is not None or media not in ([], None):
                issues.append(f"{proposal_id}: non-work Storm part carries object media or identity")
        expected_roles = ["resolution", *(["work"] * len(object_ids)), "synthesis"]
        actual_roles = [part.get("role") for part in parts if isinstance(part, dict)]
        if actual_roles != expected_roles:
            issues.append(f"{proposal_id}: Storm roles must be resolution, scheduled works, then synthesis")
        if work_ids != object_ids:
            issues.append(f"{proposal_id}: Storm work parts must match the object schedule exactly and in order")
        if len(source_paths) != len(set(source_paths)):
            issues.append(f"{proposal_id}: Storm parts reuse a Markdown source path")
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
