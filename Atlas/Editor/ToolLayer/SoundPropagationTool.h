#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P7 Tool — Place and configure audio propagation zones, portals, and materials.
class SoundPropagationTool : public ITool {
public:
    enum class PropagationMode { Raycast, Geometric, Hybrid };

    struct SoundMaterial {
        std::string materialId;
        float absorptionLow{0.1f};
        float absorptionMid{0.2f};
        float absorptionHigh{0.3f};
        float transmission{0.05f};
        float scattering{0.05f};
    };

    struct PropagationZone {
        std::string zoneId;
        PropagationMode mode{PropagationMode::Hybrid};
        float x{0.0f};
        float y{0.0f};
        float z{0.0f};
        float radius{20.0f};
        float reverbWet{0.3f};
        float reverbDecay{1.0f};
        std::string materialId;
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "SoundPropagationTool"; }
    bool IsActive() const override { return m_active; }

    std::string AddZone(float x, float y, float z, float radius = 20.0f);
    bool RemoveZone(const std::string& zoneId);
    bool SetZonePropagationMode(const std::string& zoneId, PropagationMode mode);
    bool SetZoneReverb(const std::string& zoneId, float wet, float decay);
    bool SetZoneMaterial(const std::string& zoneId, const std::string& materialId);
    std::string RegisterMaterial(const std::string& name,
                                  float absLow, float absMid, float absHigh);
    bool UpdateMaterial(const std::string& materialId,
                        float absLow, float absMid, float absHigh);
    const PropagationZone* GetZone(const std::string& zoneId) const;
    const SoundMaterial* GetMaterial(const std::string& materialId) const;
    int GetZoneCount() const { return static_cast<int>(m_zones.size()); }
    int GetMaterialCount() const { return static_cast<int>(m_materials.size()); }
    void ClearAll();

private:
    bool m_active{false};
    std::vector<PropagationZone> m_zones;
    std::vector<SoundMaterial> m_materials;
    int m_nextZoneIndex{0};
    int m_nextMaterialIndex{0};
};

} // namespace Atlas::Editor
