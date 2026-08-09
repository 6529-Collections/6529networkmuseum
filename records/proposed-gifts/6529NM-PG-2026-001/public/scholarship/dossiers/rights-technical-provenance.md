# Rights, technical identity, and proposal provenance

*6529 Network Museum, Curatorial Research · Edition 1.0.0 · Published 9 August 2026 · Research through 9 August 2026 · [Publication record and suggested citation](../publication-record.md)*

## Scope

This dossier records what the proposal package and public chain/metadata
observations establish about the five token-linked manifestations. It keeps
token identity, source-image identity, copyright, title, custody, display
permission, and Museum accession as separate facts. The five photographs are
public Work projections for the selected acquisition; no accession or object record is
manufactured here ([S37](../sources/source-register.md)).

## Technical identity schedule

The five-row schedule reproduces the token, curation, and acquisition-independent
Work bindings in the source register and machine record
([S10–S14](../sources/source-register.md)).

| Public Work | Work | Proposal alias | Token / curation | CAIP-19 | Archive reference |
| --- | --- | --- | --- | --- | --- |
| `6529NM-W-0024` | David Seymour, *Patrolling the border between the Negev Desert and Jordan* | `6529NM-PG-2026-001.OBJ-001` | `127`; `2/3`; `127/225` | `eip155:1/erc721:0xe628b59d34f42b16c53f4d697f1ffd4d8d987b91/127` | `SED1952003W00003/23` |
| `6529NM-W-0025` | Larry Towell, *Government soldiers in a church, Suchitoto, El Salvador* | `6529NM-PG-2026-001.OBJ-002` | `145`; `2/3`; `145/225` | `eip155:1/erc721:0xe628b59d34f42b16c53f4d697f1ffd4d8d987b91/145` | `TOL1986003W00045/26` |
| `6529NM-W-0026` | Micha Bar-Am, *Demonstration, Western Wall, Jerusalem* | `6529NM-PG-2026-001.OBJ-003` | `97`; `2/3`; `97/225` | `eip155:1/erc721:0xe628b59d34f42b16c53f4d697f1ffd4d8d987b91/97` | `BAM1989009W02477/26C` |
| `6529NM-W-0027` | Moisés Saman, *Tripoli, Libya* | `6529NM-PG-2026-001.OBJ-004` | `44`; `1/3`; `44/225` | `eip155:1/erc721:0xe628b59d34f42b16c53f4d697f1ffd4d8d987b91/44` | `SAM2011005H2503/5482` |
| `6529NM-W-0028` | Lorenzo Meloni, *Palmyra, Syria* | `6529NM-PG-2026-001.OBJ-005` | `104`; `2/3`; `104/225` | `eip155:1/erc721:0xe628b59d34f42b16c53f4d697f1ffd4d8d987b91/104` | `MEL2016002G0401/4032` |

The Work IDs above are the acquisition-independent identities in the governed
public entity inventory. Proposal aliases remain typed source-package
references; they are not accession numbers and do not replace the Work records.

| Work | Metadata record | Source-image record | Observed JPEG bytes | Dimensions | SHA-256 |
| --- | --- | --- | ---: | --- | --- |
| Seymour #127 | Governed record S10 | Exact URI retained in complete-manifest evidence; no visitor link | 2,518,674 | 3,056 × 4,600 | `65abf8b6a182bb641787a43b40d10f0b6471357e5c90777aacccf9eb73ea1453` |
| Towell #145 | Governed record S11 | Exact URI retained in complete-manifest evidence; no visitor link | 1,813,285 | 5,369 × 3,601 | `e60f2d2c56b702981597606315c6c77e07dedf4dd9a95804ae2da720d0f5bcee` |
| Bar-Am #97 | Governed record S12 | Exact URI retained in complete-manifest evidence; no visitor link | 1,666,083 | 5,000 × 3,292 | `a59d8624c8da11758c5f1c0b64484229e4ffb68167b8e5783cdbafa9628b74df` |
| Saman #44 | Governed record S13 | Exact URI retained in complete-manifest evidence; no visitor link | 1,540,870 | 5,616 × 3,744 | `cf1ec75dc4e3de3bcd85cffd9954c75395d9af2bff38374468440e403352b816` |
| Meloni #104 | Governed record S14 | Exact URI retained in complete-manifest evidence; no visitor link | 16,871,807 | 5,964 × 4,768 | `49c45762f344fcc058a1f1167b01e9c298b1f4cff5e200e9033577f9c1023ad2` |

The proposal package reports that all five metadata objects and linked JPEGs
were resolved and SHA-256 verified on 5 August 2026. The Museum visually
inspected the five upstream images on 8 August 2026; no JPEG or derivative was
added to this repository. The local observations identify retrievable upstream
resources at those observation times, not Museum preservation objects
([S37](../sources/source-register.md)).

## Chain and contract observation

The common ERC-721 contract is
`0xe628b59d34f42b16c53f4d697f1ffd4d8d987b91`. The proposal package records the
following finalized-block observation:

