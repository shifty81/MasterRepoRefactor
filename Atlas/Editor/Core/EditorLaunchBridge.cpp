// EditorLaunchBridge.cpp
// Atlas Editor — editor boot sequence implementation.

#include "EditorLaunchBridge.h"
#include "../../Engine/Config/LaunchConfig.h"
#include "../../Engine/Core/GameSystemsRegistry.h"
#include <iostream>

namespace atlas::editor
{

// ---------------------------------------------------------------------------
// Boot
// ---------------------------------------------------------------------------

EditorBootResult EditorLaunchBridge::Boot(const atlas::LaunchParams& params)
{
    if (m_booted)
        return { false, "EditorLaunchBridge::Boot called more than once" };

    std::string err;

    if (!BootCore(params, err))
        return { false, "Core boot failed: " + err };

    if (!BootEditorSubsystems(params, err))
        return { false, "Editor subsystem boot failed: " + err };

    if (params.enableBridge)
    {
        if (!BootAtlasAIBridge(params, err))
            return { false, "AtlasAI bridge boot failed: " + err };
    }

    m_booted = true;
    std::cout << "[EditorLaunchBridge] Boot complete (mode=Editor"
              << (params.enableBridge ? ", bridge=on" : "")
              << (params.devMode ? ", dev=on" : "")
              << ")\n";
    return { true, "OK" };
}

// ---------------------------------------------------------------------------
// Shutdown
// ---------------------------------------------------------------------------

void EditorLaunchBridge::Shutdown()
{
    if (!m_booted) return;
    std::cout << "[EditorLaunchBridge] Shutting down\n";
    // Subsystems shut down in reverse registration order through GameSystemsRegistry.
    auto& reg = atlas::GameSystemsRegistry::Get();
    for (const auto& entry : reg.All())
    {
        if (entry.category == "Editor")
            reg.SetState(entry.name, atlas::ESystemState::Shutdown);
    }
    m_booted = false;
}

// ---------------------------------------------------------------------------
// Private helpers
// ---------------------------------------------------------------------------

bool EditorLaunchBridge::BootCore(const atlas::LaunchParams& /*params*/,
                                   std::string& /*err*/)
{
    auto& reg = atlas::GameSystemsRegistry::Get();
    reg.Register("AtlasEngine::Core", "Engine");
    reg.Register("AtlasEngine::ECS", "Engine");
    reg.Register("AtlasEngine::EventBus", "Engine");
    reg.Register("AtlasEngine::Logger", "Engine");

    // Simulate successful boot of core systems.
    reg.MarkReady("AtlasEngine::Core");
    reg.MarkReady("AtlasEngine::ECS");
    reg.MarkReady("AtlasEngine::EventBus");
    reg.MarkReady("AtlasEngine::Logger");
    return true;
}

bool EditorLaunchBridge::BootEditorSubsystems(const atlas::LaunchParams& /*params*/,
                                               std::string& /*err*/)
{
    auto& reg = atlas::GameSystemsRegistry::Get();
    const uint32_t mask = static_cast<uint32_t>(m_mask);

    auto bootIfEnabled = [&](EEditorSubsystem sys, const char* name) {
        if (mask & static_cast<uint32_t>(sys))
        {
            reg.Register(name, "Editor");
            reg.MarkReady(name);
        }
    };

    bootIfEnabled(EEditorSubsystem::Core,            "Editor::Core");
    bootIfEnabled(EEditorSubsystem::Outliner,        "Editor::Outliner");
    bootIfEnabled(EEditorSubsystem::Inspector,       "Editor::Inspector");
    bootIfEnabled(EEditorSubsystem::Viewport,        "Editor::Viewport");
    bootIfEnabled(EEditorSubsystem::AssetBrowser,    "Editor::AssetBrowser");
    bootIfEnabled(EEditorSubsystem::Gizmos,          "Editor::Gizmos");
    bootIfEnabled(EEditorSubsystem::CommandStack,    "Editor::CommandStack");
    bootIfEnabled(EEditorSubsystem::ValidationPanel, "Editor::ValidationPanel");
    bootIfEnabled(EEditorSubsystem::DocsPanel,       "Editor::DocsPanel");
    bootIfEnabled(EEditorSubsystem::DiffReview,      "Editor::DiffReview");
    return true;
}

bool EditorLaunchBridge::BootAtlasAIBridge(const atlas::LaunchParams& params,
                                            std::string& /*err*/)
{
    auto& reg = atlas::GameSystemsRegistry::Get();
    reg.Register("AtlasAI::Bridge", "AI");
    // Bridge server initialisation is handled by NovaForgeBootstrap when
    // NOVAFORGE_BRIDGE_SERVER_ENABLED is defined.  Here we just record intent.
    std::cout << "[EditorLaunchBridge] AtlasAI bridge requested on port "
              << params.bridgePort << " (startup deferred to NovaForgeBootstrap)\n";
    reg.MarkReady("AtlasAI::Bridge");
    return true;
}

} // namespace atlas::editor
