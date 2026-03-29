"""Phase 17D tests — Code Intelligence scaffold."""
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent

sys.path.insert(0, str(REPO_ROOT / "AtlasAI" / "AIEngine"))

INTELLIGENCE_DIR = REPO_ROOT / "AtlasAI" / "AIEngine" / "AtlasAIEngine" / "intelligence"
SYMBOL_SEARCH_PANEL_H = REPO_ROOT / "Atlas" / "Editor" / "Panels" / "SymbolSearchPanel.h"
TOOL_LAYER_DIR = REPO_ROOT / "Atlas" / "Editor" / "ToolLayer"


class TestPhase17DIntelligencePackage(unittest.TestCase):
    def test_intelligence_directory_exists(self):
        self.assertTrue(INTELLIGENCE_DIR.is_dir())

    def test_intelligence_init_exists(self):
        self.assertTrue((INTELLIGENCE_DIR / "__init__.py").exists())

    def test_clangd_bridge_file_exists(self):
        self.assertTrue((INTELLIGENCE_DIR / "clangd_bridge.py").exists())

    def test_symbol_index_file_exists(self):
        self.assertTrue((INTELLIGENCE_DIR / "symbol_index.py").exists())


class TestPhase17DClangdBridgeImport(unittest.TestCase):
    def setUp(self):
        from AtlasAIEngine.intelligence.clangd_bridge import ClangdBridge
        self.ClangdBridge = ClangdBridge

    def test_clangd_bridge_init(self):
        bridge = self.ClangdBridge("/fake/workspace")
        self.assertIsNotNone(bridge)

    def test_clangd_bridge_workspace_root_stored(self):
        bridge = self.ClangdBridge("/fake/workspace")
        self.assertEqual(str(bridge.workspace_root), "/fake/workspace")

    def test_clangd_bridge_start_returns_true(self):
        bridge = self.ClangdBridge("/fake/workspace")
        self.assertTrue(bridge.start())

    def test_clangd_bridge_is_running_after_start(self):
        bridge = self.ClangdBridge("/fake/workspace")
        bridge.start()
        self.assertTrue(bridge.is_running())

    def test_clangd_bridge_not_running_initially(self):
        bridge = self.ClangdBridge("/fake/workspace")
        self.assertFalse(bridge.is_running())

    def test_clangd_bridge_stop_sets_not_running(self):
        bridge = self.ClangdBridge("/fake/workspace")
        bridge.start()
        bridge.stop()
        self.assertFalse(bridge.is_running())

    def test_clangd_bridge_find_symbol_returns_list_when_running(self):
        bridge = self.ClangdBridge("/fake/workspace")
        bridge.start()
        result = bridge.find_symbol("MultiSelectionManager")
        self.assertIsInstance(result, list)

    def test_clangd_bridge_find_symbol_returns_empty_when_not_running(self):
        bridge = self.ClangdBridge("/fake/workspace")
        result = bridge.find_symbol("Foo")
        self.assertEqual(result, [])

    def test_clangd_bridge_get_definition_returns_none_when_running(self):
        bridge = self.ClangdBridge("/fake/workspace")
        bridge.start()
        result = bridge.get_definition("foo.cpp", 1, 1)
        self.assertIsNone(result)

    def test_clangd_bridge_get_definition_returns_none_when_not_running(self):
        bridge = self.ClangdBridge("/fake/workspace")
        result = bridge.get_definition("foo.cpp", 1, 1)
        self.assertIsNone(result)

    def test_clangd_bridge_find_references_returns_list_when_running(self):
        bridge = self.ClangdBridge("/fake/workspace")
        bridge.start()
        result = bridge.find_references("foo.cpp", 1, 1)
        self.assertIsInstance(result, list)

    def test_clangd_bridge_find_references_returns_empty_when_not_running(self):
        bridge = self.ClangdBridge("/fake/workspace")
        result = bridge.find_references("foo.cpp", 1, 1)
        self.assertEqual(result, [])

    def test_clangd_bridge_rename_symbol_returns_true_when_running(self):
        bridge = self.ClangdBridge("/fake/workspace")
        bridge.start()
        result = bridge.rename_symbol("foo.cpp", 5, 3, "NewName")
        self.assertTrue(result)

    def test_clangd_bridge_rename_symbol_returns_false_when_not_running(self):
        bridge = self.ClangdBridge("/fake/workspace")
        result = bridge.rename_symbol("foo.cpp", 5, 3, "NewName")
        self.assertFalse(result)


