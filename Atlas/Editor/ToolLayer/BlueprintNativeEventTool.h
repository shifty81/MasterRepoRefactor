#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P27 Tool — Blueprint native event binding, C++ override stub generation, and event graph wiring.
class BlueprintNativeEventTool : public ITool {
public:
    enum class EventBindingType { NativeOverride, ImplementableEvent, MulticastDelegate, Interface, Custom };
    enum class EventVisibility { Public, Protected, Private, Custom };
    enum class StubGenMode { Header, Implementation, Both, Custom };
    enum class EventCallConvention { BlueprintCallable, BlueprintPure, BlueprintImplementableEvent, Custom };

    struct NativeEventDef {
        std::string eventId;
        std::string eventName;
        std::string className;
        EventBindingType bindingType{EventBindingType::NativeOverride};
        EventVisibility visibility{EventVisibility::Public};
        std::string returnType;
        std::string paramList;
        bool isConst{false};
        bool enabled{true};
    };

    struct StubGenDef {
        std::string stubGenId;
        std::string eventId;
        StubGenMode genMode{StubGenMode::Both};
        std::string outputHeaderPath;
        std::string outputCppPath;
        bool includeUFUNCTION{true};
        EventCallConvention callConvention{EventCallConvention::BlueprintCallable};
        bool generated{false};
    };

    struct EventGraphWireDef {
        std::string wireId;
        std::string eventId;
        std::string sourcePinId;
        std::string targetPinId;
        std::string graphId;
        bool breakable{true};
        bool enabled{true};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "BlueprintNativeEventTool"; }
    bool IsActive() const override { return m_active; }

    bool RegisterEvent(const NativeEventDef& def);
    bool UnregisterEvent(const std::string& eventId);
    bool SetEventVisibility(const std::string& eventId, EventVisibility visibility);
    const NativeEventDef* GetEvent(const std::string& eventId) const;
    std::vector<std::string> GetAllEventIds() const;
    std::vector<std::string> GetEventsByClass(const std::string& className) const;
    std::vector<std::string> GetEventsByBindingType(EventBindingType type) const;
    bool CreateStubGen(const StubGenDef& def);
    bool DeleteStubGen(const std::string& stubGenId);
    bool GenerateStub(const std::string& stubGenId);
    const StubGenDef* GetStubGen(const std::string& stubGenId) const;
    std::vector<std::string> GetStubGensByEvent(const std::string& eventId) const;
    std::vector<std::string> GetGeneratedStubs() const;
    bool AddWire(const EventGraphWireDef& wire);
    bool RemoveWire(const std::string& wireId);
    bool BreakWire(const std::string& wireId);
    const EventGraphWireDef* GetWire(const std::string& wireId) const;
    std::vector<std::string> GetWiresByEvent(const std::string& eventId) const;
    std::vector<std::string> GetWiresByGraph(const std::string& graphId) const;
    void Reset();

private:
    bool m_active{false};
    std::unordered_map<std::string, NativeEventDef> m_events;
    std::unordered_map<std::string, StubGenDef> m_stubGens;
    std::unordered_map<std::string, EventGraphWireDef> m_wires;
};

} // namespace Atlas::Editor
