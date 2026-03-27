# Integration tests

if(NOVAFORGE_ENABLE_ARBITER_INTEGRATION)
    # Verify the bridge service, session manager, and audit logger work together.
    masterrepo_add_test(
        BridgeServiceIntegrationTest
        SOURCES bridge_service_integration_test.cpp
        DEPS    NovaForgeIntegrationArbiter
    )
endif()

message(STATUS "Tests/Integration: configured")
