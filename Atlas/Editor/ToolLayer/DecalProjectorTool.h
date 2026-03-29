#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P13/P16 Tool — Decal projection authoring, surface blending, and fade distance management.
/// Originally authored in Phase 28 (P13); extended in Phase 31 (P16) with additional blend modes and
/// SurfaceMask/ProjectionShape enums for finer-grained projection control.
class DecalProjectorTool : public ITool {
public:
    enum class DecalSurface { Any, StaticMesh, SkeletalMesh, Terrain, Water, Custom };
    enum class FadeMode { None, DistanceBased, AngleBased, Combined };
    enum class DecalBlend { Translucent, Stain, Normal, Emissive, DBuffer, DBufferNormal };
    enum class SurfaceMask { All, StaticOnly, DynamicOnly, TerrainOnly, Custom };
    enum class ProjectionShape { Box, Sphere, Cylinder, Cone, Flat };

    struct DecalDef {
        std::string decalId;
        std::string name;
        std::string materialPath;
        DecalSurface surface{DecalSurface::Any};
        DecalBlend blendMode{DecalBlend::Translucent};
        float width{100.0f};
        float height{100.0f};
        float depth{100.0f};
        float fadeStartDist{500.0f};
        float fadeEndDist{1000.0f};
        int sortOrder{0};
    };

    struct DecalBatch {
        std::string batchId;
        std::string name;
        std::vector<std::string> decals;
    };

    struct DecalRenderSettings {
        std::vector<std::string> receiverLayers;
        int maxDecals{128};
        std::string sortPolicy{"Distance"};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "DecalProjectorTool"; }
    bool IsActive() const override { return m_active; }

    std::string CreateDecal(const std::string& name, const std::string& materialPath);
    bool RemoveDecal(const std::string& decalId);
    std::string CreateBatch(const std::string& name);
    bool RemoveBatch(const std::string& batchId);
    bool AddDecalToBatch(const std::string& batchId, const std::string& decalId);
    bool SetDecalMaterial(const std::string& decalId, const std::string& materialPath);
    bool SetDecalSize(const std::string& decalId, float width, float height, float depth);
    bool SetFadeDistances(const std::string& decalId, float startDist, float endDist);
    bool SetBlendMode(const std::string& decalId, DecalBlend blendMode);
    bool PlaceDecal(const std::string& decalId, float x, float y, float z);
    const DecalDef* GetDecalById(const std::string& decalId) const;
    std::vector<std::string> GetAllDecalIds() const;
    const DecalBatch* GetBatchById(const std::string& batchId) const;
    int GetBatchCount() const { return static_cast<int>(m_batches.size()); }
    bool ValidateDecal(const std::string& decalId) const;
    bool ExportDecalSet(const std::string& filePath) const;
    bool SaveDecals(const std::string& filePath) const;
    bool LoadDecals(const std::string& filePath);
    void ClearAll();

private:
    bool m_active{false};
    std::unordered_map<std::string, DecalDef> m_decals;
    std::unordered_map<std::string, DecalBatch> m_batches;
    DecalRenderSettings m_renderSettings;
    int m_nextDecalIndex{0};
    int m_nextBatchIndex{0};
};

} // namespace Atlas::Editor
