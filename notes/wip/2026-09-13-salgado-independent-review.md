# Independent advisory review: Salgado six-work accession package

**Reviewer:** Codex independent subagent `/root/salgado_independent_review`,
distinct from constructor `codex-task:01a087a1-5e64-7280-b5f8-82d0df4ec066`.
This identifies an AI reviewer; it is not a human, external scholar,
cryptographic signature or GitHub approval.

**Requested effort:** Ultra, as authorized by punk6529. Review combined all
six images, scholarship and sources, typed-record comparison, and independent
raw-evidence checks. A read-only source spotcheck was delegated to
`/root/salgado_independent_review/source_spotcheck`; this reviewer assessed
and incorporates that agent's findings below.

**Source state:** branch `codex/salgado-accession`; HEAD and local `origin/main`
both `3926d78faacf67a62b8d9b48e15d26c43b52eae9`. The accession package is
uncommitted construction on that base. This is a file-bound review, not approval
of the eventual PR head. Instructions were read from this checkout; the main
task owns live remote and protected-PR checks.

**Scope:** Every public text for lot `6529NM.2026.004`, six object records,
six rights statements, six condition reports, gift authorization, accession lot,
Wave observation and resolution; supporting source, contract, authority,
custody, provenance and Wave evidence; `tests/test_salgado_accession.py`.
Exact tokens: 226, 1117, 2059, 2216, 2768 and 4697 in Ethereum contract
`0xf1f036cebb4b64f138e4f57754edbceb64fb80fc`. This is not a security audit of
executable ingest or an independent live RPC recapture.

## First-review determination

**Advisory result: CONDITIONAL PASS for the catalogue and evidence package,
subject to the corrections below. Formal accession/admission: NOT PASSED /
not attempted.** No critical visual, token-identity, transfer-log or source-hash
mismatch was found. The objects remain `received_onchain`; the lot remains
`not_complete`; all 21 typed records retain null reviewers and pending review.
No certificate, register admission, production publication or qualifying human
review is asserted by this artifact.

## Findings and requested dispositions

1. **P2 — Source-characterization evidence class.** Typed evidence references
   label “Source JPEG and metadata characterization” as class A.
   `docs/record-model.md` defines A as directly chain-verifiable, while C covers
   Museum checksum and condition work. Change this Museum-generated off-chain
   characterization reference to C throughout builder/output; preserve B for
   issuer statements and A for Ethereum observations. This affects authority
   typing, not the verified bytes.
