// ArbiterWorkspace.cs
// Central workspace manager for Arbiter.
//
// Epic 6 / Task 6.5 — Standardize workspace loading
// Epic 10 / Task 10.5 — Workspace dashboard surface
//
// Responsibilities:
// - Locate the project manifest for a given repo root
// - Instantiate and activate the correct IProjectAdapter
// - Manage the connection lifecycle (connect / disconnect)
// - Expose the active adapter to the rest of Arbiter (shell, AI engine, etc.)
// - Surface the workspace dashboard and search roots for the shell UI
//
// Rules:
// - Generic: must not hard-code any project-specific logic.
// - Project adapters are activated by detecting the project manifest.
// - The workspace is the single source of truth for the active project.

using System;
using System.Collections.Generic;
using System.IO;
using System.Threading;
using System.Threading.Tasks;

using Arbiter.ProjectAdapters;
using Arbiter.ProjectAdapters.NovaForge;

namespace Arbiter.HostApp.Workspace
{
    /// <summary>
    /// Manages the active project workspace for Arbiter.
    /// Load a workspace by calling <see cref="LoadFromRepoRoot"/>.
    /// </summary>
    public sealed class ArbiterWorkspace : IDisposable
    {
        private IProjectAdapter? _adapter;
        private bool             _disposed;

        // ----------------------------------------------------------------
        // Factory
        // ----------------------------------------------------------------

        /// <summary>
        /// Loads a workspace from a repo root directory.
        /// Auto-detects the project type from the manifest present in the repo.
        /// </summary>
        public static ArbiterWorkspace LoadFromRepoRoot(string repoRoot)
        {
            if (string.IsNullOrWhiteSpace(repoRoot))
                throw new ArgumentException(
                    "repoRoot must not be null or empty.", nameof(repoRoot));

            var workspace = new ArbiterWorkspace();
            workspace._adapter = workspace.CreateAdapter(repoRoot);
            return workspace;
        }

        // ----------------------------------------------------------------
        // Active adapter
        // ----------------------------------------------------------------

        /// <summary>The active project adapter, or null if no project is loaded.</summary>
        public IProjectAdapter? ActiveAdapter => _adapter;

        /// <summary>Returns true when a project has been loaded.</summary>
        public bool HasActiveProject => _adapter != null;

        /// <summary>The active project name, or null when no project is loaded.</summary>
        public string? ProjectName => _adapter?.ProjectName;

        /// <summary>The active project ID, or null when no project is loaded.</summary>
        public string? ProjectId => _adapter?.ProjectId;

        // ----------------------------------------------------------------
        // Connection lifecycle
        // ----------------------------------------------------------------

        /// <summary>
        /// Connects the active adapter to the backend bridge service.
        /// Must be called after <see cref="LoadFromRepoRoot"/>.
        /// </summary>
        public async Task<BridgeResponse> ConnectAsync(
            CancellationToken cancellationToken = default)
        {
            if (_adapter == null)
                return new BridgeResponse(false, "No project adapter loaded.");

            return await _adapter.ConnectSessionAsync(cancellationToken);
        }

        /// <summary>
        /// Disconnects the active adapter from the backend bridge service.
        /// </summary>
        public async Task DisconnectAsync(
            CancellationToken cancellationToken = default)
        {
            if (_adapter != null)
                await _adapter.DisconnectSessionAsync(cancellationToken);
        }

        // ----------------------------------------------------------------
        // Epic 10 / Task 10.1 — Search roots
        // ----------------------------------------------------------------

        /// <summary>
        /// Returns the full set of searchable project roots from the backend.
        /// Requires an active session.
        /// </summary>
        public async Task<BridgeResponse> GetSearchRootsAsync(
            CancellationToken cancellationToken = default)
        {
            if (_adapter == null)
                return new BridgeResponse(false, "No project adapter loaded.");

            return await _adapter.GetSearchRootsAsync(cancellationToken);
        }

        // ----------------------------------------------------------------
        // Epic 10 / Task 10.5 — Workspace dashboard
        // ----------------------------------------------------------------

        /// <summary>
        /// Returns an aggregated workspace dashboard snapshot from the bridge backend.
        /// Includes build health, recent actions, search roots, and project status.
        /// Requires an active session.
        /// </summary>
        public async Task<BridgeResponse> GetDashboardAsync(
            CancellationToken cancellationToken = default)
        {
            if (_adapter == null)
                return new BridgeResponse(false, "No project adapter loaded.");

            // The dashboard is served by the backend bridge service.
            // The adapter routes to GET /workspace/dashboard via a GET request.
            // Use a helper on the NovaForge adapter if available, otherwise fall back.
            if (_adapter is NovaForgeProjectAdapter nfAdapter)
                return await nfAdapter.GetWorkspaceDashboardAsync(cancellationToken);

            // Generic fallback: not supported for unknown adapters
            return new BridgeResponse(false, "Dashboard not supported by this adapter.");
        }

        // ----------------------------------------------------------------
        // Adapter creation (project detection)
        // ----------------------------------------------------------------

        /// <summary>
        /// Detects the project type from the repo root and creates the
        /// appropriate adapter. Currently only NovaForge is supported;
        /// future projects would be detected and dispatched here.
        /// </summary>
        private IProjectAdapter CreateAdapter(string repoRoot)
        {
            // Check for NovaForge manifest
            string novaForgeManifest =
                NovaForgeProjectManifest.ResolveManifestPath(repoRoot);

            if (File.Exists(novaForgeManifest))
                return new NovaForgeProjectAdapter(repoRoot);

            throw new InvalidOperationException(
                $"No recognised project manifest found under: {repoRoot}");
        }

        // ----------------------------------------------------------------
        // IDisposable
        // ----------------------------------------------------------------

        public void Dispose()
        {
            if (!_disposed)
            {
                _adapter?.Dispose();
                _adapter  = null;
                _disposed = true;
            }
        }
    }
}
