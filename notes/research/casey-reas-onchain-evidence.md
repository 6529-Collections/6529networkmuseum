# Casey Reas donation: on-chain provenance evidence

Status: research evidence report. This is not an accession decision, legal-title opinion, or claim that the donation package is complete.

Observed at: `2026-08-01T14:58:31.9051150Z` UTC

Chain: Ethereum mainnet, chain ID `1`

Observed chain head: block `25,660,767` (`0x1878d5f`)

## Executive result

`networkmuseum.6529.eth` resolved through the ENS Registry to:

```text
0xbECfa2bA5a782D11E1a0e821E8F2e30b6684178c
```

This address is the current ERC-721 owner of all seven described tokens at the observed chain head. All seven arrived in one successful transaction:

```text
0xbdde33b32d4b70335b10cbd37c0b00a027844f14c900d82aa4f75b7a7b390498
```

The transaction was mined in block `25,660,311` (`0x1878b97`) at `2026-08-01T13:25:47Z`, with seven ERC-721 `Transfer` events from `0x6DAA633C23615a29471dEaFae351727867E7dAD1` to the Museum address. The receipt status is `0x1`.

The chain establishes custody at the receiving address. It does not, by itself, establish legal title, a completed donation instrument, copyright or display rights, curatorial acceptance, or that the source address is a particular human or institution.

## Evidence priority and method

Evidence was collected in this order:

1. Direct Ethereum JSON-RPC calls for ENS resolution, contract view functions, transaction receipts, transaction fields, blocks, and ERC-721 logs.
2. Contract-bound `tokenURI` values and Art Blocks-compatible project view functions.
3. Blockscout's Ethereum index for the complete historical transfer path and discovery of the seven objects. Its method labels and metadata are treated as indexer observations, not as substitutes for chain state.

No OpenSea rarity or marketplace-derived rarity metric was used. Marketplace labels were not used as title evidence.

Primary RPC endpoints used:

- `https://ethereum.publicnode.com`
- `https://1rpc.io/eth` (used for several receipt reads while the first endpoint was rate-limited)
- `https://rpc.mevblocker.io` (fallback read for one transaction lookup)

Indexer endpoints used for historical enumeration:

- `https://eth.blockscout.com/api/v2/addresses/0xbECfa2ba5a782D11E1a0e821E8F2e30b6684178c/nft`
- `https://eth.blockscout.com/api/v2/tokens/<contract>/instances/<token-id>/transfers`

## ENS resolution

Name: `networkmuseum.6529.eth`

ENS namehash:

```text
0xf90c6c0dca064bc19c04756dc088ceb60402ce8522ab4623f016d19abbb76394
```

The namehash was computed with the ENS namehash algorithm: starting at the zero node and iterating labels from right to left with `keccak256(parentNode || keccak256(label))`.

ENS Registry:

```text
0x00000000000C2E074eC69A0dFb2997BA6C7d2e1e
```

At the observed head, this direct call returned resolver `0xf29100983e058b709f3d539b0c765937b804ac15`:

```text
eth_call(
  to = 0x00000000000C2E074eC69A0dFb2997BA6C7d2e1e,
  data = 0x0178b8bf000000000000000000000000f90c6c0dca064bc19c04756dc088ceb60402ce8522ab4623f016d19abbb76394,
  block = latest
)
```

`0x0178b8bf` is `resolver(bytes32)`.

The resolver's direct `addr(bytes32)` call returned the Museum address:

```text
eth_call(
  to = 0xf29100983e058b709f3d539b0c765937b804ac15,
  data = 0x3b3b57de000000000000000000000000f90c6c0dca064bc19c04756dc088ceb60402ce8522ab4623f016d19abbb76394,
  block = latest
)
```

`0x3b3b57de` is `addr(bytes32)`.

The returned ABI word ended in `becfa2ba5a782d11e1a0e821e8f2e30b6684178c`, which is checksummed above. ENS resolution is time-dependent and must be rechecked at accession, publication, and every custody audit.

## Object identity and current owner

All seven objects are ERC-721 tokens on Ethereum mainnet. The CAIP-19-shaped identifiers below use lowercase contract addresses, as required by the Museum working standard.

