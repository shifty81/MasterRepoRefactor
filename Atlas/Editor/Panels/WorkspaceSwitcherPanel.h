#pragma once

#include <string>

namespace Atlas::Editor {

class WorkspaceSwitcherPanel {
public:
    void Refresh();
    void SwitchTo(const std::string& workspaceId);
    std::string GetActiveWorkspaceId() const;

private:
    std::string m_activeWorkspaceId;
};

} // namespace Atlas::Editor
