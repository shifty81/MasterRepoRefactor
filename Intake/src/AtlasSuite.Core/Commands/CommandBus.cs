using AtlasSuite.Core.Abstractions;

namespace AtlasSuite.Core.Commands;

public sealed class CommandBus : ICommandBus
{
    private readonly Dictionary<string, CommandDefinition> _commands = new(StringComparer.OrdinalIgnoreCase);

    public void Register(CommandDefinition command)
    {
        ArgumentNullException.ThrowIfNull(command);
        _commands[command.Id] = command;
    }

    public IReadOnlyCollection<CommandDefinition> GetAll() => _commands.Values.OrderBy(c => c.Category).ThenBy(c => c.Label).ToArray();

    public async Task ExecuteAsync(string commandId, CancellationToken cancellationToken = default)
    {
        if (!_commands.TryGetValue(commandId, out var command))
        {
            throw new InvalidOperationException($"Command '{commandId}' is not registered.");
        }

        await command.Handler(cancellationToken).ConfigureAwait(false);
    }
}
