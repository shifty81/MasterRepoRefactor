#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P23 Tool — Actor palette management, placement preview, and instance stamp operations.
class ActorPaletteTool : public ITool {
public:
    enum class PaletteCategory { Environment, Characters, Props, Effects, Lights, Volumes, Custom };
    enum class PlacementMode { Single, Grid, Scatter, Paint, Line, Custom };
    enum class SnapAxis { None, X, Y, Z, Surface, Custom };
    enum class StampMode { Replace, Additive, Subtract, Custom };

    struct PaletteActorDef {
        std::string actorDefId;
        std::string actorClass;
        PaletteCategory category{PaletteCategory::Props};
        std::string thumbnailPath;
    };

    struct PalettePlacementConfig {
        std::string configId;
        PlacementMode mode{PlacementMode::Single};
        SnapAxis snapAxis{SnapAxis::Surface};
        float spacing{100.0f};
        int maxInstances{1000};
    };

    struct StampBatchRecord {
        std::string batchId;
        std::string configId;
        int instanceCount{0};
        bool committed{false};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "ActorPaletteTool"; }
    bool IsActive() const override { return m_active; }

    bool RegisterActor(const PaletteActorDef& def);
    bool UnregisterActor(const std::string& actorDefId);
    const PaletteActorDef* GetActor(const std::string& actorDefId) const;
    std::vector<std::string> GetAllActorDefIds() const;
    std::vector<std::string> GetActorsByCategory(PaletteCategory category) const;
    std::string CreatePlacementConfig(const PalettePlacementConfig& config);
    bool DeletePlacementConfig(const std::string& configId);
    const PalettePlacementConfig* GetPlacementConfig(const std::string& configId) const;
    std::vector<std::string> GetAllConfigIds() const;
    bool SetPlacementMode(const std::string& configId, PlacementMode mode);
    bool SetSnapAxis(const std::string& configId, SnapAxis axis);
    std::string BeginStamp(const std::string& configId);
    bool CommitStamp(const std::string& batchId);
    bool CancelStamp(const std::string& batchId);
    const StampBatchRecord* GetStampBatch(const std::string& batchId) const;
    std::vector<std::string> GetAllBatchIds() const;
    std::vector<std::string> GetPendingBatches() const;
    void Reset();

private:
    bool m_active{false};
    std::unordered_map<std::string, PaletteActorDef> m_actors;
    std::unordered_map<std::string, PalettePlacementConfig> m_configs;
    std::unordered_map<std::string, StampBatchRecord> m_batches;
    int m_nextConfigIndex{0};
};

} // namespace Atlas::Editor
