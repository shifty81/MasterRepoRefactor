# NovaForge — game project, gameplay systems, data, content

include(NovaForgeTargets)

add_subdirectory(Gameplay)
add_subdirectory(World)

if(NOVAFORGE_ENABLE_ARBITER_INTEGRATION)
    add_subdirectory(Integrations/Arbiter)
endif()

# App depends on the integration layer when the bridge is enabled,
# so it must be added after Integrations/Arbiter.
add_subdirectory(App)

message(STATUS "NovaForge: modules configured")
