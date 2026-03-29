#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P13 Tool — Decal painting, projection volumes, and surface masking for environment art.
class DecalProjectorTool : public ITool {
public:
    enum class ProjectionShape { Box, Sphere, Cylinder, Frustum };
    enum class SurfaceMask { All, StaticOnly, DynamicOnly, TerrainOnly, MeshOnly };
    enum class DecalBlendMode { Albedo, Normal, SpecularRoughness, Emissive, Full };
    enum class FadeMode { None, Distance, Angle, Both };

    struct ProjectionVolume {
        ProjectionShape shape{ProjectionShape::Box};
        float extentX{1.0f};
        float extentY{1.0f};
        float extentZ{1.0f};
        float nearPlane{0.001f};
        float farPlane{2.0f};
        float fieldOfView{90.0f};
    };

    struct DecalMaterial {
        std::string materialId;
        std::string albedoTexPath;
        std::string normalTexPath;
        std::string roughnessTexPath;
        float normalStrength{1.0f};
        float roughnessValue{0.5f};
        float metallicValue{0.0f};
    };

    struct FadeSettings {
        FadeMode fadeMode{FadeMode::Distance};
        float startFadeDistance{10.0f};
        float endFadeDistance{20.0f};
        float angleThreshold{45.0f};
        float angleFadeSoftness{15.0f};
        bool enabled{true};
    };

    struct DecalRecord {
        std::string decalId;
        std::string name;
        DecalBlendMode blendMode{DecalBlendMode::Albedo};
        SurfaceMask surfaceMask{SurfaceMask::All};
        ProjectionVolume volume;
        DecalMaterial material;
        FadeSettings fadeSettings;
        float posX{0.0f};
        float posY{0.0f};
        float posZ{0.0f};
        float rotX{0.0f};
        float rotY{0.0f};
        float rotZ{0.0f};
        float opacity{1.0f};
        int renderLayer{0};
        bool affectsAlbedo{true};
        bool affectsNormals{true};
        bool affectsSpecular{false};
        bool enabled{true};
        std::string linkedEntityId;
        std::string linkedSceneId;
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "DecalProjectorTool"; }
    bool IsActive() const override { return m_active; }

    // Decal management
    std::string CreateDecal(const std::string& name, DecalBlendMode blendMode = DecalBlendMode::Albedo);
    bool RemoveDecal(const std::string& decalId);
    bool SetBlendMode(const std::string& decalId, DecalBlendMode mode);
    bool SetSurfaceMask(const std::string& decalId, SurfaceMask mask);
    bool SetOpacity(const std::string& decalId, float opacity);
    bool SetDecalEnabled(const std::string& decalId, bool enabled);
    bool SetDecalPosition(const std::string& decalId, float x, float y, float z);
    bool SetDecalRotation(const std::string& decalId, float rx, float ry, float rz);
    bool SetRenderLayer(const std::string& decalId, int layer);
    bool LinkToEntity(const std::string& decalId, const std::string& entityId);
    bool LinkToScene(const std::string& decalId, const std::string& sceneId);

    // Projection volume
    bool SetProjectionShape(const std::string& decalId, ProjectionShape shape);
    bool SetProjectionExtents(const std::string& decalId, float x, float y, float z);
    bool SetProjectionDepth(const std::string& decalId, float near, float far);

    // Material
    bool SetMaterial(const std::string& decalId, const DecalMaterial& mat);
    bool SetAlbedoTexture(const std::string& decalId, const std::string& path);
    bool SetNormalTexture(const std::string& decalId, const std::string& path);
    bool SetNormalStrength(const std::string& decalId, float strength);
    bool SetAffectsAlbedo(const std::string& decalId, bool enabled);
    bool SetAffectsNormals(const std::string& decalId, bool enabled);
    bool SetAffectsSpecular(const std::string& decalId, bool enabled);

    // Fade settings
    bool SetFadeMode(const std::string& decalId, FadeMode mode);
    bool SetFadeDistance(const std::string& decalId, float start, float end);
    bool SetAngleFade(const std::string& decalId, float threshold, float softness);

    // Queries
    int GetDecalCount() const { return static_cast<int>(m_decals.size()); }
    const DecalRecord* GetDecal(const std::string& decalId) const;
    std::vector<std::string> GetDecalIds() const;
    std::vector<std::string> GetDecalsByScene(const std::string& sceneId) const;
    std::vector<std::string> GetDecalsByBlendMode(DecalBlendMode mode) const;
    std::vector<std::string> GetEnabledDecalIds() const;

    // Persistence
    bool SaveDecals(const std::string& filePath) const;
    bool LoadDecals(const std::string& filePath);
    void ClearAll();

private:
    bool m_active{false};
    std::unordered_map<std::string, DecalRecord> m_decals;
    int m_nextDecalIndex{0};
};

} // namespace Atlas::Editor
