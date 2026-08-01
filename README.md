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
| Donations and accession work | [`records/accessions/register.json`](records/accessions/register.json) | Casey Reas donation received; work-level accession documentation in progress, not yet represented as accession complete |
| Accession standard | [`docs/accession-standard.md`](docs/accession-standard.md) | Museum-rigorous, chain-native, Stream-aligned profile |
| Stream interoperability | [`docs/stream-interoperability.md`](docs/stream-interoperability.md) | Bilateral record and ontology contract |
| Future contract | [`docs/onchain-design.md`](docs/onchain-design.md) | Requirements and migration boundary, not deployed code |
| Externally minted works | [`docs/external-works-registry.md`](docs/external-works-registry.md) | Token-agnostic registry design; no wrapping/reminting |

## Status is deliberate

These states are not synonyms:

`offered` → `authorized` → `acquired` → `received_onchain` → `accessioned` → `catalogued` → `technically_verified` → `preservation_complete` → `display_ready`

A work can be held by a Museum wallet without being accessioned. A Wave `WINNER` can be selected without having been minted, purchased, transferred, rights-cleared, or accessioned. The records preserve those distinctions.

## Integrity and validation

The complete schema and release-manifest pipeline is under construction. The active required check is:

```powershell
python scripts/bootstrap_validate.py
```

The target release manifest uses the 6529Stream conventions:

- repository-relative POSIX paths;
- `sha256:` file digests over LF-normalized Museum-authored text;
- raw-byte SHA-256 for explicitly binary authenticated evidence snapshots, with the byte mode recorded in their evidence manifest;
- RFC 8785-compatible canonical JSON under the repository's constrained I-JSON profile;
- Keccak-256 payload commitments;
- the Stream `HashRef` algorithm and canonicalization identifiers.

Raw evidence hashes and canonical record commitments are intentionally separate domains. A release manifest must identify the applicable byte mode; it must never silently normalize an authenticated source snapshot.

## Public and restricted records

This repository contains public institutional records only. Never commit private donor contact details, non-public legal instruments, tax/appraisal material, Safe internals, hardware-wallet details, private storage locations, credentials, private keys, seed phrases, or raw signatures. Public records may contain a hash and a non-sensitive custodian reference to a restricted instrument.

## Source priority

When sources conflict, use live chain state for ownership/custody facts, live Wave API status for proposal status, adopted proposal text for governance effect, the applicable Meme Card for program facts, then formal institutional/program notes. Chat is context, not hidden policy.
