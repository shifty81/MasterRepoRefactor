using AtlasSuite.Core.Abstractions;

namespace AtlasSuite.Plugins.Abstractions;

public interface IAtlasSuitePlugin
{
    string Id { get; }
    string DisplayName { get; }
    void Register(IPanelRegistry panelRegistry, ICommandBus commandBus);
}
