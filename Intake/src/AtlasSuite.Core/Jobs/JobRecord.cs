namespace AtlasSuite.Core.Jobs;

public sealed record JobRecord(
    string Id,
    string Label,
    DateTimeOffset StartedUtc,
    DateTimeOffset? FinishedUtc,
    string Status,
    string? Error = null);
