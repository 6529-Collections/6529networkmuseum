# Reviewed public projection release

Status: active release ledger

## Boundary discovered before candidate B

Candidate A `1e8c6f60f1fd2d23e972455cef193ccd43b8e515` contains the complete
review-pending public graph and visitor corpus. The independently reviewed
projection was generated correctly with explicit reviewer, time, candidate
commit, and candidate-manifest commitments. Its exact reviewed replay passed
locally.

The hosted workflow still invoked `migrate_public_entities.py --check` without
the reviewed parameters. That command deliberately constructs the pending
projection, so it would reject a valid reviewed B before the catalog verifier
could inspect the A-to-B transition.

## Resolution

Introduce `--check-existing-review-state` as a deterministic replay mode. It
reads only the closed generated-record set, requires either one wholly pending
state or one wholly reviewed state with an identical closed reviewer binding,
then regenerates and byte-compares that state. Mixed, malformed, partial, or
differently bound reviewed records fail closed.

This mode does not authorize review. Catalog activation continues to require:

- candidate A as the direct parent of reviewed B;
- exact candidate manifest SHA-256 and Keccak bindings;
- the same generator bytes in A and B;
- an exact review-only graph delta plus deterministic bundle/manifest effects;
- a non-constructor reviewer and a complete validator replay.

The replay fix must merge as a new pending candidate A. Candidate B will then
be regenerated as its direct child, rebound to the new A commitments, and
independently requalified before catalog activation.
