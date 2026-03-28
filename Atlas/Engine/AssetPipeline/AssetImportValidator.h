// AssetImportValidator.h
// Atlas Engine — validates asset files before they enter the content pipeline.

#pragma once
#include "AssetPipeline/AssetNamingRules.h"

#include <string>
#include <vector>

namespace atlas::asset {

enum class EImportIssueLevel : uint8_t { Warning, Error };

struct ImportIssue
{
    EImportIssueLevel level     = EImportIssueLevel::Error;
    std::string       assetPath;
    std::string       message;
    std::string       suggestion;
};

struct ImportValidationResult
{
    std::string             assetPath;
    bool                    passed = false;
    std::vector<ImportIssue> issues;
};

class AssetImportValidator
{
public:
    explicit AssetImportValidator(const AssetNamingRules& rules);

    /// Validate a single asset file before import.
    ImportValidationResult Validate(const std::string& assetPath,
                                    const std::string& destinationPath) const;

    /// Batch validate multiple files; returns combined results.
    std::vector<ImportValidationResult> ValidateBatch(
        const std::vector<std::pair<std::string, std::string>>& pathPairs) const;

    /// Quick check — true only if there are no errors (warnings are allowed).
    bool IsImportAllowed(const std::string& assetPath,
                         const std::string& destinationPath) const;

private:
    const AssetNamingRules& m_rules;
};

} // namespace atlas::asset
