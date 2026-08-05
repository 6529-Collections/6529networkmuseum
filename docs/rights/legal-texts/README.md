# Creative Commons legal-code snapshots

This directory retains the exact English plain-text legal code for CC0 1.0 and
the six Creative Commons 4.0 International licenses covered by the Museum's
rights handbook.

The bytes come from the official Creative Commons
[`cc-legal-tools-data`](https://github.com/creativecommons/cc-legal-tools-data)
repository at commit
[`22fc2c31d0297a1feb8a257c0e6f84e95c9a38ae`](https://github.com/creativecommons/cc-legal-tools-data/tree/22fc2c31d0297a1feb8a257c0e6f84e95c9a38ae).
Their source URLs, publication URLs, and SHA-256 digests are recorded in
[`../registry.json`](../registry.json).

The retained text is unchanged. The Museum's plain-language explanations are
separate fields in the registry. Run:

```text
python scripts/sync_rights_legal_texts.py
```

to verify the closed inventory and every digest. The `--write` option acquires
the pinned official source through the repository's bounded HTTPS transport;
it fails if the upstream bytes differ from the recorded hash.

The Public Domain Mark and RightsStatements.org entries are descriptive tools,
not public licenses. Their canonical official pages are linked from the
registry rather than stored here as legal code.
