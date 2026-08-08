# Repository index

Read this file first. It indexes both authoritative records and work in progress so design reasoning survives task compaction and agent handoff.

Status vocabulary:

- **source transcription** — faithful copy of an external governing source;
- **adopted** — approved through the recorded Museum governance process;
- **canonical register** — current machine-readable Museum register;
- **working standard** — active design, not yet governance-approved;
- **WIP analysis** — reasoning or proposal retained for review;
- **template** — no factual or completion claim.

## Institutional and policy records

| File | Status | Contents |
|---|---|---|
| [`policies/founding-and-operating-principles.md`](policies/founding-and-operating-principles.md) | source transcription | Mission, public-good posture, TDH governance, custody, permanent holding, pathways, documentation, CC0 default |
| [`policies/general-nft-collecting-scope.md`](policies/general-nft-collecting-scope.md) | adopted | Exact text of winning Wave proposal #1052604 |
| [`policies/donation-acceptance.md`](policies/donation-acceptance.md) | adopted | Exact text of winning Wave proposal #1052812 |
| [`records/collections/approved-collections.json`](records/collections/approved-collections.json) | canonical reviewed register | Four adopted donation preapprovals and two proposals with no adopted effect at snapshot |

## Governance and programs

| File | Status | Contents |
|---|---|---|
| [`records/governance/decisions.json`](records/governance/decisions.json) | canonical reviewed register | Six adopted decisions and two proposals with no adopted effect at snapshot, with source hashes |
| [`governance/github-repository-governance.md`](governance/github-repository-governance.md) | active operating control | Maintainer approval/merge policy, configured team access, and current GitHub Free enforcement limitation |
| [`governance/pull-request-review-policy.md`](governance/pull-request-review-policy.md) | active operating control | Baseline 6529bot reviews, specialist routing matrix, follow-up procedure, and constructor/reviewer boundary |
| [`.github/6529bot.yml`](.github/6529bot.yml) | active review policy | Four-kind automatic production baseline plus bounded, maintainer-requested specialists; Stream review uses the documented central head-bound fallback until catalog upgrade |
| [`.github/workflows/museum-validation.yml`](.github/workflows/museum-validation.yml) | active CI | Required `Museum validation` foundation/full checks plus Ubuntu/Windows deterministic matrix on every PR and main push |
| [`records/programs/6529NM-AP-01/program.json`](records/programs/6529NM-AP-01/program.json) | canonical constructed program record | Keys and Gates rules, source provenance, undecided mint topology, and registrar gates |
| [`records/programs/6529NM-AP-01/selected-works.json`](records/programs/6529NM-AP-01/selected-works.json) | canonical constructed outcome index | Sixteen Wave winners retained as `selected_unminted`, explicitly not acquisition/accession |
| [`records/programs/6529NM-AP-01/media-manifest.json`](records/programs/6529NM-AP-01/media-manifest.json) | constructed technical manifest | Fixity-identified submitted sources with every public width and derivative currently withheld pending reviewed display authority; no preservation-master, rights, mint, acquisition, or accession claim |
| [records/programs/6529NM-AP-01/public/curated-acquisition.md](records/programs/6529NM-AP-01/public/curated-acquisition.md) | review-pending text edition | Art-led Keys and Gates overview for Curated Acquisition 6529NM-CA-2026-002: sixteen selected photographs, fifteen artist profiles, Research Publication 6529NM-RP-0002, visitor status, and Collection boundary; image display remains withheld pending reviewed authority |
| [records/programs/6529NM-AP-01/public/accessibility-amendment.md](records/programs/6529NM-AP-01/public/accessibility-amendment.md) | append-only derived publication amendment | Historical completed sixteen-image visual audit; exact OUT-002/011/016 accessibility corrections; one-to-one media/work invariant; source and rights boundary |
| [records/programs/6529NM-AP-01/public/accessibility-amendment-2026-08-08-002.md](records/programs/6529NM-AP-01/public/accessibility-amendment-2026-08-08-002.md) | append-only derived publication amendment | Follow-on OUT-013 accessibility correction preserving the separated “NO / WHERE / TO” key sequence and Esc key; synchronized JSON/typed output and hashes |
| [records/programs/6529NM-AP-01/public/accessibility-amendment-2026-08-08-003.md](records/programs/6529NM-AP-01/public/accessibility-amendment-2026-08-08-003.md) | append-only current-state amendment | Returns accessibility status to pending independent review; corrects OUT-008; limits OUT-011 to 640; records historical OUT-013 location note, prior derivative fixity, and exact current hashes |
| [records/programs/6529NM-AP-01/public/accessibility-amendment-2026-08-08-004.md](records/programs/6529NM-AP-01/public/accessibility-amendment-2026-08-08-004.md) | append-only delivery-enforcement amendment | Records exact OUT-011 640/1280/2400 post-invalidation readback, prior withdrawn-byte fixity, deterministic derivation boundary, and visitor/institutional infrastructure separation |
| [records/programs/6529NM-AP-01/public/accessibility-amendment-2026-08-08-006.md](records/programs/6529NM-AP-01/public/accessibility-amendment-2026-08-08-006.md) | append-only delivery-enforcement amendment | Records exact OUT-004 640/1280/2400 post-invalidation readback, prior withdrawn-byte fixity, and the image-specific minor-privacy delivery boundary |
| [records/programs/6529NM-AP-01/public/publication-authority-amendment-2026-08-08-005.md](records/programs/6529NM-AP-01/public/publication-authority-amendment-2026-08-08-005.md) | append-only registrar/publication amendment | Records `PROVISIONAL_EDITORIAL_DISPLAY_LIMITED` for all sixteen selected outcomes, with Museum-created WebP and catalogue-text scope kept separate from independent rights and acquisition gates |
| [records/programs/6529NM-AP-01/public/media-delivery-withdrawal-amendment-2026-08-09.md](records/programs/6529NM-AP-01/public/media-delivery-withdrawal-amendment-2026-08-09.md) | append-only current media-delivery amendment | Supersedes the candidate delivery state, closes the active width and derivative inventories at zero, preserves the exact prior commitment, and requires reviewed exact-commit display authority before restoration |
| [records/programs/6529NM-AP-01/public/publication-integration.md](records/programs/6529NM-AP-01/public/publication-integration.md) | WP-1 integration handoff | Canonical Work/Artist ID assignment, exact public routes, OUT source aliases, media relations, and pending typed-release admission |
| [`records/accessions/register.json`](records/accessions/register.json) | canonical reviewed current-view register | Casey REAS seven-work gift accepted and accessioned; title, rights, curatorial, and technical decisions complete; software preservation remains active stewardship |
| [`records/proposed-gifts/`](records/proposed-gifts/) | active public candidate register and packages | Exact gifts prepared for or open in a Museum Wave decision; no acceptance, custody, accession number, or collection-status claim |

