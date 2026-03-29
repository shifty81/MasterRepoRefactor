#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P16 Tool — Level streaming tile authoring, load/unload trigger management, and streaming budget control.
class LevelStreamingTool : public ITool {
public:
    enum class StreamingMethod { Distance, Trigger, Manual, Predictive, Priority };
    enum class StreamingState { Unloaded, Loading, Loaded, Unloading, Error };
    enum class LevelTileType { Persistent, Streaming, Overlay, Always, Conditional };

    struct StreamingTile {
        std::string tileId;
        std::string name;
        LevelTileType tileType{LevelTileType::Streaming};
        std::string levelPath;
        float loadDistance{5000.0f};
        float unloadDistance{6000.0f};
        int priority{0};
        StreamingMethod streamingMethod{StreamingMethod::Distance};
        std::vector<float> boundMin;
        std::vector<float> boundMax;
    };

    struct StreamingTrigger {
        std::string triggerId;
        std::string name;
        std::string tileId;
        std::string shape{"Box"};
        std::vector<float> extents;
        std::vector<float> offset;
    };

    struct StreamingBudget {
        int maxSimultaneousLoads{4};
        float maxMemoryMB{2048.0f};
        float loadTimeBudgetMs{16.0f};
        std::string priorityPolicy{"Distance"};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "LevelStreamingTool"; }
    bool IsActive() const override { return m_active; }

    std::string CreateTile(const std::string& name, const std::string& levelPath);
    bool RemoveTile(const std::string& tileId);
    std::string CreateTrigger(const std::string& name, const std::string& tileId);
    bool RemoveTrigger(const std::string& triggerId);
    bool SetStreamingMethod(const std::string& tileId, StreamingMethod method);
    bool SetLoadDistances(const std::string& tileId, float loadDist, float unloadDist);
    bool SetTilePriority(const std::string& tileId, int priority);
    bool SetStreamingBudget(const StreamingBudget& budget);
    bool ForceLoadTile(const std::string& tileId);
    bool ForceUnloadTile(const std::string& tileId);
    const StreamingTile* GetTile(const std::string& tileId) const;
    StreamingState GetTileState(const std::string& tileId) const;
    std::vector<std::string> GetAllTileIds() const;
    std::vector<std::string> GetLoadedTiles() const;
    const StreamingTrigger* GetTrigger(const std::string& triggerId) const;
    bool ValidateTiles() const;
    bool ExportStreamingManifest(const std::string& filePath) const;
    bool SaveStreamingConfig(const std::string& filePath) const;
    bool LoadStreamingConfig(const std::string& filePath);
    void ClearAll();

private:
    bool m_active{false};
    std::unordered_map<std::string, StreamingTile> m_tiles;
    std::unordered_map<std::string, StreamingTrigger> m_triggers;
    std::unordered_map<std::string, StreamingState> m_tileStates;
    StreamingBudget m_budget;
    int m_nextTileIndex{0};
    int m_nextTriggerIndex{0};
};

} // namespace Atlas::Editor
