namespace AtlasSuite.Core.Jobs;

public sealed record JobDefinition(
    string Id,
    string Label,
    Func<CancellationToken, Task> Work,
    int Priority = 0);
