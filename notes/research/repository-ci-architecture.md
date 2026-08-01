# Repository and CI architecture proposal

Status: WIP design proposal; not adopted policy and not an implementation record.

Scope: the transitional GitHub system of record for the 6529 Network Museum. The
repository must be usable by a registrar, curator, conservator, engineer, or an
independent archivist without relying on undocumented agent context. The design
below treats records as data, Markdown as a deterministic publication, and CI as
the first line of registrar control.

## Design commitments

The implementation should make these commitments executable:

1. Canonical facts live in machine-readable records. Hand-authored Markdown is
   for policy, research, and interpretation; generated Markdown is a view of
   canonical records and is never edited by hand.
2. Every material assertion has an authority, observation/effective time, source
   or evidence reference, and an explicit evidence class. A missing fact is
   represented as `unknown`, `not_assessed`, or `not_applicable`, never silently
   omitted when omission would imply completion.
3. A Wave winner, a donation offer, a wallet transfer, and an accession are
   different events. CI must reject records that collapse those states.
4. Public records contain no donor contact details, private legal instruments,
   signer information, secrets, or private storage locations. A public record
   may point to a restricted instrument by non-sensitive reference and content
   hash.
5. Corrections are append-only. A changed assertion creates a new revision with
   `supersedes`; it does not rewrite a published historical assertion.
6. Museum-to-Stream interoperability is a byte-level compatibility target where
   the concepts overlap. The Stream `HashRef` and `CollectionRecord` envelope,
   RFC 8785 JCS identifier, Keccak-256 semantics, and pinned profile IDs are
   imported as normative constants rather than re-invented locally.
7. A constructor prepares a record and a distinct reviewer accepts it. The
   constructor cannot be the sole reviewer of their own accession or release.
8. A build on Windows and Linux produces the same rendered bytes, canonical JSON
   bytes, hashes, and manifest root for the same source tree.

These are implementation requirements for the documentation system. They do
not themselves grant accession authority or change adopted Museum policy.

## Proposed directory tree

The proposal extends the current `policies/`, `docs/`, `records/`, and `schemas/`
layout without moving the existing governing sources during the first
implementation. New data is one-record-per-file wherever possible so reviews
can identify a small, meaningful diff.

