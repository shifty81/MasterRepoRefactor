using System;
using System.Collections.Generic;

namespace Runtime.NovaForge.Persistence;

public sealed record SaveManifest(
    string ManifestId,
    int ManifestVersion,
    string ProjectId,
    string WorldId,
    DateTime SavedAtUtc,
    IReadOnlyList<ContributorSnapshotRef> Contributors);
