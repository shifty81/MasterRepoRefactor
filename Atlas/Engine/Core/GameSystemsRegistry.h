// GameSystemsRegistry.h
// Atlas Engine — registry that tracks every game subsystem and its initialisation status.
//
// All subsystems register themselves here at startup so that:
//   1. The boot sequence can verify nothing was skipped.
//   2. RuntimeDiagnostics can produce a health report.
//   3. PlaytestSession / TestHarness can assert full readiness.

#pragma once
#include <string>
#include <vector>
#include <functional>
#include <cstdint>

namespace atlas
{

/// Lifecycle state of a registered subsystem.
enum class ESystemState : uint8_t
{
    Pending,        ///< Registered but not yet initialised
    Initialising,   ///< Initialisation in progress
    Ready,          ///< Fully initialised and operational
    Failed,         ///< Initialisation failed
    ShuttingDown,   ///< Shutdown in progress
    Shutdown,       ///< Cleanly shut down
};

/// A snapshot of one registered subsystem.
struct SystemEntry
{
    std::string name;
    std::string category;       ///< e.g. "Engine", "Gameplay", "Editor", "AI"
    ESystemState state  = ESystemState::Pending;
    std::string  errorMessage;  ///< Populated when state == Failed
};

/// Global registry of all game/engine/editor subsystems.
///
/// Thread-safety: this class is not thread-safe; all registrations and state
/// transitions must occur on the main thread.
class GameSystemsRegistry
{
public:
    static GameSystemsRegistry& Get();

    // ------------------------------------------------------------------ //
    // Registration
    // ------------------------------------------------------------------ //

    /// Register a new subsystem.  Returns false if a subsystem with the same
    /// name is already registered.
    bool Register(const std::string& name, const std::string& category = "Engine");

    // ------------------------------------------------------------------ //
    // State transitions
    // ------------------------------------------------------------------ //

    bool SetState(const std::string& name, ESystemState state,
                  const std::string& errorMessage = {});

    bool MarkReady(const std::string& name);
    bool MarkFailed(const std::string& name, const std::string& reason);

    // ------------------------------------------------------------------ //
    // Queries
    // ------------------------------------------------------------------ //

    /// True if every registered subsystem is in Ready state.
    bool AllReady() const;

    /// Returns all subsystems that are in Failed state.
    std::vector<const SystemEntry*> GetFailed() const;

    /// Returns all subsystems in a given state.
    std::vector<const SystemEntry*> GetByState(ESystemState state) const;

    /// Returns all registered subsystems.
    const std::vector<SystemEntry>& All() const { return m_systems; }

    /// Look up a subsystem by name (returns nullptr if not found).
    const SystemEntry* Find(const std::string& name) const;

    /// Total count of registered subsystems.
    size_t Count() const { return m_systems.size(); }

    /// Count subsystems in a given state.
    size_t CountByState(ESystemState state) const;

    // ------------------------------------------------------------------ //
    // Lifecycle
    // ------------------------------------------------------------------ //

    /// Clear all registrations (used between tests or on full restart).
    void Reset();

    /// Produce a multi-line human-readable health report.
    std::string HealthReport() const;

private:
    GameSystemsRegistry() = default;
    SystemEntry* FindMutable(const std::string& name);

    std::vector<SystemEntry> m_systems;
};

} // namespace atlas
