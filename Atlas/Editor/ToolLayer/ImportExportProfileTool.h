#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P23 Tool — Import and export profile management, format mapping, and batch transfer operations.
class ImportExportProfileTool : public ITool {
public:
    enum class TransferDirection { Import, Export, Bidirectional, Custom };
    enum class AssetFormat { FBX, USD, OBJ, GLTF, Alembic, PNG, EXR, Custom };
    enum class ProfileScope { Project, Asset, Material, Mesh, Animation, Texture, Custom };
    enum class BatchStatus { Idle, Running, Paused, Completed, Failed, Custom };

    struct ImportExportProfileDef {
        std::string profileId;
        std::string profileName;
        TransferDirection direction{TransferDirection::Import};
        AssetFormat format{AssetFormat::FBX};
        ProfileScope scope{ProfileScope::Asset};
        bool validateOnImport{true};
    };

    struct BatchTransferJob {
        std::string jobId;
        std::string profileId;
        BatchStatus status{BatchStatus::Idle};
        int totalItems{0};
        int completedItems{0};
        float progressPct{0.0f};
    };

    struct FormatMappingDef {
        std::string mappingId;
        AssetFormat srcFormat{AssetFormat::FBX};
        AssetFormat dstFormat{AssetFormat::USD};
        std::string conversionScript;
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "ImportExportProfileTool"; }
    bool IsActive() const override { return m_active; }

    std::string CreateProfile(const ImportExportProfileDef& def);
    bool DeleteProfile(const std::string& profileId);
    const ImportExportProfileDef* GetProfile(const std::string& profileId) const;
    std::vector<std::string> GetAllProfileIds() const;
    std::vector<std::string> GetProfilesByDirection(TransferDirection direction) const;
    std::vector<std::string> GetProfilesByFormat(AssetFormat format) const;
    std::string StartBatchJob(const std::string& profileId, const std::vector<std::string>& items);
    bool PauseBatchJob(const std::string& jobId);
    bool CancelBatchJob(const std::string& jobId);
    const BatchTransferJob* GetBatchJob(const std::string& jobId) const;
    std::vector<std::string> GetAllJobIds() const;
    std::vector<std::string> GetRunningJobs() const;
    std::vector<std::string> GetCompletedJobs() const;
    bool AddFormatMapping(const FormatMappingDef& mapping);
    bool RemoveFormatMapping(const std::string& mappingId);
    std::vector<std::string> GetMappingsForFormat(AssetFormat format) const;
    void Reset();

private:
    bool m_active{false};
    std::unordered_map<std::string, ImportExportProfileDef> m_profiles;
    std::unordered_map<std::string, BatchTransferJob> m_jobs;
    std::unordered_map<std::string, FormatMappingDef> m_mappings;
    int m_nextProfileIndex{0};
};

} // namespace Atlas::Editor
