# Casey Reas public media presentation correction

Status: active append-only release correction; candidate A is constructed but not yet independently reviewed, merged, or catalog-activated.

## Defect and authority

The reviewed public entity graph left all seven accessioned Casey Reas Works without public visual art media. The retained preservation manifest and token metadata were correctly nonvisual JSON, but the official Art Blocks live generators were also marked nonvisual and no official Art Blocks stills were projected. That result conflicts with the Museum's art-first visitor standard and with the seven existing per-object CC BY-NC 4.0 determinations, which permit the required noncommercial reproduction, publication, exhibition, accessibility, and preservation uses subject to their recorded conditions.

The correction is controlled by an append-only predecessor/current pair:

- `6529NM-MEDIA-PRES-AMD-2026-08-09-000` binds the exact defective C4 catalog and the twenty-one affected Work, media, and relation payload commitments. Its payload commitment is `sha256:9ad86106947408ae2535f991ef76c347ddb3d94ae1cd6b2606c884ddf10073aa`.
- `6529NM-MEDIA-PRES-AMD-2026-08-09-001` supersedes that snapshot and carries the seven exact object-specific corrections. Its constructed payload commitment is `sha256:6c5363d44adb8f99e3a6ddf5932e3abac07b7d880a81f0fe4fb51026ad62f2d6`.

The source pair changes no title, custody, accession, Collection membership, rights grant, preservation completion, Magnum state, or Keys and Gates state.

## Exact projection

For objects `.01` through `.07`, media IDs `6529NM-MED-0045` through `0051` are official Art Blocks media-proxy PNG stills. Each is visual, primary, and display order 1. Existing generator IDs `6529NM-MED-0010` through `0016` remain the same identities but become visual `text/html` interactive media with the `interact_sandboxed` affordance and display order 2. New Work-to-still relations are `6529NM-REL-0212` through `0218`; the existing Work-to-generator relations `6529NM-REL-0126` through `0132` carry display order 2.

Every Work lists its still before its live generator. The first Work continues to list the preservation manifest and token metadata afterward; both remain nonvisual `application/json`. The other six Works list only their still and live media. The existing seven visual descriptions are the exact accessibility text on both presentation forms, and each media record cites its exact per-object rights record, object credit, and the official CC BY-NC 4.0 license URL.

## Fixity and geometry boundary

Each still's verified SHA-256 applies only to the exact Art Blocks media-proxy PNG response observed at `2026-08-09T23:04:32Z`. The host remains mutable, future bytes at the same URL may differ, and the digest does not apply to the live generator. The Museum did not retain the observed still response as a preservation master.

The generator remains mutable external HTML with no asserted response digest and no retained generator response bytes. The existing visual-observation record supplies canvas CSS geometry and accessibility evidence; it does not turn a live response into a preservation master.

The Pre-Process still is `2400 × 1349` because that was the exact observed PNG response geometry. Its live canvas is separately recorded as `1280 × 720` CSS pixels. Neither dimension is substituted for the other.

## Guardrails and remaining work

The schema permits verified fixity for mutable external media only as an exact observed-response commitment; semantic validation requires explicit mutability and non-retention language. Graph validation joins every correction row to its Work, still, live generator, rights record, accessibility text, affordances, exact source URL, dimensions, and display-order relations. It also fixes the preservation/metadata records as nonvisual JSON and keeps the Magnum and Keys and Gates nonvisual presentation records outside this amendment.

Candidate A construction and local qualification are complete. The deterministic inventory, visitor bundle, and complete manifest are current; bootstrap and full Museum/Casey validation pass; the 340-record migration replays exactly; the complete 323-test suite passes with one expected Windows platform skip; and the closed-affordance, response-fixity, display-order, and unchanged-boundary regressions pass. The exact manifest commitments live in the generated manifest to avoid a self-reference from this manifest-covered note.

Remaining gates are a frozen candidate A commit; independent Luna-max exact-head review; hosted PR checks and review bots; direct reviewed-child B generation; immutable catalog C activation; frontend PR #3695 rebinding; and exact-green merges. No A, B, or C state is asserted before those gates complete.
