#pragma once

#include "common/Status.h"

#include <chrono>
#include <optional>
#include <string>
#include <unordered_map>
#include <vector>

namespace Atlas::Security {

enum class SessionMode {
    Observer,
    Reviewer,
    Editor,
    AdminLocal
};

struct SessionRecord {
    std::string token;
    SessionMode mode{SessionMode::Observer};
    std::vector<std::string> capabilities;
    std::string machineIdentity;
    std::string userIdentity;
    std::chrono::system_clock::time_point expiresAt{};
    bool writeElevation{false};
};

class SessionAuthority {
public:
    SessionAuthority() = default;

    std::string CreateSession(SessionMode mode,
                              std::vector<std::string> capabilities,
                              std::string machineIdentity,
                              std::string userIdentity,
                              std::chrono::minutes ttl,
                              bool writeElevation);

    std::optional<SessionRecord> Validate(const std::string& token) const;
    Atlas::Common::Status Revoke(const std::string& token);
    Atlas::Common::Status Rotate(const std::string& token, std::chrono::minutes ttl, std::string* newToken);

private:
    static std::string GenerateToken();
    std::unordered_map<std::string, SessionRecord> sessions_;
};

std::string ToString(SessionMode mode);

} // namespace Atlas::Security