| Described object | Contract / on-chain collection name | Project ID from contract | Token ID | CAIP-19-shaped identity | Contract artist address | Current `ownerOf` |
|---|---|---:|---:|---|---|---|
| CENTURY #31 | `0xa7d8d9ef8D8Ce8992Df33D8b8CF4Aebabd5bD270` / Art Blocks | 100 | 100000031 | `eip155:1/erc721:0xa7d8d9ef8d8ce8992df33d8b8cf4aebabd5bd270/100000031` | `0x457ee5f723c7606c12a7264b52e285906f91eea6` | `0xbECfa2bA5a782D11E1a0e821E8F2e30b6684178c` |
| CENTURY #724 | `0xa7d8d9ef8D8Ce8992Df33D8b8CF4Aebabd5bD270` / Art Blocks | 100 | 100000724 | `eip155:1/erc721:0xa7d8d9ef8d8ce8992df33d8b8cf4aebabd5bd270/100000724` | `0x457ee5f723c7606c12a7264b52e285906f91eea6` | `0xbECfa2bA5a782D11E1a0e821E8F2e30b6684178c` |
| CENTURY #401 | `0xa7d8d9ef8D8Ce8992Df33D8b8CF4Aebabd5bD270` / Art Blocks | 100 | 100000401 | `eip155:1/erc721:0xa7d8d9ef8d8ce8992df33d8b8cf4aebabd5bd270/100000401` | `0x457ee5f723c7606c12a7264b52e285906f91eea6` | `0xbECfa2bA5a782D11E1a0e821E8F2e30b6684178c` |
| Pre-Process #63 | `0x99a9B7c1116f9ceEB1652de04d5969CcE509B069` / Art Blocks | 383 | 383000063 | `eip155:1/erc721:0x99a9b7c1116f9ceeb1652de04d5969cce509b069/383000063` | `0x457ee5f723c7606c12a7264b52e285906f91eea6` | `0xbECfa2bA5a782D11E1a0e821E8F2e30b6684178c` |
| Phototaxis #308 | `0xa7d8d9ef8D8Ce8992Df33D8b8CF4Aebabd5bD270` / Art Blocks | 164 | 164000308 | `eip155:1/erc721:0xa7d8d9ef8d8ce8992df33d8b8cf4aebabd5bd270/164000308` | `0x457ee5f723c7606c12a7264b52e285906f91eea6` | `0xbECfa2bA5a782D11E1a0e821E8F2e30b6684178c` |
| 923 EMPTY ROOMS #713 | `0x145789247973C5D612bF121e9E4Eef84b63Eb707` / Art Blocks x Bright Moments | 1 | 1000713 | `eip155:1/erc721:0x145789247973c5d612bf121e9e4eef84b63eb707/1000713` | `0x457ee5f723c7606c12a7264b52e285906f91eea6` | `0xbECfa2bA5a782D11E1a0e821E8F2e30b6684178c` |
| Ex Nihilo (Cosmos) #248 | `0x0000000C687DaeD0fbA60d1dBA4e5f6149E8B894` / Art Blocks Studio \| 92 | 0 | 248 | `eip155:1/erc721:0x0000000c687daed0fba60d1dba4e5f6149e8b894/248` | `0x457ee5f723c7606c12a7264b52e285906f91eea6` | `0xbECfa2bA5a782D11E1a0e821E8F2e30b6684178c` |

The `ownerOf(uint256)` calls were evaluated at `latest` on the observed head. They all returned the Museum address. This is an ownership/custody fact under the ERC-721 contract's current state, not a legal-title conclusion.

## Creator and project-contract evidence

The seven contracts expose the Art Blocks-compatible view functions used below. Direct calls produced the project IDs in the identity table and the same configured artist address for every project:

```text
tokenIdToProjectId(uint256)       selector 0x1b689c0b
projectIdToArtistAddress(uint256) selector 0xa47d29cb
ownerOf(uint256)                  selector 0x6352211e
tokenURI(uint256)                 selector 0xc87b56dd
```

The contract `name()` results were:

```text
0xa7d8...d270  -> Art Blocks
0x99a9...b069  -> Art Blocks
0x1457...b707  -> Art Blocks x Bright Moments
0x0000...b894  -> Art Blocks Studio | 92
```

The project artist address returned by `projectIdToArtistAddress` for project IDs `100`, `164`, `383`, `1`, and `0` is:

```text
0x457ee5f723c7606c12a7264b52e285906f91eea6
```

The supplied object names and the Casey REAS artist attribution are corroborated by the contract-bound Art Blocks token URI metadata. The URI strings returned by the contracts are:

| Object group | Direct `tokenURI` result |
|---|---|
| CENTURY #31 | `https://api.artblocks.io/token/100000031` |
| CENTURY #724 | `https://api.artblocks.io/token/100000724` |
| CENTURY #401 | `https://api.artblocks.io/token/100000401` |
| Pre-Process #63 | `https://api.artblocks.io/token/383000063` |
| Phototaxis #308 | `https://api.artblocks.io/token/164000308` |
| 923 EMPTY ROOMS #713 | `https://token.artblocks.io/0x145789247973c5d612bf121e9e4eef84b63eb707/1000713` |
| Ex Nihilo (Cosmos) #248 | `https://token.artblocks.io/0x0000000c687daed0fba60d1dba4e5f6149e8b894/248` |

