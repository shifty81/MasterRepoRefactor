#pragma once
#include <string>
#include <vector>
#include <unordered_map>
#include <functional>

namespace Atlas::Engine {

/// Phase 35C — Router for solar system message passing and inter-system communication.
class SolarSystemRouter {
public:
    enum class RouteState { Idle, Active, Queued, Blocked, Expired, Error, Custom };
    enum class RouteProtocol { Direct, Relay, Broadcast, Multicast, Anycast, Custom };
    enum class MessageType { Command, Query, Event, Acknowledgment, Heartbeat, Error, Custom };

    struct RouteDef {
        std::string routeId;
        std::string name;
        RouteProtocol protocol{RouteProtocol::Direct};
        std::string sourceSystem;
        std::string targetSystem;
        std::vector<MessageType> allowedTypes;
        int priority{0};
        long long ttlMs{30000};
    };

    struct RouteMessage {
        std::string messageId;
        std::string routeId;
        MessageType messageType{MessageType::Command};
        std::string payload;
        std::string senderId;
        std::vector<std::string> recipientIds;
        long long timestamp{0};
        int retryCount{0};
    };

    struct RouteLog {
        std::string logId;
        std::string routeId;
        std::string messageId;
        bool success{false};
        double elapsedMs{0.0};
        std::string errorMessage;
    };

    // Route management
    bool RegisterRoute(const RouteDef& route);
    bool UnregisterRoute(const std::string& routeId);
    bool SetRouteProtocol(const std::string& routeId, RouteProtocol protocol);
    bool SetRoutePriority(const std::string& routeId, int priority);
    bool SetTTL(const std::string& routeId, long long ttlMs);
    bool AddAllowedType(const std::string& routeId, MessageType type);
    bool RemoveAllowedType(const std::string& routeId, MessageType type);

    // Message operations
    bool SendMessage(const RouteMessage& message);
    bool SendMessageAsync(const RouteMessage& message, const std::string& callbackId);
    bool BroadcastMessage(const std::string& sourceSystem, MessageType type, const std::string& payload);
    bool MulticastMessage(const std::vector<std::string>& routeIds, const RouteMessage& message);

    // Route queries
    const RouteDef* GetRoute(const std::string& routeId) const;
    std::vector<std::string> GetAllRouteIds() const;
    const RouteMessage* GetMessageById(const std::string& messageId) const;
    std::vector<std::string> GetMessagesByRoute(const std::string& routeId) const;
    std::vector<std::string> GetRoutesByProtocol(RouteProtocol protocol) const;
    std::vector<std::string> GetRoutesBySystem(const std::string& systemId) const;
    std::vector<std::string> GetActiveRoutes() const;
    std::vector<std::string> GetBlockedRoutes() const;

    // Message control
    bool AcknowledgeMessage(const std::string& messageId);
    bool RetryMessage(const std::string& messageId);
    bool CancelMessage(const std::string& messageId);

    // Logging
    const RouteLog* GetLog(const std::string& logId) const;
    std::vector<std::string> GetAllLogs() const;
    std::vector<std::string> GetLogsByRoute(const std::string& routeId) const;
    void FlushLogs();

    // Validation and maintenance
    bool ValidateRoute(const std::string& routeId) const;
    void Reset();

private:
    std::unordered_map<std::string, RouteDef> m_routes;
    std::unordered_map<std::string, RouteMessage> m_messages;
    std::unordered_map<std::string, RouteLog> m_logs;
    int m_nextMessageIndex{0};
    int m_nextLogIndex{0};
};

} // namespace Atlas::Engine
