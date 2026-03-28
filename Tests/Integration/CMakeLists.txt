# Integration tests

# Epic 5 / Task 9 — Context, session, and bootstrap tests.
# These are shipping-safe: no dependency on ArbiterBridgeService.
masterrepo_add_test(
    NovaForgeContextTest
    SOURCES novaforge_context_test.cpp
    DEPS    NovaForgeApp
)

if(NOVAFORGE_ENABLE_ARBITER_INTEGRATION)
    # Verify the bridge service, session manager, and audit logger work together.
    masterrepo_add_test(
        BridgeServiceIntegrationTest
        SOURCES bridge_service_integration_test.cpp
        DEPS    NovaForgeIntegrationArbiter
    )

    # Epic 9 — End-to-end workflow milestone: bridge endpoints tasks 9.1–9.5.
    masterrepo_add_test(
        NovaForgeWorkflowTest
        SOURCES novaforge_workflow_test.cpp
        DEPS    NovaForgeIntegrationArbiter
    )

    # Epic 10 — Second-wave improvements: tasks 10.1–10.5.
    masterrepo_add_test(
        NovaForgeEpic10Test
        SOURCES novaforge_epic10_test.cpp
        DEPS    NovaForgeIntegrationArbiter
    )
endif()

message(STATUS "Tests/Integration: configured")
