namespace Runtime.NovaForge.Persistence.Snapshots;

public sealed record CombatHazardPersistenceSnapshot(
    string TargetId,
    string ZoneId,
    bool HasActiveBreach,
    bool HasActiveFire,
    float LastAppliedDamage);
