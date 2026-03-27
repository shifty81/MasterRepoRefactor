// NovaForgeProjectAdapter.cs
// Arbiter project adapter for NovaForge.
//
// This adapter:
// - loads the NovaForge project manifest
// - connects to the NovaForge Arbiter bridge service
// - exposes project info, build targets, and whitelisted tool actions to Arbiter
//
// Rules:
// - must not directly access gameplay runtime internals
// - must not contain WPF or UI code
// - all operations go through the bridge protocol defined in Shared/ToolProtocol

using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Text;
using System.Text.Json;
using System.Threading;
using System.Threading.Tasks;

namespace Arbiter.ProjectAdapters.NovaForge
{
    public sealed class NovaForgeProjectAdapter : IDisposable
    {
        private readonly NovaForgeProjectManifest _manifest;
        private readonly HttpClient               _http;
        private bool                              _disposed;

        public string ProjectId      => _manifest.Project.Id;
        public string ProjectName    => _manifest.Project.DisplayName;
        public string ProjectVersion => _manifest.Project.Version;

        public NovaForgeProjectAdapter(string repoRoot)
        {
            string manifestPath = NovaForgeProjectManifest.ResolveManifestPath(repoRoot);
            _manifest = NovaForgeProjectManifest.Load(manifestPath);

            _http = new HttpClient
            {
                BaseAddress = new Uri(
                    $"http://{_manifest.Bridge.Host}:{_manifest.Bridge.RestPort}/"),
                Timeout = TimeSpan.FromSeconds(_manifest.Bridge.TimeoutSeconds),
            };
        }

        // ----------------------------------------------------------------
        // Project info
        // ----------------------------------------------------------------

        /// <summary>Returns cached project info from the manifest.</summary>
        public ProjectInfoModel GetProjectInfo() => _manifest.Project;

        /// <summary>Returns capability flags from the manifest.</summary>
        public ProjectCapabilitiesModel GetCapabilities() => _manifest.Capabilities;

        /// <summary>Returns all configured build targets.</summary>
        public IReadOnlyList<BuildTargetModel> GetBuildTargets() =>
            _manifest.BuildTargets;

        /// <summary>Returns all allowed tool actions from safety settings.</summary>
        public IReadOnlyList<string> GetAllowedToolActions() =>
            _manifest.SafetySettings.AllowedToolActions;

        // ----------------------------------------------------------------
        // Bridge connectivity
        // ----------------------------------------------------------------

        /// <summary>
        /// Checks whether the NovaForge bridge service is reachable.
        /// </summary>
        public async Task<bool> IsBackendReachableAsync(
            CancellationToken cancellationToken = default)
        {
            try
            {
                var response = await _http.GetAsync(
                    "project/info", cancellationToken);
                return response.IsSuccessStatusCode;
            }
            catch
            {
                return false;
            }
        }

        // ----------------------------------------------------------------
        // Build
        // ----------------------------------------------------------------

        /// <summary>
        /// Requests a build via the bridge service.
        /// </summary>
        public async Task<BridgeResponse> RequestBuildAsync(
            string              targetName,
            string              configuration    = "Debug",
            CancellationToken   cancellationToken = default)
        {
            var payload = new
            {
                target        = targetName,
                configuration = configuration,
                platform      = "Win64",
                rebuild       = false,
            };

            return await PostAsync("build/run", payload, cancellationToken);
        }

        // ----------------------------------------------------------------
        // Editor state
        // ----------------------------------------------------------------

        /// <summary>
        /// Queries the current editor selection snapshot.
        /// </summary>
        public async Task<BridgeResponse> GetEditorSelectionAsync(
            CancellationToken cancellationToken = default)
        {
            try
            {
                var response = await _http.GetAsync(
                    "editor/selection", cancellationToken);
                string content = await response.Content.ReadAsStringAsync(cancellationToken);
                return new BridgeResponse(response.IsSuccessStatusCode, content);
            }
            catch (Exception ex)
            {
                return new BridgeResponse(false, ex.Message);
            }
        }

        // ----------------------------------------------------------------
        // Tool actions
        // ----------------------------------------------------------------

        /// <summary>
        /// Runs a whitelisted tool action. Defaults to dry-run for safety.
        /// </summary>
        public async Task<BridgeResponse> RunToolActionAsync(
            string              actionName,
            string?             parameter         = null,
            bool                dryRun            = true,
            CancellationToken   cancellationToken  = default)
        {
            if (!IsActionAllowed(actionName))
                return new BridgeResponse(false,
                    $"Tool action '{actionName}' is not in the allowed list.");

            var payload = new
            {
                action    = actionName,
                parameter = parameter ?? string.Empty,
                dryRun    = dryRun,
            };

            return await PostAsync("editor/tools/run", payload, cancellationToken);
        }

        // ----------------------------------------------------------------
        // Path helpers
        // ----------------------------------------------------------------

        /// <summary>Returns the absolute path to the data root.</summary>
        public string GetDataRoot(string repoRoot) =>
            System.IO.Path.Combine(repoRoot, _manifest.RepoPaths.DataRoot);

        /// <summary>Returns the absolute path to the content root.</summary>
        public string GetContentRoot(string repoRoot) =>
            System.IO.Path.Combine(repoRoot, _manifest.RepoPaths.ContentRoot);

        /// <summary>Returns the absolute path to the docs root.</summary>
        public string GetDocsRoot(string repoRoot) =>
            System.IO.Path.Combine(repoRoot, _manifest.RepoPaths.DocsRoot);

        // ----------------------------------------------------------------
        // Private helpers
        // ----------------------------------------------------------------

        private bool IsActionAllowed(string actionName)
        {
            foreach (var allowed in _manifest.SafetySettings.AllowedToolActions)
            {
                if (string.Equals(allowed, actionName,
                        StringComparison.OrdinalIgnoreCase))
                    return true;
            }
            return false;
        }

        private async Task<BridgeResponse> PostAsync(
            string            endpoint,
            object            payload,
            CancellationToken cancellationToken)
        {
            try
            {
                string json    = JsonSerializer.Serialize(payload);
                var    content = new StringContent(json, Encoding.UTF8, "application/json");
                var    response = await _http.PostAsync(endpoint, content, cancellationToken);
                string body    = await response.Content.ReadAsStringAsync(cancellationToken);
                return new BridgeResponse(response.IsSuccessStatusCode, body);
            }
            catch (Exception ex)
            {
                return new BridgeResponse(false, ex.Message);
            }
        }

        // ----------------------------------------------------------------
        // IDisposable
        // ----------------------------------------------------------------

        public void Dispose()
        {
            if (!_disposed)
            {
                _http.Dispose();
                _disposed = true;
            }
        }
    }

    /// <summary>Simple response wrapper for bridge calls.</summary>
    public sealed record BridgeResponse(bool Success, string Body);
}
