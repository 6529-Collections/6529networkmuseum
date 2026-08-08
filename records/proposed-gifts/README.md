# Proposed gifts

This directory contains public source packages for exact gifts placed, or being
prepared for placement, before the 6529 Network Museum Wave.

A proposal is not part of the collection. It receives a candidate ID and no
accession number. A Wave threshold outcome records selection or closure without
selection; transfer, title, custody, acceptance, and accession remain later
events with their own evidence.

The public presentation belongs in the Wave as one multi-part Storm. There is
no standing proposed-gifts gallery on the Museum website. This keeps an open
decision with its voters and discussion, and it avoids presenting an unselected
gift beside artists and permanent holdings.

The working form and minimum standard are documented in
[`docs/proposed-gift-wave-standard.md`](../../docs/proposed-gift-wave-standard.md).

The current Magnum Photos 75 proposal has an authenticated `WINNER` status
observation and is publicly described as **Selected by Museum Wave; acquisition
review in progress**. Selection remains distinct from formal acceptance,
donor authority, transfer, title, custody, rights clearance, technical or
preservation completion, accession, and Collection membership. Its dated
[status amendment](6529NM-PG-2026-001/public/status-amendments/2026-08-08-winner.md)
preserves the earlier proposal publication and live-state observation.

Each candidate's `public/voter-dossier.md` is a deterministic projection of
the ordered Markdown parts named in `wave-storm.json`. Regenerate and verify it
with:

```powershell
python scripts/build_proposed_gift_dossiers.py
python scripts/build_proposed_gift_dossiers.py --check
```
