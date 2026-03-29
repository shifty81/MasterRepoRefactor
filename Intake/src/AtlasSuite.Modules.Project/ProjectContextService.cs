namespace AtlasSuite.Modules.Project;

public sealed class ProjectContextService
{
    public string CurrentProjectName { get; private set; } = "NovaForge";

    public void SetCurrentProject(string projectName)
    {
        CurrentProjectName = projectName;
    }
}
