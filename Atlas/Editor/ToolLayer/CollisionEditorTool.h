#pragma once
#include "ITool.h"
#include <string>
#include <vector>

namespace Atlas::Editor {

/// P6 Tool — Visualise and edit collision meshes, primitives, and compound shapes.
class CollisionEditorTool : public ITool {
public:
    enum class ColliderType { Box, Sphere, Capsule, Mesh, Convex };

    struct Collider {
        std::string colliderId;
        std::string entityId;
        ColliderType type{ColliderType::Box};
        float x{0.0f};
        float y{0.0f};
        float z{0.0f};
        float sizeX{1.0f};
        float sizeY{1.0f};
        float sizeZ{1.0f};
        bool trigger{false};
        bool visualize{true};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "CollisionEditorTool"; }
    bool IsActive() const override { return m_active; }

    std::string AddCollider(const std::string& entityId,
                            ColliderType type = ColliderType::Box);
    bool RemoveCollider(const std::string& colliderId);
    bool SetColliderSize(const std::string& colliderId,
                         float sx, float sy, float sz);
    bool SetTrigger(const std::string& colliderId, bool trigger);
    bool SetVisualize(const std::string& colliderId, bool vis);
    const Collider* GetCollider(const std::string& colliderId) const;
    std::vector<Collider> GetCollidersForEntity(const std::string& entityId) const;
    int GetColliderCount() const { return static_cast<int>(m_colliders.size()); }
    void ClearAll();

private:
    bool m_active{false};
    std::vector<Collider> m_colliders;
    int m_nextIndex{0};
};

} // namespace Atlas::Editor
