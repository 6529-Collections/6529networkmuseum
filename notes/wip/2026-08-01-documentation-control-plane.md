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
  responses, strict framing/header policy, bounded streamed reads, and
  structured observations. Only structurally checked PNG is admitted as raw
  binary evidence in the current public-safety profile; known credential
  patterns are checked across raw, ASCII/UTF-8, and UTF-16 forms. The guard
  scans tests too and keeps future collectors from bypassing that path.

## Review-bot deployment compatibility checkpoint

The deployed App Runner image was observed as `eefe911e-202606222152`. Its
repository catalog rejects `stream-contracts`, which invalidates the complete
repository configuration and suppresses automatic baseline/follow-up jobs.
`.github/6529bot.yml` therefore carries the deployed-compatible set and omits
that specialist temporarily; this is not a permanent catalog decision. When a
diff reaches the Stream-equivalent contract boundary, dispatch the central
`review-job.yml` workflow at a head-bound SHA using its supported input until
App Runner is upgraded. Do not use the unsupported shortcut, substitute an
unrelated profile, or deploy/restart production from this PR. The pinned
compatibility assertion is tested by `test_reviewbot_config_matches_deployed_compatibility_catalog`.

## Exact-head remediation checkpoint

Independent review of the prior head identified three fail-closed gaps. The
working remediation now rejects every declared non-text evidence media type
outside the structurally parsed PNG profile, scans bounded UTF-16LE/BE
candidate spans case-insensitively, and rejects `getattr`-mediated access to
network/process/dynamic-import roots in every Python tree including tests.
Governance prose now states the exact four-kind automatic production baseline;
external-media and deploy-actions remain manual specialists, and Stream review
uses the central head-bound workflow until the production catalog upgrade.
Focused adversarial tests cover PDF/octet-stream polyglots, uppercase secrets
in both UTF-16 endiannesses, and aliased `getattr` bypasses.

The subsequent exact-head probe also covered an unmanifested ASCII polyglot.
Evidence fallback now checks the raw bytes and suffix before decoding, so
executable/container signatures cannot pass merely because they are valid
UTF-8; non-text evidence must be admitted by an approved raw-byte manifest.

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
