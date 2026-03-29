#pragma once
#include <string>
#include <vector>
#include <unordered_map>
#include <functional>

namespace Atlas::Engine {

/// Phase 19C — Registry managing multiple solar systems within a session.
/// Extends SolarSystemManager with cross-system lookup, activation tracking,
/// and iteration over all loaded systems.
class SolarSystemRegistry {
public:
    struct SystemRecord {
        std::string id;
        std::string name;
        std::string dataPath;
        bool loaded{false};
    };

    // Registration
    bool RegisterSystem(const std::string& id, const std::string& name,
                        const std::string& dataPath);
    bool UnregisterSystem(const std::string& id);
    bool IsRegistered(const std::string& id) const;
    int GetSystemCount() const { return static_cast<int>(m_systems.size()); }

    // Activation
    bool SetActiveSystem(const std::string& id);
    const std::string& GetActiveSystemId() const { return m_activeId; }
    bool HasActiveSystem() const { return !m_activeId.empty(); }

    // Lookup
    const SystemRecord* GetSystem(const std::string& id) const;
    std::vector<std::string> GetAllSystemIds() const;

    // Load state
    bool MarkLoaded(const std::string& id);
    bool IsLoaded(const std::string& id) const;
    int GetLoadedCount() const;

    // Traversal
    void ForEach(const std::function<void(const SystemRecord&)>& fn) const;

    // Lifecycle
    void Clear();

private:
    std::unordered_map<std::string, SystemRecord> m_systems;
    std::string m_activeId;
};

} // namespace Atlas::Engine
