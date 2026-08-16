from pathlib import Path

path = Path("tests/test_sources.py")
text = path.read_text(encoding="utf-8")
old = '''        mock_get_text.return_value = """
        <a href="https://osu.ppy.sh/beatmapsets/101#osu/1">
          <span class="beatmap-pack-items__artist">Artist</span>
          <span class="beatmap-pack-items__title">Title</span>
        </a>
        """
        with self.assertRaisesRegex(RuntimeError, "no longer contains audited beatmapsets"):
            import_official_pack({"tag": "A99", "verified_ids": [101, 202]})
'''
new = '''        mock_get_text.return_value = """
        <a href="https://osu.ppy.sh/beatmapsets/101#osu/1">
          <span class="beatmap-pack-items__artist">Artist</span>
          <span class="beatmap-pack-items__title">Title</span>
        </a>
        <a href="https://osu.ppy.sh/beatmapsets/303#osu/3">
          <span class="beatmap-pack-items__artist">Other Artist</span>
          <span class="beatmap-pack-items__title">Other Title</span>
        </a>
        """
        with self.assertRaisesRegex(RuntimeError, "no longer contains audited beatmapsets"):
            import_official_pack({"tag": "A99", "verified_ids": [101, 202]})
'''
if text.count(old) != 1:
    raise SystemExit(f"expected one missing-id fixture, found {text.count(old)}")
path.write_text(text.replace(old, new), encoding="utf-8")
