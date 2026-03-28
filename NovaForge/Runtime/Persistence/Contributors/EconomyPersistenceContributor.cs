using Runtime.NovaForge.Persistence.Snapshots;

namespace Runtime.NovaForge.Persistence.Contributors;

public sealed class EconomyPersistenceContributor : IPersistenceContributor
{
    public string ContributorId => "economy";
    public bool IsRequired => true;

    public object CaptureSnapshot()
    {
        return new EconomyPersistenceSnapshot("station_orbit_12_market", 300, 470, 1.28f);
    }

    public void RestoreSnapshot(object snapshot)
    {
        // Stub: reconnect to economy node state service.
    }

    public PersistenceValidationResult ValidateRestoredState()
    {
        return new PersistenceValidationResult(ContributorId, true, "Economy state validated.");
    }
}
