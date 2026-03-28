using AtlasSuite.Integration;

namespace AtlasSuite.PlaytestHost;

public sealed class PlaytestService
{
    public static PlaytestService Instance { get; } = new();

    public bool IsInPlayMode { get; private set; }

    private PlaytestService() { }

    public void EnterPlayMode()
    {
        if (IsInPlayMode) return;
        EngineBridge.Instance.StartPlaySession();
        IsInPlayMode = true;
    }

    public void ExitPlayMode()
    {
        if (!IsInPlayMode) return;
        EngineBridge.Instance.StopPlaySession();
        IsInPlayMode = false;
    }
}
