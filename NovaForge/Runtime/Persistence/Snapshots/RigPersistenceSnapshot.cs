namespace Runtime.NovaForge.Persistence.Snapshots;

public sealed record RigPersistenceSnapshot(
    string PlayerId,
    string LoadoutRef,
    float Health,
    float Integrity,
    float Oxygen,
    float Power,
    float Heat);
