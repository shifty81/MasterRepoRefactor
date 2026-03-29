#pragma once
#include <string>
#include <vector>
#include <unordered_map>
#include <functional>

namespace Atlas::Engine {

/// Phase 22D — Registry for streaming world regions.  Each region is a
/// named bounding box that can be streamed in/out independently based on
/// player position or explicit requests.
class StreamingRegionRegistry {
public:
    enum class RegionState { Unloaded, Loading, Loaded, Unloading, Failed };

    struct AABB {
        float minX{0.0f};
        float minY{0.0f};
        float minZ{0.0f};
        float maxX{100.0f};
        float maxY{100.0f};
        float maxZ{100.0f};
    };

    struct RegionRecord {
        std::string regionId;
        std::string name;
        AABB bounds;
        RegionState state{RegionState::Unloaded};
        std::vector<std::string> bundleIds;
        bool alwaysLoaded{false};
        int priority{0};
    };

    // Registration
    bool RegisterRegion(const std::string& regionId,
                        const std::string& name,
                        const AABB& bounds,
                        bool alwaysLoaded = false,
                        int priority = 0);
    bool UnregisterRegion(const std::string& regionId);
    bool IsRegistered(const std::string& regionId) const;
    int GetRegionCount() const { return static_cast<int>(m_regions.size()); }

    // Bundle wiring
    bool AddBundle(const std::string& regionId, const std::string& bundleId);
    std::vector<std::string> GetBundles(const std::string& regionId) const;

    // Load / unload
    bool LoadRegion(const std::string& regionId);
    bool UnloadRegion(const std::string& regionId);
    bool IsLoaded(const std::string& regionId) const;
    int GetLoadedCount() const;
    std::vector<std::string> GetLoadedRegionIds() const;

    // Spatial query
    std::vector<std::string> QueryPoint(float px, float py, float pz) const;
    std::vector<std::string> QueryAABB(const AABB& aabb) const;
    std::vector<std::string> GetAlwaysLoadedRegions() const;
    std::vector<std::string> GetRegionsByPriority(int minPriority) const;

    // Lookup
    const RegionRecord* GetRegion(const std::string& regionId) const;
    std::vector<std::string> GetAllRegionIds() const;

    // Traversal
    void ForEach(const std::function<void(const RegionRecord&)>& fn) const;

    // Lifecycle
    void Clear();

    // Callbacks
    void SetOnRegionLoadedCallback(
        std::function<void(const std::string&)> cb);
    void SetOnRegionUnloadedCallback(
        std::function<void(const std::string&)> cb);

private:
    static bool _aabbContainsPoint(const AABB& b,
                                    float px, float py, float pz);
    static bool _aabbIntersects(const AABB& a, const AABB& b);

    std::unordered_map<std::string, RegionRecord> m_regions;
    std::function<void(const std::string&)> m_onLoaded;
    std::function<void(const std::string&)> m_onUnloaded;
};

} // namespace Atlas::Engine
