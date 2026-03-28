"""Tests for AtlasAI core/tool_registry.py — ToolRegistry."""

import json
import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "AIEngine" / "AtlasAIEngine"))

from core.tool_registry import ToolRegistry


def _echo_def():
    return {
        "name": "echo",
        "description": "Echoes its input.",
        "parameters": {"type": "object", "properties": {"text": {"type": "string"}}},
    }

def _greet_def():
    return {
        "name": "greet",
        "description": "Returns a greeting.",
        "parameters": {"type": "object", "properties": {"name": {"type": "string"}}},
    }


class TestToolRegistryRegister(unittest.TestCase):
    def setUp(self):
        self.registry = ToolRegistry()

    def test_register_basic(self):
        self.registry.register(_echo_def())
        self.assertIn("echo", [t["name"] for t in self.registry.list_tools()])

    def test_register_with_callable(self):
        func = MagicMock(return_value="pong")
        self.registry.register(_echo_def(), func)
        self.assertIs(self.registry.get_callable("echo"), func)

    def test_register_without_callable_has_no_callable(self):
        self.registry.register(_echo_def())
        self.assertIsNone(self.registry.get_callable("echo"))

    def test_register_multiple_tools(self):
        self.registry.register(_echo_def())
        self.registry.register(_greet_def())
        names = [t["name"] for t in self.registry.list_tools()]
        self.assertIn("echo", names)
        self.assertIn("greet", names)

    def test_register_overwrites_existing(self):
        self.registry.register(_echo_def())
        updated = {**_echo_def(), "description": "Updated description."}
        self.registry.register(updated)
        result = self.registry.get("echo")
        self.assertEqual(result["description"], "Updated description.")


class TestToolRegistryGet(unittest.TestCase):
    def setUp(self):
        self.registry = ToolRegistry()
        self.registry.register(_echo_def())

    def test_get_existing_tool(self):
        tool = self.registry.get("echo")
        self.assertIsNotNone(tool)
        self.assertEqual(tool["name"], "echo")

    def test_get_missing_tool_returns_none(self):
        self.assertIsNone(self.registry.get("nonexistent"))

    def test_get_includes_callable_key_when_registered(self):
        func = MagicMock()
        self.registry.register(_echo_def(), func)
        tool = self.registry.get("echo")
        self.assertIn("_callable", tool)
        self.assertIs(tool["_callable"], func)

    def test_get_no_callable_key_when_no_func(self):
        tool = self.registry.get("echo")
        self.assertNotIn("_callable", tool)


class TestToolRegistryListTools(unittest.TestCase):
    def setUp(self):
        self.registry = ToolRegistry()

    def test_list_tools_empty(self):
        self.assertEqual(self.registry.list_tools(), [])

    def test_list_tools_returns_all(self):
        self.registry.register(_echo_def())
        self.registry.register(_greet_def())
        tools = self.registry.list_tools()
        self.assertEqual(len(tools), 2)

    def test_list_tools_result_is_a_new_list(self):
        self.registry.register(_echo_def())
        list_a = self.registry.list_tools()
        list_b = self.registry.list_tools()
        self.assertIsNot(list_a, list_b)

    def test_list_tools_contains_registered_names(self):
        self.registry.register(_echo_def())
        self.registry.register(_greet_def())
        names = {t["name"] for t in self.registry.list_tools()}
        self.assertEqual(names, {"echo", "greet"})


class TestToolRegistryRegisterFromFile(unittest.TestCase):
    def setUp(self):
        self.registry = ToolRegistry()

    def test_register_from_file_list_format(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            tools_file = Path(tmp) / "tools.json"
            tools_file.write_text(json.dumps([_echo_def(), _greet_def()]))
            self.registry.register_from_file(tools_file)
            names = [t["name"] for t in self.registry.list_tools()]
            self.assertIn("echo", names)
            self.assertIn("greet", names)

    def test_register_from_file_dict_format(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            tools_file = Path(tmp) / "tools.json"
            tools_file.write_text(json.dumps({"tools": [_echo_def()]}))
            self.registry.register_from_file(tools_file)
            self.assertIsNotNone(self.registry.get("echo"))

    def test_register_from_file_missing_file_is_silent(self):
        # Should not raise; simply logs a warning
        self.registry.register_from_file("/nonexistent/path/tools.json")
        self.assertEqual(self.registry.list_tools(), [])

    def test_register_from_file_invalid_json_raises(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            bad_file = Path(tmp) / "tools.json"
            bad_file.write_text("not valid json {{")
            with self.assertRaises(json.JSONDecodeError):
                self.registry.register_from_file(bad_file)

    def test_register_from_file_with_function_path_unresolvable(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            tool_with_func = {**_echo_def(), "function": "no.such.module.func"}
            tools_file = Path(tmp) / "tools.json"
            tools_file.write_text(json.dumps([tool_with_func]))
            # Should not raise; logs a warning and registers without callable
            self.registry.register_from_file(tools_file)
            self.assertIsNotNone(self.registry.get("echo"))
            self.assertIsNone(self.registry.get_callable("echo"))


class TestToolRegistryRegisterFromDirectory(unittest.TestCase):
    def setUp(self):
        self.registry = ToolRegistry()

    def test_register_from_directory_finds_nested_files(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            sub = Path(tmp) / "module_a"
            sub.mkdir()
            (sub / "tools.json").write_text(json.dumps([_echo_def()]))
            sub2 = Path(tmp) / "module_b"
            sub2.mkdir()
            (sub2 / "tools.json").write_text(json.dumps([_greet_def()]))
            self.registry.register_from_directory(tmp)
            names = [t["name"] for t in self.registry.list_tools()]
            self.assertIn("echo", names)
            self.assertIn("greet", names)

    def test_register_from_directory_empty_dir(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            self.registry.register_from_directory(tmp)
            self.assertEqual(self.registry.list_tools(), [])

    def test_register_from_directory_no_tools_json(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "other.json").write_text("{}")
            self.registry.register_from_directory(tmp)
            self.assertEqual(self.registry.list_tools(), [])


class TestToolRegistryCall(unittest.TestCase):
    def setUp(self):
        self.registry = ToolRegistry()

    def test_callable_is_invoked(self):
        func = MagicMock(return_value=42)
        self.registry.register(_echo_def(), func)
        result = self.registry.get_callable("echo")("hello")
        func.assert_called_once_with("hello")
        self.assertEqual(result, 42)

    def test_get_callable_missing_returns_none(self):
        self.assertIsNone(self.registry.get_callable("missing"))


if __name__ == "__main__":
    unittest.main()
