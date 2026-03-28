namespace Runtime.NovaForge.Persistence.Snapshots;

public sealed record VehiclePersistenceSnapshot(
    string ActiveConstructId,
    string PossessionState,
    bool InMech,
    bool InShip);