The token URI string is chain evidence. The response document at that URI is an issuer/platform-controlled external resource and must be captured, hashed, and preservation-tested before accession. The address-to-human attribution is not treated as proven solely by the address value; it needs an independent artist or project authority record in the accession dossier.

## Mint provenance

Each row below is supported by a successful transaction receipt containing an ERC-721 `Transfer` event with `from = 0x0000000000000000000000000000000000000000`. That is direct evidence of the token's minting event and initial on-chain recipient. It is not proof of the creator's legal title, the sale consideration, or the identity of the initial recipient.

| Object | Mint transaction | Block / block hash | UTC time | Transfer log | Initial recipient | Receipt status |
|---|---|---:|---|---:|---|---|
| CENTURY #31 | `0x37f8400704b8d2829dab23cb1df2e5ad85d7c7ae943797a91f40a99895677544` | 12704968 / `0x881417caed83cdfdbb21310b82e233ecb8ed9383f7969da9d2135382713c6bed` | 2021-06-25T19:00:08Z | 42 | `0xf873BeBDD61AB385D6b24C135BAF36C729CE8824` | `0x1` |
| CENTURY #724 | `0x0f6f3b970006c0d4efabc064f761a03dc93aa20a2b587643b8250e6f1afb53fb` | 12704986 / `0x86afb3a5aac6e07b4aa3f65b7628a805d6a24b9e6f02f626b6a1dcbc2e74de24` | 2021-06-25T19:04:52Z | 58 | `0x60C83D65F25F2791C1d66Ca129B035e7D5e2d2a1` | `0x1` |
| CENTURY #401 | `0x0337b7cd3a783d43d7ff55d1173664a1e172475cb6017fd311fa85cfb33a7242` | 12704978 / `0x476dc66de79efc853978bfba03586ab21eb8dee1f315e9585e7111edd010fbd2` | 2021-06-25T19:02:56Z | 23 | `0x36091073086495792E0ab3b94D230C2202243bAC` | `0x1` |
| Pre-Process #63 | `0x89de0effce798c6eb7557418a6ec9eeab78a583a05159e444fcd8cb6402fef39` | 16084576 / `0x19ec7108f7689d8fa5d5d5d2676918810b1b09cb629c0dd9519ebcb4827b5201` | 2022-11-30T18:25:23Z | 102 | `0x83f61D3c25f0596bA217426EdFFA6a446169148c` | `0x1` |
| Phototaxis #308 | `0x6a9ccda8e9d7f5dc87453d499972fa76eb19eb8cfc3479054afc8563f61156cf` | 13271125 / `0xbc2da252bb2570df669186fdacfc48466cff15bc969124ce7feef879792af096` | 2021-09-21T19:52:20Z | 116 | `0x9a19ff773eb4971c25f84882E609B2E3c44C4e8D` | `0x1` |
| 923 EMPTY ROOMS #713 | `0x96ce976bbe2e9393876cba120dc842a1c1cc1aea8f94e919b9b60c05d936c841` | 17943010 / `0xbdbfda459c29ca42efe8edfd912bb66c6d3a0c7acbe9f95d3d8875e24950195e` | 2023-08-18T16:57:59Z | 75 | `0xED075cAF72D905bC24C18007BFEA0f1dFA3353ad` | `0x1` |
| Ex Nihilo (Cosmos) #248 | `0xb432b939b0f4a5fde252f109267dd98f219d00a8939d819f746542be7b0846c2` | 24635482 / `0xd762381cc7466b760919539b9b3a0591a9a39f8f2c6fd19597ac4a1e439779ff` | 2026-03-11T16:41:35Z | 113 | `0x12bd6121197848F93F40bd82D4c80Db4E3198990` | `0x1` |

The Pre-Process mint receipt was read successfully and the event, block, timestamp, and status were verified; its block hash was not retained in the investigator's compact output. This is a report completeness gap, not an inferred value. It should be filled from `eth_getTransactionReceipt` before final accession publication.

## Common custody/acquisition transfer

The direct receipt for the common inbound transaction returned:

```text
transactionHash: 0xbdde33b32d4b70335b10cbd37c0b00a027844f14c900d82aa4f75b7a7b390498
blockHash:       0x059428dfd0b8a09d639fd37452ae9f74bc56fbadef31e19a98dc28bb7130297f
blockNumber:     25660311 (0x1878b97)
timestamp:       2026-08-01T13:25:47Z
receipt status:  0x1
transaction from: 0x6daa633c23615a29471deafae351727867e7dad1
transaction to:   0x0000000000c2d145a2526bd8c716263bfebe1a72
```

The receipt contained the following seven ERC-721 `Transfer` events. The event topic was `keccak256("Transfer(address,address,uint256)")`:

