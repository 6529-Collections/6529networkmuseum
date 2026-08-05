# BagIt: a package that can be checked on arrival

Status: working Museum application profile; the cited standard remains authoritative

## The question

**Did every declared file arrive, and are its bytes unchanged?**

When an artist, collector, laboratory, or repository transfers a digital-art
dossier, a folder name and a download link provide little assurance. The
receiver needs a list of expected files and checksums calculated before
transfer. BagIt supplies a simple directory convention for that exchange.

A BagIt package places its payload in `data/`, declares the BagIt version, and
includes one or more manifests listing the payload files and their checksums.
The receiver can test whether every declared file is present and whether its
bytes are unchanged without yet interpreting the files.

## In the Casey Reas accession

A Casey Reas evidence bag could carry raw JSON-RPC responses, token metadata
responses, object and rights records, a condition report, generator materials
that the Museum is permitted to retain, approved reference media, and a package
readme. The receiving repository checks that every path in the manifests exists
and every checksum matches.

Passing that test means the declared bytes arrived. Curators, registrars, and
conservators still assess what those bytes mean, whether the package is
complete for the artwork, and what may be preserved or shown.

## What BagIt contributes

RFC 8493 defines a hierarchical file layout for reliable storage and transfer:

```text
casey-reas-6529NM.2026.001.01/
├── bagit.txt
├── bag-info.txt
├── manifest-sha256.txt
├── manifest-sha512.txt
├── tagmanifest-sha512.txt
└── data/
    ├── chain/
    ├── metadata/
    ├── media/
    └── museum-records/
```

Required elements are `bagit.txt`, `data/`, and at least one payload manifest.
`bag-info.txt`, tag manifests, `fetch.txt`, and other tag files are optional.
A complete bag has every required and declared file. A valid bag is complete
and all declared checksums match.

## Museum application profile

### Closed payload at release

During controlled ingest, a transfer may be incomplete. A released Museum bag
is self-contained: it does not rely on `fetch.txt` for a required payload.
Where rights or technical limits prevent retention, the Museum record describes
the missing material instead of presenting the package as complete.

### Algorithms and text conventions

The Museum creates both SHA-256 and SHA-512 payload manifests and a SHA-512 tag
manifest. Museum-authored text uses UTF-8 and LF endings. Manifest paths are
sorted by their UTF-8 byte sequence after normalization to forward slashes.
Source evidence whose exact bytes matter is retained and hashed raw, without
line-ending conversion.

### Package identity and external commitment

BagIt defines no universal bag identifier or cryptographic signature. The
Museum therefore records a stable package ID, creation event, creator, source
Museum release, per-file manifests, a deterministic archive recipe if an
archive is distributed, and an external package commitment in the release
record. A ZIP or TAR digest identifies that serialized archive, not BagIt in
general.

### Validation record

Every receipt stores the validator name and version, validation time,
algorithms, payload count and bytes, manifest digests, completeness result,
fixity result, warnings, and responsible agent. The validator output is itself
retained as evidence outside or in a later version of the bag.

## What this standard leaves to the Museum

BagIt checks declared files. It does not interpret payload semantics, establish
authorship or authenticity before packaging, determine legal title or rights,
verify a blockchain event, preserve an earlier bag state after in-place change,
or protect against an attacker able to replace both payload and manifests.

## For machines and implementers

### Authority and status

- Specification: **The BagIt File Packaging Format (V1.0)**.
- Publication: RFC 8493, October 2018.
- RFC status: Informational, Independent Submission; not Internet Standards
  Track.
- Status and verified errata: [RFC Editor record](https://www.rfc-editor.org/info/rfc8493).

### Declaration

`bagit.txt` contains exactly:

```text
BagIt-Version: 1.0
Tag-File-Character-Encoding: UTF-8
```

### Manifest line

```text
<hexadecimal message digest><two spaces><payload path>
```

RFC 8493 defines the manifest grammar; the two ASCII spaces shown above are the
Museum's deterministic writer profile. Validators must accept conforming RFC
manifest whitespace, while Museum-generated bags use this one canonical form.

Every payload file appears exactly once in each payload manifest. The Museum
rejects absolute paths, parent traversal, duplicate normalized paths, linked or
non-regular entries, unsupported algorithms, malformed UTF-8 tag files, digest
case/length errors, and extra undeclared payload files.

### Reproducibility

The profile pins the RFC including applied errata, validator version, path
normalization, text byte modes, algorithms, deterministic archive settings,
and package-level commitment algorithm. A third party must be able to rebuild
the manifest from the retained tree and obtain the same ordered entries and
digests.

## The Casey Reas accession

Museum state: `conceptual_mapping`. The Casey dossier has strong content-addressed evidence
manifests and closed inventory checks, but its directories are not RFC 8493
bags: they do not contain the required `bagit.txt`, `data/` payload root, and
BagIt payload manifests. The existing package must not be labelled BagIt until a
conformant bag is generated and independently validated.

## Official sources

- RFC Editor, [RFC 8493 status and errata](https://www.rfc-editor.org/info/rfc8493).
- RFC Editor, [RFC 8493 full specification](https://www.rfc-editor.org/rfc/rfc8493).
