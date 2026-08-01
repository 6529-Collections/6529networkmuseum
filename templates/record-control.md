# Governed record control block

Status: documentation-only draft template. This target contract mirrors `scripts/bootstrap_validate.py` and the active bootstrap schemas for existing governed JSON records. It is not itself a governed schema or CI-validated record; the Markdown template file is not the payload being hashed. Matching schemas, cross-record invariants, state/publication gates, and binding for this template family remain required before these forms can be treated as governed.

## Exact control shape

Every governed JSON record has a top-level `record_control` object. A newly constructed record has a null review:

```json
{
  "record_control": {
    "revision": 1,
    "record_status": "constructed",
    "constructor": {
      "actor_id": "<non-empty constructor actor id>",
      "role": "constructor",
      "constructed_at": "<RFC 3339 UTC timestamp>"
    },
    "review": null
  }
}
```

After independent approval, the same record revision has:

```json
{
  "record_control": {
    "revision": 1,
    "record_status": "reviewed",
    "constructor": {
      "actor_id": "<non-empty constructor actor id>",
      "role": "constructor",
      "constructed_at": "<RFC 3339 UTC timestamp>"
    },
    "review": {
      "actor_id": "<non-empty reviewer actor id, distinct from constructor>",
      "role": "reviewer",
      "reviewed_at": "<RFC 3339 UTC timestamp>",
      "reviewed_commit": "<40 lowercase hexadecimal Git commit>",
      "outcome": "approved",
      "payload_sha256": "sha256:<64 lowercase hexadecimal characters>"
    }
  }
}
```

## Canonical payload hash

`review.payload_sha256` is the SHA-256 of the canonical UTF-8 JSON serialization of the entire top-level record after removing the `record_control` key. The validator's exact algorithm is:

```python
payload = {key: value for key, value in record.items() if key != "record_control"}
encoded = json.dumps(
    payload,
    ensure_ascii=False,
    allow_nan=False,
    sort_keys=True,
    separators=(",", ":"),
).encode("utf-8")
payload_sha256 = "sha256:" + hashlib.sha256(encoded).hexdigest()
```

Consequences:

- Hash the JSON payload, not the Markdown template, rendered prose, file bytes, or `record_control` block.
- Include `$schema` and every other top-level record field in the payload unless the validator explicitly excludes it.
- Do not hash the review object into its own `payload_sha256`; the entire `record_control` block is excluded.
- Changing a governed payload requires a new revision and a new review payload hash.
- `reviewed_commit` identifies the immutable reviewed Git revision; it is not a branch name, PR number, filename, or payload hash.
- `outcome` must be exactly `approved`; an anonymous reviewer, self-review, missing commit, or alternate signature field is not a valid substitute.

## Template implementation rule

Each instantiated JSON record must contain the exact block above, with the record's own constructor/reviewer identities and timestamps. The prose attestations in [`attestations.md`](attestations.md) explain scope and limitations; they do not replace `record_control` or alter the payload-hash algorithm.
