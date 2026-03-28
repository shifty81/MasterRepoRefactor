// RuntimeDiagnostics.h
// Atlas Engine — runtime health checks and diagnostics reporter.
//
// RuntimeDiagnostics aggregates information from GameSystemsRegistry and other
// subsystems to produce a structured health snapshot usable by:
//   - PlaytestSession (automated exit-code decisions)
//   - TestHarness (CI pass/fail gate)
//   - The editor "Diagnostics" panel
//   - Log output at startup

#pragma once
#include <string>
#include <vector>
#include <cstdint>

namespace atlas
{

/// Severity of a diagnostic entry.
enum class EDiagnosticSeverity : uint8_t
{
    Info,
    Warning,
    Error,
    Critical,
};

/// A single diagnostic finding.
struct DiagnosticEntry
{
    EDiagnosticSeverity severity  = EDiagnosticSeverity::Info;
    std::string         category;   ///< e.g. "Systems", "Data", "Rendering"
    std::string         message;
};

/// Result of a full diagnostics run.
struct DiagnosticsReport
{
    std::vector<DiagnosticEntry> entries;
    bool                         hasErrors   = false;
    bool                         hasCritical = false;
    uint32_t                     errorCount  = 0;
    uint32_t                     warningCount = 0;

    /// True only when no errors or critical findings are present.
    bool IsHealthy() const { return !hasErrors && !hasCritical; }

    /// Multi-line human-readable summary.
    std::string Format() const;
};

/// Runs diagnostics across engine subsystems and produces a DiagnosticsReport.
class RuntimeDiagnostics
{
public:
    RuntimeDiagnostics() = default;

    /// Run all diagnostic checks and return a filled report.
    DiagnosticsReport Run() const;

    // ------------------------------------------------------------------ //
    // Individual checks (also callable independently)
    // ------------------------------------------------------------------ //

    /// Check that all registered systems are in Ready state.
    void CheckSystemRegistry(DiagnosticsReport& report) const;

    /// Check that the data registry has loaded at least one record type.
    void CheckDataRegistry(DiagnosticsReport& report) const;

    /// Check that the render system is initialised and a viewport exists.
    void CheckRenderSystem(DiagnosticsReport& report) const;

    /// Check that the save system is reachable and not in an error state.
    void CheckSaveSystem(DiagnosticsReport& report) const;

private:
    void AddEntry(DiagnosticsReport& report,
                  EDiagnosticSeverity severity,
                  const std::string& category,
                  const std::string& message) const;
};

} // namespace atlas
