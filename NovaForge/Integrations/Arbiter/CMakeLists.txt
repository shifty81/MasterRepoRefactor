# NovaForge Arbiter Integration — bridge service for AI tooling

set(NOVAFORGE_ARBITER_INTEGRATION_SOURCES
    src/ArbiterBridgeService.cpp
    src/BridgeSessionManager.cpp
    src/BridgeAuditLogger.cpp
)

add_library(NovaForgeIntegrationArbiter STATIC
    ${NOVAFORGE_ARBITER_INTEGRATION_SOURCES}
)

target_include_directories(NovaForgeIntegrationArbiter
    PUBLIC
        "${CMAKE_CURRENT_SOURCE_DIR}/include"
        "${CMAKE_SOURCE_DIR}/Shared/ArbiterBridgeContract/include"
    PRIVATE
        "${CMAKE_CURRENT_SOURCE_DIR}/src"
)

target_link_libraries(NovaForgeIntegrationArbiter
    PUBLIC
        ArbiterBridgeContract
        AtlasRuntime
)

# Epic 7 / Task 7.5: propagate compile-time feature guards
if(NOVAFORGE_ENABLE_BRIDGE_SERVER)
    target_compile_definitions(NovaForgeIntegrationArbiter
        PUBLIC NOVAFORGE_BRIDGE_SERVER_ENABLED=1)
endif()

if(NOVAFORGE_ENABLE_AUDIT_LOGGING)
    target_compile_definitions(NovaForgeIntegrationArbiter
        PUBLIC NOVAFORGE_AUDIT_LOGGING_ENABLED=1)
endif()

masterrepo_set_compiler_warnings(NovaForgeIntegrationArbiter)

message(STATUS "NovaForgeIntegrationArbiter: configured")
