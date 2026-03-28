using System.Threading.Tasks;
using Runtime.NovaForge.DevWorld.Services;

namespace UI.AtlasSuite.PlaytestHost;

public sealed class RigPlaytestCommand
{
    private readonly IRigSmokeTestService _rigSmokeTestService;

    public RigPlaytestCommand(IRigSmokeTestService rigSmokeTestService)
    {
        _rigSmokeTestService = rigSmokeTestService;
    }

    public Task<bool> ExecuteAsync()
    {
        return _rigSmokeTestService.RunAsync("dev_player_001");
    }
}
