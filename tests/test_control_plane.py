from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import struct
import subprocess
import sys
import tempfile
import unittest
import zlib
from datetime import UTC, datetime, timedelta
from pathlib import Path
from unittest.mock import patch

TESTS_DIR = Path(__file__).resolve().parent
REPO_ROOT = TESTS_DIR.parent
sys.path.append(str(REPO_ROOT / "scripts"))

from canonical import canonicalize  # noqa: E402
import bootstrap_validate  # noqa: E402
from check_fetch_guard import scan_file, scan_tree  # noqa: E402
from generate_manifest import (  # noqa: E402
    DuplicateJsonKeyError as ManifestDuplicateJsonKeyError,
    INVENTORY_FILES,
    INVENTORY_ROOTS,
    ManifestUnsafePathError,
    make_manifest,
    normalized_bytes,
)
from safe_fetch import SAFE_FETCH_POLICY, SAFE_FETCH_POLICY_JSON, FetchPolicyError, SafeHTTPSFetcher, canonicalize_https_url  # noqa: E402
from validate import keccak256, load_schemas, validate_provenance_schedule, validate_records, validate_state_machine, validate_vocabularies, validator_for  # noqa: E402


VALID_FIXTURES = TESTS_DIR / "fixtures" / "valid"
ONCHAIN_CONFORMANCE_HARNESSES = (
    "uri_safety_vectors_v1.py",
    "batch_vector_check_v1.py",
    "batch_gas_gate_check_v1.py",
    "https_expiry_renewal_check_v1.py",
    "stream_mirror_link_check_v1.py",
    "release_attestor_policy_check_v1.py",
    "target_release_signature_bundle_check_v1.py",
    "target_release_evidence_check_v1.py",
    "initial_authority_activation_check_v1.py",
    "manifest_abi_selector_check_v1.py",
)


