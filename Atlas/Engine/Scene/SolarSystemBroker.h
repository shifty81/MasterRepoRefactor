#pragma once
#include <string>
#include <vector>
#include <unordered_map>
#include <functional>

namespace Atlas::Engine {

/// Phase 37C — Message broker for solar system inter-system communication and pub/sub routing.
class SolarSystemBroker {
public:
    enum class BrokerState { Idle, Active, Busy, Suspended, Overloaded, Error };
    enum class MessagePriority { Critical, High, Normal, Low, Deferred, Custom };
    enum class BrokerTopicType { Broadcast, Direct, Multicast, Fanout, Request, Response, Custom };
    enum class BrokerEventType { Subscribe, Unsubscribe, Publish, Receive, Timeout, Error, Custom };

    struct BrokerConfig {
        std::string configId;
        std::string name;
        BrokerTopicType defaultTopic{BrokerTopicType::Broadcast};
        int maxSubscribers{100};
        float throughputLimit{10000.0f};
        bool persistMessages{false};
        bool enableMetrics{true};
    };

    struct BrokerMessage {
        std::string messageId;
        std::string topicId;
        std::string senderId;
        std::string payload;
        MessagePriority priority{MessagePriority::Normal};
        long long timestamp{0};
        int ttl{0};
        bool acknowledged{false};
    };

    struct BrokerSubscription {
        std::string subscriptionId;
        std::string topicId;
        std::string subscriberId;
        std::string filterExpr;
        bool active{true};
    };

    // Broker management
    bool RegisterBroker(const BrokerConfig& config);
    bool UnregisterBroker(const std::string& brokerId);
    bool SetBrokerState(const std::string& brokerId, BrokerState state);
    BrokerState GetBrokerState(const std::string& brokerId) const;

    // Topic management
    bool CreateTopic(const std::string& brokerId, const std::string& topicId, BrokerTopicType topicType);
    bool DeleteTopic(const std::string& topicId);
    const std::string* GetTopic(const std::string& topicId) const;
    std::vector<std::string> GetAllTopicIds() const;

    // Subscription management
    bool Subscribe(const BrokerSubscription& subscription);
    bool Unsubscribe(const std::string& subscriptionId);
    const BrokerSubscription* GetSubscription(const std::string& subscriptionId) const;
    std::vector<std::string> GetSubscriptionsByTopic(const std::string& topicId) const;
    std::vector<std::string> GetActiveSubscriptions() const;

    // Message operations
    bool PublishMessage(const BrokerMessage& message);
    bool BroadcastMessage(const std::string& brokerId, const BrokerMessage& message);
    const BrokerMessage* GetMessage(const std::string& messageId) const;
    std::vector<std::string> GetMessagesByTopic(const std::string& topicId) const;
    std::vector<std::string> GetUnacknowledgedMessages() const;
    bool AcknowledgeMessage(const std::string& messageId);
    bool PurgeMessages(const std::string& topicId);

    // Metrics
    std::string GetBrokerMetrics(const std::string& brokerId) const;
    void ResetMetrics(const std::string& brokerId);

    void Reset();

private:
    std::unordered_map<std::string, BrokerConfig> m_brokers;
    std::unordered_map<std::string, BrokerState> m_brokerStates;
    std::unordered_map<std::string, std::string> m_topics;
    std::unordered_map<std::string, BrokerSubscription> m_subscriptions;
    std::unordered_map<std::string, BrokerMessage> m_messages;
    int m_nextIndex{0};
};

} // namespace Atlas::Engine
