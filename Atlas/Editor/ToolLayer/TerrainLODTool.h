#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P28 Tool — Terrain LOD group authoring, screen-size thresholding, and tessellation config.
class TerrainLODTool : public ITool {
public:
    enum class LODMethod { ScreenSize, Distance, ErrorMetric, Continuous, Custom };
    enum class TessellationMode { None, PN, PhongTess, AdaptiveTess, Custom };
    enum class HeightmapQuality { Quarter, Half, Full, Double, Custom };
    enum class TransitionType { Dither, CrossFade, Snap, Blend, Custom };

    struct TerrainLODGroupDef {
        std::string lodGroupId;
        std::string lodGroupName;
        std::string terrainId;
        LODMethod method{LODMethod::ScreenSize};
        int lodCount{4};
        float minScreenSize{0.01f};
        float maxScreenSize{1.0f};
        TessellationMode tessMode{TessellationMode::None};
        TransitionType transitionType{TransitionType::Dither};
        bool enabled{true};
    };

    struct LODLevelDef {
        std::string lodLevelId;
        std::string lodGroupId;
        int level{0};
        float screenSizeThreshold{1.0f};
        float distanceThreshold{0.0f};
        HeightmapQuality heightmapQuality{HeightmapQuality::Full};
        int patchSubdivisions{64};
        float maxError{0.1f};
        bool simplifyNormals{false};
        bool enabled{true};
    };

    struct TessConfigDef {
        std::string tessConfigId;
        std::string lodGroupId;
        TessellationMode tessMode{TessellationMode::PN};
        float maxTessFactor{64.0f};
        float minTessFactor{1.0f};
        float adaptiveScale{1.0f};
        bool phongStrength{false};
        float phongStrengthValue{0.75f};
        bool enabled{true};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "TerrainLODTool"; }
    bool IsActive() const override { return m_active; }

    bool CreateLODGroup(const TerrainLODGroupDef& def);
    bool DeleteLODGroup(const std::string& lodGroupId);
    bool EnableLODGroup(const std::string& lodGroupId, bool enabled);
    bool SetLODMethod(const std::string& lodGroupId, LODMethod method);
    const TerrainLODGroupDef* GetLODGroup(const std::string& lodGroupId) const;
    std::vector<std::string> GetAllLODGroupIds() const;
    std::vector<std::string> GetLODGroupsByMethod(LODMethod method) const;
    std::vector<std::string> GetLODGroupsByTerrain(const std::string& terrainId) const;
    bool AddLODLevel(const std::string& lodGroupId, const LODLevelDef& def);
    bool RemoveLODLevel(const std::string& lodGroupId, const std::string& lodLevelId);
    bool EnableLODLevel(const std::string& lodLevelId, bool enabled);
    const LODLevelDef* GetLODLevel(const std::string& lodLevelId) const;
    std::vector<std::string> GetLODLevelsByGroup(const std::string& lodGroupId) const;
    std::vector<std::string> GetLODLevelsByQuality(HeightmapQuality quality) const;
    bool SetTessConfig(const std::string& lodGroupId, const TessConfigDef& config);
    bool RemoveTessConfig(const std::string& lodGroupId);
    const TessConfigDef* GetTessConfig(const std::string& tessConfigId) const;
    std::vector<std::string> GetTessConfigsByMode(TessellationMode mode) const;
    void Reset();

private:
    bool m_active{false};
    std::unordered_map<std::string, TerrainLODGroupDef> m_lodGroups;
    std::unordered_map<std::string, LODLevelDef> m_lodLevels;
    std::unordered_map<std::string, TessConfigDef> m_tessConfigs;
};

} // namespace Atlas::Editor
