"""Tests for AtlasAI core/permission.py — PermissionSystem."""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "AIEngine" / "AtlasAIEngine"))

from core.permission import PermissionSystem


class TestPermissionSystemConstruction(unittest.TestCase):
    def test_default_state_allows_any_tool(self):
        ps = PermissionSystem()
        self.assertTrue(ps.is_allowed("any_tool", {}))

    def test_default_state_allows_any_path(self):
        ps = PermissionSystem()
        self.assertTrue(ps.is_path_allowed("/any/path"))


class TestPermissionSystemBlockTool(unittest.TestCase):
    def setUp(self):
        self.ps = PermissionSystem()

    def test_blocked_tool_is_denied(self):
        self.ps.block_tool("dangerous_tool")
        self.assertFalse(self.ps.is_allowed("dangerous_tool", {}))

    def test_non_blocked_tool_is_allowed(self):
        self.ps.block_tool("dangerous_tool")
        self.assertTrue(self.ps.is_allowed("safe_tool", {}))

    def test_block_multiple_tools(self):
        self.ps.block_tool("tool_a")
        self.ps.block_tool("tool_b")
        self.assertFalse(self.ps.is_allowed("tool_a", {}))
        self.assertFalse(self.ps.is_allowed("tool_b", {}))
        self.assertTrue(self.ps.is_allowed("tool_c", {}))


class TestPermissionSystemAllowOnlyTools(unittest.TestCase):
    def setUp(self):
        self.ps = PermissionSystem()

    def test_allowlist_permits_listed_tool(self):
        self.ps.allow_only_tools(["read_file", "list_dir"])
        self.assertTrue(self.ps.is_allowed("read_file", {}))
        self.assertTrue(self.ps.is_allowed("list_dir", {}))

    def test_allowlist_blocks_unlisted_tool(self):
        self.ps.allow_only_tools(["read_file"])
        self.assertFalse(self.ps.is_allowed("write_file", {}))

    def test_empty_allowlist_blocks_all_tools(self):
        self.ps.allow_only_tools([])
        self.assertFalse(self.ps.is_allowed("read_file", {}))

    def test_blocklist_takes_priority_over_allowlist(self):
        self.ps.allow_only_tools(["read_file"])
        self.ps.block_tool("read_file")
        self.assertFalse(self.ps.is_allowed("read_file", {}))


