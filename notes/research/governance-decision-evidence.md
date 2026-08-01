# 6529 Network Museum governance decision evidence

Status: WIP research evidence; this note is not itself an adopted policy or a new governance decision.

Observation date: 2026-08-01 UTC

## Scope and evidence boundary

This note records the complete proposal set currently returned for the 6529 Network Museum Wave and the institutional source that states the Museum's mission and custody policy. It separates:

- **Source transcription** — the exact or minimally formatted wording of the governing source;
- **Live observation** — mutable API fields observed at a stated time; and
- **Interpretation** — the narrow repository consequence of the source, without adding authority that the source does not grant.

The Museum Wave is `https://6529.io/waves/5f207393-5418-4a75-8738-e40edb44a94d`. Its initial description says: “This is the decision-making wave for the 6529 Network Museum. Proposals can be of any nature, but in practice need to be self-funding.” That chat drop is context about the Wave, not a substitute for an adopted proposal.

The complete authenticated API snapshot was refreshed at `2026-08-01T15:01:05Z` and returned 2,629 drops: 2,621 chat drops and 8 proposal drops. The local snapshot and proposal-payload hashes were:

- `wave-snapshot.json`: `sha256:2185bbc52ed47c7a4a35b5bdee4ce75a0e55c8633d420aa5cd9ac7997c6edaef`;
- `proposals.json`: `sha256:7693e75ca37a15ff200c3deed02377a64bbe140ac34bdfa3d9c445cd77170fe7`.

The eight proposal drops were reread individually through the authenticated `punk6529bot drops get <drop-id> --json` helper after the snapshot. Their `drop_type`, `rating`, `realtime_rating`, and `raters_count` values matched the snapshot. The figures below are the API's displayed Wave rating / TDH rating (`rating` / `realtime_rating`) at the stated observation, not counts of raters or approvals. Live `drop_type` controls adoption status: `WINNER` is recorded as adopted and `PARTICIPATORY` as active/not adopted. A displayed rating total, including one above a discussed threshold, is not used to infer adoption.

