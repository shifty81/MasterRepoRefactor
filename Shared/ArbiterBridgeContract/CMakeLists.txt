add_library(ArbiterBridgeContract INTERFACE)

target_include_directories(ArbiterBridgeContract
    INTERFACE
        ${CMAKE_CURRENT_SOURCE_DIR}/include
)

target_compile_features(ArbiterBridgeContract INTERFACE cxx_std_20)
