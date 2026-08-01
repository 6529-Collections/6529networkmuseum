# Keys and Gates registrar-research evidence inventory

Status: research inventory; not an accession register and not an accession decision.

Prepared by the Keys and Gates registrar-research constructor on 2026-08-01 UTC. Mutable Wave and chain facts were re-read live at approximately `2026-08-01T15:00:52Z` through the authenticated local `punk6529bot` tooling and public Ethereum indexer endpoints. The two formal program documents were fetched directly at the same research pass.

## Registrar invariant

For every selected work, preserve this state machine explicitly:

`WINNER` != `ACQUIRED` != `RECEIVED_ONCHAIN` != `ACCESSIONED` != `CATALOGUED`.

In this inventory, `WINNER` means only that the live Keys and Gates Wave API exposes the drop as `drop_type: WINNER` with a `winning_context.place` and a manual award label. It does not prove a purchase, a completed mint, a transfer, title passage, rights completion, custody, or accession. The institutional Museum Wave expressly says that sending an item to the Museum wallet does not itself accession the item; the same rule applies to a selected work that has not yet passed the accession gates.

## 1. Source register and provenance

### Live 6529.io sources

| Source | Identifier and direct link | Observation / integrity |
|---|---|---|
| Museum Wave | Wave `5f207393-5418-4a75-8738-e40edb44a94d`; [wave](https://6529.io/waves/5f207393-5418-4a75-8738-e40edb44a94d) | Authenticated refresh at `2026-08-01T14:56:48Z`; 2,629 drops: 2,621 chat drops and 8 proposals. Local generated snapshot SHA-256: `2185bbc52ed47c7a4a35b5bdee4ce75a0e55c8633d420aa5cd9ac7997c6edaef`. Local searchable chronology SHA-256: `8bbe10e4035c7adde9a25bb2b0063e5540af3ace950d7fdae0eac9dfeece1159`. |
| Keys and Gates Wave | Wave `4ff022b3-aa17-4a0a-ba78-58f64ff1d427`; [wave](https://6529.io/waves/4ff022b3-aa17-4a0a-ba78-58f64ff1d427) | Live metadata: `voting_period_start=2026-05-09T19:45:46.161Z`, `voting_period_end=2026-07-09T12:00:00Z`, `voting_credit_type=TDH`, `voting_credit_scope=WAVE`, `voting_credit_nfts=null`. The live read endpoint was queried with `--limit 199 --auth`; the individual selected drops below were also fetched directly by ID. |
| K&G description drop | Serial `972000`, drop `71c798bc-629d-46f2-8610-507a91be4f57`; [drop](https://6529.io/waves/4ff022b3-aa17-4a0a-ba78-58f64ff1d427?drop=71c798bc-629d-46f2-8610-507a91be4f57) | Author `simo`; created `2026-05-09T19:47:20.206Z`. The description identifies Keys and Gates as Museum Benefit Work Edition and Accession Program #1. UTF-8 content SHA-256, with `parts[].content` joined by LF: `72ea4ada83f73a788dd585519a85b544a4c14a694203b33944432ed00e80b7fb`. |
| Museum accession principle | Serial `1052455`, drop `686bedee-ad99-44d7-bfb9-80d030d61ae2`; [drop](https://6529.io/waves/5f207393-5418-4a75-8738-e40edb44a94d?drop=686bedee-ad99-44d7-bfb9-80d030d61ae2) | `@punk6529`, `2026-06-02T14:15:59Z`: sending an item to the Museum wallet is not accession; it only communicates scope. This is chat context, but it is consistent with the formal institutional note and the adopted Donation Acceptance Policy. |
| Explicit-decision principle | Serial `1053355`, drop `b977ff34-cf95-4f23-b377-7b6f54b67e69`; [drop](https://6529.io/waves/5f207393-5418-4a75-8738-e40edb44a94d?drop=b977ff34-cf95-4f23-b377-7b6f54b67e69) | `@punk6529`, `2026-06-02T19:15:53Z`: “there should be no unstated decision.” Relevant control for distinguishing Wave selection from accession. |
| Adopted general collecting scope | Serial `1052604`, drop `d65befc2-65dc-4362-8ddd-75f867338669`; [drop](https://6529.io/waves/5f207393-5418-4a75-8738-e40edb44a94d?drop=d65befc2-65dc-4362-8ddd-75f867338669) | Live Museum snapshot classifies this proposal `WINNER`; use the exact adopted payload for scope authority. |
| Adopted donation policy | Serial `1052812`, drop `86e43beb-b55d-42f0-9eea-a3c115b08abc`; [drop](https://6529.io/waves/5f207393-5418-4a75-8738-e40edb44a94d?drop=86e43beb-b55d-42f0-9eea-a3c115b08abc) | Live Museum snapshot classifies this proposal `WINNER`; use the exact adopted payload for acceptance and non-automatic-accession authority. |

The original Museum URL supplied with `divider=1132915` points to a single Museum chat message and is not a decision boundary. The complete local Museum chronology was read as a whole; targeted K&G governance and implementation references are listed below rather than treating chat as an enacted amendment to the formal program note.

### Formal public notes

| Source | Direct link | Retrieved HTML SHA-256 | Authority |
|---|---|---|---|
| Institutional note | [The 6529 Network Museum](https://6529networkmuseum_thememes.ar.io/) | `75889ed25b623fde356129e39ba5330d4c0c2b38de0f3a7d94355282ff28b8d4` | Institutional mission, public-good posture, custody reference, permanent-holding principle, acquisition pathways, documentation expectations, CC0 default, and primary-acquisition preference. |
| Program note | [Keys and Gates](https://keysandgates_thememes.ar.io/) | `0dbb79439224de8c86359a164f4777c81a70c3bc2eb852127a2ec54ae467a441` | Program-specific frame, eligibility, submission package, rights and consent requirements, voting pattern, fallback rule, acquisition terms, and publication outputs. The note states that the Meme Card controls if a program fact differs from it. |

### Chain and custody sources

| Source | Direct link / query | Observation |
|---|---|---|
| ENS resolution | [ENS resolver result](https://api.ensideas.com/ens/resolve/networkmuseum.6529.eth) | `networkmuseum.6529.eth` resolved to `0xbECfa2bA5a782D11E1a0e821E8F2e30b6684178c`. |
| Museum Safe NFT enumeration | [Blockscout address NFT API](https://eth.blockscout.com/api/v2/addresses/0xbECfa2bA5a782D11E1a0e821E8F2e30b6684178c/nft) | At the observation time the endpoint returned 8 items: the seven Casey Reas objects recorded in the separate Casey research effort and one unrelated `The Life of Larry` ERC-1155 item. No matching K&G winner token was present in this current indexed Safe inventory. This is a negative indexer observation, not proof that no K&G token exists anywhere. |
| Individual K&G token identity | Not available | No selected K&G drop currently exposes a contract address, token ID, transaction hash, or `nft_links` field in the live direct drop response. Do not invent an on-chain identity from a media URL or a Wave award label. |

## 2. Program rules and fixed mechanics

The following are the rules represented by the formal notes and live Wave metadata. They are separate from later chat suggestions about changing the voting credit or creating a committee.

### Institutional frame

- Keys and Gates is the first 6529 Network Museum accession program, `6529NM-AP-01`.
- It is a Meme Card benefit-work program: mints fund acquisitions of 1/1 works for the Museum’s permanent public holding.
- The curatorial premise is photography about access, exclusion, permission, surveillance, custody, autonomy, and the right to exit.
- The institutional note describes the collection as a public-good cultural institution, not an investment vehicle; accessioned works are intended for long-term/permanent holding.
- Custody reference: `networkmuseum.6529.eth`.
- Fixed acquisition price: `0.5 ETH` per acquired work.
- Total quantity is determined by the number of Meme Cards minted; the budget is therefore mint-dependent.
- License: CC0 only. The program is intended to produce public-commons cultural material.
- People depicted require documented written consent suitable for a CC0 release. Identifiable minors are excluded.
- The artist must be able to release the original photograph under CC0 and warrant the release.

### Eligibility and submission package

- Original photograph made by the submitting artist.
- One-of-one work (`1/1`).
- Up to three works per artist.
- Title, year, and location, with location permitted to be `withheld` where appropriate.
- A 75–150 word caption explaining the threshold, control, custody, access, or exit dynamic.
- Technical note covering process, camera/workflow, and material manipulation.
- CC0 declaration.
- Where people are depicted, confirmation that written consent documentation exists and can be produced on request.
- The program note expected first on-chain minting through a Museum common contract unless the final mechanics specified otherwise. This expectation is not evidence that a contract was deployed or that a selected work was minted.

### Curatorial and exclusion criteria

The program note seeks photographs that stand alone as photographs and also form a coherent first photography subcollection. It expressly includes thresholds, civic/state systems, permissioning and membership, financial and market gatekeeping, surveillance/compliance, informal autonomy, the right to exit, and self-custody/self-sovereignty as lived experience. It excludes tourism aesthetics without a control/access/custody/exit story, studio portraiture without a clear relationship to the premise, slogan-led or literal crypto work without photographic force, works without documented CC0-suitable consent, sensitive personal-data/doxxing risks, and identifiable minors.

The formal selection standards are photographic strength and craft; clarity of the control/access/custody/exit theme; distinct voice and point of view; long-horizon relevance as document and image; documentation quality; and suitability for permanent CC0 accession.

### Selection and fallback

- Submissions were compiled into a single program Wave.
- The live Wave metadata records TDH voting with `WAVE` scope, not K&G-card-only TDH.
- The voting window was `2026-05-09T19:45:46.161Z` through `2026-07-09T12:00:00Z`.
- The API currently exposes sixteen `WINNER` drops with `winning_context.place` 1–16 and a decision time equal to `2026-07-09T12:00:00Z`.
- The live API does not expose a contract address, token ID, purchase transaction, sale time, or sale price for these winners; all sixteen direct responses observed had `sale_time=null` and `sale_price=null`.
- The final accession list is subject to availability, program terms, documentation, consent, and all other acceptance controls.
- If a selected work is unavailable or fails program terms at acquisition, the allocation rolls to the next eligible work in rank order.

### Required public outputs

The program note calls for a curatorial subcollection page, standardized individual object pages, a checklist of final accessions, and a compact durable downloadable catalogue. A Wave winner list is not one of those completed accession outputs.

## 3. Selection mechanics: formal record versus later discussion

The following live configuration is the operative selection evidence:

```text
Wave: 4ff022b3-aa17-4a0a-ba78-58f64ff1d427
Name: Keys and Gates
Description drop: 71c798bc-629d-46f2-8610-507a91be4f57 (serial 972000)
Voting credit type: TDH
Voting credit scope: WAVE
Voting credit NFTs: null
Voting start: 2026-05-09T19:45:46.161Z
Voting end: 2026-07-09T12:00:00Z
```

The Museum Wave contains a substantial discussion of proxy voting, expert photography input, whether voting should use only the K&G Meme Card’s TDH, and whether self-voting is appropriate when sixteen works can win. Those are preserved as discussion and implementation context, not as retroactive changes to the live Wave configuration:

- Serial `1072962`, drop `6dca1ce5-605c-4de8-9002-033d1ebf92fc`: @punk6529 said that delegating/proxying TDH to a photography expert could be useful for K&G.
- Serial `1073205`, drop `9864c53f-9aea-4498-840f-3706c1914030`: @gpebbles described sharing a substantial amount of voting power with an expert photographer for K&G.
- Serial `1073208`, drop `5403aa31-79ed-416f-b165-3e43e2df9c7c`: @punk6529 distinguished a K&G-specific proxy grant from general voting power.
- Serial `1073268`, drop `7bef144f-8502-4657-801e-973fce144568`: discussion of asking a proxy for a K&G vote and then pressing the vote button.
- Serial `1086358`, drop `f62fbe6b-d170-45bc-b75c-66d3f6162a88`: question about whether a self-voter could place their own work in the top sixteen.
- Serial `1086405`, drop `0d412bce-af9e-43db-bdfe-ad8492554dfb`, and serial `1086424`, drop `2e47d659-21dd-4f58-b693-328e81a4f965`: proposals in discussion for K&G-card-only TDH.
- Serial `1086488`, drop `4657e279-7a13-4f74-a0dc-1cf784db366e`: statement that K&G-card TDH had originally been contemplated.
- Serial `1086621`, drop `60313e3f-a3da-4c24-bd5b-bcb605e578c6`: self-voting and a smaller K&G-card TDH electorate were discussed as possible remedies.

None of these discussion drops is an adopted amendment to the formal program note, and the live Wave metadata shows `TDH/WAVE`. Do not rewrite the selection mechanics as K&G-card-only voting or committee selection.

## 4. Sixteen selected drops

### How to read the records

- `statement_sha256` is SHA-256 over the UTF-8 bytes of the direct API response’s `parts[].content`, joined by LF. It commits the submitted caption/statement as retrieved, while the direct drop link remains the canonical human-readable source.
- The direct API `title` field was empty for these winner responses. Titles below are transcribed from the artist’s first heading/title in `parts[].content`; that normalization is marked as a source-quality issue below.
- Media URLs were live and reported `media_status=ready` at observation. Media bytes were not downloaded in this pass, so no media-byte hash is claimed.
- Scores are Wave rating evidence only. No OpenSea rarity or marketplace rarity metric was used.
- All sixteen winner responses carried `winning_context.awards[0].type=MANUAL` and description `Acquisition by the 6529 Network Museum / Acquisition by the 6529 Network Museum`; that label is not proof of acquisition or accession.

### 1. GulYildiz — “Take the Key !”

- Wave serial `1085874`; drop `c3283930-101e-4e3a-b921-57d81649ca81`; [canonical drop](https://6529.io/waves/4ff022b3-aa17-4a0a-ba78-58f64ff1d427?drop=c3283930-101e-4e3a-b921-57d81649ca81).
- Created `2026-06-12T19:16:47.872Z`; decision `2026-07-09T12:00:00Z`; place 1; rating `18,739,379`; raters `62`.
- Statement SHA-256: `9ea93ea62fd6bd805cd298169e78dbb6628f29f957ad6935bae209cab9582138`.
- Media: [JPEG](https://d3lqz0a4bldqgf.cloudfront.net/drops/author_61b48317-f46c-45b3-beed-cfd9054326d8/2a39fe28-4040-4a80-92a6-306384a4e735/DSCF2374-copy-2.jpg); source MIME `image/jpeg`.
- Artist statement: a person stands before a light-filled door; the key becomes a metaphor for knowledge, authority, digital sovereignty, responsibility, and transformation. The artist connects Web3 keys to direct user ownership while warning that a key can open a new labyrinth as well as freedom. Technical representation: Cologne/Germany; Fujifilm camera; 10–24 mm.
- Rights/consent representation: “I, Gül Yıldız, declare that if this piece is selected and purchased by the 6529 Network Museum, this work will be released under CC0 and I have full rights to make that release.” The text contains no separate written-consent representation for any depicted person. The CC0 wording is conditional and must be replaced or confirmed by executed acquisition documentation before accession.
- Current status: `WINNER=verified`; mint/contract/token ID `not verified`; acquisition `not verified`; custody `not verified`; accession `not verified`.

### 2. HugoFaz — “the Artist in teh Open Sea”

- Wave serial `1171592`; drop `35efbf4c-2633-4b14-aa6a-82ea7660b6b9`; [canonical drop](https://6529.io/waves/4ff022b3-aa17-4a0a-ba78-58f64ff1d427?drop=35efbf4c-2633-4b14-aa6a-82ea7660b6b9).
- Created `2026-07-06T23:51:59.982Z`; decision `2026-07-09T12:00:00Z`; place 2; rating `12,319,732`; raters `35`.
- Statement SHA-256: `1984e94dbe7417b071dcf35af0b359f6375e5b14a242817880aaef9093c304a3`.
- Media: [JPEG](https://d3lqz0a4bldqgf.cloudfront.net/drops/author_0f82f62c-87b4-11ee-9d82-029a0e4b6159/f36442bb-9ece-4410-b0af-c32ccbc8fd27/The-Artist-in-the-OpenSea-by-Hugo-Faz.jpeg); source MIME `image/jpeg`.
- Artist statement: a man rows a bathtub through rush-hour traffic. The absent water and the slow self-directed motion become a metaphor for an artist moving through a market optimized for volume and speed. Technical representation: 6000 × 4000 px composite long-exposure digital photograph, Canon 6D Mark II, directed/shot/edited/color-graded by Hugo Faz, São Paulo, 2026-07-06.
- Rights/consent representation: Hugo states full rights, formal consent to release under CC0, relinquishment of copyright and related rights, and permanent accession as part of the Museum collection. The text does not separately identify model consent for the man depicted. Verify the legal basis and any model release in restricted registrar records.
- Current status: `WINNER=verified`; mint/contract/token ID `not verified`; acquisition `not verified`; custody `not verified`; accession `not verified`.

### 3. nasimghanizadeh — “Managed Freedom”

- Wave serial `980507`; drop `b47b7d58-6276-45ba-b707-ec0f623e39e2`; [canonical drop](https://6529.io/waves/4ff022b3-aa17-4a0a-ba78-58f64ff1d427?drop=b47b7d58-6276-45ba-b707-ec0f623e39e2).
- Created `2026-05-12T02:04:20.834Z`; decision `2026-07-09T12:00:00Z`; place 3; rating `12,280,514`; raters `55`.
- Statement SHA-256: `48d3c7657b0c3b51402580b788e536e378c45c17d8df1bb54cdabad2aaf57052`.
- Media: [JPEG](https://d3lqz0a4bldqgf.cloudfront.net/drops/author_3193a483-dbd5-46b5-801b-ef54b5450314/45742d59-df5d-4d1a-9dc4-f25812df220f/Managed-Freedom.jpg); source MIME `image/jpeg`.
- Artist statement: a horse herd moving through a central-Turkey landscape appears unrestricted but remains shaped by riders, training, hierarchy, and invisible boundaries. The work treats freedom as negotiated within systems of control, while also invoking migration, departure, refusal, shelter, and quiet exit. Technical representation: Kayseri, Turkey, 2023; Canon 5D Mark IV; 24–105 mm at 70 mm; slight rotation and mild color correction; no AI manipulation.
- Rights/consent representation: conditional CC0 declaration and full-rights representation if selected and purchased. Riders or other people may be present in the landscape, but the submission text contains no separate consent representation. Verify depiction and consent before any public release.
- Current status: `WINNER=verified`; mint/contract/token ID `not verified`; acquisition `not verified`; custody `not verified`; accession `not verified`.

### 4. intrepid — “No Key, Only Light”

- Wave serial `1152154`; drop `57c49f95-7854-4a2a-ba2c-d448bc7827fc`; [canonical drop](https://6529.io/waves/4ff022b3-aa17-4a0a-ba78-58f64ff1d427?drop=57c49f95-7854-4a2a-ba2c-d448bc7827fc).
- Created `2026-07-01T12:23:08.685Z`; decision `2026-07-09T12:00:00Z`; place 4; rating `10,999,442`; raters `39`.
- Statement SHA-256: `4eb3da8002606b875c5e8be662244d09337be77eb00b6a570d7256712f06d054`.
- Media: [JPEG](https://d3lqz0a4bldqgf.cloudfront.net/drops/author_0f82f79b-87b4-11ee-9d82-029a0e4b6159/d466bc20-0b84-47d9-b542-15dcd74f59e4/No-Key-Only-Light.jpg); source MIME `image/jpeg`.
- Artist statement: the artist’s children stand in Fort Frederick, Grenada, facing the light of an open doorway after four months stranded on a sailboat during the pandemic. The work layers personal border trauma onto the fort’s colonial, revolutionary, and military history. Technical representation: 2020, Fort Frederick, Grenada; Canon 6D Mark II; Canon EF 16–35 mm at 33 mm; minor Lightroom contrast/color adjustments.
- Rights/consent representation: conditional CC0 declaration, full-rights representation, and explicit statement that all people depicted consented and are covered by appropriate model releases. The referenced children and historical/political setting require careful restricted verification even though the representation is explicit.
- Current status: `WINNER=verified`; mint/contract/token ID `not verified`; acquisition `not verified`; custody `not verified`; accession `not verified`.

### 5. ikertje — “Residual Barrier”

- Wave serial `981298`; drop `52631c54-fcce-46e7-b88c-5100de46734c`; [canonical drop](https://6529.io/waves/4ff022b3-aa17-4a0a-ba78-58f64ff1d427?drop=52631c54-fcce-46e7-b88c-5100de46734c).
- Created `2026-05-12T09:49:50.834Z`; decision `2026-07-09T12:00:00Z`; place 5; rating `10,838,602`; raters `36`.
- Statement SHA-256: `87ef3daea36e02e1c5517ea18d26cc17e83dfa0bc72cc42188c60972cf71de4a`.
- Media: [JPEG](https://d3lqz0a4bldqgf.cloudfront.net/drops/author_ebb895e0-78fd-41ef-b2eb-f397454deca5/dd518de3-fca4-469d-aba3-3cefbeb2908b/01-Residual-Barrier.jpg); source MIME `image/jpeg`.
- Artist statement: a former Berlin wall no longer blocks movement but continues to shape memory and behavior. Graffiti turns a structure of state separation into an informal archive; restored access remains non-neutral. Technical representation: Berlin, 2011; Nikon D60, 55 mm, f/6.3, 1/160; Photoshop contrast/sharpness and removal of a small building.
- Rights/consent representation: the creator states that the underlying work is released under CC0 and waives copyright and related rights. No people or consent issue is represented in the caption. The wording should still be confirmed as an executed CC0 instrument rather than treated as an accession document.
- Current status: `WINNER=verified`; mint/contract/token ID `not verified`; acquisition `not verified`; custody `not verified`; accession `not verified`.

### 6. GIANT — “The Hostile Gate”

- Wave serial `1157117`; drop `73ecf8fc-9bde-492d-a624-39d0dd547587`; [canonical drop](https://6529.io/waves/4ff022b3-aa17-4a0a-ba78-58f64ff1d427?drop=73ecf8fc-9bde-492d-a624-39d0dd547587).
- Created `2026-07-02T16:32:22.759Z`; decision `2026-07-09T12:00:00Z`; place 6; rating `10,805,417`; raters `35`.
- Statement SHA-256: `9c41a16040a3af990fcd4685ee7c6f735fb486201ed0d83bc9f94e7fbb86d693`.
- Media: [JPEG](https://d3lqz0a4bldqgf.cloudfront.net/drops/author_cd69e4ba-0cb4-41a4-8013-09a695d9d84e/1a5575fc-6718-4100-af33-1f2919edf22e/Giant.jpg); source MIME `image/jpeg`.
- Artist statement: a refrigerator door becomes a hostile gate in a meditation on caloric deficit, bodily custody, hunger, and survival. The work anchors the GIANT project. Technical representation: 2020-04-16, Mykolaiv, Ukraine; Sony ILCE-6000, 16–80 mm at 16 mm; Photoshop processing; artist says the depicted person is himself and the image is photographic, not AI or composite.
- Rights/consent representation: conditional CC0 declaration and full-rights representation. The depicted person is represented as the artist himself; written consent documentation is said to exist and be available on request.
- Current status: `WINNER=verified`; mint/contract/token ID `not verified`; acquisition `not verified`; custody `not verified`; accession `not verified`.

### 7. priyanka — “the cost of open”

- Wave serial `1147422`; drop `f24313f0-b335-4c16-9052-3a689f82f188`; [canonical drop](https://6529.io/waves/4ff022b3-aa17-4a0a-ba78-58f64ff1d427?drop=f24313f0-b335-4c16-9052-3a689f82f188).
- Created `2026-06-29T18:54:05.692Z`; decision `2026-07-09T12:00:00Z`; place 7; rating `10,724,554`; raters `28`.
- Statement SHA-256: `2453e5abd616ecea4d290f39b7baaf51d1f531a817473263a9437d067c458b0c`.
- Media: [JPEG](https://d3lqz0a4bldqgf.cloudfront.net/drops/author_0f831424-87b4-11ee-9d82-029a0e4b6159/8f259b68-2488-4bb0-add8-ec1b8e36e021/29-09-24-12-26-17.jpg); source MIME `image/jpeg`.
- Artist statement: the closing of Moraine Lake’s road to private vehicles and its replacement by reservations and timed shuttles make visible the tradeoff between environmental protection and mediated access. Technical representation: Moraine Lake, Canada, 2024; Nikon D850; f/8, ISO 400, 1/400; 10080 × 5670 px; Lightroom processing.
- Rights/consent representation: conditional CC0 and full-rights declaration. No people are identified in the statement and no separate consent representation is present.
- Current status: `WINNER=verified`; mint/contract/token ID `not verified`; acquisition `not verified`; custody `not verified`; accession `not verified`.

### 8. Rakesh — “Dichotomy.”

- Wave serial `973173`; drop `aa257b16-4309-48b6-9033-1e3d7fb9016d`; [canonical drop](https://6529.io/waves/4ff022b3-aa17-4a0a-ba78-58f64ff1d427?drop=aa257b16-4309-48b6-9033-1e3d7fb9016d).
- Created `2026-05-10T06:44:03.175Z`; decision `2026-07-09T12:00:00Z`; place 8; rating `9,845,249`; raters `59`.
- Statement SHA-256: `8c43b3ca228e34987ffc46b0b825058c49d227826173c8f9ef29fd4ad69f22b7`.
- Media: [JPEG](https://d3lqz0a4bldqgf.cloudfront.net/drops/author_771ecd1d-4149-4fa9-b589-aff9980e52dd/f41827d1-d0f7-49c3-aab3-92d55d811c87/DJI-0152-copy-2.JPG); source MIME `image/jpeg`.
- Artist statement: an aerial line separates ordered, contained palms within a jail facility from an apparently free residential neighborhood. The work asks whether custody looks like garden/order and whether freedom can look like chaos. Technical representation: Rajahmundry, India, 2017; DJI Mavic Pro drone, 26 mm, f/2.2, ISO 100, 1/120; Photoshop; 2952 × 3888 px.
- Rights/consent representation: conditional CC0 and full-rights declaration. No person or consent representation appears in the submission text; verify that no identifiable people or third-party rights are material.
- Current status: `WINNER=verified`; mint/contract/token ID `not verified`; acquisition `not verified`; custody `not verified`; accession `not verified`.

### 9. pandelic — “Now Is Our Time”

- Wave serial `1029013`; drop `a9e1af00-7ac7-4b7d-a39e-31c7a662ee28`; [canonical drop](https://6529.io/waves/4ff022b3-aa17-4a0a-ba78-58f64ff1d427?drop=a9e1af00-7ac7-4b7d-a39e-31c7a662ee28).
- Created `2026-05-25T17:22:35.108Z`; decision `2026-07-09T12:00:00Z`; place 9; rating `9,689,643`; raters `32`.
- Statement SHA-256: `7db473bf65d0bbd631312deeb4fb8831502b777f512378f32d227ea4ed839d08`.
- Media: [PNG](https://d3lqz0a4bldqgf.cloudfront.net/drops/author_165094eb-552c-4116-a201-2a7d5d94c5f0/9135e87b-47fa-4380-acae-4d52c664032d/4b-now-is-our-time.png); source MIME `image/png`.
- Artist statement: graffiti reading “NOW IS OUR TIME” documents Berlin’s RAW-Gelände autonomous-cultural period before later commercialization and displacement. The image is framed as a document of survival and repair. Technical representation: photographed by Eric Pan on 2011-07-01; Nikon D70, 35 mm f/1.8, 1/1000, f/2.2, ISO 200; 3008 × 2000 px.
- Rights/consent representation: conditional CC0 and full-rights declaration. No people or separate consent issue is represented in the text.
- Current status: `WINNER=verified`; mint/contract/token ID `not verified`; acquisition `not verified`; custody `not verified`; accession `not verified`.

### 10. Minalisa — “Checkpoint”

- Wave serial `1066664`; drop `d68542bc-f05e-4f23-ae8b-fac730cd4b7b`; [canonical drop](https://6529.io/waves/4ff022b3-aa17-4a0a-ba78-58f64ff1d427?drop=d68542bc-f05e-4f23-ae8b-fac730cd4b7b).
- Created `2026-06-07T16:02:07.479Z`; decision `2026-07-09T12:00:00Z`; place 10; rating `9,499,454`; raters `43`.
- Statement SHA-256: `534912e35abb0530aa8d26d6b73575cbc9f2c29fd2a218762551b418c7041adb`.
- Media: [JPEG](https://d3lqz0a4bldqgf.cloudfront.net/drops/author_32085850-1538-4837-b7ac-1d8d1f605fea/c58bd3f6-bda4-4ec0-8c4b-ec87e78fc108/DSCF9688-Edit-Edit.jpg); source MIME `image/jpeg`.
- Artist statement: the artist describes a woman’s body as a checkpoint formed by clothing rules, movement restrictions, law, and the gaze of others. Location is withheld. Technical representation: Fujifilm X-T4, 16 mm, f/2.8, 1/200, ISO 320; 4160 × 6240; Lightroom and Photoshop clone-stamp retouching; no composite or generative elements.
- Rights/consent representation: the artist confirms full rights over the work and all persons depicted, gives informed consent for CC0 and permanent accession, and says written consent documentation is available. The withheld location and potentially sensitive subject matter require a restricted registrar annex and privacy review.
- Current status: `WINNER=verified`; mint/contract/token ID `not verified`; acquisition `not verified`; custody `not verified`; accession `not verified`.

### 11. HugoFaz — “Sina Beizavi in Brazil”

- Wave serial `1167034`; drop `52b6f536-3ebc-4bf5-b7da-2ed775df7ad3`; [canonical drop](https://6529.io/waves/4ff022b3-aa17-4a0a-ba78-58f64ff1d427?drop=52b6f536-3ebc-4bf5-b7da-2ed775df7ad3).
- Created `2026-07-06T00:02:34.236Z`; decision `2026-07-09T12:00:00Z`; place 11; rating `9,489,775`; raters `32`.
- Statement SHA-256: `091bdabc3d668c143272ba9e275671191a95d90e78b1e4929291405691b6be14`.
- Media: [JPEG](https://d3lqz0a4bldqgf.cloudfront.net/drops/author_0f82f62c-87b4-11ee-9d82-029a0e4b6159/4f55ccbe-d546-4f96-ad45-da5acca4291e/Sina-Beizavi-in-Brazil.jpeg); source MIME `image/jpeg`.
- Artist statement: Sina Beizavi, described as a queer artist who escaped Iran and now works at Casa NUA in Brazil, is shown resting with an Iranian passport. The artist frames the portrait around migration, sanctions, sexual identity, expression, and welcome. Technical representation: digital photograph directed, shot, and color-graded by Hugo Faz; Casa NUA, São Paulo, 2026-07-05.
- Rights/consent representation: Hugo states full rights and formal written consent from the depicted person for CC0 and permanent accession, with documentation available on request. Because the caption carries sensitive identity, migration, sexuality, and political information, do not publish more biographical detail than the subject has authorized.
- Current status: `WINNER=verified`; mint/contract/token ID `not verified`; acquisition `not verified`; custody `not verified`; accession `not verified`.

### 12. Teyhu — “Rusted”

- Wave serial `1002997`; drop `7d3a31f8-41bf-4fc5-8756-ed67eccdcc96`; [canonical drop](https://6529.io/waves/4ff022b3-aa17-4a0a-ba78-58f64ff1d427?drop=7d3a31f8-41bf-4fc5-8756-ed67eccdcc96).
- Created `2026-05-18T13:09:55.597Z`; decision `2026-07-09T12:00:00Z`; place 12; rating `9,154,040`; raters `23`.
- Statement SHA-256: `41125d71170e32dd2a0ab778710d3f89b4892eb54e32971c3c6796abe38c570c`.
- Media: [JPEG](https://d3lqz0a4bldqgf.cloudfront.net/drops/author_ad2d400c-d758-4877-bea9-dd14c2b8cc33/d0b5bd70-457a-4d2e-9842-f840907ca31d/IMG-0551.jpg); source MIME `image/jpeg`.
- Artist statement: a ruined interior, layered openings, and a solitary figure holding keys evoke control, approval, exhaustion, refusal, and the courage to leave in Iran. Technical representation: Canon 7D Mark II, 24–105 L at 58 mm, f/4.5, ISO 640, 1/160; subtle Photoshop color/light adjustment; no compositing or AI.
- Rights/consent representation: the text says the work is released under CC0 and identifies the image as a self-portrait with consent documentation available on request. Confirm exact CC0 instrument and self-portrait identity in the registrar file.
- Current status: `WINNER=verified`; mint/contract/token ID `not verified`; acquisition `not verified`; custody `not verified`; accession `not verified`.

### 13. arsonic — “Nowhere To Esc.”

- Wave serial `1004919`; drop `51982d19-395a-4eaa-866c-8e89aa952cbb`; [canonical drop](https://6529.io/waves/4ff022b3-aa17-4a0a-ba78-58f64ff1d427?drop=51982d19-395a-4eaa-866c-8e89aa952cbb).
- Created `2026-05-18T21:45:41.747Z`; decision `2026-07-09T12:00:00Z`; place 13; rating `9,139,810`; raters `44`.
- Statement SHA-256: `941dabeb63fbcac5279dd767469aa084c39d6241f174d19b472f074c655f433b`.
- Media: [JPEG](https://d3lqz0a4bldqgf.cloudfront.net/drops/author_0f82dd26-87b4-11ee-9d82-029a0e4b6159/388fe01c-8dd9-4693-8f61-f6c5026902b3/nowhere-to-escape.jpg); source MIME `image/jpeg`.
- Artist statement: an ant trapped inside an Esc key turns a visible exit into a nonfunctional choice; the work translates digital interface language into a physical image of blocked agency. Technical representation: iPhone 17 Pro Max, Lightroom/Photoshop, Montréal, 2026-05-18.
- Rights/consent representation: conditional CC0 and full-rights declaration, with a humorous statement of “full consent from the ant.” No human consent issue is stated; the ant cannot provide legal consent, so the registrar should treat this as a non-human-subject representation and verify photographer rights and welfare statement rather than treating the wording as a model release.
- Current status: `WINNER=verified`; mint/contract/token ID `not verified`; acquisition `not verified`; custody `not verified`; accession `not verified`.

### 14. Zoku — “Morning Glory”

- Wave serial `991838`; drop `dc75fe32-f3c2-49db-9069-d9975b5964f3`; [canonical drop](https://6529.io/waves/4ff022b3-aa17-4a0a-ba78-58f64ff1d427?drop=dc75fe32-f3c2-49db-9069-d9975b5964f3).
- Created `2026-05-15T01:10:20.171Z`; decision `2026-07-09T12:00:00Z`; place 14; rating `9,130,092`; raters `33`.
- Statement SHA-256: `011d39808b3920d8056c607a0ee7705f4fb05e181c1cda44e87bcb5ff284f719`.
- Media: [PNG](https://d3lqz0a4bldqgf.cloudfront.net/drops/author_90bb8b3b-8780-47d6-b7cd-714139a36946/7696d476-1114-4f6a-9508-29b4a36b430a/Morning-Glory.png); source MIME `image/png`.
- Artist statement: the San Roque Dam spillway in Córdoba, Argentina, automatically regulates pressure without manual gates; the work reads this pre-internet infrastructure as permissionless design. Technical representation: captured 2026-05-12 with a Xiaomi smartphone; f/2.2, ISO 100, 1/6 s; Lightroom from RAW with minimal tonal adjustment and crop; 2670 × 1878 px.
- Rights/consent representation: CC0 if selected for acquisition. No people or separate consent issue is represented. Confirm final CC0 release after acquisition.
- Current status: `WINNER=verified`; mint/contract/token ID `not verified`; acquisition `not verified`; custody `not verified`; accession `not verified`.

### 15. shamspranto — “মুক্তিযুদ্ধ - Fight for Freedom”

- Wave serial `993675`; drop `8ac2b1b8-64f9-48ef-b41b-04ee3a9ba3ab`; [canonical drop](https://6529.io/waves/4ff022b3-aa17-4a0a-ba78-58f64ff1d427?drop=8ac2b1b8-64f9-48ef-b41b-04ee3a9ba3ab).
- Created `2026-05-15T15:37:47.110Z`; decision `2026-07-09T12:00:00Z`; place 15; rating `9,130,087`; raters `18`.
- Statement SHA-256: `2200f9952e8cd55ce105129eade6d8c818b70b276df73cb57854f12a9a6488d0`.
- Media: [PNG](https://d3lqz0a4bldqgf.cloudfront.net/drops/author_835d219b-4697-490a-ab98-b77f30b2d008/813e64dc-d483-46cf-bd97-370dabc00225/Muktijudhdho-copy.png); source MIME `image/png`.
- Artist statement: two women at train windows become a threshold between visibility and invisibility; the train is civic machinery, while the torn Bengali Liberation War poster recalls freedom as a daily claim. Technical representation: Dhaka, Bangladesh, 2020; Nikon D7200 and 50 mm; Photoshop collage.
- Rights/consent representation: the artist says written consent suitable for the release exists for the people depicted, identifies one as the artist’s mother, and declares the original work may be released under CC0. Obtain and protect the consent document before public display.
- Current status: `WINNER=verified`; mint/contract/token ID `not verified`; acquisition `not verified`; custody `not verified`; accession `not verified`.

### 16. Veerendra — “No Access”

- Wave serial `1058703`; drop `13407a59-3b86-4a04-b68e-87e818ed3766`; [canonical drop](https://6529.io/waves/4ff022b3-aa17-4a0a-ba78-58f64ff1d427?drop=13407a59-3b86-4a04-b68e-87e818ed3766).
- Created `2026-06-04T13:35:00.264Z`; decision `2026-07-09T12:00:00Z`; place 16; rating `9,129,940`; raters `32`.
- Statement SHA-256: `957b974fa7427a53520007861edfdb84b8dd0fe3cf70100b56f11cfe6c701dfe`.
- Media: [JPEG](https://d3lqz0a4bldqgf.cloudfront.net/drops/author_d5cd331a-02e5-4912-a5bd-7b39769462bc/8a4ee715-af90-48c6-a0d5-0041458a7be2/selectiongj1.jpg); source MIME `image/jpeg`.
- Artist statement: a miniature house under an open night sky is surrounded by signals of restriction; the gate and warning turn calm distance into controlled access. Technical representation: handmade miniatures and focus stacking; Nikon D750; Tamron 17–35 mm at 24 mm; 30 s, f/3.2, ISO 6400; Photoshop.
- Rights/consent representation: conditional CC0 and full-rights declaration. No people or separate consent issue is represented. The handmade miniature introduces a provenance/title question for the physical set and any third-party materials used in the photograph.
- Current status: `WINNER=verified`; mint/contract/token ID `not verified`; acquisition `not verified`; custody `not verified`; accession `not verified`.

## 5. Current status and follow-up evidence

### Live selected-work status

The direct winner responses observed at the research timestamp share the following status:

| Field | Current evidence | Registrar interpretation |
|---|---|---|
| Selection | `drop_type=WINNER`; `winning_context.place=1..16`; manual award description names Museum acquisition | Selection outcome only. |
| Vote evidence | `rating`, `realtime_rating`, `rating_prediction`, and `raters_count` are live API fields; the table above records rating and raters | Ranking evidence, not a curatorial statement and not proof of quality or accession. |
| Sale/acquisition | `winning_context.sale_time=null`; `sale_price=null`; no purchase transaction in the drop response | Acquisition not verified. |
| Mint | No contract address, token ID, mint transaction, or NFT link appears in the sixteen direct winner records | Mint not verified. |
| Museum custody | Current `networkmuseum.6529.eth` Safe NFT enumeration contains seven Casey Reas objects and one unrelated ERC-1155; no matching K&G token | No K&G custody evidence found as of observation; negative indexer result only. |
| Accession | No accession number, title-binding, executed CC0 instrument, consent file, condition report, preservation package, or second-person accession review is present in these sources | Not accessioned. |

The direct winner source therefore supports the durable statement: **sixteen works were selected by the K&G Wave, but no selected work has a verified Museum accession in this evidence set.**

### Follow-up and implementation context

These items are not formal amendments to the program rules, but they materially affect the registrar queue:

- Serial `1185780`, drop `ecc1d172-a4cc-4b8c-bf44-254f62b3060e`, [K&G drop](https://6529.io/waves/4ff022b3-aa17-4a0a-ba78-58f64ff1d427?drop=ecc1d172-a4cc-4b8c-bf44-254f62b3060e), `2026-07-09T21:10:03.195Z`, @punk6529: “Hopefully soon I will have the contract ready on which to mint them.” This is post-selection implementation context and gives no contract address.
- Serial `1187378`, drop `b90acff7-a0fa-4ae4-a38e-2c16d9443a99`, [K&G drop](https://6529.io/waves/4ff022b3-aa17-4a0a-ba78-58f64ff1d427?drop=b90acff7-a0fa-4ae4-a38e-2c16d9443a99), `2026-07-10T11:08:13.299Z`, @ikertje: a related wave was collecting minted/on-sale submissions that did not make the top sixteen. This is not an accession register and must not be confused with the selected works.
- Serial `1191021`, drop `283f328f-590d-4d80-8582-b0cfb96cb673`, [K&G drop](https://6529.io/waves/4ff022b3-aa17-4a0a-ba78-58f64ff1d427?drop=283f328f-590d-4d80-8582-b0cfb96cb673), `2026-07-11T07:42:48.343Z`, @ikertje: invited minted submissions to the related grouping wave. Again, minting a submission independently is not Museum acquisition.
- Serial `1243947`, drop `6177e578-a827-4f2b-a720-ba5dc26fa3fd`, [K&G drop](https://6529.io/waves/4ff022b3-aa17-4a0a-ba78-58f64ff1d427?drop=6177e578-a827-4f2b-a720-ba5dc26fa3fd), `2026-07-26T21:05:24.479Z`, @punk6529: a detailed Stream contract feedback mechanism was described as the main blocker for Stream and Museum/Keys and Gates. This establishes implementation dependency, not accession.
- Serial `1244144`, drop `75cfb5f2-3a67-4492-9828-f490201a2fc7`, [K&G drop](https://6529.io/waves/4ff022b3-aa17-4a0a-ba78-58f64ff1d427?drop=75cfb5f2-3a67-4492-9828-f490201a2fc7), `2026-07-27T00:43:39.890Z`, @HugoFaz: planned exhibition at Casa NUA / Dominio PubliCC0 of the sixteen winning pieces, with minted CC0 runner-ups potentially added. Planned display is not custody or accession.
- Serial `1249571`, drop `d753dabd-4d16-406a-8812-a79a84b8edbd`, [K&G drop](https://6529.io/waves/4ff022b3-aa17-4a0a-ba78-58f64ff1d427?drop=d753dabd-4d16-406a-8812-a79a84b8edbd), `2026-07-28T15:52:55.016Z`, @EstebanAmaro: a non-winning Water Portals submission reported 9/10 editions minted. This is useful evidence that independent submission minting was occurring, but it is not evidence that any K&G winner was minted or acquired.
- Serial `1257158`, drop `93e5923c-57d7-48e2-8e43-e0a216bf9b43`, [K&G drop](https://6529.io/waves/4ff022b3-aa17-4a0a-ba78-58f64ff1d427?drop=93e5923c-57d7-48e2-8e43-e0a216bf9b43), `2026-07-30T16:50:21.845Z`, @EstebanAmaro: the same non-winning submission reported sold out. Do not use this as a purchase/acquisition record for the Museum.
- Serial `1259672`, drop `d751d212-1309-4826-b63b-6c0a2d141d64`, [K&G drop](https://6529.io/waves/4ff022b3-aa17-4a0a-ba78-58f64ff1d427?drop=d751d212-1309-4826-b63b-6c0a2d141d64), `2026-07-31T16:13:50.422Z`, @ikertje: “soon the pieces will be minted, punk finished the new contract.” This is the latest located implementation update and is not a contract deployment, mint event, custody event, or accession decision.

### Required registrar follow-up before any accession claim

1. Identify the actual K&G mint contract and record its deployment transaction, verified source, chain ID, token standard, token IDs, artist minter/recipient, metadata URI, and content fixity.
2. For each winner, bind the artist’s executed CC0 release and any model/property/third-party consent to the specific token and transfer; do not rely solely on the Wave caption.
3. Record the purchase/acquisition instrument, price, payment transaction, title passage, prior owner, and Museum receiving address separately.
4. Verify the transfer into Museum custody independently at the chain level and record block, transaction, log/index, and Safe address.
5. Apply the Museum accession gates: mission/collection fit, authenticity, provenance, title, rights, sanctions/legal, technical receivability, condition, preservation, display, curatorial statement, and second-person review.
6. Assign stable Museum accession/object identifiers only after the specific accession act is complete. A program outcome record may remain `selected` or `acquisition_pending` without entering the accession register.
7. Preserve the exact artist submissions, media files, metadata, consent instruments, and hashes in a durable dossier. CloudFront media URLs alone are not preservation.

## 6. Uncertainty and source-quality register

- The direct API `title` property is empty for the selected records. Titles in this document are first-heading transcriptions, not silently promoted API fields.
- Artist handles are platform identifiers, not verified legal identities. Legal-name claims appearing in statements need a restricted identity/rights record before accession.
- The text representations of CC0 and consent are artist-submitted declarations. They are not yet executed legal instruments, and several are conditional on selection and purchase.
- Consent coverage is incomplete or ambiguous for potentially depicted people in `the Artist in teh Open Sea`, `Managed Freedom`, and any other work where the image, rather than the text, must be inspected. Sensitive subjects in `No Key, Only Light`, `Checkpoint`, and `Sina Beizavi in Brazil` require heightened privacy review.
- The K&G description says the first mint is expected through a common Museum contract, but the current evidence does not identify that contract or show its deployment. A later chat statement that the contract is finished is not a chain fact.
- The direct winner responses contain no mint, contract, token, sale, or custody facts. Their manual award description uses the word “Acquisition” as an outcome label, but it cannot override missing chain and registrar evidence.
- The Museum Safe negative NFT enumeration is useful current evidence but depends on the Blockscout indexer and the query’s indexed state. It must be repeated against the chain and after the K&G mint transaction is known.
- The selected score/rater values are mutable API observations. They are preserved with observation time and should not be treated as timeless rankings.
- No OpenSea rarity metric was used. Keys and Gates is a photography program, and selection evidence is the program Wave’s voting data; no rarity calculation is relevant to these 1/1 photographs.

## 7. Durable conclusion

As of the live research pass on 2026-08-01, the evidence supports a sixteen-work **selection outcome** for `6529NM-AP-01`, not a completed sixteen-work accession. The program rules, Wave identifiers, winning drop identifiers, timestamps, voting evidence, media URLs, artist statement hashes, and artist CC0/consent representations are now inventoried. The next authoritative state change must be evidenced by the actual common-contract deployment and per-work mint/acquisition/custody records, followed by the Museum’s formal accession documents.
