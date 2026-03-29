#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P12 Tool — Sound effect design and synthesis authoring tool.
class SoundEffectDesignerTool : public ITool {
public:
    enum class SynthType { Oscillator, Sampler, Procedural, Granular };
    enum class Waveform { Sine, Square, Triangle, Sawtooth, Noise, Custom };
    enum class FilterType { LowPass, HighPass, BandPass, Notch, AllPass };
    enum class EnvelopeStage { Attack, Decay, Sustain, Release };
    enum class ModulationTarget { Pitch, Volume, Cutoff, Resonance, Pan };

    struct ADSREnvelope {
        float attackMs{10.0f};
        float decayMs{50.0f};
        float sustainLevel{0.7f};
        float releaseMs{200.0f};
    };

    struct FilterSettings {
        FilterType type{FilterType::LowPass};
        float cutoffHz{5000.0f};
        float resonance{0.5f};
        float driveDb{0.0f};
        bool enabled{true};
    };

    struct LFOSettings {
        std::string lfoId;
        Waveform waveform{Waveform::Sine};
        ModulationTarget target{ModulationTarget::Pitch};
        float frequencyHz{2.0f};
        float depth{0.1f};
        float phase{0.0f};
        bool synced{false};
        float syncBeatDivision{4.0f};
        bool enabled{true};
    };

    struct SoundLayer {
        std::string layerId;
        std::string name;
        SynthType synthType{SynthType::Oscillator};
        Waveform waveform{Waveform::Sine};
        float volumeDb{0.0f};
        float pitchSemitones{0.0f};
        float panL{0.0f};
        float panR{0.0f};
        float startTimeMs{0.0f};
        float durationMs{500.0f};
        ADSREnvelope adsr;
        FilterSettings filter;
        std::vector<LFOSettings> lfos;
        std::string samplePath;
        bool muted{false};
        bool soloed{false};
        bool reversed{false};
        float pitchShiftSemitones{0.0f};
    };

    struct SoundEffect {
        std::string effectId;
        std::string name;
        std::vector<std::string> layerIds;
        float masterVolumeDb{0.0f};
        float masterPitchSemitones{0.0f};
        float durationMs{500.0f};
        bool randomizePitch{false};
        float pitchRangeMin{-0.5f};
        float pitchRangeMax{0.5f};
        bool randomizeVolume{false};
        float volumeRangeDbMin{-3.0f};
        float volumeRangeDbMax{0.0f};
        std::string category;
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "SoundEffectDesignerTool"; }
    bool IsActive() const override { return m_active; }

    // Effect management
    std::string CreateEffect(const std::string& name);
    bool RemoveEffect(const std::string& effectId);
    bool SetMasterVolume(const std::string& effectId, float db);
    bool SetMasterPitch(const std::string& effectId, float semitones);
    bool SetRandomizePitch(const std::string& effectId, bool enable,
                            float min = -0.5f, float max = 0.5f);
    bool SetRandomizeVolume(const std::string& effectId, bool enable,
                             float minDb = -3.0f, float maxDb = 0.0f);
    bool SetCategory(const std::string& effectId, const std::string& category);
    int GetEffectCount() const { return static_cast<int>(m_effects.size()); }
    const SoundEffect* GetEffect(const std::string& effectId) const;
    std::vector<std::string> GetEffectIds() const;

    // Layer management
    std::string AddLayer(const std::string& effectId, const std::string& name,
                          SynthType synthType = SynthType::Oscillator);
    bool RemoveLayer(const std::string& effectId, const std::string& layerId);
    bool SetSynthType(const std::string& effectId, const std::string& layerId,
                       SynthType type);
    bool SetWaveform(const std::string& effectId, const std::string& layerId,
                      Waveform waveform);
    bool SetLayerVolume(const std::string& effectId, const std::string& layerId,
                         float db);
    bool SetLayerPitch(const std::string& effectId, const std::string& layerId,
                        float semitones);
    bool SetLayerDuration(const std::string& effectId, const std::string& layerId,
                           float ms);
    bool SetLayerStartTime(const std::string& effectId, const std::string& layerId,
                            float ms);
    bool SetLayerMuted(const std::string& effectId, const std::string& layerId,
                        bool muted);
    bool SetLayerSoloed(const std::string& effectId, const std::string& layerId,
                         bool soloed);
    bool SetLayerReversed(const std::string& effectId, const std::string& layerId,
                           bool reversed);
    bool SetSamplePath(const std::string& effectId, const std::string& layerId,
                        const std::string& path);
    int GetLayerCount(const std::string& effectId) const;

    // Envelope
    bool SetADSR(const std::string& effectId, const std::string& layerId,
                  float attackMs, float decayMs, float sustainLevel,
                  float releaseMs);

    // Filter
    bool SetFilter(const std::string& effectId, const std::string& layerId,
                    FilterType type, float cutoffHz, float resonance);
    bool SetFilterEnabled(const std::string& effectId, const std::string& layerId,
                           bool enabled);

    // LFO
    std::string AddLFO(const std::string& effectId, const std::string& layerId,
                        ModulationTarget target = ModulationTarget::Pitch);
    bool SetLFOFrequency(const std::string& effectId, const std::string& layerId,
                          const std::string& lfoId, float hz);
    bool SetLFODepth(const std::string& effectId, const std::string& layerId,
                      const std::string& lfoId, float depth);
    bool SetLFOEnabled(const std::string& effectId, const std::string& layerId,
                        const std::string& lfoId, bool enabled);

    // Preview
    bool PreviewEffect(const std::string& effectId);
    bool StopPreview();
    bool IsPreviewPlaying() const { return m_previewPlaying; }

    // Persistence
    bool SaveEffects(const std::string& filePath) const;
    bool LoadEffects(const std::string& filePath);
    void ClearAll();

private:
    bool m_active{false};
    bool m_previewPlaying{false};
    std::unordered_map<std::string, SoundEffect> m_effects;
    std::unordered_map<std::string, SoundLayer> m_layers;
    int m_nextEffectIndex{0};
    int m_nextLayerIndex{0};
    int m_nextLFOIndex{0};
};

} // namespace Atlas::Editor
