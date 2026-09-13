# Technical and condition review

**Constructed:** 13 September 2026 · Independent intake review approved

The six objects are ERC-721 tokens associated with static JPEG photographs.
Their presentation does not require a generative program, animation or user
interaction. The source files all decode successfully. Five measure
3543 × 2362 pixels; token 2216 measures 3543 × 5315 pixels. Each has RGB
encoding, EXIF orientation 1 and the same embedded Adobe RGB (1998) profile.

The image and metadata hashes agree with the retained August proposal files.
Fresh metadata retrieval on September 13 returned matching metadata bytes
for all six. The JPEG checks used retained source files. A fresh image
retrieval exceeded the guarded fetcher's response-size profile; this is not
reported as a failed image or as a fresh source download.

## Identity and custody

The successful gift transfer is transaction
[`0xd1c9986c…fc3808`](https://etherscan.io/tx/0xd1c9986c1e885a5c29b03eb15ef5194ae890678ebf6d0ab84d607af8affc3808),
block 25970845, 13 September 2026 at 20:15:35 UTC. Exact logs identify
tokens 226, 1117, 2059, 2216, 2768 and 4697 from the donor's address to
Museum custody. At finalized block 25971024, hash
`0x1fdc3989d9b07cd1bd2c48811da35e3ffcd676f30d02424ea57e759c8b85eed9`,
all six `ownerOf` results match the Museum and all token-specific approvals
are zero. The Museum ENS name resolves to the same custody address. The
pinned block hash was checked again after the technical reads.

The provenance package verifies 25 distinct successful transaction receipts
and their canonical block hashes. For each token, the indexed transfers form
a continuous address sequence from mint to Museum receipt. The indexer's
pagination was exhausted. This supports the recorded sequence; it is not a
separate full-range log search or proof of off-chain legal title at every step.

## Contract and metadata authority

The contract delegates to implementation
`0x659d80ce8ac5cad5ab2fdd7137caf3d06d246289`. The retained verified source
identifies `Creator721Proxy` and `ERC721CreatorImplementation`. The proxy
initializes its implementation in the constructor. Its examined source and
ABI expose no public upgrade entry point. The presence of upgradeable library
names alone would not establish an available upgrade mechanism.

Metadata remains subject to defined authorities. The implementation's
`adminRequired` modifier admits its owner or registered admins. Base-token
URI setters and prefixes are available to those actors. Token 1117, 2059,
2768 and 4697 return “No extension for token” from `tokenExtension`, consistent
with the base path in the verified implementation. Tokens 226 and 2216 return
the registered extension `0x55a989449cc4330132a0b064d1a16ce9325c9452`.
The creator core permits extension-specific URI operations and permits
administrative blacklisting that can make extension metadata inaccessible.

The extension endpoint supplied creation/runtime bytecode without verified
source or an ABI in this retrieval. Its internal permission structure is
therefore not characterized here. The observed URI and source bytes remain
verified independently of that gap. The record does not describe the metadata
of any of the six tokens as unchangeable.

The optional `totalSupply()` call reverted. The announced 5,000-photograph
edition is a publisher statement, not a supply count established by this call.

## Photographic metadata and condition

Decoded dimensions take precedence over different image-dimension values in
the EXIF IFD. The original-date fields are camera metadata without a timezone;
the 2022 Photoshop modification fields concern later file processing. The
issuer date-code suffixes differ from the EXIF months, so the catalogue records
the corroborated years and retains the codes without expanding them into dates.

Full-frame visual examination found legible images with continuous composition.
Token 226 was examined through the native source image; the other five were
examined through 1600-pixel full-frame inspection copies because the image-view
transport rejected the larger source files. Full JPEG decode is a separate
completed check. The examination is not a comparison against camera originals,
physical prints or every source pixel.

The final construction check also examined all six 1280-pixel, full-frame,
colour-managed display copies. This pass corrected the earlier description
of token 226; the revised entry describes the verified forest image. The
separate Ultra reviewer subsequently checked the six image-to-description
joins. Neither pass is represented as a visual comparison of every source
pixel or against camera originals.

The source manifestations are usable for display. Two regional source-package
restorations and byte-identical regeneration of all 18 display copies are
documented in the [preservation record](display-and-preservation.md). Binding
Museum review and continuing observation of metadata authority and retrieval
dependencies remain separate. No additional donor rights information is
listed as a condition.
