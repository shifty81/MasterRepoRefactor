#pragma once
#include <string>
#include <vector>
#include <unordered_map>
#include <functional>

namespace Atlas::Engine {

/// Phase 25D — Registry for navigation mesh assets with runtime load/query API.
/// Manages the lifecycle of NavMesh data used by the AI pathfinding subsystem,
/// supporting spatial partitioning, neighbour connectivity, and path queries.
class NavMeshRegistry {
public:
    enum class NavMeshState { Unloaded, Loading, Loaded, Unloading, Failed };
    enum class NavMeshType { Ground, Water, Air, Ceiling, Ledge, Custom };
    enum class AgentType { Biped, Quadruped, Flying, Swimming, Small, Large };

    struct NavMeshAABB {
        float minX{0.0f};
        float minY{0.0f};
        float minZ{0.0f};
        float maxX{100.0f};
        float maxY{100.0f};
        float maxZ{100.0f};
    };

    struct NavMeshLink {
        std::string linkId;
        std::string fromMeshId;
        std::string toMeshId;
        float entryX{0.0f};
        float entryY{0.0f};
        float entryZ{0.0f};
        float exitX{0.0f};
        float exitY{0.0f};
        float exitZ{0.0f};
        float traversalCost{1.0f};
        bool bidirectional{true};
        bool enabled{true};
    };

    struct AgentCapability {
        AgentType agentType{AgentType::Biped};
        float agentRadius{0.4f};
        float agentHeight{1.8f};
        float maxClimbHeight{0.4f};
        float maxSlopeAngle{45.0f};
        bool enabled{true};
    };

    struct NavMeshRecord {
        std::string meshId;
        std::string name;
        NavMeshType type{NavMeshType::Ground};
        NavMeshState state{NavMeshState::Unloaded};
        NavMeshAABB bounds;
        std::vector<std::string> linkIds;
        std::vector<std::string> neighbourMeshIds;
        std::vector<AgentCapability> agentCapabilities;
        std::string assetPath;
        std::string parentMeshId;
        int priority{0};
        bool alwaysLoaded{false};
        int nodeCount{0};
        int edgeCount{0};
    };

    // Registration
    bool RegisterNavMesh(const std::string& meshId,
                          const std::string& name,
                          NavMeshType type,
                          const NavMeshAABB& bounds,
                          bool alwaysLoaded = false,
                          int priority = 0);
    bool UnregisterNavMesh(const std::string& meshId);
    bool UpdateNavMeshBounds(const std::string& meshId, const NavMeshAABB& bounds);
    bool SetNavMeshAssetPath(const std::string& meshId, const std::string& path);
    bool SetNavMeshPriority(const std::string& meshId, int priority);
    bool SetAlwaysLoaded(const std::string& meshId, bool alwaysLoaded);
    int GetRegisteredCount() const { return static_cast<int>(m_meshes.size()); }
    bool IsRegistered(const std::string& meshId) const;
    const NavMeshRecord* GetNavMesh(const std::string& meshId) const;
    std::vector<std::string> GetAllNavMeshIds() const;

    // Load / unload
    bool LoadNavMesh(const std::string& meshId);
    bool UnloadNavMesh(const std::string& meshId);
    bool IsLoaded(const std::string& meshId) const;
    int GetLoadedCount() const;
    std::vector<std::string> GetLoadedIds() const;
    std::vector<std::string> GetAlwaysLoadedIds() const;

    // Links
    std::string AddLink(const std::string& fromMeshId, const std::string& toMeshId,
                         float ex, float ey, float ez,
                         float exitX, float exitY, float exitZ,
                         float cost = 1.0f, bool bidirectional = true);
    bool RemoveLink(const std::string& linkId);
    bool SetLinkEnabled(const std::string& linkId, bool enabled);
    bool SetLinkCost(const std::string& linkId, float cost);
    int GetLinkCount() const { return static_cast<int>(m_links.size()); }
    const NavMeshLink* GetLink(const std::string& linkId) const;
    std::vector<std::string> GetLinksForMesh(const std::string& meshId) const;

    // Neighbours
    bool AddNeighbour(const std::string& meshId, const std::string& neighbourId);
    bool RemoveNeighbour(const std::string& meshId, const std::string& neighbourId);
    std::vector<std::string> GetNeighbours(const std::string& meshId) const;

    // Agent capabilities
    bool AddAgentCapability(const std::string& meshId, AgentType agentType,
                              float radius, float height,
                              float maxClimb = 0.4f, float maxSlope = 45.0f);
    bool RemoveAgentCapability(const std::string& meshId, AgentType agentType);
    bool SupportsAgent(const std::string& meshId, AgentType agentType) const;
    int GetAgentCapabilityCount(const std::string& meshId) const;

    // Spatial queries
    std::vector<std::string> QueryPoint(float px, float py, float pz) const;
    std::vector<std::string> QueryAABB(float minX, float minY, float minZ,
                                         float maxX, float maxY, float maxZ) const;
    std::string FindNearestMesh(float px, float py, float pz,
                                  AgentType agentType = AgentType::Biped) const;
    std::vector<std::string> QueryPath(const std::string& startMeshId,
                                        const std::string& endMeshId) const;

    // State
    NavMeshState GetState(const std::string& meshId) const;
    bool SetState(const std::string& meshId, NavMeshState state);

    // Callbacks
    using StateChangedCallback = std::function<void(const std::string&, NavMeshState)>;
    void SetOnStateChangedCallback(StateChangedCallback cb);

    // Persistence
    bool SaveRegistry(const std::string& filePath) const;
    bool LoadRegistry(const std::string& filePath);
    void Clear();

private:
    std::unordered_map<std::string, NavMeshRecord> m_meshes;
    std::unordered_map<std::string, NavMeshLink> m_links;
    StateChangedCallback m_onStateChanged;
    int m_nextLinkIndex{0};
};

} // namespace Atlas::Engine
