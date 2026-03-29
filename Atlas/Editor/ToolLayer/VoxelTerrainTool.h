#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P8 Tool — Voxel-based terrain sculpting and generation tool.
class VoxelTerrainTool : public ITool {
public:
    enum class BrushMode { Raise, Lower, Flatten, Smooth, Paint, Carve };
    enum class VoxelMaterial { Rock, Soil, Sand, Snow, Lava, Ice };

    struct VoxelBrush {
        float radius{5.0f};
        float strength{1.0f};
        float falloff{0.5f};
        BrushMode mode{BrushMode::Raise};
    };

    struct ChunkCoord {
        int x{0};
        int y{0};
        int z{0};
    };

    struct TerrainChunk {
        std::string chunkId;
        ChunkCoord coord;
        int resolution{16};
        bool isDirty{false};
        VoxelMaterial dominantMaterial{VoxelMaterial::Rock};
        std::string generatorSeed;
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "VoxelTerrainTool"; }
    bool IsActive() const override { return m_active; }

    // Chunk management
    std::string CreateChunk(int cx, int cy, int cz, int resolution = 16);
    bool RemoveChunk(const std::string& chunkId);
    bool HasChunk(int cx, int cy, int cz) const;
    int GetChunkCount() const { return static_cast<int>(m_chunks.size()); }
    const TerrainChunk* GetChunk(const std::string& chunkId) const;
    std::vector<std::string> GetDirtyChunkIds() const;
    void MarkChunkClean(const std::string& chunkId);

    // Brush operations
    void SetBrush(const VoxelBrush& brush);
    const VoxelBrush& GetBrush() const { return m_brush; }
    bool SetBrushRadius(float radius);
    bool SetBrushStrength(float strength);
    bool SetBrushMode(BrushMode mode);

    // Sculpting
    bool SculptAt(float wx, float wy, float wz);
    bool FlattenRegion(float wx, float wy, float wz, float radius, float targetHeight);
    bool SmoothRegion(float wx, float wy, float wz, float radius, int iterations = 1);
    bool CarveBox(float minX, float minY, float minZ, float maxX, float maxY, float maxZ);

    // Material painting
    bool PaintMaterial(float wx, float wy, float wz, VoxelMaterial material);
    bool SetChunkMaterial(const std::string& chunkId, VoxelMaterial material);

    // Generation
    bool GenerateChunkNoise(const std::string& chunkId, const std::string& seed,
                             float noiseScale = 1.0f, float heightScale = 50.0f);
    int RegenerateAll(float noiseScale = 1.0f);

    // Serialization
    bool SaveChunk(const std::string& chunkId, const std::string& filePath) const;
    std::string LoadChunk(const std::string& filePath);
    void ClearAll();

private:
    bool m_active{false};
    std::unordered_map<std::string, TerrainChunk> m_chunks;
    VoxelBrush m_brush;
    int m_nextChunkIndex{0};
};

} // namespace Atlas::Editor
