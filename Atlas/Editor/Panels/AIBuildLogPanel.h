#pragma once
#include <string>
#include <vector>

namespace Atlas::Editor {

/// Phase 17A — Dev AI Phase 3: AI build log panel.
/// Streams build/test output from the Dev AI agent loop.
class AIBuildLogPanel {
public:
    void AppendLine(const std::string& line);
    void Clear();
    void SetMaxLines(int maxLines);

    const std::vector<std::string>& GetLines() const { return m_lines; }
    int GetLineCount() const { return static_cast<int>(m_lines.size()); }

private:
    std::vector<std::string> m_lines;
    int m_maxLines{1000};
};

} // namespace Atlas::Editor
