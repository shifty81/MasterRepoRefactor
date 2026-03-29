using System.Windows;
using AtlasAI.Shell;

namespace AtlasAI.WpfHost;

public partial class App : Application
{
    protected override void OnStartup(StartupEventArgs e)
    {
        base.OnStartup(e);
        var shell = new ShellWindow();
        shell.Show();
    }
}
