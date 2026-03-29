#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P24 Tool — Blueprint macro library authoring, tunnel I/O management, and macro call graph analysis.
class BlueprintMacroLibraryTool : public ITool {
public:
    enum class MacroScope { Local, Global, Plugin, Project, Engine, Custom };
    enum class TunnelIOType { Input, Output, Bidirectional, Custom };
    enum class MacroParamType { Bool, Int, Float, String, Object, Struct, Custom };
    enum class MacroCallMode { Inline, Latent, Async, Macro, Custom };

    struct MacroLibraryDef {
        std::string libraryId;
        std::string libraryName;
        MacroScope scope{MacroScope::Local};
        std::string ownerClass;
        std::vector<std::string> macroIds;
    };

    struct MacroTunnelIO {
        std::string tunnelId;
        std::string macroId;
        TunnelIOType ioType{TunnelIOType::Input};
        MacroParamType paramType{MacroParamType::Bool};
        std::string paramName;
        std::string defaultValue;
    };

    struct MacroCallRecord {
        std::string callId;
        std::string macroId;
        MacroCallMode callMode{MacroCallMode::Inline};
        std::string callerNodeId;
        bool resolved{false};
        int callDepth{0};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "BlueprintMacroLibraryTool"; }
    bool IsActive() const override { return m_active; }

    std::string CreateLibrary(const MacroLibraryDef& def);
    bool DeleteLibrary(const std::string& libraryId);
    const MacroLibraryDef* GetLibrary(const std::string& libraryId) const;
    std::vector<std::string> GetAllLibraryIds() const;
    std::vector<std::string> GetLibrariesByScope(MacroScope scope) const;
    bool AddMacroToLibrary(const std::string& libraryId, const std::string& macroId);
    bool RemoveMacroFromLibrary(const std::string& libraryId, const std::string& macroId);
    std::vector<std::string> GetMacrosInLibrary(const std::string& libraryId) const;
    bool AddTunnel(const MacroTunnelIO& tunnel);
    bool RemoveTunnel(const std::string& tunnelId);
    const MacroTunnelIO* GetTunnel(const std::string& tunnelId) const;
    std::vector<std::string> GetTunnelsByMacro(const std::string& macroId) const;
    std::vector<std::string> GetInputTunnels(const std::string& macroId) const;
    std::vector<std::string> GetOutputTunnels(const std::string& macroId) const;
    bool RecordCall(const MacroCallRecord& record);
    const MacroCallRecord* GetCall(const std::string& callId) const;
    std::vector<std::string> GetCallsByMacro(const std::string& macroId) const;
    std::vector<std::string> GetUnresolvedCalls() const;
    void AnalyzeCallGraph();
    void Reset();

private:
    bool m_active{false};
    std::unordered_map<std::string, MacroLibraryDef> m_libraries;
    std::unordered_map<std::string, MacroTunnelIO> m_tunnels;
    std::unordered_map<std::string, MacroCallRecord> m_calls;
};

} // namespace Atlas::Editor
