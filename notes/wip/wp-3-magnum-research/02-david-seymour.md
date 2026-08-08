# WP-3 research memo: David Seymour, Magnum Photos 75 #127

Research completed 2026-08-08 UTC. This is a bounded research memo for the
candidate object in `6529NM-PG-2026-001`; it is not an accession, acceptance,
title, custody, or rights-clearance record.

## Working conclusion

The local proposal package and the public David Seymour estate record identify
the same vertically composed black-and-white frame: a person seen from behind
with a long firearm in the foreground, a low light-coloured tent or canopy,
rocky terrain, and eroded high ground. The local token metadata gives the
issuer/archive title and number as **David Seymour, “Patrolling the border
between the Negev Desert and Jordan,” 1952, `SED1952003W00003/23`**. The estate
publishes a visually matching file as `PAR116258.jpg` with the fuller place
caption **“The King Solomon's Mines area, Israel, 1952.”** No public source found
for this memo cross-indexes `PAR116258` to the Magnum archive number.

The 1952 date, Negev/Israel place, title/caption, and Magnum 75 token identity
are well supported at caption/issuer level. The exact day, coordinates, person,
unit, assignment, commissioner, first publication, original negative/contact
sheet, and the correspondence between the estate and Magnum identifiers remain
unresolved. The 1949 Israel–Jordan armistice documents and 1952 UN border
reports provide historical setting, but do not prove that this particular frame
shows a named incident or a marked boundary.

## Exact local proposal and token-linked media

Source: local primary package, `records/proposed-gifts/6529NM-PG-2026-001/proposal.json`,
object `6529NM-PG-2026-001.OBJ-001`, read 2026-08-08 UTC.

| Field | Local package value | Evidence note |
|---|---|---|
| Chain identity | `eip155:1/erc721:0xe628b59d34f42b16c53f4d697f1ffd4d8d987b91/127` | Candidate object identity in the constructed proposal; not an accession identity. |
| Artist | David Seymour | Local issuer metadata/proposal field. |
| Title | *Patrolling the border between the Negev Desert and Jordan* | Local proposal and token metadata; the estate uses the same title with a fuller place phrase. |
| Date/place | 1952; Negev, Israel | Local metadata attributes and proposal fields. No day or coordinates. |
| Archive number | `SED1952003W00003/23` | Local token metadata/proposal field; public Magnum crosswalk not located. |
| Edition/sequence | 1 of 1; `127/225`; curation `2/3` | Local token metadata. The proposal’s card title is “David Seymour — Magnum 75 #127.” |
| Metadata URI | <https://arweave.net/fHJAhfhIB7wTpz0my7K9-b9mWDq-fpk5Yr57gqsf_pM> | Fresh HTTP fetch on 2026-08-08 returned 2,665 bytes; SHA-256 matched the local declaration `sha256:b1c52d7cfa7ac198c08051d91a3a2e62d9260dbacbafdc7a4fd71cce0d311178`. |
| Image URI | <https://arweave.net/VE0zO2N1zVTsbEUHdUFazEgvuMbmVOi6OfaWfQOWkaM> | Fresh HTTP fetch on 2026-08-08 returned 2,518,674 bytes; SHA-256 matched `sha256:65abf8b6a182bb641787a43b40d10f0b6471357e5c90777aacccf9eb73ea1453`. |
| Image details | JPEG, 3,056 × 4,600 pixels | Matches the `image_details` object in the fetched token metadata and the local proposal. |
| Retention status | `upstream_not_retained` | The repository records the URL and fixity but does not retain the upstream photograph bytes. The fetch is a verification observation, not a preservation master. |

The fetched token metadata states that Magnum 75 was created in 2022 for the
agency’s 75th anniversary year, brings together 225 images across three
curations, and says the second curation was made in dialogue with Azu Nwagbogu.
Those are issuer/project statements in the token metadata, not evidence about
the 1952 assignment or first publication.

