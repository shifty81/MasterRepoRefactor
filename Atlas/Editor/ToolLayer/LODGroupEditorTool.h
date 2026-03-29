#pragma once
#include "ITool.h"
#include <string>
#include <vector>

namespace Atlas::Editor {

/// P7 Tool — Manage LOD (Level of Detail) groups, thresholds, and mesh assignments.
class LODGroupEditorTool : public ITool {
public:
    struct LODLevel {
        int level{0};
        std::string meshAsset;
        float screenPercentage{100.0f};
        bool castShadow{true};
    };

    struct LODGroup {
        std::string groupId;
        std::string entityId;
        std::vector<LODLevel> levels;
        float autoComputeThreshold{0.0f};
        bool useAutoCompute{false};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "LODGroupEditorTool"; }
    bool IsActive() const override { return m_active; }

    std::string CreateGroup(const std::string& entityId);
    bool RemoveGroup(const std::string& groupId);
    bool AddLODLevel(const std::string& groupId,
                     int level, const std::string& meshAsset,
                     float screenPercentage);
    bool RemoveLODLevel(const std::string& groupId, int level);
    bool SetLODMesh(const std::string& groupId, int level,
                    const std::string& meshAsset);
    bool SetLODScreenPercentage(const std::string& groupId, int level,
                                 float screenPercentage);
    bool SetCastShadow(const std::string& groupId, int level, bool cast);
    bool SetAutoCompute(const std::string& groupId, bool enabled,
                        float threshold = 0.0f);
    bool AutoGenerateLODs(const std::string& groupId, int numLevels = 4);
    const LODGroup* GetGroup(const std::string& groupId) const;
    std::vector<std::string> GetGroupsForEntity(const std::string& entityId) const;
    int GetGroupCount() const { return static_cast<int>(m_groups.size()); }
    void ClearAll();

private:
    bool m_active{false};
    std::vector<LODGroup> m_groups;
    int m_nextIndex{0};
};

} // namespace Atlas::Editor
