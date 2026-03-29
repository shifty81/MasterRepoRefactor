#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P23 Tool — Material parameter collection authoring, parameter override management, and collection preview.
class MaterialParameterCollectionTool : public ITool {
public:
    enum class ParameterType { Scalar, Vector, Texture, Bool, Int, Custom };
    enum class CollectionScope { Global, Level, Actor, Component, Custom };
    enum class OverrideMode { Replace, Add, Multiply, Lerp, Custom };
    enum class CollectionEventType { Created, Updated, Deleted, Overridden, Reset, Custom };

    struct MPCParameterDef {
        std::string parameterId;
        std::string parameterName;
        ParameterType type{ParameterType::Scalar};
        CollectionScope scope{CollectionScope::Global};
        std::string defaultValue;
    };

    struct MPCCollectionDef {
        std::string collectionId;
        std::string collectionName;
        std::string description;
        std::vector<std::string> parameterIds;
    };

    struct ParameterOverrideEntry {
        std::string overrideId;
        std::string collectionId;
        std::string parameterId;
        OverrideMode mode{OverrideMode::Replace};
        std::string overrideValue;
        std::string targetActorId;
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "MaterialParameterCollectionTool"; }
    bool IsActive() const override { return m_active; }

    std::string CreateCollection(const MPCCollectionDef& def);
    bool DeleteCollection(const std::string& collectionId);
    const MPCCollectionDef* GetCollection(const std::string& collectionId) const;
    std::vector<std::string> GetAllCollectionIds() const;
    bool AddParameter(const std::string& collectionId, const MPCParameterDef& param);
    bool RemoveParameter(const std::string& collectionId, const std::string& parameterId);
    const MPCParameterDef* GetParameter(const std::string& parameterId) const;
    std::vector<std::string> GetAllParameterIds() const;
    std::vector<std::string> GetParametersByType(ParameterType type) const;
    std::vector<std::string> GetParametersByScope(CollectionScope scope) const;
    bool AddOverride(const ParameterOverrideEntry& entry);
    bool RemoveOverride(const std::string& overrideId);
    const ParameterOverrideEntry* GetOverride(const std::string& overrideId) const;
    std::vector<std::string> GetOverridesByCollection(const std::string& collectionId) const;
    std::vector<std::string> GetOverridesByActor(const std::string& targetActorId) const;
    bool ApplyOverrides(const std::string& collectionId);
    bool ResetOverrides(const std::string& collectionId);
    void CreateCollectionEvent(const std::string& collectionId, CollectionEventType eventType);
    std::vector<std::string> GetCollectionEvents(const std::string& collectionId) const;
    void Reset();

private:
    bool m_active{false};
    std::unordered_map<std::string, MPCCollectionDef> m_collections;
    std::unordered_map<std::string, MPCParameterDef> m_parameters;
    std::unordered_map<std::string, ParameterOverrideEntry> m_overrides;
    int m_nextCollectionIndex{0};
};

} // namespace Atlas::Editor
