# Publishing Museum proposals as Wave Storms

- **Status:** working public publication standard; not adopted acquisition policy
- **Version:** 1.1.0
- **Publication date:** 2026-08-06
- **Applies to:** multi-part 6529 Network Museum proposals published in a Wave
- **Companion standard:** [`proposed-gift-wave-standard.md`](proposed-gift-wave-standard.md)

## Purpose

A Museum Storm must work at three distances. In the leaderboard it needs an image and title that can be understood at a glance. In the open drop it must present the exact decision, works, evidence, and competing arguments in a coherent sequence. In the repository it must survive as a reproducible source edition whose text, media order, rights, and fixity can be checked before and after publication.

The Storm is the proposal's public reading room and voting object. The repository is its governed source. The Wave records discussion, TDH votes, and outcome. Publication never turns an offered work into a holding, and a transfer to a Museum wallet never substitutes for selection, acceptance, or accession.

## Current 6529.io publication envelope

The following limits describe the supported profile for Museum Storms. They are release facts, not permanent properties of the Wave protocol, and must be rechecked before each publication.

| Element | Supported profile | Museum rule |
|---|---:|---|
| Text in one part | 25,000 UTF-16 code units and 65,535 UTF-8 bytes | Both limits are hard maxima. A part must satisfy both. |
| Text in one Storm | 50,000 UTF-16 code units | Hard maximum across the ordered parts. |
| Media files in one Storm | 8 | Count files across every part, including the cover. |
| Preferred cover | 1 PNG, 1,600 × 1,600 px | Opaque sRGB square; aim below 2 MB. |
| Work image | one image on its work part | Use the exact governed source image, uncropped, with visible credit and rights. |
| Drop title | up to 250 UTF-16 units in the API | Supply the reviewed proposal title; aim for 80 units or fewer. The cover and first lines must still carry the identity for clients that omit the title. |

The counts apply to the exact UTF-8 Markdown submitted for each part, with LF line endings and the final LF included. UTF-16 code units are JavaScript string length, not Unicode code points: a character outside the Basic Multilingual Plane uses two units. UTF-8 bytes are measured independently. Python's `len()` is therefore not an admissible substitute for the UTF-16 calculation.

The hard limits protect acceptance. The Museum's working targets protect editing and transport: no more than 20,000 UTF-16 units or 60,000 UTF-8 bytes in one part, and no more than 45,000 UTF-16 units across a Storm. A proposal may exceed a working target when the scholarship requires it, but it must never exceed a hard limit.

The API accepts PNG, JPEG/JPG, GIF, and WebP images, along with supported video, audio, and GLB formats. A Museum proposal should use still images unless the work requires another manifestation. The upload service accepts large files, but its transport ceiling is not a publication target. A cover should remain economical, and a work image should preserve the source dimensions and compression where the upstream file is already the governed reference.

### Pinned implementation evidence

Observed on production at 2026-08-06T11:18:41.858Z:

