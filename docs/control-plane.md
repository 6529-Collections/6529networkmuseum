# Documentation-as-code control plane

Status: working implementation standard for the public Museum repository. It
does not promote any WIP proposal, custody fact, accession, or governance
status into an adopted record.

## What is enforced

The repository currently has two compatible validation layers. The foundation
registers in `records/` use local schemas plus a `record_control` block;
`scripts/bootstrap_validate.py` uses the pinned Draft 2020-12 validator,
including `allOf`/`anyOf` composition, and validates every routed record,
including foundation records. It remains authoritative for source-derived
governance checks, raw evidence manifests, local links, public safety, and
constructor/reviewer payload hashes. New Stream-envelope records use the same
schema catalog and semantic checks in `scripts/validate.py`. The required
GitHub job `Museum validation` runs both layers.

The complete control plane is deliberately split between JSON Schema and
semantic checks. Schemas handle types, required fields, patterns, controlled
values, and closed nested objects. `scripts/validate.py` handles the checks
that need the whole repository or need to compare values:

- the off-chain file carries the Museum envelope under `envelope`; the
  executable Stream adapter converts its readable record type, hash
  references, URI, schema and subject identifiers, signature convention, and
  effective time into the exact eight-field `CollectionRecord` ABI shape;
- `payload.schema_id`, `envelope.schemaId`, and the pinned vocabulary agree;
- `envelope.contentHash` is Keccak-256 over the payload's canonical JSON;
- the subject is `keccak256("6529networkmuseum.subject.<record-type-lower>.v1:<subject_id>")`;
- envelope `effectiveAt` matches the payload's UTC timestamp;
- every stable cross-reference resolves to another record in the same public
  register, and `supersedes` preserves same-type append-only lineage without
  self-reference;
- `ACCESSION` carries distinct receipt, acceptance, acquisition, title-passage,
  custody-receipt, and accession events in order, each with its own date,
  authority, and evidence; title passage binds an off-chain instrument and
  custody receipt records its custody path;
- `RIGHTS_STATEMENT` and `CONDITION_REPORT` carry their own dated,
  authority-bound evidence events;
- `GIFT_ACCEPTANCE_AUTHORIZATION` records a formally effective gift decision
  and its authority-evidence limitations without substituting for a pending
  Stream `ACCESSION` completion certificate; its constructed/review-pending
  state is documentation QA, not a reversal of the stated decision;
- object workflow history starts at `offered`, follows only the controlled
  transitions, never regresses or repeats a state, and agrees with
  `current_state`;
- accession completion requires verified custody, an executed `TITLE_BINDING`,
  an explicit rights status (`granted`, `denied`, or `not_applicable` are all
  decisions; this gate does not grant rights), condition assessment,
  preservation evidence, and a distinct reviewer;
- the Casey post-accession diligence record must independently pass review,
  bind the complete twenty-two-file evidence package, reproduce all seven
  finalized-state owners and token-level approvals, retain a stable finalized
  block boundary and ENS resolution, and preserve the OFAC positive control,
  eight exact-address no-match observations, and their express limitations;
- a `WINNER` governance observation is adopted, while a `PARTICIPATORY`
  observation cannot be marked adopted;
- constructor and reviewer IDs differ;
- public records contain no restricted field names, credentials, private keys,
  private filesystem paths, or local/private-network URLs; endpoint policy is
  fail-closed for fetches through `scripts/safe_fetch.py`, requiring HTTPS,
  IDNA-first ASCII canonical host syntax, globally routable A/AAAA answers, a
  deterministically selected pinned IP, original-host TLS/SNI and canonical
  Host, peer-IP equality, bounded manual redirects with a fresh resolution at
  every hop, connect/read deadlines, GET/HEAD requests plus bounded JSON POST
  requests with a closed `Accept`/`Content-Type`/`User-Agent` header allowlist,
  a 1 MiB request-body limit, and strict
  Content-Length/Transfer-Encoding/content-encoding framing;
