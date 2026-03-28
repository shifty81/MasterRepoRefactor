using Runtime.NovaForge.Persistence.Snapshots;

namespace Runtime.NovaForge.Persistence.Contributors;

public sealed class BuilderSalvagePersistenceContributor : IPersistenceContributor
{
    public string ContributorId => "builder_salvage";
    public bool IsRequired => true;

    public object CaptureSnapshot()
    {
        return new BuilderSalvagePersistenceSnapshot(1, 1, 1);
    }

    public void RestoreSnapshot(object snapshot)
    {
        // Stub: reconnect to BuilderPlacementService / salvage state.
    }

    public PersistenceValidationResult ValidateRestoredState()
    {
        return new PersistenceValidationResult(ContributorId, true, "Builder/salvage state validated.");
    }
}
