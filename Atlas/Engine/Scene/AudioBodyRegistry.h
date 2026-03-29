#pragma once
#include <string>
#include <vector>
#include <unordered_map>
#include <functional>

namespace Atlas::Engine {

/// Phase 27D — Registry for 3D audio body definitions used by the spatial audio subsystem.
/// Manages audio source metadata, attenuation curves, occlusion zones, and listener
/// configurations for runtime and authoring time spatial audio scene setup.
class AudioBodyRegistry {
public:
    enum class AudioBodyState { Inactive, Active, Playing, Paused, Stopped };
    enum class AudioSourceType { Point, Area, Ambient, Directional, Surface };
    enum class AttenuationModel { None, Linear, InverseDistance, Exponential, Custom };
    enum class OcclusionType { None, Raycast, Portal, Geometry };
    enum class AudioLayer { Master, Music, SFX, Voice, UI, Ambient, Custom };
    enum class ReverbZoneBlend { None, Additive, Override };

    struct AttenuationCurve {
        AttenuationModel model{AttenuationModel::InverseDistance};
        float minDistance{1.0f};
        float maxDistance{50.0f};
        float rolloffFactor{1.0f};
        float referenceDistance{1.0f};
        bool useCustomCurve{false};
    };

    struct OcclusionSettings {
        OcclusionType type{OcclusionType::Raycast};
        float occlusionFactor{0.5f};
        float obstacleGainLF{0.1f};
        float obstacleGainHF{0.01f};
        bool enabled{true};
        int raycastSamples{4};
    };

    struct DopplerSettings {
        bool enabled{false};
        float dopplerLevel{1.0f};
        float speedOfSound{343.0f};
    };

    struct AudioBodyRecord {
        std::string bodyId;
        std::string name;
        AudioSourceType sourceType{AudioSourceType::Point};
        AudioBodyState state{AudioBodyState::Inactive};
        AudioLayer layer{AudioLayer::SFX};
        AttenuationCurve attenuation;
        OcclusionSettings occlusion;
        DopplerSettings doppler;
        float volumeDb{0.0f};
        float pitchSemitones{0.0f};
        float posX{0.0f};
        float posY{0.0f};
        float posZ{0.0f};
        float directionX{0.0f};
        float directionY{0.0f};
        float directionZ{-1.0f};
        float coneInnerAngle{360.0f};
        float coneOuterAngle{360.0f};
        float coneOuterGainDb{-6.0f};
        bool loop{false};
        bool playOnActivate{false};
        bool spatialize{true};
        float bypassEffectsGain{0.0f};
        ReverbZoneBlend reverbBlend{ReverbZoneBlend::Additive};
        std::string audioClipId;
        std::string linkedEntityId;
        std::string sceneId;
        int priority{128};
        bool alwaysPlay{false};
    };

    struct ReverbZoneRecord {
        std::string zoneId;
        std::string name;
        float posX{0.0f};
        float posY{0.0f};
        float posZ{0.0f};
        float radius{10.0f};
        float minDistance{8.0f};
        float reverbRoom{-1000.0f};
        float reverbRoomHF{-100.0f};
        float decayTime{1.49f};
        float reflectionsGainDb{-2602.0f};
        std::string presetName;
        bool enabled{true};
    };

    // Body registration
    bool RegisterBody(const AudioBodyRecord& record);
    bool UnregisterBody(const std::string& bodyId);
    bool UpdateBody(const std::string& bodyId, const AudioBodyRecord& record);
    bool SetBodyState(const std::string& bodyId, AudioBodyState state);
    bool SetBodyVolume(const std::string& bodyId, float db);
    bool SetBodyPitch(const std::string& bodyId, float semitones);
    bool SetBodyPosition(const std::string& bodyId, float x, float y, float z);
    bool SetBodyDirection(const std::string& bodyId, float dx, float dy, float dz);
    bool SetAttenuationModel(const std::string& bodyId, AttenuationModel model);
    bool SetAttenuationRange(const std::string& bodyId,
                               float minDist, float maxDist);
    bool SetOcclusionEnabled(const std::string& bodyId, bool enabled);
    bool SetDopplerEnabled(const std::string& bodyId, bool enabled);
    bool SetLoop(const std::string& bodyId, bool loop);
    bool SetSpatialize(const std::string& bodyId, bool spatialize);
    bool SetAudioClip(const std::string& bodyId, const std::string& clipId);
    bool SetAudioLayer(const std::string& bodyId, AudioLayer layer);
    bool SetPriority(const std::string& bodyId, int priority);
    bool SetAlwaysPlay(const std::string& bodyId, bool alwaysPlay);
    bool SetPlayOnActivate(const std::string& bodyId, bool playOnActivate);
    bool SetScene(const std::string& bodyId, const std::string& sceneId);
    bool LinkToEntity(const std::string& bodyId, const std::string& entityId);
    int GetRegisteredCount() const { return static_cast<int>(m_bodies.size()); }
    bool IsRegistered(const std::string& bodyId) const;
    const AudioBodyRecord* GetBody(const std::string& bodyId) const;
    std::vector<std::string> GetAllBodyIds() const;
    std::vector<std::string> GetBodiesByScene(const std::string& sceneId) const;
    std::vector<std::string> GetBodiesByLayer(AudioLayer layer) const;
    std::vector<std::string> GetBodiesByType(AudioSourceType type) const;
    std::vector<std::string> GetActiveBodies() const;
    std::vector<std::string> GetAlwaysPlayBodies() const;

    // Activation
    bool ActivateBody(const std::string& bodyId);
    bool DeactivateBody(const std::string& bodyId);
    bool PlayBody(const std::string& bodyId);
    bool PauseBody(const std::string& bodyId);
    bool StopBody(const std::string& bodyId);
    int GetActiveCount() const;
    int GetPlayingCount() const;
    void ActivateAllInScene(const std::string& sceneId);
    void DeactivateAllInScene(const std::string& sceneId);
    void ActivateAlwaysPlay();

    // Reverb zones
    bool RegisterReverbZone(const ReverbZoneRecord& zone);
    bool UnregisterReverbZone(const std::string& zoneId);
    bool SetReverbZoneEnabled(const std::string& zoneId, bool enabled);
    int GetReverbZoneCount() const { return static_cast<int>(m_reverbZones.size()); }
    const ReverbZoneRecord* GetReverbZone(const std::string& zoneId) const;
    std::vector<std::string> GetReverbZoneIds() const;
    std::vector<std::string> GetReverbZonesInRange(float x, float y, float z,
                                                     float radius) const;

    // Callbacks
    using StateChangedCallback = std::function<void(const std::string&, AudioBodyState)>;
    void SetOnStateChangedCallback(StateChangedCallback cb);

    // Persistence
    bool SaveRegistry(const std::string& filePath) const;
    bool LoadRegistry(const std::string& filePath);
    void Clear();

private:
    std::unordered_map<std::string, AudioBodyRecord> m_bodies;
    std::unordered_map<std::string, ReverbZoneRecord> m_reverbZones;
    StateChangedCallback m_onStateChanged;
};

} // namespace Atlas::Engine
