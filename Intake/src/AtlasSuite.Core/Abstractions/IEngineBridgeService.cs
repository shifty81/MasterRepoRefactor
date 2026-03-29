namespace AtlasSuite.Core.Abstractions;

public interface IEngineBridgeService
{
    Task InitializeAsync(CancellationToken cancellationToken = default);
    Task LoadProjectAsync(string projectName, CancellationToken cancellationToken = default);
    Task StartPlaytestAsync(string scenarioId, CancellationToken cancellationToken = default);
    Task StopPlaytestAsync(CancellationToken cancellationToken = default);
    Task SendCommandAsync(string commandType, object payload, CancellationToken cancellationToken = default);
}
