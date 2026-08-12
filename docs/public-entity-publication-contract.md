# Public entity publication contract

This is the compact adapter contract for the frontend and downstream public consumers. It is a constructed, review-pending source contract, not a governance or acquisition action.

## Envelope

Every entity and relation is an existing Stream-shaped Museum envelope:

```json
{
  "$schema": "https://6529networkmuseum.org/schemas/record-envelope-v1.json",
  "envelope": {
    "recordType": "PUBLIC_ENTITY",
    "subjectId": "keccak256(6529networkmuseum.subject.public_entity.v1:<record_id>)",
    "contentHash": {"algorithm": 1, "digest": "keccak256(JCS(payload))", "canonicalizationId": "Museum RFC8785 id"},
    "uri": "https://github.com/6529-Collections/6529networkmuseum/blob/main/<path>",
    "schemaId": "keccak256(PUBLIC_ENTITY_V1)",
    "signatureScheme": "0x0000...",
    "signatureHash": {"algorithm": 2, "digest": "0x0000...", "canonicalizationId": "Museum RFC8785 id"},
    "effectiveAt": "payload.effective_at in UTC seconds"
  },
  "payload": {}
}
```

`PUBLIC_RELATION` uses the same envelope and commitments. `record_id`, `entity_id`/`relation_id`, and endpoint IDs are stable Museum IDs. Consumers must fail closed on unknown entity types, profiles, relation types, qualifiers, lifecycle labels, media roles, or affordances.

## Entity adapter

The adapter exposes `entity_type`, `preferred_label`, `canonical_route`, `entity_status`, `status_observation`, and a closed `profile`. It may expose `references`, source evidence, and typed component/manifestation/media links. It must not flatten the profile into an untyped graph or infer missing facts from a route.

Required minimums are:

- Artist: authority status, practice summary, typed name variants, and evidence.
- Work: creator entity IDs, title, creation date/status, medium, work lifecycle, current Museum relation, collection membership, and component/manifestation boundary.
- Curated Acquisition: thesis, method, program/source relation, work set or source work set, one public lifecycle label, collection effect, and independent acquisition facts.
- Acquisition Program: authority records, rules, exact source program status, and selected outcomes.
- Project/Series: scope, agent/work relations, ownership boundary, and source records.
- Organization: history, roles, authority status, and typed name variants.

The canonical Project/Series example is Magnum Photos 75 (`6529NM-PRJ-0006`) at `/museum/network/projects/magnum-photos-75`. Its retained proposal evidence supplies a named 2022 anniversary-year release context and five Work links; the Work-level ERC-721 references are tokenized manifestations/source aliases, not Work identities and not evidence of Museum title, custody, rights, accession, or Collection membership. Magnum Photos is a separate Organization entity that originates/publishes the named project only to the extent retained evidence supports that wording.

## Relation adapter

Each relation has exactly one directed source and target entity, a closed relation type, assertion status, evidence, and only that type's allowed qualifier keys. Domain/range, cardinality, duplicate-active assertion, self-link, and lifecycle-sensitive checks occur before publication. An accession relation is valid only with an actual accession entity and admitted Work; a selected outcome is not an accession.

`ENTITY_HAS_MEDIA` targets exactly one `MEDIA_REFERENCE`. The target's closed media profile is the single source of the source locator/path, subject entity, role, credit, rights statement/status, source/fixity evidence, MIME/type, dimensions where visual, observation/status, and UI affordance policy; the relation joins that identity to the subject and cannot duplicate or weaken it. There is no `image_url` escape hatch.

## Status projection

Curated Acquisition labels are exact:

`proposed_in_museum_wave`, `selected_by_museum_wave_acquisition_review_in_progress`, `selected_through_acquisition_program_acquisition_pending`, `acquisition_complete_accession_review_in_progress`, `accessioned_into_permanent_collection`, `closed_without_selection`, `withdrawn`.

Mint, payment, title, custody, rights, technical, preservation, and display facts are independent typed values with evidence. “Selected,” “accessioned,” “display ready,” and “preservation complete” cannot be derived from one another.

## Migration mapping

| Existing source | New projection |
|---|---|
| Casey `/museum/network/gifts/6529NM.2026.001` and seven `WORK_DESCRIPTION` records | Curated Acquisition `6529NM-CA-2026-001`, seven Work entities, Casey Artist/Agent, five Project/Series entities, Accession entity, Collection relations |
| Keys and Gates `/museum/network/programs/6529NM-AP-01` and 16 `selected_unminted` outcomes | Curated Acquisition `6529NM-CA-2026-002`, Acquisition Program entity `6529NM-AP-ENT-0002` at `/museum/network/acquisition-programs/keys-and-gates`, source program alias `6529NM-AP-01`, 16 status-correct Work projections, program selection and acquisition relations |
| Gift proposal `6529NM-PG-2026-001`, signed Wave drop `002bfa4f-8416-48bf-b35e-38f354e9a9f0`, and accession `6529NM.2026.002` | Curated Acquisition `6529NM-CA-2026-003`, append-only `PARTICIPATORY`, `WINNER`, and accession observations, five admitted Work entities, and permanent Collection relations |
| Retained Magnum Photos 75 source-project name and five object dossiers | Organization `6529NM-ORG-0002` and Project/Series `6529NM-PRJ-0006` at `/museum/network/projects/magnum-photos-75`, one evidence-bound originator/publisher relation, and five Project-to-Work context relations; token manifestations remain distinct from Work and accession identity |
| Existing CloudFront program manifest, Casey evidence/observation records, and signed-drop API Wave publication observation | Typed `MEDIA_REFERENCE` entities and `ENTITY_HAS_MEDIA` relations for all 28 Works (7 Casey, 16 Keys and Gates, 5 Magnum); actual Wave CloudFront presentation URLs are separate from Arweave token/source locators, with source, rights, fixity, accessibility, and affordances preserved |

The governed identity inventory also binds the 21 publishable Artist IDs to human-facing slugs, including one `HugoFaz` Artist entity shared by both of that artist's Keys and Gates Works. Work routes use only `6529NM-W-####`; source accession/object/outcome/proposal identifiers are typed aliases and permanent redirects. Relational-only Agent, Accession, and Media entities have null `public_slug` and `canonical_route`.

The live WINNER observation is a separate `WAVE_STATUS_OBSERVATION` record at `records/proposed-gifts/6529NM-PG-2026-001/wave-status-observation-2026-08-08.json`. It preserves serial `1276093`, signed `WINNER`, rating/realtime `121603214`, and `29` raters observed at `2026-08-08T10:15:02.0167151Z`; it explicitly does not establish acceptance, transfer, title, custody, rights, technical or preservation completion, accession, or Collection membership. The separate `WAVE_PUBLICATION_OBSERVATION` retains all seven proposal parts and their exact source-byte hashes, while recording that `is_signed:true` was reported by the API; it is not an independent signature or license determination.

This mapping is append-only. It does not rewrite committed source payloads, mint, transfer, deploy, or publish a Stream contract. A status observation may advance the public projection when its source evidence changes; it does not collapse independent acquisition facts into a lifecycle rung.
