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
from proposed_gifts import proposed_gift_issues  # noqa: E402
from validate import (  # noqa: E402
    keccak256,
    load_json,
    load_schemas,
    validate_acquisition_authorization,
    validate_event_history,
    validate_proposed_acquisition_layout,
    validate_purchase_provenance_joins,
    validate_public_payload,
    validate_register_purchase_lots,
    validate_records,
    validator_for,
)

VALID_FIXTURES = TESTS_DIR / "fixtures" / "valid"
PURCHASE_FIXTURES = TESTS_DIR / "fixtures" / "purchase"
AQA_SCHEMA_ID = "0x00686e3e460412351a57431a74bd46252c84df12db5df0715748d46b7404e5a1"
AQA_SCHEMA_URI = "https://6529networkmuseum.org/schemas/acquisition-authorization-v1.json"
ACCESSION_SCHEMA_URI = "https://6529networkmuseum.org/schemas/accession-v1.json"
REGISTER_SCHEMA_URI = "https://6529.network/museum/schemas/accession-register/v1"
PROPOSAL_SCHEMA_URI = "https://6529.network/museum/schemas/proposed-acquisition/v1"
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
            "seller address": (("seller", "address"), "0x3333333333333333333333333333333333333333"),
            "seller without lot": (("seller", "provenance_record_id"), KeyError),
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
            ("seller log", lambda p: p["consideration"]["payment_transaction"]["transfer_logs"][0].__setitem__("from_party", "agent"), "transfer_logs[0].from_party must be the seller"),
            ("agent log", lambda p: p["consideration"]["payment_transaction"]["transfer_logs"][0].__setitem__("to", "0x" + "6" * 40), "transfer_logs[0].to must equal executing_agent.address"),
            ("transfer log coverage", lambda p: p["consideration"]["payment_transaction"]["transfer_logs"][0].__setitem__("object_id", "6529NM.2026.001.2"), "transfer_logs must cover every asset exactly once"),
            ("receipt sender", lambda p: p["custody_receipts"][0].__setitem__("from", "0x" + "3" * 40), "custody_receipts[0].from must equal executing_agent.address"),
            ("receipt recipient", lambda p: p["custody_receipts"][0].__setitem__("to", "0x" + "4" * 40), "custody_receipts[0].to must be the Museum"),
            ("single transaction", lambda p: p["custody_receipts"][0].__setitem__("transaction_hash", p["consideration"]["payment_transaction"]["transaction_hash"]), "payment and Museum receipt must be separate transactions"),
            ("receipt before payment", lambda p: p["custody_receipts"][0].__setitem__("block_number", 1), "custody receipt must not precede the payment"),
            ("seller lot", lambda p: p["seller"].__setitem__("provenance_record_id", "6529NM.2026.009"), "seller.provenance_record_id must equal subject_id"),
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

    def test_purchase_seller_is_joined_through_the_lot_provenance_schedule(self) -> None:
        aqa = self.aqa()
        lot = load_fixture("accession-lot.json")["payload"]

        def issues(change=None) -> list[str]:
            mutated_aqa, mutated_lot = copy.deepcopy(aqa), copy.deepcopy(lot)
            if change is not None:
                change(mutated_aqa, mutated_lot)
            return validate_purchase_provenance_joins([("aqa.json", mutated_aqa), ("lot.json", mutated_lot)])

        self.assertEqual([], issues())
        self.assertNotIn("address", aqa["seller"])
        self.assertTrue(all("from" not in log for log in aqa["consideration"]["payment_transaction"]["transfer_logs"]))

        def events(lot_payload: dict) -> list[dict]:
            return lot_payload["provenance_schedule"]["objects"][0]["events"]

        cases = (
            ("missing lot", lambda a, l: a["seller"].__setitem__("provenance_record_id", "6529NM.2026.009"), "provenance_schedule records the purchase"),
            ("missing schedule", lambda a, l: l.pop("provenance_schedule"), "provenance_schedule records the purchase"),
            ("missing purchase event", lambda a, l: events(l).pop(0), "must record the purchase transfer"),
            ("purchase to stranger", lambda a, l: events(l)[0].__setitem__("to", "0x" + "6" * 40), "must run to the executing agent"),
            ("seller is agent", lambda a, l: events(l)[0].__setitem__("from", a["executing_agent"]["address"]), "seller address distinct"),
            ("seller is museum", lambda a, l: events(l)[0].__setitem__("from", a["custody_receipts"][0]["to"]), "seller address distinct"),
            ("missing receipt event", lambda a, l: events(l).pop(1), "must record the Museum receipt"),
            ("receipt from stranger", lambda a, l: events(l)[1].__setitem__("from", "0x" + "6" * 40), "from the executing agent to Museum custody"),
            ("receipt before purchase", lambda a, l: events(l).reverse(), "purchase of 6529NM.2026.001.1 before its Museum receipt"),
        )
        for label, change, expected in cases:
            with self.subTest(label=label):
                found = issues(change)
                self.assertTrue(any(expected in issue for issue in found), (label, found))

    def test_custody_receipts_must_deliver_to_the_lot_custody_address(self) -> None:
        aqa = self.aqa()
        lot = load_fixture("accession-lot.json")["payload"]
        self.assertEqual([], validate_purchase_provenance_joins([("aqa.json", aqa), ("lot.json", lot)]))
        stranger = "0x" + "7" * 40
        mutated_aqa, mutated_lot = copy.deepcopy(aqa), copy.deepcopy(lot)
        # The schedule is changed to match, so only the custody binding can catch it.
        mutated_aqa["custody_receipts"][0]["to"] = stranger
        mutated_lot["provenance_schedule"]["objects"][0]["events"][1]["to"] = stranger
        found = validate_purchase_provenance_joins([("aqa.json", mutated_aqa), ("lot.json", mutated_lot)])
        self.assertTrue(any("must deliver to the lot's Museum custody address" in issue for issue in found), found)
        unnamed = copy.deepcopy(lot)
        unnamed["provenance_schedule"]["common_receipt"].pop("museum_custody_address")
        found = validate_purchase_provenance_joins([("aqa.json", aqa), ("lot.json", unnamed)])
        self.assertTrue(any("must name the Museum custody address" in issue for issue in found), found)

    def test_register_purchase_lot_must_agree_with_its_authorization(self) -> None:
        aqa = self.aqa()
        lot = copy.deepcopy(load_fixture("purchase-register-lot.json"))
        lot.update(
            accession_lot_id=aqa["seller"]["provenance_record_id"],
            acquisition_authorization_record=aqa["record_id"],
            accession_certificate_record="6529NM-ACC-2026-001",
        )

        def issues(change=None) -> list[str]:
            mutated = copy.deepcopy(lot)
            if change is not None:
                change(mutated)
            return validate_register_purchase_lots([("register.json", {"lots": [mutated]})], [("aqa.json", aqa)])

        self.assertEqual([], issues())
        cases = (
            ("unknown authorization", lambda l: l.__setitem__("acquisition_authorization_record", "6529NM.2026.001.AQA-02"), "must name an ACQUISITION_AUTHORIZATION"),
            ("other lot", lambda l: l.__setitem__("accession_lot_id", "6529NM.2026.009"), "name different accession lots"),
            ("object count", lambda l: l.__setitem__("object_count", 2), "object_count"),
            ("certificate", lambda l: l.__setitem__("accession_certificate_record", "6529NM-ACC-2026-009"), "accession certificate"),
            ("credit", lambda l: l.__setitem__("public_credit", "Acquired through a purchase, 2026"), "public_credit"),
            ("amount", lambda l: l["consideration_summary"].__setitem__("amount_wei", "1"), "consideration_summary.amount_wei"),
            ("payment", lambda l: l["consideration_summary"].__setitem__("payment_transaction", "0x" + "e" * 64), "payment_transaction"),
            ("receipt transaction", lambda l: l["receipt_event"].__setitem__("transaction_hash", "0x" + "c" * 64), "exactly one"),
            ("receipt block", lambda l: l["receipt_event"].__setitem__("block_number", 12345679), "receipt_event.block_number"),
            ("receipt log", lambda l: l["receipt_event"].__setitem__("log_index", 9), "receipt_event.log_index"),
            ("receipt recipient", lambda l: l["receipt_event"].__setitem__("to", "0x" + "7" * 40), "receipt_event.to"),
            ("custody", lambda l: l["custody"].__setitem__("address", "0x" + "7" * 40), "custody address"),
        )
        for label, change, expected in cases:
            with self.subTest(label=label):
                found = issues(change)
                self.assertTrue(any(expected in issue for issue in found), (label, found))
        gift = {key: value for key, value in lot.items() if key != "acquisition_method"}
        self.assertEqual([], validate_register_purchase_lots([("register.json", {"lots": [gift]})], []))

    def test_repository_purchase_lot_agrees_with_its_authorization(self) -> None:
        register = load_json(REPO_ROOT / "records/accessions/register.json")
        aqa = load_json(REPO_ROOT / "records/accessions/6529NM.2026.005/acquisition-authorization.json")["payload"]
        lot = load_json(REPO_ROOT / "records/accessions/6529NM.2026.005/accession-statement.json")["payload"]
        self.assertEqual([], validate_register_purchase_lots([("register.json", register)], [("aqa.json", aqa)]))
        self.assertEqual([], validate_purchase_provenance_joins([("aqa.json", aqa), ("lot.json", lot)]))

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

    # Accession register

    def test_register_gift_lots_are_unchanged_and_purchase_lot_validates(self) -> None:
        register = load_json(REPO_ROOT / "records/accessions/register.json")
        self.assertEqual([], self.schema_errors(REGISTER_SCHEMA_URI, register))
        purchase_lot = load_fixture("purchase-register-lot.json")
        with_purchase = copy.deepcopy(register)
        with_purchase["lots"].append(purchase_lot)
        self.assertEqual([], self.schema_errors(REGISTER_SCHEMA_URI, with_purchase))

        def lot_errors(lot: dict) -> list[str]:
            candidate = copy.deepcopy(register)
            candidate["lots"].append(lot)
            return self.schema_errors(REGISTER_SCHEMA_URI, candidate)

        invalid_purchase = {
            "donation status": {**purchase_lot, "donation_status": "formally_accepted"},
            "gift authorization": {**purchase_lot, "acquisition_authorization_record": "6529NM.2026.901.GAA-01"},
            "gift record field": {**purchase_lot, "gift_acceptance_authorization_record": "6529NM.2026.901.GAA-01"},
            "donor credit": {**purchase_lot, "donor_public_credit": "Gift of the contributors"},
            "gift credit": {**purchase_lot, "public_credit": "Gift of the contributors"},
            "donated credit": {**purchase_lot, "public_credit": "Donated by Wave voters"},
            "donation method": {**purchase_lot, "acquisition_method": "donation"},
            "integer amount": {**purchase_lot, "consideration_summary": {**purchase_lot["consideration_summary"], "amount_wei": 458999999900000000}},
            "no consideration": {key: value for key, value in purchase_lot.items() if key != "consideration_summary"},
            "no funding summary": {key: value for key, value in purchase_lot.items() if key != "funding_basis_summary"},
            "two receipt forms": {**purchase_lot, "receipt_events": [purchase_lot["receipt_event"]]},
        }
        for label, lot in invalid_purchase.items():
            with self.subTest(label=label):
                self.assertTrue(lot_errors(lot), label)

        gift_lot = next(lot for lot in register["lots"] if lot["accession_lot_id"] == "6529NM.2026.003")
        self.assertEqual("formally_accepted", gift_lot["donation_status"])
        purchase_lots = [lot for lot in register["lots"] if lot.get("acquisition_method") == "purchase"]
        self.assertEqual(["6529NM.2026.005"], [lot["accession_lot_id"] for lot in purchase_lots])
        invalid_gift = {
            "purchase authorization on gift": {**gift_lot, "acquisition_authorization_record": "6529NM.2026.003.AQA-01"},
            "purchase method on gift": {**gift_lot, "acquisition_method": "purchase"},
            "gift without donor credit": {key: value for key, value in gift_lot.items() if key != "donor_public_credit"},
        }
        for label, lot in invalid_gift.items():
            with self.subTest(label=label):
                self.assertTrue(lot_errors(lot), label)

    def test_accession_lot_accepts_only_an_acquisition_authorization_identifier(self) -> None:
        payload = load_fixture("accession-lot.json")["payload"]
        self.assertEqual([], self.schema_errors("https://6529networkmuseum.org/schemas/accession-lot-v1.json", payload))
        bad = copy.deepcopy(payload)
        bad["acquisition_authorization_record"] = "6529NM.2026.001.GAA-01"
        self.assertTrue(self.schema_errors("https://6529networkmuseum.org/schemas/accession-lot-v1.json", bad))

    # Proposed acquisitions

    def test_proposed_acquisition_schema(self) -> None:
        proposal = load_fixture("proposed-acquisition.json")
        self.assertEqual([], self.schema_errors(PROPOSAL_SCHEMA_URI, proposal))

        def variant(change) -> dict:
            value = copy.deepcopy(proposal)
            change(value)
            return value

        invalid = {
            "donation method": variant(lambda p: p["acquisition"].__setitem__("acquisition_method", "donation")),
            "selected while participatory": variant(lambda p: p["wave_source"].__setitem__("observed_status", "PARTICIPATORY")),
            "winner without decision record": variant(lambda p: p["wave_source"].pop("governance_decision_id")),
            "winner without decision time": variant(lambda p: p["wave_source"].__setitem__("decision_time", None)),
            "open while winner": variant(lambda p: p.__setitem__("status", "open")),
            "token claimed for named work": variant(lambda p: p["acquisition"].__setitem__("exact_token_specified", True)),
            "contributor ownership": variant(lambda p: p["acquisition"].__setitem__("contributor_ownership_interest", "fractional")),
            "proposer name": variant(lambda p: p["proposer"].__setitem__("name", "Example Member")),
            "missing transcription path": variant(lambda p: p["proposal_text"].pop("transcription_path")),
            "gift proposal id": variant(lambda p: p.__setitem__("proposal_id", "6529NM-PG-2026-901")),
            "wrong schema path": variant(lambda p: p.__setitem__("$schema", "../../../schemas/proposed-gift.schema.json")),
        }
        for label, value in invalid.items():
            with self.subTest(label=label):
                self.assertTrue(self.schema_errors(PROPOSAL_SCHEMA_URI, value), label)

        participatory = variant(
            lambda p: (
                p.__setitem__("status", "open"),
                p["wave_source"].__setitem__("observed_status", "PARTICIPATORY"),
                p["wave_source"].__setitem__("decision_time", None),
                p["wave_source"].pop("governance_decision_id"),
            )
        )
        self.assertEqual([], self.schema_errors(PROPOSAL_SCHEMA_URI, participatory))

    def test_proposed_acquisition_layout_is_closed(self) -> None:
        proposal = load_fixture("proposed-acquisition.json")
        with tempfile.TemporaryDirectory(prefix="museum-proposed-acquisition-") as temporary:
            root = Path(temporary)
            good = root / "records/proposed-acquisitions/6529NM-PA-2026-901/proposal.json"
            good.parent.mkdir(parents=True)
            self.assertEqual([], validate_proposed_acquisition_layout(root, [(good, proposal)]))

            renamed = root / "records/proposed-acquisitions/6529NM-PA-2026-902/proposal.json"
            self.assertTrue(any("directory must equal proposal_id" in issue for issue in validate_proposed_acquisition_layout(root, [(renamed, proposal)])))

            misplaced = root / "records/proposed-gifts/6529NM-PA-2026-901/proposal.json"
            self.assertTrue(any("must live at records/proposed-acquisitions" in issue for issue in validate_proposed_acquisition_layout(root, [(misplaced, proposal)])))

            other_name = root / "records/proposed-acquisitions/6529NM-PA-2026-901/notes.json"
            self.assertTrue(any("must live at records/proposed-acquisitions" in issue for issue in validate_proposed_acquisition_layout(root, [(other_name, proposal)])))

            gift_schema = dict(proposal)
            gift_schema["$schema"] = "../../../schemas/proposed-gift.schema.json"
            self.assertTrue(any("must declare the proposed-acquisition schema" in issue for issue in validate_proposed_acquisition_layout(root, [(good, gift_schema)])))

    def test_proposed_gift_tooling_ignores_proposed_acquisitions(self) -> None:
        proposal = load_fixture("proposed-acquisition.json")
        with tempfile.TemporaryDirectory(prefix="museum-proposed-acquisition-gift-tools-") as temporary:
            root = Path(temporary)
            path = root / "records/proposed-acquisitions/6529NM-PA-2026-901/proposal.json"
            path.parent.mkdir(parents=True)
            path.write_text(json.dumps(proposal), encoding="utf-8")
            (root / "records/proposed-gifts").mkdir(parents=True)
            self.assertEqual([], proposed_gift_issues(root, {path: proposal}))

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
