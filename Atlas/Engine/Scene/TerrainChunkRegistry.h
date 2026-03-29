#pragma once
#include <string>
#include <vector>
#include <unordered_map>
#include <functional>

namespace Atlas::Engine {

/// Phase 23D — Registry for terrain chunks in a voxel/heightmap world.
/// Each chunk is identified by a grid coordinate and carries LOD, material,
/// and bundle metadata required for streaming and PCG integration.
class TerrainChunkRegistry {
public:
    enum class ChunkState { Unloaded, Loading, Loaded, Unloading, Failed };
    enum class LODLevel { LOD0, LOD1, LOD2, LOD3 };

    struct ChunkCoord {
        int x{0};
        int z{0};
        bool operator==(const ChunkCoord& o) const {
            return x == o.x && z == o.z;
        }
    };

    struct ChunkRecord {
        std::string chunkId;
        ChunkCoord coord;
        ChunkState state{ChunkState::Unloaded};
        LODLevel activeLOD{LODLevel::LOD0};
        int resolution{16};
        std::vector<std::string> bundleIds;
        std::string materialId;
        std::string generatorSeed;
        bool isModified{false};
        bool alwaysLoaded{false};
        int priority{0};
        float worldX{0.0f};
        float worldZ{0.0f};
        float chunkSize{100.0f};
    };

    // Registration
    bool RegisterChunk(const std::string& chunkId,
                       const ChunkCoord& coord,
                       int resolution = 16,
                       float chunkSize = 100.0f);
    bool UnregisterChunk(const std::string& chunkId);
    bool IsRegistered(const std::string& chunkId) const;
    int GetChunkCount() const { return static_cast<int>(m_chunks.size()); }

    // State management
    bool LoadChunk(const std::string& chunkId);
    bool UnloadChunk(const std::string& chunkId);
    bool IsLoaded(const std::string& chunkId) const;
    int GetLoadedCount() const;
    std::vector<std::string> GetLoadedChunkIds() const;

    // Coordinate-based access
    std::string FindChunkAtCoord(int cx, int cz) const;
    std::vector<std::string> GetChunksInRange(int cx, int cz, int radius) const;

    // Bundle wiring
    bool AddBundle(const std::string& chunkId, const std::string& bundleId);
    std::vector<std::string> GetBundles(const std::string& chunkId) const;

    // LOD management
    bool SetActiveLOD(const std::string& chunkId, LODLevel lod);
    LODLevel GetActiveLOD(const std::string& chunkId) const;
    int GetChunkCountByLOD(LODLevel lod) const;

    // Metadata
    bool SetMaterial(const std::string& chunkId, const std::string& materialId);
    bool SetGeneratorSeed(const std::string& chunkId, const std::string& seed);
    bool MarkModified(const std::string& chunkId, bool modified = true);
    bool SetAlwaysLoaded(const std::string& chunkId, bool alwaysLoaded);
    bool SetPriority(const std::string& chunkId, int priority);
    std::vector<std::string> GetModifiedChunkIds() const;
    std::vector<std::string> GetAlwaysLoadedChunkIds() const;
    std::vector<std::string> GetChunksByPriority(int minPriority) const;

    // Lookup
    const ChunkRecord* GetChunk(const std::string& chunkId) const;
    std::vector<std::string> GetAllChunkIds() const;

    // Traversal
    void ForEach(const std::function<void(const ChunkRecord&)>& fn) const;

    // Callbacks
    void SetOnChunkLoadedCallback(std::function<void(const std::string&)> cb);
    void SetOnChunkUnloadedCallback(std::function<void(const std::string&)> cb);

    // Lifecycle
    void Clear();

private:
    std::unordered_map<std::string, ChunkRecord> m_chunks;
    std::function<void(const std::string&)> m_onLoaded;
    std::function<void(const std::string&)> m_onUnloaded;
};

} // namespace Atlas::Engine
