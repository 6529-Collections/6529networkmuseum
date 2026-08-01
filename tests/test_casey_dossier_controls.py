from __future__ import annotations

import hashlib
import json
import shutil
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
import sys

sys.path.insert(0, str(SCRIPTS))

from canonical import canonicalize  # noqa: E402
from validate import keccak256  # noqa: E402
from validate_casey_dossier import CASEY_ID, OBJECT_TO_DESCRIPTOR, validate  # noqa: E402


class CaseyDossierControlsTests(unittest.TestCase):
    def make_copy(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temporary = tempfile.TemporaryDirectory(prefix="casey-dossier-")
        destination = Path(temporary.name) / "repo"
        shutil.copytree(ROOT, destination, ignore=shutil.ignore_patterns(".git", "__pycache__"))
        self.addCleanup(temporary.cleanup)
        return temporary, destination

    @staticmethod
    def refresh_record(record: dict) -> None:
        payload = record["payload"]
        body = {key: value for key, value in payload.items() if key != "payload_sha256"}
        payload["payload_sha256"] = "sha256:" + hashlib.sha256(canonicalize(body)).hexdigest()
        record["envelope"]["contentHash"]["digest"] = "0x" + keccak256(canonicalize(payload)).hex()

    def mutate_record(self, root: Path, relative: str, mutation: object) -> None:
        path = root / relative
        record = json.loads(path.read_text(encoding="utf-8"))
        mutation(record)
        self.refresh_record(record)
        path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8", newline="\n")

    def test_published_descriptor_dossier_is_valid(self) -> None:
        self.assertEqual(validate(ROOT), [])

    def test_source_binding_descriptor_mapping_urls_and_states_fail_closed(self) -> None:
        mutations = (
            (
                "records/accessions/6529NM.2026.001/accession-statement.json",
                lambda record: record["payload"]["source_manifest"]["casey_collection_snapshot_package"].__setitem__("published_source_commit", "0" * 40),
                "published source package",
            ),
            (
                "records/accessions/6529NM.2026.001/accession-statement.json",
                lambda record: record["payload"]["source_manifest"]["casey_collection_snapshot_package"]["package_manifest"].__setitem__("sha256", "sha256:" + "0" * 64),
                "published source package",
            ),
            (
                "records/accessions/6529NM.2026.001/objects/6529NM.2026.001.01.json",
                lambda record: record["payload"]["trait_analysis"]["descriptor"].__setitem__("path", "evidence/casey-reas-collection-snapshots/descriptors/pre-process.json"),
                "descriptor mapping",
            ),
            (
                "records/accessions/6529NM.2026.001/accession-statement.json",
                lambda record: record["envelope"].__setitem__("uri", "https://github.com/6529-Collections/6529networkmuseum/tree/" + "codex/casey-reas-accession/records/accessions/6529NM.2026.001"),
                "mutable construction-branch URL",
            ),
            (
                "records/accessions/6529NM.2026.001/objects/6529NM.2026.001.01.json",
                lambda record: record["payload"].__setitem__("current_state", "accessioned"),
                "must remain received_onchain",
            ),
        )
        for relative, mutation, expected in mutations:
            with self.subTest(expected=expected):
                _temporary, root = self.make_copy()
                self.mutate_record(root, relative, mutation)
                self.assertTrue(any(expected in issue for issue in validate(root)), validate(root))

    def test_public_pages_and_raw_metadata_are_bound(self) -> None:
        for object_id, slug in OBJECT_TO_DESCRIPTOR.items():
            page = (ROOT / "records" / "accessions" / CASEY_ID / "public" / f"{object_id}.md").read_text(encoding="utf-8")
            self.assertIn("transparent linked descriptor", page)
            self.assertIn(f"descriptors/{slug}.json", page)
            self.assertNotIn("pending linked deliverable", page)
        _temporary, root = self.make_copy()
        raw = root / "evidence" / "casey-reas" / "raw" / "metadata" / f"{CASEY_ID}.01.json"
        raw.write_bytes(raw.read_bytes() + b"\n")
        self.assertTrue(any("raw public metadata manifest binding failed" in issue for issue in validate(root)), validate(root))


if __name__ == "__main__":
    unittest.main()
