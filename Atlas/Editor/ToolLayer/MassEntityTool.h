#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P18 Tool — Mass Entity archetype authoring, fragment configuration, and processor management.
class MassEntityTool : public ITool {
public:
    enum class MassFragmentAccess { None, ReadOnly, ReadWrite, Optional };
    enum class ProcessorPhase { PrePhysics, Physics, PostPhysics, FrameStart, FrameEnd, Async };
    enum class EntityLifetime { Transient, Persistent, Session, Level, Asset };

    struct MassFragmentDef {
        std::string fragmentId;
        std::string name;
        std::string structPath;
        MassFragmentAccess access{MassFragmentAccess::ReadWrite};
        int sizeBytes{0};
        std::vector<std::string> tags;
    };

    struct MassProcessorDef {
        std::string processorId;
        std::string name;
        ProcessorPhase phase{ProcessorPhase::PrePhysics};
        std::vector<std::string> queryFragments;
        std::vector<std::string> writeFragments;
        int priority{0};
        bool enabled{true};
    };

    struct MassArchetypeDef {
        std::string archetypeId;
        std::string name;
        std::vector<std::string> fragments;
        std::vector<std::string> processors;
        int entityCount{0};
        EntityLifetime lifetime{EntityLifetime::Persistent};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "MassEntityTool"; }
    bool IsActive() const override { return m_active; }

    std::string CreateArchetype(const std::string& name);
    bool RemoveArchetype(const std::string& archetypeId);
    std::string AddFragment(const std::string& archetypeId, const std::string& name, const std::string& structPath);
    bool RemoveFragment(const std::string& archetypeId, const std::string& fragmentId);
    std::string AddProcessor(const std::string& archetypeId, const std::string& name, ProcessorPhase phase);
    bool RemoveProcessor(const std::string& archetypeId, const std::string& processorId);
    bool SetFragmentAccess(const std::string& fragmentId, MassFragmentAccess access);
    bool SetProcessorPhase(const std::string& processorId, ProcessorPhase phase);
    bool SetProcessorPriority(const std::string& processorId, int priority);
    bool SetEntityCount(const std::string& archetypeId, int count);
    bool SetEntityLifetime(const std::string& archetypeId, EntityLifetime lifetime);
    bool SpawnEntities(const std::string& archetypeId, int count);
    bool DespawnEntities(const std::string& archetypeId);
    bool PreviewArchetype(const std::string& archetypeId);
    const MassArchetypeDef* GetArchetype(const std::string& archetypeId) const;
    const MassFragmentDef* GetFragment(const std::string& fragmentId) const;
    const MassProcessorDef* GetProcessor(const std::string& processorId) const;
    std::vector<std::string> GetAllArchetypeIds() const;
    std::vector<std::string> GetFragmentsByArchetype(const std::string& archetypeId) const;
    std::vector<std::string> GetProcessorsByPhase(ProcessorPhase phase) const;
    bool ValidateArchetype(const std::string& archetypeId) const;
    bool ExportArchetype(const std::string& archetypeId, const std::string& filePath) const;
    bool SaveArchetypes(const std::string& filePath) const;
    bool LoadArchetypes(const std::string& filePath);
    void ClearAll();

private:
    bool m_active{false};
    std::unordered_map<std::string, MassArchetypeDef> m_archetypes;
    std::unordered_map<std::string, MassFragmentDef> m_fragments;
    std::unordered_map<std::string, MassProcessorDef> m_processors;
    int m_nextArchetypeIndex{0};
    int m_nextFragmentIndex{0};
    int m_nextProcessorIndex{0};
};

} // namespace Atlas::Editor
