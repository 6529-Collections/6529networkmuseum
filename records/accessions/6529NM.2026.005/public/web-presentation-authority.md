---
record_id: 6529NM.2026.005.DISPLAY-01
status: active
accession_number: 6529NM.2026.005
object_id: 6529NM.2026.005.01
---

# Web presentation authority: *MAX PAIN* #4188/7394

The Museum's public presentation is authorized to show a still poster made from the first frame of the token's GIF (frame 0 in the technical record) and, at a visitor's request, the eight-frame animation. Display the work square and uncropped. Display credit:

> XCOPY, *MAX PAIN #4188/7394*, 2022. Ethereum token `eip155:1/erc721:0xd1169e5349d1cb9941f3dcba135c8a4b9eacfdde/171000104188`. Acquired through a community-funded purchase organized by Shelby and authorized by the 6529 Network Museum Wave, 2026. CC0 1.0.

## Display rules

The animation flashes, so its presentation follows these rules on every Museum page, card, and preview:

- **Poster first.** The first image a visitor sees is the still. Label it as one frame of an eight-frame animation. Thumbnails, collection cards, and social images use the still.
- **No autoplay.** The animation never starts on page load, on scrolling into view, on hover, or in a card or preview. A GIF placed in an ordinary image element animates as soon as it loads, so load the animated file only after the visitor activates it.
- **Play on request, with a warning.** Show the warning text before activation, beside the play control, and not in a dialog that appears afterward. Give the play control the accessible name "Play flashing animation".
- **Stop.** While the animation plays, a visible, keyboard-operable control stops it immediately and returns to the still.
- **Reduced motion.** When the visitor's system requests reduced motion, show the still only, do not offer the animation, and suppress viewer transitions.
- **Size cap.** Show the animation no larger than 512 CSS pixels on each side, and size the player as `min(512px, 100%)` of its container. At 200 percent browser zoom a 512-pixel image is the equivalent of 1,024 pixels, where the largest flashing share of a 10-degree field is 24.9 percent under the stricter reading below, within the 25 percent limit. Greater zoom or screen magnification enlarges the flashing area further, and the warning says so. A larger size requires a new flash review.
- **No full screen or zoom for the animation.** Do not play the animation full screen, in a zoom viewer, or enlarged. This rule is a work-specific exception to §7.4 of the public museum experience standard, which asks for fullscreen viewing. The still may be shown at any size, including full screen and zoom.
- **Verified bytes only.** Play only bytes whose SHA-256 matches the retained GIF: the copy addressed by the token's IPFS hash or a Museum-retained copy. Never play the mutable Nifty Gateway address in the token metadata.
- **Uncropped.** Never crop the image to fit a card or frame; letterbox it instead.

Warning text:

> **Flashing imagery.** When played, this animation flickers continuously: black-and-white streaks and bright mint-green outlines flash up to ten times a second, and a large pink area changes color twenty times a second. Zooming in or screen magnification makes the flashing area larger. It may affect people with photosensitive epilepsy or other sensitivity to flashing light.

XCOPY's Nifty Gateway creator profile, as captured in 2025, read "Warning: flashing imagery."[^1]

## Flash analysis

The Museum's analysis applies the WCAG 2.2 general-flash and red-flash definitions to the exactly decoded source frames at each of the eight frame steps of the loop. This is the Museum's computation under the WCAG definitions, not a certified photosensitive-epilepsy test. About 5.5 percent of the image flashes more than three times a second, so the work does not meet WCAG 2.3.2 at any size. Under WCAG 2.3.1 the deciding factor is the largest share of a 10-degree visual field that flashes at once. The table gives two readings: the pixels that change enough to flash at one step and also flash more than three times a second, and, more strictly, every pixel that changes enough to flash at that step.[^2]

| Image size on screen | Pixels flashing more than three times a second | Every pixel with a flash-sized change | Within the 25 percent limit |
|---|---|---|---|
| 512 px (the cap) | 13.1 percent | 15.3 percent | yes |
| 640 px | 15.8 percent | 18.7 percent | yes |
| 768 px | 16.5 percent | 19.6 percent | yes |
| 1,024 px (512 px at 200 percent zoom) | 20.6 percent | 24.9 percent | yes, narrowly |
| 1,280 px | 21.9 percent | 29.3 percent | no, under the stricter reading |
| 1,536 px | 26.5 percent | 33.4 percent | no |
| 2,048 px | 36.1 percent | 44.9 percent | no |
| 4,000 px (full size) | 66.8 percent | 77.5 percent | no |