```text
.
├── .github/
│   ├── CODEOWNERS
│   ├── pull_request_template.md
│   ├── workflows/
│   │   ├── museum-pr.yml
│   │   ├── museum-nightly-links.yml
│   │   └── museum-release.yml
│   └── dependabot.yml
├── docs/
│   ├── accession-standard.md
│   ├── external-works-registry.md
│   ├── onchain-design.md
│   ├── record-model.md
│   ├── repository-contribution-standard.md
│   └── stream-interoperability.md
├── policies/
│   ├── founding-and-operating-principles.md
│   ├── general-nft-collecting-scope.md
│   ├── donation-acceptance.md
│   └── README.md
├── records/
│   ├── README.md
│   ├── _index.json                         # generated ID/type/path index
│   ├── governance/
│   │   ├── decisions/                      # one decision per JSON file
│   │   └── decisions.json                  # generated compatibility index
│   ├── institution/
│   │   └── museum.json
│   ├── collections/
│   │   ├── approved-collections.json       # current-view generated index
│   │   └── approved/                       # one preapproval record per collection
│   ├── programs/
│   │   └── 6529NM-AP-01/
│   │       ├── program.json
│   │       ├── selected-works/             # selection is not accession
│   │       └── selected-works.json         # generated compatibility index
│   ├── accessions/
│   │   ├── register.json                   # current-view generated index
│   │   └── lots/                            # lot statement and object schedule
│   ├── objects/                             # one living public object record each
│   ├── curatorial/                          # collection/object interpretation
│   ├── preservation/                        # public PREMIS/IIIF/fixity summaries
│   ├── assertions/                          # atomic fact assertions
│   ├── sources/                             # public source catalog and captures
│   └── amendments/                          # append-only corrections
├── vocabularies/
│   ├── museum-terms.json
│   ├── evidence-classes.json
│   ├── status-transitions.json
│   ├── source-types.json
│   ├── acquisition-methods.json
│   ├── rights.json
│   └── mappings/                            # PREMIS, LIDO, CDWA, AAT, Spectrum
├── schemas/
│   ├── $id-registry.json
│   ├── common/
│   │   ├── identifiers.schema.json
│   │   ├── source-ref.schema.json
│   │   ├── evidence.schema.json
│   │   ├── assertion.schema.json
│   │   ├── review.schema.json
│   │   ├── lineage.schema.json
│   │   ├── chain-object.schema.json
│   │   ├── stream-envelope.schema.json
│   │   └── restricted-ref.schema.json
│   ├── records/
│   │   ├── institution.schema.json
│   │   ├── policy.schema.json
│   │   ├── governance-decision.schema.json
│   │   ├── approved-collection.schema.json
│   │   ├── accession-program.schema.json
│   │   ├── accession-lot.schema.json
│   │   ├── object-record.schema.json
│   │   ├── curatorial-statement.schema.json
│   │   ├── preservation-summary.schema.json
│   │   └── amendment.schema.json
│   ├── stream/
│   │   ├── stream-system-manifest.json
│   │   ├── stream-accession-v1.schema.json
│   │   ├── stream-work-description-v1.schema.json
│   │   ├── stream-rights-v1.schema.json
│   │   ├── stream-premis-v3-profile.schema.json
│   │   ├── stream-lido-profile-v1.schema.json
│   │   └── stream-iiif-p3-min-v1.schema.json
│   └── vocabularies/
├── scripts/
│   ├── validate.py
│   ├── generate_manifest.py
│   ├── render_records.py
│   ├── check_links.py
│   ├── check_public_tree.py
│   ├── check_transitions.py
│   ├── check_stream_conformance.py
│   └── lib/
│       ├── canonical_json.py
│       ├── paths.py
│       ├── refs.py
│       └── terms.py
├── rendered/                                # generated, reviewable Markdown
│   ├── records/
│   ├── catalog/
│   └── manifest.json
├── release-artifacts/
│   ├── latest/                               # generated pointer for humans
│   └── releases/                             # immutable versioned manifests
└── tests/
    ├── fixtures/
    ├── test_canonical_json.py
    ├── test_manifest.py
    ├── test_references.py
    ├── test_transitions.py
    ├── test_public_boundary.py
    ├── test_stream_roundtrip.py
    └── test_renderer.py
```

`records/*/index.json`, `decisions.json`, `register.json`, and `rendered/` are
derived views. The source records from which they are generated are the review
boundary. If a compatibility index is retained for existing consumers, CI must
regenerate it and fail on drift.

Restricted registrar material is not stored in a `restricted/` directory in the
public repository. The public tree contains only `restricted-ref` objects. The
registrar system (a separately controlled vault or private repository) owns the
instrument itself. A local operator may keep an ignored working copy outside the
repository, but a CI job must reject any tracked path whose class is restricted.

## Record and schema interfaces

All schemas should use JSON Schema Draft 2020-12. Each schema has a stable `$id`
under `https://museum.6529.eth/schema/...`; schema `$id` values are content
addressed by the schema release manifest but are not changed when a record is
corrected. Records use a top-level discriminator and reject unknown fields in
the canonical publication profile (`additionalProperties: false`, with an
explicit `extensions` object for reviewed extensions).

### Common envelope

