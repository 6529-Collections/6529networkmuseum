# Casey Reas accession control note

Lot `6529NM.2026.001` is a constructed `ACCESSION_LOT` record for the
formally accepted gift of seven Casey REAS Art Blocks tokens. Its controlled
workflow state is `received_onchain`; accession completion remains
`not_complete`.

`6529NM.2026.001.GAA-01` is a dated, formally effective Gift Acceptance and
Accession Authorization under the adopted Art Blocks preapproval and Donation
Acceptance Policy. Its user-authorized institutional acceptance decision is not
provisional: `record_status: constructed` and pending independent review refer
to documentation QA, not to whether the stated acceptance occurred. It is not
title passage, a rights approval, condition approval, curatorial approval,
display authorization, or a Stream-equivalent accession completion certificate.
The adopted pathway does not waive ordinary title, rights, diligence, technical,
preservation, or review gates.

Every Casey envelope payload carries a `payload_sha256` commitment computed as
SHA-256 over RFC 8785 canonical JSON after excluding the commitment field
itself. The envelope also carries the Stream-compatible Keccak content hash.
The validator binds the lot schedule to all seven object CAIP-19 identities,
the common seven-log receipt, receipt blocks/times/log indices, verified
custody, pending title bindings, unspecified rights, condition records, source
heads, and the content-addressed evidence manifest. Historical transfer events
are `indexer_observed` unless retained per-event receipt/block evidence exists;
the common museum receipt is `direct_rpc_verified`.

Raw metadata response bytes are retained under
[`evidence/casey-reas/manifest.json`](../evidence/casey-reas/manifest.json).
Generator response bytes, project/dependency capture, render comparison,
recovery testing, durable replica assignment, and independent technical review
remain explicit preservation gates. The Ex Nihilo object retains Art Blocks raw
fields (`engine_type=studio`, `project_id=0`, `tokenID=248`) separately from its
decoded invocation `248`.

The retained upstream metadata is verbatim by design. Public artist/collection
royalty-routing wallet fields and authenticity signatures are preserved solely
for source fidelity; they are not donor PII, identity inference, Museum title,
rights, or a current payment instruction. Historical counterparty wallet
addresses are published solely for reproducible provenance, with no identity
inference. The public boundary therefore preserves source bytes while keeping
donor identity, title, rights, and payment claims separate and unresolved.

The lot envelope has `reviewer: null` and zero Stream `signatureScheme` and
`signatureHash` placeholders. The constructor control explicitly labels these
as unsigned placeholders, never independent approval, an executed title
instrument, completed Stream accession, rights grant, or signed authority. The
formal gift authorization remains effective, while the lot remains
`received_onchain` / `not_complete` until the completion certificate and all
remaining gates are completed.

Transparent linked descriptors are available from the published Casey source package and are reproducible from its published frozen snapshots, method, configuration, and content hashes. They use no OpenSea or marketplace metrics and make no aesthetic, quality, value, or ranking claim. The dossier is intentionally left with `reviewer: null`; independent review and integration—not constructor self-review—control the next decision.

Evidence is intentionally two-level: the artwork-source bytes are anchored by `published_source_commit` `9700e842d0c991280b476cc67849d966221a742a`; the reviewed package/toolchain release is anchored by `bf70ba3fd888d2d1b8add90fe56e913102f8aa68`, package SHA-256 `c08749355ea12c2948efdfdeb232675ab4bf693976a94c6ebb4ce24b0b5d08ab`, and release SHA-256 `d05f75c65c0af0172a0a2f2207693e4211d5c0f4f69fad8d4907ebd90e12470e`. Exact commit URLs and content hashes identify this immutable evidence basis; later current-package revisions must not silently rewrite it.
