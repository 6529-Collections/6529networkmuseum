import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class VeraMolnarAccessionTest(unittest.TestCase):
    def load(self, rel):
        return json.loads((ROOT / rel).read_text(encoding="utf-8"))

    def test_exact_accession_and_finalized_custody(self):
        obj = self.load("records/accessions/6529NM.2026.003/objects/6529NM.2026.003.01.json")["payload"]
        self.assertEqual(obj["accession_lot_id"], "6529NM.2026.003")
        self.assertEqual(obj["object_id"], "6529NM.2026.003.01")
        self.assertEqual(obj["chain_identity"]["caip19"], "eip155:1/erc721:0xe034bb2b1b9471e11cf1a0a9199a156fb227aa5d/210")
        self.assertEqual(obj["chain_identity"]["token_hash"], "0xd0a3be9aa1a3e101a12ec038ceb71a18846dbc62eac3e91fb425232e7820a318")
        self.assertEqual(obj["chain_identity"]["custody_block"], 25816984)
        self.assertEqual(obj["chain_identity"]["custody_status"], "verified")

    def test_authority_and_media_ids(self):
        gaa = self.load("records/accessions/6529NM.2026.003/gift-acceptance-authorization.json")["payload"]
        self.assertEqual(gaa["authorization_id"], "6529NM.2026.003.GAA-01")
        self.assertEqual(gaa["authorization_status"], "formally_accepted")
        self.assertEqual(gaa["governing_basis"][0]["observed_wave_status"], "WINNER")
        work = self.load("records/entities/6529NM-W-0029.json")["payload"]
        self.assertEqual(work["media_entity_ids"], ["6529NM-MED-0052", "6529NM-MED-0053"])
        self.assertEqual(work["profile"]["creator_entity_ids"], ["6529NM-ART-0022", "6529NM-ART-0023"])

    def test_editorial_boundaries(self):
        text = (ROOT / "records/accessions/6529NM.2026.003/public/6529NM.2026.003.01.md").read_text(encoding="utf-8")
        self.assertIn("one unique output in a fixed edition of 500", text)
        self.assertIn("500 unique outputs; token 210", text)
        self.assertIn("6529NM.2026.003.GAA-01", text)
        self.assertIn("6529NM-ACC-2026-003", text)
        self.assertNotIn("1/1 of 500", text)

    def test_wave_api_status_does_not_claim_signature_verification(self):
        observation = self.load(
            "records/proposed-gifts/6529NM-PG-2026-002/wave-status-observation.json"
        )["payload"]
        self.assertTrue(observation["api_reported_is_signed"])
        self.assertNotIn("signed", observation)
        self.assertEqual(observation["observation_method"], "wave_api_status_readback")
        public_paths = [
            "records/accessions/6529NM.2026.003/public/source-and-chronology.md",
            "records/proposed-gifts/6529NM-PG-2026-002/public/status-amendments/2026-08-23-winner-and-accession.md",
            "records/proposed-gifts/6529NM-PG-2026-002/public/voter-dossier.md",
            "records/proposed-gifts/6529NM-PG-2026-002/public/wave-storm/01-resolution.md",
            "records/proposed-gifts/6529NM-PG-2026-002/public/wave-storm/03-case-and-decision.md",
        ]
        for path in public_paths:
            text = (ROOT / path).read_text(encoding="utf-8")
            self.assertNotIn("signed WINNER", text)
            self.assertNotIn("signed Wave", text)


if __name__ == "__main__":
    unittest.main()