The local proposal’s rights fields state `© David Seymour/Magnum Photos 2022
All Rights Reserved`, `license: All Rights Reserved`, and
`token_transfer_rights_effect: no_copyright_or_reproduction_grant_asserted`.
The same fetched metadata contains an attribute named `License` with value
`David Seymour`; that value is not a usable public license and conflicts in
meaning with the proposal’s “All Rights Reserved” field. Retain both until the
issuer’s terms and rights chain are independently documented. The metadata
links to <https://www.magnumphotos.com/terms-conditions/>; that page was not
accessible during this research (HTTP 403), so no broader permission is inferred.

The local proposal also records a constructed Wave status (`PARTICIPATORY` for
drop `002bfa4f-8416-48bf-b35e-38f354e9a9f0`, serial `1276093`) and says Magnum
Photos 75 is not in the adopted preapproved-collection register. This memo
makes no selection, acceptance, title, donor-authority, transfer, or accession
claim.

## Image verification and visible facts

Evidence class C, Museum-generated technical observation, 2026-08-08 UTC:

- The token-linked JPEG was fetched from the recorded Arweave URI, hashed, and
  visually inspected at its full portrait orientation.
- The frame is black and white and vertically composed. A person occupies the
  lower foreground, seen from behind/side with the face not visible. A long
  firearm and sling/harness dominate the central foreground. Partial dark or
  cropped forms appear at the lower left and lower right edges.
- Beyond the person is a low, pale, tent-like or canopy-like structure, a dirt
  track/open ground, loose rock, and layered, eroded hills or escarpments. A
  thin vertical pole or line is visible near the middle-left area.
- No face, name, insignia, flag, border marker, map, unit marking, or other
  scene-internal identifier is legible. “Patrolling,” “border,” “Negev,”
  “Jordan,” “Israel,” and “King Solomon’s Mines area” are caption/context
  claims, not visual identifications made from the pixels alone.

The estate image at
<https://davidseymour.com/wp-content/uploads/2019/03/PAR116258.jpg> was fetched
and inspected as a separate source: 598 × 900 pixels, 138,069 bytes, observed
SHA-256 `sha256:1e7d43a178ad02f259a78fe769906615c8ea3f92159e165f30f56cc2f2f14a11`.
It has the same composition and visible arrangement as the token-linked image.
This establishes a strong visual match, not byte identity, a documented
negative-to-token chain, or proof that the two files were generated from the
same intermediate.

## Caption, place, and historical setting

Evidence class B, artist-estate/public institutional records:

- The David Seymour estate’s photo album labels the frame “Patrolling the
  border between the Negev Desert and Jordan. The King Solomon's Mines area,
  Israel, 1952” and exposes the file as `PAR116258.jpg`:
  <https://davidseymour.com/photo-album/>.
- The local token metadata uses the shorter location “Negev,” country “Israel,”
  and the archive number `SED1952003W00003/23`. The estate page does not publish
  that archive number or a cross-reference to the token.
- A contemporary 6 May 1952 Jewish Telegraphic Agency report records an
  Israeli government agreement with a Belgian firm concerning copper-mining
  equipment in the Negev and refers to the “fabulous copper mines of King
  Solomon”: <https://www.jta.org/archive/israel-signs-agreement-with-belgian-firm-on-copper-mining-equipment>.
  This is useful period context for the estate’s place phrase; it is not
  evidence that this frame shows the mining works, nor evidence of Seymour’s
  assignment.
- The UN’s 3 April 1949 Israel–Jordan General Armistice Agreement states that
  the Armistice Demarcation Line was a military line, not a final peace
  boundary; its southern sector was to follow existing military positions
  surveyed by UN observers and delineated on the annexed map:
  <https://www.un.org/unispal/document/auto-insert-189953/>. The agreement also
  prohibited armed forces from crossing the line and preserved restrictions on
  civilian crossing.
- The UN Truce Supervision Organization report for the period ending 30 October
  1952 records a 18 September 1952 incident in which an Israeli survey team
  marking the border was fired on from Jordan-controlled territory. It states
  that the parties had not jointly placed markers and that the Mixed Armistice
  Commission treated the incident as a serious breach:
  <https://www.un.org/unispal/document/auto-insert-210818/>. The report also
  records other 1952 armed incidents. These records establish an unsettled
  armistice-demarcation setting, not the event pictured here.
