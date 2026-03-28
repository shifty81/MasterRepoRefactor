// EditorLaunchBridge.h
// Atlas Editor — connects editor startup to the RuntimeBootstrap / LaunchConfig pipeline.
//
// EditorLaunchBridge is the single handshake point between the editor shell and
// the engine boot sequence. It:
//   1. Accepts a parsed LaunchConfig.
//   2. Calls RuntimeBootstrap::Initialize(RuntimeMode::Editor).
//   3. Optionally starts the AtlasAI bridge server.
//   4. Registers all editor subsystems in GameSystemsRegistry.
//   5. Returns a BootResult that the editor shell uses to decide whether to
//      proceed to the main loop or report a fatal error.

#pragma once
#include <string>
#include <memory>
#include <cstdint>

namespace atlas
{
struct LaunchParams;
}

namespace atlas::editor
{

/// Outcome of an EditorLaunchBridge::Boot() call.
struct EditorBootResult
{
    bool        success = false;
    std::string message;

    /// Recommended exit code if boot fails.
    int ExitCode() const { return success ? 0 : 1; }
};

/// Subsystems that EditorLaunchBridge wires up during boot.
enum class EEditorSubsystem : uint32_t
{
    Core            = 1 << 0,
    Outliner        = 1 << 1,
    Inspector       = 1 << 2,
    Viewport        = 1 << 3,
    AssetBrowser    = 1 << 4,
    Gizmos          = 1 << 5,
    CommandStack    = 1 << 6,
    ValidationPanel = 1 << 7,
    DocsPanel       = 1 << 8,
    DiffReview      = 1 << 9,
    AtlasAIBridge   = 1 << 10,
    All             = 0x7FF,
};

inline EEditorSubsystem operator|(EEditorSubsystem a, EEditorSubsystem b)
{
    return static_cast<EEditorSubsystem>(
        static_cast<uint32_t>(a) | static_cast<uint32_t>(b));
}

/// Boots the editor stack from a resolved LaunchParams.
class EditorLaunchBridge
{
public:
    EditorLaunchBridge() = default;

    /// Subsystem mask — override to boot only a subset (useful in tests).
    void SetSubsystemMask(EEditorSubsystem mask) { m_mask = mask; }
    EEditorSubsystem GetSubsystemMask() const    { return m_mask; }

    /// Execute the editor boot sequence.
    EditorBootResult Boot(const atlas::LaunchParams& params);

    /// Whether Boot() has been called and succeeded.
    bool IsBooted() const { return m_booted; }

    /// Perform an orderly shutdown (reverse order of boot).
    void Shutdown();

private:
    EEditorSubsystem m_mask   = EEditorSubsystem::All;
    bool             m_booted = false;

    bool BootCore(const atlas::LaunchParams& params, std::string& err);
    bool BootEditorSubsystems(const atlas::LaunchParams& params, std::string& err);
    bool BootAtlasAIBridge(const atlas::LaunchParams& params, std::string& err);
};

} // namespace atlas::editor
