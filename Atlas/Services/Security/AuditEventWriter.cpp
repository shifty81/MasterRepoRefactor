#include "security/AuditEventWriter.h"

#include "common/Clock.h"
#include "common/TextUtil.h"

#include <filesystem>
#include <fstream>

namespace Atlas::Security {

AuditEventWriter::AuditEventWriter(std::filesystem::path auditDirectory)
    : auditDirectory_(std::move(auditDirectory)) {
}

bool AuditEventWriter::Write(const AuditRecord& record, std::filesystem::path* outPath) const {
    std::error_code ec;
    std::filesystem::create_directories(auditDirectory_, ec);
    if (ec) {
        return false;
    }

    const std::string day = record.timestampUtc.substr(0, 10);
    const auto filePath = auditDirectory_ / (day + "_audit.jsonl");
    std::ofstream out(filePath, std::ios::app | std::ios::binary);
    if (!out) {
        return false;
    }

    out << "{";
    out << "\"timestampUtc\":\"" << Atlas::Common::JsonEscape(record.timestampUtc) << "\",";
    out << "\"sessionId\":\"" << Atlas::Common::JsonEscape(record.sessionId) << "\",";
    out << "\"userIdentity\":\"" << Atlas::Common::JsonEscape(record.userIdentity) << "\",";
    out << "\"machineIdentity\":\"" << Atlas::Common::JsonEscape(record.machineIdentity) << "\",";
    out << "\"action\":\"" << Atlas::Common::JsonEscape(record.action) << "\",";
    out << "\"capability\":\"" << Atlas::Common::JsonEscape(record.capability) << "\",";
    out << "\"dryRun\":" << (record.dryRun ? "true" : "false") << ",";
    out << "\"success\":" << (record.success ? "true" : "false") << ",";
    out << "\"message\":\"" << Atlas::Common::JsonEscape(record.message) << "\",";
    out << "\"correlationId\":\"" << Atlas::Common::JsonEscape(record.correlationId) << "\",";
    out << "\"targetRoots\":[";
    for (std::size_t i = 0; i < record.targetRoots.size(); ++i) {
        if (i != 0) out << ',';
        out << "\"" << Atlas::Common::JsonEscape(record.targetRoots[i]) << "\"";
    }
    out << "]}" << '\n';

    if (outPath) {
        *outPath = filePath;
    }
    return true;
}

} // namespace Atlas::Security
