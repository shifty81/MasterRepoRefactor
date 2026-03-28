using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;

namespace Runtime.NovaForge.Persistence;

public sealed class PersistenceCoordinator
{
    private readonly PersistenceRegistry _registry;
    private readonly SaveSlotService _slotService;
    private readonly JsonSnapshotSerializer _serializer;

    public PersistenceCoordinator(
        PersistenceRegistry registry,
        SaveSlotService slotService,
        JsonSnapshotSerializer serializer)
    {
        _registry = registry;
        _slotService = slotService;
        _serializer = serializer;
    }

    public SaveManifest SaveAll(string rootPath, string slotId, string projectId, string worldId)
    {
        var slotPath = _slotService.EnsureSlotPath(rootPath, slotId);
        var refs = new List<ContributorSnapshotRef>();

        foreach (var contributor in _registry.GetContributors())
        {
            var snapshot = contributor.CaptureSnapshot();
            var snapshotPath = _slotService.BuildContributorSnapshotPath(slotPath, contributor.ContributorId);
            File.WriteAllText(snapshotPath, _serializer.Serialize(snapshot));

            refs.Add(new ContributorSnapshotRef(
                contributor.ContributorId,
                snapshot.GetType().Name,
                snapshotPath,
                contributor.IsRequired));
        }

        var manifest = new SaveManifest(
            Guid.NewGuid().ToString("N"),
            1,
            projectId,
            worldId,
            DateTime.UtcNow,
            refs);

        File.WriteAllText(_slotService.BuildManifestPath(slotPath), _serializer.Serialize(manifest));
        return manifest;
    }

    public IReadOnlyList<PersistenceValidationResult> ValidateAll()
    {
        return _registry.GetContributors().Select(x => x.ValidateRestoredState()).ToList();
    }
}
