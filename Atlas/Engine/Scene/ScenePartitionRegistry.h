#pragma once
#include <string>
#include <vector>
#include <unordered_map>
#include <functional>

namespace Atlas::Engine {

/// Phase 24D — Registry for spatial scene partitions (sectors/cells/portals).
/// Used by the streaming system to subdivide large scenes into independently
/// loadable spatial units with portal connectivity and priority-based loading.
class ScenePartitionRegistry {
public:
    enum class PartitionState { Unloaded, Loading, Loaded, Unloading, Failed };
    enum class PartitionType { Sector, Cell, Room, Portal, ExteriorZone, InteriorZone };

    struct PortalLink {
        std::string fromPartitionId;
        std::string toPartitionId;
        float portalWidth{3.0f};
        float portalHeight{3.0f};
        float posX{0.0f};
        float posY{0.0f};
        float posZ{0.0f};
        bool bidirectional{true};
        bool cullingEnabled{true};
    };

    struct AABB {
        float minX{0.0f};
        float minY{0.0f};
        float minZ{0.0f};
        float maxX{100.0f};
        float maxY{100.0f};
        float maxZ{100.0f};
    };

    struct PartitionRecord {
        std::string partitionId;
        std::string name;
        PartitionType type{PartitionType::Sector};
        AABB bounds;
        PartitionState state{PartitionState::Unloaded};
        std::vector<std::string> bundleIds;
        std::vector<std::string> portalIds;
        std::vector<std::string> neighbourIds;
        bool alwaysLoaded{false};
        int priority{0};
        std::string parentPartitionId;
        std::string sceneAssetPath;
    };

    // Registration
    bool RegisterPartition(const std::string& partitionId,
                            const std::string& name,
                            PartitionType type,
                            const AABB& bounds,
                            bool alwaysLoaded = false,
                            int priority = 0);
    bool UnregisterPartition(const std::string& partitionId);
    bool IsRegistered(const std::string& partitionId) const;
    int GetPartitionCount() const { return static_cast<int>(m_partitions.size()); }

    // State management
    bool LoadPartition(const std::string& partitionId);
    bool UnloadPartition(const std::string& partitionId);
    bool IsLoaded(const std::string& partitionId) const;
    int GetLoadedCount() const;
    std::vector<std::string> GetLoadedPartitionIds() const;

    // Portal management
    std::string RegisterPortal(const std::string& fromId, const std::string& toId,
                                float px, float py, float pz,
                                bool bidirectional = true);
    bool UnregisterPortal(const std::string& portalId);
    int GetPortalCount() const { return static_cast<int>(m_portals.size()); }
    const PortalLink* GetPortal(const std::string& portalId) const;
    std::vector<std::string> GetPortalsForPartition(const std::string& partitionId) const;
    std::vector<std::string> GetNeighbours(const std::string& partitionId) const;

    // Bundle wiring
    bool AddBundle(const std::string& partitionId, const std::string& bundleId);
    std::vector<std::string> GetBundles(const std::string& partitionId) const;

    // Spatial query
    std::vector<std::string> QueryPoint(float px, float py, float pz) const;
    std::vector<std::string> QueryAABB(const AABB& aabb) const;
    std::vector<std::string> GetAlwaysLoadedPartitions() const;
    std::vector<std::string> GetPartitionsByType(PartitionType type) const;
    std::vector<std::string> GetPartitionsByPriority(int minPriority) const;

    // Hierarchy
    bool SetParent(const std::string& partitionId, const std::string& parentId);
    std::vector<std::string> GetChildren(const std::string& parentId) const;

    // Lookup
    const PartitionRecord* GetPartition(const std::string& partitionId) const;
    std::vector<std::string> GetAllPartitionIds() const;

    // Traversal
    void ForEach(const std::function<void(const PartitionRecord&)>& fn) const;

    // Callbacks
    void SetOnPartitionLoadedCallback(std::function<void(const std::string&)> cb);
    void SetOnPartitionUnloadedCallback(std::function<void(const std::string&)> cb);

    // Lifecycle
    void Clear();

private:
    static bool _aabbContainsPoint(const AABB& b, float px, float py, float pz);
    static bool _aabbIntersects(const AABB& a, const AABB& b);

    std::unordered_map<std::string, PartitionRecord> m_partitions;
    std::unordered_map<std::string, PortalLink> m_portals;
    std::function<void(const std::string&)> m_onLoaded;
    std::function<void(const std::string&)> m_onUnloaded;
    int m_nextPortalIndex{0};
};

} // namespace Atlas::Engine
