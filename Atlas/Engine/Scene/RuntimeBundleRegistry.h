#pragma once
#include <string>
#include <vector>
#include <unordered_map>
#include <functional>

namespace Atlas::Engine {

/// Phase 21D — Registry for runtime asset bundles: groups of pre-cooked assets
/// that can be streamed in and out as units for level streaming and DLC support.
class RuntimeBundleRegistry {
public:
    enum class BundleState { Unloaded, Loading, Loaded, Failed };

    struct AssetRef {
        std::string assetId;
        std::string assetType;
        std::string path;
    };

    struct BundleRecord {
        std::string bundleId;
        std::string name;
        std::string version;
        BundleState state{BundleState::Unloaded};
        std::vector<AssetRef> assets;
        size_t estimatedSizeBytes{0};
        bool required{false};
    };

    // Registration
    bool RegisterBundle(const std::string& bundleId,
                        const std::string& name,
                        const std::string& version,
                        bool required = false);
    bool UnregisterBundle(const std::string& bundleId);
    bool IsRegistered(const std::string& bundleId) const;
    int GetBundleCount() const { return static_cast<int>(m_bundles.size()); }

    // Asset management
    bool AddAsset(const std::string& bundleId, const AssetRef& asset);
    int GetAssetCount(const std::string& bundleId) const;

    // Load / unload
    bool LoadBundle(const std::string& bundleId);
    bool UnloadBundle(const std::string& bundleId);
    bool IsLoaded(const std::string& bundleId) const;
    int GetLoadedCount() const;
    std::vector<std::string> GetLoadedBundleIds() const;

    // Lookup
    const BundleRecord* GetBundle(const std::string& bundleId) const;
    std::vector<std::string> GetAllBundleIds() const;
    std::vector<BundleRecord> GetRequiredBundles() const;

    // Traversal
    void ForEach(const std::function<void(const BundleRecord&)>& fn) const;

    // Estimated size
    size_t GetTotalEstimatedSize() const;

    // Lifecycle
    void Clear();

    // Callbacks
    void SetOnBundleLoadedCallback(
        std::function<void(const std::string&)> cb);
    void SetOnBundleUnloadedCallback(
        std::function<void(const std::string&)> cb);

private:
    std::unordered_map<std::string, BundleRecord> m_bundles;
    std::function<void(const std::string&)> m_onLoaded;
    std::function<void(const std::string&)> m_onUnloaded;
};

} // namespace Atlas::Engine
