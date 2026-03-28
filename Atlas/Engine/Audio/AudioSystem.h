// AudioSystem.h
// Atlas Engine — extended audio system: sound events, categories/groups,
// spatial (3D) audio, audio bus mixing, and emitter registration.

#pragma once
#include "Audio/AudioEngine.h"

#include <array>
#include <functional>
#include <optional>
#include <string>
#include <unordered_map>
#include <vector>

namespace atlas::audio {

// ---------------------------------------------------------------------------
// Audio categories (mix-bus groups)
// ---------------------------------------------------------------------------

enum class EAudioCategory : uint8_t
{
    Master,
    Music,
    SFX,
    Voice,
    Ambient,
    UI,
};

// ---------------------------------------------------------------------------
// Sound event definition
// ---------------------------------------------------------------------------

struct SoundEventDef
{
    std::string      eventId;
    std::string      assetPath;   ///< relative audio asset path
    EAudioCategory   category      = EAudioCategory::SFX;
    float            baseVolume    = 1.0f;
    float            basePitch     = 1.0f;
    float            pitchVariance = 0.0f; ///< ± random variance
    float            minDistance   = 1.0f;  ///< spatial: full volume below this
    float            maxDistance   = 100.f; ///< spatial: silent beyond this
    bool             looping       = false;
    bool             is3D          = false;
};

// ---------------------------------------------------------------------------
// Playing sound instance
// ---------------------------------------------------------------------------

struct SoundInstance
{
    std::string    eventId;
    SoundID        sourceId   = 0;
    uint64_t       entityId   = 0; ///< emitter entity (0 = world / 2D)
    bool           is3D       = false;
    float          posX = 0.f, posY = 0.f, posZ = 0.f;
    EAudioCategory category   = EAudioCategory::SFX;
};

// ---------------------------------------------------------------------------
// Listener (camera / player position for 3D panning)
// ---------------------------------------------------------------------------

struct AudioListener
{
    float posX = 0.f, posY = 0.f, posZ = 0.f;
    float forwardX = 0.f, forwardY = 0.f, forwardZ = -1.f;
    float upX = 0.f, upY = 1.f, upZ = 0.f;
};

// ---------------------------------------------------------------------------
// AudioSystem
// ---------------------------------------------------------------------------

class AudioSystem
{
public:
    AudioSystem()  = default;
    ~AudioSystem() = default;

    bool Initialize(AudioEngine& engine);
    void Shutdown();
    void Update(float deltaSeconds);

    // ---- sound event registration ------------------------------------
    void           RegisterEvent(const SoundEventDef& def);
    bool           HasEvent(const std::string& eventId) const;
    std::optional<SoundEventDef> GetEventDef(const std::string& eventId) const;

    // ---- playback -------------------------------------------------------
    SoundID PlayEvent(const std::string& eventId);
    SoundID PlayEvent3D(const std::string& eventId,
                         float x, float y, float z,
                         uint64_t entityId = 0);
    void    StopEvent(SoundID instanceId);
    void    StopAllInCategory(EAudioCategory category);

    // ---- category volume (bus mixing) ----------------------------------
    void  SetCategoryVolume(EAudioCategory category, float volume);
    float GetCategoryVolume(EAudioCategory category) const;

    // ---- listener position (spatial audio) ----------------------------
    void SetListener(const AudioListener& listener);
    const AudioListener& GetListener() const { return m_listener; }

    // ---- spatial attenuation helper -----------------------------------
    float ComputeAttenuation(float distance,
                              float minDist, float maxDist) const;

    // ---- entity emitter registration ----------------------------------
    void UpdateEmitterPosition(uint64_t entityId, float x, float y, float z);
    void UnregisterEmitter(uint64_t entityId);

    // ---- playing instances query -------------------------------------------
    const std::vector<SoundInstance>& GetInstances() const { return m_instances; }
    size_t PlayingCount() const;

private:
    AudioEngine*                              m_engine     = nullptr;
    std::vector<SoundEventDef>                m_events;
    std::vector<SoundInstance>                m_instances;
    std::unordered_map<uint8_t, float>        m_categoryVolumes;
    std::unordered_map<uint64_t, std::array<float, 3>> m_emitterPositions;
    AudioListener                             m_listener;

    const SoundEventDef* FindEvent(const std::string& eventId) const;
    void ApplyAttenuation(SoundInstance& inst);
};

} // namespace atlas::audio
