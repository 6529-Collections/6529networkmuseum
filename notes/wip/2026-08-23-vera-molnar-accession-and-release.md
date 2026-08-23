# Vera Molnár accession and production release

Status: active accession and release ledger  
Opened: 2026-08-23 09:34 UTC  
Deadline: 2026-08-23 15:34 UTC  
Constructor branch: `codex/vera-molnar-accession`  
Constructor base: `a3977a8f020f58d0c9e79f23bc4f37245be65879`

## Publication-boundary correction

The release binds the public scholarship, generated entity graph, seven
direct accession/Wave machine records, the reviewed media-presentation
manifest, and its exact 640/1280/2400 WebP derivatives into one immutable
catalog. Candidate A remains review-pending. Reviewed B may change only the
declared review states and the presentation delivery approval, plus exact
deterministic bundle and release-manifest outputs. The catalog builder verifies
that transition directly.

## Mandate

Complete the gift accession of Vera Molnár, in collaboration with Martin
Grasser, *Themes and Variations* #210 (2023), publish finished artist,
project/acquisition, object and source scholarship, and ship an art-led Museum
website edition through reviewed source and frontend pull requests, staging,
production and live E2E qualification.

## Fixed identity and decision facts

- Museum Wave: `5f207393-5418-4a75-8738-e40edb44a94d`.
- Proposal: serial `1296797`, drop
  `d09d3c3b-d354-4e39-9e1f-1e676e3cb62e`.
- Proposal title: `Proposed gift: Vera Molnár, Themes and Variations #210`.
- Authenticated readback at 2026-08-23 reported `drop_type: WINNER`.
- Exact object: `eip155:1/erc721:0xe034bb2b1b9471e11cf1a0a9199a156fb227aa5d/210`.
- Token hash:
  `0xd0a3be9aa1a3e101a12ec038ceb71a18846dbc62eac3e91fb425232e7820a318`.
- Intended next accession identifier, subject to register validation:
  `6529NM.2026.003`; intended object identifier `6529NM.2026.003.01`.

The WINNER result selects this exact proposed gift. It does not collapse donor
authority, legal title, token custody, copyright, display rights, technical
condition, preservation condition and accession into one event. Each is
recorded separately.

## Receipt observation

Ethereum transaction
`0x618603d9f21dc09a4a7b2d6b6b242cc337127e8052116d0ee28c6c25f012a5cd`
succeeded in block `25,816,958`, hash
`0x3af2d05ec6a4f942ff56f3b049c62b639aec66bcece84c006ed3ec879257d7be`,
at 2026-08-23 09:27:59 UTC. Transfer log index `315` moved token `210`
from `social.6529.eth`
(`0x6DAA633C23615a29471dEaFae351727867E7dAD1`) to
`networkmuseum.6529.eth`
(`0xbECfa2bA5a782D11E1a0e821E8F2e30b6684178c`). Transaction value was zero
and receipt status was `0x1`.

Independent latest-head reads from dRPC, Tenderly, Blast and PublicNode all
returned the Museum address from `ownerOf(210)`. The retained custody package
then bound the receipt, Transfer log, `ownerOf(210)` and `getApproved(210)` to
finalized block `25,816,984`, hash
`0x4f478846f35928cf4ead31161b54ffc601e9a9a519e035c73767aa3284b119d5`.
Its summary SHA-256 is
`sha256:a4f3b10199b566c619c164e352be85072bb71197e2328834ab2d6f2efdd5987b`.
The custody observation is final; title, rights and accession remain separate
records.

## Release quality contract

The source package must satisfy the Museum accession, record-model,
Stream-interoperability, curatorial-publication, public-experience and
digital-art-stewardship standards. It must include:

- accession, gift-acceptance, title, custody, rights, technical, condition,
  preservation, evidence and reviewer records;
- an art-historical artist profile, a project/acquisition essay, an object
  entry grounded in close looking, and a public source/chronology record;
- claim-level citations and explicit limits without deferring substantive
  judgment to an unspecified later reviewer;
- CAIP-19 identity and Stream-compatible envelope/provenance semantics;
- governed responsive media, credit, rights, accessibility and fixity;
- append-only history and a public-safe/restricted-data boundary.

The frontend edition must lead with the work. It must provide balanced artist,
acquisition, object, Collection and Research navigation; responsive stills and
an optional safe live rendering encounter; concise institutional apparatus;
and no generic process/governance composition. Public prose receives a final
line edit for concrete museum language and against machine-like abstractions,
fake profundity, promotional claims and repeated binary constructions.

Before a frontend PR is opened, exact full-page screenshots at 1440, 820 and
390 pixels must receive independent adversarial museum/curatorial, website
UX/accessibility and copy/editorial review. The release then proceeds through
hosted review and CI, staging deploy and E2E, production deploy and E2E, and a
live route-by-route visual readback.

## Active work packages

1. Freeze the accepted Wave decision and exact finalized receipt evidence.
2. Construct the complete accession and public scholarship package.
3. Run constructor/reviewer separation, deterministic validation and source PR.
4. Activate the canonical source atomically in the frontend publication model.
5. Build and review the art-led pages and changed Museum indexes.
6. Merge, qualify staging, deploy production and retain live evidence.

## Open conditions

- Exact metadata, generator, license and media bytes are retained in
  `evidence/vera-molnar-210-sources`; the package manifest SHA-256 is
  `sha256:71fb6066e1113e22c8586e195bfb8d553dcc8c4d7dec5b33de3ae47d3ebcafe5`.
- Current title, display and preservation interpretations must be bound to
  primary evidence and reviewed independently.

## 11:15 UTC source-candidate checkpoint

- Accession `6529NM.2026.003` and object `6529NM.2026.003.01` are fully
  constructed. Seven Stream-compatible accession records, the third-accession
  register entry, 136 public entities, 233 relations, and 39 Work lifecycle
  observations are deterministic.
- The public publication includes separate studies of Vera Molnár, Martin
  Grasser, and *Themes and Variations*; a gift-and-acquisition essay; a close
  object entry; chronology; certificate; gift acceptance; display authority;
  and reviewed accessibility text.
- Three responsive WebP surrogates at 640, 1,280, and 2,400 pixels reproduce
  the official square preview without crop or retouching. Their manifest
  remains constructed and display-pending until exact-commit review.
- Focused accession, proposal-history, and public-entity suites pass 88 tests.
  Bootstrap and full Museum validators, accession commitments, media
  generation checks, graph checks, manifest generation, and whitespace checks
  pass. The candidate manifest is SHA-256
  `sha256:6ea2956b80d1049fba3fb44751e3de5df21e316c9ec32b0cd1d8b7b611105502`
  and Keccak
  `0x84d29232bbddfee5b9654bd584ffb12cfe78e1a3e833f140e3e085a8582c64e0`.
- Immediate continuation: commit candidate A, bind the exact candidate and
  media payload to independent review, emit reviewed candidate B, open and
  merge the Museum PR, publish immutable media, then complete frontend visual
  qualification and the staging/production release.
