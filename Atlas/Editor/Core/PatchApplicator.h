#pragma once

#include <string>

namespace Atlas::Editor {

class PatchApplicator {
public:
    bool ApplyPatch(const std::string& workspaceRoot, const std::string& unifiedDiff);
    bool ValidatePatch(const std::string& unifiedDiff);
};

} // namespace Atlas::Editor
