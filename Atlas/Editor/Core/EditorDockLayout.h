// EditorDockLayout.h
// Atlas Editor — editor panel docking basics: named docks, layout presets,
// panel show/hide, and dock region sizing.

#pragma once
#include <functional>
#include <optional>
#include <string>
#include <unordered_map>
#include <vector>

namespace atlas::editor::dock {

enum class EDockRegion : uint8_t
{
    Left,
    Right,
    Bottom,
    Top,
    Centre,       ///< main viewport
    FloatingModal,
};

struct DockPanel
{
    std::string    panelId;
    std::string    title;
    EDockRegion    region    = EDockRegion::Right;
    float          size      = 0.25f; ///< normalised fraction of parent axis
    bool           visible   = true;
    bool           closeable = true;
    bool           focused   = false;
};

struct DockLayoutPreset
{
    std::string             presetId;
    std::string             displayName;
    std::vector<DockPanel>  panels;
};

class EditorDockLayout
{
public:
    bool Initialize();
    void Shutdown();

    // ---- panel registration -----------------------------------------
    void RegisterPanel(const DockPanel& panel);
    bool UnregisterPanel(const std::string& panelId);

    // ---- visibility -------------------------------------------------
    bool ShowPanel(const std::string& panelId);
    bool HidePanel(const std::string& panelId);
    bool TogglePanel(const std::string& panelId);
    bool IsPanelVisible(const std::string& panelId) const;

    // ---- focus ------------------------------------------------------
    bool FocusPanel(const std::string& panelId);
    std::optional<std::string> GetFocusedPanel() const;

    // ---- layout presets ---------------------------------------------
    void RegisterPreset(const DockLayoutPreset& preset);
    bool ApplyPreset(const std::string& presetId);
    DockLayoutPreset CurrentLayout() const;

    // ---- resize -----------------------------------------------------
    bool SetPanelSize(const std::string& panelId, float normalised);

    // ---- queries ----------------------------------------------------
    std::vector<DockPanel> ListPanels()                       const;
    std::vector<DockPanel> ListByRegion(EDockRegion region)   const;
    std::optional<DockPanel> FindPanel(const std::string& id) const;

    // ---- render callback --------------------------------------------
    using PanelDrawCallback = std::function<void(const std::string& panelId)>;
    void SetDrawCallback(const std::string& panelId, PanelDrawCallback cb);
    void DrawAll() const;

private:
    std::vector<DockPanel>    m_panels;
    std::vector<DockLayoutPreset> m_presets;
    std::string               m_focusedPanel;
    std::unordered_map<std::string, PanelDrawCallback> m_drawCallbacks;

    DockPanel* GetMutable(const std::string& panelId);
};

} // namespace atlas::editor::dock
