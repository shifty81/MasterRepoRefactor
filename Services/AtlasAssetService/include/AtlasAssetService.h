// AtlasAssetService.h
// Asset service — import, export, metadata, and dependency tracking.

#pragma once
#include <cstdint>
#include <string>
#include <vector>
#include <optional>

namespace Atlas::Services
{

enum class AssetType : uint8_t
{
    Mesh, Texture, Material, Sound, Script, DataTable, Blueprint, World, Unknown
};

enum class AssetStatus : uint8_t
{
    Pending, Imported, Failed, Reimporting, Deleted
};

struct AssetMetadata
{
    uint64_t    assetId       = 0;
    std::string assetPath;
    std::string displayName;
    AssetType   type          = AssetType::Unknown;
    AssetStatus status        = AssetStatus::Pending;
    uint64_t    fileSizeBytes = 0;
    std::string importedAt;
    std::vector<uint64_t> dependencies;
};

struct ImportRequest
{
    std::string sourcePath;
    std::string destinationPath;
    AssetType   hint          = AssetType::Unknown;
    bool        overwrite     = false;
    bool        dryRun        = true;
};

struct ImportResult
{
    bool        success  = false;
    uint64_t    assetId  = 0;
    std::string message;
};

class AtlasAssetService
{
public:
    AtlasAssetService()  = default;
    ~AtlasAssetService() = default;

    void initialise();
    void shutdown();

    ImportResult importAsset(const ImportRequest& request);
    ImportResult reimportAsset(uint64_t assetId);
    bool         deleteAsset(uint64_t assetId);

    std::optional<AssetMetadata> findByPath(const std::string& path) const;
    std::optional<AssetMetadata> findById(uint64_t assetId) const;
    std::vector<AssetMetadata>   listAll() const;
    std::vector<AssetMetadata>   listByType(AssetType type) const;
    std::vector<uint64_t>        getDependencies(uint64_t assetId) const;

private:
    std::vector<AssetMetadata> assets_;
    uint64_t nextAssetId_ = 1;
};

} // namespace Atlas::Services
