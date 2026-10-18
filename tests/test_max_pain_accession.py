"""Accession 6529NM.2026.005: XCOPY, MAX PAIN #4188/7394, a community-funded purchase."""

from __future__ import annotations

import hashlib
import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from validate import validate_purchase_provenance_joins  # noqa: E402

LOT = "6529NM.2026.005"
ACCESSION_ROOT = ROOT / "records" / "accessions" / LOT
PUBLIC_ROOT = ACCESSION_ROOT / "public"
CAIP19 = "eip155:1/erc721:0xd1169e5349d1cb9941f3dcba135c8a4b9eacfdde/171000104188"
SAFE = "0xbecfa2ba5a782d11e1a0e821e8f2e30b6684178c"
AGENT = "0xe84576bd68882e037d8e4df484ad9a15e2b855bc"
PURCHASE_TX = "0xdf8b07004bfed397920355ac80991a9dd592c896ca77b1fadb5655f8c85aa4d6"
RECEIPT_TX = "0xe7511598bbdabd1d4ff1c5bb7e6d1f9157a413fbcf305f0392cc30c92252ea03"
RESIDUAL_TX = "0x7d7b7733c696858dda93374395a978a4f7cb0cf4b631e2a81ab595f70d5debef"
RESIDUAL_ETH = "0.068496911687069084"
RESIDUAL_STATUS = "The Museum has received the funds but has not accepted them, and has asked the organizer how they should be held."
SUPPLEMENT_CONTRACTS = {
    "0xd1169e5349d1cb9941f3dcba135c8a4b9eacfdde",  # MAX PAIN AND FRENS
    "0x3e34ff1790bf0a13efd7d77e75870cb525687338",  # DAMAGE CONTROL
    "0x18a62e93ff3ab180e0c7abd4812595bf2be3405f",  # variant editions
    "0x33fd426905f149f8376e227d0c9d3340aad17af1",  # The Memes by 6529
}
CREDIT = (
    "XCOPY, MAX PAIN #4188/7394, 2022. Ethereum token "
    f"{CAIP19}. Acquired through a community-funded purchase organized by Shelby and authorized by the "
    "6529 Network Museum Wave, 2026. CC0 1.0."
)
DIRECT_RECORDS = (
    "accession-certificate.json",
    "accession-statement.json",
    "acquisition-authorization.json",
    "objects/6529NM.2026.005.01.json",
    "rights/6529NM.2026.005.RIGHTS.01.json",
    "technical/6529NM.2026.005.01.json",
)
# Manuscripts written in the Museum's voice. The contributor's essay is signed
# and checked separately; its Museum note is checked as Museum voice below.
MUSEUM_VOICE_MANUSCRIPTS = (
    "6529NM.2026.005.01.md",
    "accession-certificate.md",
    "acquisition-authorization.md",
    "alt-text.md",
    "max-pain-and-frens-project.md",
    "source-and-chronology.md",
    "web-presentation-authority.md",
    "xcopy-artist-practice.md",
)
GIFT_WORDING = re.compile(r"\bdonat\w*|\bgift of\b|\bfirst xcopy\b", re.IGNORECASE)
ORGANIZER_ATTRIBUTION = re.compile(r"\bthe organizer (announced|announces|calls|called)\b", re.IGNORECASE)


def load(relative: str | Path) -> dict:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def payload(relative: str) -> dict:
    return load(ACCESSION_ROOT / relative)["payload"]


def sentences(text: str) -> list[str]:
    return [part.strip() for part in re.split(r"(?<=[.!?])\s+|\n+|\|", text) if part.strip()]


