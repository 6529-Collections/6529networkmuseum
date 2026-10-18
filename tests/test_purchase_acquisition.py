"""Purchase acquisition controls: authorization, register lot, title instrument, and proposal."""

from __future__ import annotations

import copy
import hashlib
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

TESTS_DIR = Path(__file__).resolve().parent
REPO_ROOT = TESTS_DIR.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from canonical import canonicalize  # noqa: E402
from validate import (  # noqa: E402
    keccak256,
    load_json,
    load_schemas,
    validate_acquisition_authorization,
    validate_event_history,
    validate_public_payload,
    validate_records,
    validator_for,
)

VALID_FIXTURES = TESTS_DIR / "fixtures" / "valid"
PURCHASE_FIXTURES = TESTS_DIR / "fixtures" / "purchase"
AQA_SCHEMA_ID = "0x00686e3e460412351a57431a74bd46252c84df12db5df0715748d46b7404e5a1"
AQA_SCHEMA_URI = "https://6529networkmuseum.org/schemas/acquisition-authorization-v1.json"
ACCESSION_SCHEMA_URI = "https://6529networkmuseum.org/schemas/accession-v1.json"
PUBLIC_ENTITY_SCHEMA_URI = "https://6529networkmuseum.org/schemas/public-entity-v1.json"
PURCHASE_ENVELOPE_FIXTURES = ("accession-lot.json", "accession.json", "object-record.json", "acquisition-authorization.json")


def load_fixture(name: str) -> dict:
    return json.loads((PURCHASE_FIXTURES / name).read_text(encoding="utf-8"))


def reseal(record: dict) -> dict:
    payload = record["payload"]
    without = {key: value for key, value in payload.items() if key != "payload_sha256"}
    payload["payload_sha256"] = "sha256:" + hashlib.sha256(canonicalize(without)).hexdigest()
    record["envelope"]["contentHash"]["digest"] = "0x" + keccak256(canonicalize(payload)).hex()
    return record


class PurchaseAcquisitionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.vocabularies, _envelope, cls.store = load_schemas(REPO_ROOT)
        cls.identity_inventory = load_json(REPO_ROOT / "schemas/public-entity-identity-inventory.json")

    def schema_errors(self, schema_uri: str, instance: object) -> list[str]:
        validator = validator_for(self.store[schema_uri], self.store)
        return [error.message for error in validator.iter_errors(instance)]

    def make_purchase_chain(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temporary = tempfile.TemporaryDirectory(prefix="museum-purchase-chain-")
        records = Path(temporary.name) / "records"
        records.mkdir()
        for fixture in VALID_FIXTURES.glob("*.json"):
            shutil.copy2(fixture, records / fixture.name)
        for name in PURCHASE_ENVELOPE_FIXTURES:
            shutil.copy2(PURCHASE_FIXTURES / name, records / name)
        return temporary, records

    def aqa(self) -> dict:
        return load_fixture("acquisition-authorization.json")["payload"]

    # Vocabulary and schema identity

    def test_acquisition_authorization_is_a_registered_museum_local_type(self) -> None:
        literal_id = "0x" + keccak256(b"MUSEUM_ACQUISITION_AUTHORIZATION_V1").hex()
        self.assertEqual(AQA_SCHEMA_ID, literal_id)
        self.assertIn("ACQUISITION_AUTHORIZATION", self.vocabularies["record_types"])
        self.assertEqual(literal_id, self.vocabularies["schema_ids"]["ACQUISITION_AUTHORIZATION"])
        self.assertEqual("acquisition-authorization.schema.json", self.vocabularies["schema_paths"]["ACQUISITION_AUTHORIZATION"])
        schema = load_json(REPO_ROOT / "schemas/acquisition-authorization.schema.json")
        self.assertEqual(AQA_SCHEMA_URI, schema["$id"])
        self.assertEqual(literal_id, schema["allOf"][1]["properties"]["schema_id"]["const"])
        self.assertEqual(
            "0x" + keccak256(b"MUSEUM_GIFT_ACCEPTANCE_AUTHORIZATION_V1").hex(),
            self.vocabularies["schema_ids"]["GIFT_ACCEPTANCE_AUTHORIZATION"],
        )

    # Complete purchase chain

    def test_purchase_fixture_chain_validates(self) -> None:
        temporary, _records = self.make_purchase_chain()
        self.addCleanup(temporary.cleanup)
        self.assertEqual([], validate_records(Path(temporary.name)))

    def test_purchase_chain_rejects_unresolved_authorization_and_gift_credit(self) -> None:
        temporary, records = self.make_purchase_chain()
        self.addCleanup(temporary.cleanup)
        (records / "acquisition-authorization.json").unlink()
        issues = validate_records(Path(temporary.name))
        self.assertTrue(any("unresolved record reference 6529NM.2026.001.AQA-01" in issue for issue in issues), issues)

        temporary, records = self.make_purchase_chain()
        self.addCleanup(temporary.cleanup)
        record = load_fixture("acquisition-authorization.json")
        record["payload"]["public_credit"] = "Gift of the contributors"
        (records / "acquisition-authorization.json").write_text(json.dumps(reseal(record), indent=2) + "\n", encoding="utf-8")
        issues = validate_records(Path(temporary.name))
        self.assertTrue(any("public_credit must describe a purchase" in issue for issue in issues), issues)

    # ACQUISITION_AUTHORIZATION schema

    def test_acquisition_authorization_fixture_passes_schema_and_validator(self) -> None:
        payload = self.aqa()
        self.assertEqual([], self.schema_errors(AQA_SCHEMA_URI, payload))
        self.assertEqual([], validate_acquisition_authorization(payload))

    def test_acquisition_authorization_schema_rejects_gift_and_unsafe_shapes(self) -> None:
        def set_path(payload: dict, path: tuple, value: object) -> None:
            target = payload
            for key in path[:-1]:
                target = target[key]
            if value is KeyError:
                del target[path[-1]]
            else:
                target[path[-1]] = value

        mutations = {
            "donation method": (("acquisition_method",), "donation"),
            "gift consideration": (("consideration", "status"), "none"),
            "integer amount": (("consideration", "amount_wei"), 458999999900000000),
            "leading zero amount": (("consideration", "amount_wei"), "0458999999900000000"),
            "named seller": (("seller", "name"), "Example Seller"),
            "missing token selection": (("token_selection",), KeyError),
            "missing limitations": (("program_authorization_limitations",), []),
            "gift authorization id": (("authorization_id",), "6529NM.2026.001.GAA-01"),
            "contributor interest": (("funding_basis", "contributor_ownership_interest"), "fractional"),
            "checksummed agent": (("executing_agent", "address"), "0xAbCdEf0000000000000000000000000000000000"),
            "donor credit field": (("donor_public_credit",), "Gift of the contributors"),
            "missing payment": (("consideration", "payment_transaction"), KeyError),
            "unknown funding kind": (("funding_basis", "kind"), "fractional_ownership_pool"),
        }
        for label, (path, value) in mutations.items():
            with self.subTest(label=label):
                payload = copy.deepcopy(self.aqa())
                set_path(payload, path, value)
                self.assertTrue(self.schema_errors(AQA_SCHEMA_URI, payload), label)

    def test_acquisition_authorization_cross_field_invariants_fail_closed(self) -> None:
        def mutate(change):
            payload = copy.deepcopy(self.aqa())
            change(payload)
            return validate_acquisition_authorization(payload)

        def duplicate_asset(payload: dict) -> None:
            payload["assets"].append(copy.deepcopy(payload["assets"][0]))

        cases = (
            ("duplicate asset", duplicate_asset, "duplicate object_id"),
            ("receipt log coverage", lambda p: p["custody_receipts"][0]["logs"][0].__setitem__("log_index", 9), "logs must exactly cover assets"),
            ("receipt transfer count", lambda p: p["custody_receipts"][0].__setitem__("transfer_count", 2), "transfer counts must equal assets.length"),
            ("payment value", lambda p: p["consideration"]["payment_transaction"].__setitem__("value_wei", "1"), "value_wei must equal consideration.amount_wei"),
            ("zero amount", lambda p: (p["consideration"].__setitem__("amount_wei", "0"), p["consideration"]["payment_transaction"].__setitem__("value_wei", "0")), "amount_wei must be positive"),
            ("payer", lambda p: p["consideration"]["payment_transaction"].__setitem__("from", "0x" + "6" * 40), "payment_transaction.from must equal executing_agent.address"),
            ("seller log", lambda p: p["consideration"]["payment_transaction"]["transfer_logs"][0].__setitem__("from", "0x" + "6" * 40), "transfer_logs[0].from must equal seller.address"),
            ("agent log", lambda p: p["consideration"]["payment_transaction"]["transfer_logs"][0].__setitem__("to", "0x" + "6" * 40), "transfer_logs[0].to must equal executing_agent.address"),
            ("transfer log coverage", lambda p: p["consideration"]["payment_transaction"]["transfer_logs"][0].__setitem__("object_id", "6529NM.2026.001.2"), "transfer_logs must cover every asset exactly once"),
            ("receipt sender", lambda p: p["custody_receipts"][0].__setitem__("from", "0x" + "3" * 40), "custody_receipts[0].from must equal executing_agent.address"),
            ("receipt recipient", lambda p: p["custody_receipts"][0].__setitem__("to", "0x" + "4" * 40), "custody_receipts[0].to must be the Museum"),
            ("single transaction", lambda p: p["custody_receipts"][0].__setitem__("transaction_hash", p["consideration"]["payment_transaction"]["transaction_hash"]), "payment and Museum receipt must be separate transactions"),
            ("receipt before payment", lambda p: p["custody_receipts"][0].__setitem__("block_number", 1), "custody receipt must not precede the payment"),
            ("seller is agent", lambda p: p["seller"].__setitem__("address", p["executing_agent"]["address"]), "seller.address must differ from executing_agent.address"),
            ("agent authority", lambda p: p["executing_agent"].__setitem__("authority_source", "6529NM-GOV-9999999"), "authority_source must name a governing_basis decision or record"),
            ("wave basis", lambda p: p["governing_basis"][0].__setitem__("live_api_status", "PARTICIPATORY"), "adopted WINNER Wave decision"),
            ("acceptance date", lambda p: p.__setitem__("formal_acceptance_date", "2026-08-02T00:00:00Z"), "formal_acceptance_date must equal"),
            ("completion boundary", lambda p: p["completion_boundary"].__setitem__("title_binding", "pending"), "accessioned completion_boundary requires"),
            ("gift credit", lambda p: p.__setitem__("public_credit", "Gift of the contributors"), "public_credit must describe a purchase"),
            ("donated credit", lambda p: p.__setitem__("public_credit", "Donated by Wave voters"), "public_credit must describe a purchase"),
        )
        for label, change, expected in cases:
            with self.subTest(label=label):
                issues = mutate(change)
                self.assertTrue(any(expected in issue for issue in issues), (label, issues))

    def test_gift_authorization_records_are_outside_the_purchase_validator(self) -> None:
        for lot in ("6529NM.2026.001", "6529NM.2026.002", "6529NM.2026.003"):
            payload = load_json(REPO_ROOT / f"records/accessions/{lot}/gift-acceptance-authorization.json")["payload"]
            self.assertEqual([], validate_acquisition_authorization(payload))
            self.assertTrue(self.schema_errors(AQA_SCHEMA_URI, payload))

    # Title instrument

    def test_purchase_title_instrument_is_bound_to_purchase_method(self) -> None:
        payload = load_fixture("accession.json")["payload"]
        self.assertEqual([], self.schema_errors(ACCESSION_SCHEMA_URI, payload))
        self.assertEqual([], validate_event_history(payload))

        gift_kind = copy.deepcopy(payload)
        gift_kind["events"][3]["instrument"]["kind"] = "institutional_gift_title_declaration"
        self.assertTrue(any("requires acquisition_method donation" in issue for issue in validate_event_history(gift_kind)))

        donation = copy.deepcopy(payload)
        donation["acquisition_method"] = "donation"
        self.assertTrue(any("requires acquisition_method purchase" in issue for issue in validate_event_history(donation)))

        unknown = copy.deepcopy(payload)
        unknown["events"][3]["instrument"]["kind"] = "bill_of_sale_unverified"
        self.assertTrue(self.schema_errors(ACCESSION_SCHEMA_URI, unknown))
        self.assertTrue(any("supported title instrument" in issue for issue in validate_event_history(unknown)))

        generic = copy.deepcopy(payload)
        generic["events"][3]["instrument"]["kind"] = "off_chain_instrument"
        self.assertEqual([], validate_event_history(generic))

    def test_published_gift_certificates_keep_their_title_instrument(self) -> None:
        for lot in ("6529NM.2026.001", "6529NM.2026.002", "6529NM.2026.003"):
            payload = load_json(REPO_ROOT / f"records/accessions/{lot}/accession-certificate.json")["payload"]
            self.assertEqual("donation", payload["acquisition_method"])
            self.assertEqual([], validate_event_history(payload))

    # Public graph: purchase Curated Acquisition

    def purchase_curated_acquisition(self) -> dict:
        payload = copy.deepcopy(load_json(REPO_ROOT / "records/entities/6529NM-CA-2026-004.json")["payload"])
        profile = payload["profile"]
        profile["acquisition_method"] = "purchase"
        profile["program_or_pathway"] = {"kind": "museum_wave_proposal", "entity_ids": [], "source_record_ids": ["6529NM.2026.003.GAA-01"]}
        profile["public_credit"] = "Acquired through a community-funded purchase authorized by the 6529 Network Museum Wave, 2026"
        profile["independent_acquisition_facts"]["payment"]["status"] = "verified"
        return payload

    def test_purchase_curated_acquisition_needs_no_gift_program_or_gift_credit(self) -> None:
        payload = self.purchase_curated_acquisition()
        self.assertEqual([], self.schema_errors(PUBLIC_ENTITY_SCHEMA_URI, payload))
        self.assertEqual([], validate_public_payload(payload, self.vocabularies, self.identity_inventory))
        self.assertEqual(["accessioned"], [item["source_status"] for item in payload["profile"]["lifecycle_observations"]])

        gift_credit = copy.deepcopy(payload)
        gift_credit["profile"]["public_credit"] = "Gift of the contributors"
        self.assertTrue(
            any("purchase Curated Acquisition public_credit" in issue for issue in validate_public_payload(gift_credit, self.vocabularies, self.identity_inventory))
        )

    def test_accessioned_purchase_does_not_require_a_wave_status_observation(self) -> None:
        payload = self.purchase_curated_acquisition()
        issues = validate_public_payload(payload, self.vocabularies, self.identity_inventory)
        self.assertFalse(any("WINNER" in issue for issue in issues), issues)
        winner = copy.deepcopy(payload)
        winner["profile"]["lifecycle_observations"][0]["source_status"] = "WINNER"
        self.assertTrue(
            any("governed WINNER observation record ID" in issue for issue in validate_public_payload(winner, self.vocabularies, self.identity_inventory))
        )


if __name__ == "__main__":
    unittest.main()
