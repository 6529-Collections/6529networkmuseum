# From public repository to on-chain Museum record

This document sets out the proposed migration of the Museum's public record
from GitHub to a custom on-chain registry.

## Purpose

The Museum needs records that remain readable and verifiable beyond GitHub,
the current website, and its original operators.

The stated Fall 2026 goal is for every admitted Museum record—from governance
decisions and policies to accessions, provenance, rights, preservation events,
and later corrections—to have an on-chain commitment and append-only lineage
in a custom contract. This includes the record of what the Museum decided,
what it accepted, how an object entered the collection, which evidence
supports its identity and history, and how later corrections relate to what
came before.

The contract will record each authorized assertion with its author, content,
effective time, evidence commitment, and place in the record's history.

## What moves on-chain

Each admitted public-safe institutional record receives a state-readable
entry that commits to:

- a stable subject and record type;
- the schema that gives the record meaning;
- a canonical content hash and content-addressed location;
- the authority responsible for the assertion;
- the time at which the assertion became effective;
- its append-only position and any superseded record;
- the release from which the record was migrated.

The registry keeps governance decisions, policies, approved collections,
acquisition programs, selected outcomes, accessions, work descriptions, rights
statements, provenance, preservation events, and corrections as separate
record types with their own authorities and meanings.

Restricted donor, legal, custody-security, and personal information remains in
the restricted registrar record. A public record may cite a restricted
instrument by hash and non-sensitive custodian reference.

## Content-addressed documents and media

Essays, images, video, software packages, and conservation dossiers can remain
outside contract storage.

Large public-safe payloads can live on durable content-addressed storage. The
contract commits to the payload's identity, schema, hash, URI, authority,
effective time, and lineage. A third party can retrieve the payload and verify
that its bytes are exactly those admitted under the stated schema. Availability
and the truth of the underlying assertion remain separate questions.

An externally minted artwork retains its canonical token identity. The Museum
registry records the institution's claims about that work while leaving its
contract and token unchanged.

## Exhibition and interpretation

The public website presents the collection and links each work to rights,
provenance, technical documentation, and sources. Future exhibitions, research
tools, and community publications will draw on the same institutional record
preserved by the contract and its committed documents.

The responsibilities are divided as follows:

| Layer | Responsibility |
|---|---|
| Artwork and canonical token | The work's own chain, contract, code, metadata, and preserved manifestations |
| Museum record | Decisions, accession, provenance, rights, preservation, evidence commitments, authority, and revision lineage |
| Public display | Exhibition, interpretation, discovery, accessibility, and interaction |

Public presentation may change with new exhibitions and forms of access.
New evidence and corrections enter the Museum record as attributable,
append-only revisions.

## The transition from GitHub

Before migration, the repository is the public review and release layer:

1. records are written and reviewed in public;
2. automated validation checks their schemas, relationships, evidence
   boundaries, and status claims;
3. each governed release receives deterministic SHA-256 and Keccak
   commitments;
4. payloads and schemas are published to content-addressed storage;
5. the custom contract admits the records with their authority and lineage;
6. public indexes are regenerated from chain state and committed payloads;
7. the website begins reading from the contract without changing Museum
   identities or visitor addresses.

Migration will be complete when an independent third party can reproduce the
record hashes and public exports directly from contract state and committed
payloads.

### Release and export invariant

The repository release format is `6529NM_RECORD_MANIFEST`, version `1.0.0`.
Its governed inventory is the exact union of `inventory_roots` and
`inventory_files` declared in the manifest. The generator rejects symbolic
links, reparse points, duplicate JSON keys, missing configured paths, and
non-regular inventory entries. It writes POSIX-style relative paths in
lexicographic order.

Each entry contains `path`, LF-normalized byte `size`, and SHA-256 over those
normalized bytes. JSON entries also contain Keccak-256 over RFC 8785 JCS using
the `museum-i-json-v1` profile and canonicalization ID
`0x886c7c89c308c459ca8a626e0ef36a5ea9f4c7a7b56aaf86c71a2ddf3b4f9044`.
The manifest's SHA-256 and Keccak-256 commitments cover the same JCS-encoded
manifest body before either commitment field is added.

Contract readback exports must reproduce this schema, inventory ordering,
hash rules, record identities, and append-only lineage from contract state and
committed payloads. A Git commit may document the repository edition that
preceded migration; it is not required to verify a contract-derived export.

## Follow the work

- [Open Museum statement](open-museum.md)
- [General on-chain design requirements](onchain-design.md)
- [Registry design for externally minted works](external-works-registry.md)
- [Implementation-ready migration specification](../specs/onchain/contract-migration-v1.md)
- [Contributing to the Museum](../CONTRIBUTING.md)
