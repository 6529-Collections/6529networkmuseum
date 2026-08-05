from __future__ import annotations

import copy
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from scripts.validate_rights_handbook import ROOT, validate


class RightsHandbookValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        for relative in (
            "docs/rights",
            "schemas/rights-expression-registry.schema.json",
            "records/institutional-practice/rights-and-licenses.md",
            "records/institutional-practice/rights-for-artists.md",
            "records/institutional-practice/rights-for-collectors.md",
            "records/accessions/6529NM.2026.001/rights",
        ):
            source = ROOT / relative
            destination = self.root / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            if source.is_dir():
                shutil.copytree(source, destination)
            else:
                shutil.copy2(source, destination)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    @property
    def registry_path(self) -> Path:
        return self.root / "docs/rights/registry.json"

    def mutate_registry(self, mutate) -> None:
        registry = json.loads(self.registry_path.read_text(encoding="utf-8"))
        mutate(registry)
        self.registry_path.write_text(
            json.dumps(registry, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    def test_canonical_registry_passes(self) -> None:
        self.assertEqual(validate(self.root), [])

    def test_legal_text_mutation_is_rejected(self) -> None:
        path = self.root / "docs/rights/legal-texts/cc-by-4.0.txt"
        path.write_bytes(path.read_bytes() + b"\nchanged\n")
        self.assertTrue(any("legal text digest mismatch" in issue for issue in validate(self.root)))

    def test_unknown_object_expression_is_rejected(self) -> None:
        self.mutate_registry(
            lambda registry: registry["object_assignments"][0].update(
                {"expression_id": "missing-license"}
            )
        )
        issues = validate(self.root)
        self.assertTrue(any("unknown rights expression" in issue for issue in issues))

    def test_casey_assignment_cannot_drift_from_reviewed_license(self) -> None:
        self.mutate_registry(
            lambda registry: registry["object_assignments"][0].update(
                {"expression_id": "cc0-1.0"}
            )
        )
        self.assertTrue(any("must match reviewed CC BY-NC 4.0" in issue for issue in validate(self.root)))

    def test_rights_record_cannot_escape_accession_tree(self) -> None:
        rogue_path = self.root / "records/institutional-practice/rogue-rights.json"
        source_path = next(
            (self.root / "records/accessions/6529NM.2026.001/rights").glob("*.json")
        )
        shutil.copy2(source_path, rogue_path)
        self.mutate_registry(
            lambda registry: registry["object_assignments"][0].update(
                {
                    "rights_record_path":
                        "records/accessions/6529NM.2026.001/rights/../../../institutional-practice/rogue-rights.json"
                }
            )
        )
        issues = validate(self.root)
        self.assertTrue(
            any(
                "rights record is missing or escapes records/" in issue
                for issue in issues
            ),
            issues,
        )

    def test_keys_and_gates_cannot_be_marked_effective_before_mint(self) -> None:
        def mutate(registry: dict) -> None:
            registry["program_notes"][0]["effective_status"] = "effective"

        self.mutate_registry(mutate)
        self.assertNotEqual(validate(self.root), [])

    def test_no_public_license_cannot_become_a_display_ban(self) -> None:
        def mutate(registry: dict) -> None:
            expression = next(
                item for item in registry["expressions"]
                if item["id"] == "in-copyright-no-public-license"
            )
            expression["museum_practice_matrix"]["display_the_work"]["status"] = "separate_basis"

        self.mutate_registry(mutate)
        self.assertTrue(any(
            "practice posture drifted" in issue for issue in validate(self.root)
        ))

    def test_status_uncertainty_cannot_suppress_collection_documentation(self) -> None:
        def mutate(registry: dict) -> None:
            expression = next(
                item for item in registry["expressions"]
                if item["id"] == "rightsstatements-cne"
            )
            expression["museum_practice_matrix"]["publish_online"]["status"] = "separate_basis"

        self.mutate_registry(mutate)
        self.assertTrue(any(
            "blanket bar" in issue for issue in validate(self.root)
        ))

    def test_practical_readings_cannot_collapse_to_generic_copy(self) -> None:
        def mutate(registry: dict) -> None:
            first = registry["expressions"][0]["museum_practice_matrix"]
            first["publish_online"]["note"] = first["display_the_work"]["note"]

        self.mutate_registry(mutate)
        self.assertTrue(any(
            "specific rather than repeated" in issue for issue in validate(self.root)
        ))

    def test_public_copy_rejects_em_dashes(self) -> None:
        guide = self.root / "records/institutional-practice/rights-for-collectors.md"
        guide.write_text(
            guide.read_text(encoding="utf-8") + "\nAn em dash — here.\n",
            encoding="utf-8",
        )
        self.assertTrue(any("contains an em dash" in issue for issue in validate(self.root)))


if __name__ == "__main__":
    unittest.main()
