using System.Collections.Generic;

namespace Arbiter.ProjectAdapters.NovaForge
{
    public sealed class NovaForgeProjectManifest
    {
        public string ProjectId { get; set; } = "novaforge";
        public string DisplayName { get; set; } = "NovaForge";
        public int Version { get; set; } = 1;
        public string RepoRoot { get; set; } = ".";
        public string DataRoot { get; set; } = "data";
        public string DocsRoot { get; set; } = "docs";
        public string IntegrationsRoot { get; set; } = "integrations/arbiter";
        public BridgeSettings Bridge { get; set; } = new();
        public List<string> Capabilities { get; set; } = new();

        public sealed class BridgeSettings
        {
            public string Transport { get; set; } = "http";
            public string BaseUrl { get; set; } = "http://127.0.0.1:8005";
            public int TimeoutMs { get; set; } = 8000;
        }
    }
}
