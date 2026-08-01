# Repository guidance

Read `README.md`, `docs/record-model.md`, `docs/accession-standard.md`, and `docs/stream-interoperability.md` before changing records.

Read `INDEX.md` before starting work. Before ending any substantive research or design turn, save conclusions and unresolved questions to a canonical file or dated `notes/wip/` file and update `INDEX.md`. Do not rely on task context as the only copy of working reasoning.

- Never infer accession from wallet custody, a transfer, an airdrop, or a Wave `WINNER` label.
- Never infer governance adoption from a vote total; record the live API status and observation time.
- Treat corrections as append-only amendments with `supersedes`; do not silently rewrite a historical assertion.
- Keep public and restricted records separate. This repository is public-record safe even if its GitHub visibility changes.
- Use stable Museum identifiers. Do not encode artist, collection, chain, or wallet information in accession numbers.
- Use CAIP-19-shaped citations for on-chain objects and preserve title/custody/rights as separate facts.
- Match 6529Stream's record envelope and museum profiles wherever the same concept exists. Record any unavoidable divergence in `docs/stream-interoperability.md`.
- Run `python scripts/validate.py` and `python scripts/generate_manifest.py --check` before committing.
- Treat `docs/implementation-roadmap.md` and `notes/wip/orchestration-ledger.md` as the durable task handoff. Append material status changes before ending a work session.
- Keys and Gates is currently selected but unminted. Do not assign a contract, token ID, custody event, or accession number until primary mint evidence exists.
- The Casey Reas seven-work group is a completed donation requiring accession documentation; record any incomplete accession gate explicitly instead of downgrading the donation to a proposal.
- OpenSea rarity metrics are not admissible. Generative trait analysis must use the Museum's published NextGen-compatible method, source snapshot, configuration, and deterministic result set.
