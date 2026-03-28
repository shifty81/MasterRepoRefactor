#pragma once

#include <string>

namespace Atlas::Editor {

class DiagnosticsPanel {
public:
    void AddEntry(const std::string& severity, const std::string& message, const std::string& source);
    void Clear();
    void SetSeverityFilter(const std::string& minSeverity);

private:
    std::string m_severityFilter;
};

} // namespace Atlas::Editor
