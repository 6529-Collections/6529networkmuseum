# Invalid fixture scenarios

The invalid cases are generated in `tests/test_control_plane.py` from the valid
fixture chain so each test can isolate one failure without maintaining stale
hashes. The suite covers payload tampering, constructor/reviewer reuse, public
sensitive fields, unresolved references, invalid workflow transitions, and a
`WINNER` governance observation incorrectly recorded as non-adopted.
