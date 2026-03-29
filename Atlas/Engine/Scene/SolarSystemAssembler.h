#pragma once
#include <string>
#include <vector>
#include <unordered_map>
#include <functional>

namespace Atlas::Engine {

/// Phase 42C — Assembler for compositing solar system scenes, managing LOD stages, and streaming manifests.
class SolarSystemAssembler {
public:
    enum class AssemblyState { Pending, Building, Complete, Failed, Stale, Custom };
    enum class LODStage { Full, Detail, Medium, Far, Impostor, Culled, Custom };
    enum class StreamingPriority { Critical, High, Normal, Low, Background, Custom };
    enum class AssemblyPass { Geometry, Lighting, Effects, Audio, Culling, Custom };

    struct AssemblyManifestDef {
        std::string manifestId;
        std::string systemId;
        AssemblyState state{AssemblyState::Pending};
        std::string version;
        int celestialCount{0};
        bool includeEffects{true};
        bool includeAudio{true};
        bool validateOnBuild{true};
        long long buildTimestampMs{0};
    };

    struct LODStageDef {
        std::string lodStageId;
        std::string manifestId;
        std::string assetId;
        LODStage stage{LODStage::Full};
        float minDistanceLY{0.0f};
        float maxDistanceLY{100.0f};
        float screenSizeThreshold{1.0f};
        std::string lodMeshId;
        bool enabled{true};
    };

    struct StreamingChunkDef {
        std::string chunkId;
        std::string manifestId;
        StreamingPriority priority{StreamingPriority::Normal};
        std::string assetId;
        float loadRadiusLY{50.0f};
        float unloadRadiusLY{100.0f};
        AssemblyPass pass{AssemblyPass::Geometry};
        bool loaded{false};
        bool pinned{false};
    };

    // Manifest management
    bool CreateManifest(const AssemblyManifestDef& manifest);
    bool DeleteManifest(const std::string& manifestId);
    bool BuildManifest(const std::string& manifestId);
    bool InvalidateManifest(const std::string& manifestId);
    bool SetManifestState(const std::string& manifestId, AssemblyState state);
    const AssemblyManifestDef* GetManifest(const std::string& manifestId) const;
    std::vector<std::string> GetAllManifestIds() const;
    std::vector<std::string> GetManifestsByState(AssemblyState state) const;
    std::vector<std::string> GetManifestsBySystem(const std::string& systemId) const;
    std::vector<std::string> GetCompleteManifests() const;
    std::vector<std::string> GetStaleManifests() const;

    // LOD stage management
    bool AddLODStage(const std::string& manifestId, const LODStageDef& stage);
    bool RemoveLODStage(const std::string& manifestId, const std::string& lodStageId);
    bool EnableLODStage(const std::string& lodStageId, bool enabled);
    const LODStageDef* GetLODStage(const std::string& lodStageId) const;
    std::vector<std::string> GetLODStagesByManifest(const std::string& manifestId) const;
    std::vector<std::string> GetLODStagesByLevel(LODStage stage) const;
    std::vector<std::string> GetEnabledLODStages(const std::string& manifestId) const;

    // Streaming chunks
    bool AddChunk(const std::string& manifestId, const StreamingChunkDef& chunk);
    bool RemoveChunk(const std::string& manifestId, const std::string& chunkId);
    bool LoadChunk(const std::string& chunkId);
    bool UnloadChunk(const std::string& chunkId);
    bool PinChunk(const std::string& chunkId, bool pinned);
    const StreamingChunkDef* GetChunk(const std::string& chunkId) const;
    std::vector<std::string> GetChunksByManifest(const std::string& manifestId) const;
    std::vector<std::string> GetChunksByPriority(StreamingPriority priority) const;
    std::vector<std::string> GetLoadedChunks() const;
    std::vector<std::string> GetPinnedChunks() const;

    void Reset();

private:
    std::unordered_map<std::string, AssemblyManifestDef> m_manifests;
    std::unordered_map<std::string, LODStageDef> m_lodStages;
    std::unordered_map<std::string, StreamingChunkDef> m_chunks;
    AssemblyState m_globalState{AssemblyState::Pending};
};

} // namespace Atlas::Engine