```text
0xa7d8d9ef8d8ce8992df33d8b8cf4aebabd5bd270  token 100000401  log 52  from 0x6daa633c23615a29471deafae351727867e7dad1  to 0xbecfa2ba5a782d11e1a0e821e8f2e30b6684178c
0xa7d8d9ef8d8ce8992df33d8b8cf4aebabd5bd270  token 100000724  log 59  from 0x6daa633c23615a29471deafae351727867e7dad1  to 0xbecfa2ba5a782d11e1a0e821e8f2e30b6684178c
0x0000000c687daed0fba60d1dba4e5f6149e8b894  token 248       log 54  from 0x6daa633c23615a29471deafae351727867e7dad1  to 0xbecfa2ba5a782d11e1a0e821e8f2e30b6684178c
0x99a9b7c1116f9ceeb1652de04d5969cce509b069  token 383000063 log 56  from 0x6daa633c23615a29471deafae351727867e7dad1  to 0xbecfa2ba5a782d11e1a0e821e8f2e30b6684178c
0x145789247973c5d612bf121e9e4eef84b63eb707  token 1000713   log 58  from 0x6daa633c23615a29471deafae351727867e7dad1  to 0xbecfa2ba5a782d11e1a0e821e8f2e30b6684178c
0xa7d8d9ef8d8ce8992df33d8b8cf4aebabd5bd270  token 164000308 log 53  from 0x6daa633c23615a29471deafae351727867e7dad1  to 0xbecfa2ba5a782d11e1a0e821e8f2e30b6684178c
0xa7d8d9ef8d8ce8992df33d8b8cf4aebabd5bd270  token 100000031 log 60  from 0x6daa633c23615a29471deafae351727867e7dad1  to 0xbecfa2ba5a782d11e1a0e821e8f2e30b6684178c
```

The source address is consistently `0x6DAA633C23615a29471dEaFae351727867E7dAD1`, but this report does not equate that address with a donor or legal transferor. A title instrument and a `TITLE_BINDING` record are still required.

## Complete indexed ERC-721 transfer paths

The following table preserves the complete transfer history returned by the Blockscout instance endpoints at the observation time. `token_minting` is the indexer's label for a zero-address mint event. The `method` label is intentionally omitted from the canonical facts because it is an indexer classification; the transaction hash, block, timestamp, addresses, contract, token ID, and log index are the relevant evidence. Every row should be independently reproducible from the transaction receipt.

