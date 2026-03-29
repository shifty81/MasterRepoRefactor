namespace AtlasSuite.Core.Commands;

public sealed record CommandDefinition(
    string Id,
    string Label,
    string Category,
    Func<CancellationToken, Task> Handler,
    string? Description = null);
