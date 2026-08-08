# Rights, technical identity, and proposal provenance

## Scope

This dossier records what the proposal package and public chain/metadata
observations establish about the five token-linked manifestations. It keeps
token identity, source-image identity, copyright, title, custody, display
permission, and Museum accession as separate facts. The five photographs are
public Work projections for the proposed gift; no accession or object record is
manufactured here.

## Technical identity schedule

| Public Work | Work | Proposal alias | Token / curation | CAIP-19 | Archive reference |
| --- | --- | --- | --- | --- | --- |
| `6529NM-W-0024` | David Seymour, *Patrolling the border between the Negev Desert and Jordan* | `6529NM-PG-2026-001.OBJ-001` | `127`; `2/3`; `127/225` | `eip155:1/erc721:0xe628b59d34f42b16c53f4d697f1ffd4d8d987b91/127` | `SED1952003W00003/23` |
| `6529NM-W-0025` | Larry Towell, *Government soldiers in a church, Suchitoto, El Salvador* | `6529NM-PG-2026-001.OBJ-002` | `145`; `2/3`; `145/225` | `eip155:1/erc721:0xe628b59d34f42b16c53f4d697f1ffd4d8d987b91/145` | `TOL1986003W00045/26` |
| `6529NM-W-0026` | Micha Bar-Am, *Demonstration, Western Wall, Jerusalem* | `6529NM-PG-2026-001.OBJ-003` | `97`; `2/3`; `97/225` | `eip155:1/erc721:0xe628b59d34f42b16c53f4d697f1ffd4d8d987b91/97` | `BAM1989009W02477/26C` |
| `6529NM-W-0027` | Moisés Saman, *Tripoli, Libya* | `6529NM-PG-2026-001.OBJ-004` | `44`; `1/3`; `44/225` | `eip155:1/erc721:0xe628b59d34f42b16c53f4d697f1ffd4d8d987b91/44` | `SAM2011005H2503/5482` |
| `6529NM-W-0028` | Lorenzo Meloni, *Palmyra, Syria* | `6529NM-PG-2026-001.OBJ-005` | `104`; `2/3`; `104/225` | `eip155:1/erc721:0xe628b59d34f42b16c53f4d697f1ffd4d8d987b91/104` | `MEL2016002G0401/4032` |

The Work IDs above are the acquisition-independent identities supplied by the
WP-1 committed projection. Proposal aliases remain typed source-package
references; they are not accession numbers and do not replace the governed Work
records that the release integration will admit.

| Work | Metadata URI | Source-image URI | Observed JPEG bytes | Dimensions | SHA-256 |
| --- | --- | --- | ---: | --- | --- |
| Seymour #127 | [Arweave metadata](https://arweave.net/fHJAhfhIB7wTpz0my7K9-b9mWDq-fpk5Yr57gqsf_pM) | [Arweave image](https://arweave.net/VE0zO2N1zVTsbEUHdUFazEgvuMbmVOi6OfaWfQOWkaM) | 2,518,674 | 3,056 × 4,600 | `65abf8b6a182bb641787a43b40d10f0b6471357e5c90777aacccf9eb73ea1453` |
| Towell #145 | [Arweave metadata](https://arweave.net/jHZq16_Id5lJR5vIIWcRiyGBM2ctB6dSL8sRJhLrprQ) | [Arweave image](https://arweave.net/r0bUW6Mtxq897pgig0V01Ad43S_Ldwv3tARjwmjrqpE) | 1,813,285 | 5,369 × 3,601 | `e60f2d2c56b702981597606315c6c77e07dedf4dd9a95804ae2da720d0f5bcee` |
| Bar-Am #97 | [Arweave metadata](https://arweave.net/OOnuimyyLnY4ez3c7ZQA9vOZu_m9p06C3FO71Vo2wQY) | [Arweave image](https://arweave.net/vRmOcFJRTK84ILXp2Tkjz5KoS4iXXbMqki7rxhTYlr4) | 1,666,083 | 5,000 × 3,292 | `a59d8624c8da11758c5f1c0b64484229e4ffb68167b8e5783cdbafa9628b74df` |
| Saman #44 | [Arweave metadata](https://arweave.net/MVXFi_QJmcwGNRJyW_q6IGI8YVa5yYYDgY-JNOh_Tns) | [Arweave image](https://arweave.net/zLifpzu3AQWqjg59nuy9jeRqHPA5o5-LpwwBqNRcD5o) | 1,540,870 | 5,616 × 3,744 | `cf1ec75dc4e3de3bcd85cffd9954c75395d9af2bff38374468440e403352b816` |
| Meloni #104 | [Arweave metadata](https://arweave.net/T6wgoTW03zCJVK1Y5dZy5InfsiZD7BSoHYaVbQul7E0) | [Arweave image](https://arweave.net/oz0t0DJj2BgFCux1WXskxisxvzV2KA0ukqaVbQ1Ckco) | 16,871,807 | 5,964 × 4,768 | `49c45762f344fcc058a1f1167b01e9c298b1f4cff5e200e9033577f9c1023ad2` |

The proposal package reports that all five metadata objects and linked JPEGs
were resolved and SHA-256 verified on 5 August 2026. The Museum visually
inspected the five upstream images on 8 August 2026; no JPEG or derivative was
added to this repository. The local observations identify retrievable upstream
resources at those observation times, not Museum preservation objects.

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
  the observed owner.

These are point-in-time chain observations. The owner address is not treated as
the donor, copyright holder, legal-title holder, or Museum custodian. The local
proposal records themselves say that offer, repository record, Wave submission,
or threshold outcome does not complete gift acceptance or accession.

The verified contract source exposes no public proxy-upgrade path in the local
review, while the implementation allows the contract owner or administrators to
change token URIs or the base URI. The recorded Arweave objects and their
hashes therefore remain useful fixity observations, but a future technical
review must re-read tokenURI state before relying on a live pointer.

## Rights and use disposition

Each target token metadata record carries a photographer/Magnum copyright line
and `All Rights Reserved`. The proposal package records token transfer as
asserting no copyright or reproduction grant. Magnum’s terms distinguish an NFT
purchase from copyright in the associated photographic file. Those statements
are source records, not a complete chain-of-title or license determination.

The exact already-published Wave JPEG URLs may be referenced or embedded in the
proposal’s historical Wave presentation with the supplied artist/Magnum credit,
`All Rights Reserved`, and the label **Wave-source historical proposal media**.
The [Source and rights record](source-and-rights-record.md) and [media plan](media-plan.md)
define that narrow disposition. Download, full-resolution delivery, crops or
derivatives, responsive recompression, IIIF, preservation copying, and
Collection publication remain outside the current permission boundary.

## Accession boundary

| Record or fact | Current state |
| --- | --- |
| Public Work lifecycle | `selected_by_museum_wave_acquisition_review_in_progress` |
| Collection membership | `not_in_collection` |
| Canonical Work IDs | `6529NM-W-0024` through `6529NM-W-0028` in the WP-1 committed projection; governed release admission remains pending |
| Curated Acquisition | `6529NM-CA-2026-003` |
| Proposed gift | `6529NM-PG-2026-001` |
| Accession number | None |
| Object record | None |
| Title binding to Museum custody | None |
| Donor authority/legal title | Unresolved |
| Copyright/reproduction/display license | Narrow historical proposal-media disposition only |
| Museum custody/preservation | None; upstream files not retained |

Sources: proposal records and live technical boundary [S37](../sources/source-register.md),
exact token metadata [S10–S14](../sources/source-register.md), contract and
token observations [S15–S16](../sources/source-register.md), and signed proposal
media [S38](../sources/source-register.md).
