namespace Runtime.NovaForge.Persistence;

public sealed record ContributorSnapshotRef(
    string ContributorId,
    string SnapshotType,
    string SnapshotPath,
    bool IsRequired);
