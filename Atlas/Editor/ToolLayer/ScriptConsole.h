#pragma once
#include "ITool.h"
#include <string>
#include <vector>

namespace Atlas::Editor {

/// P3 Tool — Real-time scripting console for debug commands and live Lua/Python execution.
class ScriptConsole : public ITool {
public:
    struct ConsoleEntry {
        std::string text;
        std::string level;  // "info", "warn", "error", "output"
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "ScriptConsole"; }
    bool IsActive() const override { return m_active; }

    void Execute(const std::string& command);
    void Print(const std::string& text, const std::string& level = "info");
    void Clear();
    void SetMaxHistory(int maxLines);

    const std::vector<ConsoleEntry>& GetHistory() const { return m_history; }
    int GetHistorySize() const { return static_cast<int>(m_history.size()); }

private:
    bool m_active{false};
    int m_maxHistory{500};
    std::vector<ConsoleEntry> m_history;
};

} // namespace Atlas::Editor
