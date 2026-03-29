add_library(NovaForgeIntegrationArbiter STATIC
    ArbiterBridgeService.cpp
)

target_include_directories(NovaForgeIntegrationArbiter
    PUBLIC
        ${CMAKE_CURRENT_SOURCE_DIR}
)

target_link_libraries(NovaForgeIntegrationArbiter
    PUBLIC
        ArbiterBridgeContract
        AtlasEditor
        NovaForgeTools
)

target_compile_definitions(NovaForgeIntegrationArbiter
    PUBLIC
        NOVAFORGE_WITH_ARBITER_BRIDGE=1
)
