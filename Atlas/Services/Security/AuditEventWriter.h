#pragma once

#include <filesystem>
#include <string>
#include <vector>

namespace Atlas::Security {

struct AuditRecord {
    std::string timestampUtc;
    std::string sessionId;
    std::string userIdentity;
    std::string machineIdentity;
    std::string action;
    std::string capability;
    std::vector<std::string> targetRoots;
    bool dryRun{true};
    bool success{false};
    std::string message;
    std::string correlationId;
};

class AuditEventWriter {
public:
    explicit AuditEventWriter(std::filesystem::path auditDirectory);
    bool Write(const AuditRecord& record, std::filesystem::path* outPath = nullptr) const;

private:
    std::filesystem::path auditDirectory_;
};

} // namespace Atlas::Security
