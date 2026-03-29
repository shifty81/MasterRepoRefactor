#pragma once
#include "ITool.h"
#include <string>
#include <vector>

namespace Atlas::Editor {

/// P5 Tool — Paint surface decals (grunge, damage, markings) onto world geometry.
class DecalPainterTool : public ITool {
public:
    struct Decal {
        std::string id;
        std::string materialAsset;
        float x{0.0f};
        float y{0.0f};
        float z{0.0f};
        float rotY{0.0f};
        float scale{1.0f};
        float opacity{1.0f};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "DecalPainterTool"; }
    bool IsActive() const override { return m_active; }

    void SetActiveMaterial(const std::string& materialAsset);
    const std::string& GetActiveMaterial() const { return m_activeMaterial; }
    std::string PlaceDecal(float x, float y, float z, float scale = 1.0f,
                           float rotY = 0.0f);
    bool RemoveDecal(const std::string& id);
    bool SetDecalOpacity(const std::string& id, float opacity);
    const std::vector<Decal>& GetDecals() const { return m_decals; }
    int GetDecalCount() const { return static_cast<int>(m_decals.size()); }
    void ClearDecals();

private:
    bool m_active{false};
    std::string m_activeMaterial;
    std::vector<Decal> m_decals;
    int m_nextIndex{0};
};

} // namespace Atlas::Editor
