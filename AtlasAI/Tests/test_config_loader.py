"""Tests for AtlasAI core/config_loader.py — ConfigLoader."""

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "AIEngine" / "AtlasAIEngine"))

from core.config_loader import ConfigLoader


class TestConfigLoaderConstruction(unittest.TestCase):
    def test_default_config_dir(self):
        loader = ConfigLoader()
        self.assertEqual(loader.config_dir, Path("configs"))

    def test_custom_config_dir(self):
        loader = ConfigLoader("/some/dir")
        self.assertEqual(loader.config_dir, Path("/some/dir"))

    def test_initial_data_is_empty(self):
        loader = ConfigLoader()
        self.assertEqual(loader.data, {})


class TestConfigLoaderLoadJSON(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.config_dir = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def _write_json(self, filename, content):
        (self.config_dir / filename).write_text(json.dumps(content))

    def test_load_valid_json(self):
        self._write_json("config.json", {"engine": "atlas", "version": 1})
        loader = ConfigLoader(self.config_dir)
        loader.load("config.json")
        self.assertEqual(loader.get("engine"), "atlas")
        self.assertEqual(loader.get("version"), 1)

    def test_load_nested_json(self):
        self._write_json("config.json", {"database": {"host": "localhost", "port": 5432}})
        loader = ConfigLoader(self.config_dir)
        loader.load("config.json")
        self.assertEqual(loader.get("database.host"), "localhost")
        self.assertEqual(loader.get("database.port"), 5432)

    def test_load_merges_multiple_files(self):
        self._write_json("base.json", {"a": 1})
        self._write_json("extra.json", {"b": 2})
        loader = ConfigLoader(self.config_dir)
        loader.load("base.json")
        loader.load("extra.json")
        self.assertEqual(loader.get("a"), 1)
        self.assertEqual(loader.get("b"), 2)

    def test_load_later_value_overwrites_earlier(self):
        self._write_json("first.json", {"key": "original"})
        self._write_json("second.json", {"key": "overwritten"})
        loader = ConfigLoader(self.config_dir)
        loader.load("first.json")
        loader.load("second.json")
        self.assertEqual(loader.get("key"), "overwritten")


class TestConfigLoaderMissingFile(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.tmp.cleanup()

    def test_load_missing_file_is_silent(self):
        loader = ConfigLoader(self.tmp.name)
        # Should not raise; logs a warning
        loader.load("nonexistent.json")
        self.assertEqual(loader.data, {})

    def test_load_unsupported_extension_is_silent(self):
        cfg = Path(self.tmp.name) / "config.yaml"
        cfg.write_text("key: value\n")
        loader = ConfigLoader(self.tmp.name)
        loader.load("config.yaml")
        self.assertEqual(loader.data, {})


class TestConfigLoaderGet(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        config_file = Path(self.tmp.name) / "config.json"
        config_file.write_text(json.dumps({
            "level1": {
                "level2": {
                    "value": "deep"
                }
            },
            "simple": "flat",
        }))
        self.loader = ConfigLoader(self.tmp.name)
        self.loader.load("config.json")

    def tearDown(self):
        self.tmp.cleanup()

    def test_get_top_level_key(self):
        self.assertEqual(self.loader.get("simple"), "flat")

    def test_get_nested_key(self):
        self.assertEqual(self.loader.get("level1.level2.value"), "deep")

    def test_get_missing_key_returns_none(self):
        self.assertIsNone(self.loader.get("missing"))

    def test_get_missing_key_returns_default(self):
        self.assertEqual(self.loader.get("missing", "fallback"), "fallback")

    def test_get_partial_path_returns_dict(self):
        result = self.loader.get("level1.level2")
        self.assertEqual(result, {"value": "deep"})

    def test_get_too_deep_returns_default(self):
        result = self.loader.get("simple.nonexistent", "default")
        self.assertEqual(result, "default")


class TestConfigLoaderSet(unittest.TestCase):
    def setUp(self):
        self.loader = ConfigLoader()

    def test_set_top_level(self):
        self.loader.set("foo", "bar")
        self.assertEqual(self.loader.get("foo"), "bar")

    def test_set_nested_creates_intermediate_dicts(self):
        self.loader.set("a.b.c", 99)
        self.assertEqual(self.loader.get("a.b.c"), 99)

    def test_set_overwrites_existing(self):
        self.loader.set("x", 1)
        self.loader.set("x", 2)
        self.assertEqual(self.loader.get("x"), 2)

    def test_data_property_returns_copy(self):
        self.loader.set("key", "val")
        snapshot = self.loader.data
        snapshot["key"] = "mutated"
        self.assertEqual(self.loader.get("key"), "val")


if __name__ == "__main__":
    unittest.main()