## Casey Reas accession dossier

| File | Status | Contents |
|---|---|---|
| [`records/accessions/6529NM.2026.001/accession-statement.json`](records/accessions/6529NM.2026.001/accession-statement.json) | reviewed `ACCESSION_LOT` control-plane record | Completed permanent-collection accession with the exact seven-object identity/receipt schedule, curatorial determination, immutable evidence binding, reviewed rights, amber technical condition, and active preservation duties |
| [`records/accessions/6529NM.2026.001/gift-acceptance-authorization.json`](records/accessions/6529NM.2026.001/gift-acceptance-authorization.json) | reviewed `GIFT_ACCEPTANCE_AUTHORIZATION` | Executed full-gift acceptance under the adopted Art Blocks and donation-policy decisions, with authenticated Wave-status basis and completed title/accession resolution |
| [`records/accessions/6529NM.2026.001/visual-observation-record.json`](records/accessions/6529NM.2026.001/visual-observation-record.json) | reviewed `VISUAL_OBSERVATION` | Seven-object raw-metadata/source-URL binding, static-response and full-viewport screenshot fixity, canvas geometry, timing proxies, non-retention, and explicit observation limits |
| [`records/accessions/6529NM.2026.001/rights/6529NM.2026.001.RIGHTS.01.json`](records/accessions/6529NM.2026.001/rights/6529NM.2026.001.RIGHTS.01.json) | reviewed `RIGHTS_STATEMENT` | Per-object CC BY-NC 4.0 determination covering nine noncommercial Museum use classes with attribution, notice, change-marking, endorsement, and downstream-restriction conditions; sibling files cover all seven objects |
| [`records/accessions/6529NM.2026.001/technical/6529NM.2026.001.01.json`](records/accessions/6529NM.2026.001/technical/6529NM.2026.001.01.json) | reviewed `CONDITION_REPORT` | Per-object amber pass-with-conditions review with exact generator hash, dependency, interaction map, display conditions, and nonblocking preservation actions; sibling files cover all seven objects |
| [`evidence/casey-reas/manifest.json`](evidence/casey-reas/manifest.json) | content-addressed preservation evidence package | Seven retained raw metadata response byte streams, exact chain receipt, accession-level technical evidence, and an explicit boundary between completed review and unfinished autonomous generator preservation |
| [`docs/casey-accession-control.md`](docs/casey-accession-control.md) | active accession control note | Payload-hash basis, immutable Casey publication boundary, cross-file invariants, custody/title boundary, evidence grading, preservation gates, and reviewer boundary |
| [`records/accessions/6529NM.2026.001/objects/6529NM.2026.001.01.json`](records/accessions/6529NM.2026.001/objects/6529NM.2026.001.01.json) | reviewed object record | CENTURY #31 machine-readable object record; sibling files cover the other six objects |
| [`records/accessions/6529NM.2026.001/public/6529NM.2026.001.01.md`](records/accessions/6529NM.2026.001/public/6529NM.2026.001.01.md) | reviewed public page | Public object page for CENTURY #31; sibling pages cover the other six objects |
| [`records/accessions/6529NM.2026.001/public/casey-reas-artist-practice.md`](records/accessions/6529NM.2026.001/public/casey-reas-artist-practice.md) | reviewed public curatorial profile | Sourced artist biography, practice arc, pedagogy/tool-building/publishing context, and institutional exhibition/collection context |
| [`records/accessions/6529NM.2026.001/public/casey-reas-collection-essay.md`](records/accessions/6529NM.2026.001/public/casey-reas-collection-essay.md) | reviewed public curatorial essay | Collection-level reading of rule, behavior, room, and cosmos with static/live documentation boundary |
| [`records/accessions/6529NM.2026.001/public/gift-into-public-trust.md`](records/accessions/6529NM.2026.001/public/gift-into-public-trust.md) | reviewed public gift narrative | Full account of the seven-work gift, its accession into public trust, the curatorial case for the group, and the Museum's resulting obligations |
| [`records/accessions/6529NM.2026.001/public/projects/century.md`](records/accessions/6529NM.2026.001/public/projects/century.md) | reviewed public project essay | Art-historical and object-led interpretation of *CENTURY*; sibling essays cover *Pre-Process*, *Phototaxis*, *923 EMPTY ROOMS*, and *Ex Nihilo (Cosmos)* |
| [`records/accessions/6529NM.2026.001/public/source-and-chronology-matrix.md`](records/accessions/6529NM.2026.001/public/source-and-chronology-matrix.md) | reviewed public research apparatus | Claim-level source and chronology control for the artist, project, collection, gift, and object publications |
| [`records/institutional-practice/a-field-of-practice.md`](records/institutional-practice/a-field-of-practice.md) | public comparative essay | Living, work-led study of collecting, presenting, and caring for digital art, with selection method, thematic pathways, working lessons, and grouped case files |
| [`records/institutional-practice/profiles/`](records/institutional-practice/profiles/) | public institutional profiles | Twenty-seven primary-source profiles spanning media-art institutions, collecting museums, preservation services, archives, research centers, and contemporary scholarship controls |
| [`records/institutional-practice/adjacent-chain-native-practice.md`](records/institutional-practice/adjacent-chain-native-practice.md) | public comparative essay | Evidence-based classification of platforms, archives, festivals, communities, virtual presentation systems, marketplaces, and self-described museums adjacent to chain-native art |
| [`records/institutional-practice/source-register.md`](records/institutional-practice/source-register.md) | public research apparatus | Detailed source register and expanded-study source-apparatus explanation |
| [`records/institutional-practice/rights-and-licenses.md`](records/institutional-practice/rights-and-licenses.md) | public educational handbook | Copyright and public-domain foundations, token/work distinction, ordinary museum display and care, Creative Commons family, cultural-heritage rights statements, and no-license cases |
| [`records/institutional-practice/rights-for-artists.md`](records/institutional-practice/rights-for-artists.md) | public artist guide | Component inventory, licensing choices, NC/ND implications, token-holder terms, durable metadata, attribution, and preservation permissions |
| [`records/institutional-practice/rights-for-collectors.md`](records/institutional-practice/rights-for-collectors.md) | public collector guide | Token/copyright distinction, public domain, display, publication, preservation, loans, donations, resale, and evidence checklist |
| [`docs/rights/registry.json`](docs/rights/registry.json) | canonical public rights-expression registry | Twenty-two license, dedication, mark, status, no-license, and custom-term entries with separate instrument-permission and Museum-practice matrices, official sources, Casey assignments, and conditional Keys and Gates note |
| [`docs/rights/legal-texts/`](docs/rights/legal-texts/) | pinned official source snapshots | Exact English legal code for CC0 1.0 and all six CC 4.0 International licenses, retained from a fixed Creative Commons source revision and verified by SHA-256 |
| [`docs/institutional-source-inventory.json`](docs/institutional-source-inventory.json) | deterministic public source inventory | Every cited institutional-practice HTTPS source, citation label, and manuscript path; generated from the publication corpus |
| [`records/accessions/6529NM.2026.001/public/gift-acceptance-authorization.md`](records/accessions/6529NM.2026.001/public/gift-acceptance-authorization.md) | public human-readable authorization | Full-gift acceptance, exact governing basis, completed accession resolution, and continuing nonblocking stewardship duties |
| [`records/accessions/6529NM.2026.001/accession-certificate.json`](records/accessions/6529NM.2026.001/accession-certificate.json) | reviewed `ACCESSION` certificate | Executed seven-object title bindings, real receipt chronology, institutional custody registration, completed review outcomes, and Stream-aligned event/evidence structure |
| [`records/accessions/6529NM.2026.001/post-accession-diligence.json`](records/accessions/6529NM.2026.001/post-accession-diligence.json) | reviewed revision 2 post-accession diligence record | Exact-block owner, ENS, and token-level approval verification; executed-title interpretation; point-in-time OFAC exact-address screening; residual-risk disposition; and immutable evidence bindings |
| [`records/accessions/6529NM.2026.001/public/custody-title-and-compliance-diligence.md`](records/accessions/6529NM.2026.001/public/custody-title-and-compliance-diligence.md) | reviewed revision 2 public diligence note | Human-readable title, custody, encumbrance, sanctions-screening, limitations, and standing-action conclusions for the accessioned lot |
| [`evidence/casey-reas-diligence/manifest.json`](evidence/casey-reas-diligence/manifest.json) | content-addressed post-accession evidence package | Twenty-two-file package retaining nineteen exact JSON-RPC responses, the custody audit, the point-in-time official OFAC UI screening transcript, and package documentation |

