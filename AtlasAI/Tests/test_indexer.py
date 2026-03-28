"""Tests for AtlasAI core/indexer.py — ProjectIndexer."""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "AIEngine" / "AtlasAIEngine"))

from core.indexer import IndexEntry, ProjectIndexer


def _write(path: Path, content: str = "hello") -> None:
    path.write_text(content, encoding="utf-8")


class TestProjectIndexerIndexDirectory(unittest.TestCase):
    def setUp(self):
        self.indexer = ProjectIndexer()
        self.tmp = tempfile.mkdtemp()
        self.root = Path(self.tmp)

    def test_empty_directory_returns_zero(self):
        count = self.indexer.index_directory(self.root)
        self.assertEqual(count, 0)

    def test_single_file_returns_one(self):
        _write(self.root / "main.py")
        count = self.indexer.index_directory(self.root)
        self.assertEqual(count, 1)

    def test_multiple_files_counted(self):
        _write(self.root / "a.py")
        _write(self.root / "b.cpp")
        _write(self.root / "c.md")
        count = self.indexer.index_directory(self.root)
        self.assertEqual(count, 3)

    def test_non_directory_returns_zero(self):
        f = self.root / "file.txt"
        _write(f)
        count = self.indexer.index_directory(f)
        self.assertEqual(count, 0)

    def test_max_depth_one_excludes_nested(self):
        sub = self.root / "subdir"
        sub.mkdir()
        _write(self.root / "top.py")
        _write(sub / "nested.py")
        count = self.indexer.index_directory(self.root, max_depth=1)
        self.assertEqual(count, 1)

    def test_max_depth_two_includes_one_level_deep(self):
        sub = self.root / "subdir"
        sub.mkdir()
        _write(self.root / "top.py")
        _write(sub / "nested.py")
        count = self.indexer.index_directory(self.root, max_depth=2)
        self.assertEqual(count, 2)

    def test_kind_mapped_correctly_for_python(self):
        _write(self.root / "script.py")
        self.indexer.index_directory(self.root)
        entry = self.indexer.get("script.py")
        self.assertIsNotNone(entry)
        self.assertEqual(entry.kind, "source")

    def test_kind_mapped_correctly_for_markdown(self):
        _write(self.root / "README.md")
        self.indexer.index_directory(self.root)
        entry = self.indexer.get("README.md")
        self.assertEqual(entry.kind, "doc")

    def test_kind_mapped_correctly_for_yaml(self):
        _write(self.root / "config.yaml")
        self.indexer.index_directory(self.root)
        entry = self.indexer.get("config.yaml")
        self.assertEqual(entry.kind, "data")

    def test_unknown_extension_gets_kind_other(self):
        _write(self.root / "archive.xyz")
        self.indexer.index_directory(self.root)
        entry = self.indexer.get("archive.xyz")
        self.assertEqual(entry.kind, "other")

    def test_indexed_entry_has_content_hash(self):
        _write(self.root / "main.py", "print('hi')")
        self.indexer.index_directory(self.root)
        entry = self.indexer.get("main.py")
        self.assertTrue(entry.content_hash)

    def test_indexed_entry_has_size(self):
        content = "x" * 100
        _write(self.root / "data.txt", content)
        self.indexer.index_directory(self.root)
        entry = self.indexer.get("data.txt")
        self.assertEqual(entry.size, 100)

    def test_index_file_single_file(self):
        f = self.root / "solo.py"
        _write(f)
        result = self.indexer.index_file(f)
        self.assertTrue(result)
        self.assertEqual(self.indexer.count(), 1)


class TestProjectIndexerSearch(unittest.TestCase):
    def setUp(self):
        self.indexer = ProjectIndexer()
        self.tmp = tempfile.mkdtemp()
        self.root = Path(self.tmp)
        _write(self.root / "main.py")
        _write(self.root / "utils.py")
        _write(self.root / "README.md")
        _write(self.root / "config.yaml")
        self.indexer.index_directory(self.root)

    def test_search_by_substring_finds_match(self):
        results = self.indexer.search("main")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].path, "main.py")

    def test_search_case_insensitive(self):
        results = self.indexer.search("README")
        self.assertEqual(len(results), 1)

    def test_search_case_insensitive_lowercase(self):
        results = self.indexer.search("readme")
        self.assertEqual(len(results), 1)

    def test_search_no_results_returns_empty(self):
        results = self.indexer.search("nonexistent_xyz")
        self.assertEqual(results, [])

    def test_search_by_kind_filters(self):
        results = self.indexer.search("", kind="source")
        kinds = {e.kind for e in results}
        self.assertEqual(kinds, {"source"})

    def test_search_by_kind_doc(self):
        results = self.indexer.search("", kind="doc")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].path, "README.md")

    def test_search_combined_query_and_kind(self):
        results = self.indexer.search("utils", kind="source")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].path, "utils.py")

    def test_search_combined_no_match(self):
        results = self.indexer.search("utils", kind="doc")
        self.assertEqual(results, [])


class TestProjectIndexerListAll(unittest.TestCase):
    def setUp(self):
        self.indexer = ProjectIndexer()
        self.tmp = tempfile.mkdtemp()
        self.root = Path(self.tmp)
        _write(self.root / "a.py")
        _write(self.root / "b.cpp")
        _write(self.root / "c.md")
        self.indexer.index_directory(self.root)

    def test_list_all_returns_all_entries(self):
        self.assertEqual(len(self.indexer.list_all()), 3)

    def test_list_by_kind_source(self):
        source = self.indexer.list_by_kind("source")
        self.assertEqual(len(source), 2)

    def test_list_by_kind_doc(self):
        docs = self.indexer.list_by_kind("doc")
        self.assertEqual(len(docs), 1)

    def test_list_by_kind_unknown_returns_empty(self):
        result = self.indexer.list_by_kind("nonexistent_kind")
        self.assertEqual(result, [])

    def test_count_correct(self):
        self.assertEqual(self.indexer.count(), 3)

    def test_to_dict_has_required_keys(self):
        entry = self.indexer.list_all()[0]
        d = entry.to_dict()
        for key in ("path", "kind", "size", "content_hash", "tags"):
            self.assertIn(key, d)


class TestProjectIndexerClear(unittest.TestCase):
    def setUp(self):
        self.indexer = ProjectIndexer()
        self.tmp = tempfile.mkdtemp()
        self.root = Path(self.tmp)
        _write(self.root / "file.py")
        self.indexer.index_directory(self.root)

    def test_clear_resets_count(self):
        self.assertGreater(self.indexer.count(), 0)
        self.indexer.clear()
        self.assertEqual(self.indexer.count(), 0)

    def test_clear_list_all_empty(self):
        self.indexer.clear()
        self.assertEqual(self.indexer.list_all(), [])

    def test_clear_resets_root(self):
        self.indexer.clear()
        self.assertIsNone(self.indexer._root)

    def test_can_reindex_after_clear(self):
        self.indexer.clear()
        _write(self.root / "new.py")
        count = self.indexer.index_directory(self.root)
        # Both file.py and new.py should be found
        self.assertGreaterEqual(count, 1)


if __name__ == "__main__":
    unittest.main()
