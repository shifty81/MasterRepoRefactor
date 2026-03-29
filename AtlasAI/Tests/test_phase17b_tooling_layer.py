"""Phase 17B tests — Tooling Layer P0 + P1 implementations."""
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
TOOL_LAYER_DIR = REPO_ROOT / "Atlas" / "Editor" / "ToolLayer"


class TestPhase17BDirectoryExists(unittest.TestCase):
    def test_tool_layer_directory_exists(self):
        self.assertTrue(TOOL_LAYER_DIR.is_dir())


class TestPhase17BIToolHeader(unittest.TestCase):
    def _content(self):
        return (TOOL_LAYER_DIR / "ITool.h").read_text()

    def test_itool_header_exists(self):
        self.assertTrue((TOOL_LAYER_DIR / "ITool.h").exists())

    def test_itool_pragma_once(self):
        self.assertIn("#pragma once", self._content())

    def test_itool_class_declaration(self):
        self.assertIn("class ITool", self._content())

    def test_itool_virtual_activate(self):
        self.assertIn("virtual void Activate", self._content())

    def test_itool_virtual_deactivate(self):
        self.assertIn("virtual void Deactivate", self._content())

    def test_itool_virtual_get_tool_name(self):
        self.assertIn("virtual std::string GetToolName", self._content())

    def test_itool_virtual_is_active(self):
        self.assertIn("virtual bool IsActive", self._content())

    def test_itool_virtual_update(self):
        self.assertIn("virtual void Update", self._content())

    def test_itool_virtual_on_mouse_down(self):
        self.assertIn("virtual void OnMouseDown", self._content())

    def test_itool_virtual_destructor(self):
        self.assertIn("virtual ~ITool", self._content())


class TestPhase17BP0Tools(unittest.TestCase):
    """P0 tool headers: MultiSelectionManager, SnapAlignTool, PrefabLibrary, CameraViewTool, LiveEditMode."""

    def _read(self, name):
        return (TOOL_LAYER_DIR / name).read_text()

    # MultiSelectionManager
    def test_multi_selection_manager_exists(self):
        self.assertTrue((TOOL_LAYER_DIR / "MultiSelectionManager.h").exists())

    def test_multi_selection_manager_pragma_once(self):
        self.assertIn("#pragma once", self._read("MultiSelectionManager.h"))

    def test_multi_selection_manager_class(self):
        self.assertIn("class MultiSelectionManager", self._read("MultiSelectionManager.h"))

    def test_multi_selection_manager_select_entity(self):
        self.assertIn("SelectEntity", self._read("MultiSelectionManager.h"))

    def test_multi_selection_manager_clear_selection(self):
        self.assertIn("ClearSelection", self._read("MultiSelectionManager.h"))

    def test_multi_selection_manager_get_tool_name_value(self):
        self.assertIn('"MultiSelectionManager"', self._read("MultiSelectionManager.h"))

    # SnapAlignTool
    def test_snap_align_tool_exists(self):
        self.assertTrue((TOOL_LAYER_DIR / "SnapAlignTool.h").exists())

    def test_snap_align_tool_pragma_once(self):
        self.assertIn("#pragma once", self._read("SnapAlignTool.h"))

    def test_snap_align_tool_class(self):
        self.assertIn("class SnapAlignTool", self._read("SnapAlignTool.h"))

    def test_snap_align_tool_set_grid_size(self):
        self.assertIn("SetGridSize", self._read("SnapAlignTool.h"))

    def test_snap_align_tool_get_tool_name_value(self):
        self.assertIn('"SnapAlignTool"', self._read("SnapAlignTool.h"))

    # PrefabLibrary
    def test_prefab_library_exists(self):
        self.assertTrue((TOOL_LAYER_DIR / "PrefabLibrary.h").exists())

    def test_prefab_library_pragma_once(self):
        self.assertIn("#pragma once", self._read("PrefabLibrary.h"))

    def test_prefab_library_class(self):
        self.assertIn("class PrefabLibrary", self._read("PrefabLibrary.h"))

    def test_prefab_library_register_prefab(self):
        self.assertIn("RegisterPrefab", self._read("PrefabLibrary.h"))

    def test_prefab_library_spawn_prefab(self):
        self.assertIn("SpawnPrefab", self._read("PrefabLibrary.h"))

    def test_prefab_library_get_tool_name_value(self):
        self.assertIn('"PrefabLibrary"', self._read("PrefabLibrary.h"))

    # CameraViewTool
    def test_camera_view_tool_exists(self):
        self.assertTrue((TOOL_LAYER_DIR / "CameraViewTool.h").exists())

    def test_camera_view_tool_pragma_once(self):
        self.assertIn("#pragma once", self._read("CameraViewTool.h"))

    def test_camera_view_tool_class(self):
        self.assertIn("class CameraViewTool", self._read("CameraViewTool.h"))

    def test_camera_view_tool_set_view_mode(self):
        self.assertIn("SetViewMode", self._read("CameraViewTool.h"))

    def test_camera_view_tool_view_mode_enum(self):
        self.assertIn("ViewMode", self._read("CameraViewTool.h"))

    def test_camera_view_tool_get_tool_name_value(self):
        self.assertIn('"CameraViewTool"', self._read("CameraViewTool.h"))

    # LiveEditMode
    def test_live_edit_mode_exists(self):
        self.assertTrue((TOOL_LAYER_DIR / "LiveEditMode.h").exists())

    def test_live_edit_mode_pragma_once(self):
        self.assertIn("#pragma once", self._read("LiveEditMode.h"))

    def test_live_edit_mode_class(self):
        self.assertIn("class LiveEditMode", self._read("LiveEditMode.h"))

    def test_live_edit_mode_pause_simulation(self):
        self.assertIn("PauseSimulation", self._read("LiveEditMode.h"))

    def test_live_edit_mode_resume_simulation(self):
        self.assertIn("ResumeSimulation", self._read("LiveEditMode.h"))

    def test_live_edit_mode_get_tool_name_value(self):
        self.assertIn('"LiveEditMode"', self._read("LiveEditMode.h"))