Every canonical record should implement the following interface. The concrete
domain schema adds its own required fields.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://museum.6529.eth/schema/common/record-envelope/v1",
  "recordType": "object",
  "recordId": "6529NM.2026.001.01",
  "recordVersion": 1,
  "schemaId": "https://museum.6529.eth/schema/records/object-record/v1",
  "status": "catalogued",
  "createdAt": "2026-08-01T00:00:00Z",
  "effectiveAt": "2026-08-01T00:00:00Z",
  "constructedBy": {"agentId": "agent:registrar-01", "role": "constructor"},
  "review": {
    "state": "approved",
    "reviewedBy": [{"agentId": "agent:curator-01", "role": "reviewer"}],
    "reviewedAt": "2026-08-02T00:00:00Z",
    "reviewScope": ["identity", "provenance", "rights", "curatorial"]
  },
  "sources": ["SRC-CHAIN-001", "SRC-ARTIST-001"],
  "assertions": ["ASM-6529NM-2026-001-01-001"],
  "supersedes": null,
  "extensions": {}
}
```

The envelope is not a claim that the record is complete. `review.state` may be
`draft`, `in_review`, `changes_requested`, `approved`, or `withdrawn`. Approval
is valid only when the reviewer scope covers the fields being promoted and the
reviewer is independent of the constructor under the configured role policy.

### Assertion interface

Assertions are first-class records so a correction can preserve history and
conflicting evidence can remain attributed.

```json
{
  "$id": "https://museum.6529.eth/schema/common/assertion/v1",
  "assertionId": "ASM-6529NM-2026-001-01-001",
  "subject": {"recordId": "6529NM.2026.001.01", "path": "/chainObject/caip19"},
  "predicate": "museum:hasChainIdentity",
  "value": "eip155:1/erc721:0x.../123",
  "valueType": "caip-19",
  "evidenceClass": "A",
  "sourceRefs": ["SRC-CHAIN-001"],
  "assertedBy": {"agentId": "agent:technical-01", "role": "technical_verifier"},
  "observedAt": "2026-08-01T00:00:00Z",
  "confidence": "verified",
  "supersedes": null
}
```

The validator checks that `subject.recordId` exists, `subject.path` exists in
the applicable schema, the value matches the path type, evidence class A has a
chain source, and a correction points to a prior assertion with a different
payload hash. `confidence` is not a substitute for evidence class and must not
be used to turn interpretation into fact.

### Source and evidence interfaces

`SourceRef` is a public bibliographic or technical citation:

```json
{
  "sourceId": "SRC-CHAIN-001",
  "sourceType": "chain_rpc",
  "title": "Ethereum transaction receipt",
  "uri": "https://etherscan.io/tx/0x...",
  "observedAt": "2026-08-01T00:00:00Z",
  "retrievalMethod": "public_rpc_and_explorer_cross_check",
  "contentHash": {"algorithm": 2, "digest": "sha256:..."},
  "stability": "mutable_snapshot",
  "notes": "Explorer URL is a locator; the receipt and block are the evidence."
}
```

`EvidenceRef` adds the assertion-specific source fragment, a quote or JSON
pointer where appropriate, and an optional capture hash. A source URL alone is
not evidence of the page's future contents. The source catalog must distinguish
`stable_primary`, `stable_snapshot`, `mutable_api`, `third_party`, and
`interpretive` sources. Network-derived assertions are only promoted after
their retrieval output is either captured, content-addressed, or explicitly
marked as a mutable observation.

### Chain object interface

The chain interface must distinguish identity from custody and title:

```json
{
  "chainObject": {
    "caip19": "eip155:1/erc721:0xlowercasecontract/123",
    "chainId": "eip155:1",
    "standard": "erc721",
    "contract": "0x...",
    "tokenId": "123",
    "project": {"name": "Example", "contract": "0x..."},
    "mint": {"transaction": "0x...", "block": 12345678},
    "custody": {"wallet": "0x...", "verifiedAt": "2026-08-01T00:00:00Z"},
    "titleBindingRef": "TB-6529NM-2026-001-01"
  }
}
```

The CAIP-19 value is normalized for comparison, while the original observed
strings remain in evidence. Contract addresses are lower-case in canonical
identifiers; checksum presentation is a separate display field. Numeric token
IDs are decimal strings. No schema or validator may infer accession from
`custody.wallet`, a transfer, or a program winner.

### Stream envelope interface

The compatibility schema must encode the exact Stream shape rather than a
Museum-specific look-alike:

```json
{
  "recordType": "0x...32-byte-stream-record-type",
  "subjectId": "0x...32-byte-subject-id",
  "contentHash": {
    "algorithm": 1,
    "digest": "0x...",
    "canonicalizationId": "0x886c7c89c308c459ca8a626e0ef36a5ea9f4c7a7b56aaf86c71a2ddf3b4f9044"
  },
  "uri": "ipfs://...",
  "schemaId": "0x...",
  "signatureScheme": "0x...",
  "signatureHash": {
    "algorithm": 2,
    "digest": "0x...",
    "canonicalizationId": "0x886c7c89c308c459ca8a626e0ef36a5ea9f4c7a7b56aaf86c71a2ddf3b4f9044"
  },
  "effectiveAt": 1754006400
}
```

The JSON representation is a serialization of the Solidity `HashRef` and
`CollectionRecord` fields. It must preserve algorithm IDs, byte encodings,
canonicalization ID, schema ID, record type, subject ID, URI, signature fields,
and Unix-second `effectiveAt`. The implementation pins the active Stream
commit and schema identifiers in `schemas/stream/stream-system-manifest.json`.
`check_stream_conformance.py` must export Museum records to Stream profiles,
import them again, and compare semantic values and hash inputs. A change to a
shared Stream field is a release-blocking failure until the bilateral profile
is updated and reviewed.

### Accession and object interfaces

An accession lot contains:

- a stable lot ID, acceptance authority, acceptance date, method, source/donor
  reference, collecting-policy pathway, object schedule, rights/conditions,
  title-binding references, review block, and accession-state history;
- one object record per token or other accessioned object;
- a collection-level curatorial statement that is interpretive and revisable;
- separate technical, condition, preservation, and public-display summaries.

`object-record.schema.json` must require a `chainObject` for an on-chain work,
but must permit the work's token metadata, code, dependencies, rights, and
render state to be independently `unknown` or `not_assessed`. It should require
the explicit field `rarityAssessmentPolicy` when a generative work contains
derived traits, with values `not_used`, `museum_transparent_analysis`, or
`third_party_descriptive_only`. OpenSea rarity fields are forbidden by schema
and semantic validation. Internal-style generative analysis must identify its
script version, source input, parameters, output hash, and reproducible results.

### Review interface

The review record should be both in JSON and visible in the pull request:

```json
{
  "constructor": {"agentId": "agent:...", "role": "constructor"},
  "reviewers": [
    {"agentId": "agent:...", "role": "registrar", "scope": ["identity", "title"]},
    {"agentId": "agent:...", "role": "curator", "scope": ["interpretation"]}
  ],
  "independence": {"constructorMayReview": false, "minimumReviewers": 1},
  "decision": "approved",
  "decisionAt": "2026-08-02T00:00:00Z",
  "reviewEvidence": ["PR-123", "CI-RUN-456"]
}
```

For an accession, the default minimum is two reviewers: a registrar/technical
reviewer for identity, title, custody, and preservation, and a curator for
interpretation and significance. The same person may hold more than one Museum
role in the abstract but cannot satisfy the independence rule for their own
construction. CI enforces declared roles; CODEOWNERS enforces repository path
coverage; the pull request is the human-readable audit trail.

## Controlled vocabularies

Vocabularies are versioned, append-only JSON records with a stable `termId`,
preferred label, definition, status, effective dates, and external mappings.
Deprecation uses `replacedBy`; deleting or recycling a term ID is forbidden.
The validator rejects unknown terms in closed fields and allows free text only
in explicitly designated narrative fields.

At minimum, vocabulary files cover:

- record types, roles, evidence classes, source types, acquisition methods, and
  accession statuses;
- condition and preservation outcomes; rights bases and grant statuses;
- object classifications, media, techniques, manifestation types, and
  conservation risk states;
- program selection states, governance statuses, and amendment reasons;
- Stream, PREMIS v3, LIDO/CDWA-Lite, Spectrum, Object ID, IIIF, and CAIP
  mappings.

The Museum may add a local term only with a definition and a mapping or an
explicit `no_external_equivalent` explanation. It must never redefine a Stream,
PREMIS, LIDO, or external museum term. Vocabularies are exported into the
Stream profile only after a bilateral mapping test.

## Cross-reference and semantic integrity

JSON Schema handles shape; `validate.py` handles meaning. The semantic validator
must build one global index of all public record IDs and then enforce:

- every `recordId`, `sourceId`, `assertionId`, `termId`, and foreign key is unique
  and resolves exactly once;
- every source, assertion, review, amendment, and restricted reference is
  reachable from a published record or intentionally indexed as a source;
- no public record references a restricted path, private URI, secret-like value,
  raw signature, seed phrase, or credential;
- accession lot schedules match object records, object IDs remain stable, and
  an object cannot be in two active accession lots without an explicit
  deaccession or correction lineage;
- governance decisions cite the Wave serial/drop ID, URL, observed API status,
  and observation time; vote totals never stand in for adoption status;
- a program winner is linked to a selection record, but no winner link alone can
  advance acquisition or accession status;
- `supersedes` chains are acyclic, point to the same record family, preserve the
  prior content hash, and have an amendment reason and reviewer;
- status events follow the transition table and contain all required gate
  evidence; status cannot be manually edited to skip a gate;
- assertion paths exist in the applicable schema and evidence classes match
  source types; a third-party source cannot be promoted to direct chain fact;
- all Stream profile IDs, record-type IDs, and canonicalization IDs match the
  pinned system manifest;
- all collection/program/object references resolve in both canonical and
  rendered views.

Cycles are rejected for all graph edges except the explicit `supersedes` chain,
which must itself be acyclic. Display links may point outward, but canonical
record references use stable IDs, not fragile Markdown anchors.

## Status-transition gates

The state machine remains the one in the accession standard:

```text
offered
  -> authorized
  -> acquired
  -> received_onchain
  -> accessioned
  -> catalogued
  -> technically_verified
  -> preservation_complete
  -> display_ready
