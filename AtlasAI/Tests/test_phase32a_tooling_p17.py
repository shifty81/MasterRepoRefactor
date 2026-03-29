"""Phase 32A — Tests for P17 ToolLayer headers."""
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
TOOL_LAYER = REPO_ROOT / "Atlas" / "Editor" / "ToolLayer"

P17_TOOLS = [
    "NiagaraSystemTool",
    "MotionWarpingTool",
    "IKRetargetTool",
    "GeometryScriptTool",
    "ControlRigTool",
    "StateTreeTool",
]


def _read(name: str) -> str:
    return (TOOL_LAYER / f"{name}.h").read_text()


class TestP17ToolsExist(unittest.TestCase):
    def test_niagara_system_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "NiagaraSystemTool.h").exists())

    def test_motion_warping_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "MotionWarpingTool.h").exists())

    def test_ik_retarget_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "IKRetargetTool.h").exists())

    def test_geometry_script_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "GeometryScriptTool.h").exists())

    def test_control_rig_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "ControlRigTool.h").exists())

    def test_state_tree_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "StateTreeTool.h").exists())


class TestP17PragmaOnce(unittest.TestCase):
    def test_niagara_system_pragma_once(self):
        self.assertIn("#pragma once", _read("NiagaraSystemTool"))

    def test_motion_warping_pragma_once(self):
        self.assertIn("#pragma once", _read("MotionWarpingTool"))

    def test_ik_retarget_pragma_once(self):
        self.assertIn("#pragma once", _read("IKRetargetTool"))

    def test_geometry_script_pragma_once(self):
        self.assertIn("#pragma once", _read("GeometryScriptTool"))

    def test_control_rig_pragma_once(self):
        self.assertIn("#pragma once", _read("ControlRigTool"))

    def test_state_tree_pragma_once(self):
        self.assertIn("#pragma once", _read("StateTreeTool"))


class TestP17ToolName(unittest.TestCase):
    def test_niagara_system_tool_class_name(self):
        self.assertIn("NiagaraSystemTool", _read("NiagaraSystemTool"))

    def test_motion_warping_tool_class_name(self):
        self.assertIn("MotionWarpingTool", _read("MotionWarpingTool"))

    def test_ik_retarget_tool_class_name(self):
        self.assertIn("IKRetargetTool", _read("IKRetargetTool"))

    def test_geometry_script_tool_class_name(self):
        self.assertIn("GeometryScriptTool", _read("GeometryScriptTool"))

    def test_control_rig_tool_class_name(self):
        self.assertIn("ControlRigTool", _read("ControlRigTool"))

    def test_state_tree_tool_class_name(self):
        self.assertIn("StateTreeTool", _read("StateTreeTool"))


class TestP17ITool(unittest.TestCase):
    def test_niagara_system_itool(self):
        self.assertIn(": public ITool", _read("NiagaraSystemTool"))

    def test_motion_warping_itool(self):
        self.assertIn(": public ITool", _read("MotionWarpingTool"))

    def test_ik_retarget_itool(self):
        self.assertIn(": public ITool", _read("IKRetargetTool"))

    def test_geometry_script_itool(self):
        self.assertIn(": public ITool", _read("GeometryScriptTool"))

    def test_control_rig_itool(self):
        self.assertIn(": public ITool", _read("ControlRigTool"))

    def test_state_tree_itool(self):
        self.assertIn(": public ITool", _read("StateTreeTool"))


class TestNiagaraSystemToolDetail(unittest.TestCase):
    def test_emitter_type_enum(self):
        self.assertIn("EmitterType", _read("NiagaraSystemTool"))

    def test_system_module_struct(self):
        self.assertIn("SystemModule", _read("NiagaraSystemTool"))

    def test_create_system_method(self):
        self.assertIn("CreateSystem", _read("NiagaraSystemTool"))

    def test_export_system_method(self):
        self.assertIn("ExportSystem", _read("NiagaraSystemTool"))


class TestMotionWarpingToolDetail(unittest.TestCase):
    def test_warp_algorithm_enum(self):
        self.assertIn("WarpAlgorithm", _read("MotionWarpingTool"))

    def test_warp_window_struct(self):
        self.assertIn("WarpWindow", _read("MotionWarpingTool"))

    def test_create_warp_target_method(self):
        self.assertIn("CreateWarpTarget", _read("MotionWarpingTool"))

    def test_export_warp_config_method(self):
        self.assertIn("ExportWarpConfig", _read("MotionWarpingTool"))


class TestIKRetargetToolDetail(unittest.TestCase):
    def test_ik_chain_type_enum(self):
        self.assertIn("IKChainType", _read("IKRetargetTool"))

    def test_retarget_profile_struct(self):
        self.assertIn("RetargetProfile", _read("IKRetargetTool"))

    def test_create_chain_method(self):
        self.assertIn("CreateChain", _read("IKRetargetTool"))

    def test_export_profile_method(self):
        self.assertIn("ExportProfile", _read("IKRetargetTool"))


class TestGeometryScriptToolDetail(unittest.TestCase):
    def test_mesh_operation_enum(self):
        self.assertIn("MeshOperation", _read("GeometryScriptTool"))

    def test_geom_script_def_struct(self):
        self.assertIn("GeomScriptDef", _read("GeometryScriptTool"))

    def test_create_script_method(self):
        self.assertIn("CreateScript", _read("GeometryScriptTool"))

    def test_export_geom_script_method(self):
        self.assertIn("ExportGeomScript", _read("GeometryScriptTool"))


class TestControlRigToolDetail(unittest.TestCase):
    def test_control_type_enum(self):
        self.assertIn("ControlType", _read("ControlRigTool"))

    def test_control_rig_def_struct(self):
        self.assertIn("ControlRigDef", _read("ControlRigTool"))

    def test_create_rig_method(self):
        self.assertIn("CreateRig", _read("ControlRigTool"))

    def test_export_rig_method(self):
        self.assertIn("ExportRig", _read("ControlRigTool"))


class TestStateTreeToolDetail(unittest.TestCase):
    def test_state_type_enum(self):
        self.assertIn("StateType", _read("StateTreeTool"))

    def test_state_tree_def_struct(self):
        self.assertIn("StateTreeDef", _read("StateTreeTool"))

    def test_create_tree_method(self):
        self.assertIn("CreateTree", _read("StateTreeTool"))

    def test_export_state_tree_method(self):
        self.assertIn("ExportStateTree", _read("StateTreeTool"))


if __name__ == "__main__":
    unittest.main()
