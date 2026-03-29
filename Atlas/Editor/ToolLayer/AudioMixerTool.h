#pragma once
#include "ITool.h"
#include <string>
#include <vector>

namespace Atlas::Editor {

/// P9 Tool — Audio bus routing and mixing authoring tool.
class AudioMixerTool : public ITool {
public:
    enum class BusType { Master, Submix, Aux, Send };
    enum class EffectSlotType { EQ, Compressor, Reverb, Delay, Limiter, Chorus, Distortion };
    enum class PanLaw { Linear, ConstantPower, Balanced };

    struct MixerEffect {
        std::string effectId;
        EffectSlotType type{EffectSlotType::EQ};
        bool enabled{true};
        float wet{1.0f};
        float dry{0.0f};
        std::string presetName;
    };

    struct MixerBus {
        std::string busId;
        std::string name;
        BusType type{BusType::Submix};
        float volume{1.0f};
        float pan{0.0f};
        float sendLevel{1.0f};
        bool muted{false};
        bool soloed{false};
        std::string parentBusId;
        std::vector<std::string> childBusIds;
        std::vector<MixerEffect> effects;
        PanLaw panLaw{PanLaw::ConstantPower};
        int channelCount{2};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "AudioMixerTool"; }
    bool IsActive() const override { return m_active; }

    // Bus management
    std::string CreateBus(const std::string& name, BusType type = BusType::Submix,
                           const std::string& parentBusId = "");
    bool RemoveBus(const std::string& busId);
    bool SetBusVolume(const std::string& busId, float volume);
    bool SetBusPan(const std::string& busId, float pan);
    bool SetBusMuted(const std::string& busId, bool muted);
    bool SetBusSoloed(const std::string& busId, bool soloed);
    bool SetBusParent(const std::string& busId, const std::string& parentBusId);
    bool SetBusPanLaw(const std::string& busId, PanLaw panLaw);
    bool SetBusChannelCount(const std::string& busId, int channels);
    int GetBusCount() const { return static_cast<int>(m_buses.size()); }
    const MixerBus* GetBus(const std::string& busId) const;
    std::vector<std::string> GetBusIds() const;
    std::vector<std::string> GetBusIdsByType(BusType type) const;
    std::string GetMasterBusId() const;

    // Bus routing
    bool AddSend(const std::string& fromBusId, const std::string& toBusId,
                  float level = 1.0f);
    bool RemoveSend(const std::string& fromBusId, const std::string& toBusId);
    bool SetSendLevel(const std::string& fromBusId, const std::string& toBusId,
                       float level);
    bool HasSend(const std::string& fromBusId, const std::string& toBusId) const;

    // Effects
    std::string AddEffect(const std::string& busId, EffectSlotType type,
                           float wet = 1.0f);
    bool RemoveEffect(const std::string& busId, const std::string& effectId);
    bool SetEffectEnabled(const std::string& busId, const std::string& effectId,
                           bool enabled);
    bool SetEffectWet(const std::string& busId, const std::string& effectId,
                       float wet);
    bool SetEffectPreset(const std::string& busId, const std::string& effectId,
                          const std::string& presetName);
    int GetEffectCount(const std::string& busId) const;

    // Metering / monitoring
    float GetPeakLevel(const std::string& busId) const;
    float GetRMSLevel(const std::string& busId) const;
    bool ResetPeakHold(const std::string& busId);
    int GetSoloBusCount() const;
    int GetMutedBusCount() const;

    // Persistence
    bool SaveMix(const std::string& filePath) const;
    bool LoadMix(const std::string& filePath);
    void ClearAll();

private:
    bool m_active{false};
    std::vector<MixerBus> m_buses;
    std::string m_masterBusId;
    int m_nextBusIndex{0};
    int m_nextEffectIndex{0};
};

} // namespace Atlas::Editor
