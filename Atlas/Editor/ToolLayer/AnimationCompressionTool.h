#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P27 Tool — Animation compression scheme authoring, codec selection, and quality preview.
class AnimationCompressionTool : public ITool {
public:
    enum class CompressionCodec { None, Linear, Constant, ACL, Custom };
    enum class CompressionQuality { Lowest, Low, Medium, High, Lossless, Custom };
    enum class TrackType { Rotation, Translation, Scale, Morph, Custom };
    enum class KeyReductionMethod { None, Linear, Cubic, PerBone, Adaptive, Custom };

    struct CompressionSchemeDef {
        std::string schemeId;
        std::string schemeName;
        CompressionCodec codec{CompressionCodec::ACL};
        CompressionQuality quality{CompressionQuality::Medium};
        KeyReductionMethod keyReduction{KeyReductionMethod::Linear};
        float errorThreshold{0.01f};
        float rotationTolerance{0.0001f};
        float translationTolerance{0.001f};
        bool stripAdditiveRefPose{false};
        bool enabled{true};
    };

    struct TrackCompressionDef {
        std::string trackCompId;
        std::string schemeId;
        TrackType trackType{TrackType::Rotation};
        std::string boneName;
        CompressionCodec overrideCodec{CompressionCodec::None};
        CompressionQuality overrideQuality{CompressionQuality::Medium};
        bool useOverride{false};
        bool enabled{true};
    };

    struct CompressionPreviewDef {
        std::string previewId;
        std::string schemeId;
        std::string animationAssetId;
        float originalSizeKB{0.0f};
        float compressedSizeKB{0.0f};
        float maxError{0.0f};
        float avgError{0.0f};
        bool previewGenerated{false};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "AnimationCompressionTool"; }
    bool IsActive() const override { return m_active; }

    bool CreateScheme(const CompressionSchemeDef& def);
    bool DeleteScheme(const std::string& schemeId);
    bool SetCodec(const std::string& schemeId, CompressionCodec codec);
    bool SetQuality(const std::string& schemeId, CompressionQuality quality);
    const CompressionSchemeDef* GetScheme(const std::string& schemeId) const;
    std::vector<std::string> GetAllSchemeIds() const;
    std::vector<std::string> GetSchemesByCodec(CompressionCodec codec) const;
    std::vector<std::string> GetSchemesByQuality(CompressionQuality quality) const;
    bool AddTrackCompression(const std::string& schemeId, const TrackCompressionDef& def);
    bool RemoveTrackCompression(const std::string& schemeId, const std::string& trackCompId);
    bool EnableTrackOverride(const std::string& trackCompId, bool enable);
    const TrackCompressionDef* GetTrackCompression(const std::string& trackCompId) const;
    std::vector<std::string> GetTrackCompressionsByScheme(const std::string& schemeId) const;
    std::vector<std::string> GetTrackCompressionsByType(TrackType type) const;
    bool GeneratePreview(const CompressionPreviewDef& def);
    bool DeletePreview(const std::string& previewId);
    const CompressionPreviewDef* GetPreview(const std::string& previewId) const;
    std::vector<std::string> GetPreviewsByScheme(const std::string& schemeId) const;
    std::vector<std::string> GetGeneratedPreviews() const;
    void Reset();

private:
    bool m_active{false};
    std::unordered_map<std::string, CompressionSchemeDef> m_schemes;
    std::unordered_map<std::string, TrackCompressionDef> m_trackCompressions;
    std::unordered_map<std::string, CompressionPreviewDef> m_previews;
};

} // namespace Atlas::Editor
