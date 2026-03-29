#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P14 Tool — Asset packaging with manifest, compression, validation, and extraction
class AssetPackagingTool : public ITool {
public:
    enum class PackageFormat { Pak, Zip, Bundle, Custom };
    enum class CompressionMode { None, LZ4, Zstd, Deflate };
    enum class ValidationLevel { None, Checksum, Full };

    struct AssetEntry {
        std::string assetId;
        std::string sourcePath;
        std::string packagePath;
        std::string checksum;
        long long sizeBytes{0};
        bool compressed{false};
    };

    struct PackageManifest {
        std::string manifestId;
        std::string packageName;
        PackageFormat format{PackageFormat::Pak};
        CompressionMode compression{CompressionMode::None};
        int version{1};
        std::vector<std::string> assetIds;
        long long totalSizeBytes{0};
    };

    struct PackagingJob {
        std::string jobId;
        std::string manifestId;
        std::string outputPath;
        ValidationLevel validation{ValidationLevel::Checksum};
        bool overwriteExisting{false};
        bool dryRun{false};
    };

    struct PackagingResult {
        std::string resultId;
        std::string jobId;
        bool success{false};
        int assetsProcessed{0};
        int assetsFailed{0};
        long long outputSizeBytes{0};
        std::vector<std::string> errors;
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "AssetPackagingTool"; }
    bool IsActive() const override { return m_active; }

    std::string CreatePackage(const std::string& name, PackageFormat format = PackageFormat::Pak);
    bool RemovePackage(const std::string& manifestId);
    bool SetPackageCompression(const std::string& manifestId, CompressionMode mode);
    bool SetPackageFormat(const std::string& manifestId, PackageFormat format);

    std::string AddAsset(const std::string& manifestId, const std::string& sourcePath, const std::string& packagePath);
    bool RemoveAsset(const std::string& manifestId, const std::string& assetId);
    bool UpdateAssetPath(const std::string& assetId, const std::string& newPath);

    PackagingResult BuildPackage(const std::string& manifestId, const std::string& outputPath);
    PackagingResult ValidatePackage(const std::string& packagePath, ValidationLevel level = ValidationLevel::Full) const;
    bool ExtractPackage(const std::string& packagePath, const std::string& outputDir) const;
    const PackageManifest* GetPackageInfo(const std::string& manifestId) const;

    std::string CreateJob(const std::string& manifestId, const std::string& outputPath);
    bool RunJob(const std::string& jobId);
    const PackagingResult* GetJobResult(const std::string& jobId) const;

    int GetPackageCount() const;
    std::vector<std::string> GetPackageIds() const;
    std::vector<std::string> GetAssetIds(const std::string& manifestId) const;
    const AssetEntry* GetAsset(const std::string& assetId) const;

    bool SaveManifest(const std::string& filePath) const;
    bool LoadManifest(const std::string& filePath);
    void ClearAll();

private:
    bool m_active{false};
    std::unordered_map<std::string, PackageManifest> m_manifests;
    std::unordered_map<std::string, AssetEntry> m_assets;
    std::unordered_map<std::string, PackagingJob> m_jobs;
    std::unordered_map<std::string, PackagingResult> m_results;
    int m_nextManifestIndex{0};
    int m_nextAssetIndex{0};
    int m_nextJobIndex{0};
};

} // namespace Atlas::Editor
