# Public information architecture

Status: constructed canonical IA input for the source publication contract; independent review is pending for this candidate. Routes are presentation affordances over typed public entities and relations; route presence never changes Museum lifecycle state.

## Primary navigation

The public Museum has five calm top-level areas:

1. **Collection** - accessioned Works and their current Collection relations.
2. **Artists** - Artist profiles, practice evidence, and linked Works.
3. **Acquisitions** - coherent Curated Acquisition units, with proposed/selected/accessioned states clearly labelled.
4. **Research** - Research Publications and source-backed interpretive context. Projects/Series are art entities linked to research, not Research Publications.
5. **About** - Institution, collection policy, stewardship, rights, and the public-record boundary.

Exhibitions remain a reserved future area. No Exhibition page, placeholder, or route is published by this contract.

## Canonical route mapping

| Public concept | Canonical route shape | Source identity |
|---|---|---|
| Institution | `/museum/network` | stable public entity ID |
| Collection | `/museum/network/collection` | stable public entity ID |
| Artist | `/museum/network/artists/{slug}` | stored unique `public_slug`; stable entity ID remains source-linked |
| Organization | `/museum/network/organizations/{slug}` | stored unique `public_slug`; stable entity ID remains source-linked |
| Work | `/museum/network/works/{workId}` | `{workId}` is the stored canonical Work ID `6529NM-W-####`; accession, outcome, proposal, and token IDs are aliases/redirects only |
| Project/Series | `/museum/network/projects/{slug}` | stored unique `public_slug`; linked to research but not filed as a Research Publication |
| Curated Acquisition | `/museum/network/acquisitions/{slug}` | stored unique `public_slug`; IDs `6529NM-CA-2026-001` through `003` remain source-linked |
| Acquisition Program | `/museum/network/acquisition-programs/{programSlug}` | stored visitor slug such as `keys-and-gates`; canonical entity ID `6529NM-AP-ENT-####` and source `6529NM-AP-01` remain aliases; legacy `/programs/{programId}` redirects |
| Research Publication | `/museum/network/research/{slug}` | stored unique `public_slug`; publication entity only |
| Exhibition | reserved route family | no Exhibition instance, placeholder, or visitor route is published in this release |

Existing Casey gift and Keys and Gates routes are compatibility redirects into these identities. The redirect is not a duplicate record and must not make `/gifts/6529NM.2026.001` look like the Curated Acquisition identifier. Existing source IDs, proposal IDs, program IDs, accession numbers, and object IDs remain displayed as provenance links. A slug amendment creates a permanent redirect and does not change the entity identity.

The canonical Project/Series example is **Magnum Photos 75**, published at `/museum/network/projects/magnum-photos-75` (`6529NM-PRJ-0006`). Retained proposal evidence names it as a 2022 anniversary-year release context drawn from the Magnum archive. The five accessioned Works and their ERC-721 token manifestations remain linked to that source context without conflating the Project with the Museum's `Conflict at Its Edges` Curated Acquisition, the independent Work identities, or the accessioned Collection relation.

### How works enter the Museum

Acquisition Programs are pathway/mechanism records, not Curated Acquisitions and not Collection units. They live in the separate `/museum/network/acquisition-programs/{programSlug}` namespace, are discoverable from the Acquisitions hub, and link to the Curated Acquisitions or Work outcomes they produce. A Program relation never creates Collection membership: only an active accession relation, followed by the corresponding Collection relation, can place a Work in the permanent Collection.

Work IDs are acquisition-independent and are never derived from a Curated Acquisition, program outcome, accession, artist, chain, wallet, title, or slug. The initial release publishes `6529NM-W-0001` through `6529NM-W-0028`; source aliases are retained in the governed identity inventory and redirect map. `AGENT`, `ACCESSION`, and `MEDIA_REFERENCE` are relational-only machine records with no visitor route.

Agents are not automatically Artists. Generic `AGENT` entities are reached only through typed relational discovery, while Artist and Organization profiles have their own public route families.

## Publication states

Cards and lists show visitor-facing Curated Acquisition labels, not the machine token `selected_unminted`. A formal proposal that has not changed status may say **Proposed in the Museum Wave**. The current Conflict at Its Edges card says **Completed gift; accessioned into the permanent Collection** and identifies accession `6529NM.2026.002`. Its proposal, scholarship, object records, diligence, and accession documents remain linked as one record of the gift. A Keys and Gates card says **Selected through an acquisition program; acquisition pending**, with the qualifier **Not yet minted; minting route under consideration.** The exact `selected_unminted` status stays in the source record layer. Selected Keys and Gates works do not appear in Collection. Casey and Magnum appear in Collection through their accessioned Work and Collection relations.

Media components consume the typed media contract. The five Magnum image records
retain their historical Wave publication evidence and are also linked to the
accessioned Works under `6529NM.2026.002`. The retained signed-drop API
publication observation binds all seven parts, exact source-byte hashes, the
actual CloudFront presentation URLs, credits, rights labels, and separate
token-linked Arweave locators; `is_signed:true` remains an API-reported state,
not an independently verified signature or license. The Museum interprets
ordinary credited institutional display, publication, and accessibility in
accession, Collection, and scholarship contexts as permissible. That
interpretation does not transfer copyright or grant commercial or general
reproduction, derivative, licensing, download, or AI-training rights. A
frontend may render only the governed affordances listed by the source record;
it must not synthesize a rights state from a URL or MIME type.
