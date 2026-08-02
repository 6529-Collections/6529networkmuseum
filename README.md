# 6529 Network Museum

This repository is the transitional system of record for the 6529 Network Museum while the network designs durable on-chain storage. It stores the Museum's governing sources, adopted decisions, approved donation collections, accession-program outcomes, accession register, record schemas, and on-chain design.

Git history is useful evidence, but GitHub is not the final trust model. Every machine-readable release is deterministically manifested so it can later be committed to decentralized storage and an on-chain record chain.

## Canonical areas

| Area | Canonical location | Current state |
|---|---|---|
| Founding and policy | [`policies/`](policies/) | Institutional note plus adopted collecting and donation policy |
| Governance decisions | [`records/governance/decisions.json`](records/governance/decisions.json) | Six adopted decisions and two participatory proposals with no adopted effect at the snapshot |
| Preapproved donation collections | [`records/collections/approved-collections.json`](records/collections/approved-collections.json) | Autoglyphs, Art Blocks, original Rare Pepes, original CryptoPunks |
| Accession programs and selected art | [`records/programs/`](records/programs/) | Keys and Gates selection complete; acquisition/accession verification pending |
| Donations and accession work | [`records/accessions/register.json`](records/accessions/register.json) | Casey REAS seven-work gift accepted and accessioned; post-accession title, finalized-state custody, token-approval, and exact-address compliance diligence complete; autonomous software preservation remains active stewardship |
| Accession standard | [`docs/accession-standard.md`](docs/accession-standard.md) | Museum-rigorous, chain-native, Stream-aligned profile |
| Stream interoperability | [`docs/stream-interoperability.md`](docs/stream-interoperability.md) | Bilateral record and ontology contract |
| Future contract | [`docs/onchain-design.md`](docs/onchain-design.md) | Requirements and migration boundary, not deployed code |
| Externally minted works | [`docs/external-works-registry.md`](docs/external-works-registry.md) | Token-agnostic registry design; no wrapping/reminting |

## Status is deliberate

These states are not synonyms:

`offered` → `authorized` → `acquired` → `received_onchain` → `accessioned` → `catalogued` → `technically_verified` → `preservation_complete` → `display_ready`

A work can be held by a Museum wallet without being accessioned. A Wave `WINNER` can be selected without having been minted, purchased, transferred, rights-cleared, or accessioned. The records preserve those distinctions.

## Integrity and validation

Local control-plane runs require Python 3.11 or newer; `.python-version` pins
the same Python 3.12.10 patch release used by CI.

The active required check is `Museum validation`; it runs the foundation
bootstrap and full control-plane checks on every pull request and main push.
Run the complete local control plane with:

```powershell
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
python scripts/bootstrap_validate.py
python scripts/check_fetch_guard.py
python scripts/validate.py
python scripts/build_casey_diligence_manifest.py --check
python scripts/generate_manifest.py --check
```

The documentation-as-code control plane is specified in
[`docs/control-plane.md`](docs/control-plane.md). It validates JSON Schema,
controlled vocabularies, Stream envelope compatibility, canonical payload
commitments, cross-references, append-only state transitions,
constructor/reviewer separation, and public-record sensitive-field guardrails.
The pull-request workflow runs these checks on every PR.

The generated release manifest covers the governed records, governance and
review controls, protocol specifications, templates, validation source, tests,
and named root control files. The exact closed inventory is documented in
[`docs/control-plane.md`](docs/control-plane.md). Evidence remains separately
authenticated by raw-byte evidence manifests, while indexed WIP and research
notes remain outside the release authority. The manifest uses the 6529Stream
conventions:

- repository-relative POSIX paths;
- `sha256:` file digests over LF-normalized Museum-authored text;
- raw-byte SHA-256 for explicitly binary authenticated evidence snapshots, with the byte mode recorded in their evidence manifest;
- RFC 8785-compatible canonical JSON under the repository's constrained I-JSON profile;
- Keccak-256 payload commitments;
- the Stream `HashRef` algorithm and canonicalization identifiers.

Raw evidence hashes and canonical record commitments are intentionally separate domains. A release manifest must identify the applicable byte mode; it must never silently normalize an authenticated source snapshot.

## Public and restricted records

This repository contains public institutional records only. Never commit private donor contact details, non-public legal instruments, tax/appraisal material, Safe internals, hardware-wallet details, private storage locations, credentials, private keys, seed phrases, or non-public execution/signing payloads. Publicly issued upstream authenticity attestations may be retained verbatim as inert, content-addressed source evidence; they are never Museum signatures, signing authority, or executable instructions. Public records may contain a hash and a non-sensitive custodian reference to a restricted instrument.

## Source priority

When sources conflict, use live chain state for ownership/custody facts, live Wave API status for proposal status, adopted proposal text for governance effect, the applicable Meme Card for program facts, then formal institutional/program notes. Chat is context, not hidden policy.
