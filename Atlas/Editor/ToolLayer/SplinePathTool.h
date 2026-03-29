#pragma once
#include "ITool.h"
#include <string>
#include <vector>

namespace Atlas::Editor {

/// P6 Tool — Spline-based path editor for roads, rivers, cables, and pipes.
class SplinePathTool : public ITool {
public:
    enum class SplineType { Linear, Bezier, CatmullRom };

    struct SplineNode {
        std::string nodeId;
        float x{0.0f};
        float y{0.0f};
        float z{0.0f};
        float tangentX{0.0f};
        float tangentZ{0.0f};
    };

    struct SplinePath {
        std::string pathId;
        SplineType type{SplineType::Bezier};
        std::vector<SplineNode> nodes;
        float width{1.0f};
        bool closed{false};
        std::string materialAsset;
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "SplinePathTool"; }
    bool IsActive() const override { return m_active; }

    std::string CreatePath(SplineType type = SplineType::Bezier);
    bool RemovePath(const std::string& pathId);
    std::string AddNode(const std::string& pathId, float x, float y, float z);
    bool RemoveNode(const std::string& pathId, const std::string& nodeId);
    bool SetPathClosed(const std::string& pathId, bool closed);
    bool SetPathMaterial(const std::string& pathId, const std::string& material);
    const SplinePath* GetPath(const std::string& pathId) const;
    int GetPathCount() const { return static_cast<int>(m_paths.size()); }
    void ClearAll();

private:
    bool m_active{false};
    std::vector<SplinePath> m_paths;
    int m_nextPathIndex{0};
    int m_nextNodeIndex{0};
};

} // namespace Atlas::Editor
