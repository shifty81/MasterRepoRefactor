namespace AtlasSuite.Modules.AI;

public sealed class AtlasAiService
{
    public Task<string> PlanAsync(string request, CancellationToken cancellationToken = default)
    {
        var response = $"AtlasAI plan scaffold for: {request}";
        return Task.FromResult(response);
    }
}
