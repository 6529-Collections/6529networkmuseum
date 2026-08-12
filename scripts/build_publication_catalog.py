#!/usr/bin/env python3
"""Write/check immutable publication catalog C from an exact reviewed B commit."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from publication_catalog import (
    CATALOG_DIR,
    POINTER_PATH,
    CatalogError,
    build_catalog,
    build_pointer,
    check_catalog_git_transition,
    check_append_only_catalog,
    clear_cached_git_tree_readers,
    git_head_commit,
    retained_catalog_from_git_tree,
    retained_release_json,
    render_json,
    sha256_prefixed,
    strict_load,
    _catalog_tree_blobs,
    validate_canonical_catalog_path,
    validate_catalog,
    validate_pointer,
    verify_active_release_worktree,
)


ROOT = Path(__file__).resolve().parent.parent


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--commit", help="full lowercase reviewed B commit")
    parser.add_argument("--created-at")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--write-release", action="store_true")
    parser.add_argument("--mode", choices=("activate", "rollback"), default="activate")
    parser.add_argument("--actor")
    parser.add_argument("--activated-at")
    parser.add_argument("--target-catalog-id")
    parser.add_argument("--check-transition", action="store_true")
    parser.add_argument("--previous-commit")
    parser.add_argument("--current-commit")
    args = parser.parse_args(argv)
    root = ROOT.resolve()
    try:
        if args.check_transition:
            if not args.previous_commit or not args.current_commit:
                raise CatalogError("--check-transition requires --previous-commit and --current-commit")
            issues = check_catalog_git_transition(
                root, args.previous_commit, args.current_commit
            )
            if issues:
                print("publication catalog transition check failed:")
                print("\n".join(f"- {issue}" for issue in issues))
                return 1
            print(
                "publication catalog transition is append-only: "
                f"{args.previous_commit} -> {args.current_commit}"
            )
            return 0

        if args.write_release:
            if not args.actor or not args.activated_at:
                raise CatalogError("--write-release requires --actor and --activated-at")
            if args.mode == "activate" and (not args.commit or not args.created_at or args.target_catalog_id):
                raise CatalogError(
                    "activation requires --commit and --created-at and forbids --target-catalog-id"
                )
            if args.mode == "rollback" and (
                args.commit or args.created_at or not args.target_catalog_id
            ):
                raise CatalogError(
                    "rollback requires --target-catalog-id and forbids --commit/--created-at"
                )
            pointer_path = root / Path(*POINTER_PATH.split("/"))
            prior_catalog_id = None
            previous_pointer = None
            previous_catalog = None
            retained_catalog_ids: set[str] | None = None
            if args.mode == "rollback":
                tree_commit = git_head_commit(root)
                (
                    previous_pointer,
                    retained_pointer_bytes,
                    previous_catalog,
                    previous_catalog_bytes,
                ) = verify_active_release_worktree(root, tree_commit)
                if pointer_path.read_bytes() != retained_pointer_bytes:
                    raise CatalogError(
                        "rollback requires the current activation pointer to match its exact retained Git-tree bytes"
                    )
                prior_path = previous_pointer.get("catalog_path")
                validate_canonical_catalog_path(prior_path)
                prior_catalog_id = prior_path.rsplit("/", 1)[-1][:-5]
                if args.target_catalog_id == prior_catalog_id:
                    raise CatalogError("rollback target cannot equal the current prior catalog")
                previous_catalog_issues = validate_catalog(
                    previous_catalog,
                    root=root,
                    expected_commit=previous_catalog["payload"]["reviewed_source_head_commit"],
                )
                if previous_catalog_issues:
                    raise CatalogError("; ".join(previous_catalog_issues))
                previous_pointer_issues = validate_pointer(
                    previous_pointer, previous_catalog, previous_catalog_bytes, root=root
                )
                if previous_pointer_issues:
                    raise CatalogError("; ".join(previous_pointer_issues))
                retained_catalog_ids = {
                    path.rsplit("/", 1)[-1].removesuffix(".json")
                    for path in _catalog_tree_blobs(root, tree_commit)
                }
            else:
                if pointer_path.exists() or pointer_path.is_symlink():
                    tree_commit = git_head_commit(root)
                    (
                        previous_pointer,
                        _retained_pointer_bytes,
                        previous_catalog,
                        _previous_catalog_bytes,
                    ) = verify_active_release_worktree(root, tree_commit)
                    prior_path = previous_pointer.get("catalog_path")
                    validate_canonical_catalog_path(prior_path)
                    prior_catalog_id = prior_path.rsplit("/", 1)[-1][:-5]
                else:
                    # No pointer is valid only for the first activation. A
                    # retained HEAD pointer missing from the worktree is a
                    # deletion and must fail before any write.
                    tree_commit = git_head_commit(root)
                    try:
                        retained_release_json(root, tree_commit, POINTER_PATH)
                    except CatalogError as exc:
                        if "absent or ambiguous" not in str(exc):
                            raise
                    else:
                        raise CatalogError(
                            "activation requires the existing activation pointer to match its exact retained Git-tree bytes"
                        )

            if args.mode == "activate":
                catalog = build_catalog(
                    root,
                    reviewed_source_head_commit=args.commit,
                    accepted_paths=None,
                    created_at=args.created_at,
                )
                catalog_bytes = render_json(catalog)
                catalog_id = catalog["payload"]["catalog_id"]
                catalog_path = root / Path(
                    *f"{CATALOG_DIR}/{catalog_id}.json".split("/")
                )
            else:
                catalog_id = args.target_catalog_id
                catalog, catalog_bytes = retained_catalog_from_git_tree(
                    root, tree_commit, catalog_id
                )
                catalog_path = root / Path(*f"{CATALOG_DIR}/{catalog_id}.json".split("/"))
                if catalog_path.is_file() and catalog_path.read_bytes() != catalog_bytes:
                    raise CatalogError(
                        "rollback target catalog bytes do not match the exact retained Git-tree catalog"
                    )

            issues = validate_catalog(
                catalog,
                root=root,
                expected_commit=catalog["payload"]["reviewed_source_head_commit"],
            )
            if issues:
                raise CatalogError("; ".join(issues))
            pointer = build_pointer(
                catalog,
                catalog_file_sha256=sha256_prefixed(catalog_bytes),
                activation_actor=args.actor,
                activated_at=args.activated_at,
                mode=args.mode,
                prior_catalog_id=prior_catalog_id,
            )
            pointer_issues = validate_pointer(pointer, catalog, catalog_bytes)
            if pointer_issues:
                raise CatalogError("; ".join(pointer_issues))
            lineage_issues = check_append_only_catalog(
                previous_catalog,
                catalog,
                previous_pointer,
                pointer,
                root=root if args.mode == "rollback" else None,
                retained_catalog_ids=retained_catalog_ids,
            )
            if lineage_issues:
                raise CatalogError("; ".join(lineage_issues))

            if catalog_path.is_file() and catalog_path.read_bytes() != catalog_bytes:
                raise CatalogError("immutable catalog path already exists with different bytes")
            catalog_path.parent.mkdir(parents=True, exist_ok=True)
            pointer_path.parent.mkdir(parents=True, exist_ok=True)
            catalog_temp = catalog_path.with_suffix(".json.tmp")
            pointer_temp = pointer_path.with_suffix(".json.tmp")
            if not catalog_path.is_file():
                catalog_temp.write_bytes(catalog_bytes)
            pointer_temp.write_bytes(render_json(pointer))
            if not catalog_path.is_file():
                catalog_temp.replace(catalog_path)
            pointer_temp.replace(pointer_path)
            print(
                f"wrote publication {args.mode}: {catalog_path.relative_to(root)}; "
                f"pointer {pointer_path.relative_to(root)}"
            )
            return 0

        if not args.commit or not args.created_at:
            raise CatalogError("catalog build/check requires --commit and --created-at")
        output = args.output or (
            root / "release-artifacts/catalog" / f"6529NM-PUBCAT-{args.commit}.json"
        )
        output = output if output.is_absolute() else root / output
        if args.check:
            catalog = strict_load(output.read_bytes())
            issues = validate_catalog(catalog, root=root, expected_commit=args.commit)
            if issues:
                print("publication catalog check failed:")
                print("\n".join(f"- {issue}" for issue in issues))
                return 1
            print(f"publication catalog is current: {output}")
            return 0
        catalog = build_catalog(root, reviewed_source_head_commit=args.commit, accepted_paths=None, created_at=args.created_at)
        issues = validate_catalog(catalog, root=root, expected_commit=args.commit)
        if issues:
            print("publication catalog build failed validation:")
            print("\n".join(f"- {issue}" for issue in issues))
            return 1
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(render_json(catalog))
        print(f"wrote immutable publication catalog: {output}")
        return 0
    except (OSError, ValueError, CatalogError) as exc:
        print(f"publication catalog build/check failed: {exc}")
        return 1
    finally:
        clear_cached_git_tree_readers()


if __name__ == "__main__":
    sys.exit(main())
