# Keys and Gates — institutional and source record

This page is the control and evidence layer for the public [Keys and Gates](curated-acquisition.md) catalogue page. It preserves the distinction between visitor-facing curatorial prose and the records required for acquisition, rights, technical, and accession review.

## Current control state

| Field | Retained value |
|---|---|
| Acquisition Program | `6529NM-AP-01` |
| Curated Acquisition ID | `6529NM-CA-2026-002` |
| Program status | `selection_complete_acquisition_and_accession_unverified` |
| Status observation | `2026-08-01T15:03:35Z` |
| Selected-outcome state | `selected_unminted` |
| Selected outcomes | 16, ranked 1–16 |
| Distinct artist handles | 15 |
| Program Wave | `4ff022b3-aa17-4a0a-ba78-58f64ff1d427` |
| Description drop | `71c798bc-629d-46f2-8610-507a91be4f57`, serial `972000` |
| Formal program note | [`program.json`](../program.json) |
| Outcome index | [`selected-works.json`](../selected-works.json) |
| Evidence inventory | [`notes/research/keys-and-gates-evidence.md`](../../../../notes/research/keys-and-gates-evidence.md) |

This is the latest retained control observation in the canonical repository. It is not a live status refresh on the date of this editorial build.

## Selection evidence and boundary

The retained evidence supports sixteen signed `WINNER` submissions in the program Wave. The selection record explicitly says that sixteen is not a guaranteed acquisition quantity; rank-order fallback applies when a selected work is unavailable or fails program terms, and final quantity is related to Meme Card mints.

The program terms record a planned price of `0.5 ETH` per acquired work and a planned custody reference of `networkmuseum.6529.eth`. Those are program terms and planning references. The evidence set contains no verified mint, deployed contract, token ID, CAIP-19 identity, purchase, payment, title passage, transfer, custody receipt, or accession for these outcomes.

The future acquisition method is described in the working ontology as primary mint and purchase under program terms. Mint topology remains undecided between a dedicated 6529Stream instance and a main-Stream subcollection. No topology, contract, or transaction should be inferred from the selected state or the media derivatives.

## Registrar gates

Before an outcome can move from selection toward acquisition or accession, the program record requires review of:

1. artist availability and final program terms;
2. artist identity, public credit, title, and authority;
3. effective CC0 instrument and depicted-person consent;
4. contract, network, token, metadata, and media identity;
5. purchase and mint transaction evidence;
6. a title binding for the specific transfer;
7. custody receipt and independent custody verification;
8. technical, condition, preservation, accessibility, and display readiness;
9. curatorial and mission fit;
10. accession statement and individual object record; and
11. second-person review.

The current [rights and consent register](rights-and-consent.md) and [media join register](media-joins.md) document the open gates. Direct artist questions and restricted documents remain in the registrar work queue. Their existence is workflow evidence, not completion evidence.

## Public/restricted boundary

Public now: selection identifiers, artist handles and approved public-source biographies, artist-attributed submission readings, visual descriptions of the reviewed presentation derivatives, source links, current media joins, and explicit unknowns.

Restricted or pending: legal identity documents, direct contact details, model releases, consent instruments, sensitive locations, unredacted passport/document details, original high-resolution bytes, layered source files, exact site permissions, title documents, transaction evidence, custody receipts, and technical preservation packages.

The public corpus does not publish private contact information or treat a platform handle as a legal identity. Sensitive biography, migration, sexuality, religion, nudity, minor status, and location claims remain attributed, minimized, or held pending direct approval.

## Media and rights boundary

The existing [`PROGRAM_MEDIA_MANIFEST`](../media-manifest.json) identifies submitted source fixity and 48 deterministic WebP presentation derivatives. The source bytes were fixity-checked during derivation but are not retained in the repository. The derivatives are web-presentation surrogates, not preservation masters, tokenized artworks, or evidence that rights have become effective.

The manifest’s `rights_effective_status` remains controlling for each outcome. Artist statements that say “CC0,” “CCO,” or that all rights are held are submission assertions until the Museum receives and reviews an effective rights instrument, authorship/title evidence, third-party-material status, and any required depicted-person consent.

Creative Commons’ public guidance also separates copyright dedication from personality, privacy, publicity, and trademark rights. The [rights register](rights-and-consent.md) applies that distinction to people, minors, nudity, passports, graffiti, posters, sites, and physical miniatures.

## Transcription and correction note

The public page renders OUT-015 as **মুক্তিযুদ্ধ - Fight for Freedom**, following the authoritative Bangla title visible in the artist submission/media evidence. The current `selected-works.json` contains an encoding/mojibake transcription of the Bangla portion. This page does not silently modify the canonical JSON. A future append-only correction should preserve the original assertion, add `supersedes`, bind the corrected title to the direct submission evidence, and receive the repository’s normal review.

The same source discipline applies to other title or credit questions: OUT-002 preserves the submitted `teh` spelling pending artist confirmation; `GulYildiz`/Gül Yıldız, `pandelic`/Eric Pan, `Minalisa`/Mina Rahmani, `shamspranto`/Shams Nayeem Pranto, and `Veerendra`/Veerendra Jillella are displayed as source-layer associations with unresolved authority questions where indicated.

## WP-1 integration dependencies

The content layer depends on the shared definitions listed in [schema-dependencies.md](schema-dependencies.md) and the [WP-1 publication integration handoff](publication-integration.md). WP-4 has not modified shared schemas, controlled vocabularies, lifecycle values, Stream envelopes, CAIP-19 conventions, media-manifest schemas, or rights registries.

Integration must preserve:

- `6529NM-AP-01` and `6529NM-AP-01-OUT-###` identifiers;
- `selected_unminted` and the formal program status;
- Work, agent, right/permission, evidence, record, package, manifestation, and presentation-surrogate distinctions;
- observation times, fixity, evidence grades, and negative evidence;
- append-only corrections with `supersedes`; and
- public/restricted separation.

## Exact non-claims retained for audit

The public corpus does not establish:

- minting, deployment, token ID, contract, network, metadata, or CAIP-19 identity;
- purchase, payment, sale completion, title passage, or acquisition completion;
- transfer to or receipt by `networkmuseum.6529.eth`;
- effective CC0, model release, depicted-person consent, or unrestricted reproduction rights;
- preservation-master creation, technical completion, or display readiness;
- accession, accession number, Collection membership, or permanent-holding status; or
- that all sixteen selected works will ultimately be acquired.

Those boundaries are deliberately kept here so the visitor-facing page can remain a sustained photographic argument.
