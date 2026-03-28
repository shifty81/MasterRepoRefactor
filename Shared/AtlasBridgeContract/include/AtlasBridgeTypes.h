// AtlasBridgeTypes.h
// Shared bridge contract types between AtlasAI tooling and NovaForge/Atlas backend.
//
// Rules:
// - This file must have no dependency on WPF, gameplay, or engine internals.
// - All cross-boundary types must be plain data structures.
// - Use only standard C++ types or forward declarations.

#pragma once

#include <cstdint>
#include <string>
#include <vector>

namespace Atlas::Bridge
{

// ============================================================
// Protocol constants
// ============================================================

constexpr const char* kProtocolVersion = "1.0";
constexpr uint16_t    kDefaultRestPort = 57100;
constexpr uint16_t    kDefaultWsPort   = 57101;

// ============================================================
// Protocol versioning
// ============================================================

struct ProtocolVersion
{
    uint32_t major = 1;
    uint32_t minor = 0;
    uint32_t patch = 0;
};

// ============================================================
// Common result types
// ============================================================

enum class BridgeErrorCode : uint32_t
{
    Success           = 0,
    UnknownError      = 1,
    InvalidRequest    = 2,
    Unauthorized      = 3,
    UnsupportedOp     = 4,
    Timeout           = 5,
    ResourceBusy      = 6,
    InvalidState      = 7,
    NotFound          = 8,
    ValidationFailed  = 9,
    BackendUnavailable = 10,
    VersionMismatch   = 11,
    OperationCancelled = 12,
};

struct BridgeResult
{
    BridgeErrorCode errorCode = BridgeErrorCode::Success;
    std::string     message;

    bool succeeded() const { return errorCode == BridgeErrorCode::Success; }
};

// ============================================================
// Project info
// ============================================================

struct ProjectCapabilities
{
    bool supportsViewportAttach    = false;
    bool supportsLivePatch         = false;
    bool supportsAISession         = false;
    bool supportsProjectIndexing   = true;
    bool supportsMultiWorkspace    = false;
};

struct ProjectInfo
{
    std::string          projectId;
    std::string          displayName;
    std::string          version;
    std::string          repoRoot;
    ProjectCapabilities  capabilities;
};

// ============================================================
// Build types
// ============================================================

enum class BuildConfiguration : uint32_t
{
    Debug   = 0,
    Release = 1,
    Shipping = 2,
};

enum class BuildPlatform : uint32_t
{
    Win64  = 0,
    Linux  = 1,
    macOS  = 2,
};

struct BuildTarget
{
    std::string        name;          // e.g. "AtlasEditor", "NovaForgeClient"
    BuildConfiguration configuration = BuildConfiguration::Debug;
    BuildPlatform      platform      = BuildPlatform::Win64;
    bool               rebuild       = false;
};

struct BuildResult
{
    BridgeResult result;
    std::string  buildId;
    int          exitCode = -1;
    std::string  outputLog;
};

// ============================================================
// Editor selection snapshot
// ============================================================

struct EditorSelectionSnapshot
{
    std::string activeScene;
    std::string selectedObjectName;
    std::string selectedObjectType;
    uint64_t    selectedObjectId = 0;
};

// ============================================================
// Open file request
// ============================================================

struct OpenFileRequest
{
    std::string filePath;
    int         lineNumber  = -1;
    int         columnNumber = -1;
};

// ============================================================
// Tool action (whitelisted)
// ============================================================

enum class ToolActionId : uint32_t
{
    ValidateData      = 0,
    RunPCGPreview     = 1,
    OpenScene         = 2,
    FocusEntity       = 3,
    RegenerateSchemas = 4,
};

struct ToolActionRequest
{
    ToolActionId        actionId;
    std::string         parameter;   // optional action-specific parameter
    bool                dryRun = true;  // always default to dry-run for safety
};

struct ToolActionResult
{
    BridgeResult result;
    bool         wasDryRun = true;
    std::string  summary;
};

// ============================================================
// Request / response envelopes (mirrors ToolProtocol JSON spec)
// ============================================================

/// Standard envelope for all bridge requests.
struct BridgeRequestEnvelope
{
    std::string protocolVersion = kProtocolVersion;
    std::string requestId;       // UUID string, set by caller
    std::string sessionId;       // UUID string, obtained from SessionConnect
    std::string service;         // e.g. "ProjectService"
    std::string operation;       // e.g. "GetProjectInfo"
    std::string timestampUtc;    // ISO 8601 UTC timestamp
};

/// Standard envelope for all bridge responses.
struct BridgeResponseEnvelope
{
    std::string  protocolVersion = kProtocolVersion;
    std::string  requestId;      // echoed from request
    bool         success         = true;
    std::string  errorCode;      // UPPER_SNAKE_CASE, empty on success
    std::string  message;        // human-readable status
};

/// Standard envelope for WebSocket event streams.
struct BridgeEventEnvelope
{
    std::string protocolVersion = kProtocolVersion;
    std::string eventId;         // UUID string
    std::string sessionId;
    std::string service;
    std::string eventType;       // e.g. "BuildProgress"
    std::string timestampUtc;
};

// ============================================================
// Session types
// ============================================================

/// Sent by AtlasAI to establish a bridge session.
struct SessionConnectRequest
{
    std::string protocolVersion = kProtocolVersion;
    std::string clientVersion;
    std::string projectId;
};

/// Returned by the backend on a successful session handshake.
struct SessionConnectResponse
{
    BridgeResult result;
    std::string  sessionToken;   // opaque token — obtained from SessionService Connect response
    std::string  serverVersion;
    std::string  projectId;
    bool         writeEnabled = false; // true when session allows mutating ops
};

// ============================================================
// Audit log
// ============================================================

/// A single structured entry written to the audit log.
struct AuditLogEntry
{
    std::string timestampUtc;
    std::string requestId;
    std::string sessionId;
    std::string service;
    std::string operation;
    bool        success    = true;
    bool        wasDryRun  = false;
    std::string summary;
    std::string failReason; // populated on failure
};

// ============================================================
// Epic 10 / Task 10.1 — Search roots
// ============================================================

/// One searchable root exposed to AtlasAI for indexing and navigation.
struct SearchRoot
{
    std::string label; // e.g. "Docs", "DataTables", "SourceAtlas"
    std::string path;  // relative to repoRoot
    std::string kind;  // "docs" | "config" | "data" | "content" | "source"
};

/// Complete set of project search roots returned by GET /project/search-roots.
struct ProjectSearchRoots
{
    BridgeResult              result;
    std::vector<SearchRoot>   roots;
};

// ============================================================
// Epic 10 / Task 10.2 — Builder and PCG tool hooks
// ============================================================

/// Extended set of whitelisted builder / PCG tool actions.
/// Values 0-4 are the original ToolActionId values kept for backward compat.
enum class BuilderToolActionId : uint32_t
{
    // Original tool actions (mirrors ToolActionId)
    ValidateData       = 0,
    RunPCGPreview      = 1,
    OpenScene          = 2,
    FocusEntity        = 3,
    RegenerateSchemas  = 4,

