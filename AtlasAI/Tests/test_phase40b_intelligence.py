"""Phase 40B — Tests for RigidBodyJointPipeline and DataValidatorPipeline."""
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "AtlasAI" / "AIEngine"))

from AtlasAIEngine.intelligence import (
    RigidBodyJointPipeline,
    JointEntry,
    JointConstraintEntry,
    JointVisualizationEntry,
    DataValidatorPipeline,
    ValidationRuleEntry,
    ValidationResultEntry,
    ValidationReportEntry,
)


# ---------------------------------------------------------------------------
# JointEntry
# ---------------------------------------------------------------------------

class TestJointEntry(unittest.TestCase):
    def test_joint_id(self):
        j = JointEntry(joint_id="joint_001", joint_name="HingeA")
        self.assertEqual(j.joint_id, "joint_001")

    def test_joint_name(self):
        j = JointEntry(joint_id="joint_001", joint_name="HingeA")
        self.assertEqual(j.joint_name, "HingeA")

    def test_default_type_hinge(self):
        j = JointEntry(joint_id="joint_001", joint_name="HingeA")
        self.assertEqual(j.joint_type, "Hinge")

    def test_is_fixed_false(self):
        j = JointEntry(joint_id="joint_001", joint_name="HingeA", joint_type="Hinge")
        self.assertFalse(j.is_fixed)

    def test_is_fixed_true(self):
        j = JointEntry(joint_id="joint_001", joint_name="FixedA", joint_type="Fixed")
        self.assertTrue(j.is_fixed)

    def test_is_hinge_true(self):
        j = JointEntry(joint_id="joint_001", joint_name="HingeA", joint_type="Hinge")
        self.assertTrue(j.is_hinge)

    def test_is_hinge_false(self):
        j = JointEntry(joint_id="joint_001", joint_name="FixedA", joint_type="Fixed")
        self.assertFalse(j.is_hinge)

    def test_is_broken_false(self):
        j = JointEntry(joint_id="joint_001", joint_name="HingeA", limit_mode="Hard")
        self.assertFalse(j.is_broken)

    def test_is_broken_true(self):
        j = JointEntry(joint_id="joint_001", joint_name="HingeA", limit_mode="Free")
        self.assertTrue(j.is_broken)

    def test_has_bodies_false(self):
        j = JointEntry(joint_id="joint_001", joint_name="HingeA")
        self.assertFalse(j.has_bodies)

    def test_has_bodies_true(self):
        j = JointEntry(joint_id="joint_001", joint_name="HingeA", body_a_id="bodyA", body_b_id="bodyB")
        self.assertTrue(j.has_bodies)

    def test_limit_range(self):
        j = JointEntry(joint_id="joint_001", joint_name="HingeA", limit_low=-45.0, limit_high=45.0)
        self.assertAlmostEqual(j.limit_range, 90.0)

    def test_is_enabled_true(self):
        j = JointEntry(joint_id="joint_001", joint_name="HingeA", enabled=True)
        self.assertTrue(j.is_enabled)

    def test_is_enabled_false(self):
        j = JointEntry(joint_id="joint_001", joint_name="HingeA", enabled=False)
        self.assertFalse(j.is_enabled)


# ---------------------------------------------------------------------------
# JointConstraintEntry
# ---------------------------------------------------------------------------

class TestJointConstraintEntry(unittest.TestCase):
    def test_constraint_id(self):
        c = JointConstraintEntry(constraint_id="con_001", joint_id="joint_001")
        self.assertEqual(c.constraint_id, "con_001")

    def test_joint_id(self):
        c = JointConstraintEntry(constraint_id="con_001", joint_id="joint_001")
        self.assertEqual(c.joint_id, "joint_001")

    def test_is_stiff_false(self):
        c = JointConstraintEntry(constraint_id="con_001", joint_id="joint_001", stiffness=1.0)
        self.assertFalse(c.is_stiff)

    def test_is_stiff_true(self):
        c = JointConstraintEntry(constraint_id="con_001", joint_id="joint_001", stiffness=10.0)
        self.assertTrue(c.is_stiff)

    def test_is_enabled_true(self):
        c = JointConstraintEntry(constraint_id="con_001", joint_id="joint_001", enabled=True)
        self.assertTrue(c.is_enabled)

    def test_is_enabled_false(self):
        c = JointConstraintEntry(constraint_id="con_001", joint_id="joint_001", enabled=False)
        self.assertFalse(c.is_enabled)

    def test_can_break_true(self):
        c = JointConstraintEntry(constraint_id="con_001", joint_id="joint_001", break_force=500.0)
        self.assertTrue(c.can_break)

    def test_is_x_axis_true(self):
        c = JointConstraintEntry(constraint_id="con_001", joint_id="joint_001", axis="X")
        self.assertTrue(c.is_x_axis)

    def test_is_x_axis_false(self):
        c = JointConstraintEntry(constraint_id="con_001", joint_id="joint_001", axis="Y")
        self.assertFalse(c.is_x_axis)


