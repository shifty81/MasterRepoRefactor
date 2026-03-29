#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P26 Tool — Audio spatialization config, HRTF profiles, and reverb zone authoring.
class AudioSpatializationTool : public ITool {
public:
    enum class SpatializationAlgorithm { HRTF, Panning, Binaural, Ambisonics, Custom };
    enum class AttenuationModel { Linear, Logarithmic, Inverse, Custom };
    enum class ReverbPreset { Cave, Hall, Room, Cathedral, Stadium, Outdoor, Underwater, Custom };
    enum class OcclusionType { None, RayTrace, Portal, Volume, Custom };

    struct SpatializationProfileDef {
        std::string profileId;
        std::string profileName;
        SpatializationAlgorithm algorithm{SpatializationAlgorithm::HRTF};
        AttenuationModel attenuation{AttenuationModel::Logarithmic};
        float minDistance{10.0f};
        float maxDistance{5000.0f};
        float dopplerFactor{1.0f};
        bool enableOcclusion{true};
        OcclusionType occlusionType{OcclusionType::RayTrace};
    };

    struct ReverbZoneDef {
        std::string reverbZoneId;
        std::string zoneName;
        ReverbPreset preset{ReverbPreset::Room};
        float posX{0.0f};
        float posY{0.0f};
        float posZ{0.0f};
        float radius{500.0f};
        float dryMix{1.0f};
        float wetMix{0.5f};
        float decayTime{1.5f};
        bool enabled{true};
    };

    struct AudioSourceBindingDef {
        std::string bindingId;
        std::string sourceId;
        std::string profileId;
        std::string reverbZoneId;
        float spatialBlend{1.0f};
        bool override3DSettings{false};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "AudioSpatializationTool"; }
    bool IsActive() const override { return m_active; }

    bool CreateProfile(const SpatializationProfileDef& def);
    bool DeleteProfile(const std::string& profileId);
    bool SetAlgorithm(const std::string& profileId, SpatializationAlgorithm algorithm);
    const SpatializationProfileDef* GetProfile(const std::string& profileId) const;
    std::vector<std::string> GetAllProfileIds() const;
    std::vector<std::string> GetProfilesByAlgorithm(SpatializationAlgorithm algorithm) const;
    bool CreateReverbZone(const ReverbZoneDef& def);
    bool DeleteReverbZone(const std::string& reverbZoneId);
    bool SetReverbPreset(const std::string& reverbZoneId, ReverbPreset preset);
    bool EnableReverbZone(const std::string& reverbZoneId, bool enabled);
    const ReverbZoneDef* GetReverbZone(const std::string& reverbZoneId) const;
    std::vector<std::string> GetAllReverbZoneIds() const;
    std::vector<std::string> GetReverbZonesByPreset(ReverbPreset preset) const;
    std::vector<std::string> GetEnabledReverbZones() const;
    bool BindAudioSource(const AudioSourceBindingDef& binding);
    bool UnbindAudioSource(const std::string& bindingId);
    const AudioSourceBindingDef* GetBinding(const std::string& bindingId) const;
    std::vector<std::string> GetBindingsBySource(const std::string& sourceId) const;
    std::vector<std::string> GetBindingsByProfile(const std::string& profileId) const;
    void Reset();

private:
    bool m_active{false};
    std::unordered_map<std::string, SpatializationProfileDef> m_profiles;
    std::unordered_map<std::string, ReverbZoneDef> m_reverbZones;
    std::unordered_map<std::string, AudioSourceBindingDef> m_bindings;
};

} // namespace Atlas::Editor
