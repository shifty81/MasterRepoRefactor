"""Phase 21B — Tests for AIBuildMonitor and LayoutDiffReporter."""
import json
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "AtlasAI" / "AIEngine"))

from AtlasAIEngine.intelligence import (
    AIBuildMonitor,
    BuildDiagnostic,
    BuildSummary,
    LayoutDiffReporter,
    LayoutDiffReport,
    LayoutDiffEntry,
)

TMP_DIR = Path("/tmp/test_phase21b")
TMP_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# BuildDiagnostic dataclass
# ---------------------------------------------------------------------------

class TestBuildDiagnosticDataclass(unittest.TestCase):
    def test_line_field(self):
        d = BuildDiagnostic("error: foo", "error", "generic_error", "ts")
        self.assertEqual(d.line, "error: foo")

    def test_severity_field(self):
        d = BuildDiagnostic("x", "warning", "compiler_warning", "ts")
        self.assertEqual(d.severity, "warning")

    def test_category_field(self):
        d = BuildDiagnostic("x", "error", "linker_error", "ts")
        self.assertEqual(d.category, "linker_error")

    def test_file_hint_default_none(self):
        d = BuildDiagnostic("x", "error", "cat", "ts")
        self.assertIsNone(d.file_hint)


# ---------------------------------------------------------------------------
# AIBuildMonitor — ingestion
# ---------------------------------------------------------------------------

class TestAIBuildMonitorIngestion(unittest.TestCase):
    def setUp(self):
        self.mon = AIBuildMonitor(build_id="test_build")

    def test_build_id_set(self):
        self.assertEqual(self.mon.build_id, "test_build")

    def test_ingest_error_line_returns_diagnostic(self):
        d = self.mon.ingest_line("src/foo.cpp: error: undefined reference to bar()")
        self.assertIsNotNone(d)

    def test_ingest_error_classifies_severity(self):
        d = self.mon.ingest_line("error: syntax error near '}'")
        self.assertEqual(d.severity, "error")

    def test_ingest_warning_line_returns_diagnostic(self):
        d = self.mon.ingest_line("warning: deprecated function used")
        self.assertIsNotNone(d)

    def test_ingest_warning_severity(self):
        d = self.mon.ingest_line("warning C4100: unreferenced formal parameter")
        self.assertEqual(d.severity, "warning")

    def test_ingest_clean_line_returns_none(self):
        d = self.mon.ingest_line("Compiling src/main.cpp...")
        self.assertIsNone(d)

    def test_ingest_lines_returns_count(self):
        lines = [
            "error: bad syntax",
            "warning: deprecated usage",
            "Build complete",
        ]
        count = self.mon.ingest_lines(lines)
        self.assertEqual(count, 2)

    def test_error_count_increments(self):
        self.mon.ingest_line("error: something broke")
        self.mon.ingest_line("error: another problem")
        self.assertEqual(self.mon.get_error_count(), 2)

    def test_warning_count_increments(self):
        self.mon.ingest_line("warning: something deprecated")
        self.assertEqual(self.mon.get_warning_count(), 1)

    def test_diagnostic_count(self):
        self.mon.ingest_lines(["error: e1", "warning: w1", "clean line"])
        self.assertEqual(self.mon.get_diagnostic_count(), 2)

    def test_get_errors(self):
        self.mon.ingest_line("error: e1")
        self.mon.ingest_line("warning: w1")
        errs = self.mon.get_errors()
        self.assertEqual(len(errs), 1)
        self.assertEqual(errs[0].severity, "error")

    def test_get_warnings(self):
        self.mon.ingest_line("error: e1")
        self.mon.ingest_line("warning: w1")
        warns = self.mon.get_warnings()
        self.assertEqual(len(warns), 1)
        self.assertEqual(warns[0].severity, "warning")

    def test_reset_clears_state(self):
        self.mon.ingest_line("error: e1")
        self.mon.reset()
        self.assertEqual(self.mon.get_error_count(), 0)
        self.assertEqual(self.mon.get_diagnostic_count(), 0)


# ---------------------------------------------------------------------------
# AIBuildMonitor — categories
# ---------------------------------------------------------------------------

