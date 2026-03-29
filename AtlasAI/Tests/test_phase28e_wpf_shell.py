"""Phase 28E — Tests for WPF Shell scaffold under Tools/."""
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
TOOLS_DIR = REPO_ROOT / "Tools"

WPF_HOST = TOOLS_DIR / "AtlasAI.WpfHost"
SHELL = TOOLS_DIR / "AtlasAI.Shell"
PANELS = TOOLS_DIR / "AtlasAI.Panels"
WORKSPACE = TOOLS_DIR / "AtlasAI.Workspace"


def _read(path: Path) -> str:
    return path.read_text()


# ---------------------------------------------------------------------------
# Project files exist
# ---------------------------------------------------------------------------

class TestWpfHostProjectExists(unittest.TestCase):
    def test_csproj_exists(self):
        self.assertTrue((WPF_HOST / "AtlasAI.WpfHost.csproj").exists())

    def test_app_xaml_exists(self):
        self.assertTrue((WPF_HOST / "App.xaml").exists())

    def test_app_xaml_cs_exists(self):
        self.assertTrue((WPF_HOST / "App.xaml.cs").exists())


class TestShellProjectExists(unittest.TestCase):
    def test_csproj_exists(self):
        self.assertTrue((SHELL / "AtlasAI.Shell.csproj").exists())

    def test_shell_window_xaml_exists(self):
        self.assertTrue((SHELL / "ShellWindow.xaml").exists())

    def test_shell_window_xaml_cs_exists(self):
        self.assertTrue((SHELL / "ShellWindow.xaml.cs").exists())


class TestPanelsProjectExists(unittest.TestCase):
    def test_csproj_exists(self):
        self.assertTrue((PANELS / "AtlasAI.Panels.csproj").exists())

    def test_chat_panel_xaml_exists(self):
        self.assertTrue((PANELS / "ChatPanel.xaml").exists())

    def test_chat_panel_xaml_cs_exists(self):
        self.assertTrue((PANELS / "ChatPanel.xaml.cs").exists())

    def test_logs_panel_xaml_exists(self):
        self.assertTrue((PANELS / "LogsPanel.xaml").exists())

    def test_logs_panel_xaml_cs_exists(self):
        self.assertTrue((PANELS / "LogsPanel.xaml.cs").exists())

    def test_build_panel_xaml_exists(self):
        self.assertTrue((PANELS / "BuildPanel.xaml").exists())

    def test_build_panel_xaml_cs_exists(self):
        self.assertTrue((PANELS / "BuildPanel.xaml.cs").exists())


class TestWorkspaceProjectExists(unittest.TestCase):
    def test_csproj_exists(self):
        self.assertTrue((WORKSPACE / "AtlasAI.Workspace.csproj").exists())

    def test_workspace_manager_cs_exists(self):
        self.assertTrue((WORKSPACE / "WorkspaceManager.cs").exists())

    def test_workspace_session_cs_exists(self):
        self.assertTrue((WORKSPACE / "WorkspaceSession.cs").exists())


# ---------------------------------------------------------------------------
# Aliases for tests referring to individual files
# ---------------------------------------------------------------------------

class TestShellWindowExists(unittest.TestCase):
    def test_shell_window_xaml_exists(self):
        self.assertTrue((SHELL / "ShellWindow.xaml").exists())


class TestChatPanelExists(unittest.TestCase):
    def test_chat_panel_exists(self):
        self.assertTrue((PANELS / "ChatPanel.xaml").exists())


class TestLogsPanelExists(unittest.TestCase):
    def test_logs_panel_exists(self):
        self.assertTrue((PANELS / "LogsPanel.xaml").exists())


class TestBuildPanelExists(unittest.TestCase):
    def test_build_panel_exists(self):
        self.assertTrue((PANELS / "BuildPanel.xaml").exists())


class TestWorkspaceManagerExists(unittest.TestCase):
    def test_workspace_manager_exists(self):
        self.assertTrue((WORKSPACE / "WorkspaceManager.cs").exists())


class TestWorkspaceSessionExists(unittest.TestCase):
    def test_workspace_session_exists(self):
        self.assertTrue((WORKSPACE / "WorkspaceSession.cs").exists())


# ---------------------------------------------------------------------------
# Target framework checks
# ---------------------------------------------------------------------------

class TestCsprojTargetFramework(unittest.TestCase):
    def test_wpfhost_target_framework(self):
        content = _read(WPF_HOST / "AtlasAI.WpfHost.csproj")
        self.assertIn("net8.0-windows", content)

    def test_shell_target_framework(self):
        content = _read(SHELL / "AtlasAI.Shell.csproj")
        self.assertIn("net8.0-windows", content)

    def test_panels_target_framework(self):
        content = _read(PANELS / "AtlasAI.Panels.csproj")
        self.assertIn("net8.0-windows", content)

    def test_workspace_target_framework(self):
        content = _read(WORKSPACE / "AtlasAI.Workspace.csproj")
        self.assertIn("net8.0-windows", content)

    def test_wpfhost_uses_wpf(self):
        content = _read(WPF_HOST / "AtlasAI.WpfHost.csproj")
        self.assertIn("UseWPF", content)

    def test_shell_uses_wpf(self):
        content = _read(SHELL / "AtlasAI.Shell.csproj")
        self.assertIn("UseWPF", content)

    def test_panels_uses_wpf(self):
        content = _read(PANELS / "AtlasAI.Panels.csproj")
        self.assertIn("UseWPF", content)

    def test_workspace_uses_wpf(self):
        content = _read(WORKSPACE / "AtlasAI.Workspace.csproj")
        self.assertIn("UseWPF", content)


