from __future__ import annotations

import copy
import hashlib
import json
import os
import shutil
import stat
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
import sys

sys.path.insert(0, str(SCRIPTS))

from canonical import canonicalize  # noqa: E402
from acquire_casey_custody_audit import (  # noqa: E402
    AuditError,
    abi_word_address,
    main as acquire_custody_main,
    prepare_empty_output,
)
from build_casey_diligence_manifest import (  # noqa: E402
    ManifestError,
    _checked_info as checked_diligence_info,
    _files as diligence_files,
    build as build_diligence_manifest,
)
from finalize_casey_accession import REVIEW_AT, prior_event_for_replacement  # noqa: E402
from validate import keccak256, load_schemas, validate_gift_acceptance_authorization, validate_visual_observation, validator_for  # noqa: E402
from validate_casey_dossier import (  # noqa: E402
    CASEY_ID,
    GIFT_AUTHORIZATION_ID,
    OBJECT_TO_DESCRIPTOR,
    VISUAL_OBSERVATION_ID,
    validate,
    _abi_address,
    _validate_diligence_rpc_evidence,
    validate_evidence_manifest,
    validate_post_accession_diligence,
)


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

    def test_post_accession_diligence_is_valid(self) -> None:
        self.assertEqual(validate_post_accession_diligence(ROOT), [])

    def test_post_accession_diligence_fails_closed(self) -> None:
        _, root = self.make_copy()
        path = root / "records/accessions/6529NM.2026.001/post-accession-diligence.json"
        record = json.loads(path.read_text(encoding="utf-8"))
        record["title_and_authority"]["determination"] = "pending"
        record["conclusion"]["completion_blockers"] = ["future reviewer"]
        path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8", newline="\n")

        issues = validate_post_accession_diligence(root)
        self.assertTrue(any("must confirm title, bind custody and OFAC evidence" in issue for issue in issues))

    def test_post_accession_diligence_detects_evidence_mutation(self) -> None:
        _, root = self.make_copy()
        path = root / "evidence/casey-reas-diligence/custody-audit-2026-08-02.json"
        evidence = json.loads(path.read_text(encoding="utf-8"))
        evidence["custody_address"] = "0x0000000000000000000000000000000000000000"
        path.write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8", newline="\n")

        issues = validate_post_accession_diligence(root)
        self.assertTrue(any("evidence manifest must bind every package file exactly" in issue for issue in issues))

    def test_diligence_raw_rpc_semantic_rewrite_is_rejected(self) -> None:
        _, root = self.make_copy()
        package = root / "evidence/casey-reas-diligence"
        custody_path = package / "custody-audit-2026-08-02.json"
        custody = json.loads(custody_path.read_text(encoding="utf-8"))
        target_id = "owner:6529NM.2026.001.01"
        reference = next(
            item
            for item in custody["responses"]
            if json.loads((package / item["path"]).read_text(encoding="utf-8"))["id"] == target_id
        )
        original = package / reference["path"]
        response = json.loads(original.read_text(encoding="utf-8"))
        response["result"] = "0x" + "0" * 64
        payload = (json.dumps(response, separators=(",", ":")) + "\n").encode("utf-8")
        digest = hashlib.sha256(payload).hexdigest()
        replacement = original.with_name(f"sha256-{digest}.json")
        replacement.write_bytes(payload)
        original.unlink()
        reference.update(path=replacement.relative_to(package).as_posix(), sha256=f"sha256:{digest}", size=len(payload))
        custody["safe_fetch_observations"][target_id]["byte_sha256"] = digest
        custody["safe_fetch_observations"][target_id]["byte_length"] = len(payload)

        issues = _validate_diligence_rpc_evidence(package, custody)
        self.assertTrue(any("raw owner/approval response" in issue for issue in issues), issues)

    def test_diligence_eip1898_selector_mutation_is_rejected(self) -> None:
        package = ROOT / "evidence/casey-reas-diligence"
        custody = json.loads((package / "custody-audit-2026-08-02.json").read_text(encoding="utf-8"))
        custody["block"]["state_selector"]["requireCanonical"] = False
        issues = _validate_diligence_rpc_evidence(package, custody)
        self.assertTrue(any("request/transport binding" in issue or "exact finalized block hash" in issue for issue in issues), issues)

    def test_diligence_ofac_subject_role_set_is_exact(self) -> None:
        _, root = self.make_copy()
        path = root / "evidence/casey-reas-diligence/ofac-address-screening-2026-08-02.json"
        ofac = json.loads(path.read_text(encoding="utf-8"))
        ofac["screened_addresses"][0]["role"] = "uncontrolled_role"
        path.write_text(json.dumps(ofac, indent=2) + "\n", encoding="utf-8", newline="\n")
        issues = validate_post_accession_diligence(root)
        self.assertTrue(any("OFAC evidence must retain" in issue for issue in issues), issues)

    def test_diligence_manifest_rejects_symlinked_evidence(self) -> None:
        _, root = self.make_copy()
        package = root / "evidence/casey-reas-diligence"
        link = package / "raw/rpc/symlinked-response.json"
        target = next((package / "raw/rpc").glob("sha256-*.json"))
        try:
            os.symlink(target, link)
        except (OSError, NotImplementedError) as error:
            self.skipTest(f"filesystem does not permit symlink creation: {error}")
        with self.assertRaisesRegex(ManifestError, "symlink or reparse point"):
            build_diligence_manifest(package)

    def test_diligence_manifest_rejects_symlinked_directory(self) -> None:
        _, root = self.make_copy()
        package = root / "evidence/casey-reas-diligence"
        target = root / "linked-evidence-target"
        target.mkdir()
        (target / "response.json").write_text("{}\n", encoding="utf-8")
        link = package / "raw/linked-directory"
        try:
            os.symlink(target, link, target_is_directory=True)
        except (OSError, NotImplementedError) as error:
            self.skipTest(f"filesystem does not permit directory symlink creation: {error}")
        with self.assertRaisesRegex(ManifestError, "symlink or reparse point"):
            build_diligence_manifest(package)

    def test_diligence_manifest_retains_nested_manifest_named_evidence(self) -> None:
        _, root = self.make_copy()
        package = root / "evidence/casey-reas-diligence"
        nested = package / "raw/auxiliary/nested/manifest.json"
        nested.parent.mkdir(parents=True)
        nested.write_text("{}\n", encoding="utf-8")
        manifest = build_diligence_manifest(package)
        paths = {entry["path"] for entry in manifest["entries"]}
        self.assertIn("raw/auxiliary/nested/manifest.json", paths)

    def test_diligence_manifest_rejects_windows_reparse_point(self) -> None:
        package = ROOT / "evidence/casey-reas-diligence"
        reparse_info = SimpleNamespace(st_mode=stat.S_IFREG, st_file_attributes=0x400)
        with mock.patch("build_casey_diligence_manifest.os.lstat", return_value=reparse_info):
            with self.assertRaisesRegex(ManifestError, "symlink or reparse point"):
                checked_diligence_info(package / "raw/rpc/reparse.json", package)

    def test_diligence_manifest_rejects_non_regular_entry(self) -> None:
        package = ROOT / "evidence/casey-reas-diligence"
        directory_info = SimpleNamespace(st_mode=stat.S_IFDIR, st_file_attributes=0)
        pipe_info = SimpleNamespace(st_mode=stat.S_IFIFO, st_file_attributes=0)
        with (
            mock.patch("build_casey_diligence_manifest.os.walk", return_value=[(str(package), [], ["pipe"])]),
            mock.patch("build_casey_diligence_manifest.os.lstat", side_effect=[directory_info, directory_info, pipe_info]),
        ):
            with self.assertRaisesRegex(ManifestError, "non-regular file"):
                diligence_files(package)

    def test_custody_acquisition_refuses_non_empty_output(self) -> None:
        with tempfile.TemporaryDirectory(prefix="casey-custody-output-") as temporary:
            output = Path(temporary)
            (output / "existing.json").write_text("{}\n", encoding="utf-8")
            with self.assertRaisesRegex(AuditError, "output directory must be empty"):
                prepare_empty_output(output)

    def test_custody_acquisition_creates_new_empty_output(self) -> None:
        with tempfile.TemporaryDirectory(prefix="casey-custody-parent-") as temporary:
            output = Path(temporary) / "new-output"
            prepare_empty_output(output)
            self.assertTrue(output.is_dir())
            self.assertEqual(list(output.iterdir()), [])

    def test_custody_acquisition_accepts_existing_empty_output(self) -> None:
        with tempfile.TemporaryDirectory(prefix="casey-custody-output-") as temporary:
            output = Path(temporary)
            prepare_empty_output(output)
            self.assertEqual(list(output.iterdir()), [])

    def test_custody_acquisition_refuses_symlinked_output(self) -> None:
        with tempfile.TemporaryDirectory(prefix="casey-custody-parent-") as temporary:
            parent = Path(temporary)
            target = parent / "target"
            target.mkdir()
            output = parent / "linked-output"
            try:
                os.symlink(target, output, target_is_directory=True)
            except (OSError, NotImplementedError) as error:
                self.skipTest(f"filesystem does not permit directory symlink creation: {error}")
            with self.assertRaisesRegex(AuditError, "symlink or reparse point"):
                prepare_empty_output(output)

    def test_custody_acquisition_requires_output_argument(self) -> None:
        with mock.patch("sys.stderr"):
            with self.assertRaises(SystemExit) as error:
                acquire_custody_main([])
        self.assertEqual(error.exception.code, 2)

    def test_abi_address_decoders_reject_non_zero_left_padding(self) -> None:
        malformed = "0x" + "1" * 24 + "2" * 40
        self.assertIsNone(_abi_address(malformed))
        with self.assertRaisesRegex(AuditError, "non-zero left padding"):
            abi_word_address(malformed)

    def test_revision_two_schema_requires_amendment_history_entry(self) -> None:
        _vocabularies, _envelope, store = load_schemas(ROOT)
        schema = json.loads((ROOT / "schemas/post-accession-diligence.schema.json").read_text(encoding="utf-8"))
        validator = validator_for(schema, store)
        record = json.loads(
            (ROOT / "records/accessions/6529NM.2026.001/post-accession-diligence.json").read_text(encoding="utf-8")
        )
        record["amendment_history"] = []
        errors = list(validator.iter_errors(record))
        self.assertTrue(any("should be non-empty" in error.message for error in errors), errors)

    def test_live_accession_schemas_reject_undeclared_nested_fields(self) -> None:
        _vocabularies, _envelope, store = load_schemas(ROOT)
        cases = (
            (
                "accession-lot.schema.json",
                "records/accessions/6529NM.2026.001/accession-statement.json",
                lambda payload: payload["controlled_decision"].__setitem__("unreviewed_magic", True),
            ),
            (
                "object-record.schema.json",
                "records/accessions/6529NM.2026.001/objects/6529NM.2026.001.01.json",
                lambda payload: payload["artist"].__setitem__("unreviewed_magic", True),
            ),
            (
                "accession-lot.schema.json",
                "records/accessions/6529NM.2026.001/accession-statement.json",
                lambda payload: payload["provenance_schedule"]["verification_method"].__setitem__("unreviewed_magic", True),
            ),
        )
        for schema_name, record_path, mutation in cases:
            with self.subTest(schema=schema_name):
                schema = json.loads((ROOT / "schemas" / schema_name).read_text(encoding="utf-8"))
                validator = validator_for(schema, store)
                record = json.loads((ROOT / record_path).read_text(encoding="utf-8"))
                payload = copy.deepcopy(record["payload"])
                self.assertEqual([], list(validator.iter_errors(payload)))
                mutation(payload)
                errors = list(validator.iter_errors(payload))
                self.assertTrue(errors)
                self.assertTrue(any("unreviewed_magic" in error.message for error in errors), errors)

    def test_live_accession_schemas_contain_no_open_object_nodes(self) -> None:
        def open_nodes(value: object, path: str = "$") -> list[str]:
            found: list[str] = []
            if isinstance(value, dict):
                if value.get("type") == "object" and value.get("additionalProperties") is True:
                    found.append(path)
                for key, child in value.items():
                    found.extend(open_nodes(child, f"{path}.{key}"))
            elif isinstance(value, list):
                for index, child in enumerate(value):
                    found.extend(open_nodes(child, f"{path}[{index}]"))
            return found

        for schema_name in (
            "accession-lot.schema.json",
            "object-record.schema.json",
            "post-accession-diligence.schema.json",
            "transaction-provenance.schema.json",
        ):
            with self.subTest(schema=schema_name):
                schema = json.loads((ROOT / "schemas" / schema_name).read_text(encoding="utf-8"))
                self.assertEqual([], open_nodes(schema))

    def test_finished_accession_decisions_fail_closed(self) -> None:
        mutations = (
            (
                "records/accessions/6529NM.2026.001/accession-statement.json",
                lambda record: record["payload"].__setitem__("remaining_gates", ["placeholder"]),
                "completed permanent-collection accession",
            ),
            (
                "records/accessions/6529NM.2026.001/accession-statement.json",
                lambda record: record["payload"]["controlled_decision"].__setitem__("completion_status", "not_complete"),
                "completed permanent-collection accession",
            ),
            (
                "records/accessions/6529NM.2026.001/accession-statement.json",
                lambda record: record["payload"]["public_inventory"][0].__setitem__("status", "received_onchain"),
                "public inventory must place all seven",
            ),
            (
                "records/accessions/6529NM.2026.001/accession-statement.json",
                lambda record: record["payload"]["donation_rights_schedule"]["rights_matrix"][0].__setitem__("grant_status", "unspecified"),
                "lot-level donation, title, and rights schedule",
            ),
            (
                "records/accessions/6529NM.2026.001/accession-statement.json",
                lambda record: record["payload"]["preservation_manifest"].__setitem__("pending", ["future reviewer"]),
                "active stewardship actions rather than an intake-stage pending list",
            ),
            (
                "records/accessions/6529NM.2026.001/accession-statement.json",
                lambda record: record["payload"]["preservation_manifest"]["active_stewardship_actions"].__setitem__(0, None),
                "active stewardship actions rather than an intake-stage pending list",
            ),
            (
                "records/accessions/6529NM.2026.001/accession-statement.json",
                lambda record: record["payload"]["ongoing_stewardship_actions"].__setitem__(0, "future reviewer"),
                "concrete active preservation",
            ),
            (
                "records/accessions/6529NM.2026.001/accession-statement.json",
                lambda record: record["payload"].__setitem__("references", [VISUAL_OBSERVATION_ID]),
                "must link the gift authorization",
            ),
            (
                "records/accessions/6529NM.2026.001/accession-certificate.json",
                lambda record: record["payload"]["title_bindings"][0].__setitem__("status", "pending"),
                "execute one exact title binding",
            ),
            (
                "records/accessions/6529NM.2026.001/accession-certificate.json",
                lambda record: record["payload"]["title_bindings"][0].__setitem__("instrument_sha256", "sha256:" + "0" * 64),
                "execute one exact title binding",
            ),
            (
                "records/accessions/6529NM.2026.001/accession-certificate.json",
                lambda record: record["payload"]["events"][4]["custody_paths"].pop(),
                "one on-chain custody path",
            ),
            (
                "records/accessions/6529NM.2026.001/accession-certificate.json",
                lambda record: record["payload"]["events"][4].__setitem__("source_occurred_at", "2026-08-01T22:55:00Z"),
                "distinguish on-chain receipt",
            ),
            (
                "records/accessions/6529NM.2026.001/accession-certificate.json",
                lambda record: record["payload"]["events"][2]["evidence_refs"][0].pop("sha256"),
                "immutably bind the exact reviewed accession-lot bytes",
            ),
            (
                "records/accessions/6529NM.2026.001/objects/6529NM.2026.001.01.json",
                lambda record: record["payload"].__setitem__("current_state", "received_onchain"),
                "must end in accessioned state",
            ),
            (
                "records/accessions/6529NM.2026.001/objects/6529NM.2026.001.01.json",
                lambda record: record["payload"].__setitem__("state_history", []),
                "must end in accessioned state",
            ),
            (
                "records/accessions/6529NM.2026.001/objects/6529NM.2026.001.01.json",
                lambda record: record["payload"]["state_history"][0].__setitem__("observed_at", "2026-08-01T13:25:47Z"),
                "must end in accessioned state",
            ),
            (
                "records/accessions/6529NM.2026.001/technical/6529NM.2026.001.01.json",
                lambda record: record["payload"].__setitem__("reviewer", None),
                "must be substantively reviewed",
            ),
            (
                "records/accessions/6529NM.2026.001/objects/6529NM.2026.001.01.json",
                lambda record: record["payload"]["title_binding"].__setitem__("status", "pending"),
                "executed transaction-bound title declaration",
            ),
            (
                "records/accessions/6529NM.2026.001/objects/6529NM.2026.001.01.json",
                lambda record: record["payload"]["rights"]["exhibition"].__setitem__("grant_status", "unspecified"),
                "complete conditional CC BY-NC 4.0 rights matrix",
            ),
            (
                "records/accessions/6529NM.2026.001/technical/6529NM.2026.001.01.json",
                lambda record: record["payload"]["assessments"].__setitem__("render", "not_assessed"),
                "complete pass-with-conditions outcome",
            ),
            (
                "records/accessions/6529NM.2026.001/technical/6529NM.2026.001.01.json",
                lambda record: next(item for item in record["payload"]["evidence_refs"] if item.get("label") == "Controlled visual observation").pop("sha256"),
                "bind the controlled visual observation bytes",
            ),
            (
                "records/accessions/6529NM.2026.001/rights/6529NM.2026.001.RIGHTS.01.json",
                lambda record: next(item for item in record["payload"]["evidence_refs"] if item.get("label") == "Reviewed title and rights determination").__setitem__("sha256", "sha256:" + "0" * 64),
                "match the object matrix and copyright boundary",
            ),
            (
                "records/accessions/6529NM.2026.001/visual-observation-record.json",
                lambda record: record["payload"]["objects"][0]["static_capture"]["retention"].__setitem__("bytes_retained_in_public_repository", True),
                "rights-cleared future capture",
            ),
            (
                "records/accessions/6529NM.2026.001/gift-acceptance-authorization.json",
                lambda record: record["payload"]["completion_boundary"].__setitem__("accession_status", "not_complete"),
                "full gift and its completed accession resolution",
            ),
            (
                "records/accessions/6529NM.2026.001/gift-acceptance-authorization.json",
                lambda record: record["payload"]["assets"][0].__setitem__("token_id", "100000724"),
                "full gift and its completed accession resolution",
            ),
            (
                "records/accessions/6529NM.2026.001/accession-statement.json",
                lambda record: record["payload"]["object_identities"][0].pop("contract"),
                "full gift and its completed accession resolution",
            ),
            (
                "records/accessions/6529NM.2026.001/gift-acceptance-authorization.json",
                lambda record: record["payload"]["governing_basis"][0].__setitem__("observed_at", "2026-08-02T00:00:00Z"),
                "state when and from which reviewed register",
            ),
            (
                "records/accessions/6529NM.2026.001/gift-acceptance-authorization.json",
                lambda record: record["payload"]["governing_basis"][0].update({"decision_id": "6529NM-GOV-1052148", "wave_serial": 1052148}),
                "must bind exactly decisions 1052156 and 1052812",
            ),
            (
                "records/accessions/6529NM.2026.001/gift-acceptance-authorization.json",
                lambda record: record["payload"]["governing_basis"].pop(),
                "must bind exactly decisions 1052156 and 1052812",
            ),
            (
                "records/accessions/6529NM.2026.001/gift-acceptance-authorization.json",
                lambda record: record["payload"]["governing_basis"].append(copy.deepcopy(record["payload"]["governing_basis"][0])),
                "must bind exactly decisions 1052156 and 1052812",
            ),
            (
                "records/accessions/6529NM.2026.001/accession-statement.json",
                lambda record: record["payload"]["source_manifest"]["casey_collection_snapshot_package"].__setitem__("published_source_commit", "0" * 40),
                "published source package",
            ),
            (
                "records/accessions/6529NM.2026.001/objects/6529NM.2026.001.01.json",
                lambda record: record["payload"]["trait_analysis"]["descriptor"].__setitem__("path", "evidence/casey-reas-collection-snapshots/descriptors/pre-process.json"),
                "descriptor mapping",
            ),
            (
                "records/accessions/6529NM.2026.001/objects/6529NM.2026.001.01.json",
                lambda record: record["payload"]["generator_snapshot"].__setitem__("dependency_observed", "p5.js latest"),
                "generator response, dependency, and complete interaction map",
            ),
            (
                "records/accessions/6529NM.2026.001/objects/6529NM.2026.001.01.json",
                lambda record: record["payload"]["generator_snapshot"].__setitem__("sha256", "sha256:" + "0" * 64),
                "generator response, dependency, and complete interaction map",
            ),
            (
                "records/accessions/6529NM.2026.001/objects/6529NM.2026.001.01.json",
                lambda record: record["payload"]["display"].__setitem__("manifest_uri", "https://github.com/6529-Collections/6529networkmuseum/blob/main/records/accessions/6529NM.2026.001/public/technical-and-condition-review.md"),
                "payload evidence URL must be commit-pinned",
            ),
            (
                "records/accessions/6529NM.2026.001/objects/6529NM.2026.001.04.json",
                lambda record: record["payload"]["generator_snapshot"]["interaction_map"].pop(),
                "generator response, dependency, and complete interaction map",
            ),
            (
                "records/accessions/6529NM.2026.001/objects/6529NM.2026.001.05.json",
                lambda record: record["payload"]["generator_snapshot"].__setitem__("automatic_behavior", "Runs forever."),
                "generator response, dependency, and complete interaction map",
            ),
            (
                "records/accessions/6529NM.2026.001/objects/6529NM.2026.001.06.json",
                lambda record: record["payload"]["project"]["combination_structure"].__setitem__("invocation_zero_code", "000000"),
                "923-combination / 924-token distinction",
            ),
            (
                "records/accessions/6529NM.2026.001/objects/6529NM.2026.001.07.json",
                lambda record: record["payload"]["generator_snapshot"].pop("documentation_discrepancies"),
                "generator response, dependency, and complete interaction map",
            ),
        )
        for relative, mutation, expected in mutations:
            with self.subTest(expected=expected):
                _temporary, root = self.make_copy()
                self.mutate_record(root, relative, mutation)
                found = validate(root, history_root=ROOT)
                self.assertTrue(any(expected in issue for issue in found), found)

    def test_finalizer_requires_a_prior_event_to_supersede(self) -> None:
        current_only = [
            {
                "event_id": "6529NM.TEST.EVENT.rights_amendment.20260802T063000Z",
                "event_type": "rights_amendment",
                "occurred_at": REVIEW_AT,
            }
        ]
        with self.assertRaisesRegex(ValueError, "no prior event remains"):
            prior_event_for_replacement(current_only, "rights_amendment", Path("rights.json"))

    def test_generator_transcript_and_descriptor_review_fail_closed(self) -> None:
        _temporary, root = self.make_copy()
        transcript_path = root / "evidence" / "casey-reas" / "generator-observations.json"
        transcript = json.loads(transcript_path.read_text(encoding="utf-8"))
        transcript["objects"][0]["dependency"] = "p5.js latest"
        transcript_path.write_text(json.dumps(transcript, indent=2) + "\n", encoding="utf-8", newline="\n")
        manifest_path = root / "evidence" / "casey-reas" / "manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        entry = next(item for item in manifest["entries"] if item["path"] == "generator-observations.json")
        entry["sha256"] = hashlib.sha256(transcript_path.read_bytes()).hexdigest()
        entry["size"] = transcript_path.stat().st_size
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8", newline="\n")
        issues = validate(root, history_root=ROOT)
        self.assertTrue(any("independently reviewed bytes" in issue for issue in issues), issues)

        _temporary_two, root_two = self.make_copy()
        ledger_path = root_two / "evidence" / "casey-reas-collection-snapshots" / "pending-descriptors.json"
        ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
        ledger["review"] = None
        ledger_path.write_text(json.dumps(ledger, indent=2) + "\n", encoding="utf-8", newline="\n")
        issues = validate(root_two, history_root=ROOT)
        self.assertTrue(any("completed independent package review" in issue for issue in issues), issues)

    def test_public_pages_and_raw_metadata_are_bound(self) -> None:
        for object_id, slug in OBJECT_TO_DESCRIPTOR.items():
            page = (ROOT / "records" / "accessions" / CASEY_ID / "public" / f"{object_id}.md").read_text(encoding="utf-8")
            self.assertIn("transparent linked descriptor", page)
            self.assertIn(f"descriptors/{slug}.json", page)
            self.assertIn("The work is `accessioned`.", page)
            self.assertIn("title and rights review", page)
            self.assertIn("Technical condition passes with amber preservation conditions", page)
            self.assertIn("no OpenSea or marketplace rarity", page)
            self.assertNotIn("review remain pending", page)
            self.assertIn("artist and practice profile", page)
            self.assertIn("collection essay", page)
            self.assertIn("../visual-observation-record.json", page)
            self.assertNotIn("pending linked deliverable", page)
        _temporary, root = self.make_copy()
        raw = root / "evidence" / "casey-reas" / "raw" / "metadata" / f"{CASEY_ID}.01.json"
        raw.write_bytes(raw.read_bytes() + b"\n")
        self.assertTrue(any("raw public metadata manifest binding failed" in issue for issue in validate(root, history_root=ROOT)), validate(root, history_root=ROOT))

    def test_raw_receipt_semantically_binds_the_seven_accession_identities(self) -> None:
        _temporary, root = self.make_copy()
        relative = "raw/rpc/eth-get-transaction-receipt-0xbdde33b32d4b70335b10cbd37c0b00a027844f14c900d82aa4f75b7a7b390498.json"
        receipt_path = root / "evidence" / "casey-reas" / relative
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        transfer = next(log for log in receipt["result"]["logs"] if log["topics"][0].startswith("0xddf252"))
        transfer["topics"][3] = "0x" + format(int(transfer["topics"][3], 16) + 1, "064x")
        receipt_path.write_text(json.dumps(receipt, separators=(",", ":")) + "\n", encoding="utf-8", newline="\n")
        manifest_path = root / "evidence" / "casey-reas" / "manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        entry = next(item for item in manifest["entries"] if item["path"] == relative)
        entry["sha256"] = hashlib.sha256(receipt_path.read_bytes()).hexdigest()
        entry["size"] = receipt_path.stat().st_size
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8", newline="\n")
        issues = validate(root, history_root=ROOT)
        self.assertTrue(any("raw RPC receipt transfer schedule must match" in issue for issue in issues), issues)

    def test_evidence_manifest_missing_path_reports_instead_of_aborting(self) -> None:
        _temporary, root = self.make_copy()
        manifest_path = root / "evidence" / "casey-reas" / "manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["entries"][0].pop("path")
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8", newline="\n")
        issues = validate_evidence_manifest(root)
        self.assertTrue(any("entry has no path" in issue for issue in issues), issues)

    def test_raw_receipt_acquisition_metadata_is_semantically_bound(self) -> None:
        _temporary, root = self.make_copy()
        acquisition_path = root / "evidence" / "casey-reas" / "raw" / "rpc" / "receipt-acquisition.json"
        acquisition = json.loads(acquisition_path.read_text(encoding="utf-8"))
        acquisition["request"]["rpc_method"] = "eth_getTransactionByHash"
        acquisition_path.write_text(json.dumps(acquisition, indent=2) + "\n", encoding="utf-8", newline="\n")
        issues = validate(root, history_root=ROOT)
        self.assertTrue(any("raw RPC receipt acquisition metadata is invalid" in issue for issue in issues), issues)

    def test_historical_release_requires_full_git_history(self) -> None:
        with tempfile.TemporaryDirectory(prefix="casey-history-") as directory:
            issues = validate(ROOT, history_root=Path(directory))
        self.assertTrue(any("immutable publication evidence cannot be verified" in issue for issue in issues), issues)

    def test_gift_schema_is_generic_but_casey_binding_is_exact(self) -> None:
        schema = json.loads((ROOT / "schemas" / "gift-acceptance-authorization.schema.json").read_text(encoding="utf-8"))
        rendered = json.dumps(schema, sort_keys=True)
        self.assertFalse(schema["unevaluatedProperties"])
        self.assertNotIn("punk6529", rendered)
        self.assertNotIn("networkmuseum.6529.eth", rendered)
        self.assertNotIn('"maxItems": 7', rendered)
        source_types = schema["$defs"]["authorityDeclaration"]["properties"]["source_type"]["enum"]
        authority_bases = schema["$defs"]["institutionalDecisionAuthority"]["properties"]["authority_basis"]["enum"]
        governing_basis = schema["allOf"][1]["properties"]["governing_basis"]
        self.assertGreater(len(source_types), 1)
        self.assertGreater(len(authority_bases), 1)
        self.assertEqual(1, governing_basis["minItems"])
        self.assertNotIn("maxItems", governing_basis)
        record = json.loads((ROOT / "records" / "accessions" / CASEY_ID / "gift-acceptance-authorization.json").read_text(encoding="utf-8"))
        self.assertEqual(GIFT_AUTHORIZATION_ID, record["payload"]["record_id"])
        self.assertEqual("formally_accepted", record["payload"]["institutional_decision_authority"]["decision_status"])
        self.assertEqual("reviewed", record["payload"]["institutional_decision_authority"]["documentation_qa_status"])
        self.assertEqual("complete", record["payload"]["completion_boundary"]["accession_status"])

    def test_generic_gift_semantics_reject_projected_duplicates_and_count_mismatch(self) -> None:
        record = json.loads((ROOT / "records" / "accessions" / CASEY_ID / "gift-acceptance-authorization.json").read_text(encoding="utf-8"))
        payload = record["payload"]
        mutations = (
            (lambda value: value["assets"][1].__setitem__("object_id", value["assets"][0]["object_id"]), "duplicate object_id"),
            (lambda value: value["assets"][1].__setitem__("caip19", value["assets"][0]["caip19"]), "duplicate caip19"),
            (lambda value: (value["assets"][1].__setitem__("contract", value["assets"][0]["contract"]), value["assets"][1].__setitem__("token_id", value["assets"][0]["token_id"])), "duplicate contract+token_id"),
            (lambda value: value["assets"][1].__setitem__("custody_receipt_log", value["assets"][0]["custody_receipt_log"]), "duplicate custody_receipt_log"),
            (lambda value: value["custody_receipt"].__setitem__("transfer_count", 6), "transfer_count must equal assets.length"),
        )
        for mutation, expected in mutations:
            with self.subTest(expected=expected):
                candidate = copy.deepcopy(payload)
                mutation(candidate)
                issues = validate_gift_acceptance_authorization(candidate)
                self.assertTrue(any(expected in issue for issue in issues), issues)

    def test_generic_gift_semantics_reports_unhashable_duplicate_projection(self) -> None:
        record = json.loads((ROOT / "records" / "accessions" / CASEY_ID / "gift-acceptance-authorization.json").read_text(encoding="utf-8"))
        candidate = copy.deepcopy(record["payload"])
        candidate["assets"][0]["object_id"] = ["malformed"]
        candidate["assets"][1]["object_id"] = ["malformed"]
        issues = validate_gift_acceptance_authorization(candidate)
        self.assertTrue(any("duplicate object_id" in issue for issue in issues), issues)

    def test_generic_gift_schema_accepts_non_wave_basis_and_rejects_malformed_unions(self) -> None:
        _vocabularies, _envelope, store = load_schemas(ROOT)
        schema = json.loads((ROOT / "schemas" / "gift-acceptance-authorization.schema.json").read_text(encoding="utf-8"))
        validator = validator_for(schema, store)
        record = json.loads((ROOT / "records" / "accessions" / CASEY_ID / "gift-acceptance-authorization.json").read_text(encoding="utf-8"))
        payload = record["payload"]
        non_wave_basis = {
            "basis_type": "delegated_authority_record",
            "record_id": "6529NM-AUTH-DELEGATION-001",
            "title": "Delegated gift-acceptance authority",
            "authority_effect": "delegates_acceptance_authority",
            "effective_at": "2026-01-01T00:00:00Z",
            "source_uri": "https://example.org/museum/authority/6529NM-AUTH-DELEGATION-001",
        }
        candidate = copy.deepcopy(payload)
        candidate["governing_basis"] = [non_wave_basis]
        candidate["institutional_decision_authority"]["authority_basis"] = "delegated_accession_authority"
        self.assertEqual([], list(validator.iter_errors(candidate)))
        malformed = []
        wrong_branch = copy.deepcopy(payload["governing_basis"][0])
        wrong_branch["basis_type"] = "delegated_authority_record"
        malformed.append(wrong_branch)
        missing_wave_field = copy.deepcopy(payload["governing_basis"][0])
        missing_wave_field.pop("drop_id")
        malformed.append(missing_wave_field)
        missing_record_effect = copy.deepcopy(non_wave_basis)
        missing_record_effect.pop("authority_effect")
        malformed.append(missing_record_effect)
        for basis in malformed:
            with self.subTest(basis=basis["basis_type"]):
                candidate = copy.deepcopy(payload)
                candidate["governing_basis"] = [basis]
                self.assertTrue(list(validator.iter_errors(candidate)))

    def test_visual_observation_generic_relationships_and_closed_schema(self) -> None:
        schema = json.loads((ROOT / "schemas" / "visual-observation.schema.json").read_text(encoding="utf-8"))
        self.assertFalse(schema["unevaluatedProperties"])
        record = json.loads((ROOT / "records" / "accessions" / CASEY_ID / "visual-observation-record.json").read_text(encoding="utf-8"))
        payload = record["payload"]
        self.assertEqual([], validate_visual_observation(payload))
        candidate = copy.deepcopy(payload)
        candidate["objects"][0]["live_capture"]["source_url"] = "https://example.com/wrong"
        self.assertTrue(any("generator_url" in issue for issue in validate_visual_observation(candidate)))
        candidate = copy.deepcopy(payload)
        candidate["objects"][0]["live_capture"]["changed"] = False
        self.assertTrue(any("hash inequality" in issue for issue in validate_visual_observation(candidate)))
        candidate = copy.deepcopy(payload)
        candidate["objects"][0]["live_capture"]["frames"] = ["malformed"]
        candidate["objects"][0]["static_capture"]["retention"]["status"] = "retained"
        issues = validate_visual_observation(candidate)
        self.assertTrue(any("exactly two frame objects" in issue for issue in issues), issues)
        self.assertTrue(any("retention status cannot be retained" in issue for issue in issues), issues)
        for item in payload["objects"]:
            live = item["live_capture"]
            self.assertEqual([None, None], [frame["captured_at"] for frame in live["frames"]])
            self.assertEqual(1500, live["minimum_wait_between_frames_ms"])


if __name__ == "__main__":
    unittest.main()