class TestAIBuildMonitorCategories(unittest.TestCase):
    def setUp(self):
        self.mon = AIBuildMonitor()

    def test_linker_error_category(self):
        d = self.mon.ingest_line("foo.cpp: undefined reference to 'main'")
        self.assertIsNotNone(d)
        self.assertEqual(d.category, "linker_error")

    def test_syntax_error_category(self):
        d = self.mon.ingest_line("syntax error before ';'")
        self.assertIsNotNone(d)
        self.assertEqual(d.category, "syntax_error")

    def test_deprecation_warning_category(self):
        d = self.mon.ingest_line("warning: deprecated API used")
        self.assertIsNotNone(d)
        self.assertEqual(d.category, "deprecation_warning")

    def test_get_by_category(self):
        self.mon.ingest_line("syntax error near '{'")
        self.mon.ingest_line("warning: deprecated call")
        self.mon.ingest_line("syntax error again")
        results = self.mon.get_by_category("syntax_error")
        self.assertEqual(len(results), 2)


# ---------------------------------------------------------------------------
# AIBuildMonitor — finalize
# ---------------------------------------------------------------------------

class TestAIBuildMonitorFinalize(unittest.TestCase):
    def setUp(self):
        self.mon = AIBuildMonitor(build_id="finalize_build")
        self.mon.ingest_line("error: e1")
        self.mon.ingest_line("warning: w1")

    def test_finalize_returns_build_summary(self):
        summary = self.mon.finalize(success=False)
        self.assertIsInstance(summary, BuildSummary)

    def test_finalize_build_id(self):
        summary = self.mon.finalize()
        self.assertEqual(summary.build_id, "finalize_build")

    def test_finalize_success_flag(self):
        summary = self.mon.finalize(success=False)
        self.assertFalse(summary.success)

    def test_finalize_error_count(self):
        summary = self.mon.finalize()
        self.assertEqual(summary.error_count, 1)

    def test_finalize_warning_count(self):
        summary = self.mon.finalize()
        self.assertEqual(summary.warning_count, 1)

    def test_finalize_diagnostics_populated(self):
        summary = self.mon.finalize()
        self.assertEqual(len(summary.diagnostics), 2)

    def test_finalize_metadata(self):
        summary = self.mon.finalize(metadata={"project": "Atlas"})
        self.assertEqual(summary.metadata["project"], "Atlas")


# ---------------------------------------------------------------------------
# AIBuildMonitor — save_summary
# ---------------------------------------------------------------------------

class TestAIBuildMonitorSave(unittest.TestCase):
    def setUp(self):
        self.mon = AIBuildMonitor(build_id="save_build")
        self.mon.ingest_line("error: broken")

    def test_save_summary_returns_true(self):
        path = str(TMP_DIR / "build_summary.json")
        summary = self.mon.finalize()
        self.assertTrue(self.mon.save_summary(summary, path))

    def test_save_summary_creates_file(self):
        path = str(TMP_DIR / "build_summary2.json")
        summary = self.mon.finalize()
        self.mon.save_summary(summary, path)
        self.assertTrue(Path(path).exists())

    def test_save_summary_valid_json(self):
        path = str(TMP_DIR / "build_summary3.json")
        summary = self.mon.finalize()
        self.mon.save_summary(summary, path)
        data = json.loads(Path(path).read_text())
        self.assertEqual(data["build_id"], "save_build")


# ---------------------------------------------------------------------------
# LayoutDiffEntry dataclass
# ---------------------------------------------------------------------------

class TestLayoutDiffEntryDataclass(unittest.TestCase):
    def test_change_type_field(self):
        e = LayoutDiffEntry("added", "e1", "StaticMesh")
        self.assertEqual(e.change_type, "added")

    def test_entity_id_field(self):
        e = LayoutDiffEntry("removed", "e2", "Light")
        self.assertEqual(e.entity_id, "e2")

    def test_entity_type_field(self):
        e = LayoutDiffEntry("moved", "e3", "Trigger")
        self.assertEqual(e.entity_type, "Trigger")

    def test_old_value_default_none(self):
        e = LayoutDiffEntry("added", "e1", "T")
        self.assertIsNone(e.old_value)

    def test_new_value_default_none(self):
        e = LayoutDiffEntry("added", "e1", "T")
        self.assertIsNone(e.new_value)


# ---------------------------------------------------------------------------
# LayoutDiffReport dataclass
# ---------------------------------------------------------------------------

