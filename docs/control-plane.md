# Documentation-as-code control plane

Status: working implementation standard for the public Museum repository. It
does not promote any WIP proposal, custody fact, accession, or governance
status into an adopted record.

## What is enforced

The repository currently has two compatible validation layers. The foundation
registers in `records/` use local bootstrap schemas plus a `record_control`
block; `scripts/bootstrap_validate.py` remains authoritative for their source-
derived governance checks, raw evidence manifests, local links, public safety,
and constructor/reviewer payload hashes. New Stream-envelope records use the
schemas and semantic checks in `scripts/validate.py`. The required GitHub job
`Museum validation` runs both layers.

The complete control plane is deliberately split between JSON Schema and
semantic checks. Schemas handle types, required fields, patterns, controlled
values, and closed nested objects. `scripts/validate.py` handles the checks
that need the whole repository or need to compare values:

- the off-chain file has the exact Stream `CollectionRecord` envelope under
  `envelope`; field names and order are not changed in the ABI-facing shape;
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
- object workflow history starts at `offered`, follows only the controlled
  transitions, never regresses or repeats a state, and agrees with
  `current_state`;
- accession completion requires verified custody, an executed `TITLE_BINDING`,
  an explicit rights status (`granted`, `denied`, or `not_applicable` are all
  decisions; this gate does not grant rights), condition assessment,
  preservation evidence, and a distinct reviewer;
- a `WINNER` governance observation is adopted, while a `PARTICIPATORY`
  observation cannot be marked adopted;
- constructor and reviewer IDs differ;
- public records contain no restricted field names, credentials, private keys,
  private filesystem paths, or local/private-network URLs.

The bootstrap layer additionally verifies that governance decisions reproduce
the source snapshot, `WINNER`/`PARTICIPATORY` effects are not reclassified,
approved collections reference adopted decisions, evidence manifest paths and
raw-byte hashes match, and every reviewed `record_control.payload_sha256`
matches its record payload.
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
- booleans, null, arrays, and safe integers are supported;
- floats, non-finite values, unsafe integers, and Unicode surrogate code points
  are rejected rather than normalized differently by different runtimes.

JSON entries receive a Stream-shaped Keccak/JCS `content_hash` and all governed
files receive an LF-normalized SHA-256 digest. The manifest itself commits its
canonical body with both Keccak/JCS and SHA-256. The inventory covers
`policies/`, `records/`, and `schemas/` in sorted repository-relative POSIX
order; the manifest is not self-included.

## Local commands

From the repository root:

```powershell
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
python scripts/bootstrap_validate.py
python scripts/validate.py
python scripts/generate_manifest.py
python scripts/generate_manifest.py --check
```

Run the generator after changing a policy, canonical record, or schema. Commit
the resulting `release-artifacts/latest/record-manifest.json` with the change.
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
