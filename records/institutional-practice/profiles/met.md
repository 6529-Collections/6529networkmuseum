# The Metropolitan Museum of Art

- **Series:** A field of practice
- **Status:** public scholarship
- **Institutional author:** 6529 Network Museum
- **Version:** 1.0.0
- **Publication date:** 2026-08-04
- **Research cutoff:** 2026-08-04
- **Research apparatus:** [primary-source register](../source-register.md)

The Met’s public scholarship connects a collection record to several distinct
forms of evidence. The current record for Albrecht Dürer’s *Salvator Mundi*
contains an overview, catalogue entry, technical notes, provenance, exhibition
history, references, and loan restrictions, alongside structured object fields,
audio, related works, and links to the Met’s Open Access resources. [Salvator
Mundi](https://www.metmuseum.org/art/collection/search/436243) The design keeps
interpretation, material study, ownership history,
and reuse information remain addressable as separate layers under one object
number.

The same institution publishes research at longer scales. The [Heilbrunn
Timeline of Art History](https://www.metmuseum.org/essays/timeline-of-art-history)
describes itself as an expert-authored digital publication and research tool;
the current page reports more than 1,000 essays and 300 chronologies, with
regular updating and enrichment. [MetPublications](https://www.metmuseum.org/met-publications)
provides access to more than 1,700 titles from the past six decades. The
[Open Access dataset](https://github.com/metmuseum/openaccess) makes collection
data available for reuse, giving the public record a machine-readable path in
addition to its web presentation.

## Demonstrated practices

### 1. A single object page carries typed evidence

The *Salvator Mundi* record gives each type of evidence a named section. Its
overview identifies the work as a ca. 1505 oil painting on linden by Albrecht Dürer,
gives the object number and credit line, and then separates catalogue,
technical, provenance, exhibition, reference, and loan information into named
sections. The page also identifies the work as unfinished and explains that
preparatory drawing remains visible in the face and hands. [Salvator
Mundi](https://www.metmuseum.org/art/collection/search/436243)

The 6529 Network Museum should use typed separation:
an object description, runtime or technical account, provenance assertion,
exhibition event, rights statement, and conservation event should be distinct
records or fields with stable links to the same Museum identifier.

### 2. Artist instruction is cited inside interpretation

Adrian Piper’s *Everything #4* is documented as edition 6/8, with a 2004 date,
dimensions, acquisition credit, and object number. Its overview explains the
work’s serial structure and records that six editions were installed in the
Met’s *Afterlives: Contemporary Art in the Byzantine Crypt* exhibition from
January 29, 2024, through January 25, 2026, to realize the artist’s preferred
dispersed mode. A numbered note identifies the supporting Met publication.
[Everything #4](https://www.metmuseum.org/art/collection/search/900397)

The record links an artist’s stated preference, a curatorial decision, and a
specific installation
event. A chain-native record should similarly distinguish artist instruction,
Museum interpretation, display state, and the evidence for each.

### 3. Conservation writing publishes method and uncertainty

The Met’s 20 June 2019 essay [“After Three Hundred Years of Fading, a Dutch
Masterpiece Is Digitally Restored”](https://www.metmuseum.org/perspectives/margareta-haverman-vase-of-flowers-digital-conservation)
uses Margareta Haverman’s *A Vase of Flowers* to explain a digital
reconstruction. The account moves from pigment analysis to scanning electron
microscopy, X-ray fluorescence mapping, microscope examination, and image
adjustment. It states that the result is a close approximation of a possible
earlier appearance, not a recovered original. The essay also acknowledges that
technical equipment cannot answer every question and that some adjustments
remain judgments.

The case supplies a public model for software and generative art conservation.
A capture, emulation, or reconstructed runtime should record the observed state,
method, tools, assumptions, changes made during reconstruction, and residual
uncertainty. The record should preserve the distinction between evidence and
interpretation.

### 4. Research is connected across web publication and data

The Timeline’s essays and chronologies provide a research layer around
collection objects, while MetPublications provides a publication layer with
titles and related research paths. The Met’s Open Access repository supplies a
data path for independent use. [Heilbrunn Timeline of Art
History](https://www.metmuseum.org/essays/timeline-of-art-history),
[MetPublications](https://www.metmuseum.org/met-publications), and [Open Access
dataset](https://github.com/metmuseum/openaccess)

The Museum should reproduce the connection at a scale it can sustain: every public
record should expose a stable object identifier, a readable interpretation, a
machine-readable representation, and links to the essays, exhibitions,
technical studies, and versions that materially change its meaning.

## Close reading of public scholarship

The *Salvator Mundi* page assigns different evidence to separate layers.
The overview gives a short account of the work’s status and visual evidence;
the catalogue entry and technical notes can carry specialist claims; the
provenance, exhibition history, references, and loan restrictions identify
different documentary functions. The editorial voice is compact and
descriptive. It names what the page can establish and routes the reader to the
appropriate section instead of converting every type of evidence into
continuous narrative. [Salvator
Mundi](https://www.metmuseum.org/art/collection/search/436243)

The Haverman essay uses a different register. It is chronological and
procedural: the reader follows the problem of fading, the examinations, the
image work, and the qualified reconstruction. The essay makes specialist
methods legible without presenting them as self-sufficient proof. Its explicit
separation of technical observation, editorial adjustment, and approximation
is the most relevant writing lesson for a Museum that will publish software
studies, render captures, and emulation reports. [“After Three Hundred Years of
Fading, a Dutch Masterpiece Is Digitally
Restored”](https://www.metmuseum.org/perspectives/margareta-haverman-vase-of-flowers-digital-conservation)

## What the Museum should adopt

- Give each work one stable Museum identifier and expose separate, typed paths
  for description, provenance, rights, display, technical study, and
  conservation.
- Put artist instructions and display decisions beside the event and source
  that support them; do not encode interpretation as custody or provenance.
- Publish conservation as a reproducible account of observations, tools,
  transformations, and uncertainty. Label reconstructions as reconstructions.
- Connect readable essays and exhibition histories to the same object record as
  the machine-readable export.
- Make correction routes and update dates visible so that a record can change
  without erasing its earlier assertions.

## Where the analogy ends

The Met’s object-page pattern depends on curatorial, conservation, library,
publishing, and data capacity that the 6529 Network Museum does not yet have.
The Museum should begin with a small set of complete, well-sourced record types.
Open data also needs an explicit
scope, snapshot, and completeness statement; reuse access does not make an
object record complete or every image freely reusable. Finally, a digital
reconstruction can document an argument without resolving the historical
uncertainty that motivated it.

## Sources

1. Metropolitan Museum of Art, [“Salvator Mundi”](https://www.metmuseum.org/art/collection/search/436243). Publication date: not shown. Accessed: 2026-08-04. Supports: object fields; the separate overview, catalogue, technical, provenance, exhibition, reference, and loan sections; the account of the unfinished work.
2. Metropolitan Museum of Art, [“Everything #4”](https://www.metmuseum.org/art/collection/search/900397). Publication date: not shown. Accessed: 2026-08-04. Supports: edition and object metadata; the artist’s preferred dispersed installation; the *Afterlives* exhibition context and numbered note.
3. Metropolitan Museum of Art, [“Heilbrunn Timeline of Art History”](https://www.metmuseum.org/essays/timeline-of-art-history). Publication date: not shown. Accessed: 2026-08-04. Supports: the Timeline’s expert-authored digital-publication role, reported scale, and ongoing updating.
4. Metropolitan Museum of Art, [“MetPublications”](https://www.metmuseum.org/met-publications). Publication date: not shown. Accessed: 2026-08-04. Supports: the publication catalogue and its role as a research path alongside collection records.
5. Metropolitan Museum of Art, [“Open Access dataset”](https://github.com/metmuseum/openaccess). Publication date: not shown. Accessed: 2026-08-04. Supports: the machine-readable collection-data reuse path.
6. Metropolitan Museum of Art, [“After Three Hundred Years of Fading, a Dutch Masterpiece Is Digitally Restored”](https://www.metmuseum.org/perspectives/margareta-haverman-vase-of-flowers-digital-conservation), 20 June 2019. Accessed: 2026-08-04. Supports: the Haverman reconstruction’s examination methods, image adjustments, qualified result, and stated uncertainty.

## Revision history

- `1.0.0` — 2026-08-04: initial profile.