class TestLayoutDiffReportDataclass(unittest.TestCase):
    def test_snapshot_a_field(self):
        r = LayoutDiffReport("snap_a", "snap_b")
        self.assertEqual(r.snapshot_a, "snap_a")

    def test_snapshot_b_field(self):
        r = LayoutDiffReport("snap_a", "snap_b")
        self.assertEqual(r.snapshot_b, "snap_b")

    def test_total_changes_empty(self):
        r = LayoutDiffReport("a", "b")
        self.assertEqual(r.total_changes, 0)

    def test_is_empty_true_when_no_changes(self):
        r = LayoutDiffReport("a", "b")
        self.assertTrue(r.is_empty)

    def test_is_empty_false_when_changes(self):
        r = LayoutDiffReport("a", "b")
        r.added.append(LayoutDiffEntry("added", "e1", "T"))
        self.assertFalse(r.is_empty)

    def test_total_changes_sum(self):
        r = LayoutDiffReport("a", "b")
        r.added.append(LayoutDiffEntry("added", "e1", "T"))
        r.removed.append(LayoutDiffEntry("removed", "e2", "T"))
        r.moved.append(LayoutDiffEntry("moved", "e3", "T"))
        self.assertEqual(r.total_changes, 3)


# ---------------------------------------------------------------------------
# LayoutDiffReporter — compare
# ---------------------------------------------------------------------------

def _snap(**entities):
    """Build a snapshot dict: keyword args are entity_ids, values are dicts."""
    return {k: v for k, v in entities.items()}


class TestLayoutDiffReporterCompare(unittest.TestCase):
    def setUp(self):
        self.reporter = LayoutDiffReporter()

    def test_compare_empty_snapshots(self):
        report = self.reporter.compare({}, {})
        self.assertTrue(report.is_empty)

    def test_compare_identical_snapshots(self):
        snap = {"e1": {"type": "Mesh", "x": 1.0, "y": 0.0, "z": 2.0}}
        report = self.reporter.compare(snap, snap)
        self.assertTrue(report.is_empty)

    def test_compare_detects_added(self):
        snap_a = {}
        snap_b = {"e1": {"type": "Mesh", "x": 0.0, "y": 0.0, "z": 0.0}}
        report = self.reporter.compare(snap_a, snap_b)
        self.assertEqual(len(report.added), 1)
        self.assertEqual(report.added[0].entity_id, "e1")

    def test_compare_detects_removed(self):
        snap_a = {"e1": {"type": "Mesh", "x": 0.0, "y": 0.0, "z": 0.0}}
        snap_b = {}
        report = self.reporter.compare(snap_a, snap_b)
        self.assertEqual(len(report.removed), 1)
        self.assertEqual(report.removed[0].entity_id, "e1")

    def test_compare_detects_moved(self):
        snap_a = {"e1": {"type": "Mesh", "x": 0.0, "y": 0.0, "z": 0.0}}
        snap_b = {"e1": {"type": "Mesh", "x": 10.0, "y": 0.0, "z": 0.0}}
        report = self.reporter.compare(snap_a, snap_b)
        self.assertEqual(len(report.moved), 1)

    def test_compare_no_move_within_threshold(self):
        snap_a = {"e1": {"type": "Mesh", "x": 0.0, "y": 0.0, "z": 0.0}}
        snap_b = {"e1": {"type": "Mesh", "x": 0.001, "y": 0.0, "z": 0.0}}
        report = self.reporter.compare(snap_a, snap_b)
        self.assertEqual(len(report.moved), 0)

    def test_compare_detects_property_changed(self):
        snap_a = {"e1": {"type": "Mesh", "x": 0.0, "y": 0.0, "z": 0.0,
                          "visible": True}}
        snap_b = {"e1": {"type": "Mesh", "x": 0.0, "y": 0.0, "z": 0.0,
                          "visible": False}}
        report = self.reporter.compare(snap_a, snap_b)
        self.assertEqual(len(report.property_changed), 1)

    def test_compare_labels(self):
        report = self.reporter.compare({}, {}, label_a="v1", label_b="v2")
        self.assertEqual(report.snapshot_a, "v1")
        self.assertEqual(report.snapshot_b, "v2")

    def test_compare_multiple_adds(self):
        snap_b = {
            "e1": {"type": "Mesh", "x": 0.0, "y": 0.0, "z": 0.0},
            "e2": {"type": "Light", "x": 5.0, "y": 0.0, "z": 0.0},
        }
        report = self.reporter.compare({}, snap_b)
        self.assertEqual(len(report.added), 2)


