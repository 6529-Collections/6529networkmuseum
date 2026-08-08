from __future__ import annotations

import copy
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from canonical import canonicalize  # noqa: E402
from generate_manifest import inventory_paths  # noqa: E402
from migrate_public_entities import build_records  # noqa: E402
from publication_catalog import (  # noqa: E402
    CatalogError,
    _verify_deterministic_promotion_artifacts,
    build_catalog,
    build_pointer,
    check_append_only_catalog,
    keccak256,
    render_json,
    sha256_prefixed,
    validate_catalog,
    validate_pointer,
)
from stream_adapter import (  # noqa: E402
    MUSEUM_JCS_ID,
    STREAM_IMPLEMENTATION_PATH,
    STREAM_INTERFACE_PATH,
    STREAM_RECORD_HASH_DOMAIN,
    STREAM_SOURCE_COMMIT,
    ZERO32,
    derive_collection_record_hash,
    encode_collection_record_abi,
    encode_collection_record_tuple_body,
    museum_envelope_to_stream_record,
    museum_record_type_to_stream,
    reject_legacy_unsigned_placeholder,
    require_stream_admission,
    stream_record_to_semantic_json,
)


class StreamAdapterTests(unittest.TestCase):
    def museum_envelope(self) -> dict:
        return {
            "recordType": "PUBLIC_ENTITY",
            "subjectId": "0x" + "11" * 32,
            "contentHash": {"algorithm": 1, "digest": "0x" + "22" * 32, "canonicalizationId": MUSEUM_JCS_ID},
            "uri": "https://6529networkmuseum.org/records/entities/6529NM-W-0001.json",
            "schemaId": "0x" + "33" * 32,
            "signatureScheme": ZERO32,
            "signatureHash": {"algorithm": 2, "digest": ZERO32, "canonicalizationId": MUSEUM_JCS_ID},
            "effectiveAt": 1786190000,
        }

    def exact_source_repo(
        self,
        envelope: dict,
        payload: dict,
        *,
        source_path: str = "records/entities/E.json",
    ) -> tuple[tempfile.TemporaryDirectory, Path, str]:
        temporary = tempfile.TemporaryDirectory()
        root = Path(temporary.name)
        record_path = root / Path(*source_path.split("/"))
        record_path.parent.mkdir(parents=True, exist_ok=True)
        record_path.write_bytes(render_json({"envelope": envelope, "payload": payload}))
        manifest_path = root / "release-artifacts/latest/record-manifest.json"
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest_path.write_bytes(render_json({"entries": [{"path": source_path}]}))
        subprocess.run(["git", "init", "-q"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.invalid"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.name", "Stream Adapter Test"], cwd=root, check=True)
        subprocess.run(["git", "add", "."], cwd=root, check=True)
        subprocess.run(["git", "commit", "-qm", "exact source"], cwd=root, check=True)
        commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()
        return temporary, root, commit

    def test_exact_pinned_stream_v2_source_and_authorization_caveat(self) -> None:
        stream_source_root = Path(os.environ.get("STREAM_SOURCE_ROOT", r"D:\repos\6529Stream"))
        resolved_source_commit = subprocess.check_output(
            ["git", "-C", str(stream_source_root), "rev-parse", f"{STREAM_SOURCE_COMMIT}^{{commit}}"], text=True
        ).strip()
        self.assertEqual(resolved_source_commit, STREAM_SOURCE_COMMIT)
        interface = subprocess.check_output(
            ["git", "-C", str(stream_source_root), "show", f"{STREAM_SOURCE_COMMIT}:{STREAM_INTERFACE_PATH}"], text=True
        )
        implementation = subprocess.check_output(
            ["git", "-C", str(stream_source_root), "show", f"{STREAM_SOURCE_COMMIT}:{STREAM_IMPLEMENTATION_PATH}"], text=True
        )
        self.assertIn("struct CollectionRecord", interface)
        self.assertIn('keccak256("6529stream.preservation-record.v2")', implementation)
        self.assertIn("_recordFamilyRegistry.requireRecordWriter", implementation)
        self.assertIn("authorizationClass", interface)
        self.assertEqual(STREAM_RECORD_HASH_DOMAIN, "6529stream.preservation-record.v2")

    def test_unsigned_museum_placeholder_normalizes_to_stream_empty_hashref(self) -> None:
        stream_record = museum_envelope_to_stream_record(self.museum_envelope(), allow_logical_uri=True)
        self.assertEqual(stream_record["signatureScheme"], ZERO32)
        self.assertEqual(stream_record["signatureHash"], {"algorithm": 0, "digest": "0x", "canonicalizationId": ZERO32})
        reject_legacy_unsigned_placeholder(stream_record)
        self.assertEqual(stream_record_to_semantic_json(stream_record), stream_record)

    def test_adapter_requires_exact_immutable_source_binding_by_default(self) -> None:
        with self.assertRaises(ValueError):
            museum_envelope_to_stream_record(self.museum_envelope())
        for uri in (
            "https://example.invalid/record.json",
            "https://github.com/6529-Collections/6529networkmuseum/blob/main/records/entities/E.json",
            "https://raw.githubusercontent.com/6529-Collections/6529networkmuseum/main/records/entities/E.json",
        ):
            envelope = self.museum_envelope()
            envelope["uri"] = uri
            with self.assertRaises(ValueError):
                museum_envelope_to_stream_record(envelope, allow_logical_uri=True)

    def test_exact_commit_path_uri_and_payload_commitment(self) -> None:
        payload = {"record_id": "E", "value": "stable"}
        envelope = self.museum_envelope()
        envelope["contentHash"] = {"algorithm": 1, "digest": "0x" + keccak256(canonicalize(payload)).hex(), "canonicalizationId": MUSEUM_JCS_ID}
        temporary, source_root, source_commit = self.exact_source_repo(envelope, payload)
        try:
            record = museum_envelope_to_stream_record(
                envelope,
                source_commit=source_commit,
                source_path="records/entities/E.json",
                source_payload=payload,
                source_root=source_root,
            )
            self.assertEqual(record["uri"], "https://raw.githubusercontent.com/6529-Collections/6529networkmuseum/" + source_commit + "/records/entities/E.json")
            with self.assertRaises(ValueError):
                museum_envelope_to_stream_record(
                    envelope,
                    source_commit=source_commit,
                    source_path="records/entities/../E.json",
                    source_payload=payload,
                    source_root=source_root,
                )
            with self.assertRaises(ValueError):
                museum_envelope_to_stream_record(
                    envelope,
                    source_commit=source_commit,
                    source_path="records/entities/E.json",
                    source_payload={"changed": True},
                    source_root=source_root,
                )
        finally:
            temporary.cleanup()

    def test_legacy_unsigned_placeholder_cannot_pass_through(self) -> None:
        record = museum_envelope_to_stream_record(self.museum_envelope(), allow_logical_uri=True)
        record["signatureHash"] = {"algorithm": 2, "digest": ZERO32, "canonicalizationId": MUSEUM_JCS_ID}
        with self.assertRaises(ValueError):
            reject_legacy_unsigned_placeholder(record)

    def test_record_type_pins_are_exhaustive_for_generated_record_families(self) -> None:
        records = build_records()
        record_types = {record["payload"]["record_type"] for record in records.values()}
        for record_type in record_types:
            self.assertTrue(museum_record_type_to_stream(record_type))
        self.assertEqual(record_types, {"PUBLIC_ENTITY", "PUBLIC_RELATION", "WAVE_STATUS_OBSERVATION"})
        for record_type in ("WAVE_PUBLICATION_OBSERVATION", "MEDIA_DESCRIPTION_AMENDMENT", "PUBLICATION_CATALOG"):
            self.assertTrue(museum_record_type_to_stream(record_type))

    def test_abi_outer_offset_is_distinct_from_tuple_body_and_hash(self) -> None:
        record = museum_envelope_to_stream_record(self.museum_envelope(), allow_logical_uri=True)
        body = encode_collection_record_tuple_body(record)
        encoded = encode_collection_record_abi(record)
        self.assertEqual(encoded[:32], (32).to_bytes(32, "big"))
        self.assertEqual(encoded[32:], body)
        self.assertEqual(len(body) % 32, 0)
        expected_hex = "00000000000000000000000000000000000000000000000000000000000000209c5f56299520166d6f06ffa496528f8d9259a500d9397dec6bdf42977ce5ee1d1111111111111111111111111111111111111111111111111111111111111111000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000001a0333333333333333333333333333333333333333333333333333333333333333300000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000220000000000000000000000000000000000000000000000000000000006a7718b000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000060886c7c89c308c459ca8a626e0ef36a5ea9f4c7a7b56aaf86c71a2ddf3b4f904400000000000000000000000000000000000000000000000000000000000000202222222222222222222222222222222222222222222222222222222222222222000000000000000000000000000000000000000000000000000000000000004168747470733a2f2f363532396e6574776f726b6d757365756d2e6f72672f7265636f7264732f656e7469746965732f363532394e4d2d572d303030312e6a736f6e000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000006000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
        self.assertEqual(encoded.hex(), expected_hex)
        first = derive_collection_record_hash(record, chain_id=1, contract_address="0x" + "44" * 20, stream_core="0x" + "55" * 20, collection_id=7)
        record["uri"] = "https://6529networkmuseum.org/records/entities/6529NM-W-0002.json"
        second = derive_collection_record_hash(record, chain_id=1, contract_address="0x" + "44" * 20, stream_core="0x" + "55" * 20, collection_id=7)
        self.assertNotEqual(first, second)
        maximum = self.museum_envelope()
        maximum["effectiveAt"] = 18446744073709551615
        self.assertEqual(museum_envelope_to_stream_record(maximum, allow_logical_uri=True)["effectiveAt"], 18446744073709551615)

    def test_registry_collection_family_and_writer_gates_fail_closed(self) -> None:
        self.assertEqual(require_stream_admission(known_collection=True, family_admitted=True, writer_authorized=True, authorization_class=2), 2)
        for kwargs in (
            {"known_collection": False, "family_admitted": True, "writer_authorized": True, "authorization_class": 2},
            {"known_collection": True, "family_admitted": False, "writer_authorized": True, "authorization_class": 2},
            {"known_collection": True, "family_admitted": True, "writer_authorized": False, "authorization_class": 2},
            {"known_collection": True, "family_admitted": True, "writer_authorized": True, "authorization_class": 0},
        ):
            with self.assertRaises(ValueError):
                require_stream_admission(**kwargs)


