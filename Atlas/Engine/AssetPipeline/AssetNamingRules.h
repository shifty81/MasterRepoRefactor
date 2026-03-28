// AssetNamingRules.h
// Atlas Engine — asset naming conventions and path validation rules.

#pragma once
#include <string>
#include <vector>

namespace atlas::asset {

/// Expected category prefixes for each asset type.
struct AssetTypeRule
{
    std::string extension;    ///< file extension, e.g. ".fbx"
    std::string prefix;       ///< expected filename prefix, e.g. "SM_"
    std::string importDest;   ///< canonical destination folder, e.g. "Content/Meshes/"
    std::string description;
};

/// Central registry of naming/placement rules.
class AssetNamingRules
{
public:
    AssetNamingRules();

    /// Check whether a filename matches the expected prefix for its extension.
    bool ValidateName(const std::string& filename)   const;

    /// Check whether a destination path matches the canonical import destination.
    bool ValidatePath(const std::string& filename,
                      const std::string& destinationPath) const;

    const std::vector<AssetTypeRule>& GetRules() const { return m_rules; }

private:
    std::vector<AssetTypeRule> m_rules;
    void LoadDefaults();
};

} // namespace atlas::asset
