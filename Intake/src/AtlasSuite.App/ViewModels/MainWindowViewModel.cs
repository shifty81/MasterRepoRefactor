using System.Collections.ObjectModel;
using AtlasSuite.App.Commands;
using AtlasSuite.App.ViewModels.Panels;
using AtlasSuite.Core.Abstractions;
using AtlasSuite.Core.Commands;
using AtlasSuite.Core.Docking;
using AtlasSuite.Core.Jobs;
using AtlasSuite.Core.Models;
using AtlasSuite.Modules.AI;
using AtlasSuite.Modules.Project;
using AtlasSuite.App.Views.Panels;

namespace AtlasSuite.App.ViewModels;

public sealed class MainWindowViewModel : ViewModelBase
{
    private readonly ICommandBus _commandBus;
    private readonly IEngineBridgeService _engineBridgeService;
    private readonly IWorkspaceService _workspaceService;
    private readonly IJobRunner _jobRunner;
    private readonly AtlasAiService _atlasAiService;
    private readonly ProjectContextService _projectContextService;

    public MainWindowViewModel(
        ICommandBus commandBus,
        IEngineBridgeService engineBridgeService,
        IWorkspaceService workspaceService,
        IJobRunner jobRunner,
        AtlasAiService atlasAiService,
        ProjectContextService projectContextService,
        IPanelRegistry panelRegistry)
    {
        _commandBus = commandBus;
        _engineBridgeService = engineBridgeService;
        _workspaceService = workspaceService;
        _jobRunner = jobRunner;
        _atlasAiService = atlasAiService;
        _projectContextService = projectContextService;

        LogPanel = new LogPanelViewModel();
        AtlasAiPanel = new AtlasAiPanelViewModel();

        OpenProjectCommand = new RelayCommand(_ => RunFireAndForget(OpenProjectAsync));
        StartPlaytestCommand = new RelayCommand(_ => RunFireAndForget(() => _commandBus.ExecuteAsync("playtest.devworld")));
        StopPlaytestCommand = new RelayCommand(_ => RunFireAndForget(() => _commandBus.ExecuteAsync("playtest.stop")));
        AskAtlasAiCommand = new RelayCommand(_ => RunFireAndForget(AskAtlasAiAsync));

        RegisterCoreCommands();
        SeedPanels(panelRegistry);
        _jobRunner.JobCompleted += OnJobCompleted;
    }

    public string Title => $"Atlas Suite — {_projectContextService.CurrentProjectName}";
    public ObservableCollection<PanelViewModel> LeftPanels { get; } = [];
    public ObservableCollection<PanelViewModel> CenterPanels { get; } = [];
    public ObservableCollection<PanelViewModel> RightPanels { get; } = [];
    public ObservableCollection<PanelViewModel> BottomPanels { get; } = [];
    public LogPanelViewModel LogPanel { get; }
    public AtlasAiPanelViewModel AtlasAiPanel { get; }

    public RelayCommand OpenProjectCommand { get; }
    public RelayCommand StartPlaytestCommand { get; }
    public RelayCommand StopPlaytestCommand { get; }
    public RelayCommand AskAtlasAiCommand { get; }

    public async Task InitializeAsync()
    {
        await _engineBridgeService.InitializeAsync().ConfigureAwait(false);
        await _workspaceService.LoadDefaultAsync().ConfigureAwait(false);
        ApplyWorkspace(_workspaceService.Current);
        LogPanel.Append("Atlas Suite shell initialized.");
    }

    private void RegisterCoreCommands()
    {
        _commandBus.Register(new CommandDefinition(
            "project.open.default",
            "Open NovaForge",
            "Project",
            async _ => await OpenProjectAsync().ConfigureAwait(false),
            "Loads the default NovaForge project context."));

        _commandBus.Register(new CommandDefinition(
            "playtest.devworld",
            "Run Dev World Playtest",
            "Playtest",
            async _ =>
            {
                await _engineBridgeService.StartPlaytestAsync("dev_world").ConfigureAwait(false);
                LogPanel.Append("Started Dev World playtest.");
            }));

        _commandBus.Register(new CommandDefinition(
            "playtest.stop",
            "Stop Playtest",
            "Playtest",
            async _ =>
            {
                await _engineBridgeService.StopPlaytestAsync().ConfigureAwait(false);
                LogPanel.Append("Stopped playtest.");
            }));
    }

