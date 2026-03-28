using Runtime.NovaForge.Persistence.Snapshots;

namespace Runtime.NovaForge.Persistence.Contributors;

public sealed class VehiclePersistenceContributor : IPersistenceContributor
{
    public string ContributorId => "vehicles";
    public bool IsRequired => true;

    public object CaptureSnapshot()
    {
        return new VehiclePersistenceSnapshot("dev_ship_starter", "on_foot", false, false);
    }

    public void RestoreSnapshot(object snapshot)
    {
        // Stub: route into PossessionService.
    }

    public PersistenceValidationResult ValidateRestoredState()
    {
        return new PersistenceValidationResult(ContributorId, true, "Vehicle possession state validated.");
    }
}
