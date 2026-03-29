#pragma once
#include "ITool.h"
#include <string>
#include <vector>

namespace Atlas::Editor {

/// P5 Tool — Editor-side navigation mesh baking, exclusion zones, and off-mesh links.
class NavMeshEditorTool : public ITool {
public:
    struct NavExclusionZone {
        std::string id;
        float x{0.0f};
        float z{0.0f};
        float width{5.0f};
        float depth{5.0f};
    };

    struct OffMeshLink {
        std::string id;
        float startX{0.0f};
        float startZ{0.0f};
        float endX{0.0f};
        float endZ{0.0f};
        bool bidirectional{true};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "NavMeshEditorTool"; }
    bool IsActive() const override { return m_active; }

    bool BakeNavMesh();
    bool IsBaked() const { return m_baked; }
    void ClearNavMesh();

    std::string AddExclusionZone(float x, float z, float width, float depth);
    bool RemoveExclusionZone(const std::string& id);
    int GetExclusionZoneCount() const { return static_cast<int>(m_exclusions.size()); }

    std::string AddOffMeshLink(float sx, float sz, float ex, float ez,
                               bool bidirectional = true);
    bool RemoveOffMeshLink(const std::string& id);
    int GetOffMeshLinkCount() const { return static_cast<int>(m_links.size()); }

private:
    bool m_active{false};
    bool m_baked{false};
    std::vector<NavExclusionZone> m_exclusions;
    std::vector<OffMeshLink> m_links;
    int m_nextIndex{0};
};

} // namespace Atlas::Editor