- `scripts/check_fetch_guard.py` rejects direct `requests`, `httpx`, `aiohttp`,
  URL-opener, HTTP-client, raw-socket, dynamic-import, and command-line fetch
  code outside that approved module, including in tests. The fetch primitive
  emits a structured observation containing the canonical URL, resolver
  profile/revision, address set and hash, selected and peer IPs, redirect
  chain, time, status, media type, actual byte length/hash, and relevant
  response headers.
- `scripts/generate_program_media.py --check` verifies that the Keys and Gates
  media manifest joins exactly to all sixteen selected outcomes, that every
  declared WebP exists with the committed raw-byte hash, size, geometry, and
  sRGB profile, and that no undeclared derivative is present.
- `scripts/migrate_public_entities.py --check` verifies the deterministic
  Stream-shaped public projection: 120 `PUBLIC_ENTITY` records, 205 closed
  `PUBLIC_RELATION` records, and one append-only `WAVE_STATUS_OBSERVATION`
  (326 generated records in total). Six withdrawn draft relation assertions
  retain append-only identity tombstones and their identifiers cannot be
  reused.
  The graph gate covers 21 Artist entities, 2 Organization entities, 6
  Project/Series entities, 28 acquisition-independent Work entities, two
  Acquisition Programs, exact slug/route families, typed Artist
  creator relations, 7 Casey Collection memberships, 16 Keys and Gates
  selections, and the five Magnum Work identities.
- `tests/test_public_entity_layer.py` verifies that every Work has displayable
  typed media, with 7 Casey, 16 Keys and Gates, and 5 signed-Wave Magnum
  Work/media joins; it fails closed on cross-work media reuse, rights/affordance
  expansion, generic image URLs, collection membership without accession,
  proposal-as-method, route/profile mismatches, and nonexistent evidence paths.
- The live Magnum status is an append-only observation. `WINNER` selection
  advances `6529NM-CA-2026-003` and Works `6529NM-W-0024` through `0028` to
  `selected_by_museum_wave_acquisition_review_in_progress`, while mint,
  acceptance, transfer, title, custody, rights, technical/preservation,
  accession, and Collection membership remain independent facts.

The bootstrap layer additionally verifies that governance decisions reproduce
the source snapshot, `WINNER`/`PARTICIPATORY` effects are not reclassified,
approved collections reference adopted decisions, evidence manifest paths,
media types, sizes, and raw-byte hashes match, and every reviewed
`record_control.payload_sha256` matches its record payload. Manifest-authorized
raw binary evidence is checked before UTF-8 public-safety scanning and is
limited in this profile to an explicitly declared, structurally parsed PNG
(valid signature, IHDR/IEND, chunk bounds/CRCs, and no trailing bytes). It
receives the same known credential-pattern gate across raw bytes, ASCII/UTF-8,
and UTF-16LE/BE spans, including cloud-key/token, path, DSA/PGP/generic PEM,
and private-key shapes; this detects known shapes, not arbitrary
steganography. Every unmanifested evidence file must also use a recognized
textual suffix and pass raw executable/polyglot signature checks before UTF-8
decoding; non-text evidence therefore requires an approved raw-byte manifest
entry. Undeclared undecodable bytes and unapproved media types fail closed.
Markdown templates and explanatory prose never satisfy these executable event
or completion gates.

The repository may contain no canonical records while the record register is
being established. In that case the validator still compiles every schema and
validates the vocabulary catalog. Test fixtures exercise the full relationship
and completion path without making claims about the live Museum collection.

## Record layout

Each record is a JSON object with exactly three top-level properties:

```json
{
  "$schema": "https://6529networkmuseum.org/schemas/record-envelope-v1.json",
  "envelope": {
    "recordType": "WORK_DESCRIPTION",
    "subjectId": "0x…",
    "contentHash": {
      "algorithm": 1,
      "digest": "0x…",
      "canonicalizationId": "0x886c…9044"
    },
    "uri": "ipfs://…",
    "schemaId": "0x5bb3…6a3c",
    "signatureScheme": "0x…",
    "signatureHash": {
      "algorithm": 2,
      "digest": "0x…",
      "canonicalizationId": "0x886c…9044"
    },
    "effectiveAt": 0
  },
  "payload": {}
}
```

