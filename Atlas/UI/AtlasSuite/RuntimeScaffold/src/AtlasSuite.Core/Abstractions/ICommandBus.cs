using AtlasSuite.Core.Commands;

namespace AtlasSuite.Core.Abstractions;

public interface ICommandBus
{
    void Register(CommandDefinition command);
    IReadOnlyCollection<CommandDefinition> GetAll();
    Task ExecuteAsync(string commandId, CancellationToken cancellationToken = default);
}