class TestPermissionSystemPathChecks(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.safe_dir = Path(self.tmp.name) / "safe"
        self.safe_dir.mkdir()
        self.blocked_dir = Path(self.tmp.name) / "blocked"
        self.blocked_dir.mkdir()

    def tearDown(self):
        self.tmp.cleanup()

    def test_allowed_dir_permits_path_inside_it(self):
        ps = PermissionSystem()
        ps.allow_dir(self.safe_dir)
        inside = self.safe_dir / "file.txt"
        self.assertTrue(ps.is_path_allowed(str(inside)))

    def test_allowed_dir_blocks_path_outside_it(self):
        ps = PermissionSystem()
        ps.allow_dir(self.safe_dir)
        outside = Path(self.tmp.name) / "other" / "file.txt"
        self.assertFalse(ps.is_path_allowed(str(outside)))

    def test_blocked_dir_denies_path_inside_it(self):
        ps = PermissionSystem()
        ps.block_dir(self.blocked_dir)
        inside = self.blocked_dir / "secret.txt"
        self.assertFalse(ps.is_path_allowed(str(inside)))

    def test_blocked_dir_allows_path_outside_it(self):
        ps = PermissionSystem()
        ps.block_dir(self.blocked_dir)
        outside = self.safe_dir / "ok.txt"
        self.assertTrue(ps.is_path_allowed(str(outside)))

    def test_safe_write_allowed_path(self):
        ps = PermissionSystem()
        ps.allow_dir(self.safe_dir)
        self.assertTrue(ps.safe_write(str(self.safe_dir / "out.txt")))

    def test_safe_write_blocked_path(self):
        ps = PermissionSystem()
        ps.block_dir(self.blocked_dir)
        self.assertFalse(ps.safe_write(str(self.blocked_dir / "out.txt")))

    def test_safe_delete_allowed_path(self):
        ps = PermissionSystem()
        ps.allow_dir(self.safe_dir)
        self.assertTrue(ps.safe_delete(str(self.safe_dir / "old.txt")))

    def test_safe_delete_blocked_path(self):
        ps = PermissionSystem()
        ps.block_dir(self.blocked_dir)
        self.assertFalse(ps.safe_delete(str(self.blocked_dir / "old.txt")))


class TestPermissionSystemIsAllowedWithArgs(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.safe_dir = Path(self.tmp.name) / "safe"
        self.safe_dir.mkdir()
        self.blocked_dir = Path(self.tmp.name) / "blocked"
        self.blocked_dir.mkdir()

    def tearDown(self):
        self.tmp.cleanup()

    def test_args_with_allowed_path_value(self):
        ps = PermissionSystem()
        ps.allow_dir(self.safe_dir)
        args = {"path": str(self.safe_dir / "file.txt")}
        self.assertTrue(ps.is_allowed("read_file", args))

    def test_args_with_blocked_path_value(self):
        ps = PermissionSystem()
        ps.block_dir(self.blocked_dir)
        args = {"path": str(self.blocked_dir / "secret.txt")}
        self.assertFalse(ps.is_allowed("read_file", args))

    def test_args_with_no_path_strings(self):
        ps = PermissionSystem()
        ps.allow_dir(self.safe_dir)
        args = {"count": 5, "flag": True}
        self.assertTrue(ps.is_allowed("count_items", args))

    def test_args_with_nested_dict_path(self):
        ps = PermissionSystem()
        ps.block_dir(self.blocked_dir)
        args = {"options": {"output": str(self.blocked_dir / "out.txt")}}
        self.assertFalse(ps.is_allowed("export", args))

    def test_args_with_list_of_paths(self):
        ps = PermissionSystem()
        ps.block_dir(self.blocked_dir)
        args = {"files": [str(self.blocked_dir / "a.txt"), str(self.safe_dir / "b.txt")]}
        self.assertFalse(ps.is_allowed("batch_read", args))

    def test_args_with_list_of_safe_paths(self):
        ps = PermissionSystem()
        ps.allow_dir(self.safe_dir)
        args = {"files": [str(self.safe_dir / "a.txt"), str(self.safe_dir / "b.txt")]}
        self.assertTrue(ps.is_allowed("batch_read", args))

    def test_non_dict_args_are_allowed(self):
        ps = PermissionSystem()
        self.assertTrue(ps.is_allowed("any_tool", "not a dict"))  # type: ignore[arg-type]


class TestPermissionSystemGrantRevoke(unittest.TestCase):
    """Test that permission state can be changed after initial setup."""

    def setUp(self):
        self.ps = PermissionSystem()

    def test_allow_only_then_extend(self):
        self.ps.allow_only_tools(["tool_a"])
        self.assertFalse(self.ps.is_allowed("tool_b", {}))
        # Extend the allowlist by calling again (replaces it)
        self.ps.allow_only_tools(["tool_a", "tool_b"])
        self.assertTrue(self.ps.is_allowed("tool_b", {}))

    def test_block_additional_tools_incrementally(self):
        self.ps.block_tool("tool_x")
        self.assertTrue(self.ps.is_allowed("tool_y", {}))
        self.ps.block_tool("tool_y")
        self.assertFalse(self.ps.is_allowed("tool_y", {}))

    def test_add_multiple_allowed_dirs(self):
        tmp = tempfile.TemporaryDirectory()
        dir_a = Path(tmp.name) / "a"
        dir_b = Path(tmp.name) / "b"
        dir_a.mkdir()
        dir_b.mkdir()
        self.ps.allow_dir(dir_a)
        self.ps.allow_dir(dir_b)
        self.assertTrue(self.ps.is_path_allowed(str(dir_a / "file.txt")))
        self.assertTrue(self.ps.is_path_allowed(str(dir_b / "file.txt")))
        tmp.cleanup()


if __name__ == "__main__":
    unittest.main()
