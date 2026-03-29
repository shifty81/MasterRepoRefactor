#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P24 Tool — Asset bundle composition, dependency packaging, and incremental patch generation.
class AssetBundleComposerTool : public ITool {
public:
    enum class BundleTargetPlatform { PC, Console, Mobile, VR, Server, Custom };
    enum class BundleCompressionMode { None, LZ4, Zlib, Oodle, Brotli, Custom };
    enum class PatchStrategy { Full, Incremental, Delta, Signature, Custom };
    enum class BundleManifestState { Draft, Building, Ready, Shipping, Deprecated, Custom };

    struct AssetBundleDef {
        std::string bundleId;
        std::string bundleName;
        BundleTargetPlatform platform{BundleTargetPlatform::PC};
        BundleCompressionMode compression{BundleCompressionMode::LZ4};
        PatchStrategy patchStrategy{PatchStrategy::Incremental};
        std::vector<std::string> assetIds;
        BundleManifestState state{BundleManifestState::Draft};
    };

    struct BundlePatchRecord {
        std::string patchId;
        std::string bundleId;
        PatchStrategy strategy{PatchStrategy::Incremental};
        std::string baseVersion;
        std::string targetVersion;
        long long patchSizeBytes{0};
        bool validated{false};
    };

    struct BundleManifestEntry {
        std::string manifestId;
        std::string bundleId;
        std::string manifestPath;
        BundleManifestState state{BundleManifestState::Draft};
        int assetCount{0};
        long long totalSizeBytes{0};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "AssetBundleComposerTool"; }
    bool IsActive() const override { return m_active; }

    std::string CreateBundle(const AssetBundleDef& def);
    bool DeleteBundle(const std::string& bundleId);
    const AssetBundleDef* GetBundle(const std::string& bundleId) const;
    std::vector<std::string> GetAllBundleIds() const;
    std::vector<std::string> GetBundlesByPlatform(BundleTargetPlatform platform) const;
    bool AddAssetToBundle(const std::string& bundleId, const std::string& assetId);
    bool RemoveAssetFromBundle(const std::string& bundleId, const std::string& assetId);
    std::vector<std::string> GetAssetsInBundle(const std::string& bundleId) const;
    std::string CreatePatch(const BundlePatchRecord& patch);
    bool DeletePatch(const std::string& patchId);
    const BundlePatchRecord* GetPatch(const std::string& patchId) const;
    std::vector<std::string> GetPatchesByBundle(const std::string& bundleId) const;
    bool ValidatePatch(const std::string& patchId);
    std::string BuildManifest(const std::string& bundleId);
    const BundleManifestEntry* GetManifest(const std::string& manifestId) const;
    std::vector<std::string> GetManifestsByState(BundleManifestState state) const;
    std::vector<std::string> GetAllManifestIds() const;
    bool FinalizeBundle(const std::string& bundleId);
    void Reset();

private:
    bool m_active{false};
    std::unordered_map<std::string, AssetBundleDef> m_bundles;
    std::unordered_map<std::string, BundlePatchRecord> m_patches;
    std::unordered_map<std::string, BundleManifestEntry> m_manifests;
};

} // namespace Atlas::Editor
