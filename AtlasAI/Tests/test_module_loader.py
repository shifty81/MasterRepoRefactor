"""Tests for AtlasAI core/module_loader.py — ModuleLoader."""

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "AIEngine" / "AtlasAIEngine"))

from core.module_loader import ModuleLoader
from core.tool_registry import ToolRegistry


def _make_module_dir(parent: Path, name: str, meta: dict, tools: list | None = None) -> Path:
    """Helper to create a module directory with a manifest and optional tools.json."""
    module_dir = parent / name
    module_dir.mkdir(parents=True, exist_ok=True)
    (module_dir / "module.json").write_text(json.dumps(meta))
    if tools is not None:
        (module_dir / "tools.json").write_text(json.dumps(tools))
    return module_dir


class TestModuleLoaderConstruction(unittest.TestCase):
    def test_stores_modules_dir(self):
        registry = ToolRegistry()
        loader = ModuleLoader("/some/path", registry)
        self.assertEqual(loader.modules_dir, Path("/some/path"))

    def test_stores_tool_registry(self):
        registry = ToolRegistry()
        loader = ModuleLoader("/some/path", registry)
        self.assertIs(loader.tool_registry, registry)

    def test_initially_no_loaded_modules(self):
        registry = ToolRegistry()
        loader = ModuleLoader("/some/path", registry)
        self.assertEqual(loader.loaded_modules, {})


class TestModuleLoaderLoadAll(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.modules_dir = Path(self.tmp.name)
        self.registry = ToolRegistry()

    def tearDown(self):
        self.tmp.cleanup()

    def test_load_all_missing_directory_is_silent(self):
        loader = ModuleLoader(self.modules_dir / "nonexistent", self.registry)
        loader.load_all()  # Should not raise
        self.assertEqual(loader.loaded_modules, {})

    def test_load_all_single_module(self):
        _make_module_dir(self.modules_dir, "weather", {"name": "weather", "version": "1.0"})
        loader = ModuleLoader(self.modules_dir, self.registry)
        loader.load_all()
        self.assertIn("weather", loader.loaded_modules)

    def test_load_all_multiple_modules(self):
        _make_module_dir(self.modules_dir, "search", {"name": "search"})
        _make_module_dir(self.modules_dir, "files", {"name": "files"})
        loader = ModuleLoader(self.modules_dir, self.registry)
        loader.load_all()
        modules = loader.loaded_modules
        self.assertIn("search", modules)
        self.assertIn("files", modules)

    def test_load_all_registers_tools(self):
        tools = [{"name": "do_search", "description": "Performs a search."}]
        _make_module_dir(self.modules_dir, "search", {"name": "search"}, tools=tools)
        loader = ModuleLoader(self.modules_dir, self.registry)
        loader.load_all()
        self.assertIsNotNone(self.registry.get("do_search"))

    def test_load_all_module_without_tools_json(self):
        _make_module_dir(self.modules_dir, "noop", {"name": "noop"}, tools=None)
        loader = ModuleLoader(self.modules_dir, self.registry)
        loader.load_all()
        self.assertIn("noop", loader.loaded_modules)
        self.assertEqual(self.registry.list_tools(), [])

    def test_load_all_skips_dirs_without_manifest(self):
        no_manifest = self.modules_dir / "orphan"
        no_manifest.mkdir()
        loader = ModuleLoader(self.modules_dir, self.registry)
        loader.load_all()
        self.assertEqual(loader.loaded_modules, {})

    def test_load_all_falls_back_to_dirname_when_no_name_in_meta(self):
        _make_module_dir(self.modules_dir, "mymod", {})  # no "name" key in manifest
        loader = ModuleLoader(self.modules_dir, self.registry)
        loader.load_all()
        self.assertIn("mymod", loader.loaded_modules)

    def test_load_all_preserves_module_metadata(self):
        meta = {"name": "analytics", "version": "2.1", "author": "atlas"}
        _make_module_dir(self.modules_dir, "analytics", meta)
        loader = ModuleLoader(self.modules_dir, self.registry)
        loader.load_all()
        self.assertEqual(loader.loaded_modules["analytics"]["version"], "2.1")
        self.assertEqual(loader.loaded_modules["analytics"]["author"], "atlas")


class TestModuleLoaderInvalidManifest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.modules_dir = Path(self.tmp.name)
        self.registry = ToolRegistry()

    def tearDown(self):
        self.tmp.cleanup()

    def test_invalid_json_in_manifest_is_handled_gracefully(self):
        bad_dir = self.modules_dir / "bad_module"
        bad_dir.mkdir()
        (bad_dir / "module.json").write_text("{ invalid json {{")
        loader = ModuleLoader(self.modules_dir, self.registry)
        loader.load_all()  # Should not raise; logs an error
        self.assertNotIn("bad_module", loader.loaded_modules)

    def test_loaded_modules_returns_copy(self):
        _make_module_dir(self.modules_dir, "snap", {"name": "snap"})
        loader = ModuleLoader(self.modules_dir, self.registry)
        loader.load_all()
        snapshot = loader.loaded_modules
        # Adding a key to the returned dict does not affect the internal state
        snapshot["injected"] = {}
        self.assertNotIn("injected", loader.loaded_modules)


if __name__ == "__main__":
    unittest.main()
