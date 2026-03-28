#include "security/CapabilityResolver.h"

#include "common/TextUtil.h"

namespace Atlas::Security {

bool CapabilityResolver::LoadFromFile(const std::string& path) {
    const std::string json = Atlas::Common::ReadTextFile(path);
    if (json.empty()) {
        return false;
    }

    byMode_.clear();
    for (const std::string mode : {"observer", "reviewer", "editor", "admin_local"}) {
        byMode_[mode] = Atlas::Common::ExtractStringArray(json, mode);
    }
    return true;
}

bool CapabilityResolver::HasCapability(const std::string& modeName,
                                       const std::vector<std::string>& sessionCapabilities,
                                       const std::string& requestedCapability,
                                       bool writeElevation) const {
    if (requestedCapability.rfind("write_", 0) == 0 && !writeElevation) {
        return false;
    }

    auto contains = [&](const std::vector<std::string>& list) {
        for (const auto& item : list) {
            if (item == "*" || item == requestedCapability) {
                return true;
            }
        }
        return false;
    };

    const auto modeIt = byMode_.find(modeName);
    if (modeIt != byMode_.end() && contains(modeIt->second)) {
        return true;
    }
    return contains(sessionCapabilities);
}

} // namespace Atlas::Security
