using AtlasSuite.Core.Docking;

namespace AtlasSuite.Core.Abstractions;

public interface IPanelRegistry
{
    void Register(PanelDescriptor descriptor);
    IReadOnlyCollection<PanelDescriptor> GetAll();
}
