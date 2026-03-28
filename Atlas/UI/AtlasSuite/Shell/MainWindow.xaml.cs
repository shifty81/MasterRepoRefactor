using System;
using System.Windows;
using AtlasSuite.Docking;
using AtlasSuite.PlaytestHost;
using AtlasSuite.ProjectBrowser;
using AtlasSuite.Integration;

namespace AtlasSuite.Shell;

public partial class MainWindow : Window
{
    public MainWindow()
    {
        InitializeComponent();
        DockLayoutService.Instance.LoadLayout();
        AppendLog("Atlas Suite started.");
    }

    private void OpenProject_Click(object sender, RoutedEventArgs e)
    {
        ProjectBrowserService.Instance.OpenProject("NovaForge");
        AppendLog("Opened project: NovaForge");
    }

    private void Play_Click(object sender, RoutedEventArgs e)
    {
        PlaytestService.Instance.EnterPlayMode();
        AppendLog("Entered Play mode.");
    }

    private void Stop_Click(object sender, RoutedEventArgs e)
    {
        PlaytestService.Instance.ExitPlayMode();
        AppendLog("Exited Play mode.");
    }

    private void LoadDevWorld_Click(object sender, RoutedEventArgs e)
    {
        EngineBridge.Instance.LoadWorld("Projects/NovaForge/Scenes/dev_world.json");
        AppendLog("Loaded Dev World.");
    }

    private void SaveLayout_Click(object sender, RoutedEventArgs e)
    {
        DockLayoutService.Instance.SaveLayout();
        AppendLog("Saved layout.");
    }

    private void CommandPalette_Click(object sender, RoutedEventArgs e)
    {
        AppendLog("Command Palette requested.");
    }

    private void Exit_Click(object sender, RoutedEventArgs e)
    {
        Close();
    }

    private void AppendLog(string message)
    {
        OutputLog.AppendText($"[{DateTime.Now:HH:mm:ss}] {message}{Environment.NewLine}");
        OutputLog.ScrollToEnd();
    }
}
