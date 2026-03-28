// VoxelEditorMode.cpp
// Atlas Editor — voxel-editing mode controller.

#include "Voxel/VoxelEditorMode.h"

#include <cstring>

namespace atlas::editor::voxel {

bool VoxelEditorMode::Initialize() { return true; }
void VoxelEditorMode::Shutdown()   { m_chunks.clear(); }

VoxelChunkEditor& VoxelEditorMode::GetOrCreateChunk(const std::string& chunkId)
{
    auto it = m_chunks.find(chunkId);
    if (it == m_chunks.end())
    {
        auto [ins, ok] = m_chunks.emplace(chunkId,
            std::make_unique<VoxelChunkEditor>(chunkId));
        return *ins->second;
    }
    return *it->second;
}

bool VoxelEditorMode::ChunkExists(const std::string& chunkId) const
{
    return m_chunks.count(chunkId) > 0;
}

void VoxelEditorMode::UnloadChunk(const std::string& chunkId)
{
    m_chunks.erase(chunkId);
}

ChunkEditResult VoxelEditorMode::Stroke(const std::string& chunkId,
                                         VoxelPos pos)
{
    return GetOrCreateChunk(chunkId).ApplyBrush(pos, m_brush);
}

std::vector<std::string> VoxelEditorMode::GetDirtyChunkIds() const
{
    std::vector<std::string> result;
    for (const auto& [id, chunk] : m_chunks)
        if (chunk->IsDirty()) result.push_back(id);
    return result;
}

void VoxelEditorMode::RebuildDirtyMeshes()
{
    for (auto& [id, chunk] : m_chunks)
        if (chunk->IsDirty()) chunk->TriggerMeshRebuild();
}

std::vector<uint8_t> VoxelEditorMode::SerialiseAll() const
{
    // Simple format: [n_chunks:4][for each chunk: idLen:2 + id + blob:kTotal*2]
    std::vector<uint8_t> out;
    auto write32 = [&](uint32_t v) {
        for (int i = 0; i < 4; ++i) out.push_back(static_cast<uint8_t>(v >> (i * 8)));
    };
    auto write16 = [&](uint16_t v) {
        out.push_back(static_cast<uint8_t>(v & 0xFF));
        out.push_back(static_cast<uint8_t>(v >> 8));
    };

    write32(static_cast<uint32_t>(m_chunks.size()));
    for (const auto& [id, chunk] : m_chunks)
    {
        write16(static_cast<uint16_t>(id.size()));
        for (char c : id) out.push_back(static_cast<uint8_t>(c));
        auto blob = chunk->Serialise();
        out.insert(out.end(), blob.begin(), blob.end());
    }
    return out;
}

bool VoxelEditorMode::DeserialiseAll(const std::vector<uint8_t>& data)
{
    if (data.size() < 4) return false;
    size_t pos = 0;
    auto read32 = [&]() -> uint32_t {
        uint32_t v = 0;
        for (int i = 0; i < 4; ++i) v |= static_cast<uint32_t>(data[pos++]) << (i * 8);
        return v;
    };
    auto read16 = [&]() -> uint16_t {
        uint16_t v = static_cast<uint16_t>(data[pos]) |
                     static_cast<uint16_t>(data[pos + 1] << 8);
        pos += 2;
        return v;
    };

    uint32_t count = read32();
    m_chunks.clear();
    constexpr size_t kBlobSize = static_cast<size_t>(kChunkSize) *
                                  kChunkSize * kChunkSize * kBytesPerCell;
    for (uint32_t i = 0; i < count; ++i)
    {
        if (pos + 2 > data.size()) return false;
        uint16_t idLen = read16();
        if (pos + idLen + kBlobSize > data.size()) return false;
        std::string id(data.begin() + static_cast<ptrdiff_t>(pos),
                       data.begin() + static_cast<ptrdiff_t>(pos + idLen));
        pos += idLen;
        std::vector<uint8_t> blob(data.begin() + static_cast<ptrdiff_t>(pos),
                                   data.begin() + static_cast<ptrdiff_t>(pos + kBlobSize));
        pos += kBlobSize;

        auto& editor = GetOrCreateChunk(id);
        editor.Deserialise(blob);
    }
    return true;
}

} // namespace atlas::editor::voxel