The institutional source was fetched directly at `2026-08-01T15:03:05Z` from [the permanent institutional note](https://6529networkmuseum_thememes.ar.io/), HTTP 200, with HTML SHA-256 `sha256:75889ed25b623fde356129e39ba5330d4c0c2b38de0f3a7d94355282ff28b8d4`.

URL fidelity: the institutional source's published URL is exactly `https://6529networkmuseum_thememes.ar.io/`, including the underscore in the host. That exact URL was fetched successfully and is preserved verbatim for provenance. This note makes no claim that the host is a DNS-normalized or RFC-normal hostname, and does not silently replace it with a guessed variant.

## Mission source — source transcription

The mission is sourced to the permanent institutional note, not reconstructed from chat or inferred from the proposal titles. The relevant transcription is:

> The 6529 Network Museum is a cultural museum of the 6529 Network: a permanent collection of NFT art held for long-term stewardship, research, interpretation, and public access.
>
> Its goal is to become the world's most impactful decentralized art museum: open globally, governed by the network, and built for cultural permanence rather than financial extraction.

The note also transcribes these governing principles:

> The collection is held for the benefit of the 6529 Network and the public commons.
>
> Accessioned works are intended to be held in perpetuity.
>
> The collection is not an investment vehicle.
>
> No individual network member has a claim on collection assets, investment returns, dividends, or distributions.

Its launch note closes with the stable-mission wording:

> build a permanent, publicly legible, network-governed collection for the open metaverse.

### Mission interpretation

The institutional note supplies the Museum's mission and public-good posture. The six adopted Wave proposals implement collection scope and donation authorization around that mission; they do not turn the Museum into an investment vehicle, grant members an asset claim, or make every in-scope work automatically accessioned.

## Complete Museum Wave proposal register — live observation

All timestamps are UTC. `Decision time` is present only where the live API returned `winning_context.decision_time`; a blank value is not a negative decision, only the absence of an adopted-WINNER decision timestamp in the response.

| Serial | Proposal | Drop ID | Live status | Institutional effect | Created | Decision time | Wave rating / TDH rating (`rating` = `realtime_rating`) | Raters |
|---:|---|---|---|---|---|---|---:|---:|
| 1052148 | Autoglyphs | `d2613993-2714-4618-b2db-8175f395cea6` | `WINNER` | adopted | 2026-06-02T13:24:57Z | 2026-06-05T02:10:15Z | 90,331,683 | 25 |
| 1052156 | Art Blocks | `2e88273f-013c-4fdd-bea3-7de5451098e8` | `WINNER` | adopted | 2026-06-02T13:27:00Z | 2026-06-05T05:25:15Z | 73,698,446 | 21 |
| 1052401 | Rare Pepes | `457056cf-3090-4332-ba37-196b10f5f5d2` | `WINNER` | adopted | 2026-06-02T14:04:58Z | 2026-06-04T15:44:15Z | 74,715,713 | 22 |
| 1052437 | CryptoPunks | `e7999acd-4e06-44fc-8f40-bd8d55dc91d1` | `WINNER` | adopted | 2026-06-02T14:13:36Z | 2026-06-04T11:50:19Z | 85,650,475 | 24 |
| 1052604 | General NFT Collecting Scope | `d65befc2-65dc-4362-8ddd-75f867338669` | `WINNER` | adopted | 2026-06-02T14:50:40Z | 2026-06-05T02:46:14Z | 89,724,244 | 26 |
| 1052714 | The Complaint Cards (not) by 6529 | `d91dc46f-68f3-4879-bb78-bf369ae52046` | `PARTICIPATORY` | not adopted at observation | 2026-06-02T15:21:49Z | — | 5,646,938 | 15 |
| 1052812 | 6529 Network Museum Donation Acceptance Policy | `86e43beb-b55d-42f0-9eea-a3c115b08abc` | `WINNER` | adopted | 2026-06-02T15:45:27Z | 2026-06-05T03:56:15Z | 87,077,479 | 21 |
| 1069256 | Lost Robbies | `21b4ba5d-1015-4853-89a0-71eaf780199e` | `PARTICIPATORY` | not adopted at observation | 2026-06-08T17:23:19Z | — | 44,711,261 | 18 |

The source status is retained separately from the institutional effect so a future API status change can be appended without rewriting this observation. The two `PARTICIPATORY` rows are not adopted even though Lost Robbies has a larger displayed rating than the provisional threshold discussed in chat.

## Six adopted `WINNER` proposals — source transcription and effect

The full proposal payloads, including their rationales, are preserved in the authenticated snapshot used for this observation. The operative source wording is transcribed below; the rationale is not silently promoted to policy text.

### 1. Autoglyphs — Wave #1052148

> The 6529 Network Museum considers Autoglyphs to be within scope for the Museum’s collection.
>
> Donations of Autoglyphs may be accepted without further collection-specific review, subject only to the Museum’s ordinary procedures for provenance, title, custody, wallet security, legal compliance, and donor acceptance.

The proposal also states that acquisition programs involving Autoglyphs may be pursued only when approved, funded, and executed through ordinary Museum governance, budgeting, and acquisition processes.

**Interpretation:** Autoglyphs are a preapproved donation category and safe harbor. This is not an individual accession, purchase authorization, or waiver of ordinary checks.

### 2. Art Blocks — Wave #1052156

> The 6529 Network Museum considers Art Blocks collections to be within scope for the Museum’s collection.
>
> Donations of works from Art Blocks collections may be accepted without further collection-specific review, subject only to the Museum’s ordinary procedures for provenance, title, custody, wallet security, legal compliance, and donor acceptance.

The proposal separately says that other on-chain generative art collections may be reviewed through ordinary processes and that Art Blocks acquisition programs require ordinary governance, budgeting, and acquisition execution.

**Interpretation:** Art Blocks collections are preapproved for donation purposes. This does not preapprove every generative-art collection or accession every Art Blocks work.

### 3. Original Rare Pepes — Wave #1052401

> The 6529 Network Museum considers the original Rare Pepe collection to be within scope for the Museum’s collection.
>
> Donations of original Rare Pepe cards may be accepted without further collection-specific review, subject only to the Museum’s ordinary procedures for provenance, title, authenticity, custody, wallet security, legal compliance, donor acceptance, and any artwork-specific review required by Museum policy.

The proposal expressly says that this does not automatically include all Pepe derivatives, meme coins, later derivative projects, or meme-based NFT collections.

**Interpretation:** Original Rare Pepes are preapproved; derivatives and adjacent projects remain subject to separate review.

### 4. Original CryptoPunks — Wave #1052437

> The 6529 Network Museum considers the original CryptoPunks collection to be within scope for the Museum’s collection.
>
> Donations of original CryptoPunks may be accepted without further collection-specific review, subject only to the Museum’s ordinary procedures for provenance, title, authenticity, custody, wallet security, legal compliance, donor acceptance, and any artwork-specific review required by Museum policy.

The proposal expressly says that this does not automatically include all PFP collections, CryptoPunks derivatives, avatar projects, or later NFT collectibles.

**Interpretation:** Original CryptoPunks are preapproved; the proposal is not blanket approval for PFPs or derivatives.

### 5. General NFT Collecting Scope — Wave #1052604

The exact operative opening is:

> The 6529 Network Museum considers historically, artistically, culturally, or technically significant NFTs and blockchain-native digital objects to be within scope for the Museum’s collection.

The proposal's eleven category headings are transcribed here in full: **PFPs and avatar projects; Generative art; 1/1 digital art; Editions; NFT photography; Meme-native and internet-culture works; Interactive, dynamic, and programmable works; AI, computational, and software-based works; Video, audio, literary, and mixed-media NFTs; Virtual-world, gaming, and metaverse-native objects; Protocol-native and platform-native cultural artifacts.**

The operative boundary is:

> The inclusion of a category within scope does not mean that every work or collection in that category must be accepted. Individual works, collections, and acquisition programs remain subject to the Museum’s ordinary procedures for curatorial review, provenance, title, authenticity, custody, wallet security, legal compliance, donor acceptance, budgeting, and governance.

The proposal also authorizes the Museum to establish specific safe-harbor categories or pre-approved collections, where donations may bypass further collection-specific review while remaining subject to ordinary operational, legal, provenance, and custody checks.

**Interpretation:** This is broad category-level eligibility, not automatic acceptance. It is the source for the general scope record and for the distinction between “in scope,” “preapproved,” “accepted,” and “accessioned.”

### 6. Donation Acceptance Policy — Wave #1052812

The policy's purpose is transcribed as:

> The 6529 Network Museum may accept donations of digital artworks, NFTs, on-chain cultural artifacts, and related works that are consistent with its mission and collecting scope.
>
> This policy establishes two donation pathways:
>
> 1. donations from preapproved collections, which may be accepted without further pre-authorization; and
> 2. all other donations, which require authorization before acceptance.

The core principle is:

> A work is not part of the Museum’s collection merely because it has been offered, proposed, transferred, airdropped, or sent to a Museum-associated wallet.
>
> A work becomes part of the Museum’s collection only when it is accepted under this policy or another valid Museum governance process.

For preapproved collections, the source says:

> Donations from preapproved collections do not require further collection-specific pre-authorization before acceptance.
>
> Preapproved status means that the collection or category has already been determined to be within the Museum’s scope. It does not waive ordinary donation checks, including authenticity, provenance, title, donor authority, legal compliance, rights, technical receivability, and donor acceptance.

For non-preapproved donations, the source says:

> All donations outside preapproved collections require authorization before acceptance.
>
> Until authorization is granted, the work should be treated as a proposed donation, not as an accepted collection work.

For unsolicited transfers, the source says:

> Unsolicited transfers, airdrops, spam tokens, scam tokens, malicious tokens, or accidental transfers are not automatically accepted as donations.

The rights clause says:

> Donation of an NFT or other digital object does not necessarily transfer copyright, commercial rights, reproduction rights, display rights, or preservation rights.

The refusal clause says the Museum may refuse any proposed donation, including one from a preapproved collection, where acceptance conflicts with its mission, policies, legal obligations, curatorial standards, preservation responsibilities, public trust, or unacceptable legal, technical, reputational, financial, administrative, or governance risk.

**Interpretation:** The adopted policy creates a donation authorization framework, not an automatic-acquisition rule. Preapproval removes only another collection-specific authorization step. It does not establish title, custody, rights, technical receipt, accession, or cataloguing for a particular work.

## Preapproved collections — interpreted register

The four current preapproved donation categories are derived from four separate adopted `WINNER` proposals, not from chat or from a transfer:

1. Autoglyphs — `6529NM-GOV-1052148`;
2. Art Blocks collections — `6529NM-GOV-1052156`;
3. Original Rare Pepe collection — `6529NM-GOV-1052401`; and
4. Original CryptoPunks collection — `6529NM-GOV-1052437`.

The adopted General NFT Collecting Scope proposal permits future safe harbors, and the adopted Donation Acceptance Policy says the list should be maintained separately and may be amended through ordinary governance. Until a later adopted record exists, the four categories above are the complete evidence-supported list.

## Two non-adopted `PARTICIPATORY` proposals — source transcription and effect

### The Complaint Cards (not) by 6529 — Wave #1052714

The proposal asks:

> The 6529 Network Museum considers “The Complaint Cards (not) by 6529” to be within scope for the Museum’s collection.
>
> Donations of “The Complaint Cards (not) by 6529” from 6529complaints.eth or others may be accepted without further collection-specific review, subject only to the Museum’s ordinary procedures for provenance, title, custody, wallet security, legal compliance, and donor acceptance.

**Live status and interpretation:** `PARTICIPATORY` at the 2026-08-01 observation; 5,646,938 displayed Wave rating / TDH rating from 15 raters; not adopted. The source text is a proposal record only and creates no Complaint Cards safe harbor.

### Lost Robbies — Wave #1069256

The proposal asks:

> The 6529 Network Museum considers the original Lost Robbies to be within scope for the Museum’s collection.
>
> For this purpose, “Lost Robbies” means the original Robbie Barrat AI-generated Nude Portrait #7 frames associated with the 2018 Christie’s Art+Tech Summit and minted on SuperRare, not later derivative projects, tributes, wrappers, or works merely inspired by them.
>
> Donations of original Lost Robbies may be accepted without further collection-specific review, subject only to the Museum’s ordinary procedures for provenance, title, authenticity, donor authority, legal compliance, rights, technical receivability, donor acceptance, and artwork-specific suitability.

**Live status and interpretation:** `PARTICIPATORY` at the 2026-08-01 observation; 44,711,261 displayed Wave rating / TDH rating from 18 raters; not adopted. The higher displayed rating does not override the live status and creates no Lost Robbies safe harbor.

## Custody wording — source transcription

Custody language is sourced to the institutional note, not inferred from the presence of an asset in a wallet. The note says:

> The collection is held for the benefit of the network. Initial custody is maintained through a multisignature SAFE.
>
> Museum custody: networkmuseum.6529.eth
>
> The signing policy is expected to progressively decentralize over time.
>
> Initial signing policy:
>
> - Signers: @punk6529, @6529er, @itsjpower, @maybe, @hugofaz
> - Quorum: 3 of 5
> - Rationale: maintain a group with high confidence that it will transfer control toward the TDH model when technically and operationally feasible
>
> Future signing policy:
>
> - Plurality TDH control once the required technical and operating structures are ready

The permanent-holding text further says accessioned works are intended to become part of a permanent public holding; rare exchanges or transfers may be authorized only to advance the collection's curatorial mission; and “No such action is permitted during the initial signing policy period.”

### Custody interpretation and non-claims

This wording records the institutional custody reference and intended signing policy. It is not a live assertion that the named SAFE, signer set, quorum, or any particular NFT custody state still exists unchanged. A future custody-sensitive record must independently verify the current chain/SAFE state. Custody is also not accession: a transfer to `networkmuseum.6529.eth` does not by itself establish acceptance, title, rights, or a completed accession.

## Permanent append-only decision format

Each governed proposal observation should be represented as a new immutable record with a stable decision identifier. The canonical bare identifier is `6529NM-GOV-<wave-serial>`, for example `6529NM-GOV-1052604`, and **the bare form always means revision 1**. Every later revision must use an explicit revision suffix such as `6529NM-GOV-1052604-v2`; every amendment must use an explicit amendment suffix such as `6529NM-GOV-1052604-A01`. These suffixes are distinct record IDs, not aliases, and the record must populate explicit revision/lineage fields.

Minimum fields:

```yaml
record_type: GOVERNANCE_DECISION
record_id: 6529NM-GOV-1052604
record_version: 1
revision_kind: original
wave_id: 5f207393-5418-4a75-8738-e40edb44a94d
wave_serial: 1052604
drop_id: d65befc2-65dc-4362-8ddd-75f867338669
source_uri: https://6529.io/waves/5f207393-5418-4a75-8738-e40edb44a94d
source_observed_at: 2026-08-01T15:01:05Z
proposal_created_at: 2026-06-02T14:50:40Z
source_status: WINNER
institutional_effect: adopted
rating_observation:
  wave_rating: 89724244
  tdh_rating: 89724244
  raters: 26
  api_fields: rating_and_realtime_rating
source_transcription:
  title: Proposal: General NFT Collecting Scope
  operative_text: "Exact source wording, without added policy language."
interpretation:
  authority_granted: "Category-level collecting scope and future safe-harbor authority."
  explicit_non_effects: "No automatic acceptance, accession, title, custody, rights, or budget authorization."
lineage:
  supersedes: null
  amends: null
  reason: null
  original_hash: sha256:<hash-of-canonical-record>
```

Lineage rules:

1. Never edit or delete a published source transcription or its observation fields.
2. A new live status or rating observation is a new version/observation record, even if the proposal text is unchanged.
3. Use `amends` when a later record changes only a defined part of the interpretation or operational effect.
4. Use `supersedes` when a later authoritative record replaces the prior decision record in the current view. The prior record remains in the append-only history and its hash is retained.
5. Every amendment records its own authority, source URI, observation/effective timestamps, reason, and evidence. It must state the prior record ID and hash.
6. Source transcription and interpretation are separate fields. An interpretation correction never silently rewrites the source text; a source correction is an attributed new transcription with its own hash and supersession lineage.
7. A current-view index may point to the latest non-superseded record, but it must not erase or conceal the earlier record.

For the two `PARTICIPATORY` proposals, the same format is used with `source_status: PARTICIPATORY`, `institutional_effect: not_adopted`, and `supersedes: null`. If either later becomes `WINNER`, the status change is appended as a new live observation and the new adopted decision record must identify the prior non-adopted observation; the old record is never rewritten.

## Unresolved verification items

- This research note verifies the institutional custody wording but does not claim a fresh on-chain SAFE configuration or NFT ownership check.
- No donation is recorded as accepted or accessioned by this note. Preapproval is not accession.
- The API's live status and rating fields should be reobserved before any donation, acquisition, custody, or accession action.
- Any future correction to mission, scope, preapproved collections, donation policy, or custody wording must be added as an attributed amendment/supersession rather than silently editing this evidence.

## Source index

- [Institutional note](https://6529networkmuseum_thememes.ar.io/) — mission, public-good posture, custody wording, permanent holding, and acquisition framework; fetched 2026-08-01T15:03:05Z.
- [Museum Wave](https://6529.io/waves/5f207393-5418-4a75-8738-e40edb44a94d) — proposal source container.
- Authenticated API snapshot — generated 2026-08-01T15:01:05Z; proposal payloads are identified above by Wave serial and drop ID.
