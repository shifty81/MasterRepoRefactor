// NovaForgeProjectAdapter.cs
// Arbiter project adapter for NovaForge.
//
// This adapter:
// - loads the NovaForge project manifest
// - connects to the NovaForge Arbiter bridge service via /session/connect
// - exposes project info, build targets, and whitelisted tool actions to Arbiter
// - wraps all requests in the standard BridgeRequestEnvelope
//
// Epic 6 / Task 6.2 — project-specific adapter implements IProjectAdapter
//
// Rules:
// - must not directly access gameplay runtime internals
// - must not contain WPF or UI code
// - all operations go through the bridge protocol defined in Shared/ToolProtocol

using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Http;
using System.Text;
using System.Text.Json;
using System.Threading;
using System.Threading.Tasks;

// Pull in IProjectAdapter and BridgeResponse from the parent namespace
using Arbiter.ProjectAdapters;

namespace Arbiter.ProjectAdapters.NovaForge
{
    public sealed class NovaForgeProjectAdapter : IProjectAdapter
    {
        private readonly NovaForgeProjectManifest _manifest;
        private readonly HttpClient               _http;
        private string                            _sessionToken = string.Empty;
        private bool                              _disposed;

        private static readonly JsonSerializerOptions s_jsonOptions = new()
        {
            PropertyNameCaseInsensitive = true,
        };

        public string ProjectId      => _manifest.Project.Id;
        public string ProjectName    => _manifest.Project.DisplayName;
        public string ProjectVersion => _manifest.Project.Version;

        /// <summary>Returns the current session token, or empty if not connected.</summary>
        public string SessionToken => _sessionToken;

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
        // Project info (local — from manifest, no network call)
        // ----------------------------------------------------------------

        /// <summary>Returns cached project info from the manifest.</summary>
        public ProjectInfoModel GetProjectInfo() => _manifest.Project;

        /// <summary>Returns capability flags from the manifest.</summary>
        public ProjectCapabilitiesModel GetCapabilities() => _manifest.Capabilities;

        /// <summary>Returns all configured build targets.</summary>
        public IReadOnlyList<BuildTargetModel> GetBuildTargets() =>
            _manifest.BuildTargets;

        /// <summary>
        /// IProjectAdapter: returns build target names for generic consumers.
        /// </summary>
        public IReadOnlyList<string> GetBuildTargetNames() =>
            _manifest.BuildTargets.Select(t => t.Name).ToList();

        /// <summary>Returns all allowed tool actions from safety settings.</summary>
        public IReadOnlyList<string> GetAllowedToolActions() =>
            _manifest.SafetySettings.AllowedToolActions;

        // ----------------------------------------------------------------
        // Session management  (Task 4.1 prerequisite — /session/connect)
        // ----------------------------------------------------------------

        /// <summary>
        /// Establishes a bridge session with the NovaForge backend.
        /// The session token is stored and used for all subsequent requests.
        /// </summary>
        public async Task<BridgeResponse> ConnectSessionAsync(
            CancellationToken cancellationToken = default)
        {
            var payload = new SessionConnectPayload
            {
                ProjectId = _manifest.Project.Id,
            };

            var envelope = BridgeRequestEnvelope.Create(
                service:   "SessionService",
                operation: "Connect",
                payload:   payload);

            var response = await PostEnvelopeAsync(
                "session/connect", envelope, cancellationToken);

            if (response.Success)
            {
                // Extract the session token from the response payload
                try
                {
                    var parsed = JsonSerializer.Deserialize<BridgeResponseEnvelope>(
                        response.Body, s_jsonOptions);

                    if (parsed?.Payload.HasValue == true)
                    {
                        var connect = JsonSerializer.Deserialize<SessionConnectResponse>(
                            parsed.Payload.Value.GetRawText(), s_jsonOptions);
                        if (connect != null)
                            _sessionToken = connect.SessionToken;
                    }

                    if (string.IsNullOrEmpty(_sessionToken))
                    {
                        // Server responded 200 but payload had no token — treat as failure
                        return new BridgeResponse(false,
                            "Session connect succeeded but no session token was returned.");
                    }
                }
                catch (JsonException ex)
                {
                    // Deserialization failed — surface the error to the caller
                    return new BridgeResponse(false,
                        $"Session connect succeeded but token extraction failed: {ex.Message}");
                }
            }

            return response;
        }

        /// <summary>Disconnects the current bridge session.</summary>
        public async Task<BridgeResponse> DisconnectSessionAsync(
            CancellationToken cancellationToken = default)
        {
            var response = await PostEnvelopeAsync(
                "session/disconnect",
                BuildEnvelope("SessionService", "Disconnect", null),
                cancellationToken);

            _sessionToken = string.Empty;
            return response;
        }

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
        // Build  POST /build/run  (Task 4.3)
        // ----------------------------------------------------------------

        /// <summary>
        /// Requests a build via the bridge service.
        /// Requires an active session (call ConnectSessionAsync first).
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

            return await PostEnvelopeAsync(
                "build/run",
                BuildEnvelope("BuildService", "RunBuild", payload),
                cancellationToken);
        }

        // ----------------------------------------------------------------
        // Editor state  GET /editor/selection  (Task 4.2)
        // ----------------------------------------------------------------

        /// <summary>
        /// Queries the current editor selection snapshot.
        /// Requires an active session.
        /// </summary>
        public async Task<BridgeResponse> GetEditorSelectionAsync(
            CancellationToken cancellationToken = default)
        {
            try
            {
                var request = new HttpRequestMessage(
                    HttpMethod.Get, "editor/selection");
                AddSessionHeader(request);

                var response = await _http.SendAsync(request, cancellationToken);
                string content = await response.Content.ReadAsStringAsync(cancellationToken);
                return new BridgeResponse(response.IsSuccessStatusCode, content);
            }
            catch (Exception ex)
            {
                return new BridgeResponse(false, ex.Message);
            }
        }

        // ----------------------------------------------------------------
        // Tool actions  POST /editor/tools/run  (Task 4.4)
        // ----------------------------------------------------------------

        /// <summary>
        /// Runs a whitelisted tool action.
        /// Defaults to dry-run for safety. Requires an active session.
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

            return await PostEnvelopeAsync(
                "editor/tools/run",
                BuildEnvelope("ToolService", "RunToolAction", payload),
                cancellationToken);
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

        private BridgeRequestEnvelope BuildEnvelope(
            string  service,
            string  operation,
            object? payload) =>
            BridgeRequestEnvelope.Create(
                service:   service,
                operation: operation,
                sessionId: _sessionToken,
                payload:   payload);

        private void AddSessionHeader(HttpRequestMessage request)
        {
            if (!string.IsNullOrEmpty(_sessionToken))
                request.Headers.TryAddWithoutValidation(
                    "X-Bridge-Session", _sessionToken);
        }

        private async Task<BridgeResponse> PostEnvelopeAsync(
            string                  endpoint,
            BridgeRequestEnvelope   envelope,
            CancellationToken       cancellationToken)
        {
            try
            {
                string json    = JsonSerializer.Serialize(envelope);
                var    content = new StringContent(json, Encoding.UTF8, "application/json");

                var httpRequest = new HttpRequestMessage(HttpMethod.Post, endpoint)
                {
                    Content = content,
                };
                AddSessionHeader(httpRequest);

                var    response = await _http.SendAsync(httpRequest, cancellationToken);
                string body     = await response.Content.ReadAsStringAsync(cancellationToken);
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

}
