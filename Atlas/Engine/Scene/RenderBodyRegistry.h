#pragma once
#include <string>
#include <vector>
#include <unordered_map>
#include <functional>

namespace Atlas::Engine {

/// Phase 30D — Registry for render body definitions used by the rendering subsystem.
class RenderBodyRegistry {
public:
    enum class RenderBodyState { Inactive, Active, Rendering, Culled, Occluded, LOD0, LOD1, LOD2 };
    enum class MeshPrimitive { Triangle, Line, Point, Patch, Billboard, InstancedMesh };
    enum class RenderLayer { Background, World, Characters, VFX, UI, Debug, Overlay };
    enum class ShadingModel { Lit, Unlit, Toon, Subsurface, ClearCoat, Custom };
    enum class CullMode { None, Front, Back, Both };

    struct MaterialSlot {
        int slotIndex{0};
        std::string materialPath;
        std::vector<std::string> paramOverrides;
    };

    struct LODEntry {
        int lodLevel{0};
        std::string meshPath;
        float screenSizeThreshold{1.0f};
    };

    struct BoundsInfo {
        float centerX{0.0f};
        float centerY{0.0f};
        float centerZ{0.0f};
        float extentX{1.0f};
        float extentY{1.0f};
        float extentZ{1.0f};
        float radius{1.0f};
    };

    struct RenderFlags {
        bool castShadow{true};
        bool receiveShadow{true};
        bool occluder{false};
        bool occludee{true};
        bool depthWrite{true};
        bool depthTest{true};
        bool receiveFog{true};
    };

    struct RenderBodyRecord {
        std::string bodyId;
        std::string name;
        std::string meshPath;
        MeshPrimitive primitive{MeshPrimitive::Triangle};
        RenderLayer renderLayer{RenderLayer::World};
        ShadingModel shadingModel{ShadingModel::Lit};
        CullMode cullMode{CullMode::Back};
        std::vector<MaterialSlot> materialSlots;
        std::vector<LODEntry> lodEntries;
        BoundsInfo bounds;
        RenderFlags flags;
        float posX{0.0f};
        float posY{0.0f};
        float posZ{0.0f};
        float rotX{0.0f};
        float rotY{0.0f};
        float rotZ{0.0f};
        float scaleX{1.0f};
        float scaleY{1.0f};
        float scaleZ{1.0f};
        bool visible{true};
        bool enabled{true};
        RenderBodyState state{RenderBodyState::Inactive};
    };

    // Body registration
    bool RegisterBody(const RenderBodyRecord& record);
    bool UnregisterBody(const std::string& bodyId);

    // State and transform
    bool SetBodyState(const std::string& bodyId, RenderBodyState state);
    bool SetBodyPosition(const std::string& bodyId, float x, float y, float z);
    bool SetBodyRotation(const std::string& bodyId, float x, float y, float z);
    bool SetBodyScale(const std::string& bodyId, float x, float y, float z);
    bool SetBodyVisible(const std::string& bodyId, bool visible);
    bool SetBodyEnabled(const std::string& bodyId, bool enabled);

    // Material and LOD
    bool AddMaterialSlot(const std::string& bodyId, const MaterialSlot& slot);
    bool RemoveMaterialSlot(const std::string& bodyId, int slotIndex);
    bool AddLODEntry(const std::string& bodyId, const LODEntry& entry);
    bool RemoveLODEntry(const std::string& bodyId, int lodLevel);

    // Render configuration
    bool SetRenderLayer(const std::string& bodyId, RenderLayer layer);
    bool SetShadingModel(const std::string& bodyId, ShadingModel model);
    bool SetCullMode(const std::string& bodyId, CullMode mode);
    bool SetRenderFlags(const std::string& bodyId, const RenderFlags& flags);
    bool SetBounds(const std::string& bodyId, const BoundsInfo& bounds);

    // Queries
    int GetBodyCount() const { return static_cast<int>(m_bodies.size()); }
    const RenderBodyRecord* GetBodyById(const std::string& bodyId) const;
    std::vector<std::string> GetAllBodyIds() const;
    std::vector<std::string> GetBodiesByLayer(RenderLayer layer) const;
    std::vector<std::string> GetBodiesByState(RenderBodyState state) const;
    std::vector<std::string> GetVisibleBodies() const;
    std::vector<std::string> GetBodiesInBounds(float centerX, float centerY, float centerZ,
                                                float radius) const;

    // Callbacks
    using StateChangedCallback = std::function<void(const std::string&, RenderBodyState)>;
    void SetOnStateChangedCallback(StateChangedCallback cb);

    // Persistence
    bool SaveRegistry(const std::string& filePath) const;
    bool LoadRegistry(const std::string& filePath);
    void Clear();

private:
    std::unordered_map<std::string, RenderBodyRecord> m_bodies;
    StateChangedCallback m_onStateChanged;
};

} // namespace Atlas::Engine
