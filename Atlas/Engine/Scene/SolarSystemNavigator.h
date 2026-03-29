#pragma once
#include <string>
#include <vector>
#include <unordered_map>
#include <functional>

namespace Atlas::Engine {

/// Phase 40C — Navigator for inter-system pathfinding, route planning, and travel state management.
class SolarSystemNavigator {
public:
    enum class NavigationState { Idle, Planning, Traveling, Docking, Rerouting, Arrived, Error, Custom };
    enum class RouteType { Direct, Relay, Scenic, Efficient, Stealth, Emergency, Custom };
    enum class WaypointType { Origin, Transit, Destination, Hazard, Refuel, Beacon, Custom };
    enum class TravelMode { SubLight, FTL, Jump, Drift, Anchored, Custom };

    struct WaypointDef {
        std::string waypointId;
        std::string systemId;
        WaypointType waypointType{WaypointType::Transit};
        double posX{0.0};
        double posY{0.0};
        double posZ{0.0};
        double arrivalRadius{100.0};
        bool mandatory{false};
        std::string note;
    };

    struct RouteDef {
        std::string routeId;
        std::string routeName;
        RouteType routeType{RouteType::Direct};
        std::vector<std::string> waypointIds;
        double estimatedDistanceLY{0.0};
        double estimatedTravelTimeH{0.0};
        TravelMode travelMode{TravelMode::FTL};
        bool validated{false};
    };

    struct TravelRecord {
        std::string travelId;
        std::string routeId;
        NavigationState state{NavigationState::Idle};
        std::string vehicleId;
        int currentWaypointIndex{0};
        double progressPct{0.0};
        long long startTimestamp{0};
        long long lastUpdateTimestamp{0};
        bool completed{false};
    };

    // Waypoint management
    bool AddWaypoint(const WaypointDef& waypoint);
    bool RemoveWaypoint(const std::string& waypointId);
    bool SetWaypointType(const std::string& waypointId, WaypointType type);
    const WaypointDef* GetWaypoint(const std::string& waypointId) const;
    std::vector<std::string> GetAllWaypointIds() const;
    std::vector<std::string> GetWaypointsByType(WaypointType type) const;
    std::vector<std::string> GetWaypointsBySystem(const std::string& systemId) const;
    std::vector<std::string> GetMandatoryWaypoints() const;

    // Route management
    bool CreateRoute(const RouteDef& route);
    bool DeleteRoute(const std::string& routeId);
    bool ValidateRoute(const std::string& routeId);
    bool SetTravelMode(const std::string& routeId, TravelMode mode);
    const RouteDef* GetRoute(const std::string& routeId) const;
    std::vector<std::string> GetAllRouteIds() const;
    std::vector<std::string> GetRoutesByType(RouteType type) const;
    std::vector<std::string> GetValidatedRoutes() const;

    // Travel records
    bool BeginTravel(const TravelRecord& record);
    bool UpdateTravel(const std::string& travelId, double progressPct, NavigationState state);
    bool CompleteTravel(const std::string& travelId);
    bool AbortTravel(const std::string& travelId);
    const TravelRecord* GetTravelRecord(const std::string& travelId) const;
    std::vector<std::string> GetAllTravelIds() const;
    std::vector<std::string> GetActiveTravels() const;
    std::vector<std::string> GetCompletedTravels() const;
    std::vector<std::string> GetTravelsByRoute(const std::string& routeId) const;

    void Reset();

private:
    std::unordered_map<std::string, WaypointDef> m_waypoints;
    std::unordered_map<std::string, RouteDef> m_routes;
    std::unordered_map<std::string, TravelRecord> m_travelLog;
    NavigationState m_globalState{NavigationState::Idle};
};

} // namespace Atlas::Engine