class MaxPainAccessionTest(unittest.TestCase):
    def test_exact_identity_and_finalized_custody(self) -> None:
        obj = payload("objects/6529NM.2026.005.01.json")
        custody = load("evidence/xcopy-max-pain-4188-custody/summary.json")
        chain = obj["chain_identity"]
        self.assertEqual(obj["accession_lot_id"], LOT)
        self.assertEqual(obj["object_id"], "6529NM.2026.005.01")
        self.assertEqual(obj["title"], "MAX PAIN #4188/7394")
        self.assertEqual(obj["creator"], "XCOPY")
        self.assertEqual(chain["caip19"], CAIP19)
        self.assertEqual(chain["token_id"], "171000104188")
        self.assertEqual(chain["custody_account"], f"eip155:1:{SAFE}")
        self.assertEqual(chain["custody_status"], "verified")
        self.assertEqual(chain["custody_block"], custody["finalized_block"]["number"])
        self.assertEqual(chain["custody_receipt_log"], 955)
        self.assertEqual(custody["museum_address"], SAFE)
        self.assertTrue(all(custody["assertions"].values()))
        register = load("records/accessions/register.json")
        lot = next(row for row in register["lots"] if row["accession_lot_id"] == LOT)
        self.assertEqual(lot["acquisition_method"], "purchase")
        self.assertEqual(lot["custody"]["finalized_block"], custody["finalized_block"]["number"])
        self.assertEqual(lot["custody"]["finalized_block_hash"], custody["finalized_block"]["hash"])
        self.assertEqual(lot["receipt_event"]["transaction_hash"], RECEIPT_TX)
        self.assertEqual(register["record_control"]["revision"], len(register["amendment_history"]) + 1)

    def test_authority_and_media_ids(self) -> None:
        aqa = payload("acquisition-authorization.json")
        self.assertEqual(aqa["authorization_id"], "6529NM.2026.005.AQA-01")
        self.assertEqual(aqa["acquisition_method"], "purchase")
        self.assertEqual(aqa["authorization_status"], "formally_accepted")
        decision = aqa["governing_basis"][0]
        self.assertEqual((decision["decision_id"], decision["wave_serial"]), ("6529NM-GOV-1336667", 1336667))
        self.assertEqual(decision["observed_wave_status"], "WINNER")
        self.assertEqual(aqa["governing_basis"][1]["record_id"], "6529NM-POL-004")
        self.assertEqual(aqa["institutional_decision_authority"]["authority_basis"], "user_authorized_institutional_decision")
        self.assertIn("Merging the pull request", aqa["institutional_decision_authority"]["publication_semantics"])
        governance = load("records/governance/6529NM-GOV-1336667.json")["payload"]
        self.assertEqual(governance["decision_status"], "adopted")
        self.assertEqual(governance["effective_at"], "2026-08-27T18:30:18.491Z")
        self.assertEqual(governance["source"]["wave_serial"], "1336667")
        proposal = load("records/proposed-acquisitions/6529NM-PA-2026-001/proposal.json")
        self.assertEqual(proposal["wave_source"]["governance_decision_id"], "6529NM-GOV-1336667")
        self.assertFalse(proposal["acquisition"]["exact_token_specified"])
        self.assertEqual(proposal["proposal_text"]["sha256"], governance["proposal_text_sha256"])
        work = load("records/entities/6529NM-W-0036.json")["payload"]
        self.assertEqual(work["media_entity_ids"], ["6529NM-MED-0061", "6529NM-MED-0060"])
        self.assertEqual(work["profile"]["creator_entity_ids"], ["6529NM-ART-0025"])
        self.assertEqual(work["profile"]["acquisition_entity_ids"], ["6529NM-CA-2026-006"])
        self.assertEqual(work["profile"]["accession_entity_ids"], ["6529NM-ACC-ENT-0005"])
        self.assertEqual(work["profile"]["program_entity_ids"], [])
        acquisition = load("records/entities/6529NM-CA-2026-006.json")["payload"]["profile"]
        self.assertEqual(acquisition["acquisition_method"], "purchase")
        self.assertEqual(acquisition["program_or_pathway"]["kind"], "museum_wave_proposal")
        poster = load("records/entities/6529NM-MED-0061.json")["payload"]["profile"]["media"]
        animation = load("records/entities/6529NM-MED-0060.json")["payload"]["profile"]["media"]
        self.assertEqual(poster["media_role"], "museum_generated_public_derivative")
        self.assertEqual(poster["derived_from_media_entity_id"], "6529NM-MED-0060")
        self.assertEqual(animation["media_role"], "token_linked_source_media")
        self.assertNotIn("fullscreen", animation["allowed_ui_affordances"])
        self.assertNotIn("zoom", animation["allowed_ui_affordances"])
        manifest = load(PUBLIC_ROOT / "presentation-manifest.json")
        item = manifest["items"][0]
        self.assertEqual(item["work_entity_id"], "6529NM-W-0036")
        self.assertEqual(item["media_reference_entity_id"], "6529NM-MED-0061")
        self.assertEqual(item["animation_reference"]["media_reference_entity_id"], "6529NM-MED-0060")
        constraints = item["animation_reference"]["display_constraints"]
        self.assertFalse(constraints["autoplay"])
        self.assertEqual(constraints["initial_state"], "poster")
        self.assertEqual(constraints["max_css_width_px"], 512)
        self.assertEqual(constraints["css_size"], "min(512px, 100%)")
        self.assertEqual(constraints["reduced_motion"], "poster_only_no_play_control_when_prefers_reduced_motion")
        self.assertEqual(constraints["stop_control"], "visible_keyboard_operable_stop_returns_to_poster")
        self.assertEqual(constraints["playback_source"], "sha256_verified_bytes_only")
        self.assertEqual(constraints["fullscreen_or_enlarged_animation"], "not_permitted")
        self.assertEqual(item["animation_reference"]["access_urls"], ["https://gateway.pinata.cloud/ipfs/QmTcTzTPgCyvF933oeFvB4GkPgaXtF6dKuQgvg32qqLYGF"])
        self.assertNotIn("niftygateway", json.dumps(item["animation_reference"]))
        authority = (PUBLIC_ROOT / "web-presentation-authority.md").read_text(encoding="utf-8")
        self.assertTrue(authority.startswith("---\nrecord_id: 6529NM.2026.005.DISPLAY-01\nstatus: active\n"))
        self.assertIn("evidence/xcopy-max-pain-4188-display/", authority)
        condition = payload("technical/6529NM.2026.005.01.json")
        self.assertIn(
            "https://github.com/6529-Collections/6529networkmuseum/blob/main/evidence/xcopy-max-pain-4188-display/manifest.json",
            json.dumps(condition["events"]),
        )

    def test_credit_line_and_rights(self) -> None:
        obj = payload("objects/6529NM.2026.005.01.json")
        self.assertEqual(obj["credit_line"], CREDIT)
        self.assertEqual(obj["display"]["credit_line"], CREDIT)
        rights = payload("rights/6529NM.2026.005.RIGHTS.01.json")
        self.assertEqual(len(rights["grants"]), 9)
        for name, grant in rights["grants"].items():
            self.assertEqual(grant["grant_status"], "granted", name)
            self.assertIn("CC0 1.0", grant["basis"], name)
            self.assertIn("endorsement", grant["basis"], name)
        self.assertEqual(obj["rights"]["ai_training"]["grant_status"], "granted")
        self.assertIn("asserts no copyright", rights["rights_holder_reference"])
        registry = load("docs/rights/registry.json")
        self.assertNotIn("6529NM.2026.005.01", json.dumps(registry.get("object_assignments", [])))
        for record in (payload("acquisition-authorization.json"), load("records/entities/6529NM-CA-2026-006.json")["payload"]["profile"]):
            self.assertEqual(
                record["public_credit"],
                "Acquired through a community-funded purchase organized by Shelby and authorized by the 6529 Network Museum Wave, 2026",
            )

    def test_editorial_boundaries(self) -> None:
        for name in MUSEUM_VOICE_MANUSCRIPTS:
            text = (PUBLIC_ROOT / name).read_text(encoding="utf-8")
            for sentence in sentences(text):
                if GIFT_WORDING.search(sentence):
                    self.assertRegex(sentence, ORGANIZER_ATTRIBUTION, (name, sentence))
        essay = (PUBLIC_ROOT / "community-funded-acquisition.md").read_text(encoding="utf-8")
        museum_note = essay.split("## Museum note", 1)[1].split("## Credits", 1)[0]
        for sentence in sentences(museum_note):
            if GIFT_WORDING.search(sentence):
                self.assertRegex(sentence, ORGANIZER_ATTRIBUTION, sentence)
        self.assertIn("By SonOfLasG.", essay)
        self.assertIn("community-funded purchase", museum_note)
        # Public notes cite only committed evidence: aggregate wallet balances
        # and the accession register, not unretained per-transfer counts or a
        # Safe-history reading.
        self.assertIn("No earlier lot in the Museum's accession register, `6529NM.2026.001` to `6529NM.2026.003`, includes a work by XCOPY.", museum_note)
        self.assertIn("`evidence/xcopy-max-pain-4188-funding/summary.json`", essay)
        for cited in (
            "evidence/xcopy-max-pain-4188-display/close-looking-census.json",
            "evidence/xcopy-max-pain-4188-supplement/derived/damage-control-redemptions.json",
            "evidence/xcopy-max-pain-4188-supplement/wave/funding_call_2026_08_28.json",
            "evidence/xcopy-max-pain-4188-supplement/wave/residual_transfer_2026_09_14.json",
            "evidence/xcopy-max-pain-4188-supplement/raw/rpc/0011-edition-3265-burn-receipt-response.json",
        ):
            self.assertIn(cited, essay)
            self.assertTrue((ROOT / cited).is_file(), cited)
        self.assertNotIn("<INTEGRATION", essay)
        self.assertNotIn("<BEFORE PUBLICATION", essay)
        chronology = (PUBLIC_ROOT / "source-and-chronology.md").read_text(encoding="utf-8")
        for text in (essay, chronology):
            self.assertNotIn("incoming transfers", text)
            self.assertNotIn("24 payments", text)
            self.assertNotIn("26,217,714", text)
            self.assertNotIn("NFT transfer history", text)
        entry = (PUBLIC_ROOT / "6529NM.2026.005.01.md").read_text(encoding="utf-8")
        self.assertIn("6529NM.2026.005.AQA-01", entry)
        self.assertIn("6529NM-ACC-2026-005", entry)
        self.assertIn(CREDIT.replace("MAX PAIN #4188/7394", "*MAX PAIN #4188/7394*").replace(CAIP19, f"`{CAIP19}`"), entry)
        for path in sorted(PUBLIC_ROOT.glob("*.md")):
            text = path.read_text(encoding="utf-8")
            self.assertNotIn("<publication date>", text, path.name)
            self.assertNotIn("<accession date>", text, path.name)
        for record in DIRECT_RECORDS:
            text = json.dumps(payload(record))
            self.assertIsNone(GIFT_WORDING.search(text), record)

    def test_wave_api_status_does_not_claim_signature_verification(self) -> None:
        governance = load("records/governance/6529NM-GOV-1336667.json")["payload"]
        self.assertIn("signature not verified", json.dumps(governance["evidence_refs"]))
        proposal = load("records/proposed-acquisitions/6529NM-PA-2026-001/proposal.json")
        self.assertTrue(proposal["wave_source"]["api_reported_is_signed"])
        paths = [
            *(PUBLIC_ROOT / name for name in MUSEUM_VOICE_MANUSCRIPTS),
            PUBLIC_ROOT / "community-funded-acquisition.md",
            ROOT / "records/proposed-acquisitions/6529NM-PA-2026-001/public/wave-resolution.md",
        ]
        for path in paths:
            text = path.read_text(encoding="utf-8")
            self.assertNotIn("signed WINNER", text, path.name)
            self.assertNotIn("signed Wave", text, path.name)
            self.assertNotRegex(text, r"(?i)verified (the )?signature", path.name)

    def test_direct_accession_records_share_one_pending_or_reviewed_state(self) -> None:
        paths = sorted(path for path in ACCESSION_ROOT.rglob("*.json") if path.name != "presentation-manifest.json")
        self.assertEqual(len(DIRECT_RECORDS), len(paths))
        states = set()
        reviewers = []
        for path in paths:
            record = json.loads(path.read_text(encoding="utf-8"))["payload"]
            states.add((record["record_status"], record["review_status"]))
            reviewers.append(record["reviewer"])
            self.assertEqual(record["created_at"], record["effective_at"], path.name)
        self.assertEqual(1, len(states))
        state = states.pop()
        if state == ("review_pending", "pending_independent_review"):
            self.assertTrue(all(reviewer is None for reviewer in reviewers))
        else:
            self.assertEqual(("reviewed", "reviewed"), state)
            self.assertTrue(all(isinstance(reviewer, dict) for reviewer in reviewers))

    def test_purchase_invariants(self) -> None:
        aqa = payload("acquisition-authorization.json")
        statement = payload("accession-statement.json")
        certificate = payload("accession-certificate.json")
        obj = payload("objects/6529NM.2026.005.01.json")
        receipt = aqa["custody_receipts"][0]
        payment = aqa["consideration"]["payment_transaction"]
        # The Museum's acquisition transaction is the receipt into custody,
        # and it is the transaction the title binding names.
        self.assertEqual(receipt["transaction_hash"], RECEIPT_TX)
        self.assertEqual(obj["chain_identity"]["acquisition_transaction"], RECEIPT_TX)
        self.assertEqual(obj["chain_identity"]["custody_receipt_transaction"], RECEIPT_TX)
        self.assertEqual(obj["title_binding"]["transfer_transaction"], RECEIPT_TX)
        self.assertEqual(certificate["title_bindings"][0], obj["title_binding"])
        self.assertEqual(obj["title_binding"]["from"], AGENT)
        self.assertEqual(obj["title_binding"]["to"], SAFE)
        # The agent's purchase is a separate, earlier transaction of the recorded amount.
        self.assertEqual(payment["transaction_hash"], PURCHASE_TX)
        self.assertEqual(payment["value_wei"], "458999999900000000")
        self.assertEqual(aqa["consideration"]["amount_wei"], "458999999900000000")
        self.assertLess(payment["block_number"], receipt["block_number"])
        acquisition_event = next(event for event in certificate["events"] if event["event_type"] == "acquisition")
        self.assertEqual(acquisition_event["source_occurred_at"], payment["block_time"])
        self.assertIn("event_semantics", acquisition_event)
        instrument = next(event for event in certificate["events"] if event["event_type"] == "title_passage")["instrument"]
        self.assertEqual(instrument["kind"], "institutional_purchase_title_declaration")
        self.assertEqual(instrument["sha256"], obj["title_binding"]["instrument_sha256"])
        # The seller is named by role; its address lives only in the provenance schedule.
        self.assertNotIn("address", aqa["seller"])
        self.assertEqual(aqa["seller"]["provenance_record_id"], LOT)
        self.assertEqual([], validate_purchase_provenance_joins([("aqa", aqa), ("lot", statement)]))
        events = statement["provenance_schedule"]["objects"][0]["events"]
        self.assertEqual([event["kind"] for event in events], ["mint", "transfer", "transfer", "transfer", "transfer", "transfer", "museum_receipt"])
        self.assertTrue(all(event["direct_rpc_verified"] for event in events))
        for before, after in zip(events, events[1:]):
            self.assertEqual(before["to"], after["from"])
        # The residual ETH is outside the acquisition.
        self.assertTrue(any(RESIDUAL_TX in claim and "not part of this acquisition" in claim for claim in aqa["non_claims"]))
        self.assertTrue(any(RESIDUAL_TX in claim for claim in statement["non_claims"]))
        self.assertNotIn(RESIDUAL_TX, json.dumps(aqa["consideration"]))
        for name in ("acquisition-authorization.md", "source-and-chronology.md"):
            self.assertIn(RESIDUAL_STATUS, (PUBLIC_ROOT / name).read_text(encoding="utf-8"), name)
        self.assertIn(RESIDUAL_STATUS, (PUBLIC_ROOT / "community-funded-acquisition.md").read_text(encoding="utf-8"))
        residual_note = (ROOT / "notes/wip/2026-10-18-max-pain-residual-funding.md").read_text(encoding="utf-8")
        self.assertIn(RESIDUAL_ETH, residual_note)
        self.assertIn(RESIDUAL_STATUS, residual_note)

    def test_private_addresses_stay_in_machine_records_and_raw_evidence(self) -> None:
        statement = payload("accession-statement.json")
        events = statement["provenance_schedule"]["objects"][0]["events"]
        private_holders = {event["to"] for event in events[1:5]}
        self.assertEqual(4, len(private_holders))
        public_texts = [path.read_text(encoding="utf-8").lower() for path in sorted(PUBLIC_ROOT.glob("*.md"))]
        public_texts.append((ROOT / "records/proposed-acquisitions/6529NM-PA-2026-001/public/wave-resolution.md").read_text(encoding="utf-8").lower())
        public_texts.append((ACCESSION_ROOT / "current-view.md").read_text(encoding="utf-8").lower())
        for text in public_texts:
            self.assertNotIn(AGENT, text)
            for holder in private_holders:
                self.assertNotIn(holder, text)
        for record in DIRECT_RECORDS:
            text = json.dumps(payload(record)).lower()
            for holder in private_holders:
                if record == "accession-statement.json":
                    continue
                self.assertNotIn(holder, text, record)
        # Derived evidence names private accounts by role; their addresses stay
        # in raw RPC responses only.
        derived = sorted(
            path
            for path in (ROOT / "evidence/xcopy-max-pain-4188-supplement").rglob("*")
            if path.is_file() and "raw" not in path.relative_to(ROOT / "evidence/xcopy-max-pain-4188-supplement").parts
        )
        self.assertTrue(derived)
        for path in derived:
            text = path.read_bytes().decode("utf-8").lower()
            self.assertNotIn(AGENT, text, path.name)
            for holder in private_holders:
                self.assertNotIn(holder, text, path.name)
            for address in re.findall(r"0x[0-9a-f]{40}(?![0-9a-f])", text):
                self.assertIn(address, SUPPLEMENT_CONTRACTS, path.name)
        observation = json.loads((ROOT / "evidence/xcopy-max-pain-4188-technical/derived/observation.json").read_text(encoding="utf-8"))
        for row in observation["burns"]["by_transaction_target"]:
            if row["transaction_to"] is None:
                self.assertIn("address withheld", row["label"])
            else:
                self.assertNotIn("unlabelled", row["label"])

    def test_supplementary_readings_support_the_public_figures(self) -> None:
        supplement = ROOT / "evidence/xcopy-max-pain-4188-supplement"
        redemptions = json.loads((supplement / "derived/damage-control-redemptions.json").read_text(encoding="utf-8"))
        totals = redemptions["totals"]
        self.assertEqual(2547, totals["burn_logs"])
        self.assertEqual(2545, totals["burns_through_burn_redeem_extension"])
        self.assertEqual(2139, totals["burn_redeem_transactions"])
        self.assertEqual(2283, totals["redemptions_by_burn"])
        self.assertEqual(1215, totals["distinct_burn_redeem_accounts"])
        self.assertEqual(1429, totals["burns_through_2024_03_21_post_block"]["burns"])
        self.assertEqual(21525882, totals["last_redemption_burn"]["block"])
        hashes = (supplement / redemptions["burn_transaction_hash_list"]["path"]).read_bytes()
        self.assertEqual(redemptions["burn_transaction_hash_list"]["sha256"], "sha256:" + hashlib.sha256(hashes).hexdigest())
        titles = [row["title"] for row in redemptions["works"]]
        self.assertEqual(["OBLIVION", "BANG_BANG", "SIDEWAYZ", "CHURN", "CRAWLER", "XOMBO", "SH_MASH_MA", "BOT_ROT", "REIGN", "HEAVY"], titles)
        summary = json.loads((supplement / "summary.json").read_text(encoding="utf-8"))
        self.assertTrue(summary["edition_3265"]["same_wallet"])
        self.assertEqual(21, summary["mint_transactions"]["count"])
        identity = summary["contract_identity"]["damage_control"]
        self.assertEqual("xcopy.eth", identity["owner_ens_reverse_name"])
        self.assertTrue(identity["owner_equals_deployer"])
        self.assertEqual({"GIF"}, {row["image_format"] for row in identity["metadata"].values()})
        self.assertEqual("GIF", summary["memes_card_47"]["image_format"])
        self.assertEqual("Warning: flashing imagery", summary["nifty_gateway_creator_profile"]["text"])
        for message in summary["wave_messages"]:
            projection = json.loads((supplement / message["path"]).read_text(encoding="utf-8"))
            self.assertEqual("Shelby", projection["author_handle"])
            for part in projection["parts"]:
                transcript = (supplement / part["transcript_path"]).read_text(encoding="utf-8")
                self.assertNotIn("@[", transcript)


if __name__ == "__main__":
    unittest.main()
