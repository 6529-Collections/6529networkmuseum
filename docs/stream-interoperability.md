# 6529Stream interoperability

## Pinned source

This profile is aligned to `6529-Collections/6529Stream` `origin/main` commit `5021c8060950c3fef995271e674ed4b2007fee6d`, observed 2026-08-01 UTC.

Normative Stream sources at that commit:

- `smart-contracts/IStreamPreservationRecords.sol`
- `smart-contracts/StreamPreservationRecords.sol`
- `docs/collection-metadata-contract.md`
- `docs/metadata-router-and-renderer.md`

Stream currently implements the generic preservation record envelope and specifies the museum profile semantics. At the pinned commit it does not yet publish standalone canonical JSON Schema files for `STREAM_ACCESSION_V1`, `STREAM_WORK_DESCRIPTION_V1`, `STREAM_RIGHTS_V1`, `STREAM_PREMIS_V3_PROFILE`, or `STREAM_LIDO_PROFILE_V1`. Museum schemas therefore pin the same fields and vocabularies now and must be replaced or proven byte-compatible when Stream publishes those canonical schema documents.

## Exact on-chain envelope

Museum records intended for a Stream-compatible chain use the exact Stream shapes:

```solidity
struct HashRef {
    uint16 algorithm;
    bytes digest;
    bytes32 canonicalizationId;
}

struct CollectionRecord {
    bytes32 recordType;
    bytes32 subjectId;
    HashRef contentHash;
    string uri;
    bytes32 schemaId;
    bytes32 signatureScheme;
    HashRef signatureHash;
    uint64 effectiveAt;
}
```

The Museum must not create a semantically equivalent but field-incompatible envelope.

## Shared identifiers

| Concept | Literal | Identifier |
|---|---|---|
| Keccak-256 algorithm | `HASH_KECCAK256` | `1` |
| SHA-256 algorithm | `HASH_SHA256` | `2` |
| JSON canonicalization | `RFC8785_JCS` | `0x886c7c89c308c459ca8a626e0ef36a5ea9f4c7a7b56aaf86c71a2ddf3b4f9044` |
| Owner record type | `ACCESSION` | `0x4dc3a5e33f97bcd06f2d025349086438272d94a398185aca416ae539e36521fb` |
| Accession schema | `STREAM_ACCESSION_V1` | `0xc04bb48f95c8db4fe7f26a20106533f987003843f2fed36fd6d89f207ddfbd86` |
| Record type | `WORK_DESCRIPTION` | `0x3b172fd545b59c0d525256a31f44b4304ca8e7e06892d1ba171dff45a7f1a9e6` |
| Work-description schema | `STREAM_WORK_DESCRIPTION_V1` | `0x5bb3543c4c007f4396474b74ec81dd8bca13028b6d945020e4b48ff236b26a3c` |
| Record type | `RIGHTS_STATEMENT` | `0x45bc8cdeb4a6cf2cd35075c4e3176254f0ea24f8e938f632c52c83ef8d8434df` |
| Rights schema | `STREAM_RIGHTS_V1` | `0xdfdea1c86219c12e182b4023d399be35bd5602461ef1dc727784c18d7742b967` |
| PREMIS profile | `STREAM_PREMIS_V3_PROFILE` | `0x5df5267e55cdb4ee470cec99deebfeef16d1bb34992fa36b21a3b2e3d38ccc45` |
| LIDO profile | `STREAM_LIDO_PROFILE_V1` | `0xbb318aaa815fbe5cb8cfa584f0102a18948118afe3ba1709cadc6ae36dba22f9` |

Identifiers are `keccak256` of the exact ASCII literal unless Stream assigns a numeric algorithm ID.

## Bilateral ontology profile

The Museum and Stream use the same concepts in both directions:

- **PREMIS v3:** digital preservation Objects, Events, Agents, and Rights. Museum preservation data must round-trip through `STREAM_PREMIS_V3_PROFILE`, including LoC preservation event and outcome vocabularies.
- **LIDO/CDWA-Lite:** the work-description/tombstone record must round-trip through `STREAM_LIDO_PROFILE_V1`. Creator authority references use ULAN, VIAF, or Wikidata; medium/technique uses Getty AAT where available.
- **IIIF Presentation 3:** serious visual works should expose an archival manifest under `STREAM_IIIF_P3_MIN_V1`, with content-addressed painting resources and explicit rights/attribution.
- **BagIt/OCFL:** object dossiers use `STREAM_BAGIT_PROFILE_V1`; SHA-256 and Keccak-256 manifests coexist, and superseding dossiers become new repository versions.
- **C2PA:** optional provenance references remain hash-committed records with explicit validation status.
- **CAIP-19-shaped citation:** `eip155:<chainId>/erc721:<lowercase-core>/<tokenId>`, optionally followed by `@fin:`, `@snap:`, or `@chain:` plus a bytes32 state commitment.

## Shared accession semantics

An accession uses `STREAM_ACCESSION_V1`: accession identifier, acquiring-institution reference, and a `TITLE_BINDING`. The binding separates a legal instrument from the on-chain transfer and records:

- instrument URI/hash and non-sensitive custodian reference;
- block number and transaction hash;
- `from` and `to` addresses;
- the specific transfer to which legal title evidence relates.

The acquisition packet remains distinct from the accession statement. It includes chain identity, record-chain heads, finality/content roots, attribution, rights completeness, fixity/preservation coverage, ownership history, title bindings, work description, condition records, recovery lineage, and platform-sustainability evidence where applicable.

### Limited Museum gift authorization

`GIFT_ACCEPTANCE_AUTHORIZATION` is a versioned Museum-local envelope profile
for a formally accepted gift whose Stream `ACCESSION` completion certificate is
not yet evidence-backed. It is intentionally not an alternate spelling of
`STREAM_ACCESSION_V1`: it cannot carry an executed title binding, a signed
authority claim, or an `accessioned` lifecycle assertion. It records the
effective acceptance decision and its limitations while independent
documentation QA remains pending.

## Shared provenance-entry format

Human-facing provenance histories use the Stream manifest shape:

```json
{
  "entry_id": "stable-entry-id",
  "entry_type": "curation",
  "occurred_at": "2026-07-09T12:00:00Z",
  "title": "Selected by TDH vote",
  "description": "Selection is not accession.",
  "evidence_refs": [
    {
      "label": "Wave result",
      "uri": "https://6529.io/...",
      "sha256": "not_available_local",
      "notes": "Live API status observed at the stated snapshot."
    }
  ]
}
```

Museum-specific event types may extend Stream's vocabulary only through a versioned profile with an explicit PREMIS mapping. Existing Stream terms and meanings are never redefined.

## Convergence gate

Before deploying a Museum contract or publishing a completed accession on Stream:

1. vendor or content-address the canonical Stream profile documents;
2. compare schema IDs and document hashes against the active Stream system manifest;
3. validate Museum → Stream → PREMIS/LIDO export round trips;
4. regenerate the acquisition packet and object dossier without operator-only data;
5. reject deployment if any shared field, vocabulary, hash, or subject derivation has drifted.
