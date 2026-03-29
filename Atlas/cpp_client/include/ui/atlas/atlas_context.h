#pragma once

// NOTE: This file is the Atlas-editor-side copy of the AtlasContext declaration.
// It must be kept in sync with NovaForge/Client/include/ui/atlas/atlas_context.h.
// Both copies exist because Atlas/Editor cannot include across the NovaForge
// boundary; the canonical source is the NovaForge copy.

#include "atlas_types.h"
#include "atlas_renderer.h"
#include <string>

namespace atlas {

class AtlasContext {
public:
    AtlasContext();
    ~AtlasContext();

    bool init();
    void shutdown();

    void beginFrame(const InputState& input);
    void endFrame();

    AtlasRenderer& renderer() { return m_renderer; }
    const Theme&    theme()    const { return m_theme; }
    const InputState& input()  const { return m_input; }

    void setTheme(const Theme& t) { m_theme = t; }
    bool loadThemeFromFile(const std::string& path);

    bool isHovered(const Rect& r) const;

    void setHot(WidgetID id);
    void setActive(WidgetID id);
    void clearActive();

    bool isHot(WidgetID id)    const { return m_hotID == id; }
    bool isActive(WidgetID id) const { return m_activeID == id; }

    bool buttonBehavior(const Rect& r, WidgetID id);

    void pushID(const char* label);
    void popID();
    WidgetID currentID(const char* label) const;

    Vec2 getDragDelta() const;

    bool isMouseDown() const { return m_input.mouseDown[0]; }
    bool isMouseClicked() const { return m_input.mouseClicked[0]; }
    bool isRightMouseClicked() const { return m_input.mouseClicked[1]; }

    void consumeMouse() { m_mouseConsumed = true; }
    bool isMouseConsumed() const { return m_mouseConsumed; }

    void pushPanelBounds(const Rect& bounds) { m_panelBoundsStack.push_back(bounds); }
    Rect popPanelBounds() {
        if (m_panelBoundsStack.empty()) return {};
        Rect r = m_panelBoundsStack.back();
        m_panelBoundsStack.pop_back();
        return r;
    }

    void setSidebarWidth(float w) { m_sidebarWidth = w; }
    float sidebarWidth() const { return m_sidebarWidth; }

private:
    AtlasRenderer m_renderer;
    Theme          m_theme;
    InputState     m_input;
    Vec2           m_prevMousePos;

    WidgetID m_hotID    = 0;
    WidgetID m_activeID = 0;

    bool m_mouseConsumed = false;
    float m_sidebarWidth = 0.0f;

    std::vector<WidgetID> m_idStack;
    std::vector<Rect> m_panelBoundsStack;
};

} // namespace atlas
