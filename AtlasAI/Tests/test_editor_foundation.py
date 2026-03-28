"""Tests for Atlas Editor Foundation — source structure and editor config."""

import json
import sys
import unittest
from pathlib import Path

# Repo root
REPO_ROOT = Path(__file__).resolve().parent.parent.parent


class TestEditorFoundationSourceFilesExist(unittest.TestCase):
    """Verify the expected editor foundation source files are present in the repo."""

    def _check(self, relative_path: str):
        full = REPO_ROOT / relative_path
        self.assertTrue(full.exists(), f"Missing source file: {relative_path}")

    # Core
    def test_editor_types_header(self):
        self._check("Atlas/Editor/Core/EditorTypes.h")

    def test_editor_mode_controller_header(self):
        self._check("Atlas/Editor/Core/EditorModeController.h")

    def test_editor_mode_controller_source(self):
        self._check("Atlas/Editor/Core/EditorModeController.cpp")

    # Input
    def test_editor_input_types_header(self):
        self._check("Atlas/Editor/Input/EditorInputTypes.h")

    def test_editor_input_router_header(self):
        self._check("Atlas/Editor/Input/EditorInputRouter.h")

    def test_editor_input_router_source(self):
        self._check("Atlas/Editor/Input/EditorInputRouter.cpp")

    # Camera
    def test_editor_camera_types_header(self):
        self._check("Atlas/Editor/Camera/EditorCameraTypes.h")

    def test_editor_camera_controller_header(self):
        self._check("Atlas/Editor/Camera/EditorCameraController.h")

    def test_editor_camera_controller_source(self):
        self._check("Atlas/Editor/Camera/EditorCameraController.cpp")

    # Selection
    def test_selection_types_header(self):
        self._check("Atlas/Editor/Selection/SelectionTypes.h")

    def test_selection_system_header(self):
        self._check("Atlas/Editor/Selection/SelectionSystem.h")

    def test_selection_system_source(self):
        self._check("Atlas/Editor/Selection/SelectionSystem.cpp")

    # Outliner
    def test_outliner_types_header(self):
        self._check("Atlas/Editor/Outliner/OutlinerTypes.h")

    def test_scene_outliner_header(self):
        self._check("Atlas/Editor/Outliner/SceneOutliner.h")

    def test_scene_outliner_source(self):
        self._check("Atlas/Editor/Outliner/SceneOutliner.cpp")

    # Inspector
    def test_inspector_types_header(self):
        self._check("Atlas/Editor/Inspector/InspectorTypes.h")

    def test_property_inspector_header(self):
        self._check("Atlas/Editor/Inspector/PropertyInspector.h")

    def test_property_inspector_source(self):
        self._check("Atlas/Editor/Inspector/PropertyInspector.cpp")

    # Gizmos
    def test_gizmo_types_header(self):
        self._check("Atlas/Editor/Gizmos/GizmoTypes.h")

    def test_gizmo_system_header(self):
        self._check("Atlas/Editor/Gizmos/GizmoSystem.h")

    def test_gizmo_system_source(self):
        self._check("Atlas/Editor/Gizmos/GizmoSystem.cpp")

    # EditorShell
    def test_editor_shell_header(self):
        self._check("Atlas/Editor/EditorShell.h")

    def test_editor_shell_source(self):
        self._check("Atlas/Editor/EditorShell.cpp")


class TestEditorConfigData(unittest.TestCase):
    """Validate the default editor configuration data file."""

    def _load_json(self, relative_path: str) -> dict:
        full = REPO_ROOT / relative_path
        self.assertTrue(full.exists(), f"Missing file: {relative_path}")
        return json.loads(full.read_text(encoding="utf-8"))

    def test_default_editor_config_exists(self):
        path = REPO_ROOT / "Atlas/Config/Editor/default_editor_config.json"
        self.assertTrue(path.exists(), "Missing default_editor_config.json")

    def test_default_editor_config_has_mode(self):
        data = self._load_json("Atlas/Config/Editor/default_editor_config.json")
        self.assertIn("default_mode", data)

    def test_default_editor_config_has_camera_speed(self):
        data = self._load_json("Atlas/Config/Editor/default_editor_config.json")
        self.assertIn("camera_move_speed", data)

    def test_default_editor_config_has_grid_snap(self):
        data = self._load_json("Atlas/Config/Editor/default_editor_config.json")
        self.assertIn("grid_snap_enabled", data)


class TestEditorFoundationDocumentation(unittest.TestCase):
    """Verify the editor foundation roadmap is present."""

    def test_t1_t3_roadmap_exists(self):
        path = REPO_ROOT / "Docs/T1_T3_Editor_Foundation_Roadmap.md"
        self.assertTrue(path.exists(), "Missing T1_T3_Editor_Foundation_Roadmap.md")

    def test_roadmap_has_content(self):
        path = REPO_ROOT / "Docs/T1_T3_Editor_Foundation_Roadmap.md"
        content = path.read_text(encoding="utf-8")
        self.assertGreater(len(content), 50)


if __name__ == "__main__":
    unittest.main()