## Working standards and architecture

| File | Status | Contents |
|---|---|---|
| [`docs/record-model.md`](docs/record-model.md) | working standard | Record domains, identifiers, evidence classes, correction model |
| [`docs/data-architecture.md`](docs/data-architecture.md) | working standard | Public introduction to the Museum's eleven-part collections, ontology, catalogue, provenance, preservation, presentation, packaging, storage, vocabulary, media-authenticity, and chain-identity architecture |
| [`docs/data-architecture/profile.json`](docs/data-architecture/profile.json) | machine-readable working profile | Closed eleven-standard register with authority/version pins, document paths, Casey implementation states, and the Stream-deferred boundary |
| [`docs/data-architecture/casey-reas-implementation.md`](docs/data-architecture/casey-reas-implementation.md) | public implementation audit | Standard-by-standard account of what accession `6529NM.2026.001` already supplies and which serializations, packages, and validators remain to be built |
| [`docs/data-architecture/casey-reas-machine-schedule.json`](docs/data-architecture/casey-reas-machine-schedule.json) | machine-readable implementation audit | Exact seven-object title, chain identity, custody-log, metadata-digest, generator-observation-digest, accession-state, preservation-state, and retention-boundary schedule checked against canonical records |
| [`docs/accession-standard.md`](docs/accession-standard.md) | working standard | Accession statement, object record, curatorial statement, completion gates |
| [`docs/stream-interoperability.md`](docs/stream-interoperability.md) | downstream interoperability standard | Exact Stream envelope and identifiers; future field-by-field convergence against the Museum-native data architecture |
| [`docs/proposed-gift-wave-standard.md`](docs/proposed-gift-wave-standard.md) | working public standard | Wave-native Storm dossier, minimum voter evidence, respectful proposal states, exact resolution, and accession handoff |
| [`docs/wave-storm-publication-standard.md`](docs/wave-storm-publication-standard.md) | working public publication standard | Reusable Storm and leaderboard-cover specification: live limits, first-media behavior, rights, accessibility, source fixity, preflight, publication, and readback |
| [`docs/generative-system-analysis.md`](docs/generative-system-analysis.md) | working standard | Art-first generative-system dossier method: encounter, thesis, and close looking before source/seed reconstruction, causal analysis, conservation, evidence, and review apparatus |
| [`docs/public-museum-experience-standard.md`](docs/public-museum-experience-standard.md) | replacement product and implementation standard | Art-first public Museum rebuild: information architecture, page and media requirements, Casey and Keys and Gates exemplars, publication adapter, accessibility, security, performance, and release gates |
| [`docs/program-media-delivery.md`](docs/program-media-delivery.md) | active technical profile | Keys and Gates source/surrogate separation, current fail-closed media withdrawal, authority-gated WebP transform and immutable delivery, rights boundary, and restoration procedure |
| [`docs/public-information-architecture.md`](docs/public-information-architecture.md) | reviewed canonical IA | Five-label navigation, human-slug route families, independent Work IDs, relational-only source entities, and reserved Exhibition route |
| [`docs/public-entity-ontology.md`](docs/public-entity-ontology.md) | working source ontology | Closed public entity profiles, relation domains/cardinality, lifecycle labels, typed media, and identity boundaries |
| [`docs/public-entity-publication-contract.md`](docs/public-entity-publication-contract.md) | compact frontend publication contract | Stream-shaped envelope, migration mapping, independent facts, current WINNER observation, and all-Work media joins |
| [`schemas/public-entity.schema.json`](schemas/public-entity.schema.json) | active closed schema | Entity/profile/page-exposure contract for Institution, Collection, Artist, Organization, Work, Project, Acquisition, Program, Research, Accession, Media, and reserved Exhibition |
| [`schemas/public-relation.schema.json`](schemas/public-relation.schema.json) | active closed schema | Directed relation endpoints, qualifiers, evidence, and relation identity |
| [`schemas/public-entity-identity-inventory.json`](schemas/public-entity-identity-inventory.json) | governed identity inventory | Stable entity IDs, acquisition-independent Work IDs, human slugs, aliases, redirects, and bootstrap uniqueness constraints |
| [`schemas/wave-status-observation.schema.json`](schemas/wave-status-observation.schema.json) | active append-only source schema | Authenticated Wave status observation with prior PARTICIPATORY history and explicit non-effects |
| [`records/proposed-gifts/6529NM-PG-2026-001/wave-status-observation-2026-08-08.json`](records/proposed-gifts/6529NM-PG-2026-001/wave-status-observation-2026-08-08.json) | canonical source observation | Signed `WINNER`, serial 1276093, exact ratings/raters, and no inferred acquisition/accession effect |
| [`tests/test_public_entity_layer.py`](tests/test_public_entity_layer.py) | active regression suite | Exact public graph counts, identity/route/media/lifecycle invariants, and adversarial fail-closed cases |
| [`docs/curatorial-publication-standard.md`](docs/curatorial-publication-standard.md) | active scholarship and editorial standard | Arguments, close looking, evidence, publication layers, digital-art research, technical case writing, editorial voice, style, notes, and acceptance tests |
| [`docs/digital-art-stewardship-standard.md`](docs/digital-art-stewardship-standard.md) | working standard | Evidence contract for digital-work identity, components, artist documentation, manifestations, technical events, preservation packages, reproducibility, service exit, and access tiers |
| [`docs/open-museum.md`](docs/open-museum.md) | working public operating statement | Public, cloneable, group-editable repository phase; reviewed contribution model; separation of durable record and replaceable display |
| [`docs/onchain-transition.md`](docs/onchain-transition.md) | working public migration statement | Fall 2026 custom-contract target, on-chain/content-addressed boundary, migration sequence, and explicit non-deployment status |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | active contributor guide | Contribution types, evidence and correction rules, repository map, validation commands, review path, public/restricted boundary, and migration context |
| [`RIGHTS.md`](RIGHTS.md) | active repository rights map | CC0 default for Museum-authored public material; exclusions for artworks, media, evidence, and other third-party material; contribution terms |
| [`docs/onchain-design.md`](docs/onchain-design.md) | working standard | General repository-to-chain migration target |
| [`docs/external-works-registry.md`](docs/external-works-registry.md) | WIP analysis | Recommended on-chain registry for donations minted outside Stream |
| [`specs/onchain/contract-migration-v1.md`](specs/onchain/contract-migration-v1.md) | working standard | V1 immutable registry migration design, active-vector/ABI-selector conformance, Stream bilateral-convergence and release gates, and no-deployment status |
| [`specs/onchain/dependency-runtime-nonproxy-v1.json`](specs/onchain/dependency-runtime-nonproxy-v1.json) | governed policy | Exact no-proxy/no-external-call runtime policy for bounded TargetRelease dependency rows; distinct from the direct governance executor |
| [`specs/onchain/release-attestor-policy-v1.fixture.json`](specs/onchain/release-attestor-policy-v1.fixture.json) | non-deployment conformance fixture | Schema-checked synthetic 2-of-3 release-attestor policy whose JCS policy and ABI signer-set commitments demonstrate immutable governance binding; never production authority |
| [`specs/README.md`](specs/README.md) | working standard | Boundary and admission requirements for implementation-ready protocol specifications |
| [`docs/generative-trait-analysis.md`](docs/generative-trait-analysis.md) | working standard | Pinned NextGen-compatible trait prevalence analysis; not quality or curatorial significance |
| [`docs/implementation-roadmap.md`](docs/implementation-roadmap.md) | active working plan | Durable phased build, constructor/reviewer rules, unresolved decisions, and handoff procedure |
| [`docs/standards-crosswalk.md`](docs/standards-crosswalk.md) | working standard | Current operational field-level crosswalk used by the accession and donation templates |
| [`templates/`](templates/) | template | Blank born-digital/tokenized accession, donation, preservation, public/restricted, and review forms; no factual or completion claim |