# ---------------------------------------------------------------------------
# JointVisualizationEntry
# ---------------------------------------------------------------------------

class TestJointVisualizationEntry(unittest.TestCase):
    def test_vis_config_id(self):
        v = JointVisualizationEntry(vis_config_id="vis_001", joint_id="joint_001")
        self.assertEqual(v.vis_config_id, "vis_001")

    def test_joint_id(self):
        v = JointVisualizationEntry(vis_config_id="vis_001", joint_id="joint_001")
        self.assertEqual(v.joint_id, "joint_001")

    def test_is_none_false(self):
        v = JointVisualizationEntry(vis_config_id="vis_001", joint_id="joint_001", vis_mode="Axes")
        self.assertFalse(v.is_none)

    def test_is_none_true(self):
        v = JointVisualizationEntry(vis_config_id="vis_001", joint_id="joint_001", vis_mode="None")
        self.assertTrue(v.is_none)

    def test_shows_all_false(self):
        v = JointVisualizationEntry(vis_config_id="vis_001", joint_id="joint_001", vis_mode="Axes")
        self.assertFalse(v.shows_all)

    def test_shows_all_true(self):
        v = JointVisualizationEntry(vis_config_id="vis_001", joint_id="joint_001", vis_mode="All")
        self.assertTrue(v.shows_all)

    def test_is_enabled_true(self):
        v = JointVisualizationEntry(vis_config_id="vis_001", joint_id="joint_001", enabled=True)
        self.assertTrue(v.is_enabled)

    def test_is_labeled_false(self):
        v = JointVisualizationEntry(vis_config_id="vis_001", joint_id="joint_001", show_labels=False)
        self.assertFalse(v.is_labeled)

    def test_is_labeled_true(self):
        v = JointVisualizationEntry(vis_config_id="vis_001", joint_id="joint_001", show_labels=True)
        self.assertTrue(v.is_labeled)


# ---------------------------------------------------------------------------
# RigidBodyJointPipeline
# ---------------------------------------------------------------------------

