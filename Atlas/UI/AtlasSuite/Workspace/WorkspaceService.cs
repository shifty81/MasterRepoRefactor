namespace AtlasSuite.Workspace;

public sealed class WorkspaceService
{
    public static WorkspaceService Instance { get; } = new();

    public string? ActiveProjectName { get; private set; }
    public string? ActiveProjectPath { get; private set; }

    private WorkspaceService() { }

    public void Initialize()
    {
        // TODO: Load workspace settings, recent projects, and shell state.
    }

    public void LoadProject(string projectName, string? projectPath = null)
    {
        ActiveProjectName = projectName;
        ActiveProjectPath = projectPath;
    }
}