```

Every transition is an append-only `statusEvent` with `from`, `to`, actor,
effective time, evidence refs, review refs, and the resulting record hash. The
following gates are release-blocking:

| Transition | Minimum gate evidence |
|---|---|
| offered -> authorized | qualifying policy/program path, approval record, conflict and eligibility review |
| authorized -> acquired | executed public title/donation reference, conditions, rights review, source identity |
| acquired -> received_onchain | exact transfer transaction to designated custody, independent chain verification |
| received_onchain -> accessioned | title binding to that transfer, duplicate/sanctions/provenance diligence, registrar approval |
| accessioned -> catalogued | complete object identity, artist/project authority, curatorial record, public credit line |
| catalogued -> technically_verified | token/metadata/script/dependency assessment, render protocol, condition result, fixity |
| technically_verified -> preservation_complete | PREMIS event/object summary, dossier manifest, recovery lineage, verified hashes |
| preservation_complete -> display_ready | display/rights permission, approved derivatives or IIIF manifest, accessibility and credit checks |

No transition may be skipped. A failed or reversed operational condition creates
a new status event or amendment; it does not delete the prior state. A wallet
balance, ENS name, marketplace listing, Wave winner label, or generated image
cannot satisfy a gate by itself.

## Canonicalization, hashing, and manifests

The canonicalization library must be shared by validation, rendering metadata,
and release tooling. The rules are:

- all text is UTF-8, LF, with no BOM; `.gitattributes` remains authoritative;
- canonical JSON uses RFC 8785 JCS over an I-JSON-compatible subset: no NaN or
  Infinity, no duplicate keys, finite numbers only, and dates/identifiers are
  strings; arrays are semantically ordered or are sorted by an explicit schema
  rule before canonicalization;
- JSON object keys are ordered only by JCS, never by a language/runtime's default
  serializer; no whitespace is emitted in canonical payloads;
- repository paths are relative POSIX paths with `/`, sorted by Unicode code
  point; case-collision checks run on both case-sensitive and case-insensitive
  filesystems;
- text file SHA-256 is over LF-normalized bytes; binary SHA-256 is over original
  bytes; Ethereum Keccak-256 is distinct from NIST SHA3-256 and must be tested
  against fixed vectors;
- Stream `HashRef.algorithm` values and `RFC8785_JCS` canonicalization ID are
  emitted exactly as pinned in the Stream interoperability document;
- no generated file contains build time, host name, absolute path, random UUID,
  locale-formatted number, or line-ending-dependent value.

The manifest is an explicit, non-recursive input set, never “all files on disk”.
It contains, for each governed file, POSIX path, media type, byte length,
LF-normalized SHA-256 where applicable, canonical JSON digest where applicable,
Keccak digest where applicable, schema ID, and record ID(s). The manifest also
contains the sorted list of schema/vocabulary versions and the root digest.
`release-artifacts/` and its own manifest are excluded from the input set to
avoid a fixed-point problem; the manifest records its own version and input
policy instead.

`generate_manifest.py --check` must regenerate into a temporary directory and
byte-compare with the checked-in generated outputs. `--write` is only used by a
constructor or the release workflow. A release's content root is derived only
from governed inputs; Git commit IDs and GitHub run IDs belong in provenance
metadata, not in the content root.

## Rendering and reproducible builds

`render_records.py` reads canonical records, resolves vocabulary labels and
references, and emits Markdown using pinned templates. Each generated document
contains a short machine-readable header such as:

```text
<!-- GENERATED: source=6529NM.2026.001.01 sourceSha256=sha256:... renderer=1.0.0 -->
```

The renderer must use explicit locale-independent formatting, UTC ISO 8601
timestamps, stable field order, deterministic list order, safe Markdown
escaping, and POSIX-relative links. It must never fetch a remote URL during a
build. A missing optional field renders a controlled label such as “not
assessed”; it must not disappear in a way that suggests a negative finding.

CI runs the renderer twice, once in a Linux job and once in a Windows job, and
compares the resulting tree and manifest. A local `render --check` uses a
temporary directory, so generated output can be reviewed without mutating the
working tree. Markdown under `policies/` and `docs/` remains hand-authored and
is never overwritten by the renderer.

## CI and GitHub controls

### Pull request workflow

`.github/workflows/museum-pr.yml` should run on pull requests and pushes to the
default branch. Actions must be pinned to immutable commit SHAs and third-party
Python dependencies must come from a lock file with hashes.

1. **Repository policy**: confirm the branch, changed paths, file encodings,
   generated-header rules, no restricted paths, no symlink escape, and no
   unexpected binary or executable files.
2. **Schema validation**: validate every canonical JSON file against its schema;
   validate the schema registry itself and reject unknown `$schema` versions.
3. **Semantic integrity**: run ID/reference, assertions, lineage, vocabulary,
   source, transition, accession, and public-boundary checks.
4. **Stream conformance**: validate all Stream profiles, hash vectors, exact
   envelope serialization, and export/import round trips.
5. **Reproducible render**: render and check generated Markdown, compatibility
   indexes, and manifest drift.
6. **Tests**: run unit and fixture tests under a pinned Python version on both
   `ubuntu-latest` and `windows-latest`; include a case-sensitive path fixture
   and a case-collision fixture.
7. **Secret and PII scan**: scan the diff and the complete tracked tree for
   private keys, seed phrases, JWTs, credentials, email/phone patterns,
   unapproved donor fields, and restricted filenames. A finding is a hard
   failure; false-positive suppression requires a reviewed, hashed allowlist.
8. **Link policy**: hard-fail local links and schema/record references; run
   remote link checks only for stable allowlisted domains and only when a
   source record explicitly requests it.

### Nightly and scheduled workflow

`museum-nightly-links.yml` performs remote source checks and freshness reports
without blocking ordinary PRs. It retries idempotent GETs with bounded
exponential backoff, honors `Retry-After`, uses a small concurrency limit, and
records a timestamped report as a workflow artifact. A transient 429, 5xx,
timeout, DNS failure, or robots denial is `inconclusive`, not a broken source;
two consecutive scheduled failures may open an issue. A reproducible local
source capture or pinned content hash is what makes a release independent of
network availability.

### Release workflow

`museum-release.yml` runs only on a protected release tag after all required PR
checks pass. It:

- checks a clean tree and verifies the tag points to the reviewed commit;
- validates, renders, runs all tests, and regenerates manifests from scratch;
- checks Stream profile drift and hash vectors;
- creates an immutable release artifact containing canonical records, rendered
  views, schemas, vocabularies, source catalog, and manifest;
- publishes the manifest and checksums as GitHub release assets and an
  attestation/provenance record that does not alter the content root;
- updates the human convenience pointer `release-artifacts/latest` only as a
  generated view;
- refuses to release if any accession is marked complete without its required
  review, title binding, preservation, rights, or technical gates.

### GitHub review structure

`CODEOWNERS` should require at least:

- registrar/technical reviewer for `records/accessions/`, `records/objects/`,
  `records/preservation/`, `schemas/`, and `scripts/`;
- curator reviewer for `records/curatorial/`, `docs/`, and art-historical
  interpretation;
- governance reviewer for `policies/`, `records/governance/`, and approved
  collection/program decisions;
- security/registrar owner for any public-boundary or source-catalog change.

The branch ruleset should require the validation job, one independent required
review, no self-approval, resolved review threads, and linear history for
release branches. A constructor/reviewer declaration in the record is the
semantic control; GitHub ownership is the enforcement and audit surface.

## Link checking without flaky releases

Link classes have different failure policies:

| Link class | PR behavior | Release behavior |
|---|---|---|
| local Markdown/JSON/schema reference | hard fail | hard fail |
| `ipfs://`, `ar://`, content-addressed URI | syntax and hash checks | hard fail on malformed hash; availability is separately reported |
| Ethereum transaction/contract reference | syntax, chain/address checks where possible | hard fail only for malformed identity; RPC availability is non-blocking |
| allowlisted stable primary source | cached/rate-limited probe | report plus cached evidence; no network dependency in build |
| mutable API/explorer/marketplace | syntax and source metadata only | never a build blocker; snapshot/capture is required for fact promotion |
| unknown external host | warning in draft, hard fail for published source catalog | hard fail unless reviewed allowlist entry exists |

