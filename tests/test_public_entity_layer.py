"""Executable contract tests for the public entity and relation projection."""

from __future__ import annotations

import copy
import json
import re
import sys
import tempfile
import unittest
from collections import Counter
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import migrate_public_entities as migration  # noqa: E402
from migrate_public_entities import (  # noqa: E402
    GENERATED_AT,
    EVIDENCE_CLASSES,
    WINNER_AT,
    WINNER_OBSERVATION_ID,
    WINNER_SOURCE_PATH,
    WAVE_PUBLICATION_OBSERVATION_ID,
    WAVE_PUBLICATION_OBSERVATION_PATH,
    build_records,
    evidence,
    generated_directory_issues,
    identity_binding_indexes,
    infer_existing_review_arguments,
    load_json,
    relation_binding_indexes,
    resolve_identity_ids,
    semantic_relation_key,
    source_evidence,
    source_record_evidence_class,
    verify_evidence_paths,
)

TEST_REVIEWED_AT = "2026-08-24T00:00:00Z"
TEST_REVIEWED_COMMIT = "a" * 40
TEST_REVIEWED_MANIFEST_SHA256 = "sha256:" + "b" * 64
TEST_REVIEWED_MANIFEST_KECCAK = "0x" + "c" * 64
from validate import (  # noqa: E402
    DuplicateJsonKeyError,
    PUBLIC_RELATION_TYPE,
    load_schemas,
    reject_duplicate_keys,
    validate_public_graph,
    validate_public_media,
    validate_public_payload,
    validate_media_description_amendment,
    validate_wave_publication_observation,
    validator_for,
)


class PublicEntityLayerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.records = build_records(
            reviewed=True,
            reviewer_id="codex-review:test-independent",
            reviewed_at=TEST_REVIEWED_AT,
            reviewed_commit=TEST_REVIEWED_COMMIT,
            reviewed_manifest_sha256=TEST_REVIEWED_MANIFEST_SHA256,
            reviewed_manifest_keccak=TEST_REVIEWED_MANIFEST_KECCAK,
        )
        cls.vocabularies, _envelope_schema, cls.schema_store = load_schemas(ROOT)
        cls.inventory = load_json(ROOT / "schemas/public-entity-identity-inventory.json")

    @classmethod
    def payloads(cls) -> list[dict]:
        return [record["payload"] for record in cls.records.values()]

    @classmethod
    def entities(cls) -> dict[str, dict]:
        return {payload["entity_id"]: payload for payload in cls.payloads() if payload.get("record_type") == "PUBLIC_ENTITY"}

    @classmethod
    def relations(cls) -> list[dict]:
        return [payload for payload in cls.payloads() if payload.get("record_type") == PUBLIC_RELATION_TYPE]

    def graph_issues(self, records: dict | None = None) -> list[str]:
        source = records or self.records
        tuples = [(ROOT / relative, record, record.get("payload")) for relative, record in source.items()]
        return validate_public_graph(tuples, self.vocabularies, self.inventory)

    def schema_issues(self, payload: dict, schema_id: str) -> list[str]:
        validator = validator_for(self.schema_store[schema_id], self.schema_store)
        return [error.message for error in validator.iter_errors(payload)]

    def local_schema_issues(self, payload: dict, relative_schema: str) -> list[str]:
        schema = load_json(ROOT / relative_schema)
        validator = validator_for(schema, self.schema_store)
        return [error.message for error in validator.iter_errors(payload)]

    def test_existing_review_state_replay_is_closed_and_consistent(self) -> None:
        paths = {"records/entities/E1.json": {}, "records/relations/R1.json": {}}

        def write_records(root: Path, payloads: list[dict]) -> None:
            for relative, payload in zip(paths, payloads, strict=True):
                destination = root / relative
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_text(json.dumps({"payload": payload}), encoding="utf-8")

        pending = {
            "record_status": "review_pending",
            "review_status": "pending_independent_review",
            "reviewer": None,
        }
        reviewer = {
            "id": "reviewer:test",
            "role": "reviewer",
            "reviewed_at": TEST_REVIEWED_AT,
            "reviewed_commit": TEST_REVIEWED_COMMIT,
            "reviewed_manifest_sha256": TEST_REVIEWED_MANIFEST_SHA256,
            "reviewed_manifest_keccak": TEST_REVIEWED_MANIFEST_KECCAK,
            "reviewer_ids": ["reviewer:test"],
            "outcome": "approved",
        }
        reviewed = {
            "created_at": GENERATED_AT,
            "record_status": "reviewed",
            "review_status": "reviewed",
            "reviewer": reviewer,
        }
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            write_records(root, [pending, pending])
            self.assertEqual(infer_existing_review_arguments(paths, root=root), {"reviewed": False, "reviewer_id": None})

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            write_records(root, [reviewed, reviewed])
            self.assertEqual(
                infer_existing_review_arguments(paths, root=root),
                {
                    "reviewed": True,
                    "reviewer_id": "reviewer:test",
                    "reviewed_at": TEST_REVIEWED_AT,
                    "reviewed_commit": TEST_REVIEWED_COMMIT,
                    "reviewed_manifest_sha256": TEST_REVIEWED_MANIFEST_SHA256,
                    "reviewed_manifest_keccak": TEST_REVIEWED_MANIFEST_KECCAK,
                },
            )

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            write_records(root, [pending, reviewed])
            with self.assertRaisesRegex(ValueError, "mix pending and reviewed"):
                infer_existing_review_arguments(paths, root=root)

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            other = copy.deepcopy(reviewed)
            other["reviewer"]["reviewed_commit"] = "d" * 40
            write_records(root, [reviewed, other])
            with self.assertRaisesRegex(ValueError, "do not share one review binding"):
                infer_existing_review_arguments(paths, root=root)

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            early = copy.deepcopy(reviewed)
            early["reviewer"]["reviewed_at"] = GENERATED_AT
            write_records(root, [early, early])
            with self.assertRaisesRegex(ValueError, "at or before construction"):
                infer_existing_review_arguments(paths, root=root)

    def test_magnum_machine_schema_closes_nested_contracts_and_work_rows(self) -> None:
        machine_root = ROOT / "records/proposed-gifts/6529NM-PG-2026-001/public/scholarship/machine"
        records = {path.name: load_json(path) for path in sorted(machine_root.glob("*.json"))}
        for name, record in records.items():
            self.assertEqual(
                self.local_schema_issues(record, "schemas/magnum-scholarship-machine-record.schema.json"),
                [],
                name,
            )

        mutations = []
        integration = copy.deepcopy(records["integration-map.json"])
        integration["entity_projections"] = {}
        mutations.append(integration)
        integration = copy.deepcopy(records["integration-map.json"])
        integration["publication_path_contract"]["undeclared"] = True
        mutations.append(integration)
        integration = copy.deepcopy(records["integration-map.json"])
        integration["entity_projections"]["media_references"]["standalone_work_route"] = "deny_without_media_only"
        mutations.append(integration)
        media_join = copy.deepcopy(records["wave-media-join.json"])
        media_join["route_policy"]["undeclared"] = "allow"
        mutations.append(media_join)
        schedule = copy.deepcopy(records["object-schedule.json"])
        schedule["works"][0] = {}
        mutations.append(schedule)
        schedule = copy.deepcopy(records["object-schedule.json"])
        schedule["works"][0]["date"] = "1952-01-01"
        mutations.append(schedule)
        schedule = copy.deepcopy(records["object-schedule.json"])
        schedule["works"][1].pop("issuer_place_label")
        mutations.append(schedule)
        projections = copy.deepcopy(records["work-projections.json"])
        projections["works"][0]["token"]["undeclared"] = "drift"
        mutations.append(projections)
        projections = copy.deepcopy(records["work-projections.json"])
        projections["works"][3]["manifestations"][0]["identity_inference"] = {
            "required": False,
            "forbidden": ["identity"],
        }
        mutations.append(projections)

        for index, mutated in enumerate(mutations):
            self.assertTrue(
                self.local_schema_issues(mutated, "schemas/magnum-scholarship-machine-record.schema.json"),
                f"mutation {index} unexpectedly passed",
            )

        projections = records["work-projections.json"]
        schedule = records["object-schedule.json"]
        self.assertEqual([work["date_precision"] for work in schedule["works"]], ["year", "year", "year", "year", "day"])
        self.assertEqual(schedule["works"][1]["place"], "Suchitoto, El Salvador")
        self.assertEqual(schedule["works"][1]["issuer_place_label"], "Suchitito, El Salvador")
        self.assertEqual(
            projections["evidence_sources_scope"],
            "Each Work array is the complete set of source-register IDs explicitly cited on that public Work page, including contextual cross-references and the shared historical Wave-publication source.",
        )
        for work in projections["works"]:
            page = (ROOT / work["public_page"]).read_text(encoding="utf-8")
            self.assertEqual(work["evidence_sources"], sorted(set(re.findall(r"\bS\d{2,}\b", page))))

    def test_public_safe_wave_parts_are_exactly_ordered_and_distinct(self) -> None:
        evidence = load_json(
            ROOT / "records/proposed-gifts/6529NM-PG-2026-001/evidence/wave-publication-observation-public-safe-2026-08-09.json"
        )
        schema_path = "schemas/wave-publication-public-safe-evidence.schema.json"
        self.assertEqual(self.local_schema_issues(evidence, schema_path), [])

        duplicate = copy.deepcopy(evidence)
        duplicate["payload"]["parts"][1]["part_id"] = 1
        self.assertTrue(self.local_schema_issues(duplicate, schema_path))
        missing = copy.deepcopy(evidence)
        missing["payload"]["parts"].pop()
        self.assertTrue(self.local_schema_issues(missing, schema_path))
        reordered = copy.deepcopy(evidence)
        reordered["payload"]["parts"][1], reordered["payload"]["parts"][2] = (
            reordered["payload"]["parts"][2],
            reordered["payload"]["parts"][1],
        )
        self.assertTrue(self.local_schema_issues(reordered, schema_path))
        duplicate_media = copy.deepcopy(evidence)
        duplicate_media["payload"]["parts"][0]["media"].append(
            copy.deepcopy(duplicate_media["payload"]["parts"][0]["media"][0])
        )
        self.assertTrue(self.local_schema_issues(duplicate_media, schema_path))

    def test_exact_projection_counts_and_profile_counts(self) -> None:
        counts = Counter(payload["record_type"] for payload in self.payloads())
        self.assertEqual(counts, Counter({"PUBLIC_ENTITY": 136, "PUBLIC_RELATION": 233, "WAVE_STATUS_OBSERVATION": 1}))
        entities = self.entities()
        self.assertEqual(sum(payload["entity_type"] == "ARTIST" for payload in entities.values()), 23)
        self.assertEqual(sum(payload["entity_type"] == "ORGANIZATION" for payload in entities.values()), 2)
        self.assertEqual(sum(payload["entity_type"] == "PROJECT_OR_SERIES" for payload in entities.values()), 7)
        self.assertEqual(sum(payload["entity_type"] == "WORK" for payload in entities.values()), 29)
        self.assertEqual(sum(payload["entity_type"] == "AGENT" for payload in entities.values()), 21)
        self.assertEqual(sum(payload["entity_type"] == "MEDIA_REFERENCE" for payload in entities.values()), 40)
        self.assertEqual(sum(payload["entity_type"] == "ACQUISITION_PROGRAM" for payload in entities.values()), 2)
        self.assertEqual(sum(payload["entity_type"] == "RESEARCH_PUBLICATION" for payload in entities.values()), 3)
        self.assertEqual(len(self.relations()), 233)
        sample = next(iter(entities.values()))
        self.assertEqual(sample["reviewer"]["reviewed_at"], TEST_REVIEWED_AT)
        self.assertEqual(sample["reviewer"]["reviewed_commit"], TEST_REVIEWED_COMMIT)
        self.assertEqual(sample["reviewer"]["reviewed_manifest_sha256"], TEST_REVIEWED_MANIFEST_SHA256)
        self.assertEqual(sample["reviewer"]["reviewed_manifest_keccak"], TEST_REVIEWED_MANIFEST_KECCAK)
        self.assertEqual(sample["constructor"]["observed_at"], GENERATED_AT)
        self.assertNotEqual(sample["reviewer"]["reviewed_at"], sample["constructor"]["observed_at"])

    def test_keys_and_gates_research_publication_is_governed_and_explicitly_bound(self) -> None:
        entities = self.entities()
        publication = entities["6529NM-RP-0002"]
        self.assertEqual(publication["preferred_label"], "Access, Control, and Exit")
        self.assertEqual(publication["public_slug"], "access-control-and-exit")
        self.assertEqual(publication["canonical_route"], "/museum/network/research/access-control-and-exit")
        profile = publication["profile"]
        self.assertEqual(profile["publication_kind"], "catalogue_essay")
        self.assertEqual(profile["publication_date"], "2026-08-08")
        self.assertEqual(profile["version"], "1.2")
        self.assertEqual(profile["author_entity_ids"], ["6529NM-I-0001"])
        work_ids = [f"6529NM-W-{index:04d}" for index in range(8, 24)]
        artist_ids = [f"6529NM-ART-{index:04d}" for index in range(2, 17)]
        self.assertEqual(profile["subject_entity_ids"], ["6529NM-CA-2026-002", *work_ids, *artist_ids])
        self.assertTrue(profile["publication_document_uri"].endswith("records/programs/6529NM-AP-01/public/curatorial-essay.md"))
        self.assertIn("records/programs/6529NM-AP-01/public/curatorial-essay.md", json.dumps(profile["evidence_refs"]))

        relation_bindings = load_json(ROOT / "schemas/public-relation-identity-inventory.json")["relation_bindings"]
        relation_ids = [row["relation_id"] for row in relation_bindings]
        self.assertEqual(relation_ids[:158], [f"6529NM-REL-{index:04d}" for index in range(1, 159)])
        self.assertEqual(relation_ids[158:], [f"6529NM-REL-{index:04d}" for index in range(165, 240)])
        retired = load_json(ROOT / "schemas/public-relation-identity-inventory.json")["retired_relation_ids"]
        self.assertEqual([row["relation_id"] for row in retired], [f"6529NM-REL-{index:04d}" for index in range(159, 165)])
        self.assertEqual(retired[0]["superseded_by"], "6529NM-REL-0047")

        publication_inventory = load_json(ROOT / "schemas/public-publication-inventory.json")
        publication_entries = {
            row["path"]: row for row in publication_inventory["entries"]
        }
        closed_graph_controls = {
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
        }
        closed_graph_controls.update(
            f"schemas/{filename}"
            for filename in self.vocabularies["schema_paths"].values()
        )
        for path in closed_graph_controls:
            self.assertEqual(
                publication_entries[path],
                {
                    "path": path,
                    "kind": "public_assembly_control_document",
                    "delivery_role": "assembly_document",
                    "required_in_catalog": True,
                    "activation_mode": "atomic",
                },
            )
            self.assertIn(path, publication_inventory["assembler"]["required_paths"])

        visitor_bundle = load_json(
            ROOT / "records/publication/visitor-corpus-bundle-v1.json"
        )
        bundled_paths = {row["path"] for row in visitor_bundle["entries"]}
        self.assertTrue(set(closed_graph_controls).issubset(bundled_paths))
        self.assertIn("docs/generative-system-analysis.md", bundled_paths)
        self.assertIn("docs/generative-trait-analysis.md", bundled_paths)

        schema_id_paths = {}
        for path in sorted((ROOT / "schemas").glob("*.schema.json")):
            document = load_json(path)
            if isinstance(document.get("$id"), str):
                schema_id_paths[document["$id"].split("#", 1)[0]] = path.relative_to(ROOT).as_posix()
        published_schema_paths = {
            path
            for path in publication_entries
            if path.startswith("schemas/") and path.endswith(".schema.json")
        }
        for path in published_schema_paths:
            nodes = [load_json(ROOT / path)]
            while nodes:
                node = nodes.pop()
                if isinstance(node, dict):
                    reference = node.get("$ref")
                    if isinstance(reference, str) and not reference.startswith("#"):
                        base_id = reference.split("#", 1)[0]
                        self.assertIn(base_id, schema_id_paths, (path, reference))
                        self.assertIn(schema_id_paths[base_id], publication_entries, (path, reference))
                    nodes.extend(node.values())
                elif isinstance(node, list):
                    nodes.extend(node)

        interprets = [relation for relation in self.relations() if relation["source_entity_id"] == "6529NM-RP-0002" and relation["relation_type"] == "PUBLICATION_INTERPRETS_ENTITY"]
        self.assertEqual(len(interprets), 32)
        self.assertEqual({relation["target_entity_id"] for relation in interprets}, {"6529NM-CA-2026-002", *work_ids, *artist_ids})
        self.assertTrue(all(relation["qualifier"] == {"role": "subject"} for relation in interprets))
        self.assertTrue(all("records/programs/6529NM-AP-01/public/curatorial-essay.md" in json.dumps(relation["evidence_refs"]) for relation in interprets))
        publishes = [relation for relation in self.relations() if relation["relation_type"] == "INSTITUTION_PUBLISHES_PUBLICATION" and relation["target_entity_id"] == "6529NM-RP-0002"]
        self.assertEqual(len(publishes), 1)
        self.assertEqual(publishes[0]["source_entity_id"], "6529NM-I-0001")
        self.assertIn("records/programs/6529NM-AP-01/public/curatorial-essay.md", json.dumps(publishes[0]["evidence_refs"]))

        slug_row = next(row for row in self.inventory["public_slug_inventory"] if row["entity_id"] == "6529NM-RP-0002")
        self.assertEqual(slug_row, {"entity_id": "6529NM-RP-0002", "entity_type": "RESEARCH_PUBLICATION", "preferred_label": "Access, Control, and Exit", "public_slug": "access-control-and-exit", "canonical_route": "/museum/network/research/access-control-and-exit"})

    def test_magnum_research_publication_and_relations_are_governed(self) -> None:
        entities = self.entities()
        publication = entities["6529NM-RP-0003"]
        self.assertEqual(publication["preferred_label"], "Conflict at Its Edges")
        self.assertEqual(publication["public_slug"], "conflict-at-its-edges")
        self.assertEqual(publication["canonical_route"], "/museum/network/research/conflict-at-its-edges")
        profile = publication["profile"]
        self.assertEqual(profile["publication_kind"], "research_dossier")
        self.assertEqual(profile["publication_date"], "2026-08-09")
        self.assertEqual(profile["version"], "1.0.1")
        self.assertEqual(profile["author_entity_ids"], ["6529NM-I-0001"])
        artist_ids = [f"6529NM-ART-{index:04d}" for index in range(17, 22)]
        work_ids = [f"6529NM-W-{index:04d}" for index in range(24, 29)]
        subjects = ["6529NM-CA-2026-003", "6529NM-ORG-0002", "6529NM-PRJ-0006", *artist_ids, *work_ids]
        self.assertEqual(profile["subject_entity_ids"], subjects)
        manuscript = migration.MAGNUM_CATALOGUE_ESSAY_PATH
        self.assertTrue(profile["publication_document_uri"].endswith(manuscript))
        self.assertIn(manuscript, json.dumps(profile["evidence_refs"]))
        self.assertFalse(profile["publication_document_uri"].endswith(migration.MAGNUM_PUBLICATION_RECORD_PATH))
        self.assertEqual(profile["publication_component_paths"], list(migration.MAGNUM_PUBLICATION_COMPONENT_PATHS))
        self.assertEqual(len(profile["publication_component_paths"]), 22)
        self.assertEqual(len(set(profile["publication_component_paths"])), 22)
        self.assertTrue(all((ROOT / path).is_file() for path in profile["publication_component_paths"]))
        self.assertNotIn(migration.MAGNUM_PUBLICATION_RECORD_PATH, profile["publication_component_paths"])
        self.assertFalse(any("/machine/" in path for path in profile["publication_component_paths"]))

        interprets = [
            relation
            for relation in self.relations()
            if relation["source_entity_id"] == "6529NM-RP-0003"
            and relation["relation_type"] == "PUBLICATION_INTERPRETS_ENTITY"
        ]
        self.assertEqual(len(interprets), 13)
        self.assertEqual({relation["target_entity_id"] for relation in interprets}, set(subjects))
        self.assertTrue(all(relation["qualifier"] == {"role": "subject"} for relation in interprets))
        self.assertTrue(all(manuscript in json.dumps(relation["evidence_refs"]) for relation in interprets))
        publishes = [
            relation
            for relation in self.relations()
            if relation["relation_type"] == "INSTITUTION_PUBLISHES_PUBLICATION"
            and relation["target_entity_id"] == "6529NM-RP-0003"
        ]
        self.assertEqual(len(publishes), 1)
        self.assertEqual(publishes[0]["source_entity_id"], "6529NM-I-0001")
        self.assertIn(manuscript, json.dumps(publishes[0]["evidence_refs"]))

        slug_row = next(row for row in self.inventory["public_slug_inventory"] if row["entity_id"] == "6529NM-RP-0003")
        self.assertEqual(
            slug_row,
            {
                "entity_id": "6529NM-RP-0003",
                "entity_type": "RESEARCH_PUBLICATION",
                "preferred_label": "Conflict at Its Edges",
                "public_slug": "conflict-at-its-edges",
                "canonical_route": "/museum/network/research/conflict-at-its-edges",
            },
        )

    def test_migration_rejects_unexpected_generated_json(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            entities_dir = root / "entities"
            relations_dir = root / "relations"
            entities_dir.mkdir()
            relations_dir.mkdir()
            (entities_dir / "known-entity.json").write_text("{}", encoding="utf-8")
            (entities_dir / "stale-entity.json").write_text("{}", encoding="utf-8")
            (relations_dir / "known-relation.json").write_text("{}", encoding="utf-8")
            issues = generated_directory_issues(
                {
                    "records/entities/known-entity.json": {},
                    "records/relations/known-relation.json": {},
                },
                entities_dir=entities_dir,
                relations_dir=relations_dir,
            )
            unexpected, missing = issues
            self.assertEqual(unexpected, ["unexpected generated JSON: records/entities/stale-entity.json"])
            self.assertEqual(missing, [])

    def test_migration_inventory_allows_missing_write_repairs(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            entities_dir = root / "entities"
            relations_dir = root / "relations"
            entities_dir.mkdir()
            relations_dir.mkdir()
            (relations_dir / "known-relation.json").write_text("{}", encoding="utf-8")
            unexpected, missing = generated_directory_issues(
                {
                    "records/entities/missing-entity.json": {},
                    "records/relations/known-relation.json": {},
                },
                entities_dir=entities_dir,
                relations_dir=relations_dir,
            )
            self.assertEqual(unexpected, [])
            self.assertEqual(missing, ["missing generated JSON: records/entities/missing-entity.json"])
            (entities_dir / "stale-entity.json").write_text("{}", encoding="utf-8")
            unexpected, missing = generated_directory_issues(
                {
                    "records/entities/missing-entity.json": {},
                    "records/relations/known-relation.json": {},
                },
                entities_dir=entities_dir,
                relations_dir=relations_dir,
            )
            self.assertEqual(unexpected, ["unexpected generated JSON: records/entities/stale-entity.json"])
            self.assertEqual(missing, ["missing generated JSON: records/entities/missing-entity.json"])

    def test_canonical_ids_slugs_routes_and_artist_relations_are_closed(self) -> None:
        entities = self.entities()
        works = {key: value for key, value in entities.items() if value["entity_type"] == "WORK"}
        self.assertEqual(set(works), {f"6529NM-W-{index:04d}" for index in range(1, 30)})
        for work_id, work in works.items():
            expected_slug = work_id
            self.assertEqual(work["public_slug"], expected_slug)
            self.assertEqual(work["canonical_route"], f"/museum/network/works/{expected_slug}")
        artists = {payload["entity_id"]: payload for payload in entities.values() if payload["entity_type"] == "ARTIST"}
        self.assertEqual(len(artists), 23)
        self.assertNotIn("artist-", " ".join(payload["public_slug"] for payload in artists.values()))
        expected_artist_slugs = {row["entity_id"]: row["public_slug"] for row in self.inventory["public_slug_inventory"] if row["entity_type"] == "ARTIST"}
        self.assertEqual({key: value["public_slug"] for key, value in artists.items()}, expected_artist_slugs)
        programs = {payload["entity_id"]: payload for payload in entities.values() if payload["entity_type"] == "ACQUISITION_PROGRAM"}
        self.assertEqual(programs["6529NM-AP-ENT-0001"]["canonical_route"], "/museum/network/acquisition-programs/gift-acquisitions")
        self.assertEqual(programs["6529NM-AP-ENT-0002"]["canonical_route"], "/museum/network/acquisition-programs/keys-and-gates")
        organizations = {payload["entity_id"]: payload for payload in entities.values() if payload["entity_type"] == "ORGANIZATION"}
        self.assertEqual(organizations["6529NM-ORG-0002"]["canonical_route"], "/museum/network/organizations/magnum-photos")
        projects = {payload["entity_id"]: payload for payload in entities.values() if payload["entity_type"] == "PROJECT_OR_SERIES"}
        magnum_project = projects["6529NM-PRJ-0006"]
        self.assertEqual(magnum_project["public_slug"], "magnum-photos-75")
        self.assertEqual(magnum_project["canonical_route"], "/museum/network/projects/magnum-photos-75")
        self.assertEqual(magnum_project["profile"]["work_entity_ids"], [f"6529NM-W-{index:04d}" for index in range(24, 29)])
        self.assertEqual(magnum_project["profile"]["project_relation_basis"], "proposal_work_set")
        self.assertIn("public/scholarship/entities/magnum-photos-75.md", json.dumps(magnum_project))
        self.assertIn(migration.WINNER_SOURCE_URL, json.dumps(magnum_project))
        creator_relations = [relation for relation in self.relations() if relation["relation_type"] == "ARTIST_CREATES_WORK"]
        self.assertEqual(len(creator_relations), 30)
        self.assertTrue(all(entities[relation["source_entity_id"]]["entity_type"] == "ARTIST" for relation in creator_relations))
        hugo = next(payload for payload in artists.values() if payload["preferred_label"] == "HugoFaz")
        self.assertEqual({relation["target_entity_id"] for relation in creator_relations if relation["source_entity_id"] == hugo["entity_id"]}, {"6529NM-W-0009", "6529NM-W-0018"})
        self.assertEqual(works["6529NM-W-0009"]["preferred_label"], "the Artist in the Open Sea")
        self.assertEqual(works["6529NM-W-0009"]["profile"]["title"], "the Artist in the Open Sea")
        self.assertIn(migration.KEYS_TITLE_DISPLAY_AMENDMENT_PATH, {item["uri"].split("/blob/main/", 1)[-1] for item in works["6529NM-W-0009"]["evidence_refs"]})
        moises = artists["6529NM-ART-0020"]
        self.assertEqual(moises["preferred_label"], "Moisés Saman")
        self.assertTrue(any(variant["variant_role"] == "source_label" and variant["value"] == "Moisés Saman" for variant in moises["profile"]["name_variants"]))
        magnum_profiles = [
            organizations["6529NM-ORG-0002"],
            *[artists[f"6529NM-ART-{index:04d}"] for index in range(17, 22)],
        ]
        proposal_uri = migration.WINNER_SOURCE_URL
        for profile in magnum_profiles:
            self.assertEqual(profile["observed_at"], migration.MAGNUM_PUBLICATION_AT)
            self.assertEqual(profile["effective_at"], migration.MAGNUM_PUBLICATION_AT)
            labels = {item["label"] for item in profile["evidence_refs"]}
            self.assertTrue(
                any(
                    label.startswith("Original proposed-gift")
                    or label == "Proposed gift artist label"
                    for label in labels
                )
            )
            self.assertTrue(any("research profile" in label.lower() for label in labels))
            evidence_text = json.dumps(profile["evidence_refs"])
            self.assertIn(proposal_uri, evidence_text)
            self.assertIn(migration.PROPOSAL_AT, evidence_text)
            self.assertIn(migration.MAGNUM_PUBLICATION_AT, evidence_text)
        organization_evidence = json.dumps(organizations["6529NM-ORG-0002"]["evidence_refs"])
        self.assertIn(migration.WINNER_SOURCE_URL, organization_evidence)
        self.assertIn(f"{migration.MAGNUM_SCHOLARSHIP_ROOT}/entities/magnum-photos.md", organization_evidence)

        public_graph = json.dumps([*entities.values(), *self.relations()])
        for raw_decision_path in (
            "records/proposed-gifts/6529NM-PG-2026-001/proposal.json",
            "records/proposed-gifts/6529NM-PG-2026-001/wave-storm.json",
            "records/proposed-gifts/6529NM-PG-2026-001/public/wave-storm/",
            migration.WAVE_PUBLICATION_OBSERVATION_PATH,
            migration.MEDIA_DESCRIPTION_AMENDMENT_PATH,
        ):
            self.assertNotIn(raw_decision_path, public_graph)

        route_prefixes = {
            "ARTIST": "/museum/network/artists/",
            "ORGANIZATION": "/museum/network/organizations/",
            "PROJECT_OR_SERIES": "/museum/network/projects/",
            "CURATED_ACQUISITION": "/museum/network/acquisitions/",
            "RESEARCH_PUBLICATION": "/museum/network/research/",
            "WORK": "/museum/network/works/",
            "ACQUISITION_PROGRAM": "/museum/network/acquisition-programs/",
        }
        seen_route_keys = set()
        for payload in entities.values():
            entity_type = payload["entity_type"]
            if entity_type in route_prefixes:
                self.assertEqual(payload["canonical_route"], route_prefixes[entity_type] + payload["public_slug"])
                key = (entity_type, payload["public_slug"])
                self.assertNotIn(key, seen_route_keys)
                seen_route_keys.add(key)

    def test_work_identity_is_not_acquisition_scoped(self) -> None:
        aliases = {row["alias"]: row["canonical_entity_id"] for row in self.inventory["work_aliases"]}
        self.assertEqual(aliases["6529NM-AP-01-OUT-001"], "6529NM-W-0008")
        self.assertEqual(aliases["6529NM-PG-2026-001.OBJ-001"], "6529NM-W-0024")
        self.assertNotIn("6529NM-CA-2026-003.OBJ-001", aliases)
        self.assertNotEqual("6529NM-CA-2026-003", aliases["6529NM-PG-2026-001.OBJ-003"])

    def test_magnum_tokens_are_manifestations_not_work_identities(self) -> None:
        entities = self.entities()
        proposal = load_json(ROOT / "records/proposed-gifts/6529NM-PG-2026-001/proposal.json")
        for index, source in enumerate(proposal["objects"], start=24):
            work = entities[f"6529NM-W-{index:04d}"]["profile"]
            manifestation = work["manifestation_references"]
            self.assertEqual(len(manifestation), 1)
            self.assertEqual(manifestation[0]["record_id"], f"{source['candidate_object_id']}.TOKEN")
            self.assertEqual(manifestation[0]["source_record_id"], source["candidate_object_id"])
            self.assertEqual(manifestation[0]["caip19"], f"eip155:1/erc721:{source['contract']}/{source['token_id']}")
            self.assertNotEqual(f"{source['candidate_object_id']}.TOKEN", f"6529NM-W-{index:04d}")

    def test_magnum_project_relations_are_evidence_bound_and_separate_from_acquisition(self) -> None:
        entities = self.entities()
        relations = self.relations()
        project_relations = [relation for relation in relations if relation["relation_type"] == "PROJECT_CONTEXTUALIZES_WORK" and relation["source_entity_id"] == "6529NM-PRJ-0006"]
        self.assertEqual(len(project_relations), 5)
        self.assertEqual({relation["target_entity_id"] for relation in project_relations}, {f"6529NM-W-{index:04d}" for index in range(24, 29)})
        relation_evidence_paths = {
            next(item["uri"] for item in relation["evidence_refs"])
            for relation in project_relations
        }
        self.assertEqual(
            relation_evidence_paths,
            {migration.github_uri(path) for path in migration.MAGNUM_WORK_PUBLICATION_PATHS.values()},
        )
        origin_relation = next(relation for relation in relations if relation["relation_type"] == "ORGANIZATION_ORIGINATES_PROJECT" and relation["target_entity_id"] == "6529NM-PRJ-0006")
        self.assertEqual(origin_relation["source_entity_id"], "6529NM-ORG-0002")
        self.assertEqual(origin_relation["qualifier"]["role"], "originator")
        self.assertEqual(entities["6529NM-PRJ-0006"]["profile"]["agent_entity_ids"], ["6529NM-ORG-0002"])
        self.assertEqual(
            [relation for relation in relations if relation["relation_type"] == "AGENT_PLAYS_ROLE" and relation["target_entity_id"] == "6529NM-PRJ-0006"],
            [],
        )
        self.assertNotEqual(entities["6529NM-PRJ-0006"]["entity_id"], "6529NM-CA-2026-003")
        self.assertTrue(all(work["profile"]["project_or_series_entity_ids"] == ["6529NM-PRJ-0006"] for work in (entities[f"6529NM-W-{index:04d}"] for index in range(24, 29))))
        self.assertTrue(all(entities[relation["target_entity_id"]]["profile"]["collection_membership"]["status"] == "permanent_collection" for relation in project_relations))

    def test_every_work_has_typed_media_and_no_media_reuse(self) -> None:
        entities = self.entities()
        media = {key: value for key, value in entities.items() if value["entity_type"] == "MEDIA_REFERENCE"}
        media_relations = [relation for relation in self.relations() if relation["relation_type"] == "ENTITY_HAS_MEDIA" and entities[relation["source_entity_id"]]["entity_type"] == "WORK"]
        self.assertEqual({relation["source_entity_id"] for relation in media_relations}, {f"6529NM-W-{index:04d}" for index in range(1, 30)})
        target_counts = Counter(relation["target_entity_id"] for relation in media_relations)
        self.assertTrue(all(count == 1 for count in target_counts.values()))
        for relation in media_relations:
            target = media[relation["target_entity_id"]]
            self.assertEqual(target["profile"]["media"]["subject_entity_id"], relation["source_entity_id"])
            self.assertIn(relation["target_entity_id"], entities[relation["source_entity_id"]]["media_entity_ids"])
        keys_media = [value for key, value in media.items() if 20 <= int(key.rsplit("-", 1)[1]) <= 35]
        self.assertEqual(len(keys_media), 16)
        self.assertEqual(len([relation for relation in media_relations if relation["target_entity_id"] in {value["entity_id"] for value in keys_media}]), 16)
        title_corrected_media = media["6529NM-MED-0021"]
        self.assertEqual(title_corrected_media["preferred_label"], "the Artist in the Open Sea presentation record")
        self.assertEqual(title_corrected_media["profile"]["media"]["credit"], "HugoFaz — the Artist in the Open Sea; Keys and Gates presentation record")
        self.assertNotIn("teh Open Sea", json.dumps(title_corrected_media))
        magnum_media = [value for value in media.values() if value["profile"]["media"].get("media_role") == "historical_wave_proposal_presentation"]
        self.assertEqual(len(magnum_media), 5)
        expected_wave_parts_and_sizes = {
            "6529NM-MED-0003": (2, 2_518_674),
            "6529NM-MED-0041": (3, 1_813_285),
            "6529NM-MED-0042": (4, 1_666_083),
            "6529NM-MED-0043": (5, 1_540_870),
            "6529NM-MED-0044": (6, 16_871_807),
        }
        for value in magnum_media:
            media_profile = value["profile"]["media"]
            self.assertTrue(media_profile["source_locator"]["uri"].startswith("https://d3lqz0a4bldqgf.cloudfront.net/drops/"))
            self.assertIsNone(media_profile["source_locator"]["repository_path"])
            self.assertTrue(media_profile["token_source_locator"]["uri"].startswith("https://arweave.net/"))
            self.assertIsNone(media_profile["token_source_locator"]["repository_path"])
            self.assertEqual(media_profile["active_display_source_amendment"]["amendment_id"], "6529NM-MEDIA-CONT-AMD-2026-08-12-001")
            self.assertEqual(media_profile["token_source_fixity"]["digest"], media_profile["fixity"]["digest"])
            self.assertTrue(media_profile["visual"])
            self.assertEqual(media_profile["fixity"]["status"], "verified")
            self.assertEqual(media_profile["publication_boundary"], "historical_wave_proposal_context")
            self.assertEqual(media_profile["publication_context_entity_ids"], ["6529NM-CA-2026-003"])
            expected_part, expected_size = expected_wave_parts_and_sizes[value["entity_id"]]
            self.assertEqual(media_profile["publication_part_number"], expected_part)
            self.assertEqual(media_profile["source_byte_size"], expected_size)
            self.assertEqual(media_profile["wave_proposal_context"]["publication_status"], "historical_public_proposal_context")
            self.assertIn(
                "records/proposed-gifts/6529NM-PG-2026-001/public/scholarship/dossiers/public-presentation.md",
                json.dumps(media_profile["source_observation"]["evidence_refs"]),
            )
            self.assertIn("open_wave_proposal_context", media_profile["allowed_ui_affordances"])
            self.assertIn("view", media_profile["allowed_ui_affordances"])
            self.assertIn("thumbnail", media_profile["allowed_ui_affordances"])
            self.assertIn("hero", media_profile["allowed_ui_affordances"])
            self.assertNotIn("download", media_profile["allowed_ui_affordances"])
            self.assertNotIn("zoom", media_profile["allowed_ui_affordances"])
            self.assertNotIn("fullscreen", media_profile["allowed_ui_affordances"])
            self.assertNotIn("open_repository_path", media_profile["allowed_ui_affordances"])
        age_sensitive_media = next(value for value in magnum_media if value["entity_id"] == "6529NM-MED-0043")["profile"]["media"]
        self.assertEqual(age_sensitive_media["accessibility_subject_policy"], "non_identifying_apparently_young_subject")
        self.assertIn("apparently young person", age_sensitive_media["accessibility_text"].lower())
        self.assertNotRegex(age_sensitive_media["accessibility_text"].lower(), r"\b(child|named|identified|known as)\b")
        self.assertEqual(age_sensitive_media["identity_inference_prohibition"]["status"], "prohibited")
        self.assertEqual(age_sensitive_media["identity_inference_prohibition"]["scope"], "subject_identity_and_age_classification")
        cover = media["6529NM-MED-0004"]["profile"]["media"]
        self.assertEqual(cover["media_role"], "museum_authored_public_graphic")
        self.assertEqual(cover["publication_boundary"], "public_graphic")
        self.assertEqual(cover["subject_entity_id"], "6529NM-CA-2026-003")
        self.assertIsNone(cover["derived_from_media_entity_id"])
        self.assertEqual(cover["rights"]["status"], "cleared")
        self.assertIn("PROPOSED GIFT", cover["accessibility_text"])
        self.assertIn("CONFLICT AT ITS EDGES", cover["accessibility_text"])
        self.assertIn("Five Photographs of Evidence and Aftermath", cover["accessibility_text"])
        self.assertIn("1952–2016", cover["accessibility_text"])
        self.assertIn("6529 NETWORK MUSEUM", cover["accessibility_text"])
        self.assertIn(WAVE_PUBLICATION_OBSERVATION_ID, cover["source_record_ids"])
        self.assertNotIn("6529NM-CA-2026-003", json.dumps(cover["rights"]["evidence_refs"]))
        self.assertNotIn("6529NM-CA-2026-003", json.dumps(cover["source_observation"]["evidence_refs"]))
        self.assertNotIn("hero", cover["allowed_ui_affordances"])
        self.assertIn("text-only historical proposal graphic", cover["transform_profile"])
        keys_media = [value for value in media.values() if value["profile"]["media"].get("media_role") == "museum_generated_public_derivative" and any(ref.startswith("6529NM-AP-01-OUT-") for ref in value["profile"]["media"].get("source_record_ids", []))]
        self.assertEqual(len(keys_media), 16)
        for value in keys_media:
            media_profile = value["profile"]["media"]
            authority_path = "records/programs/6529NM-AP-01/public/media-display-authorization-amendment-2026-08-11.md"
            expected_width = 640 if media_profile["subject_entity_id"] in {"6529NM-W-0011", "6529NM-W-0018"} else 1280
            self.assertEqual(media_profile["width"], expected_width)
            self.assertEqual(media_profile["rights"]["status"], "cleared_with_conditions")
            self.assertEqual(media_profile["accessibility_status"], "provided")
            self.assertTrue(media_profile["visual"])
            self.assertTrue(media_profile["source_locator"]["uri"].startswith("https://d3lqz0a4bldqgf.cloudfront.net/museum/programs/6529NM-AP-01/"))
            self.assertTrue(media_profile["source_locator"]["repository_path"].startswith("media/programs/6529NM-AP-01/"))
            self.assertEqual(media_profile["allowed_ui_affordances"], ["view", "thumbnail", "hero", "alt_text", "copy_citation"])
            self.assertEqual(media_profile["source_observation"]["status"], "retrieved")
            self.assertEqual(media_profile["fixity"]["status"], "verified")
            self.assertEqual(value["effective_at"], "2026-08-11T21:56:04Z")
            self.assertEqual(value["observed_at"], "2026-08-11T21:56:04Z")
            self.assertEqual(media_profile["rights"]["observed_at"], "2026-08-11T21:56:04Z")
            self.assertEqual(media_profile["source_observation"]["observed_at"], "2026-08-11T21:56:04Z")
            self.assertNotIn("6529NM-AP-01-MEDIA-DELIVERY-2026-08-09-008", media_profile["source_record_ids"])
            self.assertIn(authority_path, json.dumps(media_profile["source_observation"]["evidence_refs"]))
            self.assertIn(authority_path, json.dumps(value["evidence_refs"]))
            self.assertIn(authority_path, json.dumps(media_profile["rights"]["evidence_refs"]))
            self.assertIn(authority_path, json.dumps(media_profile["source_observation"]["evidence_refs"]))
        generated_json = json.dumps(self.records, ensure_ascii=False)
        self.assertNotIn("OUT-004/1280.webp", generated_json)
        self.assertNotIn("OUT-004/2400.webp", generated_json)
        self.assertNotIn("OUT-011/1280.webp", generated_json)
        self.assertNotIn("OUT-011/2400.webp", generated_json)

    def test_casey_media_presentation_correction_is_exact(self) -> None:
        entities = self.entities()
        relations = {relation["relation_id"]: relation for relation in self.relations()}
        amendment = load_json(
            ROOT / "records/accessions/6529NM.2026.001/media-presentation-amendment-2026-08-09.json"
        )["payload"]
        corrections = amendment["presentation_corrections"]

        self.assertEqual(len(entities), 136)
        self.assertEqual(len(relations), 233)
        self.assertEqual(
            len([entity for entity in entities.values() if entity["entity_type"] == "MEDIA_REFERENCE"]),
            40,
        )
        self.assertEqual(len(corrections), 7)

        for index, correction in enumerate(corrections, start=1):
            work_id = f"6529NM-W-{index:04d}"
            still_id = f"6529NM-MED-{44 + index:04d}"
            live_id = f"6529NM-MED-{9 + index:04d}"
            still_relation_id = f"6529NM-REL-{211 + index:04d}"
            live_relation_id = f"6529NM-REL-{125 + index:04d}"
            expected_media = [still_id, live_id]
            if index == 1:
                expected_media.extend(["6529NM-MED-0001", "6529NM-MED-0002"])

            self.assertEqual(correction["work_entity_id"], work_id)
            self.assertEqual(correction["still_media_entity_id"], still_id)
            self.assertEqual(correction["live_media_entity_id"], live_id)
            self.assertEqual(entities[work_id]["media_entity_ids"], expected_media)

            still = entities[still_id]["profile"]["media"]
            self.assertTrue(still["visual"])
            self.assertEqual(still["media_type"], "image/png")
            self.assertEqual(still["source_observation"]["status"], "mutable_external")
            self.assertEqual(still["fixity"]["status"], "verified")
            self.assertEqual(still["fixity"]["digest"], correction["still"]["response_sha256"])
            self.assertIn("exact observed Art Blocks media-proxy image response", still["fixity"]["basis"])
            self.assertIn("future bytes may differ", still["fixity"]["basis"])
            self.assertIn("not retained as a Museum preservation master", still["fixity"]["basis"])
            self.assertEqual(still["accessibility_text"], correction["accessibility_text"])
            self.assertEqual(still["credit"], correction["credit"])
            self.assertEqual(still["rights"]["status"], "cleared_with_conditions")
            self.assertTrue(
                any(
                    ref["uri"] == correction["license_url"]
                    for ref in still["rights"]["evidence_refs"]
                )
            )
            self.assertEqual(still["allowed_ui_affordances"], correction["still"]["allowed_ui_affordances"])
            self.assertEqual((still["width"], still["height"]), (
                correction["still"]["dimensions"]["width"],
                correction["still"]["dimensions"]["height"],
            ))

            live = entities[live_id]["profile"]["media"]
            self.assertTrue(live["visual"])
            self.assertEqual(live["media_type"], "text/html")
            self.assertEqual(live["source_observation"]["status"], "mutable_external")
            self.assertEqual(live["fixity"]["status"], "unverified_not_retrieved")
            self.assertIsNone(live["fixity"]["digest"])
            self.assertEqual(live["accessibility_text"], correction["accessibility_text"])
            self.assertEqual(live["credit"], correction["credit"])
            self.assertEqual(live["rights"]["status"], "cleared_with_conditions")
            self.assertIn("interact_sandboxed", live["allowed_ui_affordances"])
            self.assertEqual(live["allowed_ui_affordances"], correction["live"]["allowed_ui_affordances"])

            self.assertEqual(relations[still_relation_id]["source_entity_id"], work_id)
            self.assertEqual(relations[still_relation_id]["target_entity_id"], still_id)
            self.assertEqual(relations[still_relation_id]["qualifier"], {"media_context": "primary", "display_order": 1})
            self.assertEqual(relations[live_relation_id]["source_entity_id"], work_id)
            self.assertEqual(relations[live_relation_id]["target_entity_id"], live_id)
            self.assertEqual(relations[live_relation_id]["qualifier"], {"media_context": "primary", "display_order": 2})

        preprocess = entities["6529NM-MED-0048"]["profile"]["media"]
        self.assertEqual((preprocess["width"], preprocess["height"]), (2400, 1349))
        self.assertIn(
            "PNG image response and not live canvas geometry",
            " ".join(amendment["immutable_boundaries"]),
        )

    def test_casey_media_correction_preserves_other_program_boundaries(self) -> None:
        entities = self.entities()
        for entity_id in ("6529NM-MED-0001", "6529NM-MED-0002"):
            media = entities[entity_id]["profile"]["media"]
            self.assertFalse(media["visual"])
            self.assertEqual(media["media_type"], "application/json")
        for index in range(20, 36):
            media = entities[f"6529NM-MED-{index:04d}"]["profile"]["media"]
            self.assertTrue(media["visual"])
            self.assertNotIn("6529NM-MEDIA-PRES-AMD-2026-08-09-001", media["source_record_ids"])
        for index in range(41, 45):
            media = entities[f"6529NM-MED-{index:04d}"]["profile"]["media"]
            self.assertTrue(media["visual"])
            self.assertNotIn("6529NM-MEDIA-PRES-AMD-2026-08-09-001", media["source_record_ids"])

    def test_casey_media_amendment_affordances_are_closed(self) -> None:
        amendment_path = ROOT / "records/accessions/6529NM.2026.001/media-presentation-amendment-2026-08-09.json"
        schema_path = "schemas/media-presentation-amendment.schema.json"
        amendment = load_json(amendment_path)
        for surface in ("still", "live"):
            mutated = copy.deepcopy(amendment)
            mutated["payload"]["presentation_corrections"][0][surface]["allowed_ui_affordances"].append("unsafe_unknown_affordance")
            self.assertTrue(self.local_schema_issues(mutated["payload"], schema_path), surface)

    def test_collection_membership_is_exactly_the_three_completed_accessions(self) -> None:
        entities = self.entities()
        relations = self.relations()
        collection_relations = [relation for relation in relations if relation["relation_type"] == "COLLECTION_CONTAINS_WORK"]
        accession_relations = [relation for relation in relations if relation["relation_type"] == "ACCESSION_ADMITS_WORK"]
        expected = {
            *{f"6529NM-W-{index:04d}" for index in range(1, 8)},
            *{f"6529NM-W-{index:04d}" for index in range(24, 29)},
            "6529NM-W-0029",
        }
        self.assertEqual(len(collection_relations), 13)
        self.assertEqual(len(accession_relations), 13)
        self.assertEqual({relation["target_entity_id"] for relation in collection_relations}, expected)
        self.assertTrue(all(entities[relation["target_entity_id"]]["profile"]["collection_membership"]["status"] == "permanent_collection" for relation in collection_relations))
        permanent_work_ids = {entity_id for entity_id, payload in entities.items() if payload["entity_type"] == "WORK" and payload["profile"]["collection_membership"]["status"] == "permanent_collection"}
        self.assertEqual(permanent_work_ids, {relation["target_entity_id"] for relation in accession_relations})
        self.assertTrue(all(entities[f"6529NM-W-{index:04d}"]["profile"]["collection_membership"]["status"] == "permanent_collection" for index in range(24, 29)))
        self.assertTrue(all(entities[f"6529NM-W-{index:04d}"]["profile"]["collection_membership"]["status"] == "not_in_collection" for index in range(8, 24)))

    def test_membership_relation_lists_and_reverse_fields_fail_closed(self) -> None:
        mutations = (
            ("collection relation removal", "COLLECTION_CONTAINS_WORK", "6529NM-C-0001", "6529NM-W-0001", "Collection admitted_work_entity_ids must equal"),
            ("project relation removal", "PROJECT_CONTEXTUALIZES_WORK", "6529NM-PRJ-0001", "6529NM-W-0001", "Project work_entity_ids must equal"),
            ("acquisition relation removal", "CURATED_ACQUISITION_BRINGS_TOGETHER_WORK", "6529NM-CA-2026-001", "6529NM-W-0001", "Curated Acquisition work_entity_ids must equal"),
            ("accession relation removal", "ACCESSION_ADMITS_WORK", "6529NM-ACC-ENT-0001", "6529NM-W-0001", "Accession admitted_work_entity_ids must equal"),
        )
        for name, relation_type, source_id, target_id, expected in mutations:
            with self.subTest(name=name):
                mutated = copy.deepcopy(self.records)
                relation_key = next(
                    key for key, record in mutated.items()
                    if record["payload"].get("relation_type") == relation_type
                    and record["payload"].get("source_entity_id") == source_id
                    and record["payload"].get("target_entity_id") == target_id
                )
                del mutated[relation_key]
                issues = self.graph_issues(mutated)
                self.assertTrue(any(expected in issue for issue in issues), issues)
                if relation_type == "COLLECTION_CONTAINS_WORK":
                    self.assertTrue(any("permanent Collection membership must equal exactly one active" in issue for issue in issues), issues)
                else:
                    self.assertTrue(any("Work " in issue and "must equal active" in issue for issue in issues), issues)

        collection_qualifier = copy.deepcopy(self.records)
        collection_relation = next(
            record["payload"] for record in collection_qualifier.values()
            if record["payload"].get("relation_type") == "COLLECTION_CONTAINS_WORK"
        )
        collection_relation["qualifier"]["collection_membership_status"] = "not_in_collection"
        self.assertTrue(any("membership qualifier must equal" in issue for issue in self.graph_issues(collection_qualifier)))

        reverse_field = copy.deepcopy(self.records)
        reverse_work = next(record["payload"] for record in reverse_field.values() if record["payload"].get("entity_id") == "6529NM-W-0001")
        reverse_work["profile"]["project_or_series_entity_ids"] = []
        self.assertTrue(any("Work project_or_series_entity_ids must equal active" in issue for issue in self.graph_issues(reverse_field)))

        membership_source = copy.deepcopy(self.records)
        membership_work = next(record["payload"] for record in membership_source.values() if record["payload"].get("entity_id") == "6529NM-W-0001")
        membership_work["profile"]["collection_membership"]["collection_entity_id"] = "6529NM-C-9999"
        self.assertTrue(any("Work collection_entity_id must equal" in issue for issue in self.graph_issues(membership_source)))

    def test_magnum_mint_is_chain_verified_independently_of_completed_accession(self) -> None:
        entities = self.entities()
        for index in range(24, 29):
            work = entities[f"6529NM-W-{index:04d}"]["profile"]
            self.assertEqual(work["mint_fact"]["status"], "verified")
            self.assertEqual(work["mint_fact"]["evidence_refs"][0]["evidence_class"], "A")
            self.assertTrue(work["mint_fact"]["evidence_refs"][0]["uri"].endswith("evidence/magnum-75-custody/summary.json"))
            self.assertIn("independently of title, custody, rights, and accession", work["mint_fact"]["notes"])
            self.assertEqual(work["collection_membership"]["status"], "permanent_collection")
            self.assertEqual(work["accession_entity_ids"], ["6529NM-ACC-ENT-0002"])
        ca3 = entities["6529NM-CA-2026-003"]["profile"]
        self.assertEqual(ca3["independent_acquisition_facts"]["mint"]["status"], "verified")
        self.assertEqual(ca3["independent_acquisition_facts"]["mint"]["evidence_refs"][0]["evidence_class"], "A")
        self.assertIn("independently of title, custody, rights, and accession", ca3["independent_acquisition_facts"]["mint"]["notes"])

    def test_conflict_downstream_accession_facts_follow_wave_selection(self) -> None:
        entities = self.entities()
        ca3 = entities["6529NM-CA-2026-003"]["profile"]
        selection_at = ca3["lifecycle_observations"][1]["observed_at"]
        for fact_name in ("rights", "technical", "display"):
            accession_fact = ca3["independent_acquisition_facts"][fact_name]
            self.assertEqual(accession_fact["status"], "verified_with_conditions")
            self.assertGreater(accession_fact["as_of"], selection_at)
            self.assertTrue(accession_fact["notes"])
        for media_id in ("6529NM-MED-0003", "6529NM-MED-0041", "6529NM-MED-0042", "6529NM-MED-0043", "6529NM-MED-0044"):
            media = entities[media_id]
            self.assertGreater(media["effective_at"], selection_at)
            self.assertIn("downstream-accession", media["preferred_label"])

    def test_program_pathways_and_produced_acquisitions_are_exact(self) -> None:
        entities = self.entities()
        programs = {entity_id: payload for entity_id, payload in entities.items() if payload["entity_type"] == "ACQUISITION_PROGRAM"}
        relations = self.relations()
        produced = {
            program_id: {relation["target_entity_id"] for relation in relations if relation["relation_type"] == "ACQUISITION_PROGRAM_PRODUCES_ACQUISITION" and relation["source_entity_id"] == program_id}
            for program_id in programs
        }
        self.assertEqual(programs["6529NM-AP-ENT-0001"]["profile"]["program_status"], "active")
        self.assertEqual(entities["6529NM-CA-2026-002"]["profile"]["thesis"], "The program’s selected group brings together photographs of access, exclusion, permission, surveillance, custody, autonomy, and exit; selection is complete, while acquisition and minting remain pending.")
        self.assertEqual(produced["6529NM-AP-ENT-0001"], {"6529NM-CA-2026-001", "6529NM-CA-2026-003", "6529NM-CA-2026-004"})
        self.assertEqual(programs["6529NM-AP-ENT-0001"]["profile"]["produced_acquisition_entity_ids"], sorted(produced["6529NM-AP-ENT-0001"]))
        self.assertEqual(produced["6529NM-AP-ENT-0002"], {"6529NM-CA-2026-002"})
        self.assertEqual(entities["6529NM-CA-2026-001"]["profile"]["program_or_pathway"]["entity_ids"], ["6529NM-AP-ENT-0001"])
        self.assertEqual(entities["6529NM-CA-2026-003"]["profile"]["program_or_pathway"]["entity_ids"], ["6529NM-AP-ENT-0001"])
        self.assertEqual(entities["6529NM-CA-2026-004"]["profile"]["program_or_pathway"]["entity_ids"], ["6529NM-AP-ENT-0001"])
        self.assertEqual(entities["6529NM-CA-2026-002"]["profile"]["program_or_pathway"]["entity_ids"], ["6529NM-AP-ENT-0002"])
        self.assertTrue(all(entities[f"6529NM-W-{index:04d}"]["profile"]["program_entity_ids"] == ["6529NM-AP-ENT-0001"] for index in [*range(1, 8), *range(24, 30)]))
        self.assertTrue(all(entities[f"6529NM-W-{index:04d}"]["profile"]["program_entity_ids"] == ["6529NM-AP-ENT-0002"] for index in range(8, 24)))
        self.assertEqual([relation for relation in relations if relation["relation_type"] == "COLLECTION_CONTAINS_WORK" and entities[relation["source_entity_id"]]["entity_type"] == "ACQUISITION_PROGRAM"], [])

    def test_art_blocks_publishes_casey_projects_without_false_origination(self) -> None:
        relations = self.relations()
        publishes = [relation for relation in relations if relation["relation_type"] == "ORGANIZATION_PUBLISHES_PROJECT"]
        self.assertEqual(len(publishes), 5)
        self.assertTrue(all(relation["source_entity_id"] == "6529NM-ORG-0001" and relation["qualifier"]["role"] == "publisher" for relation in publishes))
        self.assertEqual([relation for relation in relations if relation["relation_type"] == "ORGANIZATION_ORIGINATES_PROJECT" and relation["target_entity_id"] != "6529NM-PRJ-0006"], [])

    def test_project_agents_have_source_backed_bidirectional_role_relations(self) -> None:
        entities = self.entities()
        relations = [relation for relation in self.relations() if relation["relation_type"] in {"AGENT_PLAYS_ROLE", "ORGANIZATION_ORIGINATES_PROJECT"}]
        self.assertEqual(len(relations), 8)
        for project_id, project in entities.items():
            if project["entity_type"] != "PROJECT_OR_SERIES":
                continue
            project_relations = [relation for relation in relations if relation["target_entity_id"] == project_id]
            self.assertEqual({relation["source_entity_id"] for relation in project_relations}, set(project["profile"]["agent_entity_ids"]))
            for relation in project_relations:
                self.assertIsInstance(relation["qualifier"].get("role"), str)
                self.assertTrue(relation["qualifier"]["role"])
                self.assertTrue(set(relation["source_record_ids"]).intersection(project["profile"]["source_record_ids"]))

    def test_envelope_uris_are_canonical_repository_paths(self) -> None:
        for relative_path, record in self.records.items():
            self.assertEqual(record["envelope"]["uri"], f"https://6529networkmuseum.org/{relative_path}")
            self.assertNotIn("/records/records/", record["envelope"]["uri"])

    def test_wave_publication_observation_evidence_uses_public_locator_and_observation_time(self) -> None:
        matches: list[dict] = []

        def visit(value: object) -> None:
            if isinstance(value, dict):
                uri = value.get("uri")
                if uri == migration.WINNER_SOURCE_URL and value.get("label") == "Historical public Wave proposal presentation":
                    matches.append(value)
                for child in value.values():
                    visit(child)
            elif isinstance(value, list):
                for child in value:
                    visit(child)

        visit(self.records)
        self.assertTrue(matches)
        self.assertTrue(all(row.get("observed_at") == WINNER_AT for row in matches))
        self.assertNotIn(WAVE_PUBLICATION_OBSERVATION_PATH, json.dumps(self.records))

    def test_typed_work_references_resolve_to_authoritative_or_governed_targets(self) -> None:
        entities = self.entities()
        registry_targets = self.inventory["typed_reference_registry"]
        registry_by_target = {(row["reference_type"], row["target_id"]): row for row in registry_targets}
        for work_id, work in entities.items():
            if work["entity_type"] != "WORK":
                continue
            for field in ("component_references", "manifestation_references"):
                expected_type = field.removesuffix("_references")
                for reference in work["profile"][field]:
                    self.assertEqual(reference["reference_type"], expected_type)
                    self.assertIn(reference["source_record_id"], work["references"])
                    self.assertIn(reference["target_kind"], {"authoritative_record", "governed_typed_registry"})
                    if reference["target_kind"] == "authoritative_record":
                        self.assertEqual(reference["record_id"], reference["source_record_id"])
                        self.assertIsNone(reference["registry_id"])
                    else:
                        target = registry_by_target[(expected_type, reference["record_id"])]
                        self.assertEqual(reference["registry_id"], "PUBLIC_TYPED_REFERENCE_REGISTRY_V1")
                        self.assertEqual(reference["target_type"], target["target_type"])
                        self.assertEqual(reference["source_record_id"], target["authoritative_record_id"])
                        expected_authority_type = (
                            "WORK_DESCRIPTION"
                            if work_id == "6529NM-W-0029"
                            else "PROPOSED_GIFT"
                        )
                        self.assertEqual(target["authoritative_record_type"], expected_authority_type)
                        self.assertEqual(reference["caip19"], target["caip19"])
        self.assertEqual(self.graph_issues(), [])

    def test_typed_reference_target_mutations_fail_closed(self) -> None:
        missing_target = copy.deepcopy(self.records)
        missing_ref = next(record["payload"] for record in missing_target.values() if record["payload"].get("entity_id") == "6529NM-W-0001")["profile"]["component_references"][0]
        missing_ref["record_id"] = "6529NM.2026.001.999"
        self.assertTrue(any("does not resolve" in issue or "must equal source_record_id" in issue for issue in self.graph_issues(missing_target)))

        mismatched_type = copy.deepcopy(self.records)
        mismatched_ref = next(record["payload"] for record in mismatched_type.values() if record["payload"].get("entity_id") == "6529NM-W-0001")["profile"]["component_references"][0]
        mismatched_ref["target_type"] = "GOVERNANCE_DECISION"
        self.assertTrue(any("mismatched" in issue or "expected one of" in issue for issue in self.graph_issues(mismatched_type)))

        mismatched_registry = copy.deepcopy(self.records)
        registry_ref = next(record["payload"] for record in mismatched_registry.values() if record["payload"].get("entity_id") == "6529NM-W-0024")["profile"]["manifestation_references"][0]
        registry_ref["caip19"] = "eip155:1/erc721:0xe628b59d34f42b16c53f4d697f1ffd4d8d987b91/999"
        self.assertTrue(any("mismatched CAIP-19" in issue for issue in self.graph_issues(mismatched_registry)))

        missing_metadata = copy.deepcopy(self.entities()["6529NM-W-0008"])
        missing_metadata["profile"]["component_references"][0].pop("target_kind")
        self.assertTrue(self.schema_issues(missing_metadata, "https://6529networkmuseum.org/schemas/public-entity-v1.json"))

    def test_typed_reference_matrix_and_ambiguous_authoritative_target_fail_closed(self) -> None:
        component_matrix = copy.deepcopy(self.entities()["6529NM-W-0001"])
        component_matrix["profile"]["component_references"][0]["target_type"] = "VISUAL_OBSERVATION"
        self.assertTrue(self.schema_issues(component_matrix, "https://6529networkmuseum.org/schemas/public-entity-v1.json"))
        self.assertTrue(any("closed target_type matrix" in issue for issue in self.graph_issues({**self.records, "mutated-component": {"payload": component_matrix}})))

        manifestation_matrix = copy.deepcopy(self.entities()["6529NM-W-0001"])
        manifestation_matrix["profile"]["manifestation_references"][0]["target_type"] = "PROGRAM_OUTCOME"
        self.assertTrue(self.schema_issues(manifestation_matrix, "https://6529networkmuseum.org/schemas/public-entity-v1.json"))
        self.assertTrue(any("closed target_type matrix" in issue for issue in self.graph_issues({**self.records, "mutated-manifestation": {"payload": manifestation_matrix}})))

        ambiguous = {
            "6529NM.2026.001.01": {
                ("WORK_DESCRIPTION", Path("records/one.json")),
                ("WORK_DESCRIPTION", Path("records/two.json")),
            }
        }
        with patch("validate._typed_reference_record_index", return_value=ambiguous):
            issues = self.graph_issues()
        self.assertTrue(any("must resolve to exactly one WORK_DESCRIPTION" in issue for issue in issues), issues)

        registry_ambiguity = {
            "6529NM-PG-2026-001.OBJ-001": {
                ("PROPOSED_GIFT", Path("records/proposal-one.json")),
                ("PROPOSED_GIFT", Path("records/proposal-two.json")),
            }
        }
        with patch("validate._typed_reference_record_index", return_value=registry_ambiguity):
            issues = self.graph_issues()
        self.assertTrue(
            any("must resolve to exactly one PROPOSED_GIFT authoritative source record" in issue for issue in issues),
            issues,
        )

    def test_contextual_program_media_are_structurally_fail_closed(self) -> None:
        for entity_id in ("6529NM-MED-0020", "6529NM-MED-0041"):
            with self.subTest(entity_id=entity_id):
                baseline = copy.deepcopy(self.entities()[entity_id])
                self.assertEqual(validate_public_media(baseline["profile"]["media"], entity_id), [])
                self.assertEqual(self.schema_issues(baseline, "https://6529networkmuseum.org/schemas/public-entity-v1.json"), [])
                for name, mutate in (
                    ("source locator", lambda media: media["source_locator"].update({"uri": "https://example.org/media", "repository_path": None})),
                    ("visual", lambda media: media.update({"visual": False})),
                    ("download affordance", lambda media: media["allowed_ui_affordances"].append("download")),
                ):
                    with self.subTest(name=name):
                        mutated = copy.deepcopy(baseline)
                        mutate(mutated["profile"]["media"])
                        self.assertTrue(validate_public_media(mutated["profile"]["media"], f"{entity_id}.{name}"))

    def test_project_agent_relation_mutations_fail_closed(self) -> None:
        missing_relation = copy.deepcopy(self.records)
        relation_key = next(key for key, record in missing_relation.items() if record["payload"].get("relation_type") == "AGENT_PLAYS_ROLE" and record["payload"].get("target_entity_id") == "6529NM-PRJ-0001")
        del missing_relation[relation_key]
        self.assertTrue(any("Project agent_entity_ids must equal" in issue for issue in self.graph_issues(missing_relation)))

        missing_role = copy.deepcopy(self.records)
        relation = next(record["payload"] for record in missing_role.values() if record["payload"].get("relation_type") == "AGENT_PLAYS_ROLE")
        relation["qualifier"].pop("role")
        self.assertTrue(any("missing required qualifiers" in issue or "requires a non-empty role" in issue for issue in self.graph_issues(missing_role)))

    def test_evidence_classes_are_explicit_and_label_independent(self) -> None:
        self.assertEqual(EVIDENCE_CLASSES, {"A", "B", "C", "D", "E"})
        self.assertEqual(source_record_evidence_class("eip155:1/erc721:0xabc/1"), "A")
        self.assertEqual(source_record_evidence_class("6529NM-GOV-1052812"), "B")
        self.assertEqual(source_record_evidence_class("6529NM.2026.001.DILIGENCE-01"), "C")
        self.assertEqual(source_record_evidence_class("records/accessions/6529NM.2026.001/public/casey-reas-collection-essay.md"), "E")
        self.assertEqual(source_record_evidence_class("sources/third-party/historical-reference.md"), "D")
        original = source_evidence("Governance claim", "6529NM-GOV-1052812", GENERATED_AT)
        relabeled = source_evidence("An editor changed this label", "6529NM-GOV-1052812", GENERATED_AT)
        self.assertEqual(original["evidence_class"], "B")
        self.assertEqual(relabeled["evidence_class"], original["evidence_class"])

    def test_review_pending_candidate_state_is_not_archived_and_cannot_be_final(self) -> None:
        candidate = build_records()
        candidate_entities = [record["payload"] for record in candidate.values() if record["payload"].get("record_type") == "PUBLIC_ENTITY"]
        self.assertEqual(len(candidate_entities), 136)
        self.assertTrue(all(payload["entity_status"] == "review_pending" for payload in candidate_entities))
        self.assertTrue(all(payload["record_status"] == "review_pending" for payload in candidate_entities))
        self.assertTrue(all(payload["reviewer"] is None for payload in candidate_entities))
        finalised_candidate = copy.deepcopy(candidate_entities[0])
        finalised_candidate["record_status"] = "reviewed"
        finalised_candidate["review_status"] = "reviewed"
        finalised_candidate["reviewer"] = {"id": "codex-review:test-independent", "reviewed_at": "2026-08-08T15:00:00Z"}
        finalised_candidate["entity_status"] = "review_pending"
        issues = validate_public_payload(finalised_candidate, self.vocabularies, self.inventory)
        self.assertTrue(any("reviewed publication must use entity_status published" in issue for issue in issues))

    def test_control_plane_projection_totals_and_presentation_states_are_current(self) -> None:
        control_plane = (ROOT / "docs/control-plane.md").read_text(encoding="utf-8")
        self.assertIn("136 `PUBLIC_ENTITY` records, 233 closed", control_plane)
        self.assertIn("(370 generated records in total)", control_plane)
        self.assertIn("all 7 Casey Works have an official visual still", control_plane)
        self.assertIn("13 permanent Collection memberships", control_plane)
        self.assertIn("five accessioned Magnum", control_plane)
        self.assertNotIn("120 `PUBLIC_ENTITY` records, 205 closed", control_plane)
        self.assertNotIn("(326 generated records in total)", control_plane)

    def test_wave_receipt_and_visual_amendment_are_exact_and_mutation_safe(self) -> None:
        receipt = load_json(ROOT / "records/proposed-gifts/6529NM-PG-2026-001/wave-publication-observation-2026-08-08.json")
        amendment = load_json(ROOT / "records/proposed-gifts/6529NM-PG-2026-001/media-description-amendment-2026-08-08.json")
        self.assertEqual(validate_wave_publication_observation(receipt["payload"], ROOT), [])
        self.assertEqual(validate_media_description_amendment(amendment["payload"], ROOT), [])
        historical_part = (ROOT / receipt["payload"]["parts"][3]["source_path"]).read_text(encoding="utf-8")
        self.assertIn("tear gas", historical_part.casefold())
        self.assertNotIn("tear gas", amendment["payload"]["current_accessibility_text"].casefold())
        changed_url = copy.deepcopy(receipt["payload"])
        changed_url["parts"][1]["media_url"] = changed_url["parts"][1]["media_url"].replace("magnum-75-127.jpg", "magnum-75-127-mutated.jpg")
        self.assertTrue(validate_wave_publication_observation(changed_url, ROOT))
        changed_hash = copy.deepcopy(receipt["payload"])
        changed_hash["parts"][1]["content_sha256"] = "sha256:" + "1" * 64
        self.assertTrue(validate_wave_publication_observation(changed_hash, ROOT))
        with self.assertRaises(DuplicateJsonKeyError):
            json.loads('{"drop_id":"one","drop_id":"two"}', object_pairs_hook=reject_duplicate_keys)

    def test_media_amendment_binds_append_only_predecessor_part_and_hash(self) -> None:
        receipt = load_json(ROOT / "records/proposed-gifts/6529NM-PG-2026-001/wave-publication-observation-2026-08-08.json")
        amendment = load_json(ROOT / "records/proposed-gifts/6529NM-PG-2026-001/media-description-amendment-2026-08-08.json")
        payload = amendment["payload"]
        self.assertEqual(payload["supersedes"], WAVE_PUBLICATION_OBSERVATION_ID)
        self.assertEqual(payload["prior_payload_sha256"], receipt["payload"]["payload_sha256"])
        self.assertEqual(payload["superseded_part_id"], 4)
        self.assertEqual(payload["superseded_content_sha256"], receipt["payload"]["parts"][3]["content_sha256"])
        amendment_schema = load_json(ROOT / "schemas/media-description-amendment.schema.json")
        amendment_validator = validator_for(amendment_schema, self.schema_store)
        self.assertEqual(list(amendment_validator.iter_errors(payload)), [])
        for field, value in {
            "supersedes": "6529NM-WAVE-PUB-OBS-2026-08-08-999",
            "prior_payload_sha256": "sha256:" + "1" * 64,
            "superseded_part_id": 3,
            "superseded_content_sha256": "sha256:" + "2" * 64,
        }.items():
            mutated = copy.deepcopy(payload)
            mutated[field] = value
            self.assertTrue(list(amendment_validator.iter_errors(mutated)), field)
            self.assertTrue(validate_media_description_amendment(mutated, ROOT), field)
        missing_supersedes = copy.deepcopy(payload)
        missing_supersedes.pop("supersedes")
        self.assertTrue(list(amendment_validator.iter_errors(missing_supersedes)))
        self.assertTrue(validate_media_description_amendment(missing_supersedes, ROOT))

    def test_migrator_rejects_duplicate_json_keys_before_last_key_wins(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            source = Path(temporary_directory) / "duplicate.json"
            source.write_text('{"record_id":"first","record_id":"second"}', encoding="utf-8")
            with self.assertRaises(migration.DuplicateJsonKeyError):
                migration.load_json(source)

    def test_retired_identity_tombstone_blocks_reuse_without_resurrecting_agent(self) -> None:
        self.assertNotIn("6529NM-AGT-0012", self.entities())
        tombstone = next(row for row in self.inventory["retired_identity_ids"] if row["entity_id"] == "6529NM-AGT-0012")
        self.assertEqual(tombstone["superseded_by"], "6529NM-AGT-0003")
        mutated = copy.deepcopy(self.inventory)
        mutated["identity_bindings"]["AGENT"].append({"source_key": "hugo-duplicate", "entity_id": "6529NM-AGT-0012"})
        with self.assertRaises(ValueError):
            identity_binding_indexes(mutated)

    def test_all_lifecycle_observations_are_inventory_bound(self) -> None:
        observations = {
            observation["observation_id"]: work_id
            for work_id, work in self.entities().items()
            if work["entity_type"] == "WORK"
            for observation in work["profile"]["lifecycle_observations"]
        }
        expected = {row["entity_id"] for row in self.inventory["identity_bindings"]["WORK_LIFECYCLE_OBSERVATION"]}
        self.assertEqual(len(observations), 39)
        self.assertEqual(set(observations), expected)
        self.assertEqual(len(set(observations)), 39)
        for observation_id, work_id in observations.items():
            self.assertIn(work_id, self.entities())

    def test_every_public_entity_is_exactly_identity_inventory_bound(self) -> None:
        indexes = identity_binding_indexes(self.inventory)
        expected = {
            entity_id: entity_type
            for entity_type in migration.IDENTITY_BINDING_ENTITY_TYPES
            for entity_id in indexes[entity_type].values()
        }
        actual = {entity_id: payload["entity_type"] for entity_id, payload in self.entities().items()}
        self.assertEqual(actual, expected)
        self.assertEqual(len(actual), sum(len(indexes[entity_type]) for entity_type in migration.IDENTITY_BINDING_ENTITY_TYPES))

    def test_static_public_identities_and_casey_research_route_fail_closed(self) -> None:
        expected_static = {
            "INSTITUTION": {"6529NM-I-0001"},
            "COLLECTION": {"6529NM-C-0001"},
            "ACCESSION": {"6529NM-ACC-ENT-0001", "6529NM-ACC-ENT-0002", "6529NM-ACC-ENT-0003"},
            "RESEARCH_PUBLICATION": {"6529NM-RP-0001", "6529NM-RP-0002", "6529NM-RP-0003"},
        }
        indexes = identity_binding_indexes(self.inventory)
        for entity_type, expected_ids in expected_static.items():
            self.assertEqual(set(indexes[entity_type].values()), expected_ids)
        casey_slug = next(row for row in self.inventory["public_slug_inventory"] if row["entity_id"] == "6529NM-RP-0001")
        self.assertEqual(casey_slug["canonical_route"], "/museum/network/research/the-system-in-seven-states")

        original_load_json = migration.load_json
        for entity_type, source_key in (
            ("INSTITUTION", "6529-network-museum"),
            ("COLLECTION", "permanent-collection"),
            ("ACCESSION", "6529NM.2026.001"),
            ("RESEARCH_PUBLICATION", "the-system-in-seven-states"),
        ):
            with self.subTest(entity_type=entity_type):
                mutated = copy.deepcopy(self.inventory)
                mutated["identity_bindings"][entity_type] = [
                    row for row in mutated["identity_bindings"][entity_type] if row["source_key"] != source_key
                ]

                def mutated_load_json(path: Path):
                    if path == migration.IDENTITY_INVENTORY_PATH:
                        return mutated
                    return original_load_json(path)

                with patch.object(migration, "load_json", side_effect=mutated_load_json):
                    with self.assertRaises(ValueError):
                        migration.build_records()

    def test_full_validator_rejects_identity_and_slug_inventory_omissions(self) -> None:
        tuples = [(ROOT / relative, record, record.get("payload")) for relative, record in self.records.items()]
        for entity_type, entity_id in (
            ("INSTITUTION", "6529NM-I-0001"),
            ("COLLECTION", "6529NM-C-0001"),
            ("ACCESSION", "6529NM-ACC-ENT-0001"),
            ("RESEARCH_PUBLICATION", "6529NM-RP-0001"),
        ):
            with self.subTest(entity_type=entity_type):
                mutated = copy.deepcopy(self.inventory)
                mutated["identity_bindings"][entity_type] = [
                    row for row in mutated["identity_bindings"][entity_type] if row["entity_id"] != entity_id
                ]
                issues = validate_public_graph(tuples, self.vocabularies, mutated)
                self.assertTrue(any(f"missing {entity_type} identity bindings" in issue or f"{entity_type} identity bindings do not equal generated entities" in issue for issue in issues), issues)

        missing_slug = copy.deepcopy(self.inventory)
        missing_slug["public_slug_inventory"] = [
            row for row in missing_slug["public_slug_inventory"] if row["entity_id"] != "6529NM-RP-0001"
        ]
        issues = validate_public_graph(tuples, self.vocabularies, missing_slug)
        self.assertTrue(any("governed slug rows do not equal generated slug-bearing entities" in issue for issue in issues), issues)

        drifted_route = copy.deepcopy(self.inventory)
        next(row for row in drifted_route["public_slug_inventory"] if row["entity_id"] == "6529NM-RP-0001")["canonical_route"] = "/museum/network/research/wrong"
        issues = validate_public_graph(tuples, self.vocabularies, drifted_route)
        self.assertTrue(any("public slug inventory mismatch for 6529NM-RP-0001" in issue for issue in issues), issues)

        duplicate_route = copy.deepcopy(self.inventory)
        next(row for row in duplicate_route["public_slug_inventory"] if row["entity_id"] == "6529NM-RP-0001")["canonical_route"] = "/museum/network/research/access-control-and-exit"
        issues = validate_public_graph(tuples, self.vocabularies, duplicate_route)
        self.assertTrue(any("duplicate governed route" in issue for issue in issues), issues)

    def test_source_reordering_preserves_governed_entity_relation_media_and_observation_ids(self) -> None:
        baseline_entities = self.entities()
        baseline_entity_identity = {
            entity_id: (payload["entity_type"], payload["preferred_label"], payload["public_slug"], payload["canonical_route"])
            for entity_id, payload in baseline_entities.items()
        }
        baseline_relations = {
            payload["relation_id"]: (payload["relation_type"], payload["source_entity_id"], payload["target_entity_id"])
            for payload in self.relations()
        }
        original_load_json = migration.load_json

        def reordered_load_json(path: Path):
            value = original_load_json(path)
            if path.name == "proposal.json" and "proposed-gifts" in path.as_posix():
                value["objects"] = list(reversed(value["objects"]))
            if path.name == "selected-works.json":
                value["works"] = list(reversed(value["works"]))
            return value

        with patch.object(migration, "load_json", side_effect=reordered_load_json):
            reordered_records = migration.build_records(
                reviewed=True,
                reviewer_id="codex-review:test-independent",
                reviewed_at=TEST_REVIEWED_AT,
                reviewed_commit=TEST_REVIEWED_COMMIT,
                reviewed_manifest_sha256=TEST_REVIEWED_MANIFEST_SHA256,
                reviewed_manifest_keccak=TEST_REVIEWED_MANIFEST_KECCAK,
            )
        reordered_entities = {record["payload"]["entity_id"]: record["payload"] for record in reordered_records.values() if record["payload"].get("record_type") == "PUBLIC_ENTITY"}
        reordered_relations = {record["payload"]["relation_id"]: record["payload"] for record in reordered_records.values() if record["payload"].get("record_type") == PUBLIC_RELATION_TYPE}
        reordered_inventory = copy.deepcopy(self.inventory)
        for rows in reordered_inventory["identity_bindings"].values():
            rows.reverse()
        original_indexes = identity_binding_indexes(self.inventory)
        reordered_indexes = identity_binding_indexes(reordered_inventory)
        for binding_type in migration.IDENTITY_BINDING_TYPES:
            self.assertEqual(reordered_indexes[binding_type], original_indexes[binding_type])
        self.assertEqual({entity_id: (payload["entity_type"], payload["preferred_label"], payload["public_slug"], payload["canonical_route"]) for entity_id, payload in reordered_entities.items()}, baseline_entity_identity)
        self.assertEqual({relation_id: (payload["relation_type"], payload["source_entity_id"], payload["target_entity_id"]) for relation_id, payload in reordered_relations.items()}, baseline_relations)
        baseline_observations = {observation["observation_id"]: work_id for work_id, work in baseline_entities.items() if work["entity_type"] == "WORK" for observation in work["profile"]["lifecycle_observations"]}
        reordered_observations = {observation["observation_id"]: work_id for work_id, work in reordered_entities.items() if work["entity_type"] == "WORK" for observation in work["profile"]["lifecycle_observations"]}
        self.assertEqual(reordered_observations, baseline_observations)
        baseline_media = {entity_id: payload["profile"]["media"]["subject_entity_id"] for entity_id, payload in baseline_entities.items() if payload["entity_type"] == "MEDIA_REFERENCE"}
        reordered_media = {entity_id: payload["profile"]["media"]["subject_entity_id"] for entity_id, payload in reordered_entities.items() if payload["entity_type"] == "MEDIA_REFERENCE"}
        self.assertEqual(reordered_media, baseline_media)

    def test_relation_identity_excludes_mutable_qualifiers(self) -> None:
        relation = next(item for item in self.relations() if item["relation_type"] == "CURATED_ACQUISITION_BRINGS_TOGETHER_WORK")
        key = semantic_relation_key(relation["relation_type"], relation["source_entity_id"], relation["target_entity_id"], relation["qualifier"])
        relation_inventory = load_json(ROOT / "schemas/public-relation-identity-inventory.json")
        indexes = relation_binding_indexes(relation_inventory)
        changed = copy.deepcopy(relation["qualifier"])
        changed["display_order"] = changed.get("display_order", 1) + 100
        self.assertEqual(semantic_relation_key(relation["relation_type"], relation["source_entity_id"], relation["target_entity_id"], changed), key)
        self.assertEqual(indexes[key], relation["relation_id"])

    def test_acquisition_programs_are_pathways_not_collection_membership(self) -> None:
        entities = self.entities()
        relations = self.relations()
        programs = {entity_id for entity_id, payload in entities.items() if payload["entity_type"] == "ACQUISITION_PROGRAM"}
        collection_relations = [relation for relation in relations if relation["relation_type"] == "COLLECTION_CONTAINS_WORK"]
        self.assertTrue(all(relation["source_entity_id"] not in programs and relation["target_entity_id"] not in programs for relation in collection_relations))
        self.assertTrue(all(entities[relation["target_entity_id"]]["entity_type"] == "WORK" for relation in collection_relations))
        self.assertTrue(all(entities[relation["target_entity_id"]]["profile"]["collection_membership"]["status"] == "permanent_collection" for relation in collection_relations))
        self.assertTrue(all(entities[relation["source_entity_id"]]["entity_type"] == "ACQUISITION_PROGRAM" for relation in relations if relation["relation_type"] == "PROGRAM_SELECTS_WORK"))

    def test_winner_observation_and_append_only_lifecycle_are_exact(self) -> None:
        entities = self.entities()
        ca = entities["6529NM-CA-2026-003"]["profile"]
        self.assertEqual(ca["lifecycle"]["status"], "accessioned_into_permanent_collection")
        self.assertEqual([item["source_status"] for item in ca["lifecycle_observations"]], ["PARTICIPATORY", "WINNER", "accessioned"])
        self.assertEqual(ca["lifecycle_observations"][1]["observed_at"], WINNER_AT)
        self.assertIn(WINNER_OBSERVATION_ID, ca["lifecycle_observations"][1]["source_record_ids"])
        self.assertIn(migration.WINNER_SOURCE_URL, json.dumps(ca["lifecycle_observations"][1]))
        self.assertEqual(ca["collection_effect"], "permanent_collection")
        for index in range(24, 29):
            profile = entities[f"6529NM-W-{index:04d}"]["profile"]
            self.assertEqual(profile["work_lifecycle_status"], "accessioned")
            self.assertEqual(profile["current_museum_relation"]["relation_status"], "permanent_collection")
            self.assertEqual(profile["collection_membership"]["status"], "permanent_collection")
            self.assertEqual([item["source_status"] for item in profile["lifecycle_observations"]], ["PARTICIPATORY", "WINNER", "accessioned"])
            self.assertIn(WINNER_OBSERVATION_ID, profile["lifecycle_observations"][1]["source_record_ids"])
        observation = next(payload for payload in self.payloads() if payload.get("record_type") == "WAVE_STATUS_OBSERVATION")
        self.assertEqual(observation["observation_id"], WINNER_OBSERVATION_ID)
        self.assertEqual(observation["serial_no"], 1276093)
        self.assertEqual(observation["rating"], 121603214)
        self.assertEqual(observation["realtime_rating"], 121603214)
        self.assertEqual(observation["rater_count"], 29)
        self.assertTrue(observation["signed"])
        self.assertEqual(observation["drop_type"], "WINNER")
        self.assertEqual(observation["prior_observation"]["source_status"], "PARTICIPATORY")
        self.assertIsNone(observation["prior_observation"]["source_record_path"])
        self.assertEqual(observation["prior_observation"]["source_repository_visibility"], "complete_manifest_only")

        missing_acquisition_binding = copy.deepcopy(entities["6529NM-CA-2026-003"])
        missing_acquisition_binding["profile"]["lifecycle_observations"][1]["source_record_ids"].remove(WINNER_OBSERVATION_ID)
        missing_acquisition_binding["references"].remove(WINNER_OBSERVATION_ID)
        self.assertTrue(
            any(
                "requires a governed WINNER observation record ID" in issue
                for issue in validate_public_payload(missing_acquisition_binding, self.vocabularies, self.inventory)
            )
        )

        missing_work_binding = copy.deepcopy(entities["6529NM-W-0024"])
        missing_work_binding["profile"]["lifecycle_observations"][1]["source_record_ids"].remove(WINNER_OBSERVATION_ID)
        self.assertTrue(
            any(
                "requires a governed WINNER observation record ID" in issue
                for issue in validate_public_payload(missing_work_binding, self.vocabularies, self.inventory)
            )
        )

        unresolved_binding = copy.deepcopy(self.records)
        acquisition = next(
            record["payload"]
            for record in unresolved_binding.values()
            if record["payload"].get("entity_id") == "6529NM-CA-2026-003"
        )
        acquisition["profile"]["lifecycle_observations"][1]["source_record_ids"][-1] = (
            "6529NM-WAVE-OBS-2026-08-08-999"
        )
        self.assertTrue(
            any(
                "must resolve to a governed WINNER observation record" in issue
                for issue in self.graph_issues(unresolved_binding)
            )
        )

    def test_program_selection_survives_later_work_state_and_mint_is_independent(self) -> None:
        records = copy.deepcopy(self.records)
        work = next(record["payload"] for record in records.values() if record["payload"].get("entity_id") == "6529NM-W-0008")
        work["profile"]["mint_fact"]["status"] = "verified"
        self.assertEqual(self.graph_issues(records), [])
        work["profile"]["work_lifecycle_status"] = "acquisition_complete"
        self.assertEqual(self.graph_issues(records), [])
        selection = next(relation for relation in self.relations() if relation["relation_type"] == "PROGRAM_SELECTS_WORK" and relation["target_entity_id"] == "6529NM-W-0008")
        self.assertEqual(selection["qualifier"]["selection_status"], "selected_unminted")

    def test_adversarial_profile_route_membership_and_media_fail_closed(self) -> None:
        entities = self.entities()
        work = copy.deepcopy(entities["6529NM-W-0001"])
        work["profile"]["profile_type"] = "ARTIST"
        self.assertTrue(validate_public_payload(work, self.vocabularies, self.inventory))
        institution = copy.deepcopy(entities["6529NM-I-0001"])
        institution["canonical_route"] = "/museum/network/not-the-singleton"
        self.assertTrue(validate_public_payload(institution, self.vocabularies, self.inventory))
        acquisition = copy.deepcopy(entities["6529NM-CA-2026-003"])
        acquisition["profile"]["acquisition_method"] = "proposal"
        self.assertTrue(self.schema_issues(acquisition, "https://6529networkmuseum.org/schemas/public-entity-v1.json"))
        review_membership = copy.deepcopy(entities["6529NM-W-0008"])
        review_membership["profile"]["collection_membership"]["status"] = "accession_review_in_progress"
        self.assertTrue(self.schema_issues(review_membership, "https://6529networkmuseum.org/schemas/public-entity-v1.json"))
        no_accession = copy.deepcopy(entities["6529NM-W-0008"])
        no_accession["profile"]["collection_membership"] = {"status": "permanent_collection", "collection_entity_id": "6529NM-C-0001", "accession_entity_ids": [], "source_record_ids": ["6529NM-CA-2026-002"], "evidence_refs": [{"label": "test", "uri": "https://example.org/test", "observed_at": "2026-08-08T00:00:00Z", "evidence_class": "C"}]}
        self.assertTrue(self.schema_issues(no_accession, "https://6529networkmuseum.org/schemas/public-entity-v1.json"))
        relational = copy.deepcopy(entities["6529NM-AGT-0001"])
        relational["public_slug"] = "casey"
        relational["canonical_route"] = "/museum/network/agents/casey"
        self.assertTrue(validate_public_payload(relational, self.vocabularies, self.inventory))
        signed = copy.deepcopy(next(value for value in entities.values() if value["entity_id"] == "6529NM-MED-0041")["profile"]["media"])
        signed["allowed_ui_affordances"].append("download")
        self.assertTrue(validate_public_media(signed, "test.signed"))
        signed = copy.deepcopy(next(value for value in entities.values() if value["entity_id"] == "6529NM-MED-0041")["profile"]["media"])
        signed["source_locator"]["uri"] = "https://example.org/not-the-signed-wave-part.jpg"
        self.assertTrue(any("preserve its exact Wave-upload locator" in issue for issue in validate_public_media(signed, "test.signed-source")))
        signed["publication_context_entity_ids"] = []
        self.assertTrue(validate_public_media(signed, "test.historical-context"))
        child = copy.deepcopy(entities["6529NM-MED-0043"]["profile"]["media"])
        child["accessibility_text"] = "Named child identified as Alex."
        self.assertTrue(validate_public_media(child, "test.child"))
        child = copy.deepcopy(entities["6529NM-MED-0043"]["profile"]["media"])
        child["accessibility_text"] = "A child standing before a wall."
        self.assertTrue(validate_public_media(child, "test.child-age-classification"))
        child = copy.deepcopy(entities["6529NM-MED-0043"]["profile"]["media"])
        child["identity_inference_prohibition"] = None
        self.assertTrue(validate_public_media(child, "test.child-structural-prohibition"))
        child["identity_inference_prohibition"] = {"status": "permitted", "scope": "subject_identity", "reason": "bad"}
        self.assertTrue(validate_public_media(child, "test.child-structural-status"))
        cover = copy.deepcopy(entities["6529NM-MED-0004"]["profile"]["media"])
        cover["derived_from_media_entity_id"] = "6529NM-MED-0041"
        self.assertTrue(validate_public_media(cover, "test.cover-boundary"))
        cover = copy.deepcopy(entities["6529NM-MED-0004"]["profile"]["media"])
        cover["rights"]["evidence_refs"][0]["uri"] = "https://github.com/6529-Collections/6529networkmuseum/blob/main/records/entities/6529NM-CA-2026-003.json"
        self.assertTrue(validate_public_media(cover, "test.cover-self-rights-evidence"))

    def test_evidence_paths_and_graph_routes_fail_closed(self) -> None:
        records = copy.deepcopy(self.records)
        first = next(iter(records.values()))
        first["payload"]["evidence_refs"][0]["uri"] = "https://github.com/6529-Collections/6529networkmuseum/blob/main/does/not/exist.json"
        with self.assertRaises(ValueError):
            verify_evidence_paths(records)
        bad_route = copy.deepcopy(self.records)
        for record in bad_route.values():
            payload = record["payload"]
            if payload.get("entity_id") == "6529NM-W-0001":
                payload["canonical_route"] = "/museum/network/works/6529NM-AP-01-OUT-001"
                break
        self.assertTrue(self.graph_issues(bad_route))

    def test_keys_and_gates_publications_use_authorized_display_title(self) -> None:
        visitor_paths = (
            "docs/programs/keys-and-gates.md",
            "records/programs/6529NM-AP-01/public/README.md",
            "records/programs/6529NM-AP-01/public/curated-acquisition.md",
            "records/programs/6529NM-AP-01/public/curatorial-essay.md",
            "records/programs/6529NM-AP-01/public/sources-and-bibliography.md",
            "records/programs/6529NM-AP-01/public/artists/hugofaz.md",
            "records/programs/6529NM-AP-01/public/works/managed-freedom.md",
            "records/programs/6529NM-AP-01/public/works/no-access.md",
            "records/programs/6529NM-AP-01/public/works/the-artist-in-teh-open-sea.md",
        )
        for relative_path in visitor_paths:
            text = (ROOT / relative_path).read_text(encoding="utf-8")
            self.assertNotIn("teh Open Sea", text, relative_path)

        archival_outcome = load_json(
            ROOT / "records/programs/6529NM-AP-01/outcomes/OUT-002.json"
        )
        self.assertEqual(archival_outcome["title"], "the Artist in teh Open Sea")
        amendment = (
            ROOT
            / "records/programs/6529NM-AP-01/public/title-display-amendment-2026-08-18.md"
        ).read_text(encoding="utf-8")
        self.assertIn("the Artist in teh Open Sea", amendment)


if __name__ == "__main__":
    unittest.main()
