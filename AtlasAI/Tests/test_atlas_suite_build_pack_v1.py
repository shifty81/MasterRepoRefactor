"""test_atlas_suite_build_pack_v1.py

Pytest suite verifying that AtlasSuiteBuildPackV1 was correctly read,
its errors were fixed, and its contents were properly integrated and archived.
"""

import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SCAFFOLD = REPO_ROOT / "Atlas" / "UI" / "AtlasSuite" / "RuntimeScaffold"
ARCHIVE_ZIP = REPO_ROOT / "Docs" / "Archive" / "ZipFiles" / "AtlasSuiteBuildPackV1.zip"
INTAKE_LOG = REPO_ROOT / "Docs" / "Archive" / "AtlasSuiteBuildPackV1_intake_log.md"
INTAKE_DIR = REPO_ROOT / "Intake"


# ---------------------------------------------------------------------------
# Archival
# ---------------------------------------------------------------------------

class TestArchival:
    def test_zip_archived_in_docs(self):
        assert ARCHIVE_ZIP.exists(), "AtlasSuiteBuildPackV1.zip must be in Docs/Archive/ZipFiles/"

    def test_intake_log_exists(self):
        assert INTAKE_LOG.exists(), "Intake processing log must exist in Docs/Archive/"

    def test_intake_log_mentions_errors(self):
        text = INTAKE_LOG.read_text(encoding="utf-8")
        assert "ERROR 1" in text
        assert "ERROR 2" in text

    def test_intake_log_mentions_threading_risk(self):
        text = INTAKE_LOG.read_text(encoding="utf-8")
        assert "RunFireAndForget" in text

    def test_intake_dir_is_clean(self):
        """No .zip files should remain in the Intake/ staging area."""
        zips = list(INTAKE_DIR.glob("*.zip"))
        assert zips == [], f"Unexpected zip(s) still in Intake/: {zips}"

    def test_zip_is_not_at_repo_root(self):
        """AtlasSuiteBuildPackV1.zip must NOT live at repo root (intake policy violation)."""
        assert not (REPO_ROOT / "AtlasSuiteBuildPackV1.zip").exists()


# ---------------------------------------------------------------------------
# Archive zip integrity
# ---------------------------------------------------------------------------

class TestArchiveZipIntegrity:
    def test_zip_is_valid(self):
        assert zipfile.is_zipfile(ARCHIVE_ZIP)

    def test_zip_contains_readme(self):
        with zipfile.ZipFile(ARCHIVE_ZIP) as zf:
            names = zf.namelist()
        assert any("README" in n for n in names)

    def test_zip_contains_core_project(self):
        with zipfile.ZipFile(ARCHIVE_ZIP) as zf:
            names = zf.namelist()
        assert any("AtlasSuite.Core.csproj" in n for n in names)

    def test_zip_contains_view_model_base(self):
        with zipfile.ZipFile(ARCHIVE_ZIP) as zf:
            names = zf.namelist()
        assert any("ViewModelBase.cs" in n for n in names)


# ---------------------------------------------------------------------------
# RuntimeScaffold directory structure
# ---------------------------------------------------------------------------

class TestRuntimeScaffoldStructure:
    def test_scaffold_dir_exists(self):
        assert SCAFFOLD.is_dir()

    def test_solution_file_present(self):
        assert (SCAFFOLD / "AtlasSuite.BuildPack.sln").exists()

    def test_directory_build_props_present(self):
        assert (SCAFFOLD / "Directory.Build.props").exists()

    def test_readme_present(self):
        assert (SCAFFOLD / "README.md").exists()

    def test_docs_dir_present(self):
        assert (SCAFFOLD / "docs" / "IMPLEMENTATION_NOTES.md").exists()


# ---------------------------------------------------------------------------
# Core project files
# ---------------------------------------------------------------------------

CORE = SCAFFOLD / "src" / "AtlasSuite.Core"

class TestCoreProject:
    def test_csproj_present(self):
        assert (CORE / "AtlasSuite.Core.csproj").exists()

    def test_icommand_bus_present(self):
        assert (CORE / "Abstractions" / "ICommandBus.cs").exists()

    def test_iengine_bridge_present(self):
        assert (CORE / "Abstractions" / "IEngineBridgeService.cs").exists()

    def test_ijob_runner_present(self):
        assert (CORE / "Abstractions" / "IJobRunner.cs").exists()

    def test_ipanel_registry_present(self):
        assert (CORE / "Abstractions" / "IPanelRegistry.cs").exists()

    def test_iworkspace_service_present(self):
        assert (CORE / "Abstractions" / "IWorkspaceService.cs").exists()

    def test_command_bus_present(self):
        assert (CORE / "Commands" / "CommandBus.cs").exists()

    def test_command_definition_present(self):
        assert (CORE / "Commands" / "CommandDefinition.cs").exists()

    def test_dock_zone_present(self):
        assert (CORE / "Docking" / "DockZone.cs").exists()

    def test_panel_descriptor_present(self):
        assert (CORE / "Docking" / "PanelDescriptor.cs").exists()

    def test_panel_registry_present(self):
        assert (CORE / "Docking" / "PanelRegistry.cs").exists()

    def test_inmemory_job_runner_present(self):
        assert (CORE / "Jobs" / "InMemoryJobRunner.cs").exists()

    def test_job_definition_present(self):
        assert (CORE / "Jobs" / "JobDefinition.cs").exists()

    def test_job_record_present(self):
        assert (CORE / "Jobs" / "JobRecord.cs").exists()

    def test_workspace_layout_present(self):
        assert (CORE / "Models" / "WorkspaceLayout.cs").exists()

    def test_workspace_service_present(self):
        assert (CORE / "Services" / "WorkspaceService.cs").exists()

    def test_log_entry_present(self):
        assert (CORE / "Telemetry" / "LogEntry.cs").exists()