The checker should canonicalize URLs, strip fragments only for availability
probes, retain fragments for local resolution, and never follow arbitrary
redirects into a new domain without an allowlist decision. It should use a
repository cache of source headers/captures where legally permissible. It must
not rewrite links or “fix” a historical citation automatically.

## Versioning and release semantics

Use three independent version axes:

- schema and validator compatibility use SemVer (`schema-vMAJOR.MINOR.PATCH`);
  a breaking required-field or meaning change increments MAJOR;
- a governed repository snapshot uses an immutable date sequence tag
  (`museum-YYYY.MM.DD.N`), where `N` disambiguates multiple snapshots on a day;
- each record has an immutable stable ID and an integer `recordVersion`.
  Corrections increment the record version and point to `supersedes`; they do
  not recycle IDs.

The release manifest's content root is the durable identifier for on-chain
publication. A tag, Git commit, GitHub release, or `latest` pointer is a
locator, not the Museum's final trust model. If a later on-chain contract
records a manifest, it records the content root, schema system manifest, and
Stream-compatible `HashRef` rather than a mutable GitHub URL alone.

## Implementation priorities

### Priority 0: lock the invariants

Write the repository contribution standard, schema registry, canonicalization
test vectors, public-boundary rules, and status-transition table. Add fixtures
for a valid record, a fake winner-as-accession, a missing title binding, a
restricted leak, a superseding amendment, and a Stream envelope.

