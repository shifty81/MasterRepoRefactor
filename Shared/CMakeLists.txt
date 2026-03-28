# Shared — bridge contracts, manifests, and protocol types

include(SharedTargets)

# AtlasBridgeContract: C++ header-only interface library
add_library(AtlasBridgeContract INTERFACE)
target_include_directories(AtlasBridgeContract
    INTERFACE "${CMAKE_CURRENT_SOURCE_DIR}/AtlasBridgeContract/include"
)

message(STATUS "Shared: AtlasBridgeContract configured")
