#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P13 Tool — Audio reverb zone placement, decay parameters, and blend radius configuration.
class AudioReverbZoneTool : public ITool {
public:
    enum class ReverbPreset { None, Generic, PaddedCell, Room, Bathroom, LivingRoom,
                               StoneRoom, Auditorium, ConcertHall, Cave, Arena, Hangar };
    enum class ZoneShape { Sphere, Box, Capsule, Custom };
    enum class BlendCurve { Linear, Smooth, Exponential, InverseSquare };
    enum class ReverbQuality { Low, Medium, High };

    struct DecayParameters {
        float decayTime{1.49f};
        float decayHFRatio{0.83f};
        float reflectionsGainDb{-2602.0f};
        float reflectionsDelay{0.007f};
        float lateReverbGainDb{200.0f};
        float lateReverbDelay{0.011f};
        float diffusion{100.0f};
        float density{100.0f};
    };

    struct FrequencySettings {
        float roomGainDb{-1000.0f};
        float roomHFGainDb{-100.0f};
        float roomLFGainDb{0.0f};
        float hfReference{5000.0f};
        float lfReference{250.0f};
        bool airAbsorptionEnabled{true};
        float airAbsorptionGainHF{-5.0f};
    };

    struct BlendSettings {
        BlendCurve blendCurve{BlendCurve::Smooth};
        float blendRadius{5.0f};
        float minBlendDistance{0.0f};
        float maxBlendDistance{10.0f};
        float blendWeight{1.0f};
        bool priorityOverride{false};
    };

    struct ReverbZoneRecord {
        std::string zoneId;
        std::string name;
        ReverbPreset preset{ReverbPreset::Generic};
        ZoneShape shape{ZoneShape::Sphere};
        ReverbQuality quality{ReverbQuality::Medium};
        DecayParameters decayParams;
        FrequencySettings freqSettings;
        BlendSettings blendSettings;
        float posX{0.0f};
        float posY{0.0f};
        float posZ{0.0f};
        float extentX{10.0f};
        float extentY{10.0f};
        float extentZ{10.0f};
        float radius{10.0f};
        int priority{0};
        bool enabled{true};
        bool overridePreset{false};
        std::string linkedSceneId;
        std::string linkedEntityId;
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "AudioReverbZoneTool"; }
    bool IsActive() const override { return m_active; }

    // Zone management
    std::string CreateZone(const std::string& name, ReverbPreset preset = ReverbPreset::Generic);
    bool RemoveZone(const std::string& zoneId);
    bool SetPreset(const std::string& zoneId, ReverbPreset preset);
    bool SetZoneShape(const std::string& zoneId, ZoneShape shape);
    bool SetZoneRadius(const std::string& zoneId, float radius);
    bool SetZoneExtents(const std::string& zoneId, float x, float y, float z);
    bool SetZonePosition(const std::string& zoneId, float x, float y, float z);
    bool SetZoneEnabled(const std::string& zoneId, bool enabled);
    bool SetPriority(const std::string& zoneId, int priority);
    bool SetOverridePreset(const std::string& zoneId, bool override);
    bool LinkToScene(const std::string& zoneId, const std::string& sceneId);
    bool LinkToEntity(const std::string& zoneId, const std::string& entityId);

    // Decay settings
    bool SetDecayTime(const std::string& zoneId, float seconds);
    bool SetDecayHFRatio(const std::string& zoneId, float ratio);
    bool SetReflectionsGain(const std::string& zoneId, float gainDb);
    bool SetReflectionsDelay(const std::string& zoneId, float seconds);
    bool SetLateReverbGain(const std::string& zoneId, float gainDb);
    bool SetDiffusion(const std::string& zoneId, float diffusion);
    bool SetDensity(const std::string& zoneId, float density);

    // Blend settings
    bool SetBlendRadius(const std::string& zoneId, float radius);
    bool SetBlendCurve(const std::string& zoneId, BlendCurve curve);
    bool SetBlendWeight(const std::string& zoneId, float weight);

    // Frequency settings
    bool SetRoomGain(const std::string& zoneId, float gainDb);
    bool SetAirAbsorption(const std::string& zoneId, bool enabled, float gainHF = -5.0f);

    // Queries
    int GetZoneCount() const { return static_cast<int>(m_zones.size()); }
    const ReverbZoneRecord* GetZone(const std::string& zoneId) const;
    std::vector<std::string> GetZoneIds() const;
    std::vector<std::string> GetZonesByScene(const std::string& sceneId) const;
    std::vector<std::string> GetZonesByPreset(ReverbPreset preset) const;
    std::vector<std::string> GetZonesAtPoint(float x, float y, float z) const;
    std::vector<std::string> GetEnabledZoneIds() const;

    // Persistence
    bool SaveZones(const std::string& filePath) const;
    bool LoadZones(const std::string& filePath);
    void ClearAll();

private:
    bool m_active{false};
    std::unordered_map<std::string, ReverbZoneRecord> m_zones;
    int m_nextZoneIndex{0};
};

} // namespace Atlas::Editor
