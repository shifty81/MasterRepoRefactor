// InputContextManager.h
// Atlas Engine — input context system with game/editor context switching,
// mouse capture policy, and remappable keybind config.

#pragma once
#include "InputManager.h"

#include <functional>
#include <string>
#include <unordered_map>
#include <vector>

namespace atlas::input {

// ---------------------------------------------------------------------------
// Context definitions
// ---------------------------------------------------------------------------

enum class EInputContext : uint8_t
{
    None    = 0,
    Game    = 1,  ///< full gameplay input (camera, movement, actions)
    UI      = 2,  ///< UI / menu active — gameplay actions suppressed
    Editor  = 3,  ///< editor mode — viewport navigation + tool shortcuts
    EditorModal = 4, ///< modal dialog in editor — all gameplay suppressed
    Debug   = 5,  ///< dev console / overlay
};

// ---------------------------------------------------------------------------
// Mouse capture policy per context
// ---------------------------------------------------------------------------

enum class EMouseCaptureMode : uint8_t
{
    Free,           ///< cursor visible, not captured
    Locked,         ///< cursor hidden, locked to window centre (FPS / editor drag)
    Confined,       ///< cursor visible but confined to window rect
};

// ---------------------------------------------------------------------------
// Remappable keybind entry
// ---------------------------------------------------------------------------

struct RemappableBinding
{
    InputAction   action         = InputAction::None;
    InputDevice   primaryDevice  = InputDevice::Keyboard;
    uint32_t      primaryKey     = 0;
    InputDevice   altDevice      = InputDevice::Gamepad;
    uint32_t      altKey         = 0;
    std::string   displayName;
    bool          rebindable     = true;
};

struct KeybindConfig
{
    std::vector<RemappableBinding> bindings;
    std::string                    configVersion = "1.0";
};

// ---------------------------------------------------------------------------
// Context transition record for history
// ---------------------------------------------------------------------------

struct ContextTransition
{
    EInputContext from = EInputContext::None;
    EInputContext to   = EInputContext::None;
    std::string   reason;
};

// ---------------------------------------------------------------------------
// InputContextManager
// ---------------------------------------------------------------------------

class InputContextManager
{
public:
    InputContextManager()  = default;
    ~InputContextManager() = default;

    bool Initialize(InputManager& manager);
    void Shutdown();

    // ---- context switching ------------------------------------------
    void PushContext(EInputContext ctx, const std::string& reason = "");
    void PopContext();
    void SetContext(EInputContext ctx, const std::string& reason = "");
    EInputContext CurrentContext() const { return m_contextStack.empty()
        ? EInputContext::None : m_contextStack.back(); }
    bool IsGameActive()   const { return CurrentContext() == EInputContext::Game; }
    bool IsEditorActive() const { return CurrentContext() == EInputContext::Editor ||
                                         CurrentContext() == EInputContext::EditorModal; }
    bool IsUIActive()     const { return CurrentContext() == EInputContext::UI; }

    // ---- mouse capture ----------------------------------------------
    void              SetMouseCapture(EMouseCaptureMode mode);
    EMouseCaptureMode GetMouseCaptureMode() const { return m_mouseMode; }

    /// Automatically choose mouse mode for the given context.
    void ApplyDefaultMousePolicy(EInputContext ctx);

    // ---- remappable keybinds ----------------------------------------
    void              LoadKeybindConfig(const KeybindConfig& cfg);
    KeybindConfig     GetKeybindConfig() const;
    bool              Remap(InputAction action,
                             InputDevice device, uint32_t key);
    bool              ResetToDefault(InputAction action);
    void              ResetAllToDefault();

    // ---- action routing ---------------------------------------------
    /// Returns true when the action should be dispatched in the current context.
    bool ShouldDispatch(InputAction action) const;

    /// Route an injected press through context filter → InputManager.
    bool RoutePress(InputAction action);
    bool RouteRelease(InputAction action);

    // ---- callbacks --------------------------------------------------
    using ContextChangedCallback = std::function<void(EInputContext from, EInputContext to)>;
    void SetContextChangedCallback(ContextChangedCallback cb)
    { m_contextCb = std::move(cb); }

    // ---- history / diagnostics --------------------------------------
    const std::vector<ContextTransition>& GetTransitionHistory() const
    { return m_history; }

private:
    InputManager*                     m_manager    = nullptr;
    std::vector<EInputContext>        m_contextStack;
    EMouseCaptureMode                 m_mouseMode  = EMouseCaptureMode::Free;
    KeybindConfig                     m_keybinds;
    KeybindConfig                     m_defaultKeybinds;
    ContextChangedCallback            m_contextCb;
    std::vector<ContextTransition>    m_history;

    void FireContextChanged(EInputContext from, EInputContext to,
                             const std::string& reason);
    void ApplyBindingsToManager();

    /// Actions blocked in UI/EditorModal contexts.
    static bool IsGameplayAction(InputAction action);
};

} // namespace atlas::input