## Dated WIP notebook

| File | Status | Contents |
|---|---|---|
| [`notes/wip/2026-08-01-stream-coverage-and-gaps.md`](notes/wip/2026-08-01-stream-coverage-and-gaps.md) | WIP analysis | What Stream covers, strengths, implementation caveat, Museum gaps |
| [`notes/wip/2026-08-01-external-works-registry.md`](notes/wip/2026-08-01-external-works-registry.md) | WIP analysis | Options and recommended boundary for externally minted works |
| [`notes/wip/2026-08-01-casey-accession-working-plan.md`](notes/wip/2026-08-01-casey-accession-working-plan.md) | superseded WIP analysis | Historical multi-object numbering and proposed deliverables from the supplied accession draft; the completed accession dossier and register supersede its intake-stage gates |
| [`notes/wip/2026-08-01-nextgen-rarity-analysis.md`](notes/wip/2026-08-01-nextgen-rarity-analysis.md) | WIP analysis | Authoritative source pins, algorithm conclusions, implementation status, and unresolved questions |
| [`notes/wip/2026-08-01-documentation-control-plane.md`](notes/wip/2026-08-01-documentation-control-plane.md) | historical implementation note | Construction rationale, fail-closed remediation history, and remaining Stream/cross-language boundaries for the active documentation-as-code controls; current operation is in [`docs/control-plane.md`](docs/control-plane.md) |
| [`notes/wip/2026-08-02-curatorial-writing-redo.md`](notes/wip/2026-08-02-curatorial-writing-redo.md) | active WIP analysis | Third-lane diagnosis and replacement scope for Casey Reas monograph, project essays, seven-work collection essay, gift narrative, object entries, and reusable Museum writing standard |
| [`notes/wip/2026-08-03-open-museum-public-record.md`](notes/wip/2026-08-03-open-museum-public-record.md) | active implementation plan | Public, group-editable repository phase; Fall 2026 custom-contract target; frontend/record separation; contribution and exact-source UX contract; release gates |
| [`notes/wip/2026-08-03-publication-copy-edit.md`](notes/wip/2026-08-03-publication-copy-edit.md) | active editorial review | Museum publication voice standard, scope, diagnosis, preservation rules, and completion criteria for the institutional, curatorial, and frontend copy edit |
| [`notes/wip/2026-08-04-institutional-benchmarks.md`](notes/wip/2026-08-04-institutional-benchmarks.md) | active publication ledger | Research questions, selected field, editorial-audit decisions, and remaining frontend publication boundary |
| [`notes/wip/2026-08-04-expanded-institutional-practice.md`](notes/wip/2026-08-04-expanded-institutional-practice.md) | active research and publication ledger | Digital-weighted expansion mandate, six parallel research lanes, fixed editorial requirements, baseline, decisions, and release boundary |
| [`notes/wip/2026-08-04-rendered-publication-copy-desk.md`](notes/wip/2026-08-04-rendered-publication-copy-desk.md) | active rendered editorial checkpoint | Curatorial, registrarial, technical-methodology, and institutional-practice register review; release-blocking production labels and process narration; remaining qualification work |
| [`notes/wip/2026-08-04-generative-systems-analysis-standard.md`](notes/wip/2026-08-04-generative-systems-analysis-standard.md) | WIP design history | Source-backed proposal and Casey pilot reasoning retained behind the working standard and constructed five-project dossier set, including unresolved evidence/rights questions |
| [`notes/wip/2026-08-04-generative-system-frontend-experience.md`](notes/wip/2026-08-04-generative-system-frontend-experience.md) | live production instrument and release record | Project-owned Inside the System route, five Casey-specific visualizers, complete minted lookup/filter indexes, side-by-side Museum models, reviewed descriptor-backed suggestions, accession deep links, exact staging/production evidence, and the acquisition-extensible derived-display boundary |
| [`notes/wip/2026-08-05-museum-data-architecture.md`](notes/wip/2026-08-05-museum-data-architecture.md) | active construction and release ledger | Museum-native eleven-standard data architecture, two-level public/technical publication structure, Casey implementation crosswalk, Stream-deferred convergence boundary, and release state |
| [`notes/wip/2026-08-05-rights-handbook.md`](notes/wip/2026-08-05-rights-handbook.md) | live production release ledger | Public rights handbook, standard-license registry, retained legal texts, practical Museum-use explanations, object links, validation, and exact staging/production release evidence |
| [`notes/wip/2026-08-05-proposed-gifts-magnum-75.md`](notes/wip/2026-08-05-proposed-gifts-magnum-75.md) | active proposal and publication ledger | Wave-native seven-part Magnum Photos 75 voter dossier, evidence, API publication receipt, current WINNER status amendment, rendered acceptance, and accession boundary |
| [`records/proposed-gifts/6529NM-PG-2026-001/public/status-amendments/2026-08-08-winner.md`](records/proposed-gifts/6529NM-PG-2026-001/public/status-amendments/2026-08-08-winner.md) | live proposal status amendment | Exact authenticated WINNER readback, prior PARTICIPATORY observation, selected-by-Wave current status, and acceptance/title/custody/rights/accession boundary |
| [`notes/wip/2026-08-08-wp-3-magnum-scholarship.md`](notes/wip/2026-08-08-wp-3-magnum-scholarship.md) | active WP-3 scholarship and integration handoff | Isolated Magnum entity/artist/Work corpus, source and rights dossiers, public-media disposition, UTF-8/editorial checks, and typed WP-1 admission boundary |
| [`notes/wip/2026-08-06-production-deployment-reengineering.md`](notes/wip/2026-08-06-production-deployment-reengineering.md) | completed engineering and release ledger | Minute-by-minute release diagnosis, one-click production authority architecture, six-PR implementation, review and failure history, exact frontend and backend production evidence, measured timing, speedup, and remaining statistical follow-up |
| [`notes/wip/2026-08-07-all-gifts-wave-vote-resolution.md`](notes/wip/2026-08-07-all-gifts-wave-vote-resolution.md) | withdrawn governance proposal source | Exact source for former Museum Wave proposal serial 1281404; withdrawn before adoption and preserved as historical evidence |
| [`notes/wip/2026-08-07-all-gifts-wave-vote-publication.md`](notes/wip/2026-08-07-all-gifts-wave-vote-publication.md) | historical publication and withdrawal receipt | Signed publication identity and content commitment, final pre-withdrawal state, deletion receipt, and replacement link |
| [`notes/wip/2026-08-08-funding-gifts-and-program-authorization.md`](notes/wip/2026-08-08-funding-gifts-and-program-authorization.md) | governance analysis | Museum Wave discussion and policy distinctions among exact art gifts, already-authorized acquisition programs, unrestricted and restricted funding, nonstandard fungible assets, conversion responsibility, and unsolicited transfers |
| [`notes/wip/2026-08-08-integrated-gifts-and-acquisition-funding-policy.md`](notes/wip/2026-08-08-integrated-gifts-and-acquisition-funding-policy.md) | withdrawn replacement proposal source | Exact source for former Museum Wave proposal serial 1282040; withdrawn with zero raters and preserved as historical evidence |
| [`notes/wip/2026-08-08-integrated-gifts-and-acquisition-funding-publication.md`](notes/wip/2026-08-08-integrated-gifts-and-acquisition-funding-publication.md) | historical publication and withdrawal receipt | Signed publication identity and content commitment, final zero-voter state, deletion receipt, review-correction boundary, and replacement link |
| [`notes/wip/2026-08-08-museum-gifts-acquisition-programs-and-funding-assets-policy.md`](notes/wip/2026-08-08-museum-gifts-acquisition-programs-and-funding-assets-policy.md) | live replacement proposal source | Exact source for Museum Wave proposal serial 1282091, including versioned settlement-asset schedule `6529NM-ASA-1`, chain-object identity, separate title/custody/rights states, and the Section 9 conversion gate |
| [`notes/wip/2026-08-08-museum-gifts-acquisition-programs-and-funding-assets-publication.md`](notes/wip/2026-08-08-museum-gifts-acquisition-programs-and-funding-assets-publication.md) | live replacement publication receipt | Punk6529 authorization, append-only withdrawal history, signed `PARTICIPATORY` identity and URL, exact content commitment, zero-voter readback, and explicit not-yet-adopted status |
| [`notes/wip/orchestration-ledger.md`](notes/wip/orchestration-ledger.md) | operational WIP | Append-oriented mandate, fixed status facts, active phase, frontend release evidence, and next actions |
| [`notes/wip/2026-08-08-wp-1-source-ontology-handoff.md`](notes/wip/2026-08-08-wp-1-source-ontology-handoff.md) | active WP-1 handoff | Closed public entity/relation contract, Magnum Photos 75 Project/Organization boundary, generated counts, validation evidence, and successor-main publication hold |

