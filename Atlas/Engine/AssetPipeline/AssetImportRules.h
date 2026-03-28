// AssetImportRules.h
// Atlas Engine AssetPipeline — naming rules lock, import destination mapping,
// voxel/material standards, icon/preview generation rules, validation checks.

#pragma once
#include <functional>
#include <optional>
#include <regex>
#include <string>
#include <vector>

namespace atlas::asset {

// ---------------------------------------------------------------------------
// Naming rule definition
// ---------------------------------------------------------------------------

enum class ENamingTarget : uint8_t
{
    Asset,         ///< any asset file
    Texture,
    Mesh,
    VoxelMaterial,
    Module,
    Structure,
    Sound,
    Prefab,
    DataRecord,
    Icon,
};

struct NamingRule
{
    std::string   ruleId;
    ENamingTarget target         = ENamingTarget::Asset;
    std::string   regexPattern;   ///< must match this regex
    std::string   prefix;         ///< required prefix (e.g. "T_" for textures)
    std::string   suffix;         ///< required suffix (e.g. "_D" for diffuse)
    std::string   allowedChars;   ///< e.g. "a-z0-9_"
    bool          isCaseSensitive = false;
    bool          isLocked        = false;  ///< locked = no runtime override
    std::string   description;
};

// ---------------------------------------------------------------------------
// Import destination rule
// ---------------------------------------------------------------------------

struct ImportDestination
{
    std::string   destId;
    ENamingTarget targetType;
    std::string   basePath;         ///< e.g. "Assets/Textures/UI/"
    std::string   fileExtension;    ///< e.g. ".png"
    bool          autoSubfolder    = false;  ///< auto-create category subdir
    std::string   subfolderKey;     ///< field to use as subfolder name
};

// ---------------------------------------------------------------------------
// Voxel material standard
// ---------------------------------------------------------------------------

struct VoxelMaterialStandard
{
    std::string materialId;
    std::string displayName;
    std::string atlasRegion;       ///< e.g. "metal_01" within texture atlas
    bool        isDestructible   = true;
    float       hardness         = 1.0f;  ///< 0–10 scale
    float       density          = 1.0f;  ///< kg/m³ ratio
    bool        isTransparent    = false;
    std::string category;          ///< "metal", "rock", "organic", "tech"
};

// ---------------------------------------------------------------------------
// Icon/preview generation rule
// ---------------------------------------------------------------------------

struct IconGenerationRule
{
    std::string   ruleId;
    ENamingTarget targetType;
    std::string   outputSuffix;    ///< appended to asset name e.g. "_icon"
    std::string   outputFormat;    ///< "png", "jpg"
    uint32_t      width          = 64;
    uint32_t      height         = 64;
    bool          autoGenerate   = true;   ///< trigger generation on import
    std::string   backgroundColor = "#000000";
};

// ---------------------------------------------------------------------------
// Import validation result
// ---------------------------------------------------------------------------

struct ImportValidationResult
{
    std::string             assetPath;
    bool                    passed       = true;
    std::vector<std::string> errors;
    std::vector<std::string> warnings;
};

// ---------------------------------------------------------------------------
// AssetImportRules
// ---------------------------------------------------------------------------

class AssetImportRules
{
public:
    bool Initialize();
    void Shutdown();

    // ---- naming rules --------------------------------------------------
    void RegisterNamingRule  (const NamingRule& rule);
    bool LockNamingRule      (const std::string& ruleId);
    bool UnlockNamingRule    (const std::string& ruleId);
    bool HasNamingRule       (const std::string& ruleId) const;
    std::optional<NamingRule> FindNamingRule(const std::string& ruleId) const;
    std::vector<NamingRule>   ListNamingRules(ENamingTarget target) const;
    bool                      ValidateName   (const std::string& name,
                                               ENamingTarget target) const;
    std::string               SuggestName    (const std::string& base,
                                               ENamingTarget target) const;

    // ---- import destinations -------------------------------------------
    void  RegisterDestination(const ImportDestination& dest);
    bool  HasDestination     (const std::string& destId) const;
    std::optional<ImportDestination> FindDestination(
        const std::string& destId) const;
    std::string              GetDestinationPath(ENamingTarget target,
                                                  const std::string& subfolder = "") const;

    // ---- voxel material standards --------------------------------------
    void RegisterVoxelMaterial  (const VoxelMaterialStandard& mat);
    bool HasVoxelMaterial       (const std::string& materialId) const;
    std::optional<VoxelMaterialStandard> FindVoxelMaterial(
        const std::string& materialId) const;
    std::vector<VoxelMaterialStandard> ListVoxelMaterials(
        const std::string& category = "") const;
    void RegisterDefaultVoxelMaterials();

    // ---- icon/preview rules --------------------------------------------
    void RegisterIconRule   (const IconGenerationRule& rule);
    bool HasIconRule        (ENamingTarget target) const;
    std::optional<IconGenerationRule> GetIconRule(ENamingTarget target) const;
    std::string             GetIconPath(const std::string& assetName,
                                         ENamingTarget target) const;

    // ---- import validation checks ------------------------------------
    ImportValidationResult ValidateImport (const std::string& assetPath,
                                            ENamingTarget target) const;
    bool                   PassesAllChecks(const std::string& assetPath,
                                            ENamingTarget target) const;

    // ---- register all defaults ----------------------------------------
    void RegisterDefaultRules();

    size_t NamingRuleCount()   const { return m_namingRules.size(); }
    size_t DestinationCount()  const { return m_destinations.size(); }
    size_t VoxelMatCount()     const { return m_voxelMaterials.size(); }
    size_t IconRuleCount()     const { return m_iconRules.size(); }

private:
    std::vector<NamingRule>            m_namingRules;
    std::vector<ImportDestination>     m_destinations;
    std::vector<VoxelMaterialStandard> m_voxelMaterials;
    std::vector<IconGenerationRule>    m_iconRules;

    NamingRule* GetMutableRule(const std::string& ruleId);
};

} // namespace atlas::asset
