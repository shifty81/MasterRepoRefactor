# AtlasEngine — ECS, world, scene, assets, rendering, physics, audio

set(ATLAS_ENGINE_SOURCES
    src/AtlasEngine_stub.cpp
    Rendering/Renderer.cpp
    Rendering/RenderViewport.cpp
    Input/InputManager.cpp
    Input/InputContextManager.cpp
    AssetPipeline/AssetNamingRules.cpp
    AssetPipeline/AssetImportValidator.cpp
    Physics/PhysicsWorld.cpp
    Physics/PhysicsExtensions.cpp
    Audio/AudioEngine.cpp
    Audio/AudioSystem.cpp
    Networking/NetSession.cpp
    Scripting/ScriptingVM.cpp
    # J3 — Keybind config
    Config/KeybindConfig.cpp
    # J4 — Save/load extensions
    SaveLoad/SaveLoadExtensions.cpp
    # J5 — Asset import rules
    AssetPipeline/AssetImportRules.cpp
    # J6 — PCG determinism engine
    PCG/PCGDeterminismEngine.cpp
    # J8 — Schema version registry
    Config/SchemaVersionRegistry.cpp
    # Phase 11 — Scene subsystem
    Scene/SceneNode.cpp
    Scene/SceneGraph.cpp
    Scene/SceneManager.cpp
    # add source files here as engine systems are implemented
)

add_library(AtlasEngine STATIC ${ATLAS_ENGINE_SOURCES})

target_include_directories(AtlasEngine
    PUBLIC  "${CMAKE_CURRENT_SOURCE_DIR}"
             "${CMAKE_CURRENT_SOURCE_DIR}/Rendering"
             "${CMAKE_CURRENT_SOURCE_DIR}/Input"
             "${CMAKE_CURRENT_SOURCE_DIR}/AssetPipeline"
             "${CMAKE_CURRENT_SOURCE_DIR}/Physics"
             "${CMAKE_CURRENT_SOURCE_DIR}/Audio"
             "${CMAKE_CURRENT_SOURCE_DIR}/Networking"
             "${CMAKE_CURRENT_SOURCE_DIR}/Scripting"
             "${CMAKE_CURRENT_SOURCE_DIR}/Config"
             "${CMAKE_CURRENT_SOURCE_DIR}/SaveLoad"
             "${CMAKE_CURRENT_SOURCE_DIR}/PCG"
             "${CMAKE_CURRENT_SOURCE_DIR}/Scene"
    PRIVATE "${CMAKE_CURRENT_SOURCE_DIR}"
)

target_link_libraries(AtlasEngine PUBLIC AtlasCore)

masterrepo_set_compiler_warnings(AtlasEngine)

message(STATUS "AtlasEngine: configured")
