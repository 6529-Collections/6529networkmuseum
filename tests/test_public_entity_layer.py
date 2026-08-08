"""Executable contract tests for the WP-1 public entity/relation projection."""

from __future__ import annotations

import copy
import json
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
    build_records,
    evidence,
    generated_directory_issues,
    identity_binding_indexes,
    load_json,
    relation_binding_indexes,
    resolve_identity_ids,
    semantic_relation_key,
    source_evidence,
    source_record_evidence_class,
    verify_evidence_paths,
)

TEST_REVIEWED_AT = "2026-08-08T16:00:00Z"
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

    def test_exact_projection_counts_and_profile_counts(self) -> None:
        counts = Counter(payload["record_type"] for payload in self.payloads())
        self.assertEqual(counts, Counter({"PUBLIC_ENTITY": 118, "PUBLIC_RELATION": 164, "WAVE_STATUS_OBSERVATION": 1}))
        entities = self.entities()
        self.assertEqual(sum(payload["entity_type"] == "ARTIST" for payload in entities.values()), 21)
        self.assertEqual(sum(payload["entity_type"] == "ORGANIZATION" for payload in entities.values()), 2)
        self.assertEqual(sum(payload["entity_type"] == "PROJECT_OR_SERIES" for payload in entities.values()), 6)
        self.assertEqual(sum(payload["entity_type"] == "WORK" for payload in entities.values()), 28)
        self.assertEqual(sum(payload["entity_type"] == "AGENT" for payload in entities.values()), 21)
        self.assertEqual(sum(payload["entity_type"] == "MEDIA_REFERENCE" for payload in entities.values()), 31)
        self.assertEqual(sum(payload["entity_type"] == "ACQUISITION_PROGRAM" for payload in entities.values()), 2)
        self.assertEqual(len(self.relations()), 164)
        sample = next(iter(entities.values()))
        self.assertEqual(sample["reviewer"]["reviewed_at"], TEST_REVIEWED_AT)
        self.assertEqual(sample["reviewer"]["reviewed_commit"], TEST_REVIEWED_COMMIT)
        self.assertEqual(sample["reviewer"]["reviewed_manifest_sha256"], TEST_REVIEWED_MANIFEST_SHA256)
        self.assertEqual(sample["reviewer"]["reviewed_manifest_keccak"], TEST_REVIEWED_MANIFEST_KECCAK)
        self.assertEqual(sample["constructor"]["observed_at"], GENERATED_AT)
        self.assertNotEqual(sample["reviewer"]["reviewed_at"], sample["constructor"]["observed_at"])

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
        self.assertEqual(set(works), {f"6529NM-W-{index:04d}" for index in range(1, 29)})
        for work_id, work in works.items():
            self.assertEqual(work["public_slug"], work_id)
            self.assertEqual(work["canonical_route"], f"/museum/network/works/{work_id}")
        artists = {payload["entity_id"]: payload for payload in entities.values() if payload["entity_type"] == "ARTIST"}
        self.assertEqual(len(artists), 21)
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
        self.assertIn("public/wave-storm/01-resolution.md", json.dumps(magnum_project))
        creator_relations = [relation for relation in self.relations() if relation["relation_type"] == "ARTIST_CREATES_WORK"]
        self.assertEqual(len(creator_relations), 28)
        self.assertTrue(all(entities[relation["source_entity_id"]]["entity_type"] == "ARTIST" for relation in creator_relations))
        hugo = next(payload for payload in artists.values() if payload["preferred_label"] == "HugoFaz")
        self.assertEqual({relation["target_entity_id"] for relation in creator_relations if relation["source_entity_id"] == hugo["entity_id"]}, {"6529NM-W-0009", "6529NM-W-0018"})
        moises = artists["6529NM-ART-0020"]
        self.assertEqual(moises["preferred_label"], "Moisés Saman")
        self.assertTrue(any(variant["variant_role"] == "source_label" and variant["value"] == "Moisés Saman" for variant in moises["profile"]["name_variants"]))
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
        self.assertTrue(all("records/proposed-gifts/6529NM-PG-2026-001/public/wave-storm/" in json.dumps(relation["evidence_refs"]) for relation in project_relations))
        origin_relation = next(relation for relation in relations if relation["relation_type"] == "ORGANIZATION_ORIGINATES_PROJECT" and relation["target_entity_id"] == "6529NM-PRJ-0006")
        self.assertEqual(origin_relation["source_entity_id"], "6529NM-ORG-0002")
        self.assertEqual(origin_relation["qualifier"]["role"], "originator")
        self.assertNotEqual(entities["6529NM-PRJ-0006"]["entity_id"], "6529NM-CA-2026-003")
        self.assertTrue(all(work["profile"]["project_or_series_entity_ids"] == ["6529NM-PRJ-0006"] for work in (entities[f"6529NM-W-{index:04d}"] for index in range(24, 29))))
        self.assertTrue(all(entities[relation["target_entity_id"]]["profile"]["collection_membership"]["status"] == "not_in_collection" for relation in project_relations))

    def test_every_work_has_typed_media_and_no_media_reuse(self) -> None:
        entities = self.entities()
        media = {key: value for key, value in entities.items() if value["entity_type"] == "MEDIA_REFERENCE"}
        media_relations = [relation for relation in self.relations() if relation["relation_type"] == "ENTITY_HAS_MEDIA" and entities[relation["source_entity_id"]]["entity_type"] == "WORK"]
        self.assertEqual({relation["source_entity_id"] for relation in media_relations}, {f"6529NM-W-{index:04d}" for index in range(1, 29)})
        target_counts = Counter(relation["target_entity_id"] for relation in media_relations)
        self.assertTrue(all(count == 1 for count in target_counts.values()))
        for relation in media_relations:
            target = media[relation["target_entity_id"]]
            self.assertEqual(target["profile"]["media"]["subject_entity_id"], relation["source_entity_id"])
            self.assertIn(relation["target_entity_id"], entities[relation["source_entity_id"]]["media_entity_ids"])
        keys_media = [value for key, value in media.items() if 20 <= int(key.rsplit("-", 1)[1]) <= 35]
        self.assertEqual(len(keys_media), 16)
        self.assertEqual(len([relation for relation in media_relations if relation["target_entity_id"] in {value["entity_id"] for value in keys_media}]), 16)
        magnum_media = [value for value in media.values() if value["profile"]["media"].get("media_role") == "historical_wave_proposal_presentation"]
        self.assertEqual(len(magnum_media), 5)
        for value in magnum_media:
            media_profile = value["profile"]["media"]
            self.assertIsNone(media_profile["source_locator"]["uri"])
            self.assertIsNone(media_profile["source_locator"]["repository_path"])
            self.assertIsNone(media_profile["token_source_locator"])
            self.assertIsNone(media_profile["token_source_fixity"])
            self.assertFalse(media_profile["visual"])
            self.assertEqual(media_profile["publication_boundary"], "historical_wave_proposal_context")
            self.assertEqual(media_profile["publication_context_entity_ids"], ["6529NM-CA-2026-003"])
            self.assertEqual(media_profile["wave_proposal_context"]["publication_status"], "historical_public_proposal_context")
            self.assertIn("open_wave_proposal_context", media_profile["allowed_ui_affordances"])
            self.assertNotIn("download", media_profile["allowed_ui_affordances"])
            self.assertNotIn("zoom", media_profile["allowed_ui_affordances"])
            self.assertNotIn("fullscreen", media_profile["allowed_ui_affordances"])
            self.assertNotIn("open_repository_path", media_profile["allowed_ui_affordances"])
            self.assertNotIn("view", media_profile["allowed_ui_affordances"])
            self.assertNotIn("thumbnail", media_profile["allowed_ui_affordances"])
            self.assertNotIn("hero", media_profile["allowed_ui_affordances"])
        child_media = next(value for value in magnum_media if value["entity_id"] == "6529NM-MED-0043")["profile"]["media"]
        self.assertEqual(child_media["accessibility_subject_policy"], "non_identifying_child_subject")
        self.assertNotRegex(child_media["accessibility_text"].lower(), r"\b(named|identified|known as)\b")
        self.assertEqual(child_media["identity_inference_prohibition"]["status"], "prohibited")
        self.assertEqual(child_media["identity_inference_prohibition"]["scope"], "subject_identity")
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
        self.assertTrue(all(value["profile"]["media"]["width"] == 640 for value in keys_media))
        for value in keys_media:
            media_profile = value["profile"]["media"]
            self.assertEqual(media_profile["rights"]["status"], "unknown")
            self.assertEqual(media_profile["accessibility_status"], "pending_review")
            self.assertFalse(media_profile["visual"])
            self.assertEqual(media_profile["source_locator"], {"uri": None, "repository_path": None})
            self.assertEqual(media_profile["allowed_ui_affordances"], ["alt_text", "copy_citation"])
        generated_json = json.dumps(self.records, ensure_ascii=False)
        self.assertNotIn("OUT-004/1280.webp", generated_json)
        self.assertNotIn("OUT-004/2400.webp", generated_json)
        self.assertNotIn("OUT-011/1280.webp", generated_json)
        self.assertNotIn("OUT-011/2400.webp", generated_json)

    def test_collection_membership_remains_exactly_casey_seven(self) -> None:
        entities = self.entities()
        relations = self.relations()
        collection_relations = [relation for relation in relations if relation["relation_type"] == "COLLECTION_CONTAINS_WORK"]
        accession_relations = [relation for relation in relations if relation["relation_type"] == "ACCESSION_ADMITS_WORK"]
        self.assertEqual(len(collection_relations), 7)
        self.assertEqual(len(accession_relations), 7)
        self.assertEqual({relation["target_entity_id"] for relation in collection_relations}, {f"6529NM-W-{index:04d}" for index in range(1, 8)})
        self.assertTrue(all(entities[relation["target_entity_id"]]["profile"]["collection_membership"]["status"] == "permanent_collection" for relation in collection_relations))
        permanent_work_ids = {entity_id for entity_id, payload in entities.items() if payload["entity_type"] == "WORK" and payload["profile"]["collection_membership"]["status"] == "permanent_collection"}
        self.assertEqual(permanent_work_ids, {relation["target_entity_id"] for relation in accession_relations})
        self.assertTrue(all(entities[f"6529NM-W-{index:04d}"]["profile"]["collection_membership"]["status"] == "not_in_collection" for index in range(24, 29)))

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

    def test_magnum_mint_and_acquisition_mint_are_chain_verified_but_not_museum_acquisition(self) -> None:
        entities = self.entities()
        for index in range(24, 29):
            work = entities[f"6529NM-W-{index:04d}"]["profile"]
            self.assertEqual(work["mint_fact"]["status"], "verified")
            self.assertEqual(work["mint_fact"]["evidence_refs"][0]["evidence_class"], "A")
            self.assertIn("proposal.json", work["mint_fact"]["evidence_refs"][0]["uri"])
            self.assertEqual(work["collection_membership"]["status"], "not_in_collection")
            self.assertEqual(work["accession_entity_ids"], [])
        ca3 = entities["6529NM-CA-2026-003"]["profile"]
        self.assertEqual(ca3["independent_acquisition_facts"]["mint"]["status"], "verified")
        self.assertEqual(ca3["independent_acquisition_facts"]["mint"]["evidence_refs"][0]["evidence_class"], "A")
        self.assertIn("existing external ERC-721 token manifestation only", ca3["independent_acquisition_facts"]["mint"]["notes"])
        self.assertIn("does not establish Museum acquisition", ca3["independent_acquisition_facts"]["mint"]["notes"])

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
        self.assertEqual(produced["6529NM-AP-ENT-0001"], {"6529NM-CA-2026-001", "6529NM-CA-2026-003"})
        self.assertEqual(programs["6529NM-AP-ENT-0001"]["profile"]["produced_acquisition_entity_ids"], sorted(produced["6529NM-AP-ENT-0001"]))
        self.assertEqual(produced["6529NM-AP-ENT-0002"], {"6529NM-CA-2026-002"})
        self.assertEqual(entities["6529NM-CA-2026-001"]["profile"]["program_or_pathway"]["entity_ids"], ["6529NM-AP-ENT-0001"])
        self.assertEqual(entities["6529NM-CA-2026-003"]["profile"]["program_or_pathway"]["entity_ids"], ["6529NM-AP-ENT-0001"])
        self.assertEqual(entities["6529NM-CA-2026-002"]["profile"]["program_or_pathway"]["entity_ids"], ["6529NM-AP-ENT-0002"])
        self.assertTrue(all(entities[f"6529NM-W-{index:04d}"]["profile"]["program_entity_ids"] == ["6529NM-AP-ENT-0001"] for index in [*range(1, 8), *range(24, 29)]))
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
        relations = [relation for relation in self.relations() if relation["relation_type"] == "AGENT_PLAYS_ROLE"]
        self.assertEqual(len(relations), 11)
        for project_id, project in entities.items():
            if project["entity_type"] != "PROJECT_OR_SERIES":
                continue
            project_relations = [relation for relation in relations if relation["target_entity_id"] == project_id]
            self.assertEqual({relation["source_entity_id"] for relation in project_relations}, set(project["profile"]["agent_entity_ids"]))
            for relation in project_relations:
                self.assertIsInstance(relation["qualifier"].get("role"), str)
                self.assertTrue(relation["qualifier"]["role"])
                self.assertTrue(set(relation["source_record_ids"]).intersection(project["profile"]["source_record_ids"]))

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
                        self.assertEqual(target["authoritative_record_type"], "PROPOSED_GIFT")
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

    def test_restricted_and_unknown_media_are_structurally_metadata_only(self) -> None:
        for entity_id in ("6529NM-MED-0020", "6529NM-MED-0041"):
            with self.subTest(entity_id=entity_id):
                baseline = copy.deepcopy(self.entities()[entity_id])
                self.assertEqual(validate_public_media(baseline["profile"]["media"], entity_id), [])
                self.assertEqual(self.schema_issues(baseline, "https://6529networkmuseum.org/schemas/public-entity-v1.json"), [])
                for name, mutate in (
                    ("source locator", lambda media: media["source_locator"].update({"uri": "https://example.org/media", "repository_path": None})),
                    ("visual", lambda media: media.update({"visual": True})),
                    ("token source locator", lambda media: media.update({"token_source_locator": {"uri": "https://example.org/token", "repository_path": None}})),
                    ("view affordance", lambda media: media["allowed_ui_affordances"].append("view")),
                ):
                    with self.subTest(name=name):
                        mutated = copy.deepcopy(baseline)
                        mutate(mutated["profile"]["media"])
                        self.assertTrue(validate_public_media(mutated["profile"]["media"], f"{entity_id}.{name}"))
                        self.assertTrue(self.schema_issues(mutated, "https://6529networkmuseum.org/schemas/public-entity-v1.json"))

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
        self.assertEqual(len(candidate_entities), 118)
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
        self.assertEqual(len(observations), 33)
        self.assertEqual(set(observations), expected)
        self.assertEqual(len(set(observations)), 33)
        for observation_id, work_id in observations.items():
            self.assertIn(work_id, self.entities())

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
        for binding_type in ("AGENT", "ARTIST", "WORK", "PROJECT_OR_SERIES", "MEDIA_REFERENCE", "WORK_LIFECYCLE_OBSERVATION"):
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
        self.assertEqual(ca["lifecycle"]["status"], "selected_by_museum_wave_acquisition_review_in_progress")
        self.assertEqual([item["source_status"] for item in ca["lifecycle_observations"]], ["PARTICIPATORY", "WINNER"])
        self.assertEqual(ca["lifecycle_observations"][-1]["observed_at"], WINNER_AT)
        self.assertIn(WINNER_SOURCE_PATH, json.dumps(ca["lifecycle_observations"][-1]))
        self.assertEqual(ca["collection_effect"], "none")
        for index in range(24, 29):
            profile = entities[f"6529NM-W-{index:04d}"]["profile"]
            self.assertEqual(profile["work_lifecycle_status"], "selected_by_museum_wave_acquisition_review_in_progress")
            self.assertEqual(profile["current_museum_relation"]["relation_status"], "selected_by_museum_wave")
            self.assertEqual(profile["collection_membership"]["status"], "not_in_collection")
            self.assertEqual([item["source_status"] for item in profile["lifecycle_observations"]], ["PARTICIPATORY", "WINNER"])
        observation = next(payload for payload in self.payloads() if payload.get("record_type") == "WAVE_STATUS_OBSERVATION")
        self.assertEqual(observation["observation_id"], WINNER_OBSERVATION_ID)
        self.assertEqual(observation["serial_no"], 1276093)
        self.assertEqual(observation["rating"], 121603214)
        self.assertEqual(observation["realtime_rating"], 121603214)
        self.assertEqual(observation["rater_count"], 29)
        self.assertTrue(observation["signed"])
        self.assertEqual(observation["drop_type"], "WINNER")
        self.assertEqual(observation["prior_observation"]["source_status"], "PARTICIPATORY")

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
        signed["allowed_ui_affordances"].append("view")
        self.assertTrue(any("cannot expose visual delivery" in issue for issue in validate_public_media(signed, "test.signed-view")))
        signed["publication_context_entity_ids"] = []
        self.assertTrue(validate_public_media(signed, "test.historical-context"))
        child = copy.deepcopy(entities["6529NM-MED-0043"]["profile"]["media"])
        child["accessibility_text"] = "Named child identified as Alex."
        self.assertTrue(validate_public_media(child, "test.child"))
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


if __name__ == "__main__":
    unittest.main()
