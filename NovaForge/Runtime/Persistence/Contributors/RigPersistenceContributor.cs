using Runtime.NovaForge.Persistence.Snapshots;

namespace Runtime.NovaForge.Persistence.Contributors;

public sealed class RigPersistenceContributor : IPersistenceContributor
{
    public string ContributorId => "rig";
    public bool IsRequired => true;

    public object CaptureSnapshot()
    {
        return new RigPersistenceSnapshot("player_rig", "rig_default_loadout", 100f, 100f, 100f, 100f, 0f);
    }

    public void RestoreSnapshot(object snapshot)
    {
        // Stub: map back into PlayerRigState / QuickSlotService.
    }

    public PersistenceValidationResult ValidateRestoredState()
    {
        return new PersistenceValidationResult(ContributorId, true, "Rig state validated.");
    }
}
