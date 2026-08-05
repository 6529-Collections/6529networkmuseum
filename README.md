# 6529 Network Museum

This repository is the 6529 Network Museum's transitional system of record. It
contains the Museum's governing sources, adopted decisions, approved donation
collections, accession-program outcomes, accession register, record schemas,
and on-chain design.

Each machine-readable release carries a deterministic manifest. These
commitments prepare the record for content-addressed storage and an append-only
on-chain history.

## Public record and contribution

This repository is the Museum's shared record during the transition to an
on-chain system. Anyone can read its sources and revision history, clone the
repository, or propose a correction, new evidence, stronger scholarship,
improved accessibility, or better technical and preservation documentation
through a pull request.

Changes enter the published record after evidence review, deterministic
validation, and maintainer approval. The process keeps each revision
attributable and gives the network a direct way to improve the Museum. Start with
[`CONTRIBUTING.md`](CONTRIBUTING.md), or read
[`The record outlives the interface`](docs/open-museum.md).

The stated Fall 2026 goal is to give every admitted Museum record—from governance
decisions and policies to accessions, provenance, rights, preservation events,
and later corrections—an on-chain commitment and append-only lineage in a
custom contract. Larger documents and media may remain on content-addressed
storage. The website will present the collection from that durable record.
Contract design is in progress; deployment and activation remain pending. See
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
| Institutional practice | [`records/institutional-practice/`](records/institutional-practice/) | Digital-art-weighted comparative essay, twenty-seven primary-source profiles, a classified chain-native adjacent-practice study, detailed source notes, and [deterministic citation inventory](docs/institutional-source-inventory.json) |
| Scholarship and editorial standard | [`docs/curatorial-publication-standard.md`](docs/curatorial-publication-standard.md) | Research substance, close looking, evidence, publication architecture, digital-art scholarship, and Museum prose style |
| Museum data architecture | [`docs/data-architecture.md`](docs/data-architecture.md) | Plain-language and machine-readable profile for Spectrum, CIDOC CRM, LIDO, PREMIS, PROV-O, Getty vocabularies, IIIF, C2PA, BagIt, OCFL, and CAIP-19, with the Casey Reas implementation audit and exact seven-object machine schedule |
| Digital art stewardship | [`docs/digital-art-stewardship-standard.md`](docs/digital-art-stewardship-standard.md) | Work identity, components, artist documentation, manifestations, interventions, preservation packages, reproducibility, service exit, and public/restricted records |
| Accession standard | [`docs/accession-standard.md`](docs/accession-standard.md) | Museum-rigorous, chain-native profile governed by the Museum data architecture |
| Public Museum experience | [`docs/public-museum-experience-standard.md`](docs/public-museum-experience-standard.md) | Art-first replacement frontend standard, including media, scholarship, discovery, accessibility, and release acceptance |
| Program media delivery | [`docs/program-media-delivery.md`](docs/program-media-delivery.md) | Deterministic responsive derivatives, source fixity, immutable CDN keys, high-resolution access, rights boundaries, and verification |
| Open Museum | [`docs/open-museum.md`](docs/open-museum.md) | Public, group-editable repository phase and durable separation between record and display |
| On-chain transition | [`docs/onchain-transition.md`](docs/onchain-transition.md) | Visitor-facing Fall 2026 target, contract/content-addressed boundary, and explicit non-deployment status |
| Contributing | [`CONTRIBUTING.md`](CONTRIBUTING.md) | Public contribution paths, evidence expectations, correction rules, validation, and safety boundary |
| Rights map | [`RIGHTS.md`](RIGHTS.md) | CC0 default for Museum-authored public material and explicit limits for artworks, media, evidence, and other third-party material |
| Stream interoperability | [`docs/stream-interoperability.md`](docs/stream-interoperability.md) | Downstream envelope and contract compatibility; field-by-field ontology convergence follows the Museum profile |
| Future contract | [`docs/onchain-design.md`](docs/onchain-design.md) | Requirements and migration boundary, not deployed code |
| Externally minted works | [`docs/external-works-registry.md`](docs/external-works-registry.md) | Token-agnostic registry design; no wrapping/reminting |

## Collection status

For chain-native objects, the Museum records each stage separately:

`offered` → `authorized` → `acquired` → `received_onchain` → `accessioned` → `catalogued` → `technically_verified` → `preservation_complete` → `display_ready`

For non-token and hybrid objects, the applicable off-chain receipt, title, and
custody events replace `received_onchain`.

Wallet custody records receipt. A reviewed accession act is separate. A Wave
`WINNER` records selection; minting, purchase, transfer, rights clearance, and
accession each require their own evidence.

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
python scripts/generate_institutional_source_inventory.py --check
python scripts/generate_program_media.py --check
python scripts/build_casey_diligence_manifest.py --check
python scripts/generate_manifest.py --check
```

The documentation-as-code control plane is specified in
[`docs/control-plane.md`](docs/control-plane.md). It validates JSON Schema,
controlled vocabularies, Museum data-profile invariants, Stream envelope compatibility, canonical payload
commitments, cross-references, append-only state transitions,
constructor/reviewer separation, and public-record sensitive-field guardrails.
The pull-request workflow runs these checks on every PR.

The generated release manifest covers the governed records, governance and
review controls, protocol specifications, templates, validation source, tests,
and named root control files. The exact closed inventory is documented in
[`docs/control-plane.md`](docs/control-plane.md). Evidence remains separately
authenticated by raw-byte evidence manifests. Indexed WIP and research notes
remain outside the release authority except for the published Casey Reas
generative-system dossiers under
`notes/research/generative-systems/casey-reas/`. The manifest uses deterministic
content and hash conventions that also remain compatible with 6529Stream:

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
