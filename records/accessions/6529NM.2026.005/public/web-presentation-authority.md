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
- **Pause and stop.** The control that returns to the still is keyboard-operable, visible while the animation plays, and stops playback immediately.
- **Reduced motion.** When the visitor's system requests reduced motion, nothing starts automatically, viewer transitions are also suppressed, and the play control's label repeats the warning.
- **Size cap.** Show the animation no larger than 768 CSS pixels on each side, and size the player as `min(768px, 100%)` of its container so that browser zoom cannot push it past the viewport. The cap keeps the animation within the WCAG 2.3.1 limit at 200 percent browser zoom, where a 768-pixel image is the equivalent of 1,536 pixels (24.3 percent, against a limit of 25 percent). A larger size requires a new flash review.
- **No full screen or zoom for the animation.** Do not play the animation full screen, in a zoom viewer, or enlarged. This rule is a work-specific exception to §7.4 of the public museum experience standard, which asks for fullscreen viewing. The still may be shown at any size, including full screen and zoom.
- **Uncropped.** Never crop the image to fit a card or frame; letterbox it instead.

Warning text:

> **Flashing imagery.** When played, this animation flickers continuously: black-and-white streaks and bright mint-green outlines flash up to ten times a second, and a large pink area changes color twenty times a second. It may affect people with photosensitive epilepsy or other sensitivity to flashing light.

XCOPY's Nifty Gateway creator profile, as captured in 2025, read "Warning: flashing imagery."[^1]

## Flash analysis

The Museum's analysis applies the WCAG 2.2 general-flash and red-flash definitions to the exactly decoded source frames. This is the Museum's computation under the WCAG definitions, not a certified photosensitive-epilepsy test. About 5.5 percent of the image flashes more than three times a second, so the work does not meet WCAG 2.3.2 at any size. Under WCAG 2.3.1 the deciding factor is the largest share of a 10-degree visual field that flashes at once:[^2]

| Image size on screen | Largest flashing share of a 10-degree field | Within the 25 percent limit |
|---|---|---|
| 512 px | 12.2 percent | yes |
| 640 px | 15.2 percent | yes |
| 768 px | 15.3 percent | yes |
| 1,024 px | 17.1 percent | yes |
| 1,280 px | 20.2 percent | yes |
| 1,536 px | 24.3 percent | yes, narrowly |
| 2,048 px | 30.2 percent | no |
| 4,000 px (full size) | 54.1 percent | no |

Red flashes cover at most 0.5 percent of a 10-degree field at 768 pixels. The pink band's color change is the largest visible change, about a tenth of the image on every frame, and stays below the WCAG luminance and red-flash criteria.

## Source and derivatives

The source is the GIF the token names by IPFS hash `QmTcTzTPgCyvF933oeFvB4GkPgaXtF6dKuQgvg32qqLYGF`: 4,000 × 4,000 pixels, 4,541,937 bytes, SHA-256 `3ba2c6c6a7b7da940b5780da8fe301e61366a0b5c738be16e537ee122630be2e`, eight frames of 50 milliseconds, looping without end. On 18 October 2026 the copies served by the Nifty Gateway CDN and by an IPFS gateway were byte-identical, and the identifier the Museum recomputed from those bytes matched the token's hash.[^2] The CDN address in the token metadata is a mutable location; the IPFS hash binds the file.

The GIF is the reference file. Still WebP derivatives of the first frame at 640, 1,280, and 2,400 pixels are display surrogates. An animated access copy must be the source GIF or a lossless copy of its frames; any lossy or resized animated copy requires its own flash measurement before use. The fixity, dimensions, transform, source relationship, alt text, and rights statement of every derivative are recorded in `presentation-manifest.json`. The reviewed alt text, long description, and motion note are in [Alt text](alt-text.md).

## Rights basis

XCOPY applied a CC0 dedication to all existing work on 1 August 2022, about four months after *MAX PAIN* was released.[^3] The artist's Legal & Privacy page states that XCOPY artworks are released under CC0 and may be used, remixed, reproduced, exhibited, or built upon without permission.[^4] The token metadata carries no license. The Museum asserts no copyright in the work. It records CC0 1.0 as the basis for reproducing, displaying, and describing the work, and for making access and preservation copies.

The same page states that independent projects, exhibitions, and derivative works using XCOPY's work do not imply affiliation with or endorsement by XCOPY unless stated.[^4] The Museum's presentation is independent of the artist and implies no endorsement by XCOPY.

## Notes

[^1]: XCOPY's creator profile in the Nifty Gateway drop data, [Wayback Machine snapshot of 5 September 2025](https://web.archive.org/web/20250905032040/https://www.niftygateway.com/marketplace/collection/0xd1169e5349d1cb9941f3dcba135c8a4b9eacfdde/1/) (class B). The capture does not show who wrote the profile text or when.
[^2]: Museum condition and technical record `6529NM.2026.005.COND.01`, including the flash analysis of the source GIF, 18 October 2026 (class C). The analysis, its flash masks, and its method are retained in `evidence/xcopy-max-pain-4188-display/`. Sizes up to 1,536 pixels were measured on the flash mask resampled to that size; the 640 and 1,280 pixel rows and sizes of 2,048 pixels and above on a 1,000-pixel coverage grid with the 341 × 256 pixel window scaled to match. The two methods agree within 0.1 percentage point at 768 and 1,536 pixels.
[^3]: XCOPY (@XCOPYART), [post on X, 1 August 2022](https://x.com/XCOPYART/status/1554112748816109569), read through a public mirror of the post (class B).
[^4]: XCOPY, [Legal & Privacy](https://xcopy.art/privacy), observed 18 October 2026 (class B). See also XCOPY, [Creative Commons](https://xcopy.art/creative-commons).
