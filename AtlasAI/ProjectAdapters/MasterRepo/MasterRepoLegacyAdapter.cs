// MasterRepoLegacyAdapter.cs
// AtlasAI project adapter for the legacy MasterRepo layout.
//
// This adapter bridges AtlasAI to the pre-refactor MasterRepo monorepo structure.
// It implements the full IProjectAdapter contract, routing all requests through
// the same bridge protocol as NovaForgeProjectAdapter while compensating for
// path and naming differences introduced by the Arbiter → AtlasAI rename.
//
// Rules:
// - Must not contain WPF or UI code.
// - All write operations go through dry-run by default.
// - Legacy naming (Arbiter.*) is translated to AtlasAI.* before bridge calls.
// - Disposable: always call Dispose() or use via `using`.

using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Text;
using System.Text.Json;
using System.Threading;
using System.Threading.Tasks;

using AtlasAI.ProjectAdapters;

namespace AtlasAI.ProjectAdapters.MasterRepo
{
    /// <summary>
    /// Adapts AtlasAI to a legacy MasterRepo that still uses the pre-refactor
    /// Arbiter naming and folder structure.  All bridge calls use the same
    /// REST+WebSocket protocol as the modern NovaForge adapter.
    /// </summary>
    public sealed class MasterRepoLegacyAdapter : IProjectAdapter
    {
        private readonly MasterRepoLegacyManifestDocument _manifest;
        private readonly HttpClient                        _http;
        private          string                            _sessionToken = string.Empty;
        private          bool                              _disposed;

        private static readonly JsonSerializerOptions s_jsonOpts = new()
        {
            PropertyNameCaseInsensitive = true,
        };

        // ----------------------------------------------------------------
        // IProjectAdapter — identity
        // ----------------------------------------------------------------

        public string ProjectId      => _manifest.Project.Id;
        public string ProjectName    => _manifest.Project.DisplayName;
        public string ProjectVersion => _manifest.Project.Version;
        public string SessionToken   => _sessionToken;

        // ----------------------------------------------------------------
        // Legacy-specific properties
        // ----------------------------------------------------------------

        /// <summary>True when the manifest declares legacy-layout mode.</summary>
        public bool IsLegacyLayout => _manifest.LegacyLayout.Enabled;

        /// <summary>
        /// The legacy naming prefix used in the original codebase (e.g. "Arbiter").
        /// Used to translate old tool-action and service names to modern equivalents.
        /// </summary>
        public string LegacyNamingPrefix => _manifest.LegacyLayout.LegacyNamingPrefix;

        // ----------------------------------------------------------------
        // Construction
        // ----------------------------------------------------------------

        public MasterRepoLegacyAdapter(string repoRoot)
        {
            string path = MasterRepoLegacyManifest.ResolveManifestPath(repoRoot);
            _manifest = MasterRepoLegacyManifest.Load(path);

            _http = new HttpClient
            {
                BaseAddress = new Uri(
                    $"http://{_manifest.Bridge.Host}:{_manifest.Bridge.RestPort}/"),
                Timeout = TimeSpan.FromSeconds(_manifest.Bridge.TimeoutSeconds),
            };
        }

        // ----------------------------------------------------------------
        // Session
        // ----------------------------------------------------------------

        public async Task<BridgeResponse> ConnectSessionAsync(
            CancellationToken cancellationToken = default)
        {
            var payload = new
            {
                protocolVersion = "1.0",
                clientVersion   = ProjectVersion,
                projectId       = ProjectId,
            };

            var env = BuildEnvelope("SessionService", "Connect", payload: payload);
            return await PostAsync("/session/connect", env, cancellationToken)
                         .ConfigureAwait(false);
        }

        public async Task<BridgeResponse> DisconnectSessionAsync(
            CancellationToken cancellationToken = default)
        {
            if (string.IsNullOrEmpty(_sessionToken))
                return new BridgeResponse(false, "No active session.");

            var env = BuildEnvelope("SessionService", "Disconnect");
            var result = await PostAsync("/session/disconnect", env, cancellationToken)
                               .ConfigureAwait(false);
            if (result.Success) _sessionToken = string.Empty;
            return result;
        }