- The U.S. Department of State’s contemporaneous diplomatic record describes the
  later regional situation as involving “troublesome demilitarized zones,” a
  “tangled and unsatisfactory boundary situation,” and serious border incidents:
  <https://history.state.gov/historicaldocuments/frus1952-54v09p1/d732>.
  This is contextual evidence, not a caption for the photograph.

## David Seymour: biography and practice relevant to this image

Evidence class B, issuer and institutional biography:

- Magnum’s official store profile identifies David Szymin (1911, Warsaw), his
  1930s work in Paris, his 1947 founding role in Magnum with Cartier-Bresson,
  Capa, Rodger, and Vandivert, his UNICEF commission on children in 1948, his
  photography of the emergence of Israel, and his presidency of Magnum after
  Capa’s death: <https://store.magnumphotos.com/collections/david-seymour>.
- ICP describes him as Chim, notes his work for leftist magazines, the Spanish
  Civil War, postwar reconstruction, the birth of Israel, and a humanistic
  approach to wartime subjects: <https://www.icp.org/exhibitions/chim-photographs-by-david-seymour>.
- ICP’s *We Went Back* press release says he traveled regularly to Israel from
  1951 to document the new country and the lives of settlers, while also working
  on assignments for international magazines and special projects. It calls
  the wider practice thoughtful reportage in which informative detail can carry
  metaphor: <https://www.icp.org/sites/default/files/exhibition/credits/sites/default/files/exhibition_pdfs/icp_chim_wewentback_press.pdf>.
- The estate-hosted essay “Close Enough,” by Terry Gips, explicitly discusses
  this border-patrol image as an example of a “muscular soldier” and argues that
  Seymour’s frames often make meaning arise without a fully spelled-out
  narrative. This is an estate-hosted critical interpretation, not a primary
  caption or artist statement: <https://davidseymour.com/writings-on-close-enough/>.

The relevant practice link is therefore secure at the level of a sustained
Israel project and Seymour’s humanistic/reportorial method. It is not secure at
the level of this image’s particular commission, publication outlet, or named
subject. The estate’s album places the frame among other Israel photographs
from 1951–1953, including sentry duty, a Nahal kibbutz, Independence Day, and a
border-incident funeral. That grouping is a research lead, not proof of one
assignment or a single original sequence.

## Assignment, publication, caption, and adjacent-sequence leads

| Question | Current evidence | Boundary / next correspondence |
|---|---|---|
| Capture date | Token metadata and estate caption: 1952 | No day or itinerary. |
| Location | Negev, Israel in token metadata; King Solomon’s Mines area in estate caption | No coordinates or public scene-level map; do not collapse “Negev” into a specific Timna site without a source. |
| Assignment/commissioner | ICP establishes regular Israel travel from 1951 and general magazine/special-project assignments | No source ties this frame to a named outlet, commissioner, or assignment. |
| First publication | Not established | Do not infer *Life*, *Paris-Match*, a Magnum magazine story, or a book from Seymour’s other 1952 Israel images. |
| Caption history | Token: shorter title/location; estate: fuller place caption; local public dossier: “Negev, Israel” | Obtain Magnum caption sheet, estate negative/print record, and any period publication caption. |
| Contact sheet/negative | Not located | Request the Magnum archive record for `SED1952003W00003/23` and the estate record for `PAR116258`; ask whether `/23` identifies a frame, print, or internal archive position. |
| Related publications | *Israel: 50 Years as Seen by Magnum Photographers* (Aperture, 1998) is a catalogue-level lead with David Seymour, Negev, Jordan, and Israeli-army terms in the bibliographic record; it does not establish this frame’s inclusion: <https://books.google.com/books/about/Israel.html?id=mVQpAQAAIAAJ>. Carole Naggar’s 2022 biography has a chapter “I Found a Home: Israel, 1951–1955,” but exact image inclusion was not verified: <https://doi.org/10.1515/9783110706345>. | Inspect the physical/digital books and picture indexes before citing reproduction or publication. |
| Archival holdings | LOC’s David Seymour collection includes 1,093 gelatin-silver prints, is arranged partly by country, and says publication may be restricted; the matching item was not located in this pass: <https://www.loc.gov/pictures/item/2024634496/>. ICP also reports a large Chim holding and archive. | Search Israel/Negev portfolios and contact sheets through LOC, ICP, Magnum, and the estate. |

