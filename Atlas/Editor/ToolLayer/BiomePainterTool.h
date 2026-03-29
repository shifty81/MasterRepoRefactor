#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P4 Tool — Paint biome regions onto terrain tiles with blending support.
class BiomePainterTool : public ITool {
public:
    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "BiomePainterTool"; }
    bool IsActive() const override { return m_active; }

    void SetActiveBiome(const std::string& biomeId);
    const std::string& GetActiveBiome() const { return m_activeBiome; }
    void PaintAt(float worldX, float worldZ, float radius);
    void RegisterBiome(const std::string& biomeId, const std::string& textureAsset);
    int GetRegisteredBiomeCount() const { return static_cast<int>(m_biomes.size()); }
    int GetPaintedTileCount() const { return m_paintedTileCount; }

private:
    bool m_active{false};
    std::string m_activeBiome;
    std::unordered_map<std::string, std::string> m_biomes;
    int m_paintedTileCount{0};
};

} // namespace Atlas::Editor
