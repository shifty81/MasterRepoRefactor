using AtlasSuite.Core.Abstractions;

namespace AtlasSuite.Core.Docking;

public sealed class PanelRegistry : IPanelRegistry
{
    private readonly Dictionary<string, PanelDescriptor> _panels = new(StringComparer.OrdinalIgnoreCase);

    public void Register(PanelDescriptor descriptor)
    {
        ArgumentNullException.ThrowIfNull(descriptor);
        _panels[descriptor.Id] = descriptor;
    }

    public IReadOnlyCollection<PanelDescriptor> GetAll() => _panels.Values.OrderBy(p => p.Title).ToArray();
}
