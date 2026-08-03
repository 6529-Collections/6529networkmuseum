# From public repository to on-chain Museum record

Status: working public migration statement; not deployment or activation
evidence

## The goal

The 6529 Network Museum's institutional memory should not depend on GitHub, a
single website, or a single operator.

Our Fall 2026 goal is for every admitted Museum record—from governance
decisions and policies to accessions, provenance, rights, preservation events,
and later corrections—to have an on-chain commitment and append-only lineage
in a custom contract. This includes the record of what the Museum decided,
what it accepted, how an object entered the collection, which evidence
supports its identity and history, and how later corrections relate to what
came before.

The contract is being designed. It has not yet been deployed, audited,
activated, or populated. This document describes the intended transition, not
a completed technical state.

The contract will not make curatorial or governance decisions. It will
preserve who made an authorized assertion, what was asserted, when it took
effect, which evidence it commits to, and how it relates to the records that
came before.

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
provenance, preservation events, and corrections have different authorities
and meanings. The contract must preserve those differences rather than flatten
them into generic notes.

Restricted donor, legal, custody-security, and personal information does not
move into public contract state, public content-addressed storage, or the
public repository. Public records may commit to a restricted instrument by
hash and non-sensitive custodian reference without exposing its contents.

## What does not need to live in contract storage

Putting the Museum record on-chain does not mean forcing every essay, image,
video, software package, or conservation dossier into expensive contract
storage.

Large public-safe payloads can live on durable content-addressed storage. The
contract commits to the payload's identity, schema, hash, URI, authority,
effective time, and lineage. A third party can retrieve the payload and verify
that its bytes are exactly those admitted under the stated schema. Availability
and the truth of the underlying assertion remain separate questions.

The artwork itself also remains where its canonical identity places it. The
Museum registry records institutional claims about a work; it does not wrap,
remint, or replace an externally minted token.

## Why the frontend stays separate

The public website is a display and interpretation layer. It should lead with
art, make scholarship readable, and let visitors move naturally into rights,
provenance, technical, and source material.

It should not be the sole custodian of the Museum's decisions or history. A new
website, exhibition interface, research tool, or independent community client
should be able to reconstruct the same institutional record from the contract
and its committed payloads.

This separation produces a durable division of responsibility:

| Layer | Responsibility |
|---|---|
| Artwork and canonical token | The work's own chain, contract, code, metadata, and preserved manifestations |
| Museum record | Decisions, accession, provenance, rights, preservation, evidence commitments, authority, and revision lineage |
| Public display | Exhibition, interpretation, discovery, accessibility, and interaction |

The display can improve continuously without silently changing the record. The
record can acquire new evidence or corrections without erasing its history.

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
7. the website switches source adapters without changing Museum identities or
   visitor URLs.

Migration is complete only when an independent third party can reproduce the
record hashes and public exports without relying on GitHub, the original
operator, or a marketplace.

## Follow the work

- [Open Museum statement](open-museum.md)
- [General on-chain design requirements](onchain-design.md)
- [Registry design for externally minted works](external-works-registry.md)
- [Implementation-ready migration specification](../specs/onchain/contract-migration-v1.md)
- [Contributing to the Museum](../CONTRIBUTING.md)