- `https://6529.io/api/version` returned frontend commit [`c807f6da8efea7e39405fba8185de153096bf95d`](https://github.com/6529-Collections/6529seize-frontend/tree/c807f6da8efea7e39405fba8185de153096bf95d), with `stale: false`.
- [`drop-content-limits.ts`](https://github.com/6529-Collections/6529seize-frontend/blob/c807f6da8efea7e39405fba8185de153096bf95d/helpers/waves/drop-content-limits.ts) defines and checks 25,000 UTF-16 units and 65,535 UTF-8 bytes per part and 50,000 UTF-16 units in total.
- [`Helpers.ts`](https://github.com/6529-Collections/6529seize-frontend/blob/c807f6da8efea7e39405fba8185de153096bf95d/helpers/Helpers.ts) sets the eight-file Storm budget.
- [`WaveLeaderboardGalleryItem.tsx`](https://github.com/6529-Collections/6529seize-frontend/blob/c807f6da8efea7e39405fba8185de153096bf95d/components/waves/leaderboard/gallery/WaveLeaderboardGalleryItem.tsx) selects the first media item in the first part and displays it in a square surface, using 450-pixel or 1,080-pixel image derivatives by viewport.
- [`WaveLeaderboardGridItemViewport.tsx`](https://github.com/6529-Collections/6529seize-frontend/blob/c807f6da8efea7e39405fba8185de153096bf95d/components/waves/leaderboard/grid/WaveLeaderboardGridItemViewport.tsx) uses the same first-part media rule. Both leaderboard treatments use `object-fit: contain`, so the complete cover remains visible.
- `https://api.6529.io/health` returned backend commit [`e1ca97c54d42f83c5f7bd613fcfa5a4476b93eb6`](https://github.com/6529-Collections/6529seize-backend/tree/e1ca97c54d42f83c5f7bd613fcfa5a4476b93eb6), with the database and Redis healthy. Its [OpenAPI contract](https://github.com/6529-Collections/6529seize-backend/blob/e1ca97c54d42f83c5f7bd613fcfa5a4476b93eb6/src/api-serverless/openapi.yaml) retains the optional title and per-part request model, while the application enforces the same text limits as the frontend.

Replace these pins when the relevant production implementation changes. A source observation never proves that production has deployed the same commit; the live preflight below remains mandatory.

## The leaderboard cover

The leaderboard cover is the first media item in the first Storm part. It is an editorial frontispiece, not a substitute image for any offered work.

Use a Museum-made typographic card when the source works are All Rights Reserved, when a montage would crop or recombine them, or when no single work should stand for the group. A collage may be used only when the Museum has a documented right to make and publish that derivative and the composition does not distort the proposal. Marketplace screenshots, rarity graphics, logos copied from third parties, and generative filler are inadmissible.

### Cover specification

- 1,600 × 1,600 pixels, opaque PNG, sRGB;
- essential text kept at least 200 pixels from every edge;
- title legible in a 267 × 267 pixel square without opening the drop;
- no more than four short typographic levels: proposal status, title, subtitle/date, institution;
- contrast of at least 4.5:1 for all essential text;
- no photograph crop, watermark removal, or unrecorded third-party mark;
- concise alternative text that identifies the card as a proposal cover;
- source SVG or other editable master retained beside the PNG;
- width, height, byte length, SHA-256, credit, and rights recorded in the Storm package.

The cover should be inspected at 1,600, 450, and approximately 267 pixels square. At the smallest size, the title must remain immediate and the subtitle may remain secondary. Fine print that survives only in the source file does not belong on the card.

## Sequence and reading rhythm

A proposed multi-work gift normally uses this sequence:

1. **Frontispiece and resolution.** Attach the cover first. Open with the proposed group title, one-sentence gift description, donor credit, exact voting unit, exact resolution, and a short account of the group.
2. **One part per work.** Attach the exact source image first, then give artist, title, date, source caption, credit, rights, close looking, relevant biography, and object citation.
3. **Synthesis and decision.** Present the affirmative case, the strongest countercase, a response where the contested issue requires one, rights/provenance/technical state, sources, and the identical resolution.

The first paragraph in part one must stand on its own in a compact preview. It should name the gift and establish its visual or historical proposition before discussing procedure. Every part should begin with content rather than navigation instructions.

The API drop title should be the shortest complete public name of the proposal. Do not add “vote now,” threshold language, donor promotion, serial numbers, or a subtitle already legible on the cover. A normal composer may submit `title: null`; the governed publication package therefore records the title explicitly and the posting readback must confirm it.

Write prose paragraphs as single physical Markdown lines and separate them with blank lines. Some Wave readers preserve soft line breaks, so hard-wrapped source prose produces erratic leading. Headings, field rows, credit lines, lists, tables, and quotations retain their semantic Markdown breaks.

## Text and media budget

Before sign-off, record exact counts from the publication sources:

- UTF-16 code units and UTF-8 bytes for every part;
- total UTF-16 code units and UTF-8 bytes across all parts;
- media count for every part and for the Storm;
- the ordered relation between each media file and the part that receives it.

The complete Storm must stay at or below 50,000 UTF-16 units and eight media files. Each part must stay at or below both 25,000 UTF-16 units and 65,535 UTF-8 bytes. The machine package records the exact metrics, and validation recomputes them from the raw source. Any source edit therefore invalidates the package until its metrics are regenerated. Do not shorten scholarship merely to create arbitrary unused capacity. Do edit repetition, throat-clearing, process language, and duplicated navigation. The opening and closing resolution are the deliberate exception: they repeat exactly so the decision cannot drift from the beginning to the end.

For a five-work gift, six images are an effective pattern: one cover plus one uncropped image for each work. The first media file is the cover. Work images follow in the exact object order declared by the candidate record.

## Rights, credit, and accessibility

The cover and every work image carry independent rights data. A Museum-made CC0 cover does not alter the rights status of the photographs it introduces. An upstream image exposed by the artist, publisher, or token metadata may be used only on the basis recorded for that proposal; its availability is not a copyright transfer, preservation deposit, or general reuse grant.

Each image requires:

- useful alternative text based on visible content;
- artist or maker where applicable;
- title or identifying caption;
- date where known;
- source credit and copyright notice;
- the controlled rights label used by the object record;
- the exact source or local asset relation in the machine package.

Alternative text describes the image needed to follow the proposal. It does not repeat the surrounding essay, speculate about identity or motive, or convert a source caption into visible fact.

The current drop-media request does not expose a dedicated alternative-text field. The repository nevertheless retains the canonical `alt_text` for future clients and records. In the live Storm, the first prose following each image must supply an equivalent close visual description before relying on historical interpretation. Never imply that an inaccessible client field has been populated when it has not.

## Pre-publication gate

No operator begins the live posting flow until the proposal owner has approved the exact source edition and cover. The final check uses the merged Museum commit, not a working tree or pull-request preview.

1. Confirm the Wave ID, name, type, credit type, threshold, hold duration, open/closed state, and the posting profile's eligibility from the live authenticated API.
2. Confirm that production serves the text-limit implementation recorded by the package or a compatible successor. Recheck all three text ceilings from source and, where the release is recent, from boundary-qualified production evidence.
3. Run the complete Museum validator and deterministic manifest check against the merged source commit.
4. Verify all part counts, the 50,000 total, the eight-file total, contiguous numbering, exact repeated resolution, object order, media joins, alternative text, credit, rights, dimensions, bytes, and SHA-256.
5. Open the cover at 1,600, 450, and approximately 267 pixels square. Check title legibility, edge safety, color, and contrast.
6. Open every work image uncropped and compare it with the governed URI and recorded SHA-256.
7. Prepare a dry-run publication plan naming the posting profile, Wave, part order, media order, source commit, and expected first-screen text. Do not include wallet secrets, auth tokens, local paths, or private donor data.
8. Obtain explicit final authorization to post this exact edition. Approval to draft, research, or open a pull request is not approval to publish.

## Publication and readback

Publish all parts as one Storm so the parent drop remains the single voting object. Use the authorized profile and preserve the declared donor credit separately from the posting identity. Do not vote as part of publication unless the user gives a separate instruction to vote.

Immediately after submission:

1. read the drop through the authenticated API;
2. record drop ID, serial number, posting profile, timestamp, part count, media count, and live status;
3. compare every returned part with the merged Markdown source in order;
4. verify that part one media item one is the cover and that each work image appears on the intended part;
5. inspect list, grid, content-only, full-drop, and mobile presentations;
6. check that the cover is legible, work images are uncropped, credits are visible, text rhythm is intact, navigation reaches all parts, and voting attaches to the parent drop;
7. retain screenshots of the leaderboard and opened Storm as publication evidence;
8. update the proposal record through an append-only repository change. Record the live status observed at a stated time; do not infer selection from votes or labels.

If publication is incomplete or materially wrong, stop promotion of the link and preserve the returned drop identity. Correct the public record through the Wave's available correction mechanism and an append-only repository amendment. Never silently replace the historical source edition.

## Magnum Photos 75 first application

`6529NM-PG-2026-001`, *Conflict at Its Edges: Five Photographs of Evidence and Aftermath, 1952–2016*, uses a Museum-made square title card as its leaderboard cover. The five All Rights Reserved photographs remain uncropped and appear one per work part. The complete seven-part text is the generated voter dossier; no abridged parallel edition is needed under the supported profile.

This package remains unsubmitted until the donor approves the final manuscript and cover, the source edition is merged, the live Wave and chain observations are refreshed, and the explicit posting instruction is given.
