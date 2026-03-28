using System.Windows;
using AtlasSuite.Workspace;
using AtlasSuite.ToolHost;
using AtlasSuite.Integration;

namespace AtlasSuite.App;

public partial class App : Application
{
    protected override void OnStartup(StartupEventArgs e)
    {
        base.OnStartup(e);

        WorkspaceService.Instance.Initialize();
        ToolHostService.Instance.RegisterBuiltInTools();
        EngineBridge.Instance.Initialize();
    }

    protected override void OnExit(ExitEventArgs e)
    {
        EngineBridge.Instance.Shutdown();
        base.OnExit(e);
    }
}
