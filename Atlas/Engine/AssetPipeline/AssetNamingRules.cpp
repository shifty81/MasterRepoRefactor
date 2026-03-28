// AssetNamingRules.cpp
// Atlas Engine — asset naming conventions and path validation rules.

#include "AssetPipeline/AssetNamingRules.h"

#include <algorithm>

namespace atlas::asset {

AssetNamingRules::AssetNamingRules()
{
    LoadDefaults();
}

void AssetNamingRules::LoadDefaults()
{
    // Static mesh
    m_rules.push_back({ ".fbx",  "SM_",  "Content/Meshes/",    "Static Mesh" });
    m_rules.push_back({ ".gltf", "SM_",  "Content/Meshes/",    "Static Mesh (glTF)" });
    // Skinned mesh
    m_rules.push_back({ ".fbx",  "SK_",  "Content/Characters/","Skeletal Mesh" });
    // Texture
    m_rules.push_back({ ".png",  "T_",   "Content/Textures/",  "Texture" });
    m_rules.push_back({ ".tga",  "T_",   "Content/Textures/",  "Texture" });
    // Material
    m_rules.push_back({ ".mat",  "M_",   "Content/Materials/", "Material" });
    // Voxel material
    m_rules.push_back({ ".vmat", "VM_",  "Content/VoxelMaterials/", "Voxel Material" });
    // Audio
    m_rules.push_back({ ".wav",  "SFX_", "Content/Audio/SFX/", "Sound Effect" });
    m_rules.push_back({ ".ogg",  "MUS_", "Content/Audio/Music/","Music Track" });
    // Data / JSON
    m_rules.push_back({ ".json", "DA_",  "Data/Definitions/",  "Data Asset" });
    // Blueprint / script
    m_rules.push_back({ ".lua",  "BP_",  "Scripts/",           "Script" });
    // Icon
    m_rules.push_back({ ".png",  "ICO_", "Content/Icons/",     "Icon / Preview" });
}

bool AssetNamingRules::ValidateName(const std::string& filename) const
{
    // Find the last '.' to extract extension.
    auto dotPos = filename.rfind('.');
    if (dotPos == std::string::npos) return false;
    std::string ext = filename.substr(dotPos);

    // Find the basename (after last '/' or '\').
    auto slashPos = filename.find_last_of("/\\");
    std::string base = (slashPos == std::string::npos)
                       ? filename
                       : filename.substr(slashPos + 1);

    for (const auto& rule : m_rules)
    {
        if (rule.extension == ext)
        {
            if (base.size() >= rule.prefix.size() &&
                base.substr(0, rule.prefix.size()) == rule.prefix) return true;
        }
    }
    return false;
}

bool AssetNamingRules::ValidatePath(const std::string& filename,
                                     const std::string& destinationPath) const
{
    auto dotPos = filename.rfind('.');
    if (dotPos == std::string::npos) return false;
    std::string ext = filename.substr(dotPos);

    for (const auto& rule : m_rules)
    {
        if (rule.extension == ext)
        {
            // Check that destinationPath starts with (or equals) importDest.
            if (destinationPath.find(rule.importDest) != std::string::npos)
                return true;
        }
    }
    return false;
}

} // namespace atlas::asset
