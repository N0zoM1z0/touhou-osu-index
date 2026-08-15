import unittest

from touhou_osu.sources import _collector_entry, parse_beatmap_links, parse_beatmapset_page, parse_wiki_links


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


if __name__ == "__main__":
    unittest.main()
