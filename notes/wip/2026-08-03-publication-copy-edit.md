# Museum publication copy edit

Status: implementation and release validation in progress

## Purpose

Remove the recurring habits of synthetic institutional prose from the public
Museum publication while preserving its factual, legal, curatorial, and
record-control precision. The finished voice should read as museum publishing:
specific, assured, economical, attentive to artworks, and candid about status.

This review covers the working Open Museum statements, contributor material,
website labels and framing, and the Museum-authored Casey Reas scholarship.
Adopted proposal text and source transcriptions remain verbatim. Machine records
change only when an editorial correction is necessary to keep a public text and
its declared title or status in agreement.

## Editorial standard

1. **State the subject directly.** Open with the artwork, decision, record, or
   institutional fact. Avoid throat-clearing about what the subject is not.
2. **Use contrast sparingly.** Constructions such as “not X but Y,” “not only,”
   “rather than,” “neither/nor,” and paired “does not” sentences are reserved
   for distinctions that carry legal, evidentiary, or art-historical weight.
3. **Replace process vocabulary with museum vocabulary.** Public copy names the
   catalogue, accession, provenance, rights, conservation, source, revision,
   and publication. Terms such as surface, control plane, boundary, adapter,
   failure mode, and architecture belong in technical documentation.
4. **Prefer a status to a disclaimer.** “Contract design in progress;
   deployment pending” is clearer than a sequence of negative claims. Status
   statements retain dates, authority, and any limits material to a reader.
5. **Keep one qualification with the claim it governs.** Do not repeat the same
   caveat in headings, standfirsts, body copy, captions, and footers.
6. **Use concrete nouns and active verbs.** Avoid abstract noun chains,
   ceremonial triplets, generic claims of significance, and sentences that
   narrate the act of explanation.
7. **Write from the object outward.** Curatorial prose begins with visible,
   temporal, technical, or historical particulars and develops an argument
   from them. It does not use metadata as a substitute for looking.
8. **Preserve distinctions that matter.** Token title, copyright, custody,
   accession, selection, rights, preservation, and display remain separate
   assertions. Necessary legal negation stays intact.
9. **Preserve evidence and attribution.** Copy editing must not alter quoted
   source text, citation scope, evidence class, lifecycle state, dates,
   identities, quantities, hashes, or the documented boundary between fact,
   artist/platform statement, technical observation, and Museum interpretation.
10. **End cleanly.** Conclusions advance the argument. They do not restate the
    document’s structure, announce balance, or close with a generic slogan.

## Working method

- Review public texts sentence by sentence, not by blind pattern replacement.
- Retain negation where removing it would create a false rights, title,
  accession, preservation, deployment, or authorship claim.
- Record source-transcription and adopted-policy files as out of editorial
  scope except for repository descriptions around them.
- Re-run the complete Museum validators and deterministic manifest generation
  after governed text changes.
- Review rendered desktop and mobile pages after frontend copy changes, with
  particular attention to About, source/revision notes, collection, gift,
  artist, project, object, program, governance, and methodology routes.

## Initial diagnosis

The new Open Museum material repeats several ideas through paired contrasts:
repository versus contract, record versus interface, decision versus
commitment, and public access versus institutional control. Each distinction
is valid. Their repeated “this, not that” formulation makes the prose sound
defensive and procedural. The revision will state each relationship once and
then describe the Museum’s actual practice.

The Casey corpus has a different risk. Its strongest passages are object-led
and exact, but some sections rely too often on mirrored antithesis, serial
qualification, and “what the group can/cannot do” scaffolding. The copy edit
will preserve its research and argument while varying its syntax and returning
attention to works, materials, histories, and display conditions.

## Implemented editorial decisions

- Recast the Open Museum and on-chain transition statements in a direct
  institutional voice. Mission, publication, permanent record, and public
  encounter now lead; repository and contract mechanics support them.
- Rewrote the contributor guide as an invitation to public scholarship with a
  concise account of review, attribution, corrections, rights, and privacy.
- Copy-edited the Casey Reas artist profile, collection essay, gift narrative,
  five project essays, seven object entries, curatorial review, and public gift
  authorization. The retained draft manuscripts and promoted public copies
  remain byte-reproducible through the publication promotion script.
- Added dated revision entries to every edited Casey publication. The edit
  changes voice and cadence only; object identity, accession status, rights,
  provenance, technical condition, evidence, and citations remain unchanged.
- Revised the curatorial publication standard so that it exemplifies the
  direct prose it requires.
- Replaced the website's full rendering of internal technical documents with a
  visitor-facing methods index. Adopted texts and technical specifications
  remain public in the source archive with concise, accurate abstracts on the
  Museum site.
- Reduced repeated source and contribution explanations to a publication
  colophon and removed duplicated summaries where the governed manuscript
  already carries the argument.

## Publication boundary

Policy transcriptions and adopted proposal texts were not copy-edited. Legal
and evidentiary negation remains where it prevents a false claim about title,
copyright, accession, artist intent, preservation, deployment, or authority.
Technical specifications remain exact source documents; the visitor index
changes their presentation, not their contents.

## Completion criteria

- Public institutional copy reads naturally without repository or protocol
  jargon unless the visitor has chosen a technical source.
- No repeated disclaimer appears where one precise status line is sufficient.
- Curatorial edits preserve citations and claim boundaries.
- Source and frontend tests pass; the governed manifest is deterministic.
- Staging and production render the revised copy without fallback, truncation,
  duplication, or mobile overflow.