class TestRigidBodyJointPipeline(unittest.TestCase):
    def setUp(self):
        self.pipeline = RigidBodyJointPipeline()
        self.joint = JointEntry(joint_id="joint_001", joint_name="HingeA")

    def test_add_joint(self):
        self.assertTrue(self.pipeline.add_joint(self.joint))

    def test_remove_joint(self):
        self.pipeline.add_joint(self.joint)
        self.assertTrue(self.pipeline.remove_joint("joint_001"))

    def test_get_all_joints(self):
        self.pipeline.add_joint(self.joint)
        joints = self.pipeline.get_all_joints()
        self.assertEqual(len(joints), 1)

    def test_add_constraint(self):
        self.pipeline.add_joint(self.joint)
        c = JointConstraintEntry(constraint_id="con_001", joint_id="joint_001")
        self.assertTrue(self.pipeline.add_constraint("joint_001", c))

    def test_remove_constraint(self):
        self.pipeline.add_joint(self.joint)
        c = JointConstraintEntry(constraint_id="con_001", joint_id="joint_001")
        self.pipeline.add_constraint("joint_001", c)
        self.assertTrue(self.pipeline.remove_constraint("joint_001", "con_001"))

    def test_get_constraints_for_joint(self):
        self.pipeline.add_joint(self.joint)
        c = JointConstraintEntry(constraint_id="con_001", joint_id="joint_001")
        self.pipeline.add_constraint("joint_001", c)
        result = self.pipeline.get_constraints_for_joint("joint_001")
        self.assertEqual(len(result), 1)

    def test_add_vis_config(self):
        self.pipeline.add_joint(self.joint)
        v = JointVisualizationEntry(vis_config_id="vis_001", joint_id="joint_001")
        self.assertTrue(self.pipeline.add_vis_config("joint_001", v))

    def test_remove_vis_config(self):
        self.pipeline.add_joint(self.joint)
        v = JointVisualizationEntry(vis_config_id="vis_001", joint_id="joint_001")
        self.pipeline.add_vis_config("joint_001", v)
        self.assertTrue(self.pipeline.remove_vis_config("joint_001", "vis_001"))

    def test_get_vis_configs_for_joint(self):
        self.pipeline.add_joint(self.joint)
        v = JointVisualizationEntry(vis_config_id="vis_001", joint_id="joint_001")
        self.pipeline.add_vis_config("joint_001", v)
        result = self.pipeline.get_vis_configs_for_joint("joint_001")
        self.assertEqual(len(result), 1)

    def test_get_enabled_joints(self):
        self.pipeline.add_joint(self.joint)
        result = self.pipeline.get_enabled_joints()
        self.assertEqual(len(result), 1)

    def test_get_disabled_joints(self):
        disabled = JointEntry(joint_id="joint_002", joint_name="Disabled", enabled=False)
        self.pipeline.add_joint(disabled)
        result = self.pipeline.get_disabled_joints()
        self.assertEqual(len(result), 1)

    def test_get_joints_by_type(self):
        self.pipeline.add_joint(self.joint)
        result = self.pipeline.get_joints_by_type("Hinge")
        self.assertEqual(len(result), 1)

    def test_break_joint(self):
        self.pipeline.add_joint(self.joint)
        self.assertTrue(self.pipeline.break_joint("joint_001"))
        self.assertEqual(self.pipeline.get_joint("joint_001").limit_mode, "Free")

    def test_validate(self):
        self.assertTrue(self.pipeline.validate(self.joint))

    def test_joint_count(self):
        self.pipeline.add_joint(self.joint)
        self.assertEqual(self.pipeline.joint_count, 1)

    def test_is_empty(self):
        self.assertTrue(self.pipeline.is_empty)

    def test_clear(self):
        self.pipeline.add_joint(self.joint)
        self.pipeline.clear()
        self.assertTrue(self.pipeline.is_empty)


# ---------------------------------------------------------------------------
# ValidationRuleEntry
# ---------------------------------------------------------------------------

class TestValidationRuleEntry(unittest.TestCase):
    def test_rule_id(self):
        r = ValidationRuleEntry(rule_id="rule_001", rule_name="SchemaCheck")
        self.assertEqual(r.rule_id, "rule_001")

    def test_rule_name(self):
        r = ValidationRuleEntry(rule_id="rule_001", rule_name="SchemaCheck")
        self.assertEqual(r.rule_name, "SchemaCheck")

    def test_default_type_schema(self):
        r = ValidationRuleEntry(rule_id="rule_001", rule_name="SchemaCheck")
        self.assertEqual(r.rule_type, "Schema")

    def test_is_schema_true(self):
        r = ValidationRuleEntry(rule_id="rule_001", rule_name="SchemaCheck", rule_type="Schema")
        self.assertTrue(r.is_schema)

    def test_is_schema_false(self):
        r = ValidationRuleEntry(rule_id="rule_001", rule_name="RangeCheck", rule_type="Range")
        self.assertFalse(r.is_schema)

    def test_is_critical_false(self):
        r = ValidationRuleEntry(rule_id="rule_001", rule_name="SchemaCheck", severity="Error")
        self.assertFalse(r.is_critical)

    def test_is_critical_true(self):
        r = ValidationRuleEntry(rule_id="rule_001", rule_name="SchemaCheck", severity="Critical")
        self.assertTrue(r.is_critical)

    def test_is_enabled_true(self):
        r = ValidationRuleEntry(rule_id="rule_001", rule_name="SchemaCheck", enabled=True)
        self.assertTrue(r.is_enabled)

    def test_has_expr_false(self):
        r = ValidationRuleEntry(rule_id="rule_001", rule_name="SchemaCheck", expr="")
        self.assertFalse(r.has_expr)

    def test_has_expr_true(self):
        r = ValidationRuleEntry(rule_id="rule_001", rule_name="SchemaCheck", expr="value > 0")
        self.assertTrue(r.has_expr)

    def test_is_error_true_error(self):
        r = ValidationRuleEntry(rule_id="rule_001", rule_name="SchemaCheck", severity="Error")
        self.assertTrue(r.is_error)

    def test_is_error_true_critical(self):
        r = ValidationRuleEntry(rule_id="rule_001", rule_name="SchemaCheck", severity="Critical")
        self.assertTrue(r.is_error)

    def test_is_error_false_warning(self):
        r = ValidationRuleEntry(rule_id="rule_001", rule_name="SchemaCheck", severity="Warning")
        self.assertFalse(r.is_error)


