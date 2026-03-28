# AtlasEngine — ECS, world, scene, assets, rendering, physics, audio

set(ATLAS_ENGINE_SOURCES
    src/AtlasEngine_stub.cpp
    # add source files here as engine systems are implemented
)

add_library(AtlasEngine STATIC ${ATLAS_ENGINE_SOURCES})

target_include_directories(AtlasEngine
    PUBLIC  "${CMAKE_CURRENT_SOURCE_DIR}"
    PRIVATE "${CMAKE_CURRENT_SOURCE_DIR}"
)

target_link_libraries(AtlasEngine PUBLIC AtlasCore)

masterrepo_set_compiler_warnings(AtlasEngine)

message(STATUS "AtlasEngine: configured")