    private void SeedPanels(IPanelRegistry panelRegistry)
    {
        panelRegistry.Register(new PanelDescriptor("panel.projectExplorer", "Project Explorer", DockZone.Left, "ProjectExplorerPanel", Category: "Project"));
        panelRegistry.Register(new PanelDescriptor("panel.sceneViewport", "Scene Viewport", DockZone.Center, "SceneViewportPanel", Category: "Runtime"));
        panelRegistry.Register(new PanelDescriptor("panel.inspector", "Inspector", DockZone.Right, "InspectorPanel", Category: "Editor"));
        panelRegistry.Register(new PanelDescriptor("panel.outputLog", "Output Log", DockZone.Bottom, "OutputLogPanel", Category: "Diagnostics"));
        panelRegistry.Register(new PanelDescriptor("panel.atlasAi", "AtlasAI", DockZone.Right, "AtlasAiPanel", Category: "AI"));
    }

    private async Task OpenProjectAsync()
    {
        _jobRunner.Enqueue(new JobDefinition(
            Id: "job.openProject",
            Label: "Open NovaForge",
            Work: async _ =>
            {
                _projectContextService.SetCurrentProject("NovaForge");
                await _engineBridgeService.LoadProjectAsync("NovaForge").ConfigureAwait(false);
            }));

        LogPanel.Append("Queued NovaForge open project job.");
        RaisePropertyChanged(nameof(Title));
        await Task.CompletedTask;
    }

    private async Task AskAtlasAiAsync()
    {
        var request = string.IsNullOrWhiteSpace(AtlasAiPanel.Request)
            ? "Create the next implementation task for Atlas Suite foundation."
            : AtlasAiPanel.Request;

        AtlasAiPanel.Response = await _atlasAiService.PlanAsync(request).ConfigureAwait(false);
        LogPanel.Append("AtlasAI responded to current request.");
    }

    private void ApplyWorkspace(WorkspaceLayout layout)
    {
        LeftPanels.Clear();
        CenterPanels.Clear();
        RightPanels.Clear();
        BottomPanels.Clear();

        foreach (var panel in layout.Panels.OrderBy(p => p.Order))
        {
            var vm = panel.PanelId switch
            {
                "panel.outputLog" => new PanelViewModel { Id = panel.PanelId, Title = "Output Log", DockZone = panel.Dock, Content = new OutputLogPanelView { DataContext = LogPanel } },
                "panel.atlasAi" => new PanelViewModel { Id = panel.PanelId, Title = "AtlasAI", DockZone = panel.Dock, Content = new AtlasAiPanelView { DataContext = AtlasAiPanel } },
                "panel.projectExplorer" => new PanelViewModel { Id = panel.PanelId, Title = "Project Explorer", DockZone = panel.Dock, Content = "NovaForge / Atlas / Docs / Assets" },
                "panel.sceneViewport" => new PanelViewModel { Id = panel.PanelId, Title = "Scene Viewport", DockZone = panel.Dock, Content = "Viewport host placeholder" },
                _ => new PanelViewModel { Id = panel.PanelId, Title = panel.PanelId, DockZone = panel.Dock, Content = $"{panel.PanelId} placeholder" }
            };

            GetBucket(panel.Dock).Add(vm);
        }
    }

    private ObservableCollection<PanelViewModel> GetBucket(DockZone dockZone) => dockZone switch
    {
        DockZone.Left => LeftPanels,
        DockZone.Right => RightPanels,
        DockZone.Bottom => BottomPanels,
        _ => CenterPanels
    };

    private void OnJobCompleted(object? sender, JobRecord record)
    {
        LogPanel.Append($"Job '{record.Label}' finished with status: {record.Status}.");
    }

    private void RunFireAndForget(Func<Task> action)
    {
        _ = Task.Run(async () =>
        {
            try
            {
                await action().ConfigureAwait(false);
            }
            catch (Exception ex)
            {
                LogPanel.Append($"Error: {ex.Message}");
            }
        });
    }
}
