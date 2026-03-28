#include "security/PathPolicyService.h"

#include "common/TextUtil.h"

namespace Atlas::Security {

std::string ToString(PathClass pathClass) {
    switch (pathClass) {
    case PathClass::Protected: return "protected";
    case PathClass::Generated: return "generated";
    case PathClass::Archive: return "archive";
    case PathClass::Sandbox: return "sandbox";
    case PathClass::ExternalSync: return "external_sync";
    default: return "unknown";
    }
}

bool PathPolicyService::LoadFromFile(const std::filesystem::path& path) {
    const std::string json = Atlas::Common::ReadTextFile(path);
    if (json.empty()) {
        return false;
    }

    auto toPaths = [](const std::vector<std::string>& values) {
        std::vector<std::filesystem::path> out;
        for (const auto& value : values) {
            out.emplace_back(value);
        }
        return out;
    };

    policy_.protectedRoots = toPaths(Atlas::Common::ExtractStringArray(json, "protectedRoots"));
    policy_.generatedRoots = toPaths(Atlas::Common::ExtractStringArray(json, "generatedRoots"));
    policy_.archiveRoots = toPaths(Atlas::Common::ExtractStringArray(json, "archiveRoots"));
    policy_.sandboxRoots = toPaths(Atlas::Common::ExtractStringArray(json, "sandboxRoots"));
    policy_.externalSyncRoots = toPaths(Atlas::Common::ExtractStringArray(json, "externalSyncRoots"));
    return true;
}

PathClass PathPolicyService::Classify(const std::filesystem::path& path) const {
    auto classify = [&](const std::vector<std::filesystem::path>& roots, PathClass cls) {
        for (const auto& root : roots) {
            if (Atlas::Common::StartsWithPath(path, root)) {
                return cls;
            }
        }
        return PathClass::Unknown;
    };

    if (auto cls = classify(policy_.protectedRoots, PathClass::Protected); cls != PathClass::Unknown) return cls;
    if (auto cls = classify(policy_.generatedRoots, PathClass::Generated); cls != PathClass::Unknown) return cls;
    if (auto cls = classify(policy_.archiveRoots, PathClass::Archive); cls != PathClass::Unknown) return cls;
    if (auto cls = classify(policy_.sandboxRoots, PathClass::Sandbox); cls != PathClass::Unknown) return cls;
    if (auto cls = classify(policy_.externalSyncRoots, PathClass::ExternalSync); cls != PathClass::Unknown) return cls;
    return PathClass::Unknown;
}

bool PathPolicyService::CanRead(const std::filesystem::path& path) const {
    return Classify(path) != PathClass::Unknown;
}

bool PathPolicyService::CanWrite(const std::filesystem::path& path, bool reviewedDiffApproved) const {
    switch (Classify(path)) {
    case PathClass::Generated:
    case PathClass::Sandbox:
        return true;
    case PathClass::Archive:
        return true;
    case PathClass::ExternalSync:
        return false;
    case PathClass::Protected:
        return reviewedDiffApproved;
    default:
        return false;
    }
}

} // namespace Atlas::Security
