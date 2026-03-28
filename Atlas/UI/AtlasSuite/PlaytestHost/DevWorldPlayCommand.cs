using Runtime.NovaForge.DevWorld;

namespace UI.AtlasSuite.PlaytestHost
{
    public sealed class DevWorldPlayCommand
    {
        private readonly DevWorldBootstrap _bootstrap;

        public DevWorldPlayCommand(DevWorldBootstrap bootstrap)
        {
            _bootstrap = bootstrap;
        }

        public void Execute()
        {
            _bootstrap.Start();
        }
    }
}
