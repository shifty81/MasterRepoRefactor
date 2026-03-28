# NovaForge App — bootstrap, session, project context

set(NOVAFORGE_APP_SOURCES
    src/NovaForgeApp_stub.cpp
    src/NovaForgeProjectContext.cpp
    src/NovaForgeSession.cpp
    src/NovaForgeBootstrap.cpp
)

add_library(NovaForgeApp STATIC ${NOVAFORGE_APP_SOURCES})

target_include_directories(NovaForgeApp
    PUBLIC
        "${CMAKE_CURRENT_SOURCE_DIR}/include"
    PRIVATE
        "${CMAKE_CURRENT_SOURCE_DIR}"
)

target_link_libraries(NovaForgeApp PUBLIC AtlasRuntime)

# When bridge is enabled, NovaForgeApp links the integration layer so that
# NovaForgeBootstrap can start the ArbiterBridgeService.
if(NOVAFORGE_ENABLE_ARBITER_INTEGRATION AND NOVAFORGE_ENABLE_BRIDGE_SERVER)
    target_link_libraries(NovaForgeApp PRIVATE NovaForgeIntegrationArbiter)
    target_compile_definitions(NovaForgeApp
        PRIVATE NOVAFORGE_BRIDGE_SERVER_ENABLED=1)
    target_include_directories(NovaForgeApp
        PRIVATE
            "${CMAKE_SOURCE_DIR}/NovaForge/Integrations/Arbiter/include"
            "${CMAKE_SOURCE_DIR}/Shared/ArbiterBridgeContract/include"
    )
endif()

masterrepo_set_compiler_warnings(NovaForgeApp)

message(STATUS "NovaForgeApp: configured")