| Object | Event | From | To | Transaction | Block | UTC time | Log |
|---|---|---|---|---|---:|---|---:|
| CENTURY #31 | mint | `0x0000000000000000000000000000000000000000` | `0xf873BeBDD61AB385D6b24C135BAF36C729CE8824` | `0x37f8400704b8d2829dab23cb1df2e5ad85d7c7ae943797a91f40a99895677544` | 12704968 | 2021-06-25T19:00:08Z | 42 |
| CENTURY #31 | transfer | `0xf873BeBDD61AB385D6b24C135BAF36C729CE8824` | `0x16FfE3938B69132c72A5b0250708792DB72971B4` | `0x6d430d2114c17fd186dc395c2add2752403d475019c57e9237ad735939e15b8c` | 12705685 | 2021-06-25T21:42:45Z | 262 |
| CENTURY #31 | transfer | `0x16FfE3938B69132c72A5b0250708792DB72971B4` | `0xB53349160E38739B37E4BbfCf950Ed26e26FcB41` | `0x098aaba06cdf92e20ff1fa1c54e57329dfb8bf4e95129d63f8cb97954fd08c77` | 12836105 | 2021-07-16T05:38:41Z | 152 |
| CENTURY #31 | transfer | `0xB53349160E38739B37E4BbfCf950Ed26e26FcB41` | `0xF3c7c2603BB7689D98d727769517B585D533ED57` | `0x843d1e49c000cea26c4b4507ea6ea416ad9ae27f40d5ed316935cd8c69bfd1ae` | 24121552 | 2025-12-29T23:22:35Z | 141 |
| CENTURY #31 | transfer | `0xF3c7c2603BB7689D98d727769517B585D533ED57` | `0xaa55b6B6c8b4Df868e89a4e96fA72253256D88B4` | `0xe5371c38dd27aa006fcb2cce4c80fc05fdb1bb2a9c720cf4e837d7c4e0d4977e` | 24222964 | 2026-01-13T02:58:35Z | 53 |
| CENTURY #31 | transfer | `0xaa55b6B6c8b4Df868e89a4e96fA72253256D88B4` | `0x6DAA633C23615a29471dEaFae351727867E7dAD1` | `0x742b596280872e27e3fbe677e116669129c355c2af5a82e95e0ff53dc307248b` | 25229951 | 2026-06-02T13:19:23Z | 1148 |
| CENTURY #31 | Museum receipt | `0x6DAA633C23615a29471dEaFae351727867E7dAD1` | `0xbECfa2bA5a782D11E1a0e821E8F2e30b6684178c` | `0xbdde33b32d4b70335b10cbd37c0b00a027844f14c900d82aa4f75b7a7b390498` | 25660311 | 2026-08-01T13:25:47Z | 60 |
| CENTURY #724 | mint | `0x0000000000000000000000000000000000000000` | `0x60C83D65F25F2791C1d66Ca129B035e7D5e2d2a1` | `0x0f6f3b970006c0d4efabc064f761a03dc93aa20a2b587643b8250e6f1afb53fb` | 12704986 | 2021-06-25T19:04:52Z | 58 |
| CENTURY #724 | transfer | `0x60C83D65F25F2791C1d66Ca129B035e7D5e2d2a1` | `0x5a418d8bc0C074A4A8fa88d1322dc51Cc1cb9d29` | `0x6a525a51b42920276d87cc93b2ceadd1905b7bfcdacd8427e676ce5c627454bf` | 12705312 | 2021-06-25T20:19:26Z | 94 |
| CENTURY #724 | transfer | `0x5a418d8bc0C074A4A8fa88d1322dc51Cc1cb9d29` | `0xdDcC629c76F311d894b7c2953942A8652Df2985d` | `0x45af7034454963db5fd23ff7f5d6d1a8506d6612ff39fd54d6f9e30d16be2199` | 13066336 | 2021-08-21T03:49:01Z | 409 |
| CENTURY #724 | transfer | `0xdDcC629c76F311d894b7c2953942A8652Df2985d` | `0x6DAA633C23615a29471dEaFae351727867E7dAD1` | `0x13b222ed800dc0a2c55f9c2ac4a505dc1e587df666ab8b8e7b0ee600caf6d92b` | 25230062 | 2026-06-02T13:41:35Z | 436 |
| CENTURY #724 | Museum receipt | `0x6DAA633C23615a29471dEaFae351727867E7dAD1` | `0xbECfa2bA5a782D11E1a0e821E8F2e30b6684178c` | `0xbdde33b32d4b70335b10cbd37c0b00a027844f14c900d82aa4f75b7a7b390498` | 25660311 | 2026-08-01T13:25:47Z | 59 |
| CENTURY #401 | mint | `0x0000000000000000000000000000000000000000` | `0x36091073086495792E0ab3b94D230C2202243bAC` | `0x0337b7cd3a783d43d7ff55d1173664a1e172475cb6017fd311fa85cfb33a7242` | 12704978 | 2021-06-25T19:02:56Z | 23 |
| CENTURY #401 | transfer | `0x36091073086495792E0ab3b94D230C2202243bAC` | `0x5AEEdbc6b655C13950F32E5E8a0760D15Bbe0Afb` | `0xa68a7cec9339846e5d132ff153654ede0d9c6fafb32c12c8308add1b7fe114aa` | 12705212 | 2021-06-25T19:58:20Z | 69 |
| CENTURY #401 | transfer | `0x5AEEdbc6b655C13950F32E5E8a0760D15Bbe0Afb` | `0xCf19536605796f12dFE929f7e32Cc1631c1E2124` | `0xc506465c8f86a821eeae2d4068037fc1ed6e71110296552c3b46381ed76ce6fb` | 12904548 | 2021-07-26T22:49:08Z | 56 |
| CENTURY #401 | transfer | `0xCf19536605796f12dFE929f7e32Cc1631c1E2124` | `0x5AEEdbc6b655C13950F32E5E8a0760D15Bbe0Afb` | `0xba892314dc049233996fa05b238ff499b902e1e075700cf43d3341563000b744` | 23270314 | 2025-09-01T19:16:35Z | 489 |
| CENTURY #401 | transfer | `0x5AEEdbc6b655C13950F32E5E8a0760D15Bbe0Afb` | `0x6DAA633C23615a29471dEaFae351727867E7dAD1` | `0x6690542f972ba00b8fd7cadc90efcd5eaf3157a6e105f44cd51b1909091c79a8` | 25660193 | 2026-08-01T13:02:11Z | 470 |
| CENTURY #401 | Museum receipt | `0x6DAA633C23615a29471dEaFae351727867E7dAD1` | `0xbECfa2bA5a782D11E1a0e821E8F2e30b6684178c` | `0xbdde33b32d4b70335b10cbd37c0b00a027844f14c900d82aa4f75b7a7b390498` | 25660311 | 2026-08-01T13:25:47Z | 52 |
| Pre-Process #63 | mint | `0x0000000000000000000000000000000000000000` | `0x83f61D3c25f0596bA217426EdFFA6a446169148c` | `0x89de0effce798c6eb7557418a6ec9eeab78a583a05159e444fcd8cb6402fef39` | 16084576 | 2022-11-30T18:25:23Z | 102 |
| Pre-Process #63 | transfer | `0x83f61D3c25f0596bA217426EdFFA6a446169148c` | `0x8c12C52685de09E583D5E2B7ba56B3583484534B` | `0x4cba74271f8c21a03675efe19c81420f50994f8171c864d70a3c1208077e12b7` | 24286196 | 2026-01-21T22:37:23Z | 276 |
| Pre-Process #63 | transfer | `0x8c12C52685de09E583D5E2B7ba56B3583484534B` | `0x6DAA633C23615a29471dEaFae351727867E7dAD1` | `0x1e875add011f20ef6070e9aa66ffb707928638a60b6d3062bfa5d598c362789f` | 25278547 | 2026-06-09T08:02:59Z | 72 |
| Pre-Process #63 | Museum receipt | `0x6DAA633C23615a29471dEaFae351727867E7dAD1` | `0xbECfa2bA5a782D11E1a0e821E8F2e30b6684178c` | `0xbdde33b32d4b70335b10cbd37c0b00a027844f14c900d82aa4f75b7a7b390498` | 25660311 | 2026-08-01T13:25:47Z | 56 |
| Phototaxis #308 | mint | `0x0000000000000000000000000000000000000000` | `0x9a19ff773eb4971c25f84882E609B2E3c44C4e8D` | `0x6a9ccda8e9d7f5dc87453d499972fa76eb19eb8cfc3479054afc8563f61156cf` | 13271125 | 2021-09-21T19:52:20Z | 116 |
| Phototaxis #308 | transfer | `0x9a19ff773eb4971c25f84882E609B2E3c44C4e8D` | `0x80c939F8A66C59B37330f93f1002541fD4E51aa2` | `0x33e5fbe52b5fecd6b3d8bd29e6ef903381d561a7b4962843e701a1ee3f203cfc` | 13300954 | 2021-09-26T10:49:18Z | 640 |
| Phototaxis #308 | transfer | `0x80c939F8A66C59B37330f93f1002541fD4E51aa2` | `0x28458F3442841dA5E4773b39286447D27EC57b59` | `0x45a30535390ce1475707823c1ae356bfcf4af9179c485c612776cc974758731b` | 14747067 | 2022-05-10T06:31:15Z | 148 |
| Phototaxis #308 | transfer | `0x28458F3442841dA5E4773b39286447D27EC57b59` | `0xE7e7cb488084Bb6bA9D65f6C8372d705c0485D13` | `0x37ba554762c7b09b76ea71468999050c088c1846da9b9a5e632161eefc806770` | 16549061 | 2023-02-03T15:10:11Z | 303 |
| Phototaxis #308 | transfer | `0xE7e7cb488084Bb6bA9D65f6C8372d705c0485D13` | `0x6DAA633C23615a29471dEaFae351727867E7dAD1` | `0x472bb5b1b2d25927c14ba0f56a38cc8a88006a5d405cf5e8e681a33a530425a6` | 25660172 | 2026-08-01T12:57:59Z | 782 |
| Phototaxis #308 | Museum receipt | `0x6DAA633C23615a29471dEaFae351727867E7dAD1` | `0xbECfa2bA5a782D11E1a0e821E8F2e30b6684178c` | `0xbdde33b32d4b70335b10cbd37c0b00a027844f14c900d82aa4f75b7a7b390498` | 25660311 | 2026-08-01T13:25:47Z | 53 |
| 923 EMPTY ROOMS #713 | mint | `0x0000000000000000000000000000000000000000` | `0xED075cAF72D905bC24C18007BFEA0f1dFA3353ad` | `0x96ce976bbe2e9393876cba120dc842a1c1cc1aea8f94e919b9b60c05d936c841` | 17943010 | 2023-08-18T16:57:59Z | 75 |
| 923 EMPTY ROOMS #713 | transfer | `0xED075cAF72D905bC24C18007BFEA0f1dFA3353ad` | `0x31fC857D467AEEc23d31EF7C89b0054Eec49f711` | `0x0180274ec55b5b59033b371ccc25da00004fac9706b5d294a4d049ba177e4c6a` | 17943498 | 2023-08-18T18:35:59Z | 374 |
| 923 EMPTY ROOMS #713 | transfer | `0x31fC857D467AEEc23d31EF7C89b0054Eec49f711` | `0x0F3378E9337c13B0D20Bb3EBb6ce0F804c81DA77` | `0xca8b3c0dbb64fc62b022102085c8de85da4d97175b799c619b1eec69715358bc` | 17950148 | 2023-08-19T16:56:11Z | 357 |
| 923 EMPTY ROOMS #713 | transfer | `0x0F3378E9337c13B0D20Bb3EBb6ce0F804c81DA77` | `0xAEb4c41BFe72D72255D3744936dB056ee8308779` | `0x5ad581a40f5f842f4f7da0e630f7a42f6cd939407bb9a416defdad7bfddf79d7` | 18132735 | 2023-09-14T06:29:11Z | 110 |
| 923 EMPTY ROOMS #713 | transfer | `0xAEb4c41BFe72D72255D3744936dB056ee8308779` | `0xd7b064F257428e7B0d5f6216BC31EcDebdCCad62` | `0x353b45ddd65035f197cf8c986d754d235601d01e3f57f73130a95d1cb596851e` | 19754765 | 2024-04-28T15:39:11Z | 265 |
| 923 EMPTY ROOMS #713 | transfer | `0xd7b064F257428e7B0d5f6216BC31EcDebdCCad62` | `0xF61030d320E71256a43ec22839db345d80ac84B3` | `0xada776efae147b8bb82e729c374198eacd9aa25bc01058c1b9f4dfe6692450aa` | 24014842 | 2025-12-15T01:52:35Z | 418 |
| 923 EMPTY ROOMS #713 | transfer | `0xF61030d320E71256a43ec22839db345d80ac84B3` | `0x6DAA633C23615a29471dEaFae351727867E7dAD1` | `0x208f2e7b664e43018f37f9fce5b3ac1b5de0d56a17ea6136fa0b4784c20de8a7` | 25281309 | 2026-06-09T17:17:11Z | 218 |
| 923 EMPTY ROOMS #713 | Museum receipt | `0x6DAA633C23615a29471dEaFae351727867E7dAD1` | `0xbECfa2bA5a782D11E1a0e821E8F2e30b6684178c` | `0xbdde33b32d4b70335b10cbd37c0b00a027844f14c900d82aa4f75b7a7b390498` | 25660311 | 2026-08-01T13:25:47Z | 58 |
| Ex Nihilo (Cosmos) #248 | mint | `0x0000000000000000000000000000000000000000` | `0x12bd6121197848F93F40bd82D4c80Db4E3198990` | `0xb432b939b0f4a5fde252f109267dd98f219d00a8939d819f746542be7b0846c2` | 24635482 | 2026-03-11T16:41:35Z | 113 |
| Ex Nihilo (Cosmos) #248 | transfer | `0x12bd6121197848F93F40bd82D4c80Db4E3198990` | `0x6DAA633C23615a29471dEaFae351727867E7dAD1` | `0xe277326e855eec1b0224914a071c181ce44daace570b2228c40814a09b8bca7b` | 25658325 | 2026-08-01T06:48:11Z | 221 |
| Ex Nihilo (Cosmos) #248 | Museum receipt | `0x6DAA633C23615a29471dEaFae351727867E7dAD1` | `0xbECfa2bA5a782D11E1a0e821E8F2e30b6684178c` | `0xbdde33b32d4b70335b10cbd37c0b00a027844f14c900d82aa4f75b7a7b390498` | 25660311 | 2026-08-01T13:25:47Z | 54 |