### Priority 1: make the current repository testable

Implement `scripts/lib/paths.py`, `canonical_json.py`, `validate.py`, and
`generate_manifest.py`. Create the initial schemas and vocabularies. Convert
the first governance, collection, program, and accession indexes into canonical
records without declaring unverified works accessioned.

### Priority 2: add deterministic publication

Implement record rendering, compatibility indexes, generated headers, and
`--check` drift detection. Ensure Windows/Linux output equality before adding
large collections.

### Priority 3: add review and source controls

Add assertions/source catalog, review blocks, CODEOWNERS, branch rules, secret /
PII scan, local link checks, and the transition gate validator. Create public
registrar-ref fixtures without committing restricted instruments.

### Priority 4: add Stream bilateral tests

Pin Stream's system manifest and profile identifiers, implement exact hash and
envelope vectors, and test Museum -> Stream -> Museum plus PREMIS/LIDO/IIIF
round trips. This is a release gate before any Museum contract design is
declared implementation-ready.

### Priority 5: populate real accessions and analysis

Use the system for the Casey Reas accession, Keys and Gates outcomes, and
future approved collections. For generative works, publish the analysis script,
input snapshot, parameters, result files, and result hashes. Never import or
display OpenSea rarity as a Museum metric.

### Priority 6: release and migration

