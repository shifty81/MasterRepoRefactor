# AtlasCore — core primitives, containers, memory, math, IO, logging

set(ATLAS_CORE_SOURCES
    # placeholder — add source files here as they are created
)

add_library(AtlasCore STATIC ${ATLAS_CORE_SOURCES})

target_include_directories(AtlasCore
    PUBLIC  "${CMAKE_CURRENT_SOURCE_DIR}"
    PRIVATE "${CMAKE_CURRENT_SOURCE_DIR}"
)

masterrepo_set_compiler_warnings(AtlasCore)

message(STATUS "AtlasCore: configured")
