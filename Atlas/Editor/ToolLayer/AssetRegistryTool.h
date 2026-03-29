#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P19 Tool — Asset registry inspection, filter configuration, and dependency scanning.
class AssetRegistryTool : public ITool {
public:
    enum class AssetLoadingState { Unloaded, Loading, Loaded, Unloading, Error };
    enum class DependencyQueryType { Hard, Soft, EditorOnly, Game, All };
    enum class RegistryScanFlags { Sync, Async, Package, Deep, Redirectors, Custom };

    struct AssetFilterDef {
        std::string filterId;
        std::string name;
        std::vector<std::string> classFilter;
        std::vector<std::string> packageFilter;
        std::vector<std::string> tagFilter;
        std::vector<std::string> pathFilter;
        AssetLoadingState loadStateFilter{AssetLoadingState::Loaded};
    };

    struct AssetDependencyRecord {
        std::string depId;
        std::string sourceAsset;
        std::string targetAsset;
        DependencyQueryType queryType{DependencyQueryType::Hard};
        bool circular{false};
    };

    struct AssetScanResult {
        std::string scanId;
        std::string filterId;
        int assetsFound{0};
        int assetsLoaded{0};
        std::vector<std::string> errors;
        double elapsedMs{0.0};
        RegistryScanFlags scanFlags{RegistryScanFlags::Sync};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "AssetRegistryTool"; }
    bool IsActive() const override { return m_active; }

    std::string CreateFilter(const std::string& name);
    bool RemoveFilter(const std::string& filterId);
    const AssetFilterDef* GetFilter(const std::string& filterId) const;
    std::vector<std::string> GetAllFilterIds() const;
    bool SetClassFilter(const std::string& filterId, const std::vector<std::string>& classes);
    bool SetPackageFilter(const std::string& filterId, const std::vector<std::string>& packages);
    bool SetTagFilter(const std::string& filterId, const std::vector<std::string>& tags);
    bool SetPathFilter(const std::string& filterId, const std::vector<std::string>& paths);
    bool SetLoadStateFilter(const std::string& filterId, AssetLoadingState state);
    AssetScanResult ScanAssets(const std::string& filterId, RegistryScanFlags flags);
    bool ScanAssetsAsync(const std::string& filterId, const std::string& callbackId);
    bool CancelScan(const std::string& scanId);
    const AssetScanResult* GetScanResult(const std::string& scanId) const;
    std::vector<std::string> GetAllScanResults() const;
    std::vector<std::string> GetAssetsByFilter(const std::string& filterId) const;
    std::vector<AssetDependencyRecord> GetDependencies(const std::string& assetPath, DependencyQueryType queryType) const;
    std::vector<AssetDependencyRecord> GetReferencers(const std::string& assetPath, DependencyQueryType queryType) const;
    std::vector<AssetDependencyRecord> GetCircularDependencies(const std::string& assetPath) const;
    AssetLoadingState GetAssetLoadState(const std::string& assetPath) const;
    bool ForceLoad(const std::string& assetPath);
    bool ForceUnload(const std::string& assetPath);
    bool ValidateFilter(const std::string& filterId) const;
    bool ExportRegistry(const std::string& filePath) const;
    bool SaveFilters(const std::string& filePath) const;
    bool LoadFilters(const std::string& filePath);
    void ClearResults();
    void Reset();

private:
    bool m_active{false};
    std::unordered_map<std::string, AssetFilterDef> m_filters;
    std::unordered_map<std::string, AssetScanResult> m_scanResults;
    int m_nextFilterIndex{0};
    int m_nextScanIndex{0};
};

} // namespace Atlas::Editor