        // ----------------------------------------------------------------
        // Connectivity
        // ----------------------------------------------------------------

        public async Task<bool> IsBackendReachableAsync(
            CancellationToken cancellationToken = default)
        {
            try
            {
                using var resp = await _http
                    .GetAsync("/health", cancellationToken)
                    .ConfigureAwait(false);
                return resp.IsSuccessStatusCode;
            }
            catch
            {
                return false;
            }
        }

        // ----------------------------------------------------------------
        // Build
        // ----------------------------------------------------------------

        public IReadOnlyList<string> GetBuildTargetNames()
        {
            var names = new List<string>(_manifest.BuildTargets.Length);
            foreach (var t in _manifest.BuildTargets)
                names.Add(t.Name);
            return names;
        }

        public async Task<BridgeResponse> RequestBuildAsync(
            string            targetName,
            string            configuration    = "Debug",
            CancellationToken cancellationToken = default)
        {
            var payload = new { target = targetName, configuration, dryRun = true };
            var env     = BuildEnvelope("BuildService", "QueueBuild", payload: payload);
            return await PostAsync("/build/run", env, cancellationToken)
                         .ConfigureAwait(false);
        }

        // ----------------------------------------------------------------
        // Editor state
        // ----------------------------------------------------------------

        public async Task<BridgeResponse> GetEditorSelectionAsync(
            CancellationToken cancellationToken = default)
        {
            var env = BuildEnvelope("EditorService", "GetSelection");
            return await PostAsync("/editor/selection", env, cancellationToken)
                         .ConfigureAwait(false);
        }

        // ----------------------------------------------------------------
        // Tool actions
        // ----------------------------------------------------------------

        public IReadOnlyList<string> GetAllowedToolActions()
        {
            return _manifest.SafetySettings.AllowedToolActions;
        }

        public async Task<BridgeResponse> RunToolActionAsync(
            string            actionName,
            string?           parameter         = null,
            bool              dryRun            = true,
            CancellationToken cancellationToken  = default)
        {
            // Translate legacy Arbiter.* names to modern equivalents if needed
            string modernAction = TranslateLegacyActionName(actionName);

            var payload = new { action = modernAction, parameter, dryRun };
            var env     = BuildEnvelope("EditorService", "RunTool", payload: payload);
            return await PostAsync("/editor/tools/run", env, cancellationToken)
                         .ConfigureAwait(false);
        }

        // ----------------------------------------------------------------
        // Search roots (Epic 10 / Task 10.1)
        // ----------------------------------------------------------------

        public async Task<BridgeResponse> GetSearchRootsAsync(
            CancellationToken cancellationToken = default)
        {
            var env = BuildEnvelope("ProjectService", "GetSearchRoots");
            return await PostAsync("/project/search-roots", env, cancellationToken)
                         .ConfigureAwait(false);
        }

        // ----------------------------------------------------------------
        // Builder / PCG tool hooks (Epic 10 / Task 10.2)
        // ----------------------------------------------------------------

        public IReadOnlyList<string> GetAllowedBuilderToolActions() =>
            new[]
            {
                "ValidateData", "RunPCGPreview", "OpenScene",
                "FocusEntity",  "RegenerateSchemas",
            };

        public async Task<BridgeResponse> RunBuilderToolAsync(
            string            actionName,
            string?           sceneTarget       = null,
            string?           parameter         = null,
            bool              dryRun            = true,
            CancellationToken cancellationToken  = default)
        {
            string modernAction = TranslateLegacyActionName(actionName);
            var payload = new { action = modernAction, sceneTarget, parameter, dryRun };
            var env     = BuildEnvelope("EditorService", "RunBuilderTool", payload: payload);
            return await PostAsync("/editor/tools/builder", env, cancellationToken)
                         .ConfigureAwait(false);
        }

        // ----------------------------------------------------------------
        // Editor state snapshot (Epic 10 / Task 10.3)
        // ----------------------------------------------------------------

