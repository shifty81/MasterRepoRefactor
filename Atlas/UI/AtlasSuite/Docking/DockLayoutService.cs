namespace AtlasSuite.Docking;

public sealed class DockLayoutService
{
    public static DockLayoutService Instance { get; } = new();

    private DockLayoutService() { }

    public void LoadLayout()
    {
        // TODO: Restore serialized docking layout.
    }

    public void SaveLayout()
    {
        // TODO: Persist current docking layout.
    }
}
