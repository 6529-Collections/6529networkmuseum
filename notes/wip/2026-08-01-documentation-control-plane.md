# Documentation-as-code control plane

Status: historical implementation note. The validators, schemas,
deterministic release manifest, and CI checks described here are active
repository controls, not adopted Museum policy. Current operation is specified
in [`docs/control-plane.md`](../../docs/control-plane.md).

Supersession note (2026-08-02): this file preserves the design history of the
control plane. The repository now contains canonical governance, program,
collection, and accession records; the operational description in
[`docs/control-plane.md`](../../docs/control-plane.md), the canonical
[`INDEX.md`](../../INDEX.md), and the deterministic release manifest supersede
the implementation-state statements below. The architectural conclusions and
unresolved Stream/on-chain deployment boundaries remain useful design context.

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
- At this historical checkpoint no canonical record was introduced by the
  control-plane change itself. Canonical records were added later through
  independently reviewed pull requests. Fixtures remain explicitly synthetic
  and are not governed records even when the release inventory includes their
  test bytes.
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

Independent review of the construction head identified three fail-closed gaps.
The merged validators reject every declared non-text evidence media type
outside the structurally parsed PNG profile, scans bounded UTF-16LE/BE
candidate spans case-insensitively, and rejects `getattr`-mediated access to
network/process/dynamic-import roots in every Python tree including tests.
`.github/6529bot.yml` sets the automatic production baseline to exactly
`general`, `security`, `privacy-evidence`, and `glm-swarm`. `media-external`
and `deploy-actions` remain manual specialists. Stream-equivalent contract
review uses the central head-bound workflow until the production catalog upgrade.
Focused adversarial tests cover PDF/octet-stream polyglots, uppercase secrets
in both UTF-16 endiannesses, and aliased `getattr` bypasses.

The subsequent exact-head probe also covered an unmanifested ASCII polyglot.
Evidence fallback now checks the raw bytes and suffix before decoding, so
executable/container signatures cannot pass merely because they are valid
UTF-8; non-text evidence must be admitted by an approved raw-byte manifest.

## Remaining implementation boundaries

- The pinned Stream commit does not publish standalone canonical JSON Schema
  files for every museum profile. When it does, compare the canonical schema
  bytes and record every divergence in `docs/stream-interoperability.md` before
  migrating Museum records to that Stream revision.
- The workflow uses the local Python Keccak implementation dependency. Before
  contract deployment, add independent cross-language vectors covering every
  on-chain commitment and canonicalization path.

## Resolved after this note

- The canonical `records/` register is populated through reviewed record pull
  requests and is covered by the release manifest. In particular,
  `records/accessions/register.json` records the Casey REAS seven-work gift as
  accepted and accessioned, while the accession dossier retains the reviewed
  authorization, lot, certificate, object, rights, condition, visual,
  curatorial, technical, and public records. Ongoing software preservation is
  active stewardship, not an incomplete accession decision.
