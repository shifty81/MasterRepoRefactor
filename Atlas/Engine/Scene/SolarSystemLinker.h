#pragma once
#include <string>
#include <vector>
#include <unordered_map>
#include <functional>

namespace Atlas::Engine {

/// Phase 20C — Manages cross-system jump connections and stargate/wormhole links
/// between solar systems registered in the SolarSystemRegistry.
class SolarSystemLinker {
public:
    struct SystemLink {
        std::string linkId;
        std::string fromSystemId;
        std::string toSystemId;
        std::string fromEntityId;
        std::string toEntityId;
        bool bidirectional{true};
        std::string linkType;  // "stargate" | "wormhole" | "jump_bridge"
    };

    // Link management
    std::string AddLink(const std::string& fromSystem, const std::string& toSystem,
                        const std::string& fromEntityId, const std::string& toEntityId,
                        const std::string& linkType = "stargate",
                        bool bidirectional = true);
    bool RemoveLink(const std::string& linkId);
    bool HasLink(const std::string& linkId) const;
    int GetLinkCount() const { return static_cast<int>(m_links.size()); }

    // Lookup
    const SystemLink* GetLink(const std::string& linkId) const;
    std::vector<SystemLink> GetLinksFrom(const std::string& systemId) const;
    std::vector<SystemLink> GetLinksTo(const std::string& systemId) const;
    std::vector<std::string> GetReachableSystems(const std::string& fromSystem) const;

    // Pathfinding
    std::vector<std::string> FindPath(const std::string& fromSystem,
                                      const std::string& toSystem) const;

    // Lifecycle
    void Clear();

    // Change notification
    void SetOnLinkChangedCallback(std::function<void(const SystemLink&)> cb);

private:
    std::unordered_map<std::string, SystemLink> m_links;
    int m_nextIndex{0};
    std::function<void(const SystemLink&)> m_onLinkChanged;
};

} // namespace Atlas::Engine
