# The record outlives the interface

Status: working public operating statement; not an adopted governance policy

## An open museum, built in public

The 6529 Network Museum is not only a collection that people can visit. It is a
collection people can help make more accurate, more legible, and more useful.

The Museum's public-safe collection records, accession documents, research,
policies, and curatorial texts are maintained in the public
[`6529-Collections/6529networkmuseum`](https://github.com/6529-Collections/6529networkmuseum)
repository. Anyone can read the sources and revision history, make a copy, or
propose a correction, new evidence, a stronger interpretation, improved
accessibility, or better technical and preservation documentation through a
pull request.

Restricted donor, legal, custody-security, and personal information does not
belong in the public repository, public content-addressed storage, or public
contract state. The [contribution boundary](../CONTRIBUTING.md) and
[rights map](../RIGHTS.md) explain what may be submitted and reused.

This is more than transparency after the fact. It gives the network a practical
way to participate in the quality of its Museum.

## Open to improvement, responsible to the record

Anyone can propose an edit; no one can quietly rewrite what the Museum has
published. Accepted changes enter as reviewed, attributable revisions after
their evidence and meaning have been examined and the records have passed
deterministic validation. Pull requests keep the source, discussion,
authorship, and path of change visible to everyone.

Contributors can improve many kinds of Museum work:

- a date, title, or chain fact;
- an artist or project source;
- provenance, title, rights, condition, or preservation evidence;
- an object description or curatorial argument;
- an accessibility description or reading structure;
- a schema, validator, or reproducible research method.

The contribution guide explains how to
[propose an improvement](../CONTRIBUTING.md). Published corrections retain
lineage instead of quietly erasing the record they replace.

## Three layers, one Museum

The Museum is being built in three deliberately separate layers.

### Public record

Today, the repository is the intermediate public system of record. It is
inspectable, cloneable, group-editable through pull requests, and released with
deterministic file and manifest commitments. It lets a visitor move from an
artwork or essay to the exact material from which the page was published.

### On-chain memory

Our Fall 2026 goal is for every admitted Museum record—from governance
decisions and policies to accessions, provenance, rights, preservation events,
and later corrections—to have an on-chain commitment and append-only lineage
in a custom contract. Larger essays, images, software packages, and
preservation files can live on content-addressed storage while the contract
records their identity, schema, hash, location, authority, effective time, and
append-only history.

The contract is being designed. It has not yet been deployed or activated, and
the repository must not be mistaken for evidence that migration has occurred.

### Open display

The website is where the public encounters the art. It should be beautiful,
fast, accessible, and generous with scholarship. But a website is still an
interface: designs change, software is replaced, and domains or hosting systems
can fail.

Museum decisions, historical records, provenance, and citations should not
disappear with a frontend. The site therefore reads from the published Museum
record instead of treating the interface itself as the authority. Today that
record comes from a committed GitHub release; in the intended future it will
be resolved from on-chain commitments and content-addressed payloads without
changing the artwork's Museum identity or public URL.

## A museum the network can carry forward

The result is neither a website with an opaque database behind it nor a chain
of hashes without a meaningful public experience. It is a Museum whose art can
be encountered directly, whose claims can be examined, whose scholarship can
be improved, and whose institutional memory can survive any single team or
interface.

Explore the
[public record](https://github.com/6529-Collections/6529networkmuseum), read
[how contributions work](../CONTRIBUTING.md), or follow the
[on-chain transition](onchain-transition.md).
