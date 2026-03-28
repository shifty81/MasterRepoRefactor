#include "UIThemeManager.h"

namespace atlas::editor {

UIThemeManager& UIThemeManager::Instance() {
    static UIThemeManager instance;
    return instance;
}

void UIThemeManager::LoadTheme(const std::string& /*path*/) {
    // TODO: parse theme file and populate m_current
}

void UIThemeManager::ApplyTheme(const ThemeConfig& config) {
    m_current = config;
    // TODO: push values into the UI renderer / ImGui style
}

const ThemeConfig& UIThemeManager::GetCurrentTheme() const {
    return m_current;
}

} // namespace atlas::editor
