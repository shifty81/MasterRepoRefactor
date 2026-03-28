using System.Windows;

namespace AtlasSuite.Integration;

public sealed class EngineBridge
{
    public static EngineBridge Instance { get; } = new();

    private FrameworkElement? _viewportSurface;

    private EngineBridge() { }

    public void Initialize()
    {
        // TODO: Initialize engine/editor/runtime bridge services.
    }

    public void Shutdown()
    {
        // TODO: Shutdown and release engine services.
    }

    public void AttachViewport(FrameworkElement viewportSurface)
    {
        _viewportSurface = viewportSurface;
        // TODO: Bind native/shared engine surface to WPF host.
    }

    public void DetachViewport()
    {
        _viewportSurface = null;
        // TODO: Unbind native/shared engine surface.
    }

    public void LoadProject(string projectName)
    {
        // TODO: Route project load into runtime/editor layer.
    }

    public void LoadWorld(string worldPath)
    {
        // TODO: Load NovaForge Dev World or target scene.
    }

    public void StartPlaySession()
    {
        // TODO: Enter PIE/playtest session.
    }

    public void StopPlaySession()
    {
        // TODO: Exit PIE/playtest session.
    }

    public void SaveCurrentState(string saveSlot)
    {
        // TODO: Save current test state.
    }

    public void LoadSavedState(string saveSlot)
    {
        // TODO: Load saved test state.
    }
}
