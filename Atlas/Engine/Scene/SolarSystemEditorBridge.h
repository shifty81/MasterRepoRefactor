#pragma once
#include <string>
#include <vector>
#include <functional>

namespace Atlas::Engine {

/// Phase 18D — Wires ToolLayer editor operations to solar system scene entities.
/// Translates high-level tool actions (select, move, spawn) into scene mutations
/// and records them as DeltaEdits for propagation and rollback.
class SolarSystemEditorBridge {
public:
    struct EditRecord {
        std::string entityId;
        std::string propertyName;
        std::string oldValue;
        std::string newValue;
    };

    void SetActiveSystem(const std::string& systemId);
    const std::string& GetActiveSystem() const { return m_activeSystem; }

    // Entity selection
    void SelectEntity(const std::string& entityId);
    void ClearSelection();
    const std::vector<std::string>& GetSelection() const { return m_selection; }

    // Property edits (recorded as DeltaEdits)
    bool EditProperty(const std::string& entityId, const std::string& property,
                      const std::string& newValue);
    bool MoveEntity(const std::string& entityId, float newOrbitRadius);

    // Edit history
    const std::vector<EditRecord>& GetEditHistory() const { return m_history; }
    int GetEditCount() const { return static_cast<int>(m_history.size()); }
    bool UndoLastEdit();
    void ClearHistory();

    // PCG baseline propagation
    void PropagateEditsToBaseline();
    bool HasUncommittedEdits() const { return !m_history.empty(); }

    // Callbacks
    void SetOnEditCallback(std::function<void(const EditRecord&)> cb);

private:
    std::string m_activeSystem;
    std::vector<std::string> m_selection;
    std::vector<EditRecord> m_history;
    std::function<void(const EditRecord&)> m_onEdit;
};

} // namespace Atlas::Engine