class ControlPlaneTests(unittest.TestCase):
    def scaffold_manifest_root(self, root: Path) -> None:
        for directory in INVENTORY_ROOTS:
            (root / directory).mkdir(parents=True, exist_ok=True)
        for filename in INVENTORY_FILES:
            path = root / filename
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(f"fixture for {filename}\n", encoding="utf-8")

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

    def test_public_inventory_schema_is_not_casey_lot_specific(self) -> None:
        _vocabularies, _envelope, store = load_schemas(REPO_ROOT)
        schema = json.loads((REPO_ROOT / "schemas/public-inventory.schema.json").read_text(encoding="utf-8"))
        validator = validator_for(schema, store)
        inventory = {
            "$schema": "../../../schemas/public-inventory.schema.json",
            "record_control": {
                "revision": 1,
                "record_status": "constructed",
                "constructor": {},
                "review": None,
            },
            "record_id": "6529NM-PUB-TEST",
            "record_type": "public_inventory",
            "accession_lot_id": "6529NM.TEST.001",
            "objects": [{"object_id": "6529NM.TEST.001.01"}],
        }
        self.assertEqual([], list(validator.iter_errors(inventory)))
        self.assertTrue(list(validator.iter_errors({**inventory, "objects": []})))
        self.assertTrue(list(validator.iter_errors({**inventory, "objects": [{}]})))

    def test_transaction_provenance_schema_is_generic_and_receipt_joins_are_enforced(self) -> None:
        _vocabularies, _envelope, store = load_schemas(REPO_ROOT)
        schema = json.loads((REPO_ROOT / "schemas/transaction-provenance.schema.json").read_text(encoding="utf-8"))
        validator = validator_for(schema, store)
        lot = json.loads((REPO_ROOT / "records/accessions/6529NM.2026.001/accession-statement.json").read_text(encoding="utf-8"))["payload"]
        schedule = json.loads(json.dumps(lot["provenance_schedule"]))
        schedule["$schema"] = "../../../schemas/transaction-provenance.schema.json"
        first = schedule["objects"][0]
        schedule["objects"] = [first]
        schedule["common_receipt"]["transfer_count"] = 1
        schedule["common_receipt"]["log_indices"] = {
            first["object_id"]: next(event["log"] for event in first["events"] if event["kind"] == "museum_receipt")
        }
        self.assertEqual([], list(validator.iter_errors(schedule)))
        self.assertEqual([], validate_provenance_schedule(schedule))
        mismatched_count = json.loads(json.dumps(schedule))
        mismatched_count["common_receipt"]["transfer_count"] = 2
        self.assertTrue(any("transfer_count" in issue for issue in validate_provenance_schedule(mismatched_count)))
        mismatched_log = json.loads(json.dumps(schedule))
        mismatched_log["common_receipt"]["log_indices"][first["object_id"]] += 1
        self.assertTrue(any("museum_receipt must equal" in issue for issue in validate_provenance_schedule(mismatched_log)))

    def test_unresolved_cross_reference_is_rejected(self) -> None:
        temporary, records = self.make_records_root()
        self.addCleanup(temporary.cleanup)
        record = self.load_record(records, "accession-lot.json")
        record["payload"]["object_ids"] = ["6529NM.2026.001.999"]
        self.save_record(records, "accession-lot.json", record)
        issues = validate_records(Path(temporary.name))
        self.assertTrue(any("unresolved record reference" in issue for issue in issues), issues)

    def test_direct_reference_self_cycle_is_rejected(self) -> None:
        temporary, records = self.make_records_root()
        self.addCleanup(temporary.cleanup)
        record = self.load_record(records, "accession-lot.json")
        record["payload"]["references"] = [record["payload"]["record_id"]]
        self.refresh_content_hash(record)
        self.save_record(records, "accession-lot.json", record)
        issues = validate_records(Path(temporary.name))
        self.assertTrue(any("references must not point to the record itself" in issue for issue in issues), issues)

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
        record["payload"]["events"][4]["custody_paths"][0]["kind"] = "non_token_off_chain"
        self.save_record(records, "accession.json", record)
        issues = validate_records(Path(temporary.name))
        self.assertTrue(any("ACCESSION.events must contain" in issue for issue in issues), issues)
        self.assertTrue(any("custody_path.kind must be onchain_token" in issue for issue in issues), issues)

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
                record["payload"]["events"][4]["custody_paths"][0][field] = value
                self.save_record(records, "accession.json", record)
                issues = validate_records(Path(temporary.name))
                self.assertTrue(any(f"custody_path.{field} must match" in issue for issue in issues), issues)

    def test_accession_binding_requirements_and_backwards_chronology_are_rejected(self) -> None:
        mutations = (
            (lambda record: record["payload"]["title_bindings"][0].update(status="pending"), "executed title binding"),
            (lambda record: record["payload"]["events"][3]["instrument"].update(sha256="sha256:" + "d" * 64), "instrument sha256"),
            (lambda record: record["payload"]["events"][1].update(occurred_at="2024-12-31T23:59:59Z"), "moves backwards"),
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

    def test_accession_and_provenance_malformed_identity_projections_do_not_abort(self) -> None:
        temporary, records = self.make_records_root()
        self.addCleanup(temporary.cleanup)
        accession = self.load_record(records, "accession.json")
        accession["payload"]["object_ids"][0] = ["malformed"]
        accession["payload"]["events"][4]["custody_paths"][0]["object_id"] = ["malformed"]
        self.save_record(records, "accession.json", accession)
        issues = validate_records(Path(temporary.name))
        self.assertTrue(any("ACCESSION custody_path must identify exactly one executed title binding by object_id" in issue for issue in issues), issues)

        schedule = json.loads(
            (REPO_ROOT / "records" / "accessions" / "6529NM.2026.001" / "accession-statement.json").read_text(encoding="utf-8")
        )["payload"]["provenance_schedule"]
        schedule["objects"][0]["object_id"] = ["malformed"]
        schedule["objects"][1]["object_id"] = ["malformed"]
        next(event for event in schedule["objects"][0]["events"] if event.get("kind") == "museum_receipt")["log"] = ["malformed"]
        next(event for event in schedule["objects"][1]["events"] if event.get("kind") == "museum_receipt")["log"] = ["malformed"]
        provenance_issues = validate_provenance_schedule(schedule)
        self.assertTrue(any("duplicate object_id" in issue for issue in provenance_issues), provenance_issues)
        self.assertTrue(any("log indices must be unique" in issue for issue in provenance_issues), provenance_issues)

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

    def test_rights_and_condition_event_lineage_is_unique_and_resolvable(self) -> None:
        temporary, records = self.make_records_root()
        self.addCleanup(temporary.cleanup)
        rights = self.load_record(records, "rights-statement.json")
        first = rights["payload"]["events"][0]
        rights["payload"]["events"].append(
            {
                "event_id": first["event_id"],
                "event_type": "rights_amendment",
                "occurred_at": "2026-08-02T00:00:00Z",
                "supersedes_event_id": "missing-rights-event",
                "authority_reference": "rights-holder:example-artist",
                "evidence_refs": first["evidence_refs"],
            }
        )
        self.save_record(records, "rights-statement.json", rights)

        condition = self.load_record(records, "condition-report.json")
        condition["payload"]["events"][0].pop("event_id")
        self.save_record(records, "condition-report.json", condition)
        issues = validate_records(Path(temporary.name))
        self.assertTrue(any("RIGHTS_STATEMENT.events[1]: event_id must be unique" in issue for issue in issues), issues)
        self.assertTrue(any("RIGHTS_STATEMENT.events[1]: supersedes_event_id must identify a unique earlier event" in issue for issue in issues), issues)
        self.assertTrue(any("CONDITION_REPORT.events[0]: event_id is required" in issue for issue in issues), issues)

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
            SAFE_FETCH_POLICY_JSON,
            vocabularies["endpoint_policy"],
        )
        mutated = dict(vocabularies)
        mutated["endpoint_policy"] = {**vocabularies["endpoint_policy"], "recheck_every_redirect": False}
        self.assertTrue(any("endpoint_policy" in issue for issue in validate_vocabularies(mutated)))

    def test_reviewbot_config_matches_deployed_compatibility_catalog(self) -> None:
        catalog = json.loads((TESTS_DIR / "fixtures/6529bot-production-catalog.json").read_text(encoding="utf-8"))
        config = (REPO_ROOT / ".github/6529bot.yml").read_text(encoding="utf-8")
        match = re.search(r"(?m)^\s+allowed:\s*\[([^\]]+)\]", config)
        self.assertIsNotNone(match)
        configured = {item.strip() for item in match.group(1).split(",")}
        supported = set(catalog["supported_repository_review_kinds"])
        self.assertEqual(supported, configured)
        self.assertNotIn("stream-contracts", configured)
        self.assertEqual(["stream-contracts"], catalog["temporarily_unsupported_repository_review_kinds"])
        governance = (REPO_ROOT / "governance/github-repository-governance.md").read_text(encoding="utf-8")
        self.assertIn("automatic production-compatible baseline is exactly", governance)
        self.assertIn("These specialists are not automatic baseline coverage", governance)
        self.assertIn("central head-bound `review-job.yml` workflow", governance)

    def make_mock_fetcher(self, answers: dict[str, list[str]], responses: dict[str, tuple[int, dict[str, str], bytes, str | None]], clock=None):
        connections = []

        class MockResponse:
            def __init__(self, status: int, headers: dict[str, str] | list[tuple[str, str]], body: bytes) -> None:
                self.status = status
                self.headers = headers
                self.body = body
                self.offset = 0

            def read(self, limit: int) -> bytes:
                chunk = self.body[self.offset : self.offset + limit]
                self.offset += len(chunk)
                return chunk

        class MockConnection:
            def __init__(self, response: MockResponse, peer_ip: str) -> None:
                self.response = response
                self.peer_ip = peer_ip
                self.requests = []
                self.closed = False

            def request(self, method: str, target: str, headers: dict[str, str], body: bytes | None = None) -> MockResponse:
                self.requests.append((method, target, headers, body))
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

    def test_safe_fetch_rejects_unicode_ambiguous_hosts_before_resolution(self) -> None:
        resolver_calls: list[str] = []

        def resolver(hostname: str, _port: int) -> list[str]:
            resolver_calls.append(hostname)
            return ["93.184.216.34"]

        fetcher = SafeHTTPSFetcher(resolver=resolver, connection_factory=lambda *_args: None)
        for url in (
            "https://127.0.0。1/private",
            "https://127.0.0.1。nip.io/private",
            "https://127.0.0．1/private",
            "https://local\u3002host/private",
            "https://localhost/private",
            "https://metadata/private",
            "https://[::ffff:127.0.0.1]/private",
        ):
            with self.subTest(url=url):
                with self.assertRaises(FetchPolicyError):
                    fetcher.fetch(url)
        self.assertEqual([], resolver_calls)

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

    def test_safe_fetch_rejects_ambiguous_response_framing_and_headers(self) -> None:
        bad_response_headers = (
            [("Content-Length", "2"), ("Content-Length", "2")],
            [("Content-Length", "02")],
            [("Content-Length", "+2")],
            [("Content-Length", "-1")],
            [("Content-Length", "3")],
            [("Transfer-Encoding", "chunked")],
            [("Content-Length", "2"), ("Transfer-Encoding", "chunked")],
            [("Content-Encoding", "gzip"), ("Content-Length", "2")],
        )
        for response_headers in bad_response_headers:
            with self.subTest(response_headers=response_headers):
                fetcher, _connections = self.make_mock_fetcher(
                    {"good.example.test": ["93.184.216.34"]},
                    {"good.example.test": (200, response_headers, b"ok", None)},
                )
                with self.assertRaises(FetchPolicyError):
                    fetcher.fetch("https://good.example.test/data")

        fetcher, _connections = self.make_mock_fetcher(
            {"good.example.test": ["93.184.216.34"]},
            {"good.example.test": (200, [("Content-Length", "2")], b"not-ok", None)},
        )
        with self.assertRaises(FetchPolicyError):
            fetcher.fetch("https://good.example.test/data")

        fetcher, _connections = self.make_mock_fetcher(
            {"good.example.test": ["93.184.216.34"]},
            {"good.example.test": (200, [("Content-Length", "2")], b"ok", None)},
        )
        for headers in (
            {"X-Api-Key": "synthetic"},
            {"X-Auth-Token": "synthetic"},
            {"Forwarded": "for=127.0.0.1"},
            {"Host": "evil.example"},
            {"Content-Length": "2"},
            {"Accept": "text/plain\r\nX-Injected: yes"},
            {"Accept": "text/plain", "accept": "application/json"},
        ):
            with self.subTest(headers=headers):
                with self.assertRaises(FetchPolicyError):
                    fetcher.fetch("https://good.example.test/data", headers=headers)
        result = fetcher.fetch("https://good.example.test/data", headers={"Accept": "image/png", "User-Agent": "Museum/1"})
        self.assertEqual(2, result.observation.byte_length)

        request_body = b'{"jsonrpc":"2.0"}'
        result = fetcher.fetch(
            "https://good.example.test/data",
            method="POST",
            body=request_body,
            headers={"Accept": "application/json", "Content-Type": "application/json", "User-Agent": "Museum/1"},
        )
        self.assertEqual(2, result.observation.byte_length)
        self.assertEqual(request_body, _connections[-1][1].requests[-1][3])
        self.assertEqual(str(len(request_body)), _connections[-1][1].requests[-1][2]["Content-Length"])

    def test_safe_fetch_policy_is_deep_frozen_and_caller_owned(self) -> None:
        caller_policy = {key: list(value) if isinstance(value, list) else value for key, value in SAFE_FETCH_POLICY_JSON.items()}
        fetcher, _connections = self.make_mock_fetcher(
            {"good.example.test": ["93.184.216.34"]},
            {"good.example.test": (200, {"Content-Length": "2"}, b"ok", None)},
        )
        fetcher = SafeHTTPSFetcher(
            resolver=fetcher.resolver,
            connection_factory=fetcher.connection_factory,
            clock=fetcher.clock,
            policy=caller_policy,
        )
        caller_policy["max_response_bytes"] = 1
        caller_policy["max_request_bytes"] = 1
        self.assertEqual(1_048_576, fetcher.policy["max_response_bytes"])
        self.assertEqual(1_048_576, fetcher.policy["max_request_bytes"])
        self.assertNotEqual(caller_policy, fetcher.policy)
        with self.assertRaises((TypeError, AttributeError)):
            fetcher.policy["max_response_bytes"] = 1  # type: ignore[index]
        with self.assertRaises(FetchPolicyError):
            fetcher.fetch("https://good.example.test/data", method="POST")

        fetcher, _connections = self.make_mock_fetcher(
            {"good.example.test": ["93.184.216.34"]},
            {"good.example.test": (200, {"Content-Length": "2"}, b"ok", None)},
        )
        fixed = datetime(2026, 8, 1, tzinfo=UTC)
        with self.assertRaises(FetchPolicyError):
            fetcher.fetch("https://good.example.test/data", expires_at=fixed - timedelta(seconds=1))
        result = fetcher.fetch("https://good.example.test/data", method="POST", body=b"{}", headers={"Content-Type": "application/json"})
        self.assertEqual(b"ok", result.body)
        with self.assertRaises(FetchPolicyError):
            fetcher.fetch("https://good.example.test/data", method="POST", body=b"{}", headers={"Content-Type": "text/plain"})
        with self.assertRaises(FetchPolicyError):
            fetcher.fetch("https://good.example.test/data", method="GET", body=b"{}")
        with self.assertRaises(FetchPolicyError):
            fetcher.fetch(
                "https://good.example.test/data",
                method="POST",
                body=b"x" * (int(SAFE_FETCH_POLICY["max_request_bytes"]) + 1),
                headers={"Content-Type": "application/json"},
            )
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
        bad_sources = {
            "requests_alias.py": "import requests as rq\nrq.get('https://example.test')\n",
            "urllib_from_import.py": "from urllib.request import urlopen as open_url\nopen_url('https://example.test')\n",
            "socket_alias.py": "import socket as sock\nsock.create_connection(('example.test', 443))\n",
            "http_from_import.py": "from http.client import HTTPSConnection as Client\nClient('example.test')\n",
            "dynamic_import.py": "import importlib\nimportlib.import_module('httpx')\n",
            "dunder_import.py": "__import__('requests')\n",
            "subprocess_curl.py": "import subprocess\nsubprocess.run(['curl', 'https://example.test'])\n",
            "subprocess_alias.py": "from subprocess import Popen as launch\nlaunch(['wget', 'https://example.test'])\n",
            "os_shell.py": "import os as operating\noperating.system('powershell Invoke-WebRequest https://example.test')\n",
            "getattr_subprocess.py": "import subprocess as sp\ngetattr(sp, 'Popen')(['curl', 'https://example.test'])\n",
            "getattr_os.py": "import os as operating\ngetattr(operating, 'system')('wget https://example.test')\n",
            "getattr_importlib.py": "import importlib as loader\ngetattr(loader, 'import_module')('requests')\n",
        }
        for filename, source in bad_sources.items():
            with self.subTest(filename=filename):
                bad = root / filename
                bad.write_text(source, encoding="utf-8")
                self.assertTrue(scan_file(bad, root), filename)

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

    def test_amendment_history_is_complete_timezone_aware_and_chronological(self) -> None:
        temporary = tempfile.TemporaryDirectory(prefix="museum-amendment-chronology-")
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        path = root / "records" / "accessions" / "register.json"
        path.parent.mkdir(parents=True)
        source = REPO_ROOT / "records" / "accessions" / "register.json"
        cases = (
            ("current revision predates supersession", "current revision predates its latest supersession", lambda record: record["record_control"]["constructor"].__setitem__("constructed_at", "2026-08-01T22:55:00Z")),
            ("history missing", "revision requires a complete amendment history", lambda record: record.pop("amendment_history")),
            ("history empty", "revision requires a complete amendment history", lambda record: record.__setitem__("amendment_history", [])),
            ("timezone missing", "timezone-less revision 1 supersession timestamp", lambda record: record["amendment_history"][0].__setitem__("superseded_at", "2026-08-01T22:55:00")),
            ("supersession timestamps reversed", "supersession timestamps must be ordered by revision", lambda record: (
                record["amendment_history"][0].__setitem__("superseded_at", "2026-08-02T06:30:00Z"),
                record["amendment_history"][1].__setitem__("superseded_at", "2026-08-01T22:55:00Z"),
            )),
        )
        def raise_failure(message: str) -> None:
            raise ValueError(message)

        for label, expected, mutate in cases:
            with self.subTest(label=label):
                record = json.loads(source.read_text(encoding="utf-8"))
                mutate(record)
                record["record_control"]["review"]["payload_sha256"] = bootstrap_validate.canonical_payload_hash(record)
                path.write_text(json.dumps(record), encoding="utf-8")
                with patch.object(bootstrap_validate, "ROOT", root), patch.object(bootstrap_validate, "fail", side_effect=raise_failure):
                    with self.assertRaisesRegex(ValueError, expected):
                        bootstrap_validate.check_record_controls({path: record})

    @staticmethod
    def make_png(extra: bytes = b"") -> bytes:
        def chunk(kind: bytes, data: bytes) -> bytes:
            return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)

        chunks = [chunk(b"IHDR", struct.pack(">IIBBBBB", 1, 1, 8, 2, 0, 0, 0))]
        if extra:
            chunks.append(chunk(b"tEXt", b"note\x00" + extra))
        chunks.extend(
            [
                chunk(b"IDAT", zlib.compress(b"\x00\xff\xff\xff")),
                chunk(b"IEND", b""),
            ]
        )
        return b"\x89PNG\r\n\x1a\n" + b"".join(chunks)

    def test_manifest_authorized_binary_evidence_is_checked_before_text_decode(self) -> None:
        temporary = tempfile.TemporaryDirectory(prefix="museum-binary-evidence-")
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        evidence = root / "evidence"
        evidence.mkdir()
        binary = self.make_png()
        image = evidence / "image.png"
        image.write_bytes(binary)
        manifest = evidence / "manifest.json"

        def write_manifest(payload: bytes) -> None:
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

        write_manifest(binary)
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
            b"-----BEGIN DSA PRIVATE KEY-----",
            b"-----BEGIN PGP PRIVATE KEY BLOCK-----",
            b"eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxIn0.signature",
        )
        for credential in credential_shapes:
            with self.subTest(credential=credential[:12]):
                payload = self.make_png(credential)
                write_manifest(payload)
                with patch.object(bootstrap_validate, "ROOT", root):
                    entries = bootstrap_validate.check_evidence_manifests({manifest: json.loads(manifest.read_text(encoding="utf-8"))})
                    with self.assertRaises(SystemExit):
                        bootstrap_validate.check_public_record_safety(entries)

        for signature in (b"MZ", b"\x7fELF", b"#!/bin/sh\necho unsafe", b"PK\x03\x04", b"<script>alert(1)</script>"):
            with self.subTest(signature=signature[:8]):
                payload = binary + signature
                write_manifest(payload)
                with patch.object(bootstrap_validate, "ROOT", root):
                    entries = bootstrap_validate.check_evidence_manifests({manifest: json.loads(manifest.read_text(encoding="utf-8"))})
                    with self.assertRaises(SystemExit):
                        bootstrap_validate.check_public_record_safety(entries)

        for encoded in (
            "api_key=synthetic-secret-value".encode("utf-16-le"),
            "C:\\Users\\Administrator\\private.txt".encode("utf-16-be"),
        ):
            with self.subTest(encoded=encoded[:8]):
                payload = self.make_png(encoded)
                write_manifest(payload)
                with patch.object(bootstrap_validate, "ROOT", root):
                    entries = bootstrap_validate.check_evidence_manifests({manifest: json.loads(manifest.read_text(encoding="utf-8"))})
                    with self.assertRaises(SystemExit):
                        bootstrap_validate.check_public_record_safety(entries)

        for label in ("API_KEY", "CLIENT_SECRET", "PRIVATE_KEY", "PASSWORD"):
            for encoding in ("utf-16-le", "utf-16-be"):
                with self.subTest(label=label, encoding=encoding):
                    payload = self.make_png(f"{label}=SyntheticSecretValue".encode(encoding))
                    write_manifest(payload)
                    with patch.object(bootstrap_validate, "ROOT", root):
                        entries = bootstrap_validate.check_evidence_manifests({manifest: json.loads(manifest.read_text(encoding="utf-8"))})
                        with self.assertRaises(SystemExit):
                            bootstrap_validate.check_public_record_safety(entries)

        image.write_bytes(b"\xff\x00undeclared")
        manifest.unlink()
        with patch.object(bootstrap_validate, "ROOT", root):
            with self.assertRaises(SystemExit):
                bootstrap_validate.check_public_record_safety()

    def test_declared_nontext_binary_media_fails_closed_before_text_fallback(self) -> None:
        temporary = tempfile.TemporaryDirectory(prefix="museum-nontext-evidence-")
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        evidence = root / "evidence"
        evidence.mkdir()
        manifest = evidence / "manifest.json"
        payload = b"MZ\nPK\x03\x04\n#!/bin/sh\n<script>alert(1)</script>"
        for media_type in ("application/pdf", "application/octet-stream"):
            with self.subTest(media_type=media_type):
                target = evidence / "payload.dat"
                target.write_bytes(payload)
                manifest.write_text(
                    json.dumps(
                        {
                            "hash_algorithm": "sha256",
                            "byte_mode": "raw",
                            "entries": [
                                {
                                    "path": target.name,
                                    "byte_mode": "raw",
                                    "media_type": media_type,
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

    def test_unmanifested_ascii_polyglots_fail_closed_before_text_decode(self) -> None:
        temporary = tempfile.TemporaryDirectory(prefix="museum-unmanifested-polyglot-")
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        evidence = root / "evidence"
        evidence.mkdir()
        payloads = (
            b"MZ\nPK\x03\x04\n#!/bin/sh\n<script>alert(1)</script>",
            b"safe prefix\nPK\x03\x04\n#!/bin/sh\n<script>alert(1)</script>",
        )
        for index, payload in enumerate(payloads):
            for filename in (f"payload-{index}.txt", f"payload-{index}.dat"):
                with self.subTest(filename=filename):
                    for existing in evidence.iterdir():
                        existing.unlink()
                    (evidence / filename).write_bytes(payload)
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
        self.scaffold_manifest_root(manifest_root)
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
        self.assertEqual(
            [
                ".github",
                "policies",
                "records",
                "schemas",
                "docs",
                "governance",
                "specs",
                "templates",
                "scripts",
                "tests",
            ],
            manifest["inventory_roots"],
        )
        self.assertEqual(
            [".python-version", ".gitattributes", ".gitignore", "AGENTS.md", "INDEX.md", "README.md", "requirements-dev.txt"],
            manifest["inventory_files"],
        )
        self.assertTrue(all((REPO_ROOT / root).is_dir() for root in INVENTORY_ROOTS))
        self.assertTrue(all((REPO_ROOT / path).is_file() for path in INVENTORY_FILES))
        self.assertTrue(manifest["entries"])
        self.assertTrue(all("\\" not in entry["path"] for entry in manifest["entries"]))
        self.assertTrue(all(not entry["path"].startswith("evidence/") for entry in manifest["entries"]))
        entry_paths = [entry["path"] for entry in manifest["entries"]]
        self.assertEqual(sorted(entry_paths), entry_paths)
        self.assertEqual(len(entry_paths), len(set(entry_paths)))
        paths = set(entry_paths)
        self.assertIn("docs/generative-trait-analysis.md", paths)
        self.assertIn("governance/pull-request-review-policy.md", paths)
        self.assertIn("templates/object-record.md", paths)
        self.assertIn(".github/workflows/museum-validation.yml", paths)
        self.assertIn("specs/README.md", paths)
        self.assertIn("README.md", paths)
        self.assertIn("requirements-dev.txt", paths)
        self.assertIn("scripts/rarity/nextgen_compat.py", paths)
        self.assertIn("tests/rarity/test_nextgen_compat.py", paths)
        self.assertFalse(any("__pycache__" in path or path.endswith((".pyc", ".pyo")) for path in paths))
        self.assertNotIn("release-artifacts/latest/record-manifest.json", paths)
        self.assertFalse(any(path.startswith("notes/") for path in paths))
        self.assertRegex(manifest["manifest_commitment"]["digest"], r"^0x[0-9a-f]{64}$")
        self.assertRegex(manifest["manifest_sha256"], r"^sha256:[0-9a-f]{64}$")
        self.assertEqual(manifest, make_manifest(REPO_ROOT))

    def test_manifest_is_crlf_normalized_and_cache_free(self) -> None:
        temporary = tempfile.TemporaryDirectory(prefix="museum-manifest-normalization-")
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        self.scaffold_manifest_root(root)
        docs = root / "docs"
        specs = root / "specs"
        notes = root / "notes" / "wip"
        cache = root / "scripts" / "__pycache__"
        notes.mkdir(parents=True)
        cache.mkdir(parents=True)
        source = docs / "example.md"
        specification = specs / "protocol.md"
        source.write_bytes(b"first\r\nsecond\rthird\n")
        specification.write_bytes(b"governed\r\nspec\r")
        (notes / "working.md").write_text("not release authority\n", encoding="utf-8")
        (root / "README.md").write_bytes(b"first\r\nsecond\rthird\n")
        (cache / "example.pyc").write_bytes(b"cache")
        self.assertEqual(b"first\nsecond\nthird\n", normalized_bytes(source))
        self.assertEqual(b"governed\nspec\n", normalized_bytes(specification))
        first = make_manifest(root)
        second = make_manifest(root)
        self.assertEqual(first, second)
        paths = {entry["path"] for entry in first["entries"]}
        self.assertIn("docs/example.md", paths)
        self.assertIn("specs/protocol.md", paths)
        self.assertIn("README.md", paths)
        self.assertNotIn("notes/wip/working.md", paths)
        self.assertNotIn("scripts/__pycache__/example.pyc", paths)
        specification.write_text("changed specification\n", encoding="utf-8")
        changed = make_manifest(root)
        self.assertNotEqual(first["manifest_commitment"], changed["manifest_commitment"])
        self.assertNotEqual(first["manifest_sha256"], changed["manifest_sha256"])

    def test_manifest_rejects_file_and_directory_symlinks(self) -> None:
        temporary = tempfile.TemporaryDirectory(prefix="museum-manifest-links-")
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        self.scaffold_manifest_root(root)
        docs = root / "docs"
        (docs / "real.md").write_text("safe\n", encoding="utf-8")
        external = Path(temporary.name).parent / f"museum-manifest-external-{Path(temporary.name).name}.txt"
        external.write_text("outside\n", encoding="utf-8")
        self.addCleanup(lambda: external.unlink(missing_ok=True))
        try:
            os.symlink(external, docs / "file-link.md")
        except (OSError, NotImplementedError) as exc:
            if os.name == "nt":
                self.skipTest(f"Windows symlink privilege unavailable: {exc}")
            raise
        with self.assertRaises(ManifestUnsafePathError):
            make_manifest(root)

        (docs / "file-link.md").unlink()
        target_dir = root / "target-dir"
        target_dir.mkdir()
        (target_dir / "nested.md").write_text("nested\n", encoding="utf-8")
        try:
            os.symlink(target_dir, docs / "directory-link", target_is_directory=True)
        except (OSError, NotImplementedError) as exc:
            if os.name == "nt":
                self.skipTest(f"Windows directory symlink privilege unavailable: {exc}")
            raise
        with self.assertRaises(ManifestUnsafePathError):
            make_manifest(root)

    def test_manifest_rejects_root_file_symlink(self) -> None:
        temporary = tempfile.TemporaryDirectory(prefix="museum-manifest-root-link-")
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        self.scaffold_manifest_root(root)
        (root / "README.md").unlink()
        external = root.parent / f"museum-manifest-root-external-{root.name}.txt"
        external.write_text("outside\n", encoding="utf-8")
        self.addCleanup(lambda: external.unlink(missing_ok=True))
        try:
            os.symlink(external, root / "README.md")
        except (OSError, NotImplementedError) as exc:
            if os.name == "nt":
                self.skipTest(f"Windows symlink privilege unavailable: {exc}")
            raise
        with self.assertRaises(ManifestUnsafePathError):
            make_manifest(root)

    def test_manifest_rejects_missing_configured_root_and_file(self) -> None:
        temporary = tempfile.TemporaryDirectory(prefix="museum-manifest-missing-")
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        self.scaffold_manifest_root(root)

        (root / "AGENTS.md").unlink()
        with self.assertRaisesRegex(ManifestUnsafePathError, "configured governed file is missing"):
            make_manifest(root)

        (root / "AGENTS.md").write_text("restored\n", encoding="utf-8")
        shutil.rmtree(root / "templates")
        with self.assertRaisesRegex(ManifestUnsafePathError, "configured governed root is missing"):
            make_manifest(root)

        (root / "templates").write_text("not a directory\n", encoding="utf-8")
        with self.assertRaisesRegex(ManifestUnsafePathError, "configured governed root is not a directory"):
            make_manifest(root)

    @unittest.skipUnless(hasattr(os, "mkfifo"), "named pipes are not available on this platform")
    def test_manifest_rejects_nonregular_governed_directory_entry(self) -> None:
        temporary = tempfile.TemporaryDirectory(prefix="museum-manifest-nonregular-")
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        self.scaffold_manifest_root(root)
        pipe = root / "docs" / "named-pipe"
        os.mkfifo(pipe)
        with self.assertRaisesRegex(ManifestUnsafePathError, "not a regular file or directory"):
            make_manifest(root)

    def test_foundation_bootstrap_controls_pass_current_register(self) -> None:
        result = subprocess.run(
            [sys.executable, str(REPO_ROOT / "scripts" / "bootstrap_validate.py")],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_onchain_conformance_harnesses_pass(self) -> None:
        for name in ONCHAIN_CONFORMANCE_HARNESSES:
            with self.subTest(name=name):
                result = subprocess.run(
                    [sys.executable, "-B", str(REPO_ROOT / "specs" / "onchain" / name)],
                    cwd=REPO_ROOT,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_onchain_conformance_harnesses_reject_optimized_python(self) -> None:
        for name in ONCHAIN_CONFORMANCE_HARNESSES:
            with self.subTest(name=name):
                result = subprocess.run(
                    [sys.executable, "-O", "-B", str(REPO_ROOT / "specs" / "onchain" / name)],
                    cwd=REPO_ROOT,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertNotEqual(0, result.returncode, result.stdout + result.stderr)
                self.assertIn("optimized Python disables conformance checks", result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
