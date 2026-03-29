#pragma once

#include <filesystem>
#include <string>
#include <vector>

namespace Atlas::Security {

enum class PathClass {
    Unknown,
    Protected,
    Generated,
    Archive,
    Sandbox,
    ExternalSync
};

struct PathPolicy {
    std::vector<std::filesystem::path> protectedRoots;
    std::vector<std::filesystem::path> generatedRoots;
    std::vector<std::filesystem::path> archiveRoots;
    std::vector<std::filesystem::path> sandboxRoots;
    std::vector<std::filesystem::path> externalSyncRoots;
};

class PathPolicyService {
public:
    bool LoadFromFile(const std::filesystem::path& path);
    PathClass Classify(const std::filesystem::path& path) const;
    bool CanRead(const std::filesystem::path& path) const;
    bool CanWrite(const std::filesystem::path& path, bool reviewedDiffApproved) const;
    const PathPolicy& GetPolicy() const { return policy_; }

private:
    PathPolicy policy_;
};

std::string ToString(PathClass pathClass);

} // namespace Atlas::Security
