import json
import sys
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from validate_data_architecture import validate as validate_data_architecture  # noqa: E402


PROFILE_PATH = ROOT / "docs/data-architecture/profile.json"
SCHEMA_PATH = ROOT / "schemas/museum-data-architecture-profile.schema.json"
CASEY_SCHEDULE_PATH = ROOT / "docs/data-architecture/casey-reas-machine-schedule.json"
CASEY_SCHEMA_PATH = ROOT / "schemas/museum-data-architecture-case-study.schema.json"

STANDARD_SLUGS = {
    "spectrum",
    "cidoc-crm",
    "lido",
    "premis",
    "prov-o",
    "getty-aat-ulan",
    "iiif",
    "c2pa",
    "bagit",
    "ocfl",
    "caip-19",
}


class DataArchitectureProfileTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.profile = json.loads(PROFILE_PATH.read_text(encoding="utf-8"))
        cls.schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        cls.casey_schedule = json.loads(CASEY_SCHEDULE_PATH.read_text(encoding="utf-8"))
        cls.casey_schema = json.loads(CASEY_SCHEMA_PATH.read_text(encoding="utf-8"))

    def test_profile_validates_against_closed_schema(self) -> None:
        Draft202012Validator.check_schema(self.schema)
        validator = Draft202012Validator(self.schema, format_checker=FormatChecker())
        self.assertEqual([], list(validator.iter_errors(self.profile)))

    def test_exact_standard_registry_and_documents(self) -> None:
        standards = self.profile["standards"]
        slugs = [standard["slug"] for standard in standards]
        self.assertEqual(len(slugs), len(set(slugs)))
        self.assertEqual(STANDARD_SLUGS, set(slugs))

        for standard in standards:
            self.assertEqual(
                f"docs/data-architecture/{standard['slug']}.md",
                standard["document_path"],
            )
            path = ROOT / standard["document_path"]
            self.assertTrue(path.is_file(), standard["document_path"])
            text = path.read_text(encoding="utf-8")
            self.assertIn("## The question", text)
            self.assertIn("## What this standard leaves to the Museum", text)
            self.assertIn("## For machines and implementers", text)
            self.assertIn("## The Casey Reas accession", text)
            self.assertIn("## Official sources", text)
            self.assertLess(text.index("## The question"), text.index("## For machines and implementers"))
            self.assertIn(f"`{standard['casey_state']}`", text)

    def test_case_study_and_landing_cover_every_standard(self) -> None:
        landing = (ROOT / self.profile["source_document"]).read_text(encoding="utf-8")
        case_study_path = ROOT / self.profile["case_study_path"]
        case_study = case_study_path.read_text(encoding="utf-8")
        self.assertTrue(case_study_path.is_file())

        for standard in self.profile["standards"]:
            self.assertIn(f"data-architecture/{standard['slug']}.md", landing)
            self.assertIn(standard["name"], case_study)

    def test_only_spectrum_is_operational_for_casey(self) -> None:
        operational = [
            standard["slug"]
            for standard in self.profile["standards"]
            if standard["casey_state"] == "operational"
        ]
        self.assertEqual(["spectrum"], operational)
        self.assertFalse(
            any(
                standard["casey_state"] in {"serialized", "validated"}
                for standard in self.profile["standards"]
            )
        )

    def test_casey_machine_schedule_validates_against_closed_schema(self) -> None:
        Draft202012Validator.check_schema(self.casey_schema)
        validator = Draft202012Validator(self.casey_schema, format_checker=FormatChecker())
        self.assertEqual([], list(validator.iter_errors(self.casey_schedule)))

    def test_casey_machine_schedule_matches_canonical_objects_one_to_one(self) -> None:
        case_study = (ROOT / self.profile["case_study_path"]).read_text(encoding="utf-8")
        object_root = ROOT / "records/accessions/6529NM.2026.001/objects"
        object_paths = sorted(object_root.glob("6529NM.2026.001.*.json"))
        self.assertEqual(7, len(object_paths))

        expected_rows = []

        for path in object_paths:
            record = json.loads(path.read_text(encoding="utf-8"))
            payload = record["payload"]
            chain = payload["chain_identity"]
            self.assertIn(payload["object_id"], case_study)
            expected_rows.append(
                {
                    "object_id": payload["object_id"],
                    "title": payload["title"],
                    "caip19": chain["caip19"],
                    "custody_receipt_log": chain["custody_receipt_log"],
                    "metadata_sha256": chain["metadata_sha256"],
                    "generator_observation_sha256": chain["generator_sha256"],
                    "generator_bytes_retained": False,
                    "accession_state": payload["current_state"],
                    "preservation_state": payload["preservation"]["status"],
                }
            )
            self.assertEqual(
                self.casey_schedule["custody_transaction"],
                chain["custody_receipt_transaction"],
            )
            self.assertEqual(self.casey_schedule["custody_block"], chain["custody_receipt_block"])

        self.assertEqual(expected_rows, self.casey_schedule["objects"])
        self.assertIn(self.casey_schedule["custody_transaction"], case_study)
        self.assertIn(f"`{self.casey_schedule['custody_block']:,}`", case_study)
        self.assertIn("all seven works is `in_progress`", case_study)

    def test_full_semantic_validator_includes_architecture(self) -> None:
        self.assertEqual([], validate_data_architecture(ROOT))

    def test_stream_is_a_deferred_interoperability_mapping(self) -> None:
        stream = self.profile["stream_convergence"]
        self.assertFalse(stream["normative_for_profile"])
        self.assertEqual("deferred_until_museum_profile_release", stream["status"])
        self.assertTrue((ROOT / stream["document_path"]).is_file())


if __name__ == "__main__":
    unittest.main()
