# Casey Reas accession control note

Lot `6529NM.2026.001` is a constructed `ACCESSION_LOT` record for the
user-confirmed donation of seven Casey REAS Art Blocks tokens. Its controlled
workflow state is `received_onchain`; accession completion remains
`not_complete`.

The `acceptance_date` and `accepted_for_accession_processing` outcome are
intake/pathway processing facts tied to the 2026-08-01 receipt. They are not
formal institutional acceptance, title passage, rights approval, condition
approval, curatorial approval, or display authorization. The adopted Art Blocks
preapproval and donation policy establish the pathway; they do not waive the
ordinary title, rights, diligence, technical, preservation, or review gates.

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
as unsigned placeholders, never independent approval, formal acceptance,
completed accession, title, rights, or signed authority. The lot remains
`received_onchain` / `not_complete` until independent review and all remaining
gates are completed.

Transparent linked descriptors are available from the merged Casey source package and are reproducible from its published frozen snapshots, method, configuration, and content hashes. They use no OpenSea or marketplace metrics and make no aesthetic, quality, value, or ranking claim. The dossier is intentionally left with `reviewer: null`; independent review and integration—not constructor self-review—control the next decision.
