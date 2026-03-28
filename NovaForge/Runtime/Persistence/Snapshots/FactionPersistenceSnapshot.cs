namespace Runtime.NovaForge.Persistence.Snapshots;

public sealed record FactionPersistenceSnapshot(
    string FactionId,
    float StandingDelta,
    string EscalationState);
