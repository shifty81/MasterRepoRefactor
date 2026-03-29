using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Text.Json;
using System.Threading;
using System.Threading.Tasks;

namespace Arbiter.ProjectAdapters.NovaForge
{
    public sealed class NovaForgeProjectAdapter
    {
        private readonly HttpClient _httpClient;
        private readonly NovaForgeProjectManifest _manifest;

        public NovaForgeProjectAdapter(HttpClient httpClient, NovaForgeProjectManifest manifest)
        {
            _httpClient = httpClient ?? throw new ArgumentNullException(nameof(httpClient));
            _manifest = manifest ?? throw new ArgumentNullException(nameof(manifest));
        }

        public string ProjectId => _manifest.ProjectId;
        public string DisplayName => _manifest.DisplayName;
        public IReadOnlyList<string> Capabilities => _manifest.Capabilities;

        public async Task<string> GetProjectInfoAsync(CancellationToken cancellationToken = default)
        {
            using var response = await _httpClient.GetAsync($"{_manifest.Bridge.BaseUrl}/project/info", cancellationToken);
            response.EnsureSuccessStatusCode();
            return await response.Content.ReadAsStringAsync(cancellationToken);
        }

        public async Task<string> GetEditorSelectionAsync(CancellationToken cancellationToken = default)
        {
            using var response = await _httpClient.GetAsync($"{_manifest.Bridge.BaseUrl}/editor/selection", cancellationToken);
            response.EnsureSuccessStatusCode();
            return await response.Content.ReadAsStringAsync(cancellationToken);
        }

        public async Task<string> RunBuildAsync(string targetId, bool clean = false, bool verbose = false, CancellationToken cancellationToken = default)
        {
            var payload = JsonSerializer.Serialize(new
            {
                targetId,
                clean,
                verbose
            });

            using var content = new StringContent(payload, System.Text.Encoding.UTF8, "application/json");
            using var response = await _httpClient.PostAsync($"{_manifest.Bridge.BaseUrl}/build/run", content, cancellationToken);
            response.EnsureSuccessStatusCode();
            return await response.Content.ReadAsStringAsync(cancellationToken);
        }

        public async Task<string> RunToolActionAsync(string actionId, string jsonPayload, bool dryRun = true, CancellationToken cancellationToken = default)
        {
            var payload = JsonSerializer.Serialize(new
            {
                actionId,
                jsonPayload,
                dryRun
            });

            using var content = new StringContent(payload, System.Text.Encoding.UTF8, "application/json");
            using var response = await _httpClient.PostAsync($"{_manifest.Bridge.BaseUrl}/editor/tools/run", content, cancellationToken);
            response.EnsureSuccessStatusCode();
            return await response.Content.ReadAsStringAsync(cancellationToken);
        }
    }
}
