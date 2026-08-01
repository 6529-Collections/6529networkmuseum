# External works registry — initial analysis

Status: WIP analysis
Date: 2026-08-01 UTC

## Problem

6529Stream is the primary-minting protocol. Its implemented preservation registry is anchored to `StreamCore` collections and validates that a `collectionId` exists in that Core. Museum donations and secondary acquisitions generally retain their original token identity and were minted by unrelated contracts or on other chains.

Those works cannot be made first-class Stream collection records merely by placing them in the Museum wallet. Wrapping or reminting them would create a second token identity and could confuse provenance, ownership, rights, and conservation claims.

The detailed recommended architecture is maintained in `docs/external-works-registry.md`.

## Options

### A. Wrap or remint every external work

Not recommended. It changes the public identity surface, creates custody and bridge risk, and invites the false claim that the wrapper is the original artwork.

### B. Extend StreamCore/StreamPreservationRecords to arbitrary external contracts

Not recommended as the primary architecture. It expands a primary-minting protocol into an institutional registry, weakens module boundaries, and still does not cover non-EVM assets or Museum governance.

### C. Deploy a token-agnostic Museum registry

Recommended. The registry records Museum statements about original assets without minting or transferring a replacement token. It reuses Stream's hashes, schemas, record semantics, and museum ontologies.

## Bilateral rule

Shared object payloads use the same `STREAM_ACCESSION_V1`, `STREAM_WORK_DESCRIPTION_V1`, `STREAM_RIGHTS_V1`, PREMIS, LIDO, IIIF, condition, dossier, and acquisition-packet semantics.

The original asset remains identified by its native chain/contract/token. The Museum registry supplies institutional authority and an append-only record chain. For a Stream-native asset, the same canonical payload can be committed in Stream's owner lane and cross-referenced by the Museum registry.

## Open questions

- Whether the first deployment should support only Ethereum/EVM subjects while leaving the subject format chain-agnostic.
- Whether same-chain custody verification should be mandatory at accession or recorded through an adapter result.
- How Counterparty/Bitcoin Rare Pepes and other non-EVM objects should obtain canonical CAIP-compatible subject identifiers.
- Whether governance decisions live in the same registry or a separate governance registry.
- Whether payload bytes should be stored on-chain for small meaning-bearing records or always referenced through content-addressed storage.
- Which party may publish a correction after registrar or custody authority rotates.
