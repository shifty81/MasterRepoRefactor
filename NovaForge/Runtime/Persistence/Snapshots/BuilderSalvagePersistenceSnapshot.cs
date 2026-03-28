namespace Runtime.NovaForge.Persistence.Snapshots;

public sealed record BuilderSalvagePersistenceSnapshot(
    int PlacedParts,
    int WeldedParts,
    int SalvageRecoveries);
