namespace Runtime.NovaForge.Persistence.Snapshots;

public sealed record EconomyPersistenceSnapshot(
    string NodeId,
    int LocalSupply,
    int LocalDemand,
    float PriceMultiplier);
