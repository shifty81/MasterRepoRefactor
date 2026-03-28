#include "security/SessionAuthority.h"

#include <iomanip>
#include <random>
#include <sstream>

namespace Atlas::Security {

std::string ToString(SessionMode mode) {
    switch (mode) {
    case SessionMode::Observer: return "observer";
    case SessionMode::Reviewer: return "reviewer";
    case SessionMode::Editor: return "editor";
    case SessionMode::AdminLocal: return "admin_local";
    }
    return "observer";
}

std::string SessionAuthority::GenerateToken() {
    std::random_device rd;
    std::mt19937_64 gen(rd());
    std::uniform_int_distribution<unsigned long long> dist;

    std::ostringstream oss;
    oss << std::hex << std::setfill('0');
    for (int i = 0; i < 4; ++i) {
        oss << std::setw(16) << dist(gen);
    }
    return oss.str();
}

std::string SessionAuthority::CreateSession(SessionMode mode,
                                            std::vector<std::string> capabilities,
                                            std::string machineIdentity,
                                            std::string userIdentity,
                                            std::chrono::minutes ttl,
                                            bool writeElevation) {
    SessionRecord record;
    record.token = GenerateToken();
    record.mode = mode;
    record.capabilities = std::move(capabilities);
    record.machineIdentity = std::move(machineIdentity);
    record.userIdentity = std::move(userIdentity);
    record.expiresAt = std::chrono::system_clock::now() + ttl;
    record.writeElevation = writeElevation;
    sessions_[record.token] = record;
    return record.token;
}

std::optional<SessionRecord> SessionAuthority::Validate(const std::string& token) const {
    const auto it = sessions_.find(token);
    if (it == sessions_.end()) {
        return std::nullopt;
    }
    if (std::chrono::system_clock::now() > it->second.expiresAt) {
        return std::nullopt;
    }
    return it->second;
}

Atlas::Common::Status SessionAuthority::Revoke(const std::string& token) {
    if (sessions_.erase(token) == 0) {
        return Atlas::Common::Status::Error("session not found");
    }
    return Atlas::Common::Status::Ok("session revoked");
}

Atlas::Common::Status SessionAuthority::Rotate(const std::string& token, std::chrono::minutes ttl, std::string* newToken) {
    const auto it = sessions_.find(token);
    if (it == sessions_.end()) {
        return Atlas::Common::Status::Error("session not found");
    }

    SessionRecord record = it->second;
    sessions_.erase(it);
    record.token = GenerateToken();
    record.expiresAt = std::chrono::system_clock::now() + ttl;
    sessions_[record.token] = record;
    if (newToken) {
        *newToken = record.token;
    }
    return Atlas::Common::Status::Ok("session rotated");
}

} // namespace Atlas::Security
