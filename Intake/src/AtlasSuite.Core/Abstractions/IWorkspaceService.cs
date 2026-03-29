using AtlasSuite.Core.Models;

namespace AtlasSuite.Core.Abstractions;

public interface IWorkspaceService
{
    WorkspaceLayout Current { get; }
    Task LoadDefaultAsync(CancellationToken cancellationToken = default);
    Task SaveAsync(WorkspaceLayout layout, CancellationToken cancellationToken = default);
}
