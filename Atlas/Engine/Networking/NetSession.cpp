// NetSession.cpp
// Atlas Engine — network session management.

#include "Networking/NetSession.h"

#include <algorithm>

namespace atlas::net {

bool NetSession::Initialize(NetContext& context)
{
    m_context = &context;
    m_tick    = 0;
    return true;
}

void NetSession::Shutdown()
{
    m_clients.clear();
    m_handlers.clear();
    m_incomingQueue.clear();
    m_context = nullptr;
}

void NetSession::Tick(float deltaSeconds)
{
    ++m_tick;
    m_heartbeatTimer += deltaSeconds;
    if (m_heartbeatTimer >= m_heartbeatInterval)
    {
        SendHeartbeats();
        m_heartbeatTimer = 0.f;
    }
    ProcessIncoming();
}

// ---- client registry -------------------------------------------------------

bool NetSession::RegisterClient(const ClientEntry& entry)
{
    for (const auto& c : m_clients)
        if (c.peerId == entry.peerId) return false;
    m_clients.push_back(entry);
    return true;
}

bool NetSession::UpdateClientStatus(uint32_t peerId, EClientStatus status)
{
    ClientEntry* c = GetMutableClient(peerId);
    if (!c) return false;
    c->status = status;
    return true;
}

bool NetSession::SetClientPlayerId(uint32_t peerId, uint64_t playerId)
{
    ClientEntry* c = GetMutableClient(peerId);
    if (!c) return false;
    c->playerId = playerId;
    return true;
}

bool NetSession::RemoveClient(uint32_t peerId)
{
    auto it = std::find_if(m_clients.begin(), m_clients.end(),
                           [peerId](const ClientEntry& e){ return e.peerId == peerId; });
    if (it == m_clients.end()) return false;
    m_clients.erase(it);
    return true;
}

std::optional<ClientEntry> NetSession::FindClient(uint32_t peerId) const
{
    for (const auto& c : m_clients)
        if (c.peerId == peerId) return c;
    return std::nullopt;
}

std::vector<ClientEntry> NetSession::GetClientsByStatus(EClientStatus status) const
{
    std::vector<ClientEntry> result;
    for (const auto& c : m_clients)
        if (c.status == status) result.push_back(c);
    return result;
}

// ---- message send ----------------------------------------------------------

void NetSession::Send(uint32_t peerId, ENetMsgType msgType,
                       const std::vector<uint8_t>& payload)
{
    if (!m_context) return;
    Packet pkt;
    pkt.type    = static_cast<uint16_t>(msgType);
    pkt.payload = payload;
    pkt.tick    = static_cast<uint32_t>(m_tick);
    m_context->Send(peerId, pkt);
}

void NetSession::Broadcast(ENetMsgType msgType,
                             const std::vector<uint8_t>& payload)
{
    if (!m_context) return;
    Packet pkt;
    pkt.type    = static_cast<uint16_t>(msgType);
    pkt.payload = payload;
    pkt.tick    = static_cast<uint32_t>(m_tick);
    m_context->Broadcast(pkt);
}

void NetSession::BroadcastExcept(uint32_t excludePeerId, ENetMsgType msgType,
                                   const std::vector<uint8_t>& payload)
{
    for (const auto& client : m_clients)
        if (client.peerId != excludePeerId)
            Send(client.peerId, msgType, payload);
}

// ---- handler registration --------------------------------------------------

void NetSession::RegisterHandler(ENetMsgType msgType, NetMessageHandler handler)
{
    m_handlers[static_cast<uint16_t>(msgType)] = std::move(handler);
}

void NetSession::UnregisterHandler(ENetMsgType msgType)
{
    m_handlers.erase(static_cast<uint16_t>(msgType));
}

void NetSession::DispatchMessage(const NetMessage& msg)
{
    auto it = m_handlers.find(static_cast<uint16_t>(msg.msgType));
    if (it != m_handlers.end())
        it->second(msg);
}

void NetSession::EnqueueReceived(const NetMessage& msg)
{
    m_incomingQueue.push_back(msg);
}

void NetSession::ProcessIncoming()
{
    for (const auto& msg : m_incomingQueue)
        DispatchMessage(msg);
    m_incomingQueue.clear();
}

// ---- session info ----------------------------------------------------------

bool NetSession::IsServer() const
{
    return m_context &&
           (m_context->Mode() == NetMode::Server ||
            m_context->Mode() == NetMode::P2P_Host);
}

// ---- heartbeat -------------------------------------------------------------

void NetSession::SendHeartbeats()
{
    if (!IsServer()) return;
    for (const auto& client : m_clients)
    {
        if (client.status == EClientStatus::InGame)
            Send(client.peerId, ENetMsgType::Heartbeat);
    }
}

ClientEntry* NetSession::GetMutableClient(uint32_t peerId)
{
    for (auto& c : m_clients)
        if (c.peerId == peerId) return &c;
    return nullptr;
}

} // namespace atlas::net
