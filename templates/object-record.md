# Individual object record

Status: draft working template. Complete one record per artwork/object even when several objects share an accession lot or donor instrument.

## Record envelope

- Record type: `OBJECT_RECORD`
- Object ID: `6529NM.<year>.<sequence>.<item>`
- Accession lot: `[...]`
- Record-control block: `[instantiate exactly from record-control.md]`
- `record_control.record_status`: `[constructed | reviewed]`
- Object lifecycle state: `[draft | selected_unminted | acquired | accessioned | catalogued | technically_verified | preservation_complete | display_ready | amended | superseded]`
- Created at / effective at / revision: `[...]`
- Supersedes / amendment: `[none | record ID]`
- Constructor and reviewer refs: `[...]`

## Identification and description

- Object/work title: `[...]`
- Title type: `[artist title | project title | token title | supplied title | Museum title | untitled]`
- Creator/artist display name: `[...]`
- Creator authority identifiers (ULAN/VIAF/Wikidata/other): `[...]`
- Creation date/range: `[...]`
- Mint/release date: `[...]`
- Object/work type and classification: `[...]`
- Medium/technique: `[...]`
- Dimensions/aspect/duration/edition: `[...]`
- Project/series/collection: `[...]`
- Platform/contract standard: `[...]`
- Credit line: `[...]`
- Controlled-vocabulary terms and sources: `[...]`
- Description (controlled, non-promotional): `[...]`
- Significance and collection relationship: `[...]`

Describe the artwork as more than its token. State whether the token, contract, hash/seed, community, minting structure, or network context is part of the work's meaning, and identify the evidence for that interpretation.

## Native identity and state

- Subject state: `[native_token_verified | non_token_digital_object | hybrid | selected_unminted | not_yet_assigned]`
- Blockchain/network and numeric chain ID: `[...]`
- Token standard: `[...]`
- Contract address: `[...]`
- Token ID: `[...]`
- Project/collection ID: `[...]`
- Token hash/seed/randomness input: `[...]`
- CAIP-19-shaped citation: `[...]`
- Native metadata URI(s) and retrieval date: `[...]`
- Mint transaction/block/time: `[...]`
- Acquisition/receipt transaction/block/time: `[...]`
- Last custody verification block/time: `[...]`
- State qualifier/commitment (`@fin`, `@snap`, or `@chain` where used): `[...]`

If `subject_state` is `selected_unminted`, set all unverified chain identity fields to `not_yet_assigned` or `not_applicable`; preserve the program selection evidence in the state-gate worksheet; do not fabricate a CAIP-19 citation.

## Title, custody, and provenance references

- Legal title status: `[verified | pending | disputed | not_applicable | unknown]`
- Title-binding record: `[...]`
- Current Museum custody status: `[verified | pending | not_in_custody | not_applicable]`
- Custody record/reference: `[...]`
- Provenance schedule: `[...]`
- Artist/issuer statement: `[...]`
- Third-party historical evidence: `[...]`
- Conflicts and unresolved claims: `[...]`

## Technical constitution

- Work bytes or retrieval path: `[...]`
- Script/code location, version, and hash: `[...]`
- Language/runtime/browser/hardware: `[...]`
- Dependencies and exact versions: `[...]`
- Metadata snapshot and hash: `[...]`
- Generator/rendering mechanism: `[...]`
- Mutability and administrative controls: `[...]`
- Owner/artist/platform parameters: `[...]`
- Network/audio/timing/interaction requirements: `[...]`
- Randomness model and known rendering variance: `[...]`
- Artist intent/significant properties: `[...]`
- Technical/condition report: `[...]`

## Condition and manifestation

- Overall technical condition: `[green | amber | red | not_assessed]`
- Token/contract condition: `[...]`
- Metadata/media condition: `[...]`
- Script/dependency condition: `[...]`
- Rendering condition: `[...]`
- Behavioral/interaction condition: `[...]`
- Documentation/fixity condition: `[...]`
- Manifestation(s): `[live | static | video | audio | interactive | mixed | not_tested]`
- Display environment and restart/network behavior: `[...]`
- Fallback and accessibility plan: `[...]`
- Test capture(s) and hash(s): `[...]`

## Rights and donor terms

- Rights/donor-transfer record: `[...]`
- Copyright/authorial-rights status: `[...]`
- Token/title rights status: `[...]`
- Display/exhibition: `[granted | not_granted | conditional | unknown | not_applicable]`
- Public catalogue/publication: `[granted | not_granted | conditional | unknown | not_applicable]`
- Reproduction: `[granted | not_granted | conditional | unknown | not_applicable]`
- Print/merchandising: `[granted | not_granted | conditional | unknown | not_applicable]`
- Derivative/adaptation: `[granted | not_granted | conditional | unknown | not_applicable]`
- Preservation/migration/emulation: `[granted | not_granted | conditional | unknown | not_applicable]`
- AI training/mining: `[granted | not_granted | conditional | unknown | not_applicable]`
- Required attribution/credit: `[...]`
- Restrictions and expiry/review date: `[...]`

## Preservation and public access

- Preservation dossier: `[...]`
- PREMIS object/event/agent/right refs: `[...]`
- BagIt package/manifest: `[...]`
- OCFL object/version: `[...]`
- IIIF manifest/canvases: `[...]`
- C2PA reference and validation status: `[...]`
- Public inventory record: `[...]`
- Display/publication status: `[not_ready | restricted | pending | ready]`
- Documentation surrogate disclaimer: `[...]`

## Evidence register

| Claim or field group | Evidence class | Source/URI | Observation date | Content hash | Constructor note |
|---|---|---|---|---|---|
| `[...]` | `[A-E]` | `[...]` | `[...]` | `[...]` | `[...]` |

## Curatorial and revision history

- Selection rationale: `[...]`
- Curatorial statement reference: `[...]`
- Bibliography/exhibition/publication history: `[...]`
- Research notes: `[...]`

| Revision | Effective date | Supersedes | Change/reason | Evidence | Reviewer |
|---|---|---|---|---|---|
| `[v1]` | `[...]` | `[none]` | `[...]` | `[...]` | `[...]` |
