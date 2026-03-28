"""Tests for Phase 12 — NovaForge Client/Server CMake wiring."""

import json
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
NOVAFORGE = REPO_ROOT / "NovaForge"


# ---------------------------------------------------------------------------
# Client CMake
# ---------------------------------------------------------------------------

class TestClientCMakeExists(unittest.TestCase):
    def test_client_cmake_exists(self):
        self.assertTrue((NOVAFORGE / "Client/CMakeLists.txt").exists(),
                        "Missing NovaForge/Client/CMakeLists.txt")

    def test_client_cmake_has_novaforge_client_target(self):
        text = (NOVAFORGE / "Client/CMakeLists.txt").read_text(encoding="utf-8")
        self.assertIn("NovaForgeClient", text)

    def test_client_cmake_has_external_includes(self):
        text = (NOVAFORGE / "Client/CMakeLists.txt").read_text(encoding="utf-8")
        # At least one of the expected external header-only libs should be referenced
        self.assertTrue(
            any(lib in text for lib in ("nlohmann", "tinygltf", "stb", "tinyobjloader")),
            "Expected external dep reference not found in Client CMakeLists",
        )

    def test_novaforge_cmake_includes_client(self):
        text = (NOVAFORGE / "CMakeLists.txt").read_text(encoding="utf-8")
        self.assertIn("Client", text)


# ---------------------------------------------------------------------------
# Server CMake
# ---------------------------------------------------------------------------

class TestServerCMakeExists(unittest.TestCase):
    def test_server_cmake_exists(self):
        self.assertTrue((NOVAFORGE / "Server/CMakeLists.txt").exists(),
                        "Missing NovaForge/Server/CMakeLists.txt")

    def test_server_cmake_has_novaforge_server_target(self):
        text = (NOVAFORGE / "Server/CMakeLists.txt").read_text(encoding="utf-8")
        self.assertIn("NovaForgeServer", text)

    def test_server_cmake_references_tests(self):
        text = (NOVAFORGE / "Server/CMakeLists.txt").read_text(encoding="utf-8")
        self.assertTrue(
            "tests" in text or "CTest" in text or "add_test" in text,
            "Server CMakeLists should reference tests or CTest",
        )

    def test_novaforge_cmake_includes_server(self):
        text = (NOVAFORGE / "CMakeLists.txt").read_text(encoding="utf-8")
        self.assertIn("Server", text)


# ---------------------------------------------------------------------------
# Server Config
# ---------------------------------------------------------------------------

class TestServerConfigFiles(unittest.TestCase):
    def test_server_config_json_exists(self):
        self.assertTrue((NOVAFORGE / "Server/server_config.json").exists())

    def test_server_config_schema_exists(self):
        self.assertTrue((NOVAFORGE / "Server/server_config.schema.json").exists())


class TestServerConfigContent(unittest.TestCase):
    def _config(self):
        return json.loads((NOVAFORGE / "Server/server_config.json").read_text(encoding="utf-8"))

    def test_has_version(self):
        self.assertIn("version", self._config())

    def test_has_whitelist_enabled(self):
        self.assertIn("whitelist_enabled", self._config())

    def test_whitelist_enabled_is_bool(self):
        self.assertIsInstance(self._config()["whitelist_enabled"], bool)

    def test_has_max_players(self):
        self.assertIn("max_players", self._config())

    def test_max_players_positive(self):
        self.assertGreater(self._config()["max_players"], 0)

    def test_has_tick_rate(self):
        self.assertIn("tick_rate", self._config())

    def test_has_log_level(self):
        self.assertIn("log_level", self._config())


class TestServerConfigSchemaContent(unittest.TestCase):
    def _schema(self):
        return json.loads((NOVAFORGE / "Server/server_config.schema.json").read_text(encoding="utf-8"))

    def test_is_json_schema(self):
        schema = self._schema()
        self.assertIn("$schema", schema)

    def test_has_properties(self):
        self.assertIn("properties", self._schema())

    def test_schema_covers_version(self):
        self.assertIn("version", self._schema()["properties"])

    def test_schema_covers_whitelist_enabled(self):
        self.assertIn("whitelist_enabled", self._schema()["properties"])

    def test_schema_covers_max_players(self):
        self.assertIn("max_players", self._schema()["properties"])


# ---------------------------------------------------------------------------
# External deps structure
# ---------------------------------------------------------------------------

class TestClientExternalDeps(unittest.TestCase):
    def _check(self, path):
        self.assertTrue((NOVAFORGE / path).exists(), f"Missing: {path}")

    def test_nlohmann_exists(self):
        self._check("Client/App/external/nlohmann")

    def test_stb_exists(self):
        self._check("Client/App/external/stb")

    def test_tinygltf_exists(self):
        self._check("Client/App/external/tinygltf")

    def test_tinyobjloader_exists(self):
        self._check("Client/App/external/tinyobjloader")


# ---------------------------------------------------------------------------
# Shaders present
# ---------------------------------------------------------------------------

class TestClientShadersExist(unittest.TestCase):
    def test_shaders_dir_exists(self):
        self.assertTrue((NOVAFORGE / "Client/App/shaders").is_dir())

    def test_has_at_least_one_vert_shader(self):
        shaders = list((NOVAFORGE / "Client/App/shaders").glob("*.vert"))
        self.assertGreater(len(shaders), 0, "No .vert shaders found")

    def test_has_at_least_one_frag_shader(self):
        shaders = list((NOVAFORGE / "Client/App/shaders").glob("*.frag"))
        self.assertGreater(len(shaders), 0, "No .frag shaders found")
