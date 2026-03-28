#pragma once

#include <string>
#include <unordered_map>
#include <vector>

namespace Atlas::Security {

class CapabilityResolver {
public:
    bool LoadFromFile(const std::string& path);
    bool HasCapability(const std::string& modeOrTokenModeName,
                       const std::vector<std::string>& sessionCapabilities,
                       const std::string& requestedCapability,
                       bool writeElevation) const;

private:
    std::unordered_map<std::string, std::vector<std::string>> byMode_;
};

} // namespace Atlas::Security
