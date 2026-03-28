using System.Windows;
using AtlasSuite.App.ViewModels;
using AtlasSuite.Core.Abstractions;
using AtlasSuite.Core.Commands;
using AtlasSuite.Core.Docking;
using AtlasSuite.Core.Jobs;
using AtlasSuite.Core.Services;
using AtlasSuite.Modules.AI;
using AtlasSuite.Modules.Engine;
using AtlasSuite.Modules.Project;
using AtlasSuite.Plugin.Sample;

namespace AtlasSuite.App.Views;

public partial class MainWindow : Window
{
    public MainWindow()
    {
        InitializeComponent();

        var commandBus = new CommandBus();
        var panelRegistry = new PanelRegistry();
        var workspaceService = new WorkspaceService(System.IO.Path.Combine(AppContext.BaseDirectory, "Resources", "Layouts", "DefaultWorkspace.json"));
        var engineBridge = new EngineBridgeService();
        var jobRunner = new InMemoryJobRunner();
        var atlasAiService = new AtlasAiService();
        var projectContext = new ProjectContextService();

        new SampleSalvagePlugin().Register(panelRegistry, commandBus);

        var viewModel = new MainWindowViewModel(
            commandBus,
            engineBridge,
            workspaceService,
            jobRunner,
            atlasAiService,
            projectContext,
            panelRegistry);

        DataContext = viewModel;
        Loaded += async (_, _) => await viewModel.InitializeAsync();
    }

    private void OnExitClick(object sender, RoutedEventArgs e)
    {
        Close();
    }
}
