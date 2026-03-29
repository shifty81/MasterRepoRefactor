#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P20 Tool — Online subsystem session management, lobby configuration, and matchmaking pipeline authoring.
class OnlineSubsystemTool : public ITool {
public:
    enum class SessionState { Pending, Creating, Active, Ending, Destroyed, Searching, Error };
    enum class LobbyVisibility { Public, Private, FriendsOnly, Invite, Custom };
    enum class MatchmakingPhase { Idle, Gathering, Evaluating, Confirming, Starting, Cancelled, Error };

    struct SessionConfig {
        std::string sessionId;
        std::string sessionName;
        int maxPlayers{16};
        int minPlayers{2};
        LobbyVisibility visibility{LobbyVisibility::Public};
        std::string region;
        bool allowJoinInProgress{false};
        float sessionTimeout{300.0f};
    };

    struct LobbyConfig {
        std::string lobbyId;
        std::string name;
        int capacity{16};
        bool publicSearch{true};
        std::vector<std::string> tags;
        std::vector<std::string> allowedPlayerIds;
        std::string ownerPlayerId;
    };

    struct MatchmakingRule {
        std::string ruleId;
        std::string name;
        float skillTolerance{100.0f};
        float latencyBudgetMs{150.0f};
        bool requireSameRegion{false};
        int minGroupSize{1};
        int maxGroupSize{5};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "OnlineSubsystemTool"; }
    bool IsActive() const override { return m_active; }

    std::string CreateSession(const SessionConfig& config);
    bool DestroySession(const std::string& sessionId);
    bool JoinSession(const std::string& sessionId, const std::string& playerId);
    bool LeaveSession(const std::string& sessionId, const std::string& playerId);
    SessionState GetSessionState(const std::string& sessionId) const;
    const SessionConfig* GetSessionConfig(const std::string& sessionId) const;
    std::vector<std::string> GetAllSessionIds() const;
    bool SetSessionVisibility(const std::string& sessionId, LobbyVisibility visibility);
    bool SetMaxPlayers(const std::string& sessionId, int maxPlayers);

    std::string CreateLobby(const LobbyConfig& config);
    bool CloseLobby(const std::string& lobbyId);
    bool AddPlayerToLobby(const std::string& lobbyId, const std::string& playerId);
    bool RemovePlayerFromLobby(const std::string& lobbyId, const std::string& playerId);
    std::vector<std::string> GetLobbyPlayers(const std::string& lobbyId) const;

    std::string AddMatchmakingRule(const MatchmakingRule& rule);
    bool RemoveMatchmakingRule(const std::string& ruleId);
    const MatchmakingRule* GetMatchmakingRule(const std::string& ruleId) const;
    bool StartMatchmaking(const std::string& sessionId, const std::string& ruleId);
    bool CancelMatchmaking(const std::string& sessionId);
    MatchmakingPhase GetMatchmakingPhase(const std::string& sessionId) const;

    bool ValidateSession(const std::string& sessionId) const;
    bool SaveConfig(const std::string& filePath) const;
    bool LoadConfig(const std::string& filePath);
    void Reset();

private:
    bool m_active{false};
    std::unordered_map<std::string, SessionConfig> m_sessions;
    std::unordered_map<std::string, LobbyConfig> m_lobbies;
    std::unordered_map<std::string, MatchmakingRule> m_rules;
    int m_nextSessionIndex{0};
    int m_nextLobbyIndex{0};
};

} // namespace Atlas::Editor
