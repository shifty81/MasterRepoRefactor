#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P16 Tool — Sound occlusion, reverb zone authoring, and acoustic environment management.
class SoundOcclusionTool : public ITool {
public:
    enum class OcclusionMethod { Raycast, Portal, Geometry, Combined };
    enum class ReverbPreset { None, Room, Hall, Cathedral, Cave, Forest, Urban, Custom };
    enum class PropagationModel { Simple, HRTF, Binaural, Ambisonics };

    struct OcclusionVolume {
        std::string volumeId;
        std::string name;
        OcclusionMethod method{OcclusionMethod::Raycast};
        float attenuationFactor{0.5f};
        float lowPassFreq{5000.0f};
        std::vector<float> position;
        std::vector<float> extents;
    };

    struct ReverbZone {
        std::string zoneId;
        std::string name;
        ReverbPreset preset{ReverbPreset::Room};
        float decayTime{1.5f};
        float density{0.8f};
        float diffusion{0.9f};
        float earlyReflections{0.0f};
        float lateReflections{-6.0f};
        float blendRadius{5.0f};
    };

    struct AcousticProfile {
        std::string profileId;
        std::string name;
        PropagationModel propagationModel{PropagationModel::Simple};
        float maxPropagationDist{5000.0f};
        float roomSize{100.0f};
        float absorption{0.3f};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "SoundOcclusionTool"; }
    bool IsActive() const override { return m_active; }

    std::string CreateOcclusionVolume(const std::string& name, OcclusionMethod method = OcclusionMethod::Raycast);
    bool RemoveOcclusionVolume(const std::string& volumeId);
    std::string CreateReverbZone(const std::string& name, ReverbPreset preset = ReverbPreset::Room);
    bool RemoveReverbZone(const std::string& zoneId);
    bool SetOcclusionMethod(const std::string& volumeId, OcclusionMethod method);
    bool SetReverbPreset(const std::string& zoneId, ReverbPreset preset);
    bool SetAcousticProfile(const AcousticProfile& profile);
    bool SimulateOcclusion(const std::string& volumeId);
    bool SimulateReverb(const std::string& zoneId);
    const OcclusionVolume* GetOcclusionVolume(const std::string& volumeId) const;
    const ReverbZone* GetReverbZone(const std::string& zoneId) const;
    std::vector<std::string> GetAllOcclusionIds() const;
    std::vector<std::string> GetAllReverbIds() const;
    bool ValidateAcoustics() const;
    bool ExportAcousticConfig(const std::string& filePath) const;
    bool SaveOcclusion(const std::string& filePath) const;
    bool LoadOcclusion(const std::string& filePath);
    void ClearAll();

private:
    bool m_active{false};
    std::unordered_map<std::string, OcclusionVolume> m_occlusionVolumes;
    std::unordered_map<std::string, ReverbZone> m_reverbZones;
    std::unordered_map<std::string, AcousticProfile> m_acousticProfiles;
    int m_nextVolumeIndex{0};
    int m_nextZoneIndex{0};
};

} // namespace Atlas::Editor
