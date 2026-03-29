#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P25 Tool — Scene hierarchy filtering, visibility masking, and component-type isolation.
class HierarchyFilterTool : public ITool {
public:
    enum class FilterCriteria { ByTag, ByType, ByName, ByLayer, ByComponent, Custom };
    enum class FilterOperator { And, Or, Not, Custom };
    enum class FilterVisibilityMode { ShowAll, HideFiltered, IsolateFiltered, DimFiltered, Custom };
    enum class HierarchyViewMode { Flat, Tree, Layer, Component, Custom };

    struct HierarchyFilterDef {
        std::string filterId;
        std::string filterName;
        FilterCriteria criteria{FilterCriteria::ByTag};
        FilterOperator op{FilterOperator::And};
        std::string expr;
        FilterVisibilityMode visibilityMode{FilterVisibilityMode::ShowAll};
        bool enabled{true};
    };

    struct FilterGroupDef {
        std::string groupId;
        std::string groupName;
        std::vector<std::string> filterIds;
        FilterOperator groupOp{FilterOperator::And};
        bool active{false};
    };

    struct HierarchyViewConfig {
        std::string viewConfigId;
        HierarchyViewMode viewMode{HierarchyViewMode::Tree};
        std::vector<std::string> activeFilterIds;
        bool showHidden{false};
        bool showPrefabs{true};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "HierarchyFilterTool"; }
    bool IsActive() const override { return m_active; }

    bool CreateFilter(const HierarchyFilterDef& filter);
    bool DeleteFilter(const std::string& filterId);
    const HierarchyFilterDef* GetFilter(const std::string& filterId) const;
    std::vector<std::string> GetAllFilterIds() const;
    std::vector<std::string> GetFiltersByCriteria(FilterCriteria criteria) const;
    bool CreateGroup(const FilterGroupDef& group);
    bool DeleteGroup(const std::string& groupId);
    const FilterGroupDef* GetGroup(const std::string& groupId) const;
    std::vector<std::string> GetAllGroupIds() const;
    std::vector<std::string> GetGroupsByFilter(const std::string& filterId) const;
    bool SetViewConfig(const HierarchyViewConfig& config);
    const HierarchyViewConfig* GetViewConfig(const std::string& viewConfigId) const;
    bool ApplyFilter(const std::string& filterId);
    void ClearFilters();
    std::vector<std::string> GetActiveFilters() const;
    std::vector<std::string> GetFilteredActors() const;
    void Reset();

private:
    bool m_active{false};
    std::unordered_map<std::string, HierarchyFilterDef> m_filters;
    std::unordered_map<std::string, FilterGroupDef> m_groups;
    std::unordered_map<std::string, HierarchyViewConfig> m_viewConfigs;
};

} // namespace Atlas::Editor