# ---------------------------------------------------------------------------
# XAML content checks
# ---------------------------------------------------------------------------

class TestShellWindowXamlContent(unittest.TestCase):
    def _content(self) -> str:
        return _read(SHELL / "ShellWindow.xaml")

    def test_has_window_element(self):
        self.assertIn("<Window", self._content())

    def test_has_menu(self):
        self.assertIn("<Menu", self._content())

    def test_has_toolbar(self):
        self.assertIn("<ToolBar", self._content())

    def test_has_status_bar(self):
        self.assertIn("<StatusBar", self._content())

    def test_has_grid(self):
        self.assertIn("<Grid", self._content())

    def test_shell_namespace_class(self):
        self.assertIn("AtlasAI.Shell.ShellWindow", self._content())

    def test_has_grid_splitter(self):
        self.assertIn("GridSplitter", self._content())

    def test_has_scroll_viewer(self):
        self.assertIn("ScrollViewer", self._content())


class TestChatPanelNamespace(unittest.TestCase):
    def test_chat_panel_class_attribute(self):
        content = _read(PANELS / "ChatPanel.xaml")
        self.assertIn("AtlasAI.Panels.ChatPanel", content)

    def test_chat_panel_cs_namespace(self):
        content = _read(PANELS / "ChatPanel.xaml.cs")
        self.assertIn("AtlasAI.Panels", content)

    def test_logs_panel_cs_namespace(self):
        content = _read(PANELS / "LogsPanel.xaml.cs")
        self.assertIn("AtlasAI.Panels", content)

    def test_build_panel_cs_namespace(self):
        content = _read(PANELS / "BuildPanel.xaml.cs")
        self.assertIn("AtlasAI.Panels", content)

    def test_workspace_manager_namespace(self):
        content = _read(WORKSPACE / "WorkspaceManager.cs")
        self.assertIn("AtlasAI.Workspace", content)

    def test_workspace_session_namespace(self):
        content = _read(WORKSPACE / "WorkspaceSession.cs")
        self.assertIn("AtlasAI.Workspace", content)


# ---------------------------------------------------------------------------
# App XAML content checks
# ---------------------------------------------------------------------------

class TestAppXamlContent(unittest.TestCase):
    def test_app_xaml_startup_uri(self):
        content = _read(WPF_HOST / "App.xaml.cs")
        # ShellWindow is in a separate library; App.xaml.cs programmatically shows it
        self.assertIn("ShellWindow", content)

    def test_app_xaml_application_element(self):
        content = _read(WPF_HOST / "App.xaml")
        self.assertIn("<Application", content)

    def test_app_xaml_class(self):
        content = _read(WPF_HOST / "App.xaml")
        self.assertIn("AtlasAI.WpfHost.App", content)

    def test_app_cs_namespace(self):
        content = _read(WPF_HOST / "App.xaml.cs")
        self.assertIn("AtlasAI.WpfHost", content)


# ---------------------------------------------------------------------------
# Workspace class content
# ---------------------------------------------------------------------------

class TestWorkspaceManagerContent(unittest.TestCase):
    def test_create_session_method(self):
        content = _read(WORKSPACE / "WorkspaceManager.cs")
        self.assertIn("CreateSession", content)

    def test_get_session_method(self):
        content = _read(WORKSPACE / "WorkspaceManager.cs")
        self.assertIn("GetSession", content)

    def test_close_session_method(self):
        content = _read(WORKSPACE / "WorkspaceManager.cs")
        self.assertIn("CloseSession", content)

    def test_list_session_ids_method(self):
        content = _read(WORKSPACE / "WorkspaceManager.cs")
        self.assertIn("ListSessionIds", content)

    def test_session_count_property(self):
        content = _read(WORKSPACE / "WorkspaceManager.cs")
        self.assertIn("SessionCount", content)


class TestWorkspaceSessionContent(unittest.TestCase):
    def test_session_id_property(self):
        content = _read(WORKSPACE / "WorkspaceSession.cs")
        self.assertIn("SessionId", content)

    def test_is_active_property(self):
        content = _read(WORKSPACE / "WorkspaceSession.cs")
        self.assertIn("IsActive", content)

    def test_workspace_path_property(self):
        content = _read(WORKSPACE / "WorkspaceSession.cs")
        self.assertIn("WorkspacePath", content)

    def test_open_files_property(self):
        content = _read(WORKSPACE / "WorkspaceSession.cs")
        self.assertIn("OpenFiles", content)

    def test_duration_property(self):
        content = _read(WORKSPACE / "WorkspaceSession.cs")
        self.assertIn("Duration", content)


if __name__ == "__main__":
    unittest.main()