Each figure is the largest over the eight frame steps and over landscape and portrait 10-degree fields. Red flashes cover at most 0.6 percent of a 10-degree field at 512 pixels and 1.4 percent at 1,024 pixels. The pink band's color change is the largest visible change, about a tenth of the image on every frame, and stays below the WCAG luminance and red-flash criteria.

## Source and derivatives

The source is the GIF the token names by IPFS hash `QmTcTzTPgCyvF933oeFvB4GkPgaXtF6dKuQgvg32qqLYGF`: 4,000 × 4,000 pixels, 4,541,937 bytes, SHA-256 `3ba2c6c6a7b7da940b5780da8fe301e61366a0b5c738be16e537ee122630be2e`, eight frames of 50 milliseconds, looping without end. On 18 October 2026 the copies served by the Nifty Gateway CDN and by an IPFS gateway were byte-identical, and the identifier the Museum recomputed from those bytes matched the token's hash.[^3] The CDN address in the token metadata is a mutable location; the IPFS hash binds the file.

The GIF is the reference file. Still WebP derivatives of the first frame at 640, 1,280, and 2,400 pixels are display surrogates. An animated access copy must be the source GIF or a lossless copy of its frames; any lossy or resized animated copy requires its own flash measurement before use. The fixity, dimensions, transform, source relationship, alt text, rights statement, and display constraints of every derivative and of the animation are recorded in `presentation-manifest.json`. The reviewed alt text, long description, and motion note are in [Alt text](alt-text.md).

## Rights basis

XCOPY applied a CC0 dedication to all existing work on 1 August 2022, about four months after *MAX PAIN* was released.[^4] The artist's Legal & Privacy page states that XCOPY artworks are released under CC0 and may be used, remixed, reproduced, exhibited, or built upon without permission.[^5] The token metadata carries no license. The Museum asserts no copyright in the work. It records CC0 1.0 as the basis for reproducing, displaying, and describing the work, and for making access and preservation copies.

The same page states that independent projects, exhibitions, and derivative works using XCOPY's work do not imply affiliation with or endorsement by XCOPY unless stated.[^5] The Museum's presentation is independent of the artist and implies no endorsement by XCOPY.

## Notes

[^1]: XCOPY's creator profile in the Nifty Gateway drop data, [Wayback Machine snapshot of 5 September 2025](https://web.archive.org/web/20250905032040/https://www.niftygateway.com/marketplace/collection/0xd1169e5349d1cb9941f3dcba135c8a4b9eacfdde/1/) (class B). The phrase is retained with its byte offset in the same captured bytes as the source evidence's drop-page record, in `evidence/xcopy-max-pain-4188-supplement/citations/nifty-gateway-creator-profile.json`. The capture does not show who wrote the profile text or when.
[^2]: Museum flash analysis of the source GIF at all eight frame steps, 18 October 2026, `evidence/xcopy-max-pain-4188-display/flash-analysis-all-steps.json`, with its method and summary in `evidence/xcopy-max-pain-4188-display/addendum-01-summary.json` (class C); summarized in the condition and technical record `6529NM.2026.005.COND.01`. Flash masks were resampled to each size (to a 2,000-pixel grid, with the window scaled, at full size) and searched with a one-pixel step for 341 × 256 and 256 × 341 pixel windows, the 10-degree field on a 1,024 × 768 reference screen. These figures supersede the Museum's earlier measurement of two of the eight steps, which is retained in the same folder.
[^3]: Museum source evidence, `evidence/xcopy-max-pain-4188-sources/manifest.json`, and condition and technical record `6529NM.2026.005.COND.01`, 18 October 2026 (class C).
[^4]: XCOPY (@XCOPYART), [post on X, 1 August 2022](https://x.com/XCOPYART/status/1554112748816109569), read through a public mirror of the post (class B).
[^5]: XCOPY, [Legal & Privacy](https://xcopy.art/privacy), observed 18 October 2026 (class B). See also XCOPY, [Creative Commons](https://xcopy.art/creative-commons).
