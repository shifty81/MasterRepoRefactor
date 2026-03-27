# Shared — bridge contracts, manifests, and protocol types

include(SharedTargets)

# ArbiterBridgeContract: C++ header-only interface library
add_library(ArbiterBridgeContract INTERFACE)
target_include_directories(ArbiterBridgeContract
    INTERFACE "${CMAKE_CURRENT_SOURCE_DIR}/ArbiterBridgeContract/include"
)

message(STATUS "Shared: ArbiterBridgeContract configured")