    // Builder / PCG second-wave actions (Epic 10 / Task 10.2)
    RunBuilderInspect  = 5,  // inspect the current builder state
    RunPCGDiagnostics  = 6,  // run PCG diagnostic pass without committing
    GeneratePCGPreview = 7,  // generate a preview mesh / layout
    ValidateBuilderData = 8, // validate builder entity / config data
};

struct BuilderToolRequest
{
    BuilderToolActionId actionId = BuilderToolActionId::ValidateData;
    std::string         sceneTarget; // optional scene/entity to target
    std::string         parameter;   // action-specific parameter string
    bool                dryRun = true;
};

struct BuilderToolResult
{
    BridgeResult result;
    bool         wasDryRun = true;
    std::string  summary;
    std::string  diagnosticsLog; // populated for diagnostic actions
};

// ============================================================
// Epic 10 / Task 10.3 — Richer editor state snapshot
// ============================================================

enum class SimulationState : uint32_t
{
    Stopped = 0,
    Playing = 1,
    Paused  = 2,
};

struct SelectedComponent
{
    std::string componentType; // e.g. "MeshRenderer", "RigidBody"
    std::string componentId;   // engine-assigned ID string
};

/// Full editor state snapshot returned by GET /editor/state.
/// Extends EditorSelectionSnapshot with map, mode, world, and simulation.
struct EditorStateSnapshot
{
    BridgeResult                   result;

    // Scene / world context
    std::string                    activeScene;
    std::string                    activeMap;
    std::string                    loadedWorldId;

    // Editor mode  (e.g. "Build", "Play", "Inspect", "Simulate")
    std::string                    activeMode;

    // Simulation
    SimulationState                simulationState = SimulationState::Stopped;

    // Selected object
    std::string                    selectedObjectName;
    std::string                    selectedObjectType;
    uint64_t                       selectedObjectId = 0;

    // Selected components on the selected object
    std::vector<SelectedComponent> selectedComponents;
};

// ============================================================
// Epic 10 / Task 10.4 — Codegen proposal workflow
// ============================================================

/// Initial request to propose a code-generation change.
/// Always produces a proposal + diff for human review before applying.
struct CodegenProposalRequest
{
    std::string description; // what to generate / change (natural-language)
    std::string targetFile;  // repo-relative path to the file to touch
    std::string context;     // optional extra context for the AI
    bool        dryRun = true;
};

/// Returned after a proposal is created.
struct CodegenProposal
{
    BridgeResult result;
    std::string  proposalId;  // UUID identifying this proposal
    std::string  description; // echoed from the request
    std::string  targetFile;  // file that will be modified/created
    std::string  summary;     // one-line human-readable description of the change
};

/// Unified-diff preview of what the proposal would apply.
struct CodegenDiff
{
    BridgeResult result;
    std::string  proposalId;
    std::string  diffText;     // unified diff format (--- a/ +++ b/)
    int          linesAdded   = 0;
    int          linesRemoved = 0;
};

/// Approval or rejection of a pending proposal.
struct CodegenApprovalRequest
{
    std::string proposalId;
    bool        approved = false;
    std::string comment;       // optional human comment
};

/// Result after a proposal has been applied (or rejected).
struct CodegenApplyResult
{
    BridgeResult result;
    std::string  proposalId;
    std::string  appliedFile;  // file that was modified, empty on rejection
    bool         wasApplied = false;
};

// ============================================================
// Epic 10 / Task 10.5 — Workspace dashboard
// ============================================================

struct BuildHealthSummary
{
    std::string lastBuildTarget;
    std::string lastBuildId;
    bool        lastBuildSucceeded = false;
    std::string lastBuildTimestampUtc;
};

/// Aggregated project status snapshot for the workspace dashboard.
struct WorkspaceDashboard
{
    BridgeResult       result;

    // Identity
    std::string        projectId;
    std::string        projectName;
    std::string        projectVersion;

    // Build health
    BuildHealthSummary buildHealth;

    // Search roots (docs, data, config, content, source)
    ProjectSearchRoots searchRoots;

    // Recent activity
    std::string        lastToolAction;       // name of most-recent tool action
    std::string        lastToolTimestampUtc;

    // Overall status
    std::string        currentProjectStatus; // "idle" | "building" | "error"
    size_t             activeSessionCount = 0;
};

} // namespace Atlas::Bridge