# ---------------------------------------------------------------------------
# ValidationResultEntry
# ---------------------------------------------------------------------------

class TestValidationResultEntry(unittest.TestCase):
    def test_result_id(self):
        r = ValidationResultEntry(result_id="res_001", rule_id="rule_001")
        self.assertEqual(r.result_id, "res_001")

    def test_rule_id(self):
        r = ValidationResultEntry(result_id="res_001", rule_id="rule_001")
        self.assertEqual(r.rule_id, "rule_001")

    def test_is_passed_false(self):
        r = ValidationResultEntry(result_id="res_001", rule_id="rule_001", passed=False)
        self.assertFalse(r.is_passed)

    def test_is_passed_true(self):
        r = ValidationResultEntry(result_id="res_001", rule_id="rule_001", passed=True)
        self.assertTrue(r.is_passed)

    def test_is_failed_false(self):
        r = ValidationResultEntry(result_id="res_001", rule_id="rule_001", passed=True)
        self.assertFalse(r.is_failed)

    def test_is_failed_true(self):
        r = ValidationResultEntry(result_id="res_001", rule_id="rule_001", passed=False)
        self.assertTrue(r.is_failed)

    def test_is_error_true(self):
        r = ValidationResultEntry(result_id="res_001", rule_id="rule_001", severity="Error")
        self.assertTrue(r.is_error)

    def test_is_warning_true(self):
        r = ValidationResultEntry(result_id="res_001", rule_id="rule_001", severity="Warning")
        self.assertTrue(r.is_warning)

    def test_is_critical_true(self):
        r = ValidationResultEntry(result_id="res_001", rule_id="rule_001", severity="Critical")
        self.assertTrue(r.is_critical)

    def test_has_message_false(self):
        r = ValidationResultEntry(result_id="res_001", rule_id="rule_001", message="")
        self.assertFalse(r.has_message)

    def test_has_message_true(self):
        r = ValidationResultEntry(result_id="res_001", rule_id="rule_001", message="Field missing")
        self.assertTrue(r.has_message)


# ---------------------------------------------------------------------------
# ValidationReportEntry
# ---------------------------------------------------------------------------

class TestValidationReportEntry(unittest.TestCase):
    def test_report_id(self):
        r = ValidationReportEntry(report_id="rep_001")
        self.assertEqual(r.report_id, "rep_001")

    def test_asset_id(self):
        r = ValidationReportEntry(report_id="rep_001", asset_id="asset_001")
        self.assertEqual(r.asset_id, "asset_001")

    def test_is_passed_false(self):
        r = ValidationReportEntry(report_id="rep_001", state="Pending")
        self.assertFalse(r.is_passed)

    def test_is_passed_true(self):
        r = ValidationReportEntry(report_id="rep_001", state="Passed")
        self.assertTrue(r.is_passed)

    def test_is_failed_false(self):
        r = ValidationReportEntry(report_id="rep_001", state="Pending")
        self.assertFalse(r.is_failed)

    def test_is_failed_true(self):
        r = ValidationReportEntry(report_id="rep_001", state="Failed")
        self.assertTrue(r.is_failed)

    def test_is_pending_true(self):
        r = ValidationReportEntry(report_id="rep_001", state="Pending")
        self.assertTrue(r.is_pending)

    def test_is_pending_false(self):
        r = ValidationReportEntry(report_id="rep_001", state="Passed")
        self.assertFalse(r.is_pending)

    def test_has_errors_false(self):
        r = ValidationReportEntry(report_id="rep_001", error_count=0)
        self.assertFalse(r.has_errors)

    def test_has_errors_true(self):
        r = ValidationReportEntry(report_id="rep_001", error_count=3)
        self.assertTrue(r.has_errors)

    def test_has_warnings_false(self):
        r = ValidationReportEntry(report_id="rep_001", warning_count=0)
        self.assertFalse(r.has_warnings)

    def test_has_warnings_true(self):
        r = ValidationReportEntry(report_id="rep_001", warning_count=2)
        self.assertTrue(r.has_warnings)

    def test_total_issues(self):
        r = ValidationReportEntry(report_id="rep_001", error_count=3, warning_count=2)
        self.assertEqual(r.total_issues, 5)


