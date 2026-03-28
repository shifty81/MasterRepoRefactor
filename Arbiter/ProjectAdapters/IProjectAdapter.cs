// IProjectAdapter.cs
// Generic project adapter interface for Arbiter.
//
// Epic 6 / Task 6.1 — Split generic modules from project-specific ones
// Epic 6 / Task 6.2 — Project-specific code goes in Arbiter/ProjectAdapters/<ProjectName>/
//
// Any project adapter (NovaForge, future projects) must implement this interface.
// Arbiter's workspace and AI engine only use this interface — never the concrete type.

using System;
using System.Collections.Generic;
using System.Threading;
using System.Threading.Tasks;

namespace Arbiter.ProjectAdapters
{
    /// <summary>
    /// Generic contract that every project adapter must satisfy.
    /// The concrete implementation lives under Arbiter/ProjectAdapters/&lt;ProjectName&gt;/.
    /// </summary>
    public interface IProjectAdapter : IDisposable
    {
        // ----------------------------------------------------------------
        // Identity
        // ----------------------------------------------------------------

        /// <summary>Machine-readable project identifier (e.g. "novaforge").</summary>
        string ProjectId { get; }

        /// <summary>Human-readable project name (e.g. "NovaForge").</summary>
        string ProjectName { get; }

        /// <summary>Project version string (semver, e.g. "0.1.0").</summary>
        string ProjectVersion { get; }

        // ----------------------------------------------------------------
        // Session
        // ----------------------------------------------------------------

        /// <summary>
        /// The current session token, or empty string if not connected.
        /// </summary>
        string SessionToken { get; }

        /// <summary>Establishes a bridge session with the backend.</summary>
        Task<BridgeResponse> ConnectSessionAsync(
            CancellationToken cancellationToken = default);

        /// <summary>Disconnects the current bridge session.</summary>
        Task<BridgeResponse> DisconnectSessionAsync(
            CancellationToken cancellationToken = default);

        // ----------------------------------------------------------------
        // Connectivity
        // ----------------------------------------------------------------

        /// <summary>Returns true when the backend bridge service is reachable.</summary>
        Task<bool> IsBackendReachableAsync(
            CancellationToken cancellationToken = default);

        // ----------------------------------------------------------------
        // Build
        // ----------------------------------------------------------------

        /// <summary>Returns all build targets declared in the project manifest.</summary>
        IReadOnlyList<string> GetBuildTargetNames();

        /// <summary>Requests a build of the named target.</summary>
        Task<BridgeResponse> RequestBuildAsync(
            string            targetName,
            string            configuration    = "Debug",
            CancellationToken cancellationToken = default);

        // ----------------------------------------------------------------
        // Editor state
        // ----------------------------------------------------------------

        /// <summary>Returns the current editor selection snapshot.</summary>
        Task<BridgeResponse> GetEditorSelectionAsync(
            CancellationToken cancellationToken = default);

        // ----------------------------------------------------------------
        // Tool actions
        // ----------------------------------------------------------------

        /// <summary>Returns the list of allowed tool action names.</summary>
        IReadOnlyList<string> GetAllowedToolActions();

        /// <summary>
        /// Runs a whitelisted tool action.
        /// Defaults to dry-run for safety.
        /// </summary>
        Task<BridgeResponse> RunToolActionAsync(
            string            actionName,
            string?           parameter         = null,
            bool              dryRun            = true,
            CancellationToken cancellationToken  = default);

        // ----------------------------------------------------------------
        // Epic 10 / Task 10.1 — Search roots
        // ----------------------------------------------------------------

        /// <summary>Returns the full set of searchable project roots.</summary>
        Task<BridgeResponse> GetSearchRootsAsync(
            CancellationToken cancellationToken = default);

        // ----------------------------------------------------------------
        // Epic 10 / Task 10.2 — Builder / PCG tool hooks
        // ----------------------------------------------------------------

        /// <summary>Returns the names of allowed builder tool actions.</summary>
        IReadOnlyList<string> GetAllowedBuilderToolActions();

        /// <summary>
        /// Runs a whitelisted builder or PCG tool hook.
        /// Defaults to dry-run for safety.
        /// </summary>
        Task<BridgeResponse> RunBuilderToolAsync(
            string            actionName,
            string?           sceneTarget       = null,
            string?           parameter         = null,
            bool              dryRun            = true,
            CancellationToken cancellationToken  = default);

        // ----------------------------------------------------------------
        // Epic 10 / Task 10.3 — Richer editor state
        // ----------------------------------------------------------------

        /// <summary>
        /// Returns the full editor state snapshot including active map,
        /// mode, world state, selected components, and simulation state.
        /// </summary>
        Task<BridgeResponse> GetEditorStateAsync(
            CancellationToken cancellationToken = default);

        // ----------------------------------------------------------------
        // Epic 10 / Task 10.4 — Codegen proposal workflow
        // ----------------------------------------------------------------

        /// <summary>
        /// Proposes a code-generation change.
        /// Always creates a proposal + diff for human review; never writes directly.
        /// </summary>
        Task<BridgeResponse> ProposeCodegenAsync(
            string            description,
            string            targetFile,
            string?           context           = null,
            CancellationToken cancellationToken  = default);

        /// <summary>Gets the diff preview for a pending codegen proposal.</summary>
        Task<BridgeResponse> GetCodegenDiffAsync(
            string            proposalId,
            CancellationToken cancellationToken = default);

        /// <summary>
        /// Approves or rejects a pending proposal.
        /// Approval requires a write-authorized session.
        /// </summary>
        Task<BridgeResponse> ApproveCodegenAsync(
            string            proposalId,
            bool              approved,
            string?           comment           = null,
            CancellationToken cancellationToken  = default);
    }

    /// <summary>Simple success/body pair returned by all bridge calls.</summary>
    public sealed record BridgeResponse(bool Success, string Body);

    // ----------------------------------------------------------------
    // Epic 10 shared response types
    // ----------------------------------------------------------------

    /// <summary>One searchable root directory surfaced to Arbiter.</summary>
    public sealed record SearchRoot(
        string Label, // e.g. "Docs", "DataTables"
        string Path,  // relative to repoRoot
        string Kind   // "docs" | "config" | "data" | "content" | "source"
    );
}
