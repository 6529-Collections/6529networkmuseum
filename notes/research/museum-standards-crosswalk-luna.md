# Luna research note — accession and donation standards crosswalk

Date: 2026-08-01 UTC
Status: WIP research and design note; not adopted policy.
Scope: born-digital/tokenized art accession and donation operating templates.
Repository scope respected: this note does not edit any Casey Reas or Keys and Gates record. It is a template-alignment addendum to the foundation crosswalk at [`notes/research/museum-standards-crosswalk.md`](museum-standards-crosswalk.md) and the current operational crosswalk at [`docs/standards-crosswalk.md`](../../docs/standards-crosswalk.md).

## Research question

How should the 6529 Network Museum turn a donation or program acquisition into a durable, publicly legible packet when the subject may be a token, a software system, a generative output, a live service, a photographic file, or a mixed digital work—and when legal title, token custody, copyright, display rights, and preservation permissions may not be the same thing?

## Evidence and source method

The research used primary or steward-maintained sources available on 2026-08-01 UTC:

- Collections Trust's public Spectrum 5.1 pages, especially the acquisition/accessioning minimum requirements and the linked procedure index.
- ICOM's Object ID page and the Getty-hosted Object ID reference for the minimum identification purpose.
- The official CIDOC CRM site for release 7.1.3 and its conceptual integration purpose.
- The official LIDO 1.1 schema documentation and primer for delivery/exchange scope.
- The Library of Congress PREMIS 3.0 pages for the Objects, Events, Rights, and Agents model.
- The official IIIF Presentation API 3.0 specification.
- The C2PA technical specification pages.
- RFC 8493 for BagIt 1.0 and the official OCFL 1.1 site.
- Public Smithsonian Institution Archives and National Museum of American History pages describing born-digital inventory, fixity, backups, metadata, lifecycle stewardship, preservation/migration/emulation, access derivatives, rights, and restrictions.
- The repository's pinned 6529Stream interoperability profile and Museum working standards.

No private Met, MoMA, or Pompidou operating procedure was used or inferred. Publicly available standards and public institutional descriptions are cited; private institutional practice is out of scope.

## Findings

### 1. Accession is a documented institutional act, not a wallet state

Spectrum's public acquisition/accessioning guidance makes policy fit, applicable law/codes, written title transfer, donor terms, unique numbering, provenance, associated rights, and ongoing cost/obligation questions operational requirements. This aligns with the Museum's existing rule that custody or a transfer alone does not equal accession.

The template consequence is a lot-level accession statement plus an object schedule, with object-specific title binding and evidence. An unsolicited transfer or a selected program submission stays in an earlier state until the required gates are met.

### 2. Object ID is a floor, not a full digital-art record

Object ID is useful because it establishes the minimum information needed to identify a cultural object. For tokenized art, that floor must be extended with native chain identity, contract/token standard, token/hash/seed, metadata retrieval, execution environment, dependencies, mutability, and behavioral/manifestation evidence. A token citation cannot replace the artwork's title, creator, medium, description, provenance, or rights record.

### 3. CIDOC CRM and LIDO solve exchange and semantic integration differently

CIDOC CRM gives the Museum a conceptual vocabulary for actors, events, times, rights, condition, creation, acquisition, custody, and information objects. It should inform linked-record design and later semantic export; it should not be flattened into a single ownership field.

LIDO 1.1 is designed for describing and delivering cultural-object metadata to online services and aggregators. It is a useful downstream view for title, object ID, creator, events, resources, rights, measurements, subjects, and credit. It is not the Museum's accession or donor-instrument ledger, so the templates keep acquisition, title binding, state gates, and restricted annex control outside the LIDO delivery view.

### 4. Preservation requires event history and environment, not only a backup URL

PREMIS's four-entity model makes the preservation dossier recordable: preservation Objects, Events, Agents, and Rights. BagIt supplies a transparent transfer/package structure with payload and tag manifests. OCFL supplies versioned, rebuildable, storage-independent object management. IIIF supplies a public presentation view, while C2PA can provide optional signed/hash-linked media provenance with an explicit validation result.

The Smithsonian public practice pages reinforce the workflow: establish intellectual and physical control at accession, inventory and assess risk, establish fixity, create backups, generate metadata, retain originals, use migration or emulation as appropriate, document actions and agents, and make access derivatives separately from the preserved source. The templates translate those principles into object-level package, event, environment, fixity, recovery, and access fields.

### 5. Public access and rights must be a publication decision

Public museum practice distinguishes access goals from legal, privacy, intellectual-property, object-availability, and preservation constraints. The public inventory template therefore requires a rights/consent check, removal of restricted details, clear surrogate labeling, and a statement of uncertainty. It does not publish donor contact information, executed instruments, appraisals, security-sensitive custody details, or private storage locations.

### 6. Record control is a machine-checkable review binding

The merged foundation validator defines the exact record-control contract. A governed JSON record has `record_status: constructed` with `review: null` until independently reviewed. A reviewed record requires `review.actor_id`, `role: reviewer`, `reviewed_at`, a 40-character lowercase immutable `reviewed_commit`, `outcome: approved`, and `payload_sha256`. The constructor and reviewer actor IDs must differ.

