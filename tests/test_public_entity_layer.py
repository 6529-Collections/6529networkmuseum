"""Executable contract tests for the WP-1 public entity/relation projection."""

from __future__ import annotations

import copy
import json
import sys
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from migrate_public_entities import (  # noqa: E402
    WINNER_AT,
    WINNER_OBSERVATION_ID,
    WINNER_SOURCE_PATH,
    build_records,
    load_json,
    verify_evidence_paths,
)
from validate import (  # noqa: E402
    PUBLIC_RELATION_TYPE,
    load_schemas,
    validate_public_graph,
    validate_public_media,
    validate_public_payload,
    validator_for,
)


class PublicEntityLayerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.records = build_records(reviewed=True, reviewer_id="codex-review:test-independent")
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
        self.assertEqual(counts, Counter({"PUBLIC_ENTITY": 119, "PUBLIC_RELATION": 152, "WAVE_STATUS_OBSERVATION": 1}))
        entities = self.entities()
        self.assertEqual(sum(payload["entity_type"] == "ARTIST" for payload in entities.values()), 21)
        self.assertEqual(sum(payload["entity_type"] == "ORGANIZATION" for payload in entities.values()), 2)
        self.assertEqual(sum(payload["entity_type"] == "PROJECT_OR_SERIES" for payload in entities.values()), 6)
        self.assertEqual(sum(payload["entity_type"] == "WORK" for payload in entities.values()), 28)
        self.assertEqual(sum(payload["entity_type"] == "ACQUISITION_PROGRAM" for payload in entities.values()), 2)
        self.assertEqual(len(self.relations()), 152)

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
        self.assertEqual(origin_relation["qualifier"]["role"], "publisher")
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
        proposal = load_json(ROOT / "records/proposed-gifts/6529NM-PG-2026-001/proposal.json")
        magnum_urls = {item["image"]["uri"] for item in proposal["objects"]}
        magnum_media = [value for value in media.values() if value["profile"]["media"].get("signed_wave")]
        self.assertEqual({value["profile"]["media"]["source_locator"]["uri"] for value in magnum_media}, magnum_urls)
        self.assertEqual(len(magnum_media), 5)
        for value in magnum_media:
            media_profile = value["profile"]["media"]
            self.assertEqual(media_profile["publication_boundary"], "signed_wave_proposal_only")
            self.assertNotIn("download", media_profile["allowed_ui_affordances"])
            self.assertNotIn("zoom", media_profile["allowed_ui_affordances"])
            self.assertNotIn("fullscreen", media_profile["allowed_ui_affordances"])
        child_media = next(value for value in magnum_media if value["entity_id"] == "6529NM-MED-0043")["profile"]["media"]
        self.assertEqual(child_media["accessibility_subject_policy"], "non_identifying_child_subject")
        self.assertNotRegex(child_media["accessibility_text"].lower(), r"\b(named|identified|known as)\b")

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
        self.assertEqual({observation[key] for key in ("serial_no", "rating", "realtime_rating", "rater_count")}, {1276093, 121603214, 29})
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
        child = copy.deepcopy(entities["6529NM-MED-0043"]["profile"]["media"])
        child["accessibility_text"] = "Named child identified as Alex."
        self.assertTrue(validate_public_media(child, "test.child"))

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
