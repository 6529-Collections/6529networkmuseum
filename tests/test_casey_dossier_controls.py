from __future__ import annotations

import copy
import hashlib
import json
import shutil
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
import sys

sys.path.insert(0, str(SCRIPTS))

from canonical import canonicalize  # noqa: E402
from validate import keccak256, load_schemas, validate_gift_acceptance_authorization, validate_visual_observation, validator_for  # noqa: E402
from validate_casey_dossier import CASEY_ID, GIFT_AUTHORIZATION_ID, OBJECT_TO_DESCRIPTOR, VISUAL_OBSERVATION_ID, validate  # noqa: E402


class CaseyDossierControlsTests(unittest.TestCase):
    def make_copy(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temporary = tempfile.TemporaryDirectory(prefix="casey-dossier-")
        destination = Path(temporary.name) / "repo"
        shutil.copytree(ROOT, destination, ignore=shutil.ignore_patterns(".git", "__pycache__"))
        self.addCleanup(temporary.cleanup)
        return temporary, destination

    @staticmethod
    def refresh_record(record: dict) -> None:
        payload = record["payload"]
        body = {key: value for key, value in payload.items() if key != "payload_sha256"}
        payload["payload_sha256"] = "sha256:" + hashlib.sha256(canonicalize(body)).hexdigest()
        record["envelope"]["contentHash"]["digest"] = "0x" + keccak256(canonicalize(payload)).hex()

    def mutate_record(self, root: Path, relative: str, mutation: object) -> None:
        path = root / relative
        record = json.loads(path.read_text(encoding="utf-8"))
        mutation(record)
        self.refresh_record(record)
        path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8", newline="\n")

    def test_published_descriptor_dossier_is_valid(self) -> None:
        self.assertEqual(validate(ROOT), [])

    def test_source_binding_descriptor_mapping_urls_and_states_fail_closed(self) -> None:
        mutations = (
            (
                "records/accessions/6529NM.2026.001/accession-statement.json",
                lambda record: record["payload"]["source_manifest"]["casey_collection_snapshot_package"].__setitem__("published_source_commit", "0" * 40),
                "published source package",
            ),
            (
                "records/accessions/6529NM.2026.001/accession-statement.json",
                lambda record: record["payload"]["source_manifest"]["casey_collection_snapshot_package"]["package_manifest"].__setitem__("sha256", "sha256:" + "0" * 64),
                "published source package",
            ),
            (
                "records/accessions/6529NM.2026.001/accession-statement.json",
                lambda record: record["payload"]["source_manifest"]["casey_collection_snapshot_package"]["publication_release"].__setitem__("sha256", "sha256:" + "0" * 64),
                "published source package",
            ),
            (
                "records/accessions/6529NM.2026.001/accession-statement.json",
                lambda record: record["payload"]["source_manifest"]["casey_collection_snapshot_package"]["publication_release"].__setitem__("published_release_commit", "0" * 40),
                "published source package",
            ),
            (
                "records/accessions/6529NM.2026.001/accession-statement.json",
                lambda record: record["payload"]["source_manifest"]["casey_collection_snapshot_package"]["package_manifest"].__setitem__("uri", "https://github.com/6529-Collections/6529networkmuseum/blob/main/evidence/casey-reas-collection-snapshots/package-manifest.json"),
                "published source package",
            ),
            (
                "records/accessions/6529NM.2026.001/objects/6529NM.2026.001.01.json",
                lambda record: record["payload"]["trait_analysis"]["descriptor"].__setitem__("path", "evidence/casey-reas-collection-snapshots/descriptors/pre-process.json"),
                "descriptor mapping",
            ),
            (
                "records/accessions/6529NM.2026.001/accession-statement.json",
                lambda record: record["envelope"].__setitem__("uri", "https://github.com/6529-Collections/6529networkmuseum/tree/" + "codex/casey-reas-accession/records/accessions/6529NM.2026.001"),
                "mutable construction-branch URL",
            ),
            (
                "records/accessions/6529NM.2026.001/objects/6529NM.2026.001.01.json",
                lambda record: record["payload"].__setitem__("current_state", "accessioned"),
                "must remain received_onchain",
            ),
            (
                "records/accessions/6529NM.2026.001/accession-statement.json",
                lambda record: record["payload"]["controlled_decision"].__setitem__("decision_authority", "unverified authority"),
                "reviewer and decision-authority fields must remain null",
            ),
            (
                "records/accessions/6529NM.2026.001/accession-statement.json",
                lambda record: record["payload"].__setitem__("formal_acceptance_status", "not_formally_accepted"),
                "formal gift acceptance",
            ),
            (
                "records/accessions/6529NM.2026.001/gift-acceptance-authorization.json",
                lambda record: record["payload"]["assets"][0].__setitem__("token_id", "100000724"),
                "seven assets, receipt",
            ),
            (
                "records/accessions/6529NM.2026.001/gift-acceptance-authorization.json",
                lambda record: record["payload"]["institutional_decision_authority"].__setitem__("documentation_qa_status", "reviewed"),
                "separate effective institutional acceptance",
            ),
            (
                "records/accessions/6529NM.2026.001/accession-statement.json",
                lambda record: record["payload"].__setitem__("governing_references", [CASEY_ID]),
                "governing references",
            ),
            (
                "records/accessions/6529NM.2026.001/accession-statement.json",
                lambda record: record["payload"].__setitem__("references", [VISUAL_OBSERVATION_ID]),
                "generic reference graph",
            ),
            (
                "records/accessions/6529NM.2026.001/visual-observation-record.json",
                lambda record: record["payload"]["objects"][0]["static_capture"].__setitem__("response_sha256", "sha256:" + "0" * 64),
                "static response binding",
            ),
            (
                "records/accessions/6529NM.2026.001/visual-observation-record.json",
                lambda record: record["payload"]["objects"][0]["raw_metadata_source"].__setitem__("image_url", "https://example.com/wrong.png"),
                "raw metadata URL/hash binding",
            ),
            (
                "records/accessions/6529NM.2026.001/visual-observation-record.json",
                lambda record: record["payload"]["objects"][0]["live_capture"].__setitem__("minimum_wait_between_frames_ms", 1499),
                "live screenshot binding",
            ),
            (
                "records/accessions/6529NM.2026.001/visual-observation-record.json",
                lambda record: record["payload"]["objects"][0]["live_capture"]["frames"][0].__setitem__("captured_at", "2026-08-01T23:34:21Z"),
                "live screenshot binding",
            ),
            (
                "records/accessions/6529NM.2026.001/visual-observation-record.json",
                lambda record: record["payload"]["objects"][0]["static_capture"]["retention"].__setitem__("bytes_retained_in_public_repository", True),
                "public-byte non-retention",
            ),
            (
                "records/accessions/6529NM.2026.001/visual-observation-record.json",
                lambda record: record["payload"]["limitations"].__setitem__(2, "The commanded wait is approximate."),
                "timing/retention limitation",
            ),
            (
                "records/accessions/6529NM.2026.001/objects/6529NM.2026.001.01.json",
                lambda record: record["payload"].__setitem__("medium", "On-chain generative software art; deterministic token-hash output; ERC-721 token on Ethereum."),
                "unverified live-determinism boundary",
            ),
        )
        for relative, mutation, expected in mutations:
            with self.subTest(expected=expected):
                _temporary, root = self.make_copy()
                self.mutate_record(root, relative, mutation)
                self.assertTrue(any(expected in issue for issue in validate(root, history_root=ROOT)), validate(root, history_root=ROOT))

    def test_public_pages_and_raw_metadata_are_bound(self) -> None:
        for object_id, slug in OBJECT_TO_DESCRIPTOR.items():
            page = (ROOT / "records" / "accessions" / CASEY_ID / "public" / f"{object_id}.md").read_text(encoding="utf-8")
            self.assertIn("transparent linked descriptor", page)
            self.assertIn(f"descriptors/{slug}.json", page)
            self.assertIn("The Gift Acceptance and Accession Authorization was issued and formally accepts the gift; it does not complete accession.", page)
            self.assertIn("Title, rights, condition, preservation, and registrar review remain pending.", page)
            self.assertIn("rights-cleared derivative or a controlled restricted copy", page)
            self.assertEqual(page.count("Independent visual audit of the unretained captures will require a future rights-cleared derivative or a controlled restricted copy."), 1)
            self.assertIn("artist and practice profile", page)
            self.assertIn("collection essay", page)
            self.assertIn("../visual-observation-record.json", page)
            self.assertNotIn("pending linked deliverable", page)
        _temporary, root = self.make_copy()
        raw = root / "evidence" / "casey-reas" / "raw" / "metadata" / f"{CASEY_ID}.01.json"
        raw.write_bytes(raw.read_bytes() + b"\n")
        self.assertTrue(any("raw public metadata manifest binding failed" in issue for issue in validate(root, history_root=ROOT)), validate(root, history_root=ROOT))

    def test_historical_release_requires_full_git_history(self) -> None:
        with tempfile.TemporaryDirectory(prefix="casey-history-") as directory:
            issues = validate(ROOT, history_root=Path(directory))
        self.assertTrue(any("immutable publication evidence cannot be verified" in issue for issue in issues), issues)

    def test_gift_schema_is_generic_but_casey_binding_is_exact(self) -> None:
        schema = json.loads((ROOT / "schemas" / "gift-acceptance-authorization.schema.json").read_text(encoding="utf-8"))
        rendered = json.dumps(schema, sort_keys=True)
        self.assertFalse(schema["unevaluatedProperties"])
        self.assertNotIn("punk6529", rendered)
        self.assertNotIn("networkmuseum.6529.eth", rendered)
        self.assertNotIn('"maxItems": 7', rendered)
        source_types = schema["$defs"]["authorityDeclaration"]["properties"]["source_type"]["enum"]
        authority_bases = schema["$defs"]["institutionalDecisionAuthority"]["properties"]["authority_basis"]["enum"]
        governing_basis = schema["allOf"][1]["properties"]["governing_basis"]
        self.assertGreater(len(source_types), 1)
        self.assertGreater(len(authority_bases), 1)
        self.assertEqual(1, governing_basis["minItems"])
        self.assertNotIn("maxItems", governing_basis)
        record = json.loads((ROOT / "records" / "accessions" / CASEY_ID / "gift-acceptance-authorization.json").read_text(encoding="utf-8"))
        self.assertEqual(GIFT_AUTHORIZATION_ID, record["payload"]["record_id"])
        self.assertEqual("formally_accepted", record["payload"]["institutional_decision_authority"]["decision_status"])
        self.assertEqual("pending_independent_review", record["payload"]["institutional_decision_authority"]["documentation_qa_status"])

    def test_generic_gift_semantics_reject_projected_duplicates_and_count_mismatch(self) -> None:
        record = json.loads((ROOT / "records" / "accessions" / CASEY_ID / "gift-acceptance-authorization.json").read_text(encoding="utf-8"))
        payload = record["payload"]
        mutations = (
            (lambda value: value["assets"][1].__setitem__("object_id", value["assets"][0]["object_id"]), "duplicate object_id"),
            (lambda value: value["assets"][1].__setitem__("caip19", value["assets"][0]["caip19"]), "duplicate caip19"),
            (lambda value: (value["assets"][1].__setitem__("contract", value["assets"][0]["contract"]), value["assets"][1].__setitem__("token_id", value["assets"][0]["token_id"])), "duplicate contract+token_id"),
            (lambda value: value["assets"][1].__setitem__("custody_receipt_log", value["assets"][0]["custody_receipt_log"]), "duplicate custody_receipt_log"),
            (lambda value: value["custody_receipt"].__setitem__("transfer_count", 6), "transfer_count must equal assets.length"),
        )
        for mutation, expected in mutations:
            with self.subTest(expected=expected):
                candidate = copy.deepcopy(payload)
                mutation(candidate)
                issues = validate_gift_acceptance_authorization(candidate)
                self.assertTrue(any(expected in issue for issue in issues), issues)

    def test_generic_gift_schema_accepts_non_wave_basis_and_rejects_malformed_unions(self) -> None:
        _vocabularies, _envelope, store = load_schemas(ROOT)
        schema = json.loads((ROOT / "schemas" / "gift-acceptance-authorization.schema.json").read_text(encoding="utf-8"))
        validator = validator_for(schema, store)
        record = json.loads((ROOT / "records" / "accessions" / CASEY_ID / "gift-acceptance-authorization.json").read_text(encoding="utf-8"))
        payload = record["payload"]
        non_wave_basis = {
            "basis_type": "delegated_authority_record",
            "record_id": "6529NM-AUTH-DELEGATION-001",
            "title": "Delegated gift-acceptance authority",
            "authority_effect": "delegates_acceptance_authority",
            "effective_at": "2026-01-01T00:00:00Z",
            "source_uri": "https://example.org/museum/authority/6529NM-AUTH-DELEGATION-001",
        }
        candidate = copy.deepcopy(payload)
        candidate["governing_basis"] = [non_wave_basis]
        candidate["institutional_decision_authority"]["authority_basis"] = "delegated_accession_authority"
        self.assertEqual([], list(validator.iter_errors(candidate)))
        malformed = []
        wrong_branch = copy.deepcopy(payload["governing_basis"][0])
        wrong_branch["basis_type"] = "delegated_authority_record"
        malformed.append(wrong_branch)
        missing_wave_field = copy.deepcopy(payload["governing_basis"][0])
        missing_wave_field.pop("drop_id")
        malformed.append(missing_wave_field)
        missing_record_effect = copy.deepcopy(non_wave_basis)
        missing_record_effect.pop("authority_effect")
        malformed.append(missing_record_effect)
        for basis in malformed:
            with self.subTest(basis=basis["basis_type"]):
                candidate = copy.deepcopy(payload)
                candidate["governing_basis"] = [basis]
                self.assertTrue(list(validator.iter_errors(candidate)))

    def test_visual_observation_generic_relationships_and_closed_schema(self) -> None:
        schema = json.loads((ROOT / "schemas" / "visual-observation.schema.json").read_text(encoding="utf-8"))
        self.assertFalse(schema["unevaluatedProperties"])
        record = json.loads((ROOT / "records" / "accessions" / CASEY_ID / "visual-observation-record.json").read_text(encoding="utf-8"))
        payload = record["payload"]
        self.assertEqual([], validate_visual_observation(payload))
        candidate = copy.deepcopy(payload)
        candidate["objects"][0]["live_capture"]["source_url"] = "https://example.com/wrong"
        self.assertTrue(any("generator_url" in issue for issue in validate_visual_observation(candidate)))
        candidate = copy.deepcopy(payload)
        candidate["objects"][0]["live_capture"]["changed"] = False
        self.assertTrue(any("hash inequality" in issue for issue in validate_visual_observation(candidate)))
        for item in payload["objects"]:
            live = item["live_capture"]
            self.assertEqual([None, None], [frame["captured_at"] for frame in live["frames"]])
            self.assertEqual(1500, live["minimum_wait_between_frames_ms"])


if __name__ == "__main__":
    unittest.main()