## Generative analysis tooling

| File | Status | Contents |
|---|---|---|
| [`scripts/rarity/nextgen_compat.py`](scripts/rarity/nextgen_compat.py) | working standard | Deterministic input normalization, quality reporting, exact score/rank implementation, and hashes |
| [`scripts/rarity/analyze.py`](scripts/rarity/analyze.py) | working standard | CLI for snapshot analysis |
| [`tests/rarity/`](tests/rarity/) | test fixture | Exact compatibility fixture and coverage for missing/duplicate/tie/hash behavior |

## Research inputs

| File | Status | Contents |
|---|---|---|
| [`notes/research/governance-decision-evidence.md`](notes/research/governance-decision-evidence.md) | research input | Independently verified Museum Wave governance evidence, source/interpretation boundary, and append-only decision format |
| [`notes/research/museum-standards-crosswalk.md`](notes/research/museum-standards-crosswalk.md) | research input | Foundation source register and public-practice research retained as background to the current operational crosswalk |
| [`notes/research/museum-standards-crosswalk-luna.md`](notes/research/museum-standards-crosswalk-luna.md) | research addendum | Template-alignment delta: exact record-control payload-hash semantics and current Casey/Keys and Gates states |
| [`notes/research/repository-ci-architecture.md`](notes/research/repository-ci-architecture.md) | research input | Proposed canonical-record, schema, status-gate, manifest, CI, and release architecture |
| [`notes/research/external-registry-review.md`](notes/research/external-registry-review.md) | research input | Stream boundary analysis and synchronized, non-deployment V1 registry/hash/URI/release-bundle vectors |
| [`notes/research/nextgen-rarity-method.md`](notes/research/nextgen-rarity-method.md) | research input | Exact production NextGen trait-measure archaeology and reproducibility requirements |
| [`notes/research/casey-reas-art-technical-research.md`](notes/research/casey-reas-art-technical-research.md) | research input | Primary-source art-historical, technical, display, and preservation research for seven donated works, with dated gift-status supersession note |
| [`notes/research/generative-systems/casey-reas/README.md`](notes/research/generative-systems/casey-reas/README.md) | constructed research package | Five art-first project dossiers and a seven-work comparative study applying the working standard; research status and control apparatus are placed after the curatorial reading |
| [`notes/research/casey-reas-onchain-evidence.md`](notes/research/casey-reas-onchain-evidence.md) | research input | ENS resolution, seven token identities, common donation transaction, custody, metadata, and transfer evidence |
| [`notes/research/keys-and-gates-evidence.md`](notes/research/keys-and-gates-evidence.md) | research input | Full program rule, voting, artist statement, selected-work, CC0/consent, and unminted-status evidence inventory |

