#pragma once
#include <string>
#include <vector>
#include <unordered_map>
#include <functional>

namespace Atlas::Engine {

/// Phase 36C — Gateway for controlled solar system access, authentication, and proxy routing.
class SolarSystemGateway {
public:
    enum class GatewayState { Closed, Opening, Open, Throttled, Overloaded, Draining, Error };
    enum class AccessPolicy { Public, Private, Restricted, Authenticated, Federated, Custom };
    enum class GatewayEventType { Connect, Disconnect, Request, Response, Timeout, Error, RateLimit, Custom };

    struct GatewayConfig {
        std::string configId;
        std::string name;
        AccessPolicy policy{AccessPolicy::Public};
        int maxConnections{100};
        float rateLimitRps{1000.0f};
        bool authRequired{false};
        std::vector<std::string> allowedSystems;
        long long timeout{30000};
    };

    struct GatewayRequest {
        std::string requestId;
        std::string gatewayId;
        std::string sourceSystem;
        std::string targetSystem;
        std::string payload;
        std::string authToken;
        long long timestamp{0};
        int retryCount{0};
    };

    struct GatewayAuditEntry {
        std::string entryId;
        std::string requestId;
        std::string gatewayId;
        bool success{false};
        double elapsedMs{0.0};
        int statusCode{200};
        std::string message;
    };

    // Gateway management
    bool RegisterGateway(const GatewayConfig& config);
    bool UnregisterGateway(const std::string& gatewayId);
    bool SetGatewayPolicy(const std::string& gatewayId, AccessPolicy policy);
    bool SetMaxConnections(const std::string& gatewayId, int maxConnections);
    bool SetRateLimit(const std::string& gatewayId, float rps);
    bool SetAuthRequired(const std::string& gatewayId, bool required);
    bool AddAllowedSystem(const std::string& gatewayId, const std::string& systemId);
    bool RemoveAllowedSystem(const std::string& gatewayId, const std::string& systemId);

    // Gateway lifecycle
    bool OpenGateway(const std::string& gatewayId);
    bool CloseGateway(const std::string& gatewayId);
    bool ThrottleGateway(const std::string& gatewayId);

    // Request operations
    bool SendRequest(const GatewayRequest& request);
    bool SendRequestAsync(const GatewayRequest& request, const std::string& callbackId);

    // Queries
    const GatewayConfig* GetGateway(const std::string& gatewayId) const;
    std::vector<std::string> GetAllGatewayIds() const;
    const GatewayRequest* GetRequestById(const std::string& requestId) const;
    std::vector<std::string> GetRequestsByGateway(const std::string& gatewayId) const;
    std::vector<std::string> GetOpenGateways() const;
    std::vector<std::string> GetThrottledGateways() const;

    // Auth and validation
    bool AuthenticateRequest(const std::string& requestId);
    bool ValidateRequest(const GatewayRequest& request) const;
    bool CancelRequest(const std::string& requestId);

    // Audit log
    const GatewayAuditEntry* GetAuditEntry(const std::string& entryId) const;
    std::vector<std::string> GetAuditEntriesByGateway(const std::string& gatewayId) const;
    std::vector<std::string> GetAllAuditEntries() const;
    void FlushAuditLog();

    void Reset();

private:
    std::unordered_map<std::string, GatewayConfig> m_gateways;
    std::unordered_map<std::string, GatewayState> m_gatewayStates;
    std::unordered_map<std::string, GatewayRequest> m_requests;
    std::unordered_map<std::string, GatewayAuditEntry> m_auditLog;
    int m_nextRequestIndex{0};
    int m_nextAuditIndex{0};
};

} // namespace Atlas::Engine