        public async Task<BridgeResponse> GetEditorStateAsync(
            CancellationToken cancellationToken = default)
        {
            var env = BuildEnvelope("EditorService", "GetEditorState");
            return await PostAsync("/editor/state", env, cancellationToken)
                         .ConfigureAwait(false);
        }

        // ----------------------------------------------------------------
        // Codegen proposal workflow (Epic 10 / Task 10.4)
        // ----------------------------------------------------------------

        public async Task<BridgeResponse> ProposeCodegenAsync(
            string            description,
            string            targetFile,
            string?           context           = null,
            CancellationToken cancellationToken  = default)
        {
            var payload = new { description, targetFile, context, dryRun = true };
            var env     = BuildEnvelope("CodegenService", "Propose", payload: payload);
            return await PostAsync("/codegen/propose", env, cancellationToken)
                         .ConfigureAwait(false);
        }

        public async Task<BridgeResponse> GetCodegenDiffAsync(
            string            proposalId,
            CancellationToken cancellationToken = default)
        {
            var payload = new { proposalId };
            var env     = BuildEnvelope("CodegenService", "GetDiff", payload: payload);
            return await PostAsync("/codegen/diff", env, cancellationToken)
                         .ConfigureAwait(false);
        }

        public async Task<BridgeResponse> ApproveCodegenAsync(
            string            proposalId,
            bool              approved,
            string?           comment           = null,
            CancellationToken cancellationToken  = default)
        {
            var payload = new { proposalId, approved, comment };
            var env     = BuildEnvelope("CodegenService", "Approve", payload: payload);
            return await PostAsync("/codegen/approve", env, cancellationToken)
                         .ConfigureAwait(false);
        }

        // ----------------------------------------------------------------
        // Disposal
        // ----------------------------------------------------------------

        public void Dispose()
        {
            if (_disposed) return;
            _disposed = true;
            _http.Dispose();
        }

        // ----------------------------------------------------------------
        // Private helpers
        // ----------------------------------------------------------------

        /// <summary>
        /// Translates a legacy action name (e.g. "Arbiter.ValidateData") to its
        /// modern equivalent ("ValidateData").  If no translation is needed the
        /// original name is returned unchanged.
        /// </summary>
        private string TranslateLegacyActionName(string name)
        {
            string prefix = LegacyNamingPrefix + ".";
            return name.StartsWith(prefix, StringComparison.OrdinalIgnoreCase)
                ? name[prefix.Length..]
                : name;
        }

        private object BuildEnvelope(
            string  service,
            string  operation,
            object? payload = null) =>
            new
            {
                protocolVersion = "1.0",
                requestId       = Guid.NewGuid().ToString(),
                sessionId       = _sessionToken,
                service,
                operation,
                timestampUtc    = DateTime.UtcNow.ToString("o"),
                payload,
            };

        private async Task<BridgeResponse> PostAsync(
            string            endpoint,
            object            envelope,
            CancellationToken ct)
        {
            try
            {
                string json    = JsonSerializer.Serialize(envelope, s_jsonOpts);
                var    content = new StringContent(json, Encoding.UTF8, "application/json");

                using var resp = await _http.PostAsync(endpoint, content, ct)
                                            .ConfigureAwait(false);
                string body = await resp.Content.ReadAsStringAsync(ct)
                                        .ConfigureAwait(false);

                if (resp.IsSuccessStatusCode)
                {
                    // Extract session token on connect
                    if (endpoint == "/session/connect" && !string.IsNullOrEmpty(body))
                    {
                        TryExtractSessionToken(body);
                    }
                    return new BridgeResponse(true, body);
                }
                return new BridgeResponse(false, body);
            }
            catch (Exception ex)
            {
                return new BridgeResponse(false, ex.Message);
            }
        }

        private void TryExtractSessionToken(string json)
        {
            try
            {
                using var doc = JsonDocument.Parse(json);
                if (doc.RootElement.TryGetProperty("sessionToken", out var tok))
                    _sessionToken = tok.GetString() ?? string.Empty;
            }
            catch { /* best-effort */ }
        }
    }
}
