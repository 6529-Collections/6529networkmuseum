# Born-digital and tokenized art operating templates

Status: documentation-only draft templates. These Markdown files are not governed records, schemas, or adopted policy; they do not create, amend, or complete a Museum accession by themselves. The executable control plane in PR #7 is separate: until matching schemas, cross-record invariants, state/publication gates, and constructor/reviewer commit/payload binding are merged for this template family, current CI does not validate these forms or their cross-record relationships.

These templates are the operational layer below the governing working standard [`docs/accession-standard.md`](../docs/accession-standard.md). The field-level implementation crosswalk is [`docs/standards-crosswalk.md`](../docs/standards-crosswalk.md); it explains how this application profile maps to external standards. The templates are designed for born-digital, generative, software, photographic, video, audio, interactive, and tokenized works. They keep the original artwork, the token, legal title, custody, rights, technical dependencies, and preservation copies as related but non-identical facts.

## Packet map

| Template | Use | Record boundary |
|---|---|---|
| [`record-control.md`](record-control.md) | Instantiate the exact constructor/reviewer and canonical payload-hash contract | Top-level governed JSON `record_control` block |
| [`accession-state-gates.md`](accession-state-gates.md) | Gate offered or selected material through authorization, acquisition, receipt, accession, cataloguing, technical verification, preservation, and display | Workflow state; not an accession record |
| [`accession-lot.md`](accession-lot.md) | Establish one accession act for one donation, purchase, transfer, or program outcome | Lot-level institutional act and object schedule |
| [`object-record.md`](object-record.md) | Describe one artwork/object in the lot | One object, one evidence trail, one status view |
| [`technical-condition-report.md`](technical-condition-report.md) | Examine digital constitution, dependencies, fixity, rendering, behavior, and risk | Object-level technical and condition assessment |
| [`provenance-chain-history.md`](provenance-chain-history.md) | Keep on-chain history, legal title, custody, and historical provenance distinct | Object-level provenance and chain schedule |
| [`rights-donor-transfer.md`](rights-donor-transfer.md) | Record donor/transfer terms, title binding, rights, restrictions, and credit | Lot-level instrument plus object-level rights matrix |
| [`preservation-dossier.md`](preservation-dossier.md) | Define what is preserved, how it is packaged, and how it is verified and recovered | Object or shared-lot preservation package |
| [`generative-system-dossier.md`](generative-system-dossier.md) | Reconstruct and interpret identity, randomness, state, interaction, collection topology, causal counterfactuals, and conservation for a generative system | Project-level research dossier linked to exact Museum objects; not yet a governed record family |
| [`public-inventory.md`](public-inventory.md) | Prepare the public checklist/inventory and publication decision | Public-safe projection of governed records |
| [`restricted-annex-reference.md`](restricted-annex-reference.md) | Point to restricted registrar material without publishing it | Public reference only; never the private annex itself |
| [`attestations.md`](attestations.md) | Capture constructor, technical, curatorial, registrar, and independent review attestations | Sign-off and accountability block |

## Non-negotiable operating rules

1. An unsolicited transfer, airdrop, custody event, or Wave `WINNER` label is evidence of an event or selection—not evidence of accession.
2. A preapproved collection removes collection-specific authorization only. Authenticity, provenance, donor authority, title, rights, legal/sanctions, technical receivability, mission fit, risk, and acceptance checks still apply.
3. One lot may contain many objects, but every object gets its own stable object number, chain citation where applicable, technical/condition report, rights state, and status. A shared donor instrument or transaction schedule must not collapse object-level facts.
4. Token ownership, legal title, copyright, display permission, reproduction permission, and preservation/migration permission are separate assertions. Record `unknown` or `not_assessed`; never silently treat absence as permission.
5. Each material claim carries an evidence class (`A` direct chain, `B` authoritative issuer/governance, `C` Museum technical verification, `D` third-party historical source, `E` curatorial interpretation), source, observation date, and, where possible, a content hash.
6. Corrections are append-only amendments with `supersedes`. Do not silently rewrite a historical assertion or reuse an object number for a different work.
7. Public records contain only public-safe material. Donor contacts, executed instruments, appraisals, private signatures, custody-security details, private storage locations, and sensitive risk analysis remain in the restricted annex.
8. A retained file, render, video, manifest, or wrapper is a preservation/documentation surrogate unless the artist or governing source says otherwise. It is not automatically the tokenized artwork.
9. The target contract for instantiated governed JSON records is the exact [`record-control.md`](record-control.md) shape: `record_status` is `constructed` or `reviewed`; constructed records have `review: null`; reviewed records require a distinct non-empty reviewer, immutable 40-character lowercase commit, `outcome: approved`, and `payload_sha256` over the top-level payload with `record_control` removed. The blank Markdown forms do not themselves receive that governed status.
10. Donation offer/receipt, institutional acceptance, acquisition, legal title passage, custody receipt, and formal accession are separate events and statuses. Never infer one from another.

## State model

Use the state model in [`accession-state-gates.md`](accession-state-gates.md). The states are independent facts, not a single optimistic progress label:

`offered` → `authorized` → `acquired` → `received_onchain` → `accessioned` → `catalogued` → `technically_verified` → `preservation_complete` → `display_ready`

For pre-mint program selections, use `selected_unminted` alongside the program outcome. Do not create a token citation, title binding, custody receipt, or accession claim until a specific on-chain asset and the corresponding legal/acquisition evidence exist.

Use this shared pathway vocabulary in both the lot record and gate worksheet: `[preapproved collection | ordinary donation review | network-funded program | Meme Card benefit-work program | individual/group-funded program | secondary acquisition | purchase | bequest | exchange | transfer | other]`.

## Scenario controls

### Completed Casey Reas donation

The completed Casey Reas donation is a multi-object donation scenario for this
packet. The reviewed accession package, not this template, establishes its
accepted and accessioned state. Use one accession lot with one object record
per donated work/token, a lot-level donor/transfer record, and object-level
technical, condition, provenance, rights, preservation, and public-inventory
entries. The templates intentionally contain no Casey object facts and do not
replace or edit the actual Casey records. When filling them, copy verified
values from the canonical records and bind the title evidence to the specific
transfer for each object. Never infer an acceptance or accession state from a
wallet transfer, receipt status, or template example.

### Unminted Keys and Gates selections

Keys and Gates is a program-selection pathway, not an automatic accession. A selected submission is tracked as `selected_unminted` while mint, purchase/acquisition, title, rights/consent, custody transfer, and technical intake remain open. The program's authorization and Wave selection authorize only the program and its selection event; they never authorize a specific object's acquisition, mint, custody, or accession. The Wave selection is retained as program evidence; it is never substituted for an ERC-721/1155 identity, a transaction, or a completed accession. If a selected work is unavailable or fails the formal terms, record the outcome and any rank-based roll-forward as a new, attributed program event.

## Interoperability boundary

Use the field labels and evidence references in [`docs/standards-crosswalk.md`](../docs/standards-crosswalk.md) when exporting to Spectrum-aligned workflows, ICOM Object ID, CIDOC CRM/LIDO, PREMIS, IIIF, C2PA 2.4, BagIt, OCFL, or the pinned 6529Stream profile. The templates are an application profile; they do not claim that any external standard is a complete collections-management system or that 6529Stream has deployed every named Museum profile. PREMIS/IIIF/C2PA 2.4/OCFL mappings and exports remain `pending` unless a completed record supplies their identifiers and evidence.
