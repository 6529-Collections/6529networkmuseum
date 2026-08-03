# Contributing to the 6529 Network Museum

The 6529 Network Museum is built in public. Its policies, collection records,
accession documents, provenance, technical research, and curatorial writing are
open for the network to inspect and improve.

You do not need to be a maintainer to contribute. A useful contribution can be
as small as a corrected date or stronger citation, or as substantial as a new
piece of object research, visual analysis, preservation evidence, or tooling.

## Ways to contribute

We welcome pull requests that provide:

- factual corrections supported by reliable evidence;
- primary sources or stronger scholarly references;
- artist, project, collection, gift, and object-level research;
- careful curatorial interpretation and visual analysis;
- provenance, rights, title, custody, condition, technical, or preservation
  research;
- clearer accessibility descriptions, captions, and reading structure;
- reproducible data, validation, and conservation tooling;
- corrections to broken links, formatting, or public documentation.

If you are unsure where a contribution belongs,
[open a GitHub issue](https://github.com/6529-Collections/6529networkmuseum/issues/new)
describing what you found and the evidence available. A maintainer can help
identify the right record.

## The published record is shared, not unreviewed

This repository is group-editable through pull requests. Anyone may fork it,
propose a change, and participate in the visible revision history. A proposal
does not become the Museum's published record until it has passed evidence
review, repository validation, and maintainer approval.

This distinction keeps the Museum open without making its institutional record
arbitrary. Every accepted contribution remains attributable through its commit
and pull-request history. When a contribution materially changes published
scholarship or evidence, the relevant record will also name the contributor or
cite the pull request. Pseudonymous credit is welcome.

## Choose the right kind of change

### Correcting a published fact

Do not silently replace a historical assertion. Explain:

1. what the current record says;
2. what should change;
3. why the change is needed;
4. which evidence supports it; and
5. whether an append-only amendment or `supersedes` record is required.

Conflicting sources can coexist with attribution until review determines which
statement, if any, should supersede another.

### Improving scholarship

Curatorial writing should make a specific, supportable argument about the art.
Distinguish documented fact, artist or platform statements, technical
observation, and Museum interpretation. Cite sources close to the claims they
support. Avoid promotional language, market framing, unsupported importance
claims, and marketplace rarity scores.

### Adding chain or technical evidence

Record the chain, contract, token, transaction, block, observation time, method,
and finality assumptions. Preserve title, custody, copyright, display rights,
and preservation rights as separate facts. A wallet transfer alone is never
proof of accession.

### Improving accessibility

Describe what a visitor needs to perceive or operate without reducing the work
to metadata. Alt text should identify the visual structure that matters; longer
descriptions can explain behavior, motion, interaction, or variation. Do not
invent sensory details that were not observed.

## Repository map

- `policies/` — founding and adopted policy sources;
- `records/governance/` — proposals and decisions;
- `records/collections/` — approved donation collections;
- `records/programs/` — accession programs and outcomes;
- `records/accessions/` — accession lots, objects, rights, technical records,
  evidence bindings, and public scholarship;
- `docs/` — Museum standards and migration design;
- `schemas/`, `scripts/`, and `tests/` — the documentation-as-code control
  plane;
- `INDEX.md` — the complete human-readable repository index.

Read `README.md`, `INDEX.md`, `docs/record-model.md`,
`docs/accession-standard.md`, and `docs/stream-interoperability.md` before
changing governed records.

## Make a pull request

1. Fork the repository and create a focused branch.
2. Change the smallest coherent set of records and documentation.
3. Add the source, observation date, and evidence class for material factual
   claims where the record model requires them.
4. Update `INDEX.md` when adding a canonical document or a durable research
   note.
5. Run the validation commands below.
6. Open a pull request explaining the issue, the proposed improvement, its
   evidence, and any uncertainty that remains.

The canonical repository is
[`6529-Collections/6529networkmuseum`](https://github.com/6529-Collections/6529networkmuseum).

## Validate locally

Use Python 3.11 or newer and install the pinned development requirements:

```powershell
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
python scripts/bootstrap_validate.py
python scripts/check_fetch_guard.py
python scripts/validate.py
python scripts/build_casey_diligence_manifest.py --check
python scripts/generate_manifest.py --check
```

If your change intentionally alters the governed release inventory, regenerate
the release manifest with `python scripts/generate_manifest.py`, inspect the
diff, and rerun the manifest check.

If you cannot run the validation suite locally, you may still open a pull
request and say so. CI will report the results, and maintainers can help with
schema and manifest mechanics.

All pull requests run the same strict Museum validation and deterministic
Ubuntu/Windows suites. Review bots may add security, privacy/evidence, media,
deployment, or general feedback according to the changed files.

## Public and restricted material

This is a public repository. Never submit private donor contact information,
non-public legal instruments, tax or appraisal material, Safe internals,
signer or hardware-wallet details, private storage locations, credentials,
private keys, seed phrases, or non-public signing payloads.

Public records may refer to a restricted instrument by a content hash and a
non-sensitive custodian reference. They must not reproduce the restricted
material.

## Rights and attribution

Only contribute text, data, or media that you have the right to submit. State
the source and applicable license. A token owner's rights are not assumed to
include copyright or unrestricted reproduction rights.

By submitting a pull request, you confirm that you have the right to contribute
the material and agree that an accepted contribution may be published,
preserved, mirrored to content-addressed storage, and represented by on-chain
commitments under the terms stated in [`RIGHTS.md`](RIGHTS.md). Artworks and
third-party source material remain subject to their own stated rights.

## Where the record is going

GitHub is the Museum's intermediate public review and publication layer. Our
Fall 2026 goal is for every admitted Museum record—from governance decisions
and policies to accessions, provenance, rights, preservation events, and later
corrections—to have an on-chain commitment and append-only lineage in a custom
contract. Larger documents and media can remain on content-addressed storage
while their identity, hash, authority, and history are committed on-chain.

The contract is being designed; it has not yet been deployed or activated.
Accepted published records are intended to migrate with their cited sources,
authority, and append-only record lineage intact. Git commits and pull-request
discussions remain part of the transitional public archive; the contract does
not claim to reproduce every GitHub event.