class TestPhase17DSymbolIndex(unittest.TestCase):
    def setUp(self):
        from AtlasAIEngine.intelligence.symbol_index import SymbolIndex, SymbolEntry
        self.SymbolIndex = SymbolIndex
        self.SymbolEntry = SymbolEntry

    def test_symbol_index_init(self):
        idx = self.SymbolIndex(str(TOOL_LAYER_DIR))
        self.assertIsNotNone(idx)

    def test_symbol_index_build_returns_positive(self):
        idx = self.SymbolIndex(str(TOOL_LAYER_DIR))
        count = idx.build()
        self.assertGreater(count, 0)

    def test_symbol_index_search_finds_multi_selection(self):
        idx = self.SymbolIndex(str(TOOL_LAYER_DIR))
        idx.build()
        results = idx.search("MultiSelection")
        names = [r.name for r in results]
        self.assertIn("MultiSelectionManager", names)

    def test_symbol_index_search_case_insensitive(self):
        idx = self.SymbolIndex(str(TOOL_LAYER_DIR))
        idx.build()
        results = idx.search("multiselection")
        self.assertGreater(len(results), 0)

    def test_symbol_index_search_by_kind(self):
        idx = self.SymbolIndex(str(TOOL_LAYER_DIR))
        idx.build()
        results = idx.search("Tool", kind="class")
        self.assertTrue(all(r.kind == "class" for r in results))

    def test_symbol_index_get_by_name_found(self):
        idx = self.SymbolIndex(str(TOOL_LAYER_DIR))
        idx.build()
        entry = idx.get_by_name("MultiSelectionManager")
        self.assertIsNotNone(entry)

    def test_symbol_index_get_by_name_not_found(self):
        idx = self.SymbolIndex(str(TOOL_LAYER_DIR))
        idx.build()
        entry = idx.get_by_name("NonExistentSymbolXYZ")
        self.assertIsNone(entry)

    def test_symbol_index_get_all_returns_list(self):
        idx = self.SymbolIndex(str(TOOL_LAYER_DIR))
        idx.build()
        all_entries = idx.get_all()
        self.assertIsInstance(all_entries, list)

    def test_symbol_index_clear(self):
        idx = self.SymbolIndex(str(TOOL_LAYER_DIR))
        idx.build()
        idx.clear()
        self.assertEqual(len(idx.get_all()), 0)

    def test_symbol_index_clear_then_rebuild(self):
        idx = self.SymbolIndex(str(TOOL_LAYER_DIR))
        idx.build()
        idx.clear()
        count = idx.build()
        self.assertGreater(count, 0)


class TestPhase17DSymbolEntry(unittest.TestCase):
    def setUp(self):
        from AtlasAIEngine.intelligence.symbol_index import SymbolEntry
        self.SymbolEntry = SymbolEntry

    def test_symbol_entry_fields(self):
        entry = self.SymbolEntry(name="Foo", kind="class", file_path="foo.h", line=10)
        self.assertEqual(entry.name, "Foo")
        self.assertEqual(entry.kind, "class")
        self.assertEqual(entry.file_path, "foo.h")
        self.assertEqual(entry.line, 10)

    def test_symbol_entry_is_dataclass(self):
        import dataclasses
        self.assertTrue(dataclasses.is_dataclass(self.SymbolEntry))


class TestPhase17DSymbolSearchPanelHeader(unittest.TestCase):
    def _content(self):
        return SYMBOL_SEARCH_PANEL_H.read_text()

    def test_symbol_search_panel_header_exists(self):
        self.assertTrue(SYMBOL_SEARCH_PANEL_H.exists())

    def test_symbol_search_panel_pragma_once(self):
        self.assertIn("#pragma once", self._content())

    def test_symbol_search_panel_class(self):
        self.assertIn("class SymbolSearchPanel", self._content())

    def test_symbol_search_panel_set_query(self):
        self.assertIn("SetQuery", self._content())

    def test_symbol_search_panel_execute_search(self):
        self.assertIn("ExecuteSearch", self._content())

    def test_symbol_search_panel_navigate_to(self):
        self.assertIn("NavigateTo", self._content())

    def test_symbol_search_panel_search_result_struct(self):
        self.assertIn("SearchResult", self._content())


if __name__ == "__main__":
    unittest.main()
