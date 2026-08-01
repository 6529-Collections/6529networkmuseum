# Documentation-as-code control plane

Status: WIP implementation note; the validator and schemas are proposed
repository controls, not adopted Museum policy.

## Conclusions

- The off-chain format keeps the exact 6529Stream `CollectionRecord` field
  names in an `envelope` object and commits only the schema-identified payload.
- JSON Schema is responsible for shape and vocabularies. Repository-level
  Python checks are required for hash verification, subject derivation,
  cross-reference resolution, append-only supersession, state transitions,
  governance source semantics, constructor/reviewer separation, and public
  sensitive-field checks.
- The RFC 8785 implementation is intentionally a constrained I-JSON profile:
  safe integers only, no floats, deterministic UTF-16 key sorting, and UTF-8
  output. This avoids runtime-dependent numeric serialization for public
  commitments.
- JSON files receive JCS/Keccak commitments and the deterministic release
  inventory receives LF-normalized SHA-256 entries in
  `release-artifacts/latest/record-manifest.json`.
- No canonical record was invented in this change. Fixtures are explicitly
  synthetic and are not governed records, even when the control-plane source
  inventory includes their test bytes.
- Manifest-authorized raw media is still subject to known credential-shape
  scanning and media/signature checks; this is a known-pattern admission gate,
  not a claim to detect arbitrary steganography.
- External HTTPS retrieval is centralized in `scripts/safe_fetch.py`, with
  resolution/address pinning, peer verification, redirect rechecks, bounded
  responses, and structured observations. `scripts/check_fetch_guard.py`
  keeps future collectors from bypassing that path.

## Unresolved questions

- The pinned Stream commit does not publish standalone canonical JSON Schema
  files for every museum profile. When it does, the Museum schemas need a
  byte-compatibility comparison and any divergence must be recorded in
  `docs/stream-interoperability.md` before a live record is published.
- The repository does not yet contain the pending canonical `records/` register;
  its first populated release should be created through reviewed record PRs
  using this control plane.
- The workflow uses the local Python Keccak implementation dependency for now;
  a future on-chain migration should add independent cross-language test
  vectors before deployment.
