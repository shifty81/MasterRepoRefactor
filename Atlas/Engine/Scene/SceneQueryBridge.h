#pragma once
#include <string>
#include <vector>
#include <functional>

namespace Atlas::Engine {

/// Phase 19D — Bridges the C++ SceneManager to the AtlasAI SceneQueryEngine.
/// Serialises scene entity state to JSON so that the Python intelligence
/// layer can execute queries without requiring a live C++ runtime.
class SceneQueryBridge {
public:
    struct EntitySnapshot {
        std::string entityId;
        std::string entityType;
        float x{0.0f};
        float y{0.0f};
        float z{0.0f};
        std::vector<std::string> tags;
    };

    // Snapshot management
    void AddEntity(const EntitySnapshot& entity);
    bool RemoveEntity(const std::string& entityId);
    bool HasEntity(const std::string& entityId) const;
    int GetEntityCount() const { return static_cast<int>(m_entities.size()); }

    // Query helpers (C++-side)
    std::vector<EntitySnapshot> QueryByType(const std::string& entityType) const;
    std::vector<EntitySnapshot> QueryByTag(const std::string& tag) const;

    // JSON export (consumed by Python SceneQueryEngine)
    std::string ExportToJson() const;
    bool ExportToFile(const std::string& path) const;

    // Snapshot lifecycle
    void Clear();
    void SetSystemId(const std::string& systemId);
    const std::string& GetSystemId() const { return m_systemId; }

    // Change notification
    void SetOnSnapshotChanged(std::function<void()> cb);

private:
    std::vector<EntitySnapshot> m_entities;
    std::string m_systemId;
    std::function<void()> m_onChanged;
};

} // namespace Atlas::Engine
