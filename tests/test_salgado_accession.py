"""Independent evidence joins for the Salgado accession construction package."""
import hashlib
import json
from pathlib import Path
import unittest
from copy import deepcopy
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from validate import validate_state_machine
from finalize_salgado_accession import verify_intake_approval, old_bytes, INTAKE

ROOT = Path(__file__).resolve().parents[1]
LOT = "6529NM.2026.004"


def load(path):
    return json.loads((ROOT / path).read_bytes())


class SalgadoEvidenceJoinTests(unittest.TestCase):
    def test_intake_approval_rejects_wrong_authority_and_changed_bytes(self):
        receipt = load('notes/wip/2026-09-13-salgado-commit-review-receipt.json')
        cache = {}
        def read(path):
            if path not in cache:
                cache[path] = old_bytes(path)
            return cache[path]
        verify_intake_approval(receipt, read)
        mutations = [
            lambda r: r.update(review_outcome='rejected'),
            lambda r: r.update(reviewed_commit_sha='0' * 40, note=INTAKE),
            lambda r: r.update(reviewer_id='constructor'),
            lambda r: r['source_receipt'].update(path='unrelated.json'),
            lambda r: r['source_receipt'].update(raw_sha256='0' * 64),
            lambda r: r['source_review_artifact'].update(source_commit_sha='0' * 40),
            lambda r: r['files'].pop(),
        ]
        for mutate in mutations:
            bad = deepcopy(receipt)
            mutate(bad)
            with self.assertRaises(ValueError):
                verify_intake_approval(bad, read)
        first = receipt['files'][0]['path']
        with self.assertRaises(ValueError):
            verify_intake_approval(receipt, lambda path: read(path) + b'changed' if path == first else read(path))

    def test_register_amendment_source_forms_are_exclusive(self):
        from jsonschema import Draft202012Validator
        schema = load('schemas/accession-register.schema.json')['properties']['amendment_history']['items']
        validator = Draft202012Validator(schema)
        amendment = load('records/accessions/register.json')['amendment_history'][-1]
        self.assertEqual(list(validator.iter_errors(amendment)), [])
        reviewed = deepcopy(amendment)
        reviewed.pop('prior_source_commit')
        reviewed.pop('prior_snapshot_path')
        reviewed['prior_review_commit'] = INTAKE
        self.assertEqual(list(validator.iter_errors(reviewed)), [])
        for extra in [{'prior_source_commit': INTAKE}, {'prior_snapshot_path': 'evidence/snapshot.json'},
                      {'prior_source_commit': INTAKE, 'prior_snapshot_path': 'evidence/snapshot.json'}]:
            self.assertTrue(list(validator.iter_errors({**reviewed, **extra})))
        for missing in ['prior_source_commit', 'prior_snapshot_path']:
            bad = deepcopy(amendment)
            bad.pop(missing)
            self.assertTrue(list(validator.iter_errors(bad)))

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

    def test_admission_preserves_intake_and_exact_title_transfer_bindings(self):
        lot = load(f"records/accessions/{LOT}/accession-statement.json")["payload"]
        self.assertEqual(lot["formal_acceptance_status"], "formally_accepted")
        self.assertEqual(lot["accession_status"], "complete")
        certificate = load(f"records/accessions/{LOT}/accession-certificate.json")["payload"]
        self.assertEqual(certificate['object_ids'], lot['object_ids'])
        self.assertEqual([e['event_type'] for e in certificate['events']],
                         ['receipt', 'acceptance', 'acquisition', 'title_passage', 'custody_receipt', 'accession'])
        self.assertLess(certificate['events'][0]['occurred_at'], certificate['events'][-1]['occurred_at'])
        instrument = certificate['events'][3]['instrument']
        for oid in lot["object_ids"]:
            obj = load(f"records/accessions/{LOT}/objects/{oid}.json")["payload"]
            self.assertIn(obj["current_state"], ['technically_verified', 'preservation_complete', 'display_ready'])
            self.assertEqual([s['state'] for s in obj['state_history'][:4]],
                             ['offered', 'authorized', 'acquired', 'received_onchain'])
            binding = next(x for x in certificate['title_bindings'] if x['object_id'] == oid)
            self.assertEqual(binding, obj['title_binding'])
            self.assertEqual(binding['instrument_sha256'], instrument['sha256'])
            self.assertEqual(binding['transfer_transaction'], obj['chain_identity']['acquisition_transaction'])
            for use in ["exhibition", "publication", "preservation", "accessibility"]:
                self.assertEqual(obj["rights"][use]["grant_status"], "granted_with_conditions")

    def test_optional_reuse_is_not_an_invented_licence_or_a_display_grant(self):
        obj = load(f"records/accessions/{LOT}/objects/{LOT}.01.json")['payload']
        vocab = load('schemas/controlled-vocabularies.json')
        self.assertEqual(obj['rights']['derivative_use']['grant_status'], 'unspecified')
        self.assertEqual(obj['rights']['ai_training']['grant_status'], 'unspecified')
        self.assertEqual(validate_state_machine(obj, vocab), [])
        for use in ['exhibition', 'reproduction', 'preservation', 'ai_training']:
            bad = deepcopy(obj)
            bad['rights'][use].pop('grant_status')
            self.assertTrue(validate_state_machine(bad, vocab))
        bad = deepcopy(obj)
        bad['rights']['exhibition']['grant_status'] = 'unspecified'
        self.assertTrue(validate_state_machine(bad, vocab))

    def test_public_media_match_reviewed_hashes_and_have_no_exif_or_xmp(self):
        from PIL import Image
        display = load('evidence/salgado-amazonia-preservation/display-preparation.json')
        for obj in display['items']:
            for derivative in obj['derivatives']:
                path = ROOT / 'media/accessions' / LOT / derivative['filename']
                self.assertEqual('sha256:' + hashlib.sha256(path.read_bytes()).hexdigest(), derivative['sha256'])
                with Image.open(path) as im:
                    im.load()
                    self.assertEqual(im.size, (derivative['width'], derivative['height']))
                    self.assertNotIn('exif', im.info)
                    self.assertNotIn('xmp', im.info)


if __name__ == "__main__":
    unittest.main()
