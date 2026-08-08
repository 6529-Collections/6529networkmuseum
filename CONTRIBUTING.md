# Contributing to the 6529 Network Museum

The 6529 Network Museum publishes its policies, collection records, accession
documents, provenance, technical research, and curatorial writing in public.
Anyone may inspect this material and propose an improvement.

Contributions range from a corrected date or stronger citation to new object
research, visual analysis, preservation evidence, or tooling.

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

## Pull requests preserve attribution

Anyone may fork the repository, propose a change, and participate in its visible
revision history. Evidence review, repository validation, and maintainer
approval determine which proposals enter the Museum's published record.

Every accepted contribution remains attributable through its commit and
pull-request history. A material change to scholarship or evidence also names
the contributor in the relevant record or cites the pull request. Pseudonymous
credit is welcome.

## Choose the right kind of change

### Correcting a published fact

A correction preserves the published assertion's lineage. It names the current
statement, proposed replacement, reason for the change, supporting evidence,
and whether an append-only amendment or `supersedes` record is required.

Conflicting sources can coexist with attribution until review determines which
statement, if any, should supersede another.

### Improving scholarship

Curatorial writing makes a specific, supportable argument about the art.
Distinguish documented fact, artist or platform statements, technical
observation, and Museum interpretation. Cite sources close to the claims they
support. Exclude promotional language, market framing, unsupported importance
claims, and marketplace rarity scores.

### Adding chain or technical evidence

Use CAIP-19-shaped citations for on-chain objects. Record the chain, contract,
token, transaction, block, observation time, method, and finality assumptions.
Preserve title, custody, copyright, display rights, and preservation rights as
separate facts. Accession requires its own reviewed record; wallet custody,
transfers, airdrops, and Wave `WINNER` labels establish other facts.

### Improving accessibility

Describe what a visitor needs to perceive or operate. Alt text should identify
the visual structure that matters; longer descriptions can explain behavior,
motion, interaction, or variation. Base every sensory detail on direct
observation.

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

A pull request starts with a focused branch and the smallest coherent set of
records and documentation. Include sources, observation dates, and evidence
classes where the record model requires them; use live API status and
observation time for governance claims; update `INDEX.md` when adding a
canonical document or durable research note; run the validation commands; then
explain the issue, proposed change, evidence, and remaining uncertainty.

The canonical repository is
[`6529-Collections/6529networkmuseum`](https://github.com/6529-Collections/6529networkmuseum).

## Validate locally

Use Python 3.11 or newer and install the pinned development requirements:

```powershell
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
python scripts/bootstrap_validate.py
python scripts/check_fetch_guard.py
python scripts/verify_casey_snapshot_package.py
python scripts/migrate_public_entities.py --check
python scripts/validate.py
python scripts/build_casey_diligence_manifest.py --check
python scripts/generate_institutional_source_inventory.py --check
python scripts/generate_manifest.py --check
```

If your change intentionally alters the governed release inventory, regenerate
the release manifest with `python scripts/generate_manifest.py`, inspect the
diff, and rerun the manifest check.

Contributors who cannot run the validation suite locally may open a pull
request and identify the omitted checks. CI will report the results, and
maintainers can help with schema and manifest mechanics.

All pull requests run the same strict Museum validation and deterministic
Ubuntu/Windows suites. Review bots may add security, privacy/evidence, media,
deployment, or general feedback according to the changed files.

## Public and restricted material

This is a public repository. Never submit private donor contact information,
non-public legal instruments, tax or appraisal material, Safe internals,
signer or hardware-wallet details, private storage locations, credentials,
private keys, seed phrases, or non-public signing payloads.

Public records may refer to a restricted instrument by a content hash and a
non-sensitive custodian reference. The restricted material remains outside the
public record.

## Rights and attribution

Only contribute text, data, or media that you have the right to submit. State
the source and applicable license. Token ownership and copyright are separate;
record the reproduction rights supplied by the applicable license or grant.

By submitting a pull request, you confirm that you have the right to contribute
the material and agree that an accepted contribution may be published,
preserved, mirrored to content-addressed storage, and represented by on-chain
commitments under the terms stated in [`RIGHTS.md`](RIGHTS.md). Artworks and
third-party source material remain subject to their own stated rights.

## Where the record is going

GitHub is the Museum's intermediate public review and publication layer. The stated
Fall 2026 goal is for every admitted Museum record—from governance decisions
and policies to accessions, provenance, rights, preservation events, and later
corrections—to have an on-chain commitment and append-only lineage in a custom
contract. Larger documents and media can remain on content-addressed storage
while their identity, hash, authority, and history are committed on-chain.

Contract design is in progress; deployment and activation remain pending.
Accepted records will migrate with their cited sources, authority, and
append-only lineage. Git commits and pull-request discussions remain part of
the transitional public archive. Admitted Museum publications define the
contract record; Git history retains the repository's broader activity.
