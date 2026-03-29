#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P9 Tool — Authoring tool for post-process effect volumes in the scene.
class PostProcessVolumeTool : public ITool {
public:
    enum class VolumeShape { Box, Sphere, Capsule, Global };
    enum class BlendMode { Additive, Override, Lerp };
    enum class EffectType {
        Bloom, DepthOfField, MotionBlur, ChromaticAberration,
        ColorGrading, ToneMapping, Vignette, LensFlare, SSAO, SSR
    };

    struct EffectParam {
        std::string paramId;
        std::string name;
        EffectType effectType{EffectType::Bloom};
        float value{1.0f};
        bool enabled{true};
        float weight{1.0f};
    };

    struct PostProcessVolume {
        std::string volumeId;
        std::string name;
        VolumeShape shape{VolumeShape::Box};
        BlendMode blendMode{BlendMode::Override};
        bool isGlobal{false};
        float blendRadius{1.0f};
        float blendWeight{1.0f};
        float priority{0.0f};
        float extentX{10.0f};
        float extentY{10.0f};
        float extentZ{10.0f};
        float posX{0.0f};
        float posY{0.0f};
        float posZ{0.0f};
        std::vector<EffectParam> effects;
        bool enabled{true};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "PostProcessVolumeTool"; }
    bool IsActive() const override { return m_active; }

    // Volume management
    std::string CreateVolume(const std::string& name,
                              VolumeShape shape = VolumeShape::Box,
                              bool isGlobal = false);
    bool RemoveVolume(const std::string& volumeId);
    bool SetVolumeShape(const std::string& volumeId, VolumeShape shape);
    bool SetVolumeExtent(const std::string& volumeId,
                          float ex, float ey, float ez);
    bool SetVolumePosition(const std::string& volumeId,
                            float px, float py, float pz);
    bool SetVolumeBlendRadius(const std::string& volumeId, float radius);
    bool SetVolumeBlendWeight(const std::string& volumeId, float weight);
    bool SetVolumeBlendMode(const std::string& volumeId, BlendMode mode);
    bool SetVolumePriority(const std::string& volumeId, float priority);
    bool SetVolumeEnabled(const std::string& volumeId, bool enabled);
    int GetVolumeCount() const { return static_cast<int>(m_volumes.size()); }
    const PostProcessVolume* GetVolume(const std::string& volumeId) const;
    std::vector<std::string> GetVolumeIds() const;
    std::vector<std::string> GetActiveVolumeIds() const;

    // Effect management
    std::string AddEffect(const std::string& volumeId, const std::string& name,
                           EffectType type, float value = 1.0f);
    bool RemoveEffect(const std::string& volumeId, const std::string& paramId);
    bool SetEffectValue(const std::string& volumeId, const std::string& paramId,
                         float value);
    bool SetEffectEnabled(const std::string& volumeId, const std::string& paramId,
                           bool enabled);
    bool SetEffectWeight(const std::string& volumeId, const std::string& paramId,
                          float weight);
    int GetEffectCount(const std::string& volumeId) const;

    // Spatial query
    std::vector<std::string> QueryPoint(float px, float py, float pz) const;
    std::vector<std::string> GetGlobalVolumes() const;

    // Persistence
    bool SaveVolumes(const std::string& filePath) const;
    bool LoadVolumes(const std::string& filePath);
    void ClearAll();

private:
    bool m_active{false};
    std::unordered_map<std::string, PostProcessVolume> m_volumes;
    int m_nextVolumeIndex{0};
    int m_nextEffectIndex{0};
};

} // namespace Atlas::Editor