- Ethereum block `25,690,178`, hash
  `0x01a42cf70ba13f1ebefa607249fd9009baadb127f2a05fcb6e7573d943cb200c`;
- block timestamp 5 August 2026, 17:20:23 UTC;
- all five token IDs observed under owner
  `0x6daa633c23615a29471deafae351727867e7dad1`;
- no token-level approval at that observation; and
- three successful transfer events recorded for each token: mint, transfer to
  an address identified by Blockscout as Foundation Market, then transfer to
  the observed owner ([S16](../sources/source-register.md); [S37](../sources/source-register.md)).

These are point-in-time chain observations. The owner address establishes none
of the publicly credited offeror's authority, copyright ownership, legal title,
or Museum custody. The local
proposal records themselves say that offer, repository record, Wave submission,
or threshold outcome does not complete gift acceptance or accession
([S37](../sources/source-register.md)).

### Current finalized recheck

A later direct Ethereum JSON-RPC recheck at finalized block `25,714,155`
(`0x1885deb`), hash
`0x9ec59a4b6029e30f52491f6ebfbf34c521a4338056fa1a0b9a5cff12bb9ac767`, with
block timestamp `2026-08-09T01:33:11Z`, retained the same point-in-time owner
and approval observations. The contract read as `Magnum Photos 75` (`MPA75`)
and reported ERC-721 support through ERC-165. All five `ownerOf` reads returned
`0x6daa633c23615a29471deafae351727867e7dad1`; all five `getApproved` reads
returned the zero address. The tokenURI reads were:

| Token | tokenURI observation at block `25,714,155` | ownerOf | getApproved |
| ---: | --- | --- | --- |
| `#127` | Governed record S10; exact URI retained outside the visitor corpus | `0x6daa633c23615a29471deafae351727867e7dad1` | `0x0000000000000000000000000000000000000000` |
| `#145` | Governed record S11; exact URI retained outside the visitor corpus | `0x6daa633c23615a29471deafae351727867e7dad1` | `0x0000000000000000000000000000000000000000` |
| `#97` | Governed record S12; exact URI retained outside the visitor corpus | `0x6daa633c23615a29471deafae351727867e7dad1` | `0x0000000000000000000000000000000000000000` |
| `#44` | Governed record S13; exact URI retained outside the visitor corpus | `0x6daa633c23615a29471deafae351727867e7dad1` | `0x0000000000000000000000000000000000000000` |
| `#104` | Governed record S14; exact URI retained outside the visitor corpus | `0x6daa633c23615a29471deafae351727867e7dad1` | `0x0000000000000000000000000000000000000000` |

All fifteen mint, market, and current-owner transfer receipts returned success
(`0x1`) and the expected ERC-721 `Transfer` event. The common observed path is
mint from the zero address, transfer to an address labelled “Foundation Market”
by Blockscout, and transfer to the owner above. The label is an explorer
annotation, not a legal identity or title instrument:

