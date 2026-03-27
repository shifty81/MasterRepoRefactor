# NovaForge — game project, gameplay systems, data, content

include(NovaForgeTargets)

add_subdirectory(App)
add_subdirectory(Gameplay)
add_subdirectory(World)

if(NOVAFORGE_ENABLE_ARBITER_INTEGRATION)
    add_subdirectory(Integrations/Arbiter)
endif()

message(STATUS "NovaForge: modules configured")