The complete history shows that all seven tokens were held by the same source address immediately before the common receipt. They reached that address through separate prior transfers (or, for the most recently minted token, a direct prior transfer). Those address relationships are recorded as chain facts only.

## Reproducibility commands and API URLs

The following PowerShell pattern performs a JSON-RPC read without any credential:

```powershell
$rpc = 'https://ethereum.publicnode.com'
$body = @{
  jsonrpc = '2.0'
  id = 1
  method = 'eth_call'
  params = @(
    @{ to = '<contract>'; data = '<calldata>' },
    'latest'
  )
} | ConvertTo-Json -Depth 8
Invoke-RestMethod -Method Post -Uri $rpc -ContentType 'application/json' -Body $body
```

For direct ownership verification, concatenate selector `0x6352211e` with the 32-byte big-endian token ID. For example, CENTURY #31 (`100000031`, hex `0x5f5e11f`) uses:

```text
0x6352211e000000000000000000000000000000000000000000000000000005f5e11f
```

For each object, repeat the call against its contract address in the identity table. The direct result is a 32-byte ABI address word ending in the current owner's address.

For project and artist reads:

```text
tokenIdToProjectId(uint256):       0x1b689c0b + uint256(tokenId)
projectIdToArtistAddress(uint256): 0xa47d29cb + uint256(projectId)
tokenURI(uint256):                 0xc87b56dd + uint256(tokenId)
```

