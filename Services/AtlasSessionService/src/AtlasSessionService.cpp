// AtlasSessionService.cpp
#include "AtlasSessionService.h"
#include <sstream>

namespace Atlas::Services
{

void AtlasSessionService::initialise() {}

void AtlasSessionService::shutdown()
{
    for (auto& s : sessions_)
        s.state = SessionState::Terminated;
}

std::string AtlasSessionService::createSession(const std::string& clientId,
                                                const std::string& projectId)
{
    std::ostringstream ss;
    ss << "sess-" << ++sessionCounter_;
    SessionProfile p;
    p.sessionId = ss.str();
    p.clientId  = clientId;
    p.projectId = projectId;
    p.state     = SessionState::Active;
    p.createdAt = "stub-timestamp";
    sessions_.push_back(p);
    return p.sessionId;
}

bool AtlasSessionService::activateSession(const std::string& id)
{
    for (auto& s : sessions_)
        if (s.sessionId == id) { s.state = SessionState::Active; return true; }
    return false;
}

bool AtlasSessionService::suspendSession(const std::string& id)
{
    for (auto& s : sessions_)
        if (s.sessionId == id && s.state == SessionState::Active)
        { s.state = SessionState::Suspended; return true; }
    return false;
}

bool AtlasSessionService::terminateSession(const std::string& id)
{
    for (auto& s : sessions_)
        if (s.sessionId == id) { s.state = SessionState::Terminated; return true; }
    return false;
}

std::optional<SessionProfile> AtlasSessionService::findSession(const std::string& id) const
{
    for (const auto& s : sessions_)
        if (s.sessionId == id) return s;
    return std::nullopt;
}

std::vector<SessionProfile> AtlasSessionService::listActiveSessions() const
{
    std::vector<SessionProfile> result;
    for (const auto& s : sessions_)
        if (s.state == SessionState::Active) result.push_back(s);
    return result;
}

SessionCapabilities AtlasSessionService::getCapabilities() const { return caps_; }

} // namespace Atlas::Services
