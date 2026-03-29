#pragma once
#include <string>
#include <vector>

namespace Atlas::Editor {

/// Phase 17A — Dev AI Phase 3: AI context panel.
/// Shows the current AI session context: active file, symbols in scope,
/// recent diffs, and model backend status.
class AIContextPanel {
public:
    void SetActiveFile(const std::string& filePath);
    void AddSymbol(const std::string& symbol);
    void ClearSymbols();
    void SetModelStatus(const std::string& status);

    const std::string& GetActiveFile() const { return m_activeFile; }
    const std::vector<std::string>& GetSymbols() const { return m_symbols; }
    const std::string& GetModelStatus() const { return m_modelStatus; }

private:
    std::string m_activeFile;
    std::vector<std::string> m_symbols;
    std::string m_modelStatus{"idle"};
};

} // namespace Atlas::Editor
