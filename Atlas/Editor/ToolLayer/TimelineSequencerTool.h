#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P9 Tool — General-purpose timeline sequencer for animating any scene property.
class TimelineSequencerTool : public ITool {
public:
    enum class InterpolationType { Linear, Step, Bezier, CatmullRom, EaseIn, EaseOut };
    enum class TrackType { Float, Vector3, Color, Bool, Event, Reference };
    enum class PlaybackState { Stopped, Playing, Paused, Scrubbing };

    struct Keyframe {
        std::string keyframeId;
        float time{0.0f};
        std::string value;           // serialised value (float/vec3/colour/etc.)
        InterpolationType interp{InterpolationType::Linear};
        float tangentIn{0.0f};
        float tangentOut{0.0f};
    };

    struct Track {
        std::string trackId;
        std::string name;
        TrackType type{TrackType::Float};
        std::string targetEntityId;
        std::string targetProperty;
        std::vector<Keyframe> keyframes;
        bool enabled{true};
        bool locked{false};
        bool solo{false};
        float defaultValue{0.0f};
    };

    struct Sequence {
        std::string sequenceId;
        std::string name;
        float duration{10.0f};
        float frameRate{30.0f};
        bool looping{false};
        std::vector<std::string> trackIds;
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "TimelineSequencerTool"; }
    bool IsActive() const override { return m_active; }

    // Sequence management
    std::string CreateSequence(const std::string& name, float duration = 10.0f,
                                float frameRate = 30.0f);
    bool RemoveSequence(const std::string& sequenceId);
    bool SetActiveSequence(const std::string& sequenceId);
    bool SetSequenceDuration(const std::string& sequenceId, float duration);
    bool SetSequenceFrameRate(const std::string& sequenceId, float fps);
    bool SetSequenceLooping(const std::string& sequenceId, bool loop);
    int GetSequenceCount() const { return static_cast<int>(m_sequences.size()); }
    const Sequence* GetSequence(const std::string& sequenceId) const;
    std::vector<std::string> GetSequenceIds() const;

    // Track management
    std::string AddTrack(const std::string& sequenceId, const std::string& name,
                          TrackType type, const std::string& targetEntityId = "",
                          const std::string& targetProperty = "");
    bool RemoveTrack(const std::string& trackId);
    bool SetTrackEnabled(const std::string& trackId, bool enabled);
    bool SetTrackLocked(const std::string& trackId, bool locked);
    bool SetTrackSolo(const std::string& trackId, bool solo);
    int GetTrackCount(const std::string& sequenceId) const;
    const Track* GetTrack(const std::string& trackId) const;

    // Keyframe management
    std::string AddKeyframe(const std::string& trackId, float time,
                             const std::string& value,
                             InterpolationType interp = InterpolationType::Linear);
    bool RemoveKeyframe(const std::string& trackId, const std::string& keyframeId);
    bool MoveKeyframe(const std::string& trackId, const std::string& keyframeId,
                       float newTime);
    bool SetKeyframeValue(const std::string& trackId, const std::string& keyframeId,
                           const std::string& value);
    bool SetKeyframeInterpolation(const std::string& trackId,
                                   const std::string& keyframeId,
                                   InterpolationType interp);
    int GetKeyframeCount(const std::string& trackId) const;

    // Playback
    void Play();
    void Pause();
    void Stop();
    void Scrub(float time);
    float GetCurrentTime() const { return m_currentTime; }
    PlaybackState GetPlaybackState() const { return m_playbackState; }

    // Persistence
    bool SaveSequences(const std::string& filePath) const;
    bool LoadSequences(const std::string& filePath);
    void ClearAll();

private:
    bool m_active{false};
    float m_currentTime{0.0f};
    PlaybackState m_playbackState{PlaybackState::Stopped};
    std::string m_activeSequenceId;
    std::unordered_map<std::string, Sequence> m_sequences;
    std::unordered_map<std::string, Track> m_tracks;
    int m_nextSequenceIndex{0};
    int m_nextTrackIndex{0};
    int m_nextKeyframeIndex{0};
};

} // namespace Atlas::Editor
