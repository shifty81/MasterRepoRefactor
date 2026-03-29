#pragma once
#include "ITool.h"
#include <string>
#include <vector>

namespace Atlas::Editor {

/// P4 Tool — Interactive terrain height sculpting with brush-based editing.
class TerrainSculptTool : public ITool {
public:
    enum class BrushMode { Raise, Lower, Smooth, Flatten };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "TerrainSculptTool"; }
    bool IsActive() const override { return m_active; }

    void SetBrushRadius(float radius);
    void SetBrushStrength(float strength);
    void SetBrushMode(BrushMode mode);
    BrushMode GetBrushMode() const { return m_mode; }
    float GetBrushRadius() const { return m_brushRadius; }
    float GetBrushStrength() const { return m_brushStrength; }
    void ApplyBrush(float worldX, float worldZ);
    int GetEditCount() const { return m_editCount; }

private:
    bool m_active{false};
    BrushMode m_mode{BrushMode::Raise};
    float m_brushRadius{5.0f};
    float m_brushStrength{1.0f};
    int m_editCount{0};
};

} // namespace Atlas::Editor
