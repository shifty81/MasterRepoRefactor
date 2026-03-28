# Shared — bridge contracts, manifests, and protocol types

include(SharedTargets)

# AtlasBridgeContract: C++ header-only interface library
add_library(AtlasBridgeContract INTERFACE)
target_include_directories(AtlasBridgeContract
    INTERFACE "${CMAKE_CURRENT_SOURCE_DIR}/AtlasBridgeContract/include"
)

# MasterLogger: header-only shared logging library (C++17)
add_library(MasterLogger INTERFACE)
target_include_directories(MasterLogger
    INTERFACE "${CMAKE_SOURCE_DIR}"
)
target_compile_features(MasterLogger INTERFACE cxx_std_17)

message(STATUS "Shared: AtlasBridgeContract configured")
message(STATUS "Shared: MasterLogger (header-only) configured")
