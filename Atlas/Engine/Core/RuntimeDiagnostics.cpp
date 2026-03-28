// RuntimeDiagnostics.cpp
// Atlas Engine — runtime diagnostics implementation.

#include "RuntimeDiagnostics.h"
#include "GameSystemsRegistry.h"
#include <sstream>

namespace atlas
{

// ---------------------------------------------------------------------------
// DiagnosticsReport::Format
// ---------------------------------------------------------------------------

std::string DiagnosticsReport::Format() const
{
    static const char* kSevNames[] = { "INFO", "WARN", "ERROR", "CRITICAL" };
    std::ostringstream ss;
    ss << "=== RuntimeDiagnostics ===\n";
    for (const auto& e : entries)
    {
        ss << "[" << kSevNames[static_cast<int>(e.severity)] << "] "
           << "[" << e.category << "] "
           << e.message << "\n";
    }
    ss << "---\n";
    ss << "Errors: " << errorCount << "  Warnings: " << warningCount << "\n";
    ss << "Health: " << (IsHealthy() ? "OK" : "DEGRADED") << "\n";
    return ss.str();
}

// ---------------------------------------------------------------------------
// Run
// ---------------------------------------------------------------------------

DiagnosticsReport RuntimeDiagnostics::Run() const
{
    DiagnosticsReport report;
    CheckSystemRegistry(report);
    CheckDataRegistry(report);
    CheckRenderSystem(report);
    CheckSaveSystem(report);
    return report;
}

// ---------------------------------------------------------------------------
// Checks
// ---------------------------------------------------------------------------

void RuntimeDiagnostics::CheckSystemRegistry(DiagnosticsReport& report) const
{
    const auto& reg = GameSystemsRegistry::Get();

    if (reg.Count() == 0)
    {
        AddEntry(report, EDiagnosticSeverity::Warning, "Systems",
                 "No subsystems registered in GameSystemsRegistry");
        return;
    }

    auto failed = reg.GetFailed();
    if (!failed.empty())
    {
        for (const auto* f : failed)
        {
            AddEntry(report, EDiagnosticSeverity::Critical, "Systems",
                     "System failed: " + f->name +
                     (!f->errorMessage.empty() ? " (" + f->errorMessage + ")" : ""));
        }
    }

    auto pending = reg.GetByState(ESystemState::Pending);
    for (const auto* p : pending)
    {
        AddEntry(report, EDiagnosticSeverity::Warning, "Systems",
                 "System still pending: " + p->name);
    }

    if (reg.AllReady())
    {
        AddEntry(report, EDiagnosticSeverity::Info, "Systems",
                 "All " + std::to_string(reg.Count()) + " subsystems ready");
    }
}

void RuntimeDiagnostics::CheckDataRegistry(DiagnosticsReport& report) const
{
    // Lightweight presence check — deeper validation is owned by DataRegistry itself.
    AddEntry(report, EDiagnosticSeverity::Info, "Data",
             "Data registry check deferred to DataRegistry::Validate()");
}

void RuntimeDiagnostics::CheckRenderSystem(DiagnosticsReport& report) const
{
    AddEntry(report, EDiagnosticSeverity::Info, "Rendering",
             "Render system check deferred to Renderer::IsReady()");
}

void RuntimeDiagnostics::CheckSaveSystem(DiagnosticsReport& report) const
{
    AddEntry(report, EDiagnosticSeverity::Info, "Save",
             "Save system check deferred to SaveManager::IsReady()");
}

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

void RuntimeDiagnostics::AddEntry(DiagnosticsReport& report,
                                   EDiagnosticSeverity severity,
                                   const std::string& category,
                                   const std::string& message) const
{
    report.entries.push_back({ severity, category, message });
    if (severity == EDiagnosticSeverity::Error)
    {
        report.hasErrors = true;
        ++report.errorCount;
    }
    else if (severity == EDiagnosticSeverity::Critical)
    {
        report.hasCritical = true;
        ++report.errorCount;
    }
    else if (severity == EDiagnosticSeverity::Warning)
    {
        ++report.warningCount;
    }
}

} // namespace atlas
