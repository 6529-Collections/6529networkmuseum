from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from datetime import UTC, datetime, timedelta
from pathlib import Path
from unittest.mock import patch

TESTS_DIR = Path(__file__).resolve().parent
REPO_ROOT = TESTS_DIR.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from canonical import canonicalize  # noqa: E402
import bootstrap_validate  # noqa: E402
from check_fetch_guard import scan_file, scan_tree  # noqa: E402
from generate_manifest import DuplicateJsonKeyError as ManifestDuplicateJsonKeyError, make_manifest, normalized_bytes  # noqa: E402
from safe_fetch import SAFE_FETCH_POLICY, FetchPolicyError, SafeHTTPSFetcher, canonicalize_https_url  # noqa: E402
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

    def make_repository_copy(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temporary = tempfile.TemporaryDirectory(prefix="museum-repository-" )
        destination = Path(temporary.name) / "repo"
        shutil.copytree(
            REPO_ROOT,
            destination,
            ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"),
        )
        return temporary, destination

    def refresh_review_hash(self, record: dict) -> None:
        review = record["record_control"]["review"]
        review["payload_sha256"] = bootstrap_validate.canonical_payload_hash(record)

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

    def test_accession_custody_path_is_bound_to_executed_title_binding(self) -> None:
        for field, value in (
            ("from", "0x4444444444444444444444444444444444444444"),
            ("to", "0x5555555555555555555555555555555555555555"),
            ("custodian_reference", "othermuseum.example"),
        ):
            with self.subTest(field=field):
                temporary, records = self.make_records_root()
                self.addCleanup(temporary.cleanup)
                record = self.load_record(records, "accession.json")
                record["payload"]["events"][4]["custody_path"][field] = value
                self.save_record(records, "accession.json", record)
                issues = validate_records(Path(temporary.name))
                self.assertTrue(any(f"custody_path.{field} must match" in issue for issue in issues), issues)

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
            "https://127.1/private-record",
            "https://2130706433/private-record",
            "https://127.0.0.1.nip.io/private-record",
            "https://nip.io/private-record",
            "https://redirect.127.0.0.1.nip.io/private-record",
            "https://metadata/private-record",
            "https://0x7f000001/private-record",
            "https://%31%32%37.0.0.1/private-record",
            "https://[::ffff:127.0.0.1]/private-record",
            "https://*.example.com/private-record",
        ):
            with self.subTest(uri=uri):
                temporary, records = self.make_records_root()
                self.addCleanup(temporary.cleanup)
                record = self.load_record(records, "object-record.json")
                record["envelope"]["uri"] = uri
                self.save_record(records, "object-record.json", record)
                issues = validate_records(Path(temporary.name))
                self.assertTrue(any("envelope.uri: local/private network URL" in issue for issue in issues), issues)

    def test_endpoint_fetch_policy_is_fail_closed_and_redirect_aware(self) -> None:
        vocabularies = json.loads((REPO_ROOT / "schemas/controlled-vocabularies.json").read_text(encoding="utf-8"))
        self.assertEqual(
            SAFE_FETCH_POLICY,
            vocabularies["endpoint_policy"],
        )
        mutated = dict(vocabularies)
        mutated["endpoint_policy"] = {**vocabularies["endpoint_policy"], "recheck_every_redirect": False}
        self.assertTrue(any("endpoint_policy" in issue for issue in validate_vocabularies(mutated)))

    def make_mock_fetcher(self, answers: dict[str, list[str]], responses: dict[str, tuple[int, dict[str, str], bytes, str | None]], clock=None):
        connections = []

        class MockResponse:
            def __init__(self, status: int, headers: dict[str, str], body: bytes) -> None:
                self.status = status
                self.headers = headers
                self.body = body

            def read(self, _limit: int) -> bytes:
                return self.body

        class MockConnection:
            def __init__(self, response: MockResponse, peer_ip: str) -> None:
                self.response = response
                self.peer_ip = peer_ip
                self.requests = []
                self.closed = False

            def request(self, method: str, target: str, headers: dict[str, str]) -> MockResponse:
                self.requests.append((method, target, headers))
                return self.response

            def close(self) -> None:
                self.closed = True

        def resolver(hostname: str, _port: int) -> list[str]:
            return answers[hostname]

        def factory(endpoint, resolved, _policy):
            status, headers, body, peer = responses[endpoint.hostname]
            connection = MockConnection(MockResponse(status, headers, body), peer or resolved.selected_ip)
            connections.append((endpoint, connection))
            return connection

        fixed_clock = clock or (lambda: datetime(2026, 8, 1, tzinfo=UTC))
        return SafeHTTPSFetcher(resolver=resolver, connection_factory=factory, clock=fixed_clock), connections

    def test_safe_fetch_rejects_rebinding_private_answers_and_alternate_ip_forms(self) -> None:
        for url in (
            "https://2130706433/private",
            "https://127.1/private",
            "https://0x7f000001/private",
            "https://[::ffff:127.0.0.1]/private",
            "https://%31%32%37.0.0.1/private",
            "https://127.0.0.1.nip.io/private",
        ):
            with self.subTest(url=url):
                with self.assertRaises(FetchPolicyError):
                    canonicalize_https_url(url)

        for answers in (
            [],
            ["93.184.216.34", "127.0.0.1"],
            ["2606:4700:4700::1111", "169.254.169.254"],
        ):
            with self.subTest(answers=answers):
                fetcher, _connections = self.make_mock_fetcher(
                    {"rebind.example.test": answers},
                    {"rebind.example.test": (200, {"Content-Length": "2"}, b"ok", None)},
                )
                with self.assertRaises(FetchPolicyError):
                    fetcher.fetch("https://rebind.example.test/data")

    def test_safe_fetch_rechecks_redirects_and_rejects_metadata(self) -> None:
        fetcher, connections = self.make_mock_fetcher(
            {"redirect.example.test": ["93.184.216.34"]},
            {
                "redirect.example.test": (302, {"Location": "https://169.254.169.254/latest/meta-data"}, b"", None),
            },
        )
        with self.assertRaises(FetchPolicyError):
            fetcher.fetch("https://redirect.example.test/start")
        self.assertEqual(1, len(connections))

    def test_safe_fetch_pins_ipv6_peer_and_emits_observation(self) -> None:
        fetcher, connections = self.make_mock_fetcher(
            {
                "redirect.example.test": ["93.184.216.34"],
                "cdn.example.test": ["2001:4860:4860::8888"],
            },
            {
                "redirect.example.test": (302, {"Location": "https://cdn.example.test/final"}, b"", None),
                "cdn.example.test": (200, {"Content-Length": "5", "Content-Type": "image/png; charset=binary"}, b"hello", None),
            },
        )
        result = fetcher.fetch("https://redirect.example.test/start")
        self.assertEqual(b"hello", result.body)
        self.assertEqual("https://cdn.example.test/final", result.observation.canonical_url)
        self.assertEqual(
            ("https://redirect.example.test/start", "https://cdn.example.test/final"),
            result.observation.redirect_chain,
        )
        self.assertEqual("2001:4860:4860::8888", result.observation.selected_ip)
        self.assertEqual("image/png", result.observation.media_type)
        self.assertEqual(hashlib.sha256(b"hello").hexdigest(), result.observation.byte_sha256)
        self.assertEqual(2, len(result.observation.hops))
        self.assertEqual("redirect.example.test", connections[0][1].requests[0][2]["Host"])

    def test_safe_fetch_rejects_peer_mismatch_expiry_methods_credentials_and_size(self) -> None:
        fetcher, _connections = self.make_mock_fetcher(
            {"good.example.test": ["93.184.216.34"]},
            {"good.example.test": (200, {"Content-Length": "2"}, b"ok", "93.184.216.35")},
        )
        with self.assertRaises(FetchPolicyError):
            fetcher.fetch("https://good.example.test/data")

        fetcher, _connections = self.make_mock_fetcher(
            {"good.example.test": ["93.184.216.34"]},
            {"good.example.test": (200, {"Content-Length": "2"}, b"ok", None)},
        )
        fixed = datetime(2026, 8, 1, tzinfo=UTC)
        with self.assertRaises(FetchPolicyError):
            fetcher.fetch("https://good.example.test/data", expires_at=fixed - timedelta(seconds=1))
        with self.assertRaises(FetchPolicyError):
            fetcher.fetch("https://good.example.test/data", method="POST")
        with self.assertRaises(FetchPolicyError):
            fetcher.fetch("https://good.example.test/data", headers={"Authorization": "Bearer secret"})
        with self.assertRaises(FetchPolicyError):
            canonicalize_https_url("https://good.example.test:444/data")

        fetcher, _connections = self.make_mock_fetcher(
            {"good.example.test": ["93.184.216.34"]},
            {"good.example.test": (200, {"Content-Length": str(int(SAFE_FETCH_POLICY["max_response_bytes"]) + 1)}, b"", None)},
        )
        with self.assertRaises(FetchPolicyError):
            fetcher.fetch("https://good.example.test/data")

    def test_fetch_guard_allows_only_approved_module_and_rejects_direct_clients(self) -> None:
        self.assertEqual([], scan_tree(REPO_ROOT))
        temporary = tempfile.TemporaryDirectory(prefix="museum-fetch-guard-")
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        bad = root / "bad.py"
        bad.write_text(
            "import requests\nfrom urllib.request import urlopen\nimport socket\nsocket.create_connection(('example.test', 443))\n",
            encoding="utf-8",
        )
        violations = scan_file(bad, root)
        self.assertGreaterEqual(len(violations), 4, violations)

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

    def test_manifest_authorized_binary_evidence_is_checked_before_text_decode(self) -> None:
        temporary = tempfile.TemporaryDirectory(prefix="museum-binary-evidence-")
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        evidence = root / "evidence"
        evidence.mkdir()
        binary = b"\x89PNG\r\n\x1a\npublic-image-bytes"
        image = evidence / "image.png"
        image.write_bytes(binary)
        manifest = evidence / "manifest.json"
        manifest.write_text(
            json.dumps(
                {
                    "hash_algorithm": "sha256",
                    "byte_mode": "raw",
                    "entries": [
                        {
                            "path": "image.png",
                            "byte_mode": "raw",
                            "media_type": "image/png",
                            "size": len(binary),
                            "sha256": hashlib.sha256(binary).hexdigest(),
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )
        loaded = {manifest: json.loads(manifest.read_text(encoding="utf-8"))}
        with patch.object(bootstrap_validate, "ROOT", root):
            entries = bootstrap_validate.check_evidence_manifests(loaded)
            bootstrap_validate.check_public_record_safety(entries)

        credential_shapes = (
            b"api_key=synthetic-secret-value",
            b"ghp_" + b"a" * 36,
            b"AKIA" + b"A" * 16,
            b"private_key=0x" + b"b" * 64,
            b"-----BEGIN PRIVATE KEY-----",
        )
        for credential in credential_shapes:
            with self.subTest(credential=credential[:12]):
                payload = b"\x89PNG\r\n\x1a\npublic-image\n" + credential
                image.write_bytes(payload)
                manifest.write_text(
                    json.dumps(
                        {
                            "hash_algorithm": "sha256",
                            "byte_mode": "raw",
                            "entries": [
                                {
                                    "path": "image.png",
                                    "byte_mode": "raw",
                                    "media_type": "image/png",
                                    "size": len(payload),
                                    "sha256": hashlib.sha256(payload).hexdigest(),
                                }
                            ],
                        }
                    ),
                    encoding="utf-8",
                )
                with patch.object(bootstrap_validate, "ROOT", root):
                    entries = bootstrap_validate.check_evidence_manifests({manifest: json.loads(manifest.read_text(encoding="utf-8"))})
                    with self.assertRaises(SystemExit):
                        bootstrap_validate.check_public_record_safety(entries)

        manifest.write_text(
            json.dumps(
                {
                    "hash_algorithm": "sha256",
                    "byte_mode": "raw",
                    "entries": [
                        {
                            "path": "image.png",
                            "byte_mode": "raw",
                            "media_type": "image/png",
                            "size": len(binary),
                            "sha256": hashlib.sha256(binary).hexdigest(),
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )
        image.write_bytes(binary)

        executable = b"MZ-not-an-image"
        image.write_bytes(executable)
        manifest.write_text(
            manifest.read_text(encoding="utf-8").replace("image/png", "application/octet-stream").replace(
                hashlib.sha256(binary).hexdigest(), hashlib.sha256(executable).hexdigest()
            ).replace(str(len(binary)), str(len(executable))),
            encoding="utf-8",
        )
        with patch.object(bootstrap_validate, "ROOT", root):
            entries = bootstrap_validate.check_evidence_manifests({manifest: json.loads(manifest.read_text(encoding="utf-8"))})
            with self.assertRaises(SystemExit):
                bootstrap_validate.check_public_record_safety(entries)

        image.write_bytes(b"\xff\x00undeclared")
        manifest.unlink()
        with patch.object(bootstrap_validate, "ROOT", root):
            with self.assertRaises(SystemExit):
                bootstrap_validate.check_public_record_safety()

    def test_full_validator_enforces_all_governed_record_schemas(self) -> None:
        result = subprocess.run(
            [sys.executable, str(REPO_ROOT / "scripts" / "validate.py")],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_direct_governed_record_schema_mutations_are_rejected(self) -> None:
        mutations = (
            ("records/programs/6529NM-AP-01/program.json", lambda record: record.pop("rules"), "rules"),
            ("records/programs/6529NM-AP-01/selected-works.json", lambda record: record["works"][0].update(unknown_field="reject"), "unknown_field"),
            ("records/programs/6529NM-AP-01/outcomes/OUT-001.json", lambda record: record.update(unknown_field="reject"), "unknown_field"),
        )
        for relative, mutate, expected in mutations:
            with self.subTest(relative=relative):
                temporary, root = self.make_repository_copy()
                self.addCleanup(temporary.cleanup)
                path = root / relative
                record = json.loads(path.read_text(encoding="utf-8"))
                mutate(record)
                self.refresh_review_hash(record)
                path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
                result = subprocess.run(
                    [sys.executable, str(root / "scripts" / "validate.py")],
                    cwd=root,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertNotEqual(0, result.returncode, result.stdout + result.stderr)
                self.assertIn(expected, result.stdout + result.stderr)

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
        paths = {entry["path"] for entry in manifest["entries"]}
        self.assertIn("docs/generative-trait-analysis.md", paths)
        self.assertIn("scripts/rarity/nextgen_compat.py", paths)
        self.assertIn("tests/rarity/test_nextgen_compat.py", paths)
        self.assertFalse(any("__pycache__" in path or path.endswith((".pyc", ".pyo")) for path in paths))
        self.assertNotIn("release-artifacts/latest/record-manifest.json", paths)
        self.assertRegex(manifest["manifest_commitment"]["digest"], r"^0x[0-9a-f]{64}$")
        self.assertRegex(manifest["manifest_sha256"], r"^sha256:[0-9a-f]{64}$")
        self.assertEqual(manifest, make_manifest(REPO_ROOT))

    def test_manifest_is_crlf_normalized_and_cache_free(self) -> None:
        temporary = tempfile.TemporaryDirectory(prefix="museum-manifest-normalization-")
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        docs = root / "docs"
        cache = root / "scripts" / "__pycache__"
        docs.mkdir(parents=True)
        cache.mkdir(parents=True)
        source = docs / "example.md"
        source.write_bytes(b"first\r\nsecond\rthird\n")
        (cache / "example.pyc").write_bytes(b"cache")
        self.assertEqual(b"first\nsecond\nthird\n", normalized_bytes(source))
        first = make_manifest(root)
        second = make_manifest(root)
        self.assertEqual(first, second)
        self.assertIn("docs/example.md", {entry["path"] for entry in first["entries"]})
        self.assertNotIn("scripts/__pycache__/example.pyc", {entry["path"] for entry in first["entries"]})

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
