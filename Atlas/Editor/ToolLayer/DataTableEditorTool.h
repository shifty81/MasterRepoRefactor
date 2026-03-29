#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P14 Tool — Data table editor with column/row management, import/export
class DataTableEditorTool : public ITool {
public:
    enum class ColumnType { String, Integer, Float, Bool, Reference, Enum, Color };
    enum class TableFormat { CSV, JSON, Binary };

    struct ColumnDef {
        std::string columnId;
        std::string name;
        ColumnType type{ColumnType::String};
        std::string defaultValue;
        bool required{false};
        bool indexed{false};
    };

    struct RowData {
        std::string rowId;
        int rowIndex{0};
        std::unordered_map<std::string, std::string> cells;
        bool dirty{false};
    };

    struct TableSchema {
        std::string schemaId;
        std::string tableName;
        std::vector<ColumnDef> columns;
        TableFormat format{TableFormat::JSON};
        int version{1};
    };

    struct TableDiff {
        std::string diffId;
        std::string fromVersion;
        std::string toVersion;
        std::vector<std::string> addedRows;
        std::vector<std::string> removedRows;
        std::vector<std::string> modifiedRows;
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "DataTableEditorTool"; }
    bool IsActive() const override { return m_active; }

    std::string CreateTable(const std::string& name, TableFormat format = TableFormat::JSON);
    bool RemoveTable(const std::string& tableId);
    bool RenameTable(const std::string& tableId, const std::string& newName);

    std::string AddColumn(const std::string& tableId, const std::string& name, ColumnType type);
    bool RemoveColumn(const std::string& tableId, const std::string& columnId);
    bool SetColumnDefault(const std::string& tableId, const std::string& columnId, const std::string& defaultValue);
    bool SetColumnRequired(const std::string& tableId, const std::string& columnId, bool required);

    std::string AddRow(const std::string& tableId);
    bool RemoveRow(const std::string& tableId, const std::string& rowId);
    bool SetCell(const std::string& tableId, const std::string& rowId, const std::string& columnId, const std::string& value);
    std::string GetCell(const std::string& tableId, const std::string& rowId, const std::string& columnId) const;

    const RowData* GetRow(const std::string& tableId, const std::string& rowId) const;
    std::vector<std::string> GetRowIds(const std::string& tableId) const;
    std::vector<std::string> FilterRows(const std::string& tableId, const std::string& columnId, const std::string& value) const;

    const TableSchema* GetSchema(const std::string& tableId) const;
    int GetTableCount() const;
    std::vector<std::string> GetTableIds() const;

    bool ImportTable(const std::string& filePath, TableFormat format = TableFormat::CSV);
    bool ExportTable(const std::string& tableId, const std::string& filePath, TableFormat format = TableFormat::CSV) const;
    TableDiff DiffTables(const std::string& tableIdA, const std::string& tableIdB) const;

    bool SaveTable(const std::string& filePath) const;
    bool LoadTable(const std::string& filePath);
    void ClearAll();

private:
    bool m_active{false};
    std::unordered_map<std::string, TableSchema> m_schemas;
    std::unordered_map<std::string, std::unordered_map<std::string, RowData>> m_rows;
    int m_nextTableIndex{0};
    int m_nextRowIndex{0};
    int m_nextColumnIndex{0};
};

} // namespace Atlas::Editor
