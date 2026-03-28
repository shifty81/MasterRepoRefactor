// EditorDockLayout.cpp
// Atlas Editor — editor panel docking basics.

#include "Core/EditorDockLayout.h"

#include <algorithm>

namespace atlas::editor::dock {

bool EditorDockLayout::Initialize() { return true; }
void EditorDockLayout::Shutdown()   { m_panels.clear(); m_presets.clear(); }

void EditorDockLayout::RegisterPanel(const DockPanel& panel)
{
    for (auto& p : m_panels)
        if (p.panelId == panel.panelId) { p = panel; return; }
    m_panels.push_back(panel);
}

bool EditorDockLayout::UnregisterPanel(const std::string& panelId)
{
    auto it = std::find_if(m_panels.begin(), m_panels.end(),
                           [&](const DockPanel& p){ return p.panelId == panelId; });
    if (it == m_panels.end()) return false;
    m_panels.erase(it);
    m_drawCallbacks.erase(panelId);
    return true;
}

bool EditorDockLayout::ShowPanel(const std::string& panelId)
{
    DockPanel* p = GetMutable(panelId);
    if (!p) return false;
    p->visible = true;
    return true;
}

bool EditorDockLayout::HidePanel(const std::string& panelId)
{
    DockPanel* p = GetMutable(panelId);
    if (!p) return false;
    p->visible = false;
    return true;
}

bool EditorDockLayout::TogglePanel(const std::string& panelId)
{
    DockPanel* p = GetMutable(panelId);
    if (!p) return false;
    p->visible = !p->visible;
    return true;
}

bool EditorDockLayout::IsPanelVisible(const std::string& panelId) const
{
    for (const auto& p : m_panels)
        if (p.panelId == panelId) return p.visible;
    return false;
}

bool EditorDockLayout::FocusPanel(const std::string& panelId)
{
    for (auto& p : m_panels)
        p.focused = (p.panelId == panelId);
    m_focusedPanel = panelId;
    return true;
}

std::optional<std::string> EditorDockLayout::GetFocusedPanel() const
{
    if (m_focusedPanel.empty()) return std::nullopt;
    return m_focusedPanel;
}

void EditorDockLayout::RegisterPreset(const DockLayoutPreset& preset)
{
    for (auto& pr : m_presets)
        if (pr.presetId == preset.presetId) { pr = preset; return; }
    m_presets.push_back(preset);
}

bool EditorDockLayout::ApplyPreset(const std::string& presetId)
{
    for (const auto& pr : m_presets)
    {
        if (pr.presetId != presetId) continue;
        m_panels.clear();
        m_panels = pr.panels;
        return true;
    }
    return false;
}

DockLayoutPreset EditorDockLayout::CurrentLayout() const
{
    DockLayoutPreset layout;
    layout.presetId    = "current";
    layout.displayName = "Current Layout";
    layout.panels      = m_panels;
    return layout;
}

bool EditorDockLayout::SetPanelSize(const std::string& panelId, float normalised)
{
    DockPanel* p = GetMutable(panelId);
    if (!p) return false;
    p->size = normalised;
    return true;
}

std::vector<DockPanel> EditorDockLayout::ListPanels() const
{
    return m_panels;
}

std::vector<DockPanel> EditorDockLayout::ListByRegion(EDockRegion region) const
{
    std::vector<DockPanel> result;
    for (const auto& p : m_panels)
        if (p.region == region) result.push_back(p);
    return result;
}

std::optional<DockPanel> EditorDockLayout::FindPanel(const std::string& id) const
{
    for (const auto& p : m_panels)
        if (p.panelId == id) return p;
    return std::nullopt;
}

void EditorDockLayout::SetDrawCallback(const std::string& panelId,
                                         PanelDrawCallback cb)
{
    m_drawCallbacks[panelId] = std::move(cb);
}

void EditorDockLayout::DrawAll() const
{
    for (const auto& p : m_panels)
    {
        if (!p.visible) continue;
        auto it = m_drawCallbacks.find(p.panelId);
        if (it != m_drawCallbacks.end())
            it->second(p.panelId);
    }
}

DockPanel* EditorDockLayout::GetMutable(const std::string& panelId)
{
    for (auto& p : m_panels)
        if (p.panelId == panelId) return &p;
    return nullptr;
}

} // namespace atlas::editor::dock