# ---------------------------------------------------------------------------
# LayoutDiffReporter — history
# ---------------------------------------------------------------------------

class TestLayoutDiffReporterHistory(unittest.TestCase):
    def setUp(self):
        self.reporter = LayoutDiffReporter()

    def test_report_count_increments(self):
        self.reporter.compare({}, {})
        self.reporter.compare({}, {})
        self.assertEqual(self.reporter.get_report_count(), 2)

    def test_get_last_report(self):
        self.reporter.compare({}, {"e1": {"type": "T", "x": 0.0, "y": 0.0,
                                          "z": 0.0}})
        last = self.reporter.get_last_report()
        self.assertIsNotNone(last)
        self.assertEqual(len(last.added), 1)

    def test_get_last_report_empty(self):
        self.assertIsNone(self.reporter.get_last_report())

    def test_clear_history(self):
        self.reporter.compare({}, {})
        self.reporter.clear_history()
        self.assertEqual(self.reporter.get_report_count(), 0)


# ---------------------------------------------------------------------------
# LayoutDiffReporter — save and compare_files
# ---------------------------------------------------------------------------

class TestLayoutDiffReporterPersistence(unittest.TestCase):
    def setUp(self):
        self.reporter = LayoutDiffReporter()
        self.snap_a = {"e1": {"type": "Mesh", "x": 1.0, "y": 0.0, "z": 2.0}}
        self.snap_b = {
            "e1": {"type": "Mesh", "x": 5.0, "y": 0.0, "z": 2.0},
            "e2": {"type": "Light", "x": 0.0, "y": 3.0, "z": 0.0},
        }

    def test_save_report_returns_true(self):
        report = self.reporter.compare(self.snap_a, self.snap_b)
        path = str(TMP_DIR / "layout_diff.json")
        self.assertTrue(self.reporter.save_report(report, path))

    def test_save_report_creates_file(self):
        report = self.reporter.compare(self.snap_a, self.snap_b)
        path = str(TMP_DIR / "layout_diff2.json")
        self.reporter.save_report(report, path)
        self.assertTrue(Path(path).exists())

    def test_save_report_valid_json(self):
        report = self.reporter.compare(self.snap_a, self.snap_b,
                                        label_a="v1", label_b="v2")
        path = str(TMP_DIR / "layout_diff3.json")
        self.reporter.save_report(report, path)
        data = json.loads(Path(path).read_text())
        self.assertEqual(data["snapshot_a"], "v1")
        self.assertIn("added", data)
        self.assertIn("removed", data)

    def test_compare_files(self):
        path_a = str(TMP_DIR / "snap_a.json")
        path_b = str(TMP_DIR / "snap_b.json")
        Path(path_a).write_text(json.dumps(self.snap_a))
        Path(path_b).write_text(json.dumps(self.snap_b))
        report = self.reporter.compare_files(path_a, path_b)
        self.assertIsNotNone(report)
        self.assertGreater(report.total_changes, 0)


# ---------------------------------------------------------------------------
# __init__ exports
# ---------------------------------------------------------------------------

class TestInitExports(unittest.TestCase):
    def test_ai_build_monitor_exported(self):
        from AtlasAIEngine.intelligence import AIBuildMonitor as ABM
        self.assertIsNotNone(ABM)

    def test_build_diagnostic_exported(self):
        from AtlasAIEngine.intelligence import BuildDiagnostic as BD
        self.assertIsNotNone(BD)

    def test_build_summary_exported(self):
        from AtlasAIEngine.intelligence import BuildSummary as BS
        self.assertIsNotNone(BS)

    def test_layout_diff_reporter_exported(self):
        from AtlasAIEngine.intelligence import LayoutDiffReporter as LDR
        self.assertIsNotNone(LDR)

    def test_layout_diff_report_exported(self):
        from AtlasAIEngine.intelligence import LayoutDiffReport as LDRp
        self.assertIsNotNone(LDRp)

    def test_layout_diff_entry_exported(self):
        from AtlasAIEngine.intelligence import LayoutDiffEntry as LDE
        self.assertIsNotNone(LDE)


if __name__ == "__main__":
    unittest.main()
