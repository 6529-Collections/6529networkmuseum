# Keys and Gates — deterministic media joins

This page is the public editorial join between each selected outcome and the existing program media manifest. It records current fixity and presentation paths without turning a web derivative into a preservation master, tokenized artwork, or rights instrument.

## Join rule

For each outcome, join:

```text
6529NM-AP-01-OUT-###
  -> records/programs/6529NM-AP-01/outcomes/OUT-###.json
  -> records/programs/6529NM-AP-01/media-manifest.json.items[record_id]
  -> submitted source SHA-256 + dimensions
  -> three WebP presentation derivatives
```

The derivative repository path is deterministic:

`media/programs/6529NM-AP-01/{record_id}/{source_sha256_without_prefix}/webp-v2-q82-m6-fixed-icc/{width}.webp`

The transform is `6529NM_WEB_PRESENTATION_WEBP_V2_Q82_M6_FIXED_ICC`: Pillow 12.3.0, WebP quality 82, method 6, Lanczos resize, EXIF transpose, embedded profiles converted to sRGB, fixed ICC profile SHA-256 `sha256:4ed6f6f05df0d17516662c5fe06ac90e14e0c1936abd15a491b57998c56aef86`. The source bytes were fixity-checked during derivation but are not retained in this repository.

## Current joins

| Outcome | Source SHA-256 | Source pixels | Current accessibility text | 640 derivative | 1280 derivative | 2400 derivative |
|---|---|---:|---|---|---|---|
| <a id="out-001"></a>OUT-001 | `sha256:898df24ecb82ac0b32ca99e995e5c1b027c47d6b1bef8d636eb2b06640d9ea66` | 3243 × 4864 | A small figure stands before a blue patterned gate in a sunlit stone hall. | 640 × 960 · `sha256:3e20417e…d59f0` | 1280 × 1920 · `sha256:d28e89b7…12b04` | 2400 × 3600 · `sha256:a2c571ee…46696` |
| <a id="out-002"></a>OUT-002 | `sha256:e3d4f538d4c9d3aa79a1d7ed11e93819a806fad85dbed4b8b38e9c62528d55fe` | 6000 × 4000 | An elevated view shows blurred buses and traffic around a sharply defined performer seated in a small white tub or boat on the roadway. | 640 × 427 · `sha256:fc6d063c…f3a38` | 1280 × 853 · `sha256:3d67ee66…8425` | 2400 × 1600 · `sha256:27be835c…b5269` |
| <a id="out-003"></a>OUT-003 | `sha256:4efc4651598006e212d159710714181c61dc3dfdc80719b7ae8a573f382d9eca` | 6720 × 4480 | A rider rises with a rearing white horse above a crowded herd in a mountain landscape. | 640 × 427 · `sha256:c45f68c1…a6461` | 1280 × 853 · `sha256:58d70f55…f3749b` | 2400 × 1600 · `sha256:2e5f3c80…a0db9` |
| <a id="out-004"></a>OUT-004 | `sha256:30e39b61e696cdab4b3a54beec5b33c2152f7440343479a45bc7bfe2175b0782` | 4160 × 4160 | Two silhouetted figures move through a rough stone passage toward a bright opening. | 640 × 640 · `sha256:8e0915b0…96987` | 1280 × 1280 · `sha256:18bb9cad…48ad1` | 2400 × 2400 · `sha256:73c4e5db…6108c` |
| <a id="out-005"></a>OUT-005 | `sha256:5df39d20ceb215cc93831e52bf9a8b27f332e5e94f613fb3c8f377200ea5daca` | 3780 × 2452 | A weathered concrete wall carries layered graffiti beneath a pale sky. | 640 × 415 · `sha256:5f0a87f5…5f0a` | 1280 × 830 · `sha256:ad1dbefd…47cc` | 2400 × 1557 · `sha256:b1f87960…1537` |
| <a id="out-006"></a>OUT-006 | `sha256:29db1bb746118e074cf6cbad247be4874ada7840fd3b025c37903bd87082a233` | 3804 × 2536 | A shirtless man opens a refrigerator covered with colourful magnets. | 640 × 427 · `sha256:ffa94eec…6bbe` | 1280 × 853 · `sha256:d6c7f8b8…d0d4f9` | 2400 × 1600 · `sha256:fa68ea81…98460` |
| <a id="out-007"></a>OUT-007 | `sha256:02a8ce8495cbea2bce1475a940a436310abc0fd979ff42114f9bf7a1953e9103` | 10080 × 5670 | Turquoise water at Moraine Lake is framed by evergreen forest and snow-dusted mountains. | 640 × 360 · `sha256:52c1e505…2d90e` | 1280 × 720 · `sha256:4f91f726…39ea11` | 2400 × 1350 · `sha256:4997f1f5…27a82` |
| <a id="out-008"></a>OUT-008 | `sha256:03950568f8819a8209f4931380e05b28b17408679a838f8043987b93d2e7fc3b` | 2952 × 3888 | An aerial view divides dense homes from a geometrically ordered palm plantation. | 640 × 843 · `sha256:655726c8…81c6b` | 1280 × 1686 · `sha256:e3d10c47…ab9ac` | 2400 × 3161 · `sha256:c15ab20d…b7f21` |
| <a id="out-009"></a>OUT-009 | `sha256:c6d7f689d7e532cedeaba69270c0775ccf619bbfbbd0f0c5bd9c182e1eb64314` | 3008 × 2000 | A high-contrast black-and-white view shows a weathered industrial site with graffiti and the words NOW IS OUR TIME. | 640 × 426 · `sha256:72e55121…25275` | 1280 × 851 · `sha256:8b7b0be0…1ff7b6` | 2400 × 1596 · `sha256:d453986c…ae144` |
| <a id="out-010"></a>OUT-010 | `sha256:f7445ec2e3d716ac8878ee7538001c1b45a2e29baf6f49fd090b86140ecb8162` | 4160 × 6240 | A bare torso emerges from black fabric while the head remains concealed. | 640 × 960 · `sha256:0ef30e4f…12f17` | 1280 × 1920 · `sha256:6c9668a3…3731d` | 2400 × 3600 · `sha256:51791ac9…f072c` |
| <a id="out-011"></a>OUT-011 | `sha256:4d7c6e452638a6dd091253bf1cc2c5b14e141920dd72a28dab5085bb7b4526fc` | 6000 × 4000 | A nude figure reclines on an ornate gold chair, wearing bright sandals and holding a small dark booklet or document; its text is not legible at the public derivative scale. | 640 × 427 · `sha256:14eea875…fc784` | 1280 × 853 · `sha256:00f3ff73…6f985` | 2400 × 1600 · `sha256:c704956b…2c251` |
| <a id="out-012"></a>OUT-012 | `sha256:4c9f68e4eee9cdf87f59cb960cac072dab8ec23e2b60a94095c38969412fa45b` | 5168 × 3648 | A distant figure with keys stands among ruined arches inside a damaged interior. | 640 × 452 · `sha256:33d7d68b…bea2d` | 1280 × 904 · `sha256:0a5ad28f…cedb20` | 2400 × 1694 · `sha256:aee6a534…63f8` |
| <a id="out-013"></a>OUT-013 | `sha256:dab5b9e0e5c82cff338f9f75c401cffe6a8b2a2f13e0b875526753cbc438d541` | 5000 × 5000 | Black keyboard keys spell NO WHERE TO, with an Esc key below and a small ant beside it. | 640 × 640 · `sha256:98422b16…b76b2` | 1280 × 1280 · `sha256:e61d70d1…3732` | 2400 × 2400 · `sha256:d3c5d998…b4959` |
| <a id="out-014"></a>OUT-014 | `sha256:caff170b0ba35c185f75c6e436c2557a9ef1743c399ca07dbb08848777239d03` | 2670 × 1878 | Water radiates through a dark fluted spillway toward a small opening of sky. | 640 × 450 · `sha256:6d823740…5c45` | 1280 × 900 · `sha256:9f7688d8…b927e` | 2400 × 1688 · `sha256:2d64c952…5299a` |
| <a id="out-015"></a>OUT-015 | `sha256:2e2a0c1d7ace2f24a15d5a0e2c448b38756c86fab8e31b66a04d797ba3d22a12` | 2800 × 4000 | Two people lean from separate windows of a weathered teal train; one wears an orange head covering. | 640 × 914 · `sha256:848332c6…8c72` | 1280 × 1829 · `sha256:d01bc25c…3df7` | 2400 × 3429 · `sha256:5a904e0b…4537` |
| <a id="out-016"></a>OUT-016 | `sha256:6f2e18606cc3fc4c3af0fadb3a275ef0a739c00463481bfb5fa511be238f5b73` | 4896 × 3917 | A small white house with a red roof stands on a hill beneath a starry sky, beyond a lit gate with a warning sign and a person-like silhouette. | 640 × 512 · `sha256:3e67afb1…a65f` | 1280 × 1024 · `sha256:057c4077…f4996` | 2400 × 1920 · `sha256:24271a75…83a9f` |

