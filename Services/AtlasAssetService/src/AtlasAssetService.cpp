// AtlasAssetService.cpp
#include "AtlasAssetService.h"

namespace Atlas::Services
{

void AtlasAssetService::initialise() {}
void AtlasAssetService::shutdown()   {}

ImportResult AtlasAssetService::importAsset(const ImportRequest& req)
{
    ImportResult r;
    if (req.sourcePath.empty()) { r.message = "Empty source path"; return r; }

    AssetMetadata meta;
    meta.assetId     = nextAssetId_++;
    meta.assetPath   = req.destinationPath.empty() ? req.sourcePath : req.destinationPath;
    meta.displayName = req.sourcePath;
    meta.type        = req.hint;
    meta.status      = req.dryRun ? AssetStatus::Pending : AssetStatus::Imported;
    assets_.push_back(meta);

    r.success = true;
    r.assetId = meta.assetId;
    r.message = req.dryRun ? "[dry-run] Import simulated." : "Asset imported.";
    return r;
}

ImportResult AtlasAssetService::reimportAsset(uint64_t assetId)
{
    ImportResult r;
    for (auto& a : assets_)
    {
        if (a.assetId != assetId) continue;
        a.status  = AssetStatus::Imported;
        r.success = true;
        r.assetId = assetId;
        r.message = "Asset re-imported.";
        return r;
    }
    r.message = "Asset not found.";
    return r;
}

bool AtlasAssetService::deleteAsset(uint64_t assetId)
{
    for (auto& a : assets_)
    {
        if (a.assetId != assetId) continue;
        a.status = AssetStatus::Deleted;
        return true;
    }
    return false;
}

std::optional<AssetMetadata> AtlasAssetService::findByPath(const std::string& path) const
{
    for (const auto& a : assets_)
        if (a.assetPath == path && a.status != AssetStatus::Deleted) return a;
    return std::nullopt;
}

std::optional<AssetMetadata> AtlasAssetService::findById(uint64_t id) const
{
    for (const auto& a : assets_)
        if (a.assetId == id) return a;
    return std::nullopt;
}

std::vector<AssetMetadata> AtlasAssetService::listAll() const
{
    std::vector<AssetMetadata> result;
    for (const auto& a : assets_)
        if (a.status != AssetStatus::Deleted) result.push_back(a);
    return result;
}

std::vector<AssetMetadata> AtlasAssetService::listByType(AssetType type) const
{
    std::vector<AssetMetadata> result;
    for (const auto& a : assets_)
        if (a.type == type && a.status != AssetStatus::Deleted) result.push_back(a);
    return result;
}

std::vector<uint64_t> AtlasAssetService::getDependencies(uint64_t assetId) const
{
    for (const auto& a : assets_)
        if (a.assetId == assetId) return a.dependencies;
    return {};
}

} // namespace Atlas::Services
