# Build verification tests

# Verify that the ArbiterBridgeContract header compiles and all types are accessible.
masterrepo_add_test(
    BridgeTypesCompileTest
    SOURCES bridge_types_compile_test.cpp
    DEPS    ArbiterBridgeContract
)

message(STATUS "Tests/BuildVerification: configured")
