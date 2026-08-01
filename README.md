# 6529 Network Museum

This repository is the transitional system of record for the 6529 Network Museum while the network designs durable on-chain storage. It stores the Museum's governing sources, adopted decisions, approved donation collections, accession-program outcomes, accession register, record schemas, and on-chain design.

Git history is useful evidence, but GitHub is not the final trust model. Every machine-readable release is deterministically manifested so it can later be committed to decentralized storage and an on-chain record chain.

## Canonical areas

| Area | Canonical location | Current state |
|---|---|---|
| Founding and policy | [`policies/`](policies/) | Institutional note plus adopted collecting and donation policy |
| Governance decisions | [`records/governance/decisions.json`](records/governance/decisions.json) | Six adopted and two explicitly not adopted at the snapshot |
| Preapproved donation collections | [`records/collections/approved-collections.json`](records/collections/approved-collections.json) | Autoglyphs, Art Blocks, original Rare Pepes, original CryptoPunks |
| Accession programs and selected art | [`records/programs/`](records/programs/) | Keys and Gates selection complete; acquisition/accession verification pending |
| Accessioned donations | [`records/accessions/register.json`](records/accessions/register.json) | Empty until a work passes every accession gate |
| Accession standard | [`docs/accession-standard.md`](docs/accession-standard.md) | Museum-rigorous, chain-native, Stream-aligned profile |
| Stream interoperability | [`docs/stream-interoperability.md`](docs/stream-interoperability.md) | Bilateral record and ontology contract |
| Future contract | [`docs/onchain-design.md`](docs/onchain-design.md) | Requirements and migration boundary, not deployed code |
| Externally minted works | [`docs/external-works-registry.md`](docs/external-works-registry.md) | Token-agnostic registry design; no wrapping/reminting |

## Status is deliberate

These states are not synonyms:

`offered` → `authorized` → `acquired` → `received_onchain` → `accessioned` → `catalogued` → `technically_verified` → `preservation_complete` → `display_ready`

A work can be held by a Museum wallet without being accessioned. A Wave `WINNER` can be selected without having been minted, purchased, transferred, rights-cleared, or accessioned. The records preserve those distinctions.

## Integrity and validation

Run:

```powershell
python scripts/validate.py
python scripts/generate_manifest.py --check
```

The generated manifest uses the 6529Stream conventions:

- repository-relative POSIX paths;
- `sha256:` file digests over LF-normalized text;
- RFC 8785-compatible canonical JSON under the repository's constrained I-JSON profile;
- Keccak-256 payload commitments;
- the Stream `HashRef` algorithm and canonicalization identifiers.

## Public and restricted records

This repository contains public institutional records only. Never commit private donor contact details, non-public legal instruments, tax/appraisal material, Safe internals, hardware-wallet details, private storage locations, credentials, private keys, seed phrases, or raw signatures. Public records may contain a hash and a non-sensitive custodian reference to a restricted instrument.

## Source priority

When sources conflict, use live chain state for ownership/custody facts, live Wave API status for proposal status, adopted proposal text for governance effect, the applicable Meme Card for program facts, then formal institutional/program notes. Chat is context, not hidden policy.
