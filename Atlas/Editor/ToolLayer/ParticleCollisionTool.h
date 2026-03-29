#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P25 Tool — Particle collision authoring, kill volume setup, and collision response tuning.
class ParticleCollisionTool : public ITool {
public:
    enum class CollisionResponse { Bounce, Stick, Kill, Deflect, Custom };
    enum class KillVolumeShape { Box, Sphere, Capsule, Convex, Custom };
    enum class ParticleColliderType { Static, Dynamic, Trigger, Custom };
    enum class CollisionFilterMode { Include, Exclude, All, None, Custom };

    struct ParticleColliderDef {
        std::string colliderId;
        std::string colliderName;
        ParticleColliderType colliderType{ParticleColliderType::Static};
        CollisionResponse response{CollisionResponse::Bounce};
        float restitution{0.5f};
        float friction{0.3f};
        bool enabled{true};
    };

    struct KillVolumeDef {
        std::string killVolumeId;
        KillVolumeShape shape{KillVolumeShape::Box};
        float radius{100.0f};
        float halfExtentX{50.0f};
        float halfExtentY{50.0f};
        float halfExtentZ{50.0f};
        bool active{true};
    };

    struct CollisionFilterConfig {
        std::string filterId;
        std::string colliderId;
        CollisionFilterMode filterMode{CollisionFilterMode::All};
        std::vector<std::string> tagList;
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "ParticleCollisionTool"; }
    bool IsActive() const override { return m_active; }

    bool RegisterCollider(const ParticleColliderDef& collider);
    bool UnregisterCollider(const std::string& colliderId);
    const ParticleColliderDef* GetCollider(const std::string& colliderId) const;
    std::vector<std::string> GetAllColliderIds() const;
    std::vector<std::string> GetCollidersByType(ParticleColliderType type) const;
    bool AddKillVolume(const KillVolumeDef& killVolume);
    bool RemoveKillVolume(const std::string& killVolumeId);
    const KillVolumeDef* GetKillVolume(const std::string& killVolumeId) const;
    std::vector<std::string> GetAllKillVolumeIds() const;
    std::vector<std::string> GetActiveKillVolumes() const;
    bool AddFilter(const CollisionFilterConfig& filter);
    bool RemoveFilter(const std::string& filterId);
    const CollisionFilterConfig* GetFilter(const std::string& filterId) const;
    std::vector<std::string> GetFiltersByCollider(const std::string& colliderId) const;
    bool SetResponse(const std::string& colliderId, CollisionResponse response);
    void Reset();

private:
    bool m_active{false};
    std::unordered_map<std::string, ParticleColliderDef> m_colliders;
    std::unordered_map<std::string, KillVolumeDef> m_killVolumes;
    std::unordered_map<std::string, CollisionFilterConfig> m_filters;
};

} // namespace Atlas::Editor
