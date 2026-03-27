// ArbiterBridgeTypes.h
// Shared bridge contract types between Arbiter AI tooling and NovaForge/Atlas backend.
//
// Rules:
// - This file must have no dependency on WPF, gameplay, or engine internals.
// - All cross-boundary types must be plain data structures.
// - Use only standard C++ types or forward declarations.

#pragma once

#include <cstdint>
#include <string>
#include <vector>

namespace Arbiter::Bridge
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

/// Sent by Arbiter to establish a bridge session.
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
    std::string  sessionToken;   // opaque token for subsequent requests
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

} // namespace Arbiter::Bridge
