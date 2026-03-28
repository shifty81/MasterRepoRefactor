// KeybindConfig.cpp
// Atlas Engine Config — remappable keybind configuration.

#include "Config/KeybindConfig.h"

#include <algorithm>
#include <sstream>

namespace atlas::config {

bool KeybindConfig::Initialize() { return true; }
void KeybindConfig::Shutdown()
{
    m_entries.clear();
    m_defaults.clear();
}

void KeybindConfig::RegisterAction(const KeybindEntry& entry)
{
    for (auto& e : m_entries)
        if (e.actionId == entry.actionId) { e = entry; return; }
    m_entries.push_back(entry);
}

bool KeybindConfig::UnregisterAction(const std::string& actionId)
{
    auto it = std::find_if(m_entries.begin(), m_entries.end(),
                           [&](const KeybindEntry& e){ return e.actionId == actionId; });
    if (it == m_entries.end()) return false;
    m_entries.erase(it);
    return true;
}

bool KeybindConfig::HasAction(const std::string& actionId) const
{
    return FindAction(actionId).has_value();
}

std::optional<KeybindEntry> KeybindConfig::FindAction(
    const std::string& actionId) const
{
    for (const auto& e : m_entries)
        if (e.actionId == actionId) return e;
    return std::nullopt;
}

std::vector<KeybindEntry> KeybindConfig::ListActions(
    EInputContext ctx) const
{
    std::vector<KeybindEntry> result;
    for (const auto& e : m_entries)
        if (e.context == ctx || e.context == EInputContext::Global)
            result.push_back(e);
    return result;
}

bool KeybindConfig::SetPrimaryBinding(const std::string& actionId,
                                        EKeyCode key, KeyModifiers mods)
{
    KeybindEntry* e = GetMutable(actionId);
    if (!e || !e->isRebindable) return false;
    e->primaryKey  = key;
    e->primaryMods = mods;
    if (m_changeCb) m_changeCb(actionId);
    return true;
}

bool KeybindConfig::SetSecondaryBinding(const std::string& actionId,
                                          EKeyCode key, KeyModifiers mods)
{
    KeybindEntry* e = GetMutable(actionId);
    if (!e || !e->isRebindable) return false;
    e->secondaryKey  = key;
    e->secondaryMods = mods;
    if (m_changeCb) m_changeCb(actionId);
    return true;
}

bool KeybindConfig::ClearBinding(const std::string& actionId, bool primary)
{
    KeybindEntry* e = GetMutable(actionId);
    if (!e || !e->isRebindable) return false;
    if (primary) { e->primaryKey = EKeyCode::Unknown; e->primaryMods = Modifiers::None; }
    else         { e->secondaryKey = EKeyCode::Unknown; e->secondaryMods = Modifiers::None; }
    if (m_changeCb) m_changeCb(actionId);
    return true;
}

bool KeybindConfig::ResetToDefault(const std::string& actionId)
{
    KeybindEntry* e = GetMutable(actionId);
    if (!e) return false;

    for (const auto& [id, def] : m_defaults)
    {
        if (id != actionId) continue;
        if (def.primary)
            { e->primaryKey = def.key; e->primaryMods = def.mods; }
        else
            { e->secondaryKey = def.key; e->secondaryMods = def.mods; }
    }
    if (m_changeCb) m_changeCb(actionId);
    return true;
}

void KeybindConfig::SetDefault(const std::string& actionId,
                                  EKeyCode key, KeyModifiers mods, bool primary)
{
    m_defaults.push_back({ actionId, { key, mods, primary } });
}

std::vector<KeybindConflict> KeybindConfig::DetectConflicts() const
{
    std::vector<KeybindConflict> conflicts;
    for (size_t i = 0; i < m_entries.size(); ++i)
    {
        for (size_t j = i + 1; j < m_entries.size(); ++j)
        {
            const auto& a = m_entries[i];
            const auto& b = m_entries[j];
            // Only conflicts if same or overlapping context.
            if (a.context != b.context &&
                a.context != EInputContext::Global &&
                b.context != EInputContext::Global) continue;

            // Primary vs primary.
            if (a.primaryKey != EKeyCode::Unknown &&
                KeyModsMatch(a.primaryKey, a.primaryMods,
                              b.primaryKey, b.primaryMods))
            {
                conflicts.push_back({ a.actionId, b.actionId,
                                      a.primaryKey, a.primaryMods, true });
            }
            // Primary vs secondary.
            if (a.primaryKey != EKeyCode::Unknown &&
                KeyModsMatch(a.primaryKey, a.primaryMods,
                              b.secondaryKey, b.secondaryMods))
            {
                conflicts.push_back({ a.actionId, b.actionId,
                                      a.primaryKey, a.primaryMods, true });
            }
            // Secondary vs secondary.
            if (a.secondaryKey != EKeyCode::Unknown &&
                KeyModsMatch(a.secondaryKey, a.secondaryMods,
                              b.secondaryKey, b.secondaryMods))
            {
                conflicts.push_back({ a.actionId, b.actionId,
                                      a.secondaryKey, a.secondaryMods, false });
            }
        }
    }
    return conflicts;
}

bool KeybindConfig::HasConflicts() const
{
    return !DetectConflicts().empty();
}

std::vector<KeybindConflict> KeybindConfig::ConflictsForAction(
    const std::string& actionId) const
{
    auto all = DetectConflicts();
    std::vector<KeybindConflict> result;
    for (const auto& c : all)
        if (c.actionA == actionId || c.actionB == actionId)
            result.push_back(c);
    return result;
}

std::optional<std::string> KeybindConfig::GetActionForKey(
    EKeyCode key, KeyModifiers mods, EInputContext ctx) const
{
    for (const auto& e : m_entries)
    {
        if (e.context != ctx && e.context != EInputContext::Global) continue;
        if (KeyModsMatch(key, mods, e.primaryKey, e.primaryMods))
            return e.actionId;
        if (KeyModsMatch(key, mods, e.secondaryKey, e.secondaryMods))
            return e.actionId;
    }
    return std::nullopt;
}

std::string KeybindConfig::Serialise() const
{
    std::ostringstream ss;
    for (const auto& e : m_entries)
    {
        ss << e.actionId << "="
           << static_cast<int>(e.primaryKey) << ":"
           << static_cast<int>(e.primaryMods) << ":"
           << static_cast<int>(e.secondaryKey) << ":"
           << static_cast<int>(e.secondaryMods) << "\n";
    }
    return ss.str();
}

bool KeybindConfig::Deserialise(const std::string& data)
{
    std::istringstream ss(data);
    std::string line;
    while (std::getline(ss, line))
    {
        if (line.empty()) continue;
        auto eq = line.find('=');
        if (eq == std::string::npos) continue;
        std::string id  = line.substr(0, eq);
        std::string val = line.substr(eq + 1);

        // Parse pk:pm:sk:sm
        int pk = 0, pm = 0, sk = 0, sm = 0;
        char sep;
        std::istringstream vs(val);
        vs >> pk >> sep >> pm >> sep >> sk >> sep >> sm;

        KeybindEntry* e = GetMutable(id);
        if (e)
        {
            e->primaryKey    = static_cast<EKeyCode>(pk);
            e->primaryMods   = static_cast<KeyModifiers>(pm);
            e->secondaryKey  = static_cast<EKeyCode>(sk);
            e->secondaryMods = static_cast<KeyModifiers>(sm);
        }
    }
    return true;
}

void KeybindConfig::RegisterDefaultGameplayBindings()
{
    auto reg = [this](const char* id, const char* name, const char* cat,
                       EKeyCode key)
    {
        KeybindEntry e;
        e.actionId    = id;
        e.displayName = name;
        e.category    = cat;
        e.context     = EInputContext::Gameplay;
        e.primaryKey  = key;
        RegisterAction(e);
        SetDefault(id, key);
    };

    reg("fire_weapon",    "Fire Weapon",    "Combat",     EKeyCode::MouseLeft);
    reg("fire_secondary", "Fire Secondary", "Combat",     EKeyCode::MouseRight);
    reg("thrust_forward", "Thrust Forward", "Navigation", EKeyCode::W);
    reg("thrust_back",    "Thrust Back",    "Navigation", EKeyCode::S);
    reg("strafe_left",    "Strafe Left",    "Navigation", EKeyCode::A);
    reg("strafe_right",   "Strafe Right",   "Navigation", EKeyCode::D);
    reg("open_map",       "Open Map",       "UI",         EKeyCode::M);
    reg("open_inventory", "Open Inventory", "UI",         EKeyCode::I);
    reg("dock_request",   "Dock/Undock",    "Navigation", EKeyCode::F);
    reg("target_nearest", "Target Nearest", "Combat",     EKeyCode::T);
}

void KeybindConfig::RegisterDefaultEditorBindings()
{
    auto reg = [this](const char* id, const char* name, const char* cat,
                       EKeyCode key, KeyModifiers mods = Modifiers::None)
    {
        KeybindEntry e;
        e.actionId    = id;
        e.displayName = name;
        e.category    = cat;
        e.context     = EInputContext::Editor;
        e.primaryKey  = key;
        e.primaryMods = mods;
        RegisterAction(e);
        SetDefault(id, key, mods);
    };

    reg("undo",             "Undo",             "Edit",   EKeyCode::Z, Modifiers::Control);
    reg("redo",             "Redo",             "Edit",   EKeyCode::Y, Modifiers::Control);
    reg("save_scene",       "Save Scene",       "File",   EKeyCode::S, Modifiers::Control);
    reg("place_object",     "Place Object",     "Editor", EKeyCode::P);
    reg("delete_selection", "Delete Selection", "Editor", EKeyCode::Delete);
    reg("focus_selected",   "Focus Selected",   "Editor", EKeyCode::F);
    reg("toggle_snap",      "Toggle Snap",      "Editor", EKeyCode::G);
    reg("cycle_gizmo",      "Cycle Gizmo",      "Editor", EKeyCode::R);
    reg("open_asset_browser","Open Assets",     "Editor", EKeyCode::A, Modifiers::Control);
    reg("play_mode",        "Enter Play Mode",  "Editor", EKeyCode::F5);
}

bool KeybindConfig::KeyModsMatch(EKeyCode k, KeyModifiers m,
                                   EKeyCode ek, KeyModifiers em) const
{
    return k == ek && m == em && k != EKeyCode::Unknown;
}

KeybindEntry* KeybindConfig::GetMutable(const std::string& actionId)
{
    for (auto& e : m_entries)
        if (e.actionId == actionId) return &e;
    return nullptr;
}

} // namespace atlas::config