For the common receipt:

```powershell
$body = @{
  jsonrpc = '2.0'
  id = 1
  method = 'eth_getTransactionReceipt'
  params = @('0xbdde33b32d4b70335b10cbd37c0b00a027844f14c900d82aa4f75b7a7b390498')
} | ConvertTo-Json -Depth 8
Invoke-RestMethod -Method Post -Uri 'https://ethereum.publicnode.com' -ContentType 'application/json' -Body $body
```

For each mint transaction, use the same `eth_getTransactionReceipt` method with the transaction hash in the mint table, then inspect logs for topic:

```text
0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef
```

The indexed historical endpoint for a token is:

```text
https://eth.blockscout.com/api/v2/tokens/<lowercase-contract>/instances/<decimal-token-id>/transfers
```

Useful human-readable evidence views, not substitutes for RPC reads, are:

```text
https://eth.blockscout.com/address/0xbECfa2ba5a782D11E1a0e821E8F2e30b6684178c
https://eth.blockscout.com/tx/0xbdde33b32d4b70335b10cbd37c0b00a027844f14c900d82aa4f75b7a7b390498
```

## Uncertainty and accession follow-up

The following items remain unresolved and must not be guessed:

- **Legal title:** the common transfer proves on-chain receipt, not donation acceptance or legal title. Obtain the signed donor instrument and bind it to the exact transfer transaction and seven token identities with `TITLE_BINDING`.
- **Donor identity:** `0x6DAA...` is the on-chain source address for the seven receipt events. No human or legal identity is asserted from the address label alone.
- **Custody identity:** the ENS resolution and `ownerOf` calls establish the observed address. Recheck ENS and Safe state at every accession milestone and custody audit.
- **Creator identity:** the contracts return the same project artist address and issuer metadata names Casey REAS. The artist address still needs an independent authority record or signed project/artist statement for a museum-grade attribution.
- **Metadata persistence:** token URI responses are external and may change. Capture raw responses, content types, response headers where useful, render inputs, scripts/dependencies, and SHA-256/Keccak-256 fixity before accession publication.
- **Proxy implementation:** the Ex Nihilo contract is reported by the explorer as an EIP-1167 proxy. Resolve and record its implementation address and implementation-code hash in the technical dossier; do not treat the proxy label as a creator or rights statement.
- **Marketplace semantics:** transfer method labels in the indexed history suggest marketplace activity but do not prove a sale, price, title passage, or donor intent. Those assertions require transaction-level and legal evidence.
- **Accession status:** this report supports `received_onchain` / custody verification at the observed head. It does not support `accessioned`, `catalogued`, `technically_verified`, `preservation_complete`, or `display_ready` without the remaining Museum gates.

