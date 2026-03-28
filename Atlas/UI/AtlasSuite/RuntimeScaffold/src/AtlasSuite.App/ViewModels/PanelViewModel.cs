using AtlasSuite.Core.Docking;

namespace AtlasSuite.App.ViewModels;

public sealed class PanelViewModel : ViewModelBase
{
    public required string Id { get; init; }
    public required string Title { get; init; }
    public required DockZone DockZone { get; init; }
    public required object Content { get; init; }
}
