# Preservation dossier

Status: draft working template. The dossier is a preservation and access package, not a replacement token or a claim that every retained derivative is the artwork.

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
| C2PA manifest/reference | `[provenance]` | `[...]` | `[...]` | `[...]` | `[...]` | `[...]` | `[...]` |
| Technical/condition report | `[administrative]` | `[...]` | `[...]` | `[...]` | `[...]` | `[...]` | `[...]` |
| Rights/title/provenance records | `[administrative]` | `[...]` | `[...]` | `[...]` | `[...]` | `[...]` | `[...]` |

## BagIt and OCFL

- BagIt version: `[...]`
- Payload root: `data/`
- Required tag files present: `[bagit.txt | manifest-sha256.txt | tagmanifest-sha256.txt | bag-info.txt]`
- Payload manifest verified: `[yes/no/date]`
- Tag manifest verified: `[yes/no/date]`
- OCFL storage root/object/version: `[...]`
- OCFL inventory/version state: `[...]`
- OCFL fixity and digest algorithms: `[...]`
- Superseding version relationship: `[...]`

## PREMIS event register

| Event ID | Event type | Date/time | Agent | Objects | Outcome | Detail/error | Evidence/fixity |
|---|---|---|---|---|---|---|---|
| `[...]` | `[ingestion | validation | virus_check | fixity_check | render | migration | replication | recovery_test | other]` | `[...]` | `[...]` | `[...]` | `[...]` | `[...]` | `[...]` |

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
- IIIF Presentation 3 manifest: `[...]`
- Canvas/resource IDs and hashes: `[...]`
- Audio/video/text/model resource types: `[...]`
- Attribution/rights properties: `[...]`
- Accessibility derivative and alt text/transcript: `[...]`
- Surrogate disclaimer: `[...]`

## Preservation completion decision

- Preservation status: `[not_started | in_progress | complete_with_conditions | complete | blocked]`
- Completion basis: `[fixity, package, copies, event history, recovery test, rights, environment documentation]`
- Material exclusions: `[...]`
- Risk accepted by / date: `[...]`
- Reviewer and signature/hash reference: `[...]`
