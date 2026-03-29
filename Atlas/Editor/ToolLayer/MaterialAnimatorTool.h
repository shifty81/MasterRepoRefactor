#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P12 Tool — Material property animation timeline for shader and surface effects.
class MaterialAnimatorTool : public ITool {
public:
    enum class PropertyType { Float, Color, Vector2, Vector3, Vector4, Texture };
    enum class InterpolationType { Step, Linear, CubicBezier, EaseIn, EaseOut, EaseInOut };
    enum class PlayMode { Once, Loop, PingPong, ClampForever };

    struct ColorValue {
        float r{1.0f};
        float g{1.0f};
        float b{1.0f};
        float a{1.0f};
    };

    struct Keyframe {
        std::string keyframeId;
        float time{0.0f};
        PropertyType type{PropertyType::Float};
        float floatValue{0.0f};
        ColorValue colorValue;
        float vectorX{0.0f};
        float vectorY{0.0f};
        float vectorZ{0.0f};
        float vectorW{0.0f};
        std::string textureId;
        InterpolationType interpolation{InterpolationType::Linear};
        float tangentIn{0.0f};
        float tangentOut{0.0f};
    };

    struct PropertyTrack {
        std::string trackId;
        std::string propertyName;
        PropertyType type{PropertyType::Float};
        std::string materialId;
        std::string materialSlot;
        std::vector<Keyframe> keyframes;
        bool enabled{true};
        bool locked{false};
    };

    struct MaterialAnimation {
        std::string animationId;
        std::string name;
        std::string materialId;
        float duration{1.0f};
        float currentTime{0.0f};
        PlayMode playMode{PlayMode::Loop};
        float playbackSpeed{1.0f};
        bool playing{false};
        std::vector<std::string> trackIds;
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "MaterialAnimatorTool"; }
    bool IsActive() const override { return m_active; }

    // Animation management
    std::string CreateAnimation(const std::string& name,
                                  const std::string& materialId = "");
    bool RemoveAnimation(const std::string& animationId);
    bool SetMaterial(const std::string& animationId, const std::string& materialId);
    bool SetDuration(const std::string& animationId, float seconds);
    bool SetPlayMode(const std::string& animationId, PlayMode mode);
    bool SetPlaybackSpeed(const std::string& animationId, float speed);
    int GetAnimationCount() const { return static_cast<int>(m_animations.size()); }
    const MaterialAnimation* GetAnimation(const std::string& animationId) const;
    std::vector<std::string> GetAnimationIds() const;

    // Track management
    std::string AddTrack(const std::string& animationId,
                          const std::string& propertyName,
                          PropertyType type = PropertyType::Float,
                          const std::string& materialSlot = "");
    bool RemoveTrack(const std::string& animationId, const std::string& trackId);
    bool SetTrackEnabled(const std::string& animationId, const std::string& trackId,
                          bool enabled);
    bool SetTrackLocked(const std::string& animationId, const std::string& trackId,
                         bool locked);
    int GetTrackCount(const std::string& animationId) const;
    const PropertyTrack* GetTrack(const std::string& animationId,
                                    const std::string& trackId) const;

    // Keyframe management
    std::string AddFloatKeyframe(const std::string& animationId,
                                  const std::string& trackId,
                                  float time, float value,
                                  InterpolationType interp = InterpolationType::Linear);
    std::string AddColorKeyframe(const std::string& animationId,
                                  const std::string& trackId,
                                  float time,
                                  float r, float g, float b, float a,
                                  InterpolationType interp = InterpolationType::Linear);
    std::string AddVectorKeyframe(const std::string& animationId,
                                    const std::string& trackId,
                                    float time,
                                    float x, float y, float z = 0.0f, float w = 0.0f,
                                    InterpolationType interp = InterpolationType::Linear);
    bool RemoveKeyframe(const std::string& animationId, const std::string& trackId,
                         const std::string& keyframeId);
    bool MoveKeyframe(const std::string& animationId, const std::string& trackId,
                       const std::string& keyframeId, float newTime);
    bool SetKeyframeInterpolation(const std::string& animationId,
                                    const std::string& trackId,
                                    const std::string& keyframeId,
                                    InterpolationType interp);
    int GetKeyframeCount(const std::string& animationId,
                          const std::string& trackId) const;

    // Playback
    bool Play(const std::string& animationId);
    bool Pause(const std::string& animationId);
    bool Stop(const std::string& animationId);
    bool Seek(const std::string& animationId, float time);
    float GetCurrentTime(const std::string& animationId) const;
    bool IsPlaying(const std::string& animationId) const;

    // Persistence
    bool SaveAnimations(const std::string& filePath) const;
    bool LoadAnimations(const std::string& filePath);
    void ClearAll();

private:
    bool m_active{false};
    std::unordered_map<std::string, MaterialAnimation> m_animations;
    std::unordered_map<std::string, PropertyTrack> m_tracks;
    int m_nextAnimIndex{0};
    int m_nextTrackIndex{0};
    int m_nextKeyframeIndex{0};
};

} // namespace Atlas::Editor
