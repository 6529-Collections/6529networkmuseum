# Constructor and reviewer attestations

Status: documentation-only draft template. An attestation records who would construct or review a record, the scope of the review, and its evidence. It is not a governed record, current CI-validated schema, or substitute for a legal signature where law or an instrument requires one.

The governed JSON record must use the exact [`record-control.md`](record-control.md) block. These attestations are the human-readable review narrative; `record_control.review.payload_sha256` is the authoritative machine-checkable binding.

## Attestation envelope

- Attestation ID: `6529NM.<record-id>-AT01`
- Record(s) covered: `[...]`
- Record version/effective date: `[...]`
- Supersedes: `[none | attestation ID]`
- Attestation hash/signature reference: `[...]`
- Signature scheme or verification method: `[...]`

## Exact record-control binding

- `record_status`: `[constructed | reviewed]`
- `constructor.actor_id`: `[non-empty actor ID]`
- `constructor.role`: `constructor`
- `constructor.constructed_at`: `[RFC 3339 UTC timestamp]`
- `review.actor_id`: `[non-empty actor ID, distinct from constructor; null while constructed]`
- `review.role`: `reviewer` (when reviewed)
- `review.reviewed_at`: `[RFC 3339 UTC timestamp; null while constructed]`
- `review.reviewed_commit`: `[40 lowercase hexadecimal Git commit; null while constructed]`
- `review.outcome`: `approved` (when reviewed)
- `review.payload_sha256`: `sha256:[64 lowercase hexadecimal characters; null while constructed]`

`review.payload_sha256` is computed over the full top-level JSON record after removing `record_control`, using UTF-8, `ensure_ascii=False`, `allow_nan=False`, sorted keys, and compact separators `(',', ':')`. Do not substitute a file hash, Markdown hash, signature hash, PR number, branch name, or filename.

## Constructor/preparer attestation

I attest that I constructed this record from the cited source material, preserved the distinction between verified facts and interpretation, marked unknown or not-assessed fields, and did not infer accession from custody, transfer, airdrop, or program selection.

- Name/role or public identifier: `[...]`
- Scope and sources used: `[...]`
- Conflicts/limitations: `[...]`
- Constructed at (UTC): `[...]`
- Version: `[...]`
- Signature/hash reference: `[...]`

The constructor may calculate the payload hash for a handoff, but cannot populate an approved review or review outcome.

## Registrar/title/rights attestation

I attest that the donor/transferor authority, title evidence, title binding, rights matrix, restrictions, credit line, and public/restricted boundary are recorded for the stated scope, with unresolved matters left open or escalated.

- Name/role or public identifier: `[...]`
- Scope: `[...]`
- Reviewed at (UTC): `[...]`
- Exceptions: `[...]`
- Signature/hash reference: `[...]`

## Technical/condition attestation

I attest that the technical and condition report identifies the examination protocol, environment, fixity evidence, render/behavior outcome, significant properties, dependencies, limitations, and risk without representing a surrogate as the tokenized artwork.

- Name/role or public identifier: `[...]`
- Scope: `[...]`
- Reviewed at (UTC): `[...]`
- Exceptions: `[...]`
- Signature/hash reference: `[...]`

## Curatorial attestation

I attest that the selection/significance/collection-relationship statement is identified as interpretation, is supported by cited evidence, and does not alter legal title, custody, rights, or technical status.

- Name/role or public identifier: `[...]`
- Scope: `[...]`
- Reviewed at (UTC): `[...]`
- Exceptions: `[...]`
- Signature/hash reference: `[...]`

## Independent reviewer attestation

I attest that I reviewed the record independently of its constructor, tested the stated completion gates proportionately to risk, checked object-level references, and recorded any disagreement or open condition.

- Name/role or public identifier: `[...]`
- Independence basis: `[...]`
- Review scope: `[...]`
- Reviewed at (UTC): `[...]`
- Findings/open conditions: `[...]`
- `record_control.review.actor_id`: `[same reviewer actor ID]`
- `record_control.reviewed_commit`: `[40 lowercase hexadecimal Git commit]`
- `record_control.review.payload_sha256`: `sha256:[64 lowercase hexadecimal characters]`
- Signature/hash reference: `[...]`

## Approver/effective authority

- Approving role/authority: `[...]`
- Decision/effective date: `[...]`
- Approval evidence: `[...]`
- Restrictions or conditions: `[...]`
- Signature/hash reference: `[...]`
