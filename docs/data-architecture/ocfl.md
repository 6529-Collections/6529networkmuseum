# OCFL: preserving every version

Status: working Museum application profile; the cited standard remains authoritative

## The question

**Can the repository reconstruct every version of the object it has preserved?**

If a corrected metadata file, a new migration, or an expanded dossier silently
replaces the earlier state, the preservation record loses its history.
OCFL—the Oxford Common File Layout—defines a transparent storage layout for
versioned digital objects. Its inventories connect content digests to stored
files and connect each version to the logical paths visible in that version, so
the repository can reconstruct an earlier state after a later one becomes
current.

## In the Casey Reas accession

For *CENTURY #31*, an OCFL object might contain:

- `v1`: accession records, initial evidence, metadata response, and condition
  assessment;
- `v2`: completed post-accession custody and title diligence;
- `v3`: a self-contained generator package and reproducibility report;
- `v4`: a migrated access environment and revised preservation risk record.

Each version states what was added, changed, or removed. Unchanged content can
be deduplicated by digest without losing its presence in earlier logical states.

## What OCFL contributes

An OCFL storage root contains version declarations and one or more object
roots. An object root contains:

```text
0=ocfl_object_1.1
inventory.json
inventory.json.sha512
v1/
v2/
...
```

The inventory records a stable object `id`, the OCFL inventory type, digest
algorithm, current `head`, digest-to-physical-path `manifest`, and each version's
logical `state`. Version directories are continuous (`v1`, `v2`, `v3`) and
existing versions are immutable.

## Museum application profile

### Object boundary

The default OCFL object is one Museum accession dossier. A collection-level
object may hold shared software or dependencies when they cannot be divided
meaningfully; it receives its own stable Museum ID and explicit links to every
accession object that depends on it.

The OCFL `id` is a stable Museum preservation-object URI. A CAIP-19 string is
recorded inside the object's identity data; it does not replace the Museum ID.

### Version triggers

A new version is created for a material metadata correction, new evidence,
rights or condition amendment, preservation ingest, migration, emulation
recipe, component change, derivative replacement, or package expansion.
Routine validation that produces no record change may be an event linked to the
current version rather than an empty version.

### Content and logs

Release-relevant evidence, reports, and provenance are ordinary managed content.
They do not live only in OCFL's optional `logs` directory, which lies outside
normal object validation. Sensitive operational logs remain restricted and are
linked by non-sensitive identifiers or hashes where appropriate.

### External fixity

The Museum retains inventory and object-root digests in an independent release
record or on-chain commitment. OCFL's internal digests support integrity and
reconstruction; an external commitment strengthens detection of malicious
replacement of content and inventories together.

## What this standard leaves to the Museum

OCFL organizes and checks repository storage. It does not determine what an
artwork is, whether source files are authentic, whether rights permit copying,
which events deserve a new version, how many replicas exist, or whether a live
work remains reproducible. Those decisions belong to the Museum preservation
policy and PREMIS event record.

## For machines and implementers

### Authority and current release

- Specification family: Oxford Common File Layout.
- Current publication: **1.1.1**, released 7 November 2024 as a patch update to
  1.1.
- Object and storage-root declarations remain `ocfl_object_1.1` and `ocfl_1.1`.
- Canonical specification: [OCFL 1.1](https://ocfl.io/1.1/spec/).

### Required inventory fields

```json
{
  "id": "https://6529.io/museum/network/preservation/6529NM.2026.001.01",
  "type": "https://ocfl.io/1.1/spec/#inventory",
  "digestAlgorithm": "sha512",
  "head": "v1",
  "manifest": {},
  "versions": {
    "v1": {
      "created": "2026-08-05T00:00:00Z",
      "state": {}
    }
  }
}
```

The object-root inventory and its matching digest sidecar are required. OCFL
recommends (`SHOULD`) an inventory in each version directory; whenever one is
present, it has a matching sidecar. The Museum profile elevates that
recommendation to a local requirement, so every Museum version carries an
inventory and sidecar. A sidecar is calculated after the final inventory bytes
are written. The Museum uses deterministic JSON serialization for generated
inventories even though OCFL assigns no semantic meaning to key order.

### Validation and recovery

Every ingest passes the official validation rules and Museum extensions for
stable IDs, version triggers, content roles, public/restricted separation, and
external commitments. A recovery test rebuilds the logical state of every
version from a fresh copy of the storage root and verifies all content digests.

### BagIt relationship

A validated BagIt transfer may become content within an OCFL version. BagIt
checks one transferable snapshot; OCFL retains that snapshot and later states.
The layers are validated independently.

## The Casey Reas accession

Museum state: `conceptual_mapping`. Git and the Museum release manifest preserve valuable
version and fixity history, but the Casey dossier is not stored in an OCFL 1.1
object. No `0=ocfl_object_1.1`, OCFL inventory, version tree, or OCFL validation
report exists in the canonical package.

## Official sources

- OCFL Editors, [OCFL specifications and current release](https://ocfl.io/).
- OCFL Editors, [OCFL 1.1 specification](https://ocfl.io/1.1/spec/).
- OCFL Editors, [implementation notes](https://ocfl.io/1.1/implementation-notes/).
- OCFL Editors, [release history](https://ocfl.io/news/).
