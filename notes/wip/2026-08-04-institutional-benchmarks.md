# Institutional benchmarks for Museum practice

Status: source package editorial review complete; repository validation and
frontend publication pending. This note is not Museum policy and does not rank
institutions.

## Purpose

Study exemplary contemporary-art and digital-art institutions closely enough
to identify concrete practices the 6529 Network Museum can adopt, adapt, or
consciously decline. The result must improve the Museum's scholarship,
collection presentation, conservation practice, and public accountability. It
must not become a list of reputational namechecks or generic praise.

## Research questions

For each institution:

1. What is its institutional character, collecting or commissioning remit,
   and distinctive relationship to contemporary or computational culture?
2. Which public programs, collection systems, conservation practices,
   publishing forms, or technical initiatives demonstrate its strongest work?
3. How does it write about artists, artworks, exhibitions, collections,
   technology, and uncertainty?
4. What evidence and editorial apparatus make that writing trustworthy?
5. Which practices are transferable to a decentralized, chain-native museum,
   and which depend on a building, staff structure, jurisdiction, or budget
   that should not be imitated without qualification?

## Evidence standard

- Prefer the institution's own collection records, essays, conservation and
  research publications, annual or strategy reports, program archives, and
  technical documentation.
- Use artist, partner, standards-body, or peer-reviewed sources only where
  they establish a fact the institution's own record does not.
- Record direct URLs, page titles, publication dates where available, access
  date, and the proposition each source supports.
- Distinguish an institution's stated ambition from demonstrated practice.
- Do not infer institutional quality from reputation, visitor numbers, or a
  single exhibition.
- Keep quotation brief. Write the Museum's analysis in an independent voice.

## Comparative dimensions

- collection and commissioning model;
- artwork and artist interpretation;
- digital and time-based media conservation;
- technical transparency and reproducibility;
- online exhibition and network-native presentation;
- research depth, bibliography, and claim-level sourcing;
- public access, licensing, accessibility, and reuse;
- institutional memory, revision, and archival continuity;
- interface between the durable record and the public display;
- practices that can strengthen the 6529 Network Museum now.

## Planned outputs

1. A public introductory essay explaining why the Museum studies peers and
   how lessons are translated rather than copied.
2. Evidence-backed institutional profiles, each with a concise history,
   distinctive practice, close readings of representative public work, and
   specific lessons for the 6529 Network Museum.
3. A source register binding material claims to primary evidence.
4. A revised scholarship and editorial standard derived from the comparative
   study and the Museum's existing accession obligations.
5. A public frontend section that presents the profiles as an ongoing study in
   Museum-building, with immutable source links and contribution routes.

## Selected field

The first public field spans fourteen institutions and institutional systems:
the Met, Getty, MoMA, the Whitney, Tate, Centre Pompidou, SFMOMA, the
Guggenheim, ZKM, Ars Electronica, Rhizome/New Museum, Serpentine Arts
Technologies, the V&A, and LACMA. They supply different kinds of evidence:
layered catalogues, open data, conservation casework, media-art collections,
network-native commissions, research laboratories, archives, and technical
publishing. Selection records relevance to Museum problems; it confers no
ranking or endorsement.

## Editorial audit decisions

The first complete draft failed its own evidence and style standard in several
places. The following corrections are release requirements:

- factual claims carry direct primary-source links in the paragraph where they
  appear; a bibliography alone is insufficient;
- every profile includes a named work or project and a longer research,
  conservation, or technical source;
- collection totals and claims of institutional scale are identified as
  institution-reported facts;
- current service state is checked through the research cutoff, including
  Rhizome's 2026 Conifer transition;
- rankings, unsupported comparison, prestige language, and repetitive contrast
  syntax are removed;
- Museum lessons name records, fields, release requirements, or preservation
  actions instead of slogans;
- every profile URL is reconciled to the source register, whose entries record
  displayed title, date shown, source type, access date, and evidentiary use;
- automated tests check inventory, named cases, claim-level links, source
  reconciliation, publication control, and a small set of prohibited editorial
  phrases. Automated checks supplement editorial review; they do not certify
  truth or judgment.

## Remaining publication boundary

- canonical record paths and exact frontend atomicity contract;
- image and logo rights: no institutional mark or third-party image will be
  copied merely to decorate a profile;
- update cadence and append-only correction method for changing programs.

## Governed review checkpoint

Source pull request #22 opened from signed head `84175969cdfb`. The first
automated evidence review identified a real reconciliation gap: the
comparative essay cited Centre Pompidou's record for Vera Molnar's *Icône*,
while the source register carried the separate *Sans titre* record used by the
profile. The *Icône* page was reverified as the 1964 work, added to the source
register with its exact evidentiary use, and the test was widened from profile
reconciliation to every public publication in the package. The register now
contains exactly 114 unique sources. Publication dates are validated as dates
rather than frozen to the first release day. Rhizome's historical editorial
URL and archive root both returned HTTP 200 on recheck. Serpentine's `1.1.0`
version is intentional and is explained by its hostile-audit revision entry.

## Pre-publication factual review, second pass

The second governed review found two chronology compressions and one copy
defect. Tate's archive catalogue dates the Intermedia Art microsite to
2008–2012 and the Conifer capture to November 2019–February 2020; an earlier
source-register label incorrectly called it a 2017 capture. Rhizome's public
notices distinguish the closure of new accounts and subscriptions in December
2025, the end of paid subscriptions in May 2026, a planned June replacement by
a read-only tombstone application, and the service's current landing-page
notice. The study, profile, and register now preserve those events separately.
The Met profile's opening description was also copy-edited for grammar without
changing its claim.

The link validator now discovers both HTTP and HTTPS Markdown links and fails
unless every registered public source uses HTTPS. This closes the previous
blind spot in which an HTTP link would have escaped the test altogether.
Pre-publication corrections are recorded here and in manuscript revision
histories; no retroactive `supersedes` assertion was invented for drafts that
were never released. Immutable edition URLs remain a property of the website's
exact-commit source strip, because a manuscript cannot truthfully name its own
future merge commit.

Status amendment: this paragraph supersedes the earlier statement that full
repository validation and manifest generation remained pending. After these
corrections, the institutional test, bootstrap validator, full
Museum validator, fetch guard, Casey dossier validator, diligence inventory,
and deterministic manifest generation all passed. The resulting 230-entry
candidate manifest has SHA-256
`sha256:7ae561a27b5c3494d3bc81035af506ba5c49501ebb5c73a5535a3a2898c1b416`
and Keccak-256
`0xe71d1d744b2bccf1e2c724ab907a5bcc8e53bbf9befdc8f93b21ff89e76dd93c`.
These commitments remain candidates until PR #22 merges.

## Expanded-study handoff

The unpublished expansion brings the living study to twenty-seven profiles,
with particular attention to digital-art institutions, preservation services,
archives, research centers, and contemporary museums whose public practice
offers a concrete control case. It adds a separately classified study of
chain-native platforms and communities, a working digital-art stewardship
standard, and a deterministic inventory that binds every cited URL to its
labels and manuscript paths. The overview is organized by questions of
encounter, technical care, public records, and institutional context; the
selection remains a field of evidence, not a ranking.

Open release questions are limited to governed review of the final source
commit and exact commitments, atomic admission of the expanded study by the
existing website publication adapter, and staging and production qualification
of the restrained Stories & Research presentation. No `supersedes` target is
assigned because this entry records an unpublished revision in progress.
