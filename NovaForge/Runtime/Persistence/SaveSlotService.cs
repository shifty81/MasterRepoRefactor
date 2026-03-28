using System;
using System.Collections.Generic;
using System.IO;

namespace Runtime.NovaForge.Persistence;

public sealed class SaveSlotService
{
    public string EnsureSlotPath(string rootPath, string slotId)
    {
        var path = Path.Combine(rootPath, slotId);
        Directory.CreateDirectory(path);
        return path;
    }

    public string BuildContributorSnapshotPath(string slotPath, string contributorId)
    {
        return Path.Combine(slotPath, contributorId + ".json");
    }

    public string BuildManifestPath(string slotPath)
    {
        return Path.Combine(slotPath, "save_manifest.json");
    }
}