## Rights and media boundary

The local proposal and token-linked metadata provide a notice and a project
rights label, not a complete rights determination. The strongest current
statement is “© David Seymour/Magnum Photos 2022 All Rights Reserved”; the
proposal expressly says token transfer does not assert a copyright or
reproduction grant. The token’s `License: David Seymour` attribute must not be
treated as a license. The current Magnum terms URL was inaccessible (403) and
the launch-period archived terms URL was not independently retrieved. No
copyright transfer, reproduction permission, exhibition permission, preservation
permission, or AI-training permission is established here.

The token-linked JPEG and estate JPEG were fetched solely for verification and
visual comparison. The Museum repository retains neither source photograph as
a preservation master. The local `upstream_not_retained` status remains correct;
hashes identify the observed bytes but do not make them recoverable or licensed.
The Library of Congress rights advisory likewise warns that publication may be
restricted and that the Library does not own rights to material in its
collections. Any later Museum use needs a component-specific rights review and
an approved media source.

## Concise object-level essay notes — Museum interpretation (E)

The photograph makes a border legible without showing a line. The armed figure
is turned away from the viewer and toward the tent and eroded terrain, so the
image’s force comes from a posture of watchfulness rather than from an event
visible in the frame. The firearm is both an instrument of security and the
visual hinge that joins body, shelter, road, and landscape. The caption supplies
the geopolitical claim; the image supplies an encounter with uncertainty.

The estate’s fuller “King Solomon’s Mines area” caption places the frame between
postwar border vigilance and the Negev’s mining/settlement imagination, while
the token’s shorter “Negev, Israel” label leaves that historical association
open. That difference is productive for close looking but must remain a
caption discrepancy, not a curatorial fact about the site. The absent face and
unmarked terrain also make the photograph a case study in how an archive’s
caption carries identity and location that the image alone cannot securely
provide.

## Unresolved correspondence questions

1. Can Magnum or the Seymour estate formally connect `SED1952003W00003/23` to
   `PAR116258`, and what does each segment of the archive number mean?
2. Is “King Solomon’s Mines area” a precise Timna/Arabah location, a wider
   regional caption, or a place description inherited from a period print?
3. What was the exact date, route, assignment, commissioner, and first outlet?
   Was the frame part of a published Israel story or only an archive/print
   selection before the 2022 Magnum 75 release?
4. Does a contact sheet, negative sleeve, print verso, or caption sheet name the
   person, his unit/role, the structure, or the patrol route? The image itself
   does not.
5. What is the authoritative 2022 rights/terms record, and what does the
   metadata attribute `License: David Seymour` mean in issuer practice?
6. Were there crops, tonal variants, or period print dimensions before the
   token-linked JPEG? The two public JPEGs match visually but are not byte-
   identical evidence of a common master.

## Explicit evidence boundary

- **Established:** token-linked CAIP-19 identity, token sequence/edition,
  issuer metadata URI and fixity, image URI/fixity/dimensions, local rights
  notice, estate caption/file, visual match, Seymour biography/practice, and
  general 1949–1952 Israel–Jordan armistice context.
- **Not established:** accession, acceptance, donor authority, title passage,
  Museum custody, copyright transfer, any reproduction/display license, exact
  geographic coordinates, exact day, person/unit identity, original assignment,
  first publication, contact-sheet relationship, or negative provenance.
- **Source accessibility:** the official Magnum photographer profile and terms
  pages returned 403 in this pass; the relevant UN pages were discoverable but
  also returned 403 on direct open. Their URLs and the unresolved access limits
  are retained above rather than replaced with an inference.

## Source register

All web sources below were accessed or attempted on 2026-08-08 UTC.