class TestPhase17BP1Tools(unittest.TestCase):
    """P1 tool headers: AnimationEditorTool, IKRigTool, SimulationStepController, EnvironmentControlTool, MaterialShaderTool, LightingControlTool."""

    def _read(self, name):
        return (TOOL_LAYER_DIR / name).read_text()

    # AnimationEditorTool
    def test_animation_editor_tool_exists(self):
        self.assertTrue((TOOL_LAYER_DIR / "AnimationEditorTool.h").exists())

    def test_animation_editor_tool_pragma_once(self):
        self.assertIn("#pragma once", self._read("AnimationEditorTool.h"))

    def test_animation_editor_tool_class(self):
        self.assertIn("class AnimationEditorTool", self._read("AnimationEditorTool.h"))

    def test_animation_editor_tool_add_layer(self):
        self.assertIn("AddLayer", self._read("AnimationEditorTool.h"))

    def test_animation_editor_tool_get_tool_name_value(self):
        self.assertIn('"AnimationEditorTool"', self._read("AnimationEditorTool.h"))

    # IKRigTool
    def test_ik_rig_tool_exists(self):
        self.assertTrue((TOOL_LAYER_DIR / "IKRigTool.h").exists())

    def test_ik_rig_tool_pragma_once(self):
        self.assertIn("#pragma once", self._read("IKRigTool.h"))

    def test_ik_rig_tool_class(self):
        self.assertIn("class IKRigTool", self._read("IKRigTool.h"))

    def test_ik_rig_tool_solve_ik(self):
        self.assertIn("SolveIK", self._read("IKRigTool.h"))

    def test_ik_rig_tool_get_tool_name_value(self):
        self.assertIn('"IKRigTool"', self._read("IKRigTool.h"))

    # SimulationStepController
    def test_simulation_step_controller_exists(self):
        self.assertTrue((TOOL_LAYER_DIR / "SimulationStepController.h").exists())

    def test_simulation_step_controller_pragma_once(self):
        self.assertIn("#pragma once", self._read("SimulationStepController.h"))

    def test_simulation_step_controller_class(self):
        self.assertIn("class SimulationStepController", self._read("SimulationStepController.h"))

    def test_simulation_step_controller_step_forward(self):
        self.assertIn("StepForward", self._read("SimulationStepController.h"))

    def test_simulation_step_controller_get_tool_name_value(self):
        self.assertIn('"SimulationStepController"', self._read("SimulationStepController.h"))

    # EnvironmentControlTool
    def test_environment_control_tool_exists(self):
        self.assertTrue((TOOL_LAYER_DIR / "EnvironmentControlTool.h").exists())

    def test_environment_control_tool_pragma_once(self):
        self.assertIn("#pragma once", self._read("EnvironmentControlTool.h"))

    def test_environment_control_tool_class(self):
        self.assertIn("class EnvironmentControlTool", self._read("EnvironmentControlTool.h"))

    def test_environment_control_tool_set_skybox(self):
        self.assertIn("SetSkybox", self._read("EnvironmentControlTool.h"))

    def test_environment_control_tool_get_tool_name_value(self):
        self.assertIn('"EnvironmentControlTool"', self._read("EnvironmentControlTool.h"))

    # MaterialShaderTool
    def test_material_shader_tool_exists(self):
        self.assertTrue((TOOL_LAYER_DIR / "MaterialShaderTool.h").exists())

    def test_material_shader_tool_pragma_once(self):
        self.assertIn("#pragma once", self._read("MaterialShaderTool.h"))

    def test_material_shader_tool_class(self):
        self.assertIn("class MaterialShaderTool", self._read("MaterialShaderTool.h"))

    def test_material_shader_tool_compile_shader(self):
        self.assertIn("CompileShader", self._read("MaterialShaderTool.h"))

    def test_material_shader_tool_get_tool_name_value(self):
        self.assertIn('"MaterialShaderTool"', self._read("MaterialShaderTool.h"))

    # LightingControlTool
    def test_lighting_control_tool_exists(self):
        self.assertTrue((TOOL_LAYER_DIR / "LightingControlTool.h").exists())

    def test_lighting_control_tool_pragma_once(self):
        self.assertIn("#pragma once", self._read("LightingControlTool.h"))

    def test_lighting_control_tool_class(self):
        self.assertIn("class LightingControlTool", self._read("LightingControlTool.h"))

    def test_lighting_control_tool_add_light(self):
        self.assertIn("AddLight", self._read("LightingControlTool.h"))

    def test_lighting_control_tool_toggle_shadows(self):
        self.assertIn("ToggleShadows", self._read("LightingControlTool.h"))

    def test_lighting_control_tool_get_tool_name_value(self):
        self.assertIn('"LightingControlTool"', self._read("LightingControlTool.h"))


if __name__ == "__main__":
    unittest.main()