## Evidence conclusion

The seven described Casey REAS token identities are resolved without guessing:

```text
CENTURY #31              Art Blocks / project 100 / token 100000031
CENTURY #724             Art Blocks / project 100 / token 100000724
CENTURY #401             Art Blocks / project 100 / token 100000401
Pre-Process #63          Art Blocks / project 383 / token 383000063
Phototaxis #308          Art Blocks / project 164 / token 164000308
923 EMPTY ROOMS #713     Art Blocks x Bright Moments / project 1 / token 1000713
Ex Nihilo (Cosmos) #248  Art Blocks Studio | 92 / project 0 / token 248
```

Their current ERC-721 owner is the address resolved by `networkmuseum.6529.eth`, and the seven inbound custody events are in one successful transaction at block `25,660,311`. The report is sufficient as the on-chain evidence layer of a provisional accession dossier, but not as the complete accession itself.

## Accession resolution — 2026-08-02

The preceding uncertainty section records the boundary of this on-chain research at the time it was written. The completed accession dossier resolves those accession questions as follows and leaves the original research text intact as a historical audit trail:

- The donor's full-gift declaration, exact delivery, formal Museum acceptance, and institutional title declaration establish title to the seven tokens and the donor's entire transferable interest, subject to the expressly accepted residual risk of undisclosed private claims. They do not transfer Casey REAS's copyright.
- The public donor credit is punk6529. The chain record separately preserves `0x6DAA...` as the transfer source without using the wallet label as proof of a legal identity.
- Current custody and the receipt event are fixed to transaction, block, log, contract, token ID, destination, and retained raw receipt. Custody remains subject to periodic verification as ordinary collection care.
- Artist attribution is accepted from mutually consistent artist, Art Blocks, project, issuer-metadata, and contract project-artist sources. No contradictory attribution evidence was found; an additional artist-signed statement is not required for accession.
- All seven raw metadata responses are retained with fixity. Generator, script, dependency, and independent render-environment capture remain active technical-conservation actions rather than unanswered accession decisions.
- The Ex Nihilo proxy implementation remains a technical-provenance enrichment item; no identity, custody, rights, or display conflict was found that would make it an accession blocker.
- Marketplace labels and rarity metrics are excluded. The Museum's transparent descriptors make no sale, value, rarity, ranking, or quality claim.
- The lot and all seven objects are `accessioned`. `technically_verified`, `preservation_complete`, and unconditional `display_ready` remain later, stricter lifecycle states.

The controlling current determinations are the [accession certificate](../../records/accessions/6529NM.2026.001/public/accession-certificate.md), [title and rights review](../../records/accessions/6529NM.2026.001/public/title-rights-and-accession-review.md), and [technical and condition review](../../records/accessions/6529NM.2026.001/public/technical-and-condition-review.md).
