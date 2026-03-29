#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P18 Tool — Zone graph authoring, lane configuration, and traffic/navigation zone management.
class ZoneGraphTool : public ITool {
public:
    enum class ZoneLaneType { Pedestrian, Vehicle, Bicycle, Emergency, Restricted, Custom };
    enum class ZoneShape { Polygon, Spline, Box, Circle, Capsule };
    enum class ZoneTagType { Navigation, Traffic, AI, Streaming, Gameplay, Exclusion };

    struct ZoneLaneDef {
        std::string laneId;
        std::string name;
        ZoneLaneType laneType{ZoneLaneType::Pedestrian};
        float width{3.0f};
        int directionality{1};
        float speedLimit{50.0f};
        std::vector<std::string> tags;
    };

    struct ZoneDef {
        std::string zoneId;
        std::string name;
        ZoneShape shape{ZoneShape::Polygon};
        std::vector<std::vector<float>> vertices;
        float height{300.0f};
        std::vector<std::string> lanes;
        std::vector<std::string> zoneTags;
        bool enabled{true};
    };

    struct ZoneConnection {
        std::string connectionId;
        std::string zoneAId;
        std::string zoneBId;
        std::string laneAId;
        std::string laneBId;
        bool bidirectional{true};
        float weight{1.0f};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "ZoneGraphTool"; }
    bool IsActive() const override { return m_active; }

    std::string CreateZone(const std::string& name, ZoneShape shape);
    bool RemoveZone(const std::string& zoneId);
    std::string AddLane(const std::string& zoneId, const std::string& name, ZoneLaneType type);
    bool RemoveLane(const std::string& zoneId, const std::string& laneId);
    std::string CreateConnection(const std::string& zoneAId, const std::string& zoneBId);
    bool RemoveConnection(const std::string& connectionId);
    bool SetZoneShape(const std::string& zoneId, ZoneShape shape);
    bool SetLaneType(const std::string& laneId, ZoneLaneType type);
    bool SetLaneWidth(const std::string& laneId, float width);
    bool SetSpeedLimit(const std::string& laneId, float speedLimit);
    bool AddZoneTag(const std::string& zoneId, ZoneTagType tag);
    bool RemoveZoneTag(const std::string& zoneId, ZoneTagType tag);
    bool EnableZone(const std::string& zoneId);
    bool DisableZone(const std::string& zoneId);
    bool FindPath(const std::string& fromZoneId, const std::string& toZoneId, std::vector<std::string>& outPath) const;
    const ZoneDef* GetZone(const std::string& zoneId) const;
    const ZoneLaneDef* GetLane(const std::string& laneId) const;
    const ZoneConnection* GetConnection(const std::string& connectionId) const;
    std::vector<std::string> GetAllZoneIds() const;
    std::vector<std::string> GetLanesByZone(const std::string& zoneId) const;
    std::vector<std::string> GetConnectionsByZone(const std::string& zoneId) const;
    std::vector<std::string> GetZonesByTag(ZoneTagType tag) const;
    bool ValidateZoneGraph() const;
    bool ExportZoneGraph(const std::string& filePath) const;
    bool SaveZoneGraph(const std::string& filePath) const;
    bool LoadZoneGraph(const std::string& filePath);
    void ClearAll();

private:
    bool m_active{false};
    std::unordered_map<std::string, ZoneDef> m_zones;
    std::unordered_map<std::string, ZoneLaneDef> m_lanes;
    std::unordered_map<std::string, ZoneConnection> m_connections;
    int m_nextZoneIndex{0};
    int m_nextLaneIndex{0};
    int m_nextConnectionIndex{0};
};

} // namespace Atlas::Editor
