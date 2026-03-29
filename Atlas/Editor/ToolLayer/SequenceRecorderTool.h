#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P14 Tool — Sequence recorder for capturing transform, animation, audio and event tracks
class SequenceRecorderTool : public ITool {
public:
    enum class RecordState { Idle, Recording, Paused, Stopped };
    enum class TrackType { Transform, Animation, Audio, Event, Custom };

    struct RecordTrack {
        std::string trackId;
        std::string name;
        TrackType type{TrackType::Transform};
        std::string targetEntityId;
        bool enabled{true};
        float sampleRate{30.0f};
    };

    struct RecordFrame {
        std::string frameId;
        std::string trackId;
        float timestamp{0.0f};
        std::vector<float> values;
        std::string eventData;
    };

    struct RecordSession {
        std::string sessionId;
        std::string name;
        RecordState state{RecordState::Idle};
        float startTime{0.0f};
        float endTime{0.0f};
        float duration{0.0f};
        std::vector<std::string> trackIds;
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "SequenceRecorderTool"; }
    bool IsActive() const override { return m_active; }

    std::string CreateSession(const std::string& name);
    bool RemoveSession(const std::string& sessionId);
    bool StartRecording(const std::string& sessionId);
    bool StopRecording(const std::string& sessionId);
    bool PauseRecording(const std::string& sessionId);
    bool ResumeRecording(const std::string& sessionId);
    RecordState GetRecordState(const std::string& sessionId) const;

    std::string AddTrack(const std::string& sessionId, const std::string& name, TrackType type);
    bool RemoveTrack(const std::string& sessionId, const std::string& trackId);
    bool SetTrackEnabled(const std::string& trackId, bool enabled);
    bool SetTrackSampleRate(const std::string& trackId, float sampleRate);
    bool SetTrackTarget(const std::string& trackId, const std::string& entityId);

    std::string RecordFrame(const std::string& trackId, float timestamp, const std::vector<float>& values);
    std::vector<std::string> GetRecordedFrames(const std::string& trackId) const;
    const RecordFrame* GetFrame(const std::string& frameId) const;
    int GetFrameCount(const std::string& trackId) const;

    int GetSessionCount() const;
    const RecordSession* GetSession(const std::string& sessionId) const;
    std::vector<std::string> GetSessionIds() const;
    std::vector<std::string> GetTrackIds(const std::string& sessionId) const;

    bool SaveSequence(const std::string& sessionId, const std::string& filePath) const;
    bool LoadSequence(const std::string& filePath);
    void ClearAll();

private:
    bool m_active{false};
    std::unordered_map<std::string, RecordSession> m_sessions;
    std::unordered_map<std::string, RecordTrack> m_tracks;
    std::unordered_map<std::string, RecordFrame> m_frames;
    int m_nextSessionIndex{0};
    int m_nextTrackIndex{0};
    int m_nextFrameIndex{0};
};

} // namespace Atlas::Editor
