# PREMIS: keeping a digital artwork usable

Status: working Museum application profile; the cited standard remains authoritative

## The question

**What must the Museum preserve so this work can still be studied and
experienced?**

A digital artwork may depend on source code, a token hash, libraries, fonts,
network services, a browser, a display, timing, and the actions of a viewer.
A screenshot preserves one appearance. It does not preserve the system that
made the appearance possible.

PREMIS gives the Museum a disciplined way to name the things under its care,
the events that affect them, the people and software involved, and the
permissions that govern preservation work. It is the conservation record for
digital material.

## In the Casey Reas accession

For Casey Reas's *CENTURY #31*, the Museum has a checksum for the retained
metadata bytes. That checksum tests whether those exact bytes have changed. The
record can also identify the artwork, its external token, an observed generator,
the p5.js environment, and documentation stills. Those are different
preservation objects.

The live generator rendered when it was examined. A complete, self-contained
generator and dependency package has not yet been retained. PREMIS lets the
Museum say precisely what has been captured and why preservation remains in
progress.

## What PREMIS contributes

PREMIS 3.0 organizes preservation information around four entities:

| Entity | Museum use |
|---|---|
| **Object** | A work, representation, file, bitstream, environment, or other discrete unit being preserved |
| **Event** | A retrieval, fixity check, render test, migration, repair, validation, or other action affecting an Object |
| **Agent** | A person, organization, or software associated with an Event or Rights statement |
| **Rights** | The documented basis, permissions, restrictions, and terms under which a preservation action may occur |

The Object hierarchy is equally important:

- an **Intellectual Entity** is the coherent intellectual or artistic work, or
  a described environment;
- a **Representation** is the complete set of files and structural information
  needed for a reasonable rendition;
- a **File** is a named, ordered sequence of bytes;
- a **Bitstream** is meaningful data within a file.

The Museum reserves `Representation` for a set that can actually support the
declared rendition. A remote URL, thumbnail, or screenshot cannot receive that
designation by convenience.

## Museum application profile

### Objects and their roles

The Museum assigns every preservation Object a stable identifier and a role.
Roles include source capture, metadata response, generator source, dependency,
environment description, display derivative, documentation surrogate,
accessibility rendition, evidence package, and repository inventory.

An external CAIP-19 asset identifier remains separate from the Museum Object
identifier. One names the chain asset; the other maintains institutional
continuity through preservation versions and future migrations.

### Fixity with a declared scope

A digest always names its algorithm and the exact bytes covered. The record
also stores byte size, media type, acquisition method, source, event, and
validation outcome. A digest of an HTTP response body and a digest reported by
an upstream API are different assertions even when their values happen to
match.

### Significant properties and environments

The profile records the characteristics whose loss would materially change
the work or the evidence available to study it. For a generative work these may
include dimensions, timing, interaction, state transitions, color behavior,
randomness, token input, and dependencies.

Software and hardware environments are preservation Objects too. Browser,
library, operating-system, font, graphics, input, and network dependencies are
recorded at the level supported by evidence. A successful render is an Event
with conditions and outcome, rather than a permanent claim of compatibility.

### Events and outcomes

Every preservation Event records:

```text
event identifier and type
event date and time
Objects used, affected, or generated
Agents and their roles
method and tool versions
outcome and outcome details
evidence references
source Museum release
```

Corrections and later tests create new Events. They do not erase the earlier
observation.

## What this standard leaves to the Museum

PREMIS records preservation evidence and repository actions. It does not
authenticate an issuer, decide accession, establish legal title, prove an
artist's intent, or make an incomplete capture complete. A successful event
outcome is the repository's recorded result and remains traceable to its
evidence.

## For machines and implementers

### Authority and version

- Authority: PREMIS Editorial Committee; official publication hosted by the
  Library of Congress.
- Data Dictionary: **PREMIS 3.0**, published June 2015 and revised November
  2015; the Library of Congress identifies it as the current version.
- XML Schema: PREMIS 3.0.
- OWL ontology: PREMIS 3.0.0. It complements the Data Dictionary and imports
  PROV-O.
- Data Dictionary: [PREMIS 3.0](https://www.loc.gov/standards/premis/v3/premis-3-0-final.pdf).
- XML Schema: [premis-v3-0.xsd](https://www.loc.gov/standards/premis/v3/premis-v3-0.xsd).
- RDF namespace: `http://www.loc.gov/premis/rdf/v3/`.

Licensing is artifact-specific. The PREMIS OWL usage guidelines state CC BY
4.0, and the PREMIS-EC ontology repository states CC0 1.0 for its repository
content. Those statements do not automatically apply to every Library of
Congress PREMIS publication.

### Museum serialization target

The source Museum record remains authoritative. The planned preservation
projection provides:

1. PREMIS 3.0 XML for repository exchange;
2. PREMIS OWL with PROV-O relations for graph use;
3. a closed Museum JSON profile for routine validation and web delivery.

Each export includes the Museum profile version, PREMIS version, source commit
and manifest commitment, generator version, generation time, digest, and
validation result.

### Required Museum object shape

```json
{
  "object_id": "6529NM.2026.001.01",
  "object_category": "intellectual_entity",
  "external_asset_id": "eip155:1/erc721:0xa7d8d9ef8d8ce8992df33d8b8cf4aebabd5bd270/100000031",
  "preservation_status": "in_progress",
  "representations": [],
  "files": [
    {
      "role": "metadata_response",
      "fixity": {
        "algorithm": "sha256",
        "value": "e193e1436718786aac6e96aac69d70b3ecbb224576626378137683bbf6916e74",
        "scope": "retained HTTP response body bytes"
      }
    }
  ]
}
```

An empty `representations` array is intentional here. The present record does
not claim that the complete set needed for an autonomous rendition has been
preserved.

### Validation and conformance

Validation combines PREMIS 3.0 XSD checks, RDF parsing where applicable,
controlled-vocabulary checks, closed Museum JSON Schema, SHACL shapes, stable
identifier checks, fixity verification, and evidence-link resolution.

The Museum's first formal target is a documented Level 1B mapping: mandatory
Object elements for each supported Object category, one or more Agents, and
sufficient Event metadata to document preservation actions taken by the
repository. Level 2B additionally requires established routine export processes
and demonstrated Object, Agent, and Event export. PREMIS Rights remain in the
Museum profile even though the formal conformance levels do not include them.

## The Casey Reas accession

Museum state: `source_fields_present`. The canonical accession contains stable Objects,
retained metadata bytes and fixity, technical observations, environment facts,
Agents, Events, and preservation permissions sufficient for a substantial
PREMIS mapping. It does not yet contain a validated PREMIS 3.0 export or a
complete autonomous generator Representation. Preservation status remains
`in_progress` for all seven works.

## Official sources

- Library of Congress, [PREMIS official home](https://www.loc.gov/standards/premis/).
- Library of Congress, [PREMIS version 3](https://www.loc.gov/standards/premis/v3/).
- PREMIS Editorial Committee, [PREMIS OWL documentation](https://www.loc.gov/standards/premis/ontology/owl-version3.html).
- PREMIS Editorial Committee, [PREMIS OWL usage guidelines](https://www.loc.gov/standards/premis/ontology/pdf/premis3-owl-guidelines-20220426.pdf).
- PREMIS Editorial Committee, [conformance statement](https://www.loc.gov/standards/premis/premis-conformance-20150429.pdf).
