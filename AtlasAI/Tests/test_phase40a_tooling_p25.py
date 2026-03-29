"""Phase 40A — Tests for P25 ToolLayer headers."""
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
TOOL_LAYER = REPO_ROOT / "Atlas" / "Editor" / "ToolLayer"

P25_TOOLS = [
    "RigidBodyJointTool",
    "DataValidatorTool",
    "ParticleCollisionTool",
    "CameraTrackingTool",
    "LocalizationPreviewTool",
    "HierarchyFilterTool",
]


def _read(name: str) -> str:
    return (TOOL_LAYER / f"{name}.h").read_text()


class TestP25ToolsExist(unittest.TestCase):
    def test_rigid_body_joint_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "RigidBodyJointTool.h").exists())

    def test_data_validator_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "DataValidatorTool.h").exists())

    def test_particle_collision_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "ParticleCollisionTool.h").exists())

    def test_camera_tracking_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "CameraTrackingTool.h").exists())

    def test_localization_preview_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "LocalizationPreviewTool.h").exists())

    def test_hierarchy_filter_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "HierarchyFilterTool.h").exists())


class TestP25PragmaOnce(unittest.TestCase):
    def test_rigid_body_joint_tool_pragma_once(self):
        self.assertIn("#pragma once", _read("RigidBodyJointTool"))

    def test_data_validator_tool_pragma_once(self):
        self.assertIn("#pragma once", _read("DataValidatorTool"))

    def test_particle_collision_tool_pragma_once(self):
        self.assertIn("#pragma once", _read("ParticleCollisionTool"))

    def test_camera_tracking_tool_pragma_once(self):
        self.assertIn("#pragma once", _read("CameraTrackingTool"))

    def test_localization_preview_tool_pragma_once(self):
        self.assertIn("#pragma once", _read("LocalizationPreviewTool"))

    def test_hierarchy_filter_tool_pragma_once(self):
        self.assertIn("#pragma once", _read("HierarchyFilterTool"))


class TestP25ToolName(unittest.TestCase):
    def test_rigid_body_joint_tool_class_name(self):
        self.assertIn("RigidBodyJointTool", _read("RigidBodyJointTool"))

    def test_data_validator_tool_class_name(self):
        self.assertIn("DataValidatorTool", _read("DataValidatorTool"))

    def test_particle_collision_tool_class_name(self):
        self.assertIn("ParticleCollisionTool", _read("ParticleCollisionTool"))

    def test_camera_tracking_tool_class_name(self):
        self.assertIn("CameraTrackingTool", _read("CameraTrackingTool"))

    def test_localization_preview_tool_class_name(self):
        self.assertIn("LocalizationPreviewTool", _read("LocalizationPreviewTool"))

    def test_hierarchy_filter_tool_class_name(self):
        self.assertIn("HierarchyFilterTool", _read("HierarchyFilterTool"))


class TestP25ITool(unittest.TestCase):
    def test_rigid_body_joint_tool_itool(self):
        self.assertIn(": public ITool", _read("RigidBodyJointTool"))

    def test_data_validator_tool_itool(self):
        self.assertIn(": public ITool", _read("DataValidatorTool"))

    def test_particle_collision_tool_itool(self):
        self.assertIn(": public ITool", _read("ParticleCollisionTool"))

    def test_camera_tracking_tool_itool(self):
        self.assertIn(": public ITool", _read("CameraTrackingTool"))

    def test_localization_preview_tool_itool(self):
        self.assertIn(": public ITool", _read("LocalizationPreviewTool"))

    def test_hierarchy_filter_tool_itool(self):
        self.assertIn(": public ITool", _read("HierarchyFilterTool"))


class TestRigidBodyJointToolDetail(unittest.TestCase):
    def test_joint_type_enum(self):
        self.assertIn("JointType", _read("RigidBodyJointTool"))

    def test_joint_def_struct(self):
        self.assertIn("JointDef", _read("RigidBodyJointTool"))

    def test_add_constraint_method(self):
        self.assertIn("AddConstraint", _read("RigidBodyJointTool"))

    def test_constraint_axis_enum(self):
        self.assertIn("ConstraintAxis", _read("RigidBodyJointTool"))


class TestDataValidatorToolDetail(unittest.TestCase):
    def test_validation_severity_enum(self):
        self.assertIn("ValidationSeverity", _read("DataValidatorTool"))

    def test_validation_rule_def_struct(self):
        self.assertIn("ValidationRuleDef", _read("DataValidatorTool"))

    def test_validate_asset_method(self):
        self.assertIn("ValidateAsset", _read("DataValidatorTool"))

    def test_validator_scope_enum(self):
        self.assertIn("ValidatorScope", _read("DataValidatorTool"))


class TestParticleCollisionToolDetail(unittest.TestCase):
    def test_collision_response_enum(self):
        self.assertIn("CollisionResponse", _read("ParticleCollisionTool"))

    def test_particle_collider_def_struct(self):
        self.assertIn("ParticleColliderDef", _read("ParticleCollisionTool"))

    def test_add_kill_volume_method(self):
        self.assertIn("AddKillVolume", _read("ParticleCollisionTool"))

    def test_kill_volume_shape_enum(self):
        self.assertIn("KillVolumeShape", _read("ParticleCollisionTool"))


class TestCameraTrackingToolDetail(unittest.TestCase):
    def test_tracking_mode_enum(self):
        self.assertIn("TrackingMode", _read("CameraTrackingTool"))

    def test_tracking_target_def_struct(self):
        self.assertIn("TrackingTargetDef", _read("CameraTrackingTool"))

    def test_create_rail_method(self):
        self.assertIn("CreateRail", _read("CameraTrackingTool"))

    def test_camera_rail_type_enum(self):
        self.assertIn("CameraRailType", _read("CameraTrackingTool"))


class TestLocalizationPreviewToolDetail(unittest.TestCase):
    def test_preview_language_enum(self):
        self.assertIn("PreviewLanguage", _read("LocalizationPreviewTool"))

    def test_localized_string_preview_struct(self):
        self.assertIn("LocalizedStringPreview", _read("LocalizationPreviewTool"))

    def test_switch_language_method(self):
        self.assertIn("SwitchLanguage", _read("LocalizationPreviewTool"))

    def test_diff_mode_enum(self):
        self.assertIn("DiffMode", _read("LocalizationPreviewTool"))


class TestHierarchyFilterToolDetail(unittest.TestCase):
    def test_filter_criteria_enum(self):
        self.assertIn("FilterCriteria", _read("HierarchyFilterTool"))

    def test_hierarchy_filter_def_struct(self):
        self.assertIn("HierarchyFilterDef", _read("HierarchyFilterTool"))

    def test_create_group_method(self):
        self.assertIn("CreateGroup", _read("HierarchyFilterTool"))

    def test_filter_operator_enum(self):
        self.assertIn("FilterOperator", _read("HierarchyFilterTool"))


if __name__ == "__main__":
    unittest.main()
