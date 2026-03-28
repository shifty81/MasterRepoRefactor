// AudioSystem.cpp
// Atlas Engine — extended audio system.

#include "Audio/AudioSystem.h"

#include <algorithm>
#include <cmath>

namespace atlas::audio {

bool AudioSystem::Initialize(AudioEngine& engine)
{
    m_engine = &engine;
    // Default category volumes = 1.0.
    for (uint8_t i = 0; i <= static_cast<uint8_t>(EAudioCategory::UI); ++i)
        m_categoryVolumes[i] = 1.0f;
    return true;
}

void AudioSystem::Shutdown()
{
    m_instances.clear();
    m_events.clear();
    m_emitterPositions.clear();
    m_engine = nullptr;
}

void AudioSystem::Update(float deltaSeconds)
{
    if (!m_engine) return;

    // Update emitter positions for 3D sounds.
    for (auto& inst : m_instances)
    {
        if (!inst.is3D) continue;
        auto it = m_emitterPositions.find(inst.entityId);
        if (it != m_emitterPositions.end())
        {
            inst.posX = it->second[0];
            inst.posY = it->second[1];
            inst.posZ = it->second[2];
            m_engine->SetPosition(inst.sourceId,
                                   inst.posX, inst.posY, inst.posZ);
        }
        ApplyAttenuation(inst);
    }

    m_engine->Update(deltaSeconds);

    // Remove stopped instances.
    m_instances.erase(
        std::remove_if(m_instances.begin(), m_instances.end(),
                       [this](const SoundInstance& i){
                           return m_engine->GetState(i.sourceId)
                                  == SoundState::Stopped; }),
        m_instances.end());
}

void AudioSystem::RegisterEvent(const SoundEventDef& def)
{
    for (auto& e : m_events)
        if (e.eventId == def.eventId) { e = def; return; }
    m_events.push_back(def);
}

bool AudioSystem::HasEvent(const std::string& eventId) const
{
    return FindEvent(eventId) != nullptr;
}

std::optional<SoundEventDef> AudioSystem::GetEventDef(const std::string& eventId) const
{
    const SoundEventDef* e = FindEvent(eventId);
    if (e) return *e;
    return std::nullopt;
}

SoundID AudioSystem::PlayEvent(const std::string& eventId)
{
    const SoundEventDef* def = FindEvent(eventId);
    if (!def || !m_engine) return 0;

    SoundID sid = m_engine->LoadSound(def->assetPath);
    m_engine->SetVolume(sid, def->baseVolume * GetCategoryVolume(def->category));
    m_engine->SetPitch(sid, def->basePitch);
    m_engine->SetLooping(sid, def->looping);
    m_engine->Play(sid);

    SoundInstance inst;
    inst.eventId  = eventId;
    inst.sourceId = sid;
    inst.is3D     = false;
    inst.category = def->category;
    m_instances.push_back(inst);
    return sid;
}

SoundID AudioSystem::PlayEvent3D(const std::string& eventId,
                                    float x, float y, float z,
                                    uint64_t entityId)
{
    const SoundEventDef* def = FindEvent(eventId);
    if (!def || !m_engine) return 0;

    SoundID sid = m_engine->LoadSound(def->assetPath);

    float dist = std::sqrt((x - m_listener.posX) * (x - m_listener.posX) +
                            (y - m_listener.posY) * (y - m_listener.posY) +
                            (z - m_listener.posZ) * (z - m_listener.posZ));
    float atten = ComputeAttenuation(dist, def->minDistance, def->maxDistance);
    m_engine->SetVolume(sid, def->baseVolume * atten * GetCategoryVolume(def->category));
    m_engine->SetPitch(sid, def->basePitch);
    m_engine->SetLooping(sid, def->looping);
    m_engine->SetPosition(sid, x, y, z);
    m_engine->Play(sid);

    SoundInstance inst;
    inst.eventId  = eventId;
    inst.sourceId = sid;
    inst.entityId = entityId;
    inst.is3D     = true;
    inst.posX     = x; inst.posY = y; inst.posZ = z;
    inst.category = def->category;
    m_instances.push_back(inst);
    return sid;
}

void AudioSystem::StopEvent(SoundID instanceId)
{
    if (m_engine) m_engine->Stop(instanceId);
}

void AudioSystem::StopAllInCategory(EAudioCategory category)
{
    for (const auto& inst : m_instances)
        if (inst.category == category && m_engine)
            m_engine->Stop(inst.sourceId);
}

void AudioSystem::SetCategoryVolume(EAudioCategory category, float volume)
{
    m_categoryVolumes[static_cast<uint8_t>(category)] = volume;
    // Reapply to all playing instances in this category.
    for (const auto& inst : m_instances)
    {
        if (inst.category != category || !m_engine) continue;
        const SoundEventDef* def = FindEvent(inst.eventId);
        if (def)
            m_engine->SetVolume(inst.sourceId,
                                 def->baseVolume * volume);
    }
}

float AudioSystem::GetCategoryVolume(EAudioCategory category) const
{
    auto it = m_categoryVolumes.find(static_cast<uint8_t>(category));
    return (it != m_categoryVolumes.end()) ? it->second : 1.0f;
}

void AudioSystem::SetListener(const AudioListener& listener)
{
    m_listener = listener;
}

float AudioSystem::ComputeAttenuation(float distance,
                                        float minDist,
                                        float maxDist) const
{
    if (distance <= minDist) return 1.0f;
    if (distance >= maxDist) return 0.0f;
    // Linear rolloff.
    return 1.0f - (distance - minDist) / (maxDist - minDist);
}

void AudioSystem::UpdateEmitterPosition(uint64_t entityId,
                                          float x, float y, float z)
{
    m_emitterPositions[entityId] = { x, y, z };
}

void AudioSystem::UnregisterEmitter(uint64_t entityId)
{
    m_emitterPositions.erase(entityId);
}

size_t AudioSystem::PlayingCount() const
{
    size_t c = 0;
    for (const auto& inst : m_instances)
        if (m_engine &&
            m_engine->GetState(inst.sourceId) == SoundState::Playing) ++c;
    return c;
}

void AudioSystem::ApplyAttenuation(SoundInstance& inst)
{
    const SoundEventDef* def = FindEvent(inst.eventId);
    if (!def || !m_engine) return;

    float dx = inst.posX - m_listener.posX;
    float dy = inst.posY - m_listener.posY;
    float dz = inst.posZ - m_listener.posZ;
    float dist = std::sqrt(dx*dx + dy*dy + dz*dz);
    float atten = ComputeAttenuation(dist, def->minDistance, def->maxDistance);
    m_engine->SetVolume(inst.sourceId,
                         def->baseVolume * atten *
                         GetCategoryVolume(def->category));
}

const SoundEventDef* AudioSystem::FindEvent(const std::string& eventId) const
{
    for (const auto& e : m_events)
        if (e.eventId == eventId) return &e;
    return nullptr;
}

} // namespace atlas::audio
