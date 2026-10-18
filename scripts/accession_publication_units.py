"""Accession publication units shared by the publication inventory and catalog.

Each accession lot that contributes direct records or a responsive
presentation manifest to the visitor corpus is declared here once.
``generate_public_publication_inventory.py`` derives its assembly-control
paths, media-source manifests, and accession media lots from this table, and
``publication_catalog.py`` derives the review-bound record set, presentation
promotion checks, and A-to-B generator-identity paths from the same rows.
Adding an accession is therefore a data change: append one unit.

A unit's ``deterministic_generator_paths`` must name only scripts present in
both the candidate A and reviewed B commits of that accession's release. Units
constructed after this module exists should also list this module, because it
then decides which records the catalog treats as review-bound.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AccessionPublicationUnit:
    """One accession lot's contribution to the visitor publication corpus."""

    accession_lot_id: str
    # Responsive presentation manifest admitted as a public media-source
    # manifest; its derivatives are collected under media/accessions/<lot>/.
    presentation_manifest_path: str
    # Direct accession records (and their Wave status observation) admitted as
    # assembly documents and promoted from review_pending to reviewed in B.
    review_bound_record_paths: tuple[str, ...] = ()
    # Whether the presentation manifest itself carries a review promotion that
    # the catalog must verify between candidate A and reviewed B.
    review_bound_presentation: bool = False
    # Generators that must be byte-identical between candidate A and reviewed
    # B whenever this unit's presentation manifest is in the published corpus.
    deterministic_generator_paths: tuple[str, ...] = ()


def accession_root(accession_lot_id: str) -> str:
    return f"records/accessions/{accession_lot_id}"


def presentation_manifest_path(accession_lot_id: str) -> str:
    return f"{accession_root(accession_lot_id)}/public/presentation-manifest.json"


ACCESSION_PUBLICATION_UNITS: tuple[AccessionPublicationUnit, ...] = (
    AccessionPublicationUnit(
        accession_lot_id="6529NM.2026.002",
        presentation_manifest_path=presentation_manifest_path("6529NM.2026.002"),
    ),
    AccessionPublicationUnit(
        accession_lot_id="6529NM.2026.003",
        presentation_manifest_path=presentation_manifest_path("6529NM.2026.003"),
        review_bound_record_paths=(
            "records/accessions/6529NM.2026.003/accession-certificate.json",
            "records/accessions/6529NM.2026.003/accession-statement.json",
            "records/accessions/6529NM.2026.003/gift-acceptance-authorization.json",
            "records/accessions/6529NM.2026.003/objects/6529NM.2026.003.01.json",
            "records/accessions/6529NM.2026.003/rights/6529NM.2026.003.RIGHTS.01.json",
            "records/accessions/6529NM.2026.003/technical/6529NM.2026.003.01.json",
            "records/proposed-gifts/6529NM-PG-2026-002/wave-status-observation.json",
        ),
        review_bound_presentation=True,
        deterministic_generator_paths=(
            "scripts/finalize_vera_accession.py",
            "scripts/generate_vera_molnar_media.py",
            "scripts/migrate_public_entities.py",
            "scripts/publication_catalog.py",
        ),
    ),
)


def _validate_units(units: tuple[AccessionPublicationUnit, ...]) -> None:
    lots = [unit.accession_lot_id for unit in units]
    if len(lots) != len(set(lots)):
        raise ValueError("accession publication units must not repeat a lot")
    records = [path for unit in units for path in unit.review_bound_record_paths]
    if len(records) != len(set(records)):
        raise ValueError("a review-bound record may belong to only one accession publication unit")
    for unit in units:
        if unit.presentation_manifest_path != presentation_manifest_path(unit.accession_lot_id):
            raise ValueError(f"{unit.accession_lot_id}: presentation manifest must live under its accession public directory")
        for path in unit.review_bound_record_paths:
            if not path.startswith("records/") or not path.endswith(".json"):
                raise ValueError(f"{unit.accession_lot_id}: review-bound record path is not a governed JSON record: {path}")
        if unit.review_bound_presentation and not unit.review_bound_record_paths:
            raise ValueError(f"{unit.accession_lot_id}: a review-bound presentation requires review-bound records")


_validate_units(ACCESSION_PUBLICATION_UNITS)

# Derived views. Consumers import these rather than re-listing paths.
ACCESSION_MEDIA_LOT_IDS: tuple[str, ...] = tuple(unit.accession_lot_id for unit in ACCESSION_PUBLICATION_UNITS)
ACCESSION_PRESENTATION_MANIFEST_PATHS: tuple[str, ...] = tuple(
    unit.presentation_manifest_path for unit in ACCESSION_PUBLICATION_UNITS
)
REVIEW_BOUND_ACCESSION_RECORD_PATHS: tuple[str, ...] = tuple(
    path for unit in ACCESSION_PUBLICATION_UNITS for path in unit.review_bound_record_paths
)
REVIEW_BOUND_PRESENTATION_UNITS: tuple[AccessionPublicationUnit, ...] = tuple(
    unit for unit in ACCESSION_PUBLICATION_UNITS if unit.review_bound_presentation
)
