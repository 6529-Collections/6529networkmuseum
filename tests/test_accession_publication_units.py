"""The publication pipeline derives per-accession paths from one data table."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import accession_publication_units as units  # noqa: E402
import generate_public_publication_inventory as inventory  # noqa: E402
import migrate_public_entities as migration  # noqa: E402
import publication_catalog as catalog  # noqa: E402

VERA_DIRECT_RECORD_PATHS = (
    "records/accessions/6529NM.2026.003/accession-certificate.json",
    "records/accessions/6529NM.2026.003/accession-statement.json",
    "records/accessions/6529NM.2026.003/gift-acceptance-authorization.json",
    "records/accessions/6529NM.2026.003/objects/6529NM.2026.003.01.json",
    "records/accessions/6529NM.2026.003/rights/6529NM.2026.003.RIGHTS.01.json",
    "records/accessions/6529NM.2026.003/technical/6529NM.2026.003.01.json",
    "records/proposed-gifts/6529NM-PG-2026-002/wave-status-observation.json",
)


class AccessionPublicationUnitTests(unittest.TestCase):
    def test_units_reproduce_the_published_accession_sets(self) -> None:
        self.assertEqual(("6529NM.2026.002", "6529NM.2026.003"), units.ACCESSION_MEDIA_LOT_IDS)
        self.assertEqual(
            (
                "records/accessions/6529NM.2026.002/public/presentation-manifest.json",
                "records/accessions/6529NM.2026.003/public/presentation-manifest.json",
            ),
            units.ACCESSION_PRESENTATION_MANIFEST_PATHS,
        )
        self.assertEqual(VERA_DIRECT_RECORD_PATHS, units.REVIEW_BOUND_ACCESSION_RECORD_PATHS)
        self.assertEqual(["6529NM.2026.003"], [unit.accession_lot_id for unit in units.REVIEW_BOUND_PRESENTATION_UNITS])
        self.assertEqual(
            (
                "scripts/finalize_vera_accession.py",
                "scripts/generate_vera_molnar_media.py",
                "scripts/migrate_public_entities.py",
                "scripts/publication_catalog.py",
            ),
            units.REVIEW_BOUND_PRESENTATION_UNITS[0].deterministic_generator_paths,
        )

    def test_inventory_and_catalog_consume_the_same_rows(self) -> None:
        self.assertTrue(set(VERA_DIRECT_RECORD_PATHS).issubset(inventory.ASSEMBLY_CONTROL_PATHS))
        self.assertEqual(
            (
                "media/programs/6529NM-AP-01/accessibility.json",
                "records/programs/6529NM-AP-01/public/presentation-manifest.json",
                *units.ACCESSION_PRESENTATION_MANIFEST_PATHS,
            ),
            inventory.MEDIA_SOURCE_MANIFEST_PATHS,
        )
        for path in VERA_DIRECT_RECORD_PATHS:
            self.assertTrue(catalog._is_public_graph_record_path(path), path)
        self.assertTrue(catalog._is_public_graph_record_path("records/entities/6529NM-W-0029.json"))
        self.assertTrue(catalog._is_public_graph_record_path("records/proposed-gifts/6529NM-PG-2026-001/wave-status-observation-2026-08-08.json"))
        self.assertFalse(catalog._is_public_graph_record_path("records/accessions/6529NM.2026.002/accession-certificate.json"))
        self.assertFalse(catalog._is_public_graph_record_path("records/accessions/6529NM.2026.003/public/presentation-manifest.json"))

    def test_committed_inventory_is_the_projection_of_the_units(self) -> None:
        committed = json.loads((ROOT / "schemas/public-publication-inventory.json").read_text(encoding="utf-8"))
        self.assertEqual(committed, inventory.generate(ROOT))
        entries = {entry["path"]: entry for entry in committed["entries"]}
        for path in VERA_DIRECT_RECORD_PATHS:
            self.assertEqual("public_assembly_control_document", entries[path]["kind"])
        for path in units.ACCESSION_PRESENTATION_MANIFEST_PATHS:
            self.assertEqual("public_media_source_manifest", entries[path]["kind"])

    def test_a_new_unit_is_a_data_change(self) -> None:
        lot = "6529NM.2026.905"
        unit = units.AccessionPublicationUnit(
            accession_lot_id=lot,
            presentation_manifest_path=units.presentation_manifest_path(lot),
            review_bound_record_paths=(f"records/accessions/{lot}/accession-certificate.json",),
            review_bound_presentation=True,
            deterministic_generator_paths=("scripts/accession_publication_units.py",),
        )
        with tempfile.TemporaryDirectory(prefix="museum-publication-unit-") as temporary:
            root = Path(temporary)
            public = root / "records/accessions" / lot / "public"
            public.mkdir(parents=True)
            derivative = f"media/accessions/{lot}/6529NM-W-9999/source/webp/640.webp"
            (root / derivative).parent.mkdir(parents=True)
            (root / derivative).write_bytes(b"RIFF")
            (public / "web-presentation-authority.md").write_text(
                f"---\nrecord_id: {lot}.DISPLAY-01\nstatus: active\naccession_number: {lot}\n---\n",
                encoding="utf-8",
            )
            (public / "presentation-manifest.json").write_text(
                json.dumps(
                    {
                        "delivery": {
                            "status": "prepared_for_contextual_museum_display_pending_review",
                            "authority_path": f"records/accessions/{lot}/public/web-presentation-authority.md",
                        },
                        "items": [{"presentation": {"derivatives": [{"repository_path": derivative}]}}],
                    }
                ),
                encoding="utf-8",
            )
            with patch.object(inventory, "ACCESSION_MEDIA_LOT_IDS", (lot,)):
                self.assertEqual({derivative}, inventory._accession_media_paths(root))
        record_paths = frozenset((*units.REVIEW_BOUND_ACCESSION_RECORD_PATHS, *unit.review_bound_record_paths))
        with patch.object(catalog, "REVIEW_BOUND_ACCESSION_RECORD_PATH_SET", record_paths):
            self.assertTrue(catalog._is_public_graph_record_path(f"records/accessions/{lot}/accession-certificate.json"))
        with patch.object(catalog, "REVIEW_BOUND_PRESENTATION_UNITS", (*units.REVIEW_BOUND_PRESENTATION_UNITS, unit)):
            self.assertEqual(
                [units.presentation_manifest_path("6529NM.2026.003"), unit.presentation_manifest_path],
                [item.presentation_manifest_path for item in catalog._review_bound_presentation_units({unit.presentation_manifest_path, units.presentation_manifest_path("6529NM.2026.003")})],
            )
            self.assertEqual([], catalog._review_bound_presentation_units(set()))

    def test_unit_table_rejects_ambiguous_rows(self) -> None:
        vera = units.ACCESSION_PUBLICATION_UNITS[1]
        with self.assertRaisesRegex(ValueError, "must not repeat a lot"):
            units._validate_units((vera, vera))
        with self.assertRaisesRegex(ValueError, "only one accession publication unit"):
            units._validate_units((vera, replace(vera, accession_lot_id="6529NM.2026.906", presentation_manifest_path=units.presentation_manifest_path("6529NM.2026.906"))))
        with self.assertRaisesRegex(ValueError, "under its accession public directory"):
            units._validate_units((replace(vera, presentation_manifest_path="records/accessions/6529NM.2026.002/public/presentation-manifest.json"),))
        with self.assertRaisesRegex(ValueError, "requires review-bound records"):
            units._validate_units((replace(vera, review_bound_record_paths=()),))

    def test_public_graph_lot_list_drives_source_resolution(self) -> None:
        self.assertEqual(("6529NM.2026.001", "6529NM.2026.002", "6529NM.2026.003"), migration.PUBLIC_GRAPH_ACCESSION_LOT_IDS)
        self.assertEqual("records/accessions/6529NM.2026.003/objects/6529NM.2026.003.01.json", migration.source_repository_path("6529NM.2026.003.01"))
        self.assertEqual("records/accessions/6529NM.2026.002/rights/6529NM.2026.002.RIGHTS.05.json", migration.source_repository_path("6529NM.2026.002.RIGHTS.05"))
        self.assertEqual("records/accessions/6529NM.2026.001/technical/6529NM.2026.001.07.json", migration.source_repository_path("6529NM.2026.001.COND.07"))
        self.assertEqual("6529NM.2026.905.01", migration.source_repository_path("6529NM.2026.905.01"))
        with self.assertRaises(ValueError):
            migration.source_record_evidence_class("6529NM.2026.905.01")
        with patch.object(migration, "PUBLIC_GRAPH_ACCESSION_LOT_IDS", (*migration.PUBLIC_GRAPH_ACCESSION_LOT_IDS, "6529NM.2026.905")):
            self.assertEqual("records/accessions/6529NM.2026.905/objects/6529NM.2026.905.01.json", migration.source_repository_path("6529NM.2026.905.01"))
            self.assertEqual("records/accessions/6529NM.2026.905/technical/6529NM.2026.905.01.json", migration.source_repository_path("6529NM.2026.905.COND.01"))
            self.assertEqual("B", migration.source_record_evidence_class("6529NM.2026.905.01"))

    def test_accession_source_records_and_construction_scopes_are_data(self) -> None:
        self.assertEqual("records/accessions/6529NM.2026.003/gift-acceptance-authorization.json", migration.source_repository_path("6529NM.2026.003.GAA-01"))
        self.assertEqual("records/accessions/6529NM.2026.002/accession-certificate.json", migration.source_repository_path("6529NM-ACC-2026-002"))
        self.assertEqual("records/proposed-gifts/6529NM-PG-2026-002/proposal.json", migration.source_repository_path("6529NM-PG-2026-002.OBJ-001"))
        self.assertEqual("records/governance/decisions.json", migration.source_repository_path("6529NM-GOV-1052812"))
        with patch.dict(migration.GOVERNANCE_RECORD_PATHS, {"6529NM-GOV-9999999": "records/governance/6529NM-GOV-9999999.json"}):
            self.assertEqual("records/governance/6529NM-GOV-9999999.json", migration.source_repository_path("6529NM-GOV-9999999"))
        with patch.object(migration, "PROPOSAL_SOURCE_PATHS", (*migration.PROPOSAL_SOURCE_PATHS, ("6529NM-PA-2026-905", "records/proposed-acquisitions/6529NM-PA-2026-905/proposal.json"))):
            self.assertEqual("records/proposed-acquisitions/6529NM-PA-2026-905/proposal.json", migration.source_repository_path("6529NM-PA-2026-905"))
            self.assertEqual("B", migration.source_record_evidence_class("6529NM-PA-2026-905"))
        self.assertEqual((migration.VERA_CONSTRUCTOR_ID, migration.VERA_AT), migration.construction_scope("6529NM-W-0029"))
        self.assertEqual((migration.CONSTRUCTOR_ID, migration.GENERATED_AT), migration.construction_scope("6529NM-W-0001"))


if __name__ == "__main__":
    unittest.main()
