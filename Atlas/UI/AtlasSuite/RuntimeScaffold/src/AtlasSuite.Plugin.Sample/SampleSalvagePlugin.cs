using AtlasSuite.Core.Abstractions;
using AtlasSuite.Core.Commands;
using AtlasSuite.Core.Docking;
using AtlasSuite.Plugins.Abstractions;

namespace AtlasSuite.Plugin.Sample;

public sealed class SampleSalvagePlugin : IAtlasSuitePlugin
{
    public string Id => "plugin.sample.salvage";
    public string DisplayName => "Sample Salvage Tools";

    public void Register(IPanelRegistry panelRegistry, ICommandBus commandBus)
    {
        panelRegistry.Register(new PanelDescriptor(
            Id: "panel.salvageDebug",
            Title: "Salvage Debug",
            DefaultDock: DockZone.Right,
            ViewKey: "SalvageDebugPanel",
            Category: "Gameplay"));

        commandBus.Register(new CommandDefinition(
            Id: "playtest.salvage",
            Label: "Run Salvage Playtest",
            Category: "Playtest",
            Handler: _ => Task.CompletedTask,
            Description: "Starts the salvage scenario stub."));
    }
}