# ---------------------------------------------------------------------------
# App project files
# ---------------------------------------------------------------------------

APP = SCAFFOLD / "src" / "AtlasSuite.App"

class TestAppProject:
    def test_csproj_present(self):
        assert (APP / "AtlasSuite.App.csproj").exists()

    def test_relay_command_present(self):
        assert (APP / "Commands" / "RelayCommand.cs").exists()

    def test_view_model_base_present(self):
        assert (APP / "ViewModels" / "ViewModelBase.cs").exists()

    def test_panel_view_model_present(self):
        assert (APP / "ViewModels" / "PanelViewModel.cs").exists()

    def test_main_window_view_model_present(self):
        assert (APP / "ViewModels" / "MainWindowViewModel.cs").exists()

    def test_atlas_ai_panel_view_model_present(self):
        assert (APP / "ViewModels" / "Panels" / "AtlasAiPanelViewModel.cs").exists()

    def test_log_panel_view_model_present(self):
        assert (APP / "ViewModels" / "Panels" / "LogPanelViewModel.cs").exists()

    def test_main_window_xaml_present(self):
        assert (APP / "Views" / "MainWindow.xaml").exists()

    def test_main_window_cs_present(self):
        assert (APP / "Views" / "MainWindow.xaml.cs").exists()

    def test_output_log_panel_view_present(self):
        assert (APP / "Views" / "Panels" / "OutputLogPanelView.xaml").exists()

    def test_atlas_ai_panel_view_present(self):
        assert (APP / "Views" / "Panels" / "AtlasAiPanelView.xaml").exists()

    def test_default_workspace_json_present(self):
        assert (APP / "Resources" / "Layouts" / "DefaultWorkspace.json").exists()


# ---------------------------------------------------------------------------
# Modules and plugins
# ---------------------------------------------------------------------------

class TestModulesAndPlugins:
    def test_modules_ai_present(self):
        assert (SCAFFOLD / "src" / "AtlasSuite.Modules.AI" / "AtlasAiService.cs").exists()

    def test_modules_engine_present(self):
        assert (SCAFFOLD / "src" / "AtlasSuite.Modules.Engine" / "EngineBridgeService.cs").exists()

    def test_modules_project_present(self):
        assert (SCAFFOLD / "src" / "AtlasSuite.Modules.Project" / "ProjectContextService.cs").exists()

    def test_plugins_abstractions_present(self):
        assert (SCAFFOLD / "src" / "AtlasSuite.Plugins.Abstractions" / "IAtlasSuitePlugin.cs").exists()

    def test_plugin_sample_present(self):
        assert (SCAFFOLD / "src" / "AtlasSuite.Plugin.Sample" / "SampleSalvagePlugin.cs").exists()


# ---------------------------------------------------------------------------
# ERROR FIX 1 — MainWindow.xaml must not have duplicate DataTemplates
# ---------------------------------------------------------------------------

class TestFix1DuplicateDataTemplatesWindowResources:
    def _xaml(self) -> str:
        return (APP / "Views" / "MainWindow.xaml").read_text(encoding="utf-8")

    def test_no_ignored_template_key(self):
        assert 'x:Key="IgnoredTemplate"' not in self._xaml(), \
            "IgnoredTemplate was a placeholder artifact and must be removed"

    def test_window_resources_has_single_implicit_panel_template(self):
        xaml = self._xaml()
        resources_block = xaml.split("<Window.Resources>")[1].split("</Window.Resources>")[0]
        count = resources_block.count('<DataTemplate DataType="{x:Type vm:PanelViewModel}">')
        assert count == 1, \
            f"Window.Resources must contain exactly one implicit DataTemplate for PanelViewModel; found {count}"


# ---------------------------------------------------------------------------
# ERROR FIX 2 — Right TabControl must not have duplicate DataTemplates
# ---------------------------------------------------------------------------

class TestFix2DuplicateDataTemplatesTabControlResources:
    def _xaml(self) -> str:
        return (APP / "Views" / "MainWindow.xaml").read_text(encoding="utf-8")

    def test_right_tabcontrol_has_no_tabcontrol_resources(self):
        assert "<TabControl.Resources>" not in self._xaml(), \
            "Duplicate DataTemplates in TabControl.Resources must be removed"


# ---------------------------------------------------------------------------
# RunFireAndForget — should be on MainWindowViewModel, not ViewModelBase
# ---------------------------------------------------------------------------

class TestRunFireAndForget:
    def test_main_window_vm_defines_run_fire_and_forget(self):
        text = (APP / "ViewModels" / "MainWindowViewModel.cs").read_text(encoding="utf-8")
        assert "RunFireAndForget" in text

    def test_view_model_base_does_not_duplicate_run_fire_and_forget(self):
        """ViewModelBase should stay lean; RunFireAndForget is defined in MainWindowViewModel."""
        text = (APP / "ViewModels" / "ViewModelBase.cs").read_text(encoding="utf-8")
        assert "RunFireAndForget" not in text, \
            "RunFireAndForget must not be duplicated in ViewModelBase"
