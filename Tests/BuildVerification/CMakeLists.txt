# Build verification tests

# Verify that the AtlasBridgeContract header compiles and all types are accessible.
masterrepo_add_test(
    BridgeTypesCompileTest
    SOURCES bridge_types_compile_test.cpp
    DEPS    AtlasBridgeContract
)

message(STATUS "Tests/BuildVerification: configured")
