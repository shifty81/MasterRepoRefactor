// AtlasSessionService.h
// Session service — workspace state, active project, and tool session coordination.

#pragma once
#include <cstdint>
#include <string>
#include <vector>
#include <optional>

namespace Atlas::Services
{

enum class SessionState : uint8_t
{
    Disconnected, Connecting, Active, Suspended, Terminated
};

struct SessionProfile
{
    std::string sessionId;
    std::string clientId;       ///< e.g. "AtlasAI.WpfHost"
    std::string projectId;
    SessionState state         = SessionState::Disconnected;
    std::string  createdAt;
    std::string  lastActiveAt;
};

struct SessionCapabilities
{
    bool supportsViewportAttach  = false;
    bool supportsLivePatch       = false;
    bool supportsAISession       = true;
    bool supportsProjectIndexing = true;
    bool supportsMultiWorkspace  = false;
};

class AtlasSessionService
{
public:
    AtlasSessionService()  = default;
    ~AtlasSessionService() = default;

    void initialise();
    void shutdown();

    std::string       createSession(const std::string& clientId, const std::string& projectId);
    bool              activateSession(const std::string& sessionId);
    bool              suspendSession(const std::string& sessionId);
    bool              terminateSession(const std::string& sessionId);

    std::optional<SessionProfile> findSession(const std::string& sessionId) const;
    std::vector<SessionProfile>   listActiveSessions() const;
    SessionCapabilities           getCapabilities() const;

private:
    std::vector<SessionProfile> sessions_;
    uint32_t sessionCounter_ = 0;
    SessionCapabilities caps_;
};

} // namespace Atlas::Services
