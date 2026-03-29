#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P26 Tool — Procedural terrain generation, biome layering, and erosion simulation.
class ProceduralTerrainTool : public ITool {
public:
    enum class GenerationMode { Flat, Heightmap, Noise, Voronoi, Hydraulic, Tectonic, Custom };
    enum class BiomeType { Grassland, Desert, Tundra, Forest, Ocean, Mountain, Swamp, Custom };
    enum class ErosionType { Hydraulic, Thermal, Wind, Glacial, Chemical, None, Custom };
    enum class TerrainLayer { Base, Rock, Soil, Vegetation, Snow, Sand, Custom };

    struct TerrainGenDef {
        std::string genId;
        std::string genName;
        GenerationMode mode{GenerationMode::Noise};
        int seed{0};
        float width{1024.0f};
        float height{1024.0f};
        float maxElevation{500.0f};
        int resolution{512};
        bool seamless{false};
    };

    struct BiomeLayerDef {
        std::string biomeLayerId;
        std::string genId;
        BiomeType biomeType{BiomeType::Grassland};
        TerrainLayer layer{TerrainLayer::Base};
        float minElevation{0.0f};
        float maxElevation{1000.0f};
        float blendWeight{1.0f};
        bool enabled{true};
    };

    struct ErosionSimDef {
        std::string erosionId;
        std::string genId;
        ErosionType erosionType{ErosionType::Hydraulic};
        int iterations{100};
        float intensity{0.5f};
        float sedimentCapacity{1.0f};
        bool applyToMesh{true};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "ProceduralTerrainTool"; }
    bool IsActive() const override { return m_active; }

    bool CreateTerrain(const TerrainGenDef& def);
    bool DeleteTerrain(const std::string& genId);
    bool GenerateTerrain(const std::string& genId);
    const TerrainGenDef* GetTerrain(const std::string& genId) const;
    std::vector<std::string> GetAllTerrainIds() const;
    std::vector<std::string> GetTerrainsByMode(GenerationMode mode) const;
    bool AddBiomeLayer(const std::string& genId, const BiomeLayerDef& biome);
    bool RemoveBiomeLayer(const std::string& genId, const std::string& biomeLayerId);
    const BiomeLayerDef* GetBiomeLayer(const std::string& biomeLayerId) const;
    std::vector<std::string> GetBiomeLayersByGen(const std::string& genId) const;
    std::vector<std::string> GetBiomeLayersByType(BiomeType type) const;
    bool AddErosionSim(const std::string& genId, const ErosionSimDef& erosion);
    bool RemoveErosionSim(const std::string& genId, const std::string& erosionId);
    bool RunErosion(const std::string& erosionId);
    const ErosionSimDef* GetErosionSim(const std::string& erosionId) const;
    std::vector<std::string> GetErosionSimsByGen(const std::string& genId) const;
    bool ExportHeightmap(const std::string& genId, const std::string& filePath) const;
    void Reset();

private:
    bool m_active{false};
    std::unordered_map<std::string, TerrainGenDef> m_terrains;
    std::unordered_map<std::string, std::vector<BiomeLayerDef>> m_biomeLayers;
    std::unordered_map<std::string, std::vector<ErosionSimDef>> m_erosionSims;
};

} // namespace Atlas::Editor
