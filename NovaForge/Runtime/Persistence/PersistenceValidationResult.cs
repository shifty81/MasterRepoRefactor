namespace Runtime.NovaForge.Persistence;

public sealed record PersistenceValidationResult(
    string ContributorId,
    bool IsValid,
    string Message);
