# Spectrum 5.1: the work of running a collection

Status: working Museum application profile; the cited standard remains authoritative

## The question

**Did the Museum handle the object properly from the moment it arrived?**

Collectors often encounter the collection through a finished label: artist,
title, date, medium, credit line. Behind that label is a sequence of duties. A
museum must record why an object is in its care or custody, who is
responsible for it, whether it should be acquired, what rights and obligations
accompany it, where it is, what condition it is in, and whether the permanent
collection register is accurate.

Spectrum supplies procedures for that work. It is the UK collections-management
standard, used internationally, and its current web edition is Spectrum 5.1.
It organizes collections management into twenty-one procedures. Nine are
primary procedures that every museum should be able to perform reliably:
object entry; acquisition and accessioning; location and movement control;
inventory; cataloguing; object exit; loans in; loans out; and documentation
planning.

## In the Casey Reas accession

When punk6529 transferred seven Casey Reas tokens to
`networkmuseum.6529.eth`, the transfer established receipt in a Museum wallet.
It did not, by itself, accession the works.

The Museum then decided whether to accept the gift and recorded that decision.
It identified each object, documented the donor and governing approval,
reviewed title and rights, assessed condition and technical dependencies,
assigned one accession lot and seven object numbers, recorded custody, and
accepted the continuing work of preservation.

Spectrum gives that sequence a workable order. Ethereum supplies evidence for
particular chain events, but it does not decide whether a museum has accepted an
object into its permanent collection.

## What Spectrum contributes

Spectrum gives each procedure:

- a definition and scope;
- a minimum standard: the outcomes an institution should achieve;
- policy questions to settle before work begins;
- a suggested procedure;
- named information requirements that a collections system should retain.

Its value is practical: it makes the Museum record the decisions that carry an
object from receipt to ongoing care. The result is a chain of decisions and
records rather than a single status label.
That chain remains applicable whether an object is physical, born digital,
tokenized, hybrid, borrowed, or received unexpectedly.

## Museum application profile

### Entry and receipt

The Museum records the reason for receipt, sender, recipient, date, object
schedule, location or wallet, transaction evidence where applicable, hazards or
technical risks, expected disposition, and responsible staff or role. An
unsolicited token transfer enters this procedure even when the Museum intends
to decline it.

### Acquisition and accessioning

The acquisition record addresses collecting-policy fit, authority, provenance,
legal and ethical due diligence, donor or vendor title, rights, restrictions,
costs and continuing obligations, and the exact objects under consideration.
The accession act then records the Museum's permanent acceptance, stable
numbers, date, authority, and register entry.

The Museum keeps the following moments separate: offer, receipt, acceptance,
acquisition decision, title passage, custody receipt, accession, cataloguing,
technical verification, preservation completion, and display readiness.

### Location, movement, inventory, and audit

For a tokenized object, “location” includes the designated chain, contract,
token ID, custody account, control arrangement, and dated verification state.
Movement control records the authorized transaction rather than silently
replacing the prior wallet. Inventory confirms that the register and observed
custody still agree. Audit tests the quality and completeness of the process as
well as the balance of a wallet.

### Cataloguing, condition, rights, use, and care

Cataloguing identifies and interprets the work. Condition checking examines the
token, metadata, code, dependencies, rendering behavior, documentation, and
known risks. Rights management records rightsholders, licences, permissions,
restrictions, expiry or termination conditions, and the evidence supporting
each use. Use of collections and reproduction procedures govern exhibition,
publication, access copies, and other public activity. Collections care and
conservation continue after accession.

## What this standard leaves to the Museum

Spectrum is a procedural standard. It can be used with paper records and does
not prescribe one database or exchange serialization. It does not supply the
formal event ontology of CIDOC CRM, the public XML delivery structure of LIDO,
the preservation entities of PREMIS, or chain-asset syntax. The Museum uses
those layers to express and exchange the evidence produced through Spectrum
procedures.

## For machines and implementers

### Authority and version

- Authority: Collections Trust.
- Profiled version: Spectrum 5.1, published September 2022.
- Official current edition: [Spectrum](https://collectionstrust.org.uk/spectrum/).
- Procedure inventory: [All procedures](https://collectionstrust.org.uk/spectrum/procedures/).
- Use is subject to the [Spectrum licensing conditions](https://collectionstrust.org.uk/spectrum/spectrum-licensing/); Collections Trust permits free non-commercial download and use subject to those conditions.

The Museum paraphrases operational requirements and links to the licensed
source. It does not reproduce the full Spectrum procedure text.

### Minimum machine assertions

Every procedure event implemented by the Museum must carry:

```text
procedure_type
event_id
object_or_lot_ids[]
status
occurred_at or bounded_time
responsible_agent
authority_ref
evidence_refs[]
outcome
recorded_at
constructor
reviewer
supersedes[]
```

Fields are assertions, not free-floating values. The evidence reference records
its source, observation time, fixity where available, and Museum evidence class.
Unknown required facts are explicit. Corrections append a superseding record.

### Procedure-to-record projection

| Spectrum concern | Museum record |
|---|---|
| Object entry | receipt or intake event and object schedule |
| Acquisition and accessioning | authorization, title binding, accession statement, register transition |
| Location and movement | custody account and append-only movement event |
| Inventory and audit | dated custody/register reconciliation |
| Cataloguing | work description and public object record |
| Condition checking | technical and condition report |
| Rights management and reproduction | rights statement by use class and credit line |
| Collections care | preservation objects, events, risks, actions, and review dates |
| Deaccessioning and disposal | separately authorized event with retained accession history; no current Museum implementation |

### Conformance claim

The Museum currently states that its accession controls are **Spectrum-derived**
and operational. It does not claim Collections Trust certification. A stronger
claim would require a documented procedure-by-procedure assessment against the
licensed minimum standards and institutional policies.

## The Casey Reas accession

Museum state: `operational`. The Casey lot has distinct receipt, acquisition, title, custody,
accession, cataloguing, rights, condition, preservation, and audit evidence, and
its register state is validated in CI. The Museum has not yet completed a formal
independent Spectrum compliance audit.

## Official sources

- Collections Trust, [Spectrum 5.1](https://collectionstrust.org.uk/spectrum/).
- Collections Trust, [all twenty-one procedures](https://collectionstrust.org.uk/spectrum/procedures/).
- Collections Trust, [acquisition and accessioning](https://collectionstrust.org.uk/resource/acquisition-and-accessioning-the-spectrum-standard/).
- Collections Trust, [rights management](https://collectionstrust.org.uk/resource/rights-management-the-spectrum-standard/).
- Collections Trust, [condition checking and technical assessment](https://collectionstrust.org.uk/resource/condition-checking-and-technical-assessment-the-spectrum-standard/).
