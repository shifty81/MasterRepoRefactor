using System.Collections.Generic;
using Runtime.NovaForge.Persistence;

namespace Runtime.NovaForge.DevWorld.Services;

public sealed class PersistenceSmokeTestService
{
    private readonly PersistenceCoordinator _coordinator;

    public PersistenceSmokeTestService(PersistenceCoordinator coordinator)
    {
        _coordinator = coordinator;
    }

    public SaveManifest RunSave(string rootPath)
    {
        return _coordinator.SaveAll(rootPath, "devworld_slot_01", "NovaForge", "dev_world");
    }

    public IReadOnlyList<PersistenceValidationResult> RunValidation()
    {
        return _coordinator.ValidateAll();
    }
}