Create immutable release artifacts, GitHub attestations, a public manifest
registry, and the migration mapping to the external-works on-chain registry.
Only after repeated clean releases and bilateral conformance should contract
deployment be considered.

## Failure modes and required responses

| Failure mode | Detection | Response |
|---|---|---|
| A wallet transfer is treated as accession | transition validator finds missing acceptance/title binding | keep state at `received_onchain`; create a correction or missing gate record |
| A Wave winner is treated as acquired | program/accession cross-reference test | record selection separately; require transaction and rights evidence |
| OpenSea rarity enters a record | forbidden-key scan and schema enum | reject PR; use transparent Museum analysis or descriptive traits only |
| Stream profile drifts | pinned manifest/hash and round-trip test | block release; update bilateral profile through reviewed change |
| JCS and SHA3 are confused | fixed Keccak/RFC8785 vectors | fail the build; never substitute NIST SHA3-256 for Ethereum Keccak |
| JSON is valid but semantically inconsistent | global index and gate validator | hard fail with subject/path/source diagnostics |
| Duplicate or recycled identifier | ID registry and lineage check | reject; issue a new ID or explicit superseding amendment |
| Reviewer is constructor | review/PR identity comparison | require an independent reviewer and record scope |
| Restricted data is committed | path policy, secret/PII scan, diff scanner | block; remove the data before merge and keep only a public hash/reference |
| Generated Markdown is hand-edited | generated header and render drift | regenerate from source; reject manual output changes |
| Windows/Linux output differs | matrix byte comparison | fix locale, path, newline, serializer, or timestamp nondeterminism |
| Remote source is temporarily unavailable | link checker class and retry policy | do not alter history; use cached/captured evidence and report inconclusive |
| Mutable URL changes after publication | source stability classification and hash mismatch | append a source correction/amendment; preserve old hash and observation |
| Network/RPC is unavailable at release time | build has no network dependency for canonical inputs | release from committed captures; report live-state refresh separately |
| A schema change silently changes interpretation | SemVer and schema diff test | require major version or explicit migration and reviewer sign-off |
| Manifest includes itself or host metadata | input allowlist and reproducibility test | exclude generated outputs; remove timestamps/paths/run IDs from content root |
| A public record leaks a private URI or identifier | public-boundary scanner and allowlist | block release; replace with restricted reference and non-sensitive custodian |
| A correction rewrites history | supersedes/hash lineage test | restore prior record; publish an append-only amendment |

## Open implementation questions

These are deliberately retained for a future constructor/reviewer decision:

- which registrar vault and public capture format will hold restricted legal
  instruments and whether it can issue stable hash-addressed receipts;
- the exact Python dependency lock and approved Ethereum Keccak backend;
- whether rendered Markdown is committed on every PR or only at governed release
  boundaries, with the first implementation favoring committed output for
  reviewability;
- the final Stream profile source bundle and the mechanism for detecting an
  upstream Stream schema publication after the current pinned commit;
- the GitHub ruleset owner and the minimum independent reviewers for a routine
  object update versus an accession, policy, or release;
- whether the future on-chain registry stores individual record heads, release
  roots, or both.

Until resolved, the conservative behavior is to fail closed on schema,
identity, privacy, review, status-transition, and Stream compatibility errors,
while treating remote availability and mutable source freshness as explicit
non-blocking observations.