| Source | Type | Use / status |
|---|---|---|
| `records/proposed-gifts/6529NM-PG-2026-001/proposal.json` and `wave-storm.json` | Local primary Museum package | Exact candidate fields, hashes, rights notice, proposal boundary, and observed chain/proposal state. |
| <https://arweave.net/fHJAhfhIB7wTpz0my7K9-b9mWDq-fpk5Yr57gqsf_pM> | Issuer-linked primary metadata | Fresh 200 fetch; raw 2,665-byte SHA-256 matched local fixity. |
| <https://arweave.net/VE0zO2N1zVTsbEUHdUFazEgvuMbmVOi6OfaWfQOWkaM> | Issuer-linked primary media | Fresh 200 fetch; raw 2,518,674-byte SHA-256 matched local fixity; visual observation only. |
| <https://davidseymour.com/photo-album/> and `PAR116258.jpg` | Artist-estate authoritative archive/publication | Exact fuller caption and visually matching frame; no Magnum-number crosswalk. |
| <https://store.magnumphotos.com/collections/david-seymour> | Magnum official profile/store | Biography, Magnum founding, Israel practice, presidency. |
| <https://store.magnumphotos.com/pages/magnum-photos> | Magnum official institutional page | Cooperative history and photographer-owned institutional context. |
| <https://www.magnumphotos.com/photographer/david-seymour/> | Magnum official profile | Attempted; HTTP 403, unresolved. |
| <https://www.magnumphotos.com/terms-conditions/> | Magnum official rights/terms | Attempted; HTTP 403, unresolved. |
| <https://www.icp.org/exhibitions/chim-photographs-by-david-seymour> | Institutional authority, ICP | Humanistic approach and practice context. |
| <https://www.icp.org/sites/default/files/exhibition/credits/sites/default/files/exhibition_pdfs/icp_chim_wewentback_press.pdf> | Institutional authority, ICP press release/catalogue lead | Israel travel from 1951, assignments, practice, publication-history catalogue lead. |
| <https://www.icp.org/browse/archive/constituents/chim-david-seymour> | Institutional authority, ICP archive profile | Biography/holdings; direct open was restricted in this pass, but the indexed record was available. |
| <https://www.loc.gov/pictures/item/2024634496/> | National library/archive authority, Library of Congress | Holdings, arrangement, and rights advisory; no exact matching frame located. |
| <https://www.un.org/unispal/document/auto-insert-189953/> | Primary historical source, UN | 1949 Israel–Jordan armistice line and restrictions; direct open returned 403. |
| <https://www.un.org/unispal/document/auto-insert-210818/> | Primary historical source, UN Truce Supervision Organization | 1952 border-marking incidents; direct open returned 403. |
| <https://history.state.gov/historicaldocuments/frus1952-54v09p1/d732> | Primary/authoritative historical source, U.S. Department of State | 1953 diplomatic description of boundary tension and demilitarized zones. |
| <https://www.jta.org/archive/israel-signs-agreement-with-belgian-firm-on-copper-mining-equipment> | Contemporary historical press source | 1952 Negev copper-mining context; not scene-specific. |
| <https://books.google.com/books/about/Israel.html?id=mVQpAQAAIAAJ> | Official catalogue/bibliographic record | *Israel: 50 Years as Seen by Magnum Photographers*, Aperture 1998; publication lead only. |
| <https://doi.org/10.1515/9783110706345> | Publisher/book record | Carole Naggar, *David 'Chim' Seymour: Searching for the Light, 1911–1956*; Israel chapter lead, exact image inclusion unresolved. |
| <https://davidseymour.com/writings-on-close-enough/> | Estate-hosted secondary criticism | Terry Gips’s discussion of Seymour’s “closeness” and this border-patrol image; interpretation, not primary caption. |
| Archived Magnum 75 release: <https://web.archive.org/web/20220813041356id_/https://www.magnumphotos.com/shop/magnum-75-nft-gallery-page-280622/> | Official-source archive lead | Direct retrieval not completed; do not use for unverified token-specific claims. |
