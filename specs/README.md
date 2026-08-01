# Protocol specifications

This directory contains implementation-ready protocol specifications that may
move the Museum's governed records from GitHub to decentralized storage and
on-chain registries. A specification is a design record, not deployed code,
contract authority, or evidence that a migration occurred.

Every specification must:

- identify its status, version, dependencies, and pinned source commitments;
- preserve the repository's distinctions among governance, title, custody,
  rights, accession, preservation, and display readiness;
- use the Museum's Stream-aligned identifiers, hash references, canonicalization
  profile, and provenance ontology where concepts overlap;
- define fail-closed authorization, migration, correction, supersession, and
  conformance behavior with reproducible test vectors;
- distinguish externally minted works from primary mints without wrapping,
  reminting, or implying ownership of an underlying token contract; and
- receive independent exact-commit review before it can be presented as an
  approved implementation target.

The deterministic release manifest commits this directory. `notes/` remains a
working notebook; design work belongs here only when it is coherent enough for
formal review.
