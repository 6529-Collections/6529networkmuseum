from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PROGRAM_ID = "6529NM-AP-01"
STATUS = "constructed_visual_description_reviewed"
REVIEWER_ID = "codex-review:keys-gates-accessibility-2026-08-11-01"
REVIEWED_AT = "2026-08-11T22:44:52.647Z"
EXPECTED_ALTS = {
    f"{PROGRAM_ID}-OUT-001": (
        "A lone figure stands before a tall blue patterned gate as sunlight casts long "
        "geometric shadows across a stone hall."
    ),
    f"{PROGRAM_ID}-OUT-002": (
        "An elevated view shows blurred buses and traffic around a sharply defined "
        "person seated in a small blue tub or boat on the roadway."
    ),
    f"{PROGRAM_ID}-OUT-003": (
        "A rider on a rearing white horse rises above a herd of brown horses on a wide "
        "plain beneath hazy mountains."
    ),
    f"{PROGRAM_ID}-OUT-004": "Two silhouetted figures walk toward daylight at the end of a rough stone passage.",
    f"{PROGRAM_ID}-OUT-005": (
        "A long weathered concrete barrier with faded graffiti divides a pale sky from a dark foreground."
    ),
    f"{PROGRAM_ID}-OUT-006": "A shirtless person opens a refrigerator covered in colorful magnets in a kitchen.",
    f"{PROGRAM_ID}-OUT-007": (
        "A turquoise mountain lake is bordered by evergreen forest and a jagged, snow-dusted mountain range."
    ),
    f"{PROGRAM_ID}-OUT-008": (
        "A vertical aerial view shows dense residential roofs meeting an ordered palm plantation along a sharp boundary."
    ),
    f"{PROGRAM_ID}-OUT-009": (
        "Black-and-white industrial buildings sit beneath a cloudy sky, with the words NOW IS OUR TIME painted on a wall."
    ),
    f"{PROGRAM_ID}-OUT-010": "A bare torso emerges from folds of black fabric against a nearly black background.",
    f"{PROGRAM_ID}-OUT-011": (
        "A nude figure reclines on an ornate gold chair, wearing bright sandals, with "
        "one hand lowering a small dark booklet or document toward the floor; no text "
        "is readable on it."
    ),
    f"{PROGRAM_ID}-OUT-012": "A person stands framed by successive arched doorways inside a heavily damaged building.",
    f"{PROGRAM_ID}-OUT-013": (
        "Black keyboard keys spell NO / WHERE / TU on a white surface, while the Esc "
        "key sits apart below beside a small ant."
    ),
    f"{PROGRAM_ID}-OUT-014": (
        "The camera looks upward through a dark, fluted circular structure toward a small opening of sky."
    ),
    f"{PROGRAM_ID}-OUT-015": (
        "Two people lean from the windows of a weathered teal train; one wears a bright orange head covering."
    ),
    f"{PROGRAM_ID}-OUT-016": (
        "A small white house with a red roof stands on a hill beneath a starry sky, "
        "beyond a lit gate with a posted sign and a silhouetted figure."
    ),
}
EXPECTED_WIDTHS = {
    record_id: ([640] if record_id.endswith(("OUT-004", "OUT-011")) else [640, 1280, 2400])
    for record_id in EXPECTED_ALTS
}
CURATORIAL_SEQUENCE = (
    "take-the-key.md",
    "no-key-only-light.md",
    "rusted.md",
    "no-access.md",
    "the-artist-in-teh-open-sea.md",
    "managed-freedom.md",
    "the-cost-of-open.md",
    "dichotomy.md",
    "residual-barrier.md",
    "now-is-our-time.md",
    "morning-glory.md",
    "fight-for-freedom.md",
    "the-hostile-gate.md",
    "checkpoint.md",
    "sina-beizavi-in-brazil.md",
    "nowhere-to-esc.md",
)
RESTRICTED_WIDTH_IMAGE_ALIASES = {"OUT-004", "OUT-011"}
ACTIVE_IMAGE_PAGE_ALIASES = RESTRICTED_WIDTH_IMAGE_ALIASES | {"OUT-010"}


def load_json(relative_path: str) -> dict[str, object]:
    return json.loads((REPO_ROOT / relative_path).read_text(encoding="utf-8"))