The payload hash is computed over the entire top-level JSON object after removing `record_control`, serialized as UTF-8 JSON with `ensure_ascii=False`, `allow_nan=False`, sorted keys, and compact `(',', ':')` separators. The hash is not a Markdown hash, file hash, signature hash, branch name, PR number, or hash of the review block. The new `templates/record-control.md` makes this exact algorithm reusable across the accession, object, rights, preservation, public, and review forms.

## Design decisions retained in the templates

1. **Lot/object split.** One accession lot captures the institutional act and shared terms. Each object has its own identity, chain facts, technical/condition report, provenance, rights, preservation, and public-release decision.
2. **Independent states.** `offered`, `authorized`, `acquired`, `received_onchain`, `accessioned`, `catalogued`, `technically_verified`, `preservation_complete`, and `display_ready` are separately observed. A single green progress label is not sufficient.
3. **Title binding.** The legal instrument is bound to a specific asset transfer (`from`, `to`, transaction, block/time, and object), while custody and accession remain separate claims.
4. **Claim-level evidence.** A–E evidence classes, source, observation time, and content hash make it possible to tell direct chain evidence from issuer/governance evidence, Museum technical observation, third-party history, and curatorial interpretation.
5. **Digital condition.** Byte fixity, metadata availability, script/dependency health, render success, behavioral equivalence, and documentation completeness are distinct observations.
6. **Rights matrix.** Display, publication, reproduction, print, derivatives, preservation/migration, accessibility, and AI training/mining are separate statuses. `unknown` is recorded instead of omitted.
7. **Preservation as a versioned dossier.** Native captures, dependencies, environment, significant properties, fixity, PREMIS events, BagIt packaging, OCFL versioning, access derivatives, and recovery tests are all represented.
8. **Public/restricted separation.** Public records expose stable identity and approved public evidence; restricted material is referred to by a hash and non-sensitive custodian only.
9. **Attestations.** Constructor, registrar/title, technical, curatorial, and independent reviewer attestations make accountability explicit and preserve disagreement/open conditions.
10. **Append-only correction.** Amendments carry `supersedes`, preserve prior hashes, and explain the reason for change.
11. **Record-control binding.** A reviewed payload is bound to an immutable commit and the canonical payload SHA-256 after removing `record_control`; prose attestations do not replace the machine-checkable review object.

## Scenario controls

### Completed Casey Reas donation

The completed Casey Reas donation is the motivating multi-object scenario. Its current canonical lot state is `donation_status: received` and `accession_status: documentation_in_progress` (accession-in-progress), while work-level accession gates remain evidence-based. The templates support one lot with one object row per donated work/token, one lot-level transfer/title schedule, and separate object-level technical/condition, rights, provenance, preservation, and public-inventory records. The actual Casey records remain outside this change; this note supplies only the operating pattern and the rule that verified values must be copied from the canonical record rather than inferred here.

### Keys and Gates unminted state

The formal Keys and Gates program model distinguishes a program selection from later minting, purchase/acquisition, transfer, rights/consent verification, custody, and accession. The templates use `selected_unminted` for a selected submission that lacks verified native token identity. In that state:

- program selection evidence is recorded with Wave URL, serial, drop ID, live status, and observation time;
- native contract/token/CAIP-19 fields remain `not_yet_assigned` or `not_applicable`;
- a title binding and custody receipt remain open;
- accession remains `not_accessioned`;
- mint/purchase/transfer/consent/technical gates are tracked as open conditions;
- if a selected work fails availability or formal terms, the outcome is recorded as a new attributed program event rather than silently replacing the selection.

This prevents a Wave `WINNER` label from becoming a false claim of minting or accession.

## Unresolved implementation questions

- Stream's pinned repository profile identifies the shared envelope and museum semantics, but standalone canonical JSON Schemas for every named Museum profile were not present at the pinned commit. A future implementation must pin or content-address those profile documents before deployment.
- The exact CRM/LIDO export profile for tokenized, dynamic, and non-EVM works needs a mapping test, especially for native token identity versus digital artwork identity.
- The first Museum registry may need adapters for non-EVM objects and non-token hybrid works; a Museum wrapper/remint must not replace the native subject.
- Public publication policy still needs an adopted decision for default image/video derivative scope, access restrictions, and correction/dispute handling.
- Restricted annex custody, retention, and independent-signature procedures require an operational owner and should not be invented in a public template.
- Preservation thresholds for dynamic service dependencies, live data, oracle inputs, emulation, and behavioral equivalence need object-specific conservation review.

## Recommendation

Adopt this packet as a reviewable working profile after checking it against the actual Casey and Keys and Gates records in their own governed workflow. Keep the templates blank and reusable; do not use them to backfill facts. Before any public accession release, run the Museum completion gate, the Stream convergence gate, technical/condition review, rights/publication review, independent review, and repository integrity checks.
