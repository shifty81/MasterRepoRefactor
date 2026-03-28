namespace Runtime.NovaForge.Persistence.Snapshots;

public sealed record MissionPersistenceSnapshot(
    string ActiveMissionId,
    string MissionState,
    int CompletedObjectiveCount);
