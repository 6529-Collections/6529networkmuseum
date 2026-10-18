import argparse
import copy
import hashlib
import json
import re
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from acquire_wave_governance_evidence import (  # noqa: E402
    GovernanceEvidenceError,
    canonical_sha256,
    contains_profile_objects,
    decision_summary,
    iso_from_api_time,
    parse_decision,
    public_safe_projection,
    require_public_safe,
)


EVIDENCE = ROOT / "evidence/waves/museum-wave-governance-2026-10-18"
POLICY = ROOT / "policies/museum-gifts-acquisition-programs-and-funding-assets.md"
DECISION = ROOT / "records/governance/6529NM-GOV-1282091.json"
SOURCE_NOTE = ROOT / "notes/wip/2026-08-08-museum-gifts-acquisition-programs-and-funding-assets-policy.md"
DROP_ID = "6387c484-c602-4a2f-8d8b-456395cf077f"
WAVE_ID = "5f207393-5418-4a75-8738-e40edb44a94d"
CONTENT_SHA256 = "ce4962072ddd0cbfacb7a071be51ae779c4cae40410851e6386e49ca405becb2"
PROJECTION_PATH = f"projections/drop-{DROP_ID}.json"
PART_PATH = f"parts/drop-{DROP_ID}-part-1.txt"
WITHDRAWN = {
    "a991d0b2-4c57-4ae1-b3b1-0680a4772998": 1281404,
    "401bdae4-1da7-41d0-aeef-73b1da78b39d": 1282040,
}
TRANSCRIPTION_NOTE = (
    "The following is the adopted proposal text. The heading above is its first line. "
    "Only this metadata block has been inserted; every other line is unchanged."
)
# Token contracts named by the policy's settlement-asset schedule. They are
# policy text, not personal wallet addresses.
POLICY_TOKEN_CONTRACTS = {
    "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",
    "0xdac17f958d2ee523a2206206994597c13d831ec7",
}
PROFILE_TEXT_MARKERS = ('"handle"', '"primary_address"', '"top_raters"', '"author"', '"pfp"')


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


class MuseumGiftsFundingPolicyRecordTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = load_json(EVIDENCE / "manifest.json")
        cls.summary = load_json(EVIDENCE / "summary.json")
        cls.projection = load_json(EVIDENCE / PROJECTION_PATH)
        cls.payload_projection = cls.projection["payload"]
        cls.part_bytes = (EVIDENCE / PART_PATH).read_bytes()
        cls.content = cls.part_bytes.decode("utf-8")
        cls.record = load_json(DECISION)
        cls.payload = cls.record["payload"]

    def test_projection_records_the_adopted_museum_wave_proposal(self) -> None:
        payload = self.payload_projection
        self.assertEqual(payload["drop_id"], DROP_ID)
        self.assertEqual(payload["serial_no"], 1282091)
        self.assertEqual(payload["wave_id"], WAVE_ID)
        self.assertEqual(payload["drop_type"], "WINNER")
        self.assertIs(payload["is_signed"], True)
        self.assertEqual(payload["title"], "Museum Gifts, Acquisition Programs, and Funding Assets Policy")
        self.assertEqual(payload["parts_count"], 1)
        self.assertEqual(payload["winning_context"]["decision_time"], "2026-08-10T09:55:07.644Z")
        self.assertEqual(iso_from_api_time(payload["winning_context"]["decision_time_api_value"]), "2026-08-10T09:55:07.644Z")
        self.assertEqual(payload["created_at"], "2026-08-08T09:43:48.737Z")
        self.assertEqual(self.projection["payload_sha256"], canonical_sha256(payload))

    def test_raw_profile_response_is_not_retained(self) -> None:
        raw = self.projection["raw_response"]
        self.assertEqual(raw["retention"], "not_retained")
        self.assertFalse((EVIDENCE / f"raw/drop-{DROP_ID}.json").exists())
        entry = next(item for item in self.summary["entries"] if item["source_id"] == f"drop-{DROP_ID}")
        self.assertEqual(entry["retention"], "public_safe_projection")
        self.assertEqual(entry["retained_paths"], [PROJECTION_PATH, PART_PATH])
        self.assertEqual(raw["sha256"], "sha256:" + entry["transport"]["byte_sha256"])
        self.assertEqual(raw["size"], entry["transport"]["byte_length"])
        self.assertEqual(raw["sha256"], "sha256:" + entry["raw_sha256"])
        decision = self.summary["decisions"][0]
        self.assertEqual(decision["raw_response"], {"retained": False, "sha256": raw["sha256"], "size": raw["size"]})

    def test_package_contains_no_profile_objects_or_wallet_addresses(self) -> None:
        for path in sorted(EVIDENCE.rglob("*")):
            if not path.is_file():
                continue
            with self.subTest(path=path.relative_to(EVIDENCE).as_posix()):
                text = path.read_text(encoding="utf-8")
                for marker in PROFILE_TEXT_MARKERS:
                    self.assertNotIn(marker, text)
                addresses = {value.lower() for value in re.findall(r"0x[0-9a-fA-F]{40}(?![0-9a-fA-F])", text)}
                self.assertLessEqual(addresses, POLICY_TOKEN_CONTRACTS)
                if path.suffix == ".json":
                    self.assertFalse(contains_profile_objects(load_json(path)))

    def test_part_content_matches_the_publication_receipt_and_source_note(self) -> None:
        self.assertEqual(hashlib.sha256(self.part_bytes).hexdigest(), CONTENT_SHA256)
        self.assertEqual(len(self.part_bytes), 16_289)
        self.assertEqual(len(self.content.encode("utf-16-le")) // 2, 16_289)
        note = SOURCE_NOTE.read_text(encoding="utf-8").replace("\r\n", "\n").strip()
        self.assertEqual(note, self.content)
        part = self.payload_projection["parts"][0]
        self.assertEqual(part["content_path"], PART_PATH)
        self.assertEqual(part["content_sha256"], f"sha256:{CONTENT_SHA256}")
        self.assertEqual(part["content_utf8_bytes"], len(self.part_bytes))

    def test_policy_file_is_an_exact_transcription_with_one_inserted_metadata_block(self) -> None:
        text = POLICY.read_text(encoding="utf-8").replace("\r\n", "\n")
        title, separator, _remainder = self.content.partition("\n\n")
        self.assertTrue(separator)
        self.assertTrue(text.startswith(title + "\n\n"))
        head, separator, body = text.partition(TRANSCRIPTION_NOTE + "\n\n")
        self.assertTrue(separator, "transcription note is missing")
        self.assertEqual(title + "\n\n" + body.rstrip("\n"), self.content)
        self.assertTrue(text.endswith("\n") and not text.endswith("\n\n"))
        decision = self.summary["decisions"][0]
        for line in (
            "Record ID: `6529NM-POL-004`",
            "Governance decision: `6529NM-GOV-1282091`",
            "Wave serial: `1282091`",
            f"Drop: `{DROP_ID}`",
            f"Status observed {decision['observed_at']}: `WINNER`",
            "Wave decision time: `2026-08-10T09:55:07.644Z`",
            f"Proposal-content SHA-256: `sha256:{CONTENT_SHA256}`",
        ):
            self.assertIn("\n" + line + "\n", head)

    def test_summary_restates_the_projection(self) -> None:
        decisions = self.summary["decisions"]
        self.assertEqual(len(decisions), 1)
        decision = decisions[0]
        payload = self.payload_projection
        self.assertEqual(decision["drop_id"], DROP_ID)
        self.assertEqual(decision["evidence_path"], PROJECTION_PATH)
        self.assertEqual(decision["observed_at"], self.projection["observed_at"])
        for key in ("drop_type", "is_signed", "rating", "realtime_rating", "raters_count", "serial_no"):
            self.assertEqual(decision[key], payload[key])
        self.assertEqual(decision["decision_time"], payload["winning_context"]["decision_time"])
        self.assertEqual(decision["part_content"]["sha256"], f"sha256:{CONTENT_SHA256}")
        self.assertEqual(decision["part_content"]["path"], PART_PATH)

    def test_withdrawn_proposals_are_absent_from_the_api(self) -> None:
        rows = {row["drop_id"]: row for row in self.summary["withdrawn_proposals"]}
        self.assertEqual(set(rows), set(WITHDRAWN))
        for drop_id in WITHDRAWN:
            with self.subTest(drop_id=drop_id):
                raw_path = EVIDENCE / f"raw/drop-{drop_id}.json"
                body = load_json(raw_path)
                self.assertEqual(body, {"error": f"Drop {drop_id} not found"})
                self.assertEqual(rows[drop_id]["http_status"], 404)
                self.assertIs(rows[drop_id]["present"], False)
                entry = next(item for item in self.summary["entries"] if item["source_id"] == f"drop-{drop_id}")
                self.assertEqual(entry["retention"], "raw_response")
                self.assertEqual(entry["transport"]["byte_sha256"], hashlib.sha256(raw_path.read_bytes()).hexdigest())

    def test_manifest_covers_every_retained_file(self) -> None:
        declared = {entry["path"] for entry in self.manifest["entries"]}
        actual = {
            path.relative_to(EVIDENCE).as_posix()
            for path in EVIDENCE.rglob("*")
            if path.is_file() and path.name != "manifest.json"
        }
        self.assertEqual(declared, actual)
        self.assertEqual(self.manifest["byte_mode"], "raw")

    def test_governance_decision_binds_the_evidence(self) -> None:
        decision = self.summary["decisions"][0]
        self.assertEqual(self.payload["record_id"], "6529NM-GOV-1282091")
        self.assertEqual(self.payload["decision_id"], "6529NM-GOV-1282091")
        self.assertEqual(self.payload["decision_status"], "adopted")
        self.assertEqual(self.payload["effective_at"], decision["decision_time"])
        self.assertEqual(self.payload["observed_at"], decision["observed_at"])
        self.assertEqual(self.payload["proposal_text_sha256"], f"sha256:{CONTENT_SHA256}")
        source = self.payload["source"]
        self.assertEqual(source["status"], "WINNER")
        self.assertEqual(source["wave_serial"], "1282091")
        self.assertEqual(source["drop_id"], DROP_ID)
        self.assertEqual(source["status_observed_at"], decision["observed_at"])
        self.assertEqual(source["status_evidence_uri"], f"https://api.6529.io/api/drops/{DROP_ID}")
        self.assertIn("6529NM-GOV-1052812", self.payload["references"])
        refs = {ref["label"]: ref for ref in self.payload["evidence_refs"]}
        projection_ref = refs["Public-safe projection of the Wave API readback: WINNER"]
        projection_bytes = (EVIDENCE / PROJECTION_PATH).read_bytes()
        self.assertEqual(projection_ref["sha256"], "sha256:" + hashlib.sha256(projection_bytes).hexdigest())
        self.assertTrue(projection_ref["uri"].endswith(f"evidence/waves/museum-wave-governance-2026-10-18/{PROJECTION_PATH}"))
        self.assertIn(self.projection["raw_response"]["sha256"], projection_ref["notes"])
        text_ref = refs["Exact proposal text: parts[0].content as returned by the API"]
        self.assertEqual(text_ref["sha256"], f"sha256:{CONTENT_SHA256}")
        self.assertTrue(text_ref["uri"].endswith(f"evidence/waves/museum-wave-governance-2026-10-18/{PART_PATH}"))
        withdrawn = refs["Readbacks of withdrawn proposals 1281404 and 1282040: HTTP 404"]
        summary_bytes = (EVIDENCE / "summary.json").read_bytes()
        self.assertEqual(withdrawn["sha256"], "sha256:" + hashlib.sha256(summary_bytes).hexdigest())

    def test_governance_decision_makes_no_acceptance_claim(self) -> None:
        effect = self.payload["authority_effect"]
        self.assertIn("6529NM-POL-004", effect)
        self.assertIn("does not itself accept, acquire, or accession any work or asset", effect)
        self.assertEqual(self.payload["record_status"], "review_pending")
        self.assertIsNone(self.payload["reviewer"])


class WaveGovernanceEvidenceScriptTests(unittest.TestCase):
    def setUp(self) -> None:
        self.drop = {
            "id": DROP_ID,
            "serial_no": 1282091,
            "wave": {"id": WAVE_ID, "name": "6529 Network Museum"},
            "drop_type": "WINNER",
            "is_signed": True,
            "author": {"handle": "test-author-handle", "primary_address": "0x" + "1" * 40},
            "top_raters": [{"rating": 5, "profile": {"handle": "test-rater-handle", "primary_address": "0x" + "2" * 40}}],
            "parts": [{"part_id": 1, "content": "# Title\n\nText", "media": [], "attachments": [], "quoted_drop": None}],
            "parts_count": 1,
            "winning_context": {"place": 1, "decision_time": 1786355707644},
            "created_at": 1786182228737,
        }
        self.digest = hashlib.sha256(b"# Title\n\nText").hexdigest()

    def test_projection_drops_profiles_and_keeps_part_bytes(self) -> None:
        self.assertTrue(contains_profile_objects(self.drop))
        payload, part_files = public_safe_projection(DROP_ID, self.drop)
        self.assertFalse(contains_profile_objects(payload))
        self.assertEqual(part_files, {f"parts/drop-{DROP_ID}-part-1.txt": b"# Title\n\nText"})
        serialized = json.dumps(payload)
        self.assertNotIn("test-author-handle", serialized)
        self.assertNotIn("test-rater-handle", serialized)
        self.assertNotIn("0x" + "1" * 40, serialized)
        self.assertEqual(payload["parts"][0]["content_sha256"], f"sha256:{self.digest}")

    def test_profile_free_error_body_is_retainable(self) -> None:
        self.assertFalse(contains_profile_objects({"error": f"Drop {DROP_ID} not found"}))
        self.assertTrue(contains_profile_objects({"error": "x", "mentioned_users": [{"id": "1"}]}))
        self.assertTrue(contains_profile_objects({"value": "0x" + "a" * 40}))

    def test_public_safe_guard_fails_closed(self) -> None:
        for value in ({"author": None}, {"nested": [{"handle": "x"}]}, {"address": "0x" + "3" * 40}):
            with self.subTest(value=value), self.assertRaises(GovernanceEvidenceError):
                require_public_safe(value)

    def test_decision_summary_records_exact_part_digest(self) -> None:
        row = decision_summary(DROP_ID, self.digest, self.drop)
        self.assertEqual(row["part_content"]["sha256"], f"sha256:{self.digest}")
        self.assertEqual(row["part_content"]["path"], f"parts/drop-{DROP_ID}-part-1.txt")
        self.assertEqual(row["decision_time"], "2026-08-10T09:55:07.644Z")

    def test_decision_summary_fails_closed(self) -> None:
        mutations = {
            "wrong digest": (lambda drop: drop, "0" * 64),
            "other wave": (lambda drop: drop.update(wave={"id": "00000000-0000-0000-0000-000000000000"}), None),
            "two parts": (lambda drop: drop["parts"].append({"part_id": 2, "content": "x"}), None),
            "empty part": (lambda drop: drop["parts"][0].update(content=""), None),
            "no text part": (lambda drop: drop["parts"][0].pop("content"), None),
            "other id": (lambda drop: drop.update(id="00000000-0000-0000-0000-000000000000"), None),
        }
        for name, (mutate, digest) in mutations.items():
            with self.subTest(mutation=name):
                drop = copy.deepcopy(self.drop)
                mutate(drop)
                with self.assertRaises(GovernanceEvidenceError):
                    decision_summary(DROP_ID, digest or self.digest, drop)

    def test_argument_parsing_and_time_conversion(self) -> None:
        self.assertEqual(parse_decision(f"{DROP_ID}:{self.digest}"), (DROP_ID, self.digest))
        self.assertEqual(parse_decision(DROP_ID), (DROP_ID, None))
        for value in (DROP_ID.upper(), f"{DROP_ID}:{self.digest.upper()}", "not-a-uuid"):
            with self.subTest(value=value), self.assertRaises(argparse.ArgumentTypeError):
                parse_decision(value)
        self.assertIsNone(iso_from_api_time(True))
        self.assertIsNone(iso_from_api_time("1786355707644"))


if __name__ == "__main__":
    unittest.main()
