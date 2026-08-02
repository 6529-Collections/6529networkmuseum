# Casey Reas accession preservation evidence

This public package retains seven content-addressed Art Blocks metadata response
byte streams reused from the reviewed Casey snapshot acquisition. The files are
observation evidence, not the tokenized works and not a preservation or display
authorization.

The corresponding generator URLs and previously observed response hashes remain
recorded in the accession lot and object records. A new raw generator capture is
not claimed here: the repository's pinned safe-fetch policy rejected the live
responses because their transfer framing is not admitted. Generator capture,
render comparison, dependency capture, recovery testing, and independent
technical review remain open preservation gates.

The package also retains the raw JSON-RPC response body for the common Museum
receipt transaction and a separate acquisition record binding the endpoint,
method, parameters, observation time, response path, byte length, and SHA-256.
The receipt contains nine logs: seven ERC-721 `Transfer` events for the exact
accessioned token schedule and two `Approval` events. The validator decodes and
binds only the seven `Transfer` logs. This is one observed provider response,
not an independent-provider quorum or an identity claim about wallet
controllers.

The seven raw upstream metadata byte streams are intentionally verbatim. They
include public artist/collection royalty-routing wallet fields and authenticity
signatures because source fidelity requires preserving the upstream response;
those fields are not donor PII, identity inference, Museum title, rights, or a
current payment instruction. Historical counterparty wallet addresses are
published solely for reproducible provenance and do not support identity
inference.
