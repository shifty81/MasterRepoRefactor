#pragma once
#include "ITool.h"
#include <string>
#include <vector>

namespace Atlas::Editor {

/// P7 Tool — Define and sculpt water bodies: oceans, rivers, lakes, and pools.
class WaterVolumeTool : public ITool {
public:
    enum class WaterBodyType { Ocean, River, Lake, Pool };

    struct WaterBody {
        std::string bodyId;
        WaterBodyType type{WaterBodyType::Lake};
        float surfaceY{0.0f};
        float depth{10.0f};
        float waveAmplitude{0.5f};
        float waveFrequency{1.0f};
        float flowSpeed{0.0f};
        float visibility{10.0f};
        std::string causticTexture;
        bool enableFoam{true};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "WaterVolumeTool"; }
    bool IsActive() const override { return m_active; }

    std::string AddWaterBody(WaterBodyType type, float surfaceY = 0.0f,
                              float depth = 10.0f);
    bool RemoveWaterBody(const std::string& bodyId);
    bool SetSurfaceLevel(const std::string& bodyId, float y);
    bool SetWaveParameters(const std::string& bodyId,
                           float amplitude, float frequency);
    bool SetFlowSpeed(const std::string& bodyId, float speed);
    bool SetVisibility(const std::string& bodyId, float visibility);
    bool SetFoamEnabled(const std::string& bodyId, bool enabled);
    const WaterBody* GetWaterBody(const std::string& bodyId) const;
    int GetWaterBodyCount() const { return static_cast<int>(m_bodies.size()); }
    void ClearAll();

private:
    bool m_active{false};
    std::vector<WaterBody> m_bodies;
    int m_nextIndex{0};
};

} // namespace Atlas::Editor
