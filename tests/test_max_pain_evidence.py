"""Offline invariants of the MAX PAIN #4188/7394 evidence packages and helpers."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import acquire_max_pain_source_evidence as source_tool  # noqa: E402
import ipfs_unixfs  # noqa: E402
import max_pain_evidence_common as common  # noqa: E402
from gif_structure import parse_gif  # noqa: E402


EVIDENCE = ROOT / "evidence"
CUSTODY = EVIDENCE / "xcopy-max-pain-4188-custody"
SOURCES = EVIDENCE / "xcopy-max-pain-4188-sources"
TECHNICAL = EVIDENCE / "xcopy-max-pain-4188-technical"
FUNDING = EVIDENCE / "xcopy-max-pain-4188-funding"
PACKAGES = (CUSTODY, SOURCES, TECHNICAL, FUNDING)
ADDRESS = re.compile(r"0x[0-9a-fA-F]{40}")


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class HelperTests(unittest.TestCase):
    def test_cidv0_recomputation_matches_known_and_token_values(self) -> None:
        self.assertEqual("QmT78zSuBmuS4z925WZfrqQ1qHaJ56DQaTfyMUF7F8ff5o", ipfs_unixfs.cidv0_for_file(b"hello world\n")["cid"])
        metadata = (SOURCES / "raw" / "token-metadata.json").read_bytes()
        self.assertEqual("QmRF5jKUG5trdmEV6zJnVgnLR6QPefhSiQWjhyyC4F2BfE", ipfs_unixfs.cidv0_for_file(metadata)["cid"])

    def test_murmur3_and_hamt_shard_index(self) -> None:
        self.assertEqual((0xCBD8A7B341BD9B02, 0x5B1E906A48AE1D19), ipfs_unixfs.murmur3_x64_128(b"hello"))
        self.assertEqual(("63", "CC"), (ipfs_unixfs.hamt_index("171000104188", 0), ipfs_unixfs.hamt_index("171000104188", 1)))

    def test_visible_text_omits_scripts_and_redacts_email(self) -> None:
        html = "<html><head><title>x</title><script>alert('<script>')</script></head><body><p>One  of  4849</p><style>p{}</style><p>a@b.example</p></body></html>"
        text, count = source_tool.redact_emails(source_tool.visible_text(html))
        self.assertEqual("One of 4849\n[email address omitted]\n", text)
        self.assertEqual(1, count)
        with self.assertRaises(common.EvidenceError):
            source_tool.safe_transcript("&lt;script&gt; decoded <script>", "x")

    def test_fixed_identities_and_poisoning_guard(self) -> None:
        common.assert_fixed_identities()
        common.require_museum_address(common.MUSEUM_CHECKSUM_ADDRESS, "checksum form")
        lookalike = "0xbecfa674" + common.MUSEUM_ADDRESS[10:]
        with self.assertRaises(common.EvidenceError):
            common.require_museum_address(lookalike, "look-alike")


class PackageTests(unittest.TestCase):
    def test_manifests_cover_every_file_with_exact_bytes(self) -> None:
        for package in PACKAGES:
            with self.subTest(package=package.name):
                manifest = load(package / "manifest.json")
                declared = {row["path"]: row for row in manifest["entries"]}
                actual = {path.relative_to(package).as_posix() for path in package.rglob("*") if path.is_file() and path.name != "manifest.json"}
                if package == TECHNICAL:
                    # Vera technical precedent: summary.json commits to the manifest hash, so it sits outside it.
                    self.assertEqual(f"sha256:{hashlib.sha256((package / 'manifest.json').read_bytes()).hexdigest()}", load(package / "summary.json")["manifest_sha256"])
                    actual.discard("summary.json")
                self.assertEqual(actual, set(declared))
                for relative, row in declared.items():
                    payload = (package / relative).read_bytes()
                    self.assertEqual(row["sha256"], hashlib.sha256(payload).hexdigest(), relative)
                    self.assertEqual(row["size"], len(payload), relative)

    def test_custody_binds_receipt_finality_and_ens(self) -> None:
        summary = load(CUSTODY / "summary.json")
        self.assertTrue(all(summary["assertions"].values()))
        obj = summary["objects"][0]
        self.assertEqual((common.OBJECT_ID, common.TOKEN_ID, 955, common.MUSEUM_RECEIPT_TX), (obj["object_id"], obj["token_id"], obj["log_index"], obj["tx_hash"]))
        self.assertEqual(common.MUSEUM_ADDRESS, summary["custodian"]["address"])
        self.assertEqual(common.AGENT_ADDRESS, obj["transfer_from"])
        self.assertEqual("458999999900000000", summary["agent_purchase"]["value_wei"])
        self.assertEqual(str(common.RESIDUAL_VALUE_WEI), summary["residual_transfer"]["value_wei"])
        self.assertEqual(summary["finalized_block"]["hash"], summary["state_selector"]["blockHash"])

    def test_source_package_binds_gif_metadata_and_wave(self) -> None:
        summary = load(SOURCES / "summary.json")
        self.assertTrue(all(summary["assertions"].values()))
        gif = (SOURCES / "raw" / "token-image.gif").read_bytes()
        self.assertEqual(common.IMAGE_SHA256, hashlib.sha256(gif).hexdigest())
        self.assertEqual(common.IMAGE_CID, ipfs_unixfs.cidv0_for_file(gif)["cid"])
        structure = parse_gif(gif)
        self.assertEqual((8, 40, 0, 4000, 4000), (structure.frame_count, structure.total_delay_centiseconds, structure.loop_count, structure.width, structure.height))
        self.assertEqual({"frame_count": 8, "frame_duration_ms": 50, "total_duration_ms": 400, "loop": "infinite"}, summary["media"]["animation"])
        metadata = load(SOURCES / "raw" / "token-metadata.json")
        self.assertEqual(common.IMAGE_CID, metadata["image_hash"])
        self.assertNotIn("license", metadata)
        observations = summary["wave"]["observations"]
        self.assertEqual(("WINNER", True, 1336667, 25), (observations["drop_type"], observations["is_signed"], observations["serial_no"], observations["distinct_voters"]))
        self.assertEqual("2026-08-27T18:30:18.491Z", observations["decision_time"])

    def test_wave_projections_are_public_safe_and_hash_bound(self) -> None:
        for path in sorted((SOURCES / "raw" / "wave").glob("*.json")):
            with self.subTest(path=path.name):
                record = load(path)
                text = path.read_text(encoding="utf-8")
                self.assertIsNone(ADDRESS.search(text))
                self.assertNotRegex(text, r'"(?:primary_address|handle|pfp|voter|profile|top_raters|reactions)"\s*:')
                self.assertFalse(record["raw_response"]["retained"])
                self.assertEqual(record["payload_sha256"], "sha256:" + hashlib.sha256(common.canonical_json(record["payload"])).hexdigest())

    def test_transcripts_and_platform_sources_are_text_only(self) -> None:
        for path in sorted((SOURCES / "raw").rglob("*")):
            if path.suffix in {".txt", ".json"}:
                with self.subTest(path=path.name):
                    text = path.read_text(encoding="utf-8")
                    self.assertNotIn("<script", text.lower())
                    self.assertIsNone(re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text) if path.parent.name == "xcopy-art" else None)

    def test_funding_is_aggregate_only(self) -> None:
        summary = load(FUNDING / "summary.json")
        self.assertTrue(summary["totals"]["identity_holds"])
        self.assertEqual("0.5276", summary["totals"]["total_inflow_eth"])
        addresses = {match.lower() for match in ADDRESS.findall((FUNDING / "summary.json").read_text(encoding="utf-8"))}
        self.assertLessEqual(addresses, {common.AGENT_ADDRESS, common.MUSEUM_ADDRESS})

    def test_summaries_name_no_prior_private_holder(self) -> None:
        provenance = load(TECHNICAL / "summary.json")["observation"]["provenance"]
        public_roles = {value.lower() for value in provenance["known_role_addresses"].values()} | {common.CONTRACT, common.SEAPORT_1_6, common.ZERO_ADDRESS}
        holder_addresses = set()
        for event in provenance["events"]:
            refs = event.get("address_refs", {})
            for side in ("from", "to"):
                if side in refs:
                    receipt = load(TECHNICAL / refs[side]["path"])["result"]
                    log = next(row for row in receipt["logs"] if int(row["logIndex"], 16) == refs[side]["log_index"])
                    holder_addresses.add("0x" + log["topics"][refs[side]["topic_index"]][-40:].lower())
        private = holder_addresses - public_roles
        self.assertEqual(4, len(private))
        for package in PACKAGES:
            for name in ("summary.json", "manifest.json"):
                text = (package / name).read_text(encoding="utf-8").lower()
                for address in private:
                    self.assertNotIn(address, text, f"{package.name}/{name}")
        derived = (TECHNICAL / "derived" / "observation.json").read_text(encoding="utf-8").lower()
        for address in private:
            self.assertNotIn(address, derived)

    def test_technical_supply_burns_and_provenance(self) -> None:
        observation = load(TECHNICAL / "summary.json")["observation"]
        self.assertTrue(all(observation["assertions"].values()))
        supply = observation["supply"]
        self.assertEqual((7394, 7394), (supply["minted_count_onchain"], supply["scanned_id_count"]))
        self.assertEqual(supply["existing_count"] + supply["nonexistent_count"], 7394)
        self.assertEqual(1, supply["held_by_museum_safe"])
        burns = observation["burns"]
        self.assertTrue(burns["burned_token_ids_equal_ownerOf_nonexistent_ids"])
        self.assertEqual(burns["burn_log_count"], supply["nonexistent_count"])
        events = observation["provenance"]["events"]
        self.assertEqual(["mint", "platform_withdrawal", "secondary_sale", "transfer_without_payment", "secondary_sale", "agent_purchase", "museum_receipt"], [event["kind"] for event in events])
        self.assertEqual("museum_safe", events[-1]["to_role"])
        self.assertEqual("458999999900000000", events[5]["payment"]["gross_amount_wei"])


if __name__ == "__main__":
    unittest.main()