| Token | Mint | Market transfer | Current-owner transfer |
| ---: | --- | --- | --- |
| `#127` | [tx](https://etherscan.io/tx/0x23173c71a59f9709724537b928dde8f3ffe0e3162ab8e4f2d9d9ef787e17f0f3) | [tx](https://etherscan.io/tx/0xc924996c8aa8cc17534397c75d3ce78efdd6bd44b142a9de06c6283f3e582d03) | [tx](https://etherscan.io/tx/0x95239b5d68a414bc4bcb481490be08002e7d870ce6bf86dbd0c961ed8ee21a09) |
| `#145` | [tx](https://etherscan.io/tx/0xa8fecaea9a0eafbabf61a186e87f9c5ba14158e7b9422752c19994c16109a1e4) | [tx](https://etherscan.io/tx/0xd2e8e53a076699c7fbaeccd6020181b026ab1d02004cbaafabc0d0fb0e756af6) | [tx](https://etherscan.io/tx/0xc0a96ebabb74d5e4ff2c670c247b27b2a1d23f0a46dabee968401ebf91a62bc0) |
| `#97` | [tx](https://etherscan.io/tx/0x17057d388846e601dba0013475dc6642869058e89f90f63d231ed1b44864913b) | [tx](https://etherscan.io/tx/0xa72cfa2c0e6e8ec7066d69216c64d0e62de90726fca35b00cce20b6e0762f078) | [tx](https://etherscan.io/tx/0xa530bc66b7f14a85cb92f73b0f424cefb9bb69683dd3554b176daa38ebe47850) |
| `#44` | [tx](https://etherscan.io/tx/0x6786a3a02c43dc5334b58f416eef60e90292a43b63af00b63116c124822aaf17) | [tx](https://etherscan.io/tx/0xa5a4bbda1fb5332d5b2aee821afd0c62bfa39cd66e68cb83a551380e7af5dfa4) | [tx](https://etherscan.io/tx/0x1bd65e9320e334578f7aad039973c78566ca1b5bf84faef800d5560a89fa50d4) |
| `#104` | [tx](https://etherscan.io/tx/0x455147b6272e8924d8559dd8adc8543470e83dc13cba47605afe37b3a566554f) | [tx](https://etherscan.io/tx/0xb7a7e4612bc2ceef06f7ae430cb53564e3fb0cb19a4478ad45181268903d2c8d) | [tx](https://etherscan.io/tx/0x23315ad1425c91df68019f08e1ab92adcadb10cb69d9e5299deafaf1796d1747) |

The public contract page identifies an EIP-1967-style proxy and reports
implementation `0xe4e4003afe3765aca8149a82fc064c0b125b9e5a`. At the same
observation the implementation slot pointed to that address; the standard
EIP-1967 admin slot read zero; and the verified source reported contract owner
`0xd8d005f66296068a2efc240f7e5910af52a86ee1` with administrators
`0xdc6f5281bc65dee2d317e140eb19c927351dd86d` and that owner. The verified
implementation ABI exposed `setTokenURI` and `setBaseTokenURI`, guarded by
`adminRequired`. I found no public proxy-upgrade mutator in that verified ABI
at the observation, but this is not an immutability claim: token URIs and the
base URI are administratively mutable. A future technical review must re-read
the tokenURI values before relying on a live pointer ([S15](../sources/source-register.md);
[S53](../sources/source-register.md); [S55](../sources/source-register.md)).

## Rights and use disposition

Each target token metadata record carries a photographer/Magnum copyright line
and `All Rights Reserved` ([S10–S14](../sources/source-register.md)). The proposal package records token transfer as
asserting no copyright or reproduction grant ([S37](../sources/source-register.md)). Magnum’s terms distinguish an NFT
purchase from copyright in the associated photographic file ([S09](../sources/source-register.md)). Those statements
are source records, not a complete chain-of-title or license determination.

Museum observation `6529NM-WAVE-PUB-OBS-2026-08-08-001` records the signed
seven-part Wave publication at `2026-08-08T10:15:02.0167151Z`, including its
part-content hashes. Its payload SHA-256 is
`sha256:887d527756721cae1bf758a8205d1f5f7e0d1cebee2b3f27aafcab5271132995`;
the complete Museum record has raw-file SHA-256
`sha256:b1f57fa0010bdaf0f9f21854f88e446e7f20b4a1921ab6fd075d4836c5920e58`
([S56](../sources/source-register.md)).

A later live read command `punk6529bot drops get
002bfa4f-8416-48bf-b35e-38f354e9a9f0 --json` at
`2026-08-09T02:04:21.7672652Z` returned signed `WINNER`, serial `1276093`, and
parts 1–7. Its public-safe evidence record binds the six public media URLs to their
reported MIME/status values and records no media for part 7. The canonical
payload hash is
`sha256:93e968562297fe5acff792e027f302b938ba6fa1ac88284754c4ba684d1266a2`;
the complete Museum evidence record has raw-file SHA-256
`sha256:2d102b1e5ee4c448bad0631d3bb659949456d74a342f6203b3a1dd12d5f29d6a`.
The receipt’s `ready` values describe the Wave publisher’s media state; they
do not grant rendering or reproduction permission ([S54](../sources/source-register.md)).

The CloudFront URLs are Wave-upload presentation media. The Arweave image URLs
in the technical schedule are token-source locators reached through each
token’s metadata. A matching byte hash observed in memory does not collapse
those publication contexts, create preservation custody, or create a rights
grant. The exact already-published Wave URLs are retained as non-rendering
evidence locators with the supplied artist and Magnum credits, `All Rights
Reserved`, and the label **Wave-source historical proposal media**
([S38](../sources/source-register.md); [S54](../sources/source-register.md);
[S56](../sources/source-register.md)).
The [Source and rights record](source-and-rights-record.md) and [media plan](media-plan.md)
define that narrow disposition. Download, full-resolution delivery, crops or
derivatives, responsive recompression, IIIF, preservation copying, and
Collection publication remain outside the current permission boundary
([S38](../sources/source-register.md)).

## Accession boundary

| Record or fact | Current state |
| --- | --- |
| Public Work lifecycle | `selected_by_museum_wave_acquisition_review_in_progress` ([S37](../sources/source-register.md)) |
| Collection membership | Outside the permanent Collection |
| Canonical Work IDs | `6529NM-W-0024` through `6529NM-W-0028`; independent publication review remains pending |
| Curated Acquisition | `6529NM-CA-2026-003` ([S37](../sources/source-register.md)) |
| Proposal record | `6529NM-PG-2026-001` ([S37](../sources/source-register.md)) |
| Accession number | None |
| Object record | None |
| Title binding to Museum custody | None ([S37](../sources/source-register.md)) |
| Donor authority/legal title | Unresolved ([S37](../sources/source-register.md)) |
| Copyright/reproduction/display license | Narrow historical proposal-media disposition only ([S38](../sources/source-register.md)) |
| Museum custody/preservation | None; upstream files not retained ([S37](../sources/source-register.md)) |

Sources: proposal records and live technical boundary [S37](../sources/source-register.md),
exact token metadata [S10–S14](../sources/source-register.md), contract and
token observations [S15–S16](../sources/source-register.md), and the retained
public proposal media [S38](../sources/source-register.md).