# ---------------------------------------------------------------------------
# DataValidatorPipeline
# ---------------------------------------------------------------------------

class TestDataValidatorPipeline(unittest.TestCase):
    def setUp(self):
        self.pipeline = DataValidatorPipeline()
        self.rule = ValidationRuleEntry(rule_id="rule_001", rule_name="SchemaCheck")

    def test_add_rule(self):
        self.assertTrue(self.pipeline.add_rule(self.rule))

    def test_remove_rule(self):
        self.pipeline.add_rule(self.rule)
        self.assertTrue(self.pipeline.remove_rule("rule_001"))

    def test_get_all_rules(self):
        self.pipeline.add_rule(self.rule)
        rules = self.pipeline.get_all_rules()
        self.assertEqual(len(rules), 1)

    def test_add_result(self):
        self.pipeline.add_rule(self.rule)
        res = ValidationResultEntry(result_id="res_001", rule_id="rule_001")
        self.assertTrue(self.pipeline.add_result("rule_001", res))

    def test_remove_result(self):
        self.pipeline.add_rule(self.rule)
        res = ValidationResultEntry(result_id="res_001", rule_id="rule_001")
        self.pipeline.add_result("rule_001", res)
        self.assertTrue(self.pipeline.remove_result("rule_001", "res_001"))

    def test_get_results_for_rule(self):
        self.pipeline.add_rule(self.rule)
        res = ValidationResultEntry(result_id="res_001", rule_id="rule_001")
        self.pipeline.add_result("rule_001", res)
        result = self.pipeline.get_results_for_rule("rule_001")
        self.assertEqual(len(result), 1)

    def test_add_report(self):
        rep = ValidationReportEntry(report_id="rep_001", asset_id="asset_001")
        self.assertTrue(self.pipeline.add_report("asset_001", rep))

    def test_remove_report(self):
        rep = ValidationReportEntry(report_id="rep_001", asset_id="asset_001")
        self.pipeline.add_report("asset_001", rep)
        self.assertTrue(self.pipeline.remove_report("asset_001", "rep_001"))

    def test_get_reports_for_asset(self):
        rep = ValidationReportEntry(report_id="rep_001", asset_id="asset_001")
        self.pipeline.add_report("asset_001", rep)
        result = self.pipeline.get_reports_for_asset("asset_001")
        self.assertEqual(len(result), 1)

    def test_get_passed_results(self):
        self.pipeline.add_rule(self.rule)
        res = ValidationResultEntry(result_id="res_001", rule_id="rule_001", passed=True)
        self.pipeline.add_result("rule_001", res)
        result = self.pipeline.get_passed_results()
        self.assertEqual(len(result), 1)

    def test_get_failed_results(self):
        self.pipeline.add_rule(self.rule)
        res = ValidationResultEntry(result_id="res_001", rule_id="rule_001", passed=False)
        self.pipeline.add_result("rule_001", res)
        result = self.pipeline.get_failed_results()
        self.assertEqual(len(result), 1)

    def test_get_critical_rules(self):
        critical = ValidationRuleEntry(rule_id="rule_002", rule_name="Critical", severity="Critical")
        self.pipeline.add_rule(critical)
        result = self.pipeline.get_critical_rules()
        self.assertEqual(len(result), 1)

    def test_get_enabled_rules(self):
        self.pipeline.add_rule(self.rule)
        result = self.pipeline.get_enabled_rules()
        self.assertEqual(len(result), 1)

    def test_get_rules_by_scope(self):
        self.pipeline.add_rule(self.rule)
        result = self.pipeline.get_rules_by_scope("Asset")
        self.assertEqual(len(result), 1)

    def test_validate(self):
        self.assertTrue(self.pipeline.validate(self.rule))

    def test_rule_count(self):
        self.pipeline.add_rule(self.rule)
        self.assertEqual(self.pipeline.rule_count, 1)

    def test_is_empty(self):
        self.assertTrue(self.pipeline.is_empty)

    def test_clear(self):
        self.pipeline.add_rule(self.rule)
        self.pipeline.clear()
        self.assertTrue(self.pipeline.is_empty)


if __name__ == "__main__":
    unittest.main()
