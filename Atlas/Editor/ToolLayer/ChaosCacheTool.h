#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P20 Tool — Chaos physics cache authoring, track configuration, and playback management.
class ChaosCacheTool : public ITool {
public:
    enum class CacheRecordState { Empty, Recording, Recorded, Playing, Paused, Error, Custom };
    enum class TrackType { Particle, Rigid, Cloth, Hair, Field, Constraint, Custom };
    enum class PlaybackMode { Loop, PingPong, Once, ClampForever, Custom };

    struct CacheTrackDef {
        std::string trackId;
        std::string name;
        TrackType trackType{TrackType::Rigid};
        float startTime{0.0f};
        float endTime{10.0f};
        int sampleRate{30};
        bool compressData{true};
        std::string sourceComponent;
    };

    struct CachePlaybackConfig {
        std::string configId;
        std::string cacheId;
        PlaybackMode playbackMode{PlaybackMode::Once};
        float startOffset{0.0f};
        float playRate{1.0f};
        bool loopEnabled{false};
        float blendInTime{0.1f};
    };

    struct CacheRecord {
        std::string recordId;
        std::string name;
        CacheRecordState state{CacheRecordState::Empty};
        std::vector<std::string> trackIds;
        float duration{0.0f};
        float diskSizeMB{0.0f};
        std::string outputPath;
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "ChaosCacheTool"; }
    bool IsActive() const override { return m_active; }

    std::string CreateCacheRecord(const std::string& name);
    bool DeleteCacheRecord(const std::string& recordId);
    bool StartRecording(const std::string& recordId);
    bool StopRecording(const std::string& recordId);
    CacheRecordState GetRecordState(const std::string& recordId) const;
    const CacheRecord* GetCacheRecord(const std::string& recordId) const;
    std::vector<std::string> GetAllRecordIds() const;

    std::string AddTrack(const std::string& recordId, const CacheTrackDef& track);
    bool RemoveTrack(const std::string& recordId, const std::string& trackId);
    bool SetTrackType(const std::string& trackId, TrackType type);
    bool SetSampleRate(const std::string& trackId, int sampleRate);
    const CacheTrackDef* GetTrack(const std::string& trackId) const;
    std::vector<std::string> GetTracksByType(TrackType type) const;

    bool SetPlaybackConfig(const std::string& recordId, const CachePlaybackConfig& config);
    bool PlayCache(const std::string& recordId);
    bool PausePlayback(const std::string& recordId);
    bool StopPlayback(const std::string& recordId);
    bool SetPlayRate(const std::string& recordId, float rate);

    bool ExportCache(const std::string& recordId, const std::string& outputPath) const;
    bool ValidateCache(const std::string& recordId) const;
    void Reset();

private:
    bool m_active{false};
    std::unordered_map<std::string, CacheRecord> m_records;
    std::unordered_map<std::string, CacheTrackDef> m_tracks;
    std::unordered_map<std::string, CachePlaybackConfig> m_playbackConfigs;
    int m_nextRecordIndex{0};
};

} // namespace Atlas::Editor
