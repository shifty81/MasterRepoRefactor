// AssetImportValidator.cpp
// Atlas Engine — validates asset files before they enter the content pipeline.

#include "AssetPipeline/AssetImportValidator.h"

namespace atlas::asset {

AssetImportValidator::AssetImportValidator(const AssetNamingRules& rules)
    : m_rules(rules)
{}

ImportValidationResult AssetImportValidator::Validate(
    const std::string& assetPath,
    const std::string& destinationPath) const
{
    ImportValidationResult result;
    result.assetPath = assetPath;
    result.passed    = true;

    // 1. Naming check
    if (!m_rules.ValidateName(assetPath))
    {
        result.issues.push_back({
            EImportIssueLevel::Warning,
            assetPath,
            "File name does not follow the expected prefix convention.",
            "Rename the file to include the correct prefix (e.g. SM_, T_, SFX_)."
        });
        // Warning only — import is still permitted.
    }

    // 2. Destination path check
    if (!destinationPath.empty() && !m_rules.ValidatePath(assetPath, destinationPath))
    {
        result.issues.push_back({
            EImportIssueLevel::Error,
            assetPath,
            "Destination path does not match the canonical import directory.",
            "Move the file to the correct content subdirectory."
        });
        result.passed = false;
    }

    // 3. Extension presence check
    if (assetPath.rfind('.') == std::string::npos)
    {
        result.issues.push_back({
            EImportIssueLevel::Error,
            assetPath,
            "File has no extension; type cannot be determined.",
            "Add the correct file extension before importing."
        });
        result.passed = false;
    }

    return result;
}

std::vector<ImportValidationResult> AssetImportValidator::ValidateBatch(
    const std::vector<std::pair<std::string, std::string>>& pathPairs) const
{
    std::vector<ImportValidationResult> results;
    results.reserve(pathPairs.size());
    for (const auto& [asset, dest] : pathPairs)
        results.push_back(Validate(asset, dest));
    return results;
}

bool AssetImportValidator::IsImportAllowed(
    const std::string& assetPath,
    const std::string& destinationPath) const
{
    return Validate(assetPath, destinationPath).passed;
}

} // namespace atlas::asset
