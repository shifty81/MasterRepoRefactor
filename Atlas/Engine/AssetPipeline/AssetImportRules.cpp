// AssetImportRules.cpp
// Atlas Engine AssetPipeline — asset import rules implementation.

#include "AssetPipeline/AssetImportRules.h"

#include <algorithm>

namespace atlas::asset {

bool AssetImportRules::Initialize() { return true; }
void AssetImportRules::Shutdown()
{
    m_namingRules.clear();
    m_destinations.clear();
    m_voxelMaterials.clear();
    m_iconRules.clear();
}

// ---- naming rules ----------------------------------------------------------

void AssetImportRules::RegisterNamingRule(const NamingRule& rule)
{
    for (auto& r : m_namingRules)
        if (r.ruleId == rule.ruleId) { if (!r.isLocked) r = rule; return; }
    m_namingRules.push_back(rule);
}

bool AssetImportRules::LockNamingRule(const std::string& ruleId)
{
    NamingRule* r = GetMutableRule(ruleId);
    if (!r) return false;
    r->isLocked = true;
    return true;
}

bool AssetImportRules::UnlockNamingRule(const std::string& ruleId)
{
    NamingRule* r = GetMutableRule(ruleId);
    if (!r) return false;
    r->isLocked = false;
    return true;
}

bool AssetImportRules::HasNamingRule(const std::string& ruleId) const
{
    return FindNamingRule(ruleId).has_value();
}

std::optional<NamingRule> AssetImportRules::FindNamingRule(
    const std::string& ruleId) const
{
    for (const auto& r : m_namingRules)
        if (r.ruleId == ruleId) return r;
    return std::nullopt;
}

std::vector<NamingRule> AssetImportRules::ListNamingRules(
    ENamingTarget target) const
{
    std::vector<NamingRule> result;
    for (const auto& r : m_namingRules)
        if (r.target == target) result.push_back(r);
    return result;
}

bool AssetImportRules::ValidateName(const std::string& name,
                                       ENamingTarget target) const
{
    for (const auto& r : m_namingRules)
    {
        if (r.target != target) continue;
        if (!r.prefix.empty() && name.find(r.prefix) != 0) return false;
        if (!r.suffix.empty())
        {
            if (name.size() < r.suffix.size()) return false;
            if (name.substr(name.size() - r.suffix.size()) != r.suffix)
                return false;
        }
        if (!r.regexPattern.empty())
        {
            std::regex rx(r.regexPattern,
                           r.isCaseSensitive ? std::regex::ECMAScript
                                             : std::regex::ECMAScript | std::regex::icase);
            if (!std::regex_match(name, rx)) return false;
        }
    }
    return true;
}

std::string AssetImportRules::SuggestName(const std::string& base,
                                             ENamingTarget target) const
{
    auto rules = ListNamingRules(target);
    std::string name = base;
    for (const auto& r : rules)
    {
        if (!r.prefix.empty() && name.find(r.prefix) != 0)
            name = r.prefix + name;
        if (!r.suffix.empty() &&
            (name.size() < r.suffix.size() ||
             name.substr(name.size() - r.suffix.size()) != r.suffix))
            name = name + r.suffix;
    }
    return name;
}

// ---- destinations ----------------------------------------------------------

void AssetImportRules::RegisterDestination(const ImportDestination& dest)
{
    for (auto& d : m_destinations)
        if (d.destId == dest.destId) { d = dest; return; }
    m_destinations.push_back(dest);
}

bool AssetImportRules::HasDestination(const std::string& destId) const
{
    return FindDestination(destId).has_value();
}

std::optional<ImportDestination> AssetImportRules::FindDestination(
    const std::string& destId) const
{
    for (const auto& d : m_destinations)
        if (d.destId == destId) return d;
    return std::nullopt;
}

std::string AssetImportRules::GetDestinationPath(
    ENamingTarget target, const std::string& subfolder) const
{
    for (const auto& d : m_destinations)
    {
        if (d.targetType == target)
        {
            return d.basePath + (subfolder.empty() ? "" : subfolder + "/");
        }
    }
    return "Assets/Unknown/";
}

// ---- voxel materials -------------------------------------------------------

void AssetImportRules::RegisterVoxelMaterial(
    const VoxelMaterialStandard& mat)
{
    for (auto& m : m_voxelMaterials)
        if (m.materialId == mat.materialId) { m = mat; return; }
    m_voxelMaterials.push_back(mat);
}

bool AssetImportRules::HasVoxelMaterial(const std::string& materialId) const
{
    return FindVoxelMaterial(materialId).has_value();
}

std::optional<VoxelMaterialStandard> AssetImportRules::FindVoxelMaterial(
    const std::string& materialId) const
{
    for (const auto& m : m_voxelMaterials)
        if (m.materialId == materialId) return m;
    return std::nullopt;
}

std::vector<VoxelMaterialStandard> AssetImportRules::ListVoxelMaterials(
    const std::string& category) const
{
    if (category.empty()) return m_voxelMaterials;
    std::vector<VoxelMaterialStandard> result;
    for (const auto& m : m_voxelMaterials)
        if (m.category == category) result.push_back(m);
    return result;
}

void AssetImportRules::RegisterDefaultVoxelMaterials()
{
    auto add = [this](const char* id, const char* name, const char* cat,
                       float hardness, float density, bool transparent = false)
    {
        VoxelMaterialStandard m;
        m.materialId    = id;
        m.displayName   = name;
        m.category      = cat;
        m.hardness      = hardness;
        m.density       = density;
        m.isTransparent = transparent;
        m.atlasRegion   = id;
        RegisterVoxelMaterial(m);
    };

    add("rock_granite",    "Granite Rock",        "rock",    5.0f, 2.7f);
    add("rock_basalt",     "Basalt Rock",          "rock",    4.5f, 3.0f);
    add("metal_steel",     "Steel",                "metal",   8.0f, 7.8f);
    add("metal_titanium",  "Titanium",             "metal",   9.0f, 4.5f);
    add("metal_copper",    "Copper",               "metal",   3.0f, 8.9f);
    add("organic_dirt",    "Dirt",                 "organic", 1.0f, 1.6f);
    add("organic_ice",     "Ice",                  "organic", 2.0f, 0.9f, true);
    add("tech_circuit",    "Circuit Panel",        "tech",    4.0f, 2.0f);
    add("tech_hull",       "Reinforced Hull",      "tech",    7.0f, 5.5f);
    add("energy_crystal",  "Energy Crystal",       "energy",  6.0f, 2.2f, true);
}

// ---- icon rules ------------------------------------------------------------

void AssetImportRules::RegisterIconRule(const IconGenerationRule& rule)
{
    for (auto& r : m_iconRules)
        if (r.targetType == rule.targetType) { r = rule; return; }
    m_iconRules.push_back(rule);
}

bool AssetImportRules::HasIconRule(ENamingTarget target) const
{
    return GetIconRule(target).has_value();
}

std::optional<IconGenerationRule> AssetImportRules::GetIconRule(
    ENamingTarget target) const
{
    for (const auto& r : m_iconRules)
        if (r.targetType == target) return r;
    return std::nullopt;
}

std::string AssetImportRules::GetIconPath(const std::string& assetName,
                                             ENamingTarget target) const
{
    std::string suffix = "_icon";
    std::string format = ".png";
    auto rule = GetIconRule(target);
    if (rule) { suffix = rule->outputSuffix; format = "." + rule->outputFormat; }
    return "Assets/Icons/" + assetName + suffix + format;
}

// ---- import validation checks ---------------------------------------------

ImportValidationResult AssetImportRules::ValidateImport(
    const std::string& assetPath, ENamingTarget target) const
{
    ImportValidationResult result;
    result.assetPath = assetPath;
    result.passed    = true;

    // Extract filename from path.
    auto slash = assetPath.rfind('/');
    std::string name = (slash == std::string::npos)
                       ? assetPath : assetPath.substr(slash + 1);

    // Remove extension.
    auto dot = name.rfind('.');
    std::string nameNoExt = (dot == std::string::npos) ? name : name.substr(0, dot);

    if (!ValidateName(nameNoExt, target))
    {
        result.passed = false;
        result.errors.push_back("Name '" + nameNoExt + "' violates naming rules for type "
                                + std::to_string(static_cast<int>(target)));
    }

    if (assetPath.empty())
    {
        result.passed = false;
        result.errors.push_back("Empty asset path");
    }

    return result;
}

bool AssetImportRules::PassesAllChecks(const std::string& assetPath,
                                         ENamingTarget target) const
{
    return ValidateImport(assetPath, target).passed;
}

void AssetImportRules::RegisterDefaultRules()
{
    // Textures: T_ prefix.
    NamingRule texRule;
    texRule.ruleId = "texture_prefix"; texRule.target = ENamingTarget::Texture;
    texRule.prefix = "T_"; texRule.description = "Textures must be prefixed T_";
    RegisterNamingRule(texRule);

    // Meshes: SM_ prefix (static mesh).
    NamingRule meshRule;
    meshRule.ruleId = "mesh_prefix"; meshRule.target = ENamingTarget::Mesh;
    meshRule.prefix = "SM_"; meshRule.description = "Meshes must be prefixed SM_";
    RegisterNamingRule(meshRule);

    // Prefabs: PF_ prefix.
    NamingRule prefabRule;
    prefabRule.ruleId = "prefab_prefix"; prefabRule.target = ENamingTarget::Prefab;
    prefabRule.prefix = "PF_";
    RegisterNamingRule(prefabRule);

    // Icons: ICO_ prefix.
    NamingRule iconRule;
    iconRule.ruleId = "icon_prefix"; iconRule.target = ENamingTarget::Icon;
    iconRule.prefix = "ICO_";
    RegisterNamingRule(iconRule);

    // Import destinations.
    auto addDest = [this](const char* id, ENamingTarget t, const char* path, const char* ext)
    {
        ImportDestination d;
        d.destId = id; d.targetType = t; d.basePath = path; d.fileExtension = ext;
        RegisterDestination(d);
    };
    addDest("textures",   ENamingTarget::Texture,       "Assets/Textures/",       ".png");
    addDest("meshes",     ENamingTarget::Mesh,           "Assets/Meshes/",         ".fbx");
    addDest("sounds",     ENamingTarget::Sound,          "Assets/Audio/",          ".ogg");
    addDest("prefabs",    ENamingTarget::Prefab,         "Assets/Prefabs/",        ".pfb");
    addDest("modules",    ENamingTarget::Module,         "Assets/Modules/",        ".mod");
    addDest("structures", ENamingTarget::Structure,      "Assets/Structures/",     ".str");
    addDest("icons",      ENamingTarget::Icon,           "Assets/Icons/",          ".png");
    addDest("voxelmats",  ENamingTarget::VoxelMaterial,  "Assets/VoxelMaterials/", ".vmat");

    // Icon generation rules.
    auto addIcon = [this](ENamingTarget t, const char* suffix, uint32_t sz)
    {
        IconGenerationRule r;
        r.ruleId = suffix; r.targetType = t;
        r.outputSuffix = suffix; r.outputFormat = "png";
        r.width = sz; r.height = sz;
        RegisterIconRule(r);
    };
    addIcon(ENamingTarget::Module,    "_icon", 128);
    addIcon(ENamingTarget::Prefab,    "_icon", 64);
    addIcon(ENamingTarget::Mesh,      "_preview", 256);
    addIcon(ENamingTarget::Texture,   "_thumb", 64);
}

NamingRule* AssetImportRules::GetMutableRule(const std::string& ruleId)
{
    for (auto& r : m_namingRules)
        if (r.ruleId == ruleId) return &r;
    return nullptr;
}

} // namespace atlas::asset
