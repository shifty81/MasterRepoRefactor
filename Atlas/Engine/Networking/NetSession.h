// NetSession.h
// Atlas Engine — network session management: client registry, authenticated
// peer tracking, packet routing, and server-client message protocol.

#pragma once
#include "Networking/NetContext.h"

#include <functional>
#include <optional>
#include <string>
#include <unordered_map>
#include <vector>

namespace atlas::net {

// ---------------------------------------------------------------------------
// Message type codes (application-level)
// ---------------------------------------------------------------------------

enum class ENetMsgType : uint16_t
{
    // ---- session lifecycle ---
    JoinRequest   = 0x0001,
    JoinAccepted  = 0x0002,
    JoinRejected  = 0x0003,
    Disconnect    = 0x0004,
    Heartbeat     = 0x0005,

    // ---- world sync ---
    WorldSnapshot = 0x0010,
    EntitySpawn   = 0x0011,
    EntityDestroy = 0x0012,
    EntityUpdate  = 0x0013,

    // ---- player input ---
    PlayerInput   = 0x0020,
    PlayerRPC     = 0x0021,

    // ---- game events ---
    ChatMessage   = 0x0030,
    GameEvent     = 0x0031,
    ServerNotify  = 0x0032,

    // ---- economy/inventory ---
    InventorySync = 0x0040,
    TradeOffer    = 0x0041,
    ContractSync  = 0x0042,

    Custom        = 0xFF00,
};

// ---------------------------------------------------------------------------
// Client entry in the registry
// ---------------------------------------------------------------------------

enum class EClientStatus : uint8_t
{
    Connecting,
    Authenticated,
    InGame,
    Disconnected,
};

struct ClientEntry
{
    uint32_t      peerId       = 0;
    std::string   displayName;
    uint64_t      playerId     = 0;    ///< mapped game entity
    EClientStatus status       = EClientStatus::Connecting;
    float         rtt          = 0.f;  ///< round-trip time ms
    uint32_t      lastHeartbeat = 0;   ///< server tick
    bool          isHost       = false;
};

// ---------------------------------------------------------------------------
// Typed message wrapper
// ---------------------------------------------------------------------------

struct NetMessage
{
    ENetMsgType          msgType    = ENetMsgType::Custom;
    uint32_t             senderPeerId = 0;
    std::vector<uint8_t> payload;
};

// ---------------------------------------------------------------------------
// Message handler callback
// ---------------------------------------------------------------------------

using NetMessageHandler = std::function<void(const NetMessage&)>;

// ---------------------------------------------------------------------------
// NetSession
// ---------------------------------------------------------------------------

class NetSession
{
public:
    NetSession()  = default;
    ~NetSession() = default;

    bool Initialize(NetContext& context);
    void Shutdown();
    void Tick(float deltaSeconds);

    // ---- client registry (server-side) ---------------------------------
    bool            RegisterClient   (const ClientEntry& entry);
    bool            UpdateClientStatus(uint32_t peerId, EClientStatus status);
    bool            SetClientPlayerId(uint32_t peerId, uint64_t playerId);
    bool            RemoveClient     (uint32_t peerId);
    size_t          ClientCount()    const { return m_clients.size(); }
    std::optional<ClientEntry> FindClient(uint32_t peerId) const;
    std::vector<ClientEntry>   GetClientsByStatus(EClientStatus status) const;
    std::vector<ClientEntry>   GetAllClients()     const { return m_clients; }

    // ---- message send --------------------------------------------------
    void Send        (uint32_t peerId, ENetMsgType msgType,
                      const std::vector<uint8_t>& payload = {});
    void Broadcast   (ENetMsgType msgType,
                      const std::vector<uint8_t>& payload = {});
    void BroadcastExcept(uint32_t excludePeerId, ENetMsgType msgType,
                          const std::vector<uint8_t>& payload = {});

    // ---- message routing (handler registration) -----------------------
    void RegisterHandler(ENetMsgType msgType, NetMessageHandler handler);
    void UnregisterHandler(ENetMsgType msgType);
    void DispatchMessage(const NetMessage& msg);

    // ---- received message queue ----------------------------------------
    void EnqueueReceived(const NetMessage& msg);
    void ProcessIncoming();

    // ---- session info --------------------------------------------------
    bool     IsServer()   const;
    uint32_t LocalPeerId() const { return m_localPeerId; }
    uint64_t TickNumber()  const { return m_tick; }

    // ---- heartbeat management ------------------------------------------
    void SetHeartbeatIntervalSeconds(float interval)
    { m_heartbeatInterval = interval; }

private:
    NetContext*                                    m_context = nullptr;
    std::vector<ClientEntry>                       m_clients;
    std::unordered_map<uint16_t, NetMessageHandler> m_handlers;
    std::vector<NetMessage>                        m_incomingQueue;
    uint64_t                                       m_tick            = 0;
    float                                          m_heartbeatTimer  = 0.f;
    float                                          m_heartbeatInterval = 1.f;
    uint32_t                                       m_localPeerId     = 0;

    ClientEntry* GetMutableClient(uint32_t peerId);
    void         SendHeartbeats();
};

} // namespace atlas::net
