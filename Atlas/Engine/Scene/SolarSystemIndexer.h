#pragma once
#include <string>
#include <vector>
#include <unordered_map>
#include <functional>

namespace Atlas::Engine {

/// Phase 41C — Indexer for solar system asset cataloging, search, and cross-reference tracking.
class SolarSystemIndexer {
public:
    enum class IndexState { Unindexed, Indexing, Indexed, Stale, Error, Custom };
    enum class AssetCategory { Star, Planet, Moon, Station, Anomaly, Belt, Nebula, Custom };
    enum class SearchScope { Local, Regional, Global, Custom };
    enum class IndexSortOrder { ByName, ByType, ByOrbit, ByMass, ByPopulation, Custom };

    struct IndexEntryDef {
        std::string entryId;
        std::string systemId;
        std::string assetId;
        AssetCategory category{AssetCategory::Planet};
        std::string displayName;
        double orbitRadius{0.0};
        double mass{0.0};
        long long population{0};
        bool habitable{false};
        IndexState state{IndexState::Unindexed};
        std::string parentAssetId;
    };

    struct SearchQueryDef {
        std::string queryId;
        std::string queryText;
        SearchScope scope{SearchScope::Local};
        AssetCategory categoryFilter{AssetCategory::Planet};
        bool habitableOnly{false};
        bool hasCategoryFilter{false};
        double minOrbitRadius{0.0};
        double maxOrbitRadius{1e9};
        IndexSortOrder sortOrder{IndexSortOrder::ByName};
    };

    struct SearchResultDef {
        std::string resultId;
        std::string queryId;
        std::vector<std::string> matchedEntryIds;
        int totalMatches{0};
        long long searchTimestampMs{0};
        bool truncated{false};
    };

    // Index entry management
    bool AddEntry(const IndexEntryDef& entry);
    bool RemoveEntry(const std::string& entryId);
    bool UpdateEntryState(const std::string& entryId, IndexState state);
    bool MarkStale(const std::string& systemId);
    bool ReindexEntry(const std::string& entryId);
    const IndexEntryDef* GetEntry(const std::string& entryId) const;
    std::vector<std::string> GetAllEntryIds() const;
    std::vector<std::string> GetEntriesBySystem(const std::string& systemId) const;
    std::vector<std::string> GetEntriesByCategory(AssetCategory category) const;
    std::vector<std::string> GetHabitableEntries() const;
    std::vector<std::string> GetEntriesByState(IndexState state) const;
    std::vector<std::string> GetStaleEntries() const;

    // Search
    bool ExecuteSearch(const SearchQueryDef& query, SearchResultDef& outResult);
    bool SaveQuery(const SearchQueryDef& query);
    bool DeleteQuery(const std::string& queryId);
    const SearchQueryDef* GetQuery(const std::string& queryId) const;
    std::vector<std::string> GetAllQueryIds() const;
    const SearchResultDef* GetLastResultForQuery(const std::string& queryId) const;

    // Cross-reference
    std::vector<std::string> GetChildAssets(const std::string& parentAssetId) const;
    std::vector<std::string> GetSiblingAssets(const std::string& assetId) const;
    bool HasEntry(const std::string& assetId) const;
    int GetEntryCountBySystem(const std::string& systemId) const;

    void Reset();

private:
    std::unordered_map<std::string, IndexEntryDef> m_entries;
    std::unordered_map<std::string, SearchQueryDef> m_queries;
    std::unordered_map<std::string, SearchResultDef> m_results;
    IndexState m_globalState{IndexState::Unindexed};
};

} // namespace Atlas::Engine
