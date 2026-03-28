#pragma once
#include <string>

namespace atlas::editor {

struct ThemeConfig {
    std::string name;
    float primaryR   = 0.2f;
    float primaryG   = 0.2f;
    float primaryB   = 0.2f;
    float accentR    = 0.4f;
    float accentG    = 0.7f;
    float accentB    = 1.0f;
    float fontSize   = 14.0f;
};

class UIThemeManager {
public:
    static UIThemeManager& Instance();

    void LoadTheme(const std::string& path);
    void ApplyTheme(const ThemeConfig& config);
    const ThemeConfig& GetCurrentTheme() const;

private:
    UIThemeManager() = default;
    ThemeConfig m_current;
};

} // namespace atlas::editor
