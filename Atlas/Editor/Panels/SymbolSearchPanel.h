#pragma once
#include <string>
#include <vector>

namespace Atlas::Editor {

/// Phase 17D — Code intelligence: symbol search panel.
/// Queries the SymbolIndex via the AtlasAI bridge and displays
/// results with file/line jump-to-source navigation.
class SymbolSearchPanel {
public:
    struct SearchResult {
        std::string symbolName;
        std::string kind;
        std::string filePath;
        int line{0};
    };

    void SetQuery(const std::string& query);
    void ExecuteSearch();
    void NavigateTo(int resultIndex);
    void Clear();

    const std::string& GetQuery() const { return m_query; }
    const std::vector<SearchResult>& GetResults() const { return m_results; }
    int GetResultCount() const { return static_cast<int>(m_results.size()); }

private:
    std::string m_query;
    std::vector<SearchResult> m_results;
};

} // namespace Atlas::Editor
