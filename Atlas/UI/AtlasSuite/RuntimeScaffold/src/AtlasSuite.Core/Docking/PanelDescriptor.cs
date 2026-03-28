namespace AtlasSuite.Core.Docking;

public sealed record PanelDescriptor(
    string Id,
    string Title,
    DockZone DefaultDock,
    string ViewKey,
    bool LazyLoad = true,
    string? Category = null);
