#include "UIWidgetRegistry.h"

namespace atlas::editor {

UIWidgetRegistry& UIWidgetRegistry::Instance() {
    static UIWidgetRegistry instance;
    return instance;
}

void UIWidgetRegistry::Register(const std::string& id, WidgetFactory factory) {
    m_widgets[id] = std::move(factory);
}

void UIWidgetRegistry::Unregister(const std::string& id) {
    m_widgets.erase(id);
}

bool UIWidgetRegistry::InvokeWidget(const std::string& id) {
    auto it = m_widgets.find(id);
    if (it == m_widgets.end()) return false;
    it->second();
    return true;
}

} // namespace atlas::editor
