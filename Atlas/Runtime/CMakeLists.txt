# AtlasRuntime — application framework, game loop, simulation, save/load

set(ATLAS_RUNTIME_SOURCES
    # placeholder — add source files here as they are created
)

add_library(AtlasRuntime STATIC ${ATLAS_RUNTIME_SOURCES})

target_include_directories(AtlasRuntime
    PUBLIC  "${CMAKE_CURRENT_SOURCE_DIR}"
    PRIVATE "${CMAKE_CURRENT_SOURCE_DIR}"
)

target_link_libraries(AtlasRuntime PUBLIC AtlasEngine)

masterrepo_set_compiler_warnings(AtlasRuntime)

message(STATUS "AtlasRuntime: configured")
