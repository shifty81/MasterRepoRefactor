#pragma once

#include <string>

namespace Atlas::Editor {

class DiffPanelWidget {
public:
    void LoadDiff(const std::string& unifiedDiff);
    void OnApprove();
    void OnReject();

private:
    std::string m_pendingDiff;
};

} // namespace Atlas::Editor
