#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P24 Tool — Per-pixel GBuffer inspection, HDR value readback, and color space analysis.
class PixelInspectorTool : public ITool {
public:
    enum class InspectorChannel { BaseColor, Normal, Roughness, Metallic, Emissive, Depth, Custom };
    enum class ColorSpace { sRGB, Linear, ACEScg, Rec2020, Custom };
    enum class ReadbackMode { SinglePixel, Region, Continuous, Snapshot, Custom };
    enum class GBufferLayer { Layer0, Layer1, Layer2, Layer3, SceneDepth, Custom };

    struct PixelSampleDef {
        std::string sampleId;
        int pixelX{0};
        int pixelY{0};
        InspectorChannel channel{InspectorChannel::BaseColor};
        float r{0.0f};
        float g{0.0f};
        float b{0.0f};
        float a{0.0f};
        float depth{0.0f};
    };

    struct InspectorRegionDef {
        std::string regionId;
        int x{0};
        int y{0};
        int width{64};
        int height{64};
        ReadbackMode mode{ReadbackMode::SinglePixel};
        bool active{false};
    };

    struct ColorAnalysisResult {
        std::string analysisId;
        std::string regionId;
        ColorSpace colorSpace{ColorSpace::sRGB};
        float luminanceMin{0.0f};
        float luminanceMax{0.0f};
        float luminanceMean{0.0f};
        bool hdrClipping{false};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "PixelInspectorTool"; }
    bool IsActive() const override { return m_active; }

    void BeginInspection();
    void EndInspection();
    std::string CaptureSample(const PixelSampleDef& sample);
    const PixelSampleDef* GetSample(const std::string& sampleId) const;
    std::vector<std::string> GetAllSampleIds() const;
    std::vector<std::string> GetSamplesByChannel(InspectorChannel channel) const;
    std::string CreateRegion(const InspectorRegionDef& region);
    bool DeleteRegion(const std::string& regionId);
    const InspectorRegionDef* GetRegion(const std::string& regionId) const;
    std::vector<std::string> GetAllRegionIds() const;
    bool SetReadbackMode(const std::string& regionId, ReadbackMode mode);
    std::string AnalyzeRegion(const std::string& regionId);
    const ColorAnalysisResult* GetAnalysis(const std::string& analysisId) const;
    std::vector<std::string> GetAnalysisByRegion(const std::string& regionId) const;
    void ClearSamples();
    bool ExportSamples(const std::string& filePath) const;
    void Reset();

private:
    bool m_active{false};
    std::unordered_map<std::string, PixelSampleDef> m_samples;
    std::unordered_map<std::string, InspectorRegionDef> m_regions;
    std::unordered_map<std::string, ColorAnalysisResult> m_analyses;
};

} // namespace Atlas::Editor
