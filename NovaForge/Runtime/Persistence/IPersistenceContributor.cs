namespace Runtime.NovaForge.Persistence;

public interface IPersistenceContributor
{
    string ContributorId { get; }
    bool IsRequired { get; }
    object CaptureSnapshot();
    void RestoreSnapshot(object snapshot);
    PersistenceValidationResult ValidateRestoredState();
}
