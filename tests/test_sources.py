import unittest
from unittest.mock import patch

from touhou_osu.sources import (
    _collector_entry,
    import_collector_tournament,
    import_forum_queue,
    parse_beatmap_links,
    parse_beatmapset_page,
    parse_wiki_links,
)


class SourceParserTests(unittest.TestCase):
    def test_parses_official_pack_markup(self):
        text = """
        <a href="https://osu.ppy.sh/beatmapsets/1151630" class="beatmap-pack-items__link">
          <span class="beatmap-pack-items__artist">Rin</span>
          <span class="beatmap-pack-items__title"> - Muenzuka set 09</span>
        </a>
        """
        self.assertEqual(
            parse_beatmap_links(text),
            [{"id": 1151630, "mode": "", "artist": "Rin", "title": "Muenzuka set 09", "text": "Rin - Muenzuka set 09"}],
        )

    def test_parses_wiki_link_mode_and_text(self):
        text = '<a href="https://osu.ppy.sh/beatmapsets/99#mania/123">ZUN – Theme</a>'
        self.assertEqual(parse_beatmap_links(text)[0]["mode"], "mania")
        self.assertEqual(parse_beatmap_links(text)[0]["artist"], "ZUN")

    def test_parses_wiki_json_markdown(self):
        text = r'{"markdown":"1. [FELT - OUR SHIP \\[Enchanted Love\\]](https://osu.ppy.sh/beatmapsets/1188944#mania/2477648)"}'
        item = parse_wiki_links(text)[0]
        self.assertEqual(item["id"], 1188944)
        self.assertEqual(item["mode"], "mania")
        self.assertEqual(item["artist"], "FELT")

    def test_parses_embedded_beatmapset_json(self):
        text = '<script id="json-beatmapset" type="application/json">{"id":42,"artist":"ZUN"}</script>'
        self.assertEqual(parse_beatmapset_page(text)["id"], 42)

    def test_skips_unsubmitted_collector_map(self):
        self.assertIsNone(_collector_entry({"beatmapset": None}, "tournament:1", "verified"))

    def test_imports_every_page_of_forum_queue(self):
        pages = {
            "https://osu.ppy.sh/community/forums/topics/1": """
                <article data-post-id="10"><a href="https://osu.ppy.sh/beatmapsets/1#osu/11">Artist - one</a></article>
                <article data-post-id="20"></article>
            """,
            "https://osu.ppy.sh/community/forums/topics/1?start=20": """
                <article data-post-id="10"><a href="https://osu.ppy.sh/beatmapsets/1#osu/11">Artist - one</a></article>
                <article data-post-id="20"></article>
                <article data-post-id="30"><a href="https://osu.ppy.sh/beatmapsets/2#osu/22">two</a></article>
            """,
            "https://osu.ppy.sh/community/forums/topics/1?start=30": """
                <article data-post-id="20"></article>
                <article data-post-id="30"><a href="https://osu.ppy.sh/beatmapsets/2#osu/22">two</a></article>
            """,
        }
        with patch("touhou_osu.sources.get_text", side_effect=pages.__getitem__):
            entries = import_forum_queue(
                {
                    "slug": "sd_touhou",
                    "url": "https://osu.ppy.sh/community/forums/topics/1",
                }
            )

        self.assertEqual({entry.beatmapset_id for entry in entries}, {1, 2})
        self.assertTrue(all(entry.confidence == "candidate" for entry in entries))
        self.assertTrue(all("forum_queue:sd_touhou" in entry.evidence for entry in entries))

    def test_partial_tournament_pool_stays_candidate(self):
        payload = {
            "rounds": [
                {
                    "mods": [
                        {
                            "maps": [
                                {
                                    "mode": "osu",
                                    "beatmapset": {"id": 42, "artist": "unknown", "title": "unknown"},
                                }
                            ]
                        }
                    ]
                }
            ]
        }
        with patch("touhou_osu.sources.get_json", return_value=payload):
            entries = import_collector_tournament({"id": 526, "trusted": False})

        self.assertEqual(entries[0].confidence, "candidate")
        self.assertEqual(entries[0].evidence, ["tournament_candidate:526"])


if __name__ == "__main__":
    unittest.main()
