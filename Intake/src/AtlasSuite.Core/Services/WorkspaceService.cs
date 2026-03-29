using System.Text.Json;
using AtlasSuite.Core.Abstractions;
using AtlasSuite.Core.Models;

namespace AtlasSuite.Core.Services;

public sealed class WorkspaceService : IWorkspaceService
{
    private readonly string _defaultLayoutPath;

    public WorkspaceService(string defaultLayoutPath)
    {
        _defaultLayoutPath = defaultLayoutPath;
    }

    public WorkspaceLayout Current { get; private set; } = new();

    public async Task LoadDefaultAsync(CancellationToken cancellationToken = default)
    {
        await using var stream = File.OpenRead(_defaultLayoutPath);
        var layout = await JsonSerializer.DeserializeAsync<WorkspaceLayout>(stream, cancellationToken: cancellationToken).ConfigureAwait(false);
        Current = layout ?? new WorkspaceLayout();
    }

    public async Task SaveAsync(WorkspaceLayout layout, CancellationToken cancellationToken = default)
    {
        Current = layout;
        var json = JsonSerializer.Serialize(layout, new JsonSerializerOptions { WriteIndented = true });
        await File.WriteAllTextAsync(_defaultLayoutPath, json, cancellationToken).ConfigureAwait(false);
    }
}
