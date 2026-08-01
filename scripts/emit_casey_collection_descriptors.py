#!/usr/bin/env python3
"""Run only the independently merged PR #4 tool for Casey descriptors.

This command is intentionally dependency-gated. It refuses to run on a local
variant, an unmerged PR head, or a dirty rarity-tool path. Acquisition and
verification do not require this command.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "evidence/casey-reas-collection-snapshots"
EXPECTED_SLUGS = ("century", "pre-process", "phototaxis", "923-empty-rooms", "ex-nihilo-cosmos")
ACTOR_ID = "codex-task:019fbe33-c412-7550-a1ba-f6c68c3b5652"
PR4_MERGE_COMMIT = "ff1c5825e3b61bfb2df0a639e057297beb946e4d"
PR4_TOOL_SHA256 = "e4060edf7354aa683458dfa0e620c598673a0c65202c8efadd768ae8dc03cc53"
PR4_TOOL_BLOB_OID = "755a1b1c948d900496f5e279594223c8c99ab3e8"


class DescriptorError(RuntimeError):
    """Raised when the PR #4 dependency gate is not satisfied."""


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def git(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", *args], cwd=ROOT, text=True, capture_output=True, check=False)


def verify_dependency(commit: str) -> Path:
    if len(commit) != 40 or any(character not in "0123456789abcdefABCDEF" for character in commit):
        raise DescriptorError("--pr4-merge-commit must be a full 40-character commit ID")
    if commit.lower() != PR4_MERGE_COMMIT:
        raise DescriptorError(f"--pr4-merge-commit must equal independently verified PR #4 merge {PR4_MERGE_COMMIT}")
    ancestor = git("merge-base", "--is-ancestor", commit, "HEAD")
    if ancestor.returncode != 0:
        raise DescriptorError("PR #4 merge commit is not an ancestor of the current HEAD")
    tool = ROOT / "scripts/rarity/analyze.py"
    if not tool.is_file():
        raise DescriptorError("merged scripts/rarity/analyze.py is absent at current HEAD")
    tracked = git("ls-files", "--error-unmatch", "scripts/rarity/analyze.py")
    if tracked.returncode != 0:
        raise DescriptorError("rarity tool is not tracked at current HEAD")
    dirty = git("status", "--porcelain", "--", "scripts/rarity")
    if dirty.stdout.strip():
        raise DescriptorError("rarity-tool path is dirty; refusing an unreviewed local variant")
    if sha256_bytes(tool.read_bytes()) != PR4_TOOL_SHA256:
        raise DescriptorError("current rarity tool bytes do not match the exact PR #4 SHA-256")
    blob = git("rev-parse", f"{commit}:scripts/rarity/analyze.py")
    if blob.returncode != 0 or blob.stdout.strip() != PR4_TOOL_BLOB_OID:
        raise DescriptorError("merged PR #4 rarity tool blob does not match the pinned Git blob OID")
    return tool


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pr4-merge-commit", required=True)
    parser.add_argument("--source-snapshot-commit", required=True)
    parser.add_argument("--acquisition-commit", required=True)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args(argv)
    try:
        tool = verify_dependency(args.pr4_merge_commit)
        output_dir = args.output_dir.resolve()
        latest = read_json(output_dir / "latest-run.json")
        if latest.get("status") != "complete":
            raise DescriptorError("latest acquisition run is not complete")
        manifest_path = output_dir / latest["manifest_path"]
        manifest = read_json(manifest_path)
        if manifest.get("status") != "complete":
            raise DescriptorError("acquisition manifest is not complete")
        for commit, label in ((args.source_snapshot_commit, "source snapshot"), (args.acquisition_commit, "acquisition")):
            if len(commit) != 40 or any(character not in "0123456789abcdefABCDEF" for character in commit):
                raise DescriptorError(f"--{label.replace(' ', '-')}-commit must be a full 40-character commit ID")
            if git("merge-base", "--is-ancestor", commit, "HEAD").returncode != 0:
                raise DescriptorError(f"{label} commit is not an ancestor of current HEAD")
        jobs: list[dict[str, Any]] = []
        for collection in manifest["collections"]:
            slug = collection["slug"]
            if slug not in EXPECTED_SLUGS:
                raise DescriptorError(f"unexpected collection in manifest: {slug}")
            snapshot_path = output_dir / collection["snapshot_path"]
            snapshot = read_json(snapshot_path)
            tool_input_bytes = snapshot_path.read_bytes()
            with tempfile.NamedTemporaryFile(prefix=f"casey-{slug}-", suffix=".json", delete=False) as temp_input:
                temp_input.write(tool_input_bytes)
                tool_input_path = Path(temp_input.name)
            with tempfile.NamedTemporaryFile(prefix=f"casey-{slug}-result-", suffix=".json", delete=False) as temp_output:
                raw_result_path = Path(temp_output.name)
            try:
                completed = subprocess.run(
                    [sys.executable, str(tool), str(tool_input_path), "--duplicates", "error", "--output", str(raw_result_path)],
                    cwd=ROOT,
                    text=True,
                    capture_output=True,
                    check=False,
                )
                if completed.returncode != 0 or not raw_result_path.is_file():
                    raise DescriptorError(f"merged PR #4 tool failed for {slug}: {completed.stderr.strip()}")
                result_bytes = raw_result_path.read_bytes()
                result = json.loads(result_bytes.decode("utf-8"))
            finally:
                tool_input_path.unlink(missing_ok=True)
                raw_result_path.unlink(missing_ok=True)
            descriptor = {
                    "schema_version": "6529nm.casey-collection-descriptor.v1",
                    "status": "complete",
                    "dependency": {"pull_request": 4, "rarity_tool_merge_commit": args.pr4_merge_commit, "rarity_tool_sha256": PR4_TOOL_SHA256, "rarity_tool_git_blob_oid": PR4_TOOL_BLOB_OID, "source_snapshot_commit": args.source_snapshot_commit, "acquisition_commit": args.acquisition_commit, "tool_path": "scripts/rarity/analyze.py"},
                    "constructor": {"actor_id": ACTOR_ID, "role": "constructor"},
                    "review": None,
                    "curatorial_significance": None,
                    "collection": {"slug": slug, "name": collection["name"], "contract_address": collection["contract_address"], "project_id": collection["project_id"]},
                    "input": {"snapshot_id": snapshot["snapshot_id"], "snapshot_sha256": collection["snapshot_file_sha256"], "tool_input_sha256": f"sha256:{sha256_bytes(tool_input_bytes)}", "compatibility_projection": {"mode": "byte_identical_source_snapshot", "removed_paths": []}, "source_snapshot_commit": args.source_snapshot_commit, "acquisition_commit": args.acquisition_commit, "request_provenance_sha256": manifest["request_provenance"]["sha256"], "exclusion_summary_sha256": manifest["exclusion_summary"]["sha256"], "observed_at": snapshot["observed_at"], "source": snapshot["source"], "source_token_order": snapshot["ordering"]["source_token_order"], "canonical_token_order": snapshot["ordering"]["canonical_token_order"], "source_trait_order": snapshot["ordering"]["source_trait_row_order"], "canonical_trait_order": snapshot["ordering"]["canonical_trait_order"]},
                    "method": {"label": "transparent statistical descriptor", "quality_or_canonical_truth_claim": False, "duplicate_policy": "error", "rarity_tool_merge_commit": args.pr4_merge_commit, "rarity_tool_sha256": PR4_TOOL_SHA256, "rarity_tool_git_blob_oid": PR4_TOOL_BLOB_OID},
                    "result": result,
                    "result_sha256": f"sha256:{sha256_bytes(result_bytes)}",
                    "interpretation_note": "This is a reproducible descriptor of trait prevalence in a frozen metadata snapshot. It is not a quality judgment, marketplace rarity score, value signal, or canonical truth.",
                }
            output_path = output_dir / "descriptors" / f"{slug}.json"
            output_path.parent.mkdir(parents=True, exist_ok=True)
            descriptor_bytes = (json.dumps(descriptor, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
            output_path.write_bytes(descriptor_bytes)
            jobs.append({"collection": slug, "output": output_path.relative_to(output_dir).as_posix(), "status": "complete", "descriptor_sha256": f"sha256:{sha256_bytes(descriptor_bytes)}", "result_sha256": descriptor["result_sha256"], "review": None})
        manifest_output = {"schema_version": "6529nm.casey-collection-descriptor-manifest.v2", "status": "complete", "dependency": {"pull_request": 4, "rarity_tool_merge_commit": args.pr4_merge_commit, "rarity_tool_sha256": PR4_TOOL_SHA256, "rarity_tool_git_blob_oid": PR4_TOOL_BLOB_OID, "source_snapshot_commit": args.source_snapshot_commit, "acquisition_commit": args.acquisition_commit}, "run_id": manifest["run_id"], "constructor": {"actor_id": ACTOR_ID, "role": "constructor"}, "review": None, "jobs": jobs}
        (output_dir / "descriptor-manifest.json").write_text(json.dumps(manifest_output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
        pending_path = output_dir / "pending-descriptors.json"
        pending = read_json(pending_path)
        pending["status"] = "complete_pending_review"
        pending["dependency"]["current_state_at_construction"] = "independently_approved_and_merged"
        pending["dependency"]["final_outputs_permitted"] = True
        pending["dependency"]["rarity_tool_merge_commit"] = args.pr4_merge_commit
        pending["dependency"]["rarity_tool_sha256"] = PR4_TOOL_SHA256
        pending["dependency"]["source_snapshot_commit"] = args.source_snapshot_commit
        pending["dependency"]["acquisition_commit"] = args.acquisition_commit
        pending["descriptor_manifest"] = "descriptor-manifest.json"
        pending["jobs"] = [{"collection": job["collection"], "input": next(row["snapshot_path"] for row in manifest["collections"] if row["slug"] == job["collection"]), "output": job["output"], "status": "complete_pending_review", "result": {"result_sha256": job["result_sha256"]}, "review": None} for job in jobs]
        pending_path.write_text(json.dumps(pending, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
        package_builder = ROOT / "scripts/build_casey_package_manifest.py"
        built = subprocess.run([sys.executable, str(package_builder), "--source-snapshot-commit", args.source_snapshot_commit, "--acquisition-commit", args.acquisition_commit, "--output-dir", str(output_dir)], cwd=ROOT, text=True, capture_output=True, check=False)
        if built.returncode != 0:
            raise DescriptorError(f"package manifest build failed: {built.stderr.strip()}")
        print(json.dumps(manifest_output, ensure_ascii=False, indent=2))
    except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError, DescriptorError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
