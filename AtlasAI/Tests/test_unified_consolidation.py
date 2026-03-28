"""Tests for the Unified Repo Consolidation — core orchestration sources and config."""

import json
import sys
import unittest
from pathlib import Path

# Repo root
REPO_ROOT = Path(__file__).resolve().parent.parent.parent


class TestUnifiedOrchestrationSourceFilesExist(unittest.TestCase):
    """Verify the expected orchestration source files are present in the repo."""

    def _check(self, relative_path: str):
        full = REPO_ROOT / relative_path
        self.assertTrue(full.exists(), f"Missing source file: {relative_path}")

    # App / Orchestrator
    def test_app_header(self):
        self._check("NovaForge/App/include/App.h")

    def test_app_source(self):
        self._check("NovaForge/App/src/App.cpp")

    def test_game_orchestrator_header(self):
        self._check("NovaForge/App/include/GameOrchestrator.h")

    def test_game_orchestrator_source(self):
        self._check("NovaForge/App/src/GameOrchestrator.cpp")

    def test_data_registry_header(self):
        self._check("NovaForge/App/include/DataRegistry.h")

    def test_data_registry_source(self):
        self._check("NovaForge/App/src/DataRegistry.cpp")

    def test_main_source(self):
        self._check("NovaForge/App/src/main.cpp")

    # World
    def test_world_header(self):
        self._check("NovaForge/World/World.h")

    def test_world_source(self):
        self._check("NovaForge/World/src/World.cpp")

    # Rendering
    def test_renderer_header(self):
        self._check("Atlas/Engine/Rendering/Renderer.h")

    def test_renderer_source(self):
        self._check("Atlas/Engine/Rendering/Renderer.cpp")

    # Save
    def test_save_manager_header(self):
        self._check("NovaForge/Save/include/SaveManager.h")

    def test_save_manager_source(self):
        self._check("NovaForge/Save/src/SaveManager.cpp")

    # UI
    def test_runtime_ui_shell_header(self):
        self._check("NovaForge/UI/include/RuntimeUIShell.h")

    def test_runtime_ui_shell_source(self):
        self._check("NovaForge/UI/src/RuntimeUIShell.cpp")


class TestBootConfigData(unittest.TestCase):
    """Validate the masterrepo_boot_config.json."""

    def _load_json(self, relative_path: str) -> dict:
        full = REPO_ROOT / relative_path
        self.assertTrue(full.exists(), f"Missing file: {relative_path}")
        return json.loads(full.read_text(encoding="utf-8"))

    def test_boot_config_exists(self):
        path = REPO_ROOT / "NovaForge/Data/Config/masterrepo_boot_config.json"
        self.assertTrue(path.exists(), "Missing masterrepo_boot_config.json")

    def test_boot_config_is_valid_json(self):
        data = self._load_json("NovaForge/Data/Config/masterrepo_boot_config.json")
        self.assertIsInstance(data, dict)

    def test_boot_config_has_build_target(self):
        data = self._load_json("NovaForge/Data/Config/masterrepo_boot_config.json")
        self.assertIn("build_target", data)

    def test_boot_config_has_default_mode(self):
        data = self._load_json("NovaForge/Data/Config/masterrepo_boot_config.json")
        self.assertIn("default_mode", data)


class TestConsolidationDocsExist(unittest.TestCase):
    """Verify the consolidation documentation is present."""

    def test_unified_repo_tree(self):
        path = REPO_ROOT / "Docs/Architecture/Unified_Repo_Tree.md"
        self.assertTrue(path.exists(), "Missing Unified_Repo_Tree.md")

    def test_canonical_ownership_map(self):
        path = REPO_ROOT / "Docs/Architecture/Canonical_Ownership_Map.md"
        self.assertTrue(path.exists(), "Missing Canonical_Ownership_Map.md")

    def test_duplicate_resolution_table(self):
        path = REPO_ROOT / "Docs/Architecture/Duplicate_Resolution_Table.md"
        self.assertTrue(path.exists(), "Missing Duplicate_Resolution_Table.md")

    def test_consolidation_steps(self):
        path = REPO_ROOT / "Docs/Architecture/Consolidation_Steps.md"
        self.assertTrue(path.exists(), "Missing Consolidation_Steps.md")


class TestCMakeListsIncludeNewSubdirs(unittest.TestCase):
    """Verify CMakeLists.txt files include the new subdirectories."""

    def test_novaforge_cmake_includes_save(self):
        cmake = (REPO_ROOT / "NovaForge/CMakeLists.txt").read_text(encoding="utf-8")
        self.assertIn("add_subdirectory(Save)", cmake)

    def test_novaforge_cmake_includes_ui(self):
        cmake = (REPO_ROOT / "NovaForge/CMakeLists.txt").read_text(encoding="utf-8")
        self.assertIn("add_subdirectory(UI)", cmake)

    def test_novaforge_app_cmake_includes_app_cpp(self):
        cmake = (REPO_ROOT / "NovaForge/App/CMakeLists.txt").read_text(encoding="utf-8")
        self.assertIn("App.cpp", cmake)

    def test_novaforge_app_cmake_includes_orchestrator(self):
        cmake = (REPO_ROOT / "NovaForge/App/CMakeLists.txt").read_text(encoding="utf-8")
        self.assertIn("GameOrchestrator.cpp", cmake)

    def test_atlas_editor_cmake_includes_gizmo_system(self):
        cmake = (REPO_ROOT / "Atlas/Editor/CMakeLists.txt").read_text(encoding="utf-8")
        self.assertIn("GizmoSystem.cpp", cmake)

    def test_novaforge_gameplay_cmake_includes_character_system(self):
        cmake = (REPO_ROOT / "NovaForge/Gameplay/CMakeLists.txt").read_text(encoding="utf-8")
        self.assertIn("CharacterSystem.cpp", cmake)


if __name__ == "__main__":
    unittest.main()
