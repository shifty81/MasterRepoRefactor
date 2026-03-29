#include "archive/ArchiveIntakeService.h"

#include "common/Clock.h"
#include "common/TextUtil.h"

#include <filesystem>
#include <fstream>
#include <sstream>

namespace Atlas::Archive {

bool ArchiveIntakeService::LoadPolicy(const std::filesystem::path& path) {
    const std::string json = Atlas::Common::ReadTextFile(path);
    if (json.empty()) {
        return false;
    }
    policy_.autoExtractZips = Atlas::Common::ExtractBool(json, "autoExtractZips", true);
    policy_.quarantine = Atlas::Common::ExtractBool(json, "quarantine", true);
    policy_.generateReports = Atlas::Common::ExtractBool(json, "generateReports", true);
    const auto allow = Atlas::Common::ExtractStringArray(json, "allowedRepoRootNames");
    if (!allow.empty()) {
        policy_.allowedRepoRootNames = allow;
    }
    return true;
}

std::string ArchiveIntakeService::HashFile(const std::filesystem::path& path) {
    std::ifstream in(path, std::ios::binary);
    constexpr std::uint64_t kOffset = 1469598103934665603ull;
    constexpr std::uint64_t kPrime = 1099511628211ull;
    std::uint64_t hash = kOffset;

    char buffer[4096];
    while (in.read(buffer, sizeof(buffer)) || in.gcount() > 0) {
        for (std::streamsize i = 0; i < in.gcount(); ++i) {
            hash ^= static_cast<unsigned char>(buffer[i]);
            hash *= kPrime;
        }
    }

    std::ostringstream oss;
    oss << std::hex << hash;
    return oss.str();
}

std::string ArchiveIntakeService::Classify(const std::filesystem::path& path) {
    const auto ext = Atlas::Common::ToLower(path.extension().string());
    if (ext == ".zip") return "promote_candidate";
    if (ext == ".txt" || ext == ".md" || ext == ".rtf") return "archive_only";
    if (ext == ".png" || ext == ".jpg" || ext == ".jpeg" || ext == ".webp") return "needs_review";
    if (ext == ".json" || ext == ".csv" || ext == ".yaml" || ext == ".yml") return "needs_review";
    return "reject";
}

bool ArchiveIntakeService::IsAllowedRepoRootName(const std::string& name) const {
    for (const auto& allowed : policy_.allowedRepoRootNames) {
        if (name == allowed) {
            return true;
        }
    }
    return false;
}

Atlas::Common::Status ArchiveIntakeService::ExtractZipPlaceholder(const std::filesystem::path& zipPath,
                                                                  const std::filesystem::path& quarantineDir) const {
    std::error_code ec;
    std::filesystem::create_directories(quarantineDir, ec);
    if (ec) {
        return Atlas::Common::Status::Error("failed to create quarantine directory");
    }

    std::ofstream note(quarantineDir / "EXTRACTION_REQUIRED.txt", std::ios::binary);
    note << "Zip extraction placeholder for: " << zipPath.string() << "\n";
    note << "Hook this point into your preferred zip library or platform unzip command broker tool.\n";
    return Atlas::Common::Status::Ok("quarantine placeholder created");
}

Atlas::Common::Status ArchiveIntakeService::Run(const std::filesystem::path& repoRoot,
                                                const std::filesystem::path& archiveRoot,
                                                IntakeRunResult* outResult) const {
    if (!std::filesystem::exists(repoRoot)) {
        return Atlas::Common::Status::Error("repo root does not exist");
    }

    std::error_code ec;
    const auto intakeDir = archiveRoot / "Intake";
    const auto auditDir = archiveRoot / "Audit";
    const auto quarantineRoot = archiveRoot / "Quarantine";
    std::filesystem::create_directories(intakeDir, ec);
    std::filesystem::create_directories(auditDir, ec);
    std::filesystem::create_directories(quarantineRoot, ec);
    if (ec) {
        return Atlas::Common::Status::Error("failed to create archive directories");
    }

    IntakeRunResult result;

    for (const auto& entry : std::filesystem::directory_iterator(repoRoot)) {
        const auto name = entry.path().filename().string();
        if (IsAllowedRepoRootName(name)) {
            continue;
        }
        if (entry.path().filename() == archiveRoot.filename()) {
            continue;
        }
        if (entry.is_directory()) {
            continue;
        }

        IntakeItem item;
        item.source = entry.path();
        item.hash = HashFile(entry.path());
        item.classification = Classify(entry.path());

        const auto copyName = item.hash + "_" + entry.path().filename().string();
        item.archiveCopy = intakeDir / copyName;
        std::filesystem::copy_file(entry.path(), item.archiveCopy,
                                   std::filesystem::copy_options::skip_existing, ec);
        if (ec) {
            return Atlas::Common::Status::Error("failed to archive root drop: " + entry.path().string());
        }

        if (policy_.quarantine && Atlas::Common::ToLower(entry.path().extension().string()) == ".zip") {
            item.quarantineDirectory = quarantineRoot / item.hash;
            auto extractStatus = ExtractZipPlaceholder(entry.path(), item.quarantineDirectory);
            if (!extractStatus.ok) {
                return extractStatus;
            }
        }

        result.items.push_back(item);
    }

    const std::string timestamp = Atlas::Common::UtcNowIso8601();
    result.manifestPath = auditDir / "archive_intake_manifest.json";
    {
        std::ofstream manifest(result.manifestPath, std::ios::binary);
        manifest << "{\n  \"timestampUtc\": \"" << timestamp << "\",\n  \"items\": [\n";
        for (std::size_t i = 0; i < result.items.size(); ++i) {
            const auto& item = result.items[i];
            manifest << "    {\"source\": \"" << Atlas::Common::JsonEscape(item.source.string()) << "\", "
                     << "\"hash\": \"" << Atlas::Common::JsonEscape(item.hash) << "\", "
                     << "\"classification\": \"" << Atlas::Common::JsonEscape(item.classification) << "\", "
                     << "\"archiveCopy\": \"" << Atlas::Common::JsonEscape(item.archiveCopy.string()) << "\", "
                     << "\"quarantineDirectory\": \"" << Atlas::Common::JsonEscape(item.quarantineDirectory.string()) << "\"}";
            if (i + 1 != result.items.size()) manifest << ',';
            manifest << "\n";
        }
        manifest << "  ]\n}\n";
    }

    result.reportPath = auditDir / "archive_audit_report.md";
    {
        std::ofstream report(result.reportPath, std::ios::binary);
        report << "# Archive Intake Report\n\n";
        report << "Timestamp: " << timestamp << "\n\n";
        if (result.items.empty()) {
            report << "No root-drop files detected.\n";
        } else {
            report << "| Source | Classification | Hash | Archive Copy |\n";
            report << "|---|---|---|---|\n";
            for (const auto& item : result.items) {
                report << "| " << item.source.filename().string() << " | " << item.classification << " | "
                       << item.hash << " | " << item.archiveCopy.string() << " |\n";
            }
        }
    }

    if (outResult) {
        *outResult = result;
    }
    return Atlas::Common::Status::Ok("archive intake completed");
}

} // namespace Atlas::Archive
