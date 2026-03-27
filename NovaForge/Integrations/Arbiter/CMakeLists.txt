# NovaForge Arbiter Integration — bridge service for AI tooling

set(NOVAFORGE_ARBITER_INTEGRATION_SOURCES
    src/ArbiterBridgeService.cpp
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

masterrepo_set_compiler_warnings(NovaForgeIntegrationArbiter)

message(STATUS "NovaForgeIntegrationArbiter: configured")