The abbreviated derivative hashes above are editorially compact; the full values and full repository paths remain authoritative in [`media-manifest.json`](../media-manifest.json). The source hash is the directory key, so the path remains deterministic even when the table abbreviates a derivative digest.

## Accessibility audit

All sixteen presentation descriptions are now marked constructed_visual_description_reviewed. The complete 640px set was checked against the selected images, with the three corrected descriptions checked again at the larger derivative scale. The descriptions remain visual descriptions: they do not identify people, infer legal status, or reproduce sensitive biography.

| Outcome | Disposition |
|---|---|
| OUT-002 | The description names the sharply defined performer seated in the small tub or boat, preserving the work's central contrast with blurred traffic. |
| OUT-004 | The public description stays with two silhouetted figures; the artist's description of children remains attributed in the work record and is not converted into a public identity assertion. |
| OUT-010 | The torso and concealed head are described plainly; the work page carries a nudity notice and does not infer identity, age, or location. |
| OUT-011 | The description names the visible dark booklet or document, bright sandals, and nude figure. It states that text is not legible at the public derivative scale; no identifier is transcribed. |
| OUT-015 | The description identifies the train windows and visible figures without naming either woman or assigning poster authorship. |
| OUT-016 | The description adds the lit gate, warning sign, and person-like silhouette while leaving the silhouette's status open. |

The reviewed accessibility projection and typed manifest updates are recorded in the [initial accessibility amendment](accessibility-amendment.md) and its [follow-on OUT-013 amendment](accessibility-amendment-2026-08-08-002.md). Derivative bytes and source hashes are unchanged; the selected outcome records remain the source of status and rights facts.
