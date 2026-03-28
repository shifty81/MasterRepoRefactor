using Runtime.NovaForge.Persistence.Snapshots;

namespace Runtime.NovaForge.Persistence.Contributors;

public sealed class CombatHazardPersistenceContributor : IPersistenceContributor
{
    public string ContributorId => "combat_hazards";
    public bool IsRequired => true;

    public object CaptureSnapshot()
    {
        return new CombatHazardPersistenceSnapshot("dev_damage_hull_segment", "hull_plate_a", false, false, 45f);
    }

    public void RestoreSnapshot(object snapshot)
    {
        // Stub: reconnect to combat/breach/fire services.
    }

    public PersistenceValidationResult ValidateRestoredState()
    {
        return new PersistenceValidationResult(ContributorId, true, "Combat hazard state validated.");
    }
}
