#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P12 Tool — Environment art placement, scattering, and dressing authoring tool.
class EnvironmentArtTool : public ITool {
public:
    enum class PlacementMode { Manual, Scatter, Align, Grid, Radial };
    enum class SurfaceSnap { None, Terrain, Mesh, Both };
    enum class ScatterShape { Sphere, Box, Cylinder, Spline, Brush };
    enum class VariationType { None, RandomRotation, RandomScale, RandomMesh };
    enum class DensityFalloff { None, Linear, Smooth, Exponential };

    struct ScatterVariance {
        float posOffsetXZ{0.1f};
        float posOffsetY{0.0f};
        float scaleMin{0.9f};
        float scaleMax{1.1f};
        float rotationYMin{0.0f};
        float rotationYMax{360.0f};
        float pitchVariance{0.0f};
        float rollVariance{0.0f};
        bool uniformScale{true};
    };

    struct MeshVariant {
        std::string variantId;
        std::string meshId;
        std::string meshPath;
        float weight{1.0f};
        bool enabled{true};
    };

    struct ArtLayer {
        std::string layerId;
        std::string name;
        PlacementMode placementMode{PlacementMode::Scatter};
        SurfaceSnap surfaceSnap{SurfaceSnap::Terrain};
        ScatterShape scatterShape{ScatterShape::Sphere};
        VariationType variationType{VariationType::RandomRotation};
        DensityFalloff densityFalloff{DensityFalloff::Smooth};
        ScatterVariance variance;
        std::vector<MeshVariant> meshVariants;
        float density{1.0f};
        float scatterRadius{10.0f};
        float scatterBoxHalfX{10.0f};
        float scatterBoxHalfY{0.5f};
        float scatterBoxHalfZ{10.0f};
        float gridSpacingX{2.0f};
        float gridSpacingZ{2.0f};
        float alignNormalStrength{1.0f};
        float minSlopeAngle{0.0f};
        float maxSlopeAngle{60.0f};
        float minAltitude{-9999.0f};
        float maxAltitude{9999.0f};
        int maxObjectCount{1000};
        bool castShadows{true};
        bool receiveShadows{true};
        bool enabled{true};
        bool locked{false};
        std::string paintMaskId;
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "EnvironmentArtTool"; }
    bool IsActive() const override { return m_active; }

    // Layer management
    std::string CreateLayer(const std::string& name,
                             PlacementMode mode = PlacementMode::Scatter);
    bool RemoveLayer(const std::string& layerId);
    bool SetPlacementMode(const std::string& layerId, PlacementMode mode);
    bool SetSurfaceSnap(const std::string& layerId, SurfaceSnap snap);
    bool SetScatterShape(const std::string& layerId, ScatterShape shape);
    bool SetVariationType(const std::string& layerId, VariationType type);
    bool SetDensityFalloff(const std::string& layerId, DensityFalloff falloff);
    bool SetDensity(const std::string& layerId, float density);
    bool SetScatterRadius(const std::string& layerId, float radius);
    bool SetScatterBox(const std::string& layerId, float hx, float hy, float hz);
    bool SetGridSpacing(const std::string& layerId, float sx, float sz);
    bool SetAlignNormalStrength(const std::string& layerId, float strength);
    bool SetSlopeRange(const std::string& layerId, float minAngle, float maxAngle);
    bool SetAltitudeRange(const std::string& layerId, float minAlt, float maxAlt);
    bool SetMaxObjectCount(const std::string& layerId, int count);
    bool SetLayerEnabled(const std::string& layerId, bool enabled);
    bool SetLayerLocked(const std::string& layerId, bool locked);
    bool SetPaintMask(const std::string& layerId, const std::string& maskId);
    int GetLayerCount() const { return static_cast<int>(m_layers.size()); }
    const ArtLayer* GetLayer(const std::string& layerId) const;
    std::vector<std::string> GetLayerIds() const;
    std::vector<std::string> GetEnabledLayerIds() const;

    // Scatter variance
    bool SetPositionOffsetXZ(const std::string& layerId, float offset);
    bool SetPositionOffsetY(const std::string& layerId, float offset);
    bool SetScaleRange(const std::string& layerId, float min, float max);
    bool SetRotationYRange(const std::string& layerId, float min, float max);
    bool SetPitchVariance(const std::string& layerId, float variance);
    bool SetUniformScale(const std::string& layerId, bool uniform);

    // Mesh variants
    std::string AddMeshVariant(const std::string& layerId,
                                const std::string& meshId,
                                float weight = 1.0f,
                                const std::string& meshPath = "");
    bool RemoveMeshVariant(const std::string& layerId,
                            const std::string& variantId);
    bool SetMeshVariantWeight(const std::string& layerId,
                               const std::string& variantId, float weight);
    bool SetMeshVariantEnabled(const std::string& layerId,
                                const std::string& variantId, bool enabled);
    int GetMeshVariantCount(const std::string& layerId) const;

    // Operations
    bool ScatterLayer(const std::string& layerId);
    bool ClearLayerObjects(const std::string& layerId);
    bool BakeLayer(const std::string& layerId);
    int GetObjectCount(const std::string& layerId) const;

    // Persistence
    bool SaveLayers(const std::string& filePath) const;
    bool LoadLayers(const std::string& filePath);
    void ClearAll();

private:
    bool m_active{false};
    std::unordered_map<std::string, ArtLayer> m_layers;
    std::unordered_map<std::string, int> m_objectCounts;
    int m_nextLayerIndex{0};
    int m_nextVariantIndex{0};
};

} // namespace Atlas::Editor
