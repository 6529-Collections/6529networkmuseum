# 6529 Network Museum

This repository is the transitional system of record for the 6529 Network Museum while the network designs durable on-chain storage. It stores the Museum's governing sources, adopted decisions, approved donation collections, accession-program outcomes, accession register, record schemas, and on-chain design.

Git history is useful evidence, but GitHub is not the final trust model. Every machine-readable release is deterministically manifested so it can later be committed to decentralized storage and an on-chain record chain.

## An open museum, built in public

This repository is not only available for inspection. It is the Museum's
shared working record during the transition to an on-chain system: anyone can
read its sources and revision history, make a copy, and propose a correction,
new evidence, stronger scholarship, improved accessibility, or better
technical and preservation documentation through a pull request.

The published record changes only after review and deterministic validation.
That preserves institutional integrity while giving the network a practical
way to improve its Museum. Start with
[`CONTRIBUTING.md`](CONTRIBUTING.md), or read
[`The record outlives the interface`](docs/open-museum.md).

Our Fall 2026 goal is for every admitted Museum record—from governance
decisions and policies to accessions, provenance, rights, preservation events,
and later corrections—to have an on-chain commitment and append-only lineage
in a custom contract. Larger documents and media can remain on
content-addressed storage. The website remains a replaceable display and
interpretation layer, separate from the Museum's durable record. The contract
is being designed; it has not yet been deployed or activated. See
[`From public repository to on-chain Museum record`](docs/onchain-transition.md).

## Canonical areas

| Area | Canonical location | Current state |
|---|---|---|
| Founding and policy | [`policies/`](policies/) | Institutional note plus adopted collecting and donation policy |
| Governance decisions | [`records/governance/decisions.json`](records/governance/decisions.json) | Six adopted decisions and two participatory proposals with no adopted effect at the snapshot |
| Preapproved donation collections | [`records/collections/approved-collections.json`](records/collections/approved-collections.json) | Autoglyphs, Art Blocks, original Rare Pepes, original CryptoPunks |
| Accession programs and selected art | [`records/programs/`](records/programs/) | Keys and Gates selection complete; acquisition/accession verification pending |
| Donations and accession work | [`records/accessions/register.json`](records/accessions/register.json) | Casey REAS seven-work gift accepted and accessioned; post-accession title, finalized-state custody, token-approval, and exact-address compliance diligence complete; autonomous software preservation remains active stewardship |
| Public scholarship | [`records/accessions/6529NM.2026.001/public/`](records/accessions/6529NM.2026.001/public/) | Casey Reas artist monograph, seven-work collection and gift narratives, five project essays, seven object entries, and the supporting source-and-chronology matrix |
| Accession standard | [`docs/accession-standard.md`](docs/accession-standard.md) | Museum-rigorous, chain-native, Stream-aligned profile |
| Public Museum experience | [`docs/public-museum-experience-standard.md`](docs/public-museum-experience-standard.md) | Art-first replacement frontend standard, including media, scholarship, discovery, accessibility, and release acceptance |
| Open Museum | [`docs/open-museum.md`](docs/open-museum.md) | Public, group-editable repository phase and durable separation between record and display |
| On-chain transition | [`docs/onchain-transition.md`](docs/onchain-transition.md) | Visitor-facing Fall 2026 target, contract/content-addressed boundary, and explicit non-deployment status |
| Contributing | [`CONTRIBUTING.md`](CONTRIBUTING.md) | Public contribution paths, evidence expectations, correction rules, validation, and safety boundary |
| Rights map | [`RIGHTS.md`](RIGHTS.md) | CC0 default for Museum-authored public material and explicit limits for artworks, media, evidence, and other third-party material |
| Stream interoperability | [`docs/stream-interoperability.md`](docs/stream-interoperability.md) | Bilateral record and ontology contract |
| Future contract | [`docs/onchain-design.md`](docs/onchain-design.md) | Requirements and migration boundary, not deployed code |
| Externally minted works | [`docs/external-works-registry.md`](docs/external-works-registry.md) | Token-agnostic registry design; no wrapping/reminting |

## Status is deliberate

These states are not synonyms:

`offered` → `authorized` → `acquired` → `received_onchain` → `accessioned` → `catalogued` → `technically_verified` → `preservation_complete` → `display_ready`

A work can be held by a Museum wallet without being accessioned. A Wave `WINNER` can be selected without having been minted, purchased, transferred, rights-cleared, or accessioned. The records preserve those distinctions.

## Integrity and validation

Local control-plane runs require Python 3.11 or newer. CI is pinned to Python
3.12.10.

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
