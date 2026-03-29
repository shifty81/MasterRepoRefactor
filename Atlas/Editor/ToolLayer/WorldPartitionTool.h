#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P19 Tool — World partition streaming grid configuration, data layer management, and HLOD setup.
class WorldPartitionTool : public ITool {
public:
    enum class StreamingSourceType { Player, Camera, Volume, Trigger, Custom };
    enum class HLODLayerType { MeshMerge, Instancing, Approximation, Custom };
    enum class PartitionState { Loaded, Loading, Unloaded, Unloading, Error, Pending };

    struct StreamingGridConfig {
        std::string gridId;
        std::string name;
        float cellSize{12800.0f};
        float loadingRadius{25600.0f};
        float unloadingRadius{30000.0f};
        float serverRadius{20000.0f};
        int priority{0};
    };

    struct HLODLayerDef {
        std::string hlodId;
        std::string name;
        HLODLayerType hlodType{HLODLayerType::MeshMerge};
        float minVisibilitySizeScaled{0.01f};
        int fillMode{0};
        bool enabled{true};
    };

    struct WorldPartitionCell {
        std::string cellId;
        std::string gridId;
        std::vector<float> bounds;
        PartitionState state{PartitionState::Unloaded};
        std::vector<std::string> dataLayers;
        std::vector<std::string> actors;
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "WorldPartitionTool"; }
    bool IsActive() const override { return m_active; }

    bool SetGridConfig(const StreamingGridConfig& config);
    const StreamingGridConfig* GetGridConfig(const std::string& gridId) const;
    bool SetCellSize(const std::string& gridId, float cellSize);
    bool SetLoadingRadius(const std::string& gridId, float radius);
    bool SetUnloadingRadius(const std::string& gridId, float radius);
    std::string CreateHLODLayer(const std::string& name, HLODLayerType type);
    bool RemoveHLODLayer(const std::string& hlodId);
    bool SetHLODType(const std::string& hlodId, HLODLayerType type);
    bool EnableHLOD(const std::string& hlodId);
    bool DisableHLOD(const std::string& hlodId);
    bool AddStreamingSource(const std::string& sourceId, StreamingSourceType type);
    bool RemoveStreamingSource(const std::string& sourceId);
    bool ForceLoadCell(const std::string& cellId);
    bool ForceUnloadCell(const std::string& cellId);
    PartitionState GetCellState(const std::string& cellId) const;
    std::vector<std::string> GetAllCells() const;
    std::vector<std::string> GetCellsByState(PartitionState state) const;
    std::vector<std::string> GetCellsByDataLayer(const std::string& layerId) const;
    bool SetPartitionEnabled(bool enabled);
    bool EnableStreamingDebug(bool enabled);
    std::vector<float> GetLoadedBounds() const;
    bool PreviewPartition();
    bool ValidatePartition() const;
    bool SaveConfig(const std::string& filePath) const;
    bool LoadConfig(const std::string& filePath);
    void Reset();

private:
    bool m_active{false};
    std::unordered_map<std::string, StreamingGridConfig> m_grids;
    std::unordered_map<std::string, HLODLayerDef> m_hlodLayers;
    std::unordered_map<std::string, WorldPartitionCell> m_cells;
    int m_nextHLODIndex{0};
};

} // namespace Atlas::Editor
