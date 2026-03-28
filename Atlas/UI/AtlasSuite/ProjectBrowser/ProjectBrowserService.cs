using AtlasSuite.Workspace;
using AtlasSuite.Integration;

namespace AtlasSuite.ProjectBrowser;

public sealed class ProjectBrowserService
{
    public static ProjectBrowserService Instance { get; } = new();

    private ProjectBrowserService() { }

    public void OpenProject(string projectName)
    {
        WorkspaceService.Instance.LoadProject(projectName);
        EngineBridge.Instance.LoadProject(projectName);
    }
}
