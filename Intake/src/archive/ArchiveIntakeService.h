#pragma once

#include "common/Status.h"

#include <filesystem>
#include <string>
#include <vector>

namespace Atlas::Archive {

struct ArchiveIntakePolicy {
    bool autoExtractZips{true};
    bool quarantine{true};
    bool generateReports{true};
    std::vector<std::string> allowedRepoRootNames{
        ".git", ".github", ".gitignore", "Atlas", "Docs", "Config", "Tests", "Scripts", "README.md", "CMakeLists.txt"
    };
};

struct IntakeItem {
    std::filesystem::path source;
    std::string hash;
    std::string classification;
    std::filesystem::path archiveCopy;
    std::filesystem::path quarantineDirectory;
};

struct IntakeRunResult {
    std::vector<IntakeItem> items;
    std::filesystem::path manifestPath;
    std::filesystem::path reportPath;
};

class ArchiveIntakeService {
public:
    bool LoadPolicy(const std::filesystem::path& path);
    Atlas::Common::Status Run(const std::filesystem::path& repoRoot,
                              const std::filesystem::path& archiveRoot,
                              IntakeRunResult* outResult) const;

private:
    ArchiveIntakePolicy policy_;

    static std::string HashFile(const std::filesystem::path& path);
    static std::string Classify(const std::filesystem::path& path);
    bool IsAllowedRepoRootName(const std::string& name) const;
    Atlas::Common::Status ExtractZipPlaceholder(const std::filesystem::path& zipPath,
                                                const std::filesystem::path& quarantineDir) const;
};

} // namespace Atlas::Archive
