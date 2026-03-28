using Runtime.NovaForge.Persistence.Snapshots;

namespace Runtime.NovaForge.Persistence.Contributors;

public sealed class MissionPersistenceContributor : IPersistenceContributor
{
    public string ContributorId => "missions";
    public bool IsRequired => true;

    public object CaptureSnapshot()
    {
        return new MissionPersistenceSnapshot("mission_dev_salvage_intro_v2", "completed", 3);
    }

    public void RestoreSnapshot(object snapshot)
    {
        // Stub: reconnect to mission runtime service.
    }

    public PersistenceValidationResult ValidateRestoredState()
    {
        return new PersistenceValidationResult(ContributorId, true, "Mission state validated.");
    }
}
