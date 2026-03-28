// KeybindConfig.h
// Atlas Engine Config — remappable keybind configuration system: action
// definitions, default bindings, conflict detection, save/load.

#pragma once
#include <cstdint>
#include <functional>
#include <optional>
#include <string>
#include <vector>

namespace atlas::config {

// ---------------------------------------------------------------------------
// Key code (platform-agnostic)
// ---------------------------------------------------------------------------

enum class EKeyCode : uint16_t
{
    Unknown = 0,
    // Letters
    A=65, B, C, D, E, F, G, H, I, J, K, L, M,
    N, O, P, Q, R, S, T, U, V, W, X, Y, Z,
    // Digits
    Digit0=48, Digit1, Digit2, Digit3, Digit4,
    Digit5, Digit6, Digit7, Digit8, Digit9,
    // Function keys
    F1=112, F2, F3, F4, F5, F6, F7, F8, F9, F10, F11, F12,
    // Special
    Escape=256, Enter, Space, Tab, Backspace, Delete,
    Insert, Home, End, PageUp, PageDown,
    Left, Right, Up, Down,
    LeftShift=340, LeftControl, LeftAlt,
    RightShift, RightControl, RightAlt,
    // Mouse
    MouseLeft=400, MouseRight, MouseMiddle,
    MouseWheelUp, MouseWheelDown,
};

// ---------------------------------------------------------------------------
// Modifier flags
// ---------------------------------------------------------------------------

using KeyModifiers = uint8_t;
namespace Modifiers {
    inline constexpr KeyModifiers None    = 0x00;
    inline constexpr KeyModifiers Shift   = 0x01;
    inline constexpr KeyModifiers Control = 0x02;
    inline constexpr KeyModifiers Alt     = 0x04;
}

// ---------------------------------------------------------------------------
// Keybind entry
// ---------------------------------------------------------------------------

enum class EInputContext : uint8_t
{
    Global,     ///< active in all modes
    Gameplay,   ///< ship/flight/combat
    Editor,     ///< editor-only actions
    UI,         ///< menu/dialog overlay
    Walking,    ///< on-foot character
};

struct KeybindEntry
{
    std::string    actionId;       ///< e.g. "fire_weapon", "open_map"
    std::string    displayName;
    std::string    category;       ///< "Combat", "Navigation", "Editor", etc.
    EInputContext  context        = EInputContext::Global;
    EKeyCode       primaryKey     = EKeyCode::Unknown;
    KeyModifiers   primaryMods    = Modifiers::None;
    EKeyCode       secondaryKey   = EKeyCode::Unknown;  ///< alternate binding
    KeyModifiers   secondaryMods  = Modifiers::None;
    bool           isRebindable   = true;
    bool           isGamepad      = false;
    uint8_t        gamepadButton  = 0;
};

// ---------------------------------------------------------------------------
// Conflict
// ---------------------------------------------------------------------------

struct KeybindConflict
{
    std::string actionA;
    std::string actionB;
    EKeyCode    conflictKey;
    KeyModifiers conflictMods;
    bool        isPrimary;  ///< true = primary binding conflicted
};

// ---------------------------------------------------------------------------
// KeybindConfig
// ---------------------------------------------------------------------------

class KeybindConfig
{
public:
    bool Initialize();
    void Shutdown();

    // ---- action registration -------------------------------------------
    void RegisterAction   (const KeybindEntry& entry);
    bool UnregisterAction (const std::string& actionId);
    bool HasAction        (const std::string& actionId) const;
    std::optional<KeybindEntry> FindAction(const std::string& actionId) const;
    std::vector<KeybindEntry>   ListActions(EInputContext ctx) const;
    std::vector<KeybindEntry>   ListAllActions() const { return m_entries; }
    size_t ActionCount() const { return m_entries.size(); }

    // ---- rebinding -----------------------------------------------------
    bool SetPrimaryBinding  (const std::string& actionId, EKeyCode key,
                               KeyModifiers mods = Modifiers::None);
    bool SetSecondaryBinding(const std::string& actionId, EKeyCode key,
                               KeyModifiers mods = Modifiers::None);
    bool ClearBinding       (const std::string& actionId, bool primary = true);
    bool ResetToDefault     (const std::string& actionId);

    // ---- default bindings (stored separately for reset) ----------------
    void SetDefault(const std::string& actionId, EKeyCode key,
                     KeyModifiers mods = Modifiers::None,
                     bool primary = true);

    // ---- conflict detection --------------------------------------------
    std::vector<KeybindConflict> DetectConflicts() const;
    bool HasConflicts() const;
    std::vector<KeybindConflict> ConflictsForAction(
        const std::string& actionId) const;

    // ---- query by key --------------------------------------------------
    std::optional<std::string> GetActionForKey(EKeyCode key,
                                                 KeyModifiers mods,
                                                 EInputContext ctx) const;

    // ---- serialise / deserialise --------------------------------------
    std::string Serialise()         const;   ///< JSON-like key=value format
    bool        Deserialise(const std::string& data);

    // ---- load defaults -------------------------------------------------
    void RegisterDefaultGameplayBindings();
    void RegisterDefaultEditorBindings();

    // ---- change callback -----------------------------------------------
    using BindingChangedCallback = std::function<void(const std::string& actionId)>;
    void SetBindingChangedCallback(BindingChangedCallback cb)
    { m_changeCb = std::move(cb); }

private:
    struct DefaultEntry { EKeyCode key; KeyModifiers mods; bool primary; };

    std::vector<KeybindEntry>                           m_entries;
    std::vector<std::pair<std::string, DefaultEntry>>   m_defaults;
    BindingChangedCallback                              m_changeCb;

    KeybindEntry* GetMutable(const std::string& actionId);
    bool KeyModsMatch(EKeyCode k, KeyModifiers m,
                       EKeyCode ek, KeyModifiers em) const;
};

} // namespace atlas::config