Shared Stream schema IDs are copied from the pinned interoperability profile in
[`docs/stream-interoperability.md`](stream-interoperability.md). Museum-native
schema IDs are Keccak-256 commitments to their exact `*_V1` literal. The
controlled-vocabulary catalog is the single machine-readable list of supported
types, schema paths, workflow states, rights classes, evidence classes, and
hash identifiers.

## Canonicalization and manifests

The release profile is RFC 8785-compatible constrained I-JSON:

- objects sort keys by UTF-16 code units;
- strings use JSON's shortest valid escaping and UTF-8 output;
- booleans, null, arrays, finite IEEE-754 numbers, and safe integers are supported;
- non-finite values, unsafe integers, and Unicode surrogate code points are
  rejected rather than normalized differently by different runtimes;
- number serialization is delegated to the pinned RFC 8785 implementation and
  is covered by golden vectors for negative zero, exponent cutovers, precision,
  and subnormal values.

JSON entries receive a Stream-shaped Keccak/JCS `content_hash`. Museum-authored
text receives an LF-normalized SHA-256 digest, while declared WebP media receives
a raw-byte SHA-256 digest. Every entry names its byte mode. The manifest itself commits its
canonical body with both Keccak/JCS and SHA-256. Its closed directory inventory
covers `.github/`, `policies/`, `records/`, `schemas/`, `docs/`, `governance/`,
`media/`, `specs/`, `templates/`, `scripts/`, and `tests/`. It also covers the root control
files and the published Casey Reas generative-system dossier directory at
`notes/research/generative-systems/casey-reas/`. The root control files are
`.gitattributes`, `.gitignore`, `AGENTS.md`, `CONTRIBUTING.md`, `INDEX.md`,
`README.md`, `RIGHTS.md`, and `requirements-dev.txt`. Entries use sorted
repository-relative POSIX paths.
Generation fails closed if any configured root or named control file is missing,
linked, a reparse point, or not the expected regular-file/directory type.
Non-regular entries inside governed directories, including pipes, sockets, and
devices, are also rejected rather than silently omitted.

Evidence remains in separately governed raw-byte manifests so authenticated
source bytes are never silently normalized. Outside the explicitly governed
Casey Reas dossier directory, `notes/` is the indexed WIP and research notebook,
not a release authority. `release-artifacts/` is excluded to
avoid a self-referential manifest; Git internals are never inventoried.

The program-media verifier separately parses every WebP and reconciles its raw
bytes with the constructed program media manifest. Binary media is never passed
through line-ending normalization.

## Local commands

From the repository root:

```powershell
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
python scripts/bootstrap_validate.py
python scripts/build_proposed_gift_dossiers.py --check
python scripts/check_fetch_guard.py
python scripts/generate_program_media.py --check
python scripts/validate.py
python scripts/generate_manifest.py
python scripts/generate_manifest.py --check
```

Run `python scripts/build_proposed_gift_dossiers.py` after changing a proposed
gift's Storm source parts, then run its `--check` mode. Run the release-manifest
generator after changing a policy, canonical record, schema,
governance or control-plane document, protocol specification, template,
repository control, tool, or test. Commit the resulting
`release-artifacts/latest/record-manifest.json` with the change.
The pull-request workflow runs the bootstrap validator, test suite, full
validator, and stale-manifest check on every PR with a bounded job timeout and
pinned Python dependencies. A separate deterministic matrix runs the same
portable checks on Ubuntu and Windows; it does not replace the required
`Museum validation` job.

## Adding a correction

Do not edit a published assertion in place. Add a new record with a new
`record_id`, set `supersedes` to the prior record ID, state the
`supersession_reason`, retain the prior content hash in the historical record,
and include evidence plus independent review. The validator rejects unresolved
references and cross-type supersession.
