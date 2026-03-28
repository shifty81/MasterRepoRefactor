using AtlasSuite.Core.Abstractions;

namespace AtlasSuite.Modules.Engine;

public sealed class EngineBridgeService : IEngineBridgeService
{
    public Task InitializeAsync(CancellationToken cancellationToken = default)
    {
        return Task.CompletedTask;
    }

    public Task LoadProjectAsync(string projectName, CancellationToken cancellationToken = default)
    {
        // TODO: route into Atlas runtime/editor bootstrap.
        return Task.CompletedTask;
    }

    public Task StartPlaytestAsync(string scenarioId, CancellationToken cancellationToken = default)
    {
        // TODO: send SpawnScenario/EnterPlaytest to engine bridge transport.
        return Task.CompletedTask;
    }

    public Task StopPlaytestAsync(CancellationToken cancellationToken = default)
    {
        return Task.CompletedTask;
    }

    public Task SendCommandAsync(string commandType, object payload, CancellationToken cancellationToken = default)
    {
        return Task.CompletedTask;
    }
}
