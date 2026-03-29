#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P28 Tool — Sound wave visualization, spectrum analysis, and audio debug overlays.
class SoundVisualizerTool : public ITool {
public:
    enum class VisMode { Waveform, Spectrum, Waterfall, Oscilloscope, VUMeter, Custom };
    enum class FreqScale { Linear, Log, Mel, Bark, Custom };
    enum class WindowFunction { Rectangular, Hamming, Hanning, Blackman, Custom };
    enum class OverlayType { Spatialization, Attenuation, Reverb, Occlusion, Custom };

    struct WaveformVisDef {
        std::string visId;
        std::string audioAssetId;
        VisMode visMode{VisMode::Waveform};
        WindowFunction windowFunc{WindowFunction::Hamming};
        int fftSize{1024};
        float displayGain{1.0f};
        float scrollSpeed{1.0f};
        bool showGrid{true};
        bool enabled{true};
    };

    struct SpectrumAnalyzerDef {
        std::string analyzerId;
        std::string audioAssetId;
        FreqScale freqScale{FreqScale::Log};
        int bandCount{64};
        float minFreqHz{20.0f};
        float maxFreqHz{20000.0f};
        float peakHoldMs{1000.0f};
        bool showPeaks{true};
        bool enabled{true};
    };

    struct AudioOverlayDef {
        std::string overlayId;
        std::string audioSourceId;
        OverlayType overlayType{OverlayType::Spatialization};
        float opacity{0.8f};
        float displayRadius{500.0f};
        bool showLabels{true};
        bool showConnections{false};
        bool enabled{true};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "SoundVisualizerTool"; }
    bool IsActive() const override { return m_active; }

    bool CreateWaveformVis(const WaveformVisDef& def);
    bool DeleteWaveformVis(const std::string& visId);
    bool EnableWaveformVis(const std::string& visId, bool enabled);
    bool SetVisMode(const std::string& visId, VisMode mode);
    const WaveformVisDef* GetWaveformVis(const std::string& visId) const;
    std::vector<std::string> GetAllWaveformVisIds() const;
    std::vector<std::string> GetWaveformVisByMode(VisMode mode) const;
    std::vector<std::string> GetEnabledWaveformVis() const;
    bool AddSpectrumAnalyzer(const std::string& audioAssetId, const SpectrumAnalyzerDef& def);
    bool RemoveSpectrumAnalyzer(const std::string& analyzerId);
    bool SetFreqScale(const std::string& analyzerId, FreqScale scale);
    const SpectrumAnalyzerDef* GetSpectrumAnalyzer(const std::string& analyzerId) const;
    std::vector<std::string> GetAllAnalyzerIds() const;
    std::vector<std::string> GetAnalyzersByScale(FreqScale scale) const;
    bool AddOverlay(const std::string& audioSourceId, const AudioOverlayDef& def);
    bool RemoveOverlay(const std::string& overlayId);
    bool EnableOverlay(const std::string& overlayId, bool enabled);
    const AudioOverlayDef* GetOverlay(const std::string& overlayId) const;
    std::vector<std::string> GetAllOverlayIds() const;
    std::vector<std::string> GetOverlaysByType(OverlayType type) const;
    void Reset();

private:
    bool m_active{false};
    std::unordered_map<std::string, WaveformVisDef> m_waveformVis;
    std::unordered_map<std::string, SpectrumAnalyzerDef> m_analyzers;
    std::unordered_map<std::string, AudioOverlayDef> m_overlays;
};

} // namespace Atlas::Editor
