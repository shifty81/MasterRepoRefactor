# Integration tests

# Epic 5 / Task 9 — Context, session, and bootstrap tests.
# These are shipping-safe: no dependency on AtlasBridgeService.
masterrepo_add_test(
    NovaForgeContextTest
    SOURCES novaforge_context_test.cpp
    DEPS    NovaForgeApp
)

if(NOVAFORGE_ENABLE_ATLASAI_INTEGRATION)
    # Verify the bridge service, session manager, and audit logger work together.
    masterrepo_add_test(
        BridgeServiceIntegrationTest
        SOURCES bridge_service_integration_test.cpp
        DEPS    NovaForgeIntegrationAtlasAI
    )

    # Epic 9 — End-to-end workflow milestone: bridge endpoints tasks 9.1–9.5.
    masterrepo_add_test(
        NovaForgeWorkflowTest
        SOURCES novaforge_workflow_test.cpp
        DEPS    NovaForgeIntegrationAtlasAI
    )

    # Epic 10 — Second-wave improvements: tasks 10.1–10.5.
    masterrepo_add_test(
        NovaForgeEpic10Test
        SOURCES novaforge_epic10_test.cpp
        DEPS    NovaForgeIntegrationAtlasAI
    )

    # MasterRepo NovaForge Live Ingestion — lifecycle, capture, callback tests.
    masterrepo_add_test(
        LiveIngestionTest
        SOURCES live_ingestion_test.cpp
        DEPS    NovaForgeIntegrationAtlasAI
    )
endif()

message(STATUS "Tests/Integration: configured")
