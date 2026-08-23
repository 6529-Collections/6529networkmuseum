> Draft research; not publication-ready. Cutoff: 2026-08-23.

# Record-ready finding

Observation basis: Ethereum mainnet, 2026-08-23 UTC. No repository files were changed.

## Object identity and administrative state

- `caip19`: `eip155:1/erc721:0xe034bb2b1b9471e11cf1a0a9199a156fb227aa5d/210`
- `title`: *Themes and Variations #210*
- `artist`: Vera Molnár, in collaboration with Martin Grasser
- `date`: 2023
- `edition`: fixed edition of 500 unique works
- `platform`: Sothebys Gen Art; ERC-721; Ethereum
- `project_id`: `0`
- `token_hash`: `0xd0a3be9aa1a3e101a12ec038ceb71a18846dbc62eac3e91fb425232e7820a318`
- `acquisition_method`: gift
- `institutional_status`: accepted gift, per registrar instruction
- `custody_status`: received on-chain and verified at finalized block
- `formal title binding`: must remain separately bound to the executed gift/acceptance instrument; chain receipt alone establishes custody, not legal title.

Sources: [Art Blocks collection record](https://www.artblocks.io/collection/themes-and-variations-by-vera-molnar-in-collaboration-with-martin-grasser), [Art Blocks token metadata](https://token.artblocks.io/1/0xe034bb2b1b9471e11cf1a0a9199a156fb227aa5d/210), [Museum institutional note](https://6529networkmuseum_thememes.ar.io/).

## Chain provenance

Observed transfer sequence:

| Event | Transaction | Block / UTC | From | To |
|---|---|---:|---|---|
| Mint / purchase | [`0x6838200b…aaaa8`](https://etherscan.io/tx/0x6838200beb692a066e6a9cc0fd83e06ef58aecb716ce75423c4331270ffaaaa8) | 17,778,260 / 2023-07-26 15:50:59 | `0x0000000000000000000000000000000000000000` | `0x061600d3515b387d562504eed5a1a485f9ae0ee4` (*pokémonred.eth*) |
| Transfer | [`0x137dfa13…fa5e`](https://etherscan.io/tx/0x137dfa137b08d7354107ecd13eab8d27da81a461925f7253e42be3af1e62fa5e) | 17,784,550 / 2023-07-27 12:58:47 | `0x061600d3515b387d562504eed5a1a485f9ae0ee4` | `0xac6fd50bf975ac144b5a58bb4fae0fd64308c8aa` (*lastchancesaloon.eth*) |
| Transfer | [`0xf4bc7b31…dbf2b`](https://etherscan.io/tx/0xf4bc7b31ea60c8aea19084d40e0715fd96030c77cf170f75784ee17b598dbf2b) | 17,784,944 / 2023-07-27 14:17:35 | `0xac6fd50bf975ac144b5a58bb4fae0fd64308c8aa` | `0xe564D9AFc3e8D7dDc99912Dbc5dB58925b414024` |
| Transfer | [`0x214abec0…f50d`](https://etherscan.io/tx/0x214abec0fbe817a27dffe0900ccb3dff2c47d75cc34dc61dac4b27e8b9b8f50d) | 25,747,940 / 2026-08-13 18:37:11 | `0xe564D9AFc3e8D7dDc99912Dbc5dB58925b414024` | `0x6daa633c23615a29471deafae351727867e7dad1` (*social.6529.eth*) |
| Museum receipt | [`0x618603d9…a5cd`](https://etherscan.io/tx/0x618603d9f21dc09a4a7b2d6b6b242cc337127e8052116d0ee28c6c25f012a5cd) | 25,816,958 / 2026-08-23 09:27:59 | `0x6daa633c23615a29471deafae351727867e7dad1` | `0xbECfa2bA5a782D11E1a0e821E8F2e30b6684178c` (*networkmuseum.6529.eth*) |

The receipt transaction is a successful `safeTransferFrom`; status `0x1`. At finalized block `25,816,984`, hash `0x4f478846f35928cf4ead31161b54ffc601e9a9a519e035c73767aa3284b119d5`:

- `ownerOf(210)`: `0xbECfa2bA5a782D11E1a0e821E8F2e30b6684178c`
- `getApproved(210)`: zero address
- custody-capture summary SHA-256: `a4f3b10199b566c619c164e352be85072bb71197e2328834ab2d6f2efdd5987b`
- official source-evidence manifest SHA-256: `71fb6066e1113e22c8586e195bfb8d553dcc8c4d7dec5b33de3ae47d3ebcafe5`

Interpretation: chain provenance establishes token identity, transfer chronology, and current custody. It does not independently establish donor identity, authority to gift, copyright ownership, or absence of off-chain encumbrances.

Stewardship duty: bind the executed gift/acceptance instrument and donor-authority evidence specifically to transaction `0x618603d9…a5cd`.

## Token, metadata, and generator constitution

On-chain contract reads:

- contract name/symbol: `Sothebys Gen Art (STBYS)`
- core type/version: `GenArt721CoreV3_Engine_Flex`, `v3.1.3`
- project details: *Themes and Variations*; artist string as above; license string `CC BY-NC 4.0`
- project state: `500/500` invocations; `active=true`; `paused=true`; completed `2023-07-26T16:39:47Z`; `locked=true`
- token hash seed: `0x5f5a04ef5d4f0ca13dd9dd78`
- `tokenIdToHash(210)`: supplied token hash, exact match
- token project: `tokenIdToProjectId(210)=0`
- external dependency count: `0`
- dependency registry: zero address
- preferred IPFS and Arweave gateways: empty
- project base URI: `https://token.artblocks.io/0xe034bb2b1b9471e11cf1a0a9199a156fb227aa5d/`
- current `tokenURI(210)`: `https://token.artblocks.io/0xe034bb2b1b9471e11cf1a0a9199a156fb227aa5d/`

Art Blocks metadata reports:

- `Grid`: `6x6`
- `Letters`: `NFT`
- `Palette`: `b #00188D, b #F3F0E9`
- `Vera Letter`: `F bold`
- `aspect_ratio`: `1`
- `script_type`: `js@na`
- `engine_type`: `flex`
- `license`: `CC BY-NC 4.0`

Record the discrepancy explicitly: the token API reports a square aspect ratio of `1`, while on-chain `projectScriptDetails(0)` returns an empty aspect-ratio string. The observed rendering is square.

The project’s conceptual constitution is consistent with Sotheby’s description: N/F/T letter forms are transformed algorithmically through position, size, weight, distribution, colour selection, complementary pairings, and grid arrangements. [Sotheby’s project account](https://www.sothebys.com/en/articles/vera-molnar-the-grande-dame-of-generative-art)

## Script and dependency fixity

The verified contract is directly deployed at the supplied address. Runtime bytecode observation:

- runtime length: `24,423` bytes
- runtime SHA-256: `290c7f5a95903096f667bb48ac415c88ccb1f38ac59dcf15b09d9627108ea0d6`
- EIP-1967 implementation, beacon, and admin slots: zero

The on-chain generator comprises 11 concatenated JavaScript segments:

- `script_type`: `js@na`
- `script_count`: `11`
- total concatenated UTF-8 length: `251,163` bytes
- concatenated script SHA-256: `d7799751c1017efe9de352cd73c969893fd7757fc9e58d468ebe9c2b1a9f3f42`

Segment storage addresses, in index order:

`0xA7CEd9E81776DAaa9A4f83E282a2503999F6527c`, `0x8292d1B5f93f88725bE87b0955c66162019CB246`, `0x2ba03E6af03a5D7D5967182f4CCE7ef259E8Ebd1`, `0x7A512eA80DaF89dD36E0e5D10825A1722fF0B3B3`, `0x8536978031Ce00A6408627Fb93661c8265D3925a`, `0xc5973409Ebd5e5FA8913D13800fcd46713Bbd5cB`, `0xFA2368Ed8798c70b61aF43F9EA85c2fd186939dA`, `0x034665d304AE48E7F8eE5afDc0FCdC34484e827F`, `0x4C3f1c81075d14B4C263340c39f5650E8df38dCe`, `0xaaeAa6aEfa6faf7Bd8320d49D4EFbf373F46bA6E`, `0x96bD36648AEBD846115D1500E7A0fc8AD5Ac7403`.

Interpretation: the creative script is held in eleven contract-backed segments and the token hash is fixed on-chain. No project-level IPFS, Arweave, or dependency-registry asset was observed.

Stewardship duty: retain each segment response, the concatenation protocol, contract ABI/source, runtime bytecode, and final-block RPC evidence; do not preserve only the Art Blocks URLs.

Source: [verified contract and source](https://etherscan.io/address/0xe034bb2b1b9471e11cf1a0a9199a156fb227aa5d#code), [Art Blocks Core Contract documentation](https://docs.artblocks.io/developer/core-contract/), [Art Blocks Generator documentation](https://docs.artblocks.io/protocol/on-chain-generator/).

## Mutability

Observed and interpreted controls:

- token hash is set once by the randomizer and is already populated.
- project scripts are stored in contract bytecode and the project is locked.
- script, script-type, aspect-ratio, and external-dependency mutation paths are blocked by the project lock.
- `updateProjectBaseURI` remains artist-controlled and is not protected by the project lock.
- the contract owner/Admin ACL remains nonzero: `0x4c07d4224f4fbBDf6D4E5dCab39D07175b7Af88c`.
- the token URI therefore remains dependent on a mutable project base URI and the Art Blocks metadata service.

Condition: token hash and script `green`; URI/metadata service layer `amber`.

Stewardship duty: re-query `tokenURI`, project base URI, project license, artist address, and metadata before each major publication or re-render; preserve dated snapshots and append corrections rather than rewriting prior observations.

## Rendering and interaction

Live generator:

`https://generator.artblocks.io/1/0xe034bb2b1b9471e11cf1a0a9199a156fb227aa5d/210`

Observed rendering:

- live page loaded successfully with no browser errors;
- viewport: `1280×720`;
- artwork canvas: internal `2520×2520`, CSS `720×720`;
- square composition, responsive to the smaller viewport dimension;
- visual appearance: dark ultramarine and warm off-white modular field with 6×6 structure, bold and fragmented letter forms, bars, line fields, and dense geometric subdivisions;
- unchanged screenshot checksum after three seconds;
- no visual change after a pointer click;
- script inspection found a resize listener but no pointer, touch, keyboard, animation-frame, interval, or timeout handlers.

Interpretation: this is a deterministic static generative output presented through a live browser renderer. The platform’s `is_static=false` flag indicates a live generator is available; it does not establish animation or user interaction.

Display condition: square display, no crop, no forced interpolation, preserve the original dark-blue/off-white contrast. Use the live generator as the primary manifestation and the PNG as a documentation surrogate.

Fixity observations at `2026-08-23T09:47:12.510Z`:

- token metadata, 3,676 bytes: SHA-256 `0e513d3982144bfbc2bf8f3a7890086a3f34566927c62581d4f74370deba8409`
- Art Blocks PNG, 330,363 bytes: SHA-256 `c1b6541832f2a237555adffae2f4870143a976549e591e2dbaa4d3d87f75d166`
- generator HTML, 251,686 bytes: SHA-256 `3283658de7b4cce1e5913495aa6cd50e888e1eb285dcd2c488eb97c6d038936c`

Sources: [Art Blocks Token and Generator APIs](https://docs.artblocks.io/developer/token-and-generator-apis/), [live generator](https://generator.artblocks.io/1/0xe034bb2b1b9471e11cf1a0a9199a156fb227aa5d/210), [static PNG](https://media-proxy.artblocks.io/1/0xe034bb2b1b9471e11cf1a0a9199a156fb227aa5d/210.png).

## Rights, license, and attribution

Observed license:

- project and token metadata state `CC BY-NC 4.0`.
- the license permits noncommercial sharing and adaptation with appropriate credit, a license link, and change indication.
- commercial use is excluded.
- attribution must not imply endorsement.
- moral, publicity, privacy, trademark, and other unlicensed rights remain separate.

Operational rights determination:

- noncommercial Museum display, catalogue publication, educational interpretation, and preservation-format conversion are consistent with the recorded license, subject to attribution and change marking;
- commercial merchandise, paid editions, advertising use, commercial licensing, or monetized derivative exploitation are not cleared by the recorded license;
- AI-training permission: `unspecified`; do not treat CC BY-NC as an express AI-training grant;
- the Museum’s CC0 default does not apply because this work carries an explicit CC BY-NC license.

Recommended credit line:

> Vera Molnár, in collaboration with Martin Grasser, *Themes and Variations #210*, 2023. Ethereum token `eip155:1/erc721:0xe034bb2b1b9471e11cf1a0a9199a156fb227aa5d/210`. Art Blocks / Sotheby’s Gen Art. Licensed under CC BY-NC 4.0.

Payment routing is not copyright title:

- artist address: `0x25f8f79610637c31d52413fb503e11c4ca2a4bf2`
- primary additional payee: `0x6e9cb366000470626ee0b4103dc9f77cca19243b`, 100% of artist primary split
- secondary additional payee: `0x83a6d9DB715Aa783e20B92661D6AF302204536DB`, 66% of artist secondary split
- project secondary royalty: 3%

Sources: [CC BY-NC 4.0 deed](https://creativecommons.org/licenses/by-nc/4.0/), [CC BY-NC legal code](https://creativecommons.org/licenses/by-nc/4.0/legalcode.en), [Art Blocks token metadata](https://token.artblocks.io/1/0xe034bb2b1b9471e11cf1a0a9199a156fb227aa5d/210).

Remaining duty: retain the license-bearing metadata and bind the Museum’s accepted-gift instrument to the work’s rights record. Do not convert the license into a broader copyright assignment.

## Preservation and residual risk

Overall digital condition: `amber — pass with conditions`.

| Component | Condition | Finding |
|---|---|---|
| Token identity and custody | `green` | Contract, token ID, hash, owner, receipt, finality, and approval state match. |
| On-chain generator script | `green` | 11 bytecode-backed segments; exact aggregate fixity recorded. |
| Metadata and token URI | `amber` | Current values are retrievable but Art Blocks URI/API surfaces are mutable. |
| Rendering | `amber` | Successful deterministic observation in one browser/runtime and viewport; cross-runtime replay remains required. |
| Dependencies | `green` | No project external dependencies or gateway assets observed. Browser/renderer infrastructure remains operational dependency. |
| Rights/title | `amber` | CC BY-NC is explicit; executed gift/title and attribution evidence must remain separately bound. |
| Preservation package | `amber` | Custody capture and source-manifest hashes are supplied; raw bytes, environment data, and replay evidence must be retained together. |
| Public display | `amber` | Live and static manifestations are available; static output must remain labelled as a documentation surrogate. |

Residual risks:

1. Art Blocks metadata, generator, and media-proxy endpoints may change or become unavailable.
2. The project base URI remains artist-mutable despite the completed project lock.
3. Contract-level administration remains active.
4. Browser canvas, colour management, viewport, and headless-rendering differences may alter presentation without changing the token hash or script.
5. CC BY-NC limits commercial and some derivative uses; attribution and change marking must travel with every public manifestation.
6. ENS labels identify network-associated addresses but do not replace donor-authority or title documentation.
7. No OpenSea rarity or market-derived trait claim is admissible; the record should use only the Art Blocks traits above and any separately reproducible Museum analysis.

### Preservation actions

- retain the final-block custody capture with:
  - block `25,816,984`
  - hash `0x4f478846f35928cf4ead31161b54ffc601e9a9a519e035c73767aa3284b119d5`
  - summary SHA-256 `a4f3b10199b566c619c164e352be85072bb71197e2328834ab2d6f2efdd5987b`
  - source-evidence manifest SHA-256 `71fb6066e1113e22c8586e195bfb8d553dcc8c4d7dec5b33de3ae47d3ebcafe5`
- retain raw metadata, generator HTML, PNG, contract source/ABI, runtime bytecode, all script segments, and RPC responses;
- capture exact browser/runtime/version and rerun the generator in a second supported environment;
- create a dated display record with the recommended credit line and CC BY-NC link;
- complete the independent title/rights evidence binding before marking the object’s accession dossier complete.
