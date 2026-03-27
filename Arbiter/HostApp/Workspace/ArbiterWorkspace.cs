// ArbiterWorkspace.cs
// Central workspace manager for Arbiter.
//
// Epic 6 / Task 6.5 — Standardize workspace loading
//
// Responsibilities:
// - Locate the project manifest for a given repo root
// - Instantiate and activate the correct IProjectAdapter
// - Manage the connection lifecycle (connect / disconnect)
// - Expose the active adapter to the rest of Arbiter (shell, AI engine, etc.)
//
// Rules:
// - Generic: must not hard-code any project-specific logic.
// - Project adapters are activated by detecting the project manifest.
// - The workspace is the single source of truth for the active project.

using System;
using System.IO;
using System.Threading;
using System.Threading.Tasks;

using Arbiter.ProjectAdapters;
using Arbiter.ProjectAdapters.NovaForge;

namespace Arbiter.HostApp.Workspace
{
    /// <summary>
    /// Manages the active project workspace for Arbiter.
    /// Load a workspace by calling <see cref="LoadFromRepoRootAsync"/>.
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
