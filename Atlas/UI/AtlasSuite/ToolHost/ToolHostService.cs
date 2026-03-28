using System.Collections.Generic;

namespace AtlasSuite.ToolHost;

public sealed class ToolHostService
{
    public static ToolHostService Instance { get; } = new();

    private readonly List<string> _registeredTools = new();

    private ToolHostService() { }

    public IReadOnlyList<string> RegisteredTools => _registeredTools;

    public void RegisterBuiltInTools()
    {
        _registeredTools.Clear();
        _registeredTools.Add("ContentBrowser");
        _registeredTools.Add("Inspector");
        _registeredTools.Add("WorldOutliner");
        _registeredTools.Add("OutputLog");
        _registeredTools.Add("CommandPalette");
        _registeredTools.Add("DebugPanel");
        _registeredTools.Add("MissionDebug");
        _registeredTools.Add("EconomyDebug");
        _registeredTools.Add("FactionDebug");
        _registeredTools.Add("RigLoadout");
        _registeredTools.Add("ArbiterPanel");
    }
}
