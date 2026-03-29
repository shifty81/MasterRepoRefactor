#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P12 Tool — Animation blend space authoring for 1D and 2D blend trees.
class AnimationBlendSpaceTool : public ITool {
public:
    enum class BlendSpaceType { OneDimensional, TwoDimensional };
    enum class BlendMode { Linear, Cartesian, Radial };
    enum class SampleInterpolation { Nearest, Linear, Hermite };
    enum class AxisType { Float, Int, Enum };

    struct BlendAxis {
        std::string axisId;
        std::string name;
        AxisType type{AxisType::Float};
        float minValue{0.0f};
        float maxValue{1.0f};
        float defaultValue{0.0f};
        float gridSize{0.1f};
        bool snapToGrid{true};
        std::string parameterName;  // bound animator parameter
    };

    struct BlendSample {
        std::string sampleId;
        std::string animationClipId;
        std::string animationClipPath;
        float axisX{0.0f};
        float axisY{0.0f};
        float weight{1.0f};
        float speed{1.0f};
        bool looping{true};
        bool mirrorX{false};
    };

    struct BlendSpace {
        std::string spaceId;
        std::string name;
        BlendSpaceType type{BlendSpaceType::TwoDimensional};
        BlendMode blendMode{BlendMode::Cartesian};
        SampleInterpolation interpolation{SampleInterpolation::Linear};
        BlendAxis axisX;
        BlendAxis axisY;
        std::vector<BlendSample> samples;
        float currentValueX{0.0f};
        float currentValueY{0.0f};
        bool normalizeBlendWeights{true};
        bool useVelocityBlending{false};
        float maxVelocity{10.0f};
        std::string linkedAnimatorId;
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "AnimationBlendSpaceTool"; }
    bool IsActive() const override { return m_active; }

    // Blend space management
    std::string CreateBlendSpace(const std::string& name,
                                   BlendSpaceType type = BlendSpaceType::TwoDimensional);
    bool RemoveBlendSpace(const std::string& spaceId);
    bool SetBlendSpaceType(const std::string& spaceId, BlendSpaceType type);
    bool SetBlendMode(const std::string& spaceId, BlendMode mode);
    bool SetInterpolation(const std::string& spaceId, SampleInterpolation interp);
    bool SetNormalizeWeights(const std::string& spaceId, bool normalize);
    bool SetVelocityBlending(const std::string& spaceId, bool enable,
                               float maxVelocity = 10.0f);
    bool LinkToAnimator(const std::string& spaceId, const std::string& animatorId);
    int GetBlendSpaceCount() const { return static_cast<int>(m_spaces.size()); }
    const BlendSpace* GetBlendSpace(const std::string& spaceId) const;
    std::vector<std::string> GetBlendSpaceIds() const;

    // Axis configuration
    bool SetAxisX(const std::string& spaceId, const std::string& name,
                   float minVal, float maxVal, float defaultVal = 0.0f);
    bool SetAxisY(const std::string& spaceId, const std::string& name,
                   float minVal, float maxVal, float defaultVal = 0.0f);
    bool SetAxisXParameter(const std::string& spaceId, const std::string& paramName);
    bool SetAxisYParameter(const std::string& spaceId, const std::string& paramName);
    bool SetAxisXGridSize(const std::string& spaceId, float gridSize);
    bool SetAxisYGridSize(const std::string& spaceId, float gridSize);

    // Sample management
    std::string AddSample(const std::string& spaceId,
                           const std::string& clipId,
                           float x, float y = 0.0f);
    bool RemoveSample(const std::string& spaceId, const std::string& sampleId);
    bool SetSampleClip(const std::string& spaceId, const std::string& sampleId,
                        const std::string& clipId,
                        const std::string& clipPath = "");
    bool SetSamplePosition(const std::string& spaceId, const std::string& sampleId,
                             float x, float y = 0.0f);
    bool SetSampleSpeed(const std::string& spaceId, const std::string& sampleId,
                         float speed);
    bool SetSampleLooping(const std::string& spaceId, const std::string& sampleId,
                           bool looping);
    bool SetSampleMirror(const std::string& spaceId, const std::string& sampleId,
                          bool mirrorX);
    int GetSampleCount(const std::string& spaceId) const;
    const BlendSample* GetSample(const std::string& spaceId,
                                   const std::string& sampleId) const;

    // Preview
    bool SetPreviewPosition(const std::string& spaceId, float x, float y = 0.0f);
    bool PreviewBlendSpace(const std::string& spaceId);
    float GetCurrentAxisX(const std::string& spaceId) const;
    float GetCurrentAxisY(const std::string& spaceId) const;
    std::vector<std::pair<std::string, float>> GetBlendWeights(
        const std::string& spaceId) const;

    // Persistence
    bool SaveBlendSpaces(const std::string& filePath) const;
    bool LoadBlendSpaces(const std::string& filePath);
    void ClearAll();

private:
    bool m_active{false};
    std::unordered_map<std::string, BlendSpace> m_spaces;
    int m_nextSpaceIndex{0};
    int m_nextSampleIndex{0};
};

} // namespace Atlas::Editor