| [`notes/research/expanded-institutional-practice-synthesis.md`](notes/research/expanded-institutional-practice-synthesis.md) | reviewed research input | Twenty-seven-profile field, digital-first selection, chain-native category boundaries, stewardship requirements, scholarship principles, website judgment, and exclusions |

## Evidence snapshots

| File | Status | Contents |
|---|---|---|
| [`evidence/waves/museum-wave/README.md`](evidence/waves/museum-wave/README.md) | immutable evidence index | Complete authenticated 2026-08-01 Museum Wave snapshot, rendered history, source index, proposals, and SHA-256 digests |
| [`evidence/casey-reas-collection-snapshots/README.md`](evidence/casey-reas-collection-snapshots/README.md) | reviewed acquisition and descriptor evidence package | Full Art Blocks Hasura/tokenURI observations, reconstructed request provenance, 17 explicit cross-check exclusions, closed-scope/no-follow root manifest, direct PR #4 byte recomputation, and independently reviewed transparent descriptors for the five Casey REAS projects in lot `6529NM.2026.001` |

## Integrity tooling

| File | Status | Contents |
|---|---|---|
| [`schemas/`](schemas/) | active working standard | Bootstrap governance/collection/accession schemas, the closed Museum data-architecture profile, controlled vocabularies, and downstream Stream-compatible profiles |
| [`scripts/bootstrap_validate.py`](scripts/bootstrap_validate.py) | active CI control | Source-derived governance, raw evidence manifest, record-control, local-link, and public-safety checks |
| [`scripts/safe_fetch.py`](scripts/safe_fetch.py) | active CI control | Pinned HTTPS fetch primitive with IDNA/endpoint filtering, IP pinning, strict framing/headers, bounded JSON POST/GET requests, redirect rechecks, streamed caps, and observations |
| [`scripts/check_fetch_guard.py`](scripts/check_fetch_guard.py) | active CI control | Alias/import-aware AST guard rejecting unmediated network, dynamic-import, and command-line fetch implementations across all Python, including tests |
| [`scripts/validate.py`](scripts/validate.py) | working standard | JSON Schema, semantic, secret, cross-reference, state, status, and commitment validation |
| [`scripts/generate_manifest.py`](scripts/generate_manifest.py) | working standard | Deterministic SHA-256 and JCS/Keccak release commitments over the closed governed release inventory |
| [`scripts/validate_rights_handbook.py`](scripts/validate_rights_handbook.py) | active CI control | Rights registry schema, vocabulary completeness, legal-text fixity, reviewed Casey object links, conditional Keys and Gates status, and public-guide validation |
| [`scripts/sync_rights_legal_texts.py`](scripts/sync_rights_legal_texts.py) | deterministic source control | Offline verification and explicit safe-fetch acquisition of the seven pinned Creative Commons legal-code snapshots |
| [`scripts/generate_program_media.py`](scripts/generate_program_media.py) | deterministic media control | Enforces the current zero-width, zero-derivative Keys and Gates publication state and permits generation only under reviewed display authority, with fixity, geometry, colour, accessibility, and immutable-path checks |
| [scripts/check_public_unicode.py](scripts/check_public_unicode.py) | active editorial control | Strict UTF-8, exact Bangla title/codepoint, expected Unicode, and known-mojibake rejection for the Keys and Gates public corpus |
| [scripts/check_public_links.py](scripts/check_public_links.py) | active editorial control | Local Markdown file and anchor inventory for public corpus routes, work/media joins, source registers, and institutional records |
| [`tests/test_keys_gates_public_corpus.py`](tests/test_keys_gates_public_corpus.py) | focused editorial/media control | Exact all-sixteen accessibility text across canonical/typed/media/Work surfaces, curatorial-sequence navigation, public media allowlists, authority-width parity, visitor status, Wave-link regression, and no raw selected state on Work pages |
| [`scripts/acquire_casey_custody_audit.py`](scripts/acquire_casey_custody_audit.py) | reproducible evidence acquisition | Exact-finalized-block ENS, `ownerOf`, and token-level `getApproved` observations using EIP-1898 block-hash selectors, exact JSON-RPC response retention, stable canonical-block enforcement, and an explicit empty-output guard |
| [`scripts/build_casey_diligence_manifest.py`](scripts/build_casey_diligence_manifest.py) | active CI control | Complete-inventory raw-byte manifest builder rejecting symlinks, reparse points, non-regular files, and nested unmanifested evidence while checking idempotence |
| [`scripts/validate_casey_dossier.py`](scripts/validate_casey_dossier.py) | active CI control | Casey accession semantic verifier reconstructing exact RPC requests, decoding retained ABI responses, joining objects and OFAC subjects, and checking transport/fixity commitments |
| [`specs/onchain/`](specs/onchain/) | active design conformance | Offline-only contract-migration vectors for batch eligibility, URI canonical identity, HTTPS assertion lifecycle, address-bound TargetRelease evidence/signatures, and ABI/allowlist reconstruction; never deployment evidence |
| [`tests/`](tests/) | working standard | Valid record chain and negative control-plane fixtures |
| [`.github/workflows/museum-validation.yml`](.github/workflows/museum-validation.yml) | required CI | Required `Museum validation` check on pull requests and main pushes |
| [`docs/control-plane.md`](docs/control-plane.md) | working standard | Control-plane contract and local commands |
| [`release-artifacts/latest/record-manifest.json`](release-artifacts/latest/record-manifest.json) | canonical release commitment | Deterministic manifest for governed records and control-plane source |
| [`schemas/accession-program.schema.json`](schemas/accession-program.schema.json) | active local schema | Rigorous Keys and Gates program record contract |
| [`schemas/program-outcome-index.schema.json`](schemas/program-outcome-index.schema.json) | active local schema | Sixteen-row selected-work index contract |
| [`schemas/program-outcome.schema.json`](schemas/program-outcome.schema.json) | active local schema | Individual selected-work registrar outcome contract |

## Maintenance rule

Before ending a substantive design or research turn:

1. write new conclusions to a canonical document or dated WIP note;
2. record uncertainty and implementation status, not only conclusions;
3. update this index;
4. never promote WIP to adopted policy without a governance record;
5. run repository validation once the tooling exists.
