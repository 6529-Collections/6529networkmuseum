# From public repository to on-chain Museum record

Status: working public migration statement; not deployment or activation
evidence

## Purpose

The 6529 Network Museum requires a durable institutional memory that can be
read independently of GitHub, the current website, and its original operators.

Our Fall 2026 goal is for every admitted Museum record—from governance
decisions and policies to accessions, provenance, rights, preservation events,
and later corrections—to have an on-chain commitment and append-only lineage
in a custom contract. This includes the record of what the Museum decided,
what it accepted, how an object entered the collection, which evidence
supports its identity and history, and how later corrections relate to what
came before.

Status: contract design in progress. Audit, deployment, activation, and record
migration remain pending.

Curatorial and governance decisions remain institutional acts. The contract
will preserve each authorized assertion: its author, content, effective time,
evidence commitment, and place in the record's history.

## What moves on-chain

Each admitted public-safe institutional record should have a state-readable
entry that commits to:

- a stable subject and record type;
- the schema that gives the record meaning;
- a canonical content hash and content-addressed location;
- the authority responsible for the assertion;
- the time at which the assertion became effective;
- its append-only position and any superseded record;
- the release from which the record was migrated.

Governance decisions, policies, approved collections, acquisition programs,
selected outcomes, accessions, work descriptions, rights statements,
provenance, preservation events, and corrections retain their distinct
authorities and meanings.

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

The public website presents the collection. It leads with art, makes
scholarship readable, and gives readers a clear path into rights, provenance,
technical documentation, and sources.

Future exhibitions, research tools, and community publications will draw on
the same institutional record preserved by the contract and its committed
documents.

The responsibilities are divided as follows:

| Layer | Responsibility |
|---|---|
| Artwork and canonical token | The work's own chain, contract, code, metadata, and preserved manifestations |
| Museum record | Decisions, accession, provenance, rights, preservation, evidence commitments, authority, and revision lineage |
| Public display | Exhibition, interpretation, discovery, accessibility, and interaction |

The public presentation may change with new exhibitions and forms of access.
New evidence and corrections enter the Museum record as attributable,
append-only revisions.

## The transition from GitHub

The public repository provides the bridge:

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

## Follow the work

- [Open Museum statement](open-museum.md)
- [General on-chain design requirements](onchain-design.md)
- [Registry design for externally minted works](external-works-registry.md)
- [Implementation-ready migration specification](../specs/onchain/contract-migration-v1.md)
- [Contributing to the Museum](../CONTRIBUTING.md)