class PublicationCatalogTests(unittest.TestCase):
    JCS = "0x886c7c89c308c459ca8a626e0ef36a5ea9f4c7a7b56aaf86c71a2ddf3b4f9044"

    def _record(self, record_id: str, record_type: str, *, entity: bool) -> dict:
        payload = {
            "record_id": record_id,
            "record_type": record_type,
            "schema_id": "https://6529networkmuseum.org/schemas/record-envelope-v1.json",
            "subject_id": "0x" + (record_id.encode().hex() * 64)[:64],
            "visibility": "public",
            "record_version": "1.0.0",
            "created_at": "2026-08-08T17:00:00Z",
            "observed_at": "2026-08-08T17:00:00Z",
            "effective_at": "2026-08-08T17:00:00Z",
            "constructor": {"id": "constructor:test", "role": "constructor", "observed_at": "2026-08-08T17:00:00Z"},
            "reviewer": None,
            "record_status": "review_pending",
            "review_status": "pending_independent_review",
            "payload_sha256": "sha256:" + "0" * 64,
            "references": ["fixture:source"],
            "evidence_refs": [{"label": "Fixture source", "uri": "https://6529networkmuseum.org/records/fixture/source", "evidence_class": "B", "observed_at": "2026-08-08T17:00:00Z"}],
        }
        if entity:
            payload.update({
                "entity_id": record_id,
                "entity_type": "INSTITUTION",
                "preferred_label": "Fixture Institution",
                "public_slug": None,
                "canonical_route": "/museum/network",
                "page_exposure": "canonical_page",
                "entity_status": "review_pending",
                "status_observation": {"status_label": "review_pending", "observed_at": "2026-08-08T17:00:00Z", "evidence_refs": []},
                "source_record_ids": ["fixture:source"],
                "profile": {"profile_type": "INSTITUTION", "institution_kind": "museum", "history": "Fixture."},
            })
        return self._finalize_record(payload)

    def _finalize_record(self, payload: dict) -> dict:
        zeroed = dict(payload)
        zeroed["payload_sha256"] = "sha256:" + "0" * 64
        payload["payload_sha256"] = sha256_prefixed(canonicalize(zeroed))
        digest = "0x" + keccak256(canonicalize(payload)).hex()
        return {
            "$schema": "https://6529networkmuseum.org/schemas/record-envelope-v1.json",
            "envelope": {
                "recordType": payload["record_type"],
                "subjectId": "0x" + "11" * 32,
                "contentHash": {"algorithm": 1, "digest": digest, "canonicalizationId": self.JCS},
                "uri": "https://6529networkmuseum.org/records/fixture/" + payload["record_id"],
                "schemaId": "0x" + "22" * 32,
                "signatureScheme": "0x" + "0" * 64,
                "signatureHash": {"algorithm": 2, "digest": "0x" + "0" * 64, "canonicalizationId": self.JCS},
                "effectiveAt": 1786190000,
            },
            "payload": payload,
        }

    def _inventory(self, root: Path) -> dict:
        entries = [
            {"path": "docs/page.md", "kind": "public_curatorial_manuscript", "delivery_role": "assembly_document", "required_in_catalog": True, "activation_mode": "atomic"},
            {"path": "media/art.png", "kind": "approved_public_media", "delivery_role": "media_asset", "required_in_catalog": True, "activation_mode": "deferred_on_demand"},
            {"path": "records/entities/E.json", "kind": "public_entity_record", "delivery_role": "assembly_document", "required_in_catalog": True, "activation_mode": "atomic"},
            {"path": "records/media-manifest.json", "kind": "public_media_source_manifest", "delivery_role": "assembly_document", "required_in_catalog": True, "activation_mode": "atomic"},
            {"path": "records/proposed-gifts/6529NM-PG-2026-001/media-description-amendment-2026-08-08.json", "kind": "media_description_amendment", "delivery_role": "assembly_document", "required_in_catalog": True, "activation_mode": "atomic"},
            {"path": "records/proposed-gifts/6529NM-PG-2026-001/wave-publication-observation-2026-08-08.json", "kind": "wave_observation", "delivery_role": "assembly_document", "required_in_catalog": True, "activation_mode": "atomic"},
            {"path": "records/proposed-gifts/6529NM-PG-2026-001/wave-status-observation-2026-08-08.json", "kind": "wave_observation", "delivery_role": "assembly_document", "required_in_catalog": True, "activation_mode": "atomic"},
            {"path": "records/relations/R.json", "kind": "public_relation_record", "delivery_role": "assembly_document", "required_in_catalog": True, "activation_mode": "atomic"},
            {"path": "schemas/control.json", "kind": "public_assembly_control_document", "delivery_role": "assembly_document", "required_in_catalog": True, "activation_mode": "atomic"},
        ]
        entries.sort(key=lambda item: item["path"])
        counts: dict[str, int] = {}
        for entry in entries:
            counts[entry["kind"]] = counts.get(entry["kind"], 0) + 1
        value = {
            "$schema": "https://6529networkmuseum.org/schemas/public-publication-inventory-v1.json",
            "inventory_version": "1.0.0",
            "inventory_id": "6529NM_PUBLIC_VISITOR_CORPUS",
            "scope": "visitor_publication_corpus",
            "assembler": {"required_paths": [entry["path"] for entry in entries if entry["delivery_role"] == "assembly_document"], "activation_mode": "atomic", "bundle_path": "records/publication/visitor-corpus-bundle-v1.json"},
            "bundle": {"path": "records/publication/visitor-corpus-bundle-v1.json", "schema": "https://6529networkmuseum.org/schemas/public-publication-bundle-v1.json", "required_in_catalog": True, "activation_mode": "atomic", "max_serialized_bytes": 8000000},
            "entries": entries,
            "counts": dict(sorted(counts.items())),
            "required_source_sets": {"fixture_required_paths": ["docs/page.md"]},
        }
        value["integrity"] = {"canonicalization_id": self.JCS, "body_sha256": sha256_prefixed(canonicalize(value)), "body_keccak256": "0x" + keccak256(canonicalize(value)).hex()}
        return value

    def _write_bundle(self, root: Path) -> None:
        inventory = json.loads((root / "schemas/public-publication-inventory.json").read_text(encoding="utf-8"))
        entries = []
        for path in inventory["assembler"]["required_paths"]:
            data = (root / Path(*path.split("/"))).read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
            jcs = None
            if path.endswith(".json"):
                jcs = "0x" + keccak256(canonicalize(json.loads(data))).hex()
            entries.append({"path": path, "byte_mode": "lf-normalized", "content": data.decode("utf-8"), "file_size": len(data), "sha256": sha256_prefixed(data), "jcs_keccak256": jcs})
        body_sha = sha256_prefixed(canonicalize(inventory))
        body_keccak = "0x" + keccak256(canonicalize(inventory)).hex()
        bundle = {
            "$schema": "../../schemas/public-publication-bundle.schema.json",
            "bundle_version": "1.0.0",
            "bundle_id": "6529NM_PUBLIC_VISITOR_CORPUS_BUNDLE_V1",
            "source_inventory_path": "schemas/public-publication-inventory.json",
            "source_inventory_body_sha256": body_sha,
            "source_inventory_body_keccak256": body_keccak,
            "canonicalization_id": self.JCS,
            "entries": entries,
            "entry_count": len(entries),
            "content_bytes": sum(entry["file_size"] for entry in entries),
        }
        path = root / "records/publication/visitor-corpus-bundle-v1.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(render_json(bundle))

    def _manifest_from_worktree(self, root: Path) -> dict:
        paths = sorted(
            path.relative_to(root).as_posix()
            for path in root.rglob("*")
            if path.is_file()
            and "release-artifacts" not in path.relative_to(root).parts
            and ".git" not in path.relative_to(root).parts
            and "__pycache__" not in path.parts
        )
        entries = []
        for relative in paths:
            path = root / Path(*relative.split("/"))
            raw = path.read_bytes()
            binary = path.suffix.casefold() in {".png", ".webp"}
            data = raw if binary else raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
            entry = {"path": relative, "size": len(data), "sha256": sha256_prefixed(data), "byte_mode": "raw" if binary else "lf-normalized"}
            if relative.endswith(".json"):
                entry["content_hash"] = {"algorithm": 1, "digest": "0x" + keccak256(canonicalize(json.loads(data))).hex(), "canonicalizationId": self.JCS}
            entries.append(entry)
        body = {"manifest_type": "6529NM_RECORD_MANIFEST", "manifest_version": "1.1.0", "inventory_roots": ["docs", "media", "records", "schemas", "scripts"], "inventory_files": [], "hash_algorithms": {"keccak256": 1, "sha256": 2}, "canonicalization": {"name": "RFC8785_JCS", "id": self.JCS, "profile": "museum-i-json-v1"}, "entries": entries}
        canonical_body = canonicalize(body)
        body["manifest_commitment"] = {"algorithm": 1, "digest": "0x" + keccak256(canonical_body).hex(), "canonicalizationId": self.JCS}
        body["manifest_sha256"] = sha256_prefixed(canonical_body)
        return body

    def fixture_repo(self) -> tuple[tempfile.TemporaryDirectory, Path, str, str]:
        temporary = tempfile.TemporaryDirectory()
        root = Path(temporary.name)
        for relative, data in {"docs/page.md": b"# Public page\n", "media/art.png": b"PNG fixture bytes\x00", "records/media-manifest.json": b"{\"media\":true}\n", "schemas/control.json": b"{\"control\":true}\n"}.items():
            path = root / Path(*relative.split("/"))
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        record_paths = {
            "records/entities/E.json": self._record("E", "PUBLIC_ENTITY", entity=True),
            "records/relations/R.json": self._record("R", "PUBLIC_RELATION", entity=False),
            "records/proposed-gifts/6529NM-PG-2026-001/wave-status-observation-2026-08-08.json": self._record("WSTATUS", "WAVE_STATUS_OBSERVATION", entity=False),
            "records/proposed-gifts/6529NM-PG-2026-001/wave-publication-observation-2026-08-08.json": self._record("WPUB", "WAVE_PUBLICATION_OBSERVATION", entity=False),
            "records/proposed-gifts/6529NM-PG-2026-001/media-description-amendment-2026-08-08.json": self._record("AMEND", "MEDIA_DESCRIPTION_AMENDMENT", entity=False),
        }
        for relative, value in record_paths.items():
            path = root / Path(*relative.split("/"))
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(render_json(value))
        inventory = self._inventory(root)
        (root / "schemas").mkdir(exist_ok=True)
        (root / "schemas/public-publication-inventory.json").write_bytes(render_json(inventory))
        self._write_bundle(root)
        for relative in ("public-publication-inventory.schema.json", "public-publication-bundle.schema.json", "publication-catalog.schema.json", "publication-catalog-pointer.schema.json"):
            (root / "schemas" / relative).write_bytes((ROOT / "schemas" / relative).read_bytes())
        for relative in ("generate_manifest.py", "generate_public_publication_inventory.py", "generate_public_publication_bundle.py", "bootstrap_validate.py", "validate.py"):
            path = root / "scripts" / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("raise SystemExit(0)\n", encoding="utf-8", newline="\n")
        manifest_path = root / "release-artifacts/latest/record-manifest.json"
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["git", "init", "-q"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.invalid"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.name", "Catalog Test"], cwd=root, check=True)
        manifest_path.write_bytes(render_json(self._manifest_from_worktree(root)))
        subprocess.run(["git", "add", "."], cwd=root, check=True)
        subprocess.run(["git", "commit", "-qm", "candidate A"], cwd=root, check=True)
        candidate = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        candidate_sha = manifest["manifest_sha256"]
        candidate_keccak = manifest["manifest_commitment"]["digest"]
        for relative, record in record_paths.items():
            payload = record["payload"]
            payload["reviewer"] = {"id": "reviewer:test", "role": "reviewer", "reviewed_at": "2026-08-08T18:00:00Z", "reviewed_manifest_sha256": candidate_sha, "reviewed_manifest_keccak": candidate_keccak, "reviewed_commit": candidate, "reviewer_ids": ["reviewer:test"], "outcome": "approved"}
            payload["record_status"] = "reviewed"
            payload["review_status"] = "reviewed"
            if "entity_status" in payload:
                payload["entity_status"] = "published"
                payload["status_observation"]["status_label"] = "published"
            updated = self._finalize_record(payload)
            (root / Path(*relative.split("/"))).write_bytes(render_json(updated))
        self._write_bundle(root)
        manifest_path.write_bytes(render_json(self._manifest_from_worktree(root)))
        subprocess.run(["git", "add", "."], cwd=root, check=True)
        subprocess.run(["git", "commit", "-qm", "reviewed B"], cwd=root, check=True)
        reviewed = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()
        return temporary, root, candidate, reviewed

    def test_release_artifacts_is_the_manifest_self_reference_boundary(self) -> None:
        paths = [path.relative_to(ROOT).as_posix() for path in inventory_paths(ROOT)]
        self.assertFalse(any(path.startswith("release-artifacts/") for path in paths))

    def test_catalog_binds_exact_git_objects_and_pointer(self) -> None:
        temporary, root, _candidate, reviewed = self.fixture_repo()
        try:
            catalog = build_catalog(root, reviewed_source_head_commit=reviewed, accepted_paths=None, created_at="2026-08-08T19:00:00Z")
            self.assertEqual(validate_catalog(catalog, root=root, expected_commit=reviewed), [])
            catalog_bytes = render_json(catalog)
            pointer = build_pointer(catalog, catalog_file_sha256=sha256_prefixed(catalog_bytes), activation_actor="release-activator:test", activated_at="2026-08-08T19:01:00Z", mode="activate", prior_catalog_id=None)
            self.assertEqual(validate_pointer(pointer, catalog, catalog_bytes), [])
            self.assertEqual(check_append_only_catalog(None, catalog, current_pointer=pointer), [])
            self.assertTrue(catalog["payload"]["manifest_binding"]["immutable_raw_url"].endswith(reviewed + "/release-artifacts/latest/record-manifest.json"))
        finally:
            temporary.cleanup()

    def test_catalog_rejects_self_reference_and_moving_or_short_commit(self) -> None:
        temporary, root, _candidate, reviewed = self.fixture_repo()
        try:
            with self.assertRaises(ValueError):
                build_catalog(root, reviewed_source_head_commit="main", accepted_paths=None, created_at="2026-08-08T19:00:00Z")
            catalog = build_catalog(root, reviewed_source_head_commit=reviewed, accepted_paths=None, created_at="2026-08-08T19:00:00Z")
            mutated = copy.deepcopy(catalog)
            mutated["payload"]["media_assets"][0]["path"] = "release-artifacts/latest/publication-catalog-pointer.json"
            self.assertTrue(validate_catalog(mutated))
            self.assertEqual(check_append_only_catalog(catalog["payload"]["catalog_id"], catalog), ["catalog IDs are immutable; rewrite requires a new catalog ID"])
        finally:
            temporary.cleanup()

    def test_deterministic_replay_requires_every_generator_and_validator_path(self) -> None:
        temporary, root, _candidate, reviewed = self.fixture_repo()
        try:
            import publication_catalog as catalog_module
            _manifest, entries, _binding = catalog_module._read_manifest(root, reviewed)
            missing = dict(entries)
            missing.pop("scripts/generate_public_publication_bundle.py")
            with self.assertRaises(CatalogError):
                _verify_deterministic_promotion_artifacts(root, reviewed, missing)
        finally:
            temporary.cleanup()

    def test_append_only_pointer_lineage_and_rollback_targets(self) -> None:
        temporary, root, _candidate, reviewed = self.fixture_repo()
        try:
            catalog = build_catalog(root, reviewed_source_head_commit=reviewed, accepted_paths=None, created_at="2026-08-08T19:00:00Z")
            catalog_bytes = render_json(catalog)
            pointer = build_pointer(catalog, catalog_file_sha256=sha256_prefixed(catalog_bytes), activation_actor="test", activated_at="2026-08-08T19:01:00Z", mode="activate", prior_catalog_id=None)
            self.assertEqual(check_append_only_catalog(None, catalog, current_pointer=pointer), [])
            bad = copy.deepcopy(pointer)
            bad["activation"]["prior_catalog_id"] = catalog["payload"]["catalog_id"]
            self.assertTrue(check_append_only_catalog(None, catalog, current_pointer=bad))
            rollback = copy.deepcopy(pointer)
            rollback["activation"] = {"actor_id": "test", "activated_at": "2026-08-08T19:02:00Z", "mode": "rollback", "prior_catalog_id": catalog["payload"]["catalog_id"]}
            self.assertTrue(check_append_only_catalog(None, catalog, current_pointer=rollback, retained_catalog_ids={catalog["payload"]["catalog_id"]}))
        finally:
            temporary.cleanup()


if __name__ == "__main__":
    unittest.main()
