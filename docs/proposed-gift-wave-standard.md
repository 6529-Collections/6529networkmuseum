# Accession proposals in the Museum Wave

- **Status:** working public standard; not adopted policy
- **Version:** 1.0.0
- **Publication date:** 2026-08-05
- **Applies to:** exact gifts presented to the 6529 Network Museum Wave for a curatorial decision
- **Governing policy:** [`donation-acceptance.md`](../policies/donation-acceptance.md)
- **First application:** `6529NM-PG-2026-001`, five works from Magnum Photos 75

## Purpose

A gift proposal asks the network to judge a specific group of works. The
decision deserves more than a short appeal, yet a proposal should not enter the
Museum website as though it were already part of the collection.

The Museum Wave is the public forum for that decision. Each proposed gift
appears as one multi-part Storm: the opening part states the exact question and
object schedule, each work receives an image-led section, and the closing part
carries the case, countercase, sources, and resolution. The parent drop is the
unit that receives TDH votes. The repository holds the public source edition
and its evidence; the Wave makes the decision.

## Public location and treatment

Open proposals belong in the Museum Wave. They do not appear among artists,
collections, accessions, or permanent holdings on the Museum website.

This placement matters when a proposal closes without selection. The decision
concerns an exact offered gift at a particular moment. It is not a verdict on
the artist, the collection, the donor, or the future relevance of related
works. The historical drop remains available in its original decision context
and uses the status **closed without selection**.

If the proposal clears the applicable threshold, its record and scholarship
become intake sources for the formal accession package. The accession record
then states what was verified, accepted, transferred, received, and
accessioned. The proposal itself retains its historical role.

## The decision

Every proposal opens with one exact question and two consequences.

- **Threshold cleared:** the Wave selects the complete scheduled gift for
  accession processing.
- **Threshold not cleared:** the proposal closes without selection.

Selection authorizes the Museum to proceed with the scheduled gift. It does
not itself verify donor authority, pass title, transfer the tokens, grant
copyright, establish custody, complete technical review, accept the gift, or
assign an accession number. Those events receive their own evidence and
records.

The Wave's threshold, duration, credit type, and status are live facts. The
proposal record captures the live API configuration and observation time. A
later record captures the submitted drop ID, serial number, status, and
decision time.

## Minimum dossier

The proposer supplies a finished public case. Voters should not have to infer
the gift from marketplace pages or ask a future reviewer to fill the record.

### 1. Exact offer

State:

- donor public credit;
- donation scope and any conditions;
- whether the Wave decides one object, an exact group, or a severable schedule;
- collection and project identity;
- chain, contract, token ID, edition, artist, title, and date for every object;
- whether the collection is preapproved under the current register.

Use a candidate ID such as `6529NM-PG-2026-001`. Do not reserve an accession
number.

### 2. Works before process

Show each work at a useful scale with artist, title, date, source caption,
credit, and rights statement. Follow with concise close looking that identifies
the formal relations that matter to the proposal's argument. Distinguish what
is visible from what a caption or historical source asserts.

### 3. The curatorial case

Explain why these exact works belong together and what the public could study
if the gift were later accepted. Name who formed the group: artist, curator, donor,
or Museum. Do not call a donor-formed group a suite, series, or canonical
selection without evidence.

Place the works in the artist's and collection's history at the scale needed
for the decision. Full artist monographs and object entries follow accession.

### 4. The strongest countercase

State the material considerations that could lead a voter to withhold
selection. These may concern the
grouping, collection fit, interpretive limits, rights, provenance, technical
dependence, vulnerable subjects, preservation burden, or missing evidence.
The countercase must be specific to the offered works. It is not a ceremonial
disclaimer.

### 5. Rights, provenance, and technical state

Separate token ownership, legal title, copyright, reproduction permission,
display permission, custody, media availability, and preservation. Record the
current evidence and the consequences of any unresolved term.

The proposal may use publicly issued upstream media for the Wave presentation
when the source exposes it for that purpose. Credit and rights remain visible.
Upstream availability is not Museum retention, preservation, or a rights
grant.

### 6. Sources and revision

Link the token metadata, chain citation, artist or institutional record, and
the strongest historical sources used. Give an access date and preserve file
hashes where the source is a constitutive object. Link the exact governed
repository edition when available.

## Storm form

One proposed gift uses one Storm drop and one TDH decision. A clear sequence
is:

1. the exact question and exact object schedule;
2. one image-led part per work;
3. the group case, countercase, rights/provenance/technical state, sources, and
   the same resolution at the end.

The opening and final parts repeat the same decision language. A shorter gift
may combine work sections. A larger gift may group works by documented series
or argument, provided every object remains identifiable and the voting unit
remains unmistakable.

## Preapproved collections

The adopted donation policy currently allows administrative acceptance of
eligible gifts from preapproved collections after ordinary checks. The
network's stated direction is to require an exact-gift accession proposal even
for those collections, with preapproval serving as a prior signal of collecting
interest. That change requires its own Wave amendment before it can be recorded
as adopted policy.

This standard is ready for that operating model: it can present an exact gift
from either a preapproved or non-preapproved collection. Until the amendment is
adopted, each proposal must state the policy authority actually in force.

## Status vocabulary

| State | Meaning |
|---|---|
| `draft` | Public source package is under construction. |
| `not_submitted` | Package is complete but no Wave drop exists. |
| `open` | A submitted Wave drop is awaiting a final threshold outcome. |
| `selected_for_accession_processing` | The drop cleared the applicable TDH threshold; later gift and accession events remain separate. |
| `closed_without_selection` | The drop did not clear the threshold. No collection-status effect follows. |
| `withdrawn` | The proposer withdrew the exact offer before decision. |
| `superseded` | A named later proposal replaces this edition. |

## Acceptance test

Before submission, answer yes:

- Is the exact voting unit clear in the first screen?
- Can every work be identified without a marketplace listing?
- Does every displayed image carry useful alternative text, credit, and rights?
- Does the text begin with the works and the decision rather than Museum
  procedure?
- Does the grouping argument depend on these exact works?
- Does the countercase give voters real grounds for a different judgment?
- Are source caption, visible description, context, and interpretation distinct?
- Are token ownership, title, custody, copyright, display, and preservation
  separated?
- Is the live Wave configuration observed rather than inferred?
- Does the resolution state what threshold clearance does and leaves for later?
- Does the proposal avoid valuation, rarity ranking, promotional claims, and
  an institutional recommendation?
- Is the repository source complete, public, validated, and free of private
  donor or security information?

If any answer is no, the proposal is not ready for the Wave.
