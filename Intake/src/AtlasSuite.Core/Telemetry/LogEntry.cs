namespace AtlasSuite.Core.Telemetry;

public sealed record LogEntry(DateTimeOffset TimestampUtc, string Source, string Message);
