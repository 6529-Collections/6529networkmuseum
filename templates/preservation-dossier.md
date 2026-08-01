# Preservation dossier

Status: documentation-only draft template. It is not a governed record or current CI-validated schema. The dossier is a preservation and access package, not a replacement token or a claim that every retained derivative is the artwork.

## Dossier envelope

- Dossier ID: `6529NM.<object-or-lot-id>-DOS01`
- Record-control block: `[instantiate exactly from record-control.md]`
- Object/lot IDs: `[...]`
- Dossier version / supersedes: `[...]`
- Package type: `[SIP intake | AIP preservation | DIP access | documentation-only | other]`
- Package creation date: `[...]`
- Preservation lead / reviewer: `[...]`
- Designated community/use case: `[...]`
- Restrictions and public/private layer: `[...]`

## Package inventory

| Component | Role | Path/URI | Format/version | Size | Hash | PREMIS object ID | Rights/restriction |
|---|---|---|---|---:|---|---|---|
| Native token metadata snapshot | `[source capture]` | `[...]` | `[...]` | `[...]` | `[...]` | `[...]` | `[...]` |
| Artwork/media bytes | `[source/master]` | `[...]` | `[...]` | `[...]` | `[...]` | `[...]` | `[...]` |
| Script/code and lockfile | `[source/master]` | `[...]` | `[...]` | `[...]` | `[...]` | `[...]` | `[...]` |
| Dependencies/runtime description | `[environment]` | `[...]` | `[...]` | `[...]` | `[...]` | `[...]` | `[...]` |
| Generated output/reference still | `[documentation surrogate]` | `[...]` | `[...]` | `[...]` | `[...]` | `[...]` | `[...]` |
| Behavioral video/audio capture | `[documentation surrogate]` | `[...]` | `[...]` | `[...]` | `[...]` | `[...]` | `[...]` |
| Artist/project statement and intent | `[descriptive]` | `[...]` | `[...]` | `[...]` | `[...]` | `[...]` | `[...]` |
| Display/install instructions | `[environment]` | `[...]` | `[...]` | `[...]` | `[...]` | `[...]` | `[...]` |
| IIIF manifest | `[access]` | `[...]` | `[...]` | `[...]` | `[...]` | `[...]` | `[...]` |
| C2PA 2.4 manifest/reference | `[provenance]` | `[...]` | `[...]` | `[...]` | `[...]` | `[...]` | `[...]` |
| Technical/condition report | `[administrative]` | `[...]` | `[...]` | `[...]` | `[...]` | `[...]` | `[...]` |
| Rights/title/provenance records | `[administrative]` | `[...]` | `[...]` | `[...]` | `[...]` | `[...]` | `[...]` |

## BagIt and OCFL

- BagIt version: `[1.0 | other/pending]`
- Payload root: `data/`
- Required `bagit.txt` present: `[yes/no/pending]`
- Required `data/` directory present: `[yes/no/pending]`
- At least one required payload manifest present (`manifest-*.txt`): `[yes/no/pending]`
- Optional `bag-info.txt` present: `[yes/no/not_applicable]`
- Optional tag manifest(s) present (`tagmanifest-*.txt`): `[yes/no/not_applicable]`
- BagIt structural validation result: `[pass/fail/not_tested/pending]`
- Payload manifest verified: `[yes/no/date]`
- Optional tag manifest verified: `[yes/no/not_applicable/date]`
- OCFL storage root/object/version: `[...]`
- OCFL inventory/version state: `[...]`
- OCFL fixity and digest algorithms: `[...]`
- Superseding version relationship: `[...]`

## PREMIS structured entities and event register

Record the structured PREMIS entities before claiming a complete preservation mapping. Use stable IDs that can be carried into a PREMIS XML/JSON export; mark the mapping `pending` when the export has not been produced.

### PREMIS Objects

| Object ID | Object category/role | File/package/resource ref | Fixity | Preservation level/significant properties | Export/mapping status |
|---|---|---|---|---|---|
| `[...]` | `[representation/file/bitstream/intellectual_entity/other]` | `[...]` | `[...]` | `[...]` | `[mapped/pending/not_applicable]` |

### PREMIS Agents

| Agent ID | Agent type | Name/version or public identifier | Role in event | Evidence/reference | Export/mapping status |
|---|---|---|---|---|---|
| `[...]` | `[person/organization/software/service/other]` | `[...]` | `[...]` | `[...]` | `[mapped/pending/not_applicable]` |

### PREMIS Rights

| Rights ID | Basis/act | Granted rights or restriction | Term/conditions | Related object(s) | Evidence/reference | Export/mapping status |
|---|---|---|---|---|---|---|
| `[...]` | `[license/statute/policy/donor instrument/other]` | `[...]` | `[...]` | `[...]` | `[...]` | `[mapped/pending/not_applicable]` |

### PREMIS Events

| Event ID | Event type | Date/time | Agent | Objects | Outcome | Detail/error | Evidence/fixity | Export/mapping status |
|---|---|---|---|---|---|---|---|---|
| `[...]` | `[ingestion/validation/virus_check/fixity_check/render/migration/replication/recovery_test/other]` | `[...]` | `[...]` | `[...]` | `[...]` | `[...]` | `[...]` | `[mapped/pending/not_applicable]` |

Include preservation Objects, Events, Agents, and Rights. Record the environment and outcome, not just a file path.

## Storage, replication, and recovery

- Storage families/copies: `[...]`
- Geographic/provider separation: `[...]`
- Access controls and secret-free public reference: `[...]`
- Fixity schedule: `[...]`
- Recovery test date/result: `[...]`
- Media/format risk: `[...]`
- Migration/emulation trigger: `[...]`
- Recovery lineage after content/provider change: `[...]`
- Next preservation review: `[...]`

## Access derivatives and IIIF

- Public derivative(s): `[...]`
- IIIF Presentation 3 manifest ID/context/export: `[...]`
- Canvas/resource IDs and hashes: `[...]`
- Audio/video/text/model resource types: `[...]`
- Attribution/rights properties: `[...]`
- Accessibility derivative and alt text/transcript: `[...]`
- Surrogate disclaimer: `[...]`

## Interoperability identifiers and exports

- PREMIS XML/JSON export or mapping reference: `[...]`
- IIIF Presentation 3 manifest ID and export/reference: `[...]`
- C2PA version: `2.4` (use the [C2PA Technical Specification 2.4](https://spec.c2pa.org/specifications/specifications/2.4/specs/C2PA_Specification.html))
- C2PA manifest/claim/asset assertion IDs and validation result: `[...]`
- OCFL storage root, object/version, inventory, and export/reference: `[...]`
- Mapping/export status: `[mapped | pending | not_applicable]`

## Preservation completion decision

- Preservation status: `[not_started | in_progress | complete_with_conditions | complete | blocked]`
- Completion basis: `[fixity, package, copies, event history, recovery test, rights, environment documentation]`
- Material exclusions: `[...]`
- Risk accepted by / date: `[...]`
- Reviewer and signature/hash reference: `[...]`
