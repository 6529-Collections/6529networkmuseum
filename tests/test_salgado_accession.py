"""Independent evidence joins for the Salgado accession construction package."""
import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
LOT = "6529NM.2026.004"


def load(path):
    return json.loads((ROOT / path).read_bytes())


class SalgadoEvidenceJoinTests(unittest.TestCase):
    def test_exact_six_tokens_join_metadata_and_finalized_custody(self):
        custody = load("evidence/salgado-amazonia-custody/summary.json")
        sources = load("evidence/salgado-amazonia-sources/manifest.json")
        self.assertEqual([x["token_id"] for x in custody["objects"]],
                         [226, 1117, 2059, 2216, 2768, 4697])
        self.assertEqual(custody["state_selector"]["blockHash"], custody["finalized_block"]["hash"])
        for co, source in zip(custody["objects"], sources["objects"]):
            obj = load(f"records/accessions/{LOT}/objects/{co['object_id']}.json")["payload"]
            self.assertEqual(co["object_id"], source["object_id"])
            self.assertEqual(co["caip19"], obj["chain_identity"]["caip19"])
            self.assertEqual(co["owner"], custody["museum_address"])
            self.assertEqual(co["token_level_approved_operator"], "0x" + "0" * 40)
            raw = (ROOT / source["metadata"]["path"]).read_bytes()
            self.assertEqual("sha256:" + hashlib.sha256(raw).hexdigest(), source["metadata"]["sha256"])
            self.assertEqual(json.loads(raw)["image"], source["image"]["uri"])

    def test_provenance_is_continuous_and_receipts_are_retained(self):
        root = ROOT / "evidence/salgado-amazonia-provenance"
        summary = load("evidence/salgado-amazonia-provenance/summary.json")
        for ref in summary["raw_evidence"]:
            raw = (root / ref["path"]).read_bytes()
            self.assertEqual("sha256:" + hashlib.sha256(raw).hexdigest(), ref["sha256"])
        for obj in summary["objects"]:
            chain = obj["transfers"]
            self.assertEqual(chain[0]["from"], "0x" + "0" * 40)
            for before, after in zip(chain, chain[1:]):
                self.assertEqual(before["to"], after["from"])
            self.assertEqual(chain[-1]["tx_hash"],
                             "0xd1c9986c1e885a5c29b03eb15ef5194ae890678ebf6d0ab84d607af8affc3808")

    def test_governance_preserves_api_status_and_earlier_offer(self):
        source = load("evidence/salgado-amazonia-wave/response.json")
        record = load("records/proposed-gifts/6529NM-PG-2026-003/wave-status-observation.json")["payload"]
        old = load("evidence/salgado-amazonia-wave/original-publication.json")["drop"]
        self.assertEqual(record["drop_type"], source["drop_type"])
        self.assertEqual(record["rating"], source["rating"])
        self.assertEqual(record["drop_id"], source["id"])
        self.assertEqual(record["prior_observation"]["observed_at"], old["observed_at"])
        self.assertEqual(record["prior_observation"]["source_status"], old["drop_type"])

    def test_unrestricted_gift_display_is_separate_from_admission(self):
        lot = load(f"records/accessions/{LOT}/accession-statement.json")["payload"]
        self.assertEqual(lot["formal_acceptance_status"], "formally_accepted")
        self.assertEqual(lot["accession_status"], "not_complete")
        self.assertIsNone(lot["reviewer"])
        for oid in lot["object_ids"]:
            obj = load(f"records/accessions/{LOT}/objects/{oid}.json")["payload"]
            self.assertEqual(obj["current_state"], "received_onchain")
            self.assertIsNone(obj["reviewer"])
            for use in ["exhibition", "publication", "preservation", "accessibility"]:
                self.assertEqual(obj["rights"][use]["grant_status"], "granted_with_conditions")


if __name__ == "__main__":
    unittest.main()