class KeysAndGatesPublicCorpusTests(unittest.TestCase):
    def test_accessibility_projection_is_reviewed_and_has_exact_all_16_text(self) -> None:
        accessibility = load_json(f"media/programs/{PROGRAM_ID}/accessibility.json")
        self.assertEqual(STATUS, accessibility["status"])
        items = accessibility["items"]
        self.assertIsInstance(items, list)
        self.assertEqual(16, len(items))
        by_id = {item["record_id"]: item["alt_text"] for item in items}
        self.assertEqual(16, len(by_id))
        self.assertEqual(EXPECTED_ALTS, by_id)
        review = accessibility["record_control"]["review"]
        self.assertEqual(REVIEWER_ID, review["reviewer_id"])
        self.assertEqual("reviewer", review["role"])
        self.assertEqual(REVIEWED_AT, review["reviewed_at"])
        self.assertEqual("approved_with_corrections", review["outcome"])
        self.assertEqual("reviewed", accessibility["record_control"]["record_status"])
        self.assertEqual(
            EXPECTED_WIDTHS,
            {item["record_id"]: item["public_widths"] for item in items},
        )

        amendment = (REPO_ROOT / "records/programs/6529NM-AP-01/public/accessibility-amendment.md").read_text(
            encoding="utf-8"
        )
        self.assertIn(
            "sha256:48337baf91adb7d50beb43c65275e33d1c04f22a8ced32416683c663ba42c96e",
            amendment,
        )
        self.assertIn(
            "sha256:7f18d61c2ff6ae547c1e80384334ddc8966fae803cbee67346da3c5e6f29d7f2",
            amendment,
        )
        review_amendment = (
            REPO_ROOT / "records/programs/6529NM-AP-01/public/accessibility-review-2026-08-11.md"
        ).read_text(encoding="utf-8")
        for required in (
            "6529NM-AP-01-MEDIA-ACCESSIBILITY-2026-08-11-010",
            REVIEWER_ID,
            "22:44:52.647 UTC",
            "approved with corrections",
            "constructed_visual_description_reviewed",
        ):
            self.assertIn(required, review_amendment)

    def test_accessibility_text_projects_to_media_joins_and_work_pages(self) -> None:
        work_dir = REPO_ROOT / "records/programs/6529NM-AP-01/public/works"
        works_by_alias = {}
        alias_pattern = re.compile(r"\*\*Source alias:\*\* (OUT-\d{3})")
        image_pattern = re.compile(r"!\[([^\]]+)\]\([^\n]+\)")
        description_pattern = re.compile(r"\*\*Visual description:\*\* ([^\r\n]+)")
        for work in work_dir.glob("*.md"):
            text = work.read_text(encoding="utf-8")
            alias_match = alias_pattern.search(text)
            image_match = image_pattern.search(text)
            self.assertIsNotNone(alias_match, work)
            alias = alias_match.group(1)
            self.assertIsNone(image_match, work)
            description_match = description_pattern.search(text)
            if alias in ACTIVE_IMAGE_PAGE_ALIASES:
                self.assertIsNotNone(description_match, work)
                self.assertEqual(EXPECTED_ALTS[f"{PROGRAM_ID}-{alias}"], description_match.group(1))
            works_by_alias[alias] = (work, description_match.group(1) if description_match else None)
        self.assertEqual({f"OUT-{index:03d}" for index in range(1, 17)}, set(works_by_alias))

        media_text = (REPO_ROOT / "records/programs/6529NM-AP-01/public/media-joins.md").read_text(
            encoding="utf-8"
        )
        media_rows = {
            match.group(1): match.group(2).strip()
            for match in re.finditer(
                r'^\| <a id="out-(\d{3})"></a>OUT-\1 \| [^|]+ \| [^|]+ \| ([^|]+) \|',
                media_text,
                re.MULTILINE,
            )
        }
        self.assertEqual({f"{index:03d}" for index in range(1, 17)}, set(media_rows))
        for record_id, alt_text in EXPECTED_ALTS.items():
            alias = record_id.rsplit("-", 1)[1]
            if f"OUT-{alias}" in ACTIVE_IMAGE_PAGE_ALIASES:
                self.assertEqual(alt_text, works_by_alias[f"OUT-{alias}"][1])
            self.assertTrue(media_rows[alias])

    def test_typed_manifest_matches_accessibility_and_is_one_to_one(self) -> None:
        accessibility = load_json(f"media/programs/{PROGRAM_ID}/accessibility.json")
        manifest = load_json(f"records/programs/{PROGRAM_ID}/media-manifest.json")
        accessibility_by_id = {
            item["record_id"]: item["alt_text"] for item in accessibility["items"]
        }
        manifest_items = manifest["items"]
        self.assertEqual(16, len(manifest_items))
        manifest_ids = [item["record_id"] for item in manifest_items]
        self.assertEqual(16, len(set(manifest_ids)))
        self.assertEqual(set(accessibility_by_id), set(manifest_ids))
        for item in manifest_items:
            presentation = item["presentation"]
            self.assertEqual(STATUS, presentation["alt_text_status"])
            self.assertEqual(accessibility_by_id[item["record_id"]], presentation["alt_text"])
            expected_widths = EXPECTED_WIDTHS[item["record_id"]]
            self.assertEqual(expected_widths, presentation["public_widths"])
            self.assertEqual(expected_widths, [entry["width"] for entry in presentation["derivatives"]])

        out_011 = next(item for item in manifest_items if item["record_id"].endswith("OUT-011"))
        self.assertEqual([640], out_011["presentation"]["public_widths"])
        self.assertEqual([640], [row["width"] for row in out_011["presentation"]["derivatives"]])
        self.assertNotIn("/1280.webp", json.dumps(out_011))
        self.assertNotIn("/2400.webp", json.dumps(out_011))

        out_004 = next(item for item in manifest_items if item["record_id"].endswith("OUT-004"))
        self.assertEqual([640], out_004["presentation"]["public_widths"])
        self.assertEqual([640], [row["width"] for row in out_004["presentation"]["derivatives"]])
        self.assertNotIn("/1280.webp", json.dumps(out_004))
        self.assertNotIn("/2400.webp", json.dumps(out_004))

    def test_wave_source_link_uses_canonical_program_uuid(self) -> None:
        program_note = (REPO_ROOT / "docs/programs/keys-and-gates.md").read_text(encoding="utf-8")
        self.assertIn(
            "https://6529.io/waves/4ff022b3-aa17-4a0a-ba78-58f64ff1d427?drop=dc75fe32-f3c2-49db-9069-d9975b5964f3",
            program_note,
        )
        self.assertNotIn("https://6529.io/waves/4ff0223b-", program_note)

    def test_historical_accessibility_amendment_is_append_only_and_pending(self) -> None:
        amendment = (
            REPO_ROOT / "records/programs/6529NM-AP-01/public/accessibility-amendment-2026-08-08-003.md"
        ).read_text(encoding="utf-8")
        self.assertIn("6529NM-AP-01-MEDIA-ACCESSIBILITY-2026-08-08-003", amendment)
        self.assertIn("constructor-only status was not independent review", amendment)
        self.assertIn("OUT-008", amendment)
        self.assertIn("OUT-011", amendment)
        self.assertIn("constructed_visual_description_pending_independent_review", amendment)

    def test_out_011_withdrawal_has_exact_readback_and_stays_out_of_visitor_routes(self) -> None:
        amendment = (
            REPO_ROOT / "records/programs/6529NM-AP-01/public/accessibility-amendment-2026-08-08-004.md"
        ).read_text(encoding="utf-8")
        for required in (
            "6529NM-AP-01-MEDIA-ACCESSIBILITY-2026-08-08-004",
            "I8YFV5J3W4GCFQCZNXU39X6VYQ",
            "2026-08-08T12:49:27Z",
            "HTTP 200; 15,306 bytes",
            "HTTP 404",
            "sha256:00f3ff73be1cfff57a5ddf3ae9890cd9a49e1de547c5883cd1ac405bcda6f985",
            "sha256:c704956b390385b6c8f2c9158455292618b8237aa3355ff6b0a2615b3f62c251",
            "ECGWRHUV1NM3I",
            "6529bucket",
        ):
            self.assertIn(required, amendment)
        self.assertEqual(2, amendment.count("HTTP 404"))

        manifest = load_json(f"records/programs/{PROGRAM_ID}/media-manifest.json")
        out_011 = next(item for item in manifest["items"] if item["record_id"].endswith("OUT-011"))
        self.assertEqual([640], out_011["presentation"]["public_widths"])
        self.assertEqual([640], [row["width"] for row in out_011["presentation"]["derivatives"]])

        visitor_paths = [
            REPO_ROOT / "records/programs/6529NM-AP-01/public/README.md",
            REPO_ROOT / "records/programs/6529NM-AP-01/public/curated-acquisition.md",
            REPO_ROOT / "records/programs/6529NM-AP-01/public/curatorial-essay.md",
            *sorted((REPO_ROOT / "records/programs/6529NM-AP-01/public/works").glob("*.md")),
            *sorted((REPO_ROOT / "records/programs/6529NM-AP-01/public/artists").glob("*.md")),
        ]
        visitor_text = "\n".join(path.read_text(encoding="utf-8") for path in visitor_paths)
        for internal_value in ("ECGWRHUV1NM3I", "6529bucket", "I8YFV5J3W4GCFQCZNXU39X6VYQ"):
            self.assertNotIn(internal_value, visitor_text)

        source_url = out_011["source"]["url"]
        self.assertNotIn(source_url, visitor_text)
        self.assertIn("source hash, fixed transform, width allowlist", amendment)

    def test_out_004_withdrawal_has_exact_readback_and_lineage(self) -> None:
        amendment = (
            REPO_ROOT / "records/programs/6529NM-AP-01/public/accessibility-amendment-2026-08-08-006.md"
        ).read_text(encoding="utf-8")
        for required in (
            "6529NM-AP-01-MEDIA-ACCESSIBILITY-2026-08-08-006",
            "IBOR4WFJPZAPTU36ZXYOFBWLGK",
            "2026-08-08T13:03:13Z",
            "HTTP 200; 45,202 bytes",
            "sha256:18bb9cadc9c91a36518da2d5650cfaa3a9c398bebb4a283275a1b538bce48ad1",
            "sha256:73c4e5dbf469c3c2757ac2368409974e6b6b2c7a508b0ec4db9425252666108c",
            "HTTP 404",
            "sha256:8e0915b020965a6090c868ba29397c03ee8322d84ebca32fe3714f0537d96987",
        ):
            self.assertIn(required, amendment)
        self.assertEqual(2, amendment.count("HTTP 404"))

        manifest = load_json(f"records/programs/{PROGRAM_ID}/media-manifest.json")
        out_004 = next(item for item in manifest["items"] if item["record_id"].endswith("OUT-004"))
        self.assertEqual([640], out_004["presentation"]["public_widths"])
        self.assertEqual([640], [row["width"] for row in out_004["presentation"]["derivatives"]])

    def test_limited_editorial_display_authority_covers_all_16(self) -> None:
        amendment = (
            REPO_ROOT / "records/programs/6529NM-AP-01/public/publication-authority-amendment-2026-08-08-005.md"
        ).read_text(encoding="utf-8")
        self.assertIn("PROVISIONAL_EDITORIAL_DISPLAY_LIMITED", amendment)
        self.assertIn("No consent instrument", amendment)
        self.assertIn("private source", amendment)
        self.assertIn("does **not** activate CC0", amendment)
        self.assertEqual(16, amendment.count("| `PROVISIONAL_EDITORIAL_DISPLAY_LIMITED` |"))
        for alias in (f"OUT-{index:03d}" for index in range(1, 17)):
            self.assertIn(f"| {alias} |", amendment)

    def test_selected_outcomes_public_work_pages_and_media_are_one_to_one(self) -> None:
        selected = load_json(f"records/programs/{PROGRAM_ID}/selected-works.json")
        selected_ids = {item["record_id"] for item in selected["works"]}
        manifest = load_json(f"records/programs/{PROGRAM_ID}/media-manifest.json")
        manifest_ids = {item["record_id"] for item in manifest["items"]}
        self.assertEqual(16, len(selected_ids))
        self.assertEqual(selected_ids, manifest_ids)

        alias_pattern = re.compile(r"\*\*Source alias:\*\* (OUT-\d{3})")
        media_pattern = re.compile(r"/6529NM-AP-01-OUT-(\d{3})/")
        image_pattern = re.compile(r"!\[[^\]]*\]\([^\n]+\)")
        works = sorted((REPO_ROOT / "records/programs/6529NM-AP-01/public/works").glob("*.md"))
        self.assertEqual(16, len(works))
        aliases: dict[str, Path] = {}
        for work in works:
            text = work.read_text(encoding="utf-8")
            alias_match = alias_pattern.search(text)
            media_match = media_pattern.search(text)
            self.assertIsNotNone(alias_match, work)
            alias = alias_match.group(1)
            self.assertNotIn(alias, aliases)
            self.assertIsNone(image_pattern.search(text), work)
            self.assertIsNone(media_match, work)
            self.assertIn("**Media:** [Media and source record]", text)
            if alias in RESTRICTED_WIDTH_IMAGE_ALIASES:
                self.assertIn("**Image presentation:**", text)
                self.assertIn("**Visual description:**", text)
                self.assertNotIn("Image delivery:** Withheld", text)
                self.assertNotIn("pending independent review", text)
            self.assertIn(
                "**Status:** **Selected; not yet minted or accessioned; not in the permanent Collection.**",
                text,
            )
            self.assertNotIn("**Program state:**", text)
            self.assertNotIn("**Mint:**", text)
            self.assertNotIn("selected_unminted", text)
            aliases[alias] = work
        self.assertEqual({f"OUT-{i:03d}" for i in range(1, 17)}, set(aliases))

    def test_public_artist_and_work_navigation_is_bidirectional_and_direct(self) -> None:
        public_root = REPO_ROOT / "records/programs/6529NM-AP-01/public"
        acquisition = (public_root / "curated-acquisition.md").read_text(encoding="utf-8")
        essay_link = "(curatorial-essay.md)"
        self.assertIn(essay_link, acquisition)
        works = sorted((public_root / "works").glob("*.md"))
        artists = sorted((public_root / "artists").glob("*.md"))
        self.assertEqual(16, len(works))
        self.assertEqual(15, len(artists))
        for work in works:
            text = work.read_text(encoding="utf-8")
            self.assertIn("../curated-acquisition.md", text, work)
            self.assertIn("../curatorial-essay.md", text, work)
            artist_links = re.findall(r"\]\(\.\./artists/([^\)]+)\.md\)", text)
            self.assertTrue(artist_links, work)
            for artist_slug in set(artist_links):
                artist_path = public_root / "artists" / f"{artist_slug}.md"
                self.assertTrue(artist_path.exists(), artist_path)
                self.assertIn(f"../works/{work.name}", artist_path.read_text(encoding="utf-8"), artist_path)
        for artist in artists:
            text = artist.read_text(encoding="utf-8")
            self.assertIn("../curated-acquisition.md", text, artist)
            self.assertIn("../curatorial-essay.md", text, artist)
            self.assertRegex(text, r"\]\(\.\./works/[^\)]+\.md\)", artist)

    def test_full_work_navigation_matches_published_curatorial_sequence(self) -> None:
        public_root = REPO_ROOT / "records/programs/6529NM-AP-01/public"
        work_dir = public_root / "works"
        self.assertEqual(set(CURATORIAL_SEQUENCE), {path.name for path in work_dir.glob("*.md")})

        acquisition = (public_root / "curated-acquisition.md").read_text(encoding="utf-8")
        essay = (public_root / "curatorial-essay.md").read_text(encoding="utf-8")
        for label in (
            "Apertures and exits",
            "Managed movement",
            "Residual infrastructures",
            "Bodies and interfaces",
        ):
            self.assertIn(f"| {label} |", acquisition)
            self.assertIn(f"## {label}", essay)

        for index, filename in enumerate(CURATORIAL_SEQUENCE):
            text = (work_dir / filename).read_text(encoding="utf-8")
            browse = text.split("## Browse", 1)[1]
            actual_targets = re.findall(
                r"\[(?:Previous|Next): [^\]]+\]\(([^)]+)\)",
                browse,
            )
            expected_targets = []
            if index:
                expected_targets.append(CURATORIAL_SEQUENCE[index - 1])
            if index + 1 < len(CURATORIAL_SEQUENCE):
                expected_targets.append(CURATORIAL_SEQUENCE[index + 1])
            self.assertEqual(expected_targets, actual_targets, filename)

    def test_public_mint_language_is_non_committal(self) -> None:
        public_root = REPO_ROOT / "records/programs/6529NM-AP-01/public"
        expected = "Not yet minted; minting route under consideration"
        for relative_path in ("README.md", "curated-acquisition.md", "publication-integration.md"):
            text = (public_root / relative_path).read_text(encoding="utf-8")
            self.assertIn(expected, text, relative_path)
            self.assertNotIn("Mint pending", text, relative_path)

    def test_sina_title_and_sitter_boundary_is_explicit(self) -> None:
        text = (
            REPO_ROOT / "records/programs/6529NM-AP-01/public/works/sina-beizavi-in-brazil.md"
        ).read_text(encoding="utf-8")
        self.assertIn("The title supplies the submitted public name", text)
        self.assertIn("uses “the sitter”", text)
        self.assertIn("publishes no additional identity or biographical inference", text)
        self.assertIn("Consent is recorded separately", text)

    def test_sparse_artist_profiles_have_restrained_initial_profile_markers(self) -> None:
        artist_dir = REPO_ROOT / "records/programs/6529NM-AP-01/public/artists"
        expected_markers = {
            "intrepid.md",
            "minalisa.md",
            "teyhu.md",
            "veerendra.md",
            "zoku.md",
            "arsonic.md",
        }
        for filename in expected_markers:
            text = (artist_dir / filename).read_text(encoding="utf-8")
            self.assertIn("**Initial profile:**", text, filename)
        self.assertNotIn("**Initial profile:**", (artist_dir / "hugofaz.md").read_text(encoding="utf-8"))

    def test_gulyildiz_public_name_handle_association_has_direct_support(self) -> None:
        text = (REPO_ROOT / "records/programs/6529NM-AP-01/public/artists/gulyildiz.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("selected submission is signed", text)
        self.assertIn("public name/handle association", text)
        self.assertNotIn("professional name are established", text)
        self.assertNotIn("Istanbul", text)

    def test_fort_frederick_surveillance_is_attributed_or_source_bounded(self) -> None:
        work = (
            REPO_ROOT / "records/programs/6529NM-AP-01/public/works/no-key-only-light.md"
        ).read_text(encoding="utf-8")
        essay = (
            REPO_ROOT / "records/programs/6529NM-AP-01/public/curatorial-essay.md"
        ).read_text(encoding="utf-8")
        self.assertIn("attributes the association with surveillance", work)
        self.assertIn("artist’s account connects that personal movement to surveillance", essay)
        self.assertIn("documented military history supplies a frame of defence and control", work)
        self.assertNotIn("fort’s history places it beside a structure built to contain and surveil", work)

    def test_historical_publication_boundary_remains_append_only(self) -> None:
        public_root = REPO_ROOT / "records/programs/6529NM-AP-01/public"
        boundary = (public_root / "publication-authority-amendment-2026-08-08-007.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("Constructed and complete as text", boundary)
        self.assertIn("No independent exact-commit approval is asserted", boundary)
        self.assertIn("constructed_visual_description_pending_independent_review", boundary)
        self.assertIn("Image display and delivery", boundary)
        for alias in sorted(RESTRICTED_WIDTH_IMAGE_ALIASES | {"OUT-010"}):
            self.assertIn(f"| {alias} |", boundary)
            self.assertIn("no visual-display approval", boundary)
            self.assertIn("not approved for visual display or delivery", boundary)
            work_name = {
                "OUT-004": "no-key-only-light.md",
                "OUT-010": "checkpoint.md",
                "OUT-011": "sina-beizavi-in-brazil.md",
            }[alias]
            work = (public_root / "works" / work_name).read_text(encoding="utf-8")
            self.assertIn("**Image presentation:**", work)
            self.assertIn("**Visual description:**", work)
            self.assertNotIn("Image delivery:** Withheld", work)
            self.assertNotIn("pending independent review", work)
            self.assertNotIn("d3lqz0a4bldqgf.cloudfront.net/museum/programs/", work)

        historical_accessibility = (
            public_root / "accessibility-amendment-2026-08-08-003.md"
        ).read_text(encoding="utf-8")
        self.assertIn("Historical technical record", historical_accessibility)
        self.assertIn("constructed_visual_description_pending_independent_review", historical_accessibility)
        current_authority = (
            public_root / "media-display-authorization-amendment-2026-08-11.md"
        ).read_text(encoding="utf-8")
        self.assertIn("retains the 9 August withdrawal as an append-only predecessor", current_authority)

    def test_public_media_urls_are_manifest_allowlisted_and_restricted_urls_are_absent(self) -> None:
        public_root = REPO_ROOT / "records/programs/6529NM-AP-01/public"
        accessibility = load_json(f"media/programs/{PROGRAM_ID}/accessibility.json")
        accessibility_by_id = {item["record_id"]: item for item in accessibility["items"]}
        manifest = load_json(f"records/programs/{PROGRAM_ID}/media-manifest.json")

        allowed_urls = set()
        for item in manifest["items"]:
            record_id = item["record_id"]
            allowed_widths = set(accessibility_by_id[record_id]["public_widths"])
            for derivative in item["presentation"]["derivatives"]:
                if derivative["width"] in allowed_widths:
                    allowed_urls.add(derivative["url"])

        visitor_paths = [
            public_root / "README.md",
            public_root / "curated-acquisition.md",
            public_root / "curatorial-essay.md",
            *sorted((public_root / "artists").glob("*.md")),
            *sorted((public_root / "works").glob("*.md")),
        ]
        visitor_text = "\n".join(path.read_text(encoding="utf-8") for path in visitor_paths)
        media_urls = {
            url.rstrip(".,;")
            for url in re.findall(r"https?://[^\s)]+", visitor_text)
            if "d3lqz0a4bldqgf.cloudfront.net/museum/programs/" in url
        }
        self.assertEqual(0, len(media_urls))
        self.assertTrue(media_urls <= allowed_urls)
        self.assertNotRegex(
            visitor_text,
            r"/6529NM-AP-01-OUT-(?:004|010|011)/[^\s)]+/(?:640|1280|2400)\.webp",
        )

    def test_upstream_source_urls_are_provenance_only_and_not_media_projection(self) -> None:
        public_root = REPO_ROOT / "records/programs/6529NM-AP-01/public"
        manifest = load_json(f"records/programs/{PROGRAM_ID}/media-manifest.json")
        media_joins = (public_root / "media-joins.md").read_text(encoding="utf-8")
        self.assertIn("upstream public submission evidence", media_joins)
        self.assertIn("not themselves Museum presentation links", media_joins)
        visitor_paths = [
            public_root / "README.md",
            public_root / "curated-acquisition.md",
            public_root / "curatorial-essay.md",
            *sorted((public_root / "artists").glob("*.md")),
            *sorted((public_root / "works").glob("*.md")),
        ]
        visitor_text = "\n".join(path.read_text(encoding="utf-8") for path in visitor_paths)
        for item in manifest["items"]:
            source = item["source"]
            self.assertEqual("submitted_high_resolution_source", source["role"], item["record_id"])
            self.assertNotIn(source["url"], json.dumps(item["presentation"]), item["record_id"])
            self.assertNotIn(source["url"], media_joins, item["record_id"])
            self.assertNotIn(source["url"], visitor_text, item["record_id"])

    def test_out_011_sensitive_source_language_is_minimized_from_release_projection(self) -> None:
        public_root = REPO_ROOT / "records/programs/6529NM-AP-01/public"
        visitor_paths = [
            public_root / "README.md",
            public_root / "curated-acquisition.md",
            public_root / "curatorial-essay.md",
            *sorted((public_root / "artists").glob("*.md")),
            *sorted((public_root / "works").glob("*.md")),
        ]
        visitor_text = "\n".join(path.read_text(encoding="utf-8") for path in visitor_paths).lower()
        research_text = (
            REPO_ROOT / "notes/research/keys-and-gates-evidence.md"
        ).read_text(encoding="utf-8").lower()
        forbidden_source_phrases = (
            "queer artist",
            "escaped iran",
            "iranian passport",
            "sexual identity",
            "passport",
            "sanctions",
        )
        for phrase in forbidden_source_phrases:
            self.assertNotIn(phrase, visitor_text, phrase)
            self.assertNotIn(phrase, research_text, phrase)

        immutable_source = (
            REPO_ROOT / "records/programs/6529NM-AP-01/outcomes/OUT-011.json"
        ).read_text(encoding="utf-8").lower()
        self.assertIn("iranian passport", immutable_source)

    def test_publication_authority_candidate_has_no_unearned_independent_review(self) -> None:
        authority_text = (
            REPO_ROOT
            / "records/programs/6529NM-AP-01/public/publication-authority-amendment-2026-08-08-005.md"
        ).read_text(encoding="utf-8")
        self.assertIn("candidate publication authority", authority_text)
        self.assertIn("Independent exact-commit review", authority_text)
        self.assertIn("reviewer identity and review time are not asserted", authority_text)
        self.assertIn("no independent approval", authority_text)
        self.assertIn("is claimed here", authority_text)

    def test_historical_authority_and_withdrawal_are_superseded_by_active_display_authority(self) -> None:
        accessibility = load_json(f"media/programs/{PROGRAM_ID}/accessibility.json")
        accessibility_by_alias = {
            item["record_id"].split(f"{PROGRAM_ID}-", 1)[1]: item["public_widths"]
            for item in accessibility["items"]
        }
        manifest = load_json(f"records/programs/{PROGRAM_ID}/media-manifest.json")
        manifest_by_alias = {
            item["record_id"].split(f"{PROGRAM_ID}-", 1)[1]: item["presentation"]["public_widths"]
            for item in manifest["items"]
        }
        authority_text = (
            REPO_ROOT
            / "records/programs/6529NM-AP-01/public/publication-authority-amendment-2026-08-08-005.md"
        ).read_text(encoding="utf-8")
        rows = {
            match.group(1): {
                "authority": match.group(2),
                "widths": [int(value.strip()) for value in match.group(3).split(",")],
            }
            for match in re.finditer(
                r"^\| (OUT-\d{3}) \| `([^`]+)` \| ([0-9, ]+) \|",
                authority_text,
                re.MULTILINE,
            )
        }
        expected_aliases = {f"OUT-{index:03d}" for index in range(1, 17)}
        self.assertEqual(expected_aliases, set(rows))
        self.assertEqual(16, len(rows))
        for alias in sorted(expected_aliases):
            self.assertEqual("PROVISIONAL_EDITORIAL_DISPLAY_LIMITED", rows[alias]["authority"])
            self.assertEqual(EXPECTED_WIDTHS[f"{PROGRAM_ID}-{alias}"], accessibility_by_alias[alias], alias)
            self.assertEqual(EXPECTED_WIDTHS[f"{PROGRAM_ID}-{alias}"], manifest_by_alias[alias], alias)
            self.assertTrue(rows[alias]["widths"], alias)
        withdrawal = (
            REPO_ROOT
            / "records/programs/6529NM-AP-01/public/media-delivery-withdrawal-amendment-2026-08-09.md"
        ).read_text(encoding="utf-8")
        self.assertIn("Supersedes for current delivery state", withdrawal)
        self.assertIn("amendments 004, 005, 006", withdrawal)
        current_authority = (
            REPO_ROOT
            / "records/programs/6529NM-AP-01/public/media-display-authorization-amendment-2026-08-11.md"
        ).read_text(encoding="utf-8")
        self.assertIn("6529NM-AP-01-MEDIA-DISPLAY-2026-08-11-009", current_authority)
        self.assertIn("retains the 9 August withdrawal as an append-only predecessor", current_authority)

    def test_current_authority_binds_active_manifest_and_retains_withdrawal_history(self) -> None:
        manifest = load_json(f"records/programs/{PROGRAM_ID}/media-manifest.json")
        amendment = (
            REPO_ROOT / "records/programs/6529NM-AP-01/public/media-delivery-withdrawal-amendment-2026-08-09.md"
        ).read_text(encoding="utf-8")
        self.assertEqual("approved_by_reviewed_display_authority", manifest["delivery"]["status"])
        self.assertEqual("6529NM-AP-01-MEDIA-DISPLAY-2026-08-11-009", manifest["delivery"]["authority_record_id"])
        self.assertIn("86b0735e4a81030f94d29973001d3b2751ba8b75", amendment)
        self.assertIn("sha256:f023c79f44b8440813c11b9ebf9d428d06d399ae87d846d6e08b9e6db459cd85", amendment)

    def test_current_delivery_inventory_is_closed_and_rendering_under_authority(self) -> None:
        manifest = load_json(f"records/programs/{PROGRAM_ID}/media-manifest.json")
        self.assertEqual("approved_by_reviewed_display_authority", manifest["delivery"]["status"])
        self.assertEqual("6529NM-AP-01-MEDIA-DISPLAY-2026-08-11-009", manifest["delivery"]["authority_record_id"])
        self.assertEqual(
            EXPECTED_WIDTHS,
            {item["record_id"]: item["presentation"]["public_widths"] for item in manifest["items"]},
        )
        media_root = REPO_ROOT / "media/programs/6529NM-AP-01"
        self.assertEqual(44, len(sorted(media_root.rglob("*.webp"))))
        visitor_bundle = (
            REPO_ROOT / "records/publication/visitor-corpus-bundle-v1.json"
        ).read_text(encoding="utf-8")
        self.assertNotIn("submitted_high_resolution_source", visitor_bundle)
        self.assertNotIn("what is visible in the current presentation derivative", visitor_bundle)
        self.assertNotIn("Existing WebP derivatives may be referenced", visitor_bundle)
        self.assertNotIn("visual descriptions of the current presentation derivatives", visitor_bundle)
        self.assertNotIn("The 640px public derivative keeps its text illegible", visitor_bundle)
        self.assertNotIn("The public derivative shows", visitor_bundle)
        self.assertNotIn("the current derivative", visitor_bundle)
        self.assertNotIn("technical 640 derivative", visitor_bundle)
        self.assertNotIn("No person in the current frame", visitor_bundle)
        self.assertNotIn("No identifiable person in derivative", visitor_bundle)
        self.assertNotIn("No person visible in the current frame", visitor_bundle)
        self.assertNotIn("artist’s mother", visitor_bundle)
        self.assertNotIn("# Eric Pan (pandelic)", visitor_bundle)
        self.assertNotIn("# Priyanka Patel (priyanka)", visitor_bundle)
        ikertje_profile = (
            REPO_ROOT / "records/programs/6529NM-AP-01/public/artists/ikertje.md"
        ).read_text(encoding="utf-8")
        self.assertNotIn("Berlin Wall Memorial", ikertje_profile)
        self.assertNotIn("records/programs/6529NM-AP-01/public/accessibility-amendment.md", visitor_bundle)
        self.assertNotIn("records/programs/6529NM-AP-01/public/accessibility-amendment-2026-08-08-002.md", visitor_bundle)
        self.assertNotIn("records/programs/6529NM-AP-01/public/accessibility-amendment-2026-08-08-003.md", visitor_bundle)

    def test_visitor_copy_has_no_exhibition_or_formulaic_scaffolding_terms(self) -> None:
        public_root = REPO_ROOT / "records/programs/6529NM-AP-01/public"
        visitor_paths = [
            public_root / "curated-acquisition.md",
            public_root / "curatorial-essay.md",
            *sorted((public_root / "artists").glob("*.md")),
            *sorted((public_root / "works").glob("*.md")),
        ]
        visitor_text = "\n".join(path.read_text(encoding="utf-8") for path in visitor_paths).lower()
        for forbidden in ("exhibition", "neither", "rather than", "schema", "manifest", "deployment"):
            self.assertNotIn(forbidden, visitor_text, forbidden)

    def test_work_pages_project_only_declared_presentation_urls(self) -> None:
        public_root = REPO_ROOT / "records/programs/6529NM-AP-01/public"
        manifest = load_json(f"records/programs/{PROGRAM_ID}/media-manifest.json")
        work_text = "\n".join(path.read_text(encoding="utf-8") for path in (public_root / "works").glob("*.md"))
        visitor_text = "\n".join(
            path.read_text(encoding="utf-8")
            for path in (
                public_root / "README.md",
                public_root / "curated-acquisition.md",
                public_root / "curatorial-essay.md",
                *(public_root / "artists").glob("*.md"),
            )
        )
        for item in manifest["items"]:
            presentation = item["presentation"]
            for derivative in presentation["derivatives"]:
                self.assertNotIn(derivative["url"], work_text, item["record_id"])
            source_url = item["source"]["url"]
            self.assertNotIn(source_url, work_text, item["record_id"])
            self.assertNotIn(source_url, visitor_text, item["record_id"])


if __name__ == "__main__":
    unittest.main()
