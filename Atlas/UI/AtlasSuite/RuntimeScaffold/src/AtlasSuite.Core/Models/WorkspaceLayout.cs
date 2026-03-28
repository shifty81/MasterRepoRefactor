using AtlasSuite.Core.Docking;

namespace AtlasSuite.Core.Models;

public sealed class WorkspaceLayout
{
    public string Name { get; init; } = "Default";
    public List<WorkspacePanelPlacement> Panels { get; init; } = [];
}

public sealed class WorkspacePanelPlacement
{
    public string PanelId { get; init; } = string.Empty;
    public DockZone Dock { get; init; } = DockZone.Center;
    public int Order { get; init; }
}