2. **P3 — Hostetler attribution.** The artist study attributes neighbouring-image
   and “accompanying texts” relationships to Hostetler. The
   [ICP reproduction of her 1999 account](https://www.icp.org/content/2022)
   supports serial presentation and keeping subject with context; accompanying
   texts is an added Museum inference. Tighten the attribution or separate it.
3. **P3 — Exact UNIVAJA version.** The source register links the current
   main-domain Marubo page, while object .04 correctly cites the
   [2024 version](https://site2024.univaja.org/marubo/), which includes the
   Maronal/Curuçá village list. Align the register with that supporting version.
4. **P3 — Publication apparatus.** Several texts lack their own research cutoff,
   revision history, linked selected bibliography/source register, stable
   source/citation route or eventual immutable edition link required by
   editorial-standard section 13. Add concise edition metadata and cross-links.
   An immutable published edition must bind to the finalized reviewed commit;
   do not fabricate one during construction.
5. **P2 — Accession completion inventory.** The accession standard includes
   title, authority, encumbrance and sanctions diligence. The first package
   documents donor instruction, custody, contract authority and token provenance,
   but no distinct encumbrance/sanctions determination was found. Complete that
   existing requirement with exact scope/evidence, or list it among remaining
   gates before certificate execution. This requests no additional donor
   rights questionnaire and makes no adverse inference about the gift.
6. **P3 — Stale archive status.** README and the construction ledger still
   describe archive approval as pending. The main task reports that explicit
   approval has now been supplied. Update after the upload/restore outcome is
   evidenced; an in-flight operation is not preservation completion.

The constructor was notified promptly and is correcting these items. Any
changed-file rereview will be appended with new hashes, preserving this first
review's findings and source boundary.

## Image review

All six 1280-pixel-width WebP files were opened and examined in full frame.
Five are 1280 by 853 pixels; the portrait is 1280 by 1920. All eighteen supplied
derivatives match their manifest hashes and byte counts. The source-to-derivative
hash references and token/object joins agree with the source manifest. This
review did not compare every source pixel, camera original, physical print or
book plate.

| Token | Independent observation and result |
| ---: | --- |
| 226 | Dense forest, pale slender trunks, overlapping palm fronds and smaller growth, dark gaps; no visible water/reflection scene. Corrected prose and alt text pass. |
| 1117 | Shaded diagonal near ridge, long relatively level-topped cliff behind, pale forest distance to the left, clouds above; no exact peak identity inferred. Pass. |
| 2059 | Broad bright clouds, rain curtains, forest light/shadow and short river segment at left. Pass. |
| 2216 | Vertical portrait against dark background, pale ornament strands, face painting, slightly turned head and gaze toward camera. Community follows metadata; sitter remains unnamed. Pass. |
| 2768 | Repeated pale river bends across dense canopy; no sky; river name, flow direction and individual-loop status are not inferred. Pass. |
| 4697 | Foreground figure at right with broad feather headdress and upright shaped object; several people in the clearing behind. No identification as Biraci, exact procession/festival or object's function. Pass. |

The token-226 error is acknowledged as a corrected construction observation.
The earlier proposal's procession wording is expressly superseded in the object
entry and source notes. Selection and original evidence bytes remain unchanged.

## Evidence and state checks

Independent read-only calculations passed:

- 43 custody, 50 provenance and 10 contract-authority response/request pairs:
  raw-byte hashes and sizes agree with evidence references.
- 35 ERC-721 Transfer logs across 25 distinct successful receipts: contract,
  token, sender, recipient, log index, receipt block number and hash agree with
  recorded provenance. The retained canonical block map contains 25 blocks.
  This supports indexed continuity; it is not a full-range log enumeration.
- Raw finalized owner and token-approval responses use the common EIP-1898
  selector and report Museum owner/zero token approvals. This concerns recorded
  block 25971024, not indefinite future custody or all operator approvals.
- Six issuer metadata/image URI joins and eighteen derivative byte hashes/sizes.
  Retained August JPEGs are not misrepresented as fresh September downloads.
- Six object/rights/condition joins: IDs, tokens, grant maps and pending reviewers
  agree. Receipt, gift acceptance/title basis and accession are separated.
- Wave status follows retained API `WINNER`, serial 1344468 and the exact drop ID,
  observed at completion time `2026-09-13T21:32:17.6672350Z`. The earlier
  `PARTICIPATORY` observation remains. Vote totals are not the adoption test.

The four Salgado tests were read and check useful identity/state joins. A
constructor-authored test is not itself an independent reviewer. The main task
owns the complete suite, schema/manifest checks and final changed-tree rerun.

The contract discussion appropriately separates base tokens from extension
tokens 226/2216, discloses absent verified extension source, and does not infer
immutability from a zero admin slot or absence of a public upgrade entry in the
examined source. Current supply is not inferred from the reverted optional call.

## Scholarship and rights

The close descriptions support the collection's distance/attention argument.
Museum descriptive titles, issuer location/year codes, project history and
interpretation are separated. This is a Museum/donor-formed group, not an
artist-authored six-part suite. Book/exhibition claims stay at project level
without invented exact-image histories. No marketplace rarity metric is used.

The source spotcheck supports biography/death date in
[Praemium Imperiale](https://www.praemiumimperiale.org/en/laureate/salgado/),
dates/curatorship at [MAXXI](https://www.maxxi.art/en/events/sebastiao-salgado/),
announced edition size and launch in the
[Sotheby's catalogue](https://www.sothebys.com/en/digital-catalogues/sebastiao-salgado),
and project-level equipment testimony in the
[artist interview](https://www.sothebys.com/en/articles/photography-is-the-memory-of-our-society-a-conversation-with-sebastiao-salgado).
Community histories remain general and do not establish individual identities
or ornament meanings.

The summaries of [Sontag's criticism](https://www.newyorker.com/magazine/2002/12/09/looking-at-war)
and [Wiley's later position](https://www.newyorker.com/culture/photo-booth/sebastiao-salgados-view-of-humanity)
were checked directly and are supported. Neither is presented as reviewing
this six-token group.

The user's unrestricted gift and ordinary Museum exhibition, publication,
reproduction and preservation instruction are the operative task authority.
Artist/applicable-holder copyright remains separate; no general third-party,
commercial, creative-derivative or AI-training licence is asserted. The Museum
use determination is explicitly institutional, without claiming copyright
assignment or an independently obtained photographer licence. No further donor
rights answer is requested by this review.

## Remaining gates

- Correct/dispose findings, then record changed-file rereview and final validation.
- Evidence the archive recovery result. The main task reports private-cloud
  authorization and matching exact-version downloads; this first review has not
  inspected the restoration receipt. Two independently recoverable copies are
  required; no additional two-bucket rule is imposed by this review.
- Obtain a binding review from an identified nonconstructor reviewer satisfying
  the accession standard's second-person requirement. Under
  `governance/pull-request-review-policy.md`, bot comments are advisory. This
  artifact cannot be recast as qualifying human or GitHub approval.
- Execute the evidence-backed accession certificate/admission events after
  required review; integrate public entities/register, regenerate commitments
  and complete protected PR controls. General work authorization and permission
  for this subagent do not manufacture an exact-package binding review.

**Identified review record:** Codex independent subagent
`/root/salgado_independent_review`. No construction files, cloud storage,
on-chain state or public service were modified by this reviewer. The main task
will link this artifact in INDEX and the handoff ledger.

## Exact first-review snapshot

The findings above were reported from the initial reads. The constructor was
working concurrently and began corrections before this snapshot was assembled;
in particular, the source-characterization reference in object .01 was observed
as class C after snapshot assembly. These hashes bind the files at the stated
snapshot time, not an invented pre-correction commit. Full changed-file
verification and dispositions will be appended separately.

**Snapshot time:** `2026-09-13T22:14:43.799640+00:00`  
**Reviewed-subset digest:** `sha256:15c857f42cebaf3246bb3fa706f4071286c9a7b8ab136422b99c02afca1aafb8`  
**Inventory:** 64 files.

Hashes are SHA-256 of raw filesystem bytes, including current line endings, separate from LF-normalized release hashes and canonical payload commitments. The subset digest is SHA-256 over UTF-8 records `relative/path + NUL + lowercase raw SHA-256 + LF`, sorted by relative POSIX path. It is not a Git tree ID for this uncommitted package.

| File | Raw SHA-256 |
| --- | --- |
| `AGENTS.md` | `ed2733e39329933323a7f45e797c51bf2960b26bbe095dce8f2892966243ecbd` |
| `README.md` | `33fb5bbc011fe600db21e745b7b1496e90cebb4f90997e53d51e3dc79d6734f3` |
| `docs/accession-standard.md` | `78d6a1aee981aecaea0cd219002ee7b81d6e54fd9bed2fbd1f72ee42f55a6976` |
| `docs/curatorial-publication-standard.md` | `de5b4d22eca06b07cf84a5a9bcf1fcf0348a8634239ed73132102404add8e2b5` |
| `docs/record-model.md` | `8f1102a21fb92b833f7c71e3db63e1917b819b561a0cee5b272ff3a83e7d4e52` |
| `docs/stream-interoperability.md` | `b1e89dc8a0a67cd16e5473b690a37c4e407387768831db643139c98e943cad2d` |
| `evidence/salgado-amazonia-authority/summary.json` | `241e7d44d43c9bd15f8e4fd5a87bc917ec55d7d838aa4fc456e93c4b82b4d432` |
| `evidence/salgado-amazonia-contract/0x55a989449cc4330132a0b064d1a16ce9325c9452.response.json` | `0e6b1a13a022f9dd1428ab0d1eb59ee9ae9246a23970482f3abd9f91cb56d15c` |
| `evidence/salgado-amazonia-contract/0x659d80ce8ac5cad5ab2fdd7137caf3d06d246289.response.json` | `f0a59d67d19a0afb44fb5a372d1bfa18f4d10f8209c0ef8d02c386bcb8043099` |
| `evidence/salgado-amazonia-contract/0xf1f036cebb4b64f138e4f57754edbceb64fb80fc.response.json` | `9d755bcce329f7f4c11f9c8207f590c6ad046f687729ec52961ae3468d0c714f` |
| `evidence/salgado-amazonia-custody/summary.json` | `8ea329d9ce50d4ac7c87ff086be6ab93ba9e61619f9f504e57e6d94846f0d423` |
| `evidence/salgado-amazonia-metadata/manifest.json` | `cc45a767608a2ec15f746d08d445f574bd21e2ae0b0ab75f760cbd53ac65b0cf` |
| `evidence/salgado-amazonia-provenance/summary.json` | `42c491b6833adb8cace7acb07cab994b6e1b8f57af6441844afbdb1d9a82619d` |
| `evidence/salgado-amazonia-sources/manifest.json` | `03ecbf9fe61a8e066ee9730d1644550f164b908b1da65a20f36756cdcc6e9392` |
| `evidence/salgado-amazonia-sources/metadata/1117.json` | `e7c517c2e57815f077b9fecb71a8fb21878a35af861369d79216db1fe333fbeb` |
| `evidence/salgado-amazonia-sources/metadata/2059.json` | `b58d06ca924f22467eae0d5289df5751c1d42580db2d48dacc5513765d8cd648` |
| `evidence/salgado-amazonia-sources/metadata/2216.json` | `2900995d9113ca9b9b08590a3e06fa4e61b637ee796433750ec1c9f1c5e1531c` |
| `evidence/salgado-amazonia-sources/metadata/226.json` | `2768b4a20b80a44b17a7990183cb4030ee03065ccdd7714a8588e458bd25d621` |
| `evidence/salgado-amazonia-sources/metadata/2768.json` | `46e3fe21ea0921ee1b8f6aceb840a881d6970f1f60bb07f222170e2c253b21e2` |
| `evidence/salgado-amazonia-sources/metadata/4697.json` | `66ef09dfe5d8bd394e82399cdf69f1d97908c9232256d5f5feff205af26d5e7f` |
| `evidence/salgado-amazonia-wave/manifest.json` | `4ca5c6bfccc66d637d9dc63d1a557e5b96bfd0511ca02fadd8fb4b4c9011509e` |
| `evidence/salgado-amazonia-wave/original-publication.json` | `9faae6ca1f75fe33c5b3cfc372c2d54dc070ef55f06f97f616117452ecd8c778` |
| `evidence/salgado-amazonia-wave/response.json` | `7fcc5c3f88609ef3d084e64e185660dbf652949df051474d67a443826a1b4e13` |
| `governance/pull-request-review-policy.md` | `d6f69774caf1189c2fcda8f84f46ae76d04aadbcbe95bd38b7851fbc32515aca` |
| `records/accessions/6529NM.2026.004/accession-statement.json` | `e0c547b18aa15af8b7be7875d44ada889b70e53559d1779fb6e338a89f60d00a` |
| `records/accessions/6529NM.2026.004/gift-acceptance-authorization.json` | `4d520ad47c895bc3ac5d687e19830f9364bbb259118c559a009fcd9419ff44a4` |
| `records/accessions/6529NM.2026.004/objects/6529NM.2026.004.01.json` | `17425ab0d66de5cca029317269b749059b52a372d3f8f03406515be6dcb95ede` |
| `records/accessions/6529NM.2026.004/objects/6529NM.2026.004.02.json` | `53599ac29f5b6fededb8ad0d0973ee6de69622092dae9c0f77f2675f041f3b56` |
| `records/accessions/6529NM.2026.004/objects/6529NM.2026.004.03.json` | `d24672b5e1470db186e3ed7416a74c523935c4a1d7c0bbd6aabafb6944d2b6d5` |
| `records/accessions/6529NM.2026.004/objects/6529NM.2026.004.04.json` | `5c95057bff091bc1880d63d60b8591eb2315603874a5e75a9da1ce40ef1edc02` |
| `records/accessions/6529NM.2026.004/objects/6529NM.2026.004.05.json` | `6185809d1394534fa217cf7fa5427eb0df1ab958b7a8f0bbedfc90b749aa06dc` |
| `records/accessions/6529NM.2026.004/objects/6529NM.2026.004.06.json` | `3e4d9dee4bc4bab22b279bb9cc17a4cf79ec8b26067c197585b2ebe5956037de` |
| `records/accessions/6529NM.2026.004/public/6529NM.2026.004.01.md` | `674c1449b2e8bd7e7a3bbdbe98296de5541ebe292275320d697bbcfb8de9d139` |
| `records/accessions/6529NM.2026.004/public/6529NM.2026.004.02.md` | `1a622f739ff2eb0648ccc820997d3fa6e61634adac1c7d4acfbd2c7ef6ec5a07` |
| `records/accessions/6529NM.2026.004/public/6529NM.2026.004.03.md` | `6cd49a900860bf81f893e66810911b79254f2b8fd8d5ab5ce4885c42a968e899` |
| `records/accessions/6529NM.2026.004/public/6529NM.2026.004.04.md` | `9f59bfae9a27caacce6db67a827723140f402e97e29e81d0e7e060e05e9c8ba5` |
| `records/accessions/6529NM.2026.004/public/6529NM.2026.004.05.md` | `78b62abc765f6d11ac5e3f7fd3ad6ff1f285e34283f2c5fed5ff82fee8071e20` |
| `records/accessions/6529NM.2026.004/public/6529NM.2026.004.06.md` | `41eec35b47f138fe1e806fd6d6c03ccee0f3307596d63eac736827e7e5eedf46` |
| `records/accessions/6529NM.2026.004/public/README.md` | `51fce3cf1813be8f6b76fdcbe8f570892744e728e1498e442910f3ddfa76de6a` |
| `records/accessions/6529NM.2026.004/public/acquisition-narrative.md` | `9d778aab12ff67c1e376580e38993d99882e82d6c591da5f12325390d403bf51` |
| `records/accessions/6529NM.2026.004/public/amazonia-project.md` | `ec3f8ce88556dcc5ae489ddb27c017b1062653581c2dbaf74c7634b6af1bbef5` |
| `records/accessions/6529NM.2026.004/public/display-and-preservation.md` | `bbb1c5566d4ccc011659c3a4e66f1d98f073389054459bbcbb6eb68f2df7c553` |
| `records/accessions/6529NM.2026.004/public/forest-water-and-community.md` | `34e408b70b6d1ad46447910e1898e2ded20581b32340979329d17a5903494bb9` |
| `records/accessions/6529NM.2026.004/public/sebastiao-salgado.md` | `2990f3b17c3adefd00cb39cfe3c96c4a380607799799eb55f30a098631eb656c` |
| `records/accessions/6529NM.2026.004/public/source-and-chronology.md` | `b4e7a97bf23595b4bc07405ef5761f793f3bff919bdcc92a71086682f8172217` |
| `records/accessions/6529NM.2026.004/public/technical-and-condition-review.md` | `e45801a3271a7a420c605f4f9bd646c76e7b61d966743dc61fe935522da3e121` |
| `records/accessions/6529NM.2026.004/public/title-rights-and-display.md` | `69106efb6c559e941fd79815f854fd27c540599d904c91eb2bd8e2c27b49b3b5` |
| `records/accessions/6529NM.2026.004/rights/6529NM.2026.004.RIGHTS.01.json` | `73e90c6bfe2a4d8cc50b27b7976332400bbf1a212c0b7721b555e8096b65ae0e` |
| `records/accessions/6529NM.2026.004/rights/6529NM.2026.004.RIGHTS.02.json` | `0d396af493632882cc17d436faf9b858c0d1b93e38e1a353c8be19a6d69729a1` |
| `records/accessions/6529NM.2026.004/rights/6529NM.2026.004.RIGHTS.03.json` | `19c6d2a565bda27f500058130966fe0cf25f237a9ff1ed52de0322745a5f68f0` |
| `records/accessions/6529NM.2026.004/rights/6529NM.2026.004.RIGHTS.04.json` | `932651313b723e68a10db0e9881cfc177f7b6459c1397f6f32bd4f869c5b0d84` |
| `records/accessions/6529NM.2026.004/rights/6529NM.2026.004.RIGHTS.05.json` | `a1b7879e90b1bce9a04d3bef3b055f4a7da78f227c5dcfe5f3dda7405870cb84` |
| `records/accessions/6529NM.2026.004/rights/6529NM.2026.004.RIGHTS.06.json` | `ebea67c4160308cac7fa4b30c34d15c2c213bd8d228db7a4c0eabe3e50f1ff6a` |
| `records/accessions/6529NM.2026.004/technical/6529NM.2026.004.01.json` | `ba276349779eb3088cbb8dea87ff73a1ee5cd3e40a609b2e384dd9fa9af125fb` |
| `records/accessions/6529NM.2026.004/technical/6529NM.2026.004.02.json` | `8d25784b113437dce9e6ad658dbb95ff65c74319384e0e6f61482d541888299c` |
| `records/accessions/6529NM.2026.004/technical/6529NM.2026.004.03.json` | `186c3b83d38193550f778f21b8e55defd7078db515db48521cd44b72c2884a7a` |
| `records/accessions/6529NM.2026.004/technical/6529NM.2026.004.04.json` | `09d427c6bec5b0aaa4e5af31655466810fac6a090749540ba25700b718ce660d` |
| `records/accessions/6529NM.2026.004/technical/6529NM.2026.004.05.json` | `477b8c30d3f18328b6c27243b1a211c7170312b9fb3831bbdc5178e19335f907` |
| `records/accessions/6529NM.2026.004/technical/6529NM.2026.004.06.json` | `f3ac9e4974fa32e1487adb25ff8017abd57e931783ae7b4278e2e73de8b73a2a` |
| `records/proposed-gifts/6529NM-PG-2026-003/public/wave-resolution.md` | `f8313636375109aecf3bad66062beae59fac7223b9b60d8c0d87ee87d95b4f0a` |
| `records/proposed-gifts/6529NM-PG-2026-003/wave-status-observation.json` | `74a8b9d41ae8e3b51d19d992c29d233a36d1be9bac8e1039dc054443ed830ab2` |
| `scripts/build_salgado_accession_package.py` | `3306a8e3ea0f0f63c7e2e9480589911a3b22e2365c17d05da160252c51e52b93` |
| `scripts/validate.py` | `ae698bbd1068a965ec5748422a7e715a1bfec3cfc69e236c865e6190ae03d41a` |
| `tests/test_salgado_accession.py` | `9490500682943eca9a3311c308bddfb71fa21651ddc7d8b3f7c859c33f9f2d5c` |

### Offline review images

| File | Raw SHA-256 |
| --- | --- |
| `media-manifest.json` | `29fc862a8764c7648fba1aff344e99f13020cdb734706bdfd72cd969148587ea` |
| `index.html` | `bc43ae1c991ce00572a35fb516c0d3ef8a434506bce3b7e62a3e0414cd24a0fe` |
| `226-1280.webp` | `be435f7a85ae533547226127d580c5f87a6db3bceef952413a317a4c1b8df721` |
| `1117-1280.webp` | `13b2db44ef3c098ab9a7b21e9d05675c9eb3535a1185b3c5ef60a0675342ed2d` |
| `2059-1280.webp` | `3e167ca316d11466266b6b8a65d12d03b9dbff9cdfbded3f5a66b5e9ae47d8fb` |
| `2216-1280.webp` | `581cf037268851c2e6188a671a3819ee4903abba872e7a534d8b769356f39982` |
| `2768-1280.webp` | `3f380c486db86789508d26ec3fdbac8f01d8e81814698b52b765ca1e7a6619cb` |
| `4697-1280.webp` | `53f394065270638984a9f81575e9942846b5cf20282a018bbb446845e7b72479` |


## Binding independent AI review addendum

**Decision:** PASS. The substantive findings from the first review are resolved.
This is a binding, file/hash-bound independent AI record review of the exact
construction inventory below under punk6529's explicit appointment of this
separate Ultra agent as the accession reviewer. It is not human review or a
GitHub approval. No constructor files were changed by this reviewer.

**Reviewer and review identifier:** Codex independent subagent
`/root/salgado_independent_review`; `6529NM.2026.004.REVIEW-AI-20260913-01`.
**Schema-compatible reviewer ID:** `codex-reviewer:salgado-2026-09-13-independent`.
This ID denotes the same independent AI agent identified by the canonical task
path above; it does not denote the constructor, a human or another institution.
The reviewer is separate from the constructing parent agent. This identified
review statement is not a wallet, cryptographic or handwritten signature.

### Authority clarification and supersession

This addendum supersedes the first review's interpretation that another human
review was necessarily required. The PR policy requires an identified
nonconstructor binding reviewer and treats PR bot comments as advisory; the
accession standard refers to a second person. The user specifically appointed
a separate Ultra AI agent for this accession review. That explicit task
instruction controls the local-standard interpretation for this scope. The
reviewer is openly identified as AI, and this appointment is not represented
as a human meeting the literal second-person wording. It does not alter
GitHub's maintainer, Code Owner, self-review, last-push or protected-PR rules.

No additional human-review request is made solely to replace the appointed AI
reviewer. This decision supplies the independent record-review evidence for
the normal registrar/constructor admission process. Material changes outside
the reviewed facts and scope require further review; the eventual source
commit and published edition must retain their actual hashes.

### Disposition of first-review findings

| Finding | Disposition and rereview evidence |
| --- | --- |
| 1 — Source-characterization class | Resolved. Builder SREF is C; all 21 typed outputs retain the correct source class; object evidence grades include A/B/C/E. Retained reference hashes agree with their files. |
| 2 — Hostetler attribution | Resolved. The artist study now attributes serial presentation and the clearer scope of subjects; the unsupported accompanying-text attribution was removed. |
| 3 — UNIVAJA version | Resolved. Bibliographic register and object .04 agree on the exact site2024 version supporting the village list. |
| 4 — Publication apparatus | Resolved for this review edition. All ten artist/project/group/acquisition/object texts include selected bibliography, edition record, authorship, cutoff, draft date, source/citation route and revision history. The final immutable edition link is explicitly deferred until release. |
| 5 — Diligence inventory | Resolved at the documented scope. Registration diligence records the title/authority basis, scoped encumbrance assessment and official OFAC exact-address screen, with explicit limits. No adverse claim was invented or universal legal clearance asserted. |
| 6 — Archive status | Resolved. README, technical and preservation texts now state evidenced two-region source recovery and separate the later final-publication archive edition. The earlier approval-pending language is retained only in historical notes, followed by an update. |

No additional material catalogue or accession-evidence defect was found in this
bounded rereview. The public scholarly and object changes preserve the six-image
descriptions accepted in the first review; token 226 remains forest and the
foreground subject/occasion in 4697 remains unidentified.

### Independent restoration and consistency checks

The reviewer inspected restricted local replica/download receipts and both
restored ZIPs read-only. Private bucket names, keys, exact versions and access
locations are omitted here. Both version identifiers agree across the stored
replica, object-head and download receipts; reported checksums and actual
43,150,603-byte ZIPs agree with archive SHA-256
`cc8f174cab25232ea8469862183e7f47ab3dc3239e30be5ed9998fb32728fecc`.
The two receipts refer to distinct storage objects in distinct regions.

For each copy, the reviewer independently verified ZIP CRC, the package-manifest
hash and all 341 manifest members' byte lengths and SHA-256 hashes. The package
manifest hash is `2c53503d6898602957420f7a9b4bae4f9e68b6cb387086b53a797cbe56c49b39`.
All six restored source JPEG hashes and all eighteen reconstructed display-file
hashes agree with the public source/display manifests for each restored copy.
The reviewer checked the reconstruction outputs rather than independently
executing the image-transform pipeline again. The main task's restoration
record supplies the offline execution method and completed times.

Public evidence uses aliases `MUSEUM-PRESERVATION-REGION-01` and
`MUSEUM-PRESERVATION-REGION-02`; shared AWS-account administration is disclosed.
The source scope is recoverable. This archive is not represented as containing
subsequent catalogue amendments or this review addendum.

The ten screened addresses exactly join the documented donor, Museum, token
contract, implementation, contract owner, four admins and registered extension.
The official-interface observation records the CHATEX positive control,
individual times, zero exact matches for the ten addresses and displayed list
update dates. The reviewer checked the observation's scope and record joins;
no independent rerun of the live screening or retained HTTP response bytes is
claimed. The documented screening is not civil-identity, transaction-exposure,
50 Percent Rule, non-OFAC-list or general legal clearance.

All 21 typed records remain `review_pending` with null reviewer fields in this
reviewed input; all six object lifecycle states remain `received_onchain`, and
no accession certificate/admission is silently manufactured. This addendum is
the new independent review event, not evidence that those subsequent registrar
updates have already occurred. A recursive check of 165 retained evidence
references across seven distinct files found no reference-hash mismatch.

### Residual work and limits

The binding independent AI review gate is satisfied for the hashed scope.
Remaining work is the evidence-backed accession certificate and admission
updates, public register/entity integration and display publication, capture
of the final reviewed publication edition, deterministic validation/manifest
checks on the resulting final tree, and applicable protected-PR review/checks.
The main task reports nineteen targeted tests passed; its full validation run
was in progress when this rereview was requested. This report does not claim
that an unfinished validation, publication, certificate or GitHub approval
has occurred.

The absent verified source of the metadata extension, gateway/administrative
dependencies, absence of camera originals, scoped encumbrance assessment and
limits of exact-address screening remain disclosed characteristics of the
record. They are not hidden completion claims or new donor questionnaires.

### Exact binding-review inventory

**Rereview snapshot:** `2026-09-13T22:28:02.392785+00:00`  
**Binding inventory digest:** `sha256:b9f8f1e211fa3af9b80ace65ee617e6b8dfe037478d6509c9c6ea3f892ce1ebc`  
**Bound inventory:** 70 files.

The raw-byte SHA-256 and subset algorithm are the same as defined above. This inventory excludes this review file itself to avoid a self-hash cycle. A later commit identifier will identify the publication/integration tree; this decision binds the exact source bytes below.

| File | Raw SHA-256 |
| --- | --- |
| `AGENTS.md` | `ed2733e39329933323a7f45e797c51bf2960b26bbe095dce8f2892966243ecbd` |
| `README.md` | `33fb5bbc011fe600db21e745b7b1496e90cebb4f90997e53d51e3dc79d6734f3` |
| `docs/accession-standard.md` | `78d6a1aee981aecaea0cd219002ee7b81d6e54fd9bed2fbd1f72ee42f55a6976` |
| `docs/curatorial-publication-standard.md` | `de5b4d22eca06b07cf84a5a9bcf1fcf0348a8634239ed73132102404add8e2b5` |
| `docs/record-model.md` | `8f1102a21fb92b833f7c71e3db63e1917b819b561a0cee5b272ff3a83e7d4e52` |
| `docs/stream-interoperability.md` | `b1e89dc8a0a67cd16e5473b690a37c4e407387768831db643139c98e943cad2d` |
| `evidence/salgado-amazonia-authority/summary.json` | `241e7d44d43c9bd15f8e4fd5a87bc917ec55d7d838aa4fc456e93c4b82b4d432` |
| `evidence/salgado-amazonia-contract/0x55a989449cc4330132a0b064d1a16ce9325c9452.response.json` | `0e6b1a13a022f9dd1428ab0d1eb59ee9ae9246a23970482f3abd9f91cb56d15c` |
| `evidence/salgado-amazonia-contract/0x659d80ce8ac5cad5ab2fdd7137caf3d06d246289.response.json` | `f0a59d67d19a0afb44fb5a372d1bfa18f4d10f8209c0ef8d02c386bcb8043099` |
| `evidence/salgado-amazonia-contract/0xf1f036cebb4b64f138e4f57754edbceb64fb80fc.response.json` | `9d755bcce329f7f4c11f9c8207f590c6ad046f687729ec52961ae3468d0c714f` |
| `evidence/salgado-amazonia-custody/summary.json` | `8ea329d9ce50d4ac7c87ff086be6ab93ba9e61619f9f504e57e6d94846f0d423` |
| `evidence/salgado-amazonia-diligence/manifest.json` | `e6a530d3d9e908914a178a188e9c61ed4fbbf43e5daf1c5f0af556856f111508` |
| `evidence/salgado-amazonia-diligence/ofac-address-screening.json` | `febfb62df0c84c8b796ee5fd1ae8e4ee791065f3f90d65244be48962cd78df8d` |
| `evidence/salgado-amazonia-metadata/manifest.json` | `cc45a767608a2ec15f746d08d445f574bd21e2ae0b0ab75f760cbd53ac65b0cf` |
| `evidence/salgado-amazonia-preservation/display-preparation.json` | `29fc862a8764c7648fba1aff344e99f13020cdb734706bdfd72cd969148587ea` |
| `evidence/salgado-amazonia-preservation/manifest.json` | `c0c9e854237e7a7703a89d77213d6ac34efa24b7d743e590e71eb54065f2de13` |
| `evidence/salgado-amazonia-preservation/restoration-summary.json` | `2af890d73e3e2b4de6d5aaa5356b67dcdf6049c4a833becd3ccbe0018992df23` |
| `evidence/salgado-amazonia-provenance/summary.json` | `42c491b6833adb8cace7acb07cab994b6e1b8f57af6441844afbdb1d9a82619d` |
| `evidence/salgado-amazonia-sources/manifest.json` | `03ecbf9fe61a8e066ee9730d1644550f164b908b1da65a20f36756cdcc6e9392` |
| `evidence/salgado-amazonia-sources/metadata/1117.json` | `e7c517c2e57815f077b9fecb71a8fb21878a35af861369d79216db1fe333fbeb` |
| `evidence/salgado-amazonia-sources/metadata/2059.json` | `b58d06ca924f22467eae0d5289df5751c1d42580db2d48dacc5513765d8cd648` |
| `evidence/salgado-amazonia-sources/metadata/2216.json` | `2900995d9113ca9b9b08590a3e06fa4e61b637ee796433750ec1c9f1c5e1531c` |
| `evidence/salgado-amazonia-sources/metadata/226.json` | `2768b4a20b80a44b17a7990183cb4030ee03065ccdd7714a8588e458bd25d621` |
| `evidence/salgado-amazonia-sources/metadata/2768.json` | `46e3fe21ea0921ee1b8f6aceb840a881d6970f1f60bb07f222170e2c253b21e2` |
| `evidence/salgado-amazonia-sources/metadata/4697.json` | `66ef09dfe5d8bd394e82399cdf69f1d97908c9232256d5f5feff205af26d5e7f` |
| `evidence/salgado-amazonia-wave/manifest.json` | `4ca5c6bfccc66d637d9dc63d1a557e5b96bfd0511ca02fadd8fb4b4c9011509e` |
| `evidence/salgado-amazonia-wave/original-publication.json` | `9faae6ca1f75fe33c5b3cfc372c2d54dc070ef55f06f97f616117452ecd8c778` |
| `evidence/salgado-amazonia-wave/response.json` | `7fcc5c3f88609ef3d084e64e185660dbf652949df051474d67a443826a1b4e13` |
| `governance/pull-request-review-policy.md` | `d6f69774caf1189c2fcda8f84f46ae76d04aadbcbe95bd38b7851fbc32515aca` |
| `records/accessions/6529NM.2026.004/accession-statement.json` | `9c02393a38f3b9561a15512c78041e4f9863733b429438567c43672fd0207230` |
| `records/accessions/6529NM.2026.004/gift-acceptance-authorization.json` | `fe8845644d08d4633d0995c3c29f16ddad7d2c9c7ccf4ef800790c217767d719` |
| `records/accessions/6529NM.2026.004/objects/6529NM.2026.004.01.json` | `45eb8d6470c46c592d4ee0b2c2ee64b4e3dc8a1ece8cfdc5719ffc5c4eef825e` |
| `records/accessions/6529NM.2026.004/objects/6529NM.2026.004.02.json` | `a7a4f6f02b97ba9e54086168a3786ddfb8de954290e3a0bad6cf3e683ac7a5c1` |
| `records/accessions/6529NM.2026.004/objects/6529NM.2026.004.03.json` | `d7cebbf41adf4b39e04a543b7352e5f2215839c93de9e4d6a619d80d9403dce2` |
| `records/accessions/6529NM.2026.004/objects/6529NM.2026.004.04.json` | `4d42d714a710cd2b73438472861487b965eace4098cf1db2c3c8bad5e2b6d789` |
| `records/accessions/6529NM.2026.004/objects/6529NM.2026.004.05.json` | `216213cd1def9f6f38381ee0bc9549a0d3f7dc308174f4db2c1d4667dc7b1caf` |
| `records/accessions/6529NM.2026.004/objects/6529NM.2026.004.06.json` | `6f38ef787d78ed5cf0842bc8b38f139976c30a5db0f990f26caf2b14d9a5e92d` |
| `records/accessions/6529NM.2026.004/public/6529NM.2026.004.01.md` | `069fe9927dd6e0686f83628e7bca08fca7780ad8f27700eba312115d574d5ebf` |
| `records/accessions/6529NM.2026.004/public/6529NM.2026.004.02.md` | `0b030324b1e3b60fefc0f2571c4dcb5f9b1601f108e1b0bff496ff9378d59997` |
| `records/accessions/6529NM.2026.004/public/6529NM.2026.004.03.md` | `c94b6a2c5b1d439310f314d18e846441578dea25f947edb42d117700de57bf1e` |
| `records/accessions/6529NM.2026.004/public/6529NM.2026.004.04.md` | `6d5148449f666ca56bc512a3ccca0943e7f4d8124db85e3a775ae2cf7055d574` |
| `records/accessions/6529NM.2026.004/public/6529NM.2026.004.05.md` | `97415e12eb351b7e89f06210cc9aeff00fd77f43c16b0543397105ce0dc7cd4c` |
| `records/accessions/6529NM.2026.004/public/6529NM.2026.004.06.md` | `444d7e8e0409ec9772d40a73d39c06348504ecd555a31f3e1f0cbb74dd1d704a` |
| `records/accessions/6529NM.2026.004/public/README.md` | `c43a2afac8b8532d3269bc2a2caa5b5300b14e4031adca6e5a251adcaa6bf4bf` |
| `records/accessions/6529NM.2026.004/public/acquisition-narrative.md` | `79032e865b672baf4c49877a2e443aef792ac9a4badc492bf32abfd4f013863e` |
| `records/accessions/6529NM.2026.004/public/amazonia-project.md` | `d1b67be8c66d4d15291bd956834bb064ff1540ae5d0036dfba1a111de1d27cdc` |
| `records/accessions/6529NM.2026.004/public/display-and-preservation.md` | `3b525f1929474cc9dd8003fb9e250f7e640a17643f4e277e489f45501cdb3d97` |
| `records/accessions/6529NM.2026.004/public/forest-water-and-community.md` | `c7971cf6cb5f781ca224e826a759cb95888cb9a6928669d5f0b530483ea8eb04` |
| `records/accessions/6529NM.2026.004/public/registration-diligence.md` | `ffa2a37f823187a2fff2dee3792ca75747f0fe22c7494104dc81501100c3b432` |
| `records/accessions/6529NM.2026.004/public/sebastiao-salgado.md` | `c81ee3e18dc209b3b28b69d075a805170a3cfe8a3abba44017746e6d964c3689` |
| `records/accessions/6529NM.2026.004/public/source-and-chronology.md` | `b4e7a97bf23595b4bc07405ef5761f793f3bff919bdcc92a71086682f8172217` |
| `records/accessions/6529NM.2026.004/public/technical-and-condition-review.md` | `84d549cfaec48986c215170fd1ca7d47771383df27298ac0161997be71b1ef23` |
| `records/accessions/6529NM.2026.004/public/title-rights-and-display.md` | `69106efb6c559e941fd79815f854fd27c540599d904c91eb2bd8e2c27b49b3b5` |
| `records/accessions/6529NM.2026.004/rights/6529NM.2026.004.RIGHTS.01.json` | `9f4fe282f48c10ae8bfa17902898cc82d56bb41ef1d7791120c31351c8ae467d` |
| `records/accessions/6529NM.2026.004/rights/6529NM.2026.004.RIGHTS.02.json` | `4ae4749aa4aa0e4fe910fceed77536687aac929de33bb2e0271a1ac159ab968f` |
| `records/accessions/6529NM.2026.004/rights/6529NM.2026.004.RIGHTS.03.json` | `916295f6147af2ccd9f129f6caa32e37bcbd325272f9929927e5c8020dc87543` |
| `records/accessions/6529NM.2026.004/rights/6529NM.2026.004.RIGHTS.04.json` | `cee2039d5c0f7a7ecfdb4b06c2b02431a0c543c24d905a881d4e33fa7fa77066` |
| `records/accessions/6529NM.2026.004/rights/6529NM.2026.004.RIGHTS.05.json` | `8c5b444e9d2f4d2ea87bc0faeb269b4dc0b64fdc2596cf1e8f4c3ada62963900` |
| `records/accessions/6529NM.2026.004/rights/6529NM.2026.004.RIGHTS.06.json` | `df95c9337da4def7e18632c57281643af72cdab2d0e30ce4a74ba2eba688fd3f` |
| `records/accessions/6529NM.2026.004/technical/6529NM.2026.004.01.json` | `6e63077abd22581b6d152f32f8cf96604ef7842b259baa6a527d833888b2620c` |
| `records/accessions/6529NM.2026.004/technical/6529NM.2026.004.02.json` | `fca89fb6ad5f36b693aaabf1c6499d4e04ed5212bb0ccf5e3f538342a4f09565` |
| `records/accessions/6529NM.2026.004/technical/6529NM.2026.004.03.json` | `27b7be308c3df19bf10830c56d58b32ee2fbcb4323e1f3afb7511012f6931e8d` |
| `records/accessions/6529NM.2026.004/technical/6529NM.2026.004.04.json` | `db97e37593143983c45db7e5d1ccb796ea3997272a04245f245a180d014918a9` |
| `records/accessions/6529NM.2026.004/technical/6529NM.2026.004.05.json` | `fe67035704098376d3d22955400c59392241b64a25417d9833cc026bcb995463` |
| `records/accessions/6529NM.2026.004/technical/6529NM.2026.004.06.json` | `2697094398e56896ce320fa8c9a10464541cf379f75d0e78c182adfbe99c060f` |
| `records/proposed-gifts/6529NM-PG-2026-003/public/wave-resolution.md` | `f8313636375109aecf3bad66062beae59fac7223b9b60d8c0d87ee87d95b4f0a` |
| `records/proposed-gifts/6529NM-PG-2026-003/wave-status-observation.json` | `5d10ce1a73d3ddfa3869b84948122d5158fb8f84a5bd8a23ed4c542beb57f308` |
| `scripts/build_salgado_accession_package.py` | `baa3736b644fc47b7b8870f90c68e50bdfa679a568c1f26f5e54a360df41e683` |
| `scripts/validate.py` | `ae698bbd1068a965ec5748422a7e715a1bfec3cfc69e236c865e6190ae03d41a` |
| `tests/test_salgado_accession.py` | `9490500682943eca9a3311c308bddfb71fa21651ddc7d8b3f7c859c33f9f2d5c` |

### Restricted evidence inspection commitments

Only local receipt filenames and digests appear below; storage destinations and exact object versions remain restricted.

| Local receipt | Raw SHA-256 |
| --- | --- |
| `package-receipt.json` | `6df6d4442ffcb653cf6abf5833179a985bde7c3c0646ffbbe1065003120cf4c1` |
| `private-replica-receipt.json` | `0bd8d460a87a4cb1179f4bdcfe787db0eed1c029fad1cd058be74057ca902677` |
| `private-restore-us-east-1.json` | `726cb58f2896e3ad46b7af6f0f7316b4a4e6d36c9b380d3c7f01d72d8a408e12` |
| `private-restore-eu-west-1.json` | `904d1d017ed8ff79cb982ce0d956af6e35527ae09aa222e65c5f120b61bd5bba` |

### Final offline review presentation

| File | Raw SHA-256 |
| --- | --- |
| `index.html` | `5a0ec54cc611a0e0ce3bea0de652b5d929639b365a929aac02c27bf9f3762066` |
| `media-manifest.json` | `29fc862a8764c7648fba1aff344e99f13020cdb734706bdfd72cd969148587ea` |

**Binding decision recorded by:** Codex independent subagent `/root/salgado_independent_review`, at `2026-09-13T22:28:02.392785+00:00`. No human or protected-PR approval is claimed.
