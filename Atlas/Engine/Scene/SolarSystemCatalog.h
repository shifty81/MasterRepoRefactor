#pragma once
#include <string>
#include <vector>
#include <unordered_map>
#include <functional>

namespace Atlas::Engine {

/// Phase 27C — Solar system catalog for multi-system discovery, indexing, and search.
/// Maintains a searchable index of all known solar systems and their key attributes
/// to support fast traversal, discovery chains, and faction territory mapping.
class SolarSystemCatalog {
public:
    enum class StarClass { O, B, A, F, G, K, M, L, T, Neutron, BlackHole, WhiteDwarf };
    enum class SystemStatus { Unknown, Surveyed, Colonised, Contested, Abandoned };
    enum class SystemHazard { Safe, Low, Medium, High, Extreme, Lethal };
    enum class FactionAlignment { Neutral, Friendly, Hostile, Restricted, Lawless };

    struct SystemCoordinates {
        float x{0.0f};
        float y{0.0f};
        float z{0.0f};
        float lightYearsFromOrigin{0.0f};
    };

    struct TradeRoute {
        std::string routeId;
        std::string sourceSystemId;
        std::string destinationSystemId;
        float distanceLY{0.0f};
        float safetyRating{1.0f};
        bool hasStargate{false};
        std::string controllingFaction;
    };

    struct SystemCatalogEntry {
        std::string systemId;
        std::string name;
        StarClass starClass{StarClass::G};
        std::string starTypeCode;
        float starLuminosity{1.0f};
        float starRadius{1.0f};
        SystemStatus status{SystemStatus::Unknown};
        SystemHazard hazard{SystemHazard::Medium};
        FactionAlignment alignment{FactionAlignment::Neutral};
        SystemCoordinates coordinates;
        int celestialCount{0};
        int planetCount{0};
        int stationCount{0};
        int stargateCount{0};
        std::vector<std::string> factions;
        std::vector<std::string> oreTypes;
        std::vector<std::string> connectedSystemIds;
        float securityRating{0.5f};
        bool hasPCGConfig{false};
        std::string jsonFilePath;
        bool enabled{true};
    };

    // Entry management
    bool RegisterSystem(const SystemCatalogEntry& entry);
    bool UnregisterSystem(const std::string& systemId);
    bool UpdateSystem(const std::string& systemId, const SystemCatalogEntry& entry);
    bool SetSystemStatus(const std::string& systemId, SystemStatus status);
    bool SetSystemHazard(const std::string& systemId, SystemHazard hazard);
    bool SetFactionAlignment(const std::string& systemId, FactionAlignment alignment);
    bool SetSecurityRating(const std::string& systemId, float rating);
    bool AddConnection(const std::string& systemId,
                        const std::string& connectedId);
    bool RemoveConnection(const std::string& systemId,
                           const std::string& connectedId);
    bool SetEnabled(const std::string& systemId, bool enabled);
    int GetRegisteredCount() const { return static_cast<int>(m_entries.size()); }
    bool IsRegistered(const std::string& systemId) const;
    const SystemCatalogEntry* GetEntry(const std::string& systemId) const;
    std::vector<std::string> GetAllSystemIds() const;

    // Query / search
    std::vector<std::string> FindByStarClass(StarClass starClass) const;
    std::vector<std::string> FindByStatus(SystemStatus status) const;
    std::vector<std::string> FindByHazard(SystemHazard hazard) const;
    std::vector<std::string> FindByFactionAlignment(FactionAlignment alignment) const;
    std::vector<std::string> FindByFaction(const std::string& faction) const;
    std::vector<std::string> FindByOreType(const std::string& oreType) const;
    std::vector<std::string> FindConnectedTo(const std::string& systemId) const;
    std::vector<std::string> FindBySecurityRange(float minSec, float maxSec) const;
    std::vector<std::string> FindByRadius(float centerX, float centerY,
                                           float centerZ, float radiusLY) const;
    std::vector<std::string> FindWithStargates() const;
    std::vector<std::string> FindWithStations() const;
    int GetEnabledCount() const;

    // Distance
    float GetDistanceLY(const std::string& systemAId,
                         const std::string& systemBId) const;

    // Trade routes
    bool RegisterTradeRoute(const TradeRoute& route);
    bool UnregisterTradeRoute(const std::string& routeId);
    std::vector<TradeRoute> GetRoutesFromSystem(const std::string& systemId) const;
    std::vector<TradeRoute> GetRoutesToSystem(const std::string& systemId) const;
    int GetTradeRouteCount() const { return static_cast<int>(m_routes.size()); }
    const TradeRoute* GetTradeRoute(const std::string& routeId) const;

    // Path finding
    std::vector<std::string> FindShortestPath(const std::string& sourceId,
                                                const std::string& destinationId) const;
    std::vector<std::string> FindSafestPath(const std::string& sourceId,
                                              const std::string& destinationId,
                                              float minSecurity = 0.3f) const;
    int GetHopCount(const std::string& sourceId,
                     const std::string& destinationId) const;

    // Statistics
    int CountByStarClass(StarClass starClass) const;
    int CountByStatus(SystemStatus status) const;
    float GetAverageSecurityRating() const;

    // Callbacks
    using SystemChangedCallback = std::function<void(const std::string&, SystemStatus)>;
    void SetOnSystemChangedCallback(SystemChangedCallback cb);

    // Persistence
    bool SaveCatalog(const std::string& filePath) const;
    bool LoadCatalog(const std::string& filePath);
    void Clear();

private:
    std::unordered_map<std::string, SystemCatalogEntry> m_entries;
    std::unordered_map<std::string, TradeRoute> m_routes;
    SystemChangedCallback m_onSystemChanged;
};

} // namespace Atlas::Engine
