from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

TESTS_DIR = Path(__file__).resolve().parent
REPO_ROOT = TESTS_DIR.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from canonical import canonicalize  # noqa: E402
import bootstrap_validate  # noqa: E402
from generate_manifest import DuplicateJsonKeyError as ManifestDuplicateJsonKeyError, make_manifest  # noqa: E402
from validate import keccak256, validate_records, validate_state_machine, validate_vocabularies  # noqa: E402


VALID_FIXTURES = TESTS_DIR / "fixtures" / "valid"


class ControlPlaneTests(unittest.TestCase):
    def make_records_root(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temporary = tempfile.TemporaryDirectory(prefix="museum-control-plane-")
        records = Path(temporary.name) / "records"
        records.mkdir()
        for fixture in VALID_FIXTURES.glob("*.json"):
            shutil.copy2(fixture, records / fixture.name)
        return temporary, records

    def load_record(self, records: Path, filename: str) -> dict:
        return json.loads((records / filename).read_text(encoding="utf-8"))

    def save_record(self, records: Path, filename: str, record: dict) -> None:
        (records / filename).write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")

    def refresh_content_hash(self, record: dict) -> None:
        record["envelope"]["contentHash"]["digest"] = "0x" + keccak256(canonicalize(record["payload"])).hex()

    def test_valid_fixture_chain(self) -> None:
        temporary, records = self.make_records_root()
        self.addCleanup(temporary.cleanup)
        self.assertEqual([], validate_records(Path(temporary.name)))

    def test_rfc8785_profile_and_keccak_vector(self) -> None:
        self.assertEqual(b'{"a":1,"b":2}', canonicalize({"b": 2, "a": 1}))
        golden_numbers = {
            -0.0: b"0",
            1e-6: b"0.000001",
            1e-7: b"1e-7",
            1e20: b"100000000000000000000",
            1e21: b"1e+21",
            5e-324: b"5e-324",
            1.2345678901234567: b"1.2345678901234567",
        }
        for number, expected in golden_numbers.items():
            self.assertEqual(expected, canonicalize(number), repr(number))
        self.assertEqual(b"9007199254740991", canonicalize(9007199254740991))
        with self.assertRaises(ValueError):
            canonicalize(9007199254740992)
        with self.assertRaises(ValueError):
            canonicalize(float("nan"))
        with self.assertRaises(ValueError):
            canonicalize(float("inf"))
        self.assertEqual(
            "c5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470",
            keccak256(b"").hex(),
        )

    def test_content_hash_tampering_is_rejected(self) -> None:
        temporary, records = self.make_records_root()
        self.addCleanup(temporary.cleanup)
        record = self.load_record(records, "governance-decision.json")
        record["payload"]["authority_effect"] = "tampered"
        self.save_record(records, "governance-decision.json", record)
        issues = validate_records(Path(temporary.name))
        self.assertTrue(any("contentHash.digest does not match" in issue for issue in issues), issues)

    def test_constructor_reviewer_separation_is_rejected(self) -> None:
        temporary, records = self.make_records_root()
        self.addCleanup(temporary.cleanup)
        record = self.load_record(records, "approved-collection.json")
        record["payload"]["reviewer"]["id"] = record["payload"]["constructor"]["id"]
        self.save_record(records, "approved-collection.json", record)
        issues = validate_records(Path(temporary.name))
        self.assertTrue(any("constructor/reviewer separation" in issue for issue in issues), issues)

    def test_public_sensitive_field_is_rejected(self) -> None:
        temporary, records = self.make_records_root()
        self.addCleanup(temporary.cleanup)
        record = self.load_record(records, "governance-decision.json")
        record["payload"]["private_key"] = "not-a-real-key"
        self.save_record(records, "governance-decision.json", record)
        issues = validate_records(Path(temporary.name))
        self.assertTrue(any("sensitive field is not allowed" in issue for issue in issues), issues)

    def test_unresolved_cross_reference_is_rejected(self) -> None:
        temporary, records = self.make_records_root()
        self.addCleanup(temporary.cleanup)
        record = self.load_record(records, "accession-lot.json")
        record["payload"]["object_ids"] = ["6529NM.2026.001.999"]
        self.save_record(records, "accession-lot.json", record)
        issues = validate_records(Path(temporary.name))
        self.assertTrue(any("unresolved record reference" in issue for issue in issues), issues)

    def test_self_supersession_is_rejected(self) -> None:
        temporary, records = self.make_records_root()
        self.addCleanup(temporary.cleanup)
        record = self.load_record(records, "governance-decision.json")
        record["payload"]["supersedes"] = record["payload"]["record_id"]
        self.save_record(records, "governance-decision.json", record)
        issues = validate_records(Path(temporary.name))
        self.assertTrue(any("supersedes must not point to itself" in issue for issue in issues), issues)

    def test_accession_cross_field_integrity_is_rejected(self) -> None:
        mutations = (
            ("title_binding", "transfer_transaction", "0x" + "c" * 64, "title_binding.transfer_transaction must match"),
            ("title_binding", "to", "0x" + "4" * 40, "title_binding.to must match"),
            ("chain_identity", "caip19", "eip155:1/erc721:0x1111111111111111111111111111111111111111/2", "chain_identity.caip19 token must match"),
        )
        for section, key, value, expected in mutations:
            with self.subTest(section=section, key=key):
                temporary, records = self.make_records_root()
                self.addCleanup(temporary.cleanup)
                record = self.load_record(records, "object-record.json")
                record["payload"][section][key] = value
                self.save_record(records, "object-record.json", record)
                issues = validate_records(Path(temporary.name))
                self.assertTrue(any(expected in issue for issue in issues), issues)

    def test_accession_event_chain_separation_is_rejected(self) -> None:
        temporary, records = self.make_records_root()
        self.addCleanup(temporary.cleanup)
        record = self.load_record(records, "accession.json")
        record["payload"]["events"][1]["event_type"] = "acquisition"
        record["payload"]["events"][4]["custody_path"]["instrument_reference"] = "6529NM-INSTR-2026-999"
        self.save_record(records, "accession.json", record)
        issues = validate_records(Path(temporary.name))
        self.assertTrue(any("ACCESSION.events must contain" in issue for issue in issues), issues)
        self.assertTrue(any("instrument_reference must match" in issue for issue in issues), issues)

    def test_accession_binding_requirements_and_strict_chronology_are_rejected(self) -> None:
        mutations = (
            (lambda record: record["payload"]["title_bindings"][0].update(status="pending"), "executed title binding"),
            (lambda record: record["payload"]["events"][3]["instrument"].update(sha256="sha256:" + "d" * 64), "instrument sha256"),
            (lambda record: record["payload"]["events"][1].update(occurred_at=record["payload"]["events"][0]["occurred_at"]), "strictly increasing"),
        )
        for mutate, expected in mutations:
            with self.subTest(expected=expected):
                temporary, records = self.make_records_root()
                self.addCleanup(temporary.cleanup)
                record = self.load_record(records, "accession.json")
                mutate(record)
                self.save_record(records, "accession.json", record)
                issues = validate_records(Path(temporary.name))
                self.assertTrue(any(expected in issue for issue in issues), issues)

        temporary, records = self.make_records_root()
        self.addCleanup(temporary.cleanup)
        record = self.load_record(records, "accession.json")
        record["payload"]["title_bindings"].append(dict(record["payload"]["title_bindings"][0]))
        self.save_record(records, "accession.json", record)
        issues = validate_records(Path(temporary.name))
        self.assertTrue(any("exactly one title binding per object_id" in issue for issue in issues), issues)

    def test_rights_and_condition_events_require_their_own_authority_timeline(self) -> None:
        temporary, records = self.make_records_root()
        self.addCleanup(temporary.cleanup)
        rights = self.load_record(records, "rights-statement.json")
        rights["payload"]["events"][0]["event_type"] = "rights_amendment"
        self.save_record(records, "rights-statement.json", rights)
        condition = self.load_record(records, "condition-report.json")
        condition["payload"]["events"][0]["event_type"] = "condition_reassessment"
        self.save_record(records, "condition-report.json", condition)
        issues = validate_records(Path(temporary.name))
        self.assertTrue(any("RIGHTS_STATEMENT.events must begin" in issue for issue in issues), issues)
        self.assertTrue(any("CONDITION_REPORT.events must begin" in issue for issue in issues), issues)

    def test_private_network_envelope_uri_is_rejected(self) -> None:
        for uri in (
            "https://127.0.0.1/private-record",
            "https://0.0.0.0/private-record",
            "https://169.254.169.254/latest/meta-data",
            "https://[::1]/private-record",
            "https://[fd00::1]/private-record",
            "https://192.0.2.1/private-record",
        ):
            with self.subTest(uri=uri):
                temporary, records = self.make_records_root()
                self.addCleanup(temporary.cleanup)
                record = self.load_record(records, "object-record.json")
                record["envelope"]["uri"] = uri
                self.save_record(records, "object-record.json", record)
                issues = validate_records(Path(temporary.name))
                self.assertTrue(any("envelope.uri: local/private network URL" in issue for issue in issues), issues)

    def test_caip19_and_custody_chain_bindings_are_enforced(self) -> None:
        temporary, records = self.make_records_root()
        self.addCleanup(temporary.cleanup)
        record = self.load_record(records, "object-record.json")
        record["payload"]["chain_identity"]["token_standard"] = "ERC-1155"
        record["payload"]["chain_identity"]["caip19"] = "eip155:1/erc1155:0x1111111111111111111111111111111111111111/1"
        self.refresh_content_hash(record)
        self.save_record(records, "object-record.json", record)
        issues = validate_records(Path(temporary.name))
        self.assertFalse(any("caip19" in issue for issue in issues), issues)

        record["payload"]["chain_identity"]["custody_account"] = "eip155:5:0x2222222222222222222222222222222222222222"
        self.refresh_content_hash(record)
        self.save_record(records, "object-record.json", record)
        issues = validate_records(Path(temporary.name))
        self.assertTrue(any("custody_account chain must match" in issue for issue in issues), issues)

    def test_undecodable_evidence_fails_closed(self) -> None:
        temporary = tempfile.TemporaryDirectory(prefix="museum-undecodable-evidence-")
        self.addCleanup(temporary.cleanup)
        evidence = Path(temporary.name) / "evidence"
        evidence.mkdir()
        (evidence / "binary.bin").write_bytes(b"\xff\x00credential-shaped")
        with patch.object(bootstrap_validate, "ROOT", Path(temporary.name)):
            with self.assertRaises(SystemExit):
                bootstrap_validate.check_public_record_safety()

    def test_duplicate_json_keys_are_rejected_before_validation_and_hashing(self) -> None:
        temporary, records = self.make_records_root()
        self.addCleanup(temporary.cleanup)
        (records / "duplicate.json").write_text('{"record_id":"first","record_id":"second"}\n', encoding="utf-8")
        issues = validate_records(Path(temporary.name))
        self.assertTrue(any("duplicate JSON object key" in issue for issue in issues), issues)

        manifest_root = Path(temporary.name) / "manifest-root"
        (manifest_root / "schemas").mkdir(parents=True)
        (manifest_root / "schemas" / "duplicate.json").write_text('{"digest":"one","digest":"two"}\n', encoding="utf-8")
        with self.assertRaises(ManifestDuplicateJsonKeyError):
            make_manifest(manifest_root)

    def test_nested_title_binding_unknown_field_is_rejected(self) -> None:
        temporary, records = self.make_records_root()
        self.addCleanup(temporary.cleanup)
        record = self.load_record(records, "object-record.json")
        record["payload"]["title_binding"]["unexpected"] = "reject me"
        self.save_record(records, "object-record.json", record)
        issues = validate_records(Path(temporary.name))
        self.assertTrue(any("unexpected" in issue and "unevaluated" in issue.lower() for issue in issues), issues)

    def test_rights_grant_classes_and_status_are_closed(self) -> None:
        temporary, records = self.make_records_root()
        self.addCleanup(temporary.cleanup)
        record = self.load_record(records, "rights-statement.json")
        record["payload"]["grants"]["unknown_class"] = {
            "grant_status": "granted",
            "basis": "invalid class",
            "observed_at": "2026-08-01T00:00:00Z",
        }
        self.save_record(records, "rights-statement.json", record)
        issues = validate_records(Path(temporary.name))
        self.assertTrue(any("unknown_class" in issue for issue in issues), issues)

        record = self.load_record(records, "rights-statement.json")
        record["payload"]["grants"]["reproduction"]["grant_status"] = "maybe"
        self.save_record(records, "rights-statement.json", record)
        issues = validate_records(Path(temporary.name))
        self.assertTrue(any("maybe" in issue for issue in issues), issues)

    def test_malformed_workflow_vocabularies_fail_closed(self) -> None:
        malformed = {"workflow_states": ["offered"], "workflow_transitions": None}
        self.assertTrue(validate_vocabularies(malformed))
        self.assertTrue(
            validate_state_machine(
                {"record_type": "WORK_DESCRIPTION", "state_history": []},
                malformed,
            )
        )

    def test_invalid_workflow_transition_is_rejected(self) -> None:
        temporary, records = self.make_records_root()
        self.addCleanup(temporary.cleanup)
        record = self.load_record(records, "object-record.json")
        record["payload"]["state_history"][2]["state"] = "display_ready"
        self.save_record(records, "object-record.json", record)
        issues = validate_records(Path(temporary.name))
        self.assertTrue(any("invalid transition" in issue for issue in issues), issues)

    def test_governance_source_status_is_semantic_not_vote_count(self) -> None:
        temporary, records = self.make_records_root()
        self.addCleanup(temporary.cleanup)
        record = self.load_record(records, "governance-decision.json")
        record["payload"]["decision_status"] = "not_adopted"
        self.save_record(records, "governance-decision.json", record)
        issues = validate_records(Path(temporary.name))
        self.assertTrue(any("WINNER must be recorded as adopted" in issue for issue in issues), issues)

    def test_manifest_is_deterministic_and_has_both_commitments(self) -> None:
        manifest = make_manifest(REPO_ROOT)
        self.assertEqual("6529NM_RECORD_MANIFEST", manifest["manifest_type"])
        self.assertTrue(manifest["entries"])
        self.assertTrue(all("\\" not in entry["path"] for entry in manifest["entries"]))
        self.assertTrue(all(not entry["path"].startswith("evidence/") for entry in manifest["entries"]))
        self.assertRegex(manifest["manifest_commitment"]["digest"], r"^0x[0-9a-f]{64}$")
        self.assertRegex(manifest["manifest_sha256"], r"^sha256:[0-9a-f]{64}$")
        self.assertEqual(manifest, make_manifest(REPO_ROOT))

    def test_foundation_bootstrap_controls_pass_current_register(self) -> None:
        result = subprocess.run(
            [sys.executable, str(REPO_ROOT / "scripts" / "bootstrap_validate.py")],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
