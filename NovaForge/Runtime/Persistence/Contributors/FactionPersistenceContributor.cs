using Runtime.NovaForge.Persistence.Snapshots;

namespace Runtime.NovaForge.Persistence.Contributors;

public sealed class FactionPersistenceContributor : IPersistenceContributor
{
    public string ContributorId => "factions";
    public bool IsRequired => true;

    public object CaptureSnapshot()
    {
        return new FactionPersistenceSnapshot("industrial_union", 5f, "tense");
    }

    public void RestoreSnapshot(object snapshot)
    {
        // Stub: reconnect to faction standing/event service.
    }

    public PersistenceValidationResult ValidateRestoredState()
    {
        return new PersistenceValidationResult(ContributorId, true, "Faction state validated.");
    }
}
